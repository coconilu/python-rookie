# Session02: 变量与数据类型详细教程

## 1. 变量的概念

### 什么是变量？

变量是程序中用来存储数据的容器。你可以把变量想象成一个带标签的盒子，盒子里可以放不同类型的物品（数据），而标签就是变量名。

```python
# 创建变量
name = "张三"        # 字符串变量
age = 25            # 整数变量
height = 175.5      # 浮点数变量
is_student = True   # 布尔变量
```

### 变量的特点

1. **动态类型**：Python会根据赋值自动确定变量类型
2. **可重新赋值**：变量的值和类型都可以改变
3. **区分大小写**：`name` 和 `Name` 是不同的变量

```python
# 演示动态类型
x = 10          # x 是整数
print(type(x))  # <class 'int'>

x = "Hello"     # x 现在是字符串
print(type(x))  # <class 'str'>

x = 3.14        # x 现在是浮点数
print(type(x))  # <class 'float'>
```

## 2. 基本数据类型

### 2.1 整数类型（int）

整数类型用于表示没有小数部分的数字。

```python
# 整数的定义
positive_num = 42       # 正整数
negative_num = -17      # 负整数
zero = 0               # 零

# 不同进制的表示
binary_num = 0b1010    # 二进制，等于十进制的10
octal_num = 0o12       # 八进制，等于十进制的10
hex_num = 0xa          # 十六进制，等于十进制的10

print(f"二进制 {binary_num}, 八进制 {octal_num}, 十六进制 {hex_num}")
# 输出: 二进制 10, 八进制 10, 十六进制 10
```

### 2.2 浮点数类型（float）

浮点数类型用于表示带有小数部分的数字。

```python
# 浮点数的定义
pi = 3.14159
temperature = -2.5
scientific = 1.23e-4   # 科学计数法，等于 0.000123

# 浮点数的精度问题
result = 0.1 + 0.2
print(result)          # 0.30000000000000004
print(round(result, 1)) # 0.3

# 使用 decimal 模块获得精确计算
from decimal import Decimal
accurate_result = Decimal('0.1') + Decimal('0.2')
print(accurate_result)  # 0.3
```

### 2.3 字符串类型（str）

字符串用于表示文本数据，可以使用单引号、双引号或三引号。

```python
# 字符串的定义
single_quote = 'Hello World'
double_quote = "Python Programming"
triple_quote = """这是一个
多行字符串
可以包含换行符"""

# 字符串的基本操作
first_name = "张"
last_name = "三"
full_name = first_name + last_name  # 字符串连接
print(full_name)  # 张三

# 字符串格式化
name = "李四"
age = 30
message = f"我叫{name}，今年{age}岁"  # f-string格式化
print(message)  # 我叫李四，今年30岁

# 字符串方法
text = "  Python Programming  "
print(text.strip())      # 去除首尾空格
print(text.upper())      # 转换为大写
print(text.lower())      # 转换为小写
print(text.replace("Python", "Java"))  # 替换
```

### 2.4 布尔类型（bool）

布尔类型只有两个值：`True` 和 `False`，用于表示真假。

```python
# 布尔值的定义
is_sunny = True
is_raining = False

# 布尔值的产生
age = 18
is_adult = age >= 18    # True
is_child = age < 12     # False

# 布尔值在条件判断中的应用
if is_adult:
    print("可以投票")
else:
    print("不能投票")

# 真值测试
print(bool(1))      # True
print(bool(0))      # False
print(bool(""))     # False（空字符串）
print(bool("hello")) # True（非空字符串）
print(bool([]))     # False（空列表）
print(bool([1, 2])) # True（非空列表）
```

## 3. 变量命名规范

### 3.1 命名规则（必须遵守）

```python
# 正确的变量名
user_name = "张三"      # 使用下划线连接
age2 = 25              # 可以包含数字
_private_var = "私有"   # 可以以下划线开头

# 错误的变量名（会导致语法错误）
# 2age = 25            # 不能以数字开头
# user-name = "张三"    # 不能包含连字符
# class = "学生"        # 不能使用关键字
```

### 3.2 命名约定（建议遵守）

```python
# 推荐的命名风格
student_name = "李四"        # 小写字母+下划线（snake_case）
total_score = 95            # 有意义的名称
MAX_RETRY_COUNT = 3         # 常量使用大写字母

# 不推荐的命名风格
a = "李四"                   # 名称无意义
studentName = "李四"         # 驼峰命名（不符合Python约定）
s = 95                      # 名称过短
very_very_long_variable_name_that_is_hard_to_read = "值"  # 名称过长
```

## 4. 类型检查与转换

### 4.1 类型检查

