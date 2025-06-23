"""
示例3：网络爬虫基础

本示例演示：
1. 爬虫的基本原理
2. 使用正则表达式提取信息
3. 爬虫礼仪和道德规范
4. 处理不同编码的网页
"""

import re
import time
import urllib.request
import urllib.parse
from urllib.error import URLError, HTTPError

# 尝试导入requests
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


def crawler_ethics():
    """爬虫道德规范说明"""
    print("=== 网络爬虫道德规范 ===\n")
    
    print("作为一个负责任的爬虫开发者，你应该：")
    print("1. 遵守robots.txt规则")
    print("2. 控制请求频率，不要给服务器造成压力")
    print("3. 使用合适的User-Agent标识自己")
    print("4. 尊重网站的服务条款")
    print("5. 不要爬取个人隐私信息")
    print("6. 考虑使用API而不是爬虫（如果有的话）")
    print("\n让我们看看如何检查robots.txt：")
    
    # 检查robots.txt
    site = "https://www.python.org"
    robots_url = f"{site}/robots.txt"
    
    try:
        if REQUESTS_AVAILABLE:
            response = requests.get(robots_url)
            content = response.text
        else:
            response = urllib.request.urlopen(robots_url)
            content = response.read().decode('utf-8')
        
        print(f"\n{site} 的 robots.txt 内容（前10行）:")
        lines = content.split('\n')[:10]
        for line in lines:
            print(f"  {line}")
            
    except Exception as e:
        print(f"获取robots.txt失败: {e}")


def extract_links_from_page():
    """从网页中提取所有链接"""
    print("\n\n=== 提取网页链接 ===\n")
    
    # 使用httpbin的HTML测试页面
    url = "http://httpbin.org/html"
    
    try:
        # 获取网页内容
        if REQUESTS_AVAILABLE:
            response = requests.get(url)
            html = response.text
        else:
            response = urllib.request.urlopen(url)
            html = response.read().decode('utf-8')
        
        print(f"从 {url} 提取链接：\n")
        
        # 方法1：使用正则表达式提取href属性
        href_pattern = r'href=[\'"]?([^\'" >]+)'
        links = re.findall(href_pattern, html)
        
        print("找到的链接:")
        for i, link in enumerate(links, 1):
            print(f"{i}. {link}")
        
        # 方法2：提取特定类型的链接
        print("\n只提取HTTP(S)链接:")
        http_pattern = r'href=[\'"]?(https?://[^\'" >]+)'
        http_links = re.findall(http_pattern, html)
        
        for i, link in enumerate(http_links, 1):
            print(f"{i}. {link}")
            
    except Exception as e:
        print(f"提取链接失败: {e}")


def extract_text_content():
    """提取网页的文本内容"""
    print("\n\n=== 提取文本内容 ===\n")
    
    url = "http://httpbin.org/html"
    
    try:
        if REQUESTS_AVAILABLE:
            response = requests.get(url)
            html = response.text
        else:
            response = urllib.request.urlopen(url)
            html = response.read().decode('utf-8')
        
        # 提取标题
        title_pattern = r'<title>(.*?)</title>'
        title_match = re.search(title_pattern, html, re.IGNORECASE | re.DOTALL)
        if title_match:
            print(f"页面标题: {title_match.group(1).strip()}")
        
        # 提取所有标题标签(h1-h6)
        print("\n所有标题:")
        heading_pattern = r'<h[1-6][^>]*>(.*?)</h[1-6]>'
        headings = re.findall(heading_pattern, html, re.IGNORECASE | re.DOTALL)
        
        for i, heading in enumerate(headings, 1):
            # 清理HTML标签
            clean_heading = re.sub(r'<[^>]+>', '', heading).strip()
            print(f"  {i}. {clean_heading}")
        
        # 提取段落文本
        print("\n段落文本:")
        paragraph_pattern = r'<p[^>]*>(.*?)</p>'
        paragraphs = re.findall(paragraph_pattern, html, re.IGNORECASE | re.DOTALL)
        
        for i, para in enumerate(paragraphs[:3], 1):  # 只显示前3个段落
            clean_para = re.sub(r'<[^>]+>', '', para).strip()
            if clean_para:
                print(f"\n段落{i}: {clean_para[:100]}...")
                
    except Exception as e:
        print(f"提取文本失败: {e}")


def extract_images():
    """提取网页中的图片信息"""
    print("\n\n=== 提取图片信息 ===\n")
    
    # 使用一个包含图片的测试页面
    url = "http://httpbin.org/html"
    
    try:
        if REQUESTS_AVAILABLE:
            response = requests.get(url)
            html = response.text
        else:
            response = urllib.request.urlopen(url)
            html = response.read().decode('utf-8')
        
        # 提取img标签
        img_pattern = r'<img[^>]+src=[\'"]?([^\'" >]+)[^>]*>'
        images = re.findall(img_pattern, html, re.IGNORECASE)
        
        if images:
            print("找到的图片:")
            for i, img_src in enumerate(images, 1):
                print(f"{i}. {img_src}")
                
                # 提取alt文本（如果有）
                alt_pattern = rf'<img[^>]*src=[\'"]?{re.escape(img_src)}[^>]*alt=[\'"]?([^\'"]+)'
                alt_match = re.search(alt_pattern, html, re.IGNORECASE)
                if alt_match:
                    print(f"   Alt文本: {alt_match.group(1)}")
        else:
            print("页面中没有找到图片")
            
    except Exception as e:
        print(f"提取图片失败: {e}")


