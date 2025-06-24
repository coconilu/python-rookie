# Session24: 性能优化详细教程

## 1. 性能优化基础

### 1.1 什么是性能优化

性能优化是指通过改进算法、数据结构、代码实现等方式，提高程序的执行效率，减少资源消耗的过程。

### 1.2 性能优化的原则

1. **测量优先**：先测量，再优化
2. **找到瓶颈**：80%的时间花在20%的代码上
3. **权衡取舍**：性能 vs 可读性 vs 维护性
4. **避免过早优化**：Donald Knuth的名言

### 1.3 时间复杂度和空间复杂度

```python
# O(1) - 常数时间
def get_first_element(lst):
    return lst[0] if lst else None

# O(n) - 线性时间
def find_element(lst, target):
    for item in lst:
        if item == target:
            return True
    return False

# O(n²) - 平方时间
def bubble_sort(lst):
    n = len(lst)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst

# O(log n) - 对数时间
def binary_search(lst, target):
    left, right = 0, len(lst) - 1
    while left <= right:
        mid = (left + right) // 2
        if lst[mid] == target:
            return mid
        elif lst[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

## 2. Python性能分析工具

### 2.1 time模块 - 基础计时

```python
import time

def time_function(func, *args, **kwargs):
    """测量函数执行时间"""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    print(f"函数 {func.__name__} 执行时间: {end_time - start_time:.6f} 秒")
    return result

# 示例使用
def slow_function():
    time.sleep(0.1)
    return sum(range(1000000))

result = time_function(slow_function)
```

### 2.2 timeit模块 - 精确计时

```python
import timeit

# 测量简单语句
time_taken = timeit.timeit('sum(range(100))', number=10000)
print(f"执行时间: {time_taken:.6f} 秒")

# 测量函数
def test_function():
    return [i**2 for i in range(1000)]

time_taken = timeit.timeit(test_function, number=1000)
print(f"列表推导式执行时间: {time_taken:.6f} 秒")

# 比较不同实现
setup_code = "data = list(range(1000))"

# 方法1：列表推导式
method1 = "[x**2 for x in data]"
time1 = timeit.timeit(method1, setup=setup_code, number=1000)

# 方法2：map函数
method2 = "list(map(lambda x: x**2, data))"
time2 = timeit.timeit(method2, setup=setup_code, number=1000)

# 方法3：普通循环
method3 = """
result = []
for x in data:
    result.append(x**2)
"""
time3 = timeit.timeit(method3, setup=setup_code, number=1000)

print(f"列表推导式: {time1:.6f} 秒")
print(f"map函数: {time2:.6f} 秒")
print(f"普通循环: {time3:.6f} 秒")
```

### 2.3 cProfile - 详细性能分析

```python
import cProfile
import pstats
from io import StringIO

def profile_function(func, *args, **kwargs):
    """对函数进行详细性能分析"""
    pr = cProfile.Profile()
    pr.enable()
    
    result = func(*args, **kwargs)
    
    pr.disable()
    
    # 创建统计对象
    s = StringIO()
    ps = pstats.Stats(pr, stream=s)
    ps.sort_stats('cumulative')
    ps.print_stats(10)  # 显示前10个最耗时的函数
    
    print(s.getvalue())
    return result

# 示例：分析复杂函数
def complex_calculation():
    # 模拟复杂计算
    result = 0
    for i in range(100000):
        result += i ** 2
    
    # 模拟字符串操作
    text = ""
    for i in range(1000):
        text += str(i)
    
    return result, len(text)

profile_function(complex_calculation)
```

## 3. 算法优化技巧

### 3.1 选择合适的数据结构

```python
import time
from collections import deque, defaultdict

# 列表 vs 集合 - 查找操作
def compare_lookup():
    data_list = list(range(10000))
    data_set = set(range(10000))
    target = 9999
    
    # 列表查找 O(n)
    start = time.time()
    result1 = target in data_list
    time1 = time.time() - start
    
    # 集合查找 O(1)
    start = time.time()
    result2 = target in data_set
    time2 = time.time() - start
    
    print(f"列表查找时间: {time1:.8f} 秒")
    print(f"集合查找时间: {time2:.8f} 秒")
    print(f"性能提升: {time1/time2:.2f} 倍")

