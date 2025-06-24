#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session19 练习2：JavaScript ES6+和AJAX练习

练习目标：
1. 掌握JavaScript ES6+新特性
2. 学习异步编程（Promise、async/await）
3. 实现AJAX数据交互
4. 构建动态Web应用

作者: Python教程团队
创建日期: 2024-12-24
"""

from flask import Flask, render_template_string, request, jsonify
from datetime import datetime, timedelta
import json
import random
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'exercise2-secret-key'

# 模拟数据库
tasks_db = [
    {
        'id': 1,
        'title': '学习JavaScript ES6语法',
        'description': '掌握箭头函数、解构赋值、模板字符串等新特性',
        'category': 'learning',
        'priority': 'high',
        'status': 'completed',
        'created_at': datetime.now() - timedelta(days=3),
        'due_date': datetime.now() - timedelta(days=1),
        'tags': ['JavaScript', 'ES6', '前端']
    },
    {
        'id': 2,
        'title': '实现AJAX数据交互',
        'description': '使用Fetch API进行异步数据请求和处理',
        'category': 'project',
        'priority': 'medium',
        'status': 'in_progress',
        'created_at': datetime.now() - timedelta(days=2),
        'due_date': datetime.now() + timedelta(days=2),
        'tags': ['AJAX', 'API', '异步编程']
    },
    {
        'id': 3,
        'title': '优化用户界面交互',
        'description': '添加加载状态、错误处理和用户反馈',
        'category': 'improvement',
        'priority': 'low',
        'status': 'pending',
        'created_at': datetime.now() - timedelta(days=1),
        'due_date': datetime.now() + timedelta(days=5),
        'tags': ['UI/UX', '用户体验', '交互设计']
    }
]

users_db = [
    {'id': 1, 'name': '张三', 'email': 'zhangsan@example.com', 'role': 'developer'},
    {'id': 2, 'name': '李四', 'email': 'lisi@example.com', 'role': 'designer'},
    {'id': 3, 'name': '王五', 'email': 'wangwu@example.com', 'role': 'manager'},
    {'id': 4, 'name': '赵六', 'email': 'zhaoliu@example.com', 'role': 'tester'}
]

# 练习模板
EXERCISE_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>任务管理系统 - JavaScript ES6+练习</title>
    
    <style>
        :root {
            --primary-color: #3b82f6;
            --secondary-color: #10b981;
            --warning-color: #f59e0b;
            --danger-color: #ef4444;
            --text-color: #1f2937;
            --text-light: #6b7280;
            --bg-color: #ffffff;
            --bg-light: #f9fafb;
            --border-color: #e5e7eb;
            --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            --border-radius: 8px;
            --transition: all 0.3s ease;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: var(--bg-light);
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .header h1 {
            font-size: 2.5rem;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }
        
        .header p {
            color: var(--text-light);
            font-size: 1.1rem;
        }
        
        .controls {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
            align-items: center;
        }
        
        .btn {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: var(--border-radius);
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .btn-primary {
            background-color: var(--primary-color);
            color: white;
        }
        
        .btn-primary:hover {
            background-color: #2563eb;
        }
        
        .btn-secondary {
            background-color: var(--secondary-color);
            color: white;
        }
        
        .btn-secondary:hover {
            background-color: #059669;
        }
        
        .btn-warning {
            background-color: var(--warning-color);
            color: white;
        }
        
        .btn-danger {
            background-color: var(--danger-color);
            color: white;
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .form-group {
            margin-bottom: 1rem;
        }
        
        .form-label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 600;
            color: var(--text-color);
        }
        
        .form-input {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            font-size: 1rem;
            transition: var(--transition);
        }
        
        .form-input:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        .form-select {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            background-color: white;
            cursor: pointer;
        }
        
        .grid {
            display: grid;
            gap: 2rem;
        }
        
        .grid-2 {
            grid-template-columns: 1fr 1fr;
        }
        
        .grid-3 {
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        }
        
        .card {
            background: var(--bg-color);
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            padding: 1.5rem;
            transition: var(--transition);
        }
        
        .card:hover {
            box-shadow: var(--shadow-lg);
        }
        
        .card-header {
            display: flex;
            justify-content: between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border-color);
        }
        
        .card-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--text-color);
        }
        
        .task-card {
            border-left: 4px solid;
            position: relative;
        }
        
        .task-card.priority-high {
            border-left-color: var(--danger-color);
        }
        
        .task-card.priority-medium {
            border-left-color: var(--warning-color);
        }
        
        .task-card.priority-low {
            border-left-color: var(--secondary-color);
        }
        
        .task-meta {
            display: flex;
            gap: 1rem;
            margin-bottom: 1rem;
            flex-wrap: wrap;
        }
        
        .badge {
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 500;
        }
        
        .badge-completed {
            background-color: #dcfce7;
            color: #166534;
        }
        
        .badge-in-progress {
            background-color: #fef3c7;
            color: #92400e;
        }
        
        .badge-pending {
            background-color: #fee2e2;
            color: #991b1b;
        }
        
        .tag {
            background-color: var(--bg-light);
            color: var(--text-light);
            padding: 0.25rem 0.5rem;
            border-radius: var(--border-radius);
            font-size: 0.75rem;
        }
        
        .task-actions {
            display: flex;
            gap: 0.5rem;
            margin-top: 1rem;
        }
        
        .btn-sm {
            padding: 0.5rem 1rem;
            font-size: 0.875rem;
        }
        
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 1000;
        }
        
        .modal.show {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .modal-content {
            background: var(--bg-color);
            border-radius: var(--border-radius);
            padding: 2rem;
            max-width: 500px;
            width: 90%;
            max-height: 90vh;
            overflow-y: auto;
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        
        .modal-title {
            font-size: 1.5rem;
            font-weight: 600;
        }
        
        .close-btn {
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: var(--text-light);
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
        
        .alert {
            padding: 1rem;
            border-radius: var(--border-radius);
            margin-bottom: 1rem;
        }
        
        .alert-success {
            background-color: #dcfce7;
            color: #166534;
            border: 1px solid #bbf7d0;
        }
        
        .alert-error {
            background-color: #fee2e2;
            color: #991b1b;
            border: 1px solid #fecaca;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        
        .stat-card {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            text-align: center;
            padding: 1.5rem;
            border-radius: var(--border-radius);
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .stat-label {
            opacity: 0.9;
        }
        
        @media (max-width: 768px) {
            .grid-2 {
                grid-template-columns: 1fr;
            }
            
            .controls {
                flex-direction: column;
                align-items: stretch;
            }
            
            .task-meta {
                flex-direction: column;
                gap: 0.5rem;
            }
            
            .task-actions {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 任务管理系统</h1>
            <p>JavaScript ES6+ 和 AJAX 技术练习</p>
        </div>
        
        <!-- 统计信息 -->
        <div class="stats" id="stats">
            <!-- 动态生成统计卡片 -->
        </div>
        
        <!-- 控制面板 -->
        <div class="controls">
            <button class="btn btn-primary" onclick="showAddTaskModal()">
                ➕ 添加任务
            </button>
            <button class="btn btn-secondary" onclick="loadTasks()">
                🔄 刷新数据
            </button>
            <button class="btn btn-warning" onclick="exportTasks()">
                📥 导出任务
            </button>
            <select class="form-select" id="filterStatus" onchange="filterTasks()" style="width: auto;">
                <option value="">全部状态</option>
                <option value="pending">待处理</option>
                <option value="in_progress">进行中</option>
                <option value="completed">已完成</option>
            </select>
            <select class="form-select" id="filterPriority" onchange="filterTasks()" style="width: auto;">
                <option value="">全部优先级</option>
                <option value="high">高</option>
                <option value="medium">中</option>
                <option value="low">低</option>
            </select>
        </div>
        
        <!-- 任务列表 -->
        <div class="grid grid-3" id="taskList">
            <!-- 动态生成任务卡片 -->
        </div>
        
        <!-- 用户管理区域 -->
        <div class="grid grid-2" style="margin-top: 3rem;">
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">👥 用户管理</h3>
                    <button class="btn btn-sm btn-primary" onclick="loadUsers()">
                        加载用户
                    </button>
                </div>
                <div id="userList">
                    <!-- 动态生成用户列表 -->
                </div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">📊 实时数据</h3>
                    <button class="btn btn-sm btn-secondary" onclick="startRealTimeUpdates()">
                        开始监控
                    </button>
                </div>
                <div id="realTimeData">
                    <p>点击"开始监控"查看实时数据更新</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- 添加任务模态框 -->
    <div class="modal" id="addTaskModal">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-title">添加新任务</h3>
                <button class="close-btn" onclick="hideAddTaskModal()">&times;</button>
            </div>
            <form id="addTaskForm">
                <div class="form-group">
                    <label class="form-label">任务标题</label>
                    <input type="text" class="form-input" id="taskTitle" required>
                </div>
                <div class="form-group">
                    <label class="form-label">任务描述</label>
                    <textarea class="form-input" id="taskDescription" rows="3"></textarea>
                </div>
                <div class="form-group">
                    <label class="form-label">分类</label>
                    <select class="form-select" id="taskCategory">
                        <option value="learning">学习</option>
                        <option value="project">项目</option>
                        <option value="improvement">改进</option>
                        <option value="bug">Bug修复</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">优先级</label>
                    <select class="form-select" id="taskPriority">
                        <option value="low">低</option>
                        <option value="medium">中</option>
                        <option value="high">高</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">截止日期</label>
                    <input type="date" class="form-input" id="taskDueDate">
                </div>
                <div class="form-group">
                    <label class="form-label">标签（用逗号分隔）</label>
                    <input type="text" class="form-input" id="taskTags" placeholder="例如：JavaScript, 前端, API">
                </div>
                <div style="display: flex; gap: 1rem; margin-top: 2rem;">
                    <button type="submit" class="btn btn-primary" style="flex: 1;">
                        <span id="submitBtnText">添加任务</span>
                        <span id="submitBtnLoading" class="loading" style="display: none;"></span>
                    </button>
                    <button type="button" class="btn btn-secondary" onclick="hideAddTaskModal()">
                        取消
                    </button>
                </div>
            </form>
        </div>
    </div>
    
    <script>
        // TODO: 练习内容 - 使用ES6+语法完成以下功能
        
        // 1. 使用类和模块化编程
        class TaskManager {
            constructor() {
                this.tasks = [];
                this.users = [];
                this.realTimeInterval = null;
                this.init();
            }
            
            async init() {
                // TODO: 初始化应用
                await this.loadTasks();
                this.updateStats();
                this.setupEventListeners();
            }
            
            setupEventListeners() {
                // TODO: 设置事件监听器
                const addTaskForm = document.getElementById('addTaskForm');
                addTaskForm.addEventListener('submit', (e) => this.handleAddTask(e));
                
                // 键盘快捷键
                document.addEventListener('keydown', (e) => {
                    if (e.ctrlKey && e.key === 'n') {
                        e.preventDefault();
                        this.showAddTaskModal();
                    }
                });
            }
            
            // 2. 使用async/await进行异步操作
            async loadTasks() {
                try {
                    // TODO: 实现任务加载
                    const response = await fetch('/api/tasks');
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    
                    const data = await response.json();
                    this.tasks = data.tasks;
                    this.renderTasks();
                    this.updateStats();
                    
                    this.showAlert('任务加载成功！', 'success');
                } catch (error) {
                    console.error('加载任务失败:', error);
                    this.showAlert('加载任务失败，请稍后重试', 'error');
                }
            }
            
            async addTask(taskData) {
                try {
                    // TODO: 实现任务添加
                    const response = await fetch('/api/tasks', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(taskData)
                    });
                    
                    if (!response.ok) {
                        throw new Error('添加任务失败');
                    }
                    
                    const result = await response.json();
                    this.tasks.push(result.task);
                    this.renderTasks();
                    this.updateStats();
                    
                    return result;
                } catch (error) {
                    console.error('添加任务失败:', error);
                    throw error;
                }
            }
            
            async updateTaskStatus(taskId, status) {
                try {
                    // TODO: 实现任务状态更新
                    const response = await fetch(`/api/tasks/${taskId}`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ status })
                    });
                    
                    if (!response.ok) {
                        throw new Error('更新任务状态失败');
                    }
                    
                    // 更新本地数据
                    const taskIndex = this.tasks.findIndex(task => task.id === taskId);
                    if (taskIndex !== -1) {
                        this.tasks[taskIndex].status = status;
                        this.renderTasks();
                        this.updateStats();
                    }
                    
                    this.showAlert('任务状态更新成功！', 'success');
                } catch (error) {
                    console.error('更新任务状态失败:', error);
                    this.showAlert('更新失败，请稍后重试', 'error');
                }
            }
            
            async deleteTask(taskId) {
                if (!confirm('确定要删除这个任务吗？')) {
                    return;
                }
                
                try {
                    // TODO: 实现任务删除
                    const response = await fetch(`/api/tasks/${taskId}`, {
                        method: 'DELETE'
                    });
                    
                    if (!response.ok) {
                        throw new Error('删除任务失败');
                    }
                    
                    // 从本地数据中移除
                    this.tasks = this.tasks.filter(task => task.id !== taskId);
                    this.renderTasks();
                    this.updateStats();
                    
                    this.showAlert('任务删除成功！', 'success');
                } catch (error) {
                    console.error('删除任务失败:', error);
                    this.showAlert('删除失败，请稍后重试', 'error');
                }
            }
            
            // 3. 使用解构赋值和模板字符串
            renderTasks(filteredTasks = null) {
                const tasksToRender = filteredTasks || this.tasks;
                const taskList = document.getElementById('taskList');
                
                if (tasksToRender.length === 0) {
                    taskList.innerHTML = `
                        <div class="card" style="grid-column: 1 / -1; text-align: center; padding: 3rem;">
                            <h3>📝 暂无任务</h3>
                            <p>点击"添加任务"创建你的第一个任务</p>
                        </div>
                    `;
                    return;
                }
                
                // TODO: 使用map和模板字符串渲染任务
                taskList.innerHTML = tasksToRender.map(task => {
                    const { id, title, description, category, priority, status, due_date, tags } = task;
                    const statusBadge = this.getStatusBadge(status);
                    const priorityClass = `priority-${priority}`;
                    const tagsHtml = tags.map(tag => `<span class="tag">${tag}</span>`).join('');
                    
                    return `
                        <div class="card task-card ${priorityClass}">
                            <div class="task-meta">
                                ${statusBadge}
                                <span class="badge badge-${priority}">${this.getPriorityText(priority)}</span>
                                <small>${category}</small>
                            </div>
                            <h3>${title}</h3>
                            <p>${description}</p>
                            <div style="margin: 1rem 0;">
                                ${tagsHtml}
                            </div>
                            ${due_date ? `<p><strong>截止：</strong>${this.formatDate(due_date)}</p>` : ''}
                            <div class="task-actions">
                                ${this.getStatusButtons(id, status)}
                                <button class="btn btn-sm btn-danger" onclick="taskManager.deleteTask(${id})">
                                    🗑️ 删除
                                </button>
                            </div>
                        </div>
                    `;
                }).join('');
            }
            
            // 4. 使用箭头函数和高阶函数
            filterTasks() {
                const statusFilter = document.getElementById('filterStatus').value;
                const priorityFilter = document.getElementById('filterPriority').value;
                
                // TODO: 使用filter方法过滤任务
                const filteredTasks = this.tasks.filter(task => {
                    const statusMatch = !statusFilter || task.status === statusFilter;
                    const priorityMatch = !priorityFilter || task.priority === priorityFilter;
                    return statusMatch && priorityMatch;
                });
                
                this.renderTasks(filteredTasks);
            }
            
            updateStats() {
                // TODO: 使用reduce计算统计信息
                const stats = this.tasks.reduce((acc, task) => {
                    acc.total++;
                    acc[task.status] = (acc[task.status] || 0) + 1;
                    return acc;
                }, { total: 0, pending: 0, in_progress: 0, completed: 0 });
                
                const statsContainer = document.getElementById('stats');
                statsContainer.innerHTML = `
                    <div class="stat-card">
                        <div class="stat-number">${stats.total}</div>
                        <div class="stat-label">总任务数</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${stats.pending || 0}</div>
                        <div class="stat-label">待处理</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${stats.in_progress || 0}</div>
                        <div class="stat-label">进行中</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${stats.completed || 0}</div>
                        <div class="stat-label">已完成</div>
                    </div>
                `;
            }
            
            // 5. 使用Promise和错误处理
            async handleAddTask(event) {
                event.preventDefault();
                
                const submitBtn = document.getElementById('submitBtnText');
                const loadingSpinner = document.getElementById('submitBtnLoading');
                
                try {
                    // 显示加载状态
                    submitBtn.style.display = 'none';
                    loadingSpinner.style.display = 'inline-block';
                    
                    // TODO: 收集表单数据
                    const formData = new FormData(event.target);
                    const taskData = {
                        title: document.getElementById('taskTitle').value,
                        description: document.getElementById('taskDescription').value,
                        category: document.getElementById('taskCategory').value,
                        priority: document.getElementById('taskPriority').value,
                        due_date: document.getElementById('taskDueDate').value,
                        tags: document.getElementById('taskTags').value
                            .split(',')
                            .map(tag => tag.trim())
                            .filter(tag => tag.length > 0)
                    };
                    
                    await this.addTask(taskData);
                    
                    // 重置表单并关闭模态框
                    event.target.reset();
                    this.hideAddTaskModal();
                    this.showAlert('任务添加成功！', 'success');
                    
                } catch (error) {
                    console.error('添加任务失败:', error);
                    this.showAlert('添加任务失败，请检查输入信息', 'error');
                } finally {
                    // 恢复按钮状态
                    submitBtn.style.display = 'inline';
                    loadingSpinner.style.display = 'none';
                }
            }
            
            // 工具方法
            getStatusBadge(status) {
                const statusMap = {
                    pending: { class: 'badge-pending', text: '待处理' },
                    in_progress: { class: 'badge-in-progress', text: '进行中' },
                    completed: { class: 'badge-completed', text: '已完成' }
                };
                const { class: badgeClass, text } = statusMap[status] || statusMap.pending;
                return `<span class="badge ${badgeClass}">${text}</span>`;
            }
            
            getPriorityText(priority) {
                const priorityMap = { high: '高', medium: '中', low: '低' };
                return priorityMap[priority] || priority;
            }
            
            getStatusButtons(taskId, currentStatus) {
                const buttons = [];
                
                if (currentStatus !== 'in_progress') {
                    buttons.push(`<button class="btn btn-sm btn-warning" onclick="taskManager.updateTaskStatus(${taskId}, 'in_progress')">▶️ 开始</button>`);
                }
                
                if (currentStatus !== 'completed') {
                    buttons.push(`<button class="btn btn-sm btn-secondary" onclick="taskManager.updateTaskStatus(${taskId}, 'completed')">✅ 完成</button>`);
                }
                
                if (currentStatus !== 'pending') {
                    buttons.push(`<button class="btn btn-sm btn-primary" onclick="taskManager.updateTaskStatus(${taskId}, 'pending')">⏸️ 暂停</button>`);
                }
                
                return buttons.join('');
            }
            
            formatDate(dateString) {
                const date = new Date(dateString);
                return date.toLocaleDateString('zh-CN');
            }
            
            showAlert(message, type = 'success') {
                // TODO: 实现消息提示
                const alertDiv = document.createElement('div');
                alertDiv.className = `alert alert-${type}`;
                alertDiv.textContent = message;
                
                document.body.insertBefore(alertDiv, document.body.firstChild);
                
                setTimeout(() => {
                    alertDiv.remove();
                }, 3000);
            }
            
            showAddTaskModal() {
                document.getElementById('addTaskModal').classList.add('show');
            }
            
            hideAddTaskModal() {
                document.getElementById('addTaskModal').classList.remove('show');
            }
            
            // 6. 实时数据更新
            async startRealTimeUpdates() {
                const realTimeData = document.getElementById('realTimeData');
                
                if (this.realTimeInterval) {
                    clearInterval(this.realTimeInterval);
                    this.realTimeInterval = null;
                    realTimeData.innerHTML = '<p>实时监控已停止</p>';
                    return;
                }
                
                realTimeData.innerHTML = '<p>🔄 正在监控实时数据...</p>';
                
                this.realTimeInterval = setInterval(async () => {
                    try {
                        const response = await fetch('/api/realtime');
                        const data = await response.json();
                        
                        realTimeData.innerHTML = `
                            <div>
                                <p><strong>当前时间：</strong>${new Date().toLocaleString()}</p>
                                <p><strong>在线用户：</strong>${data.online_users}</p>
                                <p><strong>系统负载：</strong>${data.system_load}%</p>
                                <p><strong>内存使用：</strong>${data.memory_usage}%</p>
                                <p><strong>活跃任务：</strong>${data.active_tasks}</p>
                            </div>
                        `;
                    } catch (error) {
                        console.error('获取实时数据失败:', error);
                    }
                }, 2000);
            }
            
            // 7. 用户管理
            async loadUsers() {
                try {
                    const response = await fetch('/api/users');
                    const data = await response.json();
                    this.users = data.users;
                    
                    const userList = document.getElementById('userList');
                    userList.innerHTML = this.users.map(user => `
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid var(--border-color);">
                            <div>
                                <strong>${user.name}</strong><br>
                                <small>${user.email} - ${user.role}</small>
                            </div>
                            <span class="badge badge-completed">在线</span>
                        </div>
                    `).join('');
                    
                } catch (error) {
                    console.error('加载用户失败:', error);
                }
            }
            
            // 8. 数据导出
            exportTasks() {
                // TODO: 实现数据导出功能
                const dataStr = JSON.stringify(this.tasks, null, 2);
                const dataBlob = new Blob([dataStr], { type: 'application/json' });
                
                const link = document.createElement('a');
                link.href = URL.createObjectURL(dataBlob);
                link.download = `tasks_${new Date().toISOString().split('T')[0]}.json`;
                link.click();
                
                this.showAlert('任务数据导出成功！', 'success');
            }
        }
        
        // 初始化应用
        let taskManager;
        
        document.addEventListener('DOMContentLoaded', () => {
            taskManager = new TaskManager();
        });
        
        // 全局函数（为了简化HTML中的事件处理）
        function showAddTaskModal() {
            taskManager.showAddTaskModal();
        }
        
        function hideAddTaskModal() {
            taskManager.hideAddTaskModal();
        }
        
        function loadTasks() {
            taskManager.loadTasks();
        }
        
        function filterTasks() {
            taskManager.filterTasks();
        }
        
        function exportTasks() {
            taskManager.exportTasks();
        }
        
        function loadUsers() {
            taskManager.loadUsers();
        }
        
        function startRealTimeUpdates() {
            taskManager.startRealTimeUpdates();
        }
        
        // 演示ES6+特性
        console.log('🚀 任务管理系统已启动！');
        console.log('演示的ES6+特性包括：');
        console.log('- 类和模块化编程');
        console.log('- async/await异步编程');
        console.log('- 箭头函数和解构赋值');
        console.log('- 模板字符串和高阶函数');
        console.log('- Promise和错误处理');
        console.log('- Fetch API和现代AJAX');
    </script>
</body>
</html>
"""

