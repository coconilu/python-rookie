# Session 02: 变量与数据类型

## 📚 学习目标

通过本节课的学习，你将掌握：

- **变量的概念和使用**：理解变量是什么，如何创建和使用变量
- **Python基本数据类型**：掌握字符串、整数、浮点数、布尔值等数据类型
- **类型转换**：学会在不同数据类型之间进行转换
- **字符串操作**：掌握字符串的常用方法和操作技巧
- **实际应用**：通过项目实践巩固所学知识

## 🎯 核心概念

### 1. 变量 (Variables)

变量是存储数据的容器，可以把它想象成一个有标签的盒子：

```python
# 创建变量
name = "张三"        # 字符串变量
age = 25            # 整数变量
height = 1.75       # 浮点数变量
is_student = True   # 布尔变量
```

**变量命名规则：**
- 只能包含字母、数字和下划线
- 不能以数字开头
- 区分大小写
- 不能使用Python关键字

### 2. 数据类型 (Data Types)

| 类型 | 英文名 | 描述 | 示例 |
|------|--------|------|------|
| 字符串 | str | 文本数据 | `"Hello"`, `'Python'` |
| 整数 | int | 整数 | `42`, `-10`, `0` |
| 浮点数 | float | 小数 | `3.14`, `-2.5`, `0.0` |
| 布尔值 | bool | 真/假 | `True`, `False` |

### 3. 类型转换 (Type Conversion)

```python
# 字符串转数字
age_str = "25"
age_int = int(age_str)      # 转换为整数
height_str = "1.75"
height_float = float(height_str)  # 转换为浮点数

# 数字转字符串
age = 25
age_str = str(age)          # 转换为字符串

# 布尔值转换
is_adult = bool(age >= 18)  # 转换为布尔值
```

### 4. 字符串操作 (String Operations)

```python
text = "  Hello Python  "

# 常用方法
text.strip()        # 去除首尾空格
text.upper()        # 转换为大写
text.lower()        # 转换为小写
text.replace("Hello", "Hi")  # 替换文本
text.split()        # 分割字符串

# 字符串格式化
name = "张三"
age = 25
message = f"我叫{name}，今年{age}岁"  # f-string格式化
```

## 演示项目
个人信息管理系统 - 一个能够录入、存储和显示个人基本信息的程序

## 前置知识
- 完成Session01的学习
- 掌握Python程序的基本运行方法
- 了解基本的输入输出操作

## 学习时间
预计学习时间：2-3小时

## 📁 项目结构

```
session02/
├── README.md                    # 本文件
├── examples/                    # 示例代码
│   ├── example1.py             # 变量基础操作
│   ├── example2.py             # 类型转换示例
│   └── example3.py             # 字符串操作示例
├── exercises/                   # 练习题
│   ├── README.md               # 练习说明
│   ├── exercise1.py            # 练习1：变量基础
│   ├── exercise2.py            # 练习2：类型转换
│   ├── exercise3.py            # 练习3：字符串处理
│   └── solutions/              # 参考答案
│       ├── exercise1_solution.py
│       ├── exercise2_solution.py
│       └── exercise3_solution.py
└── project/                     # 综合项目
    ├── README.md               # 项目说明
    ├── main.py                 # 主程序
    ├── user_manager.py         # 用户管理模块
    ├── utils.py                # 工具函数
    ├── constants.py            # 常量定义
    └── examples/               # 项目示例
        ├── sample_data.py      # 示例数据
        └── demo_usage.py       # 使用演示
```

## 🚀 快速开始

### 1. 运行示例代码

```bash
# 进入session02目录
cd session02

# 运行变量基础示例
uv run python examples/example1.py

# 运行类型转换示例
uv run python examples/example2.py

# 运行字符串操作示例
uv run python examples/example3.py
```

### 2. 完成练习题

```bash
# 查看练习说明
cat exercises/README.md

# 完成练习1
uv run python exercises/exercise1.py

# 完成练习2
uv run python exercises/exercise2.py

# 完成练习3
uv run python exercises/exercise3.py

# 查看参考答案
uv run python exercises/solutions/exercise1_solution.py
```

### 3. 运行综合项目

```bash
# 进入项目目录
cd project

# 运行主程序
uv run python main.py

# 查看使用演示
uv run python examples/demo_usage.py
```

## 📖 学习路径

### 第一步：理解基础概念
1. 阅读本README的核心概念部分
2. 运行 `examples/example1.py` 了解变量基础
3. 运行 `examples/example2.py` 学习类型转换
4. 运行 `examples/example3.py` 掌握字符串操作

### 第二步：动手练习
1. 阅读 `exercises/README.md` 了解练习要求
2. 依次完成三个练习题
3. 对比参考答案，查漏补缺

### 第三步：项目实践
1. 阅读 `project/README.md` 了解项目需求
2. 运行 `project/examples/demo_usage.py` 查看演示
3. 运行 `project/main.py` 体验完整项目
4. 尝试修改和扩展项目功能

## 💡 重要概念详解

### 变量的动态类型

Python是动态类型语言，变量的类型可以改变：

```python
x = 42          # x是整数
print(type(x))  # <class 'int'>

x = "Hello"     # x现在是字符串
print(type(x))  # <class 'str'>

x = 3.14        # x现在是浮点数
print(type(x))  # <class 'float'>
```

### 字符串的不可变性

```python
text = "Hello"
# text[0] = "h"  # 错误！字符串不可变

# 正确的方式是创建新字符串
new_text = "h" + text[1:]  # "hello"
```

### 类型转换的注意事项

```python
# 安全的类型转换
try:
    age = int(input("请输入年龄: "))
except ValueError:
    print("输入的不是有效数字")

# 布尔值转换的特殊情况
print(bool(0))      # False
print(bool(""))     # False
print(bool("0"))    # True（非空字符串）
```

## 🎯 学习检查清单

完成本节学习后，你应该能够：

- [ ] 创建和使用不同类型的变量
- [ ] 理解Python的基本数据类型
- [ ] 在不同数据类型之间进行转换
- [ ] 使用字符串的常用方法
- [ ] 格式化字符串输出
- [ ] 处理用户输入和类型转换
- [ ] 编写简单的数据处理程序
- [ ] 应用所学知识完成实际项目

## 🎉 下一步

完成本节学习后，你可以：

1. **继续学习Session 03**：控制结构（条件语句和循环）
2. **深入项目实践**：扩展个人信息管理系统的功能
3. **探索更多数据类型**：列表、字典、集合等
4. **学习函数编程**：如何组织和重用代码

---

**记住**：编程是一门实践性很强的技能，多写代码、多实验、多思考是提高的最好方法！

🚀 **开始你的Python编程之旅吧！**