#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session24: 性能优化 - 演示代码

本文件演示了Python性能优化的基本方法和实际应用。
包括性能分析、算法优化、内存优化等核心技术。

作者: Python教程团队
创建日期: 2024-01-20
最后修改: 2024-01-20
"""

import time
import sys
import cProfile
import pstats
from io import StringIO
from functools import lru_cache
from collections import deque, defaultdict
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing


def performance_timer(func):
    """性能计时装饰器"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"⏱️  {func.__name__} 执行时间: {end_time - start_time:.6f} 秒")
        return result
    return wrapper


def demo_basic_timing():
    """演示基础计时方法"""
    print("\n" + "="*50)
    print("📊 基础性能测试演示")
    print("="*50)
    
    # 测试不同的数据结构性能
    n = 100000
    
    # 列表 vs 集合查找性能
    data_list = list(range(n))
    data_set = set(range(n))
    target = n - 1
    
    # 列表查找
    start = time.time()
    result1 = target in data_list
    time1 = time.time() - start
    
    # 集合查找
    start = time.time()
    result2 = target in data_set
    time2 = time.time() - start
    
    print(f"🔍 查找元素 {target}:")
    print(f"   列表查找: {time1:.8f} 秒")
    print(f"   集合查找: {time2:.8f} 秒")
    
    # 避免除零错误
    if time2 > 0:
        print(f"   性能提升: {time1/time2:.0f} 倍")
    else:
        print(f"   集合查找速度极快，无法精确测量时间差")
    
    # 字符串拼接性能比较
    print(f"\n🔗 字符串拼接性能比较:")
    
    n = 10000
    
    # 方法1: + 操作符
    start = time.time()
    result1 = ""
    for i in range(n):
        result1 += str(i)
    time1 = time.time() - start
    
    # 方法2: join方法
    start = time.time()
    result2 = "".join(str(i) for i in range(n))
    time2 = time.time() - start
    
    print(f"   + 操作符: {time1:.6f} 秒")
    print(f"   join方法: {time2:.6f} 秒")
    print(f"   性能提升: {time1/time2:.0f} 倍")


def demo_algorithm_optimization():
    """演示算法优化"""
    print("\n" + "="*50)
    print("🚀 算法优化演示")
    print("="*50)
    
    # 排序算法比较
    import random
    
    def bubble_sort(arr):
        """冒泡排序 O(n²)"""
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr
    
    def quick_sort(arr):
        """快速排序 O(n log n)"""
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quick_sort(left) + middle + quick_sort(right)
    
    # 生成测试数据
    test_data = [random.randint(1, 1000) for _ in range(1000)]
    
    # 测试冒泡排序
    data1 = test_data.copy()
    start = time.time()
    sorted1 = bubble_sort(data1)
    time1 = time.time() - start
    
    # 测试快速排序
    data2 = test_data.copy()
    start = time.time()
    sorted2 = quick_sort(data2)
    time2 = time.time() - start
    
    # 测试内置排序
    data3 = test_data.copy()
    start = time.time()
    sorted3 = sorted(data3)
    time3 = time.time() - start
    
    print(f"📈 排序1000个随机数:")
    print(f"   冒泡排序: {time1:.6f} 秒")
    print(f"   快速排序: {time2:.6f} 秒")
    print(f"   内置排序: {time3:.6f} 秒")
    print(f"   快排比冒泡快: {time1/time2:.0f} 倍")
    print(f"   内置比冒泡快: {time1/time3:.0f} 倍")


