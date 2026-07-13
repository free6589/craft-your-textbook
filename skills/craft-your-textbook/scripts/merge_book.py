# -*- coding: utf-8 -*-
"""
合并脚本模板：将所有单元源文件 + 附录文件合并为 BOOK.md。
产出含目录、Part 分隔、节间锚点，文件头带版本说明。

用法：
    python merge_book.py [项目根目录]
    # 省略参数时默认用下面的 DEFAULT_BASE_DIR

设计要点：可重跑——每次改完单元文件，重跑脚本即可重新生成 BOOK.md。

★ 新项目需调整的地方：
    1. DEFAULT_BASE_DIR：项目根目录
    2. header：书名、画像、目录（勿写版本号——版本是过程元数据，Phase 9 质量门会拦 v1.0/v1.1）
    3. UNIT_FILES：单元文件名 → 锚点 的映射
    4. APPENDIX_FILES：附录文件名 → 锚点 的映射
    5. STARTER_FILE：若无 Starter 预备单元则设为 None
"""
import os
import sys

DEFAULT_BASE_DIR = r"./english-book-XX"  # 占位：请传参 python merge_book.py <项目根> 或改此值

# ── 单元 / 附录 / Starter 配置（新项目按需改）────────────────────────
STARTER_FILE = "unit-00-starter.md"          # 无预备单元则设 None
UNIT_FILES = [
    ("unit-01-a-new-start.md", "unit-1"),
    ("unit-02-more-than-fun.md", "unit-2"),
    ("unit-03-family-ties.md", "unit-3"),
    ("unit-04-time-to-celebrate.md", "unit-4"),
    ("unit-05-power-of-plants.md", "unit-5"),
    ("unit-06-fantastic-friends.md", "unit-6"),
]
APPENDIX_FILES = [
    ("appendix-A-vocabulary.md", "appendix-a"),
    ("appendix-B-grammar.md", "appendix-b"),
]

HEADER = """# [书名] · 苏格拉底教学蓝本

> **本书定位**：这是给 AI 苏格拉底老师的**教学蓝本**（pedagogical spec），不是给学生读的书。
> 学生只跟 AI 老师对话，不读本蓝本；AI 老师读蓝本，用引导式提问教学生。
> AI 老师的人设由用户单独定义，本蓝本不含教学风格部分。

**学习者画像**：[画像]。
**组织方式**：[按单元顺序 / 按主题]。

---

## 📑 目录

[按需补充目录，锚点与下方 anchor 对应]

---
"""


def read_unit(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if not content.endswith("\n"):
        content += "\n"
    return content


def main():
    base_dir = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_BASE_DIR
    units_dir = os.path.join(base_dir, "volume-1-units")
    appendix_dir = os.path.join(base_dir, "appendix")

    parts = [HEADER]

    # Part 1 · 预备单元
    if STARTER_FILE:
        parts.append("\n# Part 1 · 预备单元\n\n")
        parts.append('<a id="starter"></a>\n\n')
        parts.append(read_unit(os.path.join(units_dir, STARTER_FILE)))

    # Part 2 · 正式单元
    parts.append("\n# Part 2 · 正式单元\n\n")
    for filename, anchor in UNIT_FILES:
        parts.append(f'<a id="{anchor}"></a>\n\n')
        parts.append(read_unit(os.path.join(units_dir, filename)))
        parts.append("\n")

    # Part 3 · 附录
    parts.append("# Part 3 · 附录\n\n")
    for filename, anchor in APPENDIX_FILES:
        parts.append(f'<a id="{anchor}"></a>\n\n')
        parts.append(read_unit(os.path.join(appendix_dir, filename)))
        parts.append("\n")

    output_path = os.path.join(base_dir, "BOOK.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("".join(parts))

    # ── 统计 + 验证 ──────────────────────────────────────────────
    size = os.path.getsize(output_path)
    with open(output_path, "r", encoding="utf-8") as f:
        book = f.read()
    lines = book.count("\n")
    print(f"合并完成：{output_path}")
    print(f"文件大小：{size:,} 字节 / {lines:,} 行")

    anchors = (["starter"] if STARTER_FILE else []) \
        + [a for _, a in UNIT_FILES] + [a for _, a in APPENDIX_FILES]
    for a in anchors:
        mark = "✓" if f'<a id="{a}"></a>' in book else "✗ 缺失"
        print(f"  {mark} 锚点 {a}")
    for p in ["Part 1", "Part 2", "Part 3"]:
        mark = "✓" if p in book else "✗ 缺失"
        print(f"  {mark} {p}")


if __name__ == "__main__":
    main()
