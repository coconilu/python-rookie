# Session19: 前端集成 - 详细教程

## 课程概述

在前面的课程中，我们学习了Flask框架的基础知识和数据库集成。本课程将深入学习前端技术，包括HTML、CSS和JavaScript，以及如何在Flask应用中集成这些技术来创建动态、交互式的Web应用。

## 1. HTML基础回顾与进阶

### 1.1 HTML5语义化标签

HTML5引入了许多语义化标签，让页面结构更清晰：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>待办事项管理器</title>
</head>
<body>
    <header>
        <h1>我的待办事项</h1>
        <nav>
            <ul>
                <li><a href="#all">全部</a></li>
                <li><a href="#active">未完成</a></li>
                <li><a href="#completed">已完成</a></li>
            </ul>
        </nav>
    </header>
    
    <main>
        <section id="todo-input">
            <form id="todo-form">
                <input type="text" id="todo-text" placeholder="添加新任务..." required>
                <button type="submit">添加</button>
            </form>
        </section>
        
        <section id="todo-list">
            <article class="todo-item">
                <input type="checkbox" class="todo-checkbox">
                <span class="todo-content">示例任务</span>
                <button class="edit-btn">编辑</button>
                <button class="delete-btn">删除</button>
            </article>
        </section>
    </main>
    
    <footer>
        <p>&copy; 2024 待办事项管理器</p>
    </footer>
</body>
</html>
```

### 1.2 表单元素和验证

```html
<form id="todo-form" novalidate>
    <div class="form-group">
        <label for="todo-text">任务内容</label>
        <input type="text" 
               id="todo-text" 
               name="content"
               placeholder="请输入任务内容..." 
               required 
               minlength="1" 
               maxlength="200">
        <span class="error-message"></span>
    </div>
    
    <div class="form-group">
        <label for="todo-priority">优先级</label>
        <select id="todo-priority" name="priority">
            <option value="low">低</option>
            <option value="medium" selected>中</option>
            <option value="high">高</option>
        </select>
    </div>
    
    <div class="form-group">
        <label for="todo-deadline">截止日期</label>
        <input type="date" id="todo-deadline" name="deadline">
    </div>
    
    <button type="submit">添加任务</button>
</form>
```

## 2. CSS样式设计

### 2.1 现代CSS布局

```css
/* 基础样式重置 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f4f4f4;
}

/* 容器布局 */
.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

/* Flexbox布局 */
header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
}

nav ul {
    display: flex;
    list-style: none;
    gap: 1rem;
}

nav a {
    color: white;
    text-decoration: none;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    transition: background-color 0.3s ease;
}

nav a:hover {
    background-color: rgba(255, 255, 255, 0.2);
}

/* Grid布局 */
.todo-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem;
    margin-top: 2rem;
}

/* 卡片样式 */
.todo-item {
    background: white;
    border-radius: 10px;
    padding: 1.5rem;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.todo-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

/* 表单样式 */
.form-group {
    margin-bottom: 1rem;
}

label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: #555;
}

input, select, textarea {
    width: 100%;
    padding: 0.75rem;
    border: 2px solid #ddd;
    border-radius: 5px;
    font-size: 1rem;
    transition: border-color 0.3s ease;
}

input:focus, select:focus, textarea:focus {
    outline: none;
    border-color: #667eea;
}

/* 按钮样式 */
.btn {
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.3s ease;
}

.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.btn-primary:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.btn-danger {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
    color: white;
}

.btn-success {
    background: linear-gradient(135deg, #51cf66 0%, #40c057 100%);
    color: white;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .container {
        padding: 10px;
    }
    
    header {
        flex-direction: column;
        text-align: center;
    }
    
    nav ul {
        margin-top: 1rem;
    }
    
    .todo-grid {
        grid-template-columns: 1fr;
    }
}

/* 动画效果 */
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

.fade-in {
    animation: fadeIn 0.5s ease-out;
}

/* 状态样式 */
.todo-completed {
    opacity: 0.6;
    text-decoration: line-through;
}

.priority-high {
    border-left: 4px solid #ff6b6b;
}

.priority-medium {
    border-left: 4px solid #ffd43b;
}

.priority-low {
    border-left: 4px solid #51cf66;
}
```

### 2.2 CSS变量和主题切换

```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --success-color: #51cf66;
    --danger-color: #ff6b6b;
    --warning-color: #ffd43b;
    --background-color: #f4f4f4;
    --text-color: #333;
    --card-background: #ffffff;
    --border-color: #ddd;
}

