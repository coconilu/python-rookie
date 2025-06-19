# Session03: 运算符与表达式 - 详细教程

## 📖 课程概述

运算符是编程语言的基本组成部分，它们允许我们对数据进行各种操作。在Python中，运算符可以分为算术运算符、比较运算符、逻辑运算符等几大类。掌握这些运算符的使用是编程的基础技能。

## 1. 算术运算符详解

### 1.1 基本算术运算

```python
# 基本四则运算
a = 10
b = 3

print(f"加法: {a} + {b} = {a + b}")     # 结果: 13
print(f"减法: {a} - {b} = {a - b}")     # 结果: 7
print(f"乘法: {a} * {b} = {a * b}")     # 结果: 30
print(f"除法: {a} / {b} = {a / b}")     # 结果: 3.3333333333333335
```

### 1.2 特殊算术运算

```python
# 整除运算
print(f"整除: {a} // {b} = {a // b}")   # 结果: 3

# 取模运算（求余数）
print(f"取模: {a} % {b} = {a % b}")     # 结果: 1

# 幂运算
print(f"幂运算: {a} ** {b} = {a ** b}") # 结果: 1000
```

### 1.3 运算符的实际应用

```python
# 判断奇偶数
number = 15
if number % 2 == 0:
    print(f"{number} 是偶数")
else:
    print(f"{number} 是奇数")

# 计算圆的面积
import math
radius = 5
area = math.pi * radius ** 2
print(f"半径为 {radius} 的圆的面积是: {area:.2f}")
```

## 2. 比较运算符详解

### 2.1 基本比较操作

```python
x = 5
y = 8
z = 5

print(f"{x} == {y}: {x == y}")  # False
print(f"{x} == {z}: {x == z}")  # True
print(f"{x} != {y}: {x != y}")  # True
print(f"{x} > {y}: {x > y}")    # False
print(f"{x} < {y}: {x < y}")    # True
print(f"{x} >= {z}: {x >= z}")  # True
print(f"{x} <= {y}: {x <= y}")  # True
```

### 2.2 字符串比较

```python
# 字符串比较（按字典序）
name1 = "Alice"
name2 = "Bob"
name3 = "Alice"

print(f"'{name1}' == '{name3}': {name1 == name3}")  # True
print(f"'{name1}' < '{name2}': {name1 < name2}")    # True (A < B)
print(f"'{name1}' > '{name2}': {name1 > name2}")    # False
```

### 2.3 数值类型比较

```python
# 不同数值类型的比较
int_num = 5
float_num = 5.0

print(f"{int_num} == {float_num}: {int_num == float_num}")  # True
print(f"类型相同吗: {type(int_num) == type(float_num)}")      # False
```

## 3. 逻辑运算符详解

### 3.1 基本逻辑运算

```python
# 逻辑与 (and)
print(f"True and True: {True and True}")     # True
print(f"True and False: {True and False}")   # False
print(f"False and True: {False and True}")   # False
print(f"False and False: {False and False}") # False

# 逻辑或 (or)
print(f"True or True: {True or True}")       # True
print(f"True or False: {True or False}")     # True
print(f"False or True: {False or True}")     # True
print(f"False or False: {False or False}")   # False

# 逻辑非 (not)
print(f"not True: {not True}")               # False
print(f"not False: {not False}")             # True
```

### 3.2 复合条件判断

```python
# 年龄和收入的复合判断
age = 25
income = 50000

# 同时满足年龄和收入条件
if age >= 18 and income >= 30000:
    print("符合贷款条件")
else:
    print("不符合贷款条件")

# 满足其中一个条件即可
if age >= 65 or income >= 100000:
    print("享受优惠政策")
else:
    print("不享受优惠政策")
```

### 3.3 短路求值

```python
# and 短路求值：如果第一个条件为False，不会执行第二个条件
def expensive_function():
    print("执行了昂贵的函数")
    return True

result1 = False and expensive_function()  # 不会打印"执行了昂贵的函数"
print(f"结果1: {result1}")

# or 短路求值：如果第一个条件为True，不会执行第二个条件
result2 = True or expensive_function()   # 不会打印"执行了昂贵的函数"
print(f"结果2: {result2}")
```

## 4. 运算符优先级

### 4.1 优先级表（从高到低）

1. `**` (幂运算)
2. `+x`, `-x`, `~x` (正号、负号、按位取反)
3. `*`, `/`, `//`, `%` (乘法、除法、整除、取模)
4. `+`, `-` (加法、减法)
5. `<<`, `>>` (位移运算)
6. `&` (按位与)
7. `^` (按位异或)
8. `|` (按位或)
9. `==`, `!=`, `<`, `<=`, `>`, `>=`, `is`, `is not`, `in`, `not in` (比较运算)
10. `not` (逻辑非)
11. `and` (逻辑与)
12. `or` (逻辑或)

### 4.2 优先级示例

```python
# 不使用括号的计算
result1 = 2 + 3 * 4      # 先乘后加: 2 + 12 = 14
print(f"2 + 3 * 4 = {result1}")

# 使用括号改变优先级
result2 = (2 + 3) * 4    # 先加后乘: 5 * 4 = 20
print(f"(2 + 3) * 4 = {result2}")

# 复杂表达式
result3 = 2 ** 3 * 4 + 5  # 2^3 * 4 + 5 = 8 * 4 + 5 = 37
print(f"2 ** 3 * 4 + 5 = {result3}")

# 逻辑运算优先级
result4 = True or False and False  # True or (False and False) = True
print(f"True or False and False = {result4}")
```

