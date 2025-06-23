#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session13: 数据分析 - Pandas 演示代码

本文件演示了Pandas库的核心功能和实际应用，包括：
- DataFrame和Series的基本操作
- 数据读取和处理
- 数据清洗和分析
- 数据可视化基础

作者: Python教程团队
创建日期: 2024-01-01
最后修改: 2024-01-01
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings

# 忽略警告信息
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 设置随机种子
np.random.seed(42)


def demo_basic_structures():
    """
    演示Pandas基本数据结构
    """
    print("=" * 50)
    print("1. Pandas基本数据结构演示")
    print("=" * 50)
    
    # Series演示
    print("\n--- Series演示 ---")
    cities_population = pd.Series({
        '北京': 2154,
        '上海': 2424,
        '广州': 1491,
        '深圳': 1756,
        '杭州': 1196
    }, name='人口(万人)')
    
    print("城市人口数据:")
    print(cities_population)
    print(f"\n数据类型: {type(cities_population)}")
    print(f"形状: {cities_population.shape}")
    print(f"最大值: {cities_population.max()}")
    print(f"最小值: {cities_population.min()}")
    
    # DataFrame演示
    print("\n--- DataFrame演示 ---")
    employee_data = {
        '员工ID': range(1, 11),
        '姓名': ['张三', '李四', '王五', '赵六', '钱七', 
                '孙八', '周九', '吴十', '郑一', '王二'],
        '部门': ['技术部', '销售部', '技术部', '人事部', '财务部',
                '技术部', '销售部', '技术部', '人事部', '销售部'],
        '年龄': [28, 32, 25, 35, 29, 31, 27, 33, 26, 30],
        '薪资': [12000, 8000, 10000, 9000, 11000, 
                13000, 7500, 14000, 8500, 9500],
        '入职日期': pd.date_range('2020-01-01', periods=10, freq='3M')
    }
    
    df_employees = pd.DataFrame(employee_data)
    print("员工数据:")
    print(df_employees)
    print(f"\n数据形状: {df_employees.shape}")
    print(f"列名: {df_employees.columns.tolist()}")
    print(f"数据类型:\n{df_employees.dtypes}")
    
    return df_employees


def demo_data_operations(df):
    """
    演示数据操作
    """
    print("\n" + "=" * 50)
    print("2. 数据操作演示")
    print("=" * 50)
    
    # 数据选择
    print("\n--- 数据选择 ---")
    print("选择薪资列:")
    print(df['薪资'].head())
    
    print("\n选择多列:")
    print(df[['姓名', '部门', '薪资']].head())
    
    print("\n选择前3行:")
    print(df.head(3))
    
    # 条件筛选
    print("\n--- 条件筛选 ---")
    high_salary = df[df['薪资'] > 10000]
    print("高薪员工:")
    print(high_salary[['姓名', '部门', '薪资']])
    
    tech_dept = df[df['部门'] == '技术部']
    print("\n技术部员工:")
    print(tech_dept[['姓名', '年龄', '薪资']])
    
    # 复合条件
    young_high_salary = df[(df['年龄'] < 30) & (df['薪资'] > 10000)]
    print("\n年轻高薪员工:")
    print(young_high_salary[['姓名', '年龄', '薪资']])
    
    return df


def demo_data_analysis(df):
    """
    演示数据分析
    """
    print("\n" + "=" * 50)
    print("3. 数据分析演示")
    print("=" * 50)
    
    # 基本统计
    print("\n--- 基本统计信息 ---")
    print("数值列统计:")
    print(df.describe())
    
    print("\n各部门员工数量:")
    dept_counts = df['部门'].value_counts()
    print(dept_counts)
    
    # 分组分析
    print("\n--- 分组分析 ---")
    dept_analysis = df.groupby('部门').agg({
        '薪资': ['mean', 'min', 'max', 'count'],
        '年龄': 'mean'
    }).round(2)
    
    print("各部门薪资和年龄分析:")
    print(dept_analysis)
    
    # 相关性分析
    print("\n--- 相关性分析 ---")
    correlation = df[['年龄', '薪资']].corr()
    print("年龄与薪资相关性:")
    print(correlation)
    
    return dept_analysis


