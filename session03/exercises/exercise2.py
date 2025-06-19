#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session03 练习题2：比较运算练习

题目描述：
编写一个程序，实现以下功能：
1. 创建一个成绩管理系统，能够比较和分析学生成绩
2. 实现一个商品价格比较工具
3. 编写字符串比较和排序功能
4. 实现数据验证和范围检查功能

具体要求：
1. 实现成绩等级判定和排名功能
2. 实现商品价格比较和推荐功能
3. 实现字符串排序和搜索功能
4. 实现数据范围验证功能
5. 处理各种边界情况

学习目标：
- 熟练使用所有比较运算符
- 理解比较运算符在条件判断中的应用
- 学会处理不同数据类型的比较
- 掌握链式比较的使用方法

提示：
- 注意浮点数比较的精度问题
- 考虑字符串比较的大小写问题
- 使用链式比较简化条件判断
- 处理空值和异常输入
"""

import math


def grade_classifier(score):
    """
    根据分数判定成绩等级
    
    参数:
        score (float): 学生分数 (0-100)
    
    返回:
        str: 成绩等级 ('A', 'B', 'C', 'D', 'F')
    
    等级标准:
        A: 90-100
        B: 80-89
        C: 70-79
        D: 60-69
        F: 0-59
    
    在这里实现你的代码
    """
    # TODO: 实现成绩等级判定
    # 提示：使用if-elif语句和比较运算符
    pass


def compare_students(student1, student2):
    """
    比较两个学生的成绩
    
    参数:
        student1 (dict): 学生1信息 {'name': str, 'score': float}
        student2 (dict): 学生2信息 {'name': str, 'score': float}
    
    返回:
        str: 比较结果描述
    
    在这里实现你的代码
    """
    # TODO: 比较两个学生的成绩
    # 提示：比较分数，返回描述性文字
    pass


def find_top_students(students, top_n=3):
    """
    找出成绩最好的前N名学生
    
    参数:
        students (list): 学生列表，每个元素是 {'name': str, 'score': float}
        top_n (int): 要找出的前N名
    
    返回:
        list: 前N名学生列表，按成绩从高到低排序
    
    在这里实现你的代码
    """
    # TODO: 找出前N名学生
    # 提示：使用sorted()函数和key参数
    pass


def analyze_class_performance(students):
    """
    分析班级成绩表现
    
    参数:
        students (list): 学生列表
    
    返回:
        dict: 分析结果，包含各等级人数统计
    
    在这里实现你的代码
    """
    # TODO: 统计各等级人数
    # 提示：遍历学生列表，使用grade_classifier函数
    pass


def price_comparator(products, budget):
    """
    根据预算筛选商品
    
    参数:
        products (list): 商品列表，每个元素是 {'name': str, 'price': float}
        budget (float): 预算金额
    
    返回:
        dict: 筛选结果 {'affordable': list, 'expensive': list}
    
    在这里实现你的代码
    """
    # TODO: 根据预算筛选商品
    # 提示：比较商品价格与预算
    pass


def find_best_deal(products):
    """
    找出性价比最高的商品（价格最低）
    
    参数:
        products (list): 商品列表
    
    返回:
        dict: 最便宜的商品信息
    
    在这里实现你的代码
    """
    # TODO: 找出价格最低的商品
    # 提示：使用min()函数和key参数
    pass


def price_range_filter(products, min_price, max_price):
    """
    根据价格范围筛选商品
    
    参数:
        products (list): 商品列表
        min_price (float): 最低价格
        max_price (float): 最高价格
    
    返回:
        list: 在价格范围内的商品列表
    
    在这里实现你的代码
    """
    # TODO: 筛选价格范围内的商品
    # 提示：使用链式比较 min_price <= price <= max_price
    pass


def string_sorter(strings, reverse=False):
    """
    对字符串列表进行排序
    
    参数:
        strings (list): 字符串列表
        reverse (bool): 是否逆序排列
    
    返回:
        list: 排序后的字符串列表
    
    在这里实现你的代码
    """
    # TODO: 对字符串进行排序
    # 提示：使用sorted()函数
    pass


def find_longest_string(strings):
    """
    找出最长的字符串
    
    参数:
        strings (list): 字符串列表
    
    返回:
        str: 最长的字符串
    
    在这里实现你的代码
    """
    # TODO: 找出最长的字符串
    # 提示：使用max()函数和len()作为key
    pass


def search_strings(strings, keyword, case_sensitive=False):
    """
    在字符串列表中搜索包含关键词的字符串
    
    参数:
        strings (list): 字符串列表
        keyword (str): 搜索关键词
        case_sensitive (bool): 是否区分大小写
    
    返回:
        list: 包含关键词的字符串列表
    
    在这里实现你的代码
    """
    # TODO: 搜索包含关键词的字符串
    # 提示：使用in运算符，考虑大小写问题
    pass


def validate_age(age):
    """
    验证年龄是否在合理范围内
    
    参数:
        age (int): 年龄
    
    返回:
        bool: 年龄是否有效 (0 < age <= 150)
    
    在这里实现你的代码
    """
    # TODO: 验证年龄范围
    # 提示：使用链式比较
    pass


def validate_email(email):
    """
    简单验证邮箱格式
    
    参数:
        email (str): 邮箱地址
    
    返回:
        bool: 邮箱格式是否有效
    
    在这里实现你的代码
    """
    # TODO: 简单验证邮箱格式
    # 提示：检查是否包含@和.，长度是否合理
    pass


def validate_password_strength(password):
    """
    验证密码强度
    
    参数:
        password (str): 密码
    
    返回:
        dict: 验证结果 {'valid': bool, 'strength': str, 'issues': list}
    
    密码要求:
        - 长度至少8位
        - 包含大写字母
        - 包含小写字母
        - 包含数字
    
    在这里实现你的代码
    """
    # TODO: 验证密码强度
    # 提示：检查各种条件，统计满足的条件数量
    pass


def number_range_checker(number, ranges):
    """
    检查数字属于哪个范围
    
    参数:
        number (float): 要检查的数字
        ranges (list): 范围列表，每个元素是 (min, max, label)
    
    返回:
        str: 数字所属的范围标签，如果不属于任何范围返回 'Unknown'
    
    在这里实现你的代码
    """
    # TODO: 检查数字属于哪个范围
    # 提示：遍历范围列表，使用链式比较
    pass


def test_functions():
    """
    测试所有函数的功能
    """
    print("=" * 50)
    print("Session03 练习题2：比较运算练习 - 测试")
    print("=" * 50)
    
    # 测试成绩等级判定
    print("\n1. 测试成绩等级判定:")
    test_scores = [95, 87, 76, 65, 45, 100, 0]
    for score in test_scores:
        try:
            grade = grade_classifier(score)
            print(f"  分数 {score}: 等级 {grade}")
        except Exception as e:
            print(f"  分数 {score} 判定错误: {e}")
    
    # 测试学生比较
    print("\n2. 测试学生比较:")
    student1 = {'name': '张三', 'score': 85}
    student2 = {'name': '李四', 'score': 92}
    try:
        comparison = compare_students(student1, student2)
        print(f"  {comparison}")
    except Exception as e:
        print(f"  学生比较错误: {e}")
    
    # 测试前N名学生
    print("\n3. 测试前N名学生:")
    students = [
        {'name': '张三', 'score': 85},
        {'name': '李四', 'score': 92},
        {'name': '王五', 'score': 78},
        {'name': '赵六', 'score': 96},
        {'name': '钱七', 'score': 88}
    ]
    try:
        top_students = find_top_students(students, 3)
        print("  前3名学生:")
        for i, student in enumerate(top_students, 1):
            print(f"    {i}. {student['name']}: {student['score']}分")
    except Exception as e:
        print(f"  查找前N名错误: {e}")
    
    # 测试班级成绩分析
    print("\n4. 测试班级成绩分析:")
    try:
        analysis = analyze_class_performance(students)
        print(f"  班级成绩分析: {analysis}")
    except Exception as e:
        print(f"  班级分析错误: {e}")
    
    # 测试商品价格比较
    print("\n5. 测试商品价格比较:")
    products = [
        {'name': '苹果', 'price': 8.5},
        {'name': '香蕉', 'price': 6.0},
        {'name': '橙子', 'price': 7.2},
        {'name': '葡萄', 'price': 12.0}
    ]
    budget = 8.0
    try:
        result = price_comparator(products, budget)
        print(f"  预算 {budget}元 的筛选结果:")
        print(f"    可购买: {[p['name'] for p in result['affordable']]}")
        print(f"    超预算: {[p['name'] for p in result['expensive']]}")
    except Exception as e:
        print(f"  价格比较错误: {e}")
    
    # 测试最佳优惠
    print("\n6. 测试最佳优惠:")
    try:
        best_deal = find_best_deal(products)
        print(f"  最便宜的商品: {best_deal['name']} ({best_deal['price']}元)")
    except Exception as e:
        print(f"  查找最佳优惠错误: {e}")
    
    # 测试价格范围筛选
    print("\n7. 测试价格范围筛选:")
    try:
        filtered = price_range_filter(products, 6.0, 8.0)
        print(f"  价格在6-8元的商品: {[p['name'] for p in filtered]}")
    except Exception as e:
        print(f"  价格范围筛选错误: {e}")
    
    # 测试字符串排序
    print("\n8. 测试字符串排序:")
    test_strings = ['banana', 'apple', 'cherry', 'date']
    try:
        sorted_strings = string_sorter(test_strings)
        print(f"  原列表: {test_strings}")
        print(f"  排序后: {sorted_strings}")
    except Exception as e:
        print(f"  字符串排序错误: {e}")
    
    # 测试最长字符串
    print("\n9. 测试最长字符串:")
    try:
        longest = find_longest_string(test_strings)
        print(f"  最长的字符串: '{longest}'")
    except Exception as e:
        print(f"  查找最长字符串错误: {e}")
    
    # 测试字符串搜索
    print("\n10. 测试字符串搜索:")
    try:
        search_result = search_strings(test_strings, 'a')
        print(f"  包含字母'a'的字符串: {search_result}")
    except Exception as e:
        print(f"  字符串搜索错误: {e}")
    
    # 测试数据验证
    print("\n11. 测试数据验证:")
    
    # 年龄验证
    test_ages = [25, 0, 150, 200, -5]
    for age in test_ages:
        try:
            valid = validate_age(age)
            print(f"  年龄 {age}: {'有效' if valid else '无效'}")
        except Exception as e:
            print(f"  年龄 {age} 验证错误: {e}")
    
    # 邮箱验证
    test_emails = ['user@example.com', 'invalid-email', 'test@test.', '@example.com']
    for email in test_emails:
        try:
            valid = validate_email(email)
            print(f"  邮箱 '{email}': {'有效' if valid else '无效'}")
        except Exception as e:
            print(f"  邮箱 '{email}' 验证错误: {e}")
    
    # 密码强度验证
    test_passwords = ['123456', 'Password', 'Password123', 'P@ssw0rd123']
    for password in test_passwords:
        try:
            result = validate_password_strength(password)
            print(f"  密码 '{password}': {result}")
        except Exception as e:
            print(f"  密码 '{password}' 验证错误: {e}")
    
    # 测试数字范围检查
    print("\n12. 测试数字范围检查:")
    ranges = [
        (0, 18, '未成年'),
        (18, 60, '成年人'),
        (60, 150, '老年人')
    ]
    test_numbers = [10, 25, 65, 200]
    for number in test_numbers:
        try:
            range_label = number_range_checker(number, ranges)
            print(f"  数字 {number}: {range_label}")
        except Exception as e:
            print(f"  数字 {number} 范围检查错误: {e}")
    
    print("\n" + "=" * 50)
    print("测试完成！请检查你的实现是否正确。")
    print("=" * 50)


def main():
    """
    主函数
    """
    print("Session03 练习题2：比较运算练习")
    print("\n请在上面的函数中实现你的代码，然后运行测试。")
    print("\n提示：")
    print("1. 熟练使用所有比较运算符 (==, !=, <, >, <=, >=)")
    print("2. 学会使用链式比较简化条件判断")
    print("3. 注意处理不同数据类型的比较")
    print("4. 考虑边界情况和异常输入")
    
    # 运行测试
    test_functions()


if __name__ == "__main__":
    main()