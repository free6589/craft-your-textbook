# craft-your-textbook v7 重构实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 craft-your-textbook skill 从 v6 的"预定义模板填槽"范式重构为 v7 的"元方法 + 参考模式库 + 四文件契约"范式。

**Architecture:** 重写 SKILL.md 为精简的元方法引导器；将 7 板块硬模板拆为 20 张按"教学问题"组织的模式卡；新建 invariants.md/file-contracts.md 等承载不变量和契约；删除旧的 unit-template.md/outline-and-analysis.md/vocabulary-strategy.md；通用化三个脚本去除英语教材硬编码。

**Tech Stack:** Markdown skill 文件 + Python 3 脚本（仅用标准库 + requests）。无测试框架——脚本改动以端到端手测验证，reference 文件以内容完整性和跨文件一致性验证。

## Global Constraints

- skill 根目录：`F:/code/craft-your-textbook/skills/craft-your-textbook/`
- 所有 reference 路径相对于 skill 根目录的 `references/`
- 模式卡路径相对于 `references/patterns/`
- 脚本路径相对于 skill 根目录的 `scripts/`
- 真实样本路径（写模式卡时引用）：
  - PMP：`f:/code/po-juan-xie-shu/PMP/textbook/`（human-readable，认证类）
  - CPA：`f:/code/po-juan-xie-shu/socratopia-cpa-audit-zh/`（human-readable，叙事类）
- 模式卡统一格式（六节）：解决什么教学问题 / 什么时候用 / 长什么样 / 已知陷阱 / 变体 / 不要这样用
- 脚本仍是"复制进项目再改"的示例模板，不做即插即用工具
- 提交粒度：每个 Task 结束后独立 commit
- 中文写作（skill 面向中文用户），代码注释和文件名用英文
- v6 REFACTOR-PLAN-v6.md 保留不动（历史参考）

---

## 文件结构总览

### 新建文件（26 个）

| 文件 | 职责 |
|---|---|
| `references/invariants.md` | 不变量清单（I1-I9, H1-H3） |
| `references/file-contracts.md` | 四文件契约必答问题清单 |
| `references/two-routes.md` | 两条路线决策指引+差异 |
| `references/source-material.md` | 源角色标签+两层索引+深度三档+师生合版比对 |
| `references/chapter-grammar-starter.md` | 从模式卡组合章节语法的走查示例 |
| `references/patterns/README.md` | 模式库索引+选型流程+预装配包+三书示例 |
| `references/patterns/concept-anchoring/precise-definition.md` | 精确呈现（术语/公式/分类） |
| `references/patterns/concept-anchoring/misconception.md` | 误区桩 |
| `references/patterns/concept-anchoring/socratic-questioning.md` | 苏格拉底提问路线图 |
| `references/patterns/concept-anchoring/fact-vs-judgment.md` | 确定性知识 vs 判断分离 |
| `references/patterns/assessment/judgment-card.md` | 判断题/首选卡 |
| `references/patterns/assessment/quick-judgment.md` | 速判/限时选择题 |
| `references/patterns/assessment/application-problem.md` | 长情境多步推理题 |
| `references/patterns/assessment/worked-example.md` | 例题演练 |
| `references/patterns/assessment/practice-gradient.md` | 练习三级梯度 |
| `references/patterns/assessment/deterministic-anchor.md` | 必背锚/确定知识清单 |
| `references/patterns/narrative/scenario-hook.md` | 情境钩子开章 |
| `references/patterns/narrative/running-case.md` | 贯穿案例语料库 |
| `references/patterns/narrative/character-protagonist.md` | 主角/第二人称戏剧化 |
| `references/patterns/structure/foundation-chapter.md` | 地基章 |
| `references/patterns/structure/capstone-chapter.md` | 总结/收网章 |
| `references/patterns/structure/cross-ref-trace.md` | 行内回溯引用 |
| `references/patterns/structure/appendix-compilation.md` | 附录汇编 |
| `references/patterns/structure/multi-source-arbitration.md` | 多源冲突裁决 |
| `references/patterns/structure/recurring-leitmotif.md` | 贯穿主题低音线 |
| `references/patterns/language-learning/vocabulary-dimension.md` | L1-L4 词汇分层 |

### 重写文件（4 个）

| 文件 | 改动 |
|---|---|
| `SKILL.md` | 从 150 行 v6 文档重写为 ~200 行元方法引导器 |
| `references/audit-and-testing.md` | 更新幻觉 gate 对齐 I2、加金标准门槛清单、加 sub-agent prompt 要素 |
| `references/delivery-checklist.md` | 质量门通用化（删除 7 板块硬编码，改为从四文件契约派生） |
| `references/anti-patterns.md` | 加诚实边界声明反模式，更新措辞对齐 v7 |

### 删除文件（3 个）

| 文件 | 原因 |
|---|---|
| `references/unit-template.md` | 7 板块硬模板拆为模式卡 |
| `references/outline-and-analysis.md` | 继任者为 file-contracts.md + source-material.md |
| `references/vocabulary-strategy.md` | 并入 patterns/language-learning/vocabulary-dimension.md |

### 修改文件（3 个脚本）

| 文件 | 改动 |
|---|---|
| `scripts/merge_book.py` | 删除硬编码英语书清单，通用化目录/排序/HEADER，加 META YAML 解析和 loader 注入 |
| `scripts/strip_meta_sections.py` | 脚手架标题从 META 读，递归搜索 chapters/+appendix/ |
| `scripts/01_pdf_to_md.py` | 仅更新注释中的路径示例（`source-md/` → `sources-md/`，删除师生合版输出到 source-md-teacher） |

---

## Task 1: 建目录骨架 + 删除旧 reference

**Files:**
- Create: `references/patterns/concept-anchoring/`, `references/patterns/assessment/`, `references/patterns/narrative/`, `references/patterns/structure/`, `references/patterns/language-learning/`
- Delete: `references/unit-template.md`, `references/outline-and-analysis.md`, `references/vocabulary-strategy.md`

**Interfaces:** 无——纯文件系统准备。

- [ ] **Step 1: 创建模式库目录结构**

```bash
cd F:/code/craft-your-textbook/skills/craft-your-textbook/references
mkdir -p patterns/concept-anchoring patterns/assessment patterns/narrative patterns/structure patterns/language-learning
```

- [ ] **Step 2: 删除三个旧 reference 文件**

```bash
cd F:/code/craft-your-textbook/skills/craft-your-textbook/references
rm unit-template.md outline-and-analysis.md vocabulary-strategy.md
```

- [ ] **Step 3: 验证目录和删除**

Run: `ls patterns/ && ls references/ | grep -E "unit-template|outline-and-analysis|vocabulary-strategy" || echo "deleted ok"`
Expected: 五个子目录列出；后一条命令输出 "deleted ok"。

- [ ] **Step 4: Commit**

```bash
cd F:/code/craft-your-textbook
git add skills/craft-your-textbook/references/
git commit -m "refactor: 建 patterns/ 目录骨架，删除 v6 三个硬模板 reference"
```

---

## Task 2: 写 invariants.md（不变量清单）

**Files:**
- Create: `references/invariants.md`

**Interfaces:** 无——其他 reference 和 SKILL.md 通过文本引用"I1-I9/H1-H3"。

- [ ] **Step 1: 创建 invariants.md**

写入以下内容（spec §二的完整展开，含每条不变量的"为什么""违反的后果""检查方法"）：

```markdown
# 不变量清单

> 本文列出的是从"AI 老师读书教学"和"人读教材"两个核心洞察推出来的底线。
> 模式卡（patterns/）提供可组合的解决方案；不变量是不管用不用模式卡都必须满足的底线。
> 编号：跨路线内容不变量 I1-I4、pure-blueprint 专属 I5-I6、human-readable 专属 H1-H3、过程不变量 I7-I9。

---

## 一、跨路线硬约束（I1-I4，两条路线都必须满足）

### I1. 读者意识
写每个板块前必须能回答"AI 老师上课时会怎么用这块？"（两条路线都要）。human-readable 额外回答"人读到这里会怎么理解？"——防止 prose 只考虑 AI 可读、人读着像规格书。

**违反后果**：板块沦为填充物，AI 老师无法将其转化为教学动作；或人读时遇到"指令味"段落。
**检查方法**：Phase 5.3 跨章审计时，逐板块追问"AI 老师拿到这个会做什么"。

### I2. 断言可追溯
任何权威断言——包括正式定义/公式/数字/分类名称，和偏好/首选/"应当"类判断——都必须能追溯到依据。
- 定义/公式/数字类：回源文件+行号
- 偏好/首选/判断类：回已声明的判断根（原则/模型/准则条款）
标不出依据的偏好断言，宁可不写。
Mode A（无源）下替代机制：每个断言必须能通过 L5 教学测试的学员验证，强制 L5 路径 B/C，不接受路径 A 自测。

**违反后果**：幻觉、杜撰准则/定义/偏好，喂给 AI 老师后系统性教错。
**检查方法**：L3 引文抽检；偏好类断言逐标判断依据。

### I3. 具体情境素材
必须为教学提供含具体实体（公司/角色/数字/约束）的情境或案例。不接受"某项目遇到 X"式空泛描述。

**违反后果**：AI 老师开课时没有切入素材，或只能造空泛例子。
**检查方法**：逐章检查章首情境是否包含至少一个具体数字/具体公司/具体角色名。

### I4. 跨章引用
整本书必须有前后章知识回扣机制（行内回溯/连接表/主题低音线——具体形式由 Agent 设计，不预设）。

**违反后果**：知识碎片化，AI 老师无法跨节串讲，学生只见树木不见森林。
**检查方法**：Phase 5.3 审计时逐章确认"本章至少有一处明确回扣到前/后章"。

---

## 二、pure-blueprint 路线硬约束（I5-I6）

### I5. 非对话体
不写死"老师说…学生答…"的对话脚本——写死了 AI 会照抄，教学就死。

**违反后果**：蓝本变剧本，AI 老师照本宣科，无法根据学生状态调整。

### I6. 显式提问路线图
必须为 AI 老师提供结构化提问方向/问题链（💬三类问题/双脚本/探索脚本等形式不限），不能只有知识点没有教学指引。

**违反后果**：AI 老师读完蓝本不知怎么开课、怎么追问。

---

## 三、human-readable 路线硬约束（H1-H3）

### H1. 正文叙事 prose 化
正文是流畅叙事，不内嵌"给 AI 老师"的元指令、技术回溯标注、yaml frontmatter。

**违反后果**：人读时遇到突兀的元指令块（如"【AI 老师提问脚本】"出现在正文中间）。
**注意**：章末教学区（H2）是例外，可以包含结构化教学素材。

### H2. 章末结构化教学区
每章章末必须有结构化教学素材区（练习/讨论题/探索问题/教学脚本——形态由 Agent 按教学目标设计）。这是 human-readable 路线下 AI 老师的提问路线图（等价于 blueprint 的 I6）。

**违反后果**：AI 老师拿到 prose 没有提问路线图，只能照念 prose。

### H3. BOOK.md 顶部 loader 指令
合并时在 BOOK.md 顶部注入 loader 指令，告诉 AI 老师："正文 prose 是素材库，用你自己的话重组教学；章末教学区照问题链走。"

**违反后果**：AI 老师把 prose 当逐字稿念。

---

## 四、过程不变量（I7-I9，两条路线同等适用）

### I7. 金标准先行
全量铺写前必须先写一章金标准，按 `audit-and-testing.md §金标准门槛` 通过后，回填 `style-spec §金标准写作惯例`，再铺开。

**违反后果**：并行写作的多个 agent 必然漂移，后期统一成本极高。

### I8. 交付前拆脚手架
过程元数据（自检清单/版本记录/写作惯例注释等）交付前必须拆干净。脚手架标题列表由 META 声明（每本书可能不同），不硬编码。

**违反后果**：AI 老师读到"v2.0 新增""自检清单"等过程元数据，教学时产生困惑。

### I9. 防螺旋铁律
方案定稿后不允许新增章/附录/机制级板块。新需求先问"能不能塞进现有结构"，不能才考虑，且需砍掉等量的东西并回炉 Phase 3。

**违反后果**：scope creep，书无限膨胀（PMP v5 曾因此涨到 40 万字）。
```

- [ ] **Step 2: 验证文件存在且内容非空**

Run: `wc -l F:/code/craft-your-textbook/skills/craft-your-textbook/references/invariants.md`
Expected: 80+ 行。

- [ ] **Step 3: Commit**

```bash
cd F:/code/craft-your-textbook
git add skills/craft-your-textbook/references/invariants.md
git commit -m "feat: 写 invariants.md——不变量清单 I1-I9/H1-H3"
```

---

## Task 3: 写 file-contracts.md（四文件契约必答问题）

**Files:**
- Create: `references/file-contracts.md`

- [ ] **Step 1: 创建 file-contracts.md**

内容为 spec §六的完整展开，每个文件的每个必答问题后附"回答要点提示"（不是答案，是提醒 Agent 要想清楚什么）：

