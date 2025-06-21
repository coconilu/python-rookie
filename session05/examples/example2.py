#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session05 示例2: 元组和字典操作详解

本文件详细演示元组和字典的各种操作方法，包括：
- 元组的创建和特性
- 元组解包和应用
- 字典的创建和操作
- 字典的高级用法
- 嵌套数据结构
- 实际应用场景

作者: Python教程团队
创建日期: 2024-12-21
"""

from typing import Dict, Tuple, List, Any
import json
from collections import defaultdict, Counter


def demo_tuple_basics():
    """
    演示元组的基础操作
    """
    print("📦 元组基础操作演示")
    print("=" * 30)
    
    # 1. 创建元组
    print("1. 创建元组:")
    empty_tuple = ()
    single_tuple = (42,)  # 注意逗号
    coordinates = (10, 20)
    colors = ("red", "green", "blue")
    mixed = ("Python", 3.8, True, [1, 2, 3])
    
    print(f"空元组: {empty_tuple}, 类型: {type(empty_tuple)}")
    print(f"单元素元组: {single_tuple}, 类型: {type(single_tuple)}")
    print(f"坐标元组: {coordinates}")
    print(f"颜色元组: {colors}")
    print(f"混合元组: {mixed}")
    
    # 不使用括号也可以创建元组
    point = 3, 4
    print(f"不用括号: {point}, 类型: {type(point)}")
    
    # 2. 元组的不可变性
    print(f"\n2. 元组的不可变性:")
    try:
        coordinates[0] = 15  # 这会报错
    except TypeError as e:
        print(f"尝试修改元组元素: {e}")
    
    # 但可以重新赋值整个元组
    coordinates = (15, 25)
    print(f"重新赋值后: {coordinates}")
    
    # 3. 元组方法（只有两个）
    print(f"\n3. 元组方法:")
    numbers = (1, 2, 3, 2, 4, 2, 5)
    print(f"数字元组: {numbers}")
    print(f"count(2): {numbers.count(2)}")
    print(f"index(3): {numbers.index(3)}")
    
    # 4. 元组操作
    print(f"\n4. 元组操作:")
    tuple1 = (1, 2, 3)
    tuple2 = (4, 5, 6)
    
    # 连接
    combined = tuple1 + tuple2
    print(f"连接: {tuple1} + {tuple2} = {combined}")
    
    # 重复
    repeated = ("ha",) * 3
    print(f"重复: ('ha',) * 3 = {repeated}")
    
    # 切片
    print(f"切片: {numbers[1:4]}")
    
    # 成员测试
    print(f"成员测试: 2 in numbers = {2 in numbers}")


def demo_tuple_unpacking():
    """
    演示元组解包的各种用法
    """
    print("\n🔓 元组解包演示")
    print("=" * 30)
    
    # 1. 基本解包
    print("1. 基本解包:")
    point = (3, 4)
    x, y = point
    print(f"坐标点 {point} 解包为: x={x}, y={y}")
    
    # 2. 多变量赋值
    print(f"\n2. 多变量赋值:")
    name, age, city = "张三", 25, "北京"
    print(f"姓名: {name}, 年龄: {age}, 城市: {city}")
    
    # 3. 变量交换
    print(f"\n3. 变量交换:")
    a, b = 10, 20
    print(f"交换前: a={a}, b={b}")
    a, b = b, a
    print(f"交换后: a={a}, b={b}")
    
    # 4. 函数返回多个值
    print(f"\n4. 函数返回多个值:")
    
    def get_student_info():
        return "李四", 22, "计算机科学", 85.5
    
    student_name, student_age, major, gpa = get_student_info()
    print(f"学生信息: {student_name}, {student_age}岁, {major}, GPA: {gpa}")
    
    # 5. 星号表达式（Python 3+）
    print(f"\n5. 星号表达式:")
    numbers = (1, 2, 3, 4, 5, 6)
    first, *middle, last = numbers
    print(f"数字序列: {numbers}")
    print(f"第一个: {first}, 中间: {middle}, 最后: {last}")
    
    # 忽略不需要的值
    data = ("王五", 20, "数学", "大二", 3.8)
    name, age, *_, gpa = data
    print(f"只要姓名、年龄和GPA: {name}, {age}, {gpa}")
    
    # 6. 嵌套解包
    print(f"\n6. 嵌套解包:")
    nested_data = ((1, 2), (3, 4), (5, 6))
    (a, b), (c, d), (e, f) = nested_data
    print(f"嵌套数据: {nested_data}")
    print(f"解包结果: a={a}, b={b}, c={c}, d={d}, e={e}, f={f}")


def demo_tuple_applications():
    """
    演示元组的实际应用场景
    """
    print("\n🎯 元组应用场景演示")
    print("=" * 30)
    
    # 1. 坐标和几何
    print("1. 坐标和几何:")
    points = [(0, 0), (1, 1), (2, 4), (3, 9)]
    print(f"点集合: {points}")
    
    def calculate_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        x1, y1 = point1
        x2, y2 = point2
        return ((x2-x1)**2 + (y2-y1)**2)**0.5
    
    distance = calculate_distance((0, 0), (3, 4))
    print(f"(0,0) 到 (3,4) 的距离: {distance}")
    
    # 2. 数据库记录
    print(f"\n2. 数据库记录:")
    student_records = [
        (1, "张三", "计算机科学", 85, "2023-09-01"),
        (2, "李四", "数学", 92, "2023-09-01"),
        (3, "王五", "物理", 78, "2023-09-01")
    ]
    
    print("学生记录:")
    for record in student_records:
        student_id, name, major, score, enrollment_date = record
        print(f"  ID: {student_id}, 姓名: {name}, 专业: {major}, 成绩: {score}")
    
    # 3. 配置和常量
    print(f"\n3. 配置和常量:")
    # 颜色常量
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    
    # 窗口配置
    WINDOW_CONFIG = (800, 600, "Python应用", True)
    width, height, title, resizable = WINDOW_CONFIG
    
    print(f"红色RGB: {RED}")
    print(f"窗口配置: 宽度={width}, 高度={height}, 标题={title}, 可调整={resizable}")
    
    # 4. 字典的键
    print(f"\n4. 作为字典的键:")
    locations = {
        (0, 0): "原点",
        (1, 1): "点A",
        (2, 3): "点B",
        (-1, -1): "点C"
    }
    
    print("位置字典:")
    for coord, name in locations.items():
        print(f"  {coord}: {name}")
    
    # 查找特定位置
    target = (1, 1)
    if target in locations:
        print(f"位置 {target} 是: {locations[target]}")
    
    # 5. 枚举和命名
    print(f"\n5. 枚举和命名:")
    
    # 使用namedtuple创建命名元组
    from collections import namedtuple
    
    Student = namedtuple('Student', ['name', 'age', 'major', 'gpa'])
    Point = namedtuple('Point', ['x', 'y'])
    
    student = Student("赵六", 21, "物理", 3.7)
    point = Point(10, 20)
    
    print(f"命名元组学生: {student}")
    print(f"访问属性: {student.name}, {student.age}, {student.gpa}")
    print(f"命名元组点: {point}")
    print(f"访问坐标: x={point.x}, y={point.y}")


def demo_dict_basics():
    """
    演示字典的基础操作
    """
    print("\n📚 字典基础操作演示")
    print("=" * 30)
    
    # 1. 创建字典
    print("1. 创建字典:")
    empty_dict = {}
    student = {
        "name": "张三",
        "age": 20,
        "major": "计算机科学",
        "scores": [85, 92, 78]
    }
    
    # 使用dict()函数
    from_pairs = dict([("a", 1), ("b", 2), ("c", 3)])
    from_keywords = dict(name="李四", age=25, city="上海")
    
    print(f"空字典: {empty_dict}")
    print(f"学生字典: {student}")
    print(f"从键值对创建: {from_pairs}")
    print(f"从关键字创建: {from_keywords}")
    
    # 2. 访问字典值
    print(f"\n2. 访问字典值:")
    print(f"学生姓名: {student['name']}")
    print(f"学生年龄: {student.get('age')}")
    print(f"学生年级: {student.get('grade', '未知')}")
    
    # 安全访问嵌套值
    print(f"第一门课成绩: {student['scores'][0]}")
    
    # 3. 修改字典
    print(f"\n3. 修改字典:")
    student["age"] = 21  # 修改现有键
    student["grade"] = "大二"  # 添加新键
    student["scores"].append(88)  # 修改嵌套列表
    
    print(f"修改后: {student}")
    
    # 4. 删除操作
    print(f"\n4. 删除操作:")
    student_copy = student.copy()
    
    # 不同的删除方法
    del student_copy["grade"]  # 删除键值对
    age = student_copy.pop("age")  # 删除并返回值
    major = student_copy.pop("department", "未知")  # 删除不存在的键
    
    print(f"删除grade后: {student_copy}")
    print(f"pop age返回: {age}")
    print(f"pop不存在的键返回: {major}")


def demo_dict_methods():
    """
    演示字典的方法和操作
    """
    print("\n🛠️ 字典方法演示")
    print("=" * 30)
    
    scores = {"数学": 85, "英语": 92, "物理": 78, "化学": 88}
    print(f"成绩字典: {scores}")
    
    # 1. 获取键、值、键值对
    print(f"\n1. 获取键、值、键值对:")
    print(f"所有键: {list(scores.keys())}")
    print(f"所有值: {list(scores.values())}")
    print(f"所有键值对: {list(scores.items())}")
    
    # 2. 遍历字典
    print(f"\n2. 遍历字典:")
    print("遍历键:")
    for subject in scores:
        print(f"  {subject}: {scores[subject]}")
    
    print("遍历键值对:")
    for subject, score in scores.items():
        print(f"  {subject}: {score}")
    
    print("遍历值:")
    for score in scores.values():
        print(f"  分数: {score}")
    
    # 3. 字典更新
    print(f"\n3. 字典更新:")
    more_scores = {"生物": 90, "历史": 85}
    scores.update(more_scores)
    print(f"更新后: {scores}")
    
    # 使用字典更新
    scores.update({"数学": 90, "地理": 82})
    print(f"再次更新: {scores}")
    
    # 4. 字典合并（Python 3.9+）
    print(f"\n4. 字典合并:")
    dict1 = {"a": 1, "b": 2}
    dict2 = {"c": 3, "d": 4}
    dict3 = {"b": 20, "e": 5}  # 有重复键
    
    # 使用 | 操作符（Python 3.9+）
    try:
        merged = dict1 | dict2
        print(f"合并 dict1 | dict2: {merged}")
        
        # 有重复键的合并
        merged_with_overlap = dict1 | dict3
        print(f"有重复键的合并: {merged_with_overlap}")
    except TypeError:
        # 对于较老的Python版本
        merged = {**dict1, **dict2}
        print(f"使用解包合并: {merged}")
    
    # 5. 字典推导式
    print(f"\n5. 字典推导式:")
    
    # 基本推导式
    squares = {x: x**2 for x in range(1, 6)}
    print(f"平方字典: {squares}")
    
    # 带条件的推导式
    high_scores = {subject: score for subject, score in scores.items() if score >= 85}
    print(f"高分科目: {high_scores}")
    
    # 键值互换
    score_to_subject = {score: subject for subject, score in scores.items()}
    print(f"分数到科目映射: {score_to_subject}")
    
    # 字符串处理
    words = ["python", "java", "javascript"]
    word_lengths = {word: len(word) for word in words}
    print(f"单词长度: {word_lengths}")


def demo_nested_structures():
    """
    演示嵌套数据结构
    """
    print("\n🏗️ 嵌套数据结构演示")
    print("=" * 30)
    
    # 1. 嵌套字典
    print("1. 嵌套字典:")
    students = {
        "S001": {
            "name": "张三",
            "age": 20,
            "scores": {"数学": 85, "英语": 92, "物理": 78},
            "contact": {"email": "zhangsan@email.com", "phone": "123-456-7890"}
        },
        "S002": {
            "name": "李四",
            "age": 19,
            "scores": {"数学": 90, "英语": 88, "物理": 85},
            "contact": {"email": "lisi@email.com", "phone": "098-765-4321"}
        }
    }
    
    print("学生数据库:")
    for student_id, info in students.items():
        print(f"  {student_id}: {info['name']}, {info['age']}岁")
        print(f"    成绩: {info['scores']}")
        print(f"    联系方式: {info['contact']}")
    
    # 2. 访问嵌套数据
    print(f"\n2. 访问嵌套数据:")
    print(f"张三的数学成绩: {students['S001']['scores']['数学']}")
    print(f"李四的邮箱: {students['S002']['contact']['email']}")
    
    # 安全访问嵌套数据
    def safe_get(data, *keys, default=None):
        """安全获取嵌套字典的值"""
        for key in keys:
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return default
        return data
    
    math_score = safe_get(students, "S001", "scores", "数学", default=0)
    unknown_score = safe_get(students, "S003", "scores", "数学", default=0)
    
    print(f"安全获取张三数学成绩: {math_score}")
    print(f"安全获取不存在学生成绩: {unknown_score}")
    
    # 3. 复杂数据结构
    print(f"\n3. 复杂数据结构:")
    
    # 班级管理系统
    school_data = {
        "classes": {
            "class_1": {
                "teacher": "王老师",
                "students": ["张三", "李四", "王五"],
                "subjects": ["数学", "英语", "物理"]
            },
            "class_2": {
                "teacher": "刘老师",
                "students": ["赵六", "钱七", "孙八"],
                "subjects": ["化学", "生物", "历史"]
            }
        },
        "teachers": {
            "王老师": {"subject": "数学", "experience": 10},
            "刘老师": {"subject": "化学", "experience": 8}
        }
    }
    
    print("学校数据结构:")
    for class_name, class_info in school_data["classes"].items():
        teacher = class_info["teacher"]
        student_count = len(class_info["students"])
        subjects = ", ".join(class_info["subjects"])
        
        print(f"  {class_name}: 老师={teacher}, 学生数={student_count}, 科目={subjects}")
    
    # 4. JSON数据处理
    print(f"\n4. JSON数据处理:")
    
    # 将复杂数据结构转换为JSON
    json_string = json.dumps(school_data, ensure_ascii=False, indent=2)
    print("转换为JSON:")
    print(json_string[:200] + "...")
    
    # 从JSON恢复数据
    restored_data = json.loads(json_string)
    print(f"从JSON恢复的数据类型: {type(restored_data)}")
    print(f"数据完整性检查: {restored_data == school_data}")


def demo_advanced_dict_usage():
    """
    演示字典的高级用法
    """
    print("\n🚀 字典高级用法演示")
    print("=" * 30)
    
    # 1. defaultdict - 默认字典
    print("1. defaultdict - 默认字典:")
    
    # 普通字典的问题
    word_count = {}
    text = "python is great python is powerful"
    
    for word in text.split():
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    
    print(f"普通字典词频统计: {word_count}")
    
    # 使用defaultdict简化
    word_count_default = defaultdict(int)
    for word in text.split():
        word_count_default[word] += 1
    
    print(f"defaultdict词频统计: {dict(word_count_default)}")
    
    # 分组数据
    students_by_major = defaultdict(list)
    students_data = [
        ("张三", "计算机"), ("李四", "数学"), ("王五", "计算机"),
        ("赵六", "物理"), ("钱七", "数学")
    ]
    
    for name, major in students_data:
        students_by_major[major].append(name)
    
    print(f"按专业分组: {dict(students_by_major)}")
    
    # 2. Counter - 计数器
    print(f"\n2. Counter - 计数器:")
    
    # 字符计数
    char_count = Counter("hello world")
    print(f"字符计数: {char_count}")
    
    # 单词计数
    word_count = Counter(text.split())
    print(f"单词计数: {word_count}")
    
    # 最常见的元素
    most_common = word_count.most_common(2)
    print(f"最常见的2个单词: {most_common}")
    
    # 列表元素计数
    numbers = [1, 2, 3, 2, 1, 3, 1, 4, 5, 1]
    number_count = Counter(numbers)
    print(f"数字计数: {number_count}")
    
    # 3. 字典的setdefault方法
    print(f"\n3. setdefault方法:")
    
    # 构建倒排索引
    documents = {
        "doc1": "python programming language",
        "doc2": "java programming tutorial",
        "doc3": "python data science"
    }
    
    inverted_index = {}
    for doc_id, content in documents.items():
        for word in content.split():
            inverted_index.setdefault(word, []).append(doc_id)
    
    print("倒排索引:")
    for word, docs in inverted_index.items():
        print(f"  {word}: {docs}")
    
    # 4. 字典的get方法高级用法
    print(f"\n4. get方法高级用法:")
    
    config = {
        "database": {
            "host": "localhost",
            "port": 5432
        },
        "cache": {
            "enabled": True
        }
    }
    
    # 链式get调用
    db_host = config.get("database", {}).get("host", "unknown")
    db_timeout = config.get("database", {}).get("timeout", 30)
    cache_size = config.get("cache", {}).get("size", 100)
    
    print(f"数据库主机: {db_host}")
    print(f"数据库超时: {db_timeout}")
    print(f"缓存大小: {cache_size}")
    
    # 5. 字典作为开关
    print(f"\n5. 字典作为开关:")
    
    def calculate(operation, a, b):
        operations = {
            "add": lambda x, y: x + y,
            "subtract": lambda x, y: x - y,
            "multiply": lambda x, y: x * y,
            "divide": lambda x, y: x / y if y != 0 else "除零错误"
        }
        
        return operations.get(operation, lambda x, y: "未知操作")(a, b)
    
    print(f"加法: {calculate('add', 10, 5)}")
    print(f"除法: {calculate('divide', 10, 2)}")
    print(f"未知操作: {calculate('unknown', 10, 5)}")


def demo_practical_applications():
    """
    演示元组和字典的实际应用
    """
    print("\n🎯 实际应用场景演示")
    print("=" * 30)
    
    # 1. 配置管理
    print("1. 配置管理:")
    
    # 应用配置
    app_config = {
        "app_name": "学生管理系统",
        "version": (1, 2, 3),  # 使用元组表示版本
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "student_db"
        },
        "features": {
            "authentication": True,
            "logging": True,
            "caching": False
        }
    }
    
    version = app_config["version"]
    print(f"应用版本: {version[0]}.{version[1]}.{version[2]}")
    print(f"数据库配置: {app_config['database']}")
    
    # 2. 缓存系统
    print(f"\n2. 缓存系统:")
    
    class SimpleCache:
        def __init__(self):
            self._cache = {}
            self._access_count = defaultdict(int)
        
        def get(self, key):
            if key in self._cache:
                self._access_count[key] += 1
                return self._cache[key]
            return None
        
        def set(self, key, value):
            self._cache[key] = value
            self._access_count[key] = 0
        
        def stats(self):
            return dict(self._access_count)
    
    cache = SimpleCache()
    cache.set("user:123", {"name": "张三", "age": 20})
    cache.set("user:456", {"name": "李四", "age": 22})
    
    # 访问缓存
    user1 = cache.get("user:123")
    user1_again = cache.get("user:123")
    user2 = cache.get("user:456")
    
    print(f"缓存统计: {cache.stats()}")
    
    # 3. 数据转换和映射
    print(f"\n3. 数据转换和映射:")
    
    # 成绩等级映射
    grade_mapping = {
        (90, 100): 'A',
        (80, 89): 'B',
        (70, 79): 'C',
        (60, 69): 'D',
        (0, 59): 'F'
    }
    
    def get_grade(score):
        for (min_score, max_score), grade in grade_mapping.items():
            if min_score <= score <= max_score:
                return grade
        return 'Invalid'
    
    scores = [95, 87, 76, 65, 45]
    grades = [get_grade(score) for score in scores]
    
    print(f"分数: {scores}")
    print(f"等级: {grades}")
    
    # 4. 状态机
    print(f"\n4. 状态机:")
    
    class OrderStateMachine:
        def __init__(self):
            self.state = "pending"
            self.transitions = {
                "pending": ["confirmed", "cancelled"],
                "confirmed": ["shipped", "cancelled"],
                "shipped": ["delivered"],
                "delivered": [],
                "cancelled": []
            }
        
        def can_transition_to(self, new_state):
            return new_state in self.transitions.get(self.state, [])
        
        def transition_to(self, new_state):
            if self.can_transition_to(new_state):
                old_state = self.state
                self.state = new_state
                return f"状态从 {old_state} 转换到 {new_state}"
            else:
                return f"无法从 {self.state} 转换到 {new_state}"
    
    order = OrderStateMachine()
    print(f"初始状态: {order.state}")
    print(order.transition_to("confirmed"))
    print(order.transition_to("shipped"))
    print(order.transition_to("pending"))  # 无效转换
    print(order.transition_to("delivered"))
    
    # 5. 数据聚合和分析
    print(f"\n5. 数据聚合和分析:")
    
    # 销售数据
    sales_data = [
        ("2024-01", "产品A", 1000),
        ("2024-01", "产品B", 1500),
        ("2024-02", "产品A", 1200),
        ("2024-02", "产品B", 1800),
        ("2024-01", "产品A", 800),  # 同月同产品的另一笔销售
    ]
    
    # 按月份聚合
    monthly_sales = defaultdict(int)
    # 按产品聚合
    product_sales = defaultdict(int)
    # 按月份和产品聚合
    monthly_product_sales = defaultdict(lambda: defaultdict(int))
    
    for month, product, amount in sales_data:
        monthly_sales[month] += amount
        product_sales[product] += amount
        monthly_product_sales[month][product] += amount
    
    print("按月份聚合:")
    for month, total in monthly_sales.items():
        print(f"  {month}: {total}")
    
    print("按产品聚合:")
    for product, total in product_sales.items():
        print(f"  {product}: {total}")
    
    print("按月份和产品聚合:")
    for month, products in monthly_product_sales.items():
        print(f"  {month}:")
        for product, amount in products.items():
            print(f"    {product}: {amount}")


def main():
    """
    主函数：运行所有演示
    """
    print("Session05 Example2: 元组和字典操作详解")
    print("=" * 50)
    
    demo_tuple_basics()
    demo_tuple_unpacking()
    demo_tuple_applications()
    demo_dict_basics()
    demo_dict_methods()
    demo_nested_structures()
    demo_advanced_dict_usage()
    demo_practical_applications()
    
    print("\n✅ 元组和字典操作演示完成！")


if __name__ == "__main__":
    main()