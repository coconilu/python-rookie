#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session07 示例4：JSON文件处理

本示例演示了Python中JSON文件的处理，包括：
- 使用json模块读写JSON文件
- 处理复杂的JSON数据结构
- JSON数据的验证和转换
- 处理JSON格式错误
- 与API数据交互的JSON处理

作者: Python教程团队
创建日期: 2024-12-22
"""

import json
import random
from pathlib import Path
from datetime import datetime, timedelta


def create_simple_json():
    """
    创建简单的JSON文件
    """
    print("=== 创建简单JSON文件 ===")
    
    # 简单的用户信息
    user_data = {
        "name": "张三",
        "age": 25,
        "email": "zhangsan@example.com",
        "is_active": True,
        "hobbies": ["读书", "游泳", "编程"],
        "address": {
            "city": "北京",
            "district": "朝阳区",
            "street": "建国路123号"
        },
        "created_at": datetime.now().isoformat()
    }
    
    # 写入JSON文件
    json_file = 'user_data.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(user_data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 创建用户数据JSON文件: {json_file}")
    print(f"✓ 用户姓名: {user_data['name']}")
    print(f"✓ 爱好数量: {len(user_data['hobbies'])}")
    
    return json_file


def read_json_basic(filename):
    """
    基本JSON文件读取
    """
    print(f"\n=== 基本JSON读取: {filename} ===")
    
    try:
        # 读取JSON文件
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("JSON数据内容:")
        print(f"姓名: {data['name']}")
        print(f"年龄: {data['age']}")
        print(f"邮箱: {data['email']}")
        print(f"状态: {'活跃' if data['is_active'] else '非活跃'}")
        print(f"爱好: {', '.join(data['hobbies'])}")
        print(f"地址: {data['address']['city']} {data['address']['district']} {data['address']['street']}")
        print(f"创建时间: {data['created_at']}")
        
        # 美化打印整个JSON
        print("\n完整JSON数据（美化格式）:")
        print(json.dumps(data, ensure_ascii=False, indent=2))
        
        return data
        
    except FileNotFoundError:
        print(f"❌ 文件 {filename} 不存在")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON格式错误: {e}")
        return None
    except Exception as e:
        print(f"❌ 读取JSON文件时发生错误: {e}")
        return None


def create_complex_json():
    """
    创建复杂的JSON数据结构
    """
    print("\n=== 创建复杂JSON数据结构 ===")
    
    # 模拟一个在线商店的数据
    store_data = {
        "store_info": {
            "name": "Python学习商店",
            "established": "2020-01-01",
            "owner": "李老师",
            "contact": {
                "phone": "400-123-4567",
                "email": "contact@pythonstore.com",
                "website": "https://pythonstore.com"
            },
            "location": {
                "country": "中国",
                "city": "北京",
                "coordinates": {
                    "latitude": 39.9042,
                    "longitude": 116.4074
                }
            }
        },
        "categories": [
            {
                "id": 1,
                "name": "编程书籍",
                "description": "各种编程语言的学习书籍"
            },
            {
                "id": 2,
                "name": "在线课程",
                "description": "视频教程和在线培训课程"
            },
            {
                "id": 3,
                "name": "开发工具",
                "description": "编程开发相关的软件和工具"
            }
        ],
        "products": [],
        "customers": [],
        "orders": [],
        "statistics": {
            "total_products": 0,
            "total_customers": 0,
            "total_orders": 0,
            "total_revenue": 0.0,
            "last_updated": datetime.now().isoformat()
        }
    }
    
    # 生成产品数据
    products = [
        {"name": "Python编程从入门到实践", "category_id": 1, "price": 89.0, "stock": 50},
        {"name": "JavaScript高级程序设计", "category_id": 1, "price": 99.0, "stock": 30},
        {"name": "Python Web开发课程", "category_id": 2, "price": 299.0, "stock": 100},
        {"name": "数据分析实战课程", "category_id": 2, "price": 399.0, "stock": 80},
        {"name": "PyCharm专业版", "category_id": 3, "price": 199.0, "stock": 200},
        {"name": "VS Code插件包", "category_id": 3, "price": 49.0, "stock": 150}
    ]
    
    for i, product in enumerate(products, 1):
        product_data = {
            "id": i,
            "name": product["name"],
            "category_id": product["category_id"],
            "price": product["price"],
            "stock": product["stock"],
            "description": f"{product['name']}的详细描述",
            "tags": ["编程", "学习", "Python"],
            "rating": round(random.uniform(4.0, 5.0), 1),
            "reviews_count": random.randint(10, 100),
            "created_at": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
            "is_available": True
        }
        store_data["products"].append(product_data)
    
    # 生成客户数据
    customer_names = ["王小明", "李小红", "张小强", "赵小美", "陈小华"]
    for i, name in enumerate(customer_names, 1):
        customer_data = {
            "id": i,
            "name": name,
            "email": f"customer{i}@example.com",
            "phone": f"138{random.randint(10000000, 99999999)}",
            "address": {
                "city": random.choice(["北京", "上海", "广州", "深圳"]),
                "district": f"区域{random.randint(1, 10)}",
                "detail": f"街道{random.randint(1, 100)}号"
            },
            "registration_date": (datetime.now() - timedelta(days=random.randint(1, 200))).isoformat(),
            "total_orders": 0,
            "total_spent": 0.0,
            "is_vip": False
        }
        store_data["customers"].append(customer_data)
    
    # 生成订单数据
    for i in range(1, 11):  # 10个订单
        customer = random.choice(store_data["customers"])
        products_in_order = random.sample(store_data["products"], random.randint(1, 3))
        
        order_items = []
        total_amount = 0
        
        for product in products_in_order:
            quantity = random.randint(1, 3)
            item_total = product["price"] * quantity
            total_amount += item_total
            
            order_items.append({
                "product_id": product["id"],
                "product_name": product["name"],
                "quantity": quantity,
                "unit_price": product["price"],
                "total_price": item_total
            })
        
        order_data = {
            "id": i,
            "customer_id": customer["id"],
            "customer_name": customer["name"],
            "order_date": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
            "items": order_items,
            "total_amount": total_amount,
            "status": random.choice(["pending", "processing", "shipped", "delivered"]),
            "payment_method": random.choice(["credit_card", "alipay", "wechat_pay"]),
            "shipping_address": customer["address"]
        }
        
        store_data["orders"].append(order_data)
        
        # 更新客户统计
        customer["total_orders"] += 1
        customer["total_spent"] += total_amount
        if customer["total_spent"] > 500:
            customer["is_vip"] = True
    
    # 更新统计信息
    store_data["statistics"]["total_products"] = len(store_data["products"])
    store_data["statistics"]["total_customers"] = len(store_data["customers"])
    store_data["statistics"]["total_orders"] = len(store_data["orders"])
    store_data["statistics"]["total_revenue"] = sum(order["total_amount"] for order in store_data["orders"])
    
    # 写入JSON文件
    complex_json_file = 'store_data.json'
    with open(complex_json_file, 'w', encoding='utf-8') as f:
        json.dump(store_data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 创建复杂JSON文件: {complex_json_file}")
    print(f"✓ 商店名称: {store_data['store_info']['name']}")
    print(f"✓ 产品数量: {len(store_data['products'])}")
    print(f"✓ 客户数量: {len(store_data['customers'])}")
    print(f"✓ 订单数量: {len(store_data['orders'])}")
    print(f"✓ 总收入: ¥{store_data['statistics']['total_revenue']:.2f}")
    
    return complex_json_file


def analyze_store_data(filename):
    """
    分析商店数据
    """
    print(f"\n=== 商店数据分析: {filename} ===")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            store_data = json.load(f)
        
        # 基本信息
        print(f"商店名称: {store_data['store_info']['name']}")
        print(f"成立时间: {store_data['store_info']['established']}")
        print(f"所在城市: {store_data['store_info']['location']['city']}")
        
        # 产品分析
        products = store_data['products']
        print(f"\n产品分析:")
        print(f"总产品数: {len(products)}")
        
        # 按类别统计产品
        categories = {cat['id']: cat['name'] for cat in store_data['categories']}
        category_stats = {}
        for product in products:
            cat_id = product['category_id']
            cat_name = categories[cat_id]
            if cat_name not in category_stats:
                category_stats[cat_name] = {'count': 0, 'total_value': 0}
            category_stats[cat_name]['count'] += 1
            category_stats[cat_name]['total_value'] += product['price'] * product['stock']
        
        for cat_name, stats in category_stats.items():
            print(f"  {cat_name}: {stats['count']}个产品, 库存价值¥{stats['total_value']:.2f}")
        
        # 价格分析
        prices = [p['price'] for p in products]
        print(f"\n价格分析:")
        print(f"  最高价格: ¥{max(prices):.2f}")
        print(f"  最低价格: ¥{min(prices):.2f}")
        print(f"  平均价格: ¥{sum(prices)/len(prices):.2f}")
        
        # 评分分析
        ratings = [p['rating'] for p in products]
        avg_rating = sum(ratings) / len(ratings)
        print(f"  平均评分: {avg_rating:.1f}/5.0")
        
        # 客户分析
        customers = store_data['customers']
        print(f"\n客户分析:")
        print(f"总客户数: {len(customers)}")
        
        vip_customers = [c for c in customers if c['is_vip']]
        print(f"VIP客户数: {len(vip_customers)}")
        
        # 客户消费分析
        total_spent = [c['total_spent'] for c in customers]
        if total_spent:
            print(f"客户平均消费: ¥{sum(total_spent)/len(total_spent):.2f}")
            print(f"最高消费客户: ¥{max(total_spent):.2f}")
        
        # 订单分析
        orders = store_data['orders']
        print(f"\n订单分析:")
        print(f"总订单数: {len(orders)}")
        
        # 订单状态统计
        status_stats = {}
        for order in orders:
            status = order['status']
            status_stats[status] = status_stats.get(status, 0) + 1
        
        print("订单状态分布:")
        for status, count in status_stats.items():
            print(f"  {status}: {count}个订单")
        
        # 支付方式统计
        payment_stats = {}
        for order in orders:
            payment = order['payment_method']
            payment_stats[payment] = payment_stats.get(payment, 0) + 1
        
        print("支付方式分布:")
        for payment, count in payment_stats.items():
            print(f"  {payment}: {count}个订单")
        
        # 销售额分析
        order_amounts = [o['total_amount'] for o in orders]
        if order_amounts:
            print(f"\n销售额分析:")
            print(f"总销售额: ¥{sum(order_amounts):.2f}")
            print(f"平均订单金额: ¥{sum(order_amounts)/len(order_amounts):.2f}")
            print(f"最大订单金额: ¥{max(order_amounts):.2f}")
            print(f"最小订单金额: ¥{min(order_amounts):.2f}")
        
        return store_data
        
    except Exception as e:
        print(f"❌ 分析商店数据时发生错误: {e}")
        return None


def json_data_manipulation(store_data):
    """
    JSON数据操作和转换
    """
    print("\n=== JSON数据操作和转换 ===")
    
    if not store_data:
        print("❌ 没有商店数据")
        return
    
    # 1. 添加新产品
    new_product = {
        "id": len(store_data['products']) + 1,
        "name": "机器学习实战课程",
        "category_id": 2,
        "price": 499.0,
        "stock": 60,
        "description": "从零开始学习机器学习",
        "tags": ["机器学习", "AI", "Python"],
        "rating": 4.8,
        "reviews_count": 25,
        "created_at": datetime.now().isoformat(),
        "is_available": True
    }
    
    store_data['products'].append(new_product)
    print(f"✓ 添加新产品: {new_product['name']}")
    
    # 2. 更新产品价格（打折活动）
    discount_rate = 0.9  # 9折
    discounted_products = []
    
    for product in store_data['products']:
        if product['category_id'] == 1:  # 书籍类别打折
            original_price = product['price']
            product['price'] = round(original_price * discount_rate, 2)
            product['original_price'] = original_price
            product['discount'] = f"{int((1-discount_rate)*100)}%折扣"
            discounted_products.append(product['name'])
    
    print(f"✓ 书籍类产品打折，共{len(discounted_products)}个产品")
    
    # 3. 筛选VIP客户
    vip_customers = [c for c in store_data['customers'] if c['is_vip']]
    vip_summary = {
        "total_vip_customers": len(vip_customers),
        "vip_customers": [
            {
                "name": c['name'],
                "total_spent": c['total_spent'],
                "total_orders": c['total_orders']
            } for c in vip_customers
        ],
        "generated_at": datetime.now().isoformat()
    }
    
    # 保存VIP客户摘要
    vip_file = 'vip_customers.json'
    with open(vip_file, 'w', encoding='utf-8') as f:
        json.dump(vip_summary, f, ensure_ascii=False, indent=2)
    
    print(f"✓ VIP客户摘要已保存到: {vip_file}")
    
    # 4. 生成销售报告
    sales_report = {
        "report_date": datetime.now().isoformat(),
        "period": "最近30天",
        "summary": {
            "total_orders": len(store_data['orders']),
            "total_revenue": sum(o['total_amount'] for o in store_data['orders']),
            "average_order_value": sum(o['total_amount'] for o in store_data['orders']) / len(store_data['orders']) if store_data['orders'] else 0,
            "total_customers": len(store_data['customers']),
            "vip_customers": len(vip_customers)
        },
        "top_products": [],
        "customer_insights": {
            "new_customers": 0,
            "repeat_customers": 0
        }
    }
    
    # 计算产品销量
    product_sales = {}
    for order in store_data['orders']:
        for item in order['items']:
            product_id = item['product_id']
            if product_id not in product_sales:
                product_sales[product_id] = {
                    'name': item['product_name'],
                    'quantity': 0,
                    'revenue': 0
                }
            product_sales[product_id]['quantity'] += item['quantity']
            product_sales[product_id]['revenue'] += item['total_price']
    
    # 排序并获取前5名产品
    top_products = sorted(product_sales.items(), key=lambda x: x[1]['revenue'], reverse=True)[:5]
    for product_id, stats in top_products:
        sales_report['top_products'].append({
            'product_id': product_id,
            'name': stats['name'],
            'quantity_sold': stats['quantity'],
            'revenue': stats['revenue']
        })
    
    # 保存销售报告
    report_file = 'sales_report.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(sales_report, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 销售报告已保存到: {report_file}")
    
    # 5. 更新主数据文件
    updated_store_file = 'store_data_updated.json'
    with open(updated_store_file, 'w', encoding='utf-8') as f:
        json.dump(store_data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 更新后的商店数据已保存到: {updated_store_file}")
    
    return [vip_file, report_file, updated_store_file]


def handle_json_errors():
    """
    处理JSON格式错误
    """
    print("\n=== JSON错误处理演示 ===")
    
    # 创建包含错误的JSON文件
    invalid_json_content = '''{
    "name": "测试用户",
    "age": 25,
    "hobbies": ["读书", "游泳",],  // 多余的逗号
    "address": {
        "city": "北京",
        "district": "朝阳区"  // 缺少逗号
        "street": "建国路123号"
    },
    "is_active": true,
    "score": 95.5,
    // 这是注释，JSON不支持注释
}'''
    
    invalid_file = 'invalid.json'
    with open(invalid_file, 'w', encoding='utf-8') as f:
        f.write(invalid_json_content)
    
    print(f"✓ 创建包含错误的JSON文件: {invalid_file}")
    
    # 尝试读取错误的JSON文件
    print("\n尝试读取错误的JSON文件:")
    try:
        with open(invalid_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("✓ JSON读取成功")
    except json.JSONDecodeError as e:
        print(f"❌ JSON格式错误: {e}")
        print(f"   错误位置: 行{e.lineno}, 列{e.colno}")
        print(f"   错误信息: {e.msg}")
    
    # 演示安全的JSON读取函数
    def safe_load_json(filename):
        """
        安全地加载JSON文件
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ 文件 {filename} 不存在")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ JSON格式错误: {e}")
            return None
        except Exception as e:
            print(f"❌ 读取文件时发生未知错误: {e}")
            return None
    
    print("\n使用安全的JSON读取函数:")
    result = safe_load_json(invalid_file)
    if result is None:
        print("JSON读取失败，返回默认值")
    
    # 创建修正后的JSON文件
    corrected_json = {
        "name": "测试用户",
        "age": 25,
        "hobbies": ["读书", "游泳"],
        "address": {
            "city": "北京",
            "district": "朝阳区",
            "street": "建国路123号"
        },
        "is_active": True,
        "score": 95.5
    }
    
    corrected_file = 'corrected.json'
    with open(corrected_file, 'w', encoding='utf-8') as f:
        json.dump(corrected_json, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 创建修正后的JSON文件: {corrected_file}")
    
    # 验证修正后的文件
    corrected_data = safe_load_json(corrected_file)
    if corrected_data:
        print("✓ 修正后的JSON文件读取成功")
        print(f"  用户姓名: {corrected_data['name']}")
        print(f"  用户年龄: {corrected_data['age']}")
    
    return [invalid_file, corrected_file]


def json_string_operations():
    """
    JSON字符串操作
    """
    print("\n=== JSON字符串操作 ===")
    
    # Python对象转JSON字符串
    python_data = {
        "products": [
            {"id": 1, "name": "笔记本", "price": 5999.99},
            {"id": 2, "name": "鼠标", "price": 199.99}
        ],
        "timestamp": datetime.now().isoformat(),
        "success": True
    }
    
    # 转换为JSON字符串
    json_string = json.dumps(python_data, ensure_ascii=False, indent=2)
    print("Python对象转JSON字符串:")
    print(json_string)
    
    # JSON字符串转Python对象
    print("\nJSON字符串转Python对象:")
    parsed_data = json.loads(json_string)
    print(f"产品数量: {len(parsed_data['products'])}")
    print(f"第一个产品: {parsed_data['products'][0]['name']}")
    print(f"时间戳: {parsed_data['timestamp']}")
    
    # 处理特殊字符
    special_data = {
        "message": "这是一条包含特殊字符的消息：\n换行\t制表符\"引号\\",
        "unicode": "Unicode字符: 😀 🐍 ❤️",
        "chinese": "中文测试：你好世界"
    }
    
    print("\n处理特殊字符:")
    special_json = json.dumps(special_data, ensure_ascii=False, indent=2)
    print(special_json)
    
    # 紧凑格式vs美化格式
    compact_json = json.dumps(python_data, ensure_ascii=False, separators=(',', ':'))
    pretty_json = json.dumps(python_data, ensure_ascii=False, indent=4)
    
    print(f"\n紧凑格式长度: {len(compact_json)} 字符")
    print(f"美化格式长度: {len(pretty_json)} 字符")
    print(f"紧凑格式: {compact_json[:100]}...")


def cleanup_json_files():
    """
    清理JSON示例文件
    """
    print("\n=== 清理JSON文件 ===")
    
    json_files = [
        'user_data.json',
        'store_data.json',
        'vip_customers.json',
        'sales_report.json',
        'store_data_updated.json',
        'invalid.json',
        'corrected.json'
    ]
    
    for filename in json_files:
        file_path = Path(filename)
        if file_path.exists():
            file_path.unlink()
            print(f"✓ 删除文件: {filename}")
        else:
            print(f"- 文件不存在: {filename}")


def main():
    """
    主函数
    """
    print("Session07 示例4：JSON文件处理")
    print("=" * 50)
    
    try:
        # 1. 创建和读取简单JSON文件
        simple_json_file = create_simple_json()
        user_data = read_json_basic(simple_json_file)
        
        # 2. 创建复杂JSON数据结构
        complex_json_file = create_complex_json()
        
        # 3. 分析商店数据
        store_data = analyze_store_data(complex_json_file)
        
        # 4. JSON数据操作和转换
        if store_data:
            generated_files = json_data_manipulation(store_data)
        
        # 5. 处理JSON错误
        error_files = handle_json_errors()
        
        # 6. JSON字符串操作
        json_string_operations()
        
        print("\n" + "=" * 50)
        print("✅ 示例4演示完成！")
        print("\n💡 重要提示：")
        print("- JSON是轻量级的数据交换格式")
        print("- 使用ensure_ascii=False支持中文字符")
        print("- 使用indent参数美化JSON格式")
        print("- 注意处理JSON格式错误和异常")
        print("- JSON不支持注释和多余的逗号")
        
        # 询问是否清理文件
        response = input("\n是否清理JSON示例文件？(y/n): ").lower().strip()
        if response == 'y':
            cleanup_json_files()
        else:
            print("JSON示例文件已保留，你可以手动查看和分析它们。")
            
    except Exception as e:
        print(f"\n❌ 示例运行过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()