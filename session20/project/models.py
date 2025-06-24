#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session20 API开发项目数据模型
定义图书管理系统的数据模型

作者: Python学习教程
日期: 2024
"""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import BookCategories, UserRoles
import re

# 初始化数据库
db = SQLAlchemy()

class User(db.Model):
    """用户模型"""
    
    __tablename__ = 'users'
    
    # 基础字段
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # 用户信息
    role = db.Column(db.String(20), nullable=False, default=UserRoles.USER)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    
    # 时间戳
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # 关系
    books = db.relationship('Book', backref='creator', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, username, email, password, role=UserRoles.USER):
        """初始化用户
        
        Args:
            username (str): 用户名
            email (str): 邮箱
            password (str): 密码
            role (str): 角色
        """
        self.username = username
        self.email = email.lower()
        self.set_password(password)
        self.role = role
    
    def set_password(self, password):
        """设置密码
        
        Args:
            password (str): 明文密码
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码
        
        Args:
            password (str): 明文密码
            
        Returns:
            bool: 密码是否正确
        """
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """检查是否为管理员
        
        Returns:
            bool: 是否为管理员
        """
        return self.role == UserRoles.ADMIN
    
    def is_moderator(self):
        """检查是否为版主
        
        Returns:
            bool: 是否为版主
        """
        return self.role == UserRoles.MODERATOR
    
    def has_permission(self, permission):
        """检查是否有指定权限
        
        Args:
            permission (str): 权限名称
            
        Returns:
            bool: 是否有权限
        """
        user_permissions = UserRoles.PERMISSIONS.get(self.role, [])
        return permission in user_permissions
    
    def update_last_login(self):
        """更新最后登录时间"""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self, include_sensitive=False):
        """转换为字典
        
        Args:
            include_sensitive (bool): 是否包含敏感信息
            
        Returns:
            dict: 用户信息字典
        """
        result = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'book_count': self.books.count()
        }
        
        if include_sensitive:
            result['password_hash'] = self.password_hash
        
        return result
    
    @staticmethod
    def validate_username(username):
        """验证用户名
        
        Args:
            username (str): 用户名
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not username or len(username.strip()) == 0:
            return False, "用户名不能为空"
        
        username = username.strip()
        
        if len(username) < 3:
            return False, "用户名长度至少3个字符"
        
        if len(username) > 20:
            return False, "用户名长度不能超过20个字符"
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "用户名只能包含字母、数字和下划线"
        
        return True, "用户名格式正确"
    
    @staticmethod
    def validate_email(email):
        """验证邮箱
        
        Args:
            email (str): 邮箱
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not email or len(email.strip()) == 0:
            return False, "邮箱不能为空"
        
        email = email.strip().lower()
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, email):
            return False, "邮箱格式无效"
        
        return True, "邮箱格式正确"
    
    @staticmethod
    def validate_password(password):
        """验证密码
        
        Args:
            password (str): 密码
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not password:
            return False, "密码不能为空"
        
        if len(password) < 8:
            return False, "密码长度至少8个字符"
        
        if len(password) > 128:
            return False, "密码长度不能超过128个字符"
        
        if not re.search(r'\d', password):
            return False, "密码必须包含至少一个数字"
        
        if not re.search(r'[a-zA-Z]', password):
            return False, "密码必须包含至少一个字母"
        
        return True, "密码强度符合要求"
    
    def __repr__(self):
        return f'<User {self.username}>'

