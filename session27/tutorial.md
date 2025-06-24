# Session27: 项目架构设计教程

## 1. 软件架构设计概述

### 1.1 什么是软件架构

软件架构是软件系统的高层结构，它定义了系统的组件、组件之间的关系以及组件与环境的关系。好的架构设计能够：

- 提高代码的可维护性和可扩展性
- 降低系统复杂度
- 提升开发效率
- 保证系统质量

### 1.2 架构设计的重要性

```python
# 不良架构示例：所有功能都在一个文件中
def main():
    # 用户登录
    username = input("用户名: ")
    password = input("密码: ")
    
    # 数据库连接
    import sqlite3
    conn = sqlite3.connect('app.db')
    
    # 验证用户
    cursor = conn.execute("SELECT * FROM users WHERE username=? AND password=?", 
                         (username, password))
    user = cursor.fetchone()
    
    if user:
        # 显示菜单
        while True:
            print("1. 查看图书")
            print("2. 借阅图书")
            choice = input("选择: ")
            
            if choice == "1":
                # 查看图书逻辑
                books = conn.execute("SELECT * FROM books").fetchall()
                for book in books:
                    print(f"{book[0]}: {book[1]}")
            elif choice == "2":
                # 借阅图书逻辑
                book_id = input("图书ID: ")
                conn.execute("INSERT INTO borrows (user_id, book_id) VALUES (?, ?)",
                           (user[0], book_id))
                conn.commit()
    
    conn.close()

if __name__ == "__main__":
    main()
```

上述代码存在的问题：
- 所有功能耦合在一起
- 难以测试和维护
- 无法复用
- 扩展困难

## 2. SOLID设计原则

### 2.1 单一职责原则 (Single Responsibility Principle)

每个类应该只有一个引起它变化的原因。

```python
# 违反单一职责原则
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def save_to_database(self):
        # 数据库操作
        pass
    
    def send_email(self):
        # 邮件发送
        pass
    
    def validate_password(self):
        # 密码验证
        pass

# 遵循单一职责原则
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserRepository:
    def save(self, user):
        # 数据库操作
        pass

class EmailService:
    def send_email(self, user, message):
        # 邮件发送
        pass

class PasswordValidator:
    def validate(self, password):
        # 密码验证
        pass
```

### 2.2 开闭原则 (Open/Closed Principle)

软件实体应该对扩展开放，对修改关闭。

```python
from abc import ABC, abstractmethod

# 抽象基类
class NotificationSender(ABC):
    @abstractmethod
    def send(self, message, recipient):
        pass

# 具体实现
class EmailSender(NotificationSender):
    def send(self, message, recipient):
        print(f"发送邮件给 {recipient}: {message}")

class SMSSender(NotificationSender):
    def send(self, message, recipient):
        print(f"发送短信给 {recipient}: {message}")

# 通知服务
class NotificationService:
    def __init__(self):
        self.senders = []
    
    def add_sender(self, sender: NotificationSender):
        self.senders.append(sender)
    
    def notify(self, message, recipient):
        for sender in self.senders:
            sender.send(message, recipient)

# 使用示例
service = NotificationService()
service.add_sender(EmailSender())
service.add_sender(SMSSender())
service.notify("欢迎注册", "user@example.com")
```

### 2.3 里氏替换原则 (Liskov Substitution Principle)

子类对象应该能够替换父类对象而不影响程序的正确性。

```python
class Shape:
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2

# 可以用任何Shape子类替换
def calculate_total_area(shapes):
    total = 0
    for shape in shapes:
        total += shape.area()  # 不需要知道具体类型
    return total

shapes = [Rectangle(5, 3), Circle(2), Rectangle(4, 6)]
print(f"总面积: {calculate_total_area(shapes)}")
```

### 2.4 接口隔离原则 (Interface Segregation Principle)

客户端不应该依赖它不需要的接口。

```python
from abc import ABC, abstractmethod

# 违反接口隔离原则
class Worker(ABC):
    @abstractmethod
    def work(self):
        pass
    
    @abstractmethod
    def eat(self):
        pass

# 遵循接口隔离原则
class Workable(ABC):
    @abstractmethod
    def work(self):
        pass

class Eatable(ABC):
    @abstractmethod
    def eat(self):
        pass

class Human(Workable, Eatable):
    def work(self):
        print("人类在工作")
    
    def eat(self):
        print("人类在吃饭")

class Robot(Workable):
    def work(self):
        print("机器人在工作")
```

