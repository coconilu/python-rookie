#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session01: 环境搭建与Hello World - 演示代码

本文件演示了Python的基本语法和核心概念，包括：
- 输出函数的使用
- 输入函数的使用
- 变量的定义和使用
- 基本的数据类型
- 注释的编写

作者: Python教程团队
创建日期: 2024-01-01
最后修改: 2024-01-01
"""


def main():
    """
    主函数：演示程序的入口点
    """
    print("Session01: 环境搭建与Hello World演示")
    print("=" * 40)
    
    # 演示基本输出
    demo_basic_output()
    
    # 演示变量使用
    demo_variables()
    
    # 演示用户输入
    demo_user_input()
    
    # 演示简单计算
    demo_simple_calculation()
    
    print("\n演示完成！")


def demo_basic_output():
    """
    演示基本输出功能
    """
    print("\n1. 基本输出演示")
    print("-" * 20)
    
    # 基本输出
    print("Hello, World!")
    print("欢迎来到Python的世界！")
    
    # 输出多个值
    print("姓名:", "张三", "年龄:", 25)
    
    # 使用分隔符
    print("苹果", "香蕉", "橙子", sep=", ")
    
    # 使用结束符
    print("这是第一行", end=" ")
    print("这是第二行")


def demo_variables():
    """
    演示变量的定义和使用
    """
    print("\n2. 变量演示")
    print("-" * 20)
    
    # 定义不同类型的变量
    name = "Python"  # 字符串
    version = 3.11   # 浮点数
    year = 2024      # 整数
    is_awesome = True  # 布尔值
    
    # 输出变量
    print(f"编程语言: {name}")
    print(f"版本号: {version}")
    print(f"年份: {year}")
    print(f"是否很棒: {is_awesome}")
    
    # 变量类型
    print(f"\n变量类型:")
    print(f"name的类型: {type(name)}")
    print(f"version的类型: {type(version)}")
    print(f"year的类型: {type(year)}")
    print(f"is_awesome的类型: {type(is_awesome)}")


def demo_user_input():
    """
    演示用户输入功能
    """
    print("\n3. 用户输入演示")
    print("-" * 20)
    
    # 获取用户姓名
    user_name = input("请输入你的姓名: ")
    print(f"你好, {user_name}!")
    
    # 获取用户年龄（需要类型转换）
    try:
        user_age = int(input("请输入你的年龄: "))
        print(f"你今年 {user_age} 岁")
        
        # 计算明年年龄
        next_year_age = user_age + 1
        print(f"明年你将 {next_year_age} 岁")
        
    except ValueError:
        print("请输入有效的数字！")


def demo_simple_calculation():
    """
    演示简单的数学计算
    """
    print("\n4. 简单计算演示")
    print("-" * 20)
    
    # 定义两个数字
    a = 10
    b = 3
    
    print(f"数字a = {a}")
    print(f"数字b = {b}")
    print()
    
    # 基本运算
    print(f"加法: {a} + {b} = {a + b}")
    print(f"减法: {a} - {b} = {a - b}")
    print(f"乘法: {a} × {b} = {a * b}")
    print(f"除法: {a} ÷ {b} = {a / b:.2f}")
    print(f"整除: {a} // {b} = {a // b}")
    print(f"取余: {a} % {b} = {a % b}")
    print(f"幂运算: {a} ** {b} = {a ** b}")


def demo_string_formatting():
    """
    演示字符串格式化
    """
    print("\n5. 字符串格式化演示")
    print("-" * 20)
    
    name = "小明"
    age = 20
    score = 95.5
    
    # 不同的格式化方法
    print("方法1 - 使用%格式化:")
    print("姓名: %s, 年龄: %d, 成绩: %.1f" % (name, age, score))
    
    print("\n方法2 - 使用.format()方法:")
    print("姓名: {}, 年龄: {}, 成绩: {:.1f}".format(name, age, score))
    
    print("\n方法3 - 使用f-string (推荐):")
    print(f"姓名: {name}, 年龄: {age}, 成绩: {score:.1f}")


if __name__ == "__main__":
    # 程序入口点
    main()
    
    # 额外演示
    demo_string_formatting()
    
    print("\n" + "=" * 40)
    print("感谢使用Python！继续学习下一课吧！")
    print("=" * 40)