#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session09 示例3: 封装和访问控制

演示封装的概念和Python中的访问控制，包括：
- 公开、受保护、私有属性
- 属性装饰器（@property）
- getter和setter方法
- 数据验证和保护
- 信息隐藏的好处

作者: Python教程团队
创建日期: 2024-01-09
"""

from datetime import datetime, timedelta
import re


class BankAccount:
    """银行账户类 - 演示封装和访问控制"""
    
    # 类变量（公开）
    bank_name = "Python银行"
    interest_rate = 0.03  # 年利率3%
    
    def __init__(self, account_number, owner_name, initial_balance=0, pin="1234"):
        # 公开属性
        self.account_number = account_number
        self.owner_name = owner_name
        self.created_date = datetime.now()
        
        # 受保护属性（约定：以单下划线开头）
        self._balance = initial_balance
        self._transaction_count = 0
        
        # 私有属性（名称改写：以双下划线开头）
        self.__pin = pin
        self.__transaction_history = []
        self.__is_frozen = False
        
        # 添加开户记录
        self.__add_transaction(f"开户，初始余额: {initial_balance}")
    
    # 公开方法
    def get_account_info(self):
        """获取账户基本信息（公开方法）"""
        return {
            "账户号码": self.account_number,
            "户主姓名": self.owner_name,
            "开户日期": self.created_date.strftime("%Y-%m-%d"),
            "交易次数": self._transaction_count
        }
    
    def deposit(self, amount):
        """存款（公开方法）"""
        if self.__is_frozen:
            print("❌ 账户已冻结，无法存款")
            return False
        
        if amount <= 0:
            print("❌ 存款金额必须大于0")
            return False
        
        self._balance += amount
        self._transaction_count += 1
        self.__add_transaction(f"存款: +{amount}")
        print(f"✅ 存款成功，当前余额: {self._balance}")
        return True
    
    def withdraw(self, amount, pin):
        """取款（公开方法，需要PIN验证）"""
        if not self.__verify_pin(pin):
            print("❌ PIN码错误")
            return False
        
        if self.__is_frozen:
            print("❌ 账户已冻结，无法取款")
            return False
        
        if amount <= 0:
            print("❌ 取款金额必须大于0")
            return False
        
        if amount > self._balance:
            print("❌ 余额不足")
            return False
        
        self._balance -= amount
        self._transaction_count += 1
        self.__add_transaction(f"取款: -{amount}")
        print(f"✅ 取款成功，当前余额: {self._balance}")
        return True
    
    def transfer(self, target_account, amount, pin):
        """转账（公开方法）"""
        if not self.__verify_pin(pin):
            print("❌ PIN码错误")
            return False
        
        if self.withdraw(amount, pin):
            if target_account.deposit(amount):
                self.__add_transaction(f"转账给 {target_account.account_number}: -{amount}")
                target_account._BankAccount__add_transaction(f"来自 {self.account_number} 的转账: +{amount}")
                print(f"✅ 转账成功")
                return True
        return False
    
    # 受保护方法（约定：以单下划线开头）
    def _calculate_interest(self):
        """计算利息（受保护方法）"""
        return self._balance * self.interest_rate / 365  # 日利息
    
    def _apply_daily_interest(self):
        """应用日利息（受保护方法）"""
        if self._balance > 0:
            interest = self._calculate_interest()
            self._balance += interest
            self.__add_transaction(f"利息: +{interest:.2f}")
            return interest
        return 0
    
    # 私有方法（名称改写：以双下划线开头）
    def __verify_pin(self, pin):
        """验证PIN码（私有方法）"""
        return pin == self.__pin
    
    def __add_transaction(self, description):
        """添加交易记录（私有方法）"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__transaction_history.append(f"[{timestamp}] {description}")
    
    def __freeze_account(self):
        """冻结账户（私有方法）"""
        self.__is_frozen = True
        self.__add_transaction("账户已冻结")
    
    def __unfreeze_account(self):
        """解冻账户（私有方法）"""
        self.__is_frozen = False
        self.__add_transaction("账户已解冻")
    
    # 管理员方法（需要特殊权限）
    def admin_freeze_account(self, admin_pin="admin123"):
        """管理员冻结账户"""
        if admin_pin == "admin123":
            self.__freeze_account()
            print(f"✅ 管理员已冻结账户 {self.account_number}")
        else:
            print("❌ 管理员权限验证失败")
    
    def admin_unfreeze_account(self, admin_pin="admin123"):
        """管理员解冻账户"""
        if admin_pin == "admin123":
            self.__unfreeze_account()
            print(f"✅ 管理员已解冻账户 {self.account_number}")
        else:
            print("❌ 管理员权限验证失败")
    
    def get_balance(self, pin):
        """查询余额（需要PIN验证）"""
        if self.__verify_pin(pin):
            return self._balance
        else:
            print("❌ PIN码错误")
            return None
    
    def get_transaction_history(self, pin, limit=10):
        """获取交易历史（需要PIN验证）"""
        if self.__verify_pin(pin):
            return self.__transaction_history[-limit:]
        else:
            print("❌ PIN码错误")
            return []
    
    def change_pin(self, old_pin, new_pin):
        """修改PIN码"""
        if not self.__verify_pin(old_pin):
            print("❌ 原PIN码错误")
            return False
        
        if len(new_pin) != 4 or not new_pin.isdigit():
            print("❌ 新PIN码必须是4位数字")
            return False
        
        self.__pin = new_pin
        self.__add_transaction("PIN码已修改")
        print("✅ PIN码修改成功")
        return True
    
    # 属性装饰器演示
    @property
    def account_status(self):
        """账户状态（只读属性）"""
        if self.__is_frozen:
            return "已冻结"
        elif self._balance < 0:
            return "透支"
        elif self._balance == 0:
            return "零余额"
        else:
            return "正常"
    
    @property
    def account_age_days(self):
        """账户开户天数（只读属性）"""
        return (datetime.now() - self.created_date).days
    
    def __str__(self):
        return f"账户({self.account_number}) - {self.owner_name}"
    
    def __repr__(self):
        return f"BankAccount('{self.account_number}', '{self.owner_name}', {self._balance})"


