#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session28 示例2：事件驱动架构详解

本示例展示了事件驱动架构的设计模式和实现方式。

作者: Python教程团队
创建日期: 2024-01-15
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import asyncio
import json
import uuid


# ============================================================================
# 1. 事件基础设施
# ============================================================================

@dataclass
class Event:
    """基础事件类"""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    data: Dict[str, Any] = field(default_factory=dict)
    source: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'event_id': self.event_id,
            'event_type': self.event_type,
            'timestamp': self.timestamp.isoformat(),
            'data': self.data,
            'source': self.source
        }


class EventHandler(ABC):
    """事件处理器接口"""
    
    @abstractmethod
    def handle(self, event: Event) -> None:
        """处理事件"""
        pass
    
    @abstractmethod
    def can_handle(self, event_type: str) -> bool:
        """判断是否能处理指定类型的事件"""
        pass


class AsyncEventHandler(ABC):
    """异步事件处理器接口"""
    
    @abstractmethod
    async def handle_async(self, event: Event) -> None:
        """异步处理事件"""
        pass
    
    @abstractmethod
    def can_handle(self, event_type: str) -> bool:
        """判断是否能处理指定类型的事件"""
        pass


# ============================================================================
# 2. 事件总线实现
# ============================================================================

class EventBus:
    """同步事件总线"""
    
    def __init__(self):
        self._handlers: Dict[str, List[EventHandler]] = {}
        self._global_handlers: List[EventHandler] = []
        self._event_history: List[Event] = []
        self._middleware: List[Callable[[Event], Event]] = []
    
    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        """订阅特定类型的事件"""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
        print(f"📝 订阅事件: {event_type} -> {handler.__class__.__name__}")
    
    def subscribe_global(self, handler: EventHandler) -> None:
        """订阅所有事件"""
        self._global_handlers.append(handler)
        print(f"📝 全局订阅: {handler.__class__.__name__}")
    
    def unsubscribe(self, event_type: str, handler: EventHandler) -> None:
        """取消订阅"""
        if event_type in self._handlers:
            if handler in self._handlers[event_type]:
                self._handlers[event_type].remove(handler)
                print(f"📝 取消订阅: {event_type} -> {handler.__class__.__name__}")
    
    def add_middleware(self, middleware: Callable[[Event], Event]) -> None:
        """添加中间件"""
        self._middleware.append(middleware)
    
    def publish(self, event: Event) -> None:
        """发布事件"""
        # 应用中间件
        for middleware in self._middleware:
            event = middleware(event)
        
        # 记录事件历史
        self._event_history.append(event)
        
        print(f"📢 发布事件: {event.event_type} (ID: {event.event_id[:8]}...)")
        
        # 处理特定类型的事件处理器
        if event.event_type in self._handlers:
            for handler in self._handlers[event.event_type]:
                try:
                    handler.handle(event)
                except Exception as e:
                    print(f"❌ 事件处理错误: {handler.__class__.__name__} - {str(e)}")
        
        # 处理全局事件处理器
        for handler in self._global_handlers:
            if handler.can_handle(event.event_type):
                try:
                    handler.handle(event)
                except Exception as e:
                    print(f"❌ 全局事件处理错误: {handler.__class__.__name__} - {str(e)}")
    
    def get_event_history(self) -> List[Event]:
        """获取事件历史"""
        return self._event_history.copy()
    
    def clear_history(self) -> None:
        """清空事件历史"""
        self._event_history.clear()


class AsyncEventBus:
    """异步事件总线"""
    
    def __init__(self):
        self._handlers: Dict[str, List[AsyncEventHandler]] = {}
        self._global_handlers: List[AsyncEventHandler] = []
        self._event_history: List[Event] = []
        self._middleware: List[Callable[[Event], Event]] = []
    
    def subscribe(self, event_type: str, handler: AsyncEventHandler) -> None:
        """订阅特定类型的事件"""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
        print(f"📝 异步订阅事件: {event_type} -> {handler.__class__.__name__}")
    
    def subscribe_global(self, handler: AsyncEventHandler) -> None:
        """订阅所有事件"""
        self._global_handlers.append(handler)
        print(f"📝 异步全局订阅: {handler.__class__.__name__}")
    
    async def publish(self, event: Event) -> None:
        """异步发布事件"""
        # 应用中间件
        for middleware in self._middleware:
            event = middleware(event)
        
        # 记录事件历史
        self._event_history.append(event)
        
        print(f"📢 异步发布事件: {event.event_type} (ID: {event.event_id[:8]}...)")
        
        # 收集所有需要执行的处理器
        tasks = []
        
        # 特定类型的事件处理器
        if event.event_type in self._handlers:
            for handler in self._handlers[event.event_type]:
                tasks.append(handler.handle_async(event))
        
        # 全局事件处理器
        for handler in self._global_handlers:
            if handler.can_handle(event.event_type):
                tasks.append(handler.handle_async(event))
        
        # 并发执行所有处理器
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)


