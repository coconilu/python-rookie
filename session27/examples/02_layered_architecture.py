#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分层架构模式详细示例

本文件演示了分层架构模式的实现，包括：
1. 三层架构 (表示层、业务逻辑层、数据访问层)
2. 四层架构 (表示层、应用服务层、领域层、基础设施层)
3. 层间依赖管理
4. 数据传输对象 (DTO) 的使用
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import json


# ============================================================================
# 数据传输对象 (DTOs)
# ============================================================================

@dataclass
class ProductDTO:
    """产品数据传输对象"""
    id: int
    name: str
    price: float
    category: str
    stock: int
    description: str = ""
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class OrderDTO:
    """订单数据传输对象"""
    id: int
    customer_id: int
    products: List[Dict[str, Any]]  # [{"product_id": int, "quantity": int, "price": float}]
    total_amount: float
    status: str
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class CustomerDTO:
    """客户数据传输对象"""
    id: int
    name: str
    email: str
    phone: str
    address: str
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

class OrderStatus(Enum):
    """订单状态枚举"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


# ============================================================================
# 三层架构示例
# ============================================================================

print("三层架构模式演示")
print("=" * 50)

# 数据访问层 (Data Access Layer)
class ProductRepository:
    """产品仓储 - 数据访问层"""
    def __init__(self):
        self.products = [
            ProductDTO(1, "笔记本电脑", 5999.0, "电子产品", 10, "高性能笔记本电脑"),
            ProductDTO(2, "无线鼠标", 99.0, "电子产品", 50, "蓝牙无线鼠标"),
            ProductDTO(3, "机械键盘", 299.0, "电子产品", 30, "RGB机械键盘"),
            ProductDTO(4, "显示器", 1299.0, "电子产品", 15, "27寸4K显示器"),
        ]
        self.next_id = 5
    
    def find_all(self) -> List[ProductDTO]:
        """获取所有产品"""
        print("📊 [数据层] 查询所有产品")
        return self.products.copy()
    
    def find_by_id(self, product_id: int) -> Optional[ProductDTO]:
        """根据ID查找产品"""
        print(f"📊 [数据层] 查询产品ID: {product_id}")
        return next((p for p in self.products if p.id == product_id), None)
    
    def find_by_category(self, category: str) -> List[ProductDTO]:
        """根据分类查找产品"""
        print(f"📊 [数据层] 查询分类: {category}")
        return [p for p in self.products if p.category == category]
    
    def find_in_stock(self) -> List[ProductDTO]:
        """查找有库存的产品"""
        print("📊 [数据层] 查询有库存的产品")
        return [p for p in self.products if p.stock > 0]
    
    def update_stock(self, product_id: int, quantity: int) -> bool:
        """更新库存"""
        print(f"📊 [数据层] 更新产品 {product_id} 库存: {quantity}")
        product = self.find_by_id(product_id)
        if product and product.stock >= quantity:
            product.stock -= quantity
            return True
        return False
    
    def save(self, product: ProductDTO) -> ProductDTO:
        """保存产品"""
        if product.id == 0:
            product.id = self.next_id
            self.next_id += 1
            self.products.append(product)
            print(f"📊 [数据层] 新增产品: {product.name}")
        else:
            # 更新现有产品
            for i, p in enumerate(self.products):
                if p.id == product.id:
                    self.products[i] = product
                    print(f"📊 [数据层] 更新产品: {product.name}")
                    break
        return product

class OrderRepository:
    """订单仓储 - 数据访问层"""
    def __init__(self):
        self.orders: List[OrderDTO] = []
        self.next_id = 1
    
    def save(self, order: OrderDTO) -> OrderDTO:
        """保存订单"""
        if order.id == 0:
            order.id = self.next_id
            self.next_id += 1
        self.orders.append(order)
        print(f"📊 [数据层] 保存订单: {order.id}")
        return order
    
    def find_by_id(self, order_id: int) -> Optional[OrderDTO]:
        """根据ID查找订单"""
        print(f"📊 [数据层] 查询订单ID: {order_id}")
        return next((o for o in self.orders if o.id == order_id), None)
    
    def find_by_customer(self, customer_id: int) -> List[OrderDTO]:
        """根据客户ID查找订单"""
        print(f"📊 [数据层] 查询客户 {customer_id} 的订单")
        return [o for o in self.orders if o.customer_id == customer_id]
    
    def update_status(self, order_id: int, status: str) -> bool:
        """更新订单状态"""
        print(f"📊 [数据层] 更新订单 {order_id} 状态为: {status}")
        order = self.find_by_id(order_id)
        if order:
            order.status = status
            return True
        return False

class CustomerRepository:
    """客户仓储 - 数据访问层"""
    def __init__(self):
        self.customers = [
            CustomerDTO(1, "张三", "zhangsan@example.com", "13800138000", "北京市朝阳区"),
            CustomerDTO(2, "李四", "lisi@example.com", "13900139000", "上海市浦东新区"),
        ]
        self.next_id = 3
    
    def find_by_id(self, customer_id: int) -> Optional[CustomerDTO]:
        """根据ID查找客户"""
        print(f"📊 [数据层] 查询客户ID: {customer_id}")
        return next((c for c in self.customers if c.id == customer_id), None)
    
    def find_by_email(self, email: str) -> Optional[CustomerDTO]:
        """根据邮箱查找客户"""
        print(f"📊 [数据层] 查询客户邮箱: {email}")
        return next((c for c in self.customers if c.email == email), None)

# 业务逻辑层 (Business Logic Layer)
class ProductService:
    """产品服务 - 业务逻辑层"""
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo
    
    def get_available_products(self) -> List[ProductDTO]:
        """获取可用产品"""
        print("🔧 [业务层] 获取可用产品")
        return self.product_repo.find_in_stock()
    
    def search_products_by_category(self, category: str) -> List[ProductDTO]:
        """按分类搜索产品"""
        print(f"🔧 [业务层] 按分类搜索产品: {category}")
        return self.product_repo.find_by_category(category)
    
    def get_product_details(self, product_id: int) -> Optional[ProductDTO]:
        """获取产品详情"""
        print(f"🔧 [业务层] 获取产品详情: {product_id}")
        return self.product_repo.find_by_id(product_id)
    
    def check_stock_availability(self, product_id: int, quantity: int) -> bool:
        """检查库存可用性"""
        print(f"🔧 [业务层] 检查库存: 产品{product_id}, 数量{quantity}")
        product = self.product_repo.find_by_id(product_id)
        return product is not None and product.stock >= quantity
    
    def reserve_stock(self, product_id: int, quantity: int) -> bool:
        """预留库存"""
        print(f"🔧 [业务层] 预留库存: 产品{product_id}, 数量{quantity}")
        if self.check_stock_availability(product_id, quantity):
            return self.product_repo.update_stock(product_id, quantity)
        return False

class OrderService:
    """订单服务 - 业务逻辑层"""
    def __init__(self, order_repo: OrderRepository, product_service: ProductService, customer_repo: CustomerRepository):
        self.order_repo = order_repo
        self.product_service = product_service
        self.customer_repo = customer_repo
    
    def create_order(self, customer_id: int, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """创建订单"""
        print(f"🔧 [业务层] 创建订单: 客户{customer_id}")
        
        # 验证客户存在
        customer = self.customer_repo.find_by_id(customer_id)
        if not customer:
            return {"success": False, "message": "客户不存在"}
        
        # 验证商品和库存
        order_items = []
        total_amount = 0.0
        
        for item in items:
            product_id = item["product_id"]
            quantity = item["quantity"]
            
            product = self.product_service.get_product_details(product_id)
            if not product:
                return {"success": False, "message": f"产品 {product_id} 不存在"}
            
            if not self.product_service.check_stock_availability(product_id, quantity):
                return {"success": False, "message": f"产品 {product.name} 库存不足"}
            
            item_total = product.price * quantity
            order_items.append({
                "product_id": product_id,
                "product_name": product.name,
                "quantity": quantity,
                "price": product.price,
                "total": item_total
            })
            total_amount += item_total
        
        # 预留库存
        for item in items:
            if not self.product_service.reserve_stock(item["product_id"], item["quantity"]):
                return {"success": False, "message": "库存预留失败"}
        
        # 创建订单
        order = OrderDTO(
            id=0,
            customer_id=customer_id,
            products=order_items,
            total_amount=total_amount,
            status=OrderStatus.PENDING.value
        )
        
        saved_order = self.order_repo.save(order)
        
        return {
            "success": True,
            "message": "订单创建成功",
            "order": saved_order
        }
    
    def get_order_details(self, order_id: int) -> Optional[OrderDTO]:
        """获取订单详情"""
        print(f"🔧 [业务层] 获取订单详情: {order_id}")
        return self.order_repo.find_by_id(order_id)
    
    def update_order_status(self, order_id: int, new_status: str) -> bool:
        """更新订单状态"""
        print(f"🔧 [业务层] 更新订单状态: {order_id} -> {new_status}")
        
        # 业务规则验证
        order = self.order_repo.find_by_id(order_id)
        if not order:
            return False
        
        # 状态转换规则
        valid_transitions = {
            OrderStatus.PENDING.value: [OrderStatus.CONFIRMED.value, OrderStatus.CANCELLED.value],
            OrderStatus.CONFIRMED.value: [OrderStatus.SHIPPED.value, OrderStatus.CANCELLED.value],
            OrderStatus.SHIPPED.value: [OrderStatus.DELIVERED.value],
            OrderStatus.DELIVERED.value: [],
            OrderStatus.CANCELLED.value: []
        }
        
        if new_status not in valid_transitions.get(order.status, []):
            print(f"❌ 无效的状态转换: {order.status} -> {new_status}")
            return False
        
        return self.order_repo.update_status(order_id, new_status)
    
    def get_customer_orders(self, customer_id: int) -> List[OrderDTO]:
        """获取客户订单"""
        print(f"🔧 [业务层] 获取客户订单: {customer_id}")
        return self.order_repo.find_by_customer(customer_id)

# 表示层 (Presentation Layer)
class ECommerceController:
    """电商控制器 - 表示层"""
    def __init__(self, product_service: ProductService, order_service: OrderService):
        self.product_service = product_service
        self.order_service = order_service
    
    def display_products(self):
        """显示产品列表"""
        print("🖥️  [表示层] 显示产品列表")
        products = self.product_service.get_available_products()
        
        print("\n📦 可用产品列表:")
        print(f"{'ID':<5} {'名称':<15} {'价格':<10} {'库存':<8} {'分类':<10}")
        print("-" * 55)
        
        for product in products:
            print(f"{product.id:<5} {product.name:<15} ¥{product.price:<9.2f} {product.stock:<8} {product.category:<10}")
    
    def display_product_details(self, product_id: int):
        """显示产品详情"""
        print(f"🖥️  [表示层] 显示产品详情: {product_id}")
        product = self.product_service.get_product_details(product_id)
        
        if product:
            print(f"\n📦 产品详情:")
            print(f"  ID: {product.id}")
            print(f"  名称: {product.name}")
            print(f"  价格: ¥{product.price:.2f}")
            print(f"  分类: {product.category}")
            print(f"  库存: {product.stock}")
            print(f"  描述: {product.description}")
            print(f"  创建时间: {product.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("❌ 产品不存在")
    
    def create_order_action(self, customer_id: int, items: List[Dict[str, Any]]):
        """创建订单操作"""
        print(f"🖥️  [表示层] 创建订单: 客户{customer_id}")
        result = self.order_service.create_order(customer_id, items)
        
        if result["success"]:
            order = result["order"]
            print(f"\n✅ {result['message']}")
            print(f"订单号: {order.id}")
            print(f"总金额: ¥{order.total_amount:.2f}")
            print(f"状态: {order.status}")
            print("订单明细:")
            for item in order.products:
                print(f"  - {item['product_name']} x{item['quantity']} = ¥{item['total']:.2f}")
        else:
            print(f"❌ {result['message']}")
    
    def display_order_details(self, order_id: int):
        """显示订单详情"""
        print(f"🖥️  [表示层] 显示订单详情: {order_id}")
        order = self.order_service.get_order_details(order_id)
        
        if order:
            print(f"\n📋 订单详情:")
            print(f"  订单号: {order.id}")
            print(f"  客户ID: {order.customer_id}")
            print(f"  总金额: ¥{order.total_amount:.2f}")
            print(f"  状态: {order.status}")
            print(f"  创建时间: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print("  订单明细:")
            for item in order.products:
                print(f"    - {item['product_name']} x{item['quantity']} = ¥{item['total']:.2f}")
        else:
            print("❌ 订单不存在")
    
    def update_order_status_action(self, order_id: int, new_status: str):
        """更新订单状态操作"""
        print(f"🖥️  [表示层] 更新订单状态: {order_id} -> {new_status}")
        success = self.order_service.update_order_status(order_id, new_status)
        
        if success:
            print(f"✅ 订单状态更新成功: {new_status}")
        else:
            print("❌ 订单状态更新失败")


def demo_three_layer_architecture():
    """演示三层架构"""
    print("🔹 三层架构演示")
    print("-" * 30)
    
    # 初始化各层
    # 数据访问层
    product_repo = ProductRepository()
    order_repo = OrderRepository()
    customer_repo = CustomerRepository()
    
    # 业务逻辑层
    product_service = ProductService(product_repo)
    order_service = OrderService(order_repo, product_service, customer_repo)
    
    # 表示层
    controller = ECommerceController(product_service, order_service)
    
    # 演示功能
    controller.display_products()
    
    print("\n" + "="*50)
    controller.display_product_details(1)
    
    print("\n" + "="*50)
    # 创建订单
    items = [
        {"product_id": 1, "quantity": 1},
        {"product_id": 2, "quantity": 2}
    ]
    controller.create_order_action(1, items)
    
    print("\n" + "="*50)
    controller.display_order_details(1)
    
    print("\n" + "="*50)
    controller.update_order_status_action(1, OrderStatus.CONFIRMED.value)
    controller.update_order_status_action(1, OrderStatus.SHIPPED.value)


# ============================================================================
# 四层架构示例 (DDD风格)
# ============================================================================

print("\n\n四层架构模式演示 (DDD风格)")
print("=" * 50)

# 领域层 (Domain Layer)
class Product:
    """产品领域实体"""
    def __init__(self, id: int, name: str, price: float, category: str, stock: int):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.stock = stock
        self.created_at = datetime.now()
    
    def is_available(self) -> bool:
        """检查产品是否可用"""
        return self.stock > 0
    
    def reserve_stock(self, quantity: int) -> bool:
        """预留库存"""
        if self.stock >= quantity:
            self.stock -= quantity
            return True
        return False
    
    def calculate_total_price(self, quantity: int) -> float:
        """计算总价"""
        return self.price * quantity

class Order:
    """订单领域实体"""
    def __init__(self, id: int, customer_id: int):
        self.id = id
        self.customer_id = customer_id
        self.items: List[Dict] = []
        self.status = OrderStatus.PENDING
        self.created_at = datetime.now()
        self.total_amount = 0.0
    
    def add_item(self, product: Product, quantity: int) -> bool:
        """添加订单项"""
        if not product.is_available() or product.stock < quantity:
            return False
        
        item = {
            "product_id": product.id,
            "product_name": product.name,
            "quantity": quantity,
            "unit_price": product.price,
            "total_price": product.calculate_total_price(quantity)
        }
        
        self.items.append(item)
        self.total_amount += item["total_price"]
        return True
    
    def can_transition_to(self, new_status: OrderStatus) -> bool:
        """检查是否可以转换到新状态"""
        valid_transitions = {
            OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
            OrderStatus.CONFIRMED: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
            OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
            OrderStatus.DELIVERED: [],
            OrderStatus.CANCELLED: []
        }
        return new_status in valid_transitions.get(self.status, [])
    
    def update_status(self, new_status: OrderStatus) -> bool:
        """更新订单状态"""
        if self.can_transition_to(new_status):
            self.status = new_status
            return True
        return False
    
    def calculate_total(self) -> float:
        """计算订单总额"""
        return sum(item["total_price"] for item in self.items)

# 领域服务
class OrderDomainService:
    """订单领域服务"""
    @staticmethod
    def validate_order_creation(customer_id: int, items: List[Dict]) -> Dict[str, Any]:
        """验证订单创建"""
        if not customer_id or customer_id <= 0:
            return {"valid": False, "message": "无效的客户ID"}
        
        if not items or len(items) == 0:
            return {"valid": False, "message": "订单不能为空"}
        
        for item in items:
            if item.get("quantity", 0) <= 0:
                return {"valid": False, "message": "商品数量必须大于0"}
        
        return {"valid": True, "message": "验证通过"}
    
    @staticmethod
    def calculate_discount(order: Order, customer_type: str) -> float:
        """计算折扣"""
        base_amount = order.calculate_total()
        
        discount_rates = {
            "regular": 0.0,
            "premium": 0.05,
            "vip": 0.10
        }
        
        discount_rate = discount_rates.get(customer_type, 0.0)
        return base_amount * discount_rate

# 基础设施层 (Infrastructure Layer)
class ProductInfraRepository:
    """产品基础设施仓储"""
    def __init__(self):
        self.products = {
            1: Product(1, "笔记本电脑", 5999.0, "电子产品", 10),
            2: Product(2, "无线鼠标", 99.0, "电子产品", 50),
            3: Product(3, "机械键盘", 299.0, "电子产品", 30),
        }
    
    def find_by_id(self, product_id: int) -> Optional[Product]:
        """根据ID查找产品"""
        print(f"🏗️  [基础设施层] 查询产品: {product_id}")
        return self.products.get(product_id)
    
    def find_all(self) -> List[Product]:
        """查找所有产品"""
        print("🏗️  [基础设施层] 查询所有产品")
        return list(self.products.values())
    
    def save(self, product: Product) -> Product:
        """保存产品"""
        print(f"🏗️  [基础设施层] 保存产品: {product.name}")
        self.products[product.id] = product
        return product

class OrderInfraRepository:
    """订单基础设施仓储"""
    def __init__(self):
        self.orders: Dict[int, Order] = {}
        self.next_id = 1
    
    def save(self, order: Order) -> Order:
        """保存订单"""
        if order.id == 0:
            order.id = self.next_id
            self.next_id += 1
        
        print(f"🏗️  [基础设施层] 保存订单: {order.id}")
        self.orders[order.id] = order
        return order
    
    def find_by_id(self, order_id: int) -> Optional[Order]:
        """根据ID查找订单"""
        print(f"🏗️  [基础设施层] 查询订单: {order_id}")
        return self.orders.get(order_id)
    
    def find_by_customer(self, customer_id: int) -> List[Order]:
        """根据客户ID查找订单"""
        print(f"🏗️  [基础设施层] 查询客户订单: {customer_id}")
        return [order for order in self.orders.values() if order.customer_id == customer_id]

# 应用服务层 (Application Service Layer)
class ProductApplicationService:
    """产品应用服务"""
    def __init__(self, product_repo: ProductInfraRepository):
        self.product_repo = product_repo
    
    def get_product_catalog(self) -> List[Dict]:
        """获取产品目录"""
        print("⚙️  [应用层] 获取产品目录")
        products = self.product_repo.find_all()
        
        return [{
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "category": p.category,
            "stock": p.stock,
            "available": p.is_available()
        } for p in products]
    
    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        """根据ID获取产品"""
        print(f"⚙️  [应用层] 获取产品: {product_id}")
        product = self.product_repo.find_by_id(product_id)
        
        if product:
            return {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "category": product.category,
                "stock": product.stock,
                "available": product.is_available(),
                "created_at": product.created_at.isoformat()
            }
        return None

class OrderApplicationService:
    """订单应用服务"""
    def __init__(self, order_repo: OrderInfraRepository, product_repo: ProductInfraRepository):
        self.order_repo = order_repo
        self.product_repo = product_repo
        self.domain_service = OrderDomainService()
    
    def create_order(self, customer_id: int, items: List[Dict], customer_type: str = "regular") -> Dict[str, Any]:
        """创建订单"""
        print(f"⚙️  [应用层] 创建订单: 客户{customer_id}")
        
        # 领域验证
        validation = self.domain_service.validate_order_creation(customer_id, items)
        if not validation["valid"]:
            return {"success": False, "message": validation["message"]}
        
        # 创建订单实体
        order = Order(0, customer_id)
        
        # 添加订单项
        for item in items:
            product = self.product_repo.find_by_id(item["product_id"])
            if not product:
                return {"success": False, "message": f"产品 {item['product_id']} 不存在"}
            
            if not order.add_item(product, item["quantity"]):
                return {"success": False, "message": f"产品 {product.name} 库存不足"}
            
            # 预留库存
            product.reserve_stock(item["quantity"])
            self.product_repo.save(product)
        
        # 计算折扣
        discount = self.domain_service.calculate_discount(order, customer_type)
        order.total_amount = order.calculate_total() - discount
        
        # 保存订单
        saved_order = self.order_repo.save(order)
        
        return {
            "success": True,
            "message": "订单创建成功",
            "order_id": saved_order.id,
            "total_amount": saved_order.total_amount,
            "discount": discount
        }
    
    def get_order_details(self, order_id: int) -> Optional[Dict]:
        """获取订单详情"""
        print(f"⚙️  [应用层] 获取订单详情: {order_id}")
        order = self.order_repo.find_by_id(order_id)
        
        if order:
            return {
                "id": order.id,
                "customer_id": order.customer_id,
                "items": order.items,
                "total_amount": order.total_amount,
                "status": order.status.value,
                "created_at": order.created_at.isoformat()
            }
        return None
    
    def update_order_status(self, order_id: int, new_status: str) -> Dict[str, Any]:
        """更新订单状态"""
        print(f"⚙️  [应用层] 更新订单状态: {order_id} -> {new_status}")
        
        order = self.order_repo.find_by_id(order_id)
        if not order:
            return {"success": False, "message": "订单不存在"}
        
        try:
            new_status_enum = OrderStatus(new_status)
            if order.update_status(new_status_enum):
                self.order_repo.save(order)
                return {"success": True, "message": "状态更新成功"}
            else:
                return {"success": False, "message": "无效的状态转换"}
        except ValueError:
            return {"success": False, "message": "无效的状态值"}

# 表示层 (Presentation Layer)
class ECommerceWebController:
    """电商Web控制器 - 表示层"""
    def __init__(self, product_app_service: ProductApplicationService, order_app_service: OrderApplicationService):
        self.product_app_service = product_app_service
        self.order_app_service = order_app_service
    
    def show_product_catalog(self):
        """显示产品目录"""
        print("🌐 [表示层] 显示产品目录")
        products = self.product_app_service.get_product_catalog()
        
        print("\n🛍️  产品目录:")
        print(f"{'ID':<5} {'名称':<15} {'价格':<10} {'库存':<8} {'状态':<8}")
        print("-" * 50)
        
        for product in products:
            status = "有货" if product["available"] else "缺货"
            print(f"{product['id']:<5} {product['name']:<15} ¥{product['price']:<9.2f} {product['stock']:<8} {status:<8}")
    
    def show_product_details(self, product_id: int):
        """显示产品详情"""
        print(f"🌐 [表示层] 显示产品详情: {product_id}")
        product = self.product_app_service.get_product_by_id(product_id)
        
        if product:
            print(f"\n📦 产品详情:")
            print(f"  ID: {product['id']}")
            print(f"  名称: {product['name']}")
            print(f"  价格: ¥{product['price']:.2f}")
            print(f"  分类: {product['category']}")
            print(f"  库存: {product['stock']}")
            print(f"  状态: {'有货' if product['available'] else '缺货'}")
        else:
            print("❌ 产品不存在")
    
    def create_order_request(self, customer_id: int, items: List[Dict], customer_type: str = "regular"):
        """处理创建订单请求"""
        print(f"🌐 [表示层] 处理创建订单请求: 客户{customer_id}")
        result = self.order_app_service.create_order(customer_id, items, customer_type)
        
        if result["success"]:
            print(f"\n✅ {result['message']}")
            print(f"订单号: {result['order_id']}")
            print(f"总金额: ¥{result['total_amount']:.2f}")
            if result['discount'] > 0:
                print(f"折扣金额: ¥{result['discount']:.2f}")
        else:
            print(f"❌ {result['message']}")
    
    def show_order_details(self, order_id: int):
        """显示订单详情"""
        print(f"🌐 [表示层] 显示订单详情: {order_id}")
        order = self.order_app_service.get_order_details(order_id)
        
        if order:
            print(f"\n📋 订单详情:")
            print(f"  订单号: {order['id']}")
            print(f"  客户ID: {order['customer_id']}")
            print(f"  总金额: ¥{order['total_amount']:.2f}")
            print(f"  状态: {order['status']}")
            print("  订单明细:")
            for item in order['items']:
                print(f"    - {item['product_name']} x{item['quantity']} = ¥{item['total_price']:.2f}")
        else:
            print("❌ 订单不存在")


def demo_four_layer_architecture():
    """演示四层架构"""
    print("🔹 四层架构演示 (DDD风格)")
    print("-" * 30)
    
    # 初始化各层
    # 基础设施层
    product_repo = ProductInfraRepository()
    order_repo = OrderInfraRepository()
    
    # 应用服务层
    product_app_service = ProductApplicationService(product_repo)
    order_app_service = OrderApplicationService(order_repo, product_repo)
    
    # 表示层
    web_controller = ECommerceWebController(product_app_service, order_app_service)
    
    # 演示功能
    web_controller.show_product_catalog()
    
    print("\n" + "="*50)
    web_controller.show_product_details(1)
    
    print("\n" + "="*50)
    # 创建VIP客户订单
    items = [
        {"product_id": 1, "quantity": 1},
        {"product_id": 2, "quantity": 1}
    ]
    web_controller.create_order_request(1, items, "vip")
    
    print("\n" + "="*50)
    web_controller.show_order_details(1)
    
    print("\n" + "="*50)
    # 更新订单状态
    result = order_app_service.update_order_status(1, OrderStatus.CONFIRMED.value)
    print(f"状态更新结果: {result['message']}")


if __name__ == "__main__":
    # 演示三层架构
    demo_three_layer_architecture()
    
    # 演示四层架构
    demo_four_layer_architecture()
    
    print("\n" + "="*60)
    print("✅ 分层架构演示完成！")
    print("\n架构对比总结:")
    print("📊 三层架构:")
    print("  - 表示层: 用户界面和控制器")
    print("  - 业务逻辑层: 业务规则和流程")
    print("  - 数据访问层: 数据存储和检索")
    print("\n🏗️  四层架构 (DDD):")
    print("  - 表示层: 用户界面和API")
    print("  - 应用服务层: 应用逻辑和协调")
    print("  - 领域层: 业务实体和领域逻辑")
    print("  - 基础设施层: 数据访问和外部服务")