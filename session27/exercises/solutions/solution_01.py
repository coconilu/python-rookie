#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习1解决方案: 图书管理系统架构实现

这是exercise_01.py的完整实现示例，展示了如何设计和实现
一个完整的分层架构系统。
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Type, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import hashlib
import json

# ============================================================================
# 领域模型 (Domain Models) - 重用exercise_01.py中的定义
# ============================================================================

class BookStatus(Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"

class UserRole(Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"

class BorrowStatus(Enum):
    ACTIVE = "active"
    RETURNED = "returned"
    OVERDUE = "overdue"
    RENEWED = "renewed"

@dataclass
class Book:
    book_id: int
    title: str
    author: str
    isbn: str
    category: str
    publisher: str
    publish_date: datetime
    status: BookStatus
    location: str
    created_at: datetime
    updated_at: datetime

@dataclass
class User:
    user_id: int
    username: str
    email: str
    password_hash: str
    full_name: str
    phone: str
    role: UserRole
    max_borrow_count: int
    created_at: datetime
    last_login: Optional[datetime]

@dataclass
class BorrowRecord:
    record_id: int
    user_id: int
    book_id: int
    borrow_date: datetime
    due_date: datetime
    return_date: Optional[datetime]
    status: BorrowStatus
    renewal_count: int
    fine_amount: float

# ============================================================================
# 数据访问层接口实现 (Data Access Layer Implementation)
# ============================================================================

class IBookRepository(ABC):
    """图书仓储接口"""
    @abstractmethod
    def create(self, book: Book) -> Book:
        pass
    
    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Book]:
        pass
    
    @abstractmethod
    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        pass
    
    @abstractmethod
    def search(self, keyword: str) -> List[Book]:
        pass
    
    @abstractmethod
    def get_by_category(self, category: str) -> List[Book]:
        pass
    
    @abstractmethod
    def update(self, book: Book) -> bool:
        pass
    
    @abstractmethod
    def delete(self, book_id: int) -> bool:
        pass
    
    @abstractmethod
    def get_available_books(self) -> List[Book]:
        pass

class IUserRepository(ABC):
    """用户仓储接口"""
    @abstractmethod
    def create(self, user: User) -> User:
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def update(self, user: User) -> bool:
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        pass

class IBorrowRepository(ABC):
    """借阅记录仓储接口"""
    @abstractmethod
    def create(self, record: BorrowRecord) -> BorrowRecord:
        pass
    
    @abstractmethod
    def get_by_id(self, record_id: int) -> Optional[BorrowRecord]:
        pass
    
    @abstractmethod
    def get_by_user(self, user_id: int) -> List[BorrowRecord]:
        pass
    
    @abstractmethod
    def get_by_book(self, book_id: int) -> List[BorrowRecord]:
        pass
    
    @abstractmethod
    def get_active_borrows(self, user_id: int) -> List[BorrowRecord]:
        pass
    
    @abstractmethod
    def get_overdue_records(self) -> List[BorrowRecord]:
        pass
    
    @abstractmethod
    def update(self, record: BorrowRecord) -> bool:
        pass

# ============================================================================
# 数据访问层实现 (Repository Implementation)
# ============================================================================

class MemoryBookRepository(IBookRepository):
    """内存图书仓储实现"""
    def __init__(self):
        self._books: Dict[int, Book] = {}
        self._next_id = 1
    
    def create(self, book: Book) -> Book:
        book.book_id = self._next_id
        book.created_at = datetime.now()
        book.updated_at = datetime.now()
        self._books[book.book_id] = book
        self._next_id += 1
        return book
    
    def get_by_id(self, book_id: int) -> Optional[Book]:
        return self._books.get(book_id)
    
    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        for book in self._books.values():
            if book.isbn == isbn:
                return book
        return None
    
    def search(self, keyword: str) -> List[Book]:
        keyword = keyword.lower()
        results = []
        for book in self._books.values():
            if (keyword in book.title.lower() or 
                keyword in book.author.lower() or 
                keyword in book.category.lower()):
                results.append(book)
        return results
    
    def get_by_category(self, category: str) -> List[Book]:
        return [book for book in self._books.values() if book.category == category]
    
    def update(self, book: Book) -> bool:
        if book.book_id in self._books:
            book.updated_at = datetime.now()
            self._books[book.book_id] = book
            return True
        return False
    
    def delete(self, book_id: int) -> bool:
        if book_id in self._books:
            del self._books[book_id]
            return True
        return False
    
    def get_available_books(self) -> List[Book]:
        return [book for book in self._books.values() if book.status == BookStatus.AVAILABLE]

class MemoryUserRepository(IUserRepository):
    """内存用户仓储实现"""
    def __init__(self):
        self._users: Dict[int, User] = {}
        self._next_id = 1
    
    def create(self, user: User) -> User:
        user.user_id = self._next_id
        user.created_at = datetime.now()
        self._users[user.user_id] = user
        self._next_id += 1
        return user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)
    
    def get_by_username(self, username: str) -> Optional[User]:
        for user in self._users.values():
            if user.username == username:
                return user
        return None
    
    def get_by_email(self, email: str) -> Optional[User]:
        for user in self._users.values():
            if user.email == email:
                return user
        return None
    
    def update(self, user: User) -> bool:
        if user.user_id in self._users:
            self._users[user.user_id] = user
            return True
        return False
    
    def delete(self, user_id: int) -> bool:
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False

