#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session25 练习题2：依赖管理

题目描述：
编写一个Python脚本，为一个现有项目创建pyproject.toml文件，并使用uv管理依赖。脚本应实现以下功能：
1. 扫描项目目录，找出所有Python文件中的import语句
2. 分析这些import语句，识别出第三方库依赖
3. 生成pyproject.toml文件，包含项目信息和依赖列表
4. 使用uv安装这些依赖
5. 验证依赖安装是否成功

输入示例：
项目目录路径：/path/to/project

输出示例：
✅ 扫描项目目录完成，找到15个Python文件
✅ 分析import语句完成，识别出以下依赖：
   - flask
   - requests
   - pandas
   - matplotlib
✅ 生成pyproject.toml文件成功
✅ 使用uv安装依赖中...
✅ 依赖安装完成
✅ 验证依赖安装：所有依赖均已成功安装

提示：
- 使用ast模块解析Python文件中的import语句
- 使用subprocess模块执行uv命令
- 区分标准库和第三方库
- 处理可能的异常情况
"""

import os
import ast
import subprocess
from pathlib import Path
from typing import List, Dict, Set


def scan_project_directory(project_path: str) -> List[Path]:
    """
    扫描项目目录，找出所有Python文件
    
    Args:
        project_path: 项目目录路径
    
    Returns:
        List[Path]: Python文件路径列表
    """
    # 在这里实现你的代码
    pass


def extract_imports(file_path: Path) -> Set[str]:
    """
    从Python文件中提取import语句
    
    Args:
        file_path: Python文件路径
    
    Returns:
        Set[str]: 导入的模块名集合
    """
    # 在这里实现你的代码
    pass


def filter_third_party_packages(imports: Set[str]) -> Set[str]:
    """
    过滤出第三方库依赖
    
    Args:
        imports: 所有导入的模块名
    
    Returns:
        Set[str]: 第三方库依赖集合
    """
    # 在这里实现你的代码
    pass


def generate_pyproject_toml(project_path: str, dependencies: Set[str], project_name: str = None) -> bool:
    """
    生成pyproject.toml文件
    
    Args:
        project_path: 项目目录路径
        dependencies: 依赖集合
        project_name: 项目名称，如果为None则使用目录名
    
    Returns:
        bool: 生成成功返回True，失败返回False
    """
    # 在这里实现你的代码
    pass


def install_dependencies_with_uv(project_path: str) -> bool:
    """
    使用uv安装依赖
    
    Args:
        project_path: 项目目录路径
    
    Returns:
        bool: 安装成功返回True，失败返回False
    """
    # 在这里实现你的代码
    pass


def verify_dependencies(dependencies: Set[str]) -> Dict[str, bool]:
    """
    验证依赖安装是否成功
    
    Args:
        dependencies: 依赖集合
    
    Returns:
        Dict[str, bool]: 每个依赖的验证结果
    """
    # 在这里实现你的代码
    pass


def main():
    """
    主函数：执行依赖管理任务
    """
    print("Session25 练习题2：依赖管理")
    print("=" * 40)
    
    # 获取项目目录路径（这里使用当前目录作为示例）
    project_path = os.getcwd()
    print(f"项目目录：{project_path}")
    
    # 在这里实现主要逻辑
    # 1. 扫描项目目录
    # 2. 提取和分析import语句
    # 3. 生成pyproject.toml
    # 4. 安装依赖
    # 5. 验证依赖安装
    
    pass


if __name__ == "__main__":
    main()