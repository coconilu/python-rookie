#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版BMI计算器

这是一个简化版的BMI计算器，专门为初学者设计。
重点展示运算符的使用，代码结构简单易懂。

学习重点：
1. 算术运算符的应用（+, -, *, /, **）
2. 比较运算符的使用（<, <=, >, >=, ==, !=）
3. 逻辑运算符的组合（and, or, not）
4. 运算符优先级的理解

作者：Python学习者
日期：2024年
"""

# 导入配置文件中的常量
from config import (
    WHO_BMI_CATEGORIES,
    BMI_CATEGORY_NAMES,
    POUND_TO_KG,
    INCH_TO_METER
)


def calculate_bmi_simple(weight, height, unit='metric'):
    """
    简化版BMI计算函数
    
    参数:
        weight (float): 体重
        height (float): 身高
        unit (str): 单位 ('metric' 或 'imperial')
    
    返回:
        float: BMI值
    """
    print(f"\n=== BMI计算过程演示 ===")
    print(f"输入数据: 体重={weight}, 身高={height}, 单位={unit}")
    
    # 单位转换（使用算术运算符）
    if unit == 'imperial':
        print("\n步骤1: 单位转换")
        print(f"体重转换: {weight}磅 × {POUND_TO_KG} = {weight * POUND_TO_KG:.2f}公斤")
        print(f"身高转换: {height}英寸 × {INCH_TO_METER} = {height * INCH_TO_METER:.3f}米")
        
        # 算术运算符应用
        weight_kg = weight * POUND_TO_KG  # 乘法运算符
        height_m = height * INCH_TO_METER  # 乘法运算符
    else:
        print("\n步骤1: 使用公制单位，无需转换")
        weight_kg = weight
        height_m = height
    
    print(f"转换后: 体重={weight_kg:.2f}kg, 身高={height_m:.3f}m")
    
    # BMI计算（使用算术运算符）
    print("\n步骤2: BMI计算")
    print(f"公式: BMI = 体重(kg) ÷ 身高²(m²)")
    
    # 演示运算符优先级
    height_squared = height_m ** 2  # 幂运算符（优先级高）
    print(f"身高的平方: {height_m:.3f}² = {height_squared:.6f}")
    
    bmi = weight_kg / height_squared  # 除法运算符
    print(f"BMI计算: {weight_kg:.2f} ÷ {height_squared:.6f} = {bmi:.2f}")
    
    return round(bmi, 2)  # 四舍五入


def classify_bmi_simple(bmi):
    """
    简化版BMI分类函数
    
    参数:
        bmi (float): BMI值
    
    返回:
        tuple: (分类代码, 中文名称)
    """
    print(f"\n=== BMI分类过程演示 ===")
    print(f"BMI值: {bmi}")
    print("\n分类标准（WHO标准）:")
    
    # 使用比较运算符进行分类
    for category, (min_val, max_val) in WHO_BMI_CATEGORIES.items():
        chinese_name = BMI_CATEGORY_NAMES[category]
        
        if max_val == float('inf'):
            print(f"- {chinese_name}: BMI ≥ {min_val}")
        else:
            print(f"- {chinese_name}: {min_val} ≤ BMI < {max_val}")
    
    print("\n分类判断过程:")
    
    # 演示比较运算符的使用
    if bmi < 18.5:  # 小于运算符
        print(f"{bmi} < 18.5 → 偏瘦")
        return 'underweight', '偏瘦'
    elif bmi >= 18.5 and bmi < 25.0:  # 逻辑运算符 and
        print(f"18.5 ≤ {bmi} < 25.0 → 正常")
        return 'normal', '正常'
    elif bmi >= 25.0 and bmi < 30.0:  # 逻辑运算符 and
        print(f"25.0 ≤ {bmi} < 30.0 → 偏胖")
        return 'overweight', '偏胖'
    else:  # bmi >= 30.0
        print(f"{bmi} ≥ 30.0 → 肥胖")
        return 'obese', '肥胖'


def validate_input_simple(weight, height, age, unit='metric'):
    """
    简化版输入验证函数
    
    参数:
        weight (float): 体重
        height (float): 身高
        age (int): 年龄
        unit (str): 单位
    
    返回:
        bool: 输入是否有效
    """
    print(f"\n=== 输入验证过程演示 ===")
    print(f"验证数据: 体重={weight}, 身高={height}, 年龄={age}, 单位={unit}")
    
    # 使用逻辑运算符组合多个条件
    print("\n验证规则:")
    
    if unit == 'metric':
        print("公制单位验证:")
        print("- 体重: 1-1000公斤")
        print("- 身高: 0.5-3.0米")
        
        # 复合条件判断（使用 and 运算符）
        weight_valid = weight >= 1 and weight <= 1000
        height_valid = height >= 0.5 and height <= 3.0
        
        print(f"\n体重验证: {weight} >= 1 and {weight} <= 1000 → {weight_valid}")
        print(f"身高验证: {height} >= 0.5 and {height} <= 3.0 → {height_valid}")
        
    elif unit == 'imperial':
        print("英制单位验证:")
        print("- 体重: 2-2200磅")
        print("- 身高: 20-120英寸")
        
        # 复合条件判断（使用 and 运算符）
        weight_valid = weight >= 2 and weight <= 2200
        height_valid = height >= 20 and height <= 120
        
        print(f"\n体重验证: {weight} >= 2 and {weight} <= 2200 → {weight_valid}")
        print(f"身高验证: {height} >= 20 and {height} <= 120 → {height_valid}")
        
    else:
        print(f"单位'{unit}'无效")
        return False
    
    # 年龄验证
    age_valid = age >= 1 and age <= 150
    print(f"年龄验证: {age} >= 1 and {age} <= 150 → {age_valid}")
    
    # 综合验证结果（使用 and 运算符）
    all_valid = weight_valid and height_valid and age_valid
    print(f"\n综合验证: {weight_valid} and {height_valid} and {age_valid} → {all_valid}")
    
    return all_valid


def get_health_advice_simple(bmi, age, is_male):
    """
    简化版健康建议函数
    
    参数:
        bmi (float): BMI值
        age (int): 年龄
        is_male (bool): 是否为男性
    
    返回:
        dict: 健康建议
    """
    print(f"\n=== 健康建议生成演示 ===")
    print(f"输入参数: BMI={bmi}, 年龄={age}, 男性={is_male}")
    
    # 获取BMI分类
    category, category_name = classify_bmi_simple(bmi)
    
    advice = {
        'category': category_name,
        'general': '',
        'diet': [],
        'exercise': [],
        'special_notes': []
    }
    
    print("\n建议生成逻辑:")
    
    # 根据BMI分类给出建议（使用比较运算符和逻辑运算符）
    if category == 'underweight':
        print("分类=偏瘦 → 增重建议")
        advice['general'] = "建议适当增重"
        advice['diet'] = ["增加高热量食物", "多吃坚果和牛油果"]
        advice['exercise'] = ["力量训练", "减少有氧运动"]
        
    elif category == 'normal':
        print("分类=正常 → 维持建议")
        advice['general'] = "保持当前体重"
        advice['diet'] = ["均衡饮食", "多吃蔬菜水果"]
        advice['exercise'] = ["规律运动", "有氧+力量训练"]
        
    elif category == 'overweight':
        print("分类=偏胖 → 减重建议")
        advice['general'] = "建议适当减重"
        advice['diet'] = ["控制热量", "减少高脂食物"]
        advice['exercise'] = ["增加有氧运动", "控制饮食"]
        
    else:  # obese
        print("分类=肥胖 → 强烈减重建议")
        advice['general'] = "强烈建议减重并咨询医生"
        advice['diet'] = ["严格控制热量", "寻求营养师指导"]
        advice['exercise'] = ["低强度运动开始", "专业指导"]
    
    # 年龄特殊建议（使用比较运算符）
    print(f"\n年龄特殊建议判断:")
    if age < 18:
        print(f"{age} < 18 → 未成年人特殊建议")
        advice['special_notes'].append("建议在家长指导下进行")
    elif age >= 65:
        print(f"{age} >= 65 → 老年人特殊建议")
        advice['special_notes'].append("注重平衡训练，预防跌倒")
    else:
        print(f"18 ≤ {age} < 65 → 成年人，无特殊建议")
    
    # 性别特殊建议（使用逻辑运算符）
    print(f"\n性别特殊建议判断:")
    if not is_male:  # 使用 not 运算符
        print("not 男性 → 女性特殊建议")
        advice['special_notes'].append("注意铁质和叶酸摄入")
    else:
        print("男性 → 无特殊性别建议")
    
    return advice


def demonstrate_operators():
    """
    演示各种运算符的使用
    """
    print("\n" + "="*60)
    print("运算符使用演示")
    print("="*60)
    
    # 算术运算符演示
    print("\n1. 算术运算符演示:")
    a, b = 10, 3
    print(f"a = {a}, b = {b}")
    print(f"加法: a + b = {a} + {b} = {a + b}")
    print(f"减法: a - b = {a} - {b} = {a - b}")
    print(f"乘法: a * b = {a} * {b} = {a * b}")
    print(f"除法: a / b = {a} / {b} = {a / b:.2f}")
    print(f"整除: a // b = {a} // {b} = {a // b}")
    print(f"取模: a % b = {a} % {b} = {a % b}")
    print(f"幂运算: a ** b = {a} ** {b} = {a ** b}")
    
    # 比较运算符演示
    print("\n2. 比较运算符演示:")
    x, y = 20, 15
    print(f"x = {x}, y = {y}")
    print(f"等于: x == y → {x} == {y} → {x == y}")
    print(f"不等于: x != y → {x} != {y} → {x != y}")
    print(f"大于: x > y → {x} > {y} → {x > y}")
    print(f"小于: x < y → {x} < {y} → {x < y}")
    print(f"大于等于: x >= y → {x} >= {y} → {x >= y}")
    print(f"小于等于: x <= y → {x} <= {y} → {x <= y}")
    
    # 逻辑运算符演示
    print("\n3. 逻辑运算符演示:")
    p, q = True, False
    print(f"p = {p}, q = {q}")
    print(f"逻辑与: p and q → {p} and {q} → {p and q}")
    print(f"逻辑或: p or q → {p} or {q} → {p or q}")
    print(f"逻辑非: not p → not {p} → {not p}")
    print(f"逻辑非: not q → not {q} → {not q}")
    
    # 复合条件演示
    print("\n4. 复合条件演示:")
    age, bmi = 25, 22.5
    print(f"年龄 = {age}, BMI = {bmi}")
    
    # 使用 and 运算符
    condition1 = age >= 18 and age <= 65
    print(f"成年人判断: {age} >= 18 and {age} <= 65 → {condition1}")
    
    # 使用 or 运算符
    condition2 = bmi < 18.5 or bmi >= 30
    print(f"需要关注: BMI < 18.5 or BMI >= 30 → {bmi} < 18.5 or {bmi} >= 30 → {condition2}")
    
    # 复杂条件组合
    healthy = (18.5 <= bmi < 25) and (18 <= age <= 65)
    print(f"健康成年人: (18.5 ≤ BMI < 25) and (18 ≤ 年龄 ≤ 65) → {healthy}")
    
    # 运算符优先级演示
    print("\n5. 运算符优先级演示:")
    result1 = 2 + 3 * 4  # 乘法优先级高于加法
    print(f"2 + 3 * 4 = {result1} (先算乘法: 2 + 12 = 14)")
    
    result2 = (2 + 3) * 4  # 括号改变优先级
    print(f"(2 + 3) * 4 = {result2} (先算括号: 5 * 4 = 20)")
    
    result3 = 10 > 5 and 3 < 7  # 比较运算符优先级高于逻辑运算符
    print(f"10 > 5 and 3 < 7 = {result3} (先算比较: True and True = True)")


def main():
    """
    简化版主函数
    """
    print("简化版BMI计算器 - 运算符学习版")
    print("=" * 50)
    
    # 演示运算符使用
    demonstrate_operators()
    
    print("\n" + "="*60)
    print("BMI计算实例演示")
    print("="*60)
    
    # 示例数据
    test_cases = [
        {'weight': 70, 'height': 1.75, 'age': 30, 'is_male': True, 'unit': 'metric'},
        {'weight': 154, 'height': 69, 'age': 25, 'is_male': False, 'unit': 'imperial'}
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{'='*20} 示例 {i} {'='*20}")
        
        # 输入验证
        is_valid = validate_input_simple(
            case['weight'], case['height'], case['age'], case['unit']
        )
        
        if not is_valid:
            print("❌ 输入数据无效，跳过计算")
            continue
        
        print("✅ 输入数据有效，开始计算")
        
        # BMI计算
        bmi = calculate_bmi_simple(case['weight'], case['height'], case['unit'])
        
        # BMI分类
        category, category_name = classify_bmi_simple(bmi)
        
        # 健康建议
        advice = get_health_advice_simple(bmi, case['age'], case['is_male'])
        
        # 显示结果
        print(f"\n=== 最终结果 ===")
        print(f"BMI值: {bmi}")
        print(f"分类: {category_name}")
        print(f"总体建议: {advice['general']}")
        
        if advice['diet']:
            print(f"饮食建议: {', '.join(advice['diet'])}")
        
        if advice['exercise']:
            print(f"运动建议: {', '.join(advice['exercise'])}")
        
        if advice['special_notes']:
            print(f"特殊提醒: {', '.join(advice['special_notes'])}")
    
    print("\n" + "="*60)
    print("学习总结")
    print("="*60)
    print("""
通过这个简化版BMI计算器，我们学习了：

1. 算术运算符的应用：
   - 加法(+)、减法(-)、乘法(*)、除法(/)
   - 幂运算(**)用于计算身高的平方
   - 单位转换中的乘法运算

2. 比较运算符的使用：
   - 大于(>)、小于(<)、大于等于(>=)、小于等于(<=)
   - 等于(==)、不等于(!=)
   - BMI分类判断中的范围比较

3. 逻辑运算符的组合：
   - and运算符：组合多个条件
   - or运算符：满足任一条件
   - not运算符：条件取反

4. 运算符优先级：
   - 算术运算符 > 比较运算符 > 逻辑运算符
   - 使用括号改变优先级

5. 实际应用场景：
   - 数据验证中的范围检查
   - 条件分支中的复合判断
   - 健康建议的逻辑生成

这些运算符是Python编程的基础，掌握它们对后续学习非常重要！
""")


if __name__ == "__main__":
    main()