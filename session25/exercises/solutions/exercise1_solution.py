#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session25 练习题1解决方案：虚拟环境管理
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
    # 检查是否有虚拟环境相关的环境变量
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        return True
    
    # 检查VIRTUAL_ENV环境变量
    import os
    return 'VIRTUAL_ENV' in os.environ


def check_package_installed(package_name: str) -> Tuple[bool, str]:
    """
    检查指定包是否已安装
    
    Args:
        package_name: 包名
    
    Returns:
        Tuple[bool, str]: (是否已安装, 版本号或错误信息)
    """
    try:
        # 尝试导入包
        module = importlib.import_module(package_name)
        
        # 尝试获取版本号
        version = "未知版本"
        if hasattr(module, '__version__'):
            version = module.__version__
        elif hasattr(module, 'VERSION'):
            version = str(module.VERSION)
        else:
            # 使用pip show命令获取版本
            try:
                result = subprocess.run(
                    [sys.executable, '-m', 'pip', 'show', package_name],
                    capture_output=True,
                    text=True,
                    check=True
                )
                for line in result.stdout.split('\n'):
                    if line.startswith('Version:'):
                        version = line.split(':', 1)[1].strip()
                        break
            except subprocess.CalledProcessError:
                pass
        
        return True, version
    
    except ImportError:
        return False, "包未安装"
    except Exception as e:
        return False, f"检查失败: {str(e)}"


def install_package(package_name: str) -> bool:
    """
    安装指定的包
    
    Args:
        package_name: 要安装的包名
    
    Returns:
        bool: 安装成功返回True，失败返回False
    """
    try:
        print(f"正在安装 {package_name}...")
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', package_name],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ {package_name} 安装成功")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"❌ {package_name} 安装失败: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ {package_name} 安装失败: {str(e)}")
        return False


def generate_requirements_file(packages: List[str], filename: str = "requirements.txt") -> bool:
    """
    生成requirements.txt文件
    
    Args:
        packages: 包列表
        filename: 文件名
    
    Returns:
        bool: 生成成功返回True，失败返回False
    """
    try:
        requirements = []
        
        for package in packages:
            installed, version = check_package_installed(package)
            if installed and version != "未知版本":
                requirements.append(f"{package}=={version}")
            else:
                requirements.append(package)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(requirements))
            f.write('\n')
        
        print(f"✅ {filename} 已生成")
        return True
    
    except Exception as e:
        print(f"❌ 生成 {filename} 失败: {str(e)}")
        return False


def verify_environment(packages: List[str]) -> Dict[str, bool]:
    """
    验证环境配置
    
    Args:
        packages: 要验证的包列表
    
    Returns:
        Dict[str, bool]: 每个包的验证结果
    """
    results = {}
    
    for package in packages:
        try:
            importlib.import_module(package)
            results[package] = True
        except ImportError:
            results[package] = False
    
    return results


def main():
    """
    主函数：执行虚拟环境管理任务
    """
    print("Session25 练习题1：虚拟环境管理")
    print("=" * 40)
    
    # 要检查的包列表
    required_packages = ['flask', 'requests', 'pytest']
    
    # 1. 检查虚拟环境
    print("\n1. 检查虚拟环境状态...")
    if check_virtual_environment():
        print("✅ 当前在虚拟环境中")
    else:
        print("❌ 当前不在虚拟环境中")
        print("建议：请先创建并激活虚拟环境")
        print("  python -m venv venv")
        print("  venv\\Scripts\\activate  # Windows")
        print("  source venv/bin/activate  # Linux/Mac")
        return
    
    # 2. 检查和安装包
    print("\n2. 检查和安装依赖包...")
    for package in required_packages:
        installed, version = check_package_installed(package)
        
        if installed:
            print(f"✅ {package} 已安装 (版本: {version})")
        else:
            print(f"❌ {package} 未安装，正在安装...")
            if install_package(package):
                # 重新检查版本
                _, new_version = check_package_installed(package)
                print(f"✅ {package} 安装成功 (版本: {new_version})")
    
    # 3. 生成requirements.txt
    print("\n3. 生成requirements.txt文件...")
    generate_requirements_file(required_packages)
    
    # 4. 验证环境配置
    print("\n4. 验证环境配置...")
    verification_results = verify_environment(required_packages)
    
    all_verified = True
    for package, verified in verification_results.items():
        if verified:
            print(f"✅ {package} 验证通过")
        else:
            print(f"❌ {package} 验证失败")
            all_verified = False
    
    if all_verified:
        print("\n✅ 环境配置验证通过")
    else:
        print("\n❌ 环境配置验证失败，请检查安装情况")
    
    print("\n" + "=" * 40)
    print("虚拟环境管理任务完成！")


if __name__ == "__main__":
    main()