#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习1: 设计一个图书管理系统的架构

要求:
1. 使用分层架构模式（表示层、业务逻辑层、数据访问层）
2. 应用SOLID设计原则
3. 实现依赖注入
4. 包含以下功能：
   - 图书管理（增删改查）
   - 用户管理（注册、登录）
   - 借阅管理（借书、还书、续借）
   - 通知服务（邮件、短信通知）

请完成以下任务：
1. 设计系统架构图（用注释描述）
2. 定义各层的接口和实现
3. 实现依赖注入容器
4. 编写演示代码
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

# ============================================================================
# 系统架构设计
# ============================================================================

"""
图书管理系统架构图:

┌─────────────────────────────────────────────────────────────┐
│                    表示层 (Presentation Layer)                │
├─────────────────────────────────────────────────────────────┤
│  BookController  │  UserController  │  BorrowController     │
│  - 处理HTTP请求   │  - 用户认证      │  - 借阅操作          │
│  - 数据验证      │  - 用户管理      │  - 归还操作          │
│  - 响应格式化    │  - 权限控制      │  - 续借操作          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   业务逻辑层 (Business Layer)                 │
├─────────────────────────────────────────────────────────────┤
│  BookService     │  UserService     │  BorrowService        │
│  - 图书业务逻辑   │  - 用户业务逻辑   │  - 借阅业务逻辑       │
│  - 库存管理      │  - 密码加密      │  - 逾期检查          │
│  - 分类管理      │  - 权限验证      │  - 借阅限制          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  数据访问层 (Data Access Layer)               │
├─────────────────────────────────────────────────────────────┤
│  BookRepository  │  UserRepository  │  BorrowRepository     │
│  - 图书数据操作   │  - 用户数据操作   │  - 借阅记录操作       │
│  - SQL查询       │  - 数据持久化    │  - 关联查询          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     基础设施层 (Infrastructure)               │
├─────────────────────────────────────────────────────────────┤
│  Database        │  EmailService    │  SMSService           │
│  - 数据库连接     │  - 邮件发送      │  - 短信发送           │
│  - 事务管理      │  - 模板渲染      │  - 消息队列          │
└─────────────────────────────────────────────────────────────┘

横切关注点 (Cross-cutting Concerns):
- 日志记录 (Logging)
- 异常处理 (Exception Handling)
- 安全认证 (Security)
- 缓存管理 (Caching)
- 配置管理 (Configuration)
"""

# ============================================================================
# 领域模型 (Domain Models)
# ============================================================================

class BookStatus(Enum):
    """图书状态"""
    AVAILABLE = "available"
    BORROWED = "borrowed"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"

class UserRole(Enum):
    """用户角色"""
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"

class BorrowStatus(Enum):
    """借阅状态"""
    ACTIVE = "active"
    RETURNED = "returned"
    OVERDUE = "overdue"
    RENEWED = "renewed"

@dataclass
class Book:
    """图书实体"""
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
    """用户实体"""
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
    """借阅记录实体"""
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
# 数据访问层接口 (Data Access Layer Interfaces)
# ============================================================================

# TODO: 定义Repository接口
# 提示: 为Book, User, BorrowRecord分别定义Repository接口
# 包含基本的CRUD操作和特定的查询方法

class IBookRepository(ABC):
    """图书仓储接口"""
    # TODO: 实现以下方法
    pass
    # @abstractmethod
    # def create(self, book: Book) -> Book:
    #     pass
    
    # @abstractmethod
    # def get_by_id(self, book_id: int) -> Optional[Book]:
    #     pass
    
    # @abstractmethod
    # def get_by_isbn(self, isbn: str) -> Optional[Book]:
    #     pass
    
    # @abstractmethod
    # def search(self, keyword: str) -> List[Book]:
    #     pass
    
    # @abstractmethod
    # def get_by_category(self, category: str) -> List[Book]:
    #     pass
    
    # @abstractmethod
    # def update(self, book: Book) -> bool:
    #     pass
    
    # @abstractmethod
    # def delete(self, book_id: int) -> bool:
    #     pass

class IUserRepository(ABC):
    """用户仓储接口"""
    # TODO: 实现用户相关的数据访问方法
    pass

class IBorrowRepository(ABC):
    """借阅记录仓储接口"""
    # TODO: 实现借阅记录相关的数据访问方法
    pass

# ============================================================================
# 业务逻辑层接口 (Business Layer Interfaces)
# ============================================================================

# TODO: 定义Service接口
# 提示: 为Book, User, Borrow分别定义Service接口
# 包含业务逻辑方法，如借书、还书、用户认证等

class IBookService(ABC):
    """图书服务接口"""
    # TODO: 实现图书相关的业务逻辑方法
    pass

class IUserService(ABC):
    """用户服务接口"""
    # TODO: 实现用户相关的业务逻辑方法
    pass

class IBorrowService(ABC):
    """借阅服务接口"""
    # TODO: 实现借阅相关的业务逻辑方法
    pass

# ============================================================================
# 基础设施层接口 (Infrastructure Interfaces)
# ============================================================================

# TODO: 定义基础设施接口
# 提示: 定义数据库、邮件服务、短信服务等接口

class IDatabase(ABC):
    """数据库接口"""
    # TODO: 实现数据库连接和事务管理方法
    pass

class IEmailService(ABC):
    """邮件服务接口"""
    # TODO: 实现邮件发送方法
    pass

class ISMSService(ABC):
    """短信服务接口"""
    # TODO: 实现短信发送方法
    pass

class ILogger(ABC):
    """日志接口"""
    # TODO: 实现日志记录方法
    pass

# ============================================================================
# 数据访问层实现 (Data Access Layer Implementation)
# ============================================================================

