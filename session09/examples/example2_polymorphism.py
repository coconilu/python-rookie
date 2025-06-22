#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session09 示例2: 多态

演示多态的概念和应用，包括：
- 方法重写实现多态
- 接口统一性
- 运行时类型确定
- 多态在实际应用中的优势

作者: Python教程团队
创建日期: 2024-01-09
"""

from abc import ABC, abstractmethod
import math


class Shape(ABC):
    """抽象形状类 - 定义统一接口"""
    
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def area(self):
        """计算面积 - 抽象方法"""
        pass
    
    @abstractmethod
    def perimeter(self):
        """计算周长 - 抽象方法"""
        pass
    
    def display_info(self):
        """显示形状信息 - 具体方法"""
        print(f"形状: {self.name}")
        print(f"面积: {self.area():.2f}")
        print(f"周长: {self.perimeter():.2f}")
        print("-" * 30)


class Rectangle(Shape):
    """矩形类"""
    
    def __init__(self, width, height):
        super().__init__("矩形")
        self.width = width
        self.height = height
    
    def area(self):
        """矩形面积"""
        return self.width * self.height
    
    def perimeter(self):
        """矩形周长"""
        return 2 * (self.width + self.height)
    
    def is_square(self):
        """判断是否为正方形"""
        return self.width == self.height


class Circle(Shape):
    """圆形类"""
    
    def __init__(self, radius):
        super().__init__("圆形")
        self.radius = radius
    
    def area(self):
        """圆形面积"""
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        """圆形周长"""
        return 2 * math.pi * self.radius
    
    def diameter(self):
        """直径"""
        return 2 * self.radius


class Triangle(Shape):
    """三角形类"""
    
    def __init__(self, side1, side2, side3):
        super().__init__("三角形")
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3
        
        # 验证三角形的有效性
        if not self._is_valid_triangle():
            raise ValueError("无效的三角形边长")
    
    def _is_valid_triangle(self):
        """验证三角形三边关系"""
        return (self.side1 + self.side2 > self.side3 and
                self.side1 + self.side3 > self.side2 and
                self.side2 + self.side3 > self.side1)
    
    def area(self):
        """使用海伦公式计算三角形面积"""
        s = self.perimeter() / 2  # 半周长
        return math.sqrt(s * (s - self.side1) * (s - self.side2) * (s - self.side3))
    
    def perimeter(self):
        """三角形周长"""
        return self.side1 + self.side2 + self.side3
    
    def triangle_type(self):
        """判断三角形类型"""
        sides = sorted([self.side1, self.side2, self.side3])
        if sides[0] == sides[1] == sides[2]:
            return "等边三角形"
        elif sides[0] == sides[1] or sides[1] == sides[2]:
            return "等腰三角形"
        else:
            return "普通三角形"


class Polygon(Shape):
    """多边形类"""
    
    def __init__(self, sides):
        if len(sides) < 3:
            raise ValueError("多边形至少需要3条边")
        
        super().__init__(f"{len(sides)}边形")
        self.sides = sides
    
    def perimeter(self):
        """多边形周长"""
        return sum(self.sides)
    
    def area(self):
        """简化计算：假设为正多边形"""
        n = len(self.sides)
        side_length = self.sides[0]  # 假设所有边相等
        
        # 正多边形面积公式
        apothem = side_length / (2 * math.tan(math.pi / n))
        return 0.5 * self.perimeter() * apothem


# 多态应用示例
class ShapeCalculator:
    """形状计算器 - 展示多态的应用"""
    
    def __init__(self):
        self.shapes = []
    
    def add_shape(self, shape):
        """添加形状"""
        if isinstance(shape, Shape):
            self.shapes.append(shape)
            print(f"✅ 已添加 {shape.name}")
        else:
            print("❌ 只能添加Shape类型的对象")
    
    def calculate_total_area(self):
        """计算总面积 - 多态应用"""
        total = 0
        print("\n📊 计算总面积:")
        for shape in self.shapes:
            area = shape.area()  # 多态：不同形状有不同的面积计算方法
            total += area
            print(f"  {shape.name}: {area:.2f}")
        
        print(f"\n🔢 总面积: {total:.2f}")
        return total
    
    def calculate_total_perimeter(self):
        """计算总周长 - 多态应用"""
        total = 0
        print("\n📏 计算总周长:")
        for shape in self.shapes:
            perimeter = shape.perimeter()  # 多态：不同形状有不同的周长计算方法
            total += perimeter
            print(f"  {shape.name}: {perimeter:.2f}")
        
        print(f"\n🔢 总周长: {total:.2f}")
        return total
    
    def find_largest_shape(self):
        """找到面积最大的形状"""
        if not self.shapes:
            print("没有形状可比较")
            return None
        
        largest = max(self.shapes, key=lambda s: s.area())  # 多态应用
        print(f"\n🏆 面积最大的形状: {largest.name} (面积: {largest.area():.2f})")
        return largest
    
    def display_all_shapes(self):
        """显示所有形状信息"""
        print("\n📋 所有形状信息:")
        print("=" * 40)
        for i, shape in enumerate(self.shapes, 1):
            print(f"第{i}个形状:")
            shape.display_info()  # 多态：统一的接口调用


# 动物多态示例
class Animal(ABC):
    """动物抽象基类"""
    
    def __init__(self, name, species):
        self.name = name
        self.species = species
    
    @abstractmethod
    def make_sound(self):
        """发出声音"""
        pass
    
    @abstractmethod
    def move(self):
        """移动方式"""
        pass
    
    def introduce(self):
        """自我介绍"""
        print(f"我是{self.species} {self.name}")
        self.make_sound()  # 多态调用
        self.move()  # 多态调用
        print()


class Dog(Animal):
    """狗类"""
    
    def __init__(self, name, breed):
        super().__init__(name, "狗")
        self.breed = breed
    
    def make_sound(self):
        print(f"{self.name} 汪汪叫")
    
    def move(self):
        print(f"{self.name} 在地上跑")
    
    def fetch(self):
        print(f"{self.name} 去捡球")


class Cat(Animal):
    """猫类"""
    
    def __init__(self, name, color):
        super().__init__(name, "猫")
        self.color = color
    
    def make_sound(self):
        print(f"{self.name} 喵喵叫")
    
    def move(self):
        print(f"{self.name} 优雅地走路")
    
    def climb(self):
        print(f"{self.name} 爬到树上")


class Bird(Animal):
    """鸟类"""
    
    def __init__(self, name, wingspan):
        super().__init__(name, "鸟")
        self.wingspan = wingspan
    
    def make_sound(self):
        print(f"{self.name} 啾啾叫")
    
    def move(self):
        print(f"{self.name} 展开{self.wingspan}米翅膀飞翔")
    
    def build_nest(self):
        print(f"{self.name} 在筑巢")


class AnimalShelter:
    """动物收容所 - 多态应用"""
    
    def __init__(self, name):
        self.name = name
        self.animals = []
    
    def add_animal(self, animal):
        """收容动物"""
        if isinstance(animal, Animal):
            self.animals.append(animal)
            print(f"✅ {animal.name} 已被收容到 {self.name}")
        else:
            print("❌ 只能收容动物")
    
    def daily_routine(self):
        """日常活动 - 多态演示"""
        print(f"\n🌅 {self.name} 开始日常活动")
        print("=" * 40)
        
        for animal in self.animals:
            animal.introduce()  # 多态：每种动物有不同的介绍方式
    
    def feeding_time(self):
        """喂食时间"""
        print(f"\n🍽️  {self.name} 喂食时间")
        print("=" * 40)
        
        for animal in self.animals:
            print(f"正在喂食 {animal.name}")
            animal.make_sound()  # 多态：不同动物有不同的叫声
        print()


def demonstrate_shape_polymorphism():
    """演示形状多态"""
    print("=== 形状多态演示 ===")
    
    # 创建不同形状
    shapes = [
        Rectangle(5, 3),
        Circle(4),
        Triangle(3, 4, 5),
        Polygon([6, 6, 6, 6, 6, 6])  # 正六边形
    ]
    
    # 创建计算器
    calculator = ShapeCalculator()
    
    # 添加形状
    for shape in shapes:
        calculator.add_shape(shape)
    
    # 多态应用
    calculator.display_all_shapes()
    calculator.calculate_total_area()
    calculator.calculate_total_perimeter()
    calculator.find_largest_shape()
    print()


def demonstrate_animal_polymorphism():
    """演示动物多态"""
    print("=== 动物多态演示 ===")
    
    # 创建不同动物
    animals = [
        Dog("旺财", "金毛"),
        Cat("咪咪", "橘色"),
        Bird("小鸟", 0.5),
        Dog("小黑", "拉布拉多"),
        Cat("雪球", "白色")
    ]
    
    # 创建收容所
    shelter = AnimalShelter("爱心动物收容所")
    
    # 收容动物
    for animal in animals:
        shelter.add_animal(animal)
    
    # 多态演示
    shelter.daily_routine()
    shelter.feeding_time()


def demonstrate_polymorphic_functions():
    """演示多态函数"""
    print("=== 多态函数演示 ===")
    
    def process_shape(shape):
        """处理形状 - 多态函数"""
        print(f"处理 {shape.name}:")
        print(f"  面积: {shape.area():.2f}")
        print(f"  周长: {shape.perimeter():.2f}")
        
        # 根据具体类型执行特殊操作
        if isinstance(shape, Rectangle):
            if shape.is_square():
                print(f"  这是一个正方形！")
        elif isinstance(shape, Circle):
            print(f"  直径: {shape.diameter():.2f}")
        elif isinstance(shape, Triangle):
            print(f"  类型: {shape.triangle_type()}")
        
        print()
    
    def animal_concert(animals):
        """动物音乐会 - 多态函数"""
        print("🎵 动物音乐会开始！")
        print("-" * 30)
        
        for i, animal in enumerate(animals, 1):
            print(f"{i}. ", end="")
            animal.make_sound()  # 多态调用
        
        print("-" * 30)
        print("🎵 音乐会结束！\n")
    
    # 测试形状处理
    shapes = [
        Rectangle(4, 4),  # 正方形
        Circle(3),
        Triangle(3, 4, 5)
    ]
    
    print("形状处理:")
    for shape in shapes:
        process_shape(shape)  # 多态调用
    
    # 测试动物音乐会
    animals = [
        Dog("阿黄", "土狗"),
        Cat("小花", "花色"),
        Bird("小翠", 0.3)
    ]
    
    animal_concert(animals)  # 多态调用


def demonstrate_duck_typing():
    """演示鸭子类型"""
    print("=== 鸭子类型演示 ===")
    
    class Duck:
        def quack(self):
            print("鸭子嘎嘎叫")
        
        def swim(self):
            print("鸭子在游泳")
    
    class Robot:
        def quack(self):
            print("机器人模拟鸭子叫声")
        
        def swim(self):
            print("机器人在水中移动")
    
    class Person:
        def quack(self):
            print("人模仿鸭子叫")
        
        def swim(self):
            print("人在游泳")
    
    def make_it_quack_and_swim(duck_like):
        """鸭子类型函数 - 不检查类型，只要有相应方法即可"""
        duck_like.quack()
        duck_like.swim()
        print()
    
    # 测试鸭子类型
    duck_likes = [Duck(), Robot(), Person()]
    
    print("鸭子类型测试（如果它走起来像鸭子，叫起来像鸭子，那它就是鸭子）:")
    for obj in duck_likes:
        print(f"测试 {obj.__class__.__name__}:")
        make_it_quack_and_swim(obj)  # 鸭子类型多态


def main():
    """主函数"""
    print("Session09 示例2: 多态")
    print("=" * 50)
    
    demonstrate_shape_polymorphism()
    demonstrate_animal_polymorphism()
    demonstrate_polymorphic_functions()
    demonstrate_duck_typing()
    
    print("\n💡 多态要点总结:")
    print("   • 多态允许同一接口有不同实现")
    print("   • 运行时确定具体调用哪个方法")
    print("   • 提高代码的灵活性和可扩展性")
    print("   • 抽象类定义统一接口")
    print("   • 鸭子类型：关注行为而非类型")
    print("   • isinstance()用于类型检查")


if __name__ == "__main__":
    main()