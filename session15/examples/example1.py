#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1：数据库连接和表创建
学习如何连接SQLite数据库并创建表
"""

import sqlite3
import os

def basic_database_operations():
    """基本的数据库操作示例"""
    print("示例1：数据库连接和表创建")
    print("-" * 40)
    
    # 1. 连接到数据库（如果不存在会自动创建）
    conn = sqlite3.connect('example1.db')
    print("✓ 成功连接到数据库")
    
    # 2. 创建游标对象
    cursor = conn.cursor()
    
    # 3. 创建表
    # 创建产品表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER DEFAULT 0
    )
    ''')
    print("✓ 产品表创建成功")
    
    # 创建客户表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        phone TEXT
    )
    ''')
    print("✓ 客户表创建成功")
    
    # 4. 查看数据库中的所有表
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("\n数据库中的表：")
    for table in tables:
        print(f"  - {table[0]}")
    
    # 5. 查看表结构
    print("\n产品表结构：")
    cursor.execute("PRAGMA table_info(products)")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    # 6. 提交更改并关闭连接
    conn.commit()
    conn.close()
    print("\n✓ 数据库连接已关闭")
    
    # 清理：删除示例数据库
    if os.path.exists('example1.db'):
        os.remove('example1.db')
        print("✓ 示例数据库已清理")

def connection_best_practices():
    """数据库连接的最佳实践"""
    print("\n\n使用上下文管理器的最佳实践：")
    print("-" * 40)
    
    # 使用with语句自动管理连接
    with sqlite3.connect('example1_best.db') as conn:
        cursor = conn.cursor()
        
        # 执行数据库操作
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 插入数据
        users = [
            ('alice',),
            ('bob',),
            ('charlie',)
        ]
        cursor.executemany('INSERT OR IGNORE INTO users (username) VALUES (?)', users)
        
        # 查询数据
        cursor.execute('SELECT * FROM users')
        print("用户列表：")
        for user in cursor.fetchall():
            print(f"  ID: {user[0]}, 用户名: {user[1]}, 创建时间: {user[2]}")
    
    # 连接会自动关闭
    print("✓ 使用with语句，连接自动关闭")
    
    # 清理
    if os.path.exists('example1_best.db'):
        os.remove('example1_best.db')

if __name__ == "__main__":
    # 运行示例
    basic_database_operations()
    connection_best_practices()
    
    print("\n" + "="*50)
    print("提示：")
    print("1. SQLite数据库是一个文件，非常轻量")
    print("2. 使用with语句可以自动管理连接")
    print("3. 记得提交(commit)才能保存更改")
    print("4. PRIMARY KEY会自动创建索引") 