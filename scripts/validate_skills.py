#!/usr/bin/env python3
"""Validate Hermes skill frontmatter across the repo.

For every directory under skills/ this checks:
  1. SKILL.md exists
  2. Frontmatter (text between the leading --- markers) is valid YAML
  3. Required fields present: name, description, version
  4. name matches the directory name
  5. description is non-trivial (>= 20 chars after stripping)
  6. version is semver-like (X.Y.Z)

Exit code 0 if everything passes, 1 otherwise. Run from the repo root:

    python scripts/validate_skills.py
"""
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = ROOT / "skills"
REQUIRED = ("name", "description", "version")
MIN_DESC_LEN = 20


def parse_frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*", text, re.S)
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1))
    except yaml.YAMLError as exc:
        return exc


def main():
    errors = []
    paths = sorted(SKILLS_ROOT.glob("*/*/SKILL.md"))
    if not paths:
        errors.append(f"no SKILL.md found under {SKILLS_ROOT}")

    for path in paths:
        dirname = path.parent.name
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        if not isinstance(fm, dict):
            errors.append(f"{path}: frontmatter missing or invalid YAML")
            continue

        for field in REQUIRED:
            if field not in fm or fm[field] in (None, ""):
                errors.append(f"{path}: missing required field '{field}'")

        name = fm.get("name")
        if name and name != dirname:
            errors.append(f"{path}: name '{name}' != directory '{dirname}'")

        desc = fm.get("description", "")
        if isinstance(desc, str) and len(desc.strip()) < MIN_DESC_LEN:
            errors.append(
                f"{path}: description too short "
                f"({len(desc.strip())} chars, min {MIN_DESC_LEN})"
            )

        ver = fm.get("version")
        if ver is not None and not re.match(r"^\d+\.\d+\.\d+$", str(ver)):
            errors.append(f"{path}: version '{ver}' is not semver (X.Y.Z)")

    total = len(paths)
    print(f"[skill-check] validated {total} skills")
    if errors:
        for e in errors:
            print(f"  FAIL  {e}")
        print(f"[skill-check] {len(errors)} error(s)")
        return 1
    print("[skill-check] all skills valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
