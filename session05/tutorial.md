# Session 05: 数据结构基础 - 详细教程

## 📖 课程概述

数据结构是编程的基础，选择合适的数据结构能让程序更高效、更易维护。Python提供了四种主要的内置数据结构：列表（List）、元组（Tuple）、字典（Dict）和集合（Set）。本课程将深入学习这些数据结构的特性、用法和应用场景。

## 🎯 学习路线图

```
数据结构基础
├── 列表 (List)
│   ├── 创建和访问
│   ├── 修改操作
│   ├── 常用方法
│   └── 列表推导式
├── 元组 (Tuple)
│   ├── 不可变特性
│   ├── 元组解包
│   └── 应用场景
├── 字典 (Dict)
│   ├── 键值对概念
│   ├── 字典操作
│   ├── 字典推导式
│   └── 嵌套字典
├── 集合 (Set)
│   ├── 唯一性特性
│   ├── 集合运算
│   └── 集合推导式
└── 综合应用
    ├── 数据结构选择
    ├── 性能考虑
    └── 实际项目应用
```

---

## 1. 列表 (List) 详解

### 1.1 列表基础

列表是Python中最灵活的数据结构，可以存储任意类型的数据。

```python
# 创建列表的多种方式
empty_list = []                    # 空列表
numbers = [1, 2, 3, 4, 5]         # 数字列表
names = ["Alice", "Bob", "Charlie"] # 字符串列表
mixed = [1, "hello", 3.14, True]   # 混合类型列表
nested = [[1, 2], [3, 4], [5, 6]]  # 嵌套列表

# 使用list()函数创建
from_string = list("hello")        # ['h', 'e', 'l', 'l', 'o']
from_range = list(range(5))        # [0, 1, 2, 3, 4]
```

### 1.2 列表访问和切片

```python
fruits = ["apple", "banana", "cherry", "date", "elderberry"]

# 索引访问（从0开始）
print(fruits[0])     # apple（第一个元素）
print(fruits[-1])    # elderberry（最后一个元素）
print(fruits[-2])    # date（倒数第二个元素）

# 切片操作 [start:end:step]
print(fruits[1:4])   # ['banana', 'cherry', 'date']
print(fruits[:3])    # ['apple', 'banana', 'cherry']
print(fruits[2:])    # ['cherry', 'date', 'elderberry']
print(fruits[::2])   # ['apple', 'cherry', 'elderberry']
print(fruits[::-1])  # 反转列表

# 检查元素是否存在
print("apple" in fruits)      # True
print("grape" not in fruits)  # True
```

### 1.3 列表修改操作

```python
scores = [85, 92, 78]

# 修改单个元素
scores[0] = 90
print(scores)  # [90, 92, 78]

# 添加元素
scores.append(88)           # 末尾添加: [90, 92, 78, 88]
scores.insert(1, 95)        # 指定位置插入: [90, 95, 92, 78, 88]
scores.extend([82, 87])     # 扩展列表: [90, 95, 92, 78, 88, 82, 87]

# 删除元素
scores.remove(78)           # 删除第一个78
popped = scores.pop()       # 删除并返回最后一个元素
popped_index = scores.pop(1) # 删除并返回指定索引的元素
del scores[0]               # 删除指定索引的元素

# 清空列表
scores.clear()              # 清空所有元素
```

### 1.4 列表常用方法

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

# 查找和计数
print(numbers.index(4))     # 2（元素4的索引）
print(numbers.count(1))     # 2（元素1出现的次数）

# 排序
numbers.sort()              # 原地排序（修改原列表）
print(numbers)              # [1, 1, 2, 3, 4, 5, 6, 9]

numbers.sort(reverse=True)  # 降序排序
print(numbers)              # [9, 6, 5, 4, 3, 2, 1, 1]

# 不修改原列表的排序
original = [3, 1, 4, 1, 5]
sorted_list = sorted(original)  # 返回新的排序列表
print(original)             # [3, 1, 4, 1, 5]（未改变）
print(sorted_list)          # [1, 1, 3, 4, 5]

# 反转
numbers.reverse()           # 原地反转
reversed_list = list(reversed(original))  # 返回新的反转列表