# TODO: 实现Repository类
# 提示: 实现上面定义的Repository接口
# 可以使用内存存储或模拟数据库操作

class MemoryBookRepository(IBookRepository):
    """内存图书仓储实现"""
    def __init__(self):
        self._books: Dict[int, Book] = {}
        self._next_id = 1
    
    # TODO: 实现所有接口方法
    pass

class MemoryUserRepository(IUserRepository):
    """内存用户仓储实现"""
    # TODO: 实现用户仓储
    pass

class MemoryBorrowRepository(IBorrowRepository):
    """内存借阅记录仓储实现"""
    # TODO: 实现借阅记录仓储
    pass

# ============================================================================
# 业务逻辑层实现 (Business Layer Implementation)
# ============================================================================

# TODO: 实现Service类
# 提示: 实现上面定义的Service接口
# 注入Repository依赖，实现业务逻辑

class BookService(IBookService):
    """图书服务实现"""
    def __init__(self, book_repository: IBookRepository, logger: ILogger):
        self._book_repository = book_repository
        self._logger = logger
    
    # TODO: 实现图书相关业务逻辑
    pass

class UserService(IUserService):
    """用户服务实现"""
    # TODO: 实现用户服务
    pass

class BorrowService(IBorrowService):
    """借阅服务实现"""
    # TODO: 实现借阅服务
    pass

# ============================================================================
# 基础设施层实现 (Infrastructure Implementation)
# ============================================================================

# TODO: 实现基础设施类
# 提示: 实现数据库、邮件服务、短信服务等

class MockDatabase(IDatabase):
    """模拟数据库实现"""
    # TODO: 实现数据库操作
    pass

class MockEmailService(IEmailService):
    """模拟邮件服务实现"""
    # TODO: 实现邮件发送
    pass

class MockSMSService(ISMSService):
    """模拟短信服务实现"""
    # TODO: 实现短信发送
    pass

class ConsoleLogger(ILogger):
    """控制台日志实现"""
    # TODO: 实现日志记录
    pass

# ============================================================================
# 表示层 (Presentation Layer)
# ============================================================================

# TODO: 实现Controller类
# 提示: 实现处理用户请求的控制器
# 注入Service依赖，处理HTTP请求

class BookController:
    """图书控制器"""
    def __init__(self, book_service: IBookService, logger: ILogger):
        self._book_service = book_service
        self._logger = logger
    
    # TODO: 实现图书相关的API端点
    pass

class UserController:
    """用户控制器"""
    # TODO: 实现用户控制器
    pass

class BorrowController:
    """借阅控制器"""
    # TODO: 实现借阅控制器
    pass

# ============================================================================
# 依赖注入容器 (Dependency Injection Container)
# ============================================================================

# TODO: 实现依赖注入容器
# 提示: 参考examples中的依赖注入示例
# 管理所有组件的创建和依赖关系

class DIContainer:
    """依赖注入容器"""
    def __init__(self):
        self._services = {}
        self._instances = {}
    
    # TODO: 实现服务注册和解析方法
    pass

# ============================================================================
# 应用程序入口 (Application Entry Point)
# ============================================================================

def create_application() -> DIContainer:
    """创建应用程序"""
    container = DIContainer()
    
    # TODO: 注册所有服务到容器
    # 提示: 按照依赖关系的顺序注册服务
    # 1. 基础设施层服务
    # 2. 数据访问层服务
    # 3. 业务逻辑层服务
    # 4. 表示层服务
    
    return container

def main():
    """主函数"""
    print("图书管理系统架构设计练习")
    print("=" * 40)
    
    # TODO: 创建应用程序并演示功能
    # 提示: 
    # 1. 创建应用程序容器
    # 2. 获取控制器实例
    # 3. 演示各种功能
    
    # 示例演示代码:
    # container = create_application()
    # book_controller = container.resolve("book_controller")
    # user_controller = container.resolve("user_controller")
    # borrow_controller = container.resolve("borrow_controller")
    
    # 演示图书管理
    # print("\n📚 图书管理演示:")
    # book_controller.create_book({...})
    # book_controller.search_books("Python")
    
    # 演示用户管理
    # print("\n👤 用户管理演示:")
    # user_controller.register_user({...})
    # user_controller.login({...})
    
    # 演示借阅管理
    # print("\n📖 借阅管理演示:")
    # borrow_controller.borrow_book({...})
    # borrow_controller.return_book({...})
    
    print("\n✅ 练习完成！")
    print("\n💡 扩展建议:")
    print("1. 添加图书预约功能")
    print("2. 实现图书推荐系统")
    print("3. 添加罚金计算和支付")
    print("4. 实现图书评价和评论")
    print("5. 添加图书统计和报表")

if __name__ == "__main__":
    main()

# ============================================================================
# 练习指导
# ============================================================================

"""
练习完成指导:

1. 接口设计 (30分钟)
   - 完善所有抽象接口的方法定义
   - 确保接口职责单一，符合SOLID原则
   - 考虑方法的参数和返回值类型

2. 实现类编写 (60分钟)
   - 实现所有Repository类的数据访问逻辑
   - 实现所有Service类的业务逻辑
   - 实现基础设施类的功能
   - 实现Controller类的请求处理

3. 依赖注入 (30分钟)
   - 完善DIContainer的实现
   - 注册所有服务到容器
   - 确保依赖关系正确

4. 演示代码 (30分钟)
   - 编写完整的演示流程
   - 测试各个功能模块
   - 验证架构设计的正确性

5. 扩展功能 (可选)
   - 添加缓存层
   - 实现事件驱动架构
   - 添加API文档
   - 实现单元测试

评估标准:
- 架构设计是否清晰合理
- 是否正确应用SOLID原则
- 依赖注入是否实现正确
- 代码是否可以正常运行
- 功能是否完整
"""