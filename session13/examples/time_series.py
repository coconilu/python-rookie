#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
时间序列处理示例

本文件演示使用Pandas进行时间序列数据处理，包括：
- 时间序列创建和索引
- 时间数据解析和格式化
- 时间序列重采样
- 滑动窗口计算
- 时间序列可视化
- 季节性分析

作者: Python教程团队
创建日期: 2024-01-01
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings

# 设置
warnings.filterwarnings('ignore')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")


def create_time_series_data():
    """
    创建时间序列示例数据
    """
    print("=== 创建时间序列数据 ===")
    
    # 1. 创建日期范围
    print("\n1. 创建日期范围：")
    
    # 创建日期范围
    date_range = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
    print(f"日期范围: {date_range[0]} 到 {date_range[-1]}")
    print(f"总天数: {len(date_range)}")
    
    # 2. 创建模拟的销售数据
    print("\n2. 创建模拟销售数据：")
    
    np.random.seed(42)
    n_days = len(date_range)
    
    # 基础趋势（逐渐增长）
    trend = np.linspace(1000, 1500, n_days)
    
    # 季节性模式（年度周期）
    seasonal_yearly = 200 * np.sin(2 * np.pi * np.arange(n_days) / 365.25)
    
    # 周度季节性（周末销量更高）
    seasonal_weekly = 100 * np.sin(2 * np.pi * np.arange(n_days) / 7 + np.pi/2)
    
    # 随机噪声
    noise = np.random.normal(0, 50, n_days)
    
    # 特殊事件（促销活动）
    special_events = np.zeros(n_days)
    # 春节期间销量下降
    spring_festival_2023 = (date_range >= '2023-01-21') & (date_range <= '2023-01-27')
    spring_festival_2024 = (date_range >= '2024-02-10') & (date_range <= '2024-02-16')
    special_events[spring_festival_2023] = -300
    special_events[spring_festival_2024] = -300
    
    # 双11促销
    double11_2023 = date_range == '2023-11-11'
    double11_2024 = date_range == '2024-11-11'
    special_events[double11_2023] = 800
    special_events[double11_2024] = 800
    
    # 合成最终销售数据
    sales = trend + seasonal_yearly + seasonal_weekly + noise + special_events
    sales = np.maximum(sales, 100)  # 确保销售额不为负
    
    # 创建DataFrame
    ts_data = pd.DataFrame({
        '日期': date_range,
        '销售额': sales,
        '趋势': trend,
        '年度季节性': seasonal_yearly,
        '周度季节性': seasonal_weekly,
        '噪声': noise,
        '特殊事件': special_events
    })
    
    # 设置日期为索引
    ts_data.set_index('日期', inplace=True)
    
    print(f"时间序列数据形状: {ts_data.shape}")
    print("\n数据预览:")
    print(ts_data.head())
    
    return ts_data


def datetime_operations():
    """
    日期时间操作示例
    """
    print("\n=== 日期时间操作 ===")
    
    # 1. 创建和解析日期
    print("\n1. 创建和解析日期：")
    
    # 字符串转日期
    date_strings = ['2024-01-01', '2024-06-15', '2024-12-31']
    dates = pd.to_datetime(date_strings)
    print(f"字符串转日期: {dates}")
    
    # 不同格式的日期解析
    mixed_dates = ['01/15/2024', '2024-03-20', '2024年5月1日']
    try:
        parsed_dates = pd.to_datetime(mixed_dates, infer_datetime_format=True)
        print(f"混合格式解析: {parsed_dates}")
    except:
        print("混合格式解析失败，需要指定格式")
    
    # 2. 日期组件提取
    print("\n2. 日期组件提取：")
    
    sample_date = pd.Timestamp('2024-03-15 14:30:25')
    print(f"原始日期: {sample_date}")
    print(f"年份: {sample_date.year}")
    print(f"月份: {sample_date.month}")
    print(f"日: {sample_date.day}")
    print(f"星期几: {sample_date.dayofweek} (0=周一)")
    print(f"星期名: {sample_date.day_name()}")
    print(f"月份名: {sample_date.month_name()}")
    print(f"季度: {sample_date.quarter}")
    print(f"一年中的第几天: {sample_date.dayofyear}")
    
    # 3. 日期范围和频率
    print("\n3. 日期范围和频率：")
    
    # 不同频率的日期范围
    daily = pd.date_range('2024-01-01', periods=5, freq='D')
    weekly = pd.date_range('2024-01-01', periods=5, freq='W')
    monthly = pd.date_range('2024-01-01', periods=5, freq='M')
    quarterly = pd.date_range('2024-01-01', periods=5, freq='Q')
    
    print(f"每日: {daily}")
    print(f"每周: {weekly}")
    print(f"每月: {monthly}")
    print(f"每季度: {quarterly}")
    
    # 4. 时区处理
    print("\n4. 时区处理：")
    
    # 创建带时区的时间
    utc_time = pd.Timestamp('2024-01-01 12:00:00', tz='UTC')
    beijing_time = utc_time.tz_convert('Asia/Shanghai')
    
    print(f"UTC时间: {utc_time}")
    print(f"北京时间: {beijing_time}")
    
    return dates