def demo_data_cleaning():
    """
    演示数据清洗
    """
    print("\n" + "=" * 50)
    print("4. 数据清洗演示")
    print("=" * 50)
    
    # 创建包含问题的数据
    dirty_data = {
        '姓名': ['张三', '李四', '王五', None, '赵六', '张三'],  # 包含缺失值和重复
        '年龄': [25, 30, None, 28, 35, 25],  # 包含缺失值
        '薪资': [8000, 12000, 10000, 9000, None, 8000],  # 包含缺失值
        '城市': ['北京', '上海', '广州', '深圳', '杭州', '北京']
    }
    
    df_dirty = pd.DataFrame(dirty_data)
    print("原始脏数据:")
    print(df_dirty)
    
    # 检查缺失值
    print("\n--- 缺失值检查 ---")
    print("缺失值统计:")
    print(df_dirty.isnull().sum())
    
    print("\n缺失值比例:")
    print((df_dirty.isnull().sum() / len(df_dirty) * 100).round(2))
    
    # 处理缺失值
    print("\n--- 处理缺失值 ---")
    df_cleaned = df_dirty.copy()
    
    # 删除姓名为空的行
    df_cleaned = df_cleaned.dropna(subset=['姓名'])
    
    # 用均值填充年龄
    df_cleaned['年龄'].fillna(df_cleaned['年龄'].mean(), inplace=True)
    
    # 用中位数填充薪资
    df_cleaned['薪资'].fillna(df_cleaned['薪资'].median(), inplace=True)
    
    print("处理缺失值后:")
    print(df_cleaned)
    
    # 处理重复值
    print("\n--- 处理重复值 ---")
    print(f"重复行数量: {df_cleaned.duplicated().sum()}")
    
    df_final = df_cleaned.drop_duplicates()
    print("\n删除重复值后:")
    print(df_final)
    
    return df_final


def demo_time_series():
    """
    演示时间序列处理
    """
    print("\n" + "=" * 50)
    print("5. 时间序列处理演示")
    print("=" * 50)
    
    # 创建时间序列数据
    dates = pd.date_range('2024-01-01', periods=90, freq='D')
    sales_data = {
        '日期': dates,
        '销量': np.random.randint(50, 200, 90) + 
                10 * np.sin(np.arange(90) * 2 * np.pi / 7),  # 添加周期性
        '价格': np.random.uniform(10, 50, 90)
    }
    
    df_sales = pd.DataFrame(sales_data)
    df_sales.set_index('日期', inplace=True)
    
    print("销售数据前10天:")
    print(df_sales.head(10))
    
    # 时间序列分析
    print("\n--- 时间序列分析 ---")
    
    # 按月汇总
    monthly_sales = df_sales.resample('M').agg({
        '销量': 'sum',
        '价格': 'mean'
    }).round(2)
    
    print("按月汇总:")
    print(monthly_sales)
    
    # 计算移动平均
    df_sales['销量_7日均值'] = df_sales['销量'].rolling(window=7).mean()
    df_sales['销量_30日均值'] = df_sales['销量'].rolling(window=30).mean()
    
    print("\n添加移动平均后（前15天）:")
    print(df_sales.head(15))
    
    # 提取日期特征
    df_sales['年'] = df_sales.index.year
    df_sales['月'] = df_sales.index.month
    df_sales['星期几'] = df_sales.index.dayofweek
    df_sales['是否周末'] = df_sales['星期几'].isin([5, 6])
    
    # 按星期几分析
    weekday_analysis = df_sales.groupby('星期几')['销量'].mean()
    print("\n各星期几平均销量:")
    weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    for i, day in enumerate(weekdays):
        print(f"{day}: {weekday_analysis[i]:.1f}")
    
    return df_sales


