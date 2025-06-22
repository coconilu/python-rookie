#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session 06: 函数编程 - 示例1：函数基础

本文件演示函数的基本定义、调用和文档字符串的使用。
包括简单函数、带参数函数和函数命名规范。

作者: Python教程团队
创建日期: 2024-12-22
"""

import math


def main():
    """
    主函数：演示函数基础概念
    """
    print("函数基础示例")
    print("=" * 40)
    
    # 1. 简单函数演示
    print("\n1. 简单函数演示")
    simple_function_demo()
    
    # 2. 带参数函数演示
    print("\n2. 带参数函数演示")
    parameter_function_demo()
    
    # 3. 数学计算函数演示
    print("\n3. 数学计算函数演示")
    math_function_demo()
    
    # 4. 字符串处理函数演示
    print("\n4. 字符串处理函数演示")
    string_function_demo()
    
    print("\n示例演示完成！")


# ==================== 简单函数 ====================

def say_hello():
    """
    简单的问候函数（无参数，无返回值）
    """
    print("Hello, World!")
    print("欢迎学习Python函数！")


def get_current_time():
    """
    获取当前时间（无参数，有返回值）
    
    返回:
        str: 当前时间字符串
    """
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def generate_greeting():
    """
    生成问候语（无参数，有返回值）
    
    返回:
        str: 问候语字符串
    """
    return "欢迎来到Python函数的世界！"


def simple_function_demo():
    """
    演示简单函数的使用
    """
    # 调用无返回值函数
    say_hello()
    
    # 调用有返回值函数
    current_time = get_current_time()
    print(f"当前时间: {current_time}")
    
    greeting = generate_greeting()
    print(f"问候语: {greeting}")


# ==================== 带参数函数 ====================

def greet_person(name):
    """
    问候指定的人（单个参数）
    
    参数:
        name (str): 要问候的人的姓名
    
    返回:
        str: 个性化问候语
    """
    return f"Hello, {name}! 很高兴见到你！"


def introduce_person(name, age):
    """
    介绍一个人（多个参数）
    
    参数:
        name (str): 姓名
        age (int): 年龄
    
    返回:
        str: 介绍语句
    """
    return f"这是{name}，今年{age}岁。"


def create_full_introduction(name, age, city, hobby):
    """
    创建完整的自我介绍（多个参数）
    
    参数:
        name (str): 姓名
        age (int): 年龄
        city (str): 城市
        hobby (str): 爱好
    
    返回:
        str: 完整的自我介绍
    """
    intro = f"大家好，我叫{name}，今年{age}岁，来自{city}。"
    intro += f"我的爱好是{hobby}。很高兴认识大家！"
    return intro


def parameter_function_demo():
    """
    演示带参数函数的使用
    """
    # 单个参数
    greeting = greet_person("Alice")
    print(greeting)
    
    # 多个参数
    introduction = introduce_person("Bob", 25)
    print(introduction)
    
    # 更多参数
    full_intro = create_full_introduction("Charlie", 30, "北京", "编程")
    print(full_intro)


# ==================== 数学计算函数 ====================

def calculate_area_rectangle(length, width):
    """
    计算矩形面积
    
    参数:
        length (float): 长度
        width (float): 宽度
    
    返回:
        float: 矩形面积
    """
    return length * width


def calculate_area_circle(radius):
    """
    计算圆形面积
    
    参数:
        radius (float): 半径
    
    返回:
        float: 圆形面积
    """
    return math.pi * radius ** 2


def calculate_area_triangle(base, height):
    """
    计算三角形面积
    
    参数:
        base (float): 底边长度
        height (float): 高度
    
    返回:
        float: 三角形面积
    """
    return 0.5 * base * height


def calculate_bmi(weight, height):
    """
    计算身体质量指数(BMI)
    
    参数:
        weight (float): 体重（千克）
        height (float): 身高（米）
    
    返回:
        float: BMI值
    """
    return weight / (height ** 2)


def interpret_bmi(bmi):
    """
    解释BMI值
    
    参数:
        bmi (float): BMI值
    
    返回:
        str: BMI解释
    """
    if bmi < 18.5:
        return "体重过轻"
    elif bmi < 24:
        return "正常体重"
    elif bmi < 28:
        return "超重"
    else:
        return "肥胖"


def math_function_demo():
    """
    演示数学计算函数
    """
    # 面积计算
    rect_area = calculate_area_rectangle(5, 3)
    print(f"矩形面积 (5x3): {rect_area}")
    
    circle_area = calculate_area_circle(4)
    print(f"圆形面积 (半径4): {circle_area:.2f}")
    
    triangle_area = calculate_area_triangle(6, 4)
    print(f"三角形面积 (底6高4): {triangle_area}")
    
    # BMI计算
    weight = 70  # 千克
    height = 1.75  # 米
    bmi = calculate_bmi(weight, height)
    bmi_interpretation = interpret_bmi(bmi)
    print(f"\nBMI计算: 体重{weight}kg, 身高{height}m")
    print(f"BMI值: {bmi:.2f} ({bmi_interpretation})")


# ==================== 字符串处理函数 ====================

def count_characters(text):
    """
    统计字符数量
    
    参数:
        text (str): 输入文本
    
    返回:
        int: 字符数量
    """
    return len(text)


def count_words(text):
    """
    统计单词数量
    
    参数:
        text (str): 输入文本
    
    返回:
        int: 单词数量
    """
    words = text.split()
    return len(words)


def reverse_string(text):
    """
    反转字符串
    
    参数:
        text (str): 输入文本
    
    返回:
        str: 反转后的文本
    """
    return text[::-1]


def capitalize_words(text):
    """
    将每个单词的首字母大写
    
    参数:
        text (str): 输入文本
    
    返回:
        str: 处理后的文本
    """
    return text.title()


def remove_spaces(text):
    """
    移除所有空格
    
    参数:
        text (str): 输入文本
    
    返回:
        str: 移除空格后的文本
    """
    return text.replace(" ", "")


def is_palindrome(text):
    """
    检查是否为回文
    
    参数:
        text (str): 输入文本
    
    返回:
        bool: 是否为回文
    """
    # 转换为小写并移除空格
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]


def string_function_demo():
    """
    演示字符串处理函数
    """
    sample_text = "hello world python programming"
    
    print(f"原始文本: '{sample_text}'")
    print(f"字符数量: {count_characters(sample_text)}")
    print(f"单词数量: {count_words(sample_text)}")
    print(f"反转文本: '{reverse_string(sample_text)}'")
    print(f"首字母大写: '{capitalize_words(sample_text)}'")
    print(f"移除空格: '{remove_spaces(sample_text)}'")
    
    # 回文检查
    palindrome_tests = ["level", "hello", "A man a plan a canal Panama"]
    print("\n回文检查:")
    for test in palindrome_tests:
        result = is_palindrome(test)
        print(f"  '{test}': {'是' if result else '不是'}回文")


# ==================== 函数文档和帮助 ====================

def demonstrate_function_help():
    """
    演示如何查看函数文档
    """
    print("\n=== 函数文档演示 ===")
    
    # 查看函数的文档字符串
    print("calculate_bmi函数的文档:")
    print(calculate_bmi.__doc__)
    
    # 使用help()函数
    print("\n使用help()查看函数信息:")
    help(calculate_area_circle)


if __name__ == "__main__":
    main()
    
    # 额外演示：函数文档
    demonstrate_function_help()