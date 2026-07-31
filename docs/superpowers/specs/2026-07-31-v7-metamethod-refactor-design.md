# craft-your-textbook v7 重构设计：元方法 + 模式库 + 四文件契约

> 日期：2026-07-31
> 状态：待用户审阅
> 前置：REFACTOR-PLAN-v6.md（v6 定稿），但 v7 不是 v6 的小修——是核心抽象范式的转换。
> 驱动样本：PMP 认证蓝本（`f:/code/po-juan-xie-shu/PMP/textbook/`）、CPA 审计教材（`f:/code/po-juan-xie-shu/socratopia-cpa-audit-zh/`）、英语七上教材（现有 skill 默认形态）。

---

## 〇、为什么要做 v7：v6 的根本问题

v6 把书的形状"参数化"了——domain 六值枚举 + features 七开关 + 主轴 pure-blueprint/dual-readable + 四类章节类型。看起来通用，但 PMP 实战暴露了根本问题：**这些参数是从样本归纳出来的分类学，不是从核心洞察推导的方法论**。

具体说：

1. **7 板块单元模板是英语教材的偶然形状**，被当成通用硬模板（🎬🧭📌💬🎯🔗📐）。PMP 的章节结构（Definition 双讲 + Misconception + 首选卡 + 硬记锚 + 双脚本）和它完全不同形，塞不进去。
2. **features 开关是"填槽"思维**——Agent 拿到一本书后对号入座开开关，而不是自己分析"这本书面对什么教学问题、需要什么板块"。
3. **domain 枚举预设了"书有几种类型"**，但 PMP（认证类，13 份异构源，三套知识体系双层锚定）和 CPA（叙事教材，贯穿主角）的差异比"domain=certification"一个标签能表达的大得多。
4. **v6 的 dual-readable 定义模糊**——写一份蓝本再生成导读版？还是直接写人可读的书？PMP/CPA 实战证明后者才是真实需求。

**v7 的核心转向：skill 不再预设"书长什么样"，而是提供一套元方法，引导 Agent 自己为每本书设计它的形状。**

---

## 一、核心设计决策

### 1.1 三层结构

| 层 | 作用 | 文件载体 |
|---|---|---|
| **不变量**（invariants） | 从"AI 老师读书教学"核心洞察推出来的底线，任何书都必须满足 | `references/invariants.md` |
| **参考模式库**（patterns） | 解决特定教学问题的可组合板块，按"教学问题"分类，不按学科 | `references/patterns/` 目录，每模式一卡 |
| **四文件契约**（contracts） | 强制 Agent 必须回答哪些设计问题，但不预设答案 | `references/file-contracts.md`（必答问题清单），产出为 META/OUTLINE/style-spec/源材料索引 |

### 1.2 两条互斥路线

触发 skill 后第一个决策点，不设默认（但优先推荐 pure-blueprint）：

- **pure-blueprint**：给 AI 苏格拉底老师读的教学蓝本。结构化、可含元指令块/yaml frontmatter/技术回溯。AI 教学精度最高。
- **human-readable**：给人读的流畅教材（CPA/PMP 形态）。正文 prose 化，章末有结构化教学区；AI 直接读它也能教，但约束更少。

不存在"一份源内容渲染两份输出"——选定路线后就按该路线的约束设计和写作，是两种不同的产物。

### 1.3 设计分两层，都由 Agent 在 Phase 3 自己设计

- **章内板块语法**：每章由哪些板块组成、顺序如何、循环单元是什么、哪些板块可选。落到 `style-spec.md`。
- **整书教学架构**：分卷、知识链主线、特殊功能章、跨章引用机制、附录汇编、AI 老师使用方式。落到 `OUTLINE.md` + `META.md`。

### 1.4 保留的工程铁律（从 v1→v6 实战验证）

