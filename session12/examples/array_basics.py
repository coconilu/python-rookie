#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NumPy数组基础操作示例

本文件演示NumPy数组的创建、属性、索引和基本操作

作者: Python教程团队
创建日期: 2024-12-19
"""

import numpy as np


def array_creation_examples():
    """
    演示各种数组创建方法
    """
    print("=== 数组创建示例 ===")
    
    # 从Python列表创建
    print("1. 从列表创建数组:")
    list_1d = [1, 2, 3, 4, 5]
    arr_1d = np.array(list_1d)
    print(f"一维数组: {arr_1d}")
    
    list_2d = [[1, 2, 3], [4, 5, 6]]
    arr_2d = np.array(list_2d)
    print(f"二维数组:\n{arr_2d}")
    
    # 使用NumPy函数创建
    print("\n2. 使用NumPy函数创建:")
    zeros = np.zeros((3, 4))
    print(f"零数组:\n{zeros}")
    
    ones = np.ones((2, 3))
    print(f"一数组:\n{ones}")
    
    full = np.full((2, 2), 7)
    print(f"填充数组:\n{full}")
    
    eye = np.eye(3)
    print(f"单位矩阵:\n{eye}")
    
    # 数值序列
    print("\n3. 数值序列:")
    arange_arr = np.arange(0, 10, 2)
    print(f"arange(0, 10, 2): {arange_arr}")
    
    linspace_arr = np.linspace(0, 1, 6)
    print(f"linspace(0, 1, 6): {linspace_arr}")
    
    logspace_arr = np.logspace(0, 2, 5)
    print(f"logspace(0, 2, 5): {logspace_arr}")
    
    # 随机数组
    print("\n4. 随机数组:")
    np.random.seed(42)  # 设置随机种子以获得可重复结果
    
    random_uniform = np.random.random((2, 3))
    print(f"均匀分布随机数:\n{random_uniform}")
    
    random_normal = np.random.normal(0, 1, (2, 3))
    print(f"正态分布随机数:\n{random_normal}")
    
    random_int = np.random.randint(1, 10, (2, 3))
    print(f"随机整数:\n{random_int}")


def array_properties_examples():
    """
    演示数组属性
    """
    print("\n=== 数组属性示例 ===")
    
    arr = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
    print(f"示例数组:\n{arr}")
    
    print(f"\n数组属性:")
    print(f"形状 (shape): {arr.shape}")
    print(f"维度 (ndim): {arr.ndim}")
    print(f"大小 (size): {arr.size}")
    print(f"数据类型 (dtype): {arr.dtype}")
    print(f"每个元素字节数 (itemsize): {arr.itemsize}")
    print(f"总字节数 (nbytes): {arr.nbytes}")
    
    # 数据类型转换
    print("\n数据类型转换:")
    int_arr = np.array([1, 2, 3, 4])
    print(f"整数数组: {int_arr}, 类型: {int_arr.dtype}")
    
    float_arr = int_arr.astype(float)
    print(f"转换为浮点: {float_arr}, 类型: {float_arr.dtype}")
    
    str_arr = int_arr.astype(str)
    print(f"转换为字符串: {str_arr}, 类型: {str_arr.dtype}")


def array_indexing_examples():
    """
    演示数组索引和切片
    """
    print("\n=== 数组索引和切片示例 ===")
    
    # 一维数组索引
    print("1. 一维数组索引:")
    arr_1d = np.array([10, 20, 30, 40, 50])
    print(f"数组: {arr_1d}")
    print(f"第一个元素: {arr_1d[0]}")
    print(f"最后一个元素: {arr_1d[-1]}")
    print(f"前三个元素: {arr_1d[:3]}")
    print(f"后三个元素: {arr_1d[-3:]}")
    print(f"步长为2: {arr_1d[::2]}")
    
    # 二维数组索引
    print("\n2. 二维数组索引:")
    arr_2d = np.array([[1, 2, 3, 4],
                       [5, 6, 7, 8],
                       [9, 10, 11, 12]])
    print(f"数组:\n{arr_2d}")
    print(f"第2行第3列元素: {arr_2d[1, 2]}")
    print(f"第一行: {arr_2d[0, :]}")
    print(f"第二列: {arr_2d[:, 1]}")
    print(f"前两行前三列:\n{arr_2d[:2, :3]}")
    
    # 布尔索引
    print("\n3. 布尔索引:")
    arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(f"原数组: {arr}")
    
    # 条件筛选
    mask = arr > 5
    print(f"大于5的掩码: {mask}")
    print(f"大于5的元素: {arr[mask]}")
    
    # 多条件
    complex_mask = (arr > 3) & (arr < 8)
    print(f"3到8之间的元素: {arr[complex_mask]}")
    
    # 花式索引
    print("\n4. 花式索引:")
    indices = [0, 2, 4]
    print(f"索引{indices}对应的元素: {arr[indices]}")
    
    # 二维数组的花式索引
    rows = [0, 2]
    cols = [1, 3]
    print(f"行{rows}列{cols}的元素: {arr_2d[rows, cols]}")


def array_modification_examples():
    """
    演示数组修改操作
    """
    print("\n=== 数组修改示例 ===")
    
    # 元素赋值
    print("1. 元素赋值:")
    arr = np.array([1, 2, 3, 4, 5])
    print(f"原数组: {arr}")
    
    arr[0] = 10
    print(f"修改第一个元素: {arr}")
    
    arr[1:4] = [20, 30, 40]
    print(f"修改切片: {arr}")
    
    # 条件赋值
    print("\n2. 条件赋值:")
    arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(f"原数组: {arr}")
    
    arr[arr > 5] = 0
    print(f"将大于5的元素设为0: {arr}")
    
    # 使用where函数
    print("\n3. 使用where函数:")
    arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    result = np.where(arr > 5, arr, 0)
    print(f"原数组: {arr}")
    print(f"大于5保留，否则为0: {result}")
    
    # 复杂条件
    result2 = np.where(arr % 2 == 0, arr * 2, arr)
    print(f"偶数翻倍，奇数不变: {result2}")


def main():
    """
    主函数：运行所有示例
    """
    print("NumPy数组基础操作示例")
    print("=" * 50)
    
    array_creation_examples()
    array_properties_examples()
    array_indexing_examples()
    array_modification_examples()
    
    print("\n示例演示完成！")


if __name__ == "__main__":
    main()