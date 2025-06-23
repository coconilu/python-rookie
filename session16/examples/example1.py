#!/usr/bin/env python3
"""
示例1：Tkinter基础 - 创建窗口和基本控件
"""

import tkinter as tk
from tkinter import messagebox


def example1_basic_window():
    """创建基本窗口"""
    # 创建主窗口
    root = tk.Tk()
    
    # 设置窗口属性
    root.title("我的第一个Tkinter窗口")
    root.geometry("400x300")  # 宽x高
    root.configure(bg="lightblue")  # 背景色
    
    # 创建标签
    label = tk.Label(
        root, 
        text="欢迎使用Tkinter！",
        font=("Arial", 16, "bold"),
        fg="darkblue",
        bg="lightblue"
    )
    label.pack(pady=20)
    
    # 创建按钮
    def on_button_click():
        messagebox.showinfo("提示", "你点击了按钮！")
    
    button = tk.Button(
        root,
        text="点击我",
        command=on_button_click,
        width=15,
        height=2,
        bg="green",
        fg="white"
    )
    button.pack()
    
    # 运行主循环
    root.mainloop()


def example2_basic_widgets():
    """基本控件组合示例"""
    root = tk.Tk()
    root.title("基本控件示例")
    root.geometry("500x400")
    
    # 标题
    title = tk.Label(root, text="用户信息表单", font=("Arial", 18, "bold"))
    title.pack(pady=10)
    
    # 输入框示例
    frame1 = tk.Frame(root, padx=20, pady=10)
    frame1.pack()
    
    tk.Label(frame1, text="姓名：", width=10).grid(row=0, column=0, sticky="e")
    name_entry = tk.Entry(frame1, width=20)
    name_entry.grid(row=0, column=1, padx=5)
    
    tk.Label(frame1, text="年龄：", width=10).grid(row=1, column=0, sticky="e")
    age_entry = tk.Entry(frame1, width=20)
    age_entry.grid(row=1, column=1, padx=5)
    
    # 单选按钮示例
    frame2 = tk.Frame(root, padx=20, pady=10)
    frame2.pack()
    
    tk.Label(frame2, text="性别：").pack(side=tk.LEFT)
    gender_var = tk.StringVar()
    gender_var.set("male")
    
    male_radio = tk.Radiobutton(frame2, text="男", variable=gender_var, value="male")
    male_radio.pack(side=tk.LEFT, padx=5)
    
    female_radio = tk.Radiobutton(frame2, text="女", variable=gender_var, value="female")
    female_radio.pack(side=tk.LEFT, padx=5)
    
    # 复选框示例
    frame3 = tk.Frame(root, padx=20, pady=10)
    frame3.pack()
    
    tk.Label(frame3, text="爱好：").pack(side=tk.LEFT)
    
    hobby_vars = []
    hobbies = ["阅读", "运动", "音乐", "旅游"]
    for hobby in hobbies:
        var = tk.IntVar()
        check = tk.Checkbutton(frame3, text=hobby, variable=var)
        check.pack(side=tk.LEFT, padx=5)
        hobby_vars.append((hobby, var))
    
    # 文本框示例
    frame4 = tk.Frame(root, padx=20, pady=10)
    frame4.pack()
    
    tk.Label(frame4, text="自我介绍：").pack(anchor="w")
    text_box = tk.Text(frame4, width=40, height=5)
    text_box.pack()
    
    # 提交按钮
    def submit_form():
        name = name_entry.get()
        age = age_entry.get()
        gender = "男" if gender_var.get() == "male" else "女"
        hobbies = [hobby for hobby, var in hobby_vars if var.get()]
        intro = text_box.get(1.0, tk.END).strip()
        
        info = f"姓名：{name}\n"
        info += f"年龄：{age}\n"
        info += f"性别：{gender}\n"
        info += f"爱好：{', '.join(hobbies)}\n"
        info += f"自我介绍：{intro}"
        
        messagebox.showinfo("提交成功", info)
    
    submit_button = tk.Button(
        root,
        text="提交",
        command=submit_form,
        bg="blue",
        fg="white",
        padx=20,
        pady=5
    )
    submit_button.pack(pady=10)
    
    root.mainloop()


def example3_window_properties():
    """窗口属性设置示例"""
    root = tk.Tk()
    
    # 窗口标题
    root.title("窗口属性示例")
    
    # 窗口大小和位置
    # 格式：宽度x高度+X坐标+Y坐标
    root.geometry("500x400+100+100")
    
    # 设置最小和最大尺寸
    root.minsize(300, 200)
    root.maxsize(800, 600)
    
    # 设置窗口是否可调整大小
    # root.resizable(False, False)  # 禁止调整
    
    # 设置窗口透明度（0.0-1.0）
    root.attributes('-alpha', 0.95)
    
    # 设置窗口置顶
    # root.attributes('-topmost', True)
    
    # 设置窗口图标（需要.ico文件）
    # root.iconbitmap("icon.ico")
    
    # 内容
    info_text = """窗口属性设置：
    
    1. 标题：窗口属性示例
    2. 大小：500x400
    3. 位置：(100, 100)
    4. 最小尺寸：300x200
    5. 最大尺寸：800x600
    6. 透明度：95%
    
    试着调整窗口大小看看效果！
    """
    
    label = tk.Label(
        root,
        text=info_text,
        justify="left",
        padx=20,
        pady=20
    )
    label.pack()
    
    # 获取窗口信息
    def show_window_info():
        info = f"窗口大小：{root.winfo_width()}x{root.winfo_height()}\n"
        info += f"窗口位置：({root.winfo_x()}, {root.winfo_y()})\n"
        info += f"屏幕大小：{root.winfo_screenwidth()}x{root.winfo_screenheight()}"
        messagebox.showinfo("窗口信息", info)
    
    button = tk.Button(root, text="显示窗口信息", command=show_window_info)
    button.pack()
    
    root.mainloop()


if __name__ == "__main__":
    print("Tkinter基础示例")
    print("1. 基本窗口")
    print("2. 基本控件组合")
    print("3. 窗口属性设置")
    
    choice = input("\n请选择示例 (1-3): ")
    
    if choice == '1':
        example1_basic_window()
    elif choice == '2':
        example2_basic_widgets()
    elif choice == '3':
        example3_window_properties()
    else:
        print("无效选择") 