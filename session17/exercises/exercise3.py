"""
练习3：综合练习
创建一个简单的任务管理系统
"""

from flask import Flask, render_template_string, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# 任务数据存储（实际项目应使用数据库）
tasks = []
task_id_counter = 1


# TODO: 完成以下功能

# 1. 主页路由 - 显示所有任务
@app.route('/')
def index():
    """
    TODO: 创建主页
    要求：
    1. 显示欢迎信息
    2. 显示任务统计（总数、已完成、未完成）
    3. 显示所有任务列表（表格形式）
    4. 每个任务显示：ID、标题、描述、创建时间、状态、操作按钮
    5. 提供"添加新任务"的链接
    """
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>任务管理系统</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .completed { text-decoration: line-through; color: #888; }
            .actions a { margin-right: 10px; }
            .stats { background: #f0f0f0; padding: 15px; margin: 20px 0; border-radius: 5px; }
            .flash { padding: 10px; margin: 10px 0; border-radius: 3px; }
            .flash.success { background: #d4edda; color: #155724; }
            .flash.error { background: #f8d7da; color: #721c24; }
        </style>
    </head>
    <body>
        <h1>任务管理系统</h1>
        
        <!-- TODO: 显示Flash消息 -->
        
        <!-- TODO: 显示任务统计 -->
        
        <!-- TODO: 显示任务列表 -->
        
        <p><a href="/add">添加新任务</a></p>
    </body>
    </html>
    '''
    
    return render_template_string(template, tasks=tasks)


# 2. 添加任务页面
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    """
    TODO: 创建添加任务页面
    GET请求：显示表单
    POST请求：处理表单提交
    
    表单字段：
    - title: 任务标题（必填）
    - description: 任务描述（可选）
    - priority: 优先级（高/中/低）
    
    处理逻辑：
    1. 验证表单数据
    2. 创建新任务（包含ID、创建时间、完成状态等）
    3. 添加到任务列表
    4. 显示成功消息并重定向到主页
    """
    if request.method == 'POST':
        # TODO: 处理表单提交
        pass
    
    # TODO: 显示添加任务表单
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>添加任务</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            form { background: #f0f0f0; padding: 20px; border-radius: 5px; max-width: 500px; }
            label { display: block; margin-top: 10px; }
            input, textarea, select { width: 100%; padding: 8px; margin-top: 5px; }
            button { margin-top: 15px; padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 3px; cursor: pointer; }
            button:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <h1>添加新任务</h1>
        
        <!-- TODO: 创建表单 -->
        
        <p><a href="/">返回任务列表</a></p>
    </body>
    </html>
    '''
    
    return render_template_string(template)


# 3. 编辑任务
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    """
    TODO: 创建编辑任务功能
    1. 根据task_id查找任务
    2. 如果任务不存在，显示错误并重定向
    3. GET请求：显示预填充的表单
    4. POST请求：更新任务信息
    """
    # TODO: 实现编辑功能
    pass


# 4. 删除任务
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """
    TODO: 实现删除任务功能
    1. 根据task_id查找任务
    2. 如果找到，从列表中删除
    3. 显示成功/失败消息
    4. 重定向到主页
    """
    # TODO: 实现删除功能
    pass


# 5. 切换任务状态
@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    """
    TODO: 实现切换任务完成状态
    1. 根据task_id查找任务
    2. 切换completed状态
    3. 重定向到主页
    """
    # TODO: 实现状态切换功能
    pass


# 6. 任务详情页面
@app.route('/task/<int:task_id>')
def task_detail(task_id):
    """
    TODO: 创建任务详情页面
    显示任务的所有信息：
    - 标题
    - 描述
    - 优先级
    - 创建时间
    - 完成状态
    - 操作按钮（编辑、删除、切换状态）
    """
    # TODO: 实现任务详情页面
    pass


# 7. 搜索功能
@app.route('/search')
def search_tasks():
    """
    TODO: 实现任务搜索功能
    1. 获取查询参数 q
    2. 在任务标题和描述中搜索
    3. 显示搜索结果
    """
    # TODO: 实现搜索功能
    pass


# 8. 自定义过滤器
@app.template_filter('format_datetime')
def format_datetime_filter(dt):
    """
    TODO: 创建日期时间格式化过滤器
    将datetime对象格式化为友好的显示格式
    例如：2024-01-15 14:30:00
    """
    # TODO: 实现过滤器
    pass


@app.template_filter('priority_badge')
def priority_badge_filter(priority):
    """
    TODO: 创建优先级徽章过滤器
    根据优先级返回不同颜色的HTML徽章
    高：红色，中：黄色，低：绿色
    """
    # TODO: 实现过滤器
    pass


# 9. 错误处理
@app.errorhandler(404)
def page_not_found(e):
    """
    TODO: 创建404错误页面
    """
    return "页面未找到", 404


# 10. API端点（可选）
@app.route('/api/tasks')
def api_tasks():
    """
    TODO: 创建返回JSON格式任务列表的API端点
    返回所有任务的JSON数据
    """
    # TODO: 实现API端点
    pass


# 测试数据初始化
def init_test_data():
    """初始化一些测试数据"""
    global task_id_counter
    test_tasks = [
        {'title': '学习Flask', 'description': '完成Flask基础教程', 'priority': '高'},
        {'title': '写作业', 'description': '完成Python练习题', 'priority': '中'},
        {'title': '休息', 'description': '记得适当休息', 'priority': '低'},
    ]
    
    for task_data in test_tasks:
        task = {
            'id': task_id_counter,
            'title': task_data['title'],
            'description': task_data['description'],
            'priority': task_data['priority'],
            'created_at': datetime.now(),
            'completed': False
        }
        tasks.append(task)
        task_id_counter += 1


if __name__ == '__main__':
    print("综合练习：任务管理系统")
    print("请完成所有TODO部分，实现一个完整的任务管理系统")
    print("提示：")
    print("1. 先实现基本的CRUD功能")
    print("2. 再添加搜索、过滤等高级功能")
    print("3. 最后优化界面和用户体验")
    
    # 初始化测试数据
    init_test_data()
    
    app.run(debug=True) 