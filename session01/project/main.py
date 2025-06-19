#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session01 演示项目：交互式计算器

这是一个功能完整的交互式计算器程序，演示了Session01学到的所有概念：
- 变量的使用
- 用户输入输出
- 基本数学运算
- 错误处理
- 程序结构设计

功能特性：
1. 支持基本四则运算
2. 支持高级运算（幂运算、开方等）
3. 美观的用户界面
4. 完善的错误处理
5. 历史记录功能
6. 帮助系统

作者: Python教程团队
创建日期: 2024-01-01
版本: 1.0.0
"""

import math
from typing import List, Tuple


class Calculator:
    """
    交互式计算器类
    """
    
    def __init__(self):
        """
        初始化计算器
        """
        self.history: List[str] = []  # 计算历史
        self.version = "1.0.0"
        self.author = "Python教程团队"
    
    def display_welcome(self):
        """
        显示欢迎信息
        """
        welcome_text = f"""
╔══════════════════════════════════════════╗
║            交互式计算器 v{self.version}            ║
╠══════════════════════════════════════════╣
║  欢迎使用Python交互式计算器！            ║
║  支持基本运算和高级数学函数              ║
║  输入 'help' 查看帮助，'quit' 退出       ║
╚══════════════════════════════════════════╝
        """
        print(welcome_text)
    
    def display_help(self):
        """
        显示帮助信息
        """
        help_text = """
