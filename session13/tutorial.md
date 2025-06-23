# Session13: 数据分析 - Pandas 详细教程

## 1. Pandas简介

### 什么是Pandas？

Pandas（Python Data Analysis Library）是Python中最重要的数据分析库之一。它提供了高性能、易用的数据结构和数据分析工具，特别适合处理结构化数据。

### Pandas的优势

1. **强大的数据结构**：提供DataFrame和Series两种核心数据结构
2. **灵活的数据操作**：支持数据清洗、转换、合并等操作
3. **多种数据格式支持**：可读取CSV、Excel、JSON、SQL等多种格式
4. **高性能**：底层基于NumPy，运算效率高
5. **丰富的功能**：内置统计分析、时间序列处理等功能

### 安装Pandas

```bash
# 使用uv安装
uv add pandas

# 或使用pip安装
pip install pandas
```

## 2. Pandas核心数据结构

### 2.1 导入Pandas

```python
import pandas as pd
import numpy as np

# 查看版本
print(f"Pandas版本: {pd.__version__}")
```

### 2.2 Series（一维数据）

Series是一维标记数组，可以保存任何数据类型。

```python
# 从列表创建Series
data = [1, 2, 3, 4, 5]
s1 = pd.Series(data)
print("从列表创建Series:")
print(s1)
print()

# 指定索引
s2 = pd.Series(data, index=['a', 'b', 'c', 'd', 'e'])
print("指定索引的Series:")
print(s2)
print()

# 从字典创建Series
dict_data = {'北京': 2154, '上海': 2424, '广州': 1491, '深圳': 1756}
s3 = pd.Series(dict_data)
print("从字典创建Series:")
print(s3)
print()

# Series属性
print(f"Series值: {s3.values}")
print(f"Series索引: {s3.index}")
print(f"Series形状: {s3.shape}")
print(f"Series大小: {s3.size}")
```

### 2.3 DataFrame（二维数据）

DataFrame是二维标记数据结构，类似于Excel表格。

```python
# 从字典创建DataFrame
data = {
    '姓名': ['张三', '李四', '王五', '赵六'],
    '年龄': [25, 30, 35, 28],
    '城市': ['北京', '上海', '广州', '深圳'],
    '薪资': [8000, 12000, 10000, 9000]
}
df = pd.DataFrame(data)
print("从字典创建DataFrame:")
print(df)
print()

# 指定索引
df_with_index = pd.DataFrame(data, index=['员工1', '员工2', '员工3', '员工4'])
print("指定索引的DataFrame:")
print(df_with_index)
print()

# DataFrame属性
print(f"DataFrame形状: {df.shape}")
print(f"DataFrame列名: {df.columns.tolist()}")
print(f"DataFrame索引: {df.index.tolist()}")
print(f"DataFrame数据类型:\n{df.dtypes}")
```

## 3. 数据读取和写入

### 3.1 读取CSV文件

```python
# 创建示例CSV数据
sample_data = """
日期,产品,销量,价格
2024-01-01,产品A,100,50.0
2024-01-02,产品B,150,75.5
2024-01-03,产品A,120,50.0
2024-01-04,产品C,80,100.0
2024-01-05,产品B,200,75.5
"""

# 保存为CSV文件（实际项目中通常直接读取现有文件）
with open('sales_data.csv', 'w', encoding='utf-8') as f:
    f.write(sample_data)

# 读取CSV文件
df_csv = pd.read_csv('sales_data.csv')
print("读取CSV文件:")
print(df_csv)
print()

# 读取时指定参数
df_csv_params = pd.read_csv(
    'sales_data.csv',
    parse_dates=['日期'],  # 解析日期列
    index_col='日期'       # 设置日期为索引
)
print("指定参数读取CSV:")
print(df_csv_params)
```

### 3.2 写入文件

```python
# 写入CSV文件
df.to_csv('employees.csv', index=False, encoding='utf-8')
print("数据已保存到employees.csv")

# 写入Excel文件（需要安装openpyxl: uv add openpyxl）
# df.to_excel('employees.xlsx', index=False)

# 写入JSON文件
df.to_json('employees.json', orient='records', force_ascii=False)
print("数据已保存到employees.json")
```

## 4. 数据查看和基本信息

### 4.1 数据概览

