# Session 05: 数据结构基础

## 📚 学习目标

通过本节课的学习，你将掌握：

- **列表（List）**：掌握列表的创建、访问、修改和常用方法
- **元组（Tuple）**：理解元组的特点和使用场景
- **字典（Dict）**：学会使用字典存储键值对数据
- **集合（Set）**：掌握集合的特性和集合运算
- **数据结构选择**：学会根据需求选择合适的数据结构
- **实际应用**：通过学生成绩管理系统巩固所学知识

## 🎯 核心概念

### 1. 列表 (List)

列表是Python中最常用的数据结构，可以存储多个有序的元素：

```python
# 创建列表
students = ["张三", "李四", "王五"]
scores = [85, 92, 78, 96]
mixed_list = ["Python", 3.8, True, [1, 2, 3]]

# 访问元素
print(students[0])    # 张三
print(scores[-1])     # 96（最后一个元素）

# 修改元素
students[0] = "张小三"
scores.append(88)     # 添加元素
```

### 2. 元组 (Tuple)

元组类似列表，但创建后不能修改（不可变）：

```python
# 创建元组
coordinates = (10, 20)
colors = ("red", "green", "blue")
single_item = (42,)  # 单元素元组需要逗号

# 访问元素
print(coordinates[0])  # 10
print(colors[1])       # green
```

### 3. 字典 (Dict)

字典存储键值对，通过键来访问值：

```python
# 创建字典
student_info = {
    "name": "张三",
    "age": 20,
    "major": "计算机科学",
    "scores": [85, 92, 78]
}

# 访问和修改
print(student_info["name"])     # 张三
student_info["age"] = 21        # 修改值
student_info["grade"] = "大二"   # 添加新键值对
```

### 4. 集合 (Set)

集合存储唯一元素，自动去重：

```python
# 创建集合
fruits = {"apple", "banana", "orange"}
numbers = set([1, 2, 3, 2, 1])  # {1, 2, 3}

# 集合运算
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}
print(set1 & set2)  # 交集: {3, 4}
print(set1 | set2)  # 并集: {1, 2, 3, 4, 5, 6}
```

## 📊 数据结构对比

| 数据结构 | 有序 | 可变 | 允许重复 | 主要用途 |
|----------|------|------|----------|----------|
| 列表 List | ✅ | ✅ | ✅ | 存储有序的可变数据 |
| 元组 Tuple | ✅ | ❌ | ✅ | 存储不变的有序数据 |
| 字典 Dict | ✅* | ✅ | 键唯一 | 键值对映射 |
| 集合 Set | ❌ | ✅ | ❌ | 去重、集合运算 |

*Python 3.7+字典保持插入顺序

## 🎮 演示项目

**学生成绩管理系统**
- 使用字典存储学生信息
- 使用列表管理多个学生
- 实现成绩录入、查询、统计功能
- 支持成绩排序和筛选

## 📋 前置知识

- Session 01: 环境搭建与Hello World
- Session 02: 变量与数据类型
- Session 03: 运算符与表达式
- Session 04: 控制流程

## ⏰ 学习时间

预计学习时间：**3-4小时**
- 理论学习：1小时
- 代码实践：1.5小时
- 项目开发：1-1.5小时

## 📁 文件说明

- `tutorial.md` - 详细教程文档
- `demo.py` - 主要演示代码
- `examples/` - 分类示例代码
  - `example1.py` - 列表操作示例
  - `example2.py` - 元组和字典示例
  - `example3.py` - 集合操作示例
- `exercises/` - 练习题目录
  - `exercise1.py` - 列表基础练习
  - `exercise2.py` - 字典应用练习
  - `exercise3.py` - 综合数据结构练习
  - `solutions/` - 练习答案
- `project/` - 学生成绩管理系统
  - `main.py` - 项目主文件
  - `student_manager.py` - 学生管理模块
  - `grade_calculator.py` - 成绩计算模块
  - `data_handler.py` - 数据处理模块
- `assets/` - 资源文件
  - `sample_data.py` - 示例数据

## 🚀 快速开始

```bash
# 进入session05目录
cd session05

# 运行演示代码
uv run python demo.py

# 运行示例代码
uv run python examples/example1.py

# 运行项目
uv run python project/main.py
```

## 💡 学习建议

1. **理解特性**：重点理解每种数据结构的特性和适用场景
2. **多练习**：通过大量练习熟悉各种操作方法
3. **对比学习**：对比不同数据结构的优缺点
4. **实际应用**：在项目中实践使用不同数据结构
5. **性能考虑**：了解不同操作的时间复杂度

## 🔗 相关资源

- [Python官方文档 - 数据结构](https://docs.python.org/3/tutorial/datastructures.html)
- [Python列表方法详解](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists)
- [Python字典操作指南](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)

---

**准备好探索Python的数据结构世界了吗？让我们开始吧！** 🎯