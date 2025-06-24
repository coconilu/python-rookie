#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session27: 项目架构设计 - 演示代码

本文件演示了软件架构设计的核心概念和实际应用，包括：
1. SOLID设计原则的实际应用
2. 分层架构模式的实现
3. 依赖注入容器的使用
4. 模块化设计的实践

作者: Python教程团队
创建日期: 2024-01-27
最后修改: 2024-01-27
"""

import sys
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import json


def main():
    """
    主函数：演示项目架构设计的核心概念
    """
    print("Session27: 项目架构设计演示")
    print("=" * 50)
    
    # 演示1: SOLID原则应用
    print("\n1. SOLID设计原则演示")
    print("-" * 30)
    demo_solid_principles()
    
    # 演示2: 分层架构
    print("\n2. 分层架构模式演示")
    print("-" * 30)
    demo_layered_architecture()
    
    # 演示3: 依赖注入
    print("\n3. 依赖注入容器演示")
    print("-" * 30)
    demo_dependency_injection()
    
    # 演示4: 架构模式对比
    print("\n4. 架构模式对比演示")
    print("-" * 30)
    demo_architecture_patterns()
    
    print("\n演示完成！")


# ============================================================================
# 1. SOLID设计原则演示
# ============================================================================

# 单一职责原则 (SRP)
class User:
    """用户实体 - 只负责用户数据"""
    def __init__(self, id: int, username: str, email: str):
        self.id = id
        self.username = username
        self.email = email
        self.created_at = datetime.now()

class UserValidator:
    """用户验证器 - 只负责验证逻辑"""
    @staticmethod
    def validate_email(email: str) -> bool:
        return "@" in email and "." in email
    
    @staticmethod
    def validate_username(username: str) -> bool:
        return len(username) >= 3 and username.isalnum()

class UserRepository:
    """用户仓储 - 只负责数据访问"""
    def __init__(self):
        self.users: List[User] = []
        self.next_id = 1
    
    def save(self, user: User) -> User:
        if user.id == 0:
            user.id = self.next_id
            self.next_id += 1
        self.users.append(user)
        return user
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        return next((u for u in self.users if u.id == user_id), None)
    
    def find_all(self) -> List[User]:
        return self.users.copy()

# 开闭原则 (OCP)
class NotificationSender(ABC):
    """通知发送器抽象基类"""
    @abstractmethod
    def send(self, recipient: str, message: str) -> bool:
        pass

class EmailSender(NotificationSender):
    """邮件发送器"""
    def send(self, recipient: str, message: str) -> bool:
        print(f"📧 发送邮件给 {recipient}: {message}")
        return True

class SMSSender(NotificationSender):
    """短信发送器"""
    def send(self, recipient: str, message: str) -> bool:
        print(f"📱 发送短信给 {recipient}: {message}")
        return True

class PushNotificationSender(NotificationSender):
    """推送通知发送器"""
    def send(self, recipient: str, message: str) -> bool:
        print(f"🔔 发送推送通知给 {recipient}: {message}")
        return True

class NotificationService:
    """通知服务 - 对扩展开放，对修改关闭"""
    def __init__(self):
        self.senders: List[NotificationSender] = []
    
    def add_sender(self, sender: NotificationSender):
        self.senders.append(sender)
    
    def notify_all(self, recipient: str, message: str):
        for sender in self.senders:
            sender.send(recipient, message)

# 里氏替换原则 (LSP)
class Shape(ABC):
    """形状抽象基类"""
    @abstractmethod
    def area(self) -> float:
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        pass

class Rectangle(Shape):
    """矩形"""
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

class Circle(Shape):
    """圆形"""
    def __init__(self, radius: float):
        self.radius = radius
    
    def area(self) -> float:
        return 3.14159 * self.radius ** 2
    
    def perimeter(self) -> float:
        return 2 * 3.14159 * self.radius

class GeometryCalculator:
    """几何计算器 - 可以处理任何Shape子类"""
    @staticmethod
    def calculate_total_area(shapes: List[Shape]) -> float:
        return sum(shape.area() for shape in shapes)
    
    @staticmethod
    def calculate_total_perimeter(shapes: List[Shape]) -> float:
        return sum(shape.perimeter() for shape in shapes)

# 接口隔离原则 (ISP)
class Readable(ABC):
    """可读接口"""
    @abstractmethod
    def read(self) -> str:
        pass

class Writable(ABC):
    """可写接口"""
    @abstractmethod
    def write(self, data: str) -> bool:
        pass

class Executable(ABC):
    """可执行接口"""
    @abstractmethod
    def execute(self) -> Any:
        pass

class TextFile(Readable, Writable):
    """文本文件 - 实现读写接口"""
    def __init__(self, filename: str):
        self.filename = filename
        self.content = ""
    
    def read(self) -> str:
        return f"读取文件 {self.filename}: {self.content}"
    
    def write(self, data: str) -> bool:
        self.content = data
        print(f"写入文件 {self.filename}: {data}")
        return True

class Script(Readable, Executable):
    """脚本文件 - 实现读取和执行接口"""
    def __init__(self, script_name: str, code: str):
        self.script_name = script_name
        self.code = code
    
    def read(self) -> str:
        return f"读取脚本 {self.script_name}: {self.code}"
    
    def execute(self) -> Any:
        print(f"执行脚本 {self.script_name}: {self.code}")
        return "执行完成"

# 依赖倒置原则 (DIP)
class DatabaseInterface(ABC):
    """数据库接口"""
    @abstractmethod
    def connect(self) -> bool:
        pass
    
    @abstractmethod
    def execute_query(self, query: str) -> List[Dict]:
        pass
    
    @abstractmethod
    def close(self) -> bool:
        pass

class MySQLDatabase(DatabaseInterface):
    """MySQL数据库实现"""
    def connect(self) -> bool:
        print("连接到MySQL数据库")
        return True
    
    def execute_query(self, query: str) -> List[Dict]:
        print(f"执行MySQL查询: {query}")
        return [{"id": 1, "name": "示例数据"}]
    
    def close(self) -> bool:
        print("关闭MySQL连接")
        return True

class PostgreSQLDatabase(DatabaseInterface):
    """PostgreSQL数据库实现"""
    def connect(self) -> bool:
        print("连接到PostgreSQL数据库")
        return True
    
    def execute_query(self, query: str) -> List[Dict]:
        print(f"执行PostgreSQL查询: {query}")
        return [{"id": 1, "name": "示例数据"}]
    
    def close(self) -> bool:
        print("关闭PostgreSQL连接")
        return True

class DataService:
    """数据服务 - 依赖抽象而非具体实现"""
    def __init__(self, database: DatabaseInterface):
        self.database = database
    
    def get_user_data(self, user_id: int) -> Optional[Dict]:
        self.database.connect()
        try:
            results = self.database.execute_query(f"SELECT * FROM users WHERE id = {user_id}")
            return results[0] if results else None
        finally:
            self.database.close()


def demo_solid_principles():
    """演示SOLID设计原则"""
    print("🔹 单一职责原则 (SRP)")
    user = User(0, "alice", "alice@example.com")
    validator = UserValidator()
    repository = UserRepository()
    
    if validator.validate_email(user.email) and validator.validate_username(user.username):
        saved_user = repository.save(user)
        print(f"用户保存成功: {saved_user.username} (ID: {saved_user.id})")
    
    print("\n🔹 开闭原则 (OCP)")
    notification_service = NotificationService()
    notification_service.add_sender(EmailSender())
    notification_service.add_sender(SMSSender())
    notification_service.add_sender(PushNotificationSender())
    notification_service.notify_all("user@example.com", "欢迎注册！")
    
    print("\n🔹 里氏替换原则 (LSP)")
    shapes = [Rectangle(5, 3), Circle(2), Rectangle(4, 6)]
    calculator = GeometryCalculator()
    total_area = calculator.calculate_total_area(shapes)
    total_perimeter = calculator.calculate_total_perimeter(shapes)
    print(f"总面积: {total_area:.2f}")
    print(f"总周长: {total_perimeter:.2f}")
    
    print("\n🔹 接口隔离原则 (ISP)")
    text_file = TextFile("document.txt")
    text_file.write("Hello, World!")
    print(text_file.read())
    
    script = Script("hello.py", "print('Hello from script!')")
    print(script.read())
    script.execute()
    
    print("\n🔹 依赖倒置原则 (DIP)")
    mysql_service = DataService(MySQLDatabase())
    postgresql_service = DataService(PostgreSQLDatabase())
    
    mysql_service.get_user_data(1)
    postgresql_service.get_user_data(1)


# ============================================================================
# 2. 分层架构演示
# ============================================================================

# 数据访问层 (Data Access Layer)
class BookRepository:
    """图书仓储 - 数据访问层"""
    def __init__(self):
        self.books = [
            {"id": 1, "title": "Python编程", "author": "张三", "available": True, "category": "编程"},
            {"id": 2, "title": "数据结构", "author": "李四", "available": True, "category": "计算机科学"},
            {"id": 3, "title": "算法导论", "author": "王五", "available": False, "category": "计算机科学"},
        ]
        self.next_id = 4
    
    def find_all(self) -> List[Dict]:
        return self.books.copy()
    
    def find_by_id(self, book_id: int) -> Optional[Dict]:
        return next((book for book in self.books if book["id"] == book_id), None)
    
    def find_by_category(self, category: str) -> List[Dict]:
        return [book for book in self.books if book["category"] == category]
    
    def find_available(self) -> List[Dict]:
        return [book for book in self.books if book["available"]]
    
    def update(self, book: Dict) -> bool:
        for i, b in enumerate(self.books):
            if b["id"] == book["id"]:
                self.books[i] = book
                return True
        return False
    
    def create(self, book_data: Dict) -> Dict:
        book = book_data.copy()
        book["id"] = self.next_id
        self.next_id += 1
        self.books.append(book)
        return book

class BorrowRepository:
    """借阅记录仓储"""
    def __init__(self):
        self.borrows = []
        self.next_id = 1
    
    def create_borrow_record(self, user_id: int, book_id: int) -> Dict:
        record = {
            "id": self.next_id,
            "user_id": user_id,
            "book_id": book_id,
            "borrow_date": datetime.now(),
            "due_date": datetime.now() + timedelta(days=30),
            "return_date": None,
            "is_returned": False
        }
        self.next_id += 1
        self.borrows.append(record)
        return record
    
    def find_by_user(self, user_id: int) -> List[Dict]:
        return [b for b in self.borrows if b["user_id"] == user_id]
    
    def find_active_borrows(self) -> List[Dict]:
        return [b for b in self.borrows if not b["is_returned"]]
    
    def return_book(self, borrow_id: int) -> bool:
        for borrow in self.borrows:
            if borrow["id"] == borrow_id:
                borrow["return_date"] = datetime.now()
                borrow["is_returned"] = True
                return True
        return False

# 业务逻辑层 (Business Logic Layer)
class LibraryService:
    """图书馆服务 - 业务逻辑层"""
    def __init__(self, book_repo: BookRepository, borrow_repo: BorrowRepository):
        self.book_repo = book_repo
        self.borrow_repo = borrow_repo
    
    def get_available_books(self) -> List[Dict]:
        """获取可借阅图书"""
        return self.book_repo.find_available()
    
    def search_books_by_category(self, category: str) -> List[Dict]:
        """按分类搜索图书"""
        return self.book_repo.find_by_category(category)
    
    def borrow_book(self, user_id: int, book_id: int) -> Dict:
        """借阅图书"""
        # 业务规则验证
        book = self.book_repo.find_by_id(book_id)
        if not book:
            return {"success": False, "message": "图书不存在"}
        
        if not book["available"]:
            return {"success": False, "message": "图书已被借出"}
        
        # 检查用户当前借阅数量
        user_borrows = self.borrow_repo.find_by_user(user_id)
        active_borrows = [b for b in user_borrows if not b["is_returned"]]
        if len(active_borrows) >= 5:  # 最多借5本
            return {"success": False, "message": "借阅数量已达上限"}
        
        # 执行借阅
        book["available"] = False
        self.book_repo.update(book)
        
        borrow_record = self.borrow_repo.create_borrow_record(user_id, book_id)
        
        return {
            "success": True,
            "message": "借阅成功",
            "borrow_record": borrow_record
        }
    
    def return_book(self, user_id: int, book_id: int) -> Dict:
        """归还图书"""
        # 查找借阅记录
        user_borrows = self.borrow_repo.find_by_user(user_id)
        active_borrow = next(
            (b for b in user_borrows if b["book_id"] == book_id and not b["is_returned"]),
            None
        )
        
        if not active_borrow:
            return {"success": False, "message": "未找到借阅记录"}
        
        # 计算是否逾期
        is_overdue = datetime.now() > active_borrow["due_date"]
        fine = 0
        if is_overdue:
            overdue_days = (datetime.now() - active_borrow["due_date"]).days
            fine = overdue_days * 1.0  # 每天1元罚金
        
        # 执行归还
        self.borrow_repo.return_book(active_borrow["id"])
        
        book = self.book_repo.find_by_id(book_id)
        book["available"] = True
        self.book_repo.update(book)
        
        return {
            "success": True,
            "message": "归还成功",
            "is_overdue": is_overdue,
            "fine": fine
        }
    
    def get_user_borrow_history(self, user_id: int) -> List[Dict]:
        """获取用户借阅历史"""
        borrows = self.borrow_repo.find_by_user(user_id)
        
        # 添加图书信息
        for borrow in borrows:
            book = self.book_repo.find_by_id(borrow["book_id"])
            borrow["book_title"] = book["title"] if book else "未知"
            borrow["book_author"] = book["author"] if book else "未知"
        
        return borrows

# 表示层 (Presentation Layer)
class LibraryController:
    """图书馆控制器 - 表示层"""
    def __init__(self, library_service: LibraryService):
        self.library_service = library_service
    
    def display_available_books(self):
        """显示可借阅图书"""
        books = self.library_service.get_available_books()
        print("📚 可借阅图书列表:")
        print(f"{'ID':<5} {'书名':<15} {'作者':<10} {'分类':<10}")
        print("-" * 45)
        for book in books:
            print(f"{book['id']:<5} {book['title']:<15} {book['author']:<10} {book['category']:<10}")
    
    def borrow_book_action(self, user_id: int, book_id: int):
        """借阅图书操作"""
        result = self.library_service.borrow_book(user_id, book_id)
        if result["success"]:
            print(f"✅ {result['message']}")
            record = result["borrow_record"]
            print(f"   借阅日期: {record['borrow_date'].strftime('%Y-%m-%d')}")
            print(f"   应还日期: {record['due_date'].strftime('%Y-%m-%d')}")
        else:
            print(f"❌ {result['message']}")
    
    def return_book_action(self, user_id: int, book_id: int):
        """归还图书操作"""
        result = self.library_service.return_book(user_id, book_id)
        if result["success"]:
            print(f"✅ {result['message']}")
            if result["is_overdue"]:
                print(f"   ⚠️  逾期归还，罚金: {result['fine']:.2f}元")
        else:
            print(f"❌ {result['message']}")
    
    def display_user_history(self, user_id: int):
        """显示用户借阅历史"""
        history = self.library_service.get_user_borrow_history(user_id)
        print(f"📖 用户 {user_id} 的借阅历史:")
        print(f"{'书名':<15} {'作者':<10} {'借阅日期':<12} {'状态':<8}")
        print("-" * 50)
        for record in history:
            status = "已归还" if record["is_returned"] else "借阅中"
            borrow_date = record["borrow_date"].strftime('%Y-%m-%d')
            print(f"{record['book_title']:<15} {record['book_author']:<10} {borrow_date:<12} {status:<8}")


def demo_layered_architecture():
    """演示分层架构"""
    # 初始化各层
    book_repo = BookRepository()
    borrow_repo = BorrowRepository()
    library_service = LibraryService(book_repo, borrow_repo)
    controller = LibraryController(library_service)
    
    # 演示功能
    controller.display_available_books()
    
    print("\n🔹 用户1借阅图书1")
    controller.borrow_book_action(1, 1)
    
    print("\n🔹 用户1尝试借阅已借出的图书")
    controller.borrow_book_action(2, 1)
    
    print("\n🔹 用户1归还图书")
    controller.return_book_action(1, 1)
    
    print("\n🔹 用户1的借阅历史")
    controller.display_user_history(1)


# ============================================================================
# 3. 依赖注入容器演示
# ============================================================================

class DIContainer:
    """依赖注入容器"""
    def __init__(self):
        self._services = {}
        self._singletons = {}
        self._factories = {}
    
    def register_singleton(self, interface: str, implementation: type):
        """注册单例服务"""
        self._services[interface] = {
            'type': 'singleton',
            'implementation': implementation
        }
    
    def register_transient(self, interface: str, implementation: type):
        """注册瞬态服务"""
        self._services[interface] = {
            'type': 'transient',
            'implementation': implementation
        }
    
    def register_factory(self, interface: str, factory_func):
        """注册工厂方法"""
        self._factories[interface] = factory_func
    
    def resolve(self, interface: str):
        """解析服务"""
        if interface in self._factories:
            return self._factories[interface]()
        
        if interface not in self._services:
            raise ValueError(f"Service '{interface}' not registered")
        
        service_info = self._services[interface]
        
        if service_info['type'] == 'singleton':
            if interface not in self._singletons:
                self._singletons[interface] = service_info['implementation']()
            return self._singletons[interface]
        
        elif service_info['type'] == 'transient':
            return service_info['implementation']()
    
    def resolve_with_dependencies(self, interface: str, **kwargs):
        """解析带依赖的服务"""
        if interface in self._factories:
            return self._factories[interface](**kwargs)
        
        service_info = self._services[interface]
        return service_info['implementation'](**kwargs)

# 示例服务类
class Logger(ABC):
    """日志记录器接口"""
    @abstractmethod
    def log(self, message: str):
        pass

class ConsoleLogger(Logger):
    """控制台日志记录器"""
    def log(self, message: str):
        print(f"[LOG] {datetime.now().strftime('%H:%M:%S')} - {message}")

class FileLogger(Logger):
    """文件日志记录器"""
    def __init__(self, filename: str = "app.log"):
        self.filename = filename
    
    def log(self, message: str):
        print(f"[FILE LOG] {self.filename} - {message}")

class EmailService:
    """邮件服务"""
    def __init__(self, logger: Logger):
        self.logger = logger
    
    def send_email(self, to: str, subject: str, body: str):
        self.logger.log(f"准备发送邮件给 {to}")
        print(f"📧 发送邮件: {subject} -> {to}")
        self.logger.log("邮件发送完成")

class UserService:
    """用户服务"""
    def __init__(self, logger: Logger, email_service: EmailService):
        self.logger = logger
        self.email_service = email_service
    
    def register_user(self, username: str, email: str):
        self.logger.log(f"开始注册用户: {username}")
        
        # 模拟用户注册逻辑
        user = {"username": username, "email": email, "id": 123}
        
        # 发送欢迎邮件
        self.email_service.send_email(
            email,
            "欢迎注册",
            f"欢迎 {username} 加入我们！"
        )
        
        self.logger.log(f"用户注册完成: {username}")
        return user


def demo_dependency_injection():
    """演示依赖注入容器"""
    container = DIContainer()
    
    # 注册服务
    container.register_singleton('logger', ConsoleLogger)
    
    # 使用工厂方法注册复杂依赖
    container.register_factory('email_service', 
                              lambda: EmailService(container.resolve('logger')))
    
    container.register_factory('user_service',
                              lambda: UserService(
                                  container.resolve('logger'),
                                  container.resolve('email_service')
                              ))
    
    # 使用服务
    print("🔹 使用依赖注入容器")
    user_service = container.resolve('user_service')
    user_service.register_user("alice", "alice@example.com")
    
    print("\n🔹 验证单例模式")
    logger1 = container.resolve('logger')
    logger2 = container.resolve('logger')
    print(f"两个logger实例是否相同: {logger1 is logger2}")
    
    print("\n🔹 使用不同的日志记录器")
    container.register_factory('file_logger', lambda: FileLogger("user.log"))
    file_logger = container.resolve('file_logger')
    file_logger.log("这是文件日志")


# ============================================================================
# 4. 架构模式对比演示
# ============================================================================

class MVCPattern:
    """MVC模式演示"""
    
    class Model:
        """模型 - 数据和业务逻辑"""
        def __init__(self):
            self.tasks = [
                {"id": 1, "title": "学习Python", "completed": False},
                {"id": 2, "title": "设计架构", "completed": True},
            ]
            self.next_id = 3
        
        def get_all_tasks(self):
            return self.tasks
        
        def add_task(self, title):
            task = {"id": self.next_id, "title": title, "completed": False}
            self.next_id += 1
            self.tasks.append(task)
            return task
        
        def toggle_task(self, task_id):
            for task in self.tasks:
                if task["id"] == task_id:
                    task["completed"] = not task["completed"]
                    return task
            return None
    
    class View:
        """视图 - 用户界面"""
        def display_tasks(self, tasks):
            print("📋 任务列表:")
            for task in tasks:
                status = "✅" if task["completed"] else "⭕"
                print(f"  {status} {task['id']}. {task['title']}")
        
        def get_user_input(self, prompt):
            return input(prompt)
        
        def show_message(self, message):
            print(f"💬 {message}")
    
    class Controller:
        """控制器 - 协调模型和视图"""
        def __init__(self, model, view):
            self.model = model
            self.view = view
        
        def show_tasks(self):
            tasks = self.model.get_all_tasks()
            self.view.display_tasks(tasks)
        
        def add_task(self, title):
            task = self.model.add_task(title)
            self.view.show_message(f"任务 '{task['title']}' 已添加")
        
        def toggle_task(self, task_id):
            task = self.model.toggle_task(task_id)
            if task:
                status = "完成" if task["completed"] else "未完成"
                self.view.show_message(f"任务 '{task['title']}' 状态已更新为: {status}")
            else:
                self.view.show_message("任务不存在")

class ObserverPattern:
    """观察者模式演示"""
    
    class Subject:
        """主题/被观察者"""
        def __init__(self):
            self._observers = []
            self._state = None
        
        def attach(self, observer):
            self._observers.append(observer)
        
        def detach(self, observer):
            self._observers.remove(observer)
        
        def notify(self):
            for observer in self._observers:
                observer.update(self._state)
        
        def set_state(self, state):
            self._state = state
            self.notify()
    
    class Observer(ABC):
        """观察者接口"""
        @abstractmethod
        def update(self, state):
            pass
    
    class EmailObserver(Observer):
        """邮件通知观察者"""
        def update(self, state):
            print(f"📧 邮件通知: 状态变更为 {state}")
    
    class SMSObserver(Observer):
        """短信通知观察者"""
        def update(self, state):
            print(f"📱 短信通知: 状态变更为 {state}")
    
    class LogObserver(Observer):
        """日志记录观察者"""
        def update(self, state):
            print(f"📝 日志记录: {datetime.now()} - 状态变更为 {state}")


class StrategyPattern:
    """策略模式演示"""
    
    class PaymentStrategy(ABC):
        """支付策略接口"""
        @abstractmethod
        def pay(self, amount: float) -> str:
            pass
    
    class CreditCardPayment(PaymentStrategy):
        """信用卡支付策略"""
        def pay(self, amount: float) -> str:
            return f"💳 使用信用卡支付 {amount:.2f} 元"
    
    class AlipayPayment(PaymentStrategy):
        """支付宝支付策略"""
        def pay(self, amount: float) -> str:
            return f"📱 使用支付宝支付 {amount:.2f} 元"
    
    class WeChatPayment(PaymentStrategy):
        """微信支付策略"""
        def pay(self, amount: float) -> str:
            return f"💬 使用微信支付 {amount:.2f} 元"
    
    class PaymentContext:
        """支付上下文"""
        def __init__(self, strategy: 'StrategyPattern.PaymentStrategy'):
            self._strategy = strategy
        
        def set_strategy(self, strategy: 'StrategyPattern.PaymentStrategy'):
            self._strategy = strategy
        
        def execute_payment(self, amount: float) -> str:
            return self._strategy.pay(amount)


def demo_architecture_patterns():
    """演示不同架构模式"""
    print("🔹 MVC模式演示")
    mvc = MVCPattern()
    model = mvc.Model()
    view = mvc.View()
    controller = mvc.Controller(model, view)
    
    controller.show_tasks()
    controller.add_task("编写文档")
    controller.toggle_task(1)
    controller.show_tasks()
    
    print("\n🔹 观察者模式演示")
    observer_demo = ObserverPattern()
    subject = observer_demo.Subject()
    
    email_observer = observer_demo.EmailObserver()
    sms_observer = observer_demo.SMSObserver()
    log_observer = observer_demo.LogObserver()
    
    subject.attach(email_observer)
    subject.attach(sms_observer)
    subject.attach(log_observer)
    
    subject.set_state("订单已创建")
    subject.set_state("订单已支付")
    
    print("\n🔹 策略模式演示")
    strategy_demo = StrategyPattern()
    
    # 使用不同的支付策略
    payment_context = strategy_demo.PaymentContext(strategy_demo.CreditCardPayment())
    print(payment_context.execute_payment(100.0))
    
    payment_context.set_strategy(strategy_demo.AlipayPayment())
    print(payment_context.execute_payment(200.0))
    
    payment_context.set_strategy(strategy_demo.WeChatPayment())
    print(payment_context.execute_payment(150.0))


if __name__ == "__main__":
    main()