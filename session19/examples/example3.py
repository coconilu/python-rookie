#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session19 示例3：JavaScript ES6+和AJAX示例

本示例演示了现代JavaScript语法特性和AJAX异步编程，
包括ES6+语法、Promise、async/await、Fetch API等。

作者: Python教程团队
创建日期: 2024-12-24
"""

from flask import Flask, render_template_string, request, jsonify
import json
import time
import random
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'js-ajax-example-key'

# 模拟数据存储
users_data = [
    {'id': 1, 'name': '张三', 'email': 'zhangsan@example.com', 'age': 25, 'city': '北京'},
    {'id': 2, 'name': '李四', 'email': 'lisi@example.com', 'age': 30, 'city': '上海'},
    {'id': 3, 'name': '王五', 'email': 'wangwu@example.com', 'age': 28, 'city': '广州'},
    {'id': 4, 'name': '赵六', 'email': 'zhaoliu@example.com', 'age': 32, 'city': '深圳'},
    {'id': 5, 'name': '钱七', 'email': 'qianqi@example.com', 'age': 27, 'city': '杭州'},
]

posts_data = [
    {'id': 1, 'title': 'JavaScript ES6新特性', 'content': '箭头函数、解构赋值、模板字符串等...', 'author': '张三', 'date': '2024-12-20'},
    {'id': 2, 'title': 'Promise和async/await', 'content': '异步编程的现代解决方案...', 'author': '李四', 'date': '2024-12-21'},
    {'id': 3, 'title': 'Fetch API详解', 'content': '现代浏览器的网络请求API...', 'author': '王五', 'date': '2024-12-22'},
]

# JavaScript和AJAX示例模板
JS_AJAX_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JavaScript ES6+和AJAX示例</title>
    <style>
        :root {
            --primary-color: #4f46e5;
            --secondary-color: #7c3aed;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --error-color: #ef4444;
            --text-color: #1f2937;
            --text-light: #6b7280;
            --bg-color: #f9fafb;
            --white: #ffffff;
            --border-color: #e5e7eb;
            --shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
            --border-radius: 8px;
            --transition: all 0.3s ease;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Microsoft YaHei', 'Segoe UI', system-ui, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: var(--bg-color);
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 2rem;
            border-radius: var(--border-radius);
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        
        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .section {
            background: var(--white);
            padding: 2rem;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            margin-bottom: 2rem;
        }
        
        .section h2 {
            color: var(--primary-color);
            margin-bottom: 1rem;
            font-size: 1.8rem;
        }
        
        .section h3 {
            color: var(--text-color);
            margin: 1.5rem 0 1rem 0;
            font-size: 1.3rem;
        }
        
        .code-block {
            background: #f8fafc;
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            padding: 1rem;
            margin: 1rem 0;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.9rem;
            overflow-x: auto;
        }
        
        .btn {
            display: inline-block;
            padding: 0.75rem 1.5rem;
            background: var(--primary-color);
            color: white;
            border: none;
            border-radius: var(--border-radius);
            cursor: pointer;
            text-decoration: none;
            font-size: 0.9rem;
            transition: var(--transition);
            margin: 0.25rem;
        }
        
        .btn:hover {
            background: var(--secondary-color);
            transform: translateY(-1px);
        }
        
        .btn-success {
            background: var(--success-color);
        }
        
        .btn-warning {
            background: var(--warning-color);
        }
        
        .btn-error {
            background: var(--error-color);
        }
        
        .form-group {
            margin-bottom: 1rem;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        
        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            font-size: 0.9rem;
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin: 1rem 0;
        }
        
        .card {
            background: var(--white);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            padding: 1.5rem;
            transition: var(--transition);
        }
        
        .card:hover {
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
        }
        
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid var(--primary-color);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .alert {
            padding: 1rem;
            border-radius: var(--border-radius);
            margin: 1rem 0;
        }
        
        .alert-success {
            background: #d1fae5;
            border: 1px solid #10b981;
            color: #065f46;
        }
        
        .alert-error {
            background: #fee2e2;
            border: 1px solid #ef4444;
            color: #991b1b;
        }
        
        .alert-info {
            background: #dbeafe;
            border: 1px solid #3b82f6;
            color: #1e40af;
        }
        
        .hidden {
            display: none;
        }
        
        .fade-in {
            animation: fadeIn 0.5s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .user-card {
            border-left: 4px solid var(--primary-color);
        }
        
        .post-card {
            border-left: 4px solid var(--success-color);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }
        
        .stat-card {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 1.5rem;
            border-radius: var(--border-radius);
            text-align: center;
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .stat-label {
            font-size: 0.9rem;
            opacity: 0.9;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .grid {
                grid-template-columns: 1fr;
            }
            
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- 页面头部 -->
        <header class="header">
            <h1>JavaScript ES6+ 和 AJAX 示例</h1>
            <p>现代JavaScript语法特性和异步编程技术演示</p>
        </header>
        
        <!-- ES6+语法示例 -->
        <section class="section">
            <h2>🚀 ES6+ 语法特性演示</h2>
            
            <h3>1. 箭头函数和解构赋值</h3>
            <div class="code-block">
// 箭头函数
const add = (a, b) => a + b;
const multiply = (x, y) => {
    const result = x * y;
    return result;
};

// 解构赋值
const user = { name: '张三', age: 25, city: '北京' };
const { name, age } = user;
const [first, second] = [1, 2, 3];
            </div>
            <button class="btn" onclick="demonstrateES6Syntax()">运行ES6语法示例</button>
            
            <h3>2. 模板字符串和默认参数</h3>
            <div class="code-block">
// 模板字符串
const greeting = (name, age = 18) => {
    return `你好，${name}！你今年${age}岁了。`;
};

// 默认参数
const createUser = (name, role = 'user') => ({ name, role });
            </div>
            <button class="btn" onclick="demonstrateTemplateStrings()">运行模板字符串示例</button>
            
            <h3>3. Promise和async/await</h3>
            <div class="code-block">
// Promise
const fetchData = () => {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve('数据获取成功！');
        }, 1000);
    });
};

// async/await
const getData = async () => {
    try {
        const result = await fetchData();
        console.log(result);
    } catch (error) {
        console.error('错误:', error);
    }
};
            </div>
            <button class="btn" onclick="demonstrateAsyncAwait()">运行异步示例</button>
            
            <div id="es6-results" class="alert alert-info hidden">
                <h4>运行结果：</h4>
                <div id="es6-output"></div>
            </div>
        </section>
        
        <!-- AJAX和Fetch API示例 -->
        <section class="section">
            <h2>🌐 AJAX 和 Fetch API 演示</h2>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number" id="users-count">0</div>
                    <div class="stat-label">用户总数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="posts-count">0</div>
                    <div class="stat-label">文章总数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="requests-count">0</div>
                    <div class="stat-label">请求次数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="response-time">0ms</div>
                    <div class="stat-label">平均响应时间</div>
                </div>
            </div>
            
            <h3>数据获取操作</h3>
            <div style="margin: 1rem 0;">
                <button class="btn" onclick="fetchUsers()">获取用户列表</button>
                <button class="btn" onclick="fetchPosts()">获取文章列表</button>
                <button class="btn btn-success" onclick="fetchUserById()">获取指定用户</button>
                <button class="btn btn-warning" onclick="simulateError()">模拟错误请求</button>
                <button class="btn btn-error" onclick="clearResults()">清空结果</button>
            </div>
            
            <div id="loading" class="hidden">
                <div class="loading"></div> 正在加载数据...
            </div>
            
            <div id="ajax-results"></div>
        </section>
        
        <!-- 表单提交示例 -->
        <section class="section">
            <h2>📝 表单提交和数据处理</h2>
            
            <div class="grid">
                <div>
                    <h3>添加新用户</h3>
                    <form id="user-form">
                        <div class="form-group">
                            <label for="user-name">姓名：</label>
                            <input type="text" id="user-name" name="name" required>
                        </div>
                        <div class="form-group">
                            <label for="user-email">邮箱：</label>
                            <input type="email" id="user-email" name="email" required>
                        </div>
                        <div class="form-group">
                            <label for="user-age">年龄：</label>
                            <input type="number" id="user-age" name="age" min="1" max="120">
                        </div>
                        <div class="form-group">
                            <label for="user-city">城市：</label>
                            <select id="user-city" name="city">
                                <option value="北京">北京</option>
                                <option value="上海">上海</option>
                                <option value="广州">广州</option>
                                <option value="深圳">深圳</option>
                                <option value="杭州">杭州</option>
                            </select>
                        </div>
                        <button type="submit" class="btn">添加用户</button>
                    </form>
                </div>
                
                <div>
                    <h3>发布新文章</h3>
                    <form id="post-form">
                        <div class="form-group">
                            <label for="post-title">标题：</label>
                            <input type="text" id="post-title" name="title" required>
                        </div>
                        <div class="form-group">
                            <label for="post-content">内容：</label>
                            <textarea id="post-content" name="content" rows="4" required></textarea>
                        </div>
                        <div class="form-group">
                            <label for="post-author">作者：</label>
                            <input type="text" id="post-author" name="author" required>
                        </div>
                        <button type="submit" class="btn">发布文章</button>
                    </form>
                </div>
            </div>
            
            <div id="form-results"></div>
        </section>
        
        <!-- 实时数据更新示例 -->
        <section class="section">
            <h2>⚡ 实时数据更新</h2>
            
            <div style="margin: 1rem 0;">
                <button class="btn" onclick="startRealTimeUpdates()">开始实时更新</button>
                <button class="btn btn-warning" onclick="stopRealTimeUpdates()">停止更新</button>
                <button class="btn btn-success" onclick="fetchRealTimeData()">手动刷新</button>
            </div>
            
            <div id="realtime-status" class="alert alert-info">
                实时更新状态：已停止
            </div>
            
            <div id="realtime-data"></div>
        </section>
    </div>
    
    <script>
        // ES6+ 语法演示
        class DataManager {
            constructor() {
                this.requestCount = 0;
                this.responseTimes = [];
                this.realTimeInterval = null;
            }
            
            // 箭头函数和解构赋值
            demonstrateES6() {
                const users = [
                    { name: '张三', age: 25, skills: ['JavaScript', 'Python'] },
                    { name: '李四', age: 30, skills: ['Java', 'Go'] },
                    { name: '王五', age: 28, skills: ['React', 'Vue'] }
                ];
                
                // 使用map和解构
                const userInfo = users.map(({ name, age, skills }) => {
                    const [primarySkill, ...otherSkills] = skills;
                    return `${name}(${age}岁) - 主要技能: ${primarySkill}`;
                });
                
                return userInfo;
            }
            
            // 模板字符串和默认参数
            createGreeting(name, age = 18, city = '未知') {
                return `你好，${name}！你今年${age}岁，来自${city}。`;
            }
            
            // Promise封装的AJAX请求
            async fetchData(url, options = {}) {
                const startTime = Date.now();
                this.requestCount++;
                
                try {
                    const response = await fetch(url, {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        ...options
                    });
                    
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    }
                    
                    const data = await response.json();
                    const responseTime = Date.now() - startTime;
                    this.responseTimes.push(responseTime);
                    
                    this.updateStats();
                    return data;
                } catch (error) {
                    const responseTime = Date.now() - startTime;
                    this.responseTimes.push(responseTime);
                    this.updateStats();
                    throw error;
                }
            }
            
            // 更新统计信息
            updateStats() {
                document.getElementById('requests-count').textContent = this.requestCount;
                
                if (this.responseTimes.length > 0) {
                    const avgTime = Math.round(
                        this.responseTimes.reduce((a, b) => a + b, 0) / this.responseTimes.length
                    );
                    document.getElementById('response-time').textContent = `${avgTime}ms`;
                }
            }
            
            // 显示结果的通用方法
            displayResults(containerId, data, type = 'success') {
                const container = document.getElementById(containerId);
                const alertClass = type === 'error' ? 'alert-error' : 'alert-success';
                
                let html = `<div class="alert ${alertClass} fade-in">`;
                
                if (typeof data === 'string') {
                    html += data;
                } else if (Array.isArray(data)) {
                    html += '<div class="grid">';
                    data.forEach(item => {
                        const cardClass = type === 'users' ? 'user-card' : 'post-card';
                        html += `<div class="card ${cardClass}">`;
                        
                        if (type === 'users') {
                            html += `
                                <h4>${item.name}</h4>
                                <p><strong>邮箱：</strong>${item.email}</p>
                                <p><strong>年龄：</strong>${item.age}岁</p>
                                <p><strong>城市：</strong>${item.city}</p>
                            `;
                        } else if (type === 'posts') {
                            html += `
                                <h4>${item.title}</h4>
                                <p>${item.content}</p>
                                <p><strong>作者：</strong>${item.author}</p>
                                <p><strong>日期：</strong>${item.date}</p>
                            `;
                        }
                        
                        html += '</div>';
                    });
                    html += '</div>';
                } else {
                    html += `<pre>${JSON.stringify(data, null, 2)}</pre>`;
                }
                
                html += '</div>';
                container.innerHTML = html;
            }
            
            // 显示加载状态
            showLoading(show = true) {
                const loading = document.getElementById('loading');
                if (show) {
                    loading.classList.remove('hidden');
                } else {
                    loading.classList.add('hidden');
                }
            }
        }
        
        // 创建数据管理器实例
        const dataManager = new DataManager();
        
        // ES6语法演示函数
        function demonstrateES6Syntax() {
            const results = dataManager.demonstrateES6();
            const output = document.getElementById('es6-output');
            const container = document.getElementById('es6-results');
            
            output.innerHTML = `
                <h5>解构赋值和箭头函数结果：</h5>
                <ul>
                    ${results.map(item => `<li>${item}</li>`).join('')}
                </ul>
            `;
            
            container.classList.remove('hidden');
        }
        
        function demonstrateTemplateStrings() {
            const greetings = [
                dataManager.createGreeting('张三', 25, '北京'),
                dataManager.createGreeting('李四', undefined, '上海'),
                dataManager.createGreeting('王五')
            ];
            
            const output = document.getElementById('es6-output');
            const container = document.getElementById('es6-results');
            
            output.innerHTML = `
                <h5>模板字符串和默认参数结果：</h5>
                <ul>
                    ${greetings.map(greeting => `<li>${greeting}</li>`).join('')}
                </ul>
            `;
            
            container.classList.remove('hidden');
        }
        
        async function demonstrateAsyncAwait() {
            const output = document.getElementById('es6-output');
            const container = document.getElementById('es6-results');
            
            output.innerHTML = '<p>正在执行异步操作...</p>';
            container.classList.remove('hidden');
            
            try {
                // 模拟异步操作
                const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));
                
                await delay(1000);
                const result1 = '第一个异步操作完成';
                
                await delay(500);
                const result2 = '第二个异步操作完成';
                
                await delay(300);
                const result3 = '所有异步操作完成';
                
                output.innerHTML = `
                    <h5>async/await 执行结果：</h5>
                    <ul>
                        <li>✅ ${result1}</li>
                        <li>✅ ${result2}</li>
                        <li>✅ ${result3}</li>
                    </ul>
                    <p><strong>总耗时：</strong>约1.8秒</p>
                `;
            } catch (error) {
                output.innerHTML = `<p style="color: red;">错误: ${error.message}</p>`;
            }
        }
        
        // AJAX请求函数
        async function fetchUsers() {
            dataManager.showLoading(true);
            
            try {
                const data = await dataManager.fetchData('/api/users');
                document.getElementById('users-count').textContent = data.users.length;
                dataManager.displayResults('ajax-results', data.users, 'users');
            } catch (error) {
                dataManager.displayResults('ajax-results', `获取用户失败: ${error.message}`, 'error');
            } finally {
                dataManager.showLoading(false);
            }
        }
        
        async function fetchPosts() {
            dataManager.showLoading(true);
            
            try {
                const data = await dataManager.fetchData('/api/posts');
                document.getElementById('posts-count').textContent = data.posts.length;
                dataManager.displayResults('ajax-results', data.posts, 'posts');
            } catch (error) {
                dataManager.displayResults('ajax-results', `获取文章失败: ${error.message}`, 'error');
            } finally {
                dataManager.showLoading(false);
            }
        }
        
        async function fetchUserById() {
            const userId = prompt('请输入用户ID (1-5):');
            if (!userId) return;
            
            dataManager.showLoading(true);
            
            try {
                const data = await dataManager.fetchData(`/api/users/${userId}`);
                dataManager.displayResults('ajax-results', [data.user], 'users');
            } catch (error) {
                dataManager.displayResults('ajax-results', `获取用户失败: ${error.message}`, 'error');
            } finally {
                dataManager.showLoading(false);
            }
        }
        
        async function simulateError() {
            dataManager.showLoading(true);
            
            try {
                await dataManager.fetchData('/api/nonexistent');
            } catch (error) {
                dataManager.displayResults('ajax-results', `模拟错误成功: ${error.message}`, 'error');
            } finally {
                dataManager.showLoading(false);
            }
        }
        
        function clearResults() {
            document.getElementById('ajax-results').innerHTML = '';
            document.getElementById('form-results').innerHTML = '';
            document.getElementById('realtime-data').innerHTML = '';
        }
        
        // 表单提交处理
        document.getElementById('user-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const userData = Object.fromEntries(formData.entries());
            
            try {
                const data = await dataManager.fetchData('/api/users', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(userData)
                });
                
                dataManager.displayResults('form-results', `用户添加成功: ${data.message}`);
                this.reset();
            } catch (error) {
                dataManager.displayResults('form-results', `添加用户失败: ${error.message}`, 'error');
            }
        });
        
        document.getElementById('post-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const postData = Object.fromEntries(formData.entries());
            postData.date = new Date().toISOString().split('T')[0];
            
            try {
                const data = await dataManager.fetchData('/api/posts', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(postData)
                });
                
                dataManager.displayResults('form-results', `文章发布成功: ${data.message}`);
                this.reset();
            } catch (error) {
                dataManager.displayResults('form-results', `发布文章失败: ${error.message}`, 'error');
            }
        });
        
        // 实时数据更新
        function startRealTimeUpdates() {
            if (dataManager.realTimeInterval) {
                clearInterval(dataManager.realTimeInterval);
            }
            
            document.getElementById('realtime-status').innerHTML = 
                '<div class="alert alert-success">实时更新状态：运行中 🟢</div>';
            
            dataManager.realTimeInterval = setInterval(fetchRealTimeData, 3000);
            fetchRealTimeData(); // 立即执行一次
        }
        
        function stopRealTimeUpdates() {
            if (dataManager.realTimeInterval) {
                clearInterval(dataManager.realTimeInterval);
                dataManager.realTimeInterval = null;
            }
            
            document.getElementById('realtime-status').innerHTML = 
                '<div class="alert alert-info">实时更新状态：已停止 🔴</div>';
        }
        
        async function fetchRealTimeData() {
            try {
                const data = await dataManager.fetchData('/api/realtime');
                
                const container = document.getElementById('realtime-data');
                container.innerHTML = `
                    <div class="card fade-in">
                        <h4>📊 实时数据</h4>
                        <p><strong>当前时间：</strong>${data.timestamp}</p>
                        <p><strong>随机数值：</strong>${data.randomValue}</p>
                        <p><strong>在线用户：</strong>${data.onlineUsers}</p>
                        <p><strong>系统状态：</strong><span style="color: ${data.status === 'healthy' ? 'green' : 'red'}">${data.status}</span></p>
                        <p><strong>更新次数：</strong>${data.updateCount}</p>
                    </div>
                `;
            } catch (error) {
                console.error('获取实时数据失败:', error);
            }
        }
        
        // 页面加载完成后初始化
        document.addEventListener('DOMContentLoaded', function() {
            console.log('JavaScript ES6+ 和 AJAX 示例已加载');
            console.log('功能包括：');
            console.log('- ES6+ 语法特性演示');
            console.log('- Promise 和 async/await');
            console.log('- Fetch API 和 AJAX 请求');
            console.log('- 表单提交和数据处理');
            console.log('- 实时数据更新');
            
            // 初始化统计数据
            dataManager.updateStats();
        });
    </script>
</body>
</html>
"""

