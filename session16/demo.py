#!/usr/bin/env python3
"""
Session 16: GUI编程 - Tkinter 演示程序
包含：基础控件演示、布局管理器演示、事件处理演示、桌面计算器应用
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math


def demo_basic_widgets():
    """演示基础控件"""
    window = tk.Tk()
    window.title("Tkinter 基础控件演示")
    window.geometry("600x500")
    
    # 标题
    title = tk.Label(window, text="Tkinter 控件演示", font=("Arial", 20, "bold"))
    title.pack(pady=10)
    
    # Frame 容器
    frame1 = tk.LabelFrame(window, text="文本控件", padx=10, pady=10)
    frame1.pack(padx=10, pady=5, fill="x")
    
    # Label 标签
    label = tk.Label(frame1, text="这是一个标签", bg="lightblue", fg="darkblue")
    label.pack(side=tk.LEFT, padx=5)
    
    # Entry 输入框
    entry = tk.Entry(frame1, width=20)
    entry.insert(0, "输入文本")
    entry.pack(side=tk.LEFT, padx=5)
    
    # Button 按钮
    def on_button_click():
        text = entry.get()
        messagebox.showinfo("信息", f"输入的内容是：{text}")
    
    button = tk.Button(frame1, text="点击我", command=on_button_click)
    button.pack(side=tk.LEFT, padx=5)
    
    # Frame 2 - 选择控件
    frame2 = tk.LabelFrame(window, text="选择控件", padx=10, pady=10)
    frame2.pack(padx=10, pady=5, fill="x")
    
    # Checkbutton 复选框
    var1 = tk.IntVar()
    check1 = tk.Checkbutton(frame2, text="选项1", variable=var1)
    check1.pack(side=tk.LEFT, padx=5)
    
    var2 = tk.IntVar()
    check2 = tk.Checkbutton(frame2, text="选项2", variable=var2)
    check2.pack(side=tk.LEFT, padx=5)
    
    # Radiobutton 单选按钮
    radio_var = tk.StringVar()
    radio_var.set("A")
    
    radio1 = tk.Radiobutton(frame2, text="选项A", variable=radio_var, value="A")
    radio1.pack(side=tk.LEFT, padx=5)
    
    radio2 = tk.Radiobutton(frame2, text="选项B", variable=radio_var, value="B")
    radio2.pack(side=tk.LEFT, padx=5)
    
    # Frame 3 - 列表控件
    frame3 = tk.LabelFrame(window, text="列表控件", padx=10, pady=10)
    frame3.pack(padx=10, pady=5, fill="both", expand=True)
    
    # Listbox 列表框
    listbox = tk.Listbox(frame3, height=5)
    items = ["Python", "Java", "C++", "JavaScript", "Go"]
    for item in items:
        listbox.insert(tk.END, item)
    listbox.pack(side=tk.LEFT, padx=5)
    
    # Scrollbar 滚动条
    scrollbar = tk.Scrollbar(frame3)
    scrollbar.pack(side=tk.LEFT, fill=tk.Y)
    
    # Text 文本框
    text = tk.Text(frame3, width=30, height=5, yscrollcommand=scrollbar.set)
    text.insert(tk.END, "这是一个多行文本框\n可以输入多行文本\n支持滚动")
    text.pack(side=tk.LEFT, padx=5)
    
    scrollbar.config(command=text.yview)
    
    # 获取选择结果的按钮
    def show_selections():
        selections = []
        if var1.get():
            selections.append("选项1")
        if var2.get():
            selections.append("选项2")
        selections.append(f"单选：{radio_var.get()}")
        
        list_selection = listbox.curselection()
        if list_selection:
            selections.append(f"列表选择：{listbox.get(list_selection[0])}")
        
        messagebox.showinfo("选择结果", "\n".join(selections))
    
    result_button = tk.Button(window, text="显示选择结果", command=show_selections)
    result_button.pack(pady=10)
    
    window.mainloop()


def demo_layout_managers():
    """演示布局管理器"""
    window = tk.Tk()
    window.title("布局管理器演示")
    window.geometry("700x500")
    
    # 创建笔记本（选项卡）
    notebook = ttk.Notebook(window)
    notebook.pack(fill="both", expand=True)
    
    # Pack 布局演示
    pack_frame = tk.Frame(notebook)
    notebook.add(pack_frame, text="Pack 布局")
    
    tk.Label(pack_frame, text="Pack 布局演示", font=("Arial", 16)).pack(pady=10)
    
    # 顶部按钮
    tk.Button(pack_frame, text="顶部按钮 (默认)", bg="lightblue").pack(pady=5)
    
    # 左右布局
    frame_lr = tk.Frame(pack_frame)
    frame_lr.pack(pady=10)
    tk.Button(frame_lr, text="左侧按钮", bg="lightgreen").pack(side=tk.LEFT, padx=5)
    tk.Button(frame_lr, text="右侧按钮", bg="lightyellow").pack(side=tk.RIGHT, padx=5)
    
    # 填充演示
    tk.Button(pack_frame, text="水平填充 (fill=X)", bg="lightcoral").pack(fill=tk.X, padx=20, pady=5)
    tk.Button(pack_frame, text="垂直填充 (fill=Y)", bg="lightpink").pack(fill=tk.Y, pady=5)
    
    # Grid 布局演示
    grid_frame = tk.Frame(notebook)
    notebook.add(grid_frame, text="Grid 布局")
    
    tk.Label(grid_frame, text="Grid 布局演示", font=("Arial", 16)).grid(row=0, column=0, columnspan=3, pady=10)
    
    # 创建网格
    for i in range(3):
        for j in range(3):
            btn = tk.Button(grid_frame, text=f"按钮({i},{j})", width=10, height=2)
            btn.grid(row=i+1, column=j, padx=5, pady=5)
    
    # 跨列演示
    tk.Button(grid_frame, text="跨两列按钮", bg="lightblue").grid(row=4, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
    tk.Button(grid_frame, text="跨两行按钮", bg="lightgreen", height=4).grid(row=1, column=3, rowspan=2, padx=5, pady=5)
    
    # Place 布局演示
    place_frame = tk.Frame(notebook)
    notebook.add(place_frame, text="Place 布局")
    
    tk.Label(place_frame, text="Place 布局演示", font=("Arial", 16)).place(x=250, y=20)
    
    # 绝对定位
    tk.Button(place_frame, text="绝对定位(50,100)", bg="lightblue").place(x=50, y=100)
    tk.Button(place_frame, text="绝对定位(200,150)", bg="lightgreen").place(x=200, y=150)
    
    # 相对定位
    tk.Button(place_frame, text="相对定位(0.5,0.5)", bg="lightyellow").place(relx=0.5, rely=0.5, anchor="center")
    tk.Button(place_frame, text="相对定位(0.8,0.8)", bg="lightcoral").place(relx=0.8, rely=0.8)
    
    window.mainloop()


def demo_event_handling():
    """演示事件处理"""
    window = tk.Tk()
    window.title("事件处理演示")
    window.geometry("600x500")
    
    # 标题
    tk.Label(window, text="事件处理演示", font=("Arial", 20, "bold")).pack(pady=10)
    
    # 鼠标事件演示
    mouse_frame = tk.LabelFrame(window, text="鼠标事件", padx=20, pady=20)
    mouse_frame.pack(padx=10, pady=10, fill="x")
    
    mouse_label = tk.Label(mouse_frame, text="鼠标事件显示区域", bg="lightgray", width=50, height=5)
    mouse_label.pack()
    
    def on_mouse_enter(event):
        mouse_label.config(text="鼠标进入", bg="lightgreen")
    
    def on_mouse_leave(event):
        mouse_label.config(text="鼠标离开", bg="lightcoral")
    
    def on_mouse_click(event):
        mouse_label.config(text=f"鼠标点击位置: ({event.x}, {event.y})")
    
    def on_mouse_move(event):
        mouse_label.config(text=f"鼠标移动: ({event.x}, {event.y})")
    
    mouse_label.bind("<Enter>", on_mouse_enter)
    mouse_label.bind("<Leave>", on_mouse_leave)
    mouse_label.bind("<Button-1>", on_mouse_click)
    mouse_label.bind("<B1-Motion>", on_mouse_move)
    
    # 键盘事件演示
    keyboard_frame = tk.LabelFrame(window, text="键盘事件", padx=20, pady=20)
    keyboard_frame.pack(padx=10, pady=10, fill="x")
    
    key_entry = tk.Entry(keyboard_frame, width=40, font=("Arial", 12))
    key_entry.pack(pady=5)
    key_entry.focus()
    
    key_label = tk.Label(keyboard_frame, text="按键信息将显示在这里")
    key_label.pack()
    
    def on_key_press(event):
        key_label.config(text=f"按下按键: {event.keysym} (字符: {event.char})")
    
    key_entry.bind("<Key>", on_key_press)
    
    # 焦点事件演示
    focus_frame = tk.LabelFrame(window, text="焦点事件", padx=20, pady=20)
    focus_frame.pack(padx=10, pady=10, fill="x")
    
    def on_focus_in(event):
        event.widget.config(bg="lightyellow")
    
    def on_focus_out(event):
        event.widget.config(bg="white")
    
    for i in range(3):
        entry = tk.Entry(focus_frame, width=20)
        entry.pack(side=tk.LEFT, padx=5)
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        if i == 0:
            entry.insert(0, "点击切换焦点")
    
    # 自定义事件
    custom_frame = tk.LabelFrame(window, text="组合事件", padx=20, pady=20)
    custom_frame.pack(padx=10, pady=10, fill="x")
    
    canvas = tk.Canvas(custom_frame, width=400, height=100, bg="white")
    canvas.pack()
    
    # 绘制提示文字
    canvas.create_text(200, 50, text="在这里点击并拖动绘制", font=("Arial", 12))
    
    def start_draw(event):
        canvas.start_x = event.x
        canvas.start_y = event.y
    
    def draw(event):
        canvas.create_line(canvas.start_x, canvas.start_y, event.x, event.y, width=2)
        canvas.start_x = event.x
        canvas.start_y = event.y
    
    canvas.bind("<Button-1>", start_draw)
    canvas.bind("<B1-Motion>", draw)
    
    window.mainloop()


class Calculator:
    """桌面计算器类"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("桌面计算器")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # 计算器状态
        self.current = ""
        self.result = 0
        self.operation = None
        self.new_num = True
        
        # 创建界面
        self.create_widgets()
        
        # 绑定键盘事件
        self.bind_keyboard()
    
    def create_widgets(self):
        """创建计算器界面"""
        # 显示屏
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        display = tk.Entry(
            self.root,
            textvariable=self.display_var,
            font=("Arial", 24),
            justify="right",
            state="readonly",
            readonlybackground="white"
        )
        display.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="ew")
        
        # 按钮布局
        buttons = [
            ('C', 1, 0, 'red'), ('±', 1, 1, 'gray'), ('%', 1, 2, 'gray'), ('/', 1, 3, 'orange'),
            ('7', 2, 0, 'white'), ('8', 2, 1, 'white'), ('9', 2, 2, 'white'), ('*', 2, 3, 'orange'),
            ('4', 3, 0, 'white'), ('5', 3, 1, 'white'), ('6', 3, 2, 'white'), ('-', 3, 3, 'orange'),
            ('1', 4, 0, 'white'), ('2', 4, 1, 'white'), ('3', 4, 2, 'white'), ('+', 4, 3, 'orange'),
            ('0', 5, 0, 'white'), ('.', 5, 2, 'white'), ('=', 5, 3, 'green')
        ]
        
        # 创建按钮
        for (text, row, col, color) in buttons:
            btn = tk.Button(
                self.root,
                text=text,
                font=("Arial", 18),
                bg=color,
                command=lambda t=text: self.button_click(t)
            )
            if text == '0':
                btn.grid(row=row, column=col, columnspan=2, padx=2, pady=2, sticky="nsew")
            else:
                btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
        
        # 配置网格权重
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
        
        # 添加菜单
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 视图菜单
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="视图", menu=view_menu)
        view_menu.add_command(label="标准", command=lambda: None)
        view_menu.add_command(label="科学", command=self.show_scientific)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=self.show_about)
    
    def button_click(self, char):
        """处理按钮点击"""
        if char.isdigit():
            self.number_click(char)
        elif char == '.':
            self.decimal_click()
        elif char in ['+', '-', '*', '/']:
            self.operation_click(char)
        elif char == '=':
            self.equals_click()
        elif char == 'C':
            self.clear_click()
        elif char == '±':
            self.negate_click()
        elif char == '%':
            self.percent_click()
    
    def number_click(self, num):
        """处理数字按钮"""
        if self.new_num:
            self.current = num
            self.new_num = False
        else:
            if self.current == "0":
                self.current = num
            else:
                self.current += num
        self.display_var.set(self.current)
    
    def decimal_click(self):
        """处理小数点"""
        if self.new_num:
            self.current = "0."
            self.new_num = False
        elif '.' not in self.current:
            self.current += '.'
        self.display_var.set(self.current)
    
    def operation_click(self, op):
        """处理运算符"""
        if not self.new_num:
            self.equals_click()
        self.operation = op
        self.result = float(self.current)
        self.new_num = True
    
    def equals_click(self):
        """处理等号"""
        try:
            current_num = float(self.current)
            if self.operation == '+':
                self.result += current_num
            elif self.operation == '-':
                self.result -= current_num
            elif self.operation == '*':
                self.result *= current_num
            elif self.operation == '/':
                if current_num == 0:
                    self.display_var.set("错误")
                    self.new_num = True
                    return
                self.result /= current_num
            else:
                self.result = current_num
            
            # 格式化结果
            if self.result == int(self.result):
                self.current = str(int(self.result))
            else:
                self.current = str(round(self.result, 10))
            
            self.display_var.set(self.current)
            self.operation = None
            self.new_num = True
        except:
            self.display_var.set("错误")
            self.new_num = True
    
    def clear_click(self):
        """清除"""
        self.current = "0"
        self.result = 0
        self.operation = None
        self.new_num = True
        self.display_var.set("0")
    
    def negate_click(self):
        """正负号"""
        if self.current != "0":
            if self.current[0] == '-':
                self.current = self.current[1:]
            else:
                self.current = '-' + self.current
            self.display_var.set(self.current)
    
    def percent_click(self):
        """百分比"""
        try:
            value = float(self.current) / 100
            self.current = str(value)
            self.display_var.set(self.current)
            self.new_num = True
        except:
            pass
    
    def bind_keyboard(self):
        """绑定键盘事件"""
        self.root.bind('<Key-0>', lambda e: self.button_click('0'))
        self.root.bind('<Key-1>', lambda e: self.button_click('1'))
        self.root.bind('<Key-2>', lambda e: self.button_click('2'))
        self.root.bind('<Key-3>', lambda e: self.button_click('3'))
        self.root.bind('<Key-4>', lambda e: self.button_click('4'))
        self.root.bind('<Key-5>', lambda e: self.button_click('5'))
        self.root.bind('<Key-6>', lambda e: self.button_click('6'))
        self.root.bind('<Key-7>', lambda e: self.button_click('7'))
        self.root.bind('<Key-8>', lambda e: self.button_click('8'))
        self.root.bind('<Key-9>', lambda e: self.button_click('9'))
        self.root.bind('<Key-period>', lambda e: self.button_click('.'))
        self.root.bind('<Key-plus>', lambda e: self.button_click('+'))
        self.root.bind('<Key-minus>', lambda e: self.button_click('-'))
        self.root.bind('<Key-asterisk>', lambda e: self.button_click('*'))
        self.root.bind('<Key-slash>', lambda e: self.button_click('/'))
        self.root.bind('<Key-Return>', lambda e: self.button_click('='))
        self.root.bind('<Key-c>', lambda e: self.button_click('C'))
        self.root.bind('<Key-C>', lambda e: self.button_click('C'))
        self.root.bind('<Key-Escape>', lambda e: self.button_click('C'))
    
    def show_scientific(self):
        """显示科学计算器（扩展功能）"""
        messagebox.showinfo("提示", "科学计算器功能待开发...")
    
    def show_about(self):
        """显示关于信息"""
        messagebox.showinfo(
            "关于",
            "桌面计算器 v1.0\n\n"
            "使用Python Tkinter开发\n"
            "Session 16 演示项目"
        )


def run_calculator():
    """运行计算器"""
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()


def main():
    """主函数"""
    print("=" * 50)
    print("Session 16: GUI编程 - Tkinter 演示")
    print("=" * 50)
    print("\n请选择演示内容：")
    print("1. Tkinter基础控件演示")
    print("2. 布局管理器演示")
    print("3. 事件处理演示")
    print("4. 桌面计算器应用")
    print("0. 退出")
    
    while True:
        choice = input("\n请输入选择 (0-4): ")
        
        if choice == '1':
            print("\n启动基础控件演示...")
            demo_basic_widgets()
        elif choice == '2':
            print("\n启动布局管理器演示...")
            demo_layout_managers()
        elif choice == '3':
            print("\n启动事件处理演示...")
            demo_event_handling()
        elif choice == '4':
            print("\n启动桌面计算器...")
            run_calculator()
        elif choice == '0':
            print("\n感谢使用，再见！")
            break
        else:
            print("无效选择，请重试")


if __name__ == "__main__":
    main() 