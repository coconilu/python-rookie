#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session12 练习题1解答：NumPy数组基础操作

本文件包含练习题1的完整解答，展示了NumPy数组的创建、属性、
索引、切片和形状操作的正确实现方法。

作者: Python教程团队
创建日期: 2024-12-19
"""

import numpy as np


def task1_array_creation():
    """
    任务1：数组创建 - 完整解答
    """
    print("=== 任务1：数组创建 - 解答 ===")
    
    # 1. 从列表创建一维数组
    list_1d = [1, 2, 3, 4, 5]
    array_1d = np.array(list_1d)
    print(f"1. 一维数组: {array_1d}")
    
    # 2. 从嵌套列表创建二维数组
    list_2d = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    array_2d = np.array(list_2d)
    print(f"2. 二维数组:\n{array_2d}")
    
    # 3. 创建全零数组
    zeros_array = np.zeros((3, 4))
    print(f"3. 全零数组:\n{zeros_array}")
    
    # 4. 创建全一数组
    ones_array = np.ones((2, 3, 4))
    print(f"4. 全一数组形状: {ones_array.shape}")
    
    # 5. 创建单位矩阵
    identity_matrix = np.eye(4)
    print(f"5. 单位矩阵:\n{identity_matrix}")
    
    # 6. 创建等差数列
    arange_array = np.arange(0, 20, 2)
    print(f"6. 等差数列: {arange_array}")
    
    # 7. 创建等间距数组
    linspace_array = np.linspace(0, 1, 11)
    print(f"7. 等间距数组: {linspace_array}")
    
    # 8. 创建随机数组
    np.random.seed(42)  # 设置随机种子确保结果可重现
    random_array = np.random.random((3, 3))
    print(f"8. 随机数组:\n{random_array}")
    
    # 9. 创建正态分布随机数组
    normal_array = np.random.normal(0, 1, (2, 5))
    print(f"9. 正态分布数组:\n{normal_array}")
    
    # 10. 创建指定值填充的数组
    full_array = np.full((3, 3), 7)
    print(f"10. 指定值填充数组:\n{full_array}")
    
    return {
        'array_1d': array_1d,
        'array_2d': array_2d,
        'zeros_array': zeros_array,
        'ones_array': ones_array,
        'identity_matrix': identity_matrix,
        'arange_array': arange_array,
        'linspace_array': linspace_array,
        'random_array': random_array,
        'normal_array': normal_array,
        'full_array': full_array
    }


def task2_array_properties(arrays):
    """
    任务2：数组属性 - 完整解答
    """
    print("\n=== 任务2：数组属性 - 解答 ===")
    
    array_2d = arrays['array_2d']
    ones_array = arrays['ones_array']
    
    # 1. 形状 (shape)
    shape_2d = array_2d.shape
    shape_3d = ones_array.shape
    print(f"1. 二维数组形状: {shape_2d}")
    print(f"   三维数组形状: {shape_3d}")
    
    # 2. 维度数 (ndim)
    ndim_2d = array_2d.ndim
    ndim_3d = ones_array.ndim
    print(f"2. 二维数组维度数: {ndim_2d}")
    print(f"   三维数组维度数: {ndim_3d}")
    
    # 3. 元素总数 (size)
    size_2d = array_2d.size
    size_3d = ones_array.size
    print(f"3. 二维数组元素总数: {size_2d}")
    print(f"   三维数组元素总数: {size_3d}")
    
    # 4. 数据类型 (dtype)
    dtype_2d = array_2d.dtype
    dtype_3d = ones_array.dtype
    print(f"4. 二维数组数据类型: {dtype_2d}")
    print(f"   三维数组数据类型: {dtype_3d}")
    
    # 5. 每个元素的字节数 (itemsize)
    itemsize_2d = array_2d.itemsize
    itemsize_3d = ones_array.itemsize
    print(f"5. 二维数组每元素字节数: {itemsize_2d}")
    print(f"   三维数组每元素字节数: {itemsize_3d}")
    
    # 6. 数组占用的总字节数 (nbytes)
    nbytes_2d = array_2d.nbytes
    nbytes_3d = ones_array.nbytes
    print(f"6. 二维数组总字节数: {nbytes_2d}")
    print(f"   三维数组总字节数: {nbytes_3d}")
    
    # 7. 类型转换
    float_array = array_2d.astype(np.float64)
    int_array = arrays['random_array'].astype(np.int32)
    print(f"7. 转换为float64: {float_array.dtype}")
    print(f"   转换为int32: {int_array.dtype}")
    
    return {
        'shape_2d': shape_2d,
        'shape_3d': shape_3d,
        'ndim_2d': ndim_2d,
        'ndim_3d': ndim_3d,
        'size_2d': size_2d,
        'size_3d': size_3d,
        'dtype_2d': dtype_2d,
        'dtype_3d': dtype_3d,
        'float_array': float_array,
        'int_array': int_array
    }


def task3_array_indexing_slicing(arrays):
    """
    任务3：数组索引和切片 - 完整解答
    """
    print("\n=== 任务3：数组索引和切片 - 解答 ===")
    
    array_1d = arrays['array_1d']
    array_2d = arrays['array_2d']
    
    # 1. 一维数组索引
    first_element = array_1d[0]
    last_element = array_1d[-1]
    middle_element = array_1d[2]
    print(f"1. 一维数组索引:")
    print(f"   第一个元素: {first_element}")
    print(f"   最后一个元素: {last_element}")
    print(f"   中间元素: {middle_element}")
    
    # 2. 一维数组切片
    first_three = array_1d[:3]
    last_two = array_1d[-2:]
    every_second = array_1d[::2]
    reverse_array = array_1d[::-1]
    print(f"2. 一维数组切片:")
    print(f"   前三个元素: {first_three}")
    print(f"   后两个元素: {last_two}")
    print(f"   每隔一个元素: {every_second}")
    print(f"   反转数组: {reverse_array}")
    
    # 3. 二维数组索引
    element_1_1 = array_2d[1, 1]
    element_0_2 = array_2d[0, 2]
    element_2_0 = array_2d[2, 0]
    print(f"3. 二维数组索引:")
    print(f"   [1,1]位置元素: {element_1_1}")
    print(f"   [0,2]位置元素: {element_0_2}")
    print(f"   [2,0]位置元素: {element_2_0}")
    
    # 4. 二维数组切片
    first_row = array_2d[0, :]
    last_column = array_2d[:, -1]
    subarray = array_2d[1:3, 0:2]
    print(f"4. 二维数组切片:")
    print(f"   第一行: {first_row}")
    print(f"   最后一列: {last_column}")
    print(f"   子数组[1:3, 0:2]:\n{subarray}")
    
    # 5. 布尔索引
    bool_mask = array_1d > 3
    filtered_elements = array_1d[bool_mask]
    print(f"5. 布尔索引:")
    print(f"   布尔掩码: {bool_mask}")
    print(f"   大于3的元素: {filtered_elements}")
    
    # 6. 花式索引
    indices = [0, 2, 4]
    fancy_indexed = array_1d[indices]
    print(f"6. 花式索引:")
    print(f"   索引[0,2,4]对应元素: {fancy_indexed}")
    
    # 7. 二维数组的布尔索引
    bool_mask_2d = array_2d > 5
    filtered_2d = array_2d[bool_mask_2d]
    print(f"7. 二维数组布尔索引:")
    print(f"   大于5的元素: {filtered_2d}")
    
    return {
        'first_element': first_element,
        'last_element': last_element,
        'first_three': first_three,
        'last_two': last_two,
        'every_second': every_second,
        'reverse_array': reverse_array,
        'element_1_1': element_1_1,
        'first_row': first_row,
        'last_column': last_column,
        'subarray': subarray,
        'filtered_elements': filtered_elements,
        'fancy_indexed': fancy_indexed,
        'filtered_2d': filtered_2d
    }


def task4_array_modification(arrays):
    """
    任务4：数组修改 - 完整解答
    """
    print("\n=== 任务4：数组修改 - 解答 ===")
    
    # 创建数组副本以避免修改原数组
    array_1d = arrays['array_1d'].copy()
    array_2d = arrays['array_2d'].copy()
    
    # 1. 单个元素赋值
    print(f"1. 修改前一维数组: {array_1d}")
    array_1d[0] = 10
    array_1d[-1] = 50
    print(f"   修改后一维数组: {array_1d}")
    
    # 2. 切片赋值
    array_1d[1:3] = [20, 30]
    print(f"2. 切片赋值后: {array_1d}")
    
    # 3. 二维数组元素修改
    print(f"3. 修改前二维数组:\n{array_2d}")
    array_2d[1, 1] = 99
    array_2d[0, :] = [10, 20, 30]
    print(f"   修改后二维数组:\n{array_2d}")
    
    # 4. 条件赋值
    condition_array = np.array([1, 2, 3, 4, 5, 6])
    print(f"4. 原数组: {condition_array}")
    condition_array[condition_array > 3] = 0
    print(f"   条件赋值后(>3的设为0): {condition_array}")
    
    # 5. 使用np.where进行条件替换
    original = np.array([1, 2, 3, 4, 5, 6])
    replaced = np.where(original > 3, 100, original)
    print(f"5. np.where替换:")
    print(f"   原数组: {original}")
    print(f"   替换后(>3的设为100): {replaced}")
    
    # 6. 批量修改
    batch_array = np.arange(10)
    print(f"6. 批量修改前: {batch_array}")
    batch_array[batch_array % 2 == 0] *= 10  # 偶数乘以10
    print(f"   偶数乘以10后: {batch_array}")
    
    return {
        'modified_1d': array_1d,
        'modified_2d': array_2d,
        'condition_array': condition_array,
        'replaced': replaced,
        'batch_array': batch_array
    }


def task5_array_reshaping(arrays):
    """
    任务5：数组形状操作 - 完整解答
    """
    print("\n=== 任务5：数组形状操作 - 解答 ===")
    
    # 1. reshape操作
    array_1d = arrays['arange_array']  # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
    print(f"1. 原一维数组: {array_1d}")
    reshaped_2d = array_1d.reshape(5, 2)
    print(f"   reshape为(5,2):\n{reshaped_2d}")
    
    reshaped_3d = array_1d.reshape(2, 5, 1)
    print(f"   reshape为(2,5,1)形状: {reshaped_3d.shape}")
    
    # 2. 自动推断维度
    auto_reshape = array_1d.reshape(-1, 2)  # 自动推断第一个维度
    print(f"2. 自动推断维度(-1,2):\n{auto_reshape}")
    
    # 3. flatten操作
    array_2d = arrays['array_2d']
    flattened = array_2d.flatten()
    print(f"3. 二维数组:\n{array_2d}")
    print(f"   flatten后: {flattened}")
    
    # 4. ravel操作（返回视图）
    raveled = array_2d.ravel()
    print(f"4. ravel后: {raveled}")
    
    # 5. 转置操作
    transposed = array_2d.T
    print(f"5. 转置前:\n{array_2d}")
    print(f"   转置后:\n{transposed}")
    
    # 6. 交换轴
    array_3d = arrays['ones_array']  # (2, 3, 4)
    swapped = np.swapaxes(array_3d, 0, 2)  # 交换第0轴和第2轴
    print(f"6. 三维数组原形状: {array_3d.shape}")
    print(f"   交换轴后形状: {swapped.shape}")
    
    # 7. 扩展维度
    expanded = np.expand_dims(array_1d, axis=0)
    print(f"7. 原数组形状: {array_1d.shape}")
    print(f"   扩展维度后形状: {expanded.shape}")
    
    # 8. 压缩维度
    squeezed = np.squeeze(expanded)
    print(f"8. 压缩维度后形状: {squeezed.shape}")
    
    return {
        'reshaped_2d': reshaped_2d,
        'reshaped_3d': reshaped_3d,
        'auto_reshape': auto_reshape,
        'flattened': flattened,
        'raveled': raveled,
        'transposed': transposed,
        'swapped': swapped,
        'expanded': expanded,
        'squeezed': squeezed
    }


def bonus_student_grade_system():
    """
    奖励任务：学生成绩管理系统 - 完整解答
    """
    print("\n=== 奖励任务：学生成绩管理系统 - 解答 ===")
    
    # 1. 创建成绩数据
    np.random.seed(42)
    num_students = 30
    num_subjects = 5
    
    # 生成成绩数据（60-100分）
    grades = np.random.randint(60, 101, (num_students, num_subjects))
    
    # 科目名称
    subjects = ['数学', '语文', '英语', '物理', '化学']
    
    print(f"1. 成绩数据形状: {grades.shape}")
    print(f"   科目: {subjects}")
    print(f"   前5名学生成绩:\n{grades[:5]}")
    
    # 2. 计算每个学生的总分和平均分
    total_scores = np.sum(grades, axis=1)
    average_scores = np.mean(grades, axis=1)
    
    print(f"\n2. 学生成绩统计:")
    print(f"   前5名学生总分: {total_scores[:5]}")
    print(f"   前5名学生平均分: {average_scores[:5]:.2f}")
    
    # 3. 计算每个科目的平均分
    subject_averages = np.mean(grades, axis=0)
    print(f"\n3. 各科目平均分:")
    for i, subject in enumerate(subjects):
        print(f"   {subject}: {subject_averages[i]:.2f}")
    
    # 4. 找出最高分和最低分
    max_score = np.max(grades)
    min_score = np.min(grades)
    max_position = np.unravel_index(np.argmax(grades), grades.shape)
    min_position = np.unravel_index(np.argmin(grades), grades.shape)
    
    print(f"\n4. 极值分析:")
    print(f"   最高分: {max_score} (学生{max_position[0]+1}, {subjects[max_position[1]]})")
    print(f"   最低分: {min_score} (学生{min_position[0]+1}, {subjects[min_position[1]]})")
    
    # 5. 成绩等级划分
    def grade_to_level(score):
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
    
    # 使用向量化函数
    vectorized_grade_to_level = np.vectorize(grade_to_level)
    grade_levels = vectorized_grade_to_level(grades)
    
    print(f"\n5. 成绩等级分布:")
    unique_levels, counts = np.unique(grade_levels, return_counts=True)
    for level, count in zip(unique_levels, counts):
        print(f"   等级{level}: {count}人次")
    
    # 6. 找出优秀学生（平均分>=85）
    excellent_students = np.where(average_scores >= 85)[0]
    print(f"\n6. 优秀学生(平均分>=85):")
    print(f"   学生编号: {excellent_students + 1}")
    print(f"   人数: {len(excellent_students)}")
    
    # 7. 科目难度分析（通过平均分和标准差）
    subject_std = np.std(grades, axis=0)
    print(f"\n7. 科目难度分析:")
    for i, subject in enumerate(subjects):
        difficulty = "简单" if subject_averages[i] > 80 else "中等" if subject_averages[i] > 70 else "困难"
        print(f"   {subject}: 平均分{subject_averages[i]:.2f}, 标准差{subject_std[i]:.2f}, 难度{difficulty}")
    
    # 8. 成绩改进建议
    print(f"\n8. 成绩改进建议:")
    
    # 找出需要重点关注的学生（平均分<70）
    struggling_students = np.where(average_scores < 70)[0]
    if len(struggling_students) > 0:
        print(f"   需要重点关注的学生: {struggling_students + 1}")
    
    # 找出最需要改进的科目（平均分最低）
    worst_subject_idx = np.argmin(subject_averages)
    print(f"   最需要改进的科目: {subjects[worst_subject_idx]} (平均分: {subject_averages[worst_subject_idx]:.2f})")
    
    # 9. 生成成绩报告
    print(f"\n9. 班级成绩报告:")
    print(f"   总人数: {num_students}")
    print(f"   班级平均分: {np.mean(average_scores):.2f}")
    print(f"   最高平均分: {np.max(average_scores):.2f}")
    print(f"   最低平均分: {np.min(average_scores):.2f}")
    print(f"   及格率: {len(np.where(average_scores >= 60)[0]) / num_students * 100:.1f}%")
    print(f"   优秀率: {len(excellent_students) / num_students * 100:.1f}%")
    
    return {
        'grades': grades,
        'total_scores': total_scores,
        'average_scores': average_scores,
        'subject_averages': subject_averages,
        'grade_levels': grade_levels,
        'excellent_students': excellent_students,
        'struggling_students': struggling_students,
        'subjects': subjects
    }


def main():
    """主函数"""
    print("Session12 练习题1完整解答：NumPy数组基础操作")
    print("=" * 60)
    
    # 执行所有任务
    arrays = task1_array_creation()
    properties = task2_array_properties(arrays)
    indexing = task3_array_indexing_slicing(arrays)
    modification = task4_array_modification(arrays)
    reshaping = task5_array_reshaping(arrays)
    bonus = bonus_student_grade_system()
    
    print("\n" + "=" * 60)
    print("所有任务完成！")
    print("\n学习要点总结:")
    print("1. NumPy数组的多种创建方法")
    print("2. 数组属性的查看和类型转换")
    print("3. 灵活的索引和切片操作")
    print("4. 数组元素的修改和条件赋值")
    print("5. 数组形状的变换和操作")
    print("6. 实际应用：学生成绩管理系统")
    print("=" * 60)


if __name__ == "__main__":
    main()