### 2.5 依赖倒置原则 (Dependency Inversion Principle)

高层模块不应该依赖低层模块，两者都应该依赖抽象。

```python
from abc import ABC, abstractmethod

# 抽象接口
class DatabaseInterface(ABC):
    @abstractmethod
    def save(self, data):
        pass
    
    @abstractmethod
    def find(self, id):
        pass

# 具体实现
class MySQLDatabase(DatabaseInterface):
    def save(self, data):
        print(f"保存到MySQL: {data}")
    
    def find(self, id):
        print(f"从MySQL查找: {id}")
        return {"id": id, "name": "示例数据"}

class MongoDatabase(DatabaseInterface):
    def save(self, data):
        print(f"保存到MongoDB: {data}")
    
    def find(self, id):
        print(f"从MongoDB查找: {id}")
        return {"id": id, "name": "示例数据"}

# 高层模块依赖抽象
class UserService:
    def __init__(self, database: DatabaseInterface):
        self.database = database
    
    def create_user(self, user_data):
        self.database.save(user_data)
    
    def get_user(self, user_id):
        return self.database.find(user_id)

# 使用示例
mysql_db = MySQLDatabase()
mongo_db = MongoDatabase()

user_service1 = UserService(mysql_db)
user_service2 = UserService(mongo_db)

user_service1.create_user({"name": "张三"})
user_service2.create_user({"name": "李四"})
```

## 3. 分层架构模式

### 3.1 三层架构

经典的三层架构包括：
- **表示层 (Presentation Layer)**：用户界面
- **业务逻辑层 (Business Logic Layer)**：业务规则和逻辑
- **数据访问层 (Data Access Layer)**：数据存储和访问

```python
# 数据访问层
class BookRepository:
    def __init__(self):
        self.books = [
            {"id": 1, "title": "Python编程", "author": "张三", "available": True},
            {"id": 2, "title": "数据结构", "author": "李四", "available": True},
        ]
    
    def find_all(self):
        return self.books
    
    def find_by_id(self, book_id):
        return next((book for book in self.books if book["id"] == book_id), None)
    
    def update(self, book):
        for i, b in enumerate(self.books):
            if b["id"] == book["id"]:
                self.books[i] = book
                return True
        return False

# 业务逻辑层
class BookService:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository
    
    def get_available_books(self):
        all_books = self.book_repository.find_all()
        return [book for book in all_books if book["available"]]
    
    def borrow_book(self, book_id, user_id):
        book = self.book_repository.find_by_id(book_id)
        if not book:
            return {"success": False, "message": "图书不存在"}
        
        if not book["available"]:
            return {"success": False, "message": "图书已被借出"}
        
        book["available"] = False
        book["borrowed_by"] = user_id
        self.book_repository.update(book)
        
        return {"success": True, "message": "借阅成功"}
    
    def return_book(self, book_id):
        book = self.book_repository.find_by_id(book_id)
        if not book:
            return {"success": False, "message": "图书不存在"}
        
        if book["available"]:
            return {"success": False, "message": "图书未被借出"}
        
        book["available"] = True
        if "borrowed_by" in book:
            del book["borrowed_by"]
        self.book_repository.update(book)
        
        return {"success": True, "message": "归还成功"}

# 表示层
class BookController:
    def __init__(self, book_service: BookService):
        self.book_service = book_service
    
    def list_books(self):
        books = self.book_service.get_available_books()
        print("可借阅图书：")
        for book in books:
            print(f"{book['id']}. {book['title']} - {book['author']}")
    
    def borrow_book_action(self, book_id, user_id):
        result = self.book_service.borrow_book(book_id, user_id)
        print(result["message"])
        return result["success"]
    
    def return_book_action(self, book_id):
        result = self.book_service.return_book(book_id)
        print(result["message"])
        return result["success"]

# 使用示例
book_repo = BookRepository()
book_service = BookService(book_repo)
book_controller = BookController(book_service)

book_controller.list_books()
book_controller.borrow_book_action(1, "user123")
book_controller.list_books()
book_controller.return_book_action(1)
```

