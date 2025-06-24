#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习2解决方案: RESTful API架构实现

这是exercise_02.py的完整实现示例，展示了如何设计和实现
一个完整的RESTful API系统。
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import json
import hashlib
import time
import re
from functools import wraps

# ============================================================================
# 数据模型 (Data Models) - 重用exercise_02.py中的定义
# ============================================================================

class ProductStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    OUT_OF_STOCK = "out_of_stock"

class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class PaymentStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

@dataclass
class Product:
    id: int
    name: str
    description: str
    price: float
    category: str
    stock: int
    status: ProductStatus
    images: List[str]
    created_at: datetime
    updated_at: datetime

@dataclass
class User:
    id: int
    username: str
    email: str
    password_hash: str
    full_name: str
    phone: str
    address: str
    created_at: datetime
    last_login: Optional[datetime]

@dataclass
class OrderItem:
    product_id: int
    quantity: int
    price: float

@dataclass
class Order:
    id: int
    user_id: int
    items: List[OrderItem]
    total_amount: float
    status: OrderStatus
    shipping_address: str
    created_at: datetime
    updated_at: datetime

@dataclass
class CartItem:
    product_id: int
    quantity: int
    added_at: datetime

@dataclass
class Cart:
    user_id: int
    items: List[CartItem]
    updated_at: datetime

@dataclass
class Payment:
    id: int
    order_id: int
    amount: float
    method: str
    status: PaymentStatus
    transaction_id: str
    created_at: datetime

@dataclass
class HTTPRequest:
    method: str
    path: str
    headers: Dict[str, str]
    query_params: Dict[str, str]
    body: Optional[str]
    user_id: Optional[int] = None
    path_params: Dict[str, str] = None

    def __post_init__(self):
        if self.path_params is None:
            self.path_params = {}

@dataclass
class HTTPResponse:
    status_code: int
    headers: Dict[str, str]
    body: str

@dataclass
class APIResponse:
    success: bool
    data: Any
    message: str
    timestamp: datetime
    pagination: Optional[Dict[str, Any]] = None

# ============================================================================
# 中间件实现 (Middleware Implementation)
# ============================================================================

class IMiddleware(ABC):
    @abstractmethod
    def process_request(self, request: HTTPRequest) -> Optional[HTTPResponse]:
        pass
    
    @abstractmethod
    def process_response(self, request: HTTPRequest, response: HTTPResponse) -> HTTPResponse:
        pass

class JWTAuthMiddleware(IMiddleware):
    """JWT认证中间件"""
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.public_paths = [
            '/api/v1/auth/register',
            '/api/v1/auth/login',
            '/api/v1/products'  # 商品列表允许匿名访问
        ]
    
    def process_request(self, request: HTTPRequest) -> Optional[HTTPResponse]:
        # 检查是否为公开路径
        if any(request.path.startswith(path) for path in self.public_paths):
            return None
        
        # 检查Authorization头
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return HTTPResponse(
                status_code=401,
                headers={'Content-Type': 'application/json'},
                body=json.dumps({
                    'success': False,
                    'message': '缺少认证令牌',
                    'timestamp': datetime.now().isoformat()
                })
            )
        
        # 验证JWT令牌（简化实现）
        token = auth_header[7:]  # 移除 'Bearer ' 前缀
        user_id = self._verify_token(token)
        
        if user_id is None:
            return HTTPResponse(
                status_code=401,
                headers={'Content-Type': 'application/json'},
                body=json.dumps({
                    'success': False,
                    'message': '无效的认证令牌',
                    'timestamp': datetime.now().isoformat()
                })
            )
        
        # 将用户ID添加到请求中
        request.user_id = user_id
        return None
    
    def process_response(self, request: HTTPRequest, response: HTTPResponse) -> HTTPResponse:
        return response
    
    def _verify_token(self, token: str) -> Optional[int]:
        """验证JWT令牌（简化实现）"""
        try:
            # 简化的JWT验证，实际应用中应使用专业的JWT库
            # 这里假设token格式为 "user_id.timestamp.signature"
            parts = token.split('.')
            if len(parts) != 3:
                return None
            
            user_id = int(parts[0])
            timestamp = int(parts[1])
            signature = parts[2]
            
            # 验证签名
            expected_signature = hashlib.sha256(
                f"{user_id}.{timestamp}.{self.secret_key}".encode()
            ).hexdigest()[:16]
            
            if signature != expected_signature:
                return None
            
            # 检查令牌是否过期（24小时）
            if time.time() - timestamp > 24 * 3600:
                return None
            
            return user_id
        except (ValueError, IndexError):
            return None
    
    def generate_token(self, user_id: int) -> str:
        """生成JWT令牌（简化实现）"""
        timestamp = int(time.time())
        signature = hashlib.sha256(
            f"{user_id}.{timestamp}.{self.secret_key}".encode()
        ).hexdigest()[:16]
        return f"{user_id}.{timestamp}.{signature}"

class LoggingMiddleware(IMiddleware):
    """日志中间件"""
    def process_request(self, request: HTTPRequest) -> Optional[HTTPResponse]:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {request.method} {request.path}")
        if request.query_params:
            print(f"  Query: {request.query_params}")
        if request.user_id:
            print(f"  User: {request.user_id}")
        return None
    
    def process_response(self, request: HTTPRequest, response: HTTPResponse) -> HTTPResponse:
        print(f"  Response: {response.status_code}")
        return response

