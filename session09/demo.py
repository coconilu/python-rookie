#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session09: 面向对象进阶 - 演示代码

本文件演示了面向对象编程的高级特性：继承、多态、封装等概念。
通过动物园管理系统展示这些特性的实际应用。

作者: Python教程团队
创建日期: 2024-01-09
最后修改: 2024-01-09
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional


class Animal(ABC):
    """动物抽象基类"""
    
    def __init__(self, name: str, age: int, species: str):
        self.name = name
        self.age = age
        self.species = species
        self._energy = 100
        self._health = 100
        self._last_fed = None
    
    @property
    def energy(self) -> int:
        """能量值（只读）"""
        return self._energy
    
    @property
    def health(self) -> int:
        """健康值（只读）"""
        return self._health
    
    def eat(self, food_amount: int = 20) -> None:
        """吃东西，恢复能量"""
        self._energy = min(100, self._energy + food_amount)
        self._last_fed = datetime.now()
        print(f"{self.name} 吃了食物，能量恢复到 {self._energy}")
    
    def sleep(self, hours: int = 8) -> None:
        """睡觉，恢复健康和能量"""
        energy_recovery = hours * 5
        health_recovery = hours * 3
        
        self._energy = min(100, self._energy + energy_recovery)
        self._health = min(100, self._health + health_recovery)
        
        print(f"{self.name} 睡了 {hours} 小时，能量: {self._energy}, 健康: {self._health}")
    
    @abstractmethod
    def make_sound(self) -> None:
        """发出声音（抽象方法）"""
        pass
    
    @abstractmethod
    def get_habitat_type(self) -> str:
        """获取栖息地类型（抽象方法）"""
        pass
    
    def get_info(self) -> str:
        """获取动物信息"""
        return f"{self.species} {self.name}，{self.age}岁，能量: {self._energy}, 健康: {self._health}"
    
    def __str__(self) -> str:
        return f"{self.name}({self.species})"


class Mammal(Animal):
    """哺乳动物类"""
    
    def __init__(self, name: str, age: int, species: str, fur_color: str):
        super().__init__(name, age, species)
        self.fur_color = fur_color
    
    def groom(self) -> None:
        """梳理毛发"""
        print(f"{self.name} 正在梳理 {self.fur_color} 的毛发")
        self._health = min(100, self._health + 5)


class Bird(Animal):
    """鸟类"""
    
    def __init__(self, name: str, age: int, species: str, can_fly: bool = True):
        super().__init__(name, age, species)
        self.can_fly = can_fly
    
    def fly(self) -> None:
        """飞行"""
        if self.can_fly and self._energy > 20:
            self._energy -= 10
            print(f"{self.name} 正在飞翔，消耗能量，剩余能量: {self._energy}")
        elif not self.can_fly:
            print(f"{self.name} 不会飞")
        else:
            print(f"{self.name} 能量不足，无法飞行")
    
    def build_nest(self) -> None:
        """筑巢"""
        print(f"{self.name} 正在筑巢")


class Reptile(Animal):
    """爬行动物类"""
    
    def __init__(self, name: str, age: int, species: str, is_venomous: bool = False):
        super().__init__(name, age, species)
        self.is_venomous = is_venomous
    
    def bask_in_sun(self) -> None:
        """晒太阳"""
        self._energy = min(100, self._energy + 15)
        print(f"{self.name} 正在晒太阳，能量恢复到 {self._energy}")


# 具体动物类
class Lion(Mammal):
    """狮子类"""
    
    def __init__(self, name: str, age: int, mane_length: str = "中等"):
        super().__init__(name, age, "狮子", "金黄色")
        self.mane_length = mane_length
    
    def make_sound(self) -> None:
        print(f"{self.name} 发出威武的咆哮声：吼~~~")
    
    def get_habitat_type(self) -> str:
        return "草原"
    
    def hunt(self) -> None:
        """狩猎"""
        if self._energy > 30:
            self._energy -= 20
            print(f"{self.name} 正在狩猎，消耗能量，剩余: {self._energy}")
        else:
            print(f"{self.name} 能量不足，无法狩猎")


