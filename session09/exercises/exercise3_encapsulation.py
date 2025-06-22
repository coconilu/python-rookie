#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session09 练习3: 封装和设计模式练习

练习目标：
1. 掌握封装的概念和实现
2. 理解访问控制的重要性
3. 熟练使用属性装饰器
4. 实现常见的设计模式

作者: Python教程团队
创建日期: 2024-01-09
"""

import re
import hashlib
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from enum import Enum

# ============================================================================
# 练习1: 用户账户系统 - 封装和访问控制
# ============================================================================

class UserRole(Enum):
    """用户角色枚举"""
    GUEST = "guest"
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class User:
    """用户类
    
    TODO: 实现用户类，包含以下功能：
    1. 用户信息的封装（用户名、邮箱、密码等）
    2. 密码的安全存储（哈希）
    3. 用户权限管理
    4. 登录状态管理
    5. 属性验证和保护
    """
    
    def __init__(self, username: str, email: str, password: str, role: UserRole = UserRole.USER):
        # TODO: 初始化用户属性
        # 公开属性
        # self.username = username
        # self.created_at = datetime.now()
        
        # 受保护属性
        # self._email = None
        # self._role = role
        # self._is_active = True
        # self._login_attempts = 0
        
        # 私有属性
        # self.__password_hash = None
        # self.__last_login = None
        # self.__is_logged_in = False
        # self.__session_token = None
        
        # 使用setter进行验证
        # self.email = email
        # self.password = password
        pass
    
    @property
    def email(self):
        """邮箱getter"""
        # TODO: 返回邮箱
        pass
    
    @email.setter
    def email(self, value: str):
        """邮箱setter - 带格式验证"""
        # TODO: 验证邮箱格式并设置
        # 使用正则表达式验证邮箱格式
        pass
    
    @property
    def password(self):
        """密码getter - 不允许直接获取"""
        # TODO: 抛出异常，不允许直接获取密码
        pass
    
    @password.setter
    def password(self, value: str):
        """密码setter - 哈希存储"""
        # TODO: 验证密码强度并哈希存储
        # 密码要求：至少8位，包含大小写字母和数字
        pass
    
    @property
    def role(self):
        """角色getter"""
        # TODO: 返回用户角色
        pass
    
    @role.setter
    def role(self, value: UserRole):
        """角色setter - 需要管理员权限"""
        # TODO: 设置用户角色（需要权限检查）
        pass
    
    @property
    def is_logged_in(self):
        """登录状态getter"""
        # TODO: 返回登录状态
        pass
    
    @property
    def last_login(self):
        """最后登录时间getter"""
        # TODO: 返回最后登录时间
        pass
    
    def _hash_password(self, password: str) -> str:
        """哈希密码 - 受保护方法"""
        # TODO: 使用SHA-256哈希密码
        pass
    
    def _validate_password_strength(self, password: str) -> bool:
        """验证密码强度 - 受保护方法"""
        # TODO: 验证密码强度
        # 至少8位，包含大小写字母、数字
        pass
    
    def __generate_session_token(self) -> str:
        """生成会话令牌 - 私有方法"""
        # TODO: 生成随机会话令牌
        pass
    
    def __verify_password(self, password: str) -> bool:
        """验证密码 - 私有方法"""
        # TODO: 验证输入密码是否正确
        pass
    
    def login(self, password: str) -> bool:
        """用户登录"""
        # TODO: 实现登录逻辑
        # 1. 检查账户是否激活
        # 2. 验证密码
        # 3. 检查登录尝试次数
        # 4. 更新登录状态和时间
        # 5. 生成会话令牌
        pass
    
    def logout(self):
        """用户登出"""
        # TODO: 实现登出逻辑
        pass
    
    def change_password(self, old_password: str, new_password: str) -> bool:
        """修改密码"""
        # TODO: 实现密码修改逻辑
        pass
    
    def deactivate_account(self):
        """停用账户"""
        # TODO: 停用用户账户
        pass
    
    def get_user_info(self) -> dict:
        """获取用户信息（安全的）"""
        # TODO: 返回安全的用户信息（不包含敏感数据）
        pass
    
    def has_permission(self, required_role: UserRole) -> bool:
        """检查用户权限"""
        # TODO: 检查用户是否有指定权限
        # 权限等级：GUEST < USER < ADMIN < SUPER_ADMIN
        pass
    
    def __str__(self):
        # TODO: 返回用户的字符串表示
        pass


# ============================================================================
# 练习2: 购物车系统 - 组合和封装
# ============================================================================

class Product:
    """商品类
    
    TODO: 实现商品类，包含商品信息的封装
    """
    
    def __init__(self, product_id: str, name: str, price: float, stock: int, category: str):
        # TODO: 初始化商品属性
        pass
    
    @property
    def price(self):
        """价格getter"""
        # TODO: 返回价格
        pass
    
    @price.setter
    def price(self, value: float):
        """价格setter - 带验证"""
        # TODO: 验证价格并设置
        pass
    
    @property
    def stock(self):
        """库存getter"""
        # TODO: 返回库存
        pass
    
    @stock.setter
    def stock(self, value: int):
        """库存setter - 带验证"""
        # TODO: 验证库存并设置
        pass
    
    def is_available(self, quantity: int = 1) -> bool:
        """检查商品是否有足够库存"""
        # TODO: 检查库存是否足够
        pass
    
    def reduce_stock(self, quantity: int):
        """减少库存"""
        # TODO: 减少指定数量的库存
        pass
    
    def increase_stock(self, quantity: int):
        """增加库存"""
        # TODO: 增加指定数量的库存
        pass
    
    def __str__(self):
        # TODO: 返回商品的字符串表示
        pass


class CartItem:
    """购物车项目类
    
    TODO: 实现购物车项目，包含商品和数量
    """
    
    def __init__(self, product: Product, quantity: int):
        # TODO: 初始化购物车项目
        pass
    
    @property
    def quantity(self):
        """数量getter"""
        # TODO: 返回数量
        pass
    
    @quantity.setter
    def quantity(self, value: int):
        """数量setter - 带验证"""
        # TODO: 验证数量并设置
        pass
    
    @property
    def subtotal(self):
        """小计getter"""
        # TODO: 计算小计（价格 * 数量）
        pass
    
    def update_quantity(self, new_quantity: int):
        """更新数量"""
        # TODO: 更新商品数量
        pass
    
    def __str__(self):
        # TODO: 返回购物车项目的字符串表示
        pass


class ShoppingCart:
    """购物车类
    
    TODO: 实现购物车，包含多个购物车项目
    """
    
    def __init__(self, user: User):
        # TODO: 初始化购物车
        # self._user = user
        # self._items = {}  # {product_id: CartItem}
        # self._created_at = datetime.now()
        pass
    
    @property
    def total_items(self):
        """总商品数量"""
        # TODO: 计算购物车中的总商品数量
        pass
    
    @property
    def total_amount(self):
        """总金额"""
        # TODO: 计算购物车总金额
        pass
    
    @property
    def is_empty(self):
        """购物车是否为空"""
        # TODO: 检查购物车是否为空
        pass
    
    def add_item(self, product: Product, quantity: int = 1):
        """添加商品到购物车"""
        # TODO: 添加商品到购物车
        # 1. 检查商品库存
        # 2. 如果商品已存在，增加数量
        # 3. 如果商品不存在，创建新的CartItem
        pass
    
    def remove_item(self, product_id: str):
        """从购物车移除商品"""
        # TODO: 从购物车移除指定商品
        pass
    
    def update_item_quantity(self, product_id: str, new_quantity: int):
        """更新商品数量"""
        # TODO: 更新指定商品的数量
        pass
    
    def clear(self):
        """清空购物车"""
        # TODO: 清空购物车
        pass
    
    def get_items(self) -> List[CartItem]:
        """获取购物车项目列表"""
        # TODO: 返回购物车项目列表
        pass
    
    def apply_discount(self, discount_percent: float):
        """应用折扣"""
        # TODO: 应用折扣（可以是受保护方法）
        pass
    
    def checkout(self) -> dict:
        """结账"""
        # TODO: 实现结账逻辑
        # 1. 检查所有商品库存
        # 2. 计算总金额
        # 3. 减少商品库存
        # 4. 清空购物车
        # 5. 返回订单信息
        pass
    
    def __str__(self):
        # TODO: 返回购物车的字符串表示
        pass


# ============================================================================
# 练习3: 单例模式 - 配置管理器
# ============================================================================

class ConfigManager:
    """配置管理器 - 单例模式
    
    TODO: 实现单例模式的配置管理器
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """单例模式实现"""
        # TODO: 实现单例模式
        pass
    
    def __init__(self):
        """初始化配置管理器"""
        # TODO: 确保只初始化一次
        # if not self._initialized:
        #     self._config = {}
        #     self._config_file = "config.json"
        #     self._load_default_config()
        #     ConfigManager._initialized = True
        pass
    
    def _load_default_config(self):
        """加载默认配置 - 私有方法"""
        # TODO: 加载默认配置
        pass
    
    def get_config(self, key: str, default=None):
        """获取配置值"""
        # TODO: 获取指定键的配置值
        pass
    
    def set_config(self, key: str, value):
        """设置配置值"""
        # TODO: 设置配置值
        pass
    
    def update_config(self, config_dict: dict):
        """批量更新配置"""
        # TODO: 批量更新配置
        pass
    
    def save_config(self):
        """保存配置到文件"""
        # TODO: 保存配置到文件
        pass
    
    def load_config(self):
        """从文件加载配置"""
        # TODO: 从文件加载配置
        pass
    
    def reset_config(self):
        """重置配置为默认值"""
        # TODO: 重置配置
        pass
    
    def get_all_config(self) -> dict:
        """获取所有配置"""
        # TODO: 返回所有配置的副本
        pass