# 复制列表
copy1 = numbers.copy()      # 浅拷贝
copy2 = numbers[:]          # 切片拷贝
copy3 = list(numbers)       # 构造函数拷贝
```

### 1.5 列表推导式

列表推导式是创建列表的简洁方式：

```python
# 基本语法：[expression for item in iterable]
squares = [x**2 for x in range(10)]
print(squares)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# 带条件的列表推导式
even_squares = [x**2 for x in range(10) if x % 2 == 0]
print(even_squares)  # [0, 4, 16, 36, 64]

# 字符串处理
words = ["hello", "world", "python"]
upper_words = [word.upper() for word in words]
print(upper_words)  # ['HELLO', 'WORLD', 'PYTHON']

# 嵌套列表推导式
matrix = [[i*j for j in range(3)] for i in range(3)]
print(matrix)  # [[0, 0, 0], [0, 1, 2], [0, 2, 4]]

# 条件表达式
result = [x if x > 0 else 0 for x in [-1, 2, -3, 4]]
print(result)  # [0, 2, 0, 4]
```

---

## 2. 元组 (Tuple) 详解

### 2.1 元组基础

元组是不可变的有序集合，一旦创建就不能修改。

```python
# 创建元组
empty_tuple = ()                    # 空元组
single_tuple = (42,)                # 单元素元组（注意逗号）
coordinates = (10, 20)              # 坐标点
colors = ("red", "green", "blue")   # 颜色元组
mixed_tuple = (1, "hello", 3.14)    # 混合类型

# 不使用括号也可以创建元组
point = 3, 4
print(type(point))  # <class 'tuple'>

# 使用tuple()函数
from_list = tuple([1, 2, 3])        # (1, 2, 3)
from_string = tuple("abc")          # ('a', 'b', 'c')
```

### 2.2 元组操作

```python
rgb = (255, 128, 0)

# 访问元素（与列表相同）
print(rgb[0])       # 255
print(rgb[-1])      # 0

# 切片操作
print(rgb[1:])      # (128, 0)

# 元组不能修改
# rgb[0] = 200      # 这会报错！TypeError

# 但可以重新赋值
rgb = (200, 128, 0)

# 元组连接
tuple1 = (1, 2)
tuple2 = (3, 4)
combined = tuple1 + tuple2  # (1, 2, 3, 4)

# 元组重复
repeated = ("ha",) * 3      # ('ha', 'ha', 'ha')

# 元组方法（只有两个）
numbers = (1, 2, 3, 2, 4, 2)
print(numbers.count(2))     # 3
print(numbers.index(3))     # 2
```

### 2.3 元组解包

元组解包是Python的强大特性：

```python
# 基本解包
point = (3, 4)
x, y = point
print(f"x={x}, y={y}")  # x=3, y=4

# 多个值的解包
student_info = ("张三", 20, "计算机科学")
name, age, major = student_info

# 交换变量（利用元组解包）
a, b = 10, 20
a, b = b, a  # 交换a和b的值
print(f"a={a}, b={b}")  # a=20, b=10

# 函数返回多个值
def get_name_age():
    return "李四", 25

name, age = get_name_age()

# 星号表达式（Python 3+）
numbers = (1, 2, 3, 4, 5)
first, *middle, last = numbers
print(first)   # 1
print(middle)  # [2, 3, 4]
print(last)    # 5

# 忽略不需要的值
data = ("张三", 20, "计算机科学", "大二")
name, age, *_ = data  # 忽略后面的值
```

### 2.4 元组的应用场景

```python
# 1. 坐标和点
points = [(0, 0), (1, 1), (2, 4), (3, 9)]

# 2. 数据库记录
student_records = [
    (1, "张三", "计算机科学", 85),
    (2, "李四", "数学", 92),
    (3, "王五", "物理", 78)
]

# 3. 函数参数
def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return ((x2-x1)**2 + (y2-y1)**2)**0.5

distance = calculate_distance((0, 0), (3, 4))  # 5.0

# 4. 字典的键（因为元组不可变）
locations = {
    (0, 0): "原点",
    (1, 1): "点A",
    (2, 3): "点B"
}
```

---

## 3. 字典 (Dict) 详解

### 3.1 字典基础

字典存储键值对，通过键快速访问值。

```python
# 创建字典的多种方式
empty_dict = {}                     # 空字典
student = {
    "name": "张三",
    "age": 20,
    "major": "计算机科学",
    "scores": [85, 92, 78]
}

# 使用dict()函数
from_pairs = dict([("a", 1), ("b", 2)])  # {'a': 1, 'b': 2}
from_keywords = dict(name="李四", age=25)   # {'name': '李四', 'age': 25}

