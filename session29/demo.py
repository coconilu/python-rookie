#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session29: 项目测试与调试 - 演示代码

本文件演示了项目级别的测试和调试技术，包括：
- 测试框架的使用
- 调试工具的应用
- 性能分析方法
- 自动化测试流程

作者: Python教程团队
创建日期: 2024-12-25
最后修改: 2024-12-25
"""

import sys
import os
import time
import logging
import unittest
import cProfile
import pstats
import io
from functools import wraps
from typing import List, Dict, Optional
from unittest.mock import Mock, patch


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Calculator:
    """计算器类 - 用于演示测试"""
    
    def add(self, a: float, b: float) -> float:
        """加法运算"""
        logger.debug(f"Adding {a} + {b}")
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """减法运算"""
        logger.debug(f"Subtracting {a} - {b}")
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """乘法运算"""
        logger.debug(f"Multiplying {a} * {b}")
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        """除法运算"""
        logger.debug(f"Dividing {a} / {b}")
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        return a / b
    
    def power(self, base: float, exponent: float) -> float:
        """幂运算"""
        logger.debug(f"Calculating {base} ** {exponent}")
        return base ** exponent


class DataProcessor:
    """数据处理器 - 用于演示性能测试"""
    
    def __init__(self):
        self.processed_count = 0
    
    def process_data(self, data: List[int]) -> Dict[str, float]:
        """处理数据并返回统计信息"""
        logger.info(f"Processing {len(data)} data points")
        
        if not data:
            return {'sum': 0, 'average': 0, 'max': 0, 'min': 0}
        
        # 模拟复杂计算
        total = sum(data)
        average = total / len(data)
        maximum = max(data)
        minimum = min(data)
        
        # 模拟一些CPU密集型操作
        for i in range(len(data)):
            _ = data[i] ** 2
        
        self.processed_count += len(data)
        
        result = {
            'sum': total,
            'average': average,
            'max': maximum,
            'min': minimum,
            'count': len(data)
        }
        
        logger.info(f"Processing complete: {result}")
        return result
    
    def batch_process(self, batches: List[List[int]]) -> List[Dict[str, float]]:
        """批量处理数据"""
        results = []
        for i, batch in enumerate(batches):
            logger.info(f"Processing batch {i + 1}/{len(batches)}")
            result = self.process_data(batch)
            results.append(result)
        return results


class UserService:
    """用户服务 - 用于演示模拟测试"""
    
    def __init__(self, database):
        self.database = database
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """获取用户信息"""
        logger.info(f"Getting user {user_id}")
        user = self.database.get_user(user_id)
        if user:
            logger.info(f"User found: {user['name']}")
        else:
            logger.warning(f"User {user_id} not found")
        return user
    
    def create_user(self, user_data: Dict) -> Dict:
        """创建用户"""
        logger.info(f"Creating user: {user_data['name']}")
        
        # 验证用户数据
        if not user_data.get('name'):
            raise ValueError("User name is required")
        if not user_data.get('email'):
            raise ValueError("User email is required")
        
        # 检查邮箱是否已存在
        existing_user = self.database.get_user_by_email(user_data['email'])
        if existing_user:
            raise ValueError("Email already exists")
        
        # 创建用户
        user = self.database.create_user(user_data)
        logger.info(f"User created with ID: {user['id']}")
        return user
    
    def update_user(self, user_id: int, user_data: Dict) -> Dict:
        """更新用户信息"""
        logger.info(f"Updating user {user_id}")
        
        # 检查用户是否存在
        existing_user = self.database.get_user(user_id)
        if not existing_user:
            raise ValueError(f"User {user_id} not found")
        
        # 更新用户
        updated_user = self.database.update_user(user_id, user_data)
        logger.info(f"User {user_id} updated successfully")
        return updated_user


# 测试装饰器
def performance_test(func):
    """性能测试装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        
        execution_time = end_time - start_time
        print(f"\n{'='*50}")
        print(f"Performance Test: {func.__name__}")
        print(f"Execution Time: {execution_time:.4f} seconds")
        print(f"{'='*50}")
        
        return result
    return wrapper