class MemoryBorrowRepository(IBorrowRepository):
    """内存借阅记录仓储实现"""
    def __init__(self):
        self._records: Dict[int, BorrowRecord] = {}
        self._next_id = 1
    
    def create(self, record: BorrowRecord) -> BorrowRecord:
        record.record_id = self._next_id
        self._records[record.record_id] = record
        self._next_id += 1
        return record
    
    def get_by_id(self, record_id: int) -> Optional[BorrowRecord]:
        return self._records.get(record_id)
    
    def get_by_user(self, user_id: int) -> List[BorrowRecord]:
        return [record for record in self._records.values() if record.user_id == user_id]
    
    def get_by_book(self, book_id: int) -> List[BorrowRecord]:
        return [record for record in self._records.values() if record.book_id == book_id]
    
    def get_active_borrows(self, user_id: int) -> List[BorrowRecord]:
        return [record for record in self._records.values() 
                if record.user_id == user_id and record.status == BorrowStatus.ACTIVE]
    
    def get_overdue_records(self) -> List[BorrowRecord]:
        now = datetime.now()
        overdue = []
        for record in self._records.values():
            if (record.status == BorrowStatus.ACTIVE and 
                record.due_date < now):
                record.status = BorrowStatus.OVERDUE
                overdue.append(record)
        return overdue
    
    def update(self, record: BorrowRecord) -> bool:
        if record.record_id in self._records:
            self._records[record.record_id] = record
            return True
        return False

# ============================================================================
# 基础设施层接口和实现 (Infrastructure Layer)
# ============================================================================

class ILogger(ABC):
    @abstractmethod
    def info(self, message: str):
        pass
    
    @abstractmethod
    def warning(self, message: str):
        pass
    
    @abstractmethod
    def error(self, message: str):
        pass

class IEmailService(ABC):
    @abstractmethod
    def send_email(self, to: str, subject: str, body: str) -> bool:
        pass

class ISMSService(ABC):
    @abstractmethod
    def send_sms(self, phone: str, message: str) -> bool:
        pass

class ConsoleLogger(ILogger):
    """控制台日志实现"""
    def info(self, message: str):
        print(f"[INFO] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")
    
    def warning(self, message: str):
        print(f"[WARNING] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")
    
    def error(self, message: str):
        print(f"[ERROR] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")

