#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session28 示例5：微服务架构模式详解

本示例展示了微服务架构的设计模式和实现方式。

作者: Python教程团队
创建日期: 2024-01-15
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Callable, Union, Type
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import json
import uuid
import time
import threading
from collections import defaultdict, deque
import weakref
from contextlib import contextmanager


# ============================================================================
# 1. 服务发现和注册
# ============================================================================

class ServiceStatus(Enum):
    """服务状态"""
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass
class ServiceInfo:
    """服务信息"""
    service_id: str
    service_name: str
    version: str
    host: str
    port: int
    status: ServiceStatus = ServiceStatus.STARTING
    metadata: Dict[str, Any] = field(default_factory=dict)
    health_check_url: Optional[str] = None
    last_heartbeat: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'service_id': self.service_id,
            'service_name': self.service_name,
            'version': self.version,
            'host': self.host,
            'port': self.port,
            'status': self.status.value,
            'metadata': self.metadata,
            'health_check_url': self.health_check_url,
            'last_heartbeat': self.last_heartbeat.isoformat(),
            'tags': self.tags
        }
    
    @property
    def endpoint(self) -> str:
        """获取服务端点"""
        return f"http://{self.host}:{self.port}"
    
    def is_healthy(self, timeout_seconds: int = 30) -> bool:
        """检查服务是否健康"""
        if self.status != ServiceStatus.RUNNING:
            return False
        
        elapsed = datetime.now() - self.last_heartbeat
        return elapsed.total_seconds() < timeout_seconds


class ServiceRegistry:
    """服务注册中心"""
    
    def __init__(self):
        self.services: Dict[str, ServiceInfo] = {}
        self.service_names: Dict[str, List[str]] = defaultdict(list)
        self.health_check_interval = 10  # 秒
        self.health_checker_running = False
        self.health_checker_thread: Optional[threading.Thread] = None
        self.listeners: List[Callable[[str, ServiceInfo], None]] = []
    
    def start_health_checker(self) -> None:
        """启动健康检查"""
        if not self.health_checker_running:
            self.health_checker_running = True
            self.health_checker_thread = threading.Thread(
                target=self._health_check_loop, daemon=True
            )
            self.health_checker_thread.start()
            print("🏥 服务健康检查已启动")
    
    def stop_health_checker(self) -> None:
        """停止健康检查"""
        if self.health_checker_running:
            self.health_checker_running = False
            if self.health_checker_thread:
                self.health_checker_thread.join(timeout=1)
            print("🏥 服务健康检查已停止")
    
    def register_service(self, service_info: ServiceInfo) -> bool:
        """注册服务"""
        try:
            self.services[service_info.service_id] = service_info
            self.service_names[service_info.service_name].append(service_info.service_id)
            
            print(f"📝 服务已注册: {service_info.service_name} ({service_info.service_id})")
            
            # 通知监听器
            for listener in self.listeners:
                try:
                    listener('register', service_info)
                except Exception as e:
                    print(f"❌ 监听器错误: {str(e)}")
            
            return True
        except Exception as e:
            print(f"❌ 服务注册失败: {str(e)}")
            return False
    
    def deregister_service(self, service_id: str) -> bool:
        """注销服务"""
        try:
            if service_id in self.services:
                service_info = self.services[service_id]
                del self.services[service_id]
                
                # 从服务名称索引中移除
                if service_id in self.service_names[service_info.service_name]:
                    self.service_names[service_info.service_name].remove(service_id)
                    if not self.service_names[service_info.service_name]:
                        del self.service_names[service_info.service_name]
                
                print(f"🗑️ 服务已注销: {service_info.service_name} ({service_id})")
                
                # 通知监听器
                for listener in self.listeners:
                    try:
                        listener('deregister', service_info)
                    except Exception as e:
                        print(f"❌ 监听器错误: {str(e)}")
                
                return True
            return False
        except Exception as e:
            print(f"❌ 服务注销失败: {str(e)}")
            return False
    
    def discover_services(self, service_name: str, 
                         tags: Optional[List[str]] = None,
                         healthy_only: bool = True) -> List[ServiceInfo]:
        """发现服务"""
        services = []
        
        if service_name in self.service_names:
            for service_id in self.service_names[service_name]:
                if service_id in self.services:
                    service = self.services[service_id]
                    
                    # 检查健康状态
                    if healthy_only and not service.is_healthy():
                        continue
                    
                    # 检查标签
                    if tags:
                        if not all(tag in service.tags for tag in tags):
                            continue
                    
                    services.append(service)
        
        return services
    
    def get_service(self, service_id: str) -> Optional[ServiceInfo]:
        """获取特定服务"""
        return self.services.get(service_id)
    
    def update_heartbeat(self, service_id: str) -> bool:
        """更新心跳"""
        if service_id in self.services:
            self.services[service_id].last_heartbeat = datetime.now()
            if self.services[service_id].status == ServiceStatus.STARTING:
                self.services[service_id].status = ServiceStatus.RUNNING
            return True
        return False
    
    def add_listener(self, listener: Callable[[str, ServiceInfo], None]) -> None:
        """添加事件监听器"""
        self.listeners.append(listener)
    
    def _health_check_loop(self) -> None:
        """健康检查循环"""
        while self.health_checker_running:
            try:
                current_time = datetime.now()
                unhealthy_services = []
                
                for service_id, service in self.services.items():
                    if not service.is_healthy():
                        unhealthy_services.append(service_id)
                        print(f"⚠️ 服务不健康: {service.service_name} ({service_id})")
                
                # 移除不健康的服务
                for service_id in unhealthy_services:
                    self.deregister_service(service_id)
                
                time.sleep(self.health_check_interval)
            except Exception as e:
                print(f"❌ 健康检查错误: {str(e)}")
                time.sleep(1)
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        status_count = defaultdict(int)
        for service in self.services.values():
            status_count[service.status.value] += 1
        
        return {
            'total_services': len(self.services),
            'service_types': len(self.service_names),
            'status_distribution': dict(status_count),
            'healthy_services': sum(1 for s in self.services.values() if s.is_healthy())
        }


