# Session14: 网络编程详细教程

## 引言：什么是网络编程？

想象一下，你想知道明天的天气，你会怎么做？你可能会：
1. 打开手机上的天气APP
2. APP向天气服务器发送请求："请告诉我北京明天的天气"
3. 服务器查询数据后返回："明天北京晴，温度15-25度"
4. APP显示这个信息给你

这就是网络编程的本质：**让程序通过网络与其他程序交流**。

## 1. 网络编程基础概念

### 1.1 客户端与服务器

```python
# 生活类比：
# 客户端 = 顾客（你的程序）
# 服务器 = 餐厅（提供数据的程序）
# HTTP请求 = 点餐
# HTTP响应 = 上菜

# 客户端发送请求的过程：
# 1. 建立连接（走进餐厅）
# 2. 发送请求（告诉服务员你要什么）
# 3. 等待响应（等待上菜）
# 4. 接收数据（享用美食）
```

### 1.2 URL的组成

URL就像是网络世界的地址，让我们能找到想要的资源：

```python
# URL示例：https://api.weather.com/v1/city/beijing?units=metric&lang=zh

# 分解这个URL：
# https://        - 协议（使用加密的HTTPS）
# api.weather.com - 域名（服务器的地址）
# /v1/city/beijing - 路径（具体的资源位置）
# ?units=metric&lang=zh - 查询参数（额外的要求）
```

## 2. 使用urllib进行HTTP请求

Python内置的`urllib`库可以帮助我们发送网络请求：

### 2.1 发送简单的GET请求

```python
import urllib.request
import urllib.parse

# 发送GET请求获取网页内容
def fetch_webpage(url):
    """
    获取网页内容
    
    参数:
        url: 要访问的网址
    
    返回:
        网页的HTML内容
    """
    try:
        # 发送请求并获取响应
        response = urllib.request.urlopen(url)
        
        # 读取响应内容
        content = response.read()
        
        # 将字节数据解码为字符串
        html = content.decode('utf-8')
        
        return html
    except Exception as e:
        print(f"获取网页失败：{e}")
        return None

# 使用示例
url = "http://httpbin.org/get"
result = fetch_webpage(url)
if result:
    print("获取成功！")
    print(result[:200])  # 只显示前200个字符
```

### 2.2 处理URL参数

```python
# 构建带参数的URL
def build_url_with_params(base_url, params):
    """
    构建带参数的URL
    
    参数:
        base_url: 基础URL
        params: 参数字典
    
    返回:
        完整的URL
    """
    # 将参数编码
    query_string = urllib.parse.urlencode(params)
    
    # 拼接URL
    full_url = f"{base_url}?{query_string}"
    
    return full_url

# 使用示例
base_url = "http://httpbin.org/get"
params = {
    "name": "张三",
    "age": 25,
    "city": "北京"
}

url = build_url_with_params(base_url, params)
print(f"构建的URL: {url}")
```

## 3. 使用requests库（推荐）

`requests`库让网络请求变得更简单：

```python
# 首先需要安装：pip install requests
import requests

# 3.1 简单的GET请求
def get_data_simple():
    """使用requests发送GET请求"""
    response = requests.get('http://httpbin.org/get')
    
    # requests自动处理编码
    print(response.text)
    
    # 获取状态码
    print(f"状态码: {response.status_code}")
    
    # 获取响应头
    print(f"响应头: {response.headers}")

# 3.2 带参数的GET请求
def get_data_with_params():
    """发送带参数的GET请求"""
    params = {
        'name': '小明',
        'age': 20
    }
    
    response = requests.get('http://httpbin.org/get', params=params)
    print(response.json())  # 自动解析JSON

# 3.3 发送POST请求
def post_data():
    """发送POST请求"""
    data = {
        'username': 'user123',
        'password': 'pass123'
    }
    
    response = requests.post('http://httpbin.org/post', data=data)
    print(response.json())
```

## 4. 处理JSON数据

大多数API返回JSON格式的数据：

