#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session19 示例2：CSS现代布局示例

本示例演示了现代CSS布局技术，包括Flexbox、Grid、
CSS变量、响应式设计和动画效果。

作者: Python教程团队
创建日期: 2024-12-24
"""

from flask import Flask, render_template_string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'css-example-key'

# CSS布局示例模板
CSS_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSS现代布局示例</title>
    <style>
        /* CSS变量定义 */
        :root {
            --primary-color: #667eea;
            --secondary-color: #764ba2;
            --accent-color: #f093fb;
            --text-color: #333;
            --text-light: #666;
            --bg-color: #f8f9fa;
            --white: #ffffff;
            --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            --shadow-hover: 0 8px 15px rgba(0, 0, 0, 0.2);
            --border-radius: 8px;
            --transition: all 0.3s ease;
            --font-family: 'Microsoft YaHei', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* 基础样式重置 */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: var(--font-family);
            line-height: 1.6;
            color: var(--text-color);
            background: linear-gradient(135deg, var(--bg-color) 0%, #e3f2fd 100%);
            min-height: 100vh;
        }
        
        /* 容器样式 */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        /* 页面头部 - Flexbox布局 */
        .header {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: var(--white);
            padding: 2rem;
            border-radius: var(--border-radius);
            margin-bottom: 2rem;
            box-shadow: var(--shadow);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }
        
        .header h1 {
            font-size: 2.5rem;
            font-weight: 300;
            margin: 0;
        }
        
        .header-actions {
            display: flex;
            gap: 1rem;
        }
        
        .btn {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: var(--border-radius);
            background: rgba(255, 255, 255, 0.2);
            color: var(--white);
            text-decoration: none;
            transition: var(--transition);
            cursor: pointer;
            font-size: 0.9rem;
            backdrop-filter: blur(10px);
        }
        
        .btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
        
        /* 导航栏 - Flexbox */
        .nav {
            background: var(--white);
            padding: 1rem 0;
            border-radius: var(--border-radius);
            margin-bottom: 2rem;
            box-shadow: var(--shadow);
        }
        
        .nav-list {
            display: flex;
            justify-content: center;
            list-style: none;
            gap: 2rem;
            flex-wrap: wrap;
        }
        
        .nav-link {
            color: var(--text-color);
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: var(--border-radius);
            transition: var(--transition);
            position: relative;
        }
        
        .nav-link:hover {
            color: var(--primary-color);
            background: rgba(102, 126, 234, 0.1);
        }
        
        .nav-link.active {
            color: var(--primary-color);
            background: rgba(102, 126, 234, 0.1);
        }
        
        .nav-link.active::after {
            content: '';
            position: absolute;
            bottom: -1rem;
            left: 50%;
            transform: translateX(-50%);
            width: 30px;
            height: 3px;
            background: var(--primary-color);
            border-radius: 2px;
        }
        
        /* Grid布局示例 */
        .grid-section {
            margin: 2rem 0;
        }
        
        .section-title {
            font-size: 2rem;
            margin-bottom: 1rem;
            text-align: center;
            color: var(--text-color);
        }
        
        .grid-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin: 2rem 0;
        }
        
        .grid-item {
            background: var(--white);
            padding: 2rem;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            transition: var(--transition);
            position: relative;
            overflow: hidden;
        }
        
        .grid-item::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
        }
        
        .grid-item:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-hover);
        }
        
        .grid-item h3 {
            color: var(--primary-color);
            margin-bottom: 1rem;
            font-size: 1.5rem;
        }
        
        .grid-item p {
            color: var(--text-light);
            line-height: 1.8;
        }
        
        /* Flexbox布局示例 */
        .flex-section {
            background: var(--white);
            padding: 2rem;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            margin: 2rem 0;
        }
        
        .flex-container {
            display: flex;
            gap: 1rem;
            margin: 1rem 0;
            flex-wrap: wrap;
        }
        
        .flex-item {
            flex: 1;
            min-width: 200px;
            padding: 1.5rem;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: var(--white);
            border-radius: var(--border-radius);
            text-align: center;
            transition: var(--transition);
        }
        
        .flex-item:hover {
            transform: scale(1.05);
        }
        
        .flex-item h4 {
            margin-bottom: 0.5rem;
            font-size: 1.2rem;
        }
        
        /* 卡片布局 */
        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        
        .card {
            background: var(--white);
            border-radius: var(--border-radius);
            overflow: hidden;
            box-shadow: var(--shadow);
            transition: var(--transition);
        }
        
        .card:hover {
            transform: translateY(-3px);
            box-shadow: var(--shadow-hover);
        }
        
        .card-header {
            height: 150px;
            background: linear-gradient(45deg, var(--primary-color), var(--accent-color));
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--white);
            font-size: 3rem;
        }
        
        .card-body {
            padding: 1.5rem;
        }
        
        .card-title {
            font-size: 1.3rem;
            margin-bottom: 0.5rem;
            color: var(--text-color);
        }
        
        .card-text {
            color: var(--text-light);
            font-size: 0.9rem;
            line-height: 1.6;
        }
        
        /* 动画效果 */
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
        
        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.05);
            }
        }
        
        .animate-fade-in {
            animation: fadeInUp 0.6s ease-out;
        }
        
        .animate-pulse {
            animation: pulse 2s infinite;
        }
        
        /* 响应式设计 */
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .header {
                flex-direction: column;
                text-align: center;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .nav-list {
                flex-direction: column;
                gap: 0.5rem;
            }
            
            .grid-container {
                grid-template-columns: 1fr;
            }
            
            .flex-container {
                flex-direction: column;
            }
            
            .card-grid {
                grid-template-columns: 1fr;
            }
        }
        
        @media (max-width: 480px) {
            .header h1 {
                font-size: 1.5rem;
            }
            
            .section-title {
                font-size: 1.5rem;
            }
            
            .grid-item,
            .flex-section {
                padding: 1rem;
            }
        }
        
        /* 深色模式支持 */
        @media (prefers-color-scheme: dark) {
            :root {
                --text-color: #e0e0e0;
                --text-light: #b0b0b0;
                --bg-color: #1a1a1a;
                --white: #2d2d2d;
            }
            
            body {
                background: linear-gradient(135deg, var(--bg-color) 0%, #263238 100%);
            }
        }
        
        /* 工具类 */
        .text-center { text-align: center; }
        .text-left { text-align: left; }
        .text-right { text-align: right; }
        
        .mt-1 { margin-top: 0.5rem; }
        .mt-2 { margin-top: 1rem; }
        .mt-3 { margin-top: 1.5rem; }
        
        .mb-1 { margin-bottom: 0.5rem; }
        .mb-2 { margin-bottom: 1rem; }
        .mb-3 { margin-bottom: 1.5rem; }
        
        .p-1 { padding: 0.5rem; }
        .p-2 { padding: 1rem; }
        .p-3 { padding: 1.5rem; }
    </style>
</head>
<body>
    <div class="container">
        <!-- 页面头部 -->
        <header class="header animate-fade-in">
            <h1>CSS现代布局示例</h1>
            <div class="header-actions">
                <button class="btn" onclick="toggleTheme()">切换主题</button>
                <button class="btn" onclick="toggleAnimation()">切换动画</button>
            </div>
        </header>
        
        <!-- 导航栏 -->
        <nav class="nav animate-fade-in">
            <ul class="nav-list">
                <li><a href="#grid" class="nav-link active">Grid布局</a></li>
                <li><a href="#flexbox" class="nav-link">Flexbox布局</a></li>
                <li><a href="#cards" class="nav-link">卡片布局</a></li>
                <li><a href="#responsive" class="nav-link">响应式设计</a></li>
            </ul>
        </nav>
        
        <!-- Grid布局示例 -->
        <section id="grid" class="grid-section animate-fade-in">
            <h2 class="section-title">CSS Grid布局示例</h2>
            <div class="grid-container">
                <div class="grid-item">
                    <h3>🎯 Grid基础</h3>
                    <p>CSS Grid是一个二维布局系统，可以同时处理行和列。它提供了强大的布局控制能力，适合复杂的页面布局。</p>
                </div>
                <div class="grid-item">
                    <h3>📱 响应式Grid</h3>
                    <p>使用auto-fit和minmax()函数，可以创建自适应的网格布局，在不同屏幕尺寸下自动调整列数。</p>
                </div>
                <div class="grid-item">
                    <h3>🔧 Grid属性</h3>
                    <p>grid-template-columns、grid-template-rows、gap等属性提供了灵活的网格定义方式。</p>
                </div>
                <div class="grid-item">
                    <h3>🎨 Grid区域</h3>
                    <p>通过grid-template-areas可以直观地定义布局区域，使代码更易读和维护。</p>
                </div>
            </div>
        </section>
        
        <!-- Flexbox布局示例 -->
        <section id="flexbox" class="flex-section animate-fade-in">
            <h2 class="section-title">Flexbox布局示例</h2>
            <p class="text-center mb-2">Flexbox是一维布局方法，用于在容器中分配空间和对齐项目。</p>
            
            <div class="flex-container">
                <div class="flex-item">
                    <h4>弹性项目 1</h4>
                    <p>flex: 1</p>
                </div>
                <div class="flex-item">
                    <h4>弹性项目 2</h4>
                    <p>flex: 1</p>
                </div>
                <div class="flex-item">
                    <h4>弹性项目 3</h4>
                    <p>flex: 1</p>
                </div>
            </div>
            
            <div class="flex-container" style="justify-content: space-between;">
                <div class="flex-item" style="flex: none; width: 150px;">
                    <h4>固定宽度</h4>
                    <p>150px</p>
                </div>
                <div class="flex-item" style="flex: 2;">
                    <h4>弹性项目</h4>
                    <p>flex: 2</p>
                </div>
                <div class="flex-item" style="flex: none; width: 100px;">
                    <h4>固定</h4>
                    <p>100px</p>
                </div>
            </div>
        </section>
        
        <!-- 卡片布局示例 -->
        <section id="cards" class="animate-fade-in">
            <h2 class="section-title">卡片布局示例</h2>
            <div class="card-grid">
                <div class="card">
                    <div class="card-header">🚀</div>
                    <div class="card-body">
                        <h3 class="card-title">性能优化</h3>
                        <p class="card-text">通过CSS优化、图片压缩、代码分割等技术提升网站性能。</p>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">🎨</div>
                    <div class="card-body">
                        <h3 class="card-title">视觉设计</h3>
                        <p class="card-text">运用现代设计原则，创造美观且用户友好的界面。</p>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">📱</div>
                    <div class="card-body">
                        <h3 class="card-title">响应式设计</h3>
                        <p class="card-text">确保网站在各种设备和屏幕尺寸上都能完美显示。</p>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">⚡</div>
                    <div class="card-body">
                        <h3 class="card-title">交互体验</h3>
                        <p class="card-text">通过动画和交互效果提升用户体验。</p>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">🔧</div>
                    <div class="card-body">
                        <h3 class="card-title">开发工具</h3>
                        <p class="card-text">使用现代开发工具和框架提高开发效率。</p>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">🌐</div>
                    <div class="card-body">
                        <h3 class="card-title">Web标准</h3>
                        <p class="card-text">遵循Web标准，确保代码的兼容性和可维护性。</p>
                    </div>
                </div>
            </div>
        </section>
    </div>
    
    <script>
        // 主题切换功能
        let isDarkMode = false;
        
        function toggleTheme() {
            isDarkMode = !isDarkMode;
            document.documentElement.style.setProperty('--text-color', isDarkMode ? '#e0e0e0' : '#333');
            document.documentElement.style.setProperty('--text-light', isDarkMode ? '#b0b0b0' : '#666');
            document.documentElement.style.setProperty('--bg-color', isDarkMode ? '#1a1a1a' : '#f8f9fa');
            document.documentElement.style.setProperty('--white', isDarkMode ? '#2d2d2d' : '#ffffff');
            
            document.body.style.background = isDarkMode 
                ? 'linear-gradient(135deg, #1a1a1a 0%, #263238 100%)'
                : 'linear-gradient(135deg, #f8f9fa 0%, #e3f2fd 100%)';
        }
        
        // 动画切换功能
        let animationsEnabled = true;
        
        function toggleAnimation() {
            animationsEnabled = !animationsEnabled;
            const elements = document.querySelectorAll('.animate-fade-in, .animate-pulse');
            
            elements.forEach(el => {
                if (animationsEnabled) {
                    el.style.animation = '';
                } else {
                    el.style.animation = 'none';
                }
            });
            
            // 切换悬停效果
            const style = document.createElement('style');
            if (!animationsEnabled) {
                style.textContent = `
                    .grid-item:hover,
                    .card:hover,
                    .flex-item:hover,
                    .btn:hover,
                    .nav-link:hover {
                        transform: none !important;
                    }
                `;
            }
            document.head.appendChild(style);
        }
        
        // 导航链接激活状态
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                // 移除所有激活状态
                document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                
                // 添加当前激活状态
                this.classList.add('active');
                
                // 滚动到对应部分
                const targetId = this.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
        
        // 滚动时更新导航状态
        window.addEventListener('scroll', function() {
            const sections = document.querySelectorAll('section[id]');
            const navLinks = document.querySelectorAll('.nav-link');
            
            let currentSection = '';
            
            sections.forEach(section => {
                const sectionTop = section.offsetTop - 100;
                const sectionHeight = section.offsetHeight;
                
                if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
                    currentSection = section.getAttribute('id');
                }
            });
            
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === '#' + currentSection) {
                    link.classList.add('active');
                }
            });
        });
        
        // 页面加载完成后添加动画
        document.addEventListener('DOMContentLoaded', function() {
            const elements = document.querySelectorAll('.animate-fade-in');
            elements.forEach((el, index) => {
                setTimeout(() => {
                    el.style.opacity = '0';
                    el.style.transform = 'translateY(30px)';
                    el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
                    
                    setTimeout(() => {
                        el.style.opacity = '1';
                        el.style.transform = 'translateY(0)';
                    }, 100);
                }, index * 200);
            });
        });
        
        // 卡片点击效果
        document.querySelectorAll('.card').forEach(card => {
            card.addEventListener('click', function() {
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 150);
            });
        });
        
        console.log('CSS现代布局示例已加载');
        console.log('功能包括：');
        console.log('- CSS Grid和Flexbox布局');
        console.log('- CSS变量和响应式设计');
        console.log('- 动画效果和交互');
        console.log('- 主题切换功能');
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """
    显示CSS现代布局示例页面
    """
    return render_template_string(CSS_TEMPLATE)

def main():
    """
    主函数
    """
    print("Session19 示例2：CSS现代布局示例")
    print("=" * 40)
    print("\n本示例展示了：")
    print("1. CSS Grid和Flexbox布局")
    print("2. CSS变量和自定义属性")
    print("3. 响应式设计和媒体查询")
    print("4. CSS动画和过渡效果")
    print("5. 现代CSS最佳实践")
    print("\n访问 http://127.0.0.1:5000 查看示例")
    print("按 Ctrl+C 停止服务器")
    
    app.run(debug=True, host='127.0.0.1', port=5000)

if __name__ == '__main__':
    main()