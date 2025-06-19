#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session02: 变量与数据类型 - 演示代码

本文件演示了Python中变量的使用和四种基本数据类型的特点。
通过实际例子展示变量命名、类型转换、数据操作等核心概念。

作者: Python教程团队
创建日期: 2024-12-19
最后修改: 2024-12-19
"""

import sys
from typing import Union


def main():
    """
    主函数：演示变量与数据类型的基本用法
    """
    print("Session02: 变量与数据类型演示")
    print("=" * 40)
    
    # 演示各种数据类型
    demo_integer_type()
    demo_float_type()
    demo_string_type()
    demo_boolean_type()
    
    # 演示变量操作
    demo_variable_operations()
    demo_type_conversion()
    demo_naming_conventions()
    
    # 综合应用示例
    demo_practical_application()
    
    print("\n演示完成！")


def demo_integer_type():
    """
    演示整数类型的使用
    """
    print("\n1. 整数类型（int）演示")
    print("-" * 30)
    
    # 基本整数
    positive_num = 42
    negative_num = -17
    zero = 0
    
    print(f"正整数: {positive_num}, 类型: {type(positive_num)}")
    print(f"负整数: {negative_num}, 类型: {type(negative_num)}")
    print(f"零: {zero}, 类型: {type(zero)}")
    
    # 不同进制表示
    binary_num = 0b1010    # 二进制
    octal_num = 0o12       # 八进制
    hex_num = 0xa          # 十六进制
    
    print(f"\n不同进制表示（都等于十进制10）:")
    print(f"二进制 0b1010 = {binary_num}")
    print(f"八进制 0o12 = {octal_num}")
    print(f"十六进制 0xa = {hex_num}")
    
    # 整数运算
    a, b = 15, 4
    print(f"\n整数运算示例 (a={a}, b={b}):")
    print(f"加法: {a} + {b} = {a + b}")
    print(f"减法: {a} - {b} = {a - b}")
    print(f"乘法: {a} * {b} = {a * b}")
    print(f"除法: {a} / {b} = {a / b}")
    print(f"整除: {a} // {b} = {a // b}")
    print(f"取余: {a} % {b} = {a % b}")
    print(f"幂运算: {a} ** {b} = {a ** b}")


def demo_float_type():
    """
    演示浮点数类型的使用
    """
    print("\n2. 浮点数类型（float）演示")
    print("-" * 30)
    
    # 基本浮点数
    pi = 3.14159
    temperature = -2.5
    scientific = 1.23e-4  # 科学计数法
    
    print(f"圆周率: {pi}, 类型: {type(pi)}")
    print(f"温度: {temperature}°C, 类型: {type(temperature)}")
    print(f"科学计数法: {scientific}, 类型: {type(scientific)}")
    
    # 浮点数精度问题
    result = 0.1 + 0.2
    print(f"\n浮点数精度问题:")
    print(f"0.1 + 0.2 = {result}")
    print(f"四舍五入到1位小数: {round(result, 1)}")
    
    # 浮点数运算
    radius = 5.0
    area = pi * radius ** 2
    print(f"\n圆形面积计算:")
    print(f"半径: {radius}")
    print(f"面积: π × {radius}² = {area:.2f}")


def demo_string_type():
    """
    演示字符串类型的使用
    """
    print("\n3. 字符串类型（str）演示")
    print("-" * 30)
    
    # 不同的字符串定义方式
    single_quote = 'Hello World'
    double_quote = "Python Programming"
    triple_quote = """这是一个
