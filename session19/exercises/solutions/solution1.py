#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session19 练习1解决方案：HTML5和CSS3基础

本文件提供练习1的完整解决方案，展示如何实现：
1. HTML5语义化标签的正确使用
2. CSS3现代布局技术（Flexbox、Grid）
3. 响应式设计和媒体查询
4. CSS变量和动画效果
5. JavaScript交互功能

作者: Python教程团队
创建日期: 2024-12-24
"""

from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'solution1-secret-key'

# 课程数据
courses_db = [
    {
        'id': 1,
        'title': 'Python全栈开发',
        'description': '从零开始学习Python Web开发，包括Flask、Django、数据库等',
        'instructor': '张老师',
        'duration': '12周',
        'price': 2999,
        'rating': 4.8,
        'students': 1250,
        'image': 'https://via.placeholder.com/300x200/3b82f6/ffffff?text=Python',
        'category': 'programming',
        'level': 'beginner',
        'tags': ['Python', 'Flask', 'Django', '全栈开发']
    },
    {
        'id': 2,
        'title': 'JavaScript现代开发',
        'description': '学习ES6+、React、Vue.js等现代JavaScript技术栈',
        'instructor': '李老师',
        'duration': '10周',
        'price': 2599,
        'rating': 4.9,
        'students': 980,
        'image': 'https://via.placeholder.com/300x200/f59e0b/ffffff?text=JavaScript',
        'category': 'programming',
        'level': 'intermediate',
        'tags': ['JavaScript', 'React', 'Vue.js', '前端开发']
    },
    {
        'id': 3,
        'title': 'UI/UX设计实战',
        'description': '掌握现代UI/UX设计原理和工具，创建优秀的用户体验',
        'instructor': '王老师',
        'duration': '8周',
        'price': 1999,
        'rating': 4.7,
        'students': 750,
        'image': 'https://via.placeholder.com/300x200/10b981/ffffff?text=UI%2FUX',
        'category': 'design',
        'level': 'beginner',
        'tags': ['UI设计', 'UX设计', 'Figma', '用户体验']
    },
    {
        'id': 4,
        'title': '数据科学与机器学习',
        'description': '学习数据分析、机器学习算法和深度学习技术',
        'instructor': '赵老师',
        'duration': '16周',
        'price': 3999,
        'rating': 4.9,
        'students': 650,
        'image': 'https://via.placeholder.com/300x200/ef4444/ffffff?text=Data+Science',
        'category': 'data-science',
        'level': 'advanced',
        'tags': ['数据科学', '机器学习', 'Python', 'TensorFlow']
    },
    {
        'id': 5,
        'title': '移动应用开发',
        'description': '使用React Native和Flutter开发跨平台移动应用',
        'instructor': '陈老师',
        'duration': '14周',
        'price': 3299,
        'rating': 4.6,
        'students': 520,
        'image': 'https://via.placeholder.com/300x200/8b5cf6/ffffff?text=Mobile+Dev',
        'category': 'mobile',
        'level': 'intermediate',
        'tags': ['移动开发', 'React Native', 'Flutter', '跨平台']
    },
    {
        'id': 6,
        'title': '云计算与DevOps',
        'description': '学习AWS、Docker、Kubernetes等云计算和DevOps技术',
        'instructor': '刘老师',
        'duration': '12周',
        'price': 3599,
        'rating': 4.8,
        'students': 420,
        'image': 'https://via.placeholder.com/300x200/06b6d4/ffffff?text=Cloud+%26+DevOps',
        'category': 'devops',
        'level': 'advanced',
        'tags': ['云计算', 'AWS', 'Docker', 'Kubernetes']
    }
]

# 报名数据
enrollments_db = []

# 解决方案模板
SOLUTION_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="在线学习平台 - 提供高质量的编程、设计、数据科学等课程">
    <meta name="keywords" content="在线学习,编程课程,设计课程,数据科学,技能提升">
    <title>TechEdu - 在线学习平台</title>
    
    <style>
        /* CSS变量定义 */
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
            --bg-overlay: rgba(0, 0, 0, 0.5);
            
            --border-color: #e5e7eb;
            --border-radius: 8px;
            --border-radius-lg: 12px;
            
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
            
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            --transition-fast: all 0.15s ease-in-out;
            
            --font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            --font-size-xs: 0.75rem;
            --font-size-sm: 0.875rem;
            --font-size-base: 1rem;
            --font-size-lg: 1.125rem;
            --font-size-xl: 1.25rem;
            --font-size-2xl: 1.5rem;
            --font-size-3xl: 1.875rem;
            --font-size-4xl: 2.25rem;
            
            --spacing-1: 0.25rem;
            --spacing-2: 0.5rem;
            --spacing-3: 0.75rem;
            --spacing-4: 1rem;
            --spacing-5: 1.25rem;
            --spacing-6: 1.5rem;
            --spacing-8: 2rem;
            --spacing-10: 2.5rem;
            --spacing-12: 3rem;
            --spacing-16: 4rem;
            --spacing-20: 5rem;
        }
        
        /* 基础样式重置 */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        html {
            scroll-behavior: smooth;
        }
        
        body {
            font-family: var(--font-family);
            font-size: var(--font-size-base);
            line-height: 1.6;
            color: var(--text-primary);
            background-color: var(--bg-primary);
            overflow-x: hidden;
        }
        
        /* 容器和布局 */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 var(--spacing-4);
        }
        
        .container-fluid {
            width: 100%;
            padding: 0 var(--spacing-4);
        }
        
        /* Flexbox工具类 */
        .flex {
            display: flex;
        }
        
        .flex-col {
            flex-direction: column;
        }
        
        .flex-wrap {
            flex-wrap: wrap;
        }
        
        .items-center {
            align-items: center;
        }
        
        .items-start {
            align-items: flex-start;
        }
        
        .items-end {
            align-items: flex-end;
        }
        
        .justify-center {
            justify-content: center;
        }
        
        .justify-between {
            justify-content: space-between;
        }
        
        .justify-around {
            justify-content: space-around;
        }
        
        .flex-1 {
            flex: 1;
        }
        
        /* Grid布局 */
        .grid {
            display: grid;
        }
        
        .grid-cols-1 {
            grid-template-columns: repeat(1, minmax(0, 1fr));
        }
        
        .grid-cols-2 {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
        
        .grid-cols-3 {
            grid-template-columns: repeat(3, minmax(0, 1fr));
        }
        
        .grid-cols-4 {
            grid-template-columns: repeat(4, minmax(0, 1fr));
        }
        
        .gap-4 {
            gap: var(--spacing-4);
        }
        
        .gap-6 {
            gap: var(--spacing-6);
        }
        
        .gap-8 {
            gap: var(--spacing-8);
        }
        
        /* 响应式Grid */
        .grid-responsive {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: var(--spacing-6);
        }
        
        /* 导航栏样式 */
        .navbar {
            background: var(--bg-primary);
            box-shadow: var(--shadow);
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            transition: var(--transition);
        }
        
        .navbar.scrolled {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            box-shadow: var(--shadow-lg);
        }
        
        .navbar-content {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: var(--spacing-4) 0;
        }
        
        .navbar-brand {
            font-size: var(--font-size-xl);
            font-weight: bold;
            color: var(--primary-color);
            text-decoration: none;
            transition: var(--transition);
        }
        
        .navbar-brand:hover {
            color: var(--secondary-color);
        }
        
        .navbar-nav {
            display: flex;
            list-style: none;
            gap: var(--spacing-6);
        }
        
        .nav-link {
            color: var(--text-primary);
            text-decoration: none;
            font-weight: 500;
            padding: var(--spacing-2) var(--spacing-3);
            border-radius: var(--border-radius);
            transition: var(--transition);
        }
        
        .nav-link:hover {
            color: var(--primary-color);
            background-color: rgba(59, 130, 246, 0.1);
        }
        
        .nav-link.active {
            color: var(--primary-color);
            background-color: rgba(59, 130, 246, 0.1);
        }
        
        /* 移动端菜单 */
        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            font-size: var(--font-size-xl);
            color: var(--text-primary);
            cursor: pointer;
        }
        
        /* Hero区域 */
        .hero {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: var(--text-white);
            padding: var(--spacing-20) 0 var(--spacing-16);
            margin-top: 80px;
            position: relative;
            overflow: hidden;
        }
        
        .hero::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="%23ffffff" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>') repeat;
            opacity: 0.3;
        }
        
        .hero-content {
            position: relative;
            z-index: 1;
            text-align: center;
            max-width: 800px;
            margin: 0 auto;
        }
        
        .hero-title {
            font-size: var(--font-size-4xl);
            font-weight: bold;
            margin-bottom: var(--spacing-6);
            animation: fadeInUp 1s ease-out;
        }
        
        .hero-subtitle {
            font-size: var(--font-size-xl);
            margin-bottom: var(--spacing-8);
            opacity: 0.9;
            animation: fadeInUp 1s ease-out 0.2s both;
        }
        
        .hero-cta {
            animation: fadeInUp 1s ease-out 0.4s both;
        }
        
        /* 按钮样式 */
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: var(--spacing-2);
            padding: var(--spacing-3) var(--spacing-6);
            font-size: var(--font-size-base);
            font-weight: 600;
            text-decoration: none;
            border: none;
            border-radius: var(--border-radius);
            cursor: pointer;
            transition: var(--transition);
            position: relative;
            overflow: hidden;
        }
        
        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s;
        }
        
        .btn:hover::before {
            left: 100%;
        }
        
        .btn-primary {
            background-color: var(--primary-color);
            color: var(--text-white);
        }
        
        .btn-primary:hover {
            background-color: #2563eb;
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }
        
        .btn-secondary {
            background-color: var(--secondary-color);
            color: var(--text-white);
        }
        
        .btn-secondary:hover {
            background-color: #059669;
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }
        
        .btn-outline {
            background-color: transparent;
            color: var(--primary-color);
            border: 2px solid var(--primary-color);
        }
        
        .btn-outline:hover {
            background-color: var(--primary-color);
            color: var(--text-white);
        }
        
        .btn-lg {
            padding: var(--spacing-4) var(--spacing-8);
            font-size: var(--font-size-lg);
        }
        
        .btn-sm {
            padding: var(--spacing-2) var(--spacing-4);
            font-size: var(--font-size-sm);
        }
        
        /* 卡片样式 */
        .card {
            background: var(--bg-primary);
            border-radius: var(--border-radius-lg);
            box-shadow: var(--shadow);
            overflow: hidden;
            transition: var(--transition);
            position: relative;
        }
        
        .card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-xl);
        }
        
        .card-image {
            width: 100%;
            height: 200px;
            object-fit: cover;
            transition: var(--transition);
        }
        
        .card:hover .card-image {
            transform: scale(1.05);
        }
        
        .card-content {
            padding: var(--spacing-6);
        }
        
        .card-title {
            font-size: var(--font-size-xl);
            font-weight: 600;
            margin-bottom: var(--spacing-3);
            color: var(--text-primary);
        }
        
        .card-description {
            color: var(--text-secondary);
            margin-bottom: var(--spacing-4);
            line-height: 1.6;
        }
        
        .card-meta {
            display: flex;
            align-items: center;
            gap: var(--spacing-4);
            margin-bottom: var(--spacing-4);
            font-size: var(--font-size-sm);
            color: var(--text-light);
        }
        
        .card-footer {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-top: var(--spacing-4);
            border-top: 1px solid var(--border-color);
        }
        
        /* 徽章样式 */
        .badge {
            display: inline-flex;
            align-items: center;
            padding: var(--spacing-1) var(--spacing-3);
            font-size: var(--font-size-xs);
            font-weight: 600;
            border-radius: 9999px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .badge-primary {
            background-color: rgba(59, 130, 246, 0.1);
            color: var(--primary-color);
        }
        
        .badge-success {
            background-color: rgba(16, 185, 129, 0.1);
            color: var(--success-color);
        }
        
        .badge-warning {
            background-color: rgba(245, 158, 11, 0.1);
            color: var(--warning-color);
        }
        
        .badge-danger {
            background-color: rgba(239, 68, 68, 0.1);
            color: var(--danger-color);
        }
        
        /* 标签样式 */
        .tag {
            display: inline-block;
            padding: var(--spacing-1) var(--spacing-2);
            font-size: var(--font-size-xs);
            background-color: var(--bg-secondary);
            color: var(--text-secondary);
            border-radius: var(--border-radius);
            margin-right: var(--spacing-2);
            margin-bottom: var(--spacing-1);
        }
        
        /* 评分样式 */
        .rating {
            display: flex;
            align-items: center;
            gap: var(--spacing-1);
        }
        
        .star {
            color: #fbbf24;
            font-size: var(--font-size-sm);
        }
        
        .star.empty {
            color: var(--border-color);
        }
        
        /* 价格样式 */
        .price {
            font-size: var(--font-size-xl);
            font-weight: bold;
            color: var(--primary-color);
        }
        
        .price-original {
            font-size: var(--font-size-base);
            color: var(--text-light);
            text-decoration: line-through;
            margin-left: var(--spacing-2);
        }
        
        /* 过滤器样式 */
        .filters {
            background: var(--bg-secondary);
            padding: var(--spacing-6) 0;
            margin-bottom: var(--spacing-8);
        }
        
        .filter-group {
            display: flex;
            flex-wrap: wrap;
            gap: var(--spacing-4);
            align-items: center;
        }
        
        .filter-label {
            font-weight: 600;
            color: var(--text-primary);
        }
        
        .filter-select {
            padding: var(--spacing-2) var(--spacing-4);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            background: var(--bg-primary);
            color: var(--text-primary);
            font-size: var(--font-size-sm);
            cursor: pointer;
            transition: var(--transition);
        }
        
        .filter-select:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        /* 搜索框样式 */
        .search-box {
            position: relative;
            max-width: 400px;
            margin: 0 auto var(--spacing-8);
        }
        
        .search-input {
            width: 100%;
            padding: var(--spacing-3) var(--spacing-4) var(--spacing-3) var(--spacing-12);
            border: 2px solid var(--border-color);
            border-radius: var(--border-radius-lg);
            font-size: var(--font-size-base);
            transition: var(--transition);
        }
        
        .search-input:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        .search-icon {
            position: absolute;
            left: var(--spacing-4);
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-light);
            font-size: var(--font-size-lg);
        }
        
        /* 加载动画 */
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
        
        /* 动画定义 */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
        
        @keyframes slideInLeft {
            from {
                opacity: 0;
                transform: translateX(-30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        /* 滚动动画类 */
        .animate-on-scroll {
            opacity: 0;
            transform: translateY(30px);
            transition: all 0.6s ease-out;
        }
        
        .animate-on-scroll.animated {
            opacity: 1;
            transform: translateY(0);
        }
        
        /* 模态框样式 */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: var(--bg-overlay);
            z-index: 2000;
            animation: fadeIn 0.3s ease-out;
        }
        
        .modal.show {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .modal-content {
            background: var(--bg-primary);
            border-radius: var(--border-radius-lg);
            padding: var(--spacing-8);
            max-width: 500px;
            width: 90%;
            max-height: 90vh;
            overflow-y: auto;
            animation: slideInUp 0.3s ease-out;
        }
        
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(50px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: var(--spacing-6);
        }
        
        .modal-title {
            font-size: var(--font-size-2xl);
            font-weight: 600;
            color: var(--text-primary);
        }
        
        .modal-close {
            background: none;
            border: none;
            font-size: var(--font-size-2xl);
            color: var(--text-light);
            cursor: pointer;
            transition: var(--transition);
        }
        
        .modal-close:hover {
            color: var(--text-primary);
        }
        
        /* 表单样式 */
        .form-group {
            margin-bottom: var(--spacing-4);
        }
        
        .form-label {
            display: block;
            margin-bottom: var(--spacing-2);
            font-weight: 600;
            color: var(--text-primary);
        }
        
        .form-input {
            width: 100%;
            padding: var(--spacing-3);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            font-size: var(--font-size-base);
            transition: var(--transition);
        }
        
        .form-input:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        .form-select {
            width: 100%;
            padding: var(--spacing-3);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            background: var(--bg-primary);
            font-size: var(--font-size-base);
            cursor: pointer;
            transition: var(--transition);
        }
        
        .form-textarea {
            width: 100%;
            padding: var(--spacing-3);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            font-size: var(--font-size-base);
            resize: vertical;
            min-height: 100px;
            transition: var(--transition);
        }
        
        /* 通知样式 */
        .notification {
            position: fixed;
            top: 100px;
            right: var(--spacing-4);
            background: var(--bg-primary);
            border-radius: var(--border-radius);
            box-shadow: var(--shadow-lg);
            padding: var(--spacing-4);
            max-width: 300px;
            z-index: 3000;
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
        
        /* 页脚样式 */
        .footer {
            background: var(--bg-dark);
            color: var(--text-white);
            padding: var(--spacing-16) 0 var(--spacing-8);
            margin-top: var(--spacing-20);
        }
        
        .footer-content {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: var(--spacing-8);
            margin-bottom: var(--spacing-8);
        }
        
        .footer-section h3 {
            font-size: var(--font-size-lg);
            margin-bottom: var(--spacing-4);
            color: var(--text-white);
        }
        
        .footer-section p,
        .footer-section a {
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            line-height: 1.6;
        }
        
        .footer-section a:hover {
            color: var(--text-white);
        }
        
        .footer-bottom {
            text-align: center;
            padding-top: var(--spacing-8);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: rgba(255, 255, 255, 0.6);
        }
        
        /* 响应式设计 */
        @media (max-width: 768px) {
            .container {
                padding: 0 var(--spacing-3);
            }
            
            .navbar-nav {
                display: none;
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                background: var(--bg-primary);
                box-shadow: var(--shadow-lg);
                flex-direction: column;
                padding: var(--spacing-4);
                gap: var(--spacing-2);
            }
            
            .navbar-nav.show {
                display: flex;
            }
            
            .mobile-menu-btn {
                display: block;
            }
            
            .hero {
                padding: var(--spacing-16) 0 var(--spacing-12);
            }
            
            .hero-title {
                font-size: var(--font-size-3xl);
            }
            
            .hero-subtitle {
                font-size: var(--font-size-lg);
            }
            
            .grid-cols-2,
            .grid-cols-3,
            .grid-cols-4 {
                grid-template-columns: 1fr;
            }
            
            .filter-group {
                flex-direction: column;
                align-items: stretch;
            }
            
            .card-footer {
                flex-direction: column;
                gap: var(--spacing-3);
                align-items: stretch;
            }
            
            .modal-content {
                margin: var(--spacing-4);
                width: calc(100% - var(--spacing-8));
            }
        }
        
        @media (max-width: 480px) {
            .hero-title {
                font-size: var(--font-size-2xl);
            }
            
            .btn-lg {
                padding: var(--spacing-3) var(--spacing-6);
                font-size: var(--font-size-base);
            }
            
            .card-content {
                padding: var(--spacing-4);
            }
        }
        
        /* 工具类 */
        .text-center {
            text-align: center;
        }
        
        .text-left {
            text-align: left;
        }
        
        .text-right {
            text-align: right;
        }
        
        .hidden {
            display: none;
        }
        
        .visible {
            display: block;
        }
        
        .opacity-0 {
            opacity: 0;
        }
        
        .opacity-50 {
            opacity: 0.5;
        }
        
        .opacity-100 {
            opacity: 1;
        }
        
        .pointer-events-none {
            pointer-events: none;
        }
        
        .cursor-pointer {
            cursor: pointer;
        }
        
        .select-none {
            user-select: none;
        }
        
        /* 间距工具类 */
        .m-0 { margin: 0; }
        .m-1 { margin: var(--spacing-1); }
        .m-2 { margin: var(--spacing-2); }
        .m-3 { margin: var(--spacing-3); }
        .m-4 { margin: var(--spacing-4); }
        .m-6 { margin: var(--spacing-6); }
        .m-8 { margin: var(--spacing-8); }
        
        .mt-0 { margin-top: 0; }
        .mt-1 { margin-top: var(--spacing-1); }
        .mt-2 { margin-top: var(--spacing-2); }
        .mt-3 { margin-top: var(--spacing-3); }
        .mt-4 { margin-top: var(--spacing-4); }
        .mt-6 { margin-top: var(--spacing-6); }
        .mt-8 { margin-top: var(--spacing-8); }
        
        .mb-0 { margin-bottom: 0; }
        .mb-1 { margin-bottom: var(--spacing-1); }
        .mb-2 { margin-bottom: var(--spacing-2); }
        .mb-3 { margin-bottom: var(--spacing-3); }
        .mb-4 { margin-bottom: var(--spacing-4); }
        .mb-6 { margin-bottom: var(--spacing-6); }
        .mb-8 { margin-bottom: var(--spacing-8); }
        
        .p-0 { padding: 0; }
        .p-1 { padding: var(--spacing-1); }
        .p-2 { padding: var(--spacing-2); }
        .p-3 { padding: var(--spacing-3); }
        .p-4 { padding: var(--spacing-4); }
        .p-6 { padding: var(--spacing-6); }
        .p-8 { padding: var(--spacing-8); }
    </style>
</head>
<body>
    <!-- 导航栏 -->
    <nav class="navbar" id="navbar">
        <div class="container">
            <div class="navbar-content">
                <a href="#" class="navbar-brand">🎓 TechEdu</a>
                
                <ul class="navbar-nav" id="navbarNav">
                    <li><a href="#home" class="nav-link active">首页</a></li>
                    <li><a href="#courses" class="nav-link">课程</a></li>
                    <li><a href="#about" class="nav-link">关于我们</a></li>
                    <li><a href="#contact" class="nav-link">联系我们</a></li>
                </ul>
                
                <button class="mobile-menu-btn" id="mobileMenuBtn">
                    ☰
                </button>
            </div>
        </div>
    </nav>
    
    <!-- Hero区域 -->
    <section class="hero" id="home">
        <div class="container">
            <div class="hero-content">
                <h1 class="hero-title">开启你的技术学习之旅</h1>
                <p class="hero-subtitle">高质量的在线课程，助你掌握最新技术，提升职业技能</p>
                <div class="hero-cta">
                    <a href="#courses" class="btn btn-primary btn-lg">🚀 开始学习</a>
                    <a href="#about" class="btn btn-outline btn-lg">📖 了解更多</a>
                </div>
            </div>
        </div>
    </section>
    
    <!-- 课程区域 -->
    <section id="courses" class="container" style="padding: var(--spacing-16) var(--spacing-4);">
        <div class="text-center mb-8">
            <h2 style="font-size: var(--font-size-3xl); font-weight: bold; margin-bottom: var(--spacing-4); color: var(--text-primary);">精选课程</h2>
            <p style="font-size: var(--font-size-lg); color: var(--text-secondary); max-width: 600px; margin: 0 auto;">从编程基础到高级技术，我们提供全方位的学习路径</p>
        </div>
        
        <!-- 搜索框 -->
        <div class="search-box">
            <div style="position: relative;">
                <span class="search-icon">🔍</span>
                <input type="text" class="search-input" id="searchInput" placeholder="搜索课程...">
            </div>
        </div>
        
        <!-- 过滤器 -->
        <div class="filters">
            <div class="container">
                <div class="filter-group">
                    <span class="filter-label">筛选课程：</span>
                    
                    <div class="flex items-center gap-4">
                        <label class="filter-label">分类：</label>
                        <select class="filter-select" id="categoryFilter">
                            <option value="">全部分类</option>
                            <option value="programming">编程开发</option>
                            <option value="design">设计</option>
                            <option value="data-science">数据科学</option>
                            <option value="mobile">移动开发</option>
                            <option value="devops">DevOps</option>
                        </select>
                    </div>
                    
                    <div class="flex items-center gap-4">
                        <label class="filter-label">难度：</label>
                        <select class="filter-select" id="levelFilter">
                            <option value="">全部难度</option>
                            <option value="beginner">初级</option>
                            <option value="intermediate">中级</option>
                            <option value="advanced">高级</option>
                        </select>
                    </div>
                    
                    <div class="flex items-center gap-4">
                        <label class="filter-label">排序：</label>
                        <select class="filter-select" id="sortFilter">
                            <option value="rating">评分最高</option>
                            <option value="students">学员最多</option>
                            <option value="price-low">价格从低到高</option>
                            <option value="price-high">价格从高到低</option>
                        </select>
                    </div>
                    
                    <button class="btn btn-secondary" onclick="resetFilters()">重置筛选</button>
                </div>
            </div>
        </div>
        
        <!-- 课程网格 -->
        <div class="grid-responsive" id="courseGrid">
            <!-- 课程卡片将通过JavaScript动态生成 -->
        </div>
        
        <!-- 加载更多 -->
        <div class="text-center mt-8">
            <button class="btn btn-outline" id="loadMoreBtn" onclick="loadMoreCourses()">
                <span id="loadMoreText">加载更多课程</span>
                <span id="loadMoreSpinner" class="loading hidden"></span>
            </button>
        </div>
    </section>
    
    <!-- 关于我们区域 -->
    <section id="about" style="background: var(--bg-secondary); padding: var(--spacing-16) 0;">
        <div class="container">
            <div class="grid grid-cols-2 gap-8 items-center">
                <div class="animate-on-scroll">
                    <h2 style="font-size: var(--font-size-3xl); font-weight: bold; margin-bottom: var(--spacing-6); color: var(--text-primary);">为什么选择 TechEdu？</h2>
                    <div style="space-y: var(--spacing-4);">
                        <div class="flex items-start gap-4 mb-4">
                            <div style="background: var(--primary-color); color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">1</div>
                            <div>
                                <h3 style="font-size: var(--font-size-lg); font-weight: 600; margin-bottom: var(--spacing-2);">专业师资团队</h3>
                                <p style="color: var(--text-secondary);">来自知名企业的资深工程师和技术专家，具有丰富的实战经验</p>
                            </div>
                        </div>
                        
                        <div class="flex items-start gap-4 mb-4">
                            <div style="background: var(--secondary-color); color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">2</div>
                            <div>
                                <h3 style="font-size: var(--font-size-lg); font-weight: 600; margin-bottom: var(--spacing-2);">实战项目驱动</h3>
                                <p style="color: var(--text-secondary);">通过真实项目学习，掌握实际工作中需要的技能和经验</p>
                            </div>
                        </div>
                        
                        <div class="flex items-start gap-4 mb-4">
                            <div style="background: var(--accent-color); color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">3</div>
                            <div>
                                <h3 style="font-size: var(--font-size-lg); font-weight: 600; margin-bottom: var(--spacing-2);">个性化学习路径</h3>
                                <p style="color: var(--text-secondary);">根据你的基础和目标，定制专属的学习计划和进度</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="animate-on-scroll text-center">
                    <div style="background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); border-radius: var(--border-radius-lg); padding: var(--spacing-8); color: white;">
                        <h3 style="font-size: var(--font-size-2xl); font-weight: bold; margin-bottom: var(--spacing-6);">学习成果</h3>
                        <div class="grid grid-cols-2 gap-6">
                            <div>
                                <div style="font-size: var(--font-size-3xl); font-weight: bold; margin-bottom: var(--spacing-2);">10,000+</div>
                                <div style="opacity: 0.9;">学员</div>
                            </div>
                            <div>
                                <div style="font-size: var(--font-size-3xl); font-weight: bold; margin-bottom: var(--spacing-2);">500+</div>
                                <div style="opacity: 0.9;">课程</div>
                            </div>
                            <div>
                                <div style="font-size: var(--font-size-3xl); font-weight: bold; margin-bottom: var(--spacing-2);">95%</div>
                                <div style="opacity: 0.9;">就业率</div>
                            </div>
                            <div>
                                <div style="font-size: var(--font-size-3xl); font-weight: bold; margin-bottom: var(--spacing-2);">4.8</div>
                                <div style="opacity: 0.9;">平均评分</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <!-- 联系我们区域 -->
    <section id="contact" class="container" style="padding: var(--spacing-16) var(--spacing-4);">
        <div class="text-center mb-8">
            <h2 style="font-size: var(--font-size-3xl); font-weight: bold; margin-bottom: var(--spacing-4); color: var(--text-primary);">联系我们</h2>
            <p style="font-size: var(--font-size-lg); color: var(--text-secondary);">有任何问题或建议，欢迎与我们联系</p>
        </div>
        
        <div class="grid grid-cols-2 gap-8">
            <div class="animate-on-scroll">
                <h3 style="font-size: var(--font-size-xl); font-weight: 600; margin-bottom: var(--spacing-4);">联系信息</h3>
                <div style="space-y: var(--spacing-4);">
                    <div class="flex items-center gap-4 mb-4">
                        <span style="font-size: var(--font-size-xl);">📧</span>
                        <div>
                            <div style="font-weight: 600;">邮箱</div>
                            <div style="color: var(--text-secondary);">contact@techedu.com</div>
                        </div>
                    </div>
                    
                    <div class="flex items-center gap-4 mb-4">
                        <span style="font-size: var(--font-size-xl);">📞</span>
                        <div>
                            <div style="font-weight: 600;">电话</div>
                            <div style="color: var(--text-secondary);">400-123-4567</div>
                        </div>
                    </div>
                    
                    <div class="flex items-center gap-4 mb-4">
                        <span style="font-size: var(--font-size-xl);">📍</span>
                        <div>
                            <div style="font-weight: 600;">地址</div>
                            <div style="color: var(--text-secondary);">北京市朝阳区科技园区</div>
                        </div>
                    </div>
                    
                    <div class="flex items-center gap-4 mb-4">
                        <span style="font-size: var(--font-size-xl);">⏰</span>
                        <div>
                            <div style="font-weight: 600;">工作时间</div>
                            <div style="color: var(--text-secondary);">周一至周五 9:00-18:00</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="animate-on-scroll">
                <form id="contactForm" style="background: var(--bg-secondary); padding: var(--spacing-6); border-radius: var(--border-radius-lg);">
                    <h3 style="font-size: var(--font-size-xl); font-weight: 600; margin-bottom: var(--spacing-4);">发送消息</h3>
                    
                    <div class="form-group">
                        <label class="form-label">姓名</label>
                        <input type="text" class="form-input" name="name" required>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">邮箱</label>
                        <input type="email" class="form-input" name="email" required>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">主题</label>
                        <select class="form-select" name="subject" required>
                            <option value="">请选择主题</option>
                            <option value="course">课程咨询</option>
                            <option value="technical">技术支持</option>
                            <option value="cooperation">合作洽谈</option>
                            <option value="feedback">意见反馈</option>
                            <option value="other">其他</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">消息内容</label>
                        <textarea class="form-textarea" name="message" placeholder="请输入您的消息..." required></textarea>
                    </div>
                    
                    <button type="submit" class="btn btn-primary" style="width: 100%;">
                        <span id="contactSubmitText">发送消息</span>
                        <span id="contactSubmitSpinner" class="loading hidden"></span>
                    </button>
                </form>
            </div>
        </div>
    </section>
    
    <!-- 页脚 -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>🎓 TechEdu</h3>
                    <p>专注于提供高质量的在线技术教育，帮助学员掌握最新技术，提升职业技能。</p>
                </div>
                
                <div class="footer-section">
                    <h3>快速链接</h3>
                    <p><a href="#home">首页</a></p>
                    <p><a href="#courses">课程</a></p>
                    <p><a href="#about">关于我们</a></p>
                    <p><a href="#contact">联系我们</a></p>
                </div>
                
                <div class="footer-section">
                    <h3>课程分类</h3>
                    <p><a href="#">编程开发</a></p>
                    <p><a href="#">设计</a></p>
                    <p><a href="#">数据科学</a></p>
                    <p><a href="#">移动开发</a></p>
                </div>
                
                <div class="footer-section">
                    <h3>联系方式</h3>
                    <p>📧 contact@techedu.com</p>
                    <p>📞 400-123-4567</p>
                    <p>📍 北京市朝阳区科技园区</p>
                </div>
            </div>
            
            <div class="footer-bottom">
                <p>&copy; 2024 TechEdu. 保留所有权利。</p>
            </div>
        </div>
    </footer>
    
    <!-- 课程报名模态框 -->
    <div class="modal" id="enrollModal">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-title">课程报名</h3>
                <button class="modal-close" onclick="closeEnrollModal()">&times;</button>
            </div>
            
            <form id="enrollForm">
                <input type="hidden" id="courseId" name="courseId">
                
                <div class="form-group">
                    <label class="form-label">课程名称</label>
                    <input type="text" class="form-input" id="courseName" readonly>
                </div>
                
                <div class="form-group">
                    <label class="form-label">姓名</label>
                    <input type="text" class="form-input" name="studentName" required>
                </div>
                
                <div class="form-group">
                    <label class="form-label">邮箱</label>
                    <input type="email" class="form-input" name="studentEmail" required>
                </div>
                
                <div class="form-group">
                    <label class="form-label">手机号</label>
                    <input type="tel" class="form-input" name="studentPhone" required>
                </div>
                
                <div class="form-group">
                    <label class="form-label">学习目标</label>
                    <textarea class="form-textarea" name="learningGoal" placeholder="请简述您的学习目标和期望..."></textarea>
                </div>
                
                <div class="form-group">
                    <label class="form-label">技术背景</label>
                    <select class="form-select" name="techBackground" required>
                        <option value="">请选择您的技术背景</option>
                        <option value="beginner">零基础</option>
                        <option value="some">有一些基础</option>
                        <option value="intermediate">有一定经验</option>
                        <option value="advanced">经验丰富</option>
                    </select>
                </div>
                
                <button type="submit" class="btn btn-primary" style="width: 100%;">
                    <span id="enrollSubmitText">立即报名</span>
                    <span id="enrollSubmitSpinner" class="loading hidden"></span>
                </button>
            </form>
        </div>
    </div>
    
    <script>
        // 课程数据
        const courses = {{ courses_data | tojson }};
        let filteredCourses = [...courses];
        let displayedCourses = 6; // 初始显示的课程数量
        
        // DOM元素
        const courseGrid = document.getElementById('courseGrid');
        const searchInput = document.getElementById('searchInput');
        const categoryFilter = document.getElementById('categoryFilter');
        const levelFilter = document.getElementById('levelFilter');
        const sortFilter = document.getElementById('sortFilter');
        const loadMoreBtn = document.getElementById('loadMoreBtn');
        const enrollModal = document.getElementById('enrollModal');
        
        // 初始化
        document.addEventListener('DOMContentLoaded', function() {
            renderCourses();
            initializeEventListeners();
            initializeScrollAnimations();
            initializeNavbar();
        });
        
        // 渲染课程
        function renderCourses() {
            const coursesToShow = filteredCourses.slice(0, displayedCourses);
            courseGrid.innerHTML = '';
            
            coursesToShow.forEach(course => {
                const courseCard = createCourseCard(course);
                courseGrid.appendChild(courseCard);
            });
            
            // 更新加载更多按钮
            updateLoadMoreButton();
        }
        
        // 创建课程卡片
        function createCourseCard(course) {
            const card = document.createElement('div');
            card.className = 'card animate-on-scroll';
            
            const levelBadgeClass = {
                'beginner': 'badge-success',
                'intermediate': 'badge-warning',
                'advanced': 'badge-danger'
            }[course.level] || 'badge-primary';
            
            const levelText = {
                'beginner': '初级',
                'intermediate': '中级',
                'advanced': '高级'
            }[course.level] || course.level;
            
            card.innerHTML = `
                <img src="${course.image}" alt="${course.title}" class="card-image">
                <div class="card-content">
                    <div class="card-meta">
                        <span class="badge ${levelBadgeClass}">${levelText}</span>
                        <span>⏱️ ${course.duration}</span>
                        <span>👨‍🏫 ${course.instructor}</span>
                    </div>
                    
                    <h3 class="card-title">${course.title}</h3>
                    <p class="card-description">${course.description}</p>
                    
                    <div class="flex flex-wrap gap-2 mb-4">
                        ${course.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                    </div>
                    
                    <div class="card-footer">
                        <div class="flex items-center gap-4">
                            <div class="rating">
                                ${generateStars(course.rating)}
                                <span style="margin-left: var(--spacing-2); color: var(--text-secondary); font-size: var(--font-size-sm);">${course.rating}</span>
                            </div>
                            <span style="color: var(--text-light); font-size: var(--font-size-sm);">👥 ${course.students}人</span>
                        </div>
                        
                        <div class="flex items-center gap-4">
                            <span class="price">¥${course.price}</span>
                            <button class="btn btn-primary" onclick="openEnrollModal(${course.id})">
                                立即报名
                            </button>
                        </div>
                    </div>
                </div>
            `;
            
            return card;
        }
        
        // 生成星级评分
        function generateStars(rating) {
            const fullStars = Math.floor(rating);
            const hasHalfStar = rating % 1 !== 0;
            const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
            
            let stars = '';
            
            // 满星
            for (let i = 0; i < fullStars; i++) {
                stars += '<span class="star">★</span>';
            }
            
            // 半星
            if (hasHalfStar) {
                stars += '<span class="star">☆</span>';
            }
            
            // 空星
            for (let i = 0; i < emptyStars; i++) {
                stars += '<span class="star empty">☆</span>';
            }
            
            return stars;
        }
        
        // 过滤和排序课程
        function filterAndSortCourses() {
            const searchTerm = searchInput.value.toLowerCase();
            const category = categoryFilter.value;
            const level = levelFilter.value;
            const sort = sortFilter.value;
            
            // 过滤
            filteredCourses = courses.filter(course => {
                const matchesSearch = course.title.toLowerCase().includes(searchTerm) ||
                                    course.description.toLowerCase().includes(searchTerm) ||
                                    course.tags.some(tag => tag.toLowerCase().includes(searchTerm));
                
                const matchesCategory = !category || course.category === category;
                const matchesLevel = !level || course.level === level;
                
                return matchesSearch && matchesCategory && matchesLevel;
            });
            
            // 排序
            switch (sort) {
                case 'rating':
                    filteredCourses.sort((a, b) => b.rating - a.rating);
                    break;
                case 'students':
                    filteredCourses.sort((a, b) => b.students - a.students);
                    break;
                case 'price-low':
                    filteredCourses.sort((a, b) => a.price - b.price);
                    break;
                case 'price-high':
                    filteredCourses.sort((a, b) => b.price - a.price);
                    break;
                default:
                    filteredCourses.sort((a, b) => b.rating - a.rating);
            }
            
            // 重置显示数量
            displayedCourses = 6;
            renderCourses();
        }
        
        // 重置过滤器
        function resetFilters() {
            searchInput.value = '';
            categoryFilter.value = '';
            levelFilter.value = '';
            sortFilter.value = 'rating';
            filterAndSortCourses();
        }
        
        // 加载更多课程
        function loadMoreCourses() {
            const loadMoreText = document.getElementById('loadMoreText');
            const loadMoreSpinner = document.getElementById('loadMoreSpinner');
            
            // 显示加载动画
            loadMoreText.classList.add('hidden');
            loadMoreSpinner.classList.remove('hidden');
            
            // 模拟加载延迟
            setTimeout(() => {
                displayedCourses += 6;
                renderCourses();
                
                // 隐藏加载动画
                loadMoreText.classList.remove('hidden');
                loadMoreSpinner.classList.add('hidden');
            }, 1000);
        }
        
        // 更新加载更多按钮
        function updateLoadMoreButton() {
            if (displayedCourses >= filteredCourses.length) {
                loadMoreBtn.style.display = 'none';
            } else {
                loadMoreBtn.style.display = 'inline-flex';
            }
        }
        
        // 打开报名模态框
        function openEnrollModal(courseId) {
            const course = courses.find(c => c.id === courseId);
            if (course) {
                document.getElementById('courseId').value = course.id;
                document.getElementById('courseName').value = course.title;
                enrollModal.classList.add('show');
                document.body.style.overflow = 'hidden';
            }
        }
        
        // 关闭报名模态框
        function closeEnrollModal() {
            enrollModal.classList.remove('show');
            document.body.style.overflow = 'auto';
            document.getElementById('enrollForm').reset();
        }
        
        // 初始化事件监听器
        function initializeEventListeners() {
            // 搜索和过滤
            searchInput.addEventListener('input', debounce(filterAndSortCourses, 300));
            categoryFilter.addEventListener('change', filterAndSortCourses);
            levelFilter.addEventListener('change', filterAndSortCourses);
            sortFilter.addEventListener('change', filterAndSortCourses);
            
            // 移动端菜单
            const mobileMenuBtn = document.getElementById('mobileMenuBtn');
            const navbarNav = document.getElementById('navbarNav');
            
            mobileMenuBtn.addEventListener('click', () => {
                navbarNav.classList.toggle('show');
            });
            
            // 平滑滚动
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function (e) {
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute('href'));
                    if (target) {
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                        
                        // 关闭移动端菜单
                        navbarNav.classList.remove('show');
                        
                        // 更新导航链接状态
                        updateActiveNavLink(this.getAttribute('href'));
                    }
                });
            });
            
            // 模态框点击外部关闭
            enrollModal.addEventListener('click', (e) => {
                if (e.target === enrollModal) {
                    closeEnrollModal();
                }
            });
            
            // ESC键关闭模态框
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && enrollModal.classList.contains('show')) {
                    closeEnrollModal();
                }
            });
            
            // 报名表单提交
            document.getElementById('enrollForm').addEventListener('submit', handleEnrollSubmit);
            
            // 联系表单提交
            document.getElementById('contactForm').addEventListener('submit', handleContactSubmit);
        }
        
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
        
        // 更新导航链接状态
        function updateActiveNavLink(href) {
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
            });
            
            const activeLink = document.querySelector(`a[href="${href}"]`);
            if (activeLink) {
                activeLink.classList.add('active');
            }
        }
        
        // 初始化导航栏
        function initializeNavbar() {
            const navbar = document.getElementById('navbar');
            
            window.addEventListener('scroll', () => {
                if (window.scrollY > 100) {
                    navbar.classList.add('scrolled');
                } else {
                    navbar.classList.remove('scrolled');
                }
                
                // 更新当前活动的导航链接
                updateActiveNavOnScroll();
            });
        }
        
        // 根据滚动位置更新活动导航链接
        function updateActiveNavOnScroll() {
            const sections = ['home', 'courses', 'about', 'contact'];
            const scrollPosition = window.scrollY + 100;
            
            for (let i = sections.length - 1; i >= 0; i--) {
                const section = document.getElementById(sections[i]);
                if (section && section.offsetTop <= scrollPosition) {
                    updateActiveNavLink(`#${sections[i]}`);
                    break;
                }
            }
        }
        
        // 初始化滚动动画
        function initializeScrollAnimations() {
            const observerOptions = {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            };
            
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('animated');
                    }
                });
            }, observerOptions);
            
            // 观察所有需要动画的元素
            document.querySelectorAll('.animate-on-scroll').forEach(el => {
                observer.observe(el);
            });
        }
        
        // 处理报名表单提交
        async function handleEnrollSubmit(e) {
            e.preventDefault();
            
            const submitText = document.getElementById('enrollSubmitText');
            const submitSpinner = document.getElementById('enrollSubmitSpinner');
            
            // 显示加载状态
            submitText.classList.add('hidden');
            submitSpinner.classList.remove('hidden');
            
            try {
                const formData = new FormData(e.target);
                const enrollData = Object.fromEntries(formData.entries());
                
                const response = await fetch('/api/enroll', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(enrollData)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    showNotification('报名成功！我们会尽快与您联系。', 'success');
                    closeEnrollModal();
                } else {
                    showNotification(result.message || '报名失败，请稍后重试。', 'error');
                }
            } catch (error) {
                console.error('报名错误:', error);
                showNotification('网络错误，请检查网络连接后重试。', 'error');
            } finally {
                // 恢复按钮状态
                submitText.classList.remove('hidden');
                submitSpinner.classList.add('hidden');
            }
        }
        
        // 处理联系表单提交
        async function handleContactSubmit(e) {
            e.preventDefault();
            
            const submitText = document.getElementById('contactSubmitText');
            const submitSpinner = document.getElementById('contactSubmitSpinner');
            
            // 显示加载状态
            submitText.classList.add('hidden');
            submitSpinner.classList.remove('hidden');
            
            try {
                const formData = new FormData(e.target);
                const contactData = Object.fromEntries(formData.entries());
                
                // 模拟API调用
                await new Promise(resolve => setTimeout(resolve, 1500));
                
                showNotification('消息发送成功！我们会尽快回复您。', 'success');
                e.target.reset();
            } catch (error) {
                console.error('联系错误:', error);
                showNotification('发送失败，请稍后重试。', 'error');
            } finally {
                // 恢复按钮状态
                submitText.classList.remove('hidden');
                submitSpinner.classList.add('hidden');
            }
        }
        
        // 显示通知
        function showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = `notification ${type}`;
            notification.innerHTML = `
                <div style="display: flex; align-items: center; gap: var(--spacing-3);">
                    <span style="font-size: var(--font-size-lg);">
                        ${type === 'success' ? '✅' : type === 'error' ? '❌' : type === 'warning' ? '⚠️' : 'ℹ️'}
                    </span>
                    <span>${message}</span>
                </div>
            `;
            
            document.body.appendChild(notification);
            
            // 自动移除通知
            setTimeout(() => {
                notification.style.animation = 'slideOutRight 0.3s ease-in-out';
                setTimeout(() => {
                    if (notification.parentNode) {
                        notification.parentNode.removeChild(notification);
                    }
                }, 300);
            }, 3000);
        }
        
        // 添加slideOutRight动画
        const style = document.createElement('style');
        style.textContent = `
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
        `;
        document.head.appendChild(style);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """主页路由"""
    return render_template_string(SOLUTION_TEMPLATE, courses_data=courses_db)

@app.route('/api/enroll', methods=['POST'])
def api_enroll():
    """课程报名API"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['courseId', 'studentName', 'studentEmail', 'studentPhone', 'techBackground']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'缺少必填字段: {field}'
                }), 400
        
        # 验证课程是否存在
        course = next((c for c in courses_db if c['id'] == int(data['courseId'])), None)
        if not course:
            return jsonify({
                'success': False,
                'message': '课程不存在'
            }), 404
        
        # 创建报名记录
        enrollment = {
            'id': len(enrollments_db) + 1,
            'course_id': int(data['courseId']),
            'course_title': course['title'],
            'student_name': data['studentName'],
            'student_email': data['studentEmail'],
            'student_phone': data['studentPhone'],
            'learning_goal': data.get('learningGoal', ''),
            'tech_background': data['techBackground'],
            'enrollment_date': datetime.now().isoformat(),
            'status': 'pending'
        }
        
        enrollments_db.append(enrollment)
        
        return jsonify({
            'success': True,
            'message': '报名成功！我们会尽快与您联系。',
            'enrollment_id': enrollment['id']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'服务器错误: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎓 Session19 练习1解决方案：HTML5和CSS3基础")
    print("="*60)
    print("\n📋 解决方案特性:")
    print("   ✅ HTML5语义化标签的正确使用")
    print("   ✅ CSS3现代布局技术（Flexbox、Grid）")
    print("   ✅ 响应式设计和媒体查询")
    print("   ✅ CSS变量和动画效果")
    print("   ✅ JavaScript交互功能")
    print("   ✅ 完整的在线学习平台界面")
    print("\n🚀 启动应用...")
    print("📱 访问 http://localhost:5000 查看解决方案")
    print("\n💡 解决方案亮点:")
    print("   • 使用CSS变量实现主题一致性")
    print("   • Flexbox和Grid布局的综合应用")
    print("   • 响应式设计适配移动端")
    print("   • 平滑滚动和动画效果")
    print("   • 模态框和表单交互")
    print("   • 课程搜索和过滤功能")
    print("   • 现代化的UI设计")
    print("\n" + "="*60)
    
    app.run(debug=True, port=5000)