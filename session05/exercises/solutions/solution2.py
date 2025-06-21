#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session05 练习2参考答案: 字典和集合练习

本文件提供练习2的参考答案和详细解释。
学习建议：
1. 先独立完成练习
2. 对比参考答案
3. 理解不同实现方式的优缺点
4. 学习collections模块的使用

作者: Python教程团队
创建日期: 2024-12-21
"""

from typing import Dict, Set, List, Tuple, Any, Optional
from collections import defaultdict, Counter
import re


def exercise1_dict_operations() -> Dict[str, Any]:
    """
    练习1: 字典基本操作
    
    参考答案和解释
    """
    # 1. 创建包含姓名、年龄、专业、成绩列表的字典
    student = {
        "姓名": "张三",
        "年龄": 20,
        "专业": "计算机科学",
        "成绩": [85, 92, 78]
    }
    
    # 2. 添加一个新的键值对："毕业年份": 2025
    student["毕业年份"] = 2025
    
    # 3. 修改年龄为21
    student["年龄"] = 21
    
    # 4. 在成绩列表中添加一个新成绩90
    student["成绩"].append(90)
    
    # 5. 返回最终的字典
    return student


def exercise2_dict_comprehension(words: List[str]) -> Dict[str, int]:
    """
    练习2: 字典推导式
    
    参考答案和解释
    """
    # 方法1: 字典推导式（推荐）
    return {word: len(word) for word in words if len(word) > 3}
    
    # 方法2: 传统方式
    # result = {}
    # for word in words:
    #     if len(word) > 3:
    #         result[word] = len(word)
    # return result
    
    # 方法3: 使用filter和dict
    # filtered_words = filter(lambda word: len(word) > 3, words)
    # return dict((word, len(word)) for word in filtered_words)


def exercise3_nested_dict(students: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    练习3: 嵌套字典操作
    
    参考答案和解释
    """
    # 方法1: 使用defaultdict（推荐）
    from collections import defaultdict
    
    result = defaultdict(lambda: {"学生数量": 0, "总分": 0, "学生列表": []})
    
    for student in students:
        major = student["major"]
        result[major]["学生数量"] += 1
        result[major]["总分"] += student["score"]
        result[major]["学生列表"].append(student["name"])
    
    # 计算平均分
    for major_info in result.values():
        major_info["平均分"] = major_info["总分"] / major_info["学生数量"]
        del major_info["总分"]  # 删除临时的总分字段
    
    return dict(result)
    
    # 方法2: 传统字典方式
    # result = {}
    # for student in students:
    #     major = student["major"]
    #     if major not in result:
    #         result[major] = {"学生数量": 0, "总分": 0, "学生列表": []}
    #     
    #     result[major]["学生数量"] += 1
    #     result[major]["总分"] += student["score"]
    #     result[major]["学生列表"].append(student["name"])
    # 
    # # 计算平均分
    # for major_info in result.values():
    #     major_info["平均分"] = major_info["总分"] / major_info["学生数量"]
    #     del major_info["总分"]
    # 
    # return result


def exercise4_set_operations(list1: List[int], list2: List[int]) -> Dict[str, Set[int]]:
    """
    练习4: 集合运算
    
    参考答案和解释
    """
    set1 = set(list1)
    set2 = set(list2)
    
    return {
        '并集': set1 | set2,           # 或 set1.union(set2)
        '交集': set1 & set2,           # 或 set1.intersection(set2)
        '第一个独有': set1 - set2,      # 或 set1.difference(set2)
        '第二个独有': set2 - set1,      # 或 set2.difference(set1)
        '对称差集': set1 ^ set2        # 或 set1.symmetric_difference(set2)
    }


