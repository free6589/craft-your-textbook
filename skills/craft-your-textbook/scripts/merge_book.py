# -*- coding: utf-8 -*-
"""
合并脚本【示例模板】：将 chapters/ 下所有章 + appendix/ 下所有附录合并为 BOOK.md。

★★ 本文件是示例模板。造书时复制进项目（<项目根>/scripts/）→ 按需改顶部 LOADER_TEMPLATE 再跑。
    脚本自动扫描 chapters/ 和 appendix/ 目录，按文件名"自然序"（数字按数值比较）合并。

用法：
    python merge_book.py [项目根目录] [--strip-frontmatter]

设计要点：
- 读 META.md 顶部 YAML format 字段判断路线（容忍行内注释与引号）
- human-readable 路线在 BOOK.md 顶部注入 loader 指令
- 章序按自然序：chapter-2 排在 chapter-10 之前（不必零填充）
- 零章时非零退出，不产出空 BOOK.md
- 可重跑
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

DEFAULT_BASE_DIR = "."
VALID_FORMATS = ("pure-blueprint", "human-readable")


def _natural_key(path):
    """自然序排序键：数字块按数值比，其余按字符串比。

    修 B-02：原实现 sorted(Path) 走字符串比较，chapter-10.md 会排到 chapter-2.md 前。
    这里把路径每一段切成"数字块/非数字块"序列，数字块比较数值。
    """
    key = []
    for part in path.parts:
        for chunk in re.split(r"(\d+)", part):
            if not chunk:
                continue
            if chunk.isdigit():
                key.append((0, int(chunk), ""))
            else:
                key.append((1, 0, chunk))
    return key


def read_meta_format(base_dir):
    """读 META.md 顶部 YAML 的 format 字段。

    修 H-01：原实现把 `format:` 之后整行直接 strip() 返回，导致
    `format: human-readable   # 人读版` 与 `format: "human-readable"` 都不等于
    "human-readable" → loader 静默不注入。这里去行内注释、去引号，并对无法识别的
    取值显式告警（不再静默回落）。
    """
    meta_path = Path(base_dir) / "META.md"
    if not meta_path.exists():
        return "pure-blueprint"
    content = meta_path.read_text(encoding="utf-8")
    # 匹配顶部 --- ... --- 之间的 YAML
    m = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not m:
        return "pure-blueprint"
    fm = re.search(r"^format:\s*(.+)$", m.group(1), re.MULTILINE)
    if not fm:
        return "pure-blueprint"
    raw = fm.group(1)
    # 去行内注释（# 之后），再去引号
    val = raw.split("#", 1)[0].strip().strip("\"'").strip()
    if val not in VALID_FORMATS:
        print(
            f"[warn] META.md 的 format 取值无法识别：{raw!r}；"
            f"按 pure-blueprint 处理（不注入 loader）。合法值：{', '.join(VALID_FORMATS)}",
            file=sys.stderr,
        )
        return "pure-blueprint"
    return val


def load_chapters(base_dir):
    """递归扫描 chapters/ 下所有 *.md（排除进度 ledger progress.md），按自然序排序。"""
    chapters_dir = Path(base_dir) / "chapters"
    if not chapters_dir.exists():
        return []
    files = [f for f in chapters_dir.rglob("*.md") if f.name != "progress.md"]
    no_digit = [f.name for f in files if not re.search(r"\d", f.name)]
    if no_digit:
        print(
            f"[warn] 以下章文件名不含数字，自然序下按字符串排，位置可能不符预期：{no_digit}",
            file=sys.stderr,
        )
    return sorted(files, key=_natural_key)


def load_appendices(base_dir):
    """扫描 appendix/ 下所有 *.md，按自然序排序。"""
    app_dir = Path(base_dir) / "appendix"
    if not app_dir.exists():
        return []
    return sorted(app_dir.glob("*.md"), key=_natural_key)


def strip_frontmatter(content):
    """剥离 YAML frontmatter（--- ... ---）。"""
    return re.sub(r"^---\s*\n.*?\n---\n?", "", content, count=1, flags=re.DOTALL)


LOADER_TEMPLATE = """> **AI 老师使用说明**：本书是给人读的流畅教材。正文 prose 是素材库，用你自己的话重组教学；
> 每章末尾的思考题/练习区是提问路线图，请照那些问题的层次引导学生。

---

"""


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="合并 chapters/ 与 appendix/ 为 BOOK.md（自然序、读 META 定路线）"
    )
    parser.add_argument("base_dir", nargs="?", default=DEFAULT_BASE_DIR, help="项目根目录，默认当前目录")
    parser.add_argument(
        "--strip-frontmatter", action="store_true", help="合并时剥离各文件的 YAML frontmatter"
    )
    args = parser.parse_args(argv)

    base = Path(args.base_dir)
    # 修 M-02：基目录不存在时给友好错误，不抛裸 traceback
    if not base.is_dir():
        sys.exit(f"[error] 项目根目录不存在或不是目录：{base}")

    fmt = read_meta_format(base)
    chapters = load_chapters(base)
    appendices = load_appendices(base)

    # 修 M-01：零章时不再写 0 字节 BOOK.md 并宣称"合并完成"
    if not chapters:
        sys.exit(
            f"[error] 在 {base / 'chapters'} 下没找到任何章文件（*.md，progress.md 除外）。"
            "已中止，未写 BOOK.md。"
        )

    parts = []
    if fmt == "human-readable":
        parts.append(LOADER_TEMPLATE)

    for ch in chapters:
        content = ch.read_text(encoding="utf-8")
        if args.strip_frontmatter:
            content = strip_frontmatter(content)
        if not content.endswith("\n"):
            content += "\n"
        parts.append(content)
        parts.append("\n---\n\n")

    if appendices:
        parts.append("# 附录\n\n")
        for ap in appendices:
            content = ap.read_text(encoding="utf-8")
            if args.strip_frontmatter:
                content = strip_frontmatter(content)
            if not content.endswith("\n"):
                content += "\n"
            parts.append(content)
            parts.append("\n")

    output_path = base / "BOOK.md"
    output_path.write_text("".join(parts), encoding="utf-8")

    size = output_path.stat().st_size
    lines = output_path.read_text(encoding="utf-8").count("\n")
    print(f"合并完成：{output_path}")
    print(f"路线：{fmt}")
    print(f"章数：{len(chapters)}，附录：{len(appendices)}")
    print(f"文件大小：{size:,} 字节 / {lines:,} 行")
    print("章序：" + " → ".join(ch.name for ch in chapters))


if __name__ == "__main__":
    main()
