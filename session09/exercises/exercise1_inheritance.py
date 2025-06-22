#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session09 练习1: 继承练习

练习目标：
1. 理解继承的基本概念
2. 掌握方法重写和super()的使用
3. 实现多层继承
4. 理解方法解析顺序(MRO)

作者: Python教程团队
创建日期: 2024-01-09
"""

# ============================================================================
# 练习1: 基础继承 - 员工管理系统
# ============================================================================

class Employee:
    """员工基类
    
    TODO: 实现员工基类，包含以下功能：
    1. 初始化方法：接收员工ID、姓名、基本工资
    2. 计算工资方法：返回基本工资
    3. 获取员工信息方法：返回员工基本信息
    4. 字符串表示方法
    """
    
    def __init__(self, employee_id, name, base_salary):
        # TODO: 初始化员工属性
        pass
    
    def calculate_salary(self):
        """计算工资 - 基类返回基本工资"""
        # TODO: 返回基本工资
        pass
    
    def get_info(self):
        """获取员工信息"""
        # TODO: 返回包含员工ID、姓名、职位、工资的字典
        pass
    
    def __str__(self):
        # TODO: 返回员工的字符串表示
        pass


class Manager(Employee):
    """经理类
    
    TODO: 继承Employee类，添加以下功能：
    1. 初始化方法：除了基本信息外，还有管理奖金
    2. 重写计算工资方法：基本工资 + 管理奖金
    3. 添加管理团队的方法
    """
    
    def __init__(self, employee_id, name, base_salary, management_bonus):
        # TODO: 调用父类初始化，并设置管理奖金
        pass
    
    def calculate_salary(self):
        """重写工资计算 - 包含管理奖金"""
        # TODO: 返回基本工资 + 管理奖金
        pass
    
    def manage_team(self, team_members):
        """管理团队"""
        # TODO: 实现团队管理功能
        pass


class Developer(Employee):
    """开发者类
    
    TODO: 继承Employee类，添加以下功能：
    1. 初始化方法：除了基本信息外，还有编程语言技能
    2. 重写计算工资方法：根据技能数量给予技能奖金
    3. 添加编程相关方法
    """
    
    def __init__(self, employee_id, name, base_salary, programming_languages):
        # TODO: 调用父类初始化，并设置编程语言列表
        pass
    
    def calculate_salary(self):
        """重写工资计算 - 包含技能奖金"""
        # TODO: 基本工资 + (技能数量 * 500)的技能奖金
        pass
    
    def add_skill(self, language):
        """添加编程技能"""
        # TODO: 添加新的编程语言技能
        pass
    
    def write_code(self, project_name):
        """编写代码"""
        # TODO: 实现编程功能
        pass


class SeniorDeveloper(Developer):
    """高级开发者类
    
    TODO: 继承Developer类，添加以下功能：
    1. 初始化方法：除了开发者信息外，还有项目经验年数
    2. 重写计算工资方法：在开发者工资基础上加经验奖金
    3. 添加指导新人的方法
    """
    
    def __init__(self, employee_id, name, base_salary, programming_languages, years_experience):
        # TODO: 调用父类初始化，并设置经验年数
        pass
    
    def calculate_salary(self):
        """重写工资计算 - 包含经验奖金"""
        # TODO: 开发者工资 + (经验年数 * 1000)的经验奖金
        pass
    
    def mentor_junior(self, junior_developer):
        """指导新人"""
        # TODO: 实现指导功能
        pass
    
    def lead_project(self, project_name):
        """领导项目"""
        # TODO: 实现项目领导功能
        pass


# ============================================================================
# 练习2: 多重继承 - 技能混合
# ============================================================================

class Communicator:
    """沟通技能混入类
    
    TODO: 实现沟通相关的方法
    """
    
    def __init__(self):
        self.communication_level = "基础"
    
    def conduct_meeting(self, topic):
        """主持会议"""
        # TODO: 实现会议主持功能
        pass
    
    def give_presentation(self, topic):
        """做演示"""
        # TODO: 实现演示功能
        pass


class Analyst:
    """分析技能混入类
    
    TODO: 实现分析相关的方法
    """
    
    def __init__(self):
        self.analysis_tools = ["Excel", "SQL"]
    
    def analyze_data(self, data_source):
        """分析数据"""
        # TODO: 实现数据分析功能
        pass
    
    def create_report(self, analysis_result):
        """创建报告"""
        # TODO: 实现报告创建功能
        pass


class ProductManager(Manager, Communicator, Analyst):
    """产品经理类
    
    TODO: 继承Manager、Communicator、Analyst，实现产品管理功能
    注意：需要正确处理多重继承的初始化
    """
    
    def __init__(self, employee_id, name, base_salary, management_bonus):
        # TODO: 正确初始化所有父类
        # 提示：使用super()和显式调用
        pass
    
    def plan_product(self, product_name):
        """产品规划"""
        # TODO: 实现产品规划功能
        pass
    
    def coordinate_teams(self, dev_team, design_team):
        """协调团队"""
        # TODO: 实现团队协调功能
        pass


# ============================================================================
# 测试函数
# ============================================================================

def test_basic_inheritance():
    """测试基础继承"""
    print("=== 测试基础继承 ===")
    
    # TODO: 创建不同类型的员工实例
    # employee = Employee("E001", "张三", 5000)
    # manager = Manager("M001", "李四", 8000, 2000)
    # developer = Developer("D001", "王五", 7000, ["Python", "Java"])
    # senior_dev = SeniorDeveloper("S001", "赵六", 9000, ["Python", "Java", "Go"], 5)
    
    # TODO: 测试各种方法
    # print(employee)
    # print(f"工资: {employee.calculate_salary()}")
    # print(f"信息: {employee.get_info()}")
    
    pass


def test_method_resolution_order():
    """测试方法解析顺序"""
    print("\n=== 测试方法解析顺序 ===")
    
    # TODO: 创建ProductManager实例并测试MRO
    # pm = ProductManager("PM001", "产品经理", 10000, 3000)
    # print(f"ProductManager的MRO: {ProductManager.__mro__}")
    
    pass


def test_polymorphism():
    """测试多态性"""
    print("\n=== 测试多态性 ===")
    
    # TODO: 创建员工列表，测试多态调用
    # employees = [
    #     Employee("E001", "普通员工", 5000),
    #     Manager("M001", "经理", 8000, 2000),
    #     Developer("D001", "开发者", 7000, ["Python"]),
    #     SeniorDeveloper("S001", "高级开发者", 9000, ["Python", "Java"], 3)
    # ]
    
    # TODO: 遍历员工列表，调用相同方法名但不同实现
    # for emp in employees:
    #     print(f"{emp} - 工资: {emp.calculate_salary()}")
    
    pass


def main():
    """主函数 - 运行所有测试"""
    print("Session09 练习1: 继承练习")
    print("=" * 50)
    
    test_basic_inheritance()
    test_method_resolution_order()
    test_polymorphism()
    
    print("\n💡 练习要点:")
    print("   1. 使用super()调用父类方法")
    print("   2. 正确重写父类方法")
    print("   3. 理解多重继承的MRO")
    print("   4. 实现多态性")
    print("   5. 合理设计类的层次结构")
    
    print("\n🎯 完成练习后，请运行测试函数验证实现")


if __name__ == "__main__":
    main()


# ============================================================================
# 练习提示和参考答案
# ============================================================================

"""
💡 实现提示：

1. Employee类实现：
   - __init__: 保存employee_id, name, base_salary
   - calculate_salary: 返回base_salary
   - get_info: 返回包含所有信息的字典
   - __str__: 返回格式化的员工信息

2. Manager类实现：
   - __init__: super().__init__() + management_bonus
   - calculate_salary: super().calculate_salary() + management_bonus
   - manage_team: 打印管理信息

3. Developer类实现：
   - __init__: super().__init__() + programming_languages列表
   - calculate_salary: super().calculate_salary() + len(programming_languages) * 500
   - add_skill: 添加到programming_languages列表
   - write_code: 打印编程信息

4. SeniorDeveloper类实现：
   - __init__: super().__init__() + years_experience
   - calculate_salary: super().calculate_salary() + years_experience * 1000
   - mentor_junior: 打印指导信息
   - lead_project: 打印项目领导信息

5. 多重继承注意事项：
   - 使用super().__init__()处理继承链
   - 了解MRO的工作原理
   - 避免钻石继承问题

🔍 测试要点：
   - 验证每个类的功能是否正确
   - 检查继承关系是否合理
   - 测试多态性是否工作
   - 确认MRO顺序是否符合预期
"""