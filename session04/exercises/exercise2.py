#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session04 练习题2：循环语句练习

本练习主要考查循环语句的使用，包括：
1. for循环的基本使用
2. while循环的基本使用
3. 循环控制语句（break、continue）
4. 嵌套循环
5. 循环与条件语句的结合

请在每个函数中实现相应的功能，确保代码能够正确运行。

作者: Python教程团队
创建日期: 2024-12-21
"""


def print_multiplication_table(n):
    """
    练习1：打印乘法表
    
    打印n×n的乘法表，格式要求：
    - 每行显示该行数与1到该行数的乘法结果
    - 使用制表符(\t)分隔，保持对齐
    - 例如：n=3时输出：
      1×1=1
      2×1=2  2×2=4
      3×1=3  3×2=6  3×3=9
    
    参数:
        n (int): 乘法表的大小
    
    返回:
        None (直接打印结果)
    
    示例:
        >>> print_multiplication_table(3)
        1×1=1
        2×1=2	2×2=4
        3×1=3	3×2=6	3×3=9
    """
    # 在这里编写你的代码
    pass


def find_prime_numbers(limit):
    """
    练习2：查找质数
    
    找出小于等于limit的所有质数。
    质数定义：大于1的自然数，除了1和它本身以外不再有其他因数。
    
    参数:
        limit (int): 上限值
    
    返回:
        list: 质数列表
    
    示例:
        >>> find_prime_numbers(20)
        [2, 3, 5, 7, 11, 13, 17, 19]
        >>> find_prime_numbers(10)
        [2, 3, 5, 7]
    """
    # 在这里编写你的代码
    pass


def calculate_factorial(n):
    """
    练习3：计算阶乘
    
    使用循环计算n的阶乘（n!）。
    阶乘定义：n! = n × (n-1) × (n-2) × ... × 2 × 1
    特殊情况：0! = 1
    
    参数:
        n (int): 非负整数
    
    返回:
        int: n的阶乘，如果n为负数则返回None
    
    示例:
        >>> calculate_factorial(5)
        120
        >>> calculate_factorial(0)
        1
        >>> calculate_factorial(-1)
        None
    """
    # 在这里编写你的代码
    pass


def fibonacci_sequence(n):
    """
    练习4：斐波那契数列
    
    生成前n项斐波那契数列。
    斐波那契数列定义：F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2) (n>=2)
    
    参数:
        n (int): 要生成的项数
    
    返回:
        list: 斐波那契数列，如果n<=0则返回空列表
    
    示例:
        >>> fibonacci_sequence(8)
        [0, 1, 1, 2, 3, 5, 8, 13]
        >>> fibonacci_sequence(1)
        [0]
        >>> fibonacci_sequence(0)
        []
    """
    # 在这里编写你的代码
    pass


def count_digits(number):
    """
    练习5：数字统计
    
    统计一个整数中各个数字出现的次数。
    
    参数:
        number (int): 要统计的整数
    
    返回:
        dict: 数字出现次数的字典，键为数字字符，值为出现次数
    
    示例:
        >>> count_digits(112233)
        {'1': 2, '2': 2, '3': 2}
        >>> count_digits(123321)
        {'1': 2, '2': 2, '3': 2}
        >>> count_digits(-456)
        {'4': 1, '5': 1, '6': 1}
    """
    # 在这里编写你的代码
    pass


def find_perfect_numbers(limit):
    """
    练习6：寻找完美数
    
    找出小于等于limit的所有完美数。
    完美数定义：一个正整数，它等于除自身外所有正因数的和。
    例如：6 = 1 + 2 + 3，所以6是完美数。
    
    参数:
        limit (int): 上限值
    
    返回:
        list: 完美数列表
    
    示例:
        >>> find_perfect_numbers(30)
        [6, 28]
        >>> find_perfect_numbers(10)
        [6]
    """
    # 在这里编写你的代码
    pass


def print_diamond_pattern(n):
    """
    练习7：打印钻石图案
    
    打印一个由星号(*)组成的钻石图案，n为钻石的半高。
    
    参数:
        n (int): 钻石的半高（必须为正奇数）
    
    返回:
        None (直接打印结果)
    
    示例:
        >>> print_diamond_pattern(3)
          *
         ***
        *****
         ***
          *
    """
    # 在这里编写你的代码
    pass


def guess_number_game():
    """
    练习8：猜数字游戏
    
    实现一个猜数字游戏：
    1. 程序随机生成1-100之间的数字
    2. 用户输入猜测的数字
    3. 程序提示"太大了"、"太小了"或"恭喜猜对了"
    4. 记录猜测次数
    5. 用户可以输入'quit'退出游戏
    
    返回:
        None (交互式游戏)
    
    注意:
        这是一个交互式函数，需要用户输入
    """
    import random
    
    # 在这里编写你的代码
    pass


def calculate_pi_approximation(iterations):
    """
    练习9：计算π的近似值
    
    使用莱布尼茨公式计算π的近似值：
    π/4 = 1 - 1/3 + 1/5 - 1/7 + 1/9 - 1/11 + ...
    
    参数:
        iterations (int): 迭代次数
    
    返回:
        float: π的近似值
    
    示例:
        >>> abs(calculate_pi_approximation(1000) - 3.14159) < 0.01
        True
    """
    # 在这里编写你的代码
    pass


def find_armstrong_numbers(start, end):
    """
    练习10：寻找阿姆斯特朗数
    
    在指定范围内寻找所有阿姆斯特朗数。
    阿姆斯特朗数定义：一个n位数，其各位数字的n次幂之和等于该数本身。
    例如：153 = 1³ + 5³ + 3³ = 1 + 125 + 27 = 153
    
    参数:
        start (int): 起始值
        end (int): 结束值
    
    返回:
        list: 阿姆斯特朗数列表
    
    示例:
        >>> find_armstrong_numbers(100, 1000)
        [153, 371, 407]
        >>> find_armstrong_numbers(1, 10)
        [1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    # 在这里编写你的代码
    pass


def main():
    """
    主函数：测试所有练习函数
    """
    print("Session04 练习题2：循环语句练习")
    print("=" * 50)
    
    # 测试练习1：乘法表
    print("\n练习1：乘法表测试")
    print("3×3乘法表：")
    print_multiplication_table(3)
    
    # 测试练习2：质数
    print("\n练习2：质数测试")
    primes = find_prime_numbers(30)
    print(f"30以内的质数: {primes}")
    
    # 测试练习3：阶乘
    print("\n练习3：阶乘测试")
    test_factorials = [0, 1, 5, 10, -1]
    for num in test_factorials:
        result = calculate_factorial(num)
        print(f"{num}! = {result}")
    
    # 测试练习4：斐波那契数列
    print("\n练习4：斐波那契数列测试")
    fib_sequences = [0, 1, 8, 10]
    for n in fib_sequences:
        result = fibonacci_sequence(n)
        print(f"前{n}项斐波那契数列: {result}")
    
    # 测试练习5：数字统计
    print("\n练习5：数字统计测试")
    test_numbers = [112233, 123321, -456, 1000]
    for num in test_numbers:
        result = count_digits(num)
        print(f"数字 {num} 的统计结果: {result}")
    
    # 测试练习6：完美数
    print("\n练习6：完美数测试")
    perfect_nums = find_perfect_numbers(1000)
    print(f"1000以内的完美数: {perfect_nums}")
    
    # 测试练习7：钻石图案
    print("\n练习7：钻石图案测试")
    print("钻石图案 (n=3):")
    print_diamond_pattern(3)
    
    # 测试练习9：π近似值
    print("\n练习9：π近似值测试")
    pi_approx = calculate_pi_approximation(10000)
    print(f"π的近似值 (10000次迭代): {pi_approx:.6f}")
    print(f"与真实值的差异: {abs(pi_approx - 3.141592653589793):.6f}")
    
    # 测试练习10：阿姆斯特朗数
    print("\n练习10：阿姆斯特朗数测试")
    armstrong_nums = find_armstrong_numbers(1, 1000)
    print(f"1-1000范围内的阿姆斯特朗数: {armstrong_nums}")
    
    print("\n" + "=" * 50)
    print("循环练习测试完成！")
    print("\n💡 提示：")
    print("1. 如果某些测试结果显示 'None'，说明对应函数还未实现")
    print("2. 练习8是交互式游戏，需要单独运行测试")
    print("3. 注意循环的边界条件和终止条件")
    print("4. 可以尝试优化算法提高效率")
    print("\n🎮 要测试猜数字游戏，请运行：")
    print("guess_number_game()")


if __name__ == "__main__":
    main()