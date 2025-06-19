#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session02 练习题2：类型转换实践 - 参考答案

本文件提供了练习题2的完整解决方案，展示了类型转换和用户输入处理。

作者: Python教程团队
创建日期: 2024-12-19
"""

def solution():
    """
    练习题2的完整解决方案
    """
    print("=== Session02 练习题2：类型转换实践 ===")
    
    try:
        # 1. 获取用户输入
        print("\n请输入购买信息:")
        product_name = input("请输入商品名称: ")
        price_str = input("请输入商品价格: ")
        quantity_str = input("请输入购买数量: ")
        has_membership_str = input("是否有会员卡(yes/no): ")
        
        # 2. 类型转换
        price = float(price_str)  # 转换为浮点数
        quantity = int(quantity_str)  # 转换为整数
        has_membership = has_membership_str.lower() == 'yes'  # 转换为布尔值
        
        # 3. 显示转换后的信息
        print("\n=== 购买信息 ===")
        print(f"商品名称: {product_name} (类型: {type(product_name).__name__})")
        print(f"单价: {price}元 (类型: {type(price).__name__})")
        print(f"数量: {quantity}个 (类型: {type(quantity).__name__})")
        print(f"会员卡: {'是' if has_membership else '否'} (类型: {type(has_membership).__name__})")
        
        # 4. 计算总价
        print("\n=== 计算结果 ===")
        
        # 计算原价
        original_total = price * quantity
        print(f"原价: {original_total}元")
        
        # 应用会员折扣
        if has_membership:
            discount_rate = 0.9  # 9折
            final_total = original_total * discount_rate
            print(f"会员折扣: {int(discount_rate * 100)}折")
            print(f"优惠金额: {original_total - final_total:.2f}元")
        else:
            final_total = original_total
            print("会员折扣: 无")
            print("优惠金额: 0.00元")
        
        print(f"实付金额: {final_total:.2f}元")
        
        # 额外信息
        print("\n=== 购买详情 ===")
        print(f"您购买了 {quantity} 个 {product_name}")
        print(f"单价 {price} 元，总计 {original_total} 元")
        if has_membership:
            savings = original_total - final_total
            print(f"会员优惠为您节省了 {savings:.2f} 元")
        print(f"最终支付: {final_total:.2f} 元")
        
    except ValueError as e:
        print(f"\n输入错误: {e}")
        print("请确保价格和数量输入的是有效数字")
        print("\n示例:")
        print("  价格: 5.5 (不要包含货币符号)")
        print("  数量: 3 (必须是整数)")
        print("  会员卡: yes 或 no")
    except Exception as e:
        print(f"\n发生错误: {e}")


def advanced_solution():
    """
    进阶版本：更完善的输入验证和错误处理
    """
    print("\n" + "=" * 50)
    print("=== 进阶版本：完善的输入验证 ===")
    
    def get_valid_input(prompt, input_type, validator=None):
        """获取有效的用户输入"""
        while True:
            try:
                user_input = input(prompt).strip()
                
                if not user_input:
                    print("输入不能为空，请重新输入")
                    continue
                
                if input_type == str:
                    result = user_input
                elif input_type == float:
                    result = float(user_input)
                    if result <= 0:
                        print("价格必须大于0，请重新输入")
                        continue
                elif input_type == int:
                    result = int(user_input)
                    if result <= 0:
                        print("数量必须大于0，请重新输入")
                        continue
                elif input_type == bool:
                    if user_input.lower() in ['yes', 'y', '是', '1']:
                        result = True
                    elif user_input.lower() in ['no', 'n', '否', '0']:
                        result = False
                    else:
                        print("请输入 yes/no 或 y/n，请重新输入")
                        continue
                
                if validator and not validator(result):
                    continue
                    
                return result
                
            except ValueError:
                print(f"输入格式错误，请输入有效的{input_type.__name__}")
            except KeyboardInterrupt:
                print("\n程序被用户中断")
                return None
    
    print("\n请输入购买信息（输入验证版本）:")
    
    # 获取商品名称
    product_name = get_valid_input(
        "请输入商品名称: ", 
        str, 
        lambda x: len(x.strip()) >= 1
    )
    if product_name is None:
        return
    
    # 获取价格
    price = get_valid_input(
        "请输入商品价格: ", 
        float
    )
    if price is None:
        return
    
    # 获取数量
    quantity = get_valid_input(
        "请输入购买数量: ", 
        int
    )
    if quantity is None:
        return
    
    # 获取会员状态
    has_membership = get_valid_input(
        "是否有会员卡(yes/no): ", 
        bool
    )
    if has_membership is None:
        return
    
    # 显示信息和计算
    print("\n=== 验证后的购买信息 ===")
    print(f"商品名称: {product_name}")
    print(f"单价: ¥{price:.2f}")
    print(f"数量: {quantity}个")
    print(f"会员状态: {'是' if has_membership else '否'}")
    
    # 计算总价
    original_total = price * quantity
    
    if has_membership:
        discount_rate = 0.9
        final_total = original_total * discount_rate
        savings = original_total - final_total
    else:
        final_total = original_total
        savings = 0
    
    print("\n=== 价格计算 ===")
    print(f"商品小计: ¥{original_total:.2f}")
    if has_membership:
        print(f"会员折扣: 9折")
        print(f"优惠金额: -¥{savings:.2f}")
    print(f"应付总额: ¥{final_total:.2f}")
    
    # 生成购买小票
    print("\n" + "=" * 30)
    print("         购买小票")
    print("=" * 30)
    print(f"商品: {product_name}")
    print(f"单价: ¥{price:.2f}")
    print(f"数量: {quantity}")
    print(f"小计: ¥{original_total:.2f}")
    if has_membership:
        print(f"会员优惠: -¥{savings:.2f}")
    print("-" * 30)
    print(f"总计: ¥{final_total:.2f}")
    print("=" * 30)
    print("谢谢惠顾！")


def demo_type_conversion():
    """
    演示各种类型转换的例子
    """
    print("\n" + "=" * 50)
    print("=== 类型转换演示 ===")
    
    # 字符串转数字的各种情况
    test_cases = [
        ("123", int),
        ("45.67", float),
        ("0", int),
        ("-10", int),
        ("3.14159", float),
        ("abc", int),  # 这会失败
        ("", int),     # 这会失败
        ("12.34.56", float),  # 这会失败
    ]
    
    print("\n字符串转数字测试:")
    for test_str, target_type in test_cases:
        try:
            result = target_type(test_str)
            print(f"  '{test_str}' -> {target_type.__name__}: {result} ✓")
        except ValueError as e:
            print(f"  '{test_str}' -> {target_type.__name__}: 失败 ({e}) ✗")
    
    # 布尔值转换测试
    print("\n布尔值转换测试:")
    bool_test_cases = [
        "yes", "no", "YES", "No", "y", "n", 
        "true", "false", "1", "0", 
        "是", "否", "", "anything"
    ]
    
    for test_str in bool_test_cases:
        # 自定义布尔转换逻辑
        if test_str.lower() in ['yes', 'y', 'true', '1', '是']:
            result = True
        elif test_str.lower() in ['no', 'n', 'false', '0', '否', '']:
            result = False
        else:
            result = "无法识别"
        
        print(f"  '{test_str}' -> bool: {result}")


if __name__ == "__main__":
    # 运行基础解决方案
    solution()
    
    # 运行进阶解决方案
    advanced_solution()
    
    # 演示类型转换
    demo_type_conversion()
    
    print("\n" + "=" * 50)
    print("练习完成！你已经掌握了类型转换和用户输入处理。")