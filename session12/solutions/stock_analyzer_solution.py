#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session12 项目解答：NumPy股票数据分析工具 - 完整解决方案

本文件提供了股票分析项目的完整解决方案，包含所有技术指标的实现、
数据可视化功能和详细的分析报告生成。

作者: Python教程团队
创建日期: 2024-12-19
"""

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


class StockAnalyzer:
    """
    股票数据分析器 - 完整解决方案
    
    使用NumPy实现各种技术指标的计算和分析功能
    """
    
    def __init__(self):
        """初始化分析器"""
        self.data = None
        self.dates = None
        self.prices = None
        self.volumes = None
        
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False
    
    def load_sample_data(self, days=252, initial_price=100.0, volatility=0.02):
        """
        生成模拟股票数据 - 完整解决方案
        
        参数:
            days: 交易天数，默认252天（一年）
            initial_price: 初始价格
            volatility: 波动率
            
        返回:
            dict: 包含价格、成交量等数据
        """
        print(f"生成{days}天的模拟股票数据...")
        
        np.random.seed(42)
        
        # 生成日期序列
        start_date = datetime.now() - timedelta(days=days)
        self.dates = [start_date + timedelta(days=i) for i in range(days)]
        
        # 生成价格数据（几何布朗运动）
        returns = np.random.normal(0.0005, volatility, days)  # 日收益率
        
        # 添加趋势和季节性
        trend = np.linspace(0, 0.2, days)  # 整体上升趋势
        seasonal = 0.05 * np.sin(2 * np.pi * np.arange(days) / 252)  # 年度季节性
        
        returns += trend / days + seasonal / days
        
        # 计算累积价格
        log_prices = np.cumsum(returns)
        self.prices = initial_price * np.exp(log_prices)
        
        # 生成成交量数据（与价格变化相关）
        price_changes = np.abs(np.diff(self.prices, prepend=self.prices[0]))
        base_volume = 1000000
        volume_multiplier = 1 + price_changes / np.mean(price_changes)
        self.volumes = base_volume * volume_multiplier * (0.5 + np.random.random(days))
        
        # 生成开高低收数据
        highs = self.prices * (1 + np.random.uniform(0, 0.03, days))
        lows = self.prices * (1 - np.random.uniform(0, 0.03, days))
        opens = np.roll(self.prices, 1)
        opens[0] = initial_price
        
        self.data = {
            'dates': self.dates,
            'opens': opens,
            'highs': highs,
            'lows': lows,
            'closes': self.prices,
            'volumes': self.volumes
        }
        
        print(f"数据生成完成：")
        print(f"  期间: {self.dates[0].strftime('%Y-%m-%d')} 至 {self.dates[-1].strftime('%Y-%m-%d')}")
        print(f"  初始价格: {self.prices[0]:.2f}")
        print(f"  最终价格: {self.prices[-1]:.2f}")
        print(f"  总收益率: {(self.prices[-1] / self.prices[0] - 1) * 100:.2f}%")
        print(f"  平均成交量: {np.mean(self.volumes):.0f}")
        
        return self.data
    
    def calculate_returns(self, period=1):
        """
        计算收益率 - 完整解决方案
        
        参数:
            period: 计算周期，1为日收益率
            
        返回:
            numpy.ndarray: 收益率数组
        """
        if self.prices is None:
            raise ValueError("请先加载数据")
        
        if period == 1:
            # 日收益率
            returns = np.diff(self.prices) / self.prices[:-1]
        else:
            # 多日收益率
            returns = (self.prices[period:] - self.prices[:-period]) / self.prices[:-period]
        
        return returns
    
    def calculate_moving_average(self, window=20):
        """
        计算移动平均线 - 完整解决方案
        
        参数:
            window: 移动窗口大小
            
        返回:
            numpy.ndarray: 移动平均值
        """
        if self.prices is None:
            raise ValueError("请先加载数据")
        
        # 使用卷积计算移动平均
        weights = np.ones(window) / window
        ma = np.convolve(self.prices, weights, mode='valid')
        
        # 为了保持数组长度一致，前面用NaN填充
        result = np.full(len(self.prices), np.nan)
        result[window-1:] = ma
        
        return result
    
    def calculate_bollinger_bands(self, window=20, num_std=2):
        """
        计算布林带 - 完整解决方案
        
        参数:
            window: 移动窗口大小
            num_std: 标准差倍数
            
        返回:
            tuple: (上轨, 中轨, 下轨)
        """
        if self.prices is None:
            raise ValueError("请先加载数据")
        
        # 计算移动平均（中轨）
        middle_band = self.calculate_moving_average(window)
        
        # 计算移动标准差
        rolling_std = np.full(len(self.prices), np.nan)
        for i in range(window-1, len(self.prices)):
            rolling_std[i] = np.std(self.prices[i-window+1:i+1])
        
        # 计算上下轨
        upper_band = middle_band + num_std * rolling_std
        lower_band = middle_band - num_std * rolling_std
        
        return upper_band, middle_band, lower_band
    
    def calculate_rsi(self, window=14):
        """
        计算相对强弱指数(RSI) - 完整解决方案
        
        参数:
            window: 计算窗口
            
        返回:
            numpy.ndarray: RSI值
        """
        if self.prices is None:
            raise ValueError("请先加载数据")
        
        # 计算价格变化
        price_changes = np.diff(self.prices)
        
        # 分离上涨和下跌
        gains = np.where(price_changes > 0, price_changes, 0)
        losses = np.where(price_changes < 0, -price_changes, 0)
        
        # 计算平均收益和损失
        avg_gains = np.full(len(self.prices), np.nan)
        avg_losses = np.full(len(self.prices), np.nan)
        
        # 初始平均值
        if len(gains) >= window:
            avg_gains[window] = np.mean(gains[:window])
            avg_losses[window] = np.mean(losses[:window])
            
            # 使用指数移动平均
            alpha = 1.0 / window
            for i in range(window + 1, len(self.prices)):
                avg_gains[i] = alpha * gains[i-1] + (1 - alpha) * avg_gains[i-1]
                avg_losses[i] = alpha * losses[i-1] + (1 - alpha) * avg_losses[i-1]
        
        # 计算RSI
        rs = avg_gains / (avg_losses + 1e-10)  # 避免除零
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def calculate_macd(self, fast=12, slow=26, signal=9):
        """
        计算MACD指标 - 完整解决方案
        
        参数:
            fast: 快线周期
            slow: 慢线周期
            signal: 信号线周期
            
        返回:
            tuple: (MACD线, 信号线, 柱状图)
        """
        if self.prices is None:
            raise ValueError("请先加载数据")
        
        # 计算指数移动平均
        def ema(data, span):
            alpha = 2.0 / (span + 1)
            ema_values = np.full(len(data), np.nan)
            ema_values[0] = data[0]
            
            for i in range(1, len(data)):
                ema_values[i] = alpha * data[i] + (1 - alpha) * ema_values[i-1]
            
            return ema_values
        
        # 计算快慢EMA
        ema_fast = ema(self.prices, fast)
        ema_slow = ema(self.prices, slow)
        
        # 计算MACD线
        macd_line = ema_fast - ema_slow
        
        # 计算信号线
        signal_line = ema(macd_line[~np.isnan(macd_line)], signal)
        
        # 调整信号线长度
        signal_full = np.full(len(self.prices), np.nan)
        valid_start = slow - 1
        signal_full[valid_start:valid_start + len(signal_line)] = signal_line
        
        # 计算柱状图
        histogram = macd_line - signal_full
        
        return macd_line, signal_full, histogram
    
    def calculate_volatility(self, window=20):
        """
        计算波动率 - 完整解决方案
        
        参数:
            window: 计算窗口
            
        返回:
            numpy.ndarray: 年化波动率
        """
        if self.prices is None:
            raise ValueError("请先加载数据")
        
        # 计算日收益率
        returns = self.calculate_returns()
        
        # 计算滚动标准差
        rolling_vol = np.full(len(self.prices), np.nan)
        
        for i in range(window, len(returns) + 1):
            rolling_vol[i] = np.std(returns[i-window:i]) * np.sqrt(252)  # 年化
        
        return rolling_vol
    
    def calculate_max_drawdown(self):
        """
        计算最大回撤 - 完整解决方案
        
        返回:
            tuple: (最大回撤, 回撤序列)
        """
        if self.prices is None:
            raise ValueError("请先加载数据")
        
        # 计算累积最高价
        cumulative_max = np.maximum.accumulate(self.prices)
        
        # 计算回撤
        drawdowns = (self.prices - cumulative_max) / cumulative_max
        
        # 最大回撤
        max_drawdown = np.min(drawdowns)
        
        return max_drawdown, drawdowns
    
    def calculate_sharpe_ratio(self, risk_free_rate=0.02):
        """
        计算夏普比率 - 完整解决方案
        
        参数:
            risk_free_rate: 无风险利率（年化）
            
        返回:
            float: 夏普比率
        """
        if self.prices is None:
            raise ValueError("请先加载数据")
        
        # 计算年化收益率
        total_return = (self.prices[-1] / self.prices[0]) - 1
        days_held = len(self.prices)
        annual_return = (1 + total_return) ** (252 / days_held) - 1
        
        # 计算年化波动率
        returns = self.calculate_returns()
        annual_volatility = np.std(returns) * np.sqrt(252)
        
        # 计算夏普比率
        sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility
        
        return sharpe_ratio
    
    def calculate_support_resistance(self, window=20, threshold=0.02):
        """
        计算支撑位和阻力位 - 完整解决方案
        
        参数:
            window: 查找窗口
            threshold: 价格阈值
            
        返回:
            tuple: (支撑位列表, 阻力位列表)
        """
        if self.prices is None:
            raise ValueError("请先加载数据")
        
        highs = self.data['highs']
        lows = self.data['lows']
        
        # 找局部高点（阻力位）
        resistance_levels = []
        for i in range(window, len(highs) - window):
            if highs[i] == np.max(highs[i-window:i+window+1]):
                resistance_levels.append(highs[i])
        
        # 找局部低点（支撑位）
        support_levels = []
        for i in range(window, len(lows) - window):
            if lows[i] == np.min(lows[i-window:i+window+1]):
                support_levels.append(lows[i])
        
        # 合并相近的水平
        def merge_levels(levels, threshold):
            if not levels:
                return []
            
            levels = sorted(levels)
            merged = [levels[0]]
            
            for level in levels[1:]:
                if abs(level - merged[-1]) / merged[-1] > threshold:
                    merged.append(level)
                else:
                    merged[-1] = (merged[-1] + level) / 2
            
            return merged
        
        support_levels = merge_levels(support_levels, threshold)
        resistance_levels = merge_levels(resistance_levels, threshold)
        
        return support_levels, resistance_levels
    
    def plot_price_chart(self, indicators=None, figsize=(15, 10)):
        """
        绘制价格图表 - 完整解决方案
        
        参数:
            indicators: 要显示的指标列表
            figsize: 图表大小
        """
        if self.prices is None:
            raise ValueError("请先加载数据")
        
        if indicators is None:
            indicators = ['ma20', 'bollinger', 'volume']
        
        # 创建子图
        fig, axes = plt.subplots(3, 1, figsize=figsize, height_ratios=[3, 1, 1])
        
        # 主价格图
        ax1 = axes[0]
        ax1.plot(self.dates, self.prices, label='收盘价', linewidth=2, color='black')
        
        # 添加移动平均线
        if 'ma20' in indicators:
            ma20 = self.calculate_moving_average(20)
            ax1.plot(self.dates, ma20, label='MA20', alpha=0.7, color='blue')
        
        if 'ma50' in indicators:
            ma50 = self.calculate_moving_average(50)
            ax1.plot(self.dates, ma50, label='MA50', alpha=0.7, color='red')
        
        # 添加布林带
        if 'bollinger' in indicators:
            upper, middle, lower = self.calculate_bollinger_bands()
            ax1.plot(self.dates, upper, label='布林上轨', alpha=0.5, color='gray', linestyle='--')
            ax1.plot(self.dates, lower, label='布林下轨', alpha=0.5, color='gray', linestyle='--')
            ax1.fill_between(self.dates, upper, lower, alpha=0.1, color='gray')
        
        # 添加支撑阻力位
        if 'support_resistance' in indicators:
            support, resistance = self.calculate_support_resistance()
            for level in support:
                ax1.axhline(y=level, color='green', linestyle=':', alpha=0.7, label='支撑位' if level == support[0] else "")
            for level in resistance:
                ax1.axhline(y=level, color='red', linestyle=':', alpha=0.7, label='阻力位' if level == resistance[0] else "")
        
        ax1.set_title('股票价格走势图', fontsize=16, fontweight='bold')
        ax1.set_ylabel('价格', fontsize=12)
        ax1.legend(loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        # 成交量图
        if 'volume' in indicators:
            ax2 = axes[1]
            colors = ['red' if self.prices[i] >= self.prices[i-1] else 'green' 
                     for i in range(1, len(self.prices))]
            colors.insert(0, 'red')  # 第一天默认红色
            
            ax2.bar(self.dates, self.volumes, color=colors, alpha=0.7, width=0.8)
            ax2.set_title('成交量', fontsize=14)
            ax2.set_ylabel('成交量', fontsize=12)
            ax2.grid(True, alpha=0.3)
        
        # RSI指标
        if 'rsi' in indicators:
            ax3 = axes[2]
            rsi = self.calculate_rsi()
            ax3.plot(self.dates, rsi, label='RSI(14)', color='purple', linewidth=2)
            ax3.axhline(y=70, color='red', linestyle='--', alpha=0.7, label='超买线(70)')
            ax3.axhline(y=30, color='green', linestyle='--', alpha=0.7, label='超卖线(30)')
            ax3.fill_between(self.dates, 70, 100, alpha=0.1, color='red')
            ax3.fill_between(self.dates, 0, 30, alpha=0.1, color='green')
            ax3.set_title('RSI相对强弱指数', fontsize=14)
            ax3.set_ylabel('RSI', fontsize=12)
            ax3.set_ylim(0, 100)
            ax3.legend()
            ax3.grid(True, alpha=0.3)
        
        plt.xlabel('日期', fontsize=12)
        plt.tight_layout()
        plt.show()
    
    def plot_technical_indicators(self, figsize=(15, 12)):
        """
        绘制技术指标图表 - 完整解决方案
        
        参数:
            figsize: 图表大小
        """
        if self.prices is None:
            raise ValueError("请先加载数据")
        
        fig, axes = plt.subplots(4, 1, figsize=figsize)
        
        # 1. MACD指标
        macd_line, signal_line, histogram = self.calculate_macd()
        
        ax1 = axes[0]
        ax1.plot(self.dates, macd_line, label='MACD', color='blue', linewidth=2)
        ax1.plot(self.dates, signal_line, label='信号线', color='red', linewidth=2)
        ax1.bar(self.dates, histogram, label='柱状图', alpha=0.6, 
               color=['red' if x > 0 else 'green' for x in histogram])
        ax1.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        ax1.set_title('MACD指标', fontsize=14, fontweight='bold')
        ax1.set_ylabel('MACD', fontsize=12)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. RSI指标
        rsi = self.calculate_rsi()
        
        ax2 = axes[1]
        ax2.plot(self.dates, rsi, label='RSI(14)', color='purple', linewidth=2)
        ax2.axhline(y=70, color='red', linestyle='--', alpha=0.7, label='超买线(70)')
        ax2.axhline(y=30, color='green', linestyle='--', alpha=0.7, label='超卖线(30)')
        ax2.axhline(y=50, color='gray', linestyle='-', alpha=0.5)
        ax2.fill_between(self.dates, 70, 100, alpha=0.1, color='red')
        ax2.fill_between(self.dates, 0, 30, alpha=0.1, color='green')
        ax2.set_title('RSI相对强弱指数', fontsize=14, fontweight='bold')
        ax2.set_ylabel('RSI', fontsize=12)
        ax2.set_ylim(0, 100)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. 波动率
        volatility = self.calculate_volatility()
        
        ax3 = axes[2]
        ax3.plot(self.dates, volatility * 100, label='年化波动率', color='orange', linewidth=2)
        ax3.axhline(y=np.nanmean(volatility) * 100, color='red', linestyle='--', 
                   alpha=0.7, label=f'平均波动率({np.nanmean(volatility)*100:.1f}%)')
        ax3.set_title('历史波动率', fontsize=14, fontweight='bold')
        ax3.set_ylabel('波动率 (%)', fontsize=12)
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. 回撤
        max_dd, drawdowns = self.calculate_max_drawdown()
        
        ax4 = axes[3]
        ax4.fill_between(self.dates, drawdowns * 100, 0, alpha=0.6, color='red', label='回撤')
        ax4.axhline(y=max_dd * 100, color='darkred', linestyle='--', 
                   label=f'最大回撤({max_dd*100:.2f}%)')
        ax4.set_title('回撤分析', fontsize=14, fontweight='bold')
        ax4.set_ylabel('回撤 (%)', fontsize=12)
        ax4.set_xlabel('日期', fontsize=12)
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def generate_analysis_report(self):
        """
        生成分析报告 - 完整解决方案
        
        返回:
            dict: 分析报告数据
        """
        if self.prices is None:
            raise ValueError("请先加载数据")
        
        print("\n" + "=" * 60)
        print("           股票技术分析报告")
        print("=" * 60)
        
        # 基本信息
        total_return = (self.prices[-1] / self.prices[0] - 1) * 100
        days_held = len(self.prices)
        annual_return = ((self.prices[-1] / self.prices[0]) ** (252 / days_held) - 1) * 100
        
        print(f"\n【基本信息】")
        print(f"分析期间: {self.dates[0].strftime('%Y-%m-%d')} 至 {self.dates[-1].strftime('%Y-%m-%d')}")
        print(f"交易天数: {days_held}天")
        print(f"初始价格: {self.prices[0]:.2f}")
        print(f"最终价格: {self.prices[-1]:.2f}")
        print(f"总收益率: {total_return:.2f}%")
        print(f"年化收益率: {annual_return:.2f}%")
        
        # 风险指标
        volatility = self.calculate_volatility()
        max_dd, _ = self.calculate_max_drawdown()
        sharpe = self.calculate_sharpe_ratio()
        
        print(f"\n【风险指标】")
        print(f"年化波动率: {np.nanmean(volatility)*100:.2f}%")
        print(f"最大回撤: {max_dd*100:.2f}%")
        print(f"夏普比率: {sharpe:.3f}")
        
        # 技术指标
        rsi = self.calculate_rsi()
        current_rsi = rsi[-1] if not np.isnan(rsi[-1]) else rsi[~np.isnan(rsi)][-1]
        
        macd_line, signal_line, histogram = self.calculate_macd()
        current_macd = macd_line[-1] if not np.isnan(macd_line[-1]) else 0
        current_signal = signal_line[-1] if not np.isnan(signal_line[-1]) else 0
        
        print(f"\n【技术指标】")
        print(f"当前RSI: {current_rsi:.2f}")
        print(f"当前MACD: {current_macd:.4f}")
        print(f"MACD信号线: {current_signal:.4f}")
        
        # RSI信号
        if current_rsi > 70:
            rsi_signal = "超买，考虑卖出"
        elif current_rsi < 30:
            rsi_signal = "超卖，考虑买入"
        else:
            rsi_signal = "中性"
        
        # MACD信号
        if current_macd > current_signal:
            macd_signal = "多头信号"
        else:
            macd_signal = "空头信号"
        
        print(f"RSI信号: {rsi_signal}")
        print(f"MACD信号: {macd_signal}")
        
        # 支撑阻力位
        support_levels, resistance_levels = self.calculate_support_resistance()
        current_price = self.prices[-1]
        
        print(f"\n【支撑阻力位】")
        print(f"当前价格: {current_price:.2f}")
        
        if support_levels:
            nearest_support = max([s for s in support_levels if s < current_price], default=None)
            if nearest_support:
                print(f"最近支撑位: {nearest_support:.2f} (距离: {((current_price - nearest_support) / current_price * 100):.2f}%)")
        
        if resistance_levels:
            nearest_resistance = min([r for r in resistance_levels if r > current_price], default=None)
            if nearest_resistance:
                print(f"最近阻力位: {nearest_resistance:.2f} (距离: {((nearest_resistance - current_price) / current_price * 100):.2f}%)")
        
        # 移动平均线分析
        ma20 = self.calculate_moving_average(20)
        ma50 = self.calculate_moving_average(50)
        
        current_ma20 = ma20[-1] if not np.isnan(ma20[-1]) else 0
        current_ma50 = ma50[-1] if not np.isnan(ma50[-1]) else 0
        
        print(f"\n【移动平均线】")
        print(f"MA20: {current_ma20:.2f}")
        print(f"MA50: {current_ma50:.2f}")
        
        if current_price > current_ma20 > current_ma50:
            ma_trend = "强势上升趋势"
        elif current_price > current_ma20:
            ma_trend = "短期上升趋势"
        elif current_price < current_ma20 < current_ma50:
            ma_trend = "强势下降趋势"
        elif current_price < current_ma20:
            ma_trend = "短期下降趋势"
        else:
            ma_trend = "震荡趋势"
        
        print(f"趋势判断: {ma_trend}")
        
        # 综合建议
        print(f"\n【投资建议】")
        
        signals = []
        if current_rsi < 30:
            signals.append("RSI超卖")
        elif current_rsi > 70:
            signals.append("RSI超买")
        
        if current_macd > current_signal:
            signals.append("MACD多头")
        else:
            signals.append("MACD空头")
        
        if current_price > current_ma20:
            signals.append("价格在MA20之上")
        else:
            signals.append("价格在MA20之下")
        
        # 风险评估
        if max_dd < -0.1:
            risk_level = "高风险"
        elif max_dd < -0.05:
            risk_level = "中等风险"
        else:
            risk_level = "低风险"
        
        print(f"技术信号: {', '.join(signals)}")
        print(f"风险等级: {risk_level}")
        
        # 具体建议
        buy_signals = sum([1 for s in signals if any(word in s for word in ['超卖', '多头', '之上'])])
        sell_signals = sum([1 for s in signals if any(word in s for word in ['超买', '空头', '之下'])])
        
        if buy_signals > sell_signals:
            recommendation = "建议买入或持有"
        elif sell_signals > buy_signals:
            recommendation = "建议卖出或观望"
        else:
            recommendation = "建议观望，等待明确信号"
        
        print(f"\n综合建议: {recommendation}")
        
        print(f"\n【风险提示】")
        print("1. 本分析仅基于技术指标，不构成投资建议")
        print("2. 投资有风险，入市需谨慎")
        print("3. 请结合基本面分析和市场环境做出决策")
        print("4. 建议设置止损位，控制风险")
        
        print("\n" + "=" * 60)
        print("报告生成完成")
        print("=" * 60)
        
        return {
            'total_return': total_return,
            'annual_return': annual_return,
            'volatility': np.nanmean(volatility) * 100,
            'max_drawdown': max_dd * 100,
            'sharpe_ratio': sharpe,
            'current_rsi': current_rsi,
            'rsi_signal': rsi_signal,
            'macd_signal': macd_signal,
            'ma_trend': ma_trend,
            'risk_level': risk_level,
            'recommendation': recommendation
        }


def main():
    """
    主函数：演示股票分析工具的使用 - 完整解决方案
    """
    print("Session12 项目解答：NumPy股票数据分析工具")
    print("=" * 50)
    
    # 创建分析器实例
    analyzer = StockAnalyzer()
    
    # 生成示例数据
    print("\n1. 生成模拟股票数据")
    data = analyzer.load_sample_data(days=252, initial_price=100.0, volatility=0.02)
    
    # 计算各种技术指标
    print("\n2. 计算技术指标")
    
    # 基础指标
    returns = analyzer.calculate_returns()
    ma20 = analyzer.calculate_moving_average(20)
    ma50 = analyzer.calculate_moving_average(50)
    
    print(f"日收益率统计:")
    print(f"  平均收益率: {np.mean(returns)*100:.4f}%")
    print(f"  收益率标准差: {np.std(returns)*100:.4f}%")
    print(f"  最大单日涨幅: {np.max(returns)*100:.2f}%")
    print(f"  最大单日跌幅: {np.min(returns)*100:.2f}%")
    
    # 高级指标
    upper, middle, lower = analyzer.calculate_bollinger_bands()
    rsi = analyzer.calculate_rsi()
    macd_line, signal_line, histogram = analyzer.calculate_macd()
    volatility = analyzer.calculate_volatility()
    max_dd, drawdowns = analyzer.calculate_max_drawdown()
    sharpe = analyzer.calculate_sharpe_ratio()
    
    print(f"\n技术指标摘要:")
    print(f"  当前RSI: {rsi[-1] if not np.isnan(rsi[-1]) else '计算中'}")
    print(f"  年化波动率: {np.nanmean(volatility)*100:.2f}%")
    print(f"  最大回撤: {max_dd*100:.2f}%")
    print(f"  夏普比率: {sharpe:.3f}")
    
    # 支撑阻力位
    support, resistance = analyzer.calculate_support_resistance()
    print(f"\n支撑阻力位:")
    print(f"  支撑位: {support[:3] if len(support) >= 3 else support}")
    print(f"  阻力位: {resistance[:3] if len(resistance) >= 3 else resistance}")
    
    # 生成图表
    print("\n3. 生成分析图表")
    print("正在生成价格走势图...")
    analyzer.plot_price_chart(['ma20', 'ma50', 'bollinger', 'volume', 'support_resistance'])
    
    print("正在生成技术指标图...")
    analyzer.plot_technical_indicators()
    
    # 生成分析报告
    print("\n4. 生成分析报告")
    report = analyzer.generate_analysis_report()
    
    print("\n=== 项目完成 - 学习总结 ===")
    print("恭喜！你已经完成了一个专业的股票分析工具。")
    print("\n本项目展示了NumPy在金融分析中的强大应用：")
    print("1. 数据生成和处理 - 模拟真实的股票数据")
    print("2. 技术指标计算 - RSI、MACD、布林带等")
    print("3. 风险管理指标 - 波动率、回撤、夏普比率")
    print("4. 数据可视化 - 专业的金融图表")
    print("5. 智能分析 - 自动生成投资建议")
    print("\n这些技能是量化金融的基础，NumPy是核心工具！")
    
    return analyzer, report


if __name__ == "__main__":
    analyzer, report = main()