class Elephant(Mammal):
    """大象类"""
    
    def __init__(self, name: str, age: int, trunk_length: float = 2.0):
        super().__init__(name, age, "大象", "灰色")
        self.trunk_length = trunk_length
    
    def make_sound(self) -> None:
        print(f"{self.name} 发出低沉的叫声：呜~~~")
    
    def get_habitat_type(self) -> str:
        return "草原"
    
    def spray_water(self) -> None:
        """喷水"""
        print(f"{self.name} 用 {self.trunk_length}米长的象鼻喷水")


class Eagle(Bird):
    """老鹰类"""
    
    def __init__(self, name: str, age: int, wingspan: float = 2.5):
        super().__init__(name, age, "老鹰", can_fly=True)
        self.wingspan = wingspan
    
    def make_sound(self) -> None:
        print(f"{self.name} 发出尖锐的叫声：啾~~~")
    
    def get_habitat_type(self) -> str:
        return "山地"
    
    def dive_attack(self) -> None:
        """俯冲攻击"""
        if self._energy > 25:
            self._energy -= 15
            print(f"{self.name} 展开 {self.wingspan}米的翅膀俯冲攻击")
        else:
            print(f"{self.name} 能量不足，无法俯冲")


class Penguin(Bird):
    """企鹅类"""
    
    def __init__(self, name: str, age: int, height: float = 0.8):
        super().__init__(name, age, "企鹅", can_fly=False)
        self.height = height
    
    def make_sound(self) -> None:
        print(f"{self.name} 发出可爱的叫声：嘎嘎嘎~~~")
    
    def get_habitat_type(self) -> str:
        return "极地"
    
    def swim(self) -> None:
        """游泳"""
        if self._energy > 15:
            self._energy -= 10
            print(f"{self.name} ({self.height}米高) 正在游泳")
        else:
            print(f"{self.name} 能量不足，无法游泳")


class Snake(Reptile):
    """蛇类"""
    
    def __init__(self, name: str, age: int, length: float = 2.0, is_venomous: bool = False):
        super().__init__(name, age, "蛇", is_venomous)
        self.length = length
    
    def make_sound(self) -> None:
        print(f"{self.name} 发出嘶嘶声：嘶嘶嘶~~~")
    
    def get_habitat_type(self) -> str:
        return "森林"
    
    def shed_skin(self) -> None:
        """蜕皮"""
        self._health = min(100, self._health + 10)
        print(f"{self.name} ({self.length}米长) 正在蜕皮，健康值提升到 {self._health}")


class ZooKeeper:
    """动物园管理员类"""
    
    def __init__(self, name: str, employee_id: str):
        self.name = name
        self.employee_id = employee_id
        self.animals_cared = []
    
    def feed_animal(self, animal: Animal, food_amount: int = 20) -> None:
        """喂养动物"""
        print(f"管理员 {self.name} 正在喂养 {animal.name}")
        animal.eat(food_amount)
        if animal not in self.animals_cared:
            self.animals_cared.append(animal)
    
    def check_animal_health(self, animal: Animal) -> None:
        """检查动物健康"""
        print(f"管理员 {self.name} 检查 {animal.get_info()}")
        if animal.health < 50:
            print(f"⚠️  {animal.name} 健康状况不佳，需要治疗")
        elif animal.energy < 30:
            print(f"⚠️  {animal.name} 能量不足，需要休息")
        else:
            print(f"✅ {animal.name} 状态良好")


class Habitat:
    """栖息地类"""
    
    def __init__(self, name: str, habitat_type: str, capacity: int = 10):
        self.name = name
        self.habitat_type = habitat_type
        self.capacity = capacity
        self.animals: List[Animal] = []
        self.temperature = 25  # 默认温度
    
    def add_animal(self, animal: Animal) -> bool:
        """添加动物到栖息地"""
        if len(self.animals) >= self.capacity:
            print(f"❌ {self.name} 已满，无法添加 {animal.name}")
            return False
        
        if animal.get_habitat_type() != self.habitat_type:
            print(f"❌ {animal.name} 不适合 {self.habitat_type} 环境")
            return False
        
        self.animals.append(animal)
        print(f"✅ {animal.name} 已添加到 {self.name}")
        return True
    
    def remove_animal(self, animal: Animal) -> bool:
        """从栖息地移除动物"""
        if animal in self.animals:
            self.animals.remove(animal)
            print(f"✅ {animal.name} 已从 {self.name} 移除")
            return True
        else:
            print(f"❌ {animal.name} 不在 {self.name} 中")
            return False
    
    def get_animal_count(self) -> int:
        """获取动物数量"""
        return len(self.animals)
    
    def list_animals(self) -> None:
        """列出所有动物"""
        print(f"\n🏞️  {self.name} ({self.habitat_type}) - {len(self.animals)}/{self.capacity}")
        if self.animals:
            for i, animal in enumerate(self.animals, 1):
                print(f"  {i}. {animal.get_info()}")
        else:
            print("  暂无动物")


