#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session22 练习1：TDD基础练习

通过实际编程练习掌握TDD的基本流程：红-绿-重构。

练习目标：
1. 理解TDD的基本流程
2. 学会先写测试再写实现
3. 掌握unittest的基本用法
4. 练习重构技巧

作者: Python教程团队
创建日期: 2024-01-15
"""

import unittest
from typing import List, Dict, Optional
from datetime import datetime, timedelta


# ============ 练习1：银行账户类 ============

class BankAccount:
    """
    银行账户类
    
    要求实现以下功能：
    1. 创建账户时设置初始余额
    2. 存款功能
    3. 取款功能（余额不足时抛出异常）
    4. 查询余额
    5. 获取交易历史
    6. 计算利息（年利率3%）
    
    请按照TDD流程实现：
    1. 先运行测试（应该失败）
    2. 编写最少的代码让测试通过
    3. 重构代码
    """
    
    def __init__(self, initial_balance: float = 0.0):
        """初始化银行账户"""
        # TODO: 实现初始化逻辑
        pass
    
    def deposit(self, amount: float) -> None:
        """存款"""
        # TODO: 实现存款逻辑
        pass
    
    def withdraw(self, amount: float) -> None:
        """取款"""
        # TODO: 实现取款逻辑
        pass
    
    def get_balance(self) -> float:
        """获取余额"""
        # TODO: 实现获取余额逻辑
        pass
    
    def get_transaction_history(self) -> List[Dict]:
        """获取交易历史"""
        # TODO: 实现获取交易历史逻辑
        pass
    
    def calculate_interest(self, days: int) -> float:
        """计算利息"""
        # TODO: 实现利息计算逻辑（年利率3%）
        pass


class TestBankAccount(unittest.TestCase):
    """银行账户测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.account = BankAccount(1000.0)
    
    def test_initial_balance(self):
        """测试初始余额"""
        # 测试创建账户时的初始余额
        account = BankAccount(500.0)
        self.assertEqual(account.get_balance(), 500.0)
        
        # 测试默认初始余额
        default_account = BankAccount()
        self.assertEqual(default_account.get_balance(), 0.0)
    
    def test_deposit(self):
        """测试存款功能"""
        initial_balance = self.account.get_balance()
        
        # 存款200元
        self.account.deposit(200.0)
        self.assertEqual(self.account.get_balance(), initial_balance + 200.0)
        
        # 再存款300元
        self.account.deposit(300.0)
        self.assertEqual(self.account.get_balance(), initial_balance + 500.0)
    
    def test_deposit_invalid_amount(self):
        """测试无效存款金额"""
        # 存款金额不能为负数
        with self.assertRaises(ValueError):
            self.account.deposit(-100.0)
        
        # 存款金额不能为零
        with self.assertRaises(ValueError):
            self.account.deposit(0.0)
    
    def test_withdraw(self):
        """测试取款功能"""
        initial_balance = self.account.get_balance()
        
        # 取款200元
        self.account.withdraw(200.0)
        self.assertEqual(self.account.get_balance(), initial_balance - 200.0)
        
        # 再取款300元
        self.account.withdraw(300.0)
        self.assertEqual(self.account.get_balance(), initial_balance - 500.0)
    
    def test_withdraw_insufficient_funds(self):
        """测试余额不足时取款"""
        # 尝试取款超过余额的金额
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(1500.0)
        
        self.assertIn("余额不足", str(context.exception))
        
        # 余额应该保持不变
        self.assertEqual(self.account.get_balance(), 1000.0)
    
    def test_withdraw_invalid_amount(self):
        """测试无效取款金额"""
        # 取款金额不能为负数
        with self.assertRaises(ValueError):
            self.account.withdraw(-100.0)
        
        # 取款金额不能为零
        with self.assertRaises(ValueError):
            self.account.withdraw(0.0)
    
    def test_transaction_history(self):
        """测试交易历史"""
        # 初始状态应该没有交易记录
        history = self.account.get_transaction_history()
        self.assertEqual(len(history), 0)
        
        # 进行一些交易
        self.account.deposit(200.0)
        self.account.withdraw(100.0)
        self.account.deposit(50.0)
        
        # 检查交易历史
        history = self.account.get_transaction_history()
        self.assertEqual(len(history), 3)
        
        # 检查第一笔交易
        first_transaction = history[0]
        self.assertEqual(first_transaction['type'], 'deposit')
        self.assertEqual(first_transaction['amount'], 200.0)
        self.assertIn('timestamp', first_transaction)
        
        # 检查第二笔交易
        second_transaction = history[1]
        self.assertEqual(second_transaction['type'], 'withdraw')
        self.assertEqual(second_transaction['amount'], 100.0)
        
        # 检查第三笔交易
        third_transaction = history[2]
        self.assertEqual(third_transaction['type'], 'deposit')
        self.assertEqual(third_transaction['amount'], 50.0)
    
    def test_calculate_interest(self):
        """测试利息计算"""
        # 年利率3%，1000元存30天的利息
        # 利息 = 1000 * 0.03 * (30/365) ≈ 2.47
        interest = self.account.calculate_interest(30)
        expected_interest = 1000.0 * 0.03 * (30 / 365)
        self.assertAlmostEqual(interest, expected_interest, places=2)
        
        # 测试365天（一年）的利息
        yearly_interest = self.account.calculate_interest(365)
        expected_yearly = 1000.0 * 0.03
        self.assertAlmostEqual(yearly_interest, expected_yearly, places=2)
        
        # 测试零余额的利息
        zero_account = BankAccount(0.0)
        zero_interest = zero_account.calculate_interest(30)
        self.assertEqual(zero_interest, 0.0)