多行字符串
可以包含换行符"""
    
    print(f"单引号字符串: {single_quote}")
    print(f"双引号字符串: {double_quote}")
    print(f"三引号字符串:\n{triple_quote}")
    
    # 字符串操作
    first_name = "张"
    last_name = "三"
    full_name = first_name + last_name
    
    print(f"\n字符串连接:")
    print(f"姓: {first_name}")
    print(f"名: {last_name}")
    print(f"全名: {full_name}")
    
    # 字符串格式化
    name = "李四"
    age = 30
    height = 175.5
    
    print(f"\n字符串格式化:")
    print(f"f-string: 我叫{name}，今年{age}岁，身高{height}cm")
    print("format方法: 我叫{}，今年{}岁，身高{}cm".format(name, age, height))
    print("百分号格式化: 我叫%s，今年%d岁，身高%.1fcm" % (name, age, height))
    
    # 字符串方法
    text = "  Python Programming  "
    print(f"\n字符串方法演示:")
    print(f"原字符串: '{text}'")
    print(f"去除空格: '{text.strip()}'")
    print(f"转大写: '{text.upper()}'")
    print(f"转小写: '{text.lower()}'")
    print(f"替换: '{text.replace('Python', 'Java')}'")
    print(f"分割: {text.strip().split(' ')}")
    print(f"长度: {len(text.strip())}")


def demo_boolean_type():
    """
    演示布尔类型的使用
    """
    print("\n4. 布尔类型（bool）演示")
    print("-" * 30)
    
    # 基本布尔值
    is_sunny = True
    is_raining = False
    
    print(f"今天晴天: {is_sunny}, 类型: {type(is_sunny)}")
    print(f"今天下雨: {is_raining}, 类型: {type(is_raining)}")
    
    # 比较运算产生布尔值
    age = 18
    score = 85
    
    print(f"\n比较运算产生布尔值:")
    print(f"年龄 {age} >= 18: {age >= 18}")
    print(f"分数 {score} > 90: {score > 90}")
    print(f"分数 {score} >= 60: {score >= 60}")
    
    # 逻辑运算
    is_adult = age >= 18
    is_excellent = score >= 90
    is_pass = score >= 60
    
    print(f"\n逻辑运算:")
    print(f"是成年人: {is_adult}")
    print(f"成绩优秀: {is_excellent}")
    print(f"成绩及格: {is_pass}")
    print(f"成年且优秀: {is_adult and is_excellent}")
    print(f"成年或优秀: {is_adult or is_excellent}")
    print(f"不是成年人: {not is_adult}")
    
    # 真值测试
    print(f"\n真值测试:")
    print(f"bool(1): {bool(1)}")
    print(f"bool(0): {bool(0)}")
    print(f"bool(''): {bool('')}")
    print(f"bool('hello'): {bool('hello')}")
    print(f"bool([]): {bool([])}")
    print(f"bool([1, 2]): {bool([1, 2])}")


def demo_variable_operations():
    """
    演示变量的基本操作
    """
    print("\n5. 变量操作演示")
    print("-" * 30)
    
    # 变量赋值
    x = 10
    print(f"初始值: x = {x}")
    
    # 重新赋值
    x = 20
    print(f"重新赋值: x = {x}")
    
    # 类型改变
    x = "Hello"
    print(f"类型改变: x = '{x}', 类型: {type(x)}")
    
    # 多重赋值
    a, b, c = 1, 2, 3
    print(f"\n多重赋值: a={a}, b={b}, c={c}")
    
    # 交换变量
    print(f"交换前: a={a}, b={b}")
    a, b = b, a
    print(f"交换后: a={a}, b={b}")
    
    # 链式赋值
    x = y = z = 100
    print(f"\n链式赋值: x={x}, y={y}, z={z}")


def demo_type_conversion():
    """
    演示类型转换
    """
    print("\n6. 类型转换演示")
    print("-" * 30)
    
    # 字符串转数字
    age_str = "25"
    price_str = "19.99"
    
    age_int = int(age_str)
    price_float = float(price_str)
    
    print(f"字符串转整数: '{age_str}' -> {age_int}")
    print(f"字符串转浮点数: '{price_str}' -> {price_float}")
    
    # 数字转字符串
    number = 42
    pi = 3.14159
    
    number_str = str(number)
    pi_str = str(pi)
    
    print(f"\n整数转字符串: {number} -> '{number_str}'")
    print(f"浮点数转字符串: {pi} -> '{pi_str}'")
    
    # 转换为布尔值
    print(f"\n转换为布尔值:")
    values = [0, 1, -1, "", "hello", [], [1, 2], None]
    for value in values:
        print(f"bool({repr(value)}) = {bool(value)}")
    
    # 类型转换错误处理
    print(f"\n类型转换错误处理:")
    invalid_strings = ["hello", "12.34.56", ""]
    for s in invalid_strings:
        try:
            result = int(s)
            print(f"int('{s}') = {result}")
        except ValueError as e:
            print(f"int('{s}') 转换失败: {e}")


def demo_naming_conventions():
    """
    演示变量命名规范
    """
    print("\n7. 变量命名规范演示")
    print("-" * 30)
    
    # 好的命名示例
    user_name = "张三"           # 使用下划线连接
    total_score = 95           # 有意义的名称
    is_valid_email = True      # 布尔变量用is开头
    MAX_RETRY_COUNT = 3        # 常量使用大写
    
    print("好的命名示例:")
    print(f"user_name = '{user_name}'")
    print(f"total_score = {total_score}")
    print(f"is_valid_email = {is_valid_email}")
    print(f"MAX_RETRY_COUNT = {MAX_RETRY_COUNT}")
    
    # 展示不同类型变量的命名模式
    print("\n不同类型变量的命名模式:")
    
    # 计数器
    student_count = 30
    print(f"计数器: student_count = {student_count}")
    
    # 标志位
    is_logged_in = False
    has_permission = True
    print(f"标志位: is_logged_in = {is_logged_in}, has_permission = {has_permission}")
    
    # 配置项
    database_host = "localhost"
    database_port = 3306
    print(f"配置项: database_host = '{database_host}', database_port = {database_port}")


def demo_practical_application():
    """
    演示实际应用场景
    """
    print("\n8. 实际应用演示")
    print("-" * 30)
    
    # 学生信息管理
    print("学生信息管理示例:")
    
    # 学生基本信息
    student_id = "2024001"
    student_name = "王小明"
    student_age = 20
    student_height = 175.5
    is_scholarship_recipient = True
    
    # 成绩信息
    math_score = 92.5
    english_score = 88.0
    python_score = 95.0
    
    # 计算平均分
    average_score = (math_score + english_score + python_score) / 3
    
    # 判断等级
    if average_score >= 90:
        grade = "优秀"
    elif average_score >= 80:
        grade = "良好"
    elif average_score >= 70:
        grade = "中等"
    elif average_score >= 60:
        grade = "及格"
    else:
        grade = "不及格"
    
    # 显示信息
    print(f"\n学号: {student_id}")
    print(f"姓名: {student_name}")
    print(f"年龄: {student_age}岁")
    print(f"身高: {student_height}cm")
    print(f"奖学金获得者: {'是' if is_scholarship_recipient else '否'}")
    print(f"\n成绩信息:")
    print(f"数学: {math_score}分")
    print(f"英语: {english_score}分")
    print(f"Python: {python_score}分")
    print(f"平均分: {average_score:.1f}分")
    print(f"等级: {grade}")
    
    # 简单的数据统计
    print(f"\n数据统计:")
    scores = [math_score, english_score, python_score]
    max_score = max(scores)
    min_score = min(scores)
    score_range = max_score - min_score
    
    print(f"最高分: {max_score}")
    print(f"最低分: {min_score}")
    print(f"分数差: {score_range}")


def get_type_info(value) -> str:
    """
    获取值的类型信息
    
    Args:
        value: 要检查的值
        
    Returns:
        str: 类型信息字符串
    """
    return f"值: {repr(value)}, 类型: {type(value).__name__}"


if __name__ == "__main__":
    main()