def time_series_indexing(ts_data):
    """
    时间序列索引和选择
    """
    print("\n=== 时间序列索引和选择 ===")
    
    # 1. 基本索引
    print("\n1. 基本时间索引：")
    
    # 选择特定日期
    specific_date = ts_data.loc['2024-01-01']
    print(f"2024年1月1日数据:\n{specific_date}")
    
    # 选择日期范围
    date_range_data = ts_data.loc['2024-01-01':'2024-01-07']
    print(f"\n2024年1月1-7日数据形状: {date_range_data.shape}")
    
    # 2. 部分字符串索引
    print("\n2. 部分字符串索引：")
    
    # 选择整个月
    january_2024 = ts_data.loc['2024-01']
    print(f"2024年1月数据形状: {january_2024.shape}")
    
    # 选择整年
    year_2024 = ts_data.loc['2024']
    print(f"2024年数据形状: {year_2024.shape}")
    
    # 3. 条件选择
    print("\n3. 条件选择：")
    
    # 选择周末数据
    weekend_data = ts_data[ts_data.index.dayofweek >= 5]
    print(f"周末数据形状: {weekend_data.shape}")
    
    # 选择特定月份
    summer_months = ts_data[ts_data.index.month.isin([6, 7, 8])]
    print(f"夏季月份数据形状: {summer_months.shape}")
    
    # 4. 时间序列切片
    print("\n4. 高级时间切片：")
    
    # 使用between_time选择特定时间（如果有时间信息）
    # 这里我们添加一些时间信息
    hourly_data = pd.DataFrame({
        '值': np.random.randn(24),
    }, index=pd.date_range('2024-01-01', periods=24, freq='H'))
    
    business_hours = hourly_data.between_time('09:00', '17:00')
    print(f"工作时间数据形状: {business_hours.shape}")
    
    return january_2024, weekend_data


def resampling_operations(ts_data):
    """
    时间序列重采样操作
    """
    print("\n=== 时间序列重采样 ===")
    
    # 1. 降采样（Down-sampling）
    print("\n1. 降采样操作：")
    
    # 日数据聚合为周数据
    weekly_data = ts_data['销售额'].resample('W').agg({
        '周销售额': 'sum',
        '平均日销售额': 'mean',
        '最高日销售额': 'max',
        '最低日销售额': 'min',
        '销售额标准差': 'std'
    }).round(2)
    
    print(f"周数据形状: {weekly_data.shape}")
    print("\n周数据预览:")
    print(weekly_data.head())
    
    # 日数据聚合为月数据
    monthly_data = ts_data['销售额'].resample('M').agg({
        '月销售额': 'sum',
        '平均日销售额': 'mean',
        '销售天数': 'count'
    }).round(2)
    
    print(f"\n月数据形状: {monthly_data.shape}")
    print("月数据预览:")
    print(monthly_data.head())
    
    # 2. 升采样（Up-sampling）
    print("\n2. 升采样操作：")
    
    # 创建一些月度数据
    monthly_sales = ts_data['销售额'].resample('M').sum()
    
    # 升采样为日数据（前向填充）
    daily_from_monthly_ffill = monthly_sales.resample('D').ffill()
    print(f"前向填充升采样形状: {daily_from_monthly_ffill.shape}")
    
    # 升采样为日数据（线性插值）
    daily_from_monthly_interp = monthly_sales.resample('D').interpolate()
    print(f"线性插值升采样形状: {daily_from_monthly_interp.shape}")
    
    # 3. 自定义聚合函数
    print("\n3. 自定义聚合函数：")
    
    def custom_agg(series):
        return {
            '总和': series.sum(),
            '均值': series.mean(),
            '中位数': series.median(),
            '变异系数': series.std() / series.mean() if series.mean() != 0 else 0
        }
    
    custom_weekly = ts_data['销售额'].resample('W').apply(lambda x: pd.Series(custom_agg(x)))
    print("\n自定义聚合结果预览:")
    print(custom_weekly.head())
    
    # 4. 多列重采样
    print("\n4. 多列重采样：")
    
    multi_col_resample = ts_data[['销售额', '趋势']].resample('M').agg({
        '销售额': ['sum', 'mean', 'std'],
        '趋势': ['mean', 'first', 'last']
    }).round(2)
    
    print("多列重采样结果:")
    print(multi_col_resample.head())
    
    return weekly_data, monthly_data, daily_from_monthly_interp


