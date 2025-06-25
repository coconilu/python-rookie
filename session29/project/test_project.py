#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session29 项目演示: 完整的测试和调试项目

这是一个完整的项目，展示了如何在实际项目中应用测试和调试技术。
项目包含一个简单的任务管理系统，具有完整的测试覆盖和调试功能。

作者: Python教程团队
"""

import json
import datetime
import uuid
import logging
import time
import tracemalloc
import unittest
import asyncio
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
from unittest.mock import Mock, patch, MagicMock
import sqlite3
import threading
from concurrent.futures import ThreadPoolExecutor


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('task_manager.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Priority(Enum):
    """优先级枚举"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


@dataclass
class Task:
    """任务数据类"""
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    priority: Priority = Priority.MEDIUM
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None
    due_date: Optional[datetime.datetime] = None
    id: str = None
    
    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.datetime.now()
        if self.updated_at is None:
            self.updated_at = self.created_at
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        data = asdict(self)
        data['status'] = self.status.value
        data['priority'] = self.priority.value
        data['created_at'] = self.created_at.isoformat() if self.created_at else None
        data['updated_at'] = self.updated_at.isoformat() if self.updated_at else None
        data['due_date'] = self.due_date.isoformat() if self.due_date else None
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """从字典创建任务"""
        task = cls(
            id=data['id'],
            title=data['title'],
            description=data.get('description', ''),
            status=TaskStatus(data['status']),
            priority=Priority(data['priority'])
        )
        
        if data.get('created_at'):
            task.created_at = datetime.datetime.fromisoformat(data['created_at'])
        if data.get('updated_at'):
            task.updated_at = datetime.datetime.fromisoformat(data['updated_at'])
        if data.get('due_date'):
            task.due_date = datetime.datetime.fromisoformat(data['due_date'])
        
        return task


class DatabaseError(Exception):
    """数据库错误"""
    pass


class TaskNotFoundError(Exception):
    """任务未找到错误"""
    pass


class ValidationError(Exception):
    """验证错误"""
    pass


class DatabaseConnection:
    """数据库连接类"""
    
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.connection = None
        self._lock = threading.Lock()
    
    def connect(self):
        """连接数据库"""
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
            self._create_tables()
            logger.info(f"数据库连接成功: {self.db_path}")
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            raise DatabaseError(f"无法连接数据库: {e}")
    
    def disconnect(self):
        """断开数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("数据库连接已关闭")
    
    def _create_tables(self):
        """创建表"""
        with self._lock:
            cursor = self.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL,
                    priority INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    due_date TEXT
                )
            """)
            self.connection.commit()
    
    def execute_query(self, query: str, params: tuple = ()) -> List[sqlite3.Row]:
        """执行查询"""
        if not self.connection:
            raise DatabaseError("数据库未连接")
        
        with self._lock:
            try:
                cursor = self.connection.cursor()
                cursor.execute(query, params)
                return cursor.fetchall()
            except Exception as e:
                logger.error(f"查询执行失败: {e}")
                raise DatabaseError(f"查询失败: {e}")
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """执行更新"""
        if not self.connection:
            raise DatabaseError("数据库未连接")
        
        with self._lock:
            try:
                cursor = self.connection.cursor()
                cursor.execute(query, params)
                self.connection.commit()
                return cursor.rowcount
            except Exception as e:
                logger.error(f"更新执行失败: {e}")
                self.connection.rollback()
                raise DatabaseError(f"更新失败: {e}")


