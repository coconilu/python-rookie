#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session19 练习3：Flask模板引擎和前端集成综合练习

练习目标：
1. 掌握Jinja2模板引擎高级功能
2. 实现模板继承和组件化
3. 创建自定义过滤器和函数
4. 构建完整的前后端交互系统
5. 实现用户认证和权限管理

作者: Python教程团队
创建日期: 2024-12-24
"""

from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json
import random
import string
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'exercise3-secret-key-for-sessions'

# 模拟数据库
users_db = {
    'admin': {
        'id': 1,
        'username': 'admin',
        'email': 'admin@example.com',
        'password_hash': generate_password_hash('admin123'),
        'role': 'admin',
        'avatar': 'https://ui-avatars.com/api/?name=Admin&background=3b82f6&color=fff',
        'created_at': datetime.now() - timedelta(days=30),
        'last_login': datetime.now() - timedelta(hours=1)
    },
    'user1': {
        'id': 2,
        'username': 'user1',
        'email': 'user1@example.com',
        'password_hash': generate_password_hash('user123'),
        'role': 'user',
        'avatar': 'https://ui-avatars.com/api/?name=User1&background=10b981&color=fff',
        'created_at': datetime.now() - timedelta(days=15),
        'last_login': datetime.now() - timedelta(minutes=30)
    }
}

projects_db = [
    {
        'id': 1,
        'name': '电商网站开发',
        'description': '使用Flask和Vue.js开发现代化电商平台',
        'status': 'active',
        'priority': 'high',
        'owner_id': 1,
        'team_members': [1, 2],
        'progress': 75,
        'budget': 50000,
        'start_date': datetime.now() - timedelta(days=20),
        'end_date': datetime.now() + timedelta(days=10),
        'tags': ['Flask', 'Vue.js', '电商', '全栈开发'],
        'created_at': datetime.now() - timedelta(days=25)
    },
    {
        'id': 2,
        'name': '移动应用后端API',
        'description': '为移动应用提供RESTful API服务',
        'status': 'planning',
        'priority': 'medium',
        'owner_id': 2,
        'team_members': [2],
        'progress': 25,
        'budget': 30000,
        'start_date': datetime.now() + timedelta(days=5),
        'end_date': datetime.now() + timedelta(days=35),
        'tags': ['API', 'RESTful', '移动开发', '后端'],
        'created_at': datetime.now() - timedelta(days=10)
    },
    {
        'id': 3,
        'name': '数据分析平台',
        'description': '构建企业级数据分析和可视化平台',
        'status': 'completed',
        'priority': 'high',
        'owner_id': 1,
        'team_members': [1, 2],
        'progress': 100,
        'budget': 80000,
        'start_date': datetime.now() - timedelta(days=60),
        'end_date': datetime.now() - timedelta(days=5),
        'tags': ['数据分析', '可视化', 'Python', 'D3.js'],
        'created_at': datetime.now() - timedelta(days=70)
    }
]

tasks_db = [
    {
        'id': 1,
        'title': '设计用户界面',
        'description': '创建现代化的用户界面设计',
        'project_id': 1,
        'assignee_id': 2,
        'status': 'completed',
        'priority': 'high',
        'estimated_hours': 20,
        'actual_hours': 18,
        'due_date': datetime.now() - timedelta(days=5),
        'created_at': datetime.now() - timedelta(days=15)
    },
    {
        'id': 2,
        'title': '实现用户认证',
        'description': '开发安全的用户登录和注册功能',
        'project_id': 1,
        'assignee_id': 1,
        'status': 'in_progress',
        'priority': 'high',
        'estimated_hours': 15,
        'actual_hours': 10,
        'due_date': datetime.now() + timedelta(days=3),
        'created_at': datetime.now() - timedelta(days=10)
    },
    {
        'id': 3,
        'title': '数据库设计',
        'description': '设计高效的数据库结构',
        'project_id': 2,
        'assignee_id': 2,
        'status': 'pending',
        'priority': 'medium',
        'estimated_hours': 12,
        'actual_hours': 0,
        'due_date': datetime.now() + timedelta(days=7),
        'created_at': datetime.now() - timedelta(days=5)
    }
]

# 自定义Jinja2过滤器
@app.template_filter('datetime_format')
def datetime_format(value, format='%Y-%m-%d %H:%M'):
    """格式化日期时间"""
    if isinstance(value, str):
        value = datetime.fromisoformat(value)
    return value.strftime(format)

@app.template_filter('time_ago')
def time_ago(value):
    """显示相对时间"""
    if isinstance(value, str):
        value = datetime.fromisoformat(value)
    
    now = datetime.now()
    diff = now - value
    
    if diff.days > 0:
        return f"{diff.days}天前"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours}小时前"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes}分钟前"
    else:
        return "刚刚"

@app.template_filter('currency')
def currency_format(value):
    """格式化货币"""
    return f"¥{value:,.2f}"

@app.template_filter('percentage')
def percentage_format(value):
    """格式化百分比"""
    return f"{value}%"

@app.template_filter('status_badge')
def status_badge(status):
    """生成状态徽章"""
    status_map = {
        'active': {'class': 'success', 'text': '进行中'},
        'planning': {'class': 'warning', 'text': '计划中'},
        'completed': {'class': 'primary', 'text': '已完成'},
        'cancelled': {'class': 'danger', 'text': '已取消'},
        'pending': {'class': 'secondary', 'text': '待处理'},
        'in_progress': {'class': 'info', 'text': '进行中'}
    }
    
    config = status_map.get(status, {'class': 'secondary', 'text': status})
    return f'<span class="badge badge-{config["class"]}">{config["text"]}</span>'

@app.template_filter('priority_icon')
def priority_icon(priority):
    """生成优先级图标"""
    icons = {
        'high': '🔴',
        'medium': '🟡',
        'low': '🟢'
    }
    return icons.get(priority, '⚪')

@app.template_filter('truncate_words')
def truncate_words(text, length=20):
    """截断文本"""
    if len(text) <= length:
        return text
    return text[:length] + '...'

@app.template_filter('highlight')
def highlight_text(text, keyword):
    """高亮关键词"""
    if not keyword:
        return text
    
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    return pattern.sub(f'<mark>{keyword}</mark>', text)

# 自定义全局函数
@app.template_global()
def get_user_by_id(user_id):
    """根据ID获取用户信息"""
    for user in users_db.values():
        if user['id'] == user_id:
            return user
    return None

@app.template_global()
def get_project_stats():
    """获取项目统计信息"""
    total = len(projects_db)
    active = len([p for p in projects_db if p['status'] == 'active'])
    completed = len([p for p in projects_db if p['status'] == 'completed'])
    
    return {
        'total': total,
        'active': active,
        'completed': completed,
        'completion_rate': (completed / total * 100) if total > 0 else 0
    }

@app.template_global()
def get_user_projects(user_id):
    """获取用户的项目"""
    return [p for p in projects_db if user_id in p['team_members']]

@app.template_global()
def generate_avatar_url(name, bg_color='3b82f6'):
    """生成头像URL"""
    return f"https://ui-avatars.com/api/?name={name}&background={bg_color}&color=fff"

@app.template_global()
def url_for_with_params(endpoint, **params):
    """生成带参数的URL"""
    return url_for(endpoint, **params)

# 上下文处理器
@app.context_processor
def inject_globals():
    """注入全局变量"""
    return {
        'current_user': get_current_user(),
        'app_name': 'ProjectHub',
        'app_version': '1.0.0',
        'current_year': datetime.now().year
    }

# 基础模板
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ app_name }}{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    
    <style>
        :root {
            --primary-color: #3b82f6;
            --secondary-color: #10b981;
            --success-color: #059669;
            --warning-color: #f59e0b;
            --danger-color: #ef4444;
            --info-color: #06b6d4;
            --dark-color: #1f2937;
            --light-color: #f8fafc;
        }
        
        body {
            background-color: var(--light-color);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .navbar-brand {
            font-weight: bold;
            font-size: 1.5rem;
        }
        
        .sidebar {
            min-height: calc(100vh - 56px);
            background: white;
            box-shadow: 2px 0 4px rgba(0,0,0,0.1);
        }
        
        .main-content {
            padding: 2rem;
        }
        
        .card {
            border: none;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        
        .card:hover {
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        
        .badge {
            font-size: 0.75rem;
        }
        
        .progress {
            height: 8px;
        }
        
        .avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
        }
        
        .avatar-sm {
            width: 24px;
            height: 24px;
        }
        
        .avatar-lg {
            width: 60px;
            height: 60px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            border-radius: 10px;
        }
        
        .project-card {
            border-left: 4px solid var(--primary-color);
        }
        
        .task-item {
            border-left: 3px solid transparent;
            transition: all 0.3s ease;
        }
        
        .task-item:hover {
            border-left-color: var(--primary-color);
            background-color: rgba(59, 130, 246, 0.05);
        }
        
        .nav-link {
            color: var(--dark-color);
            transition: all 0.3s ease;
        }
        
        .nav-link:hover {
            color: var(--primary-color);
            background-color: rgba(59, 130, 246, 0.1);
        }
        
        .nav-link.active {
            color: var(--primary-color);
            background-color: rgba(59, 130, 246, 0.1);
            border-radius: 5px;
        }
        
        .btn-primary {
            background-color: var(--primary-color);
            border-color: var(--primary-color);
        }
        
        .btn-success {
            background-color: var(--success-color);
            border-color: var(--success-color);
        }
        
        .text-primary {
            color: var(--primary-color) !important;
        }
        
        .bg-primary {
            background-color: var(--primary-color) !important;
        }
        
        mark {
            background-color: #fef08a;
            padding: 0.1em 0.2em;
            border-radius: 3px;
        }
        
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid rgba(59, 130, 246, 0.3);
            border-radius: 50%;
            border-top-color: var(--primary-color);
            animation: spin 1s ease-in-out infinite;
        }
        
        @keyframes spin {
            to {
                transform: rotate(360deg);
            }
        }
        
        .fade-in {
            animation: fadeIn 0.5s ease-in;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        {% block extra_css %}{% endblock %}
    </style>
</head>
<body>
    <!-- 导航栏 -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container-fluid">
            <a class="navbar-brand" href="{{ url_for('dashboard') }}">
                <i class="fas fa-project-diagram me-2"></i>{{ app_name }}
            </a>
            
            <div class="navbar-nav ms-auto">
                {% if current_user %}
                    <div class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle d-flex align-items-center" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown">
                            <img src="{{ current_user.avatar }}" alt="{{ current_user.username }}" class="avatar avatar-sm me-2">
                            {{ current_user.username }}
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="{{ url_for('profile') }}"><i class="fas fa-user me-2"></i>个人资料</a></li>
                            <li><a class="dropdown-item" href="{{ url_for('settings') }}"><i class="fas fa-cog me-2"></i>设置</a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="{{ url_for('logout') }}"><i class="fas fa-sign-out-alt me-2"></i>退出登录</a></li>
                        </ul>
                    </div>
                {% else %}
                    <a class="nav-link" href="{{ url_for('login') }}">登录</a>
                {% endif %}
            </div>
        </div>
    </nav>
    
    <div class="container-fluid">
        <div class="row">
            {% if current_user %}
            <!-- 侧边栏 -->
            <div class="col-md-2 p-0">
                <div class="sidebar p-3">
                    <ul class="nav nav-pills flex-column">
                        <li class="nav-item">
                            <a class="nav-link {{ 'active' if request.endpoint == 'dashboard' }}" href="{{ url_for('dashboard') }}">
                                <i class="fas fa-tachometer-alt me-2"></i>仪表板
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link {{ 'active' if request.endpoint == 'projects' }}" href="{{ url_for('projects') }}">
                                <i class="fas fa-folder me-2"></i>项目管理
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link {{ 'active' if request.endpoint == 'tasks' }}" href="{{ url_for('tasks') }}">
                                <i class="fas fa-tasks me-2"></i>任务管理
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link {{ 'active' if request.endpoint == 'team' }}" href="{{ url_for('team') }}">
                                <i class="fas fa-users me-2"></i>团队管理
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link {{ 'active' if request.endpoint == 'reports' }}" href="{{ url_for('reports') }}">
                                <i class="fas fa-chart-bar me-2"></i>报表分析
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
            
            <!-- 主内容区 -->
            <div class="col-md-10">
            {% else %}
            <div class="col-12">
            {% endif %}
                <div class="main-content">
                    <!-- Flash消息 -->
                    {% with messages = get_flashed_messages(with_categories=true) %}
                        {% if messages %}
                            {% for category, message in messages %}
                                <div class="alert alert-{{ 'danger' if category == 'error' else category }} alert-dismissible fade show" role="alert">
                                    {{ message }}
                                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                                </div>
                            {% endfor %}
                        {% endif %}
                    {% endwith %}
                    
                    {% block content %}{% endblock %}
                </div>
            </div>
        </div>
    </div>
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    {% block extra_js %}{% endblock %}
    
    <script>
        // 全局JavaScript功能
        document.addEventListener('DOMContentLoaded', function() {
            // 自动隐藏alert
            setTimeout(function() {
                const alerts = document.querySelectorAll('.alert');
                alerts.forEach(alert => {
                    if (alert.classList.contains('show')) {
                        alert.classList.remove('show');
                        setTimeout(() => alert.remove(), 150);
                    }
                });
            }, 5000);
            
            // 添加淡入动画
            const cards = document.querySelectorAll('.card');
            cards.forEach((card, index) => {
                setTimeout(() => {
                    card.classList.add('fade-in');
                }, index * 100);
            });
        });
        
        // AJAX工具函数
        async function apiRequest(url, options = {}) {
            try {
                const response = await fetch(url, {
                    headers: {
                        'Content-Type': 'application/json',
                        ...options.headers
                    },
                    ...options
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                return await response.json();
            } catch (error) {
                console.error('API请求失败:', error);
                throw error;
            }
        }
        
        // 显示加载状态
        function showLoading(element) {
            const originalContent = element.innerHTML;
            element.innerHTML = '<span class="loading"></span> 加载中...';
            element.disabled = true;
            
            return function hideLoading() {
                element.innerHTML = originalContent;
                element.disabled = false;
            };
        }
        
        // 显示通知
        function showNotification(message, type = 'success') {
            const alertDiv = document.createElement('div');
            alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
            alertDiv.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            const container = document.querySelector('.main-content');
            container.insertBefore(alertDiv, container.firstChild);
            
            setTimeout(() => {
                alertDiv.classList.remove('show');
                setTimeout(() => alertDiv.remove(), 150);
            }, 3000);
        }
    </script>
</body>
</html>
"""

