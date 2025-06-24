#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session22 练习2：高级TDD练习

通过复杂的实际项目练习高级TDD技巧，包括Mock、集成测试等。

练习目标：
1. 掌握Mock和测试替身的使用
2. 学会编写集成测试
3. 练习测试驱动的API设计
4. 理解测试金字塔概念

作者: Python教程团队
创建日期: 2024-01-15
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import json
import tempfile
import os
from dataclasses import dataclass
from enum import Enum


# ============ 练习1：在线商店系统 ============

class OrderStatus(Enum):
    """订单状态枚举"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass
class Product:
    """产品数据类"""
    id: str
    name: str
    price: float
    stock: int
    category: str


@dataclass
class OrderItem:
    """订单项数据类"""
    product_id: str
    quantity: int
    unit_price: float


class PaymentService:
    """支付服务（外部依赖）"""
    
    def process_payment(self, amount: float, payment_method: str, card_info: Dict) -> Dict:
        """处理支付"""
        # 这是一个外部服务，在测试中需要Mock
        # 实际实现会调用第三方支付API
        raise NotImplementedError("这是外部服务，需要在测试中Mock")
    
    def refund_payment(self, payment_id: str, amount: float) -> Dict:
        """退款"""
        raise NotImplementedError("这是外部服务，需要在测试中Mock")


class InventoryService:
    """库存服务（外部依赖）"""
    
    def check_availability(self, product_id: str, quantity: int) -> bool:
        """检查库存可用性"""
        raise NotImplementedError("这是外部服务，需要在测试中Mock")
    
    def reserve_stock(self, product_id: str, quantity: int) -> bool:
        """预留库存"""
        raise NotImplementedError("这是外部服务，需要在测试中Mock")
    
    def release_stock(self, product_id: str, quantity: int) -> bool:
        """释放库存"""
        raise NotImplementedError("这是外部服务，需要在测试中Mock")
    
    def update_stock(self, product_id: str, quantity: int) -> bool:
        """更新库存"""
        raise NotImplementedError("这是外部服务，需要在测试中Mock")


class NotificationService:
    """通知服务（外部依赖）"""
    
    def send_email(self, to: str, subject: str, body: str) -> bool:
        """发送邮件"""
        raise NotImplementedError("这是外部服务，需要在测试中Mock")
    
    def send_sms(self, phone: str, message: str) -> bool:
        """发送短信"""
        raise NotImplementedError("这是外部服务，需要在测试中Mock")


class Order:
    """
    订单类
    
    要求实现以下功能：
    1. 创建订单
    2. 添加订单项
    3. 移除订单项
    4. 计算订单总金额
    5. 应用折扣
    6. 更新订单状态
    7. 获取订单详情
    """
    
    def __init__(self, order_id: str, customer_id: str):
        """初始化订单"""
        # TODO: 实现初始化逻辑
        pass
    
    def add_item(self, product: Product, quantity: int) -> bool:
        """添加订单项"""
        # TODO: 实现添加订单项逻辑
        pass
    
    def remove_item(self, product_id: str) -> bool:
        """移除订单项"""
        # TODO: 实现移除订单项逻辑
        pass
    
    def update_item_quantity(self, product_id: str, quantity: int) -> bool:
        """更新订单项数量"""
        # TODO: 实现更新数量逻辑
        pass
    
    def calculate_subtotal(self) -> float:
        """计算小计"""
        # TODO: 实现小计计算逻辑
        pass
    
    def apply_discount(self, discount_percentage: float) -> bool:
        """应用折扣"""
        # TODO: 实现折扣应用逻辑
        pass
    
    def calculate_total(self) -> float:
        """计算总金额（含税、折扣）"""
        # TODO: 实现总金额计算逻辑（税率10%）
        pass
    
    def update_status(self, new_status: OrderStatus) -> bool:
        """更新订单状态"""
        # TODO: 实现状态更新逻辑
        pass
    
    def get_order_details(self) -> Dict:
        """获取订单详情"""
        # TODO: 实现获取订单详情逻辑
        pass
    
    def is_modifiable(self) -> bool:
        """检查订单是否可修改"""
        # TODO: 实现可修改性检查逻辑
        pass


class OrderService:
    """
    订单服务类
    
    要求实现以下功能：
    1. 创建订单
    2. 处理订单（支付、库存预留等）
    3. 取消订单
    4. 发货
    5. 确认收货
    6. 获取订单历史
    """
    
    def __init__(self, payment_service: PaymentService, 
                 inventory_service: InventoryService,
                 notification_service: NotificationService):
        """初始化订单服务"""
        # TODO: 实现初始化逻辑
        pass
    
    def create_order(self, customer_id: str, items: List[Dict]) -> Order:
        """创建订单"""
        # TODO: 实现创建订单逻辑
        pass
    
    def process_order(self, order: Order, payment_info: Dict) -> bool:
        """处理订单（支付和库存预留）"""
        # TODO: 实现订单处理逻辑
        # 1. 检查库存
        # 2. 预留库存
        # 3. 处理支付
        # 4. 更新订单状态
        # 5. 发送确认通知
        pass
    
    def cancel_order(self, order_id: str, reason: str) -> bool:
        """取消订单"""
        # TODO: 实现取消订单逻辑
        # 1. 检查订单状态
        # 2. 释放库存
        # 3. 处理退款
        # 4. 更新订单状态
        # 5. 发送取消通知
        pass
    
    def ship_order(self, order_id: str, tracking_number: str) -> bool:
        """发货"""
        # TODO: 实现发货逻辑
        pass
    
    def confirm_delivery(self, order_id: str) -> bool:
        """确认收货"""
        # TODO: 实现确认收货逻辑
        pass
    
    def get_order_history(self, customer_id: str) -> List[Order]:
        """获取订单历史"""
        # TODO: 实现获取订单历史逻辑
        pass


# ============ 测试类 ============

class TestOrder(unittest.TestCase):
    """订单类测试"""
    
    def setUp(self):
        """测试前准备"""
        self.order = Order("ORD001", "CUST001")
        self.product1 = Product("P001", "笔记本电脑", 5000.0, 10, "电子产品")
        self.product2 = Product("P002", "鼠标", 100.0, 50, "电子产品")
    
    def test_order_creation(self):
        """测试订单创建"""
        self.assertEqual(self.order.order_id, "ORD001")
        self.assertEqual(self.order.customer_id, "CUST001")
        self.assertEqual(self.order.status, OrderStatus.PENDING)
        self.assertEqual(len(self.order.items), 0)
    
    def test_add_item(self):
        """测试添加订单项"""
        # 添加第一个商品
        result = self.order.add_item(self.product1, 2)
        self.assertTrue(result)
        self.assertEqual(len(self.order.items), 1)
        
        # 添加第二个商品
        result = self.order.add_item(self.product2, 1)
        self.assertTrue(result)
        self.assertEqual(len(self.order.items), 2)
        
        # 添加相同商品应该更新数量
        result = self.order.add_item(self.product1, 1)
        self.assertTrue(result)
        self.assertEqual(len(self.order.items), 2)  # 商品种类不变
        
        # 检查商品数量
        item = next(item for item in self.order.items if item.product_id == "P001")
        self.assertEqual(item.quantity, 3)  # 2 + 1
    
    def test_add_item_invalid_quantity(self):
        """测试添加无效数量的订单项"""
        # 数量不能为零或负数
        with self.assertRaises(ValueError):
            self.order.add_item(self.product1, 0)
        
        with self.assertRaises(ValueError):
            self.order.add_item(self.product1, -1)
    
    def test_remove_item(self):
        """测试移除订单项"""
        # 先添加商品
        self.order.add_item(self.product1, 2)
        self.order.add_item(self.product2, 1)
        
        # 移除商品
        result = self.order.remove_item("P001")
        self.assertTrue(result)
        self.assertEqual(len(self.order.items), 1)
        
        # 移除不存在的商品
        result = self.order.remove_item("P999")
        self.assertFalse(result)
    
    def test_calculate_subtotal(self):
        """测试小计计算"""
        # 空订单小计为0
        self.assertEqual(self.order.calculate_subtotal(), 0.0)
        
        # 添加商品后计算小计
        self.order.add_item(self.product1, 2)  # 5000 * 2 = 10000
        self.order.add_item(self.product2, 3)  # 100 * 3 = 300
        
        expected_subtotal = 10000.0 + 300.0
        self.assertEqual(self.order.calculate_subtotal(), expected_subtotal)
    
    def test_apply_discount(self):
        """测试应用折扣"""
        self.order.add_item(self.product1, 1)  # 5000
        
        # 应用10%折扣
        result = self.order.apply_discount(10.0)
        self.assertTrue(result)
        self.assertEqual(self.order.discount_percentage, 10.0)
        
        # 无效折扣
        with self.assertRaises(ValueError):
            self.order.apply_discount(-5.0)
        
        with self.assertRaises(ValueError):
            self.order.apply_discount(101.0)
    
    def test_calculate_total(self):
        """测试总金额计算"""
        self.order.add_item(self.product1, 1)  # 5000
        
        # 无折扣情况：5000 + 10%税 = 5500
        expected_total = 5000.0 * 1.1
        self.assertAlmostEqual(self.order.calculate_total(), expected_total, places=2)
        
        # 有折扣情况：(5000 - 10%) + 10%税 = 4950
        self.order.apply_discount(10.0)
        expected_total_with_discount = (5000.0 * 0.9) * 1.1
        self.assertAlmostEqual(self.order.calculate_total(), expected_total_with_discount, places=2)
    
    def test_update_status(self):
        """测试更新订单状态"""
        # 正常状态转换
        result = self.order.update_status(OrderStatus.CONFIRMED)
        self.assertTrue(result)
        self.assertEqual(self.order.status, OrderStatus.CONFIRMED)
        
        # 无效状态转换（已确认的订单不能回到待处理状态）
        result = self.order.update_status(OrderStatus.PENDING)
        self.assertFalse(result)
        self.assertEqual(self.order.status, OrderStatus.CONFIRMED)
    
    def test_order_modification_rules(self):
        """测试订单修改规则"""
        # 待处理状态可以修改
        self.assertTrue(self.order.is_modifiable())
        
        # 已确认状态不能修改
        self.order.update_status(OrderStatus.CONFIRMED)
        self.assertFalse(self.order.is_modifiable())
        
        # 已发货状态不能修改
        self.order.update_status(OrderStatus.SHIPPED)
        self.assertFalse(self.order.is_modifiable())


class TestOrderServiceWithMocks(unittest.TestCase):
    """使用Mock的订单服务测试"""
    
    def setUp(self):
        """测试前准备"""
        # 创建Mock服务
        self.mock_payment_service = Mock(spec=PaymentService)
        self.mock_inventory_service = Mock(spec=InventoryService)
        self.mock_notification_service = Mock(spec=NotificationService)
        
        # 创建订单服务
        self.order_service = OrderService(
            self.mock_payment_service,
            self.mock_inventory_service,
            self.mock_notification_service
        )
        
        # 测试数据
        self.customer_id = "CUST001"
        self.items = [
            {"product_id": "P001", "quantity": 2, "unit_price": 5000.0},
            {"product_id": "P002", "quantity": 1, "unit_price": 100.0}
        ]
        self.payment_info = {
            "method": "credit_card",
            "card_number": "1234567890123456",
            "cvv": "123",
            "expiry": "12/25"
        }
    
    def test_create_order(self):
        """测试创建订单"""
        order = self.order_service.create_order(self.customer_id, self.items)
        
        self.assertIsNotNone(order)
        self.assertEqual(order.customer_id, self.customer_id)
        self.assertEqual(len(order.items), 2)
        self.assertEqual(order.status, OrderStatus.PENDING)
    
    @patch('exercise2_advanced_tdd.datetime')
    def test_process_order_success(self, mock_datetime):
        """测试成功处理订单"""
        # 设置固定时间
        fixed_time = datetime(2024, 1, 15, 12, 0, 0)
        mock_datetime.now.return_value = fixed_time
        
        # 创建订单
        order = self.order_service.create_order(self.customer_id, self.items)
        
        # 配置Mock服务返回成功
        self.mock_inventory_service.check_availability.return_value = True
        self.mock_inventory_service.reserve_stock.return_value = True
        self.mock_payment_service.process_payment.return_value = {
            "success": True,
            "payment_id": "PAY123456",
            "amount": order.calculate_total()
        }
        self.mock_notification_service.send_email.return_value = True
        
        # 处理订单
        result = self.order_service.process_order(order, self.payment_info)
        
        # 验证结果
        self.assertTrue(result)
        self.assertEqual(order.status, OrderStatus.CONFIRMED)
        
        # 验证服务调用
        self.assertEqual(self.mock_inventory_service.check_availability.call_count, 2)
        self.assertEqual(self.mock_inventory_service.reserve_stock.call_count, 2)
        self.mock_payment_service.process_payment.assert_called_once()
        self.mock_notification_service.send_email.assert_called_once()
    
    def test_process_order_insufficient_stock(self):
        """测试库存不足时处理订单"""
        order = self.order_service.create_order(self.customer_id, self.items)
        
        # 配置库存不足
        self.mock_inventory_service.check_availability.side_effect = [True, False]
        
        # 处理订单应该失败
        result = self.order_service.process_order(order, self.payment_info)
        
        self.assertFalse(result)
        self.assertEqual(order.status, OrderStatus.PENDING)
        
        # 验证没有进行支付
        self.mock_payment_service.process_payment.assert_not_called()
    
    def test_process_order_payment_failure(self):
        """测试支付失败时处理订单"""
        order = self.order_service.create_order(self.customer_id, self.items)
        
        # 配置库存充足但支付失败
        self.mock_inventory_service.check_availability.return_value = True
        self.mock_inventory_service.reserve_stock.return_value = True
        self.mock_payment_service.process_payment.return_value = {
            "success": False,
            "error": "信用卡被拒绝"
        }
        
        # 处理订单应该失败
        result = self.order_service.process_order(order, self.payment_info)
        
        self.assertFalse(result)
        self.assertEqual(order.status, OrderStatus.PENDING)
        
        # 验证库存被释放
        self.assertEqual(self.mock_inventory_service.release_stock.call_count, 2)
    
    def test_cancel_order(self):
        """测试取消订单"""
        # 创建并处理订单
        order = self.order_service.create_order(self.customer_id, self.items)
        order.update_status(OrderStatus.CONFIRMED)
        order.payment_id = "PAY123456"
        
        # 配置Mock服务
        self.mock_inventory_service.release_stock.return_value = True
        self.mock_payment_service.refund_payment.return_value = {
            "success": True,
            "refund_id": "REF123456"
        }
        self.mock_notification_service.send_email.return_value = True
        
        # 取消订单
        result = self.order_service.cancel_order(order.order_id, "客户要求取消")
        
        # 验证结果
        self.assertTrue(result)
        self.assertEqual(order.status, OrderStatus.CANCELLED)
        
        # 验证服务调用
        self.assertEqual(self.mock_inventory_service.release_stock.call_count, 2)
        self.mock_payment_service.refund_payment.assert_called_once_with(
            "PAY123456", order.calculate_total()
        )
        self.mock_notification_service.send_email.assert_called_once()
    
    def test_ship_order(self):
        """测试发货"""
        order = self.order_service.create_order(self.customer_id, self.items)
        order.update_status(OrderStatus.CONFIRMED)
        
        # 配置通知服务
        self.mock_notification_service.send_email.return_value = True
        self.mock_notification_service.send_sms.return_value = True
        
        # 发货
        result = self.order_service.ship_order(order.order_id, "TRACK123456")
        
        # 验证结果
        self.assertTrue(result)
        self.assertEqual(order.status, OrderStatus.SHIPPED)
        self.assertEqual(order.tracking_number, "TRACK123456")
        
        # 验证通知发送
        self.mock_notification_service.send_email.assert_called_once()
        self.mock_notification_service.send_sms.assert_called_once()


# ============ 练习2：文件处理系统 ============

class FileProcessor:
    """
    文件处理器
    
    要求实现以下功能：
    1. 读取文件内容
    2. 处理CSV文件
    3. 处理JSON文件
    4. 生成报告
    5. 错误处理
    
    注意：需要使用Mock来测试文件操作
    """
    
    def __init__(self, file_path: str):
        """初始化文件处理器"""
        # TODO: 实现初始化逻辑
        pass
    
    def read_file(self) -> str:
        """读取文件内容"""
        # TODO: 实现文件读取逻辑
        pass
    
    def process_csv(self) -> List[Dict]:
        """处理CSV文件"""
        # TODO: 实现CSV处理逻辑
        pass
    
    def process_json(self) -> Dict:
        """处理JSON文件"""
        # TODO: 实现JSON处理逻辑
        pass
    
    def generate_report(self, data: List[Dict]) -> str:
        """生成报告"""
        # TODO: 实现报告生成逻辑
        pass
    
    def save_report(self, report: str, output_path: str) -> bool:
        """保存报告"""
        # TODO: 实现报告保存逻辑
        pass


class TestFileProcessor(unittest.TestCase):
    """文件处理器测试"""
    
    def setUp(self):
        """测试前准备"""
        self.test_file_path = "/path/to/test/file.csv"
        self.processor = FileProcessor(self.test_file_path)
    
    @patch('builtins.open')
    def test_read_file(self, mock_open):
        """测试文件读取"""
        # 配置Mock
        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.read.return_value = "test content"
        
        # 测试读取
        content = self.processor.read_file()
        
        # 验证结果
        self.assertEqual(content, "test content")
        mock_open.assert_called_once_with(self.test_file_path, 'r', encoding='utf-8')
    
    @patch('builtins.open')
    def test_read_file_not_found(self, mock_open):
        """测试文件不存在"""
        # 配置Mock抛出异常
        mock_open.side_effect = FileNotFoundError("文件不存在")
        
        # 测试应该抛出异常
        with self.assertRaises(FileNotFoundError):
            self.processor.read_file()
    
    @patch.object(FileProcessor, 'read_file')
    def test_process_csv(self, mock_read_file):
        """测试CSV处理"""
        # 配置Mock返回CSV内容
        csv_content = "name,age,city\nAlice,25,Beijing\nBob,30,Shanghai"
        mock_read_file.return_value = csv_content
        
        # 处理CSV
        result = self.processor.process_csv()
        
        # 验证结果
        expected = [
            {"name": "Alice", "age": "25", "city": "Beijing"},
            {"name": "Bob", "age": "30", "city": "Shanghai"}
        ]
        self.assertEqual(result, expected)
    
    @patch.object(FileProcessor, 'read_file')
    def test_process_json(self, mock_read_file):
        """测试JSON处理"""
        # 配置Mock返回JSON内容
        json_content = '{"users": [{"name": "Alice", "age": 25}]}'
        mock_read_file.return_value = json_content
        
        # 处理JSON
        result = self.processor.process_json()
        
        # 验证结果
        expected = {"users": [{"name": "Alice", "age": 25}]}
        self.assertEqual(result, expected)
    
    def test_generate_report(self):
        """测试报告生成"""
        # 测试数据
        data = [
            {"name": "Alice", "age": "25", "city": "Beijing"},
            {"name": "Bob", "age": "30", "city": "Shanghai"}
        ]
        
        # 生成报告
        report = self.processor.generate_report(data)
        
        # 验证报告内容
        self.assertIn("Alice", report)
        self.assertIn("Bob", report)
        self.assertIn("总记录数: 2", report)
    
    @patch('builtins.open')
    def test_save_report(self, mock_open):
        """测试保存报告"""
        # 配置Mock
        mock_file = mock_open.return_value.__enter__.return_value
        
        # 保存报告
        report_content = "测试报告内容"
        output_path = "/path/to/output/report.txt"
        result = self.processor.save_report(report_content, output_path)
        
        # 验证结果
        self.assertTrue(result)
        mock_open.assert_called_once_with(output_path, 'w', encoding='utf-8')
        mock_file.write.assert_called_once_with(report_content)


# ============ 练习指导 ============

def exercise_instructions():
    """练习指导"""
    print("Session22 练习2: 高级TDD练习")
    print("=" * 50)
    
    print("\n练习说明：")
    print("1. 这是高级TDD练习，重点学习：")
    print("   - Mock和测试替身的使用")
    print("   - 外部依赖的隔离")
    print("   - 集成测试的编写")
    print("   - 复杂业务逻辑的测试")
    
    print("\n2. 练习1：在线商店系统")
    print("   - 实现Order和OrderService类")
    print("   - 使用Mock隔离外部服务")
    print("   - 测试复杂的业务流程")
    print("   - 处理各种异常情况")
    
    print("\n3. 练习2：文件处理系统")
    print("   - 实现FileProcessor类")
    print("   - 使用Mock测试文件操作")
    print("   - 处理不同格式的文件")
    print("   - 测试错误处理")
    
    print("\n4. Mock使用技巧：")
    print("   - 使用spec参数限制Mock接口")
    print("   - 使用side_effect模拟异常")
    print("   - 使用patch装饰器和上下文管理器")
    print("   - 验证Mock的调用情况")
    
    print("\n5. 测试策略：")
    print("   - 单元测试：测试单个类的功能")
    print("   - 集成测试：测试组件间的协作")
    print("   - 边界测试：测试边界条件")
    print("   - 异常测试：测试错误处理")
    
    print("\n6. 运行测试：")
    print("   python -m unittest exercise2_advanced_tdd.py -v")
    
    print("\n开始高级TDD练习吧！")


if __name__ == '__main__':
    # 显示练习指导
    exercise_instructions()
    
    print("\n" + "=" * 50)
    print("运行测试（当前应该失败，因为还没有实现）")
    print("=" * 50)
    
    # 运行测试
    unittest.main(argv=[''], exit=False, verbosity=2)