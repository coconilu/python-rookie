#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习2: 设计RESTful API架构

要求:
1. 设计一个电商系统的RESTful API
2. 实现API版本控制
3. 添加认证和授权机制
4. 实现API文档自动生成
5. 包含以下资源：
   - 商品 (Products)
   - 用户 (Users)
   - 订单 (Orders)
   - 购物车 (Cart)
   - 支付 (Payments)

请完成以下任务：
1. 设计RESTful API规范
2. 实现API路由和处理器
3. 添加中间件（认证、日志、限流）
4. 实现API文档生成
5. 编写API测试代码
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import json
import hashlib
import time
from functools import wraps

# ============================================================================
# API设计规范
# ============================================================================

"""
RESTful API设计规范:

1. 资源命名规范:
   - 使用名词复数形式
   - 使用小写字母和连字符
   - 避免动词

2. HTTP方法使用:
   - GET: 获取资源
   - POST: 创建资源
   - PUT: 完整更新资源
   - PATCH: 部分更新资源
   - DELETE: 删除资源

3. 状态码规范:
   - 200: 成功
   - 201: 创建成功
   - 204: 删除成功
   - 400: 请求错误
   - 401: 未认证
   - 403: 无权限
   - 404: 资源不存在
   - 500: 服务器错误

4. API版本控制:
   - URL版本: /api/v1/products
   - Header版本: Accept: application/vnd.api+json;version=1

5. 分页和过滤:
   - 分页: ?page=1&limit=20
   - 排序: ?sort=created_at&order=desc
   - 过滤: ?category=electronics&price_min=100

6. 响应格式:
   {
     "success": true,
     "data": {...},
     "message": "操作成功",
     "timestamp": "2024-01-01T00:00:00Z",
     "pagination": {
       "page": 1,
       "limit": 20,
       "total": 100,
       "pages": 5
     }
   }

API端点设计:

商品管理:
GET    /api/v1/products              # 获取商品列表
GET    /api/v1/products/{id}         # 获取单个商品
POST   /api/v1/products              # 创建商品
PUT    /api/v1/products/{id}         # 更新商品
DELETE /api/v1/products/{id}         # 删除商品
GET    /api/v1/products/{id}/reviews # 获取商品评价

用户管理:
POST   /api/v1/auth/register         # 用户注册
POST   /api/v1/auth/login            # 用户登录
POST   /api/v1/auth/logout           # 用户登出
GET    /api/v1/users/profile         # 获取用户信息
PUT    /api/v1/users/profile         # 更新用户信息

订单管理:
GET    /api/v1/orders                # 获取订单列表
GET    /api/v1/orders/{id}           # 获取单个订单
POST   /api/v1/orders                # 创建订单
PUT    /api/v1/orders/{id}/status    # 更新订单状态
DELETE /api/v1/orders/{id}           # 取消订单

购物车管理:
GET    /api/v1/cart                  # 获取购物车
POST   /api/v1/cart/items            # 添加商品到购物车
PUT    /api/v1/cart/items/{id}       # 更新购物车商品
DELETE /api/v1/cart/items/{id}       # 从购物车删除商品
DELETE /api/v1/cart                  # 清空购物车

支付管理:
POST   /api/v1/payments              # 创建支付
GET    /api/v1/payments/{id}         # 获取支付信息
POST   /api/v1/payments/{id}/confirm # 确认支付
"""

# ============================================================================
# 数据模型 (Data Models)
# ============================================================================

class ProductStatus(Enum):
    """商品状态"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    OUT_OF_STOCK = "out_of_stock"

class OrderStatus(Enum):
    """订单状态"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class PaymentStatus(Enum):
    """支付状态"""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

@dataclass
class Product:
    """商品模型"""
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
    """用户模型"""
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
    """订单项模型"""
    product_id: int
    quantity: int
    price: float

@dataclass
class Order:
    """订单模型"""
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
    """购物车项模型"""
    product_id: int
    quantity: int
    added_at: datetime

@dataclass
class Cart:
    """购物车模型"""
    user_id: int
    items: List[CartItem]
    updated_at: datetime

@dataclass
class Payment:
    """支付模型"""
    id: int
    order_id: int
    amount: float
    method: str
    status: PaymentStatus
    transaction_id: str
    created_at: datetime

# ============================================================================
# HTTP请求和响应模型
# ============================================================================

@dataclass
class HTTPRequest:
    """HTTP请求模型"""
    method: str
    path: str
    headers: Dict[str, str]
    query_params: Dict[str, str]
    body: Optional[str]
    user_id: Optional[int] = None

