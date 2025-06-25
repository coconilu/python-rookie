#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session28: 模块化开发实践 - 演示代码

本文件演示了模块化开发的核心概念和实践，包括：
- 依赖注入容器的使用
- 事件驱动架构
- 插件系统
- 模块间通信

作者: Python教程团队
创建日期: 2024-01-15
最后修改: 2024-01-15
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from abc import ABC, abstractmethod
import uuid
import time


# ============================================================================
# 1. 核心实体和接口定义
# ============================================================================

@dataclass
class Task:
    """任务实体"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = ""
    title: str = ""
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    
    def mark_completed(self) -> None:
        """标记任务为已完成"""
        self.completed = True
        self.completed_at = datetime.now()


class TaskRepositoryInterface(ABC):
    """任务仓储接口"""
    
    @abstractmethod
    def save(self, task: Task) -> Task:
        """保存任务"""
        pass
    
    @abstractmethod
    def find_by_id(self, task_id: str) -> Optional[Task]:
        """根据ID查找任务"""
        pass
    
    @abstractmethod
    def find_by_user_id(self, user_id: str) -> List[Task]:
        """根据用户ID查找任务"""
        pass


# ============================================================================
# 2. 依赖注入容器实现
# ============================================================================

class DIContainer:
    """简化的依赖注入容器"""
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, type] = {}
        self._singletons: Dict[str, Any] = {}
    
    def register(self, interface: type, implementation: type, singleton: bool = True) -> None:
        """注册服务"""
        key = interface.__name__
        if singleton:
            self._factories[key] = implementation
        else:
            self._services[key] = implementation
    
    def register_instance(self, interface: type, instance: Any) -> None:
        """注册实例"""
        key = interface.__name__
        self._services[key] = instance
    
    def resolve(self, interface: type):
        """解析服务"""
        key = interface.__name__
        
        # 检查已注册的实例
        if key in self._services:
            return self._services[key]
        
        # 检查工厂并创建单例
        if key in self._factories:
            if key not in self._singletons:
                implementation = self._factories[key]
                # 简化的依赖注入（实际项目中需要更复杂的实现）
                if hasattr(implementation, '__init__'):
                    try:
                        instance = implementation()
                    except TypeError:
                        # 如果构造函数需要参数，尝试解析依赖
                        instance = self._create_with_dependencies(implementation)
                else:
                    instance = implementation()
                self._singletons[key] = instance
            return self._singletons[key]
        
        raise ValueError(f"Service {interface.__name__} not registered")
    
    def _create_with_dependencies(self, cls):
        """创建带依赖的实例（简化版）"""
        # 这里简化处理，实际项目中需要使用inspect模块分析构造函数
        return cls()


# ============================================================================
# 3. 事件系统实现
# ============================================================================

@dataclass
class Event:
    """事件基类"""
    event_id: str
    event_type: str
    timestamp: datetime
    data: Dict[str, Any]
    
    def __init__(self, event_type: str, data: Dict[str, Any]):
        self.event_id = str(uuid.uuid4())
        self.event_type = event_type
        self.timestamp = datetime.now()
        self.data = data


class EventHandler(ABC):
    """事件处理器接口"""
    
    @abstractmethod
    async def handle(self, event: Event) -> None:
        """处理事件"""
        pass


class EventBus:
    """事件总线"""
    
    def __init__(self):
        self._handlers: Dict[str, List[EventHandler]] = {}
    
    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        """订阅事件"""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
    
    async def publish(self, event: Event) -> None:
        """发布事件"""
        handlers = self._handlers.get(event.event_type, [])
        if handlers:
            tasks = [handler.handle(event) for handler in handlers]
            await asyncio.gather(*tasks, return_exceptions=True)
    
    def publish_sync(self, event: Event) -> None:
        """同步发布事件"""
        try:
            asyncio.run(self.publish(event))
        except RuntimeError:
            # 如果已经在事件循环中，使用同步处理
            handlers = self._handlers.get(event.event_type, [])
            for handler in handlers:
                try:
                    # 对于演示，我们同步调用异步方法
                    if hasattr(handler, 'handle_sync'):
                        handler.handle_sync(event)
                    else:
                        print(f"处理事件: {event.event_type}")
                except Exception as e:
                    print(f"事件处理失败: {e}")


# ============================================================================
# 4. 具体实现类
# ============================================================================

class InMemoryTaskRepository(TaskRepositoryInterface):
    """内存任务仓储实现"""
    
    def __init__(self):
        self._tasks: Dict[str, Task] = {}
    
    def save(self, task: Task) -> Task:
        """保存任务"""
        self._tasks[task.id] = task
        return task
    
    def find_by_id(self, task_id: str) -> Optional[Task]:
        """根据ID查找任务"""
        return self._tasks.get(task_id)
    
    def find_by_user_id(self, user_id: str) -> List[Task]:
        """根据用户ID查找任务"""
        return [task for task in self._tasks.values() if task.user_id == user_id]


class TaskService:
    """任务服务"""
    
    def __init__(self, task_repository: TaskRepositoryInterface = None, event_bus: EventBus = None):
        self._task_repository = task_repository or InMemoryTaskRepository()
        self._event_bus = event_bus
    
    def create_task(self, user_id: str, title: str, description: str) -> Task:
        """创建任务"""
        task = Task(
            user_id=user_id,
            title=title,
            description=description
        )
        
        saved_task = self._task_repository.save(task)
        
        # 发布事件
        if self._event_bus:
            event = Event('task.created', {
                'task_id': saved_task.id,
                'user_id': saved_task.user_id,
                'title': saved_task.title
            })
            self._event_bus.publish_sync(event)
        
        return saved_task
    
    def complete_task(self, task_id: str) -> bool:
        """完成任务"""
        task = self._task_repository.find_by_id(task_id)
        if task and not task.completed:
            task.mark_completed()
            self._task_repository.save(task)
            
            # 发布事件
            if self._event_bus:
                event = Event('task.completed', {
                    'task_id': task.id,
                    'user_id': task.user_id,
                    'completed_at': task.completed_at.isoformat()
                })
                self._event_bus.publish_sync(event)
            
            return True
        return False
    
    def get_user_tasks(self, user_id: str) -> List[Task]:
        """获取用户任务"""
        return self._task_repository.find_by_user_id(user_id)


# ============================================================================
# 5. 事件处理器实现
# ============================================================================

class EmailNotificationHandler(EventHandler):
    """邮件通知处理器"""
    
    async def handle(self, event: Event) -> None:
        """处理邮件通知"""
        if event.event_type == 'task.created':
            data = event.data
            print(f"📧 邮件通知: 您的任务 '{data['title']}' 已创建成功")
        elif event.event_type == 'task.completed':
            data = event.data
            print(f"📧 邮件通知: 恭喜！您已完成任务 {data['task_id']}")
    
    def handle_sync(self, event: Event) -> None:
        """同步处理方法"""
        if event.event_type == 'task.created':
            data = event.data
            print(f"📧 邮件通知: 您的任务 '{data['title']}' 已创建成功")
        elif event.event_type == 'task.completed':
            data = event.data
            print(f"📧 邮件通知: 恭喜！您已完成任务 {data['task_id']}")


class MetricsHandler(EventHandler):
    """指标统计处理器"""
    
    def __init__(self):
        self.task_created_count = 0
        self.task_completed_count = 0
    
    async def handle(self, event: Event) -> None:
        """更新指标"""
        if event.event_type == 'task.created':
            self.task_created_count += 1
            print(f"📊 指标更新: 创建任务数 +1 (总计: {self.task_created_count})")
        elif event.event_type == 'task.completed':
            self.task_completed_count += 1
            print(f"📊 指标更新: 完成任务数 +1 (总计: {self.task_completed_count})")
    
    def handle_sync(self, event: Event) -> None:
        """同步处理方法"""
        if event.event_type == 'task.created':
            self.task_created_count += 1
            print(f"📊 指标更新: 创建任务数 +1 (总计: {self.task_created_count})")
        elif event.event_type == 'task.completed':
            self.task_completed_count += 1
            print(f"📊 指标更新: 完成任务数 +1 (总计: {self.task_completed_count})")


class AuditLogHandler(EventHandler):
    """审计日志处理器"""
    
    async def handle(self, event: Event) -> None:
        """记录审计日志"""
        print(f"📝 审计日志: {event.event_type} 事件已记录 (ID: {event.event_id})")
    
    def handle_sync(self, event: Event) -> None:
        """同步处理方法"""
        print(f"📝 审计日志: {event.event_type} 事件已记录 (ID: {event.event_id})")


# ============================================================================
# 6. 插件系统实现
# ============================================================================

class PluginInterface(ABC):
    """插件接口"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        pass
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        pass
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Any:
        pass


