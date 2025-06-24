#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session19 练习3解决方案：Flask模板引擎和前端集成综合练习

本文件提供练习3的完整解决方案，展示如何实现：
1. Jinja2模板引擎高级功能（自定义过滤器、全局函数、模板继承）
2. 前后端交互系统（用户认证、会话管理、AJAX API）
3. 现代化UI设计（Bootstrap、Chart.js、动画交互效果）
4. 实时数据更新和用户体验优化
5. 完整的项目管理系统

作者: Python教程团队
创建日期: 2024-12-24
"""

from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
from datetime import datetime, timedelta
from functools import wraps
import json
import random
import hashlib
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

# 模拟数据库
users_db = {
    'admin': {
        'id': 1,
        'username': 'admin',
        'password': hashlib.sha256('admin123'.encode()).hexdigest(),
        'email': 'admin@example.com',
        'name': '系统管理员',
        'role': 'admin',
        'avatar': '👨‍💼',
        'created_at': (datetime.now() - timedelta(days=30)).isoformat(),
        'last_login': datetime.now().isoformat(),
        'settings': {
            'theme': 'light',
            'language': 'zh-CN',
            'notifications': True,
            'email_alerts': True
        }
    },
    'developer': {
        'id': 2,
        'username': 'developer',
        'password': hashlib.sha256('dev123'.encode()).hexdigest(),
        'email': 'dev@example.com',
        'name': '开发工程师',
        'role': 'developer',
        'avatar': '👨‍💻',
        'created_at': (datetime.now() - timedelta(days=20)).isoformat(),
        'last_login': (datetime.now() - timedelta(hours=2)).isoformat(),
        'settings': {
            'theme': 'dark',
            'language': 'zh-CN',
            'notifications': True,
            'email_alerts': False
        }
    },
    'designer': {
        'id': 3,
        'username': 'designer',
        'password': hashlib.sha256('design123'.encode()).hexdigest(),
        'email': 'designer@example.com',
        'name': 'UI设计师',
        'role': 'designer',
        'avatar': '👩‍🎨',
        'created_at': (datetime.now() - timedelta(days=15)).isoformat(),
        'last_login': (datetime.now() - timedelta(hours=5)).isoformat(),
        'settings': {
            'theme': 'light',
            'language': 'zh-CN',
            'notifications': True,
            'email_alerts': True
        }
    }
}

projects_db = [
    {
        'id': 1,
        'name': '企业管理系统',
        'description': '一个完整的企业资源管理系统，包含人事、财务、项目管理等模块',
        'status': 'active',
        'priority': 'high',
        'progress': 75,
        'start_date': (datetime.now() - timedelta(days=60)).isoformat(),
        'end_date': (datetime.now() + timedelta(days=30)).isoformat(),
        'created_at': (datetime.now() - timedelta(days=60)).isoformat(),
        'updated_at': (datetime.now() - timedelta(hours=3)).isoformat(),
        'owner_id': 1,
        'team_members': [1, 2, 3],
        'budget': 500000,
        'spent': 375000,
        'tags': ['企业级', '管理系统', 'Web应用'],
        'category': 'enterprise'
    },
    {
        'id': 2,
        'name': '移动端电商应用',
        'description': '面向年轻用户的移动端购物应用，支持社交分享和个性化推荐',
        'status': 'planning',
        'priority': 'medium',
        'progress': 25,
        'start_date': (datetime.now() + timedelta(days=7)).isoformat(),
        'end_date': (datetime.now() + timedelta(days=90)).isoformat(),
        'created_at': (datetime.now() - timedelta(days=10)).isoformat(),
        'updated_at': (datetime.now() - timedelta(hours=1)).isoformat(),
        'owner_id': 2,
        'team_members': [2, 3],
        'budget': 300000,
        'spent': 75000,
        'tags': ['移动端', '电商', 'React Native'],
        'category': 'mobile'
    },
    {
        'id': 3,
        'name': '数据分析平台',
        'description': '为企业提供实时数据分析和可视化的BI平台',
        'status': 'completed',
        'priority': 'high',
        'progress': 100,
        'start_date': (datetime.now() - timedelta(days=120)).isoformat(),
        'end_date': (datetime.now() - timedelta(days=10)).isoformat(),
        'created_at': (datetime.now() - timedelta(days=120)).isoformat(),
        'updated_at': (datetime.now() - timedelta(days=10)).isoformat(),
        'owner_id': 1,
        'team_members': [1, 2],
        'budget': 800000,
        'spent': 750000,
        'tags': ['数据分析', 'BI', 'Python'],
        'category': 'analytics'
    },
    {
        'id': 4,
        'name': '在线教育平台',
        'description': '支持直播、录播、互动的在线教育平台',
        'status': 'on_hold',
        'priority': 'low',
        'progress': 40,
        'start_date': (datetime.now() - timedelta(days=45)).isoformat(),
        'end_date': (datetime.now() + timedelta(days=60)).isoformat(),
        'created_at': (datetime.now() - timedelta(days=45)).isoformat(),
        'updated_at': (datetime.now() - timedelta(days=7)).isoformat(),
        'owner_id': 3,
        'team_members': [1, 3],
        'budget': 400000,
        'spent': 160000,
        'tags': ['教育', '直播', 'Vue.js'],
        'category': 'education'
    }
]

tasks_db = [
    {
        'id': 1,
        'title': '用户认证模块开发',
        'description': '实现用户注册、登录、权限管理功能',
        'status': 'completed',
        'priority': 'high',
        'project_id': 1,
        'assignee_id': 2,
        'created_at': (datetime.now() - timedelta(days=50)).isoformat(),
        'updated_at': (datetime.now() - timedelta(days=30)).isoformat(),
        'due_date': (datetime.now() - timedelta(days=25)).isoformat(),
        'completed_at': (datetime.now() - timedelta(days=30)).isoformat(),
        'estimated_hours': 40,
        'actual_hours': 35,
        'tags': ['后端', '认证', 'Flask']
    },
    {
        'id': 2,
        'title': '数据库设计优化',
        'description': '优化数据库表结构，提升查询性能',
        'status': 'in_progress',
        'priority': 'medium',
        'project_id': 1,
        'assignee_id': 1,
        'created_at': (datetime.now() - timedelta(days=20)).isoformat(),
        'updated_at': (datetime.now() - timedelta(hours=2)).isoformat(),
        'due_date': (datetime.now() + timedelta(days=5)).isoformat(),
        'completed_at': None,
        'estimated_hours': 24,
        'actual_hours': 18,
        'tags': ['数据库', '优化', 'SQL']
    },
    {
        'id': 3,
        'title': 'UI界面设计',
        'description': '设计用户界面原型和视觉规范',
        'status': 'pending',
        'priority': 'high',
        'project_id': 2,
        'assignee_id': 3,
        'created_at': (datetime.now() - timedelta(days=5)).isoformat(),
        'updated_at': (datetime.now() - timedelta(days=5)).isoformat(),
        'due_date': (datetime.now() + timedelta(days=10)).isoformat(),
        'completed_at': None,
        'estimated_hours': 32,
        'actual_hours': 0,
        'tags': ['设计', 'UI', 'Figma']
    },
    {
        'id': 4,
        'title': '数据可视化组件',
        'description': '开发图表和数据展示组件',
        'status': 'completed',
        'priority': 'medium',
        'project_id': 3,
        'assignee_id': 2,
        'created_at': (datetime.now() - timedelta(days=80)).isoformat(),
        'updated_at': (datetime.now() - timedelta(days=15)).isoformat(),
        'due_date': (datetime.now() - timedelta(days=20)).isoformat(),
        'completed_at': (datetime.now() - timedelta(days=15)).isoformat(),
        'estimated_hours': 48,
        'actual_hours': 52,
        'tags': ['前端', '可视化', 'Chart.js']
    },
    {
        'id': 5,
        'title': '性能测试',
        'description': '进行系统性能测试和优化',
        'status': 'in_progress',
        'priority': 'low',
        'project_id': 1,
        'assignee_id': 1,
        'created_at': (datetime.now() - timedelta(days=10)).isoformat(),
        'updated_at': (datetime.now() - timedelta(hours=6)).isoformat(),
        'due_date': (datetime.now() + timedelta(days=15)).isoformat(),
        'completed_at': None,
        'estimated_hours': 16,
        'actual_hours': 8,
        'tags': ['测试', '性能', '优化']
    }
]

# 自定义Jinja2过滤器
@app.template_filter('datetime_format')
def datetime_format(value, format='%Y-%m-%d %H:%M'):
    """格式化日期时间"""
    if isinstance(value, str):
        value = datetime.fromisoformat(value.replace('Z', '+00:00'))
    return value.strftime(format)

@app.template_filter('time_ago')
def time_ago(value):
    """显示相对时间"""
    if isinstance(value, str):
        value = datetime.fromisoformat(value.replace('Z', '+00:00'))
    
    now = datetime.now()
    diff = now - value
    
    if diff.days > 0:
        return f'{diff.days}天前'
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f'{hours}小时前'
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f'{minutes}分钟前'
    else:
        return '刚刚'

@app.template_filter('currency')
def currency_format(value):
    """格式化货币"""
    return f'¥{value:,.2f}'

@app.template_filter('percentage')
def percentage_format(value):
    """格式化百分比"""
    return f'{value}%'

@app.template_filter('status_badge')
def status_badge(status):
    """生成状态徽章"""
    badges = {
        'active': '<span class="badge bg-success">进行中</span>',
        'planning': '<span class="badge bg-warning">计划中</span>',
        'completed': '<span class="badge bg-primary">已完成</span>',
        'on_hold': '<span class="badge bg-secondary">暂停</span>',
        'pending': '<span class="badge bg-warning">待处理</span>',
        'in_progress': '<span class="badge bg-info">进行中</span>'
    }
    return badges.get(status, f'<span class="badge bg-light">{status}</span>')

@app.template_filter('priority_badge')
def priority_badge(priority):
    """生成优先级徽章"""
    badges = {
        'high': '<span class="badge bg-danger">高</span>',
        'medium': '<span class="badge bg-warning">中</span>',
        'low': '<span class="badge bg-secondary">低</span>'
    }
    return badges.get(priority, f'<span class="badge bg-light">{priority}</span>')

@app.template_filter('progress_bar')
def progress_bar(value, show_text=True):
    """生成进度条"""
    color_class = 'bg-success' if value >= 80 else 'bg-warning' if value >= 50 else 'bg-info'
    text = f'{value}%' if show_text else ''
    return f'''
    <div class="progress" style="height: 20px;">
        <div class="progress-bar {color_class}" role="progressbar" 
             style="width: {value}%" aria-valuenow="{value}" 
             aria-valuemin="0" aria-valuemax="100">{text}</div>
    </div>
    '''

@app.template_filter('avatar')
def avatar_filter(user_id):
    """获取用户头像"""
    user = next((u for u in users_db.values() if u['id'] == user_id), None)
    return user['avatar'] if user else '👤'

@app.template_filter('username')
def username_filter(user_id):
    """获取用户名"""
    user = next((u for u in users_db.values() if u['id'] == user_id), None)
    return user['name'] if user else '未知用户'

# 自定义全局函数
@app.template_global()
def get_project_stats():
    """获取项目统计信息"""
    total = len(projects_db)
    active = len([p for p in projects_db if p['status'] == 'active'])
    completed = len([p for p in projects_db if p['status'] == 'completed'])
    planning = len([p for p in projects_db if p['status'] == 'planning'])
    on_hold = len([p for p in projects_db if p['status'] == 'on_hold'])
    
    total_budget = sum(p['budget'] for p in projects_db)
    total_spent = sum(p['spent'] for p in projects_db)
    
    return {
        'total': total,
        'active': active,
        'completed': completed,
        'planning': planning,
        'on_hold': on_hold,
        'total_budget': total_budget,
        'total_spent': total_spent,
        'budget_utilization': (total_spent / total_budget * 100) if total_budget > 0 else 0
    }

@app.template_global()
def get_task_stats():
    """获取任务统计信息"""
    total = len(tasks_db)
    completed = len([t for t in tasks_db if t['status'] == 'completed'])
    in_progress = len([t for t in tasks_db if t['status'] == 'in_progress'])
    pending = len([t for t in tasks_db if t['status'] == 'pending'])
    
    total_estimated = sum(t['estimated_hours'] for t in tasks_db)
    total_actual = sum(t['actual_hours'] for t in tasks_db)
    
    return {
        'total': total,
        'completed': completed,
        'in_progress': in_progress,
        'pending': pending,
        'completion_rate': (completed / total * 100) if total > 0 else 0,
        'total_estimated': total_estimated,
        'total_actual': total_actual,
        'time_efficiency': (total_estimated / total_actual * 100) if total_actual > 0 else 0
    }

@app.template_global()
def get_user_by_id(user_id):
    """根据ID获取用户信息"""
    return next((u for u in users_db.values() if u['id'] == user_id), None)

@app.template_global()
def get_project_by_id(project_id):
    """根据ID获取项目信息"""
    return next((p for p in projects_db if p['id'] == project_id), None)

@app.template_global()
def get_recent_activities(limit=5):
    """获取最近活动"""
    activities = []
    
    # 添加项目活动
    for project in projects_db:
        activities.append({
            'type': 'project',
            'action': '更新了项目',
            'target': project['name'],
            'user_id': project['owner_id'],
            'timestamp': project['updated_at']
        })
    
    # 添加任务活动
    for task in tasks_db:
        activities.append({
            'type': 'task',
            'action': '更新了任务',
            'target': task['title'],
            'user_id': task['assignee_id'],
            'timestamp': task['updated_at']
        })
    
    # 按时间排序并限制数量
    activities.sort(key=lambda x: x['timestamp'], reverse=True)
    return activities[:limit]

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

# 认证装饰器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """获取当前登录用户"""
    if 'user_id' in session:
        return next((u for u in users_db.values() if u['id'] == session['user_id']), None)
    return None

# 基础模板
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ app_name }}{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Bootstrap Icons -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <style>
        :root {
            --primary-color: #0d6efd;
            --secondary-color: #6c757d;
            --success-color: #198754;
            --info-color: #0dcaf0;
            --warning-color: #ffc107;
            --danger-color: #dc3545;
            --light-color: #f8f9fa;
            --dark-color: #212529;
        }
        
        body {
            background-color: #f8f9fa;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .sidebar {
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            box-shadow: 2px 0 10px rgba(0,0,0,0.1);
        }
        
        .sidebar .nav-link {
            color: rgba(255,255,255,0.8);
            padding: 0.75rem 1rem;
            margin: 0.25rem 0;
            border-radius: 0.5rem;
            transition: all 0.3s ease;
        }
        
        .sidebar .nav-link:hover,
        .sidebar .nav-link.active {
            color: white;
            background-color: rgba(255,255,255,0.1);
            transform: translateX(5px);
        }
        
        .main-content {
            min-height: 100vh;
        }
        
        .card {
            border: none;
            border-radius: 1rem;
            box-shadow: 0 0.125rem 0.25rem rgba(0,0,0,0.075);
            transition: all 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.15);
        }
        
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 1rem;
            padding: 1.5rem;
            margin-bottom: 1rem;
        }
        
        .stat-card .stat-number {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .stat-card .stat-label {
            opacity: 0.8;
            font-size: 0.9rem;
        }
        
        .progress {
            height: 0.5rem;
            border-radius: 0.25rem;
        }
        
        .btn {
            border-radius: 0.5rem;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .btn:hover {
            transform: translateY(-1px);
        }
        
        .table {
            border-radius: 0.5rem;
            overflow: hidden;
        }
        
        .navbar-brand {
            font-weight: bold;
            font-size: 1.5rem;
        }
        
        .activity-item {
            padding: 1rem;
            border-left: 3px solid var(--primary-color);
            margin-bottom: 1rem;
            background: white;
            border-radius: 0.5rem;
            box-shadow: 0 0.125rem 0.25rem rgba(0,0,0,0.075);
        }
        
        .chart-container {
            position: relative;
            height: 300px;
            margin: 1rem 0;
        }
        
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(13,110,253,.3);
            border-radius: 50%;
            border-top-color: #0d6efd;
            animation: spin 1s ease-in-out infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .fade-in {
            animation: fadeIn 0.5s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1050;
            min-width: 300px;
            animation: slideInRight 0.3s ease-out;
        }
        
        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(100%);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        .modal-content {
            border-radius: 1rem;
            border: none;
        }
        
        .form-control, .form-select {
            border-radius: 0.5rem;
            border: 1px solid #dee2e6;
            transition: all 0.3s ease;
        }
        
        .form-control:focus, .form-select:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 0.2rem rgba(13,110,253,.25);
        }
    </style>
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% if current_user %}
    <div class="container-fluid">
        <div class="row">
            <!-- 侧边栏 -->
            <nav class="col-md-3 col-lg-2 d-md-block sidebar collapse">
                <div class="position-sticky pt-3">
                    <div class="text-center mb-4">
                        <h4 class="text-white">{{ app_name }}</h4>
                        <small class="text-white-50">v{{ app_version }}</small>
                    </div>
                    
                    <ul class="nav flex-column">
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('dashboard') }}">
                                <i class="bi bi-house-door"></i> 仪表板
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('projects') }}">
                                <i class="bi bi-folder"></i> 项目管理
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('tasks') }}">
                                <i class="bi bi-check-square"></i> 任务管理
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('reports') }}">
                                <i class="bi bi-graph-up"></i> 报表分析
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('profile') }}">
                                <i class="bi bi-person"></i> 个人资料
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('settings') }}">
                                <i class="bi bi-gear"></i> 系统设置
                            </a>
                        </li>
                    </ul>
                    
                    <hr class="text-white-50">
                    
                    <div class="text-center">
                        <div class="text-white mb-2">
                            {{ current_user.avatar }} {{ current_user.name }}
                        </div>
                        <small class="text-white-50">{{ current_user.role }}</small>
                        <div class="mt-2">
                            <a href="{{ url_for('logout') }}" class="btn btn-outline-light btn-sm">
                                <i class="bi bi-box-arrow-right"></i> 退出
                            </a>
                        </div>
                    </div>
                </div>
            </nav>
            
            <!-- 主内容区 -->
            <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4 main-content">
                <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
                    <h1 class="h2">{% block page_title %}仪表板{% endblock %}</h1>
                    <div class="btn-toolbar mb-2 mb-md-0">
                        {% block page_actions %}{% endblock %}
                    </div>
                </div>
                
                {% block content %}{% endblock %}
            </main>
        </div>
    </div>
    {% else %}
    {% block login_content %}{% endblock %}
    {% endif %}
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- 通用JavaScript -->
    <script>
        // 通知系统
        function showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = `alert alert-${type} alert-dismissible fade show notification`;
            notification.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            document.body.appendChild(notification);
            
            // 自动移除
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 5000);
        }
        
        // AJAX请求封装
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
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                return await response.json();
            } catch (error) {
                console.error('API请求失败:', error);
                showNotification('请求失败，请重试', 'danger');
                throw error;
            }
        }
        
        // 页面加载动画
        document.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('.fade-in').forEach(el => {
                el.style.opacity = '0';
                el.style.transform = 'translateY(20px)';
                
                setTimeout(() => {
                    el.style.transition = 'all 0.5s ease';
                    el.style.opacity = '1';
                    el.style.transform = 'translateY(0)';
                }, 100);
            });
        });
    </script>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
"""