# ============================================================================
# 练习4: 观察者模式 - 事件系统
# ============================================================================

class Observer:
    """观察者接口
    
    TODO: 定义观察者接口
    """
    
    def update(self, event_type: str, data: dict):
        """接收通知"""
        # TODO: 定义更新方法
        pass


class EventPublisher:
    """事件发布者
    
    TODO: 实现事件发布者，支持观察者模式
    """
    
    def __init__(self):
        # TODO: 初始化观察者列表
        # self._observers = {}  # {event_type: [observers]}
        pass
    
    def subscribe(self, event_type: str, observer: Observer):
        """订阅事件"""
        # TODO: 添加观察者到指定事件类型
        pass
    
    def unsubscribe(self, event_type: str, observer: Observer):
        """取消订阅事件"""
        # TODO: 从指定事件类型移除观察者
        pass
    
    def notify(self, event_type: str, data: dict):
        """通知观察者"""
        # TODO: 通知所有订阅了指定事件类型的观察者
        pass
    
    def get_subscriber_count(self, event_type: str) -> int:
        """获取订阅者数量"""
        # TODO: 返回指定事件类型的订阅者数量
        pass


class EmailNotifier(Observer):
    """邮件通知器
    
    TODO: 实现邮件通知观察者
    """
    
    def __init__(self, email: str):
        # TODO: 初始化邮件地址
        pass
    
    def update(self, event_type: str, data: dict):
        """接收事件通知并发送邮件"""
        # TODO: 实现邮件通知逻辑
        pass