# ============ 练习2：图书管理系统 ============

class Book:
    """
    图书类
    
    要求实现以下功能：
    1. 图书基本信息（ISBN、标题、作者、出版年份）
    2. 图书状态（可借、已借出、维修中）
    3. 借阅和归还功能
    """
    
    def __init__(self, isbn: str, title: str, author: str, year: int):
        """初始化图书"""
        # TODO: 实现初始化逻辑
        pass
    
    def is_available(self) -> bool:
        """检查图书是否可借"""
        # TODO: 实现可借检查逻辑
        pass
    
    def borrow(self) -> bool:
        """借阅图书"""
        # TODO: 实现借阅逻辑
        pass
    
    def return_book(self) -> bool:
        """归还图书"""
        # TODO: 实现归还逻辑
        pass
    
    def set_maintenance(self) -> None:
        """设置为维修状态"""
        # TODO: 实现设置维修状态逻辑
        pass


class Library:
    """
    图书馆类
    
    要求实现以下功能：
    1. 添加图书
    2. 移除图书
    3. 按ISBN查找图书
    4. 按标题搜索图书
    5. 按作者搜索图书
    6. 获取可借图书列表
    7. 获取已借出图书列表
    """
    
    def __init__(self):
        """初始化图书馆"""
        # TODO: 实现初始化逻辑
        pass
    
    def add_book(self, book: Book) -> bool:
        """添加图书"""
        # TODO: 实现添加图书逻辑
        pass
    
    def remove_book(self, isbn: str) -> bool:
        """移除图书"""
        # TODO: 实现移除图书逻辑
        pass
    
    def find_book_by_isbn(self, isbn: str) -> Optional[Book]:
        """按ISBN查找图书"""
        # TODO: 实现按ISBN查找逻辑
        pass
    
    def search_by_title(self, title: str) -> List[Book]:
        """按标题搜索图书"""
        # TODO: 实现按标题搜索逻辑
        pass
    
    def search_by_author(self, author: str) -> List[Book]:
        """按作者搜索图书"""
        # TODO: 实现按作者搜索逻辑
        pass
    
    def get_available_books(self) -> List[Book]:
        """获取可借图书列表"""
        # TODO: 实现获取可借图书逻辑
        pass
    
    def get_borrowed_books(self) -> List[Book]:
        """获取已借出图书列表"""
        # TODO: 实现获取已借出图书逻辑
        pass
    
    def get_total_books(self) -> int:
        """获取图书总数"""
        # TODO: 实现获取图书总数逻辑
        pass


