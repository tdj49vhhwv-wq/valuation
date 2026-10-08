# runtime-and-runbook.md — 运行手册（工作版）

> 让另一位成员能按本文件完成一次小规模运行。当前唯一可运行的是 Schema 校验脚本；提取流水线待建。

## 1. 运行环境

- **待确认**：本地 Runtime / 腾讯云 Runtime / 混合，及原因。
- 当前阶段：本地即可（纯 Python 脚本，无网络 / GPU 依赖）。

## 2. 输入与输出

- 输入：`samples/valuation_sample_cn.jsonl`（已提取估值观测，26 条）或 `samples/valuation_dryrun_sample.jsonl`（最小闭环 5 条）。
- 输出：Schema 校验报告（pass / warn / fail 计数 + 字段级错误明细）。

## 3. 启动命令、参数与预期输出（可运行）

唯一可运行脚本：Schema 校验。

```bash
cd ~/GitHub/valuation
python3 src/valuation_models.py samples/valuation_sample_cn.jsonl
```

预期输出：`26 pass / 0 fail`（若有 warn 一并打印）。失败时逐条打印字段级错误，便于定位。

## 4. 小样本 dry-run 流程（人工提取）

1. 读 README.md、AGENTS.md、research-scope.md、data-management.md；
2. 选 1 份公开招股书样例（**先国内**：A 股 / 港股招股书）；
3. 提取「企业-轮次-估值额-币种-投前/投后-来源页码」；
4. 写入 `samples/*.jsonl`，跑第 3 节命令校验；
5. 由另一位成员或人工复核；
6. 报告：来源、字段、缺失项、待核实项。

## 5. 资源需求、时间与并发

- 资源：无 GPU / 网络；内存 / CPU 可忽略。
- 时间：Schema 校验 <1 秒；单条人工提取约 10–30 分钟。
- 并发：无（单机串行，无需并发控制）。

## 6. 中断、失败与重复运行

- 校验脚本幂等，可重复运行；失败不影响输入文件。
- 提取中断：保留中间结果与日志，从最近检查点重跑；不覆盖 raw。
- 发现错误：保留旧版本并发布修正版（data-management.md 第 4 节）。

## 7. 质量检查（运行后）

- 投前/投后是否显式标注；币种/单位是否统一；来源是否可回到原文。
- 范围、唯一性、抽样复核（见 data-management.md 第 4 节）。

## 8. 交付

- 结果上传/登记：正式结果进 docs/ 或 results/；数据版本与哈希记录于 data-management.md。
