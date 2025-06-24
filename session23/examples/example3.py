#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session23 示例3：静态分析示例

本文件展示了静态分析工具的使用，包括类型检查、
代码复杂度分析、安全漏洞检测等。

作者: Python教程团队
创建日期: 2024-01-01
"""

import hashlib
import os
import sqlite3
import subprocess
from typing import Any, Dict, List, Optional, Tuple, Union


class StaticAnalysisDemo:
    """
    静态分析演示类
    
    展示各种静态分析工具能够检测的问题类型，
    包括类型错误、安全问题、代码质量问题等。
    """
    
    def __init__(self, database_path: str) -> None:
        """
        初始化静态分析演示
        
        Args:
            database_path: 数据库文件路径
        """
        self.database_path: str = database_path
        self.connection: Optional[sqlite3.Connection] = None
    
    def demonstrate_type_annotations(self) -> None:
        """
        演示类型注解的正确使用
        
        类型注解帮助静态分析工具（如mypy）检测类型错误
        """
        print("类型注解演示")
        print("-" * 20)
        
        # 正确的类型注解
        def calculate_average(numbers: List[float]) -> float:
            """计算平均值"""
            if not numbers:
                return 0.0
            return sum(numbers) / len(numbers)
        
        def process_user_data(
            user_id: int,
            user_info: Dict[str, Union[str, int]],
            is_active: bool = True
        ) -> Optional[Dict[str, Any]]:
            """处理用户数据"""
            if not is_active:
                return None
            
            return {
                "id": user_id,
                "name": user_info.get("name", "Unknown"),
                "age": user_info.get("age", 0),
                "processed_at": "2024-01-01"
            }
        
        # 测试函数
        test_numbers: List[float] = [1.0, 2.0, 3.0, 4.0, 5.0]
        average: float = calculate_average(test_numbers)
        
        test_user: Dict[str, Union[str, int]] = {
            "name": "Alice",
            "age": 25
        }
        result: Optional[Dict[str, Any]] = process_user_data(1, test_user)
        
        print(f"平均值: {average}")
        print(f"处理结果: {result}")
    
    def demonstrate_security_issues(self) -> None:
        """
        演示常见的安全问题（仅作教学用途）
        
        这些是bandit等安全检查工具会检测的问题
        """
        print("\n安全问题演示")
        print("-" * 20)
        
        # 安全问题1：硬编码密码（不推荐）
        # password = "hardcoded_password_123"  # bandit会检测到这个问题
        
        # 正确做法：从环境变量获取
        password: Optional[str] = os.getenv("DATABASE_PASSWORD")
        if not password:
            print("警告: 未设置数据库密码环境变量")
            password = "default_password"  # 仅用于演示
        
        # 安全问题2：SQL注入风险（不推荐）
        def unsafe_query(user_input: str) -> str:
            """不安全的查询方法（仅作演示）"""
            # 这种方式容易受到SQL注入攻击
            query = f"SELECT * FROM users WHERE name = '{user_input}'"
            return query
        
        # 正确做法：使用参数化查询
        def safe_query(user_input: str) -> Tuple[str, Tuple[str]]:
            """安全的查询方法"""
            query = "SELECT * FROM users WHERE name = ?"
            params = (user_input,)
            return query, params
        
        # 演示
        test_input = "Alice"
        unsafe_sql = unsafe_query(test_input)
        safe_sql, safe_params = safe_query(test_input)
        
        print(f"不安全的查询: {unsafe_sql}")
        print(f"安全的查询: {safe_sql}, 参数: {safe_params}")
        
        # 安全问题3：使用不安全的随机数生成器
        import random
        import secrets
        
        # 不推荐：用于安全目的
        weak_token = str(random.randint(1000, 9999))
        
        # 推荐：用于安全目的
        secure_token = secrets.token_hex(16)
        
        print(f"弱随机令牌: {weak_token}")
        print(f"安全随机令牌: {secure_token}")
    
    def demonstrate_code_complexity(self) -> None:
        """
        演示代码复杂度问题
        
        高复杂度的代码难以维护和测试
        """
        print("\n代码复杂度演示")
        print("-" * 20)
        
        # 高复杂度函数（不推荐）
        def complex_function(x: int, y: int, z: int, mode: str) -> int:
            """复杂度过高的函数示例"""
            if mode == "add":
                if x > 0:
                    if y > 0:
                        if z > 0:
                            return x + y + z
                        else:
                            return x + y - abs(z)
                    else:
                        if z > 0:
                            return x - abs(y) + z
                        else:
                            return x - abs(y) - abs(z)
                else:
                    if y > 0:
                        if z > 0:
                            return abs(x) + y + z
                        else:
                            return abs(x) + y - abs(z)
                    else:
                        return abs(x) - abs(y) - abs(z)
            elif mode == "multiply":
                if x != 0 and y != 0 and z != 0:
                    return x * y * z
                else:
                    return 0
            else:
                return 0
        
        # 重构后的低复杂度函数（推荐）
        def simple_add_function(x: int, y: int, z: int) -> int:
            """简化的加法函数"""
            return abs(x) + abs(y) + abs(z) if x >= 0 else -(abs(x) + abs(y) + abs(z))
        
        def simple_multiply_function(x: int, y: int, z: int) -> int:
            """简化的乘法函数"""
            return x * y * z if all([x, y, z]) else 0
        
        def calculate(x: int, y: int, z: int, mode: str) -> int:
            """重构后的计算函数"""
            operations = {
                "add": simple_add_function,
                "multiply": simple_multiply_function
            }
            
            operation = operations.get(mode)
            if operation:
                return operation(x, y, z)
            else:
                raise ValueError(f"不支持的操作模式: {mode}")
        
        # 测试函数
        test_x, test_y, test_z = 2, 3, 4
        
        complex_result = complex_function(test_x, test_y, test_z, "add")
        simple_result = calculate(test_x, test_y, test_z, "add")
        
        print(f"复杂函数结果: {complex_result}")
        print(f"简化函数结果: {simple_result}")
    
    def demonstrate_common_issues(self) -> None:
        """
        演示静态分析工具能检测的常见问题
        """
        print("\n常见问题演示")
        print("-" * 20)
        
        # 问题1：未使用的变量
        def function_with_unused_variable() -> str:
            """包含未使用变量的函数"""
            used_variable = "这个变量被使用了"
            # unused_variable = "这个变量没有被使用"  # 静态分析会检测到
            return used_variable
        
        # 问题2：可能的None值访问
        def risky_none_access(data: Optional[Dict[str, str]]) -> str:
            """可能访问None值的函数"""
            if data is not None:
                return data.get("key", "default")
            else:
                return "no data"
        
        # 问题3：过长的函数
        def overly_long_function() -> Dict[str, Any]:
            """过长的函数示例（应该拆分）"""
            # 这个函数做了太多事情，应该拆分成多个小函数
            result = {}
            
            # 数据验证
            result["validation"] = "passed"
            
            # 数据处理
            result["processing"] = "completed"
            
            # 数据存储
            result["storage"] = "saved"
            
            # 通知发送
            result["notification"] = "sent"
            
            return result
        
        # 重构后的版本
        def validate_data() -> str:
            """数据验证"""
            return "passed"
        
        def process_data() -> str:
            """数据处理"""
            return "completed"
        
        def store_data() -> str:
            """数据存储"""
            return "saved"
        
        def send_notification() -> str:
            """发送通知"""
            return "sent"
        
        def well_structured_function() -> Dict[str, Any]:
            """结构良好的函数"""
            return {
                "validation": validate_data(),
                "processing": process_data(),
                "storage": store_data(),
                "notification": send_notification()
            }
        
        # 测试函数
        result1 = function_with_unused_variable()
        result2 = risky_none_access({"key": "value"})
        result3 = well_structured_function()
        
        print(f"函数1结果: {result1}")
        print(f"函数2结果: {result2}")
        print(f"函数3结果: {result3}")
    
    def demonstrate_static_analysis_tools(self) -> None:
        """
        演示静态分析工具的使用
        """
        print("\n静态分析工具演示")
        print("-" * 20)
        
        tools_info = {
            "mypy": {
                "purpose": "静态类型检查",
                "install": "pip install mypy",
                "usage": "mypy filename.py",
                "config": "mypy.ini 或 pyproject.toml"
            },
            "bandit": {
                "purpose": "安全漏洞检测",
                "install": "pip install bandit",
                "usage": "bandit -r .",
                "config": ".bandit 或 pyproject.toml"
            },
            "pylint": {
                "purpose": "代码质量检查",
                "install": "pip install pylint",
                "usage": "pylint filename.py",
                "config": ".pylintrc"
            },
            "ruff": {
                "purpose": "快速代码检查",
                "install": "pip install ruff",
                "usage": "ruff check .",
                "config": "pyproject.toml"
            }
        }
        
        for tool, info in tools_info.items():
            print(f"\n{tool.upper()}:")
            print(f"  用途: {info['purpose']}")
            print(f"  安装: {info['install']}")
            print(f"  使用: {info['usage']}")
            print(f"  配置: {info['config']}")
    
    def create_sample_config_files(self) -> None:
        """
        创建示例配置文件
        """
        print("\n配置文件示例")
        print("-" * 20)
        
        # mypy配置示例
        mypy_config = """