class TaskExportPlugin(PluginInterface):
    """任务导出插件"""
    
    @property
    def name(self) -> str:
        return "task_export"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    def initialize(self, config: Dict[str, Any]) -> None:
        self.export_format = config.get('format', 'json')
    
    def execute(self, context: Dict[str, Any]) -> Any:
        tasks = context.get('tasks', [])
        
        if self.export_format == 'json':
            # 转换Task对象为字典
            task_dicts = []
            for task in tasks:
                task_dict = {
                    'id': task.id,
                    'user_id': task.user_id,
                    'title': task.title,
                    'description': task.description,
                    'completed': task.completed,
                    'created_at': task.created_at.isoformat()
                }
                if task.completed_at:
                    task_dict['completed_at'] = task.completed_at.isoformat()
                task_dicts.append(task_dict)
            
            return json.dumps(task_dicts, indent=2, ensure_ascii=False)
        
        return str(tasks)


class PluginManager:
    """插件管理器"""
    
    def __init__(self):
        self._plugins: Dict[str, PluginInterface] = {}
        self._enabled_plugins: set = set()
    
    def register_plugin(self, plugin: PluginInterface) -> None:
        """注册插件"""
        self._plugins[plugin.name] = plugin
    
    def enable_plugin(self, plugin_name: str, config: Optional[Dict[str, Any]] = None) -> bool:
        """启用插件"""
        if plugin_name in self._plugins:
            plugin = self._plugins[plugin_name]
            plugin.initialize(config or {})
            self._enabled_plugins.add(plugin_name)
            return True
        return False
    
    def execute_plugin(self, plugin_name: str, context: Dict[str, Any]) -> Any:
        """执行插件"""
        if plugin_name in self._enabled_plugins:
            plugin = self._plugins[plugin_name]
            return plugin.execute(context)
        raise ValueError(f"Plugin {plugin_name} not enabled")


