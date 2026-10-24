# -*- coding: utf-8 -*-
"""
拆脚手架脚本【示例模板】（造书 Phase 6）：
删除章文件末尾的"脚手架"板块（自检清单/版本记录/写作笔记等写作过程元数据）。

★★ 本文件是示例模板。复制进项目后运行。脚手架标题列表从 META.md 读（META #10）。

用法：
    python strip_meta_sections.py [目录1] [目录2] ... [--dry-run] [--no-backup]
    # 默认递归扫描 chapters/ 和 appendix/

安全约束（本脚本会就地改写章文件）：
- 只按**整行标题**匹配，不做子串匹配；正文里出现同名文字（引用、代码块、三级标题）不会被误删
- 只在"尾部元数据区"截断：目标标题之后若还存在同级或更高级的非脚手架标题，就放弃该文件
- 改写前把原文备份为 <文件名>.bak（--no-backup 可关）
- --dry-run 只报告将删多少，不落盘

★ 删完后必须重跑 merge_book.py 重新合并 BOOK.md。
"""
import argparse
import re
import sys
from pathlib import Path

# Windows 控制台默认 GBK，强制 UTF-8 输出，避免 emoji/中文 print 崩溃
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

DEFAULT_DIRS = ["chapters", "appendix"]
DEFAULT_TITLES = ["## 📋 自检清单", "## 📜 版本记录", "## 写作笔记"]

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


def _norm(text):
    """归一化：折叠空白、去首尾空格。"""
    return re.sub(r"\s+", " ", text).strip()


def read_scaffold_titles(base_dir):
    """从 META.md 读脚手架标题列表（META #10）。

    修 H-02：原实现在列表中途遇到空行就 break，空行之后的标题全部丢失
    （脚手架残留且只打印 [skip]）。这里容忍空行与说明行，只在遇到新的标题行时结束小节。
    """
    meta_path = Path(base_dir) / "META.md"
    if not meta_path.exists():
        print("[warn] 没找到 META.md，用默认脚手架标题", file=sys.stderr)
        return list(DEFAULT_TITLES)
    content = meta_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    start = next((i for i, ln in enumerate(lines) if "脚手架标题" in ln), None)
    if start is None:
        print("[warn] META 里没找到'脚手架标题'小节，用默认标题（可能漏拆自定义标题）", file=sys.stderr)
        return list(DEFAULT_TITLES)

    titles = []
    for ln in lines[start + 1:]:
        s = ln.strip()
        # 遇到下一个标题行 = 小节结束
        if HEADING_RE.match(s):
            break
        m = re.match(r"^[-*]\s+(.+)$", s)
        if m:
            titles.append(m.group(1).strip().strip("`"))
        # 空行/说明行：继续往下找（不再 break）
    if not titles:
        print("[warn] '脚手架标题'后没有列表条目，用默认标题", file=sys.stderr)
        return list(DEFAULT_TITLES)
    return titles


def build_matchers(markers):
    """把标题字符串解析成 (level|None, normalized_title)。"""
    matchers = []
    for marker in markers:
        m = HEADING_RE.match(marker.strip())
        if m:
            matchers.append((len(m.group(1)), _norm(m.group(2))))
        else:
            matchers.append((None, _norm(marker)))
    return matchers


def match_heading(line, matchers):
    """该行是否是某个脚手架标题（整行标题匹配）。返回命中的 matcher 或 None。"""
    m = HEADING_RE.match(line)
    if not m:
        return None
    level = len(m.group(1))
    title = _norm(m.group(2))
    for matcher in matchers:
        m_level, m_title = matcher
        if title != m_title:
            continue
        if m_level is None or m_level == level:
            return matcher
    return None


