# Session04: 控制流程详细教程

## 📖 课程概述

控制流程是编程的核心概念之一，它决定了程序的执行顺序和逻辑。通过条件语句和循环语句，我们可以让程序根据不同的情况做出不同的反应，或者重复执行某些操作。掌握控制流程是编写复杂程序的基础。

## 1. 条件语句详解

### 1.1 基本 if 语句

```python
# 最简单的if语句
age = 18

if age >= 18:
    print("你已经成年了！")
    print("可以投票了！")

print("程序继续执行...")
```

**运行结果：**

```
你已经成年了！
可以投票了！
程序继续执行...
```

### 1.2 if-else 语句

```python
# if-else语句
score = 85

if score >= 60:
    print(f"恭喜！你的分数是{score}，考试通过了！")
else:
    print(f"很遗憾，你的分数是{score}，考试未通过。")
    print("请继续努力！")
```

**运行结果：**

```
恭喜！你的分数是85，考试通过了！
```

### 1.3 if-elif-else 语句

```python
# 多条件判断
score = 92

if score >= 90:
    grade = "A"
    comment = "优秀"
elif score >= 80:
    grade = "B"
    comment = "良好"
elif score >= 70:
    grade = "C"
    comment = "中等"
elif score >= 60:
    grade = "D"
    comment = "及格"
else:
    grade = "F"
    comment = "不及格"

print(f"分数：{score}")
print(f"等级：{grade}")
print(f"评价：{comment}")
```

**运行结果：**

```
分数：92
等级：A
评价：优秀
```

### 1.4 嵌套条件语句

```python
# 嵌套的条件语句
weather = "晴天"
temperature = 25

if weather == "晴天":
    print("今天是晴天！")
    if temperature > 30:
        print("天气很热，建议待在室内。")
    elif temperature > 20:
        print("天气很舒适，适合外出活动。")
    else:
        print("天气有点凉，记得添加衣物。")
else:
    print("今天不是晴天。")
    if weather == "雨天":
        print("记得带伞！")
    elif weather == "雪天":
        print("路面可能湿滑，小心行走。")
```

**运行结果：**

```
今天是晴天！
天气很舒适，适合外出活动。
```

## 2. 循环语句详解

### 2.1 for 循环基础

```python
# 遍历数字序列
print("使用range()函数：")
for i in range(5):
    print(f"第{i+1}次循环，i的值是{i}")

print("\n使用range(start, stop)：")
for i in range(2, 8):
    print(f"i = {i}")

print("\n使用range(start, stop, step)：")
for i in range(0, 10, 2):
    print(f"偶数：{i}")
```

**运行结果：**

```
使用range()函数：
第1次循环，i的值是0
第2次循环，i的值是1
第3次循环，i的值是2
第4次循环，i的值是3
第5次循环，i的值是4

使用range(start, stop)：
i = 2
i = 3
i = 4
i = 5
i = 6
i = 7

使用range(start, stop, step)：
偶数：0
偶数：2
偶数：4
偶数：6
偶数：8
```

### 2.2 遍历字符串和列表

```python
# 遍历字符串
name = "Python"
print("遍历字符串：")
for char in name:
    print(f"字符：{char}")

# 遍历列表
fruits = ["苹果", "香蕉", "橙子", "葡萄"]
print("\n遍历列表：")
for fruit in fruits:
    print(f"我喜欢吃{fruit}")

# 使用enumerate获取索引和值
print("\n使用enumerate：")
for index, fruit in enumerate(fruits):
    print(f"第{index+1}个水果是：{fruit}")
```

**运行结果：**

```
遍历字符串：
字符：P
字符：y
字符：t
字符：h
字符：o
字符：n

遍历列表：
我喜欢吃苹果
我喜欢吃香蕉
我喜欢吃橙子
我喜欢吃葡萄

使用enumerate：
第1个水果是：苹果
第2个水果是：香蕉
第3个水果是：橙子
第4个水果是：葡萄
```

### 2.3 while 循环基础

```python
# 基本while循环
count = 1
print("倒计时开始：")

while count <= 5:
    print(f"倒计时：{6-count}")
    count += 1

print("时间到！")

# 用户输入控制的while循环
print("\n输入'quit'退出程序：")
user_input = ""

while user_input.lower() != "quit":
    user_input = input("请输入内容（输入'quit'退出）：")
    if user_input.lower() != "quit":
        print(f"你输入了：{user_input}")

print("程序结束！")
```