# ============================================================================
# 3. 具体事件类型
# ============================================================================

class UserEvents:
    """用户相关事件"""
    USER_REGISTERED = "user.registered"
    USER_LOGIN = "user.login"
    USER_LOGOUT = "user.logout"
    USER_PROFILE_UPDATED = "user.profile_updated"
    USER_DELETED = "user.deleted"


class OrderEvents:
    """订单相关事件"""
    ORDER_CREATED = "order.created"
    ORDER_PAID = "order.paid"
    ORDER_SHIPPED = "order.shipped"
    ORDER_DELIVERED = "order.delivered"
    ORDER_CANCELLED = "order.cancelled"


class SystemEvents:
    """系统相关事件"""
    SYSTEM_STARTUP = "system.startup"
    SYSTEM_SHUTDOWN = "system.shutdown"
    ERROR_OCCURRED = "system.error"
    PERFORMANCE_ALERT = "system.performance_alert"


# ============================================================================
# 4. 具体事件处理器
# ============================================================================

class EmailNotificationHandler(EventHandler):
    """邮件通知处理器"""
    
    def __init__(self):
        self.sent_emails: List[Dict[str, Any]] = []
    
    def can_handle(self, event_type: str) -> bool:
        """判断是否处理该事件类型"""
        return event_type in [
            UserEvents.USER_REGISTERED,
            OrderEvents.ORDER_CREATED,
            OrderEvents.ORDER_SHIPPED
        ]
    
    def handle(self, event: Event) -> None:
        """处理事件"""
        if event.event_type == UserEvents.USER_REGISTERED:
            self._send_welcome_email(event)
        elif event.event_type == OrderEvents.ORDER_CREATED:
            self._send_order_confirmation(event)
        elif event.event_type == OrderEvents.ORDER_SHIPPED:
            self._send_shipping_notification(event)
    
    def _send_welcome_email(self, event: Event) -> None:
        """发送欢迎邮件"""
        email_data = {
            'to': event.data.get('email'),
            'subject': '欢迎注册！',
            'body': f"欢迎 {event.data.get('username')} 加入我们！",
            'timestamp': datetime.now()
        }
        self.sent_emails.append(email_data)
        print(f"📧 发送欢迎邮件到: {email_data['to']}")
    
    def _send_order_confirmation(self, event: Event) -> None:
        """发送订单确认邮件"""
        email_data = {
            'to': event.data.get('customer_email'),
            'subject': '订单确认',
            'body': f"您的订单 {event.data.get('order_id')} 已确认",
            'timestamp': datetime.now()
        }
        self.sent_emails.append(email_data)
        print(f"📧 发送订单确认邮件: {event.data.get('order_id')}")
    
    def _send_shipping_notification(self, event: Event) -> None:
        """发送发货通知"""
        email_data = {
            'to': event.data.get('customer_email'),
            'subject': '订单已发货',
            'body': f"您的订单 {event.data.get('order_id')} 已发货，快递单号: {event.data.get('tracking_number')}",
            'timestamp': datetime.now()
        }
        self.sent_emails.append(email_data)
        print(f"📧 发送发货通知: {event.data.get('order_id')}")


class AuditLogHandler(EventHandler):
    """审计日志处理器"""
    
    def __init__(self):
        self.audit_logs: List[Dict[str, Any]] = []
    
    def can_handle(self, event_type: str) -> bool:
        """处理所有事件"""
        return True
    
    def handle(self, event: Event) -> None:
        """记录审计日志"""
        log_entry = {
            'event_id': event.event_id,
            'event_type': event.event_type,
            'timestamp': event.timestamp,
            'source': event.source,
            'data_summary': self._summarize_data(event.data)
        }
        self.audit_logs.append(log_entry)
        print(f"📋 审计日志: {event.event_type} - {log_entry['data_summary']}")
    
    def _summarize_data(self, data: Dict[str, Any]) -> str:
        """总结事件数据"""
        if 'username' in data:
            return f"用户: {data['username']}"
        elif 'order_id' in data:
            return f"订单: {data['order_id']}"
        else:
            return f"数据项: {len(data)}"