```python
# 创建更大的示例数据集
np.random.seed(42)
n_rows = 1000

data_large = {
    '用户ID': range(1, n_rows + 1),
    '年龄': np.random.randint(18, 65, n_rows),
    '收入': np.random.normal(50000, 15000, n_rows),
    '消费金额': np.random.normal(2000, 500, n_rows),
    '城市': np.random.choice(['北京', '上海', '广州', '深圳', '杭州'], n_rows),
    '性别': np.random.choice(['男', '女'], n_rows)
}

df_large = pd.DataFrame(data_large)

# 查看前几行
print("前5行数据:")
print(df_large.head())
print()

# 查看后几行
print("后3行数据:")
print(df_large.tail(3))
print()

# 查看数据基本信息
print("数据基本信息:")
print(df_large.info())
print()

# 查看数值列的统计信息
print("数值列统计信息:")
print(df_large.describe())
print()

# 查看数据形状
print(f"数据形状: {df_large.shape}")
```

### 4.2 数据类型和内存使用

```python
# 查看数据类型
print("各列数据类型:")
print(df_large.dtypes)
print()

# 查看内存使用情况
print("内存使用情况:")
print(df_large.memory_usage(deep=True))
print()

# 查看唯一值数量
print("各列唯一值数量:")
print(df_large.nunique())
```

## 5. 数据选择和筛选

### 5.1 列选择

```python
# 选择单列
ages = df_large['年龄']
print("年龄列（Series）:")
print(ages.head())
print()

# 选择多列
subset = df_large[['用户ID', '年龄', '收入']]
print("选择多列:")
print(subset.head())
print()

# 使用点号访问列（列名不含空格时）
# user_ids = df_large.用户ID  # 这种方式不推荐，因为列名是中文
```

### 5.2 行选择

```python
# 使用iloc按位置选择
print("使用iloc选择前3行:")
print(df_large.iloc[:3])
print()

# 使用loc按标签选择
print("使用loc选择索引0-2的行:")
print(df_large.loc[0:2])
print()

# 选择特定行和列
print("选择前3行的年龄和收入列:")
print(df_large.loc[0:2, ['年龄', '收入']])
```

### 5.3 条件筛选

```python
# 单条件筛选
high_income = df_large[df_large['收入'] > 60000]
print(f"高收入用户数量: {len(high_income)}")
print("高收入用户前5行:")
print(high_income.head())
print()

# 多条件筛选
young_high_income = df_large[
    (df_large['年龄'] < 30) & (df_large['收入'] > 55000)
]
print(f"年轻高收入用户数量: {len(young_high_income)}")
print()

# 使用isin方法
big_cities = df_large[df_large['城市'].isin(['北京', '上海'])]
print(f"一线城市用户数量: {len(big_cities)}")
print()

# 字符串筛选
# 如果有字符串列，可以使用str方法
# df_large[df_large['某列'].str.contains('关键词')]
```

## 6. 数据清洗和处理

### 6.1 处理缺失值

```python
# 创建包含缺失值的数据
df_missing = df_large.copy()
# 随机设置一些缺失值
np.random.seed(42)
missing_indices = np.random.choice(df_missing.index, 50, replace=False)
df_missing.loc[missing_indices, '收入'] = np.nan

missing_indices2 = np.random.choice(df_missing.index, 30, replace=False)
df_missing.loc[missing_indices2, '消费金额'] = np.nan

print("缺失值统计:")
print(df_missing.isnull().sum())
print()

# 检查缺失值
print("是否有缺失值:")
print(df_missing.isnull().any())
print()

# 删除包含缺失值的行
df_dropna = df_missing.dropna()
print(f"删除缺失值后的数据形状: {df_dropna.shape}")

# 填充缺失值
df_filled = df_missing.copy()
# 用均值填充数值列
df_filled['收入'].fillna(df_filled['收入'].mean(), inplace=True)
df_filled['消费金额'].fillna(df_filled['消费金额'].median(), inplace=True)

print("填充后的缺失值统计:")
print(df_filled.isnull().sum())
```

### 6.2 数据类型转换

```python
# 转换数据类型
df_convert = df_large.copy()

# 将收入转换为整数
df_convert['收入'] = df_convert['收入'].astype(int)

# 将城市转换为分类类型（节省内存）
df_convert['城市'] = df_convert['城市'].astype('category')
df_convert['性别'] = df_convert['性别'].astype('category')

print("转换后的数据类型:")
print(df_convert.dtypes)
print()

print("内存使用对比:")
print(f"原始数据: {df_large.memory_usage(deep=True).sum()} bytes")
print(f"转换后: {df_convert.memory_usage(deep=True).sum()} bytes")
```

### 6.3 重复值处理