compare_lookup()

# 列表 vs 双端队列 - 插入操作
def compare_insertion():
    # 列表在开头插入 O(n)
    data_list = []
    start = time.time()
    for i in range(10000):
        data_list.insert(0, i)
    time1 = time.time() - start
    
    # 双端队列在开头插入 O(1)
    data_deque = deque()
    start = time.time()
    for i in range(10000):
        data_deque.appendleft(i)
    time2 = time.time() - start
    
    print(f"列表开头插入时间: {time1:.6f} 秒")
    print(f"双端队列开头插入时间: {time2:.6f} 秒")
    print(f"性能提升: {time1/time2:.2f} 倍")

compare_insertion()
```

### 3.2 字符串优化

```python
import time

# 字符串拼接优化
def string_concatenation_comparison():
    n = 10000
    
    # 方法1：使用 + 操作符 (低效)
    start = time.time()
    result1 = ""
    for i in range(n):
        result1 += str(i)
    time1 = time.time() - start
    
    # 方法2：使用列表和join (高效)
    start = time.time()
    parts = []
    for i in range(n):
        parts.append(str(i))
    result2 = "".join(parts)
    time2 = time.time() - start
    
    # 方法3：使用列表推导式和join (最高效)
    start = time.time()
    result3 = "".join(str(i) for i in range(n))
    time3 = time.time() - start
    
    print(f"+ 操作符: {time1:.6f} 秒")
    print(f"列表+join: {time2:.6f} 秒")
    print(f"生成器+join: {time3:.6f} 秒")
    
    print(f"方法2比方法1快: {time1/time2:.2f} 倍")
    print(f"方法3比方法1快: {time1/time3:.2f} 倍")

string_concatenation_comparison()
```

### 3.3 循环优化

```python
import time

# 循环优化技巧
def loop_optimization():
    data = list(range(100000))
    
    # 方法1：普通循环
    start = time.time()
    result1 = []
    for item in data:
        if item % 2 == 0:
            result1.append(item * 2)
    time1 = time.time() - start
    
    # 方法2：列表推导式
    start = time.time()
    result2 = [item * 2 for item in data if item % 2 == 0]
    time2 = time.time() - start
    
    # 方法3：filter + map
    start = time.time()
    result3 = list(map(lambda x: x * 2, filter(lambda x: x % 2 == 0, data)))
    time3 = time.time() - start
    
    print(f"普通循环: {time1:.6f} 秒")
    print(f"列表推导式: {time2:.6f} 秒")
    print(f"filter+map: {time3:.6f} 秒")
    
    print(f"列表推导式比普通循环快: {time1/time2:.2f} 倍")

loop_optimization()
```

## 4. 内存优化

### 4.1 生成器 vs 列表

```python
import sys

# 内存使用比较
def memory_comparison():
    n = 100000
    
    # 列表 - 占用大量内存
    list_data = [i**2 for i in range(n)]
    list_memory = sys.getsizeof(list_data)
    
    # 生成器 - 占用少量内存
    gen_data = (i**2 for i in range(n))
    gen_memory = sys.getsizeof(gen_data)
    
    print(f"列表内存使用: {list_memory:,} 字节")
    print(f"生成器内存使用: {gen_memory:,} 字节")
    print(f"内存节省: {list_memory/gen_memory:.2f} 倍")
    
    # 使用生成器进行惰性计算
    def fibonacci_generator():
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b
    
    # 只计算需要的值
    fib_gen = fibonacci_generator()
    first_10_fibs = [next(fib_gen) for _ in range(10)]
    print(f"前10个斐波那契数: {first_10_fibs}")

memory_comparison()
```

### 4.2 __slots__ 优化类内存

```python
import sys

# 普通类
class RegularPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 使用__slots__的类
class OptimizedPoint:
    __slots__ = ['x', 'y']
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 内存使用比较
regular_point = RegularPoint(1, 2)
optimized_point = OptimizedPoint(1, 2)

