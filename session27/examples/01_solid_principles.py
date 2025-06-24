#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SOLID设计原则详细示例

本文件详细演示了SOLID设计原则的应用：
1. 单一职责原则 (Single Responsibility Principle)
2. 开闭原则 (Open/Closed Principle)
3. 里氏替换原则 (Liskov Substitution Principle)
4. 接口隔离原则 (Interface Segregation Principle)
5. 依赖倒置原则 (Dependency Inversion Principle)
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime
import json


# ============================================================================
# 1. 单一职责原则 (SRP) - Single Responsibility Principle
# ============================================================================

print("1. 单一职责原则 (SRP) 演示")
print("=" * 40)

# ❌ 违反SRP的设计
class BadUser:
    """违反SRP的用户类 - 承担了太多职责"""
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email
    
    def validate_email(self) -> bool:
        """验证邮箱 - 验证职责"""
        return "@" in self.email
    
    def save_to_database(self):
        """保存到数据库 - 数据访问职责"""
        print(f"保存用户 {self.username} 到数据库")
    
    def send_welcome_email(self):
        """发送欢迎邮件 - 通知职责"""
        print(f"发送欢迎邮件给 {self.email}")
    
    def generate_report(self) -> str:
        """生成报告 - 报告职责"""
        return f"用户报告: {self.username}"

# ✅ 遵循SRP的设计
class User:
    """用户实体 - 只负责用户数据"""
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email
        self.created_at = datetime.now()
    
    def __str__(self):
        return f"User(username={self.username}, email={self.email})"

class UserValidator:
    """用户验证器 - 只负责验证逻辑"""
    @staticmethod
    def validate_email(email: str) -> bool:
        """验证邮箱格式"""
        return "@" in email and "." in email.split("@")[1]
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """验证用户名"""
        return len(username) >= 3 and username.replace("_", "").isalnum()

class UserRepository:
    """用户仓储 - 只负责数据访问"""
    def __init__(self):
        self.users: List[User] = []
    
    def save(self, user: User) -> bool:
        """保存用户"""
        self.users.append(user)
        print(f"✅ 用户 {user.username} 已保存到数据库")
        return True
    
    def find_by_username(self, username: str) -> Optional[User]:
        """根据用户名查找用户"""
        return next((u for u in self.users if u.username == username), None)

class EmailService:
    """邮件服务 - 只负责邮件发送"""
    @staticmethod
    def send_welcome_email(user: User) -> bool:
        """发送欢迎邮件"""
        print(f"📧 发送欢迎邮件给 {user.email}")
        return True

class UserReportGenerator:
    """用户报告生成器 - 只负责报告生成"""
    @staticmethod
    def generate_user_report(user: User) -> str:
        """生成用户报告"""
        return f"用户报告:\n  用户名: {user.username}\n  邮箱: {user.email}\n  创建时间: {user.created_at}"

# 演示SRP
print("🔹 使用遵循SRP的设计:")
user = User("alice", "alice@example.com")
validator = UserValidator()
repository = UserRepository()
email_service = EmailService()
report_generator = UserReportGenerator()

if validator.validate_email(user.email) and validator.validate_username(user.username):
    repository.save(user)
    email_service.send_welcome_email(user)
    report = report_generator.generate_user_report(user)
    print(f"📊 {report}")
else:
    print("❌ 用户数据验证失败")

print()


# ============================================================================
# 2. 开闭原则 (OCP) - Open/Closed Principle
# ============================================================================

print("2. 开闭原则 (OCP) 演示")
print("=" * 40)

# ❌ 违反OCP的设计
class BadDiscountCalculator:
    """违反OCP的折扣计算器 - 每次添加新折扣类型都需要修改"""
    def calculate_discount(self, customer_type: str, amount: float) -> float:
        if customer_type == "regular":
            return amount * 0.05
        elif customer_type == "premium":
            return amount * 0.10
        elif customer_type == "vip":
            return amount * 0.15
        # 如果要添加新的客户类型，就需要修改这个方法
        return 0

# ✅ 遵循OCP的设计
class DiscountStrategy(ABC):
    """折扣策略抽象基类"""
    @abstractmethod
    def calculate_discount(self, amount: float) -> float:
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        pass

class RegularCustomerDiscount(DiscountStrategy):
    """普通客户折扣"""
    def calculate_discount(self, amount: float) -> float:
        return amount * 0.05
    
    def get_description(self) -> str:
        return "普通客户5%折扣"

class PremiumCustomerDiscount(DiscountStrategy):
    """高级客户折扣"""
    def calculate_discount(self, amount: float) -> float:
        return amount * 0.10
    
    def get_description(self) -> str:
        return "高级客户10%折扣"

