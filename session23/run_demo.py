#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session23 演示脚本：代码质量与规范

这个脚本演示了如何使用代码质量检查工具来改善Python代码质量。
包含了实际的代码示例和工具使用演示。

运行方式:
    python run_demo.py

作者: Python教程团队
创建日期: 2024-01-01
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Any


def print_section(title: str) -> None:
    """
    打印章节标题
    
    Args:
        title: 章节标题
    """
    print("\n" + "=" * 60)
    print(f" {title} ")
    print("=" * 60)


def print_subsection(title: str) -> None:
    """
    打印子章节标题
    
    Args:
        title: 子章节标题
    """
    print(f"\n{'-' * 40}")
    print(f" {title} ")
    print(f"{'-' * 40}")


def check_tool_availability() -> Dict[str, bool]:
    """
    检查代码质量工具的可用性
    
    Returns:
        工具可用性字典
    """
    tools = {
        'ruff': 'ruff --version',
        'black': 'black --version',
        'mypy': 'mypy --version',
        'bandit': 'bandit --version',
        'flake8': 'flake8 --version',
        'pylint': 'pylint --version'
    }
    
    availability = {}
    
    for tool_name, command in tools.items():
        try:
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                timeout=10
            )
            availability[tool_name] = result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            availability[tool_name] = False
    
    return availability


def demonstrate_pep8_issues() -> None:
    """
    演示PEP 8规范问题
    """
    print_subsection("PEP 8 规范问题演示")
    
    # 创建有问题的代码示例
    bad_code = '''
# 这是一个违反PEP 8规范的代码示例
import os,sys,json # 导入应该分行

def bad_function(x,y,z): # 缺少空格和类型注解
    if x>0: # 操作符周围缺少空格
        result=x+y+z # 赋值操作符周围缺少空格
        return result
    else:
        return 0

class badClass: # 类名应该使用驼峰命名
    def __init__(self,name):
        self.name=name # 赋值操作符周围缺少空格
    
    def get_name(self):
        return self.name
'''
    
    print("违反PEP 8规范的代码:")
    print(bad_code)
    
    # 显示正确的代码
    good_code = '''
# 这是符合PEP 8规范的代码示例
import json
import os
import sys
from typing import Union


def good_function(x: int, y: int, z: int) -> int:
    """计算三个数的和（如果x大于0）"""
    if x > 0:
        result = x + y + z
        return result
    else:
        return 0


class GoodClass:
    """一个符合规范的类示例"""
    
    def __init__(self, name: str) -> None:
        """初始化类实例"""
        self.name = name
    
    def get_name(self) -> str:
        """获取名称"""
        return self.name
'''
    
    print("\n符合PEP 8规范的代码:")
    print(good_code)


def demonstrate_type_annotations() -> None:
    """
    演示类型注解的重要性
    """
    print_subsection("类型注解演示")
    
    print("没有类型注解的代码:")
    no_types_code = '''
def process_data(data, multiplier):
    """处理数据"""
    result = []
    for item in data:
        result.append(item * multiplier)
    return result

def calculate_average(numbers):
    """计算平均值"""
    if not numbers:
        return None
    return sum(numbers) / len(numbers)
'''
    print(no_types_code)
    
    print("\n有类型注解的代码:")
    with_types_code = '''
from typing import List, Optional, Union

def process_data(data: List[Union[int, float]], multiplier: float) -> List[float]:
    """处理数据
    
    Args:
        data: 数字列表
        multiplier: 乘数
        
    Returns:
        处理后的数据列表
    """
    result: List[float] = []
    for item in data:
        result.append(item * multiplier)
    return result

def calculate_average(numbers: List[Union[int, float]]) -> Optional[float]:
    """计算平均值
    
    Args:
        numbers: 数字列表
        
    Returns:
        平均值，如果列表为空则返回None
    """
    if not numbers:
        return None
    return sum(numbers) / len(numbers)
'''
    print(with_types_code)


