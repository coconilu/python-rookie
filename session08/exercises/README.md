# Session08 练习题说明

本目录包含Session08面向对象编程基础的练习题，旨在帮助你巩固和应用所学的知识。

## 练习题列表

### 练习题1：图书类设计
**文件：** `exercise1.py`  
**难度：** ⭐⭐  
**知识点：** 基本类定义、构造函数、实例方法、属性验证

**主要内容：**
- 设计Book类管理图书信息
- 实现购买、补充库存等功能
- 练习参数验证和错误处理
- 使用__str__方法格式化输出

**学习目标：**
- 掌握类的基本定义和使用
- 理解构造函数的作用
- 学会在方法中进行参数验证
- 练习实例方法的编写

### 练习题2：学生成绩管理系统
**文件：** `exercise2.py`  
**难度：** ⭐⭐⭐  
**知识点：** 类变量、实例变量、类方法、静态方法、数据统计

**主要内容：**
- 设计Student类管理学生成绩
- 使用字典存储科目成绩
- 实现成绩统计功能
- 练习类变量和类方法的使用

**学习目标：**
- 区分类变量和实例变量
- 掌握类方法和静态方法的使用
- 练习数据结构的应用（字典）
- 学会进行数据统计和分析

### 练习题3：购物车系统
**文件：** `exercise3.py`  
**难度：** ⭐⭐⭐⭐  
**知识点：** 类的组合、特殊方法、复杂业务逻辑

**主要内容：**
- 设计多个相关联的类
- 实现购物车的完整功能
- 练习类之间的组合关系
- 使用特殊方法增强类的功能

**学习目标：**
- 理解类的组合关系
- 掌握特殊方法的实现
- 练习复杂业务逻辑的设计
- 学会多类协作的编程模式

## 完成指南

### 建议完成顺序
1. **exercise1.py** - 从基础开始，掌握类的基本概念
2. **exercise2.py** - 进阶练习，学习类变量和方法类型
3. **exercise3.py** - 综合应用，挑战复杂的系统设计

### 编程提示

#### 通用提示
- 先设计类的结构，再实现具体方法
- 注意参数验证和异常处理
- 使用有意义的变量名和方法名
- 添加适当的注释和文档字符串

#### 调试技巧
- 使用`print()`语句查看对象状态
- 逐步测试每个方法的功能
- 先实现基本功能，再添加高级特性
- 使用`type()`和`isinstance()`检查对象类型

#### 代码规范
- 遵循PEP 8编码规范
- 类名使用大驼峰命名（PascalCase）
- 方法名和变量名使用小写加下划线（snake_case）
- 每个方法都要有文档字符串

## 测试方法

### 运行单个练习
```bash
# 进入exercises目录
cd session08/exercises

# 运行练习题1
uv run python exercise1.py

# 运行练习题2
uv run python exercise2.py

# 运行练习题3
uv run python exercise3.py
```

### 测试建议
- 为每个类编写测试函数
- 测试正常情况和异常情况
- 验证边界条件（如空值、负数等）
- 检查方法的返回值是否正确

## 扩展挑战

完成基本练习后，可以尝试以下扩展：

### 练习题1扩展
- 添加图书分类功能
- 实现图书搜索功能
- 添加图书评分系统
- 实现图书借阅功能

### 练习题2扩展
- 添加成绩排名功能
- 实现班级成绩统计
- 添加成绩趋势分析
- 实现成绩导入导出

### 练习题3扩展
- 添加优惠券系统
- 实现会员折扣功能
- 添加商品推荐功能
- 实现订单历史记录

## 常见错误

### 1. 忘记使用self
```python
# 错误
class MyClass:
    def __init__(self, value):
        value = value  # 应该是 self.value = value

# 正确
class MyClass:
    def __init__(self, value):
        self.value = value
```

### 2. 类变量和实例变量混淆
```python
# 错误
class Counter:
    count = 0
    def __init__(self):
        count += 1  # 应该是 Counter.count += 1

# 正确
class Counter:
    count = 0
    def __init__(self):
        Counter.count += 1
```

### 3. 方法调用错误
```python
# 错误
class MyClass:
    def method1(self):
        return "Hello"
    
    def method2(self):
        return method1()  # 应该是 self.method1()

# 正确
class MyClass:
    def method1(self):
        return "Hello"
    
    def method2(self):
        return self.method1()
```

## 参考答案

完成练习后，可以查看`solutions/`目录下的参考答案：
- `exercise1_solution.py` - 练习题1参考答案
- `exercise2_solution.py` - 练习题2参考答案
- `exercise3_solution.py` - 练习题3参考答案

**注意：** 建议先独立完成练习，再查看参考答案进行对比和学习。

## 学习资源

- [Python官方文档 - 类](https://docs.python.org/3/tutorial/classes.html)
- [Real Python - OOP in Python](https://realpython.com/python3-object-oriented-programming/)
- Session08教程文档：`../tutorial.md`
- Session08演示代码：`../demo.py`

---

**记住：** 面向对象编程是一种思维方式，多练习、多思考，你会逐渐掌握这种强大的编程范式！🚀