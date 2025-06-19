#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session02 示例1：基本变量操作

本示例演示了Python中变量的基本使用方法，包括：
- 变量的定义和赋值
- 不同数据类型的变量
- 变量的重新赋值和类型改变

作者: Python教程团队
创建日期: 2024-12-19
"""

def main():
    """演示基本变量操作"""
    print("=== 基本变量操作示例 ===")
    
    # 1. 创建不同类型的变量
    print("\n1. 创建不同类型的变量")
    name = "Python"          # 字符串
    version = 3.11           # 浮点数
    year = 2024             # 整数
    is_popular = True       # 布尔值
    
    print(f"编程语言: {name}")
    print(f"版本: {version}")
    print(f"年份: {year}")
    print(f"受欢迎: {is_popular}")
    
    # 2. 查看变量类型
    print("\n2. 查看变量类型")
    print(f"name 的类型: {type(name)}")
    print(f"version 的类型: {type(version)}")
    print(f"year 的类型: {type(year)}")
    print(f"is_popular 的类型: {type(is_popular)}")
    
    # 3. 变量重新赋值
    print("\n3. 变量重新赋值")
    print(f"修改前 year = {year}")
    year = 2025
    print(f"修改后 year = {year}")
    
    # 4. 变量类型改变
    print("\n4. 变量类型改变")
    x = 100
    print(f"x = {x}, 类型: {type(x)}")
    
    x = "现在是字符串"
    print(f"x = {x}, 类型: {type(x)}")
    
    x = 3.14
    print(f"x = {x}, 类型: {type(x)}")
    
    # 5. 多重赋值
    print("\n5. 多重赋值")
    a, b, c = 10, 20, 30
    print(f"a = {a}, b = {b}, c = {c}")
    
    # 6. 变量交换
    print("\n6. 变量交换")
    print(f"交换前: a = {a}, b = {b}")
    a, b = b, a
    print(f"交换后: a = {a}, b = {b}")
    
    # 7. 链式赋值
    print("\n7. 链式赋值")
    x = y = z = 999
    print(f"x = {x}, y = {y}, z = {z}")

if __name__ == "__main__":
    main()