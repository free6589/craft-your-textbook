---
name: craft-your-textbook
description: 让你具备"亲手为自己造一本教材"的能力——把源材料（教材/考纲/讲义等）加工成 AI 苏格拉底老师能拿去上课的教学蓝本（pure-blueprint），或一本给人读的流畅教材（human-readable，AI 也能直接教）。适用任何学科。两条路线互斥选择，默认推荐给 AI 老师的版本。覆盖 PDF→MD、源探查、教学设计五步、金标准先行、模式选型、并行铺章、审计合并拆脚手架全流程。当用户说"造一本教学蓝本/做一本 XX 教材/按这套方法写一本书"时使用。
---

# 亲手造属于你自己的教材（Craft Your Textbook）

## 这是什么

造书 = 为学习者制备一份**教材**。有两种形态（触发后必选，见下"第一步：定路线"）：
- **pure-blueprint**：给 AI 苏格拉底老师读的教学蓝本（pedagogical spec），结构化、含元指令
- **human-readable**：给人读的流畅教材，AI 拿到也能直接教

三方分工决定所有下游规则：

| 角色 | 做什么 | 看到什么 |
|---|---|---|
| **用户（学习者）** | 跟 AI 老师对话学习 | 只看到对话（blueprint）或读教材+对话（human-readable） |
| **AI 老师** | 读书，用引导式提问教学 | 读完整本书作为输入 |
| **书（造物）** | 教学素材 | 是 AI 老师的输入，或人读的教材 |

**最常见的根本错误**：把书写成"给读者感受的文学作品"——开篇钩子写给谁看？"你"指谁？写每一块前先问："AI 老师/人读到这块会怎么用它？"

书对 AI 老师的四个功能：①**内容锚定**（防跑题/幻觉）②**知识结构**（推理主线）③**弹药库**（案例随取随用）④**提问路线图**（引导学生抵达知识点的问题方向）。

## 何时用

- 用户要把教材/领域知识做成 AI 能教的书或人读的教材
- 用户说"造一本书""做一本教材""按这套方法写 XX"
- 需要从 PDF 教材加工出结构化教学素材

**第一步：定路线**（触发后必须问，不替用户默认）：

> "这本书是喂给 AI 苏格拉底老师教学用的教学蓝本（推荐——AI 教学精度最高），还是一本给人读的流畅教材（AI 也能直接拿它教，但教学约束更少）？"

决策启发式：
1. 用户原话含"我自己读/出版/给别人看/通读/给真人教师" → human-readable
2. 书要喂给已成型的苏格拉底 AI 软件（Socratopia 等） → pure-blueprint
3. 用户不确定 → 推荐 pure-blueprint 并等拍板

路线差异和细节见 `references/two-routes.md`。

## 全流程导航（6 阶段）

先出设计，再写正文；先写一章金标准审到满意，再并行铺开。平均每本书 5-7 轮审校。

| 阶段 | 名称 | 做什么 | 产出 |
|---|---|---|---|
| **Phase 1** | 源材料准备 | PDF→MD（MinerU API）+ 复制脚本进项目 + 装依赖 | `sources-md/`、`scripts/` |
| **Phase 2** | 源探查 | 所有有源书必走：摸源结构、角色标签、简码表、权威层级 | `源材料索引.md` 第一层 |
| **Phase 3** | 教学设计 | **核心阶段**：五步设计（见下）+ 三个用户确认关卡 | META/OUTLINE/style-spec/源材料索引 |
| **Phase 4** | 金标准验证 | 选一章按设计的语法写 → 五层审计 + L5 教学测试 → 通过后回填 style-spec | 金标准章 md |
| **Phase 5** | 全量写作+收网 | sub-agent 并行铺章 → 附录汇编 → 跨章审计 → 合并 BOOK.md | chapters/、appendix/、BOOK.md |
| **Phase 6** | 终检与交付 | 终检 → 拆脚手架 → 质量门 → 交付 | 纯净 BOOK.md |

Mode A（无源从零造）差异：Phase 2 跳过、幻觉 gate 更严，仅适合 AI 知识密度高领域。

## 核心：Phase 3 教学设计五步

