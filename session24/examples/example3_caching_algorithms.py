#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session24 示例3：缓存和算法优化

本示例演示各种缓存技术和算法优化方法，包括LRU缓存、
自定义缓存、算法复杂度优化等。

作者: Python教程团队
创建日期: 2024-01-20
"""

import time
import functools
from collections import OrderedDict, defaultdict
import hashlib


class SimpleCache:
    """简单缓存实现"""
    
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
            # 简单的FIFO策略
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        self.cache[key] = value
    
    def stats(self):
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        return f"命中率: {hit_rate:.2%} (命中: {self.hits}, 未命中: {self.misses})"


class LRUCache:
    """LRU缓存实现"""
    
    def __init__(self, capacity=128):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.hits = 0
        self.misses = 0
    
    def get(self, key):
        if key in self.cache:
            # 移动到末尾（最近使用）
            self.cache.move_to_end(key)
            self.hits += 1
            return self.cache[key]
        else:
            self.misses += 1
            return None
    
    def put(self, key, value):
        if key in self.cache:
            # 更新现有键
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            # 删除最久未使用的项
            self.cache.popitem(last=False)
        
        self.cache[key] = value
    
    def stats(self):
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        return f"LRU命中率: {hit_rate:.2%} (命中: {self.hits}, 未命中: {self.misses})"


def fibonacci_comparison():
    """斐波那契数列计算的不同实现比较"""
    print("\n=== 斐波那契数列计算比较 ===")
    
    # 1. 朴素递归实现
    def fibonacci_naive(n):
        if n <= 1:
            return n
        return fibonacci_naive(n-1) + fibonacci_naive(n-2)
    
    # 2. 使用functools.lru_cache
    @functools.lru_cache(maxsize=None)
    def fibonacci_cached(n):
        if n <= 1:
            return n
        return fibonacci_cached(n-1) + fibonacci_cached(n-2)
    
    # 3. 动态规划实现
    def fibonacci_dp(n):
        if n <= 1:
            return n
        
        dp = [0] * (n + 1)
        dp[1] = 1
        
        for i in range(2, n + 1):
            dp[i] = dp[i-1] + dp[i-2]
        
        return dp[n]
    
    # 4. 空间优化的动态规划
    def fibonacci_optimized(n):
        if n <= 1:
            return n
        
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        
        return b
    
    # 5. 使用自定义缓存
    cache = {}
    def fibonacci_manual_cache(n):
        if n in cache:
            return cache[n]
        
        if n <= 1:
            result = n
        else:
            result = fibonacci_manual_cache(n-1) + fibonacci_manual_cache(n-2)
        
        cache[n] = result
        return result
    
    # 性能测试
    test_values = [30, 35, 40]
    
    for n in test_values:
        print(f"\n计算 fibonacci({n}):")
        
        # 朴素递归（只测试较小的值）
        if n <= 35:
            start = time.time()
            result1 = fibonacci_naive(n)
            time1 = time.time() - start
            print(f"  朴素递归: {result1}, 耗时: {time1:.6f} 秒")
        
        # 缓存版本
        start = time.time()
        result2 = fibonacci_cached(n)
        time2 = time.time() - start
        print(f"  lru_cache: {result2}, 耗时: {time2:.6f} 秒")
        
        # 动态规划
        start = time.time()
        result3 = fibonacci_dp(n)
        time3 = time.time() - start
        print(f"  动态规划: {result3}, 耗时: {time3:.6f} 秒")
        
        # 优化版本
        start = time.time()
        result4 = fibonacci_optimized(n)
        time4 = time.time() - start
        print(f"  空间优化: {result4}, 耗时: {time4:.6f} 秒")
        
        # 手动缓存
        cache.clear()  # 清空缓存
        start = time.time()
        result5 = fibonacci_manual_cache(n)
        time5 = time.time() - start
        print(f"  手动缓存: {result5}, 耗时: {time5:.6f} 秒")
        
        # 显示缓存统计
        if hasattr(fibonacci_cached, 'cache_info'):
            print(f"  lru_cache统计: {fibonacci_cached.cache_info()}")


def expensive_computation_cache_demo():
    """昂贵计算的缓存演示"""
    print("\n=== 昂贵计算缓存演示 ===")
    
    def expensive_hash_computation(data):
        """模拟昂贵的哈希计算"""
        # 模拟复杂计算
        for _ in range(100000):
            data = hashlib.sha256(data.encode()).hexdigest()
        return data[:16]  # 返回前16个字符
    
    # 使用自定义缓存
    cache = LRUCache(capacity=10)
    
    def cached_expensive_computation(data):
        # 检查缓存
        result = cache.get(data)
        if result is not None:
            return result
        
        # 计算并缓存结果
        result = expensive_hash_computation(data)
        cache.put(data, result)
        return result
    
    # 测试数据
    test_data = ["hello", "world", "python", "cache", "optimization"]
    
    print("第一次计算（无缓存）:")
    start = time.time()
    results1 = []
    for data in test_data:
        result = cached_expensive_computation(data)
        results1.append(result)
        print(f"  {data} -> {result}")
    time1 = time.time() - start
    print(f"总耗时: {time1:.4f} 秒")
    print(cache.stats())
    
    print("\n第二次计算（使用缓存）:")
    start = time.time()
    results2 = []
    for data in test_data:
        result = cached_expensive_computation(data)
        results2.append(result)
    time2 = time.time() - start
    print(f"总耗时: {time2:.4f} 秒")
    print(cache.stats())
    print(f"性能提升: {time1/time2:.1f} 倍")
    print(f"结果一致: {results1 == results2}")


def algorithm_optimization_demo():
    """算法优化演示"""
    print("\n=== 算法优化演示 ===")
    
    # 问题：在数组中找到两个数的和等于目标值
    
    def two_sum_naive(nums, target):
        """朴素方法 O(n²)"""
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []
    
    def two_sum_optimized(nums, target):
        """优化方法 O(n) 使用哈希表"""
        num_map = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_map:
                return [num_map[complement], i]
            num_map[num] = i
        return []
    
    # 测试数据
    import random
    test_nums = [random.randint(1, 1000) for _ in range(10000)]
    target = test_nums[100] + test_nums[500]  # 确保有解
    
    print(f"在{len(test_nums):,}个数中找到和为{target}的两个数:")
    
    # 朴素方法
    start = time.time()
    result1 = two_sum_naive(test_nums, target)
    time1 = time.time() - start
    print(f"  朴素方法: 索引{result1}, 耗时: {time1:.6f} 秒")
    
    # 优化方法
    start = time.time()
    result2 = two_sum_optimized(test_nums, target)
    time2 = time.time() - start
    print(f"  优化方法: 索引{result2}, 耗时: {time2:.6f} 秒")
    
    print(f"  性能提升: {time1/time2:.0f} 倍")
    
    # 验证结果
    if result1 and result2:
        sum1 = test_nums[result1[0]] + test_nums[result1[1]]
        sum2 = test_nums[result2[0]] + test_nums[result2[1]]
        print(f"  结果验证: {sum1} == {sum2} == {target}")


def data_structure_optimization():
    """数据结构优化演示"""
    print("\n=== 数据结构优化演示 ===")
    
    # 问题：统计单词频率
    
    def count_words_dict(words):
        """使用普通字典"""
        word_count = {}
        for word in words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
        return word_count
    
    def count_words_defaultdict(words):
        """使用defaultdict"""
        word_count = defaultdict(int)
        for word in words:
            word_count[word] += 1
        return dict(word_count)
    
    def count_words_get(words):
        """使用dict.get方法"""
        word_count = {}
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1
        return word_count
    
    # 生成测试数据
    import random
    word_list = ['apple', 'banana', 'cherry', 'date', 'elderberry']
    test_words = [random.choice(word_list) for _ in range(100000)]
    
    print(f"统计{len(test_words):,}个单词的频率:")
    
    # 测试普通字典
    start = time.time()
    result1 = count_words_dict(test_words)
    time1 = time.time() - start
    print(f"  普通字典: 耗时 {time1:.6f} 秒")
    
    # 测试defaultdict
    start = time.time()
    result2 = count_words_defaultdict(test_words)
    time2 = time.time() - start
    print(f"  defaultdict: 耗时 {time2:.6f} 秒")
    
    # 测试get方法
    start = time.time()
    result3 = count_words_get(test_words)
    time3 = time.time() - start
    print(f"  dict.get: 耗时 {time3:.6f} 秒")
    
    print(f"  defaultdict比普通字典快: {time1/time2:.1f} 倍")
    print(f"  dict.get比普通字典快: {time1/time3:.1f} 倍")
    print(f"  结果一致: {result1 == result2 == result3}")
    
    # 显示部分结果
    print(f"  单词频率示例: {dict(list(result1.items())[:3])}")


def memoization_decorator_demo():
    """记忆化装饰器演示"""
    print("\n=== 记忆化装饰器演示 ===")
    
    def memoize(func):
        """自定义记忆化装饰器"""
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 创建缓存键
            key = str(args) + str(sorted(kwargs.items()))
            
            if key in cache:
                return cache[key]
            
            result = func(*args, **kwargs)
            cache[key] = result
            return result
        
        wrapper.cache = cache
        wrapper.cache_clear = lambda: cache.clear()
        return wrapper
    
    # 测试函数：计算组合数 C(n, k)
    @memoize
    def combination(n, k):
        """计算组合数"""
        if k == 0 or k == n:
            return 1
        if k > n:
            return 0
        return combination(n-1, k-1) + combination(n-1, k)
    
    # 不使用缓存的版本
    def combination_no_cache(n, k):
        """不使用缓存的组合数计算"""
        if k == 0 or k == n:
            return 1
        if k > n:
            return 0
        return combination_no_cache(n-1, k-1) + combination_no_cache(n-1, k)
    
    # 性能比较
    test_cases = [(20, 10), (25, 12), (30, 15)]
    
    for n, k in test_cases:
        print(f"\n计算 C({n}, {k}):")
        
        # 使用缓存
        combination.cache_clear()  # 清空缓存
        start = time.time()
        result1 = combination(n, k)
        time1 = time.time() - start
        print(f"  使用缓存: {result1}, 耗时: {time1:.6f} 秒")
        print(f"  缓存大小: {len(combination.cache)}")
        
        # 不使用缓存（只测试较小的值）
        if n <= 25:
            start = time.time()
            result2 = combination_no_cache(n, k)
            time2 = time.time() - start
            print(f"  不使用缓存: {result2}, 耗时: {time2:.6f} 秒")
            print(f"  性能提升: {time2/time1:.0f} 倍")


def main():
    """主函数"""
    print("Session24 示例3: 缓存和算法优化")
    print("=" * 50)
    
    try:
        # 斐波那契数列比较
        fibonacci_comparison()
        
        # 昂贵计算缓存
        expensive_computation_cache_demo()
        
        # 算法优化
        algorithm_optimization_demo()
        
        # 数据结构优化
        data_structure_optimization()
        
        # 记忆化装饰器
        memoization_decorator_demo()
        
        print("\n=== 缓存和算法优化总结 ===")
        print("1. 使用适当的缓存策略避免重复计算")
        print("2. 选择正确的算法降低时间复杂度")
        print("3. 使用合适的数据结构提高效率")
        print("4. 记忆化可以显著提升递归算法性能")
        print("5. 缓存大小和策略需要根据实际情况调整")
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()