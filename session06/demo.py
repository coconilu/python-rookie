#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session 06: 函数编程 - 主要演示代码

本文件演示了Python函数编程的核心概念和实际应用。
包括函数定义、参数传递、返回值、作用域等重要概念。

作者: Python教程团队
创建日期: 2024-12-22
最后修改: 2024-12-22
"""

import math
import time
from functools import wraps


def main():
    """
    主函数：演示函数编程的各个方面
    """
    print("Session 06: 函数编程演示")
    print("=" * 50)
    
    # 1. 基础函数演示
    print("\n1. 基础函数演示")
    print("-" * 30)
    basic_function_demo()
    
    # 2. 参数传递演示
    print("\n2. 参数传递演示")
    print("-" * 30)
    parameter_demo()
    
    # 3. 返回值演示
    print("\n3. 返回值演示")
    print("-" * 30)
    return_value_demo()
    
    # 4. 作用域演示
    print("\n4. 作用域演示")
    print("-" * 30)
    scope_demo()
    
    # 5. 高级特性演示
    print("\n5. 高级特性演示")
    print("-" * 30)
    advanced_features_demo()
    
    # 6. 实际应用演示
    print("\n6. 实际应用演示")
    print("-" * 30)
    practical_application_demo()
    
    print("\n演示完成！")


# ==================== 1. 基础函数演示 ====================

def greet(name):
    """
    简单的问候函数
    
    参数:
        name (str): 要问候的人的姓名
    
    返回:
        str: 问候消息
    """
    return f"Hello, {name}! Welcome to Python functions!"


def calculate_circle_area(radius):
    """
    计算圆的面积
    
    参数:
        radius (float): 圆的半径
    
    返回:
        float: 圆的面积
    """
    if radius < 0:
        raise ValueError("半径不能为负数")
    return math.pi * radius ** 2


def basic_function_demo():
    """
    演示基础函数的定义和调用
    """
    # 调用问候函数
    message = greet("Alice")
    print(f"问候消息: {message}")
    
    # 调用计算函数
    radius = 5
    area = calculate_circle_area(radius)
    print(f"半径为{radius}的圆面积: {area:.2f}")
    
    # 查看函数文档
    print(f"\n函数文档: {calculate_circle_area.__doc__.strip()}")


# ==================== 2. 参数传递演示 ====================

def create_user_profile(username, email, age=None, active=True, *hobbies, **extra_info):
    """
    创建用户档案（演示各种参数类型）
    
    参数:
        username (str): 用户名（必需）
        email (str): 邮箱地址（必需）
        age (int, optional): 年龄（可选）
        active (bool): 是否激活（默认True）
        *hobbies: 爱好列表（可变位置参数）
        **extra_info: 额外信息（可变关键字参数）
    
    返回:
        dict: 用户档案字典
    """
    profile = {
        "username": username,
        "email": email,
        "age": age,
        "active": active,
        "hobbies": list(hobbies),
        "extra_info": extra_info
    }
    return profile


def calculate_total(*numbers, tax_rate=0.1, currency="USD"):
    """
    计算总价（演示混合参数使用）
    
    参数:
        *numbers: 价格列表
        tax_rate (float): 税率
        currency (str): 货币单位
    
    返回:
        dict: 包含小计、税额和总计的字典
    """
    subtotal = sum(numbers)
    tax = subtotal * tax_rate
    total = subtotal + tax
    
    return {
        "subtotal": subtotal,
        "tax": tax,
        "total": total,
        "currency": currency
    }


def parameter_demo():
    """
    演示不同类型的参数传递
    """
    # 基本参数调用
    profile1 = create_user_profile("alice", "alice@example.com")
    print(f"基本档案: {profile1}")
    
    # 包含可选参数
    profile2 = create_user_profile(
        "bob", "bob@example.com", 
        age=25, 
        "reading", "coding", "gaming",  # 爱好
        location="Beijing", job="Engineer"  # 额外信息
    )
    print(f"完整档案: {profile2}")
    
    # 关键字参数调用
    profile3 = create_user_profile(
        email="charlie@example.com",
        username="charlie",
        active=False
    )
    print(f"关键字参数档案: {profile3}")
    
    # 计算总价演示
    bill1 = calculate_total(10.99, 25.50, 8.75)
    print(f"\n账单1: {bill1}")
    
    bill2 = calculate_total(100, 200, 300, tax_rate=0.15, currency="CNY")
    print(f"账单2: {bill2}")


# ==================== 3. 返回值演示 ====================

def get_user_info(user_id):
    """
    获取用户信息（单个返回值）
    
    参数:
        user_id (int): 用户ID
    
    返回:
        dict: 用户信息字典
    """
    # 模拟数据库查询
    users_db = {
        1: {"name": "Alice", "email": "alice@example.com", "age": 25},
        2: {"name": "Bob", "email": "bob@example.com", "age": 30},
        3: {"name": "Charlie", "email": "charlie@example.com", "age": 35}
    }
    return users_db.get(user_id, {})


def parse_full_name(full_name):
    """
    解析全名（多个返回值）
    
    参数:
        full_name (str): 完整姓名
    
    返回:
        tuple: (姓, 名, 中间名)
    """
    parts = full_name.strip().split()
    
    if len(parts) == 1:
        return parts[0], "", ""
    elif len(parts) == 2:
        return parts[0], parts[1], ""
    else:
        return parts[0], parts[-1], " ".join(parts[1:-1])


def calculate_statistics(numbers):
    """
    计算数字列表的统计信息（多个返回值）
    
    参数:
        numbers (list): 数字列表
    
    返回:
        tuple: (平均值, 最大值, 最小值, 总和)
    """
    if not numbers:
        return 0, 0, 0, 0
    
    total = sum(numbers)
    average = total / len(numbers)
    maximum = max(numbers)
    minimum = min(numbers)
    
    return average, maximum, minimum, total


def print_report(title, data):
    """
    打印报告（无返回值函数）
    
    参数:
        title (str): 报告标题
        data (dict): 报告数据
    """
    print(f"\n=== {title} ===")
    for key, value in data.items():
        print(f"{key}: {value}")
    print("=" * (len(title) + 8))


def return_value_demo():
    """
    演示不同类型的返回值
    """
    # 单个返回值
    user = get_user_info(1)
    print(f"用户信息: {user}")
    
    # 多个返回值
    first, last, middle = parse_full_name("John Michael Smith")
    print(f"姓名解析: 姓={first}, 名={last}, 中间名={middle}")
    
    # 统计信息
    numbers = [10, 25, 30, 15, 40, 35, 20]
    avg, max_val, min_val, total = calculate_statistics(numbers)
    print(f"统计信息: 平均={avg:.2f}, 最大={max_val}, 最小={min_val}, 总和={total}")
    
    # 无返回值函数
    report_data = {
        "总用户数": 1250,
        "活跃用户": 980,
        "新注册": 45
    }
    print_report("用户统计报告", report_data)


# ==================== 4. 作用域演示 ====================

# 全局变量
global_counter = 0
app_config = {
    "debug": True,
    "version": "1.0.0"
}


def increment_global_counter():
    """
    增加全局计数器
    """
    global global_counter
    global_counter += 1
    print(f"全局计数器增加到: {global_counter}")


def create_counter_closure():
    """
    创建计数器闭包（演示nonlocal）
    
    返回:
        tuple: (increment函数, get_count函数, reset函数)
    """
    count = 0
    
    def increment():
        nonlocal count
        count += 1
        return count
    
    def get_count():
        return count
    
    def reset():
        nonlocal count
        count = 0
        return count
    
    return increment, get_count, reset


def demonstrate_local_scope():
    """
    演示局部作用域
    """
    local_var = "我是局部变量"
    local_counter = 100
    
    print(f"局部变量: {local_var}")
    print(f"局部计数器: {local_counter}")
    print(f"访问全局计数器: {global_counter}")
    print(f"访问全局配置: {app_config}")


def scope_demo():
    """
    演示作用域的各种情况
    """
    print(f"初始全局计数器: {global_counter}")
    
    # 演示局部作用域
    demonstrate_local_scope()
    
    # 演示全局变量修改
    increment_global_counter()
    increment_global_counter()
    
    # 演示闭包和nonlocal
    inc, get, reset = create_counter_closure()
    print(f"\n闭包计数器初始值: {get()}")
    print(f"增加后: {inc()}")
    print(f"再次增加: {inc()}")
    print(f"重置后: {reset()}")


# ==================== 5. 高级特性演示 ====================

def timing_decorator(func):
    """
    计时装饰器
    
    参数:
        func: 要装饰的函数
    
    返回:
        function: 装饰后的函数
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 执行时间: {end_time - start_time:.4f}秒")
        return result
    return wrapper