class Student:
    """学生类 - 演示属性装饰器的高级用法"""
    
    def __init__(self, student_id, name, age):
        self.student_id = student_id
        self.name = name
        self._age = None
        self._email = None
        self._phone = None
        self._grades = {}
        
        # 使用setter进行验证
        self.age = age
    
    @property
    def age(self):
        """年龄getter"""
        return self._age
    
    @age.setter
    def age(self, value):
        """年龄setter - 带验证"""
        if not isinstance(value, int):
            raise TypeError("年龄必须是整数")
        if value < 0 or value > 150:
            raise ValueError("年龄必须在0-150之间")
        self._age = value
    
    @property
    def email(self):
        """邮箱getter"""
        return self._email
    
    @email.setter
    def email(self, value):
        """邮箱setter - 带格式验证"""
        if value is None:
            self._email = None
            return
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value):
            raise ValueError("邮箱格式不正确")
        self._email = value
    
    @property
    def phone(self):
        """电话getter"""
        return self._phone
    
    @phone.setter
    def phone(self, value):
        """电话setter - 带格式验证"""
        if value is None:
            self._phone = None
            return
        
        # 简单的手机号验证（11位数字）
        if not (isinstance(value, str) and len(value) == 11 and value.isdigit()):
            raise ValueError("手机号必须是11位数字")
        self._phone = value
    
    @property
    def average_grade(self):
        """平均成绩（只读属性）"""
        if not self._grades:
            return 0
        return sum(self._grades.values()) / len(self._grades)
    
    @property
    def grade_level(self):
        """成绩等级（只读属性）"""
        avg = self.average_grade
        if avg >= 90:
            return "优秀"
        elif avg >= 80:
            return "良好"
        elif avg >= 70:
            return "中等"
        elif avg >= 60:
            return "及格"
        else:
            return "不及格"
    
    def add_grade(self, subject, grade):
        """添加成绩"""
        if not isinstance(grade, (int, float)):
            raise TypeError("成绩必须是数字")
        if grade < 0 or grade > 100:
            raise ValueError("成绩必须在0-100之间")
        
        self._grades[subject] = grade
        print(f"✅ 已添加 {subject} 成绩: {grade}")
    
    def get_grades(self):
        """获取所有成绩"""
        return self._grades.copy()
    
    def __str__(self):
        return f"学生({self.student_id}) - {self.name}, {self.age}岁"


