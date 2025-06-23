#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session12 练习题1：NumPy数组创建和基本操作

题目描述：
本练习旨在帮助你掌握NumPy数组的创建、属性查看和基本操作。
请完成以下任务，每个任务都有具体的要求和期望输出。

练习内容：
1. 数组创建
2. 数组属性
3. 数组索引和切片
4. 数组形状操作

提示：
- 使用import numpy as np导入NumPy
- 注意数组的维度和形状
- 仔细阅读每个任务的要求

作者: Python教程团队
创建日期: 2024-12-19
"""

import numpy as np


def task1_array_creation():
    """
    任务1：数组创建
    
    要求：
    1. 创建一个包含1到20的一维数组
    2. 创建一个3x4的零数组
    3. 创建一个2x3的一数组
    4. 创建一个4x4的单位矩阵
    5. 创建一个包含0到1之间10个等间距数字的数组
    6. 创建一个2x3的随机数组（0-1之间）
    
    返回：包含所有创建数组的字典
    """
    print("=== 任务1：数组创建 ===")
    
    # TODO: 在这里完成你的代码
    # 1. 创建包含1到20的一维数组
    arr_1to20 = None  # 替换为你的代码
    
    # 2. 创建3x4的零数组
    zeros_3x4 = None  # 替换为你的代码
    
    # 3. 创建2x3的一数组
    ones_2x3 = None  # 替换为你的代码
    
    # 4. 创建4x4单位矩阵
    identity_4x4 = None  # 替换为你的代码
    
    # 5. 创建0到1之间10个等间距数字的数组
    linspace_array = None  # 替换为你的代码
    
    # 6. 创建2x3随机数组
    np.random.seed(42)  # 固定随机种子
    random_2x3 = None  # 替换为你的代码
    
    # 打印结果
    print(f"1到20数组: {arr_1to20}")
    print(f"3x4零数组:\n{zeros_3x4}")
    print(f"2x3一数组:\n{ones_2x3}")
    print(f"4x4单位矩阵:\n{identity_4x4}")
    print(f"等间距数组: {linspace_array}")
    print(f"随机数组:\n{random_2x3}")
    
    return {
        'arr_1to20': arr_1to20,
        'zeros_3x4': zeros_3x4,
        'ones_2x3': ones_2x3,
        'identity_4x4': identity_4x4,
        'linspace_array': linspace_array,
        'random_2x3': random_2x3
    }


def task2_array_properties():
    """
    任务2：数组属性
    
    要求：
    1. 创建一个3x4x5的三维数组（元素为1到60）
    2. 打印数组的形状、维度、大小、数据类型
    3. 计算数组占用的总字节数
    4. 将数组转换为浮点类型
    
    返回：数组属性信息字典
    """
    print("\n=== 任务2：数组属性 ===")
    
    # TODO: 在这里完成你的代码
    # 1. 创建3x4x5的三维数组
    arr_3d = None  # 替换为你的代码，提示：使用arange和reshape
    
    # 2. 获取数组属性
    shape = None      # 数组形状
    ndim = None       # 数组维度
    size = None       # 数组大小
    dtype = None      # 数据类型
    itemsize = None   # 每个元素字节数
    nbytes = None     # 总字节数
    
    # 3. 转换数据类型
    arr_float = None  # 转换为浮点类型
    
    # 打印结果
    print(f"数组形状: {shape}")
    print(f"数组维度: {ndim}")
    print(f"数组大小: {size}")
    print(f"数据类型: {dtype}")
    print(f"每元素字节数: {itemsize}")
    print(f"总字节数: {nbytes}")
    print(f"转换后数据类型: {arr_float.dtype if arr_float is not None else None}")
    
    return {
        'array': arr_3d,
        'shape': shape,
        'ndim': ndim,
        'size': size,
        'dtype': dtype,
        'itemsize': itemsize,
        'nbytes': nbytes,
        'float_array': arr_float
    }


def task3_array_indexing():
    """
    任务3：数组索引和切片
    
    要求：
    1. 创建一个5x6的数组，元素为1到30
    2. 获取第3行的所有元素
    3. 获取第2列的所有元素
    4. 获取前3行前4列的子数组
    5. 获取所有大于15的元素
    6. 将所有偶数元素替换为-1
    
    返回：各种索引操作的结果
    """
    print("\n=== 任务3：数组索引和切片 ===")
    
    # TODO: 在这里完成你的代码
    # 1. 创建5x6数组
    arr_5x6 = None  # 替换为你的代码
    
    print(f"原始数组:\n{arr_5x6}")
    
    # 2. 获取第3行（索引为2）
    row_3 = None  # 替换为你的代码
    
    # 3. 获取第2列（索引为1）
    col_2 = None  # 替换为你的代码
    
    # 4. 获取前3行前4列
    sub_array = None  # 替换为你的代码
    
    # 5. 获取大于15的元素
    greater_than_15 = None  # 替换为你的代码
    
    # 6. 将偶数元素替换为-1（在副本上操作）
    arr_modified = arr_5x6.copy() if arr_5x6 is not None else None
    # TODO: 完成偶数替换的代码
    
    # 打印结果
    print(f"第3行: {row_3}")
    print(f"第2列: {col_2}")
    print(f"前3行前4列:\n{sub_array}")
    print(f"大于15的元素: {greater_than_15}")
    print(f"偶数替换为-1后:\n{arr_modified}")
    
    return {
        'original': arr_5x6,
        'row_3': row_3,
        'col_2': col_2,
        'sub_array': sub_array,
        'greater_than_15': greater_than_15,
        'modified': arr_modified
    }


def task4_array_reshaping():
    """
    任务4：数组形状操作
    
    要求：
    1. 创建一个包含1到24的一维数组
    2. 将其重塑为4x6的二维数组
    3. 将其重塑为2x3x4的三维数组
    4. 将三维数组展平为一维
    5. 对二维数组进行转置
    6. 将两个2x3数组垂直拼接
    7. 将两个2x3数组水平拼接
    
    返回：各种形状操作的结果
    """
    print("\n=== 任务4：数组形状操作 ===")
    
    # TODO: 在这里完成你的代码
    # 1. 创建1到24的一维数组
    arr_1d = None  # 替换为你的代码
    
    # 2. 重塑为4x6
    arr_4x6 = None  # 替换为你的代码
    
    # 3. 重塑为2x3x4
    arr_2x3x4 = None  # 替换为你的代码
    
    # 4. 展平为一维
    arr_flattened = None  # 替换为你的代码
    
    # 5. 转置4x6数组
    arr_transposed = None  # 替换为你的代码
    
    # 6. 创建两个2x3数组用于拼接
    arr_a = np.array([[1, 2, 3], [4, 5, 6]])
    arr_b = np.array([[7, 8, 9], [10, 11, 12]])
    
    # 垂直拼接
    vstack_result = None  # 替换为你的代码
    
    # 水平拼接
    hstack_result = None  # 替换为你的代码
    
    # 打印结果
    print(f"原始一维数组: {arr_1d}")
    print(f"4x6数组:\n{arr_4x6}")
    print(f"2x3x4数组形状: {arr_2x3x4.shape if arr_2x3x4 is not None else None}")
    print(f"展平数组: {arr_flattened}")
    print(f"转置后形状: {arr_transposed.shape if arr_transposed is not None else None}")
    print(f"垂直拼接:\n{vstack_result}")
    print(f"水平拼接:\n{hstack_result}")
    
    return {
        'arr_1d': arr_1d,
        'arr_4x6': arr_4x6,
        'arr_2x3x4': arr_2x3x4,
        'arr_flattened': arr_flattened,
        'arr_transposed': arr_transposed,
        'vstack_result': vstack_result,
        'hstack_result': hstack_result
    }


def bonus_task():
    """
    挑战任务：综合应用
    
    要求：
    创建一个学生成绩管理系统的数据结构：
    1. 创建一个5x4的成绩矩阵（5个学生，4门课程）
    2. 每门课程成绩在60-100之间的随机整数
    3. 计算每个学生的平均分
    4. 计算每门课程的平均分
    5. 找出成绩最高的学生和课程
    6. 找出不及格（<60）的成绩位置
    
    返回：成绩分析结果
    """
    print("\n=== 挑战任务：学生成绩管理 ===")
    
    # TODO: 在这里完成你的代码
    np.random.seed(42)  # 固定随机种子
    
    # 1. 创建5x4成绩矩阵
    scores = None  # 替换为你的代码，提示：使用random.randint
    
    # 2. 计算每个学生的平均分
    student_avg = None  # 替换为你的代码
    
    # 3. 计算每门课程的平均分
    course_avg = None  # 替换为你的代码
    
    # 4. 找出最高分学生和课程
    max_score_position = None  # 最高分的位置(行,列)
    max_score_student = None   # 最高分学生索引
    max_score_course = None    # 最高分课程索引
    
    # 5. 找出不及格位置
    fail_positions = None  # 不及格成绩的位置
    
    # 打印结果
    print(f"成绩矩阵:\n{scores}")
    print(f"学生平均分: {student_avg}")
    print(f"课程平均分: {course_avg}")
    print(f"最高分位置: {max_score_position}")
    print(f"最高分学生: 学生{max_score_student}")
    print(f"最高分课程: 课程{max_score_course}")
    print(f"不及格位置: {fail_positions}")
    
    return {
        'scores': scores,
        'student_avg': student_avg,
        'course_avg': course_avg,
        'max_position': max_score_position,
        'fail_positions': fail_positions
    }


def main():
    """
    主函数：运行所有练习任务
    """
    print("Session12 练习题1：NumPy数组创建和基本操作")
    print("=" * 60)
    
    # 运行所有任务
    task1_result = task1_array_creation()
    task2_result = task2_array_properties()
    task3_result = task3_array_indexing()
    task4_result = task4_array_reshaping()
    bonus_result = bonus_task()
    
    print("\n=== 练习完成 ===")
    print("请检查你的输出结果是否正确！")
    print("如果遇到问题，请参考solutions目录中的答案。")


if __name__ == "__main__":
    main()