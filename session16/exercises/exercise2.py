#!/usr/bin/env python3
"""
练习2：待办事项列表应用

要求：
1. 创建一个待办事项管理窗口，包含：
   - 输入框：用于输入新的待办事项
   - 添加按钮：添加新事项到列表
   - 列表框：显示所有待办事项
   - 删除按钮：删除选中的事项
   - 清空按钮：清空所有事项
   - 状态栏：显示当前事项数量
   
2. 功能要求：
   - 输入框为空时不能添加
   - 支持回车键快速添加
   - 双击列表项可以编辑
   - 删除前需要确认
   
3. 额外功能（可选）：
   - 支持事项标记为完成（使用Checkbutton）
   - 支持保存和加载待办事项（使用文件）
   - 添加优先级功能

提示：
- 使用Listbox显示待办事项
- 使用bind方法绑定事件
- 使用messagebox.askyesno()进行确认
"""

import tkinter as tk
from tkinter import messagebox
import json
import os


def create_todo_app():
    """创建待办事项应用"""
    root = tk.Tk()
    root.title("待办事项列表")
    root.geometry("400x500")
    
    # TODO: 创建输入框和添加按钮
    
    # TODO: 创建列表框（使用Listbox）
    
    # TODO: 创建操作按钮（删除、清空）
    
    # TODO: 创建状态栏
    
    # TODO: 实现添加功能
    def add_todo():
        """添加待办事项"""
        pass
    
    # TODO: 实现删除功能
    def delete_todo():
        """删除选中的事项"""
        pass
    
    # TODO: 实现清空功能
    def clear_all():
        """清空所有事项"""
        pass
    
    # TODO: 实现更新状态栏
    def update_status():
        """更新状态栏"""
        pass
    
    root.mainloop()


