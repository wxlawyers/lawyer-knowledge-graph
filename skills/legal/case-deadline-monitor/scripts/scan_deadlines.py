#!/usr/bin/env python3
"""
案件期限扫描脚本（已验证可用）
扫描Obsidian案件笔记，提取所有日期/期限信息
用法: python3 scan_deadlines.py [--json output.json]
"""
import os
import re
import json
import sys
from datetime import datetime, timedelta

VAULT_PATH = "/Users/yuzhenghong/Library/Mobile Documents/iCloud~md~obsidian/Documents/法律知识库"
CASE_DIR = os.path.join(VAULT_PATH, "01-案件笔记")

def parse_date(date_str):
    """解析多种中文日期格式"""
    date_str = date_str.replace('年','-').replace('月','-').replace('日','').strip()
    for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d']:
        try:
            return datetime.strptime(date_str, fmt)
        except:
            continue
    return None

def scan_case_files():
    """扫描所有案件笔记，提取期限信息"""
    deadlines = []
    if not os.path.exists(CASE_DIR):
        print(f"案件笔记目录不存在: {CASE_DIR}")
        return deadlines

    date_patterns = [
        (r'开庭[日期时间]*[：:]\s*(\d{4}[-年/\.]\d{1,2}[-月/\.]\d{1,2}[日]?)', '开庭'),
        (r'举证[期限截止到]*[：:]\s*(\d{4}[-年/\.]\d{1,2}[-月/\.]\d{1,2}[日]?)', '举证期限'),
        (r'上诉[期限截止到]*[：:]\s*(\d{4}[-年/\.]\d{1,2}[-月/\.]\d{1,2}[日]?)', '上诉期限'),
        (r'执行[申请期限截止到]*[：:]\s*(\d{4}[-年/\.]\d{1,2}[-月/\.]\d{1,2}[日]?)', '执行期限'),
        (r'保全[到期期限截止]*[：:]\s*(\d{4}[-年/\.]\d{1,2}[-月/\.]\d{1,2}[日]?)', '保全到期'),
        (r'鉴定[申请期限截止]*[：:]\s*(\d{4}[-年/\.]\d{1,2}[-月/\.]\d{1,2}[日]?)', '鉴定期限'),
        (r'立案[日期时间]*[：:]\s*(\d{4}[-年/\.]\d{1,2}[-月/\.]\d{1,2}[日]?)', '立案日期'),
        (r'判决[日期送达]*[：:]\s*(\d{4}[-年/\.]\d{1,2}[-月/\.]\d{1,2}[日]?)', '判决日期'),
        (r'到期[日期]*[：:]\s*(\d{4}[-年/\.]\d{1,2}[-月/\.]\d{1,2}[日]?)', '到期日期'),
    ]

    for f in os.listdir(CASE_DIR):
        if not f.endswith('.md'):
            continue
        filepath = os.path.join(CASE_DIR, f)
        with open(filepath, 'r', encoding='utf-8') as fh:
            content = fh.read()

        # 提取案号
        case_match = re.search(r'案号[：:]\s*(.+)', content)
        case_number = case_match.group(1).strip() if case_match else f.replace('.md','')

        for pattern, dtype in date_patterns:
            matches = re.findall(pattern, content)
            for m in matches:
                deadline_date = parse_date(m)
                if deadline_date:
                    deadlines.append({
                        'case': case_number,
                        'type': dtype,
                        'date': deadline_date.strftime('%Y-%m-%d'),
                        'days_from_now': (deadline_date - datetime.now()).days,
                        'file': os.path.basename(filepath)
                    })

    return deadlines

def filter_upcoming(deadlines, days=30):
    """筛选未来N天内的期限"""
    today = datetime.now()
    upcoming = []
    for d in deadlines:
        try:
            deadline_date = datetime.strptime(d['date'], '%Y-%m-%d')
            delta = (deadline_date - today).days
            if 0 <= delta <= days:
                d['days_remaining'] = delta
                upcoming.append(d)
        except:
            pass
    return sorted(upcoming, key=lambda x: x.get('days_remaining', 999))

if __name__ == "__main__":
    deadlines = scan_case_files()
    print(f"扫描完成：{len(deadlines)} 条日期信息")

    upcoming = filter_upcoming(deadlines, days=30)
    if upcoming:
        print(f"\n⚠️ 未来30天内期限：")
        for d in upcoming:
            print(f"  [{d['type']}] {d['case']} - {d['date']} (还剩{d['days_remaining']}天)")
    else:
        print("\n✅ 未来30天内无到期期限")

    if '--json' in sys.argv:
        idx = sys.argv.index('--json')
        output = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else 'deadlines.json'
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(deadlines, f, ensure_ascii=False, indent=2)
        print(f"\n结果已保存: {output}")