def demo_visualization(df_employees, df_sales):
    """
    演示数据可视化
    """
    print("\n" + "=" * 50)
    print("6. 数据可视化演示")
    print("=" * 50)
    
    # 创建图表
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Pandas数据可视化演示', fontsize=16)
    
    # 1. 部门薪资分布
    dept_salary = df_employees.groupby('部门')['薪资'].mean()
    dept_salary.plot(kind='bar', ax=axes[0, 0], color='skyblue')
    axes[0, 0].set_title('各部门平均薪资')
    axes[0, 0].set_ylabel('薪资(元)')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # 2. 年龄分布直方图
    df_employees['年龄'].hist(bins=8, ax=axes[0, 1], color='lightgreen', alpha=0.7)
    axes[0, 1].set_title('员工年龄分布')
    axes[0, 1].set_xlabel('年龄')
    axes[0, 1].set_ylabel('人数')
    
    # 3. 销量趋势图
    df_sales['销量'].plot(ax=axes[1, 0], color='orange', alpha=0.7, label='日销量')
    df_sales['销量_7日均值'].plot(ax=axes[1, 0], color='red', label='7日均值')
    axes[1, 0].set_title('销量趋势')
    axes[1, 0].set_ylabel('销量')
    axes[1, 0].legend()
    
    # 4. 年龄与薪资散点图
    axes[1, 1].scatter(df_employees['年龄'], df_employees['薪资'], 
                      c=df_employees['部门'].astype('category').cat.codes, 
                      cmap='viridis', alpha=0.7)
    axes[1, 1].set_title('年龄与薪资关系')
    axes[1, 1].set_xlabel('年龄')
    axes[1, 1].set_ylabel('薪资(元)')
    
    plt.tight_layout()
    plt.show()
    
    print("图表已显示，包含：")
    print("1. 各部门平均薪资柱状图")
    print("2. 员工年龄分布直方图")
    print("3. 销量趋势线图")
    print("4. 年龄与薪资散点图")


def demo_advanced_operations():
    """
    演示高级操作
    """
    print("\n" + "=" * 50)
    print("7. 高级操作演示")
    print("=" * 50)
    
    # 创建两个相关的DataFrame进行合并演示
    df1 = pd.DataFrame({
        '员工ID': [1, 2, 3, 4, 5],
        '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
        '部门': ['技术部', '销售部', '技术部', '人事部', '财务部']
    })
    
    df2 = pd.DataFrame({
        '员工ID': [1, 2, 3, 6, 7],
        '薪资': [12000, 8000, 10000, 9000, 11000],
        '绩效': ['优秀', '良好', '优秀', '一般', '良好']
    })
    
    print("\n--- 数据合并演示 ---")
    print("员工基本信息:")
    print(df1)
    print("\n员工薪资信息:")
    print(df2)
    
    # 内连接
    inner_join = pd.merge(df1, df2, on='员工ID', how='inner')
    print("\n内连接结果:")
    print(inner_join)
    
    # 左连接
    left_join = pd.merge(df1, df2, on='员工ID', how='left')
    print("\n左连接结果:")
    print(left_join)
    
    # 数据透视表
    print("\n--- 数据透视表演示 ---")
    # 创建更复杂的数据
    sales_detail = pd.DataFrame({
        '日期': pd.date_range('2024-01-01', periods=20, freq='D'),
        '产品': np.random.choice(['产品A', '产品B', '产品C'], 20),
        '地区': np.random.choice(['北区', '南区', '东区', '西区'], 20),
        '销量': np.random.randint(10, 100, 20),
        '金额': np.random.randint(1000, 10000, 20)
    })
    
    pivot_table = pd.pivot_table(
        sales_detail,
        values='金额',
        index='产品',
        columns='地区',
        aggfunc='sum',
        fill_value=0
    )
    
    print("销售数据透视表:")
    print(pivot_table)
    
    # 交叉表
    crosstab = pd.crosstab(
        sales_detail['产品'], 
        sales_detail['地区'], 
        values=sales_detail['销量'],
        aggfunc='sum',
        fill_value=0
    )
    
    print("\n产品地区销量交叉表:")
    print(crosstab)
    
    return pivot_table


