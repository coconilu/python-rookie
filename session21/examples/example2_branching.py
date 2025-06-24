#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session21 示例2：Git分支管理

本示例演示了Git分支的创建、切换、合并等操作：
1. 创建和切换分支
2. 在不同分支上开发
3. 合并分支
4. 解决冲突

作者: Python教程团队
创建日期: 2024-01-20
"""

import os
import subprocess
from pathlib import Path
import shutil


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
        if e.stderr:
            print(f"错误: {e.stderr}")
        return None


def setup_demo_repo():
    """
    设置演示仓库
    """
    demo_dir = Path("git_branch_demo")
    if demo_dir.exists():
        shutil.rmtree(demo_dir)
    
    demo_dir.mkdir()
    os.chdir(demo_dir)
    
    # 初始化仓库
    run_git_command("git init")
    run_git_command("git config user.name 'Demo User'")
    run_git_command("git config user.email 'demo@example.com'")
    
    # 创建初始文件
    with open("app.py", "w", encoding="utf-8") as f:
        f.write('''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的Web应用
"""

class WebApp:
    def __init__(self):
        self.routes = {}
        self.middleware = []
    
    def route(self, path):
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator
    
    def run(self, host="localhost", port=8000):
        print(f"应用运行在 http://{host}:{port}")
        print("可用路由:")
        for path in self.routes:
            print(f"  {path}")

app = WebApp()

@app.route("/")
def home():
    return "欢迎访问我的网站！"

if __name__ == "__main__":
    app.run()
''')
    
    run_git_command("git add app.py")
    run_git_command("git commit -m 'Initial commit: 基础Web应用'")
    
    return demo_dir


def demo_feature_branch():
    """
    演示功能分支开发
    """
    print("\n=== 功能分支开发 ===")
    
    # 1. 查看当前分支
    print("\n1. 查看当前分支")
    print("$ git branch")
    output = run_git_command("git branch")
    print(output if output else "* main")
    
    # 2. 创建并切换到功能分支
    print("\n2. 创建用户认证功能分支")
    print("$ git checkout -b feature/user-auth")
    output = run_git_command("git checkout -b feature/user-auth")
    print(output)
    
    # 3. 在功能分支上开发
    print("\n3. 开发用户认证功能")
    with open("auth.py", "w", encoding="utf-8") as f:
        f.write('''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户认证模块
"""

import hashlib
import secrets

class UserAuth:
    def __init__(self):
        self.users = {}
        self.sessions = {}
    
    def hash_password(self, password):
        """密码哈希"""
        salt = secrets.token_hex(16)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', 
                                       password.encode('utf-8'), 
                                       salt.encode('utf-8'), 
                                       100000)
        return salt + pwd_hash.hex()
    
    def verify_password(self, password, hashed):
        """验证密码"""
        salt = hashed[:32]
        stored_hash = hashed[32:]
        pwd_hash = hashlib.pbkdf2_hmac('sha256',
                                       password.encode('utf-8'),
                                       salt.encode('utf-8'),
                                       100000)
        return pwd_hash.hex() == stored_hash
    
    def register(self, username, password, email):
        """用户注册"""
        if username in self.users:
            return False, "用户名已存在"
        
        self.users[username] = {
            'password': self.hash_password(password),
            'email': email,
            'active': True
        }
        return True, "注册成功"
    
    def login(self, username, password):
        """用户登录"""
        if username not in self.users:
            return False, "用户不存在"
        
        user = self.users[username]
        if not user['active']:
            return False, "账户已被禁用"
        
        if self.verify_password(password, user['password']):
            session_id = secrets.token_urlsafe(32)
            self.sessions[session_id] = username
            return True, session_id
        
        return False, "密码错误"
    
    def logout(self, session_id):
        """用户登出"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

def main():
    auth = UserAuth()
    
    # 测试注册
    success, msg = auth.register("alice", "password123", "alice@example.com")
    print(f"注册结果: {msg}")
    
    # 测试登录
    success, result = auth.login("alice", "password123")
    if success:
        print(f"登录成功，会话ID: {result[:10]}...")
        
        # 测试登出
        auth.logout(result)
        print("已登出")
    else:
        print(f"登录失败: {result}")

if __name__ == "__main__":
    main()
''')
    
    print("创建了 auth.py 文件")
    
    # 4. 提交功能
    print("\n4. 提交用户认证功能")
    print("$ git add auth.py")
    run_git_command("git add auth.py")
    
    print("$ git commit -m '添加用户认证模块'")
    output = run_git_command("git commit -m '添加用户认证模块'")
    print(output)
    
    # 5. 修改主应用文件
    print("\n5. 集成认证功能到主应用")
    with open("app.py", "a", encoding="utf-8") as f:
        f.write('''

# 集成用户认证
from auth import UserAuth

auth = UserAuth()

@app.route("/register")
def register():
    return "用户注册页面"

@app.route("/login")
def login():
    return "用户登录页面"

@app.route("/profile")
def profile():
    return "用户个人资料页面"
