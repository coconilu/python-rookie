"""
Flask基础演示
展示Flask框架的核心功能
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from datetime import datetime

# 创建Flask应用实例
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 用于session和flash消息

# 模拟数据存储（实际项目应使用数据库）
posts = [
    {
        'id': 1,
        'title': '欢迎使用Flask',
        'content': 'Flask是一个轻量级的Python Web框架...',
        'author': '张三',
        'created_at': '2024-01-01',
        'views': 100
    },
    {
        'id': 2,
        'title': 'Python Web开发入门',
        'content': '本文将介绍如何使用Python进行Web开发...',
        'author': '李四',
        'created_at': '2024-01-02',
        'views': 85
    },
    {
        'id': 3,
        'title': 'Jinja2模板引擎详解',
        'content': 'Jinja2是Flask默认的模板引擎...',
        'author': '王五',
        'created_at': '2024-01-03',
        'views': 120
    }
]

# 用户评论
comments = []

# 访问统计
stats = {
    'total_visits': 0,
    'page_views': {}
}


# 1. 基本路由
@app.route('/')
def index():
    """首页 - 显示欢迎信息和功能列表"""
    stats['total_visits'] += 1
    
    features = [
        {'name': '路由演示', 'url': '/demo/routing'},
        {'name': '模板演示', 'url': '/demo/template'},
        {'name': '表单处理', 'url': '/demo/form'},
        {'name': 'JSON API', 'url': '/api/posts'},
        {'name': '文章列表', 'url': '/posts'},
        {'name': '错误处理', 'url': '/demo/error'}
    ]
    
    return render_template('demo/index.html', 
                         features=features,
                         visit_count=stats['total_visits'])


# 2. 路由演示
@app.route('/demo/routing')
def routing_demo():
    """路由功能演示"""
    return """
    <h1>路由演示</h1>
    <ul>
        <li><a href="/user/alice">动态路由: /user/alice</a></li>
        <li><a href="/user/bob">动态路由: /user/bob</a></li>
        <li><a href="/post/1">文章路由: /post/1</a></li>
        <li><a href="/post/2">文章路由: /post/2</a></li>
        <li><a href="/path/foo/bar/baz">路径匹配: /path/foo/bar/baz</a></li>
    </ul>
    <p><a href="/">返回首页</a></p>
    """


# 3. 动态路由
@app.route('/user/<username>')
def user_profile(username):
    """用户资料页面"""
    return f"""
    <h1>{username}的个人主页</h1>
    <p>这是一个动态路由示例。</p>
    <p>URL中的用户名参数: {username}</p>
    <p><a href="/">返回首页</a></p>
    """


@app.route('/post/<int:post_id>')
def show_post(post_id):
    """显示文章详情"""
    post = next((p for p in posts if p['id'] == post_id), None)
    
    if post:
        # 增加浏览次数
        post['views'] += 1
        return render_template('demo/post.html', post=post)
    else:
        return "文章不存在", 404


# 4. 路径参数
@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    """路径参数演示"""
    return f"""
    <h1>路径参数演示</h1>
    <p>完整路径: {subpath}</p>
    <p>路径分段: {subpath.split('/')}</p>
    <p><a href="/">返回首页</a></p>
    """


# 5. 模板演示
@app.route('/demo/template')
def template_demo():
    """模板功能演示"""
    data = {
        'title': '模板演示',
        'user': {'name': '访客', 'level': 'VIP'},
        'items': ['Python', 'Flask', 'Jinja2', 'HTML', 'CSS'],
        'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'show_secret': True,
        'html_content': '<strong>这是HTML内容</strong>'
    }
    return render_template('demo/template_demo.html', **data)


# 6. 表单处理
@app.route('/demo/form', methods=['GET', 'POST'])
def form_demo():
    """表单处理演示"""
    if request.method == 'POST':
        # 获取表单数据
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        subscribe = request.form.get('subscribe')
        
        # 简单验证
        if not name or not email:
            flash('姓名和邮箱是必填项！', 'error')
            return redirect(url_for('form_demo'))
        
        # 处理数据（这里只是显示）
        flash(f'感谢您的提交，{name}！我们已收到您的信息。', 'success')
        
        # 保存评论
        comment = {
            'id': len(comments) + 1,
            'name': name,
            'email': email,
            'message': message,
            'subscribe': subscribe == 'on',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        comments.append(comment)
        
        return redirect(url_for('form_demo'))
    
    return render_template('demo/form_demo.html', comments=comments)


# 7. JSON API
@app.route('/api/posts')
def api_posts():
    """返回JSON格式的文章列表"""
    return jsonify({
        'status': 'success',
        'data': posts,
        'count': len(posts)
    })


@app.route('/api/post/<int:post_id>')
def api_post(post_id):
    """返回单篇文章的JSON数据"""
    post = next((p for p in posts if p['id'] == post_id), None)
    
    if post:
        return jsonify({
            'status': 'success',
            'data': post
        })
    else:
        return jsonify({
            'status': 'error',
            'message': '文章不存在'
        }), 404


# 8. 文章列表
@app.route('/posts')
def post_list():
    """文章列表页面"""
    # 排序（按浏览量）
    sort_by = request.args.get('sort', 'views')
    sorted_posts = sorted(posts, 
                         key=lambda x: x.get(sort_by, 0), 
                         reverse=True)
    
    return render_template('demo/posts.html', posts=sorted_posts)


# 9. 错误处理演示
@app.route('/demo/error')
def error_demo():
    """错误处理演示"""
    error_type = request.args.get('type', 'none')
    
    if error_type == '404':
        # 触发404错误
        return redirect('/non-existent-page')
    elif error_type == '500':
        # 触发500错误
        raise Exception('这是一个模拟的服务器错误')
    else:
        return """
        <h1>错误处理演示</h1>
        <p>点击下面的链接查看不同的错误处理：</p>
        <ul>
            <li><a href="?type=404">404错误（页面不存在）</a></li>
            <li><a href="?type=500">500错误（服务器错误）</a></li>
        </ul>
        <p><a href="/">返回首页</a></p>
        """


# 10. 错误处理器
@app.errorhandler(404)
def page_not_found(e):
    """404错误处理"""
    return render_template('demo/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    """500错误处理"""
    return render_template('demo/500.html'), 500


# 11. 模板上下文处理器
@app.context_processor
def inject_globals():
    """注入全局模板变量"""
    return {
        'site_name': 'Flask演示站点',
        'current_year': datetime.now().year,
        'nav_items': [
            {'name': '首页', 'url': '/'},
            {'name': '文章', 'url': '/posts'},
            {'name': '关于', 'url': '/about'}
        ]
    }


# 12. 自定义过滤器
@app.template_filter('format_date')
def format_date(date_str):
    """格式化日期"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%Y年%m月%d日')
    except:
        return date_str


