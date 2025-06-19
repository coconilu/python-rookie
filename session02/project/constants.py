#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
常量定义模块

定义项目中使用的各种常量，包括菜单选项、消息文本、数值范围等。
这展示了如何使用常量来提高代码的可维护性和可读性。

作者: Python教程团队
创建日期: 2024-12-19
"""

# ==================== 应用程序信息 ====================

APP_NAME = "个人信息管理系统"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Python教程团队"
APP_DESCRIPTION = "基于命令行的个人信息管理系统，用于学习Python变量与数据类型"

# ==================== 菜单选项 ====================

MENU_OPTIONS = {
    1: "录入新用户信息",
    2: "显示用户信息", 
    3: "查看统计信息",
    4: "搜索用户",
    5: "列出所有用户",
    6: "退出系统"
}

# 搜索菜单选项
SEARCH_OPTIONS = {
    1: "按姓名搜索",
    2: "按年龄范围搜索",
    3: "按用户类型搜索"
}

# ==================== 消息文本 ====================

WELCOME_MESSAGE = f"欢迎使用 {APP_NAME} v{APP_VERSION}"
GOODBYE_MESSAGE = "感谢使用，再见！"

# 成功消息
SUCCESS_MESSAGES = {
    'user_added': "✅ 用户信息录入成功！",
    'user_updated': "✅ 用户信息更新成功！",
    'user_deleted': "✅ 用户删除成功！",
    'data_exported': "✅ 数据导出成功！",
    'data_cleared': "✅ 数据清空成功！"
}

# 错误消息
ERROR_MESSAGES = {
    'invalid_choice': "❌ 无效选择，请重新输入！",
    'invalid_input': "❌ 输入格式错误，请重新输入！",
    'user_not_found': "❌ 未找到指定用户！",
    'name_exists': "❌ 用户名已存在！",
    'no_users': "📭 暂无用户数据",
    'operation_failed': "❌ 操作失败，请重试！",
    'validation_failed': "❌ 数据验证失败！"
}

# 提示消息
INFO_MESSAGES = {
    'enter_name': "请输入姓名: ",
    'enter_age': "请输入年龄: ",
    'enter_height': "请输入身高 (米): ",
    'enter_weight': "请输入体重 (公斤): ",
    'enter_student_status': "是否为学生 (y/n): ",
    'enter_phone': "请输入联系电话: ",
    'enter_email': "请输入邮箱地址: ",
    'press_enter': "\n按回车键继续...",
    'choose_option': "请输入选择: ",
    'search_name': "请输入要搜索的姓名（支持部分匹配）: ",
    'min_age': "请输入最小年龄: ",
    'max_age': "请输入最大年龄: "
}

# ==================== 数值范围常量 ====================

# 年龄范围
AGE_MIN = 1
AGE_MAX = 149

# 身高范围（米）
HEIGHT_MIN = 0.5
HEIGHT_MAX = 3.0

# 体重范围（公斤）
WEIGHT_MIN = 10
WEIGHT_MAX = 500

# 电话号码最小长度
PHONE_MIN_LENGTH = 8
PHONE_MAX_LENGTH = 15

# 姓名最大长度
NAME_MAX_LENGTH = 50

# 邮箱最大长度
EMAIL_MAX_LENGTH = 100

# ==================== BMI分类常量 ====================

BMI_CATEGORIES = {
    "偏瘦": (0, 18.5),
    "正常": (18.5, 24),
    "偏胖": (24, 28),
    "肥胖": (28, 100)
}

# BMI分类描述
BMI_DESCRIPTIONS = {
    "偏瘦": "体重偏轻，建议增加营养摄入",
    "正常": "体重正常，请保持健康的生活方式",
    "偏胖": "体重偏重，建议适当控制饮食和增加运动",
    "肥胖": "体重过重，建议咨询医生制定减重计划"
}

# ==================== 年龄组常量 ====================

AGE_GROUPS = {
    "儿童": (0, 13),
    "青少年": (13, 18),
    "青年": (18, 30),
    "中年": (30, 50),
    "中老年": (50, 65),
    "老年": (65, 150)
}

# 年龄组描述
AGE_GROUP_DESCRIPTIONS = {
    "儿童": "处于成长发育期，需要充足的营养和睡眠",
    "青少年": "身心快速发展期，需要平衡学习和运动",
    "青年": "精力充沛的黄金时期，适合拼搏奋斗",
    "中年": "人生经验丰富期，需要注意健康管理",
    "中老年": "需要更多关注健康，适当调整生活节奏",
    "老年": "享受生活的阶段，重点关注健康和家庭"
}

# ==================== 用户类型常量 ====================

USER_TYPES = {
    True: "学生",
    False: "非学生"
}

USER_TYPE_DESCRIPTIONS = {
    True: "在校学习的学生群体",
    False: "已参加工作或其他非学生群体"
}

# ==================== 格式化常量 ====================

# 分隔符
SEPARATOR_CHAR = "="
SUB_SEPARATOR_CHAR = "-"
SEPARATOR_WIDTH = 60
SUB_SEPARATOR_WIDTH = 40

# 表格格式
TABLE_HEADERS = {
    'user_list': ['序号', '姓名', '年龄', '身高', '体重', 'BMI', '类型'],
    'statistics': ['项目', '数值', '单位', '说明']
}

# 数字格式化精度
FORMAT_PRECISION = {
    'height': 2,  # 身高保留2位小数
    'weight': 1,  # 体重保留1位小数
    'bmi': 1,     # BMI保留1位小数
    'percentage': 1,  # 百分比保留1位小数
    'average': 1  # 平均值保留1位小数
}

# ==================== 图标和符号常量 ====================

ICONS = {
    'user': '👤',
    'name': '📛',
    'age': '🎂',
    'height': '📏',
    'weight': '⚖️',
    'bmi': '📊',
    'student': '🎓',
    'phone': '📞',
    'email': '📧',
    'search': '🔍',
    'statistics': '📈',
    'success': '✅',
    'error': '❌',
    'warning': '⚠️',
    'info': 'ℹ️',
    'question': '❓',
    'list': '📋',
    'export': '📤',
    'import': '📥',
    'delete': '🗑️',
    'edit': '✏️',
    'save': '💾',
    'exit': '👋'
}

# 状态符号
STATUS_SYMBOLS = {
    'active': '🟢',
    'inactive': '🔴',
    'pending': '🟡',
    'unknown': '⚪'
}

# ==================== 验证规则常量 ====================

# 正则表达式模式
REGEX_PATTERNS = {
    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'phone': r'^[\+]?[1-9][\d\s\-\(\)]{7,}\d$',
    'name': r'^[\u4e00-\u9fa5a-zA-Z\s]{1,50}$',  # 中文、英文、空格，1-50字符
    'number': r'^\d+(\.\d+)?$'  # 数字（整数或小数）
}

# 验证错误消息
VALIDATION_ERRORS = {
    'name_empty': "姓名不能为空",
    'name_too_long': f"姓名长度不能超过{NAME_MAX_LENGTH}个字符",
    'age_invalid': f"年龄必须在{AGE_MIN}-{AGE_MAX}之间",
    'height_invalid': f"身高必须在{HEIGHT_MIN}-{HEIGHT_MAX}米之间",
    'weight_invalid': f"体重必须在{WEIGHT_MIN}-{WEIGHT_MAX}公斤之间",
    'phone_invalid': f"电话号码长度必须在{PHONE_MIN_LENGTH}-{PHONE_MAX_LENGTH}位之间",
    'email_invalid': "邮箱地址格式不正确",
    'email_too_long': f"邮箱地址长度不能超过{EMAIL_MAX_LENGTH}个字符"
}

# ==================== 默认值常量 ====================

DEFAULT_VALUES = {
    'name': "",
    'age': 18,
    'height': 1.70,
    'weight': 60.0,
    'is_student': True,
    'phone': "",
    'email': ""
}

# ==================== 系统配置常量 ====================

# 显示配置
DISPLAY_CONFIG = {
    'max_users_per_page': 10,  # 每页显示的最大用户数
    'max_search_results': 20,  # 最大搜索结果数
    'table_width': 80,         # 表格宽度
    'clear_screen': True       # 是否清屏
}

# 数据配置
DATA_CONFIG = {
    'auto_save': False,        # 是否自动保存
    'backup_enabled': False,   # 是否启用备份
    'max_users': 1000,         # 最大用户数
    'export_format': 'txt'     # 导出格式
}

# ==================== 帮助文本常量 ====================

HELP_TEXTS = {
    'main_menu': """
