#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session28 示例4：模块间通信详解

本示例展示了不同的模块间通信模式和实现方式。

作者: Python教程团队
创建日期: 2024-01-15
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import asyncio
import json
import queue
import threading
import time
import uuid
from collections import defaultdict


# ============================================================================
# 1. 消息基础设施
# ============================================================================

class MessageType(Enum):
    """消息类型"""
    COMMAND = "command"
    EVENT = "event"
    QUERY = "query"
    RESPONSE = "response"
    NOTIFICATION = "notification"


class MessagePriority(Enum):
    """消息优先级"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Message:
    """消息类"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: MessageType = MessageType.COMMAND
    priority: MessagePriority = MessagePriority.NORMAL
    sender: str = ""
    receiver: str = ""
    topic: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    correlation_id: Optional[str] = None
    reply_to: Optional[str] = None
    ttl: Optional[int] = None  # 生存时间（秒）
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'type': self.type.value,
            'priority': self.priority.value,
            'sender': self.sender,
            'receiver': self.receiver,
            'topic': self.topic,
            'payload': self.payload,
            'timestamp': self.timestamp.isoformat(),
            'correlation_id': self.correlation_id,
            'reply_to': self.reply_to,
            'ttl': self.ttl
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """从字典创建消息"""
        return cls(
            id=data['id'],
            type=MessageType(data['type']),
            priority=MessagePriority(data['priority']),
            sender=data['sender'],
            receiver=data['receiver'],
            topic=data['topic'],
            payload=data['payload'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            correlation_id=data.get('correlation_id'),
            reply_to=data.get('reply_to'),
            ttl=data.get('ttl')
        )
    
    def is_expired(self) -> bool:
        """检查消息是否过期"""
        if self.ttl is None:
            return False
        elapsed = (datetime.now() - self.timestamp).total_seconds()
        return elapsed > self.ttl


class MessageHandler(ABC):
    """消息处理器接口"""
    
    @abstractmethod
    def handle_message(self, message: Message) -> Optional[Message]:
        """处理消息，可选返回响应消息"""
        pass
    
    @abstractmethod
    def can_handle(self, message: Message) -> bool:
        """判断是否能处理该消息"""
        pass


# ============================================================================
# 2. 消息总线实现
# ============================================================================

class MessageBus:
    """消息总线"""
    
    def __init__(self):
        self.handlers: Dict[str, List[MessageHandler]] = defaultdict(list)
        self.topic_handlers: Dict[str, List[MessageHandler]] = defaultdict(list)
        self.global_handlers: List[MessageHandler] = []
        self.message_queue = queue.PriorityQueue()
        self.response_handlers: Dict[str, Callable] = {}
        self.running = False
        self.worker_thread: Optional[threading.Thread] = None
        self.message_history: List[Message] = []
        self.middleware: List[Callable[[Message], Message]] = []
    
    def start(self) -> None:
        """启动消息总线"""
        if not self.running:
            self.running = True
            self.worker_thread = threading.Thread(target=self._process_messages, daemon=True)
            self.worker_thread.start()
            print("🚀 消息总线已启动")
    
    def stop(self) -> None:
        """停止消息总线"""
        if self.running:
            self.running = False
            if self.worker_thread:
                self.worker_thread.join(timeout=1)
            print("🛑 消息总线已停止")
    
    def register_handler(self, receiver: str, handler: MessageHandler) -> None:
        """注册消息处理器"""
        self.handlers[receiver].append(handler)
        print(f"📝 注册处理器: {receiver} -> {handler.__class__.__name__}")
    
    def register_topic_handler(self, topic: str, handler: MessageHandler) -> None:
        """注册主题处理器"""
        self.topic_handlers[topic].append(handler)
        print(f"📝 注册主题处理器: {topic} -> {handler.__class__.__name__}")
    
    def register_global_handler(self, handler: MessageHandler) -> None:
        """注册全局处理器"""
        self.global_handlers.append(handler)
        print(f"📝 注册全局处理器: {handler.__class__.__name__}")
    
    def add_middleware(self, middleware: Callable[[Message], Message]) -> None:
        """添加中间件"""
        self.middleware.append(middleware)
    
    def send_message(self, message: Message) -> None:
        """发送消息"""
        # 应用中间件
        for middleware in self.middleware:
            message = middleware(message)
        
        # 检查消息是否过期
        if message.is_expired():
            print(f"⏰ 消息已过期: {message.id}")
            return
        
        # 添加到优先级队列
        priority = -message.priority.value  # 负数使高优先级排在前面
        self.message_queue.put((priority, time.time(), message))
        
        print(f"📤 发送消息: {message.type.value} from {message.sender} to {message.receiver}")
    
    def send_command(self, sender: str, receiver: str, command: str, 
                    payload: Dict[str, Any] = None, priority: MessagePriority = MessagePriority.NORMAL) -> str:
        """发送命令消息"""
        message = Message(
            type=MessageType.COMMAND,
            priority=priority,
            sender=sender,
            receiver=receiver,
            topic=command,
            payload=payload or {}
        )
        self.send_message(message)
        return message.id
    
    def send_event(self, sender: str, topic: str, payload: Dict[str, Any] = None) -> str:
        """发送事件消息"""
        message = Message(
            type=MessageType.EVENT,
            sender=sender,
            topic=topic,
            payload=payload or {}
        )
        self.send_message(message)
        return message.id
    
    def send_query(self, sender: str, receiver: str, query: str, 
                  payload: Dict[str, Any] = None, timeout: int = 30) -> str:
        """发送查询消息"""
        message = Message(
            type=MessageType.QUERY,
            sender=sender,
            receiver=receiver,
            topic=query,
            payload=payload or {},
            reply_to=sender,
            ttl=timeout
        )
        self.send_message(message)
        return message.id
    
    def send_response(self, original_message: Message, payload: Dict[str, Any] = None) -> str:
        """发送响应消息"""
        if not original_message.reply_to:
            raise ValueError("原消息没有指定回复地址")
        
        response = Message(
            type=MessageType.RESPONSE,
            sender=original_message.receiver,
            receiver=original_message.reply_to,
            topic=f"response.{original_message.topic}",
            payload=payload or {},
            correlation_id=original_message.id
        )
        self.send_message(response)
        return response.id
    
    def wait_for_response(self, message_id: str, timeout: int = 30) -> Optional[Message]:
        """等待响应消息"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            # 检查消息历史中是否有对应的响应
            for msg in reversed(self.message_history):
                if (msg.type == MessageType.RESPONSE and 
                    msg.correlation_id == message_id):
                    return msg
            time.sleep(0.1)
        return None
    
    def _process_messages(self) -> None:
        """处理消息的工作线程"""
        while self.running:
            try:
                # 获取消息（阻塞等待）
                priority, timestamp, message = self.message_queue.get(timeout=1)
                
                # 检查消息是否过期
                if message.is_expired():
                    print(f"⏰ 处理时消息已过期: {message.id}")
                    continue
                
                # 记录消息历史
                self.message_history.append(message)
                
                # 处理消息
                self._handle_message(message)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ 处理消息时发生错误: {str(e)}")
    
    def _handle_message(self, message: Message) -> None:
        """处理单个消息"""
        print(f"📥 处理消息: {message.type.value} - {message.topic}")
        
        handled = False
        
        # 1. 尝试特定接收者的处理器
        if message.receiver in self.handlers:
            for handler in self.handlers[message.receiver]:
                if handler.can_handle(message):
                    try:
                        response = handler.handle_message(message)
                        if response:
                            self.send_message(response)
                        handled = True
                    except Exception as e:
                        print(f"❌ 处理器错误: {handler.__class__.__name__} - {str(e)}")
        
        # 2. 尝试主题处理器
        if message.topic in self.topic_handlers:
            for handler in self.topic_handlers[message.topic]:
                if handler.can_handle(message):
                    try:
                        response = handler.handle_message(message)
                        if response:
                            self.send_message(response)
                        handled = True
                    except Exception as e:
                        print(f"❌ 主题处理器错误: {handler.__class__.__name__} - {str(e)}")
        
        # 3. 尝试全局处理器
        for handler in self.global_handlers:
            if handler.can_handle(message):
                try:
                    response = handler.handle_message(message)
                    if response:
                        self.send_message(response)
                    handled = True
                except Exception as e:
                    print(f"❌ 全局处理器错误: {handler.__class__.__name__} - {str(e)}")
        
        if not handled:
            print(f"⚠️ 未找到消息处理器: {message.receiver} - {message.topic}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        message_types = defaultdict(int)
        for msg in self.message_history:
            message_types[msg.type.value] += 1
        
        return {
            'total_messages': len(self.message_history),
            'queue_size': self.message_queue.qsize(),
            'message_types': dict(message_types),
            'handlers_count': sum(len(handlers) for handlers in self.handlers.values()),
            'topic_handlers_count': sum(len(handlers) for handlers in self.topic_handlers.values()),
            'global_handlers_count': len(self.global_handlers)
        }


# ============================================================================
# 3. 异步消息总线
# ============================================================================

class AsyncMessageBus:
    """异步消息总线"""
    
    def __init__(self):
        self.handlers: Dict[str, List[MessageHandler]] = defaultdict(list)
        self.topic_handlers: Dict[str, List[MessageHandler]] = defaultdict(list)
        self.global_handlers: List[MessageHandler] = []
        self.message_queue = asyncio.Queue()
        self.running = False
        self.worker_task: Optional[asyncio.Task] = None
        self.message_history: List[Message] = []
    
    async def start(self) -> None:
        """启动异步消息总线"""
        if not self.running:
            self.running = True
            self.worker_task = asyncio.create_task(self._process_messages())
            print("🚀 异步消息总线已启动")
    
    async def stop(self) -> None:
        """停止异步消息总线"""
        if self.running:
            self.running = False
            if self.worker_task:
                self.worker_task.cancel()
                try:
                    await self.worker_task
                except asyncio.CancelledError:
                    pass
            print("🛑 异步消息总线已停止")
    
    def register_handler(self, receiver: str, handler: MessageHandler) -> None:
        """注册消息处理器"""
        self.handlers[receiver].append(handler)
        print(f"📝 注册异步处理器: {receiver} -> {handler.__class__.__name__}")
    
    async def send_message(self, message: Message) -> None:
        """发送消息"""
        await self.message_queue.put(message)
        print(f"📤 异步发送消息: {message.type.value} from {message.sender} to {message.receiver}")
    
    async def _process_messages(self) -> None:
        """异步处理消息"""
        while self.running:
            try:
                message = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
                self.message_history.append(message)
                await self._handle_message(message)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"❌ 异步处理消息时发生错误: {str(e)}")
    
    async def _handle_message(self, message: Message) -> None:
        """异步处理单个消息"""
        print(f"📥 异步处理消息: {message.type.value} - {message.topic}")
        
        # 收集所有可以处理该消息的处理器
        tasks = []
        
        # 特定接收者的处理器
        if message.receiver in self.handlers:
            for handler in self.handlers[message.receiver]:
                if handler.can_handle(message):
                    tasks.append(self._handle_with_handler(handler, message))
        
        # 主题处理器
        if message.topic in self.topic_handlers:
            for handler in self.topic_handlers[message.topic]:
                if handler.can_handle(message):
                    tasks.append(self._handle_with_handler(handler, message))
        
        # 全局处理器
        for handler in self.global_handlers:
            if handler.can_handle(message):
                tasks.append(self._handle_with_handler(handler, message))
        
        # 并发执行所有处理器
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _handle_with_handler(self, handler: MessageHandler, message: Message) -> None:
        """使用处理器处理消息"""
        try:
            # 模拟异步处理
            await asyncio.sleep(0.01)
            response = handler.handle_message(message)
            if response:
                await self.send_message(response)
        except Exception as e:
            print(f"❌ 异步处理器错误: {handler.__class__.__name__} - {str(e)}")


# ============================================================================
# 4. 中间件
# ============================================================================

def logging_middleware(message: Message) -> Message:
    """日志中间件"""
    print(f"🔍 中间件日志: {message.type.value} - {message.topic} ({message.sender} -> {message.receiver})")
    return message


def validation_middleware(message: Message) -> Message:
    """验证中间件"""
    if not message.sender:
        raise ValueError("消息发送者不能为空")
    if not message.receiver and message.type != MessageType.EVENT:
        raise ValueError("非事件消息必须指定接收者")
    print(f"✅ 中间件验证: {message.id} 验证通过")
    return message


def encryption_middleware(message: Message) -> Message:
    """加密中间件（模拟）"""
    # 模拟加密敏感数据
    if 'password' in message.payload:
        message.payload['password'] = '***encrypted***'
    print(f"🔐 中间件加密: {message.id} 敏感数据已加密")
    return message


# ============================================================================
# 5. 具体模块实现
# ============================================================================

class UserModule(MessageHandler):
    """用户模块"""
    
    def __init__(self, module_id: str):
        self.module_id = module_id
        self.users: Dict[str, Dict[str, Any]] = {}
        self.message_bus: Optional[MessageBus] = None
    
    def set_message_bus(self, message_bus: MessageBus) -> None:
        """设置消息总线"""
        self.message_bus = message_bus
        message_bus.register_handler(self.module_id, self)
    
    def can_handle(self, message: Message) -> bool:
        """判断是否能处理消息"""
        return message.topic.startswith('user.')
    
    def handle_message(self, message: Message) -> Optional[Message]:
        """处理消息"""
        if message.topic == 'user.create':
            return self._handle_create_user(message)
        elif message.topic == 'user.get':
            return self._handle_get_user(message)
        elif message.topic == 'user.update':
            return self._handle_update_user(message)
        elif message.topic == 'user.delete':
            return self._handle_delete_user(message)
        return None
    
    def _handle_create_user(self, message: Message) -> Message:
        """处理创建用户"""
        user_data = message.payload
        user_id = str(uuid.uuid4())
        
        self.users[user_id] = {
            'id': user_id,
            'username': user_data.get('username'),
            'email': user_data.get('email'),
            'created_at': datetime.now()
        }
        
        print(f"👤 用户已创建: {user_id}")
        
        # 发送用户创建事件
        if self.message_bus:
            self.message_bus.send_event(
                sender=self.module_id,
                topic='user.created',
                payload={'user_id': user_id, 'username': user_data.get('username')}
            )
        
        return Message(
            type=MessageType.RESPONSE,
            sender=self.module_id,
            receiver=message.sender,
            topic='response.user.create',
            payload={'success': True, 'user_id': user_id},
            correlation_id=message.id
        )
    
    def _handle_get_user(self, message: Message) -> Message:
        """处理获取用户"""
        user_id = message.payload.get('user_id')
        user = self.users.get(user_id)
        
        if user:
            print(f"👤 用户已找到: {user_id}")
            payload = {'success': True, 'user': user}
        else:
            print(f"👤 用户未找到: {user_id}")
            payload = {'success': False, 'error': 'User not found'}
        
        return Message(
            type=MessageType.RESPONSE,
            sender=self.module_id,
            receiver=message.sender,
            topic='response.user.get',
            payload=payload,
            correlation_id=message.id
        )
    
    def _handle_update_user(self, message: Message) -> Message:
        """处理更新用户"""
        user_id = message.payload.get('user_id')
        updates = message.payload.get('updates', {})
        
        if user_id in self.users:
            self.users[user_id].update(updates)
            self.users[user_id]['updated_at'] = datetime.now()
            
            print(f"👤 用户已更新: {user_id}")
            
            # 发送用户更新事件
            if self.message_bus:
                self.message_bus.send_event(
                    sender=self.module_id,
                    topic='user.updated',
                    payload={'user_id': user_id, 'updates': updates}
                )
            
            payload = {'success': True}
        else:
            payload = {'success': False, 'error': 'User not found'}
        
        return Message(
            type=MessageType.RESPONSE,
            sender=self.module_id,
            receiver=message.sender,
            topic='response.user.update',
            payload=payload,
            correlation_id=message.id
        )
    
    def _handle_delete_user(self, message: Message) -> Message:
        """处理删除用户"""
        user_id = message.payload.get('user_id')
        
        if user_id in self.users:
            del self.users[user_id]
            print(f"👤 用户已删除: {user_id}")
            
            # 发送用户删除事件
            if self.message_bus:
                self.message_bus.send_event(
                    sender=self.module_id,
                    topic='user.deleted',
                    payload={'user_id': user_id}
                )
            
            payload = {'success': True}
        else:
            payload = {'success': False, 'error': 'User not found'}
        
        return Message(
            type=MessageType.RESPONSE,
            sender=self.module_id,
            receiver=message.sender,
            topic='response.user.delete',
            payload=payload,
            correlation_id=message.id
        )


class OrderModule(MessageHandler):
    """订单模块"""
    
    def __init__(self, module_id: str):
        self.module_id = module_id
        self.orders: Dict[str, Dict[str, Any]] = {}
        self.message_bus: Optional[MessageBus] = None
    
    def set_message_bus(self, message_bus: MessageBus) -> None:
        """设置消息总线"""
        self.message_bus = message_bus
        message_bus.register_handler(self.module_id, self)
        # 订阅用户事件
        message_bus.register_topic_handler('user.deleted', self)
    
    def can_handle(self, message: Message) -> bool:
        """判断是否能处理消息"""
        return (message.topic.startswith('order.') or 
                message.topic == 'user.deleted')
    
    def handle_message(self, message: Message) -> Optional[Message]:
        """处理消息"""
        if message.topic == 'order.create':
            return self._handle_create_order(message)
        elif message.topic == 'order.get':
            return self._handle_get_order(message)
        elif message.topic == 'order.cancel':
            return self._handle_cancel_order(message)
        elif message.topic == 'user.deleted':
            self._handle_user_deleted(message)
        return None
    
    def _handle_create_order(self, message: Message) -> Message:
        """处理创建订单"""
        order_data = message.payload
        order_id = f"ORDER-{uuid.uuid4().hex[:8].upper()}"
        
        self.orders[order_id] = {
            'id': order_id,
            'user_id': order_data.get('user_id'),
            'items': order_data.get('items', []),
            'total': order_data.get('total', 0),
            'status': 'created',
            'created_at': datetime.now()
        }
        
        print(f"📦 订单已创建: {order_id}")
        
        # 发送订单创建事件
        if self.message_bus:
            self.message_bus.send_event(
                sender=self.module_id,
                topic='order.created',
                payload={'order_id': order_id, 'user_id': order_data.get('user_id')}
            )
        
        return Message(
            type=MessageType.RESPONSE,
            sender=self.module_id,
            receiver=message.sender,
            topic='response.order.create',
            payload={'success': True, 'order_id': order_id},
            correlation_id=message.id
        )
    
    def _handle_get_order(self, message: Message) -> Message:
        """处理获取订单"""
        order_id = message.payload.get('order_id')
        order = self.orders.get(order_id)
        
        if order:
            print(f"📦 订单已找到: {order_id}")
            payload = {'success': True, 'order': order}
        else:
            print(f"📦 订单未找到: {order_id}")
            payload = {'success': False, 'error': 'Order not found'}
        
        return Message(
            type=MessageType.RESPONSE,
            sender=self.module_id,
            receiver=message.sender,
            topic='response.order.get',
            payload=payload,
            correlation_id=message.id
        )
    
    def _handle_cancel_order(self, message: Message) -> Message:
        """处理取消订单"""
        order_id = message.payload.get('order_id')
        
        if order_id in self.orders:
            self.orders[order_id]['status'] = 'cancelled'
            self.orders[order_id]['cancelled_at'] = datetime.now()
            
            print(f"📦 订单已取消: {order_id}")
            
            # 发送订单取消事件
            if self.message_bus:
                self.message_bus.send_event(
                    sender=self.module_id,
                    topic='order.cancelled',
                    payload={'order_id': order_id}
                )
            
            payload = {'success': True}
        else:
            payload = {'success': False, 'error': 'Order not found'}
        
        return Message(
            type=MessageType.RESPONSE,
            sender=self.module_id,
            receiver=message.sender,
            topic='response.order.cancel',
            payload=payload,
            correlation_id=message.id
        )
    
    def _handle_user_deleted(self, message: Message) -> None:
        """处理用户删除事件"""
        user_id = message.payload.get('user_id')
        
        # 取消该用户的所有订单
        cancelled_orders = []
        for order_id, order in self.orders.items():
            if order['user_id'] == user_id and order['status'] != 'cancelled':
                order['status'] = 'cancelled'
                order['cancelled_at'] = datetime.now()
                order['cancel_reason'] = 'User deleted'
                cancelled_orders.append(order_id)
        
        if cancelled_orders:
            print(f"📦 因用户删除而取消的订单: {cancelled_orders}")


class NotificationModule(MessageHandler):
    """通知模块"""
    
    def __init__(self, module_id: str):
        self.module_id = module_id
        self.notifications: List[Dict[str, Any]] = []
        self.message_bus: Optional[MessageBus] = None
    
    def set_message_bus(self, message_bus: MessageBus) -> None:
        """设置消息总线"""
        self.message_bus = message_bus
        message_bus.register_handler(self.module_id, self)
        # 订阅所有事件
        message_bus.register_topic_handler('user.created', self)
        message_bus.register_topic_handler('user.updated', self)
        message_bus.register_topic_handler('order.created', self)
        message_bus.register_topic_handler('order.cancelled', self)
    
    def can_handle(self, message: Message) -> bool:
        """判断是否能处理消息"""
        return (message.topic.startswith('notification.') or 
                message.type == MessageType.EVENT)
    
    def handle_message(self, message: Message) -> Optional[Message]:
        """处理消息"""
        if message.type == MessageType.EVENT:
            self._handle_event(message)
        elif message.topic == 'notification.send':
            return self._handle_send_notification(message)
        return None
    
    def _handle_event(self, message: Message) -> None:
        """处理事件消息"""
        notification = {
            'id': str(uuid.uuid4()),
            'type': 'event_notification',
            'event_type': message.topic,
            'message': self._generate_notification_message(message),
            'timestamp': datetime.now(),
            'data': message.payload
        }
        
        self.notifications.append(notification)
        print(f"📢 事件通知: {notification['message']}")
    
    def _handle_send_notification(self, message: Message) -> Message:
        """处理发送通知"""
        notification_data = message.payload
        
        notification = {
            'id': str(uuid.uuid4()),
            'type': 'direct_notification',
            'recipient': notification_data.get('recipient'),
            'message': notification_data.get('message'),
            'timestamp': datetime.now()
        }
        
        self.notifications.append(notification)
        print(f"📢 直接通知: {notification['message']} -> {notification['recipient']}")
        
        return Message(
            type=MessageType.RESPONSE,
            sender=self.module_id,
            receiver=message.sender,
            topic='response.notification.send',
            payload={'success': True, 'notification_id': notification['id']},
            correlation_id=message.id
        )
    
    def _generate_notification_message(self, message: Message) -> str:
        """生成通知消息"""
        if message.topic == 'user.created':
            username = message.payload.get('username', 'Unknown')
            return f"新用户 {username} 已注册"
        elif message.topic == 'user.updated':
            user_id = message.payload.get('user_id', 'Unknown')
            return f"用户 {user_id} 信息已更新"
        elif message.topic == 'order.created':
            order_id = message.payload.get('order_id', 'Unknown')
            return f"新订单 {order_id} 已创建"
        elif message.topic == 'order.cancelled':
            order_id = message.payload.get('order_id', 'Unknown')
            return f"订单 {order_id} 已取消"
        else:
            return f"事件: {message.topic}"
    
    def get_notifications(self, count: int = 10) -> List[Dict[str, Any]]:
        """获取通知列表"""
        return self.notifications[-count:] if count > 0 else self.notifications


# ============================================================================
# 6. 演示函数
# ============================================================================

def demo_module_communication():
    """演示模块间通信"""
    print("模块间通信演示")
    print("=" * 50)
    
    # 1. 创建消息总线
    print("\n1. 创建消息总线")
    message_bus = MessageBus()
    
    # 添加中间件
    message_bus.add_middleware(validation_middleware)
    message_bus.add_middleware(logging_middleware)
    message_bus.add_middleware(encryption_middleware)
    
    # 启动消息总线
    message_bus.start()
    
    # 2. 创建模块
    print("\n2. 创建模块")
    user_module = UserModule("user_service")
    order_module = OrderModule("order_service")
    notification_module = NotificationModule("notification_service")
    
    # 注册模块到消息总线
    user_module.set_message_bus(message_bus)
    order_module.set_message_bus(message_bus)
    notification_module.set_message_bus(message_bus)
    
    # 等待消息总线启动
    time.sleep(0.5)
    
    # 3. 演示命令消息
    print("\n3. 演示命令消息")
    
    # 创建用户
    print("\n--- 创建用户 ---")
    create_user_msg_id = message_bus.send_command(
        sender="client",
        receiver="user_service",
        command="user.create",
        payload={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret123'
        }
    )
    
    # 等待响应
    time.sleep(1)
    response = message_bus.wait_for_response(create_user_msg_id, timeout=5)
    if response:
        user_id = response.payload.get('user_id')
        print(f"✅ 用户创建响应: {response.payload}")
    
    # 4. 演示查询消息
    print("\n4. 演示查询消息")
    
    if response and response.payload.get('success'):
        user_id = response.payload.get('user_id')
        
        # 查询用户
        print("\n--- 查询用户 ---")
        query_msg_id = message_bus.send_query(
            sender="client",
            receiver="user_service",
            query="user.get",
            payload={'user_id': user_id}
        )
        
        time.sleep(1)
        query_response = message_bus.wait_for_response(query_msg_id, timeout=5)
        if query_response:
            print(f"✅ 用户查询响应: {query_response.payload}")
    
    # 5. 演示事件消息和模块间协作
    print("\n5. 演示事件消息和模块间协作")
    
    if user_id:
        # 创建订单
        print("\n--- 创建订单 ---")
        create_order_msg_id = message_bus.send_command(
            sender="client",
            receiver="order_service",
            command="order.create",
            payload={
                'user_id': user_id,
                'items': [
                    {'name': 'Python书籍', 'price': 59.99, 'quantity': 2},
                    {'name': '编程键盘', 'price': 299.99, 'quantity': 1}
                ],
                'total': 419.97
            }
        )
        
        time.sleep(1)
        order_response = message_bus.wait_for_response(create_order_msg_id, timeout=5)
        if order_response:
            order_id = order_response.payload.get('order_id')
            print(f"✅ 订单创建响应: {order_response.payload}")
    
    # 6. 演示级联操作
    print("\n6. 演示级联操作（删除用户）")
    
    if user_id:
        print("\n--- 删除用户（观察级联效果） ---")
        delete_msg_id = message_bus.send_command(
            sender="client",
            receiver="user_service",
            command="user.delete",
            payload={'user_id': user_id}
        )
        
        time.sleep(1)
        delete_response = message_bus.wait_for_response(delete_msg_id, timeout=5)
        if delete_response:
            print(f"✅ 用户删除响应: {delete_response.payload}")
    
    # 7. 查看通知
    print("\n7. 查看通知")
    time.sleep(1)
    notifications = notification_module.get_notifications()
    print(f"📢 收到的通知数量: {len(notifications)}")
    for i, notif in enumerate(notifications, 1):
        print(f"   {i}. {notif['message']} ({notif['timestamp'].strftime('%H:%M:%S')})")
    
    # 8. 显示统计信息
    print("\n8. 消息总线统计")
    stats = message_bus.get_statistics()
    print(f"📊 统计信息:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # 9. 停止消息总线
    print("\n9. 停止消息总线")
    message_bus.stop()
    
    print("\n演示完成！")


async def demo_async_communication():
    """演示异步模块通信"""
    print("\n异步模块间通信演示")
    print("=" * 50)
    
    # 创建异步消息总线
    async_bus = AsyncMessageBus()
    await async_bus.start()
    
    # 创建简单的异步处理器
    class AsyncEchoHandler(MessageHandler):
        def __init__(self, name: str):
            self.name = name
        
        def can_handle(self, message: Message) -> bool:
            return message.topic == 'echo'
        
        def handle_message(self, message: Message) -> Optional[Message]:
            print(f"🔄 {self.name} 处理消息: {message.payload}")
            return Message(
                type=MessageType.RESPONSE,
                sender=self.name,
                receiver=message.sender,
                topic='response.echo',
                payload={'echo': message.payload, 'handler': self.name},
                correlation_id=message.id
            )
    
    # 注册处理器
    handler1 = AsyncEchoHandler("handler1")
    handler2 = AsyncEchoHandler("handler2")
    
    async_bus.register_handler("service1", handler1)
    async_bus.register_handler("service2", handler2)
    
    # 发送消息
    messages = [
        Message(
            type=MessageType.COMMAND,
            sender="client",
            receiver="service1",
            topic="echo",
            payload={'message': f'Hello from message {i}'}
        ) for i in range(3)
    ]
    
    # 并发发送消息
    print("\n发送异步消息...")
    for msg in messages:
        await async_bus.send_message(msg)
    
    # 等待处理完成
    await asyncio.sleep(1)
    
    print(f"\n📊 异步处理的消息数量: {len(async_bus.message_history)}")
    
    # 停止异步总线
    await async_bus.stop()
    
    print("\n异步演示完成！")


if __name__ == "__main__":
    # 同步演示
    demo_module_communication()
    
    # 异步演示
    print("\n" + "=" * 60)
    asyncio.run(demo_async_communication())