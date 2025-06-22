# Session09: 面向对象进阶教程

## 目录
1. [继承基础](#1-继承基础)
2. [方法重写](#2-方法重写)
3. [super()函数](#3-super函数)
4. [多重继承](#4-多重继承)
5. [多态](#5-多态)
6. [封装和访问控制](#6-封装和访问控制)
7. [抽象类](#7-抽象类)
8. [组合vs继承](#8-组合vs继承)
9. [实战应用](#9-实战应用)

---

## 1. 继承基础

### 什么是继承？

继承是面向对象编程的核心特性之一，它允许一个类（子类）继承另一个类（父类）的属性和方法。

### 基本语法

```python
class 父类:
    def __init__(self):
        self.属性 = 值
    
    def 方法(self):
        pass

class 子类(父类):
    def __init__(self):
        super().__init__()  # 调用父类构造函数
        self.子类属性 = 值
```

### 示例：动物类继承

```python
class Animal:
    """动物基类"""
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.energy = 100
    
    def eat(self):
        self.energy += 20
        print(f"{self.name} 正在吃东西，能量增加到 {self.energy}")
    
    def sleep(self):
        self.energy += 30
        print(f"{self.name} 正在睡觉，能量恢复到 {self.energy}")
    
    def make_sound(self):
        print(f"{self.name} 发出了声音")

class Dog(Animal):
    """狗类，继承自动物类"""
    def __init__(self, name, age, breed):
        super().__init__(name, age)  # 调用父类构造函数
        self.breed = breed  # 狗的品种
    
    def make_sound(self):
        print(f"{self.name} 汪汪叫")
    
    def fetch(self):
        print(f"{self.name} 正在捡球")

class Cat(Animal):
    """猫类，继承自动物类"""
    def __init__(self, name, age, color):
        super().__init__(name, age)
        self.color = color
    
    def make_sound(self):
        print(f"{self.name} 喵喵叫")
    
    def climb(self):
        print(f"{self.name} 正在爬树")

# 使用示例
dog = Dog("旺财", 3, "金毛")
cat = Cat("咪咪", 2, "橘色")

dog.eat()  # 继承自Animal的方法
dog.make_sound()  # 重写的方法
dog.fetch()  # Dog特有的方法

cat.sleep()  # 继承自Animal的方法
cat.make_sound()  # 重写的方法
cat.climb()  # Cat特有的方法
```

**运行结果：**
```
旺财 正在吃东西，能量增加到 120
旺财 汪汪叫
旺财 正在捡球
咪咪 正在睡觉，能量恢复到 130
咪咪 喵喵叫
咪咪 正在爬树
```

---

## 2. 方法重写

### 什么是方法重写？

方法重写（Override）是指子类重新定义父类中已有的方法，以实现不同的行为。

### 重写规则

1. 方法名必须相同
2. 参数列表必须相同
3. 子类方法会覆盖父类方法

### 示例：不同动物的叫声

```python
class Bird(Animal):
    """鸟类"""
    def __init__(self, name, age, can_fly=True):
        super().__init__(name, age)
        self.can_fly = can_fly
    
    def make_sound(self):
        print(f"{self.name} 啾啾叫")
    
    def fly(self):
        if self.can_fly:
            print(f"{self.name} 正在飞翔")
        else:
            print(f"{self.name} 不会飞")

class Penguin(Bird):
    """企鹅类"""
    def __init__(self, name, age):
        super().__init__(name, age, can_fly=False)
    
    def make_sound(self):
        print(f"{self.name} 嘎嘎叫")
    
    def swim(self):
        print(f"{self.name} 正在游泳")

# 测试方法重写
bird = Bird("小鸟", 1)
penguin = Penguin("企鹅", 5)

bird.make_sound()  # 啾啾叫
bird.fly()  # 正在飞翔

penguin.make_sound()  # 嘎嘎叫（重写了Bird的方法）
penguin.fly()  # 不会飞
penguin.swim()  # 正在游泳
```

---

## 3. super()函数

### super()的作用

`super()`函数用于调用父类的方法，特别是在方法重写时保留父类的功能。

### 使用场景

1. 调用父类的构造函数
2. 在重写方法中调用父类方法
3. 多重继承中的方法调用

### 示例：扩展父类方法

```python
class Vehicle:
    """交通工具基类"""
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
        self.speed = 0
    
    def start(self):
        print(f"{self.brand} {self.model} 启动了")
    
    def accelerate(self, increment):
        self.speed += increment
        print(f"加速到 {self.speed} km/h")

class Car(Vehicle):
    """汽车类"""
    def __init__(self, brand, model, fuel_type):
        super().__init__(brand, model)  # 调用父类构造函数
        self.fuel_type = fuel_type
        self.fuel_level = 100
    
    def start(self):
        if self.fuel_level > 0:
            super().start()  # 调用父类的start方法
            print(f"燃料类型：{self.fuel_type}")
        else:
            print("燃料不足，无法启动")
    
    def accelerate(self, increment):
        if self.fuel_level > 0:
            super().accelerate(increment)  # 调用父类方法
            self.fuel_level -= increment * 0.1  # 消耗燃料
            print(f"剩余燃料：{self.fuel_level:.1f}%")
        else:
            print("燃料不足，无法加速")

# 使用示例
car = Car("丰田", "卡罗拉", "汽油")
car.start()
car.accelerate(50)
car.accelerate(30)
```

**运行结果：**
```
丰田 卡罗拉 启动了
燃料类型：汽油
加速到 50 km/h
剩余燃料：95.0%
加速到 80 km/h
剩余燃料：92.0%
```

---

## 4. 多重继承

### 什么是多重继承？

多重继承允许一个类同时继承多个父类的特性。

### 方法解析顺序（MRO）

Python使用C3线性化算法确定方法解析顺序，可以通过`类名.__mro__`查看。

### 示例：多重继承

```python
class Flyable:
    """可飞行的接口"""
    def fly(self):
        print("正在飞行")

class Swimmable:
    """可游泳的接口"""
    def swim(self):
        print("正在游泳")

class Duck(Animal, Flyable, Swimmable):
    """鸭子类，继承多个类"""
    def __init__(self, name, age):
        super().__init__(name, age)
    
    def make_sound(self):
        print(f"{self.name} 嘎嘎叫")

# 使用示例
duck = Duck("唐老鸭", 3)
duck.make_sound()  # 来自Animal（重写）
duck.eat()  # 来自Animal
duck.fly()  # 来自Flyable
duck.swim()  # 来自Swimmable

# 查看方法解析顺序
print("MRO:", Duck.__mro__)
```

### 菱形继承问题

```python
class A:
    def method(self):
        print("A的方法")

class B(A):
    def method(self):
        print("B的方法")
        super().method()

class C(A):
    def method(self):
        print("C的方法")
        super().method()

class D(B, C):
    def method(self):
        print("D的方法")
        super().method()

# 测试MRO
d = D()
d.method()
print("MRO:", D.__mro__)
```

---

## 5. 多态

### 什么是多态？

多态是指同一个接口可以有不同的实现方式，在运行时根据对象的实际类型调用相应的方法。

### 多态的实现

```python
def animal_concert(animals):
    """动物音乐会 - 展示多态"""
    print("=== 动物音乐会开始 ===")
    for animal in animals:
        animal.make_sound()  # 多态：不同动物有不同的叫声
        if hasattr(animal, 'perform'):
            animal.perform()
    print("=== 音乐会结束 ===")

class PerformingDog(Dog):
    """表演犬"""
    def perform(self):
        print(f"{self.name} 表演跳圈")

class PerformingCat(Cat):
    """表演猫"""
    def perform(self):
        print(f"{self.name} 表演走钢丝")

class Parrot(Bird):
    """鹦鹉"""
    def make_sound(self):
        print(f"{self.name} 学人说话：你好！")
    
    def perform(self):
        print(f"{self.name} 表演说话")

# 创建不同类型的动物
animals = [
    PerformingDog("阿黄", 4, "边牧"),
    PerformingCat("小白", 3, "白色"),
    Parrot("波利", 2),
    Duck("小鸭", 1)
]

# 多态演示
animal_concert(animals)
```

**运行结果：**
```
=== 动物音乐会开始 ===
阿黄 汪汪叫
阿黄 表演跳圈
小白 喵喵叫
小白 表演走钢丝
波利 学人说话：你好！
波利 表演说话
小鸭 嘎嘎叫
=== 音乐会结束 ===
```

---

## 6. 封装和访问控制

### 封装的概念

封装是将数据和操作数据的方法绑定在一起，并隐藏内部实现细节。

### Python中的访问控制

```python
class BankAccount:
    """银行账户类 - 演示封装"""
    def __init__(self, account_number, initial_balance=0):
        self.account_number = account_number  # 公开属性
        self._balance = initial_balance  # 受保护属性（约定）
        self.__pin = "1234"  # 私有属性（名称改写）
        self.__transaction_history = []  # 私有属性
    
    def deposit(self, amount):
        """存款"""
        if amount > 0:
            self._balance += amount
            self.__add_transaction(f"存款 {amount}")
            return True
        return False
    
    def withdraw(self, amount, pin):
        """取款"""
        if not self.__verify_pin(pin):
            print("PIN码错误")
            return False
        
        if amount > 0 and amount <= self._balance:
            self._balance -= amount
            self.__add_transaction(f"取款 {amount}")
            return True
        else:
            print("余额不足或金额无效")
            return False
    
    def get_balance(self, pin):
        """查询余额"""
        if self.__verify_pin(pin):
            return self._balance
        else:
            print("PIN码错误")
            return None
    
    def __verify_pin(self, pin):
        """私有方法：验证PIN码"""
        return pin == self.__pin
    
    def __add_transaction(self, transaction):
        """私有方法：添加交易记录"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__transaction_history.append(f"{timestamp}: {transaction}")
    
    def get_transaction_history(self, pin):
        """获取交易历史"""
        if self.__verify_pin(pin):
            return self.__transaction_history.copy()
        else:
            print("PIN码错误")
            return []
    
    @property
    def account_info(self):
        """属性装饰器：只读属性"""
        return f"账户号码：{self.account_number}"

# 使用示例
account = BankAccount("123456789", 1000)

# 正常操作
print(account.account_info)
account.deposit(500)
print(f"余额：{account.get_balance('1234')}")
account.withdraw(200, "1234")
print(f"余额：{account.get_balance('1234')}")

# 尝试错误操作
account.withdraw(100, "0000")  # 错误PIN
print(account.get_balance("0000"))  # 错误PIN

# 查看交易历史
history = account.get_transaction_history("1234")
for record in history:
    print(record)
```

### 属性装饰器

```python
class Temperature:
    """温度类 - 演示属性装饰器"""
    def __init__(self, celsius=0):
        self._celsius = celsius
    
    @property
    def celsius(self):
        """摄氏度getter"""
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        """摄氏度setter"""
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        """华氏度（只读）"""
        return self._celsius * 9/5 + 32
    
    @property
    def kelvin(self):
        """开尔文（只读）"""
        return self._celsius + 273.15

# 使用示例
temp = Temperature(25)
print(f"摄氏度：{temp.celsius}°C")
print(f"华氏度：{temp.fahrenheit}°F")
print(f"开尔文：{temp.kelvin}K")

temp.celsius = 30  # 使用setter
print(f"新温度：{temp.celsius}°C")
```

---

## 7. 抽象类

### 什么是抽象类？

抽象类是不能被实例化的类，通常包含一个或多个抽象方法，用于定义子类必须实现的接口。

### 使用abc模块

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    """抽象形状类"""
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def area(self):
        """抽象方法：计算面积"""
        pass
    
    @abstractmethod
    def perimeter(self):
        """抽象方法：计算周长"""
        pass
    
    def display_info(self):
        """具体方法：显示信息"""
        print(f"形状：{self.name}")
        print(f"面积：{self.area():.2f}")
        print(f"周长：{self.perimeter():.2f}")

class Rectangle(Shape):
    """矩形类"""
    def __init__(self, width, height):
        super().__init__("矩形")
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

class Circle(Shape):
    """圆形类"""
    def __init__(self, radius):
        super().__init__("圆形")
        self.radius = radius
    
    def area(self):
        import math
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        import math
        return 2 * math.pi * self.radius

# 使用示例
shapes = [
    Rectangle(5, 3),
    Circle(4)
]

for shape in shapes:
    shape.display_info()
    print("-" * 20)

# 尝试实例化抽象类会报错
# shape = Shape("测试")  # TypeError
```

---

## 8. 组合vs继承

### 何时使用继承？

- "is-a"关系：狗是动物
- 需要多态行为
- 子类是父类的特殊化

### 何时使用组合？

- "has-a"关系：汽车有引擎
- 需要更灵活的设计
- 避免深层继承

### 组合示例

```python
class Engine:
    """引擎类"""
    def __init__(self, power, fuel_type):
        self.power = power  # 功率
        self.fuel_type = fuel_type
        self.is_running = False
    
    def start(self):
        self.is_running = True
        print(f"{self.power}马力{self.fuel_type}引擎启动")
    
    def stop(self):
        self.is_running = False
        print("引擎停止")

class GPS:
    """GPS导航系统"""
    def __init__(self):
        self.current_location = "未知"
    
    def navigate_to(self, destination):
        print(f"导航到：{destination}")
        self.current_location = destination

class Car:
    """汽车类 - 使用组合"""
    def __init__(self, brand, model, engine, has_gps=False):
        self.brand = brand
        self.model = model
        self.engine = engine  # 组合：汽车有引擎
        self.gps = GPS() if has_gps else None  # 可选组合
        self.speed = 0
    
    def start(self):
        print(f"{self.brand} {self.model} 准备启动")
        self.engine.start()
    
    def stop(self):
        self.engine.stop()
        self.speed = 0
        print(f"{self.brand} {self.model} 已停车")
    
    def accelerate(self, increment):
        if self.engine.is_running:
            self.speed += increment
            print(f"加速到 {self.speed} km/h")
        else:
            print("请先启动引擎")
    
    def navigate_to(self, destination):
        if self.gps:
            self.gps.navigate_to(destination)
        else:
            print("此车没有GPS导航系统")

# 使用示例
engine = Engine(200, "汽油")
car = Car("本田", "雅阁", engine, has_gps=True)

car.start()
car.accelerate(60)
car.navigate_to("北京")
car.stop()
```

---

## 9. 实战应用

### 设计模式：策略模式

```python
from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    """支付策略抽象类"""
    @abstractmethod
    def pay(self, amount):
        pass

class CreditCardPayment(PaymentStrategy):
    """信用卡支付"""
    def __init__(self, card_number):
        self.card_number = card_number
    
    def pay(self, amount):
        print(f"使用信用卡 {self.card_number[-4:]} 支付 ¥{amount}")

class AlipayPayment(PaymentStrategy):
    """支付宝支付"""
    def __init__(self, account):
        self.account = account
    
    def pay(self, amount):
        print(f"使用支付宝账户 {self.account} 支付 ¥{amount}")

class WechatPayment(PaymentStrategy):
    """微信支付"""
    def __init__(self, phone):
        self.phone = phone
    
    def pay(self, amount):
        print(f"使用微信 {self.phone} 支付 ¥{amount}")

class ShoppingCart:
    """购物车"""
    def __init__(self):
        self.items = []
        self.payment_strategy = None
    
    def add_item(self, item, price):
        self.items.append((item, price))
        print(f"添加商品：{item} - ¥{price}")
    
    def set_payment_strategy(self, strategy):
        self.payment_strategy = strategy
    
    def checkout(self):
        if not self.items:
            print("购物车为空")
            return
        
        total = sum(price for _, price in self.items)
        print(f"\n购物清单：")
        for item, price in self.items:
            print(f"  {item}: ¥{price}")
        print(f"总计：¥{total}")
        
        if self.payment_strategy:
            self.payment_strategy.pay(total)
        else:
            print("请选择支付方式")

# 使用示例
cart = ShoppingCart()
cart.add_item("Python编程书", 89)
cart.add_item("机械键盘", 299)

# 使用不同支付策略
cart.set_payment_strategy(CreditCardPayment("1234567890123456"))
cart.checkout()

print("\n" + "="*30 + "\n")

cart.set_payment_strategy(AlipayPayment("user@example.com"))
cart.checkout()
```

## 总结

本课程学习了面向对象编程的高级特性：

1. **继承**：代码复用和层次结构
2. **多态**：同一接口的不同实现
3. **封装**：数据隐藏和访问控制
4. **抽象类**：定义接口规范
5. **组合vs继承**：选择合适的设计方式

这些特性是构建复杂软件系统的基础，掌握它们将大大提高你的编程能力。

## 练习建议

1. 设计一个图形绘制系统，使用继承和多态
2. 实现一个简单的游戏角色系统
3. 创建一个文件管理系统，使用组合模式
4. 设计一个通知系统，使用观察者模式

## 下节预告

下一课我们将学习模块与包的使用，了解如何组织和管理大型Python项目。