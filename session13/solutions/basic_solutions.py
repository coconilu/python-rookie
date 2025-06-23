#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pandas基础练习题解答

本文件包含basic_exercises.py中所有练习题的详细解答。
每个解答都包含详细的注释说明，帮助理解Pandas的使用方法。

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

print("Pandas基础练习题解答")
print("=" * 50)

# ==================== 练习1：DataFrame和Series基础操作 ====================
print("\n练习1：DataFrame和Series基础操作")
print("-" * 30)

# 1.1 创建DataFrame
print("\n1.1 创建学生成绩DataFrame")
students_data = {
    '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
    '年龄': [20, 21, 19, 22, 20],
    '性别': ['男', '女', '男', '女', '男'],
    '数学': [85, 92, 78, 96, 88],
    '英语': [90, 87, 85, 93, 82],
    '物理': [88, 85, 90, 89, 91]
}
students_df = pd.DataFrame(students_data)
print("学生数据：")
print(students_df)
print(f"\nDataFrame形状: {students_df.shape}")
print(f"列名: {list(students_df.columns)}")
print(f"数据类型:\n{students_df.dtypes}")

# 1.2 基本信息查看
print("\n1.2 基本信息查看")
print("\n基本统计信息：")
print(students_df.describe())

print("\n详细信息：")
print(students_df.info())

print("\n前3行数据：")
print(students_df.head(3))

print("\n后2行数据：")
print(students_df.tail(2))

# 1.3 Series操作
print("\n1.3 Series操作")
math_scores = students_df['数学']
print(f"数学成绩Series类型: {type(math_scores)}")
print(f"数学平均分: {math_scores.mean():.2f}")
print(f"数学最高分: {math_scores.max()}")
print(f"数学最低分: {math_scores.min()}")
print(f"数学成绩标准差: {math_scores.std():.2f}")

# 1.4 添加新列
print("\n1.4 添加新列")
# 计算总分
students_df['总分'] = students_df['数学'] + students_df['英语'] + students_df['物理']
# 计算平均分
students_df['平均分'] = students_df['总分'] / 3
# 根据平均分评定等级
def get_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    else:
        return 'D'

students_df['等级'] = students_df['平均分'].apply(get_grade)

print("添加新列后的数据：")
print(students_df)

# ==================== 练习2：数据选择和筛选 ====================
print("\n\n练习2：数据选择和筛选")
print("-" * 30)

# 2.1 列选择
print("\n2.1 列选择")
print("\n选择姓名和数学成绩：")
print(students_df[['姓名', '数学']])

print("\n选择所有成绩列：")
score_columns = ['数学', '英语', '物理']
print(students_df[score_columns])

# 2.2 行选择
print("\n2.2 行选择")
print("\n使用iloc选择前3行：")
print(students_df.iloc[:3])

print("\n使用loc选择特定行：")
print(students_df.loc[1:3, ['姓名', '总分']])

# 2.3 条件筛选
print("\n2.3 条件筛选")
print("\n数学成绩大于85的学生：")
high_math = students_df[students_df['数学'] > 85]
print(high_math[['姓名', '数学']])

print("\n女学生且平均分大于85：")
female_high = students_df[(students_df['性别'] == '女') & (students_df['平均分'] > 85)]
print(female_high[['姓名', '性别', '平均分']])

print("\n数学或英语成绩大于90：")
high_scores = students_df[(students_df['数学'] > 90) | (students_df['英语'] > 90)]
print(high_scores[['姓名', '数学', '英语']])

# 2.4 使用query方法
print("\n2.4 使用query方法")
print("\n使用query筛选年龄大于20的男学生：")
query_result = students_df.query("年龄 > 20 and 性别 == '男'")
print(query_result[['姓名', '年龄', '性别']])

# ==================== 练习3：数据清洗 ====================
print("\n\n练习3：数据清洗")
print("-" * 30)

# 3.1 创建包含问题的数据
print("\n3.1 创建包含问题的数据")
dirty_data = {
    '姓名': ['张三', '李四', None, '赵六', '钱七', '张三'],  # 包含缺失值和重复
    '年龄': [20, 21, 19, None, 20, 20],  # 包含缺失值
    '成绩': [85, 92, 78, 96, None, 85],  # 包含缺失值
    '城市': ['北京', '上海', '北京 ', ' 广州', '深圳', '北京']  # 包含空格
}
dirty_df = pd.DataFrame(dirty_data)
print("原始脏数据：")
print(dirty_df)
print(f"\n数据形状: {dirty_df.shape}")

