#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
用户注册登录系统
演示Flask与SQLAlchemy集成的完整Web应用

功能特性：
- 用户注册和登录
- 密码加密存储
- 会话管理
- 用户个人信息管理
- 安全的表单验证

技术栈：
- Flask (Web框架)
- SQLAlchemy (ORM)
- Flask-Login (会话管理)
- Flask-WTF (表单处理)
- Werkzeug (密码加密)
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

# 创建Flask应用
app = Flask(__name__)

# 配置
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化扩展
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '请先登录以访问此页面'
login_manager.login_message_category = 'info'

# ==================== 数据模型 ====================

class User(UserMixin, db.Model):
    """用户模型"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # 个人信息
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(200))
    
    # 账户状态
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """设置密码（加密存储）"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """获取全名"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def get_post_count(self):
        """获取用户发布的文章数量"""
        return len(self.posts)
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.get_full_name(),
            'bio': self.bio,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'post_count': self.get_post_count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    """文章模型（扩展功能）"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(500))
    
    # 状态
    is_published = db.Column(db.Boolean, default=False)
    view_count = db.Column(db.Integer, default=0)
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def publish(self):
        """发布文章"""
        self.is_published = True
        self.published_at = datetime.utcnow()
    
    def get_summary(self, length=100):
        """获取文章摘要"""
        if self.summary:
            return self.summary
        return self.content[:length] + '...' if len(self.content) > length else self.content
    
    def __repr__(self):
        return f'<Post {self.title}>'

# ==================== 用户加载器 ====================

@login_manager.user_loader
def load_user(user_id):
    """用户加载器"""
    return User.query.get(int(user_id))

# ==================== 表单定义 ====================

class RegistrationForm(FlaskForm):
    """注册表单"""
    username = StringField('用户名', validators=[
        DataRequired(message='用户名不能为空'),
        Length(min=3, max=20, message='用户名长度必须在3-20字符之间')
    ])
    email = StringField('邮箱', validators=[
        DataRequired(message='邮箱不能为空'),
        Email(message='请输入有效的邮箱地址')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不能为空'),
        Length(min=6, message='密码长度至少6个字符')
    ])
    password2 = PasswordField('确认密码', validators=[
        DataRequired(message='请确认密码'),
        EqualTo('password', message='两次输入的密码不一致')
    ])
    submit = SubmitField('注册')
    
    def validate_username(self, username):
        """验证用户名是否已存在"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('用户名已存在，请选择其他用户名')
    
    def validate_email(self, email):
        """验证邮箱是否已存在"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('邮箱已被注册，请使用其他邮箱')

class LoginForm(FlaskForm):
    """登录表单"""
    username = StringField('用户名', validators=[
        DataRequired(message='用户名不能为空')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不能为空')
    ])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class ProfileForm(FlaskForm):
    """个人资料表单"""
    first_name = StringField('名', validators=[Length(max=50)])
    last_name = StringField('姓', validators=[Length(max=50)])
    email = StringField('邮箱', validators=[
        DataRequired(message='邮箱不能为空'),
        Email(message='请输入有效的邮箱地址')
    ])
    bio = TextAreaField('个人简介', validators=[Length(max=500)])
    submit = SubmitField('更新资料')
    
    def __init__(self, original_email, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.original_email = original_email
    
    def validate_email(self, email):
        """验证邮箱是否已被其他用户使用"""
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('此邮箱已被其他用户使用')

class PostForm(FlaskForm):
    """发布文章表单"""
    title = StringField('标题', validators=[
        DataRequired(message='标题不能为空'),
        Length(max=200, message='标题长度不能超过200字符')
    ])
    content = TextAreaField('内容', validators=[
        DataRequired(message='内容不能为空')
    ])
    summary = StringField('摘要', validators=[Length(max=500)])
    is_published = BooleanField('立即发布')
    submit = SubmitField('保存')

# ==================== 路由定义 ====================

@app.route('/')
def index():
    """首页"""
    # 获取最新发布的文章
    recent_posts = Post.query.filter_by(is_published=True)\
        .order_by(Post.published_at.desc()).limit(5).all()
    
    # 获取用户统计
    total_users = User.query.count()
    total_posts = Post.query.filter_by(is_published=True).count()
    
    return render_template('index.html', 
                         recent_posts=recent_posts,
                         total_users=total_users,
                         total_posts=total_posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # 创建新用户
            user = User(
                username=form.username.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            
            # 保存到数据库
            db.session.add(user)
            db.session.commit()
            
            flash('注册成功！请登录。', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            flash('注册失败，请重试。', 'error')
            app.logger.error(f'Registration error: {str(e)}')
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # 查找用户
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('账户已被禁用，请联系管理员。', 'error')
                return render_template('login.html', form=form)
            
            # 更新最后登录时间
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # 登录用户
            login_user(user, remember=form.remember_me.data)
            flash(f'欢迎回来，{user.username}！', 'success')
            
            # 重定向到原来的页面或首页
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('用户名或密码错误。', 'error')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """用户登出"""
    logout_user()
    flash('已成功退出登录。', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """用户仪表板"""
    # 获取用户的文章
    user_posts = Post.query.filter_by(user_id=current_user.id)\
        .order_by(Post.created_at.desc()).all()
    
    # 统计信息
    stats = {
        'total_posts': len(user_posts),
        'published_posts': len([p for p in user_posts if p.is_published]),
        'draft_posts': len([p for p in user_posts if not p.is_published]),
        'total_views': sum(p.view_count for p in user_posts)
    }
    
    return render_template('dashboard.html', posts=user_posts, stats=stats)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """个人资料管理"""
    form = ProfileForm(current_user.email)
    
    if form.validate_on_submit():
        try:
            # 更新用户信息
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.email = form.email.data
            current_user.bio = form.bio.data
            current_user.updated_at = datetime.utcnow()
            
            db.session.commit()
            flash('个人资料更新成功！', 'success')
            return redirect(url_for('profile'))
            
        except Exception as e:
            db.session.rollback()
            flash('更新失败，请重试。', 'error')
            app.logger.error(f'Profile update error: {str(e)}')
    
    elif request.method == 'GET':
        # 预填充表单
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.bio.data = current_user.bio
    
    return render_template('profile.html', form=form)

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    """创建新文章"""
    form = PostForm()
    
    if form.validate_on_submit():
        try:
            # 创建新文章
            post = Post(
                title=form.title.data,
                content=form.content.data,
                summary=form.summary.data,
                author=current_user
            )
            
            if form.is_published.data:
                post.publish()
            
            db.session.add(post)
            db.session.commit()
            
            flash('文章创建成功！', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash('创建失败，请重试。', 'error')
            app.logger.error(f'Post creation error: {str(e)}')
    
    return render_template('new_post.html', form=form)

@app.route('/post/<int:id>')
def view_post(id):
    """查看文章"""
    post = Post.query.get_or_404(id)
    
    # 如果文章未发布且不是作者，则返回404
    if not post.is_published and (not current_user.is_authenticated or current_user != post.author):
        return render_template('404.html'), 404
    
    # 增加浏览量
    post.view_count += 1
    db.session.commit()
    
    return render_template('view_post.html', post=post)

@app.route('/users')
def users():
    """用户列表"""
    page = request.args.get('page', 1, type=int)
    users = User.query.filter_by(is_active=True)\
        .order_by(User.created_at.desc())\
        .paginate(page=page, per_page=10, error_out=False)
    
    return render_template('users.html', users=users)

@app.route('/api/user/<int:id>')
def api_user(id):
    """用户API（JSON格式）"""
    user = User.query.get_or_404(id)
    return user.to_dict()

# ==================== 错误处理 ====================

@app.errorhandler(404)
def not_found_error(error):
    """404错误处理"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    db.session.rollback()
    return render_template('500.html'), 500

