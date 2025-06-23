#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session12 练习题2解答：NumPy数学运算和统计分析

本文件包含练习题2的完整解答，展示了NumPy在数学运算、
统计分析、线性代数和广播机制方面的强大功能。

作者: Python教程团队
创建日期: 2024-12-19
"""

import numpy as np
from scipy import stats  # 用于更高级的统计功能


def task1_basic_math_operations():
    """
    任务1：基础数学运算 - 完整解答
    """
    print("=== 任务1：基础数学运算 - 解答 ===")
    
    # 创建测试数组
    np.random.seed(42)
    array_a = np.random.randint(1, 10, (3, 4))
    array_b = np.random.randint(1, 10, (3, 4))
    
    print(f"数组A:\n{array_a}")
    print(f"数组B:\n{array_b}")
    
    # 1. 基本算术运算
    addition = array_a + array_b
    subtraction = array_a - array_b
    multiplication = array_a * array_b
    division = array_a / array_b
    power = array_a ** 2
    modulo = array_a % 3
    
    print(f"\n1. 基本算术运算:")
    print(f"   加法 A+B:\n{addition}")
    print(f"   减法 A-B:\n{subtraction}")
    print(f"   乘法 A*B:\n{multiplication}")
    print(f"   除法 A/B:\n{division}")
    print(f"   平方 A²:\n{power}")
    print(f"   取模 A%3:\n{modulo}")
    
    # 2. 数学函数
    sqrt_a = np.sqrt(array_a)
    exp_a = np.exp(array_a)
    log_a = np.log(array_a)
    sin_a = np.sin(array_a)
    cos_a = np.cos(array_a)
    
    print(f"\n2. 数学函数:")
    print(f"   平方根:\n{sqrt_a}")
    print(f"   指数函数:\n{exp_a}")
    print(f"   自然对数:\n{log_a}")
    print(f"   正弦值:\n{sin_a}")
    print(f"   余弦值:\n{cos_a}")
    
    # 3. 舍入函数
    float_array = np.array([[1.2, 2.7, 3.1], [4.8, 5.5, 6.9]])
    rounded = np.round(float_array)
    floor_val = np.floor(float_array)
    ceil_val = np.ceil(float_array)
    
    print(f"\n3. 舍入函数:")
    print(f"   原数组:\n{float_array}")
    print(f"   四舍五入:\n{rounded}")
    print(f"   向下取整:\n{floor_val}")
    print(f"   向上取整:\n{ceil_val}")
    
    # 4. 比较运算
    greater = array_a > array_b
    equal = array_a == array_b
    greater_equal = array_a >= 5
    
    print(f"\n4. 比较运算:")
    print(f"   A > B:\n{greater}")
    print(f"   A == B:\n{equal}")
    print(f"   A >= 5:\n{greater_equal}")
    
    return {
        'array_a': array_a,
        'array_b': array_b,
        'addition': addition,
        'subtraction': subtraction,
        'multiplication': multiplication,
        'division': division,
        'sqrt_a': sqrt_a,
        'exp_a': exp_a,
        'log_a': log_a,
        'rounded': rounded,
        'greater': greater
    }


def task2_statistical_analysis():
    """
    任务2：统计分析 - 完整解答
    """
    print("\n=== 任务2：统计分析 - 解答 ===")
    
    # 创建测试数据
    np.random.seed(42)
    data = np.random.normal(100, 15, (50, 4))  # 50个样本，4个特征
    
    print(f"数据形状: {data.shape}")
    print(f"前5行数据:\n{data[:5]}")
    
    # 1. 基本统计量
    mean_val = np.mean(data, axis=0)
    median_val = np.median(data, axis=0)
    std_val = np.std(data, axis=0)
    var_val = np.var(data, axis=0)
    min_val = np.min(data, axis=0)
    max_val = np.max(data, axis=0)
    
    print(f"\n1. 基本统计量 (按列):")
    print(f"   均值: {mean_val}")
    print(f"   中位数: {median_val}")
    print(f"   标准差: {std_val}")
    print(f"   方差: {var_val}")
    print(f"   最小值: {min_val}")
    print(f"   最大值: {max_val}")
    
    # 2. 百分位数
    percentiles = [25, 50, 75, 90, 95]
    percentile_values = np.percentile(data, percentiles, axis=0)
    
    print(f"\n2. 百分位数:")
    for i, p in enumerate(percentiles):
        print(f"   {p}%分位数: {percentile_values[i]}")
    
    # 3. 四分位距 (IQR)
    q1 = np.percentile(data, 25, axis=0)
    q3 = np.percentile(data, 75, axis=0)
    iqr = q3 - q1
    
    print(f"\n3. 四分位距分析:")
    print(f"   Q1 (25%): {q1}")
    print(f"   Q3 (75%): {q3}")
    print(f"   IQR: {iqr}")
    
    # 4. 异常值检测 (IQR方法)
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    outliers_mask = (data < lower_bound) | (data > upper_bound)
    outliers_count = np.sum(outliers_mask, axis=0)
    
    print(f"\n4. 异常值检测 (IQR方法):")
    print(f"   下界: {lower_bound}")
    print(f"   上界: {upper_bound}")
    print(f"   各列异常值数量: {outliers_count}")
    
    # 5. Z-score异常值检测
    z_scores = np.abs((data - mean_val) / std_val)
    z_outliers = z_scores > 2.5  # Z-score > 2.5认为是异常值
    z_outliers_count = np.sum(z_outliers, axis=0)
    
    print(f"\n5. Z-score异常值检测 (|Z| > 2.5):")
    print(f"   各列异常值数量: {z_outliers_count}")
    
    # 6. 相关性分析
    correlation_matrix = np.corrcoef(data.T)  # 转置后计算列间相关性
    
    print(f"\n6. 相关性矩阵:\n{correlation_matrix}")
    
    # 7. 累积统计
    cumsum_data = np.cumsum(data, axis=0)
    cumprod_data = np.cumprod(data[:5], axis=0)  # 只计算前5行避免数值过大
    
    print(f"\n7. 累积统计:")
    print(f"   累积和最后一行: {cumsum_data[-1]}")
    print(f"   累积乘积(前5行)最后一行: {cumprod_data[-1]}")
    
    # 8. 排序和排名
    sorted_data = np.sort(data, axis=0)
    argsort_indices = np.argsort(data, axis=0)
    
    print(f"\n8. 排序分析:")
    print(f"   每列最小值索引: {argsort_indices[0]}")
    print(f"   每列最大值索引: {argsort_indices[-1]}")
    
    return {
        'data': data,
        'mean_val': mean_val,
        'median_val': median_val,
        'std_val': std_val,
        'percentile_values': percentile_values,
        'iqr': iqr,
        'outliers_count': outliers_count,
        'z_outliers_count': z_outliers_count,
        'correlation_matrix': correlation_matrix,
        'sorted_data': sorted_data
    }


def task3_linear_algebra():
    """
    任务3：线性代数运算 - 完整解答
    """
    print("\n=== 任务3：线性代数运算 - 解答 ===")
    
    # 创建测试矩阵
    np.random.seed(42)
    matrix_a = np.random.randint(1, 10, (3, 3))
    matrix_b = np.random.randint(1, 10, (3, 3))
    vector = np.random.randint(1, 10, 3)
    
    print(f"矩阵A:\n{matrix_a}")
    print(f"矩阵B:\n{matrix_b}")
    print(f"向量: {vector}")
    
    # 1. 矩阵乘法
    matrix_mult = np.dot(matrix_a, matrix_b)
    matrix_mult_operator = matrix_a @ matrix_b  # Python 3.5+的矩阵乘法运算符
    
    print(f"\n1. 矩阵乘法:")
    print(f"   A × B (使用np.dot):\n{matrix_mult}")
    print(f"   A @ B (使用@运算符):\n{matrix_mult_operator}")
    
    # 2. 点积和叉积
    vector_b = np.array([2, 3, 4])
    dot_product = np.dot(vector, vector_b)
    cross_product = np.cross(vector, vector_b)
    
    print(f"\n2. 向量运算:")
    print(f"   向量A: {vector}")
    print(f"   向量B: {vector_b}")
    print(f"   点积: {dot_product}")
    print(f"   叉积: {cross_product}")
    
    # 3. 矩阵转置
    transpose_a = matrix_a.T
    transpose_b = np.transpose(matrix_a)
    
    print(f"\n3. 矩阵转置:")
    print(f"   A的转置 (使用.T):\n{transpose_a}")
    print(f"   A的转置 (使用np.transpose):\n{transpose_b}")
    
    # 4. 行列式
    det_a = np.linalg.det(matrix_a)
    det_b = np.linalg.det(matrix_b)
    
    print(f"\n4. 行列式:")
    print(f"   det(A): {det_a:.4f}")
    print(f"   det(B): {det_b:.4f}")
    
    # 5. 矩阵的逆
    try:
        inv_a = np.linalg.inv(matrix_a)
        print(f"\n5. 矩阵的逆:")
        print(f"   A的逆矩阵:\n{inv_a}")
        
        # 验证 A × A^(-1) = I
        identity_check = np.dot(matrix_a, inv_a)
        print(f"   验证 A × A^(-1):\n{identity_check}")
        
    except np.linalg.LinAlgError:
        print(f"\n5. 矩阵A不可逆（奇异矩阵）")
    
    # 6. 特征值和特征向量
    eigenvalues, eigenvectors = np.linalg.eig(matrix_a)
    
    print(f"\n6. 特征值和特征向量:")
    print(f"   特征值: {eigenvalues}")
    print(f"   特征向量:\n{eigenvectors}")
    
    # 7. 矩阵的秩
    rank_a = np.linalg.matrix_rank(matrix_a)
    rank_b = np.linalg.matrix_rank(matrix_b)
    
    print(f"\n7. 矩阵的秩:")
    print(f"   rank(A): {rank_a}")
    print(f"   rank(B): {rank_b}")
    
    # 8. 解线性方程组 Ax = b
    b_vector = np.array([10, 20, 30])
    try:
        solution = np.linalg.solve(matrix_a, b_vector)
        print(f"\n8. 线性方程组 Ax = b:")
        print(f"   系数矩阵A:\n{matrix_a}")
        print(f"   常数向量b: {b_vector}")
        print(f"   解向量x: {solution}")
        
        # 验证解
        verification = np.dot(matrix_a, solution)
        print(f"   验证 Ax: {verification}")
        
    except np.linalg.LinAlgError:
        print(f"\n8. 线性方程组无唯一解")
    
    # 9. 奇异值分解 (SVD)
    U, s, Vt = np.linalg.svd(matrix_a)
    
    print(f"\n9. 奇异值分解:")
    print(f"   U矩阵形状: {U.shape}")
    print(f"   奇异值: {s}")
    print(f"   V^T矩阵形状: {Vt.shape}")
    
    # 10. 矩阵范数
    frobenius_norm = np.linalg.norm(matrix_a, 'fro')
    spectral_norm = np.linalg.norm(matrix_a, 2)
    
    print(f"\n10. 矩阵范数:")
    print(f"    Frobenius范数: {frobenius_norm:.4f}")
    print(f"    谱范数: {spectral_norm:.4f}")
    
    return {
        'matrix_a': matrix_a,
        'matrix_b': matrix_b,
        'matrix_mult': matrix_mult,
        'dot_product': dot_product,
        'cross_product': cross_product,
        'det_a': det_a,
        'eigenvalues': eigenvalues,
        'eigenvectors': eigenvectors,
        'rank_a': rank_a
    }


def task4_broadcasting_applications():
    """
    任务4：广播机制应用 - 完整解答
    """
    print("\n=== 任务4：广播机制应用 - 解答 ===")
    
    # 1. 基本广播示例
    array_2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    scalar = 10
    vector_1d = np.array([1, 2, 3])
    
    print(f"1. 基本广播:")
    print(f"   原2D数组:\n{array_2d}")
    print(f"   标量: {scalar}")
    print(f"   1D向量: {vector_1d}")
    
    # 标量广播
    scalar_broadcast = array_2d + scalar
    print(f"   2D数组 + 标量:\n{scalar_broadcast}")
    
    # 向量广播
    vector_broadcast = array_2d + vector_1d
    print(f"   2D数组 + 1D向量:\n{vector_broadcast}")
    
    # 2. 加权平均计算
    np.random.seed(42)
    scores = np.random.randint(60, 100, (5, 4))  # 5个学生，4门课
    weights = np.array([0.3, 0.3, 0.2, 0.2])    # 课程权重
    
    print(f"\n2. 加权平均计算:")
    print(f"   学生成绩:\n{scores}")
    print(f"   课程权重: {weights}")
    
    # 使用广播计算加权平均
    weighted_scores = scores * weights  # 广播乘法
    weighted_average = np.sum(weighted_scores, axis=1)
    
    print(f"   加权成绩:\n{weighted_scores}")
    print(f"   加权平均分: {weighted_average}")
    
    # 3. 数据标准化
    data = np.random.normal(50, 10, (100, 3))
    
    print(f"\n3. 数据标准化:")
    print(f"   原数据形状: {data.shape}")
    print(f"   原数据前5行:\n{data[:5]}")
    
    # Z-score标准化
    mean_vals = np.mean(data, axis=0)
    std_vals = np.std(data, axis=0)
    standardized_data = (data - mean_vals) / std_vals  # 广播运算
    
    print(f"   各列均值: {mean_vals}")
    print(f"   各列标准差: {std_vals}")
    print(f"   标准化后前5行:\n{standardized_data[:5]}")
    print(f"   标准化后均值: {np.mean(standardized_data, axis=0)}")
    print(f"   标准化后标准差: {np.std(standardized_data, axis=0)}")
    
    # 4. 添加奖励分数
    base_scores = np.array([[85, 90, 78], [92, 88, 95], [76, 82, 89]])
    bonus_points = np.array([5, 3, 2])  # 每科目的奖励分
    
    print(f"\n4. 添加奖励分数:")
    print(f"   基础分数:\n{base_scores}")
    print(f"   奖励分数: {bonus_points}")
    
    final_scores = base_scores + bonus_points  # 广播加法
    print(f"   最终分数:\n{final_scores}")
    
    # 5. 距离计算
    points_a = np.array([[1, 2], [3, 4], [5, 6]])
    points_b = np.array([[0, 0], [2, 2]])
    
    print(f"\n5. 距离计算:")
    print(f"   点集A:\n{points_a}")
    print(f"   点集B:\n{points_b}")
    
    # 计算每个A中的点到每个B中的点的距离
    # 使用广播计算欧几里得距离
    diff = points_a[:, np.newaxis, :] - points_b[np.newaxis, :, :]
    distances = np.sqrt(np.sum(diff**2, axis=2))
    
    print(f"   距离矩阵:\n{distances}")
    
    # 6. 图像处理示例（RGB调整）
    # 模拟一个小的RGB图像
    image = np.random.randint(0, 256, (4, 4, 3), dtype=np.uint8)
    rgb_adjustment = np.array([1.2, 0.8, 1.1])  # R, G, B调整因子
    
    print(f"\n6. 图像RGB调整:")
    print(f"   原图像形状: {image.shape}")
    print(f"   RGB调整因子: {rgb_adjustment}")
    
    # 使用广播调整RGB值
    adjusted_image = np.clip(image * rgb_adjustment, 0, 255).astype(np.uint8)
    
    print(f"   原图像第一个像素: {image[0, 0]}")
    print(f"   调整后第一个像素: {adjusted_image[0, 0]}")
    
    return {
        'array_2d': array_2d,
        'scalar_broadcast': scalar_broadcast,
        'vector_broadcast': vector_broadcast,
        'weighted_average': weighted_average,
        'standardized_data': standardized_data,
        'final_scores': final_scores,
        'distances': distances,
        'adjusted_image': adjusted_image
    }


def bonus_stock_analysis():
    """
    奖励任务：股票价格分析 - 完整解答
    """
    print("\n=== 奖励任务：股票价格分析 - 解答 ===")
    
    # 1. 生成模拟股票价格数据
    np.random.seed(42)
    days = 100
    initial_price = 100
    
    # 生成价格变化（随机游走）
    daily_returns = np.random.normal(0.001, 0.02, days)  # 日收益率
    prices = np.zeros(days)
    prices[0] = initial_price
    
    for i in range(1, days):
        prices[i] = prices[i-1] * (1 + daily_returns[i])
    
    print(f"1. 股票价格数据:")
    print(f"   交易天数: {days}")
    print(f"   起始价格: {initial_price}")
    print(f"   结束价格: {prices[-1]:.2f}")
    print(f"   价格范围: [{np.min(prices):.2f}, {np.max(prices):.2f}]")
    
    # 2. 计算日收益率
    calculated_returns = np.zeros_like(prices)
    calculated_returns[1:] = (prices[1:] - prices[:-1]) / prices[:-1]
    
    print(f"\n2. 收益率分析:")
    print(f"   平均日收益率: {np.mean(calculated_returns[1:]):.4f}")
    print(f"   收益率标准差: {np.std(calculated_returns[1:]):.4f}")
    print(f"   最大单日涨幅: {np.max(calculated_returns[1:]):.4f}")
    print(f"   最大单日跌幅: {np.min(calculated_returns[1:]):.4f}")
    
    # 3. 计算移动平均线
    def moving_average(data, window):
        """计算移动平均线"""
        ma = np.zeros_like(data)
        for i in range(len(data)):
            if i < window:
                ma[i] = np.mean(data[:i+1])
            else:
                ma[i] = np.mean(data[i-window+1:i+1])
        return ma
    
    ma_5 = moving_average(prices, 5)
    ma_20 = moving_average(prices, 20)
    ma_50 = moving_average(prices, 50)
    
    print(f"\n3. 移动平均线:")
    print(f"   5日均线最新值: {ma_5[-1]:.2f}")
    print(f"   20日均线最新值: {ma_20[-1]:.2f}")
    print(f"   50日均线最新值: {ma_50[-1]:.2f}")
    
    # 4. 计算波动率（年化）
    volatility_daily = np.std(calculated_returns[1:])
    volatility_annual = volatility_daily * np.sqrt(252)  # 假设252个交易日
    
    print(f"\n4. 波动率分析:")
    print(f"   日波动率: {volatility_daily:.4f}")
    print(f"   年化波动率: {volatility_annual:.4f} ({volatility_annual*100:.2f}%)")
    
    # 5. 支撑位和阻力位分析
    # 使用滚动窗口找局部最小值和最大值
    window = 10
    support_levels = []
    resistance_levels = []
    
    for i in range(window, len(prices) - window):
        window_prices = prices[i-window:i+window+1]
        if prices[i] == np.min(window_prices):
            support_levels.append(prices[i])
        if prices[i] == np.max(window_prices):
            resistance_levels.append(prices[i])
    
    print(f"\n5. 支撑位和阻力位:")
    if support_levels:
        print(f"   主要支撑位: {np.mean(support_levels):.2f}")
        print(f"   支撑位数量: {len(support_levels)}")
    if resistance_levels:
        print(f"   主要阻力位: {np.mean(resistance_levels):.2f}")
        print(f"   阻力位数量: {len(resistance_levels)}")
    
    # 6. 最大回撤分析
    running_max = np.maximum.accumulate(prices)
    drawdown = (running_max - prices) / running_max
    max_drawdown = np.max(drawdown)
    max_drawdown_idx = np.argmax(drawdown)
    
    print(f"\n6. 回撤分析:")
    print(f"   最大回撤: {max_drawdown:.4f} ({max_drawdown*100:.2f}%)")
    print(f"   最大回撤发生日: 第{max_drawdown_idx+1}天")
    print(f"   回撤时价格: {prices[max_drawdown_idx]:.2f}")
    
    # 7. 夏普比率计算
    risk_free_rate = 0.02  # 假设无风险利率2%
    excess_returns = calculated_returns[1:] - risk_free_rate/252
    sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)
    
    print(f"\n7. 风险调整收益:")
    print(f"   夏普比率: {sharpe_ratio:.4f}")
    
    # 8. 趋势分析
    # 使用线性回归分析趋势
    days_array = np.arange(len(prices))
    
    # 手动计算线性回归系数
    n = len(prices)
    sum_x = np.sum(days_array)
    sum_y = np.sum(prices)
    sum_xy = np.sum(days_array * prices)
    sum_x2 = np.sum(days_array ** 2)
    
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    intercept = (sum_y - slope * sum_x) / n
    
    trend_line = slope * days_array + intercept
    
    print(f"\n8. 趋势分析:")
    print(f"   趋势斜率: {slope:.4f}")
    print(f"   趋势方向: {'上升' if slope > 0 else '下降' if slope < 0 else '横盘'}")
    
    # 9. 技术指标 - RSI
    def calculate_rsi(prices, window=14):
        """计算相对强弱指数"""
        returns = np.diff(prices)
        gains = np.where(returns > 0, returns, 0)
        losses = np.where(returns < 0, -returns, 0)
        
        rsi = np.zeros_like(prices)
        
        for i in range(window, len(prices)):
            avg_gain = np.mean(gains[i-window:i])
            avg_loss = np.mean(losses[i-window:i])
            
            if avg_loss == 0:
                rsi[i] = 100
            else:
                rs = avg_gain / avg_loss
                rsi[i] = 100 - (100 / (1 + rs))
        
        return rsi
    
    rsi = calculate_rsi(prices)
    current_rsi = rsi[-1]
    
    print(f"\n9. 技术指标:")
    print(f"   当前RSI: {current_rsi:.2f}")
    if current_rsi > 70:
        signal = "超买"
    elif current_rsi < 30:
        signal = "超卖"
    else:
        signal = "正常"
    print(f"   RSI信号: {signal}")
    
    # 10. 投资建议
    print(f"\n10. 投资建议:")
    
    # 基于多个指标给出建议
    signals = []
    
    if slope > 0:
        signals.append("趋势向上")
    else:
        signals.append("趋势向下")
    
    if current_rsi < 30:
        signals.append("RSI超卖")
    elif current_rsi > 70:
        signals.append("RSI超买")
    
    if prices[-1] > ma_20[-1]:
        signals.append("价格在20日均线上方")
    else:
        signals.append("价格在20日均线下方")
    
    if volatility_annual > 0.3:
        signals.append("高波动率")
    
    print(f"    技术信号: {', '.join(signals)}")
    
    if slope > 0 and current_rsi < 70 and prices[-1] > ma_20[-1]:
        recommendation = "建议买入"
    elif slope < 0 and current_rsi > 30 and prices[-1] < ma_20[-1]:
        recommendation = "建议卖出"
    else:
        recommendation = "建议观望"
    
    print(f"    投资建议: {recommendation}")
    
    return {
        'prices': prices,
        'returns': calculated_returns,
        'ma_5': ma_5,
        'ma_20': ma_20,
        'ma_50': ma_50,
        'volatility_annual': volatility_annual,
        'max_drawdown': max_drawdown,
        'sharpe_ratio': sharpe_ratio,
        'slope': slope,
        'rsi': rsi,
        'recommendation': recommendation
    }


def main():
    """主函数"""
    print("Session12 练习题2完整解答：NumPy数学运算和统计分析")
    print("=" * 70)
    
    # 执行所有任务
    math_results = task1_basic_math_operations()
    stats_results = task2_statistical_analysis()
    linalg_results = task3_linear_algebra()
    broadcast_results = task4_broadcasting_applications()
    stock_results = bonus_stock_analysis()
    
    print("\n" + "=" * 70)
    print("所有任务完成！")
    print("\n学习要点总结:")
    print("1. NumPy的数学运算和函数")
    print("2. 统计分析和异常值检测")
    print("3. 线性代数运算和矩阵操作")
    print("4. 广播机制的灵活应用")
    print("5. 实际应用：股票价格技术分析")
    print("6. 金融指标计算和投资建议")
    print("=" * 70)


if __name__ == "__main__":
    main()