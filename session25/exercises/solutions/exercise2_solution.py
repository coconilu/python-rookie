#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session25 练习题2解决方案：依赖管理
"""

import os
import ast
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Set


# 标准库模块列表（Python 3.9+的主要标准库）
STANDARD_LIBRARY = {
    'abc', 'aifc', 'argparse', 'array', 'ast', 'asynchat', 'asyncio', 'asyncore',
    'atexit', 'audioop', 'base64', 'bdb', 'binascii', 'binhex', 'bisect',
    'builtins', 'bz2', 'calendar', 'cgi', 'cgitb', 'chunk', 'cmath', 'cmd',
    'code', 'codecs', 'codeop', 'collections', 'colorsys', 'compileall',
    'concurrent', 'configparser', 'contextlib', 'copy', 'copyreg', 'cProfile',
    'crypt', 'csv', 'ctypes', 'curses', 'dataclasses', 'datetime', 'dbm',
    'decimal', 'difflib', 'dis', 'distutils', 'doctest', 'email', 'encodings',
    'ensurepip', 'enum', 'errno', 'faulthandler', 'fcntl', 'filecmp',
    'fileinput', 'fnmatch', 'formatter', 'fractions', 'ftplib', 'functools',
    'gc', 'getopt', 'getpass', 'gettext', 'glob', 'grp', 'gzip', 'hashlib',
    'heapq', 'hmac', 'html', 'http', 'imaplib', 'imghdr', 'imp', 'importlib',
    'inspect', 'io', 'ipaddress', 'itertools', 'json', 'keyword', 'lib2to3',
    'linecache', 'locale', 'logging', 'lzma', 'mailbox', 'mailcap', 'marshal',
    'math', 'mimetypes', 'mmap', 'modulefinder', 'multiprocessing', 'netrc',
    'nntplib', 'numbers', 'operator', 'optparse', 'os', 'ossaudiodev',
    'pathlib', 'pdb', 'pickle', 'pickletools', 'pipes', 'pkgutil', 'platform',
    'plistlib', 'poplib', 'posix', 'pprint', 'profile', 'pstats', 'pty',
    'pwd', 'py_compile', 'pyclbr', 'pydoc', 'queue', 'quopri', 'random',
    're', 'readline', 'reprlib', 'resource', 'rlcompleter', 'runpy', 'sched',
    'secrets', 'select', 'selectors', 'shelve', 'shlex', 'shutil', 'signal',
    'site', 'smtpd', 'smtplib', 'sndhdr', 'socket', 'socketserver', 'sqlite3',
    'ssl', 'stat', 'statistics', 'string', 'stringprep', 'struct', 'subprocess',
    'sunau', 'symbol', 'symtable', 'sys', 'sysconfig', 'syslog', 'tabnanny',
    'tarfile', 'telnetlib', 'tempfile', 'termios', 'test', 'textwrap',
    'threading', 'time', 'timeit', 'tkinter', 'token', 'tokenize', 'trace',
    'traceback', 'tracemalloc', 'tty', 'turtle', 'turtledemo', 'types',
    'typing', 'unicodedata', 'unittest', 'urllib', 'uu', 'uuid', 'venv',
    'warnings', 'wave', 'weakref', 'webbrowser', 'winreg', 'winsound',
    'wsgiref', 'xdrlib', 'xml', 'xmlrpc', 'zipapp', 'zipfile', 'zipimport',
    'zlib'
}


def scan_project_directory(project_path: str) -> List[Path]:
    """
    扫描项目目录，找出所有Python文件
    
    Args:
        project_path: 项目目录路径
    
    Returns:
        List[Path]: Python文件路径列表
    """
    python_files = []
    project_path = Path(project_path)
    
    # 忽略的目录
    ignore_dirs = {'.git', '__pycache__', '.pytest_cache', 'venv', 'env', 
                   'node_modules', '.tox', 'build', 'dist', '.egg-info'}
    
    for root, dirs, files in os.walk(project_path):
        # 过滤掉忽略的目录
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(Path(root) / file)
    
    return python_files


def extract_imports(file_path: Path) -> Set[str]:
    """
    从Python文件中提取import语句
    
    Args:
        file_path: Python文件路径
    
    Returns:
        Set[str]: 导入的模块名集合
    """
    imports = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析AST
        tree = ast.parse(content)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    # 获取顶级模块名
                    module_name = alias.name.split('.')[0]
                    imports.add(module_name)
            
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    # 获取顶级模块名
                    module_name = node.module.split('.')[0]
                    imports.add(module_name)
    
    except (SyntaxError, UnicodeDecodeError, FileNotFoundError) as e:
        print(f"警告：无法解析文件 {file_path}: {e}")
    
    return imports


def filter_third_party_packages(imports: Set[str]) -> Set[str]:
    """
    过滤出第三方库依赖
    
    Args:
        imports: 所有导入的模块名
    
    Returns:
        Set[str]: 第三方库依赖集合
    """
    third_party = set()
    
    for module in imports:
        # 跳过标准库模块
        if module in STANDARD_LIBRARY:
            continue
        
        # 跳过相对导入和本地模块（通常以项目名开头）
        if module.startswith('.'):
            continue
        
        # 跳过一些常见的本地模块模式
        if module in {'main', 'app', 'config', 'models', 'views', 'utils', 'tests'}:
            continue
        
        third_party.add(module)
    
    return third_party


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
    try:
        if project_name is None:
            project_name = Path(project_path).name
        
        # 生成pyproject.toml内容
        toml_content = f'''[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{project_name}"
version = "0.1.0"
description = "A Python project"
readme = "README.md"
requires-python = ">=3.8"
authors = [
    {{name = "Your Name", email = "your.email@example.com"}}
]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
dependencies = [
'''
        
        # 添加依赖
        for dep in sorted(dependencies):
            toml_content += f'    "{dep}",\n'
        
        toml_content += ''']

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=22.0",
    "flake8>=5.0",
    "mypy>=1.0",
]

[project.urls]
"Homepage" = "https://github.com/yourusername/''' + project_name + '''"
"Bug Reports" = "https://github.com/yourusername/''' + project_name + '''/issues"
"Source" = "https://github.com/yourusername/''' + project_name + '''"

[tool.setuptools.packages.find]
where = ["src"]
include = ["''' + project_name + '''*"]

[tool.black]
line-length = 88
target-version = ['py38']

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
'''
        
        # 写入文件
        toml_path = Path(project_path) / 'pyproject.toml'
        with open(toml_path, 'w', encoding='utf-8') as f:
            f.write(toml_content)
        
        print(f"✅ pyproject.toml文件已生成：{toml_path}")
        return True
    
    except Exception as e:
        print(f"❌ 生成pyproject.toml失败：{e}")
        return False


def install_dependencies_with_uv(project_path: str) -> bool:
    """
    使用uv安装依赖
    
    Args:
        project_path: 项目目录路径
    
    Returns:
        bool: 安装成功返回True，失败返回False
    """
    try:
        # 检查uv是否可用
        result = subprocess.run(['uv', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ uv未安装，尝试使用pip安装依赖")
            return install_dependencies_with_pip(project_path)
        
        print("使用uv安装依赖...")
        
        # 使用uv安装依赖
        result = subprocess.run(
            ['uv', 'pip', 'install', '-e', '.'],
            cwd=project_path,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ 依赖安装完成")
            return True
        else:
            print(f"❌ uv安装失败：{result.stderr}")
            return False
    
    except FileNotFoundError:
        print("❌ uv未找到，尝试使用pip安装依赖")
        return install_dependencies_with_pip(project_path)
    except Exception as e:
        print(f"❌ uv安装失败：{e}")
        return False


def install_dependencies_with_pip(project_path: str) -> bool:
    """
    使用pip安装依赖
    
    Args:
        project_path: 项目目录路径
    
    Returns:
        bool: 安装成功返回True，失败返回False
    """
    try:
        print("使用pip安装依赖...")
        
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '-e', '.'],
            cwd=project_path,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ 依赖安装完成")
            return True
        else:
            print(f"❌ pip安装失败：{result.stderr}")
            return False
    
    except Exception as e:
        print(f"❌ pip安装失败：{e}")
        return False


def verify_dependencies(dependencies: Set[str]) -> Dict[str, bool]:
    """
    验证依赖安装是否成功
    
    Args:
        dependencies: 依赖集合
    
    Returns:
        Dict[str, bool]: 每个依赖的验证结果
    """
    results = {}
    
    for dep in dependencies:
        try:
            __import__(dep)
            results[dep] = True
        except ImportError:
            results[dep] = False
    
    return results


def main():
    """
    主函数：执行依赖管理任务
    """
    print("Session25 练习题2：依赖管理")
    print("=" * 40)
    
    # 获取项目目录路径（这里使用当前目录作为示例）
    project_path = os.getcwd()
    print(f"项目目录：{project_path}")
    
    # 1. 扫描项目目录
    print("\n1. 扫描项目目录...")
    python_files = scan_project_directory(project_path)
    print(f"✅ 扫描项目目录完成，找到{len(python_files)}个Python文件")
    
    if not python_files:
        print("❌ 未找到Python文件")
        return
    
    # 2. 提取和分析import语句
    print("\n2. 分析import语句...")
    all_imports = set()
    
    for file_path in python_files:
        file_imports = extract_imports(file_path)
        all_imports.update(file_imports)
    
    # 过滤第三方依赖
    third_party_deps = filter_third_party_packages(all_imports)
    
    print(f"✅ 分析import语句完成，识别出以下依赖：")
    if third_party_deps:
        for dep in sorted(third_party_deps):
            print(f"   - {dep}")
    else:
        print("   - 未发现第三方依赖")
    
    # 3. 生成pyproject.toml
    print("\n3. 生成pyproject.toml文件...")
    if generate_pyproject_toml(project_path, third_party_deps):
        print("✅ pyproject.toml文件生成成功")
    else:
        print("❌ pyproject.toml文件生成失败")
        return
    
    # 4. 安装依赖
    if third_party_deps:
        print("\n4. 安装依赖...")
        if install_dependencies_with_uv(project_path):
            print("✅ 依赖安装成功")
        else:
            print("❌ 依赖安装失败")
            return
        
        # 5. 验证依赖安装
        print("\n5. 验证依赖安装...")
        verification_results = verify_dependencies(third_party_deps)
        
        all_verified = True
        for dep, verified in verification_results.items():
            if verified:
                print(f"✅ {dep} 验证通过")
            else:
                print(f"❌ {dep} 验证失败")
                all_verified = False
        
        if all_verified:
            print("✅ 验证依赖安装：所有依赖均已成功安装")
        else:
            print("❌ 部分依赖安装验证失败")
    else:
        print("\n4. 跳过依赖安装（无第三方依赖）")
    
    print("\n" + "=" * 40)
    print("依赖管理任务完成！")


if __name__ == "__main__":
    main()