# 字典推导式
squares_dict = {x: x**2 for x in range(5)}  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

### 3.2 字典访问和修改

```python
student = {"name": "张三", "age": 20, "major": "计算机科学"}

# 访问值
print(student["name"])          # 张三
print(student.get("age"))       # 20
print(student.get("grade", "未知"))  # 未知（默认值）

# 修改和添加
student["age"] = 21             # 修改现有键
student["grade"] = "大二"        # 添加新键值对

# 删除键值对
del student["major"]            # 删除键值对
age = student.pop("age")        # 删除并返回值
grade = student.pop("grade", "未知")  # 删除并返回值（带默认值）

# 清空字典
student.clear()
```

### 3.3 字典方法和操作

```python
scores = {"数学": 85, "英语": 92, "物理": 78, "化学": 88}

# 获取键、值、键值对
print(scores.keys())    # dict_keys(['数学', '英语', '物理', '化学'])
print(scores.values())  # dict_values([85, 92, 78, 88])
print(scores.items())   # dict_items([('数学', 85), ('英语', 92), ...])

# 遍历字典
for subject in scores:                    # 遍历键
    print(f"{subject}: {scores[subject]}")

for subject, score in scores.items():    # 遍历键值对
    print(f"{subject}: {score}")

for score in scores.values():            # 遍历值
    print(score)

# 字典合并
more_scores = {"生物": 90, "历史": 85}
scores.update(more_scores)               # 更新字典

# Python 3.9+ 字典合并操作符
# all_scores = scores | more_scores      # 合并（不修改原字典）
# scores |= more_scores                  # 原地合并

# 检查键是否存在
if "数学" in scores:
    print(f"数学成绩: {scores['数学']}")

# 获取所有键的列表
subjects = list(scores.keys())
```

### 3.4 嵌套字典

```python
# 学生信息系统
students = {
    "S001": {
        "name": "张三",
        "age": 20,
        "scores": {"数学": 85, "英语": 92, "物理": 78}
    },
    "S002": {
        "name": "李四",
        "age": 19,
        "scores": {"数学": 90, "英语": 88, "物理": 85}
    }
}

# 访问嵌套数据
print(students["S001"]["name"])                    # 张三
print(students["S001"]["scores"]["数学"])           # 85

# 安全访问嵌套数据
math_score = students.get("S001", {}).get("scores", {}).get("数学", 0)

# 修改嵌套数据
students["S001"]["scores"]["化学"] = 88
students["S003"] = {
    "name": "王五",
    "age": 21,
    "scores": {"数学": 78, "英语": 85}
}
```

### 3.5 字典推导式

```python
# 基本字典推导式
squares = {x: x**2 for x in range(5)}
print(squares)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# 带条件的字典推导式
even_squares = {x: x**2 for x in range(10) if x % 2 == 0}
print(even_squares)  # {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}

# 从列表创建字典
words = ["apple", "banana", "cherry"]
word_lengths = {word: len(word) for word in words}
print(word_lengths)  # {'apple': 5, 'banana': 6, 'cherry': 6}

# 字典键值互换
original = {"a": 1, "b": 2, "c": 3}
swapped = {v: k for k, v in original.items()}
print(swapped)  # {1: 'a', 2: 'b', 3: 'c'}

# 过滤字典
scores = {"张三": 85, "李四": 92, "王五": 78, "赵六": 88}
high_scores = {name: score for name, score in scores.items() if score >= 85}
print(high_scores)  # {'张三': 85, '李四': 92, '赵六': 88}
```

---

## 4. 集合 (Set) 详解

### 4.1 集合基础

集合是无序的唯一元素集合，自动去重。

```python
# 创建集合
empty_set = set()                   # 空集合（不能用{}）
fruits = {"apple", "banana", "cherry"}
numbers = {1, 2, 3, 4, 5}

# 从列表创建集合（自动去重）
list_with_duplicates = [1, 2, 2, 3, 3, 3, 4]
unique_numbers = set(list_with_duplicates)  # {1, 2, 3, 4}

# 从字符串创建集合
letters = set("hello")              # {'h', 'e', 'l', 'o'}

# 集合推导式
even_squares = {x**2 for x in range(10) if x % 2 == 0}
print(even_squares)  # {0, 4, 16, 36, 64}
```

