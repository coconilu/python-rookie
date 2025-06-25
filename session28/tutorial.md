# Session28: 模块化开发实践教程

## 1. 模块化开发概述

### 1.1 什么是模块化开发

模块化开发是一种软件设计方法，将复杂的系统分解为独立、可重用的模块。每个模块负责特定的功能，模块之间通过明确定义的接口进行通信。

**模块化的核心原则：**
- **单一职责原则**：每个模块只负责一个功能领域
- **高内聚低耦合**：模块内部紧密相关，模块间依赖最小
- **接口隔离**：通过接口而非实现进行交互
- **依赖倒置**：依赖抽象而非具体实现

### 1.2 模块化的优势

```python
# 传统单体架构的问题
class MonolithicTaskManager:
    def __init__(self):
        # 所有功能混在一起
        self.database_connection = None
        self.email_service = None
        self.notification_service = None
        self.user_auth = None
        self.task_logic = None
        # ... 更多功能
    
    def create_task(self, user_id, task_data):
        # 用户验证、数据库操作、通知发送都混在一起
        if not self.authenticate_user(user_id):
            return False
        
        task_id = self.save_to_database(task_data)
        self.send_notification(user_id, task_id)
        self.send_email(user_id, task_data)
        return task_id
```

**模块化架构的优势：**
- **可维护性**：修改一个模块不影响其他模块
- **可测试性**：每个模块可以独立测试
- **可重用性**：模块可以在不同项目中重用
- **团队协作**：不同团队可以并行开发不同模块
- **可扩展性**：容易添加新功能模块

## 2. 模块化设计原则

### 2.1 包结构设计

良好的包结构是模块化的基础：

```
task_manager/
├── __init__.py
├── core/                    # 核心业务逻辑
│   ├── __init__.py
│   ├── entities/           # 实体类
│   │   ├── __init__.py
│   │   ├── task.py
│   │   └── user.py
│   ├── interfaces/         # 接口定义
│   │   ├── __init__.py
│   │   ├── repository.py
│   │   └── service.py
│   └── services/           # 业务服务
│       ├── __init__.py
│       ├── task_service.py
│       └── user_service.py
├── infrastructure/          # 基础设施层
│   ├── __init__.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── repositories.py
│   ├── external/           # 外部服务
│   │   ├── __init__.py
│   │   ├── email_service.py
│   │   └── notification_service.py
│   └── config/
│       ├── __init__.py
│       └── settings.py
├── application/            # 应用层
│   ├── __init__.py
│   ├── handlers/          # 命令处理器
│   │   ├── __init__.py
│   │   └── task_handlers.py
│   └── dto/               # 数据传输对象
│       ├── __init__.py
│       └── task_dto.py
├── presentation/           # 表现层
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── task_api.py
│   └── cli/
│       ├── __init__.py
│       └── task_cli.py
└── shared/                 # 共享组件
    ├── __init__.py
    ├── events/
    │   ├── __init__.py
    │   └── event_bus.py
    ├── exceptions/
    │   ├── __init__.py
    │   └── custom_exceptions.py
    └── utils/
        ├── __init__.py
        └── helpers.py
```

### 2.2 依赖注入模式

依赖注入是模块化的核心模式，它让模块不直接创建依赖，而是从外部注入：

```python
# core/interfaces/repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.task import Task

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
    
    @abstractmethod
    def delete(self, task_id: str) -> bool:
        """删除任务"""
        pass

# core/services/task_service.py
from typing import List, Optional
from ..interfaces.repository import TaskRepositoryInterface
from ..entities.task import Task

class TaskService:
    """任务服务 - 依赖注入仓储接口"""
    
    def __init__(self, task_repository: TaskRepositoryInterface):
        self._task_repository = task_repository
    
    def create_task(self, user_id: str, title: str, description: str) -> Task:
        """创建任务"""
        task = Task(
            user_id=user_id,
            title=title,
            description=description
        )
        return self._task_repository.save(task)
    
    def get_user_tasks(self, user_id: str) -> List[Task]:
        """获取用户任务列表"""
        return self._task_repository.find_by_user_id(user_id)
    
    def complete_task(self, task_id: str) -> bool:
        """完成任务"""
        task = self._task_repository.find_by_id(task_id)
        if task:
            task.mark_completed()
            self._task_repository.save(task)
            return True
        return False
```

