"""可比企业候选对生成（第一阶段：国内 × 国内）。

输入：samples/company_master_cn.jsonl（企业主表）+ samples/valuation_sample_cn.jsonl（估值样本）。
输出：samples/comparable_pairs_cn.jsonl（候选对），控制台打印分布。

规则（对齐 research-scope 3.1/3.5 与 AGENTS.md）：
- 第一层：sector 相同 → 候选对。
- 第二层：subsector 相同 → 标「强候选」（更近）。
- 第三层：双方 financing 事件的 stage_label 有交集 → stage_overlap=true（阶段可比）。
- 候选对一律标「候选」，不写「已确认」；中美匹配留接口（country 字段已就绪）。
"""
import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
MASTER = BASE / "samples" / "company_master_cn.jsonl"
SAMPLE = BASE / "samples" / "valuation_sample_cn.jsonl"
OUT = BASE / "samples" / "comparable_pairs_cn.jsonl"

# 公司简称（用于可读输出，仅 16 家国内企业）
SHORT = {
    "688757": "胜科纳米", "301581": "黄山谷捷", "688729": "屹唐股份",
    "688727": "恒坤新材", "688783": "西安奕材", "688795": "摩尔线程",
    "688802": "沐曦股份", "301563": "云汉芯城", "688775": "影石创新",
    "688583": "思看科技", "603418": "友升股份", "920100": "三协电机",
    "688765": "禾元生物", "688759": "必贝特", "688758": "赛分科技",
    "688411": "海博思创",
}


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def financing_stages(rows: list[dict], code: str) -> set[str]:
    """某企业 financing 事件中非 n_a 的 stage_label 集合。"""
    return {
        r["stage_label"]
        for r in rows
        if r["stock_code"] == code and r.get("event_type") == "financing" and r.get("stage_label") not in (None, "n_a")
    }


def main() -> None:
    masters = load_jsonl(MASTER)
    rows = load_jsonl(SAMPLE)

    by_sector = defaultdict(list)
    for m in masters:
        by_sector[m["sector"]].append(m)

    pairs = []
    for sector, members in by_sector.items():
        for a, b in combinations(members, 2):
            sa, sb = financing_stages(rows, a["stock_code"]), financing_stages(rows, b["stock_code"])
            overlap = bool(sa and sb and sa & sb)
            pairs.append({
                "company_a": a["stock_code"],
                "company_b": b["stock_code"],
                "shared_sector": sector,
                "shared_subsector": a["subsector"] == b["subsector"],
                "stage_overlap": overlap,
                "stage_detail": f"{SHORT.get(a['stock_code'], a['stock_code'])}:{sorted(sa) or ['未标轮次']} vs "
                                f"{SHORT.get(b['stock_code'], b['stock_code'])}:{sorted(sb) or ['未标轮次']}",
                "confidence": "强候选" if a["subsector"] == b["subsector"] else "候选",
            })

    # 排序：强候选优先，同 subsector 靠前
    pairs.sort(key=lambda p: (not p["shared_subsector"], not p["stage_overlap"], p["shared_sector"], p["company_a"], p["company_b"]))

    OUT.write_text("\n".join(json.dumps(p, ensure_ascii=False) for p in pairs) + "\n", encoding="utf-8")

    print(f"候选对总数：{len(pairs)}")
    print("sector 分布：", {s: sum(1 for p in pairs if p['shared_sector'] == s) for s in sorted(by_sector)})
    print("强候选（同 subsector）：", sum(1 for p in pairs if p["shared_subsector"]))
    print("阶段可比（stage_overlap）：", sum(1 for p in pairs if p["stage_overlap"]))
    print("\n强候选对：")
    for p in pairs:
        if p["shared_subsector"]:
            print(f"  {SHORT.get(p['company_a'], '?')} × {SHORT.get(p['company_b'], '?')}  [{p['shared_sector']}/{p['stage_detail']}]")


if __name__ == "__main__":
    main()
