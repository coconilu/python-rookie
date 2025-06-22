#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session 06: 函数编程 - 练习2答案：高级函数特性

这个文件包含了函数编程高级特性练习的完整答案实现。
包括Lambda函数、高阶函数、装饰器、递归、闭包和函数式编程技巧。

作者: Python教程团队
创建日期: 2024-12-22
"""

from typing import List, Callable, Any, Dict, Tuple
from functools import wraps
import time
import inspect


# ==================== Lambda函数练习答案 ====================

def lambda_exercises():
    """
    Lambda函数练习答案
    """
    print("Lambda函数练习")
    print("-" * 30)
    
    # 练习1: 创建一个lambda函数，计算两个数的和
    add_lambda = lambda x, y: x + y
    
    # 练习2: 创建一个lambda函数，判断数字是否为偶数
    is_even_lambda = lambda x: x % 2 == 0
    
    # 练习3: 创建一个lambda函数，将字符串转换为大写
    to_upper_lambda = lambda s: s.upper()
    
    # 练习4: 使用lambda函数对列表进行排序
    students = [('Alice', 85), ('Bob', 90), ('Charlie', 78), ('Diana', 92)]
    # 按成绩从高到低排序
    sorted_by_score = sorted(students, key=lambda student: student[1], reverse=True)
    
    # 练习5: 使用lambda函数过滤列表
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # 过滤出大于5的数字
    filtered_numbers = list(filter(lambda x: x > 5, numbers))
    
    # 练习6: 使用lambda函数转换列表
    words = ['hello', 'world', 'python', 'programming']
    # 将所有单词转换为大写并添加感叹号
    transformed_words = list(map(lambda word: word.upper() + '!', words))
    
    # 测试代码
    try:
        assert add_lambda(3, 5) == 8, "add_lambda测试失败"
        print("✓ add_lambda测试通过")
        
        assert is_even_lambda(4) == True, "is_even_lambda测试失败"
        assert is_even_lambda(5) == False, "is_even_lambda测试失败"
        print("✓ is_even_lambda测试通过")
        
        assert to_upper_lambda("hello") == "HELLO", "to_upper_lambda测试失败"
        print("✓ to_upper_lambda测试通过")
        
        expected = [('Diana', 92), ('Bob', 90), ('Alice', 85), ('Charlie', 78)]
        assert sorted_by_score == expected, "sorted_by_score测试失败"
        print("✓ sorted_by_score测试通过")
        
        assert filtered_numbers == [6, 7, 8, 9, 10], "filtered_numbers测试失败"
        print("✓ filtered_numbers测试通过")
        
        expected = ['HELLO!', 'WORLD!', 'PYTHON!', 'PROGRAMMING!']
        assert transformed_words == expected, "transformed_words测试失败"
        print("✓ transformed_words测试通过")
    
    except Exception as e:
        print(f"❌ 测试失败: {e}")


# ==================== 高阶函数练习答案 ====================

def higher_order_functions_exercises():
    """
    高阶函数练习答案
    """
    print("\n高阶函数练习")
    print("-" * 30)
    
    # 练习1: 实现一个apply_operation函数，接受一个函数和两个数字
    def apply_operation(func: Callable, a: float, b: float) -> float:
        """
        应用操作函数到两个数字上
        """
        return func(a, b)
    
    # 练习2: 实现一个create_multiplier函数，返回一个乘法函数
    def create_multiplier(factor: float) -> Callable:
        """
        创建一个乘法器函数
        """
        def multiplier(value):
            return value * factor
        return multiplier
    
    # 练习3: 实现一个filter_and_transform函数
    def filter_and_transform(data: List[Any], filter_func: Callable, 
                           transform_func: Callable) -> List[Any]:
        """
        先过滤再转换数据
        """
        filtered_data = filter(filter_func, data)
        return list(map(transform_func, filtered_data))
    
    # 练习4: 实现一个compose函数，组合两个函数
    def compose(func1: Callable, func2: Callable) -> Callable:
        """
        组合两个函数 - func1(func2(x))
        """
        def composed_function(x):
            return func1(func2(x))
        return composed_function
    
    # 练习5: 实现一个reduce_list函数（类似内置的reduce）
    def reduce_list(func: Callable, data: List[Any], initial=None) -> Any:
        """
        对列表进行归约操作
        """
        if not data:
            return initial
        
        iterator = iter(data)
        if initial is None:
            result = next(iterator)
        else:
            result = initial
        
        for item in iterator:
            result = func(result, item)
        
        return result
    
    # 测试代码
    try:
        # 测试apply_operation
        result1 = apply_operation(lambda x, y: x + y, 3, 5)
        assert result1 == 8, "apply_operation测试失败"
        print("✓ apply_operation测试通过")
        
        # 测试create_multiplier
        double = create_multiplier(2)
        triple = create_multiplier(3)
        assert double(5) == 10, "create_multiplier测试失败"
        assert triple(4) == 12, "create_multiplier测试失败"
        print("✓ create_multiplier测试通过")
        
        # 测试filter_and_transform
        numbers = [1, 2, 3, 4, 5, 6]
        result2 = filter_and_transform(numbers, lambda x: x % 2 == 0, lambda x: x ** 2)
        assert result2 == [4, 16, 36], "filter_and_transform测试失败"
        print("✓ filter_and_transform测试通过")
        
        # 测试compose
        add_one = lambda x: x + 1
        multiply_two = lambda x: x * 2
        composed = compose(multiply_two, add_one)
        assert composed(3) == 8, "compose测试失败"  # (3 + 1) * 2 = 8
        print("✓ compose测试通过")
        
        # 测试reduce_list
        numbers = [1, 2, 3, 4, 5]
        sum_result = reduce_list(lambda x, y: x + y, numbers, 0)
        assert sum_result == 15, "reduce_list测试失败"
        print("✓ reduce_list测试通过")
    
    except Exception as e:
        print(f"❌ 测试失败: {e}")


# ==================== 装饰器练习答案 ====================

def decorator_exercises():
    """
    装饰器练习答案
    """
    print("\n装饰器练习")
    print("-" * 30)
    
    # 练习1: 实现一个计时装饰器
    def timer(func):
        """
        计时装饰器
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f"函数 {func.__name__} 执行时间: {end_time - start_time:.4f}秒")
            return result
        return wrapper
    
    # 练习2: 实现一个重试装饰器
    def retry(max_attempts=3):
        """
        重试装饰器工厂
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                last_exception = None
                for attempt in range(max_attempts):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        last_exception = e
                        print(f"第 {attempt + 1} 次尝试失败: {e}")
                        if attempt == max_attempts - 1:
                            raise last_exception
                return None
            return wrapper
        return decorator
    
    # 练习3: 实现一个缓存装饰器
    def memoize(func):
        """
        缓存装饰器
        """
        cache = {}
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 创建缓存键
            key = str(args) + str(sorted(kwargs.items()))
            
            if key in cache:
                print(f"缓存命中: {func.__name__}")
                return cache[key]
            
            result = func(*args, **kwargs)
            cache[key] = result
            return result
        
        return wrapper
    
    # 练习4: 实现一个参数验证装饰器
    def validate_types(*types):
        """
        参数类型验证装饰器工厂
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # 验证位置参数类型
                for i, (arg, expected_type) in enumerate(zip(args, types)):
                    if not isinstance(arg, expected_type):
                        raise TypeError(f"参数 {i+1} 应该是 {expected_type.__name__} 类型，但得到了 {type(arg).__name__}")
                
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    # 练习5: 实现一个日志装饰器
    def log_calls(func):
        """
        函数调用日志装饰器
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"调用函数: {func.__name__}")
            print(f"参数: args={args}, kwargs={kwargs}")
            result = func(*args, **kwargs)
            print(f"返回值: {result}")
            return result
        return wrapper
    
    # 测试函数
    @timer
    def slow_function():
        time.sleep(0.1)
        return "完成"
    
    @retry(max_attempts=2)
    def unreliable_function(should_fail=True):
        if should_fail:
            raise ValueError("模拟错误")
        return "成功"
    
    @memoize
    def fibonacci(n):
        if n < 2:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    @validate_types(int, int)
    def add_numbers(a, b):
        return a + b
    
    @log_calls
    def greet(name):
        return f"Hello, {name}!"
    
    # 测试代码
    try:
        # 测试timer装饰器
        result = slow_function()
        print("✓ timer装饰器测试通过")
        
        # 测试memoize装饰器
        fib_result = fibonacci(10)
        assert fib_result == 55, "memoize装饰器测试失败"
        print("✓ memoize装饰器测试通过")
        
        # 测试validate_types装饰器
        add_result = add_numbers(3, 5)
        assert add_result == 8, "validate_types装饰器测试失败"
        print("✓ validate_types装饰器测试通过")
        
        # 测试log_calls装饰器
        greet_result = greet("Alice")
        assert greet_result == "Hello, Alice!", "log_calls装饰器测试失败"
        print("✓ log_calls装饰器测试通过")
    
    except Exception as e:
        print(f"❌ 测试失败: {e}")


# ==================== 递归练习答案 ====================

def recursion_exercises():
    """
    递归练习答案
    """
    print("\n递归练习")
    print("-" * 30)
    
    # 练习1: 实现阶乘函数
    def factorial(n: int) -> int:
        """
        计算阶乘
        """
        if n < 0:
            raise ValueError("阶乘不能计算负数")
        if n == 0 or n == 1:
            return 1
        return n * factorial(n - 1)
    
    # 练习2: 实现斐波那契数列
    def fibonacci_recursive(n: int) -> int:
        """
        递归计算斐波那契数列
        """
        if n < 0:
            raise ValueError("斐波那契数列不能计算负数")
        if n < 2:
            return n
        return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)
    
    # 练习3: 实现二分查找
    def binary_search(arr: List[int], target: int, left: int = 0, right: int = None) -> int:
        """
        递归二分查找
        """
        if right is None:
            right = len(arr) - 1
        
        if left > right:
            return -1
        
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] > target:
            return binary_search(arr, target, left, mid - 1)
        else:
            return binary_search(arr, target, mid + 1, right)
    
    # 练习4: 实现快速排序
    def quick_sort(arr: List[int]) -> List[int]:
        """
        递归快速排序
        """
        if len(arr) <= 1:
            return arr
        
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        
        return quick_sort(left) + middle + quick_sort(right)
    
    # 练习5: 实现汉诺塔问题
    def hanoi_tower(n: int, source: str, target: str, auxiliary: str) -> List[str]:
        """
        汉诺塔问题求解
        """
        if n == 1:
            return [f"移动盘子从 {source} 到 {target}"]
        
        moves = []
        # 将前n-1个盘子从源柱移到辅助柱
        moves.extend(hanoi_tower(n - 1, source, auxiliary, target))
        # 将最大的盘子从源柱移到目标柱
        moves.append(f"移动盘子从 {source} 到 {target}")
        # 将前n-1个盘子从辅助柱移到目标柱
        moves.extend(hanoi_tower(n - 1, auxiliary, target, source))
        
        return moves
    
    # 练习6: 实现目录遍历（模拟）
    def traverse_directory(directory: Dict[str, Any], level: int = 0) -> List[str]:
        """
        递归遍历目录结构
        """
        result = []
        indent = "  " * level
        
        for name, content in directory.items():
            if content is None:
                # 文件
                result.append(f"{indent}{name} (文件)")
            else:
                # 目录
                result.append(f"{indent}{name}/ (目录)")
                result.extend(traverse_directory(content, level + 1))
        
        return result
    
    # 测试代码
    try:
        # 测试factorial
        assert factorial(5) == 120, "factorial测试失败"
        assert factorial(0) == 1, "factorial测试失败"
        print("✓ factorial测试通过")
        
        # 测试fibonacci_recursive
        assert fibonacci_recursive(10) == 55, "fibonacci_recursive测试失败"
        assert fibonacci_recursive(0) == 0, "fibonacci_recursive测试失败"
        print("✓ fibonacci_recursive测试通过")
        
        # 测试binary_search
        sorted_arr = [1, 3, 5, 7, 9, 11, 13, 15]
        assert binary_search(sorted_arr, 7) == 3, "binary_search测试失败"
        assert binary_search(sorted_arr, 16) == -1, "binary_search测试失败"
        print("✓ binary_search测试通过")
        
        # 测试quick_sort
        unsorted_arr = [64, 34, 25, 12, 22, 11, 90]
        sorted_result = quick_sort(unsorted_arr)
        assert sorted_result == [11, 12, 22, 25, 34, 64, 90], "quick_sort测试失败"
        print("✓ quick_sort测试通过")
        
        # 测试hanoi_tower
        hanoi_result = hanoi_tower(3, 'A', 'C', 'B')
        assert len(hanoi_result) == 7, "hanoi_tower测试失败"
        print("✓ hanoi_tower测试通过")
        
        # 测试traverse_directory
        test_dir = {
            'root': {
                'file1.txt': None,
                'folder1': {
                    'file2.txt': None,
                    'subfolder': {
                        'file3.txt': None
                    }
                },
                'file4.txt': None
            }
        }
        traverse_result = traverse_directory(test_dir)
        assert len(traverse_result) > 0, "traverse_directory测试失败"
        print("✓ traverse_directory测试通过")
    
    except Exception as e:
        print(f"❌ 测试失败: {e}")


# ==================== 闭包练习答案 ====================

def closure_exercises():
    """
    闭包练习答案
    """
    print("\n闭包练习")
    print("-" * 30)
    
    # 练习1: 实现一个计数器闭包
    def create_counter(initial_value: int = 0) -> Callable:
        """
        创建计数器闭包
        """
        count = initial_value
        
        def counter():
            nonlocal count
            count += 1
            return count
        
        return counter
    
    # 练习2: 实现一个累加器闭包
    def create_accumulator() -> Callable:
        """
        创建累加器闭包
        """
        total = 0
        
        def accumulator(value):
            nonlocal total
            total += value
            return total
        
        return accumulator
    
    # 练习3: 实现一个配置管理器闭包
    def create_config_manager(default_config: Dict[str, Any]) -> Tuple[Callable, Callable]:
        """
        创建配置管理器闭包
        """
        config = default_config.copy()
        
        def get_config(key):
            return config.get(key)
        
        def set_config(key, value):
            config[key] = value
        
        return get_config, set_config
    
    # 练习4: 实现一个函数工厂闭包
    def create_math_operation(operation: str) -> Callable:
        """
        创建数学运算函数
        """
        def math_function(a, b):
            if operation == 'add':
                return a + b
            elif operation == 'multiply':
                return a * b
            elif operation == 'power':
                return a ** b
            else:
                raise ValueError(f"不支持的运算: {operation}")
        
        return math_function
    
    # 练习5: 实现一个状态机闭包
    def create_state_machine(states: List[str], initial_state: str) -> Tuple[Callable, Callable]:
        """
        创建状态机闭包
        """
        if initial_state not in states:
            raise ValueError(f"初始状态 {initial_state} 不在状态列表中")
        
        current_state = initial_state
        
        def get_state():
            return current_state
        
        def set_state(new_state):
            nonlocal current_state
            if new_state not in states:
                raise ValueError(f"状态 {new_state} 不在状态列表中")
            current_state = new_state
        
        return get_state, set_state
    
    # 测试代码
    try:
        # 测试create_counter
        counter = create_counter(10)
        assert counter() == 11, "create_counter测试失败"
        assert counter() == 12, "create_counter测试失败"
        print("✓ create_counter测试通过")
        
        # 测试create_accumulator
        accumulator = create_accumulator()
        assert accumulator(5) == 5, "create_accumulator测试失败"
        assert accumulator(3) == 8, "create_accumulator测试失败"
        print("✓ create_accumulator测试通过")
        
        # 测试create_config_manager
        get_config, set_config = create_config_manager({'theme': 'dark', 'language': 'en'})
        assert get_config('theme') == 'dark', "create_config_manager测试失败"
        set_config('theme', 'light')
        assert get_config('theme') == 'light', "create_config_manager测试失败"
        print("✓ create_config_manager测试通过")
        
        # 测试create_math_operation
        add_func = create_math_operation('add')
        multiply_func = create_math_operation('multiply')
        assert add_func(3, 5) == 8, "create_math_operation测试失败"
        assert multiply_func(3, 5) == 15, "create_math_operation测试失败"
        print("✓ create_math_operation测试通过")
        
        # 测试create_state_machine
        get_state, set_state = create_state_machine(['idle', 'running', 'stopped'], 'idle')
        assert get_state() == 'idle', "create_state_machine测试失败"
        set_state('running')
        assert get_state() == 'running', "create_state_machine测试失败"
        print("✓ create_state_machine测试通过")
    
    except Exception as e:
        print(f"❌ 测试失败: {e}")


# ==================== 函数式编程技巧练习答案 ====================

def functional_programming_exercises():
    """
    函数式编程技巧练习答案
    """
    print("\n函数式编程技巧练习")
    print("-" * 30)
    
    # 练习1: 实现map函数的自定义版本
    def custom_map(func: Callable, iterable) -> List[Any]:
        """
        自定义map函数
        """
        result = []
        for item in iterable:
            result.append(func(item))
        return result
    
    # 练习2: 实现filter函数的自定义版本
    def custom_filter(func: Callable, iterable) -> List[Any]:
        """
        自定义filter函数
        """
        result = []
        for item in iterable:
            if func(item):
                result.append(item)
        return result
    
    # 练习3: 实现函数管道
    def pipe(*functions):
        """
        创建函数管道
        """
        def pipeline(value):
            result = value
            for func in functions:
                result = func(result)
            return result
        return pipeline
    
    # 练习4: 实现柯里化函数
    def curry(func: Callable, arity: int = None) -> Callable:
        """
        柯里化函数
        """
        if arity is None:
            arity = func.__code__.co_argcount
        
        def curried(*args):
            if len(args) >= arity:
                return func(*args[:arity])
            else:
                def partial_func(*more_args):
                    return curried(*(args + more_args))
                return partial_func
        
        return curried
    
    # 练习5: 实现偏函数应用
    def partial(func: Callable, *args, **kwargs) -> Callable:
        """
        偏函数应用
        """
        def partial_func(*more_args, **more_kwargs):
            combined_kwargs = {**kwargs, **more_kwargs}
            return func(*(args + more_args), **combined_kwargs)
        
        return partial_func
    
    # 练习6: 实现函数组合器
    def compose_all(*functions):
        """
        组合多个函数（从右到左）
        """
        def composed(value):
            result = value
            for func in reversed(functions):
                result = func(result)
            return result
        return composed
    
    # 测试代码
    try:
        # 测试custom_map
        numbers = [1, 2, 3, 4, 5]
        mapped_result = custom_map(lambda x: x * 2, numbers)
        assert mapped_result == [2, 4, 6, 8, 10], "custom_map测试失败"
        print("✓ custom_map测试通过")
        
        # 测试custom_filter
        filtered_result = custom_filter(lambda x: x % 2 == 0, numbers)
        assert filtered_result == [2, 4], "custom_filter测试失败"
        print("✓ custom_filter测试通过")
        
        # 测试pipe
        pipeline = pipe(
            lambda x: x + 1,
            lambda x: x * 2,
            lambda x: x - 3
        )
        pipe_result = pipeline(5)
        assert pipe_result == 9, "pipe测试失败"  # (5+1)*2-3 = 9
        print("✓ pipe测试通过")
        
        # 测试curry
        def add_three(a, b, c):
            return a + b + c
        
        curried_add = curry(add_three, 3)
        result = curried_add(1)(2)(3)
        assert result == 6, "curry测试失败"
        print("✓ curry测试通过")
        
        # 测试partial
        def multiply(a, b, c):
            return a * b * c
        
        partial_multiply = partial(multiply, 2, 3)
        partial_result = partial_multiply(4)
        assert partial_result == 24, "partial测试失败"
        print("✓ partial测试通过")
        
        # 测试compose_all
        composed = compose_all(
            lambda x: x + 1,
            lambda x: x * 2,
            lambda x: x ** 2
        )
        compose_result = composed(3)  # 3^2 = 9, 9*2 = 18, 18+1 = 19
        assert compose_result == 19, "compose_all测试失败"
        print("✓ compose_all测试通过")
    
    except Exception as e:
        print(f"❌ 测试失败: {e}")


# ==================== 主程序 ====================

def main():
    """
    主程序：运行所有练习答案
    """
    print("Session 06: 函数编程 - 高级特性练习答案")
    print("=" * 50)
    print("这是练习2的完整答案实现，展示了函数编程的高级特性。")
    print("=" * 50)
    
    # 运行所有练习答案
    lambda_exercises()
    higher_order_functions_exercises()
    decorator_exercises()
    recursion_exercises()
    closure_exercises()
    functional_programming_exercises()
    
    print("\n" + "=" * 50)
    print("所有练习答案演示完成！")
    print("\n学习要点总结:")
    print("1. Lambda函数：简洁的匿名函数，适用于简单操作")
    print("2. 高阶函数：接受或返回函数的函数，提高代码复用性")
    print("3. 装饰器：在不修改原函数的情况下增加功能")
    print("4. 递归：函数调用自身，适用于分治问题")
    print("5. 闭包：内部函数访问外部函数变量，实现数据封装")
    print("6. 函数式编程：使用函数组合解决复杂问题")
    print("\n继续学习更多高级主题，如异步编程、元编程等！")


if __name__ == "__main__":
    main()