#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session03 练习题3解答：逻辑运算练习

这个文件包含了exercise3.py中所有练习题的参考解答。
学习者可以参考这些解答来检查自己的实现，
但建议先独立完成练习再查看解答。
"""


def user_login_validator(username, password, is_active=True, attempts=0):
    """
    验证用户登录信息
    """
    # 检查所有条件
    username_valid = len(username) >= 3
    password_valid = len(password) >= 6
    account_active = is_active
    attempts_ok = attempts < 5
    
    # 使用and运算符组合所有条件
    success = username_valid and password_valid and account_active and attempts_ok
    
    # 生成详细的错误信息
    if success:
        message = "登录验证成功"
    else:
        issues = []
        if not username_valid:
            issues.append("用户名长度不足")
        if not password_valid:
            issues.append("密码长度不足")
        if not account_active:
            issues.append("账户未激活")
        if not attempts_ok:
            issues.append("登录尝试次数过多")
        message = "登录失败: " + ", ".join(issues)
    
    return {'success': success, 'message': message}


def check_user_permissions(user_role, required_permissions, user_permissions):
    """
    检查用户是否有足够的权限
    """
    # admin拥有所有权限
    if user_role == 'admin':
        return True
    
    # guest只有基本查看权限
    if user_role == 'guest':
        basic_permissions = ['read', 'view']
        return all(perm in basic_permissions for perm in required_permissions)
    
    # user需要检查具体权限
    if user_role == 'user':
        return all(perm in user_permissions for perm in required_permissions)
    
    # 未知角色没有权限
    return False


def smart_product_recommender(user_age, user_budget, product_category, 
                             user_interests, is_premium_member=False):
    """
    智能商品推荐系统
    """
    # 检查年龄范围
    age_ok = 18 <= user_age <= 65
    
    # 检查预算或会员状态
    budget_ok = user_budget > 100 or is_premium_member
    
    # 检查商品类别
    hot_categories = ['electronics', 'books']
    category_ok = product_category in user_interests or product_category in hot_categories
    
    # 综合判断是否推荐
    recommend = age_ok and budget_ok and category_ok
    
    # 生成推荐原因
    if recommend:
        reason = "符合推荐条件"
    else:
        issues = []
        if not age_ok:
            issues.append("年龄不在推荐范围")
        if not budget_ok:
            issues.append("预算不足且非会员")
        if not category_ok:
            issues.append("商品类别不匹配")
        reason = "不推荐: " + ", ".join(issues)
    
    # 计算折扣
    discount = 0.1 if is_premium_member else 0.0
    
    return {
        'recommend': recommend,
        'reason': reason,
        'discount': discount
    }


def data_quality_checker(data_dict):
    """
    检查数据质量
    """
    issues = []
    
    # 检查必需字段
    required_fields = ['name', 'age', 'email']
    for field in required_fields:
        if field not in data_dict:
            issues.append(f"缺少必需字段: {field}")
    
    # 检查name字段
    if 'name' in data_dict:
        name = data_dict['name']
        if not name or len(name) <= 1:
            issues.append("姓名不能为空且长度必须大于1")
    
    # 检查age字段
    if 'age' in data_dict:
        age = data_dict['age']
        if not (0 <= age <= 150):
            issues.append("年龄必须在0-150之间")
    
    # 检查email字段
    if 'email' in data_dict:
        email = data_dict['email']
        if '@' not in email or '.' not in email:
            issues.append("邮箱格式无效")
    
    # 检查可选的phone字段
    if 'phone' in data_dict:
        phone = data_dict['phone']
        if len(phone) < 10:
            issues.append("电话号码长度不足")
    
    return {
        'valid': len(issues) == 0,
        'issues': issues
    }


def game_character_status(health, mana, level, has_weapon=False, 
                         has_armor=False, in_safe_zone=False):
    """
    判断游戏角色状态
    """
    # 可以战斗：生命值 > 20 且 (有武器 或 等级 > 5)
    can_fight = health > 20 and (has_weapon or level > 5)
    
    # 可以施法：魔法值 > 10 且 等级 > 2
    can_cast_spell = mana > 10 and level > 2
    
    # 安全状态：在安全区 或 (生命值 > 80 且 有护甲)
    is_safe = in_safe_zone or (health > 80 and has_armor)
    
    # 需要休息：生命值 < 30 或 魔法值 < 20
    needs_rest = health < 30 or mana < 20
    
    return {
        'can_fight': can_fight,
        'can_cast_spell': can_cast_spell,
        'is_safe': is_safe,
        'needs_rest': needs_rest
    }


def weather_activity_advisor(temperature, humidity, wind_speed, 
                           is_raining=False, is_sunny=False):
    """
    根据天气条件推荐活动
    """
    # 适合户外：温度在15-30度 且 不下雨 且 风速 < 20
    outdoor_ok = 15 <= temperature <= 30 and not is_raining and wind_speed < 20
    
    activities = []
    
    # 跑步：适合户外 且 温度 < 25
    if outdoor_ok and temperature < 25:
        activities.append('跑步')
    
    # 游泳：温度 > 20 且 晴天
    if temperature > 20 and is_sunny:
        activities.append('游泳')
    
    # 室内活动：不适合户外 或 湿度 > 80
    if not outdoor_ok or humidity > 80:
        activities.extend(['读书', '看电影', '室内健身'])
    
    # 如果适合户外，添加更多户外活动
    if outdoor_ok:
        activities.extend(['散步', '骑行', '野餐'])
    
    return {
        'outdoor_ok': outdoor_ok,
        'activities': list(set(activities))  # 去重
    }


def investment_advisor(age, income, risk_tolerance, investment_experience,
                      has_emergency_fund=False, has_debt=False):
    """
    投资建议系统
    """
    warnings = []
    
    # 可以投资：有应急基金 且 无债务 且 收入 > 30000
    can_invest = has_emergency_fund and not has_debt and income > 30000
    
    if not can_invest:
        if not has_emergency_fund:
            warnings.append("建议先建立应急基金")
        if has_debt:
            warnings.append("建议先偿还债务")
        if income <= 30000:
            warnings.append("收入较低，建议谨慎投资")
    
    # 推荐资产配置
    recommended_allocation = {}
    
    if can_invest:
        # 年轻人(< 35)可以承受更高风险
        is_young = age < 35
        
        # 有经验的投资者(> 3年)可以考虑复杂产品
        is_experienced = investment_experience > 3
        
        if risk_tolerance == 'high' and is_young:
            recommended_allocation = {
                '股票': 70,
                '债券': 20,
                '现金': 10
            }
        elif risk_tolerance == 'medium':
            recommended_allocation = {
                '股票': 50,
                '债券': 40,
                '现金': 10
            }
        else:  # low risk tolerance
            recommended_allocation = {
                '股票': 20,
                '债券': 70,
                '现金': 10
            }
        
        # 有经验的投资者可以考虑另类投资
        if is_experienced and risk_tolerance in ['medium', 'high']:
            recommended_allocation['另类投资'] = 10
            # 重新平衡其他资产
            for key in ['股票', '债券']:
                if key in recommended_allocation:
                    recommended_allocation[key] -= 5
    
    return {
        'can_invest': can_invest,
        'recommended_allocation': recommended_allocation,
        'warnings': warnings
    }


def smart_home_controller(time_hour, is_home, outdoor_light, indoor_temp,
                         energy_saving_mode=False, security_mode=False):
    """
    智能家居控制系统
    """
    # 开灯：有人在家 且 (室外光线 < 30 或 时间在19-7点)
    # 注意：19-7点跨越午夜，需要特殊处理
    is_night_time = time_hour >= 19 or time_hour <= 7
    lights_on = is_home and (outdoor_light < 30 or is_night_time)
    
    # 开空调：有人在家 且 (温度 < 18 或 温度 > 26) 且 非节能模式
    temp_needs_adjustment = indoor_temp < 18 or indoor_temp > 26
    ac_on = is_home and temp_needs_adjustment and not energy_saving_mode
    
    # 开启安防：无人在家 或 安全模式开启 或 时间在22-6点
    is_security_time = time_hour >= 22 or time_hour <= 6
    security_on = not is_home or security_mode or is_security_time
    
    return {
        'lights_on': lights_on,
        'ac_on': ac_on,
        'security_on': security_on
    }


def complex_condition_optimizer(conditions):
    """
    复杂条件优化器 - 演示布尔表达式优化
    """
    a = conditions.get('a', False)
    b = conditions.get('b', False)
    c = conditions.get('c', False)
    d = conditions.get('d', False)
    
    # 原始复杂表达式
    original_expr = (a and b) or (not a and c) or (b and not c and d)
    
    # 使用德摩根定律优化
    # not (a and b) = (not a) or (not b)
    # not (a or b) = (not a) and (not b)
    
    # 演示短路求值的优化
    # 如果a为True，则不需要计算后面的条件
    optimized_expr = a and b  # 如果a为False，短路求值会跳过b的计算
    if not optimized_expr:
        optimized_expr = (not a and c) or (b and not c and d)
    
    # 演示条件简化
    simplified_conditions = {
        'simple_and': a and b and c,  # 所有条件都为True
        'simple_or': a or b or c,     # 任一条件为True
        'mixed': (a or b) and (c or d),  # 混合条件
        'negation': not (a and b),    # 德摩根定律应用
        'equivalent': (not a) or (not b)  # 等价表达式
    }
    
    return {
        'original_result': original_expr,
        'optimized_result': optimized_expr,
        'simplified_conditions': simplified_conditions,
        'demorgans_demo': {
            'not_and': not (a and b),
            'or_not': (not a) or (not b),
            'are_equal': not (a and b) == ((not a) or (not b))
        }
    }


def advanced_permission_system(user, resource, action):
    """
    高级权限系统演示
    """
    user_role = user.get('role', 'guest')
    user_id = user.get('id')
    resource_owner = resource.get('owner')
    resource_type = resource.get('type')
    is_public = resource.get('public', False)
    
    # 复杂的权限逻辑
    # 管理员有所有权限
    if user_role == 'admin':
        return True
    
    # 资源所有者有完全权限
    if user_id == resource_owner:
        return True
    
    # 公共资源的读取权限
    if is_public and action == 'read':
        return True
    
    # 用户对特定类型资源的权限
    if user_role == 'user':
        if resource_type == 'document' and action in ['read', 'comment']:
            return True
        if resource_type == 'image' and action == 'view':
            return True
    
    # 访客只能查看公共内容
    if user_role == 'guest':
        return is_public and action in ['read', 'view']
    
    return False


def business_rule_engine(customer, product, promotion=None):
    """
    业务规则引擎演示
    """
    # 客户信息
    customer_age = customer.get('age', 0)
    customer_vip = customer.get('is_vip', False)
    customer_history = customer.get('purchase_history', 0)
    
    # 产品信息
    product_price = product.get('price', 0)
    product_category = product.get('category', '')
    product_stock = product.get('stock', 0)
    
    # 促销信息
    promotion_active = promotion and promotion.get('active', False)
    promotion_discount = promotion.get('discount', 0) if promotion else 0
    
    # 业务规则判断
    rules_result = {
        'can_purchase': True,
        'final_price': product_price,
        'messages': []
    }
    
    # 库存检查
    if product_stock <= 0:
        rules_result['can_purchase'] = False
        rules_result['messages'].append('商品缺货')
        return rules_result
    
    # 年龄限制（某些商品）
    if product_category == 'alcohol' and customer_age < 18:
        rules_result['can_purchase'] = False
        rules_result['messages'].append('年龄不符合购买要求')
        return rules_result
    
    # VIP折扣
    if customer_vip:
        vip_discount = 0.1  # 10%折扣
        rules_result['final_price'] *= (1 - vip_discount)
        rules_result['messages'].append('VIP折扣已应用')
    
    # 促销折扣
    if promotion_active and promotion_discount > 0:
        rules_result['final_price'] *= (1 - promotion_discount)
        rules_result['messages'].append(f'促销折扣{promotion_discount*100}%已应用')
    
    # 老客户额外优惠
    if customer_history > 10:
        loyalty_discount = 0.05  # 5%折扣
        rules_result['final_price'] *= (1 - loyalty_discount)
        rules_result['messages'].append('忠诚客户折扣已应用')
    
    # 最终价格四舍五入
    rules_result['final_price'] = round(rules_result['final_price'], 2)
    
    return rules_result


def main():
    """
    主函数 - 演示所有解答
    """
    print("Session03 练习题3解答演示")
    print("=" * 50)
    
    # 演示用户登录验证
    print("\n1. 用户登录验证演示:")
    test_cases = [
        ('admin', 'password123', True, 0),
        ('ab', 'pass', True, 0),  # 用户名太短
        ('user', 'password', False, 0),  # 账户未激活
    ]
    
    for username, password, is_active, attempts in test_cases:
        result = user_login_validator(username, password, is_active, attempts)
        print(f"  用户: {username}, 结果: {result}")
    
    # 演示权限检查
    print("\n2. 权限检查演示:")
    permission_tests = [
        ('admin', ['read', 'write'], ['read']),
        ('user', ['read', 'write'], ['read', 'write', 'delete']),
        ('guest', ['read'], ['read']),
    ]
    
    for role, required, user_perms in permission_tests:
        has_permission = check_user_permissions(role, required, user_perms)
        print(f"  角色: {role}, 需要: {required}, 结果: {has_permission}")
    
    # 演示智能推荐
    print("\n3. 智能推荐演示:")
    result = smart_product_recommender(
        user_age=25,
        user_budget=150,
        product_category='electronics',
        user_interests=['books', 'music'],
        is_premium_member=True
    )
    print(f"  推荐结果: {result}")
    
    # 演示数据质量检查
    print("\n4. 数据质量检查演示:")
    test_data = [
        {'name': 'John', 'age': 25, 'email': 'john@example.com'},
        {'name': '', 'age': 25, 'email': 'john@example.com'},  # 名字为空
        {'name': 'Jane', 'age': 200, 'email': 'jane@example.com'},  # 年龄无效
    ]
    
    for i, data in enumerate(test_data, 1):
        result = data_quality_checker(data)
        print(f"  数据{i}: {result}")
    
    # 演示游戏角色状态
    print("\n5. 游戏角色状态演示:")
    status = game_character_status(
        health=50, mana=30, level=8,
        has_weapon=True, has_armor=False, in_safe_zone=False
    )
    print(f"  角色状态: {status}")
    
    # 演示天气活动建议
    print("\n6. 天气活动建议演示:")
    advice = weather_activity_advisor(
        temperature=22, humidity=60, wind_speed=15,
        is_raining=False, is_sunny=True
    )
    print(f"  活动建议: {advice}")
    
    # 演示投资建议
    print("\n7. 投资建议演示:")
    advice = investment_advisor(
        age=30, income=50000, risk_tolerance='medium',
        investment_experience=2, has_emergency_fund=True, has_debt=False
    )
    print(f"  投资建议: {advice}")
    
    # 演示智能家居控制
    print("\n8. 智能家居控制演示:")
    control = smart_home_controller(
        time_hour=20, is_home=True, outdoor_light=25, indoor_temp=24,
        energy_saving_mode=False, security_mode=False
    )
    print(f"  家居控制: {control}")
    
    # 演示条件优化
    print("\n9. 条件优化演示:")
    test_conditions = {
        'a': True, 'b': False, 'c': True, 'd': False
    }
    result = complex_condition_optimizer(test_conditions)
    print(f"  优化结果: {result}")
    
    # 演示高级权限系统
    print("\n10. 高级权限系统演示:")
    user = {'id': 1, 'role': 'user'}
    resource = {'owner': 2, 'type': 'document', 'public': True}
    has_access = advanced_permission_system(user, resource, 'read')
    print(f"  权限检查: 用户{user}, 资源{resource}, 动作'read' -> {has_access}")
    
    # 演示业务规则引擎
    print("\n11. 业务规则引擎演示:")
    customer = {'age': 25, 'is_vip': True, 'purchase_history': 15}
    product = {'price': 100, 'category': 'electronics', 'stock': 5}
    promotion = {'active': True, 'discount': 0.2}
    
    business_result = business_rule_engine(customer, product, promotion)
    print(f"  业务规则结果: {business_result}")
    
    print("\n" + "=" * 50)
    print("解答演示完成！")


def demonstrate_logical_concepts():
    """
    演示逻辑运算的高级概念
    """
    print("\n逻辑运算高级概念演示")
    print("=" * 40)
    
    # 短路求值演示
    print("\n1. 短路求值演示:")
    
    def expensive_operation():
        print("    执行了昂贵的操作")
        return True
    
    print("  False and expensive_operation():")
    result1 = False and expensive_operation()  # 不会执行expensive_operation
    print(f"  结果: {result1}")
    
    print("\n  True or expensive_operation():")
    result2 = True or expensive_operation()  # 不会执行expensive_operation
    print(f"  结果: {result2}")
    
    # 德摩根定律演示
    print("\n2. 德摩根定律演示:")
    a, b = True, False
    print(f"  给定: a={a}, b={b}")
    print(f"  not (a and b) = {not (a and b)}")
    print(f"  (not a) or (not b) = {(not a) or (not b)}")
    print(f"  两者相等: {not (a and b) == ((not a) or (not b))}")
    
    # 真值表演示
    print("\n3. 真值表演示:")
    print("  A     B     A and B   A or B    not A")
    print("  " + "-" * 40)
    for a in [True, False]:
        for b in [True, False]:
            print(f"  {str(a):5} {str(b):5} {str(a and b):7} {str(a or b):7} {str(not a):5}")


if __name__ == "__main__":
    main()
    demonstrate_logical_concepts()