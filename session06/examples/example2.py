#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session 06: 函数编程 - 示例2：参数和返回值

本文件演示函数的各种参数类型和返回值处理。
包括位置参数、关键字参数、默认参数、可变参数等。

作者: Python教程团队
创建日期: 2024-12-22
"""

import datetime


def main():
    """
    主函数：演示参数和返回值的各种用法
    """
    print("参数和返回值示例")
    print("=" * 40)
    
    # 1. 位置参数和关键字参数
    print("\n1. 位置参数和关键字参数")
    positional_keyword_demo()
    
    # 2. 默认参数
    print("\n2. 默认参数")
    default_parameter_demo()
    
    # 3. 可变参数
    print("\n3. 可变参数")
    variable_parameter_demo()
    
    # 4. 多种返回值
    print("\n4. 多种返回值")
    return_value_demo()
    
    # 5. 参数组合使用
    print("\n5. 参数组合使用")
    parameter_combination_demo()
    
    print("\n示例演示完成！")


# ==================== 位置参数和关键字参数 ====================

def calculate_rectangle_info(length, width, unit):
    """
    计算矩形信息（位置参数）
    
    参数:
        length (float): 长度
        width (float): 宽度
        unit (str): 单位
    
    返回:
        dict: 矩形信息字典
    """
    area = length * width
    perimeter = 2 * (length + width)
    
    return {
        "length": length,
        "width": width,
        "area": area,
        "perimeter": perimeter,
        "unit": unit
    }


def create_person_info(name, age, city):
    """
    创建人员信息（演示关键字参数调用）
    
    参数:
        name (str): 姓名
        age (int): 年龄
        city (str): 城市
    
    返回:
        str: 格式化的人员信息
    """
    return f"{name}，{age}岁，来自{city}"


def positional_keyword_demo():
    """
    演示位置参数和关键字参数的使用
    """
    # 位置参数调用
    rect1 = calculate_rectangle_info(5, 3, "米")
    print(f"位置参数调用: {rect1}")
    
    # 关键字参数调用
    rect2 = calculate_rectangle_info(length=8, width=4, unit="厘米")
    print(f"关键字参数调用: {rect2}")
    
    # 混合调用（位置参数在前）
    rect3 = calculate_rectangle_info(10, width=6, unit="英寸")
    print(f"混合参数调用: {rect3}")
    
    # 人员信息演示
    person1 = create_person_info("张三", 25, "北京")
    print(f"\n位置参数: {person1}")
    
    person2 = create_person_info(name="李四", age=30, city="上海")
    print(f"关键字参数: {person2}")
    
    person3 = create_person_info(city="广州", name="王五", age=28)
    print(f"关键字参数（不同顺序）: {person3}")


# ==================== 默认参数 ====================

def greet_with_time(name, greeting="你好", show_time=False):
    """
    带时间的问候（默认参数演示）
    
    参数:
        name (str): 姓名
        greeting (str): 问候语，默认"你好"
        show_time (bool): 是否显示时间，默认False
    
    返回:
        str: 问候消息
    """
    message = f"{greeting}, {name}!"
    
    if show_time:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        message += f" 现在时间是 {current_time}"
    
    return message


def create_user_account(username, email, role="user", active=True, send_welcome=True):
    """
    创建用户账户（多个默认参数）
    
    参数:
        username (str): 用户名
        email (str): 邮箱
        role (str): 角色，默认"user"
        active (bool): 是否激活，默认True
        send_welcome (bool): 是否发送欢迎邮件，默认True
    
    返回:
        dict: 用户账户信息
    """
    account = {
        "username": username,
        "email": email,
        "role": role,
        "active": active,
        "created_at": datetime.datetime.now().isoformat()
    }
    
    if send_welcome:
        account["welcome_sent"] = True
        print(f"欢迎邮件已发送到 {email}")
    
    return account


def format_price(amount, currency="CNY", show_symbol=True, decimal_places=2):
    """
    格式化价格显示（默认参数演示）
    
    参数:
        amount (float): 金额
        currency (str): 货币，默认"CNY"
        show_symbol (bool): 是否显示货币符号，默认True
        decimal_places (int): 小数位数，默认2
    
    返回:
        str: 格式化的价格字符串
    """
    symbols = {
        "CNY": "¥",
        "USD": "$",
        "EUR": "€",
        "GBP": "£"
    }
    
    formatted_amount = f"{amount:.{decimal_places}f}"
    
    if show_symbol and currency in symbols:
        return f"{symbols[currency]}{formatted_amount}"
    else:
        return f"{formatted_amount} {currency}"


def default_parameter_demo():
    """
    演示默认参数的使用
    """
    # 问候函数演示
    print("问候函数演示:")
    print(greet_with_time("Alice"))  # 使用默认参数
    print(greet_with_time("Bob", "早上好"))  # 部分默认参数
    print(greet_with_time("Charlie", "晚上好", True))  # 所有参数
    print(greet_with_time("David", show_time=True))  # 关键字参数
    
    # 用户账户创建演示
    print("\n用户账户创建:")
    user1 = create_user_account("alice", "alice@example.com")
    print(f"用户1: {user1}")
    
    user2 = create_user_account("bob", "bob@example.com", "admin")
    print(f"用户2: {user2}")
    
    user3 = create_user_account("charlie", "charlie@example.com", 
                               active=False, send_welcome=False)
    print(f"用户3: {user3}")
    
    # 价格格式化演示
    print("\n价格格式化:")
    price = 1234.567
    print(f"默认格式: {format_price(price)}")
    print(f"美元格式: {format_price(price, 'USD')}")
    print(f"无符号格式: {format_price(price, show_symbol=False)}")
    print(f"高精度格式: {format_price(price, decimal_places=3)}")


# ==================== 可变参数 ====================

def calculate_sum(*numbers):
    """
    计算任意数量数字的和（*args演示）
    
    参数:
        *numbers: 任意数量的数字
    
    返回:
        float: 数字总和
    """
    return sum(numbers)


def calculate_average(*numbers):
    """
    计算平均值（*args演示）
    
    参数:
        *numbers: 任意数量的数字
    
    返回:
        float: 平均值，如果没有数字则返回0
    """
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)


def find_max_min(*numbers):
    """
    找出最大值和最小值（*args演示）
    
    参数:
        *numbers: 任意数量的数字
    
    返回:
        tuple: (最大值, 最小值)，如果没有数字则返回(None, None)
    """
    if not numbers:
        return None, None
    return max(numbers), min(numbers)


def create_config(**settings):
    """
    创建配置字典（**kwargs演示）
    
    参数:
        **settings: 任意配置参数
    
    返回:
        dict: 配置字典
    """
    default_config = {
        "debug": False,
        "timeout": 30,
        "max_connections": 100
    }
    
    # 更新默认配置
    default_config.update(settings)
    return default_config


def log_message(level, message, **details):
    """
    记录日志消息（混合可变参数）
    
    参数:
        level (str): 日志级别
        message (str): 日志消息
        **details: 额外的日志详情
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {level}: {message}"
    
    if details:
        detail_str = ", ".join([f"{k}={v}" for k, v in details.items()])
        log_entry += f" ({detail_str})"
    
    print(log_entry)


