#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solution 2: 自定义模块练习参考答案

这个文件包含了exercise2.py中所有练习的参考答案
"""

import re
import os
import time
from datetime import datetime
from collections import Counter


# 练习1：创建数学工具模块
def exercise_1_create_math_module():
    """
    练习1：创建数学工具模块 - 参考答案
    """
    print("=== 练习1：创建数学工具模块 - 参考答案 ===")
    
    class MathTools:
        """
        数学工具模块
        提供常用的数学计算功能
        """
        
        # 模块信息
        __version__ = "1.0.0"
        __author__ = "Python学习者"
        
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
                TypeError: 当n不是整数时
            """
            # 检查输入类型
            if not isinstance(n, int):
                raise TypeError("输入必须是整数")
            
            # 检查输入值
            if n < 0:
                raise ValueError("输入不能为负数")
            
            # 计算阶乘
            if n == 0 or n == 1:
                return 1
            
            result = 1
            for i in range(2, n + 1):
                result *= i
            return result
        
        @staticmethod
        def gcd(a, b):
            """
            计算最大公约数（使用欧几里得算法）
            
            Args:
                a (int): 第一个整数
                b (int): 第二个整数
            
            Returns:
                int: a和b的最大公约数
            """
            # 确保a和b都是正数
            a, b = abs(a), abs(b)
            
            # 欧几里得算法
            while b:
                a, b = b, a % b
            return a
        
        @staticmethod
        def lcm(a, b):
            """
            计算最小公倍数
            
            Args:
                a (int): 第一个整数
                b (int): 第二个整数
            
            Returns:
                int: a和b的最小公倍数
            """
            if a == 0 or b == 0:
                return 0
            return abs(a * b) // MathTools.gcd(a, b)
        
        @staticmethod
        def is_prime(n):
            """
            判断是否为质数
            
            Args:
                n (int): 要检查的整数
            
            Returns:
                bool: 如果是质数返回True，否则返回False
            """
            if n < 2:
                return False
            if n == 2:
                return True
            if n % 2 == 0:
                return False
            
            # 只需要检查到sqrt(n)
            for i in range(3, int(n ** 0.5) + 1, 2):
                if n % i == 0:
                    return False
            return True
        
        @staticmethod
        def prime_factors(n):
            """
            计算质因数分解
            
            Args:
                n (int): 要分解的正整数
            
            Returns:
                list: 质因数列表
            """
            if n <= 1:
                return []
            
            factors = []
            d = 2
            
            while d * d <= n:
                while n % d == 0:
                    factors.append(d)
                    n //= d
                d += 1
            
            if n > 1:
                factors.append(n)
            
            return factors
        
        @staticmethod
        def fibonacci_sequence(n):
            """
            生成斐波那契数列
            
            Args:
                n (int): 数列长度
            
            Returns:
                list: 斐波那契数列
            """
            if n <= 0:
                return []
            elif n == 1:
                return [0]
            elif n == 2:
                return [0, 1]
            
            fib = [0, 1]
            for i in range(2, n):
                fib.append(fib[i-1] + fib[i-2])
            
            return fib
        
        @staticmethod
        def power_mod(base, exponent, modulus):
            """
            计算模幂运算：(base^exponent) % modulus
            使用快速幂算法提高效率
            
            Args:
                base (int): 底数
                exponent (int): 指数
                modulus (int): 模数
            
            Returns:
                int: 模幂运算结果
            """
            # 使用Python内置的pow函数，它已经实现了快速幂算法
            return pow(base, exponent, modulus)
    
    # 测试数学工具模块
    print("测试MathTools模块:")
    
    # 测试阶乘
    test_numbers = [0, 1, 5, 10]
    print("阶乘测试:")
    for num in test_numbers:
        try:
            result = MathTools.factorial(num)
            print(f"  {num}! = {result}")
        except Exception as e:
            print(f"  {num}!: 错误 - {e}")
    
    # 测试最大公约数和最小公倍数
    test_pairs = [(12, 18), (15, 25), (7, 13)]
    print("\n最大公约数和最小公倍数测试:")
    for a, b in test_pairs:
        gcd_result = MathTools.gcd(a, b)
        lcm_result = MathTools.lcm(a, b)
        print(f"  gcd({a}, {b}) = {gcd_result}, lcm({a}, {b}) = {lcm_result}")
    
    # 测试质数判断
    test_primes = [2, 3, 4, 17, 25, 29]
    print("\n质数判断测试:")
    for num in test_primes:
        is_prime = MathTools.is_prime(num)
        print(f"  {num}: {'是' if is_prime else '不是'}质数")
    
    # 测试质因数分解
    test_factorization = [12, 60, 97]
    print("\n质因数分解测试:")
    for num in test_factorization:
        factors = MathTools.prime_factors(num)
        print(f"  {num} = {' × '.join(map(str, factors))}")
    
    # 测试斐波那契数列
    fib_10 = MathTools.fibonacci_sequence(10)
    print(f"\n斐波那契数列(前10项): {fib_10}")
    
    # 测试模幂运算
    mod_result = MathTools.power_mod(2, 10, 1000)
    print(f"2^10 mod 1000 = {mod_result}")
    
    print("练习1完成！\n")


