---
name: case-deadline-monitor
description: "案件期限自动监控 — 从Obsidian提取案件信息，自动创建Apple Calendar提醒，监控开庭/举证/上诉/执行期限。"
version: 1.0.0
author: 余正洪律师
platforms: [macos]
metadata:
  hermes:
    tags: [calendar, deadline, case-management, apple-calendar, legal]
---

# 案件期限自动监控技能

从Obsidian法律知识库提取案件关键期限，自动同步到Apple Calendar，确保律师不错过任何重要时间节点。

## 适用场景

- 开庭日期提醒
- 举证期限提醒
- 上诉期限提醒（判决送达后15天）
- 执行申请期限（判决生效后2年）
- 鉴定申请期限
- 财产保全到期提醒
- 合同到期提醒
- 诉讼时效提醒

## 工具链

| 工具 | 用途 | 说明 |
|------|------|------|
| Apple Calendar | 日历提醒 | macOS自带，AppleScript控制 |
| Obsidian | 案件信息源 | 法律知识库/01-案件笔记/ |
| osascript | AppleScript执行 | macOS自带 |
| Hermes cronjob | 定时扫描 | 每日自动检查 |

### 2026-06-08 验证结果

- 扫描 `01-案件笔记/` 目录下 **33个.md文件**
- 提取 **337条日期条目**，去重后 **93个唯一日期**
- 识别出的期限类型：开庭日期、举证期限、答辩期限、质保期、合同签订日、立案日
- 输出JSON格式扫描结果（85KB）
- Apple Calendar可通过 `osascript` 控制，无需安装额外工具

## 期限类型与法定时间

| 期限类型 | 法定时间 | 法律依据 |
|----------|----------|----------|
| 民事上诉期 | 判决送达后15天 | 《民事诉讼法》第171条 |
| 刑事上诉期 | 判决送达后10天 | 《刑事诉讼法》第230条 |
| 举证期限 | 法院指定（通常15-30天） | 《民事诉讼法》第68条 |
| 执行申请期 | 判决生效后2年 | 《民事诉讼法》第250条 |
| 诉讼时效 | 3年（一般） | 《民法典》第188条 |
| 财产保全 | 30天内起诉 | 《民事诉讼法》第104条 |

## 执行步骤

### 步骤一：扫描Obsidian案件笔记

```python
import os
import re
from datetime import datetime, timedelta

VAULT_PATH = "/Users/yuzhenghong/Library/Mobile Documents/iCloud~md~obsidian/Documents/法律知识库"
CASE_DIR = os.path.join(VAULT_PATH, "01-案件笔记")

def scan_case_files():
    """扫描所有案件笔记，提取期限信息"""
    deadlines = []
    if not os.path.exists(CASE_DIR):
        return deadlines
    
    for f in os.listdir(CASE_DIR):
        if f.endswith('.md'):
            filepath = os.path.join(CASE_DIR, f)
            with open(filepath, 'r', encoding='utf-8') as fh:
                content = fh.read()
            
            # 提取案号
            case_match = re.search(r'案号[：:]\s*(.+)', content)
            case_number = case_match.group(1).strip() if case_match else f.replace('.md','')
            
            # 提取期限
            deadline_patterns = [
                (r'开庭[日期时间]*[：:]\s*(\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?)', '开庭'),
                (r'举证[期限截止]*[：:]\s*(\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?)', '举证期限'),
                (r'上诉[期限截止]*[：:]\s*(\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?)', '上诉期限'),
                (r'执行[申请期限截止]*[：:]\s*(\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?)', '执行期限'),
                (r'保全[到期期限]*[：:]\s*(\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?)', '保全到期'),
                (r'鉴定[申请期限]*[：:]\s*(\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?)', '鉴定期限'),
            ]
            
            for pattern, dtype in deadline_patterns:
                matches = re.findall(pattern, content)
                for m in matches:
                    try:
                        date_str = m.replace('年','-').replace('月','-').replace('日','')
                        deadline_date = datetime.strptime(date_str, '%Y-%m-%d')
                        deadlines.append({
                            'case': case_number,
                            'type': dtype,
                            'date': deadline_date,
                            'file': filepath
                        })
                    except:
                        pass
    
    return deadlines
```

### 步骤二：创建Apple Calendar事件

```python
def create_calendar_event(title, date, notes="", alert_days=1):
    """通过AppleScript创建Apple Calendar事件"""
    date_str = date.strftime('%Y-%m-%d')
    alert_minutes = alert_days * 24 * 60  # 提前几天提醒
    
    script = f'''
    tell application "Calendar"
        tell calendar "工作"
            set newEvent to make new event with properties {{
                summary:"{title}",
                start date:date "{date_str} 09:00:00",
                end date:date "{date_str} 10:00:00",
                description:"{notes}"
            }}
            tell newEvent
                make new sound alarm at date ((start date) - {alert_minutes} * minutes)
            end tell
        end tell
    end tell
    '''
    
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    return result.returncode == 0
```

### 步骤三：智能提醒规则

```python
def get_alert_config(deadline_type):
    """根据期限类型返回提醒配置"""
    config = {
        '开庭': {'alert_days': [7, 3, 1], 'priority': 'high'},
        '举证期限': {'alert_days': [7, 3, 1], 'priority': 'high'},
        '上诉期限': {'alert_days': [10, 5, 3, 1], 'priority': 'critical'},
        '执行期限': {'alert_days': [30, 15, 7, 3], 'priority': 'high'},
        '保全到期': {'alert_days': [7, 3, 1], 'priority': 'high'},
        '鉴定期限': {'alert_days': [7, 3], 'priority': 'medium'},
    }
    return config.get(deadline_type, {'alert_days': [3, 1], 'priority': 'medium'})
```

### 步骤四：定时扫描（Hermes cronjob）

建议创建每日扫描定时任务：
- 每天早上7:30扫描
- 检查未来30天内的所有期限
- 对临近期限（7天内）发送飞书提醒

## Obsidian案件笔记格式建议

在案件笔记中使用以下格式标记期限，系统可自动识别：

```markdown
## 案件时间线

- 开庭日期：2026-07-15
- 举证期限：2026-07-01
- 上诉期限：2026-07-30
- 执行期限：2028-07-30
```

## Apple Calendar日历结构

建议在Apple Calendar中创建以下日历：
- **案件开庭** — 红色
- **举证期限** — 橙色
- **上诉/执行** — 紫色
- **合同到期** — 蓝色

## Pitfalls

### 1. Obsidian笔记中日期格式不统一
**问题**：不同案件笔记中日期格式不一致（2026-07-15 vs 2026年7月15日 vs 7月15日）
**解决**：正则表达式兼容多种格式，优先匹配"YYYY-MM-DD"格式

### 2. Apple Calendar权限
**问题**：首次使用需授权AppleScript控制Calendar
**解决**：系统偏好设置 → 隐私与安全 → 自动化 → 允许终端控制Calendar

### 3. 重复事件
**问题**：重复扫描会创建重复事件
**解决**：创建前先查询是否已存在同名事件

### 4. 时区问题
**问题**：AppleScript日期解析可能受时区影响
**解决**：使用本地时间格式，不指定时区

### 5. 扫描结果包含非期限日期
**问题**：正则会匹配到合同签订日、立案日等非"期限"日期
**解决**：区分"已发生事件"和"待到期期限"，只对后者创建提醒。在笔记中使用明确的标记格式（如"举证期限：2026-07-01"而非"举证期限2026年7月1日到期"）

### 6. 实测数据
2026-06-08实测：扫描33个案件笔记，提取337条日期，去重后93个唯一日期。说明需要进一步过滤非期限日期。
