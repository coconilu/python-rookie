"""
示例1：基础HTTP请求

本示例演示：
1. 使用urllib发送GET请求
2. 处理响应数据
3. 解析响应头信息
"""

import urllib.request
import urllib.error
import json


def basic_get_request():
    """发送基础的GET请求"""
    print("=== 基础GET请求示例 ===\n")
    
    # 目标URL
    url = "http://httpbin.org/get"
    
    try:
        # 发送请求
        print(f"正在请求: {url}")
        response = urllib.request.urlopen(url)
        
        # 获取响应信息
        print(f"状态码: {response.status}")
        print(f"响应头: ")
        for header, value in response.headers.items():
            print(f"  {header}: {value}")
        
        # 读取响应内容
        content = response.read()  # 返回字节数据
        text = content.decode('utf-8')  # 解码为字符串
        
        print(f"\n响应内容长度: {len(text)} 字符")
        print("响应内容预览:")
        print(text[:200] + "...")
        
        # 解析JSON响应
        data = json.loads(text)
        print(f"\n解析后的数据类型: {type(data)}")
        print(f"请求来源IP: {data.get('origin', '未知')}")
        
    except urllib.error.URLError as e:
        print(f"URL错误: {e}")
    except urllib.error.HTTPError as e:
        print(f"HTTP错误: {e.code} - {e.reason}")
    except Exception as e:
        print(f"其他错误: {e}")


def get_request_with_params():
    """发送带参数的GET请求"""
    print("\n\n=== 带参数的GET请求 ===\n")
    
    # 基础URL
    base_url = "http://httpbin.org/get"
    
    # 参数
    params = {
        'name': '小明',
        'age': 18,
        'city': '北京',
        'hobbies': '编程,阅读'  # 多个值用逗号分隔
    }
    
    # 编码参数
    from urllib.parse import urlencode
    query_string = urlencode(params)
    full_url = f"{base_url}?{query_string}"
    
    print(f"完整URL: {full_url}")
    
    try:
        response = urllib.request.urlopen(full_url)
        data = json.loads(response.read().decode('utf-8'))
        
        print("\n服务器接收到的参数:")
        for key, value in data['args'].items():
            print(f"  {key}: {value}")
            
    except Exception as e:
        print(f"请求失败: {e}")


def handle_different_content_types():
    """处理不同类型的响应内容"""
    print("\n\n=== 处理不同内容类型 ===\n")
    
    # 测试不同的内容类型
    test_urls = {
        'JSON': 'http://httpbin.org/json',
        'HTML': 'http://httpbin.org/html',
        'XML': 'http://httpbin.org/xml',
    }
    
    for content_type, url in test_urls.items():
        print(f"\n--- 请求 {content_type} 内容 ---")
        try:
            response = urllib.request.urlopen(url)
            
            # 获取内容类型
            content_type_header = response.headers.get('Content-Type', '')
            print(f"内容类型: {content_type_header}")
            
            # 读取内容
            content = response.read().decode('utf-8')
            
            # 根据类型处理
            if 'json' in content_type_header:
                data = json.loads(content)
                print(f"JSON数据键: {list(data.keys())}")
            elif 'html' in content_type_header:
                print(f"HTML内容长度: {len(content)} 字符")
                print(f"包含 <h1> 标签: {'<h1>' in content}")
            elif 'xml' in content_type_header:
                print(f"XML内容长度: {len(content)} 字符")
                print(f"是否以 <?xml 开头: {content.strip().startswith('<?xml')}")
                
        except Exception as e:
            print(f"请求失败: {e}")


def custom_headers():
    """发送自定义请求头"""
    print("\n\n=== 自定义请求头 ===\n")
    
    url = "http://httpbin.org/headers"
    
    # 创建请求对象
    request = urllib.request.Request(url)
    
    # 添加自定义请求头
    request.add_header('User-Agent', 'Python-Tutorial/1.0')
    request.add_header('Accept', 'application/json')
    request.add_header('X-Custom-Header', 'Hello from Python!')
    
    try:
        response = urllib.request.urlopen(request)
        data = json.loads(response.read().decode('utf-8'))
        
        print("服务器看到的请求头:")
        for header, value in data['headers'].items():
            print(f"  {header}: {value}")
            
    except Exception as e:
        print(f"请求失败: {e}")


def main():
    """运行所有示例"""
    print("HTTP请求基础示例\n")
    print("本示例将演示如何使用urllib库进行基础的HTTP请求")
    print("=" * 50)
    
    # 运行各个示例
    basic_get_request()
    get_request_with_params()
    handle_different_content_types()
    custom_headers()
    
    print("\n" + "=" * 50)
    print("示例运行完成！")
    print("\n学习要点：")
    print("1. urllib.request.urlopen() 用于发送请求")
    print("2. response.read() 返回字节数据，需要decode()")
    print("3. 使用urlencode()编码URL参数")
    print("4. 可以通过Request对象添加自定义请求头")


if __name__ == "__main__":
    main() 