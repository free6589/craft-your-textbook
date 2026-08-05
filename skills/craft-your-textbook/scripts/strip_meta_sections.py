# -*- coding: utf-8 -*-
"""
拆脚手架脚本【示例模板】（造书 Phase 6）：
删除章文件末尾的"脚手架"板块（自检清单/版本记录/写作笔记等写作过程元数据）。

★★ 本文件是示例模板。复制进项目后运行。脚手架标题列表从 META.md 读（META #10）。

用法：
    python strip_meta_sections.py [目录1] [目录2] ...
    # 默认递归扫描 chapters/ 和 appendix/

★ 删完后必须重跑 merge_book.py 重新合并 BOOK.md。
"""
import re
import sys
from pathlib import Path

# Windows 控制台默认 GBK，强制 UTF-8 输出，避免 emoji/中文 print 崩溃
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

DEFAULT_DIRS = ["chapters", "appendix"]


def read_scaffold_titles(base_dir):
    """从 META.md 读脚手架标题列表（META #10）。
    找到含"脚手架标题"的那一行，把其后所有 `- item` 列表条目收为标题（容忍缩进）。
    找不到或没条目 → 返回默认值并打警告（不静默）。
    """
    meta_path = Path(base_dir) / "META.md"
    defaults = ["## 📋 自检清单", "## 📜 版本记录", "## 写作笔记"]
    if not meta_path.exists():
        print("[warn] 没找到 META.md，用默认脚手架标题", file=sys.stderr)
        return defaults
    content = meta_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    start = next((i for i, ln in enumerate(lines) if "脚手架标题" in ln), None)
    if start is None:
        print("[warn] META 里没找到'脚手架标题'小节，用默认标题（可能漏拆自定义标题）", file=sys.stderr)
        return defaults
    titles = []
    for ln in lines[start + 1:]:
        s = ln.strip()
        m = re.match(r"^[-*]\s+(.+)$", s)
        if m:
            titles.append(m.group(1).strip().strip("`"))
        elif titles:
            break  # 已开始收集列表，遇到非列表行 = 列表结束
        # 未开始收集时跳过空行/说明行，继续找第一条列表项
    if not titles:
        print("[warn] '脚手架标题'后没有列表条目，用默认标题", file=sys.stderr)
        return defaults
    return titles


def process_file(path, markers):
    """从找到第一个 marker 行处截断文件到末尾。返回删除的字符数。"""
    content = path.read_text(encoding="utf-8")
    cut_idx = len(content)
    for marker in markers:
        idx = content.find(marker)
        if idx != -1 and idx < cut_idx:
            cut_idx = idx
    if cut_idx == len(content):
        return 0
    removed = content[cut_idx:]
    new_content = content[:cut_idx].rstrip() + "\n"
    path.write_text(new_content, encoding="utf-8")
    return len(removed)


def main():
    args = sys.argv[1:]
    dirs = args if args else DEFAULT_DIRS
    base_dir = "."

    markers = read_scaffold_titles(base_dir)
    print(f"脚手架标题：{markers}")

    total_removed = 0
    files_changed = 0

    for dirname in dirs:
        d = Path(base_dir) / dirname
        if not d.exists():
            print(f"[skip] 目录不存在：{d}")
            continue
        for f in sorted(d.rglob("*.md")):
            removed = process_file(f, markers)
            if removed > 0:
                lines = f.read_text(encoding="utf-8").count("\n")
                print(f"[ok]   {f}: 删除 {removed:,} 字符")
                total_removed += removed
                files_changed += 1
            else:
                print(f"[skip] {f}: 未找到脚手架标题")

    print("-" * 60)
    print(f"完成：{files_changed} 个文件，共删除 {total_removed:,} 字符")
    print("★ 记得重跑 merge_book.py 重新合并 BOOK.md")


if __name__ == "__main__":
    main()