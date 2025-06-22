#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session 06: 函数编程 - 示例3：高级特性

本文件演示函数的高级特性，包括Lambda函数、高阶函数、
装饰器、递归等概念和应用。

作者: Python教程团队
创建日期: 2024-12-22
"""

import time
import functools
from typing import Callable, Any


def main():
    """
    主函数：演示函数高级特性
    """
    print("函数高级特性示例")
    print("=" * 40)
    
    # 1. Lambda函数
    print("\n1. Lambda函数")
    lambda_demo()
    
    # 2. 高阶函数
    print("\n2. 高阶函数")
    higher_order_function_demo()
    
    # 3. 装饰器
    print("\n3. 装饰器")
    decorator_demo()
    
    # 4. 递归函数
    print("\n4. 递归函数")
    recursion_demo()
    
    # 5. 闭包
    print("\n5. 闭包")
    closure_demo()
    
    print("\n高级特性演示完成！")


# ==================== Lambda函数 ====================

def lambda_demo():
    """
    演示Lambda函数的使用
    """
    print("Lambda函数演示:")
    
    # 基本Lambda函数
    square = lambda x: x ** 2
    print(f"平方函数: square(5) = {square(5)}")
    
    add = lambda x, y: x + y
    print(f"加法函数: add(3, 4) = {add(3, 4)}")
    
    # 条件Lambda
    max_value = lambda a, b: a if a > b else b
    print(f"最大值函数: max_value(10, 7) = {max_value(10, 7)}")
    
    # 字符串处理Lambda
    capitalize_words = lambda text: ' '.join(word.capitalize() for word in text.split())
    print(f"首字母大写: {capitalize_words('hello world python')}")
    
    # Lambda在数据处理中的应用
    print("\nLambda在数据处理中的应用:")
    
    # 学生数据
    students = [
        {'name': 'Alice', 'age': 20, 'score': 85},
        {'name': 'Bob', 'age': 19, 'score': 92},
        {'name': 'Charlie', 'age': 21, 'score': 78},
        {'name': 'Diana', 'age': 20, 'score': 96}
    ]
    
    # 按分数排序
    sorted_by_score = sorted(students, key=lambda s: s['score'], reverse=True)
    print("按分数排序:")
    for student in sorted_by_score:
        print(f"  {student['name']}: {student['score']}")
    
    # 筛选高分学生
    high_scorers = list(filter(lambda s: s['score'] >= 90, students))
    print(f"\n高分学生: {[s['name'] for s in high_scorers]}")
    
    # 计算分数等级
    grade_mapper = lambda score: 'A' if score >= 90 else 'B' if score >= 80 else 'C'
    grades = list(map(lambda s: {'name': s['name'], 'grade': grade_mapper(s['score'])}, students))
    print("\n分数等级:")
    for grade in grades:
        print(f"  {grade['name']}: {grade['grade']}")
    
    # Lambda在字典操作中的应用
    print("\nLambda在字典操作中的应用:")
    
    # 价格数据
    prices = {'apple': 3.5, 'banana': 2.0, 'orange': 4.2, 'grape': 6.8}
    
    # 按价格排序
    sorted_prices = dict(sorted(prices.items(), key=lambda item: item[1]))
    print(f"按价格排序: {sorted_prices}")
    
    # 价格转换（添加税费）
    tax_rate = 0.1
    prices_with_tax = dict(map(lambda item: (item[0], round(item[1] * (1 + tax_rate), 2)), 
                              prices.items()))
    print(f"含税价格: {prices_with_tax}")


# ==================== 高阶函数 ====================

def apply_operation(numbers, operation):
    """
    对数字列表应用操作（高阶函数）
    
    参数:
        numbers (list): 数字列表
        operation (function): 操作函数
    
    返回:
        list: 处理后的数字列表
    """
    return [operation(num) for num in numbers]


def filter_and_transform(data, filter_func, transform_func):
    """
    筛选并转换数据（高阶函数）
    
    参数:
        data (list): 数据列表
        filter_func (function): 筛选函数
        transform_func (function): 转换函数
    
    返回:
        list: 处理后的数据
    """
    filtered_data = filter(filter_func, data)
    return list(map(transform_func, filtered_data))


def create_validator(min_value, max_value):
    """
    创建验证器函数（返回函数的函数）
    
    参数:
        min_value: 最小值
        max_value: 最大值
    
    返回:
        function: 验证函数
    """
    def validator(value):
        return min_value <= value <= max_value
    return validator


def create_multiplier(factor):
    """
    创建乘法器函数（返回函数的函数）
    
    参数:
        factor: 乘数
    
    返回:
        function: 乘法函数
    """
    return lambda x: x * factor


def compose_functions(*functions):
    """
    组合多个函数（函数组合）
    
    参数:
        *functions: 要组合的函数
    
    返回:
        function: 组合后的函数
    """
    def composed(x):
        result = x
        for func in reversed(functions):
            result = func(result)
        return result
    return composed


def retry_function(max_attempts=3):
    """
    重试装饰器工厂（高阶函数）
    
    参数:
        max_attempts (int): 最大重试次数
    
    返回:
        function: 装饰器函数
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    print(f"第{attempt + 1}次尝试失败: {e}")
            return None
        return wrapper
    return decorator


