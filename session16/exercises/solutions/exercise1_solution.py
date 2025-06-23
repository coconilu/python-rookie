#!/usr/bin/env python3
"""
练习1解答：创建登录窗口
"""

import tkinter as tk
from tkinter import messagebox


def create_login_window():
    """创建登录窗口 - 完整解答"""
    # 创建主窗口
    root = tk.Tk()
    root.title("用户登录")
    root.geometry("350x250")
    
    # 设置窗口居中
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # 禁止调整窗口大小
    root.resizable(False, False)
    
    # 创建变量
    username_var = tk.StringVar()
    password_var = tk.StringVar()
    remember_var = tk.IntVar()
    
    # 创建主框架
    main_frame = tk.Frame(root, padx=20, pady=20)
    main_frame.pack(expand=True)
    
    # 标题
    title_label = tk.Label(
        main_frame, 
        text="欢迎登录系统", 
        font=("Arial", 16, "bold")
    )
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
    
    # 用户名标签和输入框
    tk.Label(main_frame, text="用户名：", font=("Arial", 11)).grid(
        row=1, column=0, padx=5, pady=10, sticky="e"
    )
    username_entry = tk.Entry(
        main_frame, 
        textvariable=username_var, 
        width=20,
        font=("Arial", 11)
    )
    username_entry.grid(row=1, column=1, padx=5, pady=10)
    username_entry.focus()  # 设置初始焦点
    
    # 密码标签和输入框
    tk.Label(main_frame, text="密码：", font=("Arial", 11)).grid(
        row=2, column=0, padx=5, pady=10, sticky="e"
    )
    password_entry = tk.Entry(
        main_frame, 
        textvariable=password_var, 
        width=20,
        show="*",  # 隐藏密码
        font=("Arial", 11)
    )
    password_entry.grid(row=2, column=1, padx=5, pady=10)
    
    # 记住密码复选框
    remember_check = tk.Checkbutton(
        main_frame, 
        text="记住密码", 
        variable=remember_var,
        font=("Arial", 10)
    )
    remember_check.grid(row=3, column=1, sticky="w", padx=5)
    
    # 按钮框架
    button_frame = tk.Frame(main_frame)
    button_frame.grid(row=4, column=0, columnspan=2, pady=20)
    
    # 登录功能
    def login():
        """处理登录"""
        username = username_var.get().strip()
        password = password_var.get().strip()
        
        # 验证输入
        if not username:
            messagebox.showerror("错误", "请输入用户名！")
            username_entry.focus()
            return
        
        if not password:
            messagebox.showerror("错误", "请输入密码！")
            password_entry.focus()
            return
        
        # 模拟登录验证（实际应用中应该连接数据库验证）
        if username == "admin" and password == "123456":
            remember = "是" if remember_var.get() else "否"
            messagebox.showinfo(
                "登录成功", 
                f"欢迎回来，{username}！\n\n记住密码：{remember}"
            )
            # 登录成功后的操作（如打开主窗口）
            root.destroy()
        else:
            messagebox.showerror(
                "登录失败", 
                "用户名或密码错误！\n\n提示：用户名admin，密码123456"
            )
            password_var.set("")  # 清空密码
            password_entry.focus()
    
    # 取消功能
    def cancel():
        """清空输入"""
        username_var.set("")
        password_var.set("")
        remember_var.set(0)
        username_entry.focus()
    
    # 创建按钮
    login_button = tk.Button(
        button_frame,
        text="登录",
        command=login,
        width=10,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 11, "bold"),
        cursor="hand2"
    )
    login_button.pack(side=tk.LEFT, padx=5)
    
    cancel_button = tk.Button(
        button_frame,
        text="取消",
        command=cancel,
        width=10,
        bg="#f44336",
        fg="white",
        font=("Arial", 11),
        cursor="hand2"
    )
    cancel_button.pack(side=tk.LEFT, padx=5)
    
    # 绑定键盘事件
    root.bind('<Return>', lambda e: login())  # 回车键登录
    root.bind('<Escape>', lambda e: cancel())  # ESC键取消
    
    # 添加一些美化效果
    def on_enter(event):
        event.widget.config(relief=tk.SUNKEN)
    
    def on_leave(event):
        event.widget.config(relief=tk.RAISED)
    
    login_button.bind("<Enter>", on_enter)
    login_button.bind("<Leave>", on_leave)
    cancel_button.bind("<Enter>", on_enter)
    cancel_button.bind("<Leave>", on_leave)
    
    # 运行主循环
    root.mainloop()


