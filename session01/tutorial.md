# Session01: 环境搭建与Hello World - 详细教程

## 1. Python环境搭建

### 1.1 什么是Python？

Python是一种高级编程语言，由Guido van Rossum于1991年首次发布。它以简洁、易读的语法著称，是初学者学习编程的理想选择。

**Python的特点：**
- 语法简洁明了
- 跨平台支持
- 丰富的标准库
- 活跃的社区支持
- 广泛的应用领域

### 1.2 使用uv管理Python环境

在本教程中，我们使用uv作为Python版本和依赖管理工具。uv是一个现代化的Python包管理器，比传统的pip更快更可靠。

#### 安装uv

**Windows系统：**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux系统：**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 验证安装
```bash
uv --version
```

### 1.3 创建Python项目

```bash
# 创建新项目
uv init my-first-python-project
cd my-first-python-project

# 指定Python版本
uv python install 3.11.12
uv python pin 3.11.12
```

## 2. IDE选择与配置

### 2.1 推荐的IDE

**VS Code（推荐初学者）**
- 免费开源
- 轻量级
- 丰富的插件生态
- 优秀的Python支持

**PyCharm**
- 专业的Python IDE
- 强大的调试功能
- 智能代码补全
- 适合大型项目开发

### 2.2 VS Code配置

1. **安装VS Code**
   - 访问 https://code.visualstudio.com/
   - 下载并安装适合你操作系统的版本

2. **安装Python扩展**
   - 打开VS Code
   - 按 `Ctrl+Shift+X` 打开扩展面板
   - 搜索"Python"并安装Microsoft官方扩展

3. **配置Python解释器**
   - 按 `Ctrl+Shift+P` 打开命令面板
   - 输入"Python: Select Interpreter"
   - 选择uv创建的虚拟环境中的Python解释器

## 3. 第一个Python程序

### 3.1 Hello World

创建一个名为 `hello.py` 的文件：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
我的第一个Python程序

这个程序演示了Python的基本输出功能
"""

print("Hello, World!")
print("欢迎来到Python的世界！")
```

**运行程序：**
```bash
uv run python hello.py
```

**预期输出：**
```
Hello, World!
欢迎来到Python的世界！
```

### 3.2 程序结构解析

1. **Shebang行** (`#!/usr/bin/env python3`)
   - 告诉系统使用Python3解释器
   - 在Unix/Linux系统中使程序可直接执行

2. **编码声明** (`# -*- coding: utf-8 -*-`)
   - 指定文件编码为UTF-8
   - 支持中文等非ASCII字符

3. **文档字符串** (`"""..."""`) 
   - 描述程序的功能
   - 可以通过 `help()` 函数查看

4. **代码主体**
   - 实际的程序逻辑

## 4. 基本语法概念

### 4.1 输出函数 print()

`print()` 是Python中最常用的输出函数：

```python
# 基本用法
print("Hello, Python!")

# 输出多个值
print("姓名:", "张三", "年龄:", 25)

# 自定义分隔符
print("苹果", "香蕉", "橙子", sep=", ")

# 自定义结束符
print("第一行", end=" ")
print("第二行")
```

**运行结果：**
```
Hello, Python!
姓名: 张三 年龄: 25
苹果, 香蕉, 橙子
第一行 第二行
```

### 4.2 输入函数 input()

`input()` 函数用于获取用户输入：

```python
# 获取用户输入
name = input("请输入你的姓名: ")
print("你好,", name)

# 输入数字（需要类型转换）
age = int(input("请输入你的年龄: "))
print("你今年", age, "岁")
```

### 4.3 变量

变量是存储数据的容器：

```python
# 变量赋值
name = "Python"
version = 3.11
is_awesome = True

# 输出变量
print("语言:", name)
print("版本:", version)
print("是否很棒:", is_awesome)
```

**变量命名规则：**
- 只能包含字母、数字和下划线
- 不能以数字开头
- 区分大小写
- 不能使用Python关键字

**良好的命名习惯：**
```python
# 好的命名
user_name = "张三"
student_age = 20
total_score = 95.5

# 不好的命名
a = "张三"  # 不够描述性
UserName = "张三"  # 不符合Python命名规范
2name = "张三"  # 语法错误
```

### 4.4 注释

注释用于解释代码，不会被执行：

```python
# 这是单行注释
print("Hello")  # 行末注释

"""
这是多行注释
可以写很多行
通常用于函数和类的文档
"""

'''
这也是多行注释
使用单引号
'''
```

## 5. 实践练习

### 5.1 个人信息展示

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个人信息展示程序
"""

