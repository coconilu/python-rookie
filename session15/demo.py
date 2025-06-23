#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session 15: 数据库操作 - 演示代码
主题：SQLite数据库基础操作与图书管理系统
作者：Python学习者
"""

import sqlite3
import os
from datetime import datetime

# ==================== 1. 数据库基础操作 ====================

def demo_basic_operations():
    """演示基本的数据库操作"""
    print("="*50)
    print("1. 数据库基础操作演示")
    print("="*50)
    
    # 连接数据库
    conn = sqlite3.connect('demo.db')
    cursor = conn.cursor()
    
    # 创建表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        grade TEXT
    )
    ''')
    
    # 插入数据
    students = [
        ('张三', 18, 'A'),
        ('李四', 19, 'B'),
        ('王五', 20, 'A')
    ]
    
    cursor.executemany('INSERT INTO students (name, age, grade) VALUES (?, ?, ?)', students)
    conn.commit()
    
    # 查询数据
    print("\n所有学生信息：")
    cursor.execute('SELECT * FROM students')
    for row in cursor.fetchall():
        print(f"ID: {row[0]}, 姓名: {row[1]}, 年龄: {row[2]}, 成绩: {row[3]}")
    
    # 更新数据
    cursor.execute('UPDATE students SET grade = ? WHERE name = ?', ('A+', '李四'))
    conn.commit()
    
    # 删除数据
    cursor.execute('DELETE FROM students WHERE age < ?', (19,))
    conn.commit()
    
    print("\n更新后的学生信息：")
    cursor.execute('SELECT * FROM students')
    for row in cursor.fetchall():
        print(f"ID: {row[0]}, 姓名: {row[1]}, 年龄: {row[2]}, 成绩: {row[3]}")
    
    # 清理
    cursor.execute('DROP TABLE students')
    conn.close()
    os.remove('demo.db')

# ==================== 2. 图书管理系统 ====================

class BookLibrary:
    """图书管理系统"""
    
    def __init__(self, db_name='library.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """连接数据库"""
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row  # 允许通过列名访问
        self.cursor = self.conn.cursor()
    
    def create_tables(self):
        """创建数据表"""
        # 图书表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT UNIQUE,
            price REAL DEFAULT 0.0,
            stock INTEGER DEFAULT 0,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 用户表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 借阅记录表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS borrowings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            borrow_date DATE DEFAULT CURRENT_DATE,
            return_date DATE,
            actual_return_date DATE,
            status TEXT DEFAULT 'borrowed',
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
        ''')
        
        self.conn.commit()
    
    def add_book(self, title, author, isbn, price, stock, category=None):
        """添加图书"""
        try:
            self.cursor.execute('''
            INSERT INTO books (title, author, isbn, price, stock, category)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, author, isbn, price, stock, category))
            self.conn.commit()
            print(f"✓ 成功添加图书：《{title}》")
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"✗ 添加失败：ISBN {isbn} 已存在")
            return None
    
    def search_books(self, keyword=None, category=None):
        """搜索图书"""
        if keyword and category:
            sql = "SELECT * FROM books WHERE (title LIKE ? OR author LIKE ?) AND category = ?"
            params = (f'%{keyword}%', f'%{keyword}%', category)
        elif keyword:
            sql = "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?"
            params = (f'%{keyword}%', f'%{keyword}%')
        elif category:
            sql = "SELECT * FROM books WHERE category = ?"
            params = (category,)
        else:
            sql = "SELECT * FROM books"
            params = ()
        
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()
    
    def update_stock(self, book_id, quantity_change):
        """更新库存"""
        self.cursor.execute('SELECT stock FROM books WHERE id = ?', (book_id,))
        result = self.cursor.fetchone()
        
        if result:
            new_stock = result['stock'] + quantity_change
            if new_stock >= 0:
                self.cursor.execute('UPDATE books SET stock = ? WHERE id = ?', 
                                  (new_stock, book_id))
                self.conn.commit()
                print(f"✓ 库存更新成功：{result['stock']} → {new_stock}")
                return True
            else:
                print("✗ 错误：库存不能为负数")
                return False
        else:
            print(f"✗ 未找到ID为 {book_id} 的图书")
            return False
    
    def display_books(self):
        """显示所有图书"""
        books = self.search_books()
        
        if not books:
            print("\n📚 图书库是空的")
            return
        
        print("\n" + "="*120)
        print(f"{'ID':<5} {'书名':<30} {'作者':<20} {'ISBN':<20} {'分类':<15} {'价格':<10} {'库存':<10}")
        print("="*120)
        
        for book in books:
            print(f"{book['id']:<5} {book['title']:<30} {book['author']:<20} "
                  f"{book['isbn'] or '无':<20} {book['category'] or '未分类':<15} "
                  f"¥{book['price']:<10.2f} {book['stock']:<10}")
        
        # 统计信息
        self.cursor.execute('''
        SELECT COUNT(*) as count, 
               SUM(stock) as total_stock, 
               AVG(price) as avg_price,
               SUM(price * stock) as total_value
        FROM books
        ''')
        stats = self.cursor.fetchone()
        
        print("="*120)
        print(f"📊 统计：共{stats['count']}种图书，"
              f"总库存{stats['total_stock']}本，"
              f"平均价格¥{stats['avg_price']:.2f}，"
              f"总价值¥{stats['total_value']:.2f}")
    
    def add_user(self, username, password, email=None):
        """添加用户"""
        try:
            self.cursor.execute('''
            INSERT INTO users (username, password, email)
            VALUES (?, ?, ?)
            ''', (username, password, email))
            self.conn.commit()
            print(f"✓ 用户 {username} 注册成功")
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"✗ 用户名 {username} 已存在")
            return None
    
    def borrow_book(self, user_id, book_id, days=30):
        """借阅图书"""
        # 检查图书库存
        self.cursor.execute('SELECT stock FROM books WHERE id = ?', (book_id,))
        book = self.cursor.fetchone()
        
        if not book:
            print("✗ 图书不存在")
            return False
        
        if book['stock'] <= 0:
            print("✗ 图书库存不足")
            return False
        
        # 检查是否已借阅
        self.cursor.execute('''
        SELECT * FROM borrowings 
        WHERE user_id = ? AND book_id = ? AND status = 'borrowed'
        ''', (user_id, book_id))
        
        if self.cursor.fetchone():
            print("✗ 该用户已借阅此书")
            return False
        
        # 创建借阅记录
        self.cursor.execute('''
        INSERT INTO borrowings (user_id, book_id, return_date)
        VALUES (?, ?, date('now', '+{} days'))
        '''.format(days), (user_id, book_id))
        
        # 减少库存
        self.update_stock(book_id, -1)
        
        self.conn.commit()
        print("✓ 借阅成功")
        return True
    
    def return_book(self, user_id, book_id):
        """归还图书"""
        self.cursor.execute('''
        UPDATE borrowings 
        SET status = 'returned', actual_return_date = date('now')
        WHERE user_id = ? AND book_id = ? AND status = 'borrowed'
        ''', (user_id, book_id))
        
        if self.cursor.rowcount > 0:
            # 增加库存
            self.update_stock(book_id, 1)
            self.conn.commit()
            print("✓ 归还成功")
            return True
        else:
            print("✗ 未找到借阅记录")
            return False
    
    def get_user_borrowings(self, user_id):
        """获取用户借阅记录"""
        self.cursor.execute('''
        SELECT b.*, books.title, books.author
        FROM borrowings b
        JOIN books ON b.book_id = books.id
        WHERE b.user_id = ?
        ORDER BY b.borrow_date DESC
        ''', (user_id,))
        
        return self.cursor.fetchall()
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()

# ==================== 3. 演示高级功能 ====================

def demo_advanced_features():
    """演示高级数据库功能"""
    print("\n" + "="*50)
    print("3. 高级功能演示")
    print("="*50)
    
    library = BookLibrary('advanced_demo.db')
    
    # 批量添加图书
    books_data = [
        ("Python编程：从入门到实践", "Eric Matthes", "978-7-115-42802-8", 89.00, 20, "编程"),
        ("流畅的Python", "Luciano Ramalho", "978-7-115-45415-7", 139.00, 15, "编程"),
        ("数据结构与算法", "严蔚敏", "978-7-302-14751-0", 49.00, 25, "计算机科学"),
        ("机器学习实战", "Peter Harrington", "978-7-115-27974-7", 69.00, 10, "人工智能"),
        ("深度学习", "Ian Goodfellow", "978-7-115-46147-6", 168.00, 8, "人工智能")
    ]
    
    for book in books_data:
        library.add_book(*book)
    
    # 分类统计
    print("\n📊 按分类统计图书：")
    library.cursor.execute('''
    SELECT category, COUNT(*) as count, AVG(price) as avg_price
    FROM books
    GROUP BY category
    ''')
    
    for row in library.cursor.fetchall():
        print(f"{row['category']}: {row['count']}本, 平均价格¥{row['avg_price']:.2f}")
    
    # 价格区间分析
    print("\n💰 价格区间分析：")
    price_ranges = [(0, 50), (50, 100), (100, 150), (150, 200)]
    
    for min_price, max_price in price_ranges:
        library.cursor.execute('''
        SELECT COUNT(*) as count
        FROM books
        WHERE price >= ? AND price < ?
        ''', (min_price, max_price))
        
        count = library.cursor.fetchone()['count']
        print(f"¥{min_price}-{max_price}: {count}本")
    
    # 清理
    library.close()
    os.remove('advanced_demo.db')

# ==================== 4. 实际应用示例 ====================

def interactive_library_system():
    """交互式图书管理系统"""
    library = BookLibrary()
    
    # 初始化一些示例数据
    sample_books = [
        ("Python核心编程", "Wesley Chun", "978-7-115-41497-7", 99.00, 15, "编程"),
        ("算法导论", "Thomas H. Cormen", "978-7-111-40701-0", 128.00, 10, "算法"),
        ("代码大全", "Steve McConnell", "978-7-121-02298-2", 128.00, 12, "软件工程"),
    ]
    
    for book in sample_books:
        library.add_book(*book)
    
    # 添加示例用户
    library.add_user("admin", "123456", "admin@library.com")
    library.add_user("test", "123456", "test@library.com")
    
    while True:
        print("\n" + "="*50)
        print("📚 图书管理系统")
        print("="*50)
        print("1. 显示所有图书")
        print("2. 搜索图书")
        print("3. 添加图书")
        print("4. 更新库存")
        print("5. 借阅图书")
        print("6. 归还图书")
        print("7. 查看借阅记录")
        print("0. 退出系统")
        
        choice = input("\n请选择操作 (0-7): ")
        
        if choice == '0':
            print("\n👋 感谢使用，再见！")
            break
        
        elif choice == '1':
            library.display_books()
        
        elif choice == '2':
            keyword = input("请输入搜索关键词（书名或作者）: ")
            books = library.search_books(keyword)
            if books:
                print(f"\n找到 {len(books)} 本相关图书：")
                for book in books:
                    print(f"- 《{book['title']}》 作者：{book['author']}")
            else:
                print("未找到相关图书")
        
        elif choice == '3':
            print("\n添加新书：")
            title = input("书名: ")
            author = input("作者: ")
            isbn = input("ISBN: ")
            price = float(input("价格: "))
            stock = int(input("库存: "))
            category = input("分类（可选）: ")
            library.add_book(title, author, isbn, price, stock, category or None)
        
        elif choice == '4':
            book_id = int(input("请输入图书ID: "))
            quantity = int(input("库存变化量（正数增加，负数减少）: "))
            library.update_stock(book_id, quantity)
        
        elif choice == '5':
            user_id = int(input("用户ID: "))
            book_id = int(input("图书ID: "))
            library.borrow_book(user_id, book_id)
        
        elif choice == '6':
            user_id = int(input("用户ID: "))
            book_id = int(input("图书ID: "))
            library.return_book(user_id, book_id)
        
        elif choice == '7':
            user_id = int(input("用户ID: "))
            borrowings = library.get_user_borrowings(user_id)
            if borrowings:
                print(f"\n用户 {user_id} 的借阅记录：")
                for b in borrowings:
                    status = "已归还" if b['status'] == 'returned' else "借阅中"
                    print(f"- 《{b['title']}》 {status} (借阅日期：{b['borrow_date']})")
            else:
                print("无借阅记录")
    
    library.close()

# ==================== 主程序 ====================

def main():
    """主程序"""
    print("🎓 Session 15: 数据库操作")
    print("📚 主题：SQLite数据库与图书管理系统")
    print("="*50)
    
    while True:
        print("\n请选择演示内容：")
        print("1. 数据库基础操作")
        print("2. 图书管理系统演示")
        print("3. 高级功能演示")
        print("4. 交互式图书管理系统")
        print("0. 退出")
        
        choice = input("\n请输入选择 (0-4): ")
        
        if choice == '0':
            print("\n感谢学习！继续加油！💪")
            
            # 清理临时文件
            for db_file in ['library.db', 'demo.db', 'advanced_demo.db']:
                if os.path.exists(db_file):
                    os.remove(db_file)
            break
        
        elif choice == '1':
            demo_basic_operations()
        
        elif choice == '2':
            library = BookLibrary()
            print("\n演示图书管理系统基本功能...")
            
            # 添加图书
            library.add_book("Python编程", "张三", "123-456", 59.0, 10, "编程")
            library.add_book("数据库原理", "李四", "789-012", 49.0, 5, "数据库")
            
            # 显示图书
            library.display_books()
            
            # 搜索图书
            print("\n搜索包含'Python'的图书：")
            books = library.search_books("Python")
            for book in books:
                print(f"- {book['title']}")
            
            library.close()
            os.remove('library.db')
        
        elif choice == '3':
            demo_advanced_features()
        
        elif choice == '4':
            interactive_library_system()
            if os.path.exists('library.db'):
                os.remove('library.db')
        
        else:
            print("无效选择，请重试")
        
        input("\n按Enter键继续...")

if __name__ == "__main__":
    main() 