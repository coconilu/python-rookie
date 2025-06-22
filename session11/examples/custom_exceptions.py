#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session11 示例2: 自定义异常

本文件演示了如何创建和使用自定义异常类，以及异常的继承关系。

作者: Python教程团队
创建日期: 2024-01-15
"""


# 基础自定义异常类
class ApplicationError(Exception):
    """应用程序异常基类"""
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
    
    def __str__(self):
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


# 验证相关异常
class ValidationError(ApplicationError):
    """验证错误异常"""
    def __init__(self, message, field=None, value=None):
        super().__init__(message, "VALIDATION_ERROR")
        self.field = field
        self.value = value
    
    def __str__(self):
        if self.field:
            return f"验证错误 [{self.field}]: {self.message}"
        return f"验证错误: {self.message}"


class RequiredFieldError(ValidationError):
    """必填字段错误"""
    def __init__(self, field):
        super().__init__(f"字段 '{field}' 是必填的", field)


class InvalidFormatError(ValidationError):
    """格式错误"""
    def __init__(self, field, value, expected_format):
        message = f"字段 '{field}' 的值 '{value}' 格式不正确，期望格式: {expected_format}"
        super().__init__(message, field, value)
        self.expected_format = expected_format


class ValueRangeError(ValidationError):
    """值范围错误"""
    def __init__(self, field, value, min_value=None, max_value=None):
        if min_value is not None and max_value is not None:
            message = f"字段 '{field}' 的值 {value} 超出范围 [{min_value}, {max_value}]"
        elif min_value is not None:
            message = f"字段 '{field}' 的值 {value} 小于最小值 {min_value}"
        elif max_value is not None:
            message = f"字段 '{field}' 的值 {value} 大于最大值 {max_value}"
        else:
            message = f"字段 '{field}' 的值 {value} 超出允许范围"
        
        super().__init__(message, field, value)
        self.min_value = min_value
        self.max_value = max_value


# 业务逻辑相关异常
class BusinessLogicError(ApplicationError):
    """业务逻辑错误异常"""
    def __init__(self, message, operation=None):
        super().__init__(message, "BUSINESS_ERROR")
        self.operation = operation


class InsufficientFundsError(BusinessLogicError):
    """余额不足错误"""
    def __init__(self, current_balance, required_amount):
        message = f"余额不足：当前余额 {current_balance}，需要 {required_amount}"
        super().__init__(message, "withdraw")
        self.current_balance = current_balance
        self.required_amount = required_amount


class AccountLockedError(BusinessLogicError):
    """账户锁定错误"""
    def __init__(self, account_id, reason="未知原因"):
        message = f"账户 {account_id} 已被锁定：{reason}"
        super().__init__(message, "account_access")
        self.account_id = account_id
        self.reason = reason


# 系统相关异常
class SystemError(ApplicationError):
    """系统错误异常"""
    def __init__(self, message, component=None):
        super().__init__(message, "SYSTEM_ERROR")
        self.component = component


class DatabaseConnectionError(SystemError):
    """数据库连接错误"""
    def __init__(self, database_url, original_error=None):
        message = f"无法连接到数据库: {database_url}"
        super().__init__(message, "database")
        self.database_url = database_url
        self.original_error = original_error


class ConfigurationError(SystemError):
    """配置错误"""
    def __init__(self, config_key, config_value=None):
        if config_value is not None:
            message = f"配置项 '{config_key}' 的值 '{config_value}' 无效"
        else:
            message = f"缺少必要的配置项: '{config_key}'"
        super().__init__(message, "configuration")
        self.config_key = config_key
        self.config_value = config_value


# 使用自定义异常的示例类
class User:
    """用户类 - 演示自定义异常的使用"""
    
    def __init__(self, username, email, age, balance=0.0):
        self.username = self._validate_username(username)
        self.email = self._validate_email(email)
        self.age = self._validate_age(age)
        self.balance = balance
        self.is_locked = False
        self.lock_reason = None
    
    def _validate_username(self, username):
        """验证用户名"""
        if not username:
            raise RequiredFieldError("username")
        
        if not isinstance(username, str):
            raise ValidationError("用户名必须是字符串", "username", username)
        
        if len(username) < 3:
            raise ValueRangeError("username", len(username), min_value=3)
        
        if len(username) > 20:
            raise ValueRangeError("username", len(username), max_value=20)
        
        # 检查用户名格式
        import re
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise InvalidFormatError("username", username, "字母、数字和下划线")
        
        return username
    
    def _validate_email(self, email):
        """验证邮箱"""
        if not email:
            raise RequiredFieldError("email")
        
        if not isinstance(email, str):
            raise ValidationError("邮箱必须是字符串", "email", email)
        
        # 简单的邮箱格式验证
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise InvalidFormatError("email", email, "有效的邮箱地址")
        
        return email
    
    def _validate_age(self, age):
        """验证年龄"""
        if age is None:
            raise RequiredFieldError("age")
        
        if not isinstance(age, int):
            raise ValidationError("年龄必须是整数", "age", age)
        
        if age < 0:
            raise ValueRangeError("age", age, min_value=0)
        
        if age > 150:
            raise ValueRangeError("age", age, max_value=150)
        
        return age
    
    def deposit(self, amount):
        """存款"""
        if self.is_locked:
            raise AccountLockedError(self.username, self.lock_reason)
        
        if not isinstance(amount, (int, float)):
            raise ValidationError("存款金额必须是数字", "amount", amount)
        
        if amount <= 0:
            raise ValueRangeError("amount", amount, min_value=0.01)
        
        self.balance += amount
        return self.balance
    
    def withdraw(self, amount):
        """取款"""
        if self.is_locked:
            raise AccountLockedError(self.username, self.lock_reason)
        
        if not isinstance(amount, (int, float)):
            raise ValidationError("取款金额必须是数字", "amount", amount)
        
        if amount <= 0:
            raise ValueRangeError("amount", amount, min_value=0.01)
        
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount)
        
        self.balance -= amount
        return self.balance
    
    def lock_account(self, reason="管理员操作"):
        """锁定账户"""
        self.is_locked = True
        self.lock_reason = reason
    
    def unlock_account(self):
        """解锁账户"""
        self.is_locked = False
        self.lock_reason = None
    
    def __str__(self):
        status = "锁定" if self.is_locked else "正常"
        return f"用户: {self.username}, 邮箱: {self.email}, 年龄: {self.age}, 余额: {self.balance}, 状态: {status}"


class BankSystem:
    """银行系统类 - 演示系统级异常"""
    
    def __init__(self, config=None):
        self.users = {}
        self.config = config or {}
        self._validate_config()
    
    def _validate_config(self):
        """验证系统配置"""
        required_configs = ['database_url', 'max_users', 'daily_limit']
        
        for key in required_configs:
            if key not in self.config:
                raise ConfigurationError(key)
        
        # 验证配置值
        if not isinstance(self.config['max_users'], int) or self.config['max_users'] <= 0:
            raise ConfigurationError('max_users', self.config['max_users'])
        
        if not isinstance(self.config['daily_limit'], (int, float)) or self.config['daily_limit'] <= 0:
            raise ConfigurationError('daily_limit', self.config['daily_limit'])
    
    def create_user(self, username, email, age, initial_balance=0.0):
        """创建用户"""
        if len(self.users) >= self.config['max_users']:
            raise BusinessLogicError(f"系统用户数量已达上限: {self.config['max_users']}")
        
        if username in self.users:
            raise BusinessLogicError(f"用户名 '{username}' 已存在")
        
        try:
            user = User(username, email, age, initial_balance)
            self.users[username] = user
            return user
        except ValidationError:
            # 重新抛出验证错误
            raise
        except Exception as e:
            # 包装其他异常为系统错误
            raise SystemError(f"创建用户时发生系统错误: {e}")
    
    def get_user(self, username):
        """获取用户"""
        if username not in self.users:
            raise BusinessLogicError(f"用户 '{username}' 不存在")
        return self.users[username]
    
    def transfer(self, from_username, to_username, amount):
        """转账"""
        if amount > self.config['daily_limit']:
            raise BusinessLogicError(f"转账金额 {amount} 超过日限额 {self.config['daily_limit']}")
        
        from_user = self.get_user(from_username)
        to_user = self.get_user(to_username)
        
        # 执行转账
        from_user.withdraw(amount)
        to_user.deposit(amount)
        
        return f"转账成功: {from_username} -> {to_username}, 金额: {amount}"


def demo_custom_exceptions():
    """演示自定义异常的使用"""
    print("=== 自定义异常演示 ===")
    
    # 1. 用户创建和验证异常
    print("\n1. 用户创建和验证异常:")
    
    test_cases = [
        ("", "test@example.com", 25),  # 用户名为空
        ("ab", "test@example.com", 25),  # 用户名太短
        ("valid_user", "invalid-email", 25),  # 邮箱格式错误
        ("valid_user", "test@example.com", -5),  # 年龄为负
        ("valid_user", "test@example.com", 200),  # 年龄过大
        ("valid_user", "test@example.com", 25),  # 正常情况
    ]
    
    for username, email, age in test_cases:
        try:
            user = User(username, email, age)
            print(f"✓ 用户创建成功: {user}")
        except RequiredFieldError as e:
            print(f"✗ 必填字段错误: {e}")
        except InvalidFormatError as e:
            print(f"✗ 格式错误: {e} (期望: {e.expected_format})")
        except ValueRangeError as e:
            print(f"✗ 值范围错误: {e}")
        except ValidationError as e:
            print(f"✗ 验证错误: {e}")
    
    # 2. 业务逻辑异常
    print("\n2. 业务逻辑异常:")
    
    try:
        user = User("test_user", "test@example.com", 25, 100.0)
        print(f"初始用户: {user}")
        
        # 正常存款
        user.deposit(50.0)
        print(f"存款后: 余额 {user.balance}")
        
        # 正常取款
        user.withdraw(30.0)
        print(f"取款后: 余额 {user.balance}")
        
        # 余额不足
        user.withdraw(200.0)
        
    except InsufficientFundsError as e:
        print(f"✗ 余额不足: {e}")
        print(f"  当前余额: {e.current_balance}, 需要金额: {e.required_amount}")
    
    # 3. 账户锁定异常
    print("\n3. 账户锁定异常:")
    
    try:
        user = User("locked_user", "locked@example.com", 30, 500.0)
        user.lock_account("可疑活动")
        print(f"账户已锁定: {user}")
        
        user.withdraw(100.0)  # 尝试从锁定账户取款
        
    except AccountLockedError as e:
        print(f"✗ 账户锁定错误: {e}")
        print(f"  账户ID: {e.account_id}, 锁定原因: {e.reason}")
    
    # 4. 系统配置异常
    print("\n4. 系统配置异常:")
    
    # 缺少配置
    try:
        bank = BankSystem({})
    except ConfigurationError as e:
        print(f"✗ 配置错误: {e}")
        print(f"  缺少配置项: {e.config_key}")
    
    # 无效配置值
    try:
        bank = BankSystem({
            'database_url': 'sqlite:///bank.db',
            'max_users': -1,  # 无效值
            'daily_limit': 10000
        })
    except ConfigurationError as e:
        print(f"✗ 配置错误: {e}")
        print(f"  配置项: {e.config_key}, 无效值: {e.config_value}")
    
    # 5. 完整的银行系统演示
    print("\n5. 完整的银行系统演示:")
    
    try:
        # 正确的配置
        bank = BankSystem({
            'database_url': 'sqlite:///bank.db',
            'max_users': 2,
            'daily_limit': 1000.0
        })
        
        # 创建用户
        user1 = bank.create_user("alice", "alice@example.com", 25, 500.0)
        user2 = bank.create_user("bob", "bob@example.com", 30, 300.0)
        print(f"✓ 用户创建成功: {user1}")
        print(f"✓ 用户创建成功: {user2}")
        
        # 正常转账
        result = bank.transfer("alice", "bob", 100.0)
        print(f"✓ {result}")
        print(f"  Alice余额: {user1.balance}, Bob余额: {user2.balance}")
        
        # 超过日限额的转账
        bank.transfer("alice", "bob", 2000.0)
        
    except BusinessLogicError as e:
        print(f"✗ 业务逻辑错误: {e}")
        if hasattr(e, 'operation'):
            print(f"  操作: {e.operation}")
    except ValidationError as e:
        print(f"✗ 验证错误: {e}")
    except SystemError as e:
        print(f"✗ 系统错误: {e}")
        if hasattr(e, 'component'):
            print(f"  组件: {e.component}")


def demo_exception_hierarchy():
    """演示异常继承层次"""
    print("\n=== 异常继承层次演示 ===")
    
    def handle_application_errors(func, *args, **kwargs):
        """统一处理应用程序异常"""
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            print(f"验证异常: {e}")
            if hasattr(e, 'field'):
                print(f"  字段: {e.field}")
            if hasattr(e, 'value'):
                print(f"  值: {e.value}")
        except BusinessLogicError as e:
            print(f"业务逻辑异常: {e}")
            if hasattr(e, 'operation'):
                print(f"  操作: {e.operation}")
        except SystemError as e:
            print(f"系统异常: {e}")
            if hasattr(e, 'component'):
                print(f"  组件: {e.component}")
        except ApplicationError as e:
            print(f"应用程序异常: {e}")
            if hasattr(e, 'error_code'):
                print(f"  错误代码: {e.error_code}")
        except Exception as e:
            print(f"未知异常: {e}")
    
    # 测试不同类型的异常
    print("\n测试异常处理:")
    
    # 验证异常
    handle_application_errors(lambda: User("", "test@example.com", 25))
    
    # 业务逻辑异常
    user = User("test", "test@example.com", 25, 100)
    handle_application_errors(lambda: user.withdraw(200))
    
    # 系统异常
    handle_application_errors(lambda: BankSystem({}))


def main():
    """主函数"""
    print("Session11 示例2: 自定义异常")
    print("=" * 50)
    
    demo_custom_exceptions()
    demo_exception_hierarchy()
    
    print("\n示例演示完成！")


if __name__ == "__main__":
    main()