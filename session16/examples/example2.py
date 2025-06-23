#!/usr/bin/env python3
"""
示例2：布局管理器 - pack、grid、place
"""

import tkinter as tk
from tkinter import ttk


def example1_pack_layout():
    """Pack布局示例"""
    root = tk.Tk()
    root.title("Pack布局示例")
    root.geometry("600x400")
    
    # 顶部标题
    title = tk.Label(root, text="Pack布局演示", font=("Arial", 16, "bold"), bg="lightgray")
    title.pack(fill=tk.X, pady=5)
    
    # 创建三个Frame演示不同的pack选项
    # Frame 1: side选项
    frame1 = tk.LabelFrame(root, text="side选项", padx=10, pady=10)
    frame1.pack(fill=tk.X, padx=10, pady=5)
    
    tk.Button(frame1, text="LEFT", bg="red").pack(side=tk.LEFT, padx=2)
    tk.Button(frame1, text="LEFT", bg="green").pack(side=tk.LEFT, padx=2)
    tk.Button(frame1, text="RIGHT", bg="blue").pack(side=tk.RIGHT, padx=2)
    tk.Button(frame1, text="RIGHT", bg="yellow").pack(side=tk.RIGHT, padx=2)
    
    # Frame 2: fill选项
    frame2 = tk.LabelFrame(root, text="fill选项", padx=10, pady=10)
    frame2.pack(fill=tk.X, padx=10, pady=5)
    
    tk.Button(frame2, text="fill=X", bg="lightblue").pack(fill=tk.X, pady=2)
    tk.Button(frame2, text="fill=NONE (默认)", bg="lightgreen").pack(pady=2)
    
    # Frame 3: expand选项
    frame3 = tk.LabelFrame(root, text="expand选项", padx=10, pady=10)
    frame3.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    tk.Button(frame3, text="expand=True, fill=BOTH", bg="pink").pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
    
    # 底部信息
    info = tk.Label(root, text="Pack布局：简单但灵活，适合线性布局", bg="lightyellow")
    info.pack(side=tk.BOTTOM, fill=tk.X)
    
    root.mainloop()