def demonstrate_security_issues() -> None:
    """
    演示安全问题
    """
    print_subsection("安全问题演示")
    
    print("存在安全问题的代码:")
    insecure_code = '''
import os
import subprocess

# 硬编码敏感信息
API_KEY = "sk-1234567890abcdef"
DATABASE_PASSWORD = "admin123"

def execute_command(user_input):
    """执行用户输入的命令（危险！）"""
    # 直接执行用户输入，存在命令注入风险
    os.system(user_input)

def read_file(filename):
    """读取文件（不安全）"""
    # 没有路径验证，存在路径遍历攻击风险
    with open(filename, 'r') as f:
        return f.read()

def sql_query(user_id):
    """SQL查询（存在注入风险）"""
    query = f"SELECT * FROM users WHERE id = {user_id}"
    # 直接拼接SQL，存在SQL注入风险
    return query
'''
    print(insecure_code)
    
    print("\n安全的代码:")
    secure_code = '''
import os
import subprocess
from pathlib import Path
from typing import Optional

# 从环境变量获取敏感信息
API_KEY = os.getenv("API_KEY")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

def execute_command(command: str, allowed_commands: List[str]) -> Optional[str]:
    """安全地执行命令
    
    Args:
        command: 要执行的命令
        allowed_commands: 允许的命令列表
        
    Returns:
        命令输出或None（如果命令不被允许）
    """
    if command not in allowed_commands:
        raise ValueError(f"Command '{command}' is not allowed")
    
    try:
        result = subprocess.run(
            command.split(),
            capture_output=True,
            text=True,
            timeout=30,
            check=True
        )
        return result.stdout
    except subprocess.SubprocessError as e:
        print(f"Command execution failed: {e}")
        return None

def read_file(filename: str, base_dir: str = "./data") -> Optional[str]:
    """安全地读取文件
    
    Args:
        filename: 文件名
        base_dir: 基础目录
        
    Returns:
        文件内容或None
    """
    base_path = Path(base_dir).resolve()
    file_path = (base_path / filename).resolve()
    
    # 确保文件在允许的目录内
    if not str(file_path).startswith(str(base_path)):
        raise ValueError("Path traversal attempt detected")
    
    try:
        with file_path.open('r', encoding='utf-8') as f:
            return f.read()
    except (FileNotFoundError, PermissionError) as e:
        print(f"File read error: {e}")
        return None

def sql_query(user_id: int) -> str:
    """安全的SQL查询
    
    Args:
        user_id: 用户ID
        
    Returns:
        参数化查询字符串
    """
    # 使用参数化查询防止SQL注入
    query = "SELECT * FROM users WHERE id = %s"
    # 在实际使用中，应该使用数据库驱动的参数化查询
    return query
'''
    print(secure_code)


def run_tool_demo(tool_name: str, available_tools: Dict[str, bool]) -> None:
    """
    运行工具演示
    
    Args:
        tool_name: 工具名称
        available_tools: 可用工具字典
    """
    if not available_tools.get(tool_name, False):
        print(f"❌ {tool_name} 不可用，跳过演示")
        return
    
    print(f"✅ {tool_name} 可用，运行演示...")
    
    # 创建示例文件
    example_file = Path("temp_example.py")
    example_code = '''
import os,sys

def bad_function(x,y):
    if x>0:
        return x+y
    else:
        return 0

class badClass:
    def __init__(self,name):
        self.name=name
'''
    
    try:
        example_file.write_text(example_code, encoding='utf-8')
        
        if tool_name == 'ruff':
            # 运行ruff检查
            result = subprocess.run(
                ['ruff', 'check', str(example_file)],
                capture_output=True,
                text=True
            )
            print(f"Ruff 检查结果 (退出码: {result.returncode}):")
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(f"错误: {result.stderr}")
        
        elif tool_name == 'black':
            # 运行black格式化（仅检查）
            result = subprocess.run(
                ['black', '--check', '--diff', str(example_file)],
                capture_output=True,
                text=True
            )
            print(f"Black 检查结果 (退出码: {result.returncode}):")
            if result.stdout:
                print(result.stdout)
        
        elif tool_name == 'mypy':
            # 运行mypy类型检查
            result = subprocess.run(
                ['mypy', str(example_file)],
                capture_output=True,
                text=True
            )
            print(f"MyPy 检查结果 (退出码: {result.returncode}):")
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(f"错误: {result.stderr}")
    
    except Exception as e:
        print(f"运行 {tool_name} 时出错: {e}")
    
    finally:
        # 清理临时文件
        if example_file.exists():
            example_file.unlink()


