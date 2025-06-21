#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session04 练习题1：条件语句练习

本练习主要考查条件语句的使用，包括：
1. 基本的if-else语句
2. 多条件判断（if-elif-else）
3. 嵌套条件语句
4. 逻辑运算符的使用

请在每个函数中实现相应的功能，确保代码能够正确运行。

作者: Python教程团队
创建日期: 2024-12-21
"""


def check_age_category(age):
    """
    练习1：年龄分类

    根据年龄判断人员类别：
    - 0-2岁：婴儿
    - 3-12岁：儿童
    - 13-17岁：青少年
    - 18-59岁：成年人
    - 60岁及以上：老年人
    - 负数或超过150：无效年龄

    参数:
        age (int): 年龄

    返回:
        str: 年龄类别

    示例:
        >>> check_age_category(5)
        '儿童'
        >>> check_age_category(25)
        '成年人'
        >>> check_age_category(-1)
        '无效年龄'
    """
    # 在这里编写你的代码
    pass


def calculate_grade(score):
    """
    练习2：成绩等级计算

    根据分数计算等级和评价：
    - 90-100分：A等级，优秀
    - 80-89分：B等级，良好
    - 70-79分：C等级，中等
    - 60-69分：D等级，及格
    - 0-59分：F等级，不及格
    - 其他：无效分数

    参数:
        score (int): 分数

    返回:
        tuple: (等级, 评价)

    示例:
        >>> calculate_grade(95)
        ('A', '优秀')
        >>> calculate_grade(75)
        ('C', '中等')
        >>> calculate_grade(-10)
        ('无效', '无效分数')
    """
    # 在这里编写你的代码
    pass


def check_triangle_type(a, b, c):
    """
    练习3：三角形类型判断

    根据三边长度判断三角形类型：
    - 首先检查是否能构成三角形（任意两边之和大于第三边）
    - 如果能构成三角形，判断类型：
      * 等边三角形：三边相等
      * 等腰三角形：两边相等
      * 直角三角形：满足勾股定理（a²+b²=c²）
      * 普通三角形：其他情况
    - 如果不能构成三角形，返回"不是三角形"

    参数:
        a, b, c (float): 三角形的三边长度

    返回:
        str: 三角形类型

    示例:
        >>> check_triangle_type(3, 3, 3)
        '等边三角形'
        >>> check_triangle_type(3, 4, 5)
        '直角三角形'
        >>> check_triangle_type(1, 2, 5)
        '不是三角形'
    """
    # 在这里编写你的代码
    pass


def calculate_shipping_cost(weight, distance, is_express=False):
    """
    练习4：快递费用计算

    根据重量、距离和是否加急计算快递费用：

    基础费用规则：
    - 重量 <= 1kg：10元
    - 重量 1-5kg：10 + (重量-1) * 5元
    - 重量 > 5kg：10 + 4*5 + (重量-5) * 3元

    距离附加费：
    - 距离 <= 100km：无附加费
    - 距离 100-500km：+5元
    - 距离 > 500km：+15元

    加急服务：
    - 如果选择加急，总费用 * 1.5

    参数:
        weight (float): 重量（kg）
        distance (int): 距离（km）
        is_express (bool): 是否加急

    返回:
        float: 快递费用（保留2位小数）

    示例:
        >>> calculate_shipping_cost(0.5, 50)
        10.0
        >>> calculate_shipping_cost(3, 200)
        25.0
        >>> calculate_shipping_cost(2, 100, True)
        22.5
    """
    # 在这里编写你的代码
    pass


def check_password_strength(password):
    """
    练习5：密码强度检查

    检查密码强度并返回强度等级和建议：

    强度规则：
    - 长度 >= 8
    - 包含大写字母
    - 包含小写字母
    - 包含数字
    - 包含特殊字符（!@#$%^&*）

    强度等级：
    - 满足5个条件：强
    - 满足4个条件：中等
    - 满足3个条件：弱
    - 满足少于3个条件：很弱

    参数:
        password (str): 密码

    返回:
        tuple: (强度等级, 建议列表)

    示例:
        >>> check_password_strength("Abc123!@")
        ('强', [])
        >>> check_password_strength("abc123")
        ('弱', ['密码长度至少8位', '添加大写字母', '添加特殊字符'])
    """
    # 在这里编写你的代码
    pass


def determine_season_activity(month, temperature):
    """
    练习6：季节活动推荐

    根据月份和温度推荐合适的活动：

    季节判断（北半球）：
    - 春季（3-5月）
    - 夏季（6-8月）
    - 秋季（9-11月）
    - 冬季（12,1,2月）

    活动推荐规则：
    - 春季：温度>20°C推荐"踏青赏花"，否则"室内活动"
    - 夏季：温度>30°C推荐"游泳避暑"，否则"户外运动"
    - 秋季：温度>15°C推荐"登山赏叶"，否则"室内阅读"
    - 冬季：温度<0°C推荐"滑雪运动"，否则"温泉泡汤"

    参数:
        month (int): 月份（1-12）
        temperature (float): 温度（摄氏度）

    返回:
        tuple: (季节, 推荐活动)

    示例:
        >>> determine_season_activity(4, 25)
        ('春季', '踏青赏花')
        >>> determine_season_activity(7, 35)
        ('夏季', '游泳避暑')
        >>> determine_season_activity(13, 20)
        ('无效月份', '请输入1-12的月份')
    """
    # 在这里编写你的代码
    pass


def main():
    """
    主函数：测试所有练习函数
    """
    print("Session04 练习题1：条件语句练习")
    print("=" * 50)

    # 测试练习1：年龄分类
    print("\n练习1：年龄分类测试")
    test_ages = [1, 8, 15, 25, 65, -5, 200]
    for age in test_ages:
        result = check_age_category(age)
        print(f"年龄 {age}: {result}")

    # 测试练习2：成绩等级
    print("\n练习2：成绩等级测试")
    test_scores = [95, 85, 75, 65, 45, 105, -10]
    for score in test_scores:
        grade, comment = calculate_grade(score)
        print(f"分数 {score}: {grade}等级 - {comment}")

    # 测试练习3：三角形类型
    print("\n练习3：三角形类型测试")
    test_triangles = [(3, 3, 3), (3, 4, 5), (5, 5, 8), (1, 2, 5), (6, 8, 10)]
    for a, b, c in test_triangles:
        result = check_triangle_type(a, b, c)
        print(f"边长 ({a}, {b}, {c}): {result}")

    # 测试练习4：快递费用
    print("\n练习4：快递费用测试")
    test_shipping = [
        (0.5, 50, False),
        (3, 200, False),
        (2, 100, True),
        (6, 600, False),
        (8, 300, True),
    ]
    for weight, distance, express in test_shipping:
        cost = calculate_shipping_cost(weight, distance, express)
        express_text = "加急" if express else "普通"
        print(f"{weight}kg, {distance}km, {express_text}: ¥{cost:.2f}")

    # 测试练习5：密码强度
    print("\n练习5：密码强度测试")
    test_passwords = ["Abc123!@", "abc123", "PASSWORD", "12345678", "Aa1!"]
    for password in test_passwords:
        strength, suggestions = check_password_strength(password)
        print(f"密码 '{password}': {strength}")
        if suggestions:
            print(f"  建议: {', '.join(suggestions)}")

    # 测试练习6：季节活动
    print("\n练习6：季节活动测试")
    test_seasons = [(4, 25), (7, 35), (10, 18), (1, -5), (13, 20), (6, 25)]
    for month, temp in test_seasons:
        season, activity = determine_season_activity(month, temp)
        print(f"{month}月, {temp}°C: {season} - {activity}")

    print("\n" + "=" * 50)
    print("练习测试完成！")
    print("\n💡 提示：")
    print("1. 如果某些测试结果显示 'None'，说明对应函数还未实现")
    print("2. 请逐个实现每个函数，并确保逻辑正确")
    print("3. 可以添加更多测试用例来验证你的实现")
    print("4. 注意处理边界条件和异常情况")


if __name__ == "__main__":
    main()