def rolling_operations(ts_data):
    """
    滑动窗口操作
    """
    print("\n=== 滑动窗口操作 ===")
    
    # 1. 基本滑动窗口
    print("\n1. 基本滑动窗口计算：")
    
    sales = ts_data['销售额'].copy()
    
    # 计算移动平均
    sales_ma7 = sales.rolling(window=7).mean()  # 7日移动平均
    sales_ma30 = sales.rolling(window=30).mean()  # 30日移动平均
    
    # 计算移动标准差
    sales_std7 = sales.rolling(window=7).std()
    
    # 计算移动最大值和最小值
    sales_max7 = sales.rolling(window=7).max()
    sales_min7 = sales.rolling(window=7).min()
    
    print(f"7日移动平均前5个值:\n{sales_ma7.head()}")
    
    # 2. 中心化滑动窗口
    print("\n2. 中心化滑动窗口：")
    
    # 中心化移动平均（前后各取一半窗口）
    sales_ma7_center = sales.rolling(window=7, center=True).mean()
    
    print(f"中心化7日移动平均前10个值:\n{sales_ma7_center.head(10)}")
    
    # 3. 指数加权移动平均
    print("\n3. 指数加权移动平均：")
    
    # EWMA（指数加权移动平均）
    sales_ewm = sales.ewm(span=7).mean()  # 相当于7日EWMA
    sales_ewm_alpha = sales.ewm(alpha=0.3).mean()  # 指定衰减因子
    
    print(f"指数加权移动平均前5个值:\n{sales_ewm.head()}")
    
    # 4. 自定义滑动窗口函数
    print("\n4. 自定义滑动窗口函数：")
    
    # 计算滑动窗口内的分位数
    sales_q25 = sales.rolling(window=7).quantile(0.25)
    sales_q75 = sales.rolling(window=7).quantile(0.75)
    
    # 自定义函数：计算滑动窗口内的变异系数
    def coefficient_of_variation(x):
        return x.std() / x.mean() if x.mean() != 0 else 0
    
    sales_cv = sales.rolling(window=7).apply(coefficient_of_variation)
    
    print(f"7日滑动变异系数前10个值:\n{sales_cv.head(10)}")
    
    # 5. 滑动窗口可视化
    print("\n5. 滑动窗口可视化：")
    
    # 选择一个月的数据进行可视化
    sample_period = '2024-01'
    sample_data = ts_data.loc[sample_period, '销售额']
    sample_ma7 = sales_ma7.loc[sample_period]
    sample_ma30 = sales_ma30.loc[sample_period]
    sample_ewm = sales_ewm.loc[sample_period]
    
    plt.figure(figsize=(14, 8))
    
    plt.plot(sample_data.index, sample_data, label='原始数据', alpha=0.7, linewidth=1)
    plt.plot(sample_ma7.index, sample_ma7, label='7日移动平均', linewidth=2)
    plt.plot(sample_ma30.index, sample_ma30, label='30日移动平均', linewidth=2)
    plt.plot(sample_ewm.index, sample_ewm, label='指数加权移动平均', linewidth=2)
    
    plt.title(f'{sample_period} 销售额及移动平均')
    plt.xlabel('日期')
    plt.ylabel('销售额')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    # 6. 布林带计算
    print("\n6. 布林带计算：")
    
    # 计算布林带（移动平均 ± 2倍标准差）
    bollinger_middle = sales_ma7
    bollinger_upper = sales_ma7 + 2 * sales_std7
    bollinger_lower = sales_ma7 - 2 * sales_std7
    
    # 可视化布林带
    plt.figure(figsize=(14, 8))
    
    sample_period = '2024-06'
    period_sales = sales.loc[sample_period]
    period_upper = bollinger_upper.loc[sample_period]
    period_middle = bollinger_middle.loc[sample_period]
    period_lower = bollinger_lower.loc[sample_period]
    
    plt.plot(period_sales.index, period_sales, label='销售额', linewidth=1)
    plt.plot(period_middle.index, period_middle, label='中轨（7日均线）', linewidth=2)
    plt.plot(period_upper.index, period_upper, label='上轨', linewidth=1, linestyle='--')
    plt.plot(period_lower.index, period_lower, label='下轨', linewidth=1, linestyle='--')
    
    plt.fill_between(period_upper.index, period_upper, period_lower, alpha=0.2)
    
    plt.title(f'{sample_period} 销售额布林带')
    plt.xlabel('日期')
    plt.ylabel('销售额')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    # 创建结果DataFrame
    rolling_results = pd.DataFrame({
        '原始销售额': sales,
        '7日移动平均': sales_ma7,
        '30日移动平均': sales_ma30,
        '指数加权移动平均': sales_ewm,
        '7日移动标准差': sales_std7,
        '布林带上轨': bollinger_upper,
        '布林带下轨': bollinger_lower
    })
    
    return rolling_results