def demo_memory_optimization():
    """演示内存优化"""
    print("\n" + "="*50)
    print("💾 内存优化演示")
    print("="*50)
    
    # 生成器 vs 列表
    n = 100000
    
    # 列表推导式
    list_comp = [x**2 for x in range(n)]
    list_memory = sys.getsizeof(list_comp)
    
    # 生成器表达式
    gen_exp = (x**2 for x in range(n))
    gen_memory = sys.getsizeof(gen_exp)
    
    print(f"🧮 计算{n:,}个平方数:")
    print(f"   列表内存: {list_memory:,} 字节")
    print(f"   生成器内存: {gen_memory:,} 字节")
    print(f"   内存节省: {list_memory//gen_memory:,} 倍")
    
    # __slots__ 优化演示
    class RegularClass:
        def __init__(self, x, y):
            self.x = x
            self.y = y
    
    class OptimizedClass:
        __slots__ = ['x', 'y']
        
        def __init__(self, x, y):
            self.x = x
            self.y = y
    
    # 创建实例并比较内存
    regular_obj = RegularClass(1, 2)
    optimized_obj = OptimizedClass(1, 2)
    
    regular_size = sys.getsizeof(regular_obj) + sys.getsizeof(regular_obj.__dict__)
    optimized_size = sys.getsizeof(optimized_obj)
    
    print(f"\n🏗️  类实例内存比较:")
    print(f"   普通类: {regular_size} 字节")
    print(f"   __slots__类: {optimized_size} 字节")
    print(f"   内存节省: {regular_size/optimized_size:.1f} 倍")


def demo_caching():
    """演示缓存优化"""
    print("\n" + "="*50)
    print("🗄️  缓存优化演示")
    print("="*50)
    
    # 不使用缓存的斐波那契
    def fibonacci_no_cache(n):
        if n <= 1:
            return n
        return fibonacci_no_cache(n-1) + fibonacci_no_cache(n-2)
    
    # 使用缓存的斐波那契
    @lru_cache(maxsize=None)
    def fibonacci_with_cache(n):
        if n <= 1:
            return n
        return fibonacci_with_cache(n-1) + fibonacci_with_cache(n-2)
    
    n = 30
    
    # 测试无缓存版本
    start = time.time()
    result1 = fibonacci_no_cache(n)
    time1 = time.time() - start
    
    # 测试有缓存版本
    start = time.time()
    result2 = fibonacci_with_cache(n)
    time2 = time.time() - start
    
    print(f"🔢 计算斐波那契数列第{n}项:")
    print(f"   无缓存: {time1:.6f} 秒")
    print(f"   有缓存: {time2:.6f} 秒")
    print(f"   性能提升: {time1/time2:.0f} 倍")
    print(f"   缓存信息: {fibonacci_with_cache.cache_info()}")


def cpu_intensive_task(n):
    """CPU密集型任务：计算素数"""
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True
    
    return sum(1 for i in range(2, n) if is_prime(i))


def demo_concurrency():
    """演示并发优化"""
    print("\n" + "="*50)
    print("⚡ 并发优化演示")
    print("="*50)
    
    # I/O密集型任务模拟
    def io_task(task_id):
        time.sleep(0.1)  # 模拟I/O等待
        return f"任务{task_id}完成"
    
    tasks = list(range(5))
    
    # 串行执行I/O任务
    start = time.time()
    serial_results = [io_task(i) for i in tasks]
    serial_time = time.time() - start
    
    # 并行执行I/O任务
    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        parallel_results = list(executor.map(io_task, tasks))
    parallel_time = time.time() - start
    
    print(f"🔄 I/O密集型任务 (5个任务):")
    print(f"   串行执行: {serial_time:.4f} 秒")
    print(f"   并行执行: {parallel_time:.4f} 秒")
    print(f"   性能提升: {serial_time/parallel_time:.1f} 倍")
    
    # CPU密集型任务
    cpu_tasks = [5000, 6000, 7000]
    
    # 串行执行CPU任务
    start = time.time()
    serial_cpu_results = [cpu_intensive_task(n) for n in cpu_tasks]
    serial_cpu_time = time.time() - start
    
    # 并行执行CPU任务（仅在支持多进程时）
    if __name__ == '__main__':
        start = time.time()
        with ProcessPoolExecutor() as executor:
            parallel_cpu_results = list(executor.map(cpu_intensive_task, cpu_tasks))
        parallel_cpu_time = time.time() - start
        
        print(f"\n🧮 CPU密集型任务 (计算素数):")
        print(f"   串行执行: {serial_cpu_time:.4f} 秒")
        print(f"   并行执行: {parallel_cpu_time:.4f} 秒")
        print(f"   性能提升: {serial_cpu_time/parallel_cpu_time:.1f} 倍")