''')
    
    print("$ git add app.py")
    run_git_command("git add app.py")
    
    print("$ git commit -m '集成用户认证到主应用'")
    output = run_git_command("git commit -m '集成用户认证到主应用'")
    print(output)


def demo_another_feature():
    """
    演示另一个功能分支
    """
    print("\n=== 开发另一个功能 ===")
    
    # 1. 切换回主分支
    print("\n1. 切换回主分支")
    print("$ git checkout main")
    output = run_git_command("git checkout main")
    print(output)
    
    # 2. 创建数据库功能分支
    print("\n2. 创建数据库功能分支")
    print("$ git checkout -b feature/database")
    output = run_git_command("git checkout -b feature/database")
    print(output)
    
    # 3. 开发数据库功能
    print("\n3. 开发数据库功能")
    with open("database.py", "w", encoding="utf-8") as f:
        f.write('''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库操作模块
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

class Database:
    def __init__(self, db_path="app.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 创建用户表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            # 创建会话表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    user_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # 创建日志表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    level TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()
    
    def create_user(self, username, email, password_hash):
        """创建用户"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                    (username, email, password_hash)
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
    
    def get_user(self, username):
        """获取用户信息"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            )
            return cursor.fetchone()
    
    def create_session(self, session_id, user_id, expires_at):
        """创建会话"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sessions (id, user_id, expires_at) VALUES (?, ?, ?)",
                (session_id, user_id, expires_at)
            )
            conn.commit()
    
    def log_event(self, level, message, user_id=None):
        """记录日志"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO logs (level, message, user_id) VALUES (?, ?, ?)",
                (level, message, user_id)
            )
            conn.commit()
    
    def get_recent_logs(self, limit=50):
        """获取最近的日志"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM logs ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            )
            return cursor.fetchall()

def main():
    # 测试数据库功能
    db = Database(":memory:")  # 使用内存数据库进行测试
    
    # 测试用户创建
    user_id = db.create_user("testuser", "test@example.com", "hashed_password")
    print(f"创建用户，ID: {user_id}")
    
    # 测试用户查询
    user = db.get_user("testuser")
    print(f"查询用户: {user}")
    
    # 测试日志记录
    db.log_event("INFO", "用户注册", user_id)
    db.log_event("INFO", "用户登录", user_id)
    
    # 查看日志
    logs = db.get_recent_logs(10)
    print("最近日志:")
    for log in logs:
        print(f"  {log}")

if __name__ == "__main__":
    main()
''')
    
    print("创建了 database.py 文件")
    
    # 4. 提交数据库功能
    print("\n4. 提交数据库功能")
    print("$ git add database.py")
    run_git_command("git add database.py")
    
    print("$ git commit -m '添加数据库操作模块'")
    output = run_git_command("git commit -m '添加数据库操作模块'")
    print(output)


def demo_merge_branches():
    """
    演示分支合并
    """
    print("\n=== 合并分支 ===")
    
    # 1. 切换到主分支
    print("\n1. 切换到主分支")
    print("$ git checkout main")
    output = run_git_command("git checkout main")
    print(output)
    
    # 2. 查看所有分支
    print("\n2. 查看所有分支")
    print("$ git branch")
    output = run_git_command("git branch")
    print(output)
    
    # 3. 合并用户认证分支
    print("\n3. 合并用户认证分支")
    print("$ git merge feature/user-auth")
    output = run_git_command("git merge feature/user-auth")
    print(output)
    
    # 4. 合并数据库分支
    print("\n4. 合并数据库分支")
    print("$ git merge feature/database")
    output = run_git_command("git merge feature/database")
    print(output)
    
    # 5. 查看合并后的文件
    print("\n5. 查看合并后的项目文件")
    files = list(Path(".").glob("*.py"))
    for file in files:
        print(f"  {file.name}")
    
    # 6. 查看提交历史
    print("\n6. 查看提交历史")
    print("$ git log --oneline --graph")
    output = run_git_command("git log --oneline --graph")
    print(output)
    
    # 7. 删除已合并的分支
    print("\n7. 清理已合并的分支")
    print("$ git branch -d feature/user-auth")
    output = run_git_command("git branch -d feature/user-auth")
    print(output)
    
    print("$ git branch -d feature/database")
    output = run_git_command("git branch -d feature/database")
    print(output)
    
    # 8. 查看最终分支状态
    print("\n8. 最终分支状态")
    print("$ git branch")
    output = run_git_command("git branch")
    print(output)


def branching_demo():
    """
    运行完整的分支管理演示
    """
    print("Git分支管理演示")
    print("=" * 50)
    
    try:
        # 设置演示仓库
        demo_dir = setup_demo_repo()
        
        # 演示功能分支开发
        demo_feature_branch()
        
        # 演示另一个功能分支
        demo_another_feature()
        
        # 演示分支合并
        demo_merge_branches()
        
        print("\n=== 演示完成 ===")
        print("\n学到的分支管理技能:")
        print("1. 创建和切换分支")
        print("2. 在不同分支上并行开发")
        print("3. 合并分支")
        print("4. 清理已合并的分支")
        print("5. 查看分支历史")
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
    finally:
        # 返回上级目录
        os.chdir("..")


if __name__ == "__main__":
    branching_demo()