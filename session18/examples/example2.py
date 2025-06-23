#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
示例2：数据关系示例
演示SQLAlchemy中的各种表关系

学习要点：
1. 一对多关系（One-to-Many）
2. 多对多关系（Many-to-Many）
3. 一对一关系（One-to-One）
4. 关系查询和操作
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 创建Flask应用和数据库实例
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==================== 一对多关系示例 ====================

class Author(db.Model):
    """作者模型 - 一对多关系的'一'方"""
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.Text)
    birth_date = db.Column(db.Date)
    
    # 一对多关系：一个作者可以有多本书
    books = db.relationship('Book', backref='author', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Author {self.name}>'

class Book(db.Model):
    """书籍模型 - 一对多关系的'多'方"""
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    pages = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2))
    published_date = db.Column(db.Date)
    
    # 外键：指向作者
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    
    def __repr__(self):
        return f'<Book {self.title}>'

# ==================== 多对多关系示例 ====================

# 多对多关联表
student_course = db.Table('student_course',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
    db.Column('enrollment_date', db.DateTime, default=datetime.utcnow),
    db.Column('grade', db.String(2))  # 额外字段：成绩
)

class Student(db.Model):
    """学生模型 - 多对多关系的一方"""
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    major = db.Column(db.String(100))
    
    # 多对多关系：学生可以选修多门课程
    courses = db.relationship('Course', secondary=student_course, 
                            backref=db.backref('students', lazy=True))
    
    def __repr__(self):
        return f'<Student {self.name}>'

class Course(db.Model):
    """课程模型 - 多对多关系的另一方"""
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    credits = db.Column(db.Integer, default=3)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Course {self.name}>'

# ==================== 一对一关系示例 ====================

class User(db.Model):
    """用户模型 - 一对一关系的主表"""
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # 一对一关系：一个用户对应一个档案
    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'

class UserProfile(db.Model):
    """用户档案模型 - 一对一关系的从表"""
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    avatar_url = db.Column(db.String(200))
    
    # 外键：指向用户（一对一关系需要unique=True）
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<UserProfile for {self.user.username}>'

# ==================== 复杂关系示例 ====================

class Category(db.Model):
    """分类模型 - 自引用关系"""
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    
    # 自引用关系：父分类
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    parent = db.relationship('Category', remote_side=[id], backref='children')
    
    def __repr__(self):
        return f'<Category {self.name}>'

# ==================== 演示函数 ====================

def demonstrate_one_to_many():
    """演示一对多关系"""
    print("\n=== 一对多关系演示 ===")
    
    # 创建作者
    author1 = Author(name='张三', email='zhangsan@example.com', bio='知名作家')
    author2 = Author(name='李四', email='lisi@example.com', bio='技术专家')
    
    db.session.add_all([author1, author2])
    db.session.commit()
    
    print(f"创建作者: {author1.name}, {author2.name}")
    
    # 创建书籍
    book1 = Book(title='Python编程入门', isbn='978-1234567890', pages=300, price=59.99, author=author1)
    book2 = Book(title='Flask Web开发', isbn='978-1234567891', pages=450, price=79.99, author=author1)
    book3 = Book(title='数据结构与算法', isbn='978-1234567892', pages=600, price=89.99, author=author2)
    
    db.session.add_all([book1, book2, book3])
    db.session.commit()
    
    print(f"创建书籍: {book1.title}, {book2.title}, {book3.title}")
    
    # 关系查询
    print(f"\n{author1.name}的书籍:")
    for book in author1.books:
        print(f"  - {book.title} (ISBN: {book.isbn})")
    
    print(f"\n《{book1.title}》的作者: {book1.author.name}")
    
    # 统计信息
    print(f"\n作者统计:")
    for author in Author.query.all():
        print(f"  {author.name}: {len(author.books)} 本书")

def demonstrate_many_to_many():
    """演示多对多关系"""
    print("\n=== 多对多关系演示 ===")
    
    # 创建学生
    student1 = Student(name='王五', student_id='2023001', email='wangwu@example.com', major='计算机科学')
    student2 = Student(name='赵六', student_id='2023002', email='zhaoliu@example.com', major='软件工程')
    student3 = Student(name='孙七', student_id='2023003', email='sunqi@example.com', major='数据科学')
    
    db.session.add_all([student1, student2, student3])
    
    # 创建课程
    course1 = Course(name='Python编程', code='CS101', credits=3, description='Python编程基础')
    course2 = Course(name='数据库原理', code='CS201', credits=4, description='关系数据库设计与实现')
    course3 = Course(name='Web开发', code='CS301', credits=3, description='前端与后端Web开发')
    
    db.session.add_all([course1, course2, course3])
    db.session.commit()
    
    print(f"创建学生: {student1.name}, {student2.name}, {student3.name}")
    print(f"创建课程: {course1.name}, {course2.name}, {course3.name}")
    
    # 建立多对多关系
    # 学生选课
    student1.courses.extend([course1, course2])  # 王五选择Python和数据库
    student2.courses.extend([course1, course3])  # 赵六选择Python和Web开发
    student3.courses.extend([course1, course2, course3])  # 孙七选择所有课程
    
    db.session.commit()
    
    # 查询关系
    print(f"\n学生选课情况:")
    for student in Student.query.all():
        print(f"  {student.name}: {[course.name for course in student.courses]}")
    
    print(f"\n课程选修情况:")
    for course in Course.query.all():
        print(f"  {course.name}: {[student.name for student in course.students]}")
    
    # 复杂查询：找出选修Python课程的学生
    python_course = Course.query.filter_by(code='CS101').first()
    print(f"\n选修《{python_course.name}》的学生:")
    for student in python_course.students:
        print(f"  - {student.name} ({student.student_id})")

