#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session24 演示项目：高性能数据处理器

这是一个综合性的演示项目，展示了多种性能优化技术在实际应用中的运用：
1. 大文件处理优化
2. 内存管理优化
3. 算法优化
4. 缓存策略
5. 并发处理
6. 性能监控

项目场景：
处理大量的销售数据，进行统计分析和报告生成
"""

import time
import csv
import json
import random
import threading
from datetime import datetime, timedelta
from collections import defaultdict, Counter, namedtuple
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import lru_cache
import gc
import tracemalloc
from pathlib import Path


# 使用namedtuple优化内存
SalesRecord = namedtuple('SalesRecord', [
    'date', 'product_id', 'category', 'quantity', 'price', 'customer_id', 'region'
])


class PerformanceMonitor:
    """
    性能监控器
    """
    def __init__(self):
        self.start_time = None
        self.start_memory = None
        self.operations = []
    
    def start_monitoring(self):
        """开始监控"""
        gc.collect()
        tracemalloc.start()
        self.start_time = time.time()
        self.start_memory = tracemalloc.get_traced_memory()[0]
    
    def log_operation(self, operation_name):
        """记录操作"""
        current_time = time.time()
        current_memory = tracemalloc.get_traced_memory()[0]
        
        self.operations.append({
            'operation': operation_name,
            'time': current_time - self.start_time,
            'memory_mb': (current_memory - self.start_memory) / 1024 / 1024
        })
    
    def stop_monitoring(self):
        """停止监控并返回报告"""
        end_time = time.time()
        end_memory, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        total_time = end_time - self.start_time
        memory_used = (end_memory - self.start_memory) / 1024 / 1024
        peak_memory_used = (peak_memory - self.start_memory) / 1024 / 1024
        
        return {
            'total_time': total_time,
            'memory_used_mb': memory_used,
            'peak_memory_mb': peak_memory_used,
            'operations': self.operations
        }


class OptimizedDataProcessor:
    """
    优化的数据处理器
    """
    def __init__(self, cache_size=1000):
        self.cache_size = cache_size
        self.monitor = PerformanceMonitor()
        self._category_cache = {}
        self._region_cache = {}
        
        # 线程锁，用于线程安全
        self._lock = threading.Lock()
    
    def generate_sample_data(self, num_records=100000, filename="sales_data.csv"):
        """
        生成示例销售数据
        """
        print(f"生成 {num_records:,} 条销售记录...")
        
        categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Sports', 'Beauty']
        regions = ['North', 'South', 'East', 'West', 'Central']
        
        # 使用生成器减少内存使用
        def data_generator():
            base_date = datetime(2024, 1, 1)
            for i in range(num_records):
                date = base_date + timedelta(days=random.randint(0, 365))
                yield {
                    'date': date.strftime('%Y-%m-%d'),
                    'product_id': f'P{random.randint(1000, 9999)}',
                    'category': random.choice(categories),
                    'quantity': random.randint(1, 10),
                    'price': round(random.uniform(10, 1000), 2),
                    'customer_id': f'C{random.randint(10000, 99999)}',
                    'region': random.choice(regions)
                }
        
        # 分批写入文件，避免内存溢出
        batch_size = 10000
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'date', 'product_id', 'category', 'quantity', 'price', 'customer_id', 'region'
            ])
            writer.writeheader()
            
            batch = []
            for record in data_generator():
                batch.append(record)
                if len(batch) >= batch_size:
                    writer.writerows(batch)
                    batch = []
            
            # 写入剩余记录
            if batch:
                writer.writerows(batch)
        
        print(f"数据已保存到 {filename}")
        return filename
    
    def read_data_optimized(self, filename):
        """
        优化的数据读取方法（使用生成器）
        """
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # 转换为namedtuple以节省内存
                yield SalesRecord(
                    date=row['date'],
                    product_id=row['product_id'],
                    category=row['category'],
                    quantity=int(row['quantity']),
                    price=float(row['price']),
                    customer_id=row['customer_id'],
                    region=row['region']
                )
    
    def read_data_basic(self, filename):
        """
        基础的数据读取方法（全部加载到内存）
        """
        records = []
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(SalesRecord(
                    date=row['date'],
                    product_id=row['product_id'],
                    category=row['category'],
                    quantity=int(row['quantity']),
                    price=float(row['price']),
                    customer_id=row['customer_id'],
                    region=row['region']
                ))
        return records
    
    @lru_cache(maxsize=128)
    def get_category_multiplier(self, category):
        """
        获取类别乘数（模拟复杂计算，使用缓存优化）
        """
        # 模拟复杂计算
        time.sleep(0.001)  # 模拟计算延迟
        
        multipliers = {
            'Electronics': 1.2,
            'Clothing': 1.1,
            'Books': 0.9,
            'Home': 1.15,
            'Sports': 1.05,
            'Beauty': 1.3
        }
        return multipliers.get(category, 1.0)
    
    def calculate_revenue_optimized(self, records):
        """
        优化的收入计算（使用生成器和缓存）
        """
        total_revenue = 0
        category_revenue = defaultdict(float)
        region_revenue = defaultdict(float)
        
        for record in records:
            # 使用缓存的类别乘数
            multiplier = self.get_category_multiplier(record.category)
            revenue = record.quantity * record.price * multiplier
            
            total_revenue += revenue
            category_revenue[record.category] += revenue
            region_revenue[record.region] += revenue
        
        return {
            'total': total_revenue,
            'by_category': dict(category_revenue),
            'by_region': dict(region_revenue)
        }
    
    def calculate_revenue_basic(self, records):
        """
        基础的收入计算
        """
        total_revenue = 0
        category_revenue = {}
        region_revenue = {}
        
        for record in records:
            # 每次都重新计算乘数（无缓存）
            if record.category == 'Electronics':
                multiplier = 1.2
            elif record.category == 'Clothing':
                multiplier = 1.1
            elif record.category == 'Books':
                multiplier = 0.9
            elif record.category == 'Home':
                multiplier = 1.15
            elif record.category == 'Sports':
                multiplier = 1.05
            elif record.category == 'Beauty':
                multiplier = 1.3
            else:
                multiplier = 1.0
            
            revenue = record.quantity * record.price * multiplier
            
            total_revenue += revenue
            
            # 使用普通字典（需要检查键是否存在）
            if record.category in category_revenue:
                category_revenue[record.category] += revenue
            else:
                category_revenue[record.category] = revenue
            
            if record.region in region_revenue:
                region_revenue[record.region] += revenue
            else:
                region_revenue[record.region] = revenue
        
        return {
            'total': total_revenue,
            'by_category': category_revenue,
            'by_region': region_revenue
        }
    
    def analyze_customer_patterns(self, records):
        """
        分析客户购买模式
        """
        customer_stats = defaultdict(lambda: {
            'total_spent': 0,
            'order_count': 0,
            'categories': set(),
            'regions': set()
        })
        
        for record in records:
            customer = customer_stats[record.customer_id]
            customer['total_spent'] += record.quantity * record.price
            customer['order_count'] += 1
            customer['categories'].add(record.category)
            customer['regions'].add(record.region)
        
        # 转换set为list以便JSON序列化
        for customer_id, stats in customer_stats.items():
            stats['categories'] = list(stats['categories'])
            stats['regions'] = list(stats['regions'])
            stats['avg_order_value'] = stats['total_spent'] / stats['order_count']
        
        return dict(customer_stats)
    
    def parallel_process_by_region(self, filename, max_workers=4):
        """
        并行处理不同地区的数据
        """
        # 首先按地区分组数据
        region_data = defaultdict(list)
        
        for record in self.read_data_optimized(filename):
            region_data[record.region].append(record)
        
        def process_region(region_records):
            """处理单个地区的数据"""
            region, records = region_records
            revenue = self.calculate_revenue_optimized(iter(records))
            customer_patterns = self.analyze_customer_patterns(records)
            
            return {
                'region': region,
                'revenue': revenue,
                'customer_count': len(customer_patterns),
                'record_count': len(records)
            }
        
        # 并行处理各地区
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(process_region, item) for item in region_data.items()]
            results = [future.result() for future in futures]
        
        return results
    
    def generate_report(self, analysis_results):
        """
        生成分析报告
        """
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_revenue': 0,
                'total_customers': 0,
                'total_records': 0
            },
            'regional_analysis': analysis_results,
            'performance_metrics': None
        }
        
        # 汇总统计
        for region_result in analysis_results:
            report['summary']['total_revenue'] += region_result['revenue']['total']
            report['summary']['total_customers'] += region_result['customer_count']
            report['summary']['total_records'] += region_result['record_count']
        
        return report
    
    def benchmark_methods(self, filename):
        """
        基准测试不同的处理方法
        """
        print("\n=== 性能基准测试 ===")
        
        methods = [
            ("基础方法(全内存加载)", self._benchmark_basic_method),
            ("优化方法(生成器+缓存)", self._benchmark_optimized_method),
            ("并行处理", self._benchmark_parallel_method)
        ]
        
        results = []
        
        for method_name, method_func in methods:
            print(f"\n测试 {method_name}...")
            
            # 清理缓存
            self.get_category_multiplier.cache_clear()
            gc.collect()
            
            try:
                result = method_func(filename)
                results.append((method_name, result))
                
                print(f"  执行时间: {result['execution_time']:.4f} 秒")
                print(f"  内存使用: {result['memory_used']:.2f} MB")
                print(f"  总收入: ${result['total_revenue']:,.2f}")
                
            except Exception as e:
                print(f"  ❌ 执行失败: {e}")
        
        return results
    
    def _benchmark_basic_method(self, filename):
        """基础方法基准测试"""
        self.monitor.start_monitoring()
        
        # 全部加载到内存
        records = self.read_data_basic(filename)
        self.monitor.log_operation("数据加载")
        
        # 基础计算
        revenue_result = self.calculate_revenue_basic(records)
        self.monitor.log_operation("收入计算")
        
        performance = self.monitor.stop_monitoring()
        
        return {
            'execution_time': performance['total_time'],
            'memory_used': performance['memory_used_mb'],
            'total_revenue': revenue_result['total'],
            'method': 'basic'
        }
    
    def _benchmark_optimized_method(self, filename):
        """优化方法基准测试"""
        self.monitor.start_monitoring()
        
        # 使用生成器
        records = self.read_data_optimized(filename)
        self.monitor.log_operation("数据加载(生成器)")
        
        # 优化计算
        revenue_result = self.calculate_revenue_optimized(records)
        self.monitor.log_operation("收入计算(缓存)")
        
        performance = self.monitor.stop_monitoring()
        
        return {
            'execution_time': performance['total_time'],
            'memory_used': performance['memory_used_mb'],
            'total_revenue': revenue_result['total'],
            'method': 'optimized'
        }
    
    def _benchmark_parallel_method(self, filename):
        """并行方法基准测试"""
        self.monitor.start_monitoring()
        
        # 并行处理
        results = self.parallel_process_by_region(filename)
        self.monitor.log_operation("并行处理")
        
        # 汇总结果
        total_revenue = sum(r['revenue']['total'] for r in results)
        
        performance = self.monitor.stop_monitoring()
        
        return {
            'execution_time': performance['total_time'],
            'memory_used': performance['memory_used_mb'],
            'total_revenue': total_revenue,
            'method': 'parallel'
        }


def main():
    """
    主函数：演示完整的数据处理流程
    """
    print("Session24 演示项目：高性能数据处理器")
    print("=" * 60)
    
    processor = OptimizedDataProcessor()
    
    try:
        # 1. 生成示例数据
        data_file = processor.generate_sample_data(50000)  # 5万条记录
        
        # 2. 性能基准测试
        benchmark_results = processor.benchmark_methods(data_file)
        
        # 3. 显示性能对比
        print("\n" + "=" * 60)
        print("性能对比结果:")
        print("=" * 60)
        
        # 按执行时间排序
        benchmark_results.sort(key=lambda x: x[1]['execution_time'])
        
        print(f"{'方法':<20} {'时间(秒)':<10} {'内存(MB)':<10} {'加速比':<8}")
        print("-" * 60)
        
        baseline_time = benchmark_results[-1][1]['execution_time']
        
        for i, (method_name, result) in enumerate(benchmark_results):
            speedup = baseline_time / result['execution_time']
            status = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
            
            print(f"{status} {method_name:<18} "
                  f"{result['execution_time']:<10.4f} "
                  f"{result['memory_used']:<10.2f} "
                  f"{speedup:<8.1f}x")
        
        # 4. 生成详细报告
        print("\n生成详细分析报告...")
        analysis_results = processor.parallel_process_by_region(data_file)
        report = processor.generate_report(analysis_results)
        
        # 保存报告
        report_file = "sales_analysis_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"报告已保存到 {report_file}")
        
        # 5. 显示缓存统计
        cache_info = processor.get_category_multiplier.cache_info()
        print(f"\n缓存统计: {cache_info}")
        print(f"缓存命中率: {cache_info.hits / (cache_info.hits + cache_info.misses):.2%}")
        
        # 6. 显示报告摘要
        print("\n=== 分析报告摘要 ===")
        print(f"总收入: ${report['summary']['total_revenue']:,.2f}")
        print(f"总客户数: {report['summary']['total_customers']:,}")
        print(f"总记录数: {report['summary']['total_records']:,}")
        
        print("\n各地区收入排名:")
        regional_revenues = [(r['region'], r['revenue']['total']) for r in analysis_results]
        regional_revenues.sort(key=lambda x: x[1], reverse=True)
        
        for i, (region, revenue) in enumerate(regional_revenues, 1):
            print(f"  {i}. {region}: ${revenue:,.2f}")
        
        print("\n=== 性能优化要点总结 ===")
        print("✓ 使用生成器处理大文件，减少内存占用")
        print("✓ 使用namedtuple优化数据结构内存")
        print("✓ 使用@lru_cache缓存重复计算")
        print("✓ 使用defaultdict简化字典操作")
        print("✓ 使用多线程并行处理独立任务")
        print("✓ 使用性能监控器跟踪优化效果")
        
    except Exception as e:
        print(f"执行过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理临时文件
        try:
            Path("sales_data.csv").unlink(missing_ok=True)
        except:
            pass


if __name__ == "__main__":
    main()