def seasonal_analysis(ts_data):
    """
    季节性分析
    """
    print("\n=== 季节性分析 ===")
    
    sales = ts_data['销售额'].copy()
    
    # 1. 基本季节性统计
    print("\n1. 基本季节性统计：")
    
    # 按月份统计
    monthly_stats = sales.groupby(sales.index.month).agg({
        '平均销售额': 'mean',
        '总销售额': 'sum',
        '标准差': 'std',
        '最大值': 'max',
        '最小值': 'min'
    }).round(2)
    
    monthly_stats.index = ['1月', '2月', '3月', '4月', '5月', '6月',
                          '7月', '8月', '9月', '10月', '11月', '12月']
    
    print("月度销售统计:")
    print(monthly_stats)
    
    # 按星期几统计
    weekday_stats = sales.groupby(sales.index.dayofweek).agg({
        '平均销售额': 'mean',
        '总销售额': 'sum',
        '标准差': 'std'
    }).round(2)
    
    weekday_stats.index = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    
    print("\n星期销售统计:")
    print(weekday_stats)
    
    # 2. 季节性分解
    print("\n2. 简单季节性分解：")
    
    # 计算趋势（使用长期移动平均）
    trend = sales.rolling(window=365, center=True).mean()
    
    # 计算季节性（去除趋势后的周期性模式）
    detrended = sales - trend
    seasonal = detrended.groupby(detrended.index.dayofyear).transform('mean')
    
    # 计算残差
    residual = sales - trend - seasonal
    
    print(f"原始数据均值: {sales.mean():.2f}")
    print(f"趋势均值: {trend.mean():.2f}")
    print(f"季节性均值: {seasonal.mean():.2f}")
    print(f"残差均值: {residual.mean():.2f}")
    
    # 3. 季节性可视化
    print("\n3. 季节性可视化：")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle('季节性分析', fontsize=16)
    
    # 月度模式
    monthly_stats['平均销售额'].plot(kind='bar', ax=axes[0, 0], color='skyblue')
    axes[0, 0].set_title('月度平均销售额')
    axes[0, 0].set_ylabel('销售额')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # 星期模式
    weekday_stats['平均销售额'].plot(kind='bar', ax=axes[0, 1], color='lightgreen')
    axes[0, 1].set_title('星期平均销售额')
    axes[0, 1].set_ylabel('销售额')
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # 季节性分解
    sample_period = '2024-01':'2024-03'
    sample_sales = sales.loc[sample_period]
    sample_trend = trend.loc[sample_period]
    sample_seasonal = seasonal.loc[sample_period]
    
    axes[1, 0].plot(sample_sales.index, sample_sales, label='原始数据', alpha=0.7)
    axes[1, 0].plot(sample_trend.index, sample_trend, label='趋势', linewidth=2)
    axes[1, 0].set_title('原始数据 vs 趋势')
    axes[1, 0].set_ylabel('销售额')
    axes[1, 0].legend()
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    axes[1, 1].plot(sample_seasonal.index, sample_seasonal, label='季节性', color='orange')
    axes[1, 1].set_title('季节性成分')
    axes[1, 1].set_ylabel('销售额偏差')
    axes[1, 1].legend()
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    # 4. 热力图分析
    print("\n4. 季节性热力图：")
    
    # 创建月份-星期几热力图
    pivot_data = sales.groupby([sales.index.month, sales.index.dayofweek]).mean().unstack()
    pivot_data.index = ['1月', '2月', '3月', '4月', '5月', '6月',
                       '7月', '8月', '9月', '10月', '11月', '12月']
    pivot_data.columns = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(pivot_data, annot=True, fmt='.0f', cmap='YlOrRd')
    plt.title('月份-星期几平均销售额热力图')
    plt.ylabel('月份')
    plt.xlabel('星期几')
    plt.tight_layout()
    plt.show()
    
    # 5. 同比分析
    print("\n5. 同比分析：")
    
    # 计算同比增长率（年度对比）
    sales_2023 = sales.loc['2023']
    sales_2024 = sales.loc['2024']
    
    # 按月对比
    monthly_2023 = sales_2023.resample('M').sum()
    monthly_2024 = sales_2024.resample('M').sum()
    
    # 计算同比增长率
    common_months = monthly_2023.index.intersection(monthly_2024.index)
    if len(common_months) > 0:
        yoy_growth = ((monthly_2024.loc[common_months] - monthly_2023.loc[common_months]) / 
                     monthly_2023.loc[common_months] * 100).round(2)
        
        print("月度同比增长率（%）:")
        print(yoy_growth)
    
    return monthly_stats, weekday_stats, trend, seasonal, residual


