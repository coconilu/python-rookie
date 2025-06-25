#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session28 示例1：依赖注入模式详解

本示例展示了依赖注入的不同实现方式和最佳实践。

作者: Python教程团队
创建日期: 2024-01-15
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import json


# ============================================================================
# 1. 传统方式 vs 依赖注入对比
# ============================================================================

class TraditionalUserService:
    """传统方式：直接依赖具体实现"""
    
    def __init__(self):
        # 直接创建依赖，紧耦合
        self.database = MySQLDatabase()  # 硬编码依赖
        self.email_service = SMTPEmailService()  # 硬编码依赖
        self.logger = FileLogger()  # 硬编码依赖
    
    def create_user(self, username: str, email: str) -> bool:
        """创建用户"""
        # 业务逻辑与具体实现紧密耦合
        user_data = {'username': username, 'email': email}
        
        if self.database.save_user(user_data):
            self.email_service.send_welcome_email(email)
            self.logger.log(f"User {username} created successfully")
            return True
        return False


# ============================================================================
# 2. 接口定义
# ============================================================================

class DatabaseInterface(ABC):
    """数据库接口"""
    
    @abstractmethod
    def save_user(self, user_data: Dict[str, Any]) -> bool:
        pass
    
    @abstractmethod
    def find_user(self, username: str) -> Optional[Dict[str, Any]]:
        pass


class EmailServiceInterface(ABC):
    """邮件服务接口"""
    
    @abstractmethod
    def send_welcome_email(self, email: str) -> bool:
        pass
    
    @abstractmethod
    def send_notification(self, email: str, message: str) -> bool:
        pass


class LoggerInterface(ABC):
    """日志接口"""
    
    @abstractmethod
    def log(self, message: str) -> None:
        pass
    
    @abstractmethod
    def error(self, message: str) -> None:
        pass


# ============================================================================
# 3. 具体实现类
# ============================================================================

class MySQLDatabase(DatabaseInterface):
    """MySQL数据库实现"""
    
    def __init__(self, connection_string: str = "mysql://localhost"):
        self.connection_string = connection_string
        print(f"🔗 MySQL数据库连接: {connection_string}")
    
    def save_user(self, user_data: Dict[str, Any]) -> bool:
        print(f"💾 MySQL: 保存用户 {user_data['username']}")
        return True
    
    def find_user(self, username: str) -> Optional[Dict[str, Any]]:
        print(f"🔍 MySQL: 查找用户 {username}")
        return {'username': username, 'email': f'{username}@example.com'}


class PostgreSQLDatabase(DatabaseInterface):
    """PostgreSQL数据库实现"""
    
    def __init__(self, host: str = "localhost", port: int = 5432):
        self.host = host
        self.port = port
        print(f"🔗 PostgreSQL数据库连接: {host}:{port}")
    
    def save_user(self, user_data: Dict[str, Any]) -> bool:
        print(f"💾 PostgreSQL: 保存用户 {user_data['username']}")
        return True
    
    def find_user(self, username: str) -> Optional[Dict[str, Any]]:
        print(f"🔍 PostgreSQL: 查找用户 {username}")
        return {'username': username, 'email': f'{username}@example.com'}


class InMemoryDatabase(DatabaseInterface):
    """内存数据库实现（用于测试）"""
    
    def __init__(self):
        self.users: Dict[str, Dict[str, Any]] = {}
        print("🔗 内存数据库初始化")
    
    def save_user(self, user_data: Dict[str, Any]) -> bool:
        username = user_data['username']
        self.users[username] = user_data
        print(f"💾 内存数据库: 保存用户 {username}")
        return True
    
    def find_user(self, username: str) -> Optional[Dict[str, Any]]:
        user = self.users.get(username)
        print(f"🔍 内存数据库: 查找用户 {username} - {'找到' if user else '未找到'}")
        return user


class SMTPEmailService(EmailServiceInterface):
    """SMTP邮件服务实现"""
    
    def __init__(self, smtp_host: str = "smtp.gmail.com"):
        self.smtp_host = smtp_host
        print(f"📧 SMTP邮件服务初始化: {smtp_host}")
    
    def send_welcome_email(self, email: str) -> bool:
        print(f"📧 SMTP: 发送欢迎邮件到 {email}")
        return True
    
    def send_notification(self, email: str, message: str) -> bool:
        print(f"📧 SMTP: 发送通知到 {email} - {message}")
        return True


