#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据清洗示例

本文件演示常见的数据清洗技术，包括：
- 处理缺失值
- 处理重复值
- 数据类型转换
- 异常值检测和处理
- 数据标准化

作者: Python教程团队
创建日期: 2024-01-01
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def create_dirty_data():
    """
    创建包含各种数据质量问题的示例数据
    """
    print("=== 创建包含数据质量问题的示例数据 ===")
    
    np.random.seed(42)
    
    # 创建基础数据
    n_rows = 100
    data = {
        '客户ID': range(1, n_rows + 1),
        '姓名': [f'客户{i}' for i in range(1, n_rows + 1)],
        '年龄': np.random.randint(18, 80, n_rows),
        '收入': np.random.normal(50000, 20000, n_rows),
        '消费金额': np.random.normal(5000, 2000, n_rows),
        '注册日期': pd.date_range('2020-01-01', periods=n_rows, freq='3D'),
        '城市': np.random.choice(['北京', '上海', '广州', '深圳', '杭州'], n_rows),
        '性别': np.random.choice(['男', '女'], n_rows),
        '电话': [f'138{np.random.randint(10000000, 99999999)}' for _ in range(n_rows)]
    }
    
    df = pd.DataFrame(data)
    
    # 引入数据质量问题
    
    # 1. 缺失值
    missing_indices = np.random.choice(df.index, 15, replace=False)
    df.loc[missing_indices, '年龄'] = np.nan
    
    missing_indices = np.random.choice(df.index, 20, replace=False)
    df.loc[missing_indices, '收入'] = np.nan
    
    missing_indices = np.random.choice(df.index, 10, replace=False)
    df.loc[missing_indices, '姓名'] = np.nan
    
    # 2. 重复数据
    duplicate_rows = df.iloc[:5].copy()
    df = pd.concat([df, duplicate_rows], ignore_index=True)
    
    # 3. 异常值
    df.loc[df.index[5], '年龄'] = 150  # 异常年龄
    df.loc[df.index[10], '收入'] = -10000  # 负收入
    df.loc[df.index[15], '消费金额'] = 100000  # 异常消费
    
    # 4. 数据类型问题
    df.loc[df.index[20], '年龄'] = '25岁'  # 字符串年龄
    df.loc[df.index[25], '收入'] = '50000元'  # 字符串收入
    
    # 5. 格式不一致
    df.loc[df.index[30], '性别'] = 'M'  # 不一致的性别表示
    df.loc[df.index[35], '性别'] = 'F'
    df.loc[df.index[40], '城市'] = '北京市'  # 不一致的城市名称
    df.loc[df.index[45], '城市'] = '上海市'
    
    # 6. 电话号码格式问题
    df.loc[df.index[50], '电话'] = '138-1234-5678'
    df.loc[df.index[55], '电话'] = '138 1234 5678'
    df.loc[df.index[60], '电话'] = '13812345678'
    
    print(f"创建的脏数据形状: {df.shape}")
    print("\n前10行数据:")
    print(df.head(10))
    
    return df


def analyze_data_quality(df):
    """
    分析数据质量问题
    """
    print("\n=== 数据质量分析 ===")
    
    # 1. 基本信息
    print("\n1. 数据基本信息:")
    print(f"数据形状: {df.shape}")
    print(f"内存使用: {df.memory_usage(deep=True).sum():,} bytes")
    
    # 2. 缺失值分析
    print("\n2. 缺失值分析:")
    missing_stats = pd.DataFrame({
        '缺失数量': df.isnull().sum(),
        '缺失比例(%)': (df.isnull().sum() / len(df) * 100).round(2)
    })
    missing_stats = missing_stats[missing_stats['缺失数量'] > 0]
    print(missing_stats)
    
    # 3. 重复值分析
    print("\n3. 重复值分析:")
    duplicate_count = df.duplicated().sum()
    print(f"重复行数量: {duplicate_count}")
    if duplicate_count > 0:
        print("重复的行:")
        print(df[df.duplicated(keep=False)].sort_values('客户ID'))
    
    # 4. 数据类型分析
    print("\n4. 数据类型分析:")
    print(df.dtypes)
    
    # 5. 唯一值分析
    print("\n5. 唯一值分析:")
    for col in df.columns:
        unique_count = df[col].nunique()
        total_count = len(df)
        print(f"{col}: {unique_count}/{total_count} ({unique_count/total_count*100:.1f}%)")
    
    # 6. 异常值检测（数值列）
    print("\n6. 异常值检测:")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if col != '客户ID':
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col]
            if len(outliers) > 0:
                print(f"{col}: {len(outliers)} 个异常值")
                print(f"  正常范围: [{lower_bound:.2f}, {upper_bound:.2f}]")
                print(f"  异常值: {outliers.tolist()}")