- Phase 0→9 → 合并为 6 阶段（见 §四）但节奏不变
- 金标准先行（写一章审到满意再铺开）
- 多轮审校（5-7 轮是常态）
- 四文件配置（META/OUTLINE/style-spec/源材料索引）
- 源材料索引两层化（源级探查 → 章级映射回填）
- 交付前拆脚手架 + 质量门
- 防螺旋铁律（定稿后不允许加章/附录/机制级板块，除非回炉 Phase 3）

---

## 二、不变量清单

分两节：**内容不变量**（产出形态必须满足）和**过程不变量**（写作过程必须遵守）。

### 2.1 内容不变量

#### 跨路线硬约束（两条路线都必须满足）

**I1. 读者意识**
写每个板块前必须能回答"AI 老师上课时会怎么用这块？"（两条路线都要）。human-readable 额外回答"人读到这里会怎么理解？"——防止 prose 只考虑 AI 可读、人读着像规格书。

**I2. 断言可追溯**
任何权威断言——包括正式定义/公式/数字/分类名称，**和**偏好/首选/"应当"类判断——都必须能追溯到依据。
- 定义/公式/数字类：回源文件+行号
- 偏好/首选/判断类：回已声明的判断根（原则/模型/准则条款）
标不出依据的偏好断言，宁可不写。
Mode A（无源）下替代机制：每个断言必须能通过 L5 教学测试的学员验证，强制 L5 路径 B/C，不接受路径 A 自测。

**I5. 具体情境素材**
必须为教学提供含具体实体（公司/角色/数字/约束）的情境或案例。不接受"某项目遇到 X"式空泛描述。

**I6. 跨章引用**
整本书必须有前后章知识回扣机制（行内回溯/连接表/主题低音线——具体形式由 Agent 设计，不预设）。

#### pure-blueprint 路线硬约束

**I3. 非对话体**
不写死"老师说…学生答…"的对话脚本——写死了 AI 会照抄，教学就死。

**I4. 显式提问路线图**
必须为 AI 老师提供结构化提问方向/问题链（💬三类问题/双脚本/探索脚本等形式不限），不能只有知识点没有教学指引。

#### human-readable 路线硬约束

**H1. 正文叙事 prose 化**
正文是流畅叙事，不内嵌"给 AI 老师"的元指令、技术回溯标注、yaml frontmatter。

**H2. 章末结构化教学区**
每章章末必须有结构化教学素材区（练习/讨论题/探索问题/教学脚本——形态由 Agent 按教学目标设计）。这是 human-readable 路线下 AI 老师的提问路线图（等价于 blueprint 的 I4）。

**H3. BOOK.md 顶部 loader 指令**
合并时在 BOOK.md 顶部注入 loader 指令，告诉 AI 老师："正文 prose 是素材库，用你自己的话重组教学；章末教学区照问题链走。"

### 2.2 过程不变量

**I7. 金标准先行**
全量铺写前必须先写一章金标准，按 `audit-and-testing.md §金标准门槛` 通过后，回填 `style-spec §金标准写作惯例`，再铺开。

**I8. 交付前拆脚手架**
过程元数据（自检清单/版本记录/写作惯例注释等）交付前必须拆干净。脚手架标题列表由 META 声明（每本书可能不同），不硬编码。

---

## 三、参考模式库

### 3.1 目录结构

