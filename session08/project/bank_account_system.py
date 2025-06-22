#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session08 项目演示：银行账户管理系统

这是一个完整的银行账户管理系统，展示了面向对象编程的核心概念：
- 类的定义和实例化
- 封装和数据保护
- 继承和多态
- 特殊方法的使用
- 异常处理
- 类方法和静态方法

功能特性：
1. 基础账户管理（存款、取款、查询余额）
2. 储蓄账户（利息计算）
3. 信用账户（透支功能）
4. 交易记录管理
5. 账户统计和报告
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from enum import Enum
import uuid


class TransactionType(Enum):
    """交易类型枚举"""
    DEPOSIT = "存款"
    WITHDRAWAL = "取款"
    TRANSFER_IN = "转入"
    TRANSFER_OUT = "转出"
    INTEREST = "利息"
    FEE = "手续费"


class AccountStatus(Enum):
    """账户状态枚举"""
    ACTIVE = "活跃"
    FROZEN = "冻结"
    CLOSED = "关闭"


class Transaction:
    """交易记录类"""
    
    def __init__(self, transaction_type: TransactionType, amount: float, 
                 description: str = "", balance_after: float = 0.0):
        """初始化交易记录
        
        Args:
            transaction_type (TransactionType): 交易类型
            amount (float): 交易金额
            description (str): 交易描述
            balance_after (float): 交易后余额
        """
        self.transaction_id = str(uuid.uuid4())[:8]
        self.transaction_type = transaction_type
        self.amount = amount
        self.description = description
        self.balance_after = balance_after
        self.timestamp = datetime.now()
    
    def get_info(self) -> str:
        """获取交易信息
        
        Returns:
            str: 格式化的交易信息
        """
        time_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return (
            f"[{self.transaction_id}] {time_str} | "
            f"{self.transaction_type.value} ¥{self.amount:.2f} | "
            f"余额: ¥{self.balance_after:.2f} | {self.description}"
        )
    
    def __str__(self) -> str:
        return f"{self.transaction_type.value} ¥{self.amount:.2f}"
    
    def __repr__(self) -> str:
        return f"Transaction({self.transaction_type}, {self.amount}, '{self.description}')"


