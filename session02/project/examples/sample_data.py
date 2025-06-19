#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例数据模块

提供用于测试和演示的示例用户数据。
这些数据展示了不同类型的用户信息，帮助理解数据结构和类型。

作者: Python教程团队
创建日期: 2024-12-19
"""

from typing import List, Dict, Any
import sys
import os

# 添加父目录到路径，以便导入项目模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import calculate_bmi, get_age_group
from constants import USER_TYPES, BMI_CATEGORIES


# ==================== 基础示例数据 ====================

BASIC_SAMPLE_USERS = [
    {
        'name': '张三',
        'age': 25,
        'height': 1.75,
        'weight': 70.0,
        'is_student': False,
        'phone': '13800138000',
        'email': 'zhangsan@example.com'
    },
    {
        'name': '李四',
        'age': 20,
        'height': 1.68,
        'weight': 55.5,
        'is_student': True,
        'phone': '13900139000',
        'email': 'lisi@student.edu.cn'
    },
    {
        'name': 'Alice',
        'age': 28,
        'height': 1.65,
        'weight': 58.0,
        'is_student': False,
        'phone': '15800158000',
        'email': 'alice@company.com'
    }
]

# ==================== 扩展示例数据 ====================

EXTENDED_SAMPLE_USERS = [
    # 学生群体
    {
        'name': '王小明',
        'age': 19,
        'height': 1.72,
        'weight': 65.0,
        'is_student': True,
        'phone': '13700137000',
        'email': 'xiaoming@university.edu.cn'
    },
    {
        'name': '刘小红',
        'age': 21,
        'height': 1.60,
        'weight': 50.0,
        'is_student': True,
        'phone': '13600136000',
        'email': 'xiaohong@college.edu.cn'
    },
    {
        'name': 'Bob',
        'age': 22,
        'height': 1.78,
        'weight': 72.0,
        'is_student': True,
        'phone': '15900159000',
        'email': 'bob@student.edu'
    },
    
    # 职场人士
    {
        'name': '陈经理',
        'age': 35,
        'height': 1.70,
        'weight': 68.0,
        'is_student': False,
        'phone': '13500135000',
        'email': 'chen.manager@company.com'
    },
    {
        'name': 'Sarah',
        'age': 30,
        'height': 1.63,
        'weight': 55.0,
        'is_student': False,
        'phone': '18700187000',
        'email': 'sarah@tech.com'
    },
    {
        'name': '李工程师',
        'age': 27,
        'height': 1.76,
        'weight': 73.0,
        'is_student': False,
        'phone': '13400134000',
        'email': 'li.engineer@software.com'
    },
    
    # 不同年龄段
    {
        'name': '小张',
        'age': 16,
        'height': 1.65,
        'weight': 52.0,
        'is_student': True,
        'phone': '13300133000',
        'email': 'xiaozhang@highschool.edu.cn'
    },
    {
        'name': '老王',
        'age': 45,
        'height': 1.68,
        'weight': 75.0,
        'is_student': False,
        'phone': '13200132000',
        'email': 'laowang@business.com'
    },
    {
        'name': 'Emma',
        'age': 55,
        'height': 1.58,
        'weight': 60.0,
        'is_student': False,
        'phone': '18600186000',
        'email': 'emma@consulting.com'
    },
    
    # 不同BMI类型
    {
        'name': '瘦子小李',
        'age': 24,
        'height': 1.80,
        'weight': 58.0,  # BMI: 17.9 (偏瘦)
        'is_student': False,
        'phone': '13100131000',
        'email': 'skinny.li@example.com'
    },
    {
        'name': '胖子老张',
        'age': 40,
        'height': 1.70,
        'weight': 85.0,  # BMI: 29.4 (肥胖)
        'is_student': False,
        'phone': '13000130000',
        'email': 'fat.zhang@example.com'
    }
]

# ==================== 特殊测试数据 ====================

# 边界值测试数据
BOUNDARY_TEST_DATA = [
    {
        'name': '最小年龄',
        'age': 1,
        'height': 0.6,
        'weight': 15.0,
        'is_student': False,
        'phone': '12900129000',
        'email': 'min.age@test.com'
    },
    {
        'name': '最大年龄',
        'age': 120,
        'height': 1.50,
        'weight': 45.0,
        'is_student': False,
        'phone': '12800128000',
        'email': 'max.age@test.com'
    },
    {
        'name': '最高身高',
        'age': 25,
        'height': 2.20,
        'weight': 100.0,
        'is_student': False,
        'phone': '12700127000',
        'email': 'tall@test.com'
    },
    {
        'name': '最低身高',
        'age': 25,
        'height': 1.40,
        'weight': 40.0,
        'is_student': True,
        'phone': '12600126000',
        'email': 'short@test.com'
    }
]

# ==================== 数据生成函数 ====================

def generate_sample_user(name: str, age: int, height: float, weight: float, 
                        is_student: bool = False, phone: str = "", email: str = "") -> Dict[str, Any]:
    """
    生成示例用户数据
    
    Args:
        name (str): 姓名
        age (int): 年龄
        height (float): 身高
        weight (float): 体重
        is_student (bool): 是否学生
        phone (str): 电话
        email (str): 邮箱
        
    Returns:
        Dict[str, Any]: 用户信息字典
    """
    if not phone:
        phone = f"138{age:02d}{age*2:06d}"
    
    if not email:
        email_name = name.lower().replace(' ', '.')
        domain = "student.edu.cn" if is_student else "company.com"
        email = f"{email_name}@{domain}"
    
    user_data = {
        'name': name,
        'age': age,
        'height': height,
        'weight': weight,
        'is_student': is_student,
        'phone': phone,
        'email': email
    }
    
    # 添加计算字段
    user_data['bmi'] = calculate_bmi(weight, height)
    user_data['age_group'] = get_age_group(age)
    
    return user_data


def generate_random_users(count: int = 10) -> List[Dict[str, Any]]:
    """
    生成随机用户数据（模拟随机，实际是预定义的）
    
    Args:
        count (int): 生成用户数量
        
    Returns:
        List[Dict[str, Any]]: 用户列表
    """
    import random
    
    # 姓名池
    chinese_names = ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十',
                    '郑小明', '王小红', '李小华', '陈小丽', '刘小强', '黄小美']
    english_names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Emma', 'Frank', 
                    'Grace', 'Henry', 'Ivy', 'Jack', 'Kate', 'Leo']
    
    all_names = chinese_names + english_names
    
    users = []
    used_names = set()
    
    for i in range(min(count, len(all_names))):
        # 选择未使用的姓名
        available_names = [name for name in all_names if name not in used_names]
        if not available_names:
            break
            
        name = available_names[i % len(available_names)]
        used_names.add(name)
        
        # 生成其他属性
        age = 18 + (i * 3) % 50  # 18-67岁
        height = 1.50 + (i * 0.05) % 0.50  # 1.50-2.00米
        weight = 45 + (i * 5) % 50  # 45-95公斤
        is_student = age < 25 and (i % 3 == 0)  # 年轻人更可能是学生
        
        user = generate_sample_user(name, age, height, weight, is_student)
        users.append(user)
    
    return users


def get_users_by_category(category: str) -> List[Dict[str, Any]]:
    """
    根据类别获取用户数据
    
    Args:
        category (str): 类别名称
        
    Returns:
        List[Dict[str, Any]]: 对应类别的用户列表
    """
    all_users = BASIC_SAMPLE_USERS + EXTENDED_SAMPLE_USERS
    
    if category == 'students':
        return [user for user in all_users if user['is_student']]
    elif category == 'non_students':
        return [user for user in all_users if not user['is_student']]
    elif category == 'young':
        return [user for user in all_users if user['age'] < 25]
    elif category == 'adult':
        return [user for user in all_users if 25 <= user['age'] < 50]
    elif category == 'senior':
        return [user for user in all_users if user['age'] >= 50]
    elif category == 'basic':
        return BASIC_SAMPLE_USERS
    elif category == 'extended':
        return EXTENDED_SAMPLE_USERS
    elif category == 'boundary':
        return BOUNDARY_TEST_DATA
    else:
        return all_users


def analyze_sample_data() -> Dict[str, Any]:
    """
    分析示例数据的统计信息
    
    Returns:
        Dict[str, Any]: 统计信息
    """
    all_users = BASIC_SAMPLE_USERS + EXTENDED_SAMPLE_USERS
    
    if not all_users:
        return {}
    
    # 基本统计
    total_users = len(all_users)
    ages = [user['age'] for user in all_users]
    heights = [user['height'] for user in all_users]
    weights = [user['weight'] for user in all_users]
    
    # 计算BMI
    bmis = [calculate_bmi(user['weight'], user['height']) for user in all_users]
    
    # 学生统计
    students = [user for user in all_users if user['is_student']]
    student_count = len(students)
    
    # 年龄组统计
    age_groups = {}
    for user in all_users:
        group = get_age_group(user['age'])
        age_groups[group] = age_groups.get(group, 0) + 1
    
    # BMI分类统计
    bmi_stats = {}
    for bmi in bmis:
        for category, (min_bmi, max_bmi) in BMI_CATEGORIES.items():
            if min_bmi <= bmi < max_bmi:
                bmi_stats[category] = bmi_stats.get(category, 0) + 1
                break
    
    return {
        'total_users': total_users,
        'age_stats': {
            'min': min(ages),
            'max': max(ages),
            'avg': sum(ages) / len(ages)
        },
        'height_stats': {
            'min': min(heights),
            'max': max(heights),
            'avg': sum(heights) / len(heights)
        },
        'weight_stats': {
            'min': min(weights),
            'max': max(weights),
            'avg': sum(weights) / len(weights)
        },
        'bmi_stats': {
            'min': min(bmis),
            'max': max(bmis),
            'avg': sum(bmis) / len(bmis)
        },
        'student_stats': {
            'students': student_count,
            'non_students': total_users - student_count,
            'student_percentage': (student_count / total_users) * 100
        },
        'age_groups': age_groups,
        'bmi_categories': bmi_stats
    }


def print_sample_data_info():
    """
    打印示例数据信息
    """
    print("=" * 60)
    print("                示例数据信息")
    print("=" * 60)
    
    # 基础数据
    print(f"\n📊 基础示例数据: {len(BASIC_SAMPLE_USERS)} 个用户")
    for i, user in enumerate(BASIC_SAMPLE_USERS, 1):
        user_type = "学生" if user['is_student'] else "非学生"
        bmi = calculate_bmi(user['weight'], user['height'])
        print(f"   {i}. {user['name']} - {user['age']}岁, BMI:{bmi:.1f}, {user_type}")
    
    # 扩展数据
    print(f"\n📈 扩展示例数据: {len(EXTENDED_SAMPLE_USERS)} 个用户")
    
    # 统计信息
    stats = analyze_sample_data()
    if stats:
        print(f"\n📋 总体统计:")
        print(f"   总用户数: {stats['total_users']}")
        print(f"   年龄范围: {stats['age_stats']['min']}-{stats['age_stats']['max']}岁")
        print(f"   平均年龄: {stats['age_stats']['avg']:.1f}岁")
        print(f"   学生比例: {stats['student_stats']['student_percentage']:.1f}%")
        
        print(f"\n👥 年龄组分布:")
        for group, count in stats['age_groups'].items():
            percentage = (count / stats['total_users']) * 100
            print(f"   {group}: {count}人 ({percentage:.1f}%)")
        
        print(f"\n📊 BMI分类分布:")
        for category, count in stats['bmi_categories'].items():
            percentage = (count / stats['total_users']) * 100
            print(f"   {category}: {count}人 ({percentage:.1f}%)")
    
    print("\n" + "=" * 60)


def export_sample_data_to_text() -> str:
    """
    将示例数据导出为文本格式
    
    Returns:
        str: 文本格式的数据
    """
    lines = []
    lines.append("个人信息管理系统 - 示例数据")
    lines.append("=" * 50)
    
    all_users = BASIC_SAMPLE_USERS + EXTENDED_SAMPLE_USERS
    
    for i, user in enumerate(all_users, 1):
        lines.append(f"\n{i}. {user['name']}")
        lines.append(f"   年龄: {user['age']}岁 ({get_age_group(user['age'])})")
        lines.append(f"   身高: {user['height']:.2f}米")
        lines.append(f"   体重: {user['weight']:.1f}公斤")
        
        bmi = calculate_bmi(user['weight'], user['height'])
        bmi_category = ""
        for category, (min_bmi, max_bmi) in BMI_CATEGORIES.items():
            if min_bmi <= bmi < max_bmi:
                bmi_category = category
                break
        lines.append(f"   BMI: {bmi:.1f} ({bmi_category})")
        
        user_type = "学生" if user['is_student'] else "非学生"
        lines.append(f"   类型: {user_type}")
        lines.append(f"   电话: {user['phone']}")
        lines.append(f"   邮箱: {user['email']}")
    
    # 添加统计信息
    stats = analyze_sample_data()
    if stats:
        lines.append("\n" + "=" * 50)
        lines.append("统计信息")
        lines.append("=" * 50)
        lines.append(f"总用户数: {stats['total_users']}")
        lines.append(f"平均年龄: {stats['age_stats']['avg']:.1f}岁")
        lines.append(f"平均身高: {stats['height_stats']['avg']:.2f}米")
        lines.append(f"平均体重: {stats['weight_stats']['avg']:.1f}公斤")
        lines.append(f"平均BMI: {stats['bmi_stats']['avg']:.1f}")
        lines.append(f"学生比例: {stats['student_stats']['student_percentage']:.1f}%")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # 运行示例数据展示
    print_sample_data_info()
    
    print("\n" + "=" * 60)
    print("测试数据生成功能")
    print("=" * 60)
    
    # 测试生成随机用户
    random_users = generate_random_users(5)
    print(f"\n生成了 {len(random_users)} 个随机用户:")
    for user in random_users:
        print(f"  - {user['name']}: {user['age']}岁, BMI:{user['bmi']:.1f}")
    
    # 测试分类获取
    students = get_users_by_category('students')
    print(f"\n学生用户数量: {len(students)}")
    
    print("\n示例数据模块测试完成！")