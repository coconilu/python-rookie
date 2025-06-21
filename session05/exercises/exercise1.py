#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session05 练习1: 列表和元组基础练习

本练习文件包含列表和元组的基础操作练习题，帮助巩固基本概念。
每个练习都有详细的说明和测试用例。

完成方式：
1. 阅读每个函数的文档字符串
2. 实现函数体
3. 运行测试验证结果
4. 查看solutions目录下的参考答案

作者: Python教程团队
创建日期: 2024-12-21
"""

from typing import List, Tuple, Any, Optional


def exercise1_list_operations():
    """
    练习1: 列表基本操作
    
    要求：
    1. 创建一个包含1-10的列表
    2. 在列表末尾添加数字11
    3. 在列表开头插入数字0
    4. 删除数字5
    5. 返回修改后的列表
    
    返回:
        List[int]: 修改后的列表
    """
    # TODO: 在这里实现你的代码
    pass


def exercise2_list_slicing(numbers: List[int]) -> Tuple[List[int], List[int], List[int]]:
    """
    练习2: 列表切片操作
    
    给定一个数字列表，返回以下三个切片：
    1. 前三个元素
    2. 最后三个元素
    3. 每隔一个元素取一个（从索引0开始）
    
    参数:
        numbers: 输入的数字列表
    
    返回:
        Tuple[List[int], List[int], List[int]]: (前三个, 后三个, 间隔元素)
    
    示例:
        >>> exercise2_list_slicing([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        ([1, 2, 3], [8, 9, 10], [1, 3, 5, 7, 9])
    """
    # TODO: 在这里实现你的代码
    pass


def exercise3_list_comprehension(start: int, end: int) -> List[int]:
    """
    练习3: 列表推导式
    
    使用列表推导式创建一个列表，包含指定范围内所有偶数的平方。
    
    参数:
        start: 起始数字（包含）
        end: 结束数字（不包含）
    
    返回:
        List[int]: 偶数平方的列表
    
    示例:
        >>> exercise3_list_comprehension(1, 11)
        [4, 16, 36, 64, 100]
    """
    # TODO: 在这里实现你的代码
    pass


def exercise4_tuple_unpacking(student_data: List[Tuple[str, int, str]]) -> Tuple[List[str], float]:
    """
    练习4: 元组解包
    
    给定一个包含学生信息的元组列表，每个元组包含(姓名, 年龄, 专业)。
    返回所有学生的姓名列表和平均年龄。
    
    参数:
        student_data: 学生信息列表，每个元素是(姓名, 年龄, 专业)
    
    返回:
        Tuple[List[str], float]: (姓名列表, 平均年龄)
    
    示例:
        >>> data = [("张三", 20, "计算机"), ("李四", 22, "数学"), ("王五", 19, "物理")]
        >>> exercise4_tuple_unpacking(data)
        (['张三', '李四', '王五'], 20.333333333333332)
    """
    # TODO: 在这里实现你的代码
    pass


def exercise5_nested_lists(matrix: List[List[int]]) -> Tuple[int, List[int], List[int]]:
    """
    练习5: 嵌套列表操作
    
    给定一个二维矩阵（嵌套列表），计算：
    1. 所有元素的总和
    2. 每行的和
    3. 每列的和
    
    参数:
        matrix: 二维矩阵
    
    返回:
        Tuple[int, List[int], List[int]]: (总和, 行和列表, 列和列表)
    
    示例:
        >>> matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        >>> exercise5_nested_lists(matrix)
        (45, [6, 15, 24], [12, 15, 18])
    """
    # TODO: 在这里实现你的代码
    pass


def exercise6_list_methods(words: List[str]) -> Tuple[List[str], List[str], int]:
    """
    练习6: 列表方法应用
    
    给定一个单词列表，执行以下操作：
    1. 按字母顺序排序（不修改原列表）
    2. 按单词长度排序（不修改原列表）
    3. 统计包含字母'a'的单词数量
    
    参数:
        words: 单词列表
    
    返回:
        Tuple[List[str], List[str], int]: (字母排序, 长度排序, 包含'a'的数量)
    
    示例:
        >>> words = ["python", "java", "javascript", "go", "rust"]
        >>> exercise6_list_methods(words)
        (['go', 'java', 'javascript', 'python', 'rust'], ['go', 'java', 'rust', 'python', 'javascript'], 2)
    """
    # TODO: 在这里实现你的代码
    pass


def exercise7_tuple_as_key(transactions: List[Tuple[str, str, float]]) -> dict:
    """
    练习7: 元组作为字典键
    
    给定一个交易记录列表，每个记录包含(日期, 类别, 金额)。
    创建一个字典，以(日期, 类别)作为键，金额总和作为值。
    
    参数:
        transactions: 交易记录列表
    
    返回:
        dict: 以(日期, 类别)为键，金额总和为值的字典
    
    示例:
        >>> transactions = [
        ...     ("2024-01-01", "食物", 50.0),
        ...     ("2024-01-01", "交通", 20.0),
        ...     ("2024-01-01", "食物", 30.0),
        ...     ("2024-01-02", "食物", 40.0)
        ... ]
        >>> exercise7_tuple_as_key(transactions)
        {('2024-01-01', '食物'): 80.0, ('2024-01-01', '交通'): 20.0, ('2024-01-02', '食物'): 40.0}
    """
    # TODO: 在这里实现你的代码
    pass


def exercise8_coordinate_operations(points: List[Tuple[float, float]]) -> Tuple[Tuple[float, float], float]:
    """
    练习8: 坐标点操作
    
    给定一个坐标点列表，找出：
    1. 距离原点最远的点
    2. 所有点到原点的平均距离
    
    参数:
        points: 坐标点列表，每个点是(x, y)
    
    返回:
        Tuple[Tuple[float, float], float]: (最远点, 平均距离)
    
    示例:
        >>> points = [(0, 0), (3, 4), (1, 1), (5, 0)]
        >>> exercise8_coordinate_operations(points)
        ((5, 0), 2.6)
    """
    # TODO: 在这里实现你的代码
    pass


def exercise9_data_filtering(data: List[Tuple[str, int, float]]) -> List[Tuple[str, int, float]]:
    """
    练习9: 数据过滤
    
    给定一个包含(姓名, 年龄, 分数)的数据列表，
    返回年龄在18-25之间且分数大于等于80的记录。
    
    参数:
        data: 数据列表，每个元素是(姓名, 年龄, 分数)
    
    返回:
        List[Tuple[str, int, float]]: 过滤后的数据
    
    示例:
        >>> data = [("张三", 20, 85.5), ("李四", 17, 90.0), ("王五", 23, 75.0), ("赵六", 22, 88.0)]
        >>> exercise9_data_filtering(data)
        [('张三', 20, 85.5), ('赵六', 22, 88.0)]
    """
    # TODO: 在这里实现你的代码
    pass


def exercise10_list_rotation(lst: List[Any], k: int) -> List[Any]:
    """
    练习10: 列表旋转
    
    将列表向右旋转k个位置。
    
    参数:
        lst: 输入列表
        k: 旋转位置数（正数向右，负数向左）
    
    返回:
        List[Any]: 旋转后的列表
    
    示例:
        >>> exercise10_list_rotation([1, 2, 3, 4, 5], 2)
        [4, 5, 1, 2, 3]
        >>> exercise10_list_rotation([1, 2, 3, 4, 5], -1)
        [2, 3, 4, 5, 1]
    """
    # TODO: 在这里实现你的代码
    pass


def run_tests():
    """
    运行所有练习的测试
    """
    print("Session05 练习1: 列表和元组基础练习")
    print("=" * 50)
    
    # 测试练习1
    print("\n测试练习1: 列表基本操作")
    try:
        result1 = exercise1_list_operations()
        print(f"结果: {result1}")
        expected1 = [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11]
        print(f"期望: {expected1}")
        print(f"正确: {result1 == expected1}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试练习2
    print("\n测试练习2: 列表切片操作")
    try:
        test_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result2 = exercise2_list_slicing(test_list)
        print(f"结果: {result2}")
        expected2 = ([1, 2, 3], [8, 9, 10], [1, 3, 5, 7, 9])
        print(f"期望: {expected2}")
        print(f"正确: {result2 == expected2}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试练习3
    print("\n测试练习3: 列表推导式")
    try:
        result3 = exercise3_list_comprehension(1, 11)
        print(f"结果: {result3}")
        expected3 = [4, 16, 36, 64, 100]
        print(f"期望: {expected3}")
        print(f"正确: {result3 == expected3}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试练习4
    print("\n测试练习4: 元组解包")
    try:
        test_data = [("张三", 20, "计算机"), ("李四", 22, "数学"), ("王五", 19, "物理")]
        result4 = exercise4_tuple_unpacking(test_data)
        print(f"结果: {result4}")
        expected4 = (['张三', '李四', '王五'], 20.333333333333332)
        print(f"期望: {expected4}")
        print(f"正确: {result4[0] == expected4[0] and abs(result4[1] - expected4[1]) < 0.001}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试练习5
    print("\n测试练习5: 嵌套列表操作")
    try:
        test_matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        result5 = exercise5_nested_lists(test_matrix)
        print(f"结果: {result5}")
        expected5 = (45, [6, 15, 24], [12, 15, 18])
        print(f"期望: {expected5}")
        print(f"正确: {result5 == expected5}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试练习6
    print("\n测试练习6: 列表方法应用")
    try:
        test_words = ["python", "java", "javascript", "go", "rust"]
        result6 = exercise6_list_methods(test_words)
        print(f"结果: {result6}")
        expected6 = (['go', 'java', 'javascript', 'python', 'rust'], 
                    ['go', 'java', 'rust', 'python', 'javascript'], 2)
        print(f"期望: {expected6}")
        print(f"正确: {result6 == expected6}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试练习7
    print("\n测试练习7: 元组作为字典键")
    try:
        test_transactions = [
            ("2024-01-01", "食物", 50.0),
            ("2024-01-01", "交通", 20.0),
            ("2024-01-01", "食物", 30.0),
            ("2024-01-02", "食物", 40.0)
        ]
        result7 = exercise7_tuple_as_key(test_transactions)
        print(f"结果: {result7}")
        expected7 = {('2024-01-01', '食物'): 80.0, ('2024-01-01', '交通'): 20.0, ('2024-01-02', '食物'): 40.0}
        print(f"期望: {expected7}")
        print(f"正确: {result7 == expected7}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试练习8
    print("\n测试练习8: 坐标点操作")
    try:
        test_points = [(0, 0), (3, 4), (1, 1), (5, 0)]
        result8 = exercise8_coordinate_operations(test_points)
        print(f"结果: {result8}")
        expected8 = ((5, 0), 2.6)
        print(f"期望: {expected8}")
        print(f"正确: {result8[0] == expected8[0] and abs(result8[1] - expected8[1]) < 0.1}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试练习9
    print("\n测试练习9: 数据过滤")
    try:
        test_data = [("张三", 20, 85.5), ("李四", 17, 90.0), ("王五", 23, 75.0), ("赵六", 22, 88.0)]
        result9 = exercise9_data_filtering(test_data)
        print(f"结果: {result9}")
        expected9 = [('张三', 20, 85.5), ('赵六', 22, 88.0)]
        print(f"期望: {expected9}")
        print(f"正确: {result9 == expected9}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试练习10
    print("\n测试练习10: 列表旋转")
    try:
        result10a = exercise10_list_rotation([1, 2, 3, 4, 5], 2)
        result10b = exercise10_list_rotation([1, 2, 3, 4, 5], -1)
        print(f"向右旋转2位: {result10a}")
        print(f"向左旋转1位: {result10b}")
        expected10a = [4, 5, 1, 2, 3]
        expected10b = [2, 3, 4, 5, 1]
        print(f"期望: {expected10a}, {expected10b}")
        print(f"正确: {result10a == expected10a and result10b == expected10b}")
    except Exception as e:
        print(f"错误: {e}")
    
    print("\n" + "=" * 50)
    print("练习完成！请查看solutions目录下的参考答案。")
    print("建议：")
    print("1. 先尝试独立完成所有练习")
    print("2. 遇到困难时查看相关示例代码")
    print("3. 最后对比参考答案，学习更好的实现方式")


if __name__ == "__main__":
    run_tests()