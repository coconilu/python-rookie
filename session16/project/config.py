#!/usr/bin/env python3
"""
计算器配置文件
包含所有配置常量
"""

# 窗口配置
APP_TITLE = "桌面计算器"
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
MIN_WIDTH = 300
MIN_HEIGHT = 400

# 字体配置
FONT_FAMILY = "Arial"
DISPLAY_FONT_SIZE = 24
BUTTON_FONT_SIZE = 18

# 颜色配置 - 默认主题
BG_COLOR = "#f0f0f0"
DISPLAY_BG = "#ffffff"
DISPLAY_FG = "#000000"

# 按钮颜色
BUTTON_NUMBER_BG = "#ffffff"
BUTTON_NUMBER_FG = "#000000"
BUTTON_NUMBER_ACTIVE = "#e0e0e0"

BUTTON_OPERATOR_BG = "#ff9500"
BUTTON_OPERATOR_FG = "#ffffff"
BUTTON_OPERATOR_ACTIVE = "#ffb143"

BUTTON_EQUALS_BG = "#4CAF50"
BUTTON_EQUALS_FG = "#ffffff"
BUTTON_EQUALS_ACTIVE = "#66BB6A"

BUTTON_CLEAR_BG = "#f44336"
BUTTON_CLEAR_FG = "#ffffff"
BUTTON_CLEAR_ACTIVE = "#e57373"

BUTTON_FUNCTION_BG = "#e0e0e0"
BUTTON_FUNCTION_FG = "#000000"
BUTTON_FUNCTION_ACTIVE = "#d0d0d0"

# 其他配置
MAX_HISTORY = 50  # 最大历史记录数

# 主题配置（可扩展）
THEMES = {
    "default": {
        "bg_color": "#f0f0f0",
        "display_bg": "#ffffff",
        "display_fg": "#000000",
        "button_number_bg": "#ffffff",
        "button_number_fg": "#000000",
        "button_operator_bg": "#ff9500",
        "button_operator_fg": "#ffffff",
        "button_equals_bg": "#4CAF50",
        "button_equals_fg": "#ffffff",
    },
    "dark": {
        "bg_color": "#1e1e1e",
        "display_bg": "#2d2d2d",
        "display_fg": "#ffffff",
        "button_number_bg": "#3c3c3c",
        "button_number_fg": "#ffffff",
        "button_operator_bg": "#ff9500",
        "button_operator_fg": "#ffffff",
        "button_equals_bg": "#4CAF50",
        "button_equals_fg": "#ffffff",
    },
    "blue": {
        "bg_color": "#e3f2fd",
        "display_bg": "#ffffff",
        "display_fg": "#0d47a1",
        "button_number_bg": "#bbdefb",
        "button_number_fg": "#0d47a1",
        "button_operator_bg": "#1976d2",
        "button_operator_fg": "#ffffff",
        "button_equals_bg": "#2196f3",
        "button_equals_fg": "#ffffff",
    }
} 