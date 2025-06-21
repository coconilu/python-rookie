#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session05 示例3: 集合和数据结构综合应用

本文件详细演示集合的各种操作和数据结构的综合应用，包括：
- 集合的创建和基本操作
- 集合运算（并集、交集、差集等）
- 集合推导式和高级用法
- 数据结构性能对比
- 综合应用案例
- 最佳实践和优化技巧

作者: Python教程团队
创建日期: 2024-12-21
"""

import time
import random
from typing import Set, List, Dict, Tuple, Any
from collections import defaultdict, Counter


def demo_set_basics():
    """
    演示集合的基础操作
    """
    print("🔢 集合基础操作演示")
    print("=" * 30)
    
    # 1. 创建集合
    print("1. 创建集合:")
    empty_set = set()  # 注意：{}创建的是空字典，不是空集合
    numbers = {1, 2, 3, 4, 5}
    from_list = set([1, 2, 2, 3, 3, 4])  # 自动去重
    from_string = set("hello")  # 字符集合
    
    print(f"空集合: {empty_set}, 类型: {type(empty_set)}")
    print(f"数字集合: {numbers}")
    print(f"从列表创建（自动去重）: {from_list}")
    print(f"从字符串创建: {from_string}")
    
    # 2. 集合的特性
    print(f"\n2. 集合的特性:")
    print(f"无序性: {numbers}")
    print(f"唯一性: 原列表[1,2,2,3,3,4] -> 集合{from_list}")
    
    # 3. 基本操作
    print(f"\n3. 基本操作:")
    fruits = {"apple", "banana", "orange"}
    print(f"水果集合: {fruits}")
    
    # 添加元素
    fruits.add("grape")
    print(f"添加grape后: {fruits}")
    
    # 添加多个元素
    fruits.update(["kiwi", "mango"])
    print(f"添加多个元素后: {fruits}")
    
    # 删除元素
    fruits.remove("banana")  # 如果元素不存在会报错
    print(f"删除banana后: {fruits}")
    
    fruits.discard("pear")  # 如果元素不存在不会报错
    print(f"尝试删除不存在的pear: {fruits}")
    
    # 随机删除并返回元素
    removed = fruits.pop()
    print(f"随机删除的元素: {removed}")
    print(f"删除后的集合: {fruits}")
    
    # 4. 成员测试
    print(f"\n4. 成员测试:")
    print(f"'apple' in fruits: {'apple' in fruits}")
    print(f"'banana' not in fruits: {'banana' not in fruits}")
    
    # 5. 集合长度和清空
    print(f"\n5. 集合长度和清空:")
    print(f"集合长度: {len(fruits)}")
    fruits_copy = fruits.copy()
    fruits_copy.clear()
    print(f"清空后: {fruits_copy}")


def demo_set_operations():
    """
    演示集合运算
    """
    print("\n🧮 集合运算演示")
    print("=" * 30)
    
    # 准备测试数据
    set_a = {1, 2, 3, 4, 5}
    set_b = {4, 5, 6, 7, 8}
    set_c = {1, 2, 3}
    
    print(f"集合A: {set_a}")
    print(f"集合B: {set_b}")
    print(f"集合C: {set_c}")
    
    # 1. 并集（Union）
    print(f"\n1. 并集（Union）:")
    union1 = set_a | set_b  # 使用 | 操作符
    union2 = set_a.union(set_b)  # 使用方法
    print(f"A | B = {union1}")
    print(f"A.union(B) = {union2}")
    print(f"结果相同: {union1 == union2}")
    
    # 多个集合的并集
    union_multiple = set_a | set_b | set_c
    print(f"A | B | C = {union_multiple}")
    
    # 2. 交集（Intersection）
    print(f"\n2. 交集（Intersection）:")
    intersection1 = set_a & set_b  # 使用 & 操作符
    intersection2 = set_a.intersection(set_b)  # 使用方法
    print(f"A & B = {intersection1}")
    print(f"A.intersection(B) = {intersection2}")
    
    # 3. 差集（Difference）
    print(f"\n3. 差集（Difference）:")
    diff1 = set_a - set_b  # A中有但B中没有的元素
    diff2 = set_b - set_a  # B中有但A中没有的元素
    print(f"A - B = {diff1}")
    print(f"B - A = {diff2}")
    print(f"A.difference(B) = {set_a.difference(set_b)}")
    
    # 4. 对称差集（Symmetric Difference）
    print(f"\n4. 对称差集（Symmetric Difference）:")
    sym_diff1 = set_a ^ set_b  # 使用 ^ 操作符
    sym_diff2 = set_a.symmetric_difference(set_b)  # 使用方法
    print(f"A ^ B = {sym_diff1}")
    print(f"A.symmetric_difference(B) = {sym_diff2}")
    print(f"等价于 (A-B) | (B-A) = {(set_a - set_b) | (set_b - set_a)}")
    
    # 5. 子集和超集
    print(f"\n5. 子集和超集:")
    print(f"C是否为A的子集: {set_c.issubset(set_a)}")
    print(f"A是否为C的超集: {set_a.issuperset(set_c)}")
    print(f"A和B是否不相交: {set_a.isdisjoint({9, 10, 11})}")
    
    # 6. 实际应用示例
    print(f"\n6. 实际应用示例:")
    
    # 学生选课系统
    math_students = {"张三", "李四", "王五", "赵六"}
    physics_students = {"李四", "王五", "钱七", "孙八"}
    chemistry_students = {"王五", "赵六", "钱七", "周九"}
    
    print(f"数学课学生: {math_students}")
    print(f"物理课学生: {physics_students}")
    print(f"化学课学生: {chemistry_students}")
    
    # 选了数学和物理的学生
    math_and_physics = math_students & physics_students
    print(f"同时选数学和物理: {math_and_physics}")
    
    # 选了数学但没选物理的学生
    only_math = math_students - physics_students
    print(f"只选数学不选物理: {only_math}")
    
    # 至少选了一门课的学生
    all_students = math_students | physics_students | chemistry_students
    print(f"至少选一门课的学生: {all_students}")
    
    # 选了所有三门课的学生
    all_three = math_students & physics_students & chemistry_students
    print(f"选了所有三门课: {all_three}")


def demo_set_comprehensions():
    """
    演示集合推导式
    """
    print("\n🔧 集合推导式演示")
    print("=" * 30)
    
    # 1. 基本集合推导式
    print("1. 基本集合推导式:")
    
    # 平方数集合
    squares = {x**2 for x in range(1, 6)}
    print(f"1-5的平方数: {squares}")
    
    # 偶数集合
    evens = {x for x in range(1, 11) if x % 2 == 0}
    print(f"1-10的偶数: {evens}")
    
    # 2. 字符串处理
    print(f"\n2. 字符串处理:")
    
    text = "Hello World Python Programming"
    
    # 唯一字符（忽略大小写）
    unique_chars = {char.lower() for char in text if char.isalpha()}
    print(f"唯一字符: {unique_chars}")
    
    # 单词长度集合
    word_lengths = {len(word) for word in text.split()}
    print(f"单词长度集合: {word_lengths}")
    
    # 首字母集合
    first_letters = {word[0].lower() for word in text.split() if word}
    print(f"首字母集合: {first_letters}")
    
    # 3. 数据清洗
    print(f"\n3. 数据清洗:")
    
    # 原始数据（包含重复和无效值）
    raw_data = [1, 2, 3, 2, 4, None, 5, 3, 6, '', 7, 0, 8]
    
    # 清洗数据：去重、去除None和空字符串、只保留正数
    clean_data = {x for x in raw_data if x and isinstance(x, (int, float)) and x > 0}
    print(f"原始数据: {raw_data}")
    print(f"清洗后数据: {clean_data}")
    
    # 4. 嵌套数据处理
    print(f"\n4. 嵌套数据处理:")
    
    # 学生成绩数据
    students_scores = [
        {"name": "张三", "scores": [85, 92, 78]},
        {"name": "李四", "scores": [90, 88, 85]},
        {"name": "王五", "scores": [76, 82, 79]}
    ]
    
    # 所有出现过的分数
    all_scores = {score for student in students_scores for score in student["scores"]}
    print(f"所有分数: {sorted(all_scores)}")
    
    # 高分学生（平均分>=85）
    high_performers = {student["name"] for student in students_scores 
                      if sum(student["scores"]) / len(student["scores"]) >= 85}
    print(f"高分学生: {high_performers}")
    
    # 5. 条件复杂的推导式
    print(f"\n5. 条件复杂的推导式:")
    
    # 质数集合（简单实现）
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    primes = {n for n in range(2, 50) if is_prime(n)}
    print(f"50以内的质数: {sorted(primes)}")
    
    # 回文数集合
    palindromes = {n for n in range(1, 1000) if str(n) == str(n)[::-1]}
    print(f"1000以内的回文数（前10个）: {sorted(list(palindromes))[:10]}")


def demo_performance_comparison():
    """
    演示不同数据结构的性能对比
    """
    print("\n⚡ 数据结构性能对比")
    print("=" * 30)
    
    # 准备测试数据
    size = 10000
    test_list = list(range(size))
    test_tuple = tuple(range(size))
    test_set = set(range(size))
    test_dict = {i: f"value_{i}" for i in range(size)}
    
    search_items = random.sample(range(size), 100)
    
    print(f"测试数据大小: {size}")
    print(f"搜索项目数量: {len(search_items)}")
    
    # 1. 成员测试性能
    print(f"\n1. 成员测试性能:")
    
    # 列表成员测试
    start_time = time.time()
    for item in search_items:
        _ = item in test_list
    list_time = time.time() - start_time
    
    # 元组成员测试
    start_time = time.time()
    for item in search_items:
        _ = item in test_tuple
    tuple_time = time.time() - start_time
    
    # 集合成员测试
    start_time = time.time()
    for item in search_items:
        _ = item in test_set
    set_time = time.time() - start_time
    
    # 字典键测试
    start_time = time.time()
    for item in search_items:
        _ = item in test_dict
    dict_time = time.time() - start_time
    
    print(f"列表成员测试: {list_time:.6f}秒")
    print(f"元组成员测试: {tuple_time:.6f}秒")
    print(f"集合成员测试: {set_time:.6f}秒")
    print(f"字典键测试: {dict_time:.6f}秒")
    
    # 2. 去重性能对比
    print(f"\n2. 去重性能对比:")
    
    # 创建包含重复元素的列表
    duplicate_list = [random.randint(0, size//10) for _ in range(size)]
    
    # 使用集合去重
    start_time = time.time()
    unique_set = set(duplicate_list)
    set_dedup_time = time.time() - start_time
    
    # 使用列表推导式去重（保持顺序）
    start_time = time.time()
    seen = set()
    unique_list = [x for x in duplicate_list if not (x in seen or seen.add(x))]
    list_dedup_time = time.time() - start_time
    
    # 使用字典去重（Python 3.7+保持顺序）
    start_time = time.time()
    unique_dict = list(dict.fromkeys(duplicate_list))
    dict_dedup_time = time.time() - start_time
    
    print(f"原始列表长度: {len(duplicate_list)}")
    print(f"去重后长度: {len(unique_set)}")
    print(f"集合去重: {set_dedup_time:.6f}秒")
    print(f"列表推导式去重: {list_dedup_time:.6f}秒")
    print(f"字典去重: {dict_dedup_time:.6f}秒")
    
    # 3. 内存使用对比
    print(f"\n3. 内存使用对比:")
    import sys
    
    sample_data = list(range(1000))
    
    list_size = sys.getsizeof(sample_data)
    tuple_size = sys.getsizeof(tuple(sample_data))
    set_size = sys.getsizeof(set(sample_data))
    dict_size = sys.getsizeof({i: i for i in sample_data})
    
    print(f"列表内存使用: {list_size} 字节")
    print(f"元组内存使用: {tuple_size} 字节")
    print(f"集合内存使用: {set_size} 字节")
    print(f"字典内存使用: {dict_size} 字节")
    
    # 4. 操作性能总结
    print(f"\n4. 操作性能总结:")
    performance_summary = {
        "数据结构": ["列表", "元组", "集合", "字典"],
        "成员测试": ["O(n)", "O(n)", "O(1)", "O(1)"],
        "插入": ["O(1)", "不可变", "O(1)", "O(1)"],
        "删除": ["O(n)", "不可变", "O(1)", "O(1)"],
        "内存效率": ["中等", "最好", "中等", "最差"],
        "有序性": ["有序", "有序", "无序", "有序(3.7+)"]
    }
    
    print("性能对比表:")
    for key, values in performance_summary.items():
        print(f"{key:8}: {' | '.join(f'{v:8}' for v in values)}")


def demo_comprehensive_application():
    """
    演示数据结构的综合应用
    """
    print("\n🎯 综合应用案例")
    print("=" * 30)
    
    # 案例1: 文本分析系统
    print("1. 文本分析系统:")
    
    class TextAnalyzer:
        def __init__(self):
            self.word_count = Counter()
            self.unique_words = set()
            self.word_positions = defaultdict(list)
            self.sentence_count = 0
        
        def analyze(self, text: str):
            # 分句
            sentences = [s.strip() for s in text.split('.') if s.strip()]
            self.sentence_count = len(sentences)
            
            # 分词和统计
            for sent_idx, sentence in enumerate(sentences):
                words = sentence.lower().split()
                for word_idx, word in enumerate(words):
                    # 清理标点
                    clean_word = ''.join(c for c in word if c.isalnum())
                    if clean_word:
                        self.word_count[clean_word] += 1
                        self.unique_words.add(clean_word)
                        self.word_positions[clean_word].append((sent_idx, word_idx))
        
        def get_stats(self):
            return {
                "总词数": sum(self.word_count.values()),
                "唯一词数": len(self.unique_words),
                "句子数": self.sentence_count,
                "平均句长": sum(self.word_count.values()) / self.sentence_count if self.sentence_count > 0 else 0
            }
        
        def get_most_common(self, n=5):
            return self.word_count.most_common(n)
        
        def find_word_positions(self, word):
            return self.word_positions.get(word.lower(), [])
    
    # 测试文本分析
    sample_text = """
    Python是一种高级编程语言. Python具有简洁的语法和强大的功能. 
    许多开发者选择Python进行数据分析. Python在机器学习领域也很流行.
    """
    
    analyzer = TextAnalyzer()
    analyzer.analyze(sample_text)
    
    print(f"文本统计: {analyzer.get_stats()}")
    print(f"最常见词汇: {analyzer.get_most_common(3)}")
    print(f"'Python'出现位置: {analyzer.find_word_positions('Python')}")
    
    # 案例2: 社交网络分析
    print(f"\n2. 社交网络分析:")
    
    class SocialNetwork:
        def __init__(self):
            self.users = set()
            self.friendships = defaultdict(set)
            self.user_info = {}
        
        def add_user(self, user_id, name, interests=None):
            self.users.add(user_id)
            self.user_info[user_id] = {
                "name": name,
                "interests": set(interests or [])
            }
        
        def add_friendship(self, user1, user2):
            if user1 in self.users and user2 in self.users:
                self.friendships[user1].add(user2)
                self.friendships[user2].add(user1)
        
        def get_mutual_friends(self, user1, user2):
            return self.friendships[user1] & self.friendships[user2]
        
        def get_friend_suggestions(self, user_id, max_suggestions=3):
            user_friends = self.friendships[user_id]
            suggestions = set()
            
            # 朋友的朋友
            for friend in user_friends:
                suggestions.update(self.friendships[friend])
            
            # 排除自己和已有朋友
            suggestions -= {user_id}
            suggestions -= user_friends
            
            # 按共同朋友数排序
            suggestion_scores = []
            for suggestion in suggestions:
                mutual_count = len(self.get_mutual_friends(user_id, suggestion))
                suggestion_scores.append((suggestion, mutual_count))
            
            suggestion_scores.sort(key=lambda x: x[1], reverse=True)
            return suggestion_scores[:max_suggestions]
        
        def find_users_by_interest(self, interest):
            return {user_id for user_id, info in self.user_info.items() 
                   if interest in info["interests"]}
        
        def get_common_interests(self, user1, user2):
            interests1 = self.user_info[user1]["interests"]
            interests2 = self.user_info[user2]["interests"]
            return interests1 & interests2
    
    # 构建社交网络
    network = SocialNetwork()
    
    # 添加用户
    users_data = [
        ("u1", "张三", ["编程", "音乐", "旅行"]),
        ("u2", "李四", ["编程", "游戏", "电影"]),
        ("u3", "王五", ["音乐", "摄影", "旅行"]),
        ("u4", "赵六", ["编程", "摄影", "运动"]),
        ("u5", "钱七", ["游戏", "音乐", "运动"]),
        ("u6", "孙八", ["旅行", "电影", "运动"])
    ]
    
    for user_id, name, interests in users_data:
        network.add_user(user_id, name, interests)
    
    # 添加友谊关系
    friendships = [
        ("u1", "u2"), ("u1", "u3"), ("u2", "u4"), 
        ("u3", "u5"), ("u4", "u5"), ("u5", "u6")
    ]
    
    for user1, user2 in friendships:
        network.add_friendship(user1, user2)
    
    # 分析网络
    print(f"张三的朋友: {[network.user_info[uid]['name'] for uid in network.friendships['u1']]}")
    print(f"张三和李四的共同朋友: {[network.user_info[uid]['name'] for uid in network.get_mutual_friends('u1', 'u2')]}")
    print(f"张三的朋友推荐: {[(network.user_info[uid]['name'], score) for uid, score in network.get_friend_suggestions('u1')]}")
    print(f"喜欢编程的用户: {[network.user_info[uid]['name'] for uid in network.find_users_by_interest('编程')]}")
    print(f"张三和赵六的共同兴趣: {network.get_common_interests('u1', 'u4')}")
    
    # 案例3: 数据去重和清洗
    print(f"\n3. 数据去重和清洗:")
    
    class DataCleaner:
        @staticmethod
        def remove_duplicates(data, key_func=None):
            """去除重复数据"""
            if key_func is None:
                return list(set(data))
            
            seen = set()
            result = []
            for item in data:
                key = key_func(item)
                if key not in seen:
                    seen.add(key)
                    result.append(item)
            return result
        
        @staticmethod
        def find_outliers(numbers, threshold=2):
            """找出异常值"""
            if not numbers:
                return set()
            
            mean = sum(numbers) / len(numbers)
            variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
            std_dev = variance ** 0.5
            
            outliers = set()
            for num in numbers:
                if abs(num - mean) > threshold * std_dev:
                    outliers.add(num)
            
            return outliers
        
        @staticmethod
        def merge_similar_strings(strings, similarity_threshold=0.8):
            """合并相似字符串"""
            def similarity(s1, s2):
                s1_set = set(s1.lower())
                s2_set = set(s2.lower())
                intersection = s1_set & s2_set
                union = s1_set | s2_set
                return len(intersection) / len(union) if union else 0
            
            groups = []
            for string in strings:
                placed = False
                for group in groups:
                    if any(similarity(string, existing) >= similarity_threshold 
                          for existing in group):
                        group.add(string)
                        placed = True
                        break
                if not placed:
                    groups.append({string})
            
            return groups
    
    # 测试数据清洗
    dirty_data = [1, 2, 3, 2, 4, 100, 5, 3, 6, -50, 7]  # 包含重复和异常值
    clean_numbers = DataCleaner.remove_duplicates(dirty_data)
    outliers = DataCleaner.find_outliers(dirty_data)
    
    print(f"原始数据: {dirty_data}")
    print(f"去重后: {clean_numbers}")
    print(f"异常值: {outliers}")
    
    # 字符串相似性合并
    similar_strings = ["Python", "python", "Java", "java", "JavaScript", "Javascript"]
    string_groups = DataCleaner.merge_similar_strings(similar_strings)
    print(f"相似字符串分组: {[list(group) for group in string_groups]}")


def demo_best_practices():
    """
    演示最佳实践和优化技巧
    """
    print("\n💡 最佳实践和优化技巧")
    print("=" * 30)
    
    # 1. 选择合适的数据结构
    print("1. 数据结构选择指南:")
    
    guidelines = {
        "需要有序且可变": "列表 (list)",
        "需要有序且不可变": "元组 (tuple)",
        "需要快速成员测试": "集合 (set)",
        "需要键值映射": "字典 (dict)",
        "需要去重": "集合 (set)",
        "需要计数": "Counter",
        "需要默认值": "defaultdict",
        "需要命名访问": "namedtuple"
    }
    
    for scenario, recommendation in guidelines.items():
        print(f"  {scenario}: {recommendation}")
    
    # 2. 性能优化技巧
    print(f"\n2. 性能优化技巧:")
    
    # 使用集合进行快速成员测试
    large_list = list(range(10000))
    search_set = set(large_list)
    
    # 错误方式：在列表中搜索
    def slow_filter(items, valid_items_list):
        return [item for item in items if item in valid_items_list]
    
    # 正确方式：在集合中搜索
    def fast_filter(items, valid_items_set):
        return [item for item in items if item in valid_items_set]
    
    test_items = [1, 100, 1000, 5000, 9999]
    
    start_time = time.time()
    slow_result = slow_filter(test_items, large_list)
    slow_time = time.time() - start_time
    
    start_time = time.time()
    fast_result = fast_filter(test_items, search_set)
    fast_time = time.time() - start_time
    
    print(f"列表搜索时间: {slow_time:.6f}秒")
    print(f"集合搜索时间: {fast_time:.6f}秒")
    print(f"性能提升: {slow_time/fast_time:.1f}倍")
    
    # 3. 内存优化
    print(f"\n3. 内存优化:")
    
    # 使用生成器表达式而不是列表推导式（当不需要立即获取所有结果时）
    def memory_efficient_processing():
        # 大数据集
        large_range = range(1000000)
        
        # 内存密集型：列表推导式
        # squares_list = [x**2 for x in large_range if x % 2 == 0]  # 占用大量内存
        
        # 内存友好型：生成器表达式
        squares_gen = (x**2 for x in large_range if x % 2 == 0)
        
        # 只在需要时计算
        first_10_squares = [next(squares_gen) for _ in range(10)]
        return first_10_squares
    
    efficient_result = memory_efficient_processing()
    print(f"内存友好的前10个偶数平方: {efficient_result}")
    
    # 4. 常见陷阱和解决方案
    print(f"\n4. 常见陷阱和解决方案:")
    
    # 陷阱1：可变默认参数
    print("陷阱1 - 可变默认参数:")
    
    # 错误方式
    def bad_function(item, target_list=[]):
        target_list.append(item)
        return target_list
    
    # 正确方式
    def good_function(item, target_list=None):
        if target_list is None:
            target_list = []
        target_list.append(item)
        return target_list
    
    print(f"错误方式第一次调用: {bad_function(1)}")
    print(f"错误方式第二次调用: {bad_function(2)}")
    print(f"正确方式第一次调用: {good_function(1)}")
    print(f"正确方式第二次调用: {good_function(2)}")
    
    # 陷阱2：集合和字典的可变性
    print(f"\n陷阱2 - 在迭代时修改集合:")
    
    # 错误方式：在迭代时修改
    numbers = {1, 2, 3, 4, 5}
    print(f"原始集合: {numbers}")
    
    # 正确方式：创建副本进行迭代
    for num in numbers.copy():
        if num % 2 == 0:
            numbers.remove(num)
    
    print(f"删除偶数后: {numbers}")
    
    # 5. 代码风格建议
    print(f"\n5. 代码风格建议:")
    
    style_tips = [
        "使用集合推导式而不是set(列表推导式)",
        "使用in操作符进行成员测试，而不是find()或index()",
        "使用字典的get()方法而不是try/except KeyError",
        "使用collections模块的专用数据结构",
        "在需要去重时优先考虑集合",
        "使用元组作为字典的键（当需要复合键时）",
        "使用frozenset作为不可变集合"
    ]
    
    for i, tip in enumerate(style_tips, 1):
        print(f"  {i}. {tip}")
    
    # 示例：frozenset的使用
    print(f"\nfrozenset示例:")
    mutable_set = {1, 2, 3}
    immutable_set = frozenset([1, 2, 3])
    
    # frozenset可以作为字典的键或集合的元素
    set_of_sets = {frozenset([1, 2]), frozenset([3, 4]), frozenset([1, 2])}  # 自动去重
    print(f"集合的集合: {set_of_sets}")
    
    nested_dict = {frozenset(["key1", "key2"]): "value1"}
    print(f"使用frozenset作为键: {nested_dict}")


def main():
    """
    主函数：运行所有演示
    """
    print("Session05 Example3: 集合和数据结构综合应用")
    print("=" * 50)
    
    demo_set_basics()
    demo_set_operations()
    demo_set_comprehensions()
    demo_performance_comparison()
    demo_comprehensive_application()
    demo_best_practices()
    
    print("\n✅ 集合和数据结构综合应用演示完成！")
    print("\n📚 学习要点总结:")
    print("1. 集合提供O(1)的成员测试和去重功能")
    print("2. 不同数据结构有不同的性能特征")
    print("3. 选择合适的数据结构可以显著提升性能")
    print("4. 集合运算在数据分析中非常有用")
    print("5. 避免常见陷阱，遵循最佳实践")


if __name__ == "__main__":
    main()