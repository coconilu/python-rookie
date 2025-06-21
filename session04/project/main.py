#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session04 完整版猜数字游戏 - 主程序

这是猜数字游戏的主程序入口，整合了所有功能模块。
展示了如何构建一个完整的Python项目。

功能特性：
- 多难度等级
- 计分系统
- 游戏统计
- 数据持久化
- 彩色界面
- 成就系统

作者: Python教程团队
创建日期: 2024-12-21
"""

import os
import sys
import time
import json
from datetime import datetime

# 导入项目模块
try:
    from config import *
except ImportError:
    print("❌ 无法导入配置文件，请确保 config.py 存在")
    sys.exit(1)

# 导入其他模块（如果存在）
try:
    from game_core import GuessNumberGame
    from game_ui import GameUI
    from statistics import GameStatistics
    from utils import *
except ImportError as e:
    print(f"⚠️ 部分模块导入失败：{e}")
    print("将使用简化版本运行")
    
    # 简化版本的类定义
    class GuessNumberGame:
        def __init__(self, difficulty='normal'):
            self.difficulty = difficulty
            self.config = DIFFICULTY_LEVELS[difficulty]
            self.reset_game()
        
        def reset_game(self):
            import random
            self.target = random.randint(
                self.config['min_number'], 
                self.config['max_number']
            )
            self.attempts = 0
            self.max_attempts = self.config['max_attempts']
            self.game_over = False
            self.won = False
            self.start_time = time.time()
        
        def make_guess(self, guess):
            if self.game_over:
                return "游戏已结束"
            
            self.attempts += 1
            
            if guess == self.target:
                self.won = True
                self.game_over = True
                return "correct"
            elif guess < self.target:
                return "too_low"
            else:
                return "too_high"
        
        def is_game_over(self):
            return self.game_over or self.attempts >= self.max_attempts
        
        def get_score(self):
            if not self.won:
                return 0
            
            base_score = BASE_SCORE
            penalty = self.attempts * SCORE_RULES['attempt_penalty']
            time_taken = time.time() - self.start_time
            
            if self.attempts == 1:
                base_score += SCORE_RULES['perfect_bonus']
            
            if time_taken < SCORE_RULES['time_bonus_threshold']:
                base_score += SCORE_RULES['time_bonus']
            
            multiplier = self.config['score_multiplier']
            final_score = max(0, int((base_score - penalty) * multiplier))
            
            return final_score
    
    class GameUI:
        @staticmethod
        def print_colored(text, color='reset'):
            if color in COLORS:
                print(f"{COLORS[color]}{text}{COLORS['reset']}")
            else:
                print(text)
        
        @staticmethod
        def clear_screen():
            os.system('cls' if os.name == 'nt' else 'clear')
        
        @staticmethod
        def show_welcome():
            GameUI.clear_screen()
            print(MESSAGES['welcome'])
            print(MESSAGES['game_rules'])
        
        @staticmethod
        def get_difficulty():
            print(MESSAGES['difficulty_prompt'])
            while True:
                choice = input("请选择难度 (1-3): ").strip()
                if choice == '1':
                    return 'easy'
                elif choice == '2':
                    return 'normal'
                elif choice == '3':
                    return 'hard'
                else:
                    print("请输入有效选项 (1-3)")
    
    class GameStatistics:
        def __init__(self):
            self.stats = self.load_statistics()
        
        def load_statistics(self):
            try:
                if os.path.exists(STATISTICS_FILE):
                    with open(STATISTICS_FILE, 'r', encoding='utf-8') as f:
                        return json.load(f)
            except:
                pass
            return {
                'total_games': 0,
                'games_won': 0,
                'best_score': 0,
                'total_score': 0,
                'difficulty_stats': {
                    'easy': {'games': 0, 'wins': 0},
                    'normal': {'games': 0, 'wins': 0},
                    'hard': {'games': 0, 'wins': 0}
                }
            }
        
        def save_statistics(self):
            try:
                os.makedirs(os.path.dirname(STATISTICS_FILE), exist_ok=True)
                with open(STATISTICS_FILE, 'w', encoding='utf-8') as f:
                    json.dump(self.stats, f, ensure_ascii=False, indent=2)
            except:
                pass
        
        def record_game(self, difficulty, won, score):
            self.stats['total_games'] += 1
            if won:
                self.stats['games_won'] += 1
                self.stats['total_score'] += score
                if score > self.stats['best_score']:
                    self.stats['best_score'] = score
            
            self.stats['difficulty_stats'][difficulty]['games'] += 1
            if won:
                self.stats['difficulty_stats'][difficulty]['wins'] += 1
            
            self.save_statistics()
        
        def show_statistics(self):
            stats = self.stats
            win_rate = (stats['games_won'] / max(1, stats['total_games'])) * 100
            
            print(f"\n{MESSAGES['statistics_header']}")
            print("="*40)
            print(f"总游戏数: {stats['total_games']}")
            print(f"获胜次数: {stats['games_won']}")
            print(f"胜率: {win_rate:.1f}%")
            print(f"最佳成绩: {stats['best_score']}")
            print(f"总得分: {stats['total_score']}")
            
            print("\n各难度统计:")
            for diff, data in stats['difficulty_stats'].items():
                if data['games'] > 0:
                    diff_win_rate = (data['wins'] / data['games']) * 100
                    diff_name = DIFFICULTY_LEVELS[diff]['name']
                    print(f"  {diff_name}: {data['wins']}/{data['games']} ({diff_win_rate:.1f}%)")


class GameManager:
    """
    游戏管理器 - 负责整个游戏流程的控制
    """
    
    def __init__(self):
        self.ui = GameUI()
        self.statistics = GameStatistics()
        self.current_game = None
        self.running = True
    
    def start(self):
        """
        启动游戏主循环
        """
        self.ui.show_welcome()
        
        while self.running:
            try:
                self.show_main_menu()
                choice = self.get_menu_choice()
                self.handle_menu_choice(choice)
            except KeyboardInterrupt:
                self.ui.print_colored("\n\n👋 游戏被中断，再见！", 'yellow')
                break
            except Exception as e:
                if DEBUG_MODE:
                    raise
                self.ui.print_colored(f"\n❌ 发生错误：{e}", 'red')
                input("按回车键继续...")
    
    def show_main_menu(self):
        """
        显示主菜单
        """
        print("\n" + "="*50)
        self.ui.print_colored("🎮 主菜单", 'bold')
        print("="*50)
        print("1. 🎯 开始新游戏")
        print("2. 📊 查看统计")
        print("3. ⚙️  游戏设置")
        print("4. 🆘 帮助信息")
        print("5. 👋 退出游戏")
    
    def get_menu_choice(self):
        """
        获取菜单选择
        """
        while True:
            choice = input("\n请选择 (1-5): ").strip()
            if choice in ['1', '2', '3', '4', '5']:
                return choice
            print("⚠️ 请输入有效选项 (1-5)")
    
    def handle_menu_choice(self, choice):
        """
        处理菜单选择
        """
        if choice == '1':
            self.start_new_game()
        elif choice == '2':
            self.show_statistics()
        elif choice == '3':
            self.show_settings()
        elif choice == '4':
            self.show_help()
        elif choice == '5':
            self.quit_game()
    
    def start_new_game(self):
        """
        开始新游戏
        """
        print("\n🎯 开始新游戏")
        print("="*30)
        
        # 选择难度
        difficulty = self.ui.get_difficulty()
        
        # 创建游戏实例
        self.current_game = GuessNumberGame(difficulty)
        
        # 显示游戏信息
        config = DIFFICULTY_LEVELS[difficulty]
        print(f"\n难度: {config['name']}")
        print(f"数字范围: {config['min_number']}-{config['max_number']}")
        print(f"最大尝试次数: {config['max_attempts']}")
        print("\n游戏开始！")
        
        # 游戏主循环
        self.play_game()
    
    def play_game(self):
        """
        游戏主循环
        """
        game = self.current_game
        
        while not game.is_game_over():
            # 显示当前状态
            remaining = game.max_attempts - game.attempts
            print(f"\n剩余机会: {remaining}")
            
            # 获取用户输入
            user_input = input(MESSAGES['input_prompt']).strip()
            
            # 处理特殊命令
            if user_input.lower() in INPUT_CONFIG['quit_commands']:
                if self.confirm_quit():
                    return
                continue
            
            if user_input.lower() in INPUT_CONFIG['hint_commands']:
                self.show_hint()
                continue
            
            if user_input.lower() in INPUT_CONFIG['help_commands']:
                print(HELP_TEXT)
                continue
            
            # 验证数字输入
            try:
                guess = int(user_input)
            except ValueError:
                print(MESSAGES['invalid_input'])
                continue
            
            # 检查数字范围
            config = game.config
            if not (config['min_number'] <= guess <= config['max_number']):
                print(f"⚠️ 请输入{config['min_number']}-{config['max_number']}之间的数字！")
                continue
            
            # 进行猜测
            result = game.make_guess(guess)
            
            # 处理结果
            if result == "correct":
                self.handle_win()
                break
            elif result == "too_low":
                print(MESSAGES['too_low'])
            elif result == "too_high":
                print(MESSAGES['too_high'])
        
        # 游戏结束处理
        if not game.won:
            self.handle_loss()
        
        # 询问是否再玩一局
        self.ask_play_again()
    
    def handle_win(self):
        """
        处理获胜情况
        """
        game = self.current_game
        score = game.get_score()
        
        print(MESSAGES['correct'])
        print(f"🎯 答案: {game.target}")
        print(f"🔢 尝试次数: {game.attempts}")
        print(f"⏱️ 用时: {time.time() - game.start_time:.1f}秒")
        print(f"🏆 得分: {score}")
        
        # 获取评价
        rating = self.get_performance_rating(score)
        print(f"{rating['emoji']} 评价: {rating['title']}")
        
        # 记录统计
        self.statistics.record_game(game.difficulty, True, score)
        
        # 检查成就
        self.check_achievements()
    
    def handle_loss(self):
        """
        处理失败情况
        """
        game = self.current_game
        
        print(MESSAGES['game_over'])
        print(f"💡 答案是: {game.target}")
        print(f"🔢 你用了: {game.attempts} 次机会")
        print("💪 不要灰心，再试一次吧！")
        
        # 记录统计
        self.statistics.record_game(game.difficulty, False, 0)
    
    def get_performance_rating(self, score):
        """
        根据分数获取表现评价
        """
        for rating_key, rating_info in PERFORMANCE_RATINGS.items():
            if score >= rating_info['min_score']:
                return rating_info
        return PERFORMANCE_RATINGS['poor']
    
    def show_hint(self):
        """
        显示提示
        """
        game = self.current_game
        target = game.target
        
        print("\n💡 提示信息:")
        
        # 奇偶性提示
        if target % 2 == 0:
            print("• 这是一个偶数")
        else:
            print("• 这是一个奇数")
        
        # 位数提示
        digit_count = len(str(target))
        print(f"• 这个数字有 {digit_count} 位")
        
        # 范围提示（缩小范围）
        config = game.config
        range_size = config['max_number'] - config['min_number'] + 1
        if range_size > 20:
            if target <= config['min_number'] + range_size // 3:
                print("• 这个数字比较小")
            elif target >= config['max_number'] - range_size // 3:
                print("• 这个数字比较大")
            else:
                print("• 这个数字在中间范围")
    
    def confirm_quit(self):
        """
        确认退出
        """
        response = input(MESSAGES['quit_confirm']).strip().lower()
        return response in ['y', 'yes', '是']
    
    def ask_play_again(self):
        """
        询问是否再玩一局
        """
        response = input(MESSAGES['play_again']).strip().lower()
        if response in ['y', 'yes', '是']:
            self.start_new_game()
    
    def show_statistics(self):
        """
        显示统计信息
        """
        self.statistics.show_statistics()
        input("\n按回车键返回主菜单...")
    
    def show_settings(self):
        """
        显示设置菜单
        """
        print("\n⚙️ 游戏设置")
        print("="*30)
        print("1. 重置统计数据")
        print("2. 查看游戏信息")
        print("3. 返回主菜单")
        
        choice = input("\n请选择 (1-3): ").strip()
        
        if choice == '1':
            self.reset_statistics()
        elif choice == '2':
            self.show_game_info()
        # choice == '3' 或其他情况都返回主菜单
    
    def reset_statistics(self):
        """
        重置统计数据
        """
        confirm = input("⚠️ 确定要重置所有统计数据吗？(y/n): ").strip().lower()
        if confirm in ['y', 'yes', '是']:
            self.statistics.stats = {
                'total_games': 0,
                'games_won': 0,
                'best_score': 0,
                'total_score': 0,
                'difficulty_stats': {
                    'easy': {'games': 0, 'wins': 0},
                    'normal': {'games': 0, 'wins': 0},
                    'hard': {'games': 0, 'wins': 0}
                }
            }
            self.statistics.save_statistics()
            print("✅ 统计数据已重置")
        else:
            print("❌ 操作已取消")
        
        input("按回车键继续...")
    
    def show_game_info(self):
        """
        显示游戏信息
        """
        print(f"\n📋 游戏信息")
        print("="*30)
        print(f"游戏名称: {GAME_NAME}")
        print(f"版本: {GAME_VERSION}")
        print(f"作者: {GAME_AUTHOR}")
        print(f"\n难度等级:")
        
        for key, config in DIFFICULTY_LEVELS.items():
            print(f"  {config['name']}: {config['min_number']}-{config['max_number']}, 最多{config['max_attempts']}次")
        
        input("\n按回车键继续...")
    
    def show_help(self):
        """
        显示帮助信息
        """
        print(HELP_TEXT)
        input("\n按回车键返回主菜单...")
    
    def check_achievements(self):
        """
        检查成就（简化版本）
        """
        stats = self.statistics.stats
        game = self.current_game
        
        # 检查一击必中成就
        if game.attempts == 1:
            print("\n🎯 成就解锁: 一击必中！")
        
        # 检查第一次获胜
        if stats['games_won'] == 1:
            print("\n🌱 成就解锁: 初出茅庐！")
        
        # 检查胜率成就
        if stats['total_games'] >= 10:
            win_rate = (stats['games_won'] / stats['total_games']) * 100
            if win_rate >= 80:
                print("\n👑 成就解锁: 猜数大师！")
    
    def quit_game(self):
        """
        退出游戏
        """
        print("\n👋 感谢游玩！")
        print("希望你喜欢这个游戏！")
        self.running = False


def main():
    """
    主函数 - 程序入口点
    """
    try:
        # 创建数据目录
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # 启动游戏
        game_manager = GameManager()
        game_manager.start()
        
    except KeyboardInterrupt:
        print("\n\n👋 程序被用户中断，再见！")
    except Exception as e:
        if DEBUG_MODE:
            raise
        print(f"\n❌ 程序发生严重错误：{e}")
        print("请检查配置文件或联系开发者")
        input("按回车键退出...")


if __name__ == "__main__":
    main()