#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pandas高级练习题

本文件包含Pandas高级操作的练习题，涵盖：
- 高级数据处理技术
- 复杂的时间序列分析
- 数据透视和重塑
- 性能优化
- 实际业务场景应用

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


def exercise_1_advanced_groupby():
    """
    练习1: 高级分组操作
    
    任务：
    1. 多级分组和聚合
    2. 自定义聚合函数
    3. 分组后的数据转换
    4. 分组过滤
    """
    print("=== 练习1: 高级分组操作 ===")
    
    # 创建复杂的销售数据
    np.random.seed(42)
    
    sales_data = pd.DataFrame({
        '销售员': np.random.choice(['张三', '李四', '王五', '赵六', '钱七'], 1000),
        '区域': np.random.choice(['华北', '华东', '华南', '华中', '西南'], 1000),
        '产品线': np.random.choice(['A线', 'B线', 'C线'], 1000),
        '产品': np.random.choice(['产品1', '产品2', '产品3', '产品4', '产品5'], 1000),
        '销售额': np.random.exponential(1000, 1000),
        '成本': np.random.exponential(600, 1000),
        '销售日期': pd.date_range('2024-01-01', periods=1000, freq='D')[:1000],
        '客户等级': np.random.choice(['A', 'B', 'C'], 1000, p=[0.2, 0.3, 0.5])
    })
    
    sales_data['利润'] = sales_data['销售额'] - sales_data['成本']
    sales_data['利润率'] = sales_data['利润'] / sales_data['销售额']
    sales_data['月份'] = sales_data['销售日期'].dt.month
    sales_data['季度'] = sales_data['销售日期'].dt.quarter
    
    print("销售数据预览：")
    print(sales_data.head())
    
    # TODO: 1. 多级分组聚合
    # 按区域、产品线、销售员进行三级分组
    # 计算每个组合的总销售额、平均利润率、销售次数
    
    # TODO: 2. 自定义聚合函数
    # 定义以下自定义函数：
    # - 变异系数函数：std/mean
    # - 销售额分位数函数：返回25%、50%、75%分位数
    # - 利润率等级函数：根据平均利润率返回'高'、'中'、'低'
    
    # TODO: 3. 复杂聚合
    # 使用agg()方法，对不同列应用不同的聚合函数
    # 销售额：sum, mean, std
    # 利润：sum, mean
    # 利润率：mean, min, max
    # 销售日期：min, max, count
    
    # TODO: 4. 分组转换
    # 计算每个销售员在其所在区域的销售额排名
    # 计算每个产品在其产品线中的市场份额
    # 计算每个销售员的累计销售额
    
    # TODO: 5. 分组过滤
    # 筛选出平均销售额大于1000的销售员
    # 筛选出总销售额排名前3的区域
    # 筛选出销售次数大于20的产品
    
    # TODO: 6. 滚动分组操作
    # 按销售员分组，计算每个销售员的30天滚动平均销售额
    # 按产品分组，计算每个产品的累计市场份额变化
    
    # TODO: 7. 分组应用自定义函数
    # 定义一个函数，计算每个组的销售趋势（线性回归斜率）
    # 应用到按销售员分组的数据上
    
    print("\n练习1完成提示：")
    print("- 掌握了多级分组和复杂聚合")
    print("- 学会了自定义聚合函数")
    print("- 进行了分组转换和过滤")
    print("- 应用了滚动分组操作")
    
    return sales_data