# 登录页面模板
LOGIN_TEMPLATE = """
{% extends "base.html" %}

{% block title %}登录 - {{ super() }}{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6 col-lg-4">
        <div class="card shadow">
            <div class="card-body p-5">
                <div class="text-center mb-4">
                    <i class="fas fa-project-diagram fa-3x text-primary mb-3"></i>
                    <h2 class="card-title">欢迎回来</h2>
                    <p class="text-muted">请登录您的账户</p>
                </div>
                
                <form method="POST" id="loginForm">
                    <div class="mb-3">
                        <label for="username" class="form-label">用户名</label>
                        <input type="text" class="form-control" id="username" name="username" required>
                    </div>
                    
                    <div class="mb-3">
                        <label for="password" class="form-label">密码</label>
                        <input type="password" class="form-control" id="password" name="password" required>
                    </div>
                    
                    <div class="mb-3 form-check">
                        <input type="checkbox" class="form-check-input" id="remember" name="remember">
                        <label class="form-check-label" for="remember">记住我</label>
                    </div>
                    
                    <button type="submit" class="btn btn-primary w-100 mb-3">
                        <i class="fas fa-sign-in-alt me-2"></i>登录
                    </button>
                </form>
                
                <div class="text-center">
                    <small class="text-muted">
                        演示账户：admin/admin123 或 user1/user123
                    </small>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.getElementById('loginForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const submitBtn = this.querySelector('button[type="submit"]');
        const hideLoading = showLoading(submitBtn);
        
        try {
            const formData = new FormData(this);
            const response = await fetch('/login', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                window.location.href = '/dashboard';
            } else {
                const data = await response.json();
                showNotification(data.message || '登录失败', 'danger');
            }
        } catch (error) {
            showNotification('网络错误，请稍后重试', 'danger');
        } finally {
            hideLoading();
        }
    });
</script>
{% endblock %}
"""

