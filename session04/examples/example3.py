#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session04 示例3：while循环详解

本示例详细演示了Python中while循环的各种用法，包括：
- 基本while循环
- 条件控制的while循环
- while-else语句
- 无限循环和break
- 用户输入控制的循环
- while循环的实际应用

作者: Python教程团队
创建日期: 2024-12-21
"""

import random
import time


def basic_while_examples():
    """
    基本while循环示例
    """
    print("=== 基本while循环示例 ===")

    # 示例1：简单计数
    print("1. 简单计数循环:")
    count = 1
    while count <= 5:
        print(f"  计数: {count}")
        count += 1  # 重要：更新循环变量
    print(f"  循环结束，count = {count}")

    # 示例2：倒计时
    print("\n2. 倒计时:")
    countdown = 5
    while countdown > 0:
        print(f"  倒计时: {countdown}")
        countdown -= 1
        time.sleep(0.5)  # 暂停0.5秒
    print("  🚀 发射！")

    # 示例3：累加计算
    print("\n3. 累加计算 (1+2+3+...+10):")
    total = 0
    number = 1
    while number <= 10:
        total += number
        print(f"  {number}: 累计和 = {total}")
        number += 1
    print(f"  最终结果: {total}")


def condition_controlled_examples():
    """
    条件控制的while循环示例
    """
    print("\n=== 条件控制的while循环示例 ===")

    # 示例1：查找特定条件
    print("1. 查找第一个大于50的随机数:")
    attempts = 0
    found_number = 0

    while found_number <= 50:
        found_number = random.randint(1, 100)
        attempts += 1
        print(f"  第{attempts}次尝试: {found_number}")

    print(f"  找到了！{found_number} > 50，共尝试{attempts}次")

    # 示例2：数字猜测游戏（简化版）
    print("\n2. 数字猜测游戏:")
    secret = random.randint(1, 10)
    guess = 0
    attempts = 0

    print("  我想了一个1-10的数字...")

    while guess != secret:
        guess = random.randint(1, 10)  # 模拟随机猜测
        attempts += 1
        print(f"  第{attempts}次猜测: {guess}", end="")

        if guess == secret:
            print(" ✓ 猜对了！")
        elif guess < secret:
            print(" 太小了")
        else:
            print(" 太大了")

    print(f"  游戏结束！答案是{secret}，共猜了{attempts}次")

    # 示例3：字符串处理
    print("\n3. 字符串处理 - 移除所有空格:")
    text = "  Hello   World  Python  "
    print(f"  原始字符串: '{text}'")

    while " " in text:
        text = text.replace(" ", "", 1)  # 每次只移除一个空格
        print(f"  处理中: '{text}'")

    print(f"  最终结果: '{text}'")


def while_else_examples():
    """
    while-else语句示例
    """
    print("\n=== while-else语句示例 ===")

    # 示例1：查找质数
    print("1. 判断质数 (使用while-else):")
    number = 17
    print(f"  检查 {number} 是否为质数")

    if number < 2:
        print(f"  {number} 不是质数")
    else:
        divisor = 2
        while divisor * divisor <= number:
            if number % divisor == 0:
                print(
                    f"  {number} 不是质数，因为 {number} ÷ {divisor} = {number // divisor}"
                )
                break
            divisor += 1
        else:
            print(f"  {number} 是质数！")

    # 示例2：在列表中查找元素
    print("\n2. 在列表中查找元素:")
    numbers = [3, 7, 12, 8, 15, 21]
    target = 8
    print(f"  在 {numbers} 中查找 {target}")

    index = 0
    while index < len(numbers):
        if numbers[index] == target:
            print(f"  找到了！{target} 在索引 {index} 位置")
            break
        index += 1
    else:
        print(f"  没有找到 {target}")

    # 示例3：密码验证
    print("\n3. 密码验证 (最多3次机会):")
    correct_password = "python123"
    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:
        # 模拟用户输入
        passwords = ["123456", "password", "python123"]
        user_input = passwords[attempts] if attempts < len(passwords) else "wrong"

        print(f"  第{attempts + 1}次尝试，输入密码: {user_input}")
        attempts += 1

        if user_input == correct_password:
            print("  ✓ 密码正确，登录成功！")
            break
        else:
            remaining = max_attempts - attempts
            if remaining > 0:
                print(f"  ✗ 密码错误，还有 {remaining} 次机会")
    else:
        print("  ✗ 密码错误次数过多，账户已锁定")


def infinite_loop_examples():
    """
    无限循环和break示例
    """
    print("\n=== 无限循环和break示例 ===")

    # 示例1：菜单系统
    print("1. 简单菜单系统:")
    menu_choices = ["1", "2", "3", "4"]  # 模拟用户选择
    choice_index = 0

    while True:
        print("\n  === 计算器菜单 ===")
        print("  1. 加法")
        print("  2. 减法")
        print("  3. 乘法")
        print("  4. 退出")

        # 模拟用户输入
        if choice_index < len(menu_choices):
            choice = menu_choices[choice_index]
            choice_index += 1
        else:
            choice = "4"

        print(f"  用户选择: {choice}")

        if choice == "1":
            print("  执行加法运算...")
        elif choice == "2":
            print("  执行减法运算...")
        elif choice == "3":
            print("  执行乘法运算...")
        elif choice == "4":
            print("  退出程序，再见！")
            break
        else:
            print("  无效选择，请重新输入")

    # 示例2：数据处理循环
    print("\n2. 数据处理循环:")
    data_queue = ["task1", "task2", "error", "task3", "done"]
    processed = 0

    while True:
        if not data_queue:
            print("  队列为空，等待新数据...")
            break

        item = data_queue.pop(0)
        print(f"  处理项目: {item}")

        if item == "done":
            print("  收到结束信号，停止处理")
            break
        elif item == "error":
            print("  遇到错误，跳过此项")
            continue
        else:
            processed += 1
            print(f"  成功处理，已完成 {processed} 个任务")

    print(f"  总共处理了 {processed} 个有效任务")


def user_input_examples():
    """
    用户输入控制的循环示例（模拟）
    """
    print("\n=== 用户输入控制的循环示例 ===")

    # 示例1：输入验证
    print("1. 输入验证 - 获取有效年龄:")

    # 模拟用户输入序列
    inputs = ["-5", "abc", "200", "25"]
    input_index = 0

    while True:
        # 模拟用户输入
        if input_index < len(inputs):
            user_input = inputs[input_index]
            input_index += 1
        else:
            user_input = "25"  # 最后给一个有效输入

        print(f"  用户输入: {user_input}")

        try:
            age = int(user_input)
            if age < 0:
                print("  ✗ 年龄不能为负数，请重新输入")
                continue
            elif age > 150:
                print("  ✗ 年龄不能超过150岁，请重新输入")
                continue
            else:
                print(f"  ✓ 有效年龄: {age}岁")
                break
        except ValueError:
            print("  ✗ 请输入有效的数字")

    # 示例2：累积输入
    print("\n2. 累积输入 - 收集购物清单:")
    shopping_list = []

    # 模拟用户输入
    items = ["苹果", "香蕉", "牛奶", "", "面包", "quit"]
    item_index = 0

    while True:
        if item_index < len(items):
            item = items[item_index]
            item_index += 1
        else:
            item = "quit"

        print(f"  输入商品 (输入'quit'结束): {item}")

        if item.lower() == "quit":
            print("  结束输入")
            break
        elif item.strip() == "":
            print("  商品名不能为空，请重新输入")
            continue
        else:
            shopping_list.append(item)
            print(f"  已添加: {item}")
            print(f"  当前清单: {shopping_list}")

    print(f"  最终购物清单: {shopping_list}")


def practical_applications():
    """
    while循环的实际应用示例
    """
    print("\n=== while循环的实际应用示例 ===")

    # 示例1：文件处理模拟
    print("1. 文件处理模拟:")

    # 模拟文件内容
    file_lines = [
        "# 这是注释",
        "name = John",
        "",  # 空行
        "age = 25",
        "# 另一个注释",
        "city = Beijing",
    ]

    line_index = 0
    processed_lines = []

    print("  处理配置文件，跳过注释和空行:")

    while line_index < len(file_lines):
        line = file_lines[line_index]
        line_index += 1

        print(f"    读取行: '{line}'")

        # 跳过注释和空行
        if line.strip().startswith("#") or line.strip() == "":
            print("      跳过（注释或空行）")
            continue

        processed_lines.append(line)
        print(f"      处理: {line}")

    print(f"  处理结果: {processed_lines}")

    # 示例2：网络重试机制模拟
    print("\n2. 网络重试机制模拟:")

    max_retries = 3
    retry_count = 0
    success = False

    # 模拟网络请求成功率
    success_rates = [False, False, True]  # 第3次成功

    while retry_count < max_retries and not success:
        retry_count += 1
        print(f"  第{retry_count}次尝试连接服务器...")

        # 模拟网络请求
        if retry_count <= len(success_rates):
            success = success_rates[retry_count - 1]

        if success:
            print("  ✓ 连接成功！")
        else:
            print("  ✗ 连接失败")
            if retry_count < max_retries:
                wait_time = retry_count * 2  # 递增等待时间
                print(f"  等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)

    if not success:
        print("  ✗ 达到最大重试次数，连接失败")

    # 示例3：数据流处理
    print("\n3. 数据流处理:")

    # 模拟传感器数据
    sensor_data = [22.5, 23.1, 24.8, 26.2, 28.5, 30.1, 25.3, 23.7]
    data_index = 0

    temperature_sum = 0
    reading_count = 0
    high_temp_count = 0

    print("  处理温度传感器数据:")

    while data_index < len(sensor_data):
        temperature = sensor_data[data_index]
        data_index += 1
        reading_count += 1

        print(f"    读取温度: {temperature}°C")

        temperature_sum += temperature

        if temperature > 25.0:
            high_temp_count += 1
            print(f"      ⚠️  高温警告: {temperature}°C")

        # 每3个读数计算一次平均值
        if reading_count % 3 == 0:
            avg_temp = temperature_sum / reading_count
            print(f"      📊 当前平均温度: {avg_temp:.1f}°C")

    final_avg = temperature_sum / reading_count
    print(f"  最终统计:")
    print(f"    总读数: {reading_count}")
    print(f"    平均温度: {final_avg:.1f}°C")
    print(f"    高温次数: {high_temp_count}")


def performance_considerations():
    """
    while循环的性能考虑
    """
    print("\n=== while循环的性能考虑 ===")

    # 示例1：避免不必要的计算
    print("1. 避免在循环中重复计算:")

    data = list(range(1000))

    # 低效方式（每次都计算长度）
    print("  低效方式演示:")
    start_time = time.time()
    count = 0
    index = 0
    while index < len(data):  # len(data)在每次循环中都被计算
        count += 1
        index += 1
    end_time = time.time()
    print(f"    处理了 {count} 个元素，耗时: {(end_time - start_time)*1000:.2f}ms")

    # 高效方式（预先计算长度）
    print("  高效方式演示:")
    start_time = time.time()
    count = 0
    index = 0
    data_length = len(data)  # 只计算一次
    while index < data_length:
        count += 1
        index += 1
    end_time = time.time()
    print(f"    处理了 {count} 个元素，耗时: {(end_time - start_time)*1000:.2f}ms")

    # 示例2：合理的退出条件
    print("\n2. 设置合理的退出条件:")

    # 避免无限循环的技巧
    max_iterations = 1000
    iteration = 0
    target_found = False

    while iteration < max_iterations and not target_found:
        # 模拟查找过程
        random_value = random.randint(1, 100)
        iteration += 1

        if random_value > 95:  # 找到目标
            target_found = True
            print(f"    在第 {iteration} 次迭代找到目标值: {random_value}")

        # 每100次迭代报告一次进度
        if iteration % 100 == 0:
            print(f"    已完成 {iteration} 次迭代...")

    if not target_found:
        print(f"    达到最大迭代次数 {max_iterations}，未找到目标")


def main():
    """
    主函数：运行所有示例
    """
    print("Session04 示例3：while循环详解")
    print("=" * 50)

    basic_while_examples()
    condition_controlled_examples()
    while_else_examples()
    infinite_loop_examples()
    user_input_examples()
    practical_applications()
    performance_considerations()

    print("\n" + "=" * 50)
    print("示例演示完成！")
    print("\n💡 学习要点:")
    print("1. while循环基于条件判断，条件为真时继续执行")
    print("2. 必须确保循环变量在循环体内被更新")
    print("3. while-else结构在循环正常结束时执行else")
    print("4. 使用break可以提前退出循环")
    print("5. 无限循环while True常用于菜单和事件处理")
    print("6. 注意避免无限循环和性能问题")


if __name__ == "__main__":
    main()
