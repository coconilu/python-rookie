#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session19 示例4：Flask模板引擎进阶示例

本示例演示了Flask Jinja2模板引擎的高级功能，包括模板继承、
自定义过滤器、宏定义、上下文处理器等。

作者: Python教程团队
创建日期: 2024-12-24
"""

from flask import Flask, render_template_string, request, url_for, flash, redirect
from datetime import datetime, timedelta
import re
import hashlib
import random
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'flask-template-example-key'

# 模拟数据
projects = [
    {
        'id': 1,
        'name': 'Python Web开发',
        'description': '使用Flask构建现代Web应用',
        'status': 'active',
        'priority': 'high',
        'created_at': datetime.now() - timedelta(days=30),
        'updated_at': datetime.now() - timedelta(days=2),
        'tags': ['Python', 'Flask', 'Web开发'],
        'progress': 75,
        'team_members': ['张三', '李四', '王五']
    },
    {
        'id': 2,
        'name': '数据分析平台',
        'description': '基于Python的数据分析和可视化平台',
        'status': 'completed',
        'priority': 'medium',
        'created_at': datetime.now() - timedelta(days=60),
        'updated_at': datetime.now() - timedelta(days=1),
        'tags': ['Python', 'Pandas', '数据分析'],
        'progress': 100,
        'team_members': ['赵六', '钱七']
    },
    {
        'id': 3,
        'name': '移动应用后端',
        'description': 'RESTful API服务开发',
        'status': 'planning',
        'priority': 'low',
        'created_at': datetime.now() - timedelta(days=5),
        'updated_at': datetime.now(),
        'tags': ['API', 'REST', '移动开发'],
        'progress': 15,
        'team_members': ['孙八', '周九', '吴十', '郑十一']
    }
]

notifications = [
    {'type': 'success', 'message': '项目部署成功', 'time': datetime.now() - timedelta(minutes=5)},
    {'type': 'warning', 'message': '系统资源使用率较高', 'time': datetime.now() - timedelta(minutes=15)},
    {'type': 'info', 'message': '新用户注册', 'time': datetime.now() - timedelta(hours=1)},
    {'type': 'error', 'message': '数据库连接异常', 'time': datetime.now() - timedelta(hours=2)}
]

# 自定义过滤器
@app.template_filter('datetime_format')
def datetime_format(value, format='%Y-%m-%d %H:%M'):
    """
    格式化日期时间
    """
    if isinstance(value, datetime):
        return value.strftime(format)
    return value

@app.template_filter('time_ago')
def time_ago(value):
    """
    显示相对时间（多久之前）
    """
    if not isinstance(value, datetime):
        return value
    
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

@app.template_filter('truncate_words')
def truncate_words(text, length=50, suffix='...'):
    """
    截断文本到指定长度
    """
    if len(text) <= length:
        return text
    return text[:length].rstrip() + suffix

@app.template_filter('highlight_keywords')
def highlight_keywords(text, keywords):
    """
    高亮关键词
    """
    if not keywords:
        return text
    
    if isinstance(keywords, str):
        keywords = [keywords]
    
    for keyword in keywords:
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        text = pattern.sub(f'<mark>{keyword}</mark>', text)
    
    return text

@app.template_filter('status_badge')
def status_badge(status):
    """
    根据状态生成徽章HTML
    """
    status_map = {
        'active': {'class': 'badge-success', 'text': '进行中'},
        'completed': {'class': 'badge-primary', 'text': '已完成'},
        'planning': {'class': 'badge-warning', 'text': '计划中'},
        'paused': {'class': 'badge-secondary', 'text': '已暂停'},
        'cancelled': {'class': 'badge-danger', 'text': '已取消'}
    }
    
    badge_info = status_map.get(status, {'class': 'badge-light', 'text': status})
    return f'<span class="badge {badge_info["class"]}">{badge_info["text"]}</span>'

@app.template_filter('priority_icon')
def priority_icon(priority):
    """
    根据优先级生成图标
    """
    icons = {
        'high': '🔴',
        'medium': '🟡',
        'low': '🟢'
    }
    return icons.get(priority, '⚪')

@app.template_filter('progress_bar')
def progress_bar(progress, show_text=True):
    """
    生成进度条HTML
    """
    progress = max(0, min(100, progress))  # 确保在0-100范围内
    
    # 根据进度确定颜色
    if progress < 30:
        color_class = 'bg-danger'
    elif progress < 70:
        color_class = 'bg-warning'
    else:
        color_class = 'bg-success'
    
    html = f'''
    <div class="progress" style="height: 20px;">
        <div class="progress-bar {color_class}" 
             role="progressbar" 
             style="width: {progress}%" 
             aria-valuenow="{progress}" 
             aria-valuemin="0" 
             aria-valuemax="100">
    '''
    
    if show_text:
        html += f'{progress}%'
    
    html += '</div></div>'
    return html

@app.template_filter('avatar_url')
def avatar_url(name, size=40):
    """
    生成头像URL（使用Gravatar风格）
    """
    # 使用名字生成一个简单的头像
    hash_value = hashlib.md5(name.encode()).hexdigest()[:6]
    color = f"#{hash_value}"
    
    # 返回一个简单的SVG头像
    initial = name[0].upper() if name else '?'
    return f'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}"><rect width="{size}" height="{size}" fill="{color}"/><text x="50%" y="50%" text-anchor="middle" dy=".35em" fill="white" font-family="Arial" font-size="{size//2}">{initial}</text></svg>'

# 自定义全局函数
@app.template_global()
def get_project_stats():
    """
    获取项目统计信息
    """
    total = len(projects)
    active = len([p for p in projects if p['status'] == 'active'])
    completed = len([p for p in projects if p['status'] == 'completed'])
    planning = len([p for p in projects if p['status'] == 'planning'])
    
    return {
        'total': total,
        'active': active,
        'completed': completed,
        'planning': planning,
        'completion_rate': round((completed / total * 100) if total > 0 else 0, 1)
    }

@app.template_global()
def get_random_color():
    """
    获取随机颜色
    """
    colors = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark']
    return random.choice(colors)

@app.template_global()
def url_for_with_params(endpoint, **params):
    """
    带参数的URL生成
    """
    return url_for(endpoint, **params)

# 上下文处理器
@app.context_processor
def inject_global_vars():
    """
    注入全局模板变量
    """
    return {
        'app_name': 'Flask模板示例',
        'app_version': '1.0.0',
        'current_year': datetime.now().year,
        'current_time': datetime.now(),
        'notifications': notifications[:3],  # 只显示最新3条通知
        'user_name': '演示用户',
        'user_role': 'admin'
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
            --primary-color: #6366f1;
            --secondary-color: #8b5cf6;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --error-color: #ef4444;
            --info-color: #3b82f6;
        }
        
        body {
            background-color: #f8fafc;
            font-family: 'Microsoft YaHei', 'Segoe UI', system-ui, sans-serif;
        }
        
        .navbar-brand {
            font-weight: bold;
            color: var(--primary-color) !important;
        }
        
        .sidebar {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            min-height: calc(100vh - 56px);
            color: white;
        }
        
        .sidebar .nav-link {
            color: rgba(255, 255, 255, 0.8);
            transition: all 0.3s ease;
        }
        
        .sidebar .nav-link:hover,
        .sidebar .nav-link.active {
            color: white;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
        }
        
        .card {
            border: none;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        
        .card:hover {
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
            transform: translateY(-2px);
        }
        
        .badge {
            font-size: 0.75em;
        }
        
        .badge-success {
            background-color: var(--success-color);
        }
        
        .badge-warning {
            background-color: var(--warning-color);
        }
        
        .badge-danger {
            background-color: var(--error-color);
        }
        
        .badge-primary {
            background-color: var(--primary-color);
        }
        
        .badge-secondary {
            background-color: #6c757d;
        }
        
        .progress {
            background-color: #e9ecef;
        }
        
        .notification-item {
            border-left: 4px solid;
            padding: 0.75rem;
            margin-bottom: 0.5rem;
            border-radius: 0 4px 4px 0;
        }
        
        .notification-success {
            border-left-color: var(--success-color);
            background-color: #d1fae5;
        }
        
        .notification-warning {
            border-left-color: var(--warning-color);
            background-color: #fef3c7;
        }
        
        .notification-error {
            border-left-color: var(--error-color);
            background-color: #fee2e2;
        }
        
        .notification-info {
            border-left-color: var(--info-color);
            background-color: #dbeafe;
        }
        
        .avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
        }
        
        .team-avatars {
            display: flex;
            gap: -8px;
        }
        
        .team-avatars img {
            border: 2px solid white;
            margin-left: -8px;
        }
        
        .stats-card {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
        }
        
        .tag {
            display: inline-block;
            background-color: #e5e7eb;
            color: #374151;
            padding: 0.25rem 0.5rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            margin: 0.125rem;
        }
        
        mark {
            background-color: #fef08a;
            padding: 0.125rem 0.25rem;
            border-radius: 0.25rem;
        }
        
        {% block extra_css %}{% endblock %}
    </style>
</head>
<body>
    <!-- 导航栏 -->
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
        <div class="container-fluid">
            <a class="navbar-brand" href="{{ url_for('index') }}">
                <i class="fas fa-flask me-2"></i>{{ app_name }}
            </a>
            
            <div class="navbar-nav ms-auto">
                <!-- 通知下拉菜单 -->
                <div class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                        <i class="fas fa-bell"></i>
                        <span class="badge bg-danger rounded-pill">{{ notifications|length }}</span>
                    </a>
                    <ul class="dropdown-menu dropdown-menu-end" style="width: 300px;">
                        <li><h6 class="dropdown-header">最新通知</h6></li>
                        {% for notification in notifications %}
                        <li>
                            <div class="dropdown-item-text notification-item notification-{{ notification.type }}">
                                <div class="d-flex justify-content-between">
                                    <span>{{ notification.message }}</span>
                                    <small class="text-muted">{{ notification.time|time_ago }}</small>
                                </div>
                            </div>
                        </li>
                        {% endfor %}
                        <li><hr class="dropdown-divider"></li>
                        <li><a class="dropdown-item text-center" href="#">查看所有通知</a></li>
                    </ul>
                </div>
                
                <!-- 用户菜单 -->
                <div class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                        <img src="{{ user_name|avatar_url(32) }}" class="avatar me-2" alt="用户头像">
                        {{ user_name }}
                    </a>
                    <ul class="dropdown-menu dropdown-menu-end">
                        <li><a class="dropdown-item" href="#"><i class="fas fa-user me-2"></i>个人资料</a></li>
                        <li><a class="dropdown-item" href="#"><i class="fas fa-cog me-2"></i>设置</a></li>
                        <li><hr class="dropdown-divider"></li>
                        <li><a class="dropdown-item" href="#"><i class="fas fa-sign-out-alt me-2"></i>退出登录</a></li>
                    </ul>
                </div>
            </div>
        </div>
    </nav>
    
    <div class="container-fluid">
        <div class="row">
            <!-- 侧边栏 -->
            <div class="col-md-3 col-lg-2 px-0">
                <div class="sidebar p-3">
                    <ul class="nav nav-pills flex-column">
                        <li class="nav-item">
                            <a class="nav-link {{ 'active' if request.endpoint == 'index' }}" href="{{ url_for('index') }}">
                                <i class="fas fa-home me-2"></i>首页
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link {{ 'active' if request.endpoint == 'projects' }}" href="{{ url_for('projects') }}">
                                <i class="fas fa-project-diagram me-2"></i>项目管理
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link {{ 'active' if request.endpoint == 'templates' }}" href="{{ url_for('templates') }}">
                                <i class="fas fa-code me-2"></i>模板示例
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link {{ 'active' if request.endpoint == 'filters' }}" href="{{ url_for('filters') }}">
                                <i class="fas fa-filter me-2"></i>过滤器演示
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link {{ 'active' if request.endpoint == 'macros' }}" href="{{ url_for('macros') }}">
                                <i class="fas fa-puzzle-piece me-2"></i>宏定义
                            </a>
                        </li>
                    </ul>
                    
                    <hr class="my-3">
                    
                    <!-- 系统信息 -->
                    <div class="text-center">
                        <small class="text-light">
                            <div>版本: {{ app_version }}</div>
                            <div>时间: {{ current_time|datetime_format('%H:%M') }}</div>
                            <div>用户: {{ user_role|upper }}</div>
                        </small>
                    </div>
                </div>
            </div>
            
            <!-- 主内容区域 -->
            <div class="col-md-9 col-lg-10">
                <div class="p-4">
                    {% block content %}{% endblock %}
                </div>
            </div>
        </div>
    </div>
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
"""

