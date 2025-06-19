#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个人信息管理系统 - 主程序

这是Session02的综合项目，展示了变量与数据类型的实际应用。
该系统可以录入、显示、管理个人信息，并提供基本的统计功能。

作者: Python教程团队
创建日期: 2024-12-19
"""

from user_manager import UserManager
from utils import (
    get_valid_input, 
    calculate_bmi, 
    get_age_group, 
    format_user_info,
    clear_screen,
    print_header,
    print_separator
)
from constants import (
    MENU_OPTIONS,
    WELCOME_MESSAGE,
    GOODBYE_MESSAGE,
    BMI_CATEGORIES
)


def main():
    """
    主程序入口
    """
    # 创建用户管理器实例
    user_manager = UserManager()
    
    # 显示欢迎信息
    clear_screen()
    print_header(WELCOME_MESSAGE)
    
    # 主程序循环
    while True:
        try:
            # 显示主菜单
            show_main_menu()
            
            # 获取用户选择
            choice = get_user_choice()
            
            # 处理用户选择
            if choice == 1:
                add_new_user(user_manager)
            elif choice == 2:
                display_user_info(user_manager)
            elif choice == 3:
                show_statistics(user_manager)
            elif choice == 4:
                search_users(user_manager)
            elif choice == 5:
                list_all_users(user_manager)
            elif choice == 6:
                print_header(GOODBYE_MESSAGE)
                break
            else:
                print("❌ 无效选择，请重新输入！")
            
            # 等待用户按键继续
            if choice != 6:
                input("\n按回车键继续...")
                
        except KeyboardInterrupt:
            print("\n\n👋 程序被用户中断，再见！")
            break
        except Exception as e:
            print(f"\n❌ 程序出现错误: {e}")
            input("按回车键继续...")


def show_main_menu():
    """
    显示主菜单
    """
    clear_screen()
    print_header("个人信息管理系统")
    
    print("📋 请选择操作：")
    for key, value in MENU_OPTIONS.items():
        print(f"   {key}. {value}")
    
    print_separator()


def get_user_choice():
    """
    获取用户菜单选择
    
    Returns:
        int: 用户选择的菜单项
    """
    while True:
        try:
            choice = int(input("请输入选择 (1-6): ").strip())
            if 1 <= choice <= 6:
                return choice
            else:
                print("❌ 请输入1-6之间的数字")
        except ValueError:
            print("❌ 请输入有效的数字")


def add_new_user(user_manager):
    """
    添加新用户
    
    Args:
        user_manager (UserManager): 用户管理器实例
    """
    clear_screen()
    print_header("录入新用户信息")
    
    try:
        # 获取用户基本信息
        print("📝 请输入用户信息：")
        
        # 姓名
        name = get_valid_input(
            "请输入姓名: ",
            str,
            lambda x: len(x.strip()) > 0,
            "姓名不能为空"
        ).strip()
        
        # 年龄
        age = get_valid_input(
            "请输入年龄: ",
            int,
            lambda x: 0 < x < 150,
            "年龄必须在1-149之间"
        )
        
        # 身高
        height = get_valid_input(
            "请输入身高 (米): ",
            float,
            lambda x: 0.5 < x < 3.0,
            "身高必须在0.5-3.0米之间"
        )
        
        # 体重
        weight = get_valid_input(
            "请输入体重 (公斤): ",
            float,
            lambda x: 10 < x < 500,
            "体重必须在10-500公斤之间"
        )
        
        # 是否学生
        is_student_input = input("是否为学生 (y/n): ").strip().lower()
        is_student = is_student_input in ['y', 'yes', '是', '1', 'true']
        
        # 联系电话
        phone = get_valid_input(
            "请输入联系电话: ",
            str,
            lambda x: len(x.strip()) >= 8,
            "电话号码长度至少8位"
        ).strip()
        
        # 邮箱地址
        email = get_valid_input(
            "请输入邮箱地址: ",
            str,
            lambda x: '@' in x and '.' in x.split('@')[-1],
            "请输入有效的邮箱地址"
        ).strip()
        
        # 创建用户信息字典
        user_info = {
            'name': name,
            'age': age,
            'height': height,
            'weight': weight,
            'is_student': is_student,
            'phone': phone,
            'email': email
        }
        
        # 添加用户
        user_manager.add_user(user_info)
        
        print("\n✅ 用户信息录入成功！")
        
        # 显示录入的信息
        print("\n📋 录入的信息：")
        display_single_user(user_info)
        
    except Exception as e:
        print(f"\n❌ 录入失败: {e}")


def display_user_info(user_manager):
    """
    显示用户信息
    
    Args:
        user_manager (UserManager): 用户管理器实例
    """
    clear_screen()
    print_header("显示用户信息")
    
    users = user_manager.get_all_users()
    
    if not users:
        print("📭 暂无用户信息")
        return
    
    if len(users) == 1:
        # 只有一个用户，直接显示
        display_single_user(users[0])
    else:
        # 多个用户，让用户选择
        print(f"📊 共有 {len(users)} 个用户，请选择要显示的用户：")
        
        for i, user in enumerate(users, 1):
            print(f"   {i}. {user['name']} ({user['age']}岁)")
        
        try:
            choice = int(input(f"\n请选择用户 (1-{len(users)}): "))
            if 1 <= choice <= len(users):
                display_single_user(users[choice - 1])
            else:
                print("❌ 无效选择")
        except ValueError:
            print("❌ 请输入有效的数字")


def display_single_user(user_info):
    """
    显示单个用户的详细信息
    
    Args:
        user_info (dict): 用户信息字典
    """
    print_separator()
    print("👤 用户详细信息")
    print_separator()
    
    # 基本信息
    print(f"📛 姓名: {user_info['name']}")
    print(f"🎂 年龄: {user_info['age']}岁 ({get_age_group(user_info['age'])})")
    print(f"📏 身高: {user_info['height']:.2f}米")
    print(f"⚖️  体重: {user_info['weight']:.1f}公斤")
    
    # 计算BMI
    bmi = calculate_bmi(user_info['weight'], user_info['height'])
    bmi_category = get_bmi_category(bmi)
    print(f"📊 BMI指数: {bmi:.1f} ({bmi_category})")
    
    # 其他信息
    student_status = "学生" if user_info['is_student'] else "非学生"
    print(f"🎓 用户类型: {student_status}")
    print(f"📞 联系电话: {user_info['phone']}")
    print(f"📧 邮箱地址: {user_info['email']}")
    
    print_separator()


def get_bmi_category(bmi):
    """
    根据BMI值获取分类
    
    Args:
        bmi (float): BMI值
        
    Returns:
        str: BMI分类
    """
    for category, (min_bmi, max_bmi) in BMI_CATEGORIES.items():
        if min_bmi <= bmi < max_bmi:
            return category
    return "未知"


def show_statistics(user_manager):
    """
    显示统计信息
    
    Args:
        user_manager (UserManager): 用户管理器实例
    """
    clear_screen()
    print_header("统计信息")
    
    users = user_manager.get_all_users()
    
    if not users:
        print("📭 暂无用户数据进行统计")
        return
    
    total_users = len(users)
    
    # 基本统计
    print(f"👥 用户总数: {total_users}")
    
    # 年龄统计
    ages = [user['age'] for user in users]
    avg_age = sum(ages) / len(ages)
    min_age = min(ages)
    max_age = max(ages)
    
    print(f"\n🎂 年龄统计:")
    print(f"   平均年龄: {avg_age:.1f}岁")
    print(f"   最小年龄: {min_age}岁")
    print(f"   最大年龄: {max_age}岁")
    
    # 身高体重统计
    heights = [user['height'] for user in users]
    weights = [user['weight'] for user in users]
    
    avg_height = sum(heights) / len(heights)
    avg_weight = sum(weights) / len(weights)
    
    print(f"\n📏 身高统计:")
    print(f"   平均身高: {avg_height:.2f}米")
    print(f"   最高身高: {max(heights):.2f}米")
    print(f"   最低身高: {min(heights):.2f}米")
    
    print(f"\n⚖️  体重统计:")
    print(f"   平均体重: {avg_weight:.1f}公斤")
    print(f"   最大体重: {max(weights):.1f}公斤")
    print(f"   最小体重: {min(weights):.1f}公斤")
    
    # 学生比例统计
    students = [user for user in users if user['is_student']]
    student_count = len(students)
    student_percentage = (student_count / total_users) * 100
    
    print(f"\n🎓 用户类型统计:")
    print(f"   学生: {student_count}人 ({student_percentage:.1f}%)")
    print(f"   非学生: {total_users - student_count}人 ({100 - student_percentage:.1f}%)")
    
    # BMI统计
    bmis = [calculate_bmi(user['weight'], user['height']) for user in users]
    avg_bmi = sum(bmis) / len(bmis)
    
    print(f"\n📊 BMI统计:")
    print(f"   平均BMI: {avg_bmi:.1f}")
    
    # BMI分类统计
    bmi_stats = {}
    for bmi in bmis:
        category = get_bmi_category(bmi)
        bmi_stats[category] = bmi_stats.get(category, 0) + 1
    
    print("   BMI分类分布:")
    for category, count in bmi_stats.items():
        percentage = (count / total_users) * 100
        print(f"     {category}: {count}人 ({percentage:.1f}%)")


def search_users(user_manager):
    """
    搜索用户
    
    Args:
        user_manager (UserManager): 用户管理器实例
    """
    clear_screen()
    print_header("搜索用户")
    
    users = user_manager.get_all_users()
    
    if not users:
        print("📭 暂无用户数据")
        return
    
    print("🔍 搜索选项:")
    print("   1. 按姓名搜索")
    print("   2. 按年龄范围搜索")
    print("   3. 按用户类型搜索")
    
    try:
        choice = int(input("\n请选择搜索方式 (1-3): "))
        
        if choice == 1:
            search_by_name(users)
        elif choice == 2:
            search_by_age_range(users)
        elif choice == 3:
            search_by_user_type(users)
        else:
            print("❌ 无效选择")
            
    except ValueError:
        print("❌ 请输入有效的数字")


def search_by_name(users):
    """
    按姓名搜索用户
    
    Args:
        users (list): 用户列表
    """
    name_query = input("请输入要搜索的姓名（支持部分匹配）: ").strip().lower()
    
    if not name_query:
        print("❌ 搜索关键词不能为空")
        return
    
    results = [user for user in users if name_query in user['name'].lower()]
    
    display_search_results(results, f"姓名包含 '{name_query}'")


def search_by_age_range(users):
    """
    按年龄范围搜索用户
    
    Args:
        users (list): 用户列表
    """
    try:
        min_age = int(input("请输入最小年龄: "))
        max_age = int(input("请输入最大年龄: "))
        
        if min_age > max_age:
            print("❌ 最小年龄不能大于最大年龄")
            return
        
        results = [user for user in users if min_age <= user['age'] <= max_age]
        
        display_search_results(results, f"年龄在 {min_age}-{max_age} 岁之间")
        
    except ValueError:
        print("❌ 请输入有效的年龄数字")


def search_by_user_type(users):
    """
    按用户类型搜索用户
    
    Args:
        users (list): 用户列表
    """
    print("请选择用户类型:")
    print("   1. 学生")
    print("   2. 非学生")
    
    try:
        choice = int(input("请选择 (1-2): "))
        
        if choice == 1:
            results = [user for user in users if user['is_student']]
            display_search_results(results, "学生")
        elif choice == 2:
            results = [user for user in users if not user['is_student']]
            display_search_results(results, "非学生")
        else:
            print("❌ 无效选择")
            
    except ValueError:
        print("❌ 请输入有效的数字")


def display_search_results(results, search_criteria):
    """
    显示搜索结果
    
    Args:
        results (list): 搜索结果列表
        search_criteria (str): 搜索条件描述
    """
    print(f"\n🔍 搜索条件: {search_criteria}")
    print(f"📊 找到 {len(results)} 个匹配的用户")
    
    if not results:
        print("😔 没有找到匹配的用户")
        return
    
    print_separator()
    
    for i, user in enumerate(results, 1):
        print(f"\n{i}. {user['name']}")
        print(f"   年龄: {user['age']}岁")
        print(f"   身高: {user['height']:.2f}米")
        print(f"   体重: {user['weight']:.1f}公斤")
        print(f"   类型: {'学生' if user['is_student'] else '非学生'}")
        print(f"   电话: {user['phone']}")
        print(f"   邮箱: {user['email']}")


def list_all_users(user_manager):
    """
    列出所有用户
    
    Args:
        user_manager (UserManager): 用户管理器实例
    """
    clear_screen()
    print_header("所有用户列表")
    
    users = user_manager.get_all_users()
    
    if not users:
        print("📭 暂无用户数据")
        return
    
    print(f"👥 共有 {len(users)} 个用户：")
    print_separator()
    
    for i, user in enumerate(users, 1):
        bmi = calculate_bmi(user['weight'], user['height'])
        age_group = get_age_group(user['age'])
        user_type = "学生" if user['is_student'] else "非学生"
        
        print(f"{i:2d}. {user['name']:<10} | {user['age']:2d}岁({age_group}) | "
              f"{user['height']:.2f}m | {user['weight']:4.1f}kg | "
              f"BMI:{bmi:4.1f} | {user_type}")


if __name__ == "__main__":
    main()