#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session23 示例2：代码格式化示例

本文件展示了代码格式化工具（如black、ruff format）的使用，
以及格式化前后的代码对比。

作者: Python教程团队
创建日期: 2024-01-01
"""

import json
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Union


class CodeFormatter:
    """
    代码格式化演示类
    
    展示各种代码格式化的最佳实践，包括：
    - 函数参数格式化
    - 长表达式的换行
    - 数据结构的格式化
    - 字符串格式化
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化代码格式化器
        
        Args:
            config: 配置字典，包含格式化选项
        """
        self.config = config or {
            'line_length': 88,
            'indent_size': 4,
            'use_trailing_commas': True
        }
    
    def format_function_calls(self) -> None:
        """
        演示函数调用的格式化
        """
        print("函数调用格式化演示")
        print("-" * 30)
        
        # 短参数列表 - 单行
        result1 = self._simple_function("arg1", "arg2", option=True)
        
        # 长参数列表 - 多行格式化
        result2 = self._complex_function(
            first_argument="这是一个很长的参数值",
            second_argument="另一个很长的参数值",
            third_argument={
                "nested_key1": "nested_value1",
                "nested_key2": "nested_value2",
                "nested_key3": "nested_value3"
            },
            fourth_argument=[
                "list_item1",
                "list_item2",
                "list_item3"
            ],
            enable_feature=True,
            timeout=30,
            retry_count=3
        )
        
        print(f"简单函数结果: {result1}")
        print(f"复杂函数结果: {result2}")
    
    def format_data_structures(self) -> None:
        """
        演示数据结构的格式化
        """
        print("\n数据结构格式化演示")
        print("-" * 30)
        
        # 字典格式化
        user_data = {
            "id": 1,
            "name": "张三",
            "email": "zhangsan@example.com",
            "profile": {
                "age": 25,
                "city": "北京",
                "interests": ["编程", "阅读", "旅行"],
                "skills": {
                    "python": "高级",
                    "javascript": "中级",
                    "sql": "中级"
                }
            },
            "settings": {
                "notifications": True,
                "privacy": "public",
                "theme": "dark"
            }
        }
        
        # 列表格式化
        programming_languages = [
            "Python",
            "JavaScript",
            "Java",
            "C++",
            "Go",
            "Rust",
            "TypeScript"
        ]
        
        # 元组格式化
        coordinates = (
            (0, 0),
            (10, 20),
            (30, 40),
            (50, 60)
        )
        
        print(f"用户数据: {json.dumps(user_data, ensure_ascii=False, indent=2)}")
        print(f"编程语言: {programming_languages}")
        print(f"坐标点: {coordinates}")
    
    def format_long_expressions(self) -> None:
        """
        演示长表达式的格式化
        """
        print("\n长表达式格式化演示")
        print("-" * 30)
        
        # 长条件表达式
        user_age = 25
        user_score = 85
        user_active = True
        user_premium = False
        
        is_eligible = (
            user_age >= 18
            and user_score >= 80
            and user_active
            and (user_premium or user_score >= 90)
        )
        
        # 长字符串拼接
        welcome_message = (
            "欢迎来到我们的平台！"
            "您可以在这里学习Python编程，"
            "参与项目开发，与其他开发者交流。"
            "我们提供丰富的学习资源和实践机会。"
        )
        
        # 长列表推导式
        filtered_numbers = [
            num * 2
            for num in range(100)
            if num % 3 == 0
            and num % 5 != 0
            and num > 10
        ]
        
        print(f"用户是否符合条件: {is_eligible}")
        print(f"欢迎消息: {welcome_message}")
        print(f"过滤后的数字 (前10个): {filtered_numbers[:10]}")
    
    def format_string_operations(self) -> None:
        """
        演示字符串格式化的最佳实践
        """
        print("\n字符串格式化演示")
        print("-" * 30)
        
        name = "Alice"
        age = 30
        score = 95.5
        timestamp = datetime.now()
        
        # f-string格式化（推荐）
        message1 = f"用户 {name} 今年 {age} 岁，得分为 {score:.1f}"
        
        # 多行f-string
        detailed_message = (
            f"用户信息:\n"
            f"  姓名: {name}\n"
            f"  年龄: {age}\n"
            f"  得分: {score:.2f}\n"
            f"  时间: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        # 字典格式化
        template = "姓名: {name}, 年龄: {age}, 得分: {score:.1f}"
        message2 = template.format(name=name, age=age, score=score)
        
        print(f"简单消息: {message1}")
        print(f"详细消息:\n{detailed_message}")
        print(f"模板消息: {message2}")
    
    def format_class_definitions(self) -> None:
        """
        演示类定义的格式化
        """
        print("\n类定义格式化演示")
        print("-" * 30)
        
        # 这个方法本身就是格式化的示例
        print("请查看本文件中的类定义，它们都遵循了格式化规范:")
        print("1. 类名使用PascalCase")
        print("2. 方法之间有适当的空行")
        print("3. 参数列表格式化合理")
        print("4. 文档字符串格式规范")
    
    def _simple_function(self, arg1: str, arg2: str, option: bool = False) -> str:
        """
        简单函数示例
        
        Args:
            arg1: 第一个参数
            arg2: 第二个参数
            option: 选项参数
        
        Returns:
            处理结果
        """
        return f"{arg1}-{arg2}" if option else f"{arg1}_{arg2}"
    
    def _complex_function(
        self,
        first_argument: str,
        second_argument: str,
        third_argument: Dict[str, str],
        fourth_argument: List[str],
        enable_feature: bool = True,
        timeout: int = 30,
        retry_count: int = 3
    ) -> Dict[str, Any]:
        """
        复杂函数示例，展示长参数列表的格式化
        
        Args:
            first_argument: 第一个参数
            second_argument: 第二个参数
            third_argument: 嵌套字典参数
            fourth_argument: 列表参数
            enable_feature: 是否启用功能
            timeout: 超时时间
            retry_count: 重试次数
        
        Returns:
            处理结果字典
        """
        return {
            "processed": True,
            "arguments_count": 4,
            "feature_enabled": enable_feature,
            "config": {
                "timeout": timeout,
                "retry_count": retry_count
            },
            "data_summary": {
                "dict_keys": len(third_argument),
                "list_items": len(fourth_argument)
            }
        }


def demonstrate_before_after_formatting():
    """
    演示格式化前后的代码对比
    """
    print("格式化前后对比演示")
    print("=" * 40)
    
    print("\n格式化前的代码（不推荐）:")
    print('def bad_function(x,y,z=None):')
    print('    if x>0 and y>0:')
    print('        result=x+y')
    print('        if z is not None:result+=z')
    print('        return result')
    print('    else:return 0')
    
    print("\n格式化后的代码（推荐）:")
    print('def good_function(x: int, y: int, z: Optional[int] = None) -> int:')
    print('    """计算数值的和"""')
    print('    if x > 0 and y > 0:')
    print('        result = x + y')
    print('        if z is not None:')
    print('            result += z')
    print('        return result')
    print('    else:')
    print('        return 0')
    
    # 实际的格式化函数
    def good_function(x: int, y: int, z: Optional[int] = None) -> int:
        """计算数值的和"""
        if x > 0 and y > 0:
            result = x + y
            if z is not None:
                result += z
            return result
        else:
            return 0
    
    # 测试函数
    test_result = good_function(10, 20, 5)
    print(f"\n函数测试结果: {test_result}")


def demonstrate_formatting_tools():
    """
    演示代码格式化工具的使用
    """
    print("\n代码格式化工具演示")
    print("=" * 40)
    
    print("常用的Python代码格式化工具:")
    print("\n1. Black - 无妥协的代码格式化器")
    print("   安装: pip install black")
    print("   使用: black filename.py")
    print("   特点: 自动格式化，减少代码风格争议")
    
    print("\n2. Ruff Format - 极快的格式化器")
    print("   安装: pip install ruff")
    print("   使用: ruff format filename.py")
    print("   特点: 速度极快，兼容Black")
    
    print("\n3. autopep8 - PEP 8自动格式化")
    print("   安装: pip install autopep8")
    print("   使用: autopep8 --in-place filename.py")
    print("   特点: 专注于PEP 8规范")
    
    print("\n4. YAPF - Google的格式化工具")
    print("   安装: pip install yapf")
    print("   使用: yapf --in-place filename.py")
    print("   特点: 高度可配置")
    
    print("\n推荐配置 (pyproject.toml):")
    print("[tool.black]")
    print("line-length = 88")
    print("target-version = ['py38']")
    print("include = '\\.pyi?$'")
    
    print("\n[tool.ruff.format]")
    print("quote-style = 'double'")
    print("indent-style = 'space'")
    print("line-ending = 'auto'")


def main():
    """
    主函数：演示代码格式化的各种场景
    """
    print("Session23 示例2：代码格式化演示")
    print("=" * 50)
    
    try:
        # 创建格式化器
        formatter = CodeFormatter()
        
        # 演示各种格式化场景
        formatter.format_function_calls()
        formatter.format_data_structures()
        formatter.format_long_expressions()
        formatter.format_string_operations()
        formatter.format_class_definitions()
        
        # 演示格式化前后对比
        demonstrate_before_after_formatting()
        
        # 演示格式化工具
        demonstrate_formatting_tools()
        
        print("\n=" * 50)
        print("代码格式化要点总结:")
        print("1. 使用自动化工具保持一致的代码风格")
        print("2. 长参数列表应该换行并对齐")
        print("3. 复杂数据结构应该使用多行格式")
        print("4. 长表达式应该合理换行")
        print("5. 字符串格式化优先使用f-string")
        print("6. 配置编辑器自动格式化")
        print("7. 在CI/CD中集成格式化检查")
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()