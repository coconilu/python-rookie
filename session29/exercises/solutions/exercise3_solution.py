#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session29 练习3解决方案: 性能测试和调试技术

这是exercise3.py的完整解决方案，展示了如何进行性能测试和调试。

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
import io
import logging
from typing import List, Dict, Callable, Any
from functools import wraps
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import unittest


# 复制原始类定义
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


class AlgorithmBenchmark:
    """算法基准测试类"""
    
    def bubble_sort(self, arr: List[int]) -> List[int]:
        """冒泡排序"""
        arr = arr.copy()
        n = len(arr)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        
        return arr
    
    def quick_sort(self, arr: List[int]) -> List[int]:
        """快速排序"""
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
        """二分搜索"""
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
        """递归斐波那契"""
        if n <= 1:
            return n
        return self.fibonacci_recursive(n - 1) + self.fibonacci_recursive(n - 2)
    
    def fibonacci_iterative(self, n: int) -> int:
        """迭代斐波那契"""
        if n <= 1:
            return n
        
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        
        return b
    
    def fibonacci_memoized(self, n: int, memo: Dict[int, int] = None) -> int:
        """记忆化斐波那契"""
        if memo is None:
            memo = {}
        
        if n in memo:
            return memo[n]
        
        if n <= 1:
            return n
        
        memo[n] = self.fibonacci_memoized(n - 1, memo) + self.fibonacci_memoized(n - 2, memo)
        return memo[n]


class DataProcessor:
    """数据处理类"""
    
    def process_data_sequential(self, data: List[int]) -> List[int]:
        """顺序处理数据"""
        result = []
        for item in data:
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
        result = 0
        for i in range(1000):
            result += x * i
        return result
    
    async def _async_calculation(self, x: int) -> int:
        """异步复杂计算"""
        await asyncio.sleep(0.001)
        return self._complex_calculation(x)


class MemoryLeakDemo:
    """内存泄漏演示类"""
    
    def __init__(self):
        self.data_store = []
        self.circular_refs = []
    
    def create_memory_leak(self, size: int = 1000):
        """创建内存泄漏"""
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