```
references/patterns/
├── README.md                           # 索引+怎么用+分层说明+三书选型示例+预装配包
├── concept-anchoring/                  # 章内板块层：概念锚定
│   ├── precise-definition.md           # 精确呈现（术语/公式/分类/硬数字+直觉解释，含双讲）
│   ├── misconception.md                # 误区/常见错误桩
│   ├── socratic-questioning.md         # 苏格拉底提问路线图（💬三类问题等）
│   └── fact-vs-judgment.md             # 确定性知识 vs 判断分离（PMP"硬记锚vs首选卡"）
├── assessment/                         # 章内板块层：评估/练习
│   ├── judgment-card.md                # 判断题/首选卡（首选+why-not+判断依据）
│   ├── quick-judgment.md               # 速判/限时选择题（教反射）
│   ├── application-problem.md          # 长情境多步推理题
│   ├── worked-example.md               # 例题演练（编程/数学/审计程序设计）
│   ├── practice-gradient.md            # 练习三级梯度（recall→transfer→open reasoning）
│   └── deterministic-anchor.md         # 必背锚/确定知识清单
├── narrative/                          # 章内板块层：叙事结构
│   ├── scenario-hook.md                # 情境钩子开章
│   ├── running-case.md                 # 贯穿案例语料库
│   └── character-protagonist.md        # 主角/第二人称戏剧化
├── structure/                          # 整书架构层（设计 OUTLINE 时先翻这组）
│   ├── foundation-chapter.md           # 地基章（为其他章供给判断根/前提知识）
│   ├── capstone-chapter.md             # 总结/收网章
│   ├── cross-ref-trace.md              # 行内回溯引用机制
│   ├── appendix-compilation.md         # 附录从章末板块自动汇编
│   ├── multi-source-arbitration.md     # 多源冲突裁决+双层锚定
│   └── recurring-leitmotif.md          # 贯穿性主题低音线（如 PMP 价值交付、CPA 职业怀疑）
└── language-learning/                  # 领域特化层
    └── vocabulary-dimension.md         # L1-L4 词汇分层
```

### 3.2 模式卡统一格式

每张卡固定六节：

```markdown
# 模式名

## 解决什么教学问题
一句话说清。

## 什么时候用 / 什么时候不用
- 用：本书有 [某特征] 时
- 不用：[条件] 时用它是过度设计
- 典型搭配：常和 [X卡]、[Y卡] 组合；和 [Z卡] 互斥

## 长什么样（结构示例）
最小示例片段（5-15 行）+ 至少一个真实样本出处（"见 PMP Ch4 §4.1"）。

## 已知陷阱
来自金标准踩过的坑，不是凭空想的。

## 变体
- 变体 A：human-readable vs blueprint 差异
- 变体 B：某类书里的演化形态

## 不要这样用
❌ 常见误用 + 为什么错。
```

### 3.3 模式库 README 核心内容

1. **什么时候读我**：Phase 3.3 模式选型时全读；Phase 4/5 写章时按 style-spec 重读具体卡。
2. **卡的分层说明**：structure/ 是整书架构层（Phase 3.4 用），其他目录是章内板块层（Phase 3.3 用），language-learning/ 是领域特化层。
3. **模式选型流程三步**：
   - 带 Phase 3.1 识别的教学问题翻卡
   - 回答两个强制问题（见 §3.4）
   - 或从预装配包出发再定制
4. **参考架构起点（预装配包）**：

| 起点 | 预打包模式 | 适合场景 |
|---|---|---|
| 认证应试蓝本 | precise-definition + misconception + judgment-card + quick-judgment + fact-vs-judgment + deterministic-anchor + practice-gradient + multi-source-arbitration + foundation-chapter + capstone-chapter + cross-ref-trace + appendix-compilation + scenario-hook + running-case（可选 character-protagonist） | PMP/CPA/法考/医师资格 |
| 叙事入门教材 | precise-definition + misconception + socratic-questioning + application-problem + worked-example + scenario-hook + character-protagonist + running-case + recurring-leitmotif | 通俗科普/入门教材 |
| AI 教学蓝本（K-12/技能） | socratic-questioning + precise-definition + worked-example + scenario-hook + vocabulary-dimension（语言类）+ cross-ref-trace | 英语教材/编程入门/数学 |

5. **已完成书的选型示例**（PMP 选了哪些、拒绝了哪些、为什么；CPA 选了哪些；英语选了哪些）——让 Agent 有具体参照。
6. **全部卡索引**：按"教学问题"分组列表。

### 3.4 防走过场机制

Agent 在 Phase 3.3 必须在 `style-spec §模式选型说明` 里显式回答两个强制问题：