# 3.2 检查数据质量
print("\n3.2 检查数据质量")
print("\n缺失值统计：")
print(dirty_df.isnull().sum())

print("\n重复行检查：")
print(f"重复行数量: {dirty_df.duplicated().sum()}")
print("\n重复行详情：")
print(dirty_df[dirty_df.duplicated(keep=False)])

# 3.3 处理缺失值
print("\n3.3 处理缺失值")
# 删除姓名为空的行
clean_df = dirty_df.dropna(subset=['姓名']).copy()
print("\n删除姓名缺失后：")
print(clean_df)

# 用平均值填充年龄缺失值
clean_df['年龄'].fillna(clean_df['年龄'].mean(), inplace=True)
print("\n填充年龄缺失值后：")
print(clean_df)

# 用中位数填充成绩缺失值
clean_df['成绩'].fillna(clean_df['成绩'].median(), inplace=True)
print("\n填充成绩缺失值后：")
print(clean_df)

# 3.4 处理重复值
print("\n3.4 处理重复值")
clean_df = clean_df.drop_duplicates()
print("\n删除重复行后：")
print(clean_df)
print(f"清洗后数据形状: {clean_df.shape}")

# 3.5 处理字符串问题
print("\n3.5 处理字符串问题")
clean_df['城市'] = clean_df['城市'].str.strip()  # 去除首尾空格
print("\n去除城市名称空格后：")
print(clean_df)

# ==================== 练习4：基本统计分析 ====================
print("\n\n练习4：基本统计分析")
print("-" * 30)

# 使用学生数据进行统计分析
print("\n4.1 描述性统计")
print("\n数值列的描述性统计：")
print(students_df.describe())

print("\n分类列的描述性统计：")
print(students_df.describe(include=['object']))

# 4.2 分组统计
print("\n4.2 分组统计")
print("\n按性别分组的统计：")
gender_stats = students_df.groupby('性别').agg({
    '数学': ['mean', 'max', 'min'],
    '英语': ['mean', 'max', 'min'],
    '物理': ['mean', 'max', 'min'],
    '总分': ['mean', 'std']
}).round(2)
print(gender_stats)

print("\n按等级分组的人数统计：")
grade_counts = students_df['等级'].value_counts()
print(grade_counts)

# 4.3 相关性分析
print("\n4.3 相关性分析")
subject_corr = students_df[['数学', '英语', '物理']].corr()
print("\n各科目成绩相关性：")
print(subject_corr.round(3))

# 4.4 可视化
print("\n4.4 创建可视化图表")
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('学生成绩分析', fontsize=16)

# 成绩分布直方图
students_df[['数学', '英语', '物理']].hist(bins=10, ax=axes[0, 0], alpha=0.7)
axes[0, 0].set_title('各科成绩分布')

# 性别分组的平均成绩
gender_avg = students_df.groupby('性别')[['数学', '英语', '物理']].mean()
gender_avg.plot(kind='bar', ax=axes[0, 1])
axes[0, 1].set_title('性别分组平均成绩')
axes[0, 1].tick_params(axis='x', rotation=0)

# 总分分布
students_df['总分'].hist(bins=8, ax=axes[1, 0], alpha=0.7)
axes[1, 0].set_title('总分分布')
axes[1, 0].set_xlabel('总分')
axes[1, 0].set_ylabel('人数')

# 等级分布饼图
grade_counts.plot(kind='pie', ax=axes[1, 1], autopct='%1.1f%%')
axes[1, 1].set_title('成绩等级分布')

plt.tight_layout()
plt.show()

# ==================== 练习5：数据分组和聚合 ====================
print("\n\n练习5：数据分组和聚合")
print("-" * 30)

# 5.1 创建销售数据
print("\n5.1 创建销售数据")
np.random.seed(42)
sales_data = {
    '日期': pd.date_range('2024-01-01', periods=100, freq='D'),
    '产品': np.random.choice(['A', 'B', 'C', 'D'], 100),
    '销售员': np.random.choice(['张三', '李四', '王五'], 100),
    '销量': np.random.randint(10, 100, 100),
    '单价': np.random.uniform(50, 200, 100).round(2)
}
sales_df = pd.DataFrame(sales_data)
sales_df['销售额'] = sales_df['销量'] * sales_df['单价']
print("销售数据样例：")
print(sales_df.head(10))

# 5.2 基本分组聚合
print("\n5.2 基本分组聚合")
print("\n按产品分组的销售统计：")
product_stats = sales_df.groupby('产品').agg({
    '销量': ['sum', 'mean', 'count'],
    '销售额': ['sum', 'mean'],
    '单价': 'mean'
}).round(2)
print(product_stats)

