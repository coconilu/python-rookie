#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session04 示例1：条件语句详解

本示例详细演示了Python中条件语句的各种用法，包括：
- 基本if语句
- if-else语句
- if-elif-else语句
- 嵌套条件语句
- 条件表达式（三元运算符）

作者: Python教程团队
创建日期: 2024-12-21
"""


def basic_if_examples():
    """
    基本if语句示例
    """
    print("=== 基本if语句示例 ===")

    # 示例1：简单条件判断
    age = 18
    print(f"年龄: {age}")

    if age >= 18:
        print("✓ 已成年")
        print("✓ 可以投票")
        print("✓ 可以考驾照")

    # 示例2：多个独立的if语句
    score = 85
    print(f"\n考试分数: {score}")

    if score >= 90:
        print("🏆 优秀")

    if score >= 80:
        print("👍 良好")

    if score >= 60:
        print("✓ 及格")

    if score < 60:
        print("❌ 不及格")


def if_else_examples():
    """
    if-else语句示例
    """
    print("\n=== if-else语句示例 ===")

    # 示例1：二选一的情况
    temperature = 25
    print(f"温度: {temperature}°C")

    if temperature > 20:
        print("🌞 天气温暖，适合外出")
        clothing = "短袖"
    else:
        print("🧥 天气较冷，注意保暖")
        clothing = "长袖"

    print(f"建议穿: {clothing}")

    # 示例2：用户权限检查
    is_admin = True
    print(f"\n管理员权限: {is_admin}")

    if is_admin:
        print("🔑 欢迎管理员！")
        print("  - 可以查看所有数据")
        print("  - 可以修改系统设置")
        print("  - 可以管理用户")
    else:
        print("👤 欢迎普通用户！")
        print("  - 可以查看个人数据")
        print("  - 可以修改个人信息")


def if_elif_else_examples():
    """
    if-elif-else语句示例
    """
    print("\n=== if-elif-else语句示例 ===")

    # 示例1：成绩等级划分
    score = 92
    print(f"学生分数: {score}")

    if score >= 90:
        grade = "A"
        comment = "优秀"
        emoji = "🏆"
    elif score >= 80:
        grade = "B"
        comment = "良好"
        emoji = "👍"
    elif score >= 70:
        grade = "C"
        comment = "中等"
        emoji = "👌"
    elif score >= 60:
        grade = "D"
        comment = "及格"
        emoji = "😐"
    else:
        grade = "F"
        comment = "不及格"
        emoji = "😞"

    print(f"等级: {grade} - {comment} {emoji}")

    # 示例2：季节判断
    month = 8
    print(f"\n月份: {month}")

    if month in [12, 1, 2]:
        season = "冬季"
        activity = "滑雪、堆雪人"
        emoji = "❄️"
    elif month in [3, 4, 5]:
        season = "春季"
        activity = "踏青、赏花"
        emoji = "🌸"
    elif month in [6, 7, 8]:
        season = "夏季"
        activity = "游泳、避暑"
        emoji = "☀️"
    elif month in [9, 10, 11]:
        season = "秋季"
        activity = "登山、赏叶"
        emoji = "🍂"
    else:
        season = "无效月份"
        activity = "请输入1-12的月份"
        emoji = "❓"

    print(f"{emoji} {season} - 适合: {activity}")


def nested_conditions_examples():
    """
    嵌套条件语句示例
    """
    print("\n=== 嵌套条件语句示例 ===")

    # 示例1：天气和温度的组合判断
    weather = "晴天"
    temperature = 28

    print(f"天气: {weather}, 温度: {temperature}°C")

    if weather == "晴天":
        print("☀️ 今天是晴天！")
        if temperature > 30:
            print("  🔥 天气很热")
            suggestion = "建议待在室内，开空调"
        elif temperature > 20:
            print("  😊 天气舒适")
            suggestion = "适合户外活动"
        else:
            print("  🧥 有点凉")
            suggestion = "建议穿长袖外出"
    elif weather == "雨天":
        print("🌧️ 今天下雨")
        if temperature > 25:
            print("  💧 温暖的雨天")
            suggestion = "带伞，穿轻便雨衣"
        else:
            print("  🌨️ 寒冷的雨天")
            suggestion = "带伞，注意保暖"
    else:
        print("🌫️ 其他天气")
        suggestion = "根据具体情况决定"

    print(f"建议: {suggestion}")

    # 示例2：用户登录验证
    username = "admin"
    password = "123456"
    is_active = True

    print(f"\n用户登录验证:")
    print(f"用户名: {username}")
    print(f"密码: {'*' * len(password)}")
    print(f"账户状态: {'激活' if is_active else '禁用'}")

    if username == "admin":
        print("✓ 用户名正确")
        if password == "123456":
            print("✓ 密码正确")
            if is_active:
                print("🎉 登录成功！欢迎管理员！")
                access_level = "管理员"
            else:
                print("❌ 账户已被禁用")
                access_level = "无权限"
        else:
            print("❌ 密码错误")
            access_level = "无权限"
    else:
        print("❌ 用户名不存在")
        access_level = "无权限"

    print(f"访问级别: {access_level}")


def conditional_expressions_examples():
    """
    条件表达式（三元运算符）示例
    """
    print("\n=== 条件表达式示例 ===")

    # 示例1：简单的条件赋值
    age = 17
    status = "成年人" if age >= 18 else "未成年人"
    print(f"年龄: {age}, 状态: {status}")

    # 示例2：数值比较
    a, b = 10, 20
    max_value = a if a > b else b
    print(f"数字: {a}, {b}, 最大值: {max_value}")

    # 示例3：字符串处理
    name = ""
    display_name = name if name else "匿名用户"
    print(f"显示名称: {display_name}")

    # 示例4：列表处理
    numbers = [1, 2, 3, 4, 5]
    result = "有数据" if numbers else "空列表"
    print(f"列表状态: {result}")

    # 示例5：复杂条件表达式
    score = 85
    grade = (
        "A"
        if score >= 90
        else "B" if score >= 80 else "C" if score >= 70 else "D" if score >= 60 else "F"
    )
    print(f"分数: {score}, 等级: {grade}")


def practical_examples():
    """
    实际应用示例
    """
    print("\n=== 实际应用示例 ===")

    # 示例1：BMI计算和健康建议
    height = 1.75  # 米
    weight = 70  # 公斤

    bmi = weight / (height**2)
    print(f"身高: {height}m, 体重: {weight}kg")
    print(f"BMI: {bmi:.2f}")

    if bmi < 18.5:
        category = "偏瘦"
        advice = "建议增加营养，适当运动"
        emoji = "📉"
    elif bmi < 24:
        category = "正常"
        advice = "保持良好的生活习惯"
        emoji = "✅"
    elif bmi < 28:
        category = "偏胖"
        advice = "建议控制饮食，增加运动"
        emoji = "📈"
    else:
        category = "肥胖"
        advice = "建议咨询医生，制定减重计划"
        emoji = "⚠️"

    print(f"{emoji} 体重状况: {category}")
    print(f"建议: {advice}")

    # 示例2：购物折扣计算
    total_amount = 350
    is_vip = True
    is_first_purchase = False

    print(f"\n购物金额: ¥{total_amount}")
    print(f"VIP会员: {'是' if is_vip else '否'}")
    print(f"首次购买: {'是' if is_first_purchase else '否'}")

    discount = 0
    discount_reason = []

    # 基础折扣
    if total_amount >= 500:
        discount += 0.2  # 20%折扣
        discount_reason.append("满500减20%")
    elif total_amount >= 300:
        discount += 0.1  # 10%折扣
        discount_reason.append("满300减10%")
    elif total_amount >= 100:
        discount += 0.05  # 5%折扣
        discount_reason.append("满100减5%")

    # VIP额外折扣
    if is_vip:
        discount += 0.05  # 额外5%折扣
        discount_reason.append("VIP额外5%")

    # 首次购买折扣
    if is_first_purchase:
        discount += 0.1  # 额外10%折扣
        discount_reason.append("首购额外10%")

    # 限制最大折扣
    if discount > 0.3:
        discount = 0.3
        discount_reason.append("(最大折扣30%)")

    final_amount = total_amount * (1 - discount)
    saved_amount = total_amount - final_amount

    print(f"折扣详情: {', '.join(discount_reason)}")
    print(f"总折扣: {discount*100:.0f}%")
    print(f"节省金额: ¥{saved_amount:.2f}")
    print(f"实付金额: ¥{final_amount:.2f}")


def main():
    """
    主函数：运行所有示例
    """
    print("Session04 示例1：条件语句详解")
    print("=" * 50)

    basic_if_examples()
    if_else_examples()
    if_elif_else_examples()
    nested_conditions_examples()
    conditional_expressions_examples()
    practical_examples()

    print("\n" + "=" * 50)
    print("示例演示完成！")
    print("\n💡 学习要点:")
    print("1. if语句用于单一条件判断")
    print("2. if-else用于二选一的情况")
    print("3. if-elif-else用于多选一的情况")
    print("4. 嵌套条件可以处理复杂的逻辑")
    print("5. 条件表达式可以简化简单的条件赋值")


if __name__ == "__main__":
    main()