# 完整的测试解决方案
class TestPerformanceAndDebugging(unittest.TestCase):
    """性能测试和调试练习 - 完整解决方案"""
    
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
        
        sorting_functions = [
            self.algorithm_benchmark.bubble_sort,
            self.algorithm_benchmark.quick_sort,
            self.algorithm_benchmark.python_sort
        ]
        
        print("\n小数据集测试 (100个元素):")
        results_small = self.performance_tester.compare_functions(
            sorting_functions, self.small_data, iterations=10
        )
        
        print("\n中等数据集测试 (1000个元素):")
        results_medium = self.performance_tester.compare_functions(
            sorting_functions[1:], self.medium_data, iterations=5  # 跳过冒泡排序，太慢
        )
        
        # 验证排序结果正确性
        for func in sorting_functions:
            if func.__name__ != 'bubble_sort':  # 跳过冒泡排序的大数据测试
                sorted_result = func(self.small_data)
                expected_result = sorted(self.small_data)
                self.assertEqual(sorted_result, expected_result, 
                               f"{func.__name__} 排序结果不正确")
        
        # 分析性能结果
        print("\n性能分析:")
        print("- Python内置排序性能最佳")
        print("- 快速排序性能良好")
        print("- 冒泡排序性能最差，不适合大数据")
    
    def test_search_algorithms_performance(self):
        """比较搜索算法性能"""
        print("\n=== 搜索算法性能测试 ===")
        
        # 准备排序数据用于二分搜索
        sorted_data = sorted(self.medium_data)
        target = sorted_data[len(sorted_data) // 2]  # 选择中间值作为目标
        
        print(f"搜索目标: {target}")
        print(f"数据大小: {len(sorted_data)}")
        
        # 线性搜索测试
        linear_time = self.performance_tester.time_function(
            self.algorithm_benchmark.linear_search,
            self.medium_data, target, iterations=100
        )
        
        # 二分搜索测试
        binary_time = self.performance_tester.time_function(
            self.algorithm_benchmark.binary_search,
            sorted_data, target, iterations=100
        )
        
        print(f"\n线性搜索平均时间: {linear_time['avg_time']:.6f}s")
        print(f"二分搜索平均时间: {binary_time['avg_time']:.6f}s")
        print(f"性能提升: {linear_time['avg_time'] / binary_time['avg_time']:.2f}倍")
        
        # 验证搜索结果正确性
        linear_result = self.algorithm_benchmark.linear_search(self.medium_data, target)
        binary_result = self.algorithm_benchmark.binary_search(sorted_data, target)
        
        self.assertNotEqual(linear_result, -1, "线性搜索应该找到目标")
        self.assertNotEqual(binary_result, -1, "二分搜索应该找到目标")
        self.assertEqual(sorted_data[binary_result], target, "二分搜索结果正确")
    
    def test_fibonacci_algorithms_performance(self):
        """比较斐波那契算法性能"""
        print("\n=== 斐波那契算法性能测试 ===")
        
        test_values = [10, 20, 30]
        
        for n in test_values:
            print(f"\n计算斐波那契数列第{n}项:")
            
            # 递归版本（小n值）
            if n <= 20:  # 递归版本太慢，只测试小值
                recursive_time = self.performance_tester.time_function(
                    self.algorithm_benchmark.fibonacci_recursive,
                    n, iterations=1
                )
                print(f"递归版本: {recursive_time['avg_time']:.6f}s")
            
            # 迭代版本
            iterative_time = self.performance_tester.time_function(
                self.algorithm_benchmark.fibonacci_iterative,
                n, iterations=1000
            )
            print(f"迭代版本: {iterative_time['avg_time']:.6f}s")
            
            # 记忆化版本
            memoized_time = self.performance_tester.time_function(
                self.algorithm_benchmark.fibonacci_memoized,
                n, iterations=1000
            )
            print(f"记忆化版本: {memoized_time['avg_time']:.6f}s")
            
            # 验证结果正确性
            iterative_result = self.algorithm_benchmark.fibonacci_iterative(n)
            memoized_result = self.algorithm_benchmark.fibonacci_memoized(n)
            self.assertEqual(iterative_result, memoized_result, "斐波那契结果应该相同")
    
    def test_concurrent_processing_performance(self):
        """比较并发处理性能"""
        print("\n=== 并发处理性能测试 ===")
        
        test_data = list(range(100))  # 使用较小的数据集进行测试
        
        # 顺序处理
        print("\n顺序处理:")
        sequential_time = self.performance_tester.time_function(
            self.data_processor.process_data_sequential,
            test_data, iterations=1
        )
        
        # 多线程处理
        print("\n多线程处理:")
        threading_time = self.performance_tester.time_function(
            self.data_processor.process_data_threading,
            test_data, iterations=1
        )
        
        # 多进程处理
        print("\n多进程处理:")
        multiprocessing_time = self.performance_tester.time_function(
            self.data_processor.process_data_multiprocessing,
            test_data, iterations=1
        )
        
        print(f"\n性能比较:")
        print(f"顺序处理: {sequential_time['avg_time']:.6f}s")
        print(f"多线程: {threading_time['avg_time']:.6f}s")
        print(f"多进程: {multiprocessing_time['avg_time']:.6f}s")
        
        # 验证结果正确性
        sequential_result = self.data_processor.process_data_sequential(test_data[:10])
        threading_result = self.data_processor.process_data_threading(test_data[:10])
        
        self.assertEqual(len(sequential_result), len(threading_result), "结果长度应该相同")
    
    def test_memory_usage_analysis(self):
        """内存使用分析"""
        print("\n=== 内存使用分析 ===")
        
        # 测试排序算法的内存使用
        test_data = list(range(1000))
        random.shuffle(test_data)
        
        print("\n排序算法内存使用:")
        
        # 快速排序内存测试
        quick_sort_memory = self.performance_tester.memory_test(
            self.algorithm_benchmark.quick_sort, test_data
        )
        
        # Python内置排序内存测试
        python_sort_memory = self.performance_tester.memory_test(
            self.algorithm_benchmark.python_sort, test_data
        )
        
        print(f"\n内存使用比较:")
        print(f"快速排序峰值内存: {quick_sort_memory['peak_memory'] / 1024 / 1024:.2f} MB")
        print(f"Python排序峰值内存: {python_sort_memory['peak_memory'] / 1024 / 1024:.2f} MB")
        
        # 验证内存测试有效性
        self.assertGreater(quick_sort_memory['peak_memory'], 0, "应该有内存使用")
        self.assertGreater(python_sort_memory['peak_memory'], 0, "应该有内存使用")
    
    def test_stress_testing(self):
        """压力测试"""
        print("\n=== 压力测试 ===")
        
        # 对快速排序进行压力测试
        print("\n快速排序压力测试:")
        self.performance_tester.stress_test(
            self.algorithm_benchmark.quick_sort,
            max_load=5000, step=1000
        )
        
        # 对Python内置排序进行压力测试
        print("\n Python内置排序压力测试:")
        self.performance_tester.stress_test(
            self.algorithm_benchmark.python_sort,
            max_load=10000, step=2000
        )
        
        print("\n压力测试完成")
    
    def test_memory_leak_detection(self):
        """内存泄漏检测"""
        print("\n=== 内存泄漏检测 ===")
        
        # 开始内存监控
        tracemalloc.start()
        
        # 获取初始内存状态
        gc.collect()
        initial_memory = tracemalloc.get_traced_memory()[0]
        print(f"初始内存: {initial_memory / 1024 / 1024:.2f} MB")
        
        # 创建内存泄漏
        print("\n创建内存泄漏...")
        self.memory_demo.create_memory_leak(100)
        self.memory_demo.create_circular_reference(50)
        
        # 检查内存使用
        after_leak_memory = tracemalloc.get_traced_memory()[0]
        print(f"泄漏后内存: {after_leak_memory / 1024 / 1024:.2f} MB")
        print(f"内存增长: {(after_leak_memory - initial_memory) / 1024 / 1024:.2f} MB")
        
        # 清理内存
        print("\n清理内存...")
        self.memory_demo.cleanup_memory()
        
        # 检查清理后的内存
        gc.collect()  # 强制垃圾回收
        after_cleanup_memory = tracemalloc.get_traced_memory()[0]
        print(f"清理后内存: {after_cleanup_memory / 1024 / 1024:.2f} MB")
        print(f"内存回收: {(after_leak_memory - after_cleanup_memory) / 1024 / 1024:.2f} MB")
        
        tracemalloc.stop()
        
        # 验证内存泄漏检测有效性
        self.assertGreater(after_leak_memory, initial_memory, "应该检测到内存增长")
        self.assertLess(after_cleanup_memory, after_leak_memory, "清理后内存应该减少")
    
    def test_profiling_analysis(self):
        """性能分析"""
        print("\n=== 性能分析 ===")
        
        # 创建性能分析器
        profiler = cProfile.Profile()
        
        # 开始分析
        profiler.enable()
        
        # 执行要分析的代码
        test_data = list(range(1000))
        random.shuffle(test_data)
        
        # 执行多种算法
        self.algorithm_benchmark.quick_sort(test_data.copy())
        self.algorithm_benchmark.python_sort(test_data.copy())
        
        # 计算斐波那契数列
        for i in range(10, 21):
            self.algorithm_benchmark.fibonacci_iterative(i)
            self.algorithm_benchmark.fibonacci_memoized(i)
        
        # 停止分析
        profiler.disable()
        
        # 生成报告
        print("\n性能分析报告:")
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        
        # 捕获输出到字符串
        output = io.StringIO()
        stats.print_stats(10, file=output)
        profile_output = output.getvalue()
        
        # 显示前几行分析结果
        lines = profile_output.split('\n')[:15]
        for line in lines:
            if line.strip():
                print(line)
        
        print("\n性能分析完成")
        
        # 验证分析器工作正常
        self.assertGreater(len(stats.stats), 0, "应该有性能统计数据")
    
    def test_async_performance(self):
        """异步性能测试"""
        print("\n=== 异步性能测试 ===")
        
        test_data = list(range(50))  # 使用较小的数据集
        
        # 同步处理时间
        sync_start = time.perf_counter()
        sync_result = self.data_processor.process_data_sequential(test_data)
        sync_end = time.perf_counter()
        sync_time = sync_end - sync_start
        
        # 异步处理时间
        async def run_async_test():
            async_start = time.perf_counter()
            async_result = await self.data_processor.process_data_async(test_data)
            async_end = time.perf_counter()
            return async_result, async_end - async_start
        
        async_result, async_time = asyncio.run(run_async_test())
        
        print(f"\n异步性能比较:")
        print(f"同步处理时间: {sync_time:.6f}s")
        print(f"异步处理时间: {async_time:.6f}s")
        print(f"性能比率: {sync_time / async_time:.2f}")
        
        # 验证结果正确性
        self.assertEqual(len(sync_result), len(async_result), "结果长度应该相同")
        
        # 对于IO密集型任务，异步通常更快
        if async_time < sync_time:
            print("异步处理更快（适合IO密集型任务）")
        else:
            print("同步处理更快（可能是CPU密集型任务）")


# 调试技术演示的完整实现
class DebuggingDemo:
    """调试技术演示类 - 完整实现"""
    
    def __init__(self):
        self.data = []
    
    def buggy_function(self, numbers: List[int]) -> float:
        """包含bug的函数"""
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
    
    def fixed_function(self, numbers: List[int]) -> float:
        """修复后的函数"""
        if not numbers:
            raise ValueError("输入列表不能为空")
        
        total = 0
        count = 0
        
        for num in numbers:
            if num != 0:  # 修复: 正确检查非零数字
                total += num
                count += 1
        
        if count == 0:  # 修复: 处理除零情况
            raise ValueError("没有非零数字，无法计算平均值")
        
        return total / count


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
    
    # 输出测试统计
    print(f"\n测试统计:")
    print(f"运行测试: {result.testsRun}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
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
    
    print("\n5. 修复后的函数:")
    try:
        result = demo.fixed_function(test_data)
        print(f"结果: {result}")
    except ValueError as e:
        print(f"值错误: {e}")


if __name__ == "__main__":
    print("Session29 练习3解决方案: 性能测试和调试技术")
    print("=" * 50)
    
    print("\n这个解决方案展示了:")
    print("1. 完整的性能测试框架")
    print("2. 算法性能比较和分析")
    print("3. 内存使用监控和泄漏检测")
    print("4. 并发性能测试")
    print("5. 性能分析和调试技术")
    print("6. 压力测试和基准测试")
    
    # 演示调试技术
    demonstrate_debugging()
    
    print("\n开始性能测试...")
    success = run_performance_tests()
    
    if success:
        print("\n🎉 所有性能测试都完成了！")
        print("\n学到的性能优化技巧:")
        print("- 使用基准测试比较算法性能")
        print("- 进行内存分析和泄漏检测")
        print("- 掌握各种调试技术")
        print("- 使用性能分析工具优化代码")
        print("- 理解并发和异步的性能特点")
        print("- 进行压力测试找出性能瓶颈")
    else:
        print("\n❌ 有测试未完成，请检查实现")