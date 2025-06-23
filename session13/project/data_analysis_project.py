#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据分析综合项目：电商平台数据分析

项目描述：
本项目模拟一个电商平台的数据分析场景，包含用户数据、订单数据、产品数据等。
通过综合运用Pandas的各种功能，完成从数据清洗到业务洞察的完整分析流程。

项目目标：
1. 掌握完整的数据分析流程
2. 学会处理真实业务场景中的复杂数据
3. 提供有价值的业务洞察和建议
4. 创建专业的数据分析报告

作者: Python教程团队
创建日期: 2024-01-01
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
import os

# 设置
warnings.filterwarnings('ignore')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")

# 项目配置
class Config:
    """项目配置类"""
    
    # 数据参数
    N_USERS = 10000
    N_PRODUCTS = 500
    N_ORDERS = 50000
    N_REVIEWS = 30000
    
    # 时间范围
    START_DATE = '2023-01-01'
    END_DATE = '2024-12-31'
    
    # 随机种子
    RANDOM_SEED = 42
    
    # 文件路径
    DATA_DIR = 'data'
    OUTPUT_DIR = 'output'
    PLOTS_DIR = 'plots'


class DataGenerator:
    """数据生成器类"""
    
    def __init__(self, config):
        self.config = config
        np.random.seed(config.RANDOM_SEED)
        
        # 创建输出目录
        for directory in [config.DATA_DIR, config.OUTPUT_DIR, config.PLOTS_DIR]:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    def generate_users(self):
        """生成用户数据"""
        print("生成用户数据...")
        
        users = pd.DataFrame({
            '用户ID': range(1, self.config.N_USERS + 1),
            '用户名': [f'user_{i:05d}' for i in range(1, self.config.N_USERS + 1)],
            '年龄': np.random.normal(35, 12, self.config.N_USERS).astype(int).clip(18, 80),
            '性别': np.random.choice(['男', '女'], self.config.N_USERS),
            '城市': np.random.choice([
                '北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '西安', 
                '南京', '天津', '重庆', '苏州', '长沙', '郑州', '青岛'
            ], self.config.N_USERS),
            '注册日期': pd.date_range(
                start='2020-01-01', 
                end='2024-06-30', 
                periods=self.config.N_USERS
            ),
            '会员等级': np.random.choice(
                ['普通', '银牌', '金牌', '钻石'], 
                self.config.N_USERS, 
                p=[0.6, 0.25, 0.12, 0.03]
            ),
            '职业': np.random.choice([
                'IT', '金融', '教育', '医疗', '销售', '制造', '服务', '学生', '其他'
            ], self.config.N_USERS),
            '月收入': np.random.lognormal(9, 0.8, self.config.N_USERS).astype(int)
        })
        
        # 根据会员等级调整收入
        income_multiplier = users['会员等级'].map({
            '普通': 1.0, '银牌': 1.3, '金牌': 1.8, '钻石': 2.5
        })
        users['月收入'] = (users['月收入'] * income_multiplier).astype(int)
        
        return users
    
    def generate_products(self):
        """生成产品数据"""
        print("生成产品数据...")
        
        categories = {
            '电子产品': ['手机', '电脑', '平板', '耳机', '音响', '相机'],
            '服装': ['上衣', '裤子', '裙子', '鞋子', '包包', '配饰'],
            '家居': ['家具', '厨具', '装饰', '床品', '收纳', '清洁'],
            '食品': ['零食', '饮料', '生鲜', '调料', '保健品', '茶酒'],
            '图书': ['小说', '技术', '教育', '艺术', '历史', '科学'],
            '运动': ['健身', '户外', '球类', '游泳', '跑步', '瑜伽']
        }
        
        products = []
        product_id = 1
        
        for category, subcategories in categories.items():
            n_products_in_category = self.config.N_PRODUCTS // len(categories)
            
            for _ in range(n_products_in_category):
                subcategory = np.random.choice(subcategories)
                
                # 根据类别设置价格范围
                if category == '电子产品':
                    base_price = np.random.lognormal(7, 1)
                elif category == '服装':
                    base_price = np.random.lognormal(5, 0.8)
                elif category == '家居':
                    base_price = np.random.lognormal(4.5, 1.2)
                elif category == '食品':
                    base_price = np.random.lognormal(3, 0.6)
                elif category == '图书':
                    base_price = np.random.lognormal(3.5, 0.5)
                else:  # 运动
                    base_price = np.random.lognormal(5.5, 1)
                
                products.append({
                    '产品ID': product_id,
                    '产品名称': f'{subcategory}_{product_id:03d}',
                    '类别': category,
                    '子类别': subcategory,
                    '价格': round(base_price, 2),
                    '成本': round(base_price * np.random.uniform(0.4, 0.7), 2),
                    '库存': np.random.randint(0, 1000),
                    '品牌': f'品牌{np.random.randint(1, 51)}',
                    '上架日期': pd.Timestamp('2020-01-01') + 
                               pd.Timedelta(days=np.random.randint(0, 1400)),
                    '评分': np.random.uniform(3.0, 5.0),
                    '评价数': np.random.randint(0, 1000)
                })
                
                product_id += 1
        
        return pd.DataFrame(products)
    
    def generate_orders(self, users, products):
        """生成订单数据"""
        print("生成订单数据...")
        
        orders = []
        order_details = []
        
        # 为每个用户生成不同数量的订单
        user_order_counts = np.random.poisson(5, len(users))
        
        order_id = 1
        detail_id = 1
        
        for user_idx, user_row in users.iterrows():
            user_id = user_row['用户ID']
            n_orders = user_order_counts[user_idx]
            
            for _ in range(n_orders):
                # 订单基本信息
                order_date = pd.Timestamp(self.config.START_DATE) + \
                           pd.Timedelta(days=np.random.randint(0, 730))
                
                # 根据用户会员等级影响购买行为
                if user_row['会员等级'] == '钻石':
                    n_items = np.random.poisson(3) + 1
                    discount_rate = 0.15
                elif user_row['会员等级'] == '金牌':
                    n_items = np.random.poisson(2) + 1
                    discount_rate = 0.10
                elif user_row['会员等级'] == '银牌':
                    n_items = np.random.poisson(1.5) + 1
                    discount_rate = 0.05
                else:
                    n_items = np.random.poisson(1) + 1
                    discount_rate = 0.0
                
                # 选择产品
                selected_products = products.sample(n=min(n_items, len(products)))
                
                total_amount = 0
                order_items = []
                
                for _, product in selected_products.iterrows():
                    quantity = np.random.randint(1, 4)
                    unit_price = product['价格']
                    item_total = quantity * unit_price
                    total_amount += item_total
                    
                    order_items.append({
                        '详情ID': detail_id,
                        '订单ID': order_id,
                        '产品ID': product['产品ID'],
                        '数量': quantity,
                        '单价': unit_price,
                        '小计': item_total
                    })
                    
                    detail_id += 1
                
                # 应用折扣
                discounted_amount = total_amount * (1 - discount_rate)
                
                # 订单状态
                status_weights = [0.85, 0.10, 0.03, 0.02]
                order_status = np.random.choice(
                    ['已完成', '已取消', '退款', '争议'], 
                    p=status_weights
                )
                
                # 支付方式
                payment_method = np.random.choice(
                    ['支付宝', '微信支付', '信用卡', '银行卡'], 
                    p=[0.4, 0.35, 0.15, 0.1]
                )
                
                orders.append({
                    '订单ID': order_id,
                    '用户ID': user_id,
                    '订单日期': order_date,
                    '订单金额': round(total_amount, 2),
                    '实付金额': round(discounted_amount, 2),
                    '折扣金额': round(total_amount - discounted_amount, 2),
                    '订单状态': order_status,
                    '支付方式': payment_method,
                    '配送方式': np.random.choice(['标准配送', '快速配送', '次日达'], 
                                              p=[0.6, 0.3, 0.1]),
                    '配送地址': user_row['城市']
                })
                
                order_details.extend(order_items)
                order_id += 1
        
        return pd.DataFrame(orders), pd.DataFrame(order_details)
    
    def generate_reviews(self, orders, products):
        """生成评价数据"""
        print("生成评价数据...")
        
        # 只对已完成的订单生成评价
        completed_orders = orders[orders['订单状态'] == '已完成']
        
        # 随机选择一部分订单进行评价
        review_orders = completed_orders.sample(
            n=min(self.config.N_REVIEWS, len(completed_orders))
        )
        
        reviews = []
        
        for _, order in review_orders.iterrows():
            # 评分倾向于正面
            rating = np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.05, 0.15, 0.35, 0.4])
            
            # 根据评分生成评价内容
            if rating >= 4:
                sentiment = '正面'
                content_templates = [
                    '商品质量很好，很满意！',
                    '物流很快，包装完好。',
                    '性价比很高，推荐购买。',
                    '卖家服务态度很好。',
                    '商品和描述一致，好评！'
                ]
            elif rating == 3:
                sentiment = '中性'
                content_templates = [
                    '商品一般，凑合能用。',
                    '价格合理，质量还行。',
                    '物流速度一般。',
                    '商品基本符合预期。'
                ]
            else:
                sentiment = '负面'
                content_templates = [
                    '商品质量不好，不推荐。',
                    '物流太慢了。',
                    '商品和描述不符。',
                    '客服态度不好。',
                    '性价比不高。'
                ]
            
            reviews.append({
                '评价ID': len(reviews) + 1,
                '订单ID': order['订单ID'],
                '用户ID': order['用户ID'],
                '评分': rating,
                '评价内容': np.random.choice(content_templates),
                '情感倾向': sentiment,
                '评价日期': order['订单日期'] + pd.Timedelta(days=np.random.randint(1, 30)),
                '是否匿名': np.random.choice([True, False], p=[0.3, 0.7])
            })
        
        return pd.DataFrame(reviews)
    
    def generate_all_data(self):
        """生成所有数据"""
        print("开始生成电商平台数据...")
        
        # 生成各类数据
        users = self.generate_users()
        products = self.generate_products()
        orders, order_details = self.generate_orders(users, products)
        reviews = self.generate_reviews(orders, products)
        
        # 保存数据
        users.to_csv(f'{self.config.DATA_DIR}/users.csv', index=False, encoding='utf-8')
        products.to_csv(f'{self.config.DATA_DIR}/products.csv', index=False, encoding='utf-8')
        orders.to_csv(f'{self.config.DATA_DIR}/orders.csv', index=False, encoding='utf-8')
        order_details.to_csv(f'{self.config.DATA_DIR}/order_details.csv', index=False, encoding='utf-8')
        reviews.to_csv(f'{self.config.DATA_DIR}/reviews.csv', index=False, encoding='utf-8')
        
        print(f"数据生成完成！")
        print(f"用户数据: {len(users)} 条")
        print(f"产品数据: {len(products)} 条")
        print(f"订单数据: {len(orders)} 条")
        print(f"订单详情: {len(order_details)} 条")
        print(f"评价数据: {len(reviews)} 条")
        
        return users, products, orders, order_details, reviews


