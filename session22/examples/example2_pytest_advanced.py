#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session22 示例2：pytest高级用法

演示pytest框架的高级功能，包括夹具、参数化测试、标记等。

作者: Python教程团队
创建日期: 2024-01-15
"""

import pytest
import tempfile
import os
import json
from typing import List, Dict
from unittest.mock import Mock, patch


class BankAccount:
    """银行账户类 - 用于演示复杂测试场景"""
    
    def __init__(self, account_number: str, initial_balance: float = 0):
        self.account_number = account_number
        self.balance = initial_balance
        self.transaction_history = []
        self.is_frozen = False
    
    def deposit(self, amount: float) -> bool:
        """存款"""
        if self.is_frozen:
            raise ValueError("账户已冻结")
        if amount <= 0:
            raise ValueError("存款金额必须大于0")
        
        self.balance += amount
        self.transaction_history.append({
            'type': 'deposit',
            'amount': amount,
            'balance': self.balance
        })
        return True
    
    def withdraw(self, amount: float) -> bool:
        """取款"""
        if self.is_frozen:
            raise ValueError("账户已冻结")
        if amount <= 0:
            raise ValueError("取款金额必须大于0")
        if amount > self.balance:
            raise ValueError("余额不足")
        
        self.balance -= amount
        self.transaction_history.append({
            'type': 'withdraw',
            'amount': amount,
            'balance': self.balance
        })
        return True
    
    def transfer(self, target_account: 'BankAccount', amount: float) -> bool:
        """转账"""
        self.withdraw(amount)
        target_account.deposit(amount)
        return True
    
    def freeze(self):
        """冻结账户"""
        self.is_frozen = True
    
    def unfreeze(self):
        """解冻账户"""
        self.is_frozen = False
    
    def get_balance(self) -> float:
        """获取余额"""
        return self.balance
    
    def get_transaction_history(self) -> List[Dict]:
        """获取交易历史"""
        return self.transaction_history.copy()


class NotificationService:
    """通知服务 - 用于演示Mock"""
    
    def send_sms(self, phone: str, message: str) -> bool:
        """发送短信（模拟外部服务）"""
        # 实际实现会调用外部API
        print(f"发送短信到 {phone}: {message}")
        return True
    
    def send_email(self, email: str, subject: str, body: str) -> bool:
        """发送邮件（模拟外部服务）"""
        # 实际实现会调用邮件服务
        print(f"发送邮件到 {email}: {subject}")
        return True


class BankService:
    """银行服务类 - 集成多个组件"""
    
    def __init__(self, notification_service: NotificationService):
        self.accounts = {}
        self.notification_service = notification_service
    
    def create_account(self, account_number: str, initial_balance: float = 0) -> BankAccount:
        """创建账户"""
        if account_number in self.accounts:
            raise ValueError("账户已存在")
        
        account = BankAccount(account_number, initial_balance)
        self.accounts[account_number] = account
        return account
    
    def get_account(self, account_number: str) -> BankAccount:
        """获取账户"""
        if account_number not in self.accounts:
            raise ValueError("账户不存在")
        return self.accounts[account_number]
    
    def transfer_with_notification(self, from_account: str, to_account: str, 
                                 amount: float, phone: str) -> bool:
        """转账并发送通知"""
        from_acc = self.get_account(from_account)
        to_acc = self.get_account(to_account)
        
        from_acc.transfer(to_acc, amount)
        
        # 发送通知
        message = f"您已成功转账 {amount} 元到账户 {to_account}"
        self.notification_service.send_sms(phone, message)
        
        return True


# ============ pytest夹具演示 ============

@pytest.fixture
def bank_account():
    """基本银行账户夹具"""
    return BankAccount("123456789", 1000)


@pytest.fixture
def empty_account():
    """空账户夹具"""
    return BankAccount("987654321", 0)


@pytest.fixture
def rich_account():
    """富有账户夹具"""
    account = BankAccount("111111111", 10000)
    # 添加一些交易历史
    account.deposit(5000)
    account.withdraw(2000)
    return account


@pytest.fixture(scope="session")
def temp_directory():
    """会话级别的临时目录夹具"""
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"\n创建临时目录: {temp_dir}")
        yield temp_dir
        print(f"\n清理临时目录: {temp_dir}")


@pytest.fixture(scope="module")
def notification_service():
    """模块级别的通知服务夹具"""
    print("\n创建通知服务")
    service = NotificationService()
    yield service
    print("\n清理通知服务")


@pytest.fixture
def bank_service(notification_service):
    """银行服务夹具（依赖通知服务）"""
    service = BankService(notification_service)
    # 预创建一些账户
    service.create_account("123456789", 1000)
    service.create_account("987654321", 2000)
    return service


@pytest.fixture(params=[100, 500, 1000])
def deposit_amount(request):
    """参数化夹具 - 不同的存款金额"""
    return request.param


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """自动使用的夹具 - 每个测试前后都会执行"""
    print("\n[设置] 测试开始前的准备")
    yield
    print("\n[清理] 测试结束后的清理")


# ============ 基本测试 ============

class TestBankAccount:
    """银行账户测试类"""
    
    def test_initial_balance(self, bank_account):
        """测试初始余额"""
        assert bank_account.get_balance() == 1000
        assert bank_account.account_number == "123456789"
        assert not bank_account.is_frozen
    
    def test_deposit_valid_amount(self, bank_account):
        """测试有效存款"""
        initial_balance = bank_account.get_balance()
        result = bank_account.deposit(500)
        
        assert result is True
        assert bank_account.get_balance() == initial_balance + 500
        
        # 检查交易历史
        history = bank_account.get_transaction_history()
        assert len(history) == 1
        assert history[0]['type'] == 'deposit'
        assert history[0]['amount'] == 500
    
    def test_deposit_invalid_amount(self, bank_account):
        """测试无效存款金额"""
        with pytest.raises(ValueError, match="存款金额必须大于0"):
            bank_account.deposit(-100)
        
        with pytest.raises(ValueError):
            bank_account.deposit(0)
    
    def test_withdraw_valid_amount(self, bank_account):
        """测试有效取款"""
        initial_balance = bank_account.get_balance()
        result = bank_account.withdraw(300)
        
        assert result is True
        assert bank_account.get_balance() == initial_balance - 300
    
    def test_withdraw_insufficient_funds(self, bank_account):
        """测试余额不足"""
        with pytest.raises(ValueError, match="余额不足"):
            bank_account.withdraw(2000)
    
    def test_frozen_account_operations(self, bank_account):
        """测试冻结账户操作"""
        bank_account.freeze()
        
        with pytest.raises(ValueError, match="账户已冻结"):
            bank_account.deposit(100)
        
        with pytest.raises(ValueError, match="账户已冻结"):
            bank_account.withdraw(100)
        
        # 解冻后应该可以正常操作
        bank_account.unfreeze()
        assert bank_account.deposit(100) is True


# ============ 参数化测试 ============

class TestParametrizedOperations:
    """参数化测试演示"""
    
    @pytest.mark.parametrize("amount,expected_balance", [
        (100, 1100),
        (500, 1500),
        (1000, 2000),
        (0.01, 1000.01),
    ])
    def test_deposit_amounts(self, bank_account, amount, expected_balance):
        """测试不同存款金额"""
        bank_account.deposit(amount)
        assert bank_account.get_balance() == expected_balance
    
    @pytest.mark.parametrize("withdraw_amount", [100, 500, 999.99])
    def test_valid_withdrawals(self, bank_account, withdraw_amount):
        """测试有效取款金额"""
        initial_balance = bank_account.get_balance()
        bank_account.withdraw(withdraw_amount)
        assert bank_account.get_balance() == initial_balance - withdraw_amount
    
    @pytest.mark.parametrize("invalid_amount,error_message", [
        (-100, "取款金额必须大于0"),
        (0, "取款金额必须大于0"),
        (2000, "余额不足"),
    ])
    def test_invalid_withdrawals(self, bank_account, invalid_amount, error_message):
        """测试无效取款"""
        with pytest.raises(ValueError, match=error_message):
            bank_account.withdraw(invalid_amount)
    
    def test_parametrized_fixture(self, empty_account, deposit_amount):
        """使用参数化夹具"""
        empty_account.deposit(deposit_amount)
        assert empty_account.get_balance() == deposit_amount


# ============ Mock和补丁测试 ============

class TestBankServiceWithMocks:
    """使用Mock的银行服务测试"""
    
    def test_transfer_with_mock_notification(self):
        """测试转账并模拟通知服务"""
        # 创建Mock通知服务
        mock_notification = Mock(spec=NotificationService)
        mock_notification.send_sms.return_value = True
        
        # 创建银行服务
        bank_service = BankService(mock_notification)
        bank_service.create_account("123", 1000)
        bank_service.create_account("456", 500)
        
        # 执行转账
        result = bank_service.transfer_with_notification("123", "456", 200, "13800138000")
        
        # 验证结果
        assert result is True
        assert bank_service.get_account("123").get_balance() == 800
        assert bank_service.get_account("456").get_balance() == 700
        
        # 验证Mock调用
        mock_notification.send_sms.assert_called_once_with(
            "13800138000", "您已成功转账 200 元到账户 456"
        )
    
    @patch('example2_pytest_advanced.NotificationService')
    def test_transfer_with_patch(self, mock_notification_class):
        """使用patch装饰器测试"""
        # 配置Mock
        mock_instance = mock_notification_class.return_value
        mock_instance.send_sms.return_value = True
        
        # 创建服务（会使用Mock的NotificationService）
        notification_service = NotificationService()
        bank_service = BankService(notification_service)
        bank_service.create_account("123", 1000)
        bank_service.create_account("456", 500)
        
        # 执行转账
        result = bank_service.transfer_with_notification("123", "456", 300, "13900139000")
        
        # 验证Mock被正确调用
        assert result is True
        mock_instance.send_sms.assert_called_once()
    
    def test_mock_side_effect(self):
        """测试Mock的副作用"""
        mock_notification = Mock()
        
        # 设置副作用：第一次调用成功，第二次失败
        mock_notification.send_sms.side_effect = [True, Exception("网络错误")]
        
        bank_service = BankService(mock_notification)
        bank_service.create_account("123", 1000)
        bank_service.create_account("456", 500)
        
        # 第一次调用成功
        result1 = bank_service.transfer_with_notification("123", "456", 100, "13800138000")
        assert result1 is True
        
        # 第二次调用会抛出异常
        with pytest.raises(Exception, match="网络错误"):
            bank_service.transfer_with_notification("456", "123", 50, "13900139000")


# ============ 测试标记 ============

@pytest.mark.slow
class TestSlowOperations:
    """慢速测试标记演示"""
    
    def test_large_transaction_history(self, empty_account):
        """测试大量交易历史"""
        # 模拟大量交易
        for i in range(1000):
            empty_account.deposit(1)
        
        history = empty_account.get_transaction_history()
        assert len(history) == 1000
        assert empty_account.get_balance() == 1000


@pytest.mark.integration
class TestIntegration:
    """集成测试标记演示"""
    
    def test_full_banking_workflow(self, temp_directory):
        """测试完整的银行业务流程"""
        # 创建服务
        notification_service = NotificationService()
        bank_service = BankService(notification_service)
        
        # 创建账户
        acc1 = bank_service.create_account("ACC001", 5000)
        acc2 = bank_service.create_account("ACC002", 1000)
        
        # 执行多种操作
        acc1.deposit(1000)
        acc1.withdraw(500)
        acc1.transfer(acc2, 2000)
        
        # 验证最终状态
        assert acc1.get_balance() == 3500  # 5000 + 1000 - 500 - 2000
        assert acc2.get_balance() == 3000  # 1000 + 2000
        
        # 保存交易记录到文件
        history_file = os.path.join(temp_directory, "transaction_history.json")
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump({
                'acc1_history': acc1.get_transaction_history(),
                'acc2_history': acc2.get_transaction_history()
            }, f, ensure_ascii=False, indent=2)
        
        # 验证文件存在
        assert os.path.exists(history_file)


@pytest.mark.skip(reason="功能尚未实现")
class TestFutureFeatures:
    """跳过测试演示"""
    
    def test_cryptocurrency_support(self):
        """测试加密货币支持（未实现）"""
        pass


@pytest.mark.xfail(reason="已知的bug")
class TestKnownIssues:
    """预期失败测试演示"""
    
    def test_negative_balance_bug(self, bank_account):
        """测试负余额bug（已知问题）"""
        # 这个测试预期会失败，因为存在已知bug
        bank_account.withdraw(2000)  # 应该抛出异常但可能不会
        assert bank_account.get_balance() >= 0


# ============ 自定义标记 ============

@pytest.mark.unit
class TestUnitTests:
    """单元测试标记"""
    
    def test_account_creation(self):
        """测试账户创建"""
        account = BankAccount("TEST123", 100)
        assert account.account_number == "TEST123"
        assert account.get_balance() == 100


# ============ 测试配置和运行 ============

def test_with_custom_marker():
    """自定义标记测试"""
    pass


# 为测试添加自定义标记
pytest.mark.custom = pytest.mark.custom


@pytest.mark.custom
def test_custom_marked():
    """自定义标记的测试"""
    assert True


if __name__ == "__main__":
    # 运行测试的示例命令
    print("Session22 示例2: pytest高级用法")
    print("=" * 50)
    print("\n运行测试的命令示例:")
    print("1. 运行所有测试: pytest example2_pytest_advanced.py -v")
    print("2. 运行特定标记: pytest example2_pytest_advanced.py -m slow")
    print("3. 跳过慢速测试: pytest example2_pytest_advanced.py -m 'not slow'")
    print("4. 运行集成测试: pytest example2_pytest_advanced.py -m integration")
    print("5. 显示覆盖率: pytest example2_pytest_advanced.py --cov=.")
    print("6. 并行运行: pytest example2_pytest_advanced.py -n auto")
    print("\n学习要点:")
    print("- 使用@pytest.fixture创建测试夹具")
    print("- @pytest.mark.parametrize进行参数化测试")
    print("- 使用Mock模拟外部依赖")
    print("- 通过标记组织和筛选测试")
    print("- 夹具的作用域和依赖关系")