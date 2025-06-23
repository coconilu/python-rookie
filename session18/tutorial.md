# Flask数据库集成详细教程

## 目录

1. [ORM概念与SQLAlchemy介绍](#1-orm概念与sqlalchemy介绍)
2. [Flask-SQLAlchemy配置](#2-flask-sqlalchemy配置)
3. [数据模型设计](#3-数据模型设计)
4. [数据库操作基础](#4-数据库操作基础)
5. [数据库关系](#5-数据库关系)
6. [数据库迁移](#6-数据库迁移)
7. [用户认证系统实战](#7-用户认证系统实战)
8. [会话管理](#8-会话管理)
9. [安全考虑](#9-安全考虑)
10. [性能优化](#10-性能优化)
11. [总结与最佳实践](#11-总结与最佳实践)

## 1. ORM概念与SQLAlchemy介绍

### 1.1 什么是ORM

ORM（Object-Relational Mapping，对象关系映射）是一种编程技术，用于在面向对象编程语言中操作关系数据库。

**传统SQL方式的问题：**
```python
# 传统方式：手写SQL
cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

**ORM的优势：**
- **类型安全**：编译时检查错误
- **代码复用**：模型定义可复用
- **数据库无关**：支持多种数据库
- **防止SQL注入**：自动参数化查询
- **关系处理**：自动处理表关系

### 1.2 SQLAlchemy特点

SQLAlchemy是Python最强大的ORM框架：

- **Core和ORM两层架构**
- **灵活的查询API**
- **支持多种数据库**
- **强大的关系映射**
- **连接池管理**

### 1.3 Flask-SQLAlchemy

Flask-SQLAlchemy是SQLAlchemy的Flask扩展，提供：
- 简化的配置
- Flask应用上下文集成
- 便利的查询方法
- 分页支持

## 2. Flask-SQLAlchemy配置

### 2.1 基础配置

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

# 初始化数据库
db = SQLAlchemy(app)
```

### 2.2 数据库URI格式

```python
# SQLite（开发用）
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'

# MySQL
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/dbname'

# PostgreSQL
SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/dbname'

# SQL Server
SQLALCHEMY_DATABASE_URI = 'mssql://username:password@server/database'
```

### 2.3 高级配置

```python
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

app.config.from_object(Config)
```

## 3. 数据模型设计

### 3.1 基础模型定义

```python
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """用户模型"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<User {self.username}>'
```

### 3.2 字段类型

```python
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # 字符串类型
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # 数值类型
    view_count = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    
    # 布尔类型
    is_published = db.Column(db.Boolean, default=False)
    
    # 日期时间类型
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # JSON类型（PostgreSQL和MySQL 5.7+）
    metadata = db.Column(db.JSON)
```

### 3.3 字段约束

```python
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # 唯一约束
    sku = db.Column(db.String(50), unique=True, nullable=False)
    
    # 非空约束
    name = db.Column(db.String(100), nullable=False)
    
    # 默认值
    status = db.Column(db.String(20), default='active')
    
    # 检查约束
    price = db.Column(db.Numeric(10, 2), db.CheckConstraint('price > 0'))
    
    # 外键约束
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
```

### 3.4 模型方法

```python
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def create_user(cls, username, email, password):
        """创建新用户"""
        user = cls(username=username, email=email)
        user.set_password(password)
        return user
```

## 4. 数据库操作基础

### 4.1 创建和删除表

```python
# 创建所有表
with app.app_context():
    db.create_all()

# 删除所有表
with app.app_context():
    db.drop_all()

# 重新创建表
with app.app_context():
    db.drop_all()
    db.create_all()
```

### 4.2 增加数据

```python
# 创建单个记录
user = User(username='john', email='john@example.com')
user.set_password('password123')

# 添加到会话
db.session.add(user)

# 提交事务
db.session.commit()

# 批量添加
users = [
    User(username='alice', email='alice@example.com'),
    User(username='bob', email='bob@example.com')
]
db.session.add_all(users)
db.session.commit()
```

### 4.3 查询数据

```python
# 查询所有用户
users = User.query.all()

# 根据主键查询
user = User.query.get(1)
user = User.query.get_or_404(1)  # 不存在时返回404

# 条件查询
user = User.query.filter_by(username='john').first()
user = User.query.filter(User.username == 'john').first()

# 复合查询
users = User.query.filter(
    User.username.like('%john%'),
    User.is_active == True
).all()

# 排序
users = User.query.order_by(User.created_at.desc()).all()

# 限制结果
users = User.query.limit(10).all()
users = User.query.offset(10).limit(10).all()

# 计数
count = User.query.count()
count = User.query.filter_by(is_active=True).count()
```

### 4.4 更新数据

```python
# 更新单个对象
user = User.query.get(1)
user.email = 'newemail@example.com'
db.session.commit()

# 批量更新
User.query.filter_by(is_active=False).update({'is_active': True})
db.session.commit()
```

### 4.5 删除数据

```python
# 删除单个对象
user = User.query.get(1)
db.session.delete(user)
db.session.commit()

# 批量删除
User.query.filter_by(is_active=False).delete()
db.session.commit()
```

## 5. 数据库关系

### 5.1 一对多关系

```python
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    
    # 反向引用
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    # 外键
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

# 使用关系
category = Category(name='Electronics')
product = Product(name='iPhone', category=category)

# 或者
product = Product(name='iPhone', category_id=1)

# 查询
category = Category.query.get(1)
products = category.products  # 获取分类下的所有产品
```

### 5.2 多对多关系

```python
# 关联表
user_role = db.Table('user_role',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    
    # 多对多关系
    roles = db.relationship('Role', secondary=user_role, 
                          backref=db.backref('users', lazy=True))

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

# 使用关系
user = User(username='john')
admin_role = Role(name='admin')
user_role = Role(name='user')

user.roles.append(admin_role)
user.roles.append(user_role)
```

### 5.3 一对一关系

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    
    # 一对一关系
    profile = db.relationship('UserProfile', backref='user', uselist=False)

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(200))
    
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
```

## 6. 数据库迁移

### 6.1 Flask-Migrate配置

```python
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
```

### 6.2 初始化迁移

```bash
# 初始化迁移环境
flask db init

# 创建第一个迁移
flask db migrate -m "Initial migration"

# 应用迁移
flask db upgrade
```

### 6.3 迁移工作流

```bash
# 1. 修改模型
# 2. 生成迁移文件
flask db migrate -m "Add user table"

# 3. 检查迁移文件
# 4. 应用迁移
flask db upgrade

# 回滚迁移
flask db downgrade

# 查看迁移历史
flask db history

# 查看当前版本
flask db current
```

### 6.4 手动编辑迁移

```python
"""Add user table

Revision ID: 123abc
Revises: 
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '123abc'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
```

## 7. 用户认证系统实战

### 7.1 用户模型设计

```python
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """用户模型"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """获取全名"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)
    
    def __repr__(self):
        return f'<User {self.username}>'
```

### 7.2 注册功能

```python
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[
        DataRequired(), 
        Length(min=3, max=20)
    ])
    email = StringField('邮箱', validators=[
        DataRequired(), 
        Email()
    ])
    password = PasswordField('密码', validators=[
        DataRequired(), 
        Length(min=6)
    ])
    password2 = PasswordField('确认密码', validators=[
        DataRequired(), 
        EqualTo('password', message='密码不匹配')
    ])
    submit = SubmitField('注册')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # 检查用户名是否已存在
        if User.query.filter_by(username=form.username.data).first():
            flash('用户名已存在')
            return render_template('register.html', form=form)
        
        # 检查邮箱是否已存在
        if User.query.filter_by(email=form.email.data).first():
            flash('邮箱已被注册')
            return render_template('register.html', form=form)
        
        # 创建新用户
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('注册成功！请登录。')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)
```

### 7.3 登录功能

```python
from flask_login import LoginManager, login_user, logout_user, login_required

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('账户已被禁用')
                return render_template('login.html', form=form)
            
            # 更新最后登录时间
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            login_user(user, remember=form.remember_me.data)
            flash('登录成功！')
            
            # 重定向到原来的页面
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('用户名或密码错误')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出登录')
    return redirect(url_for('index'))
```

## 8. 会话管理

### 8.1 Flask-Login集成

```python
from flask_login import LoginManager, UserMixin, current_user

# 配置Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '请先登录访问该页面'
login_manager.login_message_category = 'info'

# 用户模型继承UserMixin
class User(UserMixin, db.Model):
    # ... 模型定义
    pass

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

### 8.2 会话配置

```python
from datetime import timedelta

app.config.update(
    SECRET_KEY='your-secret-key',
    PERMANENT_SESSION_LIFETIME=timedelta(days=7),  # 会话保持7天
    SESSION_COOKIE_SECURE=True,  # HTTPS环境
    SESSION_COOKIE_HTTPONLY=True,  # 防XSS
    SESSION_COOKIE_SAMESITE='Lax',  # CSRF保护
)
```

### 8.3 权限装饰器

```python
from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(f):
    """管理员权限装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin')
@login_required
@admin_required
def admin_panel():
    return render_template('admin.html')
```

## 9. 安全考虑

### 9.1 密码安全

```python
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

class User(db.Model):
    password_hash = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(32))
    
    def set_password(self, password):
        """安全设置密码"""
        # 生成盐值
        self.salt = secrets.token_hex(16)
        # 使用pbkdf2:sha256算法
        self.password_hash = generate_password_hash(
            password + self.salt, 
            method='pbkdf2:sha256:100000'
        )
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(
            self.password_hash, 
            password + self.salt
        )
```

### 9.2 防止SQL注入

```python
# ✅ 正确：使用ORM查询
user = User.query.filter_by(username=username).first()

# ✅ 正确：使用参数化查询
result = db.session.execute(
    "SELECT * FROM users WHERE username = :username",
    {"username": username}
)

# ❌ 错误：直接拼接SQL
query = f"SELECT * FROM users WHERE username = '{username}'"
```

### 9.3 输入验证

```python
from wtforms.validators import ValidationError
import re

class CustomForm(FlaskForm):
    username = StringField('用户名', validators=[
        DataRequired(),
        Length(min=3, max=20),
        Regexp(r'^[a-zA-Z0-9_]+$', message='用户名只能包含字母、数字和下划线')
    ])
    
    def validate_username(self, username):
        """自定义验证器"""
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('用户名已存在')
```

## 10. 性能优化

### 10.1 查询优化

```python
# ✅ 使用索引
class User(db.Model):
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)

# ✅ 预加载关联数据
users = User.query.options(db.joinedload(User.posts)).all()

# ✅ 选择特定字段
usernames = db.session.query(User.username).all()

# ✅ 批量操作
db.session.bulk_insert_mappings(User, user_data_list)
```

### 10.2 连接池配置

```python
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,          # 连接池大小
    'pool_timeout': 20,       # 连接超时时间
    'pool_recycle': 3600,     # 连接回收时间
    'pool_pre_ping': True,    # 连接健康检查
    'max_overflow': 20,       # 最大溢出连接数
}
```

### 10.3 查询调试

```python
# 启用查询日志
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# 或在配置中
app.config['SQLALCHEMY_RECORD_QUERIES'] = True

# 查看慢查询
from flask_sqlalchemy import get_debug_queries

@app.after_request
def after_request(response):
    queries = get_debug_queries()
    for query in queries:
        if query.duration >= 0.5:  # 慢查询阈值
            app.logger.warning(f'Slow query: {query.statement}')
    return response
```

## 11. 总结与最佳实践

### 11.1 模型设计原则

1. **单一职责**：每个模型负责一个实体
2. **命名规范**：使用清晰的类名和字段名
3. **索引优化**：为查询字段添加索引
4. **关系明确**：正确定义表关系
5. **验证完整**：添加必要的约束和验证

### 11.2 安全最佳实践

1. **密码加密**：永远不要存储明文密码
2. **输入验证**：验证所有用户输入
3. **参数化查询**：防止SQL注入
4. **会话安全**：配置安全的会话参数
5. **权限控制**：实现细粒度的权限管理

### 11.3 性能最佳实践

1. **连接池**：合理配置数据库连接池
2. **查询优化**：避免N+1查询问题
3. **索引使用**：为常用查询添加索引
4. **批量操作**：使用批量操作提高效率
5. **缓存策略**：合理使用缓存

### 11.4 开发最佳实践

1. **迁移管理**：使用版本控制管理数据库结构
2. **环境分离**：开发、测试、生产环境分离
3. **备份策略**：定期备份数据库
4. **监控日志**：监控数据库性能和错误
5. **文档维护**：保持数据库文档更新

通过本教程的学习，你已经掌握了Flask数据库集成的核心技能。下一步可以学习更高级的主题，如数据库性能调优、分布式数据库、数据缓存等。 