# 练习2：创建字符串处理模块
def exercise_2_create_string_module():
    """
    练习2：创建字符串处理模块 - 参考答案
    """
    print("=== 练习2：创建字符串处理模块 - 参考答案 ===")
    
    class StringProcessor:
        """
        字符串处理模块
        提供各种字符串操作和分析功能
        """
        
        @staticmethod
        def word_count(text):
            """
            统计文本中的单词数量
            
            Args:
                text (str): 要分析的文本
            
            Returns:
                dict: 包含各种统计信息的字典
            """
            if not isinstance(text, str):
                return {'error': '输入必须是字符串'}
            
            # 分割单词（移除标点符号）
            words = re.findall(r'\b\w+\b', text.lower())
            
            if not words:
                return {
                    'total_words': 0,
                    'unique_words': 0,
                    'word_frequency': {},
                    'average_word_length': 0
                }
            
            # 计算统计信息
            word_frequency = Counter(words)
            total_words = len(words)
            unique_words = len(word_frequency)
            average_word_length = sum(len(word) for word in words) / total_words
            
            return {
                'total_words': total_words,
                'unique_words': unique_words,
                'word_frequency': dict(word_frequency),
                'average_word_length': round(average_word_length, 2)
            }
        
        @staticmethod
        def reverse_words(text, reverse_order=False):
            """
            反转单词
            
            Args:
                text (str): 输入文本
                reverse_order (bool): 是否反转单词顺序
            
            Returns:
                str: 处理后的文本
            """
            if not isinstance(text, str):
                return text
            
            words = text.split()
            
            if reverse_order:
                # 反转单词顺序
                return ' '.join(reversed(words))
            else:
                # 反转每个单词内的字符顺序
                return ' '.join(word[::-1] for word in words)
        
        @staticmethod
        def extract_numbers(text):
            """
            从文本中提取所有数字
            
            Args:
                text (str): 输入文本
            
            Returns:
                dict: 包含整数和浮点数列表的字典
            """
            if not isinstance(text, str):
                return {'integers': [], 'floats': []}
            
            # 提取浮点数（包括整数）
            float_pattern = r'-?\d+\.\d+'
            # 提取整数（不包括已经匹配的浮点数部分）
            int_pattern = r'-?\b\d+\b'
            
            floats = [float(match) for match in re.findall(float_pattern, text)]
            
            # 移除浮点数后再查找整数
            text_without_floats = re.sub(float_pattern, '', text)
            integers = [int(match) for match in re.findall(int_pattern, text_without_floats)]
            
            return {
                'integers': integers,
                'floats': floats
            }
        
        @staticmethod
        def text_statistics(text):
            """
            计算文本统计信息
            
            Args:
                text (str): 输入文本
            
            Returns:
                dict: 详细的文本统计信息
            """
            if not isinstance(text, str):
                return {'error': '输入必须是字符串'}
            
            # 基本统计
            total_chars = len(text)
            chars_no_spaces = len(text.replace(' ', ''))
            words = text.split()
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            paragraphs = text.split('\n\n')
            paragraphs = [p.strip() for p in paragraphs if p.strip()]
            
            # 计算平均值
            avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
            avg_sentence_length = sum(len(sentence.split()) for sentence in sentences) / len(sentences) if sentences else 0
            
            return {
                'total_characters': total_chars,
                'characters_no_spaces': chars_no_spaces,
                'words': len(words),
                'sentences': len(sentences),
                'paragraphs': len(paragraphs),
                'average_word_length': round(avg_word_length, 2),
                'average_sentence_length': round(avg_sentence_length, 2)
            }
        
        @staticmethod
        def format_text(text, style='title'):
            """
            格式化文本
            
            Args:
                text (str): 输入文本
                style (str): 格式化样式
            
            Returns:
                str: 格式化后的文本
            """
            if not isinstance(text, str):
                return text
            
            if style == 'title':
                return text.title()
            elif style == 'sentence':
                # 每个句子首字母大写
                sentences = re.split(r'([.!?]\s*)', text)
                result = []
                for i, part in enumerate(sentences):
                    if i % 2 == 0 and part.strip():  # 句子内容
                        result.append(part.strip().capitalize())
                    else:  # 标点符号
                        result.append(part)
                return ''.join(result)
            elif style == 'camel':
                # 驼峰格式
                words = re.findall(r'\w+', text)
                if not words:
                    return text
                return words[0].lower() + ''.join(word.capitalize() for word in words[1:])
            elif style == 'snake':
                # 下划线格式
                words = re.findall(r'\w+', text.lower())
                return '_'.join(words)
            elif style == 'kebab':
                # 短横线格式
                words = re.findall(r'\w+', text.lower())
                return '-'.join(words)
            else:
                return text
        
        @staticmethod
        def similarity(text1, text2, method='jaccard'):
            """
            计算两个文本的相似度
            
            Args:
                text1 (str): 第一个文本
                text2 (str): 第二个文本
                method (str): 相似度计算方法
            
            Returns:
                float: 相似度值（0-1之间）
            """
            if not isinstance(text1, str) or not isinstance(text2, str):
                return 0.0
            
            # 提取单词集合
            words1 = set(re.findall(r'\w+', text1.lower()))
            words2 = set(re.findall(r'\w+', text2.lower()))
            
            if method == 'jaccard':
                # Jaccard相似度
                intersection = words1.intersection(words2)
                union = words1.union(words2)
                return len(intersection) / len(union) if union else 0.0
            
            elif method == 'cosine':
                # 简化的余弦相似度
                intersection = words1.intersection(words2)
                if not words1 or not words2:
                    return 0.0
                return len(intersection) / (len(words1) * len(words2)) ** 0.5
            
            else:
                return 0.0
    
    # 测试字符串处理模块
    print("测试StringProcessor模块:")
    
    test_text = "Hello World! This is a test. Python is great for text processing."
    
    # 测试单词统计
    word_stats = StringProcessor.word_count(test_text)
    print(f"单词统计: {word_stats}")
    
    # 测试文本反转
    reversed_chars = StringProcessor.reverse_words(test_text, reverse_order=False)
    reversed_order = StringProcessor.reverse_words(test_text, reverse_order=True)
    print(f"\n字符反转: {reversed_chars}")
    print(f"顺序反转: {reversed_order}")
    
    # 测试数字提取
    number_text = "I have 5 apples, 3.14 pies, and -2 oranges."
    numbers = StringProcessor.extract_numbers(number_text)
    print(f"\n数字提取: {numbers}")
    
    # 测试文本统计
    stats = StringProcessor.text_statistics(test_text)
    print(f"\n文本统计: {stats}")
    
    # 测试文本格式化
    test_format = "hello world python programming"
    print(f"\n文本格式化:")
    print(f"  原文: {test_format}")
    print(f"  标题格式: {StringProcessor.format_text(test_format, 'title')}")
    print(f"  驼峰格式: {StringProcessor.format_text(test_format, 'camel')}")
    print(f"  下划线格式: {StringProcessor.format_text(test_format, 'snake')}")
    print(f"  短横线格式: {StringProcessor.format_text(test_format, 'kebab')}")
    
    # 测试相似度
    text1 = "Python is a programming language"
    text2 = "Java is a programming language"
    similarity = StringProcessor.similarity(text1, text2)
    print(f"\n相似度测试:")
    print(f"  文本1: '{text1}'")
    print(f"  文本2: '{text2}'")
    print(f"  Jaccard相似度: {similarity:.3f}")
    
    print("练习2完成！\n")


