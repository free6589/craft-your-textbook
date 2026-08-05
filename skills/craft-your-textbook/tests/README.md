# craft-your-textbook skill 测试套件

> 本目录用 superpowers 的 pressure-scenario 方法测试本 skill 的纪律规则。**改 skill 前先跑对应场景，改后 ≥2 复现全绿**（见 `references/skill-maintenance.md`）。

## 场景清单（6 个）

| 场景 | 保护规则 | 规则源 |
|---|---|---|
| `pressure-route` | 定路线不替用户默认 | SKILL.md「第一步：定路线」 |
| `pressure-golden` | 金标准先行 | invariants I7 |
| `pressure-audit` | 审计独立性 | audit-and-testing §6.1 |
| `pressure-spiral` | 防螺旋 | invariants I9 |
| `pressure-scaffold` | 拆脚手架 | invariants I8 |
| `pressure-backfill` | audit-backfill 回填 | audit-and-testing §八 |

## RED-GREEN-REFACTOR 流程

1. **RED（基线）**：带当前 skill 跑场景，违规 = RED，**逐字记翻车理由**。
2. **GREEN**：按翻车点改 skill；**借口表只收实测原话**（编造借口 = 交付物造假）。
3. **REFACTOR**：带改造后 skill 重跑，新翻车点补计数器，直到收敛（封顶 3 轮）。

**全绿判据**（REFACTOR/GREEN 通过）：同场景同模型下 ①选择正确（A）②引用加固条款作为理由 ③承认诱惑但守规则。三条齐备才算过。

> 翻车点目录 + 溯源表在工作产物 `docs/superpowers/reform-trace.md`（随改造创建）。改 skill 的编辑规矩见 `references/skill-maintenance.md`（改造期随 skill 创建，创建前视为计划中）。

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

> RED 基线 6/6 已守：当前 skill 已成功守住全部纪律。供述诱惑逐字记于 `docs/superpowers/reform-trace.md`（借口表原料）。改造定位 = 形式强化 + 防回退。
> REFACTOR 12 跑全绿（6 场景 × 2 复现）：改造后 skill 无回退，且每跑引用新红旗/借口表/铁律作为管住自己的依据——bulletproof 判据三条齐备。
