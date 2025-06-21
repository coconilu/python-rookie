#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session04 项目配置文件

本文件包含猜数字游戏的所有配置常量和设置。
将配置集中管理有助于代码维护和功能扩展。

作者: Python教程团队
创建日期: 2024-12-21
"""

# ==================== 游戏基础配置 ====================

# 游戏版本信息
GAME_VERSION = "1.0.0"
GAME_NAME = "猜数字游戏"
GAME_AUTHOR = "Python教程团队"

# 数字范围配置
DEFAULT_MIN_NUMBER = 1
DEFAULT_MAX_NUMBER = 100

# ==================== 难度等级配置 ====================

# 难度等级定义
DIFFICULTY_LEVELS = {
    'easy': {
        'name': '简单',
        'min_number': 1,
        'max_number': 50,
        'max_attempts': 10,
        'hint_frequency': 3,  # 每3次猜测给一次额外提示
        'score_multiplier': 1.0
    },
    'normal': {
        'name': '普通',
        'min_number': 1,
        'max_number': 100,
        'max_attempts': 8,
        'hint_frequency': 5,
        'score_multiplier': 1.5
    },
    'hard': {
        'name': '困难',
        'min_number': 1,
        'max_number': 200,
        'max_attempts': 6,
        'hint_frequency': 0,  # 困难模式不提供额外提示
        'score_multiplier': 2.0
    }
}

# 默认难度
DEFAULT_DIFFICULTY = 'normal'

# ==================== 计分系统配置 ====================

# 基础分数
BASE_SCORE = 1000

# 分数计算规则
SCORE_RULES = {
    'perfect_bonus': 500,      # 一次猜中的奖励分数
    'attempt_penalty': 50,     # 每次错误猜测的扣分
    'time_bonus_threshold': 30, # 时间奖励阈值（秒）
    'time_bonus': 200,         # 快速完成的奖励分数
    'hint_penalty': 100        # 使用提示的扣分
}

# 评价等级
PERFORMANCE_RATINGS = {
    'excellent': {'min_score': 900, 'title': '完美', 'emoji': '🏆'},
    'great': {'min_score': 700, 'title': '优秀', 'emoji': '🥇'},
    'good': {'min_score': 500, 'title': '良好', 'emoji': '🥈'},
    'fair': {'min_score': 300, 'title': '一般', 'emoji': '🥉'},
    'poor': {'min_score': 0, 'title': '需要努力', 'emoji': '💪'}
}

# ==================== 用户界面配置 ====================

# 颜色配置（ANSI颜色代码）
COLORS = {
    'reset': '\033[0m',
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'bold': '\033[1m',
    'underline': '\033[4m'
}

# 游戏消息模板
MESSAGES = {
    'welcome': f"""
{COLORS['bold']}{COLORS['cyan']}🎮 欢迎来到{GAME_NAME}！{COLORS['reset']}
{COLORS['yellow']}版本: {GAME_VERSION}{COLORS['reset']}
{COLORS['green']}作者: {GAME_AUTHOR}{COLORS['reset']}
""",
    
    'game_rules': f"""
{COLORS['bold']}📋 游戏规则：{COLORS['reset']}
1. 我会想一个数字，你来猜猜看
2. 我会告诉你猜测的数字是太大还是太小
3. 尽量用最少的次数猜中数字
4. 输入 'quit' 可以退出游戏
5. 输入 'hint' 可以获得提示（会扣分）
""",
    
    'difficulty_prompt': f"""
{COLORS['bold']}🎯 请选择难度等级：{COLORS['reset']}
1. 简单 (1-50, 最多10次机会)
2. 普通 (1-100, 最多8次机会)
3. 困难 (1-200, 最多6次机会)
""",
    
    'input_prompt': f"{COLORS['cyan']}请输入你的猜测: {COLORS['reset']}",
    
    'too_high': f"{COLORS['red']}📈 太大了！{COLORS['reset']}",
    'too_low': f"{COLORS['blue']}📉 太小了！{COLORS['reset']}",
    'correct': f"{COLORS['green']}🎉 恭喜你猜对了！{COLORS['reset']}",
    'game_over': f"{COLORS['red']}💀 游戏结束！{COLORS['reset']}",
    
    'invalid_input': f"{COLORS['yellow']}⚠️  请输入有效的数字！{COLORS['reset']}",
    'out_of_range': f"{COLORS['yellow']}⚠️  数字超出范围！{COLORS['reset']}",
    
    'quit_confirm': f"{COLORS['yellow']}❓ 确定要退出游戏吗？(y/n): {COLORS['reset']}",
    'play_again': f"{COLORS['cyan']}🔄 想再玩一局吗？(y/n): {COLORS['reset']}",
    
    'statistics_header': f"{COLORS['bold']}📊 游戏统计{COLORS['reset']}",
    'best_score': f"{COLORS['green']}🏆 最佳成绩{COLORS['reset']}",
    'total_games': f"{COLORS['blue']}🎮 总游戏数{COLORS['reset']}",
    'win_rate': f"{COLORS['magenta']}📈 胜率{COLORS['reset']}"
}

# ==================== 文件路径配置 ====================

# 数据文件路径
DATA_DIR = "data"
STATISTICS_FILE = f"{DATA_DIR}/statistics.json"
SETTINGS_FILE = f"{DATA_DIR}/settings.json"
HISTORY_FILE = f"{DATA_DIR}/game_history.json"

# ==================== 游戏行为配置 ====================

# 输入验证配置
INPUT_CONFIG = {
    'max_input_length': 10,
    'allowed_commands': ['quit', 'exit', 'hint', 'help', 'stats'],
    'quit_commands': ['quit', 'exit', 'q'],
    'hint_commands': ['hint', 'h'],
    'help_commands': ['help', '?'],
    'stats_commands': ['stats', 'statistics', 's']
}

# 提示系统配置
HINT_CONFIG = {
    'range_hint': True,        # 是否提供范围提示
    'parity_hint': True,       # 是否提供奇偶性提示
    'digit_count_hint': True,  # 是否提供位数提示
    'proximity_hint': True     # 是否提供接近程度提示
}

# 游戏限制配置
GAME_LIMITS = {
    'max_games_per_session': 50,
    'max_attempts_absolute': 20,
    'min_number_range': 10,
    'max_number_range': 1000
}

# ==================== 调试和开发配置 ====================

# 调试模式
DEBUG_MODE = False

# 开发者选项
DEV_OPTIONS = {
    'show_answer': False,      # 是否显示答案（仅调试用）
    'unlimited_attempts': False, # 是否允许无限次尝试
    'skip_animations': False,   # 是否跳过动画效果
    'verbose_logging': False    # 是否启用详细日志
}

# 测试配置
TEST_CONFIG = {
    'auto_play': False,        # 自动游戏模式
    'test_iterations': 100,    # 测试迭代次数
    'performance_test': False  # 性能测试模式
}

# ==================== 帮助信息配置 ====================

HELP_TEXT = f"""
{COLORS['bold']}🆘 游戏帮助{COLORS['reset']}

