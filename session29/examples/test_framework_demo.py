#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session29 Examples: 测试框架演示

本文件演示了各种测试框架和技术的使用方法：
- unittest基础用法
- pytest高级功能
- 参数化测试
- 测试夹具(fixtures)
- 模拟测试(mocking)

作者: Python教程团队
"""

import unittest
import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict
import requests
import json


# 被测试的类
class BankAccount:
    """银行账户类"""
    
    def __init__(self, account_number: str, initial_balance: float = 0):
        self.account_number = account_number
        self.balance = initial_balance
        self.transaction_history = []
    
    def deposit(self, amount: float) -> bool:
        """存款"""
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
    
    def get_balance(self) -> float:
        """获取余额"""
        return self.balance
    
    def get_transaction_history(self) -> List[Dict]:
        """获取交易历史"""
        return self.transaction_history.copy()


class WeatherService:
    """天气服务类 - 用于演示API模拟"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.weather.com"
    
    def get_weather(self, city: str) -> Dict:
        """获取天气信息"""
        url = f"{self.base_url}/weather"
        params = {
            'key': self.api_key,
            'city': city,
            'format': 'json'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def get_forecast(self, city: str, days: int = 5) -> List[Dict]:
        """获取天气预报"""
        url = f"{self.base_url}/forecast"
        params = {
            'key': self.api_key,
            'city': city,
            'days': days,
            'format': 'json'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        return response.json()['forecast']


# ============================================================================
# unittest 测试示例
# ============================================================================

class TestBankAccountUnittest(unittest.TestCase):
    """使用unittest测试银行账户类"""
    
    def setUp(self):
        """每个测试方法执行前的准备工作"""
        self.account = BankAccount("123456789", 1000.0)
    
    def tearDown(self):
        """每个测试方法执行后的清理工作"""
        # 在这里可以进行清理工作
        pass
    
    def test_initial_balance(self):
        """测试初始余额"""
        self.assertEqual(self.account.get_balance(), 1000.0)
        self.assertEqual(self.account.account_number, "123456789")
    
    def test_deposit_success(self):
        """测试成功存款"""
        result = self.account.deposit(500.0)
        self.assertTrue(result)
        self.assertEqual(self.account.get_balance(), 1500.0)
        
        # 检查交易历史
        history = self.account.get_transaction_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['type'], 'deposit')
        self.assertEqual(history[0]['amount'], 500.0)
    
    def test_deposit_invalid_amount(self):
        """测试无效存款金额"""
        with self.assertRaises(ValueError) as context:
            self.account.deposit(-100.0)
        
        self.assertIn("存款金额必须大于0", str(context.exception))
        self.assertEqual(self.account.get_balance(), 1000.0)  # 余额不变
    
    def test_withdraw_success(self):
        """测试成功取款"""
        result = self.account.withdraw(300.0)
        self.assertTrue(result)
        self.assertEqual(self.account.get_balance(), 700.0)
    
    def test_withdraw_insufficient_funds(self):
        """测试余额不足"""
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(1500.0)
        
        self.assertIn("余额不足", str(context.exception))
        self.assertEqual(self.account.get_balance(), 1000.0)  # 余额不变
    
    def test_multiple_transactions(self):
        """测试多次交易"""
        self.account.deposit(200.0)
        self.account.withdraw(150.0)
        self.account.deposit(100.0)
        
        self.assertEqual(self.account.get_balance(), 1150.0)
        
        history = self.account.get_transaction_history()
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0]['type'], 'deposit')
        self.assertEqual(history[1]['type'], 'withdraw')
        self.assertEqual(history[2]['type'], 'deposit')