```python
import json

def handle_json_response():
    """处理JSON响应"""
    # 模拟API响应
    response = requests.get('http://httpbin.org/json')
    
    # 方法1：使用response.json()
    data = response.json()
    print(f"数据类型: {type(data)}")
    
    # 方法2：手动解析
    json_text = response.text
    data2 = json.loads(json_text)
    
    # 访问JSON数据
    # 假设返回的数据结构是：
    # {
    #     "slideshow": {
    #         "author": "Yours Truly",
    #         "date": "date of publication",
    #         "slides": [...]
    #     }
    # }
    
    if 'slideshow' in data:
        author = data['slideshow']['author']
        print(f"作者: {author}")
```

## 5. 错误处理

网络请求可能会失败，必须做好错误处理：

```python
def safe_request(url):
    """安全的网络请求，包含完整的错误处理"""
    try:
        # 设置超时时间
        response = requests.get(url, timeout=5)
        
        # 检查HTTP状态码
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.Timeout:
        print("请求超时！")
    except requests.exceptions.ConnectionError:
        print("连接错误！")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP错误: {e}")
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
    except json.JSONDecodeError:
        print("JSON解析失败！")
    
    return None
```

## 6. 实战：调用真实的API

### 6.1 使用免费的API服务

```python
def get_user_info():
    """获取随机用户信息（使用randomuser.me API）"""
    url = "https://randomuser.me/api/"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        user = data['results'][0]
        
        # 提取用户信息
        name = f"{user['name']['first']} {user['name']['last']}"
        email = user['email']
        country = user['location']['country']
        
        print(f"姓名: {name}")
        print(f"邮箱: {email}")
        print(f"国家: {country}")
    else:
        print("获取用户信息失败")
```

### 6.2 使用请求头

```python
def request_with_headers():
    """发送带请求头的请求"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    
    response = requests.get('http://httpbin.org/headers', headers=headers)
    print(response.json())
```

## 7. 简单的网络爬虫

### 7.1 爬虫的道德准则

```python
# 爬虫三原则：
# 1. 遵守robots.txt规则
# 2. 控制请求频率，不要过度请求
# 3. 尊重网站的服务条款

import time

def polite_crawler(urls):
    """有礼貌的爬虫"""
    for url in urls:
        try:
            response = requests.get(url)
            # 处理数据...
            print(f"成功获取: {url}")
            
            # 重要：添加延迟，避免过度请求
            time.sleep(1)  # 等待1秒
        except Exception as e:
            print(f"获取 {url} 失败: {e}")
```

### 7.2 解析HTML内容

```python
# 使用正则表达式提取信息
import re

def extract_links(html):
    """从HTML中提取所有链接"""
    # 简单的链接匹配模式
    pattern = r'href="(https?://[^"]+)"'
    links = re.findall(pattern, html)
    return links

# 使用示例
html_content = '''
<html>
<body>
    <a href="https://www.example.com">Example</a>
    <a href="https://www.google.com">Google</a>
</body>
</html>
'''

links = extract_links(html_content)
print("找到的链接:", links)
```

## 8. 最佳实践

### 8.1 使用Session提高性能

```python
# 创建Session对象复用连接
session = requests.Session()

# 多次请求使用同一个session
for i in range(5):
    response = session.get(f'http://httpbin.org/get?page={i}')
    print(f"请求 {i+1} 完成")

# 关闭session
session.close()
```

### 8.2 处理大文件下载

```python
def download_file(url, filename):
    """下载大文件"""
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        
        with open(filename, 'wb') as file:
            # 分块下载，避免内存溢出
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    
    print(f"文件下载完成: {filename}")
```

## 总结

本课我们学习了：
1. 网络编程的基本概念
2. 使用urllib和requests库发送HTTP请求
3. 处理JSON数据
4. 错误处理的重要性
5. 调用真实API的方法
6. 简单爬虫的实现
7. 网络编程的最佳实践

记住：
- 永远要处理网络请求可能出现的错误
- 遵守API的使用条款和限制
- 爬虫要有道德，不要给服务器造成压力
- 保护好你的API密钥

## 练习建议

1. 尝试调用不同的免费API
2. 编写一个简单的网页内容提取器
3. 实现一个带缓存的API调用器
4. 学习使用更高级的HTML解析库（如BeautifulSoup）

继续加油！网络编程为你打开了连接世界的大门！ 