**运行结果：**
```
可借阅图书：
1. Python编程 - 张三
2. 数据结构 - 李四
借阅成功
可借阅图书：
2. 数据结构 - 李四
归还成功
```

### 3.2 四层架构

在三层架构基础上增加：
- **领域层 (Domain Layer)**：核心业务实体和规则

```python
# 领域层 - 实体
class Book:
    def __init__(self, id, title, author, isbn):
        self.id = id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = True
        self.borrowed_by = None
        self.borrowed_date = None
    
    def borrow(self, user_id):
        if not self.is_available:
            raise ValueError("图书已被借出")
        
        self.is_available = False
        self.borrowed_by = user_id
        from datetime import datetime
        self.borrowed_date = datetime.now()
    
    def return_book(self):
        if self.is_available:
            raise ValueError("图书未被借出")
        
        self.is_available = True
        self.borrowed_by = None
        self.borrowed_date = None
    
    def is_overdue(self, days_limit=30):
        if self.is_available or not self.borrowed_date:
            return False
        
        from datetime import datetime, timedelta
        return datetime.now() > self.borrowed_date + timedelta(days=days_limit)

class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
        self.borrowed_books = []
    
    def can_borrow(self, max_books=5):
        return len(self.borrowed_books) < max_books

# 领域服务
class LibraryDomainService:
    @staticmethod
    def calculate_fine(book: Book, fine_per_day=1.0):
        if not book.is_overdue():
            return 0.0
        
        from datetime import datetime
        overdue_days = (datetime.now() - book.borrowed_date).days - 30
        return max(0, overdue_days * fine_per_day)
```

## 4. MVC架构模式

### 4.1 MVC模式概述

MVC（Model-View-Controller）是一种将应用程序分为三个核心组件的架构模式：

- **Model（模型）**：数据和业务逻辑
- **View（视图）**：用户界面
- **Controller（控制器）**：处理用户输入，协调Model和View

```python
# Model - 数据模型
class StudentModel:
    def __init__(self):
        self.students = [
            {"id": 1, "name": "张三", "age": 20, "grade": "A"},
            {"id": 2, "name": "李四", "age": 21, "grade": "B"},
            {"id": 3, "name": "王五", "age": 19, "grade": "A"},
        ]
    
    def get_all_students(self):
        return self.students
    
    def get_student_by_id(self, student_id):
        return next((s for s in self.students if s["id"] == student_id), None)
    
    def add_student(self, student):
        new_id = max([s["id"] for s in self.students]) + 1
        student["id"] = new_id
        self.students.append(student)
        return student
    
    def update_student(self, student_id, updated_data):
        student = self.get_student_by_id(student_id)
        if student:
            student.update(updated_data)
            return student
        return None
    
    def delete_student(self, student_id):
        self.students = [s for s in self.students if s["id"] != student_id]

# View - 视图
class StudentView:
    def display_students(self, students):
        print("\n=== 学生列表 ===")
        print(f"{'ID':<5} {'姓名':<10} {'年龄':<5} {'成绩':<5}")
        print("-" * 30)
        for student in students:
            print(f"{student['id']:<5} {student['name']:<10} {student['age']:<5} {student['grade']:<5}")
    
    def display_student(self, student):
        if student:
            print(f"\n学生信息：")
            print(f"ID: {student['id']}")
            print(f"姓名: {student['name']}")
            print(f"年龄: {student['age']}")
            print(f"成绩: {student['grade']}")
        else:
            print("学生不存在")
    
    def display_message(self, message):
        print(f"\n{message}")
    
    def get_student_input(self):
        print("\n请输入学生信息：")
        name = input("姓名: ")
        age = int(input("年龄: "))
        grade = input("成绩: ")
        return {"name": name, "age": age, "grade": grade}
    
    def show_menu(self):
        print("\n=== 学生管理系统 ===")
        print("1. 查看所有学生")
        print("2. 查看单个学生")
        print("3. 添加学生")
        print("4. 更新学生")
        print("5. 删除学生")
        print("0. 退出")
        return input("请选择操作: ")

# Controller - 控制器
class StudentController:
    def __init__(self, model: StudentModel, view: StudentView):
        self.model = model
        self.view = view
    
    def show_all_students(self):
        students = self.model.get_all_students()
        self.view.display_students(students)
    
    def show_student(self, student_id):
        student = self.model.get_student_by_id(student_id)
        self.view.display_student(student)
    
    def add_student(self):
        student_data = self.view.get_student_input()
        new_student = self.model.add_student(student_data)
        self.view.display_message(f"学生 {new_student['name']} 添加成功")
    
    def update_student(self, student_id):
        existing_student = self.model.get_student_by_id(student_id)
        if not existing_student:
            self.view.display_message("学生不存在")
            return
        
        self.view.display_student(existing_student)
        updated_data = self.view.get_student_input()
        updated_student = self.model.update_student(student_id, updated_data)
        self.view.display_message(f"学生信息更新成功")
    
    def delete_student(self, student_id):
        student = self.model.get_student_by_id(student_id)
        if student:
            self.model.delete_student(student_id)
            self.view.display_message(f"学生 {student['name']} 删除成功")
        else:
            self.view.display_message("学生不存在")
    
    def run(self):
        while True:
            choice = self.view.show_menu()
            
            if choice == "1":
                self.show_all_students()
            elif choice == "2":
                student_id = int(input("请输入学生ID: "))
                self.show_student(student_id)
            elif choice == "3":
                self.add_student()
            elif choice == "4":
                student_id = int(input("请输入要更新的学生ID: "))
                self.update_student(student_id)
            elif choice == "5":
                student_id = int(input("请输入要删除的学生ID: "))
                self.delete_student(student_id)
            elif choice == "0":
                self.view.display_message("谢谢使用！")
                break
            else:
                self.view.display_message("无效选择，请重试")

# 使用示例
if __name__ == "__main__":
    model = StudentModel()
    view = StudentView()
    controller = StudentController(model, view)
    
    # 演示功能
    controller.show_all_students()
    controller.add_student()  # 需要用户输入
```

