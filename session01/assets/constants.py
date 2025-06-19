#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session01 常量配置文件

本文件定义了Session01中使用的所有常量，包括：
- 程序信息常量
- 界面显示常量
- 数学计算常量
- 错误信息常量

作者: Python教程团队
创建日期: 2024-01-01
"""

# 程序信息常量
PROGRAM_NAME = "Python新手教程"
SESSION_NAME = "Session01: 环境搭建与Hello World"
VERSION = "1.0.0"
AUTHOR = "Python教程团队"
CREATE_DATE = "2024-01-01"

# 项目信息
PROJECT_NAME = "交互式计算器"
PROJECT_VERSION = "1.0.0"
PROJECT_DESCRIPTION = "一个功能完整的交互式计算器程序"

# 界面显示常量
WELCOME_WIDTH = 50
BORDER_CHAR = "="
SEPARATOR_CHAR = "-"

# Unicode字符常量
UNICODE_BORDERS = {
    'top_left': '╔',
    'top_right': '╗',
    'bottom_left': '╚',
    'bottom_right': '╝',
    'horizontal': '═',
    'vertical': '║',
    'cross': '╬',
    'top_tee': '╦',
    'bottom_tee': '╩',
    'left_tee': '╠',
    'right_tee': '╣'
}

SIMPLE_BORDERS = {
    'top_left': '┌',
    'top_right': '┐',
    'bottom_left': '└',
    'bottom_right': '┘',
    'horizontal': '─',
    'vertical': '│',
    'cross': '┼',
    'top_tee': '┬',
    'bottom_tee': '┴',
    'left_tee': '├',
    'right_tee': '┤'
}

# 表情符号常量
EMOJI = {
    'success': '✅',
    'error': '❌',
    'warning': '⚠️',
    'info': 'ℹ️',
    'calculator': '🧮',
    'book': '📚',
    'rocket': '🚀',
    'star': '⭐',
    'heart': '❤️',
    'thumbs_up': '👍',
    'wave': '👋',
    'computer': '💻',
    'graduation': '🎓',
    'light_bulb': '💡',
    'memo': '📝'
}

# 数学常量
PI = 3.14159265359
E = 2.71828182846
GOLDEN_RATIO = 1.61803398875

# 计算器相关常量
MAX_HISTORY_ITEMS = 10
DEFAULT_PRECISION = 2
MAX_INPUT_LENGTH = 100

# 错误信息常量
ERROR_MESSAGES = {
    'invalid_number': '请输入有效的数字！',
    'division_by_zero': '除数不能为零',
    'negative_sqrt': '负数不能开平方根',
    'unknown_command': '未知命令',
    'invalid_syntax': '命令格式错误',
    'missing_parameters': '缺少必要参数',
    'too_many_parameters': '参数过多'
}

# 成功信息常量
SUCCESS_MESSAGES = {
    'calculation_complete': '计算完成',
    'history_cleared': '历史记录已清除',
    'welcome': '欢迎使用计算器',
    'goodbye': '感谢使用，再见'
}

# 提示信息常量
PROMPT_MESSAGES = {
    'enter_command': '请输入命令 (输入 \'help\' 查看帮助)',
    'enter_name': '请输入你的姓名',
    'enter_age': '请输入你的年龄',
    'enter_number': '请输入一个数字',
    'enter_first_number': '请输入第一个数字',
    'enter_second_number': '请输入第二个数字'
}

# 帮助信息常量
HELP_COMMANDS = {
    'add': 'add <a> <b>     - 加法运算',
    'sub': 'sub <a> <b>     - 减法运算',
    'mul': 'mul <a> <b>     - 乘法运算',
    'div': 'div <a> <b>     - 除法运算',
    'pow': 'pow <a> <b>     - 幂运算 (a^b)',
    'sqrt': 'sqrt <a>        - 开平方根',
    'abs': 'abs <a>         - 绝对值',
    'history': 'history         - 查看计算历史',
    'clear': 'clear           - 清除历史记录',
    'help': 'help            - 显示此帮助',
    'quit': 'quit            - 退出程序'
}

# 学生信息示例常量
SAMPLE_STUDENT_INFO = {
    'name': '张三',
    'age': 20,
    'height': 175.5,
    'weight': 68.2,
    'is_enrolled': True,
    'grade': '大二',
    'major': '计算机科学与技术'
}

# 课程信息常量
COURSE_INFO = {
    'total_sessions': 30,
    'current_session': 1,
    'session_title': '环境搭建与Hello World',
    'estimated_time': '2-3小时',
    'difficulty': '入门级',
    'prerequisites': ['基本计算机操作'],
    'learning_objectives': [
        '掌握Python的安装与配置',
        '了解IDE的选择与设置',
        '编写第一个Python程序',
        '理解Python程序的基本结构',
        '掌握基本的输入输出操作'
    ]
}

# 文件路径常量
FILE_PATHS = {
    'session_root': 'session01',
    'examples_dir': 'examples',
    'exercises_dir': 'exercises',
    'solutions_dir': 'solutions',
    'project_dir': 'project',
    'assets_dir': 'assets'
}

# 颜色代码常量（ANSI）
COLORS = {
    'reset': '\033[0m',
    'bold': '\033[1m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'bg_red': '\033[41m',
    'bg_green': '\033[42m',
    'bg_yellow': '\033[43m',
    'bg_blue': '\033[44m'
}

# 格式化模板常量
FORMAT_TEMPLATES = {
    'student_info': '姓名: {name}, 年龄: {age}, 身高: {height}cm',
    'calculation_result': '{operation} = {result}',
    'error_format': '{emoji} 错误: {message}',
    'success_format': '{emoji} {message}',
    'prompt_format': '{emoji} {message}: '
}

# 数据验证常量
VALIDATION_RULES = {
    'min_age': 0,
    'max_age': 150,
    'min_height': 50.0,
    'max_height': 300.0,
    'min_weight': 10.0,
    'max_weight': 500.0,
    'max_name_length': 50
}

# 默认值常量
DEFAULT_VALUES = {
    'student_name': '学生',
    'student_age': 18,
    'student_height': 170.0,
    'student_weight': 60.0,
    'current_year': 2024,
    'precision': 2,
    'timeout': 30
}