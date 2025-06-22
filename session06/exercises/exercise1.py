#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session 06: 函数编程 - 练习1：基础函数练习

本文件包含函数编程的基础练习题，涵盖函数定义、参数、返回值等基本概念。
请完成所有标记为 TODO 的函数实现。

作者: Python教程团队
创建日期: 2024-12-22
"""


def main():
    """
    主函数：测试所有练习函数
    """
    print("函数编程基础练习")
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


# ==================== 基础函数练习 ====================

def greet_user(name):
    """
    练习1: 创建一个问候函数
    
    要求:
    - 接收一个姓名参数
    - 返回格式为 "你好, {name}!" 的问候语
    
    参数:
        name (str): 用户姓名
    
    返回:
        str: 问候语
    
    示例:
        greet_user("Alice") -> "你好, Alice!"
    """
    # TODO: 实现问候函数
    pass


def calculate_area(length, width):
    """
    练习2: 计算矩形面积
    
    要求:
    - 接收长度和宽度两个参数
    - 返回矩形的面积
    
    参数:
        length (float): 长度
        width (float): 宽度
    
    返回:
        float: 矩形面积
    
    示例:
        calculate_area(5, 3) -> 15.0
    """
    # TODO: 实现面积计算函数
    pass


def is_even(number):
    """
    练习3: 判断数字是否为偶数
    
    要求:
    - 接收一个整数参数
    - 返回布尔值，True表示偶数，False表示奇数
    
    参数:
        number (int): 要判断的数字
    
    返回:
        bool: 是否为偶数
    
    示例:
        is_even(4) -> True
        is_even(5) -> False
    """
    # TODO: 实现偶数判断函数
    pass


def get_absolute_value(number):
    """
    练习4: 计算绝对值
    
    要求:
    - 接收一个数字参数
    - 返回该数字的绝对值
    - 不使用内置的abs()函数
    
    参数:
        number (float): 输入数字
    
    返回:
        float: 绝对值
    
    示例:
        get_absolute_value(-5) -> 5
        get_absolute_value(3) -> 3
    """
    # TODO: 实现绝对值计算函数
    pass


def test_basic_functions():
    """
    测试基础函数
    """
    print("\n=== 基础函数测试 ===")
    
    # 测试问候函数
    print("测试问候函数:")
    try:
        result = greet_user("Alice")
        print(f"greet_user('Alice') = '{result}'")
        assert result == "你好, Alice!", f"期望 '你好, Alice!'，实际 '{result}'"
        print("✓ 问候函数测试通过")
    except Exception as e:
        print(f"✗ 问候函数测试失败: {e}")
    
    # 测试面积计算
    print("\n测试面积计算:")
    try:
        result = calculate_area(5, 3)
        print(f"calculate_area(5, 3) = {result}")
        assert result == 15.0, f"期望 15.0，实际 {result}"
        print("✓ 面积计算测试通过")
    except Exception as e:
        print(f"✗ 面积计算测试失败: {e}")
    
    # 测试偶数判断
    print("\n测试偶数判断:")
    try:
        result1 = is_even(4)
        result2 = is_even(5)
        print(f"is_even(4) = {result1}")
        print(f"is_even(5) = {result2}")
        assert result1 == True, f"期望 True，实际 {result1}"
        assert result2 == False, f"期望 False，实际 {result2}"
        print("✓ 偶数判断测试通过")
    except Exception as e:
        print(f"✗ 偶数判断测试失败: {e}")
    
    # 测试绝对值
    print("\n测试绝对值:")
    try:
        result1 = get_absolute_value(-5)
        result2 = get_absolute_value(3)
        print(f"get_absolute_value(-5) = {result1}")
        print(f"get_absolute_value(3) = {result2}")
        assert result1 == 5, f"期望 5，实际 {result1}"
        assert result2 == 3, f"期望 3，实际 {result2}"
        print("✓ 绝对值测试通过")
    except Exception as e:
        print(f"✗ 绝对值测试失败: {e}")


# ==================== 参数函数练习 ====================

def create_full_name(first_name, last_name, middle_name=""):
    """
    练习5: 创建完整姓名
    
    要求:
    - 接收姓、名和可选的中间名
    - 返回完整的姓名字符串
    - 如果有中间名，格式为 "姓 中间名 名"
    - 如果没有中间名，格式为 "姓 名"
    
    参数:
        first_name (str): 名
        last_name (str): 姓
        middle_name (str): 中间名，默认为空
    
    返回:
        str: 完整姓名
    
    示例:
        create_full_name("三", "张") -> "张 三"
        create_full_name("三", "张", "小") -> "张 小 三"
    """
    # TODO: 实现完整姓名创建函数
    pass


def calculate_total_price(price, quantity=1, discount=0.0, tax_rate=0.1):
    """
    练习6: 计算总价格
    
    要求:
    - 接收商品价格、数量、折扣和税率
    - 计算公式: (价格 * 数量 * (1 - 折扣)) * (1 + 税率)
    - 返回最终价格，保留2位小数
    
    参数:
        price (float): 单价
        quantity (int): 数量，默认1
        discount (float): 折扣率，默认0.0
        tax_rate (float): 税率，默认0.1
    
    返回:
        float: 总价格
    
    示例:
        calculate_total_price(100) -> 110.0
        calculate_total_price(100, 2, 0.1, 0.05) -> 189.0
    """
    # TODO: 实现总价格计算函数
    pass


def format_phone_number(number, country_code="+86", format_style="standard"):
    """
    练习7: 格式化电话号码
    
    要求:
    - 接收电话号码、国家代码和格式样式
    - 支持两种格式:
      - "standard": "+86 138-1234-5678"
      - "compact": "+8613812345678"
    - 假设输入的号码是11位数字字符串
    
    参数:
        number (str): 11位电话号码
        country_code (str): 国家代码，默认"+86"
        format_style (str): 格式样式，默认"standard"
    
    返回:
        str: 格式化的电话号码
    
    示例:
        format_phone_number("13812345678") -> "+86 138-1234-5678"
        format_phone_number("13812345678", "+1", "compact") -> "+113812345678"
    """
    # TODO: 实现电话号码格式化函数
    pass


def calculate_bmi(weight, height, unit="metric"):
    """
    练习8: 计算BMI指数
    
    要求:
    - 接收体重、身高和单位制
    - 支持两种单位制:
      - "metric": 体重(kg)，身高(m)
      - "imperial": 体重(lb)，身高(in)
    - BMI计算公式:
      - 公制: weight / (height^2)
      - 英制: (weight / (height^2)) * 703
    - 返回BMI值，保留1位小数
    
    参数:
        weight (float): 体重
        height (float): 身高
        unit (str): 单位制，默认"metric"
    
    返回:
        float: BMI指数
    
    示例:
        calculate_bmi(70, 1.75) -> 22.9
        calculate_bmi(154, 69, "imperial") -> 22.7
    """
    # TODO: 实现BMI计算函数
    pass


def test_parameter_functions():
    """
    测试参数函数
    """
    print("\n=== 参数函数测试 ===")
    
    # 测试完整姓名
    print("测试完整姓名:")
    try:
        result1 = create_full_name("三", "张")
        result2 = create_full_name("三", "张", "小")
        print(f"create_full_name('三', '张') = '{result1}'")
        print(f"create_full_name('三', '张', '小') = '{result2}'")
        assert result1 == "张 三", f"期望 '张 三'，实际 '{result1}'"
        assert result2 == "张 小 三", f"期望 '张 小 三'，实际 '{result2}'"
        print("✓ 完整姓名测试通过")
    except Exception as e:
        print(f"✗ 完整姓名测试失败: {e}")
    
    # 测试总价格计算
    print("\n测试总价格计算:")
    try:
        result1 = calculate_total_price(100)
        result2 = calculate_total_price(100, 2, 0.1, 0.05)
        print(f"calculate_total_price(100) = {result1}")
        print(f"calculate_total_price(100, 2, 0.1, 0.05) = {result2}")
        assert abs(result1 - 110.0) < 0.01, f"期望 110.0，实际 {result1}"
        assert abs(result2 - 189.0) < 0.01, f"期望 189.0，实际 {result2}"
        print("✓ 总价格计算测试通过")
    except Exception as e:
        print(f"✗ 总价格计算测试失败: {e}")
    
    # 测试电话号码格式化
    print("\n测试电话号码格式化:")
    try:
        result1 = format_phone_number("13812345678")
        result2 = format_phone_number("13812345678", "+1", "compact")
        print(f"format_phone_number('13812345678') = '{result1}'")
        print(f"format_phone_number('13812345678', '+1', 'compact') = '{result2}'")
        assert result1 == "+86 138-1234-5678", f"期望 '+86 138-1234-5678'，实际 '{result1}'"
        assert result2 == "+113812345678", f"期望 '+113812345678'，实际 '{result2}'"
        print("✓ 电话号码格式化测试通过")
    except Exception as e:
        print(f"✗ 电话号码格式化测试失败: {e}")
    
    # 测试BMI计算
    print("\n测试BMI计算:")
    try:
        result1 = calculate_bmi(70, 1.75)
        result2 = calculate_bmi(154, 69, "imperial")
        print(f"calculate_bmi(70, 1.75) = {result1}")
        print(f"calculate_bmi(154, 69, 'imperial') = {result2}")
        assert abs(result1 - 22.9) < 0.1, f"期望 22.9，实际 {result1}"
        assert abs(result2 - 22.7) < 0.1, f"期望 22.7，实际 {result2}"
        print("✓ BMI计算测试通过")
    except Exception as e:
        print(f"✗ BMI计算测试失败: {e}")


# ==================== 返回值函数练习 ====================

def get_min_max(numbers):
    """
    练习9: 获取列表的最小值和最大值
    
    要求:
    - 接收一个数字列表
    - 返回元组 (最小值, 最大值)
    - 如果列表为空，返回 (None, None)
    
    参数:
        numbers (list): 数字列表
    
    返回:
        tuple: (最小值, 最大值)
    
    示例:
        get_min_max([1, 5, 3, 9, 2]) -> (1, 9)
        get_min_max([]) -> (None, None)
    """
    # TODO: 实现最小值最大值获取函数
    pass


def split_name(full_name):
    """
    练习10: 分割姓名
    
    要求:
    - 接收完整姓名字符串
    - 返回元组 (姓, 名)
    - 假设姓名格式为 "姓 名" 或 "姓名"（两个字符）
    - 如果包含空格，按空格分割
    - 如果不包含空格且长度为2，第一个字符为姓，第二个为名
    - 其他情况返回 (full_name, "")
    
    参数:
        full_name (str): 完整姓名
    
    返回:
        tuple: (姓, 名)
    
    示例:
        split_name("张 三") -> ("张", "三")
        split_name("李四") -> ("李", "四")
        split_name("王小明") -> ("王小明", "")
    """
    # TODO: 实现姓名分割函数
    pass


def calculate_statistics(numbers):
    """
    练习11: 计算统计信息
    
    要求:
    - 接收数字列表
    - 返回字典，包含以下统计信息:
      - count: 数字个数
      - sum: 总和
      - average: 平均值（保留2位小数）
      - min: 最小值
      - max: 最大值
    - 如果列表为空，所有值设为0或None
    
    参数:
        numbers (list): 数字列表
    
    返回:
        dict: 统计信息字典
    
    示例:
        calculate_statistics([1, 2, 3, 4, 5]) -> 
        {'count': 5, 'sum': 15, 'average': 3.0, 'min': 1, 'max': 5}
    """
    # TODO: 实现统计信息计算函数
    pass


def parse_email(email):
    """
    练习12: 解析邮箱地址
    
    要求:
    - 接收邮箱地址字符串
    - 返回字典，包含:
      - username: 用户名（@之前的部分）
      - domain: 域名（@之后的部分）
      - is_valid: 是否为有效邮箱（包含且仅包含一个@符号）
    
    参数:
        email (str): 邮箱地址
    
    返回:
        dict: 邮箱信息字典
    
    示例:
        parse_email("user@example.com") -> 
        {'username': 'user', 'domain': 'example.com', 'is_valid': True}
        parse_email("invalid-email") -> 
        {'username': '', 'domain': '', 'is_valid': False}
    """
    # TODO: 实现邮箱解析函数
    pass


def test_return_functions():
    """
    测试返回值函数
    """
    print("\n=== 返回值函数测试 ===")
    
    # 测试最小值最大值
    print("测试最小值最大值:")
    try:
        result1 = get_min_max([1, 5, 3, 9, 2])
        result2 = get_min_max([])
        print(f"get_min_max([1, 5, 3, 9, 2]) = {result1}")
        print(f"get_min_max([]) = {result2}")
        assert result1 == (1, 9), f"期望 (1, 9)，实际 {result1}"
        assert result2 == (None, None), f"期望 (None, None)，实际 {result2}"
        print("✓ 最小值最大值测试通过")
    except Exception as e:
        print(f"✗ 最小值最大值测试失败: {e}")
    
    # 测试姓名分割
    print("\n测试姓名分割:")
    try:
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
    except Exception as e:
        print(f"✗ 姓名分割测试失败: {e}")
    
    # 测试统计信息
    print("\n测试统计信息:")
    try:
        result = calculate_statistics([1, 2, 3, 4, 5])
        print(f"calculate_statistics([1, 2, 3, 4, 5]) = {result}")
        expected = {'count': 5, 'sum': 15, 'average': 3.0, 'min': 1, 'max': 5}
        assert result == expected, f"期望 {expected}，实际 {result}"
        print("✓ 统计信息测试通过")
    except Exception as e:
        print(f"✗ 统计信息测试失败: {e}")
    
    # 测试邮箱解析
    print("\n测试邮箱解析:")
    try:
        result1 = parse_email("user@example.com")
        result2 = parse_email("invalid-email")
        print(f"parse_email('user@example.com') = {result1}")
        print(f"parse_email('invalid-email') = {result2}")
        expected1 = {'username': 'user', 'domain': 'example.com', 'is_valid': True}
        expected2 = {'username': '', 'domain': '', 'is_valid': False}
        assert result1 == expected1, f"期望 {expected1}，实际 {result1}"
        assert result2 == expected2, f"期望 {expected2}，实际 {result2}"
        print("✓ 邮箱解析测试通过")
    except Exception as e:
        print(f"✗ 邮箱解析测试失败: {e}")


# ==================== 数学函数练习 ====================

def calculate_factorial(n):
    """
    练习13: 计算阶乘（迭代方式）
    
    要求:
    - 接收非负整数n
    - 返回n的阶乘
    - 使用迭代方式实现，不使用递归
    - 0! = 1
    
    参数:
        n (int): 非负整数
    
    返回:
        int: n的阶乘
    
    示例:
        calculate_factorial(5) -> 120
        calculate_factorial(0) -> 1
    """
    # TODO: 实现阶乘计算函数（迭代方式）
    pass


def is_prime(n):
    """
    练习14: 判断是否为质数
    
    要求:
    - 接收正整数n
    - 返回布尔值，True表示质数，False表示合数
    - 1不是质数
    - 优化算法，只需检查到sqrt(n)
    
    参数:
        n (int): 正整数
    
    返回:
        bool: 是否为质数
    
    示例:
        is_prime(7) -> True
        is_prime(8) -> False
        is_prime(1) -> False
    """
    # TODO: 实现质数判断函数
    pass


def gcd(a, b):
    """
    练习15: 计算最大公约数
    
    要求:
    - 接收两个正整数
    - 返回它们的最大公约数
    - 使用欧几里得算法
    
    参数:
        a (int): 正整数
        b (int): 正整数
    
    返回:
        int: 最大公约数
    
    示例:
        gcd(48, 18) -> 6
        gcd(17, 13) -> 1
    """
    # TODO: 实现最大公约数计算函数
    pass


def fibonacci_iterative(n):
    """
    练习16: 计算斐波那契数列（迭代方式）
    
    要求:
    - 接收非负整数n
    - 返回斐波那契数列的第n项
    - 使用迭代方式实现，不使用递归
    - F(0) = 0, F(1) = 1
    
    参数:
        n (int): 非负整数
    
    返回:
        int: 斐波那契数列的第n项
    
    示例:
        fibonacci_iterative(6) -> 8
        fibonacci_iterative(0) -> 0
    """
    # TODO: 实现斐波那契数列计算函数（迭代方式）
    pass


def test_math_functions():
    """
    测试数学函数
    """
    print("\n=== 数学函数测试 ===")
    
    # 测试阶乘计算
    print("测试阶乘计算:")
    try:
        result1 = calculate_factorial(5)
        result2 = calculate_factorial(0)
        print(f"calculate_factorial(5) = {result1}")
        print(f"calculate_factorial(0) = {result2}")
        assert result1 == 120, f"期望 120，实际 {result1}"
        assert result2 == 1, f"期望 1，实际 {result2}"
        print("✓ 阶乘计算测试通过")
    except Exception as e:
        print(f"✗ 阶乘计算测试失败: {e}")
    
    # 测试质数判断
    print("\n测试质数判断:")
    try:
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
    except Exception as e:
        print(f"✗ 质数判断测试失败: {e}")
    
    # 测试最大公约数
    print("\n测试最大公约数:")
    try:
        result1 = gcd(48, 18)
        result2 = gcd(17, 13)
        print(f"gcd(48, 18) = {result1}")
        print(f"gcd(17, 13) = {result2}")
        assert result1 == 6, f"期望 6，实际 {result1}"
        assert result2 == 1, f"期望 1，实际 {result2}"
        print("✓ 最大公约数测试通过")
    except Exception as e:
        print(f"✗ 最大公约数测试失败: {e}")
    
    # 测试斐波那契数列
    print("\n测试斐波那契数列:")
    try:
        result1 = fibonacci_iterative(6)
        result2 = fibonacci_iterative(0)
        print(f"fibonacci_iterative(6) = {result1}")
        print(f"fibonacci_iterative(0) = {result2}")
        assert result1 == 8, f"期望 8，实际 {result1}"
        assert result2 == 0, f"期望 0，实际 {result2}"
        print("✓ 斐波那契数列测试通过")
    except Exception as e:
        print(f"✗ 斐波那契数列测试失败: {e}")


# ==================== 字符串函数练习 ====================

def count_words(text):
    """
    练习17: 统计单词数量
    
    要求:
    - 接收文本字符串
    - 返回单词数量
    - 单词以空格分隔
    - 忽略前后空格
    
    参数:
        text (str): 输入文本
    
    返回:
        int: 单词数量
    
    示例:
        count_words("Hello world Python") -> 3
        count_words("  Hello  world  ") -> 2
    """
    # TODO: 实现单词计数函数
    pass


def reverse_words(text):
    """
    练习18: 反转单词顺序
    
    要求:
    - 接收文本字符串
    - 返回单词顺序反转后的字符串
    - 保持单词内部字符顺序不变
    - 单词间用单个空格分隔
    
    参数:
        text (str): 输入文本
    
    返回:
        str: 单词顺序反转后的文本
    
    示例:
        reverse_words("Hello world Python") -> "Python world Hello"
        reverse_words("  a  b  c  ") -> "c b a"
    """
    # TODO: 实现单词顺序反转函数
    pass


def is_palindrome(text):
    """
    练习19: 判断是否为回文
    
    要求:
    - 接收文本字符串
    - 返回布尔值，True表示回文，False表示非回文
    - 忽略大小写和空格
    - 只考虑字母和数字字符
    
    参数:
        text (str): 输入文本
    
    返回:
        bool: 是否为回文
    
    示例:
        is_palindrome("A man a plan a canal Panama") -> True
        is_palindrome("race a car") -> False
    """
    # TODO: 实现回文判断函数
    pass


def capitalize_words(text):
    """
    练习20: 首字母大写
    
    要求:
    - 接收文本字符串
    - 返回每个单词首字母大写的字符串
    - 其他字母小写
    - 保持原有的空格分布
    
    参数:
        text (str): 输入文本
    
    返回:
        str: 首字母大写后的文本
    
    示例:
        capitalize_words("hello WORLD python") -> "Hello World Python"
        capitalize_words("  hello  world  ") -> "  Hello  World  "
    """
    # TODO: 实现首字母大写函数
    pass


def test_string_functions():
    """
    测试字符串函数
    """
    print("\n=== 字符串函数测试 ===")
    
    # 测试单词计数
    print("测试单词计数:")
    try:
        result1 = count_words("Hello world Python")
        result2 = count_words("  Hello  world  ")
        print(f"count_words('Hello world Python') = {result1}")
        print(f"count_words('  Hello  world  ') = {result2}")
        assert result1 == 3, f"期望 3，实际 {result1}"
        assert result2 == 2, f"期望 2，实际 {result2}"
        print("✓ 单词计数测试通过")
    except Exception as e:
        print(f"✗ 单词计数测试失败: {e}")
    
    # 测试单词顺序反转
    print("\n测试单词顺序反转:")
    try:
        result1 = reverse_words("Hello world Python")
        result2 = reverse_words("  a  b  c  ")
        print(f"reverse_words('Hello world Python') = '{result1}'")
        print(f"reverse_words('  a  b  c  ') = '{result2}'")
        assert result1 == "Python world Hello", f"期望 'Python world Hello'，实际 '{result1}'"
        assert result2 == "c b a", f"期望 'c b a'，实际 '{result2}'"
        print("✓ 单词顺序反转测试通过")
    except Exception as e:
        print(f"✗ 单词顺序反转测试失败: {e}")
    
    # 测试回文判断
    print("\n测试回文判断:")
    try:
        result1 = is_palindrome("A man a plan a canal Panama")
        result2 = is_palindrome("race a car")
        print(f"is_palindrome('A man a plan a canal Panama') = {result1}")
        print(f"is_palindrome('race a car') = {result2}")
        assert result1 == True, f"期望 True，实际 {result1}"
        assert result2 == False, f"期望 False，实际 {result2}"
        print("✓ 回文判断测试通过")
    except Exception as e:
        print(f"✗ 回文判断测试失败: {e}")
    
    # 测试首字母大写
    print("\n测试首字母大写:")
    try:
        result1 = capitalize_words("hello WORLD python")
        result2 = capitalize_words("  hello  world  ")
        print(f"capitalize_words('hello WORLD python') = '{result1}'")
        print(f"capitalize_words('  hello  world  ') = '{result2}'")
        assert result1 == "Hello World Python", f"期望 'Hello World Python'，实际 '{result1}'"
        assert result2 == "  Hello  World  ", f"期望 '  Hello  World  '，实际 '{result2}'"
        print("✓ 首字母大写测试通过")
    except Exception as e:
        print(f"✗ 首字母大写测试失败: {e}")


if __name__ == "__main__":
    main()