def exercise_2_pivot_and_reshape():
    """
    练习2: 数据透视和重塑
    
    任务：
    1. 复杂透视表操作
    2. 数据重塑（melt和pivot）
    3. 多级索引操作
    4. 交叉表分析
    """
    print("\n=== 练习2: 数据透视和重塑 ===")
    
    # 创建宽格式的销售数据
    np.random.seed(42)
    
    # 创建月度销售数据（宽格式）
    regions = ['华北', '华东', '华南', '华中', '西南']
    products = ['产品A', '产品B', '产品C', '产品D']
    months = ['1月', '2月', '3月', '4月', '5月', '6月']
    
    wide_data = pd.DataFrame({
        '区域': np.repeat(regions, len(products)),
        '产品': products * len(regions)
    })
    
    # 添加每个月的销售数据
    for month in months:
        wide_data[month] = np.random.exponential(1000, len(wide_data))
    
    print("宽格式销售数据：")
    print(wide_data.head())
    
    # TODO: 1. 宽格式转长格式
    # 使用melt()将月份列转换为行
    # 结果应该包含：区域、产品、月份、销售额四列
    
    # TODO: 2. 长格式转宽格式
    # 使用pivot()将上面的长格式数据重新转换为宽格式
    # 验证是否与原始数据一致
    
    # TODO: 3. 复杂透视表
    # 创建一个透视表：
    # - 行索引：区域
    # - 列索引：产品
    # - 值：各月份销售额的平均值
    # - 添加行和列的总计
    
    # TODO: 4. 多值透视表
    # 创建一个透视表同时显示销售额的总和和平均值
    
    # TODO: 5. 多级索引操作
    # 创建一个多级索引的DataFrame
    # 练习多级索引的选择、切片、重排序操作
    
    # TODO: 6. 交叉表分析
    # 创建区域和产品的交叉表
    # 分析不同区域对不同产品的偏好
    
    # TODO: 7. 数据重塑应用
    # 将销售数据重塑为适合时间序列分析的格式
    # 每行代表一个时间点，列为不同区域-产品组合的销售额
    
    # TODO: 8. 透视表可视化
    # 将透视表结果进行可视化
    # 创建热力图显示区域-产品销售矩阵
    
    print("\n练习2完成提示：")
    print("- 掌握了数据的宽长格式转换")
    print("- 学会了复杂透视表操作")
    print("- 练习了多级索引操作")
    print("- 进行了交叉表分析")
    
    return wide_data


def exercise_3_time_series_advanced():
    """
    练习3: 高级时间序列分析
    
    任务：
    1. 复杂时间序列操作
    2. 季节性分解
    3. 时间序列预测准备
    4. 异常检测
    """
    print("\n=== 练习3: 高级时间序列分析 ===")
    
    # 创建复杂的时间序列数据
    np.random.seed(42)
    
    # 创建多个时间序列
    date_range = pd.date_range('2020-01-01', '2024-12-31', freq='D')
    n_days = len(date_range)
    
    # 模拟多个指标的时间序列
    ts_data = pd.DataFrame({
        '网站访问量': 1000 + 200 * np.sin(2 * np.pi * np.arange(n_days) / 365.25) + 
                     100 * np.sin(2 * np.pi * np.arange(n_days) / 7) + 
                     np.random.normal(0, 50, n_days),
        '销售额': 5000 + 1000 * np.sin(2 * np.pi * np.arange(n_days) / 365.25) + 
                 500 * np.sin(2 * np.pi * np.arange(n_days) / 7) + 
                 np.random.normal(0, 200, n_days),
        '广告支出': 2000 + 400 * np.sin(2 * np.pi * np.arange(n_days) / 365.25) + 
                   np.random.normal(0, 100, n_days),
        '客户满意度': 4.0 + 0.5 * np.sin(2 * np.pi * np.arange(n_days) / 365.25) + 
                     np.random.normal(0, 0.2, n_days)
    }, index=date_range)
    
    # 添加一些异常值
    anomaly_dates = np.random.choice(date_range, 20, replace=False)
    for date in anomaly_dates:
        ts_data.loc[date, '网站访问量'] *= np.random.uniform(2, 5)
        ts_data.loc[date, '销售额'] *= np.random.uniform(0.3, 0.7)
    
    print("时间序列数据预览：")
    print(ts_data.head())
    
    # TODO: 1. 时间序列分解
    # 对每个指标进行趋势、季节性、残差分解
    # 使用移动平均方法进行简单分解
    
    # TODO: 2. 多频率重采样
    # 将日数据重采样为：
    # - 周数据（周一开始）
    # - 月数据（月末）
    # - 季度数据
    # 对不同指标使用不同的聚合方法
    
    # TODO: 3. 滞后和领先指标
    # 创建滞后特征（lag features）：
    # - 1天前、7天前、30天前的值
    # 创建领先特征（lead features）：
    # - 1天后、7天后的值（用于预测验证）
    
    # TODO: 4. 滚动统计
    # 计算多种滚动统计指标：
    # - 7天、30天、90天滚动均值
    # - 滚动标准差
    # - 滚动最大值和最小值
    # - 滚动分位数（25%, 75%）
    
    # TODO: 5. 异常检测
    # 实现多种异常检测方法：
    # - 基于Z-score的异常检测
    # - 基于IQR的异常检测
    # - 基于滚动统计的异常检测
    
    # TODO: 6. 相关性分析
    # 分析不同指标之间的：
    # - 同期相关性
    # - 滞后相关性（一个指标对另一个指标的滞后影响）
    # - 滚动相关性（相关性随时间的变化）
    
    # TODO: 7. 季节性模式分析
    # 分析各种季节性模式：
    # - 年度季节性（按月分析）
    # - 周度季节性（按星期分析）
    # - 节假日效应分析
    
    # TODO: 8. 时间序列特征工程
    # 创建用于机器学习的特征：
    # - 时间特征（年、月、日、星期几等）
    # - 滞后特征
    # - 滚动统计特征
    # - 差分特征
    # - 季节性特征
    
    # TODO: 9. 数据可视化
    # 创建综合的时间序列可视化：
    # - 原始数据趋势图
    # - 分解后的组件图
    # - 异常值标注图
    # - 相关性热力图
    # - 季节性模式图
    
    print("\n练习3完成提示：")
    print("- 进行了复杂的时间序列分解")
    print("- 掌握了多频率重采样")
    print("- 实现了异常检测算法")
    print("- 进行了深入的季节性分析")
    print("- 完成了时间序列特征工程")
    
    return ts_data


