#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session 06: 函数编程 - 项目：文本处理工具集

这是一个综合性的文本处理工具集，展示了函数编程的各种概念和技巧。
包括文本分析、格式化、转换、验证等功能。

功能模块:
1. 文本分析 - 统计字符、单词、句子等
2. 文本格式化 - 大小写转换、对齐、缩进等
3. 文本转换 - 编码转换、格式转换等
4. 文本验证 - 邮箱、电话、身份证等验证
5. 文本处理 - 清理、过滤、替换等

作者: Python教程团队
创建日期: 2024-12-22
"""

import re
import string
import unicodedata
from typing import List, Dict, Tuple, Optional, Callable
from functools import wraps
import time


# ==================== 装饰器定义 ====================

def timing_decorator(func):
    """
    计时装饰器 - 测量函数执行时间
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"[计时] {func.__name__} 执行时间: {end_time - start_time:.4f}秒")
        return result
    return wrapper


def validate_input(input_type=str, not_empty=True):
    """
    输入验证装饰器工厂
    
    参数:
        input_type: 期望的输入类型
        not_empty: 是否允许空值
    """
    def decorator(func):
        @wraps(func)
        def wrapper(text, *args, **kwargs):
            if not isinstance(text, input_type):
                raise TypeError(f"输入必须是 {input_type.__name__} 类型")
            
            if not_empty and not text:
                raise ValueError("输入不能为空")
            
            return func(text, *args, **kwargs)
        return wrapper
    return decorator


def cache_result(func):
    """
    结果缓存装饰器
    """
    cache = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 创建缓存键
        key = str(args) + str(sorted(kwargs.items()))
        
        if key in cache:
            print(f"[缓存] {func.__name__} 使用缓存结果")
            return cache[key]
        
        result = func(*args, **kwargs)
        cache[key] = result
        return result
    
    return wrapper


# ==================== 文本分析模块 ====================

