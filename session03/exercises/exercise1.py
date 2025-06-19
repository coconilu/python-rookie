#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session03 练习题1：基础运算练习

题目描述：
编写一个程序，实现以下功能：
1. 创建一个简单的计算器，能够进行基本的四则运算
2. 实现一个数学工具集，包含常用的数学计算功能
3. 编写函数来解决实际的数学问题

具体要求：
1. 实现基本计算器功能（加减乘除、取模、幂运算）
2. 实现数学工具函数（平均值、最大最小值、阶乘等）
3. 解决实际问题（时间转换、面积计算、温度转换等）
4. 处理边界情况和错误输入

学习目标：
- 熟练使用所有算术运算符
- 理解运算符在实际问题中的应用
- 学会处理数学计算中的特殊情况

提示：
- 注意除零错误的处理
- 考虑负数的特殊情况
- 使用适当的数据类型存储结果
"""

import math


def basic_calculator(a, b, operation):
    """
    基本计算器函数
    
    参数:
        a (float): 第一个数
        b (float): 第二个数
        operation (str): 运算符 (+, -, *, /, //, %, **)
    
    返回:
        float: 计算结果
    
    在这里实现你的代码
    """
    # TODO: 实现基本计算器功能
    # 提示：使用if-elif语句处理不同的运算符
    # 注意处理除零错误
    pass


def calculate_average(numbers):
    """
    计算数字列表的平均值
    
    参数:
        numbers (list): 数字列表
    
    返回:
        float: 平均值
    
    在这里实现你的代码
    """
    # TODO: 计算平均值
    # 提示：使用sum()函数和len()函数
    pass


def find_max_min(numbers):
    """
    找出数字列表中的最大值和最小值
    
    参数:
        numbers (list): 数字列表
    
    返回:
        tuple: (最大值, 最小值)
    
    在这里实现你的代码
    """
    # TODO: 找出最大值和最小值
    # 提示：使用max()和min()函数，或者使用循环
    pass


def calculate_factorial(n):
    """
    计算n的阶乘
    
    参数:
        n (int): 非负整数
    
    返回:
        int: n的阶乘
    
    在这里实现你的代码
    """
    # TODO: 计算阶乘
    # 提示：可以使用循环或递归，注意处理n=0的情况
    pass


def is_prime(n):
    """
    判断一个数是否为质数
    
    参数:
        n (int): 要判断的数
    
    返回:
        bool: 如果是质数返回True，否则返回False
    
    在这里实现你的代码
    """
    # TODO: 判断质数
    # 提示：质数只能被1和自己整除
    # 可以只检查到sqrt(n)来提高效率
    pass


def convert_seconds(total_seconds):
    """
    将秒数转换为时分秒格式
    
    参数:
        total_seconds (int): 总秒数
    
    返回:
        tuple: (小时, 分钟, 秒)
    
    在这里实现你的代码
    """
    # TODO: 时间转换
    # 提示：使用整除和取模运算
    # 1小时 = 3600秒，1分钟 = 60秒
    pass


def calculate_circle_area(radius):
    """
    计算圆的面积
    
    参数:
        radius (float): 圆的半径
    
    返回:
        float: 圆的面积
    
    在这里实现你的代码
    """
    # TODO: 计算圆的面积
    # 提示：面积 = π * r²，使用math.pi
    pass


def celsius_to_fahrenheit(celsius):
    """
    摄氏度转华氏度
    
    参数:
        celsius (float): 摄氏度
    
    返回:
        float: 华氏度
    
    在这里实现你的代码
    """
    # TODO: 温度转换
    # 提示：华氏度 = 摄氏度 * 9/5 + 32
    pass


def calculate_compound_interest(principal, rate, time):
    """
    计算复利
    
    参数:
        principal (float): 本金
        rate (float): 年利率（小数形式，如0.05表示5%）
        time (int): 时间（年）
    
    返回:
        float: 最终金额
    
    在这里实现你的代码
    """
    # TODO: 计算复利
    # 提示：最终金额 = 本金 * (1 + 利率)^时间
    pass


def solve_quadratic_equation(a, b, c):
    """
    解一元二次方程 ax² + bx + c = 0
    
    参数:
        a, b, c (float): 方程系数
    
    返回:
        tuple: 方程的解，可能是 (x1, x2) 或 (x,) 或 None
    
    在这里实现你的代码
    """
    # TODO: 解一元二次方程
    # 提示：使用判别式 Δ = b² - 4ac
    # 当Δ > 0时有两个实根，Δ = 0时有一个实根，Δ < 0时无实根
    pass


def test_functions():
    """
    测试所有函数的功能
    """
    print("=" * 50)
    print("Session03 练习题1：基础运算练习 - 测试")
    print("=" * 50)
    
    # 测试基本计算器
    print("\n1. 测试基本计算器:")
    test_cases = [
        (10, 3, '+'),
        (10, 3, '-'),
        (10, 3, '*'),
        (10, 3, '/'),
        (10, 3, '//'),
        (10, 3, '%'),
        (2, 3, '**')
    ]
    
    for a, b, op in test_cases:
        try:
            result = basic_calculator(a, b, op)
            print(f"  {a} {op} {b} = {result}")
        except Exception as e:
            print(f"  {a} {op} {b} = 错误: {e}")
    
    # 测试数学工具函数
    print("\n2. 测试数学工具函数:")
    numbers = [1, 5, 3, 9, 2, 8, 4]
    
    try:
        avg = calculate_average(numbers)
        print(f"  数列 {numbers} 的平均值: {avg}")
    except Exception as e:
        print(f"  计算平均值错误: {e}")
    
    try:
        max_val, min_val = find_max_min(numbers)
        print(f"  数列 {numbers} 的最大值: {max_val}, 最小值: {min_val}")
    except Exception as e:
        print(f"  查找最大最小值错误: {e}")
    
    # 测试阶乘
    print("\n3. 测试阶乘计算:")
    for n in [0, 1, 5, 10]:
        try:
            factorial = calculate_factorial(n)
            print(f"  {n}! = {factorial}")
        except Exception as e:
            print(f"  计算 {n}! 错误: {e}")
    
    # 测试质数判断
    print("\n4. 测试质数判断:")
    for n in [2, 3, 4, 17, 25, 29]:
        try:
            is_prime_result = is_prime(n)
            print(f"  {n} 是质数: {is_prime_result}")
        except Exception as e:
            print(f"  判断 {n} 是否为质数错误: {e}")
    
    # 测试时间转换
    print("\n5. 测试时间转换:")
    for seconds in [3661, 7200, 90, 3725]:
        try:
            hours, minutes, secs = convert_seconds(seconds)
            print(f"  {seconds}秒 = {hours}小时{minutes}分钟{secs}秒")
        except Exception as e:
            print(f"  转换 {seconds}秒 错误: {e}")
    
    # 测试几何计算
    print("\n6. 测试几何计算:")
    for radius in [1, 5, 10]:
        try:
            area = calculate_circle_area(radius)
            print(f"  半径 {radius} 的圆面积: {area:.2f}")
        except Exception as e:
            print(f"  计算半径 {radius} 的圆面积错误: {e}")
    
    # 测试温度转换
    print("\n7. 测试温度转换:")
    for celsius in [0, 25, 100, -40]:
        try:
            fahrenheit = celsius_to_fahrenheit(celsius)
            print(f"  {celsius}°C = {fahrenheit}°F")
        except Exception as e:
            print(f"  转换 {celsius}°C 错误: {e}")
    
    # 测试复利计算
    print("\n8. 测试复利计算:")
    test_investments = [(1000, 0.05, 10), (5000, 0.03, 5)]
    for principal, rate, time in test_investments:
        try:
            amount = calculate_compound_interest(principal, rate, time)
            print(f"  本金{principal}元，年利率{rate*100}%，{time}年后: {amount:.2f}元")
        except Exception as e:
            print(f"  计算复利错误: {e}")
    
    # 测试二次方程求解
    print("\n9. 测试二次方程求解:")
    equations = [(1, -5, 6), (1, -2, 1), (1, 0, 1)]
    for a, b, c in equations:
        try:
            solutions = solve_quadratic_equation(a, b, c)
            print(f"  方程 {a}x² + {b}x + {c} = 0 的解: {solutions}")
        except Exception as e:
            print(f"  求解方程错误: {e}")
    
    print("\n" + "=" * 50)
    print("测试完成！请检查你的实现是否正确。")
    print("=" * 50)


def main():
    """
    主函数
    """
    print("Session03 练习题1：基础运算练习")
    print("\n请在上面的函数中实现你的代码，然后运行测试。")
    print("\n提示：")
    print("1. 仔细阅读每个函数的文档字符串")
    print("2. 考虑边界情况和错误处理")
    print("3. 使用适当的算术运算符")
    print("4. 测试你的实现是否正确")
    
    # 运行测试
    test_functions()


if __name__ == "__main__":
    main()