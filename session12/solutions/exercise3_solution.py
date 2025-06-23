#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session12 练习题3解答：NumPy实际应用 - 数据分析项目

本文件包含练习题3的完整解答，展示了一个完整的数据分析项目，
包括数据预处理、趋势分析、地区产品分析和预测建议。

作者: Python教程团队
创建日期: 2024-12-19
"""

import numpy as np


def generate_sales_data():
    """
    生成模拟销售数据 - 完整解答
    
    数据结构：
    - 维度：(90天, 5个产品, 4个地区)
    - 产品：['电子产品', '服装', '家居', '图书', '运动用品']
    - 地区：['北京', '上海', '广州', '深圳']
    
    返回：销售数据和相关信息
    """
    print("=== 数据生成 - 解答 ===")
    
    np.random.seed(42)
    
    # 基础参数
    days = 90
    products = ['电子产品', '服装', '家居', '图书', '运动用品']
    regions = ['北京', '上海', '广州', '深圳']
    
    # 基础销量矩阵 (产品 x 地区)
    # 不同产品在不同地区有不同的基础销量
    base_sales = np.array([
        [150, 180, 160, 170],  # 电子产品
        [120, 140, 130, 125],  # 服装
        [100, 110, 105, 115],  # 家居
        [80, 85, 75, 90],      # 图书
        [90, 95, 100, 85]      # 运动用品
    ])
    
    # 生成90天的销售数据
    sales_data = np.zeros((days, 5, 4))
    
    for day in range(days):
        for product in range(5):
            for region in range(4):
                # 基础销量 + 随机波动
                base = base_sales[product, region]
                noise = np.random.normal(0, base * 0.2)  # 20%的随机波动
                sales_data[day, product, region] = max(0, base + noise)
    
    # 添加趋势和季节性
    # 趋势：整体销量随时间增长
    trend_factor = 1 + np.linspace(0, 0.1, days)  # 90天内增长10%
    
    # 季节性：周末销量更高
    seasonal_factor = np.ones(days)
    for day in range(days):
        if day % 7 in [5, 6]:  # 周六周日
            seasonal_factor[day] = 1.3
        elif day % 7 in [0]:   # 周一
            seasonal_factor[day] = 0.8
    
    # 应用趋势和季节性
    for day in range(days):
        sales_data[day] *= trend_factor[day] * seasonal_factor[day]
    
    print(f"数据形状: {sales_data.shape}")
    print(f"产品类别: {products}")
    print(f"销售地区: {regions}")
    print(f"数据期间: {days}天")
    print(f"总销售额: {np.sum(sales_data):.2f}")
    
    return {
        'data': sales_data,
        'products': products,
        'regions': regions,
        'days': days
    }


def task1_data_preprocessing(sales_info):
    """
    任务1：数据预处理 - 完整解答
    
    要求：
    1. 检查数据的基本信息（形状、统计量）
    2. 处理异常值（使用IQR方法）
    3. 计算缺失值（模拟一些缺失数据）
    4. 数据标准化
    
    参数：
        sales_info: 销售数据信息字典
        
    返回：预处理结果
    """
    print("\n=== 任务1：数据预处理 - 解答 ===")
    
    sales_data = sales_info['data']
    products = sales_info['products']
    regions = sales_info['regions']
    
    # 1. 基本信息
    data_shape = sales_data.shape
    total_sales = np.sum(sales_data)
    mean_daily_sales = np.mean(np.sum(sales_data, axis=(1, 2)))
    std_daily_sales = np.std(np.sum(sales_data, axis=(1, 2)))
    
    print(f"1. 基本信息:")
    print(f"   数据形状: {data_shape}")
    print(f"   总销售额: {total_sales:.2f}")
    print(f"   日均销售额: {mean_daily_sales:.2f}")
    print(f"   日销售额标准差: {std_daily_sales:.2f}")
    
    # 2. 异常值检测和处理
    # 将三维数据展平为一维进行异常值检测
    flat_data = sales_data.flatten()
    q1 = np.percentile(flat_data, 25)
    q3 = np.percentile(flat_data, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    # 找出异常值
    outliers_mask = (flat_data < lower_bound) | (flat_data > upper_bound)
    outliers_count = np.sum(outliers_mask)
    
    print(f"\n2. 异常值检测:")
    print(f"   Q1: {q1:.2f}")
    print(f"   Q3: {q3:.2f}")
    print(f"   IQR: {iqr:.2f}")
    print(f"   异常值范围: (<{lower_bound:.2f} 或 >{upper_bound:.2f})")
    print(f"   异常值数量: {outliers_count}")
    print(f"   异常值比例: {outliers_count/len(flat_data)*100:.2f}%")
    
    # 处理异常值（用边界值替换）
    cleaned_data = sales_data.copy()
    cleaned_data[cleaned_data < lower_bound] = lower_bound
    cleaned_data[cleaned_data > upper_bound] = upper_bound
    
    # 3. 模拟缺失值并处理
    np.random.seed(123)
    missing_mask = np.random.random(sales_data.shape) < 0.05  # 随机生成5%的缺失值
    data_with_missing = cleaned_data.copy()
    data_with_missing[missing_mask] = np.nan
    
    missing_count = np.sum(missing_mask)
    print(f"\n3. 缺失值处理:")
    print(f"   模拟缺失值数量: {missing_count}")
    print(f"   缺失值比例: {missing_count/sales_data.size*100:.2f}%")
    
    # 用均值填充缺失值（按产品-地区组合计算均值）
    filled_data = data_with_missing.copy()
    for product in range(sales_data.shape[1]):
        for region in range(sales_data.shape[2]):
            product_region_data = data_with_missing[:, product, region]
            mean_value = np.nanmean(product_region_data)
            filled_data[:, product, region] = np.where(
                np.isnan(product_region_data), mean_value, product_region_data
            )
    
    # 4. 数据标准化（按产品标准化）
    normalized_data = np.zeros_like(filled_data)
    for product in range(sales_data.shape[1]):
        product_data = filled_data[:, product, :]
        mean_val = np.mean(product_data)
        std_val = np.std(product_data)
        normalized_data[:, product, :] = (product_data - mean_val) / std_val
    
    print(f"\n4. 数据标准化:")
    print(f"   标准化后各产品均值: {np.mean(normalized_data, axis=(0, 2))}")
    print(f"   标准化后各产品标准差: {np.std(normalized_data, axis=(0, 2))}")
    
    return {
        'original_data': sales_data,
        'cleaned_data': cleaned_data,
        'filled_data': filled_data,
        'normalized_data': normalized_data,
        'outliers_count': outliers_count,
        'missing_count': missing_count,
        'data_shape': data_shape,
        'total_sales': total_sales,
        'mean_daily_sales': mean_daily_sales,
        'std_daily_sales': std_daily_sales
    }


def task2_sales_trend_analysis(sales_info, processed_data):
    """
    任务2：销售趋势分析 - 完整解答
    
    要求：
    1. 计算每日总销售额
    2. 计算7日和30日移动平均
    3. 分析销售增长率
    4. 识别销售高峰和低谷
    5. 计算销售波动性
    
    参数：
        sales_info: 销售数据信息
        processed_data: 预处理后的数据
        
    返回：趋势分析结果
    """
    print("\n=== 任务2：销售趋势分析 - 解答 ===")
    
    sales_data = processed_data['cleaned_data']
    
    # 1. 每日总销售额
    daily_total_sales = np.sum(sales_data, axis=(1, 2))
    
    print(f"1. 每日销售额统计:")
    print(f"   平均日销售额: {np.mean(daily_total_sales):.2f}")
    print(f"   最高日销售额: {np.max(daily_total_sales):.2f}")
    print(f"   最低日销售额: {np.min(daily_total_sales):.2f}")
    
    # 2. 移动平均
    def calculate_moving_average(data, window):
        """计算移动平均"""
        ma = np.zeros_like(data)
        for i in range(len(data)):
            if i < window:
                ma[i] = np.mean(data[:i+1])
            else:
                ma[i] = np.mean(data[i-window+1:i+1])
        return ma
    
    ma_7 = calculate_moving_average(daily_total_sales, 7)
    ma_30 = calculate_moving_average(daily_total_sales, 30)
    
    print(f"\n2. 移动平均线:")
    print(f"   7日移动平均最新值: {ma_7[-1]:.2f}")
    print(f"   30日移动平均最新值: {ma_30[-1]:.2f}")
    
    # 3. 销售增长率
    daily_growth_rate = np.zeros_like(daily_total_sales)
    daily_growth_rate[1:] = (daily_total_sales[1:] - daily_total_sales[:-1]) / daily_total_sales[:-1]
    
    # 周增长率（每7天）
    weekly_growth_rate = np.zeros(len(daily_total_sales) // 7)
    for i in range(len(weekly_growth_rate)):
        if i == 0:
            weekly_growth_rate[i] = 0
        else:
            current_week = np.mean(daily_total_sales[i*7:(i+1)*7])
            previous_week = np.mean(daily_total_sales[(i-1)*7:i*7])
            weekly_growth_rate[i] = (current_week - previous_week) / previous_week
    
    print(f"\n3. 增长率分析:")
    print(f"   平均日增长率: {np.mean(daily_growth_rate[1:]):.4f} ({np.mean(daily_growth_rate[1:])*100:.2f}%)")
    print(f"   平均周增长率: {np.mean(weekly_growth_rate[1:]):.4f} ({np.mean(weekly_growth_rate[1:])*100:.2f}%)")
    print(f"   最大单日增长: {np.max(daily_growth_rate[1:]):.4f} ({np.max(daily_growth_rate[1:])*100:.2f}%)")
    print(f"   最大单日下降: {np.min(daily_growth_rate[1:]):.4f} ({np.min(daily_growth_rate[1:])*100:.2f}%)")
    
    # 4. 高峰和低谷
    peak_indices = np.argsort(daily_total_sales)[-5:]  # 前5名
    valley_indices = np.argsort(daily_total_sales)[:5]  # 后5名
    
    peak_days = peak_indices + 1  # 转换为天数（从1开始）
    valley_days = valley_indices + 1
    
    print(f"\n4. 销售高峰和低谷:")
    print(f"   销售高峰日（前5）: {peak_days}")
    print(f"   对应销售额: {daily_total_sales[peak_indices]}")
    print(f"   销售低谷日（后5）: {valley_days}")
    print(f"   对应销售额: {daily_total_sales[valley_indices]}")
    
    # 5. 波动性分析
    volatility = np.std(daily_total_sales) / np.mean(daily_total_sales)  # 变异系数
    
    # 计算总体趋势
    first_week_avg = np.mean(daily_total_sales[:7])
    last_week_avg = np.mean(daily_total_sales[-7:])
    overall_growth = (last_week_avg - first_week_avg) / first_week_avg
    
    # 趋势方向判断
    if overall_growth > 0.05:
        trend_direction = "强劲上升"
    elif overall_growth > 0.01:
        trend_direction = "温和上升"
    elif overall_growth > -0.01:
        trend_direction = "基本平稳"
    elif overall_growth > -0.05:
        trend_direction = "温和下降"
    else:
        trend_direction = "明显下降"
    
    print(f"\n5. 波动性和趋势:")
    print(f"   销售波动率: {volatility:.4f} ({volatility*100:.2f}%)")
    print(f"   总体增长率: {overall_growth:.4f} ({overall_growth*100:.2f}%)")
    print(f"   趋势方向: {trend_direction}")
    print(f"   第一周平均: {first_week_avg:.2f}")
    print(f"   最后一周平均: {last_week_avg:.2f}")
    
    return {
        'daily_sales': daily_total_sales,
        'ma_7': ma_7,
        'ma_30': ma_30,
        'growth_rates': daily_growth_rate,
        'weekly_growth_rates': weekly_growth_rate,
        'volatility': volatility,
        'overall_growth': overall_growth,
        'trend_direction': trend_direction,
        'peak_days': peak_days,
        'valley_days': valley_days,
        'peak_indices': peak_indices,
        'valley_indices': valley_indices
    }


def task3_regional_product_analysis(sales_info, processed_data):
    """
    任务3：地区和产品表现分析 - 完整解答
    
    要求：
    1. 计算各地区的总销售额和市场份额
    2. 计算各产品的总销售额和市场份额
    3. 找出表现最好和最差的地区/产品
    4. 分析地区-产品组合表现
    5. 计算相关性矩阵
    
    参数：
        sales_info: 销售数据信息
        processed_data: 预处理后的数据
        
    返回：地区产品分析结果
    """
    print("\n=== 任务3：地区和产品表现分析 - 解答 ===")
    
    sales_data = processed_data['cleaned_data']
    products = sales_info['products']
    regions = sales_info['regions']
    
    # 1. 地区分析
    regional_sales = np.sum(sales_data, axis=(0, 1))  # 对天数和产品求和
    total_sales = np.sum(regional_sales)
    regional_share = regional_sales / total_sales
    
    best_region_idx = np.argmax(regional_sales)
    worst_region_idx = np.argmin(regional_sales)
    best_region = regions[best_region_idx]
    worst_region = regions[worst_region_idx]
    
    print(f"1. 地区表现分析:")
    for i, region in enumerate(regions):
        print(f"   {region}: 销售额 {regional_sales[i]:.2f}, 份额 {regional_share[i]:.1%}")
    print(f"   最佳地区: {best_region} (销售额: {regional_sales[best_region_idx]:.2f})")
    print(f"   最差地区: {worst_region} (销售额: {regional_sales[worst_region_idx]:.2f})")
    
    # 2. 产品分析
    product_sales = np.sum(sales_data, axis=(0, 2))  # 对天数和地区求和
    product_share = product_sales / total_sales
    
    best_product_idx = np.argmax(product_sales)
    worst_product_idx = np.argmin(product_sales)
    best_product = products[best_product_idx]
    worst_product = products[worst_product_idx]
    
    print(f"\n2. 产品表现分析:")
    for i, product in enumerate(products):
        print(f"   {product}: 销售额 {product_sales[i]:.2f}, 份额 {product_share[i]:.1%}")
    print(f"   最佳产品: {best_product} (销售额: {product_sales[best_product_idx]:.2f})")
    print(f"   最差产品: {worst_product} (销售额: {product_sales[worst_product_idx]:.2f})")
    
    # 3. 地区-产品组合分析
    combo_sales = np.sum(sales_data, axis=0)  # 对天数求和，得到产品x地区矩阵
    
    # 找出最佳和最差组合
    best_combo_idx = np.unravel_index(np.argmax(combo_sales), combo_sales.shape)
    worst_combo_idx = np.unravel_index(np.argmin(combo_sales), combo_sales.shape)
    
    best_combo = f"{products[best_combo_idx[0]]}-{regions[best_combo_idx[1]]}"
    worst_combo = f"{products[worst_combo_idx[0]]}-{regions[worst_combo_idx[1]]}"
    
    print(f"\n3. 地区-产品组合分析:")
    print(f"   组合销售额矩阵 (产品x地区):\n{combo_sales}")
    print(f"   最佳组合: {best_combo} (销售额: {combo_sales[best_combo_idx]:.2f})")
    print(f"   最差组合: {worst_combo} (销售额: {combo_sales[worst_combo_idx]:.2f})")
    
    # 4. 地区间相关性
    # 计算各地区日销售额的相关性
    regional_daily_sales = np.sum(sales_data, axis=1)  # 形状: (天数, 地区)
    regional_correlation = np.corrcoef(regional_daily_sales.T)
    
    print(f"\n4. 地区间销售相关性:")
    print(f"   相关性矩阵:\n{regional_correlation}")
    
    # 找出相关性最高和最低的地区对
    mask = np.triu(np.ones_like(regional_correlation), k=1).astype(bool)
    correlations = regional_correlation[mask]
    indices = np.where(mask)
    
    max_corr_idx = np.argmax(correlations)
    min_corr_idx = np.argmin(correlations)
    
    max_corr_regions = (regions[indices[0][max_corr_idx]], regions[indices[1][max_corr_idx]])
    min_corr_regions = (regions[indices[0][min_corr_idx]], regions[indices[1][min_corr_idx]])
    
    print(f"   最高相关性: {max_corr_regions[0]}-{max_corr_regions[1]} ({correlations[max_corr_idx]:.3f})")
    print(f"   最低相关性: {min_corr_regions[0]}-{min_corr_regions[1]} ({correlations[min_corr_idx]:.3f})")
    
    # 5. 产品间相关性
    product_daily_sales = np.sum(sales_data, axis=2)  # 形状: (天数, 产品)
    product_correlation = np.corrcoef(product_daily_sales.T)
    
    print(f"\n5. 产品间销售相关性:")
    print(f"   相关性矩阵:\n{product_correlation}")
    
    # 6. 增长率分析
    # 计算各地区和产品的增长率
    first_week = sales_data[:7]
    last_week = sales_data[-7:]
    
    regional_growth = (np.sum(last_week, axis=(0, 1)) - np.sum(first_week, axis=(0, 1))) / np.sum(first_week, axis=(0, 1))
    product_growth = (np.sum(last_week, axis=(0, 2)) - np.sum(first_week, axis=(0, 2))) / np.sum(first_week, axis=(0, 2))
    
    print(f"\n6. 增长率分析 (最后一周 vs 第一周):")
    print(f"   地区增长率:")
    for i, region in enumerate(regions):
        print(f"     {region}: {regional_growth[i]:.2%}")
    
    print(f"   产品增长率:")
    for i, product in enumerate(products):
        print(f"     {product}: {product_growth[i]:.2%}")
    
    return {
        'regional_sales': regional_sales,
        'regional_share': regional_share,
        'product_sales': product_sales,
        'product_share': product_share,
        'combo_sales': combo_sales,
        'regional_correlation': regional_correlation,
        'product_correlation': product_correlation,
        'best_region': best_region,
        'worst_region': worst_region,
        'best_product': best_product,
        'worst_product': worst_product,
        'best_combo': best_combo,
        'worst_combo': worst_combo,
        'regional_growth': regional_growth,
        'product_growth': product_growth
    }


def task4_forecasting_and_insights(sales_info, trend_data, regional_data):
    """
    任务4：预测和商业洞察 - 完整解答
    
    要求：
    1. 基于历史趋势预测未来7天销售额
    2. 计算置信区间
    3. 识别业务风险和机会
    4. 提供数据驱动的建议
    
    参数：
        sales_info: 销售数据信息
        trend_data: 趋势分析数据
        regional_data: 地区分析数据
        
    返回：预测和洞察结果
    """
    print("\n=== 任务4：预测和商业洞察 - 解答 ===")
    
    daily_sales = trend_data['daily_sales']
    
    # 1. 简单线性趋势预测
    days = np.arange(len(daily_sales))
    
    # 计算线性回归系数（手动实现）
    n = len(daily_sales)
    sum_x = np.sum(days)
    sum_y = np.sum(daily_sales)
    sum_xy = np.sum(days * daily_sales)
    sum_x2 = np.sum(days ** 2)
    
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    intercept = (sum_y - slope * sum_x) / n
    
    print(f"1. 线性趋势分析:")
    print(f"   回归方程: y = {slope:.2f}x + {intercept:.2f}")
    print(f"   趋势斜率: {slope:.2f} (每天增长)")
    
    # 预测未来7天
    future_days = np.arange(len(daily_sales), len(daily_sales) + 7)
    forecast = slope * future_days + intercept
    
    print(f"\n2. 未来7天预测:")
    for i, pred in enumerate(forecast):
        print(f"   第{i+1}天: {pred:.2f}")
    
    # 2. 计算预测置信区间
    # 计算残差和标准误差
    fitted_values = slope * days + intercept
    residuals = daily_sales - fitted_values
    mse = np.mean(residuals ** 2)
    std_error = np.sqrt(mse)
    
    # 95%置信区间 (假设t分布，简化为1.96)
    confidence_interval = 1.96 * std_error
    forecast_upper = forecast + confidence_interval
    forecast_lower = forecast - confidence_interval
    
    print(f"\n3. 预测置信区间:")
    print(f"   标准误差: {std_error:.2f}")
    print(f"   95%置信区间宽度: ±{confidence_interval:.2f}")
    print(f"   预测区间:")
    for i in range(7):
        print(f"     第{i+1}天: [{forecast_lower[i]:.2f}, {forecast_upper[i]:.2f}]")
    
    # 3. 风险识别
    volatility = trend_data['volatility']
    growth_rate = trend_data['overall_growth']
    
    # 风险评估
    risk_factors = []
    if volatility > 0.15:
        risk_factors.append("高波动性")
    if growth_rate < -0.05:
        risk_factors.append("负增长趋势")
    if np.min(daily_sales) < np.mean(daily_sales) * 0.7:
        risk_factors.append("存在极低销售日")
    
    if len(risk_factors) >= 2:
        risk_level = "高"
    elif len(risk_factors) == 1:
        risk_level = "中"
    else:
        risk_level = "低"
    
    print(f"\n4. 风险评估:")
    print(f"   风险等级: {risk_level}")
    print(f"   风险因素: {', '.join(risk_factors) if risk_factors else '无明显风险'}")
    
    # 4. 商业洞察
    insights = []
    
    # 基于增长趋势的建议
    if growth_rate > 0.1:
        insights.append("销售增长强劲，建议增加库存并扩大营销投入")
    elif growth_rate > 0.05:
        insights.append("销售稳步增长，建议保持当前策略")
    elif growth_rate > 0:
        insights.append("销售温和增长，建议优化产品组合")
    elif growth_rate > -0.05:
        insights.append("销售基本平稳，建议寻找新的增长点")
    else:
        insights.append("销售下滑，需要制定紧急应对策略")
    
    # 基于波动性的建议
    if volatility > 0.2:
        insights.append("销售波动较大，建议优化供应链管理和库存策略")
    elif volatility < 0.05:
        insights.append("销售相对稳定，可以考虑扩大市场份额")
    
    # 基于地区表现的建议
    best_region = regional_data['best_region']
    worst_region = regional_data['worst_region']
    insights.append(f"重点维护{best_region}市场优势，加强{worst_region}市场投入")
    
    # 基于产品表现的建议
    best_product = regional_data['best_product']
    worst_product = regional_data['worst_product']
    insights.append(f"继续推广{best_product}，考虑{worst_product}的产品策略调整")
    
    # 基于相关性的建议
    regional_corr = regional_data['regional_correlation']
    avg_correlation = np.mean(regional_corr[np.triu_indices_from(regional_corr, k=1)])
    if avg_correlation > 0.7:
        insights.append("各地区销售高度相关，建议统一营销策略")
    elif avg_correlation < 0.3:
        insights.append("各地区销售差异较大，建议制定差异化策略")
    
    # 季节性建议
    weekly_pattern = []
    for day_of_week in range(7):
        day_sales = [daily_sales[i] for i in range(len(daily_sales)) if i % 7 == day_of_week]
        weekly_pattern.append(np.mean(day_sales))
    
    best_day = np.argmax(weekly_pattern)
    worst_day = np.argmin(weekly_pattern)
    day_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    
    insights.append(f"{day_names[best_day]}销售最佳，{day_names[worst_day]}销售最差，建议调整促销时机")
    
    print(f"\n5. 商业洞察和建议:")
    for i, insight in enumerate(insights, 1):
        print(f"   {i}. {insight}")
    
    # 5. 具体行动建议
    action_items = []
    
    if growth_rate > 0.05:
        action_items.append("增加热销产品库存")
        action_items.append("扩大优势地区的市场投入")
    
    if volatility > 0.15:
        action_items.append("建立更灵活的供应链体系")
        action_items.append("实施动态定价策略")
    
    if risk_level == "高":
        action_items.append("制定风险应对预案")
        action_items.append("加强市场监控和预警")
    
    action_items.append(f"重点关注{worst_region}市场的改进机会")
    action_items.append(f"考虑{worst_product}的产品升级或替换")
    
    print(f"\n6. 具体行动建议:")
    for i, action in enumerate(action_items, 1):
        print(f"   {i}. {action}")
    
    return {
        'forecast': forecast,
        'forecast_upper': forecast_upper,
        'forecast_lower': forecast_lower,
        'mse': mse,
        'std_error': std_error,
        'slope': slope,
        'intercept': intercept,
        'risk_level': risk_level,
        'risk_factors': risk_factors,
        'insights': insights,
        'action_items': action_items,
        'weekly_pattern': weekly_pattern
    }


def generate_report(sales_info, all_results):
    """
    生成综合分析报告 - 完整解答
    
    参数：
        sales_info: 销售数据信息
        all_results: 所有分析结果
    """
    print("\n" + "=" * 60)
    print("           销售数据分析报告")
    print("=" * 60)
    
    # 报告摘要
    print("\n【执行摘要】")
    print(f"分析期间: {sales_info['days']}天")
    print(f"产品类别: {len(sales_info['products'])}个 ({', '.join(sales_info['products'])})")
    print(f"销售地区: {len(sales_info['regions'])}个 ({', '.join(sales_info['regions'])})")
    print(f"数据质量: 异常值{all_results['processed']['outliers_count']}个，缺失值{all_results['processed']['missing_count']}个")
    
    # 关键指标
    trend_data = all_results['trend']
    regional_data = all_results['regional']
    forecast_data = all_results['forecast']
    
    print(f"\n【关键指标】")
    print(f"总销售额: {all_results['processed']['total_sales']:.2f}")
    print(f"日均销售额: {all_results['processed']['mean_daily_sales']:.2f}")
    print(f"销售增长率: {trend_data['overall_growth']:.2%}")
    print(f"销售波动率: {trend_data['volatility']:.2%}")
    print(f"趋势方向: {trend_data['trend_direction']}")
    
    print(f"\n【市场表现】")
    print(f"最佳地区: {regional_data['best_region']} (份额: {regional_data['regional_share'][sales_info['regions'].index(regional_data['best_region'])]:.1%})")
    print(f"最差地区: {regional_data['worst_region']} (份额: {regional_data['regional_share'][sales_info['regions'].index(regional_data['worst_region'])]:.1%})")
    print(f"最佳产品: {regional_data['best_product']} (份额: {regional_data['product_share'][sales_info['products'].index(regional_data['best_product'])]:.1%})")
    print(f"最差产品: {regional_data['worst_product']} (份额: {regional_data['product_share'][sales_info['products'].index(regional_data['worst_product'])]:.1%})")
    print(f"最佳组合: {regional_data['best_combo']}")
    
    print(f"\n【预测展望】")
    print(f"未来7天预期总销售额: {np.sum(forecast_data['forecast']):.2f}")
    print(f"预测置信区间: ±{1.96 * forecast_data['std_error']:.2f}")
    print(f"风险等级: {forecast_data['risk_level']}")
    if forecast_data['risk_factors']:
        print(f"主要风险: {', '.join(forecast_data['risk_factors'])}")
    
    print(f"\n【数据洞察】")
    # 显示前3个最重要的洞察
    for i, insight in enumerate(forecast_data['insights'][:3], 1):
        print(f"{i}. {insight}")
    
    print(f"\n【行动建议】")
    # 显示前3个最重要的行动建议
    for i, action in enumerate(forecast_data['action_items'][:3], 1):
        print(f"{i}. {action}")
    
    print(f"\n【技术指标】")
    print(f"线性回归斜率: {forecast_data['slope']:.2f}")
    print(f"预测标准误差: {forecast_data['std_error']:.2f}")
    print(f"地区间平均相关性: {np.mean(regional_data['regional_correlation'][np.triu_indices_from(regional_data['regional_correlation'], k=1)]):.3f}")
    print(f"产品间平均相关性: {np.mean(regional_data['product_correlation'][np.triu_indices_from(regional_data['product_correlation'], k=1)]):.3f}")
    
    print("\n" + "=" * 60)
    print("报告生成完成 - 基于NumPy数据分析")
    print("=" * 60)


def main():
    """
    主函数：运行完整的数据分析项目 - 完整解答
    """
    print("Session12 练习题3完整解答：NumPy实际应用 - 销售数据分析项目")
    print("=" * 70)
    
    # 生成数据
    sales_info = generate_sales_data()
    
    # 执行分析任务
    processed_data = task1_data_preprocessing(sales_info)
    trend_data = task2_sales_trend_analysis(sales_info, processed_data)
    regional_data = task3_regional_product_analysis(sales_info, processed_data)
    forecast_data = task4_forecasting_and_insights(sales_info, trend_data, regional_data)
    
    # 汇总结果
    all_results = {
        'processed': processed_data,
        'trend': trend_data,
        'regional': regional_data,
        'forecast': forecast_data
    }
    
    # 生成报告
    generate_report(sales_info, all_results)
    
    print("\n=== 项目完成 - 学习总结 ===")
    print("恭喜！你已经完成了一个完整的数据分析项目。")
    print("\n本项目展示了NumPy在实际数据科学工作中的应用：")
    print("1. 数据生成和预处理 - 数组创建、异常值处理、缺失值填充")
    print("2. 统计分析 - 描述性统计、移动平均、增长率计算")
    print("3. 多维数据分析 - 地区产品组合分析、相关性分析")
    print("4. 预测建模 - 线性回归、置信区间、风险评估")
    print("5. 商业洞察 - 数据驱动的决策建议")
    print("\n这些技能是数据科学家的核心能力，NumPy是基础工具！")


if __name__ == "__main__":
    main()