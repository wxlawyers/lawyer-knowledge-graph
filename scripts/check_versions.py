#!/usr/bin/env python3
"""检查「技能内容改了、版本号没升」的情况。

比较当前工作区（或指定提交）与一个基线提交：
    如果某个技能目录下的内容有变更，但该技能 SKILL.md 的 version 没有提升，
    就报错退出。规则见 VERSIONING.md。

用法：
    python3 scripts/check_versions.py                 # 与上一个提交比较（HEAD~1）
    python3 scripts/check_versions.py --base origin/master
    python3 scripts/check_versions.py --base HEAD~3
    python3 scripts/check_versions.py --all           # 检查所有技能版本格式

在 CI 中由 .github/workflows/skill-check.yml 调用。提交信息包含
`[skip version-check]` 时跳过。
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION_RE = re.compile(r"^version:\s*(\d+)\.(\d+)\.(\d+)\s*$", re.M)


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} 失败：{result.stderr.strip()}")
    return result.stdout


def parse_version(text: str):
    m = VERSION_RE.search(text)
    if not m:
        return None
    return tuple(int(x) for x in m.groups())


def version_at(rev: str, skill: str) -> str | None:
    for suffix in ("SKILL.md",):
        path = f"skills/*/{skill}/{suffix}"
        try:
            out = git("ls-tree", "-r", "--name-only", rev, "--", f"skills/")
        except SystemExit:
            return None
        for line in out.splitlines():
            if line.endswith(f"/{skill}/{suffix}"):
                try:
                    return git("show", f"{rev}:{line}")
                except SystemExit:
                    return None
        return None
    return None


def main():
    parser = argparse.ArgumentParser(description="检查技能版本号是否随内容变更提升")
    parser.add_argument("--base", default="HEAD~1", help="基线提交，默认 HEAD~1")
    parser.add_argument("--all", action="store_true", help="只校验所有技能版本格式")
    args = parser.parse_args()

    if args.all:
        bad = []
        for path in sorted(ROOT.glob("skills/*/*/SKILL.md")):
            if not VERSION_RE.search(path.read_text(encoding="utf-8")):
                bad.append(str(path.relative_to(ROOT)))
        if bad:
            print("[version-check] 以下技能缺少合法 version 字段：", file=sys.stderr)
            for b in bad:
                print(f"  - {b}", file=sys.stderr)
            return 1
        print("[version-check] 全部技能版本格式正常")
        return 0

    try:
        head_message = git("log", "-1", "--format=%B")
    except SystemExit:
        head_message = ""
    if "[skip version-check]" in head_message:
        print("[version-check] 提交信息包含 [skip version-check]，跳过")
        return 0

    # 用两点比较：把基线提交与当前工作区（含未提交改动）对比，
    # 这样本地提交前自检和 CI 都能覆盖。
    try:
        changed = git("diff", "--name-only", args.base, "--", "skills/")
    except SystemExit as exc:
        print(f"[version-check] 无法比较基线 {args.base}（{exc}），跳过检查")
        return 0

    touched = set()
    for line in changed.splitlines():
        parts = line.strip().split("/")
        if len(parts) >= 3 and parts[0] == "skills":
            touched.add(parts[2])

    if not touched:
        print("[version-check] skills/ 下没有变更")
        return 0

    problems = []
    for skill in sorted(touched):
        current_path = next(ROOT.glob(f"skills/*/{skill}/SKILL.md"), None)
        if current_path is None:
            continue  # 技能被删除，不需要升版本
        current = parse_version(current_path.read_text(encoding="utf-8"))
        previous_text = version_at(args.base, skill)
        if previous_text is None:
            continue  # 新增技能，无需比较
        previous = parse_version(previous_text)
        if previous is None:
            continue
        if current is None:
            problems.append(f"{skill}：SKILL.md 缺少合法 version 字段")
        elif current <= previous:
            problems.append(
                f"{skill}：内容有变更，但版本未提升（仍是 {'.'.join(map(str, current))}）"
            )

    if problems:
        print("[version-check] 发现问题：", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        print(
            "\n处理方式：python3 scripts/bump_version.py <技能名> --level minor"
            "\n规则见 VERSIONING.md；确需跳过时在提交信息里写 [skip version-check]",
            file=sys.stderr,
        )
        return 1

    print(f"[version-check] {len(touched)} 个变更技能版本正常")
    return 0


if __name__ == "__main__":
    sys.exit(main())