def higher_order_function_demo():
    """
    演示高阶函数的使用
    """
    print("高阶函数演示:")
    
    # 应用操作
    numbers = [1, 2, 3, 4, 5]
    
    # 平方操作
    squared = apply_operation(numbers, lambda x: x ** 2)
    print(f"平方: {squared}")
    
    # 立方操作
    cubed = apply_operation(numbers, lambda x: x ** 3)
    print(f"立方: {cubed}")
    
    # 筛选和转换
    print("\n筛选和转换演示:")
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # 筛选偶数并平方
    even_squared = filter_and_transform(
        data, 
        lambda x: x % 2 == 0,  # 筛选偶数
        lambda x: x ** 2       # 平方
    )
    print(f"偶数平方: {even_squared}")
    
    # 创建验证器
    print("\n验证器演示:")
    age_validator = create_validator(18, 65)
    score_validator = create_validator(0, 100)
    
    test_ages = [16, 25, 70, 45]
    test_scores = [85, 105, -5, 92]
    
    print("年龄验证:")
    for age in test_ages:
        print(f"  {age}: {'有效' if age_validator(age) else '无效'}")
    
    print("分数验证:")
    for score in test_scores:
        print(f"  {score}: {'有效' if score_validator(score) else '无效'}")
    
    # 创建乘法器
    print("\n乘法器演示:")
    double = create_multiplier(2)
    triple = create_multiplier(3)
    
    test_numbers = [1, 2, 3, 4, 5]
    print(f"原数字: {test_numbers}")
    print(f"双倍: {[double(x) for x in test_numbers]}")
    print(f"三倍: {[triple(x) for x in test_numbers]}")
    
    # 函数组合
    print("\n函数组合演示:")
    add_one = lambda x: x + 1
    multiply_by_two = lambda x: x * 2
    square = lambda x: x ** 2
    
    # 组合函数: square(multiply_by_two(add_one(x)))
    composed = compose_functions(square, multiply_by_two, add_one)
    
    test_value = 3
    step1 = add_one(test_value)  # 3 + 1 = 4
    step2 = multiply_by_two(step1)  # 4 * 2 = 8
    step3 = square(step2)  # 8^2 = 64
    
    print(f"输入: {test_value}")
    print(f"步骤: {test_value} -> {step1} -> {step2} -> {step3}")
    print(f"组合函数结果: {composed(test_value)}")
    
    # 重试机制演示
    print("\n重试机制演示:")
    
    @retry_function(max_attempts=3)
    def unreliable_function(x):
        import random
        if random.random() < 0.7:  # 70%概率失败
            raise ValueError("随机失败")
        return x * 2
    
    try:
        result = unreliable_function(5)
        print(f"成功结果: {result}")
    except Exception as e:
        print(f"最终失败: {e}")


