#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DataFrame基础操作示例

本文件演示DataFrame的创建、基本属性和操作方法。

作者: Python教程团队
创建日期: 2024-01-01
"""

import pandas as pd
import numpy as np


def create_dataframe_examples():
    """
    演示DataFrame的多种创建方法
    """
    print("=== DataFrame创建方法演示 ===")
    
    # 方法1: 从字典创建
    print("\n1. 从字典创建DataFrame:")
    data_dict = {
        '学号': [1001, 1002, 1003, 1004, 1005],
        '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
        '数学': [85, 92, 78, 88, 95],
        '英语': [90, 85, 82, 91, 87],
        '物理': [88, 89, 85, 92, 90]
    }
    df_from_dict = pd.DataFrame(data_dict)
    print(df_from_dict)
    
    # 方法2: 从列表的列表创建
    print("\n2. 从列表的列表创建DataFrame:")
    data_list = [
        [1006, '孙八', 87, 89, 91],
        [1007, '周九', 92, 88, 85],
        [1008, '吴十', 79, 93, 88]
    ]
    columns = ['学号', '姓名', '数学', '英语', '物理']
    df_from_list = pd.DataFrame(data_list, columns=columns)
    print(df_from_list)
    
    # 方法3: 从NumPy数组创建
    print("\n3. 从NumPy数组创建DataFrame:")
    np.random.seed(42)
    data_array = np.random.randint(60, 100, (5, 3))
    df_from_array = pd.DataFrame(
        data_array, 
        columns=['科目A', '科目B', '科目C'],
        index=[f'学生{i+1}' for i in range(5)]
    )
    print(df_from_array)
    
    return df_from_dict


def dataframe_properties(df):
    """
    演示DataFrame的基本属性
    """
    print("\n=== DataFrame基本属性 ===")
    
    print(f"\n数据形状: {df.shape}")
    print(f"行数: {df.shape[0]}")
    print(f"列数: {df.shape[1]}")
    print(f"总元素数: {df.size}")
    
    print(f"\n列名: {df.columns.tolist()}")
    print(f"索引: {df.index.tolist()}")
    
    print("\n数据类型:")
    print(df.dtypes)
    
    print("\n内存使用情况:")
    print(df.memory_usage(deep=True))
    
    print("\n数据信息概览:")
    df.info()


def dataframe_indexing(df):
    """
    演示DataFrame的索引和选择操作
    """
    print("\n=== DataFrame索引和选择 ===")
    
    # 列选择
    print("\n1. 列选择:")
    print("选择单列（返回Series）:")
    print(df['姓名'])
    print(f"类型: {type(df['姓名'])}")
    
    print("\n选择单列（返回DataFrame）:")
    print(df[['姓名']])
    print(f"类型: {type(df[['姓名']])}")
    
    print("\n选择多列:")
    print(df[['姓名', '数学', '英语']])
    
    # 行选择
    print("\n2. 行选择:")
    print("使用iloc按位置选择:")
    print("前3行:")
    print(df.iloc[:3])
    
    print("\n第2到4行:")
    print(df.iloc[1:4])
    
    print("\n使用loc按标签选择:")
    print("索引0到2:")
    print(df.loc[0:2])
    
    # 行列同时选择
    print("\n3. 行列同时选择:")
    print("前3行的姓名和数学成绩:")
    print(df.loc[0:2, ['姓名', '数学']])
    
    print("\n使用iloc选择:")
    print(df.iloc[0:3, [1, 2]])  # 前3行，第2和第3列


def dataframe_filtering(df):
    """
    演示DataFrame的条件筛选
    """
    print("\n=== DataFrame条件筛选 ===")
    
    # 单条件筛选
    print("\n1. 单条件筛选:")
    high_math = df[df['数学'] >= 90]
    print("数学成绩>=90的学生:")
    print(high_math)
    
    # 多条件筛选
    print("\n2. 多条件筛选:")
    excellent_students = df[(df['数学'] >= 85) & (df['英语'] >= 85)]
    print("数学和英语都>=85的学生:")
    print(excellent_students)
    
    # 使用isin方法
    print("\n3. 使用isin方法:")
    selected_students = df[df['姓名'].isin(['张三', '王五', '钱七'])]
    print("指定学生的成绩:")
    print(selected_students)
    
    # 字符串筛选
    print("\n4. 字符串筛选:")
    # 假设我们要筛选姓名包含特定字符的学生
    name_filter = df[df['姓名'].str.contains('三|五')]
    print("姓名包含'三'或'五'的学生:")
    print(name_filter)
    
    # 使用query方法
    print("\n5. 使用query方法:")
    query_result = df.query('数学 > 85 and 英语 > 85')
    print("使用query筛选优秀学生:")
    print(query_result)


def dataframe_operations(df):
    """
    演示DataFrame的基本操作
    """
    print("\n=== DataFrame基本操作 ===")
    
    # 添加新列
    print("\n1. 添加新列:")
    df_copy = df.copy()
    
    # 计算总分
    df_copy['总分'] = df_copy['数学'] + df_copy['英语'] + df_copy['物理']
    
    # 计算平均分
    df_copy['平均分'] = df_copy[['数学', '英语', '物理']].mean(axis=1)
    
    # 添加等级列
    df_copy['等级'] = pd.cut(
        df_copy['平均分'], 
        bins=[0, 70, 80, 90, 100], 
        labels=['不及格', '良好', '优秀', '卓越']
    )
    
    print(df_copy)
    
    # 删除列
    print("\n2. 删除列:")
    df_dropped = df_copy.drop(['总分'], axis=1)
    print("删除总分列后:")
    print(df_dropped.columns.tolist())
    
    # 重命名列
    print("\n3. 重命名列:")
    df_renamed = df_copy.rename(columns={
        '数学': 'Mathematics',
        '英语': 'English',
        '物理': 'Physics'
    })
    print("重命名后的列名:")
    print(df_renamed.columns.tolist())
    
    # 排序
    print("\n4. 排序操作:")
    print("按平均分降序排列:")
    df_sorted = df_copy.sort_values('平均分', ascending=False)
    print(df_sorted[['姓名', '平均分', '等级']])
    
    print("\n按多列排序（先按等级，再按平均分）:")
    df_multi_sorted = df_copy.sort_values(['等级', '平均分'], ascending=[True, False])
    print(df_multi_sorted[['姓名', '平均分', '等级']])
    
    return df_copy


def dataframe_statistics(df):
    """
    演示DataFrame的统计操作
    """
    print("\n=== DataFrame统计操作 ===")
    
    # 基本统计信息
    print("\n1. 基本统计信息:")
    print(df.describe())
    
    # 各科目统计
    print("\n2. 各科目详细统计:")
    subjects = ['数学', '英语', '物理']
    for subject in subjects:
        print(f"\n{subject}科目统计:")
        print(f"  平均分: {df[subject].mean():.2f}")
        print(f"  中位数: {df[subject].median():.2f}")
        print(f"  标准差: {df[subject].std():.2f}")
        print(f"  最高分: {df[subject].max()}")
        print(f"  最低分: {df[subject].min()}")
        print(f"  分数范围: {df[subject].max() - df[subject].min()}")
    
    # 相关性分析
    print("\n3. 科目间相关性:")
    correlation = df[subjects].corr()
    print(correlation)
    
    # 计数统计
    print("\n4. 计数统计:")
    print(f"总学生数: {len(df)}")
    print(f"数学>=90的学生数: {(df['数学'] >= 90).sum()}")
    print(f"英语>=90的学生数: {(df['英语'] >= 90).sum()}")
    print(f"物理>=90的学生数: {(df['物理'] >= 90).sum()}")


def main():
    """
    主函数
    """
    print("DataFrame基础操作示例")
    print("=" * 40)
    
    # 创建DataFrame
    df = create_dataframe_examples()
    
    # 基本属性
    dataframe_properties(df)
    
    # 索引和选择
    dataframe_indexing(df)
    
    # 条件筛选
    dataframe_filtering(df)
    
    # 基本操作
    df_extended = dataframe_operations(df)
    
    # 统计操作
    dataframe_statistics(df)
    
    print("\n=" * 40)
    print("DataFrame基础操作演示完成！")
    print("\n学习要点:")
    print("1. DataFrame是二维标记数据结构")
    print("2. 支持多种创建方法")
    print("3. 提供灵活的索引和选择机制")
    print("4. 支持条件筛选和复杂查询")
    print("5. 内置丰富的统计分析功能")


if __name__ == "__main__":
    main()