# 仪表板模板
DASHBOARD_TEMPLATE = """
{% extends "base.html" %}

{% block title %}仪表板 - {{ super() }}{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <div>
        <h1 class="h3 mb-0">仪表板</h1>
        <p class="text-muted">欢迎回来，{{ current_user.username }}！</p>
    </div>
    <div>
        <span class="text-muted">最后登录：{{ current_user.last_login | time_ago }}</span>
    </div>
</div>

<!-- 统计卡片 -->
<div class="row mb-4">
    {% set stats = get_project_stats() %}
    <div class="col-md-3 mb-3">
        <div class="card stat-card">
            <div class="card-body text-center">
                <i class="fas fa-folder fa-2x mb-2"></i>
                <h3 class="mb-0">{{ stats.total }}</h3>
                <small>总项目数</small>
            </div>
        </div>
    </div>
    <div class="col-md-3 mb-3">
        <div class="card stat-card">
            <div class="card-body text-center">
                <i class="fas fa-play fa-2x mb-2"></i>
                <h3 class="mb-0">{{ stats.active }}</h3>
                <small>进行中</small>
            </div>
        </div>
    </div>
    <div class="col-md-3 mb-3">
        <div class="card stat-card">
            <div class="card-body text-center">
                <i class="fas fa-check fa-2x mb-2"></i>
                <h3 class="mb-0">{{ stats.completed }}</h3>
                <small>已完成</small>
            </div>
        </div>
    </div>
    <div class="col-md-3 mb-3">
        <div class="card stat-card">
            <div class="card-body text-center">
                <i class="fas fa-percentage fa-2x mb-2"></i>
                <h3 class="mb-0">{{ "%.1f" | format(stats.completion_rate) }}%</h3>
                <small>完成率</small>
            </div>
        </div>
    </div>
</div>

<div class="row">
    <!-- 我的项目 -->
    <div class="col-md-8 mb-4">
        <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0"><i class="fas fa-folder me-2"></i>我的项目</h5>
                <a href="{{ url_for('projects') }}" class="btn btn-sm btn-outline-primary">查看全部</a>
            </div>
            <div class="card-body">
                {% set user_projects = get_user_projects(current_user.id) %}
                {% if user_projects %}
                    {% for project in user_projects[:3] %}
                    <div class="project-card card mb-3">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <div>
                                    <h6 class="card-title mb-1">{{ project.name }}</h6>
                                    <p class="card-text text-muted small mb-2">{{ project.description | truncate_words(30) }}</p>
                                </div>
                                <div class="text-end">
                                    {{ project.status | status_badge | safe }}
                                    <div class="mt-1">
                                        {{ project.priority | priority_icon }} {{ project.priority | title }}
                                    </div>
                                </div>
                            </div>
                            
                            <div class="row align-items-center">
                                <div class="col-md-6">
                                    <div class="progress mb-2">
                                        <div class="progress-bar" role="progressbar" style="width: {{ project.progress }}%" aria-valuenow="{{ project.progress }}" aria-valuemin="0" aria-valuemax="100"></div>
                                    </div>
                                    <small class="text-muted">进度：{{ project.progress | percentage }}</small>
                                </div>
                                <div class="col-md-6 text-end">
                                    <small class="text-muted">预算：{{ project.budget | currency }}</small><br>
                                    <small class="text-muted">截止：{{ project.end_date | datetime_format('%m-%d') }}</small>
                                </div>
                            </div>
                            
                            <div class="mt-2">
                                {% for tag in project.tags[:3] %}
                                    <span class="badge bg-light text-dark me-1">{{ tag }}</span>
                                {% endfor %}
                                {% if project.tags | length > 3 %}
                                    <span class="badge bg-light text-dark">+{{ project.tags | length - 3 }}</span>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                {% else %}
                    <div class="text-center py-4">
                        <i class="fas fa-folder-open fa-3x text-muted mb-3"></i>
                        <p class="text-muted">暂无项目</p>
                        <a href="{{ url_for('projects') }}" class="btn btn-primary">创建项目</a>
                    </div>
                {% endif %}
            </div>
        </div>
    </div>
    
    <!-- 最近任务 -->
    <div class="col-md-4 mb-4">
        <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0"><i class="fas fa-tasks me-2"></i>最近任务</h5>
                <a href="{{ url_for('tasks') }}" class="btn btn-sm btn-outline-primary">查看全部</a>
            </div>
            <div class="card-body">
                {% for task in tasks_db[:5] %}
                <div class="task-item p-2 mb-2 rounded">
                    <div class="d-flex justify-content-between align-items-start">
                        <div class="flex-grow-1">
                            <h6 class="mb-1">{{ task.title }}</h6>
                            <small class="text-muted">{{ task.description | truncate_words(20) }}</small>
                        </div>
                        <div class="ms-2">
                            {{ task.status | status_badge | safe }}
                        </div>
                    </div>
                    <div class="mt-2 d-flex justify-content-between align-items-center">
                        <div>
                            {% set assignee = get_user_by_id(task.assignee_id) %}
                            {% if assignee %}
                                <img src="{{ assignee.avatar }}" alt="{{ assignee.username }}" class="avatar avatar-sm me-1">
                                <small class="text-muted">{{ assignee.username }}</small>
                            {% endif %}
                        </div>
                        <small class="text-muted">{{ task.due_date | time_ago }}</small>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
</div>

<!-- 图表区域 -->
<div class="row">
    <div class="col-md-6 mb-4">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0"><i class="fas fa-chart-pie me-2"></i>项目状态分布</h5>
            </div>
            <div class="card-body">
                <canvas id="projectStatusChart" width="400" height="200"></canvas>
            </div>
        </div>
    </div>
    
    <div class="col-md-6 mb-4">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0"><i class="fas fa-chart-line me-2"></i>项目进度趋势</h5>
            </div>
            <div class="card-body">
                <canvas id="progressTrendChart" width="400" height="200"></canvas>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    // 项目状态分布图
    const statusCtx = document.getElementById('projectStatusChart').getContext('2d');
    new Chart(statusCtx, {
        type: 'doughnut',
        data: {
            labels: ['进行中', '计划中', '已完成'],
            datasets: [{
                data: [
                    {{ projects_db | selectattr('status', 'equalto', 'active') | list | length }},
                    {{ projects_db | selectattr('status', 'equalto', 'planning') | list | length }},
                    {{ projects_db | selectattr('status', 'equalto', 'completed') | list | length }}
                ],
                backgroundColor: [
                    'rgba(59, 130, 246, 0.8)',
                    'rgba(245, 158, 11, 0.8)',
                    'rgba(16, 185, 129, 0.8)'
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
    
    // 项目进度趋势图
    const progressCtx = document.getElementById('progressTrendChart').getContext('2d');
    new Chart(progressCtx, {
        type: 'line',
        data: {
            labels: {{ projects_db | map(attribute='name') | list | tojson }},
            datasets: [{
                label: '完成进度',
                data: {{ projects_db | map(attribute='progress') | list | tojson }},
                borderColor: 'rgba(59, 130, 246, 1)',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
</script>
{% endblock %}
"""