# ============================================================================
# 7. 配置系统
# ============================================================================

class AppConfig:
    """应用配置"""
    
    def __init__(self):
        self.debug = True
        self.database_url = "sqlite:///tasks.db"
        self.email_enabled = True
        self.metrics_enabled = True
        self.audit_enabled = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'debug': self.debug,
            'database_url': self.database_url,
            'email_enabled': self.email_enabled,
            'metrics_enabled': self.metrics_enabled,
            'audit_enabled': self.audit_enabled
        }


# ============================================================================
# 8. 应用程序组装
# ============================================================================

def configure_container() -> DIContainer:
    """配置依赖注入容器"""
    container = DIContainer()
    
    # 注册仓储
    container.register(TaskRepositoryInterface, InMemoryTaskRepository)
    
    # 注册配置
    container.register_instance(AppConfig, AppConfig())
    
    return container


def configure_event_system(config: AppConfig) -> EventBus:
    """配置事件系统"""
    event_bus = EventBus()
    
    # 注册事件处理器
    if config.email_enabled:
        event_bus.subscribe('task.created', EmailNotificationHandler())
        event_bus.subscribe('task.completed', EmailNotificationHandler())
    
    if config.metrics_enabled:
        metrics_handler = MetricsHandler()
        event_bus.subscribe('task.created', metrics_handler)
        event_bus.subscribe('task.completed', metrics_handler)
    
    if config.audit_enabled:
        audit_handler = AuditLogHandler()
        event_bus.subscribe('task.created', audit_handler)
        event_bus.subscribe('task.completed', audit_handler)
    
    return event_bus


