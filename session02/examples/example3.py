#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session02 示例3：字符串操作详解

本示例演示了Python中字符串的各种操作，包括：
- 字符串的创建和基本操作
- 字符串格式化的多种方法
- 常用字符串方法
- 字符串的索引和切片

作者: Python教程团队
创建日期: 2024-12-19
"""

def main():
    """演示字符串操作"""
    print("=== 字符串操作详解 ===")
    
    # 1. 字符串的创建
    print("\n1. 字符串的创建")
    
    single_quote = 'Hello World'
    double_quote = "Python Programming"
    triple_quote_single = '''这是一个
多行字符串
使用三个单引号'''
    triple_quote_double = """这也是一个
多行字符串
使用三个双引号"""
    
    print(f"单引号: {single_quote}")
    print(f"双引号: {double_quote}")
    print(f"三引号(单):\n{triple_quote_single}")
    print(f"三引号(双):\n{triple_quote_double}")
    
    # 2. 字符串连接
    print("\n2. 字符串连接")
    
    first_name = "张"
    last_name = "三"
    
    # 使用 + 连接
    full_name1 = first_name + last_name
    print(f"使用 + 连接: {full_name1}")
    
    # 使用 += 连接
    greeting = "你好, "
    greeting += full_name1
    print(f"使用 += 连接: {greeting}")
    
    # 使用 join() 方法连接
    words = ["Python", "是", "一门", "优秀的", "编程语言"]
    sentence = " ".join(words)
    print(f"使用 join() 连接: {sentence}")
    
    # 3. 字符串格式化
    print("\n3. 字符串格式化")
    
    name = "李四"
    age = 28
    salary = 12500.75
    
    # f-string 格式化（推荐）
    info1 = f"姓名: {name}, 年龄: {age}, 工资: {salary:.2f}"
    print(f"f-string: {info1}")
    
    # format() 方法
    info2 = "姓名: {}, 年龄: {}, 工资: {:.2f}".format(name, age, salary)
    print(f"format(): {info2}")
    
    # format() 方法带索引
    info3 = "姓名: {0}, 年龄: {1}, 工资: {2:.2f}".format(name, age, salary)
    print(f"format()带索引: {info3}")
    
    # format() 方法带关键字
    info4 = "姓名: {n}, 年龄: {a}, 工资: {s:.2f}".format(n=name, a=age, s=salary)
    print(f"format()带关键字: {info4}")
    
    # % 格式化（旧式）
    info5 = "姓名: %s, 年龄: %d, 工资: %.2f" % (name, age, salary)
    print(f"% 格式化: {info5}")
    
    # 4. 字符串方法
    print("\n4. 字符串方法")
    
    text = "  Python Programming Language  "
    print(f"原字符串: '{text}'")
    
    # 大小写转换
    print(f"转大写: '{text.upper()}'")
    print(f"转小写: '{text.lower()}'")
    print(f"首字母大写: '{text.title()}'")
    print(f"大小写互换: '{text.swapcase()}'")
    
    # 去除空格
    print(f"去除两端空格: '{text.strip()}'")
    print(f"去除左侧空格: '{text.lstrip()}'")
    print(f"去除右侧空格: '{text.rstrip()}'")
    
    # 查找和替换
    clean_text = text.strip()
    print(f"\n查找和替换操作:")
    print(f"查找 'Python': 位置 {clean_text.find('Python')}")
    print(f"查找 'Java': 位置 {clean_text.find('Java')}")
    print(f"替换 'Python' 为 'Java': '{clean_text.replace('Python', 'Java')}'")
    print(f"统计 'a' 的个数: {clean_text.count('a')}")
    
    # 分割和连接
    print(f"\n分割和连接:")
    words = clean_text.split(' ')
    print(f"按空格分割: {words}")
    
    rejoined = '-'.join(words)
    print(f"用连字符连接: {rejoined}")
    
    # 5. 字符串判断方法
    print("\n5. 字符串判断方法")
    
    test_strings = ["123", "abc", "ABC", "Hello123", "hello world", ""]
    
    for s in test_strings:
        print(f"\n字符串: '{s}'")
        print(f"  是否为数字: {s.isdigit()}")
        print(f"  是否为字母: {s.isalpha()}")
        print(f"  是否为字母数字: {s.isalnum()}")
        print(f"  是否为小写: {s.islower()}")
        print(f"  是否为大写: {s.isupper()}")
        print(f"  是否为空格: {s.isspace()}")
    
    # 6. 字符串索引和切片
    print("\n6. 字符串索引和切片")
    
    message = "Hello Python"
    print(f"字符串: '{message}'")
    print(f"长度: {len(message)}")
    
    # 正向索引
    print(f"\n正向索引:")
    print(f"第1个字符 [0]: '{message[0]}'")
    print(f"第6个字符 [5]: '{message[5]}'")
    print(f"最后一个字符 [{len(message)-1}]: '{message[len(message)-1]}'")
    
    # 反向索引
    print(f"\n反向索引:")
    print(f"最后一个字符 [-1]: '{message[-1]}'")
    print(f"倒数第二个字符 [-2]: '{message[-2]}'")
    
    # 切片操作
    print(f"\n切片操作:")
    print(f"前5个字符 [0:5]: '{message[0:5]}'")
    print(f"从第6个到最后 [6:]: '{message[6:]}'")
    print(f"最后5个字符 [-5:]: '{message[-5:]}'")
    print(f"每隔一个字符 [::2]: '{message[::2]}'")
    print(f"反转字符串 [::-1]: '{message[::-1]}'")
    
    # 7. 实际应用示例
    print("\n7. 实际应用示例")
    
    # 处理用户输入
    def process_user_input(user_input):
        """处理用户输入的字符串"""
        # 去除首尾空格并转换为小写
        cleaned = user_input.strip().lower()
        
        # 检查是否为空
        if not cleaned:
            return "输入不能为空"
        
        # 检查长度
        if len(cleaned) < 2:
            return "输入太短"
        
        # 首字母大写
        formatted = cleaned.capitalize()
        
        return f"处理后的输入: {formatted}"
    
    test_inputs = ["  HELLO  ", "a", "", "  python programming  "]
    for inp in test_inputs:
        result = process_user_input(inp)
        print(f"输入: '{inp}' -> {result}")
    
    # 简单的文本分析
    print("\n简单的文本分析:")
    article = """Python是一种高级编程语言。它简单易学，功能强大。
    Python广泛应用于Web开发、数据分析、人工智能等领域。
    学习Python是一个很好的选择。"""
    
    # 统计信息
    word_count = len(article.split())
    char_count = len(article)
    line_count = len(article.split('\n'))
    python_count = article.lower().count('python')
    
    print(f"文章统计:")
    print(f"  字符数: {char_count}")
    print(f"  单词数: {word_count}")
    print(f"  行数: {line_count}")
    print(f"  'Python' 出现次数: {python_count}")

if __name__ == "__main__":
    main()