```markdown
# 四文件契约必答问题清单

> Agent 在 Phase 3 产出四文件时，每个文件必须回答完下面所有问题。
> 契约强制"必须回答什么"，不预设"答案是什么"——答案由 Agent 按本书分析得出。
> 完整 Phase 3 五步流程见 SKILL.md。

---

## META.md（写作规范）

META.md 顶部含极简 YAML frontmatter（仅一个字段）：
```yaml
---
format: pure-blueprint | human-readable
---
```

正文必答问题：

1. **本书定位**：一句话说清这本书是什么、给谁用。路线已在顶部 YAML 声明，此处不重复。
2. **防幻觉铁律**：本书最危险的断言类型是什么（定义/公式/偏好判断/历史事实/代码）？回源到哪？追不到源怎么降级？
3. **读者意识声明**：本书第一读者是谁（AI 老师/人类读者）？写每块前问什么问题？
4. **章内板块语法**：从 Phase 3.3 搬过来——必含板块/循环单元/可选板块/叙事约定/章末教学区形态。
5. **章末教学区规范**：章末教学区的板块结构、长度、格式要求。
6. **写作纪律**：一个 agent 写几章？并行度？字数参考？明确排除项（不写什么）？
7. **frontmatter schema**：需要章级 yaml 则定义字段+校验规则；不需要则显式声明"本书无章级 frontmatter"。
8. **AI 老师使用方式**：顺序讲/地基章先吃透/按需检索？
9. **防螺旋铁律（I9）**：定稿后加章/附录/机制级板块的回炉规则。
10. **脚手架标题列表**：Phase 6 拆脚手架用——本书写作过程中会用哪些元数据板块标题（如"## 自检清单""## 写作笔记"）。

---

## OUTLINE.md（大纲与架构）

1. **知识链主线**：一句话说清全书推理主线。
2. **卷/部划分**：怎么分组、为什么这样分。
3. **逐章骨架表**：章号/标题/类型（eco_task/foundation/agile_practice/exam_strategy 等 Agent 自定的类型名）/在知识链中的位置/锚定的源任务或概念。
4. **特殊功能章**（如有）：地基章/总结章/策略章——为什么不能并入正常章。
5. **跨章引用机制**：本书用什么形式做知识回扣（行内回溯/连接表/主题低音线）——说清具体形式。
6. **附录汇编策略**：从哪些章末板块自动汇编成哪些附录。
7. **贯穿案例/主角约定**（如选了 narrative 卡）：案例/主角是什么，边界在哪（如"不写人物情感弧线"）。
8. **BOOK.md loader 指令内容**（human-readable 路线）：告诉 AI 老师怎么用这本书的一段话。

---

## style-spec.md（风格与语法）

1. **模式选型说明**：两个强制问题回答——考虑过哪些模式、拒绝了哪些、为什么拒绝？所选每个模式对应本书哪个教学问题？
2. **章内板块语法完整版**：必含/循环/可选板块，每个板块的写作要求、长度、人称、位置。
3. **情境钩子写法**：长度/人称/必含元素/挂靠贯穿案例的规则。
4. **正文语言风格**：正式程度/术语处理（原文/翻译/双语）/本书特有禁用词（不是全局硬编码）。
5. **量化参考密度**：每章小节数/Definition 数/misconception 数/习题数——参考非铁律，金标准后回填实测。
6. **金标准写作惯例区**：Phase 4 通过后回填——实测密度/踩过的坑/确认不套用的视角。

---

## 源材料索引.md（有源场景）

1. **源文件简码表**：简码/路径/定位/权威层级。
2. **全书通用锚点**：跨章共享的源定位（如公式汇总表/原则全文位置）。
3. **分章源映射**：每章四要素——
   - ① 章→源文件行号映射
   - ② 预抽关键条目
   - ③ 高频陷阱/偏好预判
   - ④ 写作惯例（金标准后回填）
4. **可信度声明**：建索引时实际探查了什么、发现了什么问题（如"XX 笔记是 OCR 碎片，非完整骨架"）。

Mode A（无源）不建此文件，META 里声明知识密度自评结果 + L5 强制路径。
```

- [ ] **Step 2: 验证**

Run: `wc -l F:/code/craft-your-textbook/skills/craft-your-textbook/references/file-contracts.md`
Expected: 80+ 行。

- [ ] **Step 3: Commit**

```bash
cd F:/code/craft-your-textbook
git add skills/craft-your-textbook/references/file-contracts.md
git commit -m "feat: 写 file-contracts.md——四文件必答问题清单"
```

---

## Task 4: 写 source-material.md（源处理方法论）

**Files:**
- Create: `references/source-material.md`

- [ ] **Step 1: 创建 source-material.md**

内容包含：源角色标签 7 类表 + 两层索引方法学（Phase 2 源级探查 → Phase 3.4 章级映射回填）+ 深度三档（轻量/中量/完整版，按源数量自度）+ 师生合版独有内容比对方法学 + Mode A 知识密度自评。

```markdown
# 源材料处理方法论

> Phase 2（源探查）和 Phase 3.4（章级映射回填）的方法学。
> 对应 v6 outline-and-analysis.md 里源处理的部分 + v6 源角色标签体系。

---

## 一、源角色标签（7 类）

用户给的所有素材文件都在 META.sources 里登记（自然语言描述即可，不需要 yaml），每个文件打一个角色标签。角色标签决定该文件在写作中的地位。

| 角色标签 | 什么文件 | 在写作中的地位 |
|---|---|---|
| `student_textbook` | 学生用书 PDF/MD | 教学主线骨架 |
| `teacher_textbook` | 教师用书 PDF/MD | 差异比对 + 教学方法补充 |
| `syllabus` | 考纲/ECO/课程标准 | 覆盖校验基准（启用 syllabus 覆盖校验时必备） |
| `authoritative_source` | 权威原文（PMBOK/法典/官方指南/Scrum 指南） | 防幻觉真相源，冲突裁决最高级 |
| `teaching_notes` | 教学笔记/讲义/精炼笔记 | 教学骨架与例子，条目化起点 |
| `reference` | 辅助参考（博客/旧版/碎片化资料） | 仅在恰好覆盖时辅助，不作骨架 |
| `ocr_fragment` | OCR 碎片（宝典/扫描残片） | 最低等级，不作骨架 |

任意组合都合法：
- 师生合版 = `[student_textbook, teacher_textbook]`
- 单教材 = `[student_textbook]`
- PMP 多源 = `[syllabus, authoritative_source×3, teaching_notes×5, ocr_fragment×1]`

---

## 二、两层索引方法学

### 第一层：源级探查（Phase 2 必走）

所有有源书都走 Phase 2，深度按源数量自度。产出：
1. **源文件简码表**（简码/路径/定位/权威层级）
2. **真相校准**：实际翻源文件，识别"看起来完整其实是碎片"的坑（如 PMP 发现宝典笔记是 OCR 碎片）
3. **全书通用锚点**：跨章共享的源定位（公式汇总表/原则全文位置/术语表位置）

三档深度：
- **轻量**（单教材）：只建简码表+通用锚点，不做章级预映射
- **中量**（师生合版或 2-3 份异构源）：简码表+通用锚点+教师用书独有内容粗比对
- **完整版**（≥4 份异构源或有 syllabus 的认证类）：简码表+通用锚点+每源结构探查+真相校准+高频陷阱预判

### 第二层：章级映射回填（Phase 3.4 做）

Phase 3.4 定章后，为每章回填：
1. 章→源文件行号映射（精确到段落）
2. 预抽关键条目（硬记锚/公式/术语）
3. 高频陷阱/偏好预判
4. 写作惯例（金标准后回填）

### 不要在 Phase 2 硬建章级映射
此时还没有章，硬建只会对空构造。章是 Phase 3 设计的产物，映射跟着章走。

---

## 三、师生合版独有内容比对

有 `teacher_textbook` 角色标签时，在 Phase 2 做教师用书独有内容比对：
1. 逐单元对比学生用书和教师用书
2. 教师用书独有内容分类：评价标准/教学目标/学情分析/常见错误/考点提示/深层知识讲解
3. 比对结果写入源材料索引第一层的"教师用书独有内容"小节，供 Phase 3 设计板块语法时取用（如 teacher_textbook 的"常见错误"直接对应 misconception 模式卡）

不产出独立 DIFF-STUDENT-TEACHER.md 文件——结果入源材料索引。

---

## 四、Mode A（无源从零造）知识密度自评

用户明确"什么源都没有"时走 Mode A：
1. AI 就本书覆盖的 20 个核心锚点各写一段解释
2. 有明显犹豫/错误/幻觉的锚点超过 3 个 → 建议用户找源或换领域
3. 通过自评后：
   - human-readable 路线需知识密度自评 ≥18/20 + 用户明示接受幻觉风险
   - pure-blueprint 路线需 ≥15/20
   - I2（断言可追溯）替代机制：每个断言必须通过 L5 路径 B/C 的学员验证
```

- [ ] **Step 2: 验证并提交**

```bash
cd F:/code/craft-your-textbook
git add skills/craft-your-textbook/references/source-material.md
git commit -m "feat: 写 source-material.md——源角色标签+两层索引+师生合版比对"
```

---

## Task 5: 写 two-routes.md（两条路线指引）

**Files:**
- Create: `references/two-routes.md`

- [ ] **Step 1: 创建 two-routes.md**

```markdown
# 两条路线决策指引

> Phase 3.2 路线决策的依据和两路线差异详解。
> SKILL.md 只给一句话推荐，完整决策启发式和差异都在这里。

---

## 一、决策启发式

按优先级命中即走：

1. 用户原话含"我自己读/出版/给别人看/当书出/通读/给真人教师/我想先通读" → **human-readable**，告知理由
2. 书要喂给已成型的苏格拉底 AI 软件（Socratopia 平台等） → **pure-blueprint**
3. 用户不确定 → Agent 推荐 pure-blueprint（AI 教学精度最高），等用户拍板

不要替用户默认——必须在对话里呈现选择并等用户确认。

---

## 二、两路线核心差异

| 维度 | pure-blueprint | human-readable |
|---|---|---|
| 第一读者 | AI 老师 | 人类读者（AI 第二读者） |
| 不变量约束 | I1-I6 | I1-I4 + H1-H3 |
| 正文形态 | 结构化、可含元指令块、技术回溯、yaml frontmatter、emoji 标题 | 流畅 prose，不内嵌元指令 |
| 教学路线图位置 | 散布于各板块（💬引导方向/双脚本等） | 集中在章末教学区 |
| 章级 frontmatter | 可选且常用（grep 校验用） | 默认无，META 显式声明 |
| 典型样本 | 英语七上教材 | PMP 认证蓝本、CPA 审计教材 |

---

## 三、板块语法设计差异要点

### pure-blueprint
- 元指令块可以出现在章内任何位置（如 PMP 的"【AI 老师提问脚本】"在章末，但英语教材的 💬引导方向在 📌知识锚定之下）
- 可以用 emoji 标题（🎬🧭📌…）做结构化标记，AI 解析高效
- yaml frontmatter 承载章级元数据（任务锚定/章节类型等），方便 grep 校验
- 技术回溯行内标注（"回溯 Ch2 原则6"）直接写在正文

### human-readable
- 正文读起来像一本正常的书——段落过渡、叙事桥梁、人物/案例展开
- 章末教学区是独立板块（markdown 二级标题分隔），包含练习/讨论题/思考题
- 技术回溯改为可读的交叉引用（"正如第 2 章讨论过的……"而非行内标签）
- Loader 指令示例（写入 BOOK.md 顶部）：

```
> 本书是给 AI 苏格拉底老师的教材。正文是给人读的流畅叙事，你可以用自己的话重组来教学；
> 每章末尾的"思考题/练习"区是提问路线图，请照那些问题的层次引导学生。
```

---

## 四、终检项目差异

Phase 6 终检：
- **pure-blueprint**：检查必含板块计数、提问路线图齐备、yaml frontmatter 合法、无脚手架残留
- **human-readable**：检查章末教学区齐备、正文 prose 无内嵌元指令残留、loader 指令注入、无脚手架残留

---

## 五、诚实推荐

当用户不确定时推荐 pure-blueprint 的理由：
1. 这是 skill 的核心定位——为 AI 老师造教学蓝本
2. 结构化元指令让 AI 教学质量更可控
3. human-readable 的教学约束更少，更依赖 AI 老师自身发挥，质量方差更大

但不强制——如果用户明确要人读的体验，human-readable 是完全合法的产物。
```

- [ ] **Step 2: 提交**

```bash
cd F:/code/craft-your-textbook
git add skills/craft-your-textbook/references/two-routes.md
git commit -m "feat: 写 two-routes.md——路线决策启发式+差异详解"
```

---

## Task 6: 写 patterns/README.md（模式库索引）

**Files:**
- Create: `references/patterns/README.md`

这是模式库的入口文件，Agent Phase 3.3 全读此文件，Phase 4/5 按需重读具体卡。

- [ ] **Step 1: 创建 README.md**

