#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session05 练习2: 字典和集合练习

本练习文件包含字典和集合的操作练习题，帮助掌握高级数据结构的使用。
每个练习都有详细的说明和测试用例。

完成方式：
1. 阅读每个函数的文档字符串
2. 实现函数体
3. 运行测试验证结果
4. 查看solutions目录下的参考答案

作者: Python教程团队
创建日期: 2024-12-21
"""

from typing import Dict, Set, List, Tuple, Any, Optional
from collections import defaultdict, Counter


def exercise1_dict_operations() -> Dict[str, Any]:
    """
    练习1: 字典基本操作
    
    创建一个学生信息字典，包含以下操作：
    1. 创建包含姓名、年龄、专业、成绩列表的字典
    2. 添加一个新的键值对："毕业年份": 2025
    3. 修改年龄为21
    4. 在成绩列表中添加一个新成绩90
    5. 返回最终的字典
    
    返回:
        Dict[str, Any]: 学生信息字典
    
    示例:
        返回的字典应该类似：
        {
            "姓名": "张三",
            "年龄": 21,
            "专业": "计算机科学",
            "成绩": [85, 92, 78, 90],
            "毕业年份": 2025
        }
    """
    # TODO: 在这里实现你的代码
    pass


def exercise2_dict_comprehension(words: List[str]) -> Dict[str, int]:
    """
    练习2: 字典推导式
    
    使用字典推导式创建一个字典，键是单词，值是单词的长度。
    只包含长度大于3的单词。
    
    参数:
        words: 单词列表
    
    返回:
        Dict[str, int]: 单词长度字典
    
    示例:
        >>> exercise2_dict_comprehension(["cat", "dog", "elephant", "bird", "python"])
        {'elephant': 8, 'bird': 4, 'python': 6}
    """
    # TODO: 在这里实现你的代码
    pass


def exercise3_nested_dict(students: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    练习3: 嵌套字典操作
    
    将学生列表转换为嵌套字典，外层键是专业，内层是该专业的学生信息统计。
    
    参数:
        students: 学生信息列表，每个学生包含name, major, score
    
    返回:
        Dict[str, Dict[str, Any]]: 按专业分组的统计信息
        {
            "专业名": {
                "学生数量": int,
                "平均分": float,
                "学生列表": List[str]
            }
        }
    
    示例:
        >>> students = [
        ...     {"name": "张三", "major": "计算机", "score": 85},
        ...     {"name": "李四", "major": "数学", "score": 92},
        ...     {"name": "王五", "major": "计算机", "score": 78}
        ... ]
        >>> result = exercise3_nested_dict(students)
        >>> result["计算机"]["学生数量"]
        2
    """
    # TODO: 在这里实现你的代码
    pass


def exercise4_set_operations(list1: List[int], list2: List[int]) -> Dict[str, Set[int]]:
    """
    练习4: 集合运算
    
    给定两个整数列表，计算并返回它们的：
    1. 并集
    2. 交集
    3. 第一个列表独有的元素
    4. 第二个列表独有的元素
    5. 对称差集
    
    参数:
        list1: 第一个整数列表
        list2: 第二个整数列表
    
    返回:
        Dict[str, Set[int]]: 包含各种集合运算结果的字典
    
    示例:
        >>> exercise4_set_operations([1, 2, 3, 4], [3, 4, 5, 6])
        {
            '并集': {1, 2, 3, 4, 5, 6},
            '交集': {3, 4},
            '第一个独有': {1, 2},
            '第二个独有': {5, 6},
            '对称差集': {1, 2, 5, 6}
        }
    """
    # TODO: 在这里实现你的代码
    pass


def exercise5_word_frequency(text: str) -> Dict[str, int]:
    """
    练习5: 词频统计
    
    统计文本中每个单词的出现频率（忽略大小写和标点符号）。
    
    参数:
        text: 输入文本
    
    返回:
        Dict[str, int]: 单词频率字典
    
    示例:
        >>> exercise5_word_frequency("Hello world! Hello Python. Python is great.")
        {'hello': 2, 'world': 1, 'python': 2, 'is': 1, 'great': 1}
    """
    # TODO: 在这里实现你的代码
    pass


def exercise6_set_comprehension(numbers: List[int]) -> Set[int]:
    """
    练习6: 集合推导式
    
    使用集合推导式创建一个集合，包含所有完全平方数（在给定数字列表的平方中）。
    
    参数:
        numbers: 数字列表
    
    返回:
        Set[int]: 完全平方数集合
    
    示例:
        >>> exercise6_set_comprehension([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        {1, 4, 9, 16, 25, 36, 49, 64, 81, 100}
    """
    # TODO: 在这里实现你的代码
    pass