@dataclass
class HTTPResponse:
    """HTTP响应模型"""
    status_code: int
    headers: Dict[str, str]
    body: str

@dataclass
class APIResponse:
    """API响应模型"""
    success: bool
    data: Any
    message: str
    timestamp: datetime
    pagination: Optional[Dict[str, Any]] = None

# ============================================================================
# 中间件接口 (Middleware Interfaces)
# ============================================================================

# TODO: 定义中间件接口
# 提示: 定义认证、日志、限流等中间件接口

class IMiddleware(ABC):
    """中间件接口"""
    @abstractmethod
    def process_request(self, request: HTTPRequest) -> Optional[HTTPResponse]:
        """处理请求，返回None继续，返回Response则中断"""
        pass
    
    @abstractmethod
    def process_response(self, request: HTTPRequest, response: HTTPResponse) -> HTTPResponse:
        """处理响应"""
        pass

class IAuthMiddleware(IMiddleware):
    """认证中间件接口"""
    # TODO: 定义认证相关方法
    pass

class ILoggingMiddleware(IMiddleware):
    """日志中间件接口"""
    # TODO: 定义日志相关方法
    pass

class IRateLimitMiddleware(IMiddleware):
    """限流中间件接口"""
    # TODO: 定义限流相关方法
    pass

# ============================================================================
# 控制器接口 (Controller Interfaces)
# ============================================================================

# TODO: 定义控制器接口
# 提示: 为每个资源定义控制器接口

class IProductController(ABC):
    """商品控制器接口"""
    @abstractmethod
    def get_products(self, request: HTTPRequest) -> HTTPResponse:
        """获取商品列表"""
        pass
    
    @abstractmethod
    def get_product(self, request: HTTPRequest, product_id: int) -> HTTPResponse:
        """获取单个商品"""
        pass
    
    @abstractmethod
    def create_product(self, request: HTTPRequest) -> HTTPResponse:
        """创建商品"""
        pass
    
    @abstractmethod
    def update_product(self, request: HTTPRequest, product_id: int) -> HTTPResponse:
        """更新商品"""
        pass
    
    @abstractmethod
    def delete_product(self, request: HTTPRequest, product_id: int) -> HTTPResponse:
        """删除商品"""
        pass

class IUserController(ABC):
    """用户控制器接口"""
    # TODO: 定义用户控制器方法
    pass

class IOrderController(ABC):
    """订单控制器接口"""
    # TODO: 定义订单控制器方法
    pass

class ICartController(ABC):
    """购物车控制器接口"""
    # TODO: 定义购物车控制器方法
    pass

class IPaymentController(ABC):
    """支付控制器接口"""
    # TODO: 定义支付控制器方法
    pass

# ============================================================================
# 路由器 (Router)
# ============================================================================

# TODO: 实现路由器
# 提示: 实现URL路由匹配和处理器分发

class Route:
    """路由定义"""
    def __init__(self, method: str, path: str, handler: Callable, middlewares: List[IMiddleware] = None):
        self.method = method
        self.path = path
        self.handler = handler
        self.middlewares = middlewares or []

class Router:
    """路由器"""
    def __init__(self):
        self.routes: List[Route] = []
        self.global_middlewares: List[IMiddleware] = []
    
    def add_route(self, method: str, path: str, handler: Callable, middlewares: List[IMiddleware] = None):
        """添加路由"""
        # TODO: 实现路由添加逻辑
        pass
    
    def add_middleware(self, middleware: IMiddleware):
        """添加全局中间件"""
        # TODO: 实现中间件添加逻辑
        pass
    
    def match_route(self, method: str, path: str) -> Optional[Route]:
        """匹配路由"""
        # TODO: 实现路由匹配逻辑
        # 支持路径参数，如 /products/{id}
        pass
    
    def handle_request(self, request: HTTPRequest) -> HTTPResponse:
        """处理请求"""
        # TODO: 实现请求处理逻辑
        # 1. 匹配路由
        # 2. 执行中间件
        # 3. 调用处理器
        # 4. 返回响应
        pass

# ============================================================================
# 中间件实现 (Middleware Implementation)
# ============================================================================

# TODO: 实现中间件
# 提示: 实现认证、日志、限流等中间件

class JWTAuthMiddleware(IAuthMiddleware):
    """JWT认证中间件"""
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
    
    def process_request(self, request: HTTPRequest) -> Optional[HTTPResponse]:
        """验证JWT令牌"""
        # TODO: 实现JWT验证逻辑
        pass
    
    def process_response(self, request: HTTPRequest, response: HTTPResponse) -> HTTPResponse:
        return response