def time_series_visualization(ts_data, rolling_results):
    """
    时间序列综合可视化
    """
    print("\n=== 时间序列综合可视化 ===")
    
    # 1. 多子图时间序列
    fig, axes = plt.subplots(3, 1, figsize=(16, 12))
    fig.suptitle('时间序列综合分析', fontsize=16)
    
    # 原始数据和移动平均
    sample_period = '2024-01':'2024-06'
    sample_data = ts_data.loc[sample_period]
    sample_rolling = rolling_results.loc[sample_period]
    
    axes[0].plot(sample_data.index, sample_data['销售额'], label='原始销售额', alpha=0.7, linewidth=1)
    axes[0].plot(sample_rolling.index, sample_rolling['7日移动平均'], label='7日移动平均', linewidth=2)
    axes[0].plot(sample_rolling.index, sample_rolling['30日移动平均'], label='30日移动平均', linewidth=2)
    axes[0].set_title('销售额趋势分析')
    axes[0].set_ylabel('销售额')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # 分解成分
    axes[1].plot(sample_data.index, sample_data['趋势'], label='趋势成分', linewidth=2)
    axes[1].plot(sample_data.index, sample_data['年度季节性'], label='年度季节性', linewidth=2)
    axes[1].plot(sample_data.index, sample_data['周度季节性'], label='周度季节性', linewidth=2)
    axes[1].set_title('时间序列分解')
    axes[1].set_ylabel('销售额')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    # 特殊事件影响
    axes[2].plot(sample_data.index, sample_data['销售额'], label='实际销售额', linewidth=2)
    axes[2].plot(sample_data.index, sample_data['趋势'] + sample_data['年度季节性'] + sample_data['周度季节性'], 
                label='预期销售额（无特殊事件）', linewidth=2, linestyle='--')
    
    # 标注特殊事件
    special_events = sample_data[sample_data['特殊事件'] != 0]
    if len(special_events) > 0:
        axes[2].scatter(special_events.index, special_events['销售额'], 
                       color='red', s=100, label='特殊事件', zorder=5)
    
    axes[2].set_title('特殊事件影响分析')
    axes[2].set_ylabel('销售额')
    axes[2].set_xlabel('日期')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)
    
    for ax in axes:
        ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    # 2. 相关性分析图
    print("\n相关性分析：")
    
    # 计算各成分的相关性
    correlation_data = ts_data[['销售额', '趋势', '年度季节性', '周度季节性']]
    correlation_matrix = correlation_data.corr()
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
                square=True, fmt='.3f')
    plt.title('时间序列成分相关性')
    plt.tight_layout()
    plt.show()
    
    print("相关性矩阵:")
    print(correlation_matrix.round(3))


