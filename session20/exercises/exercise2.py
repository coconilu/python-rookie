#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session20 API开发练习2 - JWT认证练习
用户管理和认证系统

练习目标:
1. 实现用户注册和登录
2. 使用JWT进行身份认证
3. 实现权限控制
4. 处理Token刷新和登出

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

# TODO: 创建Flask应用和配置
# 提示: 需要配置SECRET_KEY, JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES
app = None  # 请替换为正确的Flask应用实例

# TODO: 初始化扩展
api = None  # 请替换为正确的Api实例
jwt = None  # 请替换为正确的JWTManager实例

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

# TODO: 实现JWT回调函数
# 提示: 需要实现token_in_blocklist_loader, expired_token_loader等

# TODO: 实现权限装饰器
def admin_required(f):
    """需要管理员权限的装饰器
    
    TODO: 实现管理员权限检查
    1. 使用@jwt_required()装饰器
    2. 获取当前用户身份
    3. 检查用户是否为管理员
    4. 返回403错误如果权限不足
    """
    # TODO: 实现管理员权限检查逻辑
    pass

def active_user_required(f):
    """需要活跃用户的装饰器
    
    TODO: 实现活跃用户检查
    1. 使用@jwt_required()装饰器
    2. 获取当前用户身份
    3. 检查用户是否处于活跃状态
    4. 返回403错误如果用户被禁用
    """
    # TODO: 实现活跃用户检查逻辑
    pass

# 辅助函数
def find_user_by_username(username):
    """根据用户名查找用户
    
    TODO: 实现用户查找逻辑
    """
    # TODO: 实现查找逻辑
    pass

def find_user_by_id(user_id):
    """根据ID查找用户
    
    TODO: 实现用户查找逻辑
    """
    # TODO: 实现查找逻辑
    pass

def find_user_by_email(email):
    """根据邮箱查找用户
    
    TODO: 实现用户查找逻辑
    """
    # TODO: 实现查找逻辑
    pass

def validate_email(email):
    """验证邮箱格式
    
    TODO: 实现邮箱格式验证
    使用正则表达式验证邮箱格式
    
    Returns:
        bool: 邮箱格式是否有效
    """
    # TODO: 实现邮箱验证逻辑
    pass

def validate_password(password):
    """验证密码强度
    
    TODO: 实现密码强度验证
    要求:
    1. 长度至少8个字符
    2. 包含至少一个数字
    3. 包含至少一个字母
    
    Returns:
        tuple: (is_valid, error_message)
    """
    # TODO: 实现密码验证逻辑
    pass

def user_to_dict(user, include_sensitive=False):
    """将用户对象转换为字典
    
    TODO: 实现用户对象序列化
    注意: 不要包含敏感信息如密码哈希
    """
    # TODO: 实现序列化逻辑
    pass

class RegisterAPI(Resource):
    """用户注册API"""
    
    def post(self):
        """用户注册
        
        TODO: 实现用户注册功能
        1. 验证请求数据
        2. 检查用户名和邮箱是否已存在
        3. 验证密码强度
        4. 创建新用户
        5. 返回用户信息（不包含密码）
        
        请求体:
        {
            "username": "用户名",
            "email": "邮箱",
            "password": "密码"
        }
        """
        # TODO: 实现注册逻辑
        pass

class LoginAPI(Resource):
    """用户登录API"""
    
    def post(self):
        """用户登录
        
        TODO: 实现用户登录功能
        1. 验证用户名和密码
        2. 检查用户是否处于活跃状态
        3. 生成访问令牌和刷新令牌
        4. 返回用户信息和令牌
        
        请求体:
        {
            "username": "用户名",
            "password": "密码"
        }
        """
        # TODO: 实现登录逻辑
        pass

class RefreshAPI(Resource):
    """刷新Token API"""
    
    # TODO: 添加@jwt_required(refresh=True)装饰器
    def post(self):
        """刷新访问令牌
        
        TODO: 实现Token刷新功能
        1. 获取当前用户身份
        2. 检查用户是否存在且活跃
        3. 生成新的访问令牌
        4. 返回新令牌
        """
        # TODO: 实现Token刷新逻辑
        pass

class LogoutAPI(Resource):
    """用户登出API"""
    
    # TODO: 添加@jwt_required()装饰器
    def post(self):
        """用户登出
        
        TODO: 实现用户登出功能
        1. 获取当前Token的JTI
        2. 将Token加入黑名单
        3. 返回登出成功信息
        """
        # TODO: 实现登出逻辑
        pass