# 参考答案 - 完整实现
class TodoApp:
    """待办事项应用类"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("待办事项列表")
        self.root.geometry("450x600")
        
        # 数据文件
        self.data_file = "todos.json"
        self.todos = []
        
        # 创建界面
        self.create_widgets()
        
        # 加载数据
        self.load_todos()
        
        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """创建界面控件"""
        # 顶部框架 - 输入区域
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(
            top_frame, 
            textvariable=self.input_var,
            font=("Arial", 12)
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.input_entry.bind('<Return>', lambda e: self.add_todo())
        
        self.add_button = tk.Button(
            top_frame,
            text="添加",
            command=self.add_todo,
            bg="green",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.add_button.pack(side=tk.LEFT)
        
        # 中间框架 - 列表区域
        middle_frame = tk.Frame(self.root)
        middle_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # 列表框和滚动条
        scrollbar = tk.Scrollbar(middle_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(
            middle_frame,
            yscrollcommand=scrollbar.set,
            font=("Arial", 11),
            selectmode=tk.SINGLE
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # 绑定双击编辑
        self.listbox.bind('<Double-Button-1>', self.edit_todo)
        
        # 底部框架 - 操作按钮
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(
            button_frame,
            text="标记完成",
            command=self.toggle_complete,
            bg="blue",
            fg="white"
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            button_frame,
            text="删除",
            command=self.delete_todo,
            bg="red",
            fg="white"
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            button_frame,
            text="清空所有",
            command=self.clear_all,
            bg="orange",
            fg="white"
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            button_frame,
            text="上移",
            command=lambda: self.move_todo(-1)
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            button_frame,
            text="下移",
            command=lambda: self.move_todo(1)
        ).pack(side=tk.LEFT, padx=2)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.update_status()
    
    def add_todo(self):
        """添加待办事项"""
        todo_text = self.input_var.get().strip()
        
        if not todo_text:
            messagebox.showwarning("警告", "请输入待办事项内容！")
            return
        
        # 添加到列表
        todo_item = {
            "text": todo_text,
            "completed": False
        }
        self.todos.append(todo_item)
        
        # 更新显示
        self.refresh_listbox()
        
        # 清空输入框
        self.input_var.set("")
        self.input_entry.focus()
        
        # 保存数据
        self.save_todos()
    
    def delete_todo(self):
        """删除选中的事项"""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择要删除的事项！")
            return
        
        if messagebox.askyesno("确认", "确定要删除选中的事项吗？"):
            index = selection[0]
            del self.todos[index]
            self.refresh_listbox()
            self.save_todos()
    
    def clear_all(self):
        """清空所有事项"""
        if not self.todos:
            messagebox.showinfo("提示", "列表已经是空的！")
            return
        
        if messagebox.askyesno("确认", "确定要清空所有待办事项吗？"):
            self.todos.clear()
            self.refresh_listbox()
            self.save_todos()
    
    def toggle_complete(self):
        """切换完成状态"""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择要标记的事项！")
            return
        
        index = selection[0]
        self.todos[index]["completed"] = not self.todos[index]["completed"]
        self.refresh_listbox()
        self.save_todos()
        
        # 保持选中状态
        self.listbox.selection_set(index)
    
    def edit_todo(self, event):
        """编辑待办事项"""
        selection = self.listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        current_text = self.todos[index]["text"]
        
        # 创建编辑对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("编辑待办事项")
        dialog.geometry("300x100")
        
        # 居中显示
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 输入框
        edit_var = tk.StringVar(value=current_text)
        edit_entry = tk.Entry(dialog, textvariable=edit_var, font=("Arial", 12))
        edit_entry.pack(padx=20, pady=10, fill=tk.X)
        edit_entry.select_range(0, tk.END)
        edit_entry.focus()
        
        # 按钮框架
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)
        
        def save_edit():
            new_text = edit_var.get().strip()
            if new_text:
                self.todos[index]["text"] = new_text
                self.refresh_listbox()
                self.save_todos()
                dialog.destroy()
        
        tk.Button(button_frame, text="保存", command=save_edit).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # 绑定回车键
        edit_entry.bind('<Return>', lambda e: save_edit())
    
    def move_todo(self, direction):
        """移动待办事项"""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择要移动的事项！")
            return
        
        index = selection[0]
        new_index = index + direction
        
        if 0 <= new_index < len(self.todos):
            # 交换位置
            self.todos[index], self.todos[new_index] = self.todos[new_index], self.todos[index]
            self.refresh_listbox()
            self.save_todos()
            
            # 保持选中状态
            self.listbox.selection_set(new_index)
    
    def refresh_listbox(self):
        """刷新列表显示"""
        self.listbox.delete(0, tk.END)
        
        for i, todo in enumerate(self.todos):
            text = todo["text"]
            if todo["completed"]:
                text = f"✓ {text}"
            self.listbox.insert(tk.END, text)
            
            # 设置完成项的颜色
            if todo["completed"]:
                self.listbox.itemconfig(i, fg="gray")
        
        self.update_status()
    
    def update_status(self):
        """更新状态栏"""
        total = len(self.todos)
        completed = sum(1 for todo in self.todos if todo["completed"])
        pending = total - completed
        
        self.status_var.set(f"总计: {total} | 待完成: {pending} | 已完成: {completed}")
    
    def save_todos(self):
        """保存待办事项到文件"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.todos, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存失败: {e}")
    
    def load_todos(self):
        """从文件加载待办事项"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.todos = json.load(f)
                self.refresh_listbox()
            except Exception as e:
                print(f"加载失败: {e}")
    
    def on_closing(self):
        """关闭窗口时的处理"""
        self.save_todos()
        self.root.destroy()


def run_todo_app():
    """运行待办事项应用"""
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()


if __name__ == "__main__":
    print("练习2：待办事项列表应用")
    print("1. 查看练习要求")
    print("2. 运行参考答案")
    
    choice = input("\n请选择 (1-2): ")
    
    if choice == '1':
        print("\n请打开文件查看练习要求，然后完成create_todo_app()函数")
        print("这是一个综合性练习，建议先实现基本功能，再添加高级功能")
        # create_todo_app()  # 学生实现
    elif choice == '2':
        print("\n运行参考答案...")
        run_todo_app()
    else:
        print("无效选择") 