def practical_examples():
    """
    实用案例
    """
    print("\n=== 实用案例 ===")
    
    # 1. 业务日历处理
    print("\n1. 业务日历处理：")
    
    # 创建业务日期范围（排除周末）
    business_days = pd.bdate_range(start='2024-01-01', end='2024-01-31')
    print(f"2024年1月工作日: {len(business_days)} 天")
    print(f"工作日范围: {business_days[0]} 到 {business_days[-1]}")
    
    # 2. 节假日处理
    print("\n2. 节假日处理：")
    
    # 定义中国主要节假日
    holidays = [
        '2024-01-01',  # 元旦
        '2024-02-10', '2024-02-11', '2024-02-12',  # 春节
        '2024-04-04', '2024-04-05', '2024-04-06',  # 清明节
        '2024-05-01', '2024-05-02', '2024-05-03',  # 劳动节
        '2024-06-10',  # 端午节
        '2024-09-15', '2024-09-16', '2024-09-17',  # 中秋节
        '2024-10-01', '2024-10-02', '2024-10-03',  # 国庆节
    ]
    
    holiday_dates = pd.to_datetime(holidays)
    
    # 创建包含节假日信息的日期范围
    date_range = pd.date_range('2024-01-01', '2024-12-31', freq='D')
    is_holiday = date_range.isin(holiday_dates)
    is_weekend = date_range.dayofweek >= 5
    is_workday = ~(is_holiday | is_weekend)
    
    calendar_info = pd.DataFrame({
        '日期': date_range,
        '是否节假日': is_holiday,
        '是否周末': is_weekend,
        '是否工作日': is_workday
    })
    
    print(f"2024年总天数: {len(date_range)}")
    print(f"工作日: {is_workday.sum()} 天")
    print(f"周末: {is_weekend.sum()} 天")
    print(f"节假日: {is_holiday.sum()} 天")
    
    # 3. 时间序列预测准备
    print("\n3. 时间序列预测数据准备：")
    
    # 创建滞后特征
    sample_ts = pd.Series(
        np.random.randn(100).cumsum(),
        index=pd.date_range('2024-01-01', periods=100, freq='D')
    )
    
    # 创建特征矩阵
    features = pd.DataFrame({
        '值': sample_ts,
        '滞后1': sample_ts.shift(1),
        '滞后7': sample_ts.shift(7),
        '7日均值': sample_ts.rolling(7).mean(),
        '7日标准差': sample_ts.rolling(7).std(),
        '月份': sample_ts.index.month,
        '星期几': sample_ts.index.dayofweek,
        '是否月初': (sample_ts.index.day <= 5).astype(int),
        '是否月末': (sample_ts.index.day >= 25).astype(int)
    })
    
    print("预测特征矩阵:")
    print(features.head(10))
    
    return calendar_info, features


def main():
    """
    主函数
    """
    print("Pandas时间序列处理完整教程")
    print("=" * 60)
    
    # 1. 创建时间序列数据
    ts_data = create_time_series_data()
    
    # 2. 日期时间操作
    dates = datetime_operations()
    
    # 3. 时间序列索引
    january_data, weekend_data = time_series_indexing(ts_data)
    
    # 4. 重采样操作
    weekly_data, monthly_data, interpolated_data = resampling_operations(ts_data)
    
    # 5. 滑动窗口操作
    rolling_results = rolling_operations(ts_data)
    
    # 6. 季节性分析
    monthly_stats, weekday_stats, trend, seasonal, residual = seasonal_analysis(ts_data)
    
    # 7. 综合可视化
    time_series_visualization(ts_data, rolling_results)
    
    # 8. 实用案例
    calendar_info, features = practical_examples()
    
    print("\n" + "=" * 60)
    print("时间序列处理教程完成！")
    print("=" * 60)
    
    print("\n学习要点总结：")
    print("1. 时间序列创建和索引操作")
    print("2. 日期时间数据的解析和格式化")
    print("3. 重采样：升采样和降采样")
    print("4. 滑动窗口计算：移动平均、标准差等")
    print("5. 季节性分析和分解")
    print("6. 时间序列可视化技巧")
    print("7. 业务日历和节假日处理")
    print("8. 预测建模的数据准备")


if __name__ == "__main__":
    main()