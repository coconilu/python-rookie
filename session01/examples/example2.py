#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session01 示例2: 变量和数据类型基础

这个示例展示了Python中基本数据类型的使用
"""

# 整数类型 (int)
age = 25
student_count = 100
year = 2024

print("=== 整数类型演示 ===")
print(f"年龄: {age}")
print(f"学生数量: {student_count}")
print(f"年份: {year}")
print(f"age的类型: {type(age)}")
print()

# 浮点数类型 (float)
height = 175.5
weight = 68.2
temperature = 36.7

print("=== 浮点数类型演示 ===")
print(f"身高: {height} cm")
print(f"体重: {weight} kg")
print(f"体温: {temperature} °C")
print(f"height的类型: {type(height)}")
print()

# 字符串类型 (str)
name = "张三"
city = "北京"
email = "zhangsan@example.com"

print("=== 字符串类型演示 ===")
print(f"姓名: {name}")
print(f"城市: {city}")
print(f"邮箱: {email}")
print(f"name的类型: {type(name)}")
print()

# 布尔类型 (bool)
is_student = True
is_graduated = False
has_job = True

print("=== 布尔类型演示 ===")
print(f"是学生: {is_student}")
print(f"已毕业: {is_graduated}")
print(f"有工作: {has_job}")
print(f"is_student的类型: {type(is_student)}")
print()

# 变量重新赋值
print("=== 变量重新赋值演示 ===")
value = 10
print(f"初始值: {value}, 类型: {type(value)}")

value = 3.14
print(f"重新赋值后: {value}, 类型: {type(value)}")

value = "Hello"
print(f"再次赋值后: {value}, 类型: {type(value)}")
print()

# 变量命名规范示例
print("=== 变量命名规范 ===")
# 好的命名
user_name = "李四"
max_score = 100
total_students = 50
is_valid = True

print(f"用户名: {user_name}")
print(f"最高分: {max_score}")
print(f"学生总数: {total_students}")
print(f"是否有效: {is_valid}")
print()

# 常量（按约定使用大写）
PI = 3.14159
MAX_ATTEMPTS = 3
DEFAULT_TIMEOUT = 30

print("=== 常量演示 ===")
print(f"圆周率: {PI}")
print(f"最大尝试次数: {MAX_ATTEMPTS}")
print(f"默认超时时间: {DEFAULT_TIMEOUT}秒")
print()

# 多个变量同时赋值
print("=== 多变量赋值 ===")
x, y, z = 1, 2, 3
print(f"x = {x}, y = {y}, z = {z}")

a = b = c = 0
print(f"a = {a}, b = {b}, c = {c}")
print()

# 变量交换
print("=== 变量交换 ===")
num1 = 10
num2 = 20
print(f"交换前: num1 = {num1}, num2 = {num2}")

# Python特有的交换方式
num1, num2 = num2, num1
print(f"交换后: num1 = {num1}, num2 = {num2}")