def exercise5_word_frequency(text: str) -> Dict[str, int]:
    """
    练习5: 词频统计
    
    参考答案和解释
    """
    # 方法1: 使用正则表达式和Counter（推荐）
    words = re.findall(r'\b\w+\b', text.lower())
    return dict(Counter(words))
    
    # 方法2: 手动处理标点符号
    # import string
    # # 移除标点符号并转换为小写
    # cleaned_text = text.lower().translate(str.maketrans('', '', string.punctuation))
    # words = cleaned_text.split()
    # 
    # # 统计词频
    # word_count = {}
    # for word in words:
    #     word_count[word] = word_count.get(word, 0) + 1
    # 
    # return word_count
    
    # 方法3: 使用defaultdict
    # word_count = defaultdict(int)
    # words = re.findall(r'\b\w+\b', text.lower())
    # for word in words:
    #     word_count[word] += 1
    # return dict(word_count)


def exercise6_set_comprehension(numbers: List[int]) -> Set[int]:
    """
    练习6: 集合推导式
    
    参考答案和解释
    """
    # 方法1: 集合推导式（推荐）
    return {x**2 for x in numbers}
    
    # 方法2: 使用map和set
    # return set(map(lambda x: x**2, numbers))
    
    # 方法3: 传统循环
    # result = set()
    # for x in numbers:
    #     result.add(x**2)
    # return result


def exercise7_data_grouping(transactions: List[Tuple[str, str, float]]) -> Dict[str, List[float]]:
    """
    练习7: 数据分组
    
    参考答案和解释
    """
    # 方法1: 使用defaultdict（推荐）
    result = defaultdict(list)
    for date, category, amount in transactions:
        result[category].append(amount)
    return dict(result)
    
    # 方法2: 传统字典方式
    # result = {}
    # for date, category, amount in transactions:
    #     if category not in result:
    #         result[category] = []
    #     result[category].append(amount)
    # return result
    
    # 方法3: 使用字典的setdefault方法
    # result = {}
    # for date, category, amount in transactions:
    #     result.setdefault(category, []).append(amount)
    # return result


def exercise8_unique_elements(data: List[List[Any]]) -> Set[Any]:
    """
    练习8: 提取唯一元素
    
    参考答案和解释
    """
    # 方法1: 使用集合推导式（推荐）
    return {element for sublist in data for element in sublist}
    
    # 方法2: 使用itertools.chain
    # from itertools import chain
    # return set(chain.from_iterable(data))
    
    # 方法3: 传统循环
    # result = set()
    # for sublist in data:
    #     for element in sublist:
    #         result.add(element)
    # return result
    
    # 方法4: 使用sum（巧妙但不推荐，可读性差）
    # return set(sum(data, []))


def exercise9_dict_merge(dict1: Dict[str, int], dict2: Dict[str, int]) -> Dict[str, int]:
    """
    练习9: 字典合并
    
    参考答案和解释
    """
    # 方法1: 使用Counter（推荐）
    from collections import Counter
    return dict(Counter(dict1) + Counter(dict2))
    
    # 方法2: 手动合并
    # result = dict1.copy()
    # for key, value in dict2.items():
    #     result[key] = result.get(key, 0) + value
    # return result
    
    # 方法3: 使用defaultdict
    # result = defaultdict(int)
    # for d in [dict1, dict2]:
    #     for key, value in d.items():
    #         result[key] += value
    # return dict(result)
    
    # 方法4: Python 3.9+ 使用字典合并操作符（但这里需要特殊处理重复键）
    # all_keys = set(dict1.keys()) | set(dict2.keys())
    # return {key: dict1.get(key, 0) + dict2.get(key, 0) for key in all_keys}


