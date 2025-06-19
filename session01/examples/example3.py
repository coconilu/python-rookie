#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session01 示例3: 输入输出操作详解

这个示例展示了Python中各种输入输出操作的方法
"""

def demo_basic_input_output():
    """
    演示基本的输入输出操作
    """
    print("=== 基本输入输出演示 ===")
    
    # 基本输出
    print("欢迎使用Python输入输出演示程序！")
    
    # 获取用户姓名
    name = input("请输入你的姓名: ")
    print(f"你好, {name}!")
    
    # 获取用户年龄（带错误处理）
    while True:
        try:
            age = int(input("请输入你的年龄: "))
            break
        except ValueError:
            print("请输入有效的数字！")
    
    print(f"你今年{age}岁了")
    print()


def demo_advanced_output():
    """
    演示高级输出功能
    """
    print("=== 高级输出演示 ===")
    
    # 使用sep参数
    print("苹果", "香蕉", "橙子", sep=" | ")
    print("2024", "01", "01", sep="-")
    
    # 使用end参数
    print("加载中", end="")
    for i in range(5):
        print(".", end="")
    print(" 完成！")
    
    # 格式化输出
    name = "张三"
    score = 95.5
    print(f"学生{name}的成绩是{score:.1f}分")
    
    # 对齐输出
    print(f"{'姓名':<10}{'年龄':<5}{'成绩':<8}")
    print(f"{'张三':<10}{20:<5}{95.5:<8}")
    print(f"{'李四':<10}{22:<5}{87.2:<8}")
    print()


def demo_number_input():
    """
    演示数字输入的处理
    """
    print("=== 数字输入演示 ===")
    
    # 整数输入
    try:
        num1 = int(input("请输入一个整数: "))
        print(f"你输入的整数是: {num1}")
        print(f"它的平方是: {num1 ** 2}")
    except ValueError:
        print("输入的不是有效整数！")
    
    # 浮点数输入
    try:
        num2 = float(input("请输入一个小数: "))
        print(f"你输入的小数是: {num2}")
        print(f"保留2位小数: {num2:.2f}")
    except ValueError:
        print("输入的不是有效数字！")
    
    print()


def demo_multiple_input():
    """
    演示多个值的输入
    """
    print("=== 多值输入演示 ===")
    
    # 一行输入多个值
    print("请输入三个数字，用空格分隔:")
    try:
        numbers = input().split()
        a, b, c = map(int, numbers)
        print(f"你输入的三个数字是: {a}, {b}, {c}")
        print(f"它们的和是: {a + b + c}")
    except ValueError:
        print("请输入有效的数字！")
    except:
        print("请输入三个数字！")
    
    print()


def demo_string_operations():
    """
    演示字符串操作
    """
    print("=== 字符串操作演示 ===")
    
    text = input("请输入一段文字: ")
    
    print(f"原文: {text}")
    print(f"长度: {len(text)}")
    print(f"大写: {text.upper()}")
    print(f"小写: {text.lower()}")
    print(f"首字母大写: {text.capitalize()}")
    print(f"去除空格: '{text.strip()}'")
    
    if text:
        print(f"第一个字符: {text[0]}")
        print(f"最后一个字符: {text[-1]}")
    
    print()


def demo_formatted_output():
    """
    演示格式化输出的不同方法
    """
    print("=== 格式化输出演示 ===")
    
    name = "王五"
    age = 28
    salary = 8500.5
    
    # 方法1: % 格式化
    print("方法1 - %格式化:")
    print("姓名: %s, 年龄: %d, 薪资: %.2f" % (name, age, salary))
    
    # 方法2: .format() 方法
    print("\n方法2 - .format()方法:")
    print("姓名: {}, 年龄: {}, 薪资: {:.2f}".format(name, age, salary))
    print("姓名: {0}, 年龄: {1}, 薪资: {2:.2f}".format(name, age, salary))
    print("姓名: {n}, 年龄: {a}, 薪资: {s:.2f}".format(n=name, a=age, s=salary))
    
    # 方法3: f-string (推荐)
    print("\n方法3 - f-string (推荐):")
    print(f"姓名: {name}, 年龄: {age}, 薪资: {salary:.2f}")
    
    # 数字格式化
    number = 1234567.89
    print(f"\n数字格式化:")
    print(f"原数字: {number}")
    print(f"千分位分隔: {number:,}")
    print(f"科学计数法: {number:.2e}")
    print(f"百分比: {0.85:.1%}")
    
    print()


def main():
    """
    主函数
    """
    print("Python输入输出操作详解")
    print("=" * 40)
    
    # 演示各种输入输出操作
    demo_basic_input_output()
    demo_advanced_output()
    demo_number_input()
    demo_multiple_input()
    demo_string_operations()
    demo_formatted_output()
    
    print("演示完成！")


if __name__ == "__main__":
    main()