#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据分析示例

本文件演示使用Pandas进行数据分析的常用技术，包括：
- 描述性统计分析
- 分组聚合分析
- 相关性分析
- 数据透视表
- 趋势分析
- 客户细分分析

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


def create_sample_data():
    """
    创建用于分析的示例数据集
    """
    print("=== 创建示例数据集 ===")
    
    np.random.seed(42)
    
    # 创建客户数据
    n_customers = 1000
    
    # 基础客户信息
    customers = pd.DataFrame({
        '客户ID': range(1, n_customers + 1),
        '年龄': np.random.normal(35, 12, n_customers).astype(int),
        '性别': np.random.choice(['男', '女'], n_customers),
        '城市': np.random.choice(['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉'], n_customers, 
                              p=[0.2, 0.18, 0.15, 0.12, 0.1, 0.15, 0.1]),
        '教育程度': np.random.choice(['高中', '本科', '硕士', '博士'], n_customers, 
                                p=[0.3, 0.5, 0.15, 0.05]),
        '职业': np.random.choice(['技术', '销售', '管理', '教育', '医疗', '其他'], n_customers,
                              p=[0.25, 0.2, 0.15, 0.1, 0.1, 0.2]),
        '注册日期': pd.date_range('2020-01-01', periods=n_customers, freq='D')[:n_customers]
    })
    
    # 根据特征生成收入（添加一些相关性）
    base_income = 30000
    age_factor = (customers['年龄'] - 25) * 800
    education_factor = customers['教育程度'].map({'高中': 0, '本科': 15000, '硕士': 30000, '博士': 50000})
    city_factor = customers['城市'].map({'北京': 20000, '上海': 18000, '广州': 12000, 
                                      '深圳': 15000, '杭州': 13000, '成都': 8000, '武汉': 7000})
    
    customers['年收入'] = (base_income + age_factor + education_factor + city_factor + 
                        np.random.normal(0, 10000, n_customers)).clip(20000, 200000)
    
    # 创建交易数据
    n_transactions = 5000
    transactions = pd.DataFrame({
        '交易ID': range(1, n_transactions + 1),
        '客户ID': np.random.choice(customers['客户ID'], n_transactions),
        '交易日期': pd.date_range('2023-01-01', '2024-12-31', periods=n_transactions),
        '产品类别': np.random.choice(['电子产品', '服装', '食品', '家居', '图书', '运动'], n_transactions),
        '交易金额': np.random.lognormal(6, 1, n_transactions),
        '支付方式': np.random.choice(['信用卡', '支付宝', '微信', '现金'], n_transactions,
                                p=[0.4, 0.3, 0.25, 0.05])
    })
    
    # 合并数据
    data = transactions.merge(customers, on='客户ID', how='left')
    
    print(f"生成数据集：{len(customers)} 个客户，{len(transactions)} 笔交易")
    print(f"合并后数据形状：{data.shape}")
    
    return data, customers, transactions


def descriptive_analysis(data):
    """
    描述性统计分析
    """
    print("\n=== 描述性统计分析 ===")
    
    # 1. 基本统计信息
    print("\n1. 数值变量基本统计：")
    numeric_cols = ['年龄', '年收入', '交易金额']
    desc_stats = data[numeric_cols].describe()
    print(desc_stats)
    
    # 2. 分类变量统计
    print("\n2. 分类变量分布：")
    categorical_cols = ['性别', '城市', '教育程度', '职业', '产品类别', '支付方式']
    
    for col in categorical_cols:
        print(f"\n{col}分布：")
        value_counts = data[col].value_counts()
        percentages = data[col].value_counts(normalize=True) * 100
        
        result = pd.DataFrame({
            '数量': value_counts,
            '比例(%)': percentages.round(2)
        })
        print(result)
    
    # 3. 缺失值检查
    print("\n3. 缺失值统计：")
    missing_stats = pd.DataFrame({
        '缺失数量': data.isnull().sum(),
        '缺失比例(%)': (data.isnull().sum() / len(data) * 100).round(2)
    })
    missing_stats = missing_stats[missing_stats['缺失数量'] > 0]
    if len(missing_stats) > 0:
        print(missing_stats)
    else:
        print("无缺失值")
    
    # 4. 数据分布可视化
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('数据分布分析', fontsize=16)
    
    # 年龄分布
    data['年龄'].hist(bins=30, ax=axes[0, 0], alpha=0.7, color='skyblue')
    axes[0, 0].set_title('年龄分布')
    axes[0, 0].set_xlabel('年龄')
    axes[0, 0].set_ylabel('频数')
    
    # 收入分布
    data['年收入'].hist(bins=30, ax=axes[0, 1], alpha=0.7, color='lightgreen')
    axes[0, 1].set_title('年收入分布')
    axes[0, 1].set_xlabel('年收入')
    axes[0, 1].set_ylabel('频数')
    
    # 交易金额分布（对数尺度）
    np.log(data['交易金额']).hist(bins=30, ax=axes[1, 0], alpha=0.7, color='orange')
    axes[1, 0].set_title('交易金额分布（对数）')
    axes[1, 0].set_xlabel('log(交易金额)')
    axes[1, 0].set_ylabel('频数')
    
    # 城市分布
    city_counts = data['城市'].value_counts()
    city_counts.plot(kind='bar', ax=axes[1, 1], color='lightcoral')
    axes[1, 1].set_title('城市分布')
    axes[1, 1].set_xlabel('城市')
    axes[1, 1].set_ylabel('交易数量')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    return desc_stats