# 获取用户信息
name = input("请输入你的姓名: ")
age = int(input("请输入你的年龄: "))
city = input("请输入你的城市: ")
hobby = input("请输入你的爱好: ")

# 显示信息
print("\n=== 个人信息卡片 ===")
print(f"姓名: {name}")
print(f"年龄: {age}岁")
print(f"城市: {city}")
print(f"爱好: {hobby}")
print("===================")
```

### 5.2 简单计算器

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单计算器程序
"""

# 获取两个数字
num1 = float(input("请输入第一个数字: "))
num2 = float(input("请输入第二个数字: "))

# 进行计算
addition = num1 + num2
subtraction = num1 - num2
multiplication = num1 * num2
division = num1 / num2 if num2 != 0 else "无法除以零"

# 显示结果
print(f"\n计算结果:")
print(f"{num1} + {num2} = {addition}")
print(f"{num1} - {num2} = {subtraction}")
print(f"{num1} × {num2} = {multiplication}")
print(f"{num1} ÷ {num2} = {division}")
```

## 6. 常见错误与解决方案

### 6.1 语法错误

```python
# 错误：缺少引号
print(Hello World)  # SyntaxError

# 正确：
print("Hello World")
```

### 6.2 缩进错误

```python
# 错误：不必要的缩进
    print("Hello")  # IndentationError

# 正确：
print("Hello")
```

### 6.3 类型错误

```python
# 错误：字符串和数字直接相加
age = "25"
next_year = age + 1  # TypeError

# 正确：类型转换
age = int("25")
next_year = age + 1
```

## 7. 调试技巧

### 7.1 使用print()调试

```python
# 在关键位置添加print语句
num1 = 10
print(f"num1的值是: {num1}")  # 调试输出

num2 = 20
print(f"num2的值是: {num2}")  # 调试输出

result = num1 + num2
print(f"计算结果: {result}")  # 调试输出
```

### 7.2 使用IDE调试器

在VS Code中：
1. 在代码行号左侧点击设置断点
2. 按F5开始调试
3. 使用F10单步执行
4. 观察变量窗口中的值变化

## 8. 最佳实践

### 8.1 代码风格

```python
# 好的代码风格
def calculate_area(length, width):
    """
    计算矩形面积
    
    Args:
        length: 长度
        width: 宽度
    
    Returns:
        面积值
    """
    area = length * width
    return area

# 使用有意义的变量名
rectangle_length = 10
rectangle_width = 5
rectangle_area = calculate_area(rectangle_length, rectangle_width)
```

### 8.2 错误处理

```python
# 处理用户输入错误
try:
    age = int(input("请输入年龄: "))
    print(f"你的年龄是: {age}")
except ValueError:
    print("请输入有效的数字！")
```

## 9. 扩展阅读

- [Python官方教程](https://docs.python.org/3/tutorial/)
- [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- [uv官方文档](https://docs.astral.sh/uv/)

## 10. 下节预告

在下一课（Session02）中，我们将深入学习：
- Python的基本数据类型
- 变量的高级用法
- 类型转换的详细方法
- 字符串的基本操作

---

**记住**：编程是一门实践的艺术。不要只是阅读代码，一定要亲自动手编写和运行每一个示例！