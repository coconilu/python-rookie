#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session29 练习3: 性能测试和调试技术

练习目标:
1. 学习性能测试方法
2. 掌握调试技术
3. 使用性能分析工具
4. 优化代码性能
5. 内存泄漏检测

练习说明:
请为下面的代码实现性能测试和调试功能：
- 基准测试
- 压力测试
- 内存分析
- 调试技术
- 性能优化

作者: Python教程团队
"""

import time
import cProfile
import pstats
import tracemalloc
import threading
import multiprocessing
import asyncio
import random
import sys
import gc
from typing import List, Dict, Callable, Any
from functools import wraps
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import unittest


# 性能测试装饰器
def benchmark(func):
    """基准测试装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"{func.__name__} 执行时间: {execution_time:.6f} 秒")
        return result
    return wrapper


def memory_profiler(func):
    """内存分析装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"{func.__name__} 内存使用: 当前 {current / 1024 / 1024:.2f} MB, 峰值 {peak / 1024 / 1024:.2f} MB")
        return result
    return wrapper


class PerformanceTester:
    """性能测试工具类"""
    
    def __init__(self):
        self.results = []
    
    def time_function(self, func: Callable, *args, iterations: int = 1000, **kwargs) -> Dict:
        """测试函数执行时间"""
        times = []
        
        for _ in range(iterations):
            start = time.perf_counter()
            func(*args, **kwargs)
            end = time.perf_counter()
            times.append(end - start)
        
        result = {
            'function': func.__name__,
            'iterations': iterations,
            'total_time': sum(times),
            'avg_time': sum(times) / len(times),
            'min_time': min(times),
            'max_time': max(times)
        }
        
        self.results.append(result)
        return result
    
    def compare_functions(self, functions: List[Callable], *args, iterations: int = 1000, **kwargs):
        """比较多个函数的性能"""
        print(f"\n性能比较 (迭代次数: {iterations})")
        print("=" * 60)
        
        results = []
        for func in functions:
            result = self.time_function(func, *args, iterations=iterations, **kwargs)
            results.append(result)
            print(f"{func.__name__:20} | 平均: {result['avg_time']:.6f}s | 总计: {result['total_time']:.6f}s")
        
        # 找出最快的函数
        fastest = min(results, key=lambda x: x['avg_time'])
        print(f"\n最快函数: {fastest['function']}")
        
        return results
    
    def stress_test(self, func: Callable, max_load: int = 1000, step: int = 100):
        """压力测试"""
        print(f"\n压力测试: {func.__name__}")
        print("=" * 40)
        
        for load in range(step, max_load + 1, step):
            start_time = time.perf_counter()
            
            try:
                # 创建大量数据进行测试
                data = list(range(load))
                result = func(data)
                
                end_time = time.perf_counter()
                execution_time = end_time - start_time
                
                print(f"负载 {load:4d}: {execution_time:.6f}s")
                
            except Exception as e:
                print(f"负载 {load:4d}: 失败 - {e}")
                break
    
    def memory_test(self, func: Callable, *args, **kwargs):
        """内存测试"""
        tracemalloc.start()
        
        # 执行前的内存状态
        gc.collect()
        before_memory = tracemalloc.get_traced_memory()[0]
        
        # 执行函数
        result = func(*args, **kwargs)
        
        # 执行后的内存状态
        after_memory = tracemalloc.get_traced_memory()[0]
        peak_memory = tracemalloc.get_traced_memory()[1]
        
        tracemalloc.stop()
        
        memory_used = after_memory - before_memory
        
        print(f"\n内存测试: {func.__name__}")
        print(f"使用内存: {memory_used / 1024 / 1024:.2f} MB")
        print(f"峰值内存: {peak_memory / 1024 / 1024:.2f} MB")
        
        return {
            'memory_used': memory_used,
            'peak_memory': peak_memory,
            'result': result
        }


# 需要测试和优化的算法类
class AlgorithmBenchmark:
    """算法基准测试类 - 需要进行性能测试和优化"""
    
    def bubble_sort(self, arr: List[int]) -> List[int]:
        """冒泡排序 - 性能较差的算法"""
        arr = arr.copy()
        n = len(arr)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        
        return arr
    
    def quick_sort(self, arr: List[int]) -> List[int]:
        """快速排序 - 性能较好的算法"""
        if len(arr) <= 1:
            return arr
        
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        
        return self.quick_sort(left) + middle + self.quick_sort(right)
    
    def python_sort(self, arr: List[int]) -> List[int]:
        """Python内置排序"""
        return sorted(arr)
    
    def linear_search(self, arr: List[int], target: int) -> int:
        """线性搜索"""
        for i, value in enumerate(arr):
            if value == target:
                return i
        return -1
    
    def binary_search(self, arr: List[int], target: int) -> int:
        """二分搜索 - 需要排序数组"""
        left, right = 0, len(arr) - 1
        
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return -1
    
    def fibonacci_recursive(self, n: int) -> int:
        """递归斐波那契 - 性能很差"""
        if n <= 1:
            return n
        return self.fibonacci_recursive(n - 1) + self.fibonacci_recursive(n - 2)
    
    def fibonacci_iterative(self, n: int) -> int:
        """迭代斐波那契 - 性能较好"""
        if n <= 1:
            return n
        
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        
        return b
    
    def fibonacci_memoized(self, n: int, memo: Dict[int, int] = None) -> int:
        """记忆化斐波那契 - 性能最好"""
        if memo is None:
            memo = {}
        
        if n in memo:
            return memo[n]
        
        if n <= 1:
            return n
        
        memo[n] = self.fibonacci_memoized(n - 1, memo) + self.fibonacci_memoized(n - 2, memo)
        return memo[n]


class DataProcessor:
    """数据处理类 - 需要进行并发性能测试"""
    
    def process_data_sequential(self, data: List[int]) -> List[int]:
        """顺序处理数据"""
        result = []
        for item in data:
            # 模拟复杂计算
            processed = self._complex_calculation(item)
            result.append(processed)
        return result
    
    def process_data_threading(self, data: List[int], max_workers: int = 4) -> List[int]:
        """多线程处理数据"""
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self._complex_calculation, data))
        return results
    
    def process_data_multiprocessing(self, data: List[int], max_workers: int = 4) -> List[int]:
        """多进程处理数据"""
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self._complex_calculation, data))
        return results
    
    async def process_data_async(self, data: List[int]) -> List[int]:
        """异步处理数据"""
        tasks = [self._async_calculation(item) for item in data]
        results = await asyncio.gather(*tasks)
        return results
    
    def _complex_calculation(self, x: int) -> int:
        """模拟复杂计算"""
        # 模拟CPU密集型任务
        result = 0
        for i in range(1000):
            result += x * i
        return result
    
    async def _async_calculation(self, x: int) -> int:
        """异步复杂计算"""
        # 模拟IO密集型任务
        await asyncio.sleep(0.001)  # 模拟IO等待
        return self._complex_calculation(x)


class MemoryLeakDemo:
    """内存泄漏演示类 - 需要进行内存分析"""
    
    def __init__(self):
        self.data_store = []
        self.circular_refs = []
    
    def create_memory_leak(self, size: int = 1000):
        """创建内存泄漏"""
        # 不断添加数据但不清理
        for i in range(size):
            large_data = [random.random() for _ in range(1000)]
            self.data_store.append(large_data)
    
    def create_circular_reference(self, count: int = 100):
        """创建循环引用"""
        for i in range(count):
            obj1 = {'id': i, 'ref': None}
            obj2 = {'id': i + 1000, 'ref': obj1}
            obj1['ref'] = obj2
            self.circular_refs.append(obj1)
    
    def cleanup_memory(self):
        """清理内存"""
        self.data_store.clear()
        self.circular_refs.clear()
        gc.collect()


# TODO: 请完成以下测试类
class TestPerformanceAndDebugging(unittest.TestCase):
    """性能测试和调试练习
    
    请完成以下测试方法：
    1. test_sorting_algorithms_performance - 比较排序算法性能
    2. test_search_algorithms_performance - 比较搜索算法性能
    3. test_fibonacci_algorithms_performance - 比较斐波那契算法性能
    4. test_concurrent_processing_performance - 比较并发处理性能
    5. test_memory_usage_analysis - 内存使用分析
    6. test_stress_testing - 压力测试
    7. test_memory_leak_detection - 内存泄漏检测
    8. test_profiling_analysis - 性能分析
    """
    
    def setUp(self):
        """设置测试环境"""
        self.performance_tester = PerformanceTester()
        self.algorithm_benchmark = AlgorithmBenchmark()
        self.data_processor = DataProcessor()
        self.memory_demo = MemoryLeakDemo()
        
        # 测试数据
        self.small_data = list(range(100))
        random.shuffle(self.small_data)
        
        self.medium_data = list(range(1000))
        random.shuffle(self.medium_data)
        
        self.large_data = list(range(10000))
        random.shuffle(self.large_data)
    
    def test_sorting_algorithms_performance(self):
        """比较排序算法性能"""
        print("\n=== 排序算法性能测试 ===")
        
        # TODO: 使用PerformanceTester比较不同排序算法的性能
        # 提示：
        # 1. 使用self.performance_tester.compare_functions()
        # 2. 比较bubble_sort, quick_sort, python_sort
        # 3. 使用不同大小的数据集测试
        # 4. 分析结果并得出结论
        
        # 示例代码结构：
        # sorting_functions = [
        #     self.algorithm_benchmark.bubble_sort,
        #     self.algorithm_benchmark.quick_sort,
        #     self.algorithm_benchmark.python_sort
        # ]
        # 
        # print("小数据集测试:")
        # results_small = self.performance_tester.compare_functions(
        #     sorting_functions, self.small_data, iterations=10
        # )
        
        pass
    
    def test_search_algorithms_performance(self):
        """比较搜索算法性能"""
        print("\n=== 搜索算法性能测试 ===")
        
        # TODO: 比较线性搜索和二分搜索的性能
        # 注意：二分搜索需要排序数组
        # 提示：
        # 1. 准备排序和未排序的数据
        # 2. 选择随机目标值
        # 3. 比较两种搜索算法的性能
        # 4. 分析在不同数据大小下的性能差异
        
        pass
    
    def test_fibonacci_algorithms_performance(self):
        """比较斐波那契算法性能"""
        print("\n=== 斐波那契算法性能测试 ===")
        
        # TODO: 比较三种斐波那契实现的性能
        # 提示：
        # 1. 测试不同的n值（如10, 20, 30）
        # 2. 注意递归版本在大n值时会很慢
        # 3. 使用@benchmark装饰器
        # 4. 分析时间复杂度的差异
        
        pass
    
    def test_concurrent_processing_performance(self):
        """比较并发处理性能"""
        print("\n=== 并发处理性能测试 ===")
        
        # TODO: 比较顺序、多线程、多进程处理的性能
        # 提示：
        # 1. 使用中等大小的数据集
        # 2. 比较sequential, threading, multiprocessing
        # 3. 测试不同的worker数量
        # 4. 分析CPU密集型任务的并发效果
        
        pass
    
    def test_memory_usage_analysis(self):
        """内存使用分析"""
        print("\n=== 内存使用分析 ===")
        
        # TODO: 分析不同算法的内存使用情况
        # 提示：
        # 1. 使用self.performance_tester.memory_test()
        # 2. 测试排序算法的内存使用
        # 3. 比较不同数据大小的内存消耗
        # 4. 使用@memory_profiler装饰器
        
        pass
    
    def test_stress_testing(self):
        """压力测试"""
        print("\n=== 压力测试 ===")
        
        # TODO: 对算法进行压力测试
        # 提示：
        # 1. 使用self.performance_tester.stress_test()
        # 2. 测试排序算法在大数据量下的表现
        # 3. 找出算法的性能瓶颈
        # 4. 观察内存使用的变化
        
        pass
    
    def test_memory_leak_detection(self):
        """内存泄漏检测"""
        print("\n=== 内存泄漏检测 ===")
        
        # TODO: 检测和修复内存泄漏
        # 提示：
        # 1. 使用tracemalloc监控内存
        # 2. 测试MemoryLeakDemo的方法
        # 3. 比较cleanup前后的内存使用
        # 4. 验证垃圾回收的效果
        
        pass
    
    def test_profiling_analysis(self):
        """性能分析"""
        print("\n=== 性能分析 ===")
        
        # TODO: 使用cProfile进行详细的性能分析
        # 提示：
        # 1. 使用cProfile.run()分析函数
        # 2. 生成性能报告
        # 3. 找出性能热点
        # 4. 提出优化建议
        
        # 示例代码结构：
        # profiler = cProfile.Profile()
        # profiler.enable()
        # 
        # # 执行要分析的代码
        # result = self.algorithm_benchmark.bubble_sort(self.medium_data)
        # 
        # profiler.disable()
        # 
        # # 生成报告
        # stats = pstats.Stats(profiler)
        # stats.sort_stats('cumulative')
        # stats.print_stats(10)  # 显示前10个最耗时的函数
        
        pass
    
    def test_async_performance(self):
        """异步性能测试"""
        print("\n=== 异步性能测试 ===")
        
        # TODO: 测试异步处理的性能
        # 提示：
        # 1. 比较同步和异步处理的性能
        # 2. 使用asyncio.run()运行异步函数
        # 3. 分析IO密集型任务的异步优势
        
        pass


# 调试技术演示
class DebuggingDemo:
    """调试技术演示类"""
    
    def __init__(self):
        self.data = []
    
    def buggy_function(self, numbers: List[int]) -> float:
        """包含bug的函数 - 需要调试"""
        total = 0
        count = 0
        
        for num in numbers:
            if num > 0:  # Bug: 应该检查num != 0
                total += num
                count += 1
        
        # Bug: 可能除零错误
        average = total / count
        return average
    
    def debug_with_print(self, numbers: List[int]) -> float:
        """使用print调试"""
        print(f"输入数据: {numbers}")
        
        total = 0
        count = 0
        
        for i, num in enumerate(numbers):
            print(f"处理第{i}个数字: {num}")
            if num > 0:
                total += num
                count += 1
                print(f"  累计总和: {total}, 计数: {count}")
        
        print(f"最终总和: {total}, 计数: {count}")
        
        if count == 0:
            print("警告: 没有正数，无法计算平均值")
            return 0.0
        
        average = total / count
        print(f"平均值: {average}")
        return average
    
    def debug_with_logging(self, numbers: List[int]) -> float:
        """使用logging调试"""
        import logging
        
        # 配置日志
        logging.basicConfig(level=logging.DEBUG, 
                          format='%(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)
        
        logger.debug(f"开始处理数据: {numbers}")
        
        total = 0
        count = 0
        
        for num in numbers:
            logger.debug(f"处理数字: {num}")
            if num > 0:
                total += num
                count += 1
                logger.debug(f"累计: total={total}, count={count}")
        
        if count == 0:
            logger.warning("没有正数，返回0")
            return 0.0
        
        average = total / count
        logger.info(f"计算完成，平均值: {average}")
        return average
    
    def debug_with_assertions(self, numbers: List[int]) -> float:
        """使用断言调试"""
        assert isinstance(numbers, list), "输入必须是列表"
        assert len(numbers) > 0, "列表不能为空"
        
        total = 0
        count = 0
        
        for num in numbers:
            assert isinstance(num, (int, float)), f"数字类型错误: {type(num)}"
            
            if num > 0:
                total += num
                count += 1
        
        assert count > 0, "没有找到正数"
        
        average = total / count
        assert average > 0, "平均值应该大于0"
        
        return average


def run_performance_tests():
    """运行性能测试"""
    print("运行性能测试和调试练习...")
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestPerformanceAndDebugging))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


def demonstrate_debugging():
    """演示调试技术"""
    print("\n=== 调试技术演示 ===")
    
    demo = DebuggingDemo()
    test_data = [1, -2, 3, 0, 5, -1]
    
    print("\n1. 原始buggy函数:")
    try:
        result = demo.buggy_function(test_data)
        print(f"结果: {result}")
    except Exception as e:
        print(f"错误: {e}")
    
    print("\n2. 使用print调试:")
    result = demo.debug_with_print(test_data)
    
    print("\n3. 使用logging调试:")
    result = demo.debug_with_logging(test_data)
    
    print("\n4. 使用断言调试:")
    try:
        result = demo.debug_with_assertions(test_data)
        print(f"结果: {result}")
    except AssertionError as e:
        print(f"断言错误: {e}")


if __name__ == "__main__":
    print("Session29 练习3: 性能测试和调试技术")
    print("=" * 50)
    
    print("\n练习说明:")
    print("1. 学习各种性能测试方法")
    print("2. 掌握调试技术和工具")
    print("3. 进行内存分析和优化")
    print("4. 实践压力测试和基准测试")
    
    # 演示调试技术
    demonstrate_debugging()
    
    print("\n开始性能测试...")
    success = run_performance_tests()
    
    if success:
        print("\n🎉 恭喜！所有性能测试都完成了！")
    else:
        print("\n❌ 还有测试未完成，请检查你的实现")
    
    print("\n学习要点:")
    print("- 使用基准测试比较算法性能")
    print("- 进行内存分析和泄漏检测")
    print("- 掌握各种调试技术")
    print("- 使用性能分析工具优化代码")
    print("- 理解并发和异步的性能特点")