def handle_missing_values(df):
    """
    处理缺失值
    """
    print("\n=== 处理缺失值 ===")
    
    df_cleaned = df.copy()
    
    # 1. 删除缺失值过多的行或列
    print("\n1. 删除策略:")
    # 如果某行缺失值超过50%，则删除该行
    missing_threshold = 0.5
    rows_to_drop = df_cleaned.isnull().sum(axis=1) > len(df_cleaned.columns) * missing_threshold
    print(f"删除缺失值过多的行: {rows_to_drop.sum()} 行")
    df_cleaned = df_cleaned[~rows_to_drop]
    
    # 2. 填充缺失值
    print("\n2. 填充策略:")
    
    # 姓名：删除缺失的行（关键字段）
    before_count = len(df_cleaned)
    df_cleaned = df_cleaned.dropna(subset=['姓名'])
    print(f"删除姓名缺失的行: {before_count - len(df_cleaned)} 行")
    
    # 年龄：用中位数填充
    age_median = df_cleaned['年龄'].median()
    df_cleaned['年龄'].fillna(age_median, inplace=True)
    print(f"年龄缺失值用中位数填充: {age_median}")
    
    # 收入：用同城市同性别的平均值填充
    for city in df_cleaned['城市'].unique():
        for gender in df_cleaned['性别'].unique():
            mask = (df_cleaned['城市'] == city) & (df_cleaned['性别'] == gender)
            income_mean = df_cleaned.loc[mask, '收入'].mean()
            if not pd.isna(income_mean):
                df_cleaned.loc[mask, '收入'] = df_cleaned.loc[mask, '收入'].fillna(income_mean)
    
    # 剩余收入缺失值用全体平均值填充
    overall_income_mean = df_cleaned['收入'].mean()
    df_cleaned['收入'].fillna(overall_income_mean, inplace=True)
    print("收入缺失值用分组平均值填充")
    
    print(f"\n处理后的缺失值统计:")
    print(df_cleaned.isnull().sum())
    
    return df_cleaned


def handle_duplicates(df):
    """
    处理重复值
    """
    print("\n=== 处理重复值 ===")
    
    # 检查重复
    print(f"处理前重复行数: {df.duplicated().sum()}")
    
    # 显示重复的行
    if df.duplicated().sum() > 0:
        print("\n重复的行:")
        duplicates = df[df.duplicated(keep=False)].sort_values('客户ID')
        print(duplicates[['客户ID', '姓名', '年龄', '城市']])
    
    # 删除重复行，保留第一个
    df_no_duplicates = df.drop_duplicates(keep='first')
    print(f"\n删除重复行后: {len(df_no_duplicates)} 行（删除了 {len(df) - len(df_no_duplicates)} 行）")
    
    # 基于特定列检查重复（例如，同一个客户ID不应该重复）
    id_duplicates = df_no_duplicates['客户ID'].duplicated().sum()
    if id_duplicates > 0:
        print(f"警告: 仍有 {id_duplicates} 个重复的客户ID")
    
    return df_no_duplicates


