#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session23 工具安装脚本：代码质量工具安装器

这个脚本帮助用户安装和配置代码质量检查工具。
支持自动检测已安装的工具，并提供安装建议。

运行方式:
    python install_tools.py
    python install_tools.py --install-all  # 安装所有工具
    python install_tools.py --check-only   # 仅检查工具状态

作者: Python教程团队
创建日期: 2024-01-01
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class ToolInstaller:
    """
    代码质量工具安装器
    """
    
    def __init__(self) -> None:
        """
        初始化安装器
        """
        self.tools = {
            'ruff': {
                'description': '快速的Python代码检查器和格式化工具',
                'install_command': 'pip install ruff',
                'check_command': 'ruff --version',
                'priority': 1,  # 优先级：1=必需，2=推荐，3=可选
                'category': 'linter'
            },
            'black': {
                'description': '代码格式化工具',
                'install_command': 'pip install black',
                'check_command': 'black --version',
                'priority': 1,
                'category': 'formatter'
            },
            'mypy': {
                'description': '静态类型检查器',
                'install_command': 'pip install mypy',
                'check_command': 'mypy --version',
                'priority': 1,
                'category': 'type_checker'
            },
            'bandit': {
                'description': '安全漏洞检测工具',
                'install_command': 'pip install bandit',
                'check_command': 'bandit --version',
                'priority': 2,
                'category': 'security'
            },
            'flake8': {
                'description': '代码风格检查工具',
                'install_command': 'pip install flake8',
                'check_command': 'flake8 --version',
                'priority': 3,
                'category': 'linter'
            },
            'pylint': {
                'description': '全面的代码分析工具',
                'install_command': 'pip install pylint',
                'check_command': 'pylint --version',
                'priority': 3,
                'category': 'linter'
            },
            'isort': {
                'description': '导入语句排序工具',
                'install_command': 'pip install isort',
                'check_command': 'isort --version',
                'priority': 2,
                'category': 'formatter'
            },
            'pre-commit': {
                'description': 'Git钩子管理工具',
                'install_command': 'pip install pre-commit',
                'check_command': 'pre-commit --version',
                'priority': 2,
                'category': 'automation'
            }
        }
    
    def print_header(self, title: str) -> None:
        """
        打印标题
        
        Args:
            title: 标题文本
        """
        print("\n" + "=" * 60)
        print(f" {title} ")
        print("=" * 60)
    
    def print_section(self, title: str) -> None:
        """
        打印章节标题
        
        Args:
            title: 章节标题
        """
        print(f"\n{'-' * 40}")
        print(f" {title} ")
        print(f"{'-' * 40}")
    
    def check_tool_availability(self) -> Dict[str, Tuple[bool, str]]:
        """
        检查工具可用性
        
        Returns:
            工具可用性字典，格式为 {tool_name: (is_available, version_info)}
        """
        availability = {}
        
        for tool_name, tool_info in self.tools.items():
            try:
                result = subprocess.run(
                    tool_info['check_command'].split(),
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    version_info = result.stdout.strip() or result.stderr.strip()
                    availability[tool_name] = (True, version_info)
                else:
                    availability[tool_name] = (False, "未安装")
            
            except (subprocess.TimeoutExpired, FileNotFoundError):
                availability[tool_name] = (False, "未安装")
            except Exception as e:
                availability[tool_name] = (False, f"检查失败: {e}")
        
        return availability
    
    def display_tool_status(self, availability: Dict[str, Tuple[bool, str]]) -> None:
        """
        显示工具状态
        
        Args:
            availability: 工具可用性字典
        """
        self.print_section("工具状态检查")
        
        # 按优先级分组显示
        priority_groups = {
            1: "必需工具",
            2: "推荐工具",
            3: "可选工具"
        }
        
        for priority, group_name in priority_groups.items():
            print(f"\n{group_name}:")
            
            for tool_name, tool_info in self.tools.items():
                if tool_info['priority'] == priority:
                    is_available, version_info = availability[tool_name]
                    status_icon = "✅" if is_available else "❌"
                    
                    print(f"  {status_icon} {tool_name:12} - {tool_info['description']}")
                    if is_available:
                        print(f"    {'':14} 版本: {version_info}")
                    else:
                        print(f"    {'':14} 状态: {version_info}")
    
    def install_tool(self, tool_name: str) -> bool:
        """
        安装指定工具
        
        Args:
            tool_name: 工具名称
            
        Returns:
            安装是否成功
        """
        if tool_name not in self.tools:
            print(f"❌ 未知工具: {tool_name}")
            return False
        
        tool_info = self.tools[tool_name]
        install_command = tool_info['install_command']
        
        print(f"\n正在安装 {tool_name}...")
        print(f"执行命令: {install_command}")
        
        try:
            result = subprocess.run(
                install_command.split(),
                check=True,
                text=True
            )
            
            print(f"✅ {tool_name} 安装成功！")
            return True
        
        except subprocess.CalledProcessError as e:
            print(f"❌ {tool_name} 安装失败: {e}")
            return False
        except Exception as e:
            print(f"❌ 安装 {tool_name} 时出现错误: {e}")
            return False
    
    def install_missing_tools(self, availability: Dict[str, Tuple[bool, str]], 
                            priority_filter: Optional[int] = None) -> None:
        """
        安装缺失的工具
        
        Args:
            availability: 工具可用性字典
            priority_filter: 优先级过滤器（仅安装指定优先级的工具）
        """
        missing_tools = []
        
        for tool_name, (is_available, _) in availability.items():
            if not is_available:
                tool_priority = self.tools[tool_name]['priority']
                if priority_filter is None or tool_priority <= priority_filter:
                    missing_tools.append(tool_name)
        
        if not missing_tools:
            print("\n✅ 所有工具都已安装！")
            return
        
        self.print_section(f"安装缺失工具 ({len(missing_tools)} 个)")
        
        for tool_name in missing_tools:
            self.install_tool(tool_name)
    
    def create_config_files(self) -> None:
        """
        创建配置文件示例
        """
        self.print_section("创建配置文件")
        
        config_files = {
            'pyproject.toml': self._get_pyproject_config(),
            '.pre-commit-config.yaml': self._get_precommit_config(),
            'mypy.ini': self._get_mypy_config()
        }
        
        for filename, content in config_files.items():
            file_path = Path(filename)
            
            if file_path.exists():
                print(f"⚠️  {filename} 已存在，跳过创建")
                continue
            
            try:
                file_path.write_text(content, encoding='utf-8')
                print(f"✅ 创建配置文件: {filename}")
            except Exception as e:
                print(f"❌ 创建 {filename} 失败: {e}")
    
    def _get_pyproject_config(self) -> str:
        """
        获取pyproject.toml配置内容
        
        Returns:
            配置文件内容
        """
        return '''
[tool.ruff]
# 启用的规则
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4", # flake8-comprehensions
    "UP", # pyupgrade
]

# 忽略的规则
ignore = [
    "E501",  # 行长度由black处理
]

# 每行最大字符数
line-length = 88

# 目标Python版本
target-version = "py38"

# 排除的文件和目录
exclude = [
    ".git",
    "__pycache__",
    ".venv",
    "build",
    "dist",
]

[tool.black]
# 每行最大字符数
line-length = 88

# 目标Python版本
target-version = ["py38"]

# 包含的文件扩展名
include = "\\.pyi?$"

# 排除的文件和目录
exclude = """
/(
  (
      \\.eggs
    | \\.git
    | \\.hg
    | \\.mypy_cache
    | \\.tox
    | \\.venv
    | _build
    | buck-out
    | build
    | dist
  )/
)
"""

[tool.mypy]
# 基本配置
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true

# 严格模式
strict = false

# 排除的模块
[[tool.mypy.overrides]]
module = "tests.*"
ignore_errors = true

[tool.bandit]
# 排除的测试
skips = ["B101", "B601"]

# 排除的路径
exclude_dirs = ["tests", "test_*.py"]

[tool.isort]
# 配置文件
profile = "black"
line_length = 88
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
'''
    
    def _get_precommit_config(self) -> str:
        """
        获取pre-commit配置内容
        
        Returns:
            配置文件内容
        """
        return '''
# Pre-commit配置文件
# 安装: pre-commit install
# 运行: pre-commit run --all-files

repos:
  # Ruff - 快速的Python代码检查器
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  # Black - 代码格式化
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
        language_version: python3

  # MyPy - 类型检查
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  # Bandit - 安全检查
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ["-c", "pyproject.toml"]
        additional_dependencies: ["bandit[toml]"]

  # 通用钩子
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: debug-statements
'''
    
    def _get_mypy_config(self) -> str:
        """
        获取mypy.ini配置内容
        
        Returns:
            配置文件内容
        """
        return '''
[mypy]
# 基本配置
python_version = 3.8
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
disallow_untyped_decorators = True

# 严格模式选项
strict_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
warn_unreachable = True

# 输出格式
show_error_codes = True
show_column_numbers = True
color_output = True

# 缓存
cache_dir = .mypy_cache

# 排除的文件
exclude = (?x)(
    ^build/
    | ^dist/
    | ^__pycache__/
    | \\.git/
)

# 第三方库配置
[mypy-pytest.*]
ignore_missing_imports = True

[mypy-setuptools.*]
ignore_missing_imports = True

[mypy-tests.*]
ignore_errors = True
'''
    
    def show_usage_examples(self) -> None:
        """
        显示使用示例
        """
        self.print_section("使用示例")
        
        examples = [
            ("检查代码风格", "ruff check ."),
            ("自动修复问题", "ruff check --fix ."),
            ("格式化代码", "black ."),
            ("类型检查", "mypy ."),
            ("安全检查", "bandit -r ."),
            ("排序导入", "isort ."),
            ("运行所有检查", "ruff check . && black --check . && mypy . && bandit -r .")
        ]
        
        for description, command in examples:
            print(f"  {description}:")
            print(f"    {command}")
            print()
    
    def show_integration_tips(self) -> None:
        """
        显示集成建议
        """
        self.print_section("集成建议")
        
        tips = [
            "1. 在IDE中配置代码质量工具",
            "   - VS Code: 安装Python、Ruff、Black扩展",
            "   - PyCharm: 配置External Tools",
            "",
            "2. 设置Git钩子",
            "   - 安装pre-commit: pip install pre-commit",
            "   - 初始化钩子: pre-commit install",
            "",
            "3. CI/CD集成",
            "   - 在GitHub Actions中运行代码质量检查",
            "   - 设置质量门禁",
            "",
            "4. 团队协作",
            "   - 统一配置文件",
            "   - 定期代码审查",
            "   - 制定编码规范"
        ]
        
        for tip in tips:
            print(f"  {tip}")


def main() -> None:
    """
    主函数
    """
    parser = argparse.ArgumentParser(
        description="Python代码质量工具安装器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python install_tools.py                    # 交互式安装
  python install_tools.py --install-all     # 安装所有工具
  python install_tools.py --check-only      # 仅检查状态
  python install_tools.py --essential-only  # 仅安装必需工具
        """
    )
    
    parser.add_argument(
        '--install-all',
        action='store_true',
        help='安装所有工具'
    )
    
    parser.add_argument(
        '--essential-only',
        action='store_true',
        help='仅安装必需工具（优先级1）'
    )
    
    parser.add_argument(
        '--check-only',
        action='store_true',
        help='仅检查工具状态，不安装'
    )
    
    parser.add_argument(
        '--create-config',
        action='store_true',
        help='创建配置文件'
    )
    
    args = parser.parse_args()
    
    installer = ToolInstaller()
    installer.print_header("Python代码质量工具安装器")
    
    print("这个工具将帮助您安装和配置Python代码质量检查工具。")
    
    # 检查工具状态
    availability = installer.check_tool_availability()
    installer.display_tool_status(availability)
    
    if args.check_only:
        installer.show_usage_examples()
        installer.show_integration_tips()
        return
    
    # 安装工具
    if args.install_all:
        installer.install_missing_tools(availability)
    elif args.essential_only:
        installer.install_missing_tools(availability, priority_filter=1)
    else:
        # 交互式安装
        missing_tools = [name for name, (available, _) in availability.items() if not available]
        
        if missing_tools:
            print(f"\n发现 {len(missing_tools)} 个未安装的工具。")
            response = input("是否安装必需工具？(y/n): ").lower().strip()
            
            if response in ['y', 'yes', '是']:
                installer.install_missing_tools(availability, priority_filter=1)
                
                response = input("\n是否也安装推荐工具？(y/n): ").lower().strip()
                if response in ['y', 'yes', '是']:
                    installer.install_missing_tools(availability, priority_filter=2)
        else:
            print("\n✅ 所有工具都已安装！")
    
    # 创建配置文件
    if args.create_config or not args.check_only:
        response = input("\n是否创建配置文件示例？(y/n): ").lower().strip()
        if response in ['y', 'yes', '是']:
            installer.create_config_files()
    
    # 显示使用示例和集成建议
    installer.show_usage_examples()
    installer.show_integration_tips()
    
    installer.print_header("安装完成")
    print("感谢使用Python代码质量工具安装器！")
    print("\n下一步建议:")
    print("1. 运行 'python run_demo.py' 查看工具演示")
    print("2. 在您的项目中配置这些工具")
    print("3. 设置IDE集成")
    print("4. 配置Git钩子")


if __name__ == '__main__':
    main()