## 5. 模块化设计

### 5.1 模块划分原则

1. **高内聚**：模块内部元素紧密相关
2. **低耦合**：模块之间依赖关系最小
3. **单一职责**：每个模块只负责一个功能领域
4. **接口清晰**：模块间通过明确的接口通信

### 5.2 项目模块结构示例

```
library_system/
├── __init__.py
├── config/
│   ├── __init__.py
│   ├── settings.py
│   └── database.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── book.py
│   └── borrow.py
├── repositories/
│   ├── __init__.py
│   ├── base.py
│   ├── user_repository.py
│   └── book_repository.py
├── services/
│   ├── __init__.py
│   ├── user_service.py
│   ├── book_service.py
│   └── notification_service.py
├── controllers/
│   ├── __init__.py
│   ├── user_controller.py
│   └── book_controller.py
├── views/
│   ├── __init__.py
│   ├── templates/
│   └── static/
├── utils/
│   ├── __init__.py
│   ├── validators.py
│   └── helpers.py
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_services.py
    └── test_controllers.py
```

### 5.3 依赖注入

```python
# 依赖注入容器
class DIContainer:
    def __init__(self):
        self._services = {}
        self._singletons = {}
    
    def register(self, interface, implementation, singleton=False):
        self._services[interface] = {
            'implementation': implementation,
            'singleton': singleton
        }
    
    def resolve(self, interface):
        if interface not in self._services:
            raise ValueError(f"Service {interface} not registered")
        
        service_info = self._services[interface]
        implementation = service_info['implementation']
        
        if service_info['singleton']:
            if interface not in self._singletons:
                self._singletons[interface] = implementation()
            return self._singletons[interface]
        
        return implementation()

# 使用示例
container = DIContainer()
container.register('database', MySQLDatabase, singleton=True)
container.register('user_service', lambda: UserService(container.resolve('database')))

user_service = container.resolve('user_service')
```

## 6. 数据库设计

### 6.1 实体关系设计