```markdown
# 参考模式库

> 20 张模式卡，按"教学问题"组织（不按学科）。每张卡解决一个具体的教学设计问题。
> 这些不是"你必须套用"的模板，是"你可以选/混搭/新造"的解决方案菜单。

---

## 什么时候读我

- **Phase 3.3 模式选型时**：全读本 README + 按教学问题翻对应卡
- **Phase 4/5 写章时**：按 style-spec 里选定的卡，重读具体卡的写法示例

## 卡的分层

- **整书架构层**（`structure/`）：设计 OUTLINE 时先翻这组——地基章、收网章、跨章引用、附录汇编、多源裁决、主题低音线
- **章内板块层**（其他目录）：设计章内板块语法时翻
  - `concept-anchoring/`：概念锚定类（精确呈现、误区桩、苏格拉底提问、事实vs判断分离）
  - `assessment/`：评估/练习类（判断题、速判题、推理题、例题、练习梯度、必背锚）
  - `narrative/`：叙事结构类（情境钩子、贯穿案例、主角）
  - `language-learning/`：语言学习特化（词汇分层）

## 注意力引导（按教学目标提示优先看哪些卡）

根据 Phase 3.1 识别的教学目标，提示 Agent 优先看：
- **认证应试目标**（PMP/CPA/法考）→ 优先看 `assessment/judgment-card`、`assessment/quick-judgment`、`concept-anchoring/fact-vs-judgment`、`assessment/deterministic-anchor`、`structure/multi-source-arbitration`、`structure/foundation-chapter`、`structure/capstone-chapter`、`structure/appendix-compilation`
- **技能掌握目标**（编程/数学/写作）→ 优先看 `assessment/worked-example`、`assessment/application-problem`、`concept-anchoring/socratic-questioning`
- **概念理解目标**（哲学/经济学入门）→ 优先看 `concept-anchoring/precise-definition`、`concept-anchoring/misconception`、`narrative/character-protagonist`、`narrative/running-case`、`structure/recurring-leitmotif`
- **语言学习目标**（英语/外语）→ 优先看 `language-learning/vocabulary-dimension`、`concept-anchoring/socratic-questioning`、`narrative/scenario-hook`

这不是强制，是注意力引导——Agent 仍需遍历所有卡判断适用性。

---

## 模式选型流程三步

1. **带问题翻卡**：带 Phase 3.1 识别的"教学问题"翻卡，每张卡判断"这张卡解决的问题本书有没有"
2. **回答两个强制问题**（写进 style-spec §模式选型说明）：
   - 我考虑过哪些模式、拒绝了哪些、为什么拒绝？
   - 所选每个模式对应本书哪个具体教学问题？
3. **或从预装配包出发再定制**（见下）

审计时核对：声称用了某模式但 style-spec 板块语法里没有对应板块 = 失败。

---

## 参考架构起点（预装配包）

不想从 20 张原子卡拼装时，可以从这三个预装配包出发再定制。选用时在 style-spec 里说明"为什么这个起点适合本书、做了哪些定制"。

### 认证应试蓝本
**适合**：PMP/CPA/法考/医师资格等认证类
**预打包**：precise-definition + misconception + judgment-card + quick-judgment + fact-vs-judgment + deterministic-anchor + practice-gradient + multi-source-arbitration + foundation-chapter + capstone-chapter + cross-ref-trace + appendix-compilation + scenario-hook + running-case（可选 character-protagonist）
**典型样本**：PMP 认证蓝本（`f:/code/po-juan-xie-shu/PMP/textbook/`）

### 叙事入门教材
**适合**：通俗科普/入门教材
**预打包**：precise-definition + misconception + socratic-questioning + application-problem + worked-example + scenario-hook + character-protagonist + running-case + recurring-leitmotif（含判断/选择类知识点时加 fact-vs-judgment）
**典型样本**：CPA 审计教材（`f:/code/po-juan-xie-shu/socratopia-cpa-audit-zh/chapter-01.md`）

### AI 教学蓝本（K-12/技能）
**适合**：英语教材/编程入门/数学
**预打包**：socratic-questioning + precise-definition + worked-example + scenario-hook + vocabulary-dimension（语言类）+ cross-ref-trace
**典型样本**：本 skill v6 的英语七上教材模板

---

## 已完成书的选型示例

### PMP 认证蓝本（human-readable，认证应试起点）
**选用**：precise-definition、misconception、judgment-card（"PMI 会怎么选"板块）、quick-judgment（速判脚本）、fact-vs-judgment（硬记锚 vs 判断分离铁律）、deterministic-anchor（本章硬记锚）、practice-gradient（探索脚本→速判脚本二级梯度）、multi-source-arbitration（ECO/PMBOK7/过程组三源冲突表述范式）、foundation-chapter（Ch2 十二原则/Ch3 八绩效域）、capstone-chapter（Ch18 PMI 思维总集）、cross-ref-trace（"回溯 Ch2 原则6"行内回溯）、appendix-compilation（附录 A/B/C 从硬记锚/速判/eco_tasks 汇编）、scenario-hook（锦程建工医院项目）、running-case（锦程建工贯穿项目）
**拒绝**：character-protagonist（v6 定稿砍小说层，不用第二人称主角）、socratic-questioning（被探索脚本+速判脚本替代）

### CPA 审计教材（human-readable，叙事入门起点）
**选用**：precise-definition（Definition 双讲）、misconception（Common Misconception）、socratic-questioning（探索脚本）、application-problem（Application Problems）、worked-example（审计程序设计题）、scenario-hook（华明制造开章）、character-protagonist（老周/注册会计师视角）、running-case（华明制造贯穿案例）、recurring-leitmotif（职业怀疑/风险→程序→证据→结论/华明低音线）
**拒绝**：judgment-card（CPA 不考"四选项都对选首选"）、quick-judgment（CPA 考长推理不考 77 秒反射）

### 英语七上教材（pure-blueprint，AI 教学蓝本起点）
**选用**：socratic-questioning（💬三类引导问题）、precise-definition（📌知识锚定）、scenario-hook（🎬场景）、vocabulary-dimension（🎯弹药库词汇表）、cross-ref-trace（🔗跨单元连接表）
**拒绝**：judgment-card、quick-judgment（英语不考判断题）、fact-vs-judgment（英语无判断vs事实分离需求）

---

## 全部卡索引（按教学问题分组）

### 概念锚定类（concept-anchoring/）
| 卡 | 解决什么问题 |
|---|---|
| precise-definition | 权威术语/公式/分类怎么呈现才防幻觉又促理解（原文+大白话双讲） |
| misconception | 学习者的常见误区怎么提前暴露和拆解 |
| socratic-questioning | 怎么设计提问路线图引导学生自己推导 |
| fact-vs-judgment | 确定性知识（要背）和判断（要推理）怎么分离才不混淆 |

### 评估/练习类（assessment/）
| 卡 | 解决什么问题 |
|---|---|
| judgment-card | 有明确权威偏好的判断题怎么呈现（首选+why-not+判断依据） |
| quick-judgment | 限时/短情境选择题怎么设计教反射 |
| application-problem | 长情境多步推理题怎么设计 |
| worked-example | 例题/代码/计算题怎么做"示范解题" |
| practice-gradient | 练习怎么按 recall→transfer→open 梯度分层 |
| deterministic-anchor | 必背/确定知识清单怎么组织 |

### 叙事结构类（narrative/）
| 卡 | 解决什么问题 |
|---|---|
| scenario-hook | 章首怎么用具体情境开章 |
| running-case | 怎么用一个贯穿案例做连续情境语料 |
| character-protagonist | 要不要用主角/第二人称戏剧化 |

### 整书架构类（structure/）
| 卡 | 解决什么问题 |
|---|---|
| foundation-chapter | 要不要为其他章单独设"判断根供给"地基章 |
| capstone-chapter | 要不要设总结/收网章 |
| cross-ref-trace | 跨章引用用什么形式（行内回溯/连接表） |
| appendix-compilation | 附录从哪些章末板块汇编、怎么汇编 |
| multi-source-arbitration | 多份权威源冲突时怎么表述和裁决 |
| recurring-leitmotif | 贯穿全书的主题低音线怎么设（非人物非案例） |

### 语言学习特化（language-learning/）
| 卡 | 解决什么问题 |
|---|---|
| vocabulary-dimension | 词汇怎么按 L1-L4 分层管理 |
```

- [ ] **Step 2: 提交**

```bash
cd F:/code/craft-your-textbook
git add skills/craft-your-textbook/references/patterns/README.md
git commit -m "feat: 写 patterns/README.md——模式库索引+选型流程+预装配包+三书示例"
```

---

## Task 7: 写 chapter-grammar-starter.md（组合走查示例）

**Files:**
- Create: `references/chapter-grammar-starter.md`

- [ ] **Step 1: 创建文件**

```markdown
# 章节语法起点——从模式卡组合章结构的走查示例

> 这不是硬模板，是一个"怎么从模式卡组合出章节语法"的示范走查。
> Phase 3.3 设计板块语法时参考这个走查思路，不要照抄结构。
> 示范对象：PMP 一章（以 Ch4 冲突·领导·团队为例）。

---

## 走查过程

### 第一步：从预装配包出发

PMP 是认证类，选"认证应试蓝本"预装配包，拿到 14 张候选卡。

### 第二步：本书特化裁剪

1. **砍小说层**：PMP v6 定稿砍人物情感弧线 → 拒绝 character-protagonist
2. **替代提问卡**：认证类需要应试反射 → 用 quick-judgment（速判）+ judgment-card（首选卡）组合，替代 socratic-questioning（探索脚本保留但作为 judgment 配套）
3. **加硬记/判断分离**：PMP 有大量"框架名要背、何时用要推"的知识 → fact-vs-judgment 必选

### 第三步：把选的卡映射为板块

选出的卡 → 章内板块位置：

| 模式卡 | 在章内的位置/板块名 |
|---|---|
| scenario-hook | 章首（无编号，引用块） |
| precise-definition | 每小节内的 `### Definition: X` 子板块（循环单元内） |
| misconception | 每小节内的 `### Common Misconception` 子板块 |
| judgment-card | 每小节内的 `### PMI 会怎么选` 子板块 |
| fact-vs-judgment | 章末 `## 本章硬记锚`（放事实）+ judgment-card（放判断），分离 |
| deterministic-anchor | 章末硬记锚里的条目 |
| practice-gradient | 章末双脚本：探索脚本→速判脚本（recall→transfer 梯度） |
| quick-judgment | 章末速判脚本里的题 |
| cross-ref-trace | judgment-card 内"判断依据：回溯 Ch2 原则6"行内回溯 |
| running-case | scenario-hook 挂靠锦程建工项目 |
| multi-source-arbitration | META 里三源范式（本书级，非章内板块） |

### 第四步：确定章骨架

得到 PMP Ch4 的骨架：

```markdown
# Chapter 4 · 冲突、领导、团队与基本规则——副标题
（YAML frontmatter: eco_tasks/chapter_type/pmbok7_anchor/...）
> [锦程建工情境钩子]

## 4.1 [小节标题]
[叙事 prose]
### Definition: [概念]（precise-definition）
[PMBOK 原文定义]
用通俗的话说：[大白话]
### Common Misconception（misconception）
### PMI 会怎么选（judgment-card + cross-ref-trace）

## 4.2 ...（同上循环）

## 本章硬记锚（fact-vs-judgment + deterministic-anchor）
[必背框架清单，只放事实不放判断]

## 【AI 老师提问脚本】（practice-gradient）
### 探索脚本：[问题链]
### 速判脚本：[四选一短情境]（quick-judgment）
```

### 第五步：声明可选板块

在 style-spec 里声明：`judgment-card` 是可选板块——技术性小节无 PMI 偏好时允许略去，不硬凑。

---

## 关键思路

1. **先选卡再映射为板块**，不是先列板块再找卡填
2. **同一张卡可以出现在不同位置**（precise-definition 在小节内，cross-ref-trace 行内嵌入）
3. **卡是原子的，板块是组合的**——章骨架是卡组合后的结构，不是卡的平铺
4. **每章有可选板块的弹性**——声明哪些板块可略去，避免硬凑
5. **整书级卡（foundation-chapter/multi-source-arbitration/appendix-compilation）不进章骨架**，它们是 OUTLINE 层面的设计

用同样的走查方法，CPA 一章的骨架会映射为：
- scenario-hook + character-protagonist → 章首老周视角叙事
- precise-definition → `### Definition: X`
- misconception → `### Common Misconception`
- application-problem + worked-example → 章末 Exercises（Concept Check/Application Problems/Think Deeper 三级）
- recurring-leitmotif → prose 里行内点题
```

- [ ] **Step 2: 提交**

```bash
cd F:/code/craft-your-textbook
git add skills/craft-your-textbook/references/chapter-grammar-starter.md
git commit -m "feat: 写 chapter-grammar-starter.md——PMP 走查示例"
```

---

## Task 8: 写 concept-anchoring 四张卡

**Files:**
- Create: `references/patterns/concept-anchoring/precise-definition.md`
- Create: `references/patterns/concept-anchoring/misconception.md`
- Create: `references/patterns/concept-anchoring/socratic-questioning.md`
- Create: `references/patterns/concept-anchoring/fact-vs-judgment.md`

每张卡严格按六节统一格式（解决什么教学问题 / 什么时候用 / 长什么样 / 已知陷阱 / 变体 / 不要这样用），包含真实样本片段。

- [ ] **Step 1: 写 precise-definition.md**

```markdown
# 精确呈现（Precise Definition）

## 解决什么教学问题
权威术语/公式/分类/硬数字怎么呈现才同时做到：① 防幻觉（AI 不杜撰定义）② 促理解（学生不只背条文还懂直觉）。

## 什么时候用 / 什么时候不用
- 用：书里有正式定义的术语、定理、公式、分类名称、硬数字（年份/金额/阈值）时
- 不用：纯叙事过渡、案例描述、无正式定义的派生概念
- 典型搭配：misconception（定义后紧跟误区）、fact-vs-judgment（定义属事实）
- 理科/认证类密度最高（几乎每节都有），语言类中等，叙事类较低

## 长什么样（结构示例）

