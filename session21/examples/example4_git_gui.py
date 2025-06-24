#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session21 示例4：Git GUI工具演示

本示例创建一个简单的Git图形界面工具，演示：
1. 使用tkinter创建GUI界面
2. 集成Git命令操作
3. 实时显示仓库状态
4. 可视化提交历史
5. 分支管理界面

作者: Python教程团队
创建日期: 2024-01-20
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import subprocess
import os
from pathlib import Path
import threading
from datetime import datetime


class GitGUI:
    """
    简单的Git图形界面工具
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Git GUI 工具 - Python教程演示")
        self.root.geometry("900x700")
        
        # 当前仓库路径
        self.repo_path = tk.StringVar(value=os.getcwd())
        
        # 创建界面
        self.create_widgets()
        
        # 初始化时刷新状态
        self.refresh_status()
    
    def create_widgets(self):
        """
        创建GUI组件
        """
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # 1. 仓库路径选择
        self.create_repo_section(main_frame)
        
        # 2. 操作按钮区域
        self.create_action_section(main_frame)
        
        # 3. 状态显示区域
        self.create_status_section(main_frame)
        
        # 4. 主要内容区域（使用Notebook）
        self.create_content_section(main_frame)
    
    def create_repo_section(self, parent):
        """
        创建仓库路径选择区域
        """
        repo_frame = ttk.LabelFrame(parent, text="仓库路径", padding="5")
        repo_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        repo_frame.columnconfigure(1, weight=1)
        
        ttk.Label(repo_frame, text="路径:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        path_entry = ttk.Entry(repo_frame, textvariable=self.repo_path, width=50)
        path_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(repo_frame, text="浏览", command=self.browse_repo).grid(row=0, column=2)
        ttk.Button(repo_frame, text="刷新", command=self.refresh_status).grid(row=0, column=3, padx=(5, 0))
    
    def create_action_section(self, parent):
        """
        创建操作按钮区域
        """
        action_frame = ttk.LabelFrame(parent, text="Git操作", padding="5")
        action_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 第一行按钮
        row1_frame = ttk.Frame(action_frame)
        row1_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(row1_frame, text="Git Status", command=self.git_status).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(row1_frame, text="Git Add .", command=self.git_add_all).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(row1_frame, text="Git Commit", command=self.git_commit_dialog).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(row1_frame, text="Git Log", command=self.git_log).pack(side=tk.LEFT, padx=(0, 5))
        
        # 第二行按钮
        row2_frame = ttk.Frame(action_frame)
        row2_frame.pack(fill=tk.X)
        
        ttk.Button(row2_frame, text="创建分支", command=self.create_branch_dialog).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(row2_frame, text="切换分支", command=self.checkout_branch_dialog).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(row2_frame, text="合并分支", command=self.merge_branch_dialog).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(row2_frame, text="初始化仓库", command=self.git_init).pack(side=tk.LEFT, padx=(0, 5))
    
    def create_status_section(self, parent):
        """
        创建状态显示区域
        """
        status_frame = ttk.LabelFrame(parent, text="仓库状态", padding="5")
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        status_frame.columnconfigure(0, weight=1)
        
        self.status_text = tk.Text(status_frame, height=4, wrap=tk.WORD)
        status_scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=status_scrollbar.set)
        
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        status_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    
    def create_content_section(self, parent):
        """
        创建主要内容区域
        """
        # 创建Notebook（标签页）
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 文件状态标签页
        self.create_files_tab()
        
        # 提交历史标签页
        self.create_history_tab()
        
        # 分支管理标签页
        self.create_branches_tab()
        
        # 命令输出标签页
        self.create_output_tab()
    
    def create_files_tab(self):
        """
        创建文件状态标签页
        """
        files_frame = ttk.Frame(self.notebook)
        self.notebook.add(files_frame, text="文件状态")
        
        # 创建Treeview显示文件状态
        columns = ('状态', '文件路径')
        self.files_tree = ttk.Treeview(files_frame, columns=columns, show='tree headings')
        
        # 设置列标题
        self.files_tree.heading('#0', text='类型')
        self.files_tree.heading('状态', text='状态')
        self.files_tree.heading('文件路径', text='文件路径')
        
        # 设置列宽
        self.files_tree.column('#0', width=80)
        self.files_tree.column('状态', width=100)
        self.files_tree.column('文件路径', width=400)
        
        # 添加滚动条
        files_scrollbar = ttk.Scrollbar(files_frame, orient=tk.VERTICAL, command=self.files_tree.yview)
        self.files_tree.configure(yscrollcommand=files_scrollbar.set)
        
        # 布局
        self.files_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        files_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_history_tab(self):
        """
        创建提交历史标签页
        """
        history_frame = ttk.Frame(self.notebook)
        self.notebook.add(history_frame, text="提交历史")
        
        # 创建Treeview显示提交历史
        columns = ('哈希', '作者', '日期', '消息')
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show='tree headings')
        
        # 设置列标题
        self.history_tree.heading('#0', text='#')
        self.history_tree.heading('哈希', text='提交哈希')
        self.history_tree.heading('作者', text='作者')
        self.history_tree.heading('日期', text='提交日期')
        self.history_tree.heading('消息', text='提交消息')
        
        # 设置列宽
        self.history_tree.column('#0', width=50)
        self.history_tree.column('哈希', width=100)
        self.history_tree.column('作者', width=120)
        self.history_tree.column('日期', width=150)
        self.history_tree.column('消息', width=300)
        
        # 添加滚动条
        history_scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)
        
        # 布局
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_branches_tab(self):
        """
        创建分支管理标签页
        """
        branches_frame = ttk.Frame(self.notebook)
        self.notebook.add(branches_frame, text="分支管理")
        
        # 分支列表
        self.branches_listbox = tk.Listbox(branches_frame)
        branches_scrollbar = ttk.Scrollbar(branches_frame, orient=tk.VERTICAL, command=self.branches_listbox.yview)
        self.branches_listbox.configure(yscrollcommand=branches_scrollbar.set)
        
        # 布局
        self.branches_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        branches_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_output_tab(self):
        """
        创建命令输出标签页
        """
        output_frame = ttk.Frame(self.notebook)
        self.notebook.add(output_frame, text="命令输出")
        
        # 创建文本区域显示命令输出
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)
    
    def run_git_command(self, command, show_output=True):
        """
        执行Git命令
        """
        try:
            # 切换到仓库目录
            cwd = self.repo_path.get()
            
            # 执行命令
            result = subprocess.run(
                command.split() if isinstance(command, str) else command,
                cwd=cwd,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if show_output:
                # 显示命令和输出
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.output_text.insert(tk.END, f"[{timestamp}] $ {command}\n")
                
                if result.stdout:
                    self.output_text.insert(tk.END, result.stdout + "\n")
                if result.stderr:
                    self.output_text.insert(tk.END, f"错误: {result.stderr}\n")
                
                self.output_text.insert(tk.END, "-" * 50 + "\n")
                self.output_text.see(tk.END)
            
            return result.stdout, result.stderr, result.returncode
            
        except Exception as e:
            error_msg = f"执行命令失败: {e}"
            if show_output:
                self.output_text.insert(tk.END, error_msg + "\n")
                self.output_text.see(tk.END)
            return "", error_msg, 1
    
    def browse_repo(self):
        """
        浏览选择仓库目录
        """
        directory = filedialog.askdirectory(initialdir=self.repo_path.get())
        if directory:
            self.repo_path.set(directory)
            self.refresh_status()
    
    def refresh_status(self):
        """
        刷新仓库状态
        """
        # 检查是否是Git仓库
        git_dir = Path(self.repo_path.get()) / ".git"
        if not git_dir.exists():
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, "当前目录不是Git仓库。请选择Git仓库目录或初始化新仓库。")
            return
        
        # 获取Git状态
        stdout, stderr, returncode = self.run_git_command("git status --porcelain", show_output=False)
        
        if returncode == 0:
            self.update_status_display()
            self.update_files_display()
            self.update_history_display()
            self.update_branches_display()
        else:
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, f"获取Git状态失败: {stderr}")
    
    def update_status_display(self):
        """
        更新状态显示
        """
        stdout, stderr, returncode = self.run_git_command("git status", show_output=False)
        
        self.status_text.delete(1.0, tk.END)
        if returncode == 0:
            self.status_text.insert(tk.END, stdout)
        else:
            self.status_text.insert(tk.END, f"错误: {stderr}")
    
    def update_files_display(self):
        """
        更新文件状态显示
        """
        # 清空现有内容
        for item in self.files_tree.get_children():
            self.files_tree.delete(item)
        
        # 获取文件状态
        stdout, stderr, returncode = self.run_git_command("git status --porcelain", show_output=False)
        
        if returncode == 0 and stdout:
            for line in stdout.strip().split('\n'):
                if line:
                    status = line[:2]
                    filepath = line[3:]
                    
                    # 解析状态
                    status_desc = self.parse_git_status(status)
                    
                    # 添加到树形视图
                    self.files_tree.insert('', tk.END, text='文件', values=(status_desc, filepath))
    
    def parse_git_status(self, status):
        """
        解析Git状态代码
        """
        status_map = {
            'A ': '新增',
            'M ': '已修改',
            'D ': '已删除',
            'R ': '重命名',
            'C ': '复制',
            'U ': '未合并',
            '??': '未跟踪',
            ' M': '工作区修改',
            ' D': '工作区删除',
            'AM': '新增并修改',
            'MM': '暂存并修改'
        }
        return status_map.get(status, status)
    
    def update_history_display(self):
        """
        更新提交历史显示
        """
        # 清空现有内容
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # 获取提交历史
        stdout, stderr, returncode = self.run_git_command(
            "git log --pretty=format:%h|%an|%ad|%s --date=short -10", 
            show_output=False
        )
        
        if returncode == 0 and stdout:
            for i, line in enumerate(stdout.strip().split('\n'), 1):
                if line:
                    parts = line.split('|')
                    if len(parts) >= 4:
                        hash_short, author, date, message = parts[0], parts[1], parts[2], '|'.join(parts[3:])
                        self.history_tree.insert('', tk.END, text=str(i), values=(hash_short, author, date, message))
    
    def update_branches_display(self):
        """
        更新分支显示
        """
        # 清空现有内容
        self.branches_listbox.delete(0, tk.END)
        
        # 获取分支列表
        stdout, stderr, returncode = self.run_git_command("git branch", show_output=False)
        
        if returncode == 0 and stdout:
            for line in stdout.strip().split('\n'):
                if line:
                    branch = line.strip()
                    self.branches_listbox.insert(tk.END, branch)
    
    def git_status(self):
        """
        执行git status命令
        """
        self.run_git_command("git status")
        self.refresh_status()
    
    def git_add_all(self):
        """
        执行git add .命令
        """
        self.run_git_command("git add .")
        self.refresh_status()
    
    def git_commit_dialog(self):
        """
        显示提交对话框
        """
        dialog = CommitDialog(self.root, self.commit_callback)
    
    def commit_callback(self, message):
        """
        提交回调函数
        """
        if message:
            self.run_git_command(f'git commit -m "{message}"')
            self.refresh_status()
    
    def git_log(self):
        """
        显示Git日志
        """
        self.run_git_command("git log --oneline -10")
        self.update_history_display()
    
    def git_init(self):
        """
        初始化Git仓库
        """
        result = messagebox.askyesno("确认", "是否在当前目录初始化Git仓库？")
        if result:
            self.run_git_command("git init")
            self.refresh_status()
    
    def create_branch_dialog(self):
        """
        创建分支对话框
        """
        dialog = BranchDialog(self.root, "创建分支", self.create_branch_callback)
    
    def create_branch_callback(self, branch_name):
        """
        创建分支回调
        """
        if branch_name:
            self.run_git_command(f"git checkout -b {branch_name}")
            self.refresh_status()
    
    def checkout_branch_dialog(self):
        """
        切换分支对话框
        """
        dialog = BranchDialog(self.root, "切换分支", self.checkout_branch_callback)
    
    def checkout_branch_callback(self, branch_name):
        """
        切换分支回调
        """
        if branch_name:
            self.run_git_command(f"git checkout {branch_name}")
            self.refresh_status()
    
    def merge_branch_dialog(self):
        """
        合并分支对话框
        """
        dialog = BranchDialog(self.root, "合并分支", self.merge_branch_callback)
    
    def merge_branch_callback(self, branch_name):
        """
        合并分支回调
        """
        if branch_name:
            self.run_git_command(f"git merge {branch_name}")
            self.refresh_status()


class CommitDialog:
    """
    提交对话框
    """
    
    def __init__(self, parent, callback):
        self.callback = callback
        
        # 创建对话框窗口
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Git Commit")
        self.dialog.geometry("400x200")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 居中显示
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self.create_widgets()
    
    def create_widgets(self):
        """
        创建对话框组件
        """
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 提交消息标签
        ttk.Label(main_frame, text="提交消息:").pack(anchor=tk.W)
        
        # 提交消息输入框
        self.message_text = tk.Text(main_frame, height=6, wrap=tk.WORD)
        self.message_text.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        self.message_text.focus()
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="提交", command=self.commit).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="取消", command=self.cancel).pack(side=tk.RIGHT)
    
    def commit(self):
        """
        执行提交
        """
        message = self.message_text.get(1.0, tk.END).strip()
        if message:
            self.callback(message)
            self.dialog.destroy()
        else:
            messagebox.showwarning("警告", "请输入提交消息")
    
    def cancel(self):
        """
        取消提交
        """
        self.dialog.destroy()


class BranchDialog:
    """
    分支操作对话框
    """
    
    def __init__(self, parent, title, callback):
        self.callback = callback
        
        # 创建对话框窗口
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("300x120")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 居中显示
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 100, parent.winfo_rooty() + 100))
        
        self.create_widgets()
    
    def create_widgets(self):
        """
        创建对话框组件
        """
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 分支名称标签
        ttk.Label(main_frame, text="分支名称:").pack(anchor=tk.W)
        
        # 分支名称输入框
        self.branch_var = tk.StringVar()
        branch_entry = ttk.Entry(main_frame, textvariable=self.branch_var, width=30)
        branch_entry.pack(fill=tk.X, pady=(5, 10))
        branch_entry.focus()
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="确定", command=self.ok).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="取消", command=self.cancel).pack(side=tk.RIGHT)
        
        # 绑定回车键
        branch_entry.bind('<Return>', lambda e: self.ok())
    
    def ok(self):
        """
        确定操作
        """
        branch_name = self.branch_var.get().strip()
        if branch_name:
            self.callback(branch_name)
            self.dialog.destroy()
        else:
            messagebox.showwarning("警告", "请输入分支名称")
    
    def cancel(self):
        """
        取消操作
        """
        self.dialog.destroy()


def main():
    """
    主函数
    """
    print("启动Git GUI工具...")
    
    # 创建主窗口
    root = tk.Tk()
    
    # 设置窗口图标（如果有的话）
    try:
        # 这里可以设置窗口图标
        # root.iconbitmap('git_icon.ico')
        pass
    except:
        pass
    
    # 创建应用实例
    app = GitGUI(root)
    
    # 设置窗口关闭事件
    def on_closing():
        if messagebox.askokcancel("退出", "确定要退出Git GUI工具吗？"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    print("Git GUI工具已启动")
    print("功能说明:")
    print("1. 选择或浏览Git仓库目录")
    print("2. 查看文件状态和提交历史")
    print("3. 执行基本Git操作")
    print("4. 管理分支")
    print("5. 查看命令输出")
    
    # 启动GUI主循环
    root.mainloop()


if __name__ == "__main__":
    main()