class MetricsCollectorHandler(EventHandler):
    """指标收集处理器"""
    
    def __init__(self):
        self.metrics: Dict[str, int] = {}
    
    def can_handle(self, event_type: str) -> bool:
        """处理所有事件"""
        return True
    
    def handle(self, event: Event) -> None:
        """收集指标"""
        # 统计事件类型
        if event.event_type not in self.metrics:
            self.metrics[event.event_type] = 0
        self.metrics[event.event_type] += 1
        
        # 统计总事件数
        if 'total_events' not in self.metrics:
            self.metrics['total_events'] = 0
        self.metrics['total_events'] += 1
        
        print(f"📊 指标更新: {event.event_type} = {self.metrics[event.event_type]}")
    
    def get_metrics(self) -> Dict[str, int]:
        """获取指标"""
        return self.metrics.copy()


class CacheInvalidationHandler(EventHandler):
    """缓存失效处理器"""
    
    def __init__(self):
        self.invalidated_keys: List[str] = []
    
    def can_handle(self, event_type: str) -> bool:
        """处理用户和订单相关事件"""
        return event_type.startswith('user.') or event_type.startswith('order.')
    
    def handle(self, event: Event) -> None:
        """处理缓存失效"""
        if event.event_type.startswith('user.'):
            self._invalidate_user_cache(event)
        elif event.event_type.startswith('order.'):
            self._invalidate_order_cache(event)
    
    def _invalidate_user_cache(self, event: Event) -> None:
        """失效用户缓存"""
        user_id = event.data.get('user_id')
        username = event.data.get('username')
        
        cache_keys = []
        if user_id:
            cache_keys.append(f"user:{user_id}")
        if username:
            cache_keys.append(f"user:username:{username}")
        
        for key in cache_keys:
            self.invalidated_keys.append(key)
            print(f"🗑️ 缓存失效: {key}")
    
    def _invalidate_order_cache(self, event: Event) -> None:
        """失效订单缓存"""
        order_id = event.data.get('order_id')
        user_id = event.data.get('user_id')
        
        cache_keys = []
        if order_id:
            cache_keys.append(f"order:{order_id}")
        if user_id:
            cache_keys.append(f"user:{user_id}:orders")
        
        for key in cache_keys:
            self.invalidated_keys.append(key)
            print(f"🗑️ 缓存失效: {key}")


# ============================================================================
# 5. 异步事件处理器
# ============================================================================

class AsyncEmailHandler(AsyncEventHandler):
    """异步邮件处理器"""
    
    def __init__(self):
        self.sent_emails: List[Dict[str, Any]] = []
    
    def can_handle(self, event_type: str) -> bool:
        return event_type in [UserEvents.USER_REGISTERED, OrderEvents.ORDER_CREATED]
    
    async def handle_async(self, event: Event) -> None:
        """异步处理邮件发送"""
        print(f"📧 异步处理邮件: {event.event_type}")
        
        # 模拟异步邮件发送
        await asyncio.sleep(0.1)  # 模拟网络延迟
        
        email_data = {
            'event_id': event.event_id,
            'event_type': event.event_type,
            'timestamp': datetime.now(),
            'processed': True
        }
        self.sent_emails.append(email_data)
        print(f"📧 异步邮件发送完成: {event.event_type}")


class AsyncAnalyticsHandler(AsyncEventHandler):
    """异步分析处理器"""
    
    def __init__(self):
        self.analytics_data: List[Dict[str, Any]] = []
    
    def can_handle(self, event_type: str) -> bool:
        return True  # 处理所有事件
    
    async def handle_async(self, event: Event) -> None:
        """异步处理分析数据"""
        print(f"📈 异步分析处理: {event.event_type}")
        
        # 模拟复杂的分析计算
        await asyncio.sleep(0.2)
        
        analytics_entry = {
            'event_id': event.event_id,
            'event_type': event.event_type,
            'timestamp': event.timestamp,
            'analysis_timestamp': datetime.now(),
            'processed': True
        }
        self.analytics_data.append(analytics_entry)
        print(f"📈 异步分析完成: {event.event_type}")


# ============================================================================
# 6. 中间件
# ============================================================================

