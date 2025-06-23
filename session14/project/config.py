"""
天气应用配置文件

请在此处设置你的API密钥和其他配置项
"""

# OpenWeatherMap API密钥
# 获取免费密钥：https://openweathermap.org/api
# 注册后在 "API keys" 标签页获取
API_KEY = ""  # 在这里填入你的API密钥

# 默认城市列表
DEFAULT_CITIES = [
    "Beijing",      # 北京
    "Shanghai",     # 上海
    "Guangzhou",    # 广州
    "Shenzhen",     # 深圳
    "Hangzhou",     # 杭州
    "Chengdu",      # 成都
    "Wuhan",        # 武汉
    "Xian",         # 西安
]

# API配置
API_SETTINGS = {
    'timeout': 10,           # 请求超时时间（秒）
    'retry_times': 3,        # 重试次数
    'retry_delay': 1,        # 重试延迟（秒）
    'cache_duration': 600,   # 缓存持续时间（秒）
}

# 显示设置
DISPLAY_SETTINGS = {
    'temperature_unit': 'celsius',    # 温度单位：celsius/fahrenheit
    'wind_speed_unit': 'ms',         # 风速单位：ms（米/秒）/kmh（公里/小时）
    'language': 'zh_cn',             # API返回语言
}

# 天气图标映射（可自定义）
WEATHER_ICONS = {
    'Clear': '☀️',
    'Clouds': '☁️',
    'Rain': '🌧️',
    'Drizzle': '🌦️',
    'Thunderstorm': '⛈️',
    'Snow': '❄️',
    'Mist': '🌫️',
    'Fog': '🌫️',
    'Haze': '🌫️',
    'Dust': '💨',
    'Sand': '💨',
    'Ash': '🌋',
    'Squall': '💨',
    'Tornado': '🌪️'
}

# 城市别名（支持中文城市名）
CITY_ALIASES = {
    '北京': 'Beijing',
    '上海': 'Shanghai',
    '广州': 'Guangzhou',
    '深圳': 'Shenzhen',
    '杭州': 'Hangzhou',
    '成都': 'Chengdu',
    '武汉': 'Wuhan',
    '西安': 'Xian',
    '南京': 'Nanjing',
    '重庆': 'Chongqing',
    '天津': 'Tianjin',
    '苏州': 'Suzhou',
    '大连': 'Dalian',
    '青岛': 'Qingdao',
    '厦门': 'Xiamen',
} 