#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块

提供各种实用的辅助函数，展示了函数的定义和使用，
以及如何处理不同类型的数据转换和验证。

作者: Python教程团队
创建日期: 2024-12-19
"""

import os
import sys
from typing import Any, Callable, Union


def calculate_bmi(weight: float, height: float) -> float:
    """
    计算BMI指数
    
    BMI = 体重(kg) / 身高(m)²
    
    Args:
        weight (float): 体重，单位：公斤
        height (float): 身高，单位：米
        
    Returns:
        float: BMI指数
        
    Raises:
        ValueError: 当身高或体重无效时
    """
    if height <= 0:
        raise ValueError("身高必须大于0")
    if weight <= 0:
        raise ValueError("体重必须大于0")
    
    bmi = weight / (height ** 2)
    return round(bmi, 1)


def get_age_group(age: int) -> str:
    """
    根据年龄获取年龄组
    
    Args:
        age (int): 年龄
        
    Returns:
        str: 年龄组名称
    """
    if age < 0:
        return "无效年龄"
    elif age < 13:
        return "儿童"
    elif age < 18:
        return "青少年"
    elif age < 30:
        return "青年"
    elif age < 50:
        return "中年"
    elif age < 65:
        return "中老年"
    else:
        return "老年"


def get_valid_input(
    prompt: str, 
    data_type: type, 
    validator: Callable[[Any], bool] = None,
    error_message: str = "输入无效，请重新输入"
) -> Any:
    """
    获取有效的用户输入
    
    这个函数展示了如何结合类型转换、数据验证和错误处理。
    
    Args:
        prompt (str): 输入提示信息
        data_type (type): 期望的数据类型
        validator (Callable[[Any], bool], optional): 验证函数
        error_message (str): 错误提示信息
        
    Returns:
        Any: 转换后的有效输入
    """
    while True:
        try:
            # 获取用户输入
            user_input = input(prompt).strip()
            
            # 类型转换
            if data_type == str:
                converted_value = user_input
            elif data_type == int:
                converted_value = int(user_input)
            elif data_type == float:
                converted_value = float(user_input)
            elif data_type == bool:
                # 布尔值的特殊处理
                converted_value = user_input.lower() in ['true', '1', 'yes', 'y', '是']
            else:
                # 尝试直接转换
                converted_value = data_type(user_input)
            
            # 数据验证
            if validator is None or validator(converted_value):
                return converted_value
            else:
                print(f"❌ {error_message}")
                
        except ValueError as e:
            print(f"❌ 输入格式错误: {e}")
        except KeyboardInterrupt:
            print("\n👋 输入被取消")
            sys.exit(0)
        except Exception as e:
            print(f"❌ 未知错误: {e}")


def format_user_info(user_info: dict) -> str:
    """
    格式化用户信息为字符串
    
    Args:
        user_info (dict): 用户信息字典
        
    Returns:
        str: 格式化后的用户信息
    """
    lines = []
    lines.append("=" * 40)
    lines.append(f"👤 {user_info['name']} 的详细信息")
    lines.append("=" * 40)
    
    # 基本信息
    lines.append(f"🎂 年龄: {user_info['age']}岁 ({get_age_group(user_info['age'])})")
    lines.append(f"📏 身高: {user_info['height']:.2f}米")
    lines.append(f"⚖️  体重: {user_info['weight']:.1f}公斤")
    
    # 计算BMI
    bmi = calculate_bmi(user_info['weight'], user_info['height'])
    bmi_category = get_bmi_category(bmi)
    lines.append(f"📊 BMI: {bmi:.1f} ({bmi_category})")
    
    # 其他信息
    user_type = "学生" if user_info['is_student'] else "非学生"
    lines.append(f"🎓 类型: {user_type}")
    lines.append(f"📞 电话: {user_info['phone']}")
    lines.append(f"📧 邮箱: {user_info['email']}")
    
    lines.append("=" * 40)
    
    return "\n".join(lines)


def get_bmi_category(bmi: float) -> str:
    """
    根据BMI值获取分类
    
    Args:
        bmi (float): BMI值
        
    Returns:
        str: BMI分类
    """
    if bmi < 18.5:
        return "偏瘦"
    elif bmi < 24:
        return "正常"
    elif bmi < 28:
        return "偏胖"
    else:
        return "肥胖"


def validate_email(email: str) -> bool:
    """
    简单的邮箱验证
    
    Args:
        email (str): 邮箱地址
        
    Returns:
        bool: 是否为有效邮箱
    """
    if not isinstance(email, str):
        return False
    
    email = email.strip()
    
    # 基本格式检查
    if '@' not in email:
        return False
    
    parts = email.split('@')
    if len(parts) != 2:
        return False
    
    local, domain = parts
    
    # 检查本地部分
    if len(local) == 0 or len(local) > 64:
        return False
    
    # 检查域名部分
    if len(domain) == 0 or '.' not in domain:
        return False
    
    domain_parts = domain.split('.')
    if len(domain_parts) < 2:
        return False
    
    # 检查域名后缀
    if len(domain_parts[-1]) < 2:
        return False
    
    return True


def validate_phone(phone: str) -> bool:
    """
    简单的电话号码验证
    
    Args:
        phone (str): 电话号码
        
    Returns:
        bool: 是否为有效电话号码
    """
    if not isinstance(phone, str):
        return False
    
    # 去除空格和常见分隔符
    cleaned_phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
    
    # 检查长度
    if len(cleaned_phone) < 8 or len(cleaned_phone) > 15:
        return False
    
    # 检查是否只包含数字和+号
    if not all(c.isdigit() or c == '+' for c in cleaned_phone):
        return False
    
    # +号只能在开头
    if '+' in cleaned_phone and not cleaned_phone.startswith('+'):
        return False
    
    return True


def clear_screen():
    """
    清屏函数
    
    根据操作系统选择合适的清屏命令
    """
    try:
        # Windows
        if os.name == 'nt':
            os.system('cls')
        # Unix/Linux/MacOS
        else:
            os.system('clear')
    except Exception:
        # 如果清屏失败，打印空行
        print('\n' * 50)


def print_header(title: str, width: int = 60):
    """
    打印标题头部
    
    Args:
        title (str): 标题文本
        width (int): 总宽度
    """
    print("=" * width)
    # 计算居中位置
    padding = (width - len(title) - 2) // 2
    print(f"{'=' * padding} {title} {'=' * padding}")
    print("=" * width)


def print_separator(char: str = "-", width: int = 60):
    """
    打印分隔线
    
    Args:
        char (str): 分隔符字符
        width (int): 分隔线宽度
    """
    print(char * width)


def format_number(number: Union[int, float], decimal_places: int = 1) -> str:
    """
    格式化数字显示
    
    Args:
        number (Union[int, float]): 要格式化的数字
        decimal_places (int): 小数位数
        
    Returns:
        str: 格式化后的数字字符串
    """
    if isinstance(number, int):
        return str(number)
    else:
        return f"{number:.{decimal_places}f}"


def safe_divide(dividend: float, divisor: float, default: float = 0.0) -> float:
    """
    安全除法，避免除零错误
    
    Args:
        dividend (float): 被除数
        divisor (float): 除数
        default (float): 除零时的默认值
        
    Returns:
        float: 除法结果
    """
    try:
        if divisor == 0:
            return default
        return dividend / divisor
    except (TypeError, ValueError):
        return default


def convert_to_type(value: str, target_type: type, default: Any = None) -> Any:
    """
    安全的类型转换
    
    Args:
        value (str): 要转换的字符串值
        target_type (type): 目标类型
        default (Any): 转换失败时的默认值
        
    Returns:
        Any: 转换后的值
    """
    try:
        if target_type == bool:
            # 布尔值的特殊处理
            return value.lower() in ['true', '1', 'yes', 'y', '是', 'on']
        else:
            return target_type(value)
    except (ValueError, TypeError):
        return default


def get_percentage(part: Union[int, float], total: Union[int, float]) -> float:
    """
    计算百分比
    
    Args:
        part (Union[int, float]): 部分值
        total (Union[int, float]): 总值
        
    Returns:
        float: 百分比（0-100）
    """
    if total == 0:
        return 0.0
    return (part / total) * 100


def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """
    截断字符串
    
    Args:
        text (str): 原始字符串
        max_length (int): 最大长度
        suffix (str): 截断后缀
        
    Returns:
        str: 截断后的字符串
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小显示
    
    Args:
        size_bytes (int): 字节数
        
    Returns:
        str: 格式化后的大小字符串
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size = float(size_bytes)
    
    while size >= 1024.0 and i < len(size_names) - 1:
        size /= 1024.0
        i += 1
    
    return f"{size:.1f} {size_names[i]}"


