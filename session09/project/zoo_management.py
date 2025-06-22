#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session09 项目: 动物园管理系统

这是一个综合性的面向对象编程项目，展示了：
- 继承和多态的实际应用
- 抽象基类的设计
- 封装和访问控制
- 组合关系的使用
- 设计模式的应用

项目功能：
1. 动物管理（不同种类的动物）
2. 栖息地管理
3. 饲养员管理
4. 游客管理
5. 喂食和护理系统
6. 事件通知系统

作者: Python教程团队
创建日期: 2024-01-09
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Set
from enum import Enum
import random
import json

# ============================================================================
# 枚举定义
# ============================================================================

class AnimalType(Enum):
    """动物类型枚举"""
    MAMMAL = "哺乳动物"
    BIRD = "鸟类"
    REPTILE = "爬行动物"
    AMPHIBIAN = "两栖动物"
    FISH = "鱼类"


class DietType(Enum):
    """饮食类型枚举"""
    CARNIVORE = "肉食性"
    HERBIVORE = "草食性"
    OMNIVORE = "杂食性"


class ActivityLevel(Enum):
    """活动水平枚举"""
    LOW = "低"
    MEDIUM = "中等"
    HIGH = "高"


class HealthStatus(Enum):
    """健康状态枚举"""
    EXCELLENT = "优秀"
    GOOD = "良好"
    FAIR = "一般"
    POOR = "较差"
    CRITICAL = "危急"


class StaffRole(Enum):
    """员工角色枚举"""
    KEEPER = "饲养员"
    VETERINARIAN = "兽医"
    MANAGER = "管理员"
    GUIDE = "导游"


# ============================================================================
# 观察者模式 - 事件系统
# ============================================================================

class Observer(ABC):
    """观察者抽象基类"""
    
    @abstractmethod
    def update(self, event_type: str, data: dict):
        """接收事件通知"""
        pass


class EventPublisher:
    """事件发布者"""
    
    def __init__(self):
        self._observers: Dict[str, List[Observer]] = {}
    
    def subscribe(self, event_type: str, observer: Observer):
        """订阅事件"""
        if event_type not in self._observers:
            self._observers[event_type] = []
        if observer not in self._observers[event_type]:
            self._observers[event_type].append(observer)
    
    def unsubscribe(self, event_type: str, observer: Observer):
        """取消订阅"""
        if event_type in self._observers and observer in self._observers[event_type]:
            self._observers[event_type].remove(observer)
    
    def notify(self, event_type: str, data: dict):
        """通知观察者"""
        if event_type in self._observers:
            for observer in self._observers[event_type]:
                observer.update(event_type, data)


# ============================================================================
# 动物类层次结构
# ============================================================================

