#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session20 API开发练习1 - 基础API开发
任务管理系统API

练习目标:
1. 创建RESTful API端点
2. 实现CRUD操作
3. 添加数据验证
4. 处理错误情况

作者: Python学习教程
日期: 2024
"""

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime
import json

# TODO: 创建Flask应用和API实例
# 提示: 使用Flask(__name__)和Api(app)
app = None  # 请替换为正确的Flask应用实例
api = None  # 请替换为正确的Api实例

# 模拟任务数据存储
tasks_data = [
    {
        'id': 1,
        'title': '学习Python',
        'description': '完成Python基础教程',
        'status': 'pending',  # pending, in_progress, completed
        'priority': 'high',   # low, medium, high
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

class TaskListAPI(Resource):
    """任务列表API资源"""
    
    def get(self):
        """获取任务列表
        
        TODO: 实现以下功能
        1. 支持按状态筛选 (?status=pending)
        2. 支持按优先级筛选 (?priority=high)
        3. 支持搜索功能 (?search=关键词)
        4. 支持分页 (?page=1&per_page=10)
        
        返回格式:
        {
            "success": true,
            "data": [...],
            "pagination": {...}
        }
        """
        # TODO: 在这里实现获取任务列表的逻辑
        pass
    
    def post(self):
        """创建新任务
        
        TODO: 实现以下功能
        1. 验证必需字段: title
        2. 验证可选字段: description, priority, status
        3. 设置默认值: status='pending', priority='medium'
        4. 自动设置创建时间和更新时间
        5. 生成唯一ID
        
        请求体格式:
        {
            "title": "任务标题",
            "description": "任务描述",
            "priority": "high|medium|low",
            "status": "pending|in_progress|completed"
        }
        
        返回格式:
        {
            "success": true,
            "message": "任务创建成功",
            "data": {...}
        }
        """
        # TODO: 在这里实现创建任务的逻辑
        pass

class TaskAPI(Resource):
    """单个任务API资源"""
    
    def get(self, task_id):
        """获取指定ID的任务
        
        TODO: 实现以下功能
        1. 根据task_id查找任务
        2. 如果任务不存在，返回404错误
        3. 返回任务详情
        
        返回格式:
        {
            "success": true,
            "data": {...}
        }
        """
        # TODO: 在这里实现获取单个任务的逻辑
        pass
    
    def put(self, task_id):
        """更新指定ID的任务
        
        TODO: 实现以下功能
        1. 根据task_id查找任务
        2. 如果任务不存在，返回404错误
        3. 验证更新字段的有效性
        4. 更新任务信息
        5. 自动更新updated_at时间
        
        请求体格式:
        {
            "title": "新标题",
            "description": "新描述",
            "status": "new_status",
            "priority": "new_priority"
        }
        
        返回格式:
        {
            "success": true,
            "message": "任务更新成功",
            "data": {...}
        }
        """
        # TODO: 在这里实现更新任务的逻辑
        pass
    
    def delete(self, task_id):
        """删除指定ID的任务
        
        TODO: 实现以下功能
        1. 根据task_id查找任务
        2. 如果任务不存在，返回404错误
        3. 删除任务
        4. 返回删除成功信息
        
        返回格式:
        {
            "success": true,
            "message": "任务删除成功"
        }
        """
        # TODO: 在这里实现删除任务的逻辑
        pass

class TaskStatsAPI(Resource):
    """任务统计API资源"""
    
    def get(self):
        """获取任务统计信息
        
        TODO: 实现以下功能
        1. 统计总任务数
        2. 按状态统计任务数量
        3. 按优先级统计任务数量
        4. 计算完成率
        
        返回格式:
        {
            "success": true,
            "data": {
                "total_tasks": 10,
                "by_status": {
                    "pending": 3,
                    "in_progress": 4,
                    "completed": 3
                },
                "by_priority": {
                    "high": 2,
                    "medium": 5,
                    "low": 3
                },
                "completion_rate": 30.0
            }
        }
        """
        # TODO: 在这里实现统计功能的逻辑
        pass

# TODO: 注册API路由
# 提示: 使用api.add_resource()方法
# api.add_resource(TaskListAPI, '/api/tasks')
# api.add_resource(TaskAPI, '/api/tasks/<int:task_id>')
# api.add_resource(TaskStatsAPI, '/api/tasks/stats')

# TODO: 添加根路径处理
@app.route('/')
def index():
    """API首页
    
    TODO: 返回API信息和可用端点列表
    """
    # TODO: 实现API首页信息
    pass

# TODO: 添加错误处理
@app.errorhandler(404)
def not_found(error):
    """404错误处理
    
    TODO: 返回JSON格式的404错误信息
    """
    # TODO: 实现404错误处理
    pass

@app.errorhandler(400)
def bad_request(error):
    """400错误处理
    
    TODO: 返回JSON格式的400错误信息
    """
    # TODO: 实现400错误处理
    pass

@app.errorhandler(500)
def internal_error(error):
    """500错误处理
    
    TODO: 返回JSON格式的500错误信息
    """
    # TODO: 实现500错误处理
    pass

# 辅助函数
def validate_task_data(data, required_fields=None):
    """验证任务数据
    
    TODO: 实现数据验证逻辑
    1. 检查必需字段
    2. 验证字段值的有效性
    3. 返回验证结果和错误信息
    
    Args:
        data: 要验证的数据字典
        required_fields: 必需字段列表
    
    Returns:
        tuple: (is_valid, error_message)
    """
    # TODO: 实现数据验证逻辑
    pass

def find_task_by_id(task_id):
    """根据ID查找任务
    
    TODO: 实现查找逻辑
    
    Args:
        task_id: 任务ID
    
    Returns:
        dict or None: 找到的任务或None
    """
    # TODO: 实现查找逻辑
    pass

def filter_tasks(tasks, filters):
    """根据条件筛选任务
    
    TODO: 实现筛选逻辑
    1. 支持按状态筛选
    2. 支持按优先级筛选
    3. 支持搜索功能
    
    Args:
        tasks: 任务列表
        filters: 筛选条件字典
    
    Returns:
        list: 筛选后的任务列表
    """
    # TODO: 实现筛选逻辑
    pass

def paginate_tasks(tasks, page, per_page):
    """对任务列表进行分页
    
    TODO: 实现分页逻辑
    
    Args:
        tasks: 任务列表
        page: 页码
        per_page: 每页数量
    
    Returns:
        tuple: (分页后的任务列表, 分页信息字典)
    """
    # TODO: 实现分页逻辑
    pass

if __name__ == '__main__':
    print("\n" + "="*50)
    print("📝 Session20 练习1: 任务管理API")
    print("="*50)
    print("\n🎯 练习目标:")
    print("  1. 完成Flask应用和API实例的创建")
    print("  2. 实现TaskListAPI的get和post方法")
    print("  3. 实现TaskAPI的get、put、delete方法")
    print("  4. 实现TaskStatsAPI的get方法")
    print("  5. 添加路由注册和错误处理")
    print("  6. 实现辅助函数")
    print("\n📋 API端点:")
    print("  GET    /api/tasks           - 获取任务列表")
    print("  POST   /api/tasks           - 创建新任务")
    print("  GET    /api/tasks/{id}      - 获取任务详情")
    print("  PUT    /api/tasks/{id}      - 更新任务")
    print("  DELETE /api/tasks/{id}      - 删除任务")
    print("  GET    /api/tasks/stats     - 获取统计信息")
    print("\n💡 提示:")
    print("  - 查看注释中的TODO项目")
    print("  - 参考basic_api.py示例")
    print("  - 测试每个功能是否正常工作")
    print("  - 确保错误处理完善")
    print("\n🚀 完成后运行: python exercise1.py")
    print("="*50)
    
    # TODO: 取消注释下面的代码来启动应用
    # if app:
    #     app.run(debug=True, host='0.0.0.0', port=5002)
    # else:
    #     print("❌ 请先完成Flask应用的创建")