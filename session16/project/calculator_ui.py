#!/usr/bin/env python3
"""
计算器UI模块
负责界面布局和显示
"""

import tkinter as tk
from tkinter import ttk
from config import *


class CalculatorUI:
    """计算器UI类"""
    
    def __init__(self, root, calculator):
        self.root = root
        self.calculator = calculator
        self.logic = calculator.logic
        
        # 创建界面
        self.create_widgets()
    
    def create_widgets(self):
        """创建界面控件"""
        # 创建主容器
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建显示屏
        self.create_display(main_frame)
        
        # 创建按钮
        self.create_buttons(main_frame)
        
        # 创建菜单
        self.create_menu()
    
    def create_display(self, parent):
        """创建显示屏"""
        # 显示框架
        display_frame = tk.Frame(parent, bg=BG_COLOR)
        display_frame.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="ew")
        
        # 表达式显示（显示完整的计算式）
        self.expression_var = tk.StringVar()
        self.expression_label = tk.Label(
            display_frame,
            textvariable=self.expression_var,
            font=(FONT_FAMILY, 12),
            bg=DISPLAY_BG,
            fg=DISPLAY_FG,
            anchor="e",
            height=1
        )
        self.expression_label.pack(fill=tk.X)
        
        # 主显示屏
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        self.display = tk.Entry(
            display_frame,
            textvariable=self.display_var,
            font=(FONT_FAMILY, DISPLAY_FONT_SIZE, "bold"),
            justify="right",
            state="readonly",
            readonlybackground=DISPLAY_BG,
            fg=DISPLAY_FG,
            bd=0,
            highlightthickness=2,
            highlightcolor=BUTTON_OPERATOR_BG
        )
        self.display.pack(fill=tk.X, pady=(0, 5))
    
    def create_buttons(self, parent):
        """创建按钮"""
        # 按钮布局
        buttons = [
            # (文本, 行, 列, 列跨度, 类型)
            ('C', 1, 0, 1, 'clear'),
            ('±', 1, 1, 1, 'function'),
            ('%', 1, 2, 1, 'function'),
            ('÷', 1, 3, 1, 'operator'),
            
            ('7', 2, 0, 1, 'number'),
            ('8', 2, 1, 1, 'number'),
            ('9', 2, 2, 1, 'number'),
            ('×', 2, 3, 1, 'operator'),
            
            ('4', 3, 0, 1, 'number'),
            ('5', 3, 1, 1, 'number'),
            ('6', 3, 2, 1, 'number'),
            ('-', 3, 3, 1, 'operator'),
            
            ('1', 4, 0, 1, 'number'),
            ('2', 4, 1, 1, 'number'),
            ('3', 4, 2, 1, 'number'),
            ('+', 4, 3, 1, 'operator'),
            
            ('0', 5, 0, 2, 'number'),
            ('.', 5, 2, 1, 'number'),
            ('=', 5, 3, 1, 'equals'),
        ]
        
        # 创建按钮
        self.buttons = {}
        for (text, row, col, colspan, btn_type) in buttons:
            btn = self.create_button(parent, text, btn_type)
            btn.grid(row=row, column=col, columnspan=colspan, 
                    padx=2, pady=2, sticky="nsew")
            self.buttons[text] = btn
        
        # 配置网格权重
        for i in range(6):
            parent.grid_rowconfigure(i, weight=1)
        for i in range(4):
            parent.grid_columnconfigure(i, weight=1)
    
    def create_button(self, parent, text, btn_type):
        """创建单个按钮"""
        # 根据类型设置样式
        if btn_type == 'number':
            bg = BUTTON_NUMBER_BG
            fg = BUTTON_NUMBER_FG
            active_bg = BUTTON_NUMBER_ACTIVE
        elif btn_type == 'operator':
            bg = BUTTON_OPERATOR_BG
            fg = BUTTON_OPERATOR_FG
            active_bg = BUTTON_OPERATOR_ACTIVE
        elif btn_type == 'equals':
            bg = BUTTON_EQUALS_BG
            fg = BUTTON_EQUALS_FG
            active_bg = BUTTON_EQUALS_ACTIVE
        elif btn_type == 'clear':
            bg = BUTTON_CLEAR_BG
            fg = BUTTON_CLEAR_FG
            active_bg = BUTTON_CLEAR_ACTIVE
        else:  # function
            bg = BUTTON_FUNCTION_BG
            fg = BUTTON_FUNCTION_FG
            active_bg = BUTTON_FUNCTION_ACTIVE
        
        # 创建按钮
        btn = tk.Button(
            parent,
            text=text,
            font=(FONT_FAMILY, BUTTON_FONT_SIZE, "bold"),
            bg=bg,
            fg=fg,
            activebackground=active_bg,
            bd=0,
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self.on_button_click(text)
        )
        
        # 添加悬停效果
        btn.bind("<Enter>", lambda e: btn.config(bg=active_bg))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        
        return btn
    
    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 查看菜单
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="查看", menu=view_menu)
        view_menu.add_command(label="标准", command=lambda: None)
        view_menu.add_command(label="科学", command=self.show_scientific_mode)
        view_menu.add_separator()
        view_menu.add_command(label="历史记录", command=self.calculator.show_history)
        
        # 编辑菜单
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="编辑", menu=edit_menu)
        edit_menu.add_command(label="复制", command=self.copy_result)
        edit_menu.add_command(label="粘贴", command=self.paste_number)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="使用说明", command=self.show_help)
        help_menu.add_separator()
        help_menu.add_command(label="关于", command=self.show_about)
    
    def on_button_click(self, text):
        """处理按钮点击"""
        if text in '0123456789':
            self.on_number_click(text)
        elif text == '.':
            self.on_decimal_click()
        elif text in ['+', '-', '×', '÷']:
            # 转换显示符号为实际运算符
            operator = text
            if text == '×':
                operator = '*'
            elif text == '÷':
                operator = '/'
            self.on_operator_click(operator)
        elif text == '=':
            self.on_equals_click()
        elif text == 'C':
            self.on_clear_click()
        elif text == '±':
            self.on_negate_click()
        elif text == '%':
            self.on_percent_click()
    
    def on_number_click(self, num):
        """处理数字点击"""
        current = self.logic.get_display()
        
        if self.logic.new_number:
            self.logic.set_display(num)
            self.logic.new_number = False
        else:
            if current == "0":
                self.logic.set_display(num)
            else:
                self.logic.set_display(current + num)
        
        self.update_display()
    
    def on_decimal_click(self):
        """处理小数点"""
        current = self.logic.get_display()
        
        if self.logic.new_number:
            self.logic.set_display("0.")
            self.logic.new_number = False
        elif '.' not in current:
            self.logic.set_display(current + '.')
        
        self.update_display()
    
    def on_operator_click(self, operator):
        """处理运算符"""
        try:
            if not self.logic.new_number:
                self.on_equals_click()
            
            self.logic.set_operator(operator)
            self.update_expression()
        except Exception as e:
            self.show_error(str(e))
    
    def on_equals_click(self):
        """处理等号"""
        try:
            result = self.logic.calculate()
            if result is not None:
                # 添加到历史记录
                expression = self.expression_var.get()
                self.calculator.add_to_history(expression, result)
                
                self.update_display()
                self.expression_var.set("")
        except Exception as e:
            self.show_error(str(e))
    
    def on_clear_click(self):
        """处理清除"""
        self.logic.clear()
        self.update_display()
        self.expression_var.set("")
    
    def on_negate_click(self):
        """处理正负号"""
        try:
            self.logic.negate()
            self.update_display()
        except Exception as e:
            self.show_error(str(e))
    
    def on_percent_click(self):
        """处理百分比"""
        try:
            self.logic.percent()
            self.update_display()
        except Exception as e:
            self.show_error(str(e))
    
    def on_backspace_click(self):
        """处理退格"""
        current = self.logic.get_display()
        if len(current) > 1:
            self.logic.set_display(current[:-1])
        else:
            self.logic.set_display("0")
        self.update_display()
    
    def update_display(self):
        """更新显示"""
        self.display_var.set(self.logic.get_display())
    
    def update_expression(self):
        """更新表达式显示"""
        if self.logic.operation and self.logic.first_number is not None:
            op_symbol = self.logic.operation
            if op_symbol == '*':
                op_symbol = '×'
            elif op_symbol == '/':
                op_symbol = '÷'
            self.expression_var.set(f"{self.logic.first_number} {op_symbol}")
    
    def show_error(self, message):
        """显示错误"""
        self.display_var.set("错误")
        self.expression_var.set(message)
    
    def copy_result(self):
        """复制结果"""
        self.root.clipboard_clear()
        self.root.clipboard_append(self.display_var.get())
    
    def paste_number(self):
        """粘贴数字"""
        try:
            text = self.root.clipboard_get()
            # 验证是否为有效数字
            float(text)
            self.logic.set_display(text)
            self.update_display()
        except:
            pass
    
    def show_scientific_mode(self):
        """显示科学模式（待实现）"""
        tk.messagebox.showinfo("提示", "科学计算器模式待开发...")
    
    def show_help(self):
        """显示帮助"""
        help_text = """桌面计算器使用说明：
        
1. 基本运算：点击数字和运算符进行计算
2. 键盘快捷键：
   - 数字 0-9：输入数字
   - + - * /：四则运算
   - Enter：计算结果
   - C/Esc：清除
   - Backspace：退格
   
3. 特殊功能：
   - ±：切换正负号
   - %：百分比计算
   - .：输入小数点
   
4. 菜单功能：
   - 查看历史记录
   - 复制/粘贴结果"""
        
        tk.messagebox.showinfo("使用说明", help_text)
    
    def show_about(self):
        """显示关于"""
        about_text = """桌面计算器 v1.0
        
使用Python Tkinter开发
Session 16 项目实践

作者：Python学习者
许可：MIT License"""
        
        tk.messagebox.showinfo("关于", about_text) 