#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session21 示例1：Git基本工作流程

本示例演示了Git的基本工作流程：
1. 初始化仓库
2. 添加文件
3. 提交更改
4. 查看历史

作者: Python教程团队
创建日期: 2024-01-20
"""

import os
import subprocess
from pathlib import Path


def run_git_command(command, cwd=None):
    """
    执行Git命令并返回结果
    """
    try:
        result = subprocess.run(
            command.split(),
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {command}")
        print(f"错误: {e.stderr}")
        return None


def basic_git_workflow():
    """
    演示Git基本工作流程
    """
    print("Git基本工作流程演示")
    print("=" * 40)
    
    # 创建演示目录
    demo_dir = Path("git_basic_demo")
    if demo_dir.exists():
        import shutil
        shutil.rmtree(demo_dir)
    
    demo_dir.mkdir()
    os.chdir(demo_dir)
    
    try:
        # 1. 初始化Git仓库
        print("\n1. 初始化Git仓库")
        print("$ git init")
        output = run_git_command("git init")
        print(output)
        
        # 配置用户信息
        run_git_command("git config user.name 'Example User'")
        run_git_command("git config user.email 'user@example.com'")
        
        # 2. 创建第一个文件
        print("\n2. 创建项目文件")
        with open("hello.py", "w", encoding="utf-8") as f:
            f.write('''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
我的第一个Git管理的Python程序
"""

def greet(name="World"):
    """问候函数"""
    return f"Hello, {name}!"

def main():
    print(greet())
    print(greet("Git"))

if __name__ == "__main__":
    main()
''')
        print("创建了 hello.py 文件")
        
        # 3. 查看仓库状态
        print("\n3. 查看仓库状态")
        print("$ git status")
        output = run_git_command("git status")
        print(output)
        
        # 4. 添加文件到暂存区
        print("\n4. 添加文件到暂存区")
        print("$ git add hello.py")
        run_git_command("git add hello.py")
        
        print("$ git status")
        output = run_git_command("git status")
        print(output)
        
        # 5. 提交文件
        print("\n5. 提交文件")
        print("$ git commit -m 'Initial commit: 添加hello.py'")
        output = run_git_command("git commit -m 'Initial commit: 添加hello.py'")
        print(output)
        
        # 6. 修改文件
        print("\n6. 修改文件")
        with open("hello.py", "a", encoding="utf-8") as f:
            f.write("\n# 添加了一些注释\n")
        print("修改了 hello.py 文件")
        
        # 7. 查看差异
        print("\n7. 查看文件差异")
        print("$ git diff")
        output = run_git_command("git diff")
        print(output)
        
        # 8. 提交修改
        print("\n8. 提交修改")
        print("$ git add hello.py")
        run_git_command("git add hello.py")
        
        print("$ git commit -m '添加注释'")
        output = run_git_command("git commit -m '添加注释'")
        print(output)
        
        # 9. 查看提交历史
        print("\n9. 查看提交历史")
        print("$ git log --oneline")
        output = run_git_command("git log --oneline")
        print(output)
        
        print("\n基本工作流程演示完成！")
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
    finally:
        # 返回上级目录
        os.chdir("..")


if __name__ == "__main__":
    basic_git_workflow()