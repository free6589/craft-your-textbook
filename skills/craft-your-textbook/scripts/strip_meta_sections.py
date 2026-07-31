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

DEFAULT_DIRS = ["chapters", "appendix"]


def read_scaffold_titles(base_dir):
    """从 META.md 读脚手架标题列表。
    预期 META 有一行 "10. 脚手架标题列表" 后跟 markdown 列表。
    如没找到，返回默认值。
    """
    meta_path = Path(base_dir) / "META.md"
    defaults = ["## 📋 自检清单", "## 📜 版本记录", "## 写作笔记"]
    if not meta_path.exists():
        return defaults
    content = meta_path.read_text(encoding="utf-8")
    # 找"脚手架标题"section
    m = re.search(r"脚手架标题[^：]*：?[^\n]*\n((?:[-*]\s+[^\n]+\n)+)", content)
    if not m:
        return defaults
    titles = []
    for line in m.group(1).strip().split("\n"):
        line = line.strip().lstrip("-*").strip().strip("`")
        if line:
            titles.append(line)
    return titles if titles else defaults


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