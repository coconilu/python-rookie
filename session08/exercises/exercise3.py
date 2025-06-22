#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session08 练习题3：购物车系统

题目描述：
设计一个购物车系统，包含以下类：

1. Product类（商品类）：
   - 属性：商品ID、名称、价格、库存
   - 方法：获取商品信息、减少库存、增加库存

2. CartItem类（购物车项目类）：
   - 属性：商品对象、数量
   - 方法：计算小计、修改数量

3. ShoppingCart类（购物车类）：
   - 属性：购物车ID、商品列表
   - 方法：添加商品、移除商品、修改商品数量、计算总价、清空购物车

要求：
- 添加商品时检查库存是否足够
- 实现特殊方法：__str__、__len__、__contains__
- 购物车可以像列表一样遍历
- 计算总价时考虑商品数量

输入示例：
创建商品和购物车，进行添加、修改、删除操作

输出示例：
购物车内容、总价、操作结果等

提示：
- 使用组合关系（购物车包含商品项目）
- 在修改数量时要同步更新商品库存
- 可以使用列表存储购物车项目
"""

# 在这里编写你的代码

class Product:
    """商品类"""
    
    def __init__(self, product_id, name, price, stock):
        """初始化商品信息"""
        # 在这里实现
        pass
    
    # 添加其他方法


class CartItem:
    """购物车项目类"""
    
    def __init__(self, product, quantity):
        """初始化购物车项目"""
        # 在这里实现
        pass
    
    # 添加其他方法


class ShoppingCart:
    """购物车类"""
    
    def __init__(self, cart_id):
        """初始化购物车"""
        # 在这里实现
        pass
    
    # 添加其他方法


def test_shopping_cart():
    """测试购物车系统"""
    print("=== 购物车系统测试 ===")
    
    # 测试代码将在这里编写
    pass


if __name__ == "__main__":
    test_shopping_cart()