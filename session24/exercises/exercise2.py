#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session24 练习题2：内存优化和数据结构选择

题目描述：
实现一个日志分析器，需要处理大量的日志数据。
要求实现以下功能并比较不同实现方式的内存使用和性能：

1. 读取大文件（模拟日志文件）
2. 统计不同IP地址的访问次数
3. 找出访问次数最多的前10个IP
4. 计算每小时的访问量

需要比较的实现方式：
- 普通列表 vs 生成器
- 普通字典 vs defaultdict vs Counter
- 不同的数据结构对内存和性能的影响

输入示例：
模拟的日志格式："192.168.1.1 - - [01/Jan/2024:12:00:01] GET /index.html"

输出示例：
各种实现方式的内存使用量和执行时间对比
"""

import time
import random
import sys
from collections import defaultdict, Counter
from datetime import datetime, timedelta
import gc
import tracemalloc


class MemoryProfiler:
    """
    简单的内存分析器
    """
    def __init__(self):
        self.start_memory = 0
        self.peak_memory = 0
    
    def start(self):
        """开始内存监控"""
        gc.collect()  # 强制垃圾回收
        tracemalloc.start()
        self.start_memory = tracemalloc.get_traced_memory()[0]
    
    def stop(self):
        """停止内存监控并返回内存使用情况"""
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        memory_used = current - self.start_memory
        peak_memory = peak - self.start_memory
        
        return {
            'used': memory_used,
            'peak': peak_memory,
            'used_mb': memory_used / 1024 / 1024,
            'peak_mb': peak_memory / 1024 / 1024
        }


def generate_log_data(num_lines=100000):
    """
    生成模拟的日志数据
    """
    ips = [f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}" 
           for _ in range(1000)]  # 1000个不同的IP
    
    pages = ["/index.html", "/about.html", "/contact.html", "/products.html", 
             "/login.html", "/api/data", "/images/logo.png", "/css/style.css"]
    
    base_time = datetime(2024, 1, 1, 0, 0, 0)
    
    logs = []
    for i in range(num_lines):
        ip = random.choice(ips)
        page = random.choice(pages)
        # 模拟24小时内的随机时间
        log_time = base_time + timedelta(seconds=random.randint(0, 86400))
        time_str = log_time.strftime("%d/%b/%Y:%H:%M:%S")
        
        log_line = f"{ip} - - [{time_str}] GET {page}"
        logs.append(log_line)
    
    return logs


def parse_log_line(line):
    """
    解析日志行，提取IP和时间
    """
    parts = line.split()
    ip = parts[0]
    
    # 提取时间部分 [01/Jan/2024:12:00:01]
    time_part = parts[3][1:]  # 去掉开头的 [
    hour = int(time_part.split(':')[1])  # 提取小时
    
    return ip, hour


# 方法1：使用普通列表和字典
def analyze_logs_basic(logs):
    """
    基础方法：使用普通列表和字典
    """
    # 将所有日志加载到内存
    all_logs = list(logs)  # 如果logs是生成器，这里会全部加载
    
    ip_counts = {}
    hour_counts = {}
    
    for log_line in all_logs:
        ip, hour = parse_log_line(log_line)
        
        # 统计IP访问次数
        if ip in ip_counts:
            ip_counts[ip] += 1
        else:
            ip_counts[ip] = 1
        
        # 统计每小时访问次数
        if hour in hour_counts:
            hour_counts[hour] += 1
        else:
            hour_counts[hour] = 1
    
    # 找出访问最多的前10个IP
    top_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return {
        'total_logs': len(all_logs),
        'unique_ips': len(ip_counts),
        'top_ips': top_ips,
        'hour_counts': hour_counts
    }


# 方法2：使用defaultdict
def analyze_logs_defaultdict(logs):
    """
    使用defaultdict优化
    """
    ip_counts = defaultdict(int)
    hour_counts = defaultdict(int)
    total_logs = 0
    
    for log_line in logs:
        ip, hour = parse_log_line(log_line)
        
        ip_counts[ip] += 1
        hour_counts[hour] += 1
        total_logs += 1
    
    # 找出访问最多的前10个IP
    top_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return {
        'total_logs': total_logs,
        'unique_ips': len(ip_counts),
        'top_ips': top_ips,
        'hour_counts': dict(hour_counts)
    }


# 方法3：使用Counter
def analyze_logs_counter(logs):
    """
    使用Counter优化
    """
    ips = []
    hours = []
    total_logs = 0
    
    for log_line in logs:
        ip, hour = parse_log_line(log_line)
        ips.append(ip)
        hours.append(hour)
        total_logs += 1
    
    ip_counts = Counter(ips)
    hour_counts = Counter(hours)
    
    # 找出访问最多的前10个IP
    top_ips = ip_counts.most_common(10)
    
    return {
        'total_logs': total_logs,
        'unique_ips': len(ip_counts),
        'top_ips': top_ips,
        'hour_counts': dict(hour_counts)
    }


# 方法4：使用生成器（内存优化）
def analyze_logs_generator(log_generator):
    """
    使用生成器进行内存优化
    """
    ip_counts = defaultdict(int)
    hour_counts = defaultdict(int)
    total_logs = 0
    
    # 逐行处理，不将所有数据加载到内存
    for log_line in log_generator:
        ip, hour = parse_log_line(log_line)
        
        ip_counts[ip] += 1
        hour_counts[hour] += 1
        total_logs += 1
    
    # 找出访问最多的前10个IP
    top_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return {
        'total_logs': total_logs,
        'unique_ips': len(ip_counts),
        'top_ips': top_ips,
        'hour_counts': dict(hour_counts)
    }


def log_generator(logs):
    """
    日志生成器，逐行yield日志
    """
    for log in logs:
        yield log


def benchmark_method(method_name, method_func, data):
    """
    基准测试函数
    """
    print(f"\n测试 {method_name}...")
    
    profiler = MemoryProfiler()
    profiler.start()
    
    start_time = time.time()
    result = method_func(data)
    end_time = time.time()
    
    memory_info = profiler.stop()
    execution_time = end_time - start_time
    
    print(f"  执行时间: {execution_time:.4f} 秒")
    print(f"  内存使用: {memory_info['used_mb']:.2f} MB")
    print(f"  峰值内存: {memory_info['peak_mb']:.2f} MB")
    print(f"  处理日志: {result['total_logs']:,} 条")
    print(f"  唯一IP: {result['unique_ips']:,} 个")
    
    return {
        'method': method_name,
        'time': execution_time,
        'memory_used': memory_info['used_mb'],
        'memory_peak': memory_info['peak_mb'],
        'result': result
    }


def performance_comparison():
    """
    性能对比测试
    """
    print("Session24 练习题2: 内存优化和数据结构选择")
    print("=" * 60)
    
    # 生成测试数据
    print("生成测试数据...")
    log_data = generate_log_data(50000)  # 5万条日志
    print(f"生成了 {len(log_data):,} 条日志数据")
    
    # 测试不同的方法
    methods = [
        ("普通列表+字典", lambda data: analyze_logs_basic(data)),
        ("defaultdict", lambda data: analyze_logs_defaultdict(data)),
        ("Counter", lambda data: analyze_logs_counter(data)),
        ("生成器+defaultdict", lambda data: analyze_logs_generator(log_generator(data)))
    ]
    
    results = []
    
    for method_name, method_func in methods:
        try:
            result = benchmark_method(method_name, method_func, log_data)
            results.append(result)
        except Exception as e:
            print(f"  ❌ 方法 {method_name} 执行失败: {e}")
    
    # 结果对比
    print("\n" + "=" * 60)
    print("性能对比结果:")
    print("=" * 60)
    
    # 按执行时间排序
    results.sort(key=lambda x: x['time'])
    
    print(f"{'方法':<20} {'时间(秒)':<10} {'内存(MB)':<10} {'峰值(MB)':<10}")
    print("-" * 60)
    
    fastest_time = results[0]['time']
    lowest_memory = min(r['memory_used'] for r in results)
    
    for i, result in enumerate(results):
        time_ratio = result['time'] / fastest_time
        memory_ratio = result['memory_used'] / lowest_memory if lowest_memory > 0 else 1
        
        status = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "  "
        
        print(f"{status} {result['method']:<18} "
              f"{result['time']:<10.4f} "
              f"{result['memory_used']:<10.2f} "
              f"{result['memory_peak']:<10.2f}")
        
        if i > 0:
            print(f"   (慢 {time_ratio:.1f}x, 内存 {memory_ratio:.1f}x)")
    
    # 显示分析结果
    if results:
        sample_result = results[0]['result']
        print(f"\n分析结果示例:")
        print(f"访问量最高的前5个IP:")
        for ip, count in sample_result['top_ips'][:5]:
            print(f"  {ip}: {count:,} 次访问")
        
        print(f"\n各小时访问量:")
        hour_data = sorted(sample_result['hour_counts'].items())
        for hour, count in hour_data[:12]:  # 显示前12小时
            print(f"  {hour:02d}:00 - {count:,} 次访问")


def solution():
    """
    练习解决方案
    """
    try:
        performance_comparison()
        
        print("\n=== 学习要点 ===")
        print("1. defaultdict 比普通字典更高效，避免了键存在性检查")
        print("2. Counter 专门用于计数，提供了便利的方法如 most_common()")
        print("3. 生成器可以显著减少内存使用，适合处理大文件")
        print("4. 选择合适的数据结构对性能影响很大")
        print("5. 内存和时间往往需要权衡，没有绝对最优的方案")
        
    except Exception as e:
        print(f"执行过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    solution()