#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pandas高级练习题解答

本文件包含advanced_exercises.py中所有练习题的详细解答。
涵盖高级分组操作、数据透视、时间序列分析、性能优化等高级主题。

作者: Python教程团队
创建日期: 2024-01-01
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
import time
from functools import wraps

# 设置
warnings.filterwarnings('ignore')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")

# 性能测试装饰器
def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 执行时间: {end_time - start_time:.4f} 秒")
        return result
    return wrapper

print("Pandas高级练习题解答")
print("=" * 50)

# ==================== 练习1：高级分组操作 ====================
print("\n练习1：高级分组操作")
print("-" * 30)

# 1.1 创建复杂的销售数据
print("\n1.1 创建复杂的销售数据")
np.random.seed(42)

# 生成更复杂的销售数据
dates = pd.date_range('2023-01-01', '2024-12-31', freq='D')
products = ['iPhone', 'Samsung', 'Huawei', 'Xiaomi', 'Oppo']
regions = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉']
salespeople = ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九']

sales_data = []
for _ in range(10000):
    sales_data.append({
        '日期': np.random.choice(dates),
        '产品': np.random.choice(products),
        '地区': np.random.choice(regions),
        '销售员': np.random.choice(salespeople),
        '销量': np.random.randint(1, 20),
        '单价': np.random.uniform(3000, 8000),
        '成本': np.random.uniform(2000, 5000)
    })

sales_df = pd.DataFrame(sales_data)
sales_df['销售额'] = sales_df['销量'] * sales_df['单价']
sales_df['利润'] = sales_df['销售额'] - (sales_df['销量'] * sales_df['成本'])
sales_df['利润率'] = sales_df['利润'] / sales_df['销售额']

print(f"销售数据形状: {sales_df.shape}")
print("\n销售数据样例：")
print(sales_df.head())

# 1.2 多级分组聚合
print("\n1.2 多级分组聚合")
print("\n按产品和地区分组的详细统计：")
multi_group_stats = sales_df.groupby(['产品', '地区']).agg({
    '销量': ['sum', 'mean', 'count'],
    '销售额': ['sum', 'mean', 'std'],
    '利润': ['sum', 'mean'],
    '利润率': ['mean', 'std']
}).round(2)

# 重命名列
multi_group_stats.columns = ['总销量', '平均销量', '订单数', '总销售额', '平均销售额', '销售额标准差', 
                            '总利润', '平均利润', '平均利润率', '利润率标准差']
print(multi_group_stats.head(10))

# 1.3 自定义聚合函数
print("\n1.3 自定义聚合函数")

def coefficient_of_variation(series):
    """变异系数：标准差/均值"""
    return series.std() / series.mean() if series.mean() != 0 else 0

def sales_efficiency(group):
    """销售效率：总利润/总销量"""
    return group['利润'].sum() / group['销量'].sum() if group['销量'].sum() != 0 else 0

def top_performer_count(series):
    """高绩效订单数量（前20%）"""
    threshold = series.quantile(0.8)
    return (series >= threshold).sum()

# 应用自定义聚合
custom_agg = sales_df.groupby('产品').agg({
    '销售额': [coefficient_of_variation, 'mean'],
    '利润率': ['mean', 'std', top_performer_count]
}).round(4)

custom_agg.columns = ['销售额变异系数', '平均销售额', '平均利润率', '利润率标准差', '高绩效订单数']
print("\n自定义聚合结果：")
print(custom_agg)

# 1.4 分组应用自定义函数
print("\n1.4 分组应用自定义函数")

def analyze_sales_trend(group):
    """分析销售趋势"""
    group = group.sort_values('日期')
    
    # 计算趋势
    if len(group) > 1:
        x = np.arange(len(group))
        y = group['销售额'].values
        trend = np.polyfit(x, y, 1)[0]  # 线性趋势斜率
    else:
        trend = 0
    
    return pd.Series({
        '订单数': len(group),
        '总销售额': group['销售额'].sum(),
        '平均订单金额': group['销售额'].mean(),
        '销售趋势': trend,
        '最佳单日销售': group['销售额'].max(),
        '销售稳定性': 1 / (group['销售额'].std() + 1)  # 稳定性指标
    })

trend_analysis = sales_df.groupby('销售员').apply(analyze_sales_trend).round(2)
print("\n销售员趋势分析：")
print(trend_analysis.sort_values('总销售额', ascending=False))

