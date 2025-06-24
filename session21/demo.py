#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session21: 版本控制 - Git 演示代码

本文件演示了Git的基本操作和工作流程，包括：
1. Git仓库的初始化和配置
2. 文件的添加、提交和历史查看
3. 分支的创建、切换和合并
4. 模拟团队协作开发流程

作者: Python教程团队
创建日期: 2024-01-20
最后修改: 2024-01-20
"""

import os
import subprocess
import sys
from pathlib import Path
import tempfile
import shutil
from typing import List, Optional


class GitDemo:
    """
    Git操作演示类
    
    提供Git基本操作的演示和教学功能
    """
    
    def __init__(self, demo_dir: Optional[str] = None):
        """
        初始化Git演示环境
        
        Args:
            demo_dir: 演示目录路径，如果为None则创建临时目录
        """
        if demo_dir:
            self.demo_dir = Path(demo_dir)
        else:
            self.demo_dir = Path(tempfile.mkdtemp(prefix="git_demo_"))
        
        self.original_dir = Path.cwd()
        print(f"Git演示目录: {self.demo_dir}")
    
    def run_git_command(self, command: List[str], capture_output: bool = True) -> str:
        """
        执行Git命令
        
        Args:
            command: Git命令列表
            capture_output: 是否捕获输出
            
        Returns:
            命令输出结果
        """
        try:
            if capture_output:
                result = subprocess.run(
                    command,
                    cwd=self.demo_dir,
                    capture_output=True,
                    text=True,
                    check=True
                )
                return result.stdout.strip()
            else:
                subprocess.run(
                    command,
                    cwd=self.demo_dir,
                    check=True
                )
                return ""
        except subprocess.CalledProcessError as e:
            print(f"命令执行失败: {' '.join(command)}")
            print(f"错误信息: {e.stderr if e.stderr else str(e)}")
            return ""
    
    def print_section(self, title: str):
        """
        打印章节标题
        """
        print(f"\n{'='*60}")
        print(f" {title}")
        print(f"{'='*60}")
    
    def print_command(self, command: str, description: str = ""):
        """
        打印命令信息
        """
        print(f"\n$ {command}")
        if description:
            print(f"  # {description}")
    
    def demo_git_init(self):
        """
        演示Git仓库初始化
        """
        self.print_section("1. Git仓库初始化")
        
        # 创建演示目录
        os.makedirs(self.demo_dir, exist_ok=True)
        os.chdir(self.demo_dir)
        
        # 初始化Git仓库
        self.print_command("git init", "初始化Git仓库")
        output = self.run_git_command(["git", "init"])
        print(output)
        
        # 配置用户信息
        self.print_command("git config user.name 'Demo User'", "设置用户名")
        self.run_git_command(["git", "config", "user.name", "Demo User"])
        
        self.print_command("git config user.email 'demo@example.com'", "设置邮箱")
        self.run_git_command(["git", "config", "user.email", "demo@example.com"])
        
        # 查看仓库状态
        self.print_command("git status", "查看仓库状态")
        output = self.run_git_command(["git", "status"])
        print(output)
    
    def demo_basic_operations(self):
        """
        演示Git基本操作
        """
        self.print_section("2. Git基本操作")
        
        # 创建第一个文件
        readme_content = """# 我的第一个Git项目

这是一个学习Git的演示项目。