# 登录页面模板
LOGIN_TEMPLATE = """
{% extends "base.html" %}

{% block title %}登录 - {{ app_name }}{% endblock %}

{% block login_content %}
<div class="container-fluid vh-100">
    <div class="row h-100">
        <div class="col-lg-6 d-none d-lg-flex align-items-center justify-content-center" 
             style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <div class="text-center text-white">
                <h1 class="display-4 mb-4">{{ app_name }}</h1>
                <p class="lead">现代化的项目管理平台</p>
                <div class="mt-5">
                    <i class="bi bi-check-circle" style="font-size: 3rem;"></i>
                    <h3 class="mt-3">高效协作</h3>
                    <p>团队协作，项目管理，一站式解决方案</p>
                </div>
            </div>
        </div>
        
        <div class="col-lg-6 d-flex align-items-center justify-content-center">
            <div class="card shadow-lg" style="width: 100%; max-width: 400px;">
                <div class="card-body p-5">
                    <div class="text-center mb-4">
                        <h2 class="card-title">欢迎回来</h2>
                        <p class="text-muted">请登录您的账户</p>
                    </div>
                    
                    {% if error %}
                    <div class="alert alert-danger" role="alert">
                        {{ error }}
                    </div>
                    {% endif %}
                    
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
                            <label class="form-check-label" for="remember">
                                记住我
                            </label>
                        </div>
                        
                        <button type="submit" class="btn btn-primary w-100 mb-3">
                            <span id="loginText">登录</span>
                            <span id="loginSpinner" class="loading d-none"></span>
                        </button>
                    </form>
                    
                    <div class="text-center">
                        <small class="text-muted">
                            演示账户：admin/admin123, developer/dev123, designer/design123
                        </small>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    document.getElementById('loginForm').addEventListener('submit', function(e) {
        const loginText = document.getElementById('loginText');
        const loginSpinner = document.getElementById('loginSpinner');
        
        loginText.classList.add('d-none');
        loginSpinner.classList.remove('d-none');
    });
</script>
 {% endblock %}
 """