### 2.3 配置管理系统

模块化系统需要灵活的配置管理：

```python
# infrastructure/config/settings.py
import os
from typing import Dict, Any
from dataclasses import dataclass
from enum import Enum

class Environment(Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"

@dataclass
class DatabaseConfig:
    """数据库配置"""
    host: str
    port: int
    database: str
    username: str
    password: str
    
    @classmethod
    def from_env(cls) -> 'DatabaseConfig':
        return cls(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', '5432')),
            database=os.getenv('DB_NAME', 'task_manager'),
            username=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', '')
        )

@dataclass
class EmailConfig:
    """邮件配置"""
    smtp_host: str
    smtp_port: int
    username: str
    password: str
    use_tls: bool
    
    @classmethod
    def from_env(cls) -> 'EmailConfig':
        return cls(
            smtp_host=os.getenv('SMTP_HOST', 'localhost'),
            smtp_port=int(os.getenv('SMTP_PORT', '587')),
            username=os.getenv('SMTP_USER', ''),
            password=os.getenv('SMTP_PASSWORD', ''),
            use_tls=os.getenv('SMTP_USE_TLS', 'true').lower() == 'true'
        )

class Settings:
    """应用配置管理器"""
    
    def __init__(self):
        self.environment = Environment(os.getenv('ENVIRONMENT', 'development'))
        self.debug = os.getenv('DEBUG', 'false').lower() == 'true'
        self.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')
        
        # 模块配置
        self.database = DatabaseConfig.from_env()
        self.email = EmailConfig.from_env()
    
    def get_config_dict(self) -> Dict[str, Any]:
        """获取配置字典"""
        return {
            'environment': self.environment.value,
            'debug': self.debug,
            'database': self.database.__dict__,
            'email': self.email.__dict__
        }

# 全局配置实例
settings = Settings()
```

## 3. 依赖注入容器

### 3.1 简单的DI容器实现

```python
# shared/container.py
from typing import Dict, Type, Any, Callable, TypeVar, Optional
from functools import wraps
import inspect

T = TypeVar('T')

class DIContainer:
    """依赖注入容器"""
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Callable] = {}
        self._singletons: Dict[str, Any] = {}
    
    def register(self, interface: Type[T], implementation: Type[T], 
                singleton: bool = True) -> None:
        """注册服务"""
        key = self._get_key(interface)
        
        if singleton:
            self._singletons[key] = implementation
        else:
            self._factories[key] = implementation
    
    def register_instance(self, interface: Type[T], instance: T) -> None:
        """注册实例"""
        key = self._get_key(interface)
        self._services[key] = instance
    
    def register_factory(self, interface: Type[T], 
                        factory: Callable[[], T]) -> None:
        """注册工厂函数"""
        key = self._get_key(interface)
        self._factories[key] = factory
    
    def resolve(self, interface: Type[T]) -> T:
        """解析服务"""
        key = self._get_key(interface)
        
        # 检查已注册的实例
        if key in self._services:
            return self._services[key]
        
        # 检查单例
        if key in self._singletons:
            if key not in self._services:
                implementation = self._singletons[key]
                instance = self._create_instance(implementation)
                self._services[key] = instance
            return self._services[key]
        
        # 检查工厂
        if key in self._factories:
            factory = self._factories[key]
            if callable(factory) and not inspect.isclass(factory):
                return factory()
            else:
                return self._create_instance(factory)
        
        raise ValueError(f"Service {interface} not registered")
    
    def _create_instance(self, cls: Type[T]) -> T:
        """创建实例并自动注入依赖"""
        # 获取构造函数参数
        sig = inspect.signature(cls.__init__)
        kwargs = {}
        
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            
            if param.annotation != inspect.Parameter.empty:
                # 递归解析依赖
                kwargs[param_name] = self.resolve(param.annotation)
        
        return cls(**kwargs)
    
    def _get_key(self, interface: Type) -> str:
        """获取服务键"""
        return f"{interface.__module__}.{interface.__name__}"

# 装饰器支持
def injectable(container: DIContainer):
    """可注入装饰器"""
    def decorator(cls):
        @wraps(cls)
        def wrapper(*args, **kwargs):
            if not args and not kwargs:
                # 无参数调用，使用容器解析
                return container.resolve(cls)
            else:
                # 有参数调用，直接创建
                return cls(*args, **kwargs)
        return wrapper
    return decorator
```