def logging_middleware(event: Event) -> Event:
    """日志中间件"""
    print(f"🔍 中间件日志: {event.event_type} from {event.source}")
    return event


def validation_middleware(event: Event) -> Event:
    """验证中间件"""
    if not event.event_type:
        raise ValueError("事件类型不能为空")
    if not event.source:
        event.source = "unknown"
    print(f"✅ 中间件验证: {event.event_type} 验证通过")
    return event


def enrichment_middleware(event: Event) -> Event:
    """数据丰富中间件"""
    # 添加处理时间戳
    event.data['processed_at'] = datetime.now().isoformat()
    # 添加事件版本
    event.data['event_version'] = '1.0'
    print(f"🔧 中间件丰富: {event.event_type} 数据已丰富")
    return event


# ============================================================================
# 7. 业务服务（事件发布者）
# ============================================================================

class UserService:
    """用户服务"""
    
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.users: Dict[str, Dict[str, Any]] = {}
    
    def register_user(self, username: str, email: str, password: str) -> bool:
        """注册用户"""
        if username in self.users:
            print(f"❌ 用户 {username} 已存在")
            return False
        
        # 创建用户
        user_data = {
            'user_id': str(uuid.uuid4()),
            'username': username,
            'email': email,
            'created_at': datetime.now()
        }
        self.users[username] = user_data
        
        # 发布用户注册事件
        event = Event(
            event_type=UserEvents.USER_REGISTERED,
            source="UserService",
            data=user_data
        )
        self.event_bus.publish(event)
        
        print(f"✅ 用户 {username} 注册成功")
        return True
    
    def login_user(self, username: str, password: str) -> bool:
        """用户登录"""
        if username not in self.users:
            print(f"❌ 用户 {username} 不存在")
            return False
        
        # 发布登录事件
        event = Event(
            event_type=UserEvents.USER_LOGIN,
            source="UserService",
            data={
                'user_id': self.users[username]['user_id'],
                'username': username,
                'login_time': datetime.now()
            }
        )
        self.event_bus.publish(event)
        
        print(f"✅ 用户 {username} 登录成功")
        return True


class OrderService:
    """订单服务"""
    
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.orders: Dict[str, Dict[str, Any]] = {}
    
    def create_order(self, user_id: str, customer_email: str, items: List[Dict[str, Any]]) -> str:
        """创建订单"""
        order_id = f"ORDER-{uuid.uuid4().hex[:8].upper()}"
        
        order_data = {
            'order_id': order_id,
            'user_id': user_id,
            'customer_email': customer_email,
            'items': items,
            'total_amount': sum(item.get('price', 0) * item.get('quantity', 1) for item in items),
            'status': 'created',
            'created_at': datetime.now()
        }
        self.orders[order_id] = order_data
        
        # 发布订单创建事件
        event = Event(
            event_type=OrderEvents.ORDER_CREATED,
            source="OrderService",
            data=order_data
        )
        self.event_bus.publish(event)
        
        print(f"✅ 订单 {order_id} 创建成功")
        return order_id
    
    def ship_order(self, order_id: str, tracking_number: str) -> bool:
        """发货"""
        if order_id not in self.orders:
            print(f"❌ 订单 {order_id} 不存在")
            return False
        
        # 更新订单状态
        self.orders[order_id]['status'] = 'shipped'
        self.orders[order_id]['tracking_number'] = tracking_number
        self.orders[order_id]['shipped_at'] = datetime.now()
        
        # 发布发货事件
        event = Event(
            event_type=OrderEvents.ORDER_SHIPPED,
            source="OrderService",
            data={
                'order_id': order_id,
                'customer_email': self.orders[order_id]['customer_email'],
                'tracking_number': tracking_number,
                'shipped_at': datetime.now()
            }
        )
        self.event_bus.publish(event)
        
        print(f"✅ 订单 {order_id} 已发货")
        return True


# ============================================================================
# 8. 演示函数
# ============================================================================