class MockEmailService(EmailServiceInterface):
    """模拟邮件服务（用于测试）"""
    
    def __init__(self):
        self.sent_emails: List[Dict[str, str]] = []
        print("📧 模拟邮件服务初始化")
    
    def send_welcome_email(self, email: str) -> bool:
        email_data = {'type': 'welcome', 'to': email}
        self.sent_emails.append(email_data)
        print(f"📧 模拟: 记录欢迎邮件到 {email}")
        return True
    
    def send_notification(self, email: str, message: str) -> bool:
        email_data = {'type': 'notification', 'to': email, 'message': message}
        self.sent_emails.append(email_data)
        print(f"📧 模拟: 记录通知邮件到 {email}")
        return True


class FileLogger(LoggerInterface):
    """文件日志实现"""
    
    def __init__(self, log_file: str = "app.log"):
        self.log_file = log_file
        print(f"📝 文件日志初始化: {log_file}")
    
    def log(self, message: str) -> None:
        print(f"📝 文件日志: {message}")
    
    def error(self, message: str) -> None:
        print(f"📝 文件日志 [ERROR]: {message}")


class ConsoleLogger(LoggerInterface):
    """控制台日志实现"""
    
    def __init__(self):
        print("📝 控制台日志初始化")
    
    def log(self, message: str) -> None:
        print(f"📝 控制台: {message}")
    
    def error(self, message: str) -> None:
        print(f"📝 控制台 [ERROR]: {message}")


# ============================================================================
# 4. 依赖注入版本的用户服务
# ============================================================================

class UserService:
    """依赖注入版本：依赖抽象接口"""
    
    def __init__(self, 
                 database: DatabaseInterface,
                 email_service: EmailServiceInterface,
                 logger: LoggerInterface):
        # 依赖注入：接收接口而非具体实现
        self.database = database
        self.email_service = email_service
        self.logger = logger
    
    def create_user(self, username: str, email: str) -> bool:
        """创建用户"""
        try:
            # 检查用户是否已存在
            existing_user = self.database.find_user(username)
            if existing_user:
                self.logger.error(f"用户 {username} 已存在")
                return False
            
            # 保存用户
            user_data = {'username': username, 'email': email}
            if self.database.save_user(user_data):
                # 发送欢迎邮件
                self.email_service.send_welcome_email(email)
                # 记录日志
                self.logger.log(f"用户 {username} 创建成功")
                return True
            else:
                self.logger.error(f"保存用户 {username} 失败")
                return False
                
        except Exception as e:
            self.logger.error(f"创建用户时发生错误: {str(e)}")
            return False
    
    def notify_user(self, username: str, message: str) -> bool:
        """通知用户"""
        user = self.database.find_user(username)
        if user:
            return self.email_service.send_notification(user['email'], message)
        return False


# ============================================================================
# 5. 简单的依赖注入容器
# ============================================================================

class SimpleDIContainer:
    """简单的依赖注入容器"""
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, callable] = {}
    
    def register_instance(self, service_type: type, instance: Any) -> None:
        """注册服务实例"""
        self._services[service_type.__name__] = instance
    
    def register_factory(self, service_type: type, factory: callable) -> None:
        """注册服务工厂"""
        self._factories[service_type.__name__] = factory
    
    def get(self, service_type: type) -> Any:
        """获取服务"""
        service_name = service_type.__name__
        
        # 先检查已注册的实例
        if service_name in self._services:
            return self._services[service_name]
        
        # 再检查工厂
        if service_name in self._factories:
            instance = self._factories[service_name]()
            self._services[service_name] = instance  # 缓存实例
            return instance
        
        raise ValueError(f"Service {service_name} not registered")


# ============================================================================
# 6. 配置和演示
# ============================================================================

