#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session29 练习2: Mock测试和依赖隔离

练习目标:
1. 学习使用Mock对象
2. 隔离外部依赖
3. 测试API调用
4. 模拟数据库操作
5. 使用patch装饰器

练习说明:
请为下面的服务类编写Mock测试，模拟外部依赖：
- 数据库操作
- HTTP API调用
- 文件系统操作
- 第三方服务

作者: Python教程团队
"""

import unittest
from unittest.mock import Mock, patch, MagicMock, call
import requests
import json
import os
from typing import Dict, List, Optional


# 模拟的外部依赖
class DatabaseConnection:
    """数据库连接类"""
    
    def __init__(self, host: str, port: int, database: str):
        self.host = host
        self.port = port
        self.database = database
        self.connected = False
    
    def connect(self):
        """连接数据库"""
        # 实际实现会连接真实数据库
        self.connected = True
        return True
    
    def execute_query(self, query: str, params: tuple = None):
        """执行查询"""
        if not self.connected:
            raise RuntimeError("数据库未连接")
        # 实际实现会执行真实查询
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
        # 实际实现会发送真实邮件
        print(f"发送邮件到 {to}: {subject}")
        return True


class FileStorage:
    """文件存储类"""
    
    def save_file(self, filename: str, content: str) -> str:
        """保存文件"""
        # 实际实现会保存到文件系统
        filepath = f"/storage/{filename}"
        return filepath
    
    def read_file(self, filepath: str) -> str:
        """读取文件"""
        # 实际实现会从文件系统读取
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"文件不存在: {filepath}")
        return "file content"
    
    def delete_file(self, filepath: str) -> bool:
        """删除文件"""
        # 实际实现会删除文件
        return True


# 需要测试的业务服务类
class UserService:
    """用户服务类 - 需要为此类编写Mock测试"""
    
    def __init__(self, db: DatabaseConnection, email_service: EmailService, file_storage: FileStorage):
        self.db = db
        self.email_service = email_service
        self.file_storage = file_storage
    
    def create_user(self, user_data: Dict) -> Dict:
        """创建用户"""
        # 验证用户数据
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
        # 检查用户是否存在
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
    """天气服务类 - 需要Mock HTTP请求"""
    
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


# TODO: 请完成以下测试类
class TestUserService(unittest.TestCase):
    """用户服务Mock测试
    
    请完成以下测试方法：
    1. setUp - 创建Mock对象和服务实例
    2. test_create_user_success - 测试成功创建用户
    3. test_create_user_duplicate_email - 测试重复邮箱
    4. test_create_user_email_failure - 测试邮件发送失败
    5. test_get_user_found - 测试找到用户
    6. test_get_user_not_found - 测试用户不存在
    7. test_update_user_success - 测试成功更新用户
    8. test_update_user_email_change - 测试邮箱变更
    9. test_export_user_data - 测试导出用户数据
    10. test_delete_user_success - 测试成功删除用户
    """
    
    def setUp(self):
        """设置Mock对象"""
        # TODO: 创建Mock对象
        # 提示：使用Mock()或MagicMock()创建模拟对象
        # self.mock_db = Mock(spec=DatabaseConnection)
        # self.mock_email = Mock(spec=EmailService)
        # self.mock_storage = Mock(spec=FileStorage)
        # self.user_service = UserService(self.mock_db, self.mock_email, self.mock_storage)
        pass
    
    def test_create_user_success(self):
        """测试成功创建用户"""
        # TODO: 设置Mock返回值并测试创建用户
        # 提示：
        # 1. 设置 mock_db.execute_query 的返回值
        # 2. 设置 mock_email.send_email 的返回值
        # 3. 调用 user_service.create_user
        # 4. 验证返回结果
        # 5. 验证Mock方法被正确调用
        pass
    
    def test_create_user_duplicate_email(self):
        """测试重复邮箱"""
        # TODO: 模拟数据库返回已存在的用户
        # 提示：设置execute_query返回非空结果，然后验证抛出ValueError
        pass
    
    def test_create_user_email_failure(self):
        """测试邮件发送失败"""
        # TODO: 模拟邮件发送失败
        # 提示：设置send_email返回False，验证用户仍然创建成功但welcome_sent为False
        pass
    
    def test_get_user_found(self):
        """测试找到用户"""
        # TODO: 模拟数据库返回用户数据
        pass
    
    def test_get_user_not_found(self):
        """测试用户不存在"""
        # TODO: 模拟数据库返回空结果
        pass
    
    def test_update_user_success(self):
        """测试成功更新用户"""
        # TODO: 模拟获取用户和更新用户的过程
        pass
    
    def test_update_user_email_change(self):
        """测试邮箱变更"""
        # TODO: 测试邮箱变更时发送通知邮件
        pass
    
    def test_export_user_data(self):
        """测试导出用户数据"""
        # TODO: 模拟获取用户数据和保存文件
        pass
    
    def test_delete_user_success(self):
        """测试成功删除用户"""
        # TODO: 模拟删除用户的完整流程
        pass


class TestWeatherService(unittest.TestCase):
    """天气服务Mock测试
    
    请完成以下测试方法，使用patch装饰器模拟HTTP请求：
    1. test_get_weather_summary_success - 测试成功获取天气摘要
    2. test_get_weather_summary_api_error - 测试API错误
    3. test_get_weather_summary_network_error - 测试网络错误
    """
    
    def setUp(self):
        """设置测试环境"""
        # TODO: 创建WeatherAPI和WeatherService实例
        pass
    
    @patch('requests.get')
    def test_get_weather_summary_success(self, mock_get):
        """测试成功获取天气摘要"""
        # TODO: 使用patch模拟requests.get
        # 提示：
        # 1. 设置mock_get的返回值
        # 2. 模拟current weather和forecast的响应
        # 3. 调用get_weather_summary
        # 4. 验证结果和调用
        pass
    
    @patch('requests.get')
    def test_get_weather_summary_api_error(self, mock_get):
        """测试API错误"""
        # TODO: 模拟API返回错误状态码
        # 提示：设置mock_get.side_effect = requests.HTTPError()
        pass
    
    @patch('requests.get')
    def test_get_weather_summary_network_error(self, mock_get):
        """测试网络错误"""
        # TODO: 模拟网络连接错误
        # 提示：设置mock_get.side_effect = requests.ConnectionError()
        pass


# 高级Mock技术示例
class TestAdvancedMocking(unittest.TestCase):
    """高级Mock技术测试"""
    
    def test_mock_with_side_effect(self):
        """测试使用side_effect的Mock"""
        # TODO: 使用side_effect模拟多次调用返回不同结果
        # 示例：
        # mock_func = Mock()
        # mock_func.side_effect = [result1, result2, Exception("error")]
        pass
    
    def test_mock_call_verification(self):
        """测试Mock调用验证"""
        # TODO: 验证Mock方法的调用次数和参数
        # 提示：使用assert_called_with, assert_called_once, call_count等
        pass
    
    def test_mock_property(self):
        """测试Mock属性"""
        # TODO: 测试Mock对象的属性设置和获取
        pass
    
    @patch.object(os.path, 'exists')
    def test_patch_object(self, mock_exists):
        """测试patch.object装饰器"""
        # TODO: 使用patch.object模拟os.path.exists
        pass
    
    def test_context_manager_mock(self):
        """测试上下文管理器Mock"""
        # TODO: 使用with patch()语法
        # with patch('module.function') as mock_func:
        #     mock_func.return_value = 'mocked'
        #     # 测试代码
        pass


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
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("Session29 练习2: Mock测试和依赖隔离")
    print("=" * 50)
    
    print("\n练习说明:")
    print("1. 学习使用Mock对象隔离外部依赖")
    print("2. 使用patch装饰器模拟模块和函数")
    print("3. 验证Mock对象的调用情况")
    print("4. 处理各种异常情况")
    
    print("\n开始测试...")
    success = run_tests()
    
    if success:
        print("\n🎉 恭喜！所有Mock测试都通过了！")
    else:
        print("\n❌ 还有测试未通过，请检查你的Mock设置")
    
    print("\n学习要点:")
    print("- Mock对象用于隔离外部依赖")
    print("- patch装饰器可以替换模块中的对象")
    print("- side_effect可以模拟异常和多次调用")
    print("- 验证Mock的调用次数和参数")
    print("- 使用spec参数限制Mock的接口")