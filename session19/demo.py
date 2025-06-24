#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session19: 前端集成 - 演示代码

本文件演示了Flask与前端技术的集成，包括HTML、CSS、JavaScript的使用，
以及AJAX异步请求的实现。

作者: Python教程团队
创建日期: 2024-12-24
最后修改: 2024-12-24
"""

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, BooleanField
from wtforms.validators import DataRequired, Length
from datetime import datetime, date
import os
import json

# 应用配置
app = Flask(__name__)
app.config['SECRET_KEY'] = 'demo-secret-key-for-session19'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///demo_todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db = SQLAlchemy(app)


class Todo(db.Model):
    """
    待办事项数据模型
    """
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(10), default='medium')
    completed = db.Column(db.Boolean, default=False)
    deadline = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """
        将模型转换为字典格式，用于JSON序列化
        """
        return {
            'id': self.id,
            'content': self.content,
            'priority': self.priority,
            'completed': self.completed,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Todo {self.id}: {self.content}>'


class TodoForm(FlaskForm):
    """
    待办事项表单
    """
    content = StringField('任务内容', validators=[
        DataRequired(message='请输入任务内容'),
        Length(min=1, max=200, message='任务内容长度应在1-200字符之间')
    ])
    priority = SelectField('优先级', choices=[
        ('low', '低优先级'),
        ('medium', '中优先级'),
        ('high', '高优先级')
    ], default='medium')
    deadline = DateField('截止日期', validators=[], format='%Y-%m-%d')


# 模板过滤器
@app.template_filter('datetime_format')
def datetime_format(value, format='%Y-%m-%d %H:%M'):
    """
    格式化日期时间
    """
    if value is None:
        return ''
    return value.strftime(format)


@app.template_filter('time_ago')
def time_ago(value):
    """
    显示相对时间
    """
    if value is None:
        return ''
    
    now = datetime.now()
    diff = now - value
    
    if diff.days > 0:
        return f'{diff.days}天前'
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f'{hours}小时前'
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f'{minutes}分钟前'
    else:
        return '刚刚'


@app.template_global()
def get_todo_stats(todos):
    """
    获取待办事项统计信息
    """
    total = len(todos)
    completed = len([t for t in todos if t.completed])
    active = total - completed
    
    return {
        'total': total,
        'completed': completed,
        'active': active,
        'completion_rate': round(completed / total * 100, 1) if total > 0 else 0
    }


# 路由定义
@app.route('/')
def index():
    """
    首页路由，重定向到待办事项页面
    """
    return redirect(url_for('todos'))


@app.route('/todos')
def todos():
    """
    待办事项主页面
    """
    filter_type = request.args.get('filter', 'all')
    
    # 根据过滤条件查询数据
    query = Todo.query
    
    if filter_type == 'active':
        query = query.filter_by(completed=False)
    elif filter_type == 'completed':
        query = query.filter_by(completed=True)
    
    todos = query.order_by(Todo.created_at.desc()).all()
    
    # 获取统计信息
    all_todos = Todo.query.all()
    stats = {
        'total': len(all_todos),
        'active': len([t for t in all_todos if not t.completed]),
        'completed': len([t for t in all_todos if t.completed])
    }
    
    form = TodoForm()
    
    return render_template('todos.html', 
                         todos=todos, 
                         form=form, 
                         filter_type=filter_type,
                         stats=stats)


@app.route('/add_todo', methods=['POST'])
def add_todo():
    """
    添加新的待办事项（表单提交）
    """
    form = TodoForm()
    
    if form.validate_on_submit():
        try:
            todo = Todo(
                content=form.content.data,
                priority=form.priority.data,
                deadline=form.deadline.data
            )
            
            db.session.add(todo)
            db.session.commit()
            
            flash('任务添加成功！', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'添加失败: {str(e)}', 'error')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'error')
    
    return redirect(url_for('todos'))


# API路由
@app.route('/api/todos', methods=['GET'])
def api_get_todos():
    """
    获取所有待办事项的API接口
    """
    try:
        filter_type = request.args.get('filter', 'all')
        
        query = Todo.query
        
        if filter_type == 'active':
            query = query.filter_by(completed=False)
        elif filter_type == 'completed':
            query = query.filter_by(completed=True)
        
        todos = query.order_by(Todo.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'todos': [todo.to_dict() for todo in todos],
            'count': len(todos)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取数据失败: {str(e)}'
        }), 500


@app.route('/api/todos', methods=['POST'])
def api_add_todo():
    """
    添加新待办事项的API接口
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('content'):
            return jsonify({
                'success': False,
                'message': '任务内容不能为空'
            }), 400
        
        # 验证数据
        content = data['content'].strip()
        if len(content) == 0 or len(content) > 200:
            return jsonify({
                'success': False,
                'message': '任务内容长度应在1-200字符之间'
            }), 400
        
        # 创建新任务
        todo = Todo(
            content=content,
            priority=data.get('priority', 'medium')
        )
        
        # 处理截止日期
        if data.get('deadline'):
            try:
                todo.deadline = datetime.strptime(data['deadline'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': '日期格式错误，请使用YYYY-MM-DD格式'
                }), 400
        
        db.session.add(todo)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'todo': todo.to_dict(),
            'message': '任务添加成功'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'添加失败: {str(e)}'
        }), 500


