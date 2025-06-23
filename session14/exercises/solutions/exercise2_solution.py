"""
练习 14.2 参考答案：API数据处理练习
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
        # 检查缓存
        if self.is_cache_valid('bitcoin'):
            print("使用缓存的比特币价格数据")
            return self.cache['bitcoin']['data']
        
        try:
            if HAS_REQUESTS:
                response = requests.get(self.bitcoin_api, timeout=10)
                response.raise_for_status()
                data = response.json()
            else:
                response = urllib.request.urlopen(self.bitcoin_api, timeout=10)
                content = response.read().decode('utf-8')
                data = json.loads(content)
            
            # 提取需要的信息
            bitcoin_info = {
                'usd_price': data['bpi']['USD']['rate_float'],
                'usd_price_str': data['bpi']['USD']['rate'],
                'time': data['time']['updated'],
                'disclaimer': data['disclaimer']
            }
            
            # 更新缓存
            self.cache['bitcoin'] = {
                'timestamp': time.time(),
                'data': bitcoin_info
            }
            
            return bitcoin_info
            
        except Exception as e:
            print(f"获取比特币价格失败: {e}")
            return None
    
    def get_exchange_rates(self):
        """
        获取美元对其他货币的汇率
        
        返回:
            dict: 汇率字典，失败返回None
        """
        # 检查缓存
        if self.is_cache_valid('exchange'):
            print("使用缓存的汇率数据")
            return self.cache['exchange']['data']
        
        try:
            if HAS_REQUESTS:
                response = requests.get(self.exchange_api, timeout=10)
                response.raise_for_status()
                data = response.json()
            else:
                response = urllib.request.urlopen(self.exchange_api, timeout=10)
                content = response.read().decode('utf-8')
                data = json.loads(content)
            
            # 提取汇率
            rates = data.get('rates', {})
            
            # 更新缓存
            self.cache['exchange'] = {
                'timestamp': time.time(),
                'data': rates
            }
            
            return rates
            
        except Exception as e:
            print(f"获取汇率失败: {e}")
            return None
    
    def calculate_prices(self, usd_price, exchange_rates):
        """
        计算比特币在不同货币中的价格
        
        参数:
            usd_price: 比特币的美元价格
            exchange_rates: 汇率字典
        
        返回:
            dict: 包含不同货币价格的字典
        """
        prices = {
            'USD': usd_price,
            'CNY': usd_price * exchange_rates.get('CNY', 0),
            'EUR': usd_price * exchange_rates.get('EUR', 0),
            'GBP': usd_price * exchange_rates.get('GBP', 0),
            'JPY': usd_price * exchange_rates.get('JPY', 0)
        }
        
        return prices
    
    def format_currency(self, amount, currency_symbol):
        """
        格式化货币显示
        
        参数:
            amount: 金额
            currency_symbol: 货币符号
        
        返回:
            str: 格式化后的货币字符串
        """
        # 添加千位分隔符并保留2位小数
        formatted_amount = f"{amount:,.2f}"
        
        # 根据不同货币使用不同的符号
        currency_formats = {
            '$': f"${formatted_amount}",
            '¥': f"¥{formatted_amount}",
            '€': f"€{formatted_amount}",
            '£': f"£{formatted_amount}",
            'JPY': f"¥{amount:,.0f}"  # 日元通常不显示小数
        }
        
        return currency_formats.get(currency_symbol, f"{currency_symbol}{formatted_amount}")
    
    def generate_report(self):
        """
        生成价格报告
        
        返回:
            str: 格式化的报告字符串
        """
        # 获取比特币价格
        bitcoin_data = self.get_bitcoin_price()
        if not bitcoin_data:
            return "无法生成报告：获取比特币价格失败"
        
        # 获取汇率
        exchange_rates = self.get_exchange_rates()
        if not exchange_rates:
            return "无法生成报告：获取汇率失败"
        
        # 计算各种货币价格
        usd_price = bitcoin_data['usd_price']
        prices = self.calculate_prices(usd_price, exchange_rates)
        
        # 生成报告
        report = []
        report.append("=" * 40)
        report.append("=== 比特币价格报告 ===")
        report.append("=" * 40)
        report.append(f"更新时间: {bitcoin_data['time']}")
        report.append("")
        report.append("当前价格:")
        report.append(f"- USD: {self.format_currency(prices['USD'], '$')}")
        report.append(f"- CNY: {self.format_currency(prices['CNY'], '¥')}")
        report.append(f"- EUR: {self.format_currency(prices['EUR'], '€')}")
        report.append(f"- GBP: {self.format_currency(prices['GBP'], '£')}")
        report.append(f"- JPY: {self.format_currency(prices['JPY'], 'JPY')}")
        report.append("")
        report.append("汇率信息:")
        report.append(f"- 1 USD = {exchange_rates.get('CNY', 'N/A')} CNY")
        report.append(f"- 1 USD = {exchange_rates.get('EUR', 'N/A')} EUR")
        report.append(f"- 1 USD = {exchange_rates.get('GBP', 'N/A')} GBP")
        report.append(f"- 1 USD = {exchange_rates.get('JPY', 'N/A')} JPY")
        report.append("")
        report.append("数据来源: CoinDesk & ExchangeRate-API")
        report.append("=" * 40)
        
        return "\n".join(report)
    
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
    if not prices_history:
        return {}
    
    prices = [p['price'] for p in prices_history]
    
    trend = {
        '平均价格': sum(prices) / len(prices),
        '最高价': max(prices),
        '最低价': min(prices),
        '价格范围': max(prices) - min(prices),
        '记录数': len(prices)
    }
    
    # 计算变化百分比
    if len(prices) >= 2:
        change = ((prices[-1] - prices[0]) / prices[0]) * 100
        trend['变化百分比'] = f"{change:+.2f}%"
    
    return trend


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
        bitcoin_data = analyzer.get_bitcoin_price()
        
        if bitcoin_data:
            current_price = bitcoin_data['usd_price']
            prices_history.append({
                'time': datetime.now().strftime('%H:%M:%S'),
                'price': current_price
            })
            
            print(f"[{prices_history[-1]['time']}] ${current_price:,.2f}", end='')
            
            # 显示变化
            if len(prices_history) > 1:
                prev_price = prices_history[-2]['price']
                change = current_price - prev_price
                if change != 0:
                    print(f" ({change:+.2f})")
                else:
                    print(" (无变化)")
            else:
                print()
        
        time.sleep(interval)
    
    # 分析价格趋势
    if prices_history:
        print("\n" + "="*40)
        trend = analyze_price_trend(prices_history)
        print("价格趋势分析:")
        for key, value in trend.items():
            if isinstance(value, float):
                print(f"  {key}: ${value:,.2f}")
            else:
                print(f"  {key}: {value}")


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
    
    # 询问是否监控价格
    print("\n是否要监控价格变化？")
    print("注意：这将持续60秒")
    # monitor_prices(analyzer, duration=60, interval=10)


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
    
    # 再次调用API测试缓存
    print("\n测试缓存效果:")
    print("第一次调用:")
    analyzer.get_bitcoin_price()
    print("第二次调用（应该使用缓存）:")
    analyzer.get_bitcoin_price() 