[data-theme="dark"] {
    --background-color: #1a1a1a;
    --text-color: #ffffff;
    --card-background: #2d2d2d;
    --border-color: #444;
}

body {
    background-color: var(--background-color);
    color: var(--text-color);
    transition: background-color 0.3s ease, color 0.3s ease;
}

.todo-item {
    background: var(--card-background);
    border: 1px solid var(--border-color);
}
```

## 3. JavaScript基础与DOM操作

### 3.1 现代JavaScript语法

```javascript
// ES6+ 语法
class TodoManager {
    constructor() {
        this.todos = [];
        this.currentFilter = 'all';
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadTodos();
        this.render();
    }
    
    // 事件绑定
    bindEvents() {
        const form = document.getElementById('todo-form');
        const filterBtns = document.querySelectorAll('.filter-btn');
        
        form.addEventListener('submit', (e) => this.handleSubmit(e));
        
        filterBtns.forEach(btn => {
            btn.addEventListener('click', (e) => this.handleFilter(e));
        });
        
        // 事件委托处理动态元素
        document.getElementById('todo-list').addEventListener('click', (e) => {
            if (e.target.classList.contains('delete-btn')) {
                this.deleteTodo(e.target.dataset.id);
            } else if (e.target.classList.contains('edit-btn')) {
                this.editTodo(e.target.dataset.id);
            } else if (e.target.classList.contains('todo-checkbox')) {
                this.toggleTodo(e.target.dataset.id);
            }
        });
    }
    
    // 添加新任务
    async handleSubmit(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const todoData = {
            content: formData.get('content'),
            priority: formData.get('priority'),
            deadline: formData.get('deadline')
        };
        
        try {
            const response = await this.apiCall('/api/todos', 'POST', todoData);
            if (response.success) {
                this.todos.push(response.todo);
                this.render();
                e.target.reset();
                this.showMessage('任务添加成功！', 'success');
            }
        } catch (error) {
            this.showMessage('添加失败，请重试', 'error');
        }
    }
    
    // API调用封装
    async apiCall(url, method = 'GET', data = null) {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(url, options);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    }
    
    // 渲染待办事项列表
    render() {
        const container = document.getElementById('todo-list');
        const filteredTodos = this.getFilteredTodos();
        
        container.innerHTML = '';
        
        if (filteredTodos.length === 0) {
            container.innerHTML = '<p class="empty-message">暂无任务</p>';
            return;
        }
        
        filteredTodos.forEach(todo => {
            const todoElement = this.createTodoElement(todo);
            container.appendChild(todoElement);
        });
        
        this.updateStats();
    }
    
    // 创建待办事项元素
    createTodoElement(todo) {
        const article = document.createElement('article');
        article.className = `todo-item priority-${todo.priority} ${todo.completed ? 'todo-completed' : ''}`;
        article.innerHTML = `
            <div class="todo-header">
                <input type="checkbox" 
                       class="todo-checkbox" 
                       data-id="${todo.id}"
                       ${todo.completed ? 'checked' : ''}>
                <span class="todo-content" data-id="${todo.id}">${this.escapeHtml(todo.content)}</span>
                <div class="todo-actions">
                    <button class="btn btn-sm edit-btn" data-id="${todo.id}">编辑</button>
                    <button class="btn btn-sm btn-danger delete-btn" data-id="${todo.id}">删除</button>
                </div>
            </div>
            ${todo.deadline ? `<div class="todo-deadline">截止：${this.formatDate(todo.deadline)}</div>` : ''}
            <div class="todo-meta">
                <span class="priority-badge priority-${todo.priority}">${this.getPriorityText(todo.priority)}</span>
                <span class="todo-date">创建于 ${this.formatDate(todo.created_at)}</span>
            </div>
        `;
        
        // 添加动画效果
        article.classList.add('fade-in');
        
        return article;
    }
    