# Flask应用和路由
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# 注册自定义过滤器
app.jinja_env.filters['datetime_format'] = datetime_format
app.jinja_env.filters['time_ago'] = time_ago
app.jinja_env.filters['currency'] = currency_format
app.jinja_env.filters['percentage'] = percentage_format
app.jinja_env.filters['status_badge'] = status_badge
app.jinja_env.filters['priority_badge'] = priority_badge
app.jinja_env.filters['progress_bar'] = progress_bar
app.jinja_env.filters['avatar'] = get_user_avatar
app.jinja_env.filters['username'] = get_username

# 注册全局函数
app.jinja_env.globals['get_project_stats'] = get_project_stats
app.jinja_env.globals['get_task_stats'] = get_task_stats
app.jinja_env.globals['get_user_by_id'] = get_user_by_id
app.jinja_env.globals['get_project_by_id'] = get_project_by_id
app.jinja_env.globals['get_recent_activities'] = get_recent_activities

# 上下文处理器
@app.context_processor
def inject_globals():
    return {
        'app_name': 'ProjectHub',
        'app_version': 'v1.0.0',
        'current_user': users_db[1],  # 默认使用第一个用户
        'users_db': users_db,
        'projects': projects_db,
        'tasks': tasks_db
    }

# 路由定义
@app.route('/')
def index():
    """首页 - 重定向到登录页面"""
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """登录页面"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 简单的用户验证（实际应用中应该使用更安全的方式）
        for user in users_db.values():
            if user.email == username and password == 'password123':  # 演示用固定密码
                session['user_id'] = user.id
                session['user_name'] = user.name
                return redirect(url_for('dashboard'))
        
        return render_template_string(LOGIN_TEMPLATE, error='用户名或密码错误')
    
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/logout')
def logout():
    """退出登录"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    """仪表板页面"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template_string(DASHBOARD_TEMPLATE)

@app.route('/projects')
def projects():
    """项目管理页面"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template_string(PROJECTS_TEMPLATE)

@app.route('/tasks')
def tasks():
    """任务管理页面"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template_string(TASKS_TEMPLATE)

@app.route('/reports')
def reports():
    """报表分析页面"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template_string(REPORTS_TEMPLATE)

@app.route('/profile')
def profile():
    """个人资料页面"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template_string(PROFILE_TEMPLATE)

