#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session09 练习2: 多态和抽象类练习

练习目标：
1. 理解多态的概念和应用
2. 掌握抽象基类的使用
3. 实现接口统一性
4. 理解鸭子类型

作者: Python教程团队
创建日期: 2024-01-09
"""

from abc import ABC, abstractmethod
import math
from typing import List, Protocol

# ============================================================================
# 练习1: 图形计算系统 - 抽象基类和多态
# ============================================================================

class Shape(ABC):
    """图形抽象基类
    
    TODO: 实现抽象基类，定义所有图形的通用接口
    """
    
    def __init__(self, name):
        # TODO: 初始化图形名称
        pass
    
    @abstractmethod
    def calculate_area(self):
        """计算面积 - 抽象方法"""
        # TODO: 定义抽象方法
        pass
    
    @abstractmethod
    def calculate_perimeter(self):
        """计算周长 - 抽象方法"""
        # TODO: 定义抽象方法
        pass
    
    def get_info(self):
        """获取图形信息 - 具体方法"""
        # TODO: 返回包含名称、面积、周长的信息
        pass
    
    def __str__(self):
        # TODO: 返回图形的字符串表示
        pass


class Rectangle(Shape):
    """矩形类
    
    TODO: 继承Shape，实现矩形的具体计算
    """
    
    def __init__(self, width, height):
        # TODO: 调用父类初始化，设置宽度和高度
        pass
    
    def calculate_area(self):
        """计算矩形面积"""
        # TODO: 返回 width * height
        pass
    
    def calculate_perimeter(self):
        """计算矩形周长"""
        # TODO: 返回 2 * (width + height)
        pass


class Circle(Shape):
    """圆形类
    
    TODO: 继承Shape，实现圆形的具体计算
    """
    
    def __init__(self, radius):
        # TODO: 调用父类初始化，设置半径
        pass
    
    def calculate_area(self):
        """计算圆形面积"""
        # TODO: 返回 π * radius²
        pass
    
    def calculate_perimeter(self):
        """计算圆形周长"""
        # TODO: 返回 2 * π * radius
        pass


class Triangle(Shape):
    """三角形类
    
    TODO: 继承Shape，实现三角形的具体计算
    """
    
    def __init__(self, side_a, side_b, side_c):
        # TODO: 调用父类初始化，设置三边长
        # 验证三边是否能构成三角形
        pass
    
    def _is_valid_triangle(self, a, b, c):
        """验证是否为有效三角形"""
        # TODO: 检查三角形不等式
        pass
    
    def calculate_area(self):
        """计算三角形面积 - 使用海伦公式"""
        # TODO: 使用海伦公式计算面积
        # s = (a + b + c) / 2
        # area = sqrt(s * (s-a) * (s-b) * (s-c))
        pass
    
    def calculate_perimeter(self):
        """计算三角形周长"""
        # TODO: 返回三边之和
        pass


class RegularPolygon(Shape):
    """正多边形类
    
    TODO: 继承Shape，实现正多边形的计算
    """
    
    def __init__(self, sides, side_length):
        # TODO: 调用父类初始化，设置边数和边长
        pass
    
    def calculate_area(self):
        """计算正多边形面积"""
        # TODO: 使用公式 (n * s²) / (4 * tan(π/n))
        # 其中 n 是边数，s 是边长
        pass
    
    def calculate_perimeter(self):
        """计算正多边形周长"""
        # TODO: 返回 sides * side_length
        pass


# ============================================================================
# 练习2: 媒体播放器系统 - 协议和鸭子类型
# ============================================================================

class Playable(Protocol):
    """可播放协议
    
    TODO: 定义播放相关的协议方法
    """
    
    def play(self) -> str:
        """播放"""
        ...
    
    def pause(self) -> str:
        """暂停"""
        ...
    
    def stop(self) -> str:
        """停止"""
        ...
    
    def get_duration(self) -> int:
        """获取时长（秒）"""
        ...


class AudioFile:
    """音频文件类
    
    TODO: 实现音频文件的播放功能
    """
    
    def __init__(self, filename, duration, format_type="mp3"):
        # TODO: 初始化音频文件属性
        pass
    
    def play(self):
        """播放音频"""
        # TODO: 返回播放信息
        pass
    
    def pause(self):
        """暂停音频"""
        # TODO: 返回暂停信息
        pass
    
    def stop(self):
        """停止音频"""
        # TODO: 返回停止信息
        pass
    
    def get_duration(self):
        """获取音频时长"""
        # TODO: 返回时长
        pass


class VideoFile:
    """视频文件类
    
    TODO: 实现视频文件的播放功能
    """
    
    def __init__(self, filename, duration, resolution="1080p", format_type="mp4"):
        # TODO: 初始化视频文件属性
        pass
    
    def play(self):
        """播放视频"""
        # TODO: 返回播放信息
        pass
    
    def pause(self):
        """暂停视频"""
        # TODO: 返回暂停信息
        pass
    
    def stop(self):
        """停止视频"""
        # TODO: 返回停止信息
        pass
    
    def get_duration(self):
        """获取视频时长"""
        # TODO: 返回时长
        pass


class Podcast:
    """播客类
    
    TODO: 实现播客的播放功能
    """
    
    def __init__(self, title, host, duration, episode_number):
        # TODO: 初始化播客属性
        pass
    
    def play(self):
        """播放播客"""
        # TODO: 返回播放信息
        pass
    
    def pause(self):
        """暂停播客"""
        # TODO: 返回暂停信息
        pass
    
    def stop(self):
        """停止播客"""
        # TODO: 返回停止信息
        pass
    
    def get_duration(self):
        """获取播客时长"""
        # TODO: 返回时长
        pass


class MediaPlayer:
    """媒体播放器类
    
    TODO: 实现通用的媒体播放器，支持多种媒体类型
    """
    
    def __init__(self):
        # TODO: 初始化播放列表和当前播放项
        pass
    
    def add_media(self, media: Playable):
        """添加媒体到播放列表"""
        # TODO: 添加媒体到播放列表
        pass
    
    def play_all(self):
        """播放所有媒体"""
        # TODO: 遍历播放列表，播放所有媒体
        pass
    
    def get_total_duration(self):
        """获取总播放时长"""
        # TODO: 计算所有媒体的总时长
        pass
    
    def play_by_type(self, media_type):
        """按类型播放媒体"""
        # TODO: 播放指定类型的媒体
        pass


# ============================================================================
# 练习3: 支付系统 - 策略模式和多态
# ============================================================================

class PaymentMethod(ABC):
    """支付方式抽象基类
    
    TODO: 定义支付方式的抽象接口
    """
    
    @abstractmethod
    def process_payment(self, amount: float) -> dict:
        """处理支付"""
        pass
    
    @abstractmethod
    def validate_payment_info(self) -> bool:
        """验证支付信息"""
        pass
    
    @abstractmethod
    def get_payment_fee(self, amount: float) -> float:
        """获取支付手续费"""
        pass


class CreditCardPayment(PaymentMethod):
    """信用卡支付
    
    TODO: 实现信用卡支付方式
    """
    
    def __init__(self, card_number, cardholder_name, expiry_date, cvv):
        # TODO: 初始化信用卡信息
        pass
    
    def process_payment(self, amount):
        """处理信用卡支付"""
        # TODO: 实现信用卡支付逻辑
        pass
    
    def validate_payment_info(self):
        """验证信用卡信息"""
        # TODO: 验证卡号、有效期等信息
        pass
    
    def get_payment_fee(self, amount):
        """信用卡手续费 - 2.5%"""
        # TODO: 返回手续费
        pass


class PayPalPayment(PaymentMethod):
    """PayPal支付
    
    TODO: 实现PayPal支付方式
    """
    
    def __init__(self, email, password):
        # TODO: 初始化PayPal账户信息
        pass
    
    def process_payment(self, amount):
        """处理PayPal支付"""
        # TODO: 实现PayPal支付逻辑
        pass
    
    def validate_payment_info(self):
        """验证PayPal账户信息"""
        # TODO: 验证邮箱格式等
        pass
    
    def get_payment_fee(self, amount):
        """PayPal手续费 - 3%"""
        # TODO: 返回手续费
        pass


class BankTransferPayment(PaymentMethod):
    """银行转账支付
    
    TODO: 实现银行转账支付方式
    """
    
    def __init__(self, account_number, bank_name, account_holder):
        # TODO: 初始化银行账户信息
        pass
    
    def process_payment(self, amount):
        """处理银行转账支付"""
        # TODO: 实现银行转账支付逻辑
        pass
    
    def validate_payment_info(self):
        """验证银行账户信息"""
        # TODO: 验证账户号等信息
        pass
    
    def get_payment_fee(self, amount):
        """银行转账手续费 - 固定5元"""
        # TODO: 返回固定手续费
        pass


class PaymentProcessor:
    """支付处理器
    
    TODO: 实现支付处理器，支持多种支付方式
    """
    
    def __init__(self):
        # TODO: 初始化支付历史
        pass
    
    def process_payment(self, payment_method: PaymentMethod, amount: float):
        """处理支付"""
        # TODO: 使用指定的支付方式处理支付
        # 1. 验证支付信息
        # 2. 计算手续费
        # 3. 处理支付
        # 4. 记录支付历史
        pass
    
    def get_payment_history(self):
        """获取支付历史"""
        # TODO: 返回支付历史
        pass
    
    def calculate_total_fees(self):
        """计算总手续费"""
        # TODO: 计算所有支付的总手续费
        pass


# ============================================================================
# 测试函数
# ============================================================================

def test_shape_polymorphism():
    """测试图形多态性"""
    print("=== 测试图形多态性 ===")
    
    # TODO: 创建不同类型的图形
    # shapes = [
    #     Rectangle(5, 3),
    #     Circle(4),
    #     Triangle(3, 4, 5),
    #     RegularPolygon(6, 2)  # 正六边形
    # ]
    
    # TODO: 测试多态调用
    # for shape in shapes:
    #     print(shape)
    #     print(f"  面积: {shape.calculate_area():.2f}")
    #     print(f"  周长: {shape.calculate_perimeter():.2f}")
    #     print()
    
    pass


def test_media_player_duck_typing():
    """测试媒体播放器的鸭子类型"""
    print("=== 测试媒体播放器鸭子类型 ===")
    
    # TODO: 创建不同类型的媒体
    # audio = AudioFile("song.mp3", 180)
    # video = VideoFile("movie.mp4", 7200, "4K")
    # podcast = Podcast("Tech Talk", "John Doe", 3600, 15)
    
    # TODO: 创建播放器并添加媒体
    # player = MediaPlayer()
    # player.add_media(audio)
    # player.add_media(video)
    # player.add_media(podcast)
    
    # TODO: 测试播放功能
    # player.play_all()
    # print(f"总时长: {player.get_total_duration()} 秒")
    
    pass


def test_payment_strategy():
    """测试支付策略模式"""
    print("=== 测试支付策略模式 ===")
    
    # TODO: 创建不同的支付方式
    # credit_card = CreditCardPayment("1234-5678-9012-3456", "John Doe", "12/25", "123")
    # paypal = PayPalPayment("john@example.com", "password123")
    # bank_transfer = BankTransferPayment("9876543210", "中国银行", "张三")
    
    # TODO: 创建支付处理器
    # processor = PaymentProcessor()
    
    # TODO: 测试不同支付方式
    # processor.process_payment(credit_card, 100.0)
    # processor.process_payment(paypal, 50.0)
    # processor.process_payment(bank_transfer, 200.0)
    
    # TODO: 查看支付历史和手续费
    # print("支付历史:")
    # for record in processor.get_payment_history():
    #     print(f"  {record}")
    # print(f"总手续费: {processor.calculate_total_fees():.2f}")
    
    pass


def test_abstract_class_enforcement():
    """测试抽象类的强制性"""
    print("=== 测试抽象类强制性 ===")
    
    # TODO: 尝试直接实例化抽象类（应该失败）
    # try:
    #     shape = Shape("test")  # 这应该抛出TypeError
    # except TypeError as e:
    #     print(f"✅ 抽象类无法实例化: {e}")
    
    # TODO: 测试未完全实现抽象方法的子类
    # class IncompleteShape(Shape):
    #     def calculate_area(self):
    #         return 0
    #     # 缺少 calculate_perimeter 的实现
    
    # try:
    #     incomplete = IncompleteShape("incomplete")  # 这应该抛出TypeError
    # except TypeError as e:
    #     print(f"✅ 未完全实现抽象方法的类无法实例化: {e}")
    
    pass


def main():
    """主函数 - 运行所有测试"""
    print("Session09 练习2: 多态和抽象类练习")
    print("=" * 50)
    
    test_shape_polymorphism()
    test_media_player_duck_typing()
    test_payment_strategy()
    test_abstract_class_enforcement()
    
    print("\n💡 练习要点:")
    print("   1. 抽象基类定义统一接口")
    print("   2. 多态实现不同行为")
    print("   3. 协议定义鸭子类型")
    print("   4. 策略模式的应用")
    print("   5. 接口的一致性")
    
    print("\n🎯 完成练习后，请运行测试函数验证实现")


if __name__ == "__main__":
    main()


# ============================================================================
# 练习提示和参考答案
# ============================================================================

"""
💡 实现提示：

1. Shape抽象基类：
   - 使用@abstractmethod装饰器
   - 定义calculate_area和calculate_perimeter抽象方法
   - 实现get_info等具体方法

2. 具体图形类：
   - Rectangle: area = width * height, perimeter = 2 * (width + height)
   - Circle: area = π * r², perimeter = 2 * π * r
   - Triangle: 使用海伦公式计算面积
   - RegularPolygon: 使用正多边形公式

3. 媒体播放器：
   - 实现Playable协议的所有方法
   - MediaPlayer使用鸭子类型处理不同媒体
   - 注意类型提示的使用

4. 支付系统：
   - PaymentMethod定义抽象接口
   - 各支付方式实现具体逻辑
   - PaymentProcessor使用策略模式

5. 测试要点：
   - 验证多态调用的正确性
   - 检查抽象类的强制性
   - 测试鸭子类型的灵活性
   - 确认策略模式的可扩展性

🔍 关键概念：
   - 抽象基类 (ABC)
   - 协议 (Protocol)
   - 多态性
   - 鸭子类型
   - 策略模式
"""