PMP 样本（见 PMP Ch4 §4.1 / PMP Ch4 §4.2）：
```markdown
### Definition: 领导力 vs 职权
**领导力（Leadership）**是对项目团队内外的个人施加**影响**、以实现预期成果的态度、才能、性格和行为。它不为任何特定角色独有——项目经理、发起人、甚至普通团队成员都可能展现领导力。

**职权（Authority）**是组织正式赋予某人的、行使权力的权利，通常通过章程文件或指定职务授予。

用通俗的话说：职权是"我有权命令你"，领导力是"你愿意跟我走"。
```

CPA 样本（见 CPA Ch1）：
```markdown
### Definition: 鉴证业务
注册会计师执行的、旨在对**鉴证对象信息**提出**结论**、以增强**预期使用者**对该信息**信任程度**的业务，称为鉴证业务。

用通俗的话说：鉴证业务就是"找个可信的专业人士来给一项信息背书"。
```

结构要点：
- `### Definition: 术语名` 作为子标题
- 一段严谨的正式定义（回源核对过的），关键术语粗体
- 空一行后用固定引导句 "用通俗的话说：" 给直觉解释
- 理科公式同理：先写原文公式，再给公式各变量的物理/数学直觉

## 已知陷阱
- ❌ 只有大白话没有正式定义 → 失去防幻觉锚点，AI 会自行发挥
- ❌ 只有正式定义没有通俗解释 → 学生/AI 只能背条文不懂应用
- ❌ "用通俗的话说"里杜撰原文没有的内容 → 通俗化变歪曲，必须和正式定义一致
- ❌ 一个 Definition 塞 5+ 术语 → 每个核心术语单独卡，方便 AI 老师独立调用

## 变体
- **公式密集型**（理科/财务）：Definition 里放公式块，"用通俗的话说"解释每个变量和适用条件
- **双语源**（中文学外文知识）：Definition 给原文拼写+中文翻译双讲
- **blueprint 路线**：可以在 Definition 后加"回源：P7-a L886-930"行内行号（human-readable 不加）

## 不要这样用
- ❌ 把案例/例子放在 Definition 里——案例放在 narrative 正文或 worked-example
- ❌ 把判断/偏好放在 Definition 里（"项目经理应当 X"是判断不是定义，去 judgment-card）
- ❌ Definition 里用"你可以把它理解为……"代替"用通俗的话说："——固定引导句让 AI 和人都知道这是第二讲
```

- [ ] **Step 2: 写 misconception.md**

```markdown
# 误区桩（Common Misconception）

## 解决什么教学问题
学习者对某个概念最常见的误解/错误直觉怎么提前暴露和拆解，让 AI 老师专挑易错点操练。

## 什么时候用 / 什么时候不用
- 用：有高频错误/典型误解/考生常掉的坑时（几乎每章都有）
- 不用：纯事实性知识（无误解空间，如"Scrum 有三个角色"）
- 典型搭配：precise-definition 之后紧跟；judgment-card 之前铺垫

## 长什么样（结构示例）

PMP Ch4 §4.2：
```markdown
### Common Misconception
**误解："项目经理是团队的头，就该有'领导范儿'，遇事拿主意、下命令，把团队指挥得井井有条。"**

这是把"职权型管理者"当成了"领导者"。真相是：PMI 推崇的现代项目领导，更接近**仆人式领导（servant leadership）**——领导者先服务团队、扫清障碍、赋能成员，而不是站在团队上面发号施令。
```

CPA Ch1：
```markdown
### Common Misconception
很多人以为"审计就是会计师再把账重新做一遍，看管理层算得对不对"。这是个常见的误解。

审计不是替管理层重做账。账是管理层的责任……（下略）
```

结构要点：
- `### Common Misconception` 作为子标题（blueprint 可改中文"### 常见误区"，但要在 style-spec 统一）
- 一句加粗的口语化误区句起头（模仿考生真会说的话）
- 拆解三段：先承认"为什么会这么想" → 指出"错在哪" → 给"正确姿势"

## 已知陷阱
- ❌ 误区句太书面/不像学生真会说的话 → AI 老师抓不到痛点，失去暴露价值
- ❌ 只有正确答案没有"为什么会这么想" → 学生不知道自己为什么错，换个题还错
- ❌ 一个 misconception 塞多个误区 → 每个误区单独一个桩，方便 AI 老师独立调用

## 变体
- **blueprint 路线**：旧 7 板块里"💬陷阱暴露问题"本质就是 misconception 的问题化形式——可以用"误区+暴露问题"组合
- **理科/数学**：误区可配一个"算错的例子"——把常见错解一步步算出来再指出错在哪

## 不要这样用
- ❌ 把 misconception 写成 judgment-card（"PMI 认为 X"）——误区桩是拆解错因，判断题是选首选，两种模式
- ❌ 用"很多人误以为……但实际上……"这种弱化句式——加粗口语句模仿真学生说话更有穿透力
```

- [ ] **Step 3: 写 socratic-questioning.md**

```markdown
# 苏格拉底提问路线图（Socratic Questioning）

## 解决什么教学问题
怎么给 AI 老师一套结构化提问方向，让它能引导学生自己推导知识、而不是直接讲答案。

## 什么时候用 / 什么时候不用
- 用：需要学生"自己推出来"的概念、原理、推理链
- 不用：纯事实记忆（"Scrum 三角色是什么"不用引导，直接 deterministic-anchor）；有强权威偏好的判断题（用 judgment-card 替代或配套）
- 典型搭配：precise-definition（定义后引导推导）；blueprint 路线的核心模式
- 认证类的"探索脚本"本质就是这个卡的一种形态

## 长什么样（结构示例）

英语教材旧 7 板块（💬三类问题）：
```markdown
### 💬 苏格拉底引导方向
**场景激活问题**（从 🎬 场景切入）：
- "Tom 说 'I'm 12 years old.' 但他不说 'I 12'。为什么中间要多一个 am？"
- [3-5 个问题]

**概念发现式追问**（引导学生自己推导规则）：
- "你注意到没有，'I am'、'You are'、'He is'，三个主语后面跟的动词不一样。能不能猜一下 She 后面该跟哪个？"
- [3-5 个问题]

**陷阱暴露问题**（针对学习者常见误区）：
- "很多同学会写 'He don't like apples'，但这是错的。你知道错在哪里吗？"
- [2-8 个问题]
```

PMP 章末"探索脚本"变体：
```markdown
### 探索脚本：引导式问题链（教判断力）
按下列顺序引导学员，不要直接给答案：
1. （从情境切入）"老陈面对两个分包吵架，你觉得他第一步该做什么？为什么？"
2. "如果他直接拍板定顺序，可能会有什么后果？"
3. "那什么情况下，'强迫'反而是对的？"
...（共 8 问）
```

结构要点（三层问题）：
1. **场景激活问题**：从章首情境/学生已有经验切入，制造悬念
2. **概念发现式追问**：引导学生观察模式→自己归纳规则→走到概念
3. **陷阱暴露问题**：针对典型误区，让学生自己发现错在哪

## 已知陷阱
- ❌ 问题是反问句或含答案（"难道我们不应该合作吗？"）→ 学生不用思考
- ❌ 问题顺序不对（先问抽象规则再问具体情境）→ 违背"先具体后抽象"的认知顺序
- ❌ 问题太少（1-2 个）→ 构不成推导链，学生走不完全程
- ❌ 把"三类问题"当成硬模板每章必写——可以根据章内容调整（如纯事实章少追问多锚定）

## 变体
- **blueprint 路线**：可以用 emoji（💬）+ 明确三类小标题，AI 解析高效
- **human-readable 路线**：改为章末"思考题/讨论题"有序列表，去掉 emoji 和"陷阱暴露"标签，但保留三层递进
- **认证类探索脚本**：去掉"概念发现"层，改为"情境→偏好暴露→例外追问"结构

## 不要这样用
- ❌ 写死老师的回应（学生答 X 老师说 Y）——那是对话脚本，违反 I5（非对话体）
- ❌ 把问题答案写在问题下面——AI 老师要现场发挥，不是念答案
- ❌ 所有章用同一套问题不做定制——问题要锚定本章的具体情境和具体概念
```

- [ ] **Step 4: 写 fact-vs-judgment.md**

```markdown
# 确定性知识 vs 判断分离（Fact vs Judgment）

## 解决什么教学问题
一本书里有两类知识：①确定性知识（框架名/阶段名/公式/分类，要背）②判断知识（何时用 X/首选什么/什么例外，要推）。混在一起会导致 AI 老师把判断当事实教、学生把偏好当公理背。

## 什么时候用 / 什么时候不用
- 用：认证类/应试类/任何有"权威偏好/标准答案"的领域
- 不用：纯技能/纯入门/无判断空间的事实类（"Python 列表用 [] 声明"没什么可判断的）
- 典型搭配：deterministic-anchor（承载事实）+ judgment-card（承载判断）

## 长什么样（结构示例）

PMP 的分离做法（PMP Ch4 章末）：

事实部分（硬记锚）：
```markdown
## 本章硬记锚
> 以下是需要"背下来"的框架（区别于上面的"判断"）。考场上这些是可以直接调用的确定知识。

1. **冲突解决六方法**：面对-解决问题 · 合作 · 妥协 · 缓和-包容 · 强迫 · 撤退-回避。
2. **塔克曼五阶段**：形成 → 震荡 → 规范 → 成熟 → 解散。
...（只放名字/列表/公式，不放"何时用哪种"）
```

判断部分（每小节内的 judgment-card）：
```markdown
### PMI 会怎么选
**情境**：两个分包当众争执...
**PMI 首选**：C（面对/解决问题）。
**为什么不是其他**：A 是强迫但这里没安全红线...
**判断依据**：团队绩效域 + 原则6。
```

结构要点：
- 事实放章末集中清单（deterministic-anchor）
- 判断放节内 judgment-card
- 硬记锚条目不允许出现"默认首选/例外/何时用"这类判断词
- judgment-card 的选项/why-not/依据完整呈现

## 已知陷阱（来自 PMP 金标准踩坑）
- ❌ 硬记锚里混入"默认首选面对-解决问题" → 这是判断不是事实，必须剥离到 judgment-card
- ❌ judgment-card 里不标判断依据 → 偏好断言没回根，违反 I2
- ❌ 分离不彻底（事实清单里有"PMI 倾向于 X"） → 背的人背了错东西

## 变体
- **CPA 版**：事实放"Definition"节，判断放"Common Misconception + Exercises 解析"，但不集中到章末清单
- **理科版**：事实=公式/定理陈述，判断=公式适用条件/何时用哪个

## 不要这样用
- ❌ 把"PMI 会怎么选"的答案放进硬记锚——那是推理结论不是事实
- ❌ 为凑硬记锚数量把判断塞进去——少而准比多而杂好
```

- [ ] **Step 5: 验证 4 个文件存在并提交**

```bash
cd F:/code/craft-your-textbook/skills/craft-your-textbook/references/patterns/concept-anchoring
ls -la  # 应有 4 个 .md 文件
cd F:/code/craft-your-textbook
git add skills/craft-your-textbook/references/patterns/concept-anchoring/
git commit -m "feat: 写 concept-anchoring 四张模式卡"
```

---

## Task 9: 写 assessment 六张卡

**Files:**
- Create: `references/patterns/assessment/judgment-card.md`
- Create: `references/patterns/assessment/quick-judgment.md`
- Create: `references/patterns/assessment/application-problem.md`
- Create: `references/patterns/assessment/worked-example.md`
- Create: `references/patterns/assessment/practice-gradient.md`
- Create: `references/patterns/assessment/deterministic-anchor.md`

- [ ] **Step 1: 写 judgment-card.md**

```markdown
# 判断题/首选卡（Judgment Card）

## 解决什么教学问题
有明确权威偏好的场景判断题怎么呈现：首选是什么、为什么不是其他选项、判断依据来自哪里。认证类"四个都对选首选"题型的核心模式。

## 什么时候用 / 什么时候不用
- 用：领域内有明确"在 X 情境下权威偏好 Y"的判断（PMP 的 PMI 偏好、法律的"应当"、医学的"首选治疗"）
- 不用：无权威偏好的开放性问题；纯事实记忆
- 典型搭配：fact-vs-judgment（判断专属区）、cross-ref-trace（依据回根）、misconception（先拆误区再给首选）
- 有 PMI 偏好/准则倾向/标准答案判断的小节每节一个，无偏好小节允许略去不硬凑

## 长什么样（结构示例）

PMP Ch4 §4.1：
```markdown
### PMI 会怎么选
**情境**：两个分包的现场负责人为施工顺序当众争执，进度已滞后但不涉及安全红线，双方权力相当，项目经理有时间介入。项目经理第一步该做什么？
- A. 自己拍板定一个施工顺序，让两家照做
- B. 把矛盾上报给业主，让上级施压解决
- C. 把两家负责人拉到一起，弄清各自的技术顾虑，引导他们找到都能接受的方案
- D. 让他们冷静几天，也许问题会自己消解

**PMI 首选**：**C（面对/解决问题 + 合作）**。

**为什么不是其他**：
- A（强迫）看似果断，但这里没有安全红线、没有时间紧迫到不能谈——凭权力压下去会埋下怨气。强迫只在"安全/无时间"时才对。
- B（上报/升级）看似借力，但 PMI 眼里升级是最后手段，不是第一动作。
- D（撤退/回避）看似给冷静期，但进度已在滞后，放任只会让问题恶化。

**判断依据**：回溯**团队绩效域**（营造协作环境）与**十二原则之原则6 展现领导力行为**。
```