## 功能
- 学习Git基本操作
- 理解版本控制概念
- 掌握协作开发流程
"""
        
        readme_path = self.demo_dir / "README.md"
        readme_path.write_text(readme_content, encoding='utf-8')
        print(f"创建文件: {readme_path.name}")
        
        # 查看状态
        self.print_command("git status", "查看文件状态")
        output = self.run_git_command(["git", "status"])
        print(output)
        
        # 添加文件到暂存区
        self.print_command("git add README.md", "添加文件到暂存区")
        self.run_git_command(["git", "add", "README.md"])
        
        # 再次查看状态
        self.print_command("git status", "查看暂存区状态")
        output = self.run_git_command(["git", "status"])
        print(output)
        
        # 提交文件
        self.print_command("git commit -m 'Initial commit: 添加README文件'", "提交文件")
        output = self.run_git_command(["git", "commit", "-m", "Initial commit: 添加README文件"])
        print(output)
        
        # 查看提交历史
        self.print_command("git log --oneline", "查看提交历史")
        output = self.run_git_command(["git", "log", "--oneline"])
        print(output)
    
    def demo_file_modifications(self):
        """
        演示文件修改和版本管理
        """
        self.print_section("3. 文件修改和版本管理")
        
        # 创建Python文件
        python_content = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
我的第一个Python程序
"""

def main():
    print("Hello, Git!")
    print("这是我的第一个版本控制的Python程序")

if __name__ == "__main__":
    main()
"""
        
        python_path = self.demo_dir / "main.py"
        python_path.write_text(python_content, encoding='utf-8')
        print(f"创建文件: {python_path.name}")
        
        # 添加并提交Python文件
        self.print_command("git add main.py", "添加Python文件")
        self.run_git_command(["git", "add", "main.py"])
        
        self.print_command("git commit -m '添加主程序文件'", "提交Python文件")
        self.run_git_command(["git", "commit", "-m", "添加主程序文件"])
        
        # 修改文件
        modified_content = python_content.replace(
            'print("Hello, Git!")',
            'print("Hello, Git!\\nWelcome to version control!")'
        )
        python_path.write_text(modified_content, encoding='utf-8')
        print("\n修改了main.py文件")
        
        # 查看差异
        self.print_command("git diff", "查看文件差异")
        output = self.run_git_command(["git", "diff"])
        print(output)
        
        # 提交修改
        self.print_command("git add main.py", "暂存修改")
        self.run_git_command(["git", "add", "main.py"])
        
        self.print_command("git commit -m '改进程序输出信息'", "提交修改")
        self.run_git_command(["git", "commit", "-m", "改进程序输出信息"])
        
        # 查看提交历史
        self.print_command("git log --oneline", "查看提交历史")
        output = self.run_git_command(["git", "log", "--oneline"])
        print(output)
    
    def demo_branching(self):
        """
        演示分支操作
        """
        self.print_section("4. 分支操作")
        
        # 查看当前分支
        self.print_command("git branch", "查看当前分支")
        output = self.run_git_command(["git", "branch"])
        print(output)
        
        # 创建新分支
        self.print_command("git checkout -b feature/add-calculator", "创建并切换到新分支")
        output = self.run_git_command(["git", "checkout", "-b", "feature/add-calculator"])
        print(output)
        
        # 在新分支上开发功能
        calculator_content = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单计算器模块
"""

def add(a, b):
    """加法运算"""
    return a + b

def subtract(a, b):
    """减法运算"""
    return a - b

def multiply(a, b):
    """乘法运算"""
    return a * b

def divide(a, b):
    """除法运算"""
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b

def main():
    print("简单计算器")
    print("支持的操作: +, -, *, /")
    
    try:
        a = float(input("请输入第一个数字: "))
        op = input("请输入操作符 (+, -, *, /): ")
        b = float(input("请输入第二个数字: "))
        
        if op == '+':
            result = add(a, b)
        elif op == '-':
            result = subtract(a, b)
        elif op == '*':
            result = multiply(a, b)
        elif op == '/':
            result = divide(a, b)
        else:
            print("不支持的操作符")
            return
        
        print(f"结果: {a} {op} {b} = {result}")
    
    except ValueError as e:
        print(f"错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")

if __name__ == "__main__":
    main()
