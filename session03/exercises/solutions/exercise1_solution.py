#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session03 练习题1解答：基础运算练习

这个文件包含了exercise1.py中所有练习题的参考解答。
学习者可以参考这些解答来检查自己的实现，
但建议先独立完成练习再查看解答。
"""

import math


def basic_calculator(a, b, operation):
    """
    基本计算器实现
    """
    if operation == '+':
        return a + b
    elif operation == '-':
        return a - b
    elif operation == '*':
        return a * b
    elif operation == '/':
        if b == 0:
            return "错误：除数不能为零"
        return a / b
    elif operation == '//':
        if b == 0:
            return "错误：除数不能为零"
        return a // b
    elif operation == '%':
        if b == 0:
            return "错误：除数不能为零"
        return a % b
    elif operation == '**':
        return a ** b
    else:
        return "错误：不支持的运算符"


def temperature_converter(temp, from_unit, to_unit):
    """
    温度转换器实现
    """
    # 先转换为摄氏度
    if from_unit == 'F':
        celsius = (temp - 32) * 5 / 9
    elif from_unit == 'K':
        celsius = temp - 273.15
    else:  # 'C'
        celsius = temp
    
    # 再从摄氏度转换为目标单位
    if to_unit == 'F':
        return celsius * 9 / 5 + 32
    elif to_unit == 'K':
        return celsius + 273.15
    else:  # 'C'
        return celsius


def bmi_calculator(weight, height):
    """
    BMI计算器实现
    """
    if height <= 0 or weight <= 0:
        return {"bmi": 0, "category": "输入错误"}
    
    bmi = weight / (height ** 2)
    
    if bmi < 18.5:
        category = "偏瘦"
    elif bmi < 24:
        category = "正常"
    elif bmi < 28:
        category = "偏胖"
    else:
        category = "肥胖"
    
    return {"bmi": round(bmi, 2), "category": category}


def circle_calculator(radius):
    """
    圆形计算器实现
    """
    if radius <= 0:
        return {"area": 0, "circumference": 0, "error": "半径必须大于0"}
    
    area = math.pi * radius ** 2
    circumference = 2 * math.pi * radius
    
    return {
        "area": round(area, 2),
        "circumference": round(circumference, 2)
    }


def compound_interest_calculator(principal, rate, time, compound_frequency=1):
    """
    复利计算器实现
    """
    if principal <= 0 or rate < 0 or time <= 0 or compound_frequency <= 0:
        return {"final_amount": 0, "interest_earned": 0, "error": "输入参数错误"}
    
    # 复利公式: A = P(1 + r/n)^(nt)
    final_amount = principal * (1 + rate / compound_frequency) ** (compound_frequency * time)
    interest_earned = final_amount - principal
    
    return {
        "final_amount": round(final_amount, 2),
        "interest_earned": round(interest_earned, 2)
    }


def triangle_area_calculator(a, b, c):
    """
    三角形面积计算器实现（海伦公式）
    """
    # 检查是否能构成三角形
    if a <= 0 or b <= 0 or c <= 0:
        return {"area": 0, "error": "边长必须大于0"}
    
    if a + b <= c or a + c <= b or b + c <= a:
        return {"area": 0, "error": "无法构成三角形"}
    
    # 海伦公式
    s = (a + b + c) / 2  # 半周长
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    
    return {"area": round(area, 2)}


def quadratic_equation_solver(a, b, c):
    """
    二次方程求解器实现
    """
    if a == 0:
        if b == 0:
            if c == 0:
                return {"solutions": "无穷多解", "type": "恒等式"}
            else:
                return {"solutions": "无解", "type": "矛盾方程"}
        else:
            # 一次方程 bx + c = 0
            solution = -c / b
            return {"solutions": [round(solution, 4)], "type": "一次方程"}
    
    # 二次方程 ax² + bx + c = 0
    discriminant = b ** 2 - 4 * a * c
    
    if discriminant > 0:
        # 两个不同实根
        x1 = (-b + math.sqrt(discriminant)) / (2 * a)
        x2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return {
            "solutions": [round(x1, 4), round(x2, 4)],
            "type": "两个不同实根"
        }
    elif discriminant == 0:
        # 一个重根
        x = -b / (2 * a)
        return {
            "solutions": [round(x, 4)],
            "type": "一个重根"
        }
    else:
        # 两个复根
        real_part = -b / (2 * a)
        imaginary_part = math.sqrt(-discriminant) / (2 * a)
        return {
            "solutions": [
                f"{round(real_part, 4)} + {round(imaginary_part, 4)}i",
                f"{round(real_part, 4)} - {round(imaginary_part, 4)}i"
            ],
            "type": "两个复根"
        }


def percentage_calculator(value, total):
    """
    百分比计算器实现
    """
    if total == 0:
        return {"percentage": 0, "error": "总数不能为0"}
    
    percentage = (value / total) * 100
    return {"percentage": round(percentage, 2)}


def discount_calculator(original_price, discount_rate):
    """
    折扣计算器实现
    """
    if original_price < 0 or discount_rate < 0 or discount_rate > 100:
        return {
            "discounted_price": 0,
            "savings": 0,
            "error": "输入参数错误"
        }
    
    discount_amount = original_price * (discount_rate / 100)
    discounted_price = original_price - discount_amount
    
    return {
        "discounted_price": round(discounted_price, 2),
        "savings": round(discount_amount, 2)
    }


def unit_converter(value, from_unit, to_unit, conversion_type):
    """
    单位转换器实现
    """
    conversions = {
        'length': {
            'm': 1.0,
            'cm': 0.01,
            'mm': 0.001,
            'km': 1000.0,
            'inch': 0.0254,
            'ft': 0.3048
        },
        'weight': {
            'kg': 1.0,
            'g': 0.001,
            'lb': 0.453592,
            'oz': 0.0283495
        },
        'volume': {
            'l': 1.0,
            'ml': 0.001,
            'gal': 3.78541,
            'qt': 0.946353
        }
    }
    
    if conversion_type not in conversions:
        return {"result": 0, "error": "不支持的转换类型"}
    
    if from_unit not in conversions[conversion_type] or to_unit not in conversions[conversion_type]:
        return {"result": 0, "error": "不支持的单位"}
    
    # 转换为基准单位，再转换为目标单位
    base_value = value * conversions[conversion_type][from_unit]
    result = base_value / conversions[conversion_type][to_unit]
    
    return {"result": round(result, 6)}


def fibonacci_calculator(n):
    """
    斐波那契数列计算器实现
    """
    if n < 0:
        return {"result": 0, "error": "n必须为非负整数"}
    
    if n == 0:
        return {"result": 0}
    elif n == 1:
        return {"result": 1}
    
    # 使用迭代方法计算，避免递归的性能问题
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return {"result": b}


def factorial_calculator(n):
    """
    阶乘计算器实现
    """
    if n < 0:
        return {"result": 0, "error": "n必须为非负整数"}
    
    if n == 0 or n == 1:
        return {"result": 1}
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    
    return {"result": result}


def gcd_calculator(a, b):
    """
    最大公约数计算器实现（欧几里得算法）
    """
    a, b = abs(a), abs(b)
    
    if a == 0 and b == 0:
        return {"result": 0, "error": "两数不能同时为0"}
    
    while b:
        a, b = b, a % b
    
    return {"result": a}


def lcm_calculator(a, b):
    """
    最小公倍数计算器实现
    """
    if a == 0 or b == 0:
        return {"result": 0}
    
    gcd_result = gcd_calculator(a, b)
    if "error" in gcd_result:
        return gcd_result
    
    gcd_value = gcd_result["result"]
    lcm = abs(a * b) // gcd_value
    
    return {"result": lcm}


def prime_checker(n):
    """
    质数检查器实现
    """
    if n < 2:
        return {"is_prime": False, "reason": "小于2的数不是质数"}
    
    if n == 2:
        return {"is_prime": True, "reason": "2是最小的质数"}
    
    if n % 2 == 0:
        return {"is_prime": False, "reason": "偶数（除2外）不是质数"}
    
    # 只需检查到sqrt(n)
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return {"is_prime": False, "reason": f"能被{i}整除"}
    
    return {"is_prime": True, "reason": "通过了所有质数测试"}


def power_calculator(base, exponent):
    """
    幂运算计算器实现
    """
    try:
        if exponent == 0:
            return {"result": 1, "note": "任何数的0次幂都等于1"}
        
        if base == 0 and exponent < 0:
            return {"result": 0, "error": "0的负次幂未定义"}
        
        result = base ** exponent
        
        # 检查结果是否过大
        if abs(result) > 10**100:
            return {"result": result, "warning": "结果可能过大"}
        
        return {"result": result}
    
    except OverflowError:
        return {"result": 0, "error": "结果溢出"}
    except Exception as e:
        return {"result": 0, "error": f"计算错误: {str(e)}"}


def main():
    """
    主函数 - 演示所有解答
    """
    print("Session03 练习题1解答演示")
    print("=" * 50)
    
    # 演示基本计算器
    print("\n1. 基本计算器演示:")
    print(f"  10 + 5 = {basic_calculator(10, 5, '+')}")
    print(f"  10 / 3 = {basic_calculator(10, 3, '/')}")
    print(f"  10 // 3 = {basic_calculator(10, 3, '//')}")
    print(f"  10 % 3 = {basic_calculator(10, 3, '%')}")
    print(f"  2 ** 8 = {basic_calculator(2, 8, '**')}")
    
    # 演示温度转换
    print("\n2. 温度转换演示:")
    print(f"  100°C = {temperature_converter(100, 'C', 'F')}°F")
    print(f"  32°F = {temperature_converter(32, 'F', 'C')}°C")
    print(f"  273.15K = {temperature_converter(273.15, 'K', 'C')}°C")
    
    # 演示BMI计算
    print("\n3. BMI计算演示:")
    bmi_result = bmi_calculator(70, 1.75)
    print(f"  体重70kg, 身高1.75m: {bmi_result}")
    
    # 演示圆形计算
    print("\n4. 圆形计算演示:")
    circle_result = circle_calculator(5)
    print(f"  半径5的圆: {circle_result}")
    
    # 演示复利计算
    print("\n5. 复利计算演示:")
    compound_result = compound_interest_calculator(1000, 0.05, 10, 12)
    print(f"  本金1000, 年利率5%, 10年, 月复利: {compound_result}")
    
    # 演示二次方程求解
    print("\n6. 二次方程求解演示:")
    quad_result = quadratic_equation_solver(1, -5, 6)
    print(f"  x² - 5x + 6 = 0: {quad_result}")
    
    # 演示质数检查
    print("\n7. 质数检查演示:")
    for num in [17, 18, 97, 100]:
        prime_result = prime_checker(num)
        print(f"  {num}: {prime_result}")
    
    print("\n" + "=" * 50)
    print("解答演示完成！")


if __name__ == "__main__":
    main()