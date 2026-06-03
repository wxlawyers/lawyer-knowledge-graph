#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合赔偿计算器 — 交通事故/工伤/劳动纠纷
作者：余正洪律师
日期：2026-06-04
数据来源：
- 各省统计局官网《2025年国民经济和社会发展统计公报》
- 《工伤保险条例》、《江苏省实施〈工伤保险条例〉办法》(2015)
- 《劳动合同法》第47条、第87条、《劳动合同法实施条例》第27条
- 《最高人民法院关于审理人身损害赔偿案件适用法律若干问题的解释》
"""

import json

# ============================================================
# 数据模块：2025年度各省标准
# ============================================================

URBAN_INCOME = {
    "北京": 96292, "天津": 60099, "河北": 47544, "山西": 44649,
    "内蒙古": 52829, "辽宁": 50057, "吉林": 40817, "黑龙江": 39901,
    "上海": 96842, "江苏": 68956, "浙江": 81649, "安徽": 51737,
    "福建": 61437, "江西": 49580, "山东": 56444, "河南": 43926,
    "湖北": 49164, "湖南": 53369, "广东": 63974, "广西": 44793,
    "海南": 45829, "重庆": 51854, "四川": 49428, "贵州": 46289,
    "云南": 46699, "西藏": 58794, "陕西": 49053, "甘肃": 43910,
    "青海": 43879, "宁夏": 46593, "新疆": 45106,
}

URBAN_CONSUMPTION = {
    "北京": 54122, "天津": 39693, "河北": 30522, "山西": 27339,
    "内蒙古": 34183, "辽宁": 31428, "吉林": 29745, "黑龙江": 28666,
    "上海": 57076, "江苏": 43917, "浙江": 53223, "安徽": 30539,
    "福建": 41729, "江西": 30249, "山东": 32561, "河南": 27319,
    "湖北": 33376, "湖南": 33678, "广东": 42726, "广西": 27163,
    "海南": 32651, "重庆": 32764, "四川": 32181, "贵州": 29434,
    "云南": 30689, "西藏": 33281, "陕西": 29807, "甘肃": 29052,
    "青海": 27586, "宁夏": 29686, "新疆": 29702,
}

WORK_INJURY_MEDICAL_SUBSIDY_JS = {
    5: 200000, 6: 160000, 7: 120000, 8: 80000, 9: 50000, 10: 30000,
}

WORK_INJURY_EMPLOYMENT_SUBSIDY_JS = {
    5: 95000, 6: 85000, 7: 45000, 8: 35000, 9: 25000, 10: 15000,
}

RETIREMENT_RATIO = {5: 0.8, 4: 0.6, 3: 0.4, 2: 0.2, 1: 0.1}
DISABILITY_COEFFICIENT = {1: 1.0, 2: 0.9, 3: 0.8, 4: 0.7, 5: 0.6, 6: 0.5, 7: 0.4, 8: 0.3, 9: 0.2, 10: 0.1}
DISABILITY_SUBSIDY_MONTHS = {1: 27, 2: 25, 3: 23, 4: 21, 5: 18, 6: 16, 7: 13, 8: 11, 9: 9, 10: 7}


def calc_traffic_accident(province="江苏", age=30, disability_level=0, death=False,
                          medical_fee=0, hospital_days=0, lost_work_days=0, daily_income=0,
                          nursing_days=0, nutrition_days=0, dependents=None,
                          property_loss=0, mental_damage=0):
    """
    交通事故赔偿计算
    
    dependents参数格式：
    [{"age": 5},  # 未成年人，自动计算至18岁
     {"age": 40, "disability": True},  # 丧失劳动能力的成年人，计算20年
     {"age": 65, "disability": True}]  # 丧失劳动能力的老年人，计算15年
    """
    result = {"案件类型": "交通事故赔偿", "适用地区": province, "年龄": age,
              "伤残等级": disability_level, "各项赔偿": {}, "总计": 0}
    
    annual_income = URBAN_INCOME.get(province, 50000)
    annual_consumption = URBAN_CONSUMPTION.get(province, 30000)
    daily_income_std = annual_income / 365
    
    if medical_fee > 0: result["各项赔偿"]["医疗费"] = medical_fee
    if hospital_days > 0: result["各项赔偿"]["住院伙食补助费"] = hospital_days * 50
    if nutrition_days > 0: result["各项赔偿"]["营养费"] = nutrition_days * 30
    if lost_work_days > 0:
        income = daily_income if daily_income > 0 else daily_income_std
        result["各项赔偿"]["误工费"] = round(lost_work_days * income, 2)
    if nursing_days > 0: result["各项赔偿"]["护理费"] = nursing_days * 100
    
    if disability_level > 0 and not death:
        coeff = DISABILITY_COEFFICIENT[disability_level]
        years = 20 if age < 60 else (20 - (age - 60) if age < 75 else 5)
        amount = annual_income * years * coeff
        result["各项赔偿"]["残疾赔偿金"] = round(amount, 2)
        result["计算说明"] = f"{annual_income}元 × {years}年 × {coeff} = {round(amount, 2)}元"
    
    if death:
        years = 20 if age < 60 else (20 - (age - 60) if age < 75 else 5)
        result["各项赔偿"]["死亡赔偿金"] = round(annual_income * years, 2)
        result["各项赔偿"]["丧葬费"] = round(annual_income * 0.5, 2)
    
    # 被扶养人生活费
    if dependents and disability_level > 0:
        coeff = DISABILITY_COEFFICIENT[disability_level]
        total = 0
        details = []
        for dep in dependents:
            dep_age = dep["age"]
            is_disabled = dep.get("disability", False)
            
            if dep_age < 18:
                # 未成年人：计算至18岁
                dep_years = 18 - dep_age
            elif is_disabled:
                # 丧失劳动能力的成年人
                if dep_age < 60:
                    dep_years = 20
                elif dep_age < 75:
                    dep_years = 20 - (dep_age - 60)
                else:
                    dep_years = 5
            else:
                # 有劳动能力的成年人：不计算扶养费
                dep_years = 0
            
            amount = annual_consumption * dep_years * coeff
            total += amount
            if dep_years > 0:
                details.append(f"{dep_age}岁({dep_years}年)")
        
        result["各项赔偿"]["被扶养人生活费"] = round(total, 2)
        if details:
            result["扶养人明细"] = "、".join(details)
    
    if mental_damage > 0: result["各项赔偿"]["精神损害抚慰金"] = mental_damage
    if property_loss > 0: result["各项赔偿"]["财产损失"] = property_loss
    
    result["总计"] = round(sum(result["各项赔偿"].values()), 2)
    return result


def calc_work_injury(province="江苏", disability_level=0, monthly_salary=0,
                     work_months=0, medical_fee=0, death=False, dependents=None,
                     terminate_relation=False, years_to_retirement=0, occupational_disease=False):
    """工伤赔偿计算"""
    result = {"案件类型": "工伤赔偿", "适用地区": province, "伤残等级": disability_level,
              "月工资": monthly_salary, "各项赔偿": {}, "总计": 0}
    
    if medical_fee > 0: result["各项赔偿"]["医疗费"] = medical_fee
    if work_months > 0: result["各项赔偿"]["停工留薪期工资"] = monthly_salary * work_months
    
    if disability_level > 0 and not death:
        months = DISABILITY_SUBSIDY_MONTHS[disability_level]
        result["各项赔偿"]["一次性伤残补助金"] = monthly_salary * months
        result["计算说明"] = f"{monthly_salary}元 × {months}个月 = {monthly_salary * months}元"
    
    if 5 <= disability_level <= 10 and terminate_relation and not death:
        base_amount = WORK_INJURY_MEDICAL_SUBSIDY_JS.get(disability_level, 0)
        if occupational_disease:
            base_amount = round(base_amount * 1.4)
            result["说明_职业病"] = "职业病增发40%"
        if 0 < years_to_retirement < 5:
            ratio = RETIREMENT_RATIO.get(years_to_retirement, 1.0)
            base_amount = round(base_amount * ratio)
            result["说明_退休比例"] = f"距退休{years_to_retirement}年，按{int(ratio*100)}%支付"
        result["各项赔偿"]["一次性工伤医疗补助金"] = base_amount
    
    if 5 <= disability_level <= 10 and terminate_relation and not death:
        base_amount = WORK_INJURY_EMPLOYMENT_SUBSIDY_JS.get(disability_level, 0)
        if 0 < years_to_retirement < 5:
            ratio = RETIREMENT_RATIO.get(years_to_retirement, 1.0)
            base_amount = round(base_amount * ratio)
        result["各项赔偿"]["一次性伤残就业补助金"] = base_amount
    
    if death:
        monthly_avg = URBAN_INCOME.get(province, 50000) / 12
        result["各项赔偿"]["丧葬补助金"] = round(monthly_avg * 6, 2)
        result["各项赔偿"]["一次性工亡补助金"] = 1006420
    
    result["总计"] = round(sum(result["各项赔偿"].values()), 2)
    return result


def calc_labor_dispute(monthly_salary=0, work_years=0, work_months_extra=0,
                       violation=False, notice=False, salary_cap=0):
    """
    劳动纠纷赔偿计算
    
    依据：
    - 《劳动合同法》第47条：经济补偿计算
    - 《劳动合同法》第87条：违法解除赔偿金
    - 《劳动合同法》第40条：代通知金
    - 《劳动合同法实施条例》第27条：月工资计算
    
    规则：
    1. 月工资按照劳动者应得工资计算，包括计时工资、计件工资、奖金、津贴和补贴等
    2. 月工资高于当地社平工资3倍的，按3倍计算，补偿年限最高12年
    3. 工作不满12个月的，按实际工作月数计算平均工资
    4. 工作年限：每满1年算1个月，6个月以上不满1年算1个月，不满6个月算半个月
    """
    result = {"案件类型": "劳动纠纷赔偿", "月工资": monthly_salary,
              "工作年限": f"{work_years}年{work_months_extra}个月", "各项赔偿": {}, "总计": 0}
    
    # 计算工作年限（月数）
    total_months = work_years * 12 + work_months_extra
    if total_months < 6:
        comp_months = 0.5
    elif total_months < 12:
        comp_months = 1
    else:
        comp_months = work_years + (1 if work_months_extra >= 6 else 0)
    
    # 月工资上限检查（社平工资3倍）
    effective_salary = monthly_salary
    if salary_cap > 0 and monthly_salary > salary_cap:
        effective_salary = salary_cap
        # 高工资：补偿年限最高12年
        if comp_months > 12:
            comp_months = 12
        result["月工资上限"] = f"适用上限：{salary_cap}元（社平工资3倍）"
        result["年限上限"] = "高工资：补偿年限最高12年"
    
    # 1. 经济补偿金（N）
    compensation_n = effective_salary * comp_months
    result["各项赔偿"]["经济补偿金(N)"] = compensation_n
    result["计算说明_N"] = f"{effective_salary}元 × {comp_months}个月 = {compensation_n}元"
    
    # 2. 违法解除赔偿金（2N）
    if violation:
        compensation_2n = effective_salary * comp_months * 2
        result["各项赔偿"]["违法解除赔偿金(2N)"] = compensation_2n
    
    # 3. 代通知金（+1）
    if notice:
        result["各项赔偿"]["代通知金(+1)"] = monthly_salary
    
    result["总计"] = round(sum(result["各项赔偿"].values()), 2)
    return result


def main():
    print("=" * 60)
    print("综合赔偿计算器 — 交通事故/工伤/劳动纠纷")
    print("数据来源：2025年度各省统计局数据")
    print("=" * 60)
    print("\n1. 交通事故  2. 工伤  3. 劳动纠纷\n")
    
    choice = input("请选择 (1/2/3): ").strip()
    
    if choice == "1":
        province = input("省份（默认江苏）: ").strip() or "江苏"
        age = int(input("年龄（默认30）: ").strip() or "30")
        disability = int(input("伤残等级（0-10, 默认0）: ").strip() or "0")
        medical = float(input("医疗费（默认0）: ").strip() or "0")
        hospital = int(input("住院天数（默认0）: ").strip() or "0")
        lost_days = int(input("误工天数（默认0）: ").strip() or "0")
        daily = float(input("日收入（默认0）: ").strip() or "0")
        result = calc_traffic_accident(province=province, age=age, disability_level=disability,
                                       medical_fee=medical, hospital_days=hospital,
                                       lost_work_days=lost_days, daily_income=daily)
    elif choice == "2":
        province = input("省份（默认江苏）: ").strip() or "江苏"
        disability = int(input("伤残等级（0-10, 默认0）: ").strip() or "0")
        salary = float(input("月工资: ").strip() or "0")
        months = int(input("停工留薪期月数（默认0）: ").strip() or "0")
        medical = float(input("医疗费（默认0）: ").strip() or "0")
        terminate = input("是否解除劳动关系？(y/n, 默认n): ").strip().lower() == "y"
        retirement = int(input("距退休年数（默认0）: ").strip() or "0")
        occupational = input("是否职业病？(y/n, 默认n): ").strip().lower() == "y"
        result = calc_work_injury(province=province, disability_level=disability,
                                  monthly_salary=salary, work_months=months, medical_fee=medical,
                                  terminate_relation=terminate, years_to_retirement=retirement,
                                  occupational_disease=occupational)
    elif choice == "3":
        salary = float(input("月工资: ").strip() or "0")
        years = int(input("工作年限（年）: ").strip() or "0")
        extra = int(input("不足1年月数（默认0）: ").strip() or "0")
        violation = input("违法解除？(y/n): ").strip().lower() == "y"
        notice = input("代通知金？(y/n): ").strip().lower() == "y"
        cap = float(input("社平工资3倍上限（默认0不限）: ").strip() or "0")
        result = calc_labor_dispute(monthly_salary=salary, work_years=years,
                                    work_months_extra=extra, violation=violation, notice=notice,
                                    salary_cap=cap)
    else:
        print("无效选项"); return
    
    print("\n" + json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\n总计：{result['总计']}元")


if __name__ == "__main__":
    main()
