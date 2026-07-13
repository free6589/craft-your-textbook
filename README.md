# craft-your-textbook

> 亲手为自己造一本 **AI 苏格拉底老师能拿去上课的教学蓝本**——把教材（PDF）或某领域知识，加工成给 AI 老师读的教学 spec。学习者不读书，只跟 AI 老师对话；有教师用书时，造出来的书还能**直接针对应试**。适用任何学科。
>
> 这是 [Socratopia（破卷）](https://www.socratopia.app/r/SCR-FEJXMQ) 生态里"造书"环节的方法论沉淀，固化为一个可复用的 [Claude Code](https://claude.com/claude-code) skill。

本仓库既是一个 **Claude Code 插件市场（marketplace）**，也直接包含 skill 本体，三种用法任选。

---

## 安装

### 方式一 · 插件市场（推荐，可一键更新）

在 Claude Code 里：

```
/plugin marketplace add xx-hub/craft-your-textbook
/plugin install craft-your-textbook
```

更新：`/plugin marketplace update craft-your-textbook`；卸载：`/plugin uninstall craft-your-textbook`。

### 方式二 · clone 整个仓库到 skills 目录

```bash
# 用户级（所有项目可用）
git clone https://github.com/xx-hub/craft-your-textbook.git ~/.claude/skills/_cyt-src
ln -s ~/.claude/skills/_cyt-src/skills/craft-your-textbook ~/.claude/skills/craft-your-textbook
```

或直接把 `skills/craft-your-textbook/` 这个文件夹拷进你的 `~/.claude/skills/`（用户级）或 `<项目>/.claude/skills/`（项目级）。

> ⚠️ 关键：最终要让 `SKILL.md` 位于 `.../.claude/skills/craft-your-textbook/SKILL.md`。本仓库里 skill 本体在 `skills/craft-your-textbook/` 子目录下（插件市场结构要求），别把仓库根整个拷进去。

### 方式三 · 下载 zip

下载仓库 zip，解压后把 `skills/craft-your-textbook/` 文件夹放进 `~/.claude/skills/`。

**验证**：在 Claude Code 里说"帮我造一本 XX 教材的教学蓝本"能被识别即成功。

**依赖**：Phase 0 的 PDF→Markdown 用 [MinerU](https://mineru.net) 在线 API，需自备 API Token（见 skill 内 README 第六节）；脚本需要 Python 3 + `requests`。

---

## 仓库结构

```
craft-your-textbook/
├── .claude-plugin/
│   ├── marketplace.json          # 插件市场清单（供 /plugin marketplace add）
│   └── plugin.json               # 插件清单
├── skills/
│   └── craft-your-textbook/      # ★ skill 本体
│       ├── SKILL.md              # 主入口：模式决策 + Phase 0→9 流程
│       ├── README.md             # 完整介绍（理念/7板块/全流程/应试）
│       ├── references/           # 分析源MD·大纲·单元模板·审计·交付·反模式
│       └── scripts/              # MinerU转换 / 合并 / 拆脚手架
├── README.md                     # 本文件
└── LICENSE
```

**skill 详细说明**（Socratopia 理念、教育范式、7 板块模板、造书全流程、应试特调）见 [`skills/craft-your-textbook/README.md`](skills/craft-your-textbook/README.md)。

> ⚠️ 字段兼容性：Claude Code 插件清单（`plugin.json` / `marketplace.json`）字段随版本演进。若 `/plugin install` 报清单错误，以你本机 `/plugin` 的报错为准微调 `.claude-plugin/*.json`。

---

## 上手 Socratopia（破卷）

想亲身体验 AI 苏格拉底老师的教学，去 [www.socratopia.app](https://www.socratopia.app/r/SCR-FEJXMQ) 下载。注册时**输入邀请码 `SCR-FEJXMQ`**：免费用户得 **100 万 Token**，坐馆订阅用户得 **1 书币**（价值 $3.99）。
