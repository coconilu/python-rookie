#!/usr/bin/env python3
"""
练习2解答：待办事项列表应用（简化版）
"""

import tkinter as tk
from tkinter import messagebox


def create_todo_app():
    """创建待办事项应用 - 基础版解答"""
    root = tk.Tk()
    root.title("待办事项列表")
    root.geometry("400x500")
    
    # 待办事项列表（存储数据）
    todos = []
    
    # 顶部输入区域
    input_frame = tk.Frame(root)
    input_frame.pack(fill=tk.X, padx=10, pady=10)
    
    # 输入框
    input_var = tk.StringVar()
    input_entry = tk.Entry(
        input_frame,
        textvariable=input_var,
        font=("Arial", 12)
    )
    input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
    
    # 添加功能
    def add_todo():
        """添加待办事项"""
        todo_text = input_var.get().strip()
        
        if not todo_text:
            messagebox.showwarning("警告", "请输入待办事项内容！")
            return
        
        # 添加到列表
        todos.append(todo_text)
        listbox.insert(tk.END, todo_text)
        
        # 清空输入框
        input_var.set("")
        input_entry.focus()
        
        # 更新状态栏
        update_status()
    
    # 添加按钮
    add_button = tk.Button(
        input_frame,
        text="添加",
        command=add_todo,
        bg="green",
        fg="white",
        font=("Arial", 10, "bold"),
        width=8
    )
    add_button.pack(side=tk.LEFT)
    
    # 绑定回车键
    input_entry.bind('<Return>', lambda e: add_todo())
    
    # 列表框区域
    list_frame = tk.Frame(root)
    list_frame.pack(fill=tk.BOTH, expand=True, padx=10)
    
    # 滚动条
    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # 列表框
    listbox = tk.Listbox(
        list_frame,
        yscrollcommand=scrollbar.set,
        font=("Arial", 11),
        selectmode=tk.SINGLE,
        height=15
    )
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=listbox.yview)
    
    # 删除功能
    def delete_todo():
        """删除选中的事项"""
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择要删除的事项！")
            return
        
        # 确认删除
        if messagebox.askyesno("确认", "确定要删除选中的事项吗？"):
            index = selection[0]
            listbox.delete(index)
            del todos[index]
            update_status()
    
    # 清空功能
    def clear_all():
        """清空所有事项"""
        if not todos:
            messagebox.showinfo("提示", "列表已经是空的！")
            return
        
        if messagebox.askyesno("确认", "确定要清空所有待办事项吗？"):
            listbox.delete(0, tk.END)
            todos.clear()
            update_status()
    
    # 编辑功能（双击）
    def edit_todo(event):
        """编辑待办事项"""
        selection = listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        current_text = todos[index]
        
        # 创建简单的输入对话框
        new_text = tk.simpledialog.askstring(
            "编辑事项",
            "请修改待办事项：",
            initialvalue=current_text
        )
        
        if new_text and new_text.strip():
            todos[index] = new_text.strip()
            listbox.delete(index)
            listbox.insert(index, new_text.strip())
    
    # 绑定双击事件
    listbox.bind('<Double-Button-1>', edit_todo)
    
    # 操作按钮区域
    button_frame = tk.Frame(root)
    button_frame.pack(fill=tk.X, padx=10, pady=10)
    
    tk.Button(
        button_frame,
        text="删除选中",
        command=delete_todo,
        bg="red",
        fg="white",
        width=10
    ).pack(side=tk.LEFT, padx=2)
    
    tk.Button(
        button_frame,
        text="清空所有",
        command=clear_all,
        bg="orange",
        fg="white",
        width=10
    ).pack(side=tk.LEFT, padx=2)
    
    # 状态栏
    status_var = tk.StringVar()
    status_bar = tk.Label(
        root,
        textvariable=status_var,
        bd=1,
        relief=tk.SUNKEN,
        anchor=tk.W
    )
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    # 更新状态栏
    def update_status():
        """更新状态栏"""
        count = len(todos)
        status_var.set(f"待办事项数量：{count}")
    
    # 初始化
    update_status()
    input_entry.focus()
    
    # 导入simpledialog（用于编辑功能）
    from tkinter import simpledialog
    
    root.mainloop()


