#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session 06: 函数编程 - 练习2：高级函数特性

这个练习文件包含了函数编程的高级特性练习，包括：
- Lambda函数
- 高阶函数
- 装饰器
- 递归
- 闭包
- 函数式编程技巧

完成这些练习将帮助你掌握Python函数编程的高级概念。

作者: Python教程团队
创建日期: 2024-12-22
"""

from typing import List, Callable, Any, Dict, Tuple
from functools import wraps
import time


# ==================== Lambda函数练习 ====================

def lambda_exercises():
    """
    Lambda函数练习
    """
    print("Lambda函数练习")
    print("-" * 30)
    
    # 练习1: 创建一个lambda函数，计算两个数的和
    # TODO: 创建add_lambda函数
    add_lambda = None  # 在这里实现
    
    # 练习2: 创建一个lambda函数，判断数字是否为偶数
    # TODO: 创建is_even_lambda函数
    is_even_lambda = None  # 在这里实现
    
    # 练习3: 创建一个lambda函数，将字符串转换为大写
    # TODO: 创建to_upper_lambda函数
    to_upper_lambda = None  # 在这里实现
    
    # 练习4: 使用lambda函数对列表进行排序
    students = [('Alice', 85), ('Bob', 90), ('Charlie', 78), ('Diana', 92)]
    # TODO: 按成绩从高到低排序
    sorted_by_score = None  # 在这里实现
    
    # 练习5: 使用lambda函数过滤列表
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # TODO: 过滤出大于5的数字
    filtered_numbers = None  # 在这里实现
    
    # 练习6: 使用lambda函数转换列表
    words = ['hello', 'world', 'python', 'programming']
    # TODO: 将所有单词转换为大写并添加感叹号
    transformed_words = None  # 在这里实现
    
    # 测试代码（不要修改）
    try:
        if add_lambda:
            assert add_lambda(3, 5) == 8, "add_lambda测试失败"
            print("✓ add_lambda测试通过")
        
        if is_even_lambda:
            assert is_even_lambda(4) == True, "is_even_lambda测试失败"
            assert is_even_lambda(5) == False, "is_even_lambda测试失败"
            print("✓ is_even_lambda测试通过")
        
        if to_upper_lambda:
            assert to_upper_lambda("hello") == "HELLO", "to_upper_lambda测试失败"
            print("✓ to_upper_lambda测试通过")
        
        if sorted_by_score:
            expected = [('Diana', 92), ('Bob', 90), ('Alice', 85), ('Charlie', 78)]
            assert sorted_by_score == expected, "sorted_by_score测试失败"
            print("✓ sorted_by_score测试通过")
        
        if filtered_numbers:
            assert filtered_numbers == [6, 7, 8, 9, 10], "filtered_numbers测试失败"
            print("✓ filtered_numbers测试通过")
        
        if transformed_words:
            expected = ['HELLO!', 'WORLD!', 'PYTHON!', 'PROGRAMMING!']
            assert transformed_words == expected, "transformed_words测试失败"
            print("✓ transformed_words测试通过")
    
    except Exception as e:
        print(f"❌ 测试失败: {e}")


# ==================== 高阶函数练习 ====================

def higher_order_functions_exercises():
    """
    高阶函数练习
    """
    print("\n高阶函数练习")
    print("-" * 30)
    
    # 练习1: 实现一个apply_operation函数，接受一个函数和两个数字
    def apply_operation(func: Callable, a: float, b: float) -> float:
        """
        应用操作函数到两个数字上
        
        参数:
            func: 操作函数
            a: 第一个数字
            b: 第二个数字
        
        返回:
            float: 操作结果
        """
        # TODO: 在这里实现
        pass
    
    # 练习2: 实现一个create_multiplier函数，返回一个乘法函数
    def create_multiplier(factor: float) -> Callable:
        """
        创建一个乘法器函数
        
        参数:
            factor: 乘数
        
        返回:
            function: 乘法函数
        """
        # TODO: 在这里实现
        pass
    
    # 练习3: 实现一个filter_and_transform函数
    def filter_and_transform(data: List[Any], filter_func: Callable, 
                           transform_func: Callable) -> List[Any]:
        """
        先过滤再转换数据
        
        参数:
            data: 数据列表
            filter_func: 过滤函数
            transform_func: 转换函数
        
        返回:
            list: 处理后的数据
        """
        # TODO: 在这里实现
        pass
    
    # 练习4: 实现一个compose函数，组合两个函数
    def compose(func1: Callable, func2: Callable) -> Callable:
        """
        组合两个函数
        
        参数:
            func1: 第一个函数
            func2: 第二个函数
        
        返回:
            function: 组合后的函数
        """
        # TODO: 在这里实现
        pass
    
    # 练习5: 实现一个reduce_list函数（类似内置的reduce）
    def reduce_list(func: Callable, data: List[Any], initial=None) -> Any:
        """
        对列表进行归约操作
        
        参数:
            func: 归约函数
            data: 数据列表
            initial: 初始值
        
        返回:
            Any: 归约结果
        """
        # TODO: 在这里实现
        pass
    
    # 测试代码（不要修改）
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


# ==================== 装饰器练习 ====================

def decorator_exercises():
    """
    装饰器练习
    """
    print("\n装饰器练习")
    print("-" * 30)
    
    # 练习1: 实现一个计时装饰器
    def timer(func):
        """
        计时装饰器
        """
        # TODO: 在这里实现
        pass
    
    # 练习2: 实现一个重试装饰器
    def retry(max_attempts=3):
        """
        重试装饰器工厂
        
        参数:
            max_attempts: 最大重试次数
        """
        def decorator(func):
            # TODO: 在这里实现
            pass
        return decorator
    
    # 练习3: 实现一个缓存装饰器
    def memoize(func):
        """
        缓存装饰器
        """
        # TODO: 在这里实现
        pass
    
    # 练习4: 实现一个参数验证装饰器
    def validate_types(*types):
        """
        参数类型验证装饰器工厂
        
        参数:
            *types: 期望的参数类型
        """
        def decorator(func):
            # TODO: 在这里实现
            pass
        return decorator
    
    # 练习5: 实现一个日志装饰器
    def log_calls(func):
        """
        函数调用日志装饰器
        """
        # TODO: 在这里实现
        pass
    
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
    
    # 测试代码（不要修改）
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


# ==================== 递归练习 ====================

def recursion_exercises():
    """
    递归练习
    """
    print("\n递归练习")
    print("-" * 30)
    
    # 练习1: 实现阶乘函数
    def factorial(n: int) -> int:
        """
        计算阶乘
        
        参数:
            n: 非负整数
        
        返回:
            int: n的阶乘
        """
        # TODO: 在这里实现
        pass
    
    # 练习2: 实现斐波那契数列
    def fibonacci_recursive(n: int) -> int:
        """
        递归计算斐波那契数列
        
        参数:
            n: 位置索引
        
        返回:
            int: 第n个斐波那契数
        """
        # TODO: 在这里实现
        pass
    
    # 练习3: 实现二分查找
    def binary_search(arr: List[int], target: int, left: int = 0, right: int = None) -> int:
        """
        递归二分查找
        
        参数:
            arr: 已排序的数组
            target: 目标值
            left: 左边界
            right: 右边界
        
        返回:
            int: 目标值的索引，未找到返回-1
        """
        # TODO: 在这里实现
        pass
    
    # 练习4: 实现快速排序
    def quick_sort(arr: List[int]) -> List[int]:
        """
        递归快速排序
        
        参数:
            arr: 待排序数组
        
        返回:
            list: 排序后的数组
        """
        # TODO: 在这里实现
        pass
    
    # 练习5: 实现汉诺塔问题
    def hanoi_tower(n: int, source: str, target: str, auxiliary: str) -> List[str]:
        """
        汉诺塔问题求解
        
        参数:
            n: 盘子数量
            source: 源柱子
            target: 目标柱子
            auxiliary: 辅助柱子
        
        返回:
            list: 移动步骤列表
        """
        # TODO: 在这里实现
        pass
    
    # 练习6: 实现目录遍历（模拟）
    def traverse_directory(directory: Dict[str, Any], level: int = 0) -> List[str]:
        """
        递归遍历目录结构
        
        参数:
            directory: 目录结构字典
            level: 当前层级
        
        返回:
            list: 遍历结果列表
        """
        # TODO: 在这里实现
        pass
    
    # 测试代码（不要修改）
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


# ==================== 闭包练习 ====================

def closure_exercises():
    """
    闭包练习
    """
    print("\n闭包练习")
    print("-" * 30)
    
    # 练习1: 实现一个计数器闭包
    def create_counter(initial_value: int = 0) -> Callable:
        """
        创建计数器闭包
        
        参数:
            initial_value: 初始值
        
        返回:
            function: 计数器函数
        """
        # TODO: 在这里实现
        pass
    
    # 练习2: 实现一个累加器闭包
    def create_accumulator() -> Callable:
        """
        创建累加器闭包
        
        返回:
            function: 累加器函数
        """
        # TODO: 在这里实现
        pass
    
    # 练习3: 实现一个配置管理器闭包
    def create_config_manager(default_config: Dict[str, Any]) -> Tuple[Callable, Callable]:
        """
        创建配置管理器闭包
        
        参数:
            default_config: 默认配置
        
        返回:
            tuple: (getter函数, setter函数)
        """
        # TODO: 在这里实现
        pass
    
    # 练习4: 实现一个函数工厂闭包
    def create_math_operation(operation: str) -> Callable:
        """
        创建数学运算函数
        
        参数:
            operation: 运算类型 ('add', 'multiply', 'power')
        
        返回:
            function: 运算函数
        """
        # TODO: 在这里实现
        pass
    
    # 练习5: 实现一个状态机闭包
    def create_state_machine(states: List[str], initial_state: str) -> Tuple[Callable, Callable]:
        """
        创建状态机闭包
        
        参数:
            states: 状态列表
            initial_state: 初始状态
        
        返回:
            tuple: (get_state函数, set_state函数)
        """
        # TODO: 在这里实现
        pass
    
    # 测试代码（不要修改）
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


# ==================== 函数式编程技巧练习 ====================

def functional_programming_exercises():
    """
    函数式编程技巧练习
    """
    print("\n函数式编程技巧练习")
    print("-" * 30)
    
    # 练习1: 实现map函数的自定义版本
    def custom_map(func: Callable, iterable) -> List[Any]:
        """
        自定义map函数
        
        参数:
            func: 转换函数
            iterable: 可迭代对象
        
        返回:
            list: 转换后的列表
        """
        # TODO: 在这里实现
        pass
    
    # 练习2: 实现filter函数的自定义版本
    def custom_filter(func: Callable, iterable) -> List[Any]:
        """
        自定义filter函数
        
        参数:
            func: 过滤函数
            iterable: 可迭代对象
        
        返回:
            list: 过滤后的列表
        """
        # TODO: 在这里实现
        pass
    
    # 练习3: 实现函数管道
    def pipe(*functions):
        """
        创建函数管道
        
        参数:
            *functions: 函数列表
        
        返回:
            function: 管道函数
        """
        # TODO: 在这里实现
        pass
    
    # 练习4: 实现柯里化函数
    def curry(func: Callable, arity: int = None) -> Callable:
        """
        柯里化函数
        
        参数:
            func: 原函数
            arity: 参数数量
        
        返回:
            function: 柯里化后的函数
        """
        # TODO: 在这里实现
        pass
    
    # 练习5: 实现偏函数应用
    def partial(func: Callable, *args, **kwargs) -> Callable:
        """
        偏函数应用
        
        参数:
            func: 原函数
            *args: 位置参数
            **kwargs: 关键字参数
        
        返回:
            function: 偏应用函数
        """
        # TODO: 在这里实现
        pass
    
    # 练习6: 实现函数组合器
    def compose_all(*functions):
        """
        组合多个函数
        
        参数:
            *functions: 函数列表
        
        返回:
            function: 组合后的函数
        """
        # TODO: 在这里实现
        pass
    
    # 测试代码（不要修改）
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
        compose_result = composed(3)
        assert compose_result == 64, "compose_all测试失败"  # ((3^2)*2)+1 = 19, 等等...
        print("✓ compose_all测试通过")
    
    except Exception as e:
        print(f"❌ 测试失败: {e}")


# ==================== 主程序 ====================

def main():
    """
    主程序：运行所有练习
    """
    print("Session 06: 函数编程 - 高级特性练习")
    print("=" * 50)
    print("请完成以下练习，然后运行测试验证你的实现。")
    print("提示：查看每个函数的文档字符串了解具体要求。")
    print("=" * 50)
    
    # 运行所有练习
    lambda_exercises()
    higher_order_functions_exercises()
    decorator_exercises()
    recursion_exercises()
    closure_exercises()
    functional_programming_exercises()
    
    print("\n" + "=" * 50)
    print("练习完成！如果所有测试都通过，说明你已经掌握了函数编程的高级特性。")
    print("继续学习更多高级主题，如异步编程、元编程等。")


if __name__ == "__main__":
    main()