class TestWeatherServiceUnittest(unittest.TestCase):
    """使用unittest和mock测试天气服务"""
    
    def setUp(self):
        """测试准备"""
        self.weather_service = WeatherService("test_api_key")
    
    @patch('requests.get')
    def test_get_weather_success(self, mock_get):
        """测试成功获取天气信息"""
        # 设置模拟响应
        mock_response = Mock()
        mock_response.json.return_value = {
            'city': 'Beijing',
            'temperature': 25,
            'humidity': 60,
            'description': 'Sunny'
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # 执行测试
        result = self.weather_service.get_weather('Beijing')
        
        # 验证结果
        self.assertEqual(result['city'], 'Beijing')
        self.assertEqual(result['temperature'], 25)
        
        # 验证API调用
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        self.assertIn('Beijing', str(call_args))
        self.assertIn('test_api_key', str(call_args))
    
    @patch('requests.get')
    def test_get_weather_api_error(self, mock_get):
        """测试API错误"""
        # 设置模拟响应为错误
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("API Error")
        mock_get.return_value = mock_response
        
        # 执行测试并验证异常
        with self.assertRaises(requests.HTTPError):
            self.weather_service.get_weather('InvalidCity')
    
    @patch('requests.get')
    def test_get_forecast_success(self, mock_get):
        """测试成功获取天气预报"""
        # 设置模拟响应
        mock_response = Mock()
        mock_response.json.return_value = {
            'forecast': [
                {'date': '2024-01-01', 'temperature': 20, 'description': 'Sunny'},
                {'date': '2024-01-02', 'temperature': 18, 'description': 'Cloudy'},
                {'date': '2024-01-03', 'temperature': 22, 'description': 'Rainy'}
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # 执行测试
        result = self.weather_service.get_forecast('Shanghai', 3)
        
        # 验证结果
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['date'], '2024-01-01')
        self.assertEqual(result[1]['temperature'], 18)


# ============================================================================
# pytest 测试示例（需要安装pytest: pip install pytest）
# ============================================================================

class TestBankAccountPytest:
    """使用pytest测试银行账户类"""
    
    def setup_method(self):
        """每个测试方法执行前的准备工作"""
        self.account = BankAccount("987654321", 2000.0)
    
    def test_initial_state(self):
        """测试初始状态"""
        assert self.account.get_balance() == 2000.0
        assert self.account.account_number == "987654321"
        assert len(self.account.get_transaction_history()) == 0
    
    @pytest.mark.parametrize("amount,expected_balance", [
        (100.0, 2100.0),
        (500.0, 2500.0),
        (1000.0, 3000.0),
        (0.01, 2000.01)
    ])
    def test_deposit_amounts(self, amount, expected_balance):
        """参数化测试不同存款金额"""
        self.account.deposit(amount)
        assert self.account.get_balance() == expected_balance
    
    @pytest.mark.parametrize("invalid_amount", [
        -100.0,
        -0.01,
        0.0
    ])
    def test_deposit_invalid_amounts(self, invalid_amount):
        """参数化测试无效存款金额"""
        with pytest.raises(ValueError, match="存款金额必须大于0"):
            self.account.deposit(invalid_amount)
    
    def test_withdraw_success(self):
        """测试成功取款"""
        result = self.account.withdraw(800.0)
        assert result is True
        assert self.account.get_balance() == 1200.0
    
    def test_withdraw_all_balance(self):
        """测试取出全部余额"""
        self.account.withdraw(2000.0)
        assert self.account.get_balance() == 0.0
    
    @pytest.mark.parametrize("withdraw_amount", [
        2001.0,  # 超出余额1元
        3000.0,  # 超出余额很多
        10000.0  # 超出余额更多
    ])
    def test_withdraw_insufficient_funds(self, withdraw_amount):
        """参数化测试余额不足情况"""
        with pytest.raises(ValueError, match="余额不足"):
            self.account.withdraw(withdraw_amount)
        
        # 确保余额没有变化
        assert self.account.get_balance() == 2000.0


# pytest fixtures 示例
@pytest.fixture
def sample_account():
    """创建示例账户的fixture"""
    account = BankAccount("FIXTURE123", 5000.0)
    account.deposit(1000.0)  # 预先存入1000元
    return account


@pytest.fixture
def mock_weather_api():
    """模拟天气API的fixture"""
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {
            'city': 'Test City',
            'temperature': 25,
            'humidity': 50,
            'description': 'Clear'
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        yield mock_get


class TestWithFixtures:
    """使用fixtures的测试"""
    
    def test_account_with_fixture(self, sample_account):
        """使用账户fixture的测试"""
        # fixture已经预先存入了1000元
        assert sample_account.get_balance() == 6000.0
        
        # 继续测试
        sample_account.withdraw(2000.0)
        assert sample_account.get_balance() == 4000.0
    
    def test_weather_with_fixture(self, mock_weather_api):
        """使用天气API fixture的测试"""
        weather_service = WeatherService("test_key")
        result = weather_service.get_weather("Test City")
        
        assert result['city'] == 'Test City'
        assert result['temperature'] == 25
        
        # 验证API被调用
        mock_weather_api.assert_called_once()


# ============================================================================
# 高级Mock技术演示
# ============================================================================

class DatabaseConnection:
    """数据库连接类 - 用于演示高级Mock"""
    
    def __init__(self, host: str, port: int, database: str):
        self.host = host
        self.port = port
        self.database = database
        self.connected = False
    
    def connect(self):
        """连接数据库"""
        # 模拟连接过程
        if self.host and self.port and self.database:
            self.connected = True
            return True
        return False
    
    def execute_query(self, query: str) -> List[Dict]:
        """执行查询"""
        if not self.connected:
            raise RuntimeError("数据库未连接")
        
        # 模拟查询执行
        if "SELECT" in query.upper():
            return [{'id': 1, 'name': 'test'}]
        return []
    
    def close(self):
        """关闭连接"""
        self.connected = False


class UserRepository:
    """用户仓库类 - 使用数据库连接"""
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
    
    def get_user_by_id(self, user_id: int) -> Dict:
        """根据ID获取用户"""
        query = f"SELECT * FROM users WHERE id = {user_id}"
        results = self.db.execute_query(query)
        return results[0] if results else None
    
    def create_user(self, user_data: Dict) -> Dict:
        """创建用户"""
        query = f"INSERT INTO users (name, email) VALUES ('{user_data['name']}', '{user_data['email']}')"
        self.db.execute_query(query)
        return {'id': 1, **user_data}


class TestAdvancedMocking(unittest.TestCase):
    """高级Mock技术测试"""
    
    def test_mock_with_side_effect(self):
        """测试使用side_effect的Mock"""
        # 创建Mock对象
        mock_db = Mock(spec=DatabaseConnection)
        
        # 设置side_effect来模拟不同的返回值
        mock_db.execute_query.side_effect = [
            [{'id': 1, 'name': 'Alice'}],  # 第一次调用返回Alice
            [{'id': 2, 'name': 'Bob'}],    # 第二次调用返回Bob
            []                              # 第三次调用返回空列表
        ]
        
        repo = UserRepository(mock_db)
        
        # 测试多次调用
        user1 = repo.get_user_by_id(1)
        user2 = repo.get_user_by_id(2)
        user3 = repo.get_user_by_id(3)
        
        self.assertEqual(user1['name'], 'Alice')
        self.assertEqual(user2['name'], 'Bob')
        self.assertIsNone(user3)
        
        # 验证调用次数
        self.assertEqual(mock_db.execute_query.call_count, 3)
    
    def test_mock_with_exception(self):
        """测试Mock抛出异常"""
        mock_db = Mock(spec=DatabaseConnection)
        mock_db.connected = False
        mock_db.execute_query.side_effect = RuntimeError("数据库未连接")
        
        repo = UserRepository(mock_db)
        
        with self.assertRaises(RuntimeError) as context:
            repo.get_user_by_id(1)
        
        self.assertIn("数据库未连接", str(context.exception))
    
    def test_mock_property_and_method(self):
        """测试Mock属性和方法"""
        mock_db = MagicMock(spec=DatabaseConnection)
        
        # 设置属性
        mock_db.connected = True
        mock_db.host = "localhost"
        mock_db.port = 5432
        
        # 设置方法返回值
        mock_db.connect.return_value = True
        mock_db.execute_query.return_value = [{'id': 1, 'name': 'Test User'}]
        
        # 测试
        self.assertTrue(mock_db.connected)
        self.assertEqual(mock_db.host, "localhost")
        
        result = mock_db.connect()
        self.assertTrue(result)
        
        query_result = mock_db.execute_query("SELECT * FROM users")
        self.assertEqual(len(query_result), 1)
        self.assertEqual(query_result[0]['name'], 'Test User')
    
    @patch.object(DatabaseConnection, 'execute_query')
    @patch.object(DatabaseConnection, 'connect')
    def test_patch_object_decorator(self, mock_connect, mock_execute):
        """测试使用patch.object装饰器"""
        # 设置Mock行为
        mock_connect.return_value = True
        mock_execute.return_value = [{'id': 1, 'name': 'Patched User'}]
        
        # 创建真实对象（但方法被Mock替换）
        db = DatabaseConnection("localhost", 5432, "testdb")
        repo = UserRepository(db)
        
        # 测试
        db.connect()
        user = repo.get_user_by_id(1)
        
        self.assertEqual(user['name'], 'Patched User')
        
        # 验证Mock被调用
        mock_connect.assert_called_once()
        mock_execute.assert_called_once()


def run_unittest_examples():
    """运行unittest示例"""
    print("\n" + "="*50)
    print("运行unittest测试示例")
    print("="*50)
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestBankAccountUnittest))
    suite.addTests(loader.loadTestsFromTestCase(TestWeatherServiceUnittest))
    suite.addTests(loader.loadTestsFromTestCase(TestAdvancedMocking))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


def run_pytest_examples():
    """运行pytest示例（需要安装pytest）"""
    print("\n" + "="*50)
    print("pytest测试示例")
    print("="*50)
    
    print("要运行pytest测试，请在命令行执行：")
    print("pip install pytest")
    print("pytest test_framework_demo.py -v")
    print("")
    print("pytest特性：")
    print("- 更简洁的断言语法（assert）")
    print("- 强大的参数化测试（@pytest.mark.parametrize）")
    print("- 灵活的fixture系统")
    print("- 丰富的插件生态")
    print("- 更好的错误报告")


if __name__ == "__main__":
    print("测试框架演示")
    
    # 运行unittest示例
    unittest_result = run_unittest_examples()
    
    # 显示pytest信息
    run_pytest_examples()
    
    print("\n" + "="*50)
    print("测试框架演示完成")
    print("="*50)
    
    print("\n学习要点：")
    print("1. unittest是Python标准库，无需额外安装")
    print("2. pytest提供更现代化的测试体验")
    print("3. Mock对象用于隔离外部依赖")
    print("4. 参数化测试可以减少重复代码")
    print("5. Fixtures提供测试数据和环境准备")
    print("6. 合理使用断言验证测试结果")