### 4.2 集合操作

```python
fruits = {"apple", "banana", "cherry"}

# 添加元素
fruits.add("date")                  # 添加单个元素
fruits.update(["elderberry", "fig"]) # 添加多个元素
fruits.update({"grape", "kiwi"})     # 从其他集合添加

# 删除元素
fruits.remove("banana")             # 删除元素（不存在会报错）
fruits.discard("orange")            # 删除元素（不存在不报错）
popped = fruits.pop()               # 删除并返回任意元素

# 清空集合
fruits.clear()

# 检查元素
if "apple" in fruits:
    print("找到苹果")

# 集合长度
print(len(fruits))
```

### 4.3 集合运算

```python
set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}
set3 = {1, 2, 3}

# 并集（所有元素）
union1 = set1 | set2                # {1, 2, 3, 4, 5, 6, 7, 8}
union2 = set1.union(set2)           # 同上

# 交集（共同元素）
intersection1 = set1 & set2         # {4, 5}
intersection2 = set1.intersection(set2)  # 同上

# 差集（在set1中但不在set2中）
difference1 = set1 - set2           # {1, 2, 3}
difference2 = set1.difference(set2) # 同上

# 对称差集（不在交集中的元素）
sym_diff1 = set1 ^ set2             # {1, 2, 3, 6, 7, 8}
sym_diff2 = set1.symmetric_difference(set2)  # 同上

# 子集和超集
print(set3.issubset(set1))          # True（set3是set1的子集）
print(set1.issuperset(set3))        # True（set1是set3的超集）
print(set1.isdisjoint(set2))        # False（有交集）

# 原地运算（修改原集合）
set1 |= set2    # set1 = set1 | set2
set1 &= set2    # set1 = set1 & set2
set1 -= set2    # set1 = set1 - set2
set1 ^= set2    # set1 = set1 ^ set2
```

### 4.4 集合的实际应用

```python
# 1. 去重
def remove_duplicates(items):
    return list(set(items))

original = [1, 2, 2, 3, 3, 3, 4]
unique = remove_duplicates(original)  # [1, 2, 3, 4]

# 2. 查找共同兴趣
alice_hobbies = {"读书", "游泳", "编程", "音乐"}
bob_hobbies = {"游泳", "编程", "电影", "旅行"}
common_hobbies = alice_hobbies & bob_hobbies  # {'游泳', '编程'}

# 3. 权限管理
user_permissions = {"read", "write"}
required_permissions = {"read", "write", "execute"}
has_all_permissions = required_permissions.issubset(user_permissions)  # False
missing_permissions = required_permissions - user_permissions  # {'execute'}

# 4. 数据验证
def validate_data(data, valid_values):
    data_set = set(data)
    valid_set = set(valid_values)
    invalid_items = data_set - valid_set
    return len(invalid_items) == 0, invalid_items

data = ["red", "green", "blue", "yellow"]
valid_colors = ["red", "green", "blue"]
is_valid, invalid = validate_data(data, valid_colors)
print(f"数据有效: {is_valid}, 无效项: {invalid}")  # 数据有效: False, 无效项: {'yellow'}
```

---

## 5. 数据结构选择指南

### 5.1 选择决策树

```
需要存储数据？
├── 需要键值对映射？ → 字典 (Dict)
├── 需要唯一元素？ → 集合 (Set)
├── 数据不会改变？ → 元组 (Tuple)
└── 需要有序可变集合？ → 列表 (List)
```

### 5.2 性能对比

| 操作 | 列表 | 元组 | 字典 | 集合 |
|------|------|------|------|------|
| 访问元素 | O(1) | O(1) | O(1) | - |
| 查找元素 | O(n) | O(n) | O(1) | O(1) |
| 插入元素 | O(1)* | - | O(1) | O(1) |
| 删除元素 | O(n) | - | O(1) | O(1) |
| 内存使用 | 中等 | 最少 | 最多 | 中等 |

*列表末尾插入是O(1)，中间插入是O(n)

### 5.3 使用场景总结

