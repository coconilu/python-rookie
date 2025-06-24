#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session24 示例2：内存优化技术

本示例演示各种内存优化技术，包括生成器、__slots__、
内存分析和垃圾回收等。

作者: Python教程团队
创建日期: 2024-01-20
"""

import sys
import gc
import tracemalloc
from memory_profiler import profile


class RegularClass:
    """普通类（使用__dict__）"""
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.computed = x * y + z


class OptimizedClass:
    """优化类（使用__slots__）"""
    __slots__ = ['x', 'y', 'z', 'computed']
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.computed = x * y + z


def compare_class_memory():
    """比较普通类和优化类的内存使用"""
    print("\n=== 类内存优化比较 ===")
    
    # 创建单个实例比较
    regular_obj = RegularClass(1, 2, 3)
    optimized_obj = OptimizedClass(1, 2, 3)
    
    regular_size = sys.getsizeof(regular_obj) + sys.getsizeof(regular_obj.__dict__)
    optimized_size = sys.getsizeof(optimized_obj)
    
    print(f"单个实例内存比较:")
    print(f"  普通类: {regular_size} 字节")
    print(f"  __slots__类: {optimized_size} 字节")
    print(f"  内存节省: {regular_size - optimized_size} 字节 ({regular_size/optimized_size:.1f}倍)")
    
    # 创建大量实例比较
    n = 100000
    print(f"\n创建 {n:,} 个实例的内存比较:")
    
    # 测量普通类
    tracemalloc.start()
    regular_objects = [RegularClass(i, i+1, i+2) for i in range(n)]
    current, peak = tracemalloc.get_traced_memory()
    regular_memory = current
    tracemalloc.stop()
    
    # 清理内存
    del regular_objects
    gc.collect()
    
    # 测量优化类
    tracemalloc.start()
    optimized_objects = [OptimizedClass(i, i+1, i+2) for i in range(n)]
    current, peak = tracemalloc.get_traced_memory()
    optimized_memory = current
    tracemalloc.stop()
    
    print(f"  普通类总内存: {regular_memory / 1024 / 1024:.2f} MB")
    print(f"  __slots__类总内存: {optimized_memory / 1024 / 1024:.2f} MB")
    print(f"  内存节省: {(regular_memory - optimized_memory) / 1024 / 1024:.2f} MB")
    print(f"  节省比例: {(1 - optimized_memory/regular_memory)*100:.1f}%")
    
    del optimized_objects
    gc.collect()


def generator_vs_list():
    """比较生成器和列表的内存使用"""
    print("\n=== 生成器 vs 列表内存比较 ===")
    
    n = 1000000
    
    # 列表推导式
    print("创建列表...")
    list_data = [x**2 for x in range(n)]
    list_memory = sys.getsizeof(list_data)
    
    # 生成器表达式
    print("创建生成器...")
    gen_data = (x**2 for x in range(n))
    gen_memory = sys.getsizeof(gen_data)
    
    print(f"\n{n:,} 个平方数的内存使用:")
    print(f"  列表: {list_memory:,} 字节 ({list_memory/1024/1024:.2f} MB)")
    print(f"  生成器: {gen_memory:,} 字节")
    print(f"  内存节省: {list_memory//gen_memory:,} 倍")
    
    # 演示生成器的惰性计算
    print("\n生成器惰性计算演示:")
    
    def fibonacci_generator():
        """斐波那契数列生成器"""
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b
    
    # 只计算需要的值
    fib_gen = fibonacci_generator()
    first_20 = [next(fib_gen) for _ in range(20)]
    print(f"  前20个斐波那契数: {first_20}")
    print(f"  生成器内存: {sys.getsizeof(fib_gen)} 字节")
    
    # 如果用列表存储相同数量的斐波那契数
    fib_list = first_20.copy()
    print(f"  相同数据的列表内存: {sys.getsizeof(fib_list)} 字节")


def memory_efficient_data_processing():
    """内存高效的数据处理"""
    print("\n=== 内存高效的数据处理 ===")
    
    def process_large_dataset_memory_heavy():
        """内存密集型处理方式"""
        # 一次性加载所有数据
        data = list(range(1000000))
        filtered = [x for x in data if x % 2 == 0]
        squared = [x**2 for x in filtered]
        return sum(squared)
    
    def process_large_dataset_memory_light():
        """内存友好型处理方式"""
        # 使用生成器链式处理
        data = range(1000000)
        filtered = (x for x in data if x % 2 == 0)
        squared = (x**2 for x in filtered)
        return sum(squared)
    
    # 测量内存使用
    print("内存密集型处理:")
    tracemalloc.start()
    result1 = process_large_dataset_memory_heavy()
    current, peak = tracemalloc.get_traced_memory()
    memory1 = peak
    tracemalloc.stop()
    print(f"  结果: {result1}")
    print(f"  峰值内存: {memory1 / 1024 / 1024:.2f} MB")
    
    gc.collect()  # 清理内存
    
    print("\n内存友好型处理:")
    tracemalloc.start()
    result2 = process_large_dataset_memory_light()
    current, peak = tracemalloc.get_traced_memory()
    memory2 = peak
    tracemalloc.stop()
    print(f"  结果: {result2}")
    print(f"  峰值内存: {memory2 / 1024 / 1024:.2f} MB")
    
    print(f"\n内存节省: {(memory1 - memory2) / 1024 / 1024:.2f} MB")
    print(f"节省比例: {(1 - memory2/memory1)*100:.1f}%")
    print(f"结果相同: {result1 == result2}")


def demonstrate_weak_references():
    """演示弱引用的使用"""
    print("\n=== 弱引用演示 ===")
    
    import weakref
    
    class ExpensiveObject:
        """模拟昂贵的对象"""
        def __init__(self, data):
            self.data = data
            print(f"创建昂贵对象: {id(self)}")
        
        def __del__(self):
            print(f"销毁昂贵对象: {id(self)}")
    
    # 普通引用
    print("使用普通引用:")
    obj1 = ExpensiveObject("重要数据")
    cache = {'key1': obj1}  # 强引用
    del obj1  # 删除原始引用
    print(f"对象仍在缓存中: {'key1' in cache}")
    print(f"缓存中的对象: {cache['key1'].data}")
    
    # 清理强引用
    del cache
    gc.collect()
    
    print("\n使用弱引用:")
    obj2 = ExpensiveObject("重要数据2")
    weak_cache = {'key2': weakref.ref(obj2)}  # 弱引用
    
    # 检查弱引用是否还有效
    weak_ref = weak_cache['key2']
    if weak_ref() is not None:
        print(f"弱引用仍然有效: {weak_ref().data}")
    
    del obj2  # 删除原始引用
    gc.collect()  # 强制垃圾回收
    
    # 再次检查弱引用
    if weak_ref() is None:
        print("弱引用已失效，对象已被回收")


def memory_profiling_example():
    """内存分析示例"""
    print("\n=== 内存分析示例 ===")
    
    @profile
    def memory_intensive_function():
        """内存密集型函数"""
        # 创建大列表
        big_list = [i for i in range(100000)]
        
        # 创建字典
        big_dict = {i: i**2 for i in range(50000)}
        
        # 字符串操作
        big_string = ''.join(str(i) for i in range(10000))
        
        # 返回一些结果
        return len(big_list), len(big_dict), len(big_string)
    
    print("运行内存分析（需要安装memory_profiler）:")
    try:
        result = memory_intensive_function()
        print(f"函数执行结果: {result}")
    except NameError:
        print("memory_profiler未安装，跳过内存分析")
        print("可以使用: pip install memory_profiler")


def garbage_collection_demo():
    """垃圾回收演示"""
    print("\n=== 垃圾回收演示 ===")
    
    # 查看当前垃圾回收统计
    print("垃圾回收统计:")
    for i, count in enumerate(gc.get_count()):
        print(f"  第{i}代: {count} 个对象")
    
    # 创建循环引用
    class Node:
        def __init__(self, value):
            self.value = value
            self.ref = None
    
    print("\n创建循环引用:")
    node1 = Node(1)
    node2 = Node(2)
    node1.ref = node2
    node2.ref = node1  # 循环引用
    
    # 删除直接引用
    del node1, node2
    
    print("删除直接引用后的垃圾回收统计:")
    for i, count in enumerate(gc.get_count()):
        print(f"  第{i}代: {count} 个对象")
    
    # 手动触发垃圾回收
    collected = gc.collect()
    print(f"\n手动垃圾回收清理了 {collected} 个对象")
    
    print("垃圾回收后的统计:")
    for i, count in enumerate(gc.get_count()):
        print(f"  第{i}代: {count} 个对象")


def main():
    """主函数"""
    print("Session24 示例2: 内存优化技术")
    print("=" * 50)
    
    try:
        # 类内存优化
        compare_class_memory()
        
        # 生成器vs列表
        generator_vs_list()
        
        # 内存高效的数据处理
        memory_efficient_data_processing()
        
        # 弱引用演示
        demonstrate_weak_references()
        
        # 垃圾回收演示
        garbage_collection_demo()
        
        # 内存分析（可选）
        memory_profiling_example()
        
        print("\n=== 内存优化总结 ===")
        print("1. 使用__slots__减少类实例内存")
        print("2. 使用生成器进行惰性计算")
        print("3. 避免不必要的数据复制")
        print("4. 合理使用弱引用")
        print("5. 了解垃圾回收机制")
        print("6. 使用内存分析工具定位问题")
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()