1. 我考虑过哪些模式、拒绝了哪些、为什么拒绝？
2. 所选每个模式对应本书哪个具体教学问题？

**强制要求拒绝理由**——这迫使 Agent 真读真想，而不是"挑几张眼熟的"。

审计时核对：声称用了某模式（如 judgment-card）但 style-spec 板块语法里没有对应板块 = 失败。

---

## 四、Phase 流程（6 阶段）

旧版 Phase 0/0.5/0.75/1-9 的小数编号是历史补丁累积，v7 合并为 6 个粗粒度阶段。

| 阶段 | 名称 | 做什么 | 产出 |
|---|---|---|---|
| **Phase 1** | 源材料准备 | PDF→MD（MinerU API）+ 脚本复制进项目 + 依赖安装。已有 MD 则跳过转换。 | `sources-md/` 源 MD；`scripts/` 脚本副本 |
| **Phase 2** | 源探查 | **所有有源书必走**（不再分单源/多源路线，深度按源数量自度）：摸源结构、登记角色标签、建简码表、定权威层级、做真相校准。 | `源材料索引.md` 第一层（源级探查表） |
| **Phase 3** | 教学设计 | 五步拆解 + 三个用户确认关卡（见 §五） | META.md、OUTLINE.md、style-spec.md、`源材料索引.md` 第二层（章级映射回填） |
| **Phase 4** | 金标准验证 | 选一章（强推导链、体感峰值）按 style-spec 板块语法写 → 五层审计 + L5 教学测试 → 通过后回填 style-spec §金标准写作惯例 | 金标准章 md |
| **Phase 5** | 全量写作 + 收网 | 5.1 sub-agent 并行铺其余章（prompt 必带金标准+四文件+幻觉gate+板块语法约束）→ 5.2 附录汇编（按 OUTLINE §附录汇编策略）→ 5.3 跨章审计（含板块语法一致性审计）→ 5.4 合并 BOOK.md（human-readable 注入 loader 指令） | chapters/、appendix/、BOOK.md |
| **Phase 6** | 终检与交付 | 终检（禁用词/乱码/板块计数从 style-spec 派生/引用）→ 拆脚手架（脚手架标题从 META 读）→ 质量门（从四文件契约派生检查项）→ 交付 | 纯净 BOOK.md |

**Mode A（无源从零造）差异**：
- Phase 2 跳过；Phase 3 的源分析改为知识密度自评
- 幻觉 gate 更严：I2 替代机制（断言经 L5 学员验证），强制 L5 路径 B/C
- 首要风险是幻觉，仅适合 AI 知识密度高的领域

---

## 五、Phase 3 教学设计五步

这是 v7 元方法的核心。Agent 围绕四文件契约的"必答问题"组织设计工作，三个用户确认关卡防止"设计完了才发现方向错了"。

### Phase 3.1：分析源材料 + 推导教学目标

Agent 独立分析（此步不读模式库，避免先入为主），回答三个问题，在对话里呈现给用户：

**Q1. 源材料形态是什么？**
- 有源/无源？几份源？源之间权威层级？
- 源的天然组织逻辑（按章节/任务/主题/时间线）？

**Q2. 这本书要让学习者最终能做到什么？**（教学目标）
- 通过考试（判断力+反射速度+考纲覆盖）
- 理解领域概念（建立心智模型+能推理）
- 掌握技能（能动手做+能 debug）
- 通读建体系（全景理解+能复述）
- 这个目标决定所有下游设计

**Q3. 学习过程中学习者最大的坑是什么？**（教学问题识别）
- 术语混淆？判断题陷阱？公式记错？不会推理？迁移失败？
- 这是模式选型的输入

用户确认关卡 ①：教学目标和教学问题识别是否准确。

### Phase 3.2：两条路线决策

Agent 呈现决策点给用户：
> "这本书是喂给 AI 苏格拉底老师教学用的教学蓝本（推荐——AI 教学精度最高），还是一本给人读的流畅教材（AI 也能直接拿它教，但教学约束更少）？"

