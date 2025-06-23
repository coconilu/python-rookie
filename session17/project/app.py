"""
个人博客系统
一个简单但功能完整的Flask博客应用
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import json
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-for-blog'

# 数据文件路径
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'posts.json')

# 确保数据目录存在
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

# 简单的认证装饰器
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != 'admin' or auth.password != 'password':
            return 'Authentication required', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}
        return f(*args, **kwargs)
    return decorated_function


class BlogPost:
    """博客文章类"""
    def __init__(self, id, title, content, author, created_at=None, updated_at=None, tags=None, views=0):
        self.id = id
        self.title = title
        self.content = content
        self.author = author
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or self.created_at
        self.tags = tags or []
        self.views = views
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'tags': self.tags,
            'views': self.views
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建实例"""
        return cls(
            id=data['id'],
            title=data['title'],
            content=data['content'],
            author=data['author'],
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            tags=data.get('tags', []),
            views=data.get('views', 0)
        )


class BlogManager:
    """博客管理器"""
    def __init__(self, data_file):
        self.data_file = data_file
        self.posts = self.load_posts()
    
    def load_posts(self):
        """从文件加载文章"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return [BlogPost.from_dict(post) for post in data]
            except:
                return []
        return []
    
    def save_posts(self):
        """保存文章到文件"""
        data = [post.to_dict() for post in self.posts]
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_all_posts(self):
        """获取所有文章"""
        return sorted(self.posts, key=lambda x: x.created_at, reverse=True)
    
    def get_post(self, post_id):
        """根据ID获取文章"""
        for post in self.posts:
            if post.id == post_id:
                return post
        return None
    
    def create_post(self, title, content, author, tags=None):
        """创建新文章"""
        new_id = max([p.id for p in self.posts], default=0) + 1
        post = BlogPost(new_id, title, content, author, tags=tags)
        self.posts.append(post)
        self.save_posts()
        return post
    
    def update_post(self, post_id, title, content, tags=None):
        """更新文章"""
        post = self.get_post(post_id)
        if post:
            post.title = title
            post.content = content
            post.tags = tags or []
            post.updated_at = datetime.now()
            self.save_posts()
            return True
        return False
    
    def delete_post(self, post_id):
        """删除文章"""
        post = self.get_post(post_id)
        if post:
            self.posts.remove(post)
            self.save_posts()
            return True
        return False
    
    def increment_views(self, post_id):
        """增加浏览次数"""
        post = self.get_post(post_id)
        if post:
            post.views += 1
            self.save_posts()
    
    def search_posts(self, query):
        """搜索文章"""
        query = query.lower()
        results = []
        for post in self.posts:
            if (query in post.title.lower() or 
                query in post.content.lower() or
                any(query in tag.lower() for tag in post.tags)):
                results.append(post)
        return sorted(results, key=lambda x: x.created_at, reverse=True)
    
    def get_posts_by_tag(self, tag):
        """根据标签获取文章"""
        return [post for post in self.posts if tag in post.tags]
    
    def get_all_tags(self):
        """获取所有标签"""
        tags = {}
        for post in self.posts:
            for tag in post.tags:
                tags[tag] = tags.get(tag, 0) + 1
        return tags


# 创建博客管理器实例
blog_manager = BlogManager(DATA_FILE)


# 自定义过滤器
@app.template_filter('format_date')
def format_date_filter(date):
    """格式化日期"""
    if isinstance(date, str):
        date = datetime.fromisoformat(date)
    return date.strftime('%Y年%m月%d日')


@app.template_filter('format_datetime')
def format_datetime_filter(date):
    """格式化日期时间"""
    if isinstance(date, str):
        date = datetime.fromisoformat(date)
    return date.strftime('%Y-%m-%d %H:%M')


@app.template_filter('truncate_content')
def truncate_content_filter(content, length=200):
    """截断内容"""
    if len(content) > length:
        return content[:length] + '...'
    return content


# 路由定义
@app.route('/')
def index():
    """首页 - 显示文章列表"""
    posts = blog_manager.get_all_posts()
    return render_template('index.html', posts=posts)


@app.route('/post/<int:post_id>')
def post_detail(post_id):
    """文章详情页"""
    post = blog_manager.get_post(post_id)
    if not post:
        flash('文章不存在', 'error')
        return redirect(url_for('index'))
    
    # 增加浏览次数
    blog_manager.increment_views(post_id)
    
    # 获取相关文章（同标签的其他文章）
    related_posts = []
    if post.tags:
        for tag in post.tags:
            for p in blog_manager.get_posts_by_tag(tag):
                if p.id != post_id and p not in related_posts:
                    related_posts.append(p)
    
    return render_template('post.html', post=post, related_posts=related_posts[:3])


@app.route('/new', methods=['GET', 'POST'])
@require_auth
def new_post():
    """创建新文章"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        tags = request.form.get('tags', '').strip()
        
        if not title or not content:
            flash('标题和内容不能为空', 'error')
            return redirect(url_for('new_post'))
        
        # 处理标签
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        
        # 创建文章
        post = blog_manager.create_post(
            title=title,
            content=content,
            author='Admin',
            tags=tag_list
        )
        
        flash('文章发布成功！', 'success')
        return redirect(url_for('post_detail', post_id=post.id))
    
    return render_template('new_post.html')


