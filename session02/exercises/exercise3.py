#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session02 练习题3：字符串处理挑战

题目描述：
编写一个程序来处理和分析用户输入的文本。请完成以下任务：

1. 提示用户输入一段文本

2. 对文本进行以下处理：
   - 去除首尾空格
   - 统计字符总数（包括空格）
   - 统计单词数量
   - 统计数字字符的个数
   - 统计字母字符的个数

3. 文本转换：
   - 显示全部大写版本
   - 显示全部小写版本
   - 显示首字母大写版本

4. 查找和替换：
   - 查找文本中是否包含 "python"（不区分大小写）
   - 如果包含，统计出现次数
   - 将所有的 "python" 替换为 "Python"（保持正确的大小写）

5. 生成报告

输入示例：
请输入一段文本: python is great! I love python programming. Python version 3.11 is awesome.

输出示例：
=== 文本分析报告 ===
原始文本: python is great! I love python programming. Python version 3.11 is awesome.
处理后文本: python is great! I love python programming. Python version 3.11 is awesome.

=== 统计信息 ===
字符总数: 78
单词数量: 12
数字字符: 3
字母字符: 65

=== 文本转换 ===
全部大写: PYTHON IS GREAT! I LOVE PYTHON PROGRAMMING. PYTHON VERSION 3.11 IS AWESOME.
全部小写: python is great! i love python programming. python version 3.11 is awesome.
首字母大写: Python Is Great! I Love Python Programming. Python Version 3.11 Is Awesome.

=== 查找和替换 ===
Python 出现次数: 3
替换后文本: Python is great! I love Python programming. Python version 3.11 is awesome.

提示：
- 使用字符串的 strip(), split(), count() 等方法
- 使用 isdigit() 和 isalpha() 检查字符类型
- 使用 lower() 进行不区分大小写的查找
- 注意处理标点符号对单词计数的影响
"""

# 在这里编写你的代码

def solution():
    """
    在这里实现你的解决方案
    """
    print("=== Session02 练习题3：字符串处理挑战 ===")
    
    # TODO: 1. 获取用户输入
    # 在这里获取用户输入的文本
    
    # TODO: 2. 文本预处理
    # 在这里处理文本（去除首尾空格等）
    
    # TODO: 3. 统计分析
    print("\n=== 统计信息 ===")
    # 在这里进行各种统计
    
    # TODO: 4. 文本转换
    print("\n=== 文本转换 ===")
    # 在这里进行大小写转换
    
    # TODO: 5. 查找和替换
    print("\n=== 查找和替换 ===")
    # 在这里查找和替换 "python"
    
    # TODO: 6. 生成完整报告
    print("\n=== 文本分析报告 ===")
    # 在这里显示完整的分析报告


def count_character_types(text):
    """
    统计文本中不同类型字符的数量
    
    Args:
        text (str): 要分析的文本
        
    Returns:
        tuple: (数字字符数, 字母字符数, 其他字符数)
    """
    # TODO: 实现字符类型统计
    digit_count = 0
    alpha_count = 0
    other_count = 0
    
    # 在这里实现统计逻辑
    
    return digit_count, alpha_count, other_count


def count_words(text):
    """
    统计文本中的单词数量
    
    Args:
        text (str): 要分析的文本
        
    Returns:
        int: 单词数量
    """
    # TODO: 实现单词计数
    # 提示：可以使用 split() 方法，但要注意处理标点符号
    pass


if __name__ == "__main__":
    solution()