def create_progress_bar(current: int, total: int, width: int = 50) -> str:
    """
    创建进度条
    
    Args:
        current (int): 当前进度
        total (int): 总进度
        width (int): 进度条宽度
        
    Returns:
        str: 进度条字符串
    """
    if total == 0:
        return "[" + " " * width + "] 0%"
    
    percentage = min(100, (current / total) * 100)
    filled_width = int((current / total) * width)
    
    bar = "█" * filled_width + "░" * (width - filled_width)
    return f"[{bar}] {percentage:.1f}%"


def get_user_confirmation(message: str, default: bool = False) -> bool:
    """
    获取用户确认
    
    Args:
        message (str): 确认消息
        default (bool): 默认值
        
    Returns:
        bool: 用户确认结果
    """
    default_text = "[Y/n]" if default else "[y/N]"
    
    while True:
        try:
            response = input(f"{message} {default_text}: ").strip().lower()
            
            if not response:
                return default
            
            if response in ['y', 'yes', '是', '1', 'true']:
                return True
            elif response in ['n', 'no', '否', '0', 'false']:
                return False
            else:
                print("请输入 y/yes 或 n/no")
                
        except KeyboardInterrupt:
            print("\n操作被取消")
            return False


def format_duration(seconds: float) -> str:
    """
    格式化时间长度
    
    Args:
        seconds (float): 秒数
        
    Returns:
        str: 格式化后的时间字符串
    """
    if seconds < 60:
        return f"{seconds:.1f}秒"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}分钟"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}小时"