决策写入 META 开头：`format: pure-blueprint | human-readable`。

### Phase 3.3：模式选型 + 板块语法设计

1. 读 `patterns/README.md`，理解分层和选型流程
2. 带 Phase 3.1 的"教学问题"翻模式卡
3. 回答两个强制问题（拒绝了哪些+为什么 / 所选每个模式对应什么问题），写入 `style-spec §模式选型说明`
4. 可选：从预装配包出发再定制（要说明为什么起点适合/不适合）
5. 设计章内板块语法（必含板块/循环单元/可选板块/叙事约定/章末教学区形态）
6. 产出落到 style-spec 主体

用户确认关卡 ②：模式选型和板块语法是否合理。

### Phase 3.4：整书教学架构设计

产出 OUTLINE.md 主体，回答 file-contracts.md 里 OUTLINE 的必答问题（见 §六）：
- 知识链主线、卷/部划分、逐章骨架
- 特殊功能章、跨章引用机制、附录汇编策略
- 贯穿案例/主角约定（如选了 narrative 卡）
- AI 老师使用方式（顺序讲/地基章先吃透/按需检索）
- BOOK.md loader 指令内容（human-readable 路线）

Phase 2 的源材料索引在此步回填第二层（章级映射）。

用户确认关卡 ③：全书架构和逐章骨架。

### Phase 3.5：META + 源材料索引完稿

完成 META.md（写作铁律、frontmatter schema 或声明无、排除项、字数/并行度约定、防螺旋规则、脚手架标题列表），源材料索引全完稿。

Phase 3 完成标志：META/OUTLINE/style-spec/源材料索引四文件齐备，三个确认关卡全绿。

---

## 六、四文件契约必答问题清单

每个文件的必答问题在 `references/file-contracts.md` 里完整列出。Agent 产出文件时必须全部回答，格式/措辞/长度由 Agent 按书自定。契约强制"必须回答什么"，不预设"答案是什么"。

### META.md 必答问题

1. 本书定位（一句话+format 声明）
2. 防幻觉铁律（最危险断言类型+回源到哪+追不到怎么降级）
3. 读者意识声明（第一读者是谁+写每块前问什么）
4. 章内板块语法（从 Phase 3.3 搬过来）
5. 章末教学区规范
6. 写作纪律（agent 分配/并行度/字数参考/排除项）
7. frontmatter schema（需要则定义字段+校验规则；不需要则显式声明"本书无 frontmatter"）
8. AI 老师使用方式
9. 防螺旋铁律
10. 脚手架标题列表（Phase 6 拆脚手架用）

### OUTLINE.md 必答问题

1. 知识链主线（一句话）
2. 卷/部划分
3. 逐章骨架表（章号/标题/类型/位置/锚定源任务或概念）
4. 特殊功能章（如有，说明为什么不能并入正常章）
5. 跨章引用机制（具体形式）
6. 附录汇编策略（从哪些章末板块汇编成哪些附录）
7. 贯穿案例/主角约定（如用了 narrative 卡，含边界声明）
8. BOOK.md loader 指令内容（human-readable）

### style-spec.md 必答问题

1. 模式选型说明（两个强制问题回答）
2. 章内板块语法完整版（必含/循环/可选+每个板块写作要求+长度+人称+位置）
3. 情境钩子写法
4. 正文语言风格（正式程度/术语处理/禁用词——本书特有，不全局硬编码）
5. 量化参考密度（每章小节数/Definition 数/misconception 数/习题数——参考非铁律，金标准后回填实测）
6. 金标准写作惯例区（Phase 4 通过后回填：实测密度/踩过的坑/确认不套用的视角）

### 源材料索引.md 必答问题（有源场景）

1. 源文件简码表（简码/路径/定位/权威层级）
2. 全书通用锚点（跨章共享的源定位）
3. 分章源映射（每章：①章→源文件行号映射 ②预抽关键条目 ③高频陷阱/偏好预判 ④写作惯例）
4. 可信度声明（建索引时的实况探查结论）