class RateLimitMiddleware(IMiddleware):
    """限流中间件"""
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[float]] = {}
    
    def process_request(self, request: HTTPRequest) -> Optional[HTTPResponse]:
        # 使用IP地址作为限流键（简化实现）
        client_ip = request.headers.get('X-Real-IP', '127.0.0.1')
        current_time = time.time()
        
        # 清理过期的请求记录
        if client_ip in self.requests:
            self.requests[client_ip] = [
                req_time for req_time in self.requests[client_ip]
                if current_time - req_time < self.window_seconds
            ]
        else:
            self.requests[client_ip] = []
        
        # 检查请求频率
        if len(self.requests[client_ip]) >= self.max_requests:
            return HTTPResponse(
                status_code=429,
                headers={
                    'Content-Type': 'application/json',
                    'Retry-After': str(self.window_seconds)
                },
                body=json.dumps({
                    'success': False,
                    'message': '请求频率过高，请稍后再试',
                    'timestamp': datetime.now().isoformat()
                })
            )
        
        # 记录当前请求
        self.requests[client_ip].append(current_time)
        return None
    
    def process_response(self, request: HTTPRequest, response: HTTPResponse) -> HTTPResponse:
        return response

class CORSMiddleware(IMiddleware):
    """跨域中间件"""
    def process_request(self, request: HTTPRequest) -> Optional[HTTPResponse]:
        # 处理OPTIONS预检请求
        if request.method == 'OPTIONS':
            return HTTPResponse(
                status_code=200,
                headers={
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                    'Access-Control-Max-Age': '86400'
                },
                body=''
            )
        return None
    
    def process_response(self, request: HTTPRequest, response: HTTPResponse) -> HTTPResponse:
        # 添加CORS响应头
        response.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        })
        return response

# ============================================================================
# 路由器实现 (Router Implementation)
# ============================================================================

class Route:
    def __init__(self, method: str, path: str, handler: Callable, middlewares: List[IMiddleware] = None):
        self.method = method
        self.path = path
        self.handler = handler
        self.middlewares = middlewares or []
        self.path_pattern = self._compile_path_pattern(path)
    
    def _compile_path_pattern(self, path: str) -> re.Pattern:
        """编译路径模式，支持路径参数"""
        # 将 {id} 转换为正则表达式组
        pattern = re.sub(r'\{(\w+)\}', r'(?P<\1>[^/]+)', path)
        pattern = f"^{pattern}$"
        return re.compile(pattern)
    
    def match(self, method: str, path: str) -> Tuple[bool, Dict[str, str]]:
        """匹配路由并提取路径参数"""
        if self.method != method:
            return False, {}
        
        match = self.path_pattern.match(path)
        if match:
            return True, match.groupdict()
        return False, {}

class Router:
    def __init__(self):
        self.routes: List[Route] = []
        self.global_middlewares: List[IMiddleware] = []
    
    def add_route(self, method: str, path: str, handler: Callable, middlewares: List[IMiddleware] = None):
        route = Route(method, path, handler, middlewares)
        self.routes.append(route)
    
    def add_middleware(self, middleware: IMiddleware):
        self.global_middlewares.append(middleware)
    
    def match_route(self, method: str, path: str) -> Optional[Tuple[Route, Dict[str, str]]]:
        for route in self.routes:
            matched, path_params = route.match(method, path)
            if matched:
                return route, path_params
        return None
    
    def handle_request(self, request: HTTPRequest) -> HTTPResponse:
        try:
            # 匹配路由
            route_match = self.match_route(request.method, request.path)
            if not route_match:
                return HTTPResponse(
                    status_code=404,
                    headers={'Content-Type': 'application/json'},
                    body=json.dumps({
                        'success': False,
                        'message': '路由不存在',
                        'timestamp': datetime.now().isoformat()
                    })
                )
            
            route, path_params = route_match
            request.path_params = path_params
            
            # 执行全局中间件
            for middleware in self.global_middlewares:
                response = middleware.process_request(request)
                if response:
                    return response
            
            # 执行路由特定中间件
            for middleware in route.middlewares:
                response = middleware.process_request(request)
                if response:
                    return response
            
            # 调用处理器
            response = route.handler(request)
            
            # 执行响应中间件（逆序）
            for middleware in reversed(route.middlewares + self.global_middlewares):
                response = middleware.process_response(request, response)
            
            return response
            
        except Exception as e:
            # 全局异常处理
            return HTTPResponse(
                status_code=500,
                headers={'Content-Type': 'application/json'},
                body=json.dumps({
                    'success': False,
                    'message': f'服务器内部错误: {str(e)}',
                    'timestamp': datetime.now().isoformat()
                })
            )

# ============================================================================
# 数据存储层 (Data Storage Layer)
# ============================================================================

