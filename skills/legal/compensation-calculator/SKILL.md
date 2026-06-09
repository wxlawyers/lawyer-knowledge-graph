---
name: compensation-calculator
description: "交通事故·工伤·劳动纠纷赔偿计算器 — 三大模块合一，支持31省份标准，数据来源权威。"
version: 2.0.0
author: 余正洪律师
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [legal, compensation, calculator, traffic-accident, work-injury, labor]
auto_invoke: true
examples:
  - "交通事故10级伤残能赔多少"
  - "工伤十级，月工资8000，能赔多少"
  - "违法辞退，月工资1万，工作5年，能赔多少"
  - "帮我算一下交通事故赔偿"
---

# 交通事故·工伤·劳动纠纷赔偿计算器

**中文名**：交通事故·工伤·劳动纠纷赔偿计算器
**英文名**：Compensation Calculator
**版本**：v2.0.0
**作者**：余正洪律师

---

## 功能模块

### 1. 交通事故赔偿
- 医疗费、误工费、护理费、营养费、住院伙食补助费
- 残疾赔偿金（1-10级）
- 死亡赔偿金、丧葬费
- 被扶养人生活费（区分未成年人/丧失劳动能力成年人）
- 精神损害抚慰金、财产损失

### 2. 工伤赔偿
- 医疗费、停工留薪期工资
- 一次性伤残补助金（1-10级，全国统一）
- 一次性工伤医疗补助金（5-10级，需解除劳动关系）
- 一次性伤残就业补助金（5-10级，需解除劳动关系）
- 距退休比例（不足5年按比例支付）
- 职业病增发40%
- 工亡赔偿（丧葬补助金、一次性工亡补助金）

### 3. 劳动纠纷赔偿
- 经济补偿金（N）
- 违法解除赔偿金（2N）
- 代通知金（+1）
- 高工资限制（社平工资3倍，年限最高12年）

---

## 使用方式

### 方式1：自然语言调用（推荐）

直接对我说：
```
帮我算一下交通事故10级伤残能赔多少
工伤十级，月工资8000，解除劳动关系，能赔多少
违法辞退，月工资1万，工作5年3个月，能赔多少
```

我会自动调用计算器并返回结果。

### 方式2：Python脚本调用

```python
from compensation_calculator import calc_traffic_accident, calc_work_injury, calc_labor_dispute

# 交通事故
result = calc_traffic_accident(
    province="江苏",      # 省份
    age=35,               # 年龄
    disability_level=10,  # 伤残等级（0-10）
    medical_fee=50000,    # 医疗费
    hospital_days=30,     # 住院天数
    lost_work_days=90,    # 误工天数
    daily_income=300,     # 日收入（有固定收入时）
    nursing_days=30,      # 护理天数
    nutrition_days=30,    # 营养天数
    dependents=[          # 被扶养人
        {"age": 5},       # 未成年人
        {"age": 40, "disability": True},  # 丧失劳动能力成年人
    ],
)

# 工伤
result = calc_work_injury(
    province="江苏",
    disability_level=10,
    monthly_salary=8000,
    work_months=3,        # 停工留薪期月数
    medical_fee=30000,
    terminate_relation=True,      # 是否解除劳动关系
    years_to_retirement=0,        # 距退休年数
    occupational_disease=False,   # 是否职业病
)

# 劳动纠纷
result = calc_labor_dispute(
    monthly_salary=10000,
    work_years=5,
    work_months_extra=3,
    violation=True,       # 是否违法解除
    notice=True,          # 是否需要代通知金
    salary_cap=17239,     # 社平工资3倍上限
)
```

### 方式3：命令行交互

```bash
cd ~/Documents
python3 compensation_calculator.py
```

---

## 数据来源

| 数据类型 | 来源 |
|----------|------|
| 各省收入/消费 | 各省统计局《2025年国民经济和社会发展统计公报》 |
| 工伤标准 | 《工伤保险条例》、《江苏省实施〈工伤保险条例〉办法》 |
| 劳动标准 | 《劳动合同法》第47/87条、《实施条例》第27条 |
| 扶养费标准 | 《最高人民法院关于审理人身损害赔偿案件适用法律若干问题的解释》 |

---

## 计算规则

### 交通事故