@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def api_update_todo(todo_id):
    """
    更新待办事项的API接口
    """
    try:
        todo = Todo.query.get_or_404(todo_id)
        data = request.get_json()
        
        # 更新字段
        if 'content' in data:
            content = data['content'].strip()
            if len(content) == 0 or len(content) > 200:
                return jsonify({
                    'success': False,
                    'message': '任务内容长度应在1-200字符之间'
                }), 400
            todo.content = content
        
        if 'priority' in data:
            if data['priority'] in ['low', 'medium', 'high']:
                todo.priority = data['priority']
        
        if 'completed' in data:
            todo.completed = bool(data['completed'])
        
        if 'deadline' in data:
            if data['deadline']:
                try:
                    todo.deadline = datetime.strptime(data['deadline'], '%Y-%m-%d').date()
                except ValueError:
                    return jsonify({
                        'success': False,
                        'message': '日期格式错误，请使用YYYY-MM-DD格式'
                    }), 400
            else:
                todo.deadline = None
        
        todo.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'todo': todo.to_dict(),
            'message': '任务更新成功'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'更新失败: {str(e)}'
        }), 500


@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def api_delete_todo(todo_id):
    """
    删除待办事项的API接口
    """
    try:
        todo = Todo.query.get_or_404(todo_id)
        db.session.delete(todo)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '任务删除成功'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'删除失败: {str(e)}'
        }), 500


@app.route('/api/todos/<int:todo_id>/toggle', methods=['POST'])
def api_toggle_todo(todo_id):
    """
    切换待办事项完成状态的API接口
    """
    try:
        todo = Todo.query.get_or_404(todo_id)
        todo.completed = not todo.completed
        todo.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'todo': todo.to_dict(),
            'message': '任务状态更新成功'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'状态更新失败: {str(e)}'
        }), 500


@app.route('/api/stats')
def api_get_stats():
    """
    获取统计信息的API接口
    """
    try:
        all_todos = Todo.query.all()
        completed_todos = [t for t in all_todos if t.completed]
        active_todos = [t for t in all_todos if not t.completed]
        
        # 按优先级统计
        priority_stats = {
            'high': len([t for t in active_todos if t.priority == 'high']),
            'medium': len([t for t in active_todos if t.priority == 'medium']),
            'low': len([t for t in active_todos if t.priority == 'low'])
        }
        
        # 逾期任务统计
        today = date.today()
        overdue_todos = [
            t for t in active_todos 
            if t.deadline and t.deadline < today
        ]
        
        stats = {
            'total': len(all_todos),
            'completed': len(completed_todos),
            'active': len(active_todos),
            'overdue': len(overdue_todos),
            'completion_rate': round(len(completed_todos) / len(all_todos) * 100, 1) if all_todos else 0,
            'priority_stats': priority_stats
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取统计信息失败: {str(e)}'
        }), 500


def init_sample_data():
    """
    初始化示例数据
    """
    if Todo.query.count() == 0:
        sample_todos = [
            Todo(
                content='学习Flask前端集成',
                priority='high',
                deadline=date.today()
            ),
            Todo(
                content='完成Session19的练习题',
                priority='medium',
                completed=False
            ),
            Todo(
                content='阅读JavaScript文档',
                priority='low',
                completed=True
            ),
            Todo(
                content='设计待办事项界面',
                priority='medium',
                completed=True
            )
        ]
        
        for todo in sample_todos:
            db.session.add(todo)
        
        try:
            db.session.commit()
            print("示例数据初始化成功！")
        except Exception as e:
            db.session.rollback()
            print(f"示例数据初始化失败: {e}")


def main():
    """
    主函数：演示程序的入口点
    """
    print("Session19: 前端集成演示")
    print("=" * 40)
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
        init_sample_data()
    
    print("\n待办事项管理器已启动！")
    print("访问 http://127.0.0.1:5000 查看应用")
    print("\nAPI接口说明:")
    print("- GET  /api/todos        - 获取所有待办事项")
    print("- POST /api/todos        - 添加新待办事项")
    print("- PUT  /api/todos/<id>   - 更新待办事项")
    print("- DELETE /api/todos/<id> - 删除待办事项")
    print("- POST /api/todos/<id>/toggle - 切换完成状态")
    print("- GET  /api/stats        - 获取统计信息")
    print("\n按 Ctrl+C 停止服务器")
    
    # 启动Flask应用
    app.run(debug=True, host='127.0.0.1', port=5000)


if __name__ == "__main__":
    main()