class Temperature:
    """温度类 - 演示属性装饰器的温度转换"""
    
    def __init__(self, celsius=0):
        self._celsius = celsius
    
    @property
    def celsius(self):
        """摄氏度"""
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        """设置摄氏度"""
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度(-273.15°C)")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        """华氏度（只读）"""
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        """通过华氏度设置温度"""
        celsius_value = (value - 32) * 5/9
        self.celsius = celsius_value  # 使用celsius的setter进行验证
    
    @property
    def kelvin(self):
        """开尔文（只读）"""
        return self._celsius + 273.15
    
    @kelvin.setter
    def kelvin(self, value):
        """通过开尔文设置温度"""
        if value < 0:
            raise ValueError("开尔文温度不能为负数")
        self.celsius = value - 273.15
    
    def __str__(self):
        return f"{self.celsius:.1f}°C / {self.fahrenheit:.1f}°F / {self.kelvin:.1f}K"


def demonstrate_bank_account():
    """演示银行账户的封装"""
    print("=== 银行账户封装演示 ===")
    
    # 创建账户
    account1 = BankAccount("123456789", "张三", 1000)
    account2 = BankAccount("987654321", "李四", 500)
    
    print(f"创建账户: {account1}")
    print(f"账户信息: {account1.get_account_info()}")
    print(f"账户状态: {account1.account_status}")
    print(f"开户天数: {account1.account_age_days}")
    print()
    
    # 正常操作
    print("--- 正常操作 ---")
    account1.deposit(200)
    print(f"余额: {account1.get_balance('1234')}")
    account1.withdraw(150, "1234")
    account1.transfer(account2, 100, "1234")
    print()
    
    # 错误操作演示
    print("--- 错误操作演示 ---")
    account1.withdraw(2000, "1234")  # 余额不足
    account1.withdraw(100, "0000")   # PIN错误
    account1.deposit(-50)            # 负数存款
    print()
    
    # 查看交易历史
    print("--- 交易历史 ---")
    history = account1.get_transaction_history("1234")
    for record in history:
        print(record)
    print()
    
    # 管理员操作
    print("--- 管理员操作 ---")
    account1.admin_freeze_account()
    print(f"账户状态: {account1.account_status}")
    account1.deposit(100)  # 冻结后无法操作
    account1.admin_unfreeze_account()
    account1.deposit(100)  # 解冻后可以操作
    print()
    
    # 尝试访问私有属性（演示封装保护）
    print("--- 封装保护演示 ---")
    print(f"公开属性 - 账户号: {account1.account_number}")
    print(f"受保护属性 - 余额: {account1._balance}")
    
    # 尝试访问私有属性（会失败或访问到改写后的名称）
    try:
        print(f"私有属性 - PIN: {account1.__pin}")  # 这会失败
    except AttributeError:
        print("❌ 无法直接访问私有属性 __pin")
    
    # 通过名称改写访问（不推荐）
    print(f"通过名称改写访问PIN: {account1._BankAccount__pin}")
    print("⚠️  虽然可以访问，但这违反了封装原则")
    print()


def demonstrate_student_properties():
    """演示学生类的属性装饰器"""
    print("=== 学生类属性装饰器演示 ===")
    
    # 创建学生
    student = Student("2023001", "王小明", 20)
    print(f"学生信息: {student}")
    
    # 设置和验证属性
    print("\n--- 属性设置和验证 ---")
    try:
        student.email = "xiaoming@example.com"
        student.phone = "13812345678"
        print(f"邮箱: {student.email}")
        print(f"电话: {student.phone}")
    except ValueError as e:
        print(f"❌ 验证错误: {e}")
    
    # 错误的属性设置
    print("\n--- 错误属性设置演示 ---")
    try:
        student.age = -5  # 无效年龄
    except ValueError as e:
        print(f"❌ 年龄验证错误: {e}")
    
    try:
        student.email = "invalid-email"  # 无效邮箱
    except ValueError as e:
        print(f"❌ 邮箱验证错误: {e}")
    
    try:
        student.phone = "123"  # 无效电话
    except ValueError as e:
        print(f"❌ 电话验证错误: {e}")
    
    # 添加成绩
    print("\n--- 成绩管理 ---")
    student.add_grade("数学", 95)
    student.add_grade("英语", 88)
    student.add_grade("物理", 92)
    
    print(f"所有成绩: {student.get_grades()}")
    print(f"平均成绩: {student.average_grade:.1f}")
    print(f"成绩等级: {student.grade_level}")
    print()


def demonstrate_temperature_properties():
    """演示温度类的属性装饰器"""
    print("=== 温度类属性装饰器演示 ===")
    
    # 创建温度对象
    temp = Temperature(25)
    print(f"初始温度: {temp}")
    
    # 通过不同单位设置温度
    print("\n--- 温度转换 ---")
    temp.celsius = 0
    print(f"设置摄氏度0°C: {temp}")
    
    temp.fahrenheit = 100
    print(f"设置华氏度100°F: {temp}")
    
    temp.kelvin = 300
    print(f"设置开尔文300K: {temp}")
    
    # 错误设置演示
    print("\n--- 温度验证 ---")
    try:
        temp.celsius = -300  # 低于绝对零度
    except ValueError as e:
        print(f"❌ 温度验证错误: {e}")
    
    try:
        temp.kelvin = -10  # 负开尔文
    except ValueError as e:
        print(f"❌ 开尔文验证错误: {e}")
    print()


def demonstrate_access_control():
    """演示访问控制的重要性"""
    print("=== 访问控制重要性演示 ===")
    
    account = BankAccount("111222333", "测试用户", 1000)
    
    print("--- 正确的访问方式 ---")
    print(f"通过方法查询余额: {account.get_balance('1234')}")
    account.deposit(100)
    account.withdraw(50, "1234")
    
    print("\n--- 不当的直接访问 ---")
    print(f"直接访问受保护属性: {account._balance}")
    
    # 直接修改余额（绕过验证）
    print("直接修改余额（绕过所有验证和记录）:")
    original_balance = account._balance
    account._balance = 999999  # 直接修改，绕过所有控制
    print(f"修改后余额: {account._balance}")
    print("⚠️  这样做会破坏数据完整性，没有交易记录！")
    
    # 恢复正确余额
    account._balance = original_balance
    print(f"恢复正确余额: {account._balance}")
    
    print("\n💡 封装的好处:")
    print("   • 数据验证和保护")
    print("   • 维护数据完整性")
    print("   • 隐藏实现细节")
    print("   • 提供统一接口")
    print("   • 便于维护和修改")
    print()


def main():
    """主函数"""
    print("Session09 示例3: 封装和访问控制")
    print("=" * 50)
    
    demonstrate_bank_account()
    demonstrate_student_properties()
    demonstrate_temperature_properties()
    demonstrate_access_control()
    
    print("\n💡 封装要点总结:")
    print("   • 公开属性/方法：直接访问")
    print("   • 受保护属性/方法：_name（约定，仍可访问）")
    print("   • 私有属性/方法：__name（名称改写）")
    print("   • @property：创建只读属性")
    print("   • @property.setter：创建可写属性")
    print("   • 封装提供数据保护和验证")
    print("   • 隐藏实现细节，提供清晰接口")


if __name__ == "__main__":
    main()