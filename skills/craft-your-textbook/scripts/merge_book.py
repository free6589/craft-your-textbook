# -*- coding: utf-8 -*-
"""
合并脚本【示例模板】：将 chapters/ 下所有章 + appendix/ 下所有附录合并为 BOOK.md。

★★ 本文件是示例模板。造书时复制进项目（<项目根>/scripts/）→ 按需改顶部 HEADER 再跑。
    脚本自动扫描 chapters/ 和 appendix/ 目录，按文件名字典序合并。

用法：
    python merge_book.py [项目根目录] [--strip-frontmatter]

设计要点：
- 读 META.md 顶部 YAML format 字段判断路线
- human-readable 路线在 BOOK.md 顶部注入 loader 指令
- 可重跑
"""
import os
import re
import sys
from pathlib import Path

DEFAULT_BASE_DIR = "."


def read_meta_format(base_dir):
    """读 META.md 顶部 YAML 的 format 字段。"""
    meta_path = Path(base_dir) / "META.md"
    if not meta_path.exists():
        return "pure-blueprint"
    content = meta_path.read_text(encoding="utf-8")
    # 匹配顶部 --- ... --- 之间的 YAML
    m = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not m:
        return "pure-blueprint"
    yaml_text = m.group(1)
    fm = re.search(r"^format:\s*(.+)$", yaml_text, re.MULTILINE)
    return fm.group(1).strip() if fm else "pure-blueprint"


def load_chapters(base_dir):
    """递归扫描 chapters/ 下所有 *.md，按文件名字典序排序。"""
    chapters_dir = Path(base_dir) / "chapters"
    if not chapters_dir.exists():
        return []
    files = sorted(chapters_dir.rglob("*.md"))
    return files


def load_appendices(base_dir):
    """扫描 appendix/ 下所有 *.md，按文件名字典序排序。"""
    app_dir = Path(base_dir) / "appendix"
    if not app_dir.exists():
        return []
    files = sorted(app_dir.glob("*.md"))
    return files


def strip_frontmatter(content):
    """剥离 YAML frontmatter（--- ... ---）。"""
    return re.sub(r"^---\s*\n.*?\n---\n?", "", content, count=1, flags=re.DOTALL)


LOADER_TEMPLATE = """> **AI 老师使用说明**：本书是给人读的流畅教材。正文 prose 是素材库，用你自己的话重组教学；
> 每章末尾的思考题/练习区是提问路线图，请照那些问题的层次引导学生。

---

"""


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    base_dir = args[0] if args else DEFAULT_BASE_DIR
    do_strip = "--strip-frontmatter" in flags

    fmt = read_meta_format(base_dir)
    chapters = load_chapters(base_dir)
    appendices = load_appendices(base_dir)

    parts = []
    if fmt == "human-readable":
        parts.append(LOADER_TEMPLATE)

    for ch in chapters:
        content = ch.read_text(encoding="utf-8")
        if do_strip:
            content = strip_frontmatter(content)
        if not content.endswith("\n"):
            content += "\n"
        parts.append(content)
        parts.append("\n---\n\n")

    if appendices:
        parts.append("# 附录\n\n")
        for ap in appendices:
            content = ap.read_text(encoding="utf-8")
            if do_strip:
                content = strip_frontmatter(content)
            if not content.endswith("\n"):
                content += "\n"
            parts.append(content)
            parts.append("\n")

    output_path = Path(base_dir) / "BOOK.md"
    output_path.write_text("".join(parts), encoding="utf-8")

    size = output_path.stat().st_size
    lines = output_path.read_text(encoding="utf-8").count("\n")
    print(f"合并完成：{output_path}")
    print(f"路线：{fmt}")
    print(f"章数：{len(chapters)}，附录：{len(appendices)}")
    print(f"文件大小：{size:,} 字节 / {lines:,} 行")


if __name__ == "__main__":
    main()