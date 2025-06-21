#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session04 练习题1解答：条件语句练习

本文件包含exercise1.py中所有练习题的参考解答。
这些解答展示了条件语句的正确使用方法和最佳实践。

作者: Python教程团队
创建日期: 2024-12-21
"""


def check_age_category(age):
    """
    练习1解答：年龄分类
    """
    if age < 0 or age > 150:
        return "无效年龄"
    elif age <= 2:
        return "婴儿"
    elif age <= 12:
        return "儿童"
    elif age <= 17:
        return "青少年"
    elif age <= 59:
        return "成年人"
    else:
        return "老年人"


def calculate_grade(score):
    """
    练习2解答：成绩等级计算
    """
    if score < 0 or score > 100:
        return ("无效", "无效分数")
    elif score >= 90:
        return ("A", "优秀")
    elif score >= 80:
        return ("B", "良好")
    elif score >= 70:
        return ("C", "中等")
    elif score >= 60:
        return ("D", "及格")
    else:
        return ("F", "不及格")


def check_triangle_type(a, b, c):
    """
    练习3解答：三角形类型判断
    """
    # 首先检查是否能构成三角形
    if a + b <= c or a + c <= b or b + c <= a:
        return "不是三角形"
    
    # 检查等边三角形
    if a == b == c:
        return "等边三角形"
    
    # 检查等腰三角形
    if a == b or b == c or a == c:
        return "等腰三角形"
    
    # 检查直角三角形（使用勾股定理）
    # 将三边排序，检查最大边的平方是否等于另外两边平方和
    sides = sorted([a, b, c])
    if abs(sides[0]**2 + sides[1]**2 - sides[2]**2) < 1e-10:
        return "直角三角形"
    
    return "普通三角形"


def calculate_shipping_cost(weight, distance, is_express=False):
    """
    练习4解答：快递费用计算
    """
    # 计算基础费用
    if weight <= 1:
        base_cost = 10
    elif weight <= 5:
        base_cost = 10 + (weight - 1) * 5
    else:
        base_cost = 10 + 4 * 5 + (weight - 5) * 3
    
    # 计算距离附加费
    if distance <= 100:
        distance_fee = 0
    elif distance <= 500:
        distance_fee = 5
    else:
        distance_fee = 15
    
    # 计算总费用
    total_cost = base_cost + distance_fee
    
    # 加急服务
    if is_express:
        total_cost *= 1.5
    
    return round(total_cost, 2)


def check_password_strength(password):
    """
    练习5解答：密码强度检查
    """
    conditions = {
        'length': len(password) >= 8,
        'uppercase': any(c.isupper() for c in password),
        'lowercase': any(c.islower() for c in password),
        'digit': any(c.isdigit() for c in password),
        'special': any(c in '!@#$%^&*' for c in password)
    }
    
    # 计算满足的条件数
    satisfied_count = sum(conditions.values())
    
    # 确定强度等级
    if satisfied_count == 5:
        strength = "强"
    elif satisfied_count == 4:
        strength = "中等"
    elif satisfied_count == 3:
        strength = "弱"
    else:
        strength = "很弱"
    
    # 生成建议
    suggestions = []
    if not conditions['length']:
        suggestions.append("密码长度至少8位")
    if not conditions['uppercase']:
        suggestions.append("添加大写字母")
    if not conditions['lowercase']:
        suggestions.append("添加小写字母")
    if not conditions['digit']:
        suggestions.append("添加数字")
    if not conditions['special']:
        suggestions.append("添加特殊字符")
    
    return (strength, suggestions)


def determine_season_activity(month, temperature):
    """
    练习6解答：季节活动推荐
    """
    # 检查月份有效性
    if month < 1 or month > 12:
        return ("无效月份", "请输入1-12的月份")
    
    # 确定季节
    if month in [3, 4, 5]:
        season = "春季"
        activity = "踏青赏花" if temperature > 20 else "室内活动"
    elif month in [6, 7, 8]:
        season = "夏季"
        activity = "游泳避暑" if temperature > 30 else "户外运动"
    elif month in [9, 10, 11]:
        season = "秋季"
        activity = "登山赏叶" if temperature > 15 else "室内阅读"
    else:  # 12, 1, 2月
        season = "冬季"
        activity = "滑雪运动" if temperature < 0 else "温泉泡汤"
    
    return (season, activity)


def main():
    """
    主函数：测试所有解答函数
    """
    print("Session04 练习题1解答：条件语句练习")
    print("=" * 50)
    
    # 测试练习1：年龄分类
    print("\n练习1：年龄分类测试")
    test_ages = [1, 8, 15, 25, 65, -5, 200]
    for age in test_ages:
        result = check_age_category(age)
        print(f"年龄 {age}: {result}")
    
    # 测试练习2：成绩等级
    print("\n练习2：成绩等级测试")
    test_scores = [95, 85, 75, 65, 45, 105, -10]
    for score in test_scores:
        grade, comment = calculate_grade(score)
        print(f"分数 {score}: {grade}等级 - {comment}")
    
    # 测试练习3：三角形类型
    print("\n练习3：三角形类型测试")
    test_triangles = [(3, 3, 3), (3, 4, 5), (5, 5, 8), (1, 2, 5), (6, 8, 10)]
    for a, b, c in test_triangles:
        result = check_triangle_type(a, b, c)
        print(f"边长 ({a}, {b}, {c}): {result}")
    
    # 测试练习4：快递费用
    print("\n练习4：快递费用测试")
    test_shipping = [
        (0.5, 50, False),
        (3, 200, False),
        (2, 100, True),
        (6, 600, False),
        (8, 300, True)
    ]
    for weight, distance, express in test_shipping:
        cost = calculate_shipping_cost(weight, distance, express)
        express_text = "加急" if express else "普通"
        print(f"{weight}kg, {distance}km, {express_text}: ¥{cost:.2f}")
    
    # 测试练习5：密码强度
    print("\n练习5：密码强度测试")
    test_passwords = ["Abc123!@", "abc123", "PASSWORD", "12345678", "Aa1!"]
    for password in test_passwords:
        strength, suggestions = check_password_strength(password)
        print(f"密码 '{password}': {strength}")
        if suggestions:
            print(f"  建议: {', '.join(suggestions)}")
    
    # 测试练习6：季节活动
    print("\n练习6：季节活动测试")
    test_seasons = [(4, 25), (7, 35), (10, 18), (1, -5), (13, 20), (6, 25)]
    for month, temp in test_seasons:
        season, activity = determine_season_activity(month, temp)
        print(f"{month}月, {temp}°C: {season} - {activity}")
    
    print("\n" + "=" * 50)
    print("解答测试完成！")
    print("\n📝 学习要点：")
    print("1. 条件语句的逻辑顺序很重要，要从特殊到一般")
    print("2. 使用elif可以避免不必要的条件检查")
    print("3. 复杂条件可以使用逻辑运算符组合")
    print("4. 注意边界条件的处理")
    print("5. 函数返回值的类型要保持一致")


if __name__ == "__main__":
    main()