# Session 06: 函数编程 - 详细教程

## 📖 课程概述

函数是编程的核心概念之一，它让我们能够将代码组织成可重用的模块。通过函数，我们可以避免重复代码，提高程序的可读性和可维护性。本课程将深入学习Python函数的各个方面，从基础语法到高级特性，最终通过一个完整的文本处理工具集项目来实践所学知识。

## 🎯 学习路线图

```
函数编程
├── 函数基础
│   ├── 函数定义与调用
│   ├── 函数文档字符串
│   └── 函数命名规范
├── 参数系统
│   ├── 位置参数
│   ├── 关键字参数
│   ├── 默认参数
│   ├── 可变参数 (*args)
│   └── 关键字可变参数 (**kwargs)
├── 返回值
│   ├── 单个返回值
│   ├── 多个返回值
│   └── 无返回值函数
├── 作用域
│   ├── 局部作用域
│   ├── 全局作用域
│   ├── global关键字
│   └── nonlocal关键字
├── 高级特性
│   ├── Lambda函数
│   ├── 高阶函数
│   ├── 装饰器基础
│   └── 递归函数
└── 实际应用
    ├── 函数设计原则
    ├── 错误处理
    └── 性能优化
```

---

## 1. 函数基础

### 1.1 为什么需要函数？

想象一下，如果我们要计算多个圆的面积：

```python
# 没有函数的代码（重复且难维护）
radius1 = 5
area1 = 3.14159 * radius1 ** 2
print(f"圆1的面积: {area1}")

radius2 = 3
area2 = 3.14159 * radius2 ** 2
print(f"圆2的面积: {area2}")

radius3 = 7
area3 = 3.14159 * radius3 ** 2
print(f"圆3的面积: {area3}")
```

使用函数后：

```python
# 使用函数（简洁且可重用）
def calculate_circle_area(radius):
    """计算圆的面积"""
    return 3.14159 * radius ** 2

# 调用函数
for radius in [5, 3, 7]:
    area = calculate_circle_area(radius)
    print(f"半径{radius}的圆面积: {area:.2f}")
```

### 1.2 函数定义语法

```python
def function_name(parameters):
    """
    函数文档字符串（可选但推荐）
    描述函数的功能、参数和返回值
    """
    # 函数体
    # 执行具体的操作
    return result  # 返回结果（可选）
```

**语法要点：**
- `def` 关键字开始函数定义
- 函数名遵循变量命名规则
- 参数列表用圆括号包围
- 冒号结束函数头
- 函数体需要缩进
- `return` 语句返回结果（可选）

### 1.3 函数文档字符串

良好的文档是专业代码的标志：

```python
def calculate_bmi(weight, height):
    """
    计算身体质量指数(BMI)
    
    参数:
        weight (float): 体重，单位为千克
        height (float): 身高，单位为米
    
    返回:
        float: BMI值
    
    示例:
        >>> calculate_bmi(70, 1.75)
        22.86
    """
    if height <= 0:
        raise ValueError("身高必须大于0")
    
    bmi = weight / (height ** 2)
    return round(bmi, 2)

# 访问文档字符串
print(calculate_bmi.__doc__)
help(calculate_bmi)
```

---

## 2. 参数系统详解

### 2.1 位置参数

位置参数按照定义的顺序传递：

```python
def introduce_person(name, age, city):
    """介绍一个人的基本信息"""
    return f"我叫{name}，今年{age}岁，来自{city}"

# 位置参数调用
result = introduce_person("张三", 25, "北京")
print(result)  # 我叫张三，今年25岁，来自北京
```

### 2.2 关键字参数

关键字参数通过参数名指定值：

```python
# 关键字参数调用
result1 = introduce_person(name="李四", age=30, city="上海")
result2 = introduce_person(city="广州", name="王五", age=28)  # 顺序可以改变
result3 = introduce_person("赵六", city="深圳", age=32)      # 混合使用

print(result1)
print(result2)
print(result3)
```

### 2.3 默认参数

为参数提供默认值，使函数调用更灵活：

```python
def create_user_profile(username, email, role="user", active=True):
    """
    创建用户档案
    
    参数:
        username (str): 用户名
        email (str): 邮箱地址
        role (str): 用户角色，默认为'user'
        active (bool): 是否激活，默认为True
    """
    profile = {
        "username": username,
        "email": email,
        "role": role,
        "active": active
    }
    return profile

# 不同的调用方式
user1 = create_user_profile("alice", "alice@example.com")
user2 = create_user_profile("bob", "bob@example.com", "admin")
user3 = create_user_profile("charlie", "charlie@example.com", active=False)

print(user1)
print(user2)
print(user3)
```