print("\n按销售员分组的业绩统计：")
salesperson_stats = sales_df.groupby('销售员').agg({
    '销售额': ['sum', 'mean', 'count'],
    '销量': 'sum'
}).round(2)
print(salesperson_stats)

# 5.3 多级分组
print("\n5.3 多级分组")
print("\n按产品和销售员分组：")
multi_group = sales_df.groupby(['产品', '销售员'])['销售额'].sum().unstack(fill_value=0)
print(multi_group)

# 5.4 时间分组
print("\n5.4 时间分组")
sales_df['月份'] = sales_df['日期'].dt.to_period('M')
monthly_sales = sales_df.groupby('月份').agg({
    '销售额': 'sum',
    '销量': 'sum'
}).round(2)
print("\n月度销售统计：")
print(monthly_sales)

# 5.5 自定义聚合函数
print("\n5.5 自定义聚合函数")
def sales_range(series):
    return series.max() - series.min()

def top_performer_ratio(series):
    return (series >= series.quantile(0.8)).mean()

custom_agg = sales_df.groupby('产品')['销售额'].agg([
    'mean',
    'std',
    sales_range,
    top_performer_ratio
]).round(3)
print("\n自定义聚合结果：")
print(custom_agg)

# ==================== 练习6：时间序列基础 ====================
print("\n\n练习6：时间序列基础")
print("-" * 30)

# 6.1 创建时间序列数据
print("\n6.1 创建时间序列数据")
dates = pd.date_range('2024-01-01', periods=365, freq='D')
np.random.seed(42)
# 模拟股价数据，包含趋势和随机波动
base_price = 100
trend = np.linspace(0, 20, 365)  # 上升趋势
noise = np.random.normal(0, 5, 365)  # 随机波动
prices = base_price + trend + noise

stock_data = pd.DataFrame({
    '日期': dates,
    '价格': prices
})
stock_data.set_index('日期', inplace=True)
print("股价数据样例：")
print(stock_data.head(10))

# 6.2 时间序列基本操作
print("\n6.2 时间序列基本操作")
print(f"数据时间范围: {stock_data.index.min()} 到 {stock_data.index.max()}")
print(f"数据频率: {stock_data.index.freq}")
print(f"总天数: {len(stock_data)}")

# 6.3 时间选择
print("\n6.3 时间选择")
print("\n2024年1月的数据：")
jan_data = stock_data['2024-01']
print(jan_data.head())
print(f"1月份数据点数: {len(jan_data)}")

print("\n特定日期范围的数据：")
range_data = stock_data['2024-06-01':'2024-06-30']
print(f"6月份平均价格: {range_data['价格'].mean():.2f}")

# 6.4 重采样
print("\n6.4 重采样")
print("\n按周重采样（取平均值）：")
weekly_avg = stock_data.resample('W')['价格'].mean()
print(weekly_avg.head())

print("\n按月重采样（多种统计）：")
monthly_stats = stock_data.resample('M')['价格'].agg(['mean', 'max', 'min', 'std']).round(2)
print(monthly_stats)

# 6.5 滑动窗口
print("\n6.5 滑动窗口")
stock_data['MA_7'] = stock_data['价格'].rolling(window=7).mean()  # 7日移动平均
stock_data['MA_30'] = stock_data['价格'].rolling(window=30).mean()  # 30日移动平均
stock_data['波动率'] = stock_data['价格'].rolling(window=30).std()  # 30日波动率

print("\n添加移动平均线后的数据：")
print(stock_data.tail())

# 6.6 时间序列可视化
print("\n6.6 创建时间序列图表")
fig, axes = plt.subplots(2, 1, figsize=(12, 8))
fig.suptitle('股价时间序列分析', fontsize=16)

# 价格和移动平均线
stock_data[['价格', 'MA_7', 'MA_30']].plot(ax=axes[0])
axes[0].set_title('股价走势和移动平均线')
axes[0].set_ylabel('价格')
axes[0].legend()

# 波动率
stock_data['波动率'].plot(ax=axes[1], color='red')
axes[1].set_title('30日波动率')
axes[1].set_ylabel('波动率')
axes[1].set_xlabel('日期')

plt.tight_layout()
plt.show()

# ==================== 练习7：数据合并和连接 ====================
print("\n\n练习7：数据合并和连接")
print("-" * 30)

# 7.1 创建多个相关数据表
print("\n7.1 创建多个相关数据表")

# 员工基本信息
employees = pd.DataFrame({
    '员工ID': [1, 2, 3, 4, 5],
    '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
    '部门ID': [101, 102, 101, 103, 102],
    '入职日期': ['2020-01-15', '2019-03-20', '2021-06-10', '2020-11-05', '2022-02-28']
})