class Animal(ABC):
    """动物抽象基类"""
    
    def __init__(self, animal_id: str, name: str, species: str, age: int, 
                 animal_type: AnimalType, diet_type: DietType):
        self.animal_id = animal_id
        self.name = name
        self.species = species
        self.age = age
        self.animal_type = animal_type
        self.diet_type = diet_type
        
        # 受保护属性
        self._health_status = HealthStatus.GOOD
        self._last_fed = None
        self._last_checkup = None
        self._weight = 0.0
        self._activity_level = ActivityLevel.MEDIUM
        
        # 私有属性
        self.__medical_records = []
        self.__birth_date = datetime.now() - timedelta(days=age*365)
        
        # 事件发布者
        self._event_publisher = EventPublisher()
    
    @property
    def health_status(self) -> HealthStatus:
        """健康状态"""
        return self._health_status
    
    @health_status.setter
    def health_status(self, status: HealthStatus):
        """设置健康状态并发布事件"""
        old_status = self._health_status
        self._health_status = status
        
        if old_status != status:
            self._event_publisher.notify("health_changed", {
                "animal_id": self.animal_id,
                "animal_name": self.name,
                "old_status": old_status.value,
                "new_status": status.value,
                "timestamp": datetime.now()
            })
    
    @property
    def weight(self) -> float:
        """体重"""
        return self._weight
    
    @weight.setter
    def weight(self, value: float):
        """设置体重"""
        if value <= 0:
            raise ValueError("体重必须大于0")
        self._weight = value
    
    @property
    def days_since_last_fed(self) -> int:
        """距离上次喂食的天数"""
        if self._last_fed is None:
            return 999  # 表示从未喂食
        return (datetime.now() - self._last_fed).days
    
    @property
    def needs_feeding(self) -> bool:
        """是否需要喂食"""
        return self.days_since_last_fed >= self.get_feeding_interval()
    
    @abstractmethod
    def make_sound(self) -> str:
        """发出声音 - 抽象方法"""
        pass
    
    @abstractmethod
    def get_feeding_interval(self) -> int:
        """获取喂食间隔（天数）- 抽象方法"""
        pass
    
    @abstractmethod
    def get_habitat_requirements(self) -> Dict[str, str]:
        """获取栖息地要求 - 抽象方法"""
        pass
    
    def feed(self, food_type: str, amount: float):
        """喂食"""
        if not self._is_appropriate_food(food_type):
            raise ValueError(f"{food_type} 不适合 {self.species}")
        
        self._last_fed = datetime.now()
        self._event_publisher.notify("animal_fed", {
            "animal_id": self.animal_id,
            "animal_name": self.name,
            "food_type": food_type,
            "amount": amount,
            "timestamp": datetime.now()
        })
        
        return f"{self.name} 吃了 {amount}kg 的 {food_type}"
    
    def medical_checkup(self, veterinarian_name: str, notes: str = ""):
        """医疗检查"""
        self._last_checkup = datetime.now()
        
        # 随机生成健康状态（模拟检查结果）
        health_statuses = list(HealthStatus)
        weights = [0.4, 0.3, 0.2, 0.08, 0.02]  # 偏向良好状态
        new_status = random.choices(health_statuses, weights=weights)[0]
        
        record = {
            "date": self._last_checkup,
            "veterinarian": veterinarian_name,
            "health_status": new_status,
            "notes": notes
        }
        
        self.__medical_records.append(record)
        self.health_status = new_status
        
        return f"{self.name} 的健康检查完成，状态: {new_status.value}"
    
    def get_medical_history(self) -> List[dict]:
        """获取医疗记录"""
        return self.__medical_records.copy()
    
    def _is_appropriate_food(self, food_type: str) -> bool:
        """检查食物是否合适 - 受保护方法"""
        meat_foods = ["肉类", "鱼类", "昆虫"]
        plant_foods = ["草料", "水果", "蔬菜", "种子"]
        
        if self.diet_type == DietType.CARNIVORE:
            return food_type in meat_foods
        elif self.diet_type == DietType.HERBIVORE:
            return food_type in plant_foods
        else:  # OMNIVORE
            return food_type in meat_foods + plant_foods
    
    def subscribe_to_events(self, event_type: str, observer: Observer):
        """订阅动物事件"""
        self._event_publisher.subscribe(event_type, observer)
    
    def get_info(self) -> dict:
        """获取动物信息"""
        return {
            "ID": self.animal_id,
            "姓名": self.name,
            "物种": self.species,
            "年龄": self.age,
            "类型": self.animal_type.value,
            "饮食": self.diet_type.value,
            "健康状态": self.health_status.value,
            "体重": f"{self.weight}kg",
            "上次喂食": self._last_fed.strftime("%Y-%m-%d %H:%M") if self._last_fed else "从未",
            "需要喂食": "是" if self.needs_feeding else "否"
        }
    
    def __str__(self):
        return f"{self.species} {self.name} (ID: {self.animal_id})"
    
    def __repr__(self):
        return f"Animal(id='{self.animal_id}', name='{self.name}', species='{self.species}')"


class Mammal(Animal):
    """哺乳动物基类"""
    
    def __init__(self, animal_id: str, name: str, species: str, age: int, 
                 diet_type: DietType, fur_color: str = "棕色"):
        super().__init__(animal_id, name, species, age, AnimalType.MAMMAL, diet_type)
        self.fur_color = fur_color
    
    def groom(self) -> str:
        """梳理毛发"""
        return f"{self.name} 正在梳理 {self.fur_color} 的毛发"


class Bird(Animal):
    """鸟类基类"""
    
    def __init__(self, animal_id: str, name: str, species: str, age: int, 
                 diet_type: DietType, can_fly: bool = True, wingspan: float = 0.0):
        super().__init__(animal_id, name, species, age, AnimalType.BIRD, diet_type)
        self.can_fly = can_fly
        self.wingspan = wingspan
    
    def fly(self) -> str:
        """飞行"""
        if self.can_fly:
            return f"{self.name} 展开 {self.wingspan}m 的翅膀飞翔"
        else:
            return f"{self.name} 不会飞行"


class Reptile(Animal):
    """爬行动物基类"""
    
    def __init__(self, animal_id: str, name: str, species: str, age: int, 
                 diet_type: DietType, is_venomous: bool = False):
        super().__init__(animal_id, name, species, age, AnimalType.REPTILE, diet_type)
        self.is_venomous = is_venomous
    
    def bask_in_sun(self) -> str:
        """晒太阳"""
        return f"{self.name} 正在晒太阳调节体温"


# ============================================================================
# 具体动物类
# ============================================================================

class Lion(Mammal):
    """狮子"""
    
    def __init__(self, animal_id: str, name: str, age: int, is_male: bool = True):
        super().__init__(animal_id, name, "狮子", age, DietType.CARNIVORE, "金黄色")
        self.is_male = is_male
        self.weight = 150.0 + random.uniform(-20, 30)  # 130-180kg
        self._activity_level = ActivityLevel.HIGH
    
    def make_sound(self) -> str:
        return "吼吼吼！"
    
    def get_feeding_interval(self) -> int:
        return 2  # 每2天喂食一次
    
    def get_habitat_requirements(self) -> Dict[str, str]:
        return {
            "气候": "热带草原",
            "温度": "25-35°C",
            "湿度": "30-60%",
            "空间": "大型开放区域",
            "特殊要求": "需要高台和遮阴处"
        }
    
    def roar(self) -> str:
        """咆哮"""
        return f"雄狮 {self.name} 发出震耳欲聋的咆哮声！"
    
    def hunt(self) -> str:
        """狩猎"""
        if self.is_male:
            return f"{self.name} 正在巡视领地"
        else:
            return f"母狮 {self.name} 正在狩猎"