```python
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

# 用户表
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # 关系
    borrows = relationship("Borrow", back_populates="user")

# 图书表
class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    isbn = Column(String(20), unique=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    category = relationship("Category", back_populates="books")
    borrows = relationship("Borrow", back_populates="book")

# 分类表
class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(200))
    
    # 关系
    books = relationship("Book", back_populates="category")

# 借阅记录表
class Borrow(Base):
    __tablename__ = 'borrows'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    borrow_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime)
    is_returned = Column(Boolean, default=False)
    
    # 关系
    user = relationship("User", back_populates="borrows")
    book = relationship("Book", back_populates="borrows")

# 数据库配置
class DatabaseConfig:
    def __init__(self, database_url="sqlite:///library.db"):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        return self.SessionLocal()
```

### 6.2 Repository模式

```python
from abc import ABC, abstractmethod
from typing import List, Optional

# 基础Repository接口
class BaseRepository(ABC):
    @abstractmethod
    def create(self, entity):
        pass
    
    @abstractmethod
    def get_by_id(self, id: int):
        pass
    
    @abstractmethod
    def get_all(self) -> List:
        pass
    
    @abstractmethod
    def update(self, entity):
        pass
    
    @abstractmethod
    def delete(self, id: int):
        pass

# 用户Repository实现
class UserRepository(BaseRepository):
    def __init__(self, db_session):
        self.db = db_session
    
    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()
    
    def get_all(self) -> List[User]:
        return self.db.query(User).all()
    
    def update(self, user: User) -> User:
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False

# 图书Repository实现
class BookRepository(BaseRepository):
    def __init__(self, db_session):
        self.db = db_session
    
    def create(self, book: Book) -> Book:
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book
    
    def get_by_id(self, book_id: int) -> Optional[Book]:
        return self.db.query(Book).filter(Book.id == book_id).first()
    
    def get_available_books(self) -> List[Book]:
        return self.db.query(Book).filter(Book.is_available == True).all()
    
    def get_by_category(self, category_id: int) -> List[Book]:
        return self.db.query(Book).filter(Book.category_id == category_id).all()
    
    def search_by_title(self, title: str) -> List[Book]:
        return self.db.query(Book).filter(Book.title.contains(title)).all()
    
    def get_all(self) -> List[Book]:
        return self.db.query(Book).all()
    
    def update(self, book: Book) -> Book:
        self.db.commit()
        self.db.refresh(book)
        return book
    
    def delete(self, book_id: int) -> bool:
        book = self.get_by_id(book_id)
        if book:
            self.db.delete(book)
            self.db.commit()
            return True
        return False
```

## 7. API设计规范

### 7.1 RESTful API设计

```python
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from marshmallow import Schema, fields, ValidationError

app = Flask(__name__)
api = Api(app)

# 数据验证Schema
class UserSchema(Schema):
    username = fields.Str(required=True, validate=lambda x: len(x) >= 3)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=lambda x: len(x) >= 6)

class BookSchema(Schema):
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    isbn = fields.Str(required=True)
    category_id = fields.Int(required=True)

# API资源类
class UserListAPI(Resource):
    def get(self):
        """获取用户列表"""
        try:
            users = user_service.get_all_users()
            return {
                'status': 'success',
                'data': [{
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'created_at': user.created_at.isoformat()
                } for user in users]
            }, 200
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500
    
    def post(self):
        """创建新用户"""
        try:
            schema = UserSchema()
            data = schema.load(request.json)
            
            user = user_service.create_user(data)
            return {
                'status': 'success',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                },
                'message': '用户创建成功'
            }, 201
        except ValidationError as e:
            return {'status': 'error', 'errors': e.messages}, 400
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500

class UserAPI(Resource):
    def get(self, user_id):
        """获取单个用户"""
        try:
            user = user_service.get_user_by_id(user_id)
            if not user:
                return {'status': 'error', 'message': '用户不存在'}, 404
            
            return {
                'status': 'success',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'created_at': user.created_at.isoformat()
                }
            }, 200
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500
    
    def put(self, user_id):
        """更新用户"""
        try:
            user = user_service.get_user_by_id(user_id)
            if not user:
                return {'status': 'error', 'message': '用户不存在'}, 404
            
            schema = UserSchema(partial=True)
            data = schema.load(request.json)
            
            updated_user = user_service.update_user(user_id, data)
            return {
                'status': 'success',
                'data': {
                    'id': updated_user.id,
                    'username': updated_user.username,
                    'email': updated_user.email
                },
                'message': '用户更新成功'
            }, 200
        except ValidationError as e:
            return {'status': 'error', 'errors': e.messages}, 400
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500
    
    def delete(self, user_id):
        """删除用户"""
        try:
            success = user_service.delete_user(user_id)
            if not success:
                return {'status': 'error', 'message': '用户不存在'}, 404
            
            return {
                'status': 'success',
                'message': '用户删除成功'
            }, 200
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500

# 注册API路由
api.add_resource(UserListAPI, '/api/users')
api.add_resource(UserAPI, '/api/users/<int:user_id>')

# 错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': '资源不存在'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': '服务器内部错误'
    }), 500
```