class LoggingMiddleware(ILoggingMiddleware):
    """日志中间件"""
    def process_request(self, request: HTTPRequest) -> Optional[HTTPResponse]:
        """记录请求日志"""
        # TODO: 实现请求日志记录
        pass
    
    def process_response(self, request: HTTPRequest, response: HTTPResponse) -> HTTPResponse:
        """记录响应日志"""
        # TODO: 实现响应日志记录
        pass

class RateLimitMiddleware(IRateLimitMiddleware):
    """限流中间件"""
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[float]] = {}
    
    def process_request(self, request: HTTPRequest) -> Optional[HTTPResponse]:
        """检查请求频率"""
        # TODO: 实现限流逻辑
        pass
    
    def process_response(self, request: HTTPRequest, response: HTTPResponse) -> HTTPResponse:
        return response

class CORSMiddleware(IMiddleware):
    """跨域中间件"""
    def process_request(self, request: HTTPRequest) -> Optional[HTTPResponse]:
        # TODO: 处理OPTIONS预检请求
        pass
    
    def process_response(self, request: HTTPRequest, response: HTTPResponse) -> HTTPResponse:
        """添加CORS头"""
        # TODO: 添加CORS响应头
        pass

# ============================================================================
# 控制器实现 (Controller Implementation)
# ============================================================================

# TODO: 实现控制器
# 提示: 实现各个资源的控制器

class ProductController(IProductController):
    """商品控制器实现"""
    def __init__(self):
        # 模拟数据存储
        self.products: Dict[int, Product] = {}
        self.next_id = 1
    
    def get_products(self, request: HTTPRequest) -> HTTPResponse:
        """获取商品列表"""
        # TODO: 实现商品列表获取
        # 支持分页、排序、过滤
        pass
    
    def get_product(self, request: HTTPRequest, product_id: int) -> HTTPResponse:
        """获取单个商品"""
        # TODO: 实现单个商品获取
        pass
    
    def create_product(self, request: HTTPRequest) -> HTTPResponse:
        """创建商品"""
        # TODO: 实现商品创建
        pass
    
    def update_product(self, request: HTTPRequest, product_id: int) -> HTTPResponse:
        """更新商品"""
        # TODO: 实现商品更新
        pass
    
    def delete_product(self, request: HTTPRequest, product_id: int) -> HTTPResponse:
        """删除商品"""
        # TODO: 实现商品删除
        pass

class UserController(IUserController):
    """用户控制器实现"""
    # TODO: 实现用户控制器
    pass

class OrderController(IOrderController):
    """订单控制器实现"""
    # TODO: 实现订单控制器
    pass

class CartController(ICartController):
    """购物车控制器实现"""
    # TODO: 实现购物车控制器
    pass

class PaymentController(IPaymentController):
    """支付控制器实现"""
    # TODO: 实现支付控制器
    pass

# ============================================================================
# API文档生成器 (API Documentation Generator)
# ============================================================================

# TODO: 实现API文档生成器
# 提示: 自动生成OpenAPI/Swagger文档

class APIDocGenerator:
    """API文档生成器"""
    def __init__(self, router: Router):
        self.router = router
    
    def generate_openapi_spec(self) -> Dict[str, Any]:
        """生成OpenAPI规范"""
        # TODO: 实现OpenAPI文档生成
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
                "schemas": {},
                "securitySchemes": {
                    "bearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT"
                    }
                }
            }
        }
        # TODO: 根据路由生成路径和模式定义
        return spec
    
    def generate_html_doc(self) -> str:
        """生成HTML文档"""
        # TODO: 生成可视化API文档
        pass

# ============================================================================
# API测试框架 (API Testing Framework)
# ============================================================================

# TODO: 实现API测试框架
# 提示: 实现API端点测试

class APITestCase:
    """API测试用例"""
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
    """API测试器"""
    def __init__(self, router: Router):
        self.router = router
        self.test_cases: List[APITestCase] = []
    
    def add_test_case(self, test_case: APITestCase):
        """添加测试用例"""
        # TODO: 实现测试用例添加
        pass
    
    def run_tests(self) -> Dict[str, Any]:
        """运行所有测试"""
        # TODO: 实现测试执行
        pass
    
    def run_test_case(self, test_case: APITestCase) -> Dict[str, Any]:
        """运行单个测试用例"""
        # TODO: 实现单个测试执行
        pass

# ============================================================================
# 应用程序 (Application)
# ============================================================================

