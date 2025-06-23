# 股票数据分析工具

## 项目简介

这是一个基于NumPy的股票数据分析工具，实现了常见的技术指标计算和可视化功能。该项目展示了NumPy在金融数据分析中的实际应用，包括数据处理、统计分析、技术指标计算等核心功能。

## 功能特性

### 数据处理
- 股票OHLC数据生成和管理
- 收益率计算
- 数据清洗和预处理

### 技术指标
- **移动平均线 (MA)**: 支持任意周期的简单移动平均
- **布林带 (Bollinger Bands)**: 价格通道指标
- **相对强弱指数 (RSI)**: 超买超卖指标
- **MACD**: 趋势跟踪指标
- **波动率**: 价格波动程度测量
- **回撤分析**: 最大回撤计算
- **夏普比率**: 风险调整收益指标

### 可视化
- 价格走势图
- 技术指标图表
- 多指标综合展示

## 文件结构

```
project/
├── stock_analyzer.py    # 主程序文件
├── README.md           # 项目说明文档
└── requirements.txt    # 依赖包列表
```

## 安装依赖

```bash
# 使用uv安装依赖
uv add numpy matplotlib

# 或使用pip安装
pip install numpy matplotlib
```

## 使用方法

### 基本使用

```python
from stock_analyzer import StockAnalyzer

# 创建分析器
analyzer = StockAnalyzer()

# 加载样本数据
analyzer.load_sample_data(days=252, volatility=0.015, trend=0.0002)

# 计算技术指标
analyzer.calculate_returns()
analyzer.calculate_moving_average(20)
analyzer.calculate_rsi()
analyzer.calculate_macd()

# 生成分析报告
analyzer.generate_summary_report()

# 绘制图表
analyzer.plot_price_chart()
analyzer.plot_indicators()
```

### 高级功能

```python
# 自定义参数计算指标
ma_50 = analyzer.calculate_moving_average(50)
rsi_21 = analyzer.calculate_rsi(21)
bb_upper, bb_middle, bb_lower = analyzer.calculate_bollinger_bands(20, 2.5)

# 风险分析
drawdown, max_dd = analyzer.calculate_drawdown()
sharpe = analyzer.calculate_sharpe_ratio(risk_free_rate=0.03)
volatility = analyzer.calculate_volatility(30)

# 部分时间段分析
analyzer.plot_price_chart(start_idx=100, end_idx=200)
```

## 核心类和方法

### StockAnalyzer类

主要的股票分析类，包含以下核心方法：

#### 数据管理
- `load_sample_data()`: 生成样本股票数据
- `calculate_returns()`: 计算每日收益率

#### 技术指标计算
- `calculate_moving_average(window)`: 计算移动平均线
- `calculate_bollinger_bands(window, num_std)`: 计算布林带
- `calculate_rsi(window)`: 计算RSI指标
- `calculate_macd(fast, slow, signal)`: 计算MACD指标
- `calculate_volatility(window)`: 计算波动率
- `calculate_drawdown()`: 计算回撤
- `calculate_sharpe_ratio(risk_free_rate)`: 计算夏普比率

#### 可视化
- `plot_price_chart()`: 绘制价格图表
- `plot_indicators()`: 绘制技术指标图表
- `generate_summary_report()`: 生成摘要报告

## 技术指标说明

### 移动平均线 (Moving Average)
- **用途**: 平滑价格波动，识别趋势方向
- **计算**: 指定周期内收盘价的算术平均值
- **应用**: 常用周期为20日、50日、200日

### 布林带 (Bollinger Bands)
- **用途**: 判断价格相对高低，识别超买超卖
- **计算**: 中轨为移动平均线，上下轨为中轨±标准差×倍数
- **应用**: 价格触及上轨可能超买，触及下轨可能超卖

### RSI (Relative Strength Index)
- **用途**: 测量价格变动的速度和幅度
- **计算**: 基于一定周期内上涨和下跌的平均幅度
- **应用**: >70超买，<30超卖

### MACD
- **用途**: 趋势跟踪和动量分析
- **计算**: 快线EMA - 慢线EMA，信号线为MACD的EMA
- **应用**: MACD上穿信号线为买入信号，下穿为卖出信号

### 夏普比率 (Sharpe Ratio)
- **用途**: 衡量风险调整后的收益
- **计算**: (年化收益率 - 无风险利率) / 年化波动率
- **应用**: 比率越高，风险调整后收益越好

## 示例输出

运行程序后，你将看到类似以下的分析报告：

```
==================================================
股票分析摘要报告
==================================================
分析期间: 2023-01-03 至 2024-01-02
交易天数: 252天

价格信息:
起始价格: 100.00
结束价格: 105.23
价格变化: 5.23 (5.23%)
最高价格: 108.45
最低价格: 95.67

收益和风险指标:
年化收益率: 5.45%
年化波动率: 15.23%
最大回撤: 8.34%
夏普比率: 0.23

技术指标当前值:
RSI(14): 52.34
MACD: 0.0123
MACD信号线: 0.0098
MACD柱状图: 0.0025
==================================================
```

## 扩展建议

1. **数据源集成**: 集成真实的股票数据API
2. **更多指标**: 添加KDJ、威廉指标、CCI等
3. **策略回测**: 实现交易策略的历史回测功能
4. **风险管理**: 添加VaR、CVaR等风险度量指标
5. **机器学习**: 集成预测模型和特征工程

## 学习要点

通过这个项目，你将学会：

1. **NumPy数组操作**: 多维数组的创建、索引、切片
2. **数学计算**: 统计函数、滚动计算、线性代数
3. **数据处理**: 缺失值处理、异常值检测、数据标准化
4. **算法实现**: 技术指标的数学原理和编程实现
5. **可视化**: 使用matplotlib创建专业的金融图表
6. **面向对象编程**: 类的设计和方法的组织

## 注意事项

1. 本项目仅用于教学目的，不构成投资建议
2. 样本数据为模拟生成，不代表真实市场情况
3. 技术指标存在滞后性，应结合多种分析方法
4. 实际应用中需要考虑交易成本、滑点等因素

## 作者信息

- 作者: Python教程团队
- 创建日期: 2024-12-19
- 版本: 1.0.0
- 许可证: MIT License