# 工具函数
def get_current_user():
    """获取当前登录用户"""
    if 'user_id' in session:
        for user in users_db.values():
            if user['id'] == session['user_id']:
                return user
    return None

def login_required(f):
    """登录装饰器"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not get_current_user():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# 路由定义
@app.route('/')
def index():
    """首页"""
    if get_current_user():
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """登录页面"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = users_db.get(username)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            user['last_login'] = datetime.now()
            flash('登录成功！', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('用户名或密码错误', 'error')
    
    return render_template_string(BASE_TEMPLATE + LOGIN_TEMPLATE)

@app.route('/logout')
def logout():
    """退出登录"""
    session.pop('user_id', None)
    flash('已退出登录', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """仪表板"""
    return render_template_string(BASE_TEMPLATE + DASHBOARD_TEMPLATE, 
                                projects_db=projects_db, 
                                tasks_db=tasks_db)

@app.route('/projects')
@login_required
def projects():
    """项目管理页面"""
    # TODO: 实现项目管理页面
    return "<h1>项目管理页面</h1><p>TODO: 实现项目列表、创建、编辑功能</p>"

@app.route('/tasks')
@login_required
def tasks():
    """任务管理页面"""
    # TODO: 实现任务管理页面
    return "<h1>任务管理页面</h1><p>TODO: 实现任务列表、创建、编辑功能</p>"

@app.route('/team')
@login_required
def team():
    """团队管理页面"""
    # TODO: 实现团队管理页面
    return "<h1>团队管理页面</h1><p>TODO: 实现团队成员管理功能</p>"

@app.route('/reports')
@login_required
def reports():
    """报表分析页面"""
    # TODO: 实现报表分析页面
    return "<h1>报表分析页面</h1><p>TODO: 实现数据分析和可视化功能</p>"

@app.route('/profile')
@login_required
def profile():
    """个人资料页面"""
    # TODO: 实现个人资料页面
    return "<h1>个人资料页面</h1><p>TODO: 实现个人信息编辑功能</p>"

@app.route('/settings')
@login_required
def settings():
    """设置页面"""
    # TODO: 实现设置页面
    return "<h1>设置页面</h1><p>TODO: 实现系统设置功能</p>"

# API路由
@app.route('/api/projects', methods=['GET'])
@login_required
def api_get_projects():
    """获取项目列表API"""
    # TODO: 实现项目API
    return jsonify({
        'success': True,
        'projects': projects_db
    })

@app.route('/api/search', methods=['GET'])
@login_required
def api_search():
    """搜索API"""
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify({'success': False, 'message': '搜索关键词不能为空'})
    
    # 搜索项目
    project_results = []
    for project in projects_db:
        if (query in project['name'].lower() or 
            query in project['description'].lower() or 
            any(query in tag.lower() for tag in project['tags'])):
            project_results.append({
                'type': 'project',
                'id': project['id'],
                'title': project['name'],
                'description': project['description'],
                'url': url_for('projects') + f'#{project["id"]}'
            })
    
    # 搜索任务
    task_results = []
    for task in tasks_db:
        if (query in task['title'].lower() or 
            query in task['description'].lower()):
            task_results.append({
                'type': 'task',
                'id': task['id'],
                'title': task['title'],
                'description': task['description'],
                'url': url_for('tasks') + f'#{task["id"]}'
            })
    
    return jsonify({
        'success': True,
        'results': project_results + task_results,
        'total': len(project_results) + len(task_results)
    })

if __name__ == '__main__':
    print("Session19 练习3：Flask模板引擎和前端集成综合练习")
    print("=" * 60)
    print("练习内容：")
    print("1. Jinja2模板引擎高级功能")
    print("   - 自定义过滤器和全局函数")
    print("   - 模板继承和组件化")
    print("   - 上下文处理器")
    print("2. 前后端交互系统")
    print("   - 用户认证和会话管理")
    print("   - AJAX API接口")
    print("   - 实时数据更新")
    print("3. 现代化UI设计")
    print("   - Bootstrap响应式布局")
    print("   - Chart.js数据可视化")
    print("   - 动画和交互效果")
    print("\n练习要求：")
    print("- 完成所有TODO标记的功能")
    print("- 实现完整的项目管理系统")
    print("- 添加搜索和过滤功能")
    print("- 优化用户体验和界面设计")
    print("- 使用Flask和Jinja2最佳实践")
    print("\n登录信息：")
    print("- 管理员：admin / admin123")
    print("- 普通用户：user1 / user123")
    print("\n访问 http://localhost:5000 开始练习")
    
    app.run(debug=True, host='0.0.0.0', port=5000)