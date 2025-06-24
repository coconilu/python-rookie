#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session22 示例3：Mock和测试替身详解

演示unittest.mock的各种用法，包括Mock、MagicMock、patch等。

作者: Python教程团队
创建日期: 2024-01-15
"""

import unittest
from unittest.mock import Mock, MagicMock, patch, call, PropertyMock
import requests
import json
import os
from datetime import datetime
from typing import Dict, List, Optional


# ============ 被测试的类 ============

class DatabaseConnection:
    """数据库连接类（模拟）"""
    
    def __init__(self, host: str, port: int, database: str):
        self.host = host
        self.port = port
        self.database = database
        self.connected = False
    
    def connect(self) -> bool:
        """连接数据库"""
        # 模拟连接过程
        print(f"连接到数据库 {self.host}:{self.port}/{self.database}")
        self.connected = True
        return True
    
    def disconnect(self) -> bool:
        """断开连接"""
        print("断开数据库连接")
        self.connected = False
        return True
    
    def execute_query(self, sql: str) -> List[Dict]:
        """执行查询"""
        if not self.connected:
            raise RuntimeError("数据库未连接")
        
        # 模拟查询执行
        print(f"执行SQL: {sql}")
        return [{'id': 1, 'name': 'test'}]
    
    def execute_update(self, sql: str) -> int:
        """执行更新"""
        if not self.connected:
            raise RuntimeError("数据库未连接")
        
        print(f"执行更新SQL: {sql}")
        return 1  # 返回影响的行数


class EmailService:
    """邮件服务类"""
    
    def __init__(self, smtp_server: str, port: int):
        self.smtp_server = smtp_server
        self.port = port
    
    def send_email(self, to: str, subject: str, body: str) -> bool:
        """发送邮件"""
        print(f"发送邮件到 {to}: {subject}")
        # 实际实现会连接SMTP服务器
        return True
    
    def send_bulk_email(self, recipients: List[str], subject: str, body: str) -> Dict[str, bool]:
        """批量发送邮件"""
        results = {}
        for recipient in recipients:
            results[recipient] = self.send_email(recipient, subject, body)
        return results


class WeatherAPI:
    """天气API服务"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.weather.com"
    
    def get_current_weather(self, city: str) -> Dict:
        """获取当前天气"""
        url = f"{self.base_url}/current"
        params = {
            'key': self.api_key,
            'city': city
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_forecast(self, city: str, days: int = 7) -> Dict:
        """获取天气预报"""
        url = f"{self.base_url}/forecast"
        params = {
            'key': self.api_key,
            'city': city,
            'days': days
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()


class UserService:
    """用户服务类"""
    
    def __init__(self, db_connection: DatabaseConnection, email_service: EmailService):
        self.db = db_connection
        self.email_service = email_service
    
    def create_user(self, username: str, email: str, password: str) -> Dict:
        """创建用户"""
        # 检查用户是否已存在
        existing_users = self.db.execute_query(
            f"SELECT * FROM users WHERE username='{username}' OR email='{email}'"
        )
        
        if existing_users:
            raise ValueError("用户名或邮箱已存在")
        
        # 创建用户
        user_id = self.db.execute_update(
            f"INSERT INTO users (username, email, password) VALUES ('{username}', '{email}', '{password}')"
        )
        
        # 发送欢迎邮件
        welcome_subject = "欢迎注册我们的服务"
        welcome_body = f"亲爱的 {username}，欢迎加入我们！"
        self.email_service.send_email(email, welcome_subject, welcome_body)
        
        return {
            'id': user_id,
            'username': username,
            'email': email,
            'created_at': datetime.now().isoformat()
        }
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """获取用户信息"""
        users = self.db.execute_query(f"SELECT * FROM users WHERE id={user_id}")
        return users[0] if users else None
    
    def delete_user(self, user_id: int) -> bool:
        """删除用户"""
        affected_rows = self.db.execute_update(f"DELETE FROM users WHERE id={user_id}")
        return affected_rows > 0


class WeatherReportService:
    """天气报告服务"""
    
    def __init__(self, weather_api: WeatherAPI, email_service: EmailService):
        self.weather_api = weather_api
        self.email_service = email_service
    
    def send_weather_report(self, city: str, email: str) -> bool:
        """发送天气报告"""
        try:
            # 获取天气数据
            current_weather = self.weather_api.get_current_weather(city)
            forecast = self.weather_api.get_forecast(city, 3)
            
            # 生成报告
            subject = f"{city}天气报告"
            body = self._generate_report_body(current_weather, forecast)
            
            # 发送邮件
            return self.email_service.send_email(email, subject, body)
        
        except Exception as e:
            print(f"发送天气报告失败: {e}")
            return False
    
    def _generate_report_body(self, current: Dict, forecast: Dict) -> str:
        """生成报告内容"""
        return f"当前温度: {current.get('temperature', 'N/A')}°C\n预报: {forecast.get('summary', 'N/A')}"


# ============ Mock基础测试 ============

class TestMockBasics(unittest.TestCase):
    """Mock基础用法测试"""
    
    def test_basic_mock(self):
        """基本Mock用法"""
        # 创建Mock对象
        mock_obj = Mock()
        
        # 设置返回值
        mock_obj.some_method.return_value = "mocked result"
        
        # 调用并验证
        result = mock_obj.some_method()
        self.assertEqual(result, "mocked result")
        
        # 验证调用
        mock_obj.some_method.assert_called_once()
    
    def test_mock_with_spec(self):
        """使用spec的Mock"""
        # 创建具有规范的Mock
        mock_db = Mock(spec=DatabaseConnection)
        
        # 可以调用规范中存在的方法
        mock_db.connect.return_value = True
        result = mock_db.connect()
        self.assertTrue(result)
        
        # 尝试调用不存在的方法会报错
        with self.assertRaises(AttributeError):
            mock_db.nonexistent_method()
    
    def test_mock_side_effect(self):
        """Mock副作用测试"""
        mock_obj = Mock()
        
        # 设置副作用：抛出异常
        mock_obj.risky_method.side_effect = RuntimeError("Something went wrong")
        
        with self.assertRaises(RuntimeError):
            mock_obj.risky_method()
        
        # 设置副作用：多次调用返回不同值
        mock_obj.counter.side_effect = [1, 2, 3]
        
        self.assertEqual(mock_obj.counter(), 1)
        self.assertEqual(mock_obj.counter(), 2)
        self.assertEqual(mock_obj.counter(), 3)
    
    def test_mock_call_tracking(self):
        """Mock调用跟踪测试"""
        mock_obj = Mock()
        
        # 进行一些调用
        mock_obj.method1("arg1", "arg2")
        mock_obj.method1("arg3", keyword="value")
        mock_obj.method2()
        
        # 验证调用次数
        self.assertEqual(mock_obj.method1.call_count, 2)
        self.assertEqual(mock_obj.method2.call_count, 1)
        
        # 验证调用参数
        mock_obj.method1.assert_has_calls([
            call("arg1", "arg2"),
            call("arg3", keyword="value")
        ])
        
        # 验证最后一次调用
        mock_obj.method1.assert_called_with("arg3", keyword="value")


# ============ patch装饰器测试 ============

class TestPatchDecorator(unittest.TestCase):
    """patch装饰器用法测试"""
    
    @patch('requests.get')
    def test_weather_api_with_patch(self, mock_get):
        """使用patch测试WeatherAPI"""
        # 设置Mock响应
        mock_response = Mock()
        mock_response.json.return_value = {
            'temperature': 25,
            'humidity': 60,
            'description': 'sunny'
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # 测试WeatherAPI
        api = WeatherAPI("test_key")
        result = api.get_current_weather("Beijing")
        
        # 验证结果
        self.assertEqual(result['temperature'], 25)
        self.assertEqual(result['description'], 'sunny')
        
        # 验证requests.get被正确调用
        mock_get.assert_called_once_with(
            "https://api.weather.com/current",
            params={'key': 'test_key', 'city': 'Beijing'}
        )
    
    @patch('example3_mock_and_patch.EmailService')
    @patch('example3_mock_and_patch.DatabaseConnection')
    def test_user_service_create_user(self, mock_db_class, mock_email_class):
        """测试用户服务创建用户"""
        # 设置Mock实例
        mock_db = mock_db_class.return_value
        mock_email = mock_email_class.return_value
        
        # 配置Mock行为
        mock_db.execute_query.return_value = []  # 用户不存在
        mock_db.execute_update.return_value = 123  # 返回用户ID
        mock_email.send_email.return_value = True
        
        # 创建服务并测试
        service = UserService(mock_db, mock_email)
        result = service.create_user("testuser", "test@example.com", "password123")
        
        # 验证结果
        self.assertEqual(result['id'], 123)
        self.assertEqual(result['username'], "testuser")
        
        # 验证Mock调用
        mock_db.execute_query.assert_called_once()
        mock_db.execute_update.assert_called_once()
        mock_email.send_email.assert_called_once_with(
            "test@example.com", "欢迎注册我们的服务", "亲爱的 testuser，欢迎加入我们！"
        )
    
    def test_patch_as_context_manager(self):
        """使用patch作为上下文管理器"""
        with patch('requests.get') as mock_get:
            # 设置Mock
            mock_response = Mock()
            mock_response.json.return_value = {'forecast': 'rainy'}
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            # 测试
            api = WeatherAPI("test_key")
            result = api.get_forecast("Shanghai", 5)
            
            # 验证
            self.assertEqual(result['forecast'], 'rainy')
            mock_get.assert_called_once()
    
    @patch.object(DatabaseConnection, 'execute_query')
    def test_patch_object(self, mock_execute_query):
        """使用patch.object"""
        # 设置Mock返回值
        mock_execute_query.return_value = [{'id': 1, 'username': 'testuser'}]
        
        # 创建真实的数据库连接对象
        db = DatabaseConnection("localhost", 5432, "testdb")
        db.connected = True  # 模拟已连接状态
        
        # 调用方法
        result = db.execute_query("SELECT * FROM users")
        
        # 验证
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['username'], 'testuser')
        mock_execute_query.assert_called_once_with("SELECT * FROM users")


# ============ MagicMock测试 ============

class TestMagicMock(unittest.TestCase):
    """MagicMock用法测试"""
    
    def test_magic_mock_basics(self):
        """MagicMock基础用法"""
        mock_obj = MagicMock()
        
        # MagicMock支持魔术方法
        mock_obj.__len__.return_value = 5
        mock_obj.__getitem__.return_value = "mocked_item"
        
        # 测试魔术方法
        self.assertEqual(len(mock_obj), 5)
        self.assertEqual(mock_obj[0], "mocked_item")
        
        # 验证调用
        mock_obj.__len__.assert_called_once()
        mock_obj.__getitem__.assert_called_once_with(0)
    
    def test_magic_mock_with_iteration(self):
        """MagicMock迭代测试"""
        mock_obj = MagicMock()
        
        # 设置迭代行为
        mock_obj.__iter__.return_value = iter([1, 2, 3])
        
        # 测试迭代
        result = list(mock_obj)
        self.assertEqual(result, [1, 2, 3])
    
    def test_magic_mock_context_manager(self):
        """MagicMock上下文管理器测试"""
        mock_obj = MagicMock()
        
        # 使用as上下文管理器
        with mock_obj as context:
            context.do_something()
        
        # 验证上下文管理器方法被调用
        mock_obj.__enter__.assert_called_once()
        mock_obj.__exit__.assert_called_once()
        mock_obj.__enter__.return_value.do_something.assert_called_once()


# ============ 属性Mock测试 ============

class TestPropertyMock(unittest.TestCase):
    """PropertyMock用法测试"""
    
    def test_property_mock(self):
        """PropertyMock基础用法"""
        with patch.object(DatabaseConnection, 'connected', new_callable=PropertyMock) as mock_connected:
            mock_connected.return_value = True
            
            db = DatabaseConnection("localhost", 5432, "testdb")
            
            # 测试属性访问
            self.assertTrue(db.connected)
            
            # 验证属性被访问
            mock_connected.assert_called_once()
    
    @patch('example3_mock_and_patch.datetime')
    def test_mock_datetime(self, mock_datetime):
        """Mock datetime模块"""
        # 设置固定的时间
        fixed_time = datetime(2024, 1, 15, 12, 0, 0)
        mock_datetime.now.return_value = fixed_time
        
        # 创建用户服务（需要Mock其他依赖）
        mock_db = Mock(spec=DatabaseConnection)
        mock_email = Mock(spec=EmailService)
        mock_db.execute_query.return_value = []
        mock_db.execute_update.return_value = 1
        mock_email.send_email.return_value = True
        
        service = UserService(mock_db, mock_email)
        result = service.create_user("testuser", "test@example.com", "password")
        
        # 验证时间戳
        self.assertEqual(result['created_at'], fixed_time.isoformat())


# ============ 复杂场景测试 ============

class TestComplexScenarios(unittest.TestCase):
    """复杂场景Mock测试"""
    
    @patch('example3_mock_and_patch.EmailService')
    @patch('example3_mock_and_patch.WeatherAPI')
    def test_weather_report_service(self, mock_weather_api_class, mock_email_class):
        """测试天气报告服务"""
        # 设置Mock实例
        mock_weather_api = mock_weather_api_class.return_value
        mock_email = mock_email_class.return_value
        
        # 配置天气API Mock
        mock_weather_api.get_current_weather.return_value = {
            'temperature': 22,
            'humidity': 65
        }
        mock_weather_api.get_forecast.return_value = {
            'summary': '未来三天多云'
        }
        
        # 配置邮件服务Mock
        mock_email.send_email.return_value = True
        
        # 创建服务并测试
        service = WeatherReportService(mock_weather_api, mock_email)
        result = service.send_weather_report("Beijing", "user@example.com")
        
        # 验证结果
        self.assertTrue(result)
        
        # 验证API调用
        mock_weather_api.get_current_weather.assert_called_once_with("Beijing")
        mock_weather_api.get_forecast.assert_called_once_with("Beijing", 3)
        
        # 验证邮件发送
        mock_email.send_email.assert_called_once()
        call_args = mock_email.send_email.call_args
        self.assertEqual(call_args[0][0], "user@example.com")  # 收件人
        self.assertEqual(call_args[0][1], "Beijing天气报告")  # 主题
        self.assertIn("22°C", call_args[0][2])  # 邮件内容包含温度
    
    @patch('example3_mock_and_patch.WeatherAPI')
    def test_weather_report_service_api_failure(self, mock_weather_api_class):
        """测试天气API失败场景"""
        # 设置API抛出异常
        mock_weather_api = mock_weather_api_class.return_value
        mock_weather_api.get_current_weather.side_effect = requests.RequestException("API Error")
        
        # 创建邮件服务Mock
        mock_email = Mock(spec=EmailService)
        
        # 创建服务并测试
        service = WeatherReportService(mock_weather_api, mock_email)
        result = service.send_weather_report("Beijing", "user@example.com")
        
        # 验证失败结果
        self.assertFalse(result)
        
        # 验证邮件没有发送
        mock_email.send_email.assert_not_called()
    
    def test_mock_chaining(self):
        """测试Mock链式调用"""
        mock_obj = Mock()
        
        # 设置链式调用
        mock_obj.get_connection.return_value.execute.return_value.fetchall.return_value = [
            {'id': 1, 'name': 'test'}
        ]
        
        # 执行链式调用
        result = mock_obj.get_connection().execute("SELECT * FROM users").fetchall()
        
        # 验证结果
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'test')
        
        # 验证调用链
        mock_obj.get_connection.assert_called_once()
        mock_obj.get_connection.return_value.execute.assert_called_once_with("SELECT * FROM users")
        mock_obj.get_connection.return_value.execute.return_value.fetchall.assert_called_once()


# ============ Mock最佳实践 ============

class TestMockBestPractices(unittest.TestCase):
    """Mock最佳实践演示"""
    
    def test_mock_return_value_vs_side_effect(self):
        """return_value vs side_effect的区别"""
        mock_obj = Mock()
        
        # return_value：每次调用返回相同值
        mock_obj.method1.return_value = "fixed_value"
        self.assertEqual(mock_obj.method1(), "fixed_value")
        self.assertEqual(mock_obj.method1(), "fixed_value")
        
        # side_effect：可以返回不同值或抛出异常
        mock_obj.method2.side_effect = ["first", "second", Exception("error")]
        self.assertEqual(mock_obj.method2(), "first")
        self.assertEqual(mock_obj.method2(), "second")
        with self.assertRaises(Exception):
            mock_obj.method2()
    
    def test_mock_reset(self):
        """Mock重置"""
        mock_obj = Mock()
        
        # 进行一些调用
        mock_obj.method("arg1")
        mock_obj.method("arg2")
        
        # 验证调用
        self.assertEqual(mock_obj.method.call_count, 2)
        
        # 重置Mock
        mock_obj.reset_mock()
        
        # 验证重置后状态
        self.assertEqual(mock_obj.method.call_count, 0)
        self.assertEqual(mock_obj.method.call_args_list, [])
    
    def test_mock_configure_mock(self):
        """使用configure_mock配置Mock"""
        mock_obj = Mock()
        
        # 批量配置Mock
        mock_obj.configure_mock(
            **{
                'method1.return_value': 'value1',
                'method2.side_effect': Exception('error'),
                'property1': 'prop_value'
            }
        )
        
        # 验证配置
        self.assertEqual(mock_obj.method1(), 'value1')
        self.assertEqual(mock_obj.property1, 'prop_value')
        with self.assertRaises(Exception):
            mock_obj.method2()
    
    def test_assert_methods(self):
        """各种断言方法"""
        mock_obj = Mock()
        
        # 进行调用
        mock_obj.method("arg1", keyword="value1")
        mock_obj.method("arg2", keyword="value2")
        
        # 各种断言
        mock_obj.method.assert_called()  # 至少被调用一次
        mock_obj.method.assert_called_with("arg2", keyword="value2")  # 最后一次调用
        mock_obj.method.assert_has_calls([  # 所有调用
            call("arg1", keyword="value1"),
            call("arg2", keyword="value2")
        ])
        
        # 验证未调用
        mock_obj.other_method.assert_not_called()


def demonstrate_mock_usage():
    """演示Mock的实际使用"""
    print("Session22 示例3: Mock和测试替身详解")
    print("=" * 50)
    
    print("\n1. 基本Mock演示")
    print("-" * 30)
    
    # 创建Mock对象
    mock_service = Mock()
    mock_service.get_data.return_value = {"status": "success", "data": [1, 2, 3]}
    
    # 使用Mock
    result = mock_service.get_data()
    print(f"Mock返回结果: {result}")
    
    # 验证调用
    print(f"调用次数: {mock_service.get_data.call_count}")
    print(f"是否被调用: {mock_service.get_data.called}")
    
    print("\n2. patch演示")
    print("-" * 30)
    
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {"temperature": 25}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # 使用被patch的requests
        api = WeatherAPI("test_key")
        weather_data = api.get_current_weather("Beijing")
        print(f"天气数据: {weather_data}")
        print(f"requests.get被调用: {mock_get.called}")
    
    print("\n3. 副作用演示")
    print("-" * 30)
    
    mock_obj = Mock()
    mock_obj.unreliable_method.side_effect = [
        "success",
        "success", 
        Exception("Network error")
    ]
    
    for i in range(3):
        try:
            result = mock_obj.unreliable_method()
            print(f"第{i+1}次调用成功: {result}")
        except Exception as e:
            print(f"第{i+1}次调用失败: {e}")
    
    print("\n演示完成！")
    print("\nMock使用要点:")
    print("- Mock用于隔离外部依赖")
    print("- patch用于替换模块中的对象")
    print("- side_effect可以模拟异常和多次调用")
    print("- 使用spec限制Mock的接口")
    print("- 验证Mock的调用情况")


if __name__ == '__main__':
    # 运行演示
    demonstrate_mock_usage()
    
    print("\n" + "=" * 50)
    print("运行单元测试")
    print("=" * 50)
    
    # 运行测试
    unittest.main(argv=[''], exit=False, verbosity=2)