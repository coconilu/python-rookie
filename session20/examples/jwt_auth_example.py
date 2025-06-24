#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session20 API开发示例 - JWT认证示例
演示如何在Flask API中实现JWT用户认证

作者: Python学习教程
日期: 2024
"""

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json

# 创建Flask应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'jwt-demo-secret-key'
app.config['JWT_SECRET_KEY'] = 'jwt-super-secret-string'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

# 初始化扩展
api = Api(app)
jwt = JWTManager(app)

# 模拟用户数据存储
users_data = [
    {
        'id': 1,
        'username': 'admin',
        'email': 'admin@example.com',
        'password_hash': generate_password_hash('admin123'),
        'role': 'admin',
        'created_at': '2024-01-01T10:00:00'
    },
    {
        'id': 2,
        'username': 'user1',
        'email': 'user1@example.com',
        'password_hash': generate_password_hash('user123'),
        'role': 'user',
        'created_at': '2024-01-02T11:00:00'
    }
]

# 黑名单Token存储（实际项目中应使用Redis等）
blacklisted_tokens = set()

# JWT回调函数
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    """检查token是否在黑名单中"""
    jti = jwt_payload['jti']
    return jti in blacklisted_tokens

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """Token过期时的回调"""
    return jsonify({
        'success': False,
        'message': 'Token已过期，请重新登录'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    """无效Token时的回调"""
    return jsonify({
        'success': False,
        'message': 'Token无效，请重新登录'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    """缺少Token时的回调"""
    return jsonify({
        'success': False,
        'message': '需要提供访问令牌'
    }), 401

# 辅助函数
def find_user_by_username(username):
    """根据用户名查找用户"""
    return next((user for user in users_data if user['username'] == username), None)

def find_user_by_id(user_id):
    """根据ID查找用户"""
    return next((user for user in users_data if user['id'] == user_id), None)

def user_to_dict(user, include_sensitive=False):
    """将用户对象转换为字典"""
    result = {
        'id': user['id'],
        'username': user['username'],
        'email': user['email'],
        'role': user['role'],
        'created_at': user['created_at']
    }
    if include_sensitive:
        result['password_hash'] = user['password_hash']
    return result

# 权限装饰器
def admin_required(f):
    """需要管理员权限的装饰器"""
    from functools import wraps
    
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        current_user = find_user_by_id(current_user_id)
        
        if not current_user or current_user['role'] != 'admin':
            return jsonify({
                'success': False,
                'message': '需要管理员权限'
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function

# API资源类
class RegisterAPI(Resource):
    """用户注册API"""
    
    def post(self):
        """用户注册
        
        请求体:
        {
            "username": "用户名",
            "email": "邮箱",
            "password": "密码"
        }
        """
        try:
            data = request.get_json()
            
            if not data:
                return {
                    'success': False,
                    'message': '请求体不能为空'
                }, 400
            
            # 验证必需字段
            required_fields = ['username', 'email', 'password']
            for field in required_fields:
                if field not in data or not data[field]:
                    return {
                        'success': False,
                        'message': f'缺少必需字段: {field}'
                    }, 400
            
            username = data['username'].strip()
            email = data['email'].strip()
            password = data['password']
            
            # 验证用户名长度
            if len(username) < 3 or len(username) > 20:
                return {
                    'success': False,
                    'message': '用户名长度必须在3-20个字符之间'
                }, 400
            
            # 验证密码长度
            if len(password) < 6:
                return {
                    'success': False,
                    'message': '密码长度至少6个字符'
                }, 400
            
            # 检查用户名是否已存在
            if find_user_by_username(username):
                return {
                    'success': False,
                    'message': '用户名已存在'
                }, 400
            
            # 检查邮箱是否已存在
            if any(user['email'] == email for user in users_data):
                return {
                    'success': False,
                    'message': '邮箱已存在'
                }, 400
            
            # 创建新用户
            new_user = {
                'id': len(users_data) + 1,
                'username': username,
                'email': email,
                'password_hash': generate_password_hash(password),
                'role': 'user',
                'created_at': datetime.now().isoformat()
            }
            
            users_data.append(new_user)
            
            return {
                'success': True,
                'message': '用户注册成功',
                'data': user_to_dict(new_user)
            }, 201
            
        except Exception as e:
            return {
                'success': False,
                'message': f'注册失败: {str(e)}'
            }, 500

class LoginAPI(Resource):
    """用户登录API"""
    
    def post(self):
        """用户登录
        
        请求体:
        {
            "username": "用户名",
            "password": "密码"
        }
        """
        try:
            data = request.get_json()
            
            if not data:
                return {
                    'success': False,
                    'message': '请求体不能为空'
                }, 400
            
            username = data.get('username', '').strip()
            password = data.get('password', '')
            
            if not username or not password:
                return {
                    'success': False,
                    'message': '用户名和密码不能为空'
                }, 400
            
            # 查找用户
            user = find_user_by_username(username)
            
            if not user or not check_password_hash(user['password_hash'], password):
                return {
                    'success': False,
                    'message': '用户名或密码错误'
                }, 401
            
            # 创建Token
            additional_claims = {
                'username': user['username'],
                'role': user['role']
            }
            
            access_token = create_access_token(
                identity=user['id'],
                additional_claims=additional_claims
            )
            
            refresh_token = create_refresh_token(
                identity=user['id'],
                additional_claims=additional_claims
            )
            
            return {
                'success': True,
                'message': '登录成功',
                'data': {
                    'user': user_to_dict(user),
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'登录失败: {str(e)}'
            }, 500

class RefreshAPI(Resource):
    """刷新Token API"""
    
    @jwt_required(refresh=True)
    def post(self):
        """刷新访问令牌"""
        try:
            current_user_id = get_jwt_identity()
            current_user = find_user_by_id(current_user_id)
            
            if not current_user:
                return {
                    'success': False,
                    'message': '用户不存在'
                }, 404
            
            # 创建新的访问令牌
            additional_claims = {
                'username': current_user['username'],
                'role': current_user['role']
            }
            
            new_access_token = create_access_token(
                identity=current_user_id,
                additional_claims=additional_claims
            )
            
            return {
                'success': True,
                'message': 'Token刷新成功',
                'data': {
                    'access_token': new_access_token
                }
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Token刷新失败: {str(e)}'
            }, 500

class LogoutAPI(Resource):
    """用户登出API"""
    
    @jwt_required()
    def post(self):
        """用户登出（将Token加入黑名单）"""
        try:
            jti = get_jwt()['jti']
            blacklisted_tokens.add(jti)
            
            return {
                'success': True,
                'message': '登出成功'
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'登出失败: {str(e)}'
            }, 500

class ProfileAPI(Resource):
    """用户资料API"""
    
    @jwt_required()
    def get(self):
        """获取当前用户资料"""
        try:
            current_user_id = get_jwt_identity()
            current_user = find_user_by_id(current_user_id)
            
            if not current_user:
                return {
                    'success': False,
                    'message': '用户不存在'
                }, 404
            
            return {
                'success': True,
                'data': user_to_dict(current_user)
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'获取用户资料失败: {str(e)}'
            }, 500
    
    @jwt_required()
    def put(self):
        """更新当前用户资料"""
        try:
            current_user_id = get_jwt_identity()
            current_user = find_user_by_id(current_user_id)
            
            if not current_user:
                return {
                    'success': False,
                    'message': '用户不存在'
                }, 404
            
            data = request.get_json()
            if not data:
                return {
                    'success': False,
                    'message': '请求体不能为空'
                }, 400
            
            # 更新邮箱
            if 'email' in data:
                email = data['email'].strip()
                # 检查邮箱是否被其他用户使用
                if any(user['email'] == email and user['id'] != current_user_id 
                      for user in users_data):
                    return {
                        'success': False,
                        'message': '邮箱已被其他用户使用'
                    }, 400
                current_user['email'] = email
            
            # 更新密码
            if 'password' in data:
                password = data['password']
                if len(password) < 6:
                    return {
                        'success': False,
                        'message': '密码长度至少6个字符'
                    }, 400
                current_user['password_hash'] = generate_password_hash(password)
            
            return {
                'success': True,
                'message': '用户资料更新成功',
                'data': user_to_dict(current_user)
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'更新用户资料失败: {str(e)}'
            }, 500

class UsersAPI(Resource):
    """用户管理API（仅管理员）"""
    
    @admin_required
    def get(self):
        """获取所有用户列表（仅管理员）"""
        try:
            users = [user_to_dict(user) for user in users_data]
            
            return {
                'success': True,
                'data': users,
                'total': len(users)
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'获取用户列表失败: {str(e)}'
            }, 500

class ProtectedAPI(Resource):
    """受保护的API示例"""
    
    @jwt_required()
    def get(self):
        """需要认证的API端点"""
        try:
            current_user_id = get_jwt_identity()
            current_user = find_user_by_id(current_user_id)
            
            # 获取JWT中的额外信息
            claims = get_jwt()
            
            return {
                'success': True,
                'message': '这是一个受保护的API端点',
                'data': {
                    'current_user': user_to_dict(current_user),
                    'token_info': {
                        'jti': claims['jti'],
                        'exp': claims['exp'],
                        'iat': claims['iat'],
                        'username': claims.get('username'),
                        'role': claims.get('role')
                    }
                }
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'访问受保护资源失败: {str(e)}'
            }, 500

# 注册API路由
api.add_resource(RegisterAPI, '/api/auth/register')
api.add_resource(LoginAPI, '/api/auth/login')
api.add_resource(RefreshAPI, '/api/auth/refresh')
api.add_resource(LogoutAPI, '/api/auth/logout')
api.add_resource(ProfileAPI, '/api/auth/profile')
api.add_resource(UsersAPI, '/api/admin/users')
api.add_resource(ProtectedAPI, '/api/protected')

# 根路径处理
@app.route('/')
def index():
    """API首页"""
    return jsonify({
        'message': 'JWT Authentication API Demo',
        'version': '1.0.0',
        'endpoints': {
            'auth': {
                'POST /api/auth/register': '用户注册',
                'POST /api/auth/login': '用户登录',
                'POST /api/auth/refresh': '刷新Token',
                'POST /api/auth/logout': '用户登出',
                'GET /api/auth/profile': '获取用户资料',
                'PUT /api/auth/profile': '更新用户资料'
            },
            'admin': {
                'GET /api/admin/users': '获取用户列表（仅管理员）'
            },
            'protected': {
                'GET /api/protected': '受保护的API端点'
            }
        },
        'default_users': {
            'admin': {'username': 'admin', 'password': 'admin123', 'role': 'admin'},
            'user': {'username': 'user1', 'password': 'user123', 'role': 'user'}
        },
        'usage': {
            'login': 'POST /api/auth/login with username and password',
            'access_protected': 'Add "Authorization: Bearer <token>" header',
            'refresh_token': 'POST /api/auth/refresh with refresh token'
        }
    })

if __name__ == '__main__':
    print("🚀 启动JWT认证API演示服务...")
    print("🔐 JWT用户认证系统")
    print("🌐 访问地址: http://localhost:5001")
    print("📖 API文档: http://localhost:5001")
    print("\n默认用户:")
    print("  管理员: admin / admin123")
    print("  普通用户: user1 / user123")
    print("\n认证流程:")
    print("  1. POST /api/auth/login 获取Token")
    print("  2. 在请求头中添加: Authorization: Bearer <token>")
    print("  3. 访问受保护的API端点")
    print("\n按 Ctrl+C 停止服务")
    print("="*50)
    
    app.run(debug=True, host='0.0.0.0', port=5001)