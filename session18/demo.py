#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
第18课：数据库集成演示
SQLAlchemy ORM基础演示，包括模型定义、数据操作和关系处理

作者：Python新手教程
创建时间：2024年1月
"""

from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# 创建Flask应用
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///demo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'demo-secret-key'

# 初始化数据库
db = SQLAlchemy(app)

# ==================== 模型定义 ====================

class User(db.Model):
    """用户模型"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # 一对多关系：用户可以有多篇文章
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Category(db.Model):
    """分类模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    
    # 一对多关系：分类可以有多篇文章
    posts = db.relationship('Post', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Post(db.Model):
    """文章模型"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)
    view_count = db.Column(db.Integer, default=0)
    
    # 外键关系
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    
    def __repr__(self):
        return f'<Post {self.title}>'

# 多对多关系：文章和标签
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Tag(db.Model):
    """标签模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    
    # 多对多关系：标签可以属于多篇文章
    posts = db.relationship('Post', secondary=post_tags, lazy='subquery',
                          backref=db.backref('tags', lazy=True))
    
    def __repr__(self):
        return f'<Tag {self.name}>'

# ==================== 演示函数 ====================

def demo_basic_operations():
    """演示基础CRUD操作"""
    print("\n=== 基础CRUD操作演示 ===")
    
    # 创建用户
    user1 = User(username='alice', email='alice@example.com')
    user1.set_password('password123')
    
    user2 = User(username='bob', email='bob@example.com')
    user2.set_password('password456')
    
    # 添加到数据库
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    
    print(f"创建用户: {user1.username}, {user2.username}")
    
    # 查询操作
    all_users = User.query.all()
    print(f"所有用户: {[user.username for user in all_users]}")
    
    # 条件查询
    alice = User.query.filter_by(username='alice').first()
    print(f"查询用户 Alice: {alice}")
    
    # 更新操作
    alice.email = 'alice.new@example.com'
    db.session.commit()
    print(f"更新 Alice 邮箱: {alice.email}")
    
    # 密码验证
    print(f"密码验证: {alice.check_password('password123')}")

def demo_relationships():
    """演示表关系操作"""
    print("\n=== 表关系操作演示 ===")
    
    # 创建分类
    tech_category = Category(name='技术', description='技术相关文章')
    life_category = Category(name='生活', description='生活分享文章')
    
    db.session.add_all([tech_category, life_category])
    db.session.commit()
    
    # 创建标签
    python_tag = Tag(name='Python')
    web_tag = Tag(name='Web开发')
    tutorial_tag = Tag(name='教程')
    
    db.session.add_all([python_tag, web_tag, tutorial_tag])
    db.session.commit()
    
    # 获取用户
    alice = User.query.filter_by(username='alice').first()
    bob = User.query.filter_by(username='bob').first()
    
    # 创建文章
    post1 = Post(
        title='Python Flask教程',
        content='这是一篇关于Flask的详细教程...',
        author=alice,
        category=tech_category,
        is_published=True
    )
    
    post2 = Post(
        title='我的编程心得',
        content='分享我学习编程的一些心得体会...',
        author=bob,
        category=life_category,
        is_published=True
    )
    
    # 为文章添加标签（多对多关系）
    post1.tags.extend([python_tag, web_tag, tutorial_tag])
    post2.tags.append(python_tag)
    
    db.session.add_all([post1, post2])
    db.session.commit()
    
    print(f"创建文章: {post1.title}, {post2.title}")
    
    # 查询关系数据
    print(f"Alice 的文章: {[post.title for post in alice.posts]}")
    print(f"技术分类的文章: {[post.title for post in tech_category.posts]}")
    print(f"Python 标签的文章: {[post.title for post in python_tag.posts]}")
    print(f"第一篇文章的标签: {[tag.name for tag in post1.tags]}")

def demo_advanced_queries():
    """演示高级查询操作"""
    print("\n=== 高级查询操作演示 ===")
    
    # 连接查询
    results = db.session.query(Post, User, Category).join(User).join(Category).all()
    print("连接查询结果:")
    for post, user, category in results:
        print(f"  文章: {post.title}, 作者: {user.username}, 分类: {category.name}")
    
    # 条件查询
    published_posts = Post.query.filter(Post.is_published == True).all()
    print(f"\n已发布的文章: {[post.title for post in published_posts]}")
    
    # 排序查询
    latest_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    print(f"最新文章: {[post.title for post in latest_posts]}")
    
    # 聚合查询
    user_post_count = db.session.query(User.username, db.func.count(Post.id)).\
        join(Post).group_by(User.id).all()
    print("用户文章统计:")
    for username, count in user_post_count:
        print(f"  {username}: {count} 篇文章")
    
    # 子查询
    active_users = User.query.filter(User.is_active == True).subquery()
    posts_by_active_users = db.session.query(Post).join(
        active_users, Post.user_id == active_users.c.id
    ).all()
    print(f"活跃用户的文章: {[post.title for post in posts_by_active_users]}")

def demo_model_methods():
    """演示模型方法"""
    print("\n=== 模型方法演示 ===")
    
    # 获取用户
    alice = User.query.filter_by(username='alice').first()
    
    # 使用模型方法
    print(f"用户信息: {alice}")
    print(f"用户文章数: {len(alice.posts)}")
    
    # 获取文章
    post = Post.query.first()
    if post:
        print(f"文章: {post.title}")
        print(f"作者: {post.author.username}")
        print(f"分类: {post.category.name}")
        print(f"标签: {[tag.name for tag in post.tags]}")

# ==================== Flask路由 ====================

@app.route('/')
def index():
    """首页，显示数据库内容"""
    users = User.query.all()
    posts = Post.query.all()
    categories = Category.query.all()
    tags = Tag.query.all()
    
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>数据库集成演示</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .section { margin: 20px 0; padding: 20px; border: 1px solid #ddd; }
            .user, .post, .category, .tag { 
                margin: 10px 0; padding: 10px; background-color: #f9f9f9; 
            }
            h1, h2 { color: #333; }
        </style>
    </head>
    <body>
        <h1>Flask数据库集成演示</h1>
        
        <div class="section">
            <h2>用户列表 ({{ users|length }})</h2>
            {% for user in users %}
            <div class="user">
                <strong>{{ user.username }}</strong> ({{ user.email }})
                <br>创建时间: {{ user.created_at.strftime('%Y-%m-%d %H:%M') }}
                <br>文章数: {{ user.posts|length }}
            </div>
            {% endfor %}
        </div>
        
        <div class="section">
            <h2>文章列表 ({{ posts|length }})</h2>
            {% for post in posts %}
            <div class="post">
                <strong>{{ post.title }}</strong>
                <br>作者: {{ post.author.username }}
                <br>分类: {{ post.category.name }}
                <br>标签: {{ post.tags|map(attribute='name')|join(', ') }}
                <br>状态: {{ '已发布' if post.is_published else '草稿' }}
                <br>创建时间: {{ post.created_at.strftime('%Y-%m-%d %H:%M') }}
            </div>
            {% endfor %}
        </div>
        
        <div class="section">
            <h2>分类列表 ({{ categories|length }})</h2>
            {% for category in categories %}
            <div class="category">
                <strong>{{ category.name }}</strong>
                <br>描述: {{ category.description }}
                <br>文章数: {{ category.posts|length }}
            </div>
            {% endfor %}
        </div>
        
        <div class="section">
            <h2>标签列表 ({{ tags|length }})</h2>
            {% for tag in tags %}
            <div class="tag">
                <strong>{{ tag.name }}</strong>
                <br>使用次数: {{ tag.posts|length }}
            </div>
            {% endfor %}
        </div>
        
        <div class="section">
            <h2>操作说明</h2>
            <p>本演示展示了SQLAlchemy ORM的基本功能：</p>
            <ul>
                <li>用户模型：包含用户名、邮箱、密码等信息</li>
                <li>文章模型：与用户和分类建立外键关系</li>
                <li>分类模型：文章的分类信息</li>
                <li>标签模型：与文章建立多对多关系</li>
            </ul>
            <p>数据关系：</p>
            <ul>
                <li>用户 ←→ 文章：一对多关系</li>
                <li>分类 ←→ 文章：一对多关系</li>
                <li>标签 ←→ 文章：多对多关系</li>
            </ul>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(template, 
                                users=users, 
                                posts=posts, 
                                categories=categories, 
                                tags=tags)

@app.route('/reset')
def reset_database():
    """重置数据库"""
    try:
        # 删除所有表
        db.drop_all()
        # 重新创建表
        db.create_all()
        
        # 运行演示
        demo_basic_operations()
        demo_relationships()
        demo_advanced_queries()
        demo_model_methods()
        
        return "<h1>数据库重置成功！</h1><p><a href='/'>返回首页</a></p>"
    except Exception as e:
        return f"<h1>重置失败：{str(e)}</h1><p><a href='/'>返回首页</a></p>"

# ==================== 主函数 ====================

def main():
    """主函数"""
    print("=" * 50)
    print("第18课：数据库集成演示")
    print("SQLAlchemy ORM基础操作")
    print("=" * 50)
    
    with app.app_context():
        # 创建所有表
        db.create_all()
        
        # 检查是否有数据
        if User.query.count() == 0:
            print("首次运行，创建演示数据...")
            demo_basic_operations()
            demo_relationships()
            demo_advanced_queries()
            demo_model_methods()
        else:
            print("数据库已有数据，跳过初始化")
    
    print("\n" + "=" * 50)
    print("演示完成！")
    print("启动Web服务器查看结果...")
    print("访问 http://127.0.0.1:5000 查看数据")
    print("访问 http://127.0.0.1:5000/reset 重置数据库")
    print("按 Ctrl+C 退出")
    print("=" * 50)
    
    # 启动Flask应用
    app.run(debug=True, host='127.0.0.1', port=5000)

if __name__ == '__main__':
    main() 