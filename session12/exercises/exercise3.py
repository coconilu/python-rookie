#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session12 练习题3：NumPy实际应用 - 数据分析项目

题目描述：
本练习是一个综合性的数据分析项目，模拟真实的数据科学工作场景。
你将使用NumPy处理和分析一个虚拟的销售数据集，学习如何在实际项目中应用NumPy。

项目背景：
某电商公司有3个月的销售数据，包含5个产品类别在不同地区的销售情况。
需要分析销售趋势、地区表现、产品表现等关键指标。

练习内容：
1. 数据生成和预处理
2. 销售趋势分析
3. 地区和产品表现分析
4. 异常检测和数据清洗
5. 预测和建议

提示：
- 这是一个综合性练习，需要运用前面学到的所有NumPy知识
- 注意数据的维度和含义
- 思考业务逻辑，不只是技术实现

作者: Python教程团队
创建日期: 2024-12-19
"""

import numpy as np


def generate_sales_data():
    """
    生成模拟销售数据
    
    数据结构：
    - 维度：(90天, 5个产品, 4个地区)
    - 产品：['电子产品', '服装', '家居', '图书', '运动用品']
    - 地区：['北京', '上海', '广州', '深圳']
    
    返回：销售数据和相关信息
    """
    print("=== 数据生成 ===")
    
    np.random.seed(42)
    
    # 基础参数
    days = 90
    products = ['电子产品', '服装', '家居', '图书', '运动用品']
    regions = ['北京', '上海', '广州', '深圳']
    
    # TODO: 生成销售数据
    # 提示：可以为不同产品和地区设置不同的基础销量和波动
    
    # 基础销量矩阵 (产品 x 地区)
    base_sales = None  # 5x4矩阵，设置每个产品在每个地区的基础日销量
    
    # 生成90天的销售数据
    sales_data = None  # 90x5x4的三维数组
    
    # 添加趋势和季节性
    # 趋势：整体销量随时间增长
    trend_factor = None  # 计算趋势因子
    
    # 季节性：周末销量更高
    seasonal_factor = None  # 计算季节性因子
    
    # 应用趋势和季节性
    # TODO: 将趋势和季节性应用到销售数据
    
    print(f"数据形状: {sales_data.shape if sales_data is not None else None}")
    print(f"产品类别: {products}")
    print(f"销售地区: {regions}")
    print(f"数据期间: {days}天")
    
    return {
        'data': sales_data,
        'products': products,
        'regions': regions,
        'days': days
    }


def task1_data_preprocessing(sales_info):
    """
    任务1：数据预处理
    
    要求：
    1. 检查数据的基本信息（形状、统计量）
    2. 处理异常值（使用IQR方法）
    3. 计算缺失值（模拟一些缺失数据）
    4. 数据标准化
    
    参数：
        sales_info: 销售数据信息字典
        
    返回：预处理结果
    """
    print("\n=== 任务1：数据预处理 ===")
    
    sales_data = sales_info['data']
    products = sales_info['products']
    regions = sales_info['regions']
    
    # TODO: 在这里完成你的代码
    
    # 1. 基本信息
    data_shape = None
    total_sales = None      # 总销售额
    mean_daily_sales = None # 日均销售额
    std_daily_sales = None  # 日销售额标准差
    
    # 2. 异常值检测和处理
    # 将三维数据展平为一维进行异常值检测
    flat_data = None        # 展平数据
    q1 = None              # 第一四分位数
    q3 = None              # 第三四分位数
    iqr = None             # 四分位距
    lower_bound = None     # 下界
    upper_bound = None     # 上界
    
    # 找出异常值
    outliers_mask = None   # 异常值掩码
    outliers_count = None  # 异常值数量
    
    # 处理异常值（用边界值替换）
    cleaned_data = None    # 清洗后的数据
    
    # 3. 模拟缺失值并处理
    np.random.seed(123)
    missing_mask = None    # 随机生成5%的缺失值
    data_with_missing = None # 包含缺失值的数据
    
    # 用均值填充缺失值
    filled_data = None     # 填充后的数据
    
    # 4. 数据标准化（按产品标准化）
    normalized_data = None # 标准化后的数据
    
    # 打印结果
    print(f"数据形状: {data_shape}")
    print(f"总销售额: {total_sales:.2f}")
    print(f"日均销售额: {mean_daily_sales:.2f}")
    print(f"日销售额标准差: {std_daily_sales:.2f}")
    print(f"\n异常值检测:")
    print(f"异常值数量: {outliers_count}")
    print(f"异常值比例: {outliers_count/len(flat_data)*100:.2f}%")
    print(f"异常值范围: (<{lower_bound:.2f} 或 >{upper_bound:.2f})")
    
    return {
        'original_data': sales_data,
        'cleaned_data': cleaned_data,
        'filled_data': filled_data,
        'normalized_data': normalized_data,
        'outliers_count': outliers_count,
        'missing_count': np.sum(missing_mask) if missing_mask is not None else 0
    }


def task2_sales_trend_analysis(sales_info, processed_data):
    """
    任务2：销售趋势分析
    
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
    print("\n=== 任务2：销售趋势分析 ===")
    
    sales_data = processed_data['cleaned_data']
    
    # TODO: 在这里完成你的代码
    
    # 1. 每日总销售额
    daily_total_sales = None  # 对产品和地区维度求和
    
    # 2. 移动平均
    ma_7 = None              # 7日移动平均
    ma_30 = None             # 30日移动平均
    
    # 3. 销售增长率
    daily_growth_rate = None # 日增长率
    weekly_growth_rate = None # 周增长率（每7天）
    
    # 4. 高峰和低谷
    peak_days = None         # 销售高峰日（前5名）
    valley_days = None       # 销售低谷日（后5名）
    
    # 5. 波动性分析
    volatility = None        # 销售波动率（标准差/均值）
    trend_direction = None   # 趋势方向（正/负/平稳）
    
    # 计算总体趋势
    first_week_avg = None    # 第一周平均销售额
    last_week_avg = None     # 最后一周平均销售额
    overall_growth = None    # 总体增长率
    
    # 打印结果
    print(f"销售趋势分析:")
    print(f"日均销售额: {np.mean(daily_total_sales):.2f}")
    print(f"销售额范围: [{np.min(daily_total_sales):.2f}, {np.max(daily_total_sales):.2f}]")
    print(f"销售波动率: {volatility:.2%}")
    print(f"总体增长率: {overall_growth:.2%}")
    print(f"\n销售高峰日（前5）: {peak_days}")
    print(f"销售低谷日（后5）: {valley_days}")
    
    return {
        'daily_sales': daily_total_sales,
        'ma_7': ma_7,
        'ma_30': ma_30,
        'growth_rates': daily_growth_rate,
        'volatility': volatility,
        'overall_growth': overall_growth,
        'peak_days': peak_days,
        'valley_days': valley_days
    }


