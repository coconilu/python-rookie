#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session20 API开发练习1 - 参考答案
任务管理系统API完整实现

作者: Python学习教程
日期: 2024
"""

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime
import json
import re

# 创建Flask应用和API实例
app = Flask(__name__)
app.config['SECRET_KEY'] = 'exercise1-secret-key'
api = Api(app)

# 模拟任务数据存储
tasks_data = [
    {
        'id': 1,
        'title': '学习Python',
        'description': '完成Python基础教程',
        'status': 'pending',
        'priority': 'high',
        'created_at': '2024-01-01T10:00:00',
        'updated_at': '2024-01-01T10:00:00'
    },
    {
        'id': 2,
        'title': '开发API',
        'description': '使用Flask开发RESTful API',
        'status': 'in_progress',
        'priority': 'medium',
        'created_at': '2024-01-02T11:00:00',
        'updated_at': '2024-01-02T11:00:00'
    }
]

next_task_id = 3

# 辅助函数
def validate_task_data(data, required_fields=None):
    """验证任务数据"""
    if not data:
        return False, "请求体不能为空"
    
    # 检查必需字段
    if required_fields:
        for field in required_fields:
            if field not in data or not data[field]:
                return False, f"缺少必需字段: {field}"
    
    # 验证状态值
    if 'status' in data:
        valid_statuses = ['pending', 'in_progress', 'completed']
        if data['status'] not in valid_statuses:
            return False, f"无效的状态值，必须是: {', '.join(valid_statuses)}"
    
    # 验证优先级值
    if 'priority' in data:
        valid_priorities = ['low', 'medium', 'high']
        if data['priority'] not in valid_priorities:
            return False, f"无效的优先级值，必须是: {', '.join(valid_priorities)}"
    
    # 验证标题长度
    if 'title' in data:
        title = str(data['title']).strip()
        if len(title) < 1 or len(title) > 200:
            return False, "标题长度必须在1-200个字符之间"
    
    # 验证描述长度
    if 'description' in data:
        description = str(data['description']).strip()
        if len(description) > 1000:
            return False, "描述长度不能超过1000个字符"
    
    return True, None

def find_task_by_id(task_id):
    """根据ID查找任务"""
    return next((task for task in tasks_data if task['id'] == task_id), None)

def filter_tasks(tasks, filters):
    """根据条件筛选任务"""
    filtered_tasks = tasks.copy()
    
    # 按状态筛选
    if 'status' in filters and filters['status']:
        filtered_tasks = [task for task in filtered_tasks 
                         if task['status'] == filters['status']]
    
    # 按优先级筛选
    if 'priority' in filters and filters['priority']:
        filtered_tasks = [task for task in filtered_tasks 
                         if task['priority'] == filters['priority']]
    
    # 搜索功能
    if 'search' in filters and filters['search']:
        search_term = filters['search'].lower()
        filtered_tasks = [task for task in filtered_tasks 
                         if search_term in task['title'].lower() or 
                            search_term in task.get('description', '').lower()]
    
    return filtered_tasks

def paginate_tasks(tasks, page, per_page):
    """对任务列表进行分页"""
    total = len(tasks)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_tasks = tasks[start:end]
    
    pagination_info = {
        'page': page,
        'per_page': per_page,
        'total': total,
        'pages': (total + per_page - 1) // per_page,
        'has_next': end < total,
        'has_prev': page > 1
    }
    
    return paginated_tasks, pagination_info

class TaskListAPI(Resource):
    """任务列表API资源"""
    
    def get(self):
        """获取任务列表"""
        try:
            # 获取查询参数
            status = request.args.get('status')
            priority = request.args.get('priority')
            search = request.args.get('search')
            page = int(request.args.get('page', 1))
            per_page = min(int(request.args.get('per_page', 10)), 100)
            
            if page < 1:
                return {
                    'success': False,
                    'message': '页码必须大于0'
                }, 400
            
            if per_page < 1:
                return {
                    'success': False,
                    'message': '每页数量必须大于0'
                }, 400
            
            # 筛选任务
            filters = {
                'status': status,
                'priority': priority,
                'search': search
            }
            filtered_tasks = filter_tasks(tasks_data, filters)
            
            # 分页处理
            paginated_tasks, pagination_info = paginate_tasks(filtered_tasks, page, per_page)
            
            return {
                'success': True,
                'data': paginated_tasks,
                'pagination': pagination_info
            }, 200
            
        except ValueError:
            return {
                'success': False,
                'message': '页码和每页数量必须是数字'
            }, 400
        except Exception as e:
            return {
                'success': False,
                'message': f'获取任务列表失败: {str(e)}'
            }, 500
    
    def post(self):
        """创建新任务"""
        try:
            data = request.get_json()
            
            # 验证数据
            is_valid, error_message = validate_task_data(data, required_fields=['title'])
            if not is_valid:
                return {
                    'success': False,
                    'message': error_message
                }, 400
            
            # 创建新任务
            global next_task_id
            current_time = datetime.now().isoformat()
            
            new_task = {
                'id': next_task_id,
                'title': data['title'].strip(),
                'description': data.get('description', '').strip(),
                'status': data.get('status', 'pending'),
                'priority': data.get('priority', 'medium'),
                'created_at': current_time,
                'updated_at': current_time
            }
            
            tasks_data.append(new_task)
            next_task_id += 1
            
            return {
                'success': True,
                'message': '任务创建成功',
                'data': new_task
            }, 201
            
        except Exception as e:
            return {
                'success': False,
                'message': f'创建任务失败: {str(e)}'
            }, 500

class TaskAPI(Resource):
    """单个任务API资源"""
    
    def get(self, task_id):
        """获取指定ID的任务"""
        try:
            task = find_task_by_id(task_id)
            
            if not task:
                return {
                    'success': False,
                    'message': '任务不存在'
                }, 404
            
            return {
                'success': True,
                'data': task
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'获取任务失败: {str(e)}'
            }, 500
    
    def put(self, task_id):
        """更新指定ID的任务"""
        try:
            task = find_task_by_id(task_id)
            
            if not task:
                return {
                    'success': False,
                    'message': '任务不存在'
                }, 404
            
            data = request.get_json()
            
            # 验证数据
            is_valid, error_message = validate_task_data(data)
            if not is_valid:
                return {
                    'success': False,
                    'message': error_message
                }, 400
            
            # 更新任务字段
            updatable_fields = ['title', 'description', 'status', 'priority']
            for field in updatable_fields:
                if field in data:
                    if field in ['title', 'description']:
                        task[field] = str(data[field]).strip()
                    else:
                        task[field] = data[field]
            
            # 更新时间
            task['updated_at'] = datetime.now().isoformat()
            
            return {
                'success': True,
                'message': '任务更新成功',
                'data': task
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'更新任务失败: {str(e)}'
            }, 500
    
    def delete(self, task_id):
        """删除指定ID的任务"""
        try:
            task_index = next((i for i, task in enumerate(tasks_data) 
                             if task['id'] == task_id), None)
            
            if task_index is None:
                return {
                    'success': False,
                    'message': '任务不存在'
                }, 404
            
            # 删除任务
            deleted_task = tasks_data.pop(task_index)
            
            return {
                'success': True,
                'message': '任务删除成功',
                'data': deleted_task
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'删除任务失败: {str(e)}'
            }, 500

class TaskStatsAPI(Resource):
    """任务统计API资源"""
    
    def get(self):
        """获取任务统计信息"""
        try:
            total_tasks = len(tasks_data)
            
            # 按状态统计
            by_status = {'pending': 0, 'in_progress': 0, 'completed': 0}
            for task in tasks_data:
                status = task['status']
                if status in by_status:
                    by_status[status] += 1
            
            # 按优先级统计
            by_priority = {'low': 0, 'medium': 0, 'high': 0}
            for task in tasks_data:
                priority = task['priority']
                if priority in by_priority:
                    by_priority[priority] += 1
            
            # 计算完成率
            completed_tasks = by_status['completed']
            completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            
            stats = {
                'total_tasks': total_tasks,
                'by_status': by_status,
                'by_priority': by_priority,
                'completion_rate': round(completion_rate, 2)
            }
            
            return {
                'success': True,
                'data': stats
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'获取统计信息失败: {str(e)}'
            }, 500

# 注册API路由
api.add_resource(TaskListAPI, '/api/tasks')
api.add_resource(TaskAPI, '/api/tasks/<int:task_id>')
api.add_resource(TaskStatsAPI, '/api/tasks/stats')

# 根路径处理
@app.route('/')
def index():
    """API首页"""
    return jsonify({
        'message': 'Task Management API',
        'version': '1.0.0',
        'description': 'Session20 练习1 - 任务管理系统API',
        'endpoints': {
            'tasks': {
                'GET /api/tasks': '获取任务列表',
                'POST /api/tasks': '创建新任务',
                'GET /api/tasks/{id}': '获取任务详情',
                'PUT /api/tasks/{id}': '更新任务',
                'DELETE /api/tasks/{id}': '删除任务'
            },
            'stats': {
                'GET /api/tasks/stats': '获取统计信息'
            }
        },
        'query_parameters': {
            'GET /api/tasks': {
                'status': 'pending|in_progress|completed',
                'priority': 'low|medium|high',
                'search': '搜索关键词',
                'page': '页码 (默认1)',
                'per_page': '每页数量 (默认10, 最大100)'
            }
        },
        'examples': {
            'get_pending_tasks': 'GET /api/tasks?status=pending',
            'search_tasks': 'GET /api/tasks?search=Python',
            'get_high_priority': 'GET /api/tasks?priority=high&page=1&per_page=5',
            'create_task': 'POST /api/tasks with JSON body',
            'update_task': 'PUT /api/tasks/1 with JSON body',
            'get_stats': 'GET /api/tasks/stats'
        }
    })

# 错误处理
@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({
        'success': False,
        'message': '请求的资源不存在',
        'error_code': 404
    }), 404

@app.errorhandler(400)
def bad_request(error):
    """400错误处理"""
    return jsonify({
        'success': False,
        'message': '请求格式错误',
        'error_code': 400
    }), 400

@app.errorhandler(405)
def method_not_allowed(error):
    """405错误处理"""
    return jsonify({
        'success': False,
        'message': '不支持的HTTP方法',
        'error_code': 405
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return jsonify({
        'success': False,
        'message': '服务器内部错误',
        'error_code': 500
    }), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("✅ Session20 练习1 - 参考答案")
    print("📝 任务管理系统API")
    print("="*50)
    print("\n🚀 启动服务...")
    print("🌐 访问地址: http://localhost:5002")
    print("📖 API文档: http://localhost:5002")
    print("\n📋 可用端点:")
    print("  GET    /api/tasks           - 获取任务列表")
    print("  POST   /api/tasks           - 创建新任务")
    print("  GET    /api/tasks/{id}      - 获取任务详情")
    print("  PUT    /api/tasks/{id}      - 更新任务")
    print("  DELETE /api/tasks/{id}      - 删除任务")
    print("  GET    /api/tasks/stats     - 获取统计信息")
    print("\n🔍 查询参数示例:")
    print("  /api/tasks?status=pending")
    print("  /api/tasks?priority=high&page=1&per_page=5")
    print("  /api/tasks?search=Python")
    print("\n📊 测试命令:")
    print("  curl http://localhost:5002/api/tasks")
    print("  curl http://localhost:5002/api/tasks/stats")
    print("\n按 Ctrl+C 停止服务")
    print("="*50)
    
    app.run(debug=True, host='0.0.0.0', port=5002)