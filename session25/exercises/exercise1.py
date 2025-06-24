#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session25 练习题1：虚拟环境管理

题目描述：
编写一个Python脚本，实现以下功能：
1. 检查当前是否在虚拟环境中
2. 如果不在虚拟环境中，提示用户创建虚拟环境
3. 检查指定的包是否已安装
4. 如果包未安装，自动安装这些包
5. 生成requirements.txt文件
6. 验证环境配置是否正确

输入示例：
需要检查的包列表：['flask', 'requests', 'pytest']

输出示例：
✅ 当前在虚拟环境中
✅ flask 已安装 (版本: 2.3.3)
❌ requests 未安装，正在安装...
✅ requests 安装成功 (版本: 2.31.0)
✅ pytest 已安装 (版本: 7.4.0)
✅ requirements.txt 已生成
✅ 环境配置验证通过

提示：
- 使用sys模块检查虚拟环境
- 使用subprocess模块执行pip命令
- 使用importlib模块检查包是否可导入
- 处理可能的异常情况
"""

import sys
import subprocess
import importlib
from pathlib import Path
from typing import List, Dict, Tuple


def check_virtual_environment() -> bool:
    """
    检查当前是否在虚拟环境中
    
    Returns:
        bool: 如果在虚拟环境中返回True，否则返回False
    """
    # 在这里实现你的代码
    pass


def check_package_installed(package_name: str) -> Tuple[bool, str]:
    """
    检查指定包是否已安装
    
    Args:
        package_name: 包名
    
    Returns:
        Tuple[bool, str]: (是否已安装, 版本号或错误信息)
    """
    # 在这里实现你的代码
    pass


def install_package(package_name: str) -> bool:
    """
    安装指定的包
    
    Args:
        package_name: 要安装的包名
    
    Returns:
        bool: 安装成功返回True，失败返回False
    """
    # 在这里实现你的代码
    pass


def generate_requirements_file(packages: List[str], filename: str = "requirements.txt") -> bool:
    """
    生成requirements.txt文件
    
    Args:
        packages: 包列表
        filename: 文件名
    
    Returns:
        bool: 生成成功返回True，失败返回False
    """
    # 在这里实现你的代码
    pass


def verify_environment(packages: List[str]) -> Dict[str, bool]:
    """
    验证环境配置
    
    Args:
        packages: 要验证的包列表
    
    Returns:
        Dict[str, bool]: 每个包的验证结果
    """
    # 在这里实现你的代码
    pass


def main():
    """
    主函数：执行虚拟环境管理任务
    """
    print("Session25 练习题1：虚拟环境管理")
    print("=" * 40)
    
    # 要检查的包列表
    required_packages = ['flask', 'requests', 'pytest']
    
    # 在这里实现主要逻辑
    # 1. 检查虚拟环境
    # 2. 检查和安装包
    # 3. 生成requirements.txt
    # 4. 验证环境配置
    
    pass


if __name__ == "__main__":
    main()