def exercise7_data_grouping(transactions: List[Tuple[str, str, float]]) -> Dict[str, List[float]]:
    """
    练习7: 数据分组
    
    将交易记录按类别分组，返回每个类别的金额列表。
    
    参数:
        transactions: 交易记录列表，每个记录是(日期, 类别, 金额)
    
    返回:
        Dict[str, List[float]]: 按类别分组的金额列表
    
    示例:
        >>> transactions = [
        ...     ("2024-01-01", "食物", 50.0),
        ...     ("2024-01-02", "交通", 20.0),
        ...     ("2024-01-03", "食物", 30.0)
        ... ]
        >>> exercise7_data_grouping(transactions)
        {'食物': [50.0, 30.0], '交通': [20.0]}
    """
    # TODO: 在这里实现你的代码
    pass


def exercise8_unique_elements(data: List[List[Any]]) -> Set[Any]:
    """
    练习8: 提取唯一元素
    
    从嵌套列表中提取所有唯一元素。
    
    参数:
        data: 嵌套列表
    
    返回:
        Set[Any]: 所有唯一元素的集合
    
    示例:
        >>> exercise8_unique_elements([[1, 2, 3], [2, 3, 4], [3, 4, 5]])
        {1, 2, 3, 4, 5}
    """
    # TODO: 在这里实现你的代码
    pass


def exercise9_dict_merge(dict1: Dict[str, int], dict2: Dict[str, int]) -> Dict[str, int]:
    """
    练习9: 字典合并
    
    合并两个字典，如果有相同的键，则将值相加。
    
    参数:
        dict1: 第一个字典
        dict2: 第二个字典
    
    返回:
        Dict[str, int]: 合并后的字典
    
    示例:
        >>> dict1 = {"a": 1, "b": 2, "c": 3}
        >>> dict2 = {"b": 3, "c": 4, "d": 5}
        >>> exercise9_dict_merge(dict1, dict2)
        {'a': 1, 'b': 5, 'c': 7, 'd': 5}
    """
    # TODO: 在这里实现你的代码
    pass


def exercise10_advanced_filtering(students: List[Dict[str, Any]], 
                                 min_score: float, 
                                 majors: Set[str]) -> List[str]:
    """
    练习10: 高级过滤
    
    从学生列表中筛选出满足以下条件的学生姓名：
    1. 平均分大于等于指定分数
    2. 专业在指定专业集合中
    
    参数:
        students: 学生信息列表，每个学生包含name, major, scores
        min_score: 最低平均分要求
        majors: 允许的专业集合
    
    返回:
        List[str]: 符合条件的学生姓名列表
    
    示例:
        >>> students = [
        ...     {"name": "张三", "major": "计算机", "scores": [85, 90, 88]},
        ...     {"name": "李四", "major": "数学", "scores": [92, 89, 94]},
        ...     {"name": "王五", "major": "物理", "scores": [78, 82, 80]}
        ... ]
        >>> exercise10_advanced_filtering(students, 85, {"计算机", "数学"})
        ['张三', '李四']
    """
    # TODO: 在这里实现你的代码
    pass


def exercise11_counter_usage(text: str) -> Tuple[str, int, List[Tuple[str, int]]]:
    """
    练习11: Counter的使用
    
    使用Counter统计文本中字符的频率，返回：
    1. 出现最多的字符
    2. 该字符的出现次数
    3. 出现频率前3的字符及其次数
    
    参数:
        text: 输入文本
    
    返回:
        Tuple[str, int, List[Tuple[str, int]]]: (最常见字符, 次数, 前3名列表)
    
    示例:
        >>> exercise11_counter_usage("hello world")
        ('l', 3, [('l', 3), ('o', 2), ('h', 1)])
    """
    # TODO: 在这里实现你的代码
    pass


def exercise12_defaultdict_usage(pairs: List[Tuple[str, str]]) -> Dict[str, List[str]]:
    """
    练习12: defaultdict的使用
    
    使用defaultdict将键值对列表转换为一对多的映射。
    
    参数:
        pairs: 键值对列表
    
    返回:
        Dict[str, List[str]]: 一对多映射字典
    
    示例:
        >>> pairs = [("fruit", "apple"), ("fruit", "banana"), ("color", "red"), ("color", "blue")]
        >>> exercise12_defaultdict_usage(pairs)
        {'fruit': ['apple', 'banana'], 'color': ['red', 'blue']}
    """
    # TODO: 在这里实现你的代码
    pass