class DataStore:
    """简单的内存数据存储"""
    def __init__(self):
        self.products: Dict[int, Product] = {}
        self.users: Dict[int, User] = {}
        self.orders: Dict[int, Order] = {}
        self.carts: Dict[int, Cart] = {}
        self.payments: Dict[int, Payment] = {}
        
        self.next_product_id = 1
        self.next_user_id = 1
        self.next_order_id = 1
        self.next_payment_id = 1
    
    def create_product(self, product_data: Dict[str, Any]) -> Product:
        product = Product(
            id=self.next_product_id,
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            category=product_data['category'],
            stock=product_data['stock'],
            status=ProductStatus.ACTIVE,
            images=product_data.get('images', []),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.products[product.id] = product
        self.next_product_id += 1
        return product
    
    def create_user(self, user_data: Dict[str, Any]) -> User:
        user = User(
            id=self.next_user_id,
            username=user_data['username'],
            email=user_data['email'],
            password_hash=user_data['password_hash'],
            full_name=user_data['full_name'],
            phone=user_data['phone'],
            address=user_data.get('address', ''),
            created_at=datetime.now(),
            last_login=None
        )
        self.users[user.id] = user
        self.next_user_id += 1
        return user
    
    def create_order(self, order_data: Dict[str, Any]) -> Order:
        order = Order(
            id=self.next_order_id,
            user_id=order_data['user_id'],
            items=[OrderItem(**item) for item in order_data['items']],
            total_amount=order_data['total_amount'],
            status=OrderStatus.PENDING,
            shipping_address=order_data['shipping_address'],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.orders[order.id] = order
        self.next_order_id += 1
        return order
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        for user in self.users.values():
            if user.username == username:
                return user
        return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        for user in self.users.values():
            if user.email == email:
                return user
        return None
    
    def search_products(self, keyword: str = None, category: str = None, 
                      page: int = 1, limit: int = 20) -> Tuple[List[Product], int]:
        products = list(self.products.values())
        
        # 过滤
        if keyword:
            keyword = keyword.lower()
            products = [p for p in products if keyword in p.name.lower() or keyword in p.description.lower()]
        
        if category:
            products = [p for p in products if p.category == category]
        
        # 分页
        total = len(products)
        start = (page - 1) * limit
        end = start + limit
        products = products[start:end]
        
        return products, total

# ============================================================================
# 控制器实现 (Controller Implementation)
# ============================================================================

class ProductController:
    def __init__(self, data_store: DataStore, auth_middleware: JWTAuthMiddleware):
        self.data_store = data_store
        self.auth_middleware = auth_middleware
    
    def get_products(self, request: HTTPRequest) -> HTTPResponse:
        try:
            # 解析查询参数
            keyword = request.query_params.get('keyword')
            category = request.query_params.get('category')
            page = int(request.query_params.get('page', 1))
            limit = int(request.query_params.get('limit', 20))
            
            # 搜索商品
            products, total = self.data_store.search_products(keyword, category, page, limit)
            
            # 构建响应
            response_data = {
                'success': True,
                'data': [
                    {
                        'id': p.id,
                        'name': p.name,
                        'description': p.description,
                        'price': p.price,
                        'category': p.category,
                        'stock': p.stock,
                        'status': p.status.value,
                        'images': p.images
                    } for p in products
                ],
                'message': f'找到 {len(products)} 个商品',
                'timestamp': datetime.now().isoformat(),
                'pagination': {
                    'page': page,
                    'limit': limit,
                    'total': total,
                    'pages': (total + limit - 1) // limit
                }
            }
            
            return HTTPResponse(
                status_code=200,
                headers={'Content-Type': 'application/json'},
                body=json.dumps(response_data, ensure_ascii=False)
            )
            
        except Exception as e:
            return HTTPResponse(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body=json.dumps({
                    'success': False,
                    'message': f'请求参数错误: {str(e)}',
                    'timestamp': datetime.now().isoformat()
                })
            )
    
    def get_product(self, request: HTTPRequest) -> HTTPResponse:
        try:
            product_id = int(request.path_params['id'])
            product = self.data_store.products.get(product_id)
            
            if not product:
                return HTTPResponse(
                    status_code=404,
                    headers={'Content-Type': 'application/json'},
                    body=json.dumps({
                        'success': False,
                        'message': '商品不存在',
                        'timestamp': datetime.now().isoformat()
                    })
                )
            
            response_data = {
                'success': True,
                'data': {
                    'id': product.id,
                    'name': product.name,
                    'description': product.description,
                    'price': product.price,
                    'category': product.category,
                    'stock': product.stock,
                    'status': product.status.value,
                    'images': product.images,
                    'created_at': product.created_at.isoformat(),
                    'updated_at': product.updated_at.isoformat()
                },
                'message': '获取商品成功',
                'timestamp': datetime.now().isoformat()
            }
            
            return HTTPResponse(
                status_code=200,
                headers={'Content-Type': 'application/json'},
                body=json.dumps(response_data, ensure_ascii=False)
            )
            
        except ValueError:
            return HTTPResponse(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body=json.dumps({
                    'success': False,
                    'message': '无效的商品ID',
                    'timestamp': datetime.now().isoformat()
                })
            )
    
    def create_product(self, request: HTTPRequest) -> HTTPResponse:
        try:
            if not request.body:
                raise ValueError("请求体不能为空")
            
            product_data = json.loads(request.body)
            
            # 验证必需字段
            required_fields = ['name', 'description', 'price', 'category', 'stock']
            for field in required_fields:
                if field not in product_data:
                    raise ValueError(f"缺少必需字段: {field}")
            
            # 创建商品
            product = self.data_store.create_product(product_data)
            
            response_data = {
                'success': True,
                'data': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'category': product.category,
                    'status': product.status.value
                },
                'message': '商品创建成功',
                'timestamp': datetime.now().isoformat()
            }
            
            return HTTPResponse(
                status_code=201,
                headers={'Content-Type': 'application/json'},
                body=json.dumps(response_data, ensure_ascii=False)
            )
            
        except (json.JSONDecodeError, ValueError) as e:
            return HTTPResponse(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body=json.dumps({
                    'success': False,
                    'message': f'请求数据错误: {str(e)}',
                    'timestamp': datetime.now().isoformat()
                })
            )
    
    def update_product(self, request: HTTPRequest) -> HTTPResponse:
        try:
            product_id = int(request.path_params['id'])
            product = self.data_store.products.get(product_id)
            
            if not product:
                return HTTPResponse(
                    status_code=404,
                    headers={'Content-Type': 'application/json'},
                    body=json.dumps({
                        'success': False,
                        'message': '商品不存在',
                        'timestamp': datetime.now().isoformat()
                    })
                )
            
            if not request.body:
                raise ValueError("请求体不能为空")
            
            update_data = json.loads(request.body)
            
            # 更新商品字段
            for field in ['name', 'description', 'price', 'category', 'stock', 'status']:
                if field in update_data:
                    if field == 'status':
                        setattr(product, field, ProductStatus(update_data[field]))
                    else:
                        setattr(product, field, update_data[field])
            
            product.updated_at = datetime.now()
            
            response_data = {
                'success': True,
                'data': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'status': product.status.value
                },
                'message': '商品更新成功',
                'timestamp': datetime.now().isoformat()
            }
            
            return HTTPResponse(
                status_code=200,
                headers={'Content-Type': 'application/json'},
                body=json.dumps(response_data, ensure_ascii=False)
            )
            
        except (ValueError, json.JSONDecodeError) as e:
            return HTTPResponse(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body=json.dumps({
                    'success': False,
                    'message': f'请求数据错误: {str(e)}',
                    'timestamp': datetime.now().isoformat()
                })
            )
    
    def delete_product(self, request: HTTPRequest) -> HTTPResponse:
        try:
            product_id = int(request.path_params['id'])
            
            if product_id not in self.data_store.products:
                return HTTPResponse(
                    status_code=404,
                    headers={'Content-Type': 'application/json'},
                    body=json.dumps({
                        'success': False,
                        'message': '商品不存在',
                        'timestamp': datetime.now().isoformat()
                    })
                )
            
            del self.data_store.products[product_id]
            
            return HTTPResponse(
                status_code=204,
                headers={'Content-Type': 'application/json'},
                body=''
            )
            
        except ValueError:
            return HTTPResponse(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body=json.dumps({
                    'success': False,
                    'message': '无效的商品ID',
                    'timestamp': datetime.now().isoformat()
                })
            )

