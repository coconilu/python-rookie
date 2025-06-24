#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session24 练习题3：并发编程和缓存优化

题目描述：
实现一个网页内容下载和分析器，需要：
1. 下载多个网页内容（模拟IO密集型任务）
2. 分析网页中的关键词频率（模拟CPU密集型任务）
3. 缓存分析结果避免重复计算

要求比较以下实现方式的性能：
- 串行处理 vs 多线程 vs 多进程
- 无缓存 vs 有缓存
- 不同的缓存策略（LRU, 简单字典缓存）

模拟场景：
- 网页下载：模拟网络延迟的IO操作
- 内容分析：计算密集型的文本处理
- 缓存：避免重复下载和分析相同URL

输出示例：
各种实现方式的执行时间和缓存命中率对比
"""

import time
import random
import threading
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import lru_cache
from collections import defaultdict, OrderedDict
import hashlib
import string


class SimpleCache:
    """
    简单的字典缓存实现
    """
    def __init__(self, max_size=128):
        self.cache = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def get(self, key):
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        else:
            self.misses += 1
            return None
    
    def put(self, key, value):
        if len(self.cache) >= self.max_size:
            # 简单的清理策略：删除第一个元素
            first_key = next(iter(self.cache))
            del self.cache[first_key]
        self.cache[key] = value
    
    def get_stats(self):
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate
        }
    
    def clear_stats(self):
        self.hits = 0
        self.misses = 0


class LRUCache:
    """
    LRU (Least Recently Used) 缓存实现
    """
    def __init__(self, max_size=128):
        self.cache = OrderedDict()
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def get(self, key):
        if key in self.cache:
            # 移动到末尾（最近使用）
            value = self.cache.pop(key)
            self.cache[key] = value
            self.hits += 1
            return value
        else:
            self.misses += 1
            return None
    
    def put(self, key, value):
        if key in self.cache:
            # 更新现有键
            self.cache.pop(key)
        elif len(self.cache) >= self.max_size:
            # 删除最久未使用的项（第一个）
            self.cache.popitem(last=False)
        
        self.cache[key] = value
    
    def get_stats(self):
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate
        }
    
    def clear_stats(self):
        self.hits = 0
        self.misses = 0


def simulate_web_download(url):
    """
    模拟网页下载（IO密集型任务）
    """
    # 模拟网络延迟
    delay = random.uniform(0.1, 0.5)  # 100-500ms的随机延迟
    time.sleep(delay)
    
    # 生成模拟的网页内容
    content_length = random.randint(1000, 5000)
    words = ['python', 'programming', 'web', 'development', 'code', 'software',
             'computer', 'technology', 'data', 'analysis', 'machine', 'learning',
             'artificial', 'intelligence', 'algorithm', 'performance', 'optimization']
    
    content = []
    for _ in range(content_length // 10):
        content.append(random.choice(words))
    
    return ' '.join(content)


def analyze_content(content):
    """
    分析网页内容（CPU密集型任务）
    """
    # 模拟复杂的文本分析
    words = content.lower().split()
    
    # 词频统计
    word_count = defaultdict(int)
    for word in words:
        # 清理标点符号
        clean_word = ''.join(c for c in word if c.isalnum())
        if clean_word:
            word_count[clean_word] += 1
    
    # 模拟一些CPU密集型计算
    total_chars = sum(len(word) for word in words)
    avg_word_length = total_chars / len(words) if words else 0
    
    # 找出最常见的词
    top_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # 添加一些计算密集型操作
    hash_value = hashlib.md5(content.encode()).hexdigest()
    
    return {
        'word_count': len(word_count),
        'total_words': len(words),
        'avg_word_length': avg_word_length,
        'top_words': top_words,
        'content_hash': hash_value
    }


def process_url_no_cache(url):
    """
    处理单个URL（无缓存）
    """
    content = simulate_web_download(url)
    analysis = analyze_content(content)
    return url, analysis


def process_url_with_cache(url, cache):
    """
    处理单个URL（带缓存）
    """
    # 检查缓存
    cached_result = cache.get(url)
    if cached_result is not None:
        return url, cached_result
    
    # 缓存未命中，执行实际处理
    content = simulate_web_download(url)
    analysis = analyze_content(content)
    
    # 存入缓存
    cache.put(url, analysis)
    
    return url, analysis


# 串行处理
def process_urls_serial(urls, use_cache=False, cache=None):
    """
    串行处理URL列表
    """
    results = []
    
    for url in urls:
        if use_cache and cache:
            result = process_url_with_cache(url, cache)
        else:
            result = process_url_no_cache(url)
        results.append(result)
    
    return results


# 多线程处理
def process_urls_threaded(urls, max_workers=4, use_cache=False, cache=None):
    """
    多线程处理URL列表（适合IO密集型）
    """
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        if use_cache and cache:
            futures = [executor.submit(process_url_with_cache, url, cache) for url in urls]
        else:
            futures = [executor.submit(process_url_no_cache, url) for url in urls]
        
        for future in futures:
            results.append(future.result())
    
    return results


# 多进程处理
def process_urls_multiprocess(urls, max_workers=4):
    """
    多进程处理URL列表（适合CPU密集型）
    注意：多进程不能直接共享缓存对象
    """
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_url_no_cache, url) for url in urls]
        results = [future.result() for future in futures]
    
    return results


def generate_test_urls(num_urls=50, duplicate_rate=0.3):
    """
    生成测试URL列表
    duplicate_rate: 重复URL的比例，用于测试缓存效果
    """
    base_urls = [f"https://example{i}.com/page{j}" 
                 for i in range(1, 21) for j in range(1, 6)]  # 100个基础URL
    
    urls = []
    num_duplicates = int(num_urls * duplicate_rate)
    num_unique = num_urls - num_duplicates
    
    # 添加唯一URL
    unique_urls = random.sample(base_urls, min(num_unique, len(base_urls)))
    urls.extend(unique_urls)
    
    # 添加重复URL
    for _ in range(num_duplicates):
        urls.append(random.choice(unique_urls))
    
    # 打乱顺序
    random.shuffle(urls)
    
    return urls


def benchmark_method(method_name, method_func, urls, **kwargs):
    """
    基准测试方法
    """
    print(f"\n测试 {method_name}...")
    
    start_time = time.time()
    results = method_func(urls, **kwargs)
    end_time = time.time()
    
    execution_time = end_time - start_time
    
    print(f"  执行时间: {execution_time:.4f} 秒")
    print(f"  处理URL数: {len(results)}")
    print(f"  平均每URL: {execution_time/len(results):.4f} 秒")
    
    # 如果使用了缓存，显示缓存统计
    if 'cache' in kwargs and kwargs['cache']:
        cache_stats = kwargs['cache'].get_stats()
        print(f"  缓存命中率: {cache_stats['hit_rate']:.2%}")
        print(f"  缓存命中: {cache_stats['hits']}, 未命中: {cache_stats['misses']}")
    
    return {
        'method': method_name,
        'time': execution_time,
        'results': results,
        'cache_stats': kwargs['cache'].get_stats() if 'cache' in kwargs and kwargs['cache'] else None
    }


def performance_comparison():
    """
    性能对比测试
    """
    print("Session24 练习题3: 并发编程和缓存优化")
    print("=" * 60)
    
    # 生成测试URL
    test_urls = generate_test_urls(30, duplicate_rate=0.4)  # 30个URL，40%重复率
    unique_urls = len(set(test_urls))
    
    print(f"生成测试URL: {len(test_urls)} 个 (其中 {unique_urls} 个唯一)")
    print(f"重复率: {(len(test_urls) - unique_urls) / len(test_urls):.1%}")
    
    # 准备不同的缓存
    simple_cache = SimpleCache(max_size=50)
    lru_cache = LRUCache(max_size=50)
    
    # 测试方法列表
    test_methods = [
        ("串行处理(无缓存)", process_urls_serial, {'use_cache': False}),
        ("串行处理(简单缓存)", process_urls_serial, {'use_cache': True, 'cache': simple_cache}),
        ("串行处理(LRU缓存)", process_urls_serial, {'use_cache': True, 'cache': lru_cache}),
        ("多线程(无缓存)", process_urls_threaded, {'max_workers': 4, 'use_cache': False}),
        ("多线程(简单缓存)", process_urls_threaded, {'max_workers': 4, 'use_cache': True, 'cache': SimpleCache(50)}),
        ("多进程(无缓存)", process_urls_multiprocess, {'max_workers': 4}),
    ]
    
    results = []
    
    for method_name, method_func, kwargs in test_methods:
        try:
            # 清理缓存统计（如果有的话）
            if 'cache' in kwargs and kwargs['cache']:
                kwargs['cache'].clear_stats()
            
            result = benchmark_method(method_name, method_func, test_urls, **kwargs)
            results.append(result)
            
        except Exception as e:
            print(f"  ❌ 方法 {method_name} 执行失败: {e}")
    
    # 结果对比
    print("\n" + "=" * 70)
    print("性能对比结果:")
    print("=" * 70)
    
    # 按执行时间排序
    results.sort(key=lambda x: x['time'])
    
    print(f"{'方法':<20} {'时间(秒)':<10} {'加速比':<8} {'缓存命中率':<12}")
    print("-" * 70)
    
    baseline_time = results[-1]['time']  # 最慢的作为基准
    
    for i, result in enumerate(results):
        speedup = baseline_time / result['time']
        cache_hit_rate = ""
        
        if result['cache_stats']:
            cache_hit_rate = f"{result['cache_stats']['hit_rate']:.1%}"
        else:
            cache_hit_rate = "N/A"
        
        status = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "  "
        
        print(f"{status} {result['method']:<18} "
              f"{result['time']:<10.4f} "
              f"{speedup:<8.1f}x "
              f"{cache_hit_rate:<12}")
    
    # 显示分析结果示例
    if results:
        sample_result = results[0]['results'][0][1]  # 第一个URL的分析结果
        print(f"\n分析结果示例:")
        print(f"总词数: {sample_result['total_words']}")
        print(f"唯一词数: {sample_result['word_count']}")
        print(f"平均词长: {sample_result['avg_word_length']:.2f}")
        print(f"高频词: {sample_result['top_words'][:3]}")


@lru_cache(maxsize=128)
def cached_fibonacci(n):
    """
    使用内置lru_cache的斐波那契数列
    """
    if n < 2:
        return n
    return cached_fibonacci(n-1) + cached_fibonacci(n-2)


def demo_builtin_cache():
    """
    演示Python内置的lru_cache装饰器
    """
    print("\n=== 内置lru_cache演示 ===")
    
    # 测试缓存效果
    start_time = time.time()
    result = cached_fibonacci(35)
    end_time = time.time()
    
    print(f"fibonacci(35) = {result}")
    print(f"执行时间: {end_time - start_time:.6f} 秒")
    print(f"缓存信息: {cached_fibonacci.cache_info()}")
    
    # 再次计算，应该很快
    start_time = time.time()
    result = cached_fibonacci(35)
    end_time = time.time()
    
    print(f"再次计算 fibonacci(35) = {result}")
    print(f"执行时间: {end_time - start_time:.6f} 秒")
    print(f"缓存信息: {cached_fibonacci.cache_info()}")


def solution():
    """
    练习解决方案
    """
    try:
        performance_comparison()
        demo_builtin_cache()
        
        print("\n=== 学习要点 ===")
        print("1. 多线程适合IO密集型任务（如网络请求）")
        print("2. 多进程适合CPU密集型任务（如复杂计算）")
        print("3. 缓存可以显著提高重复操作的性能")
        print("4. LRU缓存在内存有限时比简单缓存更智能")
        print("5. Python的@lru_cache装饰器使用简单且高效")
        print("6. 并发编程需要考虑线程安全和数据共享问题")
        
    except Exception as e:
        print(f"执行过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    solution()