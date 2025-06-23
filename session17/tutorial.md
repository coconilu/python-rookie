# Flask Web开发入门详细教程

## 目录

1. [Web开发基础概念](#1-web开发基础概念)
2. [Flask框架介绍](#2-flask框架介绍)
3. [路由与视图详解](#3-路由与视图详解)
4. [Jinja2模板引擎](#4-jinja2模板引擎)
5. [静态文件处理](#5-静态文件处理)
6. [表单处理](#6-表单处理)
7. [项目实战：个人博客系统](#7-项目实战个人博客系统)
8. [总结与扩展](#8-总结与扩展)

## 1. Web开发基础概念

### 1.1 什么是Web应用

Web应用是通过网络浏览器访问的应用程序。它基于客户端-服务器架构：

- **客户端**：用户的浏览器
- **服务器**：运行Web应用的计算机
- **HTTP协议**：客户端和服务器之间的通信协议

### 1.2 HTTP协议基础

HTTP（HyperText Transfer Protocol）是Web的基础协议：

- **请求方法**：
  - GET：获取资源
  - POST：提交数据
  - PUT：更新资源
  - DELETE：删除资源

- **状态码**：
  - 200：成功
  - 404：未找到
  - 500：服务器错误

### 1.3 Web框架的作用

Web框架帮助我们：
- 处理HTTP请求和响应
- 管理路由（URL到函数的映射）
- 渲染HTML模板
- 处理表单和用户输入
- 管理会话和Cookie

## 2. Flask框架介绍

### 2.1 什么是Flask

Flask是一个轻量级的Python Web框架，具有以下特点：

- **微框架**：核心简单，功能通过扩展实现
- **灵活性高**：不强制特定的项目结构
- **易于学习**：API简洁明了
- **社区活跃**：有丰富的第三方扩展

### 2.2 Flask vs Django

| 特性 | Flask | Django |
|------|-------|--------|
| 类型 | 微框架 | 全功能框架 |
| 学习曲线 | 平缓 | 陡峭 |
| 灵活性 | 高 | 中等 |
| 内置功能 | 少 | 多 |
| 适用场景 | 小型项目、API | 大型项目 |

### 2.3 安装Flask

```bash
# 使用uv安装
uv add flask

# 或使用pip
pip install flask
```

### 2.4 第一个Flask应用

```python
from flask import Flask

# 创建Flask应用实例
app = Flask(__name__)

# 定义路由和视图函数
@app.route('/')
def hello_world():
    return 'Hello, Flask!'

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)
```

## 3. 路由与视图详解

### 3.1 路由的概念

路由是URL路径到Python函数的映射。Flask使用装饰器来定义路由。

### 3.2 基本路由

```python
@app.route('/')
def index():
    return '首页'

@app.route('/about')
def about():
    return '关于我们'

@app.route('/contact')
def contact():
    return '联系我们'
```

### 3.3 动态路由

动态路由可以接收URL中的参数：

```python
# 字符串参数
@app.route('/user/<username>')
def show_user(username):
    return f'用户：{username}'

# 整数参数
@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'文章ID：{post_id}'

# 路径参数
@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return f'路径：{subpath}'
```

### 3.4 HTTP方法

```python
from flask import request

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 处理登录表单
        username = request.form['username']
        password = request.form['password']
        return f'登录用户：{username}'
    else:
        # 显示登录表单
        return '显示登录表单'
```

### 3.5 URL构建

使用`url_for`函数构建URL：

```python
from flask import url_for

@app.route('/')
def index():
    return '首页'

@app.route('/user/<username>')
def profile(username):
    return f'{username}的个人主页'

# 在其他地方使用
with app.test_request_context():
    print(url_for('index'))  # 输出: /
    print(url_for('profile', username='john'))  # 输出: /user/john
```

## 4. Jinja2模板引擎

### 4.1 模板的作用

模板将HTML结构与Python代码分离，使代码更清晰、更易维护。

### 4.2 基本语法

#### 变量输出
```html
<h1>{{ title }}</h1>
<p>欢迎，{{ username }}！</p>
```

#### 表达式
```html
<p>{{ 2 + 2 }}</p>
<p>{{ user.name.upper() }}</p>
```

#### 控制结构
```html
<!-- 条件语句 -->
{% if user %}
    <h1>Hello {{ user.name }}!</h1>
{% else %}
    <h1>Hello, Guest!</h1>
{% endif %}

<!-- 循环语句 -->
<ul>
{% for item in items %}
    <li>{{ item }}</li>
{% endfor %}
</ul>
```

### 4.3 模板继承

基础模板（base.html）：
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}默认标题{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <nav>
        <ul>
            <li><a href="/">首页</a></li>
            <li><a href="/about">关于</a></li>
        </ul>
    </nav>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        <p>&copy; 2024 我的博客</p>
    </footer>
</body>
</html>
```

子模板（index.html）：
```html
{% extends "base.html" %}

{% block title %}首页 - 我的博客{% endblock %}

{% block content %}
    <h1>欢迎来到我的博客</h1>
    <p>这是首页内容。</p>
{% endblock %}
```

### 4.4 模板过滤器

```html
<!-- 字符串过滤器 -->
<p>{{ name|upper }}</p>
<p>{{ name|lower }}</p>
<p>{{ name|title }}</p>
<p>{{ name|trim }}</p>

<!-- 列表过滤器 -->
<p>{{ items|length }}</p>
<p>{{ items|first }}</p>
<p>{{ items|last }}</p>
<p>{{ items|join(', ') }}</p>

<!-- 默认值 -->
<p>{{ username|default('游客') }}</p>

<!-- 安全输出HTML -->
<div>{{ html_content|safe }}</div>
```

### 4.5 在Flask中使用模板

```python
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html', 
                         title='我的博客',
                         posts=get_recent_posts())

@app.route('/user/<username>')
def user_profile(username):
    user = get_user(username)
    return render_template('profile.html', user=user)
```

## 5. 静态文件处理

### 5.1 静态文件目录

Flask默认在`static`目录中查找静态文件：

```
project/
├── app.py
├── templates/
└── static/
    ├── css/
    │   └── style.css
    ├── js/
    │   └── script.js
    └── images/
        └── logo.png
```

### 5.2 在模板中引用静态文件

```html
<!-- CSS文件 -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">

<!-- JavaScript文件 -->
<script src="{{ url_for('static', filename='js/script.js') }}"></script>

<!-- 图片文件 -->
<img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo">
```

## 6. 表单处理

### 6.1 HTML表单

```html
<form method="POST" action="/submit">
    <label for="username">用户名：</label>
    <input type="text" id="username" name="username" required>
    
    <label for="email">邮箱：</label>
    <input type="email" id="email" name="email" required>
    
    <label for="message">留言：</label>
    <textarea id="message" name="message" rows="4"></textarea>
    
    <button type="submit">提交</button>
</form>
```

### 6.2 处理表单数据

```python
from flask import request, redirect, url_for, flash

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # 验证数据
        if not username or not email:
            flash('用户名和邮箱是必填项！')
            return redirect(url_for('submit'))
        
        # 处理数据（例如保存到数据库）
        save_message(username, email, message)
        
        flash('提交成功！')
        return redirect(url_for('thank_you'))
    
    return render_template('submit.html')
```

### 6.3 文件上传

```python
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('文件上传成功！')
            return redirect(url_for('uploaded_file', filename=filename))
    
    return render_template('upload.html')
```

## 7. 项目实战：个人博客系统

### 7.1 项目需求

创建一个简单的个人博客系统，包含以下功能：
- 首页显示文章列表
- 文章详情页
- 发布新文章
- 关于页面
- 简单的样式设计

### 7.2 项目结构

```
blog/
├── app.py              # 主应用文件
├── models.py           # 数据模型
├── templates/          # 模板文件
│   ├── base.html      # 基础模板
│   ├── index.html     # 首页
│   ├── post.html      # 文章详情
│   ├── new_post.html  # 新建文章
│   └── about.html     # 关于页面
├── static/            # 静态文件
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
└── data/              # 数据存储
    └── posts.json     # 文章数据
```

### 7.3 核心代码实现

详细的项目代码将在`project`目录中提供。

## 8. 总结与扩展

### 8.1 本课重点回顾

- Flask是一个轻量级的Python Web框架
- 路由将URL映射到视图函数
- Jinja2模板引擎用于生成动态HTML
- 静态文件通过`static`目录提供
- 表单处理需要考虑安全性和验证

### 8.2 进阶学习方向

1. **数据库集成**：学习SQLAlchemy ORM
2. **用户认证**：使用Flask-Login
3. **RESTful API**：构建API服务
4. **部署**：将应用部署到服务器
5. **扩展**：探索Flask生态系统

### 8.3 推荐资源

- [Flask官方教程](https://flask.palletsprojects.com/tutorial/)
- [Flask Web开发实战](https://book.douban.com/subject/35816707/)
- [The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

### 8.4 练习建议

1. 完成本课的所有练习题
2. 尝试为博客添加更多功能
3. 探索Flask的扩展库
4. 部署你的第一个Web应用

记住：Web开发是一个实践性很强的领域，多动手、多尝试是提高的关键！ 