print(f"普通类实例大小: {sys.getsizeof(regular_point)} 字节")
print(f"优化类实例大小: {sys.getsizeof(optimized_point)} 字节")
print(f"普通类__dict__大小: {sys.getsizeof(regular_point.__dict__)} 字节")

# 创建大量实例的内存差异
import time

def create_points(point_class, n=100000):
    start_time = time.time()
    points = [point_class(i, i+1) for i in range(n)]
    end_time = time.time()
    return points, end_time - start_time

regular_points, regular_time = create_points(RegularPoint)
optimized_points, optimized_time = create_points(OptimizedPoint)

print(f"\n创建{len(regular_points):,}个普通类实例耗时: {regular_time:.4f} 秒")
print(f"创建{len(optimized_points):,}个优化类实例耗时: {optimized_time:.4f} 秒")
print(f"性能提升: {regular_time/optimized_time:.2f} 倍")
```

## 5. 并发优化

### 5.1 多线程处理I/O密集型任务

```python
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import requests

# 模拟I/O操作
def simulate_io_task(task_id):
    """模拟I/O密集型任务"""
    time.sleep(0.1)  # 模拟网络请求或文件读写
    return f"任务 {task_id} 完成"

# 串行执行
def sequential_execution():
    start_time = time.time()
    results = []
    for i in range(10):
        result = simulate_io_task(i)
        results.append(result)
    end_time = time.time()
    return results, end_time - start_time

# 并行执行
def parallel_execution():
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(simulate_io_task, i) for i in range(10)]
        results = [future.result() for future in futures]
    end_time = time.time()
    return results, end_time - start_time

# 比较性能
seq_results, seq_time = sequential_execution()
par_results, par_time = parallel_execution()

print(f"串行执行时间: {seq_time:.4f} 秒")
print(f"并行执行时间: {par_time:.4f} 秒")
print(f"性能提升: {seq_time/par_time:.2f} 倍")
```

### 5.2 多进程处理CPU密集型任务

```python
import time
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

# CPU密集型任务
def cpu_intensive_task(n):
    """计算密集型任务：计算素数"""
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True
    
    primes = [i for i in range(2, n) if is_prime(i)]
    return len(primes)

# 串行执行
def sequential_cpu_task():
    start_time = time.time()
    results = []
    for i in range(1000, 5000, 1000):
        result = cpu_intensive_task(i)
        results.append(result)
    end_time = time.time()
    return results, end_time - start_time

# 并行执行
def parallel_cpu_task():
    start_time = time.time()
    with ProcessPoolExecutor() as executor:
        tasks = range(1000, 5000, 1000)
        results = list(executor.map(cpu_intensive_task, tasks))
    end_time = time.time()
    return results, end_time - start_time

if __name__ == '__main__':
    seq_results, seq_time = sequential_cpu_task()
    par_results, par_time = parallel_cpu_task()
    
    print(f"串行CPU任务时间: {seq_time:.4f} 秒")
    print(f"并行CPU任务时间: {par_time:.4f} 秒")
    print(f"性能提升: {seq_time/par_time:.2f} 倍")
```

## 6. 缓存优化

### 6.1 使用functools.lru_cache

```python
import time
from functools import lru_cache

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

# 性能比较
def compare_fibonacci():
    n = 35
    
    # 不使用缓存
    start = time.time()
    result1 = fibonacci_no_cache(n)
    time1 = time.time() - start
    
    # 使用缓存
    start = time.time()
    result2 = fibonacci_with_cache(n)
    time2 = time.time() - start
    
    print(f"fibonacci({n}) = {result1}")
    print(f"不使用缓存: {time1:.6f} 秒")
    print(f"使用缓存: {time2:.6f} 秒")
    print(f"性能提升: {time1/time2:.2f} 倍")
    
    # 查看缓存信息
    print(f"缓存信息: {fibonacci_with_cache.cache_info()}")

compare_fibonacci()
```

## 7. 实际优化案例

### 7.1 数据处理优化

```python
import time
import pandas as pd
import numpy as np

# 创建测试数据
def create_test_data(n=100000):
    return {
        'id': range(n),
        'value': np.random.randint(1, 1000, n),
        'category': np.random.choice(['A', 'B', 'C'], n)
    }

