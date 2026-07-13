# -*- coding: utf-8 -*-
"""
拆脚手架脚本模板（造书 Phase 8）：
删除每个单元源文件末尾的"📋 自检清单"和"📜 版本记录"两个板块。
这两类是造书者的 QA 笔记/修订日志，对 AI 老师教学零价值。

删除范围：从 "## 📋 自检清单" 行到文件末尾（含自检清单 + 版本记录）。
若文件无自检清单，则回退到 "## 📜 版本记录" 起始。

用法：
    python strip_meta_sections.py [单元目录]
    # 省略参数时默认用下面的 DEFAULT_UNIT_DIR

★ 删完后必须重跑 merge_book.py 重新合并 BOOK.md。
★ 本脚本只删末尾两个板块；正文内散落的版本标记 / "教师用书说" / 造书者口吻
  需另行全局清理（见 references/delivery-checklist.md 的 8 类元数据）。
"""
from pathlib import Path
import sys

DEFAULT_UNIT_DIR = r"f:\code\po-juan-xie-shu\english-book-XX\volume-1-units"

CHECKLIST_MARKER = "## 📋 自检清单"
VERSION_MARKER = "## 📜 版本记录"


def main():
    unit_dir = Path(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_UNIT_DIR)

    total_removed_chars = 0
    total_removed_lines = 0
    files_changed = 0

    for uf in sorted(unit_dir.glob("unit-*.md")):
        content = uf.read_text(encoding="utf-8")

        idx_check = content.find(CHECKLIST_MARKER)
        idx_ver = content.find(VERSION_MARKER)

        if idx_check != -1:
            cut_idx = idx_check
        elif idx_ver != -1:
            cut_idx = idx_ver
        else:
            print(f"[skip] {uf.name}: 未找到 自检清单/版本记录，跳过")
            continue

        removed = content[cut_idx:]
        removed_lines = removed.count("\n")
        new_content = content[:cut_idx].rstrip() + "\n"  # 保留单个末尾换行

        uf.write_text(new_content, encoding="utf-8")

        total_removed_chars += len(removed)
        total_removed_lines += removed_lines
        files_changed += 1
        print(f"[ok]   {uf.name}: 删除 {len(removed):,} 字符 / {removed_lines} 行")

    print("-" * 60)
    print(f"完成：{files_changed} 个文件，共删除 {total_removed_chars:,} 字符 / {total_removed_lines} 行")
    print("★ 记得重跑 merge_book.py 重新合并 BOOK.md")


if __name__ == "__main__":
    main()
