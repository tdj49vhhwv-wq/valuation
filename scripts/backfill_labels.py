"""一次性回填：给 valuation_sample_cn.jsonl 补 event_type / stage_label，并归一化恒坤公司名。

映射规则（对应 docs/decisions 与 research-scope 3.1）：
- 融资增资（financing）：round_label 含字母轮次 → series_a/b/c / pre_ipo；无字母 → stage_label=n_a（不硬凑）。
- 股权激励/员工持股 → equity_incentive；股改整体变更 → restructuring_appraisal；
  老股转让/股权转让定价基础 → share_transfer；回购条款目标估值 → repurchase_clause。以上 stage 均 n_a。

可复核：本脚本保留，映射字典逐条对应 sample 的 round_label。
"""
import json
from collections import Counter
from pathlib import Path

PATH = Path(__file__).resolve().parent.parent / "samples" / "valuation_sample_cn.jsonl"

MAPPING = {
    # 融资（有字母轮次）
    "C轮融资（投前）": ("financing", "series_c"),
    "CII轮融资": ("financing", "series_c"),
    "Pre-IPO轮融资": ("financing", "pre_ipo"),
    "A轮增资（金浦临港/金浦科创/上海骁墨）": ("financing", "series_a"),
    "B轮增资（达晨系/杉晖/联炻等10家机构）": ("financing", "series_b"),
    "北交所上市前定增（15名自然人员工/关联方）": ("financing", "pre_ipo"),
    # 融资（无字母轮次 → n_a）
    "2021年9月增资（赛格高技术/上汽科技）": ("financing", "n_a"),
    "2018年6月增资与股权转让": ("financing", "n_a"),
    "2020年5月火炬电子增资": ("financing", "n_a"),
    "2020年9月最近一次股权融资": ("financing", "n_a"),
    "2022年10月增资（深圳达晨等）": ("financing", "n_a"),
    "第十二次增资（发行股票）": ("financing", "n_a"),
    "新三板挂牌后第一次定增（稳正景明/长泽创投）": ("financing", "n_a"),
    "报告期内第一次增资（贝达药业等）": ("financing", "n_a"),
    "报告期期初至今第一次增资（合肥蔚悦/清控银杏等10家机构）": ("financing", "n_a"),
    "股份公司第三次增资（毅达服务业等外部投资人）": ("financing", "n_a"),
    "股份公司第四次增资（德开元泰/永鑫开拓）": ("financing", "n_a"),
    "2021年7月增资（盈科吉运/盈科价值等）": ("financing", "n_a"),
    "报告期内第二次增资（源峰磐赛/高瓴祈睿等）": ("financing", "n_a"),
    "股份公司第六次增资（宜兴高易/厦门羽嘉等，员工同价）": ("financing", "n_a"),
    # 股权激励
    "评估基准日估值（员工持股定价基准）": ("equity_incentive", "n_a"),
    "第四次股权激励（投后）": ("equity_incentive", "n_a"),
    "第五次股权激励（评估公允价值）": ("equity_incentive", "n_a"),
    "2022年5月员工股权激励（黄山佳捷增资）": ("equity_incentive", "n_a"),
    "股份公司第一次增资（员工股权激励，宁波胜诺）": ("equity_incentive", "n_a"),
    "股份公司第二次增资（员工股权激励，苏州胜盈）": ("equity_incentive", "n_a"),
    # 股改整体变更
    "改制基准日净资产评估（整体变更）": ("restructuring_appraisal", "n_a"),
    "整体变更为股份有限公司（净资产评估值）": ("restructuring_appraisal", "n_a"),
    # 老股转让 / 股权转让定价基础
    "第一次股权转让定价基础（评估基准2019-09-30）": ("share_transfer", "n_a"),
    "第四、五次股权转让定价基础（评估基准2020-06-30）": ("share_transfer", "n_a"),
    "申报前12个月老股转让（德朴投资→汇智同裕）": ("share_transfer", "n_a"),
    # 回购条款（非成交）
    "回购条款中的目标估值（非实际融资成交）": ("repurchase_clause", "n_a"),
}

RENAME = {"恒坤新材料股份有限公司": "厦门恒坤新材料科技股份有限公司"}

FIELDS = [
    "record_type", "company_name", "stock_code", "country", "round_label",
    "event_type", "stage_label", "event_date", "valuation_amount",
    "valuation_currency", "valuation_stage", "valuation_basis",
    "price_per_share", "total_shares", "valuation_date", "disclosure_date",
    "source_page", "evidence_text", "data_source", "notes",
]


def main() -> None:
    rows = [json.loads(l) for l in PATH.read_text(encoding="utf-8").splitlines() if l.strip()]
    missing = []
    for r in rows:
        if r["company_name"] in RENAME:
            r["company_name"] = RENAME[r["company_name"]]
        rl = r.get("round_label")
        if rl not in MAPPING:
            missing.append(rl)
            continue
        et, sl = MAPPING[rl]
        r["event_type"] = et
        r["stage_label"] = sl
        if et == "financing" and sl == "n_a":
            r["notes"] = (r.get("notes") or "").rstrip() + "；阶段待核实（round_label 未标注字母轮次）"
    if missing:
        print("未匹配 round_label（未打标签，请手动补）：")
        for m in missing:
            print("  ", m)
    ordered = [{k: r.get(k) for k in FIELDS} for r in rows]
    PATH.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in ordered) + "\n", encoding="utf-8")
    print("event_type:", dict(Counter(r["event_type"] for r in ordered)))
    print("stage_label:", dict(Counter(r["stage_label"] for r in ordered)))
    print("financing 中 stage 非 n_a 的条数：", sum(1 for r in ordered if r["event_type"] == "financing" and r["stage_label"] != "n_a"))


if __name__ == "__main__":
    main()
