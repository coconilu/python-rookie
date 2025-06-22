#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session 06: 函数编程 - 练习1答案：基础函数练习

本文件包含练习1的完整答案实现。

作者: Python教程团队
创建日期: 2024-12-22
"""

import math


def main():
    """
    主函数：测试所有练习函数
    """
    print("函数编程基础练习 - 答案版本")
    print("=" * 40)
    
    # 测试基础函数
    test_basic_functions()
    
    # 测试参数函数
    test_parameter_functions()
    
    # 测试返回值函数
    test_return_functions()
    
    # 测试数学函数
    test_math_functions()
    
    # 测试字符串函数
    test_string_functions()
    
    print("\n所有练习测试完成！")


# ==================== 基础函数练习答案 ====================

def greet_user(name):
    """
    练习1答案: 创建一个问候函数
    """
    return f"你好, {name}!"


def calculate_area(length, width):
    """
    练习2答案: 计算矩形面积
    """
    return float(length * width)


def is_even(number):
    """
    练习3答案: 判断数字是否为偶数
    """
    return number % 2 == 0


def get_absolute_value(number):
    """
    练习4答案: 计算绝对值
    """
    if number < 0:
        return -number
    else:
        return number


def test_basic_functions():
    """
    测试基础函数
    """
    print("\n=== 基础函数测试 ===")
    
    # 测试问候函数
    print("测试问候函数:")
    result = greet_user("Alice")
    print(f"greet_user('Alice') = '{result}'")
    assert result == "你好, Alice!", f"期望 '你好, Alice!'，实际 '{result}'"
    print("✓ 问候函数测试通过")
    
    # 测试面积计算
    print("\n测试面积计算:")
    result = calculate_area(5, 3)
    print(f"calculate_area(5, 3) = {result}")
    assert result == 15.0, f"期望 15.0，实际 {result}"
    print("✓ 面积计算测试通过")
    
    # 测试偶数判断
    print("\n测试偶数判断:")
    result1 = is_even(4)
    result2 = is_even(5)
    print(f"is_even(4) = {result1}")
    print(f"is_even(5) = {result2}")
    assert result1 == True, f"期望 True，实际 {result1}"
    assert result2 == False, f"期望 False，实际 {result2}"
    print("✓ 偶数判断测试通过")
    
    # 测试绝对值
    print("\n测试绝对值:")
    result1 = get_absolute_value(-5)
    result2 = get_absolute_value(3)
    print(f"get_absolute_value(-5) = {result1}")
    print(f"get_absolute_value(3) = {result2}")
    assert result1 == 5, f"期望 5，实际 {result1}"
    assert result2 == 3, f"期望 3，实际 {result2}"
    print("✓ 绝对值测试通过")


# ==================== 参数函数练习答案 ====================

def create_full_name(first_name, last_name, middle_name=""):
    """
    练习5答案: 创建完整姓名
    """
    if middle_name:
        return f"{last_name} {middle_name} {first_name}"
    else:
        return f"{last_name} {first_name}"


def calculate_total_price(price, quantity=1, discount=0.0, tax_rate=0.1):
    """
    练习6答案: 计算总价格
    """
    subtotal = price * quantity * (1 - discount)
    total = subtotal * (1 + tax_rate)
    return round(total, 2)


def format_phone_number(number, country_code="+86", format_style="standard"):
    """
    练习7答案: 格式化电话号码
    """
    if format_style == "standard":
        # 格式: +86 138-1234-5678
        formatted = f"{number[:3]}-{number[3:7]}-{number[7:]}"
        return f"{country_code} {formatted}"
    elif format_style == "compact":
        # 格式: +8613812345678
        return f"{country_code}{number}"
    else:
        return f"{country_code} {number}"


def calculate_bmi(weight, height, unit="metric"):
    """
    练习8答案: 计算BMI指数
    """
    if unit == "metric":
        # 公制: weight(kg) / height(m)^2
        bmi = weight / (height ** 2)
    elif unit == "imperial":
        # 英制: (weight(lb) / height(in)^2) * 703
        bmi = (weight / (height ** 2)) * 703
    else:
        raise ValueError("不支持的单位制")
    
    return round(bmi, 1)


def test_parameter_functions():
    """
    测试参数函数
    """
    print("\n=== 参数函数测试 ===")
    
    # 测试完整姓名
    print("测试完整姓名:")
    result1 = create_full_name("三", "张")
    result2 = create_full_name("三", "张", "小")
    print(f"create_full_name('三', '张') = '{result1}'")
    print(f"create_full_name('三', '张', '小') = '{result2}'")
    assert result1 == "张 三", f"期望 '张 三'，实际 '{result1}'"
    assert result2 == "张 小 三", f"期望 '张 小 三'，实际 '{result2}'"
    print("✓ 完整姓名测试通过")
    
    # 测试总价格计算
    print("\n测试总价格计算:")
    result1 = calculate_total_price(100)
    result2 = calculate_total_price(100, 2, 0.1, 0.05)
    print(f"calculate_total_price(100) = {result1}")
    print(f"calculate_total_price(100, 2, 0.1, 0.05) = {result2}")
    assert abs(result1 - 110.0) < 0.01, f"期望 110.0，实际 {result1}"
    assert abs(result2 - 189.0) < 0.01, f"期望 189.0，实际 {result2}"
    print("✓ 总价格计算测试通过")
    
    # 测试电话号码格式化
    print("\n测试电话号码格式化:")
    result1 = format_phone_number("13812345678")
    result2 = format_phone_number("13812345678", "+1", "compact")
    print(f"format_phone_number('13812345678') = '{result1}'")
    print(f"format_phone_number('13812345678', '+1', 'compact') = '{result2}'")
    assert result1 == "+86 138-1234-5678", f"期望 '+86 138-1234-5678'，实际 '{result1}'"
    assert result2 == "+113812345678", f"期望 '+113812345678'，实际 '{result2}'"
    print("✓ 电话号码格式化测试通过")
    
    # 测试BMI计算
    print("\n测试BMI计算:")
    result1 = calculate_bmi(70, 1.75)
    result2 = calculate_bmi(154, 69, "imperial")
    print(f"calculate_bmi(70, 1.75) = {result1}")
    print(f"calculate_bmi(154, 69, 'imperial') = {result2}")
    assert abs(result1 - 22.9) < 0.1, f"期望 22.9，实际 {result1}"
    assert abs(result2 - 22.7) < 0.1, f"期望 22.7，实际 {result2}"
    print("✓ BMI计算测试通过")


# ==================== 返回值函数练习答案 ====================

def get_min_max(numbers):
    """
    练习9答案: 获取列表的最小值和最大值
    """
    if not numbers:
        return None, None
    return min(numbers), max(numbers)


def split_name(full_name):
    """
    练习10答案: 分割姓名
    """
    full_name = full_name.strip()
    
    if " " in full_name:
        # 包含空格，按空格分割
        parts = full_name.split(" ", 1)
        return parts[0], parts[1]
    elif len(full_name) == 2:
        # 不包含空格且长度为2
        return full_name[0], full_name[1]
    else:
        # 其他情况
        return full_name, ""


def calculate_statistics(numbers):
    """
    练习11答案: 计算统计信息
    """
    if not numbers:
        return {
            'count': 0,
            'sum': 0,
            'average': 0,
            'min': None,
            'max': None
        }
    
    count = len(numbers)
    total = sum(numbers)
    average = round(total / count, 2)
    minimum = min(numbers)
    maximum = max(numbers)
    
    return {
        'count': count,
        'sum': total,
        'average': average,
        'min': minimum,
        'max': maximum
    }


def parse_email(email):
    """
    练习12答案: 解析邮箱地址
    """
    at_count = email.count('@')
    
    if at_count == 1:
        username, domain = email.split('@')
        return {
            'username': username,
            'domain': domain,
            'is_valid': True
        }
    else:
        return {
            'username': '',
            'domain': '',
            'is_valid': False
        }


def test_return_functions():
    """
    测试返回值函数
    """
    print("\n=== 返回值函数测试 ===")
    
    # 测试最小值最大值
    print("测试最小值最大值:")
    result1 = get_min_max([1, 5, 3, 9, 2])
    result2 = get_min_max([])
    print(f"get_min_max([1, 5, 3, 9, 2]) = {result1}")
    print(f"get_min_max([]) = {result2}")
    assert result1 == (1, 9), f"期望 (1, 9)，实际 {result1}"
    assert result2 == (None, None), f"期望 (None, None)，实际 {result2}"
    print("✓ 最小值最大值测试通过")
    
    # 测试姓名分割
    print("\n测试姓名分割:")
    result1 = split_name("张 三")
    result2 = split_name("李四")
    result3 = split_name("王小明")
    print(f"split_name('张 三') = {result1}")
    print(f"split_name('李四') = {result2}")
    print(f"split_name('王小明') = {result3}")
    assert result1 == ("张", "三"), f"期望 ('张', '三')，实际 {result1}"
    assert result2 == ("李", "四"), f"期望 ('李', '四')，实际 {result2}"
    assert result3 == ("王小明", ""), f"期望 ('王小明', '')，实际 {result3}"
    print("✓ 姓名分割测试通过")
    
    # 测试统计信息
    print("\n测试统计信息:")
    result = calculate_statistics([1, 2, 3, 4, 5])
    print(f"calculate_statistics([1, 2, 3, 4, 5]) = {result}")
    expected = {'count': 5, 'sum': 15, 'average': 3.0, 'min': 1, 'max': 5}
    assert result == expected, f"期望 {expected}，实际 {result}"
    print("✓ 统计信息测试通过")
    
    # 测试邮箱解析
    print("\n测试邮箱解析:")
    result1 = parse_email("user@example.com")
    result2 = parse_email("invalid-email")
    print(f"parse_email('user@example.com') = {result1}")
    print(f"parse_email('invalid-email') = {result2}")
    expected1 = {'username': 'user', 'domain': 'example.com', 'is_valid': True}
    expected2 = {'username': '', 'domain': '', 'is_valid': False}
    assert result1 == expected1, f"期望 {expected1}，实际 {result1}"
    assert result2 == expected2, f"期望 {expected2}，实际 {result2}"
    print("✓ 邮箱解析测试通过")


# ==================== 数学函数练习答案 ====================

def calculate_factorial(n):
    """
    练习13答案: 计算阶乘（迭代方式）
    """
    if n < 0:
        raise ValueError("阶乘不能计算负数")
    
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def is_prime(n):
    """
    练习14答案: 判断是否为质数
    """
    if n < 2:
        return False
    
    if n == 2:
        return True
    
    if n % 2 == 0:
        return False
    
    # 只需检查到sqrt(n)
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    
    return True


def gcd(a, b):
    """
    练习15答案: 计算最大公约数（欧几里得算法）
    """
    while b:
        a, b = b, a % b
    return a


def fibonacci_iterative(n):
    """
    练习16答案: 计算斐波那契数列（迭代方式）
    """
    if n < 0:
        raise ValueError("斐波那契数列不能计算负数")
    
    if n <= 1:
        return n
    
    prev, curr = 0, 1
    for i in range(2, n + 1):
        prev, curr = curr, prev + curr
    
    return curr


def test_math_functions():
    """
    测试数学函数
    """
    print("\n=== 数学函数测试 ===")
    
    # 测试阶乘计算
    print("测试阶乘计算:")
    result1 = calculate_factorial(5)
    result2 = calculate_factorial(0)
    print(f"calculate_factorial(5) = {result1}")
    print(f"calculate_factorial(0) = {result2}")
    assert result1 == 120, f"期望 120，实际 {result1}"
    assert result2 == 1, f"期望 1，实际 {result2}"
    print("✓ 阶乘计算测试通过")
    
    # 测试质数判断
    print("\n测试质数判断:")
    result1 = is_prime(7)
    result2 = is_prime(8)
    result3 = is_prime(1)
    print(f"is_prime(7) = {result1}")
    print(f"is_prime(8) = {result2}")
    print(f"is_prime(1) = {result3}")
    assert result1 == True, f"期望 True，实际 {result1}"
    assert result2 == False, f"期望 False，实际 {result2}"
    assert result3 == False, f"期望 False，实际 {result3}"
    print("✓ 质数判断测试通过")
    
    # 测试最大公约数
    print("\n测试最大公约数:")
    result1 = gcd(48, 18)
    result2 = gcd(17, 13)
    print(f"gcd(48, 18) = {result1}")
    print(f"gcd(17, 13) = {result2}")
    assert result1 == 6, f"期望 6，实际 {result1}"
    assert result2 == 1, f"期望 1，实际 {result2}"
    print("✓ 最大公约数测试通过")
    
    # 测试斐波那契数列
    print("\n测试斐波那契数列:")
    result1 = fibonacci_iterative(6)
    result2 = fibonacci_iterative(0)
    print(f"fibonacci_iterative(6) = {result1}")
    print(f"fibonacci_iterative(0) = {result2}")
    assert result1 == 8, f"期望 8，实际 {result1}"
    assert result2 == 0, f"期望 0，实际 {result2}"
    print("✓ 斐波那契数列测试通过")


# ==================== 字符串函数练习答案 ====================

def count_words(text):
    """
    练习17答案: 统计单词数量
    """
    text = text.strip()
    if not text:
        return 0
    return len(text.split())


def reverse_words(text):
    """
    练习18答案: 反转单词顺序
    """
    words = text.split()
    return " ".join(reversed(words))


def is_palindrome(text):
    """
    练习19答案: 判断是否为回文
    """
    # 只保留字母和数字，转换为小写
    cleaned = ''.join(char.lower() for char in text if char.isalnum())
    
    # 检查是否为回文
    return cleaned == cleaned[::-1]


def capitalize_words(text):
    """
    练习20答案: 首字母大写
    """
    words = text.split(' ')
    capitalized_words = [word.capitalize() for word in words]
    return ' '.join(capitalized_words)


def test_string_functions():
    """
    测试字符串函数
    """
    print("\n=== 字符串函数测试 ===")
    
    # 测试单词计数
    print("测试单词计数:")
    result1 = count_words("Hello world Python")
    result2 = count_words("  Hello  world  ")
    print(f"count_words('Hello world Python') = {result1}")
    print(f"count_words('  Hello  world  ') = {result2}")
    assert result1 == 3, f"期望 3，实际 {result1}"
    assert result2 == 2, f"期望 2，实际 {result2}"
    print("✓ 单词计数测试通过")
    
    # 测试单词顺序反转
    print("\n测试单词顺序反转:")
    result1 = reverse_words("Hello world Python")
    result2 = reverse_words("  a  b  c  ")
    print(f"reverse_words('Hello world Python') = '{result1}'")
    print(f"reverse_words('  a  b  c  ') = '{result2}'")
    assert result1 == "Python world Hello", f"期望 'Python world Hello'，实际 '{result1}'"
    assert result2 == "c b a", f"期望 'c b a'，实际 '{result2}'"
    print("✓ 单词顺序反转测试通过")
    
    # 测试回文判断
    print("\n测试回文判断:")
    result1 = is_palindrome("A man a plan a canal Panama")
    result2 = is_palindrome("race a car")
    print(f"is_palindrome('A man a plan a canal Panama') = {result1}")
    print(f"is_palindrome('race a car') = {result2}")
    assert result1 == True, f"期望 True，实际 {result1}"
    assert result2 == False, f"期望 False，实际 {result2}"
    print("✓ 回文判断测试通过")
    
    # 测试首字母大写
    print("\n测试首字母大写:")
    result1 = capitalize_words("hello WORLD python")
    result2 = capitalize_words("  hello  world  ")
    print(f"capitalize_words('hello WORLD python') = '{result1}'")
    print(f"capitalize_words('  hello  world  ') = '{result2}'")
    assert result1 == "Hello World Python", f"期望 'Hello World Python'，实际 '{result1}'"
    assert result2 == "  Hello  World  ", f"期望 '  Hello  World  '，实际 '{result2}'"
    print("✓ 首字母大写测试通过")


if __name__ == "__main__":
    main()