### 7.2 API文档规范

```python
# API文档示例
API_DOCS = {
    "openapi": "3.0.0",
    "info": {
        "title": "图书管理系统API",
        "version": "1.0.0",
        "description": "图书管理系统的RESTful API"
    },
    "paths": {
        "/api/users": {
            "get": {
                "summary": "获取用户列表",
                "responses": {
                    "200": {
                        "description": "成功",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string"},
                                        "data": {
                                            "type": "array",
                                            "items": {"$ref": "#/components/schemas/User"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "summary": "创建新用户",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/UserCreate"}
                        }
                    }
                },
                "responses": {
                    "201": {"description": "创建成功"},
                    "400": {"description": "请求参数错误"}
                }
            }
        }
    },
    "components": {
        "schemas": {
            "User": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "username": {"type": "string"},
                    "email": {"type": "string"},
                    "created_at": {"type": "string", "format": "date-time"}
                }
            },
            "UserCreate": {
                "type": "object",
                "required": ["username", "email", "password"],
                "properties": {
                    "username": {"type": "string", "minLength": 3},
                    "email": {"type": "string", "format": "email"},
                    "password": {"type": "string", "minLength": 6}
                }
            }
        }
    }
}
```

## 8. 性能与扩展性考虑

### 8.1 缓存策略

```python
import redis
from functools import wraps
import json
import pickle

class CacheService:
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    
    def get(self, key):
        try:
            data = self.redis_client.get(key)
            return json.loads(data) if data else None
        except:
            return None
    
    def set(self, key, value, expire=3600):
        try:
            self.redis_client.setex(key, expire, json.dumps(value))
            return True
        except:
            return False
    
    def delete(self, key):
        return self.redis_client.delete(key)

# 缓存装饰器
def cache_result(expire=3600, key_prefix=""):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # 尝试从缓存获取
            cached_result = cache_service.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # 执行函数并缓存结果
            result = func(*args, **kwargs)
            cache_service.set(cache_key, result, expire)
            return result
        return wrapper
    return decorator

# 使用缓存的服务
class BookService:
    def __init__(self, book_repository, cache_service):
        self.book_repository = book_repository
        self.cache_service = cache_service
    
    @cache_result(expire=1800, key_prefix="books")
    def get_popular_books(self, limit=10):
        """获取热门图书（缓存30分钟）"""
        return self.book_repository.get_popular_books(limit)
    
    @cache_result(expire=3600, key_prefix="categories")
    def get_categories(self):
        """获取分类列表（缓存1小时）"""
        return self.book_repository.get_all_categories()
    
    def update_book(self, book_id, data):
        """更新图书时清除相关缓存"""
        result = self.book_repository.update(book_id, data)
        
        # 清除相关缓存
        self.cache_service.delete(f"books:get_popular_books:*")
        self.cache_service.delete(f"book:{book_id}")
        
        return result
```

### 8.2 数据库优化

