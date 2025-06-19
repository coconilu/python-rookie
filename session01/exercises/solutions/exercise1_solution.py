#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session01 练习题1：Hello World变体练习 - 参考答案

这是练习题1的参考答案，展示了多种实现方式。
"""

def solution():
    """
    练习题1的参考解决方案
    """
    # 1. 基本输出
    print("Hello, Python!")
    
    # 2. 使用变量存储信息
    my_name = "张三"
    today_date = "2024-01-01"
    favorite_language = "Python"
    
    # 3. 使用不同的格式化方法输出
    
    # 方法1: 使用f-string（推荐）
    print(f"我的姓名是：{my_name}")
    
    # 方法2: 使用.format()方法
    print("今天的日期是：{}".format(today_date))
    
    # 方法3: 使用%格式化
    print("我最喜欢的编程语言是：%s" % favorite_language)
    
    # 4. 添加装饰性输出
    print("=" * 19)
    print("欢迎来到编程世界！")
    print("=" * 19)


def solution_advanced():
    """
    进阶版本：更多样化的输出方式
    """
    print("=== 进阶版本 ===")
    
    # 使用多行字符串
    greeting = """
    ╔══════════════════════╗
    ║    Hello, Python!    ║
    ╚══════════════════════╝
    """
    print(greeting)
    
    # 个人信息
    info = {
        "name": "李四",
        "date": "2024-01-01",
        "language": "Python",
        "version": "3.11"
    }
    
    # 使用字典格式化
    print("姓名: {name}".format(**info))
    print(f"日期: {info['date']}")
    print(f"喜欢的语言: {info['language']} {info['version']}")
    
    # 创意输出
    languages = ["Python", "Java", "C++", "JavaScript"]
    print("\n我学过的编程语言：")
    for i, lang in enumerate(languages, 1):
        print(f"{i}. {lang}")
    
    # ASCII艺术
    python_art = """
         ____        _   _               
        |  _ \ _   _| |_| |__   ___  _ __  
        | |_) | | | | __| '_ \ / _ \| '_ \ 
        |  __/| |_| | |_| | | | (_) | | | |
        |_|    \__, |\__|_| |_|\___/|_| |_|
               |___/                     
    """
    print(python_art)


if __name__ == "__main__":
    print("=== 基础版本 ===")
    solution()
    
    print("\n")
    solution_advanced()