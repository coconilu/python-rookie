"""
示例2：API调用实践

本示例演示：
1. 使用requests库调用API
2. 处理JSON响应
3. 调用多个免费API
4. 处理API认证（API Key）
"""

import json
import time

# 尝试导入requests
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    import urllib.request
    import urllib.parse
    print("提示：requests库未安装，将使用urllib作为备选")


def call_joke_api():
    """调用笑话API获取随机笑话"""
    print("=== 获取随机笑话 ===\n")
    
    # 使用免费的笑话API
    url = "https://v2.jokeapi.dev/joke/Programming?type=single"
    
    try:
        if REQUESTS_AVAILABLE:
            response = requests.get(url)
            response.raise_for_status()  # 检查HTTP错误
            data = response.json()
        else:
            response = urllib.request.urlopen(url)
            data = json.loads(response.read().decode('utf-8'))
        
        print(f"笑话类别: {data.get('category', '未知')}")
        print(f"笑话内容: {data.get('joke', '获取失败')}")
        print(f"安全等级: {'安全' if data.get('safe', False) else '可能不适合工作场合'}")
        
    except Exception as e:
        print(f"获取笑话失败: {e}")


def get_random_user():
    """获取随机用户信息"""
    print("\n\n=== 获取随机用户信息 ===\n")
    
    # RandomUser API
    url = "https://randomuser.me/api/?nat=us,gb,fr,de"
    
    try:
        if REQUESTS_AVAILABLE:
            response = requests.get(url)
            data = response.json()
        else:
            response = urllib.request.urlopen(url)
            data = json.loads(response.read().decode('utf-8'))
        
        # 提取用户信息
        user = data['results'][0]
        
        # 格式化输出
        print("随机用户信息:")
        print(f"姓名: {user['name']['title']} {user['name']['first']} {user['name']['last']}")
        print(f"性别: {'男' if user['gender'] == 'male' else '女'}")
        print(f"邮箱: {user['email']}")
        print(f"电话: {user['phone']}")
        print(f"国籍: {user['nat']}")
        print(f"地址: {user['location']['street']['number']} {user['location']['street']['name']}")
        print(f"城市: {user['location']['city']}")
        print(f"国家: {user['location']['country']}")
        
        # 显示头像URL
        print(f"头像: {user['picture']['medium']}")
        
    except Exception as e:
        print(f"获取用户信息失败: {e}")


def get_quote_of_the_day():
    """获取每日名言"""
    print("\n\n=== 获取励志名言 ===\n")
    
    # 使用quotable API
    url = "https://api.quotable.io/random"
    
    try:
        if REQUESTS_AVAILABLE:
            response = requests.get(url)
            data = response.json()
        else:
            response = urllib.request.urlopen(url)
            data = json.loads(response.read().decode('utf-8'))
        
        print(f"名言: {data.get('content', '获取失败')}")
        print(f"作者: {data.get('author', '未知')}")
        print(f"标签: {', '.join(data.get('tags', []))}")
        print(f"长度: {data.get('length', 0)} 字符")
        
    except Exception as e:
        print(f"获取名言失败: {e}")


def get_crypto_price():
    """获取加密货币价格"""
    print("\n\n=== 获取加密货币价格 ===\n")
    
    # CoinGecko API（免费，无需认证）
    coins = ['bitcoin', 'ethereum', 'dogecoin']
    url = "https://api.coingecko.com/api/v3/simple/price"
    
    params = {
        'ids': ','.join(coins),
        'vs_currencies': 'usd,cny',
        'include_24hr_change': 'true'
    }
    
    try:
        if REQUESTS_AVAILABLE:
            response = requests.get(url, params=params)
            data = response.json()
        else:
            query_string = urllib.parse.urlencode(params)
            full_url = f"{url}?{query_string}"
            response = urllib.request.urlopen(full_url)
            data = json.loads(response.read().decode('utf-8'))
        
        print("加密货币价格（实时）:")
        for coin in coins:
            if coin in data:
                coin_data = data[coin]
                print(f"\n{coin.capitalize()}:")
                print(f"  USD: ${coin_data.get('usd', 0):,.2f}")
                print(f"  CNY: ¥{coin_data.get('cny', 0):,.2f}")
                
                # 24小时涨跌
                change = coin_data.get('usd_24h_change', 0)
                change_symbol = '📈' if change > 0 else '📉'
                print(f"  24h变化: {change_symbol} {change:.2f}%")
                
    except Exception as e:
        print(f"获取加密货币价格失败: {e}")