# API路由
@app.route('/')
def index():
    """
    显示JavaScript和AJAX示例页面
    """
    return render_template_string(JS_AJAX_TEMPLATE)

@app.route('/api/users', methods=['GET', 'POST'])
def api_users():
    """
    用户API接口
    """
    if request.method == 'GET':
        # 模拟网络延迟
        time.sleep(0.5)
        return jsonify({
            'success': True,
            'users': users_data,
            'total': len(users_data)
        })
    
    elif request.method == 'POST':
        try:
            user_data = request.get_json()
            
            # 简单验证
            if not user_data.get('name') or not user_data.get('email'):
                return jsonify({
                    'success': False,
                    'message': '姓名和邮箱是必填项'
                }), 400
            
            # 添加新用户
            new_user = {
                'id': len(users_data) + 1,
                'name': user_data['name'],
                'email': user_data['email'],
                'age': int(user_data.get('age', 18)),
                'city': user_data.get('city', '未知')
            }
            
            users_data.append(new_user)
            
            # 模拟处理时间
            time.sleep(0.3)
            
            return jsonify({
                'success': True,
                'message': f'用户 {new_user["name"]} 添加成功',
                'user': new_user
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'添加用户失败: {str(e)}'
            }), 500

@app.route('/api/users/<int:user_id>')
def api_user_detail(user_id):
    """
    获取指定用户详情
    """
    # 模拟网络延迟
    time.sleep(0.3)
    
    user = next((u for u in users_data if u['id'] == user_id), None)
    
    if user:
        return jsonify({
            'success': True,
            'user': user
        })
    else:
        return jsonify({
            'success': False,
            'message': f'用户ID {user_id} 不存在'
        }), 404