### 3.2 使用DI容器

```python
# 配置容器
from shared.container import DIContainer
from core.interfaces.repository import TaskRepositoryInterface
from infrastructure.database.repositories import SqliteTaskRepository
from core.services.task_service import TaskService

def configure_container() -> DIContainer:
    """配置依赖注入容器"""
    container = DIContainer()
    
    # 注册仓储实现
    container.register(TaskRepositoryInterface, SqliteTaskRepository)
    
    # 注册服务
    container.register(TaskService, TaskService)
    
    return container

# 使用示例
container = configure_container()
task_service = container.resolve(TaskService)

# 创建任务
task = task_service.create_task(
    user_id="user123",
    title="学习模块化开发",
    description="完成Session28的学习"
)
```

## 4. 事件驱动架构

### 4.1 事件系统设计

```python
# shared/events/event_bus.py
from typing import Dict, List, Callable, Any
from dataclasses import dataclass
from datetime import datetime
import uuid
import asyncio
from abc import ABC, abstractmethod

@dataclass
class Event:
    """基础事件类"""
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
        self._middleware: List[Callable[[Event], Event]] = []
    
    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        """订阅事件"""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
    
    def add_middleware(self, middleware: Callable[[Event], Event]) -> None:
        """添加中间件"""
        self._middleware.append(middleware)
    
    async def publish(self, event: Event) -> None:
        """发布事件"""
        # 应用中间件
        for middleware in self._middleware:
            event = middleware(event)
        
        # 获取处理器
        handlers = self._handlers.get(event.event_type, [])
        
        # 并发处理事件
        if handlers:
            tasks = [handler.handle(event) for handler in handlers]
            await asyncio.gather(*tasks, return_exceptions=True)
    
    def publish_sync(self, event: Event) -> None:
        """同步发布事件"""
        asyncio.run(self.publish(event))

# 具体事件类型
class TaskCreatedEvent(Event):
    """任务创建事件"""
    
    def __init__(self, task_id: str, user_id: str, title: str):
        super().__init__('task.created', {
            'task_id': task_id,
            'user_id': user_id,
            'title': title
        })

class TaskCompletedEvent(Event):
    """任务完成事件"""
    
    def __init__(self, task_id: str, user_id: str, completed_at: datetime):
        super().__init__('task.completed', {
            'task_id': task_id,
            'user_id': user_id,
            'completed_at': completed_at.isoformat()
        })
```

### 4.2 事件处理器实现