def configure_plugins() -> PluginManager:
    """配置插件系统"""
    plugin_manager = PluginManager()
    
    # 注册插件
    export_plugin = TaskExportPlugin()
    plugin_manager.register_plugin(export_plugin)
    
    # 启用插件
    plugin_manager.enable_plugin('task_export', {'format': 'json'})
    
    return plugin_manager


# ============================================================================
# 9. 主演示程序
# ============================================================================

def main():
    """主函数：演示模块化开发实践"""
    print("Session28: 模块化开发实践演示")
    print("=" * 50)
    
    # 1. 配置系统
    print("\n1. 系统配置:")
    config = AppConfig()
    print(f"✓ 配置加载完成: {config.to_dict()}")
    
    # 2. 依赖注入容器
    print("\n2. 依赖注入容器演示:")
    container = configure_container()
    print("✓ 容器配置完成")
    
    # 解析服务
    task_repository = container.resolve(TaskRepositoryInterface)
    print("✓ 任务仓储解析成功")
    
    # 3. 事件系统
    print("\n3. 事件系统配置:")
    event_bus = configure_event_system(config)
    print("✓ 事件总线配置完成")
    
    # 4. 创建任务服务
    task_service = TaskService(task_repository, event_bus)
    print("✓ 任务服务创建完成")
    
    # 5. 演示任务操作
    print("\n4. 任务操作演示:")
    
    # 创建任务
    task1 = task_service.create_task(
        user_id="user123",
        title="学习模块化开发",
        description="完成Session28的学习和实践"
    )
    print(f"✓ 任务创建成功: {task1.title} (ID: {task1.id[:8]}...)")
    
    # 创建更多任务
    task2 = task_service.create_task(
        user_id="user123",
        title="编写测试代码",
        description="为模块化系统编写单元测试"
    )
    print(f"✓ 任务创建成功: {task2.title} (ID: {task2.id[:8]}...)")
    
    # 完成任务
    print("\n5. 完成任务演示:")
    success = task_service.complete_task(task1.id)
    if success:
        print(f"✓ 任务完成: {task1.title}")
    
    # 6. 插件系统演示
    print("\n6. 插件系统演示:")
    plugin_manager = configure_plugins()
    print("✓ 插件管理器配置完成")
    
    # 获取用户任务并导出
    user_tasks = task_service.get_user_tasks("user123")
    export_result = plugin_manager.execute_plugin('task_export', {
        'tasks': user_tasks
    })
    
    print("✓ 任务导出完成 (JSON格式):")
    print("导出内容预览:")
    # 只显示前200个字符
    preview = export_result[:200] + "..." if len(export_result) > 200 else export_result
    print(preview)
    
    # 7. 系统统计
    print("\n7. 系统统计:")
    all_tasks = task_service.get_user_tasks("user123")
    completed_tasks = [t for t in all_tasks if t.completed]
    pending_tasks = [t for t in all_tasks if not t.completed]
    
    print(f"📊 总任务数: {len(all_tasks)}")
    print(f"📊 已完成: {len(completed_tasks)}")
    print(f"📊 待完成: {len(pending_tasks)}")
    
    print("\n演示完成！")
    print("\n💡 关键特性展示:")
    print("   ✓ 依赖注入 - 松耦合的模块设计")
    print("   ✓ 事件驱动 - 异步解耦的通信机制")
    print("   ✓ 插件系统 - 可扩展的功能架构")
    print("   ✓ 配置管理 - 灵活的系统配置")
    print("   ✓ 接口设计 - 面向抽象的编程")


if __name__ == "__main__":
    main()