#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session20 API开发演示项目 - 主应用文件
图书管理系统API服务

作者: Python学习教程
日期: 2024
"""

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import json

# 应用配置
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# 扩展初始化
db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)
CORS(app)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# 数据模型
class User(db.Model):
    """用户模型"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat()
        }

class Book(db.Model):
    """图书模型"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'price': self.price,
            'stock': self.stock,
            'category': self.category,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# API资源类
class BookListResource(Resource):
    """图书列表资源"""
    
    @limiter.limit("30 per minute")
    def get(self):
        """获取图书列表"""
        try:
            # 获取查询参数
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', 10, type=int), 100)
            category = request.args.get('category')
            search = request.args.get('search')
            
            # 构建查询
            query = Book.query
            
            if category:
                query = query.filter(Book.category == category)
            
            if search:
                query = query.filter(
                    db.or_(
                        Book.title.contains(search),
                        Book.author.contains(search)
                    )
                )
            
            # 分页查询
            pagination = query.paginate(
                page=page, 
                per_page=per_page, 
                error_out=False
            )
            
            books = [book.to_dict() for book in pagination.items]
            
            return {
                'success': True,
                'data': books,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': pagination.total,
                    'pages': pagination.pages,
                    'has_next': pagination.has_next,
                    'has_prev': pagination.has_prev
                }
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'获取图书列表失败: {str(e)}'
            }, 500
    
    @jwt_required()
    @limiter.limit("10 per minute")
    def post(self):
        """创建新图书"""
        try:
            data = request.get_json()
            
            # 验证必需字段
            required_fields = ['title', 'author', 'isbn', 'price', 'category']
            for field in required_fields:
                if field not in data:
                    return {
                        'success': False,
                        'message': f'缺少必需字段: {field}'
                    }, 400
            
            # 检查ISBN是否已存在
            if Book.query.filter_by(isbn=data['isbn']).first():
                return {
                    'success': False,
                    'message': 'ISBN已存在'
                }, 400
            
            # 创建新图书
            book = Book(
                title=data['title'],
                author=data['author'],
                isbn=data['isbn'],
                price=float(data['price']),
                stock=data.get('stock', 0),
                category=data['category'],
                description=data.get('description', '')
            )
            
            db.session.add(book)
            db.session.commit()
            
            return {
                'success': True,
                'message': '图书创建成功',
                'data': book.to_dict()
            }, 201
            
        except ValueError as e:
            return {
                'success': False,
                'message': '数据格式错误'
            }, 400
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'创建图书失败: {str(e)}'
            }, 500

class BookResource(Resource):
    """单个图书资源"""
    
    def get(self, book_id):
        """获取单个图书"""
        try:
            book = Book.query.get_or_404(book_id)
            return {
                'success': True,
                'data': book.to_dict()
            }, 200
        except Exception as e:
            return {
                'success': False,
                'message': '图书不存在'
            }, 404
    
    @jwt_required()
    def put(self, book_id):
        """更新图书信息"""
        try:
            book = Book.query.get_or_404(book_id)
            data = request.get_json()
            
            # 更新字段
            updatable_fields = ['title', 'author', 'price', 'stock', 'category', 'description']
            for field in updatable_fields:
                if field in data:
                    setattr(book, field, data[field])
            
            book.updated_at = datetime.utcnow()
            db.session.commit()
            
            return {
                'success': True,
                'message': '图书更新成功',
                'data': book.to_dict()
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'更新图书失败: {str(e)}'
            }, 500
    
    @jwt_required()
    def delete(self, book_id):
        """删除图书"""
        try:
            book = Book.query.get_or_404(book_id)
            db.session.delete(book)
            db.session.commit()
            
            return {
                'success': True,
                'message': '图书删除成功'
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'删除图书失败: {str(e)}'
            }, 500

class AuthResource(Resource):
    """认证资源"""
    
    @limiter.limit("5 per minute")
    def post(self):
        """用户登录"""
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return {
                    'success': False,
                    'message': '用户名和密码不能为空'
                }, 400
            
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                access_token = create_access_token(
                    identity=user.id,
                    additional_claims={'username': user.username, 'is_admin': user.is_admin}
                )
                
                return {
                    'success': True,
                    'message': '登录成功',
                    'data': {
                        'access_token': access_token,
                        'user': user.to_dict()
                    }
                }, 200
            else:
                return {
                    'success': False,
                    'message': '用户名或密码错误'
                }, 401
                
        except Exception as e:
            return {
                'success': False,
                'message': f'登录失败: {str(e)}'
            }, 500

class UserResource(Resource):
    """用户资源"""
    
    @limiter.limit("3 per minute")
    def post(self):
        """用户注册"""
        try:
            data = request.get_json()
            
            # 验证必需字段
            required_fields = ['username', 'email', 'password']
            for field in required_fields:
                if field not in data:
                    return {
                        'success': False,
                        'message': f'缺少必需字段: {field}'
                    }, 400
            
            # 检查用户名是否已存在
            if User.query.filter_by(username=data['username']).first():
                return {
                    'success': False,
                    'message': '用户名已存在'
                }, 400
            
            # 检查邮箱是否已存在
            if User.query.filter_by(email=data['email']).first():
                return {
                    'success': False,
                    'message': '邮箱已存在'
                }, 400
            
            # 创建新用户
            user = User(
                username=data['username'],
                email=data['email']
            )
            user.set_password(data['password'])
            
            db.session.add(user)
            db.session.commit()
            
            return {
                'success': True,
                'message': '用户注册成功',
                'data': user.to_dict()
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'注册失败: {str(e)}'
            }, 500

# 注册API路由
api.add_resource(BookListResource, '/api/books')
api.add_resource(BookResource, '/api/books/<int:book_id>')
api.add_resource(AuthResource, '/api/auth/login')
api.add_resource(UserResource, '/api/auth/register')

# 错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': '资源不存在'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'message': '服务器内部错误'
    }), 500

# 初始化数据库
def init_db():
    """初始化数据库"""
    with app.app_context():
        db.create_all()
        
        # 创建管理员用户
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@example.com',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
        
        # 添加示例图书
        if Book.query.count() == 0:
            sample_books = [
                {
                    'title': 'Python编程：从入门到实践',
                    'author': 'Eric Matthes',
                    'isbn': '9787115428028',
                    'price': 89.0,
                    'stock': 50,
                    'category': '编程',
                    'description': 'Python编程入门经典教程'
                },
                {
                    'title': '流畅的Python',
                    'author': 'Luciano Ramalho',
                    'isbn': '9787115454157',
                    'price': 139.0,
                    'stock': 30,
                    'category': '编程',
                    'description': 'Python进阶必读书籍'
                },
                {
                    'title': '算法导论',
                    'author': 'Thomas H. Cormen',
                    'isbn': '9787111407010',
                    'price': 128.0,
                    'stock': 20,
                    'category': '算法',
                    'description': '计算机算法经典教材'
                }
            ]
            
            for book_data in sample_books:
                book = Book(**book_data)
                db.session.add(book)
        
        db.session.commit()
        print("数据库初始化完成！")

if __name__ == '__main__':
    init_db()
    print("图书管理API服务启动中...")
    print("API文档: http://localhost:5000/")
    print("管理员账号: admin / admin123")
    app.run(debug=True, host='0.0.0.0', port=5000)