def task3_regional_product_analysis(sales_info, processed_data):
    """
    任务3：地区和产品表现分析
    
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
    print("\n=== 任务3：地区和产品表现分析 ===")
    
    sales_data = processed_data['cleaned_data']
    products = sales_info['products']
    regions = sales_info['regions']
    
    # TODO: 在这里完成你的代码
    
    # 1. 地区分析
    regional_sales = None    # 各地区总销售额
    regional_share = None    # 各地区市场份额
    best_region = None       # 表现最好的地区
    worst_region = None      # 表现最差的地区
    
    # 2. 产品分析
    product_sales = None     # 各产品总销售额
    product_share = None     # 各产品市场份额
    best_product = None      # 表现最好的产品
    worst_product = None     # 表现最差的产品
    
    # 3. 地区-产品组合分析
    combo_sales = None       # 地区-产品组合销售额矩阵
    best_combo = None        # 最佳组合
    worst_combo = None       # 最差组合
    
    # 4. 地区间相关性
    regional_correlation = None  # 地区间销售相关性
    
    # 5. 产品间相关性
    product_correlation = None   # 产品间销售相关性
    
    # 6. 增长率分析
    regional_growth = None   # 各地区增长率
    product_growth = None    # 各产品增长率
    
    # 打印结果
    print(f"地区表现分析:")
    for i, region in enumerate(regions):
        print(f"{region}: 销售额 {regional_sales[i]:.2f}, 份额 {regional_share[i]:.1%}")
    print(f"最佳地区: {best_region}")
    print(f"最差地区: {worst_region}")
    
    print(f"\n产品表现分析:")
    for i, product in enumerate(products):
        print(f"{product}: 销售额 {product_sales[i]:.2f}, 份额 {product_share[i]:.1%}")
    print(f"最佳产品: {best_product}")
    print(f"最差产品: {worst_product}")
    
    print(f"\n最佳组合: {best_combo}")
    print(f"最差组合: {worst_combo}")
    
    return {
        'regional_sales': regional_sales,
        'regional_share': regional_share,
        'product_sales': product_sales,
        'product_share': product_share,
        'combo_sales': combo_sales,
        'regional_correlation': regional_correlation,
        'product_correlation': product_correlation,
        'best_region': best_region,
        'best_product': best_product
    }


def task4_forecasting_and_insights(sales_info, trend_data, regional_data):
    """
    任务4：预测和商业洞察
    
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
    print("\n=== 任务4：预测和商业洞察 ===")
    
    daily_sales = trend_data['daily_sales']
    
    # TODO: 在这里完成你的代码
    
    # 1. 简单线性趋势预测
    days = np.arange(len(daily_sales))
    
    # 计算线性回归系数（手动实现）
    slope = None             # 斜率
    intercept = None         # 截距
    
    # 预测未来7天
    future_days = np.arange(len(daily_sales), len(daily_sales) + 7)
    forecast = None          # 预测值
    
    # 2. 计算预测置信区间
    residuals = None         # 残差
    mse = None              # 均方误差
    std_error = None        # 标准误差
    
    # 95%置信区间
    confidence_interval = None  # 置信区间宽度
    forecast_upper = None    # 预测上界
    forecast_lower = None    # 预测下界
    
    # 3. 风险识别
    volatility = trend_data['volatility']
    growth_rate = trend_data['overall_growth']
    
    # 风险评估
    risk_level = None        # 风险等级（低/中/高）
    
    # 4. 商业洞察
    insights = []
    
    # 基于数据生成洞察
    if growth_rate > 0.1:
        insights.append("销售增长强劲，建议增加库存")
    elif growth_rate < -0.05:
        insights.append("销售下滑，需要制定促销策略")
    
    if volatility > 0.3:
        insights.append("销售波动较大，建议优化供应链管理")
    
    # 地区建议
    best_region = regional_data['best_region']
    worst_region = regional_data['worst_region']
    insights.append(f"重点关注{best_region}市场，加强{worst_region}市场投入")
    
    # 打印结果
    print(f"预测分析:")
    print(f"未来7天预测销售额: {forecast}")
    print(f"预测区间: [{forecast_lower}, {forecast_upper}]")
    print(f"预测准确度(MSE): {mse:.2f}")
    print(f"风险等级: {risk_level}")
    
    print(f"\n商业洞察:")
    for i, insight in enumerate(insights, 1):
        print(f"{i}. {insight}")
    
    return {
        'forecast': forecast,
        'forecast_upper': forecast_upper,
        'forecast_lower': forecast_lower,
        'mse': mse,
        'risk_level': risk_level,
        'insights': insights
    }