{COLORS['cyan']}基本命令：{COLORS['reset']}
• 输入数字进行猜测
• 'quit' 或 'q' - 退出游戏
• 'hint' 或 'h' - 获得提示
• 'help' 或 '?' - 显示帮助
• 'stats' 或 's' - 查看统计信息

{COLORS['cyan']}游戏技巧：{COLORS['reset']}
• 使用二分法可以最快找到答案
• 注意观察数字范围的变化
• 合理使用提示功能
• 记录之前的猜测结果

{COLORS['cyan']}计分说明：{COLORS['reset']}
• 基础分数：{BASE_SCORE}分
• 每次错误猜测扣{SCORE_RULES['attempt_penalty']}分
• 使用提示扣{SCORE_RULES['hint_penalty']}分
• 一次猜中奖励{SCORE_RULES['perfect_bonus']}分
• 快速完成有时间奖励
"""

# ==================== 默认设置 ====================

DEFAULT_SETTINGS = {
    'difficulty': DEFAULT_DIFFICULTY,
    'sound_enabled': True,
    'color_enabled': True,
    'auto_save': True,
    'show_statistics': True,
    'animation_speed': 'normal',
    'language': 'zh_CN'
}

# ==================== 动画配置 ====================

ANIMATION_CONFIG = {
    'typing_delay': 0.03,      # 打字机效果延迟（秒）
    'loading_chars': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
    'progress_chars': ['▱', '▰'],
    'celebration_chars': ['🎉', '🎊', '✨', '🌟', '⭐']
}

# ==================== 错误消息配置 ====================

ERROR_MESSAGES = {
    'file_not_found': "数据文件未找到，将创建新文件",
    'invalid_json': "数据文件格式错误，将重置数据",
    'permission_denied': "没有文件访问权限",
    'disk_full': "磁盘空间不足",
    'network_error': "网络连接错误",
    'unknown_error': "发生未知错误"
}

# ==================== 成就系统配置 ====================

ACHIEVEMENTS = {
    'first_win': {
        'name': '初出茅庐',
        'description': '完成第一局游戏',
        'emoji': '🌱',
        'points': 50
    },
    'perfect_game': {
        'name': '一击必中',
        'description': '一次猜中答案',
        'emoji': '🎯',
        'points': 200
    },
    'speed_demon': {
        'name': '闪电侠',
        'description': '30秒内完成游戏',
        'emoji': '⚡',
        'points': 150
    },
    'persistent': {
        'name': '坚持不懈',
        'description': '连续玩10局游戏',
        'emoji': '💪',
        'points': 100
    },
    'master': {
        'name': '猜数大师',
        'description': '胜率达到80%',
        'emoji': '👑',
        'points': 300
    }
}