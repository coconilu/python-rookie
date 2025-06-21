#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session04 练习题3解答：综合练习

本文件包含exercise3.py中所有综合练习题的参考解答。
这些解答展示了条件语句和循环语句的综合应用。

作者: Python教程团队
创建日期: 2024-12-21
"""


def student_grade_analyzer(students_data):
    """
    练习1解答：学生成绩分析器
    """
    if not students_data:
        return {}
    
    # 获取所有课程名称
    all_subjects = set()
    for student_grades in students_data.values():
        all_subjects.update(student_grades.keys())
    all_subjects = list(all_subjects)
    
    # 学生分析
    students_analysis = {}
    grade_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    
    for name, grades in students_data.items():
        total_score = sum(grades.values())
        average = total_score / len(grades)
        
        # 计算等级
        if average >= 90:
            grade = 'A'
        elif average >= 80:
            grade = 'B'
        elif average >= 70:
            grade = 'C'
        elif average >= 60:
            grade = 'D'
        else:
            grade = 'F'
        
        grade_counts[grade] += 1
        
        students_analysis[name] = {
            'grades': grades,
            'total': total_score,
            'average': round(average, 2),
            'grade': grade
        }
    
    # 课程分析
    subjects_analysis = {}
    for subject in all_subjects:
        subject_scores = []
        for student_grades in students_data.values():
            if subject in student_grades:
                subject_scores.append(student_grades[subject])
        
        if subject_scores:
            subjects_analysis[subject] = {
                'average': round(sum(subject_scores) / len(subject_scores), 2),
                'max': max(subject_scores),
                'min': min(subject_scores),
                'count': len(subject_scores)
            }
    
    # 班级统计
    all_scores = []
    for student_grades in students_data.values():
        all_scores.extend(student_grades.values())
    
    class_stats = {
        'total_students': len(students_data),
        'total_scores': len(all_scores),
        'average': round(sum(all_scores) / len(all_scores), 2),
        'max': max(all_scores),
        'min': min(all_scores)
    }
    
    return {
        'students': students_analysis,
        'subjects': subjects_analysis,
        'class_stats': class_stats,
        'grade_distribution': grade_counts
    }


def calendar_generator(year, month):
    """
    练习2解答：日历生成器
    """
    # 月份名称和天数
    month_names = [
        "", "1月", "2月", "3月", "4月", "5月", "6月",
        "7月", "8月", "9月", "10月", "11月", "12月"
    ]
    
    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    # 检查闰年
    def is_leap_year(y):
        return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)
    
    if is_leap_year(year):
        days_in_month[2] = 29
    
    # 计算该月第一天是星期几（使用蔡勒公式）
    def get_weekday(y, m, d):
        if m < 3:
            m += 12
            y -= 1
        
        q = d
        m = m
        k = y % 100
        j = y // 100
        
        h = (q + (13 * (m + 1)) // 5 + k + k // 4 + j // 4 - 2 * j) % 7
        # 转换为周日=0的格式
        return (h + 5) % 7
    
    first_weekday = get_weekday(year, month, 1)
    days_count = days_in_month[month]
    
    # 生成日历字符串
    calendar_str = f"      {year}年{month_names[month]}\n"
    calendar_str += "日  一  二  三  四  五  六\n"
    
    # 第一周的空格
    calendar_str += "   " * first_weekday
    
    # 填入日期
    current_weekday = first_weekday
    for day in range(1, days_count + 1):
        calendar_str += f"{day:2d} "
        current_weekday += 1
        
        if current_weekday % 7 == 0:
            calendar_str += "\n"
    
    return calendar_str.rstrip()


def text_statistics_analyzer(text):
    """
    练习3解答：文本统计分析器
    """
    import string
    
    # 字符统计
    total_chars = len(text)
    letters = sum(1 for c in text if c.isalpha())
    digits = sum(1 for c in text if c.isdigit())
    spaces = sum(1 for c in text if c.isspace())
    punctuation = sum(1 for c in text if c in string.punctuation)
    
    # 单词统计
    words = text.split()
    word_count = len(words)
    if word_count > 0:
        avg_word_length = sum(len(word.strip(string.punctuation)) for word in words) / word_count
        longest_word = max(words, key=lambda w: len(w.strip(string.punctuation)))
        shortest_word = min(words, key=lambda w: len(w.strip(string.punctuation)))
    else:
        avg_word_length = 0
        longest_word = ""
        shortest_word = ""
    
    # 行统计
    lines = text.split('\n')
    line_count = len(lines)
    avg_chars_per_line = total_chars / line_count if line_count > 0 else 0
    
    # 字符频率统计
    char_frequency = {}
    for char in text.lower():
        if char.isalnum():  # 只统计字母和数字
            char_frequency[char] = char_frequency.get(char, 0) + 1
    
    # 按频率排序
    sorted_chars = sorted(char_frequency.items(), key=lambda x: x[1], reverse=True)
    
    return {
        'char_stats': {
            'total': total_chars,
            'letters': letters,
            'digits': digits,
            'spaces': spaces,
            'punctuation': punctuation
        },
        'word_stats': {
            'total_words': word_count,
            'avg_length': round(avg_word_length, 2),
            'longest': longest_word,
            'shortest': shortest_word
        },
        'line_stats': {
            'total_lines': line_count,
            'avg_chars_per_line': round(avg_chars_per_line, 2)
        },
        'char_frequency': sorted_chars[:10]  # 前10个最频繁的字符
    }


def number_pattern_detector(numbers):
    """
    练习4解答：数字模式检测器
    """
    if len(numbers) < 2:
        return {
            'is_arithmetic': False,
            'is_geometric': False,
            'is_fibonacci': False,
            'is_increasing': False,
            'is_decreasing': False
        }
    
    # 检查等差数列
    is_arithmetic = True
    arithmetic_diff = numbers[1] - numbers[0]
    for i in range(2, len(numbers)):
        if numbers[i] - numbers[i-1] != arithmetic_diff:
            is_arithmetic = False
            break
    
    # 检查等比数列
    is_geometric = True
    geometric_ratio = None
    if numbers[0] != 0:
        geometric_ratio = numbers[1] / numbers[0]
        for i in range(2, len(numbers)):
            if numbers[i-1] == 0 or abs(numbers[i] / numbers[i-1] - geometric_ratio) > 1e-10:
                is_geometric = False
                break
    else:
        is_geometric = False
    
    # 检查斐波那契数列
    is_fibonacci = True
    if len(numbers) >= 3:
        for i in range(2, len(numbers)):
            if numbers[i] != numbers[i-1] + numbers[i-2]:
                is_fibonacci = False
                break
    else:
        is_fibonacci = False
    
    # 检查递增/递减
    is_increasing = all(numbers[i] <= numbers[i+1] for i in range(len(numbers)-1))
    is_decreasing = all(numbers[i] >= numbers[i+1] for i in range(len(numbers)-1))
    
    # 找最长连续递增子序列
    max_inc_length = 1
    current_inc_length = 1
    for i in range(1, len(numbers)):
        if numbers[i] > numbers[i-1]:
            current_inc_length += 1
            max_inc_length = max(max_inc_length, current_inc_length)
        else:
            current_inc_length = 1
    
    # 找最长连续递减子序列
    max_dec_length = 1
    current_dec_length = 1
    for i in range(1, len(numbers)):
        if numbers[i] < numbers[i-1]:
            current_dec_length += 1
            max_dec_length = max(max_dec_length, current_dec_length)
        else:
            current_dec_length = 1
    
    result = {
        'is_arithmetic': is_arithmetic,
        'is_geometric': is_geometric,
        'is_fibonacci': is_fibonacci,
        'is_increasing': is_increasing,
        'is_decreasing': is_decreasing,
        'max_increasing_length': max_inc_length,
        'max_decreasing_length': max_dec_length
    }
    
    if is_arithmetic:
        result['arithmetic_diff'] = arithmetic_diff
    if is_geometric:
        result['geometric_ratio'] = geometric_ratio
    
    return result


def password_generator(length=12, include_uppercase=True, include_lowercase=True, 
                      include_numbers=True, include_symbols=True, exclude_ambiguous=True):
    """
    练习5解答：密码生成器
    """
    import random
    import string
    
    # 定义字符集
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    numbers = string.digits
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # 排除容易混淆的字符
    if exclude_ambiguous:
        ambiguous = "0O1lI"
        uppercase = ''.join(c for c in uppercase if c not in ambiguous)
        lowercase = ''.join(c for c in lowercase if c not in ambiguous)
        numbers = ''.join(c for c in numbers if c not in ambiguous)
    
    # 构建可用字符集
    available_chars = ""
    required_chars = []
    
    if include_uppercase:
        available_chars += uppercase
        required_chars.append(random.choice(uppercase))
    if include_lowercase:
        available_chars += lowercase
        required_chars.append(random.choice(lowercase))
    if include_numbers:
        available_chars += numbers
        required_chars.append(random.choice(numbers))
    if include_symbols:
        available_chars += symbols
        required_chars.append(random.choice(symbols))
    
    if not available_chars:
        return []
    
    passwords = []
    for _ in range(5):  # 生成5个候选密码
        password = required_chars.copy()
        
        # 填充剩余长度
        for _ in range(length - len(required_chars)):
            password.append(random.choice(available_chars))
        
        # 打乱顺序
        random.shuffle(password)
        passwords.append(''.join(password))
    
    return passwords


def maze_solver(maze):
    """
    练习6解答：迷宫求解器
    """
    if not maze or not maze[0]:
        return []
    
    rows, cols = len(maze), len(maze[0])
    
    # 找到起点和终点
    start = end = None
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == 2:
                start = (i, j)
            elif maze[i][j] == 3:
                end = (i, j)
    
    if not start or not end:
        return []
    
    # 深度优先搜索
    def dfs(x, y, path, visited):
        if (x, y) == end:
            return path + [(x, y)]
        
        visited.add((x, y))
        
        # 四个方向：上、下、左、右
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if (0 <= nx < rows and 0 <= ny < cols and 
                (nx, ny) not in visited and 
                maze[nx][ny] != 1):  # 不是墙壁
                
                result = dfs(nx, ny, path + [(x, y)], visited.copy())
                if result:
                    return result
        
        return None
    
    path = dfs(start[0], start[1], [], set())
    return path if path else []


def stock_price_analyzer(prices):
    """
    练习7解答：股票价格分析器
    """
    if len(prices) < 5:
        return {}
    
    # 计算简单移动平均线
    def calculate_sma(data, period):
        sma = []
        for i in range(period - 1, len(data)):
            avg = sum(data[i - period + 1:i + 1]) / period
            sma.append(round(avg, 2))
        return sma
    
    sma_5 = calculate_sma(prices, 5)
    sma_10 = calculate_sma(prices, 10) if len(prices) >= 10 else []
    
    # 计算最大回撤
    max_drawdown = 0
    peak = prices[0]
    for price in prices:
        if price > peak:
            peak = price
        drawdown = (peak - price) / peak
        max_drawdown = max(max_drawdown, drawdown)
    
    # 计算波动率（标准差）
    mean_price = sum(prices) / len(prices)
    variance = sum((price - mean_price) ** 2 for price in prices) / len(prices)
    volatility = variance ** 0.5
    
    # 寻找支撑位和阻力位（简化版本）
    sorted_prices = sorted(set(prices))
    support_level = sorted_prices[len(sorted_prices) // 4]  # 25%分位数
    resistance_level = sorted_prices[len(sorted_prices) * 3 // 4]  # 75%分位数
    
    return {
        'sma_5': sma_5,
        'sma_10': sma_10,
        'max_drawdown': round(max_drawdown * 100, 2),  # 百分比
        'volatility': round(volatility, 2),
        'support_level': support_level,
        'resistance_level': resistance_level,
        'current_price': prices[-1],
        'price_change': round(((prices[-1] - prices[0]) / prices[0]) * 100, 2)
    }


def sudoku_validator(board):
    """
    练习8解答：数独验证器
    """
    def is_valid_unit(unit):
        """检查一个单元（行、列或3x3方格）是否有效"""
        non_zero = [num for num in unit if num != 0]
        return len(non_zero) == len(set(non_zero))
    
    errors = []
    
    # 检查行
    for i, row in enumerate(board):
        if not is_valid_unit(row):
            errors.append(f"第{i+1}行有重复数字")
    
    # 检查列
    for j in range(9):
        column = [board[i][j] for i in range(9)]
        if not is_valid_unit(column):
            errors.append(f"第{j+1}列有重复数字")
    
    # 检查3x3方格
    for box_row in range(3):
        for box_col in range(3):
            box = []
            for i in range(3):
                for j in range(3):
                    box.append(board[box_row * 3 + i][box_col * 3 + j])
            if not is_valid_unit(box):
                errors.append(f"第{box_row * 3 + box_col + 1}个3x3方格有重复数字")
    
    return {
        'is_valid': len(errors) == 0,
        'errors': errors
    }


def main():
    """
    主函数：测试所有综合练习解答
    """
    print("Session04 练习题3解答：综合练习")
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
    print(f"班级平均分: {result1['class_stats']['average']}")
    print(f"等级分布: {result1['grade_distribution']}")
    
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
    print(f"总字符数: {result3['char_stats']['total']}")
    print(f"单词数: {result3['word_stats']['total_words']}")
    print(f"最频繁字符: {result3['char_frequency'][:3]}")
    
    # 测试练习4：数字模式检测
    print("\n练习4：数字模式检测测试")
    test_sequences = [
        [1, 3, 5, 7, 9],  # 等差数列
        [2, 4, 8, 16, 32],  # 等比数列
        [1, 1, 2, 3, 5, 8, 13],  # 斐波那契数列
    ]
    for i, seq in enumerate(test_sequences, 1):
        result = number_pattern_detector(seq)
        print(f"序列{i}: 等差={result['is_arithmetic']}, 等比={result['is_geometric']}, 斐波那契={result['is_fibonacci']}")
    
    # 测试练习5：密码生成
    print("\n练习5：密码生成测试")
    passwords = password_generator(12, True, True, True, True, True)
    print(f"生成的密码示例: {passwords[0] if passwords else '无'}")
    
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
    print(f"迷宫路径长度: {len(path) if path else 0}")
    
    # 测试练习7：股票分析
    print("\n练习7：股票分析测试")
    stock_prices = [100, 102, 98, 105, 110, 108, 112, 115, 113, 118, 120, 116, 122]
    result7 = stock_price_analyzer(stock_prices)
    print(f"5日均线: {result7.get('sma_5', [])[-3:] if result7.get('sma_5') else []}")
    print(f"最大回撤: {result7.get('max_drawdown', 0)}%")
    
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
    print(f"数独有效性: {result8['is_valid']}")
    if result8['errors']:
        print(f"错误: {result8['errors']}")
    
    print("\n" + "=" * 50)
    print("综合练习解答测试完成！")
    print("\n📝 学习要点：")
    print("1. 综合练习需要灵活运用多种编程技巧")
    print("2. 算法设计要考虑时间和空间复杂度")
    print("3. 代码结构要清晰，便于理解和维护")
    print("4. 边界条件和异常情况的处理很重要")
    print("5. 实际问题往往需要多种数据结构和算法的组合")


if __name__ == "__main__":
    main()