# 宏定义模板
MACROS_TEMPLATE = """
{# 项目卡片宏 #}
{% macro project_card(project, show_details=True) %}
<div class="card mb-3">
    <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="card-title mb-0">
            {{ project.priority|priority_icon }} {{ project.name }}
        </h5>
        {{ project.status|status_badge|safe }}
    </div>
    <div class="card-body">
        <p class="card-text">{{ project.description|truncate_words(80) }}</p>
        
        {% if show_details %}
        <div class="row mb-3">
            <div class="col-md-6">
                <small class="text-muted">创建时间：</small><br>
                <span>{{ project.created_at|datetime_format }}</span>
            </div>
            <div class="col-md-6">
                <small class="text-muted">更新时间：</small><br>
                <span>{{ project.updated_at|time_ago }}</span>
            </div>
        </div>
        
        <div class="mb-3">
            <small class="text-muted">进度：</small>
            {{ project.progress|progress_bar|safe }}
        </div>
        
        <div class="mb-3">
            <small class="text-muted">标签：</small><br>
            {% for tag in project.tags %}
                <span class="tag">{{ tag }}</span>
            {% endfor %}
        </div>
        
        <div class="mb-3">
            <small class="text-muted">团队成员：</small><br>
            <div class="team-avatars">
                {% for member in project.team_members %}
                    <img src="{{ member|avatar_url(32) }}" 
                         class="avatar" 
                         title="{{ member }}" 
                         alt="{{ member }}">
                {% endfor %}
            </div>
        </div>
        {% endif %}
        
        <div class="d-flex justify-content-between align-items-center">
            <small class="text-muted">ID: {{ project.id }}</small>
            <div>
                <a href="{{ url_for('project_detail', project_id=project.id) }}" class="btn btn-sm btn-outline-primary">
                    <i class="fas fa-eye me-1"></i>查看详情
                </a>
                <a href="#" class="btn btn-sm btn-outline-secondary">
                    <i class="fas fa-edit me-1"></i>编辑
                </a>
            </div>
        </div>
    </div>
</div>
{% endmacro %}

{# 统计卡片宏 #}
{% macro stats_card(title, value, icon, color='primary', subtitle='') %}
<div class="card stats-card text-white mb-3" style="background: linear-gradient(135deg, var(--{{ color }}-color), var(--secondary-color));">
    <div class="card-body">
        <div class="d-flex justify-content-between align-items-center">
            <div>
                <h6 class="card-title text-uppercase mb-1">{{ title }}</h6>
                <h2 class="mb-0">{{ value }}</h2>
                {% if subtitle %}
                    <small class="opacity-75">{{ subtitle }}</small>
                {% endif %}
            </div>
            <div class="text-end">
                <i class="{{ icon }} fa-2x opacity-75"></i>
            </div>
        </div>
    </div>
</div>
{% endmacro %}

{# 表格宏 #}
{% macro data_table(headers, rows, table_class='table table-striped') %}
<div class="table-responsive">
    <table class="{{ table_class }}">
        <thead class="table-dark">
            <tr>
                {% for header in headers %}
                    <th>{{ header }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
            {% for row in rows %}
                <tr>
                    {% for cell in row %}
                        <td>{{ cell|safe }}</td>
                    {% endfor %}
                </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endmacro %}

{# 分页宏 #}
{% macro pagination(page, total_pages, endpoint) %}
{% if total_pages > 1 %}
<nav aria-label="分页导航">
    <ul class="pagination justify-content-center">
        <li class="page-item {{ 'disabled' if page <= 1 }}">
            <a class="page-link" href="{{ url_for(endpoint, page=page-1) if page > 1 else '#' }}">
                <i class="fas fa-chevron-left"></i>
            </a>
        </li>
        
        {% for p in range(1, total_pages + 1) %}
            {% if p == page %}
                <li class="page-item active">
                    <span class="page-link">{{ p }}</span>
                </li>
            {% elif p <= 3 or p >= total_pages - 2 or (p >= page - 1 and p <= page + 1) %}
                <li class="page-item">
                    <a class="page-link" href="{{ url_for(endpoint, page=p) }}">{{ p }}</a>
                </li>
            {% elif p == 4 or p == total_pages - 3 %}
                <li class="page-item disabled">
                    <span class="page-link">...</span>
                </li>
            {% endif %}
        {% endfor %}
        
        <li class="page-item {{ 'disabled' if page >= total_pages }}">
            <a class="page-link" href="{{ url_for(endpoint, page=page+1) if page < total_pages else '#' }}">
                <i class="fas fa-chevron-right"></i>
            </a>
        </li>
    </ul>
</nav>
{% endif %}
{% endmacro %}
"""