class TestBook(unittest.TestCase):
    """图书测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.book = Book("978-0134685991", "Effective Python", "Brett Slatkin", 2019)
    
    def test_book_creation(self):
        """测试图书创建"""
        self.assertEqual(self.book.isbn, "978-0134685991")
        self.assertEqual(self.book.title, "Effective Python")
        self.assertEqual(self.book.author, "Brett Slatkin")
        self.assertEqual(self.book.year, 2019)
    
    def test_book_initially_available(self):
        """测试图书初始状态为可借"""
        self.assertTrue(self.book.is_available())
    
    def test_borrow_book(self):
        """测试借阅图书"""
        # 借阅成功
        result = self.book.borrow()
        self.assertTrue(result)
        self.assertFalse(self.book.is_available())
        
        # 已借出的图书不能再次借阅
        result = self.book.borrow()
        self.assertFalse(result)
    
    def test_return_book(self):
        """测试归还图书"""
        # 先借阅图书
        self.book.borrow()
        self.assertFalse(self.book.is_available())
        
        # 归还图书
        result = self.book.return_book()
        self.assertTrue(result)
        self.assertTrue(self.book.is_available())
        
        # 可用图书不能归还
        result = self.book.return_book()
        self.assertFalse(result)
    
    def test_maintenance_status(self):
        """测试维修状态"""
        # 设置为维修状态
        self.book.set_maintenance()
        self.assertFalse(self.book.is_available())
        
        # 维修中的图书不能借阅
        result = self.book.borrow()
        self.assertFalse(result)


class TestLibrary(unittest.TestCase):
    """图书馆测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.library = Library()
        self.book1 = Book("978-0134685991", "Effective Python", "Brett Slatkin", 2019)
        self.book2 = Book("978-0596009250", "Learning Python", "Mark Lutz", 2013)
        self.book3 = Book("978-1491946008", "Fluent Python", "Luciano Ramalho", 2015)
    
    def test_add_book(self):
        """测试添加图书"""
        # 添加图书
        result = self.library.add_book(self.book1)
        self.assertTrue(result)
        self.assertEqual(self.library.get_total_books(), 1)
        
        # 添加重复ISBN的图书应该失败
        duplicate_book = Book("978-0134685991", "Another Title", "Another Author", 2020)
        result = self.library.add_book(duplicate_book)
        self.assertFalse(result)
        self.assertEqual(self.library.get_total_books(), 1)
    
    def test_remove_book(self):
        """测试移除图书"""
        # 先添加图书
        self.library.add_book(self.book1)
        self.assertEqual(self.library.get_total_books(), 1)
        
        # 移除图书
        result = self.library.remove_book(self.book1.isbn)
        self.assertTrue(result)
        self.assertEqual(self.library.get_total_books(), 0)
        
        # 移除不存在的图书
        result = self.library.remove_book("nonexistent")
        self.assertFalse(result)
    
    def test_find_book_by_isbn(self):
        """测试按ISBN查找图书"""
        # 添加图书
        self.library.add_book(self.book1)
        
        # 查找存在的图书
        found_book = self.library.find_book_by_isbn(self.book1.isbn)
        self.assertIsNotNone(found_book)
        self.assertEqual(found_book.title, "Effective Python")
        
        # 查找不存在的图书
        not_found = self.library.find_book_by_isbn("nonexistent")
        self.assertIsNone(not_found)
    
    def test_search_by_title(self):
        """测试按标题搜索图书"""
        # 添加图书
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        self.library.add_book(self.book3)
        
        # 搜索包含"Python"的图书
        python_books = self.library.search_by_title("Python")
        self.assertEqual(len(python_books), 3)
        
        # 搜索特定标题
        effective_books = self.library.search_by_title("Effective")
        self.assertEqual(len(effective_books), 1)
        self.assertEqual(effective_books[0].title, "Effective Python")
        
        # 搜索不存在的标题
        not_found = self.library.search_by_title("Java")
        self.assertEqual(len(not_found), 0)
    
    def test_search_by_author(self):
        """测试按作者搜索图书"""
        # 添加图书
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        
        # 搜索特定作者
        brett_books = self.library.search_by_author("Brett Slatkin")
        self.assertEqual(len(brett_books), 1)
        self.assertEqual(brett_books[0].title, "Effective Python")
        
        # 搜索部分作者名
        lutz_books = self.library.search_by_author("Lutz")
        self.assertEqual(len(lutz_books), 1)
        
        # 搜索不存在的作者
        not_found = self.library.search_by_author("Unknown Author")
        self.assertEqual(len(not_found), 0)
    
    def test_available_and_borrowed_books(self):
        """测试可借和已借出图书列表"""
        # 添加图书
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        self.library.add_book(self.book3)
        
        # 初始状态：所有图书都可借
        available = self.library.get_available_books()
        borrowed = self.library.get_borrowed_books()
        self.assertEqual(len(available), 3)
        self.assertEqual(len(borrowed), 0)
        
        # 借阅一本图书
        self.book1.borrow()
        available = self.library.get_available_books()
        borrowed = self.library.get_borrowed_books()
        self.assertEqual(len(available), 2)
        self.assertEqual(len(borrowed), 1)
        
        # 设置一本图书为维修状态
        self.book2.set_maintenance()
        available = self.library.get_available_books()
        self.assertEqual(len(available), 1)  # 只有book3可借


# ============ 练习指导 ============

def exercise_instructions():
    """练习指导"""
    print("Session22 练习1: TDD基础练习")
    print("=" * 50)
    
    print("\n练习说明：")
    print("1. 请按照TDD流程完成以下练习：")
    print("   - 红：运行测试，确保测试失败")
    print("   - 绿：编写最少的代码让测试通过")
    print("   - 重构：改进代码质量，保持测试通过")
    
    print("\n2. 练习1：银行账户类")
    print("   - 实现BankAccount类的所有方法")
    print("   - 确保所有测试用例通过")
    print("   - 注意异常处理和边界条件")
    
    print("\n3. 练习2：图书管理系统")
    print("   - 实现Book类和Library类")
    print("   - 考虑图书状态管理")
    print("   - 实现搜索功能")
    
    print("\n4. TDD最佳实践：")
    print("   - 测试应该简单、快速、独立")
    print("   - 一次只关注一个功能")
    print("   - 测试名称应该清楚描述测试内容")
    print("   - 使用setUp和tearDown管理测试环境")
    
    print("\n5. 运行测试：")
    print("   python -m unittest exercise1_basic_tdd.py -v")
    
    print("\n开始练习吧！记住：先写测试，再写实现！")


if __name__ == '__main__':
    # 显示练习指导
    exercise_instructions()
    
    print("\n" + "=" * 50)
    print("运行测试（当前应该失败，因为还没有实现）")
    print("=" * 50)
    
    # 运行测试
    unittest.main(argv=[''], exit=False, verbosity=2)