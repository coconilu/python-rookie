# Session 16 练习题

## 练习说明

本节包含两个练习题，帮助你掌握Tkinter GUI编程的核心概念。

## 练习1：创建登录窗口

**难度**：⭐⭐

**目标**：创建一个功能完整的登录窗口

**要求**：
- 用户名和密码输入框
- 记住密码选项
- 登录和取消按钮
- 输入验证
- 窗口居中显示

**知识点**：
- 基本控件使用（Label、Entry、Button、Checkbutton）
- Grid布局管理
- 事件处理
- 对话框使用

## 练习2：待办事项列表应用

**难度**：⭐⭐⭐

**目标**：创建一个完整的待办事项管理应用

**要求**：
- 添加、删除、编辑待办事项
- 标记完成状态
- 数据持久化（保存到文件）
- 状态栏显示统计信息

**知识点**：
- 复杂界面布局
- 列表控件使用
- 事件绑定（双击、回车等）
- 文件操作
- 数据管理

## 练习指导

### 步骤建议

1. **分析需求**
   - 理解练习要求
   - 列出需要的功能
   - 设计界面布局

2. **搭建框架**
   - 创建主窗口
   - 设置基本属性
   - 规划布局结构

3. **实现功能**
   - 逐个添加控件
   - 实现事件处理
   - 添加业务逻辑

4. **优化完善**
   - 美化界面
   - 添加错误处理
   - 测试各种情况

### 学习建议

- 先尝试自己实现，遇到问题再查看提示
- 完成基础功能后，尝试添加额外功能
- 参考解答文件学习最佳实践

## 解答文件

- `solutions/exercise1_solution.py` - 练习1的完整解答
- `solutions/exercise2_solution.py` - 练习2的完整解答

## 扩展挑战

完成基础练习后，可以尝试以下扩展：

### 练习1扩展
- 添加注册功能
- 实现密码强度检查
- 添加验证码功能
- 美化界面设计

### 练习2扩展
- 添加分类功能
- 实现拖拽排序
- 添加提醒功能
- 导出为不同格式

## 常见问题

### Q: 如何让窗口居中？
```python
window.update_idletasks()
width = window.winfo_width()
height = window.winfo_height()
x = (window.winfo_screenwidth() // 2) - (width // 2)
y = (window.winfo_screenheight() // 2) - (height // 2)
window.geometry(f'{width}x{height}+{x}+{y}')
```

### Q: 如何绑定回车键？
```python
widget.bind('<Return>', callback_function)
```

### Q: 如何创建确认对话框？
```python
result = messagebox.askyesno("标题", "消息内容")
if result:
    # 用户点击了"是"
```

## 学习资源

- [Tkinter官方文档](https://docs.python.org/3/library/tkinter.html)
- [Tkinter教程](https://www.pythontutorial.net/tkinter/)
- [Tkinter事件列表](https://www.python-course.eu/tkinter_events_binds.php)

加油！通过这些练习，你将掌握Tkinter GUI编程的精髓！💪 