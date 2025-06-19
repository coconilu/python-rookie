#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session01 练习题2：变量和数据类型练习 - 参考答案

这是练习题2的参考答案，展示了变量和数据类型的使用。
"""

def solution():
    """
    练习题2的参考解决方案
    """
    # 1. 创建变量存储学生信息
    student_name = "李明"
    student_age = 17
    student_height = 175.5
    is_enrolled = True
    
    # 2. 输出变量值和类型
    print("=== 学生信息 ===")
    print(f"姓名: {student_name} (类型: {type(student_name)})")
    print(f"年龄: {student_age} (类型: {type(student_age)})")
    print(f"身高: {student_height} (类型: {type(student_height)})")
    print(f"在校状态: {is_enrolled} (类型: {type(is_enrolled)})")
    
    # 3. 计算10年后的年龄
    future_age = student_age + 10
    
    # 4. 判断是否成年
    is_adult = student_age >= 18
    
    # 5. 输出计算结果
    print("\n=== 计算结果 ===")
    print(f"10年后年龄: {future_age}岁")
    print(f"是否成年: {is_adult}")


def solution_advanced():
    """
    进阶版本：更详细的信息处理
    """
    print("\n=== 进阶版本 ===")
    
    # 更多学生信息
    student_info = {
        "name": "王小红",
        "age": 19,
        "height": 162.3,
        "weight": 52.5,
        "is_enrolled": True,
        "grade": "大一",
        "major": "计算机科学"
    }
    
    # 输出详细信息
    print("╔═══════════════════════════════╗")
    print("║          学生档案             ║")
    print("╠═══════════════════════════════╣")
    
    for key, value in student_info.items():
        if key == "name":
            print(f"║ 姓名: {value:<20} ║")
        elif key == "age":
            print(f"║ 年龄: {value}岁{'':<17} ║")
        elif key == "height":
            print(f"║ 身高: {value}cm{'':<15} ║")
        elif key == "weight":
            print(f"║ 体重: {value}kg{'':<15} ║")
        elif key == "is_enrolled":
            status = "在校" if value else "离校"
            print(f"║ 状态: {status:<20} ║")
        elif key == "grade":
            print(f"║ 年级: {value:<20} ║")
        elif key == "major":
            print(f"║ 专业: {value:<18} ║")
    
    print("╚═══════════════════════════════╝")
    
    # 计算BMI
    height_m = student_info["height"] / 100  # 转换为米
    bmi = student_info["weight"] / (height_m ** 2)
    
    # BMI分类
    if bmi < 18.5:
        bmi_category = "偏瘦"
    elif bmi < 24:
        bmi_category = "正常"
    elif bmi < 28:
        bmi_category = "偏胖"
    else:
        bmi_category = "肥胖"
    
    print(f"\n健康指标：")
    print(f"BMI: {bmi:.1f} ({bmi_category})")
    
    # 年龄相关计算
    current_year = 2024
    birth_year = current_year - student_info["age"]
    retirement_age = 65
    years_to_retirement = retirement_age - student_info["age"]
    
    print(f"\n时间计算：")
    print(f"出生年份: {birth_year}年")
    print(f"距离退休还有: {years_to_retirement}年")
    
    # 类型转换示例
    print(f"\n类型转换示例：")
    age_str = str(student_info["age"])
    height_int = int(student_info["height"])
    weight_str = f"{student_info['weight']:.1f}"
    
    print(f"年龄转字符串: '{age_str}' (类型: {type(age_str)})")
    print(f"身高转整数: {height_int} (类型: {type(height_int)})")
    print(f"体重格式化: '{weight_str}' (类型: {type(weight_str)})")


if __name__ == "__main__":
    solution()
    solution_advanced()