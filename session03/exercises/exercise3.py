#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session03 练习题3：逻辑运算练习

题目描述：
编写一个程序，实现以下功能：
1. 创建一个用户权限管理系统
2. 实现一个智能推荐系统
3. 编写条件筛选和数据过滤功能
4. 实现复杂的业务逻辑判断

具体要求：
1. 实现用户登录验证和权限检查
2. 实现商品推荐的多条件筛选
3. 实现数据验证的复合条件判断
4. 实现游戏逻辑的状态判断
5. 处理复杂的布尔逻辑组合

学习目标：
- 熟练使用逻辑运算符 (and, or, not)
- 理解短路求值的概念和应用
- 掌握复杂条件判断的组合
- 学会优化布尔表达式

提示：
- 利用短路求值提高程序效率
- 使用括号明确运算优先级
- 考虑德摩根定律简化逻辑表达式
- 注意真值判断的特殊情况
"""


def user_login_validator(username, password, is_active=True, attempts=0):
    """
    验证用户登录信息
    
    参数:
        username (str): 用户名
        password (str): 密码
        is_active (bool): 账户是否激活
        attempts (int): 登录尝试次数
    
    返回:
        dict: 验证结果 {'success': bool, 'message': str}
    
    验证规则:
        - 用户名长度 >= 3
        - 密码长度 >= 6
        - 账户必须是激活状态
        - 登录尝试次数 < 5
    
    在这里实现你的代码
    """
    # TODO: 实现用户登录验证
    # 提示：使用and运算符组合多个条件
    pass


def check_user_permissions(user_role, required_permissions, user_permissions):
    """
    检查用户是否有足够的权限
    
    参数:
        user_role (str): 用户角色 ('admin', 'user', 'guest')
        required_permissions (list): 需要的权限列表
        user_permissions (list): 用户拥有的权限列表
    
    返回:
        bool: 是否有足够权限
    
    权限规则:
        - admin 拥有所有权限
        - user 需要检查具体权限
        - guest 只有基本查看权限
    
    在这里实现你的代码
    """
    # TODO: 检查用户权限
    # 提示：使用or和and运算符，考虑不同角色的权限
    pass


def smart_product_recommender(user_age, user_budget, product_category, 
                             user_interests, is_premium_member=False):
    """
    智能商品推荐系统
    
    参数:
        user_age (int): 用户年龄
        user_budget (float): 用户预算
        product_category (str): 商品类别
        user_interests (list): 用户兴趣列表
        is_premium_member (bool): 是否为会员
    
    返回:
        dict: 推荐结果 {'recommend': bool, 'reason': str, 'discount': float}
    
    推荐规则:
        - 年龄在18-65之间
        - 预算 > 100 或者是会员
        - 商品类别在用户兴趣中 或者 是热门类别('electronics', 'books')
        - 会员享受10%折扣
    
    在这里实现你的代码
    """
    # TODO: 实现智能推荐逻辑
    # 提示：使用复杂的逻辑运算符组合
    pass


def data_quality_checker(data_dict):
    """
    检查数据质量
    
    参数:
        data_dict (dict): 要检查的数据字典
    
    返回:
        dict: 检查结果 {'valid': bool, 'issues': list}
    
    检查规则:
        - 必须包含 'name', 'age', 'email' 字段
        - name 不能为空且长度 > 1
        - age 必须在 0-150 之间
        - email 必须包含 '@' 和 '.'
        - 如果有 'phone' 字段，长度必须 >= 10
    
    在这里实现你的代码
    """
    # TODO: 实现数据质量检查
    # 提示：使用and和or运算符检查多个条件
    pass


def game_character_status(health, mana, level, has_weapon=False, 
                         has_armor=False, in_safe_zone=False):
    """
    判断游戏角色状态
    
    参数:
        health (int): 生命值 (0-100)
        mana (int): 魔法值 (0-100)
        level (int): 等级
        has_weapon (bool): 是否有武器
        has_armor (bool): 是否有护甲
        in_safe_zone (bool): 是否在安全区
    
    返回:
        dict: 角色状态 {'can_fight': bool, 'can_cast_spell': bool, 
                      'is_safe': bool, 'needs_rest': bool}
    
    状态规则:
        - 可以战斗：生命值 > 20 且 (有武器 或 等级 > 5)
        - 可以施法：魔法值 > 10 且 等级 > 2
        - 安全状态：在安全区 或 (生命值 > 80 且 有护甲)
        - 需要休息：生命值 < 30 或 魔法值 < 20
    
    在这里实现你的代码
    """
    # TODO: 判断游戏角色状态
    # 提示：使用逻辑运算符组合多个条件
    pass


def weather_activity_advisor(temperature, humidity, wind_speed, 
                           is_raining=False, is_sunny=False):
    """
    根据天气条件推荐活动
    
    参数:
        temperature (float): 温度 (摄氏度)
        humidity (float): 湿度 (0-100)
        wind_speed (float): 风速 (km/h)
        is_raining (bool): 是否下雨
        is_sunny (bool): 是否晴天
    
    返回:
        dict: 活动建议 {'outdoor_ok': bool, 'activities': list}
    
    推荐规则:
        - 适合户外：温度在15-30度 且 不下雨 且 风速 < 20
        - 跑步：适合户外 且 温度 < 25
        - 游泳：温度 > 20 且 晴天
        - 室内活动：不适合户外 或 湿度 > 80
    
    在这里实现你的代码
    """
    # TODO: 根据天气推荐活动
    # 提示：使用复杂的逻辑判断
    pass


def investment_advisor(age, income, risk_tolerance, investment_experience,
                      has_emergency_fund=False, has_debt=False):
    """
    投资建议系统
    
    参数:
        age (int): 年龄
        income (float): 年收入
        risk_tolerance (str): 风险承受能力 ('low', 'medium', 'high')
        investment_experience (int): 投资经验年数
        has_emergency_fund (bool): 是否有应急基金
        has_debt (bool): 是否有债务
    
    返回:
        dict: 投资建议 {'can_invest': bool, 'recommended_allocation': dict, 
                      'warnings': list}
    
    投资规则:
        - 可以投资：有应急基金 且 无债务 且 收入 > 30000
        - 年轻人(< 35)可以承受更高风险
        - 有经验的投资者(> 3年)可以考虑复杂产品
        - 低风险承受能力者主要投资债券
    
    在这里实现你的代码
    """
    # TODO: 实现投资建议逻辑
    # 提示：使用复杂的条件判断和逻辑运算
    pass


def smart_home_controller(time_hour, is_home, outdoor_light, indoor_temp,
                         energy_saving_mode=False, security_mode=False):
    """
    智能家居控制系统
    
    参数:
        time_hour (int): 当前小时 (0-23)
        is_home (bool): 是否有人在家
        outdoor_light (int): 室外光线强度 (0-100)
        indoor_temp (float): 室内温度
        energy_saving_mode (bool): 是否开启节能模式
        security_mode (bool): 是否开启安全模式
    
    返回:
        dict: 控制指令 {'lights_on': bool, 'ac_on': bool, 'security_on': bool}
    
    控制规则:
        - 开灯：有人在家 且 (室外光线 < 30 或 时间在19-7点)
        - 开空调：有人在家 且 (温度 < 18 或 温度 > 26) 且 非节能模式
        - 开启安防：无人在家 或 安全模式开启 或 时间在22-6点
    
    在这里实现你的代码
    """
    # TODO: 实现智能家居控制逻辑
    # 提示：考虑时间范围的判断
    pass


def complex_condition_optimizer(conditions):
    """
    复杂条件优化器
    
    参数:
        conditions (dict): 条件字典，包含各种布尔值
    
    返回:
        dict: 优化后的结果
    
    这个函数演示如何优化复杂的布尔表达式
    使用德摩根定律和短路求值
    
    在这里实现你的代码
    """
    # TODO: 演示布尔表达式优化
    # 提示：展示德摩根定律的应用
    pass


def test_functions():
    """
    测试所有函数的功能
    """
    print("=" * 50)
    print("Session03 练习题3：逻辑运算练习 - 测试")
    print("=" * 50)
    
    # 测试用户登录验证
    print("\n1. 测试用户登录验证:")
    test_cases = [
        ('admin', 'password123', True, 0),
        ('ab', 'pass', True, 0),  # 用户名太短
        ('user', '12345', True, 0),  # 密码太短
        ('user', 'password', False, 0),  # 账户未激活
        ('user', 'password', True, 5),  # 尝试次数过多
    ]
    
    for username, password, is_active, attempts in test_cases:
        try:
            result = user_login_validator(username, password, is_active, attempts)
            print(f"  用户: {username}, 结果: {result}")
        except Exception as e:
            print(f"  用户: {username}, 错误: {e}")
    
    # 测试权限检查
    print("\n2. 测试权限检查:")
    permission_tests = [
        ('admin', ['read', 'write'], ['read']),
        ('user', ['read', 'write'], ['read', 'write', 'delete']),
        ('guest', ['read'], ['read']),
        ('user', ['delete'], ['read', 'write']),
    ]
    
    for role, required, user_perms in permission_tests:
        try:
            has_permission = check_user_permissions(role, required, user_perms)
            print(f"  角色: {role}, 需要: {required}, 拥有: {user_perms}, 结果: {has_permission}")
        except Exception as e:
            print(f"  权限检查错误: {e}")
    
    # 测试智能推荐
    print("\n3. 测试智能推荐:")
    try:
        result = smart_product_recommender(
            user_age=25,
            user_budget=150,
            product_category='electronics',
            user_interests=['books', 'music'],
            is_premium_member=True
        )
        print(f"  推荐结果: {result}")
    except Exception as e:
        print(f"  智能推荐错误: {e}")
    
    # 测试数据质量检查
    print("\n4. 测试数据质量检查:")
    test_data = [
        {'name': 'John', 'age': 25, 'email': 'john@example.com'},
        {'name': '', 'age': 25, 'email': 'john@example.com'},  # 名字为空
        {'name': 'Jane', 'age': 200, 'email': 'jane@example.com'},  # 年龄无效
        {'name': 'Bob', 'age': 30, 'email': 'invalid-email'},  # 邮箱无效
        {'name': 'Alice', 'age': 28, 'email': 'alice@test.com', 'phone': '123'},  # 电话太短
    ]
    
    for i, data in enumerate(test_data, 1):
        try:
            result = data_quality_checker(data)
            print(f"  数据{i}: {result}")
        except Exception as e:
            print(f"  数据{i}检查错误: {e}")
    
    # 测试游戏角色状态
    print("\n5. 测试游戏角色状态:")
    try:
        status = game_character_status(
            health=50, mana=30, level=8,
            has_weapon=True, has_armor=False, in_safe_zone=False
        )
        print(f"  角色状态: {status}")
    except Exception as e:
        print(f"  角色状态错误: {e}")
    
    # 测试天气活动建议
    print("\n6. 测试天气活动建议:")
    try:
        advice = weather_activity_advisor(
            temperature=22, humidity=60, wind_speed=15,
            is_raining=False, is_sunny=True
        )
        print(f"  活动建议: {advice}")
    except Exception as e:
        print(f"  天气建议错误: {e}")
    
    # 测试投资建议
    print("\n7. 测试投资建议:")
    try:
        advice = investment_advisor(
            age=30, income=50000, risk_tolerance='medium',
            investment_experience=2, has_emergency_fund=True, has_debt=False
        )
        print(f"  投资建议: {advice}")
    except Exception as e:
        print(f"  投资建议错误: {e}")
    
    # 测试智能家居控制
    print("\n8. 测试智能家居控制:")
    try:
        control = smart_home_controller(
            time_hour=20, is_home=True, outdoor_light=25, indoor_temp=24,
            energy_saving_mode=False, security_mode=False
        )
        print(f"  家居控制: {control}")
    except Exception as e:
        print(f"  家居控制错误: {e}")
    
    # 测试条件优化
    print("\n9. 测试条件优化:")
    test_conditions = {
        'a': True, 'b': False, 'c': True, 'd': False
    }
    try:
        result = complex_condition_optimizer(test_conditions)
        print(f"  优化结果: {result}")
    except Exception as e:
        print(f"  条件优化错误: {e}")
    
    print("\n" + "=" * 50)
    print("测试完成！请检查你的实现是否正确。")
    print("=" * 50)


def demonstrate_short_circuit():
    """
    演示短路求值的概念
    """
    print("\n短路求值演示:")
    print("=" * 30)
    
    def expensive_function():
        print("  执行了昂贵的函数")
        return True
    
    print("\n1. and 运算的短路求值:")
    print("  False and expensive_function():")
    result1 = False and expensive_function()  # expensive_function 不会被调用
    print(f"  结果: {result1}")
    
    print("\n  True and expensive_function():")
    result2 = True and expensive_function()  # expensive_function 会被调用
    print(f"  结果: {result2}")
    
    print("\n2. or 运算的短路求值:")
    print("  True or expensive_function():")
    result3 = True or expensive_function()  # expensive_function 不会被调用
    print(f"  结果: {result3}")
    
    print("\n  False or expensive_function():")
    result4 = False or expensive_function()  # expensive_function 会被调用
    print(f"  结果: {result4}")


def demonstrate_demorgans_law():
    """
    演示德摩根定律
    """
    print("\n德摩根定律演示:")
    print("=" * 30)
    
    a, b = True, False
    
    print(f"\n给定: a = {a}, b = {b}")
    print("\n德摩根定律:")
    print(f"  not (a and b) = {not (a and b)}")
    print(f"  (not a) or (not b) = {(not a) or (not b)}")
    print(f"  两者相等: {not (a and b) == ((not a) or (not b))}")
    
    print(f"\n  not (a or b) = {not (a or b)}")
    print(f"  (not a) and (not b) = {(not a) and (not b)}")
    print(f"  两者相等: {not (a or b) == ((not a) and (not b))}")


def main():
    """
    主函数
    """
    print("Session03 练习题3：逻辑运算练习")
    print("\n请在上面的函数中实现你的代码，然后运行测试。")
    print("\n提示：")
    print("1. 熟练使用逻辑运算符 (and, or, not)")
    print("2. 理解和利用短路求值")
    print("3. 使用括号明确运算优先级")
    print("4. 考虑德摩根定律优化表达式")
    
    # 运行测试
    test_functions()
    
    # 演示高级概念
    demonstrate_short_circuit()
    demonstrate_demorgans_law()


if __name__ == "__main__":
    main()