    // 工具函数
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('zh-CN');
    }
    
    getPriorityText(priority) {
        const priorityMap = {
            'high': '高优先级',
            'medium': '中优先级',
            'low': '低优先级'
        };
        return priorityMap[priority] || '未知';
    }
    
    // 显示消息提示
    showMessage(message, type = 'info') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message message-${type}`;
        messageDiv.textContent = message;
        
        document.body.appendChild(messageDiv);
        
        // 自动消失
        setTimeout(() => {
            messageDiv.remove();
        }, 3000);
    }
}

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    new TodoManager();
});
```

### 3.2 AJAX与异步编程

```javascript
// 使用 async/await 处理异步操作
class ApiService {
    constructor(baseUrl = '/api') {
        this.baseUrl = baseUrl;
    }
    
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            ...options
        };
        
        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            }
            
            return await response.text();
        } catch (error) {
            console.error('API请求失败:', error);
            throw error;
        }
    }
    
    // GET请求
    async get(endpoint) {
        return this.request(endpoint);
    }
    
    // POST请求
    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
    
    // PUT请求
    async put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }
    
    // DELETE请求
    async delete(endpoint) {
        return this.request(endpoint, {
            method: 'DELETE'
        });
    }
}

// 使用示例
const api = new ApiService();

// 获取所有待办事项
async function loadTodos() {
    try {
        const todos = await api.get('/todos');
        renderTodos(todos);
    } catch (error) {
        showError('加载待办事项失败');
    }
}

// 添加新待办事项
async function addTodo(todoData) {
    try {
        const newTodo = await api.post('/todos', todoData);
        appendTodo(newTodo);
        showSuccess('添加成功');
    } catch (error) {
        showError('添加失败');
    }
}
```

## 4. Flask模板引擎进阶

### 4.1 Jinja2模板继承

**base.html** (基础模板):
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}待办事项管理器{% endblock %}</title>
    
    <!-- CSS文件 -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    {% block extra_css %}{% endblock %}
</head>
<body data-theme="{{ session.get('theme', 'light') }}">
    <div class="container">
        <header>
            <h1>{% block header %}待办事项管理器{% endblock %}</h1>
            <nav>
                <ul>
                    <li><a href="{{ url_for('index') }}">首页</a></li>
                    <li><a href="{{ url_for('todos') }}">待办事项</a></li>
                    <li><a href="{{ url_for('settings') }}">设置</a></li>
                </ul>
            </nav>
        </header>
        
        <!-- 消息闪现 -->
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <div class="messages">
                    {% for category, message in messages %}
                        <div class="message message-{{ category }}">
                            {{ message }}
                            <button class="close-btn">&times;</button>
                        </div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}
        
        <main>
            {% block content %}{% endblock %}
        </main>
        
        <footer>
            <p>&copy; 2024 待办事项管理器</p>
        </footer>
    </div>
    
    <!-- JavaScript文件 -->
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

