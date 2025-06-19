#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session03 示例1: 算术运算符详解

本示例详细演示了Python中所有算术运算符的使用方法，
包括基本四则运算、取模、幂运算等，以及它们的实际应用场景。

学习目标:
- 掌握所有算术运算符的用法
- 理解整除和普通除法的区别
- 学会在实际问题中应用算术运算符
"""

import math


def basic_arithmetic_operations():
    """
    演示基本算术运算
    """
    print("🔢 基本算术运算演示")
    print("=" * 30)
    
    # 定义两个数
    a = 15
    b = 4
    
    print(f"给定两个数: a = {a}, b = {b}")
    print()
    
    # 加法
    result_add = a + b
    print(f"加法: {a} + {b} = {result_add}")
    
    # 减法
    result_sub = a - b
    print(f"减法: {a} - {b} = {result_sub}")
    
    # 乘法
    result_mul = a * b
    print(f"乘法: {a} * {b} = {result_mul}")
    
    # 除法（浮点数结果）
    result_div = a / b
    print(f"除法: {a} / {b} = {result_div}")
    
    # 整除（向下取整）
    result_floor_div = a // b
    print(f"整除: {a} // {b} = {result_floor_div}")
    
    # 取模（余数）
    result_mod = a % b
    print(f"取模: {a} % {b} = {result_mod}")
    
    # 幂运算
    result_pow = a ** b
    print(f"幂运算: {a} ** {b} = {result_pow}")
    
    print()


def division_examples():
    """
    详细演示除法运算的不同情况
    """
    print("➗ 除法运算详解")
    print("=" * 30)
    
    examples = [
        (10, 3),
        (15, 5),
        (7, 2),
        (-7, 2),
        (7, -2),
        (-7, -2)
    ]
    
    for dividend, divisor in examples:
        normal_div = dividend / divisor
        floor_div = dividend // divisor
        remainder = dividend % divisor
        
        print(f"{dividend} ÷ {divisor}:")
        print(f"  普通除法: {dividend} / {divisor} = {normal_div}")
        print(f"  整除: {dividend} // {divisor} = {floor_div}")
        print(f"  余数: {dividend} % {divisor} = {remainder}")
        print(f"  验证: {divisor} * {floor_div} + {remainder} = {divisor * floor_div + remainder}")
        print()


def modulo_applications():
    """
    演示取模运算的实际应用
    """
    print("🔄 取模运算的实际应用")
    print("=" * 30)
    
    # 1. 判断奇偶数
    print("1. 判断奇偶数:")
    numbers = [1, 2, 3, 4, 5, 10, 15, 20]
    for num in numbers:
        if num % 2 == 0:
            print(f"  {num} 是偶数")
        else:
            print(f"  {num} 是奇数")
    print()
    
    # 2. 判断能否被某数整除
    print("2. 判断能否被3整除:")
    for num in numbers:
        if num % 3 == 0:
            print(f"  {num} 能被3整除")
        else:
            print(f"  {num} 不能被3整除，余数为 {num % 3}")
    print()
    
    # 3. 循环索引（环形数组）
    print("3. 循环索引应用:")
    colors = ['红', '绿', '蓝', '黄']
    for i in range(10):
        color_index = i % len(colors)
        print(f"  第{i}个位置 -> 颜色: {colors[color_index]}")
    print()
    
    # 4. 时间计算
    print("4. 时间计算应用:")
    total_minutes = 150
    hours = total_minutes // 60
    minutes = total_minutes % 60
    print(f"  {total_minutes}分钟 = {hours}小时{minutes}分钟")
    
    total_seconds = 3725
    hours = total_seconds // 3600
    remaining_seconds = total_seconds % 3600
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60
    print(f"  {total_seconds}秒 = {hours}小时{minutes}分钟{seconds}秒")
    print()


def power_operations():
    """
    演示幂运算的使用
    """
    print("⚡ 幂运算演示")
    print("=" * 30)
    
    # 基本幂运算
    print("1. 基本幂运算:")
    base = 2
    for exponent in range(0, 6):
        result = base ** exponent
        print(f"  {base}^{exponent} = {result}")
    print()
    
    # 平方根（使用分数指数）
    print("2. 平方根计算:")
    numbers = [4, 9, 16, 25, 36]
    for num in numbers:
        sqrt_result = num ** 0.5
        print(f"  √{num} = {sqrt_result}")
    print()
    
    # 立方根
    print("3. 立方根计算:")
    numbers = [8, 27, 64, 125]
    for num in numbers:
        cbrt_result = num ** (1/3)
        print(f"  ∛{num} = {cbrt_result:.2f}")
    print()
    
    # 科学计算应用
    print("4. 科学计算应用:")
    
    # 复利计算
    principal = 1000  # 本金
    rate = 0.05       # 年利率 5%
    time = 10         # 时间（年）
    amount = principal * (1 + rate) ** time
    print(f"  复利计算: 本金{principal}元，年利率{rate*100}%，{time}年后 = {amount:.2f}元")
    
    # 面积计算
    radius = 5
    area = math.pi * radius ** 2
    print(f"  圆面积: 半径{radius} -> 面积 = {area:.2f}")
    
    # 体积计算
    side = 3
    volume = side ** 3
    print(f"  正方体体积: 边长{side} -> 体积 = {volume}")
    print()


def practical_calculator():
    """
    实用计算器示例
    """
    print("🧮 实用计算器")
    print("=" * 30)
    
    # BMI计算
    def calculate_bmi(weight, height):
        """计算BMI指数"""
        bmi = weight / (height ** 2)
        return bmi
    
    weight = 70  # 体重(kg)
    height = 1.75  # 身高(m)
    bmi = calculate_bmi(weight, height)
    print(f"BMI计算: 体重{weight}kg，身高{height}m -> BMI = {bmi:.2f}")
    
    # 温度转换
    def celsius_to_fahrenheit(celsius):
        """摄氏度转华氏度"""
        return celsius * 9/5 + 32
    
    def fahrenheit_to_celsius(fahrenheit):
        """华氏度转摄氏度"""
        return (fahrenheit - 32) * 5/9
    
    temp_c = 25
    temp_f = celsius_to_fahrenheit(temp_c)
    print(f"温度转换: {temp_c}°C = {temp_f}°F")
    
    temp_f = 77
    temp_c = fahrenheit_to_celsius(temp_f)
    print(f"温度转换: {temp_f}°F = {temp_c:.1f}°C")
    
    # 距离计算
    def calculate_distance(x1, y1, x2, y2):
        """计算两点间距离"""
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    
    x1, y1 = 0, 0
    x2, y2 = 3, 4
    distance = calculate_distance(x1, y1, x2, y2)
    print(f"距离计算: 点({x1},{y1})到点({x2},{y2})的距离 = {distance}")
    
    # 百分比计算
    original_price = 100
    discount_rate = 0.2  # 20%折扣
    discount_amount = original_price * discount_rate
    final_price = original_price - discount_amount
    print(f"折扣计算: 原价{original_price}元，{discount_rate*100}%折扣 -> 最终价格{final_price}元")
    print()


def main():
    """
    主函数
    """
    print("Session03 示例1: 算术运算符详解")
    print("=" * 50)
    print()
    
    basic_arithmetic_operations()
    division_examples()
    modulo_applications()
    power_operations()
    practical_calculator()
    
    print("🎉 算术运算符示例演示完成！")
    print("\n💡 学习要点:")
    print("1. 掌握所有算术运算符的基本用法")
    print("2. 理解整除(//)和普通除法(/)的区别")
    print("3. 学会使用取模(%)运算解决实际问题")
    print("4. 熟练运用幂运算(**)进行科学计算")
    print("5. 将算术运算符应用到实际项目中")


if __name__ == "__main__":
    main()