# ============================================================================
# 2. 负载均衡
# ============================================================================

class LoadBalancer(ABC):
    """负载均衡器接口"""
    
    @abstractmethod
    def select_service(self, services: List[ServiceInfo]) -> Optional[ServiceInfo]:
        """选择服务实例"""
        pass


class RoundRobinLoadBalancer(LoadBalancer):
    """轮询负载均衡器"""
    
    def __init__(self):
        self.counters: Dict[str, int] = defaultdict(int)
    
    def select_service(self, services: List[ServiceInfo]) -> Optional[ServiceInfo]:
        """轮询选择服务"""
        if not services:
            return None
        
        # 使用服务名作为轮询组
        service_name = services[0].service_name
        index = self.counters[service_name] % len(services)
        self.counters[service_name] += 1
        
        return services[index]


class RandomLoadBalancer(LoadBalancer):
    """随机负载均衡器"""
    
    def select_service(self, services: List[ServiceInfo]) -> Optional[ServiceInfo]:
        """随机选择服务"""
        if not services:
            return None
        
        import random
        return random.choice(services)


class WeightedLoadBalancer(LoadBalancer):
    """加权负载均衡器"""
    
    def select_service(self, services: List[ServiceInfo]) -> Optional[ServiceInfo]:
        """根据权重选择服务"""
        if not services:
            return None
        
        # 从元数据中获取权重，默认为1
        weights = [service.metadata.get('weight', 1) for service in services]
        total_weight = sum(weights)
        
        if total_weight == 0:
            return services[0]
        
        import random
        r = random.uniform(0, total_weight)
        
        current_weight = 0
        for i, weight in enumerate(weights):
            current_weight += weight
            if r <= current_weight:
                return services[i]
        
        return services[-1]


