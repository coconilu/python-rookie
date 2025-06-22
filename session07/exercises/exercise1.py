#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session07 练习1：基础文件操作

练习目标：
- 掌握基本的文件读写操作
- 学会使用不同的文件打开模式
- 练习文件内容的处理和分析

完成以下练习题，每个函数都有详细的要求说明。
请在每个函数中实现相应的功能。

作者: Python教程团队
创建日期: 2024-12-22
"""

import os
from datetime import datetime


def exercise1_create_student_file():
    """
    练习1：创建学生信息文件
    
    要求：
    1. 创建一个名为'students.txt'的文件
    2. 写入至少5个学生的信息，格式为："姓名,年龄,专业,成绩"
    3. 每个学生信息占一行
    4. 使用UTF-8编码
    
    示例格式：
    张三,20,计算机科学,85
    李四,21,数学,92
    
    返回：创建的文件名
    """
    # TODO: 在这里实现你的代码
    filename = 'students.txt'
    
    # 提示：使用with open()语句创建和写入文件
    # 学生数据可以使用列表存储，然后遍历写入
    
    pass  # 删除这行，实现你的代码


def exercise2_read_and_analyze():
    """
    练习2：读取并分析学生文件
    
    要求：
    1. 读取exercise1创建的'students.txt'文件
    2. 解析每行数据，提取学生信息
    3. 计算并返回以下统计信息：
       - 学生总数
       - 平均年龄
       - 平均成绩
       - 成绩最高的学生姓名
       - 各专业的学生数量
    
    返回：包含统计信息的字典
    """
    # TODO: 在这里实现你的代码
    
    # 提示：
    # 1. 使用split(',')分割每行数据
    # 2. 注意数据类型转换（年龄和成绩需要转为数字）
    # 3. 使用字典统计各专业学生数量
    
    pass  # 删除这行，实现你的代码


def exercise3_append_new_students():
    """
    练习3：追加新学生信息
    
    要求：
    1. 向'students.txt'文件追加3个新学生的信息
    2. 不要覆盖原有数据
    3. 新学生信息格式与原文件保持一致
    4. 在追加前添加一行注释："# 新增学生 - [当前时间]"
    
    返回：追加的学生数量
    """
    # TODO: 在这里实现你的代码
    
    # 提示：
    # 1. 使用'a'模式打开文件进行追加
    # 2. 使用datetime.now()获取当前时间
    # 3. 确保每行数据都以换行符结尾
    
    pass  # 删除这行，实现你的代码


def exercise4_filter_students():
    """
    练习4：筛选学生信息
    
    要求：
    1. 读取'students.txt'文件
    2. 筛选出成绩大于等于90分的学生
    3. 将筛选结果写入新文件'excellent_students.txt'
    4. 在新文件开头添加标题行："优秀学生名单"
    5. 按成绩从高到低排序
    
    返回：优秀学生的数量
    """
    # TODO: 在这里实现你的代码
    
    # 提示：
    # 1. 先读取所有学生数据到列表中
    # 2. 使用列表推导式或filter()函数筛选
    # 3. 使用sorted()函数按成绩排序
    # 4. 注意排序时的key参数和reverse参数
    
    pass  # 删除这行，实现你的代码


def exercise5_backup_and_modify():
    """
    练习5：备份和修改文件
    
    要求：
    1. 创建'students.txt'的备份文件'students_backup.txt'
    2. 读取原文件，将所有学生的成绩提高5分（但不超过100分）
    3. 将修改后的数据写入原文件
    4. 在文件末尾添加修改日志："# 成绩已于[时间]统一提高5分"
    
    返回：修改的学生数量
    """
    # TODO: 在这里实现你的代码
    
    # 提示：
    # 1. 使用shutil.copy()或手动复制创建备份
    # 2. 读取数据，修改成绩，注意边界条件
    # 3. 使用'w'模式重写原文件
    # 4. 记录修改的学生数量
    
    pass  # 删除这行，实现你的代码


def exercise6_file_statistics():
    """
    练习6：文件统计信息
    
    要求：
    1. 分析'students.txt'文件的基本信息：
       - 文件大小（字节）
       - 行数
       - 字符数（包括空格和换行符）
       - 单词数
    2. 创建统计报告文件'file_stats.txt'
    3. 将统计信息以易读的格式写入报告文件
    
    返回：包含统计信息的字典
    """
    # TODO: 在这里实现你的代码
    
    # 提示：
    # 1. 使用os.path.getsize()获取文件大小
    # 2. 逐行读取计算行数
    # 3. 使用len()计算字符数
    # 4. 使用split()计算单词数
    
    pass  # 删除这行，实现你的代码


def exercise7_error_handling():
    """
    练习7：错误处理
    
    要求：
    1. 尝试读取一个不存在的文件'nonexistent.txt'
    2. 实现适当的错误处理
    3. 创建错误日志文件'error_log.txt'
    4. 记录错误信息和时间戳
    5. 函数应该优雅地处理错误，不崩溃
    
    返回：错误处理的结果信息
    """
    # TODO: 在这里实现你的代码
    
    # 提示：
    # 1. 使用try-except语句捕获异常
    # 2. 捕获FileNotFoundError等特定异常
    # 3. 记录详细的错误信息
    # 4. 返回有意义的错误描述
    
    pass  # 删除这行，实现你的代码


def run_all_exercises():
    """
    运行所有练习
    """
    print("Session07 练习1：基础文件操作")
    print("=" * 50)
    
    exercises = [
        ("练习1：创建学生信息文件", exercise1_create_student_file),
        ("练习2：读取并分析学生文件", exercise2_read_and_analyze),
        ("练习3：追加新学生信息", exercise3_append_new_students),
        ("练习4：筛选学生信息", exercise4_filter_students),
        ("练习5：备份和修改文件", exercise5_backup_and_modify),
        ("练习6：文件统计信息", exercise6_file_statistics),
        ("练习7：错误处理", exercise7_error_handling)
    ]
    
    for title, exercise_func in exercises:
        print(f"\n{title}")
        print("-" * 30)
        
        try:
            result = exercise_func()
            if result is not None:
                print(f"结果: {result}")
            print("✅ 练习完成")
        except Exception as e:
            print(f"❌ 练习出错: {e}")
            print("💡 请检查你的代码实现")
    
    print("\n" + "=" * 50)
    print("所有练习运行完成！")
    print("\n💡 学习提示：")
    print("- 文件操作要注意异常处理")
    print("- 使用with语句确保文件正确关闭")
    print("- 注意文件编码，推荐使用UTF-8")
    print("- 处理数据时要注意类型转换")
    print("- 备份重要文件是好习惯")


if __name__ == "__main__":
    run_all_exercises()