class DataAnalyzer:
    """数据分析器类"""
    
    def __init__(self, config):
        self.config = config
        self.users = None
        self.products = None
        self.orders = None
        self.order_details = None
        self.reviews = None
        self.merged_data = None
    
    def load_data(self):
        """加载数据"""
        print("加载数据...")
        
        try:
            self.users = pd.read_csv(f'{self.config.DATA_DIR}/users.csv', encoding='utf-8')
            self.products = pd.read_csv(f'{self.config.DATA_DIR}/products.csv', encoding='utf-8')
            self.orders = pd.read_csv(f'{self.config.DATA_DIR}/orders.csv', encoding='utf-8')
            self.order_details = pd.read_csv(f'{self.config.DATA_DIR}/order_details.csv', encoding='utf-8')
            self.reviews = pd.read_csv(f'{self.config.DATA_DIR}/reviews.csv', encoding='utf-8')
            
            # 转换日期列
            self.users['注册日期'] = pd.to_datetime(self.users['注册日期'])
            self.products['上架日期'] = pd.to_datetime(self.products['上架日期'])
            self.orders['订单日期'] = pd.to_datetime(self.orders['订单日期'])
            self.reviews['评价日期'] = pd.to_datetime(self.reviews['评价日期'])
            
            print("数据加载完成！")
            
        except FileNotFoundError:
            print("数据文件不存在，请先生成数据！")
            return False
        
        return True
    
    def data_quality_check(self):
        """数据质量检查"""
        print("\n=== 数据质量检查 ===")
        
        datasets = {
            '用户数据': self.users,
            '产品数据': self.products,
            '订单数据': self.orders,
            '订单详情': self.order_details,
            '评价数据': self.reviews
        }
        
        quality_report = []
        
        for name, df in datasets.items():
            print(f"\n{name}质量检查：")
            
            # 基本信息
            print(f"数据形状: {df.shape}")
            print(f"内存使用: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
            
            # 缺失值检查
            missing_values = df.isnull().sum()
            missing_pct = (missing_values / len(df) * 100).round(2)
            
            if missing_values.sum() > 0:
                print("缺失值情况：")
                for col, count in missing_values[missing_values > 0].items():
                    print(f"  {col}: {count} ({missing_pct[col]}%)")
            else:
                print("无缺失值")
            
            # 重复值检查
            duplicates = df.duplicated().sum()
            print(f"重复行数: {duplicates}")
            
            # 数据类型
            print("数据类型：")
            for col, dtype in df.dtypes.items():
                print(f"  {col}: {dtype}")
            
            quality_report.append({
                '数据集': name,
                '行数': df.shape[0],
                '列数': df.shape[1],
                '缺失值': missing_values.sum(),
                '重复行': duplicates,
                '内存(MB)': round(df.memory_usage(deep=True).sum() / 1024**2, 2)
            })
        
        # 生成质量报告
        quality_df = pd.DataFrame(quality_report)
        print("\n数据质量总结：")
        print(quality_df)
        
        return quality_df
    
    def merge_data(self):
        """合并数据"""
        print("\n=== 数据合并 ===")
        
        # 合并订单和订单详情
        order_with_details = self.orders.merge(
            self.order_details, on='订单ID', how='left'
        )
        
        # 合并产品信息
        order_with_products = order_with_details.merge(
            self.products, on='产品ID', how='left'
        )
        
        # 合并用户信息
        self.merged_data = order_with_products.merge(
            self.users, on='用户ID', how='left'
        )
        
        print(f"合并后数据形状: {self.merged_data.shape}")
        
        return self.merged_data
    
    def user_analysis(self):
        """用户分析"""
        print("\n=== 用户分析 ===")
        
        # 用户基本统计
        print("\n1. 用户基本统计：")
        print(f"总用户数: {len(self.users):,}")
        print(f"平均年龄: {self.users['年龄'].mean():.1f}岁")
        print(f"性别分布:")
        print(self.users['性别'].value_counts())
        
        # 地域分布
        print("\n2. 地域分布TOP10：")
        city_dist = self.users['城市'].value_counts().head(10)
        print(city_dist)
        
        # 会员等级分布
        print("\n3. 会员等级分布：")
        member_dist = self.users['会员等级'].value_counts()
        print(member_dist)
        
        # 注册趋势
        print("\n4. 注册趋势分析：")
        self.users['注册年月'] = self.users['注册日期'].dt.to_period('M')
        registration_trend = self.users.groupby('注册年月').size()
        print(f"月均注册用户: {registration_trend.mean():.0f}")
        
        # 可视化
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('用户分析', fontsize=16)
        
        # 年龄分布
        self.users['年龄'].hist(bins=20, ax=axes[0, 0], alpha=0.7)
        axes[0, 0].set_title('年龄分布')
        axes[0, 0].set_xlabel('年龄')
        axes[0, 0].set_ylabel('人数')
        
        # 城市分布
        city_dist.head(10).plot(kind='bar', ax=axes[0, 1])
        axes[0, 1].set_title('城市分布TOP10')
        axes[0, 1].set_xlabel('城市')
        axes[0, 1].set_ylabel('用户数')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 会员等级分布
        member_dist.plot(kind='pie', ax=axes[1, 0], autopct='%1.1f%%')
        axes[1, 0].set_title('会员等级分布')
        
        # 注册趋势
        registration_trend.plot(ax=axes[1, 1])
        axes[1, 1].set_title('注册趋势')
        axes[1, 1].set_xlabel('时间')
        axes[1, 1].set_ylabel('注册用户数')
        
        plt.tight_layout()
        plt.savefig(f'{self.config.PLOTS_DIR}/user_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return {
            'city_distribution': city_dist,
            'member_distribution': member_dist,
            'registration_trend': registration_trend
        }
    
    def product_analysis(self):
        """产品分析"""
        print("\n=== 产品分析 ===")
        
        # 产品基本统计
        print("\n1. 产品基本统计：")
        print(f"总产品数: {len(self.products):,}")
        print(f"平均价格: ¥{self.products['价格'].mean():.2f}")
        print(f"价格范围: ¥{self.products['价格'].min():.2f} - ¥{self.products['价格'].max():.2f}")
        
        # 类别分布
        print("\n2. 产品类别分布：")
        category_dist = self.products['类别'].value_counts()
        print(category_dist)
        
        # 价格分析
        print("\n3. 各类别价格分析：")
        price_by_category = self.products.groupby('类别')['价格'].agg(['mean', 'median', 'std']).round(2)
        print(price_by_category)
        
        # 库存分析
        print("\n4. 库存分析：")
        print(f"总库存: {self.products['库存'].sum():,}")
        print(f"平均库存: {self.products['库存'].mean():.0f}")
        print(f"缺货产品数: {(self.products['库存'] == 0).sum()}")
        
        # 可视化
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('产品分析', fontsize=16)
        
        # 价格分布
        self.products['价格'].hist(bins=30, ax=axes[0, 0], alpha=0.7)
        axes[0, 0].set_title('价格分布')
        axes[0, 0].set_xlabel('价格')
        axes[0, 0].set_ylabel('产品数')
        
        # 类别分布
        category_dist.plot(kind='bar', ax=axes[0, 1])
        axes[0, 1].set_title('产品类别分布')
        axes[0, 1].set_xlabel('类别')
        axes[0, 1].set_ylabel('产品数')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 各类别平均价格
        price_by_category['mean'].plot(kind='bar', ax=axes[1, 0])
        axes[1, 0].set_title('各类别平均价格')
        axes[1, 0].set_xlabel('类别')
        axes[1, 0].set_ylabel('平均价格')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # 库存分布
        self.products['库存'].hist(bins=30, ax=axes[1, 1], alpha=0.7)
        axes[1, 1].set_title('库存分布')
        axes[1, 1].set_xlabel('库存数量')
        axes[1, 1].set_ylabel('产品数')
        
        plt.tight_layout()
        plt.savefig(f'{self.config.PLOTS_DIR}/product_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return {
            'category_distribution': category_dist,
            'price_by_category': price_by_category
        }
    
    def sales_analysis(self):
        """销售分析"""
        print("\n=== 销售分析 ===")
        
        # 销售基本统计
        print("\n1. 销售基本统计：")
        total_orders = len(self.orders)
        total_revenue = self.orders['实付金额'].sum()
        avg_order_value = self.orders['实付金额'].mean()
        
        print(f"总订单数: {total_orders:,}")
        print(f"总销售额: ¥{total_revenue:,.2f}")
        print(f"平均订单金额: ¥{avg_order_value:.2f}")
        
        # 订单状态分析
        print("\n2. 订单状态分析：")
        status_dist = self.orders['订单状态'].value_counts()
        print(status_dist)
        
        # 时间趋势分析
        print("\n3. 销售趋势分析：")
        self.orders['订单年月'] = self.orders['订单日期'].dt.to_period('M')
        monthly_sales = self.orders.groupby('订单年月').agg({
            '订单ID': 'count',
            '实付金额': 'sum'
        }).rename(columns={'订单ID': '订单数', '实付金额': '销售额'})
        
        print(f"月均订单数: {monthly_sales['订单数'].mean():.0f}")
        print(f"月均销售额: ¥{monthly_sales['销售额'].mean():,.2f}")
        
        # 支付方式分析
        print("\n4. 支付方式分析：")
        payment_analysis = self.orders.groupby('支付方式').agg({
            '订单ID': 'count',
            '实付金额': ['sum', 'mean']
        }).round(2)
        print(payment_analysis)
        
        # 可视化
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('销售分析', fontsize=16)
        
        # 订单金额分布
        self.orders['实付金额'].hist(bins=30, ax=axes[0, 0], alpha=0.7)
        axes[0, 0].set_title('订单金额分布')
        axes[0, 0].set_xlabel('订单金额')
        axes[0, 0].set_ylabel('订单数')
        
        # 订单状态分布
        status_dist.plot(kind='pie', ax=axes[0, 1], autopct='%1.1f%%')
        axes[0, 1].set_title('订单状态分布')
        
        # 月度销售趋势
        monthly_sales['销售额'].plot(ax=axes[1, 0])
        axes[1, 0].set_title('月度销售趋势')
        axes[1, 0].set_xlabel('时间')
        axes[1, 0].set_ylabel('销售额')
        
        # 支付方式分布
        payment_dist = self.orders['支付方式'].value_counts()
        payment_dist.plot(kind='bar', ax=axes[1, 1])
        axes[1, 1].set_title('支付方式分布')
        axes[1, 1].set_xlabel('支付方式')
        axes[1, 1].set_ylabel('订单数')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(f'{self.config.PLOTS_DIR}/sales_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return {
            'monthly_sales': monthly_sales,
            'status_distribution': status_dist,
            'payment_analysis': payment_analysis
        }
    
    def customer_segmentation(self):
        """客户细分分析"""
        print("\n=== 客户细分分析 ===")
        
        # 计算客户价值指标
        customer_metrics = self.orders.groupby('用户ID').agg({
            '订单日期': ['min', 'max', 'count'],
            '实付金额': ['sum', 'mean']
        })
        
        # 扁平化列名
        customer_metrics.columns = ['首次购买', '最近购买', '购买频次', '总消费', '平均消费']
        
        # 计算RFM指标
        current_date = self.orders['订单日期'].max()
        customer_metrics['最近购买天数'] = (current_date - customer_metrics['最近购买']).dt.days
        
        # 合并用户信息
        customer_analysis = customer_metrics.merge(
            self.users[['用户ID', '会员等级', '城市', '年龄']], 
            on='用户ID', 
            how='left'
        )
        
        # 客户分层
        def classify_customer(row):
            if row['总消费'] >= customer_metrics['总消费'].quantile(0.8) and row['购买频次'] >= 3:
                return '高价值客户'
            elif row['总消费'] >= customer_metrics['总消费'].quantile(0.6):
                return '中价值客户'
            elif row['购买频次'] >= 2:
                return '活跃客户'
            elif row['最近购买天数'] <= 90:
                return '新客户'
            else:
                return '低价值客户'
        
        customer_analysis['客户分层'] = customer_analysis.apply(classify_customer, axis=1)
        
        # 分层统计
        print("\n客户分层结果：")
        segment_stats = customer_analysis.groupby('客户分层').agg({
            '用户ID': 'count',
            '总消费': ['mean', 'sum'],
            '购买频次': 'mean',
            '最近购买天数': 'mean'
        }).round(2)
        
        print(segment_stats)
        
        # 可视化
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('客户细分分析', fontsize=16)
        
        # 客户分层分布
        segment_dist = customer_analysis['客户分层'].value_counts()
        segment_dist.plot(kind='pie', ax=axes[0, 0], autopct='%1.1f%%')
        axes[0, 0].set_title('客户分层分布')
        
        # RFM散点图
        scatter = axes[0, 1].scatter(
            customer_analysis['购买频次'], 
            customer_analysis['总消费'],
            c=customer_analysis['最近购买天数'], 
            cmap='viridis', 
            alpha=0.6
        )
        axes[0, 1].set_xlabel('购买频次')
        axes[0, 1].set_ylabel('总消费')
        axes[0, 1].set_title('客户价值分布（颜色=最近购买天数）')
        plt.colorbar(scatter, ax=axes[0, 1])
        
        # 各分层平均消费
        segment_avg_spend = customer_analysis.groupby('客户分层')['总消费'].mean()
        segment_avg_spend.plot(kind='bar', ax=axes[1, 0])
        axes[1, 0].set_title('各分层平均消费')
        axes[1, 0].set_xlabel('客户分层')
        axes[1, 0].set_ylabel('平均消费')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # 消费分布
        customer_analysis['总消费'].hist(bins=30, ax=axes[1, 1], alpha=0.7)
        axes[1, 1].set_title('客户消费分布')
        axes[1, 1].set_xlabel('总消费')
        axes[1, 1].set_ylabel('客户数')
        
        plt.tight_layout()
        plt.savefig(f'{self.config.PLOTS_DIR}/customer_segmentation.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return customer_analysis, segment_stats
    
    def generate_report(self):
        """生成分析报告"""
        print("\n=== 生成分析报告 ===")
        
        # 执行所有分析
        quality_report = self.data_quality_check()
        self.merge_data()
        user_results = self.user_analysis()
        product_results = self.product_analysis()
        sales_results = self.sales_analysis()
        customer_analysis, segment_stats = self.customer_segmentation()
        
        # 生成总结报告
        report = f"""
# 电商平台数据分析报告

## 数据概览
- 分析时间范围: {self.config.START_DATE} 至 {self.config.END_DATE}
- 用户总数: {len(self.users):,}
- 产品总数: {len(self.products):,}
- 订单总数: {len(self.orders):,}
- 总销售额: ¥{self.orders['实付金额'].sum():,.2f}

## 关键发现

### 用户特征
- 平均年龄: {self.users['年龄'].mean():.1f}岁
- 主要城市: {user_results['city_distribution'].index[0]}
- 会员分布: {user_results['member_distribution'].to_dict()}

### 产品表现
- 热门类别: {product_results['category_distribution'].index[0]}
- 平均价格: ¥{self.products['价格'].mean():.2f}
- 缺货产品: {(self.products['库存'] == 0).sum()} 个

### 销售表现
- 平均订单金额: ¥{self.orders['实付金额'].mean():.2f}
- 订单完成率: {(self.orders['订单状态'] == '已完成').mean()*100:.1f}%
- 主要支付方式: {self.orders['支付方式'].value_counts().index[0]}

### 客户价值
- 高价值客户占比: {(customer_analysis['客户分层'] == '高价值客户').mean()*100:.1f}%
- 客户平均消费: ¥{customer_analysis['总消费'].mean():.2f}
- 客户平均购买频次: {customer_analysis['购买频次'].mean():.1f}次

## 业务建议

1. **用户增长策略**
   - 重点发展{user_results['city_distribution'].index[0]}等核心城市市场
   - 提升会员转化率，特别是银牌到金牌的转化

2. **产品优化策略**
   - 加强{product_results['category_distribution'].index[0]}类产品的库存管理
   - 优化缺货产品的供应链

3. **客户运营策略**
   - 针对高价值客户制定VIP服务计划
   - 对低价值客户实施激活策略
   - 提升客户复购率和客单价

4. **营销策略**
   - 优化{self.orders['支付方式'].value_counts().index[0]}支付体验
   - 根据客户分层制定个性化营销方案
"""
        
        # 保存报告
        with open(f'{self.config.OUTPUT_DIR}/analysis_report.md', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("分析报告已生成！")
        print(f"报告文件: {self.config.OUTPUT_DIR}/analysis_report.md")
        print(f"图表文件: {self.config.PLOTS_DIR}/")
        
        return report


def main():
    """主函数"""
    print("电商平台数据分析项目")
    print("=" * 60)
    
    # 初始化配置
    config = Config()
    
    # 选择运行模式
    print("\n请选择运行模式：")
    print("1. 生成数据")
    print("2. 分析现有数据")
    print("3. 生成数据并分析")
    
    choice = input("请输入选择 (1/2/3): ").strip()
    
    if choice in ['1', '3']:
        # 生成数据
        generator = DataGenerator(config)
        users, products, orders, order_details, reviews = generator.generate_all_data()
    
    if choice in ['2', '3']:
        # 分析数据
        analyzer = DataAnalyzer(config)
        
        if analyzer.load_data():
            report = analyzer.generate_report()
            print("\n分析完成！")
        else:
            print("数据加载失败，请先生成数据！")
    
    print("\n" + "=" * 60)
    print("项目完成！")
    print("\n项目文件结构：")
    print("├── data/              # 数据文件")
    print("├── output/            # 分析报告")
    print("├── plots/             # 图表文件")
    print("└── data_analysis_project.py  # 主程序")


if __name__ == "__main__":
    main()