def demonstrate_project_quality_checker() -> None:
    """
    演示项目中的代码质量检查器
    """
    print_subsection("项目代码质量检查器演示")
    
    project_dir = Path("project")
    if not project_dir.exists():
        print("❌ project 目录不存在，跳过演示")
        return
    
    quality_checker_file = project_dir / "quality_checker.py"
    if not quality_checker_file.exists():
        print("❌ quality_checker.py 不存在，跳过演示")
        return
    
    print("✅ 找到代码质量检查器，运行演示...")
    
    try:
        # 切换到项目目录
        original_cwd = os.getcwd()
        os.chdir(project_dir)
        
        # 运行质量检查器
        result = subprocess.run(
            [sys.executable, "quality_checker.py", "--help"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print("代码质量检查器帮助信息:")
        print(result.stdout)
        
        if result.stderr:
            print(f"错误信息: {result.stderr}")
    
    except Exception as e:
        print(f"运行代码质量检查器时出错: {e}")
    
    finally:
        # 恢复原始工作目录
        os.chdir(original_cwd)


def show_best_practices() -> None:
    """
    显示代码质量最佳实践
    """
    print_subsection("代码质量最佳实践")
    
    practices = [
        "1. 遵循PEP 8编码规范",
        "2. 使用类型注解提高代码可读性",
        "3. 编写清晰的文档字符串",
        "4. 保持函数和类的单一职责",
        "5. 使用有意义的变量和函数名",
        "6. 避免硬编码，使用配置文件",
        "7. 处理异常情况",
        "8. 编写单元测试",
        "9. 使用代码质量检查工具",
        "10. 定期进行代码审查",
        "11. 避免安全漏洞",
        "12. 保持代码简洁和可维护"
    ]
    
    for practice in practices:
        print(f"  {practice}")
    
    print("\n推荐的工具链:")
    tools = [
        "• ruff - 快速的Python代码检查器和格式化工具",
        "• black - 代码格式化工具",
        "• mypy - 静态类型检查器",
        "• bandit - 安全漏洞检测工具",
        "• pytest - 测试框架",
        "• pre-commit - Git钩子管理工具"
    ]
    
    for tool in tools:
        print(f"  {tool}")


def main() -> None:
    """
    主函数：运行所有演示
    """
    print_section("Session23: 代码质量与规范 - 演示")
    
    print("欢迎来到Python代码质量与规范的演示！")
    print("本演示将展示如何使用各种工具来提高代码质量。")
    
    # 检查工具可用性
    print_subsection("检查工具可用性")
    available_tools = check_tool_availability()
    
    for tool_name, available in available_tools.items():
        status = "✅ 可用" if available else "❌ 不可用"
        print(f"  {tool_name}: {status}")
    
    # 演示PEP 8问题
    demonstrate_pep8_issues()
    
    # 演示类型注解
    demonstrate_type_annotations()
    
    # 演示安全问题
    demonstrate_security_issues()
    
    # 运行工具演示
    print_section("工具演示")
    for tool_name in ['ruff', 'black', 'mypy']:
        print_subsection(f"{tool_name.upper()} 演示")
        run_tool_demo(tool_name, available_tools)
    
    # 演示项目质量检查器
    print_section("项目演示")
    demonstrate_project_quality_checker()
    
    # 显示最佳实践
    print_section("最佳实践")
    show_best_practices()
    
    print_section("演示完成")
    print("感谢观看！希望这个演示对您理解Python代码质量有所帮助。")
    print("\n下一步建议:")
    print("1. 安装推荐的代码质量工具")
    print("2. 在您的项目中配置这些工具")
    print("3. 将代码质量检查集成到您的开发流程中")
    print("4. 定期审查和改进您的代码")


if __name__ == '__main__':
    main()