class SMSNotifier(Observer):
    """短信通知器
    
    TODO: 实现短信通知观察者
    """
    
    def __init__(self, phone: str):
        # TODO: 初始化手机号
        pass
    
    def update(self, event_type: str, data: dict):
        """接收事件通知并发送短信"""
        # TODO: 实现短信通知逻辑
        pass


class LogNotifier(Observer):
    """日志通知器
    
    TODO: 实现日志通知观察者
    """
    
    def __init__(self, log_file: str = "events.log"):
        # TODO: 初始化日志文件
        pass
    
    def update(self, event_type: str, data: dict):
        """接收事件通知并记录日志"""
        # TODO: 实现日志记录逻辑
        pass


# ============================================================================
# 测试函数
# ============================================================================

def test_user_encapsulation():
    """测试用户类的封装"""
    print("=== 测试用户类封装 ===")
    
    # TODO: 创建用户并测试各种功能
    # user = User("john_doe", "john@example.com", "SecurePass123", UserRole.USER)
    # print(f"用户创建: {user}")
    # print(f"用户信息: {user.get_user_info()}")
    
    # TODO: 测试登录功能
    # print(f"登录结果: {user.login('SecurePass123')}")
    # print(f"登录状态: {user.is_logged_in}")
    
    # TODO: 测试密码修改
    # print(f"密码修改: {user.change_password('SecurePass123', 'NewSecurePass456')}")
    
    # TODO: 测试权限检查
    # print(f"用户权限: {user.has_permission(UserRole.ADMIN)}")
    
    pass


def test_shopping_cart():
    """测试购物车系统"""
    print("=== 测试购物车系统 ===")
    
    # TODO: 创建用户和商品
    # user = User("customer", "customer@example.com", "Password123")
    # product1 = Product("P001", "笔记本电脑", 5999.99, 10, "电子产品")
    # product2 = Product("P002", "无线鼠标", 199.99, 50, "电子产品")
    
    # TODO: 创建购物车并添加商品
    # cart = ShoppingCart(user)
    # cart.add_item(product1, 1)
    # cart.add_item(product2, 2)
    
    # TODO: 测试购物车功能
    # print(f"购物车: {cart}")
    # print(f"总商品数: {cart.total_items}")
    # print(f"总金额: {cart.total_amount}")
    
    # TODO: 测试结账
    # order = cart.checkout()
    # print(f"订单信息: {order}")
    
    pass


