#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session22 示例1：unittest基础用法

演示unittest框架的基本功能和测试编写方法。

作者: Python教程团队
创建日期: 2024-01-15
"""

import unittest
import sys
import os


class Calculator:
    """简单计算器类 - 用于演示测试"""
    
    def add(self, a, b):
        """加法"""
        return a + b
    
    def subtract(self, a, b):
        """减法"""
        return a - b
    
    def multiply(self, a, b):
        """乘法"""
        return a * b
    
    def divide(self, a, b):
        """除法"""
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b
    
    def is_even(self, n):
        """判断是否为偶数"""
        if not isinstance(n, int):
            raise TypeError("Input must be an integer")
        return n % 2 == 0


class TestCalculator(unittest.TestCase):
    """计算器测试类"""
    
    def setUp(self):
        """测试前置设置 - 每个测试方法执行前调用"""
        self.calc = Calculator()
        print(f"\n设置测试环境: {self._testMethodName}")
    
    def tearDown(self):
        """测试后置清理 - 每个测试方法执行后调用"""
        print(f"清理测试环境: {self._testMethodName}")
    
    @classmethod
    def setUpClass(cls):
        """类级别设置 - 整个测试类执行前调用一次"""
        print("\n=== 开始Calculator测试 ===")
    
    @classmethod
    def tearDownClass(cls):
        """类级别清理 - 整个测试类执行后调用一次"""
        print("\n=== Calculator测试完成 ===")
    
    # 基本断言测试
    def test_add_positive_numbers(self):
        """测试正数加法"""
        result = self.calc.add(2, 3)
        self.assertEqual(result, 5, "2 + 3 应该等于 5")
    
    def test_add_negative_numbers(self):
        """测试负数加法"""
        result = self.calc.add(-2, -3)
        self.assertEqual(result, -5)
    
    def test_subtract(self):
        """测试减法"""
        self.assertEqual(self.calc.subtract(10, 3), 7)
        self.assertEqual(self.calc.subtract(3, 10), -7)
    
    def test_multiply(self):
        """测试乘法"""
        self.assertEqual(self.calc.multiply(4, 5), 20)
        self.assertEqual(self.calc.multiply(-2, 3), -6)
        self.assertEqual(self.calc.multiply(0, 100), 0)
    
    def test_divide(self):
        """测试除法"""
        self.assertEqual(self.calc.divide(10, 2), 5)
        self.assertAlmostEqual(self.calc.divide(1, 3), 0.3333333333333333)
    
    # 异常测试
    def test_divide_by_zero(self):
        """测试除零异常"""
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(10, 0)
    
    def test_divide_by_zero_with_message(self):
        """测试除零异常及错误消息"""
        with self.assertRaisesRegex(ZeroDivisionError, "Cannot divide by zero"):
            self.calc.divide(5, 0)
    
    # 类型检查测试
    def test_is_even_with_valid_input(self):
        """测试偶数判断 - 有效输入"""
        self.assertTrue(self.calc.is_even(4))
        self.assertFalse(self.calc.is_even(3))
        self.assertTrue(self.calc.is_even(0))
        self.assertTrue(self.calc.is_even(-2))
    
    def test_is_even_with_invalid_input(self):
        """测试偶数判断 - 无效输入"""
        with self.assertRaises(TypeError):
            self.calc.is_even(3.5)
        with self.assertRaises(TypeError):
            self.calc.is_even("4")
    
    # 多种断言方法演示
    def test_various_assertions(self):
        """演示各种断言方法"""
        # 相等性断言
        self.assertEqual(self.calc.add(1, 1), 2)
        self.assertNotEqual(self.calc.add(1, 1), 3)
        
        # 布尔断言
        self.assertTrue(self.calc.is_even(4))
        self.assertFalse(self.calc.is_even(3))
        
        # None断言
        result = None
        self.assertIsNone(result)
        
        calc_instance = self.calc
        self.assertIsNotNone(calc_instance)
        
        # 身份断言
        self.assertIs(self.calc, self.calc)
        self.assertIsNot(self.calc, Calculator())
        
        # 包含断言
        numbers = [1, 2, 3, 4, 5]
        self.assertIn(3, numbers)
        self.assertNotIn(6, numbers)
        
        # 类型断言
        self.assertIsInstance(self.calc.add(1, 2), int)
        self.assertIsInstance(self.calc.divide(1, 2), float)
    
    # 跳过测试演示
    @unittest.skip("演示跳过测试")
    def test_skipped_test(self):
        """这个测试会被跳过"""
        self.fail("这个测试不应该运行")
    
    @unittest.skipIf(sys.version_info < (3, 8), "需要Python 3.8+")
    def test_conditional_skip(self):
        """条件跳过测试"""
        self.assertTrue(True)
    
    @unittest.skipUnless(os.name == 'nt', "仅在Windows上运行")
    def test_windows_only(self):
        """仅在Windows上运行的测试"""
        self.assertTrue(True)
    
    # 预期失败测试
    @unittest.expectedFailure
    def test_expected_failure(self):
        """预期失败的测试"""
        self.assertEqual(1, 2, "这个测试预期会失败")


class TestCalculatorAdvanced(unittest.TestCase):
    """高级测试技巧演示"""
    
    def setUp(self):
        self.calc = Calculator()
    
    def test_with_subtest(self):
        """使用子测试"""
        test_cases = [
            (2, 3, 5),
            (0, 0, 0),
            (-1, 1, 0),
            (10, -5, 5)
        ]
        
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                result = self.calc.add(a, b)
                self.assertEqual(result, expected)
    
    def test_multiple_assertions(self):
        """多个断言的测试"""
        # 使用assertAll模式（自定义实现）
        errors = []
        
        try:
            self.assertEqual(self.calc.add(1, 1), 2)
        except AssertionError as e:
            errors.append(str(e))
        
        try:
            self.assertEqual(self.calc.multiply(2, 3), 6)
        except AssertionError as e:
            errors.append(str(e))
        
        try:
            self.assertEqual(self.calc.subtract(5, 2), 3)
        except AssertionError as e:
            errors.append(str(e))
        
        if errors:
            self.fail("Multiple assertions failed:\n" + "\n".join(errors))


def create_test_suite():
    """创建自定义测试套件"""
    suite = unittest.TestSuite()
    
    # 添加特定测试
    suite.addTest(TestCalculator('test_add_positive_numbers'))
    suite.addTest(TestCalculator('test_divide_by_zero'))
    
    # 添加整个测试类
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCalculatorAdvanced))
    
    return suite


def run_specific_tests():
    """运行特定测试"""
    print("\n运行特定测试:")
    print("-" * 40)
    
    # 创建测试套件
    suite = create_test_suite()
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


def demonstrate_test_discovery():
    """演示测试发现"""
    print("\n测试发现演示:")
    print("-" * 40)
    
    # 发现当前目录下的所有测试
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__) or '.'
    suite = loader.discover(start_dir, pattern='example1*.py')
    
    print(f"发现的测试数量: {suite.countTestCases()}")
    
    # 运行发现的测试
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    
    return result


def main():
    """主函数"""
    print("Session22 示例1: unittest基础用法")
    print("=" * 50)
    
    print("\n1. 运行所有测试")
    print("-" * 30)
    
    # 运行所有测试
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # 运行特定测试
    run_specific_tests()
    
    # 演示测试发现
    # demonstrate_test_discovery()
    
    print("\n示例1演示完成！")
    print("\n学习要点:")
    print("- unittest.TestCase是所有测试类的基类")
    print("- setUp/tearDown用于测试前后的准备和清理")
    print("- 各种断言方法用于验证结果")
    print("- 异常测试使用assertRaises")
    print("- 可以跳过或标记预期失败的测试")


if __name__ == '__main__':
    main()