**todos.html** (待办事项页面):
```html
{% extends "base.html" %}

{% block title %}待办事项 - {{ super() }}{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/todos.css') }}">
{% endblock %}

{% block content %}
<div class="todo-container">
    <!-- 添加任务表单 -->
    <section class="todo-form-section">
        <h2>添加新任务</h2>
        <form id="todo-form" method="POST" action="{{ url_for('add_todo') }}">
            {{ form.hidden_tag() }}
            
            <div class="form-group">
                {{ form.content.label(class="form-label") }}
                {{ form.content(class="form-control", placeholder="请输入任务内容...") }}
                {% if form.content.errors %}
                    <div class="error-messages">
                        {% for error in form.content.errors %}
                            <span class="error-message">{{ error }}</span>
                        {% endfor %}
                    </div>
                {% endif %}
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    {{ form.priority.label(class="form-label") }}
                    {{ form.priority(class="form-control") }}
                </div>
                
                <div class="form-group">
                    {{ form.deadline.label(class="form-label") }}
                    {{ form.deadline(class="form-control") }}
                </div>
            </div>
            
            <button type="submit" class="btn btn-primary">添加任务</button>
        </form>
    </section>
    
    <!-- 过滤器 -->
    <section class="filter-section">
        <div class="filter-buttons">
            <button class="filter-btn {{ 'active' if filter_type == 'all' else '' }}" 
                    data-filter="all">全部 ({{ stats.total }})</button>
            <button class="filter-btn {{ 'active' if filter_type == 'active' else '' }}" 
                    data-filter="active">未完成 ({{ stats.active }})</button>
            <button class="filter-btn {{ 'active' if filter_type == 'completed' else '' }}" 
                    data-filter="completed">已完成 ({{ stats.completed }})</button>
        </div>
    </section>
    
    <!-- 待办事项列表 -->
    <section class="todo-list-section">
        <div id="todo-list" class="todo-grid">
            {% if todos %}
                {% for todo in todos %}
                    <article class="todo-item priority-{{ todo.priority }} {{ 'todo-completed' if todo.completed else '' }}" 
                             data-id="{{ todo.id }}">
                        <div class="todo-header">
                            <input type="checkbox" 
                                   class="todo-checkbox" 
                                   data-id="{{ todo.id }}"
                                   {{ 'checked' if todo.completed else '' }}>
                            <span class="todo-content">{{ todo.content }}</span>
                            <div class="todo-actions">
                                <button class="btn btn-sm edit-btn" data-id="{{ todo.id }}">编辑</button>
                                <button class="btn btn-sm btn-danger delete-btn" data-id="{{ todo.id }}">删除</button>
                            </div>
                        </div>
                        
                        {% if todo.deadline %}
                            <div class="todo-deadline">
                                截止：{{ todo.deadline.strftime('%Y-%m-%d') }}
                                {% if todo.deadline < moment().date() and not todo.completed %}
                                    <span class="overdue">已逾期</span>
                                {% endif %}
                            </div>
                        {% endif %}
                        
                        <div class="todo-meta">
                            <span class="priority-badge priority-{{ todo.priority }}">
                                {{ {'high': '高优先级', 'medium': '中优先级', 'low': '低优先级'}[todo.priority] }}
                            </span>
                            <span class="todo-date">{{ todo.created_at.strftime('%m-%d %H:%M') }}</span>
                        </div>
                    </article>
                {% endfor %}
            {% else %}
                <div class="empty-state">
                    <p>暂无待办事项</p>
                    <p>点击上方"添加任务"开始使用吧！</p>
                </div>
            {% endif %}
        </div>
    </section>
</div>

<!-- 编辑模态框 -->
<div id="edit-modal" class="modal">
    <div class="modal-content">
        <div class="modal-header">
            <h3>编辑任务</h3>
            <button class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
            <form id="edit-form">
                <input type="hidden" id="edit-todo-id">
                <div class="form-group">
                    <label for="edit-content">任务内容</label>
                    <input type="text" id="edit-content" class="form-control" required>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="edit-priority">优先级</label>
                        <select id="edit-priority" class="form-control">
                            <option value="low">低优先级</option>
                            <option value="medium">中优先级</option>
                            <option value="high">高优先级</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="edit-deadline">截止日期</label>
                        <input type="date" id="edit-deadline" class="form-control">
                    </div>
                </div>
                <div class="modal-actions">
                    <button type="button" class="btn btn-secondary cancel-btn">取消</button>
                    <button type="submit" class="btn btn-primary">保存</button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="{{ url_for('static', filename='js/todos.js') }}"></script>
{% endblock %}
```

### 4.2 自定义过滤器和函数

```python
# app.py 中添加自定义过滤器
from datetime import datetime
import pytz

@app.template_filter('datetime_format')
def datetime_format(value, format='%Y-%m-%d %H:%M'):
    """格式化日期时间"""
    if value is None:
        return ''
    return value.strftime(format)

@app.template_filter('time_ago')
def time_ago(value):
    """显示相对时间"""
    if value is None:
        return ''
    
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

@app.template_global()
def get_todo_stats(todos):
    """获取待办事项统计信息"""
    total = len(todos)
    completed = len([t for t in todos if t.completed])
    active = total - completed
    
    return {
        'total': total,
        'completed': completed,
        'active': active,
        'completion_rate': round(completed / total * 100, 1) if total > 0 else 0
    }
```