```python
# 检查重复值
print(f"重复行数量: {df_large.duplicated().sum()}")

# 创建一些重复数据进行演示
df_with_duplicates = pd.concat([df_large, df_large.head(10)])
print(f"添加重复后的数据形状: {df_with_duplicates.shape}")
print(f"重复行数量: {df_with_duplicates.duplicated().sum()}")

# 删除重复值
df_no_duplicates = df_with_duplicates.drop_duplicates()
print(f"删除重复后的数据形状: {df_no_duplicates.shape}")
```

## 7. 数据分组和聚合

### 7.1 基本分组操作

```python
# 按城市分组
city_groups = df_large.groupby('城市')

# 查看各城市的平均收入
print("各城市平均收入:")
print(city_groups['收入'].mean().sort_values(ascending=False))
print()

# 查看各城市的统计信息
print("各城市收入统计:")
print(city_groups['收入'].describe())
print()

# 多列分组
city_gender_groups = df_large.groupby(['城市', '性别'])
print("按城市和性别分组的平均收入:")
print(city_gender_groups['收入'].mean().unstack())
```

### 7.2 聚合函数

```python
# 使用agg方法进行多种聚合
agg_result = df_large.groupby('城市').agg({
    '年龄': ['mean', 'min', 'max'],
    '收入': ['mean', 'median', 'std'],
    '消费金额': ['sum', 'count']
})

print("多种聚合结果:")
print(agg_result)
print()

# 自定义聚合函数
def income_range(series):
    return series.max() - series.min()

custom_agg = df_large.groupby('城市')['收入'].agg([
    'mean',
    ('收入范围', income_range),
    ('高收入人数', lambda x: (x > 60000).sum())
])

print("自定义聚合结果:")
print(custom_agg)
```

## 8. 数据合并和连接

### 8.1 数据合并

```python
# 创建两个相关的DataFrame
df1 = pd.DataFrame({
    '用户ID': [1, 2, 3, 4],
    '姓名': ['张三', '李四', '王五', '赵六'],
    '年龄': [25, 30, 35, 28]
})

df2 = pd.DataFrame({
    '用户ID': [1, 2, 3, 5],
    '城市': ['北京', '上海', '广州', '深圳'],
    '薪资': [8000, 12000, 10000, 9000]
})

print("DataFrame 1:")
print(df1)
print()
print("DataFrame 2:")
print(df2)
print()

# 内连接
inner_join = pd.merge(df1, df2, on='用户ID', how='inner')
print("内连接结果:")
print(inner_join)
print()

# 左连接
left_join = pd.merge(df1, df2, on='用户ID', how='left')
print("左连接结果:")
print(left_join)
print()

# 外连接
outer_join = pd.merge(df1, df2, on='用户ID', how='outer')
print("外连接结果:")
print(outer_join)
```

### 8.2 数据拼接

```python
# 垂直拼接
df_concat_v = pd.concat([df1, df1], ignore_index=True)
print("垂直拼接:")
print(df_concat_v)
print()

# 水平拼接
df_concat_h = pd.concat([df1, df2.drop('用户ID', axis=1)], axis=1)
print("水平拼接:")
print(df_concat_h)
```

## 9. 时间序列处理

### 9.1 日期时间数据

```python
# 创建时间序列数据
dates = pd.date_range('2024-01-01', periods=100, freq='D')
ts_data = pd.DataFrame({
    '日期': dates,
    '销量': np.random.randint(50, 200, 100),
    '价格': np.random.uniform(10, 50, 100)
})

# 设置日期为索引
ts_data.set_index('日期', inplace=True)
print("时间序列数据:")
print(ts_data.head())
print()

# 按月重采样
monthly_data = ts_data.resample('M').agg({
    '销量': 'sum',
    '价格': 'mean'
})
print("按月汇总:")
print(monthly_data)
print()

# 计算移动平均
ts_data['销量_7日均值'] = ts_data['销量'].rolling(window=7).mean()
print("添加移动平均后:")
print(ts_data.head(10))
```

### 9.2 日期时间操作

```python
# 提取日期组件
ts_data['年'] = ts_data.index.year
ts_data['月'] = ts_data.index.month
ts_data['星期几'] = ts_data.index.dayofweek

print("提取日期组件:")
print(ts_data.head())
print()

# 按星期几分组分析
weekday_analysis = ts_data.groupby('星期几')['销量'].mean()
print("各星期几的平均销量:")
print(weekday_analysis)
```

## 10. 数据可视化基础

### 10.1 基本图表

