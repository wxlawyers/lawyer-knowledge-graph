#!/usr/bin/env python3
"""为技能补充 argument-hint（命令参数提示）。

作用：支持斜杠命令的客户端（Claude Code / Cowork 等）会用它提示参数格式，
让技能可以「带参数调用」，例如 `/contract-review 合同.docx --side=卖方`。
不支持该字段的客户端会忽略它，不影响技能原有行为。

本脚本是各技能 argument-hint 的**唯一来源**（映射表在下面），幂等可重复运行：

    python3 scripts/add_argument_hint.py            # 写入
    python3 scripts/add_argument_hint.py --check    # 只检查，不写入

新增技能时，在 HINTS 里补一条再运行即可。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = ROOT / "skills"

HINTS = {
    "bankruptcy-liquidation": "[企业名称或案件名]",
    "business-development": "[选题或渠道]",
    "case-deadline-monitor": "[案件名称] [--days=30]",
    "case-management": "[案件名称]",
    "chinese-legal-practice": "[执业领域]",
    "claude-code-sync": "[目标平台]",
    "client-communication": "[案件名称] [--type=服务计划书|工作通报|决策辅助清单|庭审简报]",
    "compensation-calculator": "[省份] [伤残等级或月工资] [--type=交通|工伤|劳动|利息]",
    "contract-review": "[合同文件路径] [--side=买方|卖方]",
    "court-trial-realtime": "[关键词或证据照片]",
    "cpa-accounting": "[问题或材料路径]",
    "cta-tax": "[问题或材料路径]",
    "evidence-organization": "[证据材料路径]",
    "foreign-related-legal-practice": "[法域或问题]",
    "forensic-accounting": "[鉴定事项]",
    "knowledge-accumulation": "[案件或材料名称]",
    "knowledge-base-enrichment": "[知识库路径或领域]",
    "labor-compensation": "[省份] [月工资] [工作年限]",
    "lawsuit-filing": "[案由] [标的额]",
    "lawyer-douyin-livestream": "[直播主题]",
    "lawyer-letter": "[函件类型] [对方名称]",
    "lawyer-website-development": "[页面或模块]",
    "lawyer-wechat-article": "[文章主题]",
    "legal-analysis-pitfalls": "[材料路径或问题]",
    "legal-document-drafting": "[文书类型] [案件名称]",
    "legal-research": "[检索问题或法条]",
    "litigation-case-analysis": "[案件名称或材料路径]",
    "ma-restructuring": "[交易名称或目标公司]",
    "obsidian-knowledge-pipeline": "[--type=daily|weekly]",
    "preservation-execution": "[保全|执行] [标的或案号]",
    "real-estate-transaction": "[交易类型或标的]",
    "securities-compliance": "[事项或材料路径]",
    "statute-limitation": "[债权基础与起算事实]",
    "trial-preparation": "[案件名称] [--output=庭审记录]",
    "trial-response": "[案件名称]",
    "vibe-coding-legal-tools": "[工具需求]",
    "wechat-lawyer-article": "[文章主题]",
    "wechat-legal-article": "[文章主题]",
}

RE_DESC = re.compile(r"^description:", re.M)
RE_HINT = re.compile(r"^argument-hint:.*$", re.M)
BLOCK_MARKERS = (">-", ">", "|", "|-", ">+", "|+" )


def split_frontmatter(text: str):
    """返回 (frontmatter, rest)。

    frontmatter 是开头 --- 与结尾 --- 之间的内容（不含两边的分隔行）；
    rest 从结尾 --- 之前的那个换行开始，原样保留，重建时直接拼回，
    避免手工拼接把换行弄丢。
    """
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    fm_start = text.find("\n") + 1  # 跳过开头的 --- 行
    return text[fm_start:end], text[end:]


def hint_line_position(fm_lines, desc_index: int) -> int:
    """返回应插入 argument-hint 的行号（description 字段结束之后的下一行）。"""
    value = fm_lines[desc_index].split(":", 1)[1].strip()
    if value not in BLOCK_MARKERS:
        return desc_index + 1
    idx = desc_index + 1
    while idx < len(fm_lines):
        line = fm_lines[idx]
        if line.strip() == "" or line.startswith((" ", "\t")):
            idx += 1
            continue
        break
    return idx


def update_frontmatter(fm: str, hint: str) -> str:
    lines = fm.split("\n")
    new_line = f'argument-hint: "{hint}"'

    for i, line in enumerate(lines):
        if line.startswith("argument-hint:"):
            if line == new_line:
                return fm
            lines[i] = new_line
            return "\n".join(lines)

    desc_index = next((i for i, l in enumerate(lines) if l.startswith("description:")), None)
    if desc_index is None:
        raise ValueError("frontmatter 里没有 description 字段")
    insert_at = hint_line_position(lines, desc_index)
    lines.insert(insert_at, new_line)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="为技能补充 argument-hint")
    parser.add_argument("--check", action="store_true", help="只检查，不写入")
    args = parser.parse_args()

    pending, failures = [], []
    for name, hint in sorted(HINTS.items()):
        matches = list(SKILLS_ROOT.glob(f"*/{name}/SKILL.md"))
        if not matches:
            failures.append(f"{name}：找不到 SKILL.md")
            continue
        path = matches[0]
        text = path.read_text(encoding="utf-8")
        fm, rest = split_frontmatter(text)
        if fm is None:
            failures.append(f"{name}：frontmatter 格式异常")
            continue
        updated_fm = update_frontmatter(fm, hint)
        updated = f"---\n{updated_fm}{rest}"
        if updated != text:
            pending.append(path)
            if not args.check:
                path.write_text(updated, encoding="utf-8")

    if args.check:
        if pending:
            print("[argument-hint] 以下技能需要更新：", file=sys.stderr)
            for p in pending:
                print(f"  - {p.relative_to(ROOT)}", file=sys.stderr)
            return 1
        print(f"[argument-hint] {len(HINTS)} 个技能已是最新")
        return 0

    if pending:
        print(f"[argument-hint] 已更新 {len(pending)} 个技能")
        for p in pending:
            print(f"  - {p.relative_to(ROOT)}")
    else:
        print(f"[argument-hint] {len(HINTS)} 个技能已是最新，无需改动")

    if failures:
        for f in failures:
            print(f"[error] {f}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
