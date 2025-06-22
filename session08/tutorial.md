# Session08: 面向对象编程基础教程

## 1. 面向对象编程概述

### 1.1 什么是面向对象编程？

面向对象编程（Object-Oriented Programming，OOP）是一种编程范式，它使用"对象"来设计应用程序和计算机程序。面向对象编程的核心思想是将现实世界中的事物抽象为程序中的对象。

**面向对象编程的优势：**
- **代码重用性**：通过继承和组合实现代码复用
- **模块化**：将复杂问题分解为简单的对象
- **可维护性**：代码结构清晰，易于维护和修改
- **可扩展性**：容易添加新功能而不影响现有代码

### 1.2 面向对象的基本概念

**类（Class）**：对象的蓝图或模板，定义了对象的属性和方法。

**对象（Object）**：类的实例，是具体存在的实体。

**属性（Attribute）**：对象的特征或状态。

**方法（Method）**：对象能够执行的操作。

### 1.3 现实世界的类比

想象一下汽车：
- **类**：汽车的设计图纸（定义了汽车应该有什么属性和功能）
- **对象**：具体的汽车实例（比如你家的那辆车）
- **属性**：颜色、品牌、型号、油量等
- **方法**：启动、加速、刹车、转向等

## 2. 类的定义和使用

### 2.1 定义一个简单的类

```python
class Car:
    """汽车类的定义"""
    pass  # 暂时为空
```

### 2.2 创建对象（实例化）

```python
# 创建Car类的实例
my_car = Car()
print(type(my_car))  # <class '__main__.Car'>
print(my_car)        # <__main__.Car object at 0x...>
```

### 2.3 添加属性

```python
class Car:
    """汽车类"""
    
    def __init__(self, brand, model, color):
        """构造函数，初始化汽车属性"""
        self.brand = brand    # 品牌
        self.model = model    # 型号
        self.color = color    # 颜色
        self.fuel = 0         # 油量，默认为0
        self.is_running = False  # 是否启动，默认未启动

# 创建汽车对象
my_car = Car("Toyota", "Camry", "红色")
print(f"我的车是{my_car.color}的{my_car.brand} {my_car.model}")
# 输出：我的车是红色的Toyota Camry
```

## 3. 构造函数__init__

### 3.1 构造函数的作用

`__init__`方法是Python中的构造函数，在创建对象时自动调用，用于初始化对象的属性。

```python
class Student:
    def __init__(self, name, age, grade):
        """学生类的构造函数"""
        self.name = name      # 姓名
        self.age = age        # 年龄
        self.grade = grade    # 年级
        self.scores = []      # 成绩列表，初始为空

# 创建学生对象
student1 = Student("张三", 18, "高三")
student2 = Student("李四", 17, "高二")

print(f"{student1.name}今年{student1.age}岁，在读{student1.grade}")
# 输出：张三今年18岁，在读高三
```

### 3.2 self关键字

`self`代表类的实例，通过`self`可以访问实例的属性和方法。

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius  # self.radius是实例属性
    
    def get_area(self):
        """计算圆的面积"""
        return 3.14159 * self.radius * self.radius
    
    def get_circumference(self):
        """计算圆的周长"""
        return 2 * 3.14159 * self.radius

# 创建圆对象
circle1 = Circle(5)
print(f"半径为{circle1.radius}的圆")
print(f"面积：{circle1.get_area():.2f}")
print(f"周长：{circle1.get_circumference():.2f}")
```

## 4. 实例方法

### 4.1 定义实例方法

实例方法是定义在类中的函数，第一个参数必须是`self`。

```python
class BankAccount:
    """银行账户类"""
    
    def __init__(self, account_number, owner_name, initial_balance=0):
        """初始化账户"""
        self.account_number = account_number
        self.owner_name = owner_name
        self.balance = initial_balance
    
    def deposit(self, amount):
        """存款方法"""
        if amount > 0:
            self.balance += amount
            print(f"存款{amount}元成功，当前余额：{self.balance}元")
        else:
            print("存款金额必须大于0")
    
    def withdraw(self, amount):
        """取款方法"""
        if amount > 0:
            if amount <= self.balance:
                self.balance -= amount
                print(f"取款{amount}元成功，当前余额：{self.balance}元")
            else:
                print("余额不足")
        else:
            print("取款金额必须大于0")
    
    def get_balance(self):
        """查询余额"""
        return self.balance
    
    def get_account_info(self):
        """获取账户信息"""
        return f"账户号：{self.account_number}，户主：{self.owner_name}，余额：{self.balance}元"

