"""
练习 14.3：综合练习 - 新闻聚合器

任务描述：
创建一个简单的新闻聚合器，从多个来源获取新闻，并生成一个综合报告。

要求：
1. 从至少2个不同的API获取新闻或文章：
   - https://hacker-news.firebaseio.com/v0/topstories.json (Hacker News)
   - https://api.github.com/events (GitHub公开事件)
   
2. 对于Hacker News:
   - 获取前10个热门故事ID
   - 获取每个故事的详细信息（标题、URL、评分等）
   
3. 对于GitHub Events:
   - 获取最新的10个公开事件
   - 提取事件类型、仓库名称、用户等信息
   
4. 实现一个简单的网页爬虫，从一个新闻网站提取标题
   
5. 将所有信息整合成一个格式化的报告

6. 高级功能（可选）：
   - 实现关键词过滤
   - 按时间排序
   - 生成HTML格式的报告
   - 添加简单的情感分析

示例输出：
=== 今日科技新闻聚合 ===
生成时间: 2024-01-15 14:30:00

【Hacker News 热门】
1. ⭐ 1234 - "人工智能的未来发展趋势"
   链接: https://example.com/ai-future
   评论: 456条

2. ⭐ 987 - "Python 3.13 新特性预览"
   链接: https://example.com/python-313
   评论: 234条

【GitHub 动态】
1. 🔀 facebook/react - Pull Request merged by user123
2. ⭐ microsoft/vscode - Starred by user456
3. 🍴 python/cpython - Forked by user789

【其他新闻】
- "技术公司季度财报超预期"
- "新的开源项目获得大量关注"

总计: 22条新闻
热门关键词: AI, Python, 开源

提示：
- Hacker News API文档: https://github.com/HackerNews/API
- 单个故事的API: https://hacker-news.firebaseio.com/v0/item/{id}.json
- 注意处理API限流
- 使用合适的数据结构存储新闻
"""

import json
import time
import re
from datetime import datetime
from collections import Counter

# 尝试导入必要的库
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    import urllib.request
    import urllib.error
    HAS_REQUESTS = False


class NewsAggregator:
    """新闻聚合器类"""
    
    def __init__(self):
        self.hn_api = "https://hacker-news.firebaseio.com/v0"
        self.github_api = "https://api.github.com"
        self.news_data = {
            'hackernews': [],
            'github': [],
            'crawled': []
        }
        self.keywords = []
    
    def fetch_hackernews_top_stories(self, limit=10):
        """
        获取Hacker News热门故事
        
        参数:
            limit: 获取的故事数量
        
        返回:
            list: 故事详情列表
        """
        # TODO: 实现获取Hacker News热门故事
        # 步骤：
        # 1. 获取热门故事ID列表: /topstories.json
        # 2. 获取前limit个故事的详细信息
        # 3. 提取标题、URL、评分、评论数等
        # 4. 处理可能的错误
        
        pass
    
    def fetch_github_events(self, limit=10):
        """
        获取GitHub公开事件
        
        参数:
            limit: 获取的事件数量
        
        返回:
            list: 事件列表
        """
        # TODO: 实现获取GitHub事件
        # 步骤：
        # 1. 调用 /events API
        # 2. 解析事件类型、仓库、用户等信息
        # 3. 格式化事件描述
        
        pass
    
    def crawl_news_website(self, url):
        """
        从指定网站爬取新闻标题
        
        参数:
            url: 要爬取的网站URL
        
        返回:
            list: 新闻标题列表
        """
        # TODO: 实现简单的新闻爬虫
        # 步骤：
        # 1. 获取网页内容
        # 2. 使用正则表达式提取标题
        # 3. 清理和格式化标题
        # 4. 注意爬虫礼仪
        
        pass
    
    def filter_by_keywords(self, items, keywords):
        """
        根据关键词过滤新闻
        
        参数:
            items: 新闻项目列表
            keywords: 关键词列表
        
        返回:
            list: 过滤后的新闻列表
        """
        # TODO: 实现关键词过滤
        # 可以检查标题或内容中是否包含关键词
        
        pass
    
    def extract_keywords(self, texts, top_n=5):
        """
        从文本中提取热门关键词
        
        参数:
            texts: 文本列表
            top_n: 返回前N个关键词
        
        返回:
            list: 关键词列表
        """
        # TODO: 实现简单的关键词提取
        # 步骤：
        # 1. 分词（简单的按空格分割）
        # 2. 过滤常见词（the, a, is等）
        # 3. 统计词频
        # 4. 返回高频词
        
        pass
    
    def format_report(self):
        """
        生成格式化的新闻报告
        
        返回:
            str: 格式化的报告
        """
        # TODO: 实现报告生成
        # 包含：
        # 1. 时间戳
        # 2. 各个来源的新闻
        # 3. 统计信息
        # 4. 热门关键词
        
        pass
    
    def generate_html_report(self):
        """
        生成HTML格式的报告（高级功能）
        
        返回:
            str: HTML格式的报告
        """
        # TODO: 生成HTML报告（可选）
        # 可以包含：
        # 1. CSS样式
        # 2. 可点击的链接
        # 3. 更好的格式化
        
        pass
    
    def analyze_sentiment(self, text):
        """
        简单的情感分析（高级功能）
        
        参数:
            text: 要分析的文本
        
        返回:
            str: 情感标签（正面/负面/中性）
        """
        # TODO: 实现简单的情感分析（可选）
        # 可以基于关键词匹配
        
        pass


