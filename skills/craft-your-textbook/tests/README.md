# craft-your-textbook skill 测试套件

> 本目录用 superpowers 的 pressure-scenario 方法测试本 skill 的纪律规则。**改 skill 前先跑对应场景，改后 ≥2 复现全绿**（见 `references/skill-maintenance.md`）。

## 场景清单（7 个）

| 场景 | 保护规则 | 规则源 |
|---|---|---|
| `pressure-route` | 定路线不替用户默认 | SKILL.md「第一步：定路线」 |
| `pressure-golden` | 金标准先行 | invariants I7 |
| `pressure-audit` | 审计独立性 | audit-and-testing §6.1 |
| `pressure-spiral` | 防螺旋 | invariants I9 |
| `pressure-scaffold` | 拆脚手架 | invariants I8 |
| `pressure-backfill` | audit-backfill 回填 | audit-and-testing §八 |
| `pressure-depth` | 金标准深度承诺兑现 | audit-and-testing §7 门槛第 6 条 |

## RED-GREEN-REFACTOR 流程

1. **RED（基线）**：带当前 skill 跑场景，违规 = RED，**逐字记翻车理由**。
2. **GREEN**：按翻车点改 skill；**借口表只收实测原话**（编造借口 = 交付物造假）。
3. **REFACTOR**：带改造后 skill 重跑，新翻车点补计数器，直到收敛（封顶 3 轮）。

**全绿判据**（REFACTOR/GREEN 通过）：同场景同模型下 ①选择正确（A）②引用加固条款作为理由 ③承认诱惑但守规则。三条齐备才算过。

> 翻车点目录 + 溯源表在工作产物 `docs/superpowers/reform-trace.md`（随本地维护战役生成，git-ignored；安装本 skill 的用户默认没有此文件）。改 skill 的编辑规矩见 `references/skill-maintenance.md`。

## 运行方法

- 每次跑测用 **fresh subagent**，绝不复用（防污染）。
- **模型钉死**：RED/GREEN/REFACTOR 同一场景同一模型，比较才有效。
- 场景文本**冻结**，不中途改。
- 通过场景 **≥2 次复现**（单次会撒谎）。
- 翻车点目录 + 溯源表在工作产物 `docs/superpowers/reform-trace.md`。

## 战役日志

| 场景 | 场景 hash（sha256 前 8） | 模型 | 日期 | RED 结论 | GREEN/REFACTOR 结论 |
|---|---|---|---|---|---|
| ① route | c6f88f6d | opus | 2026-08-05 | 已守（A） | 全绿 2/2（引红旗①/铁律） |
| ② golden | 46bfe6f4 | opus | 2026-08-05 | 已守（A） | 全绿 2/2（引 I7 红旗/借口表②） |
| ③ audit | fd6911e9 | opus | 2026-08-05 | 已守（A） | 全绿 2/2（引红旗③/§6.1） |
| ④ spiral | 931231a4 | opus | 2026-08-05 | 已守（A） | 全绿 2/2（引红旗④/I9） |
| ⑤ scaffold | 657ceb28 | opus | 2026-08-05 | 已守（A） | 全绿 2/2（引红旗⑤+Gate Function） |
| ⑥ backfill | 6dcc77e1 | opus | 2026-08-05 | 已守（A） | 全绿 2/2（引红旗⑥/§八） |
| ⑦ depth | b1792bd6 | opus | 2026-08-06 | 未成立（行为 3/3 A，隐式纪律链拦截，无显式深度规则） | 全绿 2/2（引 §7 门槛第 6 条「深度承诺兑现」+ §7.0 第 7 项 + depth.md 判定问题 + style-spec 深度承诺 + audit 严重度 P0） |

> RED 基线 7/7：6 场景已守（A）+ 场景⑦ 行为 3/3 守（A，隐式纪律链拦截，但 skill 无任何显式深度规则）——⑦ 的真实缺口（Mode A 深度可达预筛 / Phase 5.3 深度一致性 / 审计严重度下限 / 流水线深度自问）由深度机制改造（depth.md + 契约 + 审计 gate + 模板）补齐。供述诱惑逐字记于 `docs/superpowers/reform-trace.md`（借口表原料）。
> GREEN/REFACTOR 14 跑全绿（场景①-⑥ × 2 + 场景⑦ × 2）：改造后 skill 无回退，场景⑦ 每跑引用深度条款（§7 深度门槛第 6 条 / §7.0 第 7 项 / depth.md 判定问题 / style-spec 深度承诺 / audit 严重度 P0）作为管住自己的依据——bulletproof 判据三条齐备。