# 数据验证函数集合
class Validators:
    """
    数据验证器类
    
    包含各种常用的数据验证方法
    """
    
    @staticmethod
    def is_positive_number(value: Union[int, float]) -> bool:
        """检查是否为正数"""
        return isinstance(value, (int, float)) and value > 0
    
    @staticmethod
    def is_in_range(value: Union[int, float], min_val: float, max_val: float) -> bool:
        """检查是否在指定范围内"""
        return isinstance(value, (int, float)) and min_val <= value <= max_val
    
    @staticmethod
    def is_non_empty_string(value: str) -> bool:
        """检查是否为非空字符串"""
        return isinstance(value, str) and len(value.strip()) > 0
    
    @staticmethod
    def is_valid_age(age: int) -> bool:
        """检查是否为有效年龄"""
        return isinstance(age, int) and 0 < age < 150
    
    @staticmethod
    def is_valid_height(height: float) -> bool:
        """检查是否为有效身高（米）"""
        return isinstance(height, (int, float)) and 0.5 < height < 3.0
    
    @staticmethod
    def is_valid_weight(weight: float) -> bool:
        """检查是否为有效体重（公斤）"""
        return isinstance(weight, (int, float)) and 10 < weight < 500


if __name__ == "__main__":
    # 测试一些工具函数
    print("=== 工具函数测试 ===")
    
    # 测试BMI计算
    print(f"BMI计算测试: {calculate_bmi(70, 1.75)}")
    
    # 测试年龄组
    print(f"年龄组测试: {get_age_group(25)}")
    
    # 测试邮箱验证
    print(f"邮箱验证测试: {validate_email('test@example.com')}")
    
    # 测试电话验证
    print(f"电话验证测试: {validate_phone('13800138000')}")
    
    # 测试百分比计算
    print(f"百分比计算测试: {get_percentage(25, 100)}%")
    
    print("\n所有测试完成！")