class VIPCustomerDiscount(DiscountStrategy):
    """VIP客户折扣"""
    def calculate_discount(self, amount: float) -> float:
        return amount * 0.15
    
    def get_description(self) -> str:
        return "VIP客户15%折扣"

# 新增折扣类型 - 无需修改现有代码
class StudentDiscount(DiscountStrategy):
    """学生折扣"""
    def calculate_discount(self, amount: float) -> float:
        return amount * 0.20
    
    def get_description(self) -> str:
        return "学生20%折扣"

class SeasonalDiscount(DiscountStrategy):
    """季节性折扣"""
    def __init__(self, discount_rate: float):
        self.discount_rate = discount_rate
    
    def calculate_discount(self, amount: float) -> float:
        return amount * self.discount_rate
    
    def get_description(self) -> str:
        return f"季节性{self.discount_rate*100:.0f}%折扣"

class DiscountCalculator:
    """折扣计算器 - 对扩展开放，对修改关闭"""
    def __init__(self):
        self.strategies: List[DiscountStrategy] = []
    
    def add_strategy(self, strategy: DiscountStrategy):
        """添加折扣策略"""
        self.strategies.append(strategy)
    
    def calculate_best_discount(self, amount: float) -> Dict:
        """计算最优折扣"""
        if not self.strategies:
            return {"discount": 0, "final_amount": amount, "strategy": "无折扣"}
        
        best_discount = 0
        best_strategy = None
        
        for strategy in self.strategies:
            discount = strategy.calculate_discount(amount)
            if discount > best_discount:
                best_discount = discount
                best_strategy = strategy
        
        return {
            "discount": best_discount,
            "final_amount": amount - best_discount,
            "strategy": best_strategy.get_description() if best_strategy else "无折扣"
        }

# 演示OCP
print("🔹 使用遵循OCP的设计:")
calculator = DiscountCalculator()

# 添加各种折扣策略
calculator.add_strategy(RegularCustomerDiscount())
calculator.add_strategy(PremiumCustomerDiscount())
calculator.add_strategy(VIPCustomerDiscount())
calculator.add_strategy(StudentDiscount())
calculator.add_strategy(SeasonalDiscount(0.25))  # 25%季节性折扣

amount = 1000
result = calculator.calculate_best_discount(amount)
print(f"原价: {amount}元")
print(f"最优策略: {result['strategy']}")
print(f"折扣金额: {result['discount']:.2f}元")
print(f"最终价格: {result['final_amount']:.2f}元")

print()


# ============================================================================
# 3. 里氏替换原则 (LSP) - Liskov Substitution Principle
# ============================================================================

print("3. 里氏替换原则 (LSP) 演示")
print("=" * 40)

# ❌ 违反LSP的设计
class BadBird:
    """违反LSP的鸟类设计"""
    def fly(self):
        print("鸟在飞翔")

class BadPenguin(BadBird):
    """企鹅 - 违反LSP，因为企鹅不能飞"""
    def fly(self):
        raise Exception("企鹅不能飞！")  # 违反了父类的行为契约

# ✅ 遵循LSP的设计
class Bird(ABC):
    """鸟类抽象基类"""
    @abstractmethod
    def move(self) -> str:
        pass
    
    @abstractmethod
    def make_sound(self) -> str:
        pass

class FlyingBird(Bird):
    """会飞的鸟类"""
    @abstractmethod
    def fly(self) -> str:
        pass
    
    def move(self) -> str:
        return self.fly()

class SwimmingBird(Bird):
    """会游泳的鸟类"""
    @abstractmethod
    def swim(self) -> str:
        pass
    
    def move(self) -> str:
        return self.swim()

class Eagle(FlyingBird):
    """老鹰"""
    def fly(self) -> str:
        return "🦅 老鹰在高空翱翔"
    
    def make_sound(self) -> str:
        return "老鹰发出尖锐的叫声"

class Sparrow(FlyingBird):
    """麻雀"""
    def fly(self) -> str:
        return "🐦 麻雀在树间飞舞"
    
    def make_sound(self) -> str:
        return "麻雀发出叽叽喳喳的声音"

class Penguin(SwimmingBird):
    """企鹅"""
    def swim(self) -> str:
        return "🐧 企鹅在水中游泳"
    
    def make_sound(self) -> str:
        return "企鹅发出嘎嘎的声音"

class BirdWatcher:
    """观鸟者 - 可以观察任何鸟类"""
    def observe_bird(self, bird: Bird):
        """观察鸟类 - 可以接受任何Bird子类"""
        print(f"观察到: {bird.move()}")
        print(f"听到: {bird.make_sound()}")

# 演示LSP
print("🔹 使用遵循LSP的设计:")
watcher = BirdWatcher()

