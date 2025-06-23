"""
Session14 网络编程演示代码

本演示包含：
1. 使用urllib进行基础HTTP请求
2. 使用requests库进行高级HTTP操作
3. 处理JSON数据
4. 错误处理示例
5. 调用真实API
6. 简单的网络爬虫

作者：Python新手教程
日期：2024
"""

import urllib.request
import urllib.parse
import json
import time
import re

# 尝试导入requests库
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("提示：requests库未安装，部分功能将使用urllib替代")
    print("可以使用 'pip install requests' 安装")


def demo1_urllib_basic():
    """演示1：使用urllib进行基础HTTP请求"""
    print("\n=== 演示1：urllib基础请求 ===")
    
    # 1. 简单的GET请求
    url = "http://httpbin.org/get"
    try:
        response = urllib.request.urlopen(url)
        content = response.read().decode('utf-8')
        print(f"状态码: {response.status}")
        print(f"响应内容预览: {content[:100]}...")
    except Exception as e:
        print(f"请求失败: {e}")
    
    # 2. 带参数的请求
    print("\n--- 带参数的请求 ---")
    params = {'name': '张三', 'age': 25}
    query_string = urllib.parse.urlencode(params)
    full_url = f"{url}?{query_string}"
    
    try:
        response = urllib.request.urlopen(full_url)
        data = json.loads(response.read().decode('utf-8'))
        print(f"发送的参数: {data.get('args', {})}")
    except Exception as e:
        print(f"请求失败: {e}")


def demo2_requests_advanced():
    """演示2：使用requests库进行高级操作"""
    print("\n=== 演示2：requests高级操作 ===")
    
    if not REQUESTS_AVAILABLE:
        print("requests库未安装，跳过此演示")
        return
    
    # 1. GET请求
    print("--- GET请求 ---")
    response = requests.get('http://httpbin.org/get', 
                          params={'key': 'value', 'name': '小明'})
    print(f"状态码: {response.status_code}")
    print(f"请求URL: {response.url}")
    
    # 2. POST请求
    print("\n--- POST请求 ---")
    data = {'username': 'testuser', 'password': '123456'}
    response = requests.post('http://httpbin.org/post', data=data)
    result = response.json()
    print(f"POST数据: {result.get('form', {})}")
    
    # 3. 自定义请求头
    print("\n--- 自定义请求头 ---")
    headers = {
        'User-Agent': 'Python-Tutorial/1.0',
        'Accept': 'application/json'
    }
    response = requests.get('http://httpbin.org/headers', headers=headers)
    print(f"服务器看到的请求头: {response.json()['headers']['User-Agent']}")


def demo3_json_handling():
    """演示3：JSON数据处理"""
    print("\n=== 演示3：JSON数据处理 ===")
    
    # 模拟JSON数据
    json_data = {
        "name": "Python教程",
        "lesson": 14,
        "topics": ["HTTP", "API", "爬虫"],
        "students": [
            {"name": "小明", "score": 85},
            {"name": "小红", "score": 92}
        ]
    }
    
    # 1. Python对象转JSON字符串
    json_string = json.dumps(json_data, ensure_ascii=False, indent=2)
    print("JSON字符串:")
    print(json_string)
    
    # 2. JSON字符串转Python对象
    parsed_data = json.loads(json_string)
    print(f"\n课程名称: {parsed_data['name']}")
    print(f"学生成绩: ")
    for student in parsed_data['students']:
        print(f"  {student['name']}: {student['score']}分")


def demo4_error_handling():
    """演示4：错误处理"""
    print("\n=== 演示4：错误处理 ===")
    
    # 测试不同的错误情况
    test_urls = [
        ("http://httpbin.org/status/404", "404错误"),
        ("http://httpbin.org/delay/10", "超时错误"),
        ("http://invalid-domain-name-12345.com", "域名错误"),
        ("http://httpbin.org/get", "正常请求")
    ]
    
    for url, description in test_urls:
        print(f"\n测试 {description}: {url}")
        try:
            if REQUESTS_AVAILABLE:
                response = requests.get(url, timeout=2)
                response.raise_for_status()
                print(f"✓ 请求成功，状态码: {response.status_code}")
            else:
                response = urllib.request.urlopen(url, timeout=2)
                print(f"✓ 请求成功，状态码: {response.status}")
        except Exception as e:
            print(f"✗ 请求失败: {type(e).__name__}: {e}")