@timing_decorator
def fibonacci_recursive(n):
    """
    递归计算斐波那契数列
    
    参数:
        n (int): 项数
    
    返回:
        int: 斐波那契数
    """
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)


def fibonacci_iterative(n):
    """
    迭代计算斐波那契数列
    
    参数:
        n (int): 项数
    
    返回:
        int: 斐波那契数
    """
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def apply_to_list(func, data_list):
    """
    高阶函数：对列表中的每个元素应用函数
    
    参数:
        func: 要应用的函数
        data_list: 数据列表
    
    返回:
        list: 处理后的列表
    """
    return [func(item) for item in data_list]


def advanced_features_demo():
    """
    演示高级特性
    """
    # Lambda函数
    numbers = [1, 2, 3, 4, 5]
    
    # 使用lambda和内置高阶函数
    squared = list(map(lambda x: x ** 2, numbers))
    even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
    
    print(f"原数字: {numbers}")
    print(f"平方: {squared}")
    print(f"偶数: {even_numbers}")
    
    # 自定义高阶函数
    doubled = apply_to_list(lambda x: x * 2, numbers)
    print(f"翻倍: {doubled}")
    
    # 装饰器演示
    print("\n装饰器演示:")
    result = fibonacci_recursive(10)
    print(f"斐波那契数列第10项: {result}")
    
    # 递归vs迭代性能比较
    print("\n性能比较:")
    start = time.time()
    result_iter = fibonacci_iterative(30)
    iter_time = time.time() - start
    print(f"迭代方法计算F(30): {result_iter}, 耗时: {iter_time:.6f}秒")