def groupby_analysis(data):
    """
    分组聚合分析
    """
    print("\n=== 分组聚合分析 ===")
    
    # 1. 按城市分组分析
    print("\n1. 按城市分组分析：")
    city_analysis = data.groupby('城市').agg({
        '交易金额': ['count', 'sum', 'mean', 'median'],
        '年收入': 'mean',
        '年龄': 'mean',
        '客户ID': 'nunique'
    }).round(2)
    
    # 重命名列
    city_analysis.columns = ['交易次数', '总交易额', '平均交易额', '中位交易额', 
                           '平均年收入', '平均年龄', '客户数量']
    city_analysis = city_analysis.sort_values('总交易额', ascending=False)
    print(city_analysis)
    
    # 2. 按性别和教育程度分组
    print("\n2. 按性别和教育程度分组：")
    gender_edu_analysis = data.groupby(['性别', '教育程度']).agg({
        '交易金额': ['mean', 'count'],
        '年收入': 'mean'
    }).round(2)
    
    gender_edu_analysis.columns = ['平均交易额', '交易次数', '平均年收入']
    print(gender_edu_analysis)
    
    # 3. 按产品类别分析
    print("\n3. 按产品类别分析：")
    product_analysis = data.groupby('产品类别').agg({
        '交易金额': ['count', 'sum', 'mean'],
        '客户ID': 'nunique'
    }).round(2)
    
    product_analysis.columns = ['交易次数', '总销售额', '平均交易额', '客户数量']
    product_analysis['市场份额(%)'] = (product_analysis['总销售额'] / 
                                   product_analysis['总销售额'].sum() * 100).round(2)
    product_analysis = product_analysis.sort_values('总销售额', ascending=False)
    print(product_analysis)
    
    # 4. 按年龄段分析
    print("\n4. 按年龄段分析：")
    data['年龄段'] = pd.cut(data['年龄'], 
                        bins=[0, 25, 35, 45, 55, 100], 
                        labels=['25岁以下', '25-35岁', '35-45岁', '45-55岁', '55岁以上'])
    
    age_analysis = data.groupby('年龄段').agg({
        '交易金额': ['count', 'mean', 'sum'],
        '年收入': 'mean',
        '客户ID': 'nunique'
    }).round(2)
    
    age_analysis.columns = ['交易次数', '平均交易额', '总交易额', '平均年收入', '客户数量']
    print(age_analysis)
    
    # 可视化分组分析结果
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('分组分析结果', fontsize=16)
    
    # 城市总交易额
    city_analysis['总交易额'].plot(kind='bar', ax=axes[0, 0], color='skyblue')
    axes[0, 0].set_title('各城市总交易额')
    axes[0, 0].set_ylabel('交易额')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # 产品类别市场份额
    product_analysis['市场份额(%)'].plot(kind='pie', ax=axes[0, 1], autopct='%1.1f%%')
    axes[0, 1].set_title('产品类别市场份额')
    
    # 年龄段平均交易额
    age_analysis['平均交易额'].plot(kind='bar', ax=axes[1, 0], color='lightgreen')
    axes[1, 0].set_title('各年龄段平均交易额')
    axes[1, 0].set_ylabel('平均交易额')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # 性别教育程度热力图
    gender_edu_pivot = data.pivot_table(values='交易金额', 
                                       index='性别', 
                                       columns='教育程度', 
                                       aggfunc='mean')
    sns.heatmap(gender_edu_pivot, annot=True, fmt='.0f', ax=axes[1, 1], cmap='YlOrRd')
    axes[1, 1].set_title('性别-教育程度平均交易额热力图')
    
    plt.tight_layout()
    plt.show()
    
    return city_analysis, product_analysis, age_analysis


