# Session 06: 函数编程

## 📚 学习目标

通过本节课的学习，你将掌握：

- **函数定义与调用**：掌握函数的基本语法和调用方式
- **参数传递**：理解位置参数、关键字参数、默认参数和可变参数
- **返回值**：学会使用return语句返回单个或多个值
- **作用域**：理解局部变量、全局变量和作用域规则
- **高级特性**：掌握lambda函数、装饰器基础和函数式编程思想
- **实际应用**：通过文本处理工具集项目巩固所学知识

## 🎯 核心概念

### 1. 函数定义与调用

函数是组织代码的基本单位，可以重复使用和模块化开发：

```python
# 定义函数
def greet(name):
    """问候函数"""
    return f"Hello, {name}!"

# 调用函数
message = greet("Alice")
print(message)  # Hello, Alice!
```

### 2. 参数类型

函数支持多种参数类型，提供灵活的调用方式：

```python
# 位置参数和关键字参数
def calculate_bmi(weight, height, unit="metric"):
    if unit == "metric":
        return weight / (height ** 2)
    else:
        return (weight / (height ** 2)) * 703

# 不同调用方式
bmi1 = calculate_bmi(70, 1.75)              # 位置参数
bmi2 = calculate_bmi(weight=70, height=1.75) # 关键字参数
bmi3 = calculate_bmi(154, 5.9, "imperial")   # 混合参数
```

### 3. 可变参数

处理不确定数量的参数：

```python
# *args 和 **kwargs
def flexible_function(*args, **kwargs):
    print(f"位置参数: {args}")
    print(f"关键字参数: {kwargs}")

flexible_function(1, 2, 3, name="Alice", age=25)
# 位置参数: (1, 2, 3)
# 关键字参数: {'name': 'Alice', 'age': 25}
```

### 4. 作用域

理解变量的可见性和生命周期：

```python
global_var = "我是全局变量"

def demo_scope():
    local_var = "我是局部变量"
    global global_var
    global_var = "修改后的全局变量"
    print(f"局部: {local_var}")
    print(f"全局: {global_var}")
```

## 🛠️ 函数设计原则

### 1. 单一职责原则
每个函数只做一件事，功能明确：

```python
# 好的设计
def calculate_area(radius):
    """计算圆的面积"""
    return 3.14159 * radius ** 2

def format_area(area):
    """格式化面积输出"""
    return f"面积: {area:.2f} 平方单位"
```

### 2. 函数命名规范
- 使用动词开头，描述函数的行为
- 使用小写字母和下划线
- 名称要有意义和描述性

```python
# 好的命名
def calculate_total_price(items, tax_rate):
    pass

def validate_email_format(email):
    pass

def convert_temperature(temp, from_unit, to_unit):
    pass
```

## 🎮 演示项目

**文本处理工具集**
- 实现文本统计、格式化、搜索替换等功能
- 使用函数模块化设计
- 提供命令行界面和交互式操作
- 支持文件批处理和结果导出

## 📋 前置知识

- Session 01: 环境搭建与Hello World
- Session 02: 变量与数据类型
- Session 03: 运算符与表达式
- Session 04: 控制流程
- Session 05: 数据结构基础

## ⏰ 学习时间

预计学习时间：**4-5小时**
- 理论学习：1.5小时
- 代码实践：2小时
- 项目开发：1.5-2小时

## 📁 文件说明

- `tutorial.md` - 详细教程文档
- `demo.py` - 主要演示代码
- `examples/` - 分类示例代码
  - `example1.py` - 函数基础示例
  - `example2.py` - 参数和返回值示例
  - `example3.py` - 作用域和高级特性示例
- `exercises/` - 练习题目录
  - `exercise1.py` - 函数基础练习
  - `exercise2.py` - 参数传递练习
  - `exercise3.py` - 综合函数设计练习
  - `solutions/` - 练习答案
- `project/` - 文本处理工具集
  - `main.py` - 项目主文件
  - `text_processor.py` - 文本处理核心模块
  - `file_handler.py` - 文件操作模块
  - `cli_interface.py` - 命令行界面模块
- `assets/` - 资源文件
  - `sample_texts.py` - 示例文本数据
  - `constants.py` - 常量定义

## 🚀 快速开始

```bash
# 进入session06目录
cd session06

# 运行演示代码
uv run python demo.py

# 运行示例代码
uv run python examples/example1.py

# 运行项目
uv run python project/main.py
```

## 💡 学习建议

1. **理解概念**：重点理解函数的本质和作用域概念
2. **多练习**：通过大量练习熟悉不同类型的参数传递
3. **设计思维**：学会将复杂问题分解为简单函数
4. **代码复用**：体会函数带来的代码复用和模块化优势
5. **最佳实践**：遵循函数设计的最佳实践和命名规范

## 🔗 相关资源

- [Python官方文档 - 函数定义](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
- [Python函数参数详解](https://docs.python.org/3/tutorial/controlflow.html#more-on-defining-functions)
- [Python作用域和命名空间](https://docs.python.org/3/tutorial/classes.html#python-scopes-and-namespaces)

---

**准备好掌握函数编程的精髓了吗？让我们开始构建强大的代码模块！** 🚀