# 中级版本：带完成标记功能
def create_todo_app_intermediate():
    """创建待办事项应用 - 中级版"""
    root = tk.Tk()
    root.title("待办事项列表 - 中级版")
    root.geometry("450x550")
    
    # 使用Frame来组织每个待办事项
    class TodoItem(tk.Frame):
        def __init__(self, parent, text, on_delete, on_update, **kwargs):
            super().__init__(parent, **kwargs)
            self.text = text
            self.completed = False
            self.on_delete = on_delete
            self.on_update = on_update
            
            # 复选框
            self.var = tk.IntVar()
            self.check = tk.Checkbutton(
                self,
                variable=self.var,
                command=self.toggle_complete
            )
            self.check.pack(side=tk.LEFT)
            
            # 文本标签
            self.label = tk.Label(
                self,
                text=text,
                font=("Arial", 11),
                anchor="w"
            )
            self.label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            
            # 删除按钮
            self.delete_btn = tk.Button(
                self,
                text="×",
                command=lambda: on_delete(self),
                fg="red",
                font=("Arial", 16),
                bd=0,
                padx=5
            )
            self.delete_btn.pack(side=tk.RIGHT)
            
            # 绑定双击编辑
            self.label.bind('<Double-Button-1>', self.edit)
        
        def toggle_complete(self):
            """切换完成状态"""
            self.completed = bool(self.var.get())
            if self.completed:
                self.label.config(fg="gray", font=("Arial", 11, "overstrike"))
            else:
                self.label.config(fg="black", font=("Arial", 11))
            self.on_update()
        
        def edit(self, event):
            """编辑事项"""
            from tkinter import simpledialog
            new_text = simpledialog.askstring(
                "编辑事项",
                "请修改待办事项：",
                initialvalue=self.text
            )
            if new_text and new_text.strip():
                self.text = new_text.strip()
                self.label.config(text=self.text)
    
    # 待办事项容器
    todo_items = []
    
    # 顶部输入区域
    input_frame = tk.Frame(root, bg="lightgray", pady=10)
    input_frame.pack(fill=tk.X)
    
    input_var = tk.StringVar()
    input_entry = tk.Entry(
        input_frame,
        textvariable=input_var,
        font=("Arial", 12),
        width=30
    )
    input_entry.pack(side=tk.LEFT, padx=(10, 5))
    
    def add_todo():
        text = input_var.get().strip()
        if not text:
            messagebox.showwarning("警告", "请输入待办事项内容！")
            return
        
        # 创建新的待办事项
        item = TodoItem(
            container,
            text,
            delete_item,
            update_status,
            bg="white",
            relief=tk.RAISED,
            bd=1
        )
        item.pack(fill=tk.X, padx=5, pady=2)
        todo_items.append(item)
        
        input_var.set("")
        input_entry.focus()
        update_status()
    
    tk.Button(
        input_frame,
        text="添加",
        command=add_todo,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=20
    ).pack(side=tk.LEFT)
    
    input_entry.bind('<Return>', lambda e: add_todo())
    
    # 滚动容器
    canvas_frame = tk.Frame(root)
    canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    canvas = tk.Canvas(canvas_frame, bg="white")
    scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    
    container = tk.Frame(canvas, bg="white")
    container.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=container, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # 删除事项
    def delete_item(item):
        if messagebox.askyesno("确认", "确定要删除这个事项吗？"):
            todo_items.remove(item)
            item.destroy()
            update_status()
    
    # 批量操作
    action_frame = tk.Frame(root)
    action_frame.pack(fill=tk.X, padx=10, pady=5)
    
    def clear_completed():
        completed = [item for item in todo_items if item.completed]
        if not completed:
            messagebox.showinfo("提示", "没有已完成的事项")
            return
        
        if messagebox.askyesno("确认", f"确定要清除 {len(completed)} 个已完成的事项吗？"):
            for item in completed:
                todo_items.remove(item)
                item.destroy()
            update_status()
    
    tk.Button(
        action_frame,
        text="清除已完成",
        command=clear_completed,
        bg="#FF9800",
        fg="white"
    ).pack(side=tk.LEFT, padx=2)
    
    # 状态栏
    status_var = tk.StringVar()
    status_bar = tk.Label(
        root,
        textvariable=status_var,
        bd=1,
        relief=tk.SUNKEN,
        anchor=tk.W
    )
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_status():
        total = len(todo_items)
        completed = sum(1 for item in todo_items if item.completed)
        pending = total - completed
        status_var.set(f"总计: {total} | 待完成: {pending} | 已完成: {completed}")
    
    update_status()
    input_entry.focus()
    
    root.mainloop()


if __name__ == "__main__":
    print("待办事项列表应用 - 解答")
    print("1. 基础版本")
    print("2. 中级版本（带完成标记）")
    
    choice = input("\n请选择版本 (1-2): ")
    
    if choice == '1':
        create_todo_app()
    elif choice == '2':
        create_todo_app_intermediate()
    else:
        print("无效选择") 