结构要点：
- `### PMI 会怎么选`（书名可改为"### 准则怎么判"等，style-spec 统一）
- **情境**：1-3 句具体情境（含约束）+ 4 选项
- **首选**：加粗明确选项
- **为什么不是其他**：逐项 why-not，每项说清"看似对但……"
- **判断依据**：必填，回已声明的判断根（原则/绩效域/准则条款），标不出的宁可不写

## 已知陷阱（来自 PMP 金标准二轮复审）
- ❌ why-not 杜撰附加条件贬低候选项（为了把首选"拱出来"发明原文没有的条件）→ why-not 只能用权威原文明确说过的适用条件
- ❌ 判断依据写"PMI 一般偏好..."这种空话 → 必须回具体原则/条款
- ❌ 4 选项里 3 个明显错只有 1 个对 → 失去"四个都像对"的训练价值
- ❌ 正确答案靠贬低候选项证成 → 要靠"首选项更优"证成

## 变体
- **human-readable 路线**：可以去掉 A/B/C/D 选项格式，改为叙事化描述"在这种情况下，注册会计师应当……"
- **法律/医学类**："首选"改为"应当/推荐/一线方案"，依据回法条/指南

## 不要这样用
- ❌ 把 judgment-card 当事实写进硬记锚（见 fact-vs-judgment）
- ❌ 无权威偏好的小节硬凑一个"首选"——诚实承认"这种情形下无唯一偏好，要看具体约束"
```

- [ ] **Step 2: 写 quick-judgment.md**

```markdown
# 速判/限时选择题（Quick Judgment）

## 解决什么教学问题
短情境选择题/限时判断题怎么设计，训练学习者"读约束条件→出正确牌"的反射速度。

## 什么时候用 / 什么时候不用
- 用：认证/应试类需要快速判断的题型（PMP 77秒/题、驾照科目一）
- 不用：需要长推理的题（用 application-problem）；非应试场景（不需要反射速度）
- 典型搭配：judgment-card（章内学判断，章末速判练反射）、practice-gradient（速判是 transfer 层）

## 长什么样（结构示例）

PMP Ch4 章末速判 2：
```markdown
**速判 2**（升级是最后手段）：某跨国 IT 团队两名成员就技术方案分歧，情绪尚可、时间充裕、双方平级。项目经理第一步？
- A. 上报部门总监裁决 　B. 各打五十大板要求妥协 　C. **引导两人正面讨论、弄清分歧、寻求共识** 　D. 谁资历老听谁的
- **PMI 首选：C**。why-not：A 过早升级；B 妥协在权力相当时确也适用，但有时间+信任时 PMI 更倾向合作"把蛋糕做大"；D 以地位压制。**依据**：PMI 冲突路径"先自行/私下合作解决"。
```

结构要点：
- 1-2 句情境 + 4 选项（一题一段，紧凑）
- 答案 + why-not + 依据，每题 100-150 字
- 3-5 题/章（不要更多——60-90 题建不了真反射，靠题库接力，诚实说明边界）

### 抗迁移补丁（PMP 实战经验）
速判题情境**刻意跨行业**（制药/IT/跨国/快消等），不与主线案例同行业，训练"判断依据可跨行业迁移"。主线案例留章首情境钩子用。

## 已知陷阱
- ❌ 速判题全部用同一行业情境 → 迁移失败，考场上遇陌生行业卡住
- ❌ 题量虚高声称"足够通过考试" → 诚实声明速判脚本是"示范思路"不是"刷题量"
- ❌ 速判题解析超过 200 字 → 速判要快节奏，长解析变 application-problem

## 变体
- **human-readable 路线**：章末"思考题"里的短选择题，去掉"速判"标签
- **blueprint 路线**：可以用"速判脚本"作为 AI 老师元指令块标题

## 不要这样用
- ❌ 用速判代替长推理题——它们训练不同能力，搭配 practice-gradient
- ❌ 每题都用 4 选项——是非题/填空题可以，格式服务于反射训练
```

- [ ] **Step 3: 写 application-problem.md**

```markdown
# 长情境多步推理题（Application Problem）

## 解决什么教学问题
复杂、多步骤、需要展示完整推理链的综合题怎么设计。CPA 审计/数学证明/编程设计/案例分析的核心练习模式。

## 什么时候用 / 什么时候不用
- 用：需要多步推理/综合多个概念/展示完整解题路径的题
- 不用：单步判断题（quick-judgment）；纯事实记忆（deterministic-anchor）
- 典型搭配：worked-example（先示范一道，再让学生做）、practice-gradient（application 是 open reasoning 层）

## 长什么样（结构示例）

CPA Ch1：
```markdown
### Application Problems

**Q2.** 你是华明制造审计项目的注册会计师。期末复核时，你注意到一笔在 12 月 30 日开出发货单、确认了 500 万元收入的大额销售，对方是华明的老客户，但货物直到次年 1 月初才实际离开仓库。华明的利润总额是 6,000 万元。请从三方关系和审计本质的角度，说明：你为什么必须关注这笔业务？它和"信息不对称"有什么关系？

Hint
站在老周的位置想：如果这 500 万元不该算进今年，对他读到的"6,000 万利润"意味着什么？

**Answer:**
**为什么必须关注。** 收入确认的一个基本前提是商品控制权已转移给客户……（完整推理链，多段）
```

结构要点：
- 一个真实/半真实的具体情境
- 多问（不是选 ABC），要求学生构建完整推理
- 附 Hint（引导思考方向，不给答案）
- 附完整 Answer（展示完整推理链，不是最终数字）

## 已知陷阱
- ❌ 题目太抽象无具体情境 → 变成知识背诵不是应用
- ❌ Answer 只给最终结论不给推理过程 → 学生不知道"怎么想到的"
- ❌ 所有题同构 → 无法训练迁移

## 变体
- **理科版**：推导题、证明题——Answer 展示完整推导步骤
- **编程版**：系统设计/debug 题——Answer 展示思考路径+代码
- **human-readable**：章末"思考题/讨论题"

## 不要这样用
- ❌ 把 application-problem 拆成多个 quick-judgment——它的价值在推理链完整性
```

- [ ] **Step 4: 写 worked-example.md**

```markdown
# 例题演练（Worked Example）

## 解决什么教学问题
需要展示"怎么做"的程序性知识——例题/代码/计算题/标准流程怎么写得让学生能跟着走一遍。

## 什么时候用 / 什么时候不用
- 用：编程/数学/物理/审计程序设计/任何"需要看一个完整示范"的技能
- 不用：纯概念理解（application-problem 更合适）；判断偏好（judgment-card）
- 典型搭配：application-problem（先 worked-example 示范，再让学生做）

## 长什么样（结构示例）

编程类：
```markdown
### 例：用递归算斐波那契数列

**问题**：写一个函数 fib(n) 返回第 n 个斐波那契数。

**新手常写的版本（有问题）**：
```python
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)
```
问题：重复计算，fib(5) 会算两次 fib(3)，n=40 就明显变慢。

**改进版本（带缓存）**：
```python
from functools import lru_cache
@lru_cache(maxsize=None)
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)
```
关键改进：@lru_cache 缓存已计算结果，时间复杂度从 O(2^n) 降到 O(n)。
```

数学/审计同理：完整展示一道题的解题过程，标注关键步骤和常见错在哪。

## 已知陷阱
- ❌ 跳过中间步骤直接给最终代码/答案 → 学生看不出"怎么想到的"
- ❌ 例子太小太 trivial（print("hello")）→ 不具示范价值
- ❌ 例子太大超过一章范围 → 拆成多章或者简化

## 变体
- **审计/法律版**：展示完整的审计程序设计/法律文书撰写流程
- **blueprint**：可作为 AI 老师的"标准答题模板"

## 不要这样用
- ❌ worked-example 替代学生自己做的 application-problem——示范+练习要搭配
```

- [ ] **Step 5: 写 practice-gradient.md**

```markdown
# 练习三级梯度（Practice Gradient）

## 解决什么教学问题
章末练习怎么按认知梯度分层设计，从记忆到迁移到开放推理，而不是平铺一堆同构题。

## 什么时候用 / 什么时候不用
- 用：章末有练习题/教学脚本时（几乎所有书）
- 不用：纯参考手册/字典式工具书（没练习）
- 典型搭配：quick-judgment、application-problem、deterministic-anchor——梯度决定这些卡的题在章末怎么排

## 长什么样（结构示例）

CPA Ch1 章末（三级梯度的典型）：
```markdown
### Concept Check  ← recall 层：记忆/识别
[3 道选择题，考核心概念记忆]

### Application Problems  ← transfer 层：应用/迁移
[2 道多步推理题，考多概念综合应用]

### Think Deeper  ← open reasoning 层：开放推理
[2 道讨论题，没有唯一答案，考批判性思考]
```

PMP 章末（二级梯度，认证类不需要开放讨论）：
```markdown
### 探索脚本：引导式问题链  ← recall+transfer
[8 问，从情境暴露直觉→推导出 PMI 取向]

### 速判脚本  ← transfer+反射
[5 道四选一短情境，考跨行业迁移的反射]
```

三级梯度（由浅到深）：
1. **Recall/记忆层**：核心概念识别、事实确认、术语回忆。Concept Check/探索脚本前半。
2. **Transfer/迁移层**：把概念用到新情境、跨领域迁移、多概念综合。Application Problems/速判脚本。
3. **Open Reasoning/开放推理层**：无唯一答案的讨论题、批判性反思、边界探讨。Think Deeper。

## 已知陷阱
- ❌ 所有题在 recall 层（"什么是 X？""定义 Y"）→ 学生背得熟但不会用
- ❌ 一开始就 open reasoning → 学生没地基讨论不出东西
- ❌ 三级都必须有 → 认证类书（如 PMP）可两级，入门读物可三级全有

## 变体
- **认证类**：二级（探索→速判），不需要 open reasoning（考试不考）
- **技能类**：二级（worked-example 示范→application-problem 练习）
- **叙事教材**：三级全有

## 不要这样用
- ❌ 把梯度当硬模板每章必套三级——按书的教学目标选级数
```

- [ ] **Step 6: 写 deterministic-anchor.md**

```markdown
# 必背锚/确定知识清单（Deterministic Anchor）

## 解决什么教学问题
需要直接调用的确定性知识（框架名/阶段名/公式/分类/术语）怎么集中组织成清单，方便学生记忆和 AI 老师检索。

## 什么时候用 / 什么时候不用
- 用：有需要硬记/肌肉记忆的确定知识（认证/理科/语言/医学）
- 不用：纯概念理解/无记忆内容的书
- 典型搭配：fact-vs-judgment（硬记锚只放事实）、appendix-compilation（硬记锚汇编为附录卡集）

## 长什么样（结构示例）

PMP Ch4 章末：
```markdown
## 本章硬记锚
1. **冲突解决六方法**：面对-解决问题 · 合作 · 妥协 · 缓和-包容 · 强迫 · 撤退-回避。
2. **塔克曼五阶段**：形成 → 震荡 → 规范 → 成熟 → 解散。
...（8 条）
```

结构要点：
- 章末 `## 本章硬记锚`（或类似标题，style-spec 统一）
- 编号清单，每条一个确定知识
- 只放名字/列表/公式/关系——不放"何时用/首选/例外"
- 教学重组条目加注解（"教学提炼，原文为 X 条，完整见 §Definition"）

## 已知陷阱（来自 PMP 金标准）
- ❌ 硬记锚里混入判断（"PMI 默认首选 X"）→ 剥离到 judgment-card
- ❌ 硬记锚条目不精准（"冲突五方法"vs PMBOK7 原文"六方法"）→ 必须回源逐字核对
- ❌ 清单过长（>10 条/章）→ 考虑拆分章节或放宽粒度

## 变体
- **理科章末**：公式清单（不加多余文字）
- **语言章末**：词汇表（搭配 vocabulary-dimension）
- **汇编为附录**：各章硬记锚汇总为"必背框架卡集"附录（用 appendix-compilation 卡）

## 不要这样用
- ❌ 用硬记锚替代正文讲解——清单是章末总结，不能替代 Definition 和叙事
- ❌ 硬记锚里加"注意""例外"——那些是判断，进 judgment-card
```

- [ ] **Step 7: 提交 assessment 六卡**

```bash
cd F:/code/craft-your-textbook
git add skills/craft-your-textbook/references/patterns/assessment/
git commit -m "feat: 写 assessment 六张模式卡"
```

---

## Task 10: 写 narrative 三张卡

**Files:**
- Create: `references/patterns/narrative/scenario-hook.md`
- Create: `references/patterns/narrative/running-case.md`
- Create: `references/patterns/narrative/character-protagonist.md`

- [ ] **Step 1: 写 scenario-hook.md**

```markdown
# 情境钩子开章（Scenario Hook）

## 解决什么教学问题
章首怎么用一个具体的、有悬念的情境切入，让 AI 老师开课时有素材、人类读者有阅读动力。

## 什么时候用 / 什么时候不用
- 用：几乎所有章（概念/技能/应试都需要情境锚点）
- 不用：纯参考/手册型书（字典/API 文档）
- 典型搭配：running-case（钩子挂靠贯穿案例）、character-protagonist（钩子用主角视角）

## 长什么样（结构示例）

