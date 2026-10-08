# 中美企业估值比较（Valuation）

> 招股书中一级市场股权定价：在行业、商业模式、发展阶段可比的前提下，研究中美企业**一级市场估值差异**，以及**一级市场估值 → IPO 定价 → 上市后二级市场价格**之间的关系。

## 项目身份

| 项 | 内容 |
| --- | --- |
| 项目名称 | 中国企业与美国企业估值比较 |
| Project ID | `9912c8da-9329-49d1-a20b-65a7e8c6013f`（FLAB 项目 URL 中 projects/ 后的一段） |
| Project Lead | 赵秉清 |
| 成员与角色 | 杨苗鑫（质量/交叉检验、人工金标准；分工见 [docs/meetings/2026-10-08.md](docs/meetings/2026-10-08.md)） |
| 代码仓库 | https://github.com/tdj49vhhwv-wq/valuation（暂用个人仓；指南正式仓库 suibe-flab/valuation 待建/待授权，见 DEC-005） |
| 默认分支 | main（初始化经工作分支 + PR 合并） |
| 推荐 Runtime | **待确认**（本地 / 腾讯云，见 [docs/runtime-and-runbook.md](docs/runtime-and-runbook.md)） |
| 当前阶段 | **问题定义 + 文档初始化**（未进入批量数据工作；导师决定**先做国内**，见 DEC-004） |

## 研究问题（一句话）

在行业、商业模式、发展阶段可比的前提下，研究中美企业一级市场估值差异，以及一级市场估值与上市后二级市场价格之间的关系。

## 研究范围（工作版，权威口径见 docs/research-scope.md）

- 研究对象：有可核验「一级市场股权定价」记录的中国企业与美国企业。
- **阶段顺序：先做国内**（招股书披露的一级估值），美国企业数据用已购 PitchBook 后续做比较。
- 一行数据：一次「企业 × 融资轮次/估值时点」的可核验估值观测（试行）。
- 明确不做（本阶段）：不做因果推断结论；不做全市场覆盖；不处理无披露的私人估值。

## 当前最小交付物

**10 月 10 日前**提交「可评审初始化包」：README、AGENTS.md 及 docs/ 下 6 个文件，经工作分支 + PR 交付，PR 关联 FLAB Issue **#1「项目初始化」**。

## 文档与数据入口

| 想找什么 | 去哪里 |
| --- | --- |
| 项目是什么、怎么开始 | 本文件 |
| Agent 执行边界 | [AGENTS.md](AGENTS.md) |
| 研究问题与口径 | [docs/research-scope.md](docs/research-scope.md) |
| 数据来源与字段 | [docs/data-management.md](docs/data-management.md) |
| 怎么运行 / 检查 | [docs/runtime-and-runbook.md](docs/runtime-and-runbook.md) |
| 决策与理由 | [docs/decisions.md](docs/decisions.md) |
| 会议记录 | [docs/meetings/](docs/meetings/) |
| 估值字段 Schema | [src/valuation_models.py](src/valuation_models.py) |
| 真实样例（dry-run） | [samples/valuation_dryrun_sample.jsonl](samples/valuation_dryrun_sample.jsonl) |
| 数据目录索引 | [data/README.md](data/README.md) |

## 验收方式

新成员仅靠本 README 能找到入口与下一项任务；Agent 仅靠 AGENTS.md 能判断何时开始 / 暂停 / 请求人确认；一个小样本（或明确标注的合成样例）能按 runtime-and-runbook 复现并可回到来源。