**默认参数的注意事项：**

```python
# 危险：使用可变对象作为默认参数
def add_item_bad(item, target_list=[]):
    target_list.append(item)
    return target_list

# 每次调用都会修改同一个列表
list1 = add_item_bad("apple")
list2 = add_item_bad("banana")
print(list1)  # ['apple', 'banana'] - 意外的结果！
print(list2)  # ['apple', 'banana']

# 正确：使用None作为默认值
def add_item_good(item, target_list=None):
    if target_list is None:
        target_list = []
    target_list.append(item)
    return target_list

# 每次调用都创建新列表
list3 = add_item_good("apple")
list4 = add_item_good("banana")
print(list3)  # ['apple']
print(list4)  # ['banana']
```

### 2.4 可变参数 (*args)

处理不确定数量的位置参数：

```python
def calculate_sum(*numbers):
    """
    计算任意数量数字的和
    
    参数:
        *numbers: 任意数量的数字
    
    返回:
        数字的总和
    """
    total = 0
    for num in numbers:
        total += num
    return total

# 不同数量的参数
print(calculate_sum(1, 2, 3))           # 6
print(calculate_sum(1, 2, 3, 4, 5))     # 15
print(calculate_sum())                  # 0

# 传递列表
numbers_list = [10, 20, 30]
print(calculate_sum(*numbers_list))     # 60 (使用*解包)
```

### 2.5 关键字可变参数 (**kwargs)

处理不确定数量的关键字参数：

```python
def create_database_connection(**config):
    """
    创建数据库连接
    
    参数:
        **config: 数据库配置参数
    
    返回:
        连接配置字典
    """
    default_config = {
        "host": "localhost",
        "port": 5432,
        "database": "mydb",
        "timeout": 30
    }
    
    # 更新默认配置
    default_config.update(config)
    
    print("数据库连接配置:")
    for key, value in default_config.items():
        print(f"  {key}: {value}")
    
    return default_config

# 不同的配置
conn1 = create_database_connection()
conn2 = create_database_connection(host="192.168.1.100", port=3306)
conn3 = create_database_connection(database="production", user="admin", password="secret")
```

### 2.6 参数组合使用

```python
def flexible_function(required_arg, default_arg="default", *args, **kwargs):
    """
    演示所有类型参数的组合使用
    
    参数:
        required_arg: 必需的位置参数
        default_arg: 有默认值的参数
        *args: 可变位置参数
        **kwargs: 可变关键字参数
    """
    print(f"必需参数: {required_arg}")
    print(f"默认参数: {default_arg}")
    print(f"额外位置参数: {args}")
    print(f"关键字参数: {kwargs}")
    print("-" * 40)

# 各种调用方式
flexible_function("hello")
flexible_function("hello", "world")
flexible_function("hello", "world", 1, 2, 3)
flexible_function("hello", "world", 1, 2, 3, name="Alice", age=25)
```

---

## 3. 返回值详解

### 3.1 单个返回值

```python
def get_circle_area(radius):
    """返回圆的面积"""
    return 3.14159 * radius ** 2

def get_greeting(name):
    """返回问候语"""
    return f"Hello, {name}!"

def is_even(number):
    """判断数字是否为偶数"""
    return number % 2 == 0

# 使用返回值
area = get_circle_area(5)
message = get_greeting("Alice")
even_check = is_even(10)

print(f"面积: {area}")
print(message)
print(f"10是偶数: {even_check}")
```

### 3.2 多个返回值

Python可以返回多个值（实际上是返回元组）：

```python
def get_name_parts(full_name):
    """
    分解全名为姓和名
    
    参数:
        full_name (str): 完整姓名
    
    返回:
        tuple: (姓, 名)
    """
    parts = full_name.split()
    if len(parts) >= 2:
        return parts[0], " ".join(parts[1:])
    else:
        return parts[0], ""

def calculate_rectangle_properties(length, width):
    """
    计算矩形的周长和面积
    
    返回:
        tuple: (周长, 面积)
    """
    perimeter = 2 * (length + width)
    area = length * width
    return perimeter, area

# 接收多个返回值
first_name, last_name = get_name_parts("张 三")
print(f"姓: {first_name}, 名: {last_name}")

# 可以用元组接收
result = calculate_rectangle_properties(5, 3)
print(f"周长: {result[0]}, 面积: {result[1]}")

# 或者分别接收
perimeter, area = calculate_rectangle_properties(5, 3)
print(f"周长: {perimeter}, 面积: {area}")
```