def flexible_function(required_arg, optional_arg="default", *args, **kwargs):
    """
    灵活的函数（所有参数类型组合）
    
    参数:
        required_arg: 必需参数
        optional_arg: 可选参数
        *args: 可变位置参数
        **kwargs: 可变关键字参数
    
    返回:
        dict: 包含所有参数信息的字典
    """
    return {
        "required": required_arg,
        "optional": optional_arg,
        "args": args,
        "kwargs": kwargs
    }


def variable_parameter_demo():
    """
    演示可变参数的使用
    """
    # *args 演示
    print("*args 演示:")
    print(f"求和: {calculate_sum(1, 2, 3, 4, 5)}")
    print(f"平均值: {calculate_average(10, 20, 30, 40)}")
    
    max_val, min_val = find_max_min(5, 2, 8, 1, 9, 3)
    print(f"最大值: {max_val}, 最小值: {min_val}")
    
    # 传递列表给*args
    numbers = [1, 2, 3, 4, 5]
    print(f"列表求和: {calculate_sum(*numbers)}")
    
    # **kwargs 演示
    print("\n**kwargs 演示:")
    config1 = create_config()
    print(f"默认配置: {config1}")
    
    config2 = create_config(debug=True, timeout=60, host="localhost")
    print(f"自定义配置: {config2}")
    
    # 日志记录演示
    print("\n日志记录演示:")
    log_message("INFO", "系统启动")
    log_message("ERROR", "连接失败", host="localhost", port=8080, retry=3)
    log_message("DEBUG", "处理请求", user_id=123, action="login")
    
    # 灵活函数演示
    print("\n灵活函数演示:")
    result1 = flexible_function("必需值")
    print(f"基本调用: {result1}")
    
    result2 = flexible_function("必需值", "可选值", 1, 2, 3, name="test", active=True)
    print(f"完整调用: {result2}")