def demo_profiling():
    """演示性能分析"""
    print("\n" + "="*50)
    print("🔍 性能分析演示")
    print("="*50)
    
    def complex_function():
        """复杂函数用于性能分析"""
        # 数学计算
        result = 0
        for i in range(50000):
            result += i ** 2
        
        # 字符串操作
        text = ""
        for i in range(1000):
            text += str(i)
        
        # 列表操作
        data = []
        for i in range(10000):
            data.append(i * 2)
        
        return result, len(text), len(data)
    
    # 使用cProfile进行性能分析
    print("📊 使用cProfile进行性能分析:")
    
    pr = cProfile.Profile()
    pr.enable()
    
    result = complex_function()
    
    pr.disable()
    
    # 输出性能统计
    s = StringIO()
    ps = pstats.Stats(pr, stream=s)
    ps.sort_stats('cumulative')
    ps.print_stats(5)  # 显示前5个最耗时的函数
    
    print(s.getvalue())
    print(f"函数执行结果: {result}")


def demo_data_structure_choice():
    """演示数据结构选择的重要性"""
    print("\n" + "="*50)
    print("📚 数据结构选择演示")
    print("="*50)
    
    n = 10000
    
    # 列表 vs 双端队列 - 头部插入
    print("🔄 头部插入操作比较:")
    
    # 列表头部插入
    data_list = []
    start = time.time()
    for i in range(n):
        data_list.insert(0, i)
    list_time = time.time() - start
    
    # 双端队列头部插入
    data_deque = deque()
    start = time.time()
    for i in range(n):
        data_deque.appendleft(i)
    deque_time = time.time() - start
    
    print(f"   列表insert(0): {list_time:.6f} 秒")
    print(f"   双端队列appendleft: {deque_time:.6f} 秒")
    print(f"   性能提升: {list_time/deque_time:.0f} 倍")
    
    # 字典 vs defaultdict
    print(f"\n📖 字典操作比较:")
    
    # 普通字典
    normal_dict = {}
    start = time.time()
    for i in range(n):
        key = i % 100
        if key in normal_dict:
            normal_dict[key] += 1
        else:
            normal_dict[key] = 1
    dict_time = time.time() - start
    
    # defaultdict
    default_dict = defaultdict(int)
    start = time.time()
    for i in range(n):
        key = i % 100
        default_dict[key] += 1
    defaultdict_time = time.time() - start
    
    print(f"   普通字典: {dict_time:.6f} 秒")
    print(f"   defaultdict: {defaultdict_time:.6f} 秒")
    print(f"   性能提升: {dict_time/defaultdict_time:.1f} 倍")


def main():
    """主函数：演示程序的入口点"""
    print("Session24: 性能优化演示")
    print("=" * 60)
    print("🎯 本演示将展示Python性能优化的各种技术")
    print("包括算法优化、内存优化、缓存、并发等")
    
    try:
        # 基础性能测试
        demo_basic_timing()
        
        # 算法优化
        demo_algorithm_optimization()
        
        # 内存优化
        demo_memory_optimization()
        
        # 缓存优化
        demo_caching()
        
        # 数据结构选择
        demo_data_structure_choice()
        
        # 性能分析
        demo_profiling()
        
        # 并发优化
        demo_concurrency()
        
        print("\n" + "="*60)
        print("🎉 性能优化演示完成！")
        print("💡 关键要点:")
        print("   1. 选择合适的算法和数据结构")
        print("   2. 使用缓存避免重复计算")
        print("   3. 优化内存使用")
        print("   4. 合理使用并发")
        print("   5. 基于测量进行优化")
        print("="*60)
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()