# 1.5 滚动分组操作
print("\n1.5 滚动分组操作")
sales_df_sorted = sales_df.sort_values('日期')

# 按产品分组，计算滚动统计
rolling_stats = sales_df_sorted.groupby('产品')['销售额'].rolling(window=30, min_periods=1).agg({
    '滚动均值': 'mean',
    '滚动标准差': 'std',
    '滚动最大值': 'max'
}).round(2)

print("\n滚动统计样例（iPhone产品）：")
iphone_rolling = rolling_stats.loc['iPhone'].tail(10)
print(iphone_rolling)

# ==================== 练习2：数据透视和重塑 ====================
print("\n\n练习2：数据透视和重塑")
print("-" * 30)

# 2.1 基础数据透视表
print("\n2.1 基础数据透视表")
basic_pivot = pd.pivot_table(
    sales_df,
    values='销售额',
    index='产品',
    columns='地区',
    aggfunc='sum',
    fill_value=0
).round(2)

print("\n产品-地区销售额透视表：")
print(basic_pivot)

# 2.2 多值透视表
print("\n2.2 多值透视表")
multi_value_pivot = pd.pivot_table(
    sales_df,
    values=['销售额', '利润', '销量'],
    index='产品',
    columns='地区',
    aggfunc={'销售额': 'sum', '利润': 'sum', '销量': 'sum'},
    fill_value=0
).round(2)

print("\n多指标透视表样例：")
print(multi_value_pivot.head())

# 2.3 多级索引透视表
print("\n2.3 多级索引透视表")
sales_df['月份'] = sales_df['日期'].dt.to_period('M')
multi_index_pivot = pd.pivot_table(
    sales_df,
    values='销售额',
    index=['产品', '销售员'],
    columns='月份',
    aggfunc='sum',
    fill_value=0
).round(2)

print("\n多级索引透视表样例：")
print(multi_index_pivot.iloc[:10, :5])  # 显示前10行，前5列

# 2.4 数据重塑：melt操作
print("\n2.4 数据重塑：melt操作")
# 创建宽格式数据
wide_data = pd.DataFrame({
    '产品': ['A', 'B', 'C'],
    'Q1': [100, 150, 120],
    'Q2': [110, 140, 130],
    'Q3': [120, 160, 125],
    'Q4': [130, 170, 135]
})

print("\n原始宽格式数据：")
print(wide_data)

# 转换为长格式
long_data = pd.melt(
    wide_data,
    id_vars=['产品'],
    value_vars=['Q1', 'Q2', 'Q3', 'Q4'],
    var_name='季度',
    value_name='销量'
)

print("\n转换后的长格式数据：")
print(long_data)

# 2.5 stack和unstack操作
print("\n2.5 stack和unstack操作")
# 使用多级索引数据
multi_index_data = sales_df.groupby(['产品', '地区'])['销售额'].sum().unstack(fill_value=0)
print("\n unstack后的数据：")
print(multi_index_data.head())

# stack回去
stacked_data = multi_index_data.stack()
print("\n stack后的数据样例：")
print(stacked_data.head(10))

# 2.6 交叉表
print("\n2.6 交叉表")
crosstab_result = pd.crosstab(
    sales_df['产品'],
    sales_df['地区'],
    values=sales_df['销售额'],
    aggfunc='sum',
    normalize='index'  # 按行标准化
).round(3)

print("\n产品-地区交叉表（行标准化）：")
print(crosstab_result)

# ==================== 练习3：高级时间序列分析 ====================
print("\n\n练习3：高级时间序列分析")
print("-" * 30)

# 3.1 创建复杂时间序列数据
print("\n3.1 创建复杂时间序列数据")
np.random.seed(42)

# 生成多个时间序列
dates = pd.date_range('2020-01-01', '2024-12-31', freq='D')
n_days = len(dates)

# 模拟股票价格（包含趋势、季节性、噪声）
def generate_stock_price(base_price, trend, seasonality_amplitude, noise_level):
    # 趋势分量
    trend_component = np.linspace(0, trend, n_days)
    
    # 季节性分量（年度周期）
    seasonal_component = seasonality_amplitude * np.sin(2 * np.pi * np.arange(n_days) / 365.25)
    
    # 噪声分量
    noise_component = np.random.normal(0, noise_level, n_days)
    
    # 组合所有分量
    prices = base_price + trend_component + seasonal_component + noise_component
    
    # 确保价格为正
    prices = np.maximum(prices, base_price * 0.1)
    
    return prices