class TextAnalyzer:
    """
    文本分析器类
    """
    
    @staticmethod
    @validate_input(str, True)
    def count_characters(text: str, include_spaces: bool = True) -> Dict[str, int]:
        """
        统计字符数量
        
        参数:
            text: 输入文本
            include_spaces: 是否包含空格
        
        返回:
            dict: 字符统计信息
        """
        if not include_spaces:
            text = text.replace(' ', '')
        
        return {
            'total_chars': len(text),
            'letters': sum(1 for c in text if c.isalpha()),
            'digits': sum(1 for c in text if c.isdigit()),
            'spaces': text.count(' ') if include_spaces else 0,
            'punctuation': sum(1 for c in text if c in string.punctuation),
            'chinese_chars': sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        }
    
    @staticmethod
    @validate_input(str, True)
    def count_words(text: str, language: str = 'mixed') -> Dict[str, int]:
        """
        统计单词数量
        
        参数:
            text: 输入文本
            language: 语言类型 ('english', 'chinese', 'mixed')
        
        返回:
            dict: 单词统计信息
        """
        if language == 'english':
            # 英文单词统计
            words = re.findall(r'\b[a-zA-Z]+\b', text)
        elif language == 'chinese':
            # 中文字符统计
            words = re.findall(r'[\u4e00-\u9fff]+', text)
        else:
            # 混合语言统计
            english_words = re.findall(r'\b[a-zA-Z]+\b', text)
            chinese_words = re.findall(r'[\u4e00-\u9fff]+', text)
            words = english_words + chinese_words
        
        return {
            'total_words': len(words),
            'unique_words': len(set(words)),
            'average_length': sum(len(word) for word in words) / len(words) if words else 0,
            'longest_word': max(words, key=len) if words else '',
            'shortest_word': min(words, key=len) if words else ''
        }
    
    @staticmethod
    @validate_input(str, True)
    def count_sentences(text: str) -> Dict[str, int]:
        """
        统计句子数量
        
        参数:
            text: 输入文本
        
        返回:
            dict: 句子统计信息
        """
        # 中英文句号、问号、感叹号
        sentence_endings = r'[.!?。！？]+'
        sentences = re.split(sentence_endings, text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return {
            'total_sentences': len(sentences),
            'average_length': sum(len(s) for s in sentences) / len(sentences) if sentences else 0,
            'longest_sentence': max(sentences, key=len) if sentences else '',
            'shortest_sentence': min(sentences, key=len) if sentences else ''
        }
    
    @staticmethod
    @validate_input(str, True)
    def analyze_readability(text: str) -> Dict[str, float]:
        """
        分析文本可读性
        
        参数:
            text: 输入文本
        
        返回:
            dict: 可读性分析结果
        """
        words = re.findall(r'\b\w+\b', text)
        sentences = re.split(r'[.!?。！？]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not words or not sentences:
            return {'readability_score': 0, 'difficulty_level': '无法分析'}
        
        # 简化的可读性评分
        avg_words_per_sentence = len(words) / len(sentences)
        avg_chars_per_word = sum(len(word) for word in words) / len(words)
        
        # 可读性评分 (简化版)
        readability_score = 100 - (avg_words_per_sentence * 1.5) - (avg_chars_per_word * 2)
        readability_score = max(0, min(100, readability_score))
        
        # 难度等级
        if readability_score >= 80:
            difficulty = '很容易'
        elif readability_score >= 60:
            difficulty = '容易'
        elif readability_score >= 40:
            difficulty = '中等'
        elif readability_score >= 20:
            difficulty = '困难'
        else:
            difficulty = '很困难'
        
        return {
            'readability_score': round(readability_score, 2),
            'difficulty_level': difficulty,
            'avg_words_per_sentence': round(avg_words_per_sentence, 2),
            'avg_chars_per_word': round(avg_chars_per_word, 2)
        }


# ==================== 文本格式化模块 ====================

class TextFormatter:
    """
    文本格式化器类
    """
    
    @staticmethod
    @validate_input(str, False)
    def to_title_case(text: str, style: str = 'standard') -> str:
        """
        转换为标题格式
        
        参数:
            text: 输入文本
            style: 样式 ('standard', 'smart', 'all')
        
        返回:
            str: 格式化后的文本
        """
        if style == 'standard':
            return text.title()
        elif style == 'smart':
            # 智能标题格式，不转换介词、连词等
            small_words = {'a', 'an', 'and', 'as', 'at', 'but', 'by', 'for', 
                          'if', 'in', 'of', 'on', 'or', 'the', 'to', 'up'}
            words = text.lower().split()
            result = []
            
            for i, word in enumerate(words):
                if i == 0 or i == len(words) - 1 or word not in small_words:
                    result.append(word.capitalize())
                else:
                    result.append(word)
            
            return ' '.join(result)
        elif style == 'all':
            return text.upper()
        else:
            return text
    
    @staticmethod
    @validate_input(str, False)
    def align_text(text: str, width: int, alignment: str = 'left', 
                   fill_char: str = ' ') -> str:
        """
        文本对齐
        
        参数:
            text: 输入文本
            width: 对齐宽度
            alignment: 对齐方式 ('left', 'right', 'center')
            fill_char: 填充字符
        
        返回:
            str: 对齐后的文本
        """
        if alignment == 'left':
            return text.ljust(width, fill_char)
        elif alignment == 'right':
            return text.rjust(width, fill_char)
        elif alignment == 'center':
            return text.center(width, fill_char)
        else:
            return text
    
    @staticmethod
    @validate_input(str, False)
    def add_indentation(text: str, indent_size: int = 4, 
                       indent_char: str = ' ', first_line_only: bool = False) -> str:
        """
        添加缩进
        
        参数:
            text: 输入文本
            indent_size: 缩进大小
            indent_char: 缩进字符
            first_line_only: 是否只缩进首行
        
        返回:
            str: 缩进后的文本
        """
        indent = indent_char * indent_size
        lines = text.split('\n')
        
        if first_line_only:
            if lines:
                lines[0] = indent + lines[0]
        else:
            lines = [indent + line for line in lines]
        
        return '\n'.join(lines)
    
    @staticmethod
    @validate_input(str, False)
    def wrap_text(text: str, width: int = 80, break_long_words: bool = True) -> str:
        """
        文本换行
        
        参数:
            text: 输入文本
            width: 行宽
            break_long_words: 是否拆分长单词
        
        返回:
            str: 换行后的文本
        """
        import textwrap
        return textwrap.fill(text, width=width, break_long_words=break_long_words)
    
    @staticmethod
    @validate_input(str, False)
    def create_table(data: List[List[str]], headers: Optional[List[str]] = None,
                    alignment: str = 'left') -> str:
        """
        创建表格
        
        参数:
            data: 表格数据
            headers: 表头
            alignment: 对齐方式
        
        返回:
            str: 表格字符串
        """
        if not data:
            return ""
        
        # 计算每列的最大宽度
        all_rows = [headers] + data if headers else data
        col_widths = [max(len(str(row[i])) for row in all_rows if i < len(row)) 
                     for i in range(max(len(row) for row in all_rows))]
        
        # 创建分隔线
        separator = '+' + '+'.join('-' * (width + 2) for width in col_widths) + '+'
        
        result = [separator]
        
        # 添加表头
        if headers:
            header_row = '|' + '|'.join(f' {str(headers[i]).ljust(col_widths[i])} ' 
                                       for i in range(len(headers))) + '|'
            result.append(header_row)
            result.append(separator)
        
        # 添加数据行
        for row in data:
            data_row = '|' + '|'.join(f' {str(row[i] if i < len(row) else "").ljust(col_widths[i])} ' 
                                     for i in range(len(col_widths))) + '|'
            result.append(data_row)
        
        result.append(separator)
        return '\n'.join(result)


# ==================== 文本转换模块 ====================

class TextConverter:
    """
    文本转换器类
    """
    
    @staticmethod
    @validate_input(str, False)
    def to_pinyin(text: str, tone: bool = False) -> str:
        """
        中文转拼音（简化版）
        
        参数:
            text: 中文文本
            tone: 是否包含声调
        
        返回:
            str: 拼音文本
        """
        # 简化的拼音映射（实际应用中应使用专门的拼音库）
        pinyin_map = {
            '你': 'ni', '好': 'hao', '世': 'shi', '界': 'jie',
            '中': 'zhong', '国': 'guo', '人': 'ren', '民': 'min',
            '大': 'da', '学': 'xue', '生': 'sheng', '活': 'huo'
        }
        
        result = []
        for char in text:
            if char in pinyin_map:
                result.append(pinyin_map[char])
            elif char.isalpha():
                result.append(char)
            elif char.isspace():
                result.append(' ')
        
        return ' '.join(result)
    
    @staticmethod
    @validate_input(str, False)
    def to_morse_code(text: str) -> str:
        """
        转换为摩尔斯电码
        
        参数:
            text: 输入文本
        
        返回:
            str: 摩尔斯电码
        """
        morse_map = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
            'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
            'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
            'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
            '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
            '8': '---..', '9': '----.', ' ': '/'
        }
        
        result = []
        for char in text.upper():
            if char in morse_map:
                result.append(morse_map[char])
        
        return ' '.join(result)
    
    @staticmethod
    @validate_input(str, False)
    def to_binary(text: str, encoding: str = 'utf-8') -> str:
        """
        转换为二进制
        
        参数:
            text: 输入文本
            encoding: 编码格式
        
        返回:
            str: 二进制字符串
        """
        try:
            binary_data = text.encode(encoding)
            return ' '.join(format(byte, '08b') for byte in binary_data)
        except UnicodeEncodeError:
            return "编码错误"
    
    @staticmethod
    @validate_input(str, False)
    def from_binary(binary_text: str, encoding: str = 'utf-8') -> str:
        """
        从二进制转换
        
        参数:
            binary_text: 二进制字符串
            encoding: 编码格式
        
        返回:
            str: 原始文本
        """
        try:
            binary_values = binary_text.split()
            bytes_data = bytes(int(b, 2) for b in binary_values)
            return bytes_data.decode(encoding)
        except (ValueError, UnicodeDecodeError):
            return "解码错误"
    
    @staticmethod
    @validate_input(str, False)
    def normalize_unicode(text: str, form: str = 'NFC') -> str:
        """
        Unicode标准化
        
        参数:
            text: 输入文本
            form: 标准化形式 ('NFC', 'NFD', 'NFKC', 'NFKD')
        
        返回:
            str: 标准化后的文本
        """
        return unicodedata.normalize(form, text)


# ==================== 文本验证模块 ====================

class TextValidator:
    """
    文本验证器类
    """
    
    @staticmethod
    @validate_input(str, True)
    def is_valid_email(email: str) -> bool:
        """
        验证邮箱地址
        
        参数:
            email: 邮箱地址
        
        返回:
            bool: 是否有效
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    @validate_input(str, True)
    def is_valid_phone(phone: str, country: str = 'china') -> bool:
        """
        验证电话号码
        
        参数:
            phone: 电话号码
            country: 国家 ('china', 'us')
        
        返回:
            bool: 是否有效
        """
        if country == 'china':
            # 中国手机号码
            pattern = r'^1[3-9]\d{9}$'
        elif country == 'us':
            # 美国电话号码
            pattern = r'^\+?1?[2-9]\d{2}[2-9]\d{2}\d{4}$'
        else:
            return False
        
        return bool(re.match(pattern, phone.replace('-', '').replace(' ', '')))
    
    @staticmethod
    @validate_input(str, True)
    def is_valid_id_card(id_card: str) -> bool:
        """
        验证身份证号码（中国）
        
        参数:
            id_card: 身份证号码
        
        返回:
            bool: 是否有效
        """
        if len(id_card) != 18:
            return False
        
        # 检查前17位是否为数字
        if not id_card[:17].isdigit():
            return False
        
        # 检查最后一位
        if not (id_card[17].isdigit() or id_card[17].upper() == 'X'):
            return False
        
        # 简化的校验码验证
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
        
        sum_value = sum(int(id_card[i]) * weights[i] for i in range(17))
        check_code = check_codes[sum_value % 11]
        
        return id_card[17].upper() == check_code
    
    @staticmethod
    @validate_input(str, True)
    def is_strong_password(password: str) -> Tuple[bool, List[str]]:
        """
        验证密码强度
        
        参数:
            password: 密码
        
        返回:
            tuple: (是否强密码, 不符合要求的列表)
        """
        issues = []
        
        if len(password) < 8:
            issues.append("密码长度至少8位")
        
        if not re.search(r'[a-z]', password):
            issues.append("需要包含小写字母")
        
        if not re.search(r'[A-Z]', password):
            issues.append("需要包含大写字母")
        
        if not re.search(r'\d', password):
            issues.append("需要包含数字")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            issues.append("需要包含特殊字符")
        
        return len(issues) == 0, issues
    
    @staticmethod
    @validate_input(str, True)
    def is_valid_url(url: str) -> bool:
        """
        验证URL
        
        参数:
            url: URL地址
        
        返回:
            bool: 是否有效
        """
        pattern = r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$'
        return bool(re.match(pattern, url))


# ==================== 文本处理模块 ====================

class TextProcessor:
    """
    文本处理器类
    """
    
    @staticmethod
    @validate_input(str, False)
    def clean_text(text: str, remove_extra_spaces: bool = True,
                  remove_special_chars: bool = False,
                  normalize_case: str = 'none') -> str:
        """
        清理文本
        
        参数:
            text: 输入文本
            remove_extra_spaces: 是否移除多余空格
            remove_special_chars: 是否移除特殊字符
            normalize_case: 大小写标准化 ('none', 'lower', 'upper')
        
        返回:
            str: 清理后的文本
        """
        result = text
        
        if remove_extra_spaces:
            result = re.sub(r'\s+', ' ', result.strip())
        
        if remove_special_chars:
            result = re.sub(r'[^\w\s\u4e00-\u9fff]', '', result)
        
        if normalize_case == 'lower':
            result = result.lower()
        elif normalize_case == 'upper':
            result = result.upper()
        
        return result
    
    @staticmethod
    @validate_input(str, False)
    def extract_patterns(text: str, pattern_type: str) -> List[str]:
        """
        提取文本模式
        
        参数:
            text: 输入文本
            pattern_type: 模式类型 ('email', 'phone', 'url', 'number')
        
        返回:
            list: 匹配的模式列表
        """
        patterns = {
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'phone': r'1[3-9]\d{9}',
            'url': r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?',
            'number': r'\d+(?:\.\d+)?'
        }
        
        if pattern_type not in patterns:
            return []
        
        return re.findall(patterns[pattern_type], text)
    
    @staticmethod
    @validate_input(str, False)
    def replace_patterns(text: str, replacements: Dict[str, str],
                        use_regex: bool = False) -> str:
        """
        替换文本模式
        
        参数:
            text: 输入文本
            replacements: 替换映射
            use_regex: 是否使用正则表达式
        
        返回:
            str: 替换后的文本
        """
        result = text
        
        for pattern, replacement in replacements.items():
            if use_regex:
                result = re.sub(pattern, replacement, result)
            else:
                result = result.replace(pattern, replacement)
        
        return result
    
    @staticmethod
    @validate_input(str, False)
    def filter_words(text: str, filter_list: List[str],
                    action: str = 'remove') -> str:
        """
        过滤单词
        
        参数:
            text: 输入文本
            filter_list: 过滤词列表
            action: 操作类型 ('remove', 'replace', 'highlight')
        
        返回:
            str: 过滤后的文本
        """
        result = text
        
        for word in filter_list:
            if action == 'remove':
                result = re.sub(r'\b' + re.escape(word) + r'\b', '', result, flags=re.IGNORECASE)
            elif action == 'replace':
                result = re.sub(r'\b' + re.escape(word) + r'\b', '*' * len(word), result, flags=re.IGNORECASE)
            elif action == 'highlight':
                result = re.sub(r'\b' + re.escape(word) + r'\b', f'**{word}**', result, flags=re.IGNORECASE)
        
        # 清理多余空格
        result = re.sub(r'\s+', ' ', result.strip())
        return result


# ==================== 高阶函数和工具函数 ====================

def apply_text_operations(text: str, *operations: Callable) -> str:
    """
    应用多个文本操作
    
    参数:
        text: 输入文本
        *operations: 操作函数列表
    
    返回:
        str: 处理后的文本
    """
    result = text
    for operation in operations:
        result = operation(result)
    return result


def create_text_pipeline(*functions: Callable) -> Callable:
    """
    创建文本处理管道
    
    参数:
        *functions: 处理函数列表
    
    返回:
        function: 管道函数
    """
    def pipeline(text: str) -> str:
        result = text
        for func in functions:
            result = func(result)
        return result
    return pipeline


def batch_process_texts(texts: List[str], processor: Callable) -> List[str]:
    """
    批量处理文本
    
    参数:
        texts: 文本列表
        processor: 处理函数
    
    返回:
        list: 处理后的文本列表
    """
    return [processor(text) for text in texts]


# ==================== 主程序和演示 ====================

def main():
    """
    主程序：演示文本处理工具集的功能
    """
    print("文本处理工具集演示")
    print("=" * 50)
    
    # 示例文本
    sample_text = """
    Hello World! 这是一个测试文本。
    包含中文和English混合内容。
    我的邮箱是 test@example.com，电话是 13812345678。
    访问我的网站：https://www.example.com
    这个文本用于演示各种文本处理功能！
    """
    
    print(f"原始文本:\n{sample_text}")
    print("\n" + "=" * 50)
    
    # 1. 文本分析演示
    print("\n1. 文本分析演示")
    print("-" * 30)
    
    analyzer = TextAnalyzer()
    
    # 字符统计
    char_stats = analyzer.count_characters(sample_text)
    print(f"字符统计: {char_stats}")
    
    # 单词统计
    word_stats = analyzer.count_words(sample_text)
    print(f"单词统计: {word_stats}")
    
    # 句子统计
    sentence_stats = analyzer.count_sentences(sample_text)
    print(f"句子统计: {sentence_stats}")
    
    # 可读性分析
    readability = analyzer.analyze_readability(sample_text)
    print(f"可读性分析: {readability}")
    
    # 2. 文本格式化演示
    print("\n2. 文本格式化演示")
    print("-" * 30)
    
    formatter = TextFormatter()
    
    # 标题格式
    title_text = "hello world python programming"
    print(f"标题格式: {formatter.to_title_case(title_text, 'smart')}")
    
    # 文本对齐
    align_text = "Python"
    print(f"居中对齐: '{formatter.align_text(align_text, 20, 'center', '-')}'")
    
    # 添加缩进
    indent_text = "第一行\n第二行\n第三行"
    print(f"缩进文本:\n{formatter.add_indentation(indent_text, 4)}")
    
    # 创建表格
    table_data = [['Alice', '25', '工程师'], ['Bob', '30', '设计师'], ['Charlie', '28', '产品经理']]
    table_headers = ['姓名', '年龄', '职业']
    print(f"表格:\n{formatter.create_table(table_data, table_headers)}")
    
    # 3. 文本转换演示
    print("\n3. 文本转换演示")
    print("-" * 30)
    
    converter = TextConverter()
    
    # 摩尔斯电码
    morse_text = "HELLO"
    morse_code = converter.to_morse_code(morse_text)
    print(f"摩尔斯电码: {morse_text} -> {morse_code}")
    
    # 二进制转换
    binary_text = "Hi"
    binary_code = converter.to_binary(binary_text)
    print(f"二进制: {binary_text} -> {binary_code}")
    decoded_text = converter.from_binary(binary_code)
    print(f"解码: {binary_code} -> {decoded_text}")
    
    # 4. 文本验证演示
    print("\n4. 文本验证演示")
    print("-" * 30)
    
    validator = TextValidator()
    
    # 邮箱验证
    emails = ["test@example.com", "invalid-email", "user@domain.co.uk"]
    for email in emails:
        is_valid = validator.is_valid_email(email)
        print(f"邮箱 {email}: {'有效' if is_valid else '无效'}")
    
    # 电话验证
    phones = ["13812345678", "12345678901", "15987654321"]
    for phone in phones:
        is_valid = validator.is_valid_phone(phone)
        print(f"电话 {phone}: {'有效' if is_valid else '无效'}")
    
    # 密码强度验证
    passwords = ["123456", "Password123", "StrongPass123!"]
    for password in passwords:
        is_strong, issues = validator.is_strong_password(password)
        print(f"密码 {password}: {'强' if is_strong else '弱'} {issues if issues else ''}")
    
    # 5. 文本处理演示
    print("\n5. 文本处理演示")
    print("-" * 30)
    
    processor = TextProcessor()
    
    # 清理文本
    dirty_text = "  Hello    World!!!   这是   测试  "
    clean_text = processor.clean_text(dirty_text, remove_extra_spaces=True)
    print(f"清理前: '{dirty_text}'")
    print(f"清理后: '{clean_text}'")
    
    # 提取模式
    pattern_text = "联系我：邮箱 user@test.com，电话 13812345678，网站 https://example.com"
    emails = processor.extract_patterns(pattern_text, 'email')
    phones = processor.extract_patterns(pattern_text, 'phone')
    urls = processor.extract_patterns(pattern_text, 'url')
    print(f"提取邮箱: {emails}")
    print(f"提取电话: {phones}")
    print(f"提取URL: {urls}")
    
    # 替换模式
    replace_text = "今天天气很好，明天天气也不错"
    replacements = {"天气": "weather", "今天": "today", "明天": "tomorrow"}
    replaced_text = processor.replace_patterns(replace_text, replacements)
    print(f"替换前: {replace_text}")
    print(f"替换后: {replaced_text}")
    
    # 6. 高阶函数演示
    print("\n6. 高阶函数演示")
    print("-" * 30)
    
    # 创建处理管道
    pipeline = create_text_pipeline(
        lambda text: text.strip(),
        lambda text: text.lower(),
        lambda text: re.sub(r'\s+', ' ', text)
    )
    
    messy_text = "  HELLO   WORLD   PYTHON  "
    processed_text = pipeline(messy_text)
    print(f"管道处理前: '{messy_text}'")
    print(f"管道处理后: '{processed_text}'")
    
    # 批量处理
    text_list = ["  Hello  ", "  WORLD  ", "  Python  "]
    processed_list = batch_process_texts(text_list, lambda x: x.strip().title())
    print(f"批量处理前: {text_list}")
    print(f"批量处理后: {processed_list}")
    
    print("\n" + "=" * 50)
    print("文本处理工具集演示完成！")


if __name__ == "__main__":
    main()