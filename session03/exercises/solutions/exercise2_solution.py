#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session03 练习题2解答：比较运算练习

这个文件包含了exercise2.py中所有练习题的参考解答。
学习者可以参考这些解答来检查自己的实现，
但建议先独立完成练习再查看解答。
"""

import math


def grade_classifier(score):
    """
    根据分数判定成绩等级
    """
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


def compare_students(student1, student2):
    """
    比较两个学生的成绩
    """
    name1, score1 = student1['name'], student1['score']
    name2, score2 = student2['name'], student2['score']
    
    if score1 > score2:
        return f"{name1}的成绩({score1})高于{name2}的成绩({score2})"
    elif score1 < score2:
        return f"{name2}的成绩({score2})高于{name1}的成绩({score1})"
    else:
        return f"{name1}和{name2}的成绩相同({score1})"


def find_top_students(students, top_n=3):
    """
    找出成绩最好的前N名学生
    """
    # 按成绩从高到低排序
    sorted_students = sorted(students, key=lambda x: x['score'], reverse=True)
    return sorted_students[:top_n]


def analyze_class_performance(students):
    """
    分析班级成绩表现
    """
    grade_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    
    for student in students:
        grade = grade_classifier(student['score'])
        grade_counts[grade] += 1
    
    return grade_counts


def price_comparator(products, budget):
    """
    根据预算筛选商品
    """
    affordable = []
    expensive = []
    
    for product in products:
        if product['price'] <= budget:
            affordable.append(product)
        else:
            expensive.append(product)
    
    return {'affordable': affordable, 'expensive': expensive}


def find_best_deal(products):
    """
    找出性价比最高的商品（价格最低）
    """
    if not products:
        return None
    
    return min(products, key=lambda x: x['price'])


def price_range_filter(products, min_price, max_price):
    """
    根据价格范围筛选商品
    """
    filtered_products = []
    
    for product in products:
        if min_price <= product['price'] <= max_price:
            filtered_products.append(product)
    
    return filtered_products


def string_sorter(strings, reverse=False):
    """
    对字符串列表进行排序
    """
    return sorted(strings, reverse=reverse)


def find_longest_string(strings):
    """
    找出最长的字符串
    """
    if not strings:
        return ""
    
    return max(strings, key=len)


def search_strings(strings, keyword, case_sensitive=False):
    """
    在字符串列表中搜索包含关键词的字符串
    """
    result = []
    
    for string in strings:
        if case_sensitive:
            if keyword in string:
                result.append(string)
        else:
            if keyword.lower() in string.lower():
                result.append(string)
    
    return result


def validate_age(age):
    """
    验证年龄是否在合理范围内
    """
    return 0 < age <= 150


def validate_email(email):
    """
    简单验证邮箱格式
    """
    if not isinstance(email, str) or len(email) < 5:
        return False
    
    # 检查是否包含@和.
    if '@' not in email or '.' not in email:
        return False
    
    # 检查@的位置
    at_index = email.find('@')
    if at_index <= 0 or at_index >= len(email) - 1:
        return False
    
    # 检查@后面是否有.
    domain_part = email[at_index + 1:]
    if '.' not in domain_part:
        return False
    
    return True


def validate_password_strength(password):
    """
    验证密码强度
    """
    issues = []
    strength_score = 0
    
    # 检查长度
    if len(password) >= 8:
        strength_score += 1
    else:
        issues.append("密码长度至少8位")
    
    # 检查大写字母
    has_upper = any(c.isupper() for c in password)
    if has_upper:
        strength_score += 1
    else:
        issues.append("需要包含大写字母")
    
    # 检查小写字母
    has_lower = any(c.islower() for c in password)
    if has_lower:
        strength_score += 1
    else:
        issues.append("需要包含小写字母")
    
    # 检查数字
    has_digit = any(c.isdigit() for c in password)
    if has_digit:
        strength_score += 1
    else:
        issues.append("需要包含数字")
    
    # 确定强度等级
    if strength_score == 4:
        strength = "强"
    elif strength_score >= 2:
        strength = "中等"
    else:
        strength = "弱"
    
    return {
        'valid': strength_score >= 3,
        'strength': strength,
        'issues': issues
    }


def number_range_checker(number, ranges):
    """
    检查数字属于哪个范围
    """
    for min_val, max_val, label in ranges:
        if min_val <= number <= max_val:
            return label
    
    return 'Unknown'


def advanced_student_analyzer(students):
    """
    高级学生成绩分析器
    """
    if not students:
        return {"error": "没有学生数据"}
    
    scores = [student['score'] for student in students]
    
    # 基本统计
    total_students = len(students)
    average_score = sum(scores) / total_students
    highest_score = max(scores)
    lowest_score = min(scores)
    
    # 找出最高分和最低分的学生
    top_student = max(students, key=lambda x: x['score'])
    bottom_student = min(students, key=lambda x: x['score'])
    
    # 计算及格率
    passing_students = [s for s in students if s['score'] >= 60]
    pass_rate = len(passing_students) / total_students * 100
    
    # 等级分布
    grade_distribution = analyze_class_performance(students)
    
    return {
        "total_students": total_students,
        "average_score": round(average_score, 2),
        "highest_score": highest_score,
        "lowest_score": lowest_score,
        "top_student": top_student,
        "bottom_student": bottom_student,
        "pass_rate": round(pass_rate, 2),
        "grade_distribution": grade_distribution
    }


def smart_product_filter(products, criteria):
    """
    智能商品筛选器
    """
    filtered = products.copy()
    
    # 价格范围筛选
    if 'min_price' in criteria and 'max_price' in criteria:
        filtered = [p for p in filtered 
                   if criteria['min_price'] <= p['price'] <= criteria['max_price']]
    elif 'max_price' in criteria:
        filtered = [p for p in filtered if p['price'] <= criteria['max_price']]
    elif 'min_price' in criteria:
        filtered = [p for p in filtered if p['price'] >= criteria['min_price']]
    
    # 名称关键词筛选
    if 'keyword' in criteria:
        keyword = criteria['keyword'].lower()
        filtered = [p for p in filtered if keyword in p['name'].lower()]
    
    # 排序
    if 'sort_by' in criteria:
        if criteria['sort_by'] == 'price_asc':
            filtered.sort(key=lambda x: x['price'])
        elif criteria['sort_by'] == 'price_desc':
            filtered.sort(key=lambda x: x['price'], reverse=True)
        elif criteria['sort_by'] == 'name':
            filtered.sort(key=lambda x: x['name'])
    
    return filtered


def text_analyzer(text):
    """
    文本分析器
    """
    if not text:
        return {"error": "文本不能为空"}
    
    # 基本统计
    char_count = len(text)
    word_count = len(text.split())
    line_count = text.count('\n') + 1
    
    # 字符类型统计
    letter_count = sum(1 for c in text if c.isalpha())
    digit_count = sum(1 for c in text if c.isdigit())
    space_count = sum(1 for c in text if c.isspace())
    
    # 大小写统计
    upper_count = sum(1 for c in text if c.isupper())
    lower_count = sum(1 for c in text if c.islower())
    
    return {
        "char_count": char_count,
        "word_count": word_count,
        "line_count": line_count,
        "letter_count": letter_count,
        "digit_count": digit_count,
        "space_count": space_count,
        "upper_count": upper_count,
        "lower_count": lower_count
    }


def data_validator(data, rules):
    """
    通用数据验证器
    """
    errors = []
    warnings = []
    
    for field, rule in rules.items():
        if field not in data:
            if rule.get('required', False):
                errors.append(f"缺少必需字段: {field}")
            continue
        
        value = data[field]
        
        # 类型检查
        if 'type' in rule:
            expected_type = rule['type']
            if not isinstance(value, expected_type):
                errors.append(f"字段 {field} 类型错误，期望 {expected_type.__name__}")
                continue
        
        # 范围检查（数值）
        if isinstance(value, (int, float)):
            if 'min' in rule and value < rule['min']:
                errors.append(f"字段 {field} 值 {value} 小于最小值 {rule['min']}")
            if 'max' in rule and value > rule['max']:
                errors.append(f"字段 {field} 值 {value} 大于最大值 {rule['max']}")
        
        # 长度检查（字符串）
        if isinstance(value, str):
            if 'min_length' in rule and len(value) < rule['min_length']:
                errors.append(f"字段 {field} 长度 {len(value)} 小于最小长度 {rule['min_length']}")
            if 'max_length' in rule and len(value) > rule['max_length']:
                errors.append(f"字段 {field} 长度 {len(value)} 大于最大长度 {rule['max_length']}")
        
        # 模式检查
        if 'pattern' in rule and isinstance(value, str):
            pattern = rule['pattern']
            if pattern == 'email' and not validate_email(value):
                errors.append(f"字段 {field} 不是有效的邮箱格式")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }


def main():
    """
    主函数 - 演示所有解答
    """
    print("Session03 练习题2解答演示")
    print("=" * 50)
    
    # 演示成绩等级判定
    print("\n1. 成绩等级判定演示:")
    test_scores = [95, 87, 76, 65, 45]
    for score in test_scores:
        grade = grade_classifier(score)
        print(f"  分数 {score}: 等级 {grade}")
    
    # 演示学生比较
    print("\n2. 学生比较演示:")
    student1 = {'name': '张三', 'score': 85}
    student2 = {'name': '李四', 'score': 92}
    comparison = compare_students(student1, student2)
    print(f"  {comparison}")
    
    # 演示前N名学生
    print("\n3. 前N名学生演示:")
    students = [
        {'name': '张三', 'score': 85},
        {'name': '李四', 'score': 92},
        {'name': '王五', 'score': 78},
        {'name': '赵六', 'score': 96},
        {'name': '钱七', 'score': 88}
    ]
    top_students = find_top_students(students, 3)
    print("  前3名学生:")
    for i, student in enumerate(top_students, 1):
        print(f"    {i}. {student['name']}: {student['score']}分")
    
    # 演示班级成绩分析
    print("\n4. 班级成绩分析演示:")
    analysis = analyze_class_performance(students)
    print(f"  班级成绩分析: {analysis}")
    
    # 演示高级学生分析
    print("\n5. 高级学生分析演示:")
    advanced_analysis = advanced_student_analyzer(students)
    print(f"  详细分析: {advanced_analysis}")
    
    # 演示商品价格比较
    print("\n6. 商品价格比较演示:")
    products = [
        {'name': '苹果', 'price': 8.5},
        {'name': '香蕉', 'price': 6.0},
        {'name': '橙子', 'price': 7.2},
        {'name': '葡萄', 'price': 12.0}
    ]
    budget = 8.0
    result = price_comparator(products, budget)
    print(f"  预算 {budget}元 的筛选结果:")
    print(f"    可购买: {[p['name'] for p in result['affordable']]}")
    print(f"    超预算: {[p['name'] for p in result['expensive']]}")
    
    # 演示智能商品筛选
    print("\n7. 智能商品筛选演示:")
    criteria = {
        'min_price': 6.0,
        'max_price': 10.0,
        'sort_by': 'price_asc'
    }
    filtered = smart_product_filter(products, criteria)
    print(f"  筛选条件: {criteria}")
    print(f"  筛选结果: {[(p['name'], p['price']) for p in filtered]}")
    
    # 演示字符串操作
    print("\n8. 字符串操作演示:")
    test_strings = ['banana', 'apple', 'cherry', 'date']
    sorted_strings = string_sorter(test_strings)
    longest = find_longest_string(test_strings)
    search_result = search_strings(test_strings, 'a')
    
    print(f"  原列表: {test_strings}")
    print(f"  排序后: {sorted_strings}")
    print(f"  最长字符串: '{longest}'")
    print(f"  包含'a'的字符串: {search_result}")
    
    # 演示数据验证
    print("\n9. 数据验证演示:")
    
    # 年龄验证
    test_ages = [25, 0, 150, 200, -5]
    print("  年龄验证:")
    for age in test_ages:
        valid = validate_age(age)
        print(f"    年龄 {age}: {'有效' if valid else '无效'}")
    
    # 邮箱验证
    test_emails = ['user@example.com', 'invalid-email', 'test@test.', '@example.com']
    print("  邮箱验证:")
    for email in test_emails:
        valid = validate_email(email)
        print(f"    邮箱 '{email}': {'有效' if valid else '无效'}")
    
    # 密码强度验证
    test_passwords = ['123456', 'Password', 'Password123', 'P@ssw0rd123']
    print("  密码强度验证:")
    for password in test_passwords:
        result = validate_password_strength(password)
        print(f"    密码 '{password}': {result}")
    
    # 演示文本分析
    print("\n10. 文本分析演示:")
    sample_text = "Hello World!\nThis is a sample text with 123 numbers."
    text_stats = text_analyzer(sample_text)
    print(f"  文本: {repr(sample_text)}")
    print(f"  分析结果: {text_stats}")
    
    print("\n" + "=" * 50)
    print("解答演示完成！")


if __name__ == "__main__":
    main()