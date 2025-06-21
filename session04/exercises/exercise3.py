#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session04 练习题3：综合练习

本练习综合考查条件语句和循环语句的使用，包括：
1. 复杂的条件判断与循环结合
2. 嵌套循环和条件语句
3. 实际问题的算法实现
4. 数据处理和分析

这些练习更接近实际编程场景，需要综合运用所学知识。

作者: Python教程团队
创建日期: 2024-12-21
"""


def student_grade_analyzer(students_data):
    """
    练习1：学生成绩分析器
    
    分析学生成绩数据，计算各种统计信息：
    1. 每个学生的平均分和等级
    2. 每门课程的平均分
    3. 班级整体统计（最高分、最低分、平均分）
    4. 各等级人数统计
    
    等级标准：
    - A: 90-100
    - B: 80-89
    - C: 70-79
    - D: 60-69
    - F: 0-59
    
    参数:
        students_data (dict): 学生数据，格式如下：
        {
            '张三': {'数学': 85, '语文': 92, '英语': 78},
            '李四': {'数学': 76, '语文': 88, '英语': 82},
            ...
        }
    
    返回:
        dict: 分析结果，包含学生分析、课程分析、班级统计、等级统计
    
    示例:
        >>> data = {
        ...     '张三': {'数学': 85, '语文': 92, '英语': 78},
        ...     '李四': {'数学': 76, '语文': 88, '英语': 82}
        ... }
        >>> result = student_grade_analyzer(data)
        >>> result['students']['张三']['average']
        85.0
    """
    # 在这里编写你的代码
    pass


def calendar_generator(year, month):
    """
    练习2：日历生成器
    
    生成指定年月的日历，要求：
    1. 正确处理闰年
    2. 正确计算月份的第一天是星期几
    3. 格式化输出日历
    
    参数:
        year (int): 年份
        month (int): 月份 (1-12)
    
    返回:
        str: 格式化的日历字符串
    
    示例:
        >>> print(calendar_generator(2024, 2))
              2024年2月
        日  一  二  三  四  五  六
                     1   2   3
         4   5   6   7   8   9  10
        11  12  13  14  15  16  17
        18  19  20  21  22  23  24
        25  26  27  28  29
    """
    # 在这里编写你的代码
    pass


def text_statistics_analyzer(text):
    """
    练习3：文本统计分析器
    
    分析文本的各种统计信息：
    1. 字符统计（总字符数、字母、数字、空格、标点符号）
    2. 单词统计（总单词数、平均单词长度、最长/最短单词）
    3. 行统计（总行数、平均每行字符数）
    4. 字符频率统计（按频率排序）
    
    参数:
        text (str): 要分析的文本
    
    返回:
        dict: 统计结果字典
    
    示例:
        >>> result = text_statistics_analyzer("Hello World!\nPython is great.")
        >>> result['char_stats']['total']
        28
    """
    # 在这里编写你的代码
    pass


def number_pattern_detector(numbers):
    """
    练习4：数字模式检测器
    
    检测数字序列中的各种模式：
    1. 是否为等差数列
    2. 是否为等比数列
    3. 是否为斐波那契数列
    4. 是否为递增/递减序列
    5. 找出最长的连续递增/递减子序列
    
    参数:
        numbers (list): 数字列表
    
    返回:
        dict: 模式检测结果
    
    示例:
        >>> result = number_pattern_detector([1, 3, 5, 7, 9])
        >>> result['is_arithmetic']
        True
        >>> result['arithmetic_diff']
        2
    """
    # 在这里编写你的代码
    pass


def password_generator(length=12, include_uppercase=True, include_lowercase=True, 
                      include_numbers=True, include_symbols=True, exclude_ambiguous=True):
    """
    练习5：密码生成器
    
    根据指定规则生成安全密码：
    1. 可配置密码长度
    2. 可选择包含的字符类型
    3. 可排除容易混淆的字符（如0和O，1和l）
    4. 确保至少包含每种选中的字符类型
    5. 生成多个候选密码供选择
    
    参数:
        length (int): 密码长度
        include_uppercase (bool): 是否包含大写字母
        include_lowercase (bool): 是否包含小写字母
        include_numbers (bool): 是否包含数字
        include_symbols (bool): 是否包含符号
        exclude_ambiguous (bool): 是否排除容易混淆的字符
    
    返回:
        list: 生成的密码列表（5个候选）
    
    示例:
        >>> passwords = password_generator(8, True, True, True, False)
        >>> len(passwords)
        5
        >>> all(len(pwd) == 8 for pwd in passwords)
        True
    """
    import random
    import string
    
    # 在这里编写你的代码
    pass


def maze_solver(maze):
    """
    练习6：迷宫求解器
    
    使用深度优先搜索算法解决迷宫问题：
    1. 找到从起点到终点的路径
    2. 如果有多条路径，找到最短路径
    3. 返回路径坐标列表
    
    迷宫表示：
    - 0: 可通行
    - 1: 墙壁
    - 2: 起点
    - 3: 终点
    
    参数:
        maze (list): 二维列表表示的迷宫
    
    返回:
        list: 路径坐标列表，如果无解返回空列表
    
    示例:
        >>> maze = [
        ...     [2, 0, 1, 0],
        ...     [0, 0, 1, 0],
        ...     [1, 0, 0, 0],
        ...     [1, 1, 1, 3]
        ... ]
        >>> path = maze_solver(maze)
        >>> len(path) > 0
        True
    """
    # 在这里编写你的代码
    pass


def stock_price_analyzer(prices):
    """
    练习7：股票价格分析器
    
    分析股票价格数据，计算各种技术指标：
    1. 简单移动平均线（SMA）
    2. 最大回撤
    3. 买卖信号（金叉死叉）
    4. 价格波动率
    5. 支撑位和阻力位
    
    参数:
        prices (list): 股票价格列表（按时间顺序）
    
    返回:
        dict: 分析结果
    
    示例:
        >>> prices = [100, 102, 98, 105, 110, 108, 112, 115, 113, 118]
        >>> result = stock_price_analyzer(prices)
        >>> 'sma_5' in result
        True
    """
    # 在这里编写你的代码
    pass


def sudoku_validator(board):
    """
    练习8：数独验证器
    
    验证9×9数独是否有效：
    1. 每行包含1-9的数字，无重复
    2. 每列包含1-9的数字，无重复
    3. 每个3×3子网格包含1-9的数字，无重复
    4. 0表示空格（未填入的位置）
    
    参数:
        board (list): 9×9的二维列表表示数独
    
    返回:
        dict: 验证结果，包含是否有效和错误详情
    
    示例:
        >>> board = [[5,3,0,0,7,0,0,0,0],
        ...          [6,0,0,1,9,5,0,0,0],
        ...          [0,9,8,0,0,0,0,6,0],
        ...          [8,0,0,0,6,0,0,0,3],
        ...          [4,0,0,8,0,3,0,0,1],
        ...          [7,0,0,0,2,0,0,0,6],
        ...          [0,6,0,0,0,0,2,8,0],
        ...          [0,0,0,4,1,9,0,0,5],
        ...          [0,0,0,0,8,0,0,7,9]]
        >>> result = sudoku_validator(board)
        >>> result['is_valid']
        True
    """
    # 在这里编写你的代码
    pass


def main():
    """
    主函数：测试所有综合练习
    """
    print("Session04 练习题3：综合练习")
    print("=" * 50)
    
    # 测试练习1：学生成绩分析
    print("\n练习1：学生成绩分析测试")
    students_data = {
        '张三': {'数学': 85, '语文': 92, '英语': 78},
        '李四': {'数学': 76, '语文': 88, '英语': 82},
        '王五': {'数学': 94, '语文': 85, '英语': 90},
        '赵六': {'数学': 68, '语文': 72, '英语': 75}
    }
    result1 = student_grade_analyzer(students_data)
    print(f"成绩分析结果: {result1}")
    
    # 测试练习2：日历生成
    print("\n练习2：日历生成测试")
    calendar_str = calendar_generator(2024, 2)
    print("2024年2月日历:")
    print(calendar_str)
    
    # 测试练习3：文本统计
    print("\n练习3：文本统计测试")
    sample_text = """Hello World!