class LeastConnectionsLoadBalancer(LoadBalancer):
    """最少连接负载均衡器"""
    
    def __init__(self):
        self.connections: Dict[str, int] = defaultdict(int)
    
    def select_service(self, services: List[ServiceInfo]) -> Optional[ServiceInfo]:
        """选择连接数最少的服务"""
        if not services:
            return None
        
        # 找到连接数最少的服务
        min_connections = float('inf')
        selected_service = None
        
        for service in services:
            connections = self.connections[service.service_id]
            if connections < min_connections:
                min_connections = connections
                selected_service = service
        
        return selected_service
    
    def add_connection(self, service_id: str) -> None:
        """增加连接数"""
        self.connections[service_id] += 1
    
    def remove_connection(self, service_id: str) -> None:
        """减少连接数"""
        if self.connections[service_id] > 0:
            self.connections[service_id] -= 1


# ============================================================================
# 3. 服务网关
# ============================================================================

@dataclass
class Route:
    """路由配置"""
    path: str
    service_name: str
    method: str = "GET"
    strip_prefix: bool = False
    timeout: int = 30
    retry_count: int = 3
    circuit_breaker: bool = True
    rate_limit: Optional[int] = None  # 每秒请求数
    auth_required: bool = False
    middleware: List[str] = field(default_factory=list)


