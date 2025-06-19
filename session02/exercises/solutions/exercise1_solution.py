#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session02 练习题1：变量基础操作 - 参考答案

本文件提供了练习题1的完整解决方案，展示了变量的基本操作。

作者: Python教程团队
创建日期: 2024-12-19
"""

def solution():
    """
    练习题1的完整解决方案
    """
    print("=== Session02 练习题1：变量基础操作 ===")
    
    # 1. 创建变量
    name = "张三"           # 姓名（字符串）
    age = 20               # 年龄（整数）
    height = 1.75          # 身高（浮点数，单位：米）
    is_student = True      # 是否是学生（布尔值）
    
    # 2. 打印变量值和类型
    print("\n=== 个人信息 ===")
    print(f"姓名: {name}, 类型: {type(name)}")
    print(f"年龄: {age}, 类型: {type(age)}")
    print(f"身高: {height}, 类型: {type(height)}")
    print(f"是否学生: {is_student}, 类型: {type(is_student)}")
    
    # 3. 进行计算
    print("\n=== 计算结果 ===")
    
    # 计算10年后的年龄
    future_age = age + 10
    print(f"10年后年龄: {future_age}岁")
    
    # 计算身高（厘米）
    height_cm = height * 100
    print(f"身高(厘米): {height_cm}cm")
    
    # 判断是否成年
    is_adult = age >= 18
    adult_status = "是" if is_adult else "否"
    print(f"是否成年: {adult_status}")
    
    # 4. 创建自我介绍
    print("\n=== 自我介绍 ===")
    
    # 使用f-string格式化
    student_status = "一名学生" if is_student else "不是学生"
    introduction = f"大家好，我叫{name}，今年{age}岁，身高{height_cm}cm，我是{student_status}。"
    print(introduction)
    
    # 额外的信息展示
    print("\n=== 额外信息 ===")
    print(f"我的姓名有{len(name)}个字符")
    print(f"我的年龄是{'偶数' if age % 2 == 0 else '奇数'}")
    print(f"我的身高{'超过' if height > 1.7 else '不超过'}1.7米")


def advanced_solution():
    """
    进阶版本：展示更多变量操作技巧
    """
    print("\n" + "=" * 50)
    print("=== 进阶版本：更多变量操作技巧 ===")
    
    # 使用多重赋值
    name, age, height, is_student = "李四", 22, 1.68, False
    
    print(f"\n使用多重赋值创建的变量:")
    print(f"姓名: {name}, 年龄: {age}, 身高: {height}m, 学生: {is_student}")
    
    # 变量交换
    a, b = 10, 20
    print(f"\n交换前: a = {a}, b = {b}")
    a, b = b, a
    print(f"交换后: a = {a}, b = {b}")
    
    # 链式赋值
    x = y = z = 100
    print(f"\n链式赋值结果: x = {x}, y = {y}, z = {z}")
    
    # 类型转换示例
    age_str = str(age)
    height_int = int(height)  # 截断小数部分
    is_student_str = str(is_student)
    
    print(f"\n类型转换示例:")
    print(f"年龄转字符串: '{age_str}' (类型: {type(age_str)})")
    print(f"身高转整数: {height_int} (类型: {type(height_int)})")
    print(f"学生状态转字符串: '{is_student_str}' (类型: {type(is_student_str)})")
    
    # 使用变量进行复杂计算
    bmi = height ** 2  # 简化的BMI计算（实际应该是体重/身高²）
    print(f"\n身高的平方: {bmi:.2f}")
    
    # 字符串操作
    full_info = f"{name}_{age}_{height}"
    print(f"组合信息: {full_info}")
    print(f"信息长度: {len(full_info)}")
    print(f"信息大写: {full_info.upper()}")


if __name__ == "__main__":
    # 运行基础解决方案
    solution()
    
    # 运行进阶解决方案
    advanced_solution()
    
    print("\n" + "=" * 50)
    print("练习完成！你已经掌握了变量的基本操作。")