```python
# 列表：有序、可变、允许重复
use_list_when = [
    "需要保持元素顺序",
    "需要通过索引访问",
    "需要修改数据",
    "允许重复元素",
    "需要排序功能"
]

# 元组：有序、不可变、允许重复
use_tuple_when = [
    "数据不会改变",
    "作为字典的键",
    "函数返回多个值",
    "坐标、配置等固定数据"
]

# 字典：键值对、可变、键唯一
use_dict_when = [
    "需要快速查找",
    "键值对映射",
    "配置信息",
    "缓存数据",
    "计数统计"
]

# 集合：无序、可变、元素唯一
use_set_when = [
    "需要去重",
    "集合运算",
    "成员测试",
    "权限管理"
]
```

---

## 6. 综合实例：学生成绩管理系统

让我们通过一个完整的例子来综合运用所学的数据结构：

```python
class StudentGradeManager:
    def __init__(self):
        # 使用字典存储学生信息，键为学号
        self.students = {}
        # 使用集合存储所有科目
        self.subjects = set()
    
    def add_student(self, student_id, name, age):
        """添加学生"""
        if student_id in self.students:
            print(f"学号 {student_id} 已存在")
            return False
        
        self.students[student_id] = {
            "name": name,
            "age": age,
            "scores": {}  # 使用字典存储各科成绩
        }
        print(f"成功添加学生：{name}")
        return True
    
    def add_score(self, student_id, subject, score):
        """添加成绩"""
        if student_id not in self.students:
            print(f"学号 {student_id} 不存在")
            return False
        
        if not 0 <= score <= 100:
            print("成绩必须在0-100之间")
            return False
        
        self.students[student_id]["scores"][subject] = score
        self.subjects.add(subject)  # 自动添加到科目集合
        print(f"成功添加成绩：{subject} = {score}")
        return True
    
    def get_student_average(self, student_id):
        """计算学生平均分"""
        if student_id not in self.students:
            return None
        
        scores = list(self.students[student_id]["scores"].values())
        if not scores:
            return 0
        
        return sum(scores) / len(scores)
    
    def get_subject_average(self, subject):
        """计算科目平均分"""
        scores = []
        for student in self.students.values():
            if subject in student["scores"]:
                scores.append(student["scores"][subject])
        
        if not scores:
            return None
        
        return sum(scores) / len(scores)
    
    def get_top_students(self, n=3):
        """获取成绩前N名的学生"""
        # 创建包含学生ID和平均分的元组列表
        student_averages = []
        for student_id, info in self.students.items():
            avg = self.get_student_average(student_id)
            if avg is not None:
                student_averages.append((student_id, info["name"], avg))
        
        # 按平均分降序排序
        student_averages.sort(key=lambda x: x[2], reverse=True)
        
        # 返回前N名
        return student_averages[:n]
    
    def get_failing_students(self, passing_score=60):
        """获取不及格的学生"""
        failing_students = []
        
        for student_id, info in self.students.items():
            scores = list(info["scores"].values())
            if scores:  # 如果有成绩
                min_score = min(scores)
                if min_score < passing_score:
                    failing_students.append({
                        "id": student_id,
                        "name": info["name"],
                        "min_score": min_score,
                        "average": self.get_student_average(student_id)
                    })
        
        return failing_students
    
    def generate_report(self):
        """生成统计报告"""
        print("\n=== 学生成绩统计报告 ===")
        print(f"总学生数：{len(self.students)}")
        print(f"总科目数：{len(self.subjects)}")
        print(f"科目列表：{', '.join(sorted(self.subjects))}")
        
        print("\n--- 各科平均分 ---")
        for subject in sorted(self.subjects):
            avg = self.get_subject_average(subject)
            print(f"{subject}: {avg:.2f}")
        
        print("\n--- 成绩前3名 ---")
        top_students = self.get_top_students(3)
        for i, (student_id, name, avg) in enumerate(top_students, 1):
            print(f"{i}. {name} ({student_id}): {avg:.2f}")
        
        print("\n--- 不及格学生 ---")
        failing = self.get_failing_students()
        if failing:
            for student in failing:
                print(f"{student['name']} ({student['id']}): "
                      f"最低分 {student['min_score']}, "
                      f"平均分 {student['average']:.2f}")
        else:
            print("没有不及格的学生")

# 使用示例
if __name__ == "__main__":
    # 创建管理器
    manager = StudentGradeManager()
    
    # 添加学生
    manager.add_student("S001", "张三", 20)
    manager.add_student("S002", "李四", 19)
    manager.add_student("S003", "王五", 21)
    
    # 添加成绩
    manager.add_score("S001", "数学", 85)
    manager.add_score("S001", "英语", 92)
    manager.add_score("S001", "物理", 78)
    
    manager.add_score("S002", "数学", 90)
    manager.add_score("S002", "英语", 88)
    manager.add_score("S002", "物理", 85)
    
    manager.add_score("S003", "数学", 75)
    manager.add_score("S003", "英语", 80)
    manager.add_score("S003", "物理", 55)  # 不及格
    
    # 生成报告
    manager.generate_report()
```