## 5. 完整的Flask后端实现

### 5.1 应用结构

```python
# app.py
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 数据模型
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(10), default='medium')
    completed = db.Column(db.Boolean, default=False)
    deadline = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'priority': self.priority,
            'completed': self.completed,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# 表单类
class TodoForm(FlaskForm):
    content = StringField('任务内容', validators=[
        DataRequired(message='请输入任务内容'),
        Length(min=1, max=200, message='任务内容长度应在1-200字符之间')
    ])
    priority = SelectField('优先级', choices=[
        ('low', '低优先级'),
        ('medium', '中优先级'),
        ('high', '高优先级')
    ], default='medium')
    deadline = DateField('截止日期', validators=[], format='%Y-%m-%d')

# 路由
@app.route('/')
def index():
    return redirect(url_for('todos'))

@app.route('/todos')
def todos():
    filter_type = request.args.get('filter', 'all')
    
    query = Todo.query
    
    if filter_type == 'active':
        query = query.filter_by(completed=False)
    elif filter_type == 'completed':
        query = query.filter_by(completed=True)
    
    todos = query.order_by(Todo.created_at.desc()).all()
    
    # 统计信息
    all_todos = Todo.query.all()
    stats = {
        'total': len(all_todos),
        'active': len([t for t in all_todos if not t.completed]),
        'completed': len([t for t in all_todos if t.completed])
    }
    
    form = TodoForm()
    
    return render_template('todos.html', 
                         todos=todos, 
                         form=form, 
                         filter_type=filter_type,
                         stats=stats)

# API路由
@app.route('/api/todos', methods=['GET'])
def api_get_todos():
    todos = Todo.query.order_by(Todo.created_at.desc()).all()
    return jsonify([todo.to_dict() for todo in todos])

@app.route('/api/todos', methods=['POST'])
def api_add_todo():
    try:
        data = request.get_json()
        
        todo = Todo(
            content=data['content'],
            priority=data.get('priority', 'medium'),
            deadline=datetime.strptime(data['deadline'], '%Y-%m-%d').date() if data.get('deadline') else None
        )
        
        db.session.add(todo)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'todo': todo.to_dict(),
            'message': '任务添加成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'添加失败: {str(e)}'
        }), 400

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def api_update_todo(todo_id):
    try:
        todo = Todo.query.get_or_404(todo_id)
        data = request.get_json()
        
        todo.content = data.get('content', todo.content)
        todo.priority = data.get('priority', todo.priority)
        todo.completed = data.get('completed', todo.completed)
        
        if data.get('deadline'):
            todo.deadline = datetime.strptime(data['deadline'], '%Y-%m-%d').date()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'todo': todo.to_dict(),
            'message': '任务更新成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'更新失败: {str(e)}'
        }), 400

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def api_delete_todo(todo_id):
    try:
        todo = Todo.query.get_or_404(todo_id)
        db.session.delete(todo)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '任务删除成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'删除失败: {str(e)}'
        }), 400

@app.route('/api/todos/<int:todo_id>/toggle', methods=['POST'])
def api_toggle_todo(todo_id):
    try:
        todo = Todo.query.get_or_404(todo_id)
        todo.completed = not todo.completed
        db.session.commit()
        
        return jsonify({
            'success': True,
            'todo': todo.to_dict(),
            'message': '任务状态更新成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'状态更新失败: {str(e)}'
        }), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

## 6. 实战技巧和最佳实践

### 6.1 错误处理和用户体验

```javascript
// 全局错误处理
class ErrorHandler {
    static handle(error, context = '') {
        console.error(`错误 [${context}]:`, error);
        
        let message = '操作失败，请重试';
        
        if (error.message) {
            message = error.message;
        } else if (typeof error === 'string') {
            message = error;
        }
        
        this.showError(message);
    }
    
    static showError(message) {
        const notification = new Notification(message, 'error');
        notification.show();
    }
    