# ==================== 多种返回值 ====================

def get_user_basic_info(user_id):
    """
    获取用户基本信息（单个返回值）
    
    参数:
        user_id (int): 用户ID
    
    返回:
        dict: 用户信息字典
    """
    # 模拟数据库查询
    users = {
        1: {"name": "Alice", "email": "alice@example.com", "age": 25},
        2: {"name": "Bob", "email": "bob@example.com", "age": 30},
        3: {"name": "Charlie", "email": "charlie@example.com", "age": 35}
    }
    return users.get(user_id, {})


def divide_with_remainder(dividend, divisor):
    """
    除法运算（多个返回值）
    
    参数:
        dividend (int): 被除数
        divisor (int): 除数
    
    返回:
        tuple: (商, 余数)
    """
    quotient = dividend // divisor
    remainder = dividend % divisor
    return quotient, remainder


def analyze_text(text):
    """
    分析文本（多个返回值）
    
    参数:
        text (str): 输入文本
    
    返回:
        tuple: (字符数, 单词数, 句子数)
    """
    char_count = len(text)
    word_count = len(text.split())
    sentence_count = text.count('.') + text.count('!') + text.count('?')
    
    return char_count, word_count, sentence_count


def get_name_parts(full_name):
    """
    分解姓名（多个返回值）
    
    参数:
        full_name (str): 完整姓名
    
    返回:
        tuple: (姓, 名)
    """
    parts = full_name.strip().split()
    if len(parts) >= 2:
        return parts[0], " ".join(parts[1:])
    else:
        return parts[0], ""


def calculate_circle_properties(radius):
    """
    计算圆的属性（多个返回值）
    
    参数:
        radius (float): 半径
    
    返回:
        tuple: (直径, 周长, 面积)
    """
    import math
    diameter = 2 * radius
    circumference = 2 * math.pi * radius
    area = math.pi * radius ** 2
    
    return diameter, circumference, area


def process_numbers(numbers):
    """
    处理数字列表（返回字典）
    
    参数:
        numbers (list): 数字列表
    
    返回:
        dict: 统计信息字典
    """
    if not numbers:
        return {"count": 0, "sum": 0, "average": 0, "max": None, "min": None}
    
    return {
        "count": len(numbers),
        "sum": sum(numbers),
        "average": sum(numbers) / len(numbers),
        "max": max(numbers),
        "min": min(numbers)
    }


