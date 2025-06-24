#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session24 示例1：性能计时比较

本示例演示如何使用不同的方法来测量和比较代码性能。
包括time模块、timeit模块和自定义计时器的使用。

作者: Python教程团队
创建日期: 2024-01-20
"""

import time
import timeit
from functools import wraps


def timer_decorator(func):
    """计时装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"{func.__name__} 执行时间: {end_time - start_time:.6f} 秒")
        return result
    return wrapper


class PerformanceTimer:
    """性能计时器类"""
    
    def __init__(self, name="操作"):
        self.name = name
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.perf_counter()
        print(f"{self.name} 执行时间: {end_time - self.start_time:.6f} 秒")


def compare_list_operations():
    """比较不同列表操作的性能"""
    print("\n=== 列表操作性能比较 ===")
    
    n = 100000
    
    # 方法1：使用append
    @timer_decorator
    def method1_append():
        result = []
        for i in range(n):
            result.append(i * 2)
        return result
    
    # 方法2：使用列表推导式
    @timer_decorator
    def method2_comprehension():
        return [i * 2 for i in range(n)]
    
    # 方法3：使用map
    @timer_decorator
    def method3_map():
        return list(map(lambda x: x * 2, range(n)))
    
    # 执行比较
    result1 = method1_append()
    result2 = method2_comprehension()
    result3 = method3_map()
    
    print(f"所有方法结果长度相同: {len(result1) == len(result2) == len(result3)}")


def compare_string_operations():
    """比较字符串操作性能"""
    print("\n=== 字符串操作性能比较 ===")
    
    words = ["hello", "world", "python", "performance"] * 2500
    
    # 方法1：使用 + 操作符
    with PerformanceTimer("字符串 + 操作"):
        result1 = ""
        for word in words:
            result1 += word + " "
    
    # 方法2：使用join
    with PerformanceTimer("join操作"):
        result2 = " ".join(words) + " "
    
    # 方法3：使用f-string在循环中
    with PerformanceTimer("f-string循环"):
        result3 = ""
        for word in words:
            result3 += f"{word} "
    
    print(f"所有方法结果长度相同: {len(result1) == len(result2) == len(result3)}")


def compare_lookup_operations():
    """比较查找操作性能"""
    print("\n=== 查找操作性能比较 ===")
    
    n = 50000
    data_list = list(range(n))
    data_set = set(range(n))
    data_dict = {i: i for i in range(n)}
    
    target = n - 1  # 最坏情况：查找最后一个元素
    
    # 列表查找
    start = time.perf_counter()
    result1 = target in data_list
    time1 = time.perf_counter() - start
    
    # 集合查找
    start = time.perf_counter()
    result2 = target in data_set
    time2 = time.perf_counter() - start
    
    # 字典键查找
    start = time.perf_counter()
    result3 = target in data_dict
    time3 = time.perf_counter() - start
    
    print(f"列表查找: {time1:.8f} 秒")
    print(f"集合查找: {time2:.8f} 秒")
    print(f"字典查找: {time3:.8f} 秒")
    print(f"集合比列表快: {time1/time2:.0f} 倍")
    print(f"字典比列表快: {time1/time3:.0f} 倍")


def timeit_comparison():
    """使用timeit进行精确比较"""
    print("\n=== 使用timeit进行精确比较 ===")
    
    # 比较不同的平方计算方法
    setup_code = "x = 123"
    
    # 方法1：使用 **
    time1 = timeit.timeit("x ** 2", setup=setup_code, number=1000000)
    
    # 方法2：使用 *
    time2 = timeit.timeit("x * x", setup=setup_code, number=1000000)
    
    # 方法3：使用pow函数
    time3 = timeit.timeit("pow(x, 2)", setup=setup_code, number=1000000)
    
    print(f"x ** 2: {time1:.6f} 秒")
    print(f"x * x: {time2:.6f} 秒")
    print(f"pow(x, 2): {time3:.6f} 秒")
    
    fastest = min(time1, time2, time3)
    print(f"\n最快的方法比最慢的快: {max(time1, time2, time3)/fastest:.2f} 倍")


def compare_sorting_algorithms():
    """比较排序算法性能"""
    print("\n=== 排序算法性能比较 ===")
    
    import random
    
    # 生成测试数据
    test_data = [random.randint(1, 1000) for _ in range(5000)]
    
    def bubble_sort(arr):
        """冒泡排序"""
        arr = arr.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr
    
    def selection_sort(arr):
        """选择排序"""
        arr = arr.copy()
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr
    
    # 测试各种排序方法
    algorithms = [
        ("冒泡排序", bubble_sort),
        ("选择排序", selection_sort),
        ("内置sorted", lambda x: sorted(x)),
        ("列表sort", lambda x: x.copy().sort() or x.copy())
    ]
    
    results = {}
    
    for name, func in algorithms:
        start = time.perf_counter()
        sorted_data = func(test_data)
        end = time.perf_counter()
        results[name] = end - start
        print(f"{name}: {end - start:.6f} 秒")
    
    # 找出最快的算法
    fastest_name = min(results, key=results.get)
    fastest_time = results[fastest_name]
    
    print(f"\n最快算法: {fastest_name}")
    for name, time_taken in results.items():
        if name != fastest_name:
            print(f"{fastest_name} 比 {name} 快: {time_taken/fastest_time:.1f} 倍")


def main():
    """主函数"""
    print("Session24 示例1: 性能计时比较")
    print("=" * 50)
    
    # 运行各种比较
    compare_list_operations()
    compare_string_operations()
    compare_lookup_operations()
    timeit_comparison()
    compare_sorting_algorithms()
    
    print("\n=== 总结 ===")
    print("1. 不同的实现方法性能差异可能很大")
    print("2. 选择合适的数据结构很重要")
    print("3. 内置函数通常比自定义实现更快")
    print("4. 使用timeit进行精确的性能测量")
    print("5. 性能测试要在相同条件下进行")


if __name__ == "__main__":
    main()