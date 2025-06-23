#!/usr/bin/env python3
"""
示例3：事件处理和高级控件
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import datetime


def example1_event_binding():
    """事件绑定示例"""
    root = tk.Tk()
    root.title("事件绑定示例")
    root.geometry("600x500")
    
    # 事件日志
    log_frame = tk.LabelFrame(root, text="事件日志", padx=10, pady=10)
    log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # 创建文本框和滚动条
    scrollbar = tk.Scrollbar(log_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    log_text = tk.Text(log_frame, height=15, yscrollcommand=scrollbar.set)
    log_text.pack(fill=tk.BOTH, expand=True)
    scrollbar.config(command=log_text.yview)
    
    def log_event(event_name, event=None):
        """记录事件到日志"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {event_name}"
        
        if event:
            if hasattr(event, 'x') and hasattr(event, 'y'):
                log_entry += f" - 位置: ({event.x}, {event.y})"
            if hasattr(event, 'keysym'):
                log_entry += f" - 按键: {event.keysym}"
            if hasattr(event, 'char') and event.char:
                log_entry += f" - 字符: {event.char}"
        
        log_text.insert(tk.END, log_entry + "\n")
        log_text.see(tk.END)  # 自动滚动到底部
    
    # 创建测试区域
    test_frame = tk.LabelFrame(root, text="测试区域", padx=20, pady=20)
    test_frame.pack(padx=10, pady=10, fill=tk.X)
    
    # 创建一个标签用于测试鼠标事件
    test_label = tk.Label(
        test_frame, 
        text="在这里测试鼠标事件", 
        bg="lightgray",
        width=30,
        height=5,
        relief=tk.RAISED,
        bd=2
    )
    test_label.pack(side=tk.LEFT, padx=10)
    
    # 绑定鼠标事件
    test_label.bind("<Button-1>", lambda e: log_event("鼠标左键点击", e))
    test_label.bind("<Button-2>", lambda e: log_event("鼠标中键点击", e))
    test_label.bind("<Button-3>", lambda e: log_event("鼠标右键点击", e))
    test_label.bind("<Double-Button-1>", lambda e: log_event("鼠标左键双击", e))
    test_label.bind("<B1-Motion>", lambda e: log_event("鼠标拖动", e))
    test_label.bind("<Enter>", lambda e: log_event("鼠标进入"))
    test_label.bind("<Leave>", lambda e: log_event("鼠标离开"))
    test_label.bind("<MouseWheel>", lambda e: log_event(f"鼠标滚轮: {e.delta}"))
    
    # 创建输入框测试键盘事件
    test_entry = tk.Entry(test_frame, width=30, font=("Arial", 12))
    test_entry.pack(side=tk.LEFT, padx=10)
    
    # 绑定键盘事件
    test_entry.bind("<Key>", lambda e: log_event("按键", e))
    test_entry.bind("<Return>", lambda e: log_event("回车键"))
    test_entry.bind("<FocusIn>", lambda e: log_event("获得焦点"))
    test_entry.bind("<FocusOut>", lambda e: log_event("失去焦点"))
    test_entry.bind("<Control-a>", lambda e: log_event("Ctrl+A"))
    test_entry.bind("<Control-c>", lambda e: log_event("Ctrl+C"))
    test_entry.bind("<Control-v>", lambda e: log_event("Ctrl+V"))
    
    # 清除日志按钮
    tk.Button(
        root, 
        text="清除日志",
        command=lambda: log_text.delete(1.0, tk.END)
    ).pack(pady=5)
    
    root.mainloop()