# API路由
@app.route('/')
def index():
    """
    练习2主页
    """
    return render_template_string(EXERCISE_TEMPLATE)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """
    获取任务列表
    """
    # 模拟网络延迟
    time.sleep(0.5)
    
    # 转换日期格式
    tasks_json = []
    for task in tasks_db:
        task_copy = task.copy()
        task_copy['created_at'] = task['created_at'].isoformat()
        task_copy['due_date'] = task['due_date'].isoformat() if task['due_date'] else None
        tasks_json.append(task_copy)
    
    return jsonify({
        'success': True,
        'tasks': tasks_json,
        'total': len(tasks_json)
    })

@app.route('/api/tasks', methods=['POST'])
def add_task():
    """
    添加新任务
    """
    # 模拟网络延迟
    time.sleep(1)
    
    data = request.get_json()
    
    # 验证数据
    if not data.get('title'):
        return jsonify({
            'success': False,
            'message': '任务标题不能为空'
        }), 400
    
    # 创建新任务
    new_task = {
        'id': len(tasks_db) + 1,
        'title': data['title'],
        'description': data.get('description', ''),
        'category': data.get('category', 'learning'),
        'priority': data.get('priority', 'medium'),
        'status': 'pending',
        'created_at': datetime.now(),
        'due_date': datetime.fromisoformat(data['due_date']) if data.get('due_date') else None,
        'tags': data.get('tags', [])
    }
    
    tasks_db.append(new_task)
    
    # 转换日期格式用于返回
    task_json = new_task.copy()
    task_json['created_at'] = new_task['created_at'].isoformat()
    task_json['due_date'] = new_task['due_date'].isoformat() if new_task['due_date'] else None
    
    return jsonify({
        'success': True,
        'message': '任务添加成功',
        'task': task_json
    })

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    更新任务
    """
    # 模拟网络延迟
    time.sleep(0.3)
    
    data = request.get_json()
    
    # 查找任务
    task = next((t for t in tasks_db if t['id'] == task_id), None)
    if not task:
        return jsonify({
            'success': False,
            'message': '任务不存在'
        }), 404
    
    # 更新任务状态
    if 'status' in data:
        task['status'] = data['status']
    
    return jsonify({
        'success': True,
        'message': '任务更新成功'
    })

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    删除任务
    """
    # 模拟网络延迟
    time.sleep(0.5)
    
    global tasks_db
    
    # 查找并删除任务
    task_index = next((i for i, t in enumerate(tasks_db) if t['id'] == task_id), None)
    if task_index is None:
        return jsonify({
            'success': False,
            'message': '任务不存在'
        }), 404
    
    tasks_db.pop(task_index)
    
    return jsonify({
        'success': True,
        'message': '任务删除成功'
    })

