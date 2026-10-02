#!/usr/bin/env python3
"""抽取文本中的法条引用，生成待核验清单。

配合 references/citation-verification-protocol.md 的批量核验模式使用：
先抽取全部引用，再逐条跑三层校验（存在性 / 内容一致性 / 时效性）。

用法：
    python3 scan_citations.py <文件或目录> [更多路径...]
    python3 scan_citations.py --json 案件目录        # 输出 JSON，便于下游处理

说明：
    - 只扫描纯文本类文件（.md/.txt/.markdown），不解析 docx/pdf；
    - 抽取结果是「待核验清单」，不是核验结论——必须逐条回到权威数据库核对；
    - 无《》包裹的法名（如"民法典第577条"）也能识别，但可能有误报，需人工过一眼。
"""

import argparse
import json
import re
import sys
from pathlib import Path

TEXT_SUFFIXES = {".md", ".markdown", ".txt"}

CN_NUM = r"[〇零一二三四五六七八九十百千两0-9]"
ARTICLE = rf"第{CN_NUM}+条(?:之{CN_NUM}+)?"
SUBPART = rf"(?:第{CN_NUM}+款|第{CN_NUM}+项)"
LAW_TITLE = r"《[^》\n]{2,60}》"
BARE_LAW = r"[\u4e00-\u9fff]{2,20}(?:法|典|条例|规定|解释|办法|规则)"

RE_LAW_TITLE = re.compile(LAW_TITLE)
RE_FULL = re.compile(rf"({LAW_TITLE})\s*({ARTICLE})((?:{SUBPART})*)")
RE_BARE = re.compile(rf"({BARE_LAW})\s*({ARTICLE})((?:{SUBPART})*)")
RE_TRAILING_ARTICLE = re.compile(rf"({ARTICLE})((?:{SUBPART})*)")

# 紧跟法名之后、用顿号或连接词并列的条号，视为同一法规的引用
# 注意：不能用 ^ 锚点——这里是用 re.match(pattern, text, pos) 在中间位置起匹配
RE_LIST_SEP = re.compile(r"[、，和及与或]\s*")

# 法名前面常被正则一起吞进来的连接词/介词，逐个剥掉
LEADING_NOISE = (
    "另依据", "依据", "根据", "按照", "依照", "参照", "适用", "适用了",
    "违反了", "符合", "见", "如", "依", "据", "另", "和", "与", "及", "或",
    "以及", "第",
)


def _line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def _snippet(text: str, start: int, end: int, width: int = 30) -> str:
    left = max(0, start - width)
    right = min(len(text), end + width)
    return " ".join(text[left:right].split())


def _norm_law(name: str) -> str:
    return name.strip().strip("《》").replace(" ", "")


def _trim_law(name: str) -> str:
    """剥掉法名前面被误吞的连接词，返回尽量干净的法名。"""
    changed = True
    while changed:
        changed = False
        for noise in LEADING_NOISE:
            if name.startswith(noise) and len(name) > len(noise) + 1:
                name = name[len(noise):]
                changed = True
                break
    return name


def extract(text: str):
    """返回 [(法规, 条号, 起始位置, 结束位置)]，按出现顺序。"""
    found = []
    covered = []

    for m in RE_FULL.finditer(text):
        law = _norm_law(m.group(1))
        found.append((law, m.group(2) + m.group(3), m.start(), m.end()))
        covered.append((m.start(), m.end()))

        # 同一法名后并列的条号："《民事诉讼法》第一百二十二条、第一百二十三条"
        pos = m.end()
        while True:
            sep = RE_LIST_SEP.match(text, pos)
            if not sep:
                break
            art = RE_TRAILING_ARTICLE.match(text, sep.end())
            if not art:
                break
            found.append((law, art.group(1) + art.group(2), art.start(), art.end()))
            covered.append((art.start(), art.end()))
            pos = art.end()

    for m in RE_BARE.finditer(text):
        if any(s <= m.start() < e for s, e in covered):
            continue
        law = _trim_law(_norm_law(m.group(1)))
        # 排除"该法/本法/上述规定"这类指代，避免噪声
        if not law or law[0] in "该本此上述前":
            continue
        found.append((law, m.group(2) + m.group(3), m.start(), m.end()))
        covered.append((m.start(), m.end()))

    found.sort(key=lambda item: item[2])
    return found


def iter_files(paths):
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            for child in sorted(p.rglob("*")):
                if child.is_file() and child.suffix.lower() in TEXT_SUFFIXES:
                    yield child
        elif p.is_file():
            yield p
        else:
            print(f"[warn] 跳过不存在的路径：{raw}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="抽取文本中的法条引用，生成待核验清单")
    parser.add_argument("paths", nargs="+", help="文件或目录")
    parser.add_argument("--json", action="store_true", help="输出 JSON 而不是 Markdown 表格")
    args = parser.parse_args()

    rows = []
    files = list(iter_files(args.paths))
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as exc:
            print(f"[warn] 无法读取 {path}：{exc}", file=sys.stderr)
            continue
        for law, article, start, end in extract(text):
            rows.append(
                {
                    "file": str(path),
                    "line": _line_of(text, start),
                    "law": law,
                    "article": article,
                    "snippet": _snippet(text, start, end),
                }
            )

    if args.json:
        print(json.dumps({"files": len(files), "citations": rows}, ensure_ascii=False, indent=2))
        return 0

    print("## 待核验法条引用清单\n")
    print(f"扫描文件：{len(files)} 个")
    print(f"引用条目：{len(rows)} 条\n")
    if not rows:
        print("（未发现法条引用）")
        return 0

    print("| 序号 | 文件 | 行号 | 法规 | 条号 | 原文片段 |")
    print("|------|------|------|------|------|----------|")
    for i, r in enumerate(rows, 1):
        print(
            f"| {i} | {r['file']} | {r['line']} | {r['law']} | {r['article']} | {r['snippet']} |"
        )
    print()
    print("> 逐条按 `references/citation-verification-protocol.md` 跑三层校验（存在性 / 内容一致性 / 时效性）。")
    print("> 本清单只是候选，不是核验结论；抽取结果可能包含误报或漏报。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