# 练习3：创建文件工具模块
def exercise_3_create_file_module():
    """
    练习3：创建文件工具模块 - 参考答案
    """
    print("=== 练习3：创建文件工具模块 - 参考答案 ===")
    
    class FileTools:
        """
        文件工具模块
        提供安全的文件操作和分析功能
        """
        
        @staticmethod
        def safe_read(file_path, encoding='utf-8'):
            """
            安全地读取文件内容
            
            Args:
                file_path (str): 文件路径
                encoding (str): 文件编码
            
            Returns:
                dict: 包含内容和状态信息的字典
            """
            result = {
                'success': False,
                'content': None,
                'error': None,
                'file_info': {}
            }
            
            try:
                # 检查文件是否存在
                if not os.path.exists(file_path):
                    result['error'] = '文件不存在'
                    return result
                
                # 获取文件信息
                stat = os.stat(file_path)
                result['file_info'] = {
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime),
                    'created': datetime.fromtimestamp(stat.st_ctime)
                }
                
                # 读取文件内容
                with open(file_path, 'r', encoding=encoding) as f:
                    result['content'] = f.read()
                    result['success'] = True
            
            except UnicodeDecodeError as e:
                result['error'] = f'编码错误: {e}'
            except PermissionError as e:
                result['error'] = f'权限错误: {e}'
            except Exception as e:
                result['error'] = f'未知错误: {e}'
            
            return result
        
        @staticmethod
        def analyze_file(file_path):
            """
            分析文件信息
            
            Args:
                file_path (str): 文件路径
            
            Returns:
                dict: 文件分析结果
            """
            if not os.path.exists(file_path):
                return {'error': '文件不存在'}
            
            try:
                stat = os.stat(file_path)
                
                analysis = {
                    'file_path': file_path,
                    'file_name': os.path.basename(file_path),
                    'file_size': stat.st_size,
                    'created_time': datetime.fromtimestamp(stat.st_ctime),
                    'modified_time': datetime.fromtimestamp(stat.st_mtime),
                    'file_extension': os.path.splitext(file_path)[1],
                    'is_text_file': False,
                    'line_count': None,
                    'character_count': None
                }
                
                # 尝试作为文本文件分析
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        analysis['is_text_file'] = True
                        analysis['line_count'] = len(content.splitlines())
                        analysis['character_count'] = len(content)
                except:
                    pass  # 不是文本文件或无法读取
                
                return analysis
            
            except Exception as e:
                return {'error': f'分析失败: {e}'}
        
        @staticmethod
        def backup_file(file_path, backup_dir=None):
            """
            备份文件
            
            Args:
                file_path (str): 要备份的文件路径
                backup_dir (str): 备份目录，如果为None则在原目录创建备份
            
            Returns:
                dict: 备份操作结果
            """
            if not os.path.exists(file_path):
                return {'success': False, 'error': '源文件不存在'}
            
            try:
                # 生成备份文件名
                base_name = os.path.basename(file_path)
                name, ext = os.path.splitext(base_name)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_name = f"{name}_backup_{timestamp}{ext}"
                
                # 确定备份路径
                if backup_dir:
                    if not os.path.exists(backup_dir):
                        os.makedirs(backup_dir)
                    backup_path = os.path.join(backup_dir, backup_name)
                else:
                    backup_path = os.path.join(os.path.dirname(file_path), backup_name)
                
                # 执行备份（这里只是模拟，不实际复制）
                return {
                    'success': True,
                    'backup_path': backup_path,
                    'original_path': file_path,
                    'message': f'备份将创建为: {backup_path}'
                }
            
            except Exception as e:
                return {'success': False, 'error': f'备份失败: {e}'}
        
        @staticmethod
        def find_files(directory, pattern='*', recursive=True):
            """
            查找文件
            
            Args:
                directory (str): 搜索目录
                pattern (str): 文件名模式
                recursive (bool): 是否递归搜索
            
            Returns:
                list: 找到的文件列表
            """
            import glob
            
            if not os.path.exists(directory):
                return []
            
            try:
                if recursive:
                    search_pattern = os.path.join(directory, '**', pattern)
                    return glob.glob(search_pattern, recursive=True)
                else:
                    search_pattern = os.path.join(directory, pattern)
                    return glob.glob(search_pattern)
            
            except Exception as e:
                print(f"搜索错误: {e}")
                return []
        
        @staticmethod
        def compare_files(file1, file2):
            """
            比较两个文件
            
            Args:
                file1 (str): 第一个文件路径
                file2 (str): 第二个文件路径
            
            Returns:
                dict: 比较结果
            """
            result = {
                'files_exist': False,
                'same_size': False,
                'same_content': False,
                'size_difference': 0,
                'content_difference': None
            }
            
            # 检查文件是否存在
            if not os.path.exists(file1) or not os.path.exists(file2):
                result['error'] = '一个或两个文件不存在'
                return result
            
            result['files_exist'] = True
            
            try:
                # 比较文件大小
                size1 = os.path.getsize(file1)
                size2 = os.path.getsize(file2)
                result['same_size'] = (size1 == size2)
                result['size_difference'] = abs(size1 - size2)
                
                # 如果大小相同，比较内容
                if result['same_size']:
                    try:
                        with open(file1, 'r', encoding='utf-8') as f1, \
                             open(file2, 'r', encoding='utf-8') as f2:
                            content1 = f1.read()
                            content2 = f2.read()
                            result['same_content'] = (content1 == content2)
                            
                            if not result['same_content']:
                                # 简单的差异统计
                                lines1 = content1.splitlines()
                                lines2 = content2.splitlines()
                                different_lines = sum(1 for l1, l2 in zip(lines1, lines2) if l1 != l2)
                                result['content_difference'] = {
                                    'different_lines': different_lines,
                                    'total_lines': max(len(lines1), len(lines2))
                                }
                    except UnicodeDecodeError:
                        # 二进制文件比较
                        with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
                            result['same_content'] = (f1.read() == f2.read())
                
                return result
            
            except Exception as e:
                result['error'] = f'比较失败: {e}'
                return result
    
    # 测试文件工具模块
    print("测试FileTools模块:")
    
    # 演示功能（不实际操作文件）
    print("文件工具模块功能演示:")
    
    # 模拟安全读取
    print("\n1. 安全读取文件:")
    read_result = FileTools.safe_read('nonexistent.txt')
    print(f"   结果: {read_result}")
    
    # 模拟文件分析
    print("\n2. 文件分析:")
    if os.path.exists(__file__):
        analysis = FileTools.analyze_file(__file__)
        print(f"   当前文件分析: {analysis}")
    
    # 模拟备份
    print("\n3. 文件备份:")
    backup_result = FileTools.backup_file('example.txt')
    print(f"   备份结果: {backup_result}")
    
    # 模拟文件查找
    print("\n4. 文件查找:")
    found_files = FileTools.find_files('.', '*.py', recursive=False)
    print(f"   找到的Python文件: {found_files[:3]}{'...' if len(found_files) > 3 else ''}")
    
    # 模拟文件比较
    print("\n5. 文件比较:")
    compare_result = FileTools.compare_files('file1.txt', 'file2.txt')
    print(f"   比较结果: {compare_result}")
    
    print("练习3完成！\n")


