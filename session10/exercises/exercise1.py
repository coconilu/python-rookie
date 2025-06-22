#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercise 1: 模块导入练习

练习目标：
1. 掌握不同的模块导入方式
2. 理解模块别名的使用
3. 学会使用标准库模块
4. 练习模块内省

请完成以下练习题
"""

# 练习1：基础导入练习
def exercise_1_basic_imports():
    """
    练习1：基础导入练习
    
    任务：
    1. 导入math模块，计算圆的面积（半径为5）
    2. 从random模块导入randint函数，生成1-100之间的随机数
    3. 导入datetime模块并使用别名dt，获取当前时间
    4. 从os.path模块导入join和exists函数
    
    提示：
    - 圆的面积公式：π * r²
    - 使用math.pi获取π值
    """
    print("=== 练习1：基础导入练习 ===")
    
    # TODO: 在这里完成你的代码
    # 1. 导入math模块
    
    # 2. 计算圆的面积（半径为5）
    radius = 5
    # area = ?  # 使用math模块计算
    # print(f"半径为{radius}的圆的面积: {area:.2f}")
    
    # 3. 从random模块导入randint
    
    # 4. 生成随机数
    # random_num = ?  # 生成1-100之间的随机数
    # print(f"随机数: {random_num}")
    
    # 5. 导入datetime模块并使用别名dt
    
    # 6. 获取当前时间
    # now = ?  # 获取当前时间
    # print(f"当前时间: {now}")
    
    # 7. 从os.path导入join和exists
    
    # 8. 测试路径操作
    # test_path = ?  # 使用join连接路径
    # path_exists = ?  # 检查路径是否存在
    # print(f"路径 '{test_path}' 存在: {path_exists}")
    
    print("练习1完成！\n")


# 练习2：模块内省练习
def exercise_2_module_introspection():
    """
    练习2：模块内省练习
    
    任务：
    1. 导入sys模块
    2. 打印Python版本信息
    3. 打印模块搜索路径
    4. 列出sys模块的所有属性（只显示前10个）
    5. 检查某个属性是否存在于模块中
    """
    print("=== 练习2：模块内省练习 ===")
    
    # TODO: 在这里完成你的代码
    # 1. 导入sys模块
    
    # 2. 打印Python版本信息
    # print(f"Python版本: {?}")
    
    # 3. 打印模块搜索路径（只显示前3个）
    # print("模块搜索路径（前3个）:")
    # for i, path in enumerate(?, 1):
    #     print(f"  {i}. {path}")
    #     if i >= 3:
    #         break
    
    # 4. 列出sys模块的所有属性（只显示前10个）
    # attributes = ?  # 获取sys模块的所有属性
    # print(f"\nsys模块的属性（前10个）:")
    # for i, attr in enumerate(?, 1):
    #     print(f"  {i}. {attr}")
    #     if i >= 10:
    #         break
    
    # 5. 检查某个属性是否存在
    # check_attrs = ['version', 'path', 'platform', 'nonexistent_attr']
    # print(f"\n属性存在性检查:")
    # for attr in check_attrs:
    #     exists = ?  # 检查属性是否存在
    #     print(f"  {attr}: {'存在' if exists else '不存在'}")
    
    print("练习2完成！\n")


# 练习3：文件操作模块练习
def exercise_3_file_operations():
    """
    练习3：文件操作模块练习
    
    任务：
    1. 使用os模块获取当前工作目录
    2. 使用glob模块查找当前目录下的所有.py文件
    3. 使用pathlib模块创建Path对象并获取文件信息
    4. 使用shutil模块的功能（模拟，不实际执行）
    """
    print("=== 练习3：文件操作模块练习 ===")
    
    # TODO: 在这里完成你的代码
    # 1. 导入需要的模块
    
    # 2. 获取当前工作目录
    # current_dir = ?  # 使用os模块
    # print(f"当前工作目录: {current_dir}")
    
    # 3. 查找当前目录下的所有.py文件
    # py_files = ?  # 使用glob模块
    # print(f"\n找到的Python文件:")
    # for i, file in enumerate(py_files, 1):
    #     print(f"  {i}. {file}")
    
    # 4. 使用pathlib创建Path对象
    # current_path = ?  # 创建当前目录的Path对象
    # print(f"\n使用pathlib:")
    # print(f"  路径: {current_path}")
    # print(f"  绝对路径: {?}")  # 获取绝对路径
    # print(f"  是否为目录: {?}")  # 检查是否为目录
    # print(f"  父目录: {?}")  # 获取父目录
    
    # 5. 演示shutil功能（仅打印，不实际执行）
    # print(f"\nshutil模块功能演示（仅演示，不实际执行）:")
    # print(f"  复制文件: shutil.copy('source.txt', 'dest.txt')")
    # print(f"  移动文件: shutil.move('old_name.txt', 'new_name.txt')")
    # print(f"  删除目录树: shutil.rmtree('directory_to_remove')")
    
    print("练习3完成！\n")


# 练习4：时间和日期模块练习
def exercise_4_datetime_operations():
    """
    练习4：时间和日期模块练习
    
    任务：
    1. 使用datetime模块创建特定日期
    2. 计算日期差值
    3. 格式化日期字符串
    4. 使用time模块获取时间戳
    """
    print("=== 练习4：时间和日期模块练习 ===")
    
    # TODO: 在这里完成你的代码
    # 1. 导入需要的模块
    
    # 2. 创建特定日期
    # birthday = ?  # 创建你的生日日期（例如：1990年1月1日）
    # print(f"生日: {birthday}")
    
    # 3. 获取当前日期
    # today = ?  # 获取今天的日期
    # print(f"今天: {today}")
    
    # 4. 计算年龄（天数）
    # age_days = ?  # 计算从生日到今天的天数
    # print(f"年龄: {age_days.days} 天")
    
    # 5. 格式化日期
    # formatted_birthday = ?  # 将生日格式化为 "YYYY年MM月DD日"
    # print(f"格式化的生日: {formatted_birthday}")
    
    # 6. 获取时间戳
    # timestamp = ?  # 获取当前时间戳
    # print(f"当前时间戳: {timestamp}")
    
    # 7. 创建未来日期
    # future_date = ?  # 创建30天后的日期
    # print(f"30天后: {future_date}")
    
    print("练习4完成！\n")


# 练习5：数学和随机模块练习
def exercise_5_math_random():
    """
    练习5：数学和随机模块练习
    
    任务：
    1. 使用math模块进行各种数学计算
    2. 使用random模块生成随机数据
    3. 结合使用创建一个简单的数学游戏
    """
    print("=== 练习5：数学和随机模块练习 ===")
    
    # TODO: 在这里完成你的代码
    # 1. 导入需要的模块
    
    # 2. 数学计算
    # numbers = [16, 25, 36, 49, 64]
    # print("数学计算:")
    # for num in numbers:
    #     sqrt_val = ?  # 计算平方根
    #     log_val = ?   # 计算自然对数
    #     print(f"  {num}: 平方根={sqrt_val:.2f}, 对数={log_val:.2f}")
    
    # 3. 三角函数计算
    # angles = [0, 30, 45, 60, 90]  # 角度
    # print(f"\n三角函数计算:")
    # for angle in angles:
    #     radian = ?  # 将角度转换为弧度
    #     sin_val = ?  # 计算正弦值
    #     cos_val = ?  # 计算余弦值
    #     print(f"  {angle}°: sin={sin_val:.3f}, cos={cos_val:.3f}")
    
    # 4. 随机数生成
    # print(f"\n随机数生成:")
    # random_int = ?      # 生成1-10之间的随机整数
    # random_float = ?    # 生成0-1之间的随机浮点数
    # random_choice = ?   # 从列表中随机选择一个元素
    # colors = ['红', '绿', '蓝', '黄', '紫']
    # 
    # print(f"  随机整数(1-10): {random_int}")
    # print(f"  随机浮点数(0-1): {random_float:.3f}")
    # print(f"  随机颜色: {random_choice}")
    
    # 5. 创建随机数列表并排序
    # random_list = ?  # 生成10个1-100之间的随机数
    # print(f"\n随机数列表: {random_list}")
    # print(f"排序后: {sorted(random_list)}")
    
    # 6. 简单的猜数字游戏（模拟）
    # secret_number = ?  # 生成1-100之间的秘密数字
    # print(f"\n猜数字游戏（答案是{secret_number}）:")
    # guesses = [25, 50, 75, secret_number]  # 模拟猜测
    # for i, guess in enumerate(guesses, 1):
    #     if guess == secret_number:
    #         print(f"  第{i}次猜测: {guess} - 恭喜！猜对了！")
    #         break
    #     elif guess < secret_number:
    #         print(f"  第{i}次猜测: {guess} - 太小了")
    #     else:
    #         print(f"  第{i}次猜测: {guess} - 太大了")
    
    print("练习5完成！\n")


# 练习6：综合应用练习
def exercise_6_comprehensive():
    """
    练习6：综合应用练习
    
    任务：创建一个简单的文件分析器
    1. 分析当前目录下的Python文件
    2. 统计文件数量、总行数、平均行数
    3. 找出最大和最小的文件
    4. 生成分析报告
    """
    print("=== 练习6：综合应用练习 ===")
    
    # TODO: 在这里完成你的代码
    # 1. 导入需要的模块
    
    # 2. 获取当前目录下的所有Python文件
    # py_files = ?  # 使用glob查找.py文件
    
    # if not py_files:
    #     print("当前目录下没有找到Python文件")
    #     return
    
    # 3. 分析每个文件
    # file_stats = []
    # total_lines = 0
    # 
    # print("文件分析:")
    # for file_path in py_files:
    #     try:
    #         with open(file_path, 'r', encoding='utf-8') as f:
    #             lines = f.readlines()
    #             line_count = len(lines)
    #             total_lines += line_count
    #             
    #             # 获取文件大小
    #             file_size = ?  # 使用os.path.getsize获取文件大小
    #             
    #             file_stats.append({
    #                 'name': file_path,
    #                 'lines': line_count,
    #                 'size': file_size
    #             })
    #             
    #             print(f"  {file_path}: {line_count} 行, {file_size} 字节")
    #     
    #     except Exception as e:
    #         print(f"  {file_path}: 读取失败 - {e}")
    
    # 4. 计算统计信息
    # if file_stats:
    #     file_count = len(file_stats)
    #     avg_lines = ?  # 计算平均行数
    #     
    #     # 找出最大和最小的文件
    #     largest_file = ?  # 按行数找出最大文件
    #     smallest_file = ?  # 按行数找出最小文件
    #     
    #     # 5. 生成报告
    #     print(f"\n=== 分析报告 ===")
    #     print(f"文件总数: {file_count}")
    #     print(f"总行数: {total_lines}")
    #     print(f"平均行数: {avg_lines:.1f}")
    #     print(f"最大文件: {largest_file['name']} ({largest_file['lines']} 行)")
    #     print(f"最小文件: {smallest_file['name']} ({smallest_file['lines']} 行)")
    #     
    #     # 6. 生成报告时间戳
    #     report_time = ?  # 获取当前时间
    #     print(f"报告生成时间: {report_time}")
    
    print("练习6完成！\n")


def main():
    """
    主函数 - 运行所有练习
    """
    print("Session10 - Exercise1: 模块导入练习")
    print("=" * 60)
    
    # 运行所有练习
    exercise_1_basic_imports()
    exercise_2_module_introspection()
    exercise_3_file_operations()
    exercise_4_datetime_operations()
    exercise_5_math_random()
    exercise_6_comprehensive()
    
    print("=" * 60)
    print("所有练习完成！")
    print("\n练习要点总结:")
    print("1. 掌握import、from...import、import...as的用法")
    print("2. 学会使用dir()、hasattr()等内省函数")
    print("3. 熟悉常用标准库模块的基本用法")
    print("4. 理解模块导入的最佳实践")
    print("5. 能够综合运用多个模块解决实际问题")
    
    print("\n提示：")
    print("- 完成练习后，可以查看solutions目录下的参考答案")
    print("- 尝试修改代码，探索更多模块功能")
    print("- 阅读Python官方文档了解更多标准库模块")


if __name__ == "__main__":
    main()