def demo5_real_api():
    """演示5：调用真实API"""
    print("\n=== 演示5：调用真实API ===")
    
    # 使用免费的API获取随机用户信息
    print("--- 获取随机用户信息 ---")
    
    try:
        if REQUESTS_AVAILABLE:
            response = requests.get('https://randomuser.me/api/')
            data = response.json()
        else:
            response = urllib.request.urlopen('https://randomuser.me/api/')
            data = json.loads(response.read().decode('utf-8'))
        
        user = data['results'][0]
        print(f"姓名: {user['name']['first']} {user['name']['last']}")
        print(f"邮箱: {user['email']}")
        print(f"国家: {user['location']['country']}")
        print(f"城市: {user['location']['city']}")
    except Exception as e:
        print(f"获取用户信息失败: {e}")
    
    # 获取公开的GitHub仓库信息
    print("\n--- 获取GitHub仓库信息 ---")
    repo_url = "https://api.github.com/repos/python/cpython"
    
    try:
        if REQUESTS_AVAILABLE:
            response = requests.get(repo_url)
            repo_data = response.json()
        else:
            response = urllib.request.urlopen(repo_url)
            repo_data = json.loads(response.read().decode('utf-8'))
        
        print(f"仓库名称: {repo_data['name']}")
        print(f"描述: {repo_data['description'][:50]}...")
        print(f"Stars: {repo_data['stargazers_count']}")
        print(f"Forks: {repo_data['forks_count']}")
    except Exception as e:
        print(f"获取仓库信息失败: {e}")


def demo6_simple_crawler():
    """演示6：简单的网络爬虫"""
    print("\n=== 演示6：简单网络爬虫 ===")
    
    # 爬取示例网页
    url = "http://httpbin.org/html"
    
    try:
        if REQUESTS_AVAILABLE:
            response = requests.get(url)
            html_content = response.text
        else:
            response = urllib.request.urlopen(url)
            html_content = response.read().decode('utf-8')
        
        # 使用正则表达式提取标题
        title_pattern = r'<h1>(.*?)</h1>'
        titles = re.findall(title_pattern, html_content)
        
        print("找到的标题:")
        for i, title in enumerate(titles, 1):
            print(f"{i}. {title}")
        
        # 提取所有链接
        link_pattern = r'href="([^"]+)"'
        links = re.findall(link_pattern, html_content)
        
        print(f"\n找到 {len(links)} 个链接")
        print("前5个链接:")
        for link in links[:5]:
            print(f"  - {link}")
            
    except Exception as e:
        print(f"爬取失败: {e}")


def demo7_session_performance():
    """演示7：使用Session提高性能"""
    print("\n=== 演示7：Session性能优化 ===")
    
    if not REQUESTS_AVAILABLE:
        print("需要requests库支持，跳过此演示")
        return
    
    # 不使用Session的方式
    print("--- 不使用Session (每次新建连接) ---")
    start_time = time.time()
    for i in range(5):
        response = requests.get(f'http://httpbin.org/get?page={i}')
        print(f"请求 {i+1} 完成")
    end_time = time.time()
    time_without_session = end_time - start_time
    print(f"总耗时: {time_without_session:.2f}秒")
    
    # 使用Session的方式
    print("\n--- 使用Session (复用连接) ---")
    start_time = time.time()
    with requests.Session() as session:
        for i in range(5):
            response = session.get(f'http://httpbin.org/get?page={i}')
            print(f"请求 {i+1} 完成")
    end_time = time.time()
    time_with_session = end_time - start_time
    print(f"总耗时: {time_with_session:.2f}秒")
    
    if time_with_session < time_without_session:
        improvement = ((time_without_session - time_with_session) / time_without_session) * 100
        print(f"\n使用Session性能提升: {improvement:.1f}%")


def main():
    """主函数：运行所有演示"""
    print("=" * 50)
    print("Session14: 网络编程 - 综合演示")
    print("=" * 50)
    
    demos = [
        (demo1_urllib_basic, "urllib基础请求"),
        (demo2_requests_advanced, "requests高级操作"),
        (demo3_json_handling, "JSON数据处理"),
        (demo4_error_handling, "错误处理"),
        (demo5_real_api, "真实API调用"),
        (demo6_simple_crawler, "简单网络爬虫"),
        (demo7_session_performance, "Session性能优化")
    ]
    
    for i, (demo_func, demo_name) in enumerate(demos, 1):
        print(f"\n{'='*20} {i}. {demo_name} {'='*20}")
        try:
            demo_func()
        except Exception as e:
            print(f"演示出错: {e}")
        
        # 暂停一下，避免请求过快
        time.sleep(0.5)
    
    print("\n" + "=" * 50)
    print("所有演示完成！")
    print("\n学习建议：")
    print("1. 尝试修改代码，调用其他API")
    print("2. 为网络请求添加更多的错误处理")
    print("3. 学习使用BeautifulSoup等库来解析HTML")
    print("4. 了解更多HTTP协议的知识")
    print("=" * 50)


if __name__ == "__main__":
    main() 