### 2.4 嵌套循环

```python
# 嵌套循环 - 打印乘法表
print("九九乘法表：")
for i in range(1, 10):
    for j in range(1, i + 1):
        result = i * j
        print(f"{j}×{i}={result:2d}", end="  ")
    print()  # 换行

# 嵌套循环 - 打印图案
print("\n打印星号图案：")
for i in range(1, 6):
    for j in range(i):
        print("*", end="")
    print()  # 换行
```

**运行结果：**

```
九九乘法表：
1×1= 1
1×2= 2  2×2= 4
1×3= 3  2×3= 6  3×3= 9
1×4= 4  2×4= 8  3×4=12  4×4=16
1×5= 5  2×5=10  3×5=15  4×5=20  5×5=25
1×6= 6  2×6=12  3×6=18  4×6=24  5×6=30  6×6=36
1×7= 7  2×7=14  3×7=21  4×7=28  5×7=35  6×7=42  7×7=49
1×8= 8  2×8=16  3×8=24  4×8=32  5×8=40  6×8=48  7×8=56  8×8=64
1×9= 9  2×9=18  3×9=27  4×9=36  5×9=45  6×9=54  7×9=63  8×9=72  9×9=81

打印星号图案：
*
**
***
****
*****
```

## 3. 循环控制语句

### 3.1 break 语句

```python
# break语句 - 跳出循环
print("寻找第一个偶数：")
numbers = [1, 3, 7, 8, 9, 12, 15]

for num in numbers:
    print(f"检查数字：{num}")
    if num % 2 == 0:
        print(f"找到第一个偶数：{num}")
        break
else:
    print("没有找到偶数")

# break在嵌套循环中的使用
print("\n在嵌套循环中使用break：")
for i in range(3):
    print(f"外层循环：{i}")
    for j in range(5):
        if j == 3:
            print(f"  内层循环在j={j}时break")
            break
        print(f"  内层循环：{j}")
```

**运行结果：**

```
寻找第一个偶数：
检查数字：1
检查数字：3
检查数字：7
检查数字：8
找到第一个偶数：8

在嵌套循环中使用break：
外层循环：0
  内层循环：0
  内层循环：1
  内层循环：2
  内层循环在j=3时break
外层循环：1
  内层循环：0
  内层循环：1
  内层循环：2
  内层循环在j=3时break
外层循环：2
  内层循环：0
  内层循环：1
  内层循环：2
  内层循环在j=3时break
```

### 3.2 continue 语句

```python
# continue语句 - 跳过当前迭代
print("打印1-10中的奇数：")
for i in range(1, 11):
    if i % 2 == 0:  # 如果是偶数
        continue    # 跳过本次循环
    print(f"奇数：{i}")

# continue在while循环中的使用
print("\n处理用户输入（跳过空输入）：")
count = 0
max_inputs = 3

while count < max_inputs:
    user_input = input(f"请输入第{count+1}个内容：")

    if not user_input.strip():  # 如果输入为空
        print("输入不能为空，请重新输入")
        continue

    print(f"你输入了：{user_input}")
    count += 1

print("输入完成！")
```

### 3.3 pass 语句

```python
# pass语句 - 占位符
print("使用pass作为占位符：")

for i in range(5):
    if i < 3:
        pass  # 暂时什么都不做
    else:
        print(f"处理数字：{i}")

# 在函数定义中使用pass
def future_function():
    """这个函数将来会实现某些功能"""
    pass  # 暂时不实现

# 在类定义中使用pass
class FutureClass:
    """这个类将来会实现某些功能"""
    pass  # 暂时不实现
```

## 4. 实际应用示例

### 4.1 输入验证

```python
# 输入验证示例
def get_valid_age():
    """获取有效的年龄输入"""
    while True:
        try:
            age = int(input("请输入你的年龄："))
            if age < 0:
                print("年龄不能为负数，请重新输入")
                continue
            elif age > 150:
                print("年龄不能超过150岁，请重新输入")
                continue
            else:
                return age
        except ValueError:
            print("请输入有效的数字")

# 使用函数
user_age = get_valid_age()
print(f"你的年龄是：{user_age}岁")
```