---

## 7. 最佳实践和注意事项

### 7.1 性能优化建议

```python
# 1. 列表预分配（如果知道大小）
# 好的做法
big_list = [0] * 1000000  # 预分配
for i in range(1000000):
    big_list[i] = i * 2

# 避免的做法
# big_list = []
# for i in range(1000000):
#     big_list.append(i * 2)  # 频繁扩容

# 2. 使用集合进行成员测试
valid_ids = {"S001", "S002", "S003"}  # 集合
# valid_ids = ["S001", "S002", "S003"]  # 列表（慢）

if "S001" in valid_ids:  # O(1) vs O(n)
    print("有效ID")

# 3. 字典的get()方法
student = {"name": "张三", "age": 20}

# 好的做法
grade = student.get("grade", "未知")

# 避免的做法
# if "grade" in student:
#     grade = student["grade"]
# else:
#     grade = "未知"
```

### 7.2 常见陷阱

```python
# 1. 可变对象作为默认参数
# 错误的做法
def add_student_wrong(name, scores=[]):
    scores.append(85)  # 所有调用共享同一个列表！
    return {"name": name, "scores": scores}

# 正确的做法
def add_student_correct(name, scores=None):
    if scores is None:
        scores = []
    scores.append(85)
    return {"name": name, "scores": scores}

# 2. 浅拷贝 vs 深拷贝
import copy

original = {"scores": [85, 92, 78]}
shallow = original.copy()           # 浅拷贝
deep = copy.deepcopy(original)      # 深拷贝

original["scores"].append(88)
print(shallow["scores"])   # [85, 92, 78, 88] - 受影响
print(deep["scores"])      # [85, 92, 78] - 不受影响

# 3. 字典键的类型
# 只有不可变类型可以作为字典键
valid_keys = {
    "string": "可以",
    42: "可以",
    (1, 2): "可以",
    # [1, 2]: "不可以"  # 列表不能作为键
}
```

### 7.3 代码风格建议

```python
# 1. 使用有意义的变量名
# 好的做法
student_scores = {"数学": 85, "英语": 92}
for subject, score in student_scores.items():
    print(f"{subject}: {score}")

# 避免的做法
# d = {"数学": 85, "英语": 92}
# for k, v in d.items():
#     print(f"{k}: {v}")

# 2. 适当使用推导式
# 简单情况使用推导式
squares = [x**2 for x in range(10)]

# 复杂情况使用普通循环
complex_result = []
for x in range(10):
    if x % 2 == 0:
        result = x**2
        if result > 10:
            complex_result.append(result)
    else:
        complex_result.append(0)

# 3. 合理使用数据结构
# 根据使用场景选择合适的数据结构
user_permissions = set(["read", "write"])    # 权限检查
user_history = ["login", "view", "edit"]     # 操作历史
user_profile = {"name": "张三", "age": 25}    # 用户信息
user_location = (39.9042, 116.4074)         # 坐标（不变）
```

---

## 8. 总结

通过本课程的学习，我们深入了解了Python的四种主要数据结构：

1. **列表（List）**：有序、可变、允许重复，适合存储序列数据
2. **元组（Tuple）**：有序、不可变、允许重复，适合存储固定数据
3. **字典（Dict）**：键值对映射、可变、键唯一，适合快速查找
4. **集合（Set）**：无序、可变、元素唯一，适合去重和集合运算

### 关键要点

- 根据数据特性和使用场景选择合适的数据结构
- 理解每种数据结构的时间复杂度
- 掌握推导式的使用，提高代码简洁性
- 注意可变对象的陷阱，正确处理拷贝问题
- 遵循Python编码规范，编写可读性强的代码

### 下一步学习

- Session 06: 函数编程 - 学习如何将数据结构与函数结合
- 深入学习算法和数据结构
- 了解更多Python标准库中的数据结构（如collections模块）

数据结构是编程的基础，熟练掌握它们将为后续的学习打下坚实的基础。继续练习，在实际项目中应用所学知识！