    static showSuccess(message) {
        const notification = new Notification(message, 'success');
        notification.show();
    }
}

// 通知组件
class Notification {
    constructor(message, type = 'info') {
        this.message = message;
        this.type = type;
        this.element = null;
    }
    
    show() {
        this.element = document.createElement('div');
        this.element.className = `notification notification-${this.type}`;
        this.element.innerHTML = `
            <span class="notification-message">${this.message}</span>
            <button class="notification-close">&times;</button>
        `;
        
        document.body.appendChild(this.element);
        
        // 添加关闭事件
        this.element.querySelector('.notification-close').addEventListener('click', () => {
            this.hide();
        });
        
        // 自动消失
        setTimeout(() => {
            this.hide();
        }, 5000);
        
        // 添加动画
        requestAnimationFrame(() => {
            this.element.classList.add('show');
        });
    }
    
    hide() {
        if (this.element) {
            this.element.classList.add('hide');
            setTimeout(() => {
                if (this.element && this.element.parentNode) {
                    this.element.parentNode.removeChild(this.element);
                }
            }, 300);
        }
    }
}
```

### 6.2 性能优化

```javascript
// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 节流函数
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// 使用示例
const searchInput = document.getElementById('search');
const debouncedSearch = debounce(performSearch, 300);
searchInput.addEventListener('input', debouncedSearch);

// 虚拟滚动（处理大量数据）
class VirtualList {
    constructor(container, items, itemHeight, renderItem) {
        this.container = container;
        this.items = items;
        this.itemHeight = itemHeight;
        this.renderItem = renderItem;
        this.visibleStart = 0;
        this.visibleEnd = 0;
        
        this.init();
    }
    
    init() {
        this.containerHeight = this.container.clientHeight;
        this.visibleCount = Math.ceil(this.containerHeight / this.itemHeight);
        
        this.container.addEventListener('scroll', throttle(() => {
            this.updateVisibleRange();
            this.render();
        }, 16));
        
        this.updateVisibleRange();
        this.render();
    }
    
    updateVisibleRange() {
        const scrollTop = this.container.scrollTop;
        this.visibleStart = Math.floor(scrollTop / this.itemHeight);
        this.visibleEnd = Math.min(
            this.visibleStart + this.visibleCount + 1,
            this.items.length
        );
    }
    
    render() {
        const visibleItems = this.items.slice(this.visibleStart, this.visibleEnd);
        
        this.container.innerHTML = '';
        
        // 创建占位空间
        const topSpacer = document.createElement('div');
        topSpacer.style.height = `${this.visibleStart * this.itemHeight}px`;
        this.container.appendChild(topSpacer);
        
        // 渲染可见项目
        visibleItems.forEach((item, index) => {
            const element = this.renderItem(item, this.visibleStart + index);
            this.container.appendChild(element);
        });
        
        // 创建底部占位空间
        const bottomSpacer = document.createElement('div');
        bottomSpacer.style.height = `${(this.items.length - this.visibleEnd) * this.itemHeight}px`;
        this.container.appendChild(bottomSpacer);
    }
}
```

## 7. 总结

本课程详细介绍了前端集成的核心技术：

1. **HTML5语义化标签**：提高页面结构的可读性和可访问性
2. **现代CSS技术**：Flexbox、Grid布局，CSS变量，动画效果
3. **JavaScript ES6+**：类、箭头函数、async/await、模块化
4. **AJAX异步编程**：使用fetch API进行前后端数据交互
5. **Flask模板进阶**：模板继承、自定义过滤器、表单处理
6. **用户体验优化**：错误处理、加载状态、响应式设计
7. **性能优化**：防抖节流、虚拟滚动、代码分割

通过本课程的学习，你已经掌握了创建现代Web应用所需的前端技能，能够构建用户友好、功能完整的动态Web应用。

## 扩展阅读

- [MDN Web Docs](https://developer.mozilla.org/)
- [Flask官方文档](https://flask.palletsprojects.com/)
- [JavaScript.info](https://javascript.info/)
- [CSS-Tricks](https://css-tricks.com/)
- [Web.dev](https://web.dev/)