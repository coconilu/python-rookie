#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session09 示例1: 继承基础

演示继承的基本概念和语法，包括：
- 基本继承语法
- super()函数的使用
- 方法重写
- 属性继承

作者: Python教程团队
创建日期: 2024-01-09
"""


class Vehicle:
    """交通工具基类"""
    
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year
        self.speed = 0
        self.is_running = False
    
    def start(self):
        """启动"""
        self.is_running = True
        print(f"{self.brand} {self.model} 启动了")
    
    def stop(self):
        """停止"""
        self.is_running = False
        self.speed = 0
        print(f"{self.brand} {self.model} 停止了")
    
    def accelerate(self, increment):
        """加速"""
        if self.is_running:
            self.speed += increment
            print(f"加速到 {self.speed} km/h")
        else:
            print("请先启动车辆")
    
    def get_info(self):
        """获取车辆信息"""
        return f"{self.year}年 {self.brand} {self.model}"


class Car(Vehicle):
    """汽车类 - 继承自Vehicle"""
    
    def __init__(self, brand, model, year, fuel_type, doors=4):
        # 调用父类构造函数
        super().__init__(brand, model, year)
        # 添加子类特有属性
        self.fuel_type = fuel_type
        self.doors = doors
        self.fuel_level = 100
    
    def start(self):
        """重写启动方法"""
        if self.fuel_level > 0:
            super().start()  # 调用父类方法
            print(f"燃料类型: {self.fuel_type}")
            print(f"车门数: {self.doors}")
        else:
            print("燃料不足，无法启动")
    
    def refuel(self, amount):
        """加油 - 子类特有方法"""
        self.fuel_level = min(100, self.fuel_level + amount)
        print(f"加油完成，燃料水平: {self.fuel_level}%")
    
    def accelerate(self, increment):
        """重写加速方法，增加燃料消耗"""
        if self.fuel_level > 0:
            super().accelerate(increment)  # 调用父类方法
            # 添加燃料消耗逻辑
            fuel_consumption = increment * 0.1
            self.fuel_level = max(0, self.fuel_level - fuel_consumption)
            print(f"燃料消耗: {fuel_consumption:.1f}%, 剩余: {self.fuel_level:.1f}%")
        else:
            print("燃料不足，无法加速")
    
    def get_info(self):
        """重写信息获取方法"""
        base_info = super().get_info()  # 获取父类信息
        return f"{base_info}, {self.fuel_type}燃料, {self.doors}门"


class Motorcycle(Vehicle):
    """摩托车类 - 继承自Vehicle"""
    
    def __init__(self, brand, model, year, engine_size):
        super().__init__(brand, model, year)
        self.engine_size = engine_size  # 发动机排量
        self.has_sidecar = False
    
    def start(self):
        """重写启动方法"""
        super().start()
        print(f"发动机排量: {self.engine_size}cc")
    
    def wheelie(self):
        """翘头 - 摩托车特有方法"""
        if self.is_running and self.speed > 20:
            print(f"{self.brand} {self.model} 正在翘头！")
        else:
            print("速度不够或未启动，无法翘头")
    
    def add_sidecar(self):
        """添加边车"""
        self.has_sidecar = True
        print("已添加边车")
    
    def get_info(self):
        """重写信息获取方法"""
        base_info = super().get_info()
        sidecar_info = "带边车" if self.has_sidecar else "无边车"
        return f"{base_info}, {self.engine_size}cc, {sidecar_info}"


class ElectricCar(Car):
    """电动汽车类 - 多层继承"""
    
    def __init__(self, brand, model, year, battery_capacity, doors=4):
        # 注意：电动车的fuel_type固定为"电力"
        super().__init__(brand, model, year, "电力", doors)
        self.battery_capacity = battery_capacity  # 电池容量(kWh)
        self.charge_level = 100  # 电量百分比
        # 重写燃料相关属性
        self.fuel_level = self.charge_level
    
    def start(self):
        """重写启动方法"""
        if self.charge_level > 0:
            # 调用Vehicle的start方法，跳过Car的start
            Vehicle.start(self)
            print(f"电池容量: {self.battery_capacity} kWh")
            print(f"当前电量: {self.charge_level}%")
            print(f"车门数: {self.doors}")
        else:
            print("电量不足，无法启动")
    
    def charge(self, amount):
        """充电"""
        self.charge_level = min(100, self.charge_level + amount)
        self.fuel_level = self.charge_level  # 同步更新
        print(f"充电完成，电量: {self.charge_level}%")
    
    def refuel(self, amount):
        """重写加油方法为充电"""
        print("电动车不需要加油，请使用充电功能")
        self.charge(amount)
    
    def accelerate(self, increment):
        """重写加速方法"""
        if self.charge_level > 0:
            Vehicle.accelerate(self, increment)  # 直接调用Vehicle的方法
            # 电动车的能耗计算
            energy_consumption = increment * 0.05  # 电动车更节能
            self.charge_level = max(0, self.charge_level - energy_consumption)
            self.fuel_level = self.charge_level
            print(f"电量消耗: {energy_consumption:.1f}%, 剩余: {self.charge_level:.1f}%")
        else:
            print("电量不足，无法加速")
    
    def get_info(self):
        """重写信息获取方法"""
        base_info = Vehicle.get_info(self)  # 直接调用Vehicle的方法
        return f"{base_info}, 电动车, {self.battery_capacity}kWh电池, {self.doors}门"


def demonstrate_basic_inheritance():
    """演示基本继承"""
    print("=== 基本继承演示 ===")
    
    # 创建基类对象
    vehicle = Vehicle("通用", "基础款", 2020)
    print(f"基类: {vehicle.get_info()}")
    vehicle.start()
    vehicle.accelerate(30)
    vehicle.stop()
    print()
    
    # 创建子类对象
    car = Car("丰田", "卡罗拉", 2023, "汽油", 4)
    print(f"汽车: {car.get_info()}")
    car.start()
    car.accelerate(50)
    car.accelerate(30)
    car.refuel(20)
    car.stop()
    print()
    
    motorcycle = Motorcycle("本田", "CBR600", 2022, 600)
    print(f"摩托车: {motorcycle.get_info()}")
    motorcycle.start()
    motorcycle.accelerate(40)
    motorcycle.wheelie()
    motorcycle.add_sidecar()
    print(f"更新后: {motorcycle.get_info()}")
    motorcycle.stop()
    print()


def demonstrate_multilevel_inheritance():
    """演示多层继承"""
    print("=== 多层继承演示 ===")
    
    # 创建电动汽车（三层继承：Vehicle -> Car -> ElectricCar）
    tesla = ElectricCar("特斯拉", "Model 3", 2023, 75, 4)
    print(f"电动汽车: {tesla.get_info()}")
    
    tesla.start()
    tesla.accelerate(60)
    tesla.accelerate(40)
    
    # 尝试加油（会转为充电）
    tesla.refuel(30)
    
    # 直接充电
    tesla.charge(20)
    
    tesla.accelerate(20)
    tesla.stop()
    print()


def demonstrate_method_resolution():
    """演示方法解析"""
    print("=== 方法解析演示 ===")
    
    # 查看继承链
    print("继承链信息:")
    print(f"Car的MRO: {Car.__mro__}")
    print(f"ElectricCar的MRO: {ElectricCar.__mro__}")
    print()
    
    # 演示不同层次的方法调用
    tesla = ElectricCar("比亚迪", "汉EV", 2023, 85)
    
    print("方法调用演示:")
    print(f"get_info(): {tesla.get_info()}")
    print(f"isinstance(tesla, Vehicle): {isinstance(tesla, Vehicle)}")
    print(f"isinstance(tesla, Car): {isinstance(tesla, Car)}")
    print(f"isinstance(tesla, ElectricCar): {isinstance(tesla, ElectricCar)}")
    print()


def demonstrate_super_usage():
    """演示super()的不同用法"""
    print("=== super()用法演示 ===")
    
    class SportsCar(Car):
        """跑车类 - 演示super()的高级用法"""
        
        def __init__(self, brand, model, year, fuel_type, max_speed, doors=2):
            super().__init__(brand, model, year, fuel_type, doors)
            self.max_speed = max_speed
            self.turbo_mode = False
        
        def accelerate(self, increment):
            """跑车加速 - 有涡轮模式"""
            if self.turbo_mode:
                increment *= 1.5  # 涡轮模式加速更快
                print("🚀 涡轮模式激活！")
            
            # 调用父类方法
            super().accelerate(increment)
            
            # 检查是否超过最大速度
            if self.speed > self.max_speed:
                self.speed = self.max_speed
                print(f"⚠️  已达到最大速度 {self.max_speed} km/h")
        
        def enable_turbo(self):
            """启用涡轮模式"""
            self.turbo_mode = True
            print("涡轮模式已启用")
        
        def disable_turbo(self):
            """禁用涡轮模式"""
            self.turbo_mode = False
            print("涡轮模式已禁用")
    
    # 测试跑车
    ferrari = SportsCar("法拉利", "488 GTB", 2023, "汽油", 330)
    print(f"跑车: {ferrari.get_info()}")
    
    ferrari.start()
    ferrari.accelerate(100)
    ferrari.enable_turbo()
    ferrari.accelerate(100)
    ferrari.accelerate(200)  # 会触发最大速度限制
    ferrari.disable_turbo()
    ferrari.stop()
    print()


def main():
    """主函数"""
    print("Session09 示例1: 继承基础")
    print("=" * 50)
    
    demonstrate_basic_inheritance()
    demonstrate_multilevel_inheritance()
    demonstrate_method_resolution()
    demonstrate_super_usage()
    
    print("\n💡 继承要点总结:")
    print("   • 使用class 子类(父类)语法定义继承")
    print("   • super()调用父类方法")
    print("   • 子类可以重写父类方法")
    print("   • 子类继承父类的所有属性和方法")
    print("   • isinstance()检查对象类型")
    print("   • MRO决定方法解析顺序")


if __name__ == "__main__":
    main()