birds = [Eagle(), Sparrow(), Penguin()]

for bird in birds:
    watcher.observe_bird(bird)
    print()


# ============================================================================
# 4. 接口隔离原则 (ISP) - Interface Segregation Principle
# ============================================================================

print("4. 接口隔离原则 (ISP) 演示")
print("=" * 40)

# ❌ 违反ISP的设计
class BadMultiFunction(ABC):
    """违反ISP的多功能设备接口 - 接口过于庞大"""
    @abstractmethod
    def print_document(self, document: str):
        pass
    
    @abstractmethod
    def scan_document(self) -> str:
        pass
    
    @abstractmethod
    def fax_document(self, document: str, number: str):
        pass
    
    @abstractmethod
    def copy_document(self, document: str) -> str:
        pass

class BadPrinter(BadMultiFunction):
    """简单打印机 - 被迫实现不需要的方法"""
    def print_document(self, document: str):
        print(f"打印: {document}")
    
    def scan_document(self) -> str:
        raise NotImplementedError("打印机不支持扫描")
    
    def fax_document(self, document: str, number: str):
        raise NotImplementedError("打印机不支持传真")
    
    def copy_document(self, document: str) -> str:
        raise NotImplementedError("打印机不支持复印")

# ✅ 遵循ISP的设计
class Printable(ABC):
    """可打印接口"""
    @abstractmethod
    def print_document(self, document: str) -> bool:
        pass

class Scannable(ABC):
    """可扫描接口"""
    @abstractmethod
    def scan_document(self) -> str:
        pass

class Faxable(ABC):
    """可传真接口"""
    @abstractmethod
    def fax_document(self, document: str, number: str) -> bool:
        pass

class Copyable(ABC):
    """可复印接口"""
    @abstractmethod
    def copy_document(self, document: str) -> str:
        pass

class SimplePrinter(Printable):
    """简单打印机 - 只实现需要的接口"""
    def print_document(self, document: str) -> bool:
        print(f"🖨️  简单打印机打印: {document}")
        return True

class Scanner(Scannable):
    """扫描仪"""
    def scan_document(self) -> str:
        scanned_content = "扫描的文档内容"
        print(f"📄 扫描仪扫描完成: {scanned_content}")
        return scanned_content

class MultiFunctionPrinter(Printable, Scannable, Copyable):
    """多功能打印机 - 实现多个接口"""
    def print_document(self, document: str) -> bool:
        print(f"🖨️  多功能打印机打印: {document}")
        return True
    
    def scan_document(self) -> str:
        scanned_content = "多功能机扫描的内容"
        print(f"📄 多功能打印机扫描: {scanned_content}")
        return scanned_content
    
    def copy_document(self, document: str) -> str:
        copied_content = f"复印件: {document}"
        print(f"📋 多功能打印机复印: {copied_content}")
        return copied_content

class FaxMachine(Faxable):
    """传真机"""
    def fax_document(self, document: str, number: str) -> bool:
        print(f"📠 传真机发送 '{document}' 到 {number}")
        return True

# 演示ISP
print("🔹 使用遵循ISP的设计:")

# 不同设备只实现需要的接口
simple_printer = SimplePrinter()
scanner = Scanner()
multi_printer = MultiFunctionPrinter()
fax_machine = FaxMachine()

document = "重要文档"

# 使用各种设备
simple_printer.print_document(document)
scanner.scan_document()
multi_printer.print_document(document)
multi_printer.scan_document()
multi_printer.copy_document(document)
fax_machine.fax_document(document, "123-456-7890")

print()


# ============================================================================
# 5. 依赖倒置原则 (DIP) - Dependency Inversion Principle
# ============================================================================

print("5. 依赖倒置原则 (DIP) 演示")
print("=" * 40)

# ❌ 违反DIP的设计
class BadMySQLDatabase:
    """MySQL数据库 - 具体实现"""
    def connect(self):
        print("连接到MySQL数据库")
    
    def query(self, sql: str) -> List[Dict]:
        print(f"执行MySQL查询: {sql}")
        return [{"id": 1, "name": "数据"}]

class BadUserService:
    """违反DIP的用户服务 - 直接依赖具体实现"""
    def __init__(self):
        self.database = BadMySQLDatabase()  # 直接依赖具体类
    
    def get_user(self, user_id: int):
        self.database.connect()
        return self.database.query(f"SELECT * FROM users WHERE id = {user_id}")

# ✅ 遵循DIP的设计
class DatabaseInterface(ABC):
    """数据库接口 - 抽象"""
    @abstractmethod
    def connect(self) -> bool:
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        pass
    
    @abstractmethod
    def execute_query(self, query: str) -> List[Dict]:
        pass
    
    @abstractmethod
    def execute_command(self, command: str) -> bool:
        pass

