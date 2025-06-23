#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习2：CRUD实战 - 商品库存管理系统
目标：实现一个完整的商品库存管理系统

要求：
1. 设计合理的数据库表结构
2. 实现完整的CRUD功能
3. 添加库存预警功能
4. 实现进货和销售记录
5. 提供库存统计报表
"""

import sqlite3
import os
from datetime import datetime

class InventorySystem:
    def __init__(self, db_name='inventory.db'):
        """初始化库存管理系统"""
        # TODO: 初始化数据库连接
        pass
    
    def create_tables(self):
        """创建数据表"""
        # TODO: 创建以下表
        # 1. products表：商品信息
        #    - product_id (主键)
        #    - name (商品名称)
        #    - category (类别)
        #    - price (单价)
        #    - stock (当前库存)
        #    - min_stock (最低库存警戒线)
        
        # 2. transactions表：进货/销售记录
        #    - transaction_id (主键)
        #    - product_id (外键)
        #    - type (类型：'purchase'进货 或 'sale'销售)
        #    - quantity (数量)
        #    - unit_price (单价)
        #    - total_amount (总金额)
        #    - transaction_date (交易日期)
        pass
    
    def add_product(self, name, category, price, initial_stock, min_stock):
        """添加新商品"""
        # TODO: 实现添加商品功能
        # 返回新商品的ID
        pass
    
    def update_product_price(self, product_id, new_price):
        """更新商品价格"""
        # TODO: 实现价格更新功能
        pass
    
    def delete_product(self, product_id):
        """删除商品"""
        # TODO: 实现删除功能
        # 注意：只有库存为0的商品才能删除
        pass
    
    def purchase_product(self, product_id, quantity, unit_price):
        """进货"""
        # TODO: 实现进货功能
        # 1. 增加库存
        # 2. 记录进货交易
        pass
    
    def sell_product(self, product_id, quantity):
        """销售商品"""
        # TODO: 实现销售功能
        # 1. 检查库存是否充足
        # 2. 减少库存
        # 3. 记录销售交易
        # 4. 如果库存低于警戒线，发出警告
        pass
    
    def get_low_stock_products(self):
        """获取库存预警商品"""
        # TODO: 查询库存低于警戒线的商品
        # 返回：[(商品名, 当前库存, 最低库存), ...]
        pass
    
    def get_product_transactions(self, product_id, days=30):
        """获取商品的交易记录"""
        # TODO: 查询指定商品最近N天的交易记录
        pass
    
    def generate_inventory_report(self):
        """生成库存报表"""
        # TODO: 生成包含以下信息的报表
        # 1. 商品总数
        # 2. 总库存价值
        # 3. 各类别商品数量
        # 4. 库存预警商品列表
        pass
    
    def get_sales_statistics(self, start_date, end_date):
        """获取销售统计"""
        # TODO: 统计指定时间段的销售情况
        # 返回：总销售额、销售数量最多的商品、利润等
        pass
    
    def close(self):
        """关闭数据库连接"""
        # TODO: 关闭连接
        pass

def demo_inventory_system():
    """演示库存管理系统"""
    print("商品库存管理系统演示")
    print("="*50)
    
    system = InventorySystem()
    system.create_tables()
    
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
        product_ids.append(pid)
        print(f"  添加商品：{product[0]}")
    
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
    start_date = "2024-01-01"
    end_date = "2024-01-31"
    system.get_sales_statistics(start_date, end_date)
    
    system.close()
    
    # 清理
    if os.path.exists('inventory.db'):
        os.remove('inventory.db')

if __name__ == "__main__":
    demo_inventory_system()
    
    print("\n" + "="*50)
    print("练习提示：")
    print("1. 使用事务确保进货/销售的原子性")
    print("2. 合理使用索引提高查询性能")
    print("3. 实现完善的错误处理")
    print("4. 考虑并发访问的情况") 