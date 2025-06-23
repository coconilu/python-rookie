#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
练习1：模型设计练习
设计并实现一个图书管理系统的数据模型

要求：
1. 设计用户（User）、图书（Book）、作者（Author）、分类（Category）模型
2. 实现适当的关系（一对多、多对多）
3. 添加必要的字段约束和验证
4. 实现模型方法
5. 创建示例数据并测试

学习目标：
- 掌握模型设计的基本原则
- 理解不同类型的表关系
- 学会添加字段约束
- 练习模型方法的编写
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library_exercise.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==================== 练习任务 ====================

"""
任务1：用户模型设计
设计一个用户模型，包含以下功能：
- 基本信息：用户名、邮箱、密码、姓名、电话等
- 注册时间、最后登录时间
- 用户类型：普通用户、管理员
- 账户状态：激活、禁用
- 密码加密存储和验证方法
- 获取用户借阅统计的方法
"""

class User(db.Model):
    """用户模型"""
    # TODO: 实现用户模型
    # 提示：
    # - 使用适当的字段类型和约束
    # - 添加索引提高查询性能
    # - 实现密码加密方法
    # - 添加用户状态管理
    pass

"""
任务2：作者模型设计
设计作者模型，包含以下功能：
- 基本信息：姓名、简介、国籍、出生日期等
- 作者可以写多本书（一对多关系）
- 获取作者所有作品的方法
- 计算作者作品数量的方法
"""

class Author(db.Model):
    """作者模型"""
    # TODO: 实现作者模型
    pass

"""
任务3：分类模型设计
设计图书分类模型：
- 分类名称、描述
- 支持层次分类（自引用关系）
- 分类下的图书数量统计
"""

class Category(db.Model):
    """图书分类模型"""
    # TODO: 实现分类模型
    # 提示：使用自引用关系实现层次分类
    pass

"""
任务4：图书模型设计
设计图书模型，包含：
- 基本信息：书名、ISBN、价格、页数、出版日期等
- 关系：作者（多对多）、分类（多对一）
- 状态：可借阅、已借出、维修中等
- 借阅统计：借阅次数、当前借阅者等
"""

# 图书作者关系表（多对多）
# TODO: 定义图书和作者的多对多关系表
# book_author = db.Table('book_author',
#     db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
#     db.Column('author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True)
# )

class Book(db.Model):
    """图书模型"""
    # TODO: 实现图书模型
    # 提示：
    # - 使用ISBN作为唯一标识
    # - 实现状态管理
    # - 添加借阅相关字段
    pass

"""
任务5：借阅记录模型设计
设计借阅记录模型：
- 借阅用户、图书、借出时间、应还时间、实际归还时间
- 借阅状态：借阅中、已归还、逾期等
- 续借次数、罚款金额等
"""

class BorrowRecord(db.Model):
    """借阅记录模型"""
    # TODO: 实现借阅记录模型
    pass

# ==================== 测试函数 ====================

def test_user_model():
    """测试用户模型"""
    print("测试用户模型...")
    
    # TODO: 创建测试用户
    # TODO: 测试密码加密和验证
    # TODO: 测试用户状态管理
    
    pass

def test_author_model():
    """测试作者模型"""
    print("测试作者模型...")
    
    # TODO: 创建测试作者
    # TODO: 测试作者相关方法
    
    pass

def test_category_model():
    """测试分类模型"""
    print("测试分类模型...")
    
    # TODO: 创建层次分类
    # TODO: 测试分类关系
    
    pass

def test_book_model():
    """测试图书模型"""
    print("测试图书模型...")
    
    # TODO: 创建测试图书
    # TODO: 测试图书作者关系
    # TODO: 测试图书分类关系
    
    pass

def test_borrow_record_model():
    """测试借阅记录模型"""
    print("测试借阅记录模型...")
    
    # TODO: 创建借阅记录
    # TODO: 测试借阅状态管理
    
    pass

def create_sample_data():
    """创建示例数据"""
    print("创建示例数据...")
    
    # TODO: 创建完整的示例数据
    # 包括：用户、作者、分类、图书、借阅记录
    
    pass

def run_exercises():
    """运行所有练习"""
    print("=" * 50)
    print("练习1：模型设计练习")
    print("=" * 50)
    
    with app.app_context():
        # 创建表
        db.create_all()
        
        # 运行测试
        test_user_model()
        test_author_model()
        test_category_model()
        test_book_model()
        test_borrow_record_model()
        
        # 创建示例数据
        create_sample_data()
    
    print("\n练习1完成！")
    print("\n检查点：")
    print("1. ✓ 用户模型是否包含所有必要字段？")
    print("2. ✓ 密码是否正确加密存储？")
    print("3. ✓ 表关系是否正确定义？")
    print("4. ✓ 模型方法是否正常工作？")
    print("5. ✓ 示例数据是否创建成功？")

if __name__ == '__main__':
    run_exercises()

# ==================== 参考答案 ====================

"""
参考答案（仅供参考，建议先自己完成）：

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    
    # 用户类型和状态
    user_type = db.Column(db.String(20), default='user')  # user, admin
    is_active = db.Column(db.Boolean, default=True)
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # 关系
    borrow_records = db.relationship('BorrowRecord', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_borrow_count(self):
        return len(self.borrow_records)
    
    def get_current_borrows(self):
        return [record for record in self.borrow_records if record.status == 'borrowed']

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    biography = db.Column(db.Text)
    nationality = db.Column(db.String(50))
    birth_date = db.Column(db.Date)
    death_date = db.Column(db.Date)
    
    def get_book_count(self):
        return len(self.books)

# ... 其他模型的参考实现
""" 