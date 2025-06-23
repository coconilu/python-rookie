# Session 16: GUI编程 - Tkinter

## 📖 课程大纲

1. GUI编程简介
2. Tkinter基础
3. 常用控件详解
4. 布局管理器
5. 事件处理机制
6. 综合实践：桌面计算器
7. 高级技巧与最佳实践

## 1. GUI编程简介

### 1.1 什么是GUI？

GUI（Graphical User Interface）即图形用户界面，是一种用户与计算机交互的方式。相比命令行界面，GUI提供了更直观、友好的操作方式。

### 1.2 Python GUI编程选择

Python有多个GUI库可供选择：
- **Tkinter**：Python标准库，跨平台，适合简单应用
- **PyQt**：功能强大，界面美观，学习曲线陡峭
- **Kivy**：适合移动应用开发
- **PySimpleGUI**：简化的GUI开发

本课程选择Tkinter，因为它：
- 内置于Python，无需额外安装
- 简单易学，适合初学者
- 跨平台支持良好
- 文档和资源丰富

## 2. Tkinter基础

### 2.1 第一个Tkinter程序

```python
import tkinter as tk

# 创建主窗口
root = tk.Tk()
root.title("我的第一个GUI程序")
root.geometry("300x200")

# 创建标签
label = tk.Label(root, text="Hello, Tkinter!")
label.pack()

# 运行主循环
root.mainloop()
```

### 2.2 窗口属性设置

```python
# 设置窗口标题
root.title("窗口标题")

# 设置窗口大小
root.geometry("宽度x高度+X坐标+Y坐标")
# 例如：root.geometry("400x300+100+100")

# 设置窗口图标
root.iconbitmap("icon.ico")

# 设置窗口背景色
root.configure(bg="lightblue")

# 设置窗口是否可调整大小
root.resizable(width=False, height=False)
```

## 3. 常用控件详解

### 3.1 Label（标签）

标签用于显示文本或图像：

```python
# 创建文本标签
label = tk.Label(root, text="这是一个标签")

# 设置标签属性
label = tk.Label(
    root,
    text="自定义标签",
    font=("Arial", 16, "bold"),
    fg="blue",  # 前景色
    bg="yellow",  # 背景色
    width=20,  # 宽度
    height=2,  # 高度
    anchor="center"  # 对齐方式
)
```

### 3.2 Button（按钮）

按钮用于触发操作：

```python
def button_click():
    print("按钮被点击了！")

button = tk.Button(
    root,
    text="点击我",
    command=button_click,
    width=10,
    height=2,
    bg="green",
    fg="white",
    font=("Arial", 12)
)
```

### 3.3 Entry（输入框）

单行文本输入：

```python
# 创建输入框
entry = tk.Entry(root, width=30)

# 获取输入内容
text = entry.get()

# 设置输入内容
entry.insert(0, "默认文本")

# 清空输入框
entry.delete(0, tk.END)
```

### 3.4 Text（文本框）

多行文本编辑：

```python
# 创建文本框
text = tk.Text(root, width=40, height=10)

# 插入文本
text.insert(tk.END, "这是一段文本\n")

# 获取文本内容
content = text.get(1.0, tk.END)

# 清空文本框
text.delete(1.0, tk.END)
```

### 3.5 Checkbutton（复选框）

```python
var = tk.IntVar()
check = tk.Checkbutton(
    root,
    text="同意条款",
    variable=var,
    onvalue=1,
    offvalue=0
)

# 获取状态
is_checked = var.get()
```

### 3.6 Radiobutton（单选按钮）

```python
var = tk.StringVar()
var.set("option1")

radio1 = tk.Radiobutton(root, text="选项1", variable=var, value="option1")
radio2 = tk.Radiobutton(root, text="选项2", variable=var, value="option2")
radio3 = tk.Radiobutton(root, text="选项3", variable=var, value="option3")
```

### 3.7 Listbox（列表框）

```python
listbox = tk.Listbox(root, height=5)
listbox.insert(tk.END, "项目1")
listbox.insert(tk.END, "项目2")
listbox.insert(tk.END, "项目3")

# 获取选中项
selection = listbox.curselection()
if selection:
    selected_item = listbox.get(selection[0])
```

### 3.8 Menu（菜单）

```python
menubar = tk.Menu(root)
root.config(menu=menubar)

# 创建文件菜单
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="文件", menu=file_menu)
file_menu.add_command(label="新建", command=new_file)
file_menu.add_command(label="打开", command=open_file)
file_menu.add_separator()
file_menu.add_command(label="退出", command=root.quit)
```

## 4. 布局管理器

Tkinter提供三种布局管理器：

### 4.1 pack布局

最简单的布局方式：