Mode A 不建此文件，META 里声明知识密度自评+L5 强制路径。

---

## 七、两条路线在 Phase 流程中的落点差异

| 维度 | pure-blueprint | human-readable |
|---|---|---|
| Phase 3.2 决策 | `format: pure-blueprint` | `format: human-readable` |
| 不变量约束 | I1/I2/I3/I4/I5/I6 | I1/I2/H1/H2/H3/I5/I6 |
| 板块语法（Phase 3.3） | 可含显式元指令块/技术回溯/emoji 标题/yaml frontmatter | 正文 prose 化，元指令集中章末教学区 |
| frontmatter | 可选且常用 | 默认无，META 显式声明 |
| Phase 5.4 合并 | 正常合并 | BOOK.md 顶部注入 loader 指令 |
| Phase 6 终检 | 必含板块计数/引导问题齐备 | 章末教学区齐备/正文无元指令残留 |
| 最终产物气质 | 结构化 spec（AI 解析高效，人读像规格书） | 流畅教材（人读像书，AI 直接教） |

两条路线不共享中间产物——Phase 3.2 选定后后续 Phase 各走各的约束路径。

---

## 八、脚本通用化

三个脚本保留，去硬编码：

**01_pdf_to_md.py**：基本不变。token 环境变量、转换参数按书改、理科 ENABLE_FORMULA 提示保留。

**merge_book.py**：
- 删除硬编码的英语书单元清单，改为从项目配置读（META 声明或 `chapters/` 目录排序）
- HEADER 模板通用化
- human-readable 路线：BOOK.md 顶部注入 loader 指令（从 OUTLINE §loader 读）
- blueprint 路线：可选参数剥离 yaml frontmatter

**strip_meta_sections.py**：
- 脚手架标题从硬编码 `## 📋 自检清单`/`## 📜 版本记录` 改为从 META.md 读"脚手架标题列表"
- 支持章文件在任意子目录（不硬编码 `volume-1-units/`）

脚本仍为"复制进项目再改"的示例模板范式。

---

## 九、标准目录结构

```
project-folder/
├── scripts/             # 从 skill 复制的脚本，按书改
├── sources-md/          # 所有源 MD（不再分 source-md/source-md-teacher，靠角色标签区分）
├── chapters/            # 章节 md（命名从 style-spec）
├── appendix/            # 附录 md
├── META.md
├── OUTLINE.md
├── style-spec.md
├── 源材料索引.md         # 有源场景；Mode A 无
├── L5-dialogue.md       # L5 教学测试对话记录（验收后可删）
└── BOOK.md
```

不再预设 `volume-1-units/`、`source-md-teacher/`、`DIFF-STUDENT-TEACHER.md`：
- 分卷是 OUTLINE 设计的事，需要时 chapters/ 下建子目录
- 教师用书差异并入源材料索引（角色标签 `teacher_textbook`）

---

## 十、SKILL.md 新结构

SKILL.md 精简为元方法引导器（目标 200 行以内），所有"怎么做"细节放 references/：

```markdown
# craft-your-textbook

## 这是什么
三方分工（学生/AI老师/书）+ 书对 AI 老师的四个功能 + 核心理念

## 何时用
触发词 + 不适用场景

## 第一步：定路线
pure-blueprint（推荐）vs human-readable——触发后必问

## 全流程导航（6 阶段）
每阶段一句话 + 产出 + 关键约束表格

## 核心：Phase 3 教学设计
五步拆解概览 + 三个确认关卡 + 模式选型强制问题

## 参考文件按需加载
[做什么 → 读哪个 reference] 表格
```

参考文件加载表：