# ==================== 装饰器 ====================

def timing_decorator(func):
    """
    计时装饰器
    
    参数:
        func: 被装饰的函数
    
    返回:
        function: 装饰后的函数
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 执行时间: {end_time - start_time:.4f}秒")
        return result
    return wrapper


def log_decorator(func):
    """
    日志装饰器
    
    参数:
        func: 被装饰的函数
    
    返回:
        function: 装饰后的函数
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"调用函数: {func.__name__}")
        print(f"参数: args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"返回值: {result}")
        return result
    return wrapper


def validate_types(**expected_types):
    """
    类型验证装饰器工厂
    
    参数:
        **expected_types: 期望的参数类型
    
    返回:
        function: 装饰器函数
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 获取函数参数名
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # 验证类型
            for param_name, expected_type in expected_types.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"参数 {param_name} 期望类型 {expected_type.__name__}, "
                            f"实际类型 {type(value).__name__}"
                        )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def cache_decorator(func):
    """
    缓存装饰器
    
    参数:
        func: 被装饰的函数
    
    返回:
        function: 装饰后的函数
    """
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 创建缓存键
        key = str(args) + str(sorted(kwargs.items()))
        
        if key in cache:
            print(f"缓存命中: {func.__name__}")
            return cache[key]
        
        print(f"计算结果: {func.__name__}")
        result = func(*args, **kwargs)
        cache[key] = result
        return result
    
    return wrapper


# 使用装饰器的示例函数
@timing_decorator
@log_decorator
def calculate_fibonacci(n):
    """
    计算斐波那契数列（带装饰器）
    
    参数:
        n (int): 位置
    
    返回:
        int: 斐波那契数
    """
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)


@validate_types(name=str, age=int, salary=float)
def create_employee(name, age, salary):
    """
    创建员工信息（带类型验证）
    
    参数:
        name (str): 姓名
        age (int): 年龄
        salary (float): 薪资
    
    返回:
        dict: 员工信息
    """
    return {
        "name": name,
        "age": age,
        "salary": salary
    }


@cache_decorator
def expensive_calculation(x, y):
    """
    耗时计算（带缓存）
    
    参数:
        x (int): 参数1
        y (int): 参数2
    
    返回:
        int: 计算结果
    """
    # 模拟耗时计算
    time.sleep(0.1)
    return x ** y + y ** x


def decorator_demo():
    """
    演示装饰器的使用
    """
    print("装饰器演示:")
    
    # 计时和日志装饰器
    print("\n计时和日志装饰器:")
    # 注意：这里会递归调用，实际使用中应该用迭代方式
    # result = calculate_fibonacci(5)
    # print(f"斐波那契结果: {result}")
    
    # 类型验证装饰器
    print("\n类型验证装饰器:")
    try:
        employee1 = create_employee("Alice", 25, 50000.0)
        print(f"员工1: {employee1}")
        
        # 这会引发类型错误
        employee2 = create_employee("Bob", "25", 60000.0)  # age应该是int
    except TypeError as e:
        print(f"类型错误: {e}")
    
    # 缓存装饰器
    print("\n缓存装饰器:")
    
    # 第一次计算
    result1 = expensive_calculation(2, 3)
    print(f"第一次结果: {result1}")
    
    # 第二次计算（使用缓存）
    result2 = expensive_calculation(2, 3)
    print(f"第二次结果: {result2}")
    
    # 不同参数的计算
    result3 = expensive_calculation(3, 2)
    print(f"不同参数结果: {result3}")
    
    # 多个装饰器组合
    print("\n多个装饰器组合:")
    
    @timing_decorator
    @cache_decorator
    def complex_calculation(n):
        """复杂计算函数"""
        result = 0
        for i in range(n):
            result += i ** 2
        return result
    
    # 第一次计算
    result1 = complex_calculation(1000)
    print(f"第一次计算结果: {result1}")
    
    # 第二次计算（使用缓存）
    result2 = complex_calculation(1000)
    print(f"第二次计算结果: {result2}")


# ==================== 递归函数 ====================

def factorial_recursive(n):
    """
    递归计算阶乘
    
    参数:
        n (int): 非负整数
    
    返回:
        int: n的阶乘
    """
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)


def fibonacci_recursive(n):
    """
    递归计算斐波那契数
    
    参数:
        n (int): 位置
    
    返回:
        int: 斐波那契数
    """
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_memoized(n, memo=None):
    """
    带记忆化的斐波那契递归
    
    参数:
        n (int): 位置
        memo (dict): 记忆化字典
    
    返回:
        int: 斐波那契数
    """
    if memo is None:
        memo = {}
    
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fibonacci_memoized(n - 1, memo) + fibonacci_memoized(n - 2, memo)
    return memo[n]


def binary_search_recursive(arr, target, left=0, right=None):
    """
    递归二分查找
    
    参数:
        arr (list): 已排序的数组
        target: 目标值
        left (int): 左边界
        right (int): 右边界
    
    返回:
        int: 目标值的索引，未找到返回-1
    """
    if right is None:
        right = len(arr) - 1
    
    if left > right:
        return -1
    
    mid = (left + right) // 2
    
    if arr[mid] == target:
        return mid
    elif arr[mid] > target:
        return binary_search_recursive(arr, target, left, mid - 1)
    else:
        return binary_search_recursive(arr, target, mid + 1, right)


def tree_sum(node):
    """
    递归计算树的节点值总和
    
    参数:
        node (dict): 树节点，格式: {'value': int, 'children': [...]}
    
    返回:
        int: 节点值总和
    """
    if node is None:
        return 0
    
    total = node.get('value', 0)
    
    for child in node.get('children', []):
        total += tree_sum(child)
    
    return total


def flatten_list_recursive(nested_list):
    """
    递归展平嵌套列表
    
    参数:
        nested_list (list): 嵌套列表
    
    返回:
        list: 展平后的列表
    """
    result = []
    
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten_list_recursive(item))
        else:
            result.append(item)
    
    return result


def recursion_demo():
    """
    演示递归函数的使用
    """
    print("递归函数演示:")
    
    # 阶乘计算
    print("\n阶乘计算:")
    for i in range(6):
        result = factorial_recursive(i)
        print(f"{i}! = {result}")
    
    # 斐波那契数列
    print("\n斐波那契数列:")
    print("普通递归:")
    for i in range(8):
        result = fibonacci_recursive(i)
        print(f"F({i}) = {result}")
    
    print("\n记忆化递归:")
    for i in range(8):
        result = fibonacci_memoized(i)
        print(f"F({i}) = {result}")
    
    # 性能对比
    print("\n性能对比 (F(20)):")
    
    start_time = time.time()
    result1 = fibonacci_recursive(20)
    time1 = time.time() - start_time
    print(f"普通递归: {result1}, 耗时: {time1:.4f}秒")
    
    start_time = time.time()
    result2 = fibonacci_memoized(20)
    time2 = time.time() - start_time
    print(f"记忆化递归: {result2}, 耗时: {time2:.4f}秒")
    
    # 二分查找
    print("\n二分查找:")
    sorted_array = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    targets = [7, 12, 1, 19]
    
    print(f"数组: {sorted_array}")
    for target in targets:
        index = binary_search_recursive(sorted_array, target)
        if index != -1:
            print(f"找到 {target} 在索引 {index}")
        else:
            print(f"未找到 {target}")
    
    # 树结构处理
    print("\n树结构处理:")
    tree = {
        'value': 1,
        'children': [
            {
                'value': 2,
                'children': [
                    {'value': 4, 'children': []},
                    {'value': 5, 'children': []}
                ]
            },
            {
                'value': 3,
                'children': [
                    {'value': 6, 'children': []}
                ]
            }
        ]
    }
    
    total = tree_sum(tree)
    print(f"树节点值总和: {total}")
    
    # 嵌套列表展平
    print("\n嵌套列表展平:")
    nested = [1, [2, 3], [4, [5, 6]], [[7, 8], 9]]
    flattened = flatten_list_recursive(nested)
    print(f"原列表: {nested}")
    print(f"展平后: {flattened}")


# ==================== 闭包 ====================

def create_counter(initial_value=0):
    """
    创建计数器闭包
    
    参数:
        initial_value (int): 初始值
    
    返回:
        function: 计数器函数
    """
    count = initial_value
    
    def counter():
        nonlocal count
        count += 1
        return count
    
    return counter


def create_accumulator():
    """
    创建累加器闭包
    
    返回:
        function: 累加器函数
    """
    total = 0
    
    def accumulator(value):
        nonlocal total
        total += value
        return total
    
    return accumulator


def create_multiplier_closure(factor):
    """
    创建乘法器闭包
    
    参数:
        factor: 乘数因子
    
    返回:
        function: 乘法器函数
    """
    def multiplier(value):
        return value * factor
    
    return multiplier


def create_validator_closure(validation_rules):
    """
    创建验证器闭包
    
    参数:
        validation_rules (dict): 验证规则
    
    返回:
        function: 验证器函数
    """
    def validator(data):
        errors = []
        
        for field, rules in validation_rules.items():
            if field not in data:
                if rules.get('required', False):
                    errors.append(f"{field} 是必需的")
                continue
            
            value = data[field]
            
            # 类型检查
            if 'type' in rules and not isinstance(value, rules['type']):
                errors.append(f"{field} 类型错误")
            
            # 最小值检查
            if 'min' in rules and value < rules['min']:
                errors.append(f"{field} 小于最小值 {rules['min']}")
            
            # 最大值检查
            if 'max' in rules and value > rules['max']:
                errors.append(f"{field} 大于最大值 {rules['max']}")
        
        return len(errors) == 0, errors
    
    return validator


def closure_demo():
    """
    演示闭包的使用
    """
    print("闭包演示:")
    
    # 计数器闭包
    print("\n计数器闭包:")
    counter1 = create_counter()
    counter2 = create_counter(10)
    
    print(f"计数器1: {counter1()}, {counter1()}, {counter1()}")
    print(f"计数器2: {counter2()}, {counter2()}, {counter2()}")
    
    # 累加器闭包
    print("\n累加器闭包:")
    acc = create_accumulator()
    
    print(f"累加 5: {acc(5)}")
    print(f"累加 3: {acc(3)}")
    print(f"累加 7: {acc(7)}")
    
    # 乘法器闭包
    print("\n乘法器闭包:")
    double = create_multiplier_closure(2)
    triple = create_multiplier_closure(3)
    
    test_values = [1, 2, 3, 4, 5]
    print(f"原值: {test_values}")
    print(f"双倍: {[double(x) for x in test_values]}")
    print(f"三倍: {[triple(x) for x in test_values]}")
    
    # 验证器闭包
    print("\n验证器闭包:")
    user_rules = {
        'name': {'required': True, 'type': str},
        'age': {'required': True, 'type': int, 'min': 0, 'max': 120},
        'email': {'required': True, 'type': str}
    }
    
    user_validator = create_validator_closure(user_rules)
    
    # 测试数据
    test_users = [
        {'name': 'Alice', 'age': 25, 'email': 'alice@example.com'},
        {'name': 'Bob', 'age': -5, 'email': 'bob@example.com'},
        {'age': 30, 'email': 'charlie@example.com'},  # 缺少name
        {'name': 'Diana', 'age': '25', 'email': 'diana@example.com'}  # age类型错误
    ]
    
    for i, user in enumerate(test_users, 1):
        is_valid, errors = user_validator(user)
        print(f"用户{i}: {'有效' if is_valid else '无效'}")
        if errors:
            for error in errors:
                print(f"  错误: {error}")


if __name__ == "__main__":
    main()