# ==================== 应用初始化 ====================

def create_sample_data():
    """创建示例数据"""
    # 检查是否已有数据
    if User.query.count() > 0:
        return
    
    # 创建示例用户
    admin = User(
        username='admin',
        email='admin@example.com',
        first_name='管理员',
        last_name='用户',
        bio='系统管理员账户',
        is_verified=True
    )
    admin.set_password('admin123')
    
    demo_user = User(
        username='demo',
        email='demo@example.com',
        first_name='演示',
        last_name='用户',
        bio='这是一个演示账户',
        is_verified=True
    )
    demo_user.set_password('demo123')
    
    db.session.add_all([admin, demo_user])
    db.session.commit()
    
    # 创建示例文章
    posts = [
        Post(
            title='欢迎使用用户注册登录系统',
            content='这是一个使用Flask和SQLAlchemy构建的用户注册登录系统演示。\n\n'
                   '主要功能包括：\n'
                   '- 用户注册和登录\n'
                   '- 密码加密存储\n'
                   '- 会话管理\n'
                   '- 个人资料管理\n'
                   '- 文章发布系统',
            summary='用户注册登录系统功能介绍',
            author=admin
        ),
        Post(
            title='如何使用SQLAlchemy ORM',
            content='SQLAlchemy是Python中最强大的ORM框架之一。\n\n'
                   '主要特性：\n'
                   '- 强大的查询API\n'
                   '- 关系映射\n'
                   '- 数据库迁移\n'
                   '- 连接池管理',
            summary='SQLAlchemy ORM使用指南',
            author=demo_user
        )
    ]
    
    for post in posts:
        post.publish()
        db.session.add(post)
    
    db.session.commit()
    print("示例数据创建完成！")

def init_app():
    """初始化应用"""
    with app.app_context():
        # 创建数据库表
        db.create_all()
        
        # 创建示例数据
        create_sample_data()

# ==================== 主函数 ====================

if __name__ == '__main__':
    # 初始化应用
    init_app()
    
    print("=" * 50)
    print("用户注册登录系统启动")
    print("=" * 50)
    print("访问 http://127.0.0.1:5000 开始体验")
    print("\n演示账户：")
    print("- 用户名: admin, 密码: admin123")
    print("- 用户名: demo, 密码: demo123")
    print("\n按 Ctrl+C 退出")
    print("=" * 50)
    
    # 启动应用
    app.run(debug=True, host='127.0.0.1', port=5000) 