```python
# application/handlers/event_handlers.py
from shared.events.event_bus import Event, EventHandler
from infrastructure.external.email_service import EmailService
from infrastructure.external.notification_service import NotificationService
import logging

logger = logging.getLogger(__name__)

class EmailNotificationHandler(EventHandler):
    """邮件通知处理器"""
    
    def __init__(self, email_service: EmailService):
        self.email_service = email_service
    
    async def handle(self, event: Event) -> None:
        """处理邮件通知"""
        try:
            if event.event_type == 'task.created':
                await self._handle_task_created(event)
            elif event.event_type == 'task.completed':
                await self._handle_task_completed(event)
        except Exception as e:
            logger.error(f"邮件通知处理失败: {e}")
    
    async def _handle_task_created(self, event: Event) -> None:
        """处理任务创建通知"""
        data = event.data
        await self.email_service.send_email(
            to=f"user_{data['user_id']}@example.com",
            subject="新任务创建",
            body=f"您的任务 '{data['title']}' 已创建成功"
        )
    
    async def _handle_task_completed(self, event: Event) -> None:
        """处理任务完成通知"""
        data = event.data
        await self.email_service.send_email(
            to=f"user_{data['user_id']}@example.com",
            subject="任务完成",
            body=f"恭喜！您已完成任务 {data['task_id']}"
        )

class AuditLogHandler(EventHandler):
    """审计日志处理器"""
    
    async def handle(self, event: Event) -> None:
        """记录审计日志"""
        logger.info(f"审计日志: {event.event_type} - {event.data}")

class MetricsHandler(EventHandler):
    """指标统计处理器"""
    
    def __init__(self):
        self.task_created_count = 0
        self.task_completed_count = 0
    
    async def handle(self, event: Event) -> None:
        """更新指标"""
        if event.event_type == 'task.created':
            self.task_created_count += 1
        elif event.event_type == 'task.completed':
            self.task_completed_count += 1
        
        logger.info(f"指标更新: 创建 {self.task_created_count}, 完成 {self.task_completed_count}")
```

## 5. 插件系统架构

### 5.1 插件接口设计

```python
# shared/plugins/plugin_interface.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class PluginInterface(ABC):
    """插件接口"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """插件名称"""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """插件版本"""
        pass
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """初始化插件"""
        pass
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Any:
        """执行插件功能"""
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """清理资源"""
        pass

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
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """禁用插件"""
        if plugin_name in self._enabled_plugins:
            plugin = self._plugins[plugin_name]
            plugin.cleanup()
            self._enabled_plugins.remove(plugin_name)
            return True
        return False
    
    def execute_plugin(self, plugin_name: str, context: Dict[str, Any]) -> Any:
        """执行插件"""
        if plugin_name in self._enabled_plugins:
            plugin = self._plugins[plugin_name]
            return plugin.execute(context)
        raise ValueError(f"Plugin {plugin_name} not enabled")
    
    def get_enabled_plugins(self) -> List[str]:
        """获取已启用的插件列表"""
        return list(self._enabled_plugins)
```

### 5.2 示例插件实现

```python
# plugins/export_plugin.py
from shared.plugins.plugin_interface import PluginInterface
from typing import Dict, Any
import json
import csv
from io import StringIO

class TaskExportPlugin(PluginInterface):
    """任务导出插件"""
    
    @property
    def name(self) -> str:
        return "task_export"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """初始化插件"""
        self.export_format = config.get('format', 'json')
        self.include_completed = config.get('include_completed', True)
    
    def execute(self, context: Dict[str, Any]) -> Any:
        """执行导出功能"""
        tasks = context.get('tasks', [])
        
        # 过滤任务
        if not self.include_completed:
            tasks = [task for task in tasks if not task.get('completed', False)]
        
        # 根据格式导出
        if self.export_format == 'json':
            return self._export_json(tasks)
        elif self.export_format == 'csv':
            return self._export_csv(tasks)
        else:
            raise ValueError(f"Unsupported format: {self.export_format}")
    
    def cleanup(self) -> None:
        """清理资源"""
        pass
    
    def _export_json(self, tasks: list) -> str:
        """导出为JSON格式"""
        return json.dumps(tasks, indent=2, ensure_ascii=False)
    
    def _export_csv(self, tasks: list) -> str:
        """导出为CSV格式"""
        if not tasks:
            return ""
        
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=tasks[0].keys())
        writer.writeheader()
        writer.writerows(tasks)
        return output.getvalue()

# plugins/notification_plugin.py
class SlackNotificationPlugin(PluginInterface):
    """Slack通知插件"""
    
    @property
    def name(self) -> str:
        return "slack_notification"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """初始化插件"""
        self.webhook_url = config.get('webhook_url')
        self.channel = config.get('channel', '#general')
    
    def execute(self, context: Dict[str, Any]) -> Any:
        """发送Slack通知"""
        message = context.get('message', '')
        # 这里应该实现实际的Slack API调用
        print(f"发送Slack消息到 {self.channel}: {message}")
        return True
    
    def cleanup(self) -> None:
        """清理资源"""
        pass
```