class TaskRepository:
    """任务仓库类"""
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
    
    def save_task(self, task: Task) -> bool:
        """保存任务"""
        try:
            query = """
                INSERT OR REPLACE INTO tasks 
                (id, title, description, status, priority, created_at, updated_at, due_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            params = (
                task.id,
                task.title,
                task.description,
                task.status.value,
                task.priority.value,
                task.created_at.isoformat(),
                task.updated_at.isoformat(),
                task.due_date.isoformat() if task.due_date else None
            )
            
            rows_affected = self.db.execute_update(query, params)
            logger.info(f"任务保存成功: {task.id}")
            return rows_affected > 0
            
        except Exception as e:
            logger.error(f"保存任务失败: {e}")
            raise
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """获取任务"""
        try:
            query = "SELECT * FROM tasks WHERE id = ?"
            rows = self.db.execute_query(query, (task_id,))
            
            if not rows:
                return None
            
            row = rows[0]
            task_data = dict(row)
            return Task.from_dict(task_data)
            
        except Exception as e:
            logger.error(f"获取任务失败: {e}")
            raise
    
    def get_all_tasks(self) -> List[Task]:
        """获取所有任务"""
        try:
            query = "SELECT * FROM tasks ORDER BY created_at DESC"
            rows = self.db.execute_query(query)
            
            tasks = []
            for row in rows:
                task_data = dict(row)
                tasks.append(Task.from_dict(task_data))
            
            return tasks
            
        except Exception as e:
            logger.error(f"获取所有任务失败: {e}")
            raise
    
    def delete_task(self, task_id: str) -> bool:
        """删除任务"""
        try:
            query = "DELETE FROM tasks WHERE id = ?"
            rows_affected = self.db.execute_update(query, (task_id,))
            
            if rows_affected == 0:
                raise TaskNotFoundError(f"任务不存在: {task_id}")
            
            logger.info(f"任务删除成功: {task_id}")
            return True
            
        except Exception as e:
            logger.error(f"删除任务失败: {e}")
            raise
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """根据状态获取任务"""
        try:
            query = "SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC"
            rows = self.db.execute_query(query, (status.value,))
            
            tasks = []
            for row in rows:
                task_data = dict(row)
                tasks.append(Task.from_dict(task_data))
            
            return tasks
            
        except Exception as e:
            logger.error(f"根据状态获取任务失败: {e}")
            raise


class NotificationService:
    """通知服务类"""
    
    def __init__(self):
        self.notifications = []
    
    def send_notification(self, message: str, task_id: str = None) -> bool:
        """发送通知"""
        try:
            notification = {
                'id': str(uuid.uuid4()),
                'message': message,
                'task_id': task_id,
                'timestamp': datetime.datetime.now().isoformat()
            }
            
            self.notifications.append(notification)
            logger.info(f"通知发送成功: {message}")
            return True
            
        except Exception as e:
            logger.error(f"发送通知失败: {e}")
            return False
    
    def get_notifications(self) -> List[Dict]:
        """获取所有通知"""
        return self.notifications.copy()
    
    def clear_notifications(self):
        """清空通知"""
        self.notifications.clear()


class TaskValidator:
    """任务验证器"""
    
    @staticmethod
    def validate_task(task: Task) -> bool:
        """验证任务"""
        if not task.title or not task.title.strip():
            raise ValidationError("任务标题不能为空")
        
        if len(task.title) > 100:
            raise ValidationError("任务标题不能超过100个字符")
        
        if len(task.description) > 1000:
            raise ValidationError("任务描述不能超过1000个字符")
        
        if task.due_date and task.due_date < datetime.datetime.now():
            raise ValidationError("截止日期不能是过去的时间")
        
        return True


class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self.metrics = []
    
    def monitor_function(self, func):
        """监控函数性能的装饰器"""
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            start_memory = self._get_memory_usage()
            
            try:
                result = func(*args, **kwargs)
                success = True
                error = None
            except Exception as e:
                result = None
                success = False
                error = str(e)
                raise
            finally:
                end_time = time.perf_counter()
                end_memory = self._get_memory_usage()
                
                metric = {
                    'function': func.__name__,
                    'execution_time': end_time - start_time,
                    'memory_used': end_memory - start_memory,
                    'success': success,
                    'error': error,
                    'timestamp': datetime.datetime.now().isoformat()
                }
                
                self.metrics.append(metric)
                logger.debug(f"性能监控: {func.__name__} - {metric}")
            
            return result
        return wrapper
    
    def _get_memory_usage(self) -> int:
        """获取当前内存使用量"""
        try:
            import psutil
            import os
            process = psutil.Process(os.getpid())
            return process.memory_info().rss
        except ImportError:
            return 0
    
    def get_metrics(self) -> List[Dict]:
        """获取性能指标"""
        return self.metrics.copy()
    
    def get_average_execution_time(self, function_name: str) -> float:
        """获取函数平均执行时间"""
        function_metrics = [m for m in self.metrics if m['function'] == function_name]
        if not function_metrics:
            return 0.0
        
        total_time = sum(m['execution_time'] for m in function_metrics)
        return total_time / len(function_metrics)


class TaskManager:
    """任务管理器主类"""
    
    def __init__(self, db_path: str = ":memory:"):
        self.db_connection = DatabaseConnection(db_path)
        self.repository = None
        self.notification_service = NotificationService()
        self.validator = TaskValidator()
        self.performance_monitor = PerformanceMonitor()
        self._is_initialized = False
    
    def initialize(self):
        """初始化任务管理器"""
        try:
            self.db_connection.connect()
            self.repository = TaskRepository(self.db_connection)
            self._is_initialized = True
            logger.info("任务管理器初始化成功")
        except Exception as e:
            logger.error(f"任务管理器初始化失败: {e}")
            raise
    
    def shutdown(self):
        """关闭任务管理器"""
        if self.db_connection:
            self.db_connection.disconnect()
        self._is_initialized = False
        logger.info("任务管理器已关闭")
    
    @property
    def is_initialized(self) -> bool:
        """检查是否已初始化"""
        return self._is_initialized
    
    def _ensure_initialized(self):
        """确保已初始化"""
        if not self._is_initialized:
            raise RuntimeError("任务管理器未初始化")
    
    def create_task(self, title: str, description: str = "", 
                   priority: Priority = Priority.MEDIUM,
                   due_date: Optional[datetime.datetime] = None) -> Task:
        """创建任务"""
        self._ensure_initialized()
        
        @self.performance_monitor.monitor_function
        def _create_task():
            task = Task(
                title=title,
                description=description,
                priority=priority,
                due_date=due_date
            )
            
            # 验证任务
            self.validator.validate_task(task)
            
            # 保存任务
            success = self.repository.save_task(task)
            if not success:
                raise DatabaseError("任务创建失败")
            
            # 发送通知
            self.notification_service.send_notification(
                f"新任务已创建: {task.title}", task.id
            )
            
            logger.info(f"任务创建成功: {task.id} - {task.title}")
            return task
        
        return _create_task()
    
    def get_task(self, task_id: str) -> Task:
        """获取任务"""
        self._ensure_initialized()
        
        @self.performance_monitor.monitor_function
        def _get_task():
            task = self.repository.get_task(task_id)
            if not task:
                raise TaskNotFoundError(f"任务不存在: {task_id}")
            return task
        
        return _get_task()
    
    def update_task(self, task_id: str, **kwargs) -> Task:
        """更新任务"""
        self._ensure_initialized()
        
        @self.performance_monitor.monitor_function
        def _update_task():
            # 获取现有任务
            task = self.get_task(task_id)
            
            # 更新字段
            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            
            # 更新时间戳
            task.updated_at = datetime.datetime.now()
            
            # 验证任务
            self.validator.validate_task(task)
            
            # 保存更新
            success = self.repository.save_task(task)
            if not success:
                raise DatabaseError("任务更新失败")
            
            # 发送通知
            self.notification_service.send_notification(
                f"任务已更新: {task.title}", task.id
            )
            
            logger.info(f"任务更新成功: {task.id}")
            return task
        
        return _update_task()
    
    def delete_task(self, task_id: str) -> bool:
        """删除任务"""
        self._ensure_initialized()
        
        @self.performance_monitor.monitor_function
        def _delete_task():
            # 获取任务信息用于通知
            task = self.get_task(task_id)
            
            # 删除任务
            success = self.repository.delete_task(task_id)
            
            if success:
                # 发送通知
                self.notification_service.send_notification(
                    f"任务已删除: {task.title}", task_id
                )
                logger.info(f"任务删除成功: {task_id}")
            
            return success
        
        return _delete_task()
    
    def list_tasks(self, status: Optional[TaskStatus] = None) -> List[Task]:
        """列出任务"""
        self._ensure_initialized()
        
        @self.performance_monitor.monitor_function
        def _list_tasks():
            if status:
                return self.repository.get_tasks_by_status(status)
            else:
                return self.repository.get_all_tasks()
        
        return _list_tasks()
    
    def complete_task(self, task_id: str) -> Task:
        """完成任务"""
        return self.update_task(task_id, status=TaskStatus.COMPLETED)
    
    def cancel_task(self, task_id: str) -> Task:
        """取消任务"""
        return self.update_task(task_id, status=TaskStatus.CANCELLED)
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        self._ensure_initialized()
        
        @self.performance_monitor.monitor_function
        def _get_statistics():
            all_tasks = self.list_tasks()
            
            stats = {
                'total_tasks': len(all_tasks),
                'pending_tasks': len([t for t in all_tasks if t.status == TaskStatus.PENDING]),
                'in_progress_tasks': len([t for t in all_tasks if t.status == TaskStatus.IN_PROGRESS]),
                'completed_tasks': len([t for t in all_tasks if t.status == TaskStatus.COMPLETED]),
                'cancelled_tasks': len([t for t in all_tasks if t.status == TaskStatus.CANCELLED]),
                'high_priority_tasks': len([t for t in all_tasks if t.priority == Priority.HIGH]),
                'urgent_tasks': len([t for t in all_tasks if t.priority == Priority.URGENT]),
                'overdue_tasks': len([
                    t for t in all_tasks 
                    if t.due_date and t.due_date < datetime.datetime.now() and t.status != TaskStatus.COMPLETED
                ])
            }
            
            return stats
        
        return _get_statistics()
    
    async def bulk_create_tasks(self, task_data_list: List[Dict]) -> List[Task]:
        """批量创建任务（异步）"""
        self._ensure_initialized()
        
        async def create_single_task(task_data):
            await asyncio.sleep(0.01)  # 模拟异步操作
            return self.create_task(**task_data)
        
        tasks = await asyncio.gather(*[
            create_single_task(task_data) for task_data in task_data_list
        ])
        
        return tasks
    
    def export_tasks(self, format: str = "json") -> str:
        """导出任务"""
        self._ensure_initialized()
        
        @self.performance_monitor.monitor_function
        def _export_tasks():
            tasks = self.list_tasks()
            
            if format.lower() == "json":
                task_dicts = [task.to_dict() for task in tasks]
                return json.dumps(task_dicts, indent=2, ensure_ascii=False)
            else:
                raise ValueError(f"不支持的导出格式: {format}")
        
        return _export_tasks()
    
    def import_tasks(self, data: str, format: str = "json") -> int:
        """导入任务"""
        self._ensure_initialized()
        
        @self.performance_monitor.monitor_function
        def _import_tasks():
            if format.lower() == "json":
                task_dicts = json.loads(data)
                imported_count = 0
                
                for task_dict in task_dicts:
                    try:
                        task = Task.from_dict(task_dict)
                        self.validator.validate_task(task)
                        self.repository.save_task(task)
                        imported_count += 1
                    except Exception as e:
                        logger.warning(f"导入任务失败: {e}")
                
                logger.info(f"成功导入 {imported_count} 个任务")
                return imported_count
            else:
                raise ValueError(f"不支持的导入格式: {format}")
        
        return _import_tasks()


# 完整的测试套件
class TestTaskManager(unittest.TestCase):
    """任务管理器测试套件"""
    
    def setUp(self):
        """设置测试环境"""
        self.task_manager = TaskManager()
        self.task_manager.initialize()
    
    def tearDown(self):
        """清理测试环境"""
        self.task_manager.shutdown()
    
    def test_create_task(self):
        """测试创建任务"""
        task = self.task_manager.create_task(
            title="测试任务",
            description="这是一个测试任务",
            priority=Priority.HIGH
        )
        
        self.assertIsNotNone(task.id)
        self.assertEqual(task.title, "测试任务")
        self.assertEqual(task.description, "这是一个测试任务")
        self.assertEqual(task.priority, Priority.HIGH)
        self.assertEqual(task.status, TaskStatus.PENDING)
    
    def test_get_task(self):
        """测试获取任务"""
        # 创建任务
        created_task = self.task_manager.create_task("测试任务")
        
        # 获取任务
        retrieved_task = self.task_manager.get_task(created_task.id)
        
        self.assertEqual(created_task.id, retrieved_task.id)
        self.assertEqual(created_task.title, retrieved_task.title)
    
    def test_get_nonexistent_task(self):
        """测试获取不存在的任务"""
        with self.assertRaises(TaskNotFoundError):
            self.task_manager.get_task("nonexistent-id")
    
    def test_update_task(self):
        """测试更新任务"""
        # 创建任务
        task = self.task_manager.create_task("原始标题")
        
        # 更新任务
        updated_task = self.task_manager.update_task(
            task.id,
            title="更新后的标题",
            status=TaskStatus.IN_PROGRESS
        )
        
        self.assertEqual(updated_task.title, "更新后的标题")
        self.assertEqual(updated_task.status, TaskStatus.IN_PROGRESS)
        self.assertGreater(updated_task.updated_at, task.updated_at)
    
    def test_delete_task(self):
        """测试删除任务"""
        # 创建任务
        task = self.task_manager.create_task("待删除任务")
        
        # 删除任务
        success = self.task_manager.delete_task(task.id)
        self.assertTrue(success)
        
        # 验证任务已删除
        with self.assertRaises(TaskNotFoundError):
            self.task_manager.get_task(task.id)
    
    def test_list_tasks(self):
        """测试列出任务"""
        # 创建多个任务
        task1 = self.task_manager.create_task("任务1")
        task2 = self.task_manager.create_task("任务2")
        
        # 更新一个任务状态
        self.task_manager.update_task(task1.id, status=TaskStatus.COMPLETED)
        
        # 获取所有任务
        all_tasks = self.task_manager.list_tasks()
        self.assertEqual(len(all_tasks), 2)
        
        # 获取待处理任务
        pending_tasks = self.task_manager.list_tasks(TaskStatus.PENDING)
        self.assertEqual(len(pending_tasks), 1)
        self.assertEqual(pending_tasks[0].id, task2.id)
        
        # 获取已完成任务
        completed_tasks = self.task_manager.list_tasks(TaskStatus.COMPLETED)
        self.assertEqual(len(completed_tasks), 1)
        self.assertEqual(completed_tasks[0].id, task1.id)
    
    def test_complete_task(self):
        """测试完成任务"""
        task = self.task_manager.create_task("待完成任务")
        
        completed_task = self.task_manager.complete_task(task.id)
        
        self.assertEqual(completed_task.status, TaskStatus.COMPLETED)
    
    def test_cancel_task(self):
        """测试取消任务"""
        task = self.task_manager.create_task("待取消任务")
        
        cancelled_task = self.task_manager.cancel_task(task.id)
        
        self.assertEqual(cancelled_task.status, TaskStatus.CANCELLED)
    
    def test_get_statistics(self):
        """测试获取统计信息"""
        # 创建不同状态和优先级的任务
        self.task_manager.create_task("任务1", priority=Priority.HIGH)
        self.task_manager.create_task("任务2", priority=Priority.URGENT)
        task3 = self.task_manager.create_task("任务3")
        
        # 完成一个任务
        self.task_manager.complete_task(task3.id)
        
        # 获取统计信息
        stats = self.task_manager.get_statistics()
        
        self.assertEqual(stats['total_tasks'], 3)
        self.assertEqual(stats['pending_tasks'], 2)
        self.assertEqual(stats['completed_tasks'], 1)
        self.assertEqual(stats['high_priority_tasks'], 1)
        self.assertEqual(stats['urgent_tasks'], 1)
    
    def test_task_validation(self):
        """测试任务验证"""
        # 测试空标题
        with self.assertRaises(ValidationError):
            self.task_manager.create_task("")
        
        # 测试标题过长
        with self.assertRaises(ValidationError):
            self.task_manager.create_task("x" * 101)
        
        # 测试描述过长
        with self.assertRaises(ValidationError):
            self.task_manager.create_task("正常标题", description="x" * 1001)
        
        # 测试过期日期
        past_date = datetime.datetime.now() - datetime.timedelta(days=1)
        with self.assertRaises(ValidationError):
            self.task_manager.create_task("正常标题", due_date=past_date)
    
    def test_export_import_tasks(self):
        """测试导出导入任务"""
        # 创建一些任务
        self.task_manager.create_task("任务1", description="描述1")
        self.task_manager.create_task("任务2", description="描述2", priority=Priority.HIGH)
        
        # 导出任务
        exported_data = self.task_manager.export_tasks()
        self.assertIsInstance(exported_data, str)
        
        # 清空当前任务
        tasks = self.task_manager.list_tasks()
        for task in tasks:
            self.task_manager.delete_task(task.id)
        
        # 验证任务已清空
        self.assertEqual(len(self.task_manager.list_tasks()), 0)
        
        # 导入任务
        imported_count = self.task_manager.import_tasks(exported_data)
        self.assertEqual(imported_count, 2)
        
        # 验证导入的任务
        imported_tasks = self.task_manager.list_tasks()
        self.assertEqual(len(imported_tasks), 2)
    
    @patch('uuid.uuid4')
    def test_task_id_generation(self, mock_uuid):
        """测试任务ID生成（使用Mock）"""
        mock_uuid.return_value.hex = 'mocked-uuid'
        mock_uuid.return_value.__str__ = lambda x: 'mocked-uuid'
        
        task = self.task_manager.create_task("测试任务")
        
        self.assertEqual(task.id, 'mocked-uuid')
        mock_uuid.assert_called()
    
    def test_notification_service(self):
        """测试通知服务"""
        # 创建任务会触发通知
        task = self.task_manager.create_task("测试任务")
        
        notifications = self.task_manager.notification_service.get_notifications()
        self.assertGreater(len(notifications), 0)
        
        # 检查通知内容
        notification = notifications[-1]
        self.assertIn("新任务已创建", notification['message'])
        self.assertEqual(notification['task_id'], task.id)
    
    def test_performance_monitoring(self):
        """测试性能监控"""
        # 执行一些操作
        self.task_manager.create_task("性能测试任务")
        
        # 检查性能指标
        metrics = self.task_manager.performance_monitor.get_metrics()
        self.assertGreater(len(metrics), 0)
        
        # 检查平均执行时间
        avg_time = self.task_manager.performance_monitor.get_average_execution_time('_create_task')
        self.assertGreater(avg_time, 0)
    
    def test_concurrent_access(self):
        """测试并发访问"""
        def create_tasks(start_index, count):
            tasks = []
            for i in range(count):
                task = self.task_manager.create_task(f"并发任务{start_index + i}")
                tasks.append(task)
            return tasks
        
        # 使用线程池并发创建任务
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(create_tasks, 0, 5),
                executor.submit(create_tasks, 5, 5),
                executor.submit(create_tasks, 10, 5)
            ]
            
            all_tasks = []
            for future in futures:
                tasks = future.result()
                all_tasks.extend(tasks)
        
        # 验证所有任务都创建成功
        self.assertEqual(len(all_tasks), 15)
        
        # 验证数据库中的任务数量
        db_tasks = self.task_manager.list_tasks()
        self.assertEqual(len(db_tasks), 15)
    
    def test_async_bulk_create(self):
        """测试异步批量创建"""
        task_data_list = [
            {'title': f'异步任务{i}', 'description': f'描述{i}'}
            for i in range(5)
        ]
        
        # 运行异步批量创建
        async def run_test():
            tasks = await self.task_manager.bulk_create_tasks(task_data_list)
            return tasks
        
        tasks = asyncio.run(run_test())
        
        self.assertEqual(len(tasks), 5)
        for i, task in enumerate(tasks):
            self.assertEqual(task.title, f'异步任务{i}')
            self.assertEqual(task.description, f'描述{i}')


class TestTaskManagerIntegration(unittest.TestCase):
    """任务管理器集成测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.task_manager = TaskManager("test_integration.db")
        self.task_manager.initialize()
    
    def tearDown(self):
        """清理测试环境"""
        self.task_manager.shutdown()
        import os
        if os.path.exists("test_integration.db"):
            os.remove("test_integration.db")
    
    def test_full_task_lifecycle(self):
        """测试完整的任务生命周期"""
        # 1. 创建任务
        task = self.task_manager.create_task(
            title="集成测试任务",
            description="这是一个集成测试任务",
            priority=Priority.HIGH,
            due_date=datetime.datetime.now() + datetime.timedelta(days=7)
        )
        
        # 2. 验证任务创建
        self.assertIsNotNone(task.id)
        self.assertEqual(task.status, TaskStatus.PENDING)
        
        # 3. 开始任务
        updated_task = self.task_manager.update_task(
            task.id, status=TaskStatus.IN_PROGRESS
        )
        self.assertEqual(updated_task.status, TaskStatus.IN_PROGRESS)
        
        # 4. 完成任务
        completed_task = self.task_manager.complete_task(task.id)
        self.assertEqual(completed_task.status, TaskStatus.COMPLETED)
        
        # 5. 验证统计信息
        stats = self.task_manager.get_statistics()
        self.assertEqual(stats['total_tasks'], 1)
        self.assertEqual(stats['completed_tasks'], 1)
        
        # 6. 导出任务
        exported_data = self.task_manager.export_tasks()
        self.assertIn("集成测试任务", exported_data)
        
        # 7. 删除任务
        success = self.task_manager.delete_task(task.id)
        self.assertTrue(success)
        
        # 8. 验证任务已删除
        final_stats = self.task_manager.get_statistics()
        self.assertEqual(final_stats['total_tasks'], 0)
    
    def test_error_handling(self):
        """测试错误处理"""
        # 测试未初始化的管理器
        uninit_manager = TaskManager()
        with self.assertRaises(RuntimeError):
            uninit_manager.create_task("测试")
        
        # 测试数据库错误
        with patch.object(self.task_manager.repository, 'save_task', side_effect=DatabaseError("数据库错误")):
            with self.assertRaises(DatabaseError):
                self.task_manager.create_task("测试任务")
        
        # 测试验证错误
        with self.assertRaises(ValidationError):
            self.task_manager.create_task("")  # 空标题
    
    def test_performance_under_load(self):
        """测试负载下的性能"""
        start_time = time.perf_counter()
        
        # 创建大量任务
        tasks = []
        for i in range(100):
            task = self.task_manager.create_task(f"负载测试任务{i}")
            tasks.append(task)
        
        end_time = time.perf_counter()
        creation_time = end_time - start_time
        
        print(f"\n创建100个任务耗时: {creation_time:.4f}秒")
        print(f"平均每个任务: {creation_time/100:.6f}秒")
        
        # 验证所有任务都创建成功
        all_tasks = self.task_manager.list_tasks()
        self.assertEqual(len(all_tasks), 100)
        
        # 测试查询性能
        start_time = time.perf_counter()
        for task in tasks[:10]:
            retrieved_task = self.task_manager.get_task(task.id)
            self.assertEqual(retrieved_task.id, task.id)
        end_time = time.perf_counter()
        
        query_time = end_time - start_time
        print(f"查询10个任务耗时: {query_time:.4f}秒")
        
        # 性能应该在合理范围内
        self.assertLess(creation_time, 10.0)  # 创建100个任务应该在10秒内
        self.assertLess(query_time, 1.0)      # 查询10个任务应该在1秒内


