# Picker Skills

精选 AI 技能包（SKILL）开源仓库 —— 每个 SKILL 是一个文件夹（核心是 `SKILL.md`），装着完成某类任务的**完整流程、检查清单和脚本**。装进 Claude Code 等 AI 编程工具后，一句话即可触发整套专业工作流。

A curated collection of AI skills. Each skill is a folder (centered on `SKILL.md`) containing a complete workflow, checklists and scripts for one kind of task. Install into Claude Code — or paste `SKILL.md` into any AI chat — and trigger a full professional workflow with one sentence.

**🌐 在线浏览 / Browse online: <https://picker.bluecatbot.com>**

## 安装 / Install

**Claude Code（推荐）** — 一行命令装一个技能：

```bash
npx degit shushuitie2017/picker-skills/<skill-id> "$HOME/.claude/skills/<skill-id>" --force
# 例如 / e.g.
npx degit shushuitie2017/picker-skills/oss-deep-analysis "$HOME/.claude/skills/oss-deep-analysis" --force
```

> `"$HOME/..."` 写法在 Windows PowerShell / macOS / Linux 下通用（PowerShell 不展开 `~`，请勿用 `~` 写路径）；`--force` 使重装/更新时可覆盖已有目录。
> The `"$HOME/..."` form works in Windows PowerShell, macOS and Linux alike (PowerShell does **not** expand `~`); `--force` allows reinstalling/updating over an existing folder.

或克隆后拷贝 / or clone & copy:

```bash
git clone --depth 1 https://github.com/shushuitie2017/picker-skills.git
cp -r picker-skills/<skill-id> ~/.claude/skills/
```

**通用 AI（不用 Claude Code）** — 打开对应文件夹里的 `SKILL.md`，全文复制后贴进任意 AI 对话开头即可。
**Any AI chat** — open the skill's `SKILL.md`, copy the whole file and paste it at the start of your conversation.

## 技能目录 / Skills

### 调研分析 / Research
| ID | 说明 / Description |
|---|---|
| [`oss-deep-analysis`](./oss-deep-analysis) | 开源项目深度分析：输入任意仓库，产出「值不值得用」的单文件 HTML 报告 / Deep-analysis HTML report for any open-source repo: architecture, maturity, community, verdict |
| [`repo-value-analysis`](./repo-value-analysis) | 仓库核心价值论证报告（含私有/内部项目）/ Evidence-based core-value report for any repo, incl. private ones |

### 编程开发 / Coding & Dev
| ID | 说明 / Description |
|---|---|
| [`debug-backend`](./debug-backend) | 后端 bug 系统化诊断流程 / Systematic backend debugging workflow |
| [`review`](./review) | 后端代码审查清单（安全/性能/规范）/ Backend code review checklist |
| [`test`](./test) | 按项目惯例生成单测与集成测试 / Test generation following project conventions |
| [`sql`](./sql) | SQL 审查、优化与 schema 设计 / SQL review, optimization & schema design |
| [`api`](./api) | RESTful API 全层代码生成 / Full-stack REST endpoint scaffolding |
| [`commit`](./commit) | Conventional Commits 规范化提交 / Conventional commit automation |
| [`dev-commons`](./dev-commons) | 从 30+ 真实项目提炼的 140+ 条开发模式，BM25 检索 / 140+ dev patterns from 30+ real projects, BM25-searchable |

### 写作创作 / Writing
| ID | 说明 / Description |
|---|---|
| [`note-writer`](./note-writer) | note.com/Zenn 写作智能：14 文章类型、25 标题公式、BM25 检索 / Writing intelligence for note.com/Zenn with a BM25 search engine |

### 创意制作 / Creative
| ID | 说明 / Description |
|---|---|
| [`flow-cinema`](./flow-cinema) | 用 Google Flow（Veo 3.1）端到端拍多镜头电影短片，自我进化 / Direct multi-shot AI short films end-to-end with Google Flow (Veo 3.1), self-evolving |

### 办公效率 / Productivity
| ID | 说明 / Description |
|---|---|
| [`context-handoff`](./context-handoff) | AI 会话进度交接文档，跨会话无缝接力 / Session handoff docs for seamless continuation |
| [`notebooklm`](./notebooklm) | Google NotebookLM 全功能自动化 / Full programmatic NotebookLM automation |

## 元数据 / Metadata

[`index.json`](./index.json) 收录全部技能的结构化元数据（分类、三语描述、适用场景、文件清单），Picker 网站直接以它为数据源。
[`index.json`](./index.json) holds structured metadata (category, trilingual descriptions, use cases, file lists) for every skill — it is the data source of the Picker website.

## 投稿 / Contributing

欢迎 PR：新建 `<your-skill-id>/SKILL.md`（参考现有技能的写法），并在 `index.json` 里补一条元数据。
PRs welcome: add `<your-skill-id>/SKILL.md` (see existing skills for the format) and append one entry to `index.json`.

## License

[MIT](./LICENSE)