class CircuitBreaker:
    """熔断器"""
    
    def __init__(self, failure_threshold: int = 5, 
                 recovery_timeout: int = 60,
                 success_threshold: int = 3):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """执行调用"""
        if self.state == "OPEN":
            if self._should_attempt_reset():
                self.state = "HALF_OPEN"
                print(f"🔄 熔断器半开: 尝试恢复")
            else:
                raise Exception("熔断器开启，拒绝请求")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _should_attempt_reset(self) -> bool:
        """是否应该尝试重置"""
        if self.last_failure_time is None:
            return True
        
        elapsed = datetime.now() - self.last_failure_time
        return elapsed.total_seconds() >= self.recovery_timeout
    
    def _on_success(self) -> None:
        """成功回调"""
        if self.state == "HALF_OPEN":
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = "CLOSED"
                self.failure_count = 0
                self.success_count = 0
                print(f"✅ 熔断器关闭: 服务恢复正常")
        else:
            self.failure_count = 0
    
    def _on_failure(self) -> None:
        """失败回调"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.state == "HALF_OPEN":
            self.state = "OPEN"
            self.success_count = 0
            print(f"🔴 熔断器重新开启")
        elif self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            print(f"🔴 熔断器开启: 失败次数达到阈值 ({self.failure_count})")


class RateLimiter:
    """限流器"""
    
    def __init__(self, max_requests: int, window_seconds: int = 1):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: deque = deque()
    
    def is_allowed(self) -> bool:
        """检查是否允许请求"""
        now = datetime.now()
        
        # 清理过期的请求记录
        while self.requests and (now - self.requests[0]).total_seconds() > self.window_seconds:
            self.requests.popleft()
        
        # 检查是否超过限制
        if len(self.requests) >= self.max_requests:
            return False
        
        # 记录当前请求
        self.requests.append(now)
        return True


class ServiceGateway:
    """服务网关"""
    
    def __init__(self, service_registry: ServiceRegistry, 
                 load_balancer: LoadBalancer = None):
        self.service_registry = service_registry
        self.load_balancer = load_balancer or RoundRobinLoadBalancer()
        self.routes: Dict[str, Route] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.rate_limiters: Dict[str, RateLimiter] = {}
        self.middleware: Dict[str, Callable] = {}
        self.request_history: List[Dict[str, Any]] = []
    
    def add_route(self, route: Route) -> None:
        """添加路由"""
        self.routes[route.path] = route
        
        # 创建熔断器
        if route.circuit_breaker:
            self.circuit_breakers[route.path] = CircuitBreaker()
        
        # 创建限流器
        if route.rate_limit:
            self.rate_limiters[route.path] = RateLimiter(route.rate_limit)
        
        print(f"🛣️ 路由已添加: {route.path} -> {route.service_name}")
    
    def add_middleware(self, name: str, middleware: Callable) -> None:
        """添加中间件"""
        self.middleware[name] = middleware
        print(f"🔧 中间件已添加: {name}")
    
    def handle_request(self, path: str, method: str = "GET", 
                      headers: Dict[str, str] = None,
                      body: Any = None) -> Dict[str, Any]:
        """处理请求"""
        request_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        try:
            # 查找路由
            route = self._find_route(path)
            if not route:
                return self._error_response(404, "Route not found", request_id)
            
            # 检查方法
            if route.method != "*" and route.method != method:
                return self._error_response(405, "Method not allowed", request_id)
            
            # 限流检查
            if route.path in self.rate_limiters:
                if not self.rate_limiters[route.path].is_allowed():
                    return self._error_response(429, "Rate limit exceeded", request_id)
            
            # 认证检查
            if route.auth_required:
                if not self._check_auth(headers or {}):
                    return self._error_response(401, "Authentication required", request_id)
            
            # 应用中间件
            request_context = {
                'path': path,
                'method': method,
                'headers': headers or {},
                'body': body,
                'route': route
            }
            
            for middleware_name in route.middleware:
                if middleware_name in self.middleware:
                    request_context = self.middleware[middleware_name](request_context)
            
            # 服务发现
            services = self.service_registry.discover_services(route.service_name)
            if not services:
                return self._error_response(503, "Service unavailable", request_id)
            
            # 负载均衡
            selected_service = self.load_balancer.select_service(services)
            if not selected_service:
                return self._error_response(503, "No healthy service instance", request_id)
            
            # 执行请求（使用熔断器）
            response = None
            if route.circuit_breaker and route.path in self.circuit_breakers:
                circuit_breaker = self.circuit_breakers[route.path]
                response = circuit_breaker.call(
                    self._make_service_call,
                    selected_service, path, method, headers, body, route
                )
            else:
                response = self._make_service_call(
                    selected_service, path, method, headers, body, route
                )
            
            # 记录请求
            self._log_request(request_id, path, method, selected_service, 
                            start_time, response.get('status', 200))
            
            return response
            
        except Exception as e:
            error_response = self._error_response(500, str(e), request_id)
            self._log_request(request_id, path, method, None, start_time, 500)
            return error_response
    
    def _find_route(self, path: str) -> Optional[Route]:
        """查找路由"""
        # 精确匹配
        if path in self.routes:
            return self.routes[path]
        
        # 前缀匹配
        for route_path, route in self.routes.items():
            if path.startswith(route_path.rstrip('*')):
                return route
        
        return None
    
    def _check_auth(self, headers: Dict[str, str]) -> bool:
        """检查认证"""
        # 简单的认证检查
        auth_header = headers.get('Authorization', '')
        return auth_header.startswith('Bearer ') and len(auth_header) > 7
    
    def _make_service_call(self, service: ServiceInfo, path: str, method: str,
                          headers: Dict[str, str], body: Any, route: Route) -> Dict[str, Any]:
        """调用服务（模拟）"""
        # 模拟网络延迟
        import random
        delay = random.uniform(0.01, 0.1)
        time.sleep(delay)
        
        # 模拟偶尔的失败
        if random.random() < 0.05:  # 5% 失败率
            raise Exception("Service call failed")
        
        # 构建目标路径
        target_path = path
        if route.strip_prefix and path.startswith(route.path.rstrip('*')):
            prefix = route.path.rstrip('*')
            target_path = path[len(prefix):] or '/'
        
        # 模拟成功响应
        return {
            'status': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': {
                'message': f'Response from {service.service_name}',
                'service_id': service.service_id,
                'path': target_path,
                'method': method,
                'timestamp': datetime.now().isoformat()
            }
        }
    
    def _error_response(self, status: int, message: str, request_id: str) -> Dict[str, Any]:
        """创建错误响应"""
        return {
            'status': status,
            'headers': {'Content-Type': 'application/json'},
            'body': {
                'error': message,
                'request_id': request_id,
                'timestamp': datetime.now().isoformat()
            }
        }
    
    def _log_request(self, request_id: str, path: str, method: str,
                    service: Optional[ServiceInfo], start_time: datetime, status: int) -> None:
        """记录请求日志"""
        duration = (datetime.now() - start_time).total_seconds() * 1000  # 毫秒
        
        log_entry = {
            'request_id': request_id,
            'path': path,
            'method': method,
            'service_id': service.service_id if service else None,
            'service_name': service.service_name if service else None,
            'status': status,
            'duration_ms': round(duration, 2),
            'timestamp': start_time.isoformat()
        }
        
        self.request_history.append(log_entry)
        
        # 保持最近1000条记录
        if len(self.request_history) > 1000:
            self.request_history = self.request_history[-1000:]
        
        print(f"📊 {method} {path} -> {status} ({duration:.1f}ms)")
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取网关统计信息"""
        if not self.request_history:
            return {'total_requests': 0}
        
        total_requests = len(self.request_history)
        status_codes = defaultdict(int)
        total_duration = 0
        
        for entry in self.request_history:
            status_codes[entry['status']] += 1
            total_duration += entry['duration_ms']
        
        avg_duration = total_duration / total_requests if total_requests > 0 else 0
        
        return {
            'total_requests': total_requests,
            'status_distribution': dict(status_codes),
            'average_duration_ms': round(avg_duration, 2),
            'success_rate': round((status_codes.get(200, 0) / total_requests) * 100, 2),
            'routes_count': len(self.routes),
            'circuit_breakers': {path: cb.state for path, cb in self.circuit_breakers.items()}
        }