### 3.3 无返回值函数

有些函数主要执行操作而不返回值：

```python
def print_user_info(user_dict):
    """
    打印用户信息（无返回值）
    """
    print("=== 用户信息 ===")
    for key, value in user_dict.items():
        print(f"{key}: {value}")
    print("=" * 20)

def log_message(message, level="INFO"):
    """
    记录日志消息
    """
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")

# 调用无返回值函数
user = {"name": "Alice", "age": 25, "city": "Beijing"}
print_user_info(user)
log_message("系统启动成功")
log_message("发现错误", "ERROR")
```

---

## 4. 作用域详解

### 4.1 局部作用域和全局作用域

```python
# 全局变量
global_counter = 0
global_message = "这是全局消息"

def demonstrate_scope():
    # 局部变量
    local_counter = 10
    local_message = "这是局部消息"
    
    print(f"局部计数器: {local_counter}")
    print(f"局部消息: {local_message}")
    print(f"全局计数器: {global_counter}")  # 可以访问全局变量
    print(f"全局消息: {global_message}")

demonstrate_scope()

# print(local_counter)  # 错误！局部变量在函数外不可访问
print(f"函数外的全局计数器: {global_counter}")
```

### 4.2 global关键字

在函数内修改全局变量：

```python
counter = 0  # 全局变量

def increment_counter():
    global counter  # 声明要修改全局变量
    counter += 1
    print(f"计数器增加到: {counter}")

def reset_counter():
    global counter
    counter = 0
    print("计数器已重置")

print(f"初始计数器: {counter}")
increment_counter()
increment_counter()
increment_counter()
reset_counter()
```

### 4.3 nonlocal关键字

在嵌套函数中修改外层函数的变量：

```python
def create_counter():
    """创建一个计数器函数"""
    count = 0  # 外层函数的局部变量
    
    def increment():
        nonlocal count  # 声明要修改外层函数的变量
        count += 1
        return count
    
    def decrement():
        nonlocal count
        count -= 1
        return count
    
    def get_count():
        return count  # 只读访问不需要nonlocal
    
    # 返回内层函数
    return increment, decrement, get_count

# 创建计数器
inc, dec, get = create_counter()

print(f"当前计数: {get()}")  # 0
print(f"增加后: {inc()}")     # 1
print(f"增加后: {inc()}")     # 2
print(f"减少后: {dec()}")     # 1
print(f"当前计数: {get()}")   # 1
```

---

## 5. 高级特性

### 5.1 Lambda函数

Lambda函数是简短的匿名函数：

```python
# 普通函数
def square(x):
    return x ** 2

# 等价的lambda函数
square_lambda = lambda x: x ** 2

print(square(5))        # 25
print(square_lambda(5)) # 25

# Lambda函数常用于高阶函数
numbers = [1, 2, 3, 4, 5]

# 使用map
squared = list(map(lambda x: x ** 2, numbers))
print(f"平方: {squared}")  # [1, 4, 9, 16, 25]

# 使用filter
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(f"偶数: {even_numbers}")  # [2, 4]

# 使用sorted
students = [("Alice", 85), ("Bob", 90), ("Charlie", 78)]
sorted_by_score = sorted(students, key=lambda student: student[1])
print(f"按分数排序: {sorted_by_score}")
```

### 5.2 高阶函数

接受函数作为参数或返回函数的函数：

```python
def apply_operation(numbers, operation):
    """
    对数字列表应用指定操作
    
    参数:
        numbers (list): 数字列表
        operation (function): 要应用的操作函数
    
    返回:
        list: 操作后的结果列表
    """
    return [operation(num) for num in numbers]

def create_multiplier(factor):
    """
    创建一个乘法函数
    
    参数:
        factor (int): 乘数
    
    返回:
        function: 乘法函数
    """
    def multiplier(x):
        return x * factor
    return multiplier

# 使用高阶函数
numbers = [1, 2, 3, 4, 5]

# 传递函数作为参数
squared = apply_operation(numbers, lambda x: x ** 2)
print(f"平方: {squared}")

# 函数返回函数
double = create_multiplier(2)
triple = create_multiplier(3)

print(f"2倍: {apply_operation(numbers, double)}")
print(f"3倍: {apply_operation(numbers, triple)}")
```

### 5.3 装饰器基础

装饰器是修改或增强函数功能的高级技术：