## 5. 赋值运算符

### 5.1 复合赋值运算符

```python
# 基本赋值
x = 10
print(f"初始值: x = {x}")

# 加法赋值
x += 5  # 等价于 x = x + 5
print(f"x += 5 后: x = {x}")

# 减法赋值
x -= 3  # 等价于 x = x - 3
print(f"x -= 3 后: x = {x}")

# 乘法赋值
x *= 2  # 等价于 x = x * 2
print(f"x *= 2 后: x = {x}")

# 除法赋值
x /= 4  # 等价于 x = x / 4
print(f"x /= 4 后: x = {x}")
```

## 6. 成员运算符

### 6.1 in 和 not in

```python
# 字符串中的成员检查
text = "Hello, Python!"
print(f"'Python' in '{text}': {'Python' in text}")      # True
print(f"'Java' not in '{text}': {'Java' not in text}")  # True

# 列表中的成员检查
fruits = ['apple', 'banana', 'orange']
print(f"'apple' in fruits: {'apple' in fruits}")        # True
print(f"'grape' in fruits: {'grape' in fruits}")        # False
```

## 7. 身份运算符

### 7.1 is 和 is not

```python
# 对象身份比较
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(f"a == b: {a == b}")      # True (内容相同)
print(f"a is b: {a is b}")      # False (不是同一个对象)
print(f"a is c: {a is c}")      # True (是同一个对象)

# None 的比较
value = None
print(f"value is None: {value is None}")          # True
print(f"value is not None: {value is not None}")  # False
```

## 8. 实际应用案例

### 8.1 温度转换器

```python
def celsius_to_fahrenheit(celsius):
    """摄氏度转华氏度"""
    fahrenheit = celsius * 9/5 + 32
    return fahrenheit

def fahrenheit_to_celsius(fahrenheit):
    """华氏度转摄氏度"""
    celsius = (fahrenheit - 32) * 5/9
    return celsius

# 测试温度转换
temp_c = 25
temp_f = celsius_to_fahrenheit(temp_c)
print(f"{temp_c}°C = {temp_f}°F")

temp_f = 77
temp_c = fahrenheit_to_celsius(temp_f)
print(f"{temp_f}°F = {temp_c:.1f}°C")
```

### 8.2 成绩等级判定

```python
def get_grade(score):
    """根据分数获取等级"""
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

# 测试成绩等级
scores = [95, 87, 76, 65, 45]
for score in scores:
    grade = get_grade(score)
    print(f"分数 {score}: 等级 {grade}")
```

### 8.3 密码强度检查

```python
def check_password_strength(password):
    """检查密码强度"""
    length_ok = len(password) >= 8
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in '!@#$%^&*()_+-=' for c in password)
    
    strength = 0
    if length_ok:
        strength += 1
    if has_upper:
        strength += 1
    if has_lower:
        strength += 1
    if has_digit:
        strength += 1
    if has_special:
        strength += 1
    
    if strength >= 4:
        return "强"
    elif strength >= 3:
        return "中等"
    elif strength >= 2:
        return "弱"
    else:
        return "很弱"

# 测试密码强度
passwords = ["123456", "Password", "Password123", "P@ssw0rd123"]
for pwd in passwords:
    strength = check_password_strength(pwd)
    print(f"密码 '{pwd}': 强度 {strength}")
```

## 9. 常见错误与注意事项

### 9.1 浮点数比较问题

```python
# 错误的浮点数比较
result = 0.1 + 0.2
print(f"0.1 + 0.2 = {result}")                    # 0.30000000000000004
print(f"0.1 + 0.2 == 0.3: {result == 0.3}")      # False

# 正确的浮点数比较
import math
print(f"使用 math.isclose: {math.isclose(result, 0.3)}")  # True

# 或者使用精度控制
print(f"使用 round: {round(result, 10) == 0.3}")          # True
```

### 9.2 整除运算的注意事项

```python
# 正数整除
print(f"7 // 2 = {7 // 2}")      # 3
print(f"7 / 2 = {7 / 2}")        # 3.5

# 负数整除（向下取整）
print(f"-7 // 2 = {-7 // 2}")    # -4 (不是 -3)
print(f"-7 / 2 = {-7 / 2}")      # -3.5
```

### 9.3 逻辑运算的陷阱

```python
# 空值的逻辑判断
values = [0, '', [], None, False, 'hello']

for value in values:
    if value:
        print(f"{repr(value)} 为真")
    else:
        print(f"{repr(value)} 为假")
```

## 10. 练习建议

1. **基础练习**：编写程序计算各种数学表达式
2. **条件判断**：使用比较和逻辑运算符编写条件语句
3. **实际应用**：完成BMI计算器项目
4. **调试练习**：故意写一些有运算符优先级问题的代码，然后修正

## 总结

运算符是编程的基础工具，掌握它们的正确使用方法对于编写高质量的代码至关重要。记住以下要点：

1. **算术运算符**：注意整除和取模的特殊用法
2. **比较运算符**：小心浮点数比较的精度问题
3. **逻辑运算符**：理解短路求值的机制
4. **运算符优先级**：使用括号明确运算顺序
5. **实际应用**：通过项目练习巩固理论知识

下一节课我们将学习控制流程，包括条件语句和循环语句，这将让我们能够编写更加复杂和有用的程序！