```python
# 数据库连接池
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

class DatabaseManager:
    def __init__(self, database_url):
        self.engine = create_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=20,          # 连接池大小
            max_overflow=30,       # 最大溢出连接数
            pool_pre_ping=True,    # 连接前检查
            pool_recycle=3600      # 连接回收时间
        )
    
    def get_connection(self):
        return self.engine.connect()

# 查询优化
class OptimizedBookRepository:
    def __init__(self, db_session):
        self.db = db_session
    
    def get_books_with_pagination(self, page=1, per_page=20, category_id=None):
        """分页查询图书"""
        query = self.db.query(Book)
        
        if category_id:
            query = query.filter(Book.category_id == category_id)
        
        # 添加索引提示
        query = query.order_by(Book.created_at.desc())
        
        # 分页
        offset = (page - 1) * per_page
        books = query.offset(offset).limit(per_page).all()
        
        # 获取总数（优化：使用count查询）
        total = query.count()
        
        return {
            'books': books,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }
    
    def search_books_optimized(self, keyword, page=1, per_page=20):
        """优化的图书搜索"""
        # 使用全文搜索（如果数据库支持）
        query = self.db.query(Book).filter(
            Book.title.contains(keyword) | 
            Book.author.contains(keyword)
        )
        
        # 添加相关性排序
        query = query.order_by(
            Book.title.contains(keyword).desc(),
            Book.author.contains(keyword).desc(),
            Book.created_at.desc()
        )
        
        offset = (page - 1) * per_page
        return query.offset(offset).limit(per_page).all()
```

### 8.3 异步处理

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
from celery import Celery

# Celery异步任务
celery_app = Celery('library_system')

@celery_app.task
def send_notification_email(user_email, subject, content):
    """异步发送邮件通知"""
    try:
        # 邮件发送逻辑
        email_service = EmailService()
        email_service.send(user_email, subject, content)
        return f"邮件发送成功: {user_email}"
    except Exception as e:
        return f"邮件发送失败: {str(e)}"

@celery_app.task
def generate_report(report_type, start_date, end_date):
    """异步生成报告"""
    try:
        report_service = ReportService()
        report_data = report_service.generate(report_type, start_date, end_date)
        
        # 保存报告文件
        filename = f"report_{report_type}_{start_date}_{end_date}.pdf"
        report_service.save_to_file(report_data, filename)
        
        return f"报告生成成功: {filename}"
    except Exception as e:
        return f"报告生成失败: {str(e)}"

# 异步服务类
class AsyncLibraryService:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=10)
    
    async def borrow_book_async(self, user_id, book_id):
        """异步借阅图书"""
        loop = asyncio.get_event_loop()
        
        # 在线程池中执行数据库操作
        result = await loop.run_in_executor(
            self.executor,
            self._borrow_book_sync,
            user_id,
            book_id
        )
        
        if result['success']:
            # 异步发送通知邮件
            send_notification_email.delay(
                result['user_email'],
                "借阅成功通知",
                f"您已成功借阅图书：{result['book_title']}"
            )
        
        return result
    
    def _borrow_book_sync(self, user_id, book_id):
        """同步借阅图书逻辑"""
        # 实际的借阅逻辑
        pass
```

## 9. 总结

### 9.1 架构设计最佳实践

1. **遵循SOLID原则**：确保代码的可维护性和可扩展性
2. **分层架构**：清晰的职责分离
3. **模块化设计**：高内聚、低耦合
4. **依赖注入**：提高代码的可测试性
5. **接口设计**：定义清晰的契约
6. **错误处理**：统一的异常处理机制
7. **性能优化**：缓存、分页、索引等
8. **安全考虑**：输入验证、权限控制等

### 9.2 常见架构模式对比

| 模式 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| 分层架构 | 结构清晰、易于理解 | 可能过度设计 | 中小型应用 |
| MVC | 职责分离、可维护性好 | 控制器可能过重 | Web应用 |
| 微服务 | 可扩展性强、技术多样性 | 复杂度高、运维成本大 | 大型分布式系统 |
| 事件驱动 | 松耦合、可扩展 | 调试困难、一致性问题 | 实时系统 |

### 9.3 架构演进策略

1. **从简单开始**：避免过度设计
2. **渐进式重构**：逐步优化架构
3. **监控和度量**：基于数据做决策
4. **文档化**：保持架构文档更新
5. **团队协作**：确保团队理解架构决策

通过本课程的学习，你应该能够：
- 理解软件架构的重要性
- 掌握常见的架构模式和设计原则
- 能够为项目设计合理的架构
- 具备架构演进和优化的能力

记住，好的架构不是一蹴而就的，需要在实践中不断学习和改进！