# AGENTS.md — 中美企业估值比较（Valuation）

本文件是**当前有效**的 Agent 执行规则与边界。开始任何任务前，Agent 必须先完成下方「开始前检查」。每次会议仅在改变 Agent 行为时更新本文件，详细过程见 docs/meetings/。

## 1. 项目身份与文档边界

- 项目：中国企业与美国企业估值比较
- Project ID：**待确认**（缺失时停在只读检查，向 Project Lead 询问，不得猜测）
- Project Lead：赵秉清；成员：杨苗鑫（质量/交叉检验、人工金标准，见 meetings/2026-10-08）
- 仓库：https://github.com/tdj49vhhwv-wq/valuation（暂用个人仓；正式 suibe-flab/valuation 待建/待授权，见 DEC-005）
- 本文件适用于仓库根目录及 docs/、data/、src/、scripts/、tests/
- 权威口径：研究见 [docs/research-scope.md](docs/research-scope.md)，数据见 [docs/data-management.md](docs/data-management.md)，运行见 [docs/runtime-and-runbook.md](docs/runtime-and-runbook.md)，决策见 [docs/decisions.md](docs/decisions.md)

## 2. 目标、范围、不做

- 目标：建立「中美可比企业一级市场估值差异」「一级估值 ↔ 上市后二级价格关系」的可核验证据。
- 当前阶段：问题定义 + 文档初始化；**先做国内**（导师决定），美国数据用已购 PitchBook（见 DEC-004）。
- 明确不做：不批量下载、不发布研究结论、不覆盖原始数据、不推断「数据不存在」。

## 3. 角色与责任

- Project Lead 决定并验收：研究口径、纳入排除标准、证据标准、发布内容、敏感数据处理。
- Agent 可协助或执行：文档整理、候选来源检索、小样本脚本、dry-run、结果报告。
- 发生阻塞时向 Project Lead 报告，不得自行放宽口径或跳过审批。

## 4. 开始前检查（必须逐项确认）

- [ ] Project ID、Issue、仓库、分支、Runtime 已确认？
- [ ] 已读本文件、README.md、docs/research-scope.md、docs/data-management.md？
- [ ] 输入数据版本、读取路径、输出路径已知？
- [ ] 已确认没有把密钥、个人信息、大文件、未经许可数据放入仓库？

## 5. 当前有效的工作规则

- **必须**：原始数据只读保存，不覆盖原路径。
- **必须**：候选匹配 / 候选估值标记为「候选」，不写成已确认事实。
- **必须**：估值显式区分投前 / 投后、币种、单位、时间口径（见 scope 3.2）。
- **应该**：新数据修订创建新版本，并更新 Manifest / Schema / Quality 记录。
- **可以**：先用公开样例或明确标注的合成样例做 dry-run。
- **禁止**：把 LLM 输出 / 常识当作未复核事实；提交 Token、密码、连接串、个人敏感信息；批量下载未经许可数据；读取其他项目数据。

## 6. 证据、质量与交付标准

- 一条估值记录至少需要：企业标识 + 轮次/时点 + 估值额 + 币种 + 投前/投后 + 来源 + 披露日期。
- 缺失、冲突、低置信、无法确认 → 标记「缺失 / 待核实」，不得补写。
- 交付时报告：来源、数据版本、抽样复核结果、范围与唯一性检查结果、剩余待核实项。

## 7. 输出、版本、恢复

- 正式结果进 docs/ 或 results/；原始数据、大文件不提交仓库，登记于 data-management.md。
- 每个正式数据版本保留 Manifest、Schema、Quality、文件哈希。
- 长任务中断后从最近检查点恢复；发现错误保留旧版本并发布修正版。

## 8. 本次更新

首次创建（2026-10-03）。后续会议仅在改变 Agent 行为时更新，判断与提案格式见 docs/meetings/。
