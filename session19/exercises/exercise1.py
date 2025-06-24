#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session19 练习1：HTML5和CSS3基础练习

练习目标：
1. 掌握HTML5语义化标签的使用
2. 学习CSS3新特性和布局技术
3. 实现响应式设计
4. 创建现代化的用户界面

作者: Python教程团队
创建日期: 2024-12-24
"""

from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'exercise1-secret-key'

# 练习数据
exercise_data = {
    'courses': [
        {
            'id': 1,
            'title': 'Python基础编程',
            'instructor': '张老师',
            'duration': '8周',
            'level': 'beginner',
            'price': 299,
            'rating': 4.8,
            'students': 1234,
            'image': 'https://via.placeholder.com/300x200/4f46e5/ffffff?text=Python',
            'description': '从零开始学习Python编程，掌握基础语法和核心概念。',
            'tags': ['Python', '编程基础', '后端开发']
        },
        {
            'id': 2,
            'title': 'Web前端开发',
            'instructor': '李老师',
            'duration': '12周',
            'level': 'intermediate',
            'price': 499,
            'rating': 4.9,
            'students': 856,
            'image': 'https://via.placeholder.com/300x200/10b981/ffffff?text=Frontend',
            'description': '学习HTML、CSS、JavaScript，构建现代化的Web应用。',
            'tags': ['HTML', 'CSS', 'JavaScript', '前端开发']
        },
        {
            'id': 3,
            'title': '数据科学入门',
            'instructor': '王老师',
            'duration': '10周',
            'level': 'advanced',
            'price': 699,
            'rating': 4.7,
            'students': 567,
            'image': 'https://via.placeholder.com/300x200/f59e0b/ffffff?text=DataScience',
            'description': '使用Python进行数据分析和机器学习，掌握数据科学核心技能。',
            'tags': ['Python', '数据分析', '机器学习', 'Pandas']
        }
    ],
    'testimonials': [
        {
            'name': '小明',
            'course': 'Python基础编程',
            'rating': 5,
            'comment': '课程内容很棒，老师讲解清晰，从零基础到能写简单程序！',
            'avatar': 'https://via.placeholder.com/60x60/6366f1/ffffff?text=M'
        },
        {
            'name': '小红',
            'course': 'Web前端开发',
            'rating': 5,
            'comment': '学完这个课程，我成功找到了前端开发的工作，非常感谢！',
            'avatar': 'https://via.placeholder.com/60x60/ec4899/ffffff?text=H'
        },
        {
            'name': '小刚',
            'course': '数据科学入门',
            'rating': 4,
            'comment': '内容很丰富，但需要一定的数学基础，适合有编程经验的同学。',
            'avatar': 'https://via.placeholder.com/60x60/8b5cf6/ffffff?text=G'
        }
    ]
}

# 练习模板
EXERCISE_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>在线课程平台 - HTML5/CSS3练习</title>
    
    <style>
        /* TODO: 练习1 - 完成CSS样式 */
        /* 提示：使用CSS变量、Flexbox/Grid布局、响应式设计 */
        
        :root {
            /* 定义CSS变量 */
            --primary-color: #4f46e5;
            --secondary-color: #10b981;
            --accent-color: #f59e0b;
            --text-color: #1f2937;
            --text-light: #6b7280;
            --bg-color: #ffffff;
            --bg-light: #f9fafb;
            --border-color: #e5e7eb;
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
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
            background-color: var(--bg-color);
        }
        
        /* 导航栏样式 */
        .navbar {
            /* TODO: 实现导航栏样式 */
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            padding: 1rem 0;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: var(--shadow);
        }
        
        .nav-container {
            /* TODO: 使用Flexbox布局 */
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            /* TODO: 完成logo样式 */
            color: white;
            font-size: 1.5rem;
            font-weight: bold;
            text-decoration: none;
        }
        
        .nav-menu {
            /* TODO: 导航菜单样式 */
            display: flex;
            list-style: none;
            gap: 2rem;
        }
        
        .nav-link {
            /* TODO: 导航链接样式 */
            color: rgba(255, 255, 255, 0.9);
            text-decoration: none;
            transition: var(--transition);
            padding: 0.5rem 1rem;
            border-radius: var(--border-radius);
        }
        
        .nav-link:hover {
            /* TODO: 悬停效果 */
            color: white;
            background-color: rgba(255, 255, 255, 0.1);
        }
        
        /* 英雄区域样式 */
        .hero {
            /* TODO: 实现英雄区域样式 */
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 4rem 0;
            text-align: center;
        }
        
        .hero-content {
            max-width: 800px;
            margin: 0 auto;
            padding: 0 1rem;
        }
        
        .hero h1 {
            /* TODO: 标题样式 */
            font-size: 3rem;
            margin-bottom: 1rem;
            font-weight: 700;
        }
        
        .hero p {
            /* TODO: 描述文字样式 */
            font-size: 1.2rem;
            margin-bottom: 2rem;
            opacity: 0.9;
        }
        
        .cta-button {
            /* TODO: 行动按钮样式 */
            background-color: var(--accent-color);
            color: white;
            padding: 1rem 2rem;
            border: none;
            border-radius: var(--border-radius);
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
            text-decoration: none;
            display: inline-block;
        }
        
        .cta-button:hover {
            /* TODO: 按钮悬停效果 */
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }
        
        /* 容器和布局 */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
        }
        
        .section {
            padding: 4rem 0;
        }
        
        .section-title {
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 3rem;
            color: var(--text-color);
        }
        
        /* 课程网格布局 */
        .courses-grid {
            /* TODO: 使用CSS Grid布局 */
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }
        
        .course-card {
            /* TODO: 课程卡片样式 */
            background: var(--bg-color);
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            overflow: hidden;
            transition: var(--transition);
        }
        
        .course-card:hover {
            /* TODO: 卡片悬停效果 */
            transform: translateY(-5px);
            box-shadow: var(--shadow-lg);
        }
        
        .course-image {
            /* TODO: 课程图片样式 */
            width: 100%;
            height: 200px;
            object-fit: cover;
        }
        
        .course-content {
            padding: 1.5rem;
        }
        
        .course-title {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--text-color);
        }
        
        .course-instructor {
            color: var(--text-light);
            margin-bottom: 1rem;
        }
        
        .course-meta {
            /* TODO: 课程元信息布局 */
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        
        .course-level {
            /* TODO: 课程级别标签 */
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 500;
        }
        
        .level-beginner {
            background-color: #dcfce7;
            color: #166534;
        }
        
        .level-intermediate {
            background-color: #fef3c7;
            color: #92400e;
        }
        
        .level-advanced {
            background-color: #fee2e2;
            color: #991b1b;
        }
        
        .course-price {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary-color);
        }
        
        .course-rating {
            /* TODO: 评分样式 */
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }
        
        .stars {
            color: var(--accent-color);
        }
        
        .course-tags {
            /* TODO: 标签布局 */
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }
        
        .tag {
            background-color: var(--bg-light);
            color: var(--text-light);
            padding: 0.25rem 0.5rem;
            border-radius: var(--border-radius);
            font-size: 0.875rem;
        }
        
        .enroll-button {
            /* TODO: 报名按钮样式 */
            width: 100%;
            background-color: var(--primary-color);
            color: white;
            padding: 0.75rem;
            border: none;
            border-radius: var(--border-radius);
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
        }
        
        .enroll-button:hover {
            background-color: #3730a3;
        }
        
        /* 用户评价区域 */
        .testimonials {
            background-color: var(--bg-light);
        }
        
        .testimonials-grid {
            /* TODO: 评价网格布局 */
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }
        
        .testimonial-card {
            /* TODO: 评价卡片样式 */
            background: var(--bg-color);
            padding: 2rem;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
        }
        
        .testimonial-header {
            /* TODO: 评价头部布局 */
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1rem;
        }
        
        .testimonial-avatar {
            width: 60px;
            height: 60px;
            border-radius: 50%;
        }
        
        .testimonial-info h4 {
            margin-bottom: 0.25rem;
        }
        
        .testimonial-course {
            color: var(--text-light);
            font-size: 0.875rem;
        }
        
        .testimonial-rating {
            color: var(--accent-color);
            margin-bottom: 1rem;
        }
        
        /* 页脚样式 */
        .footer {
            background-color: var(--text-color);
            color: white;
            padding: 3rem 0 1rem;
        }
        
        .footer-content {
            /* TODO: 页脚内容布局 */
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }
        
        .footer-section h3 {
            margin-bottom: 1rem;
        }
        
        .footer-section ul {
            list-style: none;
        }
        
        .footer-section ul li {
            margin-bottom: 0.5rem;
        }
        
        .footer-section a {
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            transition: var(--transition);
        }
        
        .footer-section a:hover {
            color: white;
        }
        
        .footer-bottom {
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            padding-top: 1rem;
            text-align: center;
            color: rgba(255, 255, 255, 0.6);
        }
        
        /* 响应式设计 */
        @media (max-width: 768px) {
            /* TODO: 移动端适配 */
            .nav-menu {
                display: none; /* 简化处理，实际项目中应实现汉堡菜单 */
            }
            
            .hero h1 {
                font-size: 2rem;
            }
            
            .hero p {
                font-size: 1rem;
            }
            
            .section-title {
                font-size: 2rem;
            }
            
            .courses-grid {
                grid-template-columns: 1fr;
            }
            
            .testimonials-grid {
                grid-template-columns: 1fr;
            }
            
            .footer-content {
                grid-template-columns: 1fr;
                text-align: center;
            }
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
        
        .fade-in-up {
            animation: fadeInUp 0.6s ease-out;
        }
        
        /* 加载动画 */
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 1s ease-in-out infinite;
        }
        
        @keyframes spin {
            to {
                transform: rotate(360deg);
            }
        }
    </style>
</head>
<body>
    <!-- TODO: 练习2 - 完成HTML结构 -->
    <!-- 提示：使用HTML5语义化标签 -->
    
    <!-- 导航栏 -->
    <nav class="navbar">
        <div class="nav-container">
            <a href="#" class="logo">📚 学习平台</a>
            <ul class="nav-menu">
                <li><a href="#home" class="nav-link">首页</a></li>
                <li><a href="#courses" class="nav-link">课程</a></li>
                <li><a href="#about" class="nav-link">关于我们</a></li>
                <li><a href="#contact" class="nav-link">联系我们</a></li>
            </ul>
        </div>
    </nav>
    
    <!-- 英雄区域 -->
    <header class="hero" id="home">
        <div class="hero-content">
            <h1>开启你的编程之旅</h1>
            <p>专业的在线编程课程，从基础到进阶，助你成为优秀的开发者</p>
            <a href="#courses" class="cta-button">立即开始学习</a>
        </div>
    </header>
    
    <!-- 课程区域 -->
    <section class="section" id="courses">
        <div class="container">
            <h2 class="section-title">热门课程</h2>
            <div class="courses-grid">
                {% for course in courses %}
                <article class="course-card fade-in-up">
                    <img src="{{ course.image }}" alt="{{ course.title }}" class="course-image">
                    <div class="course-content">
                        <h3 class="course-title">{{ course.title }}</h3>
                        <p class="course-instructor">讲师：{{ course.instructor }}</p>
                        
                        <div class="course-meta">
                            <span class="course-level level-{{ course.level }}">
                                {% if course.level == 'beginner' %}初级
                                {% elif course.level == 'intermediate' %}中级
                                {% else %}高级{% endif %}
                            </span>
                            <span class="course-price">¥{{ course.price }}</span>
                        </div>
                        
                        <div class="course-rating">
                            <span class="stars">
                                {% for i in range(5) %}
                                    {% if i < course.rating|int %}
                                        ⭐
                                    {% else %}
                                        ☆
                                    {% endif %}
                                {% endfor %}
                            </span>
                            <span>{{ course.rating }} ({{ course.students }} 学员)</span>
                        </div>
                        
                        <p>{{ course.description }}</p>
                        
                        <div class="course-tags">
                            {% for tag in course.tags %}
                                <span class="tag">{{ tag }}</span>
                            {% endfor %}
                        </div>
                        
                        <button class="enroll-button" onclick="enrollCourse({{ course.id }})">
                            立即报名
                        </button>
                    </div>
                </article>
                {% endfor %}
            </div>
        </div>
    </section>
    
    <!-- 用户评价区域 -->
    <section class="section testimonials">
        <div class="container">
            <h2 class="section-title">学员评价</h2>
            <div class="testimonials-grid">
                {% for testimonial in testimonials %}
                <article class="testimonial-card fade-in-up">
                    <div class="testimonial-header">
                        <img src="{{ testimonial.avatar }}" alt="{{ testimonial.name }}" class="testimonial-avatar">
                        <div class="testimonial-info">
                            <h4>{{ testimonial.name }}</h4>
                            <p class="testimonial-course">{{ testimonial.course }}</p>
                        </div>
                    </div>
                    <div class="testimonial-rating">
                        {% for i in range(testimonial.rating) %}
                            ⭐
                        {% endfor %}
                    </div>
                    <blockquote>"{{ testimonial.comment }}"</blockquote>
                </article>
                {% endfor %}
            </div>
        </div>
    </section>
    
    <!-- 页脚 -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>关于我们</h3>
                    <p>我们致力于提供高质量的在线编程教育，帮助每个人实现技术梦想。</p>
                </div>
                <div class="footer-section">
                    <h3>课程分类</h3>
                    <ul>
                        <li><a href="#">Python编程</a></li>
                        <li><a href="#">Web开发</a></li>
                        <li><a href="#">数据科学</a></li>
                        <li><a href="#">人工智能</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h3>支持</h3>
                    <ul>
                        <li><a href="#">帮助中心</a></li>
                        <li><a href="#">联系客服</a></li>
                        <li><a href="#">常见问题</a></li>
                        <li><a href="#">意见反馈</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h3>联系我们</h3>
                    <ul>
                        <li>📧 contact@example.com</li>
                        <li>📞 400-123-4567</li>
                        <li>📍 北京市朝阳区科技园</li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 在线学习平台. 保留所有权利.</p>
            </div>
        </div>
    </footer>
    
    <script>
        // TODO: 练习3 - 完成JavaScript交互功能
        // 提示：使用现代JavaScript语法（ES6+）
        
        // 课程报名功能
        function enrollCourse(courseId) {
            // TODO: 实现课程报名逻辑
            const button = event.target;
            const originalText = button.textContent;
            
            // 显示加载状态
            button.innerHTML = '<span class="loading"></span> 报名中...';
            button.disabled = true;
            
            // 模拟API调用
            setTimeout(() => {
                alert(`成功报名课程 ${courseId}！`);
                button.textContent = '已报名';
                button.style.backgroundColor = '#10b981';
            }, 2000);
        }
        
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
                }
            });
        });
        
        // 滚动动画
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animationDelay = '0.1s';
                    entry.target.classList.add('fade-in-up');
                }
            });
        }, observerOptions);
        
        // 观察所有卡片元素
        document.querySelectorAll('.course-card, .testimonial-card').forEach(card => {
            observer.observe(card);
        });
        
        // 导航栏滚动效果
        window.addEventListener('scroll', () => {
            const navbar = document.querySelector('.navbar');
            if (window.scrollY > 100) {
                navbar.style.backgroundColor = 'rgba(79, 70, 229, 0.95)';
                navbar.style.backdropFilter = 'blur(10px)';
            } else {
                navbar.style.backgroundColor = '';
                navbar.style.backdropFilter = '';
            }
        });
        
        // 响应式菜单（简化版）
        // TODO: 实现完整的移动端菜单
        
        console.log('页面加载完成！开始你的学习之旅吧！');
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """
    练习1主页
    """
    return render_template_string(
        EXERCISE_TEMPLATE,
        courses=exercise_data['courses'],
        testimonials=exercise_data['testimonials']
    )

@app.route('/api/enroll', methods=['POST'])
def enroll_course():
    """
    课程报名API
    """
    data = request.get_json()
    course_id = data.get('course_id')
    
    # 模拟报名逻辑
    course = next((c for c in exercise_data['courses'] if c['id'] == course_id), None)
    if course:
        return jsonify({
            'success': True,
            'message': f'成功报名课程：{course["title"]}',
            'course': course
        })
    else:
        return jsonify({
            'success': False,
            'message': '课程不存在'
        }), 404

if __name__ == '__main__':
    print("Session19 练习1：HTML5和CSS3基础练习")
    print("=" * 50)
    print("练习内容：")
    print("1. 完善CSS样式，实现现代化的UI设计")
    print("2. 使用HTML5语义化标签优化页面结构")
    print("3. 添加JavaScript交互功能")
    print("4. 实现响应式设计")
    print("5. 优化用户体验")
    print("\n练习要求：")
    print("- 使用CSS变量管理颜色和尺寸")
    print("- 使用Flexbox和Grid布局")
    print("- 实现悬停效果和动画")
    print("- 确保移动端适配")
    print("- 添加加载状态和用户反馈")
    print("\n访问 http://localhost:5000 查看练习页面")
    
    app.run(debug=True, host='0.0.0.0', port=5000)