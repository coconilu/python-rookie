#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习2参考答案：CRUD实战
商品库存管理系统的完整实现
"""

import sqlite3
import os
from datetime import datetime

class InventorySystem:
    def __init__(self, db_name='inventory.db'):
        """初始化库存管理系统"""
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """创建数据表"""
        # 创建商品表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            min_stock INTEGER DEFAULT 0
        )
        ''')
        
        # 创建交易记录表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('purchase', 'sale')),
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_amount REAL NOT NULL,
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
        ''')
        
        # 创建索引优化查询性能
        self.cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_transactions_product 
        ON transactions(product_id)
        ''')
        
        self.cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_transactions_date 
        ON transactions(transaction_date)
        ''')
        
        self.conn.commit()
    
    def add_product(self, name, category, price, initial_stock, min_stock):
        """添加新商品"""
        try:
            self.cursor.execute('''
            INSERT INTO products (name, category, price, stock, min_stock)
            VALUES (?, ?, ?, ?, ?)
            ''', (name, category, price, initial_stock, min_stock))
            
            product_id = self.cursor.lastrowid
            
            # 如果有初始库存，记录为进货
            if initial_stock > 0:
                self.cursor.execute('''
                INSERT INTO transactions (product_id, type, quantity, unit_price, total_amount)
                VALUES (?, 'purchase', ?, ?, ?)
                ''', (product_id, initial_stock, price, initial_stock * price))
            
            self.conn.commit()
            print(f"✓ 成功添加商品：{name}")
            return product_id
            
        except Exception as e:
            self.conn.rollback()
            print(f"✗ 添加商品失败：{e}")
            return None
    
    def update_product_price(self, product_id, new_price):
        """更新商品价格"""
        self.cursor.execute('''
        UPDATE products SET price = ? WHERE product_id = ?
        ''', (new_price, product_id))
        
        if self.cursor.rowcount > 0:
            self.conn.commit()
            print(f"✓ 成功更新商品价格")
        else:
            print(f"✗ 商品ID {product_id} 不存在")
    
    def delete_product(self, product_id):
        """删除商品"""
        # 检查库存
        self.cursor.execute(
            'SELECT stock, name FROM products WHERE product_id = ?', 
            (product_id,)
        )
        result = self.cursor.fetchone()
        
        if not result:
            print(f"✗ 商品ID {product_id} 不存在")
            return False
        
        if result['stock'] > 0:
            print(f"✗ 无法删除：商品 {result['name']} 还有 {result['stock']} 件库存")
            return False
        
        # 删除商品
        self.cursor.execute('DELETE FROM products WHERE product_id = ?', (product_id,))
        self.conn.commit()
        print(f"✓ 成功删除商品：{result['name']}")
        return True
    
    def purchase_product(self, product_id, quantity, unit_price):
        """进货"""
        try:
            self.conn.execute('BEGIN')
            
            # 更新库存
            self.cursor.execute('''
            UPDATE products SET stock = stock + ? WHERE product_id = ?
            ''', (quantity, product_id))
            
            if self.cursor.rowcount == 0:
                raise Exception("商品不存在")
            
            # 记录交易
            total_amount = quantity * unit_price
            self.cursor.execute('''
            INSERT INTO transactions (product_id, type, quantity, unit_price, total_amount)
            VALUES (?, 'purchase', ?, ?, ?)
            ''', (product_id, quantity, unit_price, total_amount))
            
            self.conn.commit()
            print(f"✓ 进货成功：{quantity}件，总金额 ¥{total_amount:.2f}")
            return True
            
        except Exception as e:
            self.conn.rollback()
            print(f"✗ 进货失败：{e}")
            return False
    
    def sell_product(self, product_id, quantity):
        """销售商品"""
        try:
            self.conn.execute('BEGIN')
            
            # 获取商品信息
            self.cursor.execute('''
            SELECT name, price, stock, min_stock 
            FROM products WHERE product_id = ?
            ''', (product_id,))
            
            product = self.cursor.fetchone()
            if not product:
                raise Exception("商品不存在")
            
            if product['stock'] < quantity:
                raise Exception(f"库存不足：当前库存 {product['stock']}，需求 {quantity}")
            
            # 更新库存
            new_stock = product['stock'] - quantity
            self.cursor.execute('''
            UPDATE products SET stock = ? WHERE product_id = ?
            ''', (new_stock, product_id))
            
            # 记录交易
            total_amount = quantity * product['price']
            self.cursor.execute('''
            INSERT INTO transactions (product_id, type, quantity, unit_price, total_amount)
            VALUES (?, 'sale', ?, ?, ?)
            ''', (product_id, quantity, product['price'], total_amount))
            
            self.conn.commit()
            print(f"✓ 销售成功：{product['name']} {quantity}件，销售额 ¥{total_amount:.2f}")
            
            # 库存预警
            if new_stock < product['min_stock']:
                print(f"⚠️  库存预警：{product['name']} 当前库存({new_stock})低于警戒线({product['min_stock']})")
            
            return True
            
        except Exception as e:
            self.conn.rollback()
            print(f"✗ 销售失败：{e}")
            return False
    
    def get_low_stock_products(self):
        """获取库存预警商品"""
        self.cursor.execute('''
        SELECT name, stock, min_stock 
        FROM products 
        WHERE stock < min_stock
        ORDER BY (min_stock - stock) DESC
        ''')
        
        return [(row['name'], row['stock'], row['min_stock']) 
                for row in self.cursor.fetchall()]
    
    def get_product_transactions(self, product_id, days=30):
        """获取商品的交易记录"""
        self.cursor.execute('''
        SELECT * FROM transactions 
        WHERE product_id = ? 
        AND transaction_date >= datetime('now', '-' || ? || ' days')
        ORDER BY transaction_date DESC
        ''', (product_id, days))
        
        return self.cursor.fetchall()
    
    def generate_inventory_report(self):
        """生成库存报表"""
        print("\n📊 库存报表")
        print("="*50)
        
        # 商品总数
        self.cursor.execute('SELECT COUNT(*) FROM products')
        total_products = self.cursor.fetchone()[0]
        print(f"商品种类：{total_products}")
        
        # 总库存价值
        self.cursor.execute('SELECT SUM(stock * price) FROM products')
        total_value = self.cursor.fetchone()[0] or 0
        print(f"总库存价值：¥{total_value:,.2f}")
        
        # 各类别统计
        print("\n各类别商品统计：")
        self.cursor.execute('''
        SELECT category, COUNT(*) as count, SUM(stock) as total_stock,
               SUM(stock * price) as category_value
        FROM products
        GROUP BY category
        ''')
        
        for row in self.cursor.fetchall():
            print(f"  {row['category']}: {row['count']}种商品, "
                  f"库存{row['total_stock']}件, 价值¥{row['category_value']:,.2f}")
        
        # 库存预警
        low_stock = self.get_low_stock_products()
        if low_stock:
            print("\n⚠️  库存预警商品：")
            for name, stock, min_stock in low_stock:
                print(f"  - {name}: 当前{stock}件 (最低{min_stock}件)")
    
    def get_sales_statistics(self, start_date, end_date):
        """获取销售统计"""
        print(f"\n📈 销售统计 ({start_date} 至 {end_date})")
        print("="*50)
        
        # 总销售额
        self.cursor.execute('''
        SELECT SUM(total_amount) as total_sales, COUNT(*) as sale_count
        FROM transactions
        WHERE type = 'sale' 
        AND DATE(transaction_date) BETWEEN ? AND ?
        ''', (start_date, end_date))
        
        result = self.cursor.fetchone()
        total_sales = result['total_sales'] or 0
        sale_count = result['sale_count'] or 0
        
        print(f"总销售额：¥{total_sales:,.2f}")
        print(f"销售笔数：{sale_count}")
        
        # 销售最多的商品
        self.cursor.execute('''
        SELECT p.name, SUM(t.quantity) as total_quantity, 
               SUM(t.total_amount) as product_sales
        FROM transactions t
        JOIN products p ON t.product_id = p.product_id
        WHERE t.type = 'sale'
        AND DATE(t.transaction_date) BETWEEN ? AND ?
        GROUP BY t.product_id
        ORDER BY total_quantity DESC
        LIMIT 5
        ''', (start_date, end_date))
        
        print("\n销量TOP 5商品：")
        for row in self.cursor.fetchall():
            print(f"  {row['name']}: {row['total_quantity']}件, "
                  f"销售额¥{row['product_sales']:,.2f}")
        
        # 计算毛利润（简化：销售额 - 进货成本）
        self.cursor.execute('''
        SELECT 
            (SELECT SUM(total_amount) FROM transactions 
             WHERE type = 'sale' AND DATE(transaction_date) BETWEEN ? AND ?) -
            (SELECT COALESCE(SUM(total_amount), 0) FROM transactions 
             WHERE type = 'purchase' AND DATE(transaction_date) BETWEEN ? AND ?)
        AS gross_profit
        ''', (start_date, end_date, start_date, end_date))
        
        gross_profit = self.cursor.fetchone()[0] or 0
        print(f"\n毛利润：¥{gross_profit:,.2f}")
    
    def close(self):
        """关闭数据库连接"""
        self.conn.close()

def demo_inventory_system():
    """演示库存管理系统"""
    print("商品库存管理系统演示")
    print("="*50)
    
    system = InventorySystem()
    
    # 添加商品
    print("\n1. 添加商品")
    products = [
        ("iPhone 15", "电子产品", 5999, 50, 10),
        ("小米手机", "电子产品", 1999, 100, 20),
        ("笔记本电脑", "电子产品", 4999, 30, 5),
        ("T恤", "服装", 99, 200, 50),
        ("牛仔裤", "服装", 199, 150, 30)
    ]
    
    product_ids = []
    for product in products:
        pid = system.add_product(*product)
        if pid:
            product_ids.append(pid)
    
    # 进货
    print("\n2. 进货操作")
    system.purchase_product(product_ids[0], 20, 5500)  # iPhone进货
    system.purchase_product(product_ids[3], 100, 80)   # T恤进货
    
    # 销售
    print("\n3. 销售操作")
    system.sell_product(product_ids[0], 45)  # 销售iPhone
    system.sell_product(product_ids[1], 85)  # 销售小米手机
    
    # 库存预警
    print("\n4. 库存预警")
    low_stock = system.get_low_stock_products()
    for item in low_stock:
        print(f"  警告：{item[0]} 库存不足 (当前:{item[1]}, 最低:{item[2]})")
    
    # 生成报表
    print("\n5. 库存报表")
    system.generate_inventory_report()
    
    # 销售统计
    print("\n6. 本月销售统计")
    today = datetime.now()
    start_date = today.replace(day=1).strftime('%Y-%m-%d')
    end_date = today.strftime('%Y-%m-%d')
    system.get_sales_statistics(start_date, end_date)
    
    system.close()
    
    # 清理
    if os.path.exists('inventory.db'):
        os.remove('inventory.db')

if __name__ == "__main__":
    demo_inventory_system()
    
    print("\n" + "="*50)
    print("实现亮点：")
    print("1. 使用事务保证数据一致性")
    print("2. 创建索引优化查询性能")
    print("3. row_factory让查询结果可以像字典访问")
    print("4. 完善的库存预警机制")
    print("5. 详细的统计报表功能") 