class ProfileAPI(Resource):
    """用户资料API"""
    
    # TODO: 添加@active_user_required装饰器
    def get(self):
        """获取当前用户资料
        
        TODO: 实现获取用户资料功能
        1. 获取当前用户身份
        2. 查找用户信息
        3. 返回用户资料（不包含敏感信息）
        """
        # TODO: 实现获取资料逻辑
        pass
    
    # TODO: 添加@active_user_required装饰器
    def put(self):
        """更新当前用户资料
        
        TODO: 实现更新用户资料功能
        1. 获取当前用户身份
        2. 验证更新数据
        3. 检查邮箱是否被其他用户使用
        4. 更新用户信息
        5. 返回更新后的用户资料
        
        请求体:
        {
            "email": "新邮箱",
            "password": "新密码"
        }
        """
        # TODO: 实现更新资料逻辑
        pass

class UsersAPI(Resource):
    """用户管理API（仅管理员）"""
    
    # TODO: 添加@admin_required装饰器
    def get(self):
        """获取所有用户列表（仅管理员）
        
        TODO: 实现获取用户列表功能
        1. 检查管理员权限
        2. 支持分页查询
        3. 支持按角色筛选
        4. 返回用户列表
        
        查询参数:
        - page: 页码
        - per_page: 每页数量
        - role: 角色筛选
        - is_active: 活跃状态筛选
        """
        # TODO: 实现获取用户列表逻辑
        pass

class UserAPI(Resource):
    """单个用户管理API（仅管理员）"""
    
    # TODO: 添加@admin_required装饰器
    def get(self, user_id):
        """获取指定用户信息（仅管理员）
        
        TODO: 实现获取用户信息功能
        """
        # TODO: 实现获取用户信息逻辑
        pass
    
    # TODO: 添加@admin_required装饰器
    def put(self, user_id):
        """更新指定用户信息（仅管理员）
        
        TODO: 实现更新用户信息功能
        1. 检查用户是否存在
        2. 验证更新数据
        3. 更新用户信息
        4. 返回更新后的用户信息
        
        请求体:
        {
            "role": "新角色",
            "is_active": true/false
        }
        """
        # TODO: 实现更新用户信息逻辑
        pass
    
    # TODO: 添加@admin_required装饰器
    def delete(self, user_id):
        """删除指定用户（仅管理员）
        
        TODO: 实现删除用户功能
        注意: 不能删除自己
        """
        # TODO: 实现删除用户逻辑
        pass

class ProtectedAPI(Resource):
    """受保护的API示例"""
    
    # TODO: 添加@active_user_required装饰器
    def get(self):
        """需要认证的API端点
        
        TODO: 实现受保护的API端点
        返回当前用户信息和Token信息
        """
        # TODO: 实现受保护API逻辑
        pass

# TODO: 注册API路由
# 提示: 使用api.add_resource()方法注册所有API资源

# TODO: 添加根路径处理
@app.route('/')
def index():
    """API首页
    
    TODO: 返回API信息和可用端点列表
    """
    # TODO: 实现API首页信息
    pass

# TODO: 添加错误处理
@app.errorhandler(401)
def unauthorized(error):
    """401错误处理"""
    # TODO: 实现401错误处理
    pass

@app.errorhandler(403)
def forbidden(error):
    """403错误处理"""
    # TODO: 实现403错误处理
    pass

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🔐 Session20 练习2: JWT认证系统")
    print("="*50)
    print("\n🎯 练习目标:")
    print("  1. 完成Flask应用和JWT配置")
    print("  2. 实现用户注册和登录功能")
    print("  3. 实现JWT Token管理")
    print("  4. 实现权限控制装饰器")
    print("  5. 实现用户资料管理")
    print("  6. 实现管理员功能")
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
    print("\n💡 提示:")
    print("  - 查看注释中的TODO项目")
    print("  - 参考jwt_auth_example.py示例")
    print("  - 测试认证流程是否正常")
    print("  - 确保权限控制有效")
    print("\n🚀 完成后运行: python exercise2.py")
    print("="*50)
    
    # TODO: 取消注释下面的代码来启动应用
    # if app and jwt:
    #     app.run(debug=True, host='0.0.0.0', port=5003)
    # else:
    #     print("❌ 请先完成Flask应用和JWT的配置")