def demonstrate_one_to_one():
    """演示一对一关系"""
    print("\n=== 一对一关系演示 ===")
    
    # 创建用户
    user1 = User(username='alice', email='alice@example.com')
    user2 = User(username='bob', email='bob@example.com')
    
    db.session.add_all([user1, user2])
    db.session.commit()
    
    print(f"创建用户: {user1.username}, {user2.username}")
    
    # 创建用户档案
    profile1 = UserProfile(
        first_name='Alice',
        last_name='Johnson',
        phone='123-456-7890',
        address='123 Main St, City, State',
        user=user1
    )
    
    profile2 = UserProfile(
        first_name='Bob',
        last_name='Smith',
        phone='098-765-4321',
        address='456 Oak Ave, City, State',
        user=user2
    )
    
    db.session.add_all([profile1, profile2])
    db.session.commit()
    
    print(f"创建档案: {profile1.first_name} {profile1.last_name}, {profile2.first_name} {profile2.last_name}")
    
    # 关系查询
    print(f"\n用户档案:")
    for user in User.query.all():
        if user.profile:
            print(f"  {user.username}: {user.profile.first_name} {user.profile.last_name}")
            print(f"    电话: {user.profile.phone}")
            print(f"    地址: {user.profile.address}")

def demonstrate_self_reference():
    """演示自引用关系"""
    print("\n=== 自引用关系演示 ===")
    
    # 创建分类层次结构
    root_category = Category(name='根分类', description='顶级分类')
    db.session.add(root_category)
    db.session.commit()
    
    # 创建子分类
    electronics = Category(name='电子产品', description='各种电子设备', parent=root_category)
    clothing = Category(name='服装', description='男女服装', parent=root_category)
    
    db.session.add_all([electronics, clothing])
    db.session.commit()
    
    # 创建更深层的子分类
    laptops = Category(name='笔记本电脑', description='便携式电脑', parent=electronics)
    phones = Category(name='手机', description='智能手机', parent=electronics)
    mens_clothing = Category(name='男装', description='男性服装', parent=clothing)
    womens_clothing = Category(name='女装', description='女性服装', parent=clothing)
    
    db.session.add_all([laptops, phones, mens_clothing, womens_clothing])
    db.session.commit()
    
    print("创建分类层次结构:")
    
    # 打印分类树
    def print_category_tree(category, level=0):
        indent = "  " * level
        print(f"{indent}- {category.name}")
        for child in category.children:
            print_category_tree(child, level + 1)
    
    print_category_tree(root_category)
    
    # 查询特定分类的父分类和子分类
    electronics_cat = Category.query.filter_by(name='电子产品').first()
    print(f"\n电子产品分类:")
    print(f"  父分类: {electronics_cat.parent.name if electronics_cat.parent else '无'}")
    print(f"  子分类: {[child.name for child in electronics_cat.children]}")

def demonstrate_complex_queries():
    """演示复杂关系查询"""
    print("\n=== 复杂关系查询演示 ===")
    
    # 连接查询
    print("1. 连接查询 - 查找张三写的所有书籍:")
    results = db.session.query(Book, Author).join(Author).filter(Author.name == '张三').all()
    for book, author in results:
        print(f"  《{book.title}》- {author.name}")
    
    # 子查询
    print("\n2. 子查询 - 查找书籍数量超过1本的作者:")
    from sqlalchemy import func
    subquery = db.session.query(Book.author_id, func.count(Book.id).label('book_count')).\
        group_by(Book.author_id).having(func.count(Book.id) > 1).subquery()
    
    prolific_authors = db.session.query(Author).join(subquery, Author.id == subquery.c.author_id).all()
    for author in prolific_authors:
        print(f"  {author.name}: {len(author.books)} 本书")
    
    # 聚合查询
    print("\n3. 聚合查询 - 各专业学生人数:")
    major_stats = db.session.query(Student.major, func.count(Student.id)).\
        group_by(Student.major).all()
    for major, count in major_stats:
        print(f"  {major}: {count} 人")
    
    # 条件查询
    print("\n4. 条件查询 - 选修课程数量超过2门的学生:")
    for student in Student.query.all():
        if len(student.courses) > 2:
            print(f"  {student.name}: {len(student.courses)} 门课程")

def main():
    """主函数"""
    print("=" * 60)
    print("示例2：数据关系演示")
    print("=" * 60)
    
    with app.app_context():
        # 创建表
        db.create_all()
        
        # 清空数据（如果存在）
        for model in [Book, Author, Student, Course, User, UserProfile, Category]:
            if model.query.count() > 0:
                db.session.query(model).delete()
        
        # 清空关联表
        db.session.execute(student_course.delete())
        db.session.commit()
        
        # 运行演示
        demonstrate_one_to_many()
        demonstrate_many_to_many()
        demonstrate_one_to_one()
        demonstrate_self_reference()
        demonstrate_complex_queries()
    
    print("\n" + "=" * 60)
    print("示例2完成！")
    print("学习要点总结：")
    print("1. 一对多关系：使用外键(ForeignKey)和relationship")
    print("2. 多对多关系：使用关联表(Table)和secondary参数")
    print("3. 一对一关系：使用外键加unique约束和uselist=False")
    print("4. 自引用关系：外键指向自己的主键")
    print("5. 关系查询：使用join、filter、聚合函数等")
    print("6. 级联操作：使用cascade参数管理关联数据")
    print("=" * 60)

if __name__ == '__main__':
    main() 