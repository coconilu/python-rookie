#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session20 API开发练习2参考答案 - JWT认证系统
用户管理和认证系统完整实现

功能特性:
1. 用户注册和登录
2. JWT Token管理
3. 权限控制
4. 用户资料管理
5. 管理员功能
6. Token黑名单

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
from functools import wraps
import re
import uuid

# Flask应用配置
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
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
        'is_active': True,
        'created_at': '2024-01-01T10:00:00'
    },
    {
        'id': 2,
        'username': 'user1',
        'email': 'user1@example.com',
        'password_hash': generate_password_hash('user123'),
        'role': 'user',
        'is_active': True,
        'created_at': '2024-01-02T11:00:00'
    }
]

# 黑名单Token存储
blacklisted_tokens = set()
next_user_id = 3

# JWT回调函数
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    """检查Token是否在黑名单中"""
    jti = jwt_payload['jti']
    return jti in blacklisted_tokens

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """Token过期回调"""
    return jsonify({
        'error': 'Token已过期',
        'message': '请重新登录或刷新Token'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    """无效Token回调"""
    return jsonify({
        'error': '无效的Token',
        'message': '请提供有效的访问令牌'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    """缺少Token回调"""
    return jsonify({
        'error': '需要认证',
        'message': '请提供访问令牌'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    """被撤销Token回调"""
    return jsonify({
        'error': 'Token已被撤销',
        'message': '请重新登录'
    }), 401

# 权限装饰器
def admin_required(f):
    """需要管理员权限的装饰器"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = find_user_by_id(current_user_id)
        
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
        if user['role'] != 'admin':
            return jsonify({
                'error': '权限不足',
                'message': '需要管理员权限'
            }), 403
        
        if not user['is_active']:
            return jsonify({
                'error': '账户已被禁用',
                'message': '请联系管理员'
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function

def active_user_required(f):
    """需要活跃用户的装饰器"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = find_user_by_id(current_user_id)
        
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
        if not user['is_active']:
            return jsonify({
                'error': '账户已被禁用',
                'message': '请联系管理员'
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function

# 辅助函数
def find_user_by_username(username):
    """根据用户名查找用户"""
    for user in users_data:
        if user['username'] == username:
            return user
    return None

def find_user_by_id(user_id):
    """根据ID查找用户"""
    for user in users_data:
        if user['id'] == user_id:
            return user
    return None

def find_user_by_email(email):
    """根据邮箱查找用户"""
    for user in users_data:
        if user['email'] == email:
            return user
    return None

def validate_email(email):
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """验证密码强度"""
    if len(password) < 8:
        return False, "密码长度至少8个字符"
    
    if not re.search(r'\d', password):
        return False, "密码必须包含至少一个数字"
    
    if not re.search(r'[a-zA-Z]', password):
        return False, "密码必须包含至少一个字母"
    
    return True, "密码强度符合要求"

def user_to_dict(user, include_sensitive=False):
    """将用户对象转换为字典"""
    result = {
        'id': user['id'],
        'username': user['username'],
        'email': user['email'],
        'role': user['role'],
        'is_active': user['is_active'],
        'created_at': user['created_at']
    }
    
    if include_sensitive:
        result['password_hash'] = user['password_hash']
    
    return result

class RegisterAPI(Resource):
    """用户注册API"""
    
    def post(self):
        """用户注册"""
        try:
            data = request.get_json()
            
            # 验证必需字段
            required_fields = ['username', 'email', 'password']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({
                        'error': f'缺少必需字段: {field}'
                    }), 400
            
            username = data['username'].strip()
            email = data['email'].strip().lower()
            password = data['password']
            
            # 验证用户名长度
            if len(username) < 3 or len(username) > 20:
                return jsonify({
                    'error': '用户名长度必须在3-20个字符之间'
                }), 400
            
            # 验证邮箱格式
            if not validate_email(email):
                return jsonify({
                    'error': '邮箱格式无效'
                }), 400
            
            # 验证密码强度
            is_valid, message = validate_password(password)
            if not is_valid:
                return jsonify({'error': message}), 400
            
            # 检查用户名是否已存在
            if find_user_by_username(username):
                return jsonify({
                    'error': '用户名已存在'
                }), 409
            
            # 检查邮箱是否已存在
            if find_user_by_email(email):
                return jsonify({
                    'error': '邮箱已被注册'
                }), 409
            
            # 创建新用户
            global next_user_id
            new_user = {
                'id': next_user_id,
                'username': username,
                'email': email,
                'password_hash': generate_password_hash(password),
                'role': 'user',
                'is_active': True,
                'created_at': datetime.now().isoformat()
            }
            
            users_data.append(new_user)
            next_user_id += 1
            
            return jsonify({
                'message': '注册成功',
                'user': user_to_dict(new_user)
            }), 201
            
        except Exception as e:
            return jsonify({
                'error': '注册失败',
                'message': str(e)
            }), 500

class LoginAPI(Resource):
    """用户登录API"""
    
    def post(self):
        """用户登录"""
        try:
            data = request.get_json()
            
            # 验证必需字段
            if not data.get('username') or not data.get('password'):
                return jsonify({
                    'error': '用户名和密码不能为空'
                }), 400
            
            username = data['username'].strip()
            password = data['password']
            
            # 查找用户
            user = find_user_by_username(username)
            if not user:
                return jsonify({
                    'error': '用户名或密码错误'
                }), 401
            
            # 验证密码
            if not check_password_hash(user['password_hash'], password):
                return jsonify({
                    'error': '用户名或密码错误'
                }), 401
            
            # 检查用户是否活跃
            if not user['is_active']:
                return jsonify({
                    'error': '账户已被禁用',
                    'message': '请联系管理员'
                }), 403
            
            # 生成Token
            access_token = create_access_token(
                identity=user['id'],
                additional_claims={'role': user['role']}
            )
            refresh_token = create_refresh_token(identity=user['id'])
            
            return jsonify({
                'message': '登录成功',
                'user': user_to_dict(user),
                'access_token': access_token,
                'refresh_token': refresh_token
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': '登录失败',
                'message': str(e)
            }), 500

class RefreshAPI(Resource):
    """刷新Token API"""
    
    @jwt_required(refresh=True)
    def post(self):
        """刷新访问令牌"""
        try:
            current_user_id = get_jwt_identity()
            user = find_user_by_id(current_user_id)
            
            if not user:
                return jsonify({'error': '用户不存在'}), 404
            
            if not user['is_active']:
                return jsonify({
                    'error': '账户已被禁用',
                    'message': '请联系管理员'
                }), 403
            
            # 生成新的访问令牌
            new_access_token = create_access_token(
                identity=current_user_id,
                additional_claims={'role': user['role']}
            )
            
            return jsonify({
                'message': 'Token刷新成功',
                'access_token': new_access_token
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': 'Token刷新失败',
                'message': str(e)
            }), 500

class LogoutAPI(Resource):
    """用户登出API"""
    
    @jwt_required()
    def post(self):
        """用户登出"""
        try:
            # 获取当前Token的JTI
            jti = get_jwt()['jti']
            
            # 将Token加入黑名单
            blacklisted_tokens.add(jti)
            
            return jsonify({
                'message': '登出成功'
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': '登出失败',
                'message': str(e)
            }), 500

class ProfileAPI(Resource):
    """用户资料API"""
    
    @active_user_required
    def get(self):
        """获取当前用户资料"""
        try:
            current_user_id = get_jwt_identity()
            user = find_user_by_id(current_user_id)
            
            return jsonify({
                'user': user_to_dict(user)
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': '获取用户资料失败',
                'message': str(e)
            }), 500
    
    @active_user_required
    def put(self):
        """更新当前用户资料"""
        try:
            current_user_id = get_jwt_identity()
            user = find_user_by_id(current_user_id)
            data = request.get_json()
            
            updated = False
            
            # 更新邮箱
            if 'email' in data:
                new_email = data['email'].strip().lower()
                if not validate_email(new_email):
                    return jsonify({'error': '邮箱格式无效'}), 400
                
                # 检查邮箱是否被其他用户使用
                existing_user = find_user_by_email(new_email)
                if existing_user and existing_user['id'] != current_user_id:
                    return jsonify({'error': '邮箱已被其他用户使用'}), 409
                
                user['email'] = new_email
                updated = True
            
            # 更新密码
            if 'password' in data:
                new_password = data['password']
                is_valid, message = validate_password(new_password)
                if not is_valid:
                    return jsonify({'error': message}), 400
                
                user['password_hash'] = generate_password_hash(new_password)
                updated = True
            
            if not updated:
                return jsonify({'error': '没有提供要更新的字段'}), 400
            
            return jsonify({
                'message': '用户资料更新成功',
                'user': user_to_dict(user)
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': '更新用户资料失败',
                'message': str(e)
            }), 500

class UsersAPI(Resource):
    """用户管理API（仅管理员）"""
    
    @admin_required
    def get(self):
        """获取所有用户列表（仅管理员）"""
        try:
            # 获取查询参数
            page = int(request.args.get('page', 1))
            per_page = min(int(request.args.get('per_page', 10)), 100)
            role_filter = request.args.get('role')
            is_active_filter = request.args.get('is_active')
            
            # 筛选用户
            filtered_users = users_data.copy()
            
            if role_filter:
                filtered_users = [u for u in filtered_users if u['role'] == role_filter]
            
            if is_active_filter is not None:
                is_active = is_active_filter.lower() == 'true'
                filtered_users = [u for u in filtered_users if u['is_active'] == is_active]
            
            # 分页
            total = len(filtered_users)
            start = (page - 1) * per_page
            end = start + per_page
            paginated_users = filtered_users[start:end]
            
            return jsonify({
                'users': [user_to_dict(user) for user in paginated_users],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': (total + per_page - 1) // per_page
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': '获取用户列表失败',
                'message': str(e)
            }), 500

class UserAPI(Resource):
    """单个用户管理API（仅管理员）"""
    
    @admin_required
    def get(self, user_id):
        """获取指定用户信息（仅管理员）"""
        try:
            user = find_user_by_id(user_id)
            if not user:
                return jsonify({'error': '用户不存在'}), 404
            
            return jsonify({
                'user': user_to_dict(user)
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': '获取用户信息失败',
                'message': str(e)
            }), 500
    
    @admin_required
    def put(self, user_id):
        """更新指定用户信息（仅管理员）"""
        try:
            user = find_user_by_id(user_id)
            if not user:
                return jsonify({'error': '用户不存在'}), 404
            
            data = request.get_json()
            updated = False
            
            # 更新角色
            if 'role' in data:
                new_role = data['role']
                if new_role not in ['user', 'admin']:
                    return jsonify({'error': '无效的角色'}), 400
                user['role'] = new_role
                updated = True
            
            # 更新活跃状态
            if 'is_active' in data:
                user['is_active'] = bool(data['is_active'])
                updated = True
            
            if not updated:
                return jsonify({'error': '没有提供要更新的字段'}), 400
            
            return jsonify({
                'message': '用户信息更新成功',
                'user': user_to_dict(user)
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': '更新用户信息失败',
                'message': str(e)
            }), 500
    
    @admin_required
    def delete(self, user_id):
        """删除指定用户（仅管理员）"""
        try:
            current_user_id = get_jwt_identity()
            
            # 不能删除自己
            if user_id == current_user_id:
                return jsonify({
                    'error': '不能删除自己的账户'
                }), 400
            
            user = find_user_by_id(user_id)
            if not user:
                return jsonify({'error': '用户不存在'}), 404
            
            # 删除用户
            users_data.remove(user)
            
            return jsonify({
                'message': '用户删除成功'
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': '删除用户失败',
                'message': str(e)
            }), 500

class ProtectedAPI(Resource):
    """受保护的API示例"""
    
    @active_user_required
    def get(self):
        """需要认证的API端点"""
        try:
            current_user_id = get_jwt_identity()
            user = find_user_by_id(current_user_id)
            claims = get_jwt()
            
            return jsonify({
                'message': '这是一个受保护的API端点',
                'user': user_to_dict(user),
                'token_info': {
                    'jti': claims['jti'],
                    'exp': claims['exp'],
                    'iat': claims['iat'],
                    'type': claims['type']
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': '访问受保护资源失败',
                'message': str(e)
            }), 500

# 注册API路由
api.add_resource(RegisterAPI, '/api/auth/register')
api.add_resource(LoginAPI, '/api/auth/login')
api.add_resource(RefreshAPI, '/api/auth/refresh')
api.add_resource(LogoutAPI, '/api/auth/logout')
api.add_resource(ProfileAPI, '/api/auth/profile')
api.add_resource(UsersAPI, '/api/admin/users')
api.add_resource(UserAPI, '/api/admin/users/<int:user_id>')
api.add_resource(ProtectedAPI, '/api/protected')

# 根路径处理
@app.route('/')
def index():
    """API首页"""
    return jsonify({
        'message': 'Session20 JWT认证系统API',
        'version': '1.0.0',
        'endpoints': {
            'auth': {
                'register': 'POST /api/auth/register',
                'login': 'POST /api/auth/login',
                'refresh': 'POST /api/auth/refresh',
                'logout': 'POST /api/auth/logout',
                'profile': 'GET/PUT /api/auth/profile'
            },
            'admin': {
                'users': 'GET /api/admin/users',
                'user': 'GET/PUT/DELETE /api/admin/users/{id}'
            },
            'protected': {
                'demo': 'GET /api/protected'
            }
        },
        'default_users': {
            'admin': {'username': 'admin', 'password': 'admin123'},
            'user': {'username': 'user1', 'password': 'user123'}
        }
    })

# 错误处理
@app.errorhandler(401)
def unauthorized(error):
    """401错误处理"""
    return jsonify({
        'error': '未授权访问',
        'message': '请提供有效的认证信息'
    }), 401

@app.errorhandler(403)
def forbidden(error):
    """403错误处理"""
    return jsonify({
        'error': '权限不足',
        'message': '您没有访问此资源的权限'
    }), 403

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({
        'error': '资源不存在',
        'message': '请求的资源未找到'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return jsonify({
        'error': '服务器内部错误',
        'message': '请稍后重试'
    }), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🔐 Session20 练习2参考答案: JWT认证系统")
    print("="*60)
    print("\n✅ 已实现功能:")
    print("  ✓ 用户注册和登录")
    print("  ✓ JWT Token管理")
    print("  ✓ Token刷新和登出")
    print("  ✓ 权限控制装饰器")
    print("  ✓ 用户资料管理")
    print("  ✓ 管理员功能")
    print("  ✓ Token黑名单")
    print("  ✓ 错误处理")
    print("\n🔑 认证端点:")
    print("  POST   /api/auth/register    - 用户注册")
    print("  POST   /api/auth/login       - 用户登录")
    print("  POST   /api/auth/refresh     - 刷新Token")
    print("  POST   /api/auth/logout      - 用户登出")
    print("  GET    /api/auth/profile     - 获取用户资料")
    print("  PUT    /api/auth/profile     - 更新用户资料")
    print("\n👥 管理端点:")
    print("  GET    /api/admin/users      - 获取用户列表")
    print("  GET    /api/admin/users/{id} - 获取用户信息")
    print("  PUT    /api/admin/users/{id} - 更新用户信息")
    print("  DELETE /api/admin/users/{id} - 删除用户")
    print("\n🔒 受保护端点:")
    print("  GET    /api/protected         - 受保护的API")
    print("\n👤 默认用户:")
    print("  管理员: admin / admin123")
    print("  普通用户: user1 / user123")
    print("\n🚀 服务器启动在: http://localhost:5003")
    print("="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5003)