# 使用银行账户类
account = BankAccount("123456789", "张三", 1000)
print(account.get_account_info())

account.deposit(500)    # 存款500元
account.withdraw(200)   # 取款200元
print(f"当前余额：{account.get_balance()}元")
```

**运行结果：**
```
账户号：123456789，户主：张三，余额：1000元
存款500元成功，当前余额：1500元
取款200元成功，当前余额：1300元
当前余额：1300元
```

## 5. 实例变量vs类变量

### 5.1 实例变量

实例变量是属于特定对象实例的变量，每个对象都有自己的副本。

```python
class Dog:
    def __init__(self, name, breed):
        self.name = name      # 实例变量
        self.breed = breed    # 实例变量

dog1 = Dog("旺财", "金毛")
dog2 = Dog("小黑", "拉布拉多")

print(dog1.name)  # 旺财
print(dog2.name)  # 小黑
```

### 5.2 类变量

类变量是属于整个类的变量，所有实例共享同一个副本。

```python
class Dog:
    species = "犬科动物"  # 类变量
    
    def __init__(self, name, breed):
        self.name = name      # 实例变量
        self.breed = breed    # 实例变量

dog1 = Dog("旺财", "金毛")
dog2 = Dog("小黑", "拉布拉多")

print(dog1.species)  # 犬科动物
print(dog2.species)  # 犬科动物
print(Dog.species)   # 犬科动物

# 修改类变量
Dog.species = "家犬"
print(dog1.species)  # 家犬
print(dog2.species)  # 家犬
```

### 5.3 实际应用示例

```python
class Employee:
    """员工类"""
    company_name = "ABC科技公司"  # 类变量
    employee_count = 0           # 类变量，记录员工总数
    
    def __init__(self, name, position, salary):
        self.name = name          # 实例变量
        self.position = position  # 实例变量
        self.salary = salary      # 实例变量
        Employee.employee_count += 1  # 每创建一个员工，总数+1
    
    def get_info(self):
        """获取员工信息"""
        return f"姓名：{self.name}，职位：{self.position}，薪资：{self.salary}"
    
    @classmethod
    def get_company_info(cls):
        """获取公司信息（类方法）"""
        return f"公司：{cls.company_name}，员工总数：{cls.employee_count}"

# 创建员工对象
emp1 = Employee("张三", "程序员", 8000)
emp2 = Employee("李四", "设计师", 7000)
emp3 = Employee("王五", "产品经理", 9000)

print(emp1.get_info())
print(Employee.get_company_info())
```

**运行结果：**
```
姓名：张三，职位：程序员，薪资：8000
公司：ABC科技公司，员工总数：3
```

## 6. 特殊方法（魔法方法）

### 6.1 __str__方法

`__str__`方法定义了对象的字符串表示，当使用`print()`或`str()`时会调用。

```python
class Book:
    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price
    
    def __str__(self):
        """定义对象的字符串表示"""
        return f"《{self.title}》- {self.author}，价格：{self.price}元"

book = Book("Python编程", "张三", 59.9)
print(book)  # 《Python编程》- 张三，价格：59.9元
```

### 6.2 __repr__方法

`__repr__`方法定义了对象的"官方"字符串表示，通常用于调试。

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"点({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

point = Point(3, 4)
print(str(point))   # 点(3, 4)
print(repr(point))  # Point(3, 4)
print(point)        # 点(3, 4)
```