def handle_data_types(df):
    """
    处理数据类型问题
    """
    print("\n=== 处理数据类型问题 ===")
    
    df_typed = df.copy()
    
    # 1. 处理年龄列的混合类型
    print("\n1. 处理年龄列:")
    print(f"年龄列当前类型: {df_typed['年龄'].dtype}")
    
    # 清理年龄数据
    def clean_age(age):
        if pd.isna(age):
            return age
        if isinstance(age, str):
            # 提取数字
            import re
            numbers = re.findall(r'\d+', str(age))
            if numbers:
                return int(numbers[0])
            else:
                return np.nan
        return age
    
    df_typed['年龄'] = df_typed['年龄'].apply(clean_age)
    df_typed['年龄'] = pd.to_numeric(df_typed['年龄'], errors='coerce')
    print(f"清理后年龄列类型: {df_typed['年龄'].dtype}")
    
    # 2. 处理收入列
    print("\n2. 处理收入列:")
    def clean_income(income):
        if pd.isna(income):
            return income
        if isinstance(income, str):
            # 移除非数字字符
            import re
            cleaned = re.sub(r'[^\d.-]', '', str(income))
            try:
                return float(cleaned)
            except:
                return np.nan
        return income
    
    df_typed['收入'] = df_typed['收入'].apply(clean_income)
    df_typed['收入'] = pd.to_numeric(df_typed['收入'], errors='coerce')
    print(f"清理后收入列类型: {df_typed['收入'].dtype}")
    
    # 3. 标准化分类数据
    print("\n3. 标准化分类数据:")
    
    # 标准化性别
    gender_mapping = {'M': '男', 'F': '女'}
    df_typed['性别'] = df_typed['性别'].replace(gender_mapping)
    print(f"性别唯一值: {df_typed['性别'].unique()}")
    
    # 标准化城市名称
    city_mapping = {'北京市': '北京', '上海市': '上海'}
    df_typed['城市'] = df_typed['城市'].replace(city_mapping)
    print(f"城市唯一值: {df_typed['城市'].unique()}")
    
    # 4. 优化数据类型以节省内存
    print("\n4. 优化数据类型:")
    print(f"优化前内存使用: {df_typed.memory_usage(deep=True).sum():,} bytes")
    
    # 将分类列转换为category类型
    categorical_cols = ['城市', '性别']
    for col in categorical_cols:
        df_typed[col] = df_typed[col].astype('category')
    
    # 将整数列转换为更小的类型
    if df_typed['年龄'].max() < 128:
        df_typed['年龄'] = df_typed['年龄'].astype('int8')
    
    print(f"优化后内存使用: {df_typed.memory_usage(deep=True).sum():,} bytes")
    print("\n优化后的数据类型:")
    print(df_typed.dtypes)
    
    return df_typed