def correlation_analysis(data):
    """
    相关性分析
    """
    print("\n=== 相关性分析 ===")
    
    # 1. 数值变量相关性
    print("\n1. 数值变量相关性矩阵：")
    numeric_vars = ['年龄', '年收入', '交易金额']
    correlation_matrix = data[numeric_vars].corr()
    print(correlation_matrix.round(3))
    
    # 2. 相关性可视化
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                square=True, fmt='.3f')
    plt.title('数值变量相关性热力图')
    plt.show()
    
    # 3. 散点图矩阵
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('变量关系散点图', fontsize=16)
    
    # 年龄 vs 年收入
    axes[0, 0].scatter(data['年龄'], data['年收入'], alpha=0.5)
    axes[0, 0].set_xlabel('年龄')
    axes[0, 0].set_ylabel('年收入')
    axes[0, 0].set_title('年龄 vs 年收入')
    
    # 年收入 vs 交易金额
    axes[0, 1].scatter(data['年收入'], data['交易金额'], alpha=0.5)
    axes[0, 1].set_xlabel('年收入')
    axes[0, 1].set_ylabel('交易金额')
    axes[0, 1].set_title('年收入 vs 交易金额')
    
    # 年龄 vs 交易金额
    axes[1, 0].scatter(data['年龄'], data['交易金额'], alpha=0.5)
    axes[1, 0].set_xlabel('年龄')
    axes[1, 0].set_ylabel('交易金额')
    axes[1, 0].set_title('年龄 vs 交易金额')
    
    # 按性别分组的年收入 vs 交易金额
    for gender in data['性别'].unique():
        gender_data = data[data['性别'] == gender]
        axes[1, 1].scatter(gender_data['年收入'], gender_data['交易金额'], 
                          alpha=0.5, label=gender)
    axes[1, 1].set_xlabel('年收入')
    axes[1, 1].set_ylabel('交易金额')
    axes[1, 1].set_title('年收入 vs 交易金额（按性别）')
    axes[1, 1].legend()
    
    plt.tight_layout()
    plt.show()
    
    # 4. 分类变量与数值变量的关系
    print("\n4. 分类变量对交易金额的影响：")
    
    categorical_vars = ['性别', '教育程度', '职业', '产品类别']
    
    for var in categorical_vars:
        print(f"\n{var}对交易金额的影响：")
        group_stats = data.groupby(var)['交易金额'].agg(['mean', 'std', 'count']).round(2)
        print(group_stats)
    
    return correlation_matrix


