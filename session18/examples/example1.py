#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
示例1：基础模型定义
演示如何定义基本的SQLAlchemy模型

学习要点：
1. 基础模型结构
2. 字段类型和约束
3. 模型方法定义
4. 基础CRUD操作
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# 创建Flask应用和数据库实例
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==================== 模型定义 ====================

class User(db.Model):
    """用户模型 - 展示基础字段类型和约束"""
    
    # 主键
    id = db.Column(db.Integer, primary_key=True)
    
    # 字符串字段
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # 可选字段
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    bio = db.Column(db.Text)
    
    # 布尔字段
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    # 数值字段
    age = db.Column(db.Integer)
    score = db.Column(db.Float, default=0.0)
    
    # 日期时间字段
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def __init__(self, username, email, password=None):
        """构造函数"""
        self.username = username
        self.email = email
        if password:
            self.set_password(password)
    
    def set_password(self, password):
        """设置密码（加密存储）"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """获取全名"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def is_authenticated(self):
        """检查是否已认证"""
        return True
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.get_full_name(),
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'age': self.age,
            'score': self.score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def __repr__(self):
        """字符串表示"""
        return f'<User {self.username}>'

class Product(db.Model):
    """产品模型 - 展示数值约束和默认值"""
    
    id = db.Column(db.Integer, primary_key=True)
    
    # 产品信息
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    
    # 价格信息（使用Numeric确保精度）
    price = db.Column(db.Numeric(10, 2), nullable=False)
    cost = db.Column(db.Numeric(10, 2))
    
    # 库存信息
    stock_quantity = db.Column(db.Integer, default=0)
    min_stock = db.Column(db.Integer, default=0)
    
    # 状态
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    
    # 评分系统
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, name, sku, price):
        """构造函数"""
        self.name = name
        self.sku = sku
        self.price = price
    
    @property
    def profit_margin(self):
        """计算利润率"""
        if self.cost and self.price:
            return float((self.price - self.cost) / self.price * 100)
        return 0.0
    
    def is_in_stock(self):
        """检查是否有库存"""
        return self.stock_quantity > 0
    
    def is_low_stock(self):
        """检查是否库存不足"""
        return self.stock_quantity <= self.min_stock
    
    def update_stock(self, quantity):
        """更新库存"""
        self.stock_quantity += quantity
        if self.stock_quantity < 0:
            self.stock_quantity = 0
    
    def add_review(self, rating):
        """添加评价"""
        total_rating = self.rating * self.review_count + rating
        self.review_count += 1
        self.rating = total_rating / self.review_count
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'sku': self.sku,
            'price': float(self.price),
            'cost': float(self.cost) if self.cost else None,
            'stock_quantity': self.stock_quantity,
            'min_stock': self.min_stock,
            'is_active': self.is_active,
            'is_featured': self.is_featured,
            'rating': self.rating,
            'review_count': self.review_count,
            'profit_margin': self.profit_margin,
            'is_in_stock': self.is_in_stock(),
            'is_low_stock': self.is_low_stock(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Product {self.name} ({self.sku})>'

# ==================== 演示函数 ====================

def demonstrate_basic_operations():
    """演示基础CRUD操作"""
    print("\n=== 基础CRUD操作演示 ===")
    
    # 创建用户
    print("1. 创建用户")
    user1 = User('alice', 'alice@example.com', 'password123')
    user1.first_name = 'Alice'
    user1.last_name = 'Johnson'
    user1.age = 25
    user1.bio = '喜欢编程的软件工程师'
    
    user2 = User('bob', 'bob@example.com', 'password456')
    user2.first_name = 'Bob'
    user2.last_name = 'Smith'
    user2.age = 30
    user2.is_admin = True
    
    # 保存到数据库
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    
    print(f"创建用户: {user1.username}, {user2.username}")
    
    # 查询操作
    print("\n2. 查询操作")
    all_users = User.query.all()
    print(f"所有用户: {[user.username for user in all_users]}")
    
    alice = User.query.filter_by(username='alice').first()
    print(f"查询Alice: {alice.get_full_name()}")
    
    admin_users = User.query.filter_by(is_admin=True).all()
    print(f"管理员用户: {[user.username for user in admin_users]}")
    
    # 更新操作
    print("\n3. 更新操作")
    alice.last_login = datetime.utcnow()
    alice.score = 95.5
    db.session.commit()
    print(f"更新Alice登录时间和分数: {alice.last_login}, {alice.score}")
    
    # 删除操作（演示用，实际不删除）
    print("\n4. 查询统计")
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    print(f"总用户数: {total_users}, 活跃用户数: {active_users}")

def demonstrate_product_operations():
    """演示产品模型操作"""
    print("\n=== 产品模型操作演示 ===")
    
    # 创建产品
    print("1. 创建产品")
    laptop = Product('MacBook Pro', 'MBP-001', 999.99)
    laptop.description = '高性能笔记本电脑'
    laptop.cost = 700.00
    laptop.stock_quantity = 50
    laptop.min_stock = 10
    laptop.is_featured = True
    
    phone = Product('iPhone 15', 'IP15-001', 799.99)
    phone.description = '最新款智能手机'
    phone.cost = 500.00
    phone.stock_quantity = 100
    phone.min_stock = 20
    
    # 保存产品
    db.session.add_all([laptop, phone])
    db.session.commit()
    
    print(f"创建产品: {laptop.name}, {phone.name}")
    
    # 产品操作
    print("\n2. 产品业务操作")
    print(f"MacBook利润率: {laptop.profit_margin:.2f}%")
    print(f"iPhone库存状态: {'有库存' if phone.is_in_stock() else '无库存'}")
    
    # 模拟销售
    laptop.update_stock(-5)  # 卖出5台
    print(f"卖出5台MacBook后库存: {laptop.stock_quantity}")
    
    # 添加评价
    laptop.add_review(4.5)
    laptop.add_review(5.0)
    laptop.add_review(4.8)
    print(f"MacBook评价: {laptop.rating:.2f} 分 ({laptop.review_count} 条评价)")
    
    # 保存更改
    db.session.commit()
    
    # 查询产品
    print("\n3. 产品查询")
    featured_products = Product.query.filter_by(is_featured=True).all()
    print(f"推荐产品: {[p.name for p in featured_products]}")
    
    expensive_products = Product.query.filter(Product.price > 800).all()
    print(f"高价产品: {[p.name for p in expensive_products]}")

def demonstrate_model_methods():
    """演示模型方法"""
    print("\n=== 模型方法演示 ===")
    
    # 获取用户
    alice = User.query.filter_by(username='alice').first()
    laptop = Product.query.filter_by(sku='MBP-001').first()
    
    if alice:
        print("用户信息:")
        print(f"  全名: {alice.get_full_name()}")
        print(f"  认证状态: {alice.is_authenticated()}")
        print(f"  密码验证: {alice.check_password('password123')}")
        print(f"  字典格式: {alice.to_dict()}")
    
    if laptop:
        print("\n产品信息:")
        print(f"  利润率: {laptop.profit_margin:.2f}%")
        print(f"  库存状态: {'充足' if not laptop.is_low_stock() else '不足'}")
        print(f"  字典格式: {laptop.to_dict()}")

def main():
    """主函数"""
    print("=" * 60)
    print("示例1：基础模型定义")
    print("=" * 60)
    
    with app.app_context():
        # 创建表
        db.create_all()
        
        # 清空数据（如果存在）
        if User.query.count() > 0:
            db.session.query(User).delete()
            db.session.query(Product).delete()
            db.session.commit()
        
        # 运行演示
        demonstrate_basic_operations()
        demonstrate_product_operations()
        demonstrate_model_methods()
    
    print("\n" + "=" * 60)
    print("示例1完成！")
    print("学习要点总结：")
    print("1. 模型定义：类继承db.Model，字段使用db.Column定义")
    print("2. 字段类型：Integer, String, Text, Boolean, Float, DateTime等")
    print("3. 字段约束：primary_key, unique, nullable, default, index等")
    print("4. 模型方法：构造函数、属性方法、业务方法、转换方法")
    print("5. CRUD操作：create, read, update, delete的基本操作")
    print("=" * 60)

if __name__ == '__main__':
    main() 