#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3：事务处理和高级查询
学习如何使用事务保证数据一致性，以及高级查询技巧
"""

import sqlite3
import os
from datetime import datetime, timedelta

class BankingSystem:
    """银行系统示例 - 演示事务处理"""
    
    def __init__(self, db_name='banking.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        # 设置隔离级别
        self.conn.isolation_level = None  # 自动提交模式关闭
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """创建账户和交易记录表"""
        # 账户表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT UNIQUE NOT NULL,
            holder_name TEXT NOT NULL,
            balance REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 交易记录表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_account TEXT,
            to_account TEXT,
            amount REAL NOT NULL,
            transaction_type TEXT NOT NULL,
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            description TEXT
        )
        ''')
        
        self.conn.commit()
    
    def create_account(self, account_number, holder_name, initial_balance=0):
        """创建账户"""
        try:
            self.cursor.execute('''
            INSERT INTO accounts (account_number, holder_name, balance)
            VALUES (?, ?, ?)
            ''', (account_number, holder_name, initial_balance))
            self.conn.commit()
            print(f"✓ 账户 {account_number} 创建成功")
            return True
        except sqlite3.IntegrityError:
            print(f"✗ 账户 {account_number} 已存在")
            return False
    
    def transfer_money(self, from_account, to_account, amount):
        """转账操作 - 使用事务"""
        try:
            # 开始事务
            self.cursor.execute('BEGIN TRANSACTION')
            
            # 1. 检查源账户余额
            self.cursor.execute(
                'SELECT balance FROM accounts WHERE account_number = ?',
                (from_account,)
            )
            from_balance = self.cursor.fetchone()
            
            if not from_balance:
                raise Exception(f"源账户 {from_account} 不存在")
            
            if from_balance[0] < amount:
                raise Exception("余额不足")
            
            # 2. 检查目标账户是否存在
            self.cursor.execute(
                'SELECT id FROM accounts WHERE account_number = ?',
                (to_account,)
            )
            if not self.cursor.fetchone():
                raise Exception(f"目标账户 {to_account} 不存在")
            
            # 3. 扣除源账户金额
            self.cursor.execute('''
            UPDATE accounts 
            SET balance = balance - ? 
            WHERE account_number = ?
            ''', (amount, from_account))
            
            # 4. 增加目标账户金额
            self.cursor.execute('''
            UPDATE accounts 
            SET balance = balance + ? 
            WHERE account_number = ?
            ''', (amount, to_account))
            
            # 5. 记录交易
            self.cursor.execute('''
            INSERT INTO transactions (from_account, to_account, amount, 
                                    transaction_type, description)
            VALUES (?, ?, ?, 'transfer', ?)
            ''', (from_account, to_account, amount, 
                  f'转账: {from_account} -> {to_account}'))
            
            # 提交事务
            self.cursor.execute('COMMIT')
            print(f"✓ 转账成功: {from_account} -> {to_account}, 金额: ¥{amount:.2f}")
            return True
            
        except Exception as e:
            # 回滚事务
            self.cursor.execute('ROLLBACK')
            print(f"✗ 转账失败: {e}")
            return False
    
    def deposit(self, account_number, amount):
        """存款操作"""
        try:
            self.cursor.execute('BEGIN TRANSACTION')
            
            # 更新余额
            self.cursor.execute('''
            UPDATE accounts 
            SET balance = balance + ? 
            WHERE account_number = ?
            ''', (amount, account_number))
            
            if self.cursor.rowcount == 0:
                raise Exception("账户不存在")
            
            # 记录交易
            self.cursor.execute('''
            INSERT INTO transactions (to_account, amount, transaction_type, description)
            VALUES (?, ?, 'deposit', '存款')
            ''', (account_number, amount))
            
            self.cursor.execute('COMMIT')
            print(f"✓ 存款成功: 账户 {account_number}, 金额: ¥{amount:.2f}")
            return True
            
        except Exception as e:
            self.cursor.execute('ROLLBACK')
            print(f"✗ 存款失败: {e}")
            return False
    
    def get_balance(self, account_number):
        """查询余额"""
        self.cursor.execute(
            'SELECT balance FROM accounts WHERE account_number = ?',
            (account_number,)
        )
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def get_transaction_history(self, account_number, days=30):
        """获取交易历史"""
        date_limit = datetime.now() - timedelta(days=days)
        
        self.cursor.execute('''
        SELECT * FROM transactions 
        WHERE (from_account = ? OR to_account = ?) 
        AND transaction_date >= ?
        ORDER BY transaction_date DESC
        ''', (account_number, account_number, date_limit))
        
        return self.cursor.fetchall()
    
    def close(self):
        """关闭连接"""
        self.conn.close()

def demo_transactions():
    """演示事务处理"""
    print("事务处理演示")
    print("="*50)
    
    bank = BankingSystem()
    
    # 创建账户
    print("\n1. 创建账户")
    bank.create_account("ACC001", "张三", 10000)
    bank.create_account("ACC002", "李四", 5000)
    bank.create_account("ACC003", "王五", 3000)
    
    # 显示初始余额
    print("\n初始余额：")
    for acc in ["ACC001", "ACC002", "ACC003"]:
        balance = bank.get_balance(acc)
        print(f"  {acc}: ¥{balance:.2f}")
    
    # 演示转账
    print("\n2. 转账操作")
    bank.transfer_money("ACC001", "ACC002", 2000)  # 成功
    bank.transfer_money("ACC002", "ACC003", 1000)  # 成功
    bank.transfer_money("ACC003", "ACC001", 5000)  # 失败：余额不足
    
    # 存款
    print("\n3. 存款操作")
    bank.deposit("ACC003", 3000)
    
    # 显示最终余额
    print("\n最终余额：")
    for acc in ["ACC001", "ACC002", "ACC003"]:
        balance = bank.get_balance(acc)
        print(f"  {acc}: ¥{balance:.2f}")
    
    # 查看交易历史
    print("\n4. ACC001的交易历史：")
    transactions = bank.get_transaction_history("ACC001")
    for trans in transactions:
        print(f"  {trans[5]}: {trans[3]} - ¥{trans[2]:.2f}")
    
    bank.close()

def demo_advanced_queries():
    """演示高级查询"""
    print("\n\n高级查询演示")
    print("="*50)
    
    # 创建示例数据库
    conn = sqlite3.connect('advanced_queries.db')
    cursor = conn.cursor()
    
    # 创建销售数据表
    cursor.execute('''
    CREATE TABLE sales (
        id INTEGER PRIMARY KEY,
        product TEXT NOT NULL,
        category TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        sale_date DATE NOT NULL,
        region TEXT NOT NULL
    )
    ''')
    
    # 插入示例数据
    sales_data = [
        ('手机', '电子产品', 10, 2999, '2024-01-15', '华北'),
        ('笔记本', '电子产品', 5, 4999, '2024-01-16', '华东'),
        ('T恤', '服装', 50, 99, '2024-01-15', '华北'),
        ('手机', '电子产品', 8, 2999, '2024-01-17', '华南'),
        ('牛仔裤', '服装', 30, 199, '2024-01-16', '华东'),
        ('平板', '电子产品', 12, 1999, '2024-01-18', '华北'),
        ('衬衫', '服装', 40, 149, '2024-01-17', '华南'),
        ('手机', '电子产品', 15, 2999, '2024-01-19', '华东'),
    ]
    
    cursor.executemany('''
    INSERT INTO sales (product, category, quantity, price, sale_date, region)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', sales_data)
    conn.commit()
    
    # 1. 分组统计
    print("\n1. 按类别统计销售额")
    cursor.execute('''
    SELECT category, 
           SUM(quantity * price) as total_sales,
           COUNT(*) as order_count,
           AVG(quantity * price) as avg_order_value
    FROM sales
    GROUP BY category
    ''')
    
    for row in cursor.fetchall():
        print(f"  {row[0]}: 总销售额 ¥{row[1]:,.2f}, "
              f"订单数 {row[2]}, 平均订单额 ¥{row[3]:,.2f}")
    
    # 2. 多条件查询
    print("\n2. 查找销售额超过10000的订单")
    cursor.execute('''
    SELECT product, quantity, price, quantity * price as total
    FROM sales
    WHERE quantity * price > 10000
    ORDER BY total DESC
    ''')
    
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]}件 × ¥{row[2]} = ¥{row[3]:,.2f}")
    
    # 3. 子查询
    print("\n3. 查找销售量高于平均值的产品")
    cursor.execute('''
    SELECT DISTINCT product, SUM(quantity) as total_quantity
    FROM sales
    GROUP BY product
    HAVING SUM(quantity) > (SELECT AVG(quantity) FROM sales)
    ''')
    
    for row in cursor.fetchall():
        print(f"  {row[0]}: 总销售量 {row[1]}件")
    
    # 4. 窗口函数（需要SQLite 3.25.0+）
    print("\n4. 按地区排名（销售额）")
    try:
        cursor.execute('''
        SELECT region, 
               SUM(quantity * price) as total_sales,
               RANK() OVER (ORDER BY SUM(quantity * price) DESC) as rank
        FROM sales
        GROUP BY region
        ''')
        
        for row in cursor.fetchall():
            print(f"  第{row[2]}名: {row[0]} - ¥{row[1]:,.2f}")
    except:
        print("  （需要SQLite 3.25.0+版本支持窗口函数）")
    
    # 5. 日期函数
    print("\n5. 按日期统计")
    cursor.execute('''
    SELECT sale_date, 
           COUNT(*) as orders,
           SUM(quantity * price) as daily_sales
    FROM sales
    GROUP BY sale_date
    ORDER BY sale_date
    ''')
    
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]}笔订单, 销售额 ¥{row[2]:,.2f}")
    
    # 清理
    conn.close()
    os.remove('advanced_queries.db')

def demo_indexes_and_optimization():
    """演示索引和查询优化"""
    print("\n\n索引和优化演示")
    print("="*50)
    
    conn = sqlite3.connect(':memory:')  # 使用内存数据库
    cursor = conn.cursor()
    
    # 创建大量数据
    cursor.execute('''
    CREATE TABLE large_table (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        city TEXT,
        salary REAL
    )
    ''')
    
    # 插入10000条数据
    import random
    cities = ['北京', '上海', '广州', '深圳', '杭州']
    
    print("\n插入10000条测试数据...")
    data = []
    for i in range(10000):
        name = f'用户{i}'
        age = random.randint(20, 60)
        city = random.choice(cities)
        salary = random.randint(3000, 50000)
        data.append((name, age, city, salary))
    
    cursor.executemany(
        'INSERT INTO large_table (name, age, city, salary) VALUES (?, ?, ?, ?)',
        data
    )
    
    # 无索引查询
    import time
    
    print("\n1. 无索引查询")
    start = time.time()
    cursor.execute('SELECT * FROM large_table WHERE city = ? AND age > ?', ('北京', 30))
    results = cursor.fetchall()
    end = time.time()
    print(f"  查询结果: {len(results)}条")
    print(f"  耗时: {(end - start)*1000:.2f}ms")
    
    # 创建索引
    print("\n2. 创建索引")
    cursor.execute('CREATE INDEX idx_city_age ON large_table(city, age)')
    print("  索引创建完成")
    
    # 有索引查询
    print("\n3. 有索引查询")
    start = time.time()
    cursor.execute('SELECT * FROM large_table WHERE city = ? AND age > ?', ('北京', 30))
    results = cursor.fetchall()
    end = time.time()
    print(f"  查询结果: {len(results)}条")
    print(f"  耗时: {(end - start)*1000:.2f}ms")
    
    # 查看查询计划
    print("\n4. 查询计划分析")
    cursor.execute('EXPLAIN QUERY PLAN SELECT * FROM large_table WHERE city = ? AND age > ?', 
                   ('北京', 30))
    plan = cursor.fetchall()
    print("  查询计划:")
    for step in plan:
        print(f"    {step}")
    
    conn.close()

if __name__ == "__main__":
    # 清理可能存在的数据库文件
    for db_file in ['banking.db', 'advanced_queries.db']:
        if os.path.exists(db_file):
            os.remove(db_file)
    
    # 运行演示
    demo_transactions()
    demo_advanced_queries()
    demo_indexes_and_optimization()
    
    print("\n" + "="*50)
    print("高级技巧总结：")
    print("1. 事务处理保证数据一致性")
    print("2. 使用GROUP BY进行分组统计")
    print("3. 子查询可以实现复杂逻辑")
    print("4. 创建索引可以大幅提升查询性能")
    print("5. 使用EXPLAIN分析查询计划")
    
    # 清理
    if os.path.exists('banking.db'):
        os.remove('banking.db') 