PMP Ch4（第三人称中性）：
```markdown
> 锦程建工的"市中心医院综合体"项目进入土建阶段的第二个月。机电分包与土建分包在管线预埋的施工顺序上僵持了两周——两家的现场负责人在监理例会上当众拍了桌子，关键线路已经滞后 5 天。项目经理老陈坐在会议室里，面前摆着三个选择...
```

CPA Ch1（第二人称/主角代入）：
```markdown
老周手里攥着一份打印出来的财务报表，封面上写着"华明制造股份有限公司"。这是一家 A 股上市的精密零部件制造企业，资产总额 12 亿元...老周想拿出一笔钱买它的股票，但他翻到利润表那一栏，盯着"利润总额 6,000 万元"这个数字看了很久...
```

结构要点：
- 章首（YAML frontmatter 后，第一个 `##` 前），无编号，引用块格式
- 2-4 段，约 300-600 字
- 必含：具体实体（公司名/角色名）+ 具体数字（金额/工期/人数）+ 具体约束/冲突 + 一句导向本章核心问题的"逼问"
- 挂靠贯穿案例（如有）

## 已知陷阱
- ❌ 空泛："某项目遇到冲突，项目经理该怎么办？" → 没有具体实体，AI 没有弹药
- ❌ 过长（>600 字）铺陈太多 → 钩子变小说开头，喧宾夺主
- ❌ 没有逼问句收尾 → AI 老师不知道这节课要解决什么
- ❌ PMP 砍了小说层还在用第二人称戏剧化 → 风格错配

## 变体
- **blueprint 路线（旧 7 板块🎬场景）**：分"前段·开课钩子（抛悬念）"和"后段·收尾回响（推导后回扣）"，可以更短更结构化
- **human-readable 中性**：第三人称（PMP 风格）
- **human-readable 戏剧化**：第二人称/主角视角（CPA 风格）

## 不要这样用
- ❌ 钩子写成"本章我们将学习……"的教材式开头 → 零悬念零素材
- ❌ 每章钩子是独立的无关联案例 → 考虑用 running-case 贯穿
```

- [ ] **Step 2: 写 running-case.md**

```markdown
# 贯穿案例语料库（Running Case）

## 解决什么教学问题
怎么用一个贯穿全书的虚构项目/公司/场景，为所有章提供连续的情境素材，制造"上一章我们在这个项目上是怎么判断的"的连续感。

## 什么时候用 / 什么时候不用
- 用：需要跨章连续情境的书（认证/技能/入门都适用）
- 不用：纯参考手册；每章主题完全独立的文集
- 典型搭配：scenario-hook（章首钩子挂靠）；可选搭配 character-protagonist（案例里加主角）
- 与 character-protagonist 互斥：可以只用 running-case 不写主角（PMP），可以两者都用（CPA）

## 长什么样（结构示例）

PMP OUTLINE（只用 running-case，不写主角）：
```markdown
**贯穿案例弹药**（非小说主角，只作 AI 老师提问的情境语料）：全书统一挂靠一个虚构的**建筑企业数字化转型项目**——

> **锦程建工集团承接的"市中心医院综合体"项目**（金额约 8 亿，工期 30 个月）。项目天然含两条线：
> - **预测型主体**（Ch1-12）：土建/机电/装修三大标段，固定总价合同...
> - **敏捷型配套**（Ch13-15）：为项目自研的 BIM 协同平台...
```

CPA（running-case + 主角老周）：华明制造作为贯穿公司，老周作为贯穿主角。

结构要点：
- 在 OUTLINE 里声明贯穿案例是什么
- 给出具体数字/角色/约束（让各章可以引用）
- 声明**边界**：
  - PMP 边界："不写人物情感弧线、不切支线主角、不用第二人称小说"
  - CPA 边界：（可以写老周的心理活动和判断过程）

### 抗迁移失败补丁（PMP 实战）
章末速判/练习题**刻意跳出贯穿案例行业**（PMP 速判题用制药/IT/跨国），训练判断依据的跨行业迁移。主线案例只用于章首情境钩子和探索脚本。

## 已知陷阱
- ❌ 贯穿案例太复杂多条线交织 → 写作 agent 把握不住，写成小说
- ❌ 只在 OUTLINE 声明但各章钩子不挂靠 → 失去连续感
- ❌ 所有练习都用贯穿案例行业 → 迁移失败（考场遇陌生行业不会判断）
- ❌ running-case 被写成小说主线 → 违背 PMP v6 "要案例弹药不要小说"原则

## 变体
- **项目型**：一个虚构项目贯穿（PMP/工程/编程）
- **公司型**：一个虚构公司贯穿（CPA 华明制造/经济学虚拟岛国）
- **人物型**：一个虚构人物的成长/旅程（搭配 character-protagonist）

## 不要这样用
- ❌ running-case 需要多卷长篇小说式展开——案例是素材库不是主线剧情
```

- [ ] **Step 3: 写 character-protagonist.md**

```markdown
# 主角/第二人称戏剧化（Character Protagonist）

## 解决什么教学问题
要不要用一个主角（或第二人称"你"）代入叙事，让读者通过主角的眼睛经历知识的应用过程。

## 什么时候用 / 什么时候不用
- 用：入门读物/叙事教材/需要情感共鸣的书
- 不用：认证类蓝本（PMP 明确砍小说层）；纯参考手册
- 典型搭配：running-case（主角在贯穿案例里活动）、scenario-hook（章首用主角视角切入）
- 与 running-case 可独立选择：PMP 用 running-case 不要主角；CPA 两者都用

## 长什么样（结构示例）

CPA Ch1（第三人称主角老周）：
```markdown
老周手里攥着一份打印出来的财务报表，封面上写着"华明制造股份有限公司"...
老周可能会不满意：我就想要个百分之百的保证...
```

第二人称变体（CPA 也用过）：
```markdown
换你是那位注册会计师，现在你接下了华明制造的审计。你心里要时刻清楚：你不是华明的人，你也不是替老周炒股的人。你是站在中间、靠证据说话的那一个。
```

结构要点：
- 主角有名有姓（"老周"），不是"你"或"某学生"
- 主角有功能性角色（老周=投资者/报表使用者；注册会计师=专业人士）
- 主角的心理活动和判断过程是教学载体——读者通过主角的思考推理学知识

## 已知陷阱
- ❌ 主角有个人情感弧线/成长线 → 变小说偏离教学
- ❌ 第二人称"你是林薇"式小说层（Socratopia 平台已承担人设/情感线功能） → 蓝本不重复承担
- ❌ 主角太完美/从不犯错 → 失去通过错误教学的机会

## 变体
- **第三人称主角**（CPA 老周）：读着像小说，旁观者视角
- **第二人称代入**（部分 CPA 段落）：读者直接代入角色
- **多角色切换**（PMP 不要）：从 PM/监理/分包多角度看同一事件

## 不要这样用
- ❌ PMP 等认证应试蓝本选这张卡——判断/选择题需要的是规范叙事不是戏剧代入
- ❌ 用主角承载平台已有的情感线（Socratopia 人设由平台管，蓝本只供教学素材）
```

- [ ] **Step 4: 提交 narrative 三卡**

```bash
cd F:/code/craft-your-textbook
git add skills/craft-your-textbook/references/patterns/narrative/
git commit -m "feat: 写 narrative 三张模式卡"
```

---

## Task 11: 写 structure 六张卡

**Files:**
- Create: `references/patterns/structure/foundation-chapter.md`
- Create: `references/patterns/structure/capstone-chapter.md`
- Create: `references/patterns/structure/cross-ref-trace.md`
- Create: `references/patterns/structure/appendix-compilation.md`
- Create: `references/patterns/structure/multi-source-arbitration.md`
- Create: `references/patterns/structure/recurring-leitmotif.md`

- [ ] **Step 1: 写 foundation-chapter.md**

```markdown
# 地基章（Foundation Chapter）

## 解决什么教学问题
是否需要在前几章设一两章"不直接对应教学任务/考纲，但为后续所有章供给判断根/前提知识"的地基章。

## 什么时候用 / 什么时候不用
- 用：多源/认证类书有需要反复回溯的核心原则/模型/理论框架（PMP 的十二原则/八绩效域；CPA 的审计三方关系/合理保证）
- 不用：单教材线性推进；无跨章复用的理论根
- 典型搭配：cross-ref-trace（后续章 judgment-card 回溯到地基章）、capstone-chapter（地基→各章→收网呼应）

## 长什么样（结构示例）

PMP Ch2（十二原则）和 Ch3（八绩效域）：
- Ch2 作为 foundation 章，主类型 `chapter_type: foundation`，eco_tasks 为空（不主承任何 ECO 任务）
- Ch2/Ch3 逐条讲透所有原则/绩效域（每条给"准确名称+一句话内核+对应的 PMI 行为倾向"）
- 后续每个 eco_task 章的 judgment-card "判断依据"都回溯到 Ch2/Ch3

结构要点：
- 在 OUTLINE 里明确标注地基章（chapter_type 或类似标记）
- 地基章不挂具体任务/知识点，而是"判断根/理论根"
- 地基章位置在前（第 0 卷/第一部分）
- 地基章必须先通过金标准审计——它是所有后续章的依据

## 已知陷阱
- ❌ 地基章变成"走马观花概览"不深讲 → 后续章回溯时地基不牢
- ❌ 把太多章都设成地基章 → 读者迟迟进不了正题
- ❌ 地基章和后续章的回溯机制没设计好（cross-ref-trace 没选）→ 地基章白写

## 变体
- **理科类**：地基章=数学预备知识章（线性代数基础/概率基础）
- **编程类**：地基章=语言基础语法章
- **叙事入门**：地基章可能不存在（叙事推进不需要独立地基）

## 不要这样用
- ❌ 把"引言/前言"当地基章——地基章是完整教学章，不是概览
```

- [ ] **Step 2: 写 capstone-chapter.md**

```markdown
# 总结/收网章（Capstone Chapter）

## 解决什么教学问题
是否需要在最后设一章把全书的 PMI 偏好/思维模式/应试策略收网汇总，作为收束。

## 什么时候用 / 什么时候不用
- 用：认证类有全书级判断汇总需求（PMP Ch18 PMI 思维总集）；技能类有综合应用章
- 不用：线性教材不需要单独收网章；叙事类收网在最后一章自然完成
- 典型搭配：foundation-chapter（地基→各章→收网首尾呼应）、appendix-compilation（收网章+附录卡集互补）

## 长什么样（结构示例）

PMP Ch18：
- chapter_type: exam_strategy
- 无新源材料，是全书 judgment-card/速判脚本的汇总
- 内容：PMI-ism 优先级层级、BEST/FIRST/NEXT 题型拆解法、"四个都对选首选"判定路径

结构要点：
- 收网章不引入新概念——汇总/提升/体系化已有内容
- 位置在最后（第 4 卷/最后一部分）
- 可包含应试策略/思维总集/综合练习

## 已知陷阱
- ❌ 收网章变成"再来一遍"——要有体系化提升（把碎片偏好组织成判定路径）
- ❌ 收网章引入新内容（违反"不新造"原则）
- ❌ 有地基章无收网章 → 结构不对称

## 变体
- **项目实战章**（编程/技能类）：用一个综合项目串起全书技能
- **应试策略章**（认证类）：题型拆解、时间分配、做题流程

## 不要这样用
- ❌ 收网章代替附录——它是体系化正文，不是速查卡集
```

- [ ] **Step 3: 写 cross-ref-trace.md**

```markdown
# 行内回溯引用（Cross-Reference Trace）

## 解决什么教学问题
章与章之间怎么做知识回扣——是用行内回溯标注、连接表、还是主题低音线。

## 什么时候用 / 什么时候不用
- 用：几乎所有书（I4 跨章引用是不变量）
- 不用：完全独立的文集/参考书
- 典型搭配：foundation-chapter（后续章回溯地基）、recurring-leitmotif（主题低音线也是一种跨章回扣方式）

## 长什么样（结构示例）

PMP 行内回溯（human-readable，技术回根）：
```markdown
**判断依据**：回溯**团队绩效域**（营造协作环境）与**十二原则之原则6 展现领导力行为**。
```

英语教材连接表（blueprint，🔗板块）：
```markdown
## 🔗 与后续单元的连接
| 本单元知识点 | 在后续单元如何使用 | 关联强度 |
|---|---|---|
| be 动词 am/is/are | Unit 3 复数 are / Unit 5 过去式 was/were | 强 |
```

CPA 行内交叉引用（human-readable，自然语言）：
```markdown
独立性这条低音，我们会在全书里反复听到，到第 20 章再系统地展开。
```

三种形式：
1. **行内回溯标签**（PMP 风格）：在 judgment-card 里加一行"回溯 Ch2 原则6"，blueprint/human-readable 都适用
2. **连接表**（英语教材风格）：章末一张表列本章知识点→后续章节，blueprint 风格
3. **自然语言交叉引用**（CPA 风格）：prose 里"正如第 X 章讨论过的""我们会在第 Y 章看到"，最适合 human-readable

## 已知陷阱
- ❌ 回溯指向不存在的章/概念 → 跨章审计必扫
- ❌ 每句都回溯打断阅读 → 只在关键判断处回溯
- ❌ human-readable 用 blueprint 风格的行内标签 → 破坏 prose 流畅感

## 变体
- blueprint：可以用 emoji 标记 + 连接表
- human-readable：自然语言交叉引用为主，关键判断可加技术回根
- 与 recurring-leitmotif 区别：leitmotif 是主题重复（"职业怀疑"在全书出现），cross-ref-trace 是具体指向某章某节

