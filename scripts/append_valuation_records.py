"""追加 6 条新估值观测：兴福电子(688545) + 百奥赛图(688796)。

来源：prospectus-pevc-project 仓库 week1/review 下两家招股书正式稿（MinerU）。
每条附逐字证据 + 行号，可回源。写入 samples/valuation_sample_cn.jsonl。
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
PATH = BASE / "samples" / "valuation_sample_cn.jsonl"

XINGFU = "688545_兴福电子_招股书_正式稿_20250117.md"
BAIO = "688796_百奥赛图_招股书_正式稿_20251204.md"

FIELDS = [
    "record_type", "company_name", "stock_code", "country", "round_label",
    "event_type", "stage_label", "event_date", "valuation_amount",
    "valuation_currency", "valuation_stage", "valuation_basis",
    "price_per_share", "total_shares", "valuation_date", "disclosure_date",
    "source_page", "evidence_text", "data_source", "notes",
]

RECORDS = [
    {  # 兴福电子 增资定价评估值
        "record_type": "valuation_event",
        "company_name": "湖北兴福电子材料股份有限公司",
        "stock_code": "688545",
        "country": "CN",
        "round_label": "第二次增资定价依据（净资产评估，基准2021-10-31）",
        "event_type": "financing",
        "stage_label": "n_a",
        "event_date": "2021-10-31",
        "valuation_amount": 158510.0,
        "valuation_currency": "CNY",
        "valuation_stage": "appraised",
        "valuation_basis": "appraisal",
        "price_per_share": None,
        "total_shares": None,
        "valuation_date": "2021-10-31",
        "disclosure_date": None,
        "source_page": f"{XINGFU} L2905-2908",
        "evidence_text": "在评估基准日2021年10月31日，兴福有限股东全部权益的评估价值为158,510.00万元。",
        "data_source": "pdf_disclosed",
        "notes": "增资定价依据（众联评报字[2021]第1245号），国家大基金二期等15家战投增资的评估基准",
    },
    {  # 兴福电子 股改净资产评估值
        "record_type": "valuation_event",
        "company_name": "湖北兴福电子材料股份有限公司",
        "stock_code": "688545",
        "country": "CN",
        "round_label": "整体变更为股份有限公司（净资产评估值）",
        "event_type": "restructuring_appraisal",
        "stage_label": "n_a",
        "event_date": "2022-04-30",
        "valuation_amount": 136830.56,
        "valuation_currency": "CNY",
        "valuation_stage": "appraised",
        "valuation_basis": "appraisal",
        "price_per_share": None,
        "total_shares": None,
        "valuation_date": "2022-04-30",
        "disclosure_date": None,
        "source_page": f"{XINGFU} L2635-2636",
        "evidence_text": "确认截至2022年4月30日，兴福有限净资产评估值136,830.56万元。",
        "data_source": "pdf_disclosed",
        "notes": "股改整体变更净资产评估（众联评报字[2022]第1211号）",
    },
    {  # 兴福电子 战投增资投后（价格×注册资本）
        "record_type": "valuation_event",
        "company_name": "湖北兴福电子材料股份有限公司",
        "stock_code": "688545",
        "country": "CN",
        "round_label": "2021年12月增资（国家大基金二期等15家战略投资者）",
        "event_type": "financing",
        "stage_label": "n_a",
        "event_date": "2021-12",
        "valuation_amount": 249600.0,
        "valuation_currency": "CNY",
        "valuation_stage": "post_money",
        "valuation_basis": "price_times_shares",
        "price_per_share": 4.8,
        "total_shares": 52000.0,
        "valuation_date": None,
        "disclosure_date": None,
        "source_page": f"{XINGFU} L2918-2922",
        "evidence_text": "15家战略投资者出资人民币76,800万元认购兴福有限新增注册资本16,000万元，此次增资的股东投资溢价60,800万元全部计入兴福有限的资本公积。本次增资价格为4.8元/注册资本",
        "data_source": "calculated",
        "notes": "4.8元/注册资本 × 52,000万注册资本 = 249,600万元投后；阶段待核实（round_label未标注字母轮次）",
    },
    {  # 百奥赛图 股改净资产评估值
        "record_type": "valuation_event",
        "company_name": "百奥赛图（北京）医药科技股份有限公司",
        "stock_code": "688796",
        "country": "CN",
        "round_label": "整体变更为股份有限公司（净资产评估值）",
        "event_type": "restructuring_appraisal",
        "stage_label": "n_a",
        "event_date": "2020-10-31",
        "valuation_amount": 272024.04,
        "valuation_currency": "CNY",
        "valuation_stage": "appraised",
        "valuation_basis": "appraisal",
        "price_per_share": None,
        "total_shares": None,
        "valuation_date": "2020-10-31",
        "disclosure_date": None,
        "source_page": f"{BAIO} L2715-2716",
        "evidence_text": "截至2020年10月31日，百奥赛图有限净资产的评估值为272,024.04万元。",
        "data_source": "pdf_disclosed",
        "notes": "股改整体变更净资产评估（中水致远评报字[2020]第010211号）",
    },
    {  # 百奥赛图 老股转让隐含估值
        "record_type": "valuation_event",
        "company_name": "百奥赛图（北京）医药科技股份有限公司",
        "stock_code": "688796",
        "country": "CN",
        "round_label": "2020年10月老股转让（百奥维达→Astral/苇渡阿尔法）",
        "event_type": "share_transfer",
        "stage_label": "n_a",
        "event_date": "2020-10",
        "valuation_amount": 647000.0,
        "valuation_currency": "CNY",
        "valuation_stage": "post_money",
        "valuation_basis": "price_times_shares",
        "price_per_share": 105.60,
        "total_shares": 6127.4,
        "valuation_date": None,
        "disclosure_date": None,
        "source_page": f"{BAIO} L3315-3322",
        "evidence_text": "约定百奥维达以38,318.0839万元等值美元的价格将其持有的百奥赛图有限注册资本362.8455万元（占百奥赛图有限注册资本5.9217%）转让给Astral。",
        "data_source": "calculated",
        "notes": "老股转让隐含估值：38,318.08万元÷5.9217%≈647,000万元（105.60元/注册资本×6,127.4万注册资本）",
    },
    {  # 百奥赛图 D+轮增资投后（价格×股本）
        "record_type": "valuation_event",
        "company_name": "百奥赛图（北京）医药科技股份有限公司",
        "stock_code": "688796",
        "country": "CN",
        "round_label": "2021年6月增资（D+轮，LBC/CTW/OrbiMed/Cbio/Octagon）",
        "event_type": "financing",
        "stage_label": "series_c",
        "event_date": "2021-06",
        "valuation_amount": 750000.0,
        "valuation_currency": "CNY",
        "valuation_stage": "post_money",
        "valuation_basis": "price_times_shares",
        "price_per_share": 20.83,
        "total_shares": 36000.0,
        "valuation_date": None,
        "disclosure_date": None,
        "source_page": f"{BAIO} L3465-3466",
        "evidence_text": "LBC向公司增资9,720万元人民币等值的美元，溢价认购公司新增注册资本466.5600万元（即466.5600万股新增股份），其中466.5600万元计为公司注册资本，9,253.4400万元计入公司的资本公积",
        "data_source": "calculated",
        "notes": "增资价≈20.83元/股（9,720万÷466.56万股）×股改折股36,000万股≈75亿元投后；D+轮",
    },
]


def main() -> None:
    existing = [json.loads(l) for l in PATH.read_text(encoding="utf-8").splitlines() if l.strip()]
    existing_keys = {(r["stock_code"], r["round_label"], r["event_date"]) for r in existing}
    added = 0
    for rec in RECORDS:
        key = (rec["stock_code"], rec["round_label"], rec["event_date"])
        if key in existing_keys:
            print("跳过重复：", key)
            continue
        ordered = {k: rec[k] for k in FIELDS}
        existing.append(ordered)
        added += 1
    PATH.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in existing) + "\n", encoding="utf-8")
    print(f"新增 {added} 条，当前总数 {len(existing)}")


if __name__ == "__main__":
    main()