"""
        
        calc_path = self.demo_dir / "calculator.py"
        calc_path.write_text(calculator_content, encoding='utf-8')
        print(f"创建文件: {calc_path.name}")
        
        # 提交新功能
        self.print_command("git add calculator.py", "添加计算器文件")
        self.run_git_command(["git", "add", "calculator.py"])
        
        self.print_command("git commit -m '添加计算器功能'", "提交新功能")
        self.run_git_command(["git", "commit", "-m", "添加计算器功能"])
        
        # 切换回主分支
        self.print_command("git checkout main", "切换回主分支")
        output = self.run_git_command(["git", "checkout", "main"])
        print(output)
        
        # 查看文件（计算器文件不存在）
        print("\n当前目录文件:")
        for file in self.demo_dir.iterdir():
            if file.is_file() and not file.name.startswith('.'):
                print(f"  {file.name}")
        
        # 合并分支
        self.print_command("git merge feature/add-calculator", "合并功能分支")
        output = self.run_git_command(["git", "merge", "feature/add-calculator"])
        print(output)
        
        # 查看合并后的文件
        print("\n合并后的文件:")
        for file in self.demo_dir.iterdir():
            if file.is_file() and not file.name.startswith('.'):
                print(f"  {file.name}")
        
        # 删除已合并的分支
        self.print_command("git branch -d feature/add-calculator", "删除已合并的分支")
        output = self.run_git_command(["git", "branch", "-d", "feature/add-calculator"])
        print(output)
        
        # 查看最终的提交历史
        self.print_command("git log --oneline --graph", "查看提交历史图")
        output = self.run_git_command(["git", "log", "--oneline", "--graph"])
        print(output)
    
    def demo_gitignore(self):
        """
        演示.gitignore的使用
        """
        self.print_section("5. .gitignore文件")
        
        # 创建一些应该被忽略的文件
        (self.demo_dir / "__pycache__").mkdir(exist_ok=True)
        (self.demo_dir / "__pycache__" / "main.cpython-39.pyc").write_text("compiled code")
        (self.demo_dir / "config.ini").write_text("[database]\npassword=secret123")
        (self.demo_dir / "debug.log").write_text("DEBUG: Application started")
        
        print("创建了一些临时文件...")
        
        # 查看状态（会显示这些文件）
        self.print_command("git status", "查看状态（包含临时文件）")
        output = self.run_git_command(["git", "status"])
        print(output)
        
        # 创建.gitignore文件
        gitignore_content = """# Python编译文件
__pycache__/
*.py[cod]
*.pyo
*.pyd

# 配置文件
config.ini
*.conf

# 日志文件
*.log

# 临时文件
*.tmp
*.temp

# IDE文件
.vscode/
.idea/

# 操作系统文件
.DS_Store
Thumbs.db
"""
        
        gitignore_path = self.demo_dir / ".gitignore"
        gitignore_path.write_text(gitignore_content, encoding='utf-8')
        print(f"创建文件: {gitignore_path.name}")
        
        # 再次查看状态（临时文件被忽略）
        self.print_command("git status", "查看状态（临时文件被忽略）")
        output = self.run_git_command(["git", "status"])
        print(output)
        
        # 提交.gitignore
        self.print_command("git add .gitignore", "添加.gitignore文件")
        self.run_git_command(["git", "add", ".gitignore"])
        
        self.print_command("git commit -m '添加.gitignore文件'", "提交.gitignore")
        self.run_git_command(["git", "commit", "-m", "添加.gitignore文件"])
    
    def demo_collaboration_workflow(self):
        """
        演示协作开发工作流程
        """
        self.print_section("6. 协作开发工作流程模拟")
        
        print("模拟场景: 两个开发者协作开发")
        print("开发者A: 添加用户管理功能")
        print("开发者B: 添加数据验证功能")
        
        # 开发者A的工作
        print("\n--- 开发者A的工作 ---")
        
        # 创建用户管理分支
        self.print_command("git checkout -b feature/user-management", "创建用户管理分支")
        self.run_git_command(["git", "checkout", "-b", "feature/user-management"])
        
        # 添加用户管理功能
        user_mgmt_content = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户管理模块
"""

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.is_active = True
    
    def __str__(self):
        return f"User(username='{self.username}', email='{self.email}')"

