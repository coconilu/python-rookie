#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session08 练习题1参考答案：图书类设计

这是exercise1.py的参考答案，展示了如何设计一个完整的Book类。
"""


class Book:
    """图书类 - 管理图书信息和库存"""
    
    # 类变量
    total_books = 0
    library_name = "Python图书馆"
    
    def __init__(self, title, author, isbn, price, stock=0):
        """初始化图书信息
        
        Args:
            title (str): 书名
            author (str): 作者
            isbn (str): ISBN号
            price (float): 价格
            stock (int): 库存数量，默认为0
        
        Raises:
            ValueError: 当价格或库存为负数时
            TypeError: 当参数类型不正确时
        """
        # 参数验证
        if not isinstance(title, str) or not title.strip():
            raise ValueError("书名必须是非空字符串")
        if not isinstance(author, str) or not author.strip():
            raise ValueError("作者必须是非空字符串")
        if not isinstance(isbn, str) or not isbn.strip():
            raise ValueError("ISBN必须是非空字符串")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("价格必须是非负数")
        if not isinstance(stock, int) or stock < 0:
            raise ValueError("库存必须是非负整数")
        
        # 初始化实例变量
        self.title = title.strip()
        self.author = author.strip()
        self.isbn = isbn.strip()
        self.price = float(price)
        self.stock = stock
        
        # 更新图书总数
        Book.total_books += 1
        self.book_id = Book.total_books
    
    def get_info(self):
        """获取图书信息
        
        Returns:
            str: 格式化的图书信息
        """
        return (
            f"图书ID: {self.book_id}\n"
            f"书名: 《{self.title}》\n"
            f"作者: {self.author}\n"
            f"ISBN: {self.isbn}\n"
            f"价格: ¥{self.price:.2f}\n"
            f"库存: {self.stock}本"
        )
    
    def purchase(self, quantity=1):
        """购买图书（减少库存）
        
        Args:
            quantity (int): 购买数量，默认为1
        
        Returns:
            bool: 购买是否成功
        
        Raises:
            ValueError: 当购买数量无效时
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("购买数量必须是正整数")
        
        if self.stock >= quantity:
            self.stock -= quantity
            total_price = self.price * quantity
            print(f"购买成功！《{self.title}》x{quantity}本，总价：¥{total_price:.2f}")
            print(f"剩余库存：{self.stock}本")
            return True
        else:
            print(f"库存不足！当前库存：{self.stock}本，需要：{quantity}本")
            return False
    
    def restock(self, quantity):
        """补充库存
        
        Args:
            quantity (int): 补充数量
        
        Raises:
            ValueError: 当补充数量无效时
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("补充数量必须是正整数")
        
        old_stock = self.stock
        self.stock += quantity
        print(f"库存补充成功！《{self.title}》库存：{old_stock} -> {self.stock}本")
    
    def has_stock(self, quantity=1):
        """判断是否有足够库存
        
        Args:
            quantity (int): 需要的数量，默认为1
        
        Returns:
            bool: 是否有足够库存
        """
        return self.stock >= quantity
    
    def calculate_discount_price(self, discount_rate):
        """计算折扣价格
        
        Args:
            discount_rate (float): 折扣率（0-1之间，如0.8表示8折）
        
        Returns:
            float: 折扣后价格
        
        Raises:
            ValueError: 当折扣率无效时
        """
        if not isinstance(discount_rate, (int, float)) or not (0 <= discount_rate <= 1):
            raise ValueError("折扣率必须在0-1之间")
        
        discount_price = self.price * discount_rate
        return round(discount_price, 2)
    
    def is_expensive(self, threshold=50.0):
        """判断图书是否昂贵
        
        Args:
            threshold (float): 价格阈值，默认50元
        
        Returns:
            bool: 是否昂贵
        """
        return self.price > threshold
    
    @classmethod
    def get_library_info(cls):
        """获取图书馆信息（类方法）
        
        Returns:
            str: 图书馆信息
        """
        return f"{cls.library_name} - 总藏书：{cls.total_books}本"
    
    @classmethod
    def create_from_string(cls, book_string):
        """从字符串创建图书对象（类方法）
        
        Args:
            book_string (str): 格式为"title,author,isbn,price,stock"的字符串
        
        Returns:
            Book: 图书对象
        """
        parts = book_string.split(',')
        if len(parts) != 5:
            raise ValueError("字符串格式错误，应为：title,author,isbn,price,stock")
        
        title, author, isbn, price, stock = parts
        return cls(title.strip(), author.strip(), isbn.strip(), 
                  float(price.strip()), int(stock.strip()))
    
    @staticmethod
    def is_valid_isbn(isbn):
        """验证ISBN格式（静态方法）
        
        Args:
            isbn (str): ISBN号
        
        Returns:
            bool: 是否为有效的ISBN格式
        """
        # 简化的ISBN验证（实际应该更复杂）
        if not isinstance(isbn, str):
            return False
        
        # 移除连字符
        clean_isbn = isbn.replace('-', '').replace(' ', '')
        
        # ISBN-10: 10位数字
        # ISBN-13: 13位数字
        return (len(clean_isbn) == 10 and clean_isbn.isdigit()) or \
               (len(clean_isbn) == 13 and clean_isbn.isdigit())
    
    def __str__(self):
        """字符串表示（用户友好）"""
        status = "有库存" if self.stock > 0 else "缺货"
        return f"《{self.title}》- {self.author} (¥{self.price:.2f}) [{status}]"
    
    def __repr__(self):
        """字符串表示（开发者友好）"""
        return f"Book('{self.title}', '{self.author}', '{self.isbn}', {self.price}, {self.stock})"
    
    def __eq__(self, other):
        """相等比较（按ISBN）"""
        if isinstance(other, Book):
            return self.isbn == other.isbn
        return False
    
    def __lt__(self, other):
        """小于比较（按价格）"""
        if isinstance(other, Book):
            return self.price < other.price
        return NotImplemented
    
    def __hash__(self):
        """哈希值（基于ISBN）"""
        return hash(self.isbn)


def test_book():
    """测试Book类的功能"""
    print("=== 图书类测试 ===")
    
    # 1. 创建图书对象
    print("\n1. 创建图书对象：")
    print("-" * 30)
    
    try:
        book1 = Book("Python编程从入门到实践", "埃里克·马瑟斯", "978-7-115-42802-8", 89.0, 10)
        book2 = Book("流畅的Python", "Luciano Ramalho", "978-7-115-45415-7", 139.0, 5)
        book3 = Book("Python核心编程", "Wesley Chun", "978-7-115-23183-9", 99.0, 0)
        
        print("图书创建成功！")
        print(Book.get_library_info())
        
    except ValueError as e:
        print(f"创建图书失败：{e}")
    
    # 2. 显示图书信息
    print("\n2. 图书信息：")
    print("-" * 30)
    
    books = [book1, book2, book3]
    for i, book in enumerate(books, 1):
        print(f"\n图书{i}：{book}")
        print(book.get_info())
    
    # 3. 测试购买功能
    print("\n3. 购买测试：")
    print("-" * 30)
    
    print("\n尝试购买book1（有库存）：")
    book1.purchase(2)
    
    print("\n尝试购买book3（无库存）：")
    book3.purchase(1)
    
    print("\n尝试购买超过库存的数量：")
    book1.purchase(20)
    
    # 4. 测试库存管理
    print("\n4. 库存管理：")
    print("-" * 30)
    
    print("\n补充book3的库存：")
    book3.restock(15)
    
    print("\n检查库存状态：")
    for book in books:
        print(f"{book.title}: 库存{book.stock}本，{'有货' if book.has_stock() else '缺货'}")
    
    # 5. 测试折扣价格
    print("\n5. 折扣价格计算：")
    print("-" * 30)
    
    for book in books:
        original_price = book.price
        discount_price = book.calculate_discount_price(0.8)  # 8折
        print(f"{book.title}: 原价¥{original_price:.2f} -> 8折¥{discount_price:.2f}")
    
    # 6. 测试静态方法和类方法
    print("\n6. 静态方法和类方法测试：")
    print("-" * 30)
    
    # 测试ISBN验证
    test_isbns = ["978-7-115-42802-8", "1234567890", "invalid", "9787115428028"]
    for isbn in test_isbns:
        is_valid = Book.is_valid_isbn(isbn)
        print(f"ISBN '{isbn}': {'有效' if is_valid else '无效'}")
    
    # 从字符串创建图书
    print("\n从字符串创建图书：")
    try:
        book4 = Book.create_from_string("算法导论,Thomas H. Cormen,978-0-262-03384-8,128.0,3")
        print(f"创建成功：{book4}")
    except ValueError as e:
        print(f"创建失败：{e}")
    
    # 7. 测试比较操作
    print("\n7. 比较操作：")
    print("-" * 30)
    
    print(f"book1 == book2: {book1 == book2}")
    print(f"book1 < book2: {book1 < book2}")
    print(f"book2 > book1: {book2 > book1}")
    
    # 按价格排序
    sorted_books = sorted(books)
    print("\n按价格排序：")
    for book in sorted_books:
        print(f"  {book.title}: ¥{book.price:.2f}")
    
    # 8. 测试异常处理
    print("\n8. 异常处理测试：")
    print("-" * 30)
    
    try:
        # 测试无效参数
        invalid_book = Book("", "作者", "isbn", -10, -5)
    except ValueError as e:
        print(f"捕获异常：{e}")
    
    try:
        # 测试无效购买数量
        book1.purchase(-1)
    except ValueError as e:
        print(f"捕获异常：{e}")
    
    try:
        # 测试无效折扣率
        book1.calculate_discount_price(1.5)
    except ValueError as e:
        print(f"捕获异常：{e}")
    
    # 9. 最终状态
    print("\n9. 最终状态：")
    print("-" * 30)
    
    print(Book.get_library_info())
    print("\n所有图书：")
    for book in books:
        print(f"  {book}")
    
    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    test_book()