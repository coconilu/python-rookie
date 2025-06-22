#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session07 示例2：文件路径处理

本示例演示了Python中的文件路径处理，包括：
- os.path模块的使用
- pathlib模块的使用（推荐）
- 路径的拼接、分离和检查
- 目录的创建和遍历
- 跨平台路径处理

作者: Python教程团队
创建日期: 2024-12-22
"""

import os
import sys
from pathlib import Path
from datetime import datetime


def demo_os_path():
    """
    演示os.path模块的使用
    """
    print("=== os.path模块演示 ===")
    
    # 获取当前工作目录
    current_dir = os.getcwd()
    print(f"当前工作目录: {current_dir}")
    
    # 路径拼接
    file_path = os.path.join('data', 'logs', 'app.log')
    print(f"拼接路径: {file_path}")
    
    # 绝对路径
    abs_path = os.path.abspath(file_path)
    print(f"绝对路径: {abs_path}")
    
    # 路径分离
    dir_name = os.path.dirname(abs_path)
    file_name = os.path.basename(abs_path)
    print(f"目录名: {dir_name}")
    print(f"文件名: {file_name}")
    
    # 分离文件名和扩展名
    name, ext = os.path.splitext(file_name)
    print(f"文件名（无扩展名）: {name}")
    print(f"扩展名: {ext}")
    
    # 路径存在性检查
    print(f"\n路径存在性检查:")
    print(f"当前目录存在: {os.path.exists(current_dir)}")
    print(f"示例路径存在: {os.path.exists(file_path)}")
    
    # 路径类型检查
    print(f"\n路径类型检查:")
    print(f"当前目录是文件夹: {os.path.isdir(current_dir)}")
    print(f"当前目录是文件: {os.path.isfile(current_dir)}")
    
    # 获取文件大小和修改时间（如果文件存在）
    current_file = __file__  # 当前脚本文件
    if os.path.exists(current_file):
        size = os.path.getsize(current_file)
        mtime = os.path.getmtime(current_file)
        mtime_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n当前脚本文件信息:")
        print(f"文件大小: {size} 字节")
        print(f"修改时间: {mtime_str}")


def demo_pathlib():
    """
    演示pathlib模块的使用（推荐方式）
    """
    print("\n=== pathlib模块演示 ===")
    
    # 创建路径对象
    current_path = Path('.')
    print(f"当前路径: {current_path.resolve()}")
    
    # 路径拼接（使用 / 操作符）
    data_path = Path('data')
    log_path = data_path / 'logs' / 'app.log'
    config_path = data_path / 'config' / 'settings.json'
    
    print(f"\n路径拼接:")
    print(f"日志路径: {log_path}")
    print(f"配置路径: {config_path}")
    
    # 路径属性
    print(f"\n路径属性:")
    print(f"父目录: {log_path.parent}")
    print(f"文件名: {log_path.name}")
    print(f"文件名（无扩展名）: {log_path.stem}")
    print(f"扩展名: {log_path.suffix}")
    print(f"所有扩展名: {log_path.suffixes}")
    
    # 路径检查
    print(f"\n路径检查:")
    print(f"路径存在: {log_path.exists()}")
    print(f"是文件: {log_path.is_file()}")
    print(f"是目录: {log_path.is_dir()}")
    print(f"是绝对路径: {log_path.is_absolute()}")
    
    # 当前脚本文件信息
    current_file = Path(__file__)
    if current_file.exists():
        stat = current_file.stat()
        print(f"\n当前脚本文件信息:")
        print(f"文件大小: {stat.st_size} 字节")
        print(f"修改时间: {datetime.fromtimestamp(stat.st_mtime)}")
        print(f"绝对路径: {current_file.resolve()}")


def create_directory_structure():
    """
    创建示例目录结构
    """
    print("\n=== 创建目录结构 ===")
    
    # 定义目录结构
    base_dir = Path('example_project')
    directories = [
        base_dir / 'src' / 'main',
        base_dir / 'src' / 'utils',
        base_dir / 'data' / 'input',
        base_dir / 'data' / 'output',
        base_dir / 'logs',
        base_dir / 'config',
        base_dir / 'tests'
    ]
    
    # 创建目录
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✓ 创建目录: {directory}")
    
    # 创建一些示例文件
    files_to_create = [
        (base_dir / 'README.md', '# 示例项目\n\n这是一个示例项目结构。'),
        (base_dir / 'src' / 'main' / '__init__.py', '# 主模块'),
        (base_dir / 'src' / 'utils' / '__init__.py', '# 工具模块'),
        (base_dir / 'config' / 'settings.txt', 'debug=True\nport=8080'),
        (base_dir / 'logs' / 'app.log', f'[{datetime.now()}] 应用启动\n'),
    ]
    
    for file_path, content in files_to_create:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ 创建文件: {file_path}")
    
    return base_dir


def traverse_directory(directory):
    """
    遍历目录
    """
    print(f"\n=== 遍历目录: {directory} ===")
    
    directory = Path(directory)
    
    if not directory.exists():
        print(f"❌ 目录 {directory} 不存在")
        return
    
    print("\n方法1: 使用iterdir()遍历直接子项")
    for item in directory.iterdir():
        if item.is_file():
            size = item.stat().st_size
            print(f"📄 {item.name} ({size} 字节)")
        elif item.is_dir():
            print(f"📁 {item.name}/")
    
    print("\n方法2: 使用rglob()递归查找所有文件")
    for file_path in directory.rglob('*'):
        if file_path.is_file():
            # 计算相对路径
            relative_path = file_path.relative_to(directory)
            size = file_path.stat().st_size
            print(f"📄 {relative_path} ({size} 字节)")
    
    print("\n方法3: 查找特定类型的文件")
    # 查找所有.py文件
    py_files = list(directory.rglob('*.py'))
    if py_files:
        print("Python文件:")
        for py_file in py_files:
            relative_path = py_file.relative_to(directory)
            print(f"  🐍 {relative_path}")
    
    # 查找所有.txt文件
    txt_files = list(directory.rglob('*.txt'))
    if txt_files:
        print("文本文件:")
        for txt_file in txt_files:
            relative_path = txt_file.relative_to(directory)
            print(f"  📝 {relative_path}")


def demonstrate_path_operations():
    """
    演示各种路径操作
    """
    print("\n=== 路径操作演示 ===")
    
    # 路径解析
    sample_paths = [
        'data/logs/app.log',
        '../config/settings.json',
        '/absolute/path/to/file.txt',
        'relative/path/file.py'
    ]
    
    print("路径解析:")
    for path_str in sample_paths:
        path = Path(path_str)
        print(f"\n原始路径: {path_str}")
        print(f"  父目录: {path.parent}")
        print(f"  文件名: {path.name}")
        print(f"  扩展名: {path.suffix}")
        print(f"  是绝对路径: {path.is_absolute()}")
        
        # 尝试解析为绝对路径
        try:
            abs_path = path.resolve()
            print(f"  绝对路径: {abs_path}")
        except Exception as e:
            print(f"  无法解析绝对路径: {e}")
    
    # 路径比较
    print("\n路径比较:")
    path1 = Path('data/file.txt')
    path2 = Path('data') / 'file.txt'
    path3 = Path('DATA/FILE.TXT')  # 不同大小写
    
    print(f"path1: {path1}")
    print(f"path2: {path2}")
    print(f"path3: {path3}")
    print(f"path1 == path2: {path1 == path2}")
    print(f"path1 == path3: {path1 == path3}")
    
    # 路径匹配
    print("\n路径匹配:")
    test_paths = [
        Path('data/logs/app.log'),
        Path('data/config/settings.json'),
        Path('src/main.py'),
        Path('tests/test_main.py')
    ]
    
    patterns = ['*.log', '*.py', 'data/*', 'test*']
    
    for pattern in patterns:
        print(f"\n模式 '{pattern}' 匹配的路径:")
        for test_path in test_paths:
            if test_path.match(pattern):
                print(f"  ✓ {test_path}")


def cross_platform_paths():
    """
    演示跨平台路径处理
    """
    print("\n=== 跨平台路径处理 ===")
    
    print(f"当前操作系统: {sys.platform}")
    print(f"路径分隔符: '{os.sep}'")
    print(f"路径列表分隔符: '{os.pathsep}'")
    
    # 使用pathlib自动处理跨平台路径
    cross_platform_path = Path('data') / 'logs' / 'app.log'
    print(f"\n跨平台路径: {cross_platform_path}")
    print(f"字符串表示: '{str(cross_platform_path)}'")
    
    # 转换路径格式
    if sys.platform.startswith('win'):
        print("Windows平台路径示例:")
        win_path = Path('C:/Users/Admin/Documents/file.txt')
        print(f"  原始: {win_path}")
        print(f"  标准化: {win_path.resolve()}")
    else:
        print("Unix/Linux平台路径示例:")
        unix_path = Path('/home/user/documents/file.txt')
        print(f"  原始: {unix_path}")
        print(f"  标准化: {unix_path.resolve()}")
    
    # 处理特殊字符
    special_chars_path = Path('文件夹') / '中文文件名.txt'
    print(f"\n包含特殊字符的路径: {special_chars_path}")
    print(f"编码后: {str(special_chars_path).encode('utf-8')}")


def cleanup_example_project():
    """
    清理示例项目目录
    """
    print("\n=== 清理示例项目 ===")
    
    import shutil
    
    project_dir = Path('example_project')
    if project_dir.exists():
        shutil.rmtree(project_dir)
        print(f"✓ 删除目录: {project_dir}")
    else:
        print(f"- 目录不存在: {project_dir}")


def main():
    """
    主函数
    """
    print("Session07 示例2：文件路径处理")
    print("=" * 50)
    
    try:
        # 1. 演示os.path模块
        demo_os_path()
        
        # 2. 演示pathlib模块
        demo_pathlib()
        
        # 3. 创建目录结构
        project_dir = create_directory_structure()
        
        # 4. 遍历目录
        traverse_directory(project_dir)
        
        # 5. 演示路径操作
        demonstrate_path_operations()
        
        # 6. 跨平台路径处理
        cross_platform_paths()
        
        print("\n" + "=" * 50)
        print("✅ 示例2演示完成！")
        print("\n💡 重要提示：")
        print("- 推荐使用pathlib模块而不是os.path")
        print("- pathlib提供了更现代、更直观的API")
        print("- pathlib自动处理跨平台路径问题")
        
        # 询问是否清理文件
        response = input("\n是否清理示例项目？(y/n): ").lower().strip()
        if response == 'y':
            cleanup_example_project()
        else:
            print("示例项目已保留，你可以手动查看目录结构。")
            
    except Exception as e:
        print(f"\n❌ 示例运行过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()