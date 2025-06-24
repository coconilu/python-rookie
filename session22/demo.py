#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session22: 测试驱动开发 - 演示代码

本文件演示了测试驱动开发(TDD)的基本流程和最佳实践。
通过开发一个科学计算器来展示红绿重构循环。

作者: Python教程团队
创建日期: 2024-01-15
最后修改: 2024-01-15
"""

import unittest
import math
from typing import Union


class ScientificCalculator:
    """
    科学计算器类
    
    通过TDD方式开发的计算器，支持基本运算和科学计算功能。
    """
    
    def __init__(self):
        """初始化计算器"""
        self.history = []
        self.memory = 0
    
    def add(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """加法运算"""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("参数必须是数字")
        result = a + b
        self._add_to_history(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """减法运算"""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("参数必须是数字")
        result = a - b
        self._add_to_history(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """乘法运算"""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("参数必须是数字")
        result = a * b
        self._add_to_history(f"{a} × {b} = {result}")
        return result
    
    def divide(self, a: Union[int, float], b: Union[int, float]) -> float:
        """除法运算"""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("参数必须是数字")
        if b == 0:
            raise ZeroDivisionError("除数不能为零")
        result = a / b
        self._add_to_history(f"{a} ÷ {b} = {result}")
        return result
    
    def power(self, base: Union[int, float], exponent: Union[int, float]) -> Union[int, float]:
        """幂运算"""
        if not isinstance(base, (int, float)) or not isinstance(exponent, (int, float)):
            raise TypeError("参数必须是数字")
        result = base ** exponent
        self._add_to_history(f"{base} ^ {exponent} = {result}")
        return result
    
    def square_root(self, x: Union[int, float]) -> float:
        """平方根运算"""
        if not isinstance(x, (int, float)):
            raise TypeError("参数必须是数字")
        if x < 0:
            raise ValueError("不能计算负数的平方根")
        result = math.sqrt(x)
        self._add_to_history(f"√{x} = {result}")
        return result
    
    def sin(self, x: Union[int, float]) -> float:
        """正弦函数"""
        if not isinstance(x, (int, float)):
            raise TypeError("参数必须是数字")
        result = math.sin(x)
        self._add_to_history(f"sin({x}) = {result}")
        return result
    
    def cos(self, x: Union[int, float]) -> float:
        """余弦函数"""
        if not isinstance(x, (int, float)):
            raise TypeError("参数必须是数字")
        result = math.cos(x)
        self._add_to_history(f"cos({x}) = {result}")
        return result
    
    def log(self, x: Union[int, float], base: Union[int, float] = math.e) -> float:
        """对数函数"""
        if not isinstance(x, (int, float)) or not isinstance(base, (int, float)):
            raise TypeError("参数必须是数字")
        if x <= 0:
            raise ValueError("真数必须大于0")
        if base <= 0 or base == 1:
            raise ValueError("底数必须大于0且不等于1")
        result = math.log(x, base)
        self._add_to_history(f"log_{base}({x}) = {result}")
        return result
    
    def factorial(self, n: int) -> int:
        """阶乘运算"""
        if not isinstance(n, int):
            raise TypeError("参数必须是整数")
        if n < 0:
            raise ValueError("不能计算负数的阶乘")
        result = math.factorial(n)
        self._add_to_history(f"{n}! = {result}")
        return result
    
    def memory_store(self, value: Union[int, float]) -> None:
        """存储到内存"""
        if not isinstance(value, (int, float)):
            raise TypeError("值必须是数字")
        self.memory = value
        self._add_to_history(f"M = {value}")
    
    def memory_recall(self) -> Union[int, float]:
        """从内存读取"""
        self._add_to_history(f"MR = {self.memory}")
        return self.memory
    
    def memory_clear(self) -> None:
        """清除内存"""
        self.memory = 0
        self._add_to_history("MC")
    
    def get_history(self) -> list:
        """获取计算历史"""
        return self.history.copy()
    
    def clear_history(self) -> None:
        """清除计算历史"""
        self.history.clear()
    
    def _add_to_history(self, operation: str) -> None:
        """添加操作到历史记录"""
        self.history.append(operation)
        # 限制历史记录数量
        if len(self.history) > 100:
            self.history.pop(0)


class TestScientificCalculator(unittest.TestCase):
    """
    科学计算器的单元测试
    
    演示TDD的测试编写方法和最佳实践。
    """
    
    def setUp(self):
        """每个测试方法执行前的设置"""
        self.calc = ScientificCalculator()
    
    def tearDown(self):
        """每个测试方法执行后的清理"""
        pass
    
    # 基本运算测试
    def test_add_positive_numbers(self):
        """测试正数加法"""
        result = self.calc.add(2, 3)
        self.assertEqual(result, 5)
    
    def test_add_negative_numbers(self):
        """测试负数加法"""
        result = self.calc.add(-2, -3)
        self.assertEqual(result, -5)
    
    def test_add_mixed_numbers(self):
        """测试正负数混合加法"""
        result = self.calc.add(-2, 3)
        self.assertEqual(result, 1)
    
    def test_add_with_zero(self):
        """测试与零相加"""
        self.assertEqual(self.calc.add(5, 0), 5)
        self.assertEqual(self.calc.add(0, 5), 5)
    
    def test_add_invalid_type(self):
        """测试无效类型参数"""
        with self.assertRaises(TypeError):
            self.calc.add("2", 3)
        with self.assertRaises(TypeError):
            self.calc.add(2, "3")
    
    def test_subtract(self):
        """测试减法"""
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(3, 5), -2)
        self.assertEqual(self.calc.subtract(-2, -3), 1)
    
    def test_multiply(self):
        """测试乘法"""
        self.assertEqual(self.calc.multiply(3, 4), 12)
        self.assertEqual(self.calc.multiply(-2, 3), -6)
        self.assertEqual(self.calc.multiply(0, 5), 0)
    
    def test_divide(self):
        """测试除法"""
        self.assertEqual(self.calc.divide(10, 2), 5)
        self.assertEqual(self.calc.divide(7, 2), 3.5)
        self.assertAlmostEqual(self.calc.divide(1, 3), 0.3333333333333333)
    
    def test_divide_by_zero(self):
        """测试除零异常"""
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(10, 0)
    
    # 科学计算测试
    def test_power(self):
        """测试幂运算"""
        self.assertEqual(self.calc.power(2, 3), 8)
        self.assertEqual(self.calc.power(5, 0), 1)
        self.assertAlmostEqual(self.calc.power(4, 0.5), 2)
    
    def test_square_root(self):
        """测试平方根"""
        self.assertEqual(self.calc.square_root(4), 2)
        self.assertEqual(self.calc.square_root(9), 3)
        self.assertAlmostEqual(self.calc.square_root(2), 1.4142135623730951)
    
    def test_square_root_negative(self):
        """测试负数平方根异常"""
        with self.assertRaises(ValueError):
            self.calc.square_root(-1)
    
    def test_trigonometric_functions(self):
        """测试三角函数"""
        # 测试特殊角度
        self.assertAlmostEqual(self.calc.sin(0), 0)
        self.assertAlmostEqual(self.calc.cos(0), 1)
        self.assertAlmostEqual(self.calc.sin(math.pi/2), 1)
        self.assertAlmostEqual(self.calc.cos(math.pi/2), 0, places=10)
    
    def test_logarithm(self):
        """测试对数函数"""
        self.assertAlmostEqual(self.calc.log(math.e), 1)
        self.assertAlmostEqual(self.calc.log(10, 10), 1)
        self.assertAlmostEqual(self.calc.log(8, 2), 3)
    
    def test_logarithm_invalid_input(self):
        """测试对数函数无效输入"""
        with self.assertRaises(ValueError):
            self.calc.log(-1)  # 负数真数
        with self.assertRaises(ValueError):
            self.calc.log(10, -1)  # 负数底数
        with self.assertRaises(ValueError):
            self.calc.log(10, 1)  # 底数为1
    
    def test_factorial(self):
        """测试阶乘"""
        self.assertEqual(self.calc.factorial(0), 1)
        self.assertEqual(self.calc.factorial(1), 1)
        self.assertEqual(self.calc.factorial(5), 120)
    
    def test_factorial_invalid_input(self):
        """测试阶乘无效输入"""
        with self.assertRaises(ValueError):
            self.calc.factorial(-1)
        with self.assertRaises(TypeError):
            self.calc.factorial(3.5)
    
    # 内存功能测试
    def test_memory_operations(self):
        """测试内存操作"""
        # 初始内存应为0
        self.assertEqual(self.calc.memory_recall(), 0)
        
        # 存储值到内存
        self.calc.memory_store(42)
        self.assertEqual(self.calc.memory_recall(), 42)
        
        # 清除内存
        self.calc.memory_clear()
        self.assertEqual(self.calc.memory_recall(), 0)
    
    def test_memory_store_invalid_type(self):
        """测试内存存储无效类型"""
        with self.assertRaises(TypeError):
            self.calc.memory_store("invalid")
    
    # 历史记录测试
    def test_history_tracking(self):
        """测试历史记录功能"""
        # 初始历史应为空
        self.assertEqual(len(self.calc.get_history()), 0)
        
        # 执行一些操作
        self.calc.add(2, 3)
        self.calc.multiply(4, 5)
        
        # 检查历史记录
        history = self.calc.get_history()
        self.assertEqual(len(history), 2)
        self.assertIn("2 + 3 = 5", history)
        self.assertIn("4 × 5 = 20", history)
    
    def test_clear_history(self):
        """测试清除历史记录"""
        self.calc.add(1, 1)
        self.calc.clear_history()
        self.assertEqual(len(self.calc.get_history()), 0)
    
    def test_history_limit(self):
        """测试历史记录数量限制"""
        # 执行超过100次操作
        for i in range(105):
            self.calc.add(i, 1)
        
        # 历史记录应限制在100条
        history = self.calc.get_history()
        self.assertEqual(len(history), 100)
        # 最早的记录应被删除
        self.assertNotIn("0 + 1 = 1", history)
        self.assertIn("104 + 1 = 105", history)


def demonstrate_tdd_process():
    """
    演示TDD开发流程
    
    展示红绿重构循环的实际应用。
    """
    print("Session22: 测试驱动开发演示")
    print("=" * 50)
    
    print("\n1. TDD流程演示")
    print("-" * 30)
    
    # 创建计算器实例
    calc = ScientificCalculator()
    
    print("步骤1: 红 - 编写失败的测试")
    print("# 假设我们要添加一个新功能：百分比计算")
    print("# def test_percentage():")
    print("#     assert calc.percentage(50, 200) == 25  # 50是200的25%")
    
    print("\n步骤2: 绿 - 编写最少代码使测试通过")
    print("# def percentage(self, part, whole):")
    print("#     return (part / whole) * 100")
    
    print("\n步骤3: 重构 - 改进代码质量")
    print("# 添加类型检查、异常处理、文档等")
    
    print("\n2. 基本功能演示")
    print("-" * 30)
    
    # 演示基本运算
    operations = [
        ("加法", lambda: calc.add(10, 5)),
        ("减法", lambda: calc.subtract(10, 5)),
        ("乘法", lambda: calc.multiply(10, 5)),
        ("除法", lambda: calc.divide(10, 5)),
        ("幂运算", lambda: calc.power(2, 3)),
        ("平方根", lambda: calc.square_root(16)),
    ]
    
    for name, operation in operations:
        try:
            result = operation()
            print(f"{name}: {result}")
        except Exception as e:
            print(f"{name}: 错误 - {e}")
    
    print("\n3. 科学计算演示")
    print("-" * 30)
    
    # 演示科学计算
    scientific_ops = [
        ("sin(π/2)", lambda: calc.sin(math.pi/2)),
        ("cos(0)", lambda: calc.cos(0)),
        ("log(e)", lambda: calc.log(math.e)),
        ("5!", lambda: calc.factorial(5)),
    ]
    
    for name, operation in scientific_ops:
        try:
            result = operation()
            print(f"{name}: {result}")
        except Exception as e:
            print(f"{name}: 错误 - {e}")
    
    print("\n4. 内存功能演示")
    print("-" * 30)
    
    calc.memory_store(42)
    print(f"存储到内存: 42")
    print(f"从内存读取: {calc.memory_recall()}")
    calc.memory_clear()
    print(f"清除内存后: {calc.memory_recall()}")
    
    print("\n5. 历史记录演示")
    print("-" * 30)
    
    history = calc.get_history()
    print(f"操作历史记录 ({len(history)}条):")
    for i, record in enumerate(history[-5:], 1):  # 显示最后5条
        print(f"  {i}. {record}")
    
    print("\n6. 异常处理演示")
    print("-" * 30)
    
    error_cases = [
        ("除零错误", lambda: calc.divide(10, 0)),
        ("负数平方根", lambda: calc.square_root(-1)),
        ("类型错误", lambda: calc.add("a", 1)),
        ("负数阶乘", lambda: calc.factorial(-1)),
    ]
    
    for name, operation in error_cases:
        try:
            operation()
            print(f"{name}: 未捕获到预期异常")
        except Exception as e:
            print(f"{name}: {type(e).__name__} - {e}")
    
    print("\n演示完成！")
    print("\nTDD的核心价值:")
    print("- 更好的代码设计")
    print("- 更高的代码质量")
    print("- 更安全的重构")
    print("- 活文档和规范")


def run_tests():
    """
    运行所有测试
    """
    print("\n" + "=" * 50)
    print("运行单元测试")
    print("=" * 50)
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestScientificCalculator)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 显示测试结果摘要
    print(f"\n测试摘要:")
    print(f"运行测试: {result.testsRun}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print(f"成功率: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")


def main():
    """
    主函数：演示程序的入口点
    """
    demonstrate_tdd_process()
    run_tests()


if __name__ == "__main__":
    main()