class Elephant(Mammal):
    """大象"""
    
    def __init__(self, animal_id: str, name: str, age: int):
        super().__init__(animal_id, name, "大象", age, DietType.HERBIVORE, "灰色")
        self.weight = 3000.0 + random.uniform(-500, 1000)  # 2500-4000kg
        self._activity_level = ActivityLevel.MEDIUM
    
    def make_sound(self) -> str:
        return "嗷呜～"
    
    def get_feeding_interval(self) -> int:
        return 1  # 每天喂食
    
    def get_habitat_requirements(self) -> Dict[str, str]:
        return {
            "气候": "热带/亚热带",
            "温度": "20-30°C",
            "湿度": "60-80%",
            "空间": "超大型区域",
            "特殊要求": "需要水池和泥浴区"
        }
    
    def spray_water(self) -> str:
        """喷水"""
        return f"{self.name} 用鼻子喷水洗澡"
    
    def trumpet(self) -> str:
        """吹号"""
        return f"{self.name} 高举鼻子发出嘹亮的号声"


class Eagle(Bird):
    """老鹰"""
    
    def __init__(self, animal_id: str, name: str, age: int):
        super().__init__(animal_id, name, "老鹰", age, DietType.CARNIVORE, True, 2.0)
        self.weight = 4.0 + random.uniform(-1, 2)  # 3-6kg
        self._activity_level = ActivityLevel.HIGH
    
    def make_sound(self) -> str:
        return "啾啾啾！"
    
    def get_feeding_interval(self) -> int:
        return 1  # 每天喂食
    
    def get_habitat_requirements(self) -> Dict[str, str]:
        return {
            "气候": "温带/寒带",
            "温度": "10-25°C",
            "湿度": "40-70%",
            "空间": "高空飞行区域",
            "特殊要求": "需要高台筑巢和飞行空间"
        }
    
    def hunt_from_sky(self) -> str:
        """空中狩猎"""
        return f"{self.name} 在高空盘旋寻找猎物"
    
    def dive(self) -> str:
        """俯冲"""
        return f"{self.name} 以极快的速度俯冲而下"


class Penguin(Bird):
    """企鹅"""
    
    def __init__(self, animal_id: str, name: str, age: int):
        super().__init__(animal_id, name, "企鹅", age, DietType.CARNIVORE, False, 0.0)
        self.weight = 15.0 + random.uniform(-5, 10)  # 10-25kg
        self._activity_level = ActivityLevel.MEDIUM
    
    def make_sound(self) -> str:
        return "嘎嘎嘎！"
    
    def get_feeding_interval(self) -> int:
        return 1  # 每天喂食
    
    def get_habitat_requirements(self) -> Dict[str, str]:
        return {
            "气候": "极地",
            "温度": "-10-5°C",
            "湿度": "70-90%",
            "空间": "冰雪环境",
            "特殊要求": "需要游泳池和冰块"
        }
    
    def swim(self) -> str:
        """游泳"""
        return f"{self.name} 在水中优雅地游泳"
    
    def slide_on_ice(self) -> str:
        """滑冰"""
        return f"{self.name} 在冰面上滑行"


class Snake(Reptile):
    """蛇"""
    
    def __init__(self, animal_id: str, name: str, age: int, length: float, is_venomous: bool = False):
        super().__init__(animal_id, name, "蛇", age, DietType.CARNIVORE, is_venomous)
        self.length = length
        self.weight = length * 2.0 + random.uniform(-1, 1)  # 根据长度估算体重
        self._activity_level = ActivityLevel.LOW
    
    def make_sound(self) -> str:
        return "嘶嘶嘶..."
    
    def get_feeding_interval(self) -> int:
        return 7  # 每周喂食一次
    
    def get_habitat_requirements(self) -> Dict[str, str]:
        return {
            "气候": "热带/温带",
            "温度": "25-30°C",
            "湿度": "50-80%",
            "空间": "密闭玻璃环境",
            "特殊要求": "需要加热设备和隐蔽处"
        }
    
    def shed_skin(self) -> str:
        """蜕皮"""
        return f"{self.name} 正在蜕皮"
    
    def coil(self) -> str:
        """盘绕"""
        return f"{self.name} 将 {self.length}m 长的身体盘绕起来"


# ============================================================================
# 栖息地管理
# ============================================================================

