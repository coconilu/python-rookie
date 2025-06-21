#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session05 练习1参考答案: 列表和元组基础练习

本文件提供练习1的参考答案和详细解释。
学习建议：
1. 先独立完成练习
2. 对比参考答案
3. 理解不同实现方式的优缺点
4. 学习更优雅的Python写法

作者: Python教程团队
创建日期: 2024-12-21
"""

from typing import List, Tuple, Any, Optional


def exercise1_list_operations():
    """
    练习1: 列表基本操作
    
    参考答案和解释
    """
    # 1. 创建包含1-10的列表
    numbers = list(range(1, 11))  # 或者 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # 2. 在列表末尾添加数字11
    numbers.append(11)
    
    # 3. 在列表开头插入数字0
    numbers.insert(0, 0)
    
    # 4. 删除数字5
    numbers.remove(5)  # 删除第一个出现的5
    
    # 5. 返回修改后的列表
    return numbers


def exercise2_list_slicing(numbers: List[int]) -> Tuple[List[int], List[int], List[int]]:
    """
    练习2: 列表切片操作
    
    参考答案和解释
    """
    # 1. 前三个元素
    first_three = numbers[:3]
    
    # 2. 最后三个元素
    last_three = numbers[-3:]
    
    # 3. 每隔一个元素取一个（从索引0开始）
    every_other = numbers[::2]
    
    return first_three, last_three, every_other


def exercise3_list_comprehension(start: int, end: int) -> List[int]:
    """
    练习3: 列表推导式
    
    参考答案和解释
    """
    # 方法1: 使用列表推导式（推荐）
    return [x**2 for x in range(start, end) if x % 2 == 0]
    
    # 方法2: 传统循环方式
    # result = []
    # for x in range(start, end):
    #     if x % 2 == 0:
    #         result.append(x**2)
    # return result


def exercise4_tuple_unpacking(student_data: List[Tuple[str, int, str]]) -> Tuple[List[str], float]:
    """
    练习4: 元组解包
    
    参考答案和解释
    """
    # 方法1: 使用列表推导式和元组解包（推荐）
    names = [name for name, age, major in student_data]
    ages = [age for name, age, major in student_data]
    average_age = sum(ages) / len(ages)
    
    return names, average_age
    
    # 方法2: 传统循环方式
    # names = []
    # total_age = 0
    # for student in student_data:
    #     name, age, major = student  # 元组解包
    #     names.append(name)
    #     total_age += age
    # average_age = total_age / len(student_data)
    # return names, average_age
    
    # 方法3: 使用zip解包（高级技巧）
    # names, ages, majors = zip(*student_data)
    # return list(names), sum(ages) / len(ages)


def exercise5_nested_lists(matrix: List[List[int]]) -> Tuple[int, List[int], List[int]]:
    """
    练习5: 嵌套列表操作
    
    参考答案和解释
    """
    # 1. 计算所有元素的总和
    total_sum = sum(sum(row) for row in matrix)
    
    # 2. 计算每行的和
    row_sums = [sum(row) for row in matrix]
    
    # 3. 计算每列的和
    # 方法1: 使用zip转置矩阵
    col_sums = [sum(col) for col in zip(*matrix)]
    
    # 方法2: 传统方式
    # col_sums = []
    # for col_idx in range(len(matrix[0])):
    #     col_sum = sum(matrix[row_idx][col_idx] for row_idx in range(len(matrix)))
    #     col_sums.append(col_sum)
    
    return total_sum, row_sums, col_sums


def exercise6_list_methods(words: List[str]) -> Tuple[List[str], List[str], int]:
    """
    练习6: 列表方法应用
    
    参考答案和解释
    """
    # 1. 按字母顺序排序（不修改原列表）
    alphabetical = sorted(words)
    
    # 2. 按单词长度排序（不修改原列表）
    by_length = sorted(words, key=len)
    
    # 3. 统计包含字母'a'的单词数量
    # 方法1: 使用列表推导式和sum
    count_with_a = sum(1 for word in words if 'a' in word)
    
    # 方法2: 使用filter和len
    # count_with_a = len(list(filter(lambda word: 'a' in word, words)))
    
    # 方法3: 传统循环
    # count_with_a = 0
    # for word in words:
    #     if 'a' in word:
    #         count_with_a += 1
    
    return alphabetical, by_length, count_with_a


def exercise7_tuple_as_key(transactions: List[Tuple[str, str, float]]) -> dict:
    """
    练习7: 元组作为字典键
    
    参考答案和解释
    """
    # 方法1: 使用字典和get方法
    result = {}
    for date, category, amount in transactions:
        key = (date, category)
        result[key] = result.get(key, 0) + amount
    
    return result
    
    # 方法2: 使用defaultdict
    # from collections import defaultdict
    # result = defaultdict(float)
    # for date, category, amount in transactions:
    #     result[(date, category)] += amount
    # return dict(result)
    
    # 方法3: 使用字典推导式和groupby（需要先排序）
    # from itertools import groupby
    # from operator import itemgetter
    # 
    # # 按(日期, 类别)分组
    # sorted_transactions = sorted(transactions, key=lambda x: (x[0], x[1]))
    # grouped = groupby(sorted_transactions, key=lambda x: (x[0], x[1]))
    # return {key: sum(amount for _, _, amount in group) for key, group in grouped}


def exercise8_coordinate_operations(points: List[Tuple[float, float]]) -> Tuple[Tuple[float, float], float]:
    """
    练习8: 坐标点操作
    
    参考答案和解释
    """
    # 计算每个点到原点的距离
    def distance_from_origin(point):
        x, y = point
        return (x**2 + y**2)**0.5
    
    # 1. 找出距离原点最远的点
    farthest_point = max(points, key=distance_from_origin)
    
    # 2. 计算所有点到原点的平均距离
    distances = [distance_from_origin(point) for point in points]
    average_distance = sum(distances) / len(distances)
    
    return farthest_point, round(average_distance, 1)
    
    # 另一种实现方式：
    # distances_with_points = [(distance_from_origin(point), point) for point in points]
    # farthest_distance, farthest_point = max(distances_with_points)
    # average_distance = sum(dist for dist, _ in distances_with_points) / len(distances_with_points)
    # return farthest_point, round(average_distance, 1)


def exercise9_data_filtering(data: List[Tuple[str, int, float]]) -> List[Tuple[str, int, float]]:
    """
    练习9: 数据过滤
    
    参考答案和解释
    """
    # 方法1: 使用列表推导式（推荐）
    return [record for record in data 
            if 18 <= record[1] <= 25 and record[2] >= 80]
    
    # 方法2: 使用filter函数
    # return list(filter(lambda record: 18 <= record[1] <= 25 and record[2] >= 80, data))
    
    # 方法3: 传统循环
    # result = []
    # for name, age, score in data:
    #     if 18 <= age <= 25 and score >= 80:
    #         result.append((name, age, score))
    # return result


def exercise10_list_rotation(lst: List[Any], k: int) -> List[Any]:
    """
    练习10: 列表旋转
    
    参考答案和解释
    """
    if not lst or k == 0:
        return lst.copy()
    
    # 标准化k值（处理k大于列表长度的情况）
    k = k % len(lst)
    
    # 方法1: 使用切片（推荐）
    return lst[-k:] + lst[:-k]
    
    # 方法2: 使用列表方法
    # result = lst.copy()
    # for _ in range(k):
    #     result.insert(0, result.pop())
    # return result
    
    # 方法3: 使用collections.deque（对于大列表更高效）
    # from collections import deque
    # d = deque(lst)
    # d.rotate(k)
    # return list(d)


def demonstrate_solutions():
    """
    演示所有解决方案
    """
    print("Session05 练习1参考答案演示")
    print("=" * 50)
    
    # 演示练习1
    print("\n练习1: 列表基本操作")
    result1 = exercise1_list_operations()
    print(f"结果: {result1}")
    print("解释: 使用list(range(1, 11))创建列表，append()添加元素，insert()插入元素，remove()删除元素")
    
    # 演示练习2
    print("\n练习2: 列表切片操作")
    test_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result2 = exercise2_list_slicing(test_list)
    print(f"输入: {test_list}")
    print(f"结果: {result2}")
    print("解释: [:3]取前三个，[-3:]取后三个，[::2]每隔一个取一个")
    
    # 演示练习3
    print("\n练习3: 列表推导式")
    result3 = exercise3_list_comprehension(1, 11)
    print(f"结果: {result3}")
    print("解释: [x**2 for x in range(start, end) if x % 2 == 0] 简洁高效")
    
    # 演示练习4
    print("\n练习4: 元组解包")
    test_data = [("张三", 20, "计算机"), ("李四", 22, "数学"), ("王五", 19, "物理")]
    result4 = exercise4_tuple_unpacking(test_data)
    print(f"输入: {test_data}")
    print(f"结果: {result4}")
    print("解释: 使用元组解包 name, age, major = student 简化代码")
    
    # 演示练习5
    print("\n练习5: 嵌套列表操作")
    test_matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    result5 = exercise5_nested_lists(test_matrix)
    print(f"输入: {test_matrix}")
    print(f"结果: {result5}")
    print("解释: 使用zip(*matrix)转置矩阵来计算列和")
    
    # 演示练习6
    print("\n练习6: 列表方法应用")
    test_words = ["python", "java", "javascript", "go", "rust"]
    result6 = exercise6_list_methods(test_words)
    print(f"输入: {test_words}")
    print(f"结果: {result6}")
    print("解释: sorted()不修改原列表，key=len按长度排序，生成器表达式计数")
    
    # 演示练习7
    print("\n练习7: 元组作为字典键")
    test_transactions = [
        ("2024-01-01", "食物", 50.0),
        ("2024-01-01", "交通", 20.0),
        ("2024-01-01", "食物", 30.0),
        ("2024-01-02", "食物", 40.0)
    ]
    result7 = exercise7_tuple_as_key(test_transactions)
    print(f"输入: {test_transactions}")
    print(f"结果: {result7}")
    print("解释: 元组是不可变的，可以作为字典的键")
    
    # 演示练习8
    print("\n练习8: 坐标点操作")
    test_points = [(0, 0), (3, 4), (1, 1), (5, 0)]
    result8 = exercise8_coordinate_operations(test_points)
    print(f"输入: {test_points}")
    print(f"结果: {result8}")
    print("解释: 使用max()和key参数找最大值，计算欧几里得距离")
    
    # 演示练习9
    print("\n练习9: 数据过滤")
    test_data = [("张三", 20, 85.5), ("李四", 17, 90.0), ("王五", 23, 75.0), ("赵六", 22, 88.0)]
    result9 = exercise9_data_filtering(test_data)
    print(f"输入: {test_data}")
    print(f"结果: {result9}")
    print("解释: 列表推导式结合条件判断，简洁明了")
    
    # 演示练习10
    print("\n练习10: 列表旋转")
    test_list = [1, 2, 3, 4, 5]
    result10a = exercise10_list_rotation(test_list, 2)
    result10b = exercise10_list_rotation(test_list, -1)
    print(f"输入: {test_list}")
    print(f"向右旋转2位: {result10a}")
    print(f"向左旋转1位: {result10b}")
    print("解释: 使用切片lst[-k:] + lst[:-k]实现旋转")
    
    print("\n" + "=" * 50)
    print("学习要点总结:")
    print("1. 列表推导式比传统循环更简洁高效")
    print("2. 元组解包可以简化代码")
    print("3. 切片操作功能强大，掌握各种用法")
    print("4. sorted()不修改原列表，sort()修改原列表")
    print("5. max()和min()可以使用key参数自定义比较")
    print("6. 元组可以作为字典的键")
    print("7. zip()可以用来转置矩阵")
    print("8. 使用模运算处理边界情况")


if __name__ == "__main__":
    demonstrate_solutions()