class UserController:
    def __init__(self, data_store: DataStore, auth_middleware: JWTAuthMiddleware):
        self.data_store = data_store
        self.auth_middleware = auth_middleware
    
    def register(self, request: HTTPRequest) -> HTTPResponse:
        try:
            if not request.body:
                raise ValueError("请求体不能为空")
            
            user_data = json.loads(request.body)
            
            # 验证必需字段
            required_fields = ['username', 'email', 'password', 'full_name', 'phone']
            for field in required_fields:
                if field not in user_data:
                    raise ValueError(f"缺少必需字段: {field}")
            
            # 检查用户名和邮箱是否已存在
            if self.data_store.get_user_by_username(user_data['username']):
                raise ValueError("用户名已存在")
            
            if self.data_store.get_user_by_email(user_data['email']):
                raise ValueError("邮箱已存在")
            
            # 密码哈希
            password_hash = hashlib.sha256(user_data['password'].encode()).hexdigest()
            user_data['password_hash'] = password_hash
            del user_data['password']
            
            # 创建用户
            user = self.data_store.create_user(user_data)
            
            response_data = {
                'success': True,
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'full_name': user.full_name
                },
                'message': '用户注册成功',
                'timestamp': datetime.now().isoformat()
            }
            
            return HTTPResponse(
                status_code=201,
                headers={'Content-Type': 'application/json'},
                body=json.dumps(response_data, ensure_ascii=False)
            )
            
        except (json.JSONDecodeError, ValueError) as e:
            return HTTPResponse(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body=json.dumps({
                    'success': False,
                    'message': f'注册失败: {str(e)}',
                    'timestamp': datetime.now().isoformat()
                })
            )
    
    def login(self, request: HTTPRequest) -> HTTPResponse:
        try:
            if not request.body:
                raise ValueError("请求体不能为空")
            
            login_data = json.loads(request.body)
            
            username = login_data.get('username')
            password = login_data.get('password')
            
            if not username or not password:
                raise ValueError("用户名和密码不能为空")
            
            # 验证用户
            user = self.data_store.get_user_by_username(username)
            if not user:
                raise ValueError("用户名或密码错误")
            
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if user.password_hash != password_hash:
                raise ValueError("用户名或密码错误")
            
            # 更新最后登录时间
            user.last_login = datetime.now()
            
            # 生成JWT令牌
            token = self.auth_middleware.generate_token(user.id)
            
            response_data = {
                'success': True,
                'data': {
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'full_name': user.full_name
                    },
                    'token': token
                },
                'message': '登录成功',
                'timestamp': datetime.now().isoformat()
            }
            
            return HTTPResponse(
                status_code=200,
                headers={'Content-Type': 'application/json'},
                body=json.dumps(response_data, ensure_ascii=False)
            )
            
        except (json.JSONDecodeError, ValueError) as e:
            return HTTPResponse(
                status_code=401,
                headers={'Content-Type': 'application/json'},
                body=json.dumps({
                    'success': False,
                    'message': f'登录失败: {str(e)}',
                    'timestamp': datetime.now().isoformat()
                })
            )
    
    def get_profile(self, request: HTTPRequest) -> HTTPResponse:
        try:
            user_id = request.user_id
            user = self.data_store.users.get(user_id)
            
            if not user:
                return HTTPResponse(
                    status_code=404,
                    headers={'Content-Type': 'application/json'},
                    body=json.dumps({
                        'success': False,
                        'message': '用户不存在',
                        'timestamp': datetime.now().isoformat()
                    })
                )
            
            response_data = {
                'success': True,
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'full_name': user.full_name,
                    'phone': user.phone,
                    'address': user.address,
                    'created_at': user.created_at.isoformat(),
                    'last_login': user.last_login.isoformat() if user.last_login else None
                },
                'message': '获取用户信息成功',
                'timestamp': datetime.now().isoformat()
            }
            
            return HTTPResponse(
                status_code=200,
                headers={'Content-Type': 'application/json'},
                body=json.dumps(response_data, ensure_ascii=False)
            )
            
        except Exception as e:
            return HTTPResponse(
                status_code=500,
                headers={'Content-Type': 'application/json'},
                body=json.dumps({
                    'success': False,
                    'message': f'服务器错误: {str(e)}',
                    'timestamp': datetime.now().isoformat()
                })
            )