def pivot_table_analysis(data):
    """
    数据透视表分析
    """
    print("\n=== 数据透视表分析 ===")
    
    # 1. 城市-产品类别透视表
    print("\n1. 城市-产品类别销售额透视表：")
    city_product_pivot = pd.pivot_table(
        data,
        values='交易金额',
        index='城市',
        columns='产品类别',
        aggfunc='sum',
        fill_value=0
    ).round(0)
    
    print(city_product_pivot)
    
    # 2. 性别-年龄段-教育程度多维透视表
    print("\n2. 性别-年龄段平均交易额透视表：")
    gender_age_pivot = pd.pivot_table(
        data,
        values='交易金额',
        index='性别',
        columns='年龄段',
        aggfunc='mean',
        fill_value=0
    ).round(2)
    
    print(gender_age_pivot)
    
    # 3. 支付方式-产品类别交易次数透视表
    print("\n3. 支付方式-产品类别交易次数透视表：")
    payment_product_pivot = pd.pivot_table(
        data,
        values='交易ID',
        index='支付方式',
        columns='产品类别',
        aggfunc='count',
        fill_value=0
    )
    
    print(payment_product_pivot)
    
    # 4. 透视表可视化
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('数据透视表可视化', fontsize=16)
    
    # 城市-产品类别热力图
    sns.heatmap(city_product_pivot, annot=True, fmt='.0f', ax=axes[0, 0], cmap='Blues')
    axes[0, 0].set_title('城市-产品类别销售额热力图')
    
    # 性别-年龄段热力图
    sns.heatmap(gender_age_pivot, annot=True, fmt='.2f', ax=axes[0, 1], cmap='Greens')
    axes[0, 1].set_title('性别-年龄段平均交易额热力图')
    
    # 支付方式-产品类别堆叠柱状图
    payment_product_pivot.plot(kind='bar', stacked=True, ax=axes[1, 0])
    axes[1, 0].set_title('支付方式-产品类别交易次数')
    axes[1, 0].set_ylabel('交易次数')
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # 城市销售额对比
    city_total = city_product_pivot.sum(axis=1).sort_values(ascending=False)
    city_total.plot(kind='bar', ax=axes[1, 1], color='orange')
    axes[1, 1].set_title('各城市总销售额')
    axes[1, 1].set_ylabel('销售额')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    return city_product_pivot, gender_age_pivot, payment_product_pivot


def time_series_analysis(data):
    """
    时间序列分析
    """
    print("\n=== 时间序列分析 ===")
    
    # 1. 按日期聚合
    print("\n1. 时间趋势分析：")
    
    # 按日聚合
    daily_sales = data.groupby(data['交易日期'].dt.date).agg({
        '交易金额': ['sum', 'count', 'mean']
    }).round(2)
    daily_sales.columns = ['日销售额', '日交易次数', '日平均交易额']
    
    # 按月聚合
    monthly_sales = data.groupby(data['交易日期'].dt.to_period('M')).agg({
        '交易金额': ['sum', 'count', 'mean'],
        '客户ID': 'nunique'
    }).round(2)
    monthly_sales.columns = ['月销售额', '月交易次数', '月平均交易额', '月活跃客户数']
    
    print("月度销售统计：")
    print(monthly_sales.head(10))
    
    # 2. 季节性分析
    print("\n2. 季节性分析：")
    data['月份'] = data['交易日期'].dt.month
    data['季度'] = data['交易日期'].dt.quarter
    data['星期几'] = data['交易日期'].dt.dayofweek
    
    # 按月份分析
    monthly_pattern = data.groupby('月份')['交易金额'].agg(['sum', 'mean', 'count']).round(2)
    monthly_pattern.columns = ['总销售额', '平均交易额', '交易次数']
    print("\n月份销售模式：")
    print(monthly_pattern)
    
    # 按星期几分析
    weekday_pattern = data.groupby('星期几')['交易金额'].agg(['sum', 'mean', 'count']).round(2)
    weekday_pattern.columns = ['总销售额', '平均交易额', '交易次数']
    weekday_pattern.index = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    print("\n星期销售模式：")
    print(weekday_pattern)
    
    # 3. 时间序列可视化
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle('时间序列分析', fontsize=16)
    
    # 日销售额趋势
    daily_sales['日销售额'].plot(ax=axes[0, 0], color='blue', alpha=0.7)
    axes[0, 0].set_title('日销售额趋势')
    axes[0, 0].set_ylabel('销售额')
    
    # 月销售额趋势
    monthly_sales['月销售额'].plot(ax=axes[0, 1], color='green', marker='o')
    axes[0, 1].set_title('月销售额趋势')
    axes[0, 1].set_ylabel('销售额')
    
    # 月份销售模式
    monthly_pattern['总销售额'].plot(kind='bar', ax=axes[1, 0], color='orange')
    axes[1, 0].set_title('各月份销售额')
    axes[1, 0].set_ylabel('销售额')
    axes[1, 0].tick_params(axis='x', rotation=0)
    
    # 星期销售模式
    weekday_pattern['总销售额'].plot(kind='bar', ax=axes[1, 1], color='red')
    axes[1, 1].set_title('各星期销售额')
    axes[1, 1].set_ylabel('销售额')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    # 4. 移动平均和趋势
    print("\n4. 趋势分析：")
    daily_sales['7日移动平均'] = daily_sales['日销售额'].rolling(window=7).mean()
    daily_sales['30日移动平均'] = daily_sales['日销售额'].rolling(window=30).mean()
    
    plt.figure(figsize=(14, 6))
    plt.plot(daily_sales.index, daily_sales['日销售额'], alpha=0.3, label='日销售额')
    plt.plot(daily_sales.index, daily_sales['7日移动平均'], label='7日移动平均')
    plt.plot(daily_sales.index, daily_sales['30日移动平均'], label='30日移动平均')
    plt.title('销售额趋势和移动平均')
    plt.ylabel('销售额')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    return daily_sales, monthly_sales, monthly_pattern, weekday_pattern


