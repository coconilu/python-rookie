#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用演示模块

演示个人信息管理系统的各种功能和用法。
这个文件展示了如何使用项目中的各个模块和函数。

作者: Python教程团队
创建日期: 2024-12-19
"""

import sys
import os

# 添加父目录到路径，以便导入项目模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from user_manager import UserManager
from utils import (
    calculate_bmi, 
    get_age_group, 
    format_user_info,
    get_bmi_category,
    validate_email,
    validate_phone,
    print_header,
    print_separator
)
from constants import (
    APP_NAME,
    BMI_CATEGORIES,
    AGE_GROUPS,
    ICONS,
    SAMPLE_USERS
)
from sample_data import (
    BASIC_SAMPLE_USERS,
    generate_sample_user,
    analyze_sample_data
)


def demo_basic_data_types():
    """
    演示基本数据类型的使用
    """
    print_header("基本数据类型演示")
    
    # 字符串类型
    name = "张三"  # str
    print(f"📛 姓名: {name} (类型: {type(name).__name__})")
    
    # 整数类型
    age = 25  # int
    print(f"🎂 年龄: {age} (类型: {type(age).__name__})")
    
    # 浮点数类型
    height = 1.75  # float
    weight = 70.0  # float
    print(f"📏 身高: {height} (类型: {type(height).__name__})")
    print(f"⚖️  体重: {weight} (类型: {type(weight).__name__})")
    
    # 布尔类型
    is_student = False  # bool
    print(f"🎓 是否学生: {is_student} (类型: {type(is_student).__name__})")
    
    # 字符串类型（联系信息）
    phone = "13800138000"  # str
    email = "zhangsan@example.com"  # str
    print(f"📞 电话: {phone} (类型: {type(phone).__name__})")
    print(f"📧 邮箱: {email} (类型: {type(email).__name__})")
    
    print_separator()


def demo_type_conversion():
    """
    演示类型转换
    """
    print_header("类型转换演示")
    
    # 字符串转数字
    age_str = "25"
    age_int = int(age_str)
    print(f"字符串 '{age_str}' 转换为整数: {age_int}")
    
    height_str = "1.75"
    height_float = float(height_str)
    print(f"字符串 '{height_str}' 转换为浮点数: {height_float}")
    
    # 数字转字符串
    weight = 70.5
    weight_str = str(weight)
    print(f"浮点数 {weight} 转换为字符串: '{weight_str}'")
    
    # 布尔值转换
    student_input = "y"
    is_student = student_input.lower() in ['y', 'yes', '是', '1']
    print(f"输入 '{student_input}' 转换为布尔值: {is_student}")
    
    # 数字格式化
    bmi = 22.857142857142858
    bmi_formatted = f"{bmi:.1f}"
    print(f"BMI {bmi} 格式化为: {bmi_formatted}")
    
    print_separator()


def demo_string_operations():
    """
    演示字符串操作
    """
    print_header("字符串操作演示")
    
    name = "  张三  "
    email = "ZhangSan@Example.COM"
    
    # 字符串清理
    clean_name = name.strip()
    print(f"原始姓名: '{name}' -> 清理后: '{clean_name}'")
    
    # 大小写转换
    lower_email = email.lower()
    print(f"原始邮箱: {email} -> 小写: {lower_email}")
    
    # 字符串格式化
    age = 25
    height = 1.75
    formatted_info = f"姓名: {clean_name}, 年龄: {age}岁, 身高: {height:.2f}米"
    print(f"格式化信息: {formatted_info}")
    
    # 字符串检查
    phone = "13800138000"
    print(f"电话 '{phone}' 是否全为数字: {phone.isdigit()}")
    print(f"电话 '{phone}' 长度: {len(phone)}")
    
    # 字符串分割和连接
    full_name = "张 三"
    name_parts = full_name.split()
    joined_name = "".join(name_parts)
    print(f"姓名 '{full_name}' 分割: {name_parts} -> 连接: '{joined_name}'")
    
    print_separator()


def demo_calculations():
    """
    演示数值计算
    """
    print_header("数值计算演示")
    
    # BMI计算
    weight = 70.0
    height = 1.75
    bmi = calculate_bmi(weight, height)
    print(f"体重: {weight}kg, 身高: {height}m")
    print(f"BMI计算: {weight} / ({height}²) = {bmi}")
    
    # 年龄相关计算
    birth_year = 1998
    current_year = 2024
    age = current_year - birth_year
    print(f"出生年份: {birth_year}, 当前年份: {current_year}")
    print(f"年龄计算: {current_year} - {birth_year} = {age}岁")
    
    # 百分比计算
    students = 15
    total_users = 50
    percentage = (students / total_users) * 100
    print(f"学生人数: {students}, 总人数: {total_users}")
    print(f"学生比例: ({students} / {total_users}) × 100 = {percentage}%")
    
    # 平均值计算
    ages = [20, 25, 30, 22, 28]
    avg_age = sum(ages) / len(ages)
    print(f"年龄列表: {ages}")
    print(f"平均年龄: sum({ages}) / {len(ages)} = {avg_age:.1f}岁")
    
    print_separator()


def demo_data_validation():
    """
    演示数据验证
    """
    print_header("数据验证演示")
    
    # 年龄验证
    test_ages = [25, 0, 150, -5, "abc"]
    print("年龄验证测试:")
    for age in test_ages:
        try:
            if isinstance(age, int) and 0 < age < 150:
                result = "✅ 有效"
            else:
                result = "❌ 无效"
        except:
            result = "❌ 类型错误"
        print(f"  年龄 {age}: {result}")
    
    # 邮箱验证
    test_emails = [
        "valid@example.com",
        "invalid.email",
        "@example.com",
        "user@",
        "user@domain.c"
    ]
    print("\n邮箱验证测试:")
    for email in test_emails:
        is_valid = validate_email(email)
        result = "✅ 有效" if is_valid else "❌ 无效"
        print(f"  {email}: {result}")
    
    # 电话验证
    test_phones = [
        "13800138000",
        "138-0013-8000",
        "+86 138 0013 8000",
        "123",
        "abcdefghijk"
    ]
    print("\n电话验证测试:")
    for phone in test_phones:
        is_valid = validate_phone(phone)
        result = "✅ 有效" if is_valid else "❌ 无效"
        print(f"  {phone}: {result}")
    
    print_separator()


def demo_user_manager():
    """
    演示用户管理器的使用
    """
    print_header("用户管理器演示")
    
    # 创建用户管理器
    manager = UserManager()
    print(f"创建用户管理器，当前用户数: {manager.get_user_count()}")
    
    # 添加用户
    sample_user = {
        'name': '演示用户',
        'age': 25,
        'height': 1.70,
        'weight': 65.0,
        'is_student': True,
        'phone': '13700137000',
        'email': 'demo@example.com'
    }
    
    success = manager.add_user(sample_user)
    if success:
        print(f"✅ 成功添加用户: {sample_user['name']}")
    else:
        print(f"❌ 添加用户失败")
    
    print(f"添加后用户数: {manager.get_user_count()}")
    
    # 获取用户信息
    users = manager.get_all_users()
    if users:
        user = users[0]
        print(f"\n第一个用户信息:")
        print(f"  姓名: {user['name']}")
        print(f"  年龄: {user['age']}岁")
        print(f"  BMI: {user.get('bmi', 'N/A')}")
        print(f"  年龄组: {user.get('age_group', 'N/A')}")
    
    # 搜索用户
    search_results = manager.search_users(is_student=True)
    print(f"\n搜索学生用户，找到 {len(search_results)} 个结果")
    
    # 获取统计信息
    stats = manager.get_statistics()
    if stats:
        print(f"\n统计信息:")
        print(f"  平均年龄: {stats['age_stats']['avg_age']:.1f}岁")
        print(f"  学生比例: {stats['student_stats']['student_percentage']:.1f}%")
    
    print_separator()


def demo_constants_usage():
    """
    演示常量的使用
    """
    print_header("常量使用演示")
    
    # 应用信息常量
    print(f"应用名称: {APP_NAME}")
    
    # BMI分类常量
    print("\nBMI分类:")
    for category, (min_val, max_val) in BMI_CATEGORIES.items():
        print(f"  {category}: {min_val} - {max_val}")
    
    # 年龄组常量
    print("\n年龄组:")
    for group, (min_age, max_age) in AGE_GROUPS.items():
        print(f"  {group}: {min_age} - {max_age}岁")
    
    # 图标常量
    print("\n常用图标:")
    icon_examples = ['user', 'age', 'height', 'weight', 'student', 'phone', 'email']
    for icon_name in icon_examples:
        if icon_name in ICONS:
            print(f"  {icon_name}: {ICONS[icon_name]}")
    
    print_separator()


def demo_sample_data():
    """
    演示示例数据的使用
    """
    print_header("示例数据演示")
    
    # 显示基础示例数据
    print(f"基础示例数据 ({len(BASIC_SAMPLE_USERS)} 个用户):")
    for i, user in enumerate(BASIC_SAMPLE_USERS, 1):
        bmi = calculate_bmi(user['weight'], user['height'])
        age_group = get_age_group(user['age'])
        user_type = "学生" if user['is_student'] else "非学生"
        
        print(f"  {i}. {user['name']} - {user['age']}岁({age_group}), "
              f"BMI:{bmi:.1f}, {user_type}")
    
    # 生成新用户
    new_user = generate_sample_user("新用户", 30, 1.68, 62.0, False)
    print(f"\n生成的新用户:")
    print(f"  姓名: {new_user['name']}")
    print(f"  BMI: {new_user['bmi']}")
    print(f"  年龄组: {new_user['age_group']}")
    
    # 分析示例数据
    stats = analyze_sample_data()
    if stats:
        print(f"\n示例数据统计:")
        print(f"  总用户数: {stats['total_users']}")
        print(f"  平均年龄: {stats['age_stats']['avg']:.1f}岁")
        print(f"  学生比例: {stats['student_stats']['student_percentage']:.1f}%")
    
    print_separator()


def demo_error_handling():
    """
    演示错误处理
    """
    print_header("错误处理演示")
    
    # 类型转换错误
    print("类型转换错误处理:")
    invalid_inputs = ["abc", "", "25.5.5", "负数"]
    
    for input_val in invalid_inputs:
        try:
            age = int(input_val)
            print(f"  '{input_val}' -> {age} ✅")
        except ValueError as e:
            print(f"  '{input_val}' -> 转换失败: {type(e).__name__} ❌")
    
    # BMI计算错误
    print("\nBMI计算错误处理:")
    invalid_params = [(70, 0), (-10, 1.75), ("abc", 1.75)]
    
    for weight, height in invalid_params:
        try:
            bmi = calculate_bmi(weight, height)
            print(f"  体重:{weight}, 身高:{height} -> BMI:{bmi:.1f} ✅")
        except Exception as e:
            print(f"  体重:{weight}, 身高:{height} -> 计算失败: {type(e).__name__} ❌")
    
    # 用户管理器错误
    print("\n用户管理器错误处理:")
    manager = UserManager()
    
    # 尝试添加无效用户
    invalid_user = {
        'name': '',  # 空姓名
        'age': -5,   # 无效年龄
        'height': 0, # 无效身高
        'weight': 0, # 无效体重
        'is_student': 'maybe',  # 无效布尔值
        'phone': '123',  # 太短的电话
        'email': 'invalid'  # 无效邮箱
    }
    
    success = manager.add_user(invalid_user)
    if success:
        print(f"  添加无效用户: 成功 ✅")
    else:
        print(f"  添加无效用户: 失败（符合预期）❌")
    
    print_separator()


def demo_practical_examples():
    """
    演示实际应用示例
    """
    print_header("实际应用示例")
    
    # 示例1: 健康评估
    print("示例1: 健康评估系统")
    user_data = {
        'name': '健康测试者',
        'age': 35,
        'height': 1.72,
        'weight': 75.0,
        'is_student': False
    }
    
    bmi = calculate_bmi(user_data['weight'], user_data['height'])
    bmi_category = get_bmi_category(bmi)
    age_group = get_age_group(user_data['age'])
    
    print(f"  用户: {user_data['name']}")
    print(f"  BMI: {bmi:.1f} ({bmi_category})")
    print(f"  年龄组: {age_group}")
    
    # 健康建议
    if bmi < 18.5:
        advice = "建议增加营养摄入，适当增重"
    elif bmi < 24:
        advice = "体重正常，保持健康生活方式"
    elif bmi < 28:
        advice = "建议控制饮食，增加运动"
    else:
        advice = "建议咨询医生，制定减重计划"
    
    print(f"  健康建议: {advice}")
    
    # 示例2: 学生信息统计
    print("\n示例2: 学生信息统计")
    all_users = BASIC_SAMPLE_USERS + [
        {'name': '学生A', 'age': 20, 'height': 1.65, 'weight': 55, 'is_student': True},
        {'name': '学生B', 'age': 22, 'height': 1.70, 'weight': 60, 'is_student': True},
        {'name': '职员C', 'age': 30, 'height': 1.75, 'weight': 70, 'is_student': False}
    ]
    
    students = [user for user in all_users if user['is_student']]
    non_students = [user for user in all_users if not user['is_student']]
    
    print(f"  总用户数: {len(all_users)}")
    print(f"  学生数: {len(students)}")
    print(f"  非学生数: {len(non_students)}")
    print(f"  学生比例: {len(students)/len(all_users)*100:.1f}%")
    
    if students:
        avg_student_age = sum(user['age'] for user in students) / len(students)
        print(f"  学生平均年龄: {avg_student_age:.1f}岁")
    
    # 示例3: 数据格式化输出
    print("\n示例3: 数据格式化输出")
    sample_user = BASIC_SAMPLE_USERS[0]
    
    # 简单格式
    simple_format = f"{sample_user['name']} ({sample_user['age']}岁)"
    print(f"  简单格式: {simple_format}")
    
    # 详细格式
    bmi = calculate_bmi(sample_user['weight'], sample_user['height'])
    detailed_format = (
        f"{sample_user['name']} - {sample_user['age']}岁, "
        f"{sample_user['height']:.2f}m, {sample_user['weight']:.1f}kg, "
        f"BMI:{bmi:.1f}"
    )
    print(f"  详细格式: {detailed_format}")
    
    # 表格格式
    print(f"  表格格式:")
    print(f"    {'姓名':<10} {'年龄':<5} {'身高':<8} {'体重':<8} {'BMI':<6}")
    print(f"    {'-'*10} {'-'*5} {'-'*8} {'-'*8} {'-'*6}")
    for user in BASIC_SAMPLE_USERS[:3]:
        bmi = calculate_bmi(user['weight'], user['height'])
        print(f"    {user['name']:<10} {user['age']:<5} "
              f"{user['height']:<8.2f} {user['weight']:<8.1f} {bmi:<6.1f}")
    
    print_separator()


def run_all_demos():
    """
    运行所有演示
    """
    print("=" * 80)
    print("                个人信息管理系统 - 功能演示")
    print("=" * 80)
    print("\n这个演示将展示项目中使用的各种Python概念和技术")
    print("包括：变量、数据类型、类型转换、字符串操作、数值计算等")
    print("\n" + "=" * 80)
    
    # 运行各个演示
    demo_basic_data_types()
    demo_type_conversion()
    demo_string_operations()
    demo_calculations()
    demo_data_validation()
    demo_user_manager()
    demo_constants_usage()
    demo_sample_data()
    demo_error_handling()
    demo_practical_examples()
    
    print("=" * 80)
    print("                    演示完成")
    print("=" * 80)
    print("\n🎉 恭喜！你已经了解了个人信息管理系统的各种功能。")
    print("💡 这些演示展示了Python中变量与数据类型的实际应用。")
    print("📚 建议你尝试修改代码，实验不同的参数和场景。")
    print("🚀 准备好开始你自己的编程项目了吗？")


if __name__ == "__main__":
    # 运行完整演示
    run_all_demos()