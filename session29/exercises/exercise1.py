#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session29 练习1: 单元测试基础

练习目标:
1. 编写基本的单元测试
2. 使用unittest框架
3. 测试正常情况和异常情况
4. 使用断言验证结果

练习说明:
请为下面的类编写完整的单元测试，包括：
- 测试所有公共方法
- 测试边界条件
- 测试异常情况
- 使用setUp和tearDown方法

作者: Python教程团队
"""

import unittest
from typing import List, Dict, Optional


class ShoppingCart:
    """购物车类 - 需要为此类编写测试"""
    
    def __init__(self):
        self.items = {}  # {product_id: {'name': str, 'price': float, 'quantity': int}}
        self.discount_rate = 0.0
    
    def add_item(self, product_id: str, name: str, price: float, quantity: int = 1):
        """添加商品到购物车"""
        if not product_id or not name:
            raise ValueError("商品ID和名称不能为空")
        
        if price < 0:
            raise ValueError("商品价格不能为负数")
        
        if quantity <= 0:
            raise ValueError("商品数量必须大于0")
        
        if product_id in self.items:
            self.items[product_id]['quantity'] += quantity
        else:
            self.items[product_id] = {
                'name': name,
                'price': price,
                'quantity': quantity
            }
    
    def remove_item(self, product_id: str, quantity: int = None):
        """从购物车移除商品"""
        if product_id not in self.items:
            raise KeyError(f"商品 {product_id} 不在购物车中")
        
        if quantity is None:
            # 移除所有数量
            del self.items[product_id]
        else:
            if quantity <= 0:
                raise ValueError("移除数量必须大于0")
            
            current_quantity = self.items[product_id]['quantity']
            if quantity >= current_quantity:
                del self.items[product_id]
            else:
                self.items[product_id]['quantity'] -= quantity
    
    def update_quantity(self, product_id: str, new_quantity: int):
        """更新商品数量"""
        if product_id not in self.items:
            raise KeyError(f"商品 {product_id} 不在购物车中")
        
        if new_quantity <= 0:
            raise ValueError("商品数量必须大于0")
        
        self.items[product_id]['quantity'] = new_quantity
    
    def get_item_count(self) -> int:
        """获取商品种类数量"""
        return len(self.items)
    
    def get_total_quantity(self) -> int:
        """获取商品总数量"""
        return sum(item['quantity'] for item in self.items.values())
    
    def get_subtotal(self) -> float:
        """获取小计金额（不含折扣）"""
        return sum(item['price'] * item['quantity'] for item in self.items.values())
    
    def set_discount(self, discount_rate: float):
        """设置折扣率"""
        if not 0 <= discount_rate <= 1:
            raise ValueError("折扣率必须在0到1之间")
        
        self.discount_rate = discount_rate
    
    def get_total(self) -> float:
        """获取总金额（含折扣）"""
        subtotal = self.get_subtotal()
        return subtotal * (1 - self.discount_rate)
    
    def clear(self):
        """清空购物车"""
        self.items.clear()
        self.discount_rate = 0.0
    
    def get_items(self) -> Dict:
        """获取购物车中的所有商品"""
        return self.items.copy()
    
    def is_empty(self) -> bool:
        """检查购物车是否为空"""
        return len(self.items) == 0


# TODO: 请在下面编写测试类
class TestShoppingCart(unittest.TestCase):
    """购物车测试类
    
    请完成以下测试方法：
    1. setUp方法 - 初始化测试环境
    2. tearDown方法 - 清理测试环境
    3. test_init - 测试初始化
    4. test_add_item_success - 测试成功添加商品
    5. test_add_item_invalid_params - 测试添加商品时的无效参数
    6. test_add_item_duplicate - 测试添加重复商品
    7. test_remove_item_success - 测试成功移除商品
    8. test_remove_item_not_found - 测试移除不存在的商品
    9. test_remove_item_partial - 测试部分移除商品
    10. test_update_quantity_success - 测试成功更新数量
    11. test_update_quantity_invalid - 测试无效的数量更新
    12. test_get_counts - 测试获取数量相关方法
    13. test_discount_functionality - 测试折扣功能
    14. test_total_calculation - 测试总金额计算
    15. test_clear_cart - 测试清空购物车
    16. test_empty_cart_operations - 测试空购物车的操作
    """
    
    def setUp(self):
        """每个测试方法执行前的准备工作"""
        # TODO: 创建购物车实例
        pass
    
    def tearDown(self):
        """每个测试方法执行后的清理工作"""
        # TODO: 清理测试环境
        pass
    
    def test_init(self):
        """测试购物车初始化"""
        # TODO: 验证购物车初始状态
        # 提示：检查items是否为空字典，discount_rate是否为0
        pass
    
    def test_add_item_success(self):
        """测试成功添加商品"""
        # TODO: 测试添加单个商品
        # 提示：添加商品后检查items字典的内容
        pass
    
    def test_add_item_invalid_params(self):
        """测试添加商品时的无效参数"""
        # TODO: 测试各种无效参数情况
        # 提示：使用assertRaises测试异常
        # 测试情况：空product_id、空name、负价格、零数量等
        pass
    
    def test_add_item_duplicate(self):
        """测试添加重复商品"""
        # TODO: 测试添加相同product_id的商品
        # 提示：验证数量是否正确累加
        pass
    
    def test_remove_item_success(self):
        """测试成功移除商品"""
        # TODO: 测试移除商品的各种情况
        # 提示：先添加商品，然后测试移除
        pass
    
    def test_remove_item_not_found(self):
        """测试移除不存在的商品"""
        # TODO: 测试移除不存在的商品
        # 提示：应该抛出KeyError
        pass
    
    def test_remove_item_partial(self):
        """测试部分移除商品"""
        # TODO: 测试部分移除商品数量
        # 提示：添加数量为5的商品，然后移除2个，验证剩余3个
        pass
    
    def test_update_quantity_success(self):
        """测试成功更新数量"""
        # TODO: 测试更新商品数量
        pass
    
    def test_update_quantity_invalid(self):
        """测试无效的数量更新"""
        # TODO: 测试更新不存在的商品和无效数量
        pass
    
    def test_get_counts(self):
        """测试获取数量相关方法"""
        # TODO: 测试get_item_count和get_total_quantity方法
        pass
    
    def test_discount_functionality(self):
        """测试折扣功能"""
        # TODO: 测试设置折扣和折扣计算
        pass
    
    def test_total_calculation(self):
        """测试总金额计算"""
        # TODO: 测试小计和总计的计算
        pass
    
    def test_clear_cart(self):
        """测试清空购物车"""
        # TODO: 测试清空购物车功能
        pass
    
    def test_empty_cart_operations(self):
        """测试空购物车的操作"""
        # TODO: 测试空购物车的各种操作
        pass


# 额外挑战：参数化测试
class TestShoppingCartParametrized(unittest.TestCase):
    """参数化测试示例
    
    挑战：使用subTest实现参数化测试
    """
    
    def setUp(self):
        self.cart = ShoppingCart()
    
    def test_add_multiple_items(self):
        """测试添加多种商品"""
        # TODO: 使用subTest测试添加多种不同的商品
        test_items = [
            ('item1', '苹果', 5.0, 3),
            ('item2', '香蕉', 3.0, 5),
            ('item3', '橙子', 4.0, 2),
        ]
        
        # 提示：使用 with self.subTest(item=item) 进行参数化测试
        pass
    
    def test_invalid_prices(self):
        """测试各种无效价格"""
        # TODO: 测试多种无效价格情况
        invalid_prices = [-1.0, -10.5, -0.01]
        
        # 提示：使用subTest测试每种无效价格
        pass


def run_tests():
    """运行测试"""
    print("运行购物车单元测试...")
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestShoppingCart))
    suite.addTests(loader.loadTestsFromTestCase(TestShoppingCartParametrized))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 显示结果
    print(f"\n测试结果:")
    print(f"运行测试数: {result.testsRun}")
    print(f"失败数: {len(result.failures)}")
    print(f"错误数: {len(result.errors)}")
    
    if result.failures:
        print("\n失败的测试:")
        for test, traceback in result.failures:
            print(f"- {test}")
    
    if result.errors:
        print("\n错误的测试:")
        for test, traceback in result.errors:
            print(f"- {test}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("Session29 练习1: 单元测试基础")
    print("=" * 50)
    
    print("\n练习说明:")
    print("1. 请完成TestShoppingCart类中的所有测试方法")
    print("2. 每个测试方法都有详细的TODO注释")
    print("3. 运行测试验证你的实现")
    print("4. 尝试完成参数化测试的挑战")
    
    print("\n开始测试...")
    success = run_tests()
    
    if success:
        print("\n🎉 恭喜！所有测试都通过了！")
    else:
        print("\n❌ 还有测试未通过，请检查你的实现")
    
    print("\n学习要点:")
    print("- unittest.TestCase是所有测试类的基类")
    print("- setUp和tearDown用于测试前后的准备和清理")
    print("- 使用各种assert方法验证结果")
    print("- assertRaises用于测试异常")
    print("- subTest可以实现参数化测试")