def demo_event_driven_architecture():
    """演示事件驱动架构"""
    print("事件驱动架构演示")
    print("=" * 50)
    
    # 1. 创建事件总线
    print("\n1. 创建事件总线和处理器")
    event_bus = EventBus()
    
    # 添加中间件
    event_bus.add_middleware(validation_middleware)
    event_bus.add_middleware(logging_middleware)
    event_bus.add_middleware(enrichment_middleware)
    
    # 创建事件处理器
    email_handler = EmailNotificationHandler()
    audit_handler = AuditLogHandler()
    metrics_handler = MetricsCollectorHandler()
    cache_handler = CacheInvalidationHandler()
    
    # 订阅事件
    event_bus.subscribe(UserEvents.USER_REGISTERED, email_handler)
    event_bus.subscribe(OrderEvents.ORDER_CREATED, email_handler)
    event_bus.subscribe(OrderEvents.ORDER_SHIPPED, email_handler)
    
    event_bus.subscribe_global(audit_handler)
    event_bus.subscribe_global(metrics_handler)
    event_bus.subscribe_global(cache_handler)
    
    # 2. 创建业务服务
    print("\n2. 创建业务服务")
    user_service = UserService(event_bus)
    order_service = OrderService(event_bus)
    
    # 3. 执行业务操作
    print("\n3. 执行业务操作")
    
    # 注册用户
    print("\n--- 用户注册 ---")
    user_service.register_user("alice", "alice@example.com", "password123")
    
    # 用户登录
    print("\n--- 用户登录 ---")
    user_service.login_user("alice", "password123")
    
    # 创建订单
    print("\n--- 创建订单 ---")
    order_id = order_service.create_order(
        user_id="user-123",
        customer_email="alice@example.com",
        items=[
            {'name': 'Python书籍', 'price': 59.99, 'quantity': 2},
            {'name': '编程键盘', 'price': 299.99, 'quantity': 1}
        ]
    )
    
    # 发货
    print("\n--- 订单发货 ---")
    order_service.ship_order(order_id, "SF1234567890")
    
    # 4. 查看处理结果
    print("\n4. 查看处理结果")
    
    print(f"\n📧 发送的邮件数量: {len(email_handler.sent_emails)}")
    for email in email_handler.sent_emails:
        print(f"   - {email.get('subject', 'N/A')} -> {email.get('to', 'N/A')}")
    
    print(f"\n📋 审计日志数量: {len(audit_handler.audit_logs)}")
    for log in audit_handler.audit_logs[-3:]:  # 显示最后3条
        print(f"   - {log['event_type']}: {log['data_summary']}")
    
    print(f"\n📊 事件指标:")
    for event_type, count in metrics_handler.get_metrics().items():
        print(f"   - {event_type}: {count}")
    
    print(f"\n🗑️ 失效的缓存键数量: {len(cache_handler.invalidated_keys)}")
    for key in cache_handler.invalidated_keys[-5:]:  # 显示最后5个
        print(f"   - {key}")
    
    print(f"\n📚 事件历史数量: {len(event_bus.get_event_history())}")
    
    print("\n演示完成！")


async def demo_async_event_driven():
    """演示异步事件驱动架构"""
    print("\n异步事件驱动架构演示")
    print("=" * 50)
    
    # 创建异步事件总线
    async_bus = AsyncEventBus()
    
    # 创建异步处理器
    async_email_handler = AsyncEmailHandler()
    async_analytics_handler = AsyncAnalyticsHandler()
    
    # 订阅事件
    async_bus.subscribe(UserEvents.USER_REGISTERED, async_email_handler)
    async_bus.subscribe(OrderEvents.ORDER_CREATED, async_email_handler)
    async_bus.subscribe_global(async_analytics_handler)
    
    # 发布多个事件
    events = [
        Event(
            event_type=UserEvents.USER_REGISTERED,
            source="AsyncDemo",
            data={'username': 'bob', 'email': 'bob@example.com'}
        ),
        Event(
            event_type=OrderEvents.ORDER_CREATED,
            source="AsyncDemo",
            data={'order_id': 'ORDER-ASYNC-001', 'customer_email': 'bob@example.com'}
        ),
        Event(
            event_type=UserEvents.USER_LOGIN,
            source="AsyncDemo",
            data={'username': 'bob'}
        )
    ]
    
    # 并发发布事件
    print("\n发布异步事件...")
    tasks = [async_bus.publish(event) for event in events]
    await asyncio.gather(*tasks)
    
    print(f"\n📧 异步邮件处理数量: {len(async_email_handler.sent_emails)}")
    print(f"📈 异步分析数据数量: {len(async_analytics_handler.analytics_data)}")
    
    print("\n异步演示完成！")


if __name__ == "__main__":
    # 同步演示
    demo_event_driven_architecture()
    
    # 异步演示
    print("\n" + "=" * 60)
    asyncio.run(demo_async_event_driven())