# 生成多只股票数据
stocks = {
    'AAPL': generate_stock_price(150, 50, 10, 5),
    'GOOGL': generate_stock_price(2000, 300, 100, 50),
    'TSLA': generate_stock_price(200, 400, 50, 20),
    'MSFT': generate_stock_price(250, 100, 15, 8)
}

stock_df = pd.DataFrame(stocks, index=dates)
print(f"股票数据形状: {stock_df.shape}")
print("\n股票数据样例：")
print(stock_df.head())

# 3.2 时间序列分解
print("\n3.2 时间序列分解")

def decompose_time_series(series, period=365):
    """简单的时间序列分解"""
    # 趋势（移动平均）
    trend = series.rolling(window=period, center=True).mean()
    
    # 去趋势
    detrended = series - trend
    
    # 季节性（按周期分组的平均值）
    seasonal = detrended.groupby(detrended.index.dayofyear).transform('mean')
    
    # 残差
    residual = detrended - seasonal
    
    return pd.DataFrame({
        '原始': series,
        '趋势': trend,
        '季节性': seasonal,
        '残差': residual
    })

# 分解AAPL股价
aapl_decomp = decompose_time_series(stock_df['AAPL'])
print("\nAAPL股价分解结果样例：")
print(aapl_decomp.dropna().head(10))

# 3.3 技术指标计算
print("\n3.3 技术指标计算")

def calculate_technical_indicators(df):
    """计算技术指标"""
    result = df.copy()
    
    for col in df.columns:
        # 移动平均线
        result[f'{col}_MA5'] = df[col].rolling(5).mean()
        result[f'{col}_MA20'] = df[col].rolling(20).mean()
        result[f'{col}_MA50'] = df[col].rolling(50).mean()
        
        # 布林带
        ma20 = df[col].rolling(20).mean()
        std20 = df[col].rolling(20).std()
        result[f'{col}_BB_Upper'] = ma20 + 2 * std20
        result[f'{col}_BB_Lower'] = ma20 - 2 * std20
        
        # RSI（相对强弱指数）
        delta = df[col].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        result[f'{col}_RSI'] = 100 - (100 / (1 + rs))
        
        # 波动率
        result[f'{col}_Volatility'] = df[col].rolling(20).std()
    
    return result

tech_indicators = calculate_technical_indicators(stock_df)
print("\n技术指标样例（AAPL相关）：")
aapl_indicators = tech_indicators[['AAPL', 'AAPL_MA5', 'AAPL_MA20', 'AAPL_RSI', 'AAPL_Volatility']].dropna()
print(aapl_indicators.tail(10))

# 3.4 相关性分析
print("\n3.4 股票相关性分析")
correlation_matrix = stock_df.corr()
print("\n股票相关性矩阵：")
print(correlation_matrix.round(3))

# 滚动相关性
print("\n滚动相关性分析（AAPL vs MSFT）：")
rolling_corr = stock_df['AAPL'].rolling(60).corr(stock_df['MSFT'])
print(f"平均滚动相关性: {rolling_corr.mean():.3f}")
print(f"相关性标准差: {rolling_corr.std():.3f}")

# 3.5 时间序列重采样和聚合
print("\n3.5 时间序列重采样和聚合")

# 月度聚合
monthly_stats = stock_df.resample('M').agg({
    'AAPL': ['first', 'last', 'max', 'min', 'mean'],
    'GOOGL': ['first', 'last', 'max', 'min', 'mean']
}).round(2)

print("\n月度统计样例：")
print(monthly_stats.head())

# 季度收益率
quarterly_returns = stock_df.resample('Q').last().pct_change().round(4)
print("\n季度收益率：")
print(quarterly_returns.head())

# 3.6 时间序列可视化
print("\n3.6 创建时间序列分析图表")
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('股票时间序列分析', fontsize=16)

# 股价走势
stock_df[['AAPL', 'MSFT']].plot(ax=axes[0, 0])
axes[0, 0].set_title('股价走势')
axes[0, 0].set_ylabel('价格')

# 技术指标
aapl_with_ma = tech_indicators[['AAPL', 'AAPL_MA5', 'AAPL_MA20']].dropna()
aapl_with_ma.tail(252).plot(ax=axes[0, 1])  # 最近一年
axes[0, 1].set_title('AAPL技术指标')
axes[0, 1].set_ylabel('价格')

# 相关性热力图
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, ax=axes[1, 0])
axes[1, 0].set_title('股票相关性矩阵')