class BankAccount:
    """银行账户基类"""
    
    # 类变量
    total_accounts = 0
    bank_name = "Python银行"
    min_balance = 0.0
    
    def __init__(self, account_holder: str, initial_balance: float = 0.0, 
                 account_number: Optional[str] = None):
        """初始化银行账户
        
        Args:
            account_holder (str): 账户持有人
            initial_balance (float): 初始余额，默认为0
            account_number (str, optional): 账户号码，如果不提供则自动生成
        
        Raises:
            ValueError: 当参数无效时
        """
        # 参数验证
        if not isinstance(account_holder, str) or not account_holder.strip():
            raise ValueError("账户持有人姓名必须是非空字符串")
        if not isinstance(initial_balance, (int, float)) or initial_balance < 0:
            raise ValueError("初始余额必须是非负数")
        
        # 更新账户总数
        BankAccount.total_accounts += 1
        
        # 初始化实例变量
        self.account_holder = account_holder.strip()
        self._balance = float(initial_balance)  # 使用私有变量保护余额
        self.account_number = account_number or self._generate_account_number()
        self.status = AccountStatus.ACTIVE
        self.created_date = datetime.now()
        self.last_transaction_date = datetime.now() if initial_balance > 0 else None
        self.transactions: List[Transaction] = []
        
        # 如果有初始余额，记录初始存款
        if initial_balance > 0:
            self._add_transaction(
                TransactionType.DEPOSIT, 
                initial_balance, 
                "开户初始存款"
            )
    
    def _generate_account_number(self) -> str:
        """生成账户号码（私有方法）
        
        Returns:
            str: 账户号码
        """
        return f"ACC{BankAccount.total_accounts:08d}"
    
    def _add_transaction(self, transaction_type: TransactionType, 
                        amount: float, description: str = "") -> None:
        """添加交易记录（私有方法）
        
        Args:
            transaction_type (TransactionType): 交易类型
            amount (float): 交易金额
            description (str): 交易描述
        """
        transaction = Transaction(transaction_type, amount, description, self._balance)
        self.transactions.append(transaction)
        self.last_transaction_date = datetime.now()
    
    def _validate_amount(self, amount: float) -> None:
        """验证金额（私有方法）
        
        Args:
            amount (float): 待验证的金额
        
        Raises:
            ValueError: 当金额无效时
        """
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("金额必须是正数")
    
    def _check_account_status(self) -> None:
        """检查账户状态（私有方法）
        
        Raises:
            RuntimeError: 当账户状态不允许操作时
        """
        if self.status == AccountStatus.FROZEN:
            raise RuntimeError("账户已冻结，无法进行操作")
        if self.status == AccountStatus.CLOSED:
            raise RuntimeError("账户已关闭，无法进行操作")
    
    @property
    def balance(self) -> float:
        """获取账户余额（属性）
        
        Returns:
            float: 当前余额
        """
        return self._balance
    
    def deposit(self, amount: float, description: str = "") -> bool:
        """存款
        
        Args:
            amount (float): 存款金额
            description (str): 交易描述
        
        Returns:
            bool: 存款是否成功
        
        Raises:
            ValueError: 当金额无效时
            RuntimeError: 当账户状态不允许操作时
        """
        self._check_account_status()
        self._validate_amount(amount)
        
        self._balance += amount
        self._add_transaction(
            TransactionType.DEPOSIT, 
            amount, 
            description or f"存款 ¥{amount:.2f}"
        )
        
        print(f"存款成功！金额：¥{amount:.2f}，当前余额：¥{self._balance:.2f}")
        return True
    
    def withdraw(self, amount: float, description: str = "") -> bool:
        """取款
        
        Args:
            amount (float): 取款金额
            description (str): 交易描述
        
        Returns:
            bool: 取款是否成功
        
        Raises:
            ValueError: 当金额无效时
            RuntimeError: 当账户状态不允许操作时
        """
        self._check_account_status()
        self._validate_amount(amount)
        
        if not self._can_withdraw(amount):
            print(f"取款失败！余额不足。当前余额：¥{self._balance:.2f}，尝试取款：¥{amount:.2f}")
            return False
        
        self._balance -= amount
        self._add_transaction(
            TransactionType.WITHDRAWAL, 
            amount, 
            description or f"取款 ¥{amount:.2f}"
        )
        
        print(f"取款成功！金额：¥{amount:.2f}，当前余额：¥{self._balance:.2f}")
        return True
    
    def _can_withdraw(self, amount: float) -> bool:
        """检查是否可以取款（私有方法，子类可重写）
        
        Args:
            amount (float): 取款金额
        
        Returns:
            bool: 是否可以取款
        """
        return self._balance >= amount
    
    def transfer_to(self, target_account: 'BankAccount', amount: float, 
                   description: str = "") -> bool:
        """转账到其他账户
        
        Args:
            target_account (BankAccount): 目标账户
            amount (float): 转账金额
            description (str): 交易描述
        
        Returns:
            bool: 转账是否成功
        
        Raises:
            TypeError: 当目标账户类型不正确时
            ValueError: 当金额无效时
            RuntimeError: 当账户状态不允许操作时
        """
        if not isinstance(target_account, BankAccount):
            raise TypeError("目标账户必须是BankAccount类的实例")
        
        self._check_account_status()
        target_account._check_account_status()
        self._validate_amount(amount)
        
        if not self._can_withdraw(amount):
            print(f"转账失败！余额不足。当前余额：¥{self._balance:.2f}，尝试转账：¥{amount:.2f}")
            return False
        
        # 执行转账
        self._balance -= amount
        target_account._balance += amount
        
        # 记录交易
        transfer_desc = description or f"转账给 {target_account.account_holder}"
        receive_desc = f"来自 {self.account_holder} 的转账"
        
        self._add_transaction(TransactionType.TRANSFER_OUT, amount, transfer_desc)
        target_account._add_transaction(TransactionType.TRANSFER_IN, amount, receive_desc)
        
        print(f"转账成功！向 {target_account.account_holder} 转账 ¥{amount:.2f}")
        print(f"您的余额：¥{self._balance:.2f}，对方余额：¥{target_account._balance:.2f}")
        return True
    
    def get_balance(self) -> float:
        """获取余额
        
        Returns:
            float: 当前余额
        """
        return self._balance
    
    def get_account_info(self) -> str:
        """获取账户信息
        
        Returns:
            str: 格式化的账户信息
        """
        created_str = self.created_date.strftime("%Y-%m-%d")
        last_transaction_str = (
            self.last_transaction_date.strftime("%Y-%m-%d %H:%M:%S") 
            if self.last_transaction_date else "无"
        )
        
        return (
            f"账户信息：\n"
            f"  账户号码：{self.account_number}\n"
            f"  持有人：{self.account_holder}\n"
            f"  账户类型：{self.__class__.__name__}\n"
            f"  当前余额：¥{self._balance:.2f}\n"
            f"  账户状态：{self.status.value}\n"
            f"  开户日期：{created_str}\n"
            f"  最后交易：{last_transaction_str}\n"
            f"  交易次数：{len(self.transactions)}次\n"
            f"  所属银行：{self.bank_name}"
        )
    
    def get_transaction_history(self, limit: int = 10) -> List[Transaction]:
        """获取交易历史
        
        Args:
            limit (int): 返回的交易记录数量限制，默认10条
        
        Returns:
            List[Transaction]: 交易记录列表
        """
        return self.transactions[-limit:] if limit > 0 else self.transactions
    
    def print_transaction_history(self, limit: int = 10) -> None:
        """打印交易历史
        
        Args:
            limit (int): 显示的交易记录数量限制，默认10条
        """
        transactions = self.get_transaction_history(limit)
        
        if not transactions:
            print("暂无交易记录")
            return
        
        print(f"\n最近 {len(transactions)} 条交易记录：")
        print("-" * 80)
        for transaction in transactions:
            print(transaction.get_info())
    
    def freeze_account(self) -> None:
        """冻结账户"""
        if self.status == AccountStatus.CLOSED:
            print("账户已关闭，无法冻结")
            return
        
        self.status = AccountStatus.FROZEN
        print(f"账户 {self.account_number} 已冻结")
    
    def unfreeze_account(self) -> None:
        """解冻账户"""
        if self.status == AccountStatus.FROZEN:
            self.status = AccountStatus.ACTIVE
            print(f"账户 {self.account_number} 已解冻")
        else:
            print("账户未处于冻结状态")
    
    def close_account(self) -> bool:
        """关闭账户
        
        Returns:
            bool: 关闭是否成功
        """
        if self._balance > 0:
            print(f"账户关闭失败！请先取出余额 ¥{self._balance:.2f}")
            return False
        
        self.status = AccountStatus.CLOSED
        print(f"账户 {self.account_number} 已关闭")
        return True
    
    @classmethod
    def get_bank_info(cls) -> str:
        """获取银行信息（类方法）
        
        Returns:
            str: 银行信息
        """
        return f"{cls.bank_name} - 总账户数：{cls.total_accounts}，最低余额要求：¥{cls.min_balance:.2f}"
    
    @classmethod
    def set_min_balance(cls, new_min_balance: float) -> None:
        """设置最低余额要求（类方法）
        
        Args:
            new_min_balance (float): 新的最低余额要求
        
        Raises:
            ValueError: 当金额无效时
        """
        if not isinstance(new_min_balance, (int, float)) or new_min_balance < 0:
            raise ValueError("最低余额必须是非负数")
        
        old_min = cls.min_balance
        cls.min_balance = float(new_min_balance)
        print(f"最低余额要求已更新：¥{old_min:.2f} -> ¥{new_min_balance:.2f}")
    
    @staticmethod
    def is_valid_account_number(account_number: str) -> bool:
        """验证账户号码格式（静态方法）
        
        Args:
            account_number (str): 账户号码
        
        Returns:
            bool: 是否为有效的账户号码格式
        """
        if not isinstance(account_number, str):
            return False
        
        # 简化的账户号码验证：ACC开头 + 8位数字
        return (len(account_number) == 11 and 
                account_number.startswith('ACC') and 
                account_number[3:].isdigit())
    
    def __str__(self) -> str:
        """字符串表示（用户友好）"""
        return f"{self.account_holder}的{self.__class__.__name__}({self.account_number}) - ¥{self._balance:.2f}"
    
    def __repr__(self) -> str:
        """字符串表示（开发者友好）"""
        return f"{self.__class__.__name__}('{self.account_holder}', {self._balance}, '{self.account_number}')"
    
    def __eq__(self, other) -> bool:
        """相等比较（按账户号码）"""
        if isinstance(other, BankAccount):
            return self.account_number == other.account_number
        return False
    
    def __hash__(self) -> int:
        """哈希值（基于账户号码）"""
        return hash(self.account_number)
    
    def __lt__(self, other) -> bool:
        """小于比较（按余额）"""
        if isinstance(other, BankAccount):
            return self._balance < other._balance
        return NotImplemented