def customer_segmentation(data, customers):
    """
    客户细分分析
    """
    print("\n=== 客户细分分析 ===")
    
    # 1. RFM分析（Recency, Frequency, Monetary）
    print("\n1. RFM客户价值分析：")
    
    # 计算每个客户的RFM指标
    current_date = data['交易日期'].max()
    
    customer_rfm = data.groupby('客户ID').agg({
        '交易日期': lambda x: (current_date - x.max()).days,  # Recency
        '交易ID': 'count',  # Frequency
        '交易金额': 'sum'  # Monetary
    }).round(2)
    
    customer_rfm.columns = ['最近购买天数', '购买频次', '总消费金额']
    
    # 计算RFM分数（1-5分）
    customer_rfm['R_Score'] = pd.qcut(customer_rfm['最近购买天数'], 5, labels=[5,4,3,2,1])
    customer_rfm['F_Score'] = pd.qcut(customer_rfm['购买频次'].rank(method='first'), 5, labels=[1,2,3,4,5])
    customer_rfm['M_Score'] = pd.qcut(customer_rfm['总消费金额'], 5, labels=[1,2,3,4,5])
    
    # 计算RFM综合分数
    customer_rfm['RFM_Score'] = (customer_rfm['R_Score'].astype(int) + 
                                customer_rfm['F_Score'].astype(int) + 
                                customer_rfm['M_Score'].astype(int))
    
    print("RFM分析结果（前10名客户）：")
    print(customer_rfm.sort_values('RFM_Score', ascending=False).head(10))
    
    # 2. 客户分层
    print("\n2. 客户分层：")
    
    def rfm_segment(row):
        if row['RFM_Score'] >= 13:
            return '冠军客户'
        elif row['RFM_Score'] >= 11:
            return '忠诚客户'
        elif row['RFM_Score'] >= 9:
            return '潜力客户'
        elif row['RFM_Score'] >= 7:
            return '新客户'
        elif row['RFM_Score'] >= 5:
            return '风险客户'
        else:
            return '流失客户'
    
    customer_rfm['客户分层'] = customer_rfm.apply(rfm_segment, axis=1)
    
    segment_analysis = customer_rfm.groupby('客户分层').agg({
        '最近购买天数': 'mean',
        '购买频次': 'mean',
        '总消费金额': 'mean',
        'RFM_Score': 'count'
    }).round(2)
    
    segment_analysis.columns = ['平均最近购买天数', '平均购买频次', '平均总消费', '客户数量']
    segment_analysis['客户占比(%)'] = (segment_analysis['客户数量'] / 
                                   segment_analysis['客户数量'].sum() * 100).round(2)
    
    print(segment_analysis)
    
    # 3. 客户生命周期价值分析
    print("\n3. 客户生命周期价值分析：")
    
    # 合并客户基本信息
    customer_analysis = customer_rfm.merge(customers[['客户ID', '年龄', '性别', '城市', '教育程度', '年收入']], 
                                         on='客户ID', how='left')
    
    # 按客户分层分析人口统计特征
    demographic_analysis = customer_analysis.groupby('客户分层').agg({
        '年龄': 'mean',
        '年收入': 'mean',
        '性别': lambda x: x.value_counts().index[0],  # 最常见的性别
        '教育程度': lambda x: x.value_counts().index[0]  # 最常见的教育程度
    }).round(2)
    
    print("各客户分层的人口统计特征：")
    print(demographic_analysis)
    
    # 4. 可视化客户细分
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('客户细分分析', fontsize=16)
    
    # 客户分层分布
    segment_counts = customer_rfm['客户分层'].value_counts()
    segment_counts.plot(kind='pie', ax=axes[0, 0], autopct='%1.1f%%')
    axes[0, 0].set_title('客户分层分布')
    
    # RFM散点图
    scatter = axes[0, 1].scatter(customer_rfm['购买频次'], customer_rfm['总消费金额'], 
                                c=customer_rfm['RFM_Score'], cmap='viridis', alpha=0.6)
    axes[0, 1].set_xlabel('购买频次')
    axes[0, 1].set_ylabel('总消费金额')
    axes[0, 1].set_title('购买频次 vs 总消费金额（颜色=RFM分数）')
    plt.colorbar(scatter, ax=axes[0, 1])
    
    # 各分层平均消费
    segment_analysis['平均总消费'].plot(kind='bar', ax=axes[1, 0], color='lightblue')
    axes[1, 0].set_title('各客户分层平均总消费')
    axes[1, 0].set_ylabel('平均总消费')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # 各分层客户数量
    segment_analysis['客户数量'].plot(kind='bar', ax=axes[1, 1], color='lightgreen')
    axes[1, 1].set_title('各客户分层客户数量')
    axes[1, 1].set_ylabel('客户数量')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    return customer_rfm, segment_analysis


