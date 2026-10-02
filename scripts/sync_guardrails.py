#!/usr/bin/env python3
"""把通用护栏同步到所有技能。

单一来源：skills/legal/_shared/guardrails.md 里 <!-- BEGIN:guardrails --> 与
<!-- END:guardrails --> 之间的内容。

同步动作：把每个 skills/*/*/SKILL.md 末尾的「事实核验原则」一节替换为该内容；
原本没有这一节的技能，会追加到文件末尾。

用法：
    python3 scripts/sync_guardrails.py           # 同步
    python3 scripts/sync_guardrails.py --check   # 只检查，不写入（不一致时退出码 1）
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = ROOT / "skills"
SHARED = SKILLS_ROOT / "legal" / "_shared" / "guardrails.md"

BEGIN = "<!-- BEGIN:guardrails -->"
END = "<!-- END:guardrails -->"
HEADING = "## 事实核验原则"


def load_block() -> str:
    text = SHARED.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        raise SystemExit(f"单一来源文件缺少 {BEGIN} / {END} 标记：{SHARED}")
    block = text.split(BEGIN, 1)[1].split(END, 1)[0]
    return block.strip("\n")


def apply_block(text: str, block: str) -> str:
    if HEADING in text:
        # 该节目前都位于文件末尾；如有例外，也一并截断重写
        head = text.split(HEADING, 1)[0].rstrip("\n")
        return f"{head}\n\n{block}\n"
    return f"{text.rstrip(chr(10))}\n\n{block}\n"


def main():
    parser = argparse.ArgumentParser(description="同步通用护栏到所有技能")
    parser.add_argument("--check", action="store_true", help="只检查是否一致，不写入")
    args = parser.parse_args()

    block = load_block()
    targets = sorted(SKILLS_ROOT.glob("*/*/SKILL.md"))
    if not targets:
        raise SystemExit("没有找到任何 SKILL.md")

    changed, out_of_sync = [], []
    for path in targets:
        original = path.read_text(encoding="utf-8")
        updated = apply_block(original, block)
        if updated != original:
            rel = path.relative_to(ROOT)
            changed.append(str(rel))
            if args.check:
                out_of_sync.append(str(rel))
            else:
                path.write_text(updated, encoding="utf-8")

    if args.check:
        if out_of_sync:
            print("[guardrails] 以下技能与单一来源不一致：", file=sys.stderr)
            for item in out_of_sync:
                print(f"  - {item}", file=sys.stderr)
            print("\n运行 python3 scripts/sync_guardrails.py 修复。", file=sys.stderr)
            return 1
        print(f"[guardrails] {len(targets)} 个技能与单一来源一致")
        return 0

    if changed:
        print(f"[guardrails] 已同步 {len(changed)} 个技能：")
        for item in changed:
            print(f"  - {item}")
    else:
        print(f"[guardrails] {len(targets)} 个技能已是最新，无需改动")
    return 0


if __name__ == "__main__":
    sys.exit(main())