def extract_table_data():
    """提取表格数据"""
    print("\n\n=== 提取表格数据 ===\n")
    
    # 创建一个包含表格的HTML示例
    html_with_table = """
    <html>
    <body>
        <table>
            <tr>
                <th>姓名</th>
                <th>年龄</th>
                <th>城市</th>
            </tr>
            <tr>
                <td>张三</td>
                <td>25</td>
                <td>北京</td>
            </tr>
            <tr>
                <td>李四</td>
                <td>30</td>
                <td>上海</td>
            </tr>
            <tr>
                <td>王五</td>
                <td>28</td>
                <td>广州</td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    print("从HTML表格中提取数据：")
    
    # 提取表格行
    row_pattern = r'<tr[^>]*>(.*?)</tr>'
    rows = re.findall(row_pattern, html_with_table, re.IGNORECASE | re.DOTALL)
    
    # 处理每一行
    table_data = []
    for row in rows:
        # 提取单元格
        cell_pattern = r'<t[hd][^>]*>(.*?)</t[hd]>'
        cells = re.findall(cell_pattern, row, re.IGNORECASE)
        
        # 清理单元格内容
        clean_cells = [re.sub(r'<[^>]+>', '', cell).strip() for cell in cells]
        if clean_cells:
            table_data.append(clean_cells)
    
    # 显示表格数据
    if table_data:
        # 表头
        headers = table_data[0]
        print("\n表头:", " | ".join(headers))
        print("-" * 30)
        
        # 数据行
        for row in table_data[1:]:
            print(" | ".join(row))


def crawl_with_encoding():
    """处理不同编码的网页"""
    print("\n\n=== 处理网页编码 ===\n")
    
    # 测试不同编码的处理
    test_urls = [
        ("http://httpbin.org/html", "UTF-8"),
        ("http://httpbin.org/encoding/utf8", "UTF-8"),
    ]
    
    for url, expected_encoding in test_urls:
        print(f"\n测试URL: {url}")
        print(f"预期编码: {expected_encoding}")
        
        try:
            if REQUESTS_AVAILABLE:
                response = requests.get(url)
                # requests会自动检测编码
                detected_encoding = response.encoding
                print(f"检测到的编码: {detected_encoding}")
                
                # 获取内容
                content = response.text
            else:
                response = urllib.request.urlopen(url)
                
                # 从响应头获取编码
                content_type = response.headers.get('Content-Type', '')
                encoding = 'utf-8'  # 默认编码
                
                if 'charset=' in content_type:
                    encoding = content_type.split('charset=')[-1]
                
                print(f"从响应头获取的编码: {encoding}")
                
                # 使用正确的编码解码内容
                content = response.read().decode(encoding)
            
            print(f"成功获取内容，长度: {len(content)} 字符")
            
        except Exception as e:
            print(f"处理失败: {e}")


def smart_crawler():
    """智能爬虫示例：综合运用各种技术"""
    print("\n\n=== 智能爬虫示例 ===\n")
    
    url = "http://httpbin.org/html"
    
    print(f"正在爬取: {url}")
    
    try:
        # 设置请求头，模拟浏览器
        headers = {
            'User-Agent': 'Mozilla/5.0 (Educational Spider) PythonTutorial/1.0',
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }
        
        # 发送请求
        if REQUESTS_AVAILABLE:
            response = requests.get(url, headers=headers, timeout=10)
            html = response.text
            status_code = response.status_code
        else:
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request, timeout=10)
            html = response.read().decode('utf-8')
            status_code = response.status
        
        print(f"响应状态码: {status_code}")
        
        # 提取页面信息
        info = {
            'title': '',
            'headings': [],
            'links': [],
            'images': [],
            'word_count': 0
        }
        
        # 提取标题
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        if title_match:
            info['title'] = title_match.group(1).strip()
        
        # 提取标题标签
        info['headings'] = re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>', html, re.IGNORECASE)
        
        # 提取链接
        info['links'] = re.findall(r'href=[\'"]?([^\'" >]+)', html)
        
        # 提取图片
        info['images'] = re.findall(r'<img[^>]+src=[\'"]?([^\'" >]+)', html, re.IGNORECASE)
        
        # 计算文本字数（移除所有HTML标签后）
        text_only = re.sub(r'<[^>]+>', '', html)
        info['word_count'] = len(text_only.split())
        
        # 显示结果
        print("\n爬取结果:")
        print(f"页面标题: {info['title']}")
        print(f"标题数量: {len(info['headings'])}")
        print(f"链接数量: {len(info['links'])}")
        print(f"图片数量: {len(info['images'])}")
        print(f"文本字数: {info['word_count']}")
        
        # 等待一秒（爬虫礼仪）
        time.sleep(1)
        
    except Exception as e:
        print(f"爬取失败: {e}")


def main():
    """运行所有爬虫示例"""
    print("网络爬虫基础示例\n")
    print("本示例演示基础的网页内容提取技术")
    print("=" * 50)
    
    # 运行各个示例
    examples = [
        (crawler_ethics, "爬虫道德规范"),
        (extract_links_from_page, "提取链接"),
        (extract_text_content, "提取文本"),
        (extract_images, "提取图片"),
        (extract_table_data, "提取表格"),
        (crawl_with_encoding, "处理编码"),
        (smart_crawler, "智能爬虫")
    ]
    
    for func, name in examples:
        try:
            func()
        except Exception as e:
            print(f"\n{name} 执行失败: {e}")
        
        # 爬虫礼仪：请求间隔
        time.sleep(0.5)
    
    print("\n" + "=" * 50)
    print("示例运行完成！")
    print("\n学习要点：")
    print("1. 正则表达式是提取信息的强大工具")
    print("2. 始终要遵守爬虫道德规范")
    print("3. 处理好网页编码问题")
    print("4. 添加适当的请求间隔")
    print("5. 考虑使用更专业的解析库（如BeautifulSoup）")


if __name__ == "__main__":
    main() 