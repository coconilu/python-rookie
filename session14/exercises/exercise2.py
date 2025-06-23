"""
练习 14.2：API数据处理练习

任务描述：
创建一个程序，从多个API获取数据，进行处理和分析，并生成报告。

要求：
1. 使用 https://api.coindesk.com/v1/bpi/currentprice.json 获取比特币价格
2. 使用 https://api.exchangerate-api.com/v4/latest/USD 获取汇率信息
3. 计算比特币在不同货币中的价值
4. 生成一个价格报告，包含：
   - 比特币的美元价格
   - 比特币的人民币价格（使用汇率转换）
   - 比特币的欧元价格
   - 价格更新时间
5. 实现缓存机制，避免频繁调用API（可选）

示例输出：
=== 比特币价格报告 ===
更新时间: 2024-01-15 10:30:45

当前价格:
- USD: $42,567.89
- CNY: ¥304,123.45
- EUR: €38,910.23

24小时变化: +2.5%

数据来源: CoinDesk & ExchangeRate-API

提示：
- CoinDesk API返回的数据中，美元价格在 bpi.USD.rate_float
- 汇率API返回的数据中，汇率在 rates 字典中
- 处理时间格式可以使用 datetime 模块
- 格式化货币显示时注意千位分隔符
"""

import json
import time
from datetime import datetime

# 尝试导入requests
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    import urllib.request
    import urllib.error
    HAS_REQUESTS = False


class BitcoinPriceAnalyzer:
    """比特币价格分析器"""
    
    def __init__(self):
        self.bitcoin_api = "https://api.coindesk.com/v1/bpi/currentprice.json"
        self.exchange_api = "https://api.exchangerate-api.com/v4/latest/USD"
        self.cache = {}  # 简单的缓存字典
        self.cache_timeout = 300  # 缓存5分钟
    
    def get_bitcoin_price(self):
        """
        获取比特币价格信息
        
        返回:
            dict: 包含价格信息的字典，失败返回None
        """
        # TODO: 实现获取比特币价格的功能
        # 提示：
        # 1. 检查缓存是否有效
        # 2. 发送请求到 self.bitcoin_api
        # 3. 解析返回的JSON数据
        # 4. 提取需要的信息（USD价格、更新时间等）
        # 5. 更新缓存
        
        pass
    
    def get_exchange_rates(self):
        """
        获取美元对其他货币的汇率
        
        返回:
            dict: 汇率字典，失败返回None
        """
        # TODO: 实现获取汇率的功能
        # 提示：
        # 1. 发送请求到 self.exchange_api
        # 2. 解析返回的JSON数据
        # 3. 提取 rates 字典
        
        pass
    
    def calculate_prices(self, usd_price, exchange_rates):
        """
        计算比特币在不同货币中的价格
        
        参数:
            usd_price: 比特币的美元价格
            exchange_rates: 汇率字典
        
        返回:
            dict: 包含不同货币价格的字典
        """
        # TODO: 实现价格计算功能
        # 提示：
        # 1. 计算CNY价格: usd_price * exchange_rates['CNY']
        # 2. 计算EUR价格: usd_price * exchange_rates['EUR']
        # 3. 可以添加更多货币
        
        pass
    
    def format_currency(self, amount, currency_symbol):
        """
        格式化货币显示
        
        参数:
            amount: 金额
            currency_symbol: 货币符号
        
        返回:
            str: 格式化后的货币字符串
        """
        # TODO: 实现货币格式化功能
        # 提示：
        # 1. 使用 format 或 f-string 添加千位分隔符
        # 2. 保留2位小数
        # 3. 添加货币符号
        
        pass
    
    def generate_report(self):
        """
        生成价格报告
        
        返回:
            str: 格式化的报告字符串
        """
        # TODO: 实现报告生成功能
        # 提示：
        # 1. 调用 get_bitcoin_price() 获取比特币价格
        # 2. 调用 get_exchange_rates() 获取汇率
        # 3. 调用 calculate_prices() 计算各种货币价格
        # 4. 格式化输出报告
        
        pass
    
    def is_cache_valid(self, cache_key):
        """
        检查缓存是否有效
        
        参数:
            cache_key: 缓存键
        
        返回:
            bool: 缓存是否有效
        """
        if cache_key not in self.cache:
            return False
        
        cache_time = self.cache[cache_key].get('timestamp', 0)
        current_time = time.time()
        
        return (current_time - cache_time) < self.cache_timeout


def analyze_price_trend(prices_history):
    """
    分析价格趋势（扩展功能）
    
    参数:
        prices_history: 价格历史列表
    
    返回:
        dict: 包含趋势分析的字典
    """
    # TODO: 实现价格趋势分析（可选）
    # 可以计算：
    # - 平均价格
    # - 最高价和最低价
    # - 价格变化百分比
    
    pass


def main():
    """主函数"""
    print("练习14.2：比特币价格分析器\n")
    
    # 创建分析器实例
    analyzer = BitcoinPriceAnalyzer()
    
    # 生成报告
    report = analyzer.generate_report()
    
    if report:
        print(report)
    else:
        print("生成报告失败！")
    
    # 扩展功能：连续监控价格（可选）
    # monitor_prices(analyzer, duration=60, interval=10)


def monitor_prices(analyzer, duration=60, interval=10):
    """
    监控价格变化（扩展功能）
    
    参数:
        analyzer: 价格分析器实例
        duration: 监控持续时间（秒）
        interval: 更新间隔（秒）
    """
    print(f"\n开始监控价格变化（持续{duration}秒，每{interval}秒更新）...")
    
    start_time = time.time()
    prices_history = []
    
    while time.time() - start_time < duration:
        # TODO: 实现价格监控功能（可选）
        # 1. 获取当前价格
        # 2. 添加到历史记录
        # 3. 显示价格变化
        # 4. 等待下一次更新
        
        time.sleep(interval)
    
    # 分析价格趋势
    if prices_history:
        trend = analyze_price_trend(prices_history)
        print("\n价格趋势分析:")
        print(trend)


# 测试代码
if __name__ == "__main__":
    main()
    
    # 单元测试
    print("\n" + "="*50)
    print("单元测试：")
    
    analyzer = BitcoinPriceAnalyzer()
    
    # 测试汇率获取
    print("\n测试汇率获取:")
    rates = analyzer.get_exchange_rates()
    if rates:
        print(f"✓ 成功获取汇率")
        print(f"  USD->CNY: {rates.get('CNY', 'N/A')}")
        print(f"  USD->EUR: {rates.get('EUR', 'N/A')}")
    else:
        print("✗ 获取汇率失败")
    
    # 测试货币格式化
    print("\n测试货币格式化:")
    test_amount = 42567.89
    formatted = analyzer.format_currency(test_amount, "$")
    print(f"格式化结果: {formatted}")
    
    # 测试缓存机制
    print("\n测试缓存机制:")
    analyzer.cache['test'] = {'timestamp': time.time(), 'data': 'test_data'}
    print(f"缓存是否有效: {analyzer.is_cache_valid('test')}") 