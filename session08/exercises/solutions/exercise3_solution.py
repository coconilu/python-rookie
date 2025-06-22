#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session08 练习题3参考答案：购物车系统

这是exercise3.py的参考答案，展示了如何设计一个完整的购物车系统。
"""

from datetime import datetime
from typing import List, Optional, Dict, Any


class Product:
    """商品类 - 管理商品信息"""
    
    # 类变量
    total_products = 0
    
    def __init__(self, product_id: str, name: str, price: float, category: str = "其他"):
        """初始化商品信息
        
        Args:
            product_id (str): 商品ID
            name (str): 商品名称
            price (float): 商品价格
            category (str): 商品分类，默认为"其他"
        
        Raises:
            ValueError: 当参数无效时
        """
        # 参数验证
        if not isinstance(product_id, str) or not product_id.strip():
            raise ValueError("商品ID必须是非空字符串")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("商品名称必须是非空字符串")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("商品价格必须是非负数")
        if not isinstance(category, str) or not category.strip():
            raise ValueError("商品分类必须是非空字符串")
        
        # 初始化实例变量
        self.product_id = product_id.strip()
        self.name = name.strip()
        self.price = float(price)
        self.category = category.strip()
        
        # 更新商品总数
        Product.total_products += 1
    
    def get_info(self) -> str:
        """获取商品信息
        
        Returns:
            str: 格式化的商品信息
        """
        return f"[{self.product_id}] {self.name} - ¥{self.price:.2f} ({self.category})"
    
    def apply_discount(self, discount_rate: float) -> float:
        """计算折扣价格
        
        Args:
            discount_rate (float): 折扣率（0-1之间）
        
        Returns:
            float: 折扣后价格
        
        Raises:
            ValueError: 当折扣率无效时
        """
        if not isinstance(discount_rate, (int, float)) or not (0 <= discount_rate <= 1):
            raise ValueError("折扣率必须在0-1之间")
        
        discount_price = self.price * discount_rate
        return round(discount_price, 2)
    
    @classmethod
    def get_total_products(cls) -> int:
        """获取商品总数（类方法）
        
        Returns:
            int: 商品总数
        """
        return cls.total_products
    
    @staticmethod
    def is_valid_price(price: Any) -> bool:
        """验证价格是否有效（静态方法）
        
        Args:
            price: 待验证的价格
        
        Returns:
            bool: 价格是否有效
        """
        try:
            price_float = float(price)
            return price_float >= 0
        except (ValueError, TypeError):
            return False
    
    def __str__(self) -> str:
        """字符串表示（用户友好）"""
        return f"{self.name} (¥{self.price:.2f})"
    
    def __repr__(self) -> str:
        """字符串表示（开发者友好）"""
        return f"Product('{self.product_id}', '{self.name}', {self.price}, '{self.category}')"
    
    def __eq__(self, other) -> bool:
        """相等比较（按商品ID）"""
        if isinstance(other, Product):
            return self.product_id == other.product_id
        return False
    
    def __hash__(self) -> int:
        """哈希值（基于商品ID）"""
        return hash(self.product_id)
    
    def __lt__(self, other) -> bool:
        """小于比较（按价格）"""
        if isinstance(other, Product):
            return self.price < other.price
        return NotImplemented


class CartItem:
    """购物车项目类 - 管理购物车中的单个商品项目"""
    
    def __init__(self, product: Product, quantity: int = 1):
        """初始化购物车项目
        
        Args:
            product (Product): 商品对象
            quantity (int): 数量，默认为1
        
        Raises:
            ValueError: 当参数无效时
            TypeError: 当参数类型不正确时
        """
        if not isinstance(product, Product):
            raise TypeError("product必须是Product类的实例")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("数量必须是正整数")
        
        self.product = product
        self.quantity = quantity
        self.added_time = datetime.now()
    
    def get_subtotal(self) -> float:
        """计算小计金额
        
        Returns:
            float: 小计金额
        """
        return round(self.product.price * self.quantity, 2)
    
    def update_quantity(self, new_quantity: int) -> None:
        """更新数量
        
        Args:
            new_quantity (int): 新数量
        
        Raises:
            ValueError: 当数量无效时
        """
        if not isinstance(new_quantity, int) or new_quantity <= 0:
            raise ValueError("数量必须是正整数")
        
        old_quantity = self.quantity
        self.quantity = new_quantity
        print(f"更新数量：{self.product.name} {old_quantity} -> {new_quantity}")
    
    def increase_quantity(self, amount: int = 1) -> None:
        """增加数量
        
        Args:
            amount (int): 增加的数量，默认为1
        
        Raises:
            ValueError: 当数量无效时
        """
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("增加数量必须是正整数")
        
        self.quantity += amount
        print(f"增加数量：{self.product.name} +{amount} = {self.quantity}")
    
    def decrease_quantity(self, amount: int = 1) -> bool:
        """减少数量
        
        Args:
            amount (int): 减少的数量，默认为1
        
        Returns:
            bool: 操作是否成功
        
        Raises:
            ValueError: 当数量无效时
        """
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("减少数量必须是正整数")
        
        if self.quantity > amount:
            self.quantity -= amount
            print(f"减少数量：{self.product.name} -{amount} = {self.quantity}")
            return True
        else:
            print(f"无法减少：{self.product.name} 当前数量{self.quantity}，无法减少{amount}")
            return False
    
    def get_info(self) -> str:
        """获取项目信息
        
        Returns:
            str: 格式化的项目信息
        """
        subtotal = self.get_subtotal()
        return f"{self.product.name} x{self.quantity} = ¥{subtotal:.2f}"
    
    def __str__(self) -> str:
        """字符串表示（用户友好）"""
        return f"{self.product.name} x{self.quantity}"
    
    def __repr__(self) -> str:
        """字符串表示（开发者友好）"""
        return f"CartItem({self.product!r}, {self.quantity})"
    
    def __eq__(self, other) -> bool:
        """相等比较（按商品ID）"""
        if isinstance(other, CartItem):
            return self.product.product_id == other.product.product_id
        return False
    
    def __hash__(self) -> int:
        """哈希值（基于商品ID）"""
        return hash(self.product.product_id)


class ShoppingCart:
    """购物车类 - 管理购物车操作"""
    
    # 类变量
    total_carts = 0
    
    def __init__(self, cart_id: Optional[str] = None):
        """初始化购物车
        
        Args:
            cart_id (str, optional): 购物车ID，如果不提供则自动生成
        """
        ShoppingCart.total_carts += 1
        
        if cart_id is None:
            self.cart_id = f"CART_{ShoppingCart.total_carts:06d}"
        else:
            self.cart_id = str(cart_id)
        
        self.items: Dict[str, CartItem] = {}  # 使用商品ID作为键
        self.created_time = datetime.now()
        self.last_modified = datetime.now()
    
    def add_item(self, product: Product, quantity: int = 1) -> None:
        """添加商品到购物车
        
        Args:
            product (Product): 商品对象
            quantity (int): 数量，默认为1
        
        Raises:
            TypeError: 当product不是Product实例时
            ValueError: 当数量无效时
        """
        if not isinstance(product, Product):
            raise TypeError("product必须是Product类的实例")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("数量必须是正整数")
        
        product_id = product.product_id
        
        if product_id in self.items:
            # 如果商品已存在，增加数量
            self.items[product_id].increase_quantity(quantity)
        else:
            # 如果商品不存在，创建新项目
            self.items[product_id] = CartItem(product, quantity)
            print(f"添加商品：{product.name} x{quantity}")
        
        self._update_modified_time()
    
    def remove_item(self, product_id: str) -> bool:
        """从购物车移除商品
        
        Args:
            product_id (str): 商品ID
        
        Returns:
            bool: 移除是否成功
        """
        if product_id in self.items:
            removed_item = self.items.pop(product_id)
            print(f"移除商品：{removed_item.product.name}")
            self._update_modified_time()
            return True
        else:
            print(f"未找到商品ID：{product_id}")
            return False
    
    def update_quantity(self, product_id: str, new_quantity: int) -> bool:
        """更新商品数量
        
        Args:
            product_id (str): 商品ID
            new_quantity (int): 新数量
        
        Returns:
            bool: 更新是否成功
        """
        if product_id in self.items:
            if new_quantity <= 0:
                return self.remove_item(product_id)
            else:
                self.items[product_id].update_quantity(new_quantity)
                self._update_modified_time()
                return True
        else:
            print(f"未找到商品ID：{product_id}")
            return False
    
    def get_item(self, product_id: str) -> Optional[CartItem]:
        """获取购物车项目
        
        Args:
            product_id (str): 商品ID
        
        Returns:
            CartItem or None: 购物车项目，如果不存在返回None
        """
        return self.items.get(product_id)
    
    def calculate_total(self) -> float:
        """计算购物车总金额
        
        Returns:
            float: 总金额
        """
        total = sum(item.get_subtotal() for item in self.items.values())
        return round(total, 2)
    
    def calculate_total_with_discount(self, discount_rate: float = 0.0) -> float:
        """计算折扣后总金额
        
        Args:
            discount_rate (float): 折扣率（0-1之间），默认为0
        
        Returns:
            float: 折扣后总金额
        
        Raises:
            ValueError: 当折扣率无效时
        """
        if not isinstance(discount_rate, (int, float)) or not (0 <= discount_rate <= 1):
            raise ValueError("折扣率必须在0-1之间")
        
        original_total = self.calculate_total()
        discount_amount = original_total * discount_rate
        final_total = original_total - discount_amount
        return round(final_total, 2)
    
    def get_item_count(self) -> int:
        """获取商品种类数量
        
        Returns:
            int: 商品种类数量
        """
        return len(self.items)
    
    def get_total_quantity(self) -> int:
        """获取商品总数量
        
        Returns:
            int: 商品总数量
        """
        return sum(item.quantity for item in self.items.values())
    
    def clear(self) -> None:
        """清空购物车"""
        item_count = len(self.items)
        self.items.clear()
        self._update_modified_time()
        print(f"购物车已清空，移除了{item_count}种商品")
    
    def is_empty(self) -> bool:
        """判断购物车是否为空
        
        Returns:
            bool: 是否为空
        """
        return len(self.items) == 0
    
    def get_items_by_category(self, category: str) -> List[CartItem]:
        """按分类获取商品项目
        
        Args:
            category (str): 商品分类
        
        Returns:
            List[CartItem]: 指定分类的商品项目列表
        """
        return [item for item in self.items.values() 
                if item.product.category == category]
    
    def get_expensive_items(self, threshold: float = 100.0) -> List[CartItem]:
        """获取昂贵商品项目
        
        Args:
            threshold (float): 价格阈值，默认100元
        
        Returns:
            List[CartItem]: 昂贵商品项目列表
        """
        return [item for item in self.items.values() 
                if item.product.price >= threshold]
    
    def get_cart_summary(self) -> str:
        """获取购物车摘要
        
        Returns:
            str: 格式化的购物车摘要
        """
        if self.is_empty():
            return f"购物车 {self.cart_id} 为空"
        
        summary = [
            f"购物车ID：{self.cart_id}",
            f"创建时间：{self.created_time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"最后修改：{self.last_modified.strftime('%Y-%m-%d %H:%M:%S')}",
            f"商品种类：{self.get_item_count()}种",
            f"商品总数：{self.get_total_quantity()}件",
            f"总金额：¥{self.calculate_total():.2f}",
            "",
            "商品详情："
        ]
        
        # 按价格排序显示商品
        sorted_items = sorted(self.items.values(), 
                            key=lambda x: x.product.price, reverse=True)
        
        for item in sorted_items:
            summary.append(f"  {item.get_info()}")
        
        return "\n".join(summary)
    
    def _update_modified_time(self) -> None:
        """更新最后修改时间（私有方法）"""
        self.last_modified = datetime.now()
    
    @classmethod
    def get_total_carts(cls) -> int:
        """获取购物车总数（类方法）
        
        Returns:
            int: 购物车总数
        """
        return cls.total_carts
    
    @staticmethod
    def merge_carts(cart1: 'ShoppingCart', cart2: 'ShoppingCart') -> 'ShoppingCart':
        """合并两个购物车（静态方法）
        
        Args:
            cart1 (ShoppingCart): 第一个购物车
            cart2 (ShoppingCart): 第二个购物车
        
        Returns:
            ShoppingCart: 合并后的新购物车
        
        Raises:
            TypeError: 当参数不是ShoppingCart实例时
        """
        if not isinstance(cart1, ShoppingCart) or not isinstance(cart2, ShoppingCart):
            raise TypeError("参数必须是ShoppingCart类的实例")
        
        merged_cart = ShoppingCart(f"MERGED_{cart1.cart_id}_{cart2.cart_id}")
        
        # 添加第一个购物车的商品
        for item in cart1.items.values():
            merged_cart.add_item(item.product, item.quantity)
        
        # 添加第二个购物车的商品
        for item in cart2.items.values():
            merged_cart.add_item(item.product, item.quantity)
        
        return merged_cart
    
    def __str__(self) -> str:
        """字符串表示（用户友好）"""
        if self.is_empty():
            return f"购物车 {self.cart_id} (空)"
        
        total = self.calculate_total()
        item_count = self.get_item_count()
        total_quantity = self.get_total_quantity()
        return f"购物车 {self.cart_id} ({item_count}种商品，共{total_quantity}件，¥{total:.2f})"
    
    def __repr__(self) -> str:
        """字符串表示（开发者友好）"""
        return f"ShoppingCart('{self.cart_id}')"
    
    def __len__(self) -> int:
        """返回商品种类数量"""
        return len(self.items)
    
    def __contains__(self, product_id: str) -> bool:
        """检查是否包含指定商品
        
        Args:
            product_id (str): 商品ID
        
        Returns:
            bool: 是否包含该商品
        """
        return product_id in self.items
    
    def __iter__(self):
        """迭代器，返回购物车项目"""
        return iter(self.items.values())
    
    def __getitem__(self, product_id: str) -> CartItem:
        """索引访问，获取指定商品项目
        
        Args:
            product_id (str): 商品ID
        
        Returns:
            CartItem: 购物车项目
        
        Raises:
            KeyError: 当商品不存在时
        """
        if product_id not in self.items:
            raise KeyError(f"购物车中不存在商品ID：{product_id}")
        return self.items[product_id]
    
    def __eq__(self, other) -> bool:
        """相等比较（按购物车ID）"""
        if isinstance(other, ShoppingCart):
            return self.cart_id == other.cart_id
        return False
    
    def __hash__(self) -> int:
        """哈希值（基于购物车ID）"""
        return hash(self.cart_id)


def test_shopping_cart():
    """测试购物车系统的功能"""
    print("=== 购物车系统测试 ===")
    
    # 1. 创建商品
    print("\n1. 创建商品：")
    print("-" * 40)
    
    try:
        # 创建各种商品
        products = [
            Product("P001", "iPhone 15 Pro", 7999.0, "电子产品"),
            Product("P002", "MacBook Air", 8999.0, "电子产品"),
            Product("P003", "Python编程书籍", 89.0, "图书"),
            Product("P004", "无线耳机", 299.0, "电子产品"),
            Product("P005", "咖啡杯", 39.0, "生活用品"),
            Product("P006", "机械键盘", 599.0, "电子产品")
        ]
        
        print(f"成功创建{len(products)}个商品")
        print(f"商品总数：{Product.get_total_products()}")
        
        print("\n商品列表：")
        for product in products:
            print(f"  {product.get_info()}")
        
    except ValueError as e:
        print(f"创建商品失败：{e}")
    
    # 2. 创建购物车
    print("\n2. 创建购物车：")
    print("-" * 40)
    
    cart1 = ShoppingCart("USER_001_CART")
    cart2 = ShoppingCart()  # 自动生成ID
    
    print(f"创建购物车：{cart1}")
    print(f"创建购物车：{cart2}")
    print(f"购物车总数：{ShoppingCart.get_total_carts()}")
    
    # 3. 添加商品到购物车
    print("\n3. 添加商品到购物车：")
    print("-" * 40)
    
    print("\n向cart1添加商品：")
    cart1.add_item(products[0], 1)  # iPhone
    cart1.add_item(products[2], 2)  # 书籍
    cart1.add_item(products[3], 1)  # 耳机
    cart1.add_item(products[4], 3)  # 咖啡杯
    
    print("\n向cart2添加商品：")
    cart2.add_item(products[1], 1)  # MacBook
    cart2.add_item(products[5], 1)  # 键盘
    cart2.add_item(products[2], 1)  # 书籍
    
    # 4. 显示购物车信息
    print("\n4. 购物车信息：")
    print("-" * 40)
    
    carts = [cart1, cart2]
    for i, cart in enumerate(carts, 1):
        print(f"\n购物车{i}：{cart}")
        print(cart.get_cart_summary())
    
    # 5. 测试购物车操作
    print("\n5. 购物车操作测试：")
    print("-" * 40)
    
    print("\n更新商品数量：")
    cart1.update_quantity("P004", 2)  # 耳机数量改为2
    
    print("\n移除商品：")
    cart1.remove_item("P005")  # 移除咖啡杯
    
    print("\n再次添加相同商品（测试数量累加）：")
    cart1.add_item(products[2], 1)  # 再添加1本书
    
    # 6. 测试特殊方法
    print("\n6. 特殊方法测试：")
    print("-" * 40)
    
    print(f"len(cart1): {len(cart1)}种商品")
    print(f"'P001' in cart1: {'P001' in cart1}")
    print(f"'P999' in cart1: {'P999' in cart1}")
    
    print("\n迭代购物车商品：")
    for item in cart1:
        print(f"  {item.get_info()}")
    
    print("\n索引访问：")
    try:
        iphone_item = cart1["P001"]
        print(f"  iPhone项目：{iphone_item.get_info()}")
    except KeyError as e:
        print(f"  访问失败：{e}")
    
    # 7. 测试分类和筛选
    print("\n7. 分类和筛选测试：")
    print("-" * 40)
    
    print("\ncart1中的电子产品：")
    electronic_items = cart1.get_items_by_category("电子产品")
    for item in electronic_items:
        print(f"  {item.get_info()}")
    
    print("\ncart1中的昂贵商品（>100元）：")
    expensive_items = cart1.get_expensive_items(100.0)
    for item in expensive_items:
        print(f"  {item.get_info()}")
    
    # 8. 测试折扣计算
    print("\n8. 折扣计算测试：")
    print("-" * 40)
    
    for cart in carts:
        original_total = cart.calculate_total()
        discount_total = cart.calculate_total_with_discount(0.1)  # 9折
        discount_amount = original_total - discount_total
        
        print(f"\n{cart.cart_id}：")
        print(f"  原价：¥{original_total:.2f}")
        print(f"  9折价：¥{discount_total:.2f}")
        print(f"  优惠：¥{discount_amount:.2f}")
    
    # 9. 测试购物车合并
    print("\n9. 购物车合并测试：")
    print("-" * 40)
    
    print("\n合并前：")
    print(f"  cart1: {cart1}")
    print(f"  cart2: {cart2}")
    
    merged_cart = ShoppingCart.merge_carts(cart1, cart2)
    print(f"\n合并后：{merged_cart}")
    print(merged_cart.get_cart_summary())
    
    # 10. 测试商品价格验证
    print("\n10. 商品价格验证测试：")
    print("-" * 40)
    
    test_prices = [99.99, "50.0", -10, "invalid", None]
    for price in test_prices:
        is_valid = Product.is_valid_price(price)
        print(f"  价格'{price}': {'有效' if is_valid else '无效'}")
    
    # 11. 测试异常处理
    print("\n11. 异常处理测试：")
    print("-" * 40)
    
    try:
        # 测试无效商品创建
        invalid_product = Product("", "商品", -100)
    except ValueError as e:
        print(f"捕获异常：{e}")
    
    try:
        # 测试无效数量
        cart1.add_item(products[0], -1)
    except ValueError as e:
        print(f"捕获异常：{e}")
    
    try:
        # 测试无效折扣率
        cart1.calculate_total_with_discount(1.5)
    except ValueError as e:
        print(f"捕获异常：{e}")
    
    try:
        # 测试访问不存在的商品
        non_existent = cart1["P999"]
    except KeyError as e:
        print(f"捕获异常：{e}")
    
    # 12. 测试购物车清空
    print("\n12. 购物车清空测试：")
    print("-" * 40)
    
    print(f"\n清空前：{cart2}")
    cart2.clear()
    print(f"清空后：{cart2}")
    print(f"是否为空：{cart2.is_empty()}")
    
    # 13. 最终状态
    print("\n13. 最终状态：")
    print("-" * 40)
    
    print(f"商品总数：{Product.get_total_products()}")
    print(f"购物车总数：{ShoppingCart.get_total_carts()}")
    
    print("\n所有购物车：")
    all_carts = [cart1, cart2, merged_cart]
    for cart in all_carts:
        print(f"  {cart}")
    
    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    test_shopping_cart()