def exercise10_advanced_filtering(students: List[Dict[str, Any]], 
                                 min_score: float, 
                                 majors: Set[str]) -> List[str]:
    """
    练习10: 高级过滤
    
    参考答案和解释
    """
    # 方法1: 列表推导式（推荐）
    return [student["name"] for student in students 
            if (sum(student["scores"]) / len(student["scores"]) >= min_score 
                and student["major"] in majors)]
    
    # 方法2: 使用filter函数
    # def meets_criteria(student):
    #     avg_score = sum(student["scores"]) / len(student["scores"])
    #     return avg_score >= min_score and student["major"] in majors
    # 
    # return [student["name"] for student in filter(meets_criteria, students)]
    
    # 方法3: 传统循环
    # result = []
    # for student in students:
    #     avg_score = sum(student["scores"]) / len(student["scores"])
    #     if avg_score >= min_score and student["major"] in majors:
    #         result.append(student["name"])
    # return result


def exercise11_counter_usage(text: str) -> Tuple[str, int, List[Tuple[str, int]]]:
    """
    练习11: Counter的使用
    
    参考答案和解释
    """
    # 使用Counter统计字符频率
    char_counter = Counter(text)
    
    # 1. 出现最多的字符和次数
    most_common_char, count = char_counter.most_common(1)[0]
    
    # 2. 出现频率前3的字符及其次数
    top_3 = char_counter.most_common(3)
    
    return most_common_char, count, top_3
    
    # 手动实现（不使用Counter）：
    # char_count = {}
    # for char in text:
    #     char_count[char] = char_count.get(char, 0) + 1
    # 
    # # 找出最常见的字符
    # most_common_char = max(char_count, key=char_count.get)
    # count = char_count[most_common_char]
    # 
    # # 按频率排序，取前3
    # sorted_chars = sorted(char_count.items(), key=lambda x: x[1], reverse=True)
    # top_3 = sorted_chars[:3]
    # 
    # return most_common_char, count, top_3


def exercise12_defaultdict_usage(pairs: List[Tuple[str, str]]) -> Dict[str, List[str]]:
    """
    练习12: defaultdict的使用
    
    参考答案和解释
    """
    # 方法1: 使用defaultdict（推荐）
    result = defaultdict(list)
    for key, value in pairs:
        result[key].append(value)
    return dict(result)
    
    # 方法2: 传统字典方式
    # result = {}
    # for key, value in pairs:
    #     if key not in result:
    #         result[key] = []
    #     result[key].append(value)
    # return result
    
    # 方法3: 使用setdefault
    # result = {}
    # for key, value in pairs:
    #     result.setdefault(key, []).append(value)
    # return result