# 方法1：使用纯Python
def process_data_python(data):
    start = time.time()
    
    # 过滤和计算
    filtered_data = []
    for i, (id_val, value, category) in enumerate(zip(data['id'], data['value'], data['category'])):
        if value > 500 and category == 'A':
            filtered_data.append({
                'id': id_val,
                'value': value,
                'processed_value': value * 1.1
            })
    
    # 计算统计信息
    total = sum(item['processed_value'] for item in filtered_data)
    avg = total / len(filtered_data) if filtered_data else 0
    
    end = time.time()
    return len(filtered_data), avg, end - start

# 方法2：使用pandas
def process_data_pandas(data):
    start = time.time()
    
    df = pd.DataFrame(data)
    
    # 过滤和计算
    filtered_df = df[(df['value'] > 500) & (df['category'] == 'A')].copy()
    filtered_df['processed_value'] = filtered_df['value'] * 1.1
    
    # 计算统计信息
    count = len(filtered_df)
    avg = filtered_df['processed_value'].mean() if count > 0 else 0
    
    end = time.time()
    return count, avg, end - start

# 方法3：使用numpy
def process_data_numpy(data):
    start = time.time()
    
    # 转换为numpy数组
    values = np.array(data['value'])
    categories = np.array(data['category'])
    ids = np.array(data['id'])
    
    # 创建过滤条件
    mask = (values > 500) & (categories == 'A')
    
    # 应用过滤
    filtered_values = values[mask]
    processed_values = filtered_values * 1.1
    
    # 计算统计信息
    count = len(processed_values)
    avg = np.mean(processed_values) if count > 0 else 0
    
    end = time.time()
    return count, avg, end - start

# 性能比较
test_data = create_test_data()

count1, avg1, time1 = process_data_python(test_data)
count2, avg2, time2 = process_data_pandas(test_data)
count3, avg3, time3 = process_data_numpy(test_data)

print(f"纯Python: 处理{count1}条记录，平均值{avg1:.2f}，耗时{time1:.4f}秒")
print(f"Pandas: 处理{count2}条记录，平均值{avg2:.2f}，耗时{time2:.4f}秒")
print(f"NumPy: 处理{count3}条记录，平均值{avg3:.2f}，耗时{time3:.4f}秒")

print(f"\nPandas比Python快: {time1/time2:.2f}倍")
print(f"NumPy比Python快: {time1/time3:.2f}倍")
```

## 8. 性能优化最佳实践

### 8.1 优化检查清单

1. **算法层面**
   - 选择合适的算法和数据结构
   - 减少时间复杂度
   - 避免不必要的计算

2. **代码层面**
   - 使用内置函数和库
   - 避免全局变量查找
   - 使用局部变量缓存

3. **内存层面**
   - 使用生成器代替列表
   - 及时释放不需要的对象
   - 使用__slots__优化类

4. **I/O层面**
   - 批量处理数据
   - 使用缓存减少I/O操作
   - 异步处理I/O密集型任务

### 8.2 性能测试模板

```python
import time
import functools

def performance_test(func):
    """性能测试装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 执行时间: {end_time - start_time:.6f} 秒")
        return result
    return wrapper

# 使用示例
@performance_test
def example_function():
    return sum(i**2 for i in range(100000))

result = example_function()
```

## 总结

性能优化是一个系统性的工程，需要：

1. **正确的心态**：先保证正确性，再考虑性能
2. **科学的方法**：基于测量数据，不凭主观感受
3. **合适的工具**：选择正确的分析和优化工具
4. **平衡的考虑**：性能、可读性、维护性的平衡

记住："过早优化是万恶之源"，但适时的优化能让你的程序飞起来！

## 扩展阅读

- [Python Performance Tips](https://wiki.python.org/moin/PythonSpeed/PerformanceTips)
- [High Performance Python](https://www.oreilly.com/library/view/high-performance-python/9781449361747/)
- [Python Profiling](https://docs.python.org/3/library/profile.html)
- [NumPy Performance](https://numpy.org/doc/stable/user/basics.performance.html)