class OrderController:
    def __init__(self, data_store: DataStore):
        self.data_store = data_store
    
    def create_order(self, request: HTTPRequest) -> HTTPResponse:
        try:
            if not request.body:
                raise ValueError("请求体不能为空")
            
            order_data = json.loads(request.body)
            order_data['user_id'] = request.user_id
            
            # 验证必需字段
            required_fields = ['items', 'shipping_address']
            for field in required_fields:
                if field not in order_data:
                    raise ValueError(f"缺少必需字段: {field}")
            
            # 计算总金额
            total_amount = 0
            for item in order_data['items']:
                product = self.data_store.products.get(item['product_id'])
                if not product:
                    raise ValueError(f"商品 {item['product_id']} 不存在")
                if product.stock < item['quantity']:
                    raise ValueError(f"商品 {product.name} 库存不足")
                total_amount += product.price * item['quantity']
                item['price'] = product.price
            
            order_data['total_amount'] = total_amount
            
            # 创建订单
            order = self.data_store.create_order(order_data)
            
            # 更新商品库存
            for item in order.items:
                product = self.data_store.products[item.product_id]
                product.stock -= item.quantity
            
            response_data = {
                'success': True,
                'data': {
                    'id': order.id,
                    'total_amount': order.total_amount,
                    'status': order.status.value,
                    'created_at': order.created_at.isoformat()
                },
                'message': '订单创建成功',
                'timestamp': datetime.now().isoformat()
            }
            
            return HTTPResponse(
                status_code=201,
                headers={'Content-Type': 'application/json'},
                body=json.dumps(response_data, ensure_ascii=False)
            )
            
        except (json.JSONDecodeError, ValueError) as e:
            return HTTPResponse(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body=json.dumps({
                    'success': False,
                    'message': f'创建订单失败: {str(e)}',
                    'timestamp': datetime.now().isoformat()
                })
            )
    
    def get_orders(self, request: HTTPRequest) -> HTTPResponse:
        try:
            user_id = request.user_id
            user_orders = [order for order in self.data_store.orders.values() if order.user_id == user_id]
            
            response_data = {
                'success': True,
                'data': [
                    {
                        'id': order.id,
                        'total_amount': order.total_amount,
                        'status': order.status.value,
                        'items_count': len(order.items),
                        'created_at': order.created_at.isoformat()
                    } for order in user_orders
                ],
                'message': f'找到 {len(user_orders)} 个订单',
                'timestamp': datetime.now().isoformat()
            }
            
            return HTTPResponse(
                status_code=200,
                headers={'Content-Type': 'application/json'},
                body=json.dumps(response_data, ensure_ascii=False)
            )
            
        except Exception as e:
            return HTTPResponse(
                status_code=500,
                headers={'Content-Type': 'application/json'},
                body=json.dumps({
                    'success': False,
                    'message': f'服务器错误: {str(e)}',
                    'timestamp': datetime.now().isoformat()
                })
            )

# ============================================================================
# API文档生成器 (API Documentation Generator)
# ============================================================================

