#!/usr/bin/env python3
"""
练习1：创建登录窗口

要求：
1. 创建一个登录窗口，包含：
   - 窗口标题："用户登录"
   - 用户名输入框（带标签）
   - 密码输入框（带标签，输入时显示*）
   - 记住密码复选框
   - 登录按钮和取消按钮
   
2. 功能要求：
   - 点击登录按钮时，检查用户名和密码是否为空
   - 如果为空，显示错误提示
   - 如果不为空，显示欢迎信息
   - 点击取消按钮时，清空输入框
   
3. 布局要求：
   - 使用grid布局
   - 窗口居中显示
   - 适当的间距和对齐

提示：
- 使用Entry控件的show参数隐藏密码
- 使用messagebox显示提示信息
- 使用StringVar()绑定输入框的值
"""

import tkinter as tk
from tkinter import messagebox


def create_login_window():
    """创建登录窗口"""
    # TODO: 创建主窗口
    root = tk.Tk()
    root.title("用户登录")
    
    # TODO: 设置窗口大小和位置（居中）
    # 提示：获取屏幕尺寸，计算中心位置
    
    # TODO: 创建用户名标签和输入框
    
    # TODO: 创建密码标签和输入框（注意show参数）
    
    # TODO: 创建记住密码复选框
    
    # TODO: 创建登录和取消按钮
    
    # TODO: 实现登录功能
    def login():
        """登录功能"""
        pass
    
    # TODO: 实现取消功能
    def cancel():
        """取消功能"""
        pass
    
    root.mainloop()


# 参考答案框架
def create_login_window_solution():
    """登录窗口参考实现"""
    root = tk.Tk()
    root.title("用户登录")
    root.geometry("300x200")
    
    # 窗口居中
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # 创建变量
    username_var = tk.StringVar()
    password_var = tk.StringVar()
    remember_var = tk.IntVar()
    
    # 用户名
    tk.Label(root, text="用户名：").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    username_entry = tk.Entry(root, textvariable=username_var, width=20)
    username_entry.grid(row=0, column=1, padx=10, pady=10)
    username_entry.focus()  # 设置焦点
    
    # 密码
    tk.Label(root, text="密码：").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    password_entry = tk.Entry(root, textvariable=password_var, width=20, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)
    
    # 记住密码
    remember_check = tk.Checkbutton(root, text="记住密码", variable=remember_var)
    remember_check.grid(row=2, column=1, sticky="w", padx=10)
    
    # 按钮框架
    button_frame = tk.Frame(root)
    button_frame.grid(row=3, column=0, columnspan=2, pady=20)
    
    def login():
        username = username_var.get()
        password = password_var.get()
        
        if not username or not password:
            messagebox.showerror("错误", "用户名和密码不能为空！")
            return
        
        # 这里可以添加实际的登录验证逻辑
        remember = "是" if remember_var.get() else "否"
        messagebox.showinfo(
            "登录成功", 
            f"欢迎 {username}！\n记住密码：{remember}"
        )
    
    def cancel():
        username_var.set("")
        password_var.set("")
        remember_var.set(0)
        username_entry.focus()
    
    tk.Button(button_frame, text="登录", command=login, width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="取消", command=cancel, width=10).pack(side=tk.LEFT, padx=5)
    
    # 绑定回车键到登录
    root.bind('<Return>', lambda e: login())
    
    root.mainloop()


if __name__ == "__main__":
    print("练习1：创建登录窗口")
    print("1. 查看练习要求")
    print("2. 运行参考答案")
    
    choice = input("\n请选择 (1-2): ")
    
    if choice == '1':
        print("\n请打开文件查看练习要求，然后完成create_login_window()函数")
        print("完成后运行程序测试你的实现")
        # create_login_window()  # 学生实现
    elif choice == '2':
        print("\n运行参考答案...")
        create_login_window_solution()
    else:
        print("无效选择") 