@app.route('/api/users', methods=['GET'])
def get_users():
    """
    获取用户列表
    """
    # 模拟网络延迟
    time.sleep(0.8)
    
    return jsonify({
        'success': True,
        'users': users_db,
        'total': len(users_db)
    })

@app.route('/api/realtime', methods=['GET'])
def get_realtime_data():
    """
    获取实时数据
    """
    # 模拟实时数据
    return jsonify({
        'online_users': random.randint(50, 200),
        'system_load': random.randint(20, 80),
        'memory_usage': random.randint(30, 70),
        'active_tasks': len([t for t in tasks_db if t['status'] == 'in_progress']),
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("Session19 练习2：JavaScript ES6+和AJAX练习")
    print("=" * 50)
    print("练习内容：")
    print("1. 使用ES6+类和模块化编程")
    print("2. 掌握async/await异步编程")
    print("3. 实现Fetch API和AJAX数据交互")
    print("4. 使用解构赋值和模板字符串")
    print("5. 应用箭头函数和高阶函数")
    print("6. 实现错误处理和用户反馈")
    print("7. 构建实时数据更新功能")
    print("8. 创建现代化的用户界面")
    print("\n练习要求：")
    print("- 完成TaskManager类的所有TODO项")
    print("- 实现完整的CRUD操作")
    print("- 添加错误处理和加载状态")
    print("- 优化用户体验和交互")
    print("- 使用现代JavaScript最佳实践")
    print("\n访问 http://localhost:5000 查看练习页面")
    
    app.run(debug=True, host='0.0.0.0', port=5000)