class SavingsAccount(BankAccount):
    """储蓄账户类（继承自BankAccount）"""
    
    def __init__(self, account_holder: str, initial_balance: float = 0.0, 
                 interest_rate: float = 0.02, account_number: Optional[str] = None):
        """初始化储蓄账户
        
        Args:
            account_holder (str): 账户持有人
            initial_balance (float): 初始余额
            interest_rate (float): 年利率，默认2%
            account_number (str, optional): 账户号码
        
        Raises:
            ValueError: 当参数无效时
        """
        if not isinstance(interest_rate, (int, float)) or interest_rate < 0:
            raise ValueError("利率必须是非负数")
        
        super().__init__(account_holder, initial_balance, account_number)
        self.interest_rate = float(interest_rate)
        self.last_interest_date = self.created_date
    
    def calculate_interest(self, days: int = 30) -> float:
        """计算利息
        
        Args:
            days (int): 计息天数，默认30天
        
        Returns:
            float: 利息金额
        
        Raises:
            ValueError: 当天数无效时
        """
        if not isinstance(days, int) or days <= 0:
            raise ValueError("计息天数必须是正整数")
        
        # 简化的利息计算：年利率 / 365 * 天数 * 余额
        daily_rate = self.interest_rate / 365
        interest = self._balance * daily_rate * days
        return round(interest, 2)
    
    def add_interest(self, days: int = 30) -> float:
        """添加利息到账户
        
        Args:
            days (int): 计息天数，默认30天
        
        Returns:
            float: 添加的利息金额
        
        Raises:
            RuntimeError: 当账户状态不允许操作时
        """
        self._check_account_status()
        
        interest = self.calculate_interest(days)
        if interest > 0:
            self._balance += interest
            self._add_transaction(
                TransactionType.INTEREST, 
                interest, 
                f"{days}天利息，利率{self.interest_rate*100:.2f}%"
            )
            self.last_interest_date = datetime.now()
            print(f"利息已添加：¥{interest:.2f}，当前余额：¥{self._balance:.2f}")
        
        return interest
    
    def get_account_info(self) -> str:
        """获取账户信息（重写父类方法）
        
        Returns:
            str: 格式化的账户信息
        """
        base_info = super().get_account_info()
        last_interest_str = self.last_interest_date.strftime("%Y-%m-%d")
        
        savings_info = (
            f"\n储蓄账户特有信息：\n"
            f"  年利率：{self.interest_rate*100:.2f}%\n"
            f"  最后计息日期：{last_interest_str}\n"
            f"  30天预期利息：¥{self.calculate_interest(30):.2f}"
        )
        
        return base_info + savings_info