@app.route('/settings')
def settings():
    """系统设置页面"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template_string(SETTINGS_TEMPLATE)

# API路由
@app.route('/api/projects', methods=['GET', 'POST'])
def api_projects():
    """项目API"""
    if 'user_id' not in session:
        return jsonify({'error': '未授权'}), 401
    
    if request.method == 'GET':
        return jsonify([{
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'status': p.status,
            'priority': p.priority,
            'progress': p.progress,
            'budget': p.budget,
            'spent': p.spent,
            'start_date': p.start_date.isoformat(),
            'end_date': p.end_date.isoformat(),
            'team_members': p.team_members,
            'tags': p.tags
        } for p in projects_db])
    
    elif request.method == 'POST':
        data = request.get_json()
        new_project = Project(
            id=len(projects_db) + 1,
            name=data['name'],
            description=data['description'],
            status=data.get('status', 'planning'),
            priority=data.get('priority', 'medium'),
            progress=0,
            budget=float(data.get('budget', 0)),
            spent=0,
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d'),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d'),
            team_members=data.get('team_members', []),
            tags=data.get('tags', [])
        )
        projects_db.append(new_project)
        return jsonify({'message': '项目创建成功', 'id': new_project.id})

@app.route('/api/projects/<int:project_id>', methods=['PUT', 'DELETE'])
def api_project_detail(project_id):
    """项目详情API"""
    if 'user_id' not in session:
        return jsonify({'error': '未授权'}), 401
    
    project = next((p for p in projects_db if p.id == project_id), None)
    if not project:
        return jsonify({'error': '项目不存在'}), 404
    
    if request.method == 'PUT':
        data = request.get_json()
        project.name = data.get('name', project.name)
        project.description = data.get('description', project.description)
        project.status = data.get('status', project.status)
        project.priority = data.get('priority', project.priority)
        project.budget = float(data.get('budget', project.budget))
        if 'start_date' in data:
            project.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        if 'end_date' in data:
            project.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
        project.team_members = data.get('team_members', project.team_members)
        project.tags = data.get('tags', project.tags)
        return jsonify({'message': '项目更新成功'})
    
    elif request.method == 'DELETE':
        projects_db.remove(project)
        return jsonify({'message': '项目删除成功'})

@app.route('/api/tasks', methods=['GET', 'POST'])
def api_tasks():
    """任务API"""
    if 'user_id' not in session:
        return jsonify({'error': '未授权'}), 401
    
    if request.method == 'GET':
        return jsonify([{
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'project_id': t.project_id,
            'assignee_id': t.assignee_id,
            'status': t.status,
            'priority': t.priority,
            'due_date': t.due_date.isoformat() if t.due_date else None,
            'estimated_hours': t.estimated_hours,
            'actual_hours': t.actual_hours,
            'tags': t.tags
        } for t in tasks_db])
    
    elif request.method == 'POST':
        data = request.get_json()
        new_task = Task(
            id=len(tasks_db) + 1,
            title=data['title'],
            description=data['description'],
            project_id=int(data['project_id']),
            assignee_id=int(data['assignee_id']),
            status=data.get('status', 'pending'),
            priority=data.get('priority', 'medium'),
            due_date=datetime.strptime(data['due_date'], '%Y-%m-%d') if data.get('due_date') else None,
            estimated_hours=int(data.get('estimated_hours', 0)),
            actual_hours=int(data.get('actual_hours', 0)),
            tags=data.get('tags', [])
        )
        tasks_db.append(new_task)
        return jsonify({'message': '任务创建成功', 'id': new_task.id})

@app.route('/api/tasks/<int:task_id>', methods=['PUT', 'DELETE'])
def api_task_detail(task_id):
    """任务详情API"""
    if 'user_id' not in session:
        return jsonify({'error': '未授权'}), 401
    
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        return jsonify({'error': '任务不存在'}), 404
    
    if request.method == 'PUT':
        data = request.get_json()
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.status = data.get('status', task.status)
        task.priority = data.get('priority', task.priority)
        if 'due_date' in data and data['due_date']:
            task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
        task.estimated_hours = int(data.get('estimated_hours', task.estimated_hours))
        task.actual_hours = int(data.get('actual_hours', task.actual_hours))
        task.tags = data.get('tags', task.tags)
        return jsonify({'message': '任务更新成功'})
    
    elif request.method == 'DELETE':
        tasks_db.remove(task)
        return jsonify({'message': '任务删除成功'})

@app.route('/api/tasks/<int:task_id>/status', methods=['PUT'])
def api_task_status(task_id):
    """更新任务状态API"""
    if 'user_id' not in session:
        return jsonify({'error': '未授权'}), 401
    
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        return jsonify({'error': '任务不存在'}), 404
    
    data = request.get_json()
    task.status = data['status']
    return jsonify({'message': '任务状态更新成功'})

@app.route('/api/users')
def api_users():
    """用户列表API"""
    if 'user_id' not in session:
        return jsonify({'error': '未授权'}), 401
    
    return jsonify([{
        'id': u.id,
        'name': u.name,
        'email': u.email,
        'role': u.role,
        'avatar': u.avatar
    } for u in users_db.values()])

@app.route('/api/stats')
def api_stats():
    """统计数据API"""
    if 'user_id' not in session:
        return jsonify({'error': '未授权'}), 401
    
    return jsonify({
        'projects': get_project_stats().__dict__,
        'tasks': get_task_stats().__dict__
    })

@app.route('/api/activities')
def api_activities():
    """最近活动API"""
    if 'user_id' not in session:
        return jsonify({'error': '未授权'}), 401
    
    activities = get_recent_activities(10)
    return jsonify([{
        'id': a.id,
        'user_id': a.user_id,
        'action': a.action,
        'target': a.target,
        'type': a.type,
        'timestamp': a.timestamp.isoformat()
    } for a in activities])

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Flask模板引擎和前端集成综合练习 - 完整解决方案")
    print("="*60)
    print("\n📋 功能特性:")
    print("   • Jinja2模板高级功能（自定义过滤器、全局函数、模板继承）")
    print("   • 前后端交互系统（用户认证、会话管理、AJAX API）")
    print("   • 现代化UI设计（Bootstrap、Chart.js、动画交互效果）")
    print("   • 项目和任务管理系统")
    print("   • 数据可视化和报表分析")
    print("   • 个人资料和系统设置")
    print("\n🔧 技术栈:")
    print("   • 后端: Flask + Jinja2")
    print("   • 前端: Bootstrap 5 + Chart.js + Vanilla JavaScript")
    print("   • 数据: 内存模拟数据库")
    print("\n🌐 访问地址: http://localhost:5000")
    print("\n👤 测试账户:")
    print("   • 用户名: admin@example.com")
    print("   • 密码: password123")
    print("\n" + "="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

# 任务管理页面模板
TASKS_TEMPLATE = """
{% extends "base.html" %}

{% block title %}任务管理 - {{ app_name }}{% endblock %}

{% block page_title %}任务管理{% endblock %}

{% block page_actions %}
<div class="btn-group" role="group">
    <button type="button" class="btn btn-outline-primary" onclick="filterTasks()">
        <i class="bi bi-funnel"></i> 筛选
    </button>
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#taskModal">
        <i class="bi bi-plus"></i> 新建任务
    </button>
</div>
{% endblock %}

{% block content %}
<div class="fade-in">
    <!-- 任务统计 -->
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <h3 class="text-primary">{{ get_task_stats().total }}</h3>
                    <p class="card-text">总任务数</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <h3 class="text-success">{{ get_task_stats().completed }}</h3>
                    <p class="card-text">已完成</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <h3 class="text-info">{{ get_task_stats().in_progress }}</h3>
                    <p class="card-text">进行中</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <h3 class="text-warning">{{ get_task_stats().pending }}</h3>
                    <p class="card-text">待处理</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- 任务列表 -->
    <div class="card">
        <div class="card-header">
            <h5 class="card-title mb-0">任务列表</h5>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>任务名称</th>
                            <th>项目</th>
                            <th>负责人</th>
                            <th>状态</th>
                            <th>优先级</th>
                            <th>截止日期</th>
                            <th>进度</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for task in tasks %}
                        <tr>
                            <td>
                                <div class="fw-bold">{{ task.title }}</div>
                                <small class="text-muted">{{ task.description[:50] }}...</small>
                            </td>
                            <td>
                                {% set project = get_project_by_id(task.project_id) %}
                                <span class="badge bg-light text-dark">{{ project.name if project else '未知项目' }}</span>
                            </td>
                            <td>
                                <div class="d-flex align-items-center">
                                    <span class="me-2">{{ task.assignee_id|avatar }}</span>
                                    {{ task.assignee_id|username }}
                                </div>
                            </td>
                            <td>{{ task.status|status_badge|safe }}</td>
                            <td>{{ task.priority|priority_badge|safe }}</td>
                            <td>
                                <small class="text-muted">
                                    {{ task.due_date|datetime_format('%Y-%m-%d') if task.due_date else '无' }}
                                </small>
                            </td>
                            <td>
                                {% if task.status == 'completed' %}
                                <span class="text-success">100%</span>
                                {% elif task.status == 'in_progress' %}
                                <span class="text-info">{{ (task.actual_hours / task.estimated_hours * 100)|round|int if task.estimated_hours > 0 else 0 }}%</span>
                                {% else %}
                                <span class="text-muted">0%</span>
                                {% endif %}
                            </td>
                            <td>
                                <div class="btn-group btn-group-sm" role="group">
                                    <button type="button" class="btn btn-outline-primary" 
                                            onclick="viewTask({{ task.id }})">
                                        <i class="bi bi-eye"></i>
                                    </button>
                                    <button type="button" class="btn btn-outline-success" 
                                            onclick="editTask({{ task.id }})">
                                        <i class="bi bi-pencil"></i>
                                    </button>
                                    <button type="button" class="btn btn-outline-danger" 
                                            onclick="deleteTask({{ task.id }})">
                                        <i class="bi bi-trash"></i>
                                    </button>
                                </div>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

