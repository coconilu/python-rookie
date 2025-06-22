#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session10: 模块与包 - 主演示代码

本文件演示了Python模块和包的基本用法和实际应用。

作者: Python教程团队
创建日期: 2024-01-01
最后修改: 2024-01-01
"""

import sys
import os
from datetime import datetime, timedelta
import math
import random
import json


def demonstrate_standard_library():
    """
    演示标准库模块的使用
    """
    print("=== 标准库模块演示 ===")
    
    # os模块 - 操作系统接口
    print(f"当前工作目录: {os.getcwd()}")
    print(f"用户主目录: {os.path.expanduser('~')}")
    
    # sys模块 - 系统参数
    print(f"Python版本: {sys.version.split()[0]}")
    print(f"平台: {sys.platform}")
    
    # datetime模块 - 日期时间
    now = datetime.now()
    print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    
    future = now + timedelta(days=7, hours=3)
    print(f"一周零3小时后: {future.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # math模块 - 数学函数
    print(f"π的值: {math.pi:.6f}")
    print(f"e的值: {math.e:.6f}")
    print(f"√16 = {math.sqrt(16)}")
    print(f"2^10 = {math.pow(2, 10)}")
    
    # random模块 - 随机数
    print(f"随机整数(1-100): {random.randint(1, 100)}")
    print(f"随机浮点数: {random.random():.4f}")
    
    colors = ['红', '绿', '蓝', '黄', '紫']
    print(f"随机选择颜色: {random.choice(colors)}")
    
    # json模块 - JSON处理
    data = {
        'name': '张三',
        'age': 25,
        'skills': ['Python', 'JavaScript', 'SQL']
    }
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    print(f"JSON字符串:\n{json_str}")
    
    print()


def demonstrate_import_methods():
    """
    演示不同的导入方法
    """
    print("=== 导入方法演示 ===")
    
    # 方法1: 导入整个模块
    import math as m
    result1 = m.sqrt(25)
    print(f"使用别名导入: math.sqrt(25) = {result1}")
    
    # 方法2: 导入特定函数
    from random import randint, choice
    result2 = randint(1, 10)
    print(f"导入特定函数: randint(1, 10) = {result2}")
    
    # 方法3: 导入多个函数
    from datetime import date, time, datetime as dt
    today = date.today()
    print(f"今天的日期: {today}")
    
    # 演示模块搜索路径
    print(f"\n模块搜索路径前3个:")
    for i, path in enumerate(sys.path[:3]):
        print(f"  {i+1}. {path}")
    
    print()


def create_simple_module_demo():
    """
    演示创建简单模块的概念
    """
    print("=== 模块创建概念演示 ===")
    
    # 模拟一个简单的数学工具模块
    class MathUtils:
        """数学工具类 - 模拟模块功能"""
        
        PI = 3.14159
        VERSION = "1.0.0"
        
        @staticmethod
        def add(a, b):
            """加法"""
            return a + b
        
        @staticmethod
        def multiply(a, b):
            """乘法"""
            return a * b
        
        @staticmethod
        def circle_area(radius):
            """计算圆面积"""
            return MathUtils.PI * radius * radius
        
        @staticmethod
        def factorial(n):
            """计算阶乘"""
            if n < 0:
                raise ValueError("阶乘的参数必须是非负整数")
            if n == 0 or n == 1:
                return 1
            return n * MathUtils.factorial(n - 1)
    
    # 使用模拟的模块
    print(f"模块版本: {MathUtils.VERSION}")
    print(f"PI的值: {MathUtils.PI}")
    print(f"5 + 3 = {MathUtils.add(5, 3)}")
    print(f"4 * 7 = {MathUtils.multiply(4, 7)}")
    print(f"半径为3的圆面积: {MathUtils.circle_area(3):.2f}")
    print(f"5的阶乘: {MathUtils.factorial(5)}")
    
    print()


def demonstrate_package_concept():
    """
    演示包的概念
    """
    print("=== 包的概念演示 ===")
    
    # 模拟包的结构
    class PackageDemo:
        """模拟包的功能组织"""
        
        class MathUtils:
            """数学工具模块"""
            @staticmethod
            def add(a, b):
                return a + b
            
            @staticmethod
            def is_prime(n):
                if n < 2:
                    return False
                for i in range(2, int(n ** 0.5) + 1):
                    if n % i == 0:
                        return False
                return True
        
        class StringUtils:
            """字符串工具模块"""
            @staticmethod
            def reverse(s):
                return s[::-1]
            
            @staticmethod
            def count_words(text):
                return len(text.split())
            
            @staticmethod
            def is_palindrome(s):
                s = s.lower().replace(' ', '')
                return s == s[::-1]
        
        class FileUtils:
            """文件工具模块"""
            @staticmethod
            def get_extension(filename):
                return os.path.splitext(filename)[1]
            
            @staticmethod
            def get_basename(filepath):
                return os.path.basename(filepath)
    
    # 使用模拟的包
    pkg = PackageDemo()
    
    print("数学工具:")
    print(f"  10 + 15 = {pkg.MathUtils.add(10, 15)}")
    print(f"  17是质数吗? {pkg.MathUtils.is_prime(17)}")
    print(f"  20是质数吗? {pkg.MathUtils.is_prime(20)}")
    
    print("\n字符串工具:")
    text = "Hello World"
    print(f"  原字符串: {text}")
    print(f"  反转后: {pkg.StringUtils.reverse(text)}")
    print(f"  单词数: {pkg.StringUtils.count_words(text)}")
    print(f"  'level'是回文吗? {pkg.StringUtils.is_palindrome('level')}")
    
    print("\n文件工具:")
    filepath = "/home/user/document.txt"
    print(f"  文件路径: {filepath}")
    print(f"  文件扩展名: {pkg.FileUtils.get_extension(filepath)}")
    print(f"  文件名: {pkg.FileUtils.get_basename(filepath)}")
    
    print()


def demonstrate_module_attributes():
    """
    演示模块属性和内省
    """
    print("=== 模块属性演示 ===")
    
    # 查看模块属性
    print(f"当前模块名: {__name__}")
    print(f"当前文件路径: {__file__}")
    
    # 查看math模块的属性
    print("\nmath模块的部分属性:")
    math_attrs = [attr for attr in dir(math) if not attr.startswith('_')][:10]
    for attr in math_attrs:
        print(f"  {attr}: {getattr(math, attr)}")
    
    # 使用help()查看模块信息（简化版）
    print("\n模块文档字符串示例:")
    print(f"math模块文档: {math.__doc__[:100]}...")
    
    print()


def practical_example():
    """
    实际应用示例：日志分析器
    """
    print("=== 实际应用示例：简单日志分析 ===")
    
    # 模拟日志数据
    log_entries = [
        "2024-01-01 10:30:15 INFO 用户登录成功",
        "2024-01-01 10:31:22 ERROR 数据库连接失败",
        "2024-01-01 10:32:10 INFO 用户查看商品列表",
        "2024-01-01 10:33:45 WARNING 内存使用率过高",
        "2024-01-01 10:34:12 INFO 用户退出登录",
        "2024-01-01 10:35:33 ERROR 支付接口超时"
    ]
    
    # 使用多个标准库模块进行分析
    from collections import Counter
    import re
    
    print(f"总日志条数: {len(log_entries)}")
    
    # 统计日志级别
    levels = []
    for entry in log_entries:
        match = re.search(r'(INFO|ERROR|WARNING)', entry)
        if match:
            levels.append(match.group(1))
    
    level_counts = Counter(levels)
    print("\n日志级别统计:")
    for level, count in level_counts.items():
        print(f"  {level}: {count}条")
    
    # 提取时间信息
    times = []
    for entry in log_entries:
        time_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', entry)
        if time_match:
            times.append(time_match.group(1))
    
    print(f"\n时间范围: {times[0]} 到 {times[-1]}")
    
    # 查找错误日志
    error_logs = [entry for entry in log_entries if 'ERROR' in entry]
    print(f"\n错误日志 ({len(error_logs)}条):")
    for error in error_logs:
        print(f"  {error}")
    
    print()


def main():
    """
    主函数：演示程序的入口点
    """
    print("Session10: 模块与包演示")
    print("=" * 50)
    
    # 执行各种演示
    demonstrate_standard_library()
    demonstrate_import_methods()
    create_simple_module_demo()
    demonstrate_package_concept()
    demonstrate_module_attributes()
    practical_example()
    
    print("=" * 50)
    print("演示完成！")
    print("\n学习要点:")
    print("1. 模块是包含Python代码的文件")
    print("2. 包是包含多个模块的目录")
    print("3. import语句有多种用法")
    print("4. 标准库提供了丰富的功能")
    print("5. 良好的模块设计能提高代码复用性")


if __name__ == "__main__":
    main()