def test_singleton_pattern():
    """测试单例模式"""
    print("=== 测试单例模式 ===")
    
    # TODO: 测试单例模式
    # config1 = ConfigManager()
    # config2 = ConfigManager()
    # print(f"是否为同一实例: {config1 is config2}")
    
    # TODO: 测试配置管理
    # config1.set_config("app_name", "我的应用")
    # print(f"从config2获取配置: {config2.get_config('app_name')}")
    
    pass


def test_observer_pattern():
    """测试观察者模式"""
    print("=== 测试观察者模式 ===")
    
    # TODO: 创建事件发布者和观察者
    # publisher = EventPublisher()
    # email_notifier = EmailNotifier("admin@example.com")
    # sms_notifier = SMSNotifier("13812345678")
    # log_notifier = LogNotifier()
    
    # TODO: 订阅事件
    # publisher.subscribe("user_login", email_notifier)
    # publisher.subscribe("user_login", log_notifier)
    # publisher.subscribe("order_created", sms_notifier)
    # publisher.subscribe("order_created", log_notifier)
    
    # TODO: 发布事件
    # publisher.notify("user_login", {"user": "john_doe", "time": datetime.now()})
    # publisher.notify("order_created", {"order_id": "ORD001", "amount": 299.99})
    
    pass


def test_access_control():
    """测试访问控制"""
    print("=== 测试访问控制 ===")
    
    # TODO: 测试不同的访问控制
    # user = User("test_user", "test@example.com", "TestPass123")
    
    # TODO: 测试公开属性访问
    # print(f"公开属性 - 用户名: {user.username}")
    
    # TODO: 测试受保护属性访问
    # print(f"受保护属性 - 邮箱: {user._email}")
    
    # TODO: 测试私有属性访问（应该失败）
    # try:
    #     print(f"私有属性 - 密码哈希: {user.__password_hash}")
    # except AttributeError:
    #     print("❌ 无法直接访问私有属性")
    
    # TODO: 测试属性装饰器
    # try:
    #     password = user.password  # 应该抛出异常
    # except Exception as e:
    #     print(f"❌ 密码访问被拒绝: {e}")
    
    pass


def main():
    """主函数 - 运行所有测试"""
    print("Session09 练习3: 封装和设计模式练习")
    print("=" * 50)
    
    test_user_encapsulation()
    test_shopping_cart()
    test_singleton_pattern()
    test_observer_pattern()
    test_access_control()
    
    print("\n💡 练习要点:")
    print("   1. 合理使用公开、受保护、私有属性")
    print("   2. 属性装饰器的验证和保护")
    print("   3. 单例模式的正确实现")
    print("   4. 观察者模式的事件通知")
    print("   5. 封装提供的数据安全性")
    
    print("\n🎯 完成练习后，请运行测试函数验证实现")


if __name__ == "__main__":
    main()


# ============================================================================
# 练习提示和参考答案
# ============================================================================

"""
💡 实现提示：

1. User类封装：
   - 使用@property装饰器创建安全的属性访问
   - 密码使用SHA-256哈希存储
   - 邮箱格式验证使用正则表达式
   - 权限检查使用枚举比较

2. 购物车系统：
   - Product类包含价格和库存验证
   - CartItem封装商品和数量
   - ShoppingCart管理多个CartItem
   - 结账时需要检查库存并更新

3. 单例模式：
   - 重写__new__方法确保只有一个实例
   - 使用类变量_instance存储实例
   - 使用_initialized标志避免重复初始化

4. 观察者模式：
   - Observer定义通用接口
   - EventPublisher管理观察者列表
   - 不同类型的通知器实现Observer接口
   - 支持事件类型分类

5. 访问控制要点：
   - 公开属性：直接访问
   - 受保护属性：_name（约定）
   - 私有属性：__name（名称改写）
   - 属性装饰器：控制访问和验证

🔍 测试要点：
   - 验证封装的有效性
   - 检查访问控制是否正确
   - 测试设计模式的实现
   - 确认数据验证和保护
   - 验证业务逻辑的正确性

🎯 扩展练习：
   - 添加更多的用户角色和权限
   - 实现购物车的持久化存储
   - 扩展配置管理器支持不同格式
   - 添加更多类型的事件通知器
   - 实现其他设计模式（工厂、装饰器等）
"""