class LoggerInterface(ABC):
    """日志接口"""
    @abstractmethod
    def log(self, level: str, message: str):
        pass

class MySQLDatabase(DatabaseInterface):
    """MySQL数据库实现"""
    def __init__(self):
        self.connected = False
    
    def connect(self) -> bool:
        print("🔗 连接到MySQL数据库")
        self.connected = True
        return True
    
    def disconnect(self) -> bool:
        print("❌ 断开MySQL数据库连接")
        self.connected = False
        return True
    
    def execute_query(self, query: str) -> List[Dict]:
        if not self.connected:
            raise Exception("数据库未连接")
        print(f"🔍 执行MySQL查询: {query}")
        return [{"id": 1, "name": "MySQL数据", "type": "mysql"}]
    
    def execute_command(self, command: str) -> bool:
        if not self.connected:
            raise Exception("数据库未连接")
        print(f"⚡ 执行MySQL命令: {command}")
        return True

class PostgreSQLDatabase(DatabaseInterface):
    """PostgreSQL数据库实现"""
    def __init__(self):
        self.connected = False
    
    def connect(self) -> bool:
        print("🔗 连接到PostgreSQL数据库")
        self.connected = True
        return True
    
    def disconnect(self) -> bool:
        print("❌ 断开PostgreSQL数据库连接")
        self.connected = False
        return True
    
    def execute_query(self, query: str) -> List[Dict]:
        if not self.connected:
            raise Exception("数据库未连接")
        print(f"🔍 执行PostgreSQL查询: {query}")
        return [{"id": 1, "name": "PostgreSQL数据", "type": "postgresql"}]
    
    def execute_command(self, command: str) -> bool:
        if not self.connected:
            raise Exception("数据库未连接")
        print(f"⚡ 执行PostgreSQL命令: {command}")
        return True

class ConsoleLogger(LoggerInterface):
    """控制台日志实现"""
    def log(self, level: str, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"📝 [{timestamp}] {level.upper()}: {message}")

class FileLogger(LoggerInterface):
    """文件日志实现"""
    def __init__(self, filename: str):
        self.filename = filename
    
    def log(self, level: str, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"📁 写入文件 {self.filename}: [{timestamp}] {level.upper()}: {message}")

class UserService:
    """遵循DIP的用户服务 - 依赖抽象接口"""
    def __init__(self, database: DatabaseInterface, logger: LoggerInterface):
        self.database = database  # 依赖抽象接口
        self.logger = logger      # 依赖抽象接口
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """获取用户信息"""
        try:
            self.logger.log("INFO", f"开始获取用户 {user_id} 的信息")
            
            self.database.connect()
            result = self.database.execute_query(f"SELECT * FROM users WHERE id = {user_id}")
            self.database.disconnect()
            
            if result:
                self.logger.log("INFO", f"成功获取用户 {user_id} 的信息")
                return result[0]
            else:
                self.logger.log("WARNING", f"用户 {user_id} 不存在")
                return None
                
        except Exception as e:
            self.logger.log("ERROR", f"获取用户信息失败: {str(e)}")
            return None
    
    def create_user(self, user_data: Dict) -> bool:
        """创建用户"""
        try:
            self.logger.log("INFO", f"开始创建用户: {user_data.get('name', 'Unknown')}")
            
            self.database.connect()
            success = self.database.execute_command(
                f"INSERT INTO users (name, email) VALUES ('{user_data['name']}', '{user_data['email']}')"
            )
            self.database.disconnect()
            
            if success:
                self.logger.log("INFO", "用户创建成功")
            else:
                self.logger.log("ERROR", "用户创建失败")
            
            return success
            
        except Exception as e:
            self.logger.log("ERROR", f"创建用户失败: {str(e)}")
            return False

# 演示DIP
print("🔹 使用遵循DIP的设计:")

# 可以轻松切换不同的数据库和日志实现
print("使用MySQL数据库 + 控制台日志:")
mysql_service = UserService(MySQLDatabase(), ConsoleLogger())
mysql_service.get_user(1)
mysql_service.create_user({"name": "Alice", "email": "alice@example.com"})

print("\n使用PostgreSQL数据库 + 文件日志:")
postgresql_service = UserService(PostgreSQLDatabase(), FileLogger("app.log"))
postgresql_service.get_user(2)
postgresql_service.create_user({"name": "Bob", "email": "bob@example.com"})

print("\n✅ SOLID原则演示完成！")
print("\n总结:")
print("- SRP: 每个类只有一个职责")
print("- OCP: 对扩展开放，对修改关闭")
print("- LSP: 子类可以替换父类")
print("- ISP: 接口应该小而专一")
print("- DIP: 依赖抽象而非具体实现")