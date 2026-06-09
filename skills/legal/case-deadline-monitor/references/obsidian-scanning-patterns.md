# Obsidian案件笔记日期提取模式

## 实际扫描结果（2026-06-08）
- 扫描范围：`法律知识库/01-案件笔记/` 下33个.md文件
- 提取日期条目：337条，去重93个唯一日期
- 主要案件：华都琥珀诉双烨环保合同纠纷

## 日期提取正则模式

```python
import re

DEADLINE_PATTERNS = [
    # 开庭日期
    (r'开庭[日期时间]*[：:]\s*(\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?)', '开庭'),
    # 举证期限
    (r'举证[期限截止]*[：:]\s*(\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?)', '举证期限'),
    # 上诉期限
    (r'上诉[期限截止]*[：:]\s*(\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?)', '上诉期限'),
    # 执行期限
    (r'执行[申请期限截止]*[：:]\s*(\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?)', '执行期限'),
    # 保全到期
    (r'保全[到期期限]*[：:]\s*(\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?)', '保全到期'),
    # 鉴定期限
    (r'鉴定[申请期限]*[：:]\s*(\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?)', '鉴定期限'),
    # 通用日期（立案、合同签订等）
    (r'(\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?)', '通用日期'),
]
```

## Obsidian笔记中的实际格式

案件笔记中的日期通常出现在以下上下文中：
- `立案日 2026-04-10`
- `合同签订日 2022-12-14`
- `答辩状提交（立案后15日）`
- `举证期限（立案后约30日）`
- `质保期推算截止（货到后30个月，约2025-10）`

## 日期格式兼容

```python
def normalize_date(date_str):
    """统一日期格式为 YYYY-MM-DD"""
    date_str = date_str.replace('年','-').replace('月','-').replace('日','')
    return date_str.strip()
```

## Apple Calendar创建事件

```python
def create_calendar_event(title, date_str, notes="", calendar_name="工作"):
    """通过AppleScript创建Apple Calendar事件"""
    script = f'''
    tell application "Calendar"
        tell calendar "{calendar_name}"
            set newEvent to make new event with properties {{
                summary:"{title}",
                start date:date "{date_str} 09:00:00",
                end date:date "{date_str} 10:00:00",
                description:"{notes}"
            }}
            tell newEvent
                make new sound alarm at date ((start date) - 1440 * minutes)
            end tell
        end tell
    end tell
    '''
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    return result.returncode == 0
```

⚠️ Apple Calendar首次使用需授权AppleScript控制权限。
