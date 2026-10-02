#!/usr/bin/env python3
"""按语义化版本规则提升技能的 version 字段。

用法：
    python3 scripts/bump_version.py <技能名> [更多技能名...] --level minor
    python3 scripts/bump_version.py legal-research --level minor --dry-run
    python3 scripts/bump_version.py --list          # 列出所有技能及当前版本

规则见 VERSIONING.md：
    major —— 重命名/拆分/合并/删除，或适用范围实质变化
    minor —— 新增步骤、模块、参考文件、脚本，或修订流程与口径
    patch —— 错别字、格式、失效链接等不影响用法的修正
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = ROOT / "skills"
VERSION_RE = re.compile(r"^version:\s*(\d+)\.(\d+)\.(\d+)\s*$", re.M)


def find_skill(name: str) -> Path | None:
    matches = list(SKILLS_ROOT.glob(f"*/{name}/SKILL.md"))
    if not matches:
        return None
    return matches[0]


def bump(current: str, level: str) -> str:
    major, minor, patch = (int(x) for x in current.split("."))
    if level == "major":
        return f"{major + 1}.0.0"
    if level == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def list_skills():
    rows = []
    for path in sorted(SKILLS_ROOT.glob("*/*/SKILL.md")):
        m = VERSION_RE.search(path.read_text(encoding="utf-8"))
        rows.append((path.parent.name, m.group(0).split(":", 1)[1].strip() if m else "（缺失）"))
    width = max((len(name) for name, _ in rows), default=10)
    for name, version in rows:
        print(f"{name:<{width}}  {version}")


def main():
    parser = argparse.ArgumentParser(description="提升技能 version 字段")
    parser.add_argument("skills", nargs="*", help="技能名（目录名）")
    parser.add_argument("--level", choices=["major", "minor", "patch"], default="minor")
    parser.add_argument("--dry-run", action="store_true", help="只显示结果，不写入")
    parser.add_argument("--list", action="store_true", help="列出所有技能及当前版本")
    args = parser.parse_args()

    if args.list:
        list_skills()
        return 0

    if not args.skills:
        parser.error("至少指定一个技能名，或用 --list 查看全部技能")

    failures = []
    for name in args.skills:
        path = find_skill(name)
        if path is None:
            failures.append(f"找不到技能：{name}")
            continue

        text = path.read_text(encoding="utf-8")
        m = VERSION_RE.search(text)
        if not m:
            failures.append(f"{name}：SKILL.md 里没有合法的 version 字段")
            continue

        current = m.group(0).split(":", 1)[1].strip()
        new = bump(current, args.level)
        if args.dry_run:
            print(f"[dry-run] {name}: {current} -> {new}")
            continue

        updated = VERSION_RE.sub(f"version: {new}", text, count=1)
        path.write_text(updated, encoding="utf-8")
        print(f"{name}: {current} -> {new}")

    if failures:
        for f in failures:
            print(f"[error] {f}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