| 项目 | 公式 |
|------|------|
| 残疾赔偿金 | 年人均可支配收入 × 赔偿年限 × 伤残系数 |
| 死亡赔偿金 | 年人均可支配收入 × 赔偿年限 |
| 被扶养人生活费 | 年人均消费支出 × 扶养年限 × 伤残系数 |
| 误工费 | 日收入 × 误工天数 |

赔偿年限：≤60岁=20年，60-75岁=20-(年龄-60)，≥75岁=5年

### 工伤

| 项目 | 公式 |
|------|------|
| 一次性伤残补助金 | 月工资 × 月数（1-10级：27/25/23/21/18/16/13/11/9/7） |
| 一次性工伤医疗补助金 | 固定金额（江苏10级：3万元） |
| 一次性伤残就业补助金 | 固定金额（江苏10级：1.5万元） |

### 劳动纠纷

| 项目 | 公式 |
|------|------|
| 经济补偿金(N) | 月工资 × 工作年限 |
| 违法解除赔偿金(2N) | N × 2 |
| 代通知金(+1) | 1个月工资 |

高工资限制：月工资>社平3倍时，按3倍计算，年限最高12年

---

## 注意事项

1. 计算结果仅供参考，具体金额需根据实际情况调整
2. 工伤医疗/就业补助金需解除劳动关系才能获得
3. 距退休不足5年按比例支付
4. 职业病增发40%医疗补助金
5. 被扶养人需区分未成年人和丧失劳动能力成年人

---

## 常见问题

### 1. JavaScript依赖加载失败

**问题**：CDN链接被墙或网络不稳定

**解决方案**：所有资源已内联到HTML，无需外部依赖

### 2. 赔偿标准错误

**问题**：使用了错误的标准

**解决方案**：参考 `references/standards.md` 中的准确数据，或询问用户

### 3. 计算逻辑错误

**问题**：公式实现有误

**解决方案**：参考 `references/formulas.md` 中的标准公式

### 4. HTML行号问题（GitHub Pages部署）

**问题**：`read_file`工具会添加行号（如`1|`），导致HTML无法渲染

**解决方案**：
```python
import re

with open('docs/index.html', 'r') as f:
    content = f.read()

# 删除行号
content = re.sub(r'^\d+\|', '', content, flags=re.MULTILINE)

with open('docs/index.html', 'w') as f:
    f.write(content)
```

**预防**：避免使用read_file读取HTML文件后直接写入，使用execute_code或terminal直接操作

---

## 文件位置

- 脚本：`~/Documents/compensation_calculator.py`
- 技能：`~/.hermes/skills/legal/compensation-calculator/`

---

## 常见错误（血泪教训）

### 1. 数据来源错误
**错误**：使用旧数据或凭记忆填写各省标准
**正确**：必须核实数据来源，标注"余律师确认"或"待核实"

### 2. 年度标注错误
**错误**：写成"2024年标准"或"2025年标准"
**正确**：应写"2026年公布（2025年度数据）"——统计数据通常在次年公布

### 3. 工伤补助金计算方式错误
**错误**：用月数计算（如10级4个月×月平均工资）
**正确**：江苏是固定金额（10级医疗3万+就业1.5万），依据《江苏省实施〈工伤保险条例〉办法》第27条

### 4. 被扶养人生活费计算错误
**错误**：18岁以上成年人默认计算20年
**正确**：18岁以上需"丧失劳动能力"才有扶养费，需添加`disability`参数

### 5. 高工资限制遗漏
**错误**：高工资时不限制补偿年限
**正确**：月工资>社平3倍时，按3倍计算，补偿年限最高12年

### 6. 假装能联网获取数据
**错误**：说"我来联网获取"，但实际无法访问统计局网站
**正确**：直接说"我无法获取权威数据，请您提供"

---

## 版本历史

- v1.0.0 (2026-06-04)：初始版本
- v2.0.0 (2026-06-04)：完善工伤/劳动纠纷模块，修正数据错误，三遍核查

## 参考文件

- `references/jiangsu-work-injury-standards.md` — 江苏工伤赔偿标准详解
- `references/2025-provincial-compensation-data.md` — 2025年度31省赔偿标准数据（已核实）

- [[legal-analysis-pitfalls]] — 法律分析常见错误与教训（本技能开发过程中的血泪教训）