# ============================================================================
# 4. 微服务基类
# ============================================================================

class MicroService:
    """微服务基类"""
    
    def __init__(self, service_name: str, version: str = "1.0.0",
                 host: str = "localhost", port: int = 8080):
        self.service_info = ServiceInfo(
            service_id=f"{service_name}-{uuid.uuid4().hex[:8]}",
            service_name=service_name,
            version=version,
            host=host,
            port=port
        )
        self.registry: Optional[ServiceRegistry] = None
        self.running = False
        self.heartbeat_thread: Optional[threading.Thread] = None
        self.heartbeat_interval = 10  # 秒
    
    def register_to_registry(self, registry: ServiceRegistry) -> None:
        """注册到服务注册中心"""
        self.registry = registry
        self.registry.register_service(self.service_info)
    
    def start(self) -> None:
        """启动服务"""
        if not self.running:
            self.running = True
            self.service_info.status = ServiceStatus.RUNNING
            
            # 启动心跳
            if self.registry:
                self.heartbeat_thread = threading.Thread(
                    target=self._heartbeat_loop, daemon=True
                )
                self.heartbeat_thread.start()
            
            print(f"🚀 服务已启动: {self.service_info.service_name} ({self.service_info.service_id})")
    
    def stop(self) -> None:
        """停止服务"""
        if self.running:
            self.running = False
            self.service_info.status = ServiceStatus.STOPPING
            
            # 停止心跳
            if self.heartbeat_thread:
                self.heartbeat_thread.join(timeout=1)
            
            # 从注册中心注销
            if self.registry:
                self.registry.deregister_service(self.service_info.service_id)
            
            self.service_info.status = ServiceStatus.STOPPED
            print(f"🛑 服务已停止: {self.service_info.service_name} ({self.service_info.service_id})")
    
    def _heartbeat_loop(self) -> None:
        """心跳循环"""
        while self.running:
            try:
                if self.registry:
                    self.registry.update_heartbeat(self.service_info.service_id)
                time.sleep(self.heartbeat_interval)
            except Exception as e:
                print(f"❌ 心跳错误: {str(e)}")
                time.sleep(1)
    
    def add_tag(self, tag: str) -> None:
        """添加标签"""
        if tag not in self.service_info.tags:
            self.service_info.tags.append(tag)
    
    def set_metadata(self, key: str, value: Any) -> None:
        """设置元数据"""
        self.service_info.metadata[key] = value


