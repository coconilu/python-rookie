#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session24 练习题1：基础性能优化

题目描述：
给定一个包含大量数字的列表，需要找出其中所有的素数。
请实现三种不同的方法，并比较它们的性能：
1. 朴素方法：对每个数字检查是否为素数
2. 优化方法：使用埃拉托斯特尼筛法
3. 进一步优化：只检查到平方根，并跳过偶数

输入示例：
numbers = list(range(2, 10000))

输出示例：
找到的素数数量和每种方法的执行时间

提示：
- 使用time模块测量执行时间
- 素数是只能被1和自身整除的大于1的自然数
- 埃拉托斯特尼筛法是一种高效的素数筛选算法
- 可以通过只检查到sqrt(n)来优化素数判断
"""

import time
import math


def is_prime_naive(n):
    """
    朴素的素数判断方法
    时间复杂度: O(n)
    """
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


def is_prime_optimized(n):
    """
    优化的素数判断方法
    时间复杂度: O(sqrt(n))
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # 只检查到平方根，且只检查奇数
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def sieve_of_eratosthenes(limit):
    """
    埃拉托斯特尼筛法
    时间复杂度: O(n log log n)
    """
    if limit < 2:
        return []
    
    # 创建布尔数组，初始化为True
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    
    # 筛选过程
    for i in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[i]:
            # 标记i的所有倍数为非素数
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False
    
    # 收集所有素数
    return [i for i in range(2, limit + 1) if is_prime[i]]


def find_primes_method1(numbers):
    """
    方法1：使用朴素方法找素数
    """
    primes = []
    for num in numbers:
        if is_prime_naive(num):
            primes.append(num)
    return primes


def find_primes_method2(numbers):
    """
    方法2：使用优化方法找素数
    """
    primes = []
    for num in numbers:
        if is_prime_optimized(num):
            primes.append(num)
    return primes


def find_primes_method3(numbers):
    """
    方法3：使用埃拉托斯特尼筛法
    """
    if not numbers:
        return []
    
    max_num = max(numbers)
    all_primes = sieve_of_eratosthenes(max_num)
    
    # 只返回在输入列表中的素数
    number_set = set(numbers)
    return [p for p in all_primes if p in number_set]


def performance_test():
    """
    性能测试函数
    """
    # 测试数据
    test_numbers = list(range(2, 5000))  # 可以调整范围来测试不同规模
    
    print(f"测试范围: {min(test_numbers)} 到 {max(test_numbers)}")
    print(f"总数字数量: {len(test_numbers):,}")
    print("=" * 50)
    
    methods = [
        ("朴素方法", find_primes_method1),
        ("优化方法", find_primes_method2),
        ("筛法", find_primes_method3)
    ]
    
    results = {}
    
    for method_name, method_func in methods:
        print(f"\n正在测试 {method_name}...")
        
        start_time = time.time()
        primes = method_func(test_numbers)
        end_time = time.time()
        
        execution_time = end_time - start_time
        results[method_name] = {
            'primes': primes,
            'count': len(primes),
            'time': execution_time
        }
        
        print(f"{method_name}: 找到 {len(primes)} 个素数，耗时 {execution_time:.6f} 秒")
    
    # 验证结果一致性
    print("\n=== 结果验证 ===")
    prime_counts = [results[method]['count'] for method in results]
    if len(set(prime_counts)) == 1:
        print("✓ 所有方法找到的素数数量一致")
    else:
        print("✗ 方法结果不一致，请检查实现")
    
    # 性能比较
    print("\n=== 性能比较 ===")
    times = [(method, results[method]['time']) for method in results]
    times.sort(key=lambda x: x[1])  # 按时间排序
    
    fastest_time = times[0][1]
    
    for i, (method, time_taken) in enumerate(times):
        if i == 0:
            print(f"🥇 {method}: {time_taken:.6f} 秒 (最快)")
        else:
            speedup = time_taken / fastest_time
            print(f"{'🥈' if i == 1 else '🥉'} {method}: {time_taken:.6f} 秒 (慢 {speedup:.1f} 倍)")
    
    # 显示部分素数
    first_method = list(results.keys())[0]
    primes = results[first_method]['primes']
    print(f"\n前20个素数: {primes[:20]}")
    print(f"最大的10个素数: {primes[-10:]}")


def solution():
    """
    练习解决方案
    """
    print("Session24 练习题1: 基础性能优化")
    print("=" * 50)
    print("任务: 比较三种素数查找方法的性能")
    
    try:
        performance_test()
        
        print("\n=== 学习要点 ===")
        print("1. 算法复杂度对性能的巨大影响")
        print("2. 埃拉托斯特尼筛法在大规模数据上的优势")
        print("3. 简单的优化（如只检查到平方根）也能带来显著提升")
        print("4. 不同算法适用于不同的场景")
        
    except Exception as e:
        print(f"执行过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    solution()