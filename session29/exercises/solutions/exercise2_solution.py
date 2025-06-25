#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session29 练习2解决方案: Mock测试和依赖隔离

这是exercise2.py的完整解决方案，展示了如何使用Mock对象进行测试。

作者: Python教程团队
"""

import unittest
from unittest.mock import Mock, patch, MagicMock, call, PropertyMock
import requests
import json
import os
from typing import Dict, List, Optional


# 复制原始类定义（在实际项目中这些会在单独的模块中）
class DatabaseConnection:
    """数据库连接类"""
    
    def __init__(self, host: str, port: int, database: str):
        self.host = host
        self.port = port
        self.database = database
        self.connected = False
    
    def connect(self):
        """连接数据库"""
        self.connected = True
        return True
    
    def execute_query(self, query: str, params: tuple = None):
        """执行查询"""
        if not self.connected:
            raise RuntimeError("数据库未连接")
        return []
    
    def close(self):
        """关闭连接"""
        self.connected = False


class EmailService:
    """邮件服务类"""
    
    def __init__(self, smtp_server: str, port: int):
        self.smtp_server = smtp_server
        self.port = port
    
    def send_email(self, to: str, subject: str, body: str) -> bool:
        """发送邮件"""
        print(f"发送邮件到 {to}: {subject}")
        return True


class FileStorage:
    """文件存储类"""
    
    def save_file(self, filename: str, content: str) -> str:
        """保存文件"""
        filepath = f"/storage/{filename}"
        return filepath
    
    def read_file(self, filepath: str) -> str:
        """读取文件"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"文件不存在: {filepath}")
        return "file content"
    
    def delete_file(self, filepath: str) -> bool:
        """删除文件"""
        return True