def advanced_analysis(data):
    """
    高级分析
    """
    print("\n=== 高级分析 ===")
    
    # 1. 同期群分析（Cohort Analysis）
    print("\n1. 同期群分析：")
    
    # 计算客户首次购买月份
    data['交易年月'] = data['交易日期'].dt.to_period('M')
    customer_first_purchase = data.groupby('客户ID')['交易年月'].min().reset_index()
    customer_first_purchase.columns = ['客户ID', '首次购买月份']
    
    # 合并首次购买信息
    data_with_cohort = data.merge(customer_first_purchase, on='客户ID')
    data_with_cohort['购买周期'] = (data_with_cohort['交易年月'] - 
                                data_with_cohort['首次购买月份']).apply(attrgetter('n'))
    
    # 计算同期群表
    cohort_table = data_with_cohort.groupby(['首次购买月份', '购买周期'])['客户ID'].nunique().reset_index()
    cohort_table = cohort_table.pivot(index='首次购买月份', 
                                     columns='购买周期', 
                                     values='客户ID')
    
    # 计算留存率
    cohort_sizes = data_with_cohort.groupby('首次购买月份')['客户ID'].nunique()
    retention_table = cohort_table.divide(cohort_sizes, axis=0)
    
    print("客户留存率表（前6个月）：")
    print(retention_table.iloc[:, :6].round(3))
    
    # 2. 产品关联分析
    print("\n2. 产品关联分析：")
    
    # 计算产品共现矩阵
    customer_products = data.groupby('客户ID')['产品类别'].apply(list).reset_index()
    
    from itertools import combinations
    
    # 计算产品对的共现次数
    product_pairs = []
    for products in customer_products['产品类别']:
        if len(products) > 1:
            for pair in combinations(set(products), 2):
                product_pairs.append(sorted(pair))
    
    pair_counts = pd.Series([tuple(pair) for pair in product_pairs]).value_counts()
    print("最常见的产品组合（前10）：")
    print(pair_counts.head(10))
    
    # 3. 客户价值预测特征
    print("\n3. 客户价值预测特征：")
    
    # 构建客户特征
    customer_features = data.groupby('客户ID').agg({
        '交易金额': ['sum', 'mean', 'std', 'count'],
        '交易日期': ['min', 'max'],
        '产品类别': lambda x: len(set(x))  # 购买产品类别数
    })
    
    # 扁平化列名
    customer_features.columns = ['总消费', '平均消费', '消费标准差', '交易次数', 
                               '首次购买', '最近购买', '产品类别数']
    
    # 计算客户活跃天数
    customer_features['活跃天数'] = (customer_features['最近购买'] - 
                                  customer_features['首次购买']).dt.days + 1
    
    # 计算平均购买间隔
    customer_features['平均购买间隔'] = customer_features['活跃天数'] / customer_features['交易次数']
    
    print("客户特征统计：")
    print(customer_features[['总消费', '平均消费', '交易次数', '产品类别数', '活跃天数']].describe().round(2))
    
    return retention_table, pair_counts, customer_features