@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@require_auth
def edit_post(post_id):
    """编辑文章"""
    post = blog_manager.get_post(post_id)
    if not post:
        flash('文章不存在', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        tags = request.form.get('tags', '').strip()
        
        if not title or not content:
            flash('标题和内容不能为空', 'error')
            return redirect(url_for('edit_post', post_id=post_id))
        
        # 处理标签
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        
        # 更新文章
        if blog_manager.update_post(post_id, title, content, tag_list):
            flash('文章更新成功！', 'success')
            return redirect(url_for('post_detail', post_id=post_id))
    
    return render_template('edit_post.html', post=post)


@app.route('/delete/<int:post_id>', methods=['POST'])
@require_auth
def delete_post(post_id):
    """删除文章"""
    if blog_manager.delete_post(post_id):
        flash('文章已删除', 'success')
    else:
        flash('文章不存在', 'error')
    
    return redirect(url_for('index'))


@app.route('/search')
def search():
    """搜索文章"""
    query = request.args.get('q', '').strip()
    
    if query:
        posts = blog_manager.search_posts(query)
        flash(f'搜索 "{query}" 找到 {len(posts)} 篇文章', 'info')
    else:
        posts = blog_manager.get_all_posts()
    
    return render_template('index.html', posts=posts, search_query=query)


@app.route('/tag/<tag>')
def posts_by_tag(tag):
    """按标签筛选文章"""
    posts = blog_manager.get_posts_by_tag(tag)
    return render_template('index.html', posts=posts, current_tag=tag)


@app.route('/about')
def about():
    """关于页面"""
    return render_template('about.html')


@app.route('/admin')
@require_auth
def admin():
    """管理页面"""
    posts = blog_manager.get_all_posts()
    return render_template('admin.html', posts=posts)


# 错误处理
@app.errorhandler(404)
def page_not_found(e):
    """404错误页面"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    """500错误页面"""
    return render_template('500.html'), 500


# 上下文处理器
@app.context_processor
def inject_globals():
    """注入全局变量"""
    return {
        'site_name': '我的个人博客',
        'current_year': datetime.now().year,
        'all_tags': blog_manager.get_all_tags()
    }


# 初始化示例数据
def init_sample_data():
    """初始化示例数据"""
    if not blog_manager.posts:
        sample_posts = [
            {
                'title': '欢迎来到我的博客',
                'content': '''这是我的第一篇博客文章！

我很高兴能够使用Flask创建自己的博客系统。这个博客系统虽然简单，但是包含了一个博客应该有的基本功能：

- 文章的创建、编辑和删除
- 文章列表和详情页
- 标签系统
- 搜索功能
- 简单的管理界面

希望通过这个项目，我能够：
1. 深入学习Flask框架
2. 理解Web开发的基本概念
3. 提升自己的编程能力

让我们一起开始这段学习之旅吧！''',
                'author': 'Admin',
                'tags': ['Flask', 'Python', '博客']
            },
            {
                'title': 'Flask学习笔记：路由系统',
                'content': '''今天学习了Flask的路由系统，收获很大。

## 什么是路由？

路由是Web框架中的核心概念，它定义了URL路径与处理函数之间的映射关系。

## Flask中的路由

在Flask中，我们使用装饰器来定义路由：

```python
@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/user/<username>')
def user_profile(username):
    return f'Welcome, {username}!'
```

## 动态路由

Flask支持动态路由，可以在URL中包含变量：

- `<variable>` - 匹配任意字符串
- `<int:variable>` - 匹配整数
- `<float:variable>` - 匹配浮点数
- `<path:variable>` - 匹配路径

## HTTP方法

默认情况下，路由只响应GET请求。可以通过methods参数指定其他HTTP方法：

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 处理登录
        pass
    else:
        # 显示登录表单
        pass
```

继续加油学习！''',
                'author': 'Admin',
                'tags': ['Flask', '学习笔记', '路由']
            },
            {
                'title': 'Jinja2模板引擎入门',
                'content': '''Jinja2是Flask默认的模板引擎，功能强大且易于使用。

## 基本语法

### 变量输出
```
{{ variable }}
{{ user.name }}
{{ items[0] }}
```

### 控制结构
```
{% if condition %}
    ...
{% endif %}

{% for item in items %}
    {{ item }}
{% endfor %}
```

### 过滤器
```
{{ name|upper }}
{{ price|round(2) }}
{{ text|truncate(100) }}
```

## 模板继承

模板继承是Jinja2的强大特性之一：

基础模板（base.html）：
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

子模板：
```html
{% extends "base.html" %}

{% block title %}首页{% endblock %}

{% block content %}
    <h1>欢迎</h1>
{% endblock %}
```

## 宏（Macro）

宏类似于函数，可以重复使用：

```
{% macro render_item(item) %}
    <div class="item">
        <h3>{{ item.title }}</h3>
        <p>{{ item.description }}</p>
    </div>
{% endmacro %}
```

模板引擎让HTML页面变得更加灵活和强大！''',
                'author': 'Admin',
                'tags': ['Jinja2', '模板', '学习笔记']
            }
        ]
        
        for post_data in sample_posts:
            blog_manager.create_post(
                title=post_data['title'],
                content=post_data['content'],
                author=post_data['author'],
                tags=post_data['tags']
            )
        
        print(f"已创建 {len(sample_posts)} 篇示例文章")


if __name__ == '__main__':
    # 初始化示例数据
    init_sample_data()
    
    print("个人博客系统启动中...")
    print("访问 http://127.0.0.1:5000 查看博客")
    print("管理员登录：")
    print("  用户名：admin")
    print("  密码：password")
    
    app.run(debug=True) 