def handle_outliers(df):
    """
    处理异常值
    """
    print("\n=== 处理异常值 ===")
    
    df_outliers = df.copy()
    
    # 1. 年龄异常值
    print("\n1. 处理年龄异常值:")
    age_outliers = (df_outliers['年龄'] < 0) | (df_outliers['年龄'] > 120)
    print(f"年龄异常值数量: {age_outliers.sum()}")
    if age_outliers.sum() > 0:
        print(f"异常年龄值: {df_outliers.loc[age_outliers, '年龄'].tolist()}")
        # 用中位数替换异常值
        age_median = df_outliers.loc[~age_outliers, '年龄'].median()
        df_outliers.loc[age_outliers, '年龄'] = age_median
        print(f"已用中位数 {age_median} 替换异常年龄值")
    
    # 2. 收入异常值
    print("\n2. 处理收入异常值:")
    # 使用IQR方法检测异常值
    Q1 = df_outliers['收入'].quantile(0.25)
    Q3 = df_outliers['收入'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    income_outliers = (df_outliers['收入'] < lower_bound) | (df_outliers['收入'] > upper_bound)
    print(f"收入异常值数量: {income_outliers.sum()}")
    print(f"正常收入范围: [{lower_bound:.2f}, {upper_bound:.2f}]")
    
    if income_outliers.sum() > 0:
        print(f"异常收入值: {df_outliers.loc[income_outliers, '收入'].tolist()}")
        # 用边界值替换异常值（Winsorization）
        df_outliers.loc[df_outliers['收入'] < lower_bound, '收入'] = lower_bound
        df_outliers.loc[df_outliers['收入'] > upper_bound, '收入'] = upper_bound
        print("已用边界值替换收入异常值")
    
    # 3. 消费金额异常值
    print("\n3. 处理消费金额异常值:")
    # 消费金额不应该为负数
    negative_spending = df_outliers['消费金额'] < 0
    if negative_spending.sum() > 0:
        print(f"负消费金额数量: {negative_spending.sum()}")
        df_outliers.loc[negative_spending, '消费金额'] = 0
        print("已将负消费金额设为0")
    
    # 检查消费金额是否合理（不应超过收入的某个倍数）
    unreasonable_spending = df_outliers['消费金额'] > df_outliers['收入'] * 2
    if unreasonable_spending.sum() > 0:
        print(f"不合理消费金额数量: {unreasonable_spending.sum()}")
        # 将不合理的消费金额设为收入的一定比例
        df_outliers.loc[unreasonable_spending, '消费金额'] = df_outliers.loc[unreasonable_spending, '收入'] * 0.3
        print("已调整不合理的消费金额")
    
    return df_outliers


def standardize_formats(df):
    """
    标准化数据格式
    """
    print("\n=== 标准化数据格式 ===")
    
    df_formatted = df.copy()
    
    # 1. 标准化电话号码格式
    print("\n1. 标准化电话号码:")
    def clean_phone(phone):
        if pd.isna(phone):
            return phone
        # 移除所有非数字字符
        import re
        cleaned = re.sub(r'\D', '', str(phone))
        # 确保是11位手机号码
        if len(cleaned) == 11 and cleaned.startswith('1'):
            return cleaned
        else:
            return np.nan
    
    df_formatted['电话'] = df_formatted['电话'].apply(clean_phone)
    print(f"标准化后的电话号码示例: {df_formatted['电话'].dropna().head().tolist()}")
    
    # 2. 标准化日期格式
    print("\n2. 确保日期格式:")
    df_formatted['注册日期'] = pd.to_datetime(df_formatted['注册日期'])
    print(f"注册日期类型: {df_formatted['注册日期'].dtype}")
    
    # 3. 添加派生字段
    print("\n3. 添加派生字段:")
    # 计算客户年龄段
    df_formatted['年龄段'] = pd.cut(
        df_formatted['年龄'], 
        bins=[0, 25, 35, 45, 55, 100], 
        labels=['青年', '青壮年', '中年', '中老年', '老年']
    )
    
    # 计算收入等级
    df_formatted['收入等级'] = pd.qcut(
        df_formatted['收入'], 
        q=5, 
        labels=['低收入', '中低收入', '中等收入', '中高收入', '高收入']
    )
    
    # 计算注册时长（天数）
    df_formatted['注册天数'] = (datetime.now() - df_formatted['注册日期']).dt.days
    
    print("添加的派生字段:")
    print(f"- 年龄段: {df_formatted['年龄段'].value_counts().to_dict()}")
    print(f"- 收入等级: {df_formatted['收入等级'].value_counts().to_dict()}")
    print(f"- 注册天数范围: {df_formatted['注册天数'].min()} - {df_formatted['注册天数'].max()}")
    
    return df_formatted


def validate_cleaned_data(df_original, df_cleaned):
    """
    验证清洗后的数据质量
    """
    print("\n=== 数据清洗效果验证 ===")
    
    print("\n1. 数据量对比:")
    print(f"原始数据: {len(df_original)} 行")
    print(f"清洗后: {len(df_cleaned)} 行")
    print(f"保留率: {len(df_cleaned)/len(df_original)*100:.1f}%")
    
    print("\n2. 缺失值对比:")
    original_missing = df_original.isnull().sum().sum()
    cleaned_missing = df_cleaned.isnull().sum().sum()
    print(f"原始缺失值: {original_missing}")
    print(f"清洗后缺失值: {cleaned_missing}")
    print(f"缺失值减少: {original_missing - cleaned_missing}")
    
    print("\n3. 重复值对比:")
    original_duplicates = df_original.duplicated().sum()
    cleaned_duplicates = df_cleaned.duplicated().sum()
    print(f"原始重复值: {original_duplicates}")
    print(f"清洗后重复值: {cleaned_duplicates}")
    
    print("\n4. 数据类型优化:")
    original_memory = df_original.memory_usage(deep=True).sum()
    cleaned_memory = df_cleaned.memory_usage(deep=True).sum()
    print(f"原始内存使用: {original_memory:,} bytes")
    print(f"清洗后内存使用: {cleaned_memory:,} bytes")
    print(f"内存节省: {(original_memory - cleaned_memory)/original_memory*100:.1f}%")
    
    print("\n5. 数据质量评分:")
    # 简单的数据质量评分
    completeness = (1 - cleaned_missing / (len(df_cleaned) * len(df_cleaned.columns))) * 100
    uniqueness = (1 - cleaned_duplicates / len(df_cleaned)) * 100
    validity = 100  # 假设经过清洗后数据都是有效的
    
    overall_score = (completeness + uniqueness + validity) / 3
    
    print(f"完整性: {completeness:.1f}%")
    print(f"唯一性: {uniqueness:.1f}%")
    print(f"有效性: {validity:.1f}%")
    print(f"总体质量评分: {overall_score:.1f}%")


def visualize_cleaning_results(df_original, df_cleaned):
    """
    可视化数据清洗结果
    """
    print("\n=== 数据清洗结果可视化 ===")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('数据清洗效果对比', fontsize=16)
    
    # 1. 缺失值对比
    missing_original = df_original.isnull().sum()
    missing_cleaned = df_cleaned.isnull().sum()
    
    x = range(len(missing_original))
    width = 0.35
    
    axes[0, 0].bar([i - width/2 for i in x], missing_original, width, label='清洗前', alpha=0.7)
    axes[0, 0].bar([i + width/2 for i in x], missing_cleaned, width, label='清洗后', alpha=0.7)
    axes[0, 0].set_title('缺失值对比')
    axes[0, 0].set_xlabel('列名')
    axes[0, 0].set_ylabel('缺失值数量')
    axes[0, 0].set_xticks(x)
    axes[0, 0].set_xticklabels(missing_original.index, rotation=45)
    axes[0, 0].legend()
    
    # 2. 年龄分布对比
    axes[0, 1].hist(df_original['年龄'].dropna(), bins=20, alpha=0.7, label='清洗前')
    axes[0, 1].hist(df_cleaned['年龄'].dropna(), bins=20, alpha=0.7, label='清洗后')
    axes[0, 1].set_title('年龄分布对比')
    axes[0, 1].set_xlabel('年龄')
    axes[0, 1].set_ylabel('频数')
    axes[0, 1].legend()
    
    # 3. 收入分布对比
    axes[1, 0].hist(df_original['收入'].dropna(), bins=20, alpha=0.7, label='清洗前')
    axes[1, 0].hist(df_cleaned['收入'].dropna(), bins=20, alpha=0.7, label='清洗后')
    axes[1, 0].set_title('收入分布对比')
    axes[1, 0].set_xlabel('收入')
    axes[1, 0].set_ylabel('频数')
    axes[1, 0].legend()
    
    # 4. 数据量统计
    categories = ['总行数', '缺失值', '重复值']
    original_stats = [len(df_original), df_original.isnull().sum().sum(), df_original.duplicated().sum()]
    cleaned_stats = [len(df_cleaned), df_cleaned.isnull().sum().sum(), df_cleaned.duplicated().sum()]
    
    x = range(len(categories))
    axes[1, 1].bar([i - width/2 for i in x], original_stats, width, label='清洗前', alpha=0.7)
    axes[1, 1].bar([i + width/2 for i in x], cleaned_stats, width, label='清洗后', alpha=0.7)
    axes[1, 1].set_title('数据统计对比')
    axes[1, 1].set_xlabel('统计项')
    axes[1, 1].set_ylabel('数量')
    axes[1, 1].set_xticks(x)
    axes[1, 1].set_xticklabels(categories)
    axes[1, 1].legend()
    
    plt.tight_layout()
    plt.show()
    
    print("已生成数据清洗效果对比图表")


def main():
    """
    主函数
    """
    print("数据清洗完整流程演示")
    print("=" * 50)
    
    # 1. 创建脏数据
    df_dirty = create_dirty_data()
    
    # 2. 分析数据质量
    analyze_data_quality(df_dirty)
    
    # 3. 数据清洗流程
    print("\n" + "=" * 50)
    print("开始数据清洗流程")
    print("=" * 50)
    
    # 处理缺失值
    df_step1 = handle_missing_values(df_dirty)
    
    # 处理重复值
    df_step2 = handle_duplicates(df_step1)
    
    # 处理数据类型
    df_step3 = handle_data_types(df_step2)
    
    # 处理异常值
    df_step4 = handle_outliers(df_step3)
    
    # 标准化格式
    df_cleaned = standardize_formats(df_step4)
    
    # 4. 验证清洗效果
    validate_cleaned_data(df_dirty, df_cleaned)
    
    # 5. 可视化结果
    visualize_cleaning_results(df_dirty, df_cleaned)
    
    print("\n" + "=" * 50)
    print("数据清洗完成！")
    print("=" * 50)
    
    print("\n清洗后的数据预览:")
    print(df_cleaned.head())
    
    print("\n数据清洗要点总结:")
    print("1. 缺失值处理：删除、填充、插值")
    print("2. 重复值处理：识别和删除重复记录")
    print("3. 数据类型：确保数据类型正确和优化")
    print("4. 异常值处理：检测和处理离群值")
    print("5. 格式标准化：统一数据格式")
    print("6. 数据验证：确保清洗效果")
    
    return df_cleaned


if __name__ == "__main__":
    main()