def demonstrate_solutions():
    """
    演示所有解决方案
    """
    print("Session05 练习2参考答案演示")
    print("=" * 50)
    
    # 演示练习1
    print("\n练习1: 字典基本操作")
    result1 = exercise1_dict_operations()
    print(f"结果: {result1}")
    print("解释: 字典是可变的，可以直接修改值和添加新键值对")
    
    # 演示练习2
    print("\n练习2: 字典推导式")
    test_words = ["cat", "dog", "elephant", "bird", "python"]
    result2 = exercise2_dict_comprehension(test_words)
    print(f"输入: {test_words}")
    print(f"结果: {result2}")
    print("解释: {word: len(word) for word in words if len(word) > 3}")
    
    # 演示练习3
    print("\n练习3: 嵌套字典操作")
    test_students = [
        {"name": "张三", "major": "计算机", "score": 85},
        {"name": "李四", "major": "数学", "score": 92},
        {"name": "王五", "major": "计算机", "score": 78}
    ]
    result3 = exercise3_nested_dict(test_students)
    print(f"输入: {test_students}")
    print(f"结果: {result3}")
    print("解释: defaultdict简化了嵌套字典的初始化")
    
    # 演示练习4
    print("\n练习4: 集合运算")
    result4 = exercise4_set_operations([1, 2, 3, 4], [3, 4, 5, 6])
    print(f"输入: [1, 2, 3, 4], [3, 4, 5, 6]")
    print(f"结果: {result4}")
    print("解释: 集合运算符 |, &, -, ^ 分别表示并集、交集、差集、对称差集")
    
    # 演示练习5
    print("\n练习5: 词频统计")
    test_text = "Hello world! Hello Python. Python is great."
    result5 = exercise5_word_frequency(test_text)
    print(f"输入: {test_text}")
    print(f"结果: {result5}")
    print("解释: 使用正则表达式提取单词，Counter统计频率")
    
    # 演示练习6
    print("\n练习6: 集合推导式")
    test_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result6 = exercise6_set_comprehension(test_numbers)
    print(f"输入: {test_numbers}")
    print(f"结果: {result6}")
    print("解释: {x**2 for x in numbers} 创建平方数集合")
    
    # 演示练习7
    print("\n练习7: 数据分组")
    test_transactions = [
        ("2024-01-01", "食物", 50.0),
        ("2024-01-02", "交通", 20.0),
        ("2024-01-03", "食物", 30.0)
    ]
    result7 = exercise7_data_grouping(test_transactions)
    print(f"输入: {test_transactions}")
    print(f"结果: {result7}")
    print("解释: defaultdict(list)自动创建空列表")
    
    # 演示练习8
    print("\n练习8: 提取唯一元素")
    test_data = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
    result8 = exercise8_unique_elements(test_data)
    print(f"输入: {test_data}")
    print(f"结果: {result8}")
    print("解释: 嵌套推导式 {element for sublist in data for element in sublist}")
    
    # 演示练习9
    print("\n练习9: 字典合并")
    dict1 = {"a": 1, "b": 2, "c": 3}
    dict2 = {"b": 3, "c": 4, "d": 5}
    result9 = exercise9_dict_merge(dict1, dict2)
    print(f"输入: {dict1}, {dict2}")
    print(f"结果: {result9}")
    print("解释: Counter支持加法运算，自动处理重复键")
    
    # 演示练习10
    print("\n练习10: 高级过滤")
    test_students = [
        {"name": "张三", "major": "计算机", "scores": [85, 90, 88]},
        {"name": "李四", "major": "数学", "scores": [92, 89, 94]},
        {"name": "王五", "major": "物理", "scores": [78, 82, 80]}
    ]
    result10 = exercise10_advanced_filtering(test_students, 85, {"计算机", "数学"})
    print(f"输入: {test_students}")
    print(f"结果: {result10}")
    print("解释: 列表推导式结合复杂条件判断")
    
    # 演示练习11
    print("\n练习11: Counter的使用")
    test_text = "hello world"
    result11 = exercise11_counter_usage(test_text)
    print(f"输入: {test_text}")
    print(f"结果: {result11}")
    print("解释: Counter.most_common()返回按频率排序的列表")
    
    # 演示练习12
    print("\n练习12: defaultdict的使用")
    test_pairs = [("fruit", "apple"), ("fruit", "banana"), ("color", "red"), ("color", "blue")]
    result12 = exercise12_defaultdict_usage(test_pairs)
    print(f"输入: {test_pairs}")
    print(f"结果: {result12}")
    print("解释: defaultdict(list)避免了键不存在的检查")
    
    print("\n" + "=" * 50)
    print("学习要点总结:")
    print("1. 字典推导式语法: {key: value for item in iterable if condition}")
    print("2. 集合推导式语法: {expression for item in iterable if condition}")
    print("3. defaultdict避免KeyError，简化代码")
    print("4. Counter专门用于计数，提供便利方法")
    print("5. 集合运算符: | (并), & (交), - (差), ^ (对称差)")
    print("6. 正则表达式处理文本更准确")
    print("7. 嵌套推导式可以处理多层数据结构")
    print("8. 使用in操作符检查集合成员关系效率高")
    
    print("\n性能提示:")
    print("1. 集合的成员测试比列表快得多 (O(1) vs O(n))")
    print("2. 字典的键查找也是O(1)")
    print("3. Counter比手动计数更高效")
    print("4. defaultdict比使用get()或setdefault()更快")
    print("5. 推导式通常比等价的循环更快")


if __name__ == "__main__":
    demonstrate_solutions()