Python is a great programming language.
It's easy to learn and powerful to use."""
    result3 = text_statistics_analyzer(sample_text)
    print(f"文本统计结果: {result3}")
    
    # 测试练习4：数字模式检测
    print("\n练习4：数字模式检测测试")
    test_sequences = [
        [1, 3, 5, 7, 9],  # 等差数列
        [2, 4, 8, 16, 32],  # 等比数列
        [1, 1, 2, 3, 5, 8, 13],  # 斐波那契数列
        [5, 3, 8, 1, 9, 2]  # 随机序列
    ]
    for i, seq in enumerate(test_sequences, 1):
        result = number_pattern_detector(seq)
        print(f"序列{i} {seq}: {result}")
    
    # 测试练习5：密码生成
    print("\n练习5：密码生成测试")
    passwords = password_generator(12, True, True, True, True, True)
    print(f"生成的密码: {passwords}")
    
    # 测试练习6：迷宫求解
    print("\n练习6：迷宫求解测试")
    test_maze = [
        [2, 0, 1, 0, 0],
        [0, 0, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 0, 0],
        [0, 0, 0, 0, 3]
    ]
    path = maze_solver(test_maze)
    print(f"迷宫路径: {path}")
    
    # 测试练习7：股票分析
    print("\n练习7：股票分析测试")
    stock_prices = [100, 102, 98, 105, 110, 108, 112, 115, 113, 118, 120, 116, 122]
    result7 = stock_price_analyzer(stock_prices)
    print(f"股票分析结果: {result7}")
    
    # 测试练习8：数独验证
    print("\n练习8：数独验证测试")
    sudoku_board = [
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]
    ]
    result8 = sudoku_validator(sudoku_board)
    print(f"数独验证结果: {result8}")
    
    print("\n" + "=" * 50)
    print("综合练习测试完成！")
    print("\n💡 提示：")
    print("1. 这些是高难度的综合练习，需要综合运用多种知识")
    print("2. 建议先完成前面的基础练习再挑战这些题目")
    print("3. 可以分步骤实现，先实现基本功能再优化")
    print("4. 注意代码的可读性和效率")
    print("5. 遇到困难可以查阅相关算法资料")


if __name__ == "__main__":
    main()