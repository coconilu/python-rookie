#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session08: 面向对象编程基础 - 演示代码

本文件演示了面向对象编程的基本概念和用法，包括：
- 类的定义和实例化
- 构造函数的使用
- 实例方法的定义和调用
- 实例变量和类变量
- 特殊方法的使用

作者: Python教程团队
创建日期: 2024-01-08
最后修改: 2024-01-08
"""

import math
from datetime import datetime


def main():
    """
    主函数：演示面向对象编程的基本概念
    """
    print("Session08: 面向对象编程基础演示")
    print("=" * 50)
    
    # 1. 基本类的定义和使用
    print("\n1. 基本类的定义和使用")
    print("-" * 30)
    demo_basic_class()
    
    # 2. 构造函数和实例变量
    print("\n2. 构造函数和实例变量")
    print("-" * 30)
    demo_constructor()
    
    # 3. 实例方法
    print("\n3. 实例方法")
    print("-" * 30)
    demo_instance_methods()
    
    # 4. 类变量vs实例变量
    print("\n4. 类变量vs实例变量")
    print("-" * 30)
    demo_class_vs_instance_variables()
    
    # 5. 特殊方法
    print("\n5. 特殊方法")
    print("-" * 30)
    demo_special_methods()
    
    # 6. 综合应用示例
    print("\n6. 综合应用示例")
    print("-" * 30)
    demo_comprehensive_example()
    
    print("\n演示完成！")


def demo_basic_class():
    """
    演示基本类的定义和使用
    """
    
    class Person:
        """人员类"""
        pass
    
    # 创建对象
    person1 = Person()
    person2 = Person()
    
    print(f"person1的类型: {type(person1)}")
    print(f"person2的类型: {type(person2)}")
    print(f"person1和person2是同一个对象吗? {person1 is person2}")
    
    # 动态添加属性
    person1.name = "张三"
    person1.age = 25
    
    print(f"person1的姓名: {person1.name}")
    print(f"person1的年龄: {person1.age}")
    
    # person2没有这些属性
    try:
        print(f"person2的姓名: {person2.name}")
    except AttributeError as e:
        print(f"错误: {e}")


def demo_constructor():
    """
    演示构造函数和实例变量
    """
    
    class Student:
        """学生类"""
        
        def __init__(self, name, age, student_id):
            """构造函数"""
            self.name = name
            self.age = age
            self.student_id = student_id
            self.courses = []  # 选课列表
            self.enrollment_date = datetime.now().strftime("%Y-%m-%d")
    
    # 创建学生对象
    student1 = Student("李四", 20, "2023001")
    student2 = Student("王五", 19, "2023002")
    
    print(f"学生1: {student1.name}, 年龄: {student1.age}, 学号: {student1.student_id}")
    print(f"学生2: {student2.name}, 年龄: {student2.age}, 学号: {student2.student_id}")
    print(f"入学日期: {student1.enrollment_date}")


def demo_instance_methods():
    """
    演示实例方法的定义和使用
    """
    
    class Rectangle:
        """矩形类"""
        
        def __init__(self, width, height):
            """初始化矩形"""
            self.width = width
            self.height = height
        
        def get_area(self):
            """计算面积"""
            return self.width * self.height
        
        def get_perimeter(self):
            """计算周长"""
            return 2 * (self.width + self.height)
        
        def is_square(self):
            """判断是否为正方形"""
            return self.width == self.height
        
        def resize(self, new_width, new_height):
            """调整大小"""
            old_area = self.get_area()
            self.width = new_width
            self.height = new_height
            new_area = self.get_area()
            print(f"矩形大小已调整: {old_area} -> {new_area}")
    
    # 创建矩形对象
    rect1 = Rectangle(5, 3)
    rect2 = Rectangle(4, 4)
    
    print(f"矩形1: 宽={rect1.width}, 高={rect1.height}")
    print(f"矩形1面积: {rect1.get_area()}")
    print(f"矩形1周长: {rect1.get_perimeter()}")
    print(f"矩形1是正方形吗? {rect1.is_square()}")
    
    print(f"\n矩形2: 宽={rect2.width}, 高={rect2.height}")
    print(f"矩形2是正方形吗? {rect2.is_square()}")
    
    # 调整矩形大小
    rect1.resize(6, 4)
    print(f"调整后矩形1面积: {rect1.get_area()}")


def demo_class_vs_instance_variables():
    """
    演示类变量和实例变量的区别
    """
    
    class Car:
        """汽车类"""
        
        # 类变量
        total_cars = 0
        manufacturer = "通用汽车公司"
        
        def __init__(self, brand, model, year):
            """构造函数"""
            # 实例变量
            self.brand = brand
            self.model = model
            self.year = year
            self.mileage = 0
            
            # 每创建一辆车，总数加1
            Car.total_cars += 1
            self.car_id = Car.total_cars
        
        def drive(self, distance):
            """行驶"""
            self.mileage += distance
            print(f"{self.brand} {self.model} 行驶了 {distance} 公里")
        
        @classmethod
        def get_total_cars(cls):
            """获取汽车总数（类方法）"""
            return cls.total_cars
        
        def get_car_info(self):
            """获取汽车信息"""
            return f"ID: {self.car_id}, {self.brand} {self.model} ({self.year}年), 里程: {self.mileage}km"
    
    # 创建汽车对象
    car1 = Car("丰田", "凯美瑞", 2022)
    car2 = Car("本田", "雅阁", 2023)
    car3 = Car("大众", "帕萨特", 2021)
    
    print(f"制造商: {Car.manufacturer}")
    print(f"汽车总数: {Car.get_total_cars()}")
    
    print("\n汽车信息:")
    print(car1.get_car_info())
    print(car2.get_car_info())
    print(car3.get_car_info())
    
    # 汽车行驶
    car1.drive(100)
    car2.drive(50)
    
    print("\n行驶后的信息:")
    print(car1.get_car_info())
    print(car2.get_car_info())
    
    # 修改类变量
    Car.manufacturer = "新能源汽车公司"
    print(f"\n更新后的制造商: {car1.manufacturer}")
    print(f"更新后的制造商: {car2.manufacturer}")


def demo_special_methods():
    """
    演示特殊方法的使用
    """
    
    class Circle:
        """圆形类"""
        
        def __init__(self, radius):
            """初始化圆形"""
            self.radius = radius
        
        def get_area(self):
            """计算面积"""
            return math.pi * self.radius ** 2
        
        def get_circumference(self):
            """计算周长"""
            return 2 * math.pi * self.radius
        
        def __str__(self):
            """字符串表示（用户友好）"""
            return f"半径为{self.radius}的圆形"
        
        def __repr__(self):
            """字符串表示（开发者友好）"""
            return f"Circle(radius={self.radius})"
        
        def __eq__(self, other):
            """相等比较"""
            if isinstance(other, Circle):
                return self.radius == other.radius
            return False
        
        def __lt__(self, other):
            """小于比较"""
            if isinstance(other, Circle):
                return self.radius < other.radius
            return NotImplemented
        
        def __add__(self, other):
            """加法运算（合并两个圆的面积）"""
            if isinstance(other, Circle):
                total_area = self.get_area() + other.get_area()
                new_radius = math.sqrt(total_area / math.pi)
                return Circle(new_radius)
            return NotImplemented
    
    # 创建圆形对象
    circle1 = Circle(5)
    circle2 = Circle(3)
    circle3 = Circle(5)
    
    print(f"圆形1: {circle1}")  # 调用__str__
    print(f"圆形2: {circle2}")
    print(f"repr表示: {repr(circle1)}")  # 调用__repr__
    
    print(f"\n圆形1面积: {circle1.get_area():.2f}")
    print(f"圆形1周长: {circle1.get_circumference():.2f}")
    
    # 比较操作
    print(f"\n圆形1 == 圆形3: {circle1 == circle3}")  # 调用__eq__
    print(f"圆形1 == 圆形2: {circle1 == circle2}")
    print(f"圆形2 < 圆形1: {circle2 < circle1}")  # 调用__lt__
    
    # 加法操作
    combined_circle = circle1 + circle2  # 调用__add__
    print(f"\n合并后的圆形: {combined_circle}")
    print(f"合并后面积: {combined_circle.get_area():.2f}")


def demo_comprehensive_example():
    """
    综合应用示例：图书管理系统
    """
    
    class Book:
        """图书类"""
        
        # 类变量
        total_books = 0
        library_name = "Python学习图书馆"
        
        def __init__(self, title, author, isbn, price):
            """初始化图书"""
            self.title = title
            self.author = author
            self.isbn = isbn
            self.price = price
            self.is_borrowed = False
            self.borrower = None
            self.borrow_date = None
            
            Book.total_books += 1
            self.book_id = Book.total_books
        
        def borrow(self, borrower_name):
            """借书"""
            if not self.is_borrowed:
                self.is_borrowed = True
                self.borrower = borrower_name
                self.borrow_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return f"《{self.title}》借阅成功！借阅人：{borrower_name}"
            else:
                return f"《{self.title}》已被{self.borrower}借阅"
        
        def return_book(self):
            """还书"""
            if self.is_borrowed:
                borrower = self.borrower
                self.is_borrowed = False
                self.borrower = None
                self.borrow_date = None
                return f"《{self.title}》归还成功！归还人：{borrower}"
            else:
                return f"《{self.title}》未被借阅"
        
        def get_status(self):
            """获取图书状态"""
            if self.is_borrowed:
                return f"已借出 - 借阅人：{self.borrower}，借阅时间：{self.borrow_date}"
            else:
                return "可借阅"
        
        def __str__(self):
            """字符串表示"""
            return f"《{self.title}》- {self.author} (¥{self.price})"
        
        def __repr__(self):
            """开发者字符串表示"""
            return f"Book('{self.title}', '{self.author}', '{self.isbn}', {self.price})"
        
        @classmethod
        def get_library_info(cls):
            """获取图书馆信息"""
            return f"{cls.library_name} - 总藏书量：{cls.total_books}本"
    
    # 创建图书对象
    book1 = Book("Python编程从入门到实践", "埃里克·马瑟斯", "978-7-115-42802-8", 89.0)
    book2 = Book("流畅的Python", "Luciano Ramalho", "978-7-115-45415-7", 139.0)
    book3 = Book("Python核心编程", "Wesley Chun", "978-7-115-23183-9", 99.0)
    
    print(Book.get_library_info())
    print("\n图书列表:")
    books = [book1, book2, book3]
    for book in books:
        print(f"ID: {book.book_id}, {book}, 状态: {book.get_status()}")
    
    print("\n借阅操作:")
    print(book1.borrow("张三"))
    print(book2.borrow("李四"))
    print(book1.borrow("王五"))  # 尝试借阅已被借出的书
    
    print("\n当前状态:")
    for book in books:
        print(f"{book}: {book.get_status()}")
    
    print("\n归还操作:")
    print(book1.return_book())
    
    print("\n最终状态:")
    for book in books:
        print(f"{book}: {book.get_status()}")


if __name__ == "__main__":
    main()