def generate_report(sales_info, all_results):
    """
    生成综合分析报告
    
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
    print(f"产品类别: {len(sales_info['products'])}个")
    print(f"销售地区: {len(sales_info['regions'])}个")
    
    # 关键指标
    trend_data = all_results['trend']
    regional_data = all_results['regional']
    forecast_data = all_results['forecast']
    
    print(f"\n【关键指标】")
    print(f"总销售额: {np.sum(trend_data['daily_sales']):.2f}")
    print(f"日均销售额: {np.mean(trend_data['daily_sales']):.2f}")
    print(f"销售增长率: {trend_data['overall_growth']:.2%}")
    print(f"销售波动率: {trend_data['volatility']:.2%}")
    
    print(f"\n【市场表现】")
    print(f"最佳地区: {regional_data['best_region']}")
    print(f"最佳产品: {regional_data['best_product']}")
    
    print(f"\n【预测展望】")
    print(f"未来7天预期销售额: {np.sum(forecast_data['forecast']):.2f}")
    print(f"风险等级: {forecast_data['risk_level']}")
    
    print(f"\n【建议措施】")
    for i, insight in enumerate(forecast_data['insights'], 1):
        print(f"{i}. {insight}")
    
    print("\n" + "=" * 60)
    print("报告生成完成")
    print("=" * 60)


def main():
    """
    主函数：运行完整的数据分析项目
    """
    print("Session12 练习题3：NumPy实际应用 - 销售数据分析项目")
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
    
    print("\n=== 项目完成 ===")
    print("恭喜！你已经完成了一个完整的数据分析项目。")
    print("这个练习展示了NumPy在实际数据科学工作中的强大应用。")
    print("如果遇到问题，请参考solutions目录中的完整解答。")


if __name__ == "__main__":
    main()