def test_api_connection():
    """测试API连接"""
    print("测试API连接...")
    
    # 测试Hacker News API
    try:
        if HAS_REQUESTS:
            response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")
            success = response.status_code == 200
        else:
            response = urllib.request.urlopen("https://hacker-news.firebaseio.com/v0/topstories.json")
            success = response.status == 200
        
        print(f"Hacker News API: {'✓ 连接成功' if success else '✗ 连接失败'}")
    except Exception as e:
        print(f"Hacker News API: ✗ 连接失败 - {e}")
    
    # 测试GitHub API
    try:
        if HAS_REQUESTS:
            response = requests.get("https://api.github.com/events")
            success = response.status_code == 200
        else:
            response = urllib.request.urlopen("https://api.github.com/events")
            success = response.status == 200
        
        print(f"GitHub API: {'✓ 连接成功' if success else '✗ 连接失败'}")
    except Exception as e:
        print(f"GitHub API: ✗ 连接失败 - {e}")


def main():
    """主函数"""
    print("练习14.3：新闻聚合器\n")
    
    # 测试连接
    test_api_connection()
    print()
    
    # 创建聚合器
    aggregator = NewsAggregator()
    
    # 设置关键词过滤（可选）
    # aggregator.keywords = ['Python', 'AI', '开源']
    
    print("正在获取新闻...")
    
    # 获取Hacker News
    print("- 获取Hacker News热门故事...")
    hn_stories = aggregator.fetch_hackernews_top_stories(5)
    
    # 获取GitHub事件
    print("- 获取GitHub公开事件...")
    github_events = aggregator.fetch_github_events(5)
    
    # 爬取新闻网站（使用httpbin作为示例）
    print("- 爬取新闻网站...")
    crawled_news = aggregator.crawl_news_website("http://httpbin.org/html")
    
    # 生成报告
    print("\n生成报告...\n")
    report = aggregator.format_report()
    
    if report:
        print(report)
        
        # 可选：生成HTML报告
        # html_report = aggregator.generate_html_report()
        # with open('news_report.html', 'w', encoding='utf-8') as f:
        #     f.write(html_report)
        # print("\nHTML报告已保存到 news_report.html")
    else:
        print("生成报告失败！")


# 辅助函数
def format_number(num):
    """格式化大数字显示"""
    if num >= 1000:
        return f"{num/1000:.1f}k"
    return str(num)


def clean_html(text):
    """清理HTML标签"""
    return re.sub(r'<[^>]+>', '', text)


# 测试代码
if __name__ == "__main__":
    main()
    
    # 单元测试
    print("\n" + "="*50)
    print("单元测试：")
    
    aggregator = NewsAggregator()
    
    # 测试关键词提取
    print("\n测试关键词提取:")
    sample_texts = [
        "Python programming is awesome",
        "Machine learning with Python",
        "Python for data science"
    ]
    keywords = aggregator.extract_keywords(sample_texts)
    print(f"提取的关键词: {keywords}")
    
    # 测试数字格式化
    print("\n测试数字格式化:")
    test_numbers = [123, 1234, 12345, 123456]
    for num in test_numbers:
        print(f"{num} -> {format_number(num)}") 