<!-- 任务模态框 -->
<div class="modal fade" id="taskModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">新建任务</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <form id="taskForm">
                    <div class="row">
                        <div class="col-md-8">
                            <div class="mb-3">
                                <label for="taskTitle" class="form-label">任务标题</label>
                                <input type="text" class="form-control" id="taskTitle" required>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="mb-3">
                                <label for="taskProject" class="form-label">所属项目</label>
                                <select class="form-select" id="taskProject" required>
                                    <option value="">选择项目</option>
                                    {% for project in projects %}
                                    <option value="{{ project.id }}">{{ project.name }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label for="taskDescription" class="form-label">任务描述</label>
                        <textarea class="form-control" id="taskDescription" rows="3" required></textarea>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-4">
                            <div class="mb-3">
                                <label for="taskStatus" class="form-label">状态</label>
                                <select class="form-select" id="taskStatus" required>
                                    <option value="pending">待处理</option>
                                    <option value="in_progress">进行中</option>
                                    <option value="completed">已完成</option>
                                </select>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="mb-3">
                                <label for="taskPriority" class="form-label">优先级</label>
                                <select class="form-select" id="taskPriority" required>
                                    <option value="low">低</option>
                                    <option value="medium">中</option>
                                    <option value="high">高</option>
                                </select>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="mb-3">
                                <label for="taskAssignee" class="form-label">负责人</label>
                                <select class="form-select" id="taskAssignee" required>
                                    <option value="">选择负责人</option>
                                    {% for user in users_db.values() %}
                                    <option value="{{ user.id }}">{{ user.name }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-4">
                            <div class="mb-3">
                                <label for="taskDueDate" class="form-label">截止日期</label>
                                <input type="date" class="form-control" id="taskDueDate">
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="mb-3">
                                <label for="taskEstimatedHours" class="form-label">预估工时</label>
                                <input type="number" class="form-control" id="taskEstimatedHours" min="1">
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="mb-3">
                                <label for="taskActualHours" class="form-label">实际工时</label>
                                <input type="number" class="form-control" id="taskActualHours" min="0" value="0">
                            </div>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label for="taskTags" class="form-label">标签（用逗号分隔）</label>
                        <input type="text" class="form-control" id="taskTags" 
                               placeholder="例如：前端,React,紧急">
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                <button type="button" class="btn btn-primary" onclick="saveTask()">保存</button>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    function filterTasks() {
        showNotification('筛选功能开发中', 'info');
    }
    
    function viewTask(id) {
        showNotification('查看任务详情功能开发中', 'info');
    }
    
    function editTask(id) {
        showNotification('编辑任务功能开发中', 'info');
    }
    
    function deleteTask(id) {
        if (confirm('确定要删除这个任务吗？')) {
            showNotification('任务已删除', 'success');
        }
    }
    
    async function saveTask() {
        const formData = {
            title: document.getElementById('taskTitle').value,
            description: document.getElementById('taskDescription').value,
            project_id: document.getElementById('taskProject').value,
            status: document.getElementById('taskStatus').value,
            priority: document.getElementById('taskPriority').value,
            assignee_id: document.getElementById('taskAssignee').value,
            due_date: document.getElementById('taskDueDate').value,
            estimated_hours: document.getElementById('taskEstimatedHours').value,
            actual_hours: document.getElementById('taskActualHours').value,
            tags: document.getElementById('taskTags').value.split(',').map(tag => tag.trim())
        };
        
        try {
            const response = await apiRequest('/api/tasks', {
                method: 'POST',
                body: JSON.stringify(formData)
            });
            
            showNotification('任务创建成功', 'success');
            bootstrap.Modal.getInstance(document.getElementById('taskModal')).hide();
            location.reload();
        } catch (error) {
            showNotification('创建失败，请重试', 'danger');
        }
    }
</script>
{% endblock %}
"""

# 报表分析页面模板
REPORTS_TEMPLATE = """
{% extends "base.html" %}

{% block title %}报表分析 - {{ app_name }}{% endblock %}

{% block page_title %}报表分析{% endblock %}

{% block page_actions %}
<div class="btn-group" role="group">
    <button type="button" class="btn btn-outline-primary" onclick="exportReport()">
        <i class="bi bi-download"></i> 导出报表
    </button>
    <button type="button" class="btn btn-primary" onclick="refreshReports()">
        <i class="bi bi-arrow-clockwise"></i> 刷新数据
    </button>
</div>
{% endblock %}

{% block content %}
<div class="fade-in">
    <!-- 关键指标 -->
    <div class="row mb-4">
        <div class="col-lg-3 col-md-6">
            <div class="card bg-primary text-white">
                <div class="card-body">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h4>{{ get_project_stats().total }}</h4>
                            <p class="mb-0">总项目数</p>
                        </div>
                        <div class="align-self-center">
                            <i class="bi bi-folder" style="font-size: 2rem;"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-lg-3 col-md-6">
            <div class="card bg-success text-white">
                <div class="card-body">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h4>{{ '%.1f'|format(get_project_stats().budget_utilization) }}%</h4>
                            <p class="mb-0">预算使用率</p>
                        </div>
                        <div class="align-self-center">
                            <i class="bi bi-currency-dollar" style="font-size: 2rem;"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-lg-3 col-md-6">
            <div class="card bg-info text-white">
                <div class="card-body">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h4>{{ '%.1f'|format(get_task_stats().completion_rate) }}%</h4>
                            <p class="mb-0">任务完成率</p>
                        </div>
                        <div class="align-self-center">
                            <i class="bi bi-check-circle" style="font-size: 2rem;"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-lg-3 col-md-6">
            <div class="card bg-warning text-white">
                <div class="card-body">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h4>{{ '%.1f'|format(get_task_stats().time_efficiency) }}%</h4>
                            <p class="mb-0">时间效率</p>
                        </div>
                        <div class="align-self-center">
                            <i class="bi bi-clock" style="font-size: 2rem;"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- 图表区域 -->
    <div class="row">
        <div class="col-lg-8">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">项目进度趋势</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="progressTrendChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-lg-4">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">项目状态分布</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="statusDistributionChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="row mt-4">
        <div class="col-lg-6">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">团队工作量分布</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="workloadChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-lg-6">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">预算执行情况</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="budgetExecutionChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- 详细数据表格 -->
    <div class="row mt-4">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">项目详细数据</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>项目名称</th>
                                    <th>状态</th>
                                    <th>进度</th>
                                    <th>预算</th>
                                    <th>已用</th>
                                    <th>预算使用率</th>
                                    <th>团队成员</th>
                                    <th>开始日期</th>
                                    <th>结束日期</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for project in projects %}
                                <tr>
                                    <td>{{ project.name }}</td>
                                    <td>{{ project.status|status_badge|safe }}</td>
                                    <td>
                                        <div class="d-flex align-items-center">
                                            <div class="progress me-2" style="width: 100px; height: 20px;">
                                                <div class="progress-bar" role="progressbar" 
                                                     style="width: {{ project.progress }}%"></div>
                                            </div>
                                            <span>{{ project.progress }}%</span>
                                        </div>
                                    </td>
                                    <td>{{ project.budget|currency }}</td>
                                    <td>{{ project.spent|currency }}</td>
                                    <td>
                                        {% set usage_rate = (project.spent / project.budget * 100) if project.budget > 0 else 0 %}
                                        <span class="{% if usage_rate > 90 %}text-danger{% elif usage_rate > 70 %}text-warning{% else %}text-success{% endif %}">
                                            {{ '%.1f'|format(usage_rate) }}%
                                        </span>
                                    </td>
                                    <td>{{ project.team_members|length }}</td>
                                    <td>{{ project.start_date|datetime_format('%Y-%m-%d') }}</td>
                                    <td>{{ project.end_date|datetime_format('%Y-%m-%d') }}</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        initProgressTrendChart();
        initStatusDistributionChart();
        initWorkloadChart();
        initBudgetExecutionChart();
    });
    
    function initProgressTrendChart() {
        const ctx = document.getElementById('progressTrendChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['1月', '2月', '3月', '4月', '5月', '6月'],
                datasets: [{
                    label: '企业管理系统',
                    data: [10, 25, 40, 55, 65, 75],
                    borderColor: 'rgba(13, 110, 253, 1)',
                    backgroundColor: 'rgba(13, 110, 253, 0.1)',
                    tension: 0.4
                }, {
                    label: '移动端电商应用',
                    data: [0, 5, 10, 15, 20, 25],
                    borderColor: 'rgba(255, 193, 7, 1)',
                    backgroundColor: 'rgba(255, 193, 7, 0.1)',
                    tension: 0.4
                }, {
                    label: '数据分析平台',
                    data: [20, 40, 60, 80, 95, 100],
                    borderColor: 'rgba(25, 135, 84, 1)',
                    backgroundColor: 'rgba(25, 135, 84, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }
    
    function initStatusDistributionChart() {
        const ctx = document.getElementById('statusDistributionChart').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['进行中', '计划中', '已完成', '暂停'],
                datasets: [{
                    data: [1, 1, 1, 1],
                    backgroundColor: [
                        'rgba(25, 135, 84, 0.8)',
                        'rgba(255, 193, 7, 0.8)',
                        'rgba(13, 110, 253, 0.8)',
                        'rgba(108, 117, 125, 0.8)'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
    
    function initWorkloadChart() {
        const ctx = document.getElementById('workloadChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['系统管理员', '开发工程师', 'UI设计师'],
                datasets: [{
                    label: '任务数量',
                    data: [2, 3, 2],
                    backgroundColor: 'rgba(13, 110, 253, 0.8)',
                    borderColor: 'rgba(13, 110, 253, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    function initBudgetExecutionChart() {
        const ctx = document.getElementById('budgetExecutionChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['企业管理系统', '移动端电商应用', '数据分析平台', '在线教育平台'],
                datasets: [{
                    label: '预算',
                    data: [500000, 300000, 800000, 400000],
                    backgroundColor: 'rgba(13, 110, 253, 0.3)',
                    borderColor: 'rgba(13, 110, 253, 1)',
                    borderWidth: 1
                }, {
                    label: '实际支出',
                    data: [375000, 75000, 750000, 160000],
                    backgroundColor: 'rgba(220, 53, 69, 0.8)',
                    borderColor: 'rgba(220, 53, 69, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    function exportReport() {
        showNotification('报表导出功能开发中', 'info');
    }
    
    function refreshReports() {
        showNotification('数据已刷新', 'success');
        // 重新初始化图表
        setTimeout(() => {
            initProgressTrendChart();
            initStatusDistributionChart();
            initWorkloadChart();
            initBudgetExecutionChart();
        }, 500);
    }
</script>
{% endblock %}
"""

# 个人资料页面模板
PROFILE_TEMPLATE = """
{% extends "base.html" %}

{% block title %}个人资料 - {{ app_name }}{% endblock %}

{% block page_title %}个人资料{% endblock %}

{% block content %}
<div class="fade-in">
    <div class="row">
        <div class="col-lg-4">
            <!-- 用户信息卡片 -->
            <div class="card">
                <div class="card-body text-center">
                    <div class="mb-3">
                        <div style="font-size: 4rem;">{{ current_user.avatar }}</div>
                    </div>
                    <h4>{{ current_user.name }}</h4>
                    <p class="text-muted">{{ current_user.role }}</p>
                    <p class="text-muted">{{ current_user.email }}</p>
                    
                    <div class="row text-center mt-4">
                        <div class="col-4">
                            <div class="fw-bold">{{ projects|length }}</div>
                            <small class="text-muted">参与项目</small>
                        </div>
                        <div class="col-4">
                            <div class="fw-bold">{{ tasks|length }}</div>
                            <small class="text-muted">负责任务</small>
                        </div>
                        <div class="col-4">
                            <div class="fw-bold">{{ current_user.created_at|time_ago }}</div>
                            <small class="text-muted">加入时间</small>
                        </div>
                    </div>
                    
                    <div class="mt-4">
                        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#editProfileModal">
                            <i class="bi bi-pencil"></i> 编辑资料
                        </button>
                    </div>
                </div>
            </div>
            
            <!-- 最近活动 -->
            <div class="card mt-4">
                <div class="card-header">
                    <h5 class="card-title mb-0">最近活动</h5>
                </div>
                <div class="card-body">
                    {% for activity in get_recent_activities(3) %}
                    {% if activity.user_id == current_user.id %}
                    <div class="d-flex align-items-center mb-3">
                        <div class="me-3">
                            <i class="bi bi-{{ 'folder' if activity.type == 'project' else 'check-square' }} text-primary"></i>
                        </div>
                        <div class="flex-grow-1">
                            <div class="fw-bold">{{ activity.action }}</div>
                            <div class="text-muted small">{{ activity.target }}</div>
                            <div class="text-muted small">{{ activity.timestamp|time_ago }}</div>
                        </div>
                    </div>
                    {% endif %}
                    {% endfor %}
                </div>
            </div>
        </div>
        
        <div class="col-lg-8">
            <!-- 我的项目 -->
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">我的项目</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        {% for project in projects %}
                        {% if current_user.id in project.team_members %}
                        <div class="col-md-6 mb-3">
                            <div class="card border">
                                <div class="card-body">
                                    <div class="d-flex justify-content-between align-items-start mb-2">
                                        <h6 class="card-title">{{ project.name }}</h6>
                                        {{ project.status|status_badge|safe }}
                                    </div>
                                    <p class="card-text small text-muted">{{ project.description[:80] }}...</p>
                                    <div class="mb-2">
                                        <div class="d-flex justify-content-between mb-1">
                                            <small>进度</small>
                                            <small>{{ project.progress }}%</small>
                                        </div>
                                        {{ project.progress|progress_bar(False)|safe }}
                                    </div>
                                    <small class="text-muted">
                                        <i class="bi bi-calendar"></i> {{ project.end_date|datetime_format('%Y-%m-%d') }}
                                    </small>
                                </div>
                            </div>
                        </div>
                        {% endif %}
                        {% endfor %}
                    </div>
                </div>
            </div>
            
            <!-- 我的任务 -->
            <div class="card mt-4">
                <div class="card-header">
                    <h5 class="card-title mb-0">我的任务</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-sm">
                            <thead>
                                <tr>
                                    <th>任务名称</th>
                                    <th>项目</th>
                                    <th>状态</th>
                                    <th>优先级</th>
                                    <th>截止日期</th>
                                    <th>操作</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for task in tasks %}
                                {% if task.assignee_id == current_user.id %}
                                <tr>
                                    <td>{{ task.title }}</td>
                                    <td>
                                        {% set project = get_project_by_id(task.project_id) %}
                                        <small class="text-muted">{{ project.name if project else '未知项目' }}</small>
                                    </td>
                                    <td>{{ task.status|status_badge|safe }}</td>
                                    <td>{{ task.priority|priority_badge|safe }}</td>
                                    <td>
                                        <small>{{ task.due_date|datetime_format('%m-%d') if task.due_date else '无' }}</small>
                                    </td>
                                    <td>
                                        <button type="button" class="btn btn-outline-primary btn-sm" 
                                                onclick="updateTaskStatus({{ task.id }})">
                                            <i class="bi bi-check"></i>
                                        </button>
                                    </td>
                                </tr>
                                {% endif %}
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- 编辑资料模态框 -->
<div class="modal fade" id="editProfileModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">编辑个人资料</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <form id="profileForm">
                    <div class="mb-3">
                        <label for="profileName" class="form-label">姓名</label>
                        <input type="text" class="form-control" id="profileName" value="{{ current_user.name }}">
                    </div>
                    <div class="mb-3">
                        <label for="profileEmail" class="form-label">邮箱</label>
                        <input type="email" class="form-control" id="profileEmail" value="{{ current_user.email }}">
                    </div>
                    <div class="mb-3">
                        <label for="profileAvatar" class="form-label">头像</label>
                        <select class="form-select" id="profileAvatar">
                            <option value="👨‍💼" {{ 'selected' if current_user.avatar == '👨‍💼' else '' }}>👨‍💼 管理员</option>
                            <option value="👨‍💻" {{ 'selected' if current_user.avatar == '👨‍💻' else '' }}>👨‍💻 开发者</option>
                            <option value="👩‍🎨" {{ 'selected' if current_user.avatar == '👩‍🎨' else '' }}>👩‍🎨 设计师</option>
                            <option value="👤" {{ 'selected' if current_user.avatar == '👤' else '' }}>👤 默认</option>
                        </select>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                <button type="button" class="btn btn-primary" onclick="saveProfile()">保存</button>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    function updateTaskStatus(taskId) {
        showNotification('任务状态更新功能开发中', 'info');
    }
    
    function saveProfile() {
        const formData = {
            name: document.getElementById('profileName').value,
            email: document.getElementById('profileEmail').value,
            avatar: document.getElementById('profileAvatar').value
        };
        
        // 模拟保存
        showNotification('个人资料已更新', 'success');
        bootstrap.Modal.getInstance(document.getElementById('editProfileModal')).hide();
    }
</script>
{% endblock %}
"""

# 设置页面模板
SETTINGS_TEMPLATE = """
{% extends "base.html" %}

{% block title %}系统设置 - {{ app_name }}{% endblock %}

{% block page_title %}系统设置{% endblock %}

{% block content %}
<div class="fade-in">
    <div class="row">
        <div class="col-lg-8">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">个人偏好设置</h5>
                </div>
                <div class="card-body">
                    <form id="settingsForm">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="theme" class="form-label">主题</label>
                                    <select class="form-select" id="theme">
                                        <option value="light" {{ 'selected' if current_user.settings.theme == 'light' else '' }}>浅色主题</option>
                                        <option value="dark" {{ 'selected' if current_user.settings.theme == 'dark' else '' }}>深色主题</option>
                                        <option value="auto">跟随系统</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="language" class="form-label">语言</label>
                                    <select class="form-select" id="language">
                                        <option value="zh-CN" {{ 'selected' if current_user.settings.language == 'zh-CN' else '' }}>简体中文</option>
                                        <option value="en-US">English</option>
                                        <option value="ja-JP">日本語</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" id="notifications" 
                                       {{ 'checked' if current_user.settings.notifications else '' }}>
                                <label class="form-check-label" for="notifications">
                                    启用桌面通知
                                </label>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" id="emailAlerts" 
                                       {{ 'checked' if current_user.settings.email_alerts else '' }}>
                                <label class="form-check-label" for="emailAlerts">
                                    启用邮件提醒
                                </label>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label for="timezone" class="form-label">时区</label>
                            <select class="form-select" id="timezone">
                                <option value="Asia/Shanghai" selected>中国标准时间 (UTC+8)</option>
                                <option value="America/New_York">美国东部时间 (UTC-5)</option>
                                <option value="Europe/London">英国时间 (UTC+0)</option>
                                <option value="Asia/Tokyo">日本标准时间 (UTC+9)</option>
                            </select>
                        </div>
                        
                        <div class="mb-3">
                            <label for="dateFormat" class="form-label">日期格式</label>
                            <select class="form-select" id="dateFormat">
                                <option value="YYYY-MM-DD" selected>2024-12-24</option>
                                <option value="MM/DD/YYYY">12/24/2024</option>
                                <option value="DD/MM/YYYY">24/12/2024</option>
                                <option value="DD-MM-YYYY">24-12-2024</option>
                            </select>
                        </div>
                        
                        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                            <button type="button" class="btn btn-secondary" onclick="resetSettings()">重置</button>
                            <button type="button" class="btn btn-primary" onclick="saveSettings()">保存设置</button>
                        </div>
                    </form>
                </div>
            </div>
            
            <!-- 安全设置 -->
            <div class="card mt-4">
                <div class="card-header">
                    <h5 class="card-title mb-0">安全设置</h5>
                </div>
                <div class="card-body">
                    <form id="securityForm">
                        <div class="mb-3">
                            <label for="currentPassword" class="form-label">当前密码</label>
                            <input type="password" class="form-control" id="currentPassword">
                        </div>
                        
                        <div class="mb-3">
                            <label for="newPassword" class="form-label">新密码</label>
                            <input type="password" class="form-control" id="newPassword">
                        </div>
                        
                        <div class="mb-3">
                            <label for="confirmPassword" class="form-label">确认新密码</label>
                            <input type="password" class="form-control" id="confirmPassword">
                        </div>
                        
                        <div class="mb-3">
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" id="twoFactor">
                                <label class="form-check-label" for="twoFactor">
                                    启用双因素认证
                                </label>
                            </div>
                        </div>
                        
                        <button type="button" class="btn btn-warning" onclick="changePassword()">
                            <i class="bi bi-shield-lock"></i> 更改密码
                        </button>
                    </form>
                </div>
            </div>
        </div>
        
        <div class="col-lg-4">
            <!-- 系统信息 -->
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">系统信息</h5>
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        <div class="d-flex justify-content-between">
                            <span>应用版本:</span>
                            <span class="fw-bold">{{ app_version }}</span>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <div class="d-flex justify-content-between">
                            <span>最后登录:</span>
                            <span class="text-muted">{{ current_user.last_login|time_ago }}</span>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <div class="d-flex justify-content-between">
                            <span>账户创建:</span>
                            <span class="text-muted">{{ current_user.created_at|time_ago }}</span>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <div class="d-flex justify-content-between">
                            <span>用户角色:</span>
                            <span class="badge bg-primary">{{ current_user.role }}</span>
                        </div>
                    </div>
                    
                    <hr>
                    
                    <div class="d-grid gap-2">
                        <button type="button" class="btn btn-outline-info" onclick="exportData()">
                            <i class="bi bi-download"></i> 导出数据
                        </button>
                        <button type="button" class="btn btn-outline-warning" onclick="clearCache()">
                            <i class="bi bi-trash"></i> 清除缓存
                        </button>
                        <button type="button" class="btn btn-outline-danger" onclick="deleteAccount()">
                            <i class="bi bi-exclamation-triangle"></i> 删除账户
                        </button>
                    </div>
                </div>
            </div>
            
            <!-- 快捷操作 -->
            <div class="card mt-4">
                <div class="card-header">
                    <h5 class="card-title mb-0">快捷操作</h5>
                </div>
                <div class="card-body">
                    <div class="d-grid gap-2">
                        <button type="button" class="btn btn-outline-primary" onclick="backupData()">
                            <i class="bi bi-cloud-upload"></i> 备份数据
                        </button>
                        <button type="button" class="btn btn-outline-success" onclick="syncData()">
                            <i class="bi bi-arrow-repeat"></i> 同步数据
                        </button>
                        <button type="button" class="btn btn-outline-info" onclick="checkUpdates()">
                            <i class="bi bi-arrow-up-circle"></i> 检查更新
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    function saveSettings() {
        const settings = {
            theme: document.getElementById('theme').value,
            language: document.getElementById('language').value,
            notifications: document.getElementById('notifications').checked,
            email_alerts: document.getElementById('emailAlerts').checked,
            timezone: document.getElementById('timezone').value,
            date_format: document.getElementById('dateFormat').value
        };
        
        showNotification('设置已保存', 'success');
    }
    
    function resetSettings() {
        if (confirm('确定要重置所有设置吗？')) {
            document.getElementById('settingsForm').reset();
            showNotification('设置已重置', 'info');
        }
    }
    
    function changePassword() {
        const currentPassword = document.getElementById('currentPassword').value;
        const newPassword = document.getElementById('newPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        if (!currentPassword || !newPassword || !confirmPassword) {
            showNotification('请填写所有密码字段', 'warning');
            return;
        }
        
        if (newPassword !== confirmPassword) {
            showNotification('新密码和确认密码不匹配', 'danger');
            return;
        }
        
        showNotification('密码已更改', 'success');
        document.getElementById('securityForm').reset();
    }
    
    function exportData() {
        showNotification('数据导出功能开发中', 'info');
    }
    
    function clearCache() {
        if (confirm('确定要清除缓存吗？')) {
            showNotification('缓存已清除', 'success');
        }
    }
    
    function deleteAccount() {
        if (confirm('警告：删除账户将永久删除所有数据，此操作不可恢复！确定要继续吗？')) {
            showNotification('账户删除功能需要管理员权限', 'warning');
        }
    }
    
    function backupData() {
        showNotification('数据备份功能开发中', 'info');
    }
    
    function syncData() {
        showNotification('正在同步数据...', 'info');
        setTimeout(() => {
            showNotification('数据同步完成', 'success');
        }, 2000);
    }
    
    function checkUpdates() {
        showNotification('检查更新中...', 'info');
        setTimeout(() => {
            showNotification('当前已是最新版本', 'success');
        }, 1500);
    }
</script>
{% endblock %}
"""

# 仪表板页面模板
DASHBOARD_TEMPLATE = """
{% extends "base.html" %}

{% block title %}仪表板 - {{ app_name }}{% endblock %}

{% block page_title %}仪表板{% endblock %}

{% block page_actions %}
<div class="btn-group" role="group">
    <button type="button" class="btn btn-outline-primary" onclick="refreshData()">
        <i class="bi bi-arrow-clockwise"></i> 刷新
    </button>
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#quickActionModal">
        <i class="bi bi-plus"></i> 快速操作
    </button>
</div>
{% endblock %}

{% block content %}
<div class="fade-in">
    <!-- 统计卡片 -->
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="stat-card">
                <div class="stat-number">{{ get_project_stats().total }}</div>
                <div class="stat-label">总项目数</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stat-card" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">
                <div class="stat-number">{{ get_project_stats().active }}</div>
                <div class="stat-label">进行中项目</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stat-card" style="background: linear-gradient(135deg, #fc466b 0%, #3f5efb 100%);">
                <div class="stat-number">{{ get_task_stats().total }}</div>
                <div class="stat-label">总任务数</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stat-card" style="background: linear-gradient(135deg, #fdbb2d 0%, #22c1c3 100%);">
                <div class="stat-number">{{ '%.1f'|format(get_task_stats().completion_rate) }}%</div>
                <div class="stat-label">任务完成率</div>
            </div>
        </div>
    </div>
    
    <div class="row">
        <!-- 项目进度图表 -->
        <div class="col-lg-8">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">项目进度概览</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="projectChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 最近活动 -->
        <div class="col-lg-4">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">最近活动</h5>
                </div>
                <div class="card-body">
                    {% for activity in get_recent_activities() %}
                    <div class="activity-item">
                        <div class="d-flex align-items-center">
                            <div class="me-3">
                                {{ get_user_by_id(activity.user_id).avatar }}
                            </div>
                            <div class="flex-grow-1">
                                <div class="fw-bold">{{ get_user_by_id(activity.user_id).name }}</div>
                                <div class="text-muted small">
                                    {{ activity.action }} "{{ activity.target }}"
                                </div>
                                <div class="text-muted small">
                                    {{ activity.timestamp|time_ago }}
                                </div>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
    
    <!-- 任务状态分布 -->
    <div class="row mt-4">
        <div class="col-lg-6">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">任务状态分布</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="taskChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 预算使用情况 -->
        <div class="col-lg-6">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">预算使用情况</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="budgetChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- 快速操作模态框 -->
<div class="modal fade" id="quickActionModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">快速操作</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <div class="d-grid gap-2">
                    <button type="button" class="btn btn-primary" onclick="createProject()">
                        <i class="bi bi-folder-plus"></i> 创建新项目
                    </button>
                    <button type="button" class="btn btn-success" onclick="createTask()">
                        <i class="bi bi-plus-square"></i> 创建新任务
                    </button>
                    <button type="button" class="btn btn-info" onclick="generateReport()">
                        <i class="bi bi-file-earmark-text"></i> 生成报表
                    </button>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    // 初始化图表
    document.addEventListener('DOMContentLoaded', function() {
        initProjectChart();
        initTaskChart();
        initBudgetChart();
    });
    
    function initProjectChart() {
        const ctx = document.getElementById('projectChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['企业管理系统', '移动端电商应用', '数据分析平台', '在线教育平台'],
                datasets: [{
                    label: '进度 (%)',
                    data: [75, 25, 100, 40],
                    backgroundColor: [
                        'rgba(13, 110, 253, 0.8)',
                        'rgba(255, 193, 7, 0.8)',
                        'rgba(25, 135, 84, 0.8)',
                        'rgba(108, 117, 125, 0.8)'
                    ],
                    borderColor: [
                        'rgba(13, 110, 253, 1)',
                        'rgba(255, 193, 7, 1)',
                        'rgba(25, 135, 84, 1)',
                        'rgba(108, 117, 125, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }
    
    function initTaskChart() {
        const ctx = document.getElementById('taskChart').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['已完成', '进行中', '待处理'],
                datasets: [{
                    data: [2, 2, 1],
                    backgroundColor: [
                        'rgba(25, 135, 84, 0.8)',
                        'rgba(13, 202, 240, 0.8)',
                        'rgba(255, 193, 7, 0.8)'
                    ],
                    borderColor: [
                        'rgba(25, 135, 84, 1)',
                        'rgba(13, 202, 240, 1)',
                        'rgba(255, 193, 7, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
    
    function initBudgetChart() {
        const ctx = document.getElementById('budgetChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['1月', '2月', '3月', '4月', '5月', '6月'],
                datasets: [{
                    label: '预算',
                    data: [500000, 500000, 500000, 500000, 500000, 500000],
                    borderColor: 'rgba(13, 110, 253, 1)',
                    backgroundColor: 'rgba(13, 110, 253, 0.1)',
                    tension: 0.4
                }, {
                    label: '实际支出',
                    data: [50000, 120000, 200000, 280000, 340000, 375000],
                    borderColor: 'rgba(220, 53, 69, 1)',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    function refreshData() {
        showNotification('数据已刷新', 'success');
    }
    
    function createProject() {
        window.location.href = '/projects?action=create';
    }
    
    function createTask() {
        window.location.href = '/tasks?action=create';
    }
    
    function generateReport() {
        window.location.href = '/reports';
    }
</script>
{% endblock %}
"""

# 项目管理页面模板
PROJECTS_TEMPLATE = """
{% extends "base.html" %}

{% block title %}项目管理 - {{ app_name }}{% endblock %}

{% block page_title %}项目管理{% endblock %}

{% block page_actions %}
<div class="btn-group" role="group">
    <button type="button" class="btn btn-outline-primary" onclick="filterProjects()">
        <i class="bi bi-funnel"></i> 筛选
    </button>
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#projectModal">
        <i class="bi bi-plus"></i> 新建项目
    </button>
</div>
{% endblock %}

{% block content %}
<div class="fade-in">
    <!-- 筛选器 -->
    <div class="card mb-4" id="filterCard" style="display: none;">
        <div class="card-body">
            <div class="row">
                <div class="col-md-3">
                    <select class="form-select" id="statusFilter">
                        <option value="">所有状态</option>
                        <option value="active">进行中</option>
                        <option value="planning">计划中</option>
                        <option value="completed">已完成</option>
                        <option value="on_hold">暂停</option>
                    </select>
                </div>
                <div class="col-md-3">
                    <select class="form-select" id="priorityFilter">
                        <option value="">所有优先级</option>
                        <option value="high">高</option>
                        <option value="medium">中</option>
                        <option value="low">低</option>
                    </select>
                </div>
                <div class="col-md-3">
                    <select class="form-select" id="categoryFilter">
                        <option value="">所有分类</option>
                        <option value="enterprise">企业级</option>
                        <option value="mobile">移动端</option>
                        <option value="analytics">数据分析</option>
                        <option value="education">教育</option>
                    </select>
                </div>
                <div class="col-md-3">
                    <button type="button" class="btn btn-primary" onclick="applyFilters()">
                        应用筛选
                    </button>
                </div>
            </div>
        </div>
    </div>
    
    <!-- 项目列表 -->
    <div class="row" id="projectsList">
        {% for project in projects %}
        <div class="col-lg-6 mb-4 project-card" 
             data-status="{{ project.status }}" 
             data-priority="{{ project.priority }}" 
             data-category="{{ project.category }}">
            <div class="card h-100">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h5 class="card-title mb-0">{{ project.name }}</h5>
                    <div>
                        {{ project.status|status_badge|safe }}
                        {{ project.priority|priority_badge|safe }}
                    </div>
                </div>
                <div class="card-body">
                    <p class="card-text">{{ project.description }}</p>
                    
                    <div class="mb-3">
                        <div class="d-flex justify-content-between mb-1">
                            <small>进度</small>
                            <small>{{ project.progress }}%</small>
                        </div>
                        {{ project.progress|progress_bar(False)|safe }}
                    </div>
                    
                    <div class="row text-center">
                        <div class="col-4">
                            <div class="fw-bold">{{ project.budget|currency }}</div>
                            <small class="text-muted">预算</small>
                        </div>
                        <div class="col-4">
                            <div class="fw-bold">{{ project.spent|currency }}</div>
                            <small class="text-muted">已用</small>
                        </div>
                        <div class="col-4">
                            <div class="fw-bold">{{ project.team_members|length }}</div>
                            <small class="text-muted">成员</small>
                        </div>
                    </div>
                    
                    <div class="mt-3">
                        <small class="text-muted">
                            <i class="bi bi-calendar"></i> 
                            {{ project.start_date|datetime_format('%Y-%m-%d') }} - 
                            {{ project.end_date|datetime_format('%Y-%m-%d') }}
                        </small>
                    </div>
                    
                    <div class="mt-2">
                        {% for tag in project.tags %}
                        <span class="badge bg-light text-dark me-1">{{ tag }}</span>
                        {% endfor %}
                    </div>
                </div>
                <div class="card-footer">
                    <div class="btn-group w-100" role="group">
                        <button type="button" class="btn btn-outline-primary" 
                                onclick="viewProject({{ project.id }})">
                            <i class="bi bi-eye"></i> 查看
                        </button>
                        <button type="button" class="btn btn-outline-success" 
                                onclick="editProject({{ project.id }})">
                            <i class="bi bi-pencil"></i> 编辑
                        </button>
                        <button type="button" class="btn btn-outline-danger" 
                                onclick="deleteProject({{ project.id }})">
                            <i class="bi bi-trash"></i> 删除
                        </button>
                    </div>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>

<!-- 项目模态框 -->
<div class="modal fade" id="projectModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">新建项目</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <form id="projectForm">
                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="projectName" class="form-label">项目名称</label>
                                <input type="text" class="form-control" id="projectName" required>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="projectCategory" class="form-label">项目分类</label>
                                <select class="form-select" id="projectCategory" required>
                                    <option value="">选择分类</option>
                                    <option value="enterprise">企业级</option>
                                    <option value="mobile">移动端</option>
                                    <option value="analytics">数据分析</option>
                                    <option value="education">教育</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label for="projectDescription" class="form-label">项目描述</label>
                        <textarea class="form-control" id="projectDescription" rows="3" required></textarea>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-4">
                            <div class="mb-3">
                                <label for="projectStatus" class="form-label">状态</label>
                                <select class="form-select" id="projectStatus" required>
                                    <option value="planning">计划中</option>
                                    <option value="active">进行中</option>
                                    <option value="on_hold">暂停</option>
                                    <option value="completed">已完成</option>
                                </select>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="mb-3">
                                <label for="projectPriority" class="form-label">优先级</label>
                                <select class="form-select" id="projectPriority" required>
                                    <option value="low">低</option>
                                    <option value="medium">中</option>
                                    <option value="high">高</option>
                                </select>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="mb-3">
                                <label for="projectBudget" class="form-label">预算</label>
                                <input type="number" class="form-control" id="projectBudget" required>
                            </div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="projectStartDate" class="form-label">开始日期</label>
                                <input type="date" class="form-control" id="projectStartDate" required>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="projectEndDate" class="form-label">结束日期</label>
                                <input type="date" class="form-control" id="projectEndDate" required>
                            </div>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label for="projectTags" class="form-label">标签（用逗号分隔）</label>
                        <input type="text" class="form-control" id="projectTags" 
                               placeholder="例如：Web应用,React,Node.js">
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                <button type="button" class="btn btn-primary" onclick="saveProject()">保存</button>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    function filterProjects() {
        const filterCard = document.getElementById('filterCard');
        filterCard.style.display = filterCard.style.display === 'none' ? 'block' : 'none';
    }
    
    function applyFilters() {
        const statusFilter = document.getElementById('statusFilter').value;
        const priorityFilter = document.getElementById('priorityFilter').value;
        const categoryFilter = document.getElementById('categoryFilter').value;
        
        const projectCards = document.querySelectorAll('.project-card');
        
        projectCards.forEach(card => {
            const status = card.dataset.status;
            const priority = card.dataset.priority;
            const category = card.dataset.category;
            
            const statusMatch = !statusFilter || status === statusFilter;
            const priorityMatch = !priorityFilter || priority === priorityFilter;
            const categoryMatch = !categoryFilter || category === categoryFilter;
            
            if (statusMatch && priorityMatch && categoryMatch) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
        
        showNotification('筛选已应用', 'success');
    }
    
    function viewProject(id) {
        window.location.href = `/projects/${id}`;
    }
    
    function editProject(id) {
        // 实现编辑项目逻辑
        showNotification('编辑功能开发中', 'info');
    }
    
    function deleteProject(id) {
        if (confirm('确定要删除这个项目吗？')) {
            // 实现删除项目逻辑
            showNotification('项目已删除', 'success');
        }
    }
    
    async function saveProject() {
        const formData = {
            name: document.getElementById('projectName').value,
            description: document.getElementById('projectDescription').value,
            category: document.getElementById('projectCategory').value,
            status: document.getElementById('projectStatus').value,
            priority: document.getElementById('projectPriority').value,
            budget: document.getElementById('projectBudget').value,
            start_date: document.getElementById('projectStartDate').value,
            end_date: document.getElementById('projectEndDate').value,
            tags: document.getElementById('projectTags').value.split(',').map(tag => tag.trim())
        };
        
        try {
            const response = await apiRequest('/api/projects', {
                method: 'POST',
                body: JSON.stringify(formData)
            });
            
            showNotification('项目创建成功', 'success');
            bootstrap.Modal.getInstance(document.getElementById('projectModal')).hide();
            location.reload();
        } catch (error) {
            showNotification('创建失败，请重试', 'danger');
        }
    }
</script>
{% endblock %}
"""