# 部门信息
departments = pd.DataFrame({
    '部门ID': [101, 102, 103, 104],
    '部门名称': ['技术部', '销售部', '人事部', '财务部'],
    '部门经理': ['李经理', '王经理', '赵经理', '钱经理']
})

# 薪资信息
salaries = pd.DataFrame({
    '员工ID': [1, 2, 3, 4, 6],  # 注意：包含不存在的员工ID 6
    '基本工资': [8000, 9000, 7500, 8500, 7000],
    '绩效奖金': [2000, 2500, 1500, 2000, 1000]
})

print("员工信息：")
print(employees)
print("\n部门信息：")
print(departments)
print("\n薪资信息：")
print(salaries)

# 7.2 内连接
print("\n7.2 内连接")
inner_join = pd.merge(employees, salaries, on='员工ID', how='inner')
print("\n员工和薪资内连接结果：")
print(inner_join)

# 7.3 左连接
print("\n7.3 左连接")
left_join = pd.merge(employees, salaries, on='员工ID', how='left')
print("\n员工和薪资左连接结果：")
print(left_join)

# 7.4 右连接
print("\n7.4 右连接")
right_join = pd.merge(employees, salaries, on='员工ID', how='right')
print("\n员工和薪资右连接结果：")
print(right_join)

# 7.5 外连接
print("\n7.5 外连接")
outer_join = pd.merge(employees, salaries, on='员工ID', how='outer')
print("\n员工和薪资外连接结果：")
print(outer_join)

# 7.6 多表连接
print("\n7.6 多表连接")
# 先连接员工和部门
emp_dept = pd.merge(employees, departments, on='部门ID', how='left')
# 再连接薪资
full_info = pd.merge(emp_dept, salaries, on='员工ID', how='left')
print("\n完整员工信息：")
print(full_info)

# 7.7 按索引连接
print("\n7.7 按索引连接")
# 设置索引后连接
employees_indexed = employees.set_index('员工ID')
salaries_indexed = salaries.set_index('员工ID')
index_join = employees_indexed.join(salaries_indexed, how='left')
print("\n按索引连接结果：")
print(index_join)

# 7.8 concat连接
print("\n7.8 concat连接")
# 创建两个时间段的数据
q1_sales = pd.DataFrame({
    '产品': ['A', 'B', 'C'],
    'Q1销量': [100, 150, 120]
})

q2_sales = pd.DataFrame({
    '产品': ['A', 'B', 'C'],
    'Q2销量': [110, 140, 130]
})

print("Q1销量：")
print(q1_sales)
print("\nQ2销量：")
print(q2_sales)

# 横向连接
horizontal_concat = pd.concat([q1_sales.set_index('产品'), q2_sales.set_index('产品')], axis=1)
print("\n横向连接结果：")
print(horizontal_concat)

# ==================== 练习8：综合分析项目 ====================
print("\n\n练习8：综合分析项目")
print("-" * 30)

# 8.1 项目背景
print("\n8.1 项目背景：在线教育平台学习数据分析")

# 8.2 创建综合数据集
print("\n8.2 创建综合数据集")
np.random.seed(42)

# 学生信息
student_info = pd.DataFrame({
    '学生ID': range(1, 1001),
    '姓名': [f'学生{i:04d}' for i in range(1, 1001)],
    '年龄': np.random.randint(18, 35, 1000),
    '性别': np.random.choice(['男', '女'], 1000),
    '城市': np.random.choice(['北京', '上海', '广州', '深圳', '杭州'], 1000),
    '注册日期': pd.date_range('2023-01-01', periods=1000, freq='H')
})

# 课程信息
course_info = pd.DataFrame({
    '课程ID': range(1, 21),
    '课程名称': [f'课程{i:02d}' for i in range(1, 21)],
    '课程类别': np.random.choice(['编程', '数据科学', '设计', '商业'], 20),
    '难度等级': np.random.choice(['初级', '中级', '高级'], 20),
    '课程价格': np.random.randint(99, 999, 20)
})

# 学习记录
learning_records = []
for student_id in range(1, 1001):
    # 每个学生随机选择1-5门课程
    n_courses = np.random.randint(1, 6)
    courses = np.random.choice(range(1, 21), n_courses, replace=False)
    
    for course_id in courses:
        learning_records.append({
            '学生ID': student_id,
            '课程ID': course_id,
            '开始日期': pd.Timestamp('2023-01-01') + pd.Timedelta(days=np.random.randint(0, 365)),
            '完成进度': np.random.randint(0, 101),
            '学习时长': np.random.randint(1, 100),
            '考试成绩': np.random.randint(60, 100) if np.random.random() > 0.3 else None
        })

