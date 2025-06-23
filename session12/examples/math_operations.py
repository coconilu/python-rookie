#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NumPy数学运算示例

本文件演示NumPy的各种数学运算功能，包括：
- 基本算术运算
- 数学函数
- 线性代数运算
- 广播机制

作者: Python教程团队
创建日期: 2024-12-19
"""

import numpy as np


def basic_arithmetic_examples():
    """
    演示基本算术运算
    """
    print("=== 基本算术运算示例 ===")
    
    arr1 = np.array([1, 2, 3, 4])
    arr2 = np.array([5, 6, 7, 8])
    
    print(f"数组1: {arr1}")
    print(f"数组2: {arr2}")
    
    # 基本运算
    print("\n1. 基本运算:")
    print(f"加法: {arr1 + arr2}")
    print(f"减法: {arr2 - arr1}")
    print(f"乘法: {arr1 * arr2}")
    print(f"除法: {arr2 / arr1}")
    print(f"整除: {arr2 // arr1}")
    print(f"取余: {arr2 % arr1}")
    print(f"幂运算: {arr1 ** 2}")
    
    # 标量运算
    print("\n2. 标量运算:")
    scalar = 3
    print(f"数组: {arr1}")
    print(f"标量: {scalar}")
    print(f"数组 + 标量: {arr1 + scalar}")
    print(f"数组 * 标量: {arr1 * scalar}")
    print(f"数组 ** 标量: {arr1 ** scalar}")
    
    # 复合赋值运算
    print("\n3. 复合赋值运算:")
    arr_copy = arr1.copy()
    print(f"原数组: {arr_copy}")
    
    arr_copy += 10
    print(f"+=10后: {arr_copy}")
    
    arr_copy *= 2
    print(f"*=2后: {arr_copy}")


def mathematical_functions_examples():
    """
    演示数学函数
    """
    print("\n=== 数学函数示例 ===")
    
    # 基本数学函数
    print("1. 基本数学函数:")
    arr = np.array([1, 4, 9, 16, 25])
    print(f"原数组: {arr}")
    print(f"平方根: {np.sqrt(arr)}")
    print(f"平方: {np.square(arr)}")
    print(f"绝对值: {np.abs(np.array([-1, -2, 3, -4]))}")
    
    # 指数和对数函数
    print("\n2. 指数和对数函数:")
    arr = np.array([1, 2, 3, 4])
    print(f"原数组: {arr}")
    print(f"e^x: {np.exp(arr)}")
    print(f"2^x: {np.power(2, arr)}")
    print(f"ln(x): {np.log(arr)}")
    print(f"log10(x): {np.log10(arr)}")
    print(f"log2(x): {np.log2(arr)}")
    
    # 三角函数
    print("\n3. 三角函数:")
    angles = np.array([0, np.pi/6, np.pi/4, np.pi/3, np.pi/2])
    print(f"角度(弧度): {angles}")
    print(f"角度(度): {np.degrees(angles)}")
    print(f"sin: {np.sin(angles)}")
    print(f"cos: {np.cos(angles)}")
    print(f"tan: {np.tan(angles)}")
    
    # 反三角函数
    values = np.array([0, 0.5, 0.707, 0.866, 1])
    print(f"\n值: {values}")
    print(f"arcsin: {np.arcsin(values)}")
    print(f"arccos: {np.arccos(values)}")
    print(f"arctan: {np.arctan(values)}")
    
    # 双曲函数
    print("\n4. 双曲函数:")
    x = np.array([0, 1, 2])
    print(f"x: {x}")
    print(f"sinh: {np.sinh(x)}")
    print(f"cosh: {np.cosh(x)}")
    print(f"tanh: {np.tanh(x)}")


def rounding_functions_examples():
    """
    演示舍入函数
    """
    print("\n=== 舍入函数示例 ===")
    
    arr = np.array([1.2, 2.7, -1.3, -2.8, 3.5, 4.5])
    print(f"原数组: {arr}")
    
    print(f"四舍五入: {np.round(arr)}")
    print(f"向下取整: {np.floor(arr)}")
    print(f"向上取整: {np.ceil(arr)}")
    print(f"截断取整: {np.trunc(arr)}")
    
    # 指定小数位数
    print(f"\n保留1位小数: {np.round(arr, 1)}")
    print(f"保留到十位: {np.round(arr, -1)}")


def comparison_functions_examples():
    """
    演示比较函数
    """
    print("\n=== 比较函数示例 ===")
    
    arr1 = np.array([1, 2, 3, 4, 5])
    arr2 = np.array([1, 3, 2, 4, 6])
    
    print(f"数组1: {arr1}")
    print(f"数组2: {arr2}")
    
    print(f"\n相等: {np.equal(arr1, arr2)}")
    print(f"不等: {np.not_equal(arr1, arr2)}")
    print(f"小于: {np.less(arr1, arr2)}")
    print(f"小于等于: {np.less_equal(arr1, arr2)}")
    print(f"大于: {np.greater(arr1, arr2)}")
    print(f"大于等于: {np.greater_equal(arr1, arr2)}")
    
    # 逻辑运算
    print("\n逻辑运算:")
    mask1 = arr1 > 2
    mask2 = arr1 < 5
    print(f"arr1 > 2: {mask1}")
    print(f"arr1 < 5: {mask2}")
    print(f"逻辑与: {np.logical_and(mask1, mask2)}")
    print(f"逻辑或: {np.logical_or(mask1, mask2)}")
    print(f"逻辑非: {np.logical_not(mask1)}")


def broadcasting_examples():
    """
    演示广播机制
    """
    print("\n=== 广播机制示例 ===")
    
    # 标量与数组
    print("1. 标量与数组:")
    arr = np.array([[1, 2, 3], [4, 5, 6]])
    scalar = 10
    print(f"数组:\n{arr}")
    print(f"标量: {scalar}")
    print(f"数组 + 标量:\n{arr + scalar}")
    
    # 一维数组与二维数组
    print("\n2. 一维数组与二维数组:")
    arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
    arr_1d = np.array([10, 20, 30])
    print(f"2D数组:\n{arr_2d}")
    print(f"1D数组: {arr_1d}")
    print(f"广播相加:\n{arr_2d + arr_1d}")
    
    # 不同形状的二维数组
    print("\n3. 不同形状的二维数组:")
    arr1 = np.array([[1], [2], [3]])
    arr2 = np.array([10, 20, 30])
    print(f"数组1 (3x1):\n{arr1}")
    print(f"数组2 (1x3): {arr2}")
    print(f"广播相加:\n{arr1 + arr2}")
    
    # 广播规则演示
    print("\n4. 广播规则演示:")
    print("广播规则：")
    print("- 从右向左比较维度")
    print("- 维度相等或其中一个为1时可以广播")
    print("- 缺失的维度视为1")
    
    examples = [
        ((3, 4), (4,)),      # (3,4) + (4,) -> (3,4)
        ((3, 4), (3, 1)),    # (3,4) + (3,1) -> (3,4)
        ((3, 1), (1, 4)),    # (3,1) + (1,4) -> (3,4)
    ]
    
    for shape1, shape2 in examples:
        arr1 = np.ones(shape1)
        arr2 = np.ones(shape2)
        result = arr1 + arr2
        print(f"{shape1} + {shape2} -> {result.shape}")


def linear_algebra_examples():
    """
    演示线性代数运算
    """
    print("\n=== 线性代数示例 ===")
    
    # 矩阵乘法
    print("1. 矩阵乘法:")
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    
    print(f"矩阵A:\n{A}")
    print(f"矩阵B:\n{B}")
    
    # 点积
    dot_product = np.dot(A, B)
    print(f"点积 np.dot(A, B):\n{dot_product}")
    
    # @操作符
    matmul_product = A @ B
    print(f"矩阵乘法 A @ B:\n{matmul_product}")
    
    # 向量点积
    print("\n2. 向量运算:")
    v1 = np.array([1, 2, 3])
    v2 = np.array([4, 5, 6])
    print(f"向量1: {v1}")
    print(f"向量2: {v2}")
    print(f"点积: {np.dot(v1, v2)}")
    print(f"叉积: {np.cross(v1, v2)}")
    
    # 矩阵运算
    print("\n3. 矩阵运算:")
    matrix = np.array([[1, 2], [3, 4]])
    print(f"矩阵:\n{matrix}")
    
    # 转置
    print(f"转置:\n{matrix.T}")
    
    # 行列式
    det = np.linalg.det(matrix)
    print(f"行列式: {det}")
    
    # 逆矩阵
    try:
        inv = np.linalg.inv(matrix)
        print(f"逆矩阵:\n{inv}")
        
        # 验证逆矩阵
        identity = matrix @ inv
        print(f"验证 A * A^(-1):\n{identity}")
    except np.linalg.LinAlgError:
        print("矩阵不可逆")
    
    # 特征值和特征向量
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    print(f"特征值: {eigenvalues}")
    print(f"特征向量:\n{eigenvectors}")


def aggregation_functions_examples():
    """
    演示聚合函数
    """
    print("\n=== 聚合函数示例 ===")
    
    # 创建示例数据
    data = np.array([[1, 2, 3, 4],
                     [5, 6, 7, 8],
                     [9, 10, 11, 12]])
    
    print(f"示例数据:\n{data}")
    
    # 基本聚合
    print("\n1. 基本聚合:")
    print(f"总和: {np.sum(data)}")
    print(f"平均值: {np.mean(data)}")
    print(f"最小值: {np.min(data)}")
    print(f"最大值: {np.max(data)}")
    print(f"标准差: {np.std(data)}")
    print(f"方差: {np.var(data)}")
    
    # 按轴聚合
    print("\n2. 按轴聚合:")
    print(f"按行求和 (axis=1): {np.sum(data, axis=1)}")
    print(f"按列求和 (axis=0): {np.sum(data, axis=0)}")
    print(f"按列平均 (axis=0): {np.mean(data, axis=0)}")
    
    # 累积函数
    print("\n3. 累积函数:")
    arr = np.array([1, 2, 3, 4, 5])
    print(f"原数组: {arr}")
    print(f"累积和: {np.cumsum(arr)}")
    print(f"累积积: {np.cumprod(arr)}")
    
    # 排序相关
    print("\n4. 排序相关:")
    arr = np.array([3, 1, 4, 1, 5, 9, 2, 6])
    print(f"原数组: {arr}")
    print(f"排序: {np.sort(arr)}")
    print(f"排序索引: {np.argsort(arr)}")
    print(f"最小值索引: {np.argmin(arr)}")
    print(f"最大值索引: {np.argmax(arr)}")


def main():
    """
    主函数：运行所有示例
    """
    print("NumPy数学运算示例")
    print("=" * 50)
    
    basic_arithmetic_examples()
    mathematical_functions_examples()
    rounding_functions_examples()
    comparison_functions_examples()
    broadcasting_examples()
    linear_algebra_examples()
    aggregation_functions_examples()
    
    print("\n示例演示完成！")


if __name__ == "__main__":
    main()