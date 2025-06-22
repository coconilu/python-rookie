#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example2: 自定义模块示例

演示如何创建和使用自定义模块
"""

import sys
import os
from datetime import datetime


# 模拟自定义模块的内容
class MathToolsModule:
    """
    模拟数学工具模块
    这个类模拟了一个独立的Python模块的功能
    """
    
    # 模块级常量
    PI = 3.14159265359
    E = 2.71828182846
    VERSION = "1.2.0"
    AUTHOR = "Python学习者"
    
    @staticmethod
    def add(a, b):
        """
        加法运算
        
        Args:
            a (float): 第一个数
            b (float): 第二个数
        
        Returns:
            float: 两数之和
        """
        return a + b
    
    @staticmethod
    def subtract(a, b):
        """减法运算"""
        return a - b
    
    @staticmethod
    def multiply(a, b):
        """乘法运算"""
        return a * b
    
    @staticmethod
    def divide(a, b):
        """
        除法运算
        
        Args:
            a (float): 被除数
            b (float): 除数
        
        Returns:
            float: 商
        
        Raises:
            ValueError: 当除数为0时
        """
        if b == 0:
            raise ValueError("除数不能为零")
        return a / b
    
    @staticmethod
    def power(base, exponent):
        """幂运算"""
        return base ** exponent
    
    @staticmethod
    def factorial(n):
        """
        计算阶乘
        
        Args:
            n (int): 非负整数
        
        Returns:
            int: n的阶乘
        
        Raises:
            ValueError: 当n为负数时
        """
        if not isinstance(n, int) or n < 0:
            raise ValueError("阶乘的参数必须是非负整数")
        
        if n == 0 or n == 1:
            return 1
        
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    @staticmethod
    def is_prime(n):
        """
        判断是否为质数
        
        Args:
            n (int): 要判断的数
        
        Returns:
            bool: 是否为质数
        """
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        for i in range(3, int(n ** 0.5) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    @staticmethod
    def gcd(a, b):
        """
        计算最大公约数（欧几里得算法）
        """
        while b:
            a, b = b, a % b
        return a
    
    @staticmethod
    def lcm(a, b):
        """
        计算最小公倍数
        """
        return abs(a * b) // MathToolsModule.gcd(a, b)
    
    @staticmethod
    def circle_area(radius):
        """计算圆的面积"""
        return MathToolsModule.PI * radius * radius
    
    @staticmethod
    def circle_circumference(radius):
        """计算圆的周长"""
        return 2 * MathToolsModule.PI * radius


class StringToolsModule:
    """
    模拟字符串工具模块
    """
    
    VERSION = "1.1.0"
    
    @staticmethod
    def reverse_string(s):
        """反转字符串"""
        return s[::-1]
    
    @staticmethod
    def count_words(text):
        """统计单词数量"""
        return len(text.split())
    
    @staticmethod
    def count_characters(text, include_spaces=True):
        """统计字符数量"""
        if include_spaces:
            return len(text)
        else:
            return len(text.replace(' ', ''))
    
    @staticmethod
    def capitalize_words(text):
        """将每个单词的首字母大写"""
        return ' '.join(word.capitalize() for word in text.split())
    
    @staticmethod
    def remove_spaces(text):
        """移除所有空格"""
        return text.replace(' ', '')
    
    @staticmethod
    def is_palindrome(s):
        """
        判断是否为回文字符串（忽略大小写和空格）
        """
        cleaned = s.lower().replace(' ', '').replace(',', '').replace('.', '')
        return cleaned == cleaned[::-1]
    
    @staticmethod
    def count_vowels(text):
        """统计元音字母数量"""
        vowels = 'aeiouAEIOU'
        return sum(1 for char in text if char in vowels)
    
    @staticmethod
    def extract_numbers(text):
        """从文本中提取数字"""
        import re
        return re.findall(r'\d+', text)
    
    @staticmethod
    def word_frequency(text):
        """统计单词频率"""
        words = text.lower().split()
        frequency = {}
        for word in words:
            # 移除标点符号
            clean_word = ''.join(char for char in word if char.isalnum())
            if clean_word:
                frequency[clean_word] = frequency.get(clean_word, 0) + 1
        return frequency


class FileToolsModule:
    """
    模拟文件工具模块
    """
    
    VERSION = "1.0.0"
    
    @staticmethod
    def get_file_extension(filename):
        """获取文件扩展名"""
        return os.path.splitext(filename)[1]
    
    @staticmethod
    def get_file_name(filepath):
        """获取文件名（不含路径）"""
        return os.path.basename(filepath)
    
    @staticmethod
    def get_file_directory(filepath):
        """获取文件所在目录"""
        return os.path.dirname(filepath)
    
    @staticmethod
    def file_exists(filepath):
        """检查文件是否存在"""
        return os.path.exists(filepath)
    
    @staticmethod
    def get_file_size(filepath):
        """
        获取文件大小（字节）
        
        Returns:
            int: 文件大小，如果文件不存在返回None
        """
        try:
            return os.path.getsize(filepath)
        except OSError:
            return None
    
    @staticmethod
    def create_backup_name(filename):
        """创建备份文件名"""
        name, ext = os.path.splitext(filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{name}_backup_{timestamp}{ext}"
    
    @staticmethod
    def list_files_by_extension(directory, extension):
        """
        列出指定目录中特定扩展名的文件
        """
        try:
            files = []
            for filename in os.listdir(directory):
                if filename.endswith(extension):
                    files.append(filename)
            return files
        except OSError:
            return []


def demonstrate_math_tools():
    """
    演示数学工具模块的使用
    """
    print("=== 数学工具模块演示 ===")
    
    # 使用模块信息
    print(f"模块版本: {MathToolsModule.VERSION}")
    print(f"模块作者: {MathToolsModule.AUTHOR}")
    print(f"PI值: {MathToolsModule.PI}")
    print(f"E值: {MathToolsModule.E}")
    
    # 基本运算
    print("\n基本运算:")
    print(f"  15 + 25 = {MathToolsModule.add(15, 25)}")
    print(f"  50 - 18 = {MathToolsModule.subtract(50, 18)}")
    print(f"  7 × 8 = {MathToolsModule.multiply(7, 8)}")
    print(f"  84 ÷ 12 = {MathToolsModule.divide(84, 12)}")
    print(f"  2^10 = {MathToolsModule.power(2, 10)}")
    
    # 高级运算
    print("\n高级运算:")
    print(f"  5! = {MathToolsModule.factorial(5)}")
    print(f"  17是质数吗? {MathToolsModule.is_prime(17)}")
    print(f"  20是质数吗? {MathToolsModule.is_prime(20)}")
    print(f"  gcd(48, 18) = {MathToolsModule.gcd(48, 18)}")
    print(f"  lcm(12, 8) = {MathToolsModule.lcm(12, 8)}")
    
    # 几何计算
    radius = 5
    print(f"\n几何计算（半径={radius}）:")
    print(f"  圆面积: {MathToolsModule.circle_area(radius):.2f}")
    print(f"  圆周长: {MathToolsModule.circle_circumference(radius):.2f}")
    
    print()


def demonstrate_string_tools():
    """
    演示字符串工具模块的使用
    """
    print("=== 字符串工具模块演示 ===")
    
    print(f"模块版本: {StringToolsModule.VERSION}")
    
    # 测试文本
    text = "Hello World Python Programming"
    print(f"\n原始文本: '{text}'")
    
    # 基本操作
    print("\n基本操作:")
    print(f"  反转: '{StringToolsModule.reverse_string(text)}'")
    print(f"  单词数: {StringToolsModule.count_words(text)}")
    print(f"  字符数（含空格）: {StringToolsModule.count_characters(text)}")
    print(f"  字符数（不含空格）: {StringToolsModule.count_characters(text, False)}")
    print(f"  首字母大写: '{StringToolsModule.capitalize_words(text.lower())}'")
    print(f"  移除空格: '{StringToolsModule.remove_spaces(text)}'")
    print(f"  元音字母数: {StringToolsModule.count_vowels(text)}")
    
    # 回文检测
    palindromes = ["level", "A man a plan a canal Panama", "race a car", "hello"]
    print("\n回文检测:")
    for word in palindromes:
        is_pal = StringToolsModule.is_palindrome(word)
        print(f"  '{word}' -> {is_pal}")
    
    # 数字提取
    text_with_numbers = "我有3个苹果，5个橙子，总共8个水果，花费了25元"
    numbers = StringToolsModule.extract_numbers(text_with_numbers)
    print(f"\n从'{text_with_numbers}'中提取的数字: {numbers}")
    
    # 词频统计
    sample_text = "Python is great. Python is powerful. Programming with Python is fun."
    frequency = StringToolsModule.word_frequency(sample_text)
    print(f"\n词频统计:")
    for word, count in sorted(frequency.items(), key=lambda x: x[1], reverse=True):
        print(f"  '{word}': {count}次")
    
    print()


def demonstrate_file_tools():
    """
    演示文件工具模块的使用
    """
    print("=== 文件工具模块演示 ===")
    
    print(f"模块版本: {FileToolsModule.VERSION}")
    
    # 文件路径分析
    filepaths = [
        "/home/user/documents/report.pdf",
        "C:\\Users\\Admin\\Desktop\\photo.jpg",
        "data.csv",
        "script.py"
    ]
    
    print("\n文件路径分析:")
    for filepath in filepaths:
        print(f"  文件路径: {filepath}")
        print(f"    文件名: {FileToolsModule.get_file_name(filepath)}")
        print(f"    目录: {FileToolsModule.get_file_directory(filepath)}")
        print(f"    扩展名: {FileToolsModule.get_file_extension(filepath)}")
        print(f"    存在: {FileToolsModule.file_exists(filepath)}")
        
        size = FileToolsModule.get_file_size(filepath)
        if size is not None:
            print(f"    大小: {size} 字节")
        else:
            print(f"    大小: 无法获取")
        
        backup_name = FileToolsModule.create_backup_name(FileToolsModule.get_file_name(filepath))
        print(f"    备份名: {backup_name}")
        print()
    
    # 列出当前目录的Python文件
    current_dir = "."
    python_files = FileToolsModule.list_files_by_extension(current_dir, ".py")
    print(f"当前目录的Python文件:")
    for py_file in python_files[:5]:  # 只显示前5个
        print(f"  {py_file}")
    if len(python_files) > 5:
        print(f"  ... 还有 {len(python_files) - 5} 个文件")
    
    print()


def demonstrate_module_integration():
    """
    演示多个模块的集成使用
    """
    print("=== 模块集成应用演示 ===")
    
    # 综合应用：分析一段文本
    text = "Python编程语言有25年的历史，它有3个主要版本。Python 2在2020年停止支持，现在我们使用Python 3。"
    
    print(f"分析文本: '{text}'")
    print()
    
    # 使用字符串工具分析
    print("文本分析结果:")
    print(f"  单词数量: {StringToolsModule.count_words(text)}")
    print(f"  字符数量: {StringToolsModule.count_characters(text)}")
    print(f"  元音字母: {StringToolsModule.count_vowels(text)}")
    
    # 提取数字并进行数学运算
    numbers = StringToolsModule.extract_numbers(text)
    print(f"  提取的数字: {numbers}")
    
    if len(numbers) >= 2:
        num1, num2 = int(numbers[0]), int(numbers[1])
        print(f"\n数学运算 ({num1} 和 {num2}):")
        print(f"  加法: {MathToolsModule.add(num1, num2)}")
        print(f"  乘法: {MathToolsModule.multiply(num1, num2)}")
        print(f"  最大公约数: {MathToolsModule.gcd(num1, num2)}")
    
    # 词频分析
    frequency = StringToolsModule.word_frequency(text)
    print(f"\n高频词汇:")
    sorted_words = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    for word, count in sorted_words[:5]:
        if count > 1:
            print(f"  '{word}': {count}次")
    
    print()


def main():
    """
    主函数
    """
    print("Example2: 自定义模块示例")
    print("=" * 50)
    
    demonstrate_math_tools()
    demonstrate_string_tools()
    demonstrate_file_tools()
    demonstrate_module_integration()
    
    print("=" * 50)
    print("示例完成！")
    print("\n模块设计要点:")
    print("1. 模块应该有明确的功能定位")
    print("2. 提供清晰的文档和注释")
    print("3. 包含版本信息和作者信息")
    print("4. 函数应该有适当的错误处理")
    print("5. 模块之间可以相互配合使用")


if __name__ == "__main__":
    main()