📖 使用说明：
1. 选择菜单项对应的数字
2. 按照提示输入相关信息
3. 输入过程中可以按 Ctrl+C 退出
4. 所有输入都会进行格式验证
""",
    
    'input_format': """
📝 输入格式说明：
• 姓名：中文或英文，不超过50个字符
• 年龄：1-149之间的整数
• 身高：0.5-3.0米之间的小数
• 体重：10-500公斤之间的小数
• 学生状态：y/yes/是 表示学生，n/no/否 表示非学生
• 电话：8-15位数字，可包含+、-、()、空格
• 邮箱：标准邮箱格式，如 user@example.com
""",
    
    'bmi_info': """
📊 BMI指数说明：
• BMI = 体重(kg) / 身高(m)²
• 偏瘦：BMI < 18.5
• 正常：18.5 ≤ BMI < 24
• 偏胖：24 ≤ BMI < 28
• 肥胖：BMI ≥ 28
""",
    
    'search_tips': """
🔍 搜索技巧：
• 姓名搜索支持部分匹配
• 年龄搜索可以指定范围
• 用户类型可以筛选学生/非学生
• 搜索结果按相关度排序
"""
}

# ==================== 示例数据常量 ====================

SAMPLE_USERS = [
    {
        'name': '张三',
        'age': 25,
        'height': 1.75,
        'weight': 70.0,
        'is_student': False,
        'phone': '13800138000',
        'email': 'zhangsan@example.com'
    },
    {
        'name': '李四',
        'age': 20,
        'height': 1.68,
        'weight': 55.5,
        'is_student': True,
        'phone': '13900139000',
        'email': 'lisi@student.edu.cn'
    },
    {
        'name': 'Alice',
        'age': 28,
        'height': 1.65,
        'weight': 58.0,
        'is_student': False,
        'phone': '15800158000',
        'email': 'alice@company.com'
    },
    {
        'name': '王五',
        'age': 22,
        'height': 1.80,
        'weight': 75.0,
        'is_student': True,
        'phone': '18800188000',
        'email': 'wangwu@university.edu.cn'
    }
]

# ==================== 颜色常量（用于终端显示）====================

# ANSI颜色代码
COLORS = {
    'reset': '\033[0m',
    'bold': '\033[1m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m'
}

# 背景颜色
BG_COLORS = {
    'red': '\033[41m',
    'green': '\033[42m',
    'yellow': '\033[43m',
    'blue': '\033[44m',
    'magenta': '\033[45m',
    'cyan': '\033[46m',
    'white': '\033[47m'
}

# ==================== 导出常量 ====================

# 将常用的常量组合导出，方便其他模块使用
__all__ = [
    'APP_NAME', 'APP_VERSION', 'MENU_OPTIONS', 'WELCOME_MESSAGE', 'GOODBYE_MESSAGE',
    'SUCCESS_MESSAGES', 'ERROR_MESSAGES', 'INFO_MESSAGES',
    'AGE_MIN', 'AGE_MAX', 'HEIGHT_MIN', 'HEIGHT_MAX', 'WEIGHT_MIN', 'WEIGHT_MAX',
    'BMI_CATEGORIES', 'AGE_GROUPS', 'USER_TYPES',
    'ICONS', 'SEPARATOR_CHAR', 'SEPARATOR_WIDTH',
    'VALIDATION_ERRORS', 'DEFAULT_VALUES', 'HELP_TEXTS'
]

if __name__ == "__main__":
    # 测试常量定义
    print(f"应用名称: {APP_NAME}")
    print(f"版本: {APP_VERSION}")
    print(f"菜单选项数量: {len(MENU_OPTIONS)}")
    print(f"BMI分类数量: {len(BMI_CATEGORIES)}")
    print(f"年龄组数量: {len(AGE_GROUPS)}")
    print("\n常量定义测试完成！")