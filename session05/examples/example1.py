#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session05 示例1: 列表操作详解

本文件详细演示列表的各种操作方法，包括：
- 列表创建和初始化
- 元素访问和切片
- 列表修改操作
- 列表方法使用
- 列表推导式
- 实际应用场景

作者: Python教程团队
创建日期: 2024-12-21
"""

from typing import List, Any
import random


def demo_list_creation():
    """
    演示列表的创建方法
    """
    print("📝 列表创建方法演示")
    print("=" * 30)
    
    # 1. 直接创建
    fruits = ["apple", "banana", "cherry"]
    numbers = [1, 2, 3, 4, 5]
    mixed = ["Python", 3.8, True, None]
    empty = []
    
    print(f"水果列表: {fruits}")
    print(f"数字列表: {numbers}")
    print(f"混合列表: {mixed}")
    print(f"空列表: {empty}")
    
    # 2. 使用list()函数
    from_string = list("hello")
    from_range = list(range(5))
    from_tuple = list((1, 2, 3))
    
    print(f"\n从字符串创建: {from_string}")
    print(f"从range创建: {from_range}")
    print(f"从元组创建: {from_tuple}")
    
    # 3. 列表乘法（重复）
    zeros = [0] * 5
    pattern = [1, 2] * 3
    
    print(f"\n重复创建 - 零列表: {zeros}")
    print(f"重复创建 - 模式: {pattern}")
    
    # 4. 嵌套列表
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    nested = [[0] * 3 for _ in range(3)]  # 正确的方式
    # 错误方式: [[0] * 3] * 3  # 会创建相同引用
    
    print(f"\n矩阵: {matrix}")
    print(f"嵌套列表: {nested}")


def demo_list_access():
    """
    演示列表的访问和切片操作
    """
    print("\n🔍 列表访问和切片演示")
    print("=" * 30)
    
    data = ["a", "b", "c", "d", "e", "f", "g", "h"]
    print(f"原始列表: {data}")
    
    # 1. 索引访问
    print(f"\n索引访问:")
    print(f"第一个元素 [0]: {data[0]}")
    print(f"最后一个元素 [-1]: {data[-1]}")
    print(f"倒数第二个 [-2]: {data[-2]}")
    
    # 2. 切片操作
    print(f"\n切片操作:")
    print(f"前三个 [:3]: {data[:3]}")
    print(f"后三个 [-3:]: {data[-3:]}")
    print(f"中间部分 [2:5]: {data[2:5]}")
    print(f"每隔一个 [::2]: {data[::2]}")
    print(f"反转 [::-1]: {data[::-1]}")
    print(f"从索引1开始每隔2个 [1::2]: {data[1::2]}")
    
    # 3. 切片赋值
    data_copy = data.copy()
    data_copy[1:4] = ["X", "Y", "Z"]
    print(f"\n切片赋值后: {data_copy}")
    
    # 4. 成员测试
    print(f"\n成员测试:")
    print(f"'c' in data: {'c' in data}")
    print(f"'z' not in data: {'z' not in data}")


def demo_list_modification():
    """
    演示列表的修改操作
    """
    print("\n✏️ 列表修改操作演示")
    print("=" * 30)
    
    # 初始列表
    fruits = ["apple", "banana"]
    print(f"初始列表: {fruits}")
    
    # 1. 添加元素
    print(f"\n添加元素:")
    fruits.append("cherry")  # 末尾添加
    print(f"append('cherry'): {fruits}")
    
    fruits.insert(1, "blueberry")  # 指定位置插入
    print(f"insert(1, 'blueberry'): {fruits}")
    
    fruits.extend(["date", "elderberry"])  # 扩展列表
    print(f"extend(['date', 'elderberry']): {fruits}")
    
    # 2. 删除元素
    print(f"\n删除元素:")
    fruits.remove("banana")  # 删除第一个匹配的元素
    print(f"remove('banana'): {fruits}")
    
    popped = fruits.pop()  # 删除并返回最后一个元素
    print(f"pop(): {fruits}, 返回值: {popped}")
    
    popped_index = fruits.pop(1)  # 删除并返回指定索引的元素
    print(f"pop(1): {fruits}, 返回值: {popped_index}")
    
    del fruits[0]  # 删除指定索引的元素
    print(f"del fruits[0]: {fruits}")
    
    # 3. 修改元素
    print(f"\n修改元素:")
    fruits[0] = "grape"
    print(f"fruits[0] = 'grape': {fruits}")
    
    # 4. 清空列表
    fruits_copy = fruits.copy()
    fruits_copy.clear()
    print(f"clear()后: {fruits_copy}")


def demo_list_methods():
    """
    演示列表的常用方法
    """
    print("\n🛠️ 列表方法演示")
    print("=" * 30)
    
    # 测试数据
    numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5]
    print(f"原始列表: {numbers}")
    
    # 1. 查找方法
    print(f"\n查找方法:")
    print(f"index(5): {numbers.index(5)}")
    print(f"count(1): {numbers.count(1)}")
    print(f"count(5): {numbers.count(5)}")
    
    # 2. 排序方法
    print(f"\n排序方法:")
    numbers_copy = numbers.copy()
    numbers_copy.sort()  # 原地排序
    print(f"sort()后: {numbers_copy}")
    
    numbers_copy.sort(reverse=True)  # 降序排序
    print(f"sort(reverse=True)后: {numbers_copy}")
    
    # 使用sorted()不修改原列表
    sorted_numbers = sorted(numbers)
    print(f"sorted()结果: {sorted_numbers}")
    print(f"原列表未变: {numbers}")
    
    # 3. 反转方法
    print(f"\n反转方法:")
    numbers_copy = numbers.copy()
    numbers_copy.reverse()  # 原地反转
    print(f"reverse()后: {numbers_copy}")
    
    # 使用reversed()不修改原列表
    reversed_numbers = list(reversed(numbers))
    print(f"reversed()结果: {reversed_numbers}")
    
    # 4. 复制方法
    print(f"\n复制方法:")
    copy1 = numbers.copy()  # 浅拷贝
    copy2 = numbers[:]      # 切片拷贝
    copy3 = list(numbers)   # 构造函数拷贝
    
    print(f"copy(): {copy1}")
    print(f"[:]: {copy2}")
    print(f"list(): {copy3}")
    
    # 验证是不同对象
    print(f"copy1 is numbers: {copy1 is numbers}")
    print(f"copy1 == numbers: {copy1 == numbers}")


def demo_list_comprehensions():
    """
    演示列表推导式的各种用法
    """
    print("\n🔄 列表推导式演示")
    print("=" * 30)
    
    # 1. 基本列表推导式
    squares = [x**2 for x in range(1, 6)]
    print(f"平方列表: {squares}")
    
    # 2. 带条件的列表推导式
    even_numbers = [x for x in range(1, 11) if x % 2 == 0]
    print(f"偶数列表: {even_numbers}")
    
    odd_squares = [x**2 for x in range(1, 11) if x % 2 == 1]
    print(f"奇数平方: {odd_squares}")
    
    # 3. 字符串处理
    words = ["hello", "world", "python", "programming"]
    upper_words = [word.upper() for word in words]
    long_words = [word for word in words if len(word) > 5]
    word_lengths = [len(word) for word in words]
    
    print(f"\n字符串处理:")
    print(f"原单词: {words}")
    print(f"大写: {upper_words}")
    print(f"长单词: {long_words}")
    print(f"单词长度: {word_lengths}")
    
    # 4. 嵌套列表推导式
    matrix = [[i*j for j in range(1, 4)] for i in range(1, 4)]
    print(f"\n乘法表矩阵: {matrix}")
    
    # 展平嵌套列表
    nested = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flattened = [item for sublist in nested for item in sublist]
    print(f"嵌套列表: {nested}")
    print(f"展平后: {flattened}")
    
    # 5. 条件表达式
    numbers = [-2, -1, 0, 1, 2]
    abs_numbers = [x if x >= 0 else -x for x in numbers]
    positive_or_zero = [x if x > 0 else 0 for x in numbers]
    
    print(f"\n条件表达式:")
    print(f"原数字: {numbers}")
    print(f"绝对值: {abs_numbers}")
    print(f"正数或零: {positive_or_zero}")
    
    # 6. 复杂表达式
    students = ["Alice", "Bob", "Charlie", "David"]
    scores = [85, 92, 78, 96]
    
    # 创建学生成绩对
    student_scores = [(student, score) for student, score in zip(students, scores)]
    print(f"\n学生成绩对: {student_scores}")
    
    # 筛选高分学生
    high_achievers = [student for student, score in zip(students, scores) if score >= 90]
    print(f"高分学生: {high_achievers}")


def demo_practical_applications():
    """
    演示列表的实际应用场景
    """
    print("\n🎯 实际应用场景演示")
    print("=" * 30)
    
    # 1. 数据过滤和处理
    print("1. 数据过滤和处理:")
    temperatures = [23.5, 25.1, 22.8, 26.3, 24.7, 21.9, 27.2]
    
    # 过滤高温
    high_temps = [temp for temp in temperatures if temp > 25.0]
    print(f"温度数据: {temperatures}")
    print(f"高温(>25°C): {high_temps}")
    
    # 温度转换（摄氏度转华氏度）
    fahrenheit = [temp * 9/5 + 32 for temp in temperatures]
    print(f"华氏温度: {[f'{temp:.1f}' for temp in fahrenheit]}")
    
    # 2. 统计分析
    print(f"\n2. 统计分析:")
    scores = [85, 92, 78, 96, 88, 73, 91, 84, 79, 95]
    
    print(f"成绩列表: {scores}")
    print(f"最高分: {max(scores)}")
    print(f"最低分: {min(scores)}")
    print(f"平均分: {sum(scores) / len(scores):.1f}")
    print(f"及格人数: {len([score for score in scores if score >= 60])}")
    print(f"优秀人数: {len([score for score in scores if score >= 90])}")
    
    # 3. 数据分组
    print(f"\n3. 数据分组:")
    grades = []
    for score in scores:
        if score >= 90:
            grades.append('A')
        elif score >= 80:
            grades.append('B')
        elif score >= 70:
            grades.append('C')
        elif score >= 60:
            grades.append('D')
        else:
            grades.append('F')
    
    print(f"等级分布: {grades}")
    
    # 统计各等级人数
    grade_count = {}
    for grade in grades:
        grade_count[grade] = grade_count.get(grade, 0) + 1
    print(f"等级统计: {grade_count}")
    
    # 4. 列表作为栈和队列
    print(f"\n4. 栈和队列操作:")
    
    # 栈操作（LIFO - 后进先出）
    stack = []
    print("栈操作演示:")
    for item in [1, 2, 3]:
        stack.append(item)
        print(f"  入栈 {item}: {stack}")
    
    while stack:
        item = stack.pop()
        print(f"  出栈 {item}: {stack}")
    
    # 队列操作（FIFO - 先进先出）
    from collections import deque
    queue = deque()
    print("\n队列操作演示:")
    for item in [1, 2, 3]:
        queue.append(item)
        print(f"  入队 {item}: {list(queue)}")
    
    while queue:
        item = queue.popleft()
        print(f"  出队 {item}: {list(queue)}")
    
    # 5. 随机操作
    print(f"\n5. 随机操作:")
    numbers = list(range(1, 11))
    print(f"原列表: {numbers}")
    
    # 随机打乱
    shuffled = numbers.copy()
    random.shuffle(shuffled)
    print(f"打乱后: {shuffled}")
    
    # 随机选择
    random_choice = random.choice(numbers)
    random_sample = random.sample(numbers, 3)
    print(f"随机选择一个: {random_choice}")
    print(f"随机选择三个: {random_sample}")


def performance_tips():
    """
    列表性能优化建议
    """
    print("\n⚡ 性能优化建议")
    print("=" * 30)
    
    import time
    
    # 1. 预分配 vs 动态增长
    print("1. 预分配 vs 动态增长:")
    
    # 动态增长
    start_time = time.time()
    dynamic_list = []
    for i in range(100000):
        dynamic_list.append(i)
    dynamic_time = time.time() - start_time
    
    # 预分配
    start_time = time.time()
    preallocated = [0] * 100000
    for i in range(100000):
        preallocated[i] = i
    preallocated_time = time.time() - start_time
    
    print(f"  动态增长时间: {dynamic_time:.4f}秒")
    print(f"  预分配时间: {preallocated_time:.4f}秒")
    print(f"  预分配快 {dynamic_time/preallocated_time:.1f} 倍")
    
    # 2. 列表推导式 vs 循环
    print(f"\n2. 列表推导式 vs 循环:")
    
    # 使用循环
    start_time = time.time()
    loop_result = []
    for i in range(10000):
        if i % 2 == 0:
            loop_result.append(i**2)
    loop_time = time.time() - start_time
    
    # 使用列表推导式
    start_time = time.time()
    comprehension_result = [i**2 for i in range(10000) if i % 2 == 0]
    comprehension_time = time.time() - start_time
    
    print(f"  循环时间: {loop_time:.4f}秒")
    print(f"  推导式时间: {comprehension_time:.4f}秒")
    print(f"  推导式快 {loop_time/comprehension_time:.1f} 倍")
    
    # 3. 成员测试：列表 vs 集合
    print(f"\n3. 成员测试：列表 vs 集合:")
    
    large_list = list(range(10000))
    large_set = set(range(10000))
    
    # 列表成员测试
    start_time = time.time()
    result = 9999 in large_list
    list_time = time.time() - start_time
    
    # 集合成员测试
    start_time = time.time()
    result = 9999 in large_set
    set_time = time.time() - start_time
    
    print(f"  列表查找时间: {list_time:.6f}秒")
    print(f"  集合查找时间: {set_time:.6f}秒")
    if set_time > 0:
        print(f"  集合快 {list_time/set_time:.0f} 倍")


def main():
    """
    主函数：运行所有演示
    """
    print("Session05 Example1: 列表操作详解")
    print("=" * 50)
    
    demo_list_creation()
    demo_list_access()
    demo_list_modification()
    demo_list_methods()
    demo_list_comprehensions()
    demo_practical_applications()
    performance_tips()
    
    print("\n✅ 列表操作演示完成！")


if __name__ == "__main__":
    main()