learning_df = pd.DataFrame(learning_records)

print(f"学生信息: {len(student_info)} 条")
print(f"课程信息: {len(course_info)} 条")
print(f"学习记录: {len(learning_df)} 条")

# 8.3 数据合并
print("\n8.3 数据合并")
full_data = learning_df.merge(student_info, on='学生ID', how='left') \
                      .merge(course_info, on='课程ID', how='left')

print(f"合并后数据形状: {full_data.shape}")
print("\n合并后数据样例：")
print(full_data.head())

# 8.4 数据清洗
print("\n8.4 数据清洗")
print(f"考试成绩缺失值: {full_data['考试成绩'].isnull().sum()}")

# 只对完成进度大于80%的学生填充考试成绩
high_progress = full_data['完成进度'] > 80
full_data.loc[high_progress & full_data['考试成绩'].isnull(), '考试成绩'] = \
    full_data.loc[high_progress, '考试成绩'].median()

print(f"清洗后考试成绩缺失值: {full_data['考试成绩'].isnull().sum()}")

# 8.5 综合分析
print("\n8.5 综合分析")

# 学习效果分析
print("\n学习效果分析：")
effectiveness = full_data.groupby('课程类别').agg({
    '完成进度': 'mean',
    '学习时长': 'mean',
    '考试成绩': 'mean',
    '学生ID': 'count'
}).round(2)
effectiveness.columns = ['平均完成进度', '平均学习时长', '平均考试成绩', '学习人数']
print(effectiveness)

# 学生画像分析
print("\n学生画像分析：")
student_profile = full_data.groupby(['性别', '城市']).agg({
    '学生ID': 'nunique',
    '完成进度': 'mean',
    '考试成绩': 'mean'
}).round(2)
student_profile.columns = ['学生数量', '平均完成进度', '平均考试成绩']
print(student_profile.head(10))

# 课程受欢迎程度
print("\n课程受欢迎程度TOP10：")
course_popularity = full_data.groupby('课程名称').agg({
    '学生ID': 'nunique',
    '完成进度': 'mean',
    '考试成绩': 'mean'
}).round(2)
course_popularity.columns = ['选课人数', '平均完成进度', '平均考试成绩']
course_popularity = course_popularity.sort_values('选课人数', ascending=False)
print(course_popularity.head(10))

# 8.6 可视化总结
print("\n8.6 创建综合分析图表")
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('在线教育平台学习数据分析', fontsize=16)

# 课程类别学习效果
effectiveness[['平均完成进度', '平均考试成绩']].plot(kind='bar', ax=axes[0, 0])
axes[0, 0].set_title('各类别课程学习效果')
axes[0, 0].tick_params(axis='x', rotation=45)

# 完成进度分布
full_data['完成进度'].hist(bins=20, ax=axes[0, 1], alpha=0.7)
axes[0, 1].set_title('完成进度分布')
axes[0, 1].set_xlabel('完成进度(%)')
axes[0, 1].set_ylabel('学习记录数')

# 学习时长vs考试成绩散点图
valid_scores = full_data.dropna(subset=['考试成绩'])
axes[1, 0].scatter(valid_scores['学习时长'], valid_scores['考试成绩'], alpha=0.5)
axes[1, 0].set_xlabel('学习时长(小时)')
axes[1, 0].set_ylabel('考试成绩')
axes[1, 0].set_title('学习时长vs考试成绩')

# 性别分布
gender_dist = full_data['性别'].value_counts()
gender_dist.plot(kind='pie', ax=axes[1, 1], autopct='%1.1f%%')
axes[1, 1].set_title('学生性别分布')

plt.tight_layout()
plt.show()

print("\n" + "=" * 50)
print("所有练习题解答完成！")
print("\n主要知识点总结：")
print("1. DataFrame和Series的创建和基本操作")
print("2. 数据选择、筛选和查询")
print("3. 数据清洗：处理缺失值、重复值、异常值")
print("4. 描述性统计和相关性分析")
print("5. 数据分组和聚合操作")
print("6. 时间序列数据处理")
print("7. 数据合并和连接")
print("8. 综合项目：完整的数据分析流程")
print("\n建议：")
print("- 多练习不同类型的数据操作")
print("- 熟悉Pandas的各种方法和参数")
print("- 结合实际业务场景进行数据分析")
print("- 注重数据质量检查和清洗")
print("- 学会用可视化辅助数据分析")