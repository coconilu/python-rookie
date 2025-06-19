#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session02 练习题3：字符串处理挑战 - 参考答案

本文件提供了练习题3的完整解决方案，展示了字符串的各种处理方法。

作者: Python教程团队
创建日期: 2024-12-19
"""

import re
from collections import Counter


def solution():
    """
    练习题3的完整解决方案
    """
    print("=== Session02 练习题3：字符串处理挑战 ===")
    
    # 1. 获取用户输入
    text = input("\n请输入一段文本: ")
    
    # 2. 文本预处理
    original_text = text
    processed_text = text.strip()  # 去除首尾空格
    
    print(f"\n=== 文本分析报告 ===")
    print(f"原始文本: {original_text}")
    print(f"处理后文本: {processed_text}")
    
    # 3. 统计分析
    print("\n=== 统计信息 ===")
    
    # 字符总数（包括空格）
    total_chars = len(processed_text)
    print(f"字符总数: {total_chars}")
    
    # 单词数量
    word_count = count_words(processed_text)
    print(f"单词数量: {word_count}")
    
    # 统计不同类型的字符
    digit_count, alpha_count, other_count = count_character_types(processed_text)
    print(f"数字字符: {digit_count}")
    print(f"字母字符: {alpha_count}")
    print(f"其他字符: {other_count}")
    
    # 4. 文本转换
    print("\n=== 文本转换 ===")
    print(f"全部大写: {processed_text.upper()}")
    print(f"全部小写: {processed_text.lower()}")
    print(f"首字母大写: {processed_text.title()}")
    
    # 5. 查找和替换
    print("\n=== 查找和替换 ===")
    
    # 查找 "python"（不区分大小写）
    python_count = processed_text.lower().count('python')
    print(f"Python 出现次数: {python_count}")
    
    # 替换所有的 "python" 为 "Python"
    # 使用正则表达式进行不区分大小写的替换
    replaced_text = re.sub(r'python', 'Python', processed_text, flags=re.IGNORECASE)
    print(f"替换后文本: {replaced_text}")
    
    # 6. 生成完整报告
    generate_detailed_report(processed_text, replaced_text)


def count_character_types(text):
    """
    统计文本中不同类型字符的数量
    
    Args:
        text (str): 要分析的文本
        
    Returns:
        tuple: (数字字符数, 字母字符数, 其他字符数)
    """
    digit_count = 0
    alpha_count = 0
    other_count = 0
    
    for char in text:
        if char.isdigit():
            digit_count += 1
        elif char.isalpha():
            alpha_count += 1
        else:
            other_count += 1
    
    return digit_count, alpha_count, other_count


def count_words(text):
    """
    统计文本中的单词数量
    
    Args:
        text (str): 要分析的文本
        
    Returns:
        int: 单词数量
    """
    # 使用正则表达式分割单词，只保留字母和数字
    words = re.findall(r'\b\w+\b', text)
    return len(words)


def generate_detailed_report(original_text, replaced_text):
    """
    生成详细的文本分析报告
    
    Args:
        original_text (str): 原始文本
        replaced_text (str): 替换后的文本
    """
    print("\n" + "=" * 60)
    print("                    详细分析报告")
    print("=" * 60)
    
    # 基本统计
    print(f"\n📊 基本统计:")
    print(f"   总字符数: {len(original_text)}")
    print(f"   总单词数: {count_words(original_text)}")
    print(f"   总行数: {len(original_text.splitlines())}")
    
    # 字符类型分析
    digit_count, alpha_count, other_count = count_character_types(original_text)
    print(f"\n🔤 字符类型分析:")
    print(f"   字母字符: {alpha_count} ({alpha_count/len(original_text)*100:.1f}%)")
    print(f"   数字字符: {digit_count} ({digit_count/len(original_text)*100:.1f}%)")
    print(f"   其他字符: {other_count} ({other_count/len(original_text)*100:.1f}%)")
    
    # 空格和标点统计
    space_count = original_text.count(' ')
    punctuation_count = sum(1 for char in original_text if char in '.,!?;:"\'-()[]{}/')
    
    print(f"\n📝 特殊字符统计:")
    print(f"   空格数量: {space_count}")
    print(f"   标点符号: {punctuation_count}")
    
    # 单词长度分析
    words = re.findall(r'\b\w+\b', original_text.lower())
    if words:
        word_lengths = [len(word) for word in words]
        avg_word_length = sum(word_lengths) / len(word_lengths)
        max_word_length = max(word_lengths)
        min_word_length = min(word_lengths)
        
        print(f"\n📏 单词长度分析:")
        print(f"   平均单词长度: {avg_word_length:.1f} 字符")
        print(f"   最长单词长度: {max_word_length} 字符")
        print(f"   最短单词长度: {min_word_length} 字符")
        
        # 找出最长和最短的单词
        longest_words = [word for word in words if len(word) == max_word_length]
        shortest_words = [word for word in words if len(word) == min_word_length]
        
        print(f"   最长单词: {', '.join(set(longest_words))}")
        print(f"   最短单词: {', '.join(set(shortest_words))}")
    
    # 词频分析
    if words:
        word_freq = Counter(words)
        most_common = word_freq.most_common(5)
        
        print(f"\n🔥 词频分析 (前5名):")
        for i, (word, count) in enumerate(most_common, 1):
            print(f"   {i}. '{word}': {count} 次")
    
    # 大小写分析
    upper_count = sum(1 for char in original_text if char.isupper())
    lower_count = sum(1 for char in original_text if char.islower())
    
    print(f"\n🔠 大小写分析:")
    print(f"   大写字母: {upper_count}")
    print(f"   小写字母: {lower_count}")
    
    # Python相关统计
    python_variations = ['python', 'Python', 'PYTHON', 'PyThOn']
    total_python_count = sum(original_text.count(variation) for variation in python_variations)
    
    print(f"\n🐍 Python 相关统计:")
    print(f"   'Python' 总出现次数: {total_python_count}")
    for variation in python_variations:
        count = original_text.count(variation)
        if count > 0:
            print(f"   '{variation}': {count} 次")
    
    print("\n" + "=" * 60)


def advanced_solution():
    """
    进阶版本：更多字符串处理技巧
    """
    print("\n" + "=" * 50)
    print("=== 进阶版本：高级字符串处理 ===")
    
    # 预设一些测试文本
    test_texts = [
        "Python is great! I love Python programming. Python version 3.11 is awesome.",
        "Hello World! This is a TEST string with Numbers 123 and Symbols @#$%.",
        "   Mixed   CASE   text   with   EXTRA   spaces   ",
        "Email: test@example.com, Phone: +1-234-567-8900, Website: https://python.org"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n--- 测试文本 {i} ---")
        print(f"原文: {text}")
        
        # 高级文本清理
        cleaned = advanced_text_cleaning(text)
        print(f"清理后: {cleaned}")
        
        # 提取特定信息
        info = extract_information(text)
        if info:
            print(f"提取信息: {info}")
        
        # 文本转换
        transformed = transform_text(text)
        print(f"转换后: {transformed}")


def advanced_text_cleaning(text):
    """
    高级文本清理
    
    Args:
        text (str): 原始文本
        
    Returns:
        str: 清理后的文本
    """
    # 去除多余空格
    cleaned = re.sub(r'\s+', ' ', text.strip())
    
    # 标准化标点符号
    cleaned = re.sub(r'\s*([,.!?;:])\s*', r'\1 ', cleaned)
    
    # 去除末尾多余空格
    cleaned = cleaned.strip()
    
    return cleaned


def extract_information(text):
    """
    从文本中提取特定信息
    
    Args:
        text (str): 要分析的文本
        
    Returns:
        dict: 提取的信息
    """
    info = {}
    
    # 提取邮箱
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    if emails:
        info['emails'] = emails
    
    # 提取电话号码
    phones = re.findall(r'\+?\d[\d\s\-\(\)]{7,}\d', text)
    if phones:
        info['phones'] = phones
    
    # 提取URL
    urls = re.findall(r'https?://[^\s]+', text)
    if urls:
        info['urls'] = urls
    
    # 提取数字
    numbers = re.findall(r'\b\d+(?:\.\d+)?\b', text)
    if numbers:
        info['numbers'] = numbers
    
    return info


def transform_text(text):
    """
    文本转换
    
    Args:
        text (str): 原始文本
        
    Returns:
        str: 转换后的文本
    """
    # 将每个单词的首字母大写，其余小写
    words = text.split()
    transformed_words = []
    
    for word in words:
        # 保留标点符号
        if word.isalpha():
            transformed_words.append(word.capitalize())
        else:
            # 处理包含标点的单词
            result = ""
            current_word = ""
            
            for char in word:
                if char.isalpha():
                    current_word += char
                else:
                    if current_word:
                        result += current_word.capitalize()
                        current_word = ""
                    result += char
            
            if current_word:
                result += current_word.capitalize()
            
            transformed_words.append(result)
    
    return ' '.join(transformed_words)


def interactive_demo():
    """
    交互式演示
    """
    print("\n" + "=" * 50)
    print("=== 交互式字符串处理演示 ===")
    
    while True:
        print("\n选择操作:")
        print("1. 文本分析")
        print("2. 文本清理")
        print("3. 信息提取")
        print("4. 文本转换")
        print("5. 退出")
        
        choice = input("\n请选择 (1-5): ").strip()
        
        if choice == '5':
            print("再见！")
            break
        
        if choice not in ['1', '2', '3', '4']:
            print("无效选择，请重新输入")
            continue
        
        text = input("\n请输入文本: ")
        
        if choice == '1':
            # 文本分析
            print("\n=== 分析结果 ===")
            digit_count, alpha_count, other_count = count_character_types(text)
            word_count = count_words(text)
            
            print(f"字符总数: {len(text)}")
            print(f"单词数量: {word_count}")
            print(f"数字字符: {digit_count}")
            print(f"字母字符: {alpha_count}")
            print(f"其他字符: {other_count}")
            
        elif choice == '2':
            # 文本清理
            cleaned = advanced_text_cleaning(text)
            print(f"\n清理前: {text}")
            print(f"清理后: {cleaned}")
            
        elif choice == '3':
            # 信息提取
            info = extract_information(text)
            print("\n=== 提取的信息 ===")
            if info:
                for key, value in info.items():
                    print(f"{key}: {value}")
            else:
                print("未找到特定信息")
                
        elif choice == '4':
            # 文本转换
            transformed = transform_text(text)
            print(f"\n转换前: {text}")
            print(f"转换后: {transformed}")


if __name__ == "__main__":
    # 运行基础解决方案
    solution()
    
    # 运行进阶解决方案
    advanced_solution()
    
    # 可选：运行交互式演示
    # interactive_demo()
    
    print("\n" + "=" * 50)
    print("练习完成！你已经掌握了字符串处理的高级技巧。")