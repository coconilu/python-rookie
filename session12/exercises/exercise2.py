#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session12 练习题2：NumPy数学运算和统计分析

题目描述：
本练习旨在帮助你掌握NumPy的数学运算和统计分析功能。
通过实际的数据分析场景，学习如何使用NumPy进行数值计算。

练习内容：
1. 基本数学运算
2. 统计分析
3. 线性代数运算
4. 广播机制应用

提示：
- 注意数组的形状和广播规则
- 使用合适的轴参数进行统计计算
- 理解线性代数运算的含义

作者: Python教程团队
创建日期: 2024-12-19
"""

import numpy as np


def task1_mathematical_operations():
    """
    任务1：基本数学运算
    
    要求：
    1. 创建两个3x3矩阵A和B
    2. 计算A+B, A-B, A*B（元素级乘法）, A/B
    3. 计算A的平方根、对数、指数
    4. 计算A和B的矩阵乘法
    5. 使用广播机制：A与标量10的运算
    
    返回：运算结果字典
    """
    print("=== 任务1：基本数学运算 ===")
    
    # TODO: 在这里完成你的代码
    # 1. 创建两个3x3矩阵
    np.random.seed(42)
    A = None  # 创建3x3矩阵，元素为1-9
    B = None  # 创建3x3矩阵，元素为2-10
    
    print(f"矩阵A:\n{A}")
    print(f"矩阵B:\n{B}")
    
    # 2. 基本运算
    add_result = None      # A + B
    sub_result = None      # A - B
    mul_result = None      # A * B (元素级)
    div_result = None      # A / B
    
    # 3. 数学函数
    sqrt_A = None          # A的平方根
    log_A = None           # A的自然对数
    exp_A = None           # A的指数
    
    # 4. 矩阵乘法
    matmul_result = None   # A @ B
    
    # 5. 广播运算
    scalar = 10
    broadcast_add = None   # A + scalar
    broadcast_mul = None   # A * scalar
    
    # 打印结果
    print(f"\nA + B:\n{add_result}")
    print(f"A - B:\n{sub_result}")
    print(f"A * B (元素级):\n{mul_result}")
    print(f"A / B:\n{div_result}")
    print(f"sqrt(A):\n{sqrt_A}")
    print(f"A @ B (矩阵乘法):\n{matmul_result}")
    print(f"A + {scalar}:\n{broadcast_add}")
    
    return {
        'A': A, 'B': B,
        'add': add_result, 'sub': sub_result,
        'mul': mul_result, 'div': div_result,
        'sqrt_A': sqrt_A, 'log_A': log_A, 'exp_A': exp_A,
        'matmul': matmul_result,
        'broadcast_add': broadcast_add, 'broadcast_mul': broadcast_mul
    }


def task2_statistical_analysis():
    """
    任务2：统计分析
    
    要求：
    1. 生成100个正态分布的随机数（均值50，标准差10）
    2. 计算基本统计量：均值、中位数、标准差、方差
    3. 计算分位数：25%, 50%, 75%, 90%
    4. 创建一个4x5的矩阵，计算按行和按列的统计量
    5. 找出异常值（使用Z-score方法，阈值为2）
    
    返回：统计分析结果
    """
    print("\n=== 任务2：统计分析 ===")
    
    # TODO: 在这里完成你的代码
    np.random.seed(42)
    
    # 1. 生成正态分布数据
    data = None  # 100个正态分布随机数，均值50，标准差10
    
    print(f"数据前10个值: {data[:10] if data is not None else None}")
    
    # 2. 基本统计量
    mean_val = None        # 均值
    median_val = None      # 中位数
    std_val = None         # 标准差
    var_val = None         # 方差
    min_val = None         # 最小值
    max_val = None         # 最大值
    
    # 3. 分位数
    q25 = None             # 25%分位数
    q50 = None             # 50%分位数
    q75 = None             # 75%分位数
    q90 = None             # 90%分位数
    
    # 4. 矩阵统计
    matrix_4x5 = None      # 创建4x5矩阵，元素为1-20
    row_means = None       # 按行计算均值
    col_means = None       # 按列计算均值
    row_sums = None        # 按行求和
    col_sums = None        # 按列求和
    
    # 5. 异常值检测
    z_scores = None        # 计算Z-score
    outliers = None        # 找出异常值（|z_score| > 2）
    outlier_indices = None # 异常值的索引
    
    # 打印结果
    print(f"\n基本统计量:")
    print(f"均值: {mean_val:.2f}")
    print(f"中位数: {median_val:.2f}")
    print(f"标准差: {std_val:.2f}")
    print(f"方差: {var_val:.2f}")
    print(f"范围: [{min_val:.2f}, {max_val:.2f}]")
    
    print(f"\n分位数:")
    print(f"25%: {q25:.2f}, 50%: {q50:.2f}, 75%: {q75:.2f}, 90%: {q90:.2f}")
    
    print(f"\n矩阵统计:")
    print(f"4x5矩阵:\n{matrix_4x5}")
    print(f"按行均值: {row_means}")
    print(f"按列均值: {col_means}")
    
    print(f"\n异常值检测:")
    print(f"异常值数量: {len(outliers) if outliers is not None else 0}")
    print(f"异常值: {outliers}")
    
    return {
        'data': data,
        'mean': mean_val, 'median': median_val, 'std': std_val, 'var': var_val,
        'percentiles': {'q25': q25, 'q50': q50, 'q75': q75, 'q90': q90},
        'matrix': matrix_4x5, 'row_means': row_means, 'col_means': col_means,
        'outliers': outliers, 'outlier_indices': outlier_indices
    }


def task3_linear_algebra():
    """
    任务3：线性代数运算
    
    要求：
    1. 创建一个3x3的可逆矩阵
    2. 计算矩阵的行列式
    3. 计算矩阵的逆
    4. 验证 A * A^(-1) = I
    5. 计算矩阵的特征值和特征向量
    6. 解线性方程组 Ax = b
    
    返回：线性代数运算结果
    """
    print("\n=== 任务3：线性代数运算 ===")
    
    # TODO: 在这里完成你的代码
    # 1. 创建可逆矩阵
    A = np.array([[2, 1, 1],
                  [1, 3, 2],
                  [1, 0, 0]])
    
    print(f"矩阵A:\n{A}")
    
    # 2. 计算行列式
    det_A = None           # 行列式
    
    # 3. 计算逆矩阵
    inv_A = None           # 逆矩阵
    
    # 4. 验证逆矩阵
    identity_check = None  # A @ inv_A
    
    # 5. 特征值和特征向量
    eigenvalues = None     # 特征值
    eigenvectors = None    # 特征向量
    
    # 6. 解线性方程组 Ax = b
    b = np.array([6, 8, 2])
    x_solution = None      # 方程组的解
    
    # 验证解
    verification = None    # A @ x_solution
    
    # 打印结果
    print(f"\n行列式: {det_A:.3f}")
    print(f"逆矩阵:\n{inv_A}")
    print(f"验证 A * A^(-1):\n{identity_check}")
    print(f"特征值: {eigenvalues}")
    print(f"特征向量:\n{eigenvectors}")
    print(f"\n线性方程组 Ax = b:")
    print(f"b = {b}")
    print(f"解 x = {x_solution}")
    print(f"验证 Ax = {verification}")
    
    return {
        'matrix': A,
        'determinant': det_A,
        'inverse': inv_A,
        'identity_check': identity_check,
        'eigenvalues': eigenvalues,
        'eigenvectors': eigenvectors,
        'solution': x_solution,
        'verification': verification
    }


def task4_broadcasting_applications():
    """
    任务4：广播机制应用
    
    要求：
    1. 创建一个学生成绩矩阵（5学生 x 3科目）
    2. 每科目有不同的权重：[0.3, 0.4, 0.3]
    3. 使用广播计算加权平均分
    4. 对每科成绩进行标准化（减去均值除以标准差）
    5. 给每个学生的成绩加上不同的奖励分：[2, 1, 3, 0, 1]
    
    返回：广播应用结果
    """
    print("\n=== 任务4：广播机制应用 ===")
    
    # TODO: 在这里完成你的代码
    np.random.seed(42)
    
    # 1. 创建成绩矩阵
    scores = None          # 5x3矩阵，成绩在70-100之间
    
    print(f"原始成绩矩阵:\n{scores}")
    
    # 2. 科目权重
    weights = np.array([0.3, 0.4, 0.3])
    
    # 3. 计算加权平均分
    weighted_scores = None # scores * weights
    weighted_avg = None    # 每个学生的加权平均分
    
    # 4. 标准化成绩
    subject_means = None   # 每科目的平均分
    subject_stds = None    # 每科目的标准差
    normalized_scores = None # 标准化后的成绩
    
    # 5. 添加奖励分
    bonus_points = np.array([2, 1, 3, 0, 1])
    scores_with_bonus = None # 添加奖励分后的成绩
    
    # 打印结果
    print(f"\n科目权重: {weights}")
    print(f"加权成绩矩阵:\n{weighted_scores}")
    print(f"加权平均分: {weighted_avg}")
    
    print(f"\n标准化前各科均值: {subject_means}")
    print(f"标准化前各科标准差: {subject_stds}")
    print(f"标准化后成绩:\n{normalized_scores}")
    
    print(f"\n奖励分: {bonus_points}")
    print(f"添加奖励分后:\n{scores_with_bonus}")
    
    return {
        'original_scores': scores,
        'weights': weights,
        'weighted_scores': weighted_scores,
        'weighted_avg': weighted_avg,
        'normalized_scores': normalized_scores,
        'scores_with_bonus': scores_with_bonus
    }


def bonus_task_data_analysis():
    """
    挑战任务：综合数据分析
    
    要求：
    模拟一个股票价格分析场景：
    1. 生成30天的股票价格数据（随机游走）
    2. 计算日收益率
    3. 计算5日和10日移动平均线
    4. 计算价格的波动率（标准差）
    5. 找出价格的支撑位和阻力位（最低和最高的10%分位数）
    6. 计算最大回撤
    
    返回：股票分析结果
    """
    print("\n=== 挑战任务：股票价格分析 ===")
    
    # TODO: 在这里完成你的代码
    np.random.seed(42)
    
    # 1. 生成股票价格数据
    initial_price = 100
    days = 30
    daily_returns = None   # 生成日收益率（正态分布，均值0.001，标准差0.02）
    prices = None          # 计算累积价格
    
    print(f"股票价格（前10天）: {prices[:10] if prices is not None else None}")
    
    # 2. 计算日收益率
    returns = None         # (prices[1:] - prices[:-1]) / prices[:-1]
    
    # 3. 计算移动平均线
    ma_5 = None           # 5日移动平均
    ma_10 = None          # 10日移动平均
    
    # 4. 计算波动率
    volatility = None     # 价格标准差
    return_volatility = None # 收益率标准差
    
    # 5. 支撑位和阻力位
    support_level = None  # 10%分位数
    resistance_level = None # 90%分位数
    
    # 6. 最大回撤
    peak_prices = None    # 累积最高价
    drawdowns = None      # 回撤
    max_drawdown = None   # 最大回撤
    
    # 打印结果
    print(f"\n价格统计:")
    print(f"起始价格: {initial_price}")
    print(f"最终价格: {prices[-1] if prices is not None else None:.2f}")
    print(f"最高价: {np.max(prices) if prices is not None else None:.2f}")
    print(f"最低价: {np.min(prices) if prices is not None else None:.2f}")
    
    print(f"\n技术指标:")
    print(f"5日均线（最后5天）: {ma_5[-5:] if ma_5 is not None else None}")
    print(f"10日均线（最后5天）: {ma_10[-5:] if ma_10 is not None else None}")
    print(f"价格波动率: {volatility:.2f}")
    print(f"收益率波动率: {return_volatility:.4f}")
    
    print(f"\n风险指标:")
    print(f"支撑位: {support_level:.2f}")
    print(f"阻力位: {resistance_level:.2f}")
    print(f"最大回撤: {max_drawdown:.2%}")
    
    return {
        'prices': prices,
        'returns': returns,
        'ma_5': ma_5,
        'ma_10': ma_10,
        'volatility': volatility,
        'support_level': support_level,
        'resistance_level': resistance_level,
        'max_drawdown': max_drawdown
    }


def main():
    """
    主函数：运行所有练习任务
    """
    print("Session12 练习题2：NumPy数学运算和统计分析")
    print("=" * 60)
    
    # 运行所有任务
    task1_result = task1_mathematical_operations()
    task2_result = task2_statistical_analysis()
    task3_result = task3_linear_algebra()
    task4_result = task4_broadcasting_applications()
    bonus_result = bonus_task_data_analysis()
    
    print("\n=== 练习完成 ===")
    print("请检查你的输出结果是否正确！")
    print("如果遇到问题，请参考solutions目录中的答案。")


if __name__ == "__main__":
    main()