def debug_trace(func):
    """调试跟踪装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"Entering {func.__name__} with args={args}, kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Exiting {func.__name__} with result={result}")
            return result
        except Exception as e:
            logger.error(f"Exception in {func.__name__}: {type(e).__name__}: {e}")
            raise
    return wrapper


class TestCalculator(unittest.TestCase):
    """计算器单元测试"""
    
    def setUp(self):
        """测试前准备"""
        self.calc = Calculator()
    
    def test_add(self):
        """测试加法"""
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(0, 0), 0)
    
    def test_subtract(self):
        """测试减法"""
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(0, 5), -5)
        self.assertEqual(self.calc.subtract(-1, -1), 0)
    
    def test_multiply(self):
        """测试乘法"""
        self.assertEqual(self.calc.multiply(3, 4), 12)
        self.assertEqual(self.calc.multiply(-2, 3), -6)
        self.assertEqual(self.calc.multiply(0, 100), 0)
    
    def test_divide(self):
        """测试除法"""
        self.assertEqual(self.calc.divide(10, 2), 5)
        self.assertEqual(self.calc.divide(-6, 3), -2)
        
        # 测试除零异常
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)
    
    def test_power(self):
        """测试幂运算"""
        self.assertEqual(self.calc.power(2, 3), 8)
        self.assertEqual(self.calc.power(5, 0), 1)
        self.assertEqual(self.calc.power(10, 2), 100)


class TestUserService(unittest.TestCase):
    """用户服务测试 - 演示模拟测试"""
    
    def setUp(self):
        """测试前准备"""
        # 创建模拟数据库
        self.mock_db = Mock()
        self.user_service = UserService(self.mock_db)
    
    def test_get_user_success(self):
        """测试成功获取用户"""
        # 设置模拟返回值
        expected_user = {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'}
        self.mock_db.get_user.return_value = expected_user
        
        # 执行测试
        result = self.user_service.get_user(1)
        
        # 验证结果
        self.assertEqual(result, expected_user)
        self.mock_db.get_user.assert_called_once_with(1)
    
    def test_get_user_not_found(self):
        """测试用户不存在"""
        # 设置模拟返回值
        self.mock_db.get_user.return_value = None
        
        # 执行测试
        result = self.user_service.get_user(999)
        
        # 验证结果
        self.assertIsNone(result)
        self.mock_db.get_user.assert_called_once_with(999)
    
    def test_create_user_success(self):
        """测试成功创建用户"""
        # 设置模拟数据
        user_data = {'name': 'Jane Doe', 'email': 'jane@example.com'}
        expected_user = {'id': 2, **user_data}
        
        self.mock_db.get_user_by_email.return_value = None  # 邮箱不存在
        self.mock_db.create_user.return_value = expected_user
        
        # 执行测试
        result = self.user_service.create_user(user_data)
        
        # 验证结果
        self.assertEqual(result, expected_user)
        self.mock_db.get_user_by_email.assert_called_once_with('jane@example.com')
        self.mock_db.create_user.assert_called_once_with(user_data)
    
    def test_create_user_missing_name(self):
        """测试创建用户时缺少姓名"""
        user_data = {'email': 'test@example.com'}
        
        with self.assertRaises(ValueError) as context:
            self.user_service.create_user(user_data)
        
        self.assertIn('name is required', str(context.exception))
    
    def test_create_user_email_exists(self):
        """测试创建用户时邮箱已存在"""
        user_data = {'name': 'Test User', 'email': 'existing@example.com'}
        existing_user = {'id': 1, 'name': 'Existing User', 'email': 'existing@example.com'}
        
        self.mock_db.get_user_by_email.return_value = existing_user
        
        with self.assertRaises(ValueError) as context:
            self.user_service.create_user(user_data)
        
        self.assertIn('Email already exists', str(context.exception))


class TestDataProcessor(unittest.TestCase):
    """数据处理器测试"""
    
    def setUp(self):
        """测试前准备"""
        self.processor = DataProcessor()
    
    def test_process_empty_data(self):
        """测试处理空数据"""
        result = self.processor.process_data([])
        expected = {'sum': 0, 'average': 0, 'max': 0, 'min': 0}
        self.assertEqual(result, expected)
    
    def test_process_single_item(self):
        """测试处理单个数据"""
        result = self.processor.process_data([5])
        expected = {'sum': 5, 'average': 5, 'max': 5, 'min': 5, 'count': 1}
        self.assertEqual(result, expected)
    
    def test_process_multiple_items(self):
        """测试处理多个数据"""
        data = [1, 2, 3, 4, 5]
        result = self.processor.process_data(data)
        
        self.assertEqual(result['sum'], 15)
        self.assertEqual(result['average'], 3.0)
        self.assertEqual(result['max'], 5)
        self.assertEqual(result['min'], 1)
        self.assertEqual(result['count'], 5)
    
    @performance_test
    def test_process_large_data(self):
        """测试处理大量数据的性能"""
        large_data = list(range(10000))
        result = self.processor.process_data(large_data)
        
        self.assertEqual(result['count'], 10000)
        self.assertEqual(result['sum'], sum(large_data))
        self.assertEqual(result['max'], 9999)
        self.assertEqual(result['min'], 0)


@debug_trace
def demonstrate_debugging():
    """演示调试技术"""
    print("\n" + "="*50)
    print("调试技术演示")
    print("="*50)
    
    # 1. 日志调试
    logger.info("开始调试演示")
    
    calc = Calculator()
    
    # 2. 正常操作
    result1 = calc.add(10, 5)
    logger.info(f"正常计算结果: {result1}")
    
    # 3. 异常处理调试
    try:
        result2 = calc.divide(10, 0)
    except ValueError as e:
        logger.error(f"捕获到异常: {e}")
        print(f"异常已被正确处理: {e}")
    
    # 4. 断言调试
    assert result1 == 15, f"期望结果为15，实际为{result1}"
    logger.info("断言检查通过")
    
    print("调试演示完成")


def demonstrate_performance_analysis():
    """演示性能分析"""
    print("\n" + "="*50)
    print("性能分析演示")
    print("="*50)
    
    def cpu_intensive_function():
        """CPU密集型函数"""
        total = 0
        for i in range(100000):
            total += i * i
        return total
    
    # 使用cProfile进行性能分析
    pr = cProfile.Profile()
    pr.enable()
    
    # 执行性能测试
    processor = DataProcessor()
    data = list(range(1000))
    result = processor.process_data(data)
    
    # CPU密集型操作
    cpu_result = cpu_intensive_function()
    
    pr.disable()
    
    # 生成性能报告
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(10)  # 显示前10个最耗时的函数
    
    print("性能分析报告:")
    print(s.getvalue())
    
    print(f"数据处理结果: {result}")
    print(f"CPU密集型计算结果: {cpu_result}")


def demonstrate_test_coverage():
    """演示测试覆盖率"""
    print("\n" + "="*50)
    print("测试覆盖率演示")
    print("="*50)
    
    # 运行单元测试
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestCalculator))
    suite.addTests(loader.loadTestsFromTestCase(TestUserService))
    suite.addTests(loader.loadTestsFromTestCase(TestDataProcessor))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 显示测试结果
    print(f"\n测试结果统计:")
    print(f"运行测试数: {result.testsRun}")
    print(f"失败测试数: {len(result.failures)}")
    print(f"错误测试数: {len(result.errors)}")
    print(f"成功率: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\n失败的测试:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\n错误的测试:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")


def demonstrate_integration_testing():
    """演示集成测试"""
    print("\n" + "="*50)
    print("集成测试演示")
    print("="*50)
    
    # 模拟数据库类
    class MockDatabase:
        def __init__(self):
            self.users = {}
            self.next_id = 1
        
        def get_user(self, user_id):
            return self.users.get(user_id)
        
        def get_user_by_email(self, email):
            for user in self.users.values():
                if user['email'] == email:
                    return user
            return None
        
        def create_user(self, user_data):
            user = {'id': self.next_id, **user_data}
            self.users[self.next_id] = user
            self.next_id += 1
            return user
        
        def update_user(self, user_id, user_data):
            if user_id in self.users:
                self.users[user_id].update(user_data)
                return self.users[user_id]
            return None
    
    # 集成测试
    db = MockDatabase()
    user_service = UserService(db)
    
    print("1. 测试创建用户")
    user_data = {'name': 'Integration Test User', 'email': 'integration@test.com'}
    created_user = user_service.create_user(user_data)
    print(f"创建的用户: {created_user}")
    
    print("\n2. 测试获取用户")
    retrieved_user = user_service.get_user(created_user['id'])
    print(f"获取的用户: {retrieved_user}")
    
    print("\n3. 测试更新用户")
    update_data = {'name': 'Updated User'}
    updated_user = user_service.update_user(created_user['id'], update_data)
    print(f"更新的用户: {updated_user}")
    
    print("\n4. 测试重复邮箱")
    try:
        duplicate_user = user_service.create_user(user_data)
    except ValueError as e:
        print(f"正确捕获重复邮箱错误: {e}")
    
    print("\n集成测试完成")


def main():
    """主函数：演示程序的入口点"""
    print("Session29: 项目测试与调试演示")
    print("=" * 50)
    
    try:
        # 1. 调试技术演示
        demonstrate_debugging()
        
        # 2. 性能分析演示
        demonstrate_performance_analysis()
        
        # 3. 单元测试演示
        demonstrate_test_coverage()
        
        # 4. 集成测试演示
        demonstrate_integration_testing()
        
        print("\n" + "="*50)
        print("所有演示完成！")
        print("="*50)
        
        print("\n学习要点总结:")
        print("1. 使用unittest框架编写单元测试")
        print("2. 使用Mock对象模拟外部依赖")
        print("3. 使用装饰器进行性能测试和调试跟踪")
        print("4. 使用cProfile进行性能分析")
        print("5. 使用日志记录程序执行状态")
        print("6. 编写集成测试验证模块间交互")
        print("7. 使用断言进行状态验证")
        print("8. 合理处理异常和错误情况")
        
    except Exception as e:
        logger.error(f"演示过程中发生错误: {e}")
        print(f"\n错误: {e}")
        print("请检查代码并重试")


if __name__ == "__main__":
    main()