def return_value_demo():
    """
    演示不同类型的返回值
    """
    # 单个返回值
    print("单个返回值演示:")
    user = get_user_basic_info(1)
    print(f"用户信息: {user}")
    
    # 多个返回值
    print("\n多个返回值演示:")
    quotient, remainder = divide_with_remainder(17, 5)
    print(f"17 ÷ 5 = {quotient} 余 {remainder}")
    
    # 文本分析
    sample_text = "Hello world! This is a test. How are you?"
    chars, words, sentences = analyze_text(sample_text)
    print(f"文本分析: {chars}字符, {words}单词, {sentences}句子")
    
    # 姓名分解
    first_name, last_name = get_name_parts("张 三")
    print(f"姓名分解: 姓={first_name}, 名={last_name}")
    
    # 圆的属性
    diameter, circumference, area = calculate_circle_properties(5)
    print(f"圆的属性: 直径={diameter}, 周长={circumference:.2f}, 面积={area:.2f}")
    
    # 返回字典
    print("\n返回字典演示:")
    numbers = [1, 5, 3, 9, 2, 8, 4]
    stats = process_numbers(numbers)
    print(f"数字统计: {stats}")
    
    # 接收部分返回值
    print("\n接收部分返回值:")
    _, circumference_only, _ = calculate_circle_properties(3)
    print(f"只获取周长: {circumference_only:.2f}")


# ==================== 参数组合使用 ====================

def create_database_connection(host, port, database, username=None, password=None, 
                             timeout=30, *options, **config):
    """
    创建数据库连接（参数组合演示）
    
    参数:
        host (str): 主机地址
        port (int): 端口号
        database (str): 数据库名
        username (str, optional): 用户名
        password (str, optional): 密码
        timeout (int): 超时时间，默认30秒
        *options: 额外选项
        **config: 额外配置
    
    返回:
        dict: 连接配置字典
    """
    connection_config = {
        "host": host,
        "port": port,
        "database": database,
        "timeout": timeout
    }
    
    if username:
        connection_config["username"] = username
    if password:
        connection_config["password"] = "***"  # 隐藏密码
    
    if options:
        connection_config["options"] = options
    
    if config:
        connection_config["extra_config"] = config
    
    return connection_config


def send_notification(recipient, message, method="email", urgent=False, 
                     *cc_recipients, **delivery_options):
    """
    发送通知（参数组合演示）
    
    参数:
        recipient (str): 接收者
        message (str): 消息内容
        method (str): 发送方式，默认"email"
        urgent (bool): 是否紧急，默认False
        *cc_recipients: 抄送接收者
        **delivery_options: 发送选项
    
    返回:
        dict: 发送结果
    """
    notification = {
        "recipient": recipient,
        "message": message,
        "method": method,
        "urgent": urgent,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    if cc_recipients:
        notification["cc_recipients"] = cc_recipients
    
    if delivery_options:
        notification["delivery_options"] = delivery_options
    
    # 模拟发送
    print(f"发送{method}通知给 {recipient}: {message}")
    if urgent:
        print("  [紧急通知]")
    if cc_recipients:
        print(f"  抄送: {', '.join(cc_recipients)}")
    
    return notification


def parameter_combination_demo():
    """
    演示参数组合使用
    """
    # 数据库连接演示
    print("数据库连接演示:")
    
    # 基本连接
    conn1 = create_database_connection("localhost", 5432, "mydb")
    print(f"基本连接: {conn1}")
    
    # 带认证的连接
    conn2 = create_database_connection("192.168.1.100", 3306, "production", 
                                     "admin", "secret123")
    print(f"认证连接: {conn2}")
    
    # 完整配置连接
    conn3 = create_database_connection(
        "db.example.com", 5432, "app_db",
        username="user", password="pass", timeout=60,
        "ssl", "compression",  # options
        pool_size=10, retry_count=3  # config
    )
    print(f"完整连接: {conn3}")
    
    # 通知发送演示
    print("\n通知发送演示:")
    
    # 简单通知
    result1 = send_notification("alice@example.com", "会议提醒")
    print(f"简单通知: {result1}")
    
    # 紧急通知
    result2 = send_notification("bob@example.com", "系统故障", "sms", True)
    print(f"紧急通知: {result2}")
    
    # 完整通知
    result3 = send_notification(
        "team@example.com", "项目更新",
        method="email", urgent=False,
        "manager@example.com", "hr@example.com",  # cc_recipients
        priority="high", retry=True, delay=5  # delivery_options
    )
    print(f"完整通知: {result3}")


if __name__ == "__main__":
    main()