# 首页模板
INDEX_TEMPLATE = """
{% extends base_template %}
{% from macros_template import stats_card, project_card %}

{% block title %}首页 - {{ super() }}{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1 class="h3 mb-0">
        <i class="fas fa-home me-2 text-primary"></i>项目管理仪表板
    </h1>
    <div>
        <span class="badge bg-success">在线</span>
        <small class="text-muted ms-2">最后更新: {{ current_time|time_ago }}</small>
    </div>
</div>

<!-- 统计卡片 -->
<div class="row mb-4">
    {% set stats = get_project_stats() %}
    <div class="col-md-3">
        {{ stats_card('总项目数', stats.total, 'fas fa-project-diagram', 'primary') }}
    </div>
    <div class="col-md-3">
        {{ stats_card('进行中', stats.active, 'fas fa-play-circle', 'success') }}
    </div>
    <div class="col-md-3">
        {{ stats_card('已完成', stats.completed, 'fas fa-check-circle', 'info') }}
    </div>
    <div class="col-md-3">
        {{ stats_card('完成率', stats.completion_rate ~ '%', 'fas fa-chart-pie', 'warning') }}
    </div>
</div>

<!-- 最新项目 -->
<div class="row">
    <div class="col-lg-8">
        <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">
                    <i class="fas fa-clock me-2"></i>最新项目
                </h5>
                <a href="{{ url_for('projects') }}" class="btn btn-sm btn-outline-primary">
                    查看全部
                </a>
            </div>
            <div class="card-body">
                {% for project in projects[:2] %}
                    {{ project_card(project, show_details=False) }}
                {% endfor %}
            </div>
        </div>
    </div>
    
    <div class="col-lg-4">
        <!-- 快速操作 -->
        <div class="card mb-3">
            <div class="card-header">
                <h5 class="mb-0">
                    <i class="fas fa-bolt me-2"></i>快速操作
                </h5>
            </div>
            <div class="card-body">
                <div class="d-grid gap-2">
                    <a href="#" class="btn btn-primary">
                        <i class="fas fa-plus me-2"></i>新建项目
                    </a>
                    <a href="{{ url_for('templates') }}" class="btn btn-outline-secondary">
                        <i class="fas fa-code me-2"></i>模板示例
                    </a>
                    <a href="{{ url_for('filters') }}" class="btn btn-outline-info">
                        <i class="fas fa-filter me-2"></i>过滤器演示
                    </a>
                </div>
            </div>
        </div>
        
        <!-- 系统状态 -->
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">
                    <i class="fas fa-server me-2"></i>系统状态
                </h5>
            </div>
            <div class="card-body">
                <div class="mb-3">
                    <div class="d-flex justify-content-between">
                        <span>CPU使用率</span>
                        <span>65%</span>
                    </div>
                    {{ 65|progress_bar(False)|safe }}
                </div>
                <div class="mb-3">
                    <div class="d-flex justify-content-between">
                        <span>内存使用率</span>
                        <span>42%</span>
                    </div>
                    {{ 42|progress_bar(False)|safe }}
                </div>
                <div class="mb-3">
                    <div class="d-flex justify-content-between">
                        <span>磁盘使用率</span>
                        <span>78%</span>
                    </div>
                    {{ 78|progress_bar(False)|safe }}
                </div>
                <small class="text-muted">
                    <i class="fas fa-info-circle me-1"></i>
                    系统运行正常，所有服务可用
                </small>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

# 项目列表模板
PROJECTS_TEMPLATE = """
{% extends base_template %}
{% from macros_template import project_card, data_table %}

