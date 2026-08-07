#!/usr/bin/env python3
"""Run skill trigger evals.

Each case in evals/cases/*.json describes a skill and a set of natural-language
phrases that should (or should not) activate it. The runner checks whether the
phrases still overlap the skill's own frontmatter (description + examples), so
a rewrite of the skill that drifts out of its domain fails loudly in CI.

Semantics:
  - every `triggers` phrase must share >= 1 significant token with the skill
  - every `negative` phrase must share 0 significant tokens

Significant tokens = CJK bigrams + ASCII words (>= 2 chars), minus generic
connective bigrams (stopwords). Run from the repo root:

    python evals/run_evals.py
"""
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
CASES = Path(__file__).resolve().parent / "cases"

STOPWORDS = {
    "帮我", "一下", "一个", "这份", "这个", "那个", "什么", "怎么", "为什么",
    "如何", "请问", "需要", "可以", "给我", "我的", "我想", "我要", "请帮",
    "的话", "那么", "这样", "那样", "有没", "有没有", "一份", "帮我",
    "我需要", "应该是", "是不是", "能不能", "可不可以", "您能", "帮我算",
}

CJK = re.compile(r"[一-鿿]")
ASCII = re.compile(r"[a-zA-Z0-9]+")


def tokens(text):
    out = set()
    cjk = "".join(CJK.findall(text))
    out.update(cjk[i : i + 2] for i in range(len(cjk) - 1))
    out.update(w.lower() for w in ASCII.findall(text) if len(w) >= 2)
    return out - STOPWORDS


def skill_reference(skill_dir):
    path = next(SKILLS.glob(f"*/{skill_dir}/SKILL.md"), None)
    if path is None:
        return None
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*", text, re.S)
    fm = yaml.safe_load(m.group(1)) if m else {}
    parts = []
    for key in ("description", "name"):
        val = fm.get(key)
        if isinstance(val, str):
            parts.append(val)
    examples = fm.get("examples", [])
    if isinstance(examples, list):
        parts.extend(str(e) for e in examples if isinstance(e, str))
    return " ".join(parts)


def check_examples_drift():
    """Every example in every skill must overlap its own description."""
    failures = []
    checked = 0
    for path in sorted(SKILLS.glob("*/*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        m = re.match(r"^---\s*\n(.*?)\n---\s*", text, re.S)
        fm = yaml.safe_load(m.group(1)) if m else {}
        desc = fm.get("description")
        examples = fm.get("examples", [])
        if not desc or not isinstance(examples, list) or not examples:
            continue
        desc_tokens = tokens(str(desc))
        for ex in examples:
            ex_str = str(ex)
            checked += 1
            if not (desc_tokens & tokens(ex_str)):
                failures.append(
                    f"example '{ex_str}' ({path.parent.name}) has no overlap with its description"
                )
    return failures, checked


def main():
    failures = []
    total_triggers = total_negatives = 0

    drift_failures, drift_checked = check_examples_drift()
    failures.extend(drift_failures)

    case_files = sorted(CASES.glob("*.json"))
    if not case_files:
        failures.append(f"no case files found under {CASES}")

    for case_file in case_files:
        case = json.loads(case_file.read_text(encoding="utf-8"))
        skill = case["skill"]
        ref = skill_reference(skill)
        if ref is None:
            failures.append(f"{case_file.name}: skill '{skill}' not found")
            continue
        ref_tokens = tokens(ref)
        if not ref_tokens:
            failures.append(
                f"{case_file.name}: skill '{skill}' reference yields no tokens"
            )
            continue

        for phrase in case.get("triggers", []):
            total_triggers += 1
            overlap = ref_tokens & tokens(phrase)
            if not overlap:
                failures.append(
                    f"{case_file.name}: trigger '{phrase}' does not overlap skill '{skill}'"
                )

        for phrase in case.get("negative", []):
            total_negatives += 1
            overlap = ref_tokens & tokens(phrase)
            if overlap:
                failures.append(
                    f"{case_file.name}: negative '{phrase}' overlaps skill "
                    f"'{skill}' ({sorted(overlap)})"
                )

    print(
        f"[evals] {len(case_files)} cases, {total_triggers} triggers, "
        f"{total_negatives} negatives, {drift_checked} example-drift checks"
    )
    if failures:
        for f in failures:
            print(f"  FAIL  {f}")
        print(f"[evals] {len(failures)} failure(s)")
        return 1
    print("[evals] all cases pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
