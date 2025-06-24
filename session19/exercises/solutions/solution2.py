#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session19 练习2解决方案：JavaScript ES6+和AJAX技术

本文件提供练习2的完整解决方案，展示如何实现：
1. JavaScript ES6+语法特性的综合应用
2. 类、async/await、解构赋值等现代语法
3. Fetch API和现代AJAX技术
4. Promise和错误处理
5. 实时数据更新和用户体验优化

作者: Python教程团队
创建日期: 2024-12-24
"""

from flask import Flask, render_template_string, request, jsonify
from datetime import datetime, timedelta
import json
import random
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'solution2-secret-key'

# 任务数据
tasks_db = [
    {
        'id': 1,
        'title': '完成项目文档',
        'description': '编写项目的技术文档和用户手册',
        'status': 'pending',
        'priority': 'high',
        'category': 'documentation',
        'assignee': 'Alice',
        'due_date': (datetime.now() + timedelta(days=3)).isoformat(),
        'created_at': (datetime.now() - timedelta(days=2)).isoformat(),
        'updated_at': (datetime.now() - timedelta(hours=1)).isoformat(),
        'tags': ['文档', '技术', '重要'],
        'progress': 60
    },
    {
        'id': 2,
        'title': '修复登录bug',
        'description': '解决用户登录时偶尔出现的验证失败问题',
        'status': 'in_progress',
        'priority': 'urgent',
        'category': 'bug',
        'assignee': 'Bob',
        'due_date': (datetime.now() + timedelta(days=1)).isoformat(),
        'created_at': (datetime.now() - timedelta(days=1)).isoformat(),
        'updated_at': (datetime.now() - timedelta(minutes=30)).isoformat(),
        'tags': ['Bug', '登录', '紧急'],
        'progress': 80
    },
    {
        'id': 3,
        'title': '设计新功能界面',
        'description': '为即将上线的新功能设计用户界面',
        'status': 'completed',
        'priority': 'medium',
        'category': 'design',
        'assignee': 'Carol',
        'due_date': (datetime.now() - timedelta(days=1)).isoformat(),
        'created_at': (datetime.now() - timedelta(days=5)).isoformat(),
        'updated_at': (datetime.now() - timedelta(hours=2)).isoformat(),
        'tags': ['设计', 'UI', '新功能'],
        'progress': 100
    },
    {
        'id': 4,
        'title': '数据库优化',
        'description': '优化数据库查询性能，减少响应时间',
        'status': 'pending',
        'priority': 'medium',
        'category': 'optimization',
        'assignee': 'David',
        'due_date': (datetime.now() + timedelta(days=7)).isoformat(),
        'created_at': (datetime.now() - timedelta(hours=6)).isoformat(),
        'updated_at': (datetime.now() - timedelta(hours=6)).isoformat(),
        'tags': ['数据库', '性能', '优化'],
        'progress': 0
    },
    {
        'id': 5,
        'title': '用户反馈分析',
        'description': '分析最近收到的用户反馈，制定改进计划',
        'status': 'in_progress',
        'priority': 'low',
        'category': 'analysis',
        'assignee': 'Eve',
        'due_date': (datetime.now() + timedelta(days=5)).isoformat(),
        'created_at': (datetime.now() - timedelta(days=3)).isoformat(),
        'updated_at': (datetime.now() - timedelta(hours=4)).isoformat(),
        'tags': ['用户反馈', '分析', '改进'],
        'progress': 30
    }
]

# 用户数据
users_db = [
    {'id': 1, 'name': 'Alice', 'email': 'alice@example.com', 'role': 'Developer', 'avatar': '👩‍💻'},
    {'id': 2, 'name': 'Bob', 'email': 'bob@example.com', 'role': 'Developer', 'avatar': '👨‍💻'},
    {'id': 3, 'name': 'Carol', 'email': 'carol@example.com', 'role': 'Designer', 'avatar': '👩‍🎨'},
    {'id': 4, 'name': 'David', 'email': 'david@example.com', 'role': 'DBA', 'avatar': '👨‍🔧'},
    {'id': 5, 'name': 'Eve', 'email': 'eve@example.com', 'role': 'Analyst', 'avatar': '👩‍📊'}
]

# 解决方案模板
SOLUTION_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>任务管理系统 - JavaScript ES6+解决方案</title>
    
    <style>
        :root {
            --primary-color: #3b82f6;
            --secondary-color: #10b981;
            --accent-color: #f59e0b;
            --danger-color: #ef4444;
            --success-color: #059669;
            --warning-color: #d97706;
            --info-color: #0ea5e9;
            
            --text-primary: #1f2937;
            --text-secondary: #6b7280;
            --text-light: #9ca3af;
            --text-white: #ffffff;
            
            --bg-primary: #ffffff;
            --bg-secondary: #f9fafb;
            --bg-dark: #111827;
            
            --border-color: #e5e7eb;
            --border-radius: 8px;
            --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            
            --transition: all 0.3s ease;
            --font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: var(--font-family);
            background-color: var(--bg-secondary);
            color: var(--text-primary);
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: var(--text-white);
            padding: 2rem 0;
            margin-bottom: 2rem;
            border-radius: var(--border-radius);
        }
        
        .header h1 {
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        
        .header p {
            text-align: center;
            opacity: 0.9;
            font-size: 1.1rem;
        }
        
        .controls {
            background: var(--bg-primary);
            padding: 1.5rem;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            margin-bottom: 2rem;
        }
        
        .controls-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            align-items: end;
        }
        
        .form-group {
            display: flex;
            flex-direction: column;
        }
        
        .form-label {
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--text-primary);
        }
        
        .form-input,
        .form-select {
            padding: 0.75rem;
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            font-size: 1rem;
            transition: var(--transition);
        }
        
        .form-input:focus,
        .form-select:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        .btn {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: var(--border-radius);
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .btn-primary {
            background-color: var(--primary-color);
            color: var(--text-white);
        }
        
        .btn-primary:hover {
            background-color: #2563eb;
            transform: translateY(-2px);
        }
        
        .btn-secondary {
            background-color: var(--secondary-color);
            color: var(--text-white);
        }
        
        .btn-secondary:hover {
            background-color: #059669;
        }
        
        .btn-danger {
            background-color: var(--danger-color);
            color: var(--text-white);
        }
        
        .btn-danger:hover {
            background-color: #dc2626;
        }
        
        .btn-sm {
            padding: 0.5rem 1rem;
            font-size: 0.875rem;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        
        .stat-card {
            background: var(--bg-primary);
            padding: 1.5rem;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            text-align: center;
            transition: var(--transition);
        }
        
        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .stat-label {
            color: var(--text-secondary);
            font-size: 0.875rem;
        }
        
        .tasks-container {
            background: var(--bg-primary);
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            overflow: hidden;
        }
        
        .tasks-header {
            padding: 1.5rem;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .tasks-grid {
            display: grid;
            gap: 1rem;
            padding: 1.5rem;
        }
        
        .task-card {
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            padding: 1.5rem;
            transition: var(--transition);
            position: relative;
            overflow: hidden;
        }
        
        .task-card:hover {
            border-color: var(--primary-color);
            box-shadow: var(--shadow-lg);
        }
        
        .task-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }
        
        .task-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        
        .task-meta {
            display: flex;
            gap: 1rem;
            font-size: 0.875rem;
            color: var(--text-secondary);
            margin-bottom: 1rem;
        }
        
        .task-description {
            color: var(--text-secondary);
            margin-bottom: 1rem;
            line-height: 1.6;
        }
        
        .task-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }
        
        .tag {
            padding: 0.25rem 0.75rem;
            background-color: var(--bg-secondary);
            color: var(--text-secondary);
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 500;
        }
        
        .task-progress {
            margin-bottom: 1rem;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background-color: var(--bg-secondary);
            border-radius: 4px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            transition: width 0.3s ease;
        }
        
        .progress-text {
            font-size: 0.875rem;
            color: var(--text-secondary);
            margin-top: 0.25rem;
        }
        
        .task-actions {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }
        
        .badge {
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        .badge-pending {
            background-color: rgba(245, 158, 11, 0.1);
            color: var(--warning-color);
        }
        
        .badge-in-progress {
            background-color: rgba(59, 130, 246, 0.1);
            color: var(--primary-color);
        }
        
        .badge-completed {
            background-color: rgba(16, 185, 129, 0.1);
            color: var(--success-color);
        }
        
        .badge-high {
            background-color: rgba(239, 68, 68, 0.1);
            color: var(--danger-color);
        }
        
        .badge-medium {
            background-color: rgba(245, 158, 11, 0.1);
            color: var(--warning-color);
        }
        
        .badge-low {
            background-color: rgba(107, 114, 128, 0.1);
            color: var(--text-secondary);
        }
        
        .badge-urgent {
            background-color: rgba(239, 68, 68, 0.2);
            color: var(--danger-color);
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
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
            to { transform: rotate(360deg); }
        }
        
        .hidden {
            display: none;
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
            background: var(--bg-primary);
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
            margin-bottom: 1.5rem;
        }
        
        .modal-title {
            font-size: 1.5rem;
            font-weight: 600;
        }
        
        .modal-close {
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: var(--text-secondary);
        }
        
        .form-textarea {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            resize: vertical;
            min-height: 100px;
            font-family: inherit;
        }
        
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--bg-primary);
            border-radius: var(--border-radius);
            box-shadow: var(--shadow-lg);
            padding: 1rem;
            max-width: 300px;
            z-index: 2000;
            animation: slideInRight 0.3s ease-out;
        }
        
        .notification.success {
            border-left: 4px solid var(--success-color);
        }
        
        .notification.error {
            border-left: 4px solid var(--danger-color);
        }
        
        .notification.warning {
            border-left: 4px solid var(--warning-color);
        }
        
        .notification.info {
            border-left: 4px solid var(--info-color);
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
        
        @keyframes slideOutRight {
            from {
                opacity: 1;
                transform: translateX(0);
            }
            to {
                opacity: 0;
                transform: translateX(100%);
            }
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .controls-grid {
                grid-template-columns: 1fr;
            }
            
            .stats {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .task-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 0.5rem;
            }
            
            .task-meta {
                flex-direction: column;
                gap: 0.5rem;
            }
            
            .task-actions {
                justify-content: flex-start;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 任务管理系统</h1>
            <p>JavaScript ES6+ 和 AJAX 技术解决方案</p>
        </div>
        
        <!-- 控制面板 -->
        <div class="controls">
            <div class="controls-grid">
                <div class="form-group">
                    <label class="form-label">搜索任务</label>
                    <input type="text" class="form-input" id="searchInput" placeholder="输入关键词搜索...">
                </div>
                
                <div class="form-group">
                    <label class="form-label">状态筛选</label>
                    <select class="form-select" id="statusFilter">
                        <option value="">全部状态</option>
                        <option value="pending">待处理</option>
                        <option value="in_progress">进行中</option>
                        <option value="completed">已完成</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label class="form-label">优先级筛选</label>
                    <select class="form-select" id="priorityFilter">
                        <option value="">全部优先级</option>
                        <option value="urgent">紧急</option>
                        <option value="high">高</option>
                        <option value="medium">中</option>
                        <option value="low">低</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label class="form-label">负责人筛选</label>
                    <select class="form-select" id="assigneeFilter">
                        <option value="">全部负责人</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label class="form-label">排序方式</label>
                    <select class="form-select" id="sortBy">
                        <option value="created_at">创建时间</option>
                        <option value="due_date">截止时间</option>
                        <option value="priority">优先级</option>
                        <option value="progress">进度</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label class="form-label">操作</label>
                    <button class="btn btn-primary" onclick="taskManager.openCreateModal()">➕ 新建任务</button>
                </div>
            </div>
        </div>
        
        <!-- 统计信息 -->
        <div class="stats" id="statsContainer">
            <!-- 统计卡片将通过JavaScript动态生成 -->
        </div>
        
        <!-- 任务列表 -->
        <div class="tasks-container">
            <div class="tasks-header">
                <h2>📋 任务列表</h2>
                <div>
                    <button class="btn btn-secondary btn-sm" onclick="taskManager.refreshTasks()">
                        <span id="refreshText">🔄 刷新</span>
                        <span id="refreshSpinner" class="loading hidden"></span>
                    </button>
                    <button class="btn btn-primary btn-sm" onclick="taskManager.exportTasks()">📤 导出</button>
                </div>
            </div>
            
            <div class="tasks-grid" id="tasksContainer">
                <!-- 任务卡片将通过JavaScript动态生成 -->
            </div>
        </div>
    </div>
    
    <!-- 任务创建/编辑模态框 -->
    <div class="modal" id="taskModal">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-title" id="modalTitle">新建任务</h3>
                <button class="modal-close" onclick="taskManager.closeModal()">&times;</button>
            </div>
            
            <form id="taskForm">
                <input type="hidden" id="taskId">
                
                <div class="form-group">
                    <label class="form-label">任务标题</label>
                    <input type="text" class="form-input" id="taskTitle" required>
                </div>
                
                <div class="form-group">
                    <label class="form-label">任务描述</label>
                    <textarea class="form-textarea" id="taskDescription" placeholder="详细描述任务内容..."></textarea>
                </div>
                
                <div class="form-group">
                    <label class="form-label">优先级</label>
                    <select class="form-select" id="taskPriority" required>
                        <option value="low">低</option>
                        <option value="medium">中</option>
                        <option value="high">高</option>
                        <option value="urgent">紧急</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label class="form-label">分类</label>
                    <select class="form-select" id="taskCategory" required>
                        <option value="development">开发</option>
                        <option value="design">设计</option>
                        <option value="testing">测试</option>
                        <option value="documentation">文档</option>
                        <option value="bug">Bug修复</option>
                        <option value="optimization">优化</option>
                        <option value="analysis">分析</option>
                        <option value="other">其他</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label class="form-label">负责人</label>
                    <select class="form-select" id="taskAssignee" required>
                        <!-- 选项将通过JavaScript动态生成 -->
                    </select>
                </div>
                
                <div class="form-group">
                    <label class="form-label">截止日期</label>
                    <input type="datetime-local" class="form-input" id="taskDueDate" required>
                </div>
                
                <div class="form-group">
                    <label class="form-label">标签（用逗号分隔）</label>
                    <input type="text" class="form-input" id="taskTags" placeholder="例如：重要,紧急,前端">
                </div>
                
                <div class="form-group">
                    <label class="form-label">进度 (%)</label>
                    <input type="range" class="form-input" id="taskProgress" min="0" max="100" value="0">
                    <div class="progress-text" id="progressText">0%</div>
                </div>
                
                <div style="display: flex; gap: 1rem; justify-content: flex-end; margin-top: 2rem;">
                    <button type="button" class="btn btn-secondary" onclick="taskManager.closeModal()">取消</button>
                    <button type="submit" class="btn btn-primary">
                        <span id="submitText">保存任务</span>
                        <span id="submitSpinner" class="loading hidden"></span>
                    </button>
                </div>
            </form>
        </div>
    </div>
    
    <script>
        // ES6+ 类定义 - 任务管理器
        class TaskManager {
            constructor() {
                this.tasks = [];
                this.users = [];
                this.filteredTasks = [];
                this.currentEditId = null;
                
                // 绑定方法到实例
                this.handleSearch = this.debounce(this.filterTasks.bind(this), 300);
                this.handleRealtimeUpdate = this.handleRealtimeUpdate.bind(this);
                
                this.init();
            }
            
            // 初始化
            async init() {
                try {
                    await this.loadInitialData();
                    this.setupEventListeners();
                    this.startRealtimeUpdates();
                    this.renderAll();
                } catch (error) {
                    console.error('初始化失败:', error);
                    this.showNotification('初始化失败，请刷新页面重试', 'error');
                }
            }
            
            // 加载初始数据
            async loadInitialData() {
                const [tasksResponse, usersResponse] = await Promise.all([
                    this.fetchWithRetry('/api/tasks'),
                    this.fetchWithRetry('/api/users')
                ]);
                
                const [tasksData, usersData] = await Promise.all([
                    tasksResponse.json(),
                    usersResponse.json()
                ]);
                
                this.tasks = tasksData.tasks || [];
                this.users = usersData.users || [];
                this.filteredTasks = [...this.tasks];
                
                this.populateAssigneeOptions();
            }
            
            // 带重试的fetch
            async fetchWithRetry(url, options = {}, retries = 3) {
                for (let i = 0; i < retries; i++) {
                    try {
                        const response = await fetch(url, options);
                        if (!response.ok) {
                            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                        }
                        return response;
                    } catch (error) {
                        if (i === retries - 1) throw error;
                        await this.delay(1000 * (i + 1)); // 递增延迟
                    }
                }
            }
            
            // 延迟函数
            delay(ms) {
                return new Promise(resolve => setTimeout(resolve, ms));
            }
            
            // 防抖函数
            debounce(func, wait) {
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
            
            // 设置事件监听器
            setupEventListeners() {
                // 搜索和筛选
                document.getElementById('searchInput').addEventListener('input', this.handleSearch);
                document.getElementById('statusFilter').addEventListener('change', () => this.filterTasks());
                document.getElementById('priorityFilter').addEventListener('change', () => this.filterTasks());
                document.getElementById('assigneeFilter').addEventListener('change', () => this.filterTasks());
                document.getElementById('sortBy').addEventListener('change', () => this.filterTasks());
                
                // 表单提交
                document.getElementById('taskForm').addEventListener('submit', (e) => this.handleSubmit(e));
                
                // 进度滑块
                document.getElementById('taskProgress').addEventListener('input', (e) => {
                    document.getElementById('progressText').textContent = `${e.target.value}%`;
                });
                
                // 模态框外部点击关闭
                document.getElementById('taskModal').addEventListener('click', (e) => {
                    if (e.target.id === 'taskModal') {
                        this.closeModal();
                    }
                });
                
                // ESC键关闭模态框
                document.addEventListener('keydown', (e) => {
                    if (e.key === 'Escape') {
                        this.closeModal();
                    }
                });
            }
            
            // 填充负责人选项
            populateAssigneeOptions() {
                const assigneeFilter = document.getElementById('assigneeFilter');
                const taskAssignee = document.getElementById('taskAssignee');
                
                // 清空现有选项
                assigneeFilter.innerHTML = '<option value="">全部负责人</option>';
                taskAssignee.innerHTML = '';
                
                this.users.forEach(user => {
                    const option1 = new Option(`${user.avatar} ${user.name}`, user.name);
                    const option2 = new Option(`${user.avatar} ${user.name}`, user.name);
                    
                    assigneeFilter.appendChild(option1);
                    taskAssignee.appendChild(option2);
                });
            }
            
            // 过滤任务
            filterTasks() {
                const searchTerm = document.getElementById('searchInput').value.toLowerCase();
                const statusFilter = document.getElementById('statusFilter').value;
                const priorityFilter = document.getElementById('priorityFilter').value;
                const assigneeFilter = document.getElementById('assigneeFilter').value;
                const sortBy = document.getElementById('sortBy').value;
                
                // 使用数组方法进行过滤
                this.filteredTasks = this.tasks.filter(task => {
                    const matchesSearch = !searchTerm || 
                        task.title.toLowerCase().includes(searchTerm) ||
                        task.description.toLowerCase().includes(searchTerm) ||
                        task.tags.some(tag => tag.toLowerCase().includes(searchTerm));
                    
                    const matchesStatus = !statusFilter || task.status === statusFilter;
                    const matchesPriority = !priorityFilter || task.priority === priorityFilter;
                    const matchesAssignee = !assigneeFilter || task.assignee === assigneeFilter;
                    
                    return matchesSearch && matchesStatus && matchesPriority && matchesAssignee;
                });
                
                // 排序
                this.sortTasks(sortBy);
                
                // 重新渲染
                this.renderTasks();
                this.renderStats();
            }
            
            // 排序任务
            sortTasks(sortBy) {
                const priorityOrder = { urgent: 4, high: 3, medium: 2, low: 1 };
                
                this.filteredTasks.sort((a, b) => {
                    switch (sortBy) {
                        case 'priority':
                            return priorityOrder[b.priority] - priorityOrder[a.priority];
                        case 'due_date':
                            return new Date(a.due_date) - new Date(b.due_date);
                        case 'progress':
                            return b.progress - a.progress;
                        case 'created_at':
                        default:
                            return new Date(b.created_at) - new Date(a.created_at);
                    }
                });
            }
            
            // 渲染所有内容
            renderAll() {
                this.renderTasks();
                this.renderStats();
            }
            
            // 渲染任务列表
            renderTasks() {
                const container = document.getElementById('tasksContainer');
                
                if (this.filteredTasks.length === 0) {
                    container.innerHTML = `
                        <div style="text-align: center; padding: 3rem; color: var(--text-secondary);">
                            <div style="font-size: 3rem; margin-bottom: 1rem;">📝</div>
                            <h3>暂无任务</h3>
                            <p>点击"新建任务"开始创建第一个任务</p>
                        </div>
                    `;
                    return;
                }
                
                container.innerHTML = this.filteredTasks.map(task => this.createTaskCard(task)).join('');
            }
            
            // 创建任务卡片
            createTaskCard(task) {
                const { 
                    id, title, description, status, priority, category, 
                    assignee, due_date, created_at, tags, progress 
                } = task;
                
                const user = this.users.find(u => u.name === assignee);
                const avatar = user ? user.avatar : '👤';
                
                const statusBadge = this.getStatusBadge(status);
                const priorityBadge = this.getPriorityBadge(priority);
                const dueDateFormatted = this.formatDate(due_date);
                const isOverdue = new Date(due_date) < new Date() && status !== 'completed';
                
                return `
                    <div class="task-card" data-task-id="${id}">
                        <div class="task-header">
                            <div>
                                <h3 class="task-title">${title}</h3>
                                <div class="task-meta">
                                    <span>${avatar} ${assignee}</span>
                                    <span>📅 ${dueDateFormatted}</span>
                                    ${isOverdue ? '<span style="color: var(--danger-color);">⚠️ 已逾期</span>' : ''}
                                </div>
                            </div>
                            <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                                ${statusBadge}
                                ${priorityBadge}
                            </div>
                        </div>
                        
                        <p class="task-description">${description}</p>
                        
                        <div class="task-tags">
                            ${tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                        </div>
                        
                        <div class="task-progress">
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: ${progress}%"></div>
                            </div>
                            <div class="progress-text">进度: ${progress}%</div>
                        </div>
                        
                        <div class="task-actions">
                            <button class="btn btn-primary btn-sm" onclick="taskManager.editTask(${id})">
                                ✏️ 编辑
                            </button>
                            <button class="btn btn-secondary btn-sm" onclick="taskManager.toggleStatus(${id})">
                                ${status === 'completed' ? '↩️ 重新开始' : '✅ 完成'}
                            </button>
                            <button class="btn btn-danger btn-sm" onclick="taskManager.deleteTask(${id})">
                                🗑️ 删除
                            </button>
                        </div>
                    </div>
                `;
            }
            
            // 获取状态徽章
            getStatusBadge(status) {
                const badges = {
                    pending: '<span class="badge badge-pending">待处理</span>',
                    in_progress: '<span class="badge badge-in-progress">进行中</span>',
                    completed: '<span class="badge badge-completed">已完成</span>'
                };
                return badges[status] || '';
            }
            
            // 获取优先级徽章
            getPriorityBadge(priority) {
                const badges = {
                    low: '<span class="badge badge-low">低</span>',
                    medium: '<span class="badge badge-medium">中</span>',
                    high: '<span class="badge badge-high">高</span>',
                    urgent: '<span class="badge badge-urgent">紧急</span>'
                };
                return badges[priority] || '';
            }
            
            // 格式化日期
            formatDate(dateString) {
                const date = new Date(dateString);
                const now = new Date();
                const diffTime = date - now;
                const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
                
                if (diffDays === 0) return '今天';
                if (diffDays === 1) return '明天';
                if (diffDays === -1) return '昨天';
                if (diffDays > 0) return `${diffDays}天后`;
                if (diffDays < 0) return `${Math.abs(diffDays)}天前`;
                
                return date.toLocaleDateString('zh-CN');
            }
            
            // 渲染统计信息
            renderStats() {
                const stats = this.calculateStats();
                const container = document.getElementById('statsContainer');
                
                container.innerHTML = `
                    <div class="stat-card">
                        <div class="stat-number" style="color: var(--primary-color);">${stats.total}</div>
                        <div class="stat-label">总任务数</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" style="color: var(--warning-color);">${stats.pending}</div>
                        <div class="stat-label">待处理</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" style="color: var(--info-color);">${stats.inProgress}</div>
                        <div class="stat-label">进行中</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" style="color: var(--success-color);">${stats.completed}</div>
                        <div class="stat-label">已完成</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" style="color: var(--danger-color);">${stats.overdue}</div>
                        <div class="stat-label">已逾期</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" style="color: var(--secondary-color);">${stats.avgProgress}%</div>
                        <div class="stat-label">平均进度</div>
                    </div>
                `;
            }
            
            // 计算统计信息
            calculateStats() {
                const now = new Date();
                
                const stats = this.filteredTasks.reduce((acc, task) => {
                    acc.total++;
                    
                    switch (task.status) {
                        case 'pending':
                            acc.pending++;
                            break;
                        case 'in_progress':
                            acc.inProgress++;
                            break;
                        case 'completed':
                            acc.completed++;
                            break;
                    }
                    
                    if (new Date(task.due_date) < now && task.status !== 'completed') {
                        acc.overdue++;
                    }
                    
                    acc.totalProgress += task.progress;
                    
                    return acc;
                }, {
                    total: 0,
                    pending: 0,
                    inProgress: 0,
                    completed: 0,
                    overdue: 0,
                    totalProgress: 0
                });
                
                stats.avgProgress = stats.total > 0 ? Math.round(stats.totalProgress / stats.total) : 0;
                
                return stats;
            }
            
            // 打开创建模态框
            openCreateModal() {
                this.currentEditId = null;
                document.getElementById('modalTitle').textContent = '新建任务';
                document.getElementById('taskForm').reset();
                document.getElementById('taskProgress').value = 0;
                document.getElementById('progressText').textContent = '0%';
                document.getElementById('taskModal').classList.add('show');
            }
            
            // 编辑任务
            editTask(id) {
                const task = this.tasks.find(t => t.id === id);
                if (!task) return;
                
                this.currentEditId = id;
                document.getElementById('modalTitle').textContent = '编辑任务';
                
                // 填充表单
                document.getElementById('taskId').value = task.id;
                document.getElementById('taskTitle').value = task.title;
                document.getElementById('taskDescription').value = task.description;
                document.getElementById('taskPriority').value = task.priority;
                document.getElementById('taskCategory').value = task.category;
                document.getElementById('taskAssignee').value = task.assignee;
                document.getElementById('taskDueDate').value = new Date(task.due_date).toISOString().slice(0, 16);
                document.getElementById('taskTags').value = task.tags.join(', ');
                document.getElementById('taskProgress').value = task.progress;
                document.getElementById('progressText').textContent = `${task.progress}%`;
                
                document.getElementById('taskModal').classList.add('show');
            }
            
            // 关闭模态框
            closeModal() {
                document.getElementById('taskModal').classList.remove('show');
                this.currentEditId = null;
            }
            
            // 处理表单提交
            async handleSubmit(e) {
                e.preventDefault();
                
                const submitBtn = document.getElementById('submitText');
                const spinner = document.getElementById('submitSpinner');
                
                // 显示加载状态
                submitBtn.classList.add('hidden');
                spinner.classList.remove('hidden');
                
                try {
                    const formData = this.getFormData();
                    
                    if (this.currentEditId) {
                        await this.updateTask(this.currentEditId, formData);
                    } else {
                        await this.createTask(formData);
                    }
                    
                    this.closeModal();
                    await this.refreshTasks();
                    
                    this.showNotification(
                        this.currentEditId ? '任务更新成功！' : '任务创建成功！',
                        'success'
                    );
                    
                } catch (error) {
                    console.error('提交失败:', error);
                    this.showNotification('操作失败，请重试', 'error');
                } finally {
                    // 恢复按钮状态
                    submitBtn.classList.remove('hidden');
                    spinner.classList.add('hidden');
                }
            }
            
            // 获取表单数据
            getFormData() {
                const tags = document.getElementById('taskTags').value
                    .split(',')
                    .map(tag => tag.trim())
                    .filter(tag => tag.length > 0);
                
                return {
                    title: document.getElementById('taskTitle').value,
                    description: document.getElementById('taskDescription').value,
                    priority: document.getElementById('taskPriority').value,
                    category: document.getElementById('taskCategory').value,
                    assignee: document.getElementById('taskAssignee').value,
                    due_date: new Date(document.getElementById('taskDueDate').value).toISOString(),
                    tags,
                    progress: parseInt(document.getElementById('taskProgress').value)
                };
            }
            
            // 创建任务
            async createTask(taskData) {
                const response = await this.fetchWithRetry('/api/tasks', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(taskData)
                });
                
                return response.json();
            }
            
            // 更新任务
            async updateTask(id, taskData) {
                const response = await this.fetchWithRetry(`/api/tasks/${id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(taskData)
                });
                
                return response.json();
            }
            
            // 切换任务状态
            async toggleStatus(id) {
                try {
                    const response = await this.fetchWithRetry(`/api/tasks/${id}/toggle`, {
                        method: 'POST'
                    });
                    
                    const result = await response.json();
                    
                    // 更新本地数据
                    const taskIndex = this.tasks.findIndex(t => t.id === id);
                    if (taskIndex !== -1) {
                        this.tasks[taskIndex] = { ...this.tasks[taskIndex], ...result.task };
                        this.filterTasks();
                    }
                    
                    this.showNotification('任务状态更新成功！', 'success');
                    
                } catch (error) {
                    console.error('状态切换失败:', error);
                    this.showNotification('状态更新失败，请重试', 'error');
                }
            }
            
            // 删除任务
            async deleteTask(id) {
                if (!confirm('确定要删除这个任务吗？此操作不可撤销。')) {
                    return;
                }
                
                try {
                    await this.fetchWithRetry(`/api/tasks/${id}`, {
                        method: 'DELETE'
                    });
                    
                    // 从本地数据中移除
                    this.tasks = this.tasks.filter(t => t.id !== id);
                    this.filterTasks();
                    
                    this.showNotification('任务删除成功！', 'success');
                    
                } catch (error) {
                    console.error('删除失败:', error);
                    this.showNotification('删除失败，请重试', 'error');
                }
            }
            
            // 刷新任务列表
            async refreshTasks() {
                const refreshText = document.getElementById('refreshText');
                const refreshSpinner = document.getElementById('refreshSpinner');
                
                refreshText.classList.add('hidden');
                refreshSpinner.classList.remove('hidden');
                
                try {
                    const response = await this.fetchWithRetry('/api/tasks');
                    const data = await response.json();
                    
                    this.tasks = data.tasks || [];
                    this.filterTasks();
                    
                    this.showNotification('任务列表已刷新！', 'info');
                    
                } catch (error) {
                    console.error('刷新失败:', error);
                    this.showNotification('刷新失败，请重试', 'error');
                } finally {
                    refreshText.classList.remove('hidden');
                    refreshSpinner.classList.add('hidden');
                }
            }
            
            // 导出任务
            exportTasks() {
                try {
                    const exportData = {
                        exported_at: new Date().toISOString(),
                        total_tasks: this.filteredTasks.length,
                        tasks: this.filteredTasks.map(task => ({
                            ...task,
                            assignee_info: this.users.find(u => u.name === task.assignee)
                        }))
                    };
                    
                    const dataStr = JSON.stringify(exportData, null, 2);
                    const dataBlob = new Blob([dataStr], { type: 'application/json' });
                    const url = URL.createObjectURL(dataBlob);
                    
                    const link = document.createElement('a');
                    link.href = url;
                    link.download = `tasks_export_${new Date().toISOString().split('T')[0]}.json`;
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    
                    URL.revokeObjectURL(url);
                    
                    this.showNotification('任务数据导出成功！', 'success');
                    
                } catch (error) {
                    console.error('导出失败:', error);
                    this.showNotification('导出失败，请重试', 'error');
                }
            }
            
            // 开始实时更新
            startRealtimeUpdates() {
                // 模拟实时更新
                setInterval(async () => {
                    try {
                        const response = await fetch('/api/realtime');
                        const data = await response.json();
                        
                        if (data.updates && data.updates.length > 0) {
                            this.handleRealtimeUpdate(data.updates);
                        }
                    } catch (error) {
                        // 静默处理实时更新错误
                        console.warn('实时更新失败:', error);
                    }
                }, 30000); // 每30秒检查一次
            }
            
            // 处理实时更新
            handleRealtimeUpdate(updates) {
                let hasChanges = false;
                
                updates.forEach(update => {
                    const { type, task_id, data } = update;
                    
                    switch (type) {
                        case 'task_updated':
                            const taskIndex = this.tasks.findIndex(t => t.id === task_id);
                            if (taskIndex !== -1) {
                                this.tasks[taskIndex] = { ...this.tasks[taskIndex], ...data };
                                hasChanges = true;
                            }
                            break;
                            
                        case 'task_created':
                            if (!this.tasks.find(t => t.id === data.id)) {
                                this.tasks.push(data);
                                hasChanges = true;
                            }
                            break;
                            
                        case 'task_deleted':
                            const deleteIndex = this.tasks.findIndex(t => t.id === task_id);
                            if (deleteIndex !== -1) {
                                this.tasks.splice(deleteIndex, 1);
                                hasChanges = true;
                            }
                            break;
                    }
                });
                
                if (hasChanges) {
                    this.filterTasks();
                    this.showNotification('任务数据已更新', 'info');
                }
            }
            
            // 显示通知
            showNotification(message, type = 'info') {
                const notification = document.createElement('div');
                notification.className = `notification ${type}`;
                notification.innerHTML = `
                    <div style="font-weight: 600; margin-bottom: 0.25rem;">
                        ${type === 'success' ? '✅' : type === 'error' ? '❌' : type === 'warning' ? '⚠️' : 'ℹ️'}
                        ${type === 'success' ? '成功' : type === 'error' ? '错误' : type === 'warning' ? '警告' : '信息'}
                    </div>
                    <div>${message}</div>
                `;
                
                document.body.appendChild(notification);
                
                // 自动移除
                setTimeout(() => {
                    notification.style.animation = 'slideOutRight 0.3s ease-out';
                    setTimeout(() => {
                        if (notification.parentNode) {
                            notification.parentNode.removeChild(notification);
                        }
                    }, 300);
                }, 3000);
            }
        }
        
        // 创建全局实例
        let taskManager;
        
        // DOM加载完成后初始化
        document.addEventListener('DOMContentLoaded', () => {
            taskManager = new TaskManager();
        });
    </script>
</body>
</html>
"""