class ECommerceAPI:
    """电商API应用"""
    def __init__(self):
        self.router = Router()
        self.setup_middlewares()
        self.setup_routes()
    
    def setup_middlewares(self):
        """设置中间件"""
        # TODO: 添加全局中间件
        pass
    
    def setup_routes(self):
        """设置路由"""
        # TODO: 注册所有API路由
        # 商品路由
        # self.router.add_route("GET", "/products", product_controller.get_products)
        # self.router.add_route("GET", "/products/{id}", product_controller.get_product)
        # ...
        pass
    
    def handle_request(self, request: HTTPRequest) -> HTTPResponse:
        """处理HTTP请求"""
        return self.router.handle_request(request)

# ============================================================================
# 演示代码 (Demo Code)
# ============================================================================

def create_sample_data():
    """创建示例数据"""
    # TODO: 创建示例商品、用户等数据
    pass

def demo_api_requests():
    """演示API请求"""
    print("RESTful API架构演示")
    print("=" * 40)
    
    # TODO: 创建API应用
    # api = ECommerceAPI()
    
    # TODO: 演示各种API请求
    # 1. 商品管理API
    # 2. 用户认证API
    # 3. 订单管理API
    # 4. 购物车API
    # 5. 支付API
    
    print("\n📱 API请求演示:")
    
    # 示例请求
    requests = [
        HTTPRequest("GET", "/api/v1/products", {}, {"page": "1", "limit": "10"}, None),
        HTTPRequest("POST", "/api/v1/auth/login", {"Content-Type": "application/json"}, {}, 
                   '{"username": "user1", "password": "password123"}'),
        HTTPRequest("POST", "/api/v1/products", {"Authorization": "Bearer token123"}, {}, 
                   '{"name": "iPhone 15", "price": 999.99, "category": "electronics"}'),
    ]
    
    # TODO: 处理请求并显示响应
    # for req in requests:
    #     response = api.handle_request(req)
    #     print(f"{req.method} {req.path} -> {response.status_code}")
    
    print("\n📚 API文档生成演示:")
    # TODO: 生成API文档
    # doc_generator = APIDocGenerator(api.router)
    # openapi_spec = doc_generator.generate_openapi_spec()
    # print(f"生成OpenAPI文档: {len(openapi_spec['paths'])} 个端点")
    
    print("\n🧪 API测试演示:")
    # TODO: 运行API测试
    # tester = APITester(api.router)
    # test_results = tester.run_tests()
    # print(f"测试结果: {test_results}")

def main():
    """主函数"""
    print("RESTful API架构设计练习")
    print("=" * 40)
    
    # 创建示例数据
    create_sample_data()
    
    # 演示API功能
    demo_api_requests()
    
    print("\n✅ 练习完成！")
    print("\n💡 扩展建议:")
    print("1. 实现API版本控制")
    print("2. 添加API缓存机制")
    print("3. 实现API监控和指标")
    print("4. 添加API安全防护")
    print("5. 实现API网关功能")

if __name__ == "__main__":
    main()

# ============================================================================
# 练习指导
# ============================================================================

"""
练习完成指导:

1. 路由系统 (30分钟)
   - 实现Router类的路由匹配逻辑
   - 支持路径参数解析
   - 实现请求分发机制

2. 中间件系统 (45分钟)
   - 实现认证中间件（JWT验证）
   - 实现日志中间件（请求/响应记录）
   - 实现限流中间件（频率控制）
   - 实现CORS中间件（跨域支持）

3. 控制器实现 (60分钟)
   - 实现ProductController的所有方法
   - 实现UserController（注册、登录、认证）
   - 实现OrderController（订单管理）
   - 实现CartController（购物车管理）
   - 实现PaymentController（支付处理）

4. API文档生成 (30分钟)
   - 实现OpenAPI规范生成
   - 生成HTML格式文档
   - 包含请求/响应示例

5. API测试框架 (30分钟)
   - 实现测试用例执行
   - 验证响应状态码和数据
   - 生成测试报告

6. 演示和集成 (30分钟)
   - 创建完整的API应用
   - 演示各种API操作
   - 展示文档和测试结果

评估标准:
- RESTful设计是否规范
- 中间件是否正确实现
- API功能是否完整
- 文档是否自动生成
- 测试是否覆盖全面
- 代码是否可以正常运行

高级扩展:
- 实现API版本控制策略
- 添加API缓存和性能优化
- 实现API监控和日志分析
- 添加API安全防护机制
- 实现微服务API网关
"""