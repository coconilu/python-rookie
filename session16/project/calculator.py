#!/usr/bin/env python3
"""
桌面计算器主程序
一个功能完整的GUI计算器应用
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math
from calculator_ui import CalculatorUI
from calculator_logic import CalculatorLogic
from config import *


class Calculator:
    """计算器主类"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(MIN_WIDTH, MIN_HEIGHT)
        
        # 设置应用图标（如果有）
        try:
            self.root.iconbitmap("calculator.ico")
        except:
            pass
        
        # 初始化计算逻辑
        self.logic = CalculatorLogic()
        
        # 初始化UI
        self.ui = CalculatorUI(root, self)
        
        # 绑定键盘事件
        self.bind_keyboard_events()
        
        # 历史记录
        self.history = []
        
        # 设置窗口居中
        self.center_window()
    
    def center_window(self):
        """窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def bind_keyboard_events(self):
        """绑定键盘事件"""
        # 数字键
        for i in range(10):
            self.root.bind(f'<Key-{i}>', lambda e, num=str(i): self.ui.on_number_click(num))
            self.root.bind(f'<KP_{i}>', lambda e, num=str(i): self.ui.on_number_click(num))
        
        # 运算符
        self.root.bind('<Key-plus>', lambda e: self.ui.on_operator_click('+'))
        self.root.bind('<KP_Add>', lambda e: self.ui.on_operator_click('+'))
        self.root.bind('<Key-minus>', lambda e: self.ui.on_operator_click('-'))
        self.root.bind('<KP_Subtract>', lambda e: self.ui.on_operator_click('-'))
        self.root.bind('<Key-asterisk>', lambda e: self.ui.on_operator_click('*'))
        self.root.bind('<KP_Multiply>', lambda e: self.ui.on_operator_click('*'))
        self.root.bind('<Key-slash>', lambda e: self.ui.on_operator_click('/'))
        self.root.bind('<KP_Divide>', lambda e: self.ui.on_operator_click('/'))
        
        # 功能键
        self.root.bind('<Key-period>', lambda e: self.ui.on_decimal_click())
        self.root.bind('<KP_Decimal>', lambda e: self.ui.on_decimal_click())
        self.root.bind('<Return>', lambda e: self.ui.on_equals_click())
        self.root.bind('<KP_Enter>', lambda e: self.ui.on_equals_click())
        self.root.bind('<Key-c>', lambda e: self.ui.on_clear_click())
        self.root.bind('<Key-C>', lambda e: self.ui.on_clear_click())
        self.root.bind('<Escape>', lambda e: self.ui.on_clear_click())
        self.root.bind('<BackSpace>', lambda e: self.ui.on_backspace_click())
        
        # 百分比和正负号
        self.root.bind('<Key-percent>', lambda e: self.ui.on_percent_click())
        self.root.bind('<Key-n>', lambda e: self.ui.on_negate_click())
    
    def add_to_history(self, expression, result):
        """添加到历史记录"""
        self.history.append(f"{expression} = {result}")
        if len(self.history) > MAX_HISTORY:
            self.history.pop(0)
    
    def show_history(self):
        """显示历史记录"""
        if not self.history:
            messagebox.showinfo("历史记录", "暂无计算历史")
            return
        
        history_window = tk.Toplevel(self.root)
        history_window.title("计算历史")
        history_window.geometry("300x400")
        
        # 创建列表框显示历史
        listbox = tk.Listbox(history_window, font=("Arial", 11))
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for item in self.history:
            listbox.insert(tk.END, item)
        
        # 清除历史按钮
        def clear_history():
            self.history.clear()
            listbox.delete(0, tk.END)
        
        tk.Button(
            history_window,
            text="清除历史",
            command=clear_history
        ).pack(pady=5)
    
    def run(self):
        """运行计算器"""
        self.root.mainloop()


def main():
    """主函数"""
    root = tk.Tk()
    app = Calculator(root)
    app.run()


if __name__ == "__main__":
    main() 