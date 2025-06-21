#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session04 练习题2解答：循环语句练习

本文件包含exercise2.py中所有练习题的参考解答。
这些解答展示了循环语句的正确使用方法和最佳实践。

作者: Python教程团队
创建日期: 2024-12-21
"""


def print_multiplication_table(n):
    """
    练习1解答：打印乘法表
    """
    for i in range(1, n + 1):
        line = []
        for j in range(1, i + 1):
            line.append(f"{i}×{j}={i*j}")
        print("\t".join(line))


def find_prime_numbers(limit):
    """
    练习2解答：查找质数
    """
    if limit < 2:
        return []
    
    primes = []
    for num in range(2, limit + 1):
        is_prime = True
        # 只需要检查到sqrt(num)
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    
    return primes


def calculate_factorial(n):
    """
    练习3解答：计算阶乘
    """
    if n < 0:
        return None
    
    result = 1
    for i in range(1, n + 1):
        result *= i
    
    return result


def fibonacci_sequence(n):
    """
    练习4解答：斐波那契数列
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    
    return fib


def count_digits(number):
    """
    练习5解答：数字统计
    """
    # 转换为字符串并去掉负号
    num_str = str(abs(number))
    
    digit_count = {}
    for digit in num_str:
        digit_count[digit] = digit_count.get(digit, 0) + 1
    
    return digit_count


def find_perfect_numbers(limit):
    """
    练习6解答：寻找完美数
    """
    perfect_numbers = []
    
    for num in range(2, limit + 1):
        divisors_sum = 0
        # 找出所有真因数（除了自身的因数）
        for i in range(1, num):
            if num % i == 0:
                divisors_sum += i
        
        if divisors_sum == num:
            perfect_numbers.append(num)
    
    return perfect_numbers


def print_diamond_pattern(n):
    """
    练习7解答：打印钻石图案
    """
    if n % 2 == 0:
        print("n必须为奇数")
        return
    
    # 上半部分（包括中间）
    for i in range(n):
        spaces = " " * (n - 1 - i)
        stars = "*" * (2 * i + 1)
        print(spaces + stars)
    
    # 下半部分
    for i in range(n - 2, -1, -1):
        spaces = " " * (n - 1 - i)
        stars = "*" * (2 * i + 1)
        print(spaces + stars)


def guess_number_game():
    """
    练习8解答：猜数字游戏
    """
    import random
    
    target = random.randint(1, 100)
    attempts = 0
    
    print("🎮 欢迎来到猜数字游戏！")
    print("我已经想好了一个1-100之间的数字，请你来猜猜看！")
    print("输入'quit'可以退出游戏")
    
    while True:
        try:
            user_input = input("\n请输入你的猜测: ").strip()
            
            if user_input.lower() == 'quit':
                print(f"游戏结束！答案是 {target}")
                break
            
            guess = int(user_input)
            attempts += 1
            
            if guess < 1 or guess > 100:
                print("请输入1-100之间的数字！")
                continue
            
            if guess == target:
                print(f"🎉 恭喜你猜对了！答案就是 {target}")
                print(f"你总共猜了 {attempts} 次")
                break
            elif guess < target:
                print("太小了！再试试更大的数字")
            else:
                print("太大了！再试试更小的数字")
                
        except ValueError:
            print("请输入有效的数字！")


def calculate_pi_approximation(iterations):
    """
    练习9解答：计算π的近似值
    """
    pi_quarter = 0
    
    for i in range(iterations):
        # 莱布尼茨公式：π/4 = 1 - 1/3 + 1/5 - 1/7 + ...
        term = 1 / (2 * i + 1)
        if i % 2 == 0:
            pi_quarter += term
        else:
            pi_quarter -= term
    
    return pi_quarter * 4


def find_armstrong_numbers(start, end):
    """
    练习10解答：寻找阿姆斯特朗数
    """
    armstrong_numbers = []
    
    for num in range(start, end + 1):
        # 转换为字符串以获取位数
        num_str = str(num)
        num_digits = len(num_str)
        
        # 计算各位数字的n次幂之和
        digit_sum = sum(int(digit) ** num_digits for digit in num_str)
        
        if digit_sum == num:
            armstrong_numbers.append(num)
    
    return armstrong_numbers


def main():
    """
    主函数：测试所有解答函数
    """
    print("Session04 练习题2解答：循环语句练习")
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
    print("循环练习解答测试完成！")
    print("\n📝 学习要点：")
    print("1. for循环适合已知次数的循环")
    print("2. while循环适合条件控制的循环")
    print("3. 注意循环的边界条件和终止条件")
    print("4. 合理使用break和continue优化循环逻辑")
    print("5. 嵌套循环要注意时间复杂度")
    print("\n🎮 要测试猜数字游戏，请运行：")
    print("guess_number_game()")


if __name__ == "__main__":
    main()