```python
import time
import functools

def timing_decorator(func):
    """
    计时装饰器：测量函数执行时间
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 执行时间: {end_time - start_time:.4f}秒")
        return result
    return wrapper

def log_decorator(func):
    """
    日志装饰器：记录函数调用
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"调用函数: {func.__name__}")
        print(f"参数: args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"返回值: {result}")
        return result
    return wrapper

# 使用装饰器
@timing_decorator
@log_decorator
def calculate_fibonacci(n):
    """计算斐波那契数列的第n项"""
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

# 调用被装饰的函数
result = calculate_fibonacci(10)
print(f"斐波那契数列第10项: {result}")
```

### 5.4 递归函数

函数调用自身来解决问题：

```python
def factorial(n):
    """
    计算阶乘（递归实现）
    
    参数:
        n (int): 非负整数
    
    返回:
        int: n的阶乘
    """
    # 基础情况
    if n == 0 or n == 1:
        return 1
    # 递归情况
    return n * factorial(n - 1)

def fibonacci_recursive(n):
    """
    计算斐波那契数列（递归实现）
    """
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

def fibonacci_iterative(n):
    """
    计算斐波那契数列（迭代实现，更高效）
    """
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# 比较递归和迭代
print("阶乘:")
for i in range(6):
    print(f"{i}! = {factorial(i)}")

print("\n斐波那契数列（递归）:")
for i in range(10):
    print(f"F({i}) = {fibonacci_recursive(i)}")

print("\n斐波那契数列（迭代）:")
for i in range(10):
    print(f"F({i}) = {fibonacci_iterative(i)}")
```

---

## 6. 函数设计最佳实践

### 6.1 单一职责原则

每个函数应该只做一件事：

```python
# 不好的设计：函数做了太多事情
def process_user_data_bad(user_data):
    # 验证数据
    if not user_data.get("email"):
        raise ValueError("邮箱不能为空")
    
    # 格式化数据
    user_data["name"] = user_data["name"].title()
    
    # 保存到数据库
    print(f"保存用户: {user_data}")
    
    # 发送欢迎邮件
    print(f"发送欢迎邮件到: {user_data['email']}")
    
    return user_data

# 好的设计：每个函数职责单一
def validate_user_data(user_data):
    """验证用户数据"""
    if not user_data.get("email"):
        raise ValueError("邮箱不能为空")
    if not user_data.get("name"):
        raise ValueError("姓名不能为空")
    return True

def format_user_data(user_data):
    """格式化用户数据"""
    formatted_data = user_data.copy()
    formatted_data["name"] = formatted_data["name"].title()
    formatted_data["email"] = formatted_data["email"].lower()
    return formatted_data

def save_user_to_database(user_data):
    """保存用户到数据库"""
    print(f"保存用户到数据库: {user_data}")
    return True

def send_welcome_email(email):
    """发送欢迎邮件"""
    print(f"发送欢迎邮件到: {email}")
    return True

def process_user_data_good(user_data):
    """处理用户数据（协调函数）"""
    validate_user_data(user_data)
    formatted_data = format_user_data(user_data)
    save_user_to_database(formatted_data)
    send_welcome_email(formatted_data["email"])
    return formatted_data
```

### 6.2 错误处理

```python
def safe_divide(a, b):
    """
    安全的除法运算
    
    参数:
        a (float): 被除数
        b (float): 除数
    
    返回:
        float: 除法结果
    
    异常:
        ValueError: 当除数为0时
        TypeError: 当参数不是数字时
    """
    try:
        # 类型检查
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("参数必须是数字")
        
        # 零除检查
        if b == 0:
            raise ValueError("除数不能为0")
        
        return a / b
    
    except Exception as e:
        print(f"计算错误: {e}")
        raise

def read_file_safely(filename):
    """
    安全地读取文件
    
    参数:
        filename (str): 文件名
    
    返回:
        str: 文件内容，如果失败返回None
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"文件 {filename} 不存在")
        return None
    except PermissionError:
        print(f"没有权限读取文件 {filename}")
        return None
    except Exception as e:
        print(f"读取文件时发生未知错误: {e}")
        return None

# 使用示例
try:
    result = safe_divide(10, 2)
    print(f"10 / 2 = {result}")
    
    result = safe_divide(10, 0)  # 会抛出异常
except ValueError as e:
    print(f"数值错误: {e}")

content = read_file_safely("example.txt")
if content:
    print("文件读取成功")
else:
    print("文件读取失败")
```

### 6.3 性能优化技巧

