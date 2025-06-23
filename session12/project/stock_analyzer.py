#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session12 项目：股票数据分析工具

本项目实现了一个简单的股票数据分析工具，使用NumPy进行数据处理和分析。
该工具可以计算常见的股票技术指标，如移动平均线、相对强弱指数(RSI)、
布林带、MACD等，并提供基本的风险分析功能。

作者: Python教程团队
创建日期: 2024-12-19
"""

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


class StockAnalyzer:
    """股票数据分析工具类"""
    
    def __init__(self, data=None, dates=None):
        """
        初始化股票分析器
        
        参数:
            data: 股票价格数据，形状为(n, 4)的NumPy数组，包含开盘价、最高价、最低价、收盘价
            dates: 对应的日期列表
        """
        self.data = data
        self.dates = dates
        self.indicators = {}
    
    def load_sample_data(self, days=252, volatility=0.01, trend=0.0001):
        """
        生成样本股票数据
        
        参数:
            days: 交易日数量
            volatility: 波动率
            trend: 趋势因子
        """
        np.random.seed(42)  # 设置随机种子，确保结果可重现
        
        # 生成收盘价
        close = np.zeros(days)
        close[0] = 100  # 起始价格
        
        # 模拟价格变动
        for i in range(1, days):
            # 添加随机波动和趋势
            change = np.random.normal(trend, volatility) + trend
            close[i] = close[i-1] * (1 + change)
        
        # 生成开盘价、最高价、最低价
        daily_volatility = volatility / 2
        open_prices = close * (1 + np.random.normal(0, daily_volatility, days))
        high_prices = np.maximum(close, open_prices) * (1 + np.abs(np.random.normal(0, daily_volatility, days)))
        low_prices = np.minimum(close, open_prices) * (1 - np.abs(np.random.normal(0, daily_volatility, days)))
        
        # 组合OHLC数据
        self.data = np.column_stack((open_prices, high_prices, low_prices, close))
        
        # 生成日期（从今天向前推days天）
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days*1.5)  # 考虑周末和节假日
        
        # 简单模拟交易日（排除周末）
        all_dates = []
        current_date = start_date
        while len(all_dates) < days:
            if current_date.weekday() < 5:  # 0-4表示周一至周五
                all_dates.append(current_date)
            current_date += timedelta(days=1)
        
        self.dates = all_dates
        
        print(f"已生成{days}天的样本股票数据")
        print(f"起始日期: {all_dates[0].strftime('%Y-%m-%d')}")
        print(f"结束日期: {all_dates[-1].strftime('%Y-%m-%d')}")
        print(f"起始价格: {self.data[0, 3]:.2f}")
        print(f"结束价格: {self.data[-1, 3]:.2f}")
        
        return self.data, self.dates
    
    def calculate_returns(self):
        """
        计算每日收益率
        
        返回:
            daily_returns: 每日收益率数组
        """
        if self.data is None:
            raise ValueError("请先加载数据")
        
        # 使用收盘价计算收益率
        close_prices = self.data[:, 3]
        daily_returns = np.zeros_like(close_prices)
        daily_returns[1:] = (close_prices[1:] - close_prices[:-1]) / close_prices[:-1]
        
        self.indicators['daily_returns'] = daily_returns
        return daily_returns
    
    def calculate_moving_average(self, window=20):
        """
        计算移动平均线
        
        参数:
            window: 窗口大小
            
        返回:
            ma: 移动平均线数组
        """
        if self.data is None:
            raise ValueError("请先加载数据")
        
        close_prices = self.data[:, 3]
        ma = np.zeros_like(close_prices)
        
        # 计算移动平均
        for i in range(len(close_prices)):
            if i < window:
                ma[i] = np.mean(close_prices[:i+1])
            else:
                ma[i] = np.mean(close_prices[i-window+1:i+1])
        
        self.indicators[f'ma_{window}'] = ma
        return ma
    
    def calculate_bollinger_bands(self, window=20, num_std=2):
        """
        计算布林带
        
        参数:
            window: 窗口大小
            num_std: 标准差倍数
            
        返回:
            upper_band: 上轨
            middle_band: 中轨（移动平均线）
            lower_band: 下轨
        """
        if self.data is None:
            raise ValueError("请先加载数据")
        
        close_prices = self.data[:, 3]
        middle_band = self.calculate_moving_average(window)
        
        # 计算标准差
        std = np.zeros_like(close_prices)
        for i in range(len(close_prices)):
            if i < window:
                std[i] = np.std(close_prices[:i+1])
            else:
                std[i] = np.std(close_prices[i-window+1:i+1])
        
        # 计算上下轨
        upper_band = middle_band + num_std * std
        lower_band = middle_band - num_std * std
        
        self.indicators['bollinger_upper'] = upper_band
        self.indicators['bollinger_middle'] = middle_band
        self.indicators['bollinger_lower'] = lower_band
        
        return upper_band, middle_band, lower_band
    
    def calculate_rsi(self, window=14):
        """
        计算相对强弱指数(RSI)
        
        参数:
            window: 窗口大小
            
        返回:
            rsi: RSI数组
        """
        if self.data is None:
            raise ValueError("请先加载数据")
        
        # 确保已计算收益率
        if 'daily_returns' not in self.indicators:
            self.calculate_returns()
        
        returns = self.indicators['daily_returns']
        
        # 初始化数组
        rsi = np.zeros_like(returns)
        gains = np.zeros_like(returns)
        losses = np.zeros_like(returns)
        
        # 分离收益和损失
        gains[returns > 0] = returns[returns > 0]
        losses[returns < 0] = -returns[returns < 0]
        
        # 计算平均收益和平均损失
        avg_gain = np.zeros_like(returns)
        avg_loss = np.zeros_like(returns)
        
        # 第一个窗口的平均值
        for i in range(window, len(returns)):
            if i == window:
                avg_gain[i] = np.mean(gains[1:window+1])
                avg_loss[i] = np.mean(losses[1:window+1])
            else:
                avg_gain[i] = (avg_gain[i-1] * (window-1) + gains[i]) / window
                avg_loss[i] = (avg_loss[i-1] * (window-1) + losses[i]) / window
            
            # 计算相对强度和RSI
            if avg_loss[i] == 0:
                rsi[i] = 100
            else:
                rs = avg_gain[i] / avg_loss[i]
                rsi[i] = 100 - (100 / (1 + rs))
        
        self.indicators['rsi'] = rsi
        return rsi
    
    def calculate_macd(self, fast=12, slow=26, signal=9):
        """
        计算MACD指标
        
        参数:
            fast: 快线周期
            slow: 慢线周期
            signal: 信号线周期
            
        返回:
            macd_line: MACD线
            signal_line: 信号线
            histogram: MACD柱状图
        """
        if self.data is None:
            raise ValueError("请先加载数据")
        
        close_prices = self.data[:, 3]
        
        # 计算EMA
        def ema(prices, period):
            ema_values = np.zeros_like(prices)
            # 初始值为简单平均
            ema_values[period-1] = np.mean(prices[:period])
            
            # 计算EMA
            k = 2 / (period + 1)
            for i in range(period, len(prices)):
                ema_values[i] = prices[i] * k + ema_values[i-1] * (1-k)
            
            return ema_values
        
        # 计算快线和慢线
        fast_ema = ema(close_prices, fast)
        slow_ema = ema(close_prices, slow)
        
        # 计算MACD线
        macd_line = fast_ema - slow_ema
        
        # 计算信号线（MACD的EMA）
        signal_line = ema(macd_line, signal)
        
        # 计算柱状图
        histogram = macd_line - signal_line
        
        self.indicators['macd_line'] = macd_line
        self.indicators['macd_signal'] = signal_line
        self.indicators['macd_histogram'] = histogram
        
        return macd_line, signal_line, histogram
    
    def calculate_volatility(self, window=20):
        """
        计算波动率
        
        参数:
            window: 窗口大小
            
        返回:
            volatility: 波动率数组
        """
        if self.data is None:
            raise ValueError("请先加载数据")
        
        # 确保已计算收益率
        if 'daily_returns' not in self.indicators:
            self.calculate_returns()
        
        returns = self.indicators['daily_returns']
        
        # 计算滚动标准差
        volatility = np.zeros_like(returns)
        for i in range(len(returns)):
            if i < window:
                volatility[i] = np.std(returns[1:i+1]) * np.sqrt(252)  # 年化
            else:
                volatility[i] = np.std(returns[i-window+1:i+1]) * np.sqrt(252)  # 年化
        
        self.indicators['volatility'] = volatility
        return volatility
    
    def calculate_drawdown(self):
        """
        计算回撤
        
        返回:
            drawdown: 回撤百分比
            max_drawdown: 最大回撤
        """
        if self.data is None:
            raise ValueError("请先加载数据")
        
        close_prices = self.data[:, 3]
        
        # 计算累计最大值
        running_max = np.maximum.accumulate(close_prices)
        
        # 计算回撤
        drawdown = (running_max - close_prices) / running_max
        max_drawdown = np.max(drawdown)
        
        self.indicators['drawdown'] = drawdown
        self.indicators['max_drawdown'] = max_drawdown
        
        return drawdown, max_drawdown
    
    def calculate_sharpe_ratio(self, risk_free_rate=0.02):
        """
        计算夏普比率
        
        参数:
            risk_free_rate: 无风险利率
            
        返回:
            sharpe_ratio: 夏普比率
        """
        if self.data is None:
            raise ValueError("请先加载数据")
        
        # 确保已计算收益率
        if 'daily_returns' not in self.indicators:
            self.calculate_returns()
        
        returns = self.indicators['daily_returns']
        
        # 计算年化收益率和标准差
        annual_return = np.mean(returns) * 252
        annual_volatility = np.std(returns) * np.sqrt(252)
        
        # 计算夏普比率
        sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility
        
        self.indicators['sharpe_ratio'] = sharpe_ratio
        return sharpe_ratio
    
    def plot_price_chart(self, start_idx=0, end_idx=None, show_ma=True, ma_windows=[20, 50, 200]):
        """
        绘制价格图表
        
        参数:
            start_idx: 起始索引
            end_idx: 结束索引
            show_ma: 是否显示移动平均线
            ma_windows: 移动平均线窗口大小列表
        """
        if self.data is None:
            raise ValueError("请先加载数据")
        
        if end_idx is None:
            end_idx = len(self.data)
        
        # 提取数据
        dates = self.dates[start_idx:end_idx]
        ohlc = self.data[start_idx:end_idx]
        
        # 创建图表
        plt.figure(figsize=(12, 6))
        
        # 绘制收盘价
        plt.plot(dates, ohlc[:, 3], label='收盘价', color='black')
        
        # 绘制移动平均线
        if show_ma:
            for window in ma_windows:
                if f'ma_{window}' not in self.indicators:
                    self.calculate_moving_average(window)
                plt.plot(dates, self.indicators[f'ma_{window}'][start_idx:end_idx], 
                         label=f'{window}日均线')
        
        # 设置图表
        plt.title('股票价格走势图')
        plt.xlabel('日期')
        plt.ylabel('价格')
        plt.grid(True)
        plt.legend()
        plt.xticks(rotation=45)
        
        # 显示图表
        plt.tight_layout()
        plt.show()
    
    def plot_indicators(self, start_idx=0, end_idx=None):
        """
        绘制技术指标图表
        
        参数:
            start_idx: 起始索引
            end_idx: 结束索引
        """
        if self.data is None:
            raise ValueError("请先加载数据")
        
        if end_idx is None:
            end_idx = len(self.data)
        
        # 提取数据
        dates = self.dates[start_idx:end_idx]
        
        # 确保计算了所有指标
        if 'rsi' not in self.indicators:
            self.calculate_rsi()
        if 'bollinger_upper' not in self.indicators:
            self.calculate_bollinger_bands()
        if 'macd_line' not in self.indicators:
            self.calculate_macd()
        
        # 创建子图
        fig, axs = plt.subplots(4, 1, figsize=(12, 12), sharex=True)
        
        # 1. 价格和布林带
        axs[0].plot(dates, self.data[start_idx:end_idx, 3], label='收盘价', color='black')
        axs[0].plot(dates, self.indicators['bollinger_upper'][start_idx:end_idx], 'r--', label='布林上轨')
        axs[0].plot(dates, self.indicators['bollinger_middle'][start_idx:end_idx], 'g--', label='布林中轨')
        axs[0].plot(dates, self.indicators['bollinger_lower'][start_idx:end_idx], 'b--', label='布林下轨')
        axs[0].set_title('价格和布林带')
        axs[0].grid(True)
        axs[0].legend()
        
        # 2. RSI
        axs[1].plot(dates, self.indicators['rsi'][start_idx:end_idx], label='RSI', color='purple')
        axs[1].axhline(y=70, color='r', linestyle='--')
        axs[1].axhline(y=30, color='g', linestyle='--')
        axs[1].set_title('相对强弱指数(RSI)')
        axs[1].set_ylim(0, 100)
        axs[1].grid(True)
        
        # 3. MACD
        axs[2].plot(dates, self.indicators['macd_line'][start_idx:end_idx], label='MACD线', color='blue')
        axs[2].plot(dates, self.indicators['macd_signal'][start_idx:end_idx], label='信号线', color='red')
        axs[2].bar(dates, self.indicators['macd_histogram'][start_idx:end_idx], label='柱状图', color='green', alpha=0.5)
        axs[2].set_title('MACD指标')
        axs[2].grid(True)
        axs[2].legend()
        
        # 4. 波动率和回撤
        if 'volatility' not in self.indicators:
            self.calculate_volatility()
        if 'drawdown' not in self.indicators:
            self.calculate_drawdown()
        
        ax4 = axs[3]
        ax4.plot(dates, self.indicators['volatility'][start_idx:end_idx], label='波动率', color='orange')
        ax4.set_title('波动率')
        ax4.set_ylabel('波动率', color='orange')
        ax4.tick_params(axis='y', labelcolor='orange')
        ax4.grid(True)
        
        ax5 = ax4.twinx()
        ax5.plot(dates, self.indicators['drawdown'][start_idx:end_idx], label='回撤', color='red')
        ax5.set_ylabel('回撤', color='red')
        ax5.tick_params(axis='y', labelcolor='red')
        ax5.invert_yaxis()  # 回撤为负值，反转y轴使其向下显示
        
        # 添加图例
        lines1, labels1 = ax4.get_legend_handles_labels()
        lines2, labels2 = ax5.get_legend_handles_labels()
        ax4.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        # 设置x轴标签
        plt.xticks(rotation=45)
        
        # 显示图表
        plt.tight_layout()
        plt.show()
    
    def generate_summary_report(self):
        """
        生成摘要报告
        """
        if self.data is None:
            raise ValueError("请先加载数据")
        
        # 确保计算了所有指标
        if 'daily_returns' not in self.indicators:
            self.calculate_returns()
        if 'volatility' not in self.indicators:
            self.calculate_volatility()
        if 'max_drawdown' not in self.indicators:
            self.calculate_drawdown()
        if 'sharpe_ratio' not in self.indicators:
            self.calculate_sharpe_ratio()
        
        # 提取数据
        close_prices = self.data[:, 3]
        returns = self.indicators['daily_returns']
        
        # 计算基本统计量
        start_price = close_prices[0]
        end_price = close_prices[-1]
        total_return = (end_price / start_price - 1) * 100
        annual_return = np.mean(returns) * 252 * 100
        annual_volatility = self.indicators['volatility'][-1] * 100
        max_drawdown = self.indicators['max_drawdown'] * 100
        sharpe_ratio = self.indicators['sharpe_ratio']
        
        # 打印报告
        print("\n" + "=" * 50)
        print("股票分析摘要报告")
        print("=" * 50)
        print(f"分析期间: {self.dates[0].strftime('%Y-%m-%d')} 至 {self.dates[-1].strftime('%Y-%m-%d')}")
        print(f"交易天数: {len(self.data)}天")
        print("\n价格信息:")
        print(f"起始价格: {start_price:.2f}")
        print(f"结束价格: {end_price:.2f}")
        print(f"价格变化: {end_price - start_price:.2f} ({total_return:.2f}%)")
        print(f"最高价格: {np.max(close_prices):.2f}")
        print(f"最低价格: {np.min(close_prices):.2f}")
        
        print("\n收益和风险指标:")
        print(f"年化收益率: {annual_return:.2f}%")
        print(f"年化波动率: {annual_volatility:.2f}%")
        print(f"最大回撤: {max_drawdown:.2f}%")
        print(f"夏普比率: {sharpe_ratio:.2f}")
        
        print("\n技术指标当前值:")
        if 'rsi' in self.indicators:
            print(f"RSI(14): {self.indicators['rsi'][-1]:.2f}")
        if 'macd_line' in self.indicators:
            print(f"MACD: {self.indicators['macd_line'][-1]:.4f}")
            print(f"MACD信号线: {self.indicators['macd_signal'][-1]:.4f}")
            print(f"MACD柱状图: {self.indicators['macd_histogram'][-1]:.4f}")
        
        print("\n" + "=" * 50)


def main():
    """主函数"""
    print("股票数据分析工具")
    print("=" * 50)
    
    # 创建分析器并加载样本数据
    analyzer = StockAnalyzer()
    analyzer.load_sample_data(days=252, volatility=0.015, trend=0.0002)
    
    # 计算技术指标
    analyzer.calculate_returns()
    analyzer.calculate_moving_average(20)
    analyzer.calculate_moving_average(50)
    analyzer.calculate_moving_average(200)
    analyzer.calculate_bollinger_bands()
    analyzer.calculate_rsi()
    analyzer.calculate_macd()
    analyzer.calculate_volatility()
    analyzer.calculate_drawdown()
    analyzer.calculate_sharpe_ratio()
    
    # 生成报告
    analyzer.generate_summary_report()
    
    # 绘制图表
    analyzer.plot_price_chart()
    analyzer.plot_indicators()
    
    print("\n分析完成！")


if __name__ == "__main__":
    main()