class CreditAccount(BankAccount):
    """信用账户类（继承自BankAccount）"""
    
    def __init__(self, account_holder: str, initial_balance: float = 0.0, 
                 credit_limit: float = 1000.0, account_number: Optional[str] = None):
        """初始化信用账户
        
        Args:
            account_holder (str): 账户持有人
            initial_balance (float): 初始余额
            credit_limit (float): 信用额度，默认1000元
            account_number (str, optional): 账户号码
        
        Raises:
            ValueError: 当参数无效时
        """
        if not isinstance(credit_limit, (int, float)) or credit_limit < 0:
            raise ValueError("信用额度必须是非负数")
        
        super().__init__(account_holder, initial_balance, account_number)
        self.credit_limit = float(credit_limit)
        self.used_credit = 0.0
    
    def _can_withdraw(self, amount: float) -> bool:
        """检查是否可以取款（重写父类方法，支持透支）
        
        Args:
            amount (float): 取款金额
        
        Returns:
            bool: 是否可以取款
        """
        available_amount = self._balance + (self.credit_limit - self.used_credit)
        return available_amount >= amount
    
    def withdraw(self, amount: float, description: str = "") -> bool:
        """取款（重写父类方法，支持透支）
        
        Args:
            amount (float): 取款金额
            description (str): 交易描述
        
        Returns:
            bool: 取款是否成功
        """
        self._check_account_status()
        self._validate_amount(amount)
        
        if not self._can_withdraw(amount):
            available = self._balance + (self.credit_limit - self.used_credit)
            print(f"取款失败！可用金额不足。可用金额：¥{available:.2f}，尝试取款：¥{amount:.2f}")
            return False
        
        if amount <= self._balance:
            # 余额足够，正常取款
            self._balance -= amount
        else:
            # 需要使用信用额度
            overdraft = amount - self._balance
            self.used_credit += overdraft
            self._balance = 0.0
            print(f"使用信用额度：¥{overdraft:.2f}")
        
        self._add_transaction(
            TransactionType.WITHDRAWAL, 
            amount, 
            description or f"取款 ¥{amount:.2f}"
        )
        
        print(f"取款成功！金额：¥{amount:.2f}，当前余额：¥{self._balance:.2f}")
        if self.used_credit > 0:
            print(f"已使用信用额度：¥{self.used_credit:.2f}")
        
        return True
    
    def deposit(self, amount: float, description: str = "") -> bool:
        """存款（重写父类方法，优先还信用额度）
        
        Args:
            amount (float): 存款金额
            description (str): 交易描述
        
        Returns:
            bool: 存款是否成功
        """
        self._check_account_status()
        self._validate_amount(amount)
        
        if self.used_credit > 0:
            # 优先还信用额度
            if amount >= self.used_credit:
                # 存款足够还清信用额度
                remaining = amount - self.used_credit
                print(f"还清信用额度：¥{self.used_credit:.2f}")
                self.used_credit = 0.0
                self._balance += remaining
            else:
                # 存款不足以还清信用额度
                self.used_credit -= amount
                print(f"部分还款信用额度：¥{amount:.2f}，剩余欠款：¥{self.used_credit:.2f}")
        else:
            # 正常存款
            self._balance += amount
        
        self._add_transaction(
            TransactionType.DEPOSIT, 
            amount, 
            description or f"存款 ¥{amount:.2f}"
        )
        
        print(f"存款成功！金额：¥{amount:.2f}，当前余额：¥{self._balance:.2f}")
        return True
    
    def get_available_credit(self) -> float:
        """获取可用信用额度
        
        Returns:
            float: 可用信用额度
        """
        return self.credit_limit - self.used_credit
    
    def get_total_available(self) -> float:
        """获取总可用金额（余额 + 可用信用额度）
        
        Returns:
            float: 总可用金额
        """
        return self._balance + self.get_available_credit()
    
    def get_account_info(self) -> str:
        """获取账户信息（重写父类方法）
        
        Returns:
            str: 格式化的账户信息
        """
        base_info = super().get_account_info()
        
        credit_info = (
            f"\n信用账户特有信息：\n"
            f"  信用额度：¥{self.credit_limit:.2f}\n"
            f"  已使用信用：¥{self.used_credit:.2f}\n"
            f"  可用信用：¥{self.get_available_credit():.2f}\n"
            f"  总可用金额：¥{self.get_total_available():.2f}"
        )
        
        return base_info + credit_info