class Habitat:
    """栖息地类"""
    
    def __init__(self, habitat_id: str, name: str, habitat_type: str, 
                 capacity: int, area: float):
        self.habitat_id = habitat_id
        self.name = name
        self.habitat_type = habitat_type
        self.capacity = capacity
        self.area = area
        
        # 受保护属性
        self._animals: List[Animal] = []
        self._temperature = 20.0
        self._humidity = 50.0
        self._cleanliness = 100.0
        
        # 私有属性
        self.__maintenance_log = []
        self.__last_cleaned = datetime.now()
    
    @property
    def current_occupancy(self) -> int:
        """当前入住数量"""
        return len(self._animals)
    
    @property
    def occupancy_rate(self) -> float:
        """入住率"""
        return (self.current_occupancy / self.capacity) * 100
    
    @property
    def is_full(self) -> bool:
        """是否已满"""
        return self.current_occupancy >= self.capacity
    
    @property
    def temperature(self) -> float:
        """温度"""
        return self._temperature
    
    @temperature.setter
    def temperature(self, value: float):
        """设置温度"""
        if -50 <= value <= 60:
            self._temperature = value
        else:
            raise ValueError("温度必须在-50°C到60°C之间")
    
    @property
    def humidity(self) -> float:
        """湿度"""
        return self._humidity
    
    @humidity.setter
    def humidity(self, value: float):
        """设置湿度"""
        if 0 <= value <= 100:
            self._humidity = value
        else:
            raise ValueError("湿度必须在0%到100%之间")
    
    @property
    def cleanliness(self) -> float:
        """清洁度"""
        return self._cleanliness
    
    def add_animal(self, animal: Animal) -> bool:
        """添加动物"""
        if self.is_full:
            return False
        
        if animal not in self._animals:
            self._animals.append(animal)
            return True
        return False
    
    def remove_animal(self, animal: Animal) -> bool:
        """移除动物"""
        if animal in self._animals:
            self._animals.remove(animal)
            return True
        return False
    
    def get_animals(self) -> List[Animal]:
        """获取动物列表"""
        return self._animals.copy()
    
    def clean_habitat(self, cleaner_name: str):
        """清洁栖息地"""
        self._cleanliness = 100.0
        self.__last_cleaned = datetime.now()
        
        log_entry = {
            "date": self.__last_cleaned,
            "action": "清洁",
            "staff": cleaner_name,
            "notes": "栖息地已清洁"
        }
        self.__maintenance_log.append(log_entry)
    
    def maintain_habitat(self, staff_name: str, action: str, notes: str = ""):
        """维护栖息地"""
        log_entry = {
            "date": datetime.now(),
            "action": action,
            "staff": staff_name,
            "notes": notes
        }
        self.__maintenance_log.append(log_entry)
    
    def get_maintenance_log(self) -> List[dict]:
        """获取维护日志"""
        return self.__maintenance_log.copy()
    
    def daily_degradation(self):
        """每日环境退化"""
        # 清洁度每天下降
        degradation = self.current_occupancy * 5  # 动物越多，退化越快
        self._cleanliness = max(0, self._cleanliness - degradation)
    
    def get_status(self) -> dict:
        """获取栖息地状态"""
        return {
            "ID": self.habitat_id,
            "名称": self.name,
            "类型": self.habitat_type,
            "容量": f"{self.current_occupancy}/{self.capacity}",
            "入住率": f"{self.occupancy_rate:.1f}%",
            "面积": f"{self.area}平方米",
            "温度": f"{self.temperature}°C",
            "湿度": f"{self.humidity}%",
            "清洁度": f"{self.cleanliness:.1f}%",
            "动物数量": self.current_occupancy
        }
    
    def __str__(self):
        return f"{self.name} ({self.habitat_type}) - {self.current_occupancy}/{self.capacity}"


# ============================================================================
# 员工管理
# ============================================================================

class Staff:
    """员工基类"""
    
    def __init__(self, staff_id: str, name: str, role: StaffRole, 
                 hire_date: datetime = None):
        self.staff_id = staff_id
        self.name = name
        self.role = role
        self.hire_date = hire_date or datetime.now()
        
        # 受保护属性
        self._assigned_areas: Set[str] = set()
        self._work_log = []
        self._is_active = True
    
    @property
    def years_of_service(self) -> float:
        """工作年限"""
        return (datetime.now() - self.hire_date).days / 365.25
    
    @property
    def assigned_areas(self) -> Set[str]:
        """分配的区域"""
        return self._assigned_areas.copy()
    
    def assign_area(self, area_id: str):
        """分配工作区域"""
        self._assigned_areas.add(area_id)
    
    def unassign_area(self, area_id: str):
        """取消分配区域"""
        self._assigned_areas.discard(area_id)
    
    def log_work(self, activity: str, notes: str = ""):
        """记录工作日志"""
        log_entry = {
            "timestamp": datetime.now(),
            "activity": activity,
            "notes": notes
        }
        self._work_log.append(log_entry)
    
    def get_work_log(self, days: int = 7) -> List[dict]:
        """获取工作日志"""
        cutoff_date = datetime.now() - timedelta(days=days)
        return [log for log in self._work_log if log["timestamp"] >= cutoff_date]
    
    def get_info(self) -> dict:
        """获取员工信息"""
        return {
            "ID": self.staff_id,
            "姓名": self.name,
            "职位": self.role.value,
            "入职日期": self.hire_date.strftime("%Y-%m-%d"),
            "工作年限": f"{self.years_of_service:.1f}年",
            "分配区域": list(self._assigned_areas),
            "状态": "在职" if self._is_active else "离职"
        }
    
    def __str__(self):
        return f"{self.role.value} {self.name} (ID: {self.staff_id})"