class UserManager:
    def __init__(self):
        self.users = {}
    
    def add_user(self, username, email):
        if username in self.users:
            raise ValueError(f"用户 {username} 已存在")
        
        user = User(username, email)
        self.users[username] = user
        return user
    
    def get_user(self, username):
        return self.users.get(username)
    
    def list_users(self):
        return list(self.users.values())
    
    def deactivate_user(self, username):
        user = self.get_user(username)
        if user:
            user.is_active = False
            return True
        return False

def main():
    manager = UserManager()
    
    # 添加一些用户
    manager.add_user("alice", "alice@example.com")
    manager.add_user("bob", "bob@example.com")
    
    # 列出所有用户
    print("所有用户:")
    for user in manager.list_users():
        print(f"  {user}")

if __name__ == "__main__":
    main()
"""
        
        user_path = self.demo_dir / "user_management.py"
        user_path.write_text(user_mgmt_content, encoding='utf-8')
        
        self.print_command("git add user_management.py", "添加用户管理文件")
        self.run_git_command(["git", "add", "user_management.py"])
        
        self.print_command("git commit -m '添加用户管理功能'", "提交用户管理功能")
        self.run_git_command(["git", "commit", "-m", "添加用户管理功能"])
        
        # 切换回主分支
        self.print_command("git checkout main", "切换回主分支")
        self.run_git_command(["git", "checkout", "main"])
        
        # 开发者B的工作
        print("\n--- 开发者B的工作 ---")
        
        # 创建数据验证分支
        self.print_command("git checkout -b feature/data-validation", "创建数据验证分支")
        self.run_git_command(["git", "checkout", "-b", "feature/data-validation"])
        
        # 添加数据验证功能
        validation_content = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据验证模块
"""

import re

