"""
Valuation 项目 Pydantic v2 模型 — 一级市场估值提取

定位：在 PEVC 招股书提取（price_per_share / amount / shares）之上，补出「估值」本身。
PEVC 项目（prospectus-pevc-project）提取了融资事件的价格与数量，但没有把
投前/投后估值、评估值、IPO 定价、上市后价格作为一等字段记录。本 schema 补这一层。

一行 = 一次「企业 × 估值时点」的估值观测。
关键规则（沿用 PEVC 项目的诚实原则）：
  - 原文直接披露估值 → valuation_amount 填披露值，valuation_basis=disclosed/appraisal
  - 只有价格没有总股本 → 不强行回算估值，valuation_amount 留空，标「待核实总股本」
  - 价格×总股本 / 市盈率×净利润 回算 → valuation_basis 标 calculated，notes 写公式
"""
from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field, field_validator, model_validator


class Currency(str, Enum):
    CNY = "CNY"
    USD = "USD"
    HKD = "HKD"


class Country(str, Enum):
    CN = "CN"
    HK = "HK"  # 港股上市（中国公司，境外架构），仍属「中国侧」比较口径
    US = "US"


class ValuationStage(str, Enum):
    PRE_MONEY = "pre_money"        # 投前估值
    POST_MONEY = "post_money"      # 投后估值
    APPRAISED = "appraised"        # 资产评估值 / 公允价值
    IPO_PRICE = "ipo_price"        # IPO 定价
    LISTED_PRICE = "listed_price"  # 上市后二级价格


class ValuationBasis(str, Enum):
    DISCLOSED = "disclosed"                    # 原文直接披露估值额
    APPRAISAL = "appraisal"                    # 评估报告 / 估值报告
    PRICE_TIMES_SHARES = "price_times_shares"  # 价格×总股本回算（calculated）
    PE_MULTIPLE = "pe_multiple"                # 市盈率×净利润回算（calculated）
    OTHER = "other"


class DataSource(str, Enum):
    PDF_DISCLOSED = "pdf_disclosed"
    CALCULATED = "calculated"
    INFERRED = "inferred"


class EventType(str, Enum):
    """估值事件类型：融资增资 / 股权激励 / 老股转让 / 股改评估 / 回购条款 / 其他。"""
    FINANCING = "financing"                            # 融资增资（外部投资人）
    EQUITY_INCENTIVE = "equity_incentive"              # 股权激励 / 员工持股
    SHARE_TRANSFER = "share_transfer"                  # 老股转让 / 股权转让定价基础
    RESTRUCTURING_APPRAISAL = "restructuring_appraisal"  # 股改整体变更净资产评估
    REPURCHASE_CLAUSE = "repurchase_clause"            # 回购条款目标估值（非成交）
    OTHER = "other"


class StageLabel(str, Enum):
    """融资阶段标签：只在融资事件（financing）上打，非融资事件标 n_a。"""
    SEED = "seed"
    ANGEL = "angel"
    SERIES_A = "series_a"
    SERIES_B = "series_b"
    SERIES_C = "series_c"      # 含 C 轮及以后（CII 等）
    PRE_IPO = "pre_ipo"
    LISTED = "listed"
    N_A = "n_a"


