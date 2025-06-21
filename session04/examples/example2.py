#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session04 示例2：for循环详解

本示例详细演示了Python中for循环的各种用法，包括：
- 基本for循环
- range()函数的使用
- 遍历不同类型的序列
- enumerate()和zip()函数
- 嵌套for循环
- 列表推导式

作者: Python教程团队
创建日期: 2024-12-21
"""

import string
import random


def basic_for_examples():
    """
    基本for循环示例
    """
    print("=== 基本for循环示例 ===")

    # 示例1：使用range()函数
    print("1. 基本计数循环:")
    for i in range(5):
        print(f"  第{i+1}次循环，i = {i}")

    # 示例2：指定起始和结束
    print("\n2. 指定范围的循环:")
    for i in range(2, 8):
        print(f"  数字: {i}")

    # 示例3：指定步长
    print("\n3. 指定步长的循环:")
    for i in range(0, 20, 3):
        print(f"  步长为3: {i}")

    # 示例4：倒序循环
    print("\n4. 倒序循环:")
    for i in range(10, 0, -2):
        print(f"  倒序: {i}")


def sequence_iteration_examples():
    """
    遍历序列的示例
    """
    print("\n=== 遍历序列示例 ===")

    # 示例1：遍历字符串
    word = "Python"
    print(f"1. 遍历字符串 '{word}':")
    for char in word:
        print(f"  字符: '{char}'")

    # 示例2：遍历列表
    fruits = ["🍎苹果", "🍌香蕉", "🍊橙子", "🍇葡萄", "🥝猕猴桃"]
    print(f"\n2. 遍历水果列表:")
    for fruit in fruits:
        print(f"  我喜欢: {fruit}")

    # 示例3：遍历元组
    coordinates = (10, 20, 30)
    print(f"\n3. 遍历坐标元组:")
    for coord in coordinates:
        print(f"  坐标值: {coord}")

    # 示例4：遍历字典的键
    student_scores = {"小明": 85, "小红": 92, "小李": 78, "小王": 96}
    print(f"\n4. 遍历字典的键:")
    for name in student_scores:
        print(f"  学生: {name}")

    # 示例5：遍历字典的值
    print(f"\n5. 遍历字典的值:")
    for score in student_scores.values():
        print(f"  分数: {score}")

    # 示例6：遍历字典的键值对
    print(f"\n6. 遍历字典的键值对:")
    for name, score in student_scores.items():
        print(f"  {name}: {score}分")


def enumerate_examples():
    """
    enumerate()函数示例
    """
    print("\n=== enumerate()函数示例 ===")

    # 示例1：基本用法
    colors = ["红色", "绿色", "蓝色", "黄色"]
    print("1. 基本enumerate用法:")
    for index, color in enumerate(colors):
        print(f"  索引{index}: {color}")

    # 示例2：指定起始索引
    print("\n2. 指定起始索引:")
    for index, color in enumerate(colors, start=1):
        print(f"  第{index}种颜色: {color}")

    # 示例3：实际应用 - 创建编号列表
    tasks = ["学习Python", "写作业", "看电影", "运动"]
    print("\n3. 今日任务清单:")
    for i, task in enumerate(tasks, 1):
        print(f"  {i}. {task}")

    # 示例4：查找特定元素的位置
    numbers = [10, 25, 30, 45, 30, 60]
    target = 30
    print(f"\n4. 查找数字 {target} 的所有位置:")
    positions = []
    for index, num in enumerate(numbers):
        if num == target:
            positions.append(index)
            print(f"  在索引 {index} 处找到 {target}")
    print(f"  总共找到 {len(positions)} 个位置: {positions}")


def zip_examples():
    """
    zip()函数示例
    """
    print("\n=== zip()函数示例 ===")

    # 示例1：基本用法
    names = ["小明", "小红", "小李"]
    ages = [20, 19, 21]
    cities = ["北京", "上海", "广州"]

    print("1. 基本zip用法:")
    for name, age, city in zip(names, ages, cities):
        print(f"  {name}, {age}岁, 来自{city}")

    # 示例2：创建字典
    print("\n2. 使用zip创建字典:")
    subjects = ["数学", "英语", "物理"]
    scores = [85, 92, 78]
    grade_dict = dict(zip(subjects, scores))
    print(f"  成绩字典: {grade_dict}")

    # 示例3：并行处理多个列表
    print("\n3. 并行处理多个列表:")
    list1 = [1, 2, 3, 4]
    list2 = [10, 20, 30, 40]
    print("  计算对应元素的和:")
    for a, b in zip(list1, list2):
        print(f"    {a} + {b} = {a + b}")

    # 示例4：不等长列表的zip
    print("\n4. 不等长列表的zip:")
    short_list = [1, 2, 3]
    long_list = [10, 20, 30, 40, 50]
    print("  zip会以最短列表为准:")
    for a, b in zip(short_list, long_list):
        print(f"    {a} - {b}")


def nested_loops_examples():
    """
    嵌套循环示例
    """
    print("\n=== 嵌套循环示例 ===")

    # 示例1：打印乘法表
    print("1. 九九乘法表:")
    for i in range(1, 10):
        for j in range(1, i + 1):
            print(f"{j}×{i}={i*j:2d}", end="  ")
        print()  # 换行

    # 示例2：打印图案
    print("\n2. 星号图案:")
    for i in range(1, 6):
        # 打印空格
        for j in range(5 - i):
            print(" ", end="")
        # 打印星号
        for k in range(2 * i - 1):
            print("*", end="")
        print()  # 换行

    # 示例3：矩阵操作
    print("\n3. 创建和打印矩阵:")
    matrix = []
    rows, cols = 3, 4

    # 创建矩阵
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(i * cols + j + 1)
        matrix.append(row)

    # 打印矩阵
    print("  矩阵内容:")
    for row in matrix:
        print("   ", end="")
        for element in row:
            print(f"{element:3d}", end=" ")
        print()

    # 示例4：查找二维列表中的元素
    print("\n4. 在矩阵中查找元素:")
    target = 7
    found = False
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == target:
                print(f"  找到 {target} 在位置 ({i}, {j})")
                found = True
                break
        if found:
            break

    if not found:
        print(f"  未找到 {target}")


def practical_examples():
    """
    实际应用示例
    """
    print("\n=== 实际应用示例 ===")

    # 示例1：统计字符频率
    text = "Hello Python Programming"
    print(f"1. 统计字符频率 - 文本: '{text}'")
    char_count = {}

    for char in text.lower():
        if char.isalpha():  # 只统计字母
            if char in char_count:
                char_count[char] += 1
            else:
                char_count[char] = 1

    print("  字符频率:")
    for char, count in sorted(char_count.items()):
        print(f"    '{char}': {count}次")

    # 示例2：生成密码
    print("\n2. 生成随机密码:")
    password_length = 8
    characters = string.ascii_letters + string.digits + "!@#$%^&*"

    for i in range(3):  # 生成3个密码
        password = ""
        for j in range(password_length):
            password += random.choice(characters)
        print(f"  密码{i+1}: {password}")

    # 示例3：计算平均分
    print("\n3. 计算班级平均分:")
    students_grades = {
        "小明": [85, 92, 78, 96],
        "小红": [90, 88, 85, 92],
        "小李": [78, 85, 90, 87],
        "小王": [95, 89, 92, 94],
    }

    class_total = 0
    student_count = 0

    for name, grades in students_grades.items():
        student_total = 0
        for grade in grades:
            student_total += grade

        student_avg = student_total / len(grades)
        print(f"  {name}: 平均分 {student_avg:.1f}")

        class_total += student_avg
        student_count += 1

    class_avg = class_total / student_count
    print(f"  班级平均分: {class_avg:.1f}")

    # 示例4：数据清洗
    print("\n4. 数据清洗示例:")
    raw_data = ["  apple  ", "BANANA", "  Orange", "grape  ", "", "  ", "kiwi"]
    print(f"  原始数据: {raw_data}")

    cleaned_data = []
    for item in raw_data:
        cleaned_item = item.strip().lower()  # 去除空格并转小写
        if cleaned_item:  # 只保留非空项
            cleaned_data.append(cleaned_item)

    print(f"  清洗后数据: {cleaned_data}")

    # 示例5：简单的进度条
    print("\n5. 模拟进度条:")
    import time

    total_steps = 20
    for i in range(total_steps + 1):
        progress = i / total_steps
        bar_length = 30
        filled_length = int(bar_length * progress)

        bar = "█" * filled_length + "-" * (bar_length - filled_length)
        percent = progress * 100

        print(f"\r  进度: |{bar}| {percent:5.1f}%", end="")
        time.sleep(0.1)  # 模拟处理时间

    print("\n  任务完成！")


def list_comprehension_examples():
    """
    列表推导式示例（for循环的简化形式）
    """
    print("\n=== 列表推导式示例 ===")

    # 示例1：基本列表推导式
    print("1. 基本列表推导式:")

    # 传统方法
    squares_traditional = []
    for i in range(1, 6):
        squares_traditional.append(i**2)
    print(f"  传统方法: {squares_traditional}")

    # 列表推导式
    squares_comprehension = [i**2 for i in range(1, 6)]
    print(f"  列表推导式: {squares_comprehension}")

    # 示例2：带条件的列表推导式
    print("\n2. 带条件的列表推导式:")
    numbers = range(1, 11)

    # 筛选偶数
    even_numbers = [n for n in numbers if n % 2 == 0]
    print(f"  偶数: {even_numbers}")

    # 筛选并转换
    even_squares = [n**2 for n in numbers if n % 2 == 0]
    print(f"  偶数的平方: {even_squares}")

    # 示例3：字符串处理
    print("\n3. 字符串处理:")
    words = ["hello", "world", "python", "programming"]

    # 转换为大写
    upper_words = [word.upper() for word in words]
    print(f"  大写: {upper_words}")

    # 筛选长单词
    long_words = [word for word in words if len(word) > 5]
    print(f"  长单词: {long_words}")

    # 获取单词长度
    word_lengths = [len(word) for word in words]
    print(f"  单词长度: {word_lengths}")


def main():
    """
    主函数：运行所有示例
    """
    print("Session04 示例2：for循环详解")
    print("=" * 50)

    basic_for_examples()
    sequence_iteration_examples()
    enumerate_examples()
    zip_examples()
    nested_loops_examples()
    practical_examples()
    list_comprehension_examples()

    print("\n" + "=" * 50)
    print("示例演示完成！")
    print("\n💡 学习要点:")
    print("1. for循环用于遍历序列或可迭代对象")
    print("2. range()函数生成数字序列")
    print("3. enumerate()获取索引和值")
    print("4. zip()并行遍历多个序列")
    print("5. 嵌套循环处理多维数据")
    print("6. 列表推导式是for循环的简化形式")


if __name__ == "__main__":
    main()
