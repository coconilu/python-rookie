#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session20 API开发示例 - 基础API示例
演示如何使用Flask-RESTful创建基本的API

作者: Python学习教程
日期: 2024
"""

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import json
from datetime import datetime

# 创建Flask应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'demo-secret-key'

# 创建API实例
api = Api(app)

# 模拟数据存储
books_data = [
    {
        'id': 1,
        'title': 'Python编程入门',
        'author': '张三',
        'price': 59.9,
        'category': '编程',
        'created_at': '2024-01-01T10:00:00'
    },
    {
        'id': 2,
        'title': 'Web开发实战',
        'author': '李四',
        'price': 79.9,
        'category': '编程',
        'created_at': '2024-01-02T11:00:00'
    },
    {
        'id': 3,
        'title': '数据结构与算法',
        'author': '王五',
        'price': 89.9,
        'category': '算法',
        'created_at': '2024-01-03T12:00:00'
    }
]

# 全局变量用于生成新ID
next_id = 4

class BookListAPI(Resource):
    """图书列表API资源"""
    
    def get(self):
        """获取图书列表
        
        查询参数:
        - category: 按分类筛选
        - search: 搜索关键词
        - page: 页码 (默认1)
        - per_page: 每页数量 (默认10)
        """
        try:
            # 获取查询参数
            category = request.args.get('category')
            search = request.args.get('search')
            page = int(request.args.get('page', 1))
            per_page = min(int(request.args.get('per_page', 10)), 100)
            
            # 过滤数据
            filtered_books = books_data.copy()
            
            # 按分类筛选
            if category:
                filtered_books = [book for book in filtered_books 
                                if book['category'].lower() == category.lower()]
            
            # 搜索功能
            if search:
                search_lower = search.lower()
                filtered_books = [book for book in filtered_books 
                                if search_lower in book['title'].lower() or 
                                   search_lower in book['author'].lower()]
            
            # 分页处理
            total = len(filtered_books)
            start = (page - 1) * per_page
            end = start + per_page
            paginated_books = filtered_books[start:end]
            
            # 构造响应
            response = {
                'success': True,
                'data': paginated_books,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': (total + per_page - 1) // per_page
                }
            }
            
            return response, 200
            
        except ValueError:
            return {
                'success': False,
                'message': '页码和每页数量必须是数字'
            }, 400
        except Exception as e:
            return {
                'success': False,
                'message': f'获取图书列表失败: {str(e)}'
            }, 500
    
    def post(self):
        """创建新图书
        
        请求体:
        {
            "title": "图书标题",
            "author": "作者",
            "price": 价格,
            "category": "分类"
        }
        """
        try:
            # 获取请求数据
            data = request.get_json()
            
            if not data:
                return {
                    'success': False,
                    'message': '请求体不能为空'
                }, 400
            
            # 验证必需字段
            required_fields = ['title', 'author', 'price', 'category']
            for field in required_fields:
                if field not in data or not data[field]:
                    return {
                        'success': False,
                        'message': f'缺少必需字段: {field}'
                    }, 400
            
            # 验证数据类型
            try:
                price = float(data['price'])
                if price <= 0:
                    return {
                        'success': False,
                        'message': '价格必须大于0'
                    }, 400
            except (ValueError, TypeError):
                return {
                    'success': False,
                    'message': '价格必须是有效数字'
                }, 400
            
            # 创建新图书
            global next_id
            new_book = {
                'id': next_id,
                'title': data['title'].strip(),
                'author': data['author'].strip(),
                'price': price,
                'category': data['category'].strip(),
                'created_at': datetime.now().isoformat()
            }
            
            books_data.append(new_book)
            next_id += 1
            
            return {
                'success': True,
                'message': '图书创建成功',
                'data': new_book
            }, 201
            
        except Exception as e:
            return {
                'success': False,
                'message': f'创建图书失败: {str(e)}'
            }, 500

class BookAPI(Resource):
    """单个图书API资源"""
    
    def get(self, book_id):
        """获取指定ID的图书"""
        try:
            # 查找图书
            book = next((book for book in books_data if book['id'] == book_id), None)
            
            if not book:
                return {
                    'success': False,
                    'message': '图书不存在'
                }, 404
            
            return {
                'success': True,
                'data': book
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'获取图书失败: {str(e)}'
            }, 500
    
    def put(self, book_id):
        """更新指定ID的图书"""
        try:
            # 查找图书
            book = next((book for book in books_data if book['id'] == book_id), None)
            
            if not book:
                return {
                    'success': False,
                    'message': '图书不存在'
                }, 404
            
            # 获取更新数据
            data = request.get_json()
            if not data:
                return {
                    'success': False,
                    'message': '请求体不能为空'
                }, 400
            
            # 更新字段
            updatable_fields = ['title', 'author', 'price', 'category']
            for field in updatable_fields:
                if field in data:
                    if field == 'price':
                        try:
                            price = float(data[field])
                            if price <= 0:
                                return {
                                    'success': False,
                                    'message': '价格必须大于0'
                                }, 400
                            book[field] = price
                        except (ValueError, TypeError):
                            return {
                                'success': False,
                                'message': '价格必须是有效数字'
                            }, 400
                    else:
                        book[field] = str(data[field]).strip()
            
            return {
                'success': True,
                'message': '图书更新成功',
                'data': book
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'更新图书失败: {str(e)}'
            }, 500
    
    def delete(self, book_id):
        """删除指定ID的图书"""
        try:
            # 查找图书索引
            book_index = next((i for i, book in enumerate(books_data) 
                             if book['id'] == book_id), None)
            
            if book_index is None:
                return {
                    'success': False,
                    'message': '图书不存在'
                }, 404
            
            # 删除图书
            deleted_book = books_data.pop(book_index)
            
            return {
                'success': True,
                'message': '图书删除成功',
                'data': deleted_book
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'删除图书失败: {str(e)}'
            }, 500

class StatsAPI(Resource):
    """统计信息API资源"""
    
    def get(self):
        """获取统计信息"""
        try:
            # 计算统计信息
            total_books = len(books_data)
            categories = {}
            total_value = 0
            
            for book in books_data:
                # 统计分类
                category = book['category']
                categories[category] = categories.get(category, 0) + 1
                
                # 计算总价值
                total_value += book['price']
            
            # 平均价格
            avg_price = total_value / total_books if total_books > 0 else 0
            
            stats = {
                'total_books': total_books,
                'categories': categories,
                'total_value': round(total_value, 2),
                'average_price': round(avg_price, 2)
            }
            
            return {
                'success': True,
                'data': stats
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'获取统计信息失败: {str(e)}'
            }, 500

# 注册API路由
api.add_resource(BookListAPI, '/api/books')
api.add_resource(BookAPI, '/api/books/<int:book_id>')
api.add_resource(StatsAPI, '/api/stats')

# 根路径处理
@app.route('/')
def index():
    """API首页"""
    return jsonify({
        'message': 'Welcome to Book API',
        'version': '1.0.0',
        'endpoints': {
            'books': {
                'GET /api/books': '获取图书列表',
                'POST /api/books': '创建新图书',
                'GET /api/books/{id}': '获取指定图书',
                'PUT /api/books/{id}': '更新指定图书',
                'DELETE /api/books/{id}': '删除指定图书'
            },
            'stats': {
                'GET /api/stats': '获取统计信息'
            }
        },
        'examples': {
            'get_books': 'GET /api/books?category=编程&page=1&per_page=5',
            'create_book': 'POST /api/books with JSON body',
            'search_books': 'GET /api/books?search=Python'
        }
    })

# 错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': '请求的资源不存在'
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'message': '不支持的HTTP方法'
    }), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'message': '服务器内部错误'
    }), 500

if __name__ == '__main__':
    print("🚀 启动基础API演示服务...")
    print("📚 图书管理API")
    print("🌐 访问地址: http://localhost:5000")
    print("📖 API文档: http://localhost:5000")
    print("\n可用端点:")
    print("  GET    /api/books       - 获取图书列表")
    print("  POST   /api/books       - 创建新图书")
    print("  GET    /api/books/{id}  - 获取指定图书")
    print("  PUT    /api/books/{id}  - 更新指定图书")
    print("  DELETE /api/books/{id}  - 删除指定图书")
    print("  GET    /api/stats       - 获取统计信息")
    print("\n按 Ctrl+C 停止服务")
    print("="*50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)