# 练习4：模块测试和文档
def exercise_4_module_testing():
    """
    练习4：模块测试和文档 - 参考答案
    """
    print("=== 练习4：模块测试和文档 - 参考答案 ===")
    
    # 简单的测试框架（与练习文件相同）
    class SimpleTestFramework:
        def __init__(self):
            self.tests_run = 0
            self.tests_passed = 0
            self.tests_failed = 0
        
        def assert_equal(self, actual, expected, message=""):
            self.tests_run += 1
            if actual == expected:
                self.tests_passed += 1
                print(f"  ✓ 测试通过: {message}")
            else:
                self.tests_failed += 1
                print(f"  ✗ 测试失败: {message}")
                print(f"    期望: {expected}")
                print(f"    实际: {actual}")
        
        def assert_true(self, condition, message=""):
            self.assert_equal(condition, True, message)
        
        def assert_false(self, condition, message=""):
            self.assert_equal(condition, False, message)
        
        def run_test(self, test_func, test_name):
            print(f"\n运行测试: {test_name}")
            try:
                test_func(self)
            except Exception as e:
                self.tests_failed += 1
                print(f"  ✗ 测试异常: {e}")
        
        def summary(self):
            print(f"\n=== 测试摘要 ===")
            print(f"总测试数: {self.tests_run}")
            print(f"通过: {self.tests_passed}")
            print(f"失败: {self.tests_failed}")
            print(f"成功率: {self.tests_passed/self.tests_run*100:.1f}%" if self.tests_run > 0 else "无测试")
    
    # 从前面的练习中导入MathTools类（这里重新定义简化版本）
    class MathTools:
        @staticmethod
        def factorial(n):
            if not isinstance(n, int) or n < 0:
                raise ValueError("输入必须是非负整数")
            if n <= 1:
                return 1
            return n * MathTools.factorial(n - 1)
        
        @staticmethod
        def gcd(a, b):
            a, b = abs(a), abs(b)
            while b:
                a, b = b, a % b
            return a
        
        @staticmethod
        def is_prime(n):
            if n < 2:
                return False
            for i in range(2, int(n ** 0.5) + 1):
                if n % i == 0:
                    return False
            return True
    
    # 测试函数
    def test_math_tools(tester):
        """测试数学工具模块"""
        # 测试阶乘
        tester.assert_equal(MathTools.factorial(0), 1, "0的阶乘应该是1")
        tester.assert_equal(MathTools.factorial(5), 120, "5的阶乘应该是120")
        
        # 测试最大公约数
        tester.assert_equal(MathTools.gcd(12, 18), 6, "12和18的最大公约数应该是6")
        tester.assert_equal(MathTools.gcd(17, 13), 1, "17和13的最大公约数应该是1")
        
        # 测试质数判断
        tester.assert_true(MathTools.is_prime(17), "17应该是质数")
        tester.assert_false(MathTools.is_prime(15), "15不应该是质数")
        tester.assert_false(MathTools.is_prime(1), "1不应该是质数")
    
    def test_string_processor(tester):
        """测试字符串处理模块"""
        # 这里可以添加StringProcessor的测试
        # 由于篇幅限制，这里只做示例
        tester.assert_true(True, "字符串处理模块测试占位符")
    
    def test_file_tools(tester):
        """测试文件工具模块"""
        # 这里可以添加FileTools的测试
        tester.assert_true(True, "文件工具模块测试占位符")
    
    # 运行测试
    tester = SimpleTestFramework()
    
    tester.run_test(test_math_tools, "数学工具模块测试")
    tester.run_test(test_string_processor, "字符串处理模块测试")
    tester.run_test(test_file_tools, "文件工具模块测试")
    
    tester.summary()
    
    print("练习4完成！\n")


