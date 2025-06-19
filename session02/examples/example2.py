#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session02 示例2：类型转换

本示例演示了Python中不同数据类型之间的转换，包括：
- 字符串与数字的相互转换
- 布尔值转换
- 类型转换的错误处理

作者: Python教程团队
创建日期: 2024-12-19
"""

def main():
    """演示类型转换"""
    print("=== 类型转换示例 ===")
    
    # 1. 字符串转数字
    print("\n1. 字符串转数字")
    age_str = "25"
    height_str = "175.5"
    
    age = int(age_str)
    height = float(height_str)
    
    print(f"字符串 '{age_str}' 转为整数: {age}")
    print(f"字符串 '{height_str}' 转为浮点数: {height}")
    
    # 进行数学运算
    next_year_age = age + 1
    height_in_meters = height / 100
    
    print(f"明年年龄: {next_year_age}")
    print(f"身高(米): {height_in_meters}")
    
    # 2. 数字转字符串
    print("\n2. 数字转字符串")
    score = 95
    pi = 3.14159
    
    score_str = str(score)
    pi_str = str(pi)
    
    print(f"整数 {score} 转为字符串: '{score_str}'")
    print(f"浮点数 {pi} 转为字符串: '{pi_str}'")
    
    # 字符串连接
    message = "你的分数是: " + score_str + " 分"
    print(f"字符串连接结果: {message}")
    
    # 3. 布尔值转换
    print("\n3. 布尔值转换")
    
    # 数字转布尔值
    print("数字转布尔值:")
    numbers = [0, 1, -1, 42, 0.0, 3.14]
    for num in numbers:
        print(f"bool({num}) = {bool(num)}")
    
    # 字符串转布尔值
    print("\n字符串转布尔值:")
    strings = ["", "hello", "0", "false", " "]
    for s in strings:
        print(f"bool('{s}') = {bool(s)}")
    
    # 4. 浮点数与整数转换
    print("\n4. 浮点数与整数转换")
    
    # 浮点数转整数（截断小数部分）
    float_num = 3.99
    int_num = int(float_num)
    print(f"浮点数 {float_num} 转为整数: {int_num}")
    
    # 整数转浮点数
    int_value = 42
    float_value = float(int_value)
    print(f"整数 {int_value} 转为浮点数: {float_value}")
    
    # 5. 类型转换错误处理
    print("\n5. 类型转换错误处理")
    
    invalid_strings = ["hello", "12.34.56", "abc123"]
    
    for s in invalid_strings:
        try:
            result = int(s)
            print(f"'{s}' 成功转换为整数: {result}")
        except ValueError as e:
            print(f"'{s}' 转换失败: {e}")
    
    # 6. 实用的转换技巧
    print("\n6. 实用的转换技巧")
    
    # 安全的字符串转数字
    def safe_int_convert(s, default=0):
        """安全地将字符串转换为整数"""
        try:
            return int(s)
        except ValueError:
            return default
    
    test_strings = ["123", "abc", "45.67", ""]
    for s in test_strings:
        result = safe_int_convert(s)
        print(f"安全转换 '{s}': {result}")
    
    # 7. 格式化输出中的类型转换
    print("\n7. 格式化输出中的类型转换")
    
    name = "张三"
    age = 25
    salary = 8500.50
    is_manager = True
    
    # 使用 f-string 自动处理类型转换
    info = f"姓名: {name}, 年龄: {age}, 工资: {salary:.2f}, 管理者: {is_manager}"
    print(info)
    
    # 手动类型转换后格式化
    status = "是" if is_manager else "否"
    info2 = f"员工 {name} 今年 {age} 岁，月薪 {salary} 元，管理者身份: {status}"
    print(info2)

if __name__ == "__main__":
    main()