def exercise_4_performance_optimization():
    """
    练习4: 性能优化
    
    任务：
    1. 内存优化
    2. 计算性能优化
    3. 大数据处理技巧
    4. 并行处理
    """
    print("\n=== 练习4: 性能优化 ===")
    
    # 创建大型数据集
    np.random.seed(42)
    
    # 创建一个相对较大的数据集
    n_rows = 100000
    large_data = pd.DataFrame({
        'id': range(n_rows),
        'category': np.random.choice(['A', 'B', 'C', 'D', 'E'], n_rows),
        'value1': np.random.randn(n_rows),
        'value2': np.random.exponential(1, n_rows),
        'date': pd.date_range('2020-01-01', periods=n_rows, freq='H'),
        'text': ['text_' + str(i) for i in range(n_rows)]
    })
    
    print(f"大型数据集形状: {large_data.shape}")
    print(f"内存使用: {large_data.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # TODO: 1. 内存优化
    # 优化数据类型以减少内存使用：
    # - 将category列转换为category类型
    # - 将id列转换为合适的整数类型
    # - 优化浮点数精度
    # 比较优化前后的内存使用
    
    # TODO: 2. 高效的数据操作
    # 比较不同操作的性能：
    # - 使用.loc vs .iloc vs .query()
    # - 使用.apply() vs 向量化操作
    # - 使用.groupby().agg() vs 手动循环
    
    # TODO: 3. 索引优化
    # 设置合适的索引以提高查询性能：
    # - 设置date为索引
    # - 创建多级索引
    # - 比较有索引和无索引的查询性能
    
    # TODO: 4. 分块处理
    # 实现分块处理大数据：
    # - 将数据分成多个块
    # - 对每个块进行处理
    # - 合并结果
    
    # TODO: 5. 向量化操作
    # 将循环操作转换为向量化操作：
    # - 条件赋值
    # - 数学运算
    # - 字符串操作
    
    # TODO: 6. 缓存和预计算
    # 实现结果缓存机制：
    # - 缓存昂贵的计算结果
    # - 预计算常用的聚合结果
    
    # TODO: 7. 并行处理模拟
    # 模拟并行处理（使用multiprocessing概念）：
    # - 将数据分割为多个部分
    # - 模拟并行处理每个部分
    # - 合并结果
    
    # TODO: 8. 性能监控
    # 实现性能监控工具：
    # - 测量操作执行时间
    # - 监控内存使用
    # - 创建性能报告
    
    print("\n练习4完成提示：")
    print("- 学会了内存优化技巧")
    print("- 掌握了高效的数据操作方法")
    print("- 实现了分块处理策略")
    print("- 应用了向量化操作")
    print("- 了解了并行处理概念")
    
    return large_data


def exercise_5_real_world_scenarios():
    """
    练习5: 真实世界场景
    
    任务：
    1. 金融数据分析
    2. 用户行为分析
    3. 供应链分析
    4. 市场研究分析
    """
    print("\n=== 练习5: 真实世界场景 ===")
    
    # 场景1: 股票数据分析
    print("\n场景1: 股票数据分析")
    
    # 创建模拟股票数据
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', '2024-12-31', freq='D')
    
    stocks = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    stock_data = {}
    
    for stock in stocks:
        # 模拟股价随机游走
        returns = np.random.normal(0.001, 0.02, len(dates))
        prices = 100 * np.exp(np.cumsum(returns))
        volumes = np.random.lognormal(15, 1, len(dates))
        
        stock_data[stock] = pd.DataFrame({
            '开盘价': prices * np.random.uniform(0.98, 1.02, len(dates)),
            '最高价': prices * np.random.uniform(1.00, 1.05, len(dates)),
            '最低价': prices * np.random.uniform(0.95, 1.00, len(dates)),
            '收盘价': prices,
            '成交量': volumes.astype(int)
        }, index=dates)
    
    # TODO: 股票分析任务
    """
    1. 计算技术指标：
       - 简单移动平均线（SMA）
       - 指数移动平均线（EMA）
       - 相对强弱指数（RSI）
       - 布林带
    
    2. 风险分析：
       - 计算日收益率
       - 计算波动率
       - 计算最大回撤
       - 计算夏普比率
    
    3. 相关性分析：
       - 股票间的相关性
       - 滚动相关性
    
    4. 投资组合分析：
       - 等权重投资组合
       - 风险平价投资组合
    """
    
    # 场景2: 用户行为分析
    print("\n场景2: 用户行为分析")
    
    # 创建用户行为数据
    np.random.seed(42)
    n_users = 10000
    n_events = 50000
    
    user_events = pd.DataFrame({
        '用户ID': np.random.choice(range(1, n_users + 1), n_events),
        '事件类型': np.random.choice(['登录', '浏览', '点击', '购买', '分享'], n_events,
                                p=[0.3, 0.4, 0.2, 0.08, 0.02]),
        '时间戳': pd.date_range('2024-01-01', periods=n_events, freq='min'),
        '页面': np.random.choice(['首页', '产品页', '购物车', '结算页', '个人中心'], n_events),
        '设备类型': np.random.choice(['PC', '手机', '平板'], n_events, p=[0.4, 0.5, 0.1]),
        '会话ID': np.random.choice(range(1, 20000), n_events)
    })
    
    # TODO: 用户行为分析任务
    """
    1. 用户活跃度分析：
       - 日活跃用户数（DAU）
       - 月活跃用户数（MAU）
       - 用户留存率
    
    2. 用户路径分析：
       - 用户访问路径
       - 转化漏斗分析
       - 页面跳出率
    
    3. 用户分群：
       - RFM分析
       - 用户生命周期分析
       - 行为模式聚类
    
    4. 设备和渠道分析：
       - 不同设备的用户行为差异
       - 时间段分析
    """
    
    # 场景3: 供应链分析
    print("\n场景3: 供应链分析")
    
    # 创建供应链数据
    np.random.seed(42)
    
    suppliers = ['供应商A', '供应商B', '供应商C', '供应商D', '供应商E']
    products = ['产品1', '产品2', '产品3', '产品4', '产品5', '产品6']
    warehouses = ['仓库1', '仓库2', '仓库3', '仓库4']
    
    supply_data = pd.DataFrame({
        '供应商': np.random.choice(suppliers, 1000),
        '产品': np.random.choice(products, 1000),
        '仓库': np.random.choice(warehouses, 1000),
        '订单日期': pd.date_range('2024-01-01', periods=1000, freq='D')[:1000],
        '交付日期': pd.date_range('2024-01-01', periods=1000, freq='D')[:1000] + 
                    pd.to_timedelta(np.random.randint(1, 15, 1000), unit='D'),
        '订单数量': np.random.poisson(100, 1000),
        '单价': np.random.uniform(10, 100, 1000),
        '质量评分': np.random.uniform(3.0, 5.0, 1000)
    })
    
    supply_data['总金额'] = supply_data['订单数量'] * supply_data['单价']
    supply_data['交付天数'] = (supply_data['交付日期'] - supply_data['订单日期']).dt.days
    
    # TODO: 供应链分析任务
    """
    1. 供应商绩效分析：
       - 交付及时率
       - 质量评分分析
       - 成本分析
    
    2. 库存分析：
       - 库存周转率
       - 安全库存计算
       - 缺货分析
    
    3. 需求预测：
       - 历史需求趋势
       - 季节性分析
       - 预测模型准备
    
    4. 风险分析：
       - 供应商集中度风险
       - 交付延迟风险
       - 质量风险
    """
    
    print("\n练习5完成提示：")
    print("- 应用了金融数据分析技术")
    print("- 进行了用户行为深度分析")
    print("- 完成了供应链绩效分析")
    print("- 解决了真实业务问题")
    
    return stock_data, user_events, supply_data


def exercise_6_data_quality_and_validation():
    """
    练习6: 数据质量和验证
    
    任务：
    1. 数据质量评估
    2. 数据验证规则
    3. 数据清洗策略
    4. 数据质量监控
    """
    print("\n=== 练习6: 数据质量和验证 ===")
    
    # 创建包含各种数据质量问题的数据集
    np.random.seed(42)
    
    # 故意创建有问题的数据
    problematic_data = pd.DataFrame({
        'ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 12],  # 重复ID
        '姓名': ['张三', '李四', '', '赵六', None, '钱七', '孙八', '周九', '吴十', '郑一', '李四', '王二'],
        '年龄': [25, 30, -5, 150, 28, 35, None, 40, 22, 29, 30, 33],  # 负数、异常值、缺失值
        '邮箱': ['zhang@email.com', 'li@email', 'wang@email.com', 'zhao@email.com', 
                'qian@email.com', 'sun@email.com', 'zhou@email.com', 'wu@email.com',
                'zheng@email.com', 'wang2@email.com', 'li@email', 'wang3@email.com'],  # 格式不一致
        '工资': [5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 6000, 15000],
        '入职日期': ['2020-01-01', '2019-05-15', '2021-13-10', '2018-12-01', '2020-07-20',
                   '2022-02-14', '2021-11-30', '2019-08-10', '2020-03-15', '2021-06-01',
                   '2019-05-15', '2022-01-10'],  # 无效日期
        '部门': ['IT', 'HR', 'IT', 'Finance', 'IT', 'HR', 'Finance', 'IT', 'HR', 'Finance', 'HR', 'IT']
    })
    
    print("问题数据集：")
    print(problematic_data)
    
    # TODO: 1. 数据质量评估
    # 创建数据质量报告，包括：
    # - 缺失值统计
    # - 重复值统计
    # - 数据类型检查
    # - 异常值检测
    # - 格式一致性检查
    
    # TODO: 2. 数据验证规则
    # 定义并实现数据验证规则：
    # - ID唯一性检查
    # - 年龄范围检查（0-120）
    # - 邮箱格式检查
    # - 日期格式检查
    # - 必填字段检查
    
    # TODO: 3. 数据清洗策略
    # 实现数据清洗流程：
    # - 处理重复记录
    # - 修正异常值
    # - 标准化格式
    # - 填充缺失值
    # - 数据类型转换
    
    # TODO: 4. 数据质量评分
    # 为每条记录计算质量评分：
    # - 完整性评分
    # - 准确性评分
    # - 一致性评分
    # - 综合质量评分
    
    # TODO: 5. 数据质量监控
    # 创建数据质量监控仪表板：
    # - 质量趋势图
    # - 问题分布图
    # - 清洗效果对比
    
    # TODO: 6. 自动化清洗流程
    # 设计自动化数据清洗管道：
    # - 检测阶段
    # - 清洗阶段
    # - 验证阶段
    # - 报告阶段
    
    print("\n练习6完成提示：")
    print("- 建立了数据质量评估体系")
    print("- 实现了数据验证规则")
    print("- 设计了数据清洗策略")
    print("- 创建了质量监控机制")
    
    return problematic_data


def exercise_7_advanced_visualization():
    """
    练习7: 高级数据可视化
    
    任务：
    1. 复杂图表创建
    2. 交互式可视化
    3. 多维数据可视化
    4. 可视化最佳实践
    """
    print("\n=== 练习7: 高级数据可视化 ===")
    
    # 创建多维数据集
    np.random.seed(42)
    
    viz_data = pd.DataFrame({
        '产品': np.random.choice(['产品A', '产品B', '产品C', '产品D'], 1000),
        '区域': np.random.choice(['华北', '华东', '华南', '华中'], 1000),
        '渠道': np.random.choice(['线上', '线下', '代理'], 1000),
        '销售额': np.random.exponential(1000, 1000),
        '利润率': np.random.uniform(0.1, 0.4, 1000),
        '客户满意度': np.random.uniform(3.0, 5.0, 1000),
        '市场份额': np.random.uniform(0.05, 0.3, 1000),
        '销售日期': pd.date_range('2024-01-01', periods=1000, freq='D')[:1000]
    })
    
    viz_data['月份'] = viz_data['销售日期'].dt.month
    viz_data['季度'] = viz_data['销售日期'].dt.quarter
    
    print("可视化数据预览：")
    print(viz_data.head())
    
    # TODO: 1. 多维散点图
    # 创建散点图显示：
    # - X轴：销售额
    # - Y轴：利润率
    # - 颜色：产品类别
    # - 大小：市场份额
    # - 形状：渠道类型
    
    # TODO: 2. 复合图表
    # 创建包含多个子图的复合图表：
    # - 销售额趋势线图
    # - 利润率分布直方图
    # - 产品-区域热力图
    # - 客户满意度箱线图
    
    # TODO: 3. 动态图表
    # 创建按时间变化的动态图表：
    # - 月度销售额变化
    # - 产品市场份额变化
    # - 区域表现变化
    
    # TODO: 4. 3D可视化
    # 创建3D图表：
    # - 3D散点图（销售额、利润率、客户满意度）
    # - 3D表面图
    
    # TODO: 5. 网络图
    # 创建关系网络图：
    # - 产品-区域关系网络
    # - 渠道-客户关系网络
    
    # TODO: 6. 仪表板设计
    # 设计综合仪表板：
    # - KPI指标卡片
    # - 趋势图表
    # - 对比分析
    # - 钻取功能
    
    # TODO: 7. 可视化最佳实践
    # 应用可视化最佳实践：
    # - 颜色选择
    # - 图表类型选择
    # - 标题和标签
    # - 图例和注释
    
    print("\n练习7完成提示：")
    print("- 创建了复杂的多维可视化")
    print("- 设计了交互式图表")
    print("- 构建了综合仪表板")
    print("- 应用了可视化最佳实践")
    
    return viz_data


def main():
    """
    主函数 - 运行所有高级练习
    """
    print("Pandas高级练习题")
    print("=" * 60)
    
    # 运行练习（学生可以选择性运行）
    
    # 练习1: 高级分组操作
    # sales_data = exercise_1_advanced_groupby()
    
    # 练习2: 数据透视和重塑
    # wide_data = exercise_2_pivot_and_reshape()
    
    # 练习3: 高级时间序列分析
    # ts_data = exercise_3_time_series_advanced()
    
    # 练习4: 性能优化
    # large_data = exercise_4_performance_optimization()
    
    # 练习5: 真实世界场景
    # stock_data, user_events, supply_data = exercise_5_real_world_scenarios()
    
    # 练习6: 数据质量和验证
    # problematic_data = exercise_6_data_quality_and_validation()
    
    # 练习7: 高级数据可视化
    # viz_data = exercise_7_advanced_visualization()
    
    print("\n" + "=" * 60)
    print("高级练习说明：")
    print("1. 这些练习涵盖了Pandas的高级应用")
    print("2. 每个练习都模拟了真实的业务场景")
    print("3. 建议在完成基础练习后再进行高级练习")
    print("4. 可以结合实际项目需求选择相关练习")
    print("5. 注重代码的可读性和性能优化")
    print("6. 完成后可以查看solutions目录中的参考实现")
    print("=" * 60)


if __name__ == "__main__":
    main()