class ZooKeeper(Staff):
    """饲养员"""
    
    def __init__(self, staff_id: str, name: str, specialization: str = ""):
        super().__init__(staff_id, name, StaffRole.KEEPER)
        self.specialization = specialization  # 专业领域（如"大型哺乳动物"）
    
    def feed_animal(self, animal: Animal, food_type: str, amount: float) -> str:
        """喂食动物"""
        try:
            result = animal.feed(food_type, amount)
            self.log_work(f"喂食 {animal.name}", f"食物: {food_type}, 数量: {amount}kg")
            return result
        except ValueError as e:
            error_msg = f"喂食失败: {str(e)}"
            self.log_work(f"喂食失败 {animal.name}", error_msg)
            return error_msg
    
    def clean_habitat(self, habitat: Habitat) -> str:
        """清洁栖息地"""
        habitat.clean_habitat(self.name)
        self.log_work(f"清洁栖息地 {habitat.name}")
        return f"{self.name} 已清洁 {habitat.name}"
    
    def observe_animal(self, animal: Animal) -> str:
        """观察动物"""
        observation = f"观察 {animal.name}: 健康状态 {animal.health_status.value}"
        if animal.needs_feeding:
            observation += ", 需要喂食"
        
        self.log_work(f"观察 {animal.name}", observation)
        return observation


class Veterinarian(Staff):
    """兽医"""
    
    def __init__(self, staff_id: str, name: str, license_number: str):
        super().__init__(staff_id, name, StaffRole.VETERINARIAN)
        self.license_number = license_number
    
    def examine_animal(self, animal: Animal, notes: str = "") -> str:
        """检查动物"""
        result = animal.medical_checkup(self.name, notes)
        self.log_work(f"检查 {animal.name}", f"结果: {animal.health_status.value}")
        return result
    
    def treat_animal(self, animal: Animal, treatment: str) -> str:
        """治疗动物"""
        # 简化的治疗逻辑
        if animal.health_status in [HealthStatus.POOR, HealthStatus.CRITICAL]:
            # 治疗后状态可能改善
            improvement_chance = random.random()
            if improvement_chance > 0.3:  # 70%的改善机会
                better_statuses = [HealthStatus.FAIR, HealthStatus.GOOD]
                animal.health_status = random.choice(better_statuses)
        
        self.log_work(f"治疗 {animal.name}", f"治疗方案: {treatment}")
        return f"{self.name} 对 {animal.name} 进行了 {treatment} 治疗"


# ============================================================================
# 通知系统
# ============================================================================