def get_github_user():
    """获取GitHub用户信息"""
    print("\n\n=== 获取GitHub用户信息 ===\n")
    
    # GitHub API
    username = "torvalds"  # Linux创始人
    url = f"https://api.github.com/users/{username}"
    
    try:
        headers = {'Accept': 'application/vnd.github.v3+json'}
        
        if REQUESTS_AVAILABLE:
            response = requests.get(url, headers=headers)
            data = response.json()
        else:
            request = urllib.request.Request(url)
            request.add_header('Accept', 'application/vnd.github.v3+json')
            response = urllib.request.urlopen(request)
            data = json.loads(response.read().decode('utf-8'))
        
        print(f"GitHub用户: {username}")
        print(f"真实姓名: {data.get('name', '未公开')}")
        print(f"公司: {data.get('company', '未填写')}")
        print(f"位置: {data.get('location', '未知')}")
        print(f"简介: {data.get('bio', '无')}")
        print(f"公开仓库数: {data.get('public_repos', 0)}")
        print(f"关注者: {data.get('followers', 0)}")
        print(f"正在关注: {data.get('following', 0)}")
        print(f"创建时间: {data.get('created_at', '未知')}")
        
    except Exception as e:
        print(f"获取GitHub用户信息失败: {e}")


def batch_api_calls():
    """批量API调用示例"""
    print("\n\n=== 批量API调用示例 ===\n")
    
    # 获取多个国家的信息
    countries = ['china', 'usa', 'japan', 'germany']
    base_url = "https://restcountries.com/v3.1/name/"
    
    print("获取多个国家信息:")
    
    for country in countries:
        try:
            url = f"{base_url}{country}"
            
            if REQUESTS_AVAILABLE:
                response = requests.get(url)
                data = response.json()
            else:
                response = urllib.request.urlopen(url)
                data = json.loads(response.read().decode('utf-8'))
            
            if data and len(data) > 0:
                country_info = data[0]
                print(f"\n{country_info['name']['common']}:")
                print(f"  官方名称: {country_info['name']['official']}")
                print(f"  首都: {', '.join(country_info.get('capital', ['未知']))}")
                print(f"  人口: {country_info.get('population', 0):,}")
                print(f"  地区: {country_info.get('region', '未知')}")
                
            # 避免请求过快
            time.sleep(0.5)
            
        except Exception as e:
            print(f"\n获取 {country} 信息失败: {e}")


def api_with_pagination():
    """处理分页API响应"""
    print("\n\n=== 处理分页API ===\n")
    
    # 使用JSONPlaceholder API
    base_url = "https://jsonplaceholder.typicode.com/posts"
    
    # 获取前3页的数据
    all_posts = []
    posts_per_page = 10
    total_pages = 3
    
    print(f"获取前{total_pages}页的文章（每页{posts_per_page}篇）:")
    
    for page in range(1, total_pages + 1):
        try:
            params = {
                '_page': page,
                '_limit': posts_per_page
            }
            
            if REQUESTS_AVAILABLE:
                response = requests.get(base_url, params=params)
                posts = response.json()
            else:
                query_string = urllib.parse.urlencode(params)
                url = f"{base_url}?{query_string}"
                response = urllib.request.urlopen(url)
                posts = json.loads(response.read().decode('utf-8'))
            
            all_posts.extend(posts)
            print(f"  第{page}页: 获取了{len(posts)}篇文章")
            
        except Exception as e:
            print(f"  第{page}页获取失败: {e}")
    
    print(f"\n总共获取了 {len(all_posts)} 篇文章")
    
    # 显示前3篇文章的标题
    print("\n前3篇文章标题:")
    for i, post in enumerate(all_posts[:3], 1):
        print(f"{i}. {post.get('title', '无标题')}")


def main():
    """运行所有API调用示例"""
    print("API调用实践示例\n")
    print("本示例将调用多个免费的公开API")
    print("=" * 50)
    
    # 运行各个示例
    examples = [
        (call_joke_api, "笑话API"),
        (get_random_user, "随机用户API"),
        (get_quote_of_the_day, "名言API"),
        (get_crypto_price, "加密货币价格API"),
        (get_github_user, "GitHub API"),
        (batch_api_calls, "批量调用"),
        (api_with_pagination, "分页处理")
    ]
    
    for func, name in examples:
        try:
            func()
        except Exception as e:
            print(f"\n{name} 执行失败: {e}")
        
        # 稍作延迟，避免请求过快
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print("示例运行完成！")
    print("\n学习要点：")
    print("1. 不同的API有不同的数据格式")
    print("2. 始终要处理可能的错误")
    print("3. 注意API的使用限制")
    print("4. 使用适当的延迟避免过度请求")
    print("5. 了解如何处理分页数据")


if __name__ == "__main__":
    main() 