## 7. 实际应用案例

### 7.1 学生管理系统

```python
class Student:
    """学生类"""
    school_name = "Python学院"  # 类变量
    
    def __init__(self, student_id, name, age, major):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.major = major
        self.courses = []  # 选课列表
        self.grades = {}   # 成绩字典
    
    def add_course(self, course_name):
        """添加课程"""
        if course_name not in self.courses:
            self.courses.append(course_name)
            print(f"{self.name}成功选择课程：{course_name}")
        else:
            print(f"{self.name}已经选择了课程：{course_name}")
    
    def add_grade(self, course_name, grade):
        """添加成绩"""
        if course_name in self.courses:
            self.grades[course_name] = grade
            print(f"{self.name}的{course_name}成绩已录入：{grade}分")
        else:
            print(f"{self.name}未选择课程：{course_name}")
    
    def get_average_grade(self):
        """计算平均成绩"""
        if self.grades:
            return sum(self.grades.values()) / len(self.grades)
        return 0
    
    def get_student_info(self):
        """获取学生信息"""
        info = f"学号：{self.student_id}，姓名：{self.name}，年龄：{self.age}，专业：{self.major}\n"
        info += f"选课：{', '.join(self.courses)}\n"
        info += f"成绩：{self.grades}\n"
        info += f"平均分：{self.get_average_grade():.2f}"
        return info
    
    def __str__(self):
        return f"学生：{self.name}（{self.student_id}）"

# 使用学生管理系统
student = Student("2023001", "张三", 20, "计算机科学")
student.add_course("Python编程")
student.add_course("数据结构")
student.add_course("算法设计")

student.add_grade("Python编程", 95)
student.add_grade("数据结构", 88)
student.add_grade("算法设计", 92)

print(student.get_student_info())
```

## 8. 常见错误和注意事项

### 8.1 忘记使用self

```python
# 错误示例
class Calculator:
    def __init__(self, value):
        value = value  # 错误：应该是 self.value = value
    
    def add(self, num):
        return value + num  # 错误：应该是 self.value + num

# 正确示例
class Calculator:
    def __init__(self, value):
        self.value = value  # 正确
    
    def add(self, num):
        return self.value + num  # 正确
```

### 8.2 类变量和实例变量混淆

```python
class Counter:
    count = 0  # 类变量
    
    def __init__(self):
        Counter.count += 1  # 正确：修改类变量
        self.instance_id = Counter.count  # 实例变量

# 创建多个实例
c1 = Counter()
c2 = Counter()
c3 = Counter()

print(f"总共创建了{Counter.count}个实例")  # 3
print(f"c1的ID：{c1.instance_id}")  # 1
print(f"c2的ID：{c2.instance_id}")  # 2
```

### 8.3 方法调用错误

```python
class MyClass:
    def method1(self):
        return "方法1"
    
    def method2(self):
        # 正确：调用同一个类的其他方法
        return self.method1() + "和方法2"

obj = MyClass()
print(obj.method2())  # 方法1和方法2
```

## 9. 练习建议

1. **从简单开始**：先定义只有属性的类，再逐步添加方法
2. **多练习**：尝试将现实世界的事物抽象为类
3. **理解self**：确保理解self的作用和使用方法
4. **区分变量类型**：明确什么时候使用实例变量，什么时候使用类变量
5. **调试技巧**：使用`print()`语句查看对象的状态

## 10. 总结

面向对象编程是Python的重要特性，通过本课学习，你应该掌握：

- 类和对象的基本概念
- 如何定义类和创建对象
- 构造函数`__init__`的使用
- 实例方法的定义和调用
- 实例变量和类变量的区别
- 特殊方法的使用

面向对象编程让代码更加模块化、可重用和易维护。在接下来的课程中，我们将学习面向对象的高级特性：继承、多态和封装。