## 不要这样用
- ❌ cross-ref-trace 替代章节内部的讲解——跨章引用是回扣不是内容载体
```

- [ ] **Step 4: 写 appendix-compilation.md**

```markdown
# 附录汇编（Appendix Compilation）

## 解决什么教学问题
附录从哪些章末板块自动/半自动汇编、怎么汇编、附录的定位是什么（速查/卡集/索引）。

## 什么时候用 / 什么时候不用
- 用：有可汇总内容的书（硬记锚、术语表、公式集、覆盖索引）
- 不用：纯叙事入门书（无汇总需求）
- 典型搭配：deterministic-anchor（硬记锚汇编为卡集）、multi-source-arbitration（考纲覆盖索引）、judgment-card（首选卡集）

## 长什么样（结构示例）

PMP 三个附录：
| 附录 | 汇编来源 | 主要源材料校准 |
|---|---|---|
| A ECO 35任务×章节覆盖索引 | 各章 frontmatter eco_tasks grep 汇总 | 考纲 L90-95 |
| B 必背框架卡集 | 各章"本章硬记锚"汇编 | 硬记锚各回本索引对应章核对 |
| C PMI-ism 速判卡集 | 各章"PMI 会怎么选"+速判脚本+Ch18 汇编 | 判断根回溯 Ch2/Ch3 |

结构要点：
- 在 OUTLINE §附录汇编策略里声明：从哪些章末板块汇编成哪些附录
- 汇编是机械操作（merge_book.py 可辅助），不是新写内容
- 附录定位是速查/卡集/索引，不承载首次讲解
- 附录的体量通常是章末相关内容的 10-30% 摘要

## 已知陷阱
- ❌ 附录承载首次讲解（把难的知识推到附录）→ 违反"该在单元里讲清的，别推给附录"
- ❌ 附录和章末内容不一致（汇编了旧版本）→ 汇编后做一致性审计
- ❌ 附录太多（>5 个）→ 考虑合并或放正文

## 变体
- **理科**：公式汇总附录、术语表附录
- **语言类**：词汇总表、语法点速查
- **认证类**：考纲覆盖索引（PMP 附录 A）、必背卡集（PMP 附录 B）、判断速判卡集（PMP 附录 C）

## 不要这样用
- ❌ 附录变成新章节——汇编不是创作
```

- [ ] **Step 5: 写 multi-source-arbitration.md**

## 解决什么教学问题
多份权威源材料（考纲/PMBOK7/过程组/Scrum 指南等）对同一概念给出不同说法时，怎么表述冲突、怎么裁决优先级、怎么组织双层锚定。

## 什么时候用 / 什么时候不用
- 用：≥2 份权威源且层级不同/可能冲突（认证类/交叉教材类最常见）
- 不用：单教材/无源（Mode A）
- 典型搭配：foundation-chapter（判断根来自哪份源）、judgment-card（判断依据回溯到哪份源）

## 长什么样（结构示例）

PMP META §三套知识体系主从关系：
```markdown
| 体系 | 角色 | 用法 |
|------|------|------|
| ECO 35 任务 | 🎯 出题主纲 | 考试怎么考，书就怎么组织 |
| PMBOK7 十二原则+八绩效域 | 🧭 判断根 | 讲"为什么这么做" |
| 过程组+10知识域+ITTO | 🔧 操作细节 | 讲"具体怎么做" |

**双层锚定铁律**：每个 eco_task 章，先用 PMBOK7 原则/绩效域讲"为什么"（判断根）→ 再用过程组/ITTO 讲"怎么做"（操作）。

**三源冲突时的表述范式**：
> "ECO 要求你完成 [X]。过程组的操作是 [Y]。PMBOK7 从原则角度看是 [Z]。"
```

结构要点：
1. **源角色表**：在 META 里声明每源的角色和地位（主/从/真相源）
2. **冲突表述范式**：多源说法不一时，用固定句式并列陈述（"X 要求 A，Y 操作是 B，Z 从原则看是 C"），不假装无冲突
3. **裁决优先级**：权威层级最高的源为准，站队后加注解说明差异
4. **双层锚定**（多源认证类特有）：判断根层（为什么）+ 操作层（怎么做）分源讲透

## 已知陷阱
- ❌ 假装多源无冲突（"各方说法一致"但其实不一致）→ 加注解说明差异
- ❌ 一律以某份源为准忽略其他 → 多源各有价值（考纲给靶子、原文给定义、笔记给骨架）
- ❌ 双层锚定变重复（判断根和操作讲同一件事）→ 判断根讲"为什么"、操作讲"怎么做"，各司其职

## 变体
- **双源（师生合版）**：教师用书补充学生用书没有的评价标准/学情分析/常见错误，用差异比对方法学处理
- **三源+**：PMP 这种多源，需要在 META 里明确主从关系表

## 不要这样用
- ❌ multi-source-arbitration 变成"抄各源原文"——要重组为教学主线服务
```

- [ ] **Step 6: 写 recurring-leitmotif.md**

```markdown
# 贯穿主题低音线（Recurring Leitmotif）

## 解决什么教学问题
怎么设置一条贯穿全书反复出现的主题/态度/推理主轴（非人物非案例），让知识有"低音"伴奏。

## 什么时候用 / 什么时候不用
- 用：需要反复强化某个核心态度/推理范式的书（CPA 的"职业怀疑"、PMP 的"价值交付"）
- 不用：纯事实/技能书（无反复强化的主题）
- 典型搭配：cross-ref-trace（leitmotif 也是一种回扣方式）；和 running-case 区别：leitmotif 是主题，running-case 是实体

## 长什么样（结构示例）

CPA Ch1（首次点出职业怀疑）：
```markdown
这里第一次正式登场的，是一个会贯穿全书的态度——**职业怀疑**。正因为证据是说服性的……注册会计师才不能预设管理层一定诚实……
```

CPA 后面章节反复回扣：到第 10 章评价证据落地、第 15 章舞弊达到高潮。

PMP Ch3 点出"价值交付主线"→ Ch8 钱（价值的预算）→ Ch10 风险（价值的不确定性）→ Ch17 价值实现闭环高潮。

结构要点：
- OUTLINE 里声明低音线是什么、在哪章首次亮相、在哪章高潮
- 首次亮相章点题（"这是一条贯穿全书的主线"）
- 中间各章自然回扣（不是每章都提，但关键节点点题）
- 高潮章收束

## 已知陷阱
- ❌ 低音线太隐蔽读者/AI 抓不住 → 首次亮相明确点题
- ❌ 低音线变成口号每章重复 → 只在关键节点自然回扣
- ❌ 和 running-case 混淆 → running-case 是实体（公司/项目），leitmotif 是主题（态度/原则/方法）

## 变体
- **理科**："守恒思维"/"近似思维"反复强化
- **编程**："先让它跑起来再优化"的工程态度

## 不要这样用
- ❌ leitmotif 替代跨章引用——它是情感/态度线，不是知识回扣
```

- [ ] **Step 7: 提交 structure 六卡**

```bash
cd F:/code/craft-your-textbook
git add skills/craft-your-textbook/references/patterns/structure/
git commit -m "feat: 写 structure 六张模式卡"
```

---

## Task 12: 写 vocabulary-dimension 卡

**Files:**
- Create: `references/patterns/language-learning/vocabulary-dimension.md`

这张卡基于旧 vocabulary-strategy.md 重写，改为模式卡格式。

- [ ] **Step 1: 读旧 vocabulary-strategy.md 取内容**

Run: `cat F:/code/craft-your-textbook/skills/craft-your-textbook/references/vocabulary-strategy.md`（如果已删就从 git 历史恢复）
Expected: 文件在 Task 1 已删，但内容是 L1-L4 分层+三动作（展示/复用/测试）。从 v6 git 历史里读或凭 spec 描述重写。

- [ ] **Step 2: 写 vocabulary-dimension.md**

按六节统一格式写。核心内容：词汇/生词按 L1（课前已知）/L2（本单元核心）/L3（复用拓展）/L4（识别即可）分层；三动作（展示/复用/测试）；音标/词性/例句要求；仅语言类需要。

```markdown
# 词汇分层维度（Vocabulary Dimension）

## 解决什么教学问题
语言类教材的词汇量怎么分层管理——哪些必背、哪些识别、哪些复用——避免生词堆砌或词汇量不足。

## 什么时候用 / 什么时候不用
- 用：英语/外语/语文教材（任何需要词汇管理的语言学习）
- 不用：非语言类（理科/认证/编程）——用 deterministic-anchor 管术语即可
- 典型搭配：scenario-hook（词汇在情境里展示）、socratic-questioning（引导词汇用法）

## 长什么样（结构示例）

词汇表按四层标注：
| 单词 | 音标 | 词性 | 中文 | 分层 | 例句 |
|---|---|---|---|---|---|
| celebrate | /ˈselɪbreɪt/ | v. | 庆祝 | L2 | We celebrate Spring Festival. |

- **L1 课前已知**：单元假设学生已会（如家庭成员称呼），不专门讲
- **L2 本单元核心**：必须四会（会读/会写/会用/懂意思），配场景和例句
- **L3 复用拓展**：在弹药库出现，后续单元复用，本单元不要求全掌握
- **L4 识别即可**：见到能猜意思就行，不背

三动作：展示（情境里首次出现）→ 复用（练习/对话中用）→ 测试（听写/造句）。

## 已知陷阱
- ❌ 所有词都标 L2 → 词汇量爆炸学生负担重
- ❌ L3/L4 当 L2 考 → 预期错误学生受挫
- ❌ 词汇表只有中文没有例句 → 不会用

## 变体
- **blueprint 路线**：弹药库板块里用表格；音标用英式 RP（/ / 标注）
- **human-readable 路线**：词汇融入叙事，章末附词汇表

## 不要这样用
- ❌ 非语言类用这个卡——术语用 precise-definition + deterministic-anchor 管
```

- [ ] **Step 3: 提交**

```bash
cd F:/code/craft-your-textbook
git add skills/craft-your-textbook/references/patterns/language-learning/
git commit -m "feat: 写 vocabulary-dimension 模式卡"
```

---

## Task 13: 重写 SKILL.md 为元方法引导器

**Files:**
- Modify: `SKILL.md`（全量重写，目标 200 行以内）

- [ ] **Step 1: 写新 SKILL.md**

```markdown
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
```

- [ ] **Step 2: 验证 SKILL.md 行数**

Run: `wc -l F:/code/craft-your-textbook/skills/craft-your-textbook/SKILL.md`
Expected: 200 行以内。

- [ ] **Step 3: 提交**

```bash
cd F:/code/craft-your-textbook
git add skills/craft-your-textbook/SKILL.md
git commit -m "feat: 重写 SKILL.md 为元方法引导器"
```

---

## Task 14: 更新 audit-and-testing.md

**Files:**
- Modify: `references/audit-and-testing.md`

需要修改三处：①幻觉 gate 对齐 I2（拓宽到偏好/首选断言）②加金标准门槛清单 ③加 sub-agent prompt 必带要素。

- [ ] **Step 1: 修改 §6.4 防幻觉铁律对齐 I2**

把第一条"打赌测试"拓宽覆盖偏好/首选断言；把第四条"判断类内容必标出处"从单条升级为和定义类并列：

找到第 102-107 行的"完整 4 条"部分，改为：

```markdown
### 6.4 防幻觉铁律（对齐不变量 I2）

以下 4 条取代上方的简短幻觉 gate 备注，写进 META.md / 写作规范，每个 writing agent 必读：

1. **打赌测试**：每写一条具名引用 / 数字 / 定义 / 公式 / 分类名称 / 偏好判断（"PMI 首选 X""应当 Y"）前，问自己"愿不愿打赌这是真的？"有一丝犹豫就回源材料索引核对到源文件+行号，或回已声明的判断根（原则/模型/准则条款）。
2. **追不到源就降级**：核对不到的，降级为间接转述（"通常认为…"）或干脆不写。**绝不杜撰**准则定义、过程编号、公式、偏好断言。
3. **最危险条目逐字回源**：考试/技能/条款类教材的公式、框架名称、分类名称最危险——写前必须回材料逐字核对，凭记忆写大概率出错。
4. **偏好断言必标判断根**（对齐 I2）：当书里有"在 X 情境下首选 Y""应当 Z"这类判断，每条必须标注判断依据出处（回哪条原则/绩效域/准则条款）。标不出依据的偏好断言宁可不写。PMP 的"PMI 会怎么选"why-not+判断依据就是标准做法。

Mode A（无源）替代机制：每个断言必须通过 L5 路径 B/C 的学员验证，强制不接受路径 A 自测。

> 审计是终检，**写作时的自我 gate 才是主战场。**
```

- [ ] **Step 2: 在文件末尾加"金标准门槛清单"和"sub-agent prompt 必带要素"两节**

追加：