def example2_menu_and_toolbar():
    """菜单和工具栏示例"""
    root = tk.Tk()
    root.title("菜单和工具栏示例")
    root.geometry("700x500")
    
    # 创建主文本区域
    text_area = tk.Text(root, wrap=tk.WORD)
    text_area.pack(fill=tk.BOTH, expand=True)
    
    # 创建菜单栏
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    # 文件菜单
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="文件", menu=file_menu)
    
    def new_file():
        text_area.delete(1.0, tk.END)
        root.title("新文件 - 菜单和工具栏示例")
    
    def open_file():
        filename = filedialog.askopenfilename(
            title="打开文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if filename:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                text_area.delete(1.0, tk.END)
                text_area.insert(1.0, content)
            root.title(f"{filename} - 菜单和工具栏示例")
    
    def save_file():
        filename = filedialog.asksaveasfilename(
            title="保存文件",
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if filename:
            with open(filename, 'w', encoding='utf-8') as file:
                content = text_area.get(1.0, tk.END)
                file.write(content)
            messagebox.showinfo("保存成功", f"文件已保存到：{filename}")
    
    file_menu.add_command(label="新建", command=new_file, accelerator="Ctrl+N")
    file_menu.add_command(label="打开", command=open_file, accelerator="Ctrl+O")
    file_menu.add_command(label="保存", command=save_file, accelerator="Ctrl+S")
    file_menu.add_separator()
    file_menu.add_command(label="退出", command=root.quit, accelerator="Ctrl+Q")
    
    # 编辑菜单
    edit_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="编辑", menu=edit_menu)
    
    edit_menu.add_command(label="撤销", accelerator="Ctrl+Z")
    edit_menu.add_command(label="重做", accelerator="Ctrl+Y")
    edit_menu.add_separator()
    edit_menu.add_command(label="剪切", accelerator="Ctrl+X")
    edit_menu.add_command(label="复制", accelerator="Ctrl+C")
    edit_menu.add_command(label="粘贴", accelerator="Ctrl+V")
    
    # 格式菜单
    format_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="格式", menu=format_menu)
    
    # 字体子菜单
    font_menu = tk.Menu(format_menu, tearoff=0)
    format_menu.add_cascade(label="字体", menu=font_menu)
    
    fonts = ["Arial", "Times New Roman", "Courier New", "微软雅黑"]
    for font in fonts:
        font_menu.add_radiobutton(label=font)
    
    # 字号子菜单
    size_menu = tk.Menu(format_menu, tearoff=0)
    format_menu.add_cascade(label="字号", menu=size_menu)
    
    sizes = [8, 10, 12, 14, 16, 18, 20, 24]
    for size in sizes:
        size_menu.add_radiobutton(label=str(size))
    
    # 帮助菜单
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="帮助", menu=help_menu)
    
    def show_about():
        messagebox.showinfo(
            "关于",
            "菜单和工具栏示例\n\n"
            "演示如何创建菜单栏和工具栏\n"
            "版本 1.0"
        )
    
    help_menu.add_command(label="帮助文档", command=lambda: messagebox.showinfo("帮助", "这是帮助文档"))
    help_menu.add_separator()
    help_menu.add_command(label="关于", command=show_about)
    
    # 创建工具栏
    toolbar = tk.Frame(root, bg="lightgray", height=35)
    toolbar.pack(side=tk.TOP, fill=tk.X)
    toolbar.pack_propagate(False)
    
    # 工具栏按钮
    tk.Button(toolbar, text="新建", command=new_file).pack(side=tk.LEFT, padx=2, pady=2)
    tk.Button(toolbar, text="打开", command=open_file).pack(side=tk.LEFT, padx=2, pady=2)
    tk.Button(toolbar, text="保存", command=save_file).pack(side=tk.LEFT, padx=2, pady=2)
    
    tk.Label(toolbar, text="|", bg="lightgray").pack(side=tk.LEFT, padx=5)
    
    tk.Button(toolbar, text="剪切").pack(side=tk.LEFT, padx=2, pady=2)
    tk.Button(toolbar, text="复制").pack(side=tk.LEFT, padx=2, pady=2)
    tk.Button(toolbar, text="粘贴").pack(side=tk.LEFT, padx=2, pady=2)
    
    # 右键菜单
    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="剪切")
    context_menu.add_command(label="复制")
    context_menu.add_command(label="粘贴")
    context_menu.add_separator()
    context_menu.add_command(label="全选")
    
    def show_context_menu(event):
        context_menu.post(event.x_root, event.y_root)
    
    text_area.bind("<Button-3>", show_context_menu)
    
    # 快捷键绑定
    root.bind("<Control-n>", lambda e: new_file())
    root.bind("<Control-o>", lambda e: open_file())
    root.bind("<Control-s>", lambda e: save_file())
    root.bind("<Control-q>", lambda e: root.quit())
    
    root.mainloop()