```python
import time
from functools import lru_cache

# 使用缓存优化递归函数
@lru_cache(maxsize=None)
def fibonacci_cached(n):
    """使用缓存的斐波那契函数"""
    if n <= 1:
        return n
    return fibonacci_cached(n-1) + fibonacci_cached(n-2)

def benchmark_fibonacci(n):
    """比较不同斐波那契实现的性能"""
    # 递归实现（慢）
    start = time.time()
    result1 = fibonacci_recursive(n)
    time1 = time.time() - start
    
    # 缓存递归实现（快）
    start = time.time()
    result2 = fibonacci_cached(n)
    time2 = time.time() - start
    
    # 迭代实现（最快）
    start = time.time()
    result3 = fibonacci_iterative(n)
    time3 = time.time() - start
    
    print(f"计算斐波那契数列第{n}项:")
    print(f"递归实现: {result1}, 耗时: {time1:.6f}秒")
    print(f"缓存递归: {result2}, 耗时: {time2:.6f}秒")
    print(f"迭代实现: {result3}, 耗时: {time3:.6f}秒")

# 性能测试
benchmark_fibonacci(30)
```

---

## 7. 实际应用示例

### 7.1 文本处理工具函数

```python
import re
from collections import Counter

def count_words(text):
    """
    统计文本中的单词数量
    
    参数:
        text (str): 输入文本
    
    返回:
        dict: 单词计数字典
    """
    # 转换为小写并提取单词
    words = re.findall(r'\b\w+\b', text.lower())
    return dict(Counter(words))

def remove_punctuation(text):
    """
    移除文本中的标点符号
    
    参数:
        text (str): 输入文本
    
    返回:
        str: 移除标点后的文本
    """
    return re.sub(r'[^\w\s]', '', text)

def capitalize_sentences(text):
    """
    将每个句子的首字母大写
    
    参数:
        text (str): 输入文本
    
    返回:
        str: 处理后的文本
    """
    sentences = re.split(r'[.!?]+', text)
    capitalized = [sentence.strip().capitalize() for sentence in sentences if sentence.strip()]
    return '. '.join(capitalized) + '.'

def extract_emails(text):
    """
    从文本中提取邮箱地址
    
    参数:
        text (str): 输入文本
    
    返回:
        list: 邮箱地址列表
    """
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, text)

def text_statistics(text):
    """
    计算文本统计信息
    
    参数:
        text (str): 输入文本
    
    返回:
        dict: 统计信息字典
    """
    words = re.findall(r'\b\w+\b', text)
    sentences = re.split(r'[.!?]+', text)
    paragraphs = text.split('\n\n')
    
    return {
        "字符数": len(text),
        "单词数": len(words),
        "句子数": len([s for s in sentences if s.strip()]),
        "段落数": len([p for p in paragraphs if p.strip()]),
        "平均单词长度": sum(len(word) for word in words) / len(words) if words else 0
    }

# 使用示例
sample_text = """
Hello world! This is a sample text for testing.
It contains multiple sentences and some email addresses like test@example.com.
We can analyze this text using our functions.
"""

print("=== 文本处理示例 ===")
print(f"原文本:\n{sample_text}")
print("\n=== 统计信息 ===")
stats = text_statistics(sample_text)
for key, value in stats.items():
    print(f"{key}: {value}")

print("\n=== 单词计数 ===")
word_count = count_words(sample_text)
for word, count in sorted(word_count.items()):
    print(f"{word}: {count}")

print("\n=== 提取的邮箱 ===")
emails = extract_emails(sample_text)
for email in emails:
    print(email)
```

---

## 8. 总结

### 8.1 函数编程的核心概念

1. **模块化**：将复杂问题分解为简单的函数
2. **重用性**：编写一次，多处使用
3. **可读性**：函数名和文档字符串提高代码可读性
4. **可测试性**：独立的函数更容易测试
5. **可维护性**：修改功能只需要修改对应的函数

### 8.2 函数设计检查清单

- [ ] 函数名清晰描述功能
- [ ] 参数数量合理（通常不超过5个）
- [ ] 有完整的文档字符串
- [ ] 单一职责原则
- [ ] 适当的错误处理
- [ ] 返回值类型一致
- [ ] 避免副作用（除非必要）
- [ ] 考虑性能影响

### 8.3 下一步学习

掌握了函数编程后，你可以继续学习：
- 面向对象编程（类和对象）
- 模块和包的组织
- 异常处理的高级技巧
- 函数式编程的高级概念
- 代码测试和调试技巧

---

**恭喜你完成了函数编程的学习！现在你已经掌握了编程的重要基础，可以开始构建更复杂和强大的程序了！** 🎉