#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session29 练习1解决方案: 单元测试基础

这是exercise1.py的完整解决方案，展示了如何编写全面的单元测试。

作者: Python教程团队
"""

import unittest
from typing import List, Dict, Any


class ShoppingCart:
    """购物车类 - 用于单元测试练习"""
    
    def __init__(self):
        self.items = {}  # {product_name: {'price': float, 'quantity': int}}
        self.discount = 0.0  # 折扣率 (0.0 - 1.0)
    
    def add_item(self, product_name: str, price: float, quantity: int = 1):
        """添加商品到购物车"""
        if not product_name or not product_name.strip():
            raise ValueError("商品名称不能为空")
        
        if price < 0:
            raise ValueError("商品价格不能为负数")
        
        if quantity <= 0:
            raise ValueError("商品数量必须大于0")
        
        product_name = product_name.strip()
        
        if product_name in self.items:
            self.items[product_name]['quantity'] += quantity
        else:
            self.items[product_name] = {'price': price, 'quantity': quantity}
    
    def remove_item(self, product_name: str, quantity: int = None):
        """从购物车移除商品"""
        if not product_name or not product_name.strip():
            raise ValueError("商品名称不能为空")
        
        product_name = product_name.strip()
        
        if product_name not in self.items:
            raise KeyError(f"商品 '{product_name}' 不在购物车中")
        
        if quantity is None:
            # 移除所有该商品
            del self.items[product_name]
        else:
            if quantity <= 0:
                raise ValueError("移除数量必须大于0")
            
            current_quantity = self.items[product_name]['quantity']
            
            if quantity >= current_quantity:
                del self.items[product_name]
            else:
                self.items[product_name]['quantity'] -= quantity
    
    def get_item_count(self, product_name: str) -> int:
        """获取指定商品的数量"""
        if not product_name or not product_name.strip():
            raise ValueError("商品名称不能为空")
        
        product_name = product_name.strip()
        return self.items.get(product_name, {}).get('quantity', 0)
    
    def get_total_items(self) -> int:
        """获取购物车中商品的总数量"""
        return sum(item['quantity'] for item in self.items.values())
    
    def calculate_total(self) -> float:
        """计算购物车总价"""
        subtotal = sum(item['price'] * item['quantity'] for item in self.items.values())
        total = subtotal * (1 - self.discount)
        return round(total, 2)
    
    def apply_discount(self, discount_rate: float):
        """应用折扣"""
        if discount_rate < 0 or discount_rate > 1:
            raise ValueError("折扣率必须在0到1之间")
        
        self.discount = discount_rate
    
    def clear_cart(self):
        """清空购物车"""
        self.items.clear()
        self.discount = 0.0
    
    def is_empty(self) -> bool:
        """检查购物车是否为空"""
        return len(self.items) == 0
    
    def get_items_list(self) -> List[Dict[str, Any]]:
        """获取购物车商品列表"""
        return [
            {
                'name': name,
                'price': item['price'],
                'quantity': item['quantity'],
                'subtotal': item['price'] * item['quantity']
            }
            for name, item in self.items.items()
        ]


class TestShoppingCart(unittest.TestCase):
    """购物车单元测试 - 完整解决方案"""
    
    def setUp(self):
        """每个测试方法执行前的设置"""
        self.cart = ShoppingCart()
    
    def tearDown(self):
        """每个测试方法执行后的清理"""
        self.cart = None
    
    # 基础功能测试
    def test_empty_cart_initialization(self):
        """测试空购物车初始化"""
        self.assertTrue(self.cart.is_empty())
        self.assertEqual(self.cart.get_total_items(), 0)
        self.assertEqual(self.cart.calculate_total(), 0.0)
        self.assertEqual(len(self.cart.items), 0)
    
    def test_add_single_item(self):
        """测试添加单个商品"""
        self.cart.add_item("苹果", 5.0, 3)
        
        self.assertFalse(self.cart.is_empty())
        self.assertEqual(self.cart.get_item_count("苹果"), 3)
        self.assertEqual(self.cart.get_total_items(), 3)
        self.assertEqual(self.cart.calculate_total(), 15.0)
    
    def test_add_multiple_items(self):
        """测试添加多个不同商品"""
        self.cart.add_item("苹果", 5.0, 2)
        self.cart.add_item("香蕉", 3.0, 4)
        self.cart.add_item("橙子", 4.0, 1)
        
        self.assertEqual(self.cart.get_total_items(), 7)
        self.assertEqual(self.cart.calculate_total(), 26.0)  # 10 + 12 + 4
        self.assertEqual(len(self.cart.items), 3)
    
    def test_add_same_item_multiple_times(self):
        """测试多次添加同一商品"""
        self.cart.add_item("苹果", 5.0, 2)
        self.cart.add_item("苹果", 5.0, 3)
        
        self.assertEqual(self.cart.get_item_count("苹果"), 5)
        self.assertEqual(self.cart.get_total_items(), 5)
        self.assertEqual(self.cart.calculate_total(), 25.0)
    
    def test_remove_item_completely(self):
        """测试完全移除商品"""
        self.cart.add_item("苹果", 5.0, 3)
        self.cart.add_item("香蕉", 3.0, 2)
        
        self.cart.remove_item("苹果")
        
        self.assertEqual(self.cart.get_item_count("苹果"), 0)
        self.assertEqual(self.cart.get_total_items(), 2)
        self.assertEqual(self.cart.calculate_total(), 6.0)
    
    def test_remove_item_partially(self):
        """测试部分移除商品"""
        self.cart.add_item("苹果", 5.0, 5)
        
        self.cart.remove_item("苹果", 2)
        
        self.assertEqual(self.cart.get_item_count("苹果"), 3)
        self.assertEqual(self.cart.calculate_total(), 15.0)
    
    def test_remove_more_than_available(self):
        """测试移除数量超过现有数量"""
        self.cart.add_item("苹果", 5.0, 3)
        
        self.cart.remove_item("苹果", 5)  # 移除5个，但只有3个
        
        self.assertEqual(self.cart.get_item_count("苹果"), 0)
        self.assertTrue(self.cart.is_empty())
    
    def test_apply_discount(self):
        """测试应用折扣"""
        self.cart.add_item("苹果", 10.0, 2)  # 总价20.0
        
        self.cart.apply_discount(0.1)  # 10%折扣
        
        self.assertEqual(self.cart.calculate_total(), 18.0)  # 20 * 0.9
    
    def test_clear_cart(self):
        """测试清空购物车"""
        self.cart.add_item("苹果", 5.0, 3)
        self.cart.add_item("香蕉", 3.0, 2)
        self.cart.apply_discount(0.1)
        
        self.cart.clear_cart()
        
        self.assertTrue(self.cart.is_empty())
        self.assertEqual(self.cart.get_total_items(), 0)
        self.assertEqual(self.cart.calculate_total(), 0.0)
        self.assertEqual(self.cart.discount, 0.0)
    
    def test_get_items_list(self):
        """测试获取商品列表"""
        self.cart.add_item("苹果", 5.0, 2)
        self.cart.add_item("香蕉", 3.0, 3)
        
        items_list = self.cart.get_items_list()
        
        self.assertEqual(len(items_list), 2)
        
        # 检查苹果
        apple_item = next(item for item in items_list if item['name'] == '苹果')
        self.assertEqual(apple_item['price'], 5.0)
        self.assertEqual(apple_item['quantity'], 2)
        self.assertEqual(apple_item['subtotal'], 10.0)
        
        # 检查香蕉
        banana_item = next(item for item in items_list if item['name'] == '香蕉')
        self.assertEqual(banana_item['price'], 3.0)
        self.assertEqual(banana_item['quantity'], 3)
        self.assertEqual(banana_item['subtotal'], 9.0)
    
    # 异常情况测试
    def test_add_item_empty_name(self):
        """测试添加空名称商品"""
        with self.assertRaises(ValueError) as context:
            self.cart.add_item("", 5.0, 1)
        
        self.assertIn("商品名称不能为空", str(context.exception))
    
    def test_add_item_whitespace_name(self):
        """测试添加只有空格的商品名称"""
        with self.assertRaises(ValueError):
            self.cart.add_item("   ", 5.0, 1)
    
    def test_add_item_negative_price(self):
        """测试添加负价格商品"""
        with self.assertRaises(ValueError) as context:
            self.cart.add_item("苹果", -5.0, 1)
        
        self.assertIn("商品价格不能为负数", str(context.exception))
    
    def test_add_item_zero_quantity(self):
        """测试添加零数量商品"""
        with self.assertRaises(ValueError) as context:
            self.cart.add_item("苹果", 5.0, 0)
        
        self.assertIn("商品数量必须大于0", str(context.exception))
    
    def test_add_item_negative_quantity(self):
        """测试添加负数量商品"""
        with self.assertRaises(ValueError):
            self.cart.add_item("苹果", 5.0, -1)
    
    def test_remove_nonexistent_item(self):
        """测试移除不存在的商品"""
        with self.assertRaises(KeyError) as context:
            self.cart.remove_item("不存在的商品")
        
        self.assertIn("不在购物车中", str(context.exception))
    
    def test_remove_item_empty_name(self):
        """测试移除空名称商品"""
        with self.assertRaises(ValueError):
            self.cart.remove_item("")
    
    def test_remove_item_zero_quantity(self):
        """测试移除零数量"""
        self.cart.add_item("苹果", 5.0, 3)
        
        with self.assertRaises(ValueError) as context:
            self.cart.remove_item("苹果", 0)
        
        self.assertIn("移除数量必须大于0", str(context.exception))
    
    def test_remove_item_negative_quantity(self):
        """测试移除负数量"""
        self.cart.add_item("苹果", 5.0, 3)
        
        with self.assertRaises(ValueError):
            self.cart.remove_item("苹果", -1)
    
    def test_get_item_count_nonexistent(self):
        """测试获取不存在商品的数量"""
        count = self.cart.get_item_count("不存在的商品")
        self.assertEqual(count, 0)
    
    def test_get_item_count_empty_name(self):
        """测试获取空名称商品数量"""
        with self.assertRaises(ValueError):
            self.cart.get_item_count("")
    
    def test_apply_invalid_discount(self):
        """测试应用无效折扣"""
        # 测试负折扣
        with self.assertRaises(ValueError) as context:
            self.cart.apply_discount(-0.1)
        
        self.assertIn("折扣率必须在0到1之间", str(context.exception))
        
        # 测试超过1的折扣
        with self.assertRaises(ValueError):
            self.cart.apply_discount(1.5)
    
    # 边界值测试
    def test_zero_price_item(self):
        """测试零价格商品"""
        self.cart.add_item("免费样品", 0.0, 1)
        
        self.assertEqual(self.cart.calculate_total(), 0.0)
        self.assertEqual(self.cart.get_total_items(), 1)
    
    def test_maximum_discount(self):
        """测试最大折扣"""
        self.cart.add_item("苹果", 10.0, 1)
        self.cart.apply_discount(1.0)  # 100%折扣
        
        self.assertEqual(self.cart.calculate_total(), 0.0)
    
    def test_no_discount(self):
        """测试无折扣"""
        self.cart.add_item("苹果", 10.0, 1)
        self.cart.apply_discount(0.0)  # 0%折扣
        
        self.assertEqual(self.cart.calculate_total(), 10.0)
    
    def test_name_with_spaces(self):
        """测试商品名称包含空格"""
        self.cart.add_item("  苹果  ", 5.0, 1)
        
        # 名称应该被trim
        self.assertEqual(self.cart.get_item_count("苹果"), 1)
        self.assertEqual(self.cart.get_item_count("  苹果  "), 1)
    
    # 复杂场景测试
    def test_complex_shopping_scenario(self):
        """测试复杂购物场景"""
        # 添加多种商品
        self.cart.add_item("苹果", 5.0, 3)
        self.cart.add_item("香蕉", 3.0, 2)
        self.cart.add_item("橙子", 4.0, 1)
        
        # 再次添加苹果
        self.cart.add_item("苹果", 5.0, 2)
        
        # 部分移除香蕉
        self.cart.remove_item("香蕉", 1)
        
        # 应用折扣
        self.cart.apply_discount(0.1)
        
        # 验证最终状态
        self.assertEqual(self.cart.get_item_count("苹果"), 5)  # 3 + 2
        self.assertEqual(self.cart.get_item_count("香蕉"), 1)  # 2 - 1
        self.assertEqual(self.cart.get_item_count("橙子"), 1)
        self.assertEqual(self.cart.get_total_items(), 7)
        
        # 总价计算: (5*5 + 3*1 + 4*1) * 0.9 = 32 * 0.9 = 28.8
        self.assertEqual(self.cart.calculate_total(), 28.8)
    
    def test_multiple_discounts(self):
        """测试多次应用折扣"""
        self.cart.add_item("苹果", 10.0, 1)
        
        self.cart.apply_discount(0.1)  # 10%折扣
        self.assertEqual(self.cart.calculate_total(), 9.0)
        
        self.cart.apply_discount(0.2)  # 改为20%折扣
        self.assertEqual(self.cart.calculate_total(), 8.0)
    
    # 参数化测试示例（如果使用pytest）
    def test_various_quantities(self):
        """测试各种数量"""
        test_cases = [
            (1, 5.0),
            (10, 50.0),
            (100, 500.0),
            (1000, 5000.0)
        ]
        
        for quantity, expected_total in test_cases:
            with self.subTest(quantity=quantity):
                cart = ShoppingCart()
                cart.add_item("测试商品", 5.0, quantity)
                self.assertEqual(cart.calculate_total(), expected_total)
    
    def test_various_prices(self):
        """测试各种价格"""
        test_cases = [
            (0.01, 0.01),
            (1.0, 1.0),
            (99.99, 99.99),
            (1000.0, 1000.0)
        ]
        
        for price, expected_total in test_cases:
            with self.subTest(price=price):
                cart = ShoppingCart()
                cart.add_item("测试商品", price, 1)
                self.assertEqual(cart.calculate_total(), expected_total)


def run_tests():
    """运行所有单元测试"""
    print("运行购物车单元测试...")
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestShoppingCart)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出测试统计
    print(f"\n测试统计:")
    print(f"运行测试: {result.testsRun}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print(f"跳过: {len(result.skipped)}")
    
    if result.failures:
        print("\n失败的测试:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\n错误的测试:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("Session29 练习1解决方案: 单元测试基础")
    print("=" * 50)
    
    print("\n这个解决方案展示了:")
    print("1. 完整的单元测试覆盖")
    print("2. 正常情况和异常情况的测试")
    print("3. 边界值测试")
    print("4. 复杂场景测试")
    print("5. 测试组织和最佳实践")
    
    print("\n开始运行测试...")
    success = run_tests()
    
    if success:
        print("\n🎉 所有测试都通过了！")
        print("\n学到的测试技巧:")
        print("- setUp和tearDown的使用")
        print("- 异常测试with assertRaises")
        print("- 子测试subTest的使用")
        print("- 测试用例的组织和命名")
        print("- 边界值和异常情况的覆盖")
    else:
        print("\n❌ 有测试失败，请检查实现")