╔══════════════════════════════════════════╗
║                 帮助信息                 ║
╠══════════════════════════════════════════╣
║ 基本运算：                               ║
║   add <a> <b>     - 加法运算             ║
║   sub <a> <b>     - 减法运算             ║
║   mul <a> <b>     - 乘法运算             ║
║   div <a> <b>     - 除法运算             ║
║                                          ║
║ 高级运算：                               ║
║   pow <a> <b>     - 幂运算 (a^b)         ║
║   sqrt <a>        - 开平方根             ║
║   abs <a>         - 绝对值               ║
║                                          ║
║ 其他命令：                               ║
║   history         - 查看计算历史         ║
║   clear           - 清除历史记录         ║
║   help            - 显示此帮助           ║
║   quit            - 退出程序             ║
╚══════════════════════════════════════════╝
        """
        print(help_text)
    
    def add_to_history(self, operation: str, result: float):
        """
        添加计算记录到历史
        
        Args:
            operation: 运算表达式
            result: 计算结果
        """
        self.history.append(f"{operation} = {result}")
    
    def display_history(self):
        """
        显示计算历史
        """
        if not self.history:
            print("📝 暂无计算历史")
            return
        
        print("\n╔══════════════════════════════════════════╗")
        print("║                计算历史                  ║")
        print("╠══════════════════════════════════════════╣")
        
        for i, record in enumerate(self.history[-10:], 1):  # 只显示最近10条
            print(f"║ {i:2d}. {record:<35} ║")
        
        print("╚══════════════════════════════════════════╝")
    
    def clear_history(self):
        """
        清除计算历史
        """
        self.history.clear()
        print("✅ 历史记录已清除")
    
    def safe_float_input(self, prompt: str) -> float:
        """
        安全的浮点数输入
        
        Args:
            prompt: 输入提示
        
        Returns:
            用户输入的浮点数
        """
        while True:
            try:
                value = float(input(prompt))
                return value
            except ValueError:
                print("❌ 请输入有效的数字！")
    
    def add(self, a: float, b: float) -> float:
        """
        加法运算
        """
        result = a + b
        operation = f"{a} + {b}"
        self.add_to_history(operation, result)
        return result
    
    def subtract(self, a: float, b: float) -> float:
        """
        减法运算
        """
        result = a - b
        operation = f"{a} - {b}"
        self.add_to_history(operation, result)
        return result
    
    def multiply(self, a: float, b: float) -> float:
        """
        乘法运算
        """
        result = a * b
        operation = f"{a} × {b}"
        self.add_to_history(operation, result)
        return result
    
    def divide(self, a: float, b: float) -> float:
        """
        除法运算
        """
        if b == 0:
            raise ValueError("除数不能为零")
        
        result = a / b
        operation = f"{a} ÷ {b}"
        self.add_to_history(operation, result)
        return result
    
    def power(self, a: float, b: float) -> float:
        """
        幂运算
        """
        result = a ** b
        operation = f"{a} ^ {b}"
        self.add_to_history(operation, result)
        return result
    
    def square_root(self, a: float) -> float:
        """
        开平方根
        """
        if a < 0:
            raise ValueError("负数不能开平方根")
        
        result = math.sqrt(a)
        operation = f"√{a}"
        self.add_to_history(operation, result)
        return result
    
    def absolute(self, a: float) -> float:
        """
        绝对值
        """
        result = abs(a)
        operation = f"|{a}|"
        self.add_to_history(operation, result)
        return result
    
    def process_command(self, command: str) -> bool:
        """
        处理用户命令
        
        Args:
            command: 用户输入的命令
        
        Returns:
            是否继续运行程序
        """
        parts = command.strip().lower().split()
        
        if not parts:
            return True
        
        cmd = parts[0]
        
        try:
            if cmd == "quit":
                return False
            
            elif cmd == "help":
                self.display_help()
            
            elif cmd == "history":
                self.display_history()
            
            elif cmd == "clear":
                self.clear_history()
            
            elif cmd == "add":
                if len(parts) != 3:
                    print("❌ 用法: add <数字1> <数字2>")
                else:
                    a, b = float(parts[1]), float(parts[2])
                    result = self.add(a, b)
                    print(f"✅ 结果: {a} + {b} = {result}")
            
            elif cmd == "sub":
                if len(parts) != 3:
                    print("❌ 用法: sub <数字1> <数字2>")
                else:
                    a, b = float(parts[1]), float(parts[2])
                    result = self.subtract(a, b)
                    print(f"✅ 结果: {a} - {b} = {result}")
            
            elif cmd == "mul":
                if len(parts) != 3:
                    print("❌ 用法: mul <数字1> <数字2>")
                else:
                    a, b = float(parts[1]), float(parts[2])
                    result = self.multiply(a, b)
                    print(f"✅ 结果: {a} × {b} = {result}")
            
            elif cmd == "div":
                if len(parts) != 3:
                    print("❌ 用法: div <数字1> <数字2>")
                else:
                    a, b = float(parts[1]), float(parts[2])
                    result = self.divide(a, b)
                    print(f"✅ 结果: {a} ÷ {b} = {result}")
            
            elif cmd == "pow":
                if len(parts) != 3:
                    print("❌ 用法: pow <底数> <指数>")
                else:
                    a, b = float(parts[1]), float(parts[2])
                    result = self.power(a, b)
                    print(f"✅ 结果: {a} ^ {b} = {result}")
            
            elif cmd == "sqrt":
                if len(parts) != 2:
                    print("❌ 用法: sqrt <数字>")
                else:
                    a = float(parts[1])
                    result = self.square_root(a)
                    print(f"✅ 结果: √{a} = {result}")
            
            elif cmd == "abs":
                if len(parts) != 2:
                    print("❌ 用法: abs <数字>")
                else:
                    a = float(parts[1])
                    result = self.absolute(a)
                    print(f"✅ 结果: |{a}| = {result}")
            
            else:
                print(f"❌ 未知命令: {cmd}")
                print("💡 输入 'help' 查看可用命令")
        
        except ValueError as e:
            print(f"❌ 错误: {e}")
        except Exception as e:
            print(f"❌ 发生错误: {e}")
        
        return True
    
    def run(self):
        """
        运行计算器主程序
        """
        self.display_welcome()
        
        while True:
            try:
                command = input("\n🧮 请输入命令 (输入 'help' 查看帮助): ")
                
                if not self.process_command(command):
                    break
            
            except KeyboardInterrupt:
                print("\n\n👋 感谢使用计算器，再见！")
                break
            except EOFError:
                print("\n\n👋 感谢使用计算器，再见！")
                break
        
        # 显示退出信息
        print("\n" + "=" * 50)
        print(f"📊 本次会话共进行了 {len(self.history)} 次计算")
        print(f"💻 计算器版本: {self.version}")
        print(f"👨‍💻 开发团队: {self.author}")
        print("🎓 这是Session01的演示项目")
        print("=" * 50)
        print("👋 感谢使用，继续学习Python吧！")


def main():
    """
    主函数
    """
    calculator = Calculator()
    calculator.run()


if __name__ == "__main__":
    main()