def setup_production_container() -> SimpleDIContainer:
    """配置生产环境容器"""
    container = SimpleDIContainer()
    
    # 注册生产环境服务
    container.register_factory(
        DatabaseInterface, 
        lambda: MySQLDatabase("mysql://prod-server:3306/app")
    )
    container.register_factory(
        EmailServiceInterface,
        lambda: SMTPEmailService("smtp.company.com")
    )
    container.register_factory(
        LoggerInterface,
        lambda: FileLogger("/var/log/app.log")
    )
    
    return container


def setup_test_container() -> SimpleDIContainer:
    """配置测试环境容器"""
    container = SimpleDIContainer()
    
    # 注册测试环境服务
    container.register_factory(
        DatabaseInterface,
        lambda: InMemoryDatabase()
    )
    container.register_factory(
        EmailServiceInterface,
        lambda: MockEmailService()
    )
    container.register_factory(
        LoggerInterface,
        lambda: ConsoleLogger()
    )
    
    return container


def setup_development_container() -> SimpleDIContainer:
    """配置开发环境容器"""
    container = SimpleDIContainer()
    
    # 注册开发环境服务
    container.register_factory(
        DatabaseInterface,
        lambda: PostgreSQLDatabase("localhost", 5432)
    )
    container.register_factory(
        EmailServiceInterface,
        lambda: MockEmailService()  # 开发环境使用模拟邮件
    )
    container.register_factory(
        LoggerInterface,
        lambda: ConsoleLogger()
    )
    
    return container


def demo_dependency_injection():
    """演示依赖注入的优势"""
    print("依赖注入模式演示")
    print("=" * 40)
    
    # 1. 生产环境配置
    print("\n1. 生产环境配置:")
    prod_container = setup_production_container()
    
    prod_user_service = UserService(
        database=prod_container.get(DatabaseInterface),
        email_service=prod_container.get(EmailServiceInterface),
        logger=prod_container.get(LoggerInterface)
    )
    
    print("创建生产环境用户:")
    prod_user_service.create_user("alice", "alice@company.com")
    
    # 2. 测试环境配置
    print("\n2. 测试环境配置:")
    test_container = setup_test_container()
    
    test_user_service = UserService(
        database=test_container.get(DatabaseInterface),
        email_service=test_container.get(EmailServiceInterface),
        logger=test_container.get(LoggerInterface)
    )
    
    print("创建测试环境用户:")
    test_user_service.create_user("bob", "bob@test.com")
    
    # 验证测试环境的模拟邮件服务
    email_service = test_container.get(EmailServiceInterface)
    print(f"测试环境发送的邮件数量: {len(email_service.sent_emails)}")
    
    # 3. 开发环境配置
    print("\n3. 开发环境配置:")
    dev_container = setup_development_container()
    
    dev_user_service = UserService(
        database=dev_container.get(DatabaseInterface),
        email_service=dev_container.get(EmailServiceInterface),
        logger=dev_container.get(LoggerInterface)
    )
    
    print("创建开发环境用户:")
    dev_user_service.create_user("charlie", "charlie@dev.com")
    
    # 4. 展示依赖注入的优势
    print("\n4. 依赖注入的优势:")
    print("✓ 松耦合: 服务不依赖具体实现")
    print("✓ 可测试: 可以注入模拟对象")
    print("✓ 可配置: 不同环境使用不同实现")
    print("✓ 可扩展: 容易添加新的实现")
    
    # 5. 运行时切换实现
    print("\n5. 运行时切换实现演示:")
    
    # 创建一个用户服务，然后动态切换数据库实现
    memory_db = InMemoryDatabase()
    console_logger = ConsoleLogger()
    mock_email = MockEmailService()
    
    flexible_service = UserService(memory_db, mock_email, console_logger)
    
    print("使用内存数据库创建用户:")
    flexible_service.create_user("david", "david@example.com")
    
    # 切换到不同的数据库实现
    print("\n切换到PostgreSQL数据库:")
    postgres_db = PostgreSQLDatabase("localhost", 5432)
    flexible_service.database = postgres_db  # 运行时切换
    
    flexible_service.create_user("eve", "eve@example.com")
    
    print("\n演示完成！")


if __name__ == "__main__":
    demo_dependency_injection()