# 练习5：模块文档和帮助
def exercise_5_module_documentation():
    """
    练习5：模块文档和帮助 - 参考答案
    """
    print("=== 练习5：模块文档和帮助 - 参考答案 ===")
    
    class DocumentedModule:
        """
        文档化模块示例
        
        这个模块演示了如何编写良好的文档字符串。
        
        Attributes:
            VERSION (str): 模块版本号
            AUTHOR (str): 模块作者
            DESCRIPTION (str): 模块描述
        
        Example:
            >>> dm = DocumentedModule()
            >>> result = dm.example_function("hello")
            >>> print(result)
            Hello, hello!
        """
        
        VERSION = "1.0.0"
        AUTHOR = "Python学习者"
        DESCRIPTION = "演示模块文档的示例模块"
        
        def __init__(self):
            """初始化文档化模块"""
            self.initialized = True
        
        def example_function(self, text):
            """
            示例函数，演示函数文档的写法
            
            Args:
                text (str): 要处理的文本字符串
            
            Returns:
                str: 格式化的问候语
            
            Raises:
                TypeError: 当text不是字符串时抛出
                ValueError: 当text为空字符串时抛出
            """
            if not isinstance(text, str):
                raise TypeError("文本必须是字符串")
            
            if not text.strip():
                raise ValueError("文本不能为空")
            
            return f"Hello, {text}!"
        
        def help_function(self):
            """显示模块帮助信息"""
            help_text = f"""
{self.__class__.__name__} 帮助信息
{'=' * 40}

版本: {self.VERSION}
作者: {self.AUTHOR}
描述: {self.DESCRIPTION}

可用方法:
- example_function(text): 示例函数
- help_function(): 显示帮助信息
- get_module_info(): 获取模块信息

使用示例:
    >>> dm = DocumentedModule()
    >>> dm.example_function("Python")
    >>> dm.help_function()

更多信息请使用 help(DocumentedModule) 查看详细文档。
            """
            return help_text
        
        def get_module_info(self):
            """获取模块信息"""
            return {
                'name': self.__class__.__name__,
                'version': self.VERSION,
                'author': self.AUTHOR,
                'description': self.DESCRIPTION,
                'methods': [method for method in dir(self) if not method.startswith('_')]
            }
    
    # 演示文档功能
    print("文档化模块演示:")
    
    # 创建模块实例
    dm = DocumentedModule()
    
    # 显示模块信息
    info = dm.get_module_info()
    print(f"模块名称: {info['name']}")
    print(f"版本: {info['version']}")
    print(f"作者: {info['author']}")
    print(f"可用方法: {', '.join(info['methods'])}")
    
    # 测试示例函数
    try:
        result = dm.example_function("Python")
        print(f"\n示例函数测试: {result}")
    except Exception as e:
        print(f"示例函数错误: {e}")
    
    # 显示帮助信息
    print("\n" + dm.help_function())
    
    print("练习5完成！\n")


def main():
    """
    主函数 - 运行所有练习的参考答案
    """
    print("Session10 - Exercise2 参考答案")
    print("=" * 60)
    
    # 运行所有练习
    exercise_1_create_math_module()
    exercise_2_create_string_module()
    exercise_3_create_file_module()
    exercise_4_module_testing()
    exercise_5_module_documentation()
    
    print("=" * 60)
    print("所有练习参考答案演示完成！")
    print("\n自定义模块开发总结:")
    print("1. 模块设计要遵循单一职责原则")
    print("2. 函数要有清晰的输入输出和错误处理")
    print("3. 文档字符串是模块可维护性的关键")
    print("4. 测试用例确保模块功能的正确性")
    print("5. 模块应该提供友好的使用接口")
    print("6. 考虑模块的扩展性和复用性")
    
    print("\n最佳实践建议:")
    print("- 使用类型提示提高代码可读性")
    print("- 遵循PEP 8编码规范")
    print("- 为复杂算法添加详细注释")
    print("- 考虑性能优化和内存使用")
    print("- 提供完整的使用示例")


if __name__ == "__main__":
    main()