def validate_email(email):
    """
    验证邮箱格式
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username):
    """
    验证用户名格式
    - 长度3-20字符
    - 只能包含字母、数字和下划线
    - 必须以字母开头
    """
    if not username or len(username) < 3 or len(username) > 20:
        return False
    
    if not username[0].isalpha():
        return False
    
    return all(c.isalnum() or c == '_' for c in username)

def validate_password(password):
    """
    验证密码强度
    - 至少8个字符
    - 包含大小写字母
    - 包含数字
    - 包含特殊字符
    """
    if len(password) < 8:
        return False, "密码长度至少8个字符"
    
    if not any(c.isupper() for c in password):
        return False, "密码必须包含大写字母"
    
    if not any(c.islower() for c in password):
        return False, "密码必须包含小写字母"
    
    if not any(c.isdigit() for c in password):
        return False, "密码必须包含数字"
    
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(c in special_chars for c in password):
        return False, "密码必须包含特殊字符"
    
    return True, "密码强度合格"

def main():
    # 测试验证功能
    test_emails = ["user@example.com", "invalid-email", "test@domain.co.uk"]
    test_usernames = ["alice", "user123", "123invalid", "a", "valid_user_name"]
    test_passwords = ["weak", "StrongPass123!", "NoSpecial123", "noUPPER123!"]
    
    print("邮箱验证测试:")
    for email in test_emails:
        result = validate_email(email)
        print(f"  {email}: {'✓' if result else '✗'}")
    
    print("\n用户名验证测试:")
    for username in test_usernames:
        result = validate_username(username)
        print(f"  {username}: {'✓' if result else '✗'}")
    
    print("\n密码验证测试:")
    for password in test_passwords:
        is_valid, message = validate_password(password)
        print(f"  {password}: {'✓' if is_valid else '✗'} - {message}")

if __name__ == "__main__":
    main()
"""
        
        validation_path = self.demo_dir / "data_validation.py"
        validation_path.write_text(validation_content, encoding='utf-8')
        
        self.print_command("git add data_validation.py", "添加数据验证文件")
        self.run_git_command(["git", "add", "data_validation.py"])
        
        self.print_command("git commit -m '添加数据验证功能'", "提交数据验证功能")
        self.run_git_command(["git", "commit", "-m", "添加数据验证功能"])
        
        # 合并两个功能分支
        print("\n--- 合并功能分支 ---")
        
        # 切换到主分支并合并用户管理功能
        self.print_command("git checkout main", "切换到主分支")
        self.run_git_command(["git", "checkout", "main"])
        
        self.print_command("git merge feature/user-management", "合并用户管理功能")
        output = self.run_git_command(["git", "merge", "feature/user-management"])
        print(output)
        
        self.print_command("git merge feature/data-validation", "合并数据验证功能")
        output = self.run_git_command(["git", "merge", "feature/data-validation"])
        print(output)
        
        # 清理分支
        self.print_command("git branch -d feature/user-management", "删除用户管理分支")
        self.run_git_command(["git", "branch", "-d", "feature/user-management"])
        
        self.print_command("git branch -d feature/data-validation", "删除数据验证分支")
        self.run_git_command(["git", "branch", "-d", "feature/data-validation"])
        
        # 查看最终结果
        self.print_command("git log --oneline --graph", "查看完整的提交历史")
        output = self.run_git_command(["git", "log", "--oneline", "--graph"])
        print(output)
        
        print("\n最终项目文件:")
        for file in sorted(self.demo_dir.iterdir()):
            if file.is_file() and not file.name.startswith('.'):
                print(f"  {file.name}")
    
    def cleanup(self):
        """
        清理演示环境
        """
        os.chdir(self.original_dir)
        if self.demo_dir.exists() and "git_demo_" in str(self.demo_dir):
            shutil.rmtree(self.demo_dir)
            print(f"\n清理演示目录: {self.demo_dir}")
    
    def run_full_demo(self):
        """
        运行完整的Git演示
        """
        try:
            print("Git版本控制系统演示")
            print("=" * 60)
            print("本演示将展示Git的核心功能和工作流程")
            
            # 检查Git是否安装
            try:
                result = subprocess.run(["git", "--version"], capture_output=True, text=True)
                print(f"Git版本: {result.stdout.strip()}")
            except FileNotFoundError:
                print("错误: 未找到Git，请先安装Git")
                return
            
            # 运行各个演示
            self.demo_git_init()
            self.demo_basic_operations()
            self.demo_file_modifications()
            self.demo_branching()
            self.demo_gitignore()
            self.demo_collaboration_workflow()
            
            self.print_section("演示完成")
            print("恭喜！你已经学会了Git的基本操作。")
            print("\n接下来的学习建议:")
            print("1. 在实际项目中使用Git")
            print("2. 学习更高级的Git功能（rebase, cherry-pick等）")
            print("3. 了解Git工作流程（Git Flow, GitHub Flow等）")
            print("4. 使用GitHub/GitLab等平台进行协作开发")
            
        except KeyboardInterrupt:
            print("\n演示被用户中断")
        except Exception as e:
            print(f"\n演示过程中出现错误: {e}")
        finally:
            self.cleanup()


def main():
    """
    主函数：运行Git演示
    """
    print(__doc__)
    
    # 询问用户是否运行演示
    response = input("\n是否运行Git操作演示？(y/n): ").lower().strip()
    
    if response in ['y', 'yes', '是', '']:
        demo = GitDemo()
        demo.run_full_demo()
    else:
        print("演示已取消。")
        print("\n你可以通过以下方式学习Git:")
        print("1. 阅读tutorial.md文档")
        print("2. 查看examples/目录中的示例")
        print("3. 完成exercises/目录中的练习")
        print("4. 参与project/目录中的协作项目")


if __name__ == "__main__":
    main()