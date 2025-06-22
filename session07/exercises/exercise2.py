#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session07 练习2：CSV和JSON文件操作

练习目标：
- 掌握CSV文件的读写操作
- 学会处理JSON格式数据
- 练习数据格式转换
- 学习数据清洗和验证

完成以下练习题，每个函数都有详细的要求说明。
请在每个函数中实现相应的功能。

作者: Python教程团队
创建日期: 2024-12-22
"""

import csv
import json
import os
from datetime import datetime, timedelta
import random


def exercise1_create_employee_csv():
    """
    练习1：创建员工CSV文件
    
    要求：
    1. 创建一个名为'employees.csv'的文件
    2. 包含以下列：员工ID,姓名,部门,职位,薪资,入职日期
    3. 添加至少10个员工的数据
    4. 使用csv模块写入数据
    5. 确保数据格式正确（日期格式：YYYY-MM-DD）
    
    返回：创建的员工数量
    """
    # TODO: 在这里实现你的代码
    
    # 提示：
    # 1. 使用csv.writer()或csv.DictWriter()
    # 2. 先写入标题行
    # 3. 准备员工数据列表
    # 4. 注意CSV文件的编码
    
    pass  # 删除这行，实现你的代码


def exercise2_read_and_filter_csv():
    """
    练习2：读取和筛选CSV数据
    
    要求：
    1. 读取'employees.csv'文件
    2. 筛选出薪资大于8000的员工
    3. 按薪资从高到低排序
    4. 将结果保存到'high_salary_employees.csv'
    5. 计算这些员工的平均薪资
    
    返回：高薪员工数量和平均薪资的元组
    """
    # TODO: 在这里实现你的代码
    
    # 提示：
    # 1. 使用csv.DictReader()读取数据
    # 2. 注意薪资字段的数据类型转换
    # 3. 使用sorted()函数排序
    # 4. 计算平均值时注意除零错误
    
    pass  # 删除这行，实现你的代码


def exercise3_csv_data_analysis():
    """
    练习3：CSV数据分析
    
    要求：
    1. 读取'employees.csv'文件
    2. 进行以下分析：
       - 各部门的员工数量
       - 各部门的平均薪资
       - 各职位的薪资范围（最高和最低）
       - 入职时间分布（按年份统计）
    3. 将分析结果保存到'employee_analysis.json'
    
    返回：分析结果字典
    """
    # TODO: 在这里实现你的代码
    
    # 提示：
    # 1. 使用字典统计各种数据
    # 2. 处理日期字符串，提取年份
    # 3. 计算最大值、最小值、平均值
    # 4. 将结果组织成易于理解的格式
    
    pass  # 删除这行，实现你的代码


def exercise4_create_product_json():
    """
    练习4：创建产品JSON文件
    
    要求：
    1. 创建一个包含产品信息的JSON文件'products.json'
    2. 每个产品包含：ID,名称,类别,价格,库存,描述,标签列表
    3. 创建至少15个不同类别的产品
    4. 使用嵌套结构组织数据（按类别分组）
    5. 包含创建时间戳
    
    返回：创建的产品总数
    """
    # TODO: 在这里实现你的代码
    
    # 提示：
    # 1. 设计合理的JSON数据结构
    # 2. 使用json.dump()写入文件
    # 3. 设置ensure_ascii=False支持中文
    # 4. 使用indent参数美化格式
    
    pass  # 删除这行，实现你的代码


def exercise5_json_data_manipulation():
    """
    练习5：JSON数据操作
    
    要求：
    1. 读取'products.json'文件
    2. 执行以下操作：
       - 添加3个新产品
       - 更新某些产品的价格（涨价10%）
       - 删除库存为0的产品
       - 为所有产品添加'last_updated'字段
    3. 将修改后的数据保存回文件
    
    返回：操作统计信息（添加、更新、删除的数量）
    """
    # TODO: 在这里实现你的代码
    
    # 提示：
    # 1. 深度复制数据避免意外修改
    # 2. 遍历数据结构进行修改
    # 3. 记录每种操作的数量
    # 4. 使用datetime.now().isoformat()生成时间戳
    
    pass  # 删除这行，实现你的代码


def exercise6_csv_to_json_conversion():
    """
    练习6：CSV到JSON格式转换
    
    要求：
    1. 读取'employees.csv'文件
    2. 将数据转换为JSON格式
    3. 重新组织数据结构：
       - 按部门分组
       - 每个部门包含员工列表和统计信息
       - 添加转换时间戳和元数据
    4. 保存为'employees_by_department.json'
    
    返回：转换的部门数量
    """
    # TODO: 在这里实现你的代码
    
    # 提示：
    # 1. 先读取CSV数据到内存
    # 2. 按部门分组组织数据
    # 3. 计算每个部门的统计信息
    # 4. 设计清晰的JSON结构
    
    pass  # 删除这行，实现你的代码


def exercise7_data_validation():
    """
    练习7：数据验证和清洗
    
    要求：
    1. 创建一个包含错误数据的CSV文件'dirty_data.csv'
       - 包含空值、格式错误的日期、负数薪资等
    2. 读取并验证数据
    3. 清洗数据：
       - 移除或修复无效记录
       - 标准化数据格式
       - 填充缺失值
    4. 将清洗后的数据保存为'clean_data.csv'
    5. 生成数据质量报告'data_quality_report.json'
    
    返回：清洗前后的记录数量对比
    """
    # TODO: 在这里实现你的代码
    
    # 提示：
    # 1. 先创建包含各种错误的测试数据
    # 2. 定义数据验证规则
    # 3. 实现数据清洗逻辑
    # 4. 记录清洗过程中的统计信息
    
    pass  # 删除这行，实现你的代码


def exercise8_batch_file_processing():
    """
    练习8：批量文件处理
    
    要求：
    1. 创建多个CSV文件（模拟不同月份的销售数据）
    2. 批量读取所有CSV文件
    3. 合并数据并进行汇总分析
    4. 生成综合报告：
       - 总销售额
       - 月度趋势
       - 热销产品
       - 客户分析
    5. 将报告保存为JSON和CSV两种格式
    
    返回：处理的文件数量和总记录数
    """
    # TODO: 在这里实现你的代码
    
    # 提示：
    # 1. 使用循环创建多个月份的数据文件
    # 2. 使用glob模块批量查找文件
    # 3. 合并数据时注意数据结构一致性
    # 4. 进行多维度的数据分析
    
    pass  # 删除这行，实现你的代码


def exercise9_json_schema_validation():
    """
    练习9：JSON数据结构验证
    
    要求：
    1. 定义一个产品数据的JSON模式（schema）
    2. 创建符合和不符合模式的测试数据
    3. 实现简单的模式验证函数
    4. 验证现有的'products.json'文件
    5. 生成验证报告
    
    返回：验证结果摘要
    """
    # TODO: 在这里实现你的代码
    
    # 提示：
    # 1. 定义必需字段和数据类型
    # 2. 实现字段存在性检查
    # 3. 实现数据类型验证
    # 4. 收集和报告验证错误
    
    pass  # 删除这行，实现你的代码


def exercise10_performance_comparison():
    """
    练习10：性能对比测试
    
    要求：
    1. 创建大量数据（1000+记录）
    2. 比较不同文件格式的性能：
       - CSV vs JSON 写入速度
       - CSV vs JSON 读取速度
       - 文件大小对比
    3. 测试不同的读写方法
    4. 生成性能测试报告
    
    返回：性能测试结果
    """
    # TODO: 在这里实现你的代码
    
    # 提示：
    # 1. 使用time模块测量执行时间
    # 2. 生成大量测试数据
    # 3. 多次测试取平均值
    # 4. 使用os.path.getsize()比较文件大小
    
    pass  # 删除这行，实现你的代码


def cleanup_exercise_files():
    """
    清理练习生成的文件
    """
    files_to_clean = [
        'employees.csv',
        'high_salary_employees.csv',
        'employee_analysis.json',
        'products.json',
        'employees_by_department.json',
        'dirty_data.csv',
        'clean_data.csv',
        'data_quality_report.json'
    ]
    
    # 清理批量文件
    import glob
    batch_files = glob.glob('sales_*.csv')
    files_to_clean.extend(batch_files)
    
    cleaned_count = 0
    for filename in files_to_clean:
        if os.path.exists(filename):
            os.remove(filename)
            cleaned_count += 1
            print(f"✓ 删除文件: {filename}")
    
    print(f"\n总共清理了 {cleaned_count} 个文件")


def run_all_exercises():
    """
    运行所有练习
    """
    print("Session07 练习2：CSV和JSON文件操作")
    print("=" * 50)
    
    exercises = [
        ("练习1：创建员工CSV文件", exercise1_create_employee_csv),
        ("练习2：读取和筛选CSV数据", exercise2_read_and_filter_csv),
        ("练习3：CSV数据分析", exercise3_csv_data_analysis),
        ("练习4：创建产品JSON文件", exercise4_create_product_json),
        ("练习5：JSON数据操作", exercise5_json_data_manipulation),
        ("练习6：CSV到JSON格式转换", exercise6_csv_to_json_conversion),
        ("练习7：数据验证和清洗", exercise7_data_validation),
        ("练习8：批量文件处理", exercise8_batch_file_processing),
        ("练习9：JSON数据结构验证", exercise9_json_schema_validation),
        ("练习10：性能对比测试", exercise10_performance_comparison)
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
    print("- CSV适合表格数据，JSON适合结构化数据")
    print("- 注意数据类型转换和验证")
    print("- 大数据量时考虑性能优化")
    print("- 数据清洗是数据处理的重要环节")
    print("- 选择合适的数据格式很重要")
    
    # 询问是否清理文件
    response = input("\n是否清理练习生成的文件？(y/n): ").lower().strip()
    if response == 'y':
        cleanup_exercise_files()
    else:
        print("练习文件已保留，你可以继续分析和学习。")


if __name__ == "__main__":
    run_all_exercises()