def example2_grid_layout():
    """Grid布局示例"""
    root = tk.Tk()
    root.title("Grid布局示例")
    root.geometry("600x500")
    
    # 标题
    title = tk.Label(root, text="Grid布局演示", font=("Arial", 16, "bold"))
    title.grid(row=0, column=0, columnspan=4, pady=10)
    
    # 创建一个计算器风格的布局
    # 显示屏
    display = tk.Entry(root, width=30, font=("Arial", 14), justify="right")
    display.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
    display.insert(0, "0")
    
    # 按钮
    buttons = [
        ['7', '8', '9', '/'],
        ['4', '5', '6', '*'],
        ['1', '2', '3', '-'],
        ['0', '.', '=', '+']
    ]
    
    for i, row in enumerate(buttons):
        for j, text in enumerate(row):
            btn = tk.Button(
                root, 
                text=text, 
                width=5, 
                height=2,
                font=("Arial", 12)
            )
            btn.grid(row=i+2, column=j, padx=2, pady=2, sticky="nsew")
    
    # 特殊按钮
    clear_btn = tk.Button(root, text="Clear", bg="red", fg="white")
    clear_btn.grid(row=6, column=0, columnspan=2, padx=2, pady=2, sticky="ew")
    
    # 演示sticky选项
    frame = tk.LabelFrame(root, text="sticky选项演示", padx=10, pady=10)
    frame.grid(row=7, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
    
    # 在frame中创建网格
    tk.Label(frame, text="N", bg="lightblue").grid(row=0, column=1, sticky="n", padx=5, pady=5)
    tk.Label(frame, text="S", bg="lightgreen").grid(row=2, column=1, sticky="s", padx=5, pady=5)
    tk.Label(frame, text="W", bg="lightyellow").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    tk.Label(frame, text="E", bg="lightcoral").grid(row=1, column=2, sticky="e", padx=5, pady=5)
    tk.Label(frame, text="CENTER", bg="lightgray").grid(row=1, column=1, padx=5, pady=5)
    
    # 配置网格权重
    for i in range(4):
        root.grid_columnconfigure(i, weight=1)
    
    root.mainloop()


def example3_place_layout():
    """Place布局示例"""
    root = tk.Tk()
    root.title("Place布局示例")
    root.geometry("600x500")
    root.configure(bg="white")
    
    # 标题
    title = tk.Label(root, text="Place布局演示", font=("Arial", 16, "bold"), bg="white")
    title.place(x=200, y=10)
    
    # 绝对定位示例
    abs_frame = tk.LabelFrame(root, text="绝对定位", width=250, height=200, bg="lightyellow")
    abs_frame.place(x=20, y=50)
    abs_frame.pack_propagate(False)  # 防止frame收缩
    
    tk.Label(abs_frame, text="x=20, y=20", bg="red").place(x=20, y=20)
    tk.Label(abs_frame, text="x=100, y=50", bg="green").place(x=100, y=50)
    tk.Label(abs_frame, text="x=50, y=100", bg="blue").place(x=50, y=100)
    
    # 相对定位示例
    rel_frame = tk.LabelFrame(root, text="相对定位", width=250, height=200, bg="lightblue")
    rel_frame.place(x=300, y=50)
    rel_frame.pack_propagate(False)
    
    tk.Label(rel_frame, text="relx=0.5, rely=0.5", bg="yellow").place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(rel_frame, text="relx=0, rely=0", bg="orange").place(relx=0, rely=0)
    tk.Label(rel_frame, text="relx=1, rely=1", bg="purple").place(relx=1, rely=1, anchor="se")
    
    # 混合定位示例
    mix_frame = tk.LabelFrame(root, text="混合定位与anchor", width=550, height=150, bg="lightgreen")
    mix_frame.place(x=20, y=280)
    mix_frame.pack_propagate(False)
    
    # anchor选项演示
    anchors = ['nw', 'n', 'ne', 'w', 'center', 'e', 'sw', 's', 'se']
    positions = [
        (0, 0), (0.5, 0), (1, 0),
        (0, 0.5), (0.5, 0.5), (1, 0.5),
        (0, 1), (0.5, 1), (1, 1)
    ]
    
    for anchor, (rx, ry) in zip(anchors, positions):
        btn = tk.Button(mix_frame, text=anchor, width=6)
        btn.place(relx=rx, rely=ry, anchor=anchor)
    
    # 信息标签
    info = tk.Label(
        root, 
        text="Place布局：精确控制位置，适合复杂界面设计",
        bg="white",
        font=("Arial", 10)
    )
    info.place(x=150, y=450)
    
    root.mainloop()


def example4_mixed_layout():
    """混合布局示例"""
    root = tk.Tk()
    root.title("混合布局示例")
    root.geometry("700x500")
    
    # 使用pack创建主要区域
    # 顶部工具栏
    toolbar = tk.Frame(root, bg="darkgray", height=40)
    toolbar.pack(side=tk.TOP, fill=tk.X)
    toolbar.pack_propagate(False)
    
    # 工具栏按钮使用pack
    tk.Button(toolbar, text="新建").pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(toolbar, text="打开").pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(toolbar, text="保存").pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(toolbar, text="退出").pack(side=tk.RIGHT, padx=5, pady=5)
    
    # 主要内容区域
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # 左侧面板使用pack
    left_panel = tk.Frame(main_frame, bg="lightblue", width=200)
    left_panel.pack(side=tk.LEFT, fill=tk.Y)
    left_panel.pack_propagate(False)
    
    # 左侧面板内容使用grid
    tk.Label(left_panel, text="导航面板", font=("Arial", 12, "bold"), bg="lightblue").grid(row=0, column=0, pady=10)
    
    nav_items = ["首页", "文档", "设置", "帮助", "关于"]
    for i, item in enumerate(nav_items):
        btn = tk.Button(left_panel, text=item, width=15)
        btn.grid(row=i+1, column=0, padx=10, pady=5)
    
    # 右侧内容区域
    right_panel = tk.Frame(main_frame, bg="white")
    right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    # 右侧使用place放置一些浮动元素
    floating_box = tk.Frame(right_panel, bg="yellow", width=150, height=100, relief=tk.RAISED, bd=2)
    floating_box.place(relx=0.8, rely=0.1)
    tk.Label(floating_box, text="浮动窗口\n(Place布局)", bg="yellow").pack(expand=True)
    
    # 中心内容使用grid
    content_frame = tk.Frame(right_panel, bg="white")
    content_frame.pack(expand=True)
    
    tk.Label(content_frame, text="混合布局示例", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
    tk.Label(content_frame, text="这个示例展示了如何混合使用三种布局管理器：").grid(row=1, column=0, columnspan=2, pady=5)
    tk.Label(content_frame, text="• Pack：用于主要区域划分", anchor="w").grid(row=2, column=0, sticky="w", padx=20)
    tk.Label(content_frame, text="• Grid：用于规则的表格布局", anchor="w").grid(row=3, column=0, sticky="w", padx=20)
    tk.Label(content_frame, text="• Place：用于精确定位的元素", anchor="w").grid(row=4, column=0, sticky="w", padx=20)
    
    # 底部状态栏
    statusbar = tk.Label(root, text="就绪", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    statusbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    root.mainloop()


if __name__ == "__main__":
    print("布局管理器示例")
    print("1. Pack布局")
    print("2. Grid布局")
    print("3. Place布局")
    print("4. 混合布局")
    
    choice = input("\n请选择示例 (1-4): ")
    
    if choice == '1':
        example1_pack_layout()
    elif choice == '2':
        example2_grid_layout()
    elif choice == '3':
        example3_place_layout()
    elif choice == '4':
        example4_mixed_layout()
    else:
        print("无效选择") 