```python
label1.pack()  # 默认从上到下排列
label2.pack(side=tk.LEFT)  # 左对齐
label3.pack(side=tk.RIGHT)  # 右对齐
label4.pack(fill=tk.X)  # 水平填充
label5.pack(expand=True)  # 扩展空间
```

### 4.2 grid布局

网格布局，更精确的控制：

```python
label1.grid(row=0, column=0)
label2.grid(row=0, column=1)
label3.grid(row=1, column=0, columnspan=2)  # 跨列

# 设置间距
label.grid(padx=10, pady=5)

# 设置对齐
label.grid(sticky="w")  # 西(左)对齐
```

### 4.3 place布局

绝对定位：

```python
label.place(x=50, y=100)  # 绝对坐标
label.place(relx=0.5, rely=0.5)  # 相对坐标（0-1）
```

## 5. 事件处理机制

### 5.1 事件绑定

```python
# 方法1：使用command参数（仅适用于Button等）
button = tk.Button(root, text="点击", command=callback)

# 方法2：使用bind方法（通用）
widget.bind("<Button-1>", left_click)  # 左键点击
widget.bind("<Double-Button-1>", double_click)  # 双击
widget.bind("<Enter>", mouse_enter)  # 鼠标进入
widget.bind("<Leave>", mouse_leave)  # 鼠标离开
widget.bind("<Key>", key_press)  # 按键
```

### 5.2 事件类型

常用事件类型：
- `<Button-1>`：鼠标左键点击
- `<Button-2>`：鼠标中键点击
- `<Button-3>`：鼠标右键点击
- `<ButtonRelease-1>`：鼠标左键释放
- `<B1-Motion>`：按住左键移动
- `<Double-Button-1>`：双击左键
- `<Enter>`：鼠标进入控件
- `<Leave>`：鼠标离开控件
- `<FocusIn>`：获得焦点
- `<FocusOut>`：失去焦点
- `<Key>`：任意键按下
- `<Return>`：回车键

### 5.3 事件对象

```python
def handle_event(event):
    print(f"事件类型: {event.type}")
    print(f"鼠标位置: ({event.x}, {event.y})")
    print(f"按键: {event.keysym}")
    print(f"控件: {event.widget}")
```

## 6. 综合实践：桌面计算器

### 6.1 计算器设计

我们将开发一个功能完整的桌面计算器，包括：
- 数字按钮（0-9）
- 运算符按钮（+、-、*、/）
- 功能按钮（清除、等于、小数点）
- 显示屏
- 键盘支持

### 6.2 界面布局

```python
# 使用grid布局创建计算器界面
# 显示屏
display = tk.Entry(root, width=35, borderwidth=5)
display.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# 数字按钮
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '=', '+'
]

row = 1
col = 0
for button_text in buttons:
    button = tk.Button(root, text=button_text, padx=40, pady=20)
    button.grid(row=row, column=col, sticky="nsew")
    col += 1
    if col > 3:
        col = 0
        row += 1
```

### 6.3 功能实现

实现计算逻辑、错误处理、键盘绑定等功能。

## 7. 高级技巧与最佳实践

### 7.1 自定义控件

创建自定义控件类：

```python
class CustomButton(tk.Button):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(
            bg="blue",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            bd=3
        )
```

### 7.2 样式和主题

```python
# 使用ttk获得更现代的外观
from tkinter import ttk

style = ttk.Style()
style.theme_use('clam')  # 使用主题

# 自定义样式
style.configure('Custom.TButton', 
                foreground='blue',
                background='lightgray',
                font=('Arial', 12))
```

### 7.3 响应式设计

```python
# 使窗口内容随窗口大小变化
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
```

### 7.4 多线程处理

```python
import threading

def long_running_task():
    # 耗时操作
    pass

# 在单独线程中运行
thread = threading.Thread(target=long_running_task)
thread.daemon = True
thread.start()
```

### 7.5 打包发布

```python
# 使用PyInstaller打包
# pip install pyinstaller
# pyinstaller --onefile --windowed calculator.py
```

## 📝 练习建议

1. **基础练习**：创建各种控件，熟悉属性设置
2. **布局练习**：使用不同布局管理器创建界面
3. **事件练习**：实现各种交互功能
4. **综合项目**：完成计算器项目，添加更多功能

## 🎯 学习要点总结

1. **掌握基本概念**：窗口、控件、事件、布局
2. **熟悉常用控件**：Label、Button、Entry、Text等
3. **理解布局方式**：pack、grid、place的使用场景
4. **掌握事件处理**：事件绑定和回调函数
5. **实践项目开发**：通过计算器项目综合运用所学知识

GUI编程让你的程序更加友好和专业，继续加油！🚀 