class Zoo:
    """动物园类 - 使用组合模式"""
    
    def __init__(self, name: str):
        self.name = name
        self.habitats: List[Habitat] = []
        self.keepers: List[ZooKeeper] = []
        self.visitors_today = 0
    
    def add_habitat(self, habitat: Habitat) -> None:
        """添加栖息地"""
        self.habitats.append(habitat)
        print(f"✅ 栖息地 '{habitat.name}' 已添加到 {self.name}")
    
    def add_keeper(self, keeper: ZooKeeper) -> None:
        """添加管理员"""
        self.keepers.append(keeper)
        print(f"✅ 管理员 {keeper.name} 已加入 {self.name}")
    
    def get_all_animals(self) -> List[Animal]:
        """获取所有动物"""
        all_animals = []
        for habitat in self.habitats:
            all_animals.extend(habitat.animals)
        return all_animals
    
    def animal_concert(self) -> None:
        """动物音乐会 - 展示多态"""
        print(f"\n🎵 {self.name} 动物音乐会开始！")
        print("=" * 40)
        
        all_animals = self.get_all_animals()
        if not all_animals:
            print("暂无动物参加音乐会")
            return
        
        for i, animal in enumerate(all_animals, 1):
            print(f"{i}. ", end="")
            animal.make_sound()  # 多态：不同动物有不同的叫声
        
        print("=" * 40)
        print("🎵 音乐会结束！")
    
    def daily_care_routine(self) -> None:
        """日常护理流程"""
        print(f"\n🌅 {self.name} 开始日常护理")
        print("=" * 40)
        
        all_animals = self.get_all_animals()
        if not all_animals and self.keepers:
            print("暂无动物需要护理")
            return
        
        if not self.keepers:
            print("❌ 没有管理员，无法进行护理")
            return
        
        # 每个管理员负责一些动物
        animals_per_keeper = len(all_animals) // len(self.keepers) + 1
        
        for i, keeper in enumerate(self.keepers):
            start_idx = i * animals_per_keeper
            end_idx = min((i + 1) * animals_per_keeper, len(all_animals))
            assigned_animals = all_animals[start_idx:end_idx]
            
            if assigned_animals:
                print(f"\n👨‍🔬 {keeper.name} 负责护理:")
                for animal in assigned_animals:
                    keeper.feed_animal(animal)
                    keeper.check_animal_health(animal)
                    print()
        
        print("=" * 40)
        print("🌅 日常护理完成")
    
    def show_zoo_status(self) -> None:
        """显示动物园状态"""
        print(f"\n🏛️  {self.name} 状态报告")
        print("=" * 50)
        
        print(f"📊 栖息地数量: {len(self.habitats)}")
        print(f"👨‍🔬 管理员数量: {len(self.keepers)}")
        print(f"🐾 动物总数: {len(self.get_all_animals())}")
        print(f"👥 今日访客: {self.visitors_today}")
        
        # 显示各栖息地详情
        for habitat in self.habitats:
            habitat.list_animals()
        
        print("=" * 50)


def demonstrate_inheritance():
    """演示继承"""
    print("\n" + "=" * 50)
    print("🧬 继承演示")
    print("=" * 50)
    
    # 创建不同类型的动物
    lion = Lion("辛巴", 5, "浓密")
    elephant = Elephant("大宝", 10, 2.5)
    eagle = Eagle("雄鹰", 3, 3.0)
    penguin = Penguin("波波", 2, 0.9)
    snake = Snake("小青", 4, 1.8, False)
    
    animals = [lion, elephant, eagle, penguin, snake]
    
    # 展示继承的方法
    for animal in animals:
        print(f"\n{animal.get_info()}")
        animal.make_sound()
        animal.eat()
        
        # 调用特有方法
        if isinstance(animal, Lion):
            animal.hunt()
        elif isinstance(animal, Elephant):
            animal.spray_water()
        elif isinstance(animal, Eagle):
            animal.dive_attack()
        elif isinstance(animal, Penguin):
            animal.swim()
        elif isinstance(animal, Snake):
            animal.shed_skin()