```python
# 使用 type() 函数检查类型
name = "Python"
age = 25
height = 175.5
is_student = True

print(type(name))       # <class 'str'>
print(type(age))        # <class 'int'>
print(type(height))     # <class 'float'>
print(type(is_student)) # <class 'bool'>

# 使用 isinstance() 函数检查类型
print(isinstance(name, str))    # True
print(isinstance(age, int))     # True
print(isinstance(height, float)) # True
```

### 4.2 类型转换

```python
# 字符串转数字
age_str = "25"
age_int = int(age_str)      # 字符串转整数
print(age_int + 5)          # 30

price_str = "19.99"
price_float = float(price_str)  # 字符串转浮点数
print(price_float * 2)      # 39.98

# 数字转字符串
age = 25
age_str = str(age)          # 整数转字符串
message = "我今年" + age_str + "岁"
print(message)              # 我今年25岁

# 其他类型转布尔
print(bool(1))              # True
print(bool(0))              # False
print(bool("hello"))        # True
print(bool(""))             # False

# 类型转换的注意事项
try:
    invalid_int = int("hello")  # 这会引发错误
except ValueError as e:
    print(f"转换错误: {e}")
```

## 5. 实际应用示例

### 5.1 用户信息收集

```python
# 收集用户信息
print("=== 用户信息登记 ===")
name = input("请输入您的姓名: ")
age_str = input("请输入您的年龄: ")
height_str = input("请输入您的身高(cm): ")
is_student_str = input("您是学生吗？(yes/no): ")

# 类型转换
age = int(age_str)
height = float(height_str)
is_student = is_student_str.lower() == 'yes'

# 信息处理和显示
print("\n=== 您的信息 ===")
print(f"姓名: {name}")
print(f"年龄: {age}岁")
print(f"身高: {height}cm")
print(f"学生身份: {'是' if is_student else '否'}")

# 根据信息做判断
if age >= 18:
    print("您已成年")
else:
    print(f"您还有{18-age}年成年")

if height > 170:
    print("您的身高在平均水平以上")
else:
    print("您的身高在平均水平以下")
```

### 5.2 简单计算器

```python
# 简单的数学计算
print("=== 简单计算器 ===")
num1_str = input("请输入第一个数字: ")
operator = input("请输入运算符 (+, -, *, /): ")
num2_str = input("请输入第二个数字: ")

# 转换为数字
num1 = float(num1_str)
num2 = float(num2_str)

# 执行计算
if operator == '+':
    result = num1 + num2
elif operator == '-':
    result = num1 - num2
elif operator == '*':
    result = num1 * num2
elif operator == '/':
    if num2 != 0:
        result = num1 / num2
    else:
        result = "错误：除数不能为零"
else:
    result = "错误：不支持的运算符"

print(f"计算结果: {num1} {operator} {num2} = {result}")
```

## 6. 常见错误和调试

### 6.1 类型错误

```python
# 错误示例：类型不匹配
age = "25"  # 字符串
# next_year = age + 1  # TypeError: 不能将字符串和整数相加

# 正确做法：先转换类型
age = int("25")
next_year = age + 1
print(f"明年您{next_year}岁")
```

### 6.2 变量未定义

```python
# 错误示例：使用未定义的变量
# print(undefined_variable)  # NameError: name 'undefined_variable' is not defined

# 正确做法：先定义再使用
defined_variable = "Hello"
print(defined_variable)
```

### 6.3 类型转换错误

```python
# 错误示例：无效的类型转换
try:
    number = int("hello")  # ValueError: invalid literal for int()
except ValueError:
    print("输入的不是有效数字")
    number = 0  # 设置默认值
```

## 7. 最佳实践

### 7.1 变量命名

```python
# 好的命名
user_name = "张三"
total_price = 199.99
is_valid_email = True
MAX_ATTEMPTS = 3

# 避免的命名
a = "张三"          # 无意义
tp = 199.99        # 缩写不清楚
flag = True        # 用途不明确
```

### 7.2 类型提示（可选）

```python
# 使用类型提示提高代码可读性
def calculate_bmi(weight: float, height: float) -> float:
    """计算BMI指数"""
    return weight / (height ** 2)

# 变量类型提示
name: str = "张三"
age: int = 25
height: float = 1.75
is_student: bool = True
```

## 8. 练习建议

1. **基础练习**：创建不同类型的变量，练习类型转换
2. **应用练习**：编写程序收集和处理用户输入
3. **调试练习**：故意制造类型错误，学会调试
4. **命名练习**：为不同场景的变量选择合适的名称

## 9. 总结

- 变量是存储数据的容器，Python是动态类型语言
- 四种基本数据类型：int、float、str、bool
- 遵循命名规范，使用有意义的变量名
- 掌握类型检查和类型转换的方法
- 注意类型相关的常见错误和调试方法

通过本课的学习，你应该能够熟练使用变量和基本数据类型，为后续的编程学习打下坚实基础。