# 扩展版本：带更多功能的登录窗口
class LoginWindow:
    """登录窗口类 - 更完整的实现"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("用户登录系统")
        self.root.geometry("400x300")
        
        # 变量
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.remember_var = tk.IntVar()
        self.show_password_var = tk.IntVar()
        
        # 尝试次数
        self.login_attempts = 0
        self.max_attempts = 3
        
        self.setup_ui()
        self.center_window()
        
    def setup_ui(self):
        """设置界面"""
        # 主容器
        container = tk.Frame(self.root, bg="white")
        container.pack(fill=tk.BOTH, expand=True)
        
        # 顶部标题区域
        header_frame = tk.Frame(container, bg="#2196F3", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="用户登录",
            font=("Arial", 20, "bold"),
            bg="#2196F3",
            fg="white"
        ).pack(expand=True)
        
        # 登录表单区域
        form_frame = tk.Frame(container, bg="white", padx=40, pady=30)
        form_frame.pack(expand=True)
        
        # 用户名
        tk.Label(
            form_frame,
            text="用户名",
            font=("Arial", 11),
            bg="white"
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.username_entry = tk.Entry(
            form_frame,
            textvariable=self.username_var,
            font=("Arial", 12),
            width=25
        )
        self.username_entry.grid(row=1, column=0, pady=(0, 15))
        
        # 密码
        tk.Label(
            form_frame,
            text="密码",
            font=("Arial", 11),
            bg="white"
        ).grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        password_frame = tk.Frame(form_frame, bg="white")
        password_frame.grid(row=3, column=0, pady=(0, 10))
        
        self.password_entry = tk.Entry(
            password_frame,
            textvariable=self.password_var,
            font=("Arial", 12),
            width=23,
            show="*"
        )
        self.password_entry.pack(side=tk.LEFT)
        
        # 显示/隐藏密码按钮
        self.toggle_btn = tk.Button(
            password_frame,
            text="👁",
            command=self.toggle_password,
            bd=0,
            bg="white",
            cursor="hand2"
        )
        self.toggle_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # 选项
        options_frame = tk.Frame(form_frame, bg="white")
        options_frame.grid(row=4, column=0, sticky="w", pady=(0, 20))
        
        tk.Checkbutton(
            options_frame,
            text="记住密码",
            variable=self.remember_var,
            bg="white",
            font=("Arial", 10)
        ).pack(side=tk.LEFT)
        
        tk.Label(
            options_frame,
            text="忘记密码？",
            font=("Arial", 10),
            bg="white",
            fg="#2196F3",
            cursor="hand2"
        ).pack(side=tk.RIGHT)
        
        # 登录按钮
        self.login_btn = tk.Button(
            form_frame,
            text="登录",
            command=self.login,
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            width=22,
            height=2,
            bd=0,
            cursor="hand2"
        )
        self.login_btn.grid(row=5, column=0)
        
        # 状态标签
        self.status_label = tk.Label(
            form_frame,
            text="",
            font=("Arial", 10),
            bg="white",
            fg="red"
        )
        self.status_label.grid(row=6, column=0, pady=(10, 0))
        
        # 绑定事件
        self.root.bind('<Return>', lambda e: self.login())
        self.username_entry.bind('<Tab>', lambda e: self.password_entry.focus())
        
        # 设置初始焦点
        self.username_entry.focus()
    
    def toggle_password(self):
        """切换密码显示/隐藏"""
        if self.password_entry.cget('show') == '*':
            self.password_entry.config(show='')
            self.toggle_btn.config(text='🙈')
        else:
            self.password_entry.config(show='*')
            self.toggle_btn.config(text='👁')
    
    def login(self):
        """登录验证"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        if not username or not password:
            self.status_label.config(text="请输入用户名和密码")
            return
        
        # 模拟登录验证
        if username == "admin" and password == "123456":
            self.status_label.config(text="登录成功！", fg="green")
            self.root.after(1000, self.root.destroy)
        else:
            self.login_attempts += 1
            remaining = self.max_attempts - self.login_attempts
            
            if remaining > 0:
                self.status_label.config(
                    text=f"用户名或密码错误！剩余尝试次数：{remaining}",
                    fg="red"
                )
            else:
                self.status_label.config(text="登录失败次数过多，请稍后再试")
                self.login_btn.config(state=tk.DISABLED)
    
    def center_window(self):
        """窗口居中"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def run(self):
        """运行窗口"""
        self.root.mainloop()


if __name__ == "__main__":
    print("登录窗口解答演示")
    print("1. 基础版本")
    print("2. 扩展版本（带更多功能）")
    
    choice = input("\n请选择版本 (1-2): ")
    
    if choice == '1':
        create_login_window()
    elif choice == '2':
        app = LoginWindow()
        app.run()
    else:
        print("无效选择") 