def demonstrate_polymorphism():
    """演示多态"""
    print("\n" + "=" * 50)
    print("🎭 多态演示")
    print("=" * 50)
    
    # 创建动物列表
    animals = [
        Lion("雷欧", 6),
        Elephant("艾莉", 15),
        Eagle("天鹰", 4),
        Penguin("皮皮", 3),
        Snake("小绿", 5, 2.2, True)
    ]
    
    # 多态：同一个方法调用，不同的实现
    print("🎵 动物大合唱（多态演示）:")
    for i, animal in enumerate(animals, 1):
        print(f"{i}. ", end="")
        animal.make_sound()  # 多态调用
    
    print("\n🏠 栖息地需求:")
    for animal in animals:
        print(f"{animal.name} 需要 {animal.get_habitat_type()} 环境")


def demonstrate_encapsulation():
    """演示封装"""
    print("\n" + "=" * 50)
    print("🔒 封装演示")
    print("=" * 50)
    
    lion = Lion("狮王", 8)
    
    # 展示属性访问控制
    print(f"公开属性 - 姓名: {lion.name}")
    print(f"只读属性 - 能量: {lion.energy}")
    print(f"只读属性 - 健康: {lion.health}")
    
    # 尝试直接修改受保护的属性（不推荐）
    print("\n⚠️  尝试直接修改内部属性（不推荐）:")
    original_energy = lion.energy
    lion._energy = 50  # 直接修改受保护属性
    print(f"直接修改后能量: {lion.energy}")
    
    # 通过方法修改（推荐）
    print("\n✅ 通过方法修改（推荐）:")
    lion.eat(30)
    lion.sleep(6)


def main():
    """主函数：演示面向对象进阶特性"""
    print("Session09: 面向对象进阶演示")
    print("=" * 60)
    
    # 1. 演示继承
    demonstrate_inheritance()
    
    # 2. 演示多态
    demonstrate_polymorphism()
    
    # 3. 演示封装
    demonstrate_encapsulation()
    
    # 4. 综合演示：动物园管理系统
    print("\n" + "=" * 50)
    print("🏛️  动物园管理系统综合演示")
    print("=" * 50)
    
    # 创建动物园
    zoo = Zoo("快乐动物园")
    
    # 创建栖息地
    grassland = Habitat("非洲草原", "草原", 5)
    mountain = Habitat("高山区域", "山地", 3)
    polar_area = Habitat("极地馆", "极地", 4)
    forest = Habitat("热带雨林", "森林", 6)
    
    zoo.add_habitat(grassland)
    zoo.add_habitat(mountain)
    zoo.add_habitat(polar_area)
    zoo.add_habitat(forest)
    
    # 创建管理员
    keeper1 = ZooKeeper("张三", "ZK001")
    keeper2 = ZooKeeper("李四", "ZK002")
    
    zoo.add_keeper(keeper1)
    zoo.add_keeper(keeper2)
    
    # 创建动物并分配到栖息地
    animals_to_add = [
        (Lion("狮王", 7), grassland),
        (Lion("母狮", 5), grassland),
        (Elephant("象王", 12), grassland),
        (Eagle("金雕", 4), mountain),
        (Penguin("企鹅1号", 3), polar_area),
        (Penguin("企鹅2号", 2), polar_area),
        (Snake("森蚺", 6, 3.0), forest)
    ]
    
    for animal, habitat in animals_to_add:
        habitat.add_animal(animal)
    
    # 显示动物园状态
    zoo.show_zoo_status()
    
    # 动物音乐会（多态演示）
    zoo.animal_concert()
    
    # 日常护理
    zoo.daily_care_routine()
    
    # 再次显示状态
    zoo.show_zoo_status()
    
    print("\n🎉 演示完成！")
    print("\n💡 关键概念总结:")
    print("   • 继承: 子类继承父类的属性和方法")
    print("   • 多态: 同一接口的不同实现")
    print("   • 封装: 隐藏内部实现，提供公共接口")
    print("   • 抽象类: 定义接口规范，不能直接实例化")
    print("   • 组合: 通过包含其他对象来实现功能")


if __name__ == "__main__":
    main()