## 6. 模块间通信

### 6.1 消息队列模式

```python
# shared/messaging/message_queue.py
from typing import Dict, Any, Callable, Optional
from dataclasses import dataclass
from queue import Queue, Empty
from threading import Thread, Event
import time
import logging

logger = logging.getLogger(__name__)

@dataclass
class Message:
    """消息类"""
    topic: str
    payload: Dict[str, Any]
    timestamp: float
    message_id: str
    
    def __init__(self, topic: str, payload: Dict[str, Any]):
        self.topic = topic
        self.payload = payload
        self.timestamp = time.time()
        self.message_id = f"{topic}_{int(self.timestamp * 1000)}"

class MessageQueue:
    """简单的消息队列实现"""
    
    def __init__(self, max_size: int = 1000):
        self._queue = Queue(maxsize=max_size)
        self._subscribers: Dict[str, List[Callable[[Message], None]]] = {}
        self._running = False
        self._worker_thread: Optional[Thread] = None
        self._stop_event = Event()
    
    def start(self) -> None:
        """启动消息队列"""
        if not self._running:
            self._running = True
            self._stop_event.clear()
            self._worker_thread = Thread(target=self._process_messages)
            self._worker_thread.start()
            logger.info("消息队列已启动")
    
    def stop(self) -> None:
        """停止消息队列"""
        if self._running:
            self._running = False
            self._stop_event.set()
            if self._worker_thread:
                self._worker_thread.join()
            logger.info("消息队列已停止")
    
    def publish(self, topic: str, payload: Dict[str, Any]) -> bool:
        """发布消息"""
        try:
            message = Message(topic, payload)
            self._queue.put_nowait(message)
            return True
        except Exception as e:
            logger.error(f"发布消息失败: {e}")
            return False
    
    def subscribe(self, topic: str, handler: Callable[[Message], None]) -> None:
        """订阅主题"""
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        self._subscribers[topic].append(handler)
        logger.info(f"订阅主题: {topic}")
    
    def _process_messages(self) -> None:
        """处理消息的工作线程"""
        while self._running:
            try:
                # 等待消息，超时检查停止信号
                message = self._queue.get(timeout=1.0)
                self._deliver_message(message)
                self._queue.task_done()
            except Empty:
                # 超时，检查是否需要停止
                if self._stop_event.is_set():
                    break
            except Exception as e:
                logger.error(f"处理消息时出错: {e}")
    
    def _deliver_message(self, message: Message) -> None:
        """投递消息给订阅者"""
        handlers = self._subscribers.get(message.topic, [])
        for handler in handlers:
            try:
                handler(message)
            except Exception as e:
                logger.error(f"消息处理器执行失败: {e}")
```

### 6.2 使用消息队列进行模块通信

