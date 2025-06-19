#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session03 示例3: 逻辑运算符详解

本示例详细演示了Python中所有逻辑运算符的使用方法，
包括and、or、not运算符，以及它们在复杂条件判断中的应用。

学习目标:
- 掌握所有逻辑运算符的用法
- 理解短路求值的机制
- 学会组合多个条件进行复杂判断
- 掌握逻辑运算符的优先级
"""


def basic_logical_operations():
    """
    演示基本逻辑运算
    """
    print("🧠 基本逻辑运算演示")
    print("=" * 30)
    
    # 逻辑与 (and) 运算
    print("逻辑与 (and) 运算:")
    print(f"  True and True = {True and True}")
    print(f"  True and False = {True and False}")
    print(f"  False and True = {False and True}")
    print(f"  False and False = {False and False}")
    print()
    
    # 逻辑或 (or) 运算
    print("逻辑或 (or) 运算:")
    print(f"  True or True = {True or True}")
    print(f"  True or False = {True or False}")
    print(f"  False or True = {False or True}")
    print(f"  False or False = {False or False}")
    print()
    
    # 逻辑非 (not) 运算
    print("逻辑非 (not) 运算:")
    print(f"  not True = {not True}")
    print(f"  not False = {not False}")
    print()
    
    # 复合逻辑运算
    print("复合逻辑运算:")
    print(f"  not (True and False) = {not (True and False)}")
    print(f"  not True or False = {not True or False}")
    print(f"  True and not False = {True and not False}")
    print(f"  False or not False = {False or not False}")
    print()


def truthiness_in_python():
    """
    演示Python中的真值判断
    """
    print("✅ Python中的真值判断")
    print("=" * 30)
    
    # 不同类型的真值测试
    test_values = [
        # 数值类型
        0, 1, -1, 0.0, 3.14,
        # 字符串类型
        "", "hello", " ",
        # 容器类型
        [], [1, 2, 3], (), (1, 2), {}, {"key": "value"},
        # 特殊值
        None, True, False
    ]
    
    print("各种值的真值判断:")
    for value in test_values:
        truth_value = bool(value)
        print(f"  bool({repr(value):15}) = {truth_value}")
    print()
    
    # 在条件语句中的应用
    print("在条件语句中的应用:")
    test_cases = [0, "", [], None, "hello", [1, 2, 3]]
    
    for value in test_cases:
        if value:
            print(f"  {repr(value)} 在if语句中被视为 True")
        else:
            print(f"  {repr(value)} 在if语句中被视为 False")
    print()


def short_circuit_evaluation():
    """
    演示短路求值机制
    """
    print("⚡ 短路求值机制演示")
    print("=" * 30)
    
    # 定义一个有副作用的函数
    def expensive_function(name, return_value):
        print(f"    -> 执行了 {name}() 函数")
        return return_value
    
    print("1. and 运算的短路求值:")
    print("   当第一个条件为 False 时，不会执行第二个条件")
    
    print("\n   测试: False and expensive_function('test1', True)")
    result1 = False and expensive_function('test1', True)
    print(f"   结果: {result1}")
    
    print("\n   测试: True and expensive_function('test2', True)")
    result2 = True and expensive_function('test2', True)
    print(f"   结果: {result2}")
    print()
    
    print("2. or 运算的短路求值:")
    print("   当第一个条件为 True 时，不会执行第二个条件")
    
    print("\n   测试: True or expensive_function('test3', False)")
    result3 = True or expensive_function('test3', False)
    print(f"   结果: {result3}")
    
    print("\n   测试: False or expensive_function('test4', True)")
    result4 = False or expensive_function('test4', True)
    print(f"   结果: {result4}")
    print()
    
    # 实际应用：避免错误
    print("3. 短路求值的实际应用 - 避免错误:")
    
    # 安全的除法检查
    def safe_divide(a, b):
        # 先检查除数是否为0，避免除零错误
        if b != 0 and a / b > 1:
            return f"{a} / {b} = {a / b} (大于1)"
        else:
            return f"无法进行除法或结果不大于1"
    
    test_cases = [(10, 5), (10, 0), (5, 10)]
    for a, b in test_cases:
        result = safe_divide(a, b)
        print(f"   {result}")
    print()


def complex_conditions():
    """
    演示复杂条件判断
    """
    print("🎯 复杂条件判断演示")
    print("=" * 30)
    
    # 用户权限检查
    print("1. 用户权限检查系统:")
    
    users = [
        {"name": "张三", "age": 25, "is_admin": False, "is_active": True, "department": "IT"},
        {"name": "李四", "age": 30, "is_admin": True, "is_active": True, "department": "HR"},
        {"name": "王五", "age": 22, "is_active": False, "department": "IT"},
        {"name": "赵六", "age": 35, "is_admin": True, "is_active": True, "department": "Finance"}
    ]
    
    for user in users:
        name = user["name"]
        age = user["age"]
        is_admin = user.get("is_admin", False)
        is_active = user.get("is_active", False)
        department = user.get("department", "Unknown")
        
        # 复杂权限判断
        can_access_admin = is_admin and is_active
        can_access_it = (department == "IT" and is_active) or is_admin
        can_modify_data = is_admin and is_active and age >= 25
        
        print(f"   用户: {name}")
        print(f"     管理员权限: {can_access_admin}")
        print(f"     IT系统访问: {can_access_it}")
        print(f"     数据修改权限: {can_modify_data}")
        print()
    
    # 贷款审批系统
    print("2. 贷款审批系统:")
    
    applicants = [
        {"name": "申请人A", "age": 25, "income": 8000, "credit_score": 750, "has_collateral": True},
        {"name": "申请人B", "age": 19, "income": 12000, "credit_score": 680, "has_collateral": False},
        {"name": "申请人C", "age": 35, "income": 6000, "credit_score": 720, "has_collateral": True},
        {"name": "申请人D", "age": 45, "income": 15000, "credit_score": 800, "has_collateral": False}
    ]
    
    for applicant in applicants:
        name = applicant["name"]
        age = applicant["age"]
        income = applicant["income"]
        credit_score = applicant["credit_score"]
        has_collateral = applicant["has_collateral"]
        
        # 贷款审批条件
        age_qualified = 18 <= age <= 65
        income_qualified = income >= 5000
        credit_qualified = credit_score >= 700
        
        # 基本条件：年龄、收入、信用分数都要满足
        basic_qualified = age_qualified and income_qualified and credit_qualified
        
        # 特殊情况：高收入或有抵押品可以降低信用分数要求
        special_qualified = (age_qualified and income_qualified and 
                           (credit_score >= 650 and (income >= 10000 or has_collateral)))
        
        # 最终审批结果
        approved = basic_qualified or special_qualified
        
        print(f"   {name}:")
        print(f"     年龄: {age} ({'✅' if age_qualified else '❌'})")
        print(f"     收入: {income} ({'✅' if income_qualified else '❌'})")
        print(f"     信用分数: {credit_score} ({'✅' if credit_qualified else '❌'})")
        print(f"     有抵押品: {'是' if has_collateral else '否'}")
        print(f"     审批结果: {'✅ 通过' if approved else '❌ 拒绝'}")
        print()


def logical_operator_precedence():
    """
    演示逻辑运算符优先级
    """
    print("📊 逻辑运算符优先级演示")
    print("=" * 30)
    
    print("运算符优先级 (从高到低): not > and > or")
    print()
    
    # 不使用括号的表达式
    print("1. 不使用括号的表达式:")
    
    expressions = [
        "True or False and False",
        "False and True or True",
        "not False and True",
        "not True or False",
        "True and False or True and True"
    ]
    
    for expr in expressions:
        result = eval(expr)
        print(f"   {expr} = {result}")
    print()
    
    # 使用括号明确优先级
    print("2. 使用括号明确优先级:")
    
    comparisons = [
        ("True or False and False", "True or (False and False)", "(True or False) and False"),
        ("False and True or True", "(False and True) or True", "False and (True or True)"),
        ("not False and True", "(not False) and True", "not (False and True)")
    ]
    
    for original, interpretation1, interpretation2 in comparisons:
        result_orig = eval(original)
        result_int1 = eval(interpretation1)
        result_int2 = eval(interpretation2)
        
        print(f"   原表达式: {original} = {result_orig}")
        print(f"   理解1: {interpretation1} = {result_int1} {'✅' if result_orig == result_int1 else '❌'}")
        print(f"   理解2: {interpretation2} = {result_int2} {'✅' if result_orig == result_int2 else '❌'}")
        print()


def practical_applications():
    """
    逻辑运算符的实际应用
    """
    print("🛠️ 实际应用案例")
    print("=" * 30)
    
    # 1. 表单验证
    print("1. 用户注册表单验证:")
    
    def validate_registration(username, password, email, age, terms_accepted):
        """验证用户注册信息"""
        
        # 各项验证条件
        username_valid = len(username) >= 3 and username.isalnum()
        password_valid = (len(password) >= 8 and 
                         any(c.isupper() for c in password) and 
                         any(c.islower() for c in password) and 
                         any(c.isdigit() for c in password))
        email_valid = "@" in email and "." in email
        age_valid = 13 <= age <= 120
        
        # 总体验证结果
        all_valid = (username_valid and password_valid and 
                    email_valid and age_valid and terms_accepted)
        
        return {
            "valid": all_valid,
            "username_valid": username_valid,
            "password_valid": password_valid,
            "email_valid": email_valid,
            "age_valid": age_valid,
            "terms_accepted": terms_accepted
        }
    
    test_users = [
        ("user1", "Password123", "user1@email.com", 25, True),
        ("u1", "pass", "invalid-email", 15, False),
        ("validuser", "ValidPass123", "valid@email.com", 30, True)
    ]
    
    for username, password, email, age, terms in test_users:
        result = validate_registration(username, password, email, age, terms)
        print(f"   用户: {username}")
        print(f"     用户名有效: {result['username_valid']}")
        print(f"     密码有效: {result['password_valid']}")
        print(f"     邮箱有效: {result['email_valid']}")
        print(f"     年龄有效: {result['age_valid']}")
        print(f"     同意条款: {result['terms_accepted']}")
        print(f"     整体验证: {'✅ 通过' if result['valid'] else '❌ 失败'}")
        print()
    
    # 2. 游戏角色状态判断
    print("2. 游戏角色状态判断:")
    
    def check_character_status(hp, mp, level, has_weapon, in_safe_zone):
        """检查游戏角色状态"""
        
        alive = hp > 0
        can_cast_spell = alive and mp >= 10
        can_fight = alive and (has_weapon or level >= 5)
        is_safe = in_safe_zone or (hp > 50 and has_weapon)
        needs_healing = alive and hp < 30
        can_level_up = alive and level < 100
        
        return {
            "alive": alive,
            "can_cast_spell": can_cast_spell,
            "can_fight": can_fight,
            "is_safe": is_safe,
            "needs_healing": needs_healing,
            "can_level_up": can_level_up
        }
    
    characters = [
        ("战士", 80, 20, 15, True, False),
        ("法师", 25, 5, 8, False, True),
        ("盗贼", 0, 30, 12, True, False),
        ("新手", 100, 50, 1, False, True)
    ]
    
    for name, hp, mp, level, has_weapon, in_safe_zone in characters:
        status = check_character_status(hp, mp, level, has_weapon, in_safe_zone)
        print(f"   角色: {name} (HP:{hp}, MP:{mp}, 等级:{level})")
        print(f"     存活: {status['alive']}")
        print(f"     可施法: {status['can_cast_spell']}")
        print(f"     可战斗: {status['can_fight']}")
        print(f"     安全: {status['is_safe']}")
        print(f"     需要治疗: {status['needs_healing']}")
        print(f"     可升级: {status['can_level_up']}")
        print()
    
    # 3. 智能推荐系统
    print("3. 电影推荐系统:")
    
    def recommend_movie(user_age, preferred_genre, rating_threshold, 
                       duration_preference, has_subtitles_preference):
        """电影推荐逻辑"""
        
        movies = [
            {"title": "动作大片", "genre": "动作", "rating": 8.5, "duration": 120, "has_subtitles": True, "age_rating": "PG-13"},
            {"title": "浪漫喜剧", "genre": "喜剧", "rating": 7.8, "duration": 95, "has_subtitles": False, "age_rating": "PG"},
            {"title": "科幻史诗", "genre": "科幻", "rating": 9.2, "duration": 180, "has_subtitles": True, "age_rating": "PG-13"},
            {"title": "恐怖片", "genre": "恐怖", "rating": 7.5, "duration": 90, "has_subtitles": False, "age_rating": "R"}
        ]
        
        recommended = []
        
        for movie in movies:
            # 年龄限制检查
            age_appropriate = (movie["age_rating"] == "PG" or 
                             (movie["age_rating"] == "PG-13" and user_age >= 13) or 
                             (movie["age_rating"] == "R" and user_age >= 17))
            
            # 类型匹配
            genre_match = preferred_genre == "任意" or movie["genre"] == preferred_genre
            
            # 评分要求
            rating_ok = movie["rating"] >= rating_threshold
            
            # 时长偏好
            duration_ok = (duration_preference == "任意" or 
                          (duration_preference == "短" and movie["duration"] <= 100) or 
                          (duration_preference == "中" and 100 < movie["duration"] <= 150) or 
                          (duration_preference == "长" and movie["duration"] > 150))
            
            # 字幕偏好
            subtitle_ok = not has_subtitles_preference or movie["has_subtitles"]
            
            # 综合判断
            if age_appropriate and genre_match and rating_ok and duration_ok and subtitle_ok:
                recommended.append(movie)
        
        return recommended
    
    # 测试推荐系统
    test_users = [
        (25, "动作", 8.0, "中", True),
        (15, "喜剧", 7.0, "短", False),
        (30, "任意", 9.0, "任意", True)
    ]
    
    for age, genre, rating, duration, subtitles in test_users:
        recommendations = recommend_movie(age, genre, rating, duration, subtitles)
        print(f"   用户偏好: 年龄{age}, 类型{genre}, 评分≥{rating}, 时长{duration}, 字幕{subtitles}")
        if recommendations:
            print("   推荐电影:")
            for movie in recommendations:
                print(f"     - {movie['title']} ({movie['genre']}, {movie['rating']}分, {movie['duration']}分钟)")
        else:
            print("   暂无符合条件的电影推荐")
        print()


def main():
    """
    主函数
    """
    print("Session03 示例3: 逻辑运算符详解")
    print("=" * 50)
    print()
    
    basic_logical_operations()
    truthiness_in_python()
    short_circuit_evaluation()
    complex_conditions()
    logical_operator_precedence()
    practical_applications()
    
    print("🎉 逻辑运算符示例演示完成！")
    print("\n💡 学习要点:")
    print("1. 掌握 and、or、not 三个逻辑运算符")
    print("2. 理解Python中的真值判断规则")
    print("3. 学会利用短路求值提高程序效率")
    print("4. 掌握逻辑运算符的优先级")
    print("5. 能够组合多个条件进行复杂判断")
    print("6. 将逻辑运算符应用到实际项目中")


if __name__ == "__main__":
    main()