这是 v7 的核心——Agent 不套模板，自己设计书的形状。

1. **Phase 3.1 分析源+推导目标**（不读模式库，免先入为主）：
   - 源材料形态是什么？
   - 这本书让学习者最终能做到什么？（通过考试/理解概念/掌握技能/通读建体系）
   - 学习者最大的坑是什么？
   - **用户确认关卡 ①**：目标和坑是否准确

2. **Phase 3.2 路线决策**（见"第一步：定路线"）

3. **Phase 3.3 模式选型+板块语法设计**：
   - 读 `references/patterns/README.md`，理解模式库
   - 带 Phase 3.1 的教学问题翻卡（每张卡判断"这个问题本书有没有"）
   - 回答两个强制问题写进 style-spec：
     ① 考虑过哪些模式、拒绝了哪些、为什么拒绝？
     ② 所选每个模式对应本书哪个具体教学问题？
   - 可选：从预装配包（认证/叙事/K-12）出发再定制
   - 设计章内板块语法（必含/循环/可选板块、叙事约定、章末教学区）
   - **用户确认关卡 ②**：模式选型和板块语法是否合理

4. **Phase 3.4 整书教学架构设计**：
   - 知识链主线、卷/部划分、逐章骨架
   - 特殊功能章（地基章/收网章）
   - 跨章引用机制、附录汇编策略
   - 贯穿案例/主角约定
   - 回填源材料索引第二层（章级映射）
   - **用户确认关卡 ③**：全书架构和逐章骨架

5. **Phase 3.5 META+源索引完稿**：
   - META 完成（必答 10 个问题见 `references/file-contracts.md`）
   - 源材料索引完成

不变量底线见 `references/invariants.md`——任何设计都不能违反。

## 关键工程原则

- **金标准先行**：没有金标准就并行 = agent 必然漂移
- **一个 agent 只写一章**，避免长上下文漂移
- **断言可追溯**：每写一条定义/公式/偏好判断，都能回源或回判断根
- **防螺旋**：Phase 3 定稿后不允许加章/附录/机制板块，新需求先问"能不能塞进现有结构"
- **交付前必拆脚手架**

## 参考文件按需加载

| 场景 | 参考文件 |
|---|---|
| Phase 1 PDF 转换 | scripts/ 说明 |
| Phase 2 源探查 | `references/source-material.md` |
| Phase 3 四文件契约 | `references/file-contracts.md` |
| Phase 3 模式选型 | `references/patterns/README.md` |
| Phase 3 不变量底线 | `references/invariants.md` |
| Phase 3 板块语法起点 | `references/chapter-grammar-starter.md` |
| Phase 3 路线差异 | `references/two-routes.md` |
| Phase 4-5 审计 | `references/audit-and-testing.md` |
| Phase 6 交付 | `references/delivery-checklist.md` |
| 避坑 | `references/anti-patterns.md` |

## ⚠️ Phase 1 前置：MinerU API Token

PDF→Markdown 默认走 MinerU 在线 API（`mineru.net`）。开跑前让用户完成：

0. 定位 skill 脚本目录 + 装依赖：
   ```bash
   SKILL_DIR=$(dirname "$(find ~/.claude -name SKILL.md -path '*craft-your-textbook*' | head -1)")
   pip install -r "$SKILL_DIR/scripts/requirements.txt"
   ```
   复制脚本：`cp "$SKILL_DIR/scripts/"*.py <项目根>/scripts/`
1. 打开 https://mineru.net 注册申请 API Token
2. 设环境变量：`export MINERU_TOKEN="你的token"`
3. 运行 `python <项目根>/scripts/01_pdf_to_md.py <PDF路径> sources-md/`

理科改 `ENABLE_FORMULA = True`。已有 MD 跳过 Phase 1。

## 一句话核心

> 书是给 AI 老师或人读的教学素材，学生主要跟 AI 老师对话。触发后先定路线；不套模板，Phase 3 自己设计书的形状——不变量是底线、模式库是菜单、四文件契约强制回答设计问题。**先出设计再写正文，先写金标准再并行，交付前必拆脚手架。**
