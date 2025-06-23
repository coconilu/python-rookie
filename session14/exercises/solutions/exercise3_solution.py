"""
练习 14.3 参考答案：综合练习 - 新闻聚合器
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
        # 常见的停用词
        self.stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
                              'to', 'for', 'of', 'with', 'by', 'from', 'is', 'was', 
                              'are', 'were', 'been', 'be', 'have', 'has', 'had'])
    
    def fetch_hackernews_top_stories(self, limit=10):
        """
        获取Hacker News热门故事
        
        参数:
            limit: 获取的故事数量
        
        返回:
            list: 故事详情列表
        """
        stories = []
        
        try:
            # 获取热门故事ID列表
            url = f"{self.hn_api}/topstories.json"
            
            if HAS_REQUESTS:
                response = requests.get(url, timeout=10)
                story_ids = response.json()
            else:
                response = urllib.request.urlopen(url, timeout=10)
                story_ids = json.loads(response.read().decode('utf-8'))
            
            # 获取前limit个故事的详细信息
            for story_id in story_ids[:limit]:
                story_url = f"{self.hn_api}/item/{story_id}.json"
                
                try:
                    if HAS_REQUESTS:
                        response = requests.get(story_url, timeout=5)
                        story_data = response.json()
                    else:
                        response = urllib.request.urlopen(story_url, timeout=5)
                        story_data = json.loads(response.read().decode('utf-8'))
                    
                    # 提取需要的信息
                    story = {
                        'title': story_data.get('title', '无标题'),
                        'url': story_data.get('url', ''),
                        'score': story_data.get('score', 0),
                        'by': story_data.get('by', 'anonymous'),
                        'time': story_data.get('time', 0),
                        'descendants': story_data.get('descendants', 0)  # 评论数
                    }
                    stories.append(story)
                    
                    # 避免请求过快
                    time.sleep(0.2)
                    
                except Exception as e:
                    print(f"获取故事 {story_id} 失败: {e}")
            
            self.news_data['hackernews'] = stories
            
        except Exception as e:
            print(f"获取Hacker News热门故事失败: {e}")
        
        return stories
    
    def fetch_github_events(self, limit=10):
        """
        获取GitHub公开事件
        
        参数:
            limit: 获取的事件数量
        
        返回:
            list: 事件列表
        """
        events = []
        
        try:
            url = f"{self.github_api}/events"
            
            if HAS_REQUESTS:
                response = requests.get(url, timeout=10)
                all_events = response.json()
            else:
                request = urllib.request.Request(url)
                request.add_header('Accept', 'application/vnd.github.v3+json')
                response = urllib.request.urlopen(request, timeout=10)
                all_events = json.loads(response.read().decode('utf-8'))
            
            # 处理事件数据
            for event_data in all_events[:limit]:
                event_type = event_data.get('type', 'Unknown')
                actor = event_data.get('actor', {}).get('login', 'unknown')
                repo = event_data.get('repo', {}).get('name', 'unknown/unknown')
                created_at = event_data.get('created_at', '')
                
                # 根据事件类型生成描述
                event_icons = {
                    'PushEvent': '📤',
                    'PullRequestEvent': '🔀',
                    'IssuesEvent': '📝',
                    'WatchEvent': '⭐',
                    'ForkEvent': '🍴',
                    'CreateEvent': '🆕',
                    'DeleteEvent': '🗑️'
                }
                
                icon = event_icons.get(event_type, '📌')
                
                event = {
                    'type': event_type,
                    'actor': actor,
                    'repo': repo,
                    'created_at': created_at,
                    'icon': icon,
                    'description': f"{icon} {repo} - {event_type.replace('Event', '')} by {actor}"
                }
                
                events.append(event)
            
            self.news_data['github'] = events
            
        except Exception as e:
            print(f"获取GitHub事件失败: {e}")
        
        return events
    
    def crawl_news_website(self, url):
        """
        从指定网站爬取新闻标题
        
        参数:
            url: 要爬取的网站URL
        
        返回:
            list: 新闻标题列表
        """
        titles = []
        
        try:
            # 设置User-Agent
            if HAS_REQUESTS:
                headers = {'User-Agent': 'Python News Aggregator 1.0'}
                response = requests.get(url, headers=headers, timeout=10)
                html = response.text
            else:
                request = urllib.request.Request(url)
                request.add_header('User-Agent', 'Python News Aggregator 1.0')
                response = urllib.request.urlopen(request, timeout=10)
                html = response.read().decode('utf-8')
            
            # 提取所有标题标签内容
            title_patterns = [
                r'<h1[^>]*>(.*?)</h1>',
                r'<h2[^>]*>(.*?)</h2>',
                r'<h3[^>]*>(.*?)</h3>',
                r'<title>(.*?)</title>'
            ]
            
            for pattern in title_patterns:
                matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    # 清理HTML标签和空白
                    clean_title = re.sub(r'<[^>]+>', '', match)
                    clean_title = clean_title.strip()
                    if clean_title and len(clean_title) > 10:  # 过滤太短的标题
                        titles.append(clean_title)
            
            # 去重
            titles = list(set(titles))
            self.news_data['crawled'] = titles[:10]  # 限制数量
            
        except Exception as e:
            print(f"爬取网站失败: {e}")
        
        return titles
    
    def filter_by_keywords(self, items, keywords):
        """
        根据关键词过滤新闻
        
        参数:
            items: 新闻项目列表
            keywords: 关键词列表
        
        返回:
            list: 过滤后的新闻列表
        """
        if not keywords:
            return items
        
        filtered = []
        keywords_lower = [k.lower() for k in keywords]
        
        for item in items:
            # 获取要检查的文本
            if isinstance(item, dict):
                text = item.get('title', '') + ' ' + item.get('description', '')
            else:
                text = str(item)
            
            text_lower = text.lower()
            
            # 检查是否包含任意关键词
            if any(keyword in text_lower for keyword in keywords_lower):
                filtered.append(item)
        
        return filtered
    
    def extract_keywords(self, texts, top_n=5):
        """
        从文本中提取热门关键词
        
        参数:
            texts: 文本列表
            top_n: 返回前N个关键词
        
        返回:
            list: 关键词列表
        """
        # 合并所有文本
        all_text = ' '.join(texts)
        
        # 简单分词（按空格和标点）
        words = re.findall(r'\b[a-zA-Z]+\b', all_text.lower())
        
        # 过滤停用词和短词
        filtered_words = [w for w in words 
                         if w not in self.stop_words and len(w) > 3]
        
        # 统计词频
        word_counts = Counter(filtered_words)
        
        # 返回最常见的词
        return [word for word, count in word_counts.most_common(top_n)]
    
    def format_report(self):
        """
        生成格式化的新闻报告
        
        返回:
            str: 格式化的报告
        """
        report = []
        total_news = 0
        
        # 报告头部
        report.append("=" * 50)
        report.append("=== 今日科技新闻聚合 ===")
        report.append("=" * 50)
        report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Hacker News部分
        if self.news_data['hackernews']:
            report.append("【Hacker News 热门】")
            for i, story in enumerate(self.news_data['hackernews'][:5], 1):
                report.append(f"{i}. ⭐ {story['score']} - \"{story['title']}\"")
                if story['url']:
                    report.append(f"   链接: {story['url']}")
                report.append(f"   评论: {story['descendants']}条")
                report.append("")
            total_news += len(self.news_data['hackernews'])
        
        # GitHub事件部分
        if self.news_data['github']:
            report.append("【GitHub 动态】")
            for i, event in enumerate(self.news_data['github'][:5], 1):
                report.append(f"{i}. {event['description']}")
            report.append("")
            total_news += len(self.news_data['github'])
        
        # 爬取的新闻
        if self.news_data['crawled']:
            report.append("【其他新闻】")
            for title in self.news_data['crawled'][:5]:
                report.append(f"- \"{title}\"")
            report.append("")
            total_news += len(self.news_data['crawled'])
        
        # 统计信息
        report.append("=" * 50)
        report.append(f"总计: {total_news}条新闻")
        
        # 提取关键词
        all_texts = []
        for story in self.news_data['hackernews']:
            all_texts.append(story['title'])
        all_texts.extend(self.news_data['crawled'])
        
        if all_texts:
            keywords = self.extract_keywords(all_texts, 10)
            report.append(f"热门关键词: {', '.join(keywords)}")
        
        report.append("=" * 50)
        
        return "\n".join(report)
    
    def generate_html_report(self):
        """
        生成HTML格式的报告（高级功能）
        
        返回:
            str: HTML格式的报告
        """
        html = []
        html.append("""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>科技新闻聚合</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
                h1 { color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }
                h2 { color: #007bff; margin-top: 30px; }
                .news-item { background: white; padding: 15px; margin: 10px 0; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
                .score { color: #ff6600; font-weight: bold; }
                .link { color: #007bff; text-decoration: none; }
                .link:hover { text-decoration: underline; }
                .stats { color: #666; font-size: 0.9em; }
                .keywords { background: #e9ecef; padding: 10px; border-radius: 5px; margin-top: 20px; }
            </style>
        </head>
        <body>
        """)
        
        html.append(f"<h1>科技新闻聚合 - {datetime.now().strftime('%Y-%m-%d')}</h1>")
        
        # Hacker News
        if self.news_data['hackernews']:
            html.append("<h2>Hacker News 热门</h2>")
            for story in self.news_data['hackernews'][:10]:
                html.append('<div class="news-item">')
                html.append(f'<span class="score">⭐ {story["score"]}</span> ')
                html.append(f'<strong>{story["title"]}</strong><br>')
                if story['url']:
                    html.append(f'<a class="link" href="{story["url"]}" target="_blank">查看原文</a> | ')
                html.append(f'<span class="stats">评论: {story["descendants"]}条</span>')
                html.append('</div>')
        
        # GitHub事件
        if self.news_data['github']:
            html.append("<h2>GitHub 动态</h2>")
            for event in self.news_data['github'][:10]:
                html.append('<div class="news-item">')
                html.append(f'{event["description"]}')
                html.append('</div>')
        
        html.append("</body></html>")
        
        return "\n".join(html)
    
    def analyze_sentiment(self, text):
        """
        简单的情感分析（高级功能）
        
        参数:
            text: 要分析的文本
        
        返回:
            str: 情感标签（正面/负面/中性）
        """
        # 简单的基于关键词的情感分析
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 
                         'fantastic', 'love', 'best', 'awesome', 'brilliant']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'worst', 
                         'hate', 'poor', 'disappointing', 'failure', 'broken']
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "正面 😊"
        elif negative_count > positive_count:
            return "负面 😞"
        else:
            return "中性 😐"


def test_api_connection():
    """测试API连接"""
    print("测试API连接...")
    
    # 测试Hacker News API
    try:
        if HAS_REQUESTS:
            response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=5)
            success = response.status_code == 200
        else:
            response = urllib.request.urlopen("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=5)
            success = response.status == 200
        
        print(f"Hacker News API: {'✓ 连接成功' if success else '✗ 连接失败'}")
    except Exception as e:
        print(f"Hacker News API: ✗ 连接失败 - {e}")
    
    # 测试GitHub API
    try:
        if HAS_REQUESTS:
            response = requests.get("https://api.github.com/events", timeout=5)
            success = response.status_code == 200
        else:
            response = urllib.request.urlopen("https://api.github.com/events", timeout=5)
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
        
        # 生成HTML报告
        html_report = aggregator.generate_html_report()
        with open('news_report.html', 'w', encoding='utf-8') as f:
            f.write(html_report)
        print("\nHTML报告已保存到 news_report.html")
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
        "Python programming is awesome for data science",
        "Machine learning with Python and TensorFlow",
        "Python for web development using Django"
    ]
    keywords = aggregator.extract_keywords(sample_texts, 5)
    print(f"提取的关键词: {keywords}")
    
    # 测试情感分析
    print("\n测试情感分析:")
    test_texts = [
        "This is a great product, I love it!",
        "Terrible experience, worst service ever",
        "It's okay, nothing special"
    ]
    for text in test_texts:
        sentiment = aggregator.analyze_sentiment(text)
        print(f"文本: \"{text}\"")
        print(f"情感: {sentiment}")
    
    # 测试数字格式化
    print("\n测试数字格式化:")
    test_numbers = [123, 1234, 12345, 123456]
    for num in test_numbers:
        print(f"{num} -> {format_number(num)}") 