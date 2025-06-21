#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session04: 控制流程 - 演示代码

本文件演示了Python中控制流程的基本用法，包括条件语句、循环语句和循环控制。
通过实际的代码示例，帮助理解程序的执行流程控制。

作者: Python教程团队
创建日期: 2024-12-21
最后修改: 2024-12-21
"""

import random
import time


def main():
    """
    主函数：演示程序的入口点
    """
    print("Session04: 控制流程演示")
    print("=" * 40)

    # 演示各种控制流程
    demo_conditional_statements()
    demo_for_loops()
    demo_while_loops()
    demo_loop_control()
    demo_nested_structures()

    print("\n演示完成！")


def demo_conditional_statements():
    """
    演示条件语句的使用
    """
    print("\n1. 条件语句演示")
    print("-" * 20)

    # 基本if语句
    age = 20
    print(f"年龄: {age}")

    if age >= 18:
        print("✓ 已成年，可以投票")

    # if-else语句
    score = 85
    print(f"\n考试分数: {score}")

    if score >= 60:
        print("✓ 考试通过")
    else:
        print("✗ 考试未通过")

    # if-elif-else语句
    temperature = 25
    print(f"\n当前温度: {temperature}°C")

    if temperature > 30:
        print("🔥 天气炎热")
        advice = "建议待在室内开空调"
    elif temperature > 20:
        print("☀️ 天气舒适")
        advice = "适合外出活动"
    elif temperature > 10:
        print("🌤️ 天气凉爽")
        advice = "建议穿长袖"
    else:
        print("❄️ 天气寒冷")
        advice = "注意保暖"

    print(f"建议: {advice}")


def demo_for_loops():
    """
    演示for循环的使用
    """
    print("\n2. for循环演示")
    print("-" * 20)

    # 基本for循环
    print("倒计时:")
    for i in range(5, 0, -1):
        print(f"{i}...", end=" ")
        time.sleep(0.5)  # 暂停0.5秒
    print("🚀 发射!")

    # 遍历列表
    fruits = ["🍎苹果", "🍌香蕉", "🍊橙子", "🍇葡萄"]
    print("\n水果清单:")
    for i, fruit in enumerate(fruits, 1):
        print(f"{i}. {fruit}")

    # 遍历字符串
    word = "Python"
    print(f"\n单词 '{word}' 的字母:")
    for char in word:
        print(f"[{char}]", end=" ")
    print()

    # 嵌套循环 - 打印图案
    print("\n星号图案:")
    for i in range(1, 6):
        for j in range(i):
            print("⭐", end="")
        print(f" ({i}个星星)")


def demo_while_loops():
    """
    演示while循环的使用
    """
    print("\n3. while循环演示")
    print("-" * 20)

    # 基本while循环
    print("数字累加:")
    total = 0
    number = 1

    while number <= 5:
        total += number
        print(f"{number} + ", end="")
        number += 1

    print(f"= {total}")

    # 条件控制的while循环
    print("\n随机数生成 (直到生成偶数):")
    attempts = 0

    while True:
        random_num = random.randint(1, 10)
        attempts += 1
        print(f"第{attempts}次尝试: {random_num}", end="")

        if random_num % 2 == 0:
            print(" ✓ (偶数，停止)")
            break
        else:
            print(" (奇数，继续)")

    print(f"总共尝试了 {attempts} 次")


def demo_loop_control():
    """
    演示循环控制语句的使用
    """
    print("\n4. 循环控制演示")
    print("-" * 20)

    # break语句演示
    print("break演示 - 寻找第一个大于50的数:")
    numbers = [23, 45, 67, 12, 89, 34]

    for num in numbers:
        print(f"检查: {num}", end="")
        if num > 50:
            print(f" ✓ 找到了: {num}")
            break
        else:
            print(" (继续寻找)")

    # continue语句演示
    print("\ncontinue演示 - 只打印偶数:")
    for i in range(1, 11):
        if i % 2 != 0:  # 如果是奇数
            continue  # 跳过本次循环
        print(f"偶数: {i}")

    # pass语句演示
    print("\npass演示 - 占位符的使用:")
    for i in range(3):
        if i == 0:
            print("处理第一个元素")
        elif i == 1:
            pass  # 暂时不处理第二个元素
        else:
            print("处理第三个元素")


def demo_nested_structures():
    """
    演示嵌套结构的使用
    """
    print("\n5. 嵌套结构演示")
    print("-" * 20)

    # 嵌套条件语句
    print("学生成绩分析:")
    students = [
        {"name": "小明", "score": 92, "subject": "数学"},
        {"name": "小红", "score": 78, "subject": "英语"},
        {"name": "小李", "score": 45, "subject": "物理"},
        {"name": "小王", "score": 88, "subject": "化学"},
    ]

    for student in students:
        name = student["name"]
        score = student["score"]
        subject = student["subject"]

        print(f"\n{name} - {subject}: {score}分", end=" ")

        if score >= 90:
            grade = "A"
            emoji = "🏆"
        elif score >= 80:
            grade = "B"
            emoji = "👍"
        elif score >= 70:
            grade = "C"
            emoji = "👌"
        elif score >= 60:
            grade = "D"
            emoji = "😐"
        else:
            grade = "F"
            emoji = "😞"

        print(f"[等级: {grade}] {emoji}")

        # 嵌套的条件判断
        if grade in ["A", "B"]:
            if subject in ["数学", "物理"]:
                print("  💡 理科成绩优秀！")
            else:
                print("  📚 文科成绩优秀！")
        elif grade == "F":
            print("  ⚠️  需要加强学习")

    # 嵌套循环 - 简单的乘法表
    print("\n\n简化乘法表 (1-3):")
    for i in range(1, 4):
        for j in range(1, 4):
            result = i * j
            print(f"{i}×{j}={result:2d}", end="  ")
        print()  # 换行


def interactive_demo():
    """
    交互式演示 - 简单的猜数字游戏
    """
    print("\n🎮 交互式演示: 猜数字游戏")
    print("=" * 30)

    # 生成1-10之间的随机数
    secret_number = random.randint(1, 10)
    max_attempts = 3
    attempts = 0

    print("我想了一个1到10之间的数字，你能猜中吗？")
    print(f"你有 {max_attempts} 次机会！")

    while attempts < max_attempts:
        try:
            guess = int(input(f"\n第{attempts + 1}次猜测，请输入数字: "))
            attempts += 1

            if guess == secret_number:
                print(f"🎉 恭喜！你猜对了！数字就是 {secret_number}")
                print(f"你用了 {attempts} 次就猜中了！")
                break
            elif guess < secret_number:
                print("📈 太小了！")
            else:
                print("📉 太大了！")

            remaining = max_attempts - attempts
            if remaining > 0:
                print(f"还有 {remaining} 次机会")

        except ValueError:
            print("❌ 请输入有效的数字！")
            attempts -= 1  # 无效输入不计入尝试次数

    else:
        print(f"\n😔 很遗憾，你没有猜中！")
        print(f"正确答案是: {secret_number}")

    print("\n游戏结束！")


if __name__ == "__main__":
    main()

    # 询问是否运行交互式演示
    print("\n" + "=" * 40)
    choice = input("是否运行交互式猜数字游戏？(y/n): ")
    if choice.lower() in ["y", "yes", "是"]:
        interactive_demo()
    else:
        print("感谢使用演示程序！")
