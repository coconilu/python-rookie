#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NumPy统计分析示例

本文件演示NumPy的统计分析功能，包括：
- 描述性统计
- 分布分析
- 相关性分析
- 假设检验基础

作者: Python教程团队
创建日期: 2024-12-19
"""

import numpy as np


def descriptive_statistics_examples():
    """
    演示描述性统计
    """
    print("=== 描述性统计示例 ===")
    
    # 生成示例数据
    np.random.seed(42)
    data = np.random.normal(100, 15, 1000)  # 均值100，标准差15的正态分布
    
    print(f"数据样本（前10个）: {data[:10]}")
    print(f"数据大小: {len(data)}")
    
    # 集中趋势
    print("\n1. 集中趋势:")
    print(f"平均值 (mean): {np.mean(data):.2f}")
    print(f"中位数 (median): {np.median(data):.2f}")
    
    # 计算众数（最频繁出现的值）
    unique, counts = np.unique(np.round(data), return_counts=True)
    mode_index = np.argmax(counts)
    mode = unique[mode_index]
    print(f"众数 (mode): {mode:.2f}")
    
    # 离散程度
    print("\n2. 离散程度:")
    print(f"标准差 (std): {np.std(data):.2f}")
    print(f"方差 (var): {np.var(data):.2f}")
    print(f"极差 (range): {np.max(data) - np.min(data):.2f}")
    print(f"最小值 (min): {np.min(data):.2f}")
    print(f"最大值 (max): {np.max(data):.2f}")
    
    # 分位数
    print("\n3. 分位数:")
    percentiles = [25, 50, 75, 90, 95, 99]
    for p in percentiles:
        value = np.percentile(data, p)
        print(f"{p}%分位数: {value:.2f}")
    
    # 四分位距
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    print(f"四分位距 (IQR): {iqr:.2f}")
    
    # 偏度和峰度（需要手动计算）
    print("\n4. 形状统计:")
    mean = np.mean(data)
    std = np.std(data)
    
    # 偏度 (skewness)
    skewness = np.mean(((data - mean) / std) ** 3)
    print(f"偏度 (skewness): {skewness:.3f}")
    
    # 峰度 (kurtosis)
    kurtosis = np.mean(((data - mean) / std) ** 4) - 3
    print(f"峰度 (kurtosis): {kurtosis:.3f}")


def distribution_analysis_examples():
    """
    演示分布分析
    """
    print("\n=== 分布分析示例 ===")
    
    # 生成不同分布的数据
    np.random.seed(42)
    
    # 正态分布
    normal_data = np.random.normal(0, 1, 1000)
    print("1. 正态分布数据:")
    print(f"均值: {np.mean(normal_data):.3f}")
    print(f"标准差: {np.std(normal_data):.3f}")
    
    # 均匀分布
    uniform_data = np.random.uniform(0, 10, 1000)
    print("\n2. 均匀分布数据:")
    print(f"最小值: {np.min(uniform_data):.3f}")
    print(f"最大值: {np.max(uniform_data):.3f}")
    print(f"均值: {np.mean(uniform_data):.3f}")
    
    # 指数分布
    exponential_data = np.random.exponential(2, 1000)
    print("\n3. 指数分布数据:")
    print(f"均值: {np.mean(exponential_data):.3f}")
    print(f"标准差: {np.std(exponential_data):.3f}")
    
    # 泊松分布
    poisson_data = np.random.poisson(3, 1000)
    print("\n4. 泊松分布数据:")
    print(f"均值: {np.mean(poisson_data):.3f}")
    print(f"方差: {np.var(poisson_data):.3f}")
    
    # 直方图分析
    print("\n5. 直方图分析:")
    hist, bins = np.histogram(normal_data, bins=20)
    print(f"直方图区间数: {len(bins)-1}")
    print(f"最高频率: {np.max(hist)}")
    print(f"最高频率区间: [{bins[np.argmax(hist)]:.2f}, {bins[np.argmax(hist)+1]:.2f}]")


def correlation_analysis_examples():
    """
    演示相关性分析
    """
    print("\n=== 相关性分析示例 ===")
    
    # 生成相关数据
    np.random.seed(42)
    n = 100
    
    # 强正相关
    x1 = np.random.normal(0, 1, n)
    y1 = 2 * x1 + np.random.normal(0, 0.5, n)
    
    # 负相关
    x2 = np.random.normal(0, 1, n)
    y2 = -1.5 * x2 + np.random.normal(0, 0.8, n)
    
    # 无相关
    x3 = np.random.normal(0, 1, n)
    y3 = np.random.normal(0, 1, n)
    
    print("1. 相关系数计算:")
    
    # 计算相关系数
    corr1 = np.corrcoef(x1, y1)[0, 1]
    corr2 = np.corrcoef(x2, y2)[0, 1]
    corr3 = np.corrcoef(x3, y3)[0, 1]
    
    print(f"强正相关数据相关系数: {corr1:.3f}")
    print(f"负相关数据相关系数: {corr2:.3f}")
    print(f"无相关数据相关系数: {corr3:.3f}")
    
    # 多变量相关矩阵
    print("\n2. 多变量相关矩阵:")
    data_matrix = np.column_stack([x1, y1, x2, y2, x3, y3])
    corr_matrix = np.corrcoef(data_matrix.T)
    
    print("相关矩阵:")
    variable_names = ['x1', 'y1', 'x2', 'y2', 'x3', 'y3']
    print("\t" + "\t".join(variable_names))
    for i, name in enumerate(variable_names):
        row = "\t".join([f"{corr_matrix[i, j]:.3f}" for j in range(len(variable_names))])
        print(f"{name}\t{row}")
    
    # 协方差矩阵
    print("\n3. 协方差矩阵:")
    cov_matrix = np.cov(data_matrix.T)
    print("协方差矩阵对角线（方差）:")
    for i, name in enumerate(variable_names):
        print(f"{name}的方差: {cov_matrix[i, i]:.3f}")


def time_series_analysis_examples():
    """
    演示时间序列分析基础
    """
    print("\n=== 时间序列分析示例 ===")
    
    # 生成时间序列数据
    np.random.seed(42)
    n = 100
    t = np.arange(n)
    
    # 趋势 + 季节性 + 噪声
    trend = 0.5 * t
    seasonal = 10 * np.sin(2 * np.pi * t / 12)
    noise = np.random.normal(0, 2, n)
    ts = trend + seasonal + noise + 50
    
    print(f"时间序列长度: {len(ts)}")
    print(f"时间序列前10个值: {ts[:10]}")
    
    # 基本统计
    print("\n1. 基本统计:")
    print(f"均值: {np.mean(ts):.2f}")
    print(f"标准差: {np.std(ts):.2f}")
    print(f"最小值: {np.min(ts):.2f}")
    print(f"最大值: {np.max(ts):.2f}")
    
    # 移动平均
    print("\n2. 移动平均:")
    window_sizes = [3, 5, 10]
    for window in window_sizes:
        ma = moving_average(ts, window)
        print(f"{window}期移动平均（最后5个值）: {ma[-5:]}")
    
    # 差分
    print("\n3. 差分分析:")
    diff1 = np.diff(ts, n=1)
    diff2 = np.diff(ts, n=2)
    
    print(f"一阶差分均值: {np.mean(diff1):.3f}")
    print(f"一阶差分标准差: {np.std(diff1):.3f}")
    print(f"二阶差分均值: {np.mean(diff2):.3f}")
    print(f"二阶差分标准差: {np.std(diff2):.3f}")
    
    # 自相关（简单版本）
    print("\n4. 自相关分析:")
    lags = [1, 2, 3, 5, 10]
    for lag in lags:
        if lag < len(ts):
            autocorr = np.corrcoef(ts[:-lag], ts[lag:])[0, 1]
            print(f"滞后{lag}期自相关系数: {autocorr:.3f}")


def moving_average(data, window):
    """
    计算移动平均
    
    Args:
        data: 数据数组
        window: 窗口大小
        
    Returns:
        移动平均数组
    """
    return np.convolve(data, np.ones(window)/window, mode='valid')


def outlier_detection_examples():
    """
    演示异常值检测
    """
    print("\n=== 异常值检测示例 ===")
    
    # 生成包含异常值的数据
    np.random.seed(42)
    normal_data = np.random.normal(50, 10, 95)
    outliers = np.array([100, 120, 5, -10, 150])  # 人工添加异常值
    data = np.concatenate([normal_data, outliers])
    np.random.shuffle(data)
    
    print(f"数据大小: {len(data)}")
    print(f"数据范围: [{np.min(data):.1f}, {np.max(data):.1f}]")
    
    # 方法1：Z-score方法
    print("\n1. Z-score方法:")
    z_scores = np.abs((data - np.mean(data)) / np.std(data))
    z_threshold = 3
    z_outliers = data[z_scores > z_threshold]
    print(f"Z-score阈值: {z_threshold}")
    print(f"检测到的异常值: {z_outliers}")
    print(f"异常值数量: {len(z_outliers)}")
    
    # 方法2：IQR方法
    print("\n2. IQR方法:")
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    iqr_outliers = data[(data < lower_bound) | (data > upper_bound)]
    print(f"IQR范围: [{lower_bound:.1f}, {upper_bound:.1f}]")
    print(f"检测到的异常值: {iqr_outliers}")
    print(f"异常值数量: {len(iqr_outliers)}")
    
    # 方法3：百分位数方法
    print("\n3. 百分位数方法:")
    p1 = np.percentile(data, 1)
    p99 = np.percentile(data, 99)
    percentile_outliers = data[(data < p1) | (data > p99)]
    print(f"1%-99%范围: [{p1:.1f}, {p99:.1f}]")
    print(f"检测到的异常值: {percentile_outliers}")
    print(f"异常值数量: {len(percentile_outliers)}")


def hypothesis_testing_examples():
    """
    演示假设检验基础
    """
    print("\n=== 假设检验基础示例 ===")
    
    # 生成两组样本数据
    np.random.seed(42)
    sample1 = np.random.normal(100, 15, 50)  # 组1：均值100
    sample2 = np.random.normal(105, 15, 50)  # 组2：均值105
    
    print("1. 样本描述:")
    print(f"样本1均值: {np.mean(sample1):.2f}, 标准差: {np.std(sample1):.2f}")
    print(f"样本2均值: {np.mean(sample2):.2f}, 标准差: {np.std(sample2):.2f}")
    
    # 单样本t检验（手动计算）
    print("\n2. 单样本t检验:")
    population_mean = 100
    sample_mean = np.mean(sample1)
    sample_std = np.std(sample1, ddof=1)  # 样本标准差
    n = len(sample1)
    
    t_statistic = (sample_mean - population_mean) / (sample_std / np.sqrt(n))
    print(f"t统计量: {t_statistic:.3f}")
    print(f"自由度: {n-1}")
    
    # 双样本t检验（手动计算）
    print("\n3. 双样本t检验:")
    mean1, mean2 = np.mean(sample1), np.mean(sample2)
    std1, std2 = np.std(sample1, ddof=1), np.std(sample2, ddof=1)
    n1, n2 = len(sample1), len(sample2)
    
    # 合并标准差
    pooled_std = np.sqrt(((n1-1)*std1**2 + (n2-1)*std2**2) / (n1+n2-2))
    t_statistic_2sample = (mean1 - mean2) / (pooled_std * np.sqrt(1/n1 + 1/n2))
    
    print(f"样本1均值: {mean1:.3f}")
    print(f"样本2均值: {mean2:.3f}")
    print(f"均值差: {mean1 - mean2:.3f}")
    print(f"t统计量: {t_statistic_2sample:.3f}")
    print(f"自由度: {n1+n2-2}")
    
    # 方差齐性检验（F检验）
    print("\n4. 方差齐性检验:")
    f_statistic = max(std1**2, std2**2) / min(std1**2, std2**2)
    print(f"F统计量: {f_statistic:.3f}")
    print(f"自由度: ({n1-1}, {n2-1})")


def bootstrap_examples():
    """
    演示自助法（Bootstrap）
    """
    print("\n=== 自助法示例 ===")
    
    # 原始样本
    np.random.seed(42)
    original_sample = np.random.normal(100, 15, 30)
    
    print(f"原始样本大小: {len(original_sample)}")
    print(f"原始样本均值: {np.mean(original_sample):.2f}")
    print(f"原始样本标准差: {np.std(original_sample):.2f}")
    
    # Bootstrap重采样
    n_bootstrap = 1000
    bootstrap_means = []
    
    for i in range(n_bootstrap):
        # 有放回抽样
        bootstrap_sample = np.random.choice(original_sample, 
                                          size=len(original_sample), 
                                          replace=True)
        bootstrap_means.append(np.mean(bootstrap_sample))
    
    bootstrap_means = np.array(bootstrap_means)
    
    print(f"\nBootstrap结果:")
    print(f"Bootstrap次数: {n_bootstrap}")
    print(f"Bootstrap均值的均值: {np.mean(bootstrap_means):.2f}")
    print(f"Bootstrap均值的标准差: {np.std(bootstrap_means):.2f}")
    
    # 置信区间
    confidence_level = 95
    alpha = (100 - confidence_level) / 2
    lower_ci = np.percentile(bootstrap_means, alpha)
    upper_ci = np.percentile(bootstrap_means, 100 - alpha)
    
    print(f"{confidence_level}%置信区间: [{lower_ci:.2f}, {upper_ci:.2f}]")


def main():
    """
    主函数：运行所有示例
    """
    print("NumPy统计分析示例")
    print("=" * 50)
    
    descriptive_statistics_examples()
    distribution_analysis_examples()
    correlation_analysis_examples()
    time_series_analysis_examples()
    outlier_detection_examples()
    hypothesis_testing_examples()
    bootstrap_examples()
    
    print("\n示例演示完成！")


if __name__ == "__main__":
    main()