@app.route('/api/posts', methods=['GET', 'POST'])
def api_posts():
    """
    文章API接口
    """
    if request.method == 'GET':
        # 模拟网络延迟
        time.sleep(0.4)
        return jsonify({
            'success': True,
            'posts': posts_data,
            'total': len(posts_data)
        })
    
    elif request.method == 'POST':
        try:
            post_data = request.get_json()
            
            # 简单验证
            if not post_data.get('title') or not post_data.get('content'):
                return jsonify({
                    'success': False,
                    'message': '标题和内容是必填项'
                }), 400
            
            # 添加新文章
            new_post = {
                'id': len(posts_data) + 1,
                'title': post_data['title'],
                'content': post_data['content'],
                'author': post_data.get('author', '匿名'),
                'date': post_data.get('date', datetime.now().strftime('%Y-%m-%d'))
            }
            
            posts_data.append(new_post)
            
            # 模拟处理时间
            time.sleep(0.2)
            
            return jsonify({
                'success': True,
                'message': f'文章 "{new_post["title"]}" 发布成功',
                'post': new_post
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'发布文章失败: {str(e)}'
            }), 500

@app.route('/api/realtime')
def api_realtime():
    """
    实时数据API接口
    """
    # 模拟实时数据
    data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'randomValue': random.randint(1, 100),
        'onlineUsers': random.randint(50, 200),
        'status': random.choice(['healthy', 'warning', 'healthy', 'healthy']),
        'updateCount': random.randint(1, 1000)
    }
    
    # 模拟网络延迟
    time.sleep(0.1)
    
    return jsonify({
        'success': True,
        **data
    })

