#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session12: 数据处理 - NumPy 演示代码

本文件演示了NumPy的核心功能和实际应用，包括：
- 数组创建和基本操作
- 数学运算和统计分析
- 股票数据分析实例

作者: Python教程团队
创建日期: 2024-12-19
最后修改: 2024-12-19
"""

import numpy as np
import time
from typing import Tuple, List


def main():
    """
    主函数：演示NumPy的各种功能
    """
    print("Session12: NumPy数据处理演示")
    print("=" * 50)
    
    # 1. 基础数组操作演示
    demo_array_basics()
    
    # 2. 数学运算演示
    demo_math_operations()
    
    # 3. 统计分析演示
    demo_statistical_analysis()
    
    # 4. 股票数据分析演示
    demo_stock_analysis()
    
    # 5. 性能对比演示
    demo_performance_comparison()
    
    print("\n演示完成！")


def demo_array_basics():
    """
    演示NumPy数组的基础操作
    """
    print("\n1. NumPy数组基础操作")
    print("-" * 30)
    
    # 创建不同类型的数组
    print("创建数组:")
    arr1d = np.array([1, 2, 3, 4, 5])
    arr2d = np.array([[1, 2, 3], [4, 5, 6]])
    zeros = np.zeros((2, 3))
    ones = np.ones((3, 2))
    arange_arr = np.arange(0, 10, 2)
    linspace_arr = np.linspace(0, 1, 5)
    
    print(f"一维数组: {arr1d}")
    print(f"二维数组:\n{arr2d}")
    print(f"零数组:\n{zeros}")
    print(f"一数组:\n{ones}")
    print(f"等差数列: {arange_arr}")
    print(f"等间距数列: {linspace_arr}")
    
    # 数组属性
    print("\n数组属性:")
    print(f"形状: {arr2d.shape}")
    print(f"维度: {arr2d.ndim}")
    print(f"大小: {arr2d.size}")
    print(f"数据类型: {arr2d.dtype}")
    
    # 索引和切片
    print("\n索引和切片:")
    print(f"第一行: {arr2d[0]}")
    print(f"第二列: {arr2d[:, 1]}")
    print(f"前三个元素: {arr1d[:3]}")
    
    # 布尔索引
    print("\n布尔索引:")
    mask = arr1d > 3
    print(f"大于3的元素: {arr1d[mask]}")


def demo_math_operations():
    """
    演示NumPy的数学运算功能
    """
    print("\n2. 数学运算演示")
    print("-" * 30)
    
    arr1 = np.array([1, 2, 3, 4])
    arr2 = np.array([5, 6, 7, 8])
    
    # 基本算术运算
    print("基本算术运算:")
    print(f"arr1: {arr1}")
    print(f"arr2: {arr2}")
    print(f"加法: {arr1 + arr2}")
    print(f"减法: {arr2 - arr1}")
    print(f"乘法: {arr1 * arr2}")
    print(f"除法: {arr2 / arr1}")
    print(f"幂运算: {arr1 ** 2}")
    
    # 数学函数
    print("\n数学函数:")
    arr = np.array([1, 4, 9, 16, 25])
    print(f"原数组: {arr}")
    print(f"平方根: {np.sqrt(arr)}")
    print(f"对数: {np.log(arr)}")
    
    # 三角函数
    angles = np.array([0, np.pi/6, np.pi/4, np.pi/3, np.pi/2])
    print(f"\n角度: {angles}")
    print(f"正弦值: {np.sin(angles)}")
    print(f"余弦值: {np.cos(angles)}")
    
    # 广播机制
    print("\n广播机制:")
    arr2d = np.array([[1, 2, 3], [4, 5, 6]])
    arr1d = np.array([10, 20, 30])
    result = arr2d + arr1d
    print(f"2D数组:\n{arr2d}")
    print(f"1D数组: {arr1d}")
    print(f"广播结果:\n{result}")


def demo_statistical_analysis():
    """
    演示NumPy的统计分析功能
    """
    print("\n3. 统计分析演示")
    print("-" * 30)
    
    # 创建示例数据
    np.random.seed(42)
    data = np.random.normal(100, 15, (5, 4))  # 正态分布数据
    
    print(f"示例数据:\n{data}")
    
    # 基本统计量
    print("\n基本统计量:")
    print(f"最小值: {np.min(data):.2f}")
    print(f"最大值: {np.max(data):.2f}")
    print(f"平均值: {np.mean(data):.2f}")
    print(f"中位数: {np.median(data):.2f}")
    print(f"标准差: {np.std(data):.2f}")
    print(f"方差: {np.var(data):.2f}")
    
    # 按轴统计
    print("\n按轴统计:")
    print(f"按行求和: {np.sum(data, axis=1)}")
    print(f"按列求和: {np.sum(data, axis=0)}")
    print(f"按列平均: {np.mean(data, axis=0)}")
    
    # 百分位数
    print("\n百分位数:")
    print(f"25%分位数: {np.percentile(data, 25):.2f}")
    print(f"50%分位数: {np.percentile(data, 50):.2f}")
    print(f"75%分位数: {np.percentile(data, 75):.2f}")


def demo_stock_analysis():
    """
    演示股票数据分析实例
    """
    print("\n4. 股票数据分析演示")
    print("-" * 30)
    
    # 生成模拟股票数据
    np.random.seed(42)
    days = 30
    initial_price = 100
    daily_returns = np.random.normal(0.001, 0.02, days)  # 日收益率
    prices = initial_price * np.cumprod(1 + daily_returns)
    
    print(f"股票价格数据（前10天）: {prices[:10]}")
    
    # 计算技术指标
    returns = calculate_returns(prices)
    sma_5 = calculate_moving_average(prices, 5)
    sma_10 = calculate_moving_average(prices, 10)
    volatility = calculate_volatility(returns)
    
    print(f"\n技术指标分析:")
    print(f"平均价格: {np.mean(prices):.2f}")
    print(f"最高价: {np.max(prices):.2f}")
    print(f"最低价: {np.min(prices):.2f}")
    print(f"价格标准差: {np.std(prices):.2f}")
    print(f"平均日收益率: {np.mean(returns)*100:.3f}%")
    print(f"收益率波动率: {volatility*100:.3f}%")
    
    # 移动平均线分析
    print(f"\n移动平均线（最后5天）:")
    print(f"5日均线: {sma_5[-5:]}")
    print(f"10日均线: {sma_10[-5:]}")
    
    # 风险指标
    max_drawdown = calculate_max_drawdown(prices)
    sharpe_ratio = calculate_sharpe_ratio(returns)
    
    print(f"\n风险指标:")
    print(f"最大回撤: {max_drawdown*100:.2f}%")
    print(f"夏普比率: {sharpe_ratio:.3f}")


def calculate_returns(prices: np.ndarray) -> np.ndarray:
    """
    计算日收益率
    
    Args:
        prices: 价格数组
        
    Returns:
        日收益率数组
    """
    return (prices[1:] - prices[:-1]) / prices[:-1]


def calculate_moving_average(prices: np.ndarray, window: int) -> np.ndarray:
    """
    计算移动平均线
    
    Args:
        prices: 价格数组
        window: 窗口大小
        
    Returns:
        移动平均线数组
    """
    return np.convolve(prices, np.ones(window)/window, mode='valid')


def calculate_volatility(returns: np.ndarray, annualize: bool = True) -> float:
    """
    计算波动率
    
    Args:
        returns: 收益率数组
        annualize: 是否年化
        
    Returns:
        波动率
    """
    vol = np.std(returns)
    if annualize:
        vol *= np.sqrt(252)  # 假设一年252个交易日
    return vol


def calculate_max_drawdown(prices: np.ndarray) -> float:
    """
    计算最大回撤
    
    Args:
        prices: 价格数组
        
    Returns:
        最大回撤比例
    """
    peak = np.maximum.accumulate(prices)
    drawdown = (prices - peak) / peak
    return np.min(drawdown)


def calculate_sharpe_ratio(returns: np.ndarray, risk_free_rate: float = 0.02) -> float:
    """
    计算夏普比率
    
    Args:
        returns: 收益率数组
        risk_free_rate: 无风险利率（年化）
        
    Returns:
        夏普比率
    """
    excess_returns = np.mean(returns) * 252 - risk_free_rate
    volatility = np.std(returns) * np.sqrt(252)
    return excess_returns / volatility if volatility != 0 else 0


def demo_performance_comparison():
    """
    演示NumPy与Python原生操作的性能对比
    """
    print("\n5. 性能对比演示")
    print("-" * 30)
    
    size = 100000
    
    # Python原生列表操作
    start_time = time.time()
    python_list = list(range(size))
    python_result = [x ** 2 for x in python_list]
    python_time = time.time() - start_time
    
    # NumPy数组操作
    start_time = time.time()
    numpy_array = np.arange(size)
    numpy_result = numpy_array ** 2
    numpy_time = time.time() - start_time
    
    print(f"数据规模: {size:,}")
    print(f"Python列表时间: {python_time:.4f}秒")
    print(f"NumPy数组时间: {numpy_time:.4f}秒")
    print(f"NumPy速度提升: {python_time/numpy_time:.1f}倍")
    
    # 内存使用对比
    import sys
    python_memory = sys.getsizeof(python_result)
    numpy_memory = numpy_result.nbytes
    
    print(f"\n内存使用对比:")
    print(f"Python列表内存: {python_memory:,}字节")
    print(f"NumPy数组内存: {numpy_memory:,}字节")
    print(f"内存节省: {(python_memory - numpy_memory) / python_memory * 100:.1f}%")


if __name__ == "__main__":
    main()