class NotificationSystem(Observer):
    """通知系统"""
    
    def __init__(self):
        self._notifications = []
    
    def update(self, event_type: str, data: dict):
        """接收事件通知"""
        notification = {
            "timestamp": datetime.now(),
            "event_type": event_type,
            "data": data
        }
        self._notifications.append(notification)
        
        # 打印重要通知
        if event_type == "health_changed":
            if data["new_status"] in ["较差", "危急"]:
                print(f"🚨 紧急通知: {data['animal_name']} 健康状态变为 {data['new_status']}")
        elif event_type == "animal_fed":
            print(f"🍽️ {data['animal_name']} 已进食 {data['food_type']}")
    
    def get_recent_notifications(self, hours: int = 24) -> List[dict]:
        """获取最近的通知"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [n for n in self._notifications if n["timestamp"] >= cutoff_time]
    
    def get_critical_notifications(self) -> List[dict]:
        """获取紧急通知"""
        critical_events = ["health_changed"]
        return [n for n in self._notifications 
                if n["event_type"] in critical_events 
                and n["data"].get("new_status") in ["较差", "危急"]]


# ============================================================================
# 动物园管理系统
# ============================================================================

class Zoo:
    """动物园管理系统"""
    
    def __init__(self, name: str, location: str):
        self.name = name
        self.location = location
        self.established_date = datetime.now()
        
        # 管理集合
        self._animals: Dict[str, Animal] = {}
        self._habitats: Dict[str, Habitat] = {}
        self._staff: Dict[str, Staff] = {}
        
        # 通知系统
        self._notification_system = NotificationSystem()
        
        # 统计信息
        self._visitor_count = 0
        self._daily_stats = {}
    
    # 动物管理
    def add_animal(self, animal: Animal) -> bool:
        """添加动物"""
        if animal.animal_id not in self._animals:
            self._animals[animal.animal_id] = animal
            # 订阅动物事件
            animal.subscribe_to_events("health_changed", self._notification_system)
            animal.subscribe_to_events("animal_fed", self._notification_system)
            return True
        return False
    
    def remove_animal(self, animal_id: str) -> bool:
        """移除动物"""
        if animal_id in self._animals:
            animal = self._animals[animal_id]
            # 从栖息地移除
            for habitat in self._habitats.values():
                habitat.remove_animal(animal)
            del self._animals[animal_id]
            return True
        return False
    
    def get_animal(self, animal_id: str) -> Optional[Animal]:
        """获取动物"""
        return self._animals.get(animal_id)
    
    def get_all_animals(self) -> List[Animal]:
        """获取所有动物"""
        return list(self._animals.values())
    
    def get_animals_by_type(self, animal_type: AnimalType) -> List[Animal]:
        """按类型获取动物"""
        return [animal for animal in self._animals.values() 
                if animal.animal_type == animal_type]
    
    def get_animals_needing_feeding(self) -> List[Animal]:
        """获取需要喂食的动物"""
        return [animal for animal in self._animals.values() if animal.needs_feeding]
    
    def get_animals_by_health_status(self, status: HealthStatus) -> List[Animal]:
        """按健康状态获取动物"""
        return [animal for animal in self._animals.values() 
                if animal.health_status == status]
    
    # 栖息地管理
    def add_habitat(self, habitat: Habitat) -> bool:
        """添加栖息地"""
        if habitat.habitat_id not in self._habitats:
            self._habitats[habitat.habitat_id] = habitat
            return True
        return False
    
    def get_habitat(self, habitat_id: str) -> Optional[Habitat]:
        """获取栖息地"""
        return self._habitats.get(habitat_id)
    
    def get_all_habitats(self) -> List[Habitat]:
        """获取所有栖息地"""
        return list(self._habitats.values())
    
    def assign_animal_to_habitat(self, animal_id: str, habitat_id: str) -> bool:
        """将动物分配到栖息地"""
        animal = self.get_animal(animal_id)
        habitat = self.get_habitat(habitat_id)
        
        if animal and habitat:
            return habitat.add_animal(animal)
        return False
    
    # 员工管理
    def add_staff(self, staff: Staff) -> bool:
        """添加员工"""
        if staff.staff_id not in self._staff:
            self._staff[staff.staff_id] = staff
            return True
        return False
    
    def get_staff(self, staff_id: str) -> Optional[Staff]:
        """获取员工"""
        return self._staff.get(staff_id)
    
    def get_all_staff(self) -> List[Staff]:
        """获取所有员工"""
        return list(self._staff.values())
    
    def get_staff_by_role(self, role: StaffRole) -> List[Staff]:
        """按角色获取员工"""
        return [staff for staff in self._staff.values() if staff.role == role]
    
    # 日常运营
    def daily_routine(self):
        """每日例行工作"""
        print(f"\n🌅 {self.name} 开始新的一天 ({datetime.now().strftime('%Y-%m-%d')})")
        
        # 栖息地环境退化
        for habitat in self._habitats.values():
            habitat.daily_degradation()
        
        # 检查需要喂食的动物
        animals_needing_feeding = self.get_animals_needing_feeding()
        if animals_needing_feeding:
            print(f"📋 今日需要喂食的动物: {len(animals_needing_feeding)}只")
            for animal in animals_needing_feeding:
                print(f"   - {animal.name} ({animal.species})")
        
        # 检查健康状况不佳的动物
        sick_animals = self.get_animals_by_health_status(HealthStatus.POOR) + \
                      self.get_animals_by_health_status(HealthStatus.CRITICAL)
        if sick_animals:
            print(f"🏥 需要医疗关注的动物: {len(sick_animals)}只")
            for animal in sick_animals:
                print(f"   - {animal.name} ({animal.health_status.value})")
        
        # 检查清洁度低的栖息地
        dirty_habitats = [h for h in self._habitats.values() if h.cleanliness < 50]
        if dirty_habitats:
            print(f"🧹 需要清洁的栖息地: {len(dirty_habitats)}个")
            for habitat in dirty_habitats:
                print(f"   - {habitat.name} (清洁度: {habitat.cleanliness:.1f}%)")
    
    def generate_daily_report(self) -> dict:
        """生成每日报告"""
        total_animals = len(self._animals)
        total_habitats = len(self._habitats)
        total_staff = len(self._staff)
        
        animals_by_health = {}
        for status in HealthStatus:
            count = len(self.get_animals_by_health_status(status))
            animals_by_health[status.value] = count
        
        animals_needing_feeding = len(self.get_animals_needing_feeding())
        
        habitat_occupancy = []
        for habitat in self._habitats.values():
            habitat_occupancy.append({
                "name": habitat.name,
                "occupancy_rate": habitat.occupancy_rate,
                "cleanliness": habitat.cleanliness
            })
        
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "zoo_name": self.name,
            "total_animals": total_animals,
            "total_habitats": total_habitats,
            "total_staff": total_staff,
            "animals_by_health": animals_by_health,
            "animals_needing_feeding": animals_needing_feeding,
            "habitat_status": habitat_occupancy,
            "recent_notifications": len(self._notification_system.get_recent_notifications()),
            "critical_notifications": len(self._notification_system.get_critical_notifications())
        }
    
    def get_zoo_statistics(self) -> dict:
        """获取动物园统计信息"""
        animals_by_type = {}
        for animal_type in AnimalType:
            count = len(self.get_animals_by_type(animal_type))
            animals_by_type[animal_type.value] = count
        
        staff_by_role = {}
        for role in StaffRole:
            count = len(self.get_staff_by_role(role))
            staff_by_role[role.value] = count
        
        avg_habitat_occupancy = sum(h.occupancy_rate for h in self._habitats.values()) / len(self._habitats) if self._habitats else 0
        avg_habitat_cleanliness = sum(h.cleanliness for h in self._habitats.values()) / len(self._habitats) if self._habitats else 0
        
        return {
            "动物园名称": self.name,
            "位置": self.location,
            "成立日期": self.established_date.strftime("%Y-%m-%d"),
            "总动物数": len(self._animals),
            "按类型分布": animals_by_type,
            "总栖息地数": len(self._habitats),
            "平均入住率": f"{avg_habitat_occupancy:.1f}%",
            "平均清洁度": f"{avg_habitat_cleanliness:.1f}%",
            "总员工数": len(self._staff),
            "员工分布": staff_by_role
        }
    
    def __str__(self):
        return f"{self.name} 动物园 (位于 {self.location})"


# ============================================================================
# 演示函数
# ============================================================================

def create_sample_zoo() -> Zoo:
    """创建示例动物园"""
    # 创建动物园
    zoo = Zoo("Python野生动物园", "北京市")
    
    # 创建栖息地
    savanna = Habitat("H001", "非洲草原", "草原", 5, 1000.0)
    savanna.temperature = 28.0
    savanna.humidity = 45.0
    
    arctic = Habitat("H002", "极地世界", "极地", 3, 500.0)
    arctic.temperature = -2.0
    arctic.humidity = 80.0
    
    rainforest = Habitat("H003", "热带雨林", "雨林", 4, 800.0)
    rainforest.temperature = 26.0
    rainforest.humidity = 85.0
    
    reptile_house = Habitat("H004", "爬行动物馆", "室内", 6, 200.0)
    reptile_house.temperature = 28.0
    reptile_house.humidity = 60.0
    
    # 添加栖息地到动物园
    zoo.add_habitat(savanna)
    zoo.add_habitat(arctic)
    zoo.add_habitat(rainforest)
    zoo.add_habitat(reptile_house)
    
    # 创建动物
    lion1 = Lion("A001", "辛巴", 5, True)
    lion2 = Lion("A002", "娜娜", 4, False)
    elephant1 = Elephant("A003", "大象艾莉", 12)
    eagle1 = Eagle("A004", "金雕阿波罗", 3)
    penguin1 = Penguin("A005", "企鹅波波", 2)
    penguin2 = Penguin("A006", "企鹅琪琪", 1)
    snake1 = Snake("A007", "蟒蛇小青", 4, 3.5, False)
    
    # 添加动物到动物园
    animals = [lion1, lion2, elephant1, eagle1, penguin1, penguin2, snake1]
    for animal in animals:
        zoo.add_animal(animal)
    
    # 分配动物到栖息地
    zoo.assign_animal_to_habitat("A001", "H001")  # 辛巴到草原
    zoo.assign_animal_to_habitat("A002", "H001")  # 娜娜到草原
    zoo.assign_animal_to_habitat("A003", "H001")  # 大象到草原
    zoo.assign_animal_to_habitat("A004", "H003")  # 老鹰到雨林
    zoo.assign_animal_to_habitat("A005", "H002")  # 企鹅到极地
    zoo.assign_animal_to_habitat("A006", "H002")  # 企鹅到极地
    zoo.assign_animal_to_habitat("A007", "H004")  # 蛇到爬行动物馆
    
    # 创建员工
    keeper1 = ZooKeeper("S001", "张三", "大型哺乳动物")
    keeper2 = ZooKeeper("S002", "李四", "鸟类")
    keeper3 = ZooKeeper("S003", "王五", "爬行动物")
    vet1 = Veterinarian("S004", "赵医生", "VET2024001")
    
    # 添加员工到动物园
    staff_members = [keeper1, keeper2, keeper3, vet1]
    for staff in staff_members:
        zoo.add_staff(staff)
    
    # 分配工作区域
    keeper1.assign_area("H001")  # 张三负责草原
    keeper2.assign_area("H002")  # 李四负责极地
    keeper2.assign_area("H003")  # 李四也负责雨林（鸟类）
    keeper3.assign_area("H004")  # 王五负责爬行动物馆
    
    return zoo


def demonstrate_zoo_operations(zoo: Zoo):
    """演示动物园操作"""
    print(f"\n🎪 欢迎来到 {zoo}")
    print("=" * 60)
    
    # 显示动物园统计
    stats = zoo.get_zoo_statistics()
    print("\n📊 动物园统计信息:")
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for sub_key, sub_value in value.items():
                print(f"    - {sub_key}: {sub_value}")
        else:
            print(f"  {key}: {value}")
    
    # 显示所有动物
    print("\n🐾 动物园动物列表:")
    for animal in zoo.get_all_animals():
        print(f"  {animal} - 健康状态: {animal.health_status.value}")
        print(f"    栖息地要求: {animal.get_habitat_requirements()}")
        print(f"    声音: {animal.make_sound()}")
        
        # 展示特殊行为
        if isinstance(animal, Lion):
            print(f"    特殊行为: {animal.roar()}")
        elif isinstance(animal, Elephant):
            print(f"    特殊行为: {animal.spray_water()}")
        elif isinstance(animal, Eagle):
            print(f"    特殊行为: {animal.hunt_from_sky()}")
        elif isinstance(animal, Penguin):
            print(f"    特殊行为: {animal.swim()}")
        elif isinstance(animal, Snake):
            print(f"    特殊行为: {animal.coil()}")
        print()
    
    # 显示栖息地状态
    print("\n🏠 栖息地状态:")
    for habitat in zoo.get_all_habitats():
        print(f"  {habitat}")
        status = habitat.get_status()
        for key, value in status.items():
            if key != "ID":
                print(f"    {key}: {value}")
        print()
    
    # 显示员工信息
    print("\n👥 员工信息:")
    for staff in zoo.get_all_staff():
        print(f"  {staff}")
        info = staff.get_info()
        for key, value in info.items():
            if key not in ["ID", "姓名"]:
                print(f"    {key}: {value}")
        print()


def demonstrate_daily_operations(zoo: Zoo):
    """演示日常操作"""
    print("\n🌅 开始日常操作演示")
    print("=" * 60)
    
    # 获取员工
    keepers = zoo.get_staff_by_role(StaffRole.KEEPER)
    vet = zoo.get_staff_by_role(StaffRole.VETERINARIAN)[0]
    
    # 喂食操作
    print("\n🍽️ 喂食时间:")
    animals = zoo.get_all_animals()
    
    for i, animal in enumerate(animals[:3]):  # 只演示前3只动物
        keeper = keepers[i % len(keepers)]
        
        # 根据动物类型选择食物
        if animal.diet_type == DietType.CARNIVORE:
            food = "肉类"
        elif animal.diet_type == DietType.HERBIVORE:
            food = "草料"
        else:
            food = "水果"
        
        amount = random.uniform(1.0, 5.0)
        result = keeper.feed_animal(animal, food, amount)
        print(f"  {result}")
    
    # 清洁栖息地
    print("\n🧹 清洁栖息地:")
    habitats = zoo.get_all_habitats()
    for i, habitat in enumerate(habitats[:2]):  # 只演示前2个栖息地
        keeper = keepers[i % len(keepers)]
        result = keeper.clean_habitat(habitat)
        print(f"  {result}")
    
    # 医疗检查
    print("\n🏥 医疗检查:")
    for animal in animals[:2]:  # 只检查前2只动物
        result = vet.examine_animal(animal, "定期检查")
        print(f"  {result}")
        
        # 如果健康状况不佳，进行治疗
        if animal.health_status in [HealthStatus.POOR, HealthStatus.CRITICAL]:
            treatment_result = vet.treat_animal(animal, "药物治疗")
            print(f"    {treatment_result}")
    
    # 动物观察
    print("\n👀 动物观察:")
    for animal in animals[:3]:
        keeper = keepers[0]  # 使用第一个饲养员
        observation = keeper.observe_animal(animal)
        print(f"  {observation}")


def demonstrate_event_system(zoo: Zoo):
    """演示事件系统"""
    print("\n📢 事件系统演示")
    print("=" * 60)
    
    # 获取一些动物进行演示
    animals = zoo.get_all_animals()[:3]
    
    # 模拟一些事件
    print("\n模拟健康状态变化:")
    for animal in animals:
        # 随机改变健康状态
        old_status = animal.health_status
        new_status = random.choice(list(HealthStatus))
        animal.health_status = new_status
        print(f"  {animal.name}: {old_status.value} → {new_status.value}")
    
    # 显示通知
    print("\n📋 最近的通知:")
    notifications = zoo._notification_system.get_recent_notifications()
    for notification in notifications[-5:]:  # 显示最近5条
        timestamp = notification["timestamp"].strftime("%H:%M:%S")
        event_type = notification["event_type"]
        data = notification["data"]
        print(f"  [{timestamp}] {event_type}: {data}")
    
    # 显示紧急通知
    critical_notifications = zoo._notification_system.get_critical_notifications()
    if critical_notifications:
        print("\n🚨 紧急通知:")
        for notification in critical_notifications:
            timestamp = notification["timestamp"].strftime("%H:%M:%S")
            data = notification["data"]
            print(f"  [{timestamp}] {data['animal_name']} 健康状态: {data['new_status']}")


def main():
    """主函数"""
    print("Session09 项目: 动物园管理系统")
    print("=" * 60)
    print("这是一个综合性的面向对象编程项目，展示了:")
    print("• 继承和多态的实际应用")
    print("• 抽象基类的设计")
    print("• 封装和访问控制")
    print("• 组合关系的使用")
    print("• 观察者模式的应用")
    
    # 创建示例动物园
    zoo = create_sample_zoo()
    
    # 演示基本功能
    demonstrate_zoo_operations(zoo)
    
    # 演示日常操作
    demonstrate_daily_operations(zoo)
    
    # 演示事件系统
    demonstrate_event_system(zoo)
    
    # 执行每日例行工作
    zoo.daily_routine()
    
    # 生成每日报告
    print("\n📊 每日报告:")
    daily_report = zoo.generate_daily_report()
    for key, value in daily_report.items():
        if isinstance(value, (dict, list)):
            print(f"  {key}: {len(value) if isinstance(value, list) else value}")
        else:
            print(f"  {key}: {value}")
    
    print("\n🎯 项目要点总结:")
    print("   1. 抽象基类定义了动物的通用接口")
    print("   2. 继承实现了代码复用和扩展")
    print("   3. 多态允许统一处理不同类型的动物")
    print("   4. 封装保护了对象的内部状态")
    print("   5. 组合关系实现了复杂的业务逻辑")
    print("   6. 观察者模式实现了事件通知系统")
    print("   7. 枚举提高了代码的可读性和维护性")
    
    print("\n✨ 恭喜！您已经完成了面向对象进阶的学习！")


if __name__ == "__main__":
    main()