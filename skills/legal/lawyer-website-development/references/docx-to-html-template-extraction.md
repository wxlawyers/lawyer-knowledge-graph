# 从官方docx提取模板到HTML网站

## 工作流程

当用户有官方发布的Word模板（如《要素式民事起诉状答辩状示范文本》），需要转换为HTML网站格式：

### 步骤1：分析docx结构

```python
from docx import Document

doc = Document('官方模板.docx')

# 找出所有案由的位置
case_positions = []
for i, para in enumerate(doc.paragraphs):
    text = para.text.strip()
    if text.startswith('(') and text.endswith(')') and ('纠纷' in text or '申请' in text):
        case_positions.append((i, text))

print("案由位置：")
for pos, name in case_positions:
    print(f"  Para {pos}: {name}")

print(f"\n表格总数: {len(doc.tables)}")
```

### 步骤2：确定每个案由的表格范围

```python
# 需要手动确定每个案由的表格索引范围
# 通过检查表格内容和案由位置来推断
case_table_ranges = {
    "民间借贷纠纷": (0, 4),      # Table 0-3
    "离婚纠纷": (14, 17),         # Table 14-16
    "买卖合同纠纷": (19, 23),     # Table 19-22
    # ... 根据实际情况定义
}
```

### 步骤3：表格转HTML

```python
def table_to_html(table):
    """将docx表格转换为HTML表格"""
    html = '<table class="template-table">\n'
    for row in table.rows:
        html += '  <tr>\n'
        for i, cell in enumerate(row.cells):
            text = cell.text.strip()
            text = text.replace('\n', '<br>')
            if i == 0:
                html += f'    <td class="label">{text}</td>\n'
            else:
                html += f'    <td>{text}</td>\n'
        html += '  </tr>\n'
    html += '</table>\n'
    return html
```

### 步骤4：生成完整HTML模板

```python
def generate_template(case_name, start_idx, end_idx, doc):
    """生成完整的官方模板HTML"""
    html = f'''<!-- 官方要素式起诉状模板格式 -->
<div class="official-template">
  <div class="template-header">
    <h2>民事起诉状</h2>
    <p class="case-type">（{case_name}）</p>
  </div>
'''
    
    for table_idx in range(start_idx, end_idx):
        if table_idx < len(doc.tables):
            table = doc.tables[table_idx]
            html += f'''
  <div class="template-section">
    <div class="section-content">
{table_to_html(table)}
    </div>
  </div>
'''
    
    html += '''
  <div class="template-footer">
    <p>具状人（签字、盖章）：</p>
    <p>日期：</p>
  </div>
</div>'''
    
    return html
```

### 步骤5：添加到网站JavaScript数据

```python
# 将模板添加到网站数据中的officialTemplate字段
# 注意：需要转义反引号和${}符号
template_html = generate_template(case_name, start, end, doc)
template_html = template_html.replace('\\', '\\\\')
template_html = template_html.replace('`', '\\`')
template_html = template_html.replace('${', '\\${')

# 添加到JavaScript对象
template_code = f',\n    officialTemplate: `{template_html}`'
```

## 注意事项

1. **官方模板是表格填写式**，不是叙述式
2. **必须先查看用户提供的官方文件**，不要自行生成
3. **转义特殊字符**：反引号(`)和${}需要转义
4. **避免重复字段**：每个案由只能有一个officialTemplate字段
5. **提供下载**：将原始docx文件放到网站目录供用户下载

## 官方模板结构（以民间借贷纠纷为例）

1. **说明** — 填写指引 + 诚信诉讼特别提示
2. **当事人信息** — 表格形式，区分自然人/法人，含勾选项
3. **诉讼请求和依据** — 分项表格（本金、利息、担保等）
4. **约定管辖和诉讼保全**
5. **事实和理由** — 分项表格（合同签订、借款金额、期限、利率等）
6. **证据清单** — 表格（证据名称、种类、来源、证明目的）
7. **具状人签名和日期**
