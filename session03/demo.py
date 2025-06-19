#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session03: 运算符与表达式 - 演示代码

本文件演示了Python中各种运算符的基本用法和实际应用。
包括算术运算符、比较运算符、逻辑运算符等。

作者: Python教程团队
创建日期: 2024-12-19
最后修改: 2024-12-19
"""

import math


def main():
    """
    主函数：演示程序的入口点
    """
    print("Session03: 运算符与表达式演示")
    print("=" * 40)
    
    # 演示各种运算符
    demo_arithmetic_operators()
    print()
    demo_comparison_operators()
    print()
    demo_logical_operators()
    print()
    demo_operator_precedence()
    print()
    demo_practical_examples()
    
    print("\n演示完成！")


def demo_arithmetic_operators():
    """
    演示算术运算符的使用
    """
    print("📊 算术运算符演示")
    print("-" * 20)
    
    a, b = 10, 3
    print(f"a = {a}, b = {b}")
    print(f"加法: {a} + {b} = {a + b}")
    print(f"减法: {a} - {b} = {a - b}")
    print(f"乘法: {a} * {b} = {a * b}")
    print(f"除法: {a} / {b} = {a / b:.2f}")
    print(f"整除: {a} // {b} = {a // b}")
    print(f"取模: {a} % {b} = {a % b}")
    print(f"幂运算: {a} ** {b} = {a ** b}")
    
    # 实际应用：判断奇偶数
    number = 15
    if number % 2 == 0:
        print(f"\n{number} 是偶数")
    else:
        print(f"\n{number} 是奇数")


def demo_comparison_operators():
    """
    演示比较运算符的使用
    """
    print("🔍 比较运算符演示")
    print("-" * 20)
    
    x, y, z = 5, 8, 5
    print(f"x = {x}, y = {y}, z = {z}")
    print(f"x == y: {x == y}")
    print(f"x == z: {x == z}")
    print(f"x != y: {x != y}")
    print(f"x > y: {x > y}")
    print(f"x < y: {x < y}")
    print(f"x >= z: {x >= z}")
    print(f"x <= y: {x <= y}")
    
    # 字符串比较
    name1, name2 = "Alice", "Bob"
    print(f"\n字符串比较:")
    print(f"'{name1}' < '{name2}': {name1 < name2}")
    print(f"'{name1}' == '{name1}': {name1 == name1}")


def demo_logical_operators():
    """
    演示逻辑运算符的使用
    """
    print("🧠 逻辑运算符演示")
    print("-" * 20)
    
    # 基本逻辑运算
    print("基本逻辑运算:")
    print(f"True and True: {True and True}")
    print(f"True and False: {True and False}")
    print(f"True or False: {True or False}")
    print(f"False or False: {False or False}")
    print(f"not True: {not True}")
    print(f"not False: {not False}")
    
    # 实际应用：复合条件判断
    age = 25
    income = 50000
    print(f"\n实际应用 - 贷款条件判断:")
    print(f"年龄: {age}, 收入: {income}")
    
    if age >= 18 and income >= 30000:
        print("✅ 符合贷款条件")
    else:
        print("❌ 不符合贷款条件")
    
    if age >= 65 or income >= 100000:
        print("✅ 享受优惠政策")
    else:
        print("❌ 不享受优惠政策")


def demo_operator_precedence():
    """
    演示运算符优先级
    """
    print("⚡ 运算符优先级演示")
    print("-" * 20)
    
    # 算术运算优先级
    result1 = 2 + 3 * 4
    result2 = (2 + 3) * 4
    print(f"2 + 3 * 4 = {result1} (先乘后加)")
    print(f"(2 + 3) * 4 = {result2} (括号改变优先级)")
    
    # 复杂表达式
    result3 = 2 ** 3 * 4 + 5
    print(f"2 ** 3 * 4 + 5 = {result3} (幂运算优先级最高)")
    
    # 逻辑运算优先级
    result4 = True or False and False
    result5 = (True or False) and False
    print(f"True or False and False = {result4} (and 优先级高于 or)")
    print(f"(True or False) and False = {result5} (括号改变优先级)")


def demo_practical_examples():
    """
    演示运算符的实际应用
    """
    print("🎯 实际应用示例")
    print("-" * 20)
    
    # 温度转换
    celsius = 25
    fahrenheit = celsius * 9/5 + 32
    print(f"温度转换: {celsius}°C = {fahrenheit}°F")
    
    # 圆的面积计算
    radius = 5
    area = math.pi * radius ** 2
    print(f"圆的面积: 半径 {radius} -> 面积 {area:.2f}")
    
    # 成绩等级判定
    score = 87
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
    print(f"成绩等级: {score}分 -> {grade}等")
    
    # 闰年判断
    year = 2024
    is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    print(f"闰年判断: {year}年 {'是' if is_leap else '不是'}闰年")
    
    # 密码强度简单检查
    password = "MyPassword123"
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    length_ok = len(password) >= 8
    
    strength_score = sum([has_upper, has_lower, has_digit, length_ok])
    if strength_score >= 4:
        strength = "强"
    elif strength_score >= 3:
        strength = "中等"
    else:
        strength = "弱"
    
    print(f"密码强度: '{password}' -> {strength}")
    print(f"  包含大写字母: {has_upper}")
    print(f"  包含小写字母: {has_lower}")
    print(f"  包含数字: {has_digit}")
    print(f"  长度>=8: {length_ok}")


if __name__ == "__main__":
    main()