def run_all_tests():
    """运行所有测试"""
    print("开始运行任务管理器测试套件...")
    print("=" * 60)
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestTaskManager))
    suite.addTests(loader.loadTestsFromTestCase(TestTaskManagerIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出测试统计
    print(f"\n测试统计:")
    print(f"运行测试: {result.testsRun}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    if result.failures:
        print("\n失败的测试:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\n错误的测试:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    return result.wasSuccessful()


def demonstrate_task_manager():
    """演示任务管理器功能"""
    print("\n=== 任务管理器功能演示 ===")
    
    # 创建任务管理器
    manager = TaskManager()
    manager.initialize()
    
    try:
        # 1. 创建任务
        print("\n1. 创建任务")
        task1 = manager.create_task(
            "学习Python测试",
            "学习unittest, pytest, mock等测试技术",
            Priority.HIGH,
            datetime.datetime.now() + datetime.timedelta(days=3)
        )
        print(f"创建任务: {task1.title} (ID: {task1.id[:8]}...)")
        
        task2 = manager.create_task(
            "编写项目文档",
            "为项目编写完整的技术文档",
            Priority.MEDIUM
        )
        print(f"创建任务: {task2.title} (ID: {task2.id[:8]}...)")
        
        # 2. 列出任务
        print("\n2. 列出所有任务")
        tasks = manager.list_tasks()
        for task in tasks:
            print(f"- {task.title} [{task.status.value}] ({task.priority.name})")
        
        # 3. 更新任务状态
        print("\n3. 开始第一个任务")
        manager.update_task(task1.id, status=TaskStatus.IN_PROGRESS)
        print(f"任务 '{task1.title}' 状态更新为进行中")
        
        # 4. 完成任务
        print("\n4. 完成第一个任务")
        manager.complete_task(task1.id)
        print(f"任务 '{task1.title}' 已完成")
        
        # 5. 获取统计信息
        print("\n5. 统计信息")
        stats = manager.get_statistics()
        for key, value in stats.items():
            print(f"- {key}: {value}")
        
        # 6. 导出任务
        print("\n6. 导出任务数据")
        exported_data = manager.export_tasks()
        print(f"导出数据长度: {len(exported_data)} 字符")
        
        # 7. 查看通知
        print("\n7. 通知历史")
        notifications = manager.notification_service.get_notifications()
        for notification in notifications[-3:]:  # 显示最后3个通知
            print(f"- {notification['message']} ({notification['timestamp'][:19]})")
        
        # 8. 性能指标
        print("\n8. 性能指标")
        metrics = manager.performance_monitor.get_metrics()
        if metrics:
            avg_create_time = manager.performance_monitor.get_average_execution_time('_create_task')
            avg_list_time = manager.performance_monitor.get_average_execution_time('_list_tasks')
            print(f"- 平均创建任务时间: {avg_create_time:.6f}秒")
            print(f"- 平均列出任务时间: {avg_list_time:.6f}秒")
        
        print("\n演示完成！")
        
    finally:
        manager.shutdown()


if __name__ == "__main__":
    print("Session29 项目演示: 完整的测试和调试项目")
    print("=" * 60)
    
    print("\n这个项目展示了:")
    print("1. 完整的项目架构设计")
    print("2. 全面的单元测试和集成测试")
    print("3. Mock测试和异步测试")
    print("4. 性能监控和调试技术")
    print("5. 错误处理和验证")
    print("6. 数据库操作和事务管理")
    print("7. 并发安全和线程安全")
    print("8. 日志记录和通知系统")
    
    # 演示功能
    demonstrate_task_manager()
    
    # 运行测试
    print("\n" + "=" * 60)
    success = run_all_tests()
    
    if success:
        print("\n🎉 所有测试都通过了！")
        print("\n项目特色:")
        print("- 完整的测试覆盖")
        print("- 性能监控和优化")
        print("- 错误处理和恢复")
        print("- 并发安全设计")
        print("- 可扩展的架构")
    else:
        print("\n❌ 有测试失败，请检查代码")