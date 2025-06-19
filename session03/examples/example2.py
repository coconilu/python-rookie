#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session03 示例2: 比较运算符详解

本示例详细演示了Python中所有比较运算符的使用方法，
包括数值比较、字符串比较、以及比较运算符在条件判断中的应用。

学习目标:
- 掌握所有比较运算符的用法
- 理解不同数据类型的比较规则
- 学会在条件判断中使用比较运算符
- 了解比较运算的注意事项
"""

import math


def basic_comparison_operations():
    """
    演示基本比较运算
    """
    print("🔍 基本比较运算演示")
    print("=" * 30)
    
    # 定义测试数据
    a = 10
    b = 5
    c = 10
    
    print(f"给定三个数: a = {a}, b = {b}, c = {c}")
    print()
    
    # 等于运算符
    print(f"等于运算符 (==):")
    print(f"  a == b: {a} == {b} -> {a == b}")
    print(f"  a == c: {a} == {c} -> {a == c}")
    print()
    
    # 不等于运算符
    print(f"不等于运算符 (!=):")
    print(f"  a != b: {a} != {b} -> {a != b}")
    print(f"  a != c: {a} != {c} -> {a != c}")
    print()
    
    # 大于运算符
    print(f"大于运算符 (>):")
    print(f"  a > b: {a} > {b} -> {a > b}")
    print(f"  b > a: {b} > {a} -> {b > a}")
    print(f"  a > c: {a} > {c} -> {a > c}")
    print()
    
    # 小于运算符
    print(f"小于运算符 (<):")
    print(f"  a < b: {a} < {b} -> {a < b}")
    print(f"  b < a: {b} < {a} -> {b < a}")
    print(f"  a < c: {a} < {c} -> {a < c}")
    print()
    
    # 大于等于运算符
    print(f"大于等于运算符 (>=):")
    print(f"  a >= b: {a} >= {b} -> {a >= b}")
    print(f"  a >= c: {a} >= {c} -> {a >= c}")
    print(f"  b >= a: {b} >= {a} -> {b >= a}")
    print()
    
    # 小于等于运算符
    print(f"小于等于运算符 (<=):")
    print(f"  a <= b: {a} <= {b} -> {a <= b}")
    print(f"  a <= c: {a} <= {c} -> {a <= c}")
    print(f"  b <= a: {b} <= {a} -> {b <= a}")
    print()


def string_comparison():
    """
    演示字符串比较
    """
    print("📝 字符串比较演示")
    print("=" * 30)
    
    # 基本字符串比较
    str1 = "apple"
    str2 = "banana"
    str3 = "apple"
    
    print(f"字符串: str1 = '{str1}', str2 = '{str2}', str3 = '{str3}'")
    print()
    
    print("字符串相等性比较:")
    print(f"  str1 == str2: '{str1}' == '{str2}' -> {str1 == str2}")
    print(f"  str1 == str3: '{str1}' == '{str3}' -> {str1 == str3}")
    print()
    
    print("字符串字典序比较:")
    print(f"  str1 < str2: '{str1}' < '{str2}' -> {str1 < str2}")
    print(f"  str1 > str2: '{str1}' > '{str2}' -> {str1 > str2}")
    print()
    
    # 大小写敏感性
    print("大小写敏感性:")
    upper_str = "APPLE"
    lower_str = "apple"
    print(f"  '{upper_str}' == '{lower_str}': {upper_str == lower_str}")
    print(f"  '{upper_str}'.lower() == '{lower_str}': {upper_str.lower() == lower_str}")
    print()
    
    # 字符串长度比较
    print("字符串长度比较:")
    short_str = "hi"
    long_str = "hello"
    print(f"  len('{short_str}') = {len(short_str)}")
    print(f"  len('{long_str}') = {len(long_str)}")
    print(f"  len('{short_str}') < len('{long_str}'): {len(short_str) < len(long_str)}")
    print()
    
    # 字符串排序示例
    print("字符串排序示例:")
    names = ["张三", "李四", "王五", "赵六"]
    fruits = ["apple", "banana", "cherry", "date"]
    
    print(f"  原始姓名列表: {names}")
    print(f"  排序后: {sorted(names)}")
    print(f"  原始水果列表: {fruits}")
    print(f"  排序后: {sorted(fruits)}")
    print()


def numeric_type_comparison():
    """
    演示不同数值类型的比较
    """
    print("🔢 数值类型比较演示")
    print("=" * 30)
    
    # 整数和浮点数比较
    int_num = 5
    float_num = 5.0
    float_num2 = 5.1
    
    print(f"整数和浮点数比较:")
    print(f"  int_num = {int_num} (类型: {type(int_num).__name__})")
    print(f"  float_num = {float_num} (类型: {type(float_num).__name__})")
    print(f"  float_num2 = {float_num2} (类型: {type(float_num2).__name__})")
    print()
    
    print(f"  {int_num} == {float_num}: {int_num == float_num}")
    print(f"  {int_num} == {float_num2}: {int_num == float_num2}")
    print(f"  {int_num} < {float_num2}: {int_num < float_num2}")
    print()
    
    # 浮点数精度问题
    print("浮点数精度问题:")
    result = 0.1 + 0.2
    print(f"  0.1 + 0.2 = {result}")
    print(f"  0.1 + 0.2 == 0.3: {result == 0.3}")
    print(f"  使用 math.isclose: {math.isclose(result, 0.3)}")
    print(f"  使用 round: {round(result, 10) == 0.3}")
    print()
    
    # 科学记数法比较
    print("科学记数法比较:")
    big_num1 = 1e6  # 1,000,000
    big_num2 = 1000000
    small_num1 = 1e-6  # 0.000001
    small_num2 = 0.000001
    
    print(f"  1e6 == 1000000: {big_num1 == big_num2}")
    print(f"  1e-6 == 0.000001: {small_num1 == small_num2}")
    print()


def conditional_examples():
    """
    演示比较运算符在条件判断中的应用
    """
    print("🎯 条件判断应用示例")
    print("=" * 30)
    
    # 成绩等级判定
    print("1. 成绩等级判定:")
    scores = [95, 87, 76, 65, 45]
    
    for score in scores:
        if score >= 90:
            grade = 'A'
        elif score >= 80:
            grade = 'B'
        elif score >= 70:
            grade = 'C'
        elif score >= 60:
            grade = 'D'
        else:
            grade = 'F'
        print(f"  分数 {score}: 等级 {grade}")
    print()
    
    # 年龄分组
    print("2. 年龄分组:")
    ages = [5, 12, 17, 25, 45, 70]
    
    for age in ages:
        if age < 6:
            category = "学龄前儿童"
        elif age < 18:
            category = "未成年人"
        elif age < 60:
            category = "成年人"
        else:
            category = "老年人"
        print(f"  年龄 {age}: {category}")
    print()
    
    # 温度判断
    print("3. 温度状态判断:")
    temperatures = [-10, 0, 15, 25, 35, 40]
    
    for temp in temperatures:
        if temp < 0:
            status = "结冰"
        elif temp == 0:
            status = "冰点"
        elif temp < 20:
            status = "凉爽"
        elif temp < 30:
            status = "温暖"
        elif temp < 35:
            status = "炎热"
        else:
            status = "酷热"
        print(f"  温度 {temp}°C: {status}")
    print()
    
    # BMI判断
    print("4. BMI健康状况判断:")
    weights_heights = [(50, 1.6), (70, 1.75), (80, 1.7), (90, 1.8)]
    
    for weight, height in weights_heights:
        bmi = weight / (height ** 2)
        
        if bmi < 18.5:
            status = "偏瘦"
        elif bmi < 24:
            status = "正常"
        elif bmi < 28:
            status = "偏胖"
        else:
            status = "肥胖"
        
        print(f"  体重{weight}kg, 身高{height}m -> BMI: {bmi:.1f} ({status})")
    print()


def comparison_chains():
    """
    演示比较运算符的链式使用
    """
    print("🔗 比较运算符链式使用")
    print("=" * 30)
    
    # 范围判断
    print("1. 范围判断:")
    numbers = [5, 15, 25, 35, 45]
    
    for num in numbers:
        # 链式比较：等价于 (10 <= num) and (num <= 30)
        in_range = 10 <= num <= 30
        print(f"  {num} 在 [10, 30] 范围内: {in_range}")
    print()
    
    # 多重比较
    print("2. 多重比较:")
    a, b, c = 5, 10, 15
    print(f"  a = {a}, b = {b}, c = {c}")
    print(f"  a < b < c: {a < b < c}")
    print(f"  a == b == c: {a == b == c}")
    print(f"  a <= b <= c: {a <= b <= c}")
    print()
    
    # 成绩区间判断
    print("3. 成绩区间判断:")
    scores = [85, 92, 78, 95, 88]
    
    for score in scores:
        if 90 <= score <= 100:
            level = "优秀"
        elif 80 <= score < 90:
            level = "良好"
        elif 70 <= score < 80:
            level = "中等"
        elif 60 <= score < 70:
            level = "及格"
        else:
            level = "不及格"
        print(f"  分数 {score}: {level}")
    print()


def practical_applications():
    """
    比较运算符的实际应用
    """
    print("🛠️ 实际应用案例")
    print("=" * 30)
    
    # 1. 密码强度检查
    print("1. 密码强度检查:")
    passwords = ["123", "password", "Password123", "P@ssw0rd123!"]
    
    for pwd in passwords:
        length_ok = len(pwd) >= 8
        has_upper = any(c.isupper() for c in pwd)
        has_lower = any(c.islower() for c in pwd)
        has_digit = any(c.isdigit() for c in pwd)
        has_special = any(c in '!@#$%^&*()_+-=' for c in pwd)
        
        strength_count = sum([length_ok, has_upper, has_lower, has_digit, has_special])
        
        if strength_count >= 4:
            strength = "强"
        elif strength_count >= 3:
            strength = "中等"
        elif strength_count >= 2:
            strength = "弱"
        else:
            strength = "很弱"
        
        print(f"  密码 '{pwd}': 强度 {strength} (满足 {strength_count}/5 个条件)")
    print()
    
    # 2. 商品价格比较
    print("2. 商品价格比较:")
    products = [
        ("苹果", 8.5),
        ("香蕉", 6.0),
        ("橙子", 7.2),
        ("葡萄", 12.0)
    ]
    
    budget = 8.0
    print(f"  预算: {budget}元")
    
    affordable_products = []
    for name, price in products:
        if price <= budget:
            affordable_products.append((name, price))
            print(f"  ✅ {name}: {price}元 (可购买)")
        else:
            print(f"  ❌ {name}: {price}元 (超预算)")
    
    if affordable_products:
        cheapest = min(affordable_products, key=lambda x: x[1])
        print(f"  💡 推荐最便宜的: {cheapest[0]} ({cheapest[1]}元)")
    print()
    
    # 3. 考试成绩统计
    print("3. 考试成绩统计:")
    class_scores = [85, 92, 78, 95, 88, 76, 89, 93, 82, 87]
    
    total_students = len(class_scores)
    excellent = sum(1 for score in class_scores if score >= 90)
    good = sum(1 for score in class_scores if 80 <= score < 90)
    average_level = sum(1 for score in class_scores if 70 <= score < 80)
    below_average = sum(1 for score in class_scores if score < 70)
    
    print(f"  总人数: {total_students}")
    print(f"  优秀 (≥90分): {excellent}人 ({excellent/total_students*100:.1f}%)")
    print(f"  良好 (80-89分): {good}人 ({good/total_students*100:.1f}%)")
    print(f"  中等 (70-79分): {average_level}人 ({average_level/total_students*100:.1f}%)")
    print(f"  待提高 (<70分): {below_average}人 ({below_average/total_students*100:.1f}%)")
    
    class_average = sum(class_scores) / len(class_scores)
    print(f"  班级平均分: {class_average:.1f}")
    print()


def main():
    """
    主函数
    """
    print("Session03 示例2: 比较运算符详解")
    print("=" * 50)
    print()
    
    basic_comparison_operations()
    string_comparison()
    numeric_type_comparison()
    conditional_examples()
    comparison_chains()
    practical_applications()
    
    print("🎉 比较运算符示例演示完成！")
    print("\n💡 学习要点:")
    print("1. 掌握所有比较运算符的基本用法")
    print("2. 理解不同数据类型的比较规则")
    print("3. 学会使用链式比较简化条件判断")
    print("4. 注意浮点数比较的精度问题")
    print("5. 将比较运算符应用到实际条件判断中")


if __name__ == "__main__":
    main()