class BankManager:
    """银行管理器类 - 管理多个账户"""
    
    def __init__(self, bank_name: str = "Python银行"):
        """初始化银行管理器
        
        Args:
            bank_name (str): 银行名称
        """
        self.bank_name = bank_name
        self.accounts: Dict[str, BankAccount] = {}
        self.created_date = datetime.now()
    
    def create_account(self, account_type: str, account_holder: str, 
                      initial_balance: float = 0.0, **kwargs) -> Optional[BankAccount]:
        """创建账户
        
        Args:
            account_type (str): 账户类型（'basic', 'savings', 'credit'）
            account_holder (str): 账户持有人
            initial_balance (float): 初始余额
            **kwargs: 其他参数
        
        Returns:
            BankAccount or None: 创建的账户对象，失败时返回None
        """
        try:
            if account_type.lower() == 'basic':
                account = BankAccount(account_holder, initial_balance)
            elif account_type.lower() == 'savings':
                interest_rate = kwargs.get('interest_rate', 0.02)
                account = SavingsAccount(account_holder, initial_balance, interest_rate)
            elif account_type.lower() == 'credit':
                credit_limit = kwargs.get('credit_limit', 1000.0)
                account = CreditAccount(account_holder, initial_balance, credit_limit)
            else:
                print(f"不支持的账户类型：{account_type}")
                return None
            
            self.accounts[account.account_number] = account
            print(f"账户创建成功：{account}")
            return account
            
        except (ValueError, TypeError) as e:
            print(f"账户创建失败：{e}")
            return None
    
    def get_account(self, account_number: str) -> Optional[BankAccount]:
        """获取账户
        
        Args:
            account_number (str): 账户号码
        
        Returns:
            BankAccount or None: 账户对象，不存在时返回None
        """
        return self.accounts.get(account_number)
    
    def list_accounts(self) -> List[BankAccount]:
        """列出所有账户
        
        Returns:
            List[BankAccount]: 账户列表
        """
        return list(self.accounts.values())
    
    def get_total_deposits(self) -> float:
        """获取总存款额
        
        Returns:
            float: 总存款额
        """
        return sum(account.balance for account in self.accounts.values())
    
    def get_bank_summary(self) -> str:
        """获取银行摘要
        
        Returns:
            str: 银行摘要信息
        """
        total_accounts = len(self.accounts)
        total_deposits = self.get_total_deposits()
        
        account_types = {}
        for account in self.accounts.values():
            account_type = account.__class__.__name__
            account_types[account_type] = account_types.get(account_type, 0) + 1
        
        summary = [
            f"银行摘要 - {self.bank_name}",
            f"创建日期：{self.created_date.strftime('%Y-%m-%d')}",
            f"总账户数：{total_accounts}",
            f"总存款额：¥{total_deposits:.2f}",
            "",
            "账户类型分布："
        ]
        
        for account_type, count in account_types.items():
            summary.append(f"  {account_type}: {count}个")
        
        return "\n".join(summary)
    
    def print_all_accounts(self) -> None:
        """打印所有账户信息"""
        if not self.accounts:
            print("暂无账户")
            return
        
        print(f"\n{self.bank_name} - 所有账户：")
        print("=" * 60)
        
        for account in sorted(self.accounts.values(), key=lambda x: x.account_number):
            print(f"\n{account}")
            print(f"状态：{account.status.value}")
            if isinstance(account, SavingsAccount):
                print(f"利率：{account.interest_rate*100:.2f}%")
            elif isinstance(account, CreditAccount):
                print(f"信用额度：¥{account.credit_limit:.2f}，已使用：¥{account.used_credit:.2f}")