class APIDocGenerator:
    def __init__(self, router: Router):
        self.router = router
    
    def generate_openapi_spec(self) -> Dict[str, Any]:
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "电商系统API",
                "version": "1.0.0",
                "description": "电商系统RESTful API文档"
            },
            "servers": [
                {"url": "http://localhost:8000/api/v1", "description": "开发环境"}
            ],
            "paths": {},
            "components": {
                "schemas": {
                    "Product": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                            "price": {"type": "number"},
                            "category": {"type": "string"},
                            "stock": {"type": "integer"},
                            "status": {"type": "string", "enum": ["active", "inactive", "out_of_stock"]}
                        }
                    },
                    "User": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "username": {"type": "string"},
                            "email": {"type": "string"},
                            "full_name": {"type": "string"},
                            "phone": {"type": "string"}
                        }
                    },
                    "Order": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "total_amount": {"type": "number"},
                            "status": {"type": "string", "enum": ["pending", "confirmed", "shipped", "delivered", "cancelled"]},
                            "created_at": {"type": "string", "format": "date-time"}
                        }
                    }
                },
                "securitySchemes": {
                    "bearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT"
                    }
                }
            }
        }
        
        # 根据路由生成路径文档
        for route in self.router.routes:
            path_key = route.path.replace('{', '{').replace('}', '}')
            if path_key not in spec["paths"]:
                spec["paths"][path_key] = {}
            
            method_key = route.method.lower()
            spec["paths"][path_key][method_key] = {
                "summary": f"{route.method} {route.path}",
                "responses": {
                    "200": {"description": "成功"},
                    "400": {"description": "请求错误"},
                    "401": {"description": "未认证"},
                    "404": {"description": "资源不存在"},
                    "500": {"description": "服务器错误"}
                }
            }
        
        return spec
    
    def generate_html_doc(self) -> str:
        spec = self.generate_openapi_spec()
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{spec['info']['title']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .endpoint {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .method {{ font-weight: bold; color: white; padding: 5px 10px; border-radius: 3px; }}
        .get {{ background-color: #61affe; }}
        .post {{ background-color: #49cc90; }}
        .put {{ background-color: #fca130; }}
        .delete {{ background-color: #f93e3e; }}
    </style>
</head>
<body>
    <h1>{spec['info']['title']}</h1>
    <p>{spec['info']['description']}</p>
    <p>版本: {spec['info']['version']}</p>
    
    <h2>API端点</h2>
"""
        
        for path, methods in spec['paths'].items():
            for method, details in methods.items():
                html += f"""
    <div class="endpoint">
        <span class="method {method}">{method.upper()}</span>
        <strong>{path}</strong>
        <p>{details['summary']}</p>
    </div>
"""
        
        html += """
</body>
</html>
"""
        return html

# ============================================================================
# API测试框架 (API Testing Framework)
# ============================================================================

class APITestCase:
    def __init__(self, name: str, method: str, path: str, 
                 headers: Dict[str, str] = None, 
                 body: Any = None,
                 expected_status: int = 200):
        self.name = name
        self.method = method
        self.path = path
        self.headers = headers or {}
        self.body = body
        self.expected_status = expected_status

class APITester:
    def __init__(self, router: Router):
        self.router = router
        self.test_cases: List[APITestCase] = []
    
    def add_test_case(self, test_case: APITestCase):
        self.test_cases.append(test_case)
    
    def run_tests(self) -> Dict[str, Any]:
        results = {
            'total': len(self.test_cases),
            'passed': 0,
            'failed': 0,
            'details': []
        }
        
        for test_case in self.test_cases:
            result = self.run_test_case(test_case)
            results['details'].append(result)
            
            if result['passed']:
                results['passed'] += 1
            else:
                results['failed'] += 1
        
        return results
    
    def run_test_case(self, test_case: APITestCase) -> Dict[str, Any]:
        try:
            # 创建请求
            request = HTTPRequest(
                method=test_case.method,
                path=test_case.path,
                headers=test_case.headers,
                query_params={},
                body=json.dumps(test_case.body) if test_case.body else None
            )
            
            # 执行请求
            response = self.router.handle_request(request)
            
            # 检查结果
            passed = response.status_code == test_case.expected_status
            
            return {
                'name': test_case.name,
                'method': test_case.method,
                'path': test_case.path,
                'expected_status': test_case.expected_status,
                'actual_status': response.status_code,
                'passed': passed,
                'response_body': response.body[:200] if response.body else None
            }
            
        except Exception as e:
            return {
                'name': test_case.name,
                'method': test_case.method,
                'path': test_case.path,
                'expected_status': test_case.expected_status,
                'actual_status': 500,
                'passed': False,
                'error': str(e)
            }

# ============================================================================
# 电商API应用 (E-commerce API Application)
# ============================================================================

class ECommerceAPI:
    def __init__(self):
        self.data_store = DataStore()
        self.router = Router()
        self.auth_middleware = JWTAuthMiddleware("secret_key_123")
        
        self.setup_middlewares()
        self.setup_controllers()
        self.setup_routes()
        self.create_sample_data()
    
    def setup_middlewares(self):
        # 添加全局中间件
        self.router.add_middleware(CORSMiddleware())
        self.router.add_middleware(LoggingMiddleware())
        self.router.add_middleware(RateLimitMiddleware(max_requests=100, window_seconds=60))
        self.router.add_middleware(self.auth_middleware)
    
    def setup_controllers(self):
        self.product_controller = ProductController(self.data_store, self.auth_middleware)
        self.user_controller = UserController(self.data_store, self.auth_middleware)
        self.order_controller = OrderController(self.data_store)
    
    def setup_routes(self):
        # 商品路由
        self.router.add_route("GET", "/api/v1/products", self.product_controller.get_products)
        self.router.add_route("GET", "/api/v1/products/{id}", self.product_controller.get_product)
        self.router.add_route("POST", "/api/v1/products", self.product_controller.create_product)
        self.router.add_route("PUT", "/api/v1/products/{id}", self.product_controller.update_product)
        self.router.add_route("DELETE", "/api/v1/products/{id}", self.product_controller.delete_product)
        
        # 用户路由
        self.router.add_route("POST", "/api/v1/auth/register", self.user_controller.register)
        self.router.add_route("POST", "/api/v1/auth/login", self.user_controller.login)
        self.router.add_route("GET", "/api/v1/users/profile", self.user_controller.get_profile)
        
        # 订单路由
        self.router.add_route("POST", "/api/v1/orders", self.order_controller.create_order)
        self.router.add_route("GET", "/api/v1/orders", self.order_controller.get_orders)
    
    def create_sample_data(self):
        # 创建示例商品
        products = [
            {
                'name': 'iPhone 15 Pro',
                'description': '最新款iPhone，配备A17 Pro芯片',
                'price': 7999.0,
                'category': 'electronics',
                'stock': 50,
                'images': ['iphone15pro.jpg']
            },
            {
                'name': 'MacBook Air M2',
                'description': '轻薄便携的笔记本电脑',
                'price': 8999.0,
                'category': 'electronics',
                'stock': 30,
                'images': ['macbook_air_m2.jpg']
            },
            {
                'name': 'AirPods Pro',
                'description': '主动降噪无线耳机',
                'price': 1999.0,
                'category': 'electronics',
                'stock': 100,
                'images': ['airpods_pro.jpg']
            }
        ]
        
        for product_data in products:
            self.data_store.create_product(product_data)
        
        # 创建示例用户
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password_hash': hashlib.sha256('password123'.encode()).hexdigest(),
            'full_name': '测试用户',
            'phone': '13800138000',
            'address': '北京市朝阳区'
        }
        self.data_store.create_user(user_data)
    
    def handle_request(self, request: HTTPRequest) -> HTTPResponse:
        return self.router.handle_request(request)

# ============================================================================
# 演示代码 (Demo Code)
# ============================================================================

def demo_api_requests():
    print("RESTful API架构演示")
    print("=" * 50)
    
    # 创建API应用
    api = ECommerceAPI()
    
    print("\n📱 API请求演示:")
    
    # 1. 用户注册
    print("\n1. 用户注册:")
    register_request = HTTPRequest(
        method="POST",
        path="/api/v1/auth/register",
        headers={"Content-Type": "application/json"},
        query_params={},
        body=json.dumps({
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
            "full_name": "新用户",
            "phone": "13900139000"
        })
    )
    response = api.handle_request(register_request)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.body[:100]}...")
    
    # 2. 用户登录
    print("\n2. 用户登录:")
    login_request = HTTPRequest(
        method="POST",
        path="/api/v1/auth/login",
        headers={"Content-Type": "application/json"},
        query_params={},
        body=json.dumps({
            "username": "testuser",
            "password": "password123"
        })
    )
    response = api.handle_request(login_request)
    print(f"状态码: {response.status_code}")
    
    # 提取token
    token = None
    if response.status_code == 200:
        response_data = json.loads(response.body)
        if response_data['success']:
            token = response_data['data']['token']
            print(f"获取到token: {token[:20]}...")
    
    # 3. 获取商品列表
    print("\n3. 获取商品列表:")
    products_request = HTTPRequest(
        method="GET",
        path="/api/v1/products",
        headers={},
        query_params={"page": "1", "limit": "10"},
        body=None
    )
    response = api.handle_request(products_request)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        response_data = json.loads(response.body)
        print(f"找到 {len(response_data['data'])} 个商品")
    
    # 4. 创建商品（需要认证）
    print("\n4. 创建商品:")
    if token:
        create_product_request = HTTPRequest(
            method="POST",
            path="/api/v1/products",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            query_params={},
            body=json.dumps({
                "name": "iPad Pro",
                "description": "专业级平板电脑",
                "price": 6999.0,
                "category": "electronics",
                "stock": 20
            })
        )
        response = api.handle_request(create_product_request)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.body[:100]}...")
    
    # 5. 获取用户信息（需要认证）
    print("\n5. 获取用户信息:")
    if token:
        profile_request = HTTPRequest(
            method="GET",
            path="/api/v1/users/profile",
            headers={"Authorization": f"Bearer {token}"},
            query_params={},
            body=None
        )
        response = api.handle_request(profile_request)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            response_data = json.loads(response.body)
            user_data = response_data['data']
            print(f"用户: {user_data['username']} ({user_data['full_name']})")
    
    # 6. 创建订单（需要认证）
    print("\n6. 创建订单:")
    if token:
        create_order_request = HTTPRequest(
            method="POST",
            path="/api/v1/orders",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            query_params={},
            body=json.dumps({
                "items": [
                    {"product_id": 1, "quantity": 1},
                    {"product_id": 3, "quantity": 2}
                ],
                "shipping_address": "北京市朝阳区某某街道123号"
            })
        )
        response = api.handle_request(create_order_request)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.body[:100]}...")

def demo_api_documentation():
    print("\n📚 API文档生成演示:")
    
    api = ECommerceAPI()
    doc_generator = APIDocGenerator(api.router)
    
    # 生成OpenAPI规范
    openapi_spec = doc_generator.generate_openapi_spec()
    print(f"生成OpenAPI文档: {len(openapi_spec['paths'])} 个端点")
    
    # 显示部分文档内容
    print("\nAPI端点列表:")
    for path, methods in openapi_spec['paths'].items():
        for method in methods.keys():
            print(f"  {method.upper()} {path}")
    
    # 生成HTML文档
    html_doc = doc_generator.generate_html_doc()
    print(f"\n生成HTML文档: {len(html_doc)} 字符")

def demo_api_testing():
    print("\n🧪 API测试演示:")
    
    api = ECommerceAPI()
    tester = APITester(api.router)
    
    # 添加测试用例
    test_cases = [
        APITestCase("获取商品列表", "GET", "/api/v1/products", expected_status=200),
        APITestCase("获取单个商品", "GET", "/api/v1/products/1", expected_status=200),
        APITestCase("获取不存在的商品", "GET", "/api/v1/products/999", expected_status=404),
        APITestCase("用户注册", "POST", "/api/v1/auth/register", 
                   headers={"Content-Type": "application/json"},
                   body={
                       "username": "testuser2",
                       "email": "testuser2@example.com",
                       "password": "password123",
                       "full_name": "测试用户2",
                       "phone": "13900139001"
                   },
                   expected_status=201),
        APITestCase("重复用户名注册", "POST", "/api/v1/auth/register",
                   headers={"Content-Type": "application/json"},
                   body={
                       "username": "testuser",
                       "email": "another@example.com",
                       "password": "password123",
                       "full_name": "另一个用户",
                       "phone": "13900139002"
                   },
                   expected_status=400),
        APITestCase("用户登录", "POST", "/api/v1/auth/login",
                   headers={"Content-Type": "application/json"},
                   body={
                       "username": "testuser",
                       "password": "password123"
                   },
                   expected_status=200),
        APITestCase("错误密码登录", "POST", "/api/v1/auth/login",
                   headers={"Content-Type": "application/json"},
                   body={
                       "username": "testuser",
                       "password": "wrongpassword"
                   },
                   expected_status=401)
    ]
    
    for test_case in test_cases:
        tester.add_test_case(test_case)
    
    # 运行测试
    results = tester.run_tests()
    
    print(f"测试结果: {results['passed']}/{results['total']} 通过")
    print(f"失败: {results['failed']} 个")
    
    print("\n详细结果:")
    for detail in results['details']:
        status = "✅" if detail['passed'] else "❌"
        print(f"  {status} {detail['name']} - {detail['method']} {detail['path']}")
        print(f"    期望状态码: {detail['expected_status']}, 实际: {detail['actual_status']}")
        if not detail['passed'] and 'error' in detail:
            print(f"    错误: {detail['error']}")

def demo_middleware_chain():
    print("\n🔗 中间件链演示:")
    
    # 创建简单的路由器来演示中间件
    router = Router()
    
    # 添加中间件
    auth_middleware = JWTAuthMiddleware("demo_secret")
    logging_middleware = LoggingMiddleware()
    rate_limit_middleware = RateLimitMiddleware(max_requests=5, window_seconds=10)
    cors_middleware = CORSMiddleware()
    
    router.add_middleware(cors_middleware)
    router.add_middleware(logging_middleware)
    router.add_middleware(rate_limit_middleware)
    router.add_middleware(auth_middleware)
    
    # 添加一个简单的处理器
    def simple_handler(request: HTTPRequest) -> HTTPResponse:
        return HTTPResponse(
            status_code=200,
            headers={"Content-Type": "application/json"},
            body=json.dumps({"message": "Hello from protected endpoint!"})
        )
    
    router.add_route("GET", "/api/protected", simple_handler)
    
    print("中间件执行顺序演示:")
    
    # 1. 无认证请求
    print("\n1. 无认证请求:")
    request = HTTPRequest(
        method="GET",
        path="/api/protected",
        headers={},
        query_params={},
        body=None
    )
    response = router.handle_request(request)
    print(f"状态码: {response.status_code}")
    
    # 2. 有效认证请求
    print("\n2. 有效认证请求:")
    token = auth_middleware.generate_token(1)
    request = HTTPRequest(
        method="GET",
        path="/api/protected",
        headers={"Authorization": f"Bearer {token}"},
        query_params={},
        body=None
    )
    response = router.handle_request(request)
    print(f"状态码: {response.status_code}")
    
    # 3. 频率限制测试
    print("\n3. 频率限制测试:")
    for i in range(7):  # 超过限制的5次
        request = HTTPRequest(
            method="GET",
            path="/api/protected",
            headers={"Authorization": f"Bearer {token}", "X-Real-IP": "192.168.1.100"},
            query_params={},
            body=None
        )
        response = router.handle_request(request)
        print(f"  请求 {i+1}: 状态码 {response.status_code}")
        if response.status_code == 429:
            print("    触发频率限制!")
            break

def main():
    """主演示函数"""
    print("Session 27: 项目架构设计 - RESTful API架构实现")
    print("=" * 60)
    
    try:
        # API请求演示
        demo_api_requests()
        
        # API文档生成演示
        demo_api_documentation()
        
        # API测试演示
        demo_api_testing()
        
        # 中间件链演示
        demo_middleware_chain()
        
        print("\n" + "=" * 60)
        print("🎉 RESTful API架构演示完成!")
        print("\n主要特性:")
        print("✅ 分层架构设计")
        print("✅ 中间件链处理")
        print("✅ JWT认证机制")
        print("✅ 路由参数解析")
        print("✅ 数据验证和错误处理")
        print("✅ API文档自动生成")
        print("✅ 自动化测试框架")
        print("✅ 跨域和限流支持")
        
        print("\n架构优势:")
        print("• 模块化设计，易于扩展")
        print("• 中间件机制，关注点分离")
        print("• 统一的错误处理")
        print("• 自动化文档和测试")
        print("• 安全性和性能考虑")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

"""
总结:

这个解决方案展示了如何设计和实现一个完整的RESTful API系统，包括:

1. **架构设计**:
   - 分层架构（控制器、服务、数据层）
   - 中间件模式
   - 依赖注入

2. **核心功能**:
   - HTTP请求/响应处理
   - 路由匹配和参数解析
   - JWT认证和授权
   - 数据验证和序列化

3. **中间件系统**:
   - 认证中间件
   - 日志中间件
   - 限流中间件
   - CORS中间件

4. **开发工具**:
   - API文档自动生成
   - 自动化测试框架
   - 错误处理机制

5. **最佳实践**:
   - RESTful设计原则
   - 统一的响应格式
   - 安全性考虑
   - 性能优化

这个实现为构建生产级API系统提供了坚实的基础。
"""