class ValuationEvent(BaseModel):
    """一次估值观测：某企业某时点的估值是多少、什么口径、依据是什么。"""

    record_type: str = Field(default="valuation_event", description="记录类型标识")

    # ── 企业标识 ──
    company_name: str = Field(..., min_length=1, description="公司全称")
    stock_code: str = Field(..., min_length=1, description="股票代码（A股6位 / 港股4位）；未上市可用代码0占位并标注")
    country: Country = Field(..., description="国别/上市地（CN=A股 / HK=港股 / US=美股；港股仍属中国侧比较口径）")

    # ── 事件与轮次 ──
    round_label: Optional[str] = Field(None, description="轮次/事件标签（如 C轮、第四次股权激励、A轮增资）")
    event_type: Optional[EventType] = Field(None, description="事件类型（融资/激励/转让/股改评估/回购条款），用于可比匹配")
    stage_label: Optional[StageLabel] = Field(None, description="融资阶段标签，仅融资事件（financing）打；非融资事件标 n_a")
    event_date: str = Field(..., min_length=7, description="估值/交易日期（YYYY-MM-DD 或 YYYY-MM）")

    # ── 估值核心字段 ──
    valuation_amount: Optional[float] = Field(
        None, ge=0,
        description="估值额（统一单位：万元本币）。原文未披露且无法回算则留空，不硬凑"
    )
    valuation_currency: Currency = Field(..., description="估值币种")
    valuation_stage: ValuationStage = Field(..., description="投前 / 投后 / 评估 / IPO定价 / 上市价")
    valuation_basis: ValuationBasis = Field(..., description="估值依据（披露 / 评估 / 价格×股本 / 市盈率）")

    # ── 回算输入（可为空） ──
    price_per_share: Optional[float] = Field(None, ge=0, description="每股价格（元/股 或 元/注册资本）")
    total_shares: Optional[float] = Field(None, ge=0, description="总股本（万股），用于回算投后估值")
    valuation_date: Optional[str] = Field(None, description="估值基准日（评估报告基准日等）")
    disclosure_date: Optional[str] = Field(None, description="披露日期")

    # ── 来源与证据 ──
    source_page: str = Field(..., min_length=1, description="PDF 页码或 MD 行号范围（如 胜科纳米.md L8496-8499）")
    evidence_text: str = Field(..., min_length=20, description="原文逐字摘录，不可人工概括")
    data_source: DataSource = Field(default=DataSource.PDF_DISCLOSED, description="来源：原文披露 / 计算 / 推断")

    notes: Optional[str] = Field(None, description="备注（人工概括、回算公式、待核实项放这里）")

    @field_validator("event_date", "valuation_date", "disclosure_date")
    @classmethod
    def check_date(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        import re
        if not re.match(r'^\d{4}-\d{2}(-\d{2})?$', v):
            raise ValueError(f"日期格式错误: {v}，应为 YYYY-MM-DD 或 YYYY-MM")
        return v

    @field_validator("evidence_text")
    @classmethod
    def check_not_summary(cls, v: str) -> str:
        for kw in ["招股书显示", "招股书披露", "根据招股书", "据招股书"]:
            if v.strip().startswith(kw):
                raise ValueError("evidence_text 疑似概括性语言，应为原文逐字摘录")
        return v

    @model_validator(mode="after")
    def cross_check_price_shares(self) -> "ValuationEvent":
        """价格×总股本 与估值额一致性检查（允许 6% 误差，仅记录不阻断）。"""
        if (
            self.valuation_basis == ValuationBasis.PRICE_TIMES_SHARES
            and self.price_per_share is not None
            and self.total_shares is not None
            and self.valuation_amount is not None
        ):
            expected = self.price_per_share * self.total_shares
            if expected > 0 and abs(expected - self.valuation_amount) / expected > 0.06:
                self.notes = (self.notes or "") + f" [cross-check: 价格×股本={expected:.1f} 与估值额偏差>6%]"
        return self


def validate_jsonl(jsonl_path, model_class=ValuationEvent) -> dict:
    """逐行校验 JSONL，返回 {pass, warn, fail, errors}。"""
    import json
    from pathlib import Path

    stats = {"pass": 0, "warn": 0, "fail": 0, "errors": []}
    p = Path(jsonl_path)
    if not p.exists():
        stats["errors"].append(f"文件不存在: {jsonl_path}")
        return stats

    with open(p, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                model_class(**data)
                stats["pass"] += 1
            except Exception as e:
                stats["fail"] += 1
                stats["errors"].append({"line": line_num, "error": str(e)[:200]})
    return stats


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(validate_jsonl(sys.argv[1]))