class UserService:
    """用户服务类"""
    
    def __init__(self, db: DatabaseConnection, email_service: EmailService, file_storage: FileStorage):
        self.db = db
        self.email_service = email_service
        self.file_storage = file_storage
    
    def create_user(self, user_data: Dict) -> Dict:
        """创建用户"""
        if not user_data.get('email'):
            raise ValueError("邮箱不能为空")
        
        if not user_data.get('username'):
            raise ValueError("用户名不能为空")
        
        # 检查用户是否已存在
        existing_user = self.db.execute_query(
            "SELECT * FROM users WHERE email = ?", 
            (user_data['email'],)
        )
        
        if existing_user:
            raise ValueError("用户已存在")
        
        # 创建用户
        user_id = self.db.execute_query(
            "INSERT INTO users (username, email) VALUES (?, ?) RETURNING id",
            (user_data['username'], user_data['email'])
        )
        
        # 发送欢迎邮件
        welcome_sent = self.email_service.send_email(
            user_data['email'],
            "欢迎注册",
            f"欢迎 {user_data['username']} 注册我们的服务！"
        )
        
        if not welcome_sent:
            print("警告：欢迎邮件发送失败")
        
        return {
            'id': user_id,
            'username': user_data['username'],
            'email': user_data['email'],
            'welcome_sent': welcome_sent
        }
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """获取用户信息"""
        result = self.db.execute_query(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        )
        
        if not result:
            return None
        
        return {
            'id': result[0]['id'],
            'username': result[0]['username'],
            'email': result[0]['email']
        }
    
    def update_user(self, user_id: int, update_data: Dict) -> Dict:
        """更新用户信息"""
        existing_user = self.get_user(user_id)
        if not existing_user:
            raise ValueError("用户不存在")
        
        # 更新用户
        self.db.execute_query(
            "UPDATE users SET username = ?, email = ? WHERE id = ?",
            (update_data.get('username', existing_user['username']),
             update_data.get('email', existing_user['email']),
             user_id)
        )
        
        # 如果邮箱发生变化，发送通知邮件
        if update_data.get('email') and update_data['email'] != existing_user['email']:
            self.email_service.send_email(
                update_data['email'],
                "邮箱变更通知",
                "您的邮箱已成功变更"
            )
        
        return self.get_user(user_id)
    
    def export_user_data(self, user_id: int) -> str:
        """导出用户数据"""
        user = self.get_user(user_id)
        if not user:
            raise ValueError("用户不存在")
        
        # 获取用户的所有数据
        user_posts = self.db.execute_query(
            "SELECT * FROM posts WHERE user_id = ?",
            (user_id,)
        )
        
        export_data = {
            'user': user,
            'posts': user_posts,
            'export_time': '2024-01-01 12:00:00'
        }
        
        # 保存到文件
        filename = f"user_export_{user_id}.json"
        content = json.dumps(export_data, ensure_ascii=False, indent=2)
        filepath = self.file_storage.save_file(filename, content)
        
        return filepath
    
    def delete_user(self, user_id: int) -> bool:
        """删除用户"""
        user = self.get_user(user_id)
        if not user:
            raise ValueError("用户不存在")
        
        # 删除用户数据
        self.db.execute_query("DELETE FROM posts WHERE user_id = ?", (user_id,))
        self.db.execute_query("DELETE FROM users WHERE id = ?", (user_id,))
        
        # 发送账户删除确认邮件
        self.email_service.send_email(
            user['email'],
            "账户删除确认",
            "您的账户已被成功删除"
        )
        
        return True


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
    
    def get_forecast(self, city: str, days: int = 5) -> List[Dict]:
        """获取天气预报"""
        url = f"{self.base_url}/forecast"
        params = {
            'key': self.api_key,
            'city': city,
            'days': days
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        return response.json()['forecast']


class WeatherService:
    """天气服务类"""
    
    def __init__(self, weather_api: WeatherAPI):
        self.weather_api = weather_api
    
    def get_weather_summary(self, city: str) -> Dict:
        """获取天气摘要"""
        try:
            current = self.weather_api.get_current_weather(city)
            forecast = self.weather_api.get_forecast(city, 3)
            
            return {
                'city': city,
                'current_temperature': current['temperature'],
                'current_description': current['description'],
                'forecast_days': len(forecast),
                'avg_temperature': sum(day['temperature'] for day in forecast) / len(forecast)
            }
        except requests.RequestException as e:
            raise RuntimeError(f"获取天气信息失败: {e}")


# 完整的测试解决方案
class TestUserService(unittest.TestCase):
    """用户服务Mock测试 - 完整解决方案"""
    
    def setUp(self):
        """设置Mock对象"""
        # 创建Mock对象，使用spec参数限制接口
        self.mock_db = Mock(spec=DatabaseConnection)
        self.mock_email = Mock(spec=EmailService)
        self.mock_storage = Mock(spec=FileStorage)
        
        # 创建用户服务实例
        self.user_service = UserService(self.mock_db, self.mock_email, self.mock_storage)
        
        # 测试数据
        self.test_user_data = {
            'username': 'testuser',
            'email': 'test@example.com'
        }
    
    def test_create_user_success(self):
        """测试成功创建用户"""
        # 设置Mock返回值
        self.mock_db.execute_query.side_effect = [
            [],  # 第一次查询：用户不存在
            123  # 第二次查询：返回新用户ID
        ]
        self.mock_email.send_email.return_value = True
        
        # 调用被测试方法
        result = self.user_service.create_user(self.test_user_data)
        
        # 验证返回结果
        expected_result = {
            'id': 123,
            'username': 'testuser',
            'email': 'test@example.com',
            'welcome_sent': True
        }
        self.assertEqual(result, expected_result)
        
        # 验证Mock方法被正确调用
        self.assertEqual(self.mock_db.execute_query.call_count, 2)
        
        # 验证第一次数据库调用（检查用户是否存在）
        first_call = self.mock_db.execute_query.call_args_list[0]
        self.assertEqual(first_call[0][0], "SELECT * FROM users WHERE email = ?")
        self.assertEqual(first_call[0][1], ('test@example.com',))
        
        # 验证第二次数据库调用（插入新用户）
        second_call = self.mock_db.execute_query.call_args_list[1]
        self.assertEqual(second_call[0][0], "INSERT INTO users (username, email) VALUES (?, ?) RETURNING id")
        self.assertEqual(second_call[0][1], ('testuser', 'test@example.com'))
        
        # 验证邮件发送
        self.mock_email.send_email.assert_called_once_with(
            'test@example.com',
            '欢迎注册',
            '欢迎 testuser 注册我们的服务！'
        )
    
    def test_create_user_duplicate_email(self):
        """测试重复邮箱"""
        # 模拟数据库返回已存在的用户
        self.mock_db.execute_query.return_value = [{'id': 1, 'email': 'test@example.com'}]
        
        # 验证抛出ValueError
        with self.assertRaises(ValueError) as context:
            self.user_service.create_user(self.test_user_data)
        
        self.assertIn("用户已存在", str(context.exception))
        
        # 验证只调用了一次数据库查询（检查用户存在）
        self.mock_db.execute_query.assert_called_once()
        
        # 验证没有发送邮件
        self.mock_email.send_email.assert_not_called()
    
    def test_create_user_email_failure(self):
        """测试邮件发送失败"""
        # 设置Mock返回值
        self.mock_db.execute_query.side_effect = [[], 123]
        self.mock_email.send_email.return_value = False  # 邮件发送失败
        
        # 调用被测试方法
        result = self.user_service.create_user(self.test_user_data)
        
        # 验证用户仍然创建成功，但welcome_sent为False
        self.assertEqual(result['id'], 123)
        self.assertEqual(result['username'], 'testuser')
        self.assertEqual(result['email'], 'test@example.com')
        self.assertFalse(result['welcome_sent'])
        
        # 验证邮件发送被调用
        self.mock_email.send_email.assert_called_once()
    
    def test_create_user_missing_email(self):
        """测试缺少邮箱"""
        invalid_data = {'username': 'testuser'}  # 缺少email
        
        with self.assertRaises(ValueError) as context:
            self.user_service.create_user(invalid_data)
        
        self.assertIn("邮箱不能为空", str(context.exception))
        
        # 验证没有调用数据库
        self.mock_db.execute_query.assert_not_called()
    
    def test_create_user_missing_username(self):
        """测试缺少用户名"""
        invalid_data = {'email': 'test@example.com'}  # 缺少username
        
        with self.assertRaises(ValueError) as context:
            self.user_service.create_user(invalid_data)
        
        self.assertIn("用户名不能为空", str(context.exception))
    
    def test_get_user_found(self):
        """测试找到用户"""
        # 模拟数据库返回用户数据
        mock_user_data = [{
            'id': 123,
            'username': 'testuser',
            'email': 'test@example.com'
        }]
        self.mock_db.execute_query.return_value = mock_user_data
        
        # 调用被测试方法
        result = self.user_service.get_user(123)
        
        # 验证返回结果
        expected_result = {
            'id': 123,
            'username': 'testuser',
            'email': 'test@example.com'
        }
        self.assertEqual(result, expected_result)
        
        # 验证数据库调用
        self.mock_db.execute_query.assert_called_once_with(
            "SELECT * FROM users WHERE id = ?",
            (123,)
        )
    
    def test_get_user_not_found(self):
        """测试用户不存在"""
        # 模拟数据库返回空结果
        self.mock_db.execute_query.return_value = []
        
        # 调用被测试方法
        result = self.user_service.get_user(999)
        
        # 验证返回None
        self.assertIsNone(result)
        
        # 验证数据库调用
        self.mock_db.execute_query.assert_called_once_with(
            "SELECT * FROM users WHERE id = ?",
            (999,)
        )
    
    def test_update_user_success(self):
        """测试成功更新用户"""
        # 模拟get_user的返回值
        existing_user = {
            'id': 123,
            'username': 'olduser',
            'email': 'old@example.com'
        }
        
        updated_user = {
            'id': 123,
            'username': 'newuser',
            'email': 'old@example.com'
        }
        
        # 设置Mock返回值
        self.mock_db.execute_query.side_effect = [
            [existing_user],  # 第一次调用get_user
            None,             # 更新操作
            [updated_user]    # 第二次调用get_user
        ]
        
        update_data = {'username': 'newuser'}
        
        # 调用被测试方法
        result = self.user_service.update_user(123, update_data)
        
        # 验证返回结果
        self.assertEqual(result, updated_user)
        
        # 验证数据库调用次数
        self.assertEqual(self.mock_db.execute_query.call_count, 3)
        
        # 验证更新调用
        update_call = self.mock_db.execute_query.call_args_list[1]
        self.assertEqual(update_call[0][0], "UPDATE users SET username = ?, email = ? WHERE id = ?")
        self.assertEqual(update_call[0][1], ('newuser', 'old@example.com', 123))
    
    def test_update_user_email_change(self):
        """测试邮箱变更"""
        # 模拟现有用户
        existing_user = {
            'id': 123,
            'username': 'testuser',
            'email': 'old@example.com'
        }
        
        updated_user = {
            'id': 123,
            'username': 'testuser',
            'email': 'new@example.com'
        }
        
        # 设置Mock返回值
        self.mock_db.execute_query.side_effect = [
            [existing_user],  # get_user调用
            None,             # 更新操作
            [updated_user]    # 第二次get_user调用
        ]
        
        update_data = {'email': 'new@example.com'}
        
        # 调用被测试方法
        result = self.user_service.update_user(123, update_data)
        
        # 验证邮件变更通知被发送
        self.mock_email.send_email.assert_called_once_with(
            'new@example.com',
            '邮箱变更通知',
            '您的邮箱已成功变更'
        )
    
    def test_update_user_not_found(self):
        """测试更新不存在的用户"""
        # 模拟用户不存在
        self.mock_db.execute_query.return_value = []
        
        with self.assertRaises(ValueError) as context:
            self.user_service.update_user(999, {'username': 'newuser'})
        
        self.assertIn("用户不存在", str(context.exception))
    
    def test_export_user_data(self):
        """测试导出用户数据"""
        # 模拟用户数据
        user_data = {
            'id': 123,
            'username': 'testuser',
            'email': 'test@example.com'
        }
        
        posts_data = [
            {'id': 1, 'title': 'Post 1', 'content': 'Content 1'},
            {'id': 2, 'title': 'Post 2', 'content': 'Content 2'}
        ]
        
        # 设置Mock返回值
        self.mock_db.execute_query.side_effect = [
            [user_data],  # get_user调用
            posts_data    # 获取用户帖子
        ]
        
        self.mock_storage.save_file.return_value = "/storage/user_export_123.json"
        
        # 调用被测试方法
        result = self.user_service.export_user_data(123)
        
        # 验证返回结果
        self.assertEqual(result, "/storage/user_export_123.json")
        
        # 验证文件保存被调用
        self.mock_storage.save_file.assert_called_once()
        
        # 验证保存的文件名和内容
        save_call = self.mock_storage.save_file.call_args
        filename = save_call[0][0]
        content = save_call[0][1]
        
        self.assertEqual(filename, "user_export_123.json")
        
        # 验证导出内容
        export_data = json.loads(content)
        self.assertEqual(export_data['user'], user_data)
        self.assertEqual(export_data['posts'], posts_data)
        self.assertIn('export_time', export_data)
    
    def test_delete_user_success(self):
        """测试成功删除用户"""
        # 模拟用户数据
        user_data = {
            'id': 123,
            'username': 'testuser',
            'email': 'test@example.com'
        }
        
        # 设置Mock返回值
        self.mock_db.execute_query.side_effect = [
            [user_data],  # get_user调用
            None,         # 删除帖子
            None          # 删除用户
        ]
        
        # 调用被测试方法
        result = self.user_service.delete_user(123)
        
        # 验证返回结果
        self.assertTrue(result)
        
        # 验证数据库调用
        self.assertEqual(self.mock_db.execute_query.call_count, 3)
        
        # 验证删除帖子调用
        delete_posts_call = self.mock_db.execute_query.call_args_list[1]
        self.assertEqual(delete_posts_call[0][0], "DELETE FROM posts WHERE user_id = ?")
        self.assertEqual(delete_posts_call[0][1], (123,))
        
        # 验证删除用户调用
        delete_user_call = self.mock_db.execute_query.call_args_list[2]
        self.assertEqual(delete_user_call[0][0], "DELETE FROM users WHERE id = ?")
        self.assertEqual(delete_user_call[0][1], (123,))
        
        # 验证确认邮件发送
        self.mock_email.send_email.assert_called_once_with(
            'test@example.com',
            '账户删除确认',
            '您的账户已被成功删除'
        )


class TestWeatherService(unittest.TestCase):
    """天气服务Mock测试 - 完整解决方案"""
    
    def setUp(self):
        """设置测试环境"""
        self.weather_api = WeatherAPI("test_api_key")
        self.weather_service = WeatherService(self.weather_api)
    
    @patch('requests.get')
    def test_get_weather_summary_success(self, mock_get):
        """测试成功获取天气摘要"""
        # 模拟API响应
        mock_current_response = Mock()
        mock_current_response.json.return_value = {
            'temperature': 25,
            'description': '晴天'
        }
        mock_current_response.raise_for_status.return_value = None
        
        mock_forecast_response = Mock()
        mock_forecast_response.json.return_value = {
            'forecast': [
                {'temperature': 24},
                {'temperature': 26},
                {'temperature': 23}
            ]
        }
        mock_forecast_response.raise_for_status.return_value = None
        
        # 设置requests.get的返回值
        mock_get.side_effect = [mock_current_response, mock_forecast_response]
        
        # 调用被测试方法
        result = self.weather_service.get_weather_summary("北京")
        
        # 验证返回结果
        expected_result = {
            'city': '北京',
            'current_temperature': 25,
            'current_description': '晴天',
            'forecast_days': 3,
            'avg_temperature': 24.333333333333332  # (24+26+23)/3
        }
        self.assertEqual(result, expected_result)
        
        # 验证API调用
        self.assertEqual(mock_get.call_count, 2)
        
        # 验证第一次调用（当前天气）
        first_call = mock_get.call_args_list[0]
        self.assertEqual(first_call[0][0], "https://api.weather.com/current")
        self.assertEqual(first_call[1]['params'], {
            'key': 'test_api_key',
            'city': '北京'
        })
        
        # 验证第二次调用（天气预报）
        second_call = mock_get.call_args_list[1]
        self.assertEqual(second_call[0][0], "https://api.weather.com/forecast")
        self.assertEqual(second_call[1]['params'], {
            'key': 'test_api_key',
            'city': '北京',
            'days': 3
        })
    
    @patch('requests.get')
    def test_get_weather_summary_api_error(self, mock_get):
        """测试API错误"""
        # 模拟HTTP错误
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_get.return_value = mock_response
        
        # 验证抛出RuntimeError
        with self.assertRaises(RuntimeError) as context:
            self.weather_service.get_weather_summary("不存在的城市")
        
        self.assertIn("获取天气信息失败", str(context.exception))
        self.assertIn("404 Not Found", str(context.exception))
    
    @patch('requests.get')
    def test_get_weather_summary_network_error(self, mock_get):
        """测试网络错误"""
        # 模拟网络连接错误
        mock_get.side_effect = requests.ConnectionError("网络连接失败")
        
        # 验证抛出RuntimeError
        with self.assertRaises(RuntimeError) as context:
            self.weather_service.get_weather_summary("北京")
        
        self.assertIn("获取天气信息失败", str(context.exception))
        self.assertIn("网络连接失败", str(context.exception))
    
    @patch('requests.get')
    def test_get_weather_summary_timeout(self, mock_get):
        """测试请求超时"""
        # 模拟请求超时
        mock_get.side_effect = requests.Timeout("请求超时")
        
        # 验证抛出RuntimeError
        with self.assertRaises(RuntimeError) as context:
            self.weather_service.get_weather_summary("北京")
        
        self.assertIn("获取天气信息失败", str(context.exception))


class TestAdvancedMocking(unittest.TestCase):
    """高级Mock技术测试 - 完整解决方案"""
    
    def test_mock_with_side_effect(self):
        """测试使用side_effect的Mock"""
        # 创建Mock函数
        mock_func = Mock()
        
        # 设置side_effect，模拟多次调用返回不同结果
        mock_func.side_effect = ["第一次调用", "第二次调用", ValueError("第三次调用出错")]
        
        # 测试多次调用
        self.assertEqual(mock_func(), "第一次调用")
        self.assertEqual(mock_func(), "第二次调用")
        
        # 第三次调用应该抛出异常
        with self.assertRaises(ValueError) as context:
            mock_func()
        self.assertEqual(str(context.exception), "第三次调用出错")
        
        # 验证调用次数
        self.assertEqual(mock_func.call_count, 3)
    
    def test_mock_call_verification(self):
        """测试Mock调用验证"""
        mock_service = Mock()
        
        # 调用Mock方法
        mock_service.process_data("test_data", timeout=30)
        mock_service.process_data("another_data", timeout=60)
        
        # 验证调用次数
        self.assertEqual(mock_service.process_data.call_count, 2)
        
        # 验证特定调用
        mock_service.process_data.assert_any_call("test_data", timeout=30)
        mock_service.process_data.assert_any_call("another_data", timeout=60)
        
        # 验证最后一次调用
        mock_service.process_data.assert_called_with("another_data", timeout=60)
        
        # 验证所有调用
        expected_calls = [
            call("test_data", timeout=30),
            call("another_data", timeout=60)
        ]
        mock_service.process_data.assert_has_calls(expected_calls)
    
    def test_mock_property(self):
        """测试Mock属性"""
        # 创建Mock对象
        mock_obj = Mock()
        
        # 设置属性
        mock_obj.name = "测试对象"
        mock_obj.value = 42
        
        # 测试属性访问
        self.assertEqual(mock_obj.name, "测试对象")
        self.assertEqual(mock_obj.value, 42)
        
        # 使用PropertyMock
        mock_obj = Mock()
        type(mock_obj).status = PropertyMock(return_value="active")
        
        self.assertEqual(mock_obj.status, "active")
    
    @patch.object(os.path, 'exists')
    def test_patch_object(self, mock_exists):
        """测试patch.object装饰器"""
        # 设置Mock返回值
        mock_exists.return_value = True
        
        # 测试文件存在检查
        result = os.path.exists("/test/file.txt")
        
        # 验证结果
        self.assertTrue(result)
        
        # 验证Mock被调用
        mock_exists.assert_called_once_with("/test/file.txt")
    
    def test_context_manager_mock(self):
        """测试上下文管理器Mock"""
        # 使用with patch()语法
        with patch('builtins.open', create=True) as mock_open:
            mock_file = Mock()
            mock_file.read.return_value = "文件内容"
            mock_open.return_value.__enter__.return_value = mock_file
            
            # 测试文件读取
            with open("test.txt", "r") as f:
                content = f.read()
            
            # 验证结果
            self.assertEqual(content, "文件内容")
            
            # 验证Mock被调用
            mock_open.assert_called_once_with("test.txt", "r")
    
    def test_mock_chaining(self):
        """测试Mock链式调用"""
        mock_api = Mock()
        
        # 设置链式调用
        mock_api.get_user.return_value.get_profile.return_value.get_avatar.return_value = "avatar.jpg"
        
        # 测试链式调用
        result = mock_api.get_user(123).get_profile().get_avatar()
        
        # 验证结果
        self.assertEqual(result, "avatar.jpg")
        
        # 验证调用
        mock_api.get_user.assert_called_once_with(123)
    
    def test_mock_spec_enforcement(self):
        """测试Mock spec约束"""
        # 使用spec限制Mock接口
        mock_db = Mock(spec=DatabaseConnection)
        
        # 这些调用是允许的（因为在spec中）
        mock_db.connect()
        mock_db.execute_query("SELECT * FROM users")
        mock_db.close()
        
        # 这个调用会抛出AttributeError（因为不在spec中）
        with self.assertRaises(AttributeError):
            mock_db.non_existent_method()
    
    def test_mock_reset(self):
        """测试Mock重置"""
        mock_service = Mock()
        
        # 进行一些调用
        mock_service.method1()
        mock_service.method2("arg")
        
        # 验证调用次数
        self.assertEqual(mock_service.method1.call_count, 1)
        self.assertEqual(mock_service.method2.call_count, 1)
        
        # 重置Mock
        mock_service.reset_mock()
        
        # 验证调用次数被重置
        self.assertEqual(mock_service.method1.call_count, 0)
        self.assertEqual(mock_service.method2.call_count, 0)
    
    def test_mock_configure_mock(self):
        """测试Mock配置"""
        mock_obj = Mock()
        
        # 使用configure_mock配置多个属性和方法
        mock_obj.configure_mock(
            name="测试对象",
            value=42,
            get_info=Mock(return_value="信息")
        )
        
        # 验证配置
        self.assertEqual(mock_obj.name, "测试对象")
        self.assertEqual(mock_obj.value, 42)
        self.assertEqual(mock_obj.get_info(), "信息")


def run_tests():
    """运行所有Mock测试"""
    print("运行Mock测试...")
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestUserService))
    suite.addTests(loader.loadTestsFromTestCase(TestWeatherService))
    suite.addTests(loader.loadTestsFromTestCase(TestAdvancedMocking))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出测试统计
    print(f"\n测试统计:")
    print(f"运行测试: {result.testsRun}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("Session29 练习2解决方案: Mock测试和依赖隔离")
    print("=" * 50)
    
    print("\n这个解决方案展示了:")
    print("1. 基础Mock对象的使用")
    print("2. patch装饰器的应用")
    print("3. side_effect的高级用法")
    print("4. Mock调用验证技巧")
    print("5. spec参数的接口约束")
    print("6. 复杂依赖的隔离测试")
    
    print("\n开始测试...")
    success = run_tests()
    
    if success:
        print("\n🎉 所有Mock测试都通过了！")
        print("\n学到的Mock技巧:")
        print("- 使用Mock隔离外部依赖")
        print("- patch装饰器模拟模块函数")
        print("- side_effect模拟异常和多次调用")
        print("- 验证Mock的调用次数和参数")
        print("- spec参数限制Mock接口")
        print("- 上下文管理器的Mock测试")
    else:
        print("\n❌ 有测试失败，请检查Mock设置")