```markdown

## 七、金标准门槛清单（Phase 4 判据）

金标准章必须同时满足以下门槛才"通过"，否则回炉：

1. **板块语法一致**：严格遵守 style-spec 定义的章内板块语法，无遗漏必含板块、无约定外板块
2. **源回溯干净**：随机抽 10 条定义/公式/判断，全部能回源或回判断根（L3 引文抽检）
3. **事实/判断分离**（如选了 fact-vs-judgment 卡）：确定性知识清单里不混入判断类断言
4. **why-not 无附加条件杜撰**（如选了 judgment-card 卡）：候选项排除只靠权威原文明确说过的适用条件
5. **L5 教学测试通过**：20-30 轮对话 AI 老师不卡住、不编造、能带学生抵达锚点

前 4 条是静态门槛，第 5 条是实测门槛。

## 八、sub-agent prompt 必带要素

Phase 5 并行铺章时，每个 writing sub-agent 的 prompt 必带：

1. 金标准章全文（作为范例）
2. META.md + OUTLINE.md + style-spec.md + 源材料索引.md（四个文件全文）
3. 本章的具体源材料映射（源材料索引里本章的那一节，精确到行号）
4. 防幻觉铁律完整 4 条（上面 §6.4）
5. 不变量底线（I1-I9/H1-H3，提示从 invariants.md 读哪几条适用）
6. 本章在知识链中的位置和跨章引用指向
```

- [ ] **Step 3: 提交**

```bash
cd F:/code/craft-your-textbook
git add skills/craft-your-textbook/references/audit-and-testing.md
git commit -m "feat: audit-and-testing 对齐 I2、加金标准门槛和 prompt 要素"
```

---

## Task 15: 更新 delivery-checklist.md（质量门通用化）

**Files:**
- Modify: `references/delivery-checklist.md`

核心改动：删除硬编码的"7 板块 emoji 计数""Unit 标题格式"检查，改为从四文件契约派生。

- [ ] **Step 1: 重写 Phase 9 质量门表格**

找到第 96-103 行的"6 项质量门"表格，替换为：

```markdown
| 检查项 | 方法 | 判据 |
|---|---|---|
| ① 必含板块完整 | 按 style-spec §章内板块语法定义的必含板块 grep 计数 | = 章数 × 每章必含板块数（从 style-spec 读，不是硬编码 7 板块） |
| ② 禁用词 | 从 style-spec §正文语言风格 读本书特有禁用词表，grep BOOK.md | = 0（"AI 老师"等合法词人工放行） |
| ③ 元数据残余 | grep META 声明的脚手架标题列表 | = 0 |
| ④ 章数 | 从 OUTLINE §逐章骨架 读预期章数，grep 章标题（格式从 style-spec 读，不是硬编码 `^# Unit`） | = 预期章数 |
| ⑤ 跨章引用 | 逐章检查行内回溯/连接表/交叉引用指向的章/概念真实存在（Phase 5.3 已做，此步抽查） | 无空指 |
| ⑥ 文件大小 | 合并后字节数 | 首本书记录 baseline，重跑时 ±10% |

判据②③④的具体值从四文件派生：
- 必含板块清单：读 style-spec §章内板块语法
- 禁用词表：读 style-spec §正文语言风格
- 脚手架标题：读 META #10 脚手架标题列表
- 章标题格式：读 style-spec §章标题格式
- 预期章数：读 OUTLINE §逐章骨架
```

- [ ] **Step 2: 重写 Phase 7 终检表格里的"板块齐全"行**

找到第 29 行：
```
| 板块齐全 | 每个单元 6 个二级板块（`## 🎬🧭📌🎯🔗📐`）+ 1 个嵌在 📌 下的三级板块（`### 💬`），合称 7 板块，都在 | 齐全 |
```

替换为：
```
| 板块齐全 | 每个章都包含 style-spec §章内板块语法定义的必含板块（不是硬编码 7 板块，按本书设计核对） | 齐全 |
```

- [ ] **Step 3: 更新 Phase 7/8 里硬编码路径**

把所有 `volume-1-units/` 改为 `chapters/`；更新 strip_meta_sections.py 调用命令：

```bash
python scripts/strip_meta_sections.py chapters/ appendix/
```

（新脚本接受多个目录）

- [ ] **Step 4: 提交**

```bash
cd F:/code/craft-your-textbook
git add skills/craft-your-textbook/references/delivery-checklist.md
git commit -m "feat: delivery-checklist 质量门通用化——从四文件契约派生"
```

---

## Task 16: 更新 anti-patterns.md

**Files:**
- Modify: `references/anti-patterns.md`

加"诚实边界声明"反模式，并把旧的 7 板块/Unit 相关措辞更新为 v7 通用表述。

- [ ] **Step 1: 加诚实边界声明反模式**

在"拆脚手架级"后面加一个新分类：

```markdown
## 诚实边界级
- ❌ 不诚实声明本书能力边界（如"本题库足够通过考试"但题量明显不够；"读完就能掌握"但内容明显不足）
- ❌ 假装速判脚本/练习能替代题库（PMP 60-90 题建不了真反射，要诚实说"示范思路，刷题量靠题库接力"）
```

- [ ] **Step 2: 更新旧措辞（替换硬编码模板引用）**

- "把蓝本当'给读者读的书'来写"保留（跨路线适用）
- 把"只列模块标题不写'含义三问'"改为"Phase 3 不充分分析源和目标就开写"
- 其他保持不变

- [ ] **Step 3: 提交**

```bash
cd F:/code/craft-your-textbook
git add skills/craft-your-textbook/references/anti-patterns.md
git commit -m "feat: anti-patterns 加诚实边界声明，更新措辞"
```

---

## Task 17: 通用化 merge_book.py

**Files:**
- Modify: `scripts/merge_book.py`

改动要点：
1. 读 META.md 顶部 YAML 的 `format` 字段（PyYAML 或简单正则解析）
2. 章文件发现：扫描 `chapters/`（含子目录）递归找 `*.md`，按文件名字典序排序
3. 附录扫描 `appendix/`
4. human-readable 路线注入 loader 指令（从 OUTLINE.md §loader 读，或用默认模板）
5. blueprint 路线支持 `--strip-frontmatter` 参数
6. 删除硬编码的英语书 UNIT_FILES/APPENDIX_FILES/STARTER_FILE/HEADER

- [ ] **Step 1: 重写 merge_book.py**

```python
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
```

- [ ] **Step 2: 测试脚本基本功能（dry run）**

```bash
cd F:/code/craft-your-textbook/skills/craft-your-textbook/scripts
python merge_book.py 2>&1 | head -5
```
Expected: 脚本能运行（无 chapters/ 目录时空输出不报错）。

- [ ] **Step 3: 提交**

```bash
cd F:/code/craft-your-textbook
git add skills/craft-your-textbook/scripts/merge_book.py
git commit -m "feat: merge_book.py 通用化——读 META format、扫描 chapters/、注入 loader"
```

---

## Task 18: 通用化 strip_meta_sections.py

**Files:**
- Modify: `scripts/strip_meta_sections.py`

改动要点：
1. 脚手架标题从 META.md 读（META #10 列表），不是硬编码
2. 支持多个目录参数（chapters/ + appendix/）
3. 递归扫描子目录
4. 删除每个文件从"脚手架标题行"到文件末尾的全部内容

- [ ] **Step 1: 重写 strip_meta_sections.py**

```python
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
                print(f"[ok]   {f.relative_to(base_dir)}: 删除 {removed:,} 字符")
                total_removed += removed
                files_changed += 1
            else:
                print(f"[skip] {f.relative_to(base_dir)}: 未找到脚手架标题")

    print("-" * 60)
    print(f"完成：{files_changed} 个文件，共删除 {total_removed:,} 字符")
    print("★ 记得重跑 merge_book.py 重新合并 BOOK.md")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 测试脚本**

```bash
cd F:/code/craft-your-textbook/skills/craft-your-textbook/scripts
python strip_meta_sections.py 2>&1 | head -5
```
Expected: 运行无错（无 chapters/ 目录时 skip）。

- [ ] **Step 3: 提交**

```bash
cd F:/code/craft-your-textbook
git add skills/craft-your-textbook/scripts/strip_meta_sections.py
git commit -m "feat: strip_meta_sections.py 通用化——从 META 读脚手架标题、支持多目录"
```

---

## Task 19: 更新 01_pdf_to_md.py 注释路径

**Files:**
- Modify: `scripts/01_pdf_to_md.py`

只更新注释/用法里的示例路径（`source-md/` → `sources-md/`；删除"师生合版输出到 source-md-teacher"），脚本逻辑不变。

- [ ] **Step 1: 修改注释和用法行**

找到第 21 行 `# 例：python 01_pdf_to_md.py "教材.pdf" source-md/`，改为：
```python
# 例：python 01_pdf_to_md.py "教材.pdf" sources-md/
```

找到第 22 行 `# 师生合版：教师用书再跑一次，输出到 source-md-teacher/`，删除该行（教师用书也是 sources-md/，靠角色标签区分）。

- [ ] **Step 2: 提交**

```bash
cd F:/code/craft-your-textbook
git add skills/craft-your-textbook/scripts/01_pdf_to_md.py
git commit -m "docs: 01_pdf_to_md.py 注释路径更新"
```

---

## Task 20: 更新 README.md

**Files:**
- Modify: `README.md`（根目录）

README 反映 v7 变化，但不需要全量重写——核心定位不变，更新以下部分：
1. 描述里加"两种路线选择"
2. 安装/使用节提到新模式（Phase 3 自己设计、不套模板）
3. 目录结构节更新

**注**：此 Task 可以最后做，因为 README 不阻塞 skill 功能。如果时间紧张，可以只更新最必要的段落。

- [ ] **Step 1: 更新 README 关键段落**

README.md 核心不变（项目定位、三方分工、师生合版默认——这些仍成立），但要：
- 第六节"怎么用"：更新为两条路线决策 + Phase 1-6 流程（不再提 0/0.5/0.75 小数编号）
- 第七节"目录结构"：更新为新文件结构（patterns/ 目录、不变量、四文件契约等）

- [ ] **Step 2: 提交**

```bash
cd F:/code/craft-your-textbook
git add README.md skills/craft-your-textbook/README.md
git commit -m "docs: README 更新到 v7"
```

---

## Task 21: 最终验证

- [ ] **Step 1: 检查文件完整性**

```bash
cd F:/code/craft-your-textbook/skills/craft-your-textbook
echo "=== 新文件存在检查 ==="
for f in references/invariants.md references/file-contracts.md references/two-routes.md \
         references/source-material.md references/chapter-grammar-starter.md \
         references/patterns/README.md \
         references/patterns/concept-anchoring/precise-definition.md \
         references/patterns/concept-anchoring/misconception.md \
         references/patterns/concept-anchoring/socratic-questioning.md \
         references/patterns/concept-anchoring/fact-vs-judgment.md \
         references/patterns/assessment/judgment-card.md \
         references/patterns/assessment/quick-judgment.md \
         references/patterns/assessment/application-problem.md \
         references/patterns/assessment/worked-example.md \
         references/patterns/assessment/practice-gradient.md \
         references/patterns/assessment/deterministic-anchor.md \
         references/patterns/narrative/scenario-hook.md \
         references/patterns/narrative/running-case.md \
         references/patterns/narrative/character-protagonist.md \
         references/patterns/structure/foundation-chapter.md \
         references/patterns/structure/capstone-chapter.md \
         references/patterns/structure/cross-ref-trace.md \
         references/patterns/structure/appendix-compilation.md \
         references/patterns/structure/multi-source-arbitration.md \
         references/patterns/structure/recurring-leitmotif.md \
         references/patterns/language-learning/vocabulary-dimension.md; do
  [ -f "$f" ] && echo "✓ $f" || echo "✗ MISSING: $f"
done
echo ""
echo "=== 旧文件删除检查 ==="
for f in references/unit-template.md references/outline-and-analysis.md references/vocabulary-strategy.md; do
  [ -f "$f" ] && echo "✗ NOT DELETED: $f" || echo "✓ deleted: $f"
done
```

Expected: 26 个新文件全 ✓，3 个旧文件全 deleted。

- [ ] **Step 2: 模式卡总数验证**

```bash
find references/patterns -name "*.md" | wc -l
```
Expected: 21（README.md + 20 张卡）。

- [ ] **Step 3: SKILL.md 行数验证**

```bash
wc -l SKILL.md
```
Expected: ≤200 行。

- [ ] **Step 4: 脚本语法检查**

```bash
python -m py_compile scripts/01_pdf_to_md.py && echo "01 OK"
python -m py_compile scripts/merge_book.py && echo "merge OK"
python -m py_compile scripts/strip_meta_sections.py && echo "strip OK"
```
Expected: 三个都 OK。

- [ ] **Step 5: 最终 commit**

```bash
cd F:/code/craft-your-textbook
git add -A
git status  # review
git commit -m "feat: v7 重构完成——元方法+模式库+四文件契约"
```

---

## Self-Review Checklist

- [x] Spec §一核心决策（三层结构/两条路线/两层设计）→ Task 1-7 覆盖（目录+invariants+contracts+source-material+two-routes+patterns-README+starter）
- [x] Spec §二不变量清单 → Task 2 invariants.md
- [x] Spec §三模式库 20 张卡 → Task 8-12
- [x] Spec §四 Phase 1-6 流程 → Task 13 SKILL.md
- [x] Spec §五 Phase 3 五步 → Task 13 SKILL.md
- [x] Spec §六四文件契约 → Task 3 file-contracts.md
- [x] Spec §七两路线差异 → Task 5 two-routes.md + Task 17 merge_book.py loader
- [x] Spec §八脚本通用化 → Task 17-19
- [x] Spec §九目录结构 → Task 1 目录骨架
- [x] Spec §十 SKILL.md/reference 处置 → Task 13-16
- [x] Spec §十一 v6→v7 关系（旧文件删除）→ Task 1
- [x] Global constraints 全部满足：中文写作、模式卡六节格式、示例模板范式、独立 commit