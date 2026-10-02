#!/usr/bin/env python3
"""把结构化的事件数据渲染成一张克制风格的时间线 SVG。

用法：
    python3 scripts/timeline_svg.py events.json -o 时间线.svg
    python3 scripts/timeline_svg.py events.json --title "某案事实经过" --note "排序规则：同日按材料出现顺序"

输入 JSON 格式：
    {
      "title": "案件大事记",
      "events": [
        {"date": "2023-05-12", "text": "签订《设备买卖合同》",
         "source": "合同原件 p1", "importance": "key"},
        {"date": "2023-08-03", "text": "交付货物，对方签收",
         "source": "送货单 p2", "importance": "normal"}
      ]
    }

importance 取值：key（关键节点）/ important（重要）/ normal（背景），省略按 normal。

设计约束（与 SKILL.md 一致）：
    - 深红只用于关键节点，**全图至多两处**；超过两处会自动降级为琥珀色并在终端提示；
    - 每条事件都要求 source；没有 source 的会打印警告，图上也留空以便人工补；
    - 脚本只做排版，不改写文字；事件文字原样照录。
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

WIDTH = 900
MARGIN = 40
DATE_COL_W = 130
AXIS_X = MARGIN + DATE_COL_W + 10
TEXT_X = AXIS_X + 26
TEXT_MAX_W = WIDTH - MARGIN - TEXT_X
FONT = "PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif"
TEXT_SIZE = 14
LINE_H = 22
CHARS_PER_LINE = 38

COLORS = {
    "key": "#991B1B",
    "important": "#B45309",
    "normal": "#94A3B8",
}


def wrap(text: str, limit: int = CHARS_PER_LINE):
    """按字符数折行（中英文混排的近似处理）。"""
    text = text.strip()
    if not text:
        return [""]
    return [text[i : i + limit] for i in range(0, len(text), limit)]


def load(path: str):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    events = data.get("events")
    if not isinstance(events, list) or not events:
        raise SystemExit("JSON 里没有 events 数组，或数组为空")
    for i, ev in enumerate(events, 1):
        if "date" not in ev or "text" not in ev:
            raise SystemExit(f"第 {i} 条事件缺少 date 或 text 字段")
    return data


def normalize(grid) -> None:
    """关键节点超过两处时降级，避免"满图红"。"""
    key_count = sum(1 for ev in grid["events"] if ev.get("importance") == "key")
    if key_count <= 2:
        return
    for ev in grid["events"]:
        if ev.get("importance") == "key":
            ev["importance"] = "important"
    print(
        f"[warn] 关键节点有 {key_count} 处，超过 2 处，已自动降级为琥珀色："
        "请拆图，或在图下说明共有几处关键节点。",
        file=sys.stderr,
    )


def render(grid, title: str, note: str) -> str:
    events = grid["events"]
    for ev in events:
        if not ev.get("source"):
            print(f"[warn] 事件缺少 source（出处）：{ev['text'][:24]}", file=sys.stderr)

    # 先算高度
    layout = []
    for ev in events:
        lines = wrap(str(ev["text"]))
        row_h = max(52, len(lines) * LINE_H + 20)
        layout.append((ev, lines, row_h))

    header_h = 96
    footer_h = 72
    height = header_h + sum(r[2] for r in layout) + footer_h

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" '
        f'viewBox="0 0 {WIDTH} {height}" font-family="{FONT}">',
        f'<rect width="{WIDTH}" height="{height}" fill="#FFFFFF"/>',
        f'<text x="{MARGIN}" y="52" font-size="22" font-weight="600" fill="#0F172A">'
        f"{escape(title)}</text>",
        f'<line x1="{MARGIN}" y1="72" x2="{WIDTH - MARGIN}" y2="72" stroke="#E2E8F0"/>',
        f'<line x1="{AXIS_X}" y1="{header_h}" x2="{AXIS_X}" y2="{height - footer_h}" '
        f'stroke="#CBD5E1" stroke-width="2"/>',
    ]

    y = header_h
    for ev, lines, row_h in layout:
        center = y + row_h / 2
        importance = ev.get("importance", "normal")
        color = COLORS.get(importance, COLORS["normal"])

        out.append(
            f'<circle cx="{AXIS_X}" cy="{center:.0f}" r="6" fill="{color}"/>'
        )
        out.append(
            f'<text x="{MARGIN}" y="{center + 5:.0f}" font-size="13" fill="#334155">'
            f'{escape(str(ev["date"]))}</text>'
        )

        text_y = y + 28
        for i, line in enumerate(lines):
            weight = "600" if importance == "key" else "400"
            fill = "#0F172A" if importance != "normal" else "#334155"
            out.append(
                f'<text x="{TEXT_X}" y="{text_y + i * LINE_H}" font-size="{TEXT_SIZE}" '
                f'font-weight="{weight}" fill="{fill}">{escape(line)}</text>'
            )

        source = str(ev.get("source", "")).strip()
        src_y = text_y + len(lines) * LINE_H + 2
        if source:
            out.append(
                f'<text x="{TEXT_X}" y="{src_y}" font-size="11" fill="#94A3B8">'
                f"来源：{escape(source)}</text>"
            )
        y += row_h

    legend_y = height - 46
    out.append(
        f'<text x="{MARGIN}" y="{legend_y}" font-size="11" fill="#64748B">'
        f"图例：<tspan fill=\"{COLORS['key']}\">●</tspan> 关键节点 · "
        f"<tspan fill=\"{COLORS['important']}\">●</tspan> 重要 · "
        f"<tspan fill=\"{COLORS['normal']}\">●</tspan> 背景"
        f"　|　生成日期：{date.today().isoformat()}</text>"
    )
    if note:
        out.append(
            f'<text x="{MARGIN}" y="{legend_y + 18}" font-size="11" fill="#64748B">'
            f"{escape(note)}</text>"
        )
    out.append("</svg>")
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description="渲染时间线 SVG")
    parser.add_argument("input", help="事件数据 JSON 文件")
    parser.add_argument("-o", "--output", help="输出 SVG 路径（默认同名 .svg）")
    parser.add_argument("--title", help="图标题（默认取 JSON 里的 title）")
    parser.add_argument("--note", default="", help="图下补充说明，例如排序规则")
    args = parser.parse_args()

    grid = load(args.input)
    normalize(grid)
    title = args.title or grid.get("title") or "案件大事记"
    svg = render(grid, title, args.note)

    out_path = Path(args.output) if args.output else Path(args.input).with_suffix(".svg")
    out_path.write_text(svg, encoding="utf-8")
    print(f"已生成：{out_path}（{len(grid['events'])} 条事件）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
