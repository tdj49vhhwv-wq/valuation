# initialization-check.md — 初始化检查（真实小样本已跑通）

> 记录一次最小闭环（真实公开招股书样例）的预期、实际结果与剩余问题。
> 状态：**已执行**（2026-10-03，两条真实来源，5 条记录，Pydantic 校验全通过）。
> 后续扩展：dry-run 5 条已扩充为 **16 条真实估值观测**（8 家国内公司），见 [samples/valuation_sample_cn.jsonl](../samples/valuation_sample_cn.jsonl) 与 [docs/data-coverage-survey.md](data-coverage-survey.md)；本文件仍保留 5 条最小闭环记录。

## 目标

用公开招股书样例，验证「文档 → 字段 → 输出 → 回到来源」的最小闭环。

## 样例来源（两边）

| 来源 | 公司 | 代码 | 用途 |
| --- | --- | --- | --- |
| 之前用过（PEVC 项目） | 黄山谷捷 | 301581 | 增资定价 / 评估值 |
| 公开（巨潮，未进 PEVC 8 家） | 胜科纳米 | 688757 | 投前 / 投后 / 评估 时间序列 |

## 字段规格（schema）

代码：[src/valuation_models.py](../src/valuation_models.py)。核心字段：

- `valuation_amount`（估值额，万元）/ `valuation_currency`（币种）
- `valuation_stage`：`pre_money` 投前 / `post_money` 投后 / `appraised` 评估 / `ipo_price` / `listed_price`
- `valuation_basis`：`disclosed` 原文披露 / `appraisal` 评估报告 / `price_times_shares` 价格×股本回算 / `pe_multiple` 市盈率回算
- 回算输入：`price_per_share`（元/股 或 元/注册资本）/ `total_shares`（万股）
- 证据：`evidence_text`（原文逐字摘录）+ `source_page`（MD 行号/PDF 页码）

## 预期 vs 实际

| 项 | 预期 | 实际 |
| --- | --- | --- |
| 字段完整 | 核心字段全部可填 | 5 条记录字段完整；1 条估值额留空（待总股本，见下） |
| 可回源 | 有页码/行号 | 全部有 `source_page` + `evidence_text` 原文 |
| Schema 校验 | 全部通过 | **5 pass / 0 fail**（`python3 src/valuation_models.py samples/valuation_dryrun_sample.jsonl`） |

## 提取结果（5 条，样例见 samples/valuation_dryrun_sample.jsonl）

| # | 公司 | 时点 | 估值（万元） | 口径 | 依据 |
| --- | --- | --- | --- | --- | --- |
| 1 | 黄山谷捷 | 2021-12-31 | 40,370 | 评估 | 评估报告（股东全部权益） |
| 2 | 黄山谷捷 | 2021-09-18 | **留空** | 投后（待回算） | 增资价 22.42 元/注册资本，缺总股本 |
| 3 | 胜科纳米 | 2020-11 | 50,300 | 投后 | 原文披露 5.03 亿 |
| 4 | 胜科纳米 | 2021-02 | 100,000 | 投前 | 原文披露 C 轮 10.00 亿 |
| 5 | 胜科纳米 | 2021-04-30 | 129,000 | 评估 | 评估报告公允价值 12.90 亿 |

## 这次 dry-run 验证了什么

1. **三种估值口径都能落**：投前 / 投后 / 评估值，且都能量化到统一单位（万元 CNY）。
2. **口径必须显式区分**：胜科纳米 5.03亿（投后）→ 10.00亿（投前）→ 12.90亿（评估），若混在一起会得到错误的时间序列。
3. **诚实处理「不硬凑」**：黄山谷捷第 2 条只有增资价、没有总股本，`valuation_amount` 留空并标注「待核实总股本」，而不是编一个估值。

## 剩余问题

| 事项 | 状态 | 下一步 |
| --- | --- | --- |
| 黄山谷捷增资后总注册资本 | 待核实 | 在招股书「股本情况」章节补总股本，回算投后估值 |
| 币种统一为 USD 的折算规则 | 待核实 | 做中美比较时定汇率口径 |
| 上市后二级价格（listed_price）字段 | 待补充 | 第二阶段接 PitchBook / 行情数据 |
| 港币（HKD）港股招股书口径 | 待核实 | 港股样例验证 |