def example3_dialogs():
    """对话框示例"""
    root = tk.Tk()
    root.title("对话框示例")
    root.geometry("600x400")
    
    # 创建按钮框架
    button_frame = tk.Frame(root)
    button_frame.pack(expand=True)
    
    # 结果显示标签
    result_label = tk.Label(root, text="点击按钮查看各种对话框", font=("Arial", 12))
    result_label.pack(pady=20)
    
    # 消息对话框
    def show_info():
        messagebox.showinfo("信息", "这是一个信息对话框")
    
    def show_warning():
        messagebox.showwarning("警告", "这是一个警告对话框")
    
    def show_error():
        messagebox.showerror("错误", "这是一个错误对话框")
    
    def show_question():
        result = messagebox.askquestion("询问", "你喜欢Python吗？")
        result_label.config(text=f"你的回答：{result}")
    
    def show_okcancel():
        result = messagebox.askokcancel("确认", "确定要继续吗？")
        result_label.config(text=f"你的选择：{'确定' if result else '取消'}")
    
    def show_yesno():
        result = messagebox.askyesno("选择", "是否保存更改？")
        result_label.config(text=f"你的选择：{'是' if result else '否'}")
    
    def show_retrycancel():
        result = messagebox.askretrycancel("重试", "操作失败，是否重试？")
        result_label.config(text=f"你的选择：{'重试' if result else '取消'}")
    
    # 文件对话框
    def open_file_dialog():
        filename = filedialog.askopenfilename(
            title="选择文件",
            initialdir="/",
            filetypes=[
                ("Python文件", "*.py"),
                ("文本文件", "*.txt"),
                ("所有文件", "*.*")
            ]
        )
        if filename:
            result_label.config(text=f"选择的文件：{filename}")
    
    def save_file_dialog():
        filename = filedialog.asksaveasfilename(
            title="保存文件",
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if filename:
            result_label.config(text=f"保存到：{filename}")
    
    def choose_directory():
        directory = filedialog.askdirectory(title="选择目录")
        if directory:
            result_label.config(text=f"选择的目录：{directory}")
    
    # 颜色选择对话框
    def choose_color():
        color = colorchooser.askcolor(title="选择颜色")
        if color[1]:  # color[1]是十六进制颜色值
            result_label.config(text=f"选择的颜色：{color[1]}", bg=color[1])
    
    # 创建按钮
    # 消息对话框按钮
    msg_frame = tk.LabelFrame(button_frame, text="消息对话框", padx=10, pady=10)
    msg_frame.grid(row=0, column=0, padx=10, pady=10)
    
    tk.Button(msg_frame, text="信息", command=show_info, width=15).pack(pady=2)
    tk.Button(msg_frame, text="警告", command=show_warning, width=15).pack(pady=2)
    tk.Button(msg_frame, text="错误", command=show_error, width=15).pack(pady=2)
    
    # 询问对话框按钮
    ask_frame = tk.LabelFrame(button_frame, text="询问对话框", padx=10, pady=10)
    ask_frame.grid(row=0, column=1, padx=10, pady=10)
    
    tk.Button(ask_frame, text="Question", command=show_question, width=15).pack(pady=2)
    tk.Button(ask_frame, text="OK/Cancel", command=show_okcancel, width=15).pack(pady=2)
    tk.Button(ask_frame, text="Yes/No", command=show_yesno, width=15).pack(pady=2)
    tk.Button(ask_frame, text="Retry/Cancel", command=show_retrycancel, width=15).pack(pady=2)
    
    # 文件对话框按钮
    file_frame = tk.LabelFrame(button_frame, text="文件对话框", padx=10, pady=10)
    file_frame.grid(row=1, column=0, padx=10, pady=10)
    
    tk.Button(file_frame, text="打开文件", command=open_file_dialog, width=15).pack(pady=2)
    tk.Button(file_frame, text="保存文件", command=save_file_dialog, width=15).pack(pady=2)
    tk.Button(file_frame, text="选择目录", command=choose_directory, width=15).pack(pady=2)
    
    # 其他对话框按钮
    other_frame = tk.LabelFrame(button_frame, text="其他对话框", padx=10, pady=10)
    other_frame.grid(row=1, column=1, padx=10, pady=10)
    
    tk.Button(other_frame, text="选择颜色", command=choose_color, width=15).pack(pady=2)
    
    root.mainloop()


def example4_advanced_widgets():
    """高级控件示例"""
    root = tk.Tk()
    root.title("高级控件示例")
    root.geometry("800x600")
    
    # 创建Notebook（选项卡）
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Tab 1: 进度条和滑块
    tab1 = tk.Frame(notebook)
    notebook.add(tab1, text="进度条和滑块")
    
    # 进度条
    tk.Label(tab1, text="进度条演示", font=("Arial", 12, "bold")).pack(pady=10)
    
    # 确定进度条
    progress1 = ttk.Progressbar(tab1, length=400, mode='determinate')
    progress1.pack(pady=5)
    
    def update_progress():
        current = progress1['value']
        if current < 100:
            progress1['value'] = current + 10
        else:
            progress1['value'] = 0
    
    tk.Button(tab1, text="增加进度", command=update_progress).pack(pady=5)
    
    # 不确定进度条
    progress2 = ttk.Progressbar(tab1, length=400, mode='indeterminate')
    progress2.pack(pady=5)
    
    def toggle_progress():
        if progress2.cget('mode') == 'indeterminate':
            progress2.stop()
            progress2.configure(mode='determinate')
        else:
            progress2.configure(mode='indeterminate')
            progress2.start(10)
    
    tk.Button(tab1, text="启动/停止", command=toggle_progress).pack(pady=5)
    
    # 滑块
    tk.Label(tab1, text="滑块演示", font=("Arial", 12, "bold")).pack(pady=20)
    
    # 水平滑块
    scale_var = tk.DoubleVar()
    scale_label = tk.Label(tab1, text="当前值：0")
    scale_label.pack()
    
    def on_scale_change(value):
        scale_label.config(text=f"当前值：{float(value):.1f}")
    
    scale = tk.Scale(
        tab1,
        from_=0,
        to=100,
        orient=tk.HORIZONTAL,
        length=400,
        variable=scale_var,
        command=on_scale_change
    )
    scale.pack(pady=5)
    
    # Tab 2: 树形视图
    tab2 = tk.Frame(notebook)
    notebook.add(tab2, text="树形视图")
    
    # 创建Treeview
    tree = ttk.Treeview(tab2, columns=('size', 'modified'), height=15)
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # 定义列
    tree.heading('#0', text='名称')
    tree.heading('size', text='大小')
    tree.heading('modified', text='修改时间')
    
    # 添加数据
    root_node = tree.insert('', 'end', text='根目录', open=True)
    
    # 添加文件夹
    folder1 = tree.insert(root_node, 'end', text='文档', values=('', '2024-01-01'))
    folder2 = tree.insert(root_node, 'end', text='图片', values=('', '2024-01-02'))
    
    # 添加文件
    tree.insert(folder1, 'end', text='readme.txt', values=('2 KB', '2024-01-01'))
    tree.insert(folder1, 'end', text='report.docx', values=('156 KB', '2024-01-02'))
    tree.insert(folder2, 'end', text='photo1.jpg', values=('2.3 MB', '2024-01-03'))
    tree.insert(folder2, 'end', text='photo2.png', values=('1.5 MB', '2024-01-04'))
    
    # 添加滚动条
    scrollbar = tk.Scrollbar(tab2, orient=tk.VERTICAL, command=tree.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Tab 3: Canvas画布
    tab3 = tk.Frame(notebook)
    notebook.add(tab3, text="画布")
    
    # 创建Canvas
    canvas = tk.Canvas(tab3, bg="white", width=600, height=400)
    canvas.pack(padx=10, pady=10)
    
    # 绘制各种图形
    # 矩形
    canvas.create_rectangle(50, 50, 150, 100, fill="red", outline="black", width=2)
    canvas.create_text(100, 125, text="矩形", font=("Arial", 12))
    
    # 椭圆
    canvas.create_oval(200, 50, 300, 100, fill="green", outline="black", width=2)
    canvas.create_text(250, 125, text="椭圆", font=("Arial", 12))
    
    # 多边形
    points = [350, 50, 400, 100, 450, 75]
    canvas.create_polygon(points, fill="blue", outline="black", width=2)
    canvas.create_text(400, 125, text="三角形", font=("Arial", 12))
    
    # 线条
    canvas.create_line(50, 200, 150, 250, width=3, fill="purple")
    canvas.create_text(100, 270, text="线条", font=("Arial", 12))
    
    # 弧形
    canvas.create_arc(200, 200, 300, 250, start=0, extent=180, fill="orange", outline="black", width=2)
    canvas.create_text(250, 270, text="弧形", font=("Arial", 12))
    
    # 文字
    canvas.create_text(400, 225, text="Canvas\n画布", font=("Arial", 20, "bold"), fill="navy")
    
    # 图片（需要图片文件）
    # photo = tk.PhotoImage(file="image.png")
    # canvas.create_image(500, 300, image=photo)
    
    root.mainloop()


if __name__ == "__main__":
    print("事件处理和高级控件示例")
    print("1. 事件绑定")
    print("2. 菜单和工具栏")
    print("3. 对话框")
    print("4. 高级控件")
    
    choice = input("\n请选择示例 (1-4): ")
    
    if choice == '1':
        example1_event_binding()
    elif choice == '2':
        example2_menu_and_toolbar()
    elif choice == '3':
        example3_dialogs()
    elif choice == '4':
        example4_advanced_widgets()
    else:
        print("无效选择") 