```python
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

# 直方图
plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
df_large['年龄'].hist(bins=20)
plt.title('年龄分布')
plt.xlabel('年龄')
plt.ylabel('频数')

# 散点图
plt.subplot(2, 2, 2)
plt.scatter(df_large['年龄'], df_large['收入'], alpha=0.5)
plt.title('年龄与收入关系')
plt.xlabel('年龄')
plt.ylabel('收入')

# 箱线图
plt.subplot(2, 2, 3)
df_large.boxplot(column='收入', by='城市', ax=plt.gca())
plt.title('各城市收入分布')
plt.suptitle('')  # 移除自动标题

# 柱状图
plt.subplot(2, 2, 4)
city_counts = df_large['城市'].value_counts()
city_counts.plot(kind='bar')
plt.title('各城市用户数量')
plt.xlabel('城市')
plt.ylabel('用户数量')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
```

### 10.2 Pandas内置绘图

```python
# 使用Pandas内置绘图功能
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# 线图
ts_data['销量'].plot(ax=axes[0, 0], title='销量趋势')

# 柱状图
df_large.groupby('城市')['收入'].mean().plot(kind='bar', ax=axes[0, 1], title='各城市平均收入')

# 饼图
df_large['性别'].value_counts().plot(kind='pie', ax=axes[1, 0], title='性别分布', autopct='%1.1f%%')

# 相关性热力图
corr_matrix = df_large[['年龄', '收入', '消费金额']].corr()
im = axes[1, 1].imshow(corr_matrix, cmap='coolwarm', aspect='auto')
axes[1, 1].set_xticks(range(len(corr_matrix.columns)))
axes[1, 1].set_yticks(range(len(corr_matrix.columns)))
axes[1, 1].set_xticklabels(corr_matrix.columns)
axes[1, 1].set_yticklabels(corr_matrix.columns)
axes[1, 1].set_title('相关性矩阵')

# 添加相关系数文本
for i in range(len(corr_matrix.columns)):
    for j in range(len(corr_matrix.columns)):
        axes[1, 1].text(j, i, f'{corr_matrix.iloc[i, j]:.2f}', 
                        ha='center', va='center')

plt.tight_layout()
plt.show()
```

## 11. 实用技巧和最佳实践

### 11.1 性能优化

```python
# 使用分类数据类型节省内存
df_optimized = df_large.copy()
for col in ['城市', '性别']:
    df_optimized[col] = df_optimized[col].astype('category')

print("内存使用对比:")
print(f"原始: {df_large.memory_usage(deep=True).sum():,} bytes")
print(f"优化后: {df_optimized.memory_usage(deep=True).sum():,} bytes")
print()

# 使用query方法进行复杂筛选
result = df_large.query('年龄 > 30 and 收入 > 50000 and 城市 in ["北京", "上海"]')
print(f"Query方法筛选结果: {len(result)} 行")
```

### 11.2 链式操作

```python
# 使用方法链进行数据处理
result = (df_large
          .query('收入 > 40000')
          .groupby('城市')
          .agg({'收入': 'mean', '年龄': 'mean'})
          .round(2)
          .sort_values('收入', ascending=False))

print("链式操作结果:")
print(result)
```

### 11.3 常用数据处理模式

```python
# 数据透视表
pivot_table = pd.pivot_table(
    df_large,
    values='收入',
    index='城市',
    columns='性别',
    aggfunc='mean',
    fill_value=0
)
print("数据透视表:")
print(pivot_table)
print()

# 交叉表
crosstab = pd.crosstab(df_large['城市'], df_large['性别'], normalize='index')
print("交叉表（比例）:")
print(crosstab)
```

## 12. 总结

### 关键概念回顾

1. **Series和DataFrame**：Pandas的两种核心数据结构
2. **数据读写**：支持多种格式的数据导入导出
3. **数据选择**：iloc、loc、条件筛选等方法
4. **数据清洗**：处理缺失值、重复值、数据类型转换
5. **分组聚合**：groupby操作和各种聚合函数
6. **数据合并**：merge、concat等数据连接方法
7. **时间序列**：日期时间数据的处理和分析
8. **数据可视化**：基本图表绘制

### 学习建议

1. **多练习真实数据**：使用实际的数据集进行练习
2. **掌握核心方法**：重点掌握常用的数据操作方法
3. **注意性能**：了解如何优化Pandas操作的性能
4. **结合可视化**：数据分析要结合图表展示
5. **持续学习**：Pandas功能丰富，需要持续学习新特性

### 下一步学习方向

- 深入学习数据可视化（Matplotlib、Seaborn）
- 学习机器学习库（Scikit-learn）
- 掌握大数据处理工具（Dask）
- 学习数据库操作（SQLAlchemy）

---

**记住**：数据分析是一个实践性很强的技能，多动手操作真实数据，才能真正掌握Pandas的精髓！