def demo_bank_system():
    """演示银行账户管理系统"""
    print("=== 银行账户管理系统演示 ===")
    
    # 1. 创建银行管理器
    print("\n1. 创建银行管理器：")
    print("-" * 40)
    
    bank = BankManager("Python编程银行")
    print(f"银行管理器创建成功：{bank.bank_name}")
    
    # 2. 创建不同类型的账户
    print("\n2. 创建不同类型的账户：")
    print("-" * 40)
    
    # 创建基础账户
    basic_account = bank.create_account("basic", "张三", 1000.0)
    
    # 创建储蓄账户
    savings_account = bank.create_account("savings", "李四", 5000.0, interest_rate=0.03)
    
    # 创建信用账户
    credit_account = bank.create_account("credit", "王五", 500.0, credit_limit=2000.0)
    
    print(f"\n成功创建 {len(bank.accounts)} 个账户")
    
    # 3. 显示账户信息
    print("\n3. 账户信息：")
    print("-" * 40)
    
    accounts = [basic_account, savings_account, credit_account]
    for i, account in enumerate(accounts, 1):
        if account:
            print(f"\n账户{i}：")
            print(account.get_account_info())
    
    # 4. 测试基础操作
    print("\n4. 基础操作测试：")
    print("-" * 40)
    
    if basic_account:
        print("\n张三的基础账户操作：")
        basic_account.deposit(500, "工资存款")
        basic_account.withdraw(200, "日常消费")
        basic_account.print_transaction_history(5)
    
    # 5. 测试储蓄账户利息
    print("\n5. 储蓄账户利息测试：")
    print("-" * 40)
    
    if savings_account:
        print("\n李四的储蓄账户：")
        print(f"当前余额：¥{savings_account.balance:.2f}")
        print(f"30天预期利息：¥{savings_account.calculate_interest(30):.2f}")
        savings_account.add_interest(30)
        savings_account.print_transaction_history(3)
    
    # 6. 测试信用账户透支
    print("\n6. 信用账户透支测试：")
    print("-" * 40)
    
    if credit_account:
        print("\n王五的信用账户：")
        print(f"当前余额：¥{credit_account.balance:.2f}")
        print(f"总可用金额：¥{credit_account.get_total_available():.2f}")
        
        # 测试透支
        credit_account.withdraw(1000, "大额消费")
        print(f"透支后余额：¥{credit_account.balance:.2f}")
        print(f"已使用信用：¥{credit_account.used_credit:.2f}")
        
        # 存款还款
        credit_account.deposit(600, "还款")
        credit_account.print_transaction_history(5)
    
    # 7. 测试转账
    print("\n7. 转账测试：")
    print("-" * 40)
    
    if basic_account and savings_account:
        print("\n张三向李四转账：")
        basic_account.transfer_to(savings_account, 300, "朋友借款")
        
        print("\n转账后余额：")
        print(f"张三：¥{basic_account.balance:.2f}")
        print(f"李四：¥{savings_account.balance:.2f}")
    
    # 8. 测试账户状态管理
    print("\n8. 账户状态管理测试：")
    print("-" * 40)
    
    if basic_account:
        print("\n冻结和解冻账户：")
        basic_account.freeze_account()
        
        # 尝试在冻结状态下操作
        try:
            basic_account.deposit(100)
        except RuntimeError as e:
            print(f"操作失败：{e}")
        
        basic_account.unfreeze_account()
        basic_account.deposit(100, "解冻后存款")
    
    # 9. 银行统计
    print("\n9. 银行统计：")
    print("-" * 40)
    
    print("\n银行摘要：")
    print(bank.get_bank_summary())
    
    print("\n所有账户列表：")
    bank.print_all_accounts()
    
    # 10. 测试类方法和静态方法
    print("\n10. 类方法和静态方法测试：")
    print("-" * 40)
    
    print("\n银行信息：")
    print(BankAccount.get_bank_info())
    
    print("\n账户号码验证：")
    test_numbers = ["ACC00000001", "INVALID", "ACC123", "ACC00000999"]
    for number in test_numbers:
        is_valid = BankAccount.is_valid_account_number(number)
        print(f"  {number}: {'有效' if is_valid else '无效'}")
    
    # 11. 测试比较和排序
    print("\n11. 比较和排序测试：")
    print("-" * 40)
    
    all_accounts = [acc for acc in accounts if acc]
    if all_accounts:
        print("\n按余额排序（从低到高）：")
        sorted_accounts = sorted(all_accounts)
        for account in sorted_accounts:
            print(f"  {account}")
    
    # 12. 异常处理测试
    print("\n12. 异常处理测试：")
    print("-" * 40)
    
    try:
        # 测试无效参数
        invalid_account = BankAccount("", -100)
    except ValueError as e:
        print(f"捕获异常：{e}")
    
    try:
        # 测试无效转账
        if basic_account and savings_account:
            basic_account.transfer_to("invalid", 100)
    except TypeError as e:
        print(f"捕获异常：{e}")
    
    print("\n=== 演示完成 ===")


if __name__ == "__main__":
    demo_bank_system()