[mypy]
python_version = 3.8
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
show_error_codes = True

[mypy-requests.*]
ignore_missing_imports = True

[mypy-pandas.*]
ignore_missing_imports = True
        """
        
        # ruff配置示例
        ruff_config = """
[tool.ruff]
line-length = 88
target-version = "py38"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "C4", "S"]
ignore = ["E203", "E501"]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]
"tests/*" = ["S101"]
        """
        
        print("mypy.ini 配置示例:")
        print(mypy_config)
        
        print("\npyproject.toml 中的 ruff 配置示例:")
        print(ruff_config)


def main() -> None:
    """
    主函数：演示静态分析的各种场景
    """
    print("Session23 示例3：静态分析演示")
    print("=" * 50)
    
    try:
        # 创建演示实例
        demo = StaticAnalysisDemo("demo.db")
        
        # 演示各种静态分析场景
        demo.demonstrate_type_annotations()
        demo.demonstrate_security_issues()
        demo.demonstrate_code_complexity()
        demo.demonstrate_common_issues()
        demo.demonstrate_static_analysis_tools()
        demo.create_sample_config_files()
        
        print("\n=" * 50)
        print("静态分析要点总结:")
        print("1. 使用类型注解提高代码可读性和可维护性")
        print("2. 定期运行安全检查工具检测潜在漏洞")
        print("3. 控制函数和类的复杂度")
        print("4. 配置静态分析工具适应项目需求")
        print("5. 在CI/CD中集成静态分析")
        print("6. 逐步改善现有代码的质量")
        print("7. 团队统一使用相同的分析工具和配置")
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()