@app.errorhandler(404)
def not_found(error):
    """
    404错误处理
    """
    return jsonify({
        'success': False,
        'message': '请求的资源不存在'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """
    500错误处理
    """
    return jsonify({
        'success': False,
        'message': '服务器内部错误'
    }), 500

def main():
    """
    主函数
    """
    print("Session19 示例3：JavaScript ES6+和AJAX示例")
    print("=" * 50)
    print("\n本示例展示了：")
    print("1. ES6+ 语法特性（箭头函数、解构赋值、模板字符串）")
    print("2. Promise 和 async/await 异步编程")
    print("3. Fetch API 和现代 AJAX 技术")
    print("4. 表单提交和数据验证")
    print("5. 实时数据更新和错误处理")
    print("\n可用的API接口：")
    print("- GET  /api/users - 获取用户列表")
    print("- POST /api/users - 添加新用户")
    print("- GET  /api/users/<id> - 获取指定用户")
    print("- GET  /api/posts - 获取文章列表")
    print("- POST /api/posts - 发布新文章")
    print("- GET  /api/realtime - 获取实时数据")
    print("\n访问 http://127.0.0.1:5000 查看示例")
    print("按 Ctrl+C 停止服务器")
    
    app.run(debug=True, host='127.0.0.1', port=5000)

if __name__ == '__main__':
    main()