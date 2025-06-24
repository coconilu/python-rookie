#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session22 示例4：测试覆盖率和高级测试技巧

演示测试覆盖率分析、参数化测试、测试数据生成等高级技巧。

作者: Python教程团队
创建日期: 2024-01-15
"""

import unittest
import pytest
from unittest.mock import Mock, patch
import random
import string
import tempfile
import os
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import itertools


# ============ 被测试的类 ============

@dataclass
class Product:
    """产品数据类"""
    id: int
    name: str
    price: float
    category: str
    stock: int
    created_at: datetime
    
    def is_available(self) -> bool:
        """检查产品是否可用"""
        return self.stock > 0
    
    def apply_discount(self, percentage: float) -> float:
        """应用折扣"""
        if not 0 <= percentage <= 100:
            raise ValueError("折扣百分比必须在0-100之间")
        
        discount_amount = self.price * (percentage / 100)
        return self.price - discount_amount
    
    def update_stock(self, quantity: int) -> bool:
        """更新库存"""
        if quantity < 0 and abs(quantity) > self.stock:
            return False  # 库存不足
        
        self.stock += quantity
        return True


class ShoppingCart:
    """购物车类"""
    
    def __init__(self):
        self.items: Dict[int, Dict[str, Any]] = {}
        self.discount_code: Optional[str] = None
        self.tax_rate: float = 0.1  # 10%税率
    
    def add_item(self, product: Product, quantity: int = 1) -> bool:
        """添加商品到购物车"""
        if quantity <= 0:
            raise ValueError("数量必须大于0")
        
        if not product.is_available():
            return False
        
        if product.stock < quantity:
            return False
        
        if product.id in self.items:
            self.items[product.id]['quantity'] += quantity
        else:
            self.items[product.id] = {
                'product': product,
                'quantity': quantity,
                'added_at': datetime.now()
            }
        
        return True
    
    def remove_item(self, product_id: int) -> bool:
        """从购物车移除商品"""
        if product_id in self.items:
            del self.items[product_id]
            return True
        return False
    
    def update_quantity(self, product_id: int, quantity: int) -> bool:
        """更新商品数量"""
        if product_id not in self.items:
            return False
        
        if quantity <= 0:
            return self.remove_item(product_id)
        
        product = self.items[product_id]['product']
        if product.stock < quantity:
            return False
        
        self.items[product_id]['quantity'] = quantity
        return True
    
    def apply_discount_code(self, code: str) -> bool:
        """应用折扣码"""
        valid_codes = {
            'SAVE10': 10,
            'SAVE20': 20,
            'WELCOME': 15,
            'STUDENT': 25
        }
        
        if code in valid_codes:
            self.discount_code = code
            return True
        return False
    
    def get_subtotal(self) -> float:
        """获取小计"""
        total = 0
        for item in self.items.values():
            total += item['product'].price * item['quantity']
        return total
    
    def get_discount_amount(self) -> float:
        """获取折扣金额"""
        if not self.discount_code:
            return 0
        
        discount_rates = {
            'SAVE10': 0.1,
            'SAVE20': 0.2,
            'WELCOME': 0.15,
            'STUDENT': 0.25
        }
        
        subtotal = self.get_subtotal()
        return subtotal * discount_rates.get(self.discount_code, 0)
    
    def get_tax_amount(self) -> float:
        """获取税额"""
        subtotal = self.get_subtotal()
        discount = self.get_discount_amount()
        return (subtotal - discount) * self.tax_rate
    
    def get_total(self) -> float:
        """获取总计"""
        subtotal = self.get_subtotal()
        discount = self.get_discount_amount()
        tax = self.get_tax_amount()
        return subtotal - discount + tax
    
    def is_empty(self) -> bool:
        """检查购物车是否为空"""
        return len(self.items) == 0
    
    def get_item_count(self) -> int:
        """获取商品总数"""
        return sum(item['quantity'] for item in self.items.values())
    
    def clear(self) -> None:
        """清空购物车"""
        self.items.clear()
        self.discount_code = None


class OrderProcessor:
    """订单处理器"""
    
    def __init__(self, payment_service, inventory_service, notification_service):
        self.payment_service = payment_service
        self.inventory_service = inventory_service
        self.notification_service = notification_service
        self.order_counter = 1000
    
    def process_order(self, cart: ShoppingCart, customer_info: Dict) -> Dict:
        """处理订单"""
        if cart.is_empty():
            raise ValueError("购物车为空")
        
        # 验证库存
        for item in cart.items.values():
            product = item['product']
            quantity = item['quantity']
            
            if not self.inventory_service.check_stock(product.id, quantity):
                raise ValueError(f"商品 {product.name} 库存不足")
        
        # 计算总金额
        total_amount = cart.get_total()
        
        # 处理支付
        payment_result = self.payment_service.process_payment(
            customer_info['payment_method'],
            total_amount
        )
        
        if not payment_result['success']:
            raise RuntimeError(f"支付失败: {payment_result['error']}")
        
        # 更新库存
        for item in cart.items.values():
            product = item['product']
            quantity = item['quantity']
            self.inventory_service.reduce_stock(product.id, quantity)
        
        # 生成订单
        order_id = self._generate_order_id()
        order = {
            'id': order_id,
            'customer': customer_info,
            'items': list(cart.items.values()),
            'subtotal': cart.get_subtotal(),
            'discount': cart.get_discount_amount(),
            'tax': cart.get_tax_amount(),
            'total': total_amount,
            'payment_id': payment_result['payment_id'],
            'status': 'confirmed',
            'created_at': datetime.now()
        }
        
        # 发送通知
        self.notification_service.send_order_confirmation(
            customer_info['email'],
            order
        )
        
        return order
    
    def _generate_order_id(self) -> str:
        """生成订单ID"""
        self.order_counter += 1
        return f"ORD{self.order_counter}"
    
    def cancel_order(self, order_id: str) -> bool:
        """取消订单"""
        # 简化实现
        if not order_id.startswith('ORD'):
            return False
        
        # 实际实现会包含退款、恢复库存等逻辑
        return True


class DataValidator:
    """数据验证器"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """验证邮箱格式"""
        if not email or '@' not in email:
            return False
        
        parts = email.split('@')
        if len(parts) != 2:
            return False
        
        local, domain = parts
        if not local or not domain:
            return False
        
        if '.' not in domain:
            return False
        
        return True
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """验证手机号"""
        if not phone:
            return False
        
        # 移除所有非数字字符
        digits = ''.join(filter(str.isdigit, phone))
        
        # 检查长度
        if len(digits) < 10 or len(digits) > 15:
            return False
        
        return True
    
    @staticmethod
    def validate_password(password: str) -> Dict[str, bool]:
        """验证密码强度"""
        result = {
            'length_ok': len(password) >= 8,
            'has_upper': any(c.isupper() for c in password),
            'has_lower': any(c.islower() for c in password),
            'has_digit': any(c.isdigit() for c in password),
            'has_special': any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
        }
        
        result['is_strong'] = all([
            result['length_ok'],
            result['has_upper'],
            result['has_lower'],
            result['has_digit']
        ])
        
        return result
    
    @staticmethod
    def validate_credit_card(card_number: str) -> bool:
        """验证信用卡号（简化的Luhn算法）"""
        if not card_number:
            return False
        
        # 移除空格和连字符
        card_number = card_number.replace(' ', '').replace('-', '')
        
        # 检查是否全为数字
        if not card_number.isdigit():
            return False
        
        # 检查长度
        if len(card_number) < 13 or len(card_number) > 19:
            return False
        
        # 简化的Luhn算法检查
        def luhn_check(card_num):
            digits = [int(d) for d in card_num]
            for i in range(len(digits) - 2, -1, -2):
                digits[i] *= 2
                if digits[i] > 9:
                    digits[i] -= 9
            return sum(digits) % 10 == 0
        
        return luhn_check(card_number)


# ============ 测试数据生成器 ============

class TestDataGenerator:
    """测试数据生成器"""
    
    @staticmethod
    def generate_product(product_id: int = None, **kwargs) -> Product:
        """生成测试产品"""
        defaults = {
            'id': product_id or random.randint(1, 10000),
            'name': f"测试产品{random.randint(1, 1000)}",
            'price': round(random.uniform(10, 1000), 2),
            'category': random.choice(['电子产品', '服装', '书籍', '家居', '运动']),
            'stock': random.randint(0, 100),
            'created_at': datetime.now() - timedelta(days=random.randint(0, 365))
        }
        
        defaults.update(kwargs)
        return Product(**defaults)
    
    @staticmethod
    def generate_customer_info(**kwargs) -> Dict:
        """生成测试客户信息"""
        defaults = {
            'name': f"测试用户{random.randint(1, 1000)}",
            'email': f"test{random.randint(1, 1000)}@example.com",
            'phone': f"1{random.randint(3000000000, 9999999999)}",
            'address': f"测试地址{random.randint(1, 100)}号",
            'payment_method': random.choice(['credit_card', 'debit_card', 'paypal'])
        }
        
        defaults.update(kwargs)
        return defaults
    
    @staticmethod
    def generate_random_string(length: int = 10) -> str:
        """生成随机字符串"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    @staticmethod
    def generate_email() -> str:
        """生成随机邮箱"""
        username = TestDataGenerator.generate_random_string(8)
        domain = random.choice(['gmail.com', 'yahoo.com', 'hotmail.com', 'example.com'])
        return f"{username}@{domain}"
    
    @staticmethod
    def generate_phone() -> str:
        """生成随机手机号"""
        return f"1{random.randint(3000000000, 9999999999)}"
    
    @staticmethod
    def generate_credit_card() -> str:
        """生成测试信用卡号"""
        # 生成符合Luhn算法的测试卡号
        prefixes = ['4', '5', '6']  # Visa, MasterCard, Discover
        prefix = random.choice(prefixes)
        
        # 生成15位数字
        digits = [int(prefix)] + [random.randint(0, 9) for _ in range(14)]
        
        # 计算校验位
        for i in range(len(digits) - 2, -1, -2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9
        
        checksum = sum(digits) % 10
        check_digit = (10 - checksum) % 10
        digits.append(check_digit)
        
        return ''.join(map(str, digits))


# ============ 参数化测试 ============

class TestParametrized(unittest.TestCase):
    """参数化测试示例"""
    
    def test_product_discount_multiple_values(self):
        """测试产品折扣的多个值"""
        product = TestDataGenerator.generate_product(price=100.0)
        
        test_cases = [
            (0, 100.0),      # 无折扣
            (10, 90.0),      # 10%折扣
            (25, 75.0),      # 25%折扣
            (50, 50.0),      # 50%折扣
            (100, 0.0),      # 100%折扣
        ]
        
        for discount_percentage, expected_price in test_cases:
            with self.subTest(discount=discount_percentage):
                result = product.apply_discount(discount_percentage)
                self.assertAlmostEqual(result, expected_price, places=2)
    
    def test_email_validation_multiple_cases(self):
        """测试邮箱验证的多种情况"""
        test_cases = [
            ('valid@example.com', True),
            ('user.name@domain.co.uk', True),
            ('test123@test-domain.com', True),
            ('', False),
            ('invalid', False),
            ('@domain.com', False),
            ('user@', False),
            ('user@domain', False),
            ('user@@domain.com', False),
        ]
        
        for email, expected in test_cases:
            with self.subTest(email=email):
                result = DataValidator.validate_email(email)
                self.assertEqual(result, expected, f"邮箱 {email} 验证失败")
    
    def test_phone_validation_multiple_formats(self):
        """测试手机号验证的多种格式"""
        test_cases = [
            ('13812345678', True),
            ('138-1234-5678', True),
            ('138 1234 5678', True),
            ('+86 138 1234 5678', True),
            ('12345', False),      # 太短
            ('123456789012345678', False),  # 太长
            ('abc1234567890', False),  # 包含字母
            ('', False),           # 空字符串
        ]
        
        for phone, expected in test_cases:
            with self.subTest(phone=phone):
                result = DataValidator.validate_phone(phone)
                self.assertEqual(result, expected, f"手机号 {phone} 验证失败")


# ============ pytest参数化测试 ============

@pytest.mark.parametrize("price,discount,expected", [
    (100.0, 0, 100.0),
    (100.0, 10, 90.0),
    (100.0, 25, 75.0),
    (100.0, 50, 50.0),
    (100.0, 100, 0.0),
    (50.0, 20, 40.0),
])
def test_product_discount_pytest(price, discount, expected):
    """使用pytest参数化测试产品折扣"""
    product = TestDataGenerator.generate_product(price=price)
    result = product.apply_discount(discount)
    assert abs(result - expected) < 0.01


@pytest.mark.parametrize("password,expected_strong", [
    ("Password123", True),
    ("password123", False),  # 缺少大写字母
    ("PASSWORD123", False),  # 缺少小写字母
    ("Password", False),     # 缺少数字
    ("Pass123", False),      # 长度不够
    ("VeryStrongPassword123", True),
])
def test_password_validation_pytest(password, expected_strong):
    """使用pytest参数化测试密码验证"""
    result = DataValidator.validate_password(password)
    assert result['is_strong'] == expected_strong


# ============ 属性测试（Property-based Testing）============

class TestPropertyBased(unittest.TestCase):
    """基于属性的测试"""
    
    def test_shopping_cart_properties(self):
        """测试购物车的属性"""
        cart = ShoppingCart()
        
        # 属性1：空购物车的总计应该为0
        self.assertEqual(cart.get_total(), 0)
        self.assertTrue(cart.is_empty())
        
        # 属性2：添加商品后，购物车不应该为空
        product = TestDataGenerator.generate_product(stock=10)
        cart.add_item(product, 1)
        self.assertFalse(cart.is_empty())
        self.assertGreater(cart.get_total(), 0)
        
        # 属性3：清空购物车后应该恢复初始状态
        cart.clear()
        self.assertTrue(cart.is_empty())
        self.assertEqual(cart.get_total(), 0)
        self.assertEqual(cart.get_item_count(), 0)
    
    def test_product_stock_properties(self):
        """测试产品库存的属性"""
        for _ in range(10):  # 运行多次随机测试
            initial_stock = random.randint(1, 100)
            product = TestDataGenerator.generate_product(stock=initial_stock)
            
            # 属性1：减少库存不应该超过当前库存
            reduce_amount = random.randint(1, initial_stock)
            success = product.update_stock(-reduce_amount)
            self.assertTrue(success)
            self.assertEqual(product.stock, initial_stock - reduce_amount)
            
            # 属性2：增加库存应该总是成功
            increase_amount = random.randint(1, 50)
            current_stock = product.stock
            success = product.update_stock(increase_amount)
            self.assertTrue(success)
            self.assertEqual(product.stock, current_stock + increase_amount)
    
    def test_credit_card_luhn_property(self):
        """测试信用卡Luhn算法的属性"""
        for _ in range(20):  # 生成多个测试卡号
            card_number = TestDataGenerator.generate_credit_card()
            
            # 属性：生成的卡号应该通过验证
            self.assertTrue(DataValidator.validate_credit_card(card_number))
            
            # 属性：修改任意一位数字应该使验证失败（大概率）
            digits = list(card_number)
            pos = random.randint(0, len(digits) - 1)
            original_digit = digits[pos]
            
            # 尝试所有其他数字
            for new_digit in '0123456789':
                if new_digit != original_digit:
                    digits[pos] = new_digit
                    modified_card = ''.join(digits)
                    
                    # 大多数情况下应该验证失败
                    # 注意：有1/10的概率仍然有效（如果新数字恰好是正确的校验位）
                    if not DataValidator.validate_credit_card(modified_card):
                        break  # 找到一个无效的修改
            
            # 恢复原始数字
            digits[pos] = original_digit


# ============ 边界值测试 ============

class TestBoundaryValues(unittest.TestCase):
    """边界值测试"""
    
    def test_product_discount_boundaries(self):
        """测试产品折扣的边界值"""
        product = TestDataGenerator.generate_product(price=100.0)
        
        # 有效边界值
        self.assertEqual(product.apply_discount(0), 100.0)    # 最小值
        self.assertEqual(product.apply_discount(100), 0.0)    # 最大值
        
        # 无效边界值
        with self.assertRaises(ValueError):
            product.apply_discount(-1)    # 小于最小值
        
        with self.assertRaises(ValueError):
            product.apply_discount(101)   # 大于最大值
    
    def test_shopping_cart_quantity_boundaries(self):
        """测试购物车数量的边界值"""
        cart = ShoppingCart()
        product = TestDataGenerator.generate_product(stock=5)
        
        # 有效边界值
        self.assertTrue(cart.add_item(product, 1))    # 最小有效数量
        cart.clear()
        self.assertTrue(cart.add_item(product, 5))    # 最大可用数量
        
        # 无效边界值
        cart.clear()
        with self.assertRaises(ValueError):
            cart.add_item(product, 0)     # 零数量
        
        with self.assertRaises(ValueError):
            cart.add_item(product, -1)    # 负数量
        
        self.assertFalse(cart.add_item(product, 6))   # 超过库存
    
    def test_password_length_boundaries(self):
        """测试密码长度边界值"""
        # 7个字符（不满足最小长度）
        result = DataValidator.validate_password("Pass12A")
        self.assertFalse(result['length_ok'])
        
        # 8个字符（最小长度）
        result = DataValidator.validate_password("Pass123A")
        self.assertTrue(result['length_ok'])
        
        # 非常长的密码
        long_password = "A" * 100 + "a" * 100 + "1" * 100
        result = DataValidator.validate_password(long_password)
        self.assertTrue(result['length_ok'])


# ============ 性能测试 ============

class TestPerformance(unittest.TestCase):
    """性能测试示例"""
    
    def test_large_shopping_cart_performance(self):
        """测试大型购物车的性能"""
        import time
        
        cart = ShoppingCart()
        
        # 添加大量商品
        start_time = time.time()
        
        for i in range(1000):
            product = TestDataGenerator.generate_product(
                product_id=i,
                stock=100,
                price=random.uniform(10, 100)
            )
            cart.add_item(product, random.randint(1, 5))
        
        add_time = time.time() - start_time
        
        # 计算总计
        start_time = time.time()
        total = cart.get_total()
        calc_time = time.time() - start_time
        
        # 性能断言（这些值需要根据实际情况调整）
        self.assertLess(add_time, 1.0, "添加1000个商品应该在1秒内完成")
        self.assertLess(calc_time, 0.1, "计算总计应该在0.1秒内完成")
        self.assertGreater(total, 0, "总计应该大于0")
        
        print(f"添加1000个商品耗时: {add_time:.3f}秒")
        print(f"计算总计耗时: {calc_time:.3f}秒")
        print(f"购物车总计: {total:.2f}")
    
    def test_email_validation_performance(self):
        """测试邮箱验证性能"""
        import time
        
        # 生成测试邮箱
        emails = [TestDataGenerator.generate_email() for _ in range(10000)]
        
        # 测试验证性能
        start_time = time.time()
        
        valid_count = 0
        for email in emails:
            if DataValidator.validate_email(email):
                valid_count += 1
        
        validation_time = time.time() - start_time
        
        # 性能断言
        self.assertLess(validation_time, 1.0, "验证10000个邮箱应该在1秒内完成")
        self.assertGreater(valid_count, 0, "应该有有效的邮箱")
        
        print(f"验证10000个邮箱耗时: {validation_time:.3f}秒")
        print(f"有效邮箱数量: {valid_count}")


# ============ 集成测试 ============

class TestIntegration(unittest.TestCase):
    """集成测试示例"""
    
    def setUp(self):
        """设置测试环境"""
        # 创建Mock服务
        self.mock_payment_service = Mock()
        self.mock_inventory_service = Mock()
        self.mock_notification_service = Mock()
        
        # 创建订单处理器
        self.order_processor = OrderProcessor(
            self.mock_payment_service,
            self.mock_inventory_service,
            self.mock_notification_service
        )
    
    def test_complete_order_flow(self):
        """测试完整的订单流程"""
        # 准备测试数据
        cart = ShoppingCart()
        product1 = TestDataGenerator.generate_product(id=1, price=50.0, stock=10)
        product2 = TestDataGenerator.generate_product(id=2, price=30.0, stock=5)
        
        cart.add_item(product1, 2)
        cart.add_item(product2, 1)
        cart.apply_discount_code('SAVE10')
        
        customer_info = TestDataGenerator.generate_customer_info()
        
        # 配置Mock服务
        self.mock_inventory_service.check_stock.return_value = True
        self.mock_payment_service.process_payment.return_value = {
            'success': True,
            'payment_id': 'PAY123456'
        }
        self.mock_notification_service.send_order_confirmation.return_value = True
        
        # 执行订单处理
        order = self.order_processor.process_order(cart, customer_info)
        
        # 验证订单结果
        self.assertIsNotNone(order)
        self.assertEqual(order['status'], 'confirmed')
        self.assertEqual(order['payment_id'], 'PAY123456')
        self.assertAlmostEqual(order['subtotal'], 130.0, places=2)  # 50*2 + 30*1
        self.assertAlmostEqual(order['discount'], 13.0, places=2)   # 10% of 130
        
        # 验证服务调用
        self.assertEqual(self.mock_inventory_service.check_stock.call_count, 2)
        self.mock_payment_service.process_payment.assert_called_once()
        self.assertEqual(self.mock_inventory_service.reduce_stock.call_count, 2)
        self.mock_notification_service.send_order_confirmation.assert_called_once()
    
    def test_order_flow_with_payment_failure(self):
        """测试支付失败的订单流程"""
        cart = ShoppingCart()
        product = TestDataGenerator.generate_product(price=100.0, stock=5)
        cart.add_item(product, 1)
        
        customer_info = TestDataGenerator.generate_customer_info()
        
        # 配置Mock服务 - 支付失败
        self.mock_inventory_service.check_stock.return_value = True
        self.mock_payment_service.process_payment.return_value = {
            'success': False,
            'error': '信用卡被拒绝'
        }
        
        # 验证抛出异常
        with self.assertRaises(RuntimeError) as context:
            self.order_processor.process_order(cart, customer_info)
        
        self.assertIn('支付失败', str(context.exception))
        
        # 验证库存没有被减少
        self.mock_inventory_service.reduce_stock.assert_not_called()
        
        # 验证没有发送通知
        self.mock_notification_service.send_order_confirmation.assert_not_called()


# ============ 测试覆盖率演示 ============

def demonstrate_coverage_analysis():
    """演示测试覆盖率分析"""
    print("Session22 示例4: 测试覆盖率和高级测试技巧")
    print("=" * 50)
    
    print("\n1. 测试数据生成演示")
    print("-" * 30)
    
    # 生成测试产品
    product = TestDataGenerator.generate_product()
    print(f"生成的产品: {product.name}, 价格: {product.price}, 库存: {product.stock}")
    
    # 生成客户信息
    customer = TestDataGenerator.generate_customer_info()
    print(f"生成的客户: {customer['name']}, 邮箱: {customer['email']}")
    
    # 生成信用卡号
    card_number = TestDataGenerator.generate_credit_card()
    print(f"生成的信用卡号: {card_number}")
    print(f"信用卡验证结果: {DataValidator.validate_credit_card(card_number)}")
    
    print("\n2. 购物车功能演示")
    print("-" * 30)
    
    cart = ShoppingCart()
    
    # 添加商品
    for i in range(3):
        product = TestDataGenerator.generate_product(
            name=f"商品{i+1}",
            price=random.uniform(20, 100),
            stock=10
        )
        cart.add_item(product, random.randint(1, 3))
    
    print(f"购物车商品数量: {cart.get_item_count()}")
    print(f"购物车小计: {cart.get_subtotal():.2f}")
    
    # 应用折扣
    cart.apply_discount_code('SAVE20')
    print(f"应用20%折扣后:")
    print(f"  折扣金额: {cart.get_discount_amount():.2f}")
    print(f"  税额: {cart.get_tax_amount():.2f}")
    print(f"  总计: {cart.get_total():.2f}")
    
    print("\n3. 数据验证演示")
    print("-" * 30)
    
    # 测试邮箱验证
    test_emails = [
        'valid@example.com',
        'invalid-email',
        'user@domain.com',
        '@invalid.com'
    ]
    
    for email in test_emails:
        is_valid = DataValidator.validate_email(email)
        print(f"邮箱 '{email}': {'有效' if is_valid else '无效'}")
    
    # 测试密码强度
    test_passwords = [
        'weak',
        'StrongPass123',
        'NoNumbers',
        'VeryStrongPassword123!'
    ]
    
    for password in test_passwords:
        result = DataValidator.validate_password(password)
        print(f"密码 '{password}': {'强' if result['is_strong'] else '弱'}")
    
    print("\n4. 边界值测试演示")
    print("-" * 30)
    
    product = TestDataGenerator.generate_product(price=100.0)
    
    # 测试折扣边界值
    boundary_discounts = [0, 10, 50, 100]
    for discount in boundary_discounts:
        try:
            discounted_price = product.apply_discount(discount)
            print(f"{discount}%折扣后价格: {discounted_price:.2f}")
        except ValueError as e:
            print(f"{discount}%折扣: 错误 - {e}")
    
    print("\n演示完成！")
    print("\n高级测试技巧要点:")
    print("- 使用测试数据生成器创建随机测试数据")
    print("- 参数化测试可以用相同逻辑测试多组数据")
    print("- 边界值测试确保边界条件的正确性")
    print("- 属性测试验证代码的不变性质")
    print("- 性能测试确保代码在可接受时间内执行")
    print("- 集成测试验证组件间的协作")
    print("- 测试覆盖率帮助发现未测试的代码路径")


if __name__ == '__main__':
    # 运行演示
    demonstrate_coverage_analysis()
    
    print("\n" + "=" * 50)
    print("运行单元测试")
    print("=" * 50)
    
    # 运行测试
    unittest.main(argv=[''], exit=False, verbosity=2)