{% block title %}项目管理 - {{ super() }}{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1 class="h3 mb-0">
        <i class="fas fa-project-diagram me-2 text-primary"></i>项目管理
    </h1>
    <div>
        <button class="btn btn-primary">
            <i class="fas fa-plus me-2"></i>新建项目
        </button>
        <button class="btn btn-outline-secondary">
            <i class="fas fa-download me-2"></i>导出
        </button>
    </div>
</div>

<!-- 搜索和筛选 -->
<div class="card mb-4">
    <div class="card-body">
        <form class="row g-3">
            <div class="col-md-4">
                <label for="search" class="form-label">搜索项目</label>
                <input type="text" class="form-control" id="search" placeholder="输入项目名称或描述">
            </div>
            <div class="col-md-3">
                <label for="status" class="form-label">状态筛选</label>
                <select class="form-select" id="status">
                    <option value="">全部状态</option>
                    <option value="active">进行中</option>
                    <option value="completed">已完成</option>
                    <option value="planning">计划中</option>
                </select>
            </div>
            <div class="col-md-3">
                <label for="priority" class="form-label">优先级</label>
                <select class="form-select" id="priority">
                    <option value="">全部优先级</option>
                    <option value="high">高</option>
                    <option value="medium">中</option>
                    <option value="low">低</option>
                </select>
            </div>
            <div class="col-md-2">
                <label class="form-label">&nbsp;</label>
                <div class="d-grid">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-search"></i>
                    </button>
                </div>
            </div>
        </form>
    </div>
</div>

<!-- 项目列表 -->
<div class="row">
    {% for project in projects %}
        <div class="col-lg-6 mb-4">
            {{ project_card(project) }}
        </div>
    {% endfor %}
</div>

<!-- 表格视图 -->
<div class="card">
    <div class="card-header">
        <h5 class="mb-0">
            <i class="fas fa-table me-2"></i>表格视图
        </h5>
    </div>
    <div class="card-body">
        {% set headers = ['项目名称', '状态', '优先级', '进度', '团队', '更新时间', '操作'] %}
        {% set rows = [] %}
        {% for project in projects %}
            {% set row = [
                project.priority|priority_icon ~ ' ' ~ project.name,
                project.status|status_badge,
                project.priority|title,
                project.progress|progress_bar(False),
                project.team_members|length ~ ' 人',
                project.updated_at|time_ago,
                '<a href="' ~ url_for('project_detail', project_id=project.id) ~ '" class="btn btn-sm btn-outline-primary">查看</a>'
            ] %}
            {% set _ = rows.append(row) %}
        {% endfor %}
        {{ data_table(headers, rows) }}
    </div>
</div>
{% endblock %}
"""

# 过滤器演示模板
FILTERS_TEMPLATE = """
{% extends base_template %}

{% block title %}过滤器演示 - {{ super() }}{% endblock %}

{% block content %}
<div class="mb-4">
    <h1 class="h3 mb-3">
        <i class="fas fa-filter me-2 text-primary"></i>自定义过滤器演示
    </h1>
    <p class="text-muted">展示各种自定义Jinja2过滤器的使用效果</p>
</div>

<div class="row">
    <!-- 时间格式化过滤器 -->
    <div class="col-lg-6 mb-4">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">时间格式化过滤器</h5>
            </div>
            <div class="card-body">
                <h6>datetime_format 过滤器：</h6>
                <ul class="list-unstyled">
                    <li><strong>默认格式：</strong>{{ current_time|datetime_format }}</li>
                    <li><strong>日期格式：</strong>{{ current_time|datetime_format('%Y年%m月%d日') }}</li>
                    <li><strong>时间格式：</strong>{{ current_time|datetime_format('%H:%M:%S') }}</li>
                    <li><strong>完整格式：</strong>{{ current_time|datetime_format('%Y-%m-%d %H:%M:%S %A') }}</li>
                </ul>
                
                <h6 class="mt-3">time_ago 过滤器：</h6>
                <ul class="list-unstyled">
                    {% for project in projects %}
                        <li><strong>{{ project.name }}：</strong>{{ project.updated_at|time_ago }}</li>
                    {% endfor %}
                </ul>
            </div>
        </div>
    </div>
    
    <!-- 文本处理过滤器 -->
    <div class="col-lg-6 mb-4">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">文本处理过滤器</h5>
            </div>
            <div class="card-body">
                <h6>truncate_words 过滤器：</h6>
                {% set long_text = "这是一段很长的文本内容，用来演示文本截断过滤器的效果。它会在指定长度处截断文本并添加省略号。" %}
                <ul class="list-unstyled">
                    <li><strong>原文：</strong>{{ long_text }}</li>
                    <li><strong>截断20字符：</strong>{{ long_text|truncate_words(20) }}</li>
                    <li><strong>截断30字符：</strong>{{ long_text|truncate_words(30, '...') }}</li>
                </ul>
                
                <h6 class="mt-3">highlight_keywords 过滤器：</h6>
                {% set demo_text = "Flask是一个轻量级的Python Web框架，它简单易用且功能强大。" %}
                <ul class="list-unstyled">
                    <li><strong>原文：</strong>{{ demo_text }}</li>
                    <li><strong>高亮'Flask'：</strong>{{ demo_text|highlight_keywords('Flask')|safe }}</li>
                    <li><strong>高亮多个词：</strong>{{ demo_text|highlight_keywords(['Python', 'Web', '框架'])|safe }}</li>
                </ul>
            </div>
        </div>
    </div>
    
    <!-- 状态和进度过滤器 -->
    <div class="col-lg-6 mb-4">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">状态和进度过滤器</h5>
            </div>
            <div class="card-body">
                <h6>status_badge 过滤器：</h6>
                <div class="mb-3">
                    {{ 'active'|status_badge|safe }}
                    {{ 'completed'|status_badge|safe }}
                    {{ 'planning'|status_badge|safe }}
                    {{ 'paused'|status_badge|safe }}
                    {{ 'cancelled'|status_badge|safe }}
                </div>
                
                <h6>priority_icon 过滤器：</h6>
                <div class="mb-3">
                    <span>{{ 'high'|priority_icon }} 高优先级</span><br>
                    <span>{{ 'medium'|priority_icon }} 中优先级</span><br>
                    <span>{{ 'low'|priority_icon }} 低优先级</span>
                </div>
                
                <h6>progress_bar 过滤器：</h6>
                <div class="mb-2">25% 进度：{{ 25|progress_bar|safe }}</div>
                <div class="mb-2">60% 进度：{{ 60|progress_bar|safe }}</div>
                <div class="mb-2">90% 进度：{{ 90|progress_bar|safe }}</div>
                <div class="mb-2">无文字进度条：{{ 75|progress_bar(False)|safe }}</div>
            </div>
        </div>
    </div>
    
    <!-- 头像过滤器 -->
    <div class="col-lg-6 mb-4">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">头像过滤器</h5>
            </div>
            <div class="card-body">
                <h6>avatar_url 过滤器：</h6>
                <div class="d-flex align-items-center gap-3 mb-3">
                    {% for project in projects %}
                        {% for member in project.team_members[:3] %}
                            <div class="text-center">
                                <img src="{{ member|avatar_url(48) }}" class="rounded-circle mb-1" width="48" height="48" alt="{{ member }}">
                                <div><small>{{ member }}</small></div>
                            </div>
                        {% endfor %}
                    {% endfor %}
                </div>
                
                <h6>不同尺寸的头像：</h6>
                <div class="d-flex align-items-center gap-2">
                    <img src="{{ user_name|avatar_url(24) }}" class="rounded-circle" width="24" height="24" alt="小">
                    <img src="{{ user_name|avatar_url(32) }}" class="rounded-circle" width="32" height="32" alt="中">
                    <img src="{{ user_name|avatar_url(48) }}" class="rounded-circle" width="48" height="48" alt="大">
                    <img src="{{ user_name|avatar_url(64) }}" class="rounded-circle" width="64" height="64" alt="特大">
                </div>
            </div>
        </div>
    </div>
</div>

<!-- 过滤器代码示例 -->
<div class="card">
    <div class="card-header">
        <h5 class="mb-0">
            <i class="fas fa-code me-2"></i>过滤器实现代码
        </h5>
    </div>
    <div class="card-body">
        <div class="accordion" id="filterAccordion">
            <div class="accordion-item">
                <h2 class="accordion-header" id="timeFilters">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTime">
                        时间格式化过滤器代码
                    </button>
                </h2>
                <div id="collapseTime" class="accordion-collapse collapse" data-bs-parent="#filterAccordion">
                    <div class="accordion-body">
                        <pre><code>@app.template_filter('datetime_format')
def datetime_format(value, format='%Y-%m-%d %H:%M'):
    if isinstance(value, datetime):
        return value.strftime(format)
    return value

@app.template_filter('time_ago')
def time_ago(value):
    if not isinstance(value, datetime):
        return value
    
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
        return '刚刚'</code></pre>
                    </div>
                </div>
            </div>
            
            <div class="accordion-item">
                <h2 class="accordion-header" id="textFilters">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseText">
                        文本处理过滤器代码
                    </button>
                </h2>
                <div id="collapseText" class="accordion-collapse collapse" data-bs-parent="#filterAccordion">
                    <div class="accordion-body">
                        <pre><code>@app.template_filter('truncate_words')
def truncate_words(text, length=50, suffix='...'):
    if len(text) <= length:
        return text
    return text[:length].rstrip() + suffix

@app.template_filter('highlight_keywords')
def highlight_keywords(text, keywords):
    if not keywords:
        return text
    
    if isinstance(keywords, str):
        keywords = [keywords]
    
    for keyword in keywords:
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        text = pattern.sub(f'&lt;mark&gt;{keyword}&lt;/mark&gt;', text)
    
    return text</code></pre>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

# 路由定义
@app.route('/')
def index():
    """
    首页
    """
    return render_template_string(
        INDEX_TEMPLATE,
        base_template=BASE_TEMPLATE,
        macros_template=MACROS_TEMPLATE,
        projects=projects
    )

@app.route('/projects')
def projects():
    """
    项目列表页
    """
    return render_template_string(
        PROJECTS_TEMPLATE,
        base_template=BASE_TEMPLATE,
        macros_template=MACROS_TEMPLATE,
        projects=projects
    )

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    """
    项目详情页
    """
    project = next((p for p in projects if p['id'] == project_id), None)
    if not project:
        flash('项目不存在', 'error')
        return redirect(url_for('projects'))
    
    # 简单的项目详情模板
    detail_template = """
    {% extends base_template %}
    {% from macros_template import project_card %}
    
    {% block title %}{{ project.name }} - 项目详情 - {{ super() }}{% endblock %}
    
    {% block content %}
    <div class="mb-4">
        <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><a href="{{ url_for('index') }}">首页</a></li>
                <li class="breadcrumb-item"><a href="{{ url_for('projects') }}">项目管理</a></li>
                <li class="breadcrumb-item active">{{ project.name }}</li>
            </ol>
        </nav>
        
        <div class="d-flex justify-content-between align-items-center">
            <h1 class="h3 mb-0">
                {{ project.priority|priority_icon }} {{ project.name }}
            </h1>
            <div>
                <button class="btn btn-primary">
                    <i class="fas fa-edit me-2"></i>编辑项目
                </button>
                <button class="btn btn-outline-danger">
                    <i class="fas fa-trash me-2"></i>删除
                </button>
            </div>
        </div>
    </div>
    
    <div class="row">
        <div class="col-lg-8">
            {{ project_card(project) }}
            
            <!-- 项目活动 -->
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">
                        <i class="fas fa-history me-2"></i>项目活动
                    </h5>
                </div>
                <div class="card-body">
                    <div class="timeline">
                        <div class="d-flex mb-3">
                            <div class="flex-shrink-0">
                                <img src="{{ '张三'|avatar_url(32) }}" class="rounded-circle" width="32" height="32">
                            </div>
                            <div class="flex-grow-1 ms-3">
                                <div class="d-flex justify-content-between">
                                    <h6 class="mb-1">张三更新了项目进度</h6>
                                    <small class="text-muted">{{ project.updated_at|time_ago }}</small>
                                </div>
                                <p class="mb-0 text-muted">项目进度从70%更新到{{ project.progress }}%</p>
                            </div>
                        </div>
                        
                        <div class="d-flex mb-3">
                            <div class="flex-shrink-0">
                                <img src="{{ '李四'|avatar_url(32) }}" class="rounded-circle" width="32" height="32">
                            </div>
                            <div class="flex-grow-1 ms-3">
                                <div class="d-flex justify-content-between">
                                    <h6 class="mb-1">李四添加了新的标签</h6>
                                    <small class="text-muted">{{ (project.updated_at - timedelta(hours=2))|time_ago }}</small>
                                </div>
                                <p class="mb-0 text-muted">添加了标签: 
                                    {% for tag in project.tags[-2:] %}
                                        <span class="tag">{{ tag }}</span>
                                    {% endfor %}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-lg-4">
            <!-- 项目统计 -->
            <div class="card mb-3">
                <div class="card-header">
                    <h5 class="mb-0">
                        <i class="fas fa-chart-bar me-2"></i>项目统计
                    </h5>
                </div>
                <div class="card-body">
                    <div class="row text-center">
                        <div class="col-6">
                            <h4 class="text-primary">{{ project.team_members|length }}</h4>
                            <small class="text-muted">团队成员</small>
                        </div>
                        <div class="col-6">
                            <h4 class="text-success">{{ project.tags|length }}</h4>
                            <small class="text-muted">技术标签</small>
                        </div>
                    </div>
                    <hr>
                    <div class="row text-center">
                        <div class="col-6">
                            <h4 class="text-info">{{ ((project.updated_at - project.created_at).days) }}</h4>
                            <small class="text-muted">项目天数</small>
                        </div>
                        <div class="col-6">
                            <h4 class="text-warning">{{ project.progress }}%</h4>
                            <small class="text-muted">完成进度</small>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 相关项目 -->
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">
                        <i class="fas fa-link me-2"></i>相关项目
                    </h5>
                </div>
                <div class="card-body">
                    {% for related_project in projects %}
                        {% if related_project.id != project.id %}
                            <div class="d-flex align-items-center mb-2">
                                <div class="flex-shrink-0">
                                    {{ related_project.priority|priority_icon }}
                                </div>
                                <div class="flex-grow-1 ms-2">
                                    <a href="{{ url_for('project_detail', project_id=related_project.id) }}" class="text-decoration-none">
                                        {{ related_project.name|truncate_words(20) }}
                                    </a>
                                    <br>
                                    <small class="text-muted">{{ related_project.status|status_badge|safe }}</small>
                                </div>
                            </div>
                        {% endif %}
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
    {% endblock %}
    """
    
    return render_template_string(
        detail_template,
        base_template=BASE_TEMPLATE,
        macros_template=MACROS_TEMPLATE,
        project=project,
        timedelta=timedelta
    )

@app.route('/templates')
def templates():
    """
    模板示例页
    """
    template_examples = [
        {
            'name': '模板继承',
            'description': '使用extends和block实现模板继承',
            'code': '{% extends "base.html" %}\n{% block content %}...{% endblock %}'
        },
        {
            'name': '宏定义',
            'description': '使用macro定义可重用的模板片段',
            'code': '{% macro button(text, type="primary") %}\n<button class="btn btn-{{ type }}">{{ text }}</button>\n{% endmacro %}'
        },
        {
            'name': '包含模板',
            'description': '使用include包含其他模板文件',
            'code': '{% include "sidebar.html" %}'
        },
        {
            'name': '条件语句',
            'description': '使用if语句进行条件判断',
            'code': '{% if user.is_authenticated %}\n欢迎，{{ user.name }}！\n{% else %}\n请登录\n{% endif %}'
        }
    ]
    
    templates_template = """
    {% extends base_template %}
    
    {% block title %}模板示例 - {{ super() }}{% endblock %}
    
    {% block content %}
    <div class="mb-4">
        <h1 class="h3 mb-3">
            <i class="fas fa-code me-2 text-primary"></i>Jinja2模板示例
        </h1>
        <p class="text-muted">展示Flask Jinja2模板引擎的各种功能和用法</p>
    </div>
    
    <div class="row">
        {% for example in examples %}
            <div class="col-lg-6 mb-4">
                <div class="card h-100">
                    <div class="card-header">
                        <h5 class="mb-0">{{ example.name }}</h5>
                    </div>
                    <div class="card-body">
                        <p class="card-text">{{ example.description }}</p>
                        <pre class="bg-light p-3 rounded"><code>{{ example.code }}</code></pre>
                    </div>
                </div>
            </div>
        {% endfor %}
    </div>
    
    <!-- 实际模板结构展示 -->
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">
                <i class="fas fa-sitemap me-2"></i>当前页面模板结构
            </h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-4">
                    <h6>基础模板 (base.html)</h6>
                    <ul class="list-unstyled">
                        <li><i class="fas fa-file-code text-primary"></i> HTML结构</li>
                        <li><i class="fas fa-palette text-success"></i> CSS样式</li>
                        <li><i class="fas fa-cogs text-info"></i> JavaScript交互</li>
                        <li><i class="fas fa-database text-warning"></i> 数据绑定</li>
                    </ul>
                </div>
                <div class="col-md-4">
                    <h6>页面模板 (templates.html)</h6>
                    <ul class="list-unstyled">
                        <li><i class="fas fa-expand-arrows-alt text-primary"></i> 继承基础模板</li>
                        <li><i class="fas fa-puzzle-piece text-success"></i> 使用宏定义</li>
                        <li><i class="fas fa-filter text-info"></i> 应用过滤器</li>
                        <li><i class="fas fa-code-branch text-warning"></i> 条件和循环</li>
                    </ul>
                </div>
                <div class="col-md-4">
                    <h6>组件 (macros.html)</h6>
                    <ul class="list-unstyled">
                        <li><i class="fas fa-th-large text-primary"></i> 项目卡片宏</li>
                        <li><i class="fas fa-chart-bar text-success"></i> 统计卡片宏</li>
                        <li><i class="fas fa-table text-info"></i> 数据表格宏</li>
                        <li><i class="fas fa-ellipsis-h text-warning"></i> 分页宏</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}
    """
    
    return render_template_string(
        templates_template,
        base_template=BASE_TEMPLATE,
        examples=template_examples
    )

@app.route('/filters')
def filters():
    """
    过滤器演示页
    """
    return render_template_string(
        FILTERS_TEMPLATE,
        base_template=BASE_TEMPLATE,
        projects=projects
    )

@app.route('/macros')
def macros():
    """
    宏定义演示页
    """
    macros_demo_template = """
    {% extends base_template %}
    {% from macros_template import stats_card, project_card, data_table, pagination %}
    
    {% block title %}宏定义演示 - {{ super() }}{% endblock %}
    
    {% block content %}
    <div class="mb-4">
        <h1 class="h3 mb-3">
            <i class="fas fa-puzzle-piece me-2 text-primary"></i>Jinja2宏定义演示
        </h1>
        <p class="text-muted">展示如何使用宏(macro)创建可重用的模板组件</p>
    </div>
    
    <!-- 统计卡片宏演示 -->
    <div class="mb-4">
        <h4>统计卡片宏 (stats_card)</h4>
        <div class="row">
            <div class="col-md-3">
                {{ stats_card('用户总数', '1,234', 'fas fa-users', 'primary', '较上月增长12%') }}
            </div>
            <div class="col-md-3">
                {{ stats_card('订单数量', '856', 'fas fa-shopping-cart', 'success', '今日新增23个') }}
            </div>
            <div class="col-md-3">
                {{ stats_card('收入', '¥45,678', 'fas fa-dollar-sign', 'info', '本月目标完成78%') }}
            </div>
            <div class="col-md-3">
                {{ stats_card('转化率', '3.2%', 'fas fa-chart-line', 'warning', '优化中') }}
            </div>
        </div>
    </div>
    
    <!-- 项目卡片宏演示 -->
    <div class="mb-4">
        <h4>项目卡片宏 (project_card)</h4>
        <div class="row">
            {% for project in projects[:2] %}
                <div class="col-lg-6">
                    {{ project_card(project) }}
                </div>
            {% endfor %}
        </div>
    </div>
    
    <!-- 数据表格宏演示 -->
    <div class="mb-4">
        <h4>数据表格宏 (data_table)</h4>
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">用户列表</h5>
            </div>
            <div class="card-body">
                {% set user_headers = ['用户名', '邮箱', '角色', '注册时间', '状态'] %}
                {% set user_rows = [
                    ['张三', 'zhangsan@example.com', '管理员', '2024-01-15', '<span class="badge bg-success">活跃</span>'],
                    ['李四', 'lisi@example.com', '编辑', '2024-02-20', '<span class="badge bg-success">活跃</span>'],
                    ['王五', 'wangwu@example.com', '用户', '2024-03-10', '<span class="badge bg-warning">待激活</span>'],
                    ['赵六', 'zhaoliu@example.com', '用户', '2024-03-25', '<span class="badge bg-danger">已禁用</span>']
                ] %}
                {{ data_table(user_headers, user_rows, 'table table-hover') }}
            </div>
        </div>
    </div>
    
    <!-- 分页宏演示 -->
    <div class="mb-4">
        <h4>分页宏 (pagination)</h4>
        <div class="card">
            <div class="card-body text-center">
                <p>当前页: 5，总页数: 12</p>
                {{ pagination(5, 12, 'macros') }}
            </div>
        </div>
    </div>
    
    <!-- 宏定义代码展示 -->
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">
                <i class="fas fa-code me-2"></i>宏定义源代码
            </h5>
        </div>
        <div class="card-body">
            <div class="accordion" id="macroAccordion">
                <div class="accordion-item">
                    <h2 class="accordion-header">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseStatsCard">
                            统计卡片宏 (stats_card)
                        </button>
                    </h2>
                    <div id="collapseStatsCard" class="accordion-collapse collapse" data-bs-parent="#macroAccordion">
                        <div class="accordion-body">
                            <pre><code>{% raw %}{% macro stats_card(title, value, icon, color='primary', subtitle='') %}
<div class="card stats-card text-white mb-3" style="background: linear-gradient(135deg, var(--{{ color }}-color), var(--secondary-color));">
    <div class="card-body">
        <div class="d-flex justify-content-between align-items-center">
            <div>
                <h6 class="card-title text-uppercase mb-1">{{ title }}</h6>
                <h2 class="mb-0">{{ value }}</h2>
                {% if subtitle %}
                    <small class="opacity-75">{{ subtitle }}</small>
                {% endif %}
            </div>
            <div class="text-end">
                <i class="{{ icon }} fa-2x opacity-75"></i>
            </div>
        </div>
    </div>
</div>
{% endmacro %}{% endraw %}</code></pre>
                        </div>
                    </div>
                </div>
                
                <div class="accordion-item">
                    <h2 class="accordion-header">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseProjectCard">
                            项目卡片宏 (project_card)
                        </button>
                    </h2>
                    <div id="collapseProjectCard" class="accordion-collapse collapse" data-bs-parent="#macroAccordion">
                        <div class="accordion-body">
                            <pre><code>{% raw %}{% macro project_card(project, show_details=True) %}
<div class="card mb-3">
    <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="card-title mb-0">
            {{ project.priority|priority_icon }} {{ project.name }}
        </h5>
        {{ project.status|status_badge|safe }}
    </div>
    <div class="card-body">
        <p class="card-text">{{ project.description|truncate_words(80) }}</p>
        <!-- 更多内容... -->
    </div>
</div>
{% endmacro %}{% endraw %}</code></pre>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}
    """
    
    return render_template_string(
        macros_demo_template,
        base_template=BASE_TEMPLATE,
        macros_template=MACROS_TEMPLATE,
        projects=projects
    )

if __name__ == '__main__':
    print("Flask模板引擎进阶示例")
    print("=" * 50)
    print("本示例演示了以下功能:")
    print("1. 模板继承 (extends/block)")
    print("2. 自定义过滤器 (template_filter)")
    print("3. 全局函数 (template_global)")
    print("4. 上下文处理器 (context_processor)")
    print("5. 宏定义 (macro)")
    print("6. 模板包含 (include)")
    print("7. 条件和循环语句")
    print("8. 变量和表达式")
    print("\n访问以下URL查看不同功能:")
    print("- http://localhost:5000/ (首页)")
    print("- http://localhost:5000/projects (项目管理)")
    print("- http://localhost:5000/templates (模板示例)")
    print("- http://localhost:5000/filters (过滤器演示)")
    print("- http://localhost:5000/macros (宏定义演示)")
    print("\n启动服务器...")
    
    app.run(debug=True, host='0.0.0.0', port=5000)