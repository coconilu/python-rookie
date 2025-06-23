#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图书管理系统 - 主程序
一个功能完整的图书管理系统，包含用户管理、图书管理、借阅管理等功能
"""

import sqlite3
import os
import sys
from datetime import datetime, timedelta
from getpass import getpass
import hashlib

class LibrarySystem:
    """图书管理系统主类"""
    
    def __init__(self, db_name='library.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.current_user = None
        self.init_database()
    
    def init_database(self):
        """初始化数据库表"""
        # 启用外键约束
        self.conn.execute('PRAGMA foreign_keys = ON')
        
        # 用户表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            user_type TEXT DEFAULT 'member',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 图书表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            publisher TEXT,
            category TEXT,
            total_copies INTEGER DEFAULT 1,
            available_copies INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 借阅记录表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS borrowings (
            borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            borrow_date DATE DEFAULT CURRENT_DATE,
            due_date DATE NOT NULL,
            return_date DATE,
            status TEXT DEFAULT 'active',
            fine REAL DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (book_id) REFERENCES books(book_id)
        )
        ''')
        
        # 创建索引
        self.cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_borrowings_user 
        ON borrowings(user_id)
        ''')
        
        self.cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_borrowings_book 
        ON borrowings(book_id)
        ''')
        
        self.cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_books_title 
        ON books(title)
        ''')
        
        self.conn.commit()
        
        # 创建默认管理员账户
        self._create_default_admin()
    
    def _create_default_admin(self):
        """创建默认管理员账户"""
        try:
            password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
            self.cursor.execute('''
            INSERT OR IGNORE INTO users (username, password_hash, user_type)
            VALUES ('admin', ?, 'admin')
            ''', (password_hash,))
            self.conn.commit()
        except:
            pass
    
    def hash_password(self, password):
        """密码哈希"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, password, email=None):
        """用户注册"""
        try:
            password_hash = self.hash_password(password)
            self.cursor.execute('''
            INSERT INTO users (username, password_hash, email)
            VALUES (?, ?, ?)
            ''', (username, password_hash, email))
            self.conn.commit()
            print(f"✓ 用户 {username} 注册成功！")
            return True
        except sqlite3.IntegrityError:
            print(f"✗ 用户名 {username} 已存在！")
            return False
    
    def login(self, username, password):
        """用户登录"""
        password_hash = self.hash_password(password)
        self.cursor.execute('''
        SELECT * FROM users 
        WHERE username = ? AND password_hash = ?
        ''', (username, password_hash))
        
        user = self.cursor.fetchone()
        if user:
            self.current_user = user
            print(f"✓ 欢迎回来，{username}！")
            return True
        else:
            print("✗ 用户名或密码错误！")
            return False
    
    def logout(self):
        """用户登出"""
        self.current_user = None
        print("✓ 已退出登录")
    
    def add_book(self, isbn, title, author, publisher=None, category=None, copies=1):
        """添加图书"""
        if not self.current_user or self.current_user['user_type'] != 'admin':
            print("✗ 只有管理员才能添加图书！")
            return False
        
        try:
            self.cursor.execute('''
            INSERT INTO books (isbn, title, author, publisher, category, 
                             total_copies, available_copies)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (isbn, title, author, publisher, category, copies, copies))
            self.conn.commit()
            print(f"✓ 成功添加图书：《{title}》")
            return True
        except sqlite3.IntegrityError:
            print(f"✗ ISBN {isbn} 已存在！")
            return False
    
    def search_books(self, keyword):
        """搜索图书"""
        self.cursor.execute('''
        SELECT * FROM books 
        WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?
        ORDER BY title
        ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
        
        return self.cursor.fetchall()
    
    def borrow_book(self, book_id, days=30):
        """借阅图书"""
        if not self.current_user:
            print("✗ 请先登录！")
            return False
        
        try:
            self.conn.execute('BEGIN')
            
            # 检查图书是否可借
            self.cursor.execute('''
            SELECT available_copies, title FROM books WHERE book_id = ?
            ''', (book_id,))
            
            book = self.cursor.fetchone()
            if not book:
                raise Exception("图书不存在")
            
            if book['available_copies'] <= 0:
                raise Exception(f"《{book['title']}》暂无可借副本")
            
            # 检查用户是否已借此书
            self.cursor.execute('''
            SELECT COUNT(*) FROM borrowings 
            WHERE user_id = ? AND book_id = ? AND status = 'active'
            ''', (self.current_user['user_id'], book_id))
            
            if self.cursor.fetchone()[0] > 0:
                raise Exception("您已借阅此书，请先归还")
            
            # 创建借阅记录
            due_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
            self.cursor.execute('''
            INSERT INTO borrowings (user_id, book_id, due_date)
            VALUES (?, ?, ?)
            ''', (self.current_user['user_id'], book_id, due_date))
            
            # 更新可借数量
            self.cursor.execute('''
            UPDATE books SET available_copies = available_copies - 1
            WHERE book_id = ?
            ''', (book_id,))
            
            self.conn.commit()
            print(f"✓ 成功借阅《{book['title']}》，请于 {due_date} 前归还")
            return True
            
        except Exception as e:
            self.conn.rollback()
            print(f"✗ 借阅失败：{e}")
            return False
    
    def return_book(self, book_id):
        """归还图书"""
        if not self.current_user:
            print("✗ 请先登录！")
            return False
        
        try:
            self.conn.execute('BEGIN')
            
            # 查找借阅记录
            self.cursor.execute('''
            SELECT b.*, books.title 
            FROM borrowings b
            JOIN books ON b.book_id = books.book_id
            WHERE b.user_id = ? AND b.book_id = ? AND b.status = 'active'
            ''', (self.current_user['user_id'], book_id))
            
            borrowing = self.cursor.fetchone()
            if not borrowing:
                raise Exception("未找到此书的借阅记录")
            
            # 计算罚金（如果逾期）
            return_date = datetime.now().date()
            due_date = datetime.strptime(borrowing['due_date'], '%Y-%m-%d').date()
            
            fine = 0
            if return_date > due_date:
                days_overdue = (return_date - due_date).days
                fine = days_overdue * 0.5  # 每天0.5元罚金
            
            # 更新借阅记录
            self.cursor.execute('''
            UPDATE borrowings 
            SET return_date = ?, status = 'returned', fine = ?
            WHERE borrow_id = ?
            ''', (return_date.strftime('%Y-%m-%d'), fine, borrowing['borrow_id']))
            
            # 更新可借数量
            self.cursor.execute('''
            UPDATE books SET available_copies = available_copies + 1
            WHERE book_id = ?
            ''', (book_id,))
            
            self.conn.commit()
            
            print(f"✓ 成功归还《{borrowing['title']}》")
            if fine > 0:
                print(f"⚠️  逾期 {days_overdue} 天，需缴纳罚金 ¥{fine:.2f}")
            
            return True
            
        except Exception as e:
            self.conn.rollback()
            print(f"✗ 归还失败：{e}")
            return False
    
    def view_my_borrowings(self):
        """查看我的借阅记录"""
        if not self.current_user:
            print("✗ 请先登录！")
            return
        
        self.cursor.execute('''
        SELECT b.*, books.title, books.author
        FROM borrowings b
        JOIN books ON b.book_id = books.book_id
        WHERE b.user_id = ?
        ORDER BY b.borrow_date DESC
        ''', (self.current_user['user_id'],))
        
        borrowings = self.cursor.fetchall()
        
        if not borrowings:
            print("\n暂无借阅记录")
            return
        
        print("\n我的借阅记录：")
        print("-" * 100)
        print(f"{'书名':<30} {'作者':<20} {'借阅日期':<12} {'应还日期':<12} {'状态':<10} {'罚金':<10}")
        print("-" * 100)
        
        for b in borrowings:
            status = '已归还' if b['status'] == 'returned' else '借阅中'
            fine = f"¥{b['fine']:.2f}" if b['fine'] > 0 else '-'
            print(f"{b['title']:<30} {b['author']:<20} {b['borrow_date']:<12} "
                  f"{b['due_date']:<12} {status:<10} {fine:<10}")
    
    def view_popular_books(self):
        """查看热门图书"""
        self.cursor.execute('''
        SELECT b.*, COUNT(br.borrow_id) as borrow_count
        FROM books b
        LEFT JOIN borrowings br ON b.book_id = br.book_id
        GROUP BY b.book_id
        ORDER BY borrow_count DESC
        LIMIT 10
        ''')
        
        books = self.cursor.fetchall()
        
        print("\n📚 热门图书TOP 10：")
        print("-" * 80)
        print(f"{'排名':<5} {'书名':<30} {'作者':<20} {'借阅次数':<10} {'可借':<10}")
        print("-" * 80)
        
        for idx, book in enumerate(books, 1):
            available = f"{book['available_copies']}/{book['total_copies']}"
            print(f"{idx:<5} {book['title']:<30} {book['author']:<20} "
                  f"{book['borrow_count']:<10} {available:<10}")
    
    def generate_statistics(self):
        """生成统计报表（仅管理员）"""
        if not self.current_user or self.current_user['user_type'] != 'admin':
            print("✗ 只有管理员才能查看统计报表！")
            return
        
        print("\n📊 图书馆统计报表")
        print("="*50)
        
        # 图书统计
        self.cursor.execute('''
        SELECT COUNT(*) as total_books, 
               SUM(total_copies) as total_copies,
               SUM(available_copies) as available_copies
        FROM books
        ''')
        
        stats = self.cursor.fetchone()
        print(f"图书种类：{stats['total_books']}")
        print(f"图书总册数：{stats['total_copies']}")
        print(f"可借册数：{stats['available_copies']}")
        
        # 用户统计
        self.cursor.execute('SELECT COUNT(*) FROM users WHERE user_type = "member"')
        member_count = self.cursor.fetchone()[0]
        print(f"\n注册用户数：{member_count}")
        
        # 借阅统计
        self.cursor.execute('''
        SELECT COUNT(*) as active_borrowings,
               COUNT(DISTINCT user_id) as active_users
        FROM borrowings
        WHERE status = 'active'
        ''')
        
        borrow_stats = self.cursor.fetchone()
        print(f"当前借阅数：{borrow_stats['active_borrowings']}")
        print(f"活跃用户数：{borrow_stats['active_users']}")
        
        # 逾期统计
        self.cursor.execute('''
        SELECT COUNT(*) FROM borrowings
        WHERE status = 'active' AND due_date < date('now')
        ''')
        
        overdue_count = self.cursor.fetchone()[0]
        print(f"逾期未还：{overdue_count}")
        
        # 罚金统计
        self.cursor.execute('SELECT SUM(fine) FROM borrowings WHERE fine > 0')
        total_fine = self.cursor.fetchone()[0] or 0
        print(f"\n累计罚金：¥{total_fine:.2f}")
    
    def run(self):
        """运行主程序"""
        print("="*50)
        print("📚 欢迎使用图书管理系统")
        print("="*50)
        
        while True:
            if self.current_user:
                print(f"\n当前用户：{self.current_user['username']} "
                      f"({self.current_user['user_type']})")
            
            print("\n请选择操作：")
            print("1. 用户登录")
            print("2. 用户注册")
            print("3. 搜索图书")
            print("4. 借阅图书")
            print("5. 归还图书")
            print("6. 我的借阅")
            print("7. 热门图书")
            
            if self.current_user and self.current_user['user_type'] == 'admin':
                print("8. 添加图书（管理员）")
                print("9. 统计报表（管理员）")
            
            if self.current_user:
                print("L. 退出登录")
            
            print("0. 退出系统")
            
            choice = input("\n请输入选择：").upper()
            
            if choice == '0':
                print("\n感谢使用，再见！")
                break
            
            elif choice == '1':
                if self.current_user:
                    print("您已登录！")
                else:
                    username = input("用户名：")
                    password = getpass("密码：")
                    self.login(username, password)
            
            elif choice == '2':
                username = input("用户名：")
                password = getpass("密码：")
                email = input("邮箱（可选）：")
                self.register_user(username, password, email or None)
            
            elif choice == '3':
                keyword = input("请输入搜索关键词：")
                books = self.search_books(keyword)
                
                if books:
                    print(f"\n找到 {len(books)} 本相关图书：")
                    print("-" * 100)
                    print(f"{'ID':<5} {'ISBN':<15} {'书名':<30} {'作者':<20} {'可借':<10}")
                    print("-" * 100)
                    
                    for book in books:
                        available = f"{book['available_copies']}/{book['total_copies']}"
                        print(f"{book['book_id']:<5} {book['isbn']:<15} "
                              f"{book['title']:<30} {book['author']:<20} {available:<10}")
                else:
                    print("未找到相关图书")
            
            elif choice == '4':
                if not self.current_user:
                    print("请先登录！")
                else:
                    book_id = int(input("请输入图书ID："))
                    self.borrow_book(book_id)
            
            elif choice == '5':
                if not self.current_user:
                    print("请先登录！")
                else:
                    book_id = int(input("请输入要归还的图书ID："))
                    self.return_book(book_id)
            
            elif choice == '6':
                self.view_my_borrowings()
            
            elif choice == '7':
                self.view_popular_books()
            
            elif choice == '8' and self.current_user and self.current_user['user_type'] == 'admin':
                print("\n添加新书：")
                isbn = input("ISBN：")
                title = input("书名：")
                author = input("作者：")
                publisher = input("出版社（可选）：")
                category = input("分类（可选）：")
                copies = int(input("册数（默认1）：") or "1")
                
                self.add_book(isbn, title, author, 
                            publisher or None, category or None, copies)
            
            elif choice == '9' and self.current_user and self.current_user['user_type'] == 'admin':
                self.generate_statistics()
            
            elif choice == 'L' and self.current_user:
                self.logout()
            
            else:
                print("无效选择，请重试")
    
    def close(self):
        """关闭数据库连接"""
        self.conn.close()

def main():
    """主函数"""
    system = LibrarySystem()
    
    try:
        system.run()
    except KeyboardInterrupt:
        print("\n\n程序被中断")
    except Exception as e:
        print(f"\n发生错误：{e}")
    finally:
        system.close()

if __name__ == "__main__":
    main() 