| 场景 | 参考文件 |
|---|---|
| Phase 1 PDF 转换 | scripts/ 说明 |
| Phase 2 源探查 | `references/source-material.md` |
| Phase 3 四文件契约 | `references/file-contracts.md` |
| Phase 3 模式选型 | `references/patterns/README.md` |
| Phase 3 不变量底线 | `references/invariants.md` |
| Phase 3 章节语法起点参考 | `references/chapter-grammar-starter.md` |
| Phase 3 路线差异 | `references/two-routes.md` |
| Phase 4-5 审计 | `references/audit-and-testing.md`（同步更新幻觉 gate：对齐 I2 拓宽的"断言可追溯"范围，覆盖偏好/首选类断言） |
| Phase 6 交付 | `references/delivery-checklist.md` |
| 避坑 | `references/anti-patterns.md` |

### 删除/合并的旧 reference

- `references/unit-template.md`（7 板块硬模板）→ 拆成多个模式卡，原文件删除
- `references/outline-and-analysis.md` → 继任者为 `file-contracts.md`（四文件必答问题）+ `source-material.md`（源处理方法论）
- `references/vocabulary-strategy.md` → 并入 `patterns/language-learning/vocabulary-dimension.md`

### 新增 reference

- `references/invariants.md`：不变量清单（§二）
- `references/file-contracts.md`：四文件必答问题清单（§六）
- `references/patterns/`：完整模式库（§三）
- `references/two-routes.md`：两条路线决策指引+差异详解
- `references/chapter-grammar-starter.md`：极简骨架起点（展示如何从模式卡组合章节语法的最小示例——含"从 3 张卡拼出一个章节结构"的走查，非硬模板）
- `references/source-material.md`：源角色标签+两层索引+防幻觉（从 outline-and-analysis.md 抽出）
- `references/anti-patterns.md`：保留反模式速查，加入"诚实边界声明"反模式（❌ 不诚实声明本书能力边界，如"本题库足够通过考试"但题量明显不够）

---

## 十一、与 v6 的关系

v7 **不**是 v6 的增量修改。核心范式转换：

| v6 | v7 |
|---|---|
| 书有预设形状（domain 枚举 + features 开关 + 章节类型） | Agent 按教学问题自己设计书的形状 |
| 7 板块单元模板是通用硬模板 | 7 板块降级为"AI 教学蓝本（K-12/技能）"预装配包里的模式组合之一 |
| features 是枚举开关 | features 概念消失，改为"模式选型时的注意力引导"（domain=certification 时提示 Agent 优先看 judgment-card 等） |
| 主轴 dual-readable 定义模糊 | 两条互斥路线清晰：pure-blueprint / human-readable |
| Phase 0/0.5/0.75/1-9 小数编号 | 6 阶段连续编号 |
| 差异报告（Phase 0.5）单列 | 教师用书并入源材料索引的角色标签体系 |

v6 REFACTOR-PLAN-v6.md 保留作为历史参考，但 skill 本体按 v7 重写。

---

## 十二、风险与缓解

| 风险 | 缓解 |
|---|---|
| Phase 3 过重，Agent 读不完 16 张模式卡就选型走过场 | 预装配包提供起点；强制拒绝理由问题；三个用户确认关卡；`chapter-grammar-starter.md` 提供组合示例 |
| Agent 设计的板块语法质量不稳定，金标准写完才发现不可教 | Phase 3.3 后用户确认关卡 ② 专门审板块语法；金标准不过不允许铺开（Phase 4 门槛） |
| 新模式卡需要样本支撑，无样本领域（理科/编程/文史）的卡凭想象 | 现有卡都来自 PMP/CPA/英语三个真实样本；无样本领域的卡暂不写死，留成"插件点"——未来有真样本再加卡，不凭想象设计 |
| human-readable 路线 AI 教学质量低于 blueprint | loader 指令（H3）+ 章末教学区（H2）保证 AI 有提问路线图；明确告知用户"blueprint 教学精度更高"作为推荐选项 |
| Agent 可能漏掉关键设计问题（如不建跨章引用） | 不变量 I6 硬约束；file-contracts.md 必答问题清单逐项核对 |
