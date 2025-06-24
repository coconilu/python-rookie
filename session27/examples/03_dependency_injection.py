#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
依赖注入模式详细示例

本文件演示了依赖注入的各种实现方式：
1. 构造函数注入 (Constructor Injection)
2. 属性注入 (Property Injection)
3. 方法注入 (Method Injection)
4. 依赖注入容器 (DI Container)
5. 服务定位器模式 (Service Locator)
6. 装饰器注入 (Decorator Injection)
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Callable, Type, Optional, List
from datetime import datetime
from functools import wraps
import inspect


# ============================================================================
# 基础接口定义
# ============================================================================

class ILogger(ABC):
    """日志记录器接口"""
    @abstractmethod
    def log(self, level: str, message: str):
        pass

class IDatabase(ABC):
    """数据库接口"""
    @abstractmethod
    def connect(self) -> bool:
        pass
    
    @abstractmethod
    def execute(self, query: str) -> List[Dict]:
        pass
    
    @abstractmethod
    def close(self) -> bool:
        pass

class IEmailService(ABC):
    """邮件服务接口"""
    @abstractmethod
    def send_email(self, to: str, subject: str, body: str) -> bool:
        pass

class IConfigService(ABC):
    """配置服务接口"""
    @abstractmethod
    def get_config(self, key: str) -> Any:
        pass
    
    @abstractmethod
    def set_config(self, key: str, value: Any):
        pass


# ============================================================================
# 具体实现类
# ============================================================================

