#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session29 Examples: 性能测试演示

本文件演示了各种性能测试技术：
- 基准测试(Benchmarking)
- 压力测试(Stress Testing)
- 负载测试(Load Testing)
- 内存性能测试
- 并发性能测试
- 性能回归测试

作者: Python教程团队
"""

import time
import timeit
import threading
import multiprocessing
import concurrent.futures
import asyncio
import psutil
import os
import gc
import sys
from functools import wraps
from typing import List, Dict, Callable, Any
from dataclasses import dataclass
from collections import defaultdict
import statistics
import matplotlib.pyplot as plt
import numpy as np


@dataclass
class PerformanceResult:
    """性能测试结果"""
    test_name: str
    execution_time: float
    memory_usage: float
    cpu_usage: float
    iterations: int
    success_rate: float
    error_count: int
    throughput: float  # 每秒处理数量


class PerformanceTester:
    """性能测试器"""
    
    def __init__(self):
        self.results = []
        self.process = psutil.Process(os.getpid())
    
    def benchmark(self, func: Callable, iterations: int = 1000, warmup: int = 100):
        """基准测试装饰器"""
        def decorator(test_func):
            @wraps(test_func)
            def wrapper(*args, **kwargs):
                print(f"\n开始基准测试: {func.__name__}")
                print(f"预热次数: {warmup}, 测试次数: {iterations}")
                
                # 预热
                print("预热中...")
                for _ in range(warmup):
                    try:
                        func(*args, **kwargs)
                    except Exception:
                        pass
                
                # 强制垃圾回收
                gc.collect()
                
                # 记录初始状态
                start_memory = self.process.memory_info().rss / 1024 / 1024
                start_cpu = self.process.cpu_percent()
                
                # 执行测试
                print("执行测试中...")
                times = []
                errors = 0
                
                start_time = time.perf_counter()
                
                for i in range(iterations):
                    iter_start = time.perf_counter()
                    try:
                        func(*args, **kwargs)
                    except Exception as e:
                        errors += 1
                    iter_end = time.perf_counter()
                    times.append(iter_end - iter_start)
                
                end_time = time.perf_counter()
                
                # 记录结束状态
                end_memory = self.process.memory_info().rss / 1024 / 1024
                end_cpu = self.process.cpu_percent()
                
                # 计算统计信息
                total_time = end_time - start_time
                avg_time = statistics.mean(times)
                median_time = statistics.median(times)
                min_time = min(times)
                max_time = max(times)
                std_time = statistics.stdev(times) if len(times) > 1 else 0
                
                success_rate = (iterations - errors) / iterations * 100
                throughput = iterations / total_time
                memory_diff = end_memory - start_memory
                
                # 创建结果对象
                result = PerformanceResult(
                    test_name=func.__name__,
                    execution_time=avg_time,
                    memory_usage=memory_diff,
                    cpu_usage=end_cpu - start_cpu,
                    iterations=iterations,
                    success_rate=success_rate,
                    error_count=errors,
                    throughput=throughput
                )
                
                self.results.append(result)
                
                # 打印结果
                print(f"\n{'='*60}")
                print(f"基准测试结果: {func.__name__}")
                print(f"{'='*60}")
                print(f"总执行时间: {total_time:.4f} 秒")
                print(f"平均执行时间: {avg_time*1000:.4f} 毫秒")
                print(f"中位数执行时间: {median_time*1000:.4f} 毫秒")
                print(f"最快执行时间: {min_time*1000:.4f} 毫秒")
                print(f"最慢执行时间: {max_time*1000:.4f} 毫秒")
                print(f"标准差: {std_time*1000:.4f} 毫秒")
                print(f"成功率: {success_rate:.1f}%")
                print(f"错误次数: {errors}")
                print(f"吞吐量: {throughput:.1f} 次/秒")
                print(f"内存变化: {memory_diff:+.1f} MB")
                print(f"CPU使用率变化: {end_cpu - start_cpu:+.1f}%")
                print(f"{'='*60}")
                
                return result
            
            return wrapper
        return decorator
    
    def stress_test(self, func: Callable, duration: int = 60, max_threads: int = 10):
        """压力测试"""
        print(f"\n开始压力测试: {func.__name__}")
        print(f"测试时长: {duration} 秒, 最大线程数: {max_threads}")
        
        results = []
        errors = []
        start_time = time.time()
        
        def worker():
            """工作线程"""
            thread_results = []
            thread_errors = []
            
            while time.time() - start_time < duration:
                try:
                    iter_start = time.perf_counter()
                    func()
                    iter_end = time.perf_counter()
                    thread_results.append(iter_end - iter_start)
                except Exception as e:
                    thread_errors.append(str(e))
            
            results.extend(thread_results)
            errors.extend(thread_errors)
        
        # 启动线程
        threads = []
        for i in range(max_threads):
            thread = threading.Thread(target=worker)
            thread.start()
            threads.append(thread)
        
        # 等待所有线程完成
        for thread in threads:
            thread.join()
        
        # 计算结果
        total_operations = len(results)
        total_errors = len(errors)
        success_rate = (total_operations / (total_operations + total_errors)) * 100 if (total_operations + total_errors) > 0 else 0
        throughput = total_operations / duration
        
        if results:
            avg_time = statistics.mean(results)
            median_time = statistics.median(results)
            min_time = min(results)
            max_time = max(results)
        else:
            avg_time = median_time = min_time = max_time = 0
        
        print(f"\n{'='*60}")
        print(f"压力测试结果: {func.__name__}")
        print(f"{'='*60}")
        print(f"测试时长: {duration} 秒")
        print(f"线程数: {max_threads}")
        print(f"总操作数: {total_operations}")
        print(f"错误数: {total_errors}")
        print(f"成功率: {success_rate:.1f}%")
        print(f"吞吐量: {throughput:.1f} 次/秒")
        print(f"平均响应时间: {avg_time*1000:.4f} 毫秒")
        print(f"中位数响应时间: {median_time*1000:.4f} 毫秒")
        print(f"最快响应时间: {min_time*1000:.4f} 毫秒")
        print(f"最慢响应时间: {max_time*1000:.4f} 毫秒")
        print(f"{'='*60}")
        
        return {
            'total_operations': total_operations,
            'total_errors': total_errors,
            'success_rate': success_rate,
            'throughput': throughput,
            'avg_time': avg_time,
            'median_time': median_time,
            'min_time': min_time,
            'max_time': max_time
        }
    
    def load_test(self, func: Callable, users: List[int], duration: int = 30):
        """负载测试 - 测试不同用户数下的性能"""
        print(f"\n开始负载测试: {func.__name__}")
        print(f"用户数序列: {users}, 每个负载测试时长: {duration} 秒")
        
        load_results = []
        
        for user_count in users:
            print(f"\n测试 {user_count} 个并发用户...")
            
            result = self.stress_test(func, duration=duration, max_threads=user_count)
            result['user_count'] = user_count
            load_results.append(result)
        
        # 生成负载测试报告
        print(f"\n{'='*80}")
        print(f"负载测试报告: {func.__name__}")
        print(f"{'='*80}")
        print(f"{'用户数':<8} {'吞吐量':<12} {'平均响应时间':<15} {'成功率':<8} {'错误数':<8}")
        print("-" * 80)
        
        for result in load_results:
            print(f"{result['user_count']:<8} "
                  f"{result['throughput']:<12.1f} "
                  f"{result['avg_time']*1000:<15.2f} "
                  f"{result['success_rate']:<8.1f}% "
                  f"{result['total_errors']:<8}")
        
        print(f"{'='*80}")
        
        return load_results
    
    def memory_test(self, func: Callable, iterations: int = 1000):
        """内存性能测试"""
        print(f"\n开始内存性能测试: {func.__name__}")
        print(f"测试次数: {iterations}")
        
        # 强制垃圾回收
        gc.collect()
        
        # 记录初始内存
        initial_memory = self.process.memory_info().rss / 1024 / 1024
        memory_samples = [initial_memory]
        
        print(f"初始内存使用: {initial_memory:.1f} MB")
        
        # 执行测试
        for i in range(iterations):
            func()
            
            # 每100次迭代记录一次内存
            if (i + 1) % 100 == 0:
                current_memory = self.process.memory_info().rss / 1024 / 1024
                memory_samples.append(current_memory)
                print(f"迭代 {i+1}: {current_memory:.1f} MB")
        
        # 强制垃圾回收
        gc.collect()
        final_memory = self.process.memory_info().rss / 1024 / 1024
        memory_samples.append(final_memory)
        
        # 计算内存统计
        memory_growth = final_memory - initial_memory
        max_memory = max(memory_samples)
        avg_memory = statistics.mean(memory_samples)
        
        print(f"\n{'='*60}")
        print(f"内存性能测试结果: {func.__name__}")
        print(f"{'='*60}")
        print(f"初始内存: {initial_memory:.1f} MB")
        print(f"最终内存: {final_memory:.1f} MB")
        print(f"内存增长: {memory_growth:+.1f} MB")
        print(f"峰值内存: {max_memory:.1f} MB")
        print(f"平均内存: {avg_memory:.1f} MB")
        print(f"内存增长率: {(memory_growth/initial_memory)*100:+.1f}%")
        print(f"{'='*60}")
        
        return {
            'initial_memory': initial_memory,
            'final_memory': final_memory,
            'memory_growth': memory_growth,
            'max_memory': max_memory,
            'avg_memory': avg_memory,
            'memory_samples': memory_samples
        }
    
    def compare_functions(self, functions: List[Callable], iterations: int = 1000):
        """比较多个函数的性能"""
        print(f"\n开始函数性能比较")
        print(f"测试函数: {[f.__name__ for f in functions]}")
        print(f"测试次数: {iterations}")
        
        comparison_results = []
        
        for func in functions:
            print(f"\n测试函数: {func.__name__}")
            
            # 使用timeit进行精确测量
            times = []
            for _ in range(iterations):
                start = time.perf_counter()
                func()
                end = time.perf_counter()
                times.append(end - start)
            
            avg_time = statistics.mean(times)
            median_time = statistics.median(times)
            min_time = min(times)
            max_time = max(times)
            std_time = statistics.stdev(times) if len(times) > 1 else 0
            
            comparison_results.append({
                'name': func.__name__,
                'avg_time': avg_time,
                'median_time': median_time,
                'min_time': min_time,
                'max_time': max_time,
                'std_time': std_time
            })
        
        # 排序结果（按平均时间）
        comparison_results.sort(key=lambda x: x['avg_time'])
        
        # 打印比较结果
        print(f"\n{'='*80}")
        print(f"函数性能比较结果")
        print(f"{'='*80}")
        print(f"{'排名':<4} {'函数名':<20} {'平均时间(ms)':<15} {'中位数(ms)':<15} {'标准差(ms)':<15}")
        print("-" * 80)
        
        fastest_time = comparison_results[0]['avg_time']
        
        for i, result in enumerate(comparison_results):
            ratio = result['avg_time'] / fastest_time
            print(f"{i+1:<4} "
                  f"{result['name']:<20} "
                  f"{result['avg_time']*1000:<15.4f} "
                  f"{result['median_time']*1000:<15.4f} "
                  f"{result['std_time']*1000:<15.4f} "
                  f"({ratio:.1f}x)")
        
        print(f"{'='*80}")
        
        return comparison_results
    
    def generate_report(self):
        """生成性能测试报告"""
        if not self.results:
            print("没有测试结果可生成报告")
            return
        
        print(f"\n{'='*80}")
        print(f"性能测试总结报告")
        print(f"{'='*80}")
        print(f"总测试数: {len(self.results)}")
        
        print(f"\n{'测试名称':<20} {'平均时间(ms)':<15} {'吞吐量':<12} {'成功率':<8} {'内存(MB)':<10}")
        print("-" * 80)
        
        for result in self.results:
            print(f"{result.test_name:<20} "
                  f"{result.execution_time*1000:<15.4f} "
                  f"{result.throughput:<12.1f} "
                  f"{result.success_rate:<8.1f}% "
                  f"{result.memory_usage:<10.1f}")
        
        print(f"{'='*80}")


# ============================================================================
# 测试用例
# ============================================================================

class TestCases:
    """性能测试用例"""
    
    @staticmethod
    def cpu_intensive_task():
        """CPU密集型任务"""
        total = 0
        for i in range(10000):
            total += i * i
        return total
    
    @staticmethod
    def memory_intensive_task():
        """内存密集型任务"""
        data = list(range(10000))
        processed = [x * 2 for x in data]
        return sum(processed)
    
    @staticmethod
    def io_simulation_task():
        """IO模拟任务"""
        # 模拟文件IO
        time.sleep(0.001)  # 模拟1ms的IO延迟
        return "IO completed"
    
    @staticmethod
    def string_processing_task():
        """字符串处理任务"""
        text = "Hello World " * 1000
        words = text.split()
        return len([word for word in words if len(word) > 3])
    
    @staticmethod
    def list_comprehension_task():
        """列表推导式任务"""
        return [x*2 for x in range(1000) if x % 2 == 0]
    
    @staticmethod
    def generator_task():
        """生成器任务"""
        return list(x*2 for x in range(1000) if x % 2 == 0)
    
    @staticmethod
    def dict_operations_task():
        """字典操作任务"""
        data = {i: i*2 for i in range(1000)}
        return sum(data.values())
    
    @staticmethod
    def recursive_fibonacci(n=20):
        """递归斐波那契数列"""
        if n <= 1:
            return n
        return TestCases.recursive_fibonacci(n-1) + TestCases.recursive_fibonacci(n-2)
    
    @staticmethod
    def iterative_fibonacci(n=20):
        """迭代斐波那契数列"""
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n+1):
            a, b = b, a + b
        return b


async def async_task():
    """异步任务"""
    await asyncio.sleep(0.001)
    return "Async task completed"


def demonstrate_benchmark_testing():
    """演示基准测试"""
    print("\n" + "="*50)
    print("基准测试演示")
    print("="*50)
    
    tester = PerformanceTester()
    
    # 测试CPU密集型任务
    @tester.benchmark(TestCases.cpu_intensive_task, iterations=100)
    def test_cpu_task():
        return TestCases.cpu_intensive_task()
    
    # 测试内存密集型任务
    @tester.benchmark(TestCases.memory_intensive_task, iterations=100)
    def test_memory_task():
        return TestCases.memory_intensive_task()
    
    # 测试字符串处理任务
    @tester.benchmark(TestCases.string_processing_task, iterations=100)
    def test_string_task():
        return TestCases.string_processing_task()
    
    # 执行测试
    test_cpu_task()
    test_memory_task()
    test_string_task()
    
    return tester


def demonstrate_stress_testing():
    """演示压力测试"""
    print("\n" + "="*50)
    print("压力测试演示")
    print("="*50)
    
    tester = PerformanceTester()
    
    # 压力测试CPU任务
    print("\n压力测试 - CPU密集型任务")
    tester.stress_test(TestCases.cpu_intensive_task, duration=10, max_threads=4)
    
    # 压力测试IO任务
    print("\n压力测试 - IO模拟任务")
    tester.stress_test(TestCases.io_simulation_task, duration=10, max_threads=10)
    
    return tester


def demonstrate_load_testing():
    """演示负载测试"""
    print("\n" + "="*50)
    print("负载测试演示")
    print("="*50)
    
    tester = PerformanceTester()
    
    # 负载测试 - 不同用户数
    user_loads = [1, 2, 4, 8, 16]
    tester.load_test(TestCases.string_processing_task, users=user_loads, duration=15)
    
    return tester


def demonstrate_memory_testing():
    """演示内存测试"""
    print("\n" + "="*50)
    print("内存测试演示")
    print("="*50)
    
    tester = PerformanceTester()
    
    # 内存测试
    tester.memory_test(TestCases.memory_intensive_task, iterations=500)
    
    return tester


def demonstrate_function_comparison():
    """演示函数性能比较"""
    print("\n" + "="*50)
    print("函数性能比较演示")
    print("="*50)
    
    tester = PerformanceTester()
    
    # 比较不同的实现方式
    functions_to_compare = [
        TestCases.list_comprehension_task,
        TestCases.generator_task,
        TestCases.dict_operations_task
    ]
    
    tester.compare_functions(functions_to_compare, iterations=1000)
    
    # 比较递归vs迭代
    print("\n比较递归vs迭代实现:")
    fibonacci_functions = [
        TestCases.iterative_fibonacci,
        TestCases.recursive_fibonacci
    ]
    
    tester.compare_functions(fibonacci_functions, iterations=100)
    
    return tester


def demonstrate_concurrent_testing():
    """演示并发性能测试"""
    print("\n" + "="*50)
    print("并发性能测试演示")
    print("="*50)
    
    def test_threading():
        """测试多线程性能"""
        def worker():
            return TestCases.cpu_intensive_task()
        
        start_time = time.perf_counter()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(worker) for _ in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        end_time = time.perf_counter()
        
        print(f"多线程执行时间: {end_time - start_time:.4f} 秒")
        print(f"处理任务数: {len(results)}")
        return end_time - start_time
    
    def test_multiprocessing():
        """测试多进程性能"""
        def worker():
            return TestCases.cpu_intensive_task()
        
        start_time = time.perf_counter()
        
        with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(worker) for _ in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        end_time = time.perf_counter()
        
        print(f"多进程执行时间: {end_time - start_time:.4f} 秒")
        print(f"处理任务数: {len(results)}")
        return end_time - start_time
    
    def test_sequential():
        """测试顺序执行性能"""
        start_time = time.perf_counter()
        
        results = [TestCases.cpu_intensive_task() for _ in range(10)]
        
        end_time = time.perf_counter()
        
        print(f"顺序执行时间: {end_time - start_time:.4f} 秒")
        print(f"处理任务数: {len(results)}")
        return end_time - start_time
    
    # 执行并发测试
    sequential_time = test_sequential()
    threading_time = test_threading()
    multiprocessing_time = test_multiprocessing()
    
    # 比较结果
    print(f"\n{'='*60}")
    print(f"并发性能比较结果")
    print(f"{'='*60}")
    print(f"顺序执行: {sequential_time:.4f} 秒 (基准)")
    print(f"多线程: {threading_time:.4f} 秒 ({sequential_time/threading_time:.1f}x 加速)")
    print(f"多进程: {multiprocessing_time:.4f} 秒 ({sequential_time/multiprocessing_time:.1f}x 加速)")
    print(f"{'='*60}")


def demonstrate_async_testing():
    """演示异步性能测试"""
    print("\n" + "="*50)
    print("异步性能测试演示")
    print("="*50)
    
    async def test_async_performance():
        """测试异步性能"""
        start_time = time.perf_counter()
        
        # 并发执行多个异步任务
        tasks = [async_task() for _ in range(100)]
        results = await asyncio.gather(*tasks)
        
        end_time = time.perf_counter()
        
        print(f"异步执行时间: {end_time - start_time:.4f} 秒")
        print(f"处理任务数: {len(results)}")
        print(f"平均每任务时间: {(end_time - start_time) / len(results) * 1000:.2f} 毫秒")
        
        return end_time - start_time
    
    def test_sync_performance():
        """测试同步性能"""
        start_time = time.perf_counter()
        
        # 顺序执行模拟的同步任务
        results = []
        for _ in range(100):
            time.sleep(0.001)  # 模拟IO延迟
            results.append("Sync task completed")
        
        end_time = time.perf_counter()
        
        print(f"同步执行时间: {end_time - start_time:.4f} 秒")
        print(f"处理任务数: {len(results)}")
        print(f"平均每任务时间: {(end_time - start_time) / len(results) * 1000:.2f} 毫秒")
        
        return end_time - start_time
    
    # 执行测试
    sync_time = test_sync_performance()
    async_time = asyncio.run(test_async_performance())
    
    # 比较结果
    print(f"\n{'='*60}")
    print(f"同步vs异步性能比较")
    print(f"{'='*60}")
    print(f"同步执行: {sync_time:.4f} 秒")
    print(f"异步执行: {async_time:.4f} 秒")
    print(f"性能提升: {sync_time/async_time:.1f}x")
    print(f"{'='*60}")


def main():
    """主函数：性能测试演示"""
    print("Session29: 性能测试演示")
    print("=" * 50)
    
    try:
        # 1. 基准测试演示
        tester1 = demonstrate_benchmark_testing()
        
        # 2. 压力测试演示
        tester2 = demonstrate_stress_testing()
        
        # 3. 负载测试演示
        tester3 = demonstrate_load_testing()
        
        # 4. 内存测试演示
        tester4 = demonstrate_memory_testing()
        
        # 5. 函数比较演示
        tester5 = demonstrate_function_comparison()
        
        # 6. 并发测试演示
        demonstrate_concurrent_testing()
        
        # 7. 异步测试演示
        demonstrate_async_testing()
        
        # 生成综合报告
        print("\n" + "="*50)
        print("生成综合性能报告")
        print("="*50)
        tester1.generate_report()
        
        print("\n" + "="*50)
        print("性能测试演示完成！")
        print("="*50)
        
        print("\n性能测试总结:")
        print("1. 基准测试: 测量单个函数的基础性能")
        print("2. 压力测试: 测试系统在高负载下的表现")
        print("3. 负载测试: 测试不同负载级别下的性能")
        print("4. 内存测试: 监控内存使用和泄漏")
        print("5. 并发测试: 比较不同并发模式的性能")
        print("6. 异步测试: 测试异步操作的性能优势")
        
        print("\n性能优化建议:")
        print("- 选择合适的数据结构和算法")
        print("- 合理使用并发和异步编程")
        print("- 监控和优化内存使用")
        print("- 定期进行性能回归测试")
        print("- 使用性能分析工具找出瓶颈")
        
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()