# ============================================================================
# 5. 具体微服务实现
# ============================================================================

class UserService(MicroService):
    """用户服务"""
    
    def __init__(self, host: str = "localhost", port: int = 8081):
        super().__init__("user-service", "1.0.0", host, port)
        self.users: Dict[str, Dict[str, Any]] = {}
        self.add_tag("business")
        self.add_tag("user-management")
        self.set_metadata("weight", 2)
    
    def create_user(self, username: str, email: str) -> Dict[str, Any]:
        """创建用户"""
        user_id = str(uuid.uuid4())
        user = {
            'id': user_id,
            'username': username,
            'email': email,
            'created_at': datetime.now().isoformat()
        }
        self.users[user_id] = user
        print(f"👤 用户已创建: {username} ({user_id})")
        return user
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """获取用户"""
        return self.users.get(user_id)
    
    def list_users(self) -> List[Dict[str, Any]]:
        """列出所有用户"""
        return list(self.users.values())


class OrderService(MicroService):
    """订单服务"""
    
    def __init__(self, host: str = "localhost", port: int = 8082):
        super().__init__("order-service", "1.0.0", host, port)
        self.orders: Dict[str, Dict[str, Any]] = {}
        self.add_tag("business")
        self.add_tag("order-management")
        self.set_metadata("weight", 3)
    
    def create_order(self, user_id: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """创建订单"""
        order_id = f"ORDER-{uuid.uuid4().hex[:8].upper()}"
        total = sum(item.get('price', 0) * item.get('quantity', 1) for item in items)
        
        order = {
            'id': order_id,
            'user_id': user_id,
            'items': items,
            'total': total,
            'status': 'created',
            'created_at': datetime.now().isoformat()
        }
        self.orders[order_id] = order
        print(f"📦 订单已创建: {order_id} (总额: ${total})")
        return order
    
    def get_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        """获取订单"""
        return self.orders.get(order_id)
    
    def list_orders(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出订单"""
        if user_id:
            return [order for order in self.orders.values() if order['user_id'] == user_id]
        return list(self.orders.values())


class PaymentService(MicroService):
    """支付服务"""
    
    def __init__(self, host: str = "localhost", port: int = 8083):
        super().__init__("payment-service", "1.0.0", host, port)
        self.payments: Dict[str, Dict[str, Any]] = {}
        self.add_tag("business")
        self.add_tag("payment")
        self.set_metadata("weight", 1)
    
    def process_payment(self, order_id: str, amount: float, method: str = "credit_card") -> Dict[str, Any]:
        """处理支付"""
        payment_id = f"PAY-{uuid.uuid4().hex[:8].upper()}"
        
        # 模拟支付处理
        import random
        success = random.random() > 0.1  # 90% 成功率
        
        payment = {
            'id': payment_id,
            'order_id': order_id,
            'amount': amount,
            'method': method,
            'status': 'success' if success else 'failed',
            'processed_at': datetime.now().isoformat()
        }
        
        self.payments[payment_id] = payment
        
        if success:
            print(f"💳 支付成功: {payment_id} (${amount})")
        else:
            print(f"❌ 支付失败: {payment_id} (${amount})")
        
        return payment
    
    def get_payment(self, payment_id: str) -> Optional[Dict[str, Any]]:
        """获取支付信息"""
        return self.payments.get(payment_id)


# ============================================================================
# 6. 演示函数
# ============================================================================

def demo_microservice_architecture():
    """演示微服务架构"""
    print("微服务架构演示")
    print("=" * 50)
    
    # 1. 创建服务注册中心
    print("\n1. 创建服务注册中心")
    registry = ServiceRegistry()
    registry.start_health_checker()
    
    # 2. 创建微服务实例
    print("\n2. 创建微服务实例")
    user_service1 = UserService(port=8081)
    user_service2 = UserService(port=8082)  # 用户服务的第二个实例
    order_service = OrderService(port=8083)
    payment_service = PaymentService(port=8084)
    
    # 注册服务
    services = [user_service1, user_service2, order_service, payment_service]
    for service in services:
        service.register_to_registry(registry)
        service.start()
    
    time.sleep(1)  # 等待服务启动
    
    # 3. 创建服务网关
    print("\n3. 创建服务网关")
    
    # 使用不同的负载均衡策略
    load_balancer = WeightedLoadBalancer()
    gateway = ServiceGateway(registry, load_balancer)
    
    # 添加路由
    gateway.add_route(Route(
        path="/api/users/*",
        service_name="user-service",
        method="*",
        strip_prefix=True,
        rate_limit=10,  # 每秒10个请求
        middleware=["logging", "auth"]
    ))
    
    gateway.add_route(Route(
        path="/api/orders/*",
        service_name="order-service",
        method="*",
        strip_prefix=True,
        rate_limit=5,
        auth_required=True
    ))
    
    gateway.add_route(Route(
        path="/api/payments/*",
        service_name="payment-service",
        method="*",
        strip_prefix=True,
        circuit_breaker=True
    ))
    
    # 添加中间件
    def logging_middleware(context):
        print(f"🔍 请求日志: {context['method']} {context['path']}")
        return context
    
    def auth_middleware(context):
        # 模拟认证
        context['headers']['Authorization'] = 'Bearer valid-token'
        print(f"🔐 认证中间件: 已添加认证头")
        return context
    
    gateway.add_middleware("logging", logging_middleware)
    gateway.add_middleware("auth", auth_middleware)
    
    # 4. 演示服务发现
    print("\n4. 演示服务发现")
    user_services = registry.discover_services("user-service")
    print(f"🔍 发现用户服务实例: {len(user_services)}")
    for service in user_services:
        print(f"   - {service.service_id} @ {service.endpoint} (权重: {service.metadata.get('weight', 1)})")
    
    # 5. 演示负载均衡
    print("\n5. 演示负载均衡")
    print("发送多个请求观察负载均衡效果:")
    
    for i in range(6):
        response = gateway.handle_request(
            path="/api/users/list",
            method="GET",
            headers={"User-Agent": "Demo Client"}
        )
        
        if response['status'] == 200:
            service_id = response['body']['service_id']
            print(f"   请求 {i+1}: 路由到 {service_id}")
        else:
            print(f"   请求 {i+1}: 失败 - {response['body']['error']}")
        
        time.sleep(0.1)
    
    # 6. 演示限流
    print("\n6. 演示限流")
    print("快速发送请求触发限流:")
    
    for i in range(15):
        response = gateway.handle_request(
            path="/api/orders/list",
            method="GET",
            headers={"Authorization": "Bearer valid-token"}
        )
        
        if response['status'] == 429:
            print(f"   请求 {i+1}: 被限流")
            break
        else:
            print(f"   请求 {i+1}: 成功")
    
    # 7. 演示熔断器
    print("\n7. 演示熔断器")
    print("模拟服务故障触发熔断:")
    
    # 停止支付服务模拟故障
    payment_service.stop()
    time.sleep(1)
    
    # 发送请求触发熔断
    for i in range(8):
        try:
            response = gateway.handle_request(
                path="/api/payments/process",
                method="POST"
            )
            print(f"   请求 {i+1}: 状态 {response['status']}")
        except Exception as e:
            print(f"   请求 {i+1}: 异常 - {str(e)}")
        
        time.sleep(0.1)
    
    # 8. 显示统计信息
    print("\n8. 统计信息")
    
    print("\n服务注册中心统计:")
    registry_stats = registry.get_statistics()
    for key, value in registry_stats.items():
        print(f"   {key}: {value}")
    
    print("\n网关统计:")
    gateway_stats = gateway.get_statistics()
    for key, value in gateway_stats.items():
        print(f"   {key}: {value}")
    
    # 9. 清理资源
    print("\n9. 清理资源")
    
    # 停止所有服务
    for service in services:
        if service.running:
            service.stop()
    
    # 停止注册中心
    registry.stop_health_checker()
    
    print("\n演示完成！")


def demo_service_mesh():
    """演示服务网格概念"""
    print("\n服务网格概念演示")
    print("=" * 50)
    
    # 服务网格是微服务架构的进一步发展
    # 这里演示一些核心概念
    
    class ServiceMesh:
        """简化的服务网格实现"""
        
        def __init__(self):
            self.services: Dict[str, MicroService] = {}
            self.traffic_policies: Dict[str, Dict[str, Any]] = {}
            self.security_policies: Dict[str, Dict[str, Any]] = {}
            self.observability_data: List[Dict[str, Any]] = []
        
        def register_service(self, service: MicroService) -> None:
            """注册服务到网格"""
            self.services[service.service_info.service_id] = service
            print(f"🕸️ 服务已加入网格: {service.service_info.service_name}")
        
        def set_traffic_policy(self, service_name: str, policy: Dict[str, Any]) -> None:
            """设置流量策略"""
            self.traffic_policies[service_name] = policy
            print(f"🚦 流量策略已设置: {service_name}")
        
        def set_security_policy(self, service_name: str, policy: Dict[str, Any]) -> None:
            """设置安全策略"""
            self.security_policies[service_name] = policy
            print(f"🔒 安全策略已设置: {service_name}")
        
        def intercept_call(self, from_service: str, to_service: str, 
                          request: Dict[str, Any]) -> Dict[str, Any]:
            """拦截服务调用"""
            # 记录可观测性数据
            call_data = {
                'from': from_service,
                'to': to_service,
                'timestamp': datetime.now().isoformat(),
                'request_id': str(uuid.uuid4())
            }
            self.observability_data.append(call_data)
            
            # 应用安全策略
            if to_service in self.security_policies:
                policy = self.security_policies[to_service]
                if policy.get('require_mtls', False):
                    print(f"🔐 mTLS验证: {from_service} -> {to_service}")
            
            # 应用流量策略
            if to_service in self.traffic_policies:
                policy = self.traffic_policies[to_service]
                if 'retry' in policy:
                    print(f"🔄 重试策略: {policy['retry']}")
                if 'timeout' in policy:
                    print(f"⏱️ 超时策略: {policy['timeout']}s")
            
            print(f"🕸️ 网格拦截: {from_service} -> {to_service}")
            
            # 模拟调用
            return {
                'status': 'success',
                'data': f'Response from {to_service}',
                'call_id': call_data['request_id']
            }
    
    # 创建服务网格
    mesh = ServiceMesh()
    
    # 创建服务
    user_service = UserService()
    order_service = OrderService()
    
    # 注册到网格
    mesh.register_service(user_service)
    mesh.register_service(order_service)
    
    # 设置策略
    mesh.set_traffic_policy("user-service", {
        'retry': {'attempts': 3, 'backoff': '1s'},
        'timeout': 30,
        'circuit_breaker': {'threshold': 5}
    })
    
    mesh.set_security_policy("order-service", {
        'require_mtls': True,
        'allowed_sources': ['user-service'],
        'rate_limit': 100
    })
    
    # 模拟服务间调用
    print("\n模拟服务间调用:")
    for i in range(3):
        response = mesh.intercept_call(
            "user-service", 
            "order-service", 
            {'action': 'create_order', 'user_id': f'user-{i}'}
        )
        print(f"   调用 {i+1}: {response['status']}")
    
    print(f"\n📊 网格可观测性数据: {len(mesh.observability_data)} 条记录")
    
    print("\n服务网格演示完成！")


if __name__ == "__main__":
    # 微服务架构演示
    demo_microservice_architecture()
    
    # 服务网格演示
    demo_service_mesh()