# Flask路由
@app.route('/')
def index():
    """主页路由"""
    return render_template_string(SOLUTION_TEMPLATE)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """获取任务列表"""
    try:
        # 模拟数据库查询延迟
        time.sleep(0.1)
        
        return jsonify({
            'success': True,
            'tasks': tasks_db,
            'total': len(tasks_db)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """创建新任务"""
    try:
        data = request.get_json()
        
        # 验证必需字段
        required_fields = ['title', 'priority', 'category', 'assignee', 'due_date']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'缺少必需字段: {field}'
                }), 400
        
        # 创建新任务
        new_task = {
            'id': max([t['id'] for t in tasks_db], default=0) + 1,
            'title': data['title'],
            'description': data.get('description', ''),
            'status': 'pending',
            'priority': data['priority'],
            'category': data['category'],
            'assignee': data['assignee'],
            'due_date': data['due_date'],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'tags': data.get('tags', []),
            'progress': data.get('progress', 0)
        }
        
        tasks_db.append(new_task)
        
        return jsonify({
            'success': True,
            'task': new_task,
            'message': '任务创建成功'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """更新任务"""
    try:
        task = next((t for t in tasks_db if t['id'] == task_id), None)
        if not task:
            return jsonify({
                'success': False,
                'error': '任务不存在'
            }), 404
        
        data = request.get_json()
        
        # 更新任务字段
        updatable_fields = [
            'title', 'description', 'priority', 'category', 
            'assignee', 'due_date', 'tags', 'progress'
        ]
        
        for field in updatable_fields:
            if field in data:
                task[field] = data[field]
        
        task['updated_at'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'task': task,
            'message': '任务更新成功'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """删除任务"""
    try:
        global tasks_db
        task = next((t for t in tasks_db if t['id'] == task_id), None)
        if not task:
            return jsonify({
                'success': False,
                'error': '任务不存在'
            }), 404
        
        tasks_db = [t for t in tasks_db if t['id'] != task_id]
        
        return jsonify({
            'success': True,
            'message': '任务删除成功'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task_status(task_id):
    """切换任务状态"""
    try:
        task = next((t for t in tasks_db if t['id'] == task_id), None)
        if not task:
            return jsonify({
                'success': False,
                'error': '任务不存在'
            }), 404
        
        # 状态切换逻辑
        if task['status'] == 'completed':
            task['status'] = 'pending'
            task['progress'] = 0
        elif task['status'] == 'pending':
            task['status'] = 'in_progress'
            task['progress'] = 50
        else:  # in_progress
            task['status'] = 'completed'
            task['progress'] = 100
        
        task['updated_at'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'task': task,
            'message': '任务状态更新成功'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    """获取用户列表"""
    try:
        return jsonify({
            'success': True,
            'users': users_db,
            'total': len(users_db)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/realtime', methods=['GET'])
def get_realtime_updates():
    """获取实时更新（模拟）"""
    try:
        # 模拟随机更新
        updates = []
        
        if random.random() < 0.3:  # 30%概率有更新
            if tasks_db:
                task = random.choice(tasks_db)
                updates.append({
                    'type': 'task_updated',
                    'task_id': task['id'],
                    'data': {
                        'updated_at': datetime.now().isoformat()
                    },
                    'timestamp': datetime.now().isoformat()
                })
        
        return jsonify({
            'success': True,
            'updates': updates,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Session19 练习2解决方案：JavaScript ES6+和AJAX技术")
    print("="*60)
    print("\n📋 功能特性:")
    print("  • ES6+类和现代语法")
    print("  • async/await异步编程")
    print("  • Fetch API和错误处理")
    print("  • 实时数据更新")
    print("  • 响应式设计")
    print("  • 任务管理系统")
    print("\n🌐 访问地址: http://localhost:5000")
    print("\n💡 技术要点:")
    print("  • 解构赋值和模板字符串")
    print("  • 箭头函数和高阶函数")
    print("  • Promise和错误处理")
    print("  • 防抖和节流")
    print("  • 模块化代码组织")
    print("\n" + "="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
            }