# ==================== 6. 实际应用演示 ====================

def validate_email(email):
    """
    验证邮箱格式
    
    参数:
        email (str): 邮箱地址
    
    返回:
        bool: 是否有效
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def format_currency(amount, currency="USD", decimal_places=2):
    """
    格式化货币显示
    
    参数:
        amount (float): 金额
        currency (str): 货币代码
        decimal_places (int): 小数位数
    
    返回:
        str: 格式化的货币字符串
    """
    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "CNY": "¥",
        "GBP": "£"
    }
    
    symbol = currency_symbols.get(currency, currency)
    formatted_amount = f"{amount:,.{decimal_places}f}"
    return f"{symbol}{formatted_amount}"


def calculate_discount(original_price, discount_percent, min_amount=0):
    """
    计算折扣价格
    
    参数:
        original_price (float): 原价
        discount_percent (float): 折扣百分比
        min_amount (float): 最低消费金额
    
    返回:
        dict: 包含原价、折扣、最终价格的字典
    """
    if original_price < min_amount:
        discount_amount = 0
        final_price = original_price
    else:
        discount_amount = original_price * (discount_percent / 100)
        final_price = original_price - discount_amount
    
    return {
        "original_price": original_price,
        "discount_percent": discount_percent,
        "discount_amount": discount_amount,
        "final_price": final_price,
        "savings": discount_amount
    }


def process_user_registration(username, email, password, **additional_info):
    """
    处理用户注册
    
    参数:
        username (str): 用户名
        email (str): 邮箱
        password (str): 密码
        **additional_info: 额外信息
    
    返回:
        dict: 注册结果
    """
    errors = []
    
    # 验证用户名
    if len(username) < 3:
        errors.append("用户名至少需要3个字符")
    
    # 验证邮箱
    if not validate_email(email):
        errors.append("邮箱格式无效")
    
    # 验证密码
    if len(password) < 6:
        errors.append("密码至少需要6个字符")
    
    if errors:
        return {
            "success": False,
            "errors": errors
        }
    
    # 创建用户档案
    user_profile = {
        "username": username,
        "email": email,
        "registration_date": time.strftime("%Y-%m-%d %H:%M:%S"),
        **additional_info
    }
    
    return {
        "success": True,
        "user_profile": user_profile,
        "message": "用户注册成功"
    }


def practical_application_demo():
    """
    演示实际应用场景
    """
    # 邮箱验证
    emails = ["test@example.com", "invalid-email", "user@domain.co.uk"]
    print("邮箱验证结果:")
    for email in emails:
        is_valid = validate_email(email)
        print(f"  {email}: {'有效' if is_valid else '无效'}")
    
    # 货币格式化
    print("\n货币格式化:")
    amounts = [1234.56, 999999.99, 0.99]
    for amount in amounts:
        usd = format_currency(amount, "USD")
        cny = format_currency(amount, "CNY")
        print(f"  {amount} -> {usd} / {cny}")
    
    # 折扣计算
    print("\n折扣计算:")
    discount_info = calculate_discount(100, 20, min_amount=50)
    for key, value in discount_info.items():
        print(f"  {key}: {value}")
    
    # 用户注册
    print("\n用户注册演示:")
    
    # 成功注册
    result1 = process_user_registration(
        "alice123", 
        "alice@example.com", 
        "password123",
        age=25,
        city="Beijing"
    )
    print(f"注册结果1: {result1}")
    
    # 失败注册
    result2 = process_user_registration(
        "ab",  # 用户名太短
        "invalid-email",  # 邮箱无效
        "123"  # 密码太短
    )
    print(f"注册结果2: {result2}")


if __name__ == "__main__":
    main()