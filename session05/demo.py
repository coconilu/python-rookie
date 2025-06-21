#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session05: 数据结构基础 - 演示代码

本文件演示了Python四种主要数据结构的基本用法和实际应用：
- 列表（List）：有序、可变、允许重复
- 元组（Tuple）：有序、不可变、允许重复
- 字典（Dict）：键值对映射、可变、键唯一
- 集合（Set）：无序、可变、元素唯一

作者: Python教程团队
创建日期: 2024-12-21
最后修改: 2024-12-21
"""

import sys
import os
from typing import List, Dict, Set, Tuple, Any


def main():
    """
    主函数：演示程序的入口点
    """
    print("Session05: 数据结构基础演示")
    print("=" * 50)
    
    # 演示各种数据结构
    demo_list_operations()
    print("\n" + "-" * 50)
    
    demo_tuple_operations()
    print("\n" + "-" * 50)
    
    demo_dict_operations()
    print("\n" + "-" * 50)
    
    demo_set_operations()
    print("\n" + "-" * 50)
    
    demo_data_structure_comparison()
    print("\n" + "-" * 50)
    
    demo_practical_examples()
    
    print("\n演示完成！")


def demo_list_operations():
    """
    演示列表的基本操作
    """
    print("📋 列表（List）操作演示")
    
    # 创建列表
    fruits = ["apple", "banana", "cherry"]
    numbers = [1, 2, 3, 4, 5]
    mixed = ["Python", 3.8, True, [1, 2, 3]]
    
    print(f"水果列表: {fruits}")
    print(f"数字列表: {numbers}")
    print(f"混合列表: {mixed}")
    
    # 访问元素
    print(f"\n访问元素:")
    print(f"第一个水果: {fruits[0]}")
    print(f"最后一个数字: {numbers[-1]}")
    print(f"前三个数字: {numbers[:3]}")
    
    # 修改列表
    print(f"\n修改列表:")
    fruits.append("date")  # 添加元素
    print(f"添加date后: {fruits}")
    
    fruits.insert(1, "blueberry")  # 插入元素
    print(f"在位置1插入blueberry: {fruits}")
    
    fruits.remove("banana")  # 删除元素
    print(f"删除banana后: {fruits}")
    
    # 列表方法
    print(f"\n列表方法:")
    numbers_copy = numbers.copy()
    numbers_copy.sort(reverse=True)
    print(f"原数字列表: {numbers}")
    print(f"降序排序后: {numbers_copy}")
    
    # 列表推导式
    squares = [x**2 for x in range(1, 6)]
    even_squares = [x**2 for x in range(1, 11) if x % 2 == 0]
    print(f"\n列表推导式:")
    print(f"1-5的平方: {squares}")
    print(f"1-10中偶数的平方: {even_squares}")


def demo_tuple_operations():
    """
    演示元组的基本操作
    """
    print("📦 元组（Tuple）操作演示")
    
    # 创建元组
    coordinates = (10, 20)
    colors = ("red", "green", "blue")
    single_item = (42,)  # 单元素元组需要逗号
    
    print(f"坐标点: {coordinates}")
    print(f"颜色元组: {colors}")
    print(f"单元素元组: {single_item}")
    
    # 访问元素
    print(f"\n访问元素:")
    print(f"X坐标: {coordinates[0]}")
    print(f"Y坐标: {coordinates[1]}")
    print(f"第二种颜色: {colors[1]}")
    
    # 元组解包
    print(f"\n元组解包:")
    x, y = coordinates
    print(f"解包坐标 - x: {x}, y: {y}")
    
    # 多变量赋值
    name, age, city = "张三", 25, "北京"
    print(f"多变量赋值 - 姓名: {name}, 年龄: {age}, 城市: {city}")
    
    # 变量交换
    a, b = 10, 20
    print(f"交换前: a={a}, b={b}")
    a, b = b, a
    print(f"交换后: a={a}, b={b}")
    
    # 函数返回多个值
    def get_student_info():
        return "李四", 22, "计算机科学"
    
    student_name, student_age, major = get_student_info()
    print(f"\n函数返回多值: {student_name}, {student_age}岁, {major}专业")
    
    # 元组方法
    numbers = (1, 2, 3, 2, 4, 2)
    print(f"\n元组方法:")
    print(f"数字元组: {numbers}")
    print(f"数字2出现次数: {numbers.count(2)}")
    print(f"数字3的索引: {numbers.index(3)}")


def demo_dict_operations():
    """
    演示字典的基本操作
    """
    print("📚 字典（Dict）操作演示")
    
    # 创建字典
    student = {
        "name": "张三",
        "age": 20,
        "major": "计算机科学",
        "scores": [85, 92, 78]
    }
    
    print(f"学生信息: {student}")
    
    # 访问值
    print(f"\n访问字典值:")
    print(f"学生姓名: {student['name']}")
    print(f"学生年龄: {student.get('age')}")
    print(f"学生年级: {student.get('grade', '未知')}")
    
    # 修改和添加
    print(f"\n修改字典:")
    student["age"] = 21  # 修改现有键
    student["grade"] = "大二"  # 添加新键
    print(f"修改后: {student}")
    
    # 字典方法
    print(f"\n字典方法:")
    print(f"所有键: {list(student.keys())}")
    print(f"所有值: {list(student.values())}")
    print(f"所有键值对: {list(student.items())}")
    
    # 遍历字典
    print(f"\n遍历字典:")
    for key, value in student.items():
        print(f"  {key}: {value}")
    
    # 嵌套字典
    students_db = {
        "S001": {
            "name": "张三",
            "scores": {"数学": 85, "英语": 92}
        },
        "S002": {
            "name": "李四",
            "scores": {"数学": 90, "英语": 88}
        }
    }
    
    print(f"\n嵌套字典:")
    print(f"学生S001的数学成绩: {students_db['S001']['scores']['数学']}")
    
    # 字典推导式
    squares_dict = {x: x**2 for x in range(1, 6)}
    print(f"\n字典推导式 - 平方字典: {squares_dict}")
    
    # 过滤字典
    high_scores = {subject: score for subject, score in students_db["S001"]["scores"].items() if score >= 90}
    print(f"张三的高分科目: {high_scores}")


def demo_set_operations():
    """
    演示集合的基本操作
    """
    print("🔢 集合（Set）操作演示")
    
    # 创建集合
    fruits = {"apple", "banana", "cherry"}
    numbers = {1, 2, 3, 4, 5}
    
    # 从列表创建集合（自动去重）
    list_with_duplicates = [1, 2, 2, 3, 3, 3, 4]
    unique_numbers = set(list_with_duplicates)
    
    print(f"水果集合: {fruits}")
    print(f"数字集合: {numbers}")
    print(f"去重后的数字: {unique_numbers}")
    
    # 集合操作
    print(f"\n集合操作:")
    fruits.add("date")
    print(f"添加date后: {fruits}")
    
    fruits.discard("banana")  # 安全删除（不存在不报错）
    print(f"删除banana后: {fruits}")
    
    # 集合运算
    set1 = {1, 2, 3, 4, 5}
    set2 = {4, 5, 6, 7, 8}
    
    print(f"\n集合运算:")
    print(f"集合1: {set1}")
    print(f"集合2: {set2}")
    print(f"并集 (|): {set1 | set2}")
    print(f"交集 (&): {set1 & set2}")
    print(f"差集 (-): {set1 - set2}")
    print(f"对称差集 (^): {set1 ^ set2}")
    
    # 子集和超集
    set3 = {1, 2, 3}
    print(f"\n子集和超集:")
    print(f"集合3: {set3}")
    print(f"{set3} 是 {set1} 的子集: {set3.issubset(set1)}")
    print(f"{set1} 是 {set3} 的超集: {set1.issuperset(set3)}")
    
    # 集合推导式
    even_squares = {x**2 for x in range(10) if x % 2 == 0}
    print(f"\n集合推导式 - 偶数平方: {even_squares}")


def demo_data_structure_comparison():
    """
    演示数据结构的对比和选择
    """
    print("⚖️ 数据结构对比演示")
    
    # 相同数据的不同表示
    data_list = ["apple", "banana", "cherry", "apple"]  # 允许重复
    data_tuple = ("apple", "banana", "cherry", "apple")  # 不可变
    data_set = {"apple", "banana", "cherry"}  # 自动去重
    data_dict = {"fruit1": "apple", "fruit2": "banana", "fruit3": "cherry"}  # 键值对
    
    print(f"列表（允许重复）: {data_list}")
    print(f"元组（不可变）: {data_tuple}")
    print(f"集合（自动去重）: {data_set}")
    print(f"字典（键值对）: {data_dict}")
    
    # 性能对比示例
    print(f"\n性能对比:")
    
    # 成员测试性能
    large_list = list(range(10000))
    large_set = set(range(10000))
    
    import time
    
    # 列表查找（O(n)）
    start_time = time.time()
    result = 9999 in large_list
    list_time = time.time() - start_time
    
    # 集合查找（O(1)）
    start_time = time.time()
    result = 9999 in large_set
    set_time = time.time() - start_time
    
    print(f"列表查找时间: {list_time:.6f}秒")
    print(f"集合查找时间: {set_time:.6f}秒")
    print(f"集合比列表快: {list_time/set_time:.1f}倍")


def demo_practical_examples():
    """
    演示实际应用场景
    """
    print("🎯 实际应用场景演示")
    
    # 1. 数据去重
    print("\n1. 数据去重:")
    duplicate_data = ["张三", "李四", "张三", "王五", "李四", "赵六"]
    unique_data = list(set(duplicate_data))
    print(f"原始数据: {duplicate_data}")
    print(f"去重后: {unique_data}")
    
    # 2. 统计词频
    print("\n2. 统计词频:")
    text = "python is great python is powerful python is easy"
    words = text.split()
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    print(f"文本: {text}")
    print(f"词频统计: {word_count}")
    
    # 3. 学生成绩管理
    print("\n3. 学生成绩管理:")
    students = {
        "张三": {"数学": 85, "英语": 92, "物理": 78},
        "李四": {"数学": 90, "英语": 88, "物理": 85},
        "王五": {"数学": 75, "英语": 80, "物理": 82}
    }
    
    # 计算平均分
    for name, scores in students.items():
        avg_score = sum(scores.values()) / len(scores)
        print(f"{name}的平均分: {avg_score:.1f}")
    
    # 找出数学成绩最高的学生
    best_math_student = max(students.items(), key=lambda x: x[1]["数学"])
    print(f"数学成绩最高: {best_math_student[0]} ({best_math_student[1]['数学']}分)")
    
    # 4. 权限管理
    print("\n4. 权限管理:")
    user_permissions = {"read", "write"}
    required_permissions = {"read", "write", "execute"}
    admin_permissions = {"read", "write", "execute", "delete"}
    
    print(f"用户权限: {user_permissions}")
    print(f"所需权限: {required_permissions}")
    print(f"管理员权限: {admin_permissions}")
    
    has_required = required_permissions.issubset(user_permissions)
    missing_permissions = required_permissions - user_permissions
    extra_admin_permissions = admin_permissions - required_permissions
    
    print(f"用户是否有足够权限: {has_required}")
    print(f"缺少的权限: {missing_permissions}")
    print(f"管理员额外权限: {extra_admin_permissions}")
    
    # 5. 数据分组
    print("\n5. 数据分组:")
    students_list = [
        ("张三", "计算机", 85),
        ("李四", "数学", 92),
        ("王五", "计算机", 78),
        ("赵六", "物理", 88),
        ("钱七", "数学", 90)
    ]
    
    # 按专业分组
    major_groups = {}
    for name, major, score in students_list:
        if major not in major_groups:
            major_groups[major] = []
        major_groups[major].append((name, score))
    
    print("按专业分组:")
    for major, students in major_groups.items():
        print(f"  {major}: {students}")


def demonstrate_comprehensions():
    """
    演示各种推导式的使用
    """
    print("\n🔄 推导式演示")
    
    # 列表推导式
    numbers = range(1, 11)
    squares = [x**2 for x in numbers]
    even_squares = [x**2 for x in numbers if x % 2 == 0]
    
    print(f"数字: {list(numbers)}")
    print(f"平方: {squares}")
    print(f"偶数平方: {even_squares}")
    
    # 字典推导式
    word_lengths = {word: len(word) for word in ["python", "java", "javascript"]}
    print(f"单词长度: {word_lengths}")
    
    # 集合推导式
    unique_lengths = {len(word) for word in ["python", "java", "go", "rust", "c++"]}
    print(f"唯一长度: {unique_lengths}")
    
    # 嵌套推导式
    matrix = [[i*j for j in range(1, 4)] for i in range(1, 4)]
    print(f"乘法表矩阵: {matrix}")


if __name__ == "__main__":
    main()
    demonstrate_comprehensions()