def generate_insights(data, city_analysis, product_analysis, customer_rfm):
    """
    生成业务洞察
    """
    print("\n=== 业务洞察和建议 ===")
    
    # 1. 关键指标总结
    print("\n1. 关键业务指标：")
    total_revenue = data['交易金额'].sum()
    total_transactions = len(data)
    total_customers = data['客户ID'].nunique()
    avg_transaction = data['交易金额'].mean()
    avg_customer_value = total_revenue / total_customers
    
    print(f"总销售额: ¥{total_revenue:,.2f}")
    print(f"总交易次数: {total_transactions:,}")
    print(f"总客户数: {total_customers:,}")
    print(f"平均交易金额: ¥{avg_transaction:.2f}")
    print(f"平均客户价值: ¥{avg_customer_value:.2f}")
    
    # 2. 市场洞察
    print("\n2. 市场洞察：")
    top_city = city_analysis['总交易额'].index[0]
    top_product = product_analysis['总销售额'].index[0]
    
    print(f"• 最有价值的城市市场: {top_city}")
    print(f"• 最受欢迎的产品类别: {top_product}")
    print(f"• 高价值客户占比: {(customer_rfm['客户分层'] == '冠军客户').mean()*100:.1f}%")
    
    # 3. 业务建议
    print("\n3. 业务建议：")
    
    print("\n营销策略建议：")
    print(f"• 重点发展{top_city}市场，该市场贡献了最高的销售额")
    print(f"• 加强{top_product}产品线的推广和库存管理")
    print("• 针对冠军客户制定VIP服务计划")
    print("• 对风险客户和流失客户实施挽回策略")
    
    print("\n产品策略建议：")
    low_performing_products = product_analysis.sort_values('总销售额').head(2).index.tolist()
    print(f"• 评估{low_performing_products}等低表现产品的市场定位")
    print("• 分析高价值客户的产品偏好，开发相关产品")
    
    print("\n客户策略建议：")
    print("• 建立客户分层管理体系")
    print("• 为不同客户群体设计个性化营销方案")
    print("• 提高客户留存率和复购率")
    
    # 4. 风险提示
    print("\n4. 风险提示：")
    risk_customers_pct = (customer_rfm['客户分层'].isin(['风险客户', '流失客户'])).mean() * 100
    print(f"• {risk_customers_pct:.1f}%的客户处于风险或流失状态，需要关注")
    
    if data['交易金额'].std() > data['交易金额'].mean():
        print("• 交易金额波动较大，建议分析异常交易原因")
    
    print("\n数据质量建议：")
    print("• 建立完善的数据收集和清洗流程")
    print("• 定期进行数据质量检查")
    print("• 建立数据驱动的决策机制")


def main():
    """
    主函数
    """
    print("Pandas数据分析完整案例")
    print("=" * 60)
    
    # 1. 创建数据
    data, customers, transactions = create_sample_data()
    
    # 2. 描述性统计分析
    desc_stats = descriptive_analysis(data)
    
    # 3. 分组聚合分析
    city_analysis, product_analysis, age_analysis = groupby_analysis(data)
    
    # 4. 相关性分析
    correlation_matrix = correlation_analysis(data)
    
    # 5. 数据透视表分析
    city_product_pivot, gender_age_pivot, payment_product_pivot = pivot_table_analysis(data)
    
    # 6. 时间序列分析
    daily_sales, monthly_sales, monthly_pattern, weekday_pattern = time_series_analysis(data)
    
    # 7. 客户细分分析
    customer_rfm, segment_analysis = customer_segmentation(data, customers)
    
    # 8. 高级分析
    retention_table, pair_counts, customer_features = advanced_analysis(data)
    
    # 9. 生成业务洞察
    generate_insights(data, city_analysis, product_analysis, customer_rfm)
    
    print("\n" + "=" * 60)
    print("数据分析完成！")
    print("=" * 60)
    
    print("\n分析要点总结：")
    print("1. 描述性统计：了解数据的基本特征")
    print("2. 分组分析：发现不同群体的差异")
    print("3. 相关性分析：识别变量间的关系")
    print("4. 透视表：多维度交叉分析")
    print("5. 时间序列：发现趋势和季节性")
    print("6. 客户细分：识别不同价值的客户群体")
    print("7. 高级分析：深入挖掘业务价值")
    print("8. 业务洞察：将分析结果转化为行动建议")


if __name__ == "__main__":
    from operator import attrgetter
    main()