def find_cut(lines, matchers):
    """返回应截断的行下标（0-based）；不该截断返回 None。

    修 B-01：原实现 content.find(marker) 子串定位 + 截断到 EOF，正文里出现一次
    标题字符串就会永久删掉其后全部教学内容。这里改为：
    1) 只匹配整行标题；
    2) 要求该标题之后不存在"同级或更高级的非脚手架标题"（即确属尾部元数据区）。
    """
    for i, line in enumerate(lines):
        hit = match_heading(line, matchers)
        if hit is None:
            continue
        level = len(HEADING_RE.match(line).group(1))
        safe = True
        for later in lines[i + 1:]:
            lm = HEADING_RE.match(later)
            if lm and len(lm.group(1)) <= level and match_heading(later, matchers) is None:
                safe = False
                break
        if safe:
            return i, hit
    return None, None


def process_file(path, matchers, dry_run=False, backup=True):
    """返回 (删除字符数, 命中的 matcher, 文件中出现过的所有 matcher)。"""
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines(keepends=True)
    # 本文件里出现过的全部脚手架标题（含被截断掉的那些），用于抑制"未命中"误报
    seen = {m for line in lines for m in [match_heading(line, matchers)] if m}

    cut, hit = find_cut(lines, matchers)
    if cut is None:
        return 0, None, seen

    new_content = "".join(lines[:cut]).rstrip() + "\n"
    removed = len(content) - len(new_content)
    if removed <= 0:
        return 0, None, seen
    if dry_run:
        return removed, hit, seen

    if backup:
        bak = path.with_name(path.name + ".bak")
        bak.write_text(content, encoding="utf-8")
    path.write_text(new_content, encoding="utf-8")
    return removed, hit, seen


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="删除章文件末尾的脚手架板块（整行标题匹配 + 尾部元数据区校验 + 自动备份）"
    )
    parser.add_argument("dirs", nargs="*", default=None, help="要扫描的目录，默认 chapters/ 与 appendix/")
    parser.add_argument("--base-dir", default=".", help="项目根目录（读 META.md 用），默认当前目录")
    parser.add_argument("--dry-run", action="store_true", help="只报告将删除多少，不落盘")
    parser.add_argument("--no-backup", action="store_true", help="不生成 .bak 备份（不建议）")
    args = parser.parse_args(argv)

    dirs = args.dirs or DEFAULT_DIRS
    base_dir = args.base_dir
    dry_run = args.dry_run
    backup = not args.no_backup

    markers = read_scaffold_titles(base_dir)
    matchers = build_matchers(markers)
    print(f"脚手架标题：{markers}")
    if dry_run:
        print("（dry-run：不写盘）")

    total_removed = 0
    files_changed = 0
    hit_matchers = set()

    for dirname in dirs:
        d = Path(base_dir) / dirname
        if not d.exists():
            print(f"[skip] 目录不存在：{d}")
            continue
        for f in sorted(d.rglob("*.md"), key=lambda p: p.as_posix()):
            if f.name.endswith(".bak"):
                continue
            removed, hit, seen = process_file(f, matchers, dry_run=dry_run, backup=backup)
            hit_matchers |= seen
            if removed > 0:
                tag = "would " if dry_run else ""
                print(f"[ok]   {f}: {tag}删除 {removed:,} 字符（自「{hit[1]}」起）")
                total_removed += removed
                files_changed += 1
            else:
                print(f"[skip] {f}: 未找到可安全截断的脚手架标题")

    unused = [m for m in matchers if m not in hit_matchers]
    if unused:
        print(
            "[warn] 以下脚手架标题在本轮没有任何文件命中（META 写错？或该板块确实不存在）："
            + ", ".join(f"{('#' * lv + ' ') if lv else ''}{t}" for lv, t in unused),
            file=sys.stderr,
        )

    print("-" * 60)
    verb = "将删除" if dry_run else "共删除"
    print(f"完成：{files_changed} 个文件，{verb} {total_removed:,} 字符")
    if not dry_run:
        print("★ 记得重跑 merge_book.py 重新合并 BOOK.md")
        if backup and files_changed:
            print("★ 原文已备份为同名 .bak，需要回滚就 mv 回去")


if __name__ == "__main__":
    main()