class ConsoleLogger(ILogger):
    """控制台日志记录器"""
    def __init__(self, prefix: str = "[APP]"):
        self.prefix = prefix
    
    def log(self, level: str, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{self.prefix} [{timestamp}] {level.upper()}: {message}")

class FileLogger(ILogger):
    """文件日志记录器"""
    def __init__(self, filename: str):
        self.filename = filename
    
    def log(self, level: str, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"📁 写入文件 {self.filename}: [{timestamp}] {level.upper()}: {message}")

class DatabaseLogger(ILogger):
    """数据库日志记录器"""
    def __init__(self, database: IDatabase):
        self.database = database
    
    def log(self, level: str, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"💾 写入数据库日志: [{timestamp}] {level.upper()}: {message}")

class MySQLDatabase(IDatabase):
    """MySQL数据库实现"""
    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connected = False
    
    def connect(self) -> bool:
        print(f"🔗 连接到MySQL: {self.host}:{self.port}")
        self.connected = True
        return True
    
    def execute(self, query: str) -> List[Dict]:
        if not self.connected:
            raise Exception("数据库未连接")
        print(f"🔍 执行MySQL查询: {query}")
        return [{"id": 1, "result": "MySQL数据"}]
    
    def close(self) -> bool:
        print("❌ 关闭MySQL连接")
        self.connected = False
        return True

class PostgreSQLDatabase(IDatabase):
    """PostgreSQL数据库实现"""
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connected = False
    
    def connect(self) -> bool:
        print(f"🔗 连接到PostgreSQL: {self.connection_string}")
        self.connected = True
        return True
    
    def execute(self, query: str) -> List[Dict]:
        if not self.connected:
            raise Exception("数据库未连接")
        print(f"🔍 执行PostgreSQL查询: {query}")
        return [{"id": 1, "result": "PostgreSQL数据"}]
    
    def close(self) -> bool:
        print("❌ 关闭PostgreSQL连接")
        self.connected = False
        return True

class SMTPEmailService(IEmailService):
    """SMTP邮件服务"""
    def __init__(self, smtp_server: str, port: int, username: str, password: str):
        self.smtp_server = smtp_server
        self.port = port
        self.username = username
        self.password = password
    
    def send_email(self, to: str, subject: str, body: str) -> bool:
        print(f"📧 通过SMTP发送邮件: {subject} -> {to}")
        print(f"   服务器: {self.smtp_server}:{self.port}")
        return True

class SendGridEmailService(IEmailService):
    """SendGrid邮件服务"""
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def send_email(self, to: str, subject: str, body: str) -> bool:
        print(f"📧 通过SendGrid发送邮件: {subject} -> {to}")
        print(f"   API Key: {self.api_key[:10]}...")
        return True

class ConfigService(IConfigService):
    """配置服务实现"""
    def __init__(self):
        self.config = {
            "database_host": "localhost",
            "database_port": 3306,
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "log_level": "INFO",
            "max_connections": 100
        }
    
    def get_config(self, key: str) -> Any:
        return self.config.get(key)
    
    def set_config(self, key: str, value: Any):
        self.config[key] = value


# ============================================================================
# 1. 构造函数注入 (Constructor Injection)
# ============================================================================

print("1. 构造函数注入演示")
print("=" * 40)

class UserService:
    """用户服务 - 使用构造函数注入"""
    def __init__(self, logger: ILogger, database: IDatabase, email_service: IEmailService):
        self.logger = logger
        self.database = database
        self.email_service = email_service
    
    def create_user(self, username: str, email: str) -> Dict[str, Any]:
        """创建用户"""
        self.logger.log("INFO", f"开始创建用户: {username}")
        
        try:
            # 连接数据库
            self.database.connect()
            
            # 检查用户是否存在
            existing_users = self.database.execute(f"SELECT * FROM users WHERE username = '{username}'")
            if existing_users:
                self.logger.log("WARNING", f"用户 {username} 已存在")
                return {"success": False, "message": "用户已存在"}
            
            # 创建用户
            self.database.execute(f"INSERT INTO users (username, email) VALUES ('{username}', '{email}')")
            
            # 发送欢迎邮件
            self.email_service.send_email(
                email,
                "欢迎注册",
                f"欢迎 {username} 加入我们的平台！"
            )
            
            self.logger.log("INFO", f"用户 {username} 创建成功")
            return {"success": True, "message": "用户创建成功"}
            
        except Exception as e:
            self.logger.log("ERROR", f"创建用户失败: {str(e)}")
            return {"success": False, "message": "创建用户失败"}
        
        finally:
            self.database.close()
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """用户认证"""
        self.logger.log("INFO", f"用户认证: {username}")
        
        try:
            self.database.connect()
            users = self.database.execute(f"SELECT * FROM users WHERE username = '{username}'")
            
            if users:
                self.logger.log("INFO", f"用户 {username} 认证成功")
                return True
            else:
                self.logger.log("WARNING", f"用户 {username} 认证失败")
                return False
                
        finally:
            self.database.close()

# 演示构造函数注入
print("🔹 构造函数注入演示:")

# 创建依赖对象
console_logger = ConsoleLogger("[USER_SERVICE]")
mysql_db = MySQLDatabase("localhost", 3306, "admin", "password")
smtp_email = SMTPEmailService("smtp.gmail.com", 587, "user@gmail.com", "password")

# 通过构造函数注入依赖
user_service = UserService(console_logger, mysql_db, smtp_email)

# 使用服务
result = user_service.create_user("alice", "alice@example.com")
print(f"创建结果: {result['message']}")

auth_result = user_service.authenticate_user("alice", "password123")
print(f"认证结果: {'成功' if auth_result else '失败'}")

print()


# ============================================================================
# 2. 属性注入 (Property Injection)
# ============================================================================

print("2. 属性注入演示")
print("=" * 40)

class OrderService:
    """订单服务 - 使用属性注入"""
    def __init__(self):
        self.logger: Optional[ILogger] = None
        self.database: Optional[IDatabase] = None
        self.email_service: Optional[IEmailService] = None
        self.config_service: Optional[IConfigService] = None
    
    def set_logger(self, logger: ILogger):
        """设置日志记录器"""
        self.logger = logger
    
    def set_database(self, database: IDatabase):
        """设置数据库"""
        self.database = database
    
    def set_email_service(self, email_service: IEmailService):
        """设置邮件服务"""
        self.email_service = email_service
    
    def set_config_service(self, config_service: IConfigService):
        """设置配置服务"""
        self.config_service = config_service
    
    def _check_dependencies(self):
        """检查依赖是否已注入"""
        if not self.logger:
            raise Exception("Logger未注入")
        if not self.database:
            raise Exception("Database未注入")
        if not self.email_service:
            raise Exception("EmailService未注入")
        if not self.config_service:
            raise Exception("ConfigService未注入")
    
    def create_order(self, customer_id: int, items: List[Dict]) -> Dict[str, Any]:
        """创建订单"""
        self._check_dependencies()
        
        self.logger.log("INFO", f"开始创建订单: 客户{customer_id}")
        
        try:
            # 获取配置
            max_items = self.config_service.get_config("max_order_items") or 10
            
            if len(items) > max_items:
                self.logger.log("WARNING", f"订单商品数量超过限制: {len(items)} > {max_items}")
                return {"success": False, "message": "订单商品数量超过限制"}
            
            # 连接数据库
            self.database.connect()
            
            # 计算总金额
            total_amount = sum(item.get("price", 0) * item.get("quantity", 1) for item in items)
            
            # 创建订单
            order_data = {
                "customer_id": customer_id,
                "items": items,
                "total_amount": total_amount,
                "status": "pending"
            }
            
            self.database.execute(f"INSERT INTO orders (customer_id, total_amount, status) VALUES ({customer_id}, {total_amount}, 'pending')")
            
            # 发送确认邮件
            customer_email = "customer@example.com"  # 实际应该从数据库获取
            self.email_service.send_email(
                customer_email,
                "订单确认",
                f"您的订单已创建，总金额: ¥{total_amount:.2f}"
            )
            
            self.logger.log("INFO", f"订单创建成功，总金额: ¥{total_amount:.2f}")
            return {"success": True, "message": "订单创建成功", "order": order_data}
            
        except Exception as e:
            self.logger.log("ERROR", f"创建订单失败: {str(e)}")
            return {"success": False, "message": "创建订单失败"}
        
        finally:
            self.database.close()

# 演示属性注入
print("🔹 属性注入演示:")

# 创建服务实例
order_service = OrderService()

# 通过属性注入依赖
order_service.set_logger(FileLogger("orders.log"))
order_service.set_database(PostgreSQLDatabase("postgresql://localhost:5432/shop"))
order_service.set_email_service(SendGridEmailService("sg_api_key_123456"))

config_service = ConfigService()
config_service.set_config("max_order_items", 5)
order_service.set_config_service(config_service)

# 使用服务
items = [
    {"product_id": 1, "name": "笔记本电脑", "price": 5999.0, "quantity": 1},
    {"product_id": 2, "name": "鼠标", "price": 99.0, "quantity": 2}
]

result = order_service.create_order(1, items)
print(f"订单创建结果: {result['message']}")

print()


# ============================================================================
# 3. 方法注入 (Method Injection)
# ============================================================================

print("3. 方法注入演示")
print("=" * 40)

class ReportService:
    """报告服务 - 使用方法注入"""
    def __init__(self):
        pass
    
    def generate_user_report(self, database: IDatabase, logger: ILogger) -> str:
        """生成用户报告 - 通过方法参数注入依赖"""
        logger.log("INFO", "开始生成用户报告")
        
        try:
            database.connect()
            users = database.execute("SELECT COUNT(*) as user_count FROM users")
            user_count = users[0].get("user_count", 0) if users else 0
            
            report = f"用户报告\n" \
                    f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" \
                    f"用户总数: {user_count}\n" \
                    f"报告状态: 成功生成"
            
            logger.log("INFO", "用户报告生成完成")
            return report
            
        except Exception as e:
            logger.log("ERROR", f"生成用户报告失败: {str(e)}")
            return "报告生成失败"
        
        finally:
            database.close()
    
    def generate_sales_report(self, database: IDatabase, logger: ILogger, email_service: IEmailService, recipient: str) -> bool:
        """生成销售报告并发送邮件 - 多个依赖通过方法注入"""
        logger.log("INFO", "开始生成销售报告")
        
        try:
            database.connect()
            sales = database.execute("SELECT SUM(total_amount) as total_sales FROM orders WHERE status = 'completed'")
            total_sales = sales[0].get("total_sales", 0) if sales else 0
            
            report_content = f"销售报告\n" \
                           f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" \
                           f"总销售额: ¥{total_sales:.2f}\n" \
                           f"报告状态: 成功生成"
            
            # 发送报告邮件
            email_sent = email_service.send_email(
                recipient,
                "销售报告",
                report_content
            )
            
            if email_sent:
                logger.log("INFO", f"销售报告已发送给 {recipient}")
                return True
            else:
                logger.log("ERROR", "销售报告发送失败")
                return False
                
        except Exception as e:
            logger.log("ERROR", f"生成销售报告失败: {str(e)}")
            return False
        
        finally:
            database.close()

# 演示方法注入
print("🔹 方法注入演示:")

report_service = ReportService()

# 创建依赖对象
report_logger = ConsoleLogger("[REPORT]")
report_db = MySQLDatabase("localhost", 3306, "admin", "password")
report_email = SMTPEmailService("smtp.company.com", 587, "reports@company.com", "password")

# 通过方法参数注入依赖
user_report = report_service.generate_user_report(report_db, report_logger)
print(f"用户报告:\n{user_report}")

print("\n" + "-"*30)
sales_report_sent = report_service.generate_sales_report(
    report_db, 
    report_logger, 
    report_email, 
    "manager@company.com"
)
print(f"销售报告发送结果: {'成功' if sales_report_sent else '失败'}")

print()


# ============================================================================
# 4. 依赖注入容器 (DI Container)
# ============================================================================

print("4. 依赖注入容器演示")
print("=" * 40)

class DIContainer:
    """依赖注入容器"""
    def __init__(self):
        self._services: Dict[str, Dict] = {}
        self._instances: Dict[str, Any] = {}
    
    def register_singleton(self, interface: str, implementation: Type, *args, **kwargs):
        """注册单例服务"""
        self._services[interface] = {
            'type': 'singleton',
            'implementation': implementation,
            'args': args,
            'kwargs': kwargs
        }
    
    def register_transient(self, interface: str, implementation: Type, *args, **kwargs):
        """注册瞬态服务"""
        self._services[interface] = {
            'type': 'transient',
            'implementation': implementation,
            'args': args,
            'kwargs': kwargs
        }
    
    def register_factory(self, interface: str, factory: Callable):
        """注册工厂方法"""
        self._services[interface] = {
            'type': 'factory',
            'factory': factory
        }
    
    def register_instance(self, interface: str, instance: Any):
        """注册实例"""
        self._instances[interface] = instance
    
    def resolve(self, interface: str) -> Any:
        """解析服务"""
        # 检查是否有已注册的实例
        if interface in self._instances:
            return self._instances[interface]
        
        # 检查是否有注册的服务
        if interface not in self._services:
            raise ValueError(f"服务 '{interface}' 未注册")
        
        service_info = self._services[interface]
        
        if service_info['type'] == 'singleton':
            # 单例模式：如果已创建则返回现有实例
            if interface not in self._instances:
                self._instances[interface] = self._create_instance(service_info)
            return self._instances[interface]
        
        elif service_info['type'] == 'transient':
            # 瞬态模式：每次都创建新实例
            return self._create_instance(service_info)
        
        elif service_info['type'] == 'factory':
            # 工厂模式：使用工厂方法创建
            return service_info['factory']()
    
    def _create_instance(self, service_info: Dict) -> Any:
        """创建服务实例"""
        implementation = service_info['implementation']
        args = service_info.get('args', ())
        kwargs = service_info.get('kwargs', {})
        
        # 解析构造函数参数中的依赖
        resolved_args = []
        for arg in args:
            if isinstance(arg, str) and arg.startswith('@'):
                # 以@开头的字符串表示需要从容器解析的依赖
                dependency_name = arg[1:]
                resolved_args.append(self.resolve(dependency_name))
            else:
                resolved_args.append(arg)
        
        resolved_kwargs = {}
        for key, value in kwargs.items():
            if isinstance(value, str) and value.startswith('@'):
                dependency_name = value[1:]
                resolved_kwargs[key] = self.resolve(dependency_name)
            else:
                resolved_kwargs[key] = value
        
        return implementation(*resolved_args, **resolved_kwargs)
    
    def resolve_with_dependencies(self, interface: str, **additional_kwargs) -> Any:
        """解析服务并注入额外的依赖"""
        instance = self.resolve(interface)
        
        # 如果有额外的依赖需要注入
        for key, value in additional_kwargs.items():
            if hasattr(instance, f'set_{key}'):
                getattr(instance, f'set_{key}')(value)
        
        return instance

class NotificationService:
    """通知服务 - 演示容器注入"""
    def __init__(self, logger: ILogger, email_service: IEmailService, config_service: IConfigService):
        self.logger = logger
        self.email_service = email_service
        self.config_service = config_service
    
    def send_notification(self, user_id: int, message: str, notification_type: str = "info") -> bool:
        """发送通知"""
        self.logger.log("INFO", f"发送通知给用户 {user_id}: {message}")
        
        try:
            # 获取用户邮箱（模拟）
            user_email = f"user{user_id}@example.com"
            
            # 根据通知类型设置邮件主题
            subject_prefix = self.config_service.get_config("email_subject_prefix") or "[通知]"
            subject = f"{subject_prefix} {notification_type.upper()}"
            
            # 发送邮件
            success = self.email_service.send_email(user_email, subject, message)
            
            if success:
                self.logger.log("INFO", f"通知发送成功: {user_id}")
            else:
                self.logger.log("ERROR", f"通知发送失败: {user_id}")
            
            return success
            
        except Exception as e:
            self.logger.log("ERROR", f"发送通知异常: {str(e)}")
            return False

# 演示依赖注入容器
print("🔹 依赖注入容器演示:")

# 创建容器
container = DIContainer()

# 注册基础服务
container.register_singleton("logger", ConsoleLogger, "[CONTAINER]")
container.register_singleton("config", ConfigService)
container.register_transient("mysql_db", MySQLDatabase, "localhost", 3306, "admin", "password")
container.register_transient("email_service", SMTPEmailService, "smtp.gmail.com", 587, "app@gmail.com", "password")

# 注册复合服务（依赖其他服务）
container.register_singleton("notification_service", NotificationService, "@logger", "@email_service", "@config")

# 使用工厂方法注册复杂服务
def create_user_service_factory():
    logger = container.resolve("logger")
    database = container.resolve("mysql_db")
    email_service = container.resolve("email_service")
    return UserService(logger, database, email_service)

container.register_factory("user_service_factory", create_user_service_factory)

# 解析和使用服务
notification_service = container.resolve("notification_service")
notification_service.send_notification(123, "您有新的消息", "info")

print("\n验证单例模式:")
logger1 = container.resolve("logger")
logger2 = container.resolve("logger")
print(f"两个logger实例是否相同: {logger1 is logger2}")

print("\n验证瞬态模式:")
db1 = container.resolve("mysql_db")
db2 = container.resolve("mysql_db")
print(f"两个数据库实例是否相同: {db1 is db2}")

print("\n使用工厂方法:")
user_service_from_factory = container.resolve("user_service_factory")
user_service_from_factory.create_user("bob", "bob@example.com")

print()


# ============================================================================
# 5. 服务定位器模式 (Service Locator)
# ============================================================================

print("5. 服务定位器模式演示")
print("=" * 40)

class ServiceLocator:
    """服务定位器"""
    _instance = None
    _services: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def register_service(cls, name: str, service: Any):
        """注册服务"""
        cls._services[name] = service
    
    @classmethod
    def get_service(cls, name: str) -> Any:
        """获取服务"""
        if name not in cls._services:
            raise ValueError(f"服务 '{name}' 未注册")
        return cls._services[name]
    
    @classmethod
    def has_service(cls, name: str) -> bool:
        """检查服务是否存在"""
        return name in cls._services
    
    @classmethod
    def clear_services(cls):
        """清空所有服务"""
        cls._services.clear()

class PaymentService:
    """支付服务 - 使用服务定位器"""
    def __init__(self):
        pass
    
    def process_payment(self, amount: float, payment_method: str) -> Dict[str, Any]:
        """处理支付"""
        # 从服务定位器获取依赖
        logger = ServiceLocator.get_service("logger")
        database = ServiceLocator.get_service("database")
        email_service = ServiceLocator.get_service("email_service")
        
        logger.log("INFO", f"开始处理支付: ¥{amount:.2f}, 方式: {payment_method}")
        
        try:
            # 验证支付方式
            valid_methods = ["credit_card", "alipay", "wechat_pay"]
            if payment_method not in valid_methods:
                logger.log("ERROR", f"不支持的支付方式: {payment_method}")
                return {"success": False, "message": "不支持的支付方式"}
            
            # 模拟支付处理
            database.connect()
            
            # 创建支付记录
            payment_id = f"PAY_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            database.execute(f"INSERT INTO payments (id, amount, method, status) VALUES ('{payment_id}', {amount}, '{payment_method}', 'completed')")
            
            # 发送支付确认邮件
            email_service.send_email(
                "customer@example.com",
                "支付确认",
                f"您的支付已成功处理\n支付ID: {payment_id}\n金额: ¥{amount:.2f}\n方式: {payment_method}"
            )
            
            logger.log("INFO", f"支付处理成功: {payment_id}")
            return {
                "success": True,
                "message": "支付成功",
                "payment_id": payment_id,
                "amount": amount
            }
            
        except Exception as e:
            logger.log("ERROR", f"支付处理失败: {str(e)}")
            return {"success": False, "message": "支付处理失败"}
        
        finally:
            database.close()

# 演示服务定位器模式
print("🔹 服务定位器模式演示:")

# 注册服务到服务定位器
ServiceLocator.register_service("logger", ConsoleLogger("[PAYMENT]"))
ServiceLocator.register_service("database", PostgreSQLDatabase("postgresql://localhost:5432/payments"))
ServiceLocator.register_service("email_service", SendGridEmailService("sg_payment_api_key"))

# 创建和使用支付服务
payment_service = PaymentService()

# 处理支付
result = payment_service.process_payment(299.99, "alipay")
print(f"支付结果: {result['message']}")
if result["success"]:
    print(f"支付ID: {result['payment_id']}")

print()


# ============================================================================
# 6. 装饰器注入 (Decorator Injection)
# ============================================================================

print("6. 装饰器注入演示")
print("=" * 40)

# 全局依赖注册表
_dependency_registry: Dict[str, Any] = {}

def register_dependency(name: str, instance: Any):
    """注册依赖"""
    _dependency_registry[name] = instance

def inject(**dependencies):
    """依赖注入装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 解析依赖
            injected_kwargs = {}
            for param_name, dependency_name in dependencies.items():
                if dependency_name in _dependency_registry:
                    injected_kwargs[param_name] = _dependency_registry[dependency_name]
                else:
                    raise ValueError(f"依赖 '{dependency_name}' 未注册")
            
            # 合并注入的依赖和原有参数
            merged_kwargs = {**injected_kwargs, **kwargs}
            return func(*args, **merged_kwargs)
        return wrapper
    return decorator

def auto_inject(func):
    """自动依赖注入装饰器 - 根据参数名自动注入"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 获取函数签名
        sig = inspect.signature(func)
        
        # 自动注入依赖
        for param_name, param in sig.parameters.items():
            if param_name not in kwargs and param_name in _dependency_registry:
                kwargs[param_name] = _dependency_registry[param_name]
        
        return func(*args, **kwargs)
    return wrapper

class InventoryService:
    """库存服务 - 使用装饰器注入"""
    
    @inject(logger="inventory_logger", database="inventory_db")
    def update_stock(self, product_id: int, quantity: int, logger: ILogger, database: IDatabase) -> bool:
        """更新库存 - 使用装饰器注入依赖"""
        logger.log("INFO", f"更新库存: 产品{product_id}, 数量{quantity}")
        
        try:
            database.connect()
            
            # 检查当前库存
            current_stock = database.execute(f"SELECT stock FROM products WHERE id = {product_id}")
            if not current_stock:
                logger.log("ERROR", f"产品 {product_id} 不存在")
                return False
            
            # 更新库存
            database.execute(f"UPDATE products SET stock = stock + {quantity} WHERE id = {product_id}")
            
            logger.log("INFO", f"库存更新成功: 产品{product_id}")
            return True
            
        except Exception as e:
            logger.log("ERROR", f"更新库存失败: {str(e)}")
            return False
        
        finally:
            database.close()
    
    @auto_inject
    def check_low_stock(self, threshold: int = 10, logger: ILogger = None, database: IDatabase = None) -> List[Dict]:
        """检查低库存产品 - 使用自动注入"""
        if logger:
            logger.log("INFO", f"检查低库存产品，阈值: {threshold}")
        
        try:
            if database:
                database.connect()
                low_stock_products = database.execute(f"SELECT id, name, stock FROM products WHERE stock < {threshold}")
                
                if logger:
                    logger.log("INFO", f"发现 {len(low_stock_products)} 个低库存产品")
                
                return low_stock_products
            else:
                return []
                
        except Exception as e:
            if logger:
                logger.log("ERROR", f"检查低库存失败: {str(e)}")
            return []
        
        finally:
            if database:
                database.close()

# 演示装饰器注入
print("🔹 装饰器注入演示:")

# 注册依赖
register_dependency("inventory_logger", ConsoleLogger("[INVENTORY]"))
register_dependency("inventory_db", MySQLDatabase("localhost", 3306, "inventory_user", "password"))
register_dependency("logger", ConsoleLogger("[AUTO_INJECT]"))
register_dependency("database", PostgreSQLDatabase("postgresql://localhost:5432/inventory"))

# 创建和使用库存服务
inventory_service = InventoryService()

# 使用装饰器注入
update_result = inventory_service.update_stock(1, 50)
print(f"库存更新结果: {'成功' if update_result else '失败'}")

print("\n" + "-"*30)
# 使用自动注入
low_stock_products = inventory_service.check_low_stock(5)
print(f"低库存产品数量: {len(low_stock_products)}")

print()


# ============================================================================
# 总结和对比
# ============================================================================

print("依赖注入模式总结")
print("=" * 50)

print("✅ 依赖注入的优点:")
print("  1. 降低耦合度 - 组件不直接依赖具体实现")
print("  2. 提高可测试性 - 容易进行单元测试")
print("  3. 增强灵活性 - 可以轻松替换实现")
print("  4. 支持配置化 - 通过配置文件管理依赖")
print("  5. 遵循SOLID原则 - 特别是依赖倒置原则")

print("\n📊 不同注入方式对比:")
print("  构造函数注入: 强制依赖，保证对象完整性")
print("  属性注入: 可选依赖，灵活但可能遗漏")
print("  方法注入: 临时依赖，适合特定操作")
print("  容器注入: 集中管理，支持复杂依赖关系")
print("  服务定位器: 全局访问，但增加了耦合")
print("  装饰器注入: 声明式，代码简洁")

print("\n🎯 最佳实践:")
print("  1. 优先使用构造函数注入")
print("  2. 依赖接口而非具体类")
print("  3. 避免循环依赖")
print("  4. 使用容器管理复杂依赖")
print("  5. 保持依赖关系清晰")