class Book(db.Model):
    """图书模型"""
    
    __tablename__ = 'books'
    
    # 基础字段
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    author = db.Column(db.String(100), nullable=False, index=True)
    isbn = db.Column(db.String(20), unique=True, index=True)
    
    # 图书信息
    category = db.Column(db.String(50), nullable=False, index=True)
    description = db.Column(db.Text)
    publisher = db.Column(db.String(100))
    publication_date = db.Column(db.Date)
    
    # 价格和库存
    price = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    stock = db.Column(db.Integer, nullable=False, default=0)
    
    # 状态
    is_available = db.Column(db.Boolean, nullable=False, default=True)
    
    # 时间戳
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 外键
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __init__(self, title, author, category, price=0.00, stock=0, 
                 isbn=None, description=None, publisher=None, 
                 publication_date=None, created_by=None):
        """初始化图书
        
        Args:
            title (str): 书名
            author (str): 作者
            category (str): 分类
            price (float): 价格
            stock (int): 库存
            isbn (str): ISBN
            description (str): 描述
            publisher (str): 出版社
            publication_date (date): 出版日期
            created_by (int): 创建者ID
        """
        self.title = title
        self.author = author
        self.category = category
        self.price = price
        self.stock = stock
        self.isbn = isbn
        self.description = description
        self.publisher = publisher
        self.publication_date = publication_date
        self.created_by = created_by
    
    def is_in_stock(self):
        """检查是否有库存
        
        Returns:
            bool: 是否有库存
        """
        return self.stock > 0 and self.is_available
    
    def update_stock(self, quantity):
        """更新库存
        
        Args:
            quantity (int): 库存变化量（正数增加，负数减少）
            
        Returns:
            bool: 是否更新成功
        """
        new_stock = self.stock + quantity
        if new_stock < 0:
            return False
        
        self.stock = new_stock
        return True
    
    def to_dict(self, include_creator=False):
        """转换为字典
        
        Args:
            include_creator (bool): 是否包含创建者信息
            
        Returns:
            dict: 图书信息字典
        """
        result = {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'category': self.category,
            'description': self.description,
            'publisher': self.publisher,
            'publication_date': self.publication_date.isoformat() if self.publication_date else None,
            'price': float(self.price) if self.price else 0.00,
            'stock': self.stock,
            'is_available': self.is_available,
            'is_in_stock': self.is_in_stock(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by
        }
        
        if include_creator and self.creator:
            result['creator'] = {
                'id': self.creator.id,
                'username': self.creator.username
            }
        
        return result
    
    @staticmethod
    def validate_title(title):
        """验证书名
        
        Args:
            title (str): 书名
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not title or len(title.strip()) == 0:
            return False, "书名不能为空"
        
        title = title.strip()
        
        if len(title) > 200:
            return False, "书名长度不能超过200个字符"
        
        return True, "书名格式正确"
    
    @staticmethod
    def validate_author(author):
        """验证作者
        
        Args:
            author (str): 作者
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not author or len(author.strip()) == 0:
            return False, "作者不能为空"
        
        author = author.strip()
        
        if len(author) > 100:
            return False, "作者名长度不能超过100个字符"
        
        return True, "作者格式正确"
    
    @staticmethod
    def validate_category(category):
        """验证分类
        
        Args:
            category (str): 分类
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not category:
            return False, "分类不能为空"
        
        if category not in BookCategories.ALL_CATEGORIES:
            return False, f"无效的分类，可选分类: {', '.join(BookCategories.ALL_CATEGORIES)}"
        
        return True, "分类格式正确"
    
    @staticmethod
    def validate_isbn(isbn):
        """验证ISBN
        
        Args:
            isbn (str): ISBN
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not isbn:
            return True, "ISBN可以为空"
        
        isbn = isbn.strip().replace('-', '').replace(' ', '')
        
        # 简单的ISBN验证（10位或13位数字）
        if not (len(isbn) == 10 or len(isbn) == 13):
            return False, "ISBN必须是10位或13位"
        
        if not isbn.replace('X', '').replace('x', '').isdigit():
            return False, "ISBN只能包含数字和X"
        
        return True, "ISBN格式正确"
    
    @staticmethod
    def validate_price(price):
        """验证价格
        
        Args:
            price (float): 价格
            
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            price = float(price)
        except (TypeError, ValueError):
            return False, "价格必须是数字"
        
        if price < 0:
            return False, "价格不能为负数"
        
        if price > 99999.99:
            return False, "价格不能超过99999.99"
        
        return True, "价格格式正确"
    
    @staticmethod
    def validate_stock(stock):
        """验证库存
        
        Args:
            stock (int): 库存
            
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            stock = int(stock)
        except (TypeError, ValueError):
            return False, "库存必须是整数"
        
        if stock < 0:
            return False, "库存不能为负数"
        
        if stock > 999999:
            return False, "库存不能超过999999"
        
        return True, "库存格式正确"
    
    @classmethod
    def search(cls, query, category=None, page=1, per_page=10):
        """搜索图书
        
        Args:
            query (str): 搜索关键词
            category (str): 分类筛选
            page (int): 页码
            per_page (int): 每页数量
            
        Returns:
            Pagination: 分页结果
        """
        # 构建查询
        book_query = cls.query.filter(cls.is_available == True)
        
        # 关键词搜索
        if query:
            search_filter = db.or_(
                cls.title.contains(query),
                cls.author.contains(query),
                cls.description.contains(query)
            )
            book_query = book_query.filter(search_filter)
        
        # 分类筛选
        if category and category in BookCategories.ALL_CATEGORIES:
            book_query = book_query.filter(cls.category == category)
        
        # 排序和分页
        return book_query.order_by(cls.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
    
    @classmethod
    def get_statistics(cls):
        """获取图书统计信息
        
        Returns:
            dict: 统计信息
        """
        total_books = cls.query.count()
        available_books = cls.query.filter(cls.is_available == True).count()
        in_stock_books = cls.query.filter(
            cls.is_available == True, cls.stock > 0
        ).count()
        
        # 按分类统计
        category_stats = {}
        for category in BookCategories.ALL_CATEGORIES:
            count = cls.query.filter(
                cls.category == category, cls.is_available == True
            ).count()
            if count > 0:
                category_stats[category] = count
        
        return {
            'total_books': total_books,
            'available_books': available_books,
            'in_stock_books': in_stock_books,
            'out_of_stock_books': available_books - in_stock_books,
            'category_distribution': category_stats
        }
    
    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'

# 数据库初始化函数
def init_db(app):
    """初始化数据库
    
    Args:
        app: Flask应用实例
    """
    db.init_app(app)
    
    with app.app_context():
        # 创建所有表
        db.create_all()
        
        # 创建默认管理员用户
        if not User.query.filter_by(username='admin').first():
            admin_user = User(
                username='admin',
                email='admin@example.com',
                password='admin123',
                role=UserRoles.ADMIN
            )
            db.session.add(admin_user)
        
        # 创建默认普通用户
        if not User.query.filter_by(username='user1').first():
            normal_user = User(
                username='user1',
                email='user1@example.com',
                password='user123',
                role=UserRoles.USER
            )
            db.session.add(normal_user)
        
        # 提交更改
        db.session.commit()
        
        print("数据库初始化完成")
        print("默认用户:")
        print("  管理员: admin / admin123")
        print("  普通用户: user1 / user123")

def create_sample_books(app):
    """创建示例图书数据
    
    Args:
        app: Flask应用实例
    """
    with app.app_context():
        # 检查是否已有图书数据
        if Book.query.count() > 0:
            return
        
        # 获取管理员用户
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            return
        
        # 示例图书数据
        sample_books = [
            {
                'title': 'Python编程从入门到实践',
                'author': 'Eric Matthes',
                'category': BookCategories.TECHNOLOGY,
                'description': '一本针对所有层次Python读者而作的Python入门书',
                'publisher': '人民邮电出版社',
                'price': 89.00,
                'stock': 50,
                'isbn': '9787115428028'
            },
            {
                'title': '流畅的Python',
                'author': 'Luciano Ramalho',
                'category': BookCategories.TECHNOLOGY,
                'description': '致力于帮助Python开发人员挖掘这门语言及相关库的优秀特性',
                'publisher': '人民邮电出版社',
                'price': 139.00,
                'stock': 30,
                'isbn': '9787115454157'
            },
            {
                'title': '三体',
                'author': '刘慈欣',
                'category': BookCategories.FICTION,
                'description': '中国科幻文学的里程碑之作',
                'publisher': '重庆出版社',
                'price': 23.00,
                'stock': 100,
                'isbn': '9787536692930'
            },
            {
                'title': '人类简史',
                'author': '尤瓦尔·赫拉利',
                'category': BookCategories.HISTORY,
                'description': '从动物到上帝的人类发展史',
                'publisher': '中信出版社',
                'price': 68.00,
                'stock': 75,
                'isbn': '9787508647357'
            },
            {
                'title': '算法导论',
                'author': 'Thomas H. Cormen',
                'category': BookCategories.TECHNOLOGY,
                'description': '计算机算法领域的经典教材',
                'publisher': '机械工业出版社',
                'price': 128.00,
                'stock': 25,
                'isbn': '9787111407010'
            }
        ]
        
        # 创建图书记录
        for book_data in sample_books:
            book = Book(
                title=book_data['title'],
                author=book_data['author'],
                category=book_data['category'],
                description=book_data['description'],
                publisher=book_data['publisher'],
                price=book_data['price'],
                stock=book_data['stock'],
                isbn=book_data['isbn'],
                created_by=admin_user.id
            )
            db.session.add(book)
        
        # 提交更改
        db.session.commit()
        print(f"已创建 {len(sample_books)} 本示例图书")