#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session04 简化版猜数字游戏

这是一个简化版的猜数字游戏，专门为初学者设计。
代码结构简单清晰，重点展示控制流语句的基本用法。

学习重点：
1. while循环的使用
2. if-elif-else条件判断
3. break和continue的应用
4. 异常处理的基础用法
5. 用户输入验证

作者: Python教程团队
创建日期: 2024-12-21
"""

import random


def simple_guess_game():
    """
    简化版猜数字游戏主函数
    
    游戏规则：
    1. 程序随机生成1-100之间的数字
    2. 玩家输入猜测的数字
    3. 程序提示"太大"、"太小"或"猜对了"
    4. 记录猜测次数
    5. 玩家可以输入'quit'退出
    """
    print("🎮 欢迎来到猜数字游戏！")
    print("我已经想好了一个1-100之间的数字，请你来猜猜看！")
    print("输入 'quit' 可以退出游戏\n")
    
    # 生成随机数
    target_number = random.randint(1, 100)
    attempts = 0  # 猜测次数计数器
    max_attempts = 10  # 最大尝试次数
    
    # 游戏主循环
    while attempts < max_attempts:
        # 获取用户输入
        user_input = input(f"第{attempts + 1}次猜测，请输入数字: ").strip()
        
        # 检查是否要退出游戏
        if user_input.lower() == 'quit':
            print(f"游戏结束！答案是 {target_number}")
            break
        
        # 验证输入是否为有效数字
        try:
            guess = int(user_input)
        except ValueError:
            print("⚠️ 请输入有效的数字！")
            continue  # 跳过本次循环，重新开始
        
        # 检查数字范围
        if guess < 1 or guess > 100:
            print("⚠️ 请输入1-100之间的数字！")
            continue
        
        # 增加尝试次数
        attempts += 1
        
        # 判断猜测结果
        if guess == target_number:
            print(f"🎉 恭喜你猜对了！答案就是 {target_number}")
            print(f"你总共猜了 {attempts} 次")
            
            # 根据猜测次数给出评价
            if attempts == 1:
                print("🏆 太厉害了！一次就猜中了！")
            elif attempts <= 3:
                print("🥇 非常棒！你很聪明！")
            elif attempts <= 6:
                print("🥈 不错！表现很好！")
            elif attempts <= 8:
                print("🥉 还可以，继续努力！")
            else:
                print("💪 加油！下次会更好的！")
            
            break  # 猜对了，退出游戏循环
        
        elif guess < target_number:
            print("📈 太小了！试试更大的数字")
        else:
            print("📉 太大了！试试更小的数字")
        
        # 显示剩余机会
        remaining = max_attempts - attempts
        if remaining > 0:
            print(f"还有 {remaining} 次机会\n")
    
    # 如果用完所有机会还没猜中
    else:
        print(f"💀 很遗憾，你没有在 {max_attempts} 次内猜中！")
        print(f"答案是 {target_number}")
        print("不要灰心，再试一次吧！")


def play_multiple_games():
    """
    支持多局游戏的函数
    
    使用外层循环控制游戏会话，内层循环控制单局游戏
    """
    games_played = 0
    games_won = 0
    
    print("🎯 多局游戏模式")
    print("你可以连续玩多局游戏，我会记录你的成绩！\n")
    
    # 游戏会话循环
    while True:
        print(f"\n{'='*50}")
        print(f"第 {games_played + 1} 局游戏开始！")
        print(f"{'='*50}")
        
        # 开始单局游戏
        target_number = random.randint(1, 100)
        attempts = 0
        max_attempts = 10
        game_won = False
        
        print("我想好了一个新数字，开始猜吧！")
        
        # 单局游戏循环
        while attempts < max_attempts:
            user_input = input(f"第{attempts + 1}次猜测: ").strip()
            
            if user_input.lower() == 'quit':
                print(f"答案是 {target_number}")
                return  # 退出整个游戏
            
            try:
                guess = int(user_input)
            except ValueError:
                print("请输入有效数字！")
                continue
            
            if not 1 <= guess <= 100:
                print("请输入1-100之间的数字！")
                continue
            
            attempts += 1
            
            if guess == target_number:
                print(f"🎉 猜对了！答案是 {target_number}")
                print(f"用了 {attempts} 次")
                game_won = True
                break
            elif guess < target_number:
                print("太小了！")
            else:
                print("太大了！")
            
            print(f"剩余 {max_attempts - attempts} 次机会")
        
        # 单局游戏结束
        games_played += 1
        if game_won:
            games_won += 1
        else:
            print(f"很遗憾！答案是 {target_number}")
        
        # 显示当前战绩
        win_rate = (games_won / games_played) * 100
        print(f"\n📊 当前战绩：{games_won}/{games_played} 胜率：{win_rate:.1f}%")
        
        # 询问是否继续
        while True:
            play_again = input("\n想再玩一局吗？(y/n): ").strip().lower()
            if play_again in ['y', 'yes', '是']:
                break
            elif play_again in ['n', 'no', '否']:
                print(f"\n🎮 游戏结束！")
                print(f"总共玩了 {games_played} 局，赢了 {games_won} 局")
                print(f"最终胜率：{win_rate:.1f}%")
                
                # 根据胜率给出评价
                if win_rate >= 80:
                    print("🏆 你是猜数字大师！")
                elif win_rate >= 60:
                    print("🥇 表现优秀！")
                elif win_rate >= 40:
                    print("🥈 还不错！")
                else:
                    print("💪 继续练习，你会更好的！")
                
                return
            else:
                print("请输入 y 或 n")


def demo_control_flow():
    """
    演示控制流语句的使用
    
    这个函数展示了各种控制流语句在实际项目中的应用
    """
    print("\n🔍 控制流语句演示")
    print("="*40)
    
    # 演示条件语句
    print("\n1. 条件语句演示：")
    number = random.randint(1, 100)
    print(f"随机数：{number}")
    
    # 多重条件判断
    if number <= 20:
        category = "很小"
    elif number <= 40:
        category = "较小"
    elif number <= 60:
        category = "中等"
    elif number <= 80:
        category = "较大"
    else:
        category = "很大"
    
    print(f"数字类别：{category}")
    
    # 演示循环语句
    print("\n2. 循环语句演示：")
    print("倒计时：", end=" ")
    for i in range(5, 0, -1):
        print(i, end=" ")
    print("开始！")
    
    # 演示while循环
    print("\n3. while循环演示：")
    count = 0
    while count < 3:
        print(f"循环第 {count + 1} 次")
        count += 1
    
    # 演示循环控制
    print("\n4. 循环控制演示：")
    for i in range(10):
        if i == 3:
            print("跳过数字3")
            continue
        if i == 7:
            print("在数字7处停止")
            break
        print(f"数字：{i}")
    
    print("\n演示完成！")


def main():
    """
    主函数：程序入口
    """
    print("🎮 Session04 简化版猜数字游戏")
    print("="*50)
    
    while True:
        print("\n请选择游戏模式：")
        print("1. 单局游戏")
        print("2. 多局游戏")
        print("3. 控制流演示")
        print("4. 退出程序")
        
        choice = input("\n请输入选项 (1-4): ").strip()
        
        if choice == '1':
            simple_guess_game()
        elif choice == '2':
            play_multiple_games()
        elif choice == '3':
            demo_control_flow()
        elif choice == '4':
            print("👋 谢谢游玩，再见！")
            break
        else:
            print("⚠️ 请输入有效的选项 (1-4)")


if __name__ == "__main__":
    # 程序入口点
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 程序被用户中断，再见！")
    except Exception as e:
        print(f"\n❌ 程序发生错误：{e}")
        print("请检查代码或联系开发者")