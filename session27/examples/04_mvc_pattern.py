#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MVC架构模式详细示例

本文件演示了MVC（Model-View-Controller）架构模式的实现：
1. 传统MVC模式
2. Web MVC模式
3. MVP模式（Model-View-Presenter）
4. MVVM模式（Model-View-ViewModel）
5. 事件驱动的MVC
6. 组件化MVC
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import json


# ============================================================================
# 1. 传统MVC模式
# ============================================================================

print("1. 传统MVC模式演示")
print("=" * 40)

# Model层 - 数据和业务逻辑
class User:
    """用户模型"""
    def __init__(self, user_id: int, username: str, email: str, age: int):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.age = age
        self.created_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'age': self.age,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def __str__(self):
        return f"User(id={self.user_id}, username='{self.username}', email='{self.email}')"

class UserModel:
    """用户数据模型 - 负责数据管理和业务逻辑"""
    def __init__(self):
        self._users: Dict[int, User] = {}
        self._next_id = 1
        self._observers: List[Callable] = []
    
    def add_observer(self, observer: Callable):
        """添加观察者"""
        self._observers.append(observer)
    
    def remove_observer(self, observer: Callable):
        """移除观察者"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def _notify_observers(self, event: str, data: Any = None):
        """通知观察者"""
        for observer in self._observers:
            observer(event, data)
    
    def create_user(self, username: str, email: str, age: int) -> User:
        """创建用户"""
        # 业务逻辑验证
        if not username or len(username) < 3:
            raise ValueError("用户名至少需要3个字符")
        
        if not email or '@' not in email:
            raise ValueError("邮箱格式不正确")
        
        if age < 0 or age > 150:
            raise ValueError("年龄必须在0-150之间")
        
        # 检查用户名是否已存在
        for user in self._users.values():
            if user.username == username:
                raise ValueError(f"用户名 '{username}' 已存在")
            if user.email == email:
                raise ValueError(f"邮箱 '{email}' 已被使用")
        
        # 创建用户
        user = User(self._next_id, username, email, age)
        self._users[self._next_id] = user
        self._next_id += 1
        
        # 通知观察者
        self._notify_observers('user_created', user)
        
        return user
    
    def get_user(self, user_id: int) -> Optional[User]:
        """获取用户"""
        return self._users.get(user_id)
    
    def get_all_users(self) -> List[User]:
        """获取所有用户"""
        return list(self._users.values())
    
    def update_user(self, user_id: int, **kwargs) -> bool:
        """更新用户"""
        user = self._users.get(user_id)
        if not user:
            return False
        
        # 更新用户信息
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        # 通知观察者
        self._notify_observers('user_updated', user)
        
        return True
    
    def delete_user(self, user_id: int) -> bool:
        """删除用户"""
        if user_id in self._users:
            user = self._users.pop(user_id)
            self._notify_observers('user_deleted', user)
            return True
        return False
    
    def search_users(self, keyword: str) -> List[User]:
        """搜索用户"""
        keyword = keyword.lower()
        results = []
        for user in self._users.values():
            if (keyword in user.username.lower() or 
                keyword in user.email.lower()):
                results.append(user)
        return results

# View层 - 用户界面
class UserView:
    """用户视图 - 负责显示用户界面"""
    
    def display_user(self, user: User):
        """显示单个用户信息"""
        print(f"👤 用户信息:")
        print(f"   ID: {user.user_id}")
        print(f"   用户名: {user.username}")
        print(f"   邮箱: {user.email}")
        print(f"   年龄: {user.age}")
        print(f"   创建时间: {user.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def display_user_list(self, users: List[User]):
        """显示用户列表"""
        if not users:
            print("📝 暂无用户数据")
            return
        
        print(f"📋 用户列表 (共 {len(users)} 个用户):")
        print("-" * 60)
        print(f"{'ID':<4} {'用户名':<15} {'邮箱':<25} {'年龄':<5}")
        print("-" * 60)
        
        for user in users:
            print(f"{user.user_id:<4} {user.username:<15} {user.email:<25} {user.age:<5}")
    
    def display_message(self, message: str, message_type: str = "info"):
        """显示消息"""
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌"
        }
        icon = icons.get(message_type, "ℹ️")
        print(f"{icon} {message}")
    
    def display_menu(self):
        """显示菜单"""
        print("\n" + "=" * 40)
        print("🏠 用户管理系统")
        print("=" * 40)
        print("1. 创建用户")
        print("2. 查看所有用户")
        print("3. 查看用户详情")
        print("4. 更新用户")
        print("5. 删除用户")
        print("6. 搜索用户")
        print("0. 退出")
        print("-" * 40)
    
    def get_user_input(self, prompt: str) -> str:
        """获取用户输入"""
        return input(f"📝 {prompt}: ").strip()
    
    def display_error(self, error: str):
        """显示错误信息"""
        self.display_message(f"错误: {error}", "error")
    
    def display_success(self, message: str):
        """显示成功信息"""
        self.display_message(message, "success")

# Controller层 - 控制逻辑
class UserController:
    """用户控制器 - 负责处理用户交互和协调Model与View"""
    
    def __init__(self, model: UserModel, view: UserView):
        self.model = model
        self.view = view
        
        # 注册为模型的观察者
        self.model.add_observer(self._on_model_change)
    
    def _on_model_change(self, event: str, data: Any):
        """响应模型变化"""
        if event == 'user_created':
            self.view.display_success(f"用户 '{data.username}' 创建成功")
        elif event == 'user_updated':
            self.view.display_success(f"用户 '{data.username}' 更新成功")
        elif event == 'user_deleted':
            self.view.display_success(f"用户 '{data.username}' 删除成功")
    
    def create_user(self):
        """创建用户"""
        try:
            username = self.view.get_user_input("请输入用户名")
            email = self.view.get_user_input("请输入邮箱")
            age_str = self.view.get_user_input("请输入年龄")
            
            if not username or not email or not age_str:
                self.view.display_error("所有字段都是必填的")
                return
            
            age = int(age_str)
            user = self.model.create_user(username, email, age)
            
        except ValueError as e:
            self.view.display_error(str(e))
        except Exception as e:
            self.view.display_error(f"创建用户失败: {str(e)}")
    
    def show_all_users(self):
        """显示所有用户"""
        users = self.model.get_all_users()
        self.view.display_user_list(users)
    
    def show_user_details(self):
        """显示用户详情"""
        try:
            user_id_str = self.view.get_user_input("请输入用户ID")
            user_id = int(user_id_str)
            
            user = self.model.get_user(user_id)
            if user:
                self.view.display_user(user)
            else:
                self.view.display_error(f"用户ID {user_id} 不存在")
                
        except ValueError:
            self.view.display_error("请输入有效的用户ID")
    
    def update_user(self):
        """更新用户"""
        try:
            user_id_str = self.view.get_user_input("请输入要更新的用户ID")
            user_id = int(user_id_str)
            
            user = self.model.get_user(user_id)
            if not user:
                self.view.display_error(f"用户ID {user_id} 不存在")
                return
            
            # 显示当前用户信息
            print("\n当前用户信息:")
            self.view.display_user(user)
            
            # 获取更新信息
            new_username = self.view.get_user_input(f"新用户名 (当前: {user.username}, 回车跳过)")
            new_email = self.view.get_user_input(f"新邮箱 (当前: {user.email}, 回车跳过)")
            new_age_str = self.view.get_user_input(f"新年龄 (当前: {user.age}, 回车跳过)")
            
            # 构建更新数据
            update_data = {}
            if new_username:
                update_data['username'] = new_username
            if new_email:
                update_data['email'] = new_email
            if new_age_str:
                update_data['age'] = int(new_age_str)
            
            if update_data:
                success = self.model.update_user(user_id, **update_data)
                if not success:
                    self.view.display_error("更新用户失败")
            else:
                self.view.display_message("没有进行任何更新")
                
        except ValueError as e:
            self.view.display_error(f"输入错误: {str(e)}")
    
    def delete_user(self):
        """删除用户"""
        try:
            user_id_str = self.view.get_user_input("请输入要删除的用户ID")
            user_id = int(user_id_str)
            
            user = self.model.get_user(user_id)
            if not user:
                self.view.display_error(f"用户ID {user_id} 不存在")
                return
            
            # 确认删除
            confirm = self.view.get_user_input(f"确认删除用户 '{user.username}' 吗? (y/N)")
            if confirm.lower() == 'y':
                success = self.model.delete_user(user_id)
                if not success:
                    self.view.display_error("删除用户失败")
            else:
                self.view.display_message("取消删除操作")
                
        except ValueError:
            self.view.display_error("请输入有效的用户ID")
    
    def search_users(self):
        """搜索用户"""
        keyword = self.view.get_user_input("请输入搜索关键词")
        if keyword:
            users = self.model.search_users(keyword)
            if users:
                print(f"\n🔍 搜索结果 (关键词: '{keyword}'):")
                self.view.display_user_list(users)
            else:
                self.view.display_message(f"没有找到包含 '{keyword}' 的用户")
        else:
            self.view.display_error("请输入搜索关键词")
    
    def run(self):
        """运行应用程序"""
        self.view.display_message("欢迎使用用户管理系统 (MVC架构演示)", "success")
        
        # 添加一些示例数据
        try:
            self.model.create_user("alice", "alice@example.com", 25)
            self.model.create_user("bob", "bob@example.com", 30)
            self.model.create_user("charlie", "charlie@example.com", 28)
            print("\n📊 已添加示例数据")
        except:
            pass
        
        while True:
            self.view.display_menu()
            choice = self.view.get_user_input("请选择操作")
            
            if choice == '1':
                self.create_user()
            elif choice == '2':
                self.show_all_users()
            elif choice == '3':
                self.show_user_details()
            elif choice == '4':
                self.update_user()
            elif choice == '5':
                self.delete_user()
            elif choice == '6':
                self.search_users()
            elif choice == '0':
                self.view.display_message("感谢使用，再见！", "success")
                break
            else:
                self.view.display_error("无效的选择，请重新输入")

# 演示传统MVC模式
print("🔹 传统MVC模式演示:")

# 创建MVC组件
user_model = UserModel()
user_view = UserView()
user_controller = UserController(user_model, user_view)

# 演示基本功能（非交互式）
print("\n📝 创建示例用户:")
try:
    user1 = user_model.create_user("demo_user", "demo@example.com", 25)
    user_view.display_user(user1)
except Exception as e:
    user_view.display_error(str(e))

print("\n📋 显示所有用户:")
all_users = user_model.get_all_users()
user_view.display_user_list(all_users)

print("\n🔍 搜索用户:")
search_results = user_model.search_users("demo")
user_view.display_user_list(search_results)

print()


# ============================================================================
# 2. Web MVC模式
# ============================================================================

print("2. Web MVC模式演示")
print("=" * 40)

# HTTP请求和响应模拟
@dataclass
class HttpRequest:
    """HTTP请求模拟"""
    method: str
    path: str
    params: Dict[str, Any]
    body: Dict[str, Any]
    headers: Dict[str, str]

@dataclass
class HttpResponse:
    """HTTP响应模拟"""
    status_code: int
    headers: Dict[str, str]
    body: str
    content_type: str = "application/json"

class ProductModel:
    """产品模型 - Web应用"""
    def __init__(self):
        self._products = {
            1: {"id": 1, "name": "笔记本电脑", "price": 5999.0, "category": "电子产品", "stock": 50},
            2: {"id": 2, "name": "无线鼠标", "price": 99.0, "category": "电子产品", "stock": 200},
            3: {"id": 3, "name": "机械键盘", "price": 299.0, "category": "电子产品", "stock": 100}
        }
        self._next_id = 4
    
    def get_all_products(self) -> List[Dict]:
        """获取所有产品"""
        return list(self._products.values())
    
    def get_product(self, product_id: int) -> Optional[Dict]:
        """获取单个产品"""
        return self._products.get(product_id)
    
    def create_product(self, name: str, price: float, category: str, stock: int) -> Dict:
        """创建产品"""
        product = {
            "id": self._next_id,
            "name": name,
            "price": price,
            "category": category,
            "stock": stock
        }
        self._products[self._next_id] = product
        self._next_id += 1
        return product
    
    def update_product(self, product_id: int, **kwargs) -> bool:
        """更新产品"""
        if product_id in self._products:
            self._products[product_id].update(kwargs)
            return True
        return False
    
    def delete_product(self, product_id: int) -> bool:
        """删除产品"""
        if product_id in self._products:
            del self._products[product_id]
            return True
        return False

class ProductView:
    """产品视图 - Web应用"""
    
    def render_product_list(self, products: List[Dict]) -> str:
        """渲染产品列表"""
        return json.dumps({
            "status": "success",
            "data": products,
            "count": len(products)
        }, ensure_ascii=False, indent=2)
    
    def render_product_detail(self, product: Dict) -> str:
        """渲染产品详情"""
        return json.dumps({
            "status": "success",
            "data": product
        }, ensure_ascii=False, indent=2)
    
    def render_success(self, message: str, data: Any = None) -> str:
        """渲染成功响应"""
        response = {
            "status": "success",
            "message": message
        }
        if data:
            response["data"] = data
        return json.dumps(response, ensure_ascii=False, indent=2)
    
    def render_error(self, message: str, error_code: str = "UNKNOWN_ERROR") -> str:
        """渲染错误响应"""
        return json.dumps({
            "status": "error",
            "error_code": error_code,
            "message": message
        }, ensure_ascii=False, indent=2)
    
    def render_html_page(self, title: str, content: str) -> str:
        """渲染HTML页面"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .product {{ border: 1px solid #ddd; padding: 10px; margin: 10px 0; }}
        .price {{ color: #e74c3c; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    {content}
</body>
</html>
        """

class ProductController:
    """产品控制器 - Web应用"""
    
    def __init__(self, model: ProductModel, view: ProductView):
        self.model = model
        self.view = view
    
    def handle_request(self, request: HttpRequest) -> HttpResponse:
        """处理HTTP请求"""
        try:
            # 路由分发
            if request.method == "GET" and request.path == "/api/products":
                return self._get_products(request)
            elif request.method == "GET" and request.path.startswith("/api/products/"):
                return self._get_product(request)
            elif request.method == "POST" and request.path == "/api/products":
                return self._create_product(request)
            elif request.method == "PUT" and request.path.startswith("/api/products/"):
                return self._update_product(request)
            elif request.method == "DELETE" and request.path.startswith("/api/products/"):
                return self._delete_product(request)
            elif request.method == "GET" and request.path == "/products":
                return self._get_products_html(request)
            else:
                return HttpResponse(
                    status_code=404,
                    headers={"Content-Type": "application/json"},
                    body=self.view.render_error("接口不存在", "NOT_FOUND")
                )
        
        except Exception as e:
            return HttpResponse(
                status_code=500,
                headers={"Content-Type": "application/json"},
                body=self.view.render_error(f"服务器内部错误: {str(e)}", "INTERNAL_ERROR")
            )
    
    def _get_products(self, request: HttpRequest) -> HttpResponse:
        """获取产品列表"""
        products = self.model.get_all_products()
        
        # 支持分类筛选
        category = request.params.get("category")
        if category:
            products = [p for p in products if p["category"] == category]
        
        return HttpResponse(
            status_code=200,
            headers={"Content-Type": "application/json"},
            body=self.view.render_product_list(products)
        )
    
    def _get_product(self, request: HttpRequest) -> HttpResponse:
        """获取单个产品"""
        try:
            product_id = int(request.path.split("/")[-1])
            product = self.model.get_product(product_id)
            
            if product:
                return HttpResponse(
                    status_code=200,
                    headers={"Content-Type": "application/json"},
                    body=self.view.render_product_detail(product)
                )
            else:
                return HttpResponse(
                    status_code=404,
                    headers={"Content-Type": "application/json"},
                    body=self.view.render_error("产品不存在", "PRODUCT_NOT_FOUND")
                )
        
        except ValueError:
            return HttpResponse(
                status_code=400,
                headers={"Content-Type": "application/json"},
                body=self.view.render_error("无效的产品ID", "INVALID_PRODUCT_ID")
            )
    
    def _create_product(self, request: HttpRequest) -> HttpResponse:
        """创建产品"""
        try:
            data = request.body
            required_fields = ["name", "price", "category", "stock"]
            
            # 验证必填字段
            for field in required_fields:
                if field not in data:
                    return HttpResponse(
                        status_code=400,
                        headers={"Content-Type": "application/json"},
                        body=self.view.render_error(f"缺少必填字段: {field}", "MISSING_FIELD")
                    )
            
            # 创建产品
            product = self.model.create_product(
                name=data["name"],
                price=float(data["price"]),
                category=data["category"],
                stock=int(data["stock"])
            )
            
            return HttpResponse(
                status_code=201,
                headers={"Content-Type": "application/json"},
                body=self.view.render_success("产品创建成功", product)
            )
        
        except (ValueError, TypeError) as e:
            return HttpResponse(
                status_code=400,
                headers={"Content-Type": "application/json"},
                body=self.view.render_error(f"数据格式错误: {str(e)}", "INVALID_DATA")
            )
    
    def _update_product(self, request: HttpRequest) -> HttpResponse:
        """更新产品"""
        try:
            product_id = int(request.path.split("/")[-1])
            data = request.body
            
            if not self.model.get_product(product_id):
                return HttpResponse(
                    status_code=404,
                    headers={"Content-Type": "application/json"},
                    body=self.view.render_error("产品不存在", "PRODUCT_NOT_FOUND")
                )
            
            # 更新产品
            success = self.model.update_product(product_id, **data)
            
            if success:
                updated_product = self.model.get_product(product_id)
                return HttpResponse(
                    status_code=200,
                    headers={"Content-Type": "application/json"},
                    body=self.view.render_success("产品更新成功", updated_product)
                )
            else:
                return HttpResponse(
                    status_code=500,
                    headers={"Content-Type": "application/json"},
                    body=self.view.render_error("更新失败", "UPDATE_FAILED")
                )
        
        except ValueError:
            return HttpResponse(
                status_code=400,
                headers={"Content-Type": "application/json"},
                body=self.view.render_error("无效的产品ID", "INVALID_PRODUCT_ID")
            )
    
    def _delete_product(self, request: HttpRequest) -> HttpResponse:
        """删除产品"""
        try:
            product_id = int(request.path.split("/")[-1])
            
            if not self.model.get_product(product_id):
                return HttpResponse(
                    status_code=404,
                    headers={"Content-Type": "application/json"},
                    body=self.view.render_error("产品不存在", "PRODUCT_NOT_FOUND")
                )
            
            success = self.model.delete_product(product_id)
            
            if success:
                return HttpResponse(
                    status_code=200,
                    headers={"Content-Type": "application/json"},
                    body=self.view.render_success("产品删除成功")
                )
            else:
                return HttpResponse(
                    status_code=500,
                    headers={"Content-Type": "application/json"},
                    body=self.view.render_error("删除失败", "DELETE_FAILED")
                )
        
        except ValueError:
            return HttpResponse(
                status_code=400,
                headers={"Content-Type": "application/json"},
                body=self.view.render_error("无效的产品ID", "INVALID_PRODUCT_ID")
            )
    
    def _get_products_html(self, request: HttpRequest) -> HttpResponse:
        """获取产品HTML页面"""
        products = self.model.get_all_products()
        
        content = ""
        for product in products:
            content += f"""
            <div class="product">
                <h3>{product['name']}</h3>
                <p>分类: {product['category']}</p>
                <p class="price">价格: ¥{product['price']:.2f}</p>
                <p>库存: {product['stock']}</p>
            </div>
            """
        
        html = self.view.render_html_page("产品列表", content)
        
        return HttpResponse(
            status_code=200,
            headers={"Content-Type": "text/html; charset=utf-8"},
            body=html
        )

# 演示Web MVC模式
print("🔹 Web MVC模式演示:")

# 创建Web MVC组件
product_model = ProductModel()
product_view = ProductView()
product_controller = ProductController(product_model, product_view)

# 模拟HTTP请求
requests = [
    HttpRequest("GET", "/api/products", {}, {}, {}),
    HttpRequest("GET", "/api/products/1", {}, {}, {}),
    HttpRequest("POST", "/api/products", {}, {
        "name": "智能手表",
        "price": 1299.0,
        "category": "电子产品",
        "stock": 30
    }, {}),
    HttpRequest("GET", "/api/products", {"category": "电子产品"}, {}, {})
]

for i, req in enumerate(requests, 1):
    print(f"\n📡 请求 {i}: {req.method} {req.path}")
    if req.body:
        print(f"   请求体: {req.body}")
    
    response = product_controller.handle_request(req)
    print(f"   响应状态: {response.status_code}")
    print(f"   响应内容: {response.body[:200]}..." if len(response.body) > 200 else f"   响应内容: {response.body}")

print()


# ============================================================================
# 3. MVP模式 (Model-View-Presenter)
# ============================================================================

print("3. MVP模式演示")
print("=" * 40)

# View接口
class ITaskView(ABC):
    """任务视图接口"""
    @abstractmethod
    def show_tasks(self, tasks: List[Dict]):
        pass
    
    @abstractmethod
    def show_message(self, message: str):
        pass
    
    @abstractmethod
    def show_error(self, error: str):
        pass
    
    @abstractmethod
    def get_task_input(self) -> Dict[str, str]:
        pass

# Model
class TaskModel:
    """任务模型"""
    def __init__(self):
        self._tasks = [
            {"id": 1, "title": "学习Python", "completed": False, "priority": "high"},
            {"id": 2, "title": "写项目文档", "completed": True, "priority": "medium"},
            {"id": 3, "title": "代码审查", "completed": False, "priority": "low"}
        ]
        self._next_id = 4
    
    def get_all_tasks(self) -> List[Dict]:
        return self._tasks.copy()
    
    def add_task(self, title: str, priority: str = "medium") -> Dict:
        task = {
            "id": self._next_id,
            "title": title,
            "completed": False,
            "priority": priority
        }
        self._tasks.append(task)
        self._next_id += 1
        return task
    
    def toggle_task(self, task_id: int) -> bool:
        for task in self._tasks:
            if task["id"] == task_id:
                task["completed"] = not task["completed"]
                return True
        return False
    
    def delete_task(self, task_id: int) -> bool:
        for i, task in enumerate(self._tasks):
            if task["id"] == task_id:
                del self._tasks[i]
                return True
        return False

# View实现
class ConsoleTaskView(ITaskView):
    """控制台任务视图"""
    
    def show_tasks(self, tasks: List[Dict]):
        if not tasks:
            print("📝 暂无任务")
            return
        
        print("\n📋 任务列表:")
        print("-" * 60)
        for task in tasks:
            status = "✅" if task["completed"] else "⏳"
            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task["priority"], "⚪")
            print(f"{status} [{task['id']}] {task['title']} {priority_icon}")
    
    def show_message(self, message: str):
        print(f"ℹ️ {message}")
    
    def show_error(self, error: str):
        print(f"❌ 错误: {error}")
    
    def get_task_input(self) -> Dict[str, str]:
        title = input("📝 请输入任务标题: ").strip()
        priority = input("🎯 请输入优先级 (high/medium/low, 默认medium): ").strip() or "medium"
        return {"title": title, "priority": priority}

# Presenter
class TaskPresenter:
    """任务展示器 - MVP模式的核心"""
    
    def __init__(self, model: TaskModel, view: ITaskView):
        self.model = model
        self.view = view
    
    def load_tasks(self):
        """加载任务"""
        try:
            tasks = self.model.get_all_tasks()
            self.view.show_tasks(tasks)
        except Exception as e:
            self.view.show_error(f"加载任务失败: {str(e)}")
    
    def add_task(self):
        """添加任务"""
        try:
            task_data = self.view.get_task_input()
            
            if not task_data["title"]:
                self.view.show_error("任务标题不能为空")
                return
            
            if task_data["priority"] not in ["high", "medium", "low"]:
                self.view.show_error("优先级必须是 high、medium 或 low")
                return
            
            task = self.model.add_task(task_data["title"], task_data["priority"])
            self.view.show_message(f"任务 '{task['title']}' 添加成功")
            self.load_tasks()
            
        except Exception as e:
            self.view.show_error(f"添加任务失败: {str(e)}")
    
    def toggle_task(self, task_id: int):
        """切换任务状态"""
        try:
            success = self.model.toggle_task(task_id)
            if success:
                self.view.show_message(f"任务 {task_id} 状态已更新")
                self.load_tasks()
            else:
                self.view.show_error(f"任务 {task_id} 不存在")
        except Exception as e:
            self.view.show_error(f"更新任务失败: {str(e)}")
    
    def delete_task(self, task_id: int):
        """删除任务"""
        try:
            success = self.model.delete_task(task_id)
            if success:
                self.view.show_message(f"任务 {task_id} 已删除")
                self.load_tasks()
            else:
                self.view.show_error(f"任务 {task_id} 不存在")
        except Exception as e:
            self.view.show_error(f"删除任务失败: {str(e)}")
    
    def get_task_statistics(self):
        """获取任务统计"""
        try:
            tasks = self.model.get_all_tasks()
            total = len(tasks)
            completed = len([t for t in tasks if t["completed"]])
            pending = total - completed
            
            high_priority = len([t for t in tasks if t["priority"] == "high" and not t["completed"]])
            
            stats_message = f"📊 任务统计: 总计 {total}, 已完成 {completed}, 待完成 {pending}, 高优先级待办 {high_priority}"
            self.view.show_message(stats_message)
            
        except Exception as e:
            self.view.show_error(f"获取统计失败: {str(e)}")

# 演示MVP模式
print("🔹 MVP模式演示:")

# 创建MVP组件
task_model = TaskModel()
task_view = ConsoleTaskView()
task_presenter = TaskPresenter(task_model, task_view)

# 演示功能
print("\n📋 初始任务列表:")
task_presenter.load_tasks()

print("\n📊 任务统计:")
task_presenter.get_task_statistics()

print("\n✅ 完成任务1:")
task_presenter.toggle_task(1)

print("\n🗑️ 删除任务2:")
task_presenter.delete_task(2)

print("\n📊 更新后的统计:")
task_presenter.get_task_statistics()

print()


# ============================================================================
# 总结和对比
# ============================================================================

print("MVC架构模式总结")
print("=" * 50)

print("✅ MVC模式的优点:")
print("  1. 关注点分离 - Model、View、Controller各司其职")
print("  2. 可维护性强 - 修改一层不影响其他层")
print("  3. 可测试性好 - 各层可以独立测试")
print("  4. 代码复用 - View和Model可以被多个Controller使用")
print("  5. 并行开发 - 团队可以同时开发不同层")

print("\n📊 不同MVC变体对比:")
print("  传统MVC: View观察Model，Controller处理用户输入")
print("  Web MVC: Controller处理HTTP请求，View渲染响应")
print("  MVP: Presenter完全控制View，View不直接访问Model")
print("  MVVM: ViewModel绑定View，支持双向数据绑定")

print("\n🎯 适用场景:")
print("  传统MVC: 桌面应用程序")
print("  Web MVC: Web应用程序和API")
print("  MVP: 需要复杂UI逻辑的应用")
print("  MVVM: 支持数据绑定的现代UI框架")

print("\n🔧 实施建议:")
print("  1. 保持Model的纯净性，只包含业务逻辑")
print("  2. View应该尽可能简单，只负责显示")
print("  3. Controller/Presenter处理用户交互和协调")
print("  4. 使用依赖注入降低耦合度")
print("  5. 考虑使用观察者模式实现松耦合")