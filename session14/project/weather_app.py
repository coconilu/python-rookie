"""
天气信息获取器
Session14 项目：通过调用天气API获取指定城市的实时天气信息

功能：
1. 获取当前天气信息
2. 获取未来几天的天气预报
3. 支持多个城市查询
4. 历史查询记录
5. 天气数据可视化（简单文本图表）

作者：Python新手教程
日期：2024
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path

# 尝试导入requests
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    import urllib.request
    import urllib.parse
    HAS_REQUESTS = False

# 导入配置
try:
    from config import API_KEY, DEFAULT_CITIES
except ImportError:
    print("警告：未找到config.py，使用默认配置")
    API_KEY = ""  # 需要在config.py中设置
    DEFAULT_CITIES = ["Beijing", "Shanghai", "Guangzhou"]


class WeatherApp:
    """天气应用主类"""
    
    def __init__(self):
        # 使用OpenWeatherMap API（免费版）
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.api_key = API_KEY
        self.history_file = "weather_history.json"
        self.history = self.load_history()
        
        # 天气图标映射
        self.weather_icons = {
            'Clear': '☀️',
            'Clouds': '☁️',
            'Rain': '🌧️',
            'Drizzle': '🌦️',
            'Thunderstorm': '⛈️',
            'Snow': '❄️',
            'Mist': '🌫️',
            'Fog': '🌫️'
        }
    
    def get_current_weather(self, city):
        """
        获取指定城市的当前天气
        
        参数:
            city: 城市名称（英文）
        
        返回:
            dict: 天气信息字典
        """
        if not self.api_key:
            # 如果没有API key，使用模拟数据
            return self.get_mock_weather(city)
        
        url = f"{self.base_url}/weather"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric',  # 使用摄氏度
            'lang': 'zh_cn'     # 中文描述
        }
        
        try:
            if HAS_REQUESTS:
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                else:
                    print(f"API返回错误: {response.status_code}")
                    return None
            else:
                query_string = urllib.parse.urlencode(params)
                full_url = f"{url}?{query_string}"
                response = urllib.request.urlopen(full_url, timeout=10)
                data = json.loads(response.read().decode('utf-8'))
            
            # 解析天气数据
            weather_info = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'],
                'main': data['weather'][0]['main'],
                'wind_speed': data['wind']['speed'],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # 添加到历史记录
            self.add_to_history(city, weather_info)
            
            return weather_info
            
        except Exception as e:
            print(f"获取天气信息失败: {e}")
            return None
    
    def get_forecast(self, city, days=5):
        """
        获取天气预报
        
        参数:
            city: 城市名称
            days: 预报天数
        
        返回:
            list: 预报信息列表
        """
        if not self.api_key:
            return self.get_mock_forecast(city, days)
        
        url = f"{self.base_url}/forecast"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'zh_cn',
            'cnt': days * 8  # 每3小时一个数据点
        }
        
        try:
            if HAS_REQUESTS:
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                else:
                    return None
            else:
                query_string = urllib.parse.urlencode(params)
                full_url = f"{url}?{query_string}"
                response = urllib.request.urlopen(full_url, timeout=10)
                data = json.loads(response.read().decode('utf-8'))
            
            # 解析预报数据
            forecasts = []
            for item in data['list']:
                forecast = {
                    'datetime': item['dt_txt'],
                    'temperature': item['main']['temp'],
                    'description': item['weather'][0]['description'],
                    'main': item['weather'][0]['main']
                }
                forecasts.append(forecast)
            
            return forecasts
            
        except Exception as e:
            print(f"获取天气预报失败: {e}")
            return None
    
    def get_mock_weather(self, city):
        """获取模拟天气数据（用于演示）"""
        import random
        
        weather_conditions = ['Clear', 'Clouds', 'Rain']
        
        return {
            'city': city,
            'country': 'CN',
            'temperature': random.uniform(10, 30),
            'feels_like': random.uniform(8, 32),
            'humidity': random.randint(30, 80),
            'pressure': random.randint(1000, 1020),
            'description': '模拟天气数据',
            'main': random.choice(weather_conditions),
            'wind_speed': random.uniform(0, 10),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def get_mock_forecast(self, city, days):
        """获取模拟预报数据"""
        import random
        
        forecasts = []
        current_date = datetime.now()
        
        for i in range(days):
            date = current_date + timedelta(days=i)
            forecast = {
                'datetime': date.strftime('%Y-%m-%d'),
                'temperature': random.uniform(10, 30),
                'description': '模拟预报',
                'main': random.choice(['Clear', 'Clouds', 'Rain'])
            }
            forecasts.append(forecast)
        
        return forecasts
    
    def display_weather(self, weather_info):
        """显示天气信息"""
        if not weather_info:
            print("无天气数据")
            return
        
        icon = self.weather_icons.get(weather_info['main'], '🌈')
        
        print("\n" + "="*50)
        print(f"🏙️  {weather_info['city']}, {weather_info['country']} 天气信息")
        print("="*50)
        print(f"{icon} 天气状况: {weather_info['description']}")
        print(f"🌡️  温度: {weather_info['temperature']:.1f}°C")
        print(f"🤔 体感温度: {weather_info['feels_like']:.1f}°C")
        print(f"💧 湿度: {weather_info['humidity']}%")
        print(f"🌬️  风速: {weather_info['wind_speed']} m/s")
        print(f"⏰ 更新时间: {weather_info['timestamp']}")
        print("="*50)
    
    def display_forecast(self, city, forecasts):
        """显示天气预报"""
        if not forecasts:
            print("无预报数据")
            return
        
        print(f"\n{city} 天气预报")
        print("-"*50)
        
        # 按日期分组
        daily_forecast = {}
        for forecast in forecasts:
            date = forecast['datetime'].split()[0]
            if date not in daily_forecast:
                daily_forecast[date] = []
            daily_forecast[date].append(forecast)
        
        # 显示每日预报
        for date, day_forecasts in list(daily_forecast.items())[:5]:
            # 计算当日平均温度
            temps = [f['temperature'] for f in day_forecasts]
            avg_temp = sum(temps) / len(temps)
            
            # 获取主要天气状况
            weather_counts = {}
            for f in day_forecasts:
                main = f['main']
                weather_counts[main] = weather_counts.get(main, 0) + 1
            
            main_weather = max(weather_counts, key=weather_counts.get)
            icon = self.weather_icons.get(main_weather, '🌈')
            
            print(f"{date}: {icon} {main_weather}, 平均温度: {avg_temp:.1f}°C")
    
    def draw_temperature_chart(self, forecasts):
        """绘制简单的温度图表"""
        if not forecasts:
            return
        
        print("\n温度趋势图")
        print("-"*50)
        
        # 获取温度数据
        temps = []
        labels = []
        
        for i, forecast in enumerate(forecasts[:8]):  # 显示8个时间点
            temps.append(forecast['temperature'])
            time_str = forecast['datetime'].split()[1][:5]  # HH:MM
            labels.append(time_str)
        
        # 找出最大最小值
        max_temp = max(temps)
        min_temp = min(temps)
        range_temp = max_temp - min_temp
        
        # 绘制图表
        height = 10
        for h in range(height, -1, -1):
            temp_threshold = min_temp + (range_temp * h / height)
            line = f"{temp_threshold:5.1f}°C |"
            
            for temp in temps:
                if temp >= temp_threshold:
                    line += " ▓▓"
                else:
                    line += "   "
            
            print(line)
        
        # 时间标签
        print(" "*9 + "-"*25)
        print(" "*9, end="")
        for label in labels:
            print(f"{label[:3]}", end="")
        print()
    
    def load_history(self):
        """加载历史记录"""
        history_path = Path(self.history_file)
        if history_path.exists():
            try:
                with open(history_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载历史记录失败: {e}")
        return []
    
    def save_history(self):
        """保存历史记录"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存历史记录失败: {e}")
    
    def add_to_history(self, city, weather_info):
        """添加到历史记录"""
        history_entry = {
            'city': city,
            'weather': weather_info,
            'query_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.history.append(history_entry)
        
        # 保留最近100条记录
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        self.save_history()
    
    def show_history(self, limit=10):
        """显示历史查询记录"""
        if not self.history:
            print("无历史记录")
            return
        
        print(f"\n最近{limit}条查询记录:")
        print("-"*50)
        
        for entry in self.history[-limit:]:
            weather = entry['weather']
            print(f"{entry['query_time']} - {weather['city']}: "
                  f"{weather['temperature']:.1f}°C, {weather['description']}")
    
    def compare_cities(self, cities):
        """比较多个城市的天气"""
        print("\n城市天气对比")
        print("="*80)
        print(f"{'城市':^15} {'温度':^10} {'湿度':^10} {'天气':^15} {'风速':^10}")
        print("-"*80)
        
        for city in cities:
            weather = self.get_current_weather(city)
            if weather:
                icon = self.weather_icons.get(weather['main'], '🌈')
                print(f"{weather['city']:^15} "
                      f"{weather['temperature']:^10.1f}°C "
                      f"{weather['humidity']:^10}% "
                      f"{icon} {weather['main']:^12} "
                      f"{weather['wind_speed']:^10.1f}m/s")
                time.sleep(0.5)  # 避免请求过快
    
    def interactive_mode(self):
        """交互模式"""
        print("欢迎使用天气信息获取器！")
        print("="*50)
        
        while True:
            print("\n请选择操作：")
            print("1. 查询当前天气")
            print("2. 查询天气预报")
            print("3. 比较多个城市")
            print("4. 查看历史记录")
            print("5. 查看默认城市天气")
            print("0. 退出")
            
            choice = input("\n请输入选项: ")
            
            if choice == '0':
                print("感谢使用，再见！")
                break
            
            elif choice == '1':
                city = input("请输入城市名称（英文）: ")
                weather = self.get_current_weather(city)
                self.display_weather(weather)
            
            elif choice == '2':
                city = input("请输入城市名称（英文）: ")
                forecasts = self.get_forecast(city)
                self.display_forecast(city, forecasts)
                if forecasts:
                    self.draw_temperature_chart(forecasts)
            
            elif choice == '3':
                cities_input = input("请输入多个城市名称（用逗号分隔）: ")
                cities = [c.strip() for c in cities_input.split(',')]
                self.compare_cities(cities)
            
            elif choice == '4':
                self.show_history()
            
            elif choice == '5':
                self.compare_cities(DEFAULT_CITIES)
            
            else:
                print("无效选项，请重试")


def main():
    """主函数"""
    app = WeatherApp()
    
    # 检查是否有API密钥
    if not app.api_key:
        print("提示：未设置API密钥，将使用模拟数据")
        print("要使用真实数据，请：")
        print("1. 在 https://openweathermap.org 注册获取免费API密钥")
        print("2. 在 config.py 中设置 API_KEY = '你的密钥'")
        print()
    
    # 进入交互模式
    app.interactive_mode()


if __name__ == "__main__":
    main() 