def run_tests():
    """
    运行所有练习的测试
    """
    print("Session05 练习2: 字典和集合练习")
    print("=" * 50)
    
    # 测试练习1
    print("\n测试练习1: 字典基本操作")
    try:
        result1 = exercise1_dict_operations()
        print(f"结果: {result1}")
        expected_keys = {"姓名", "年龄", "专业", "成绩", "毕业年份"}
        print(f"包含所有必需键: {set(result1.keys()) >= expected_keys}")
        print(f"年龄是21: {result1.get('年龄') == 21}")
        print(f"毕业年份是2025: {result1.get('毕业年份') == 2025}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试练习2
    print("\n测试练习2: 字典推导式")
    try:
        test_words = ["cat", "dog", "elephant", "bird", "python"]
        result2 = exercise2_dict_comprehension(test_words)
        print(f"结果: {result2}")
        expected2 = {'elephant': 8, 'bird': 4, 'python': 6}
        print(f"期望: {expected2}")
        print(f"正确: {result2 == expected2}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试练习3
    print("\n测试练习3: 嵌套字典操作")
    try:
        test_students = [
            {"name": "张三", "major": "计算机", "score": 85},
            {"name": "李四", "major": "数学", "score": 92},
            {"name": "王五", "major": "计算机", "score": 78}
        ]
        result3 = exercise3_nested_dict(test_students)
        print(f"结果: {result3}")
        print(f"计算机专业学生数: {result3.get('计算机', {}).get('学生数量', 0)}")
        print(f"数学专业学生数: {result3.get('数学', {}).get('学生数量', 0)}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试练习4
    print("\n测试练习4: 集合运算")
    try:
        result4 = exercise4_set_operations([1, 2, 3, 4], [3, 4, 5, 6])
        print(f"结果: {result4}")
        expected4 = {
            '并集': {1, 2, 3, 4, 5, 6},
            '交集': {3, 4},
            '第一个独有': {1, 2},
            '第二个独有': {5, 6},
            '对称差集': {1, 2, 5, 6}
        }
        print(f"期望: {expected4}")
        print(f"正确: {result4 == expected4}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试练习5
    print("\n测试练习5: 词频统计")
    try:
        test_text = "Hello world! Hello Python. Python is great."
        result5 = exercise5_word_frequency(test_text)
        print(f"结果: {result5}")
        expected5 = {'hello': 2, 'world': 1, 'python': 2, 'is': 1, 'great': 1}
        print(f"期望: {expected5}")
        print(f"正确: {result5 == expected5}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试练习6
    print("\n测试练习6: 集合推导式")
    try:
        result6 = exercise6_set_comprehension([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        print(f"结果: {result6}")
        expected6 = {1, 4, 9, 16, 25, 36, 49, 64, 81, 100}
        print(f"期望: {expected6}")
        print(f"正确: {result6 == expected6}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试练习7
    print("\n测试练习7: 数据分组")
    try:
        test_transactions = [
            ("2024-01-01", "食物", 50.0),
            ("2024-01-02", "交通", 20.0),
            ("2024-01-03", "食物", 30.0)
        ]
        result7 = exercise7_data_grouping(test_transactions)
        print(f"结果: {result7}")
        expected7 = {'食物': [50.0, 30.0], '交通': [20.0]}
        print(f"期望: {expected7}")
        print(f"正确: {result7 == expected7}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试练习8
    print("\n测试练习8: 提取唯一元素")
    try:
        test_data = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
        result8 = exercise8_unique_elements(test_data)
        print(f"结果: {result8}")
        expected8 = {1, 2, 3, 4, 5}
        print(f"期望: {expected8}")
        print(f"正确: {result8 == expected8}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试练习9
    print("\n测试练习9: 字典合并")
    try:
        dict1 = {"a": 1, "b": 2, "c": 3}
        dict2 = {"b": 3, "c": 4, "d": 5}
        result9 = exercise9_dict_merge(dict1, dict2)
        print(f"结果: {result9}")
        expected9 = {'a': 1, 'b': 5, 'c': 7, 'd': 5}
        print(f"期望: {expected9}")
        print(f"正确: {result9 == expected9}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试练习10
    print("\n测试练习10: 高级过滤")
    try:
        test_students = [
            {"name": "张三", "major": "计算机", "scores": [85, 90, 88]},
            {"name": "李四", "major": "数学", "scores": [92, 89, 94]},
            {"name": "王五", "major": "物理", "scores": [78, 82, 80]}
        ]
        result10 = exercise10_advanced_filtering(test_students, 85, {"计算机", "数学"})
        print(f"结果: {result10}")
        expected10 = ['张三', '李四']
        print(f"期望: {expected10}")
        print(f"正确: {set(result10) == set(expected10)}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试练习11
    print("\n测试练习11: Counter的使用")
    try:
        result11 = exercise11_counter_usage("hello world")
        print(f"结果: {result11}")
        expected11 = ('l', 3, [('l', 3), ('o', 2), ('h', 1)])
        print(f"期望: {expected11}")
        print(f"最常见字符正确: {result11[0] == expected11[0] and result11[1] == expected11[1]}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试练习12
    print("\n测试练习12: defaultdict的使用")
    try:
        test_pairs = [("fruit", "apple"), ("fruit", "banana"), ("color", "red"), ("color", "blue")]
        result12 = exercise12_defaultdict_usage(test_pairs)
        print(f"结果: {dict(result12)}")
        expected12 = {'fruit': ['apple', 'banana'], 'color': ['red', 'blue']}
        print(f"期望: {expected12}")
        print(f"正确: {dict(result12) == expected12}")
    except Exception as e:
        print(f"错误: {e}")
    
    print("\n" + "=" * 50)
    print("练习完成！请查看solutions目录下的参考答案。")
    print("建议：")
    print("1. 重点掌握字典和集合的常用操作")
    print("2. 学习使用collections模块的高级数据结构")
    print("3. 练习推导式的使用，提高代码简洁性")
    print("4. 理解不同数据结构的性能特点")


if __name__ == "__main__":
    run_tests()