### 4.2 菜单系统

```python
# 简单的菜单系统
def show_menu():
    """显示菜单选项"""
    print("\n=== 计算器菜单 ===")
    print("1. 加法")
    print("2. 减法")
    print("3. 乘法")
    print("4. 除法")
    print("5. 退出")
    print("==================")

def calculator():
    """简单计算器"""
    while True:
        show_menu()
        choice = input("请选择操作（1-5）：")

        if choice == "5":
            print("谢谢使用，再见！")
            break

        if choice not in ["1", "2", "3", "4"]:
            print("无效选择，请重新输入")
            continue

        try:
            num1 = float(input("请输入第一个数字："))
            num2 = float(input("请输入第二个数字："))
        except ValueError:
            print("请输入有效的数字")
            continue

        if choice == "1":
            result = num1 + num2
            operation = "加法"
        elif choice == "2":
            result = num1 - num2
            operation = "减法"
        elif choice == "3":
            result = num1 * num2
            operation = "乘法"
        elif choice == "4":
            if num2 == 0:
                print("错误：除数不能为零")
                continue
            result = num1 / num2
            operation = "除法"

        print(f"{operation}结果：{num1} {choice} {num2} = {result}")

# 运行计算器
# calculator()  # 取消注释来运行
```

## 5. 常见错误和注意事项

### 5.1 缩进错误

```python
# 错误示例：缩进不正确
# if True:
# print("这会导致缩进错误")  # IndentationError

# 正确示例：
if True:
    print("正确的缩进")
```

### 5.2 无限循环

```python
# 危险：无限循环示例（不要运行）
# while True:
#     print("这是无限循环")  # 永远不会停止

# 正确：有退出条件的循环
count = 0
while count < 5:
    print(f"计数：{count}")
    count += 1  # 重要：更新循环变量
```

### 5.3 条件判断的常见错误

```python
# 错误：使用赋值运算符而不是比较运算符
# if x = 5:  # SyntaxError
#     print("错误")

# 正确：使用比较运算符
x = 5
if x == 5:
    print("正确")

# 注意：浮点数比较
result = 0.1 + 0.2
print(f"0.1 + 0.2 = {result}")

# 错误的比较方式
if result == 0.3:
    print("相等")
else:
    print("不相等")  # 这会被执行

# 正确的浮点数比较方式
if abs(result - 0.3) < 1e-10:
    print("基本相等")
```

## 6. 性能优化建议

### 6.1 避免不必要的计算

```python
# 低效：在循环中重复计算
data = list(range(1000))
results = []

for item in data:
    if len(data) > 500:  # len(data)在每次循环中都被计算
        results.append(item * 2)

# 高效：将计算移到循环外
data = list(range(1000))
results = []
data_length = len(data)  # 只计算一次

for item in data:
    if data_length > 500:
        results.append(item * 2)
```

### 6.2 使用合适的循环类型

```python
# 当需要索引时，使用enumerate而不是range(len())
data = ["a", "b", "c", "d"]

# 低效
for i in range(len(data)):
    print(f"索引{i}: {data[i]}")

# 高效
for i, value in enumerate(data):
    print(f"索引{i}: {value}")
```

## 7. 总结

控制流程是编程的基础，通过本课的学习，你应该掌握：

1. **条件语句**：if、elif、else 的使用
2. **循环语句**：for 和 while 循环的应用场景
3. **循环控制**：break、continue、pass 的作用
4. **嵌套结构**：条件语句和循环的组合使用
5. **实际应用**：输入验证、菜单系统等常见模式

### 最佳实践

1. **保持代码简洁**：避免过深的嵌套
2. **使用有意义的变量名**：让代码更易读
3. **添加适当的注释**：解释复杂的逻辑
4. **考虑边界条件**：确保程序的健壮性
5. **避免无限循环**：总是确保循环有退出条件

### 下一步学习

掌握了控制流程后，你可以：

- 编写更复杂的程序逻辑
- 学习数据结构的操作
- 理解算法的基本概念
- 开始学习函数的定义和使用

继续加油，编程之路越来越精彩！ 🚀
