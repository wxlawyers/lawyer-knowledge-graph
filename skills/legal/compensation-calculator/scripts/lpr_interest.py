#!/usr/bin/env python3
"""LPR 分段利息计算器。

用途：按一年期 LPR 的分段变动，计算资金占用利息 / 逾期利息，输出可直接用于
起诉状、代理词或立案材料的计算表。

重要说明：
    - 本脚本**不内置利率数据**。LPR 由全国银行间同业拆借中心受权公布（每月 20 日，
      遇节假日顺延），必须由使用者从权威渠道取得后填入利率表，不得凭记忆填写。
    - 天数口径默认「算头不算尾」（即 end - start），可用 --inclusive 改为含尾日。
    - 结果仅为计算草稿，须由律师复核后使用。

用法：
    python3 lpr_interest.py --principal 1000000 --start 2023-06-01 --end 2025-03-15 \\
        --rates rates.json
    python3 lpr_interest.py ... --json          # 输出 JSON

利率表 rates.json 格式（每段起始日 + 该日起施行的年利率，百分数）：
    [
      {"from": "2023-06-20", "rate": 3.55},
      {"from": "2023-08-21", "rate": 3.45},
      {"from": "2024-07-22", "rate": 3.35}
    ]
第一段的 from 应不晚于起算日；最后一段持续到结束日。
"""

import argparse
import json
import sys
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


def parse_date(text: str) -> date:
    try:
        return date.fromisoformat(text)
    except ValueError:
        raise SystemExit(f"日期格式应为 YYYY-MM-DD，收到：{text}")


def load_rates(path: str):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise SystemExit("利率表必须是非空数组")
    parsed = []
    for item in data:
        try:
            parsed.append((parse_date(item["from"]), Decimal(str(item["rate"]))))
        except (KeyError, TypeError):
            raise SystemExit(f"利率表条目格式错误：{item}")
    parsed.sort(key=lambda pair: pair[0])
    return parsed


def build_segments(start: date, end: date, rates):
    """把 [start, end] 按利率生效日切段，返回 [(段起, 段止, 年利率)]。"""
    if end <= start:
        raise SystemExit("结束日期必须晚于开始日期")

    marks = [start]
    for effective, _ in rates:
        if start < effective < end:
            marks.append(effective)
    marks.append(end)

    segments = []
    for i in range(len(marks) - 1):
        seg_start, seg_end = marks[i], marks[i + 1]
        rate = None
        for effective, value in rates:
            if effective <= seg_start:
                rate = value
            else:
                break
        if rate is None:
            raise SystemExit(
                f"{seg_start} 之前没有可用利率——请把利率表第一段的 from 设到起算日或更早"
            )
        segments.append((seg_start, seg_end, rate))
    return segments


def money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def main():
    parser = argparse.ArgumentParser(description="LPR 分段利息计算器")
    parser.add_argument("--principal", required=True, help="本金（元）")
    parser.add_argument("--start", required=True, help="起算日 YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="截止日 YYYY-MM-DD")
    parser.add_argument("--rates", required=True, help="利率表 JSON 文件路径")
    parser.add_argument("--annual-days", type=int, default=365, help="年天数基数，默认 365")
    parser.add_argument("--inclusive", action="store_true", help="天数含截止日（默认算头不算尾）")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    principal = Decimal(str(args.principal))
    start, end = parse_date(args.start), parse_date(args.end)
    rates = load_rates(args.rates)
    segments = build_segments(start, end, rates)

    rows = []
    total = Decimal("0")
    for seg_start, seg_end, rate in segments:
        days = (seg_end - seg_start).days + (1 if args.inclusive else 0)
        if days <= 0:
            continue
        interest = principal * (rate / Decimal("100")) * Decimal(days) / Decimal(args.annual_days)
        total += interest
        rows.append(
            {
                "from": seg_start.isoformat(),
                "to": seg_end.isoformat(),
                "days": days,
                "rate": str(rate),
                "interest": str(money(interest)),
            }
        )

    end_for_days = end + timedelta(days=1) if args.inclusive else end
    total_days = (end_for_days - start).days

    if args.json:
        print(
            json.dumps(
                {
                    "principal": str(principal),
                    "start": start.isoformat(),
                    "end": end.isoformat(),
                    "annual_days": args.annual_days,
                    "inclusive": args.inclusive,
                    "total_days": total_days,
                    "total_interest": str(money(total)),
                    "segments": rows,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    print(f"本金：{money(principal)} 元")
    print(f"计息期间：{start} 至 {end}（共 {total_days} 天，年基数 {args.annual_days} 天）")
    print()
    print("| 起始日 | 截止日 | 天数 | 年利率(%) | 利息(元) |")
    print("|--------|--------|------|-----------|----------|")
    for r in rows:
        print(f"| {r['from']} | {r['to']} | {r['days']} | {r['rate']} | {r['interest']} |")
    print()
    print(f"**利息合计：{money(total)} 元**（本金 + 利息 = {money(principal + total)} 元）")
    print()
    print("> 利率须来自全国银行间同业拆借中心公布的 LPR，并保留公布日期与来源记录。")
    print("> 本表为计算草稿，正式使用前请复核天数口径与利率分段。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