# 波动率
volatility_data = tech_indicators[['AAPL_Volatility', 'GOOGL_Volatility', 'TSLA_Volatility', 'MSFT_Volatility']].dropna()
volatility_data.tail(252).plot(ax=axes[1, 1])
axes[1, 1].set_title('股票波动率')
axes[1, 1].set_ylabel('波动率')

plt.tight_layout()
plt.show()

# ==================== 练习4：性能优化 ====================
print("\n\n练习4：性能优化")
print("-" * 30)

# 4.1 创建大数据集
print("\n4.1 创建大数据集进行性能测试")
np.random.seed(42)

# 生成大数据集
n_rows = 1000000
large_df = pd.DataFrame({
    'id': range(n_rows),
    'category': np.random.choice(['A', 'B', 'C', 'D', 'E'], n_rows),
    'value1': np.random.randn(n_rows),
    'value2': np.random.randn(n_rows),
    'date': pd.date_range('2020-01-01', periods=n_rows, freq='1min')
})

print(f"大数据集形状: {large_df.shape}")
print(f"内存使用: {large_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# 4.2 性能对比：不同的分组方法
print("\n4.2 性能对比：不同的分组方法")

@timing_decorator
def groupby_standard(df):
    """标准分组方法"""
    return df.groupby('category')['value1'].mean()

@timing_decorator
def groupby_with_sort(df):
    """预排序后分组"""
    df_sorted = df.sort_values('category')
    return df_sorted.groupby('category', sort=False)['value1'].mean()

@timing_decorator
def groupby_categorical(df):
    """使用分类数据类型"""
    df_cat = df.copy()
    df_cat['category'] = df_cat['category'].astype('category')
    return df_cat.groupby('category')['value1'].mean()

print("\n性能测试结果：")
result1 = groupby_standard(large_df)
result2 = groupby_with_sort(large_df)
result3 = groupby_categorical(large_df)

# 4.3 内存优化
print("\n4.3 内存优化")

def optimize_memory(df):
    """优化DataFrame内存使用"""
    optimized_df = df.copy()
    
    # 优化数值列
    for col in optimized_df.select_dtypes(include=['int64']).columns:
        col_min = optimized_df[col].min()
        col_max = optimized_df[col].max()
        
        if col_min >= 0:
            if col_max < 255:
                optimized_df[col] = optimized_df[col].astype('uint8')
            elif col_max < 65535:
                optimized_df[col] = optimized_df[col].astype('uint16')
            elif col_max < 4294967295:
                optimized_df[col] = optimized_df[col].astype('uint32')
        else:
            if col_min > -128 and col_max < 127:
                optimized_df[col] = optimized_df[col].astype('int8')
            elif col_min > -32768 and col_max < 32767:
                optimized_df[col] = optimized_df[col].astype('int16')
            elif col_min > -2147483648 and col_max < 2147483647:
                optimized_df[col] = optimized_df[col].astype('int32')
    
    # 优化浮点数列
    for col in optimized_df.select_dtypes(include=['float64']).columns:
        optimized_df[col] = optimized_df[col].astype('float32')
    
    # 优化字符串列
    for col in optimized_df.select_dtypes(include=['object']).columns:
        if optimized_df[col].nunique() / len(optimized_df) < 0.5:  # 如果唯一值比例小于50%
            optimized_df[col] = optimized_df[col].astype('category')
    
    return optimized_df

print("\n内存优化前后对比：")
original_memory = large_df.memory_usage(deep=True).sum() / 1024**2
optimized_df = optimize_memory(large_df)
optimized_memory = optimized_df.memory_usage(deep=True).sum() / 1024**2

print(f"原始内存使用: {original_memory:.2f} MB")
print(f"优化后内存使用: {optimized_memory:.2f} MB")
print(f"内存节省: {(1 - optimized_memory/original_memory)*100:.1f}%")

# 4.4 向量化操作vs循环
print("\n4.4 向量化操作vs循环")

# 创建测试数据
test_df = pd.DataFrame({
    'a': np.random.randn(100000),
    'b': np.random.randn(100000)
})

@timing_decorator
def loop_calculation(df):
    """使用循环计算"""
    result = []
    for i in range(len(df)):
        result.append(df.iloc[i]['a'] * df.iloc[i]['b'] + 1)
    return result

@timing_decorator
def vectorized_calculation(df):
    """使用向量化计算"""
    return df['a'] * df['b'] + 1

@timing_decorator
def apply_calculation(df):
    """使用apply计算"""
    return df.apply(lambda row: row['a'] * row['b'] + 1, axis=1)

print("\n计算性能对比：")
result_loop = loop_calculation(test_df)
result_vectorized = vectorized_calculation(test_df)
result_apply = apply_calculation(test_df)

# 4.5 查询优化
print("\n4.5 查询优化")

@timing_decorator
def query_boolean_indexing(df):
    """布尔索引查询"""
    return df[(df['value1'] > 0) & (df['category'] == 'A')]

@timing_decorator
def query_method(df):
    """query方法查询"""
    return df.query("value1 > 0 and category == 'A'")

@timing_decorator
def query_with_index(df):
    """使用索引查询"""
    df_indexed = df.set_index('category')
    return df_indexed.loc['A'][df_indexed.loc['A']['value1'] > 0]

print("\n查询性能对比：")
result_bool = query_boolean_indexing(large_df)
result_query = query_method(large_df)
result_index = query_with_index(large_df)

# ==================== 练习5：真实世界场景应用 ====================
print("\n\n练习5：真实世界场景应用")
print("-" * 30)

# 5.1 客户流失分析
print("\n5.1 客户流失分析")

# 生成客户数据
np.random.seed(42)
n_customers = 10000

customer_data = pd.DataFrame({
    '客户ID': range(1, n_customers + 1),
    '注册日期': pd.date_range('2020-01-01', periods=n_customers, freq='H'),
    '年龄': np.random.randint(18, 70, n_customers),
    '性别': np.random.choice(['男', '女'], n_customers),
    '城市等级': np.random.choice(['一线', '二线', '三线'], n_customers, p=[0.3, 0.4, 0.3]),
    '月收入': np.random.lognormal(9, 0.8, n_customers),
    '最后活跃日期': pd.date_range('2024-01-01', periods=n_customers, freq='H'),
    '总消费金额': np.random.lognormal(7, 1.5, n_customers),
    '订单数量': np.random.poisson(5, n_customers),
    '平均订单金额': np.random.lognormal(5, 0.8, n_customers)
})

# 计算客户特征
current_date = pd.Timestamp('2024-12-31')
customer_data['注册天数'] = (current_date - customer_data['注册日期']).dt.days
customer_data['最后活跃天数'] = (current_date - customer_data['最后活跃日期']).dt.days
customer_data['客户生命周期'] = customer_data['注册天数']
customer_data['平均消费频率'] = customer_data['订单数量'] / (customer_data['注册天数'] + 1) * 30  # 月均订单

# 定义流失客户（超过90天未活跃）
customer_data['是否流失'] = customer_data['最后活跃天数'] > 90

print(f"总客户数: {len(customer_data)}")
print(f"流失客户数: {customer_data['是否流失'].sum()}")
print(f"流失率: {customer_data['是否流失'].mean()*100:.2f}%")

# 流失分析
churn_analysis = customer_data.groupby('是否流失').agg({
    '年龄': 'mean',
    '月收入': 'mean',
    '总消费金额': 'mean',
    '订单数量': 'mean',
    '平均订单金额': 'mean',
    '平均消费频率': 'mean',
    '客户ID': 'count'
}).round(2)

churn_analysis.columns = ['平均年龄', '平均月收入', '平均总消费', '平均订单数', '平均订单金额', '平均消费频率', '客户数量']
print("\n流失vs活跃客户对比：")
print(churn_analysis)

# 5.2 RFM分析
print("\n5.2 RFM客户价值分析")

# 计算RFM指标
rfm_data = customer_data.copy()
rfm_data['R_Score'] = pd.qcut(rfm_data['最后活跃天数'], 5, labels=[5,4,3,2,1])  # 最近性（越小越好）
rfm_data['F_Score'] = pd.qcut(rfm_data['平均消费频率'].rank(method='first'), 5, labels=[1,2,3,4,5])  # 频率
rfm_data['M_Score'] = pd.qcut(rfm_data['总消费金额'], 5, labels=[1,2,3,4,5])  # 货币价值

# 计算RFM综合得分
rfm_data['RFM_Score'] = (rfm_data['R_Score'].astype(int) + 
                        rfm_data['F_Score'].astype(int) + 
                        rfm_data['M_Score'].astype(int))

# 客户分层
def classify_customer_rfm(row):
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

rfm_data['客户分层'] = rfm_data.apply(classify_customer_rfm, axis=1)

rfm_summary = rfm_data.groupby('客户分层').agg({
    '客户ID': 'count',
    '总消费金额': 'mean',
    '平均消费频率': 'mean',
    '最后活跃天数': 'mean'
}).round(2)

rfm_summary.columns = ['客户数量', '平均消费金额', '平均消费频率', '平均最后活跃天数']
print("\nRFM客户分层结果：")
print(rfm_summary)

# 5.3 同期群分析
print("\n5.3 同期群分析")

# 按注册月份分组
customer_data['注册月份'] = customer_data['注册日期'].dt.to_period('M')
customer_data['活跃月份'] = customer_data['最后活跃日期'].dt.to_period('M')

# 计算每个同期群的留存情况
cohort_data = customer_data.groupby('注册月份')['客户ID'].nunique().reset_index()
cohort_data.columns = ['注册月份', '初始客户数']

# 计算各月份的活跃客户数
active_customers = customer_data.groupby(['注册月份', '活跃月份'])['客户ID'].nunique().reset_index()
active_customers.columns = ['注册月份', '活跃月份', '活跃客户数']

# 合并数据
cohort_analysis = active_customers.merge(cohort_data, on='注册月份')
cohort_analysis['留存率'] = cohort_analysis['活跃客户数'] / cohort_analysis['初始客户数']

print("\n同期群分析样例：")
print(cohort_analysis.head(10))

# 5.4 产品关联分析
print("\n5.4 产品关联分析")

# 生成购物篮数据
np.random.seed(42)
products = ['手机', '耳机', '充电器', '手机壳', '数据线', '移动电源', '蓝牙音箱', '平板', '笔记本', '鼠标']

# 生成交易数据
transactions = []
for i in range(10000):
    # 每个交易包含1-5个产品
    n_products = np.random.randint(1, 6)
    transaction_products = np.random.choice(products, n_products, replace=False)
    
    for product in transaction_products:
        transactions.append({
            '交易ID': i,
            '产品': product
        })

transaction_df = pd.DataFrame(transactions)

# 创建购物篮矩阵
basket = transaction_df.groupby(['交易ID', '产品'])['产品'].count().unstack(fill_value=0)
basket = basket.applymap(lambda x: 1 if x > 0 else 0)

print(f"\n购物篮数据形状: {basket.shape}")
print("购物篮样例：")
print(basket.head())

# 计算支持度
support = basket.mean()
print("\n产品支持度（购买频率）：")
print(support.sort_values(ascending=False))

# 计算关联规则（简化版）
from itertools import combinations

def calculate_confidence(antecedent, consequent, basket_df):
    """计算置信度"""
    antecedent_support = (basket_df[antecedent] == 1).sum()
    both_support = ((basket_df[antecedent] == 1) & (basket_df[consequent] == 1)).sum()
    
    if antecedent_support == 0:
        return 0
    return both_support / antecedent_support

# 计算常见产品对的关联度
product_pairs = list(combinations(products[:5], 2))  # 只分析前5个产品的组合
association_rules = []

for prod1, prod2 in product_pairs:
    conf_1_to_2 = calculate_confidence(prod1, prod2, basket)
    conf_2_to_1 = calculate_confidence(prod2, prod1, basket)
    
    association_rules.append({
        '规则': f'{prod1} -> {prod2}',
        '置信度': conf_1_to_2
    })
    association_rules.append({
        '规则': f'{prod2} -> {prod1}',
        '置信度': conf_2_to_1
    })

association_df = pd.DataFrame(association_rules)
association_df = association_df.sort_values('置信度', ascending=False)

print("\n产品关联规则TOP10：")
print(association_df.head(10))

# ==================== 练习6：数据质量和验证 ====================
print("\n\n练习6：数据质量和验证")
print("-" * 30)

# 6.1 数据质量检查框架
print("\n6.1 数据质量检查框架")

class DataQualityChecker:
    """数据质量检查器"""
    
    def __init__(self, df):
        self.df = df
        self.quality_report = {}
    
    def check_completeness(self):
        """完整性检查"""
        missing_stats = self.df.isnull().sum()
        missing_pct = (missing_stats / len(self.df) * 100).round(2)
        
        self.quality_report['completeness'] = {
            'missing_values': missing_stats.to_dict(),
            'missing_percentage': missing_pct.to_dict(),
            'total_missing': missing_stats.sum(),
            'columns_with_missing': (missing_stats > 0).sum()
        }
        
        return missing_stats
    
    def check_uniqueness(self):
        """唯一性检查"""
        duplicate_rows = self.df.duplicated().sum()
        
        uniqueness_stats = {}
        for col in self.df.columns:
            total_values = len(self.df[col])
            unique_values = self.df[col].nunique()
            uniqueness_stats[col] = {
                'unique_count': unique_values,
                'uniqueness_ratio': unique_values / total_values if total_values > 0 else 0
            }
        
        self.quality_report['uniqueness'] = {
            'duplicate_rows': duplicate_rows,
            'column_uniqueness': uniqueness_stats
        }
        
        return duplicate_rows
    
    def check_validity(self):
        """有效性检查"""
        validity_issues = {}
        
        for col in self.df.select_dtypes(include=[np.number]).columns:
            # 检查异常值（使用IQR方法）
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = ((self.df[col] < lower_bound) | (self.df[col] > upper_bound)).sum()
            validity_issues[col] = {
                'outliers': outliers,
                'outlier_percentage': outliers / len(self.df) * 100
            }
        
        self.quality_report['validity'] = validity_issues
        return validity_issues
    
    def check_consistency(self):
        """一致性检查"""
        consistency_issues = {}
        
        # 检查数据类型一致性
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                # 检查字符串格式一致性
                has_leading_spaces = self.df[col].astype(str).str.startswith(' ').sum()
                has_trailing_spaces = self.df[col].astype(str).str.endswith(' ').sum()
                
                consistency_issues[col] = {
                    'leading_spaces': has_leading_spaces,
                    'trailing_spaces': has_trailing_spaces
                }
        
        self.quality_report['consistency'] = consistency_issues
        return consistency_issues
    
    def generate_report(self):
        """生成完整的质量报告"""
        print("执行数据质量检查...")
        
        self.check_completeness()
        self.check_uniqueness()
        self.check_validity()
        self.check_consistency()
        
        print("\n=== 数据质量报告 ===")
        print(f"数据集形状: {self.df.shape}")
        print(f"总缺失值: {self.quality_report['completeness']['total_missing']}")
        print(f"重复行数: {self.quality_report['uniqueness']['duplicate_rows']}")
        
        # 质量评分
        completeness_score = 1 - (self.quality_report['completeness']['total_missing'] / (self.df.shape[0] * self.df.shape[1]))
        uniqueness_score = 1 - (self.quality_report['uniqueness']['duplicate_rows'] / self.df.shape[0])
        
        overall_score = (completeness_score + uniqueness_score) / 2
        
        print(f"\n质量评分:")
        print(f"完整性得分: {completeness_score:.3f}")
        print(f"唯一性得分: {uniqueness_score:.3f}")
        print(f"总体质量得分: {overall_score:.3f}")
        
        return self.quality_report

# 使用质量检查器
quality_checker = DataQualityChecker(customer_data)
quality_report = quality_checker.generate_report()

# 6.2 数据验证规则
print("\n6.2 数据验证规则")

def validate_customer_data(df):
    """客户数据验证"""
    validation_results = []
    
    # 规则1：年龄应该在合理范围内
    age_invalid = ((df['年龄'] < 18) | (df['年龄'] > 100)).sum()
    validation_results.append({
        '规则': '年龄范围检查',
        '违规数量': age_invalid,
        '通过': age_invalid == 0
    })
    
    # 规则2：收入应该为正数
    income_invalid = (df['月收入'] <= 0).sum()
    validation_results.append({
        '规则': '收入正数检查',
        '违规数量': income_invalid,
        '通过': income_invalid == 0
    })
    
    # 规则3：注册日期应该早于最后活跃日期
    date_invalid = (df['注册日期'] > df['最后活跃日期']).sum()
    validation_results.append({
        '规则': '日期逻辑检查',
        '违规数量': date_invalid,
        '通过': date_invalid == 0
    })
    
    # 规则4：总消费应该大于等于平均订单金额
    consumption_invalid = (df['总消费金额'] < df['平均订单金额']).sum()
    validation_results.append({
        '规则': '消费逻辑检查',
        '违规数量': consumption_invalid,
        '通过': consumption_invalid == 0
    })
    
    return pd.DataFrame(validation_results)

validation_results = validate_customer_data(customer_data)
print("\n数据验证结果：")
print(validation_results)

# ==================== 练习7：高级数据可视化 ====================
print("\n\n练习7：高级数据可视化")
print("-" * 30)

# 7.1 创建综合仪表板
print("\n7.1 创建综合数据分析仪表板")

fig = plt.figure(figsize=(20, 15))
fig.suptitle('电商平台综合数据分析仪表板', fontsize=20)

# 创建网格布局
gs = fig.add_gridspec(4, 4, hspace=0.3, wspace=0.3)

# 1. 客户分层饼图
ax1 = fig.add_subplot(gs[0, 0])
customer_segment_counts = rfm_data['客户分层'].value_counts()
customer_segment_counts.plot(kind='pie', ax=ax1, autopct='%1.1f%%')
ax1.set_title('客户分层分布')

# 2. 流失率对比
ax2 = fig.add_subplot(gs[0, 1])
churn_by_city = customer_data.groupby('城市等级')['是否流失'].mean()
churn_by_city.plot(kind='bar', ax=ax2, color=['skyblue', 'lightcoral', 'lightgreen'])
ax2.set_title('不同城市等级流失率')
ax2.set_ylabel('流失率')
ax2.tick_params(axis='x', rotation=0)

# 3. 年龄分布直方图
ax3 = fig.add_subplot(gs[0, 2])
customer_data['年龄'].hist(bins=20, ax=ax3, alpha=0.7, color='orange')
ax3.set_title('客户年龄分布')
ax3.set_xlabel('年龄')
ax3.set_ylabel('客户数量')

# 4. 消费金额箱线图
ax4 = fig.add_subplot(gs[0, 3])
customer_data.boxplot(column='总消费金额', by='性别', ax=ax4)
ax4.set_title('性别消费金额分布')
ax4.set_xlabel('性别')
ax4.set_ylabel('总消费金额')

# 5. 股价走势图
ax5 = fig.add_subplot(gs[1, :])
stock_df[['AAPL', 'GOOGL', 'TSLA', 'MSFT']].plot(ax=ax5)
ax5.set_title('股票价格走势')
ax5.set_ylabel('价格')
ax5.legend()

# 6. 相关性热力图
ax6 = fig.add_subplot(gs[2, :2])
corr_matrix = customer_data[['年龄', '月收入', '总消费金额', '订单数量', '平均订单金额']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=ax6)
ax6.set_title('客户特征相关性矩阵')

# 7. RFM散点图
ax7 = fig.add_subplot(gs[2, 2:])
scatter = ax7.scatter(rfm_data['平均消费频率'], rfm_data['总消费金额'], 
                     c=rfm_data['最后活跃天数'], cmap='viridis', alpha=0.6)
ax7.set_xlabel('平均消费频率')
ax7.set_ylabel('总消费金额')
ax7.set_title('RFM客户分布（颜色=最后活跃天数）')
plt.colorbar(scatter, ax=ax7)

# 8. 产品关联网络图（简化）
ax8 = fig.add_subplot(gs[3, :2])
top_associations = association_df.head(10)
top_associations.plot(x='规则', y='置信度', kind='bar', ax=ax8)
ax8.set_title('产品关联规则TOP10')
ax8.set_xlabel('关联规则')
ax8.set_ylabel('置信度')
ax8.tick_params(axis='x', rotation=45)

# 9. 时间序列分解
ax9 = fig.add_subplot(gs[3, 2:])
aapl_decomp_clean = aapl_decomp.dropna()
aapl_decomp_clean[['原始', '趋势']].tail(365).plot(ax=ax9)
ax9.set_title('AAPL股价分解（最近一年）')
ax9.set_ylabel('价格')

plt.tight_layout()
plt.show()

print("\n" + "=" * 50)
print("所有高级练习题解答完成！")
print("\n高级知识点总结：")
print("1. 高级分组操作：多级分组、自定义聚合函数、滚动分组")
print("2. 数据透视和重塑：pivot_table、melt、stack/unstack")
print("3. 高级时间序列分析：分解、技术指标、相关性分析")
print("4. 性能优化：内存优化、向量化操作、查询优化")
print("5. 真实世界应用：客户流失分析、RFM分析、关联分析")
print("6. 数据质量和验证：质量检查框架、验证规则")
print("7. 高级可视化：综合仪表板、多图表组合")
print("\n进阶建议：")
print("- 深入学习机器学习与Pandas的结合")
print("- 掌握大数据处理工具（Dask、Spark）")
print("- 学习实时数据处理和流式计算")
print("- 提升数据可视化和报告制作能力")
print("- 关注数据安全和隐私保护")