class MockEmailService(IEmailService):
    """模拟邮件服务"""
    def send_email(self, to: str, subject: str, body: str) -> bool:
        print(f"📧 发送邮件到 {to}")
        print(f"   主题: {subject}")
        print(f"   内容: {body}")
        return True

class MockSMSService(ISMSService):
    """模拟短信服务"""
    def send_sms(self, phone: str, message: str) -> bool:
        print(f"📱 发送短信到 {phone}: {message}")
        return True

# ============================================================================
# 业务逻辑层接口和实现 (Business Layer)
# ============================================================================

class IBookService(ABC):
    @abstractmethod
    def create_book(self, title: str, author: str, isbn: str, category: str, 
                   publisher: str, publish_date: datetime, location: str) -> Book:
        pass
    
    @abstractmethod
    def get_book(self, book_id: int) -> Optional[Book]:
        pass
    
    @abstractmethod
    def search_books(self, keyword: str) -> List[Book]:
        pass
    
    @abstractmethod
    def update_book_status(self, book_id: int, status: BookStatus) -> bool:
        pass
    
    @abstractmethod
    def delete_book(self, book_id: int) -> bool:
        pass

class IUserService(ABC):
    @abstractmethod
    def register_user(self, username: str, email: str, password: str, 
                     full_name: str, phone: str, role: UserRole) -> User:
        pass
    
    @abstractmethod
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_user(self, user_id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    def update_user(self, user: User) -> bool:
        pass

class IBorrowService(ABC):
    @abstractmethod
    def borrow_book(self, user_id: int, book_id: int) -> Optional[BorrowRecord]:
        pass
    
    @abstractmethod
    def return_book(self, record_id: int) -> bool:
        pass
    
    @abstractmethod
    def renew_book(self, record_id: int) -> bool:
        pass
    
    @abstractmethod
    def get_user_borrows(self, user_id: int) -> List[BorrowRecord]:
        pass
    
    @abstractmethod
    def check_overdue_books(self) -> List[BorrowRecord]:
        pass

class BookService(IBookService):
    """图书服务实现"""
    def __init__(self, book_repository: IBookRepository, logger: ILogger):
        self._book_repository = book_repository
        self._logger = logger
    
    def create_book(self, title: str, author: str, isbn: str, category: str, 
                   publisher: str, publish_date: datetime, location: str) -> Book:
        # 检查ISBN是否已存在
        existing_book = self._book_repository.get_by_isbn(isbn)
        if existing_book:
            raise ValueError(f"ISBN {isbn} 已存在")
        
        book = Book(
            book_id=0,  # 将由repository分配
            title=title,
            author=author,
            isbn=isbn,
            category=category,
            publisher=publisher,
            publish_date=publish_date,
            status=BookStatus.AVAILABLE,
            location=location,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        created_book = self._book_repository.create(book)
        self._logger.info(f"创建图书: {created_book.title} (ID: {created_book.book_id})")
        return created_book
    
    def get_book(self, book_id: int) -> Optional[Book]:
        return self._book_repository.get_by_id(book_id)
    
    def search_books(self, keyword: str) -> List[Book]:
        self._logger.info(f"搜索图书: {keyword}")
        return self._book_repository.search(keyword)
    
    def update_book_status(self, book_id: int, status: BookStatus) -> bool:
        book = self._book_repository.get_by_id(book_id)
        if not book:
            return False
        
        book.status = status
        book.updated_at = datetime.now()
        success = self._book_repository.update(book)
        
        if success:
            self._logger.info(f"更新图书状态: {book.title} -> {status.value}")
        
        return success
    
    def delete_book(self, book_id: int) -> bool:
        book = self._book_repository.get_by_id(book_id)
        if not book:
            return False
        
        success = self._book_repository.delete(book_id)
        if success:
            self._logger.info(f"删除图书: {book.title} (ID: {book_id})")
        
        return success

class UserService(IUserService):
    """用户服务实现"""
    def __init__(self, user_repository: IUserRepository, logger: ILogger):
        self._user_repository = user_repository
        self._logger = logger
    
    def register_user(self, username: str, email: str, password: str, 
                     full_name: str, phone: str, role: UserRole) -> User:
        # 检查用户名和邮箱是否已存在
        if self._user_repository.get_by_username(username):
            raise ValueError(f"用户名 {username} 已存在")
        
        if self._user_repository.get_by_email(email):
            raise ValueError(f"邮箱 {email} 已存在")
        
        # 密码哈希
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # 根据角色设置借阅限制
        max_borrow_count = {
            UserRole.STUDENT: 5,
            UserRole.TEACHER: 10,
            UserRole.ADMIN: 20
        }.get(role, 5)
        
        user = User(
            user_id=0,  # 将由repository分配
            username=username,
            email=email,
            password_hash=password_hash,
            full_name=full_name,
            phone=phone,
            role=role,
            max_borrow_count=max_borrow_count,
            created_at=datetime.now(),
            last_login=None
        )
        
        created_user = self._user_repository.create(user)
        self._logger.info(f"注册用户: {created_user.username} ({created_user.role.value})")
        return created_user
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self._user_repository.get_by_username(username)
        if not user:
            return None
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if user.password_hash != password_hash:
            return None
        
        # 更新最后登录时间
        user.last_login = datetime.now()
        self._user_repository.update(user)
        
        self._logger.info(f"用户登录: {user.username}")
        return user
    
    def get_user(self, user_id: int) -> Optional[User]:
        return self._user_repository.get_by_id(user_id)
    
    def update_user(self, user: User) -> bool:
        success = self._user_repository.update(user)
        if success:
            self._logger.info(f"更新用户信息: {user.username}")
        return success

class BorrowService(IBorrowService):
    """借阅服务实现"""
    def __init__(self, borrow_repository: IBorrowRepository, 
                 book_repository: IBookRepository, 
                 user_repository: IUserRepository,
                 email_service: IEmailService,
                 sms_service: ISMSService,
                 logger: ILogger):
        self._borrow_repository = borrow_repository
        self._book_repository = book_repository
        self._user_repository = user_repository
        self._email_service = email_service
        self._sms_service = sms_service
        self._logger = logger
    
    def borrow_book(self, user_id: int, book_id: int) -> Optional[BorrowRecord]:
        # 验证用户和图书
        user = self._user_repository.get_by_id(user_id)
        book = self._book_repository.get_by_id(book_id)
        
        if not user or not book:
            return None
        
        # 检查图书是否可借
        if book.status != BookStatus.AVAILABLE:
            raise ValueError("图书不可借阅")
        
        # 检查用户借阅限制
        active_borrows = self._borrow_repository.get_active_borrows(user_id)
        if len(active_borrows) >= user.max_borrow_count:
            raise ValueError(f"超出借阅限制 ({user.max_borrow_count} 本)")
        
        # 创建借阅记录
        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days=30)  # 30天借期
        
        record = BorrowRecord(
            record_id=0,  # 将由repository分配
            user_id=user_id,
            book_id=book_id,
            borrow_date=borrow_date,
            due_date=due_date,
            return_date=None,
            status=BorrowStatus.ACTIVE,
            renewal_count=0,
            fine_amount=0.0
        )
        
        # 保存借阅记录
        created_record = self._borrow_repository.create(record)
        
        # 更新图书状态
        book.status = BookStatus.BORROWED
        self._book_repository.update(book)
        
        # 发送通知
        self._email_service.send_email(
            user.email,
            "借阅成功通知",
            f"您已成功借阅《{book.title}》，请于 {due_date.strftime('%Y-%m-%d')} 前归还。"
        )
        
        self._logger.info(f"借阅图书: {user.username} 借阅 《{book.title}》")
        return created_record
    
    def return_book(self, record_id: int) -> bool:
        record = self._borrow_repository.get_by_id(record_id)
        if not record or record.status != BorrowStatus.ACTIVE:
            return False
        
        # 更新借阅记录
        record.return_date = datetime.now()
        record.status = BorrowStatus.RETURNED
        
        # 计算罚金（如果逾期）
        if record.return_date > record.due_date:
            overdue_days = (record.return_date - record.due_date).days
            record.fine_amount = overdue_days * 1.0  # 每天1元罚金
        
        # 更新图书状态
        book = self._book_repository.get_by_id(record.book_id)
        if book:
            book.status = BookStatus.AVAILABLE
            self._book_repository.update(book)
        
        # 保存更新
        success = self._borrow_repository.update(record)
        
        if success:
            user = self._user_repository.get_by_id(record.user_id)
            if user and book:
                # 发送归还通知
                message = f"您已成功归还《{book.title}》"
                if record.fine_amount > 0:
                    message += f"，产生罚金 {record.fine_amount} 元"
                
                self._email_service.send_email(user.email, "归还成功通知", message)
                self._logger.info(f"归还图书: {user.username} 归还 《{book.title}》")
        
        return success
    
    def renew_book(self, record_id: int) -> bool:
        record = self._borrow_repository.get_by_id(record_id)
        if not record or record.status != BorrowStatus.ACTIVE:
            return False
        
        # 检查续借次数限制
        if record.renewal_count >= 2:  # 最多续借2次
            raise ValueError("超出续借次数限制")
        
        # 检查是否逾期
        if datetime.now() > record.due_date:
            raise ValueError("逾期图书不能续借")
        
        # 更新借阅记录
        record.due_date += timedelta(days=15)  # 续借15天
        record.renewal_count += 1
        record.status = BorrowStatus.RENEWED
        
        success = self._borrow_repository.update(record)
        
        if success:
            user = self._user_repository.get_by_id(record.user_id)
            book = self._book_repository.get_by_id(record.book_id)
            if user and book:
                self._email_service.send_email(
                    user.email,
                    "续借成功通知",
                    f"《{book.title}》续借成功，新的归还日期为 {record.due_date.strftime('%Y-%m-%d')}"
                )
                self._logger.info(f"续借图书: {user.username} 续借 《{book.title}》")
        
        return success
    
    def get_user_borrows(self, user_id: int) -> List[BorrowRecord]:
        return self._borrow_repository.get_by_user(user_id)
    
    def check_overdue_books(self) -> List[BorrowRecord]:
        overdue_records = self._borrow_repository.get_overdue_records()
        
        # 发送逾期通知
        for record in overdue_records:
            user = self._user_repository.get_by_id(record.user_id)
            book = self._book_repository.get_by_id(record.book_id)
            
            if user and book:
                overdue_days = (datetime.now() - record.due_date).days
                message = f"您借阅的《{book.title}》已逾期 {overdue_days} 天，请尽快归还。"
                
                self._email_service.send_email(user.email, "逾期提醒", message)
                self._sms_service.send_sms(user.phone, message)
        
        if overdue_records:
            self._logger.warning(f"发现 {len(overdue_records)} 本逾期图书")
        
        return overdue_records

# ============================================================================
# 表示层 (Presentation Layer)
# ============================================================================

class BookController:
    """图书控制器"""
    def __init__(self, book_service: IBookService, logger: ILogger):
        self._book_service = book_service
        self._logger = logger
    
    def create_book(self, book_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            book = self._book_service.create_book(
                title=book_data['title'],
                author=book_data['author'],
                isbn=book_data['isbn'],
                category=book_data['category'],
                publisher=book_data['publisher'],
                publish_date=datetime.fromisoformat(book_data['publish_date']),
                location=book_data['location']
            )
            return {
                'success': True,
                'data': {
                    'book_id': book.book_id,
                    'title': book.title,
                    'author': book.author,
                    'isbn': book.isbn,
                    'status': book.status.value
                },
                'message': '图书创建成功'
            }
        except Exception as e:
            self._logger.error(f"创建图书失败: {str(e)}")
            return {
                'success': False,
                'data': None,
                'message': f'创建失败: {str(e)}'
            }
    
    def search_books(self, keyword: str) -> Dict[str, Any]:
        try:
            books = self._book_service.search_books(keyword)
            return {
                'success': True,
                'data': [
                    {
                        'book_id': book.book_id,
                        'title': book.title,
                        'author': book.author,
                        'category': book.category,
                        'status': book.status.value
                    } for book in books
                ],
                'message': f'找到 {len(books)} 本图书'
            }
        except Exception as e:
            self._logger.error(f"搜索图书失败: {str(e)}")
            return {
                'success': False,
                'data': [],
                'message': f'搜索失败: {str(e)}'
            }

class UserController:
    """用户控制器"""
    def __init__(self, user_service: IUserService, logger: ILogger):
        self._user_service = user_service
        self._logger = logger
    
    def register_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            user = self._user_service.register_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                full_name=user_data['full_name'],
                phone=user_data['phone'],
                role=UserRole(user_data['role'])
            )
            return {
                'success': True,
                'data': {
                    'user_id': user.user_id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role.value
                },
                'message': '用户注册成功'
            }
        except Exception as e:
            self._logger.error(f"用户注册失败: {str(e)}")
            return {
                'success': False,
                'data': None,
                'message': f'注册失败: {str(e)}'
            }
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        try:
            user = self._user_service.authenticate_user(username, password)
            if user:
                return {
                    'success': True,
                    'data': {
                        'user_id': user.user_id,
                        'username': user.username,
                        'role': user.role.value,
                        'last_login': user.last_login.isoformat() if user.last_login else None
                    },
                    'message': '登录成功'
                }
            else:
                return {
                    'success': False,
                    'data': None,
                    'message': '用户名或密码错误'
                }
        except Exception as e:
            self._logger.error(f"用户登录失败: {str(e)}")
            return {
                'success': False,
                'data': None,
                'message': f'登录失败: {str(e)}'
            }

class BorrowController:
    """借阅控制器"""
    def __init__(self, borrow_service: IBorrowService, logger: ILogger):
        self._borrow_service = borrow_service
        self._logger = logger
    
    def borrow_book(self, user_id: int, book_id: int) -> Dict[str, Any]:
        try:
            record = self._borrow_service.borrow_book(user_id, book_id)
            if record:
                return {
                    'success': True,
                    'data': {
                        'record_id': record.record_id,
                        'borrow_date': record.borrow_date.isoformat(),
                        'due_date': record.due_date.isoformat(),
                        'status': record.status.value
                    },
                    'message': '借阅成功'
                }
            else:
                return {
                    'success': False,
                    'data': None,
                    'message': '借阅失败'
                }
        except Exception as e:
            self._logger.error(f"借阅失败: {str(e)}")
            return {
                'success': False,
                'data': None,
                'message': f'借阅失败: {str(e)}'
            }
    
    def return_book(self, record_id: int) -> Dict[str, Any]:
        try:
            success = self._borrow_service.return_book(record_id)
            if success:
                return {
                    'success': True,
                    'data': None,
                    'message': '归还成功'
                }
            else:
                return {
                    'success': False,
                    'data': None,
                    'message': '归还失败'
                }
        except Exception as e:
            self._logger.error(f"归还失败: {str(e)}")
            return {
                'success': False,
                'data': None,
                'message': f'归还失败: {str(e)}'
            }

# ============================================================================
# 依赖注入容器 (Dependency Injection Container)
# ============================================================================

class DIContainer:
    """依赖注入容器"""
    def __init__(self):
        self._services: Dict[str, Callable] = {}
        self._instances: Dict[str, Any] = {}
        self._singletons: Dict[str, bool] = {}
    
    def register(self, name: str, factory: Callable, singleton: bool = True):
        """注册服务"""
        self._services[name] = factory
        self._singletons[name] = singleton
    
    def resolve(self, name: str) -> Any:
        """解析服务"""
        if name not in self._services:
            raise ValueError(f"服务 {name} 未注册")
        
        # 如果是单例且已创建，直接返回
        if self._singletons[name] and name in self._instances:
            return self._instances[name]
        
        # 创建实例
        factory = self._services[name]
        instance = factory()
        
        # 如果是单例，缓存实例
        if self._singletons[name]:
            self._instances[name] = instance
        
        return instance

# ============================================================================
# 应用程序配置 (Application Setup)
# ============================================================================

def create_application() -> DIContainer:
    """创建应用程序"""
    container = DIContainer()
    
    # 注册基础设施服务
    container.register("logger", lambda: ConsoleLogger())
    container.register("email_service", lambda: MockEmailService())
    container.register("sms_service", lambda: MockSMSService())
    
    # 注册数据访问层服务
    container.register("book_repository", lambda: MemoryBookRepository())
    container.register("user_repository", lambda: MemoryUserRepository())
    container.register("borrow_repository", lambda: MemoryBorrowRepository())
    
    # 注册业务逻辑层服务
    container.register("book_service", lambda: BookService(
        container.resolve("book_repository"),
        container.resolve("logger")
    ))
    
    container.register("user_service", lambda: UserService(
        container.resolve("user_repository"),
        container.resolve("logger")
    ))
    
    container.register("borrow_service", lambda: BorrowService(
        container.resolve("borrow_repository"),
        container.resolve("book_repository"),
        container.resolve("user_repository"),
        container.resolve("email_service"),
        container.resolve("sms_service"),
        container.resolve("logger")
    ))
    
    # 注册表示层服务
    container.register("book_controller", lambda: BookController(
        container.resolve("book_service"),
        container.resolve("logger")
    ))
    
    container.register("user_controller", lambda: UserController(
        container.resolve("user_service"),
        container.resolve("logger")
    ))
    
    container.register("borrow_controller", lambda: BorrowController(
        container.resolve("borrow_service"),
        container.resolve("logger")
    ))
    
    return container

# ============================================================================
# 演示代码 (Demo Code)
# ============================================================================

def create_sample_data(container: DIContainer):
    """创建示例数据"""
    book_controller = container.resolve("book_controller")
    user_controller = container.resolve("user_controller")
    
    # 创建示例图书
    books_data = [
        {
            'title': 'Python编程：从入门到实践',
            'author': 'Eric Matthes',
            'isbn': '9787115428028',
            'category': '编程',
            'publisher': '人民邮电出版社',
            'publish_date': '2016-07-01',
            'location': 'A区1层001'
        },
        {
            'title': '深度学习',
            'author': 'Ian Goodfellow',
            'isbn': '9787115461476',
            'category': '人工智能',
            'publisher': '人民邮电出版社',
            'publish_date': '2017-07-01',
            'location': 'B区2层015'
        },
        {
            'title': '算法导论',
            'author': 'Thomas H. Cormen',
            'isbn': '9787111407010',
            'category': '算法',
            'publisher': '机械工业出版社',
            'publish_date': '2012-12-01',
            'location': 'A区2层032'
        }
    ]
    
    for book_data in books_data:
        result = book_controller.create_book(book_data)
        if result['success']:
            print(f"✅ 创建图书: {book_data['title']}")
    
    # 创建示例用户
    users_data = [
        {
            'username': 'student1',
            'email': 'student1@example.com',
            'password': 'password123',
            'full_name': '张三',
            'phone': '13800138001',
            'role': 'student'
        },
        {
            'username': 'teacher1',
            'email': 'teacher1@example.com',
            'password': 'password123',
            'full_name': '李老师',
            'phone': '13800138002',
            'role': 'teacher'
        },
        {
            'username': 'admin1',
            'email': 'admin1@example.com',
            'password': 'admin123',
            'full_name': '管理员',
            'phone': '13800138003',
            'role': 'admin'
        }
    ]
    
    for user_data in users_data:
        result = user_controller.register_user(user_data)
        if result['success']:
            print(f"✅ 注册用户: {user_data['username']} ({user_data['role']})")

def demo_library_system(container: DIContainer):
    """演示图书管理系统"""
    print("\n📚 图书管理系统演示")
    print("=" * 50)
    
    # 获取控制器
    book_controller = container.resolve("book_controller")
    user_controller = container.resolve("user_controller")
    borrow_controller = container.resolve("borrow_controller")
    borrow_service = container.resolve("borrow_service")
    
    print("\n1. 用户登录演示:")
    login_result = user_controller.login("student1", "password123")
    print(f"登录结果: {login_result['message']}")
    if login_result['success']:
        user_id = login_result['data']['user_id']
        print(f"用户ID: {user_id}")
    
    print("\n2. 图书搜索演示:")
    search_result = book_controller.search_books("Python")
    print(f"搜索结果: {search_result['message']}")
    if search_result['success'] and search_result['data']:
        book_id = search_result['data'][0]['book_id']
        book_title = search_result['data'][0]['title']
        print(f"找到图书: {book_title} (ID: {book_id})")
    
    print("\n3. 借阅图书演示:")
    if 'user_id' in locals() and 'book_id' in locals():
        borrow_result = borrow_controller.borrow_book(user_id, book_id)
        print(f"借阅结果: {borrow_result['message']}")
        if borrow_result['success']:
            record_id = borrow_result['data']['record_id']
            due_date = borrow_result['data']['due_date']
            print(f"借阅记录ID: {record_id}")
            print(f"归还日期: {due_date[:10]}")
    
    print("\n4. 查看用户借阅记录:")
    if 'user_id' in locals():
        user_borrows = borrow_service.get_user_borrows(user_id)
        print(f"当前借阅: {len(user_borrows)} 本图书")
        for record in user_borrows:
            if record.status == BorrowStatus.ACTIVE:
                print(f"  - 记录ID: {record.record_id}, 图书ID: {record.book_id}, 状态: {record.status.value}")
    
    print("\n5. 归还图书演示:")
    if 'record_id' in locals():
        return_result = borrow_controller.return_book(record_id)
        print(f"归还结果: {return_result['message']}")
    
    print("\n6. 逾期检查演示:")
    overdue_records = borrow_service.check_overdue_books()
    print(f"逾期图书: {len(overdue_records)} 本")

def main():
    """主函数"""
    print("图书管理系统架构设计 - 完整实现")
    print("=" * 60)
    
    # 创建应用程序
    print("\n🏗️ 初始化应用程序...")
    container = create_application()
    print("✅ 应用程序初始化完成")
    
    # 创建示例数据
    print("\n📝 创建示例数据...")
    create_sample_data(container)
    print("✅ 示例数据创建完成")
    
    # 演示系统功能
    demo_library_system(container)
    
    print("\n🎯 架构设计要点总结:")
    print("1. ✅ 分层架构: 表示层 -> 业务逻辑层 -> 数据访问层 -> 基础设施层")
    print("2. ✅ SOLID原则: 单一职责、开闭原则、里氏替换、接口隔离、依赖倒置")
    print("3. ✅ 依赖注入: 通过容器管理组件依赖关系")
    print("4. ✅ 接口抽象: 定义清晰的接口契约")
    print("5. ✅ 关注点分离: 业务逻辑与技术实现分离")
    
    print("\n💡 扩展建议:")
    print("1. 添加数据库持久化层")
    print("2. 实现Web API接口")
    print("3. 添加缓存机制")
    print("4. 实现事件驱动架构")
    print("5. 添加单元测试和集成测试")
    
    print("\n✅ 练习完成！")

if __name__ == "__main__":
    main()