# 13. 关于页面
@app.route('/about')
def about():
    """关于页面"""
    return """
    <h1>关于Flask演示</h1>
    <p>这是一个Flask框架的功能演示项目。</p>
    <p>包含的功能：</p>
    <ul>
        <li>路由和视图</li>
        <li>模板渲染</li>
        <li>表单处理</li>
        <li>JSON API</li>
        <li>错误处理</li>
        <li>静态文件</li>
    </ul>
    <p>Flask版本: 3.0.0</p>
    <p><a href="/">返回首页</a></p>
    """


# 创建模板目录
def create_templates():
    """创建必要的模板文件"""
    template_dir = os.path.join(os.path.dirname(__file__), 'templates', 'demo')
    os.makedirs(template_dir, exist_ok=True)
    
    # 创建基础模板
    base_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Flask演示{% endblock %}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        nav {
            background-color: #333;
            color: white;
            padding: 10px;
            margin-bottom: 20px;
        }
        nav a {
            color: white;
            text-decoration: none;
            margin-right: 15px;
        }
        .flash-messages {
            list-style: none;
            padding: 0;
        }
        .flash-messages li {
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 3px;
        }
        .flash-messages .success {
            background-color: #d4edda;
            color: #155724;
        }
        .flash-messages .error {
            background-color: #f8d7da;
            color: #721c24;
        }
    </style>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav>
        {% for item in nav_items %}
        <a href="{{ item.url }}">{{ item.name }}</a>
        {% endfor %}
    </nav>
    
    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <ul class="flash-messages">
                {% for category, message in messages %}
                    <li class="{{ category }}">{{ message }}</li>
                {% endfor %}
                </ul>
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
        
        <hr>
        <footer>
            <p>&copy; {{ current_year }} {{ site_name }}</p>
        </footer>
    </div>
    
    {% block extra_js %}{% endblock %}
</body>
</html>"""
    
    # 保存基础模板
    with open(os.path.join(template_dir, 'base.html'), 'w', encoding='utf-8') as f:
        f.write(base_template)
    
    print("模板目录已创建")


if __name__ == '__main__':
    # 创建模板目录和文件
    create_templates()
    
    print("Flask演示应用启动中...")
    print("访问 http://127.0.0.1:5000 查看演示")
    print("按 Ctrl+C 停止服务器")
    
    # 运行应用
    app.run(debug=True, host='0.0.0.0', port=5000) 