def demo_performance_tips():
    """
    演示性能优化技巧
    """
    print("\n" + "=" * 50)
    print("8. 性能优化技巧演示")
    print("=" * 50)
    
    # 创建大数据集
    n_rows = 10000
    large_data = {
        'ID': range(n_rows),
        '类别': np.random.choice(['A', 'B', 'C', 'D'], n_rows),
        '数值1': np.random.randn(n_rows),
        '数值2': np.random.randn(n_rows),
        '文本': np.random.choice(['文本1', '文本2', '文本3'], n_rows)
    }
    
    df_large = pd.DataFrame(large_data)
    
    print(f"原始数据内存使用: {df_large.memory_usage(deep=True).sum():,} bytes")
    
    # 优化数据类型
    df_optimized = df_large.copy()
    df_optimized['类别'] = df_optimized['类别'].astype('category')
    df_optimized['文本'] = df_optimized['文本'].astype('category')
    
    print(f"优化后内存使用: {df_optimized.memory_usage(deep=True).sum():,} bytes")
    
    memory_saved = df_large.memory_usage(deep=True).sum() - df_optimized.memory_usage(deep=True).sum()
    print(f"节省内存: {memory_saved:,} bytes ({memory_saved/df_large.memory_usage(deep=True).sum()*100:.1f}%)")
    
    # 使用query方法
    print("\n--- 高效筛选方法 ---")
    # 传统方法
    result1 = df_optimized[(df_optimized['类别'] == 'A') & (df_optimized['数值1'] > 0)]
    
    # query方法
    result2 = df_optimized.query('类别 == "A" and 数值1 > 0')
    
    print(f"传统筛选结果: {len(result1)} 行")
    print(f"Query筛选结果: {len(result2)} 行")
    print("Query方法代码更简洁，在大数据集上通常更快")
    
    # 链式操作
    print("\n--- 链式操作演示 ---")
    result = (df_optimized
              .query('数值1 > 0')
              .groupby('类别')
              .agg({'数值1': 'mean', '数值2': 'sum'})
              .round(3)
              .sort_values('数值1', ascending=False))
    
    print("链式操作结果:")
    print(result)


def main():
    """
    主函数：演示程序的入口点
    """
    print("Session13: 数据分析 - Pandas 完整演示")
    print("=" * 60)
    print("本演示将展示Pandas库的核心功能和实际应用")
    print("包括数据结构、操作、分析、清洗、可视化等")
    print("=" * 60)
    
    try:
        # 1. 基本数据结构
        df_employees = demo_basic_structures()
        
        # 2. 数据操作
        demo_data_operations(df_employees)
        
        # 3. 数据分析
        demo_data_analysis(df_employees)
        
        # 4. 数据清洗
        demo_data_cleaning()
        
        # 5. 时间序列处理
        df_sales = demo_time_series()
        
        # 6. 数据可视化
        demo_visualization(df_employees, df_sales)
        
        # 7. 高级操作
        demo_advanced_operations()
        
        # 8. 性能优化
        demo_performance_tips()
        
        print("\n" + "=" * 60)
        print("演示完成！")
        print("=" * 60)
        print("\n学习要点总结：")
        print("1. Pandas提供了强大的数据结构：Series和DataFrame")
        print("2. 支持多种数据格式的读写操作")
        print("3. 提供了丰富的数据选择和筛选方法")
        print("4. 内置强大的数据分析和统计功能")
        print("5. 数据清洗是数据分析的重要环节")
        print("6. 时间序列处理功能完善")
        print("7. 与Matplotlib集成，支持数据可视化")
        print("8. 注意性能优化，合理使用数据类型")
        print("\n继续学习建议：")
        print("- 多练习真实数据集的处理")
        print("- 学习更多可视化库（Seaborn、Plotly）")
        print("- 掌握数据库操作和大数据处理")
        print("- 学习机器学习相关库")
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        print("请检查是否正确安装了所需的库：pandas, numpy, matplotlib")


if __name__ == "__main__":
    main()