```python
# 在任务服务中发布消息
class TaskService:
    def __init__(self, task_repository: TaskRepositoryInterface, 
                 message_queue: MessageQueue):
        self._task_repository = task_repository
        self._message_queue = message_queue
    
    def create_task(self, user_id: str, title: str, description: str) -> Task:
        """创建任务"""
        task = Task(user_id=user_id, title=title, description=description)
        saved_task = self._task_repository.save(task)
        
        # 发布任务创建消息
        self._message_queue.publish('task.created', {
            'task_id': saved_task.id,
            'user_id': saved_task.user_id,
            'title': saved_task.title
        })
        
        return saved_task

# 邮件服务订阅消息
class EmailService:
    def __init__(self, message_queue: MessageQueue):
        self._message_queue = message_queue
        # 订阅任务相关消息
        self._message_queue.subscribe('task.created', self._handle_task_created)
        self._message_queue.subscribe('task.completed', self._handle_task_completed)
    
    def _handle_task_created(self, message: Message) -> None:
        """处理任务创建消息"""
        payload = message.payload
        print(f"发送邮件: 任务 '{payload['title']}' 已创建")
    
    def _handle_task_completed(self, message: Message) -> None:
        """处理任务完成消息"""
        payload = message.payload
        print(f"发送邮件: 任务 {payload['task_id']} 已完成")
```

## 7. 实践总结

### 7.1 模块化开发最佳实践

1. **明确模块边界**：每个模块应该有清晰的职责和边界
2. **使用接口编程**：依赖抽象而非具体实现
3. **配置外部化**：将配置从代码中分离
4. **事件驱动解耦**：使用事件系统减少模块间直接依赖
5. **插件化扩展**：通过插件系统支持功能扩展
6. **统一错误处理**：建立统一的错误处理机制
7. **完善的测试**：每个模块都应该有独立的测试

### 7.2 常见陷阱和解决方案

**陷阱1：过度设计**
- 问题：为了模块化而模块化，增加不必要的复杂性
- 解决：从简单开始，根据需要逐步重构

**陷阱2：循环依赖**
- 问题：模块A依赖模块B，模块B又依赖模块A
- 解决：引入中介模块或使用事件系统解耦

**陷阱3：配置管理混乱**
- 问题：配置散落在各个模块中，难以管理
- 解决：建立统一的配置管理系统

**陷阱4：测试困难**
- 问题：模块间依赖复杂，难以进行单元测试
- 解决：使用依赖注入和模拟对象

### 7.3 性能考虑

1. **延迟加载**：只在需要时加载模块
2. **缓存机制**：缓存频繁访问的数据
3. **异步处理**：使用异步模式处理耗时操作
4. **资源池化**：复用昂贵的资源（如数据库连接）

## 8. 运行结果展示

当你运行演示代码时，你会看到类似以下的输出：

```
模块化任务管理系统演示
========================================

1. 依赖注入容器演示:
✓ 任务仓储已注册
✓ 任务服务已注册
✓ 服务解析成功

2. 创建任务:
✓ 任务创建成功: 学习模块化开发 (ID: task_001)
✓ 事件已发布: task.created

3. 事件处理结果:
📧 邮件通知: 您的任务 '学习模块化开发' 已创建成功
📊 指标更新: 创建任务数 +1
📝 审计日志: task.created 事件已记录

4. 插件系统演示:
✓ 导出插件已启用
✓ 任务导出完成 (JSON格式)

5. 消息队列演示:
✓ 消息队列已启动
📨 消息发布: task.status_changed
📨 消息处理: 任务状态已更新

演示完成！
```

这个输出展示了模块化系统的各个组件如何协同工作，包括依赖注入、事件处理、插件系统和消息队列等核心功能。

## 9. 扩展阅读

- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Dependency Injection in Python](https://python-dependency-injector.ets-labs.org/)
- [Event-Driven Architecture](https://martinfowler.com/articles/201701-event-driven.html)
- [Plugin Architecture](https://www.oreilly.com/library/view/software-architecture-patterns/9781491971437/ch05.html)

通过本课程的学习，你已经掌握了模块化开发的核心概念和实践技巧。这些技能将帮助你构建更加灵活、可维护和可扩展的Python应用程序。