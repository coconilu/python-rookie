"""
练习3参考答案：综合练习 - 任务管理系统
"""

from flask import Flask, render_template_string, request, redirect, url_for, flash, jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# 任务数据存储
tasks = []
task_id_counter = 1


# 1. 主页路由 - 显示所有任务
@app.route('/')
def index():
    """显示任务列表和统计信息"""
    # 计算统计信息
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t['completed']])
    pending_tasks = total_tasks - completed_tasks
    
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
            .actions a { margin-right: 10px; text-decoration: none; }
            .actions a:hover { text-decoration: underline; }
            .stats { background: #f0f0f0; padding: 15px; margin: 20px 0; border-radius: 5px; }
            .stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
            .stat-item { text-align: center; }
            .stat-value { font-size: 24px; font-weight: bold; }
            .flash { padding: 10px; margin: 10px 0; border-radius: 3px; }
            .flash.success { background: #d4edda; color: #155724; }
            .flash.error { background: #f8d7da; color: #721c24; }
            .priority-high { color: #dc3545; font-weight: bold; }
            .priority-medium { color: #ffc107; }
            .priority-low { color: #28a745; }
            .add-button { 
                background: #007bff; 
                color: white; 
                padding: 10px 20px; 
                text-decoration: none; 
                border-radius: 5px; 
                display: inline-block;
                margin: 10px 0;
            }
            .add-button:hover { background: #0056b3; }
            .search-box { margin: 20px 0; }
            .search-box input { padding: 8px; width: 300px; }
            .search-box button { padding: 8px 15px; }
        </style>
    </head>
    <body>
        <h1>🗂️ 任务管理系统</h1>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash {{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <div class="stats">
            <h2>任务统计</h2>
            <div class="stats-grid">
                <div class="stat-item">
                    <div>总任务数</div>
                    <div class="stat-value">{{ total_tasks }}</div>
                </div>
                <div class="stat-item">
                    <div>已完成</div>
                    <div class="stat-value" style="color: #28a745;">{{ completed_tasks }}</div>
                </div>
                <div class="stat-item">
                    <div>未完成</div>
                    <div class="stat-value" style="color: #dc3545;">{{ pending_tasks }}</div>
                </div>
            </div>
        </div>
        
        <div class="search-box">
            <form action="/search" method="get">
                <input type="text" name="q" placeholder="搜索任务..." value="{{ request.args.get('q', '') }}">
                <button type="submit">搜索</button>
                {% if request.args.get('q') %}
                    <a href="/">清除搜索</a>
                {% endif %}
            </form>
        </div>
        
        <a href="/add" class="add-button">➕ 添加新任务</a>
        
        {% if tasks %}
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>标题</th>
                    <th>描述</th>
                    <th>优先级</th>
                    <th>创建时间</th>
                    <th>状态</th>
                    <th>操作</th>
                </tr>
            </thead>
            <tbody>
            {% for task in tasks %}
                <tr>
                    <td>{{ task.id }}</td>
                    <td class="{{ 'completed' if task.completed else '' }}">
                        <a href="/task/{{ task.id }}">{{ task.title }}</a>
                    </td>
                    <td>{{ task.description[:30] }}{{ '...' if task.description|length > 30 else '' }}</td>
                    <td class="priority-{{ task.priority }}">{{ task.priority|capitalize }}</td>
                    <td>{{ task.created_at|format_datetime }}</td>
                    <td>
                        {% if task.completed %}
                            ✅ 已完成
                        {% else %}
                            ⏳ 进行中
                        {% endif %}
                    </td>
                    <td class="actions">
                        <a href="/edit/{{ task.id }}">编辑</a>
                        <a href="/toggle/{{ task.id }}">
                            {{ '标记未完成' if task.completed else '标记完成' }}
                        </a>
                        <a href="/delete/{{ task.id }}" onclick="return confirm('确定要删除这个任务吗？');">删除</a>
                    </td>
                </tr>
            {% endfor %}
            </tbody>
        </table>
        {% else %}
        <p style="text-align: center; color: #666; margin: 40px 0;">暂无任务，点击上方按钮添加第一个任务！</p>
        {% endif %}
    </body>
    </html>
    '''
    
    return render_template_string(template, 
                                tasks=tasks, 
                                total_tasks=total_tasks,
                                completed_tasks=completed_tasks,
                                pending_tasks=pending_tasks,
                                request=request)


# 2. 添加任务页面
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    """添加新任务"""
    if request.method == 'POST':
        global task_id_counter
        
        # 获取表单数据
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        priority = request.form.get('priority', 'medium')
        
        # 验证数据
        if not title:
            flash('任务标题不能为空！', 'error')
            return redirect(url_for('add_task'))
        
        # 创建新任务
        new_task = {
            'id': task_id_counter,
            'title': title,
            'description': description,
            'priority': priority,
            'created_at': datetime.now(),
            'completed': False
        }
        
        tasks.append(new_task)
        task_id_counter += 1
        
        flash(f'任务 "{title}" 已成功添加！', 'success')
        return redirect(url_for('index'))
    
    # 显示添加表单
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>添加任务</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            form { background: #f0f0f0; padding: 20px; border-radius: 5px; max-width: 500px; }
            label { display: block; margin-top: 10px; font-weight: bold; }
            input, textarea, select { width: 100%; padding: 8px; margin-top: 5px; box-sizing: border-box; }
            textarea { resize: vertical; min-height: 100px; }
            button { 
                margin-top: 15px; 
                padding: 10px 20px; 
                background: #007bff; 
                color: white; 
                border: none; 
                border-radius: 3px; 
                cursor: pointer; 
            }
            button:hover { background: #0056b3; }
            .flash { padding: 10px; margin: 10px 0; border-radius: 3px; }
            .flash.error { background: #f8d7da; color: #721c24; }
            .required { color: red; }
        </style>
    </head>
    <body>
        <h1>添加新任务</h1>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash {{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <form method="POST">
            <label for="title">任务标题 <span class="required">*</span></label>
            <input type="text" id="title" name="title" required autofocus>
            
            <label for="description">任务描述</label>
            <textarea id="description" name="description" placeholder="详细描述任务内容..."></textarea>
            
            <label for="priority">优先级</label>
            <select id="priority" name="priority">
                <option value="low">低</option>
                <option value="medium" selected>中</option>
                <option value="high">高</option>
            </select>
            
            <button type="submit">创建任务</button>
            <a href="/" style="margin-left: 10px;">取消</a>
        </form>
    </body>
    </html>
    '''
    
    return render_template_string(template)


# 3. 编辑任务
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    """编辑任务"""
    # 查找任务
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if not task:
        flash('任务不存在！', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # 获取表单数据
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        priority = request.form.get('priority', 'medium')
        
        # 验证数据
        if not title:
            flash('任务标题不能为空！', 'error')
            return redirect(url_for('edit_task', task_id=task_id))
        
        # 更新任务
        task['title'] = title
        task['description'] = description
        task['priority'] = priority
        
        flash(f'任务 "{title}" 已更新！', 'success')
        return redirect(url_for('index'))
    
    # 显示编辑表单
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>编辑任务</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            form { background: #f0f0f0; padding: 20px; border-radius: 5px; max-width: 500px; }
            label { display: block; margin-top: 10px; font-weight: bold; }
            input, textarea, select { width: 100%; padding: 8px; margin-top: 5px; box-sizing: border-box; }
            textarea { resize: vertical; min-height: 100px; }
            button { 
                margin-top: 15px; 
                padding: 10px 20px; 
                background: #28a745; 
                color: white; 
                border: none; 
                border-radius: 3px; 
                cursor: pointer; 
            }
            button:hover { background: #218838; }
            .required { color: red; }
        </style>
    </head>
    <body>
        <h1>编辑任务</h1>
        
        <form method="POST">
            <label for="title">任务标题 <span class="required">*</span></label>
            <input type="text" id="title" name="title" value="{{ task.title }}" required>
            
            <label for="description">任务描述</label>
            <textarea id="description" name="description">{{ task.description }}</textarea>
            
            <label for="priority">优先级</label>
            <select id="priority" name="priority">
                <option value="low" {{ 'selected' if task.priority == 'low' else '' }}>低</option>
                <option value="medium" {{ 'selected' if task.priority == 'medium' else '' }}>中</option>
                <option value="high" {{ 'selected' if task.priority == 'high' else '' }}>高</option>
            </select>
            
            <button type="submit">保存更改</button>
            <a href="/" style="margin-left: 10px;">取消</a>
        </form>
    </body>
    </html>
    '''
    
    return render_template_string(template, task=task)


# 4. 删除任务
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """删除任务"""
    global tasks
    
    # 查找任务
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if task:
        tasks = [t for t in tasks if t['id'] != task_id]
        flash(f'任务 "{task["title"]}" 已删除！', 'success')
    else:
        flash('任务不存在！', 'error')
    
    return redirect(url_for('index'))


# 5. 切换任务状态
@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    """切换任务完成状态"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if task:
        task['completed'] = not task['completed']
        status = '已完成' if task['completed'] else '未完成'
        flash(f'任务 "{task["title"]}" 标记为{status}！', 'success')
    else:
        flash('任务不存在！', 'error')
    
    return redirect(url_for('index'))


# 6. 任务详情页面
@app.route('/task/<int:task_id>')
def task_detail(task_id):
    """显示任务详情"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if not task:
        flash('任务不存在！', 'error')
        return redirect(url_for('index'))
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>任务详情</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .task-detail { background: #f0f0f0; padding: 20px; border-radius: 5px; }
            .task-header { display: flex; justify-content: space-between; align-items: center; }
            .priority-high { color: #dc3545; }
            .priority-medium { color: #ffc107; }
            .priority-low { color: #28a745; }
            .completed { text-decoration: line-through; color: #888; }
            .actions { margin-top: 20px; }
            .actions a { 
                margin-right: 10px; 
                padding: 8px 15px; 
                background: #007bff; 
                color: white; 
                text-decoration: none; 
                border-radius: 3px; 
            }
            .actions a:hover { opacity: 0.8; }
            .delete-btn { background: #dc3545 !important; }
            .complete-btn { background: #28a745 !important; }
            .info-item { margin: 10px 0; }
            .info-label { font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>任务详情</h1>
        
        <div class="task-detail">
            <div class="task-header">
                <h2 class="{{ 'completed' if task.completed else '' }}">{{ task.title }}</h2>
                <span class="priority-{{ task.priority }}">{{ task.priority|priority_badge|safe }}</span>
            </div>
            
            <div class="info-item">
                <span class="info-label">ID：</span>{{ task.id }}
            </div>
            
            <div class="info-item">
                <span class="info-label">描述：</span>
                <p>{{ task.description or '无描述' }}</p>
            </div>
            
            <div class="info-item">
                <span class="info-label">创建时间：</span>{{ task.created_at|format_datetime }}
            </div>
            
            <div class="info-item">
                <span class="info-label">状态：</span>
                {% if task.completed %}
                    ✅ 已完成
                {% else %}
                    ⏳ 进行中
                {% endif %}
            </div>
            
            <div class="actions">
                <a href="/edit/{{ task.id }}">✏️ 编辑</a>
                <a href="/toggle/{{ task.id }}" class="complete-btn">
                    {% if task.completed %}
                        ↩️ 标记未完成
                    {% else %}
                        ✅ 标记完成
                    {% endif %}
                </a>
                <a href="/delete/{{ task.id }}" class="delete-btn" 
                   onclick="return confirm('确定要删除这个任务吗？');">🗑️ 删除</a>
                <a href="/" style="background: #6c757d;">🔙 返回列表</a>
            </div>
        </div>
    </body>
    </html>
    '''
    
    return render_template_string(template, task=task)


# 7. 搜索功能
@app.route('/search')
def search_tasks():
    """搜索任务"""
    query = request.args.get('q', '').strip().lower()
    
    if not query:
        return redirect(url_for('index'))
    
    # 在标题和描述中搜索
    results = [
        task for task in tasks
        if query in task['title'].lower() or query in task['description'].lower()
    ]
    
    template = '''
    <h1>搜索结果</h1>
    <p>搜索关键词："{{ query }}"，找到 {{ results|length }} 个结果</p>
    
    <p><a href="/">返回所有任务</a></p>
    
    {% if results %}
        <!-- 这里可以重用主页的表格 -->
        <table border="1">
            <tr>
                <th>标题</th>
                <th>描述</th>
                <th>优先级</th>
                <th>状态</th>
            </tr>
            {% for task in results %}
            <tr>
                <td><a href="/task/{{ task.id }}">{{ task.title }}</a></td>
                <td>{{ task.description[:50] }}...</td>
                <td>{{ task.priority }}</td>
                <td>{{ '已完成' if task.completed else '进行中' }}</td>
            </tr>
            {% endfor %}
        </table>
    {% else %}
        <p>没有找到匹配的任务。</p>
    {% endif %}
    '''
    
    # 为了代码复用，实际上应该渲染主页模板，只是传入过滤后的任务
    # 这里简化处理
    flash(f'搜索 "{query}" 找到 {len(results)} 个结果', 'success')
    
    # 重定向到主页并显示搜索结果
    global tasks
    original_tasks = tasks
    tasks = results
    response = index()
    tasks = original_tasks
    
    return response


# 8. 自定义过滤器
@app.template_filter('format_datetime')
def format_datetime_filter(dt):
    """格式化日期时间"""
    if isinstance(dt, datetime):
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    return str(dt)


@app.template_filter('priority_badge')
def priority_badge_filter(priority):
    """优先级徽章"""
    badges = {
        'high': '<span style="background: #dc3545; color: white; padding: 2px 8px; border-radius: 3px;">高</span>',
        'medium': '<span style="background: #ffc107; color: black; padding: 2px 8px; border-radius: 3px;">中</span>',
        'low': '<span style="background: #28a745; color: white; padding: 2px 8px; border-radius: 3px;">低</span>'
    }
    return badges.get(priority, priority)


# 9. 错误处理
@app.errorhandler(404)
def page_not_found(e):
    """404错误页面"""
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>页面未找到</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                text-align: center; 
                margin-top: 100px; 
            }
            h1 { color: #dc3545; }
            a { 
                color: #007bff; 
                text-decoration: none; 
                font-size: 18px; 
            }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>404 - 页面未找到</h1>
        <p>抱歉，您访问的页面不存在。</p>
        <p><a href="/">返回首页</a></p>
    </body>
    </html>
    '''
    return render_template_string(template), 404


# 10. API端点
@app.route('/api/tasks')
def api_tasks():
    """返回JSON格式的任务列表"""
    # 将datetime对象转换为字符串
    tasks_json = []
    for task in tasks:
        task_dict = task.copy()
        task_dict['created_at'] = task_dict['created_at'].isoformat()
        tasks_json.append(task_dict)
    
    return jsonify({
        'status': 'success',
        'data': tasks_json,
        'count': len(tasks),
        'stats': {
            'total': len(tasks),
            'completed': len([t for t in tasks if t['completed']]),
            'pending': len([t for t in tasks if not t['completed']])
        }
    })


# 测试数据初始化
def init_test_data():
    """初始化测试数据"""
    global task_id_counter
    test_tasks = [
        {'title': '学习Flask', 'description': '完成Flask基础教程，掌握路由、模板和表单处理', 'priority': 'high'},
        {'title': '写作业', 'description': '完成Python练习题第17章', 'priority': 'medium'},
        {'title': '代码复习', 'description': '复习本周学习的代码，整理笔记', 'priority': 'medium'},
        {'title': '休息', 'description': '记得适当休息，保持身心健康', 'priority': 'low'},
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
    
    # 标记第一个任务为已完成
    if tasks:
        tasks[0]['completed'] = True


if __name__ == '__main__':
    print("任务管理系统 - 综合练习参考答案")
    print("功能包括：")
    print("- 查看任务列表和统计")
    print("- 添加、编辑、删除任务")
    print("- 切换任务完成状态")
    print("- 搜索任务")
    print("- API接口")
    print("\n正在初始化测试数据...")
    
    # 初始化测试数据
    init_test_data()
    
    print(f"已创建 {len(tasks)} 个测试任务")
    print("\n访问 http://127.0.0.1:5000 开始使用")
    
    app.run(debug=True) 