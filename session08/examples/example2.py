#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session08 示例2：类变量和实例变量

本示例演示了：
- 类变量的定义和使用
- 实例变量的定义和使用
- 类变量和实例变量的区别
- 类方法和静态方法的使用
"""


class Employee:
    """员工类 - 演示类变量和实例变量的使用"""
    
    # 类变量
    company_name = "Python科技有限公司"
    employee_count = 0
    base_salary = 5000
    departments = ["技术部", "产品部", "市场部", "人事部", "财务部"]
    
    def __init__(self, name, position, department, salary_multiplier=1.0):
        """构造函数"""
        # 实例变量
        self.name = name
        self.position = position
        self.department = department
        self.salary_multiplier = salary_multiplier
        self.hire_date = "2024-01-08"  # 简化处理
        self.performance_score = 0
        
        # 每创建一个员工，员工总数加1
        Employee.employee_count += 1
        self.employee_id = f"EMP{Employee.employee_count:04d}"
    
    def get_salary(self):
        """计算实际薪资"""
        return Employee.base_salary * self.salary_multiplier
    
    def update_performance(self, score):
        """更新绩效分数"""
        if 0 <= score <= 100:
            self.performance_score = score
            print(f"{self.name}的绩效分数已更新为：{score}")
        else:
            print("绩效分数必须在0-100之间")
    
    def get_employee_info(self):
        """获取员工信息"""
        return (
            f"员工ID：{self.employee_id}\n"
            f"姓名：{self.name}\n"
            f"职位：{self.position}\n"
            f"部门：{self.department}\n"
            f"薪资：{self.get_salary():.2f}元\n"
            f"绩效分数：{self.performance_score}\n"
            f"入职日期：{self.hire_date}"
        )
    
    def promote(self, new_position, new_multiplier):
        """升职"""
        old_position = self.position
        old_salary = self.get_salary()
        
        self.position = new_position
        self.salary_multiplier = new_multiplier
        
        new_salary = self.get_salary()
        print(f"🎉 恭喜{self.name}升职！")
        print(f"职位：{old_position} -> {new_position}")
        print(f"薪资：{old_salary:.2f}元 -> {new_salary:.2f}元")
    
    @classmethod
    def get_company_info(cls):
        """获取公司信息（类方法）"""
        return (
            f"公司名称：{cls.company_name}\n"
            f"员工总数：{cls.employee_count}人\n"
            f"基础薪资：{cls.base_salary}元\n"
            f"部门列表：{', '.join(cls.departments)}"
        )
    
    @classmethod
    def set_base_salary(cls, new_base_salary):
        """设置基础薪资（类方法）"""
        old_salary = cls.base_salary
        cls.base_salary = new_base_salary
        print(f"基础薪资已调整：{old_salary}元 -> {new_base_salary}元")
    
    @staticmethod
    def is_valid_department(department):
        """验证部门是否有效（静态方法）"""
        return department in Employee.departments
    
    @staticmethod
    def calculate_annual_salary(monthly_salary, months=12, bonus_months=1):
        """计算年薪（静态方法）"""
        return monthly_salary * (months + bonus_months)
    
    def __str__(self):
        """字符串表示"""
        return f"{self.name}（{self.employee_id}）- {self.position}"
    
    def __repr__(self):
        """开发者字符串表示"""
        return f"Employee('{self.name}', '{self.position}', '{self.department}', {self.salary_multiplier})"


class Manager(Employee):
    """经理类 - 继承自员工类"""
    
    def __init__(self, name, department, team_size=0):
        """经理构造函数"""
        super().__init__(name, "经理", department, 2.0)  # 经理薪资倍数为2.0
        self.team_size = team_size
        self.team_members = []
    
    def add_team_member(self, employee):
        """添加团队成员"""
        if isinstance(employee, Employee) and employee not in self.team_members:
            self.team_members.append(employee)
            self.team_size = len(self.team_members)
            print(f"{employee.name}已加入{self.name}的团队")
        else:
            print("无法添加团队成员")
    
    def get_team_info(self):
        """获取团队信息"""
        if self.team_members:
            members = [member.name for member in self.team_members]
            return f"{self.name}的团队（{self.team_size}人）：{', '.join(members)}"
        else:
            return f"{self.name}暂无团队成员"


def main():
    """主函数"""
    print("示例2：类变量和实例变量")
    print("=" * 40)
    
    # 显示初始公司信息
    print("1. 初始公司信息：")
    print(Employee.get_company_info())
    
    # 创建员工对象
    print("\n2. 创建员工：")
    emp1 = Employee("张三", "初级程序员", "技术部", 1.2)
    emp2 = Employee("李四", "UI设计师", "产品部", 1.1)
    emp3 = Employee("王五", "市场专员", "市场部", 1.0)
    
    print(f"创建了{Employee.employee_count}名员工")
    
    # 显示员工信息
    print("\n3. 员工信息：")
    employees = [emp1, emp2, emp3]
    for emp in employees:
        print(f"\n{emp}")
        print("-" * 30)
        print(emp.get_employee_info())
    
    # 更新绩效
    print("\n4. 更新绩效：")
    emp1.update_performance(95)
    emp2.update_performance(88)
    emp3.update_performance(92)
    
    # 升职
    print("\n5. 升职操作：")
    emp1.promote("高级程序员", 1.5)
    
    # 调整基础薪资（影响所有员工）
    print("\n6. 调整基础薪资：")
    Employee.set_base_salary(5500)
    
    print("\n调整后的薪资：")
    for emp in employees:
        print(f"{emp.name}：{emp.get_salary():.2f}元")
    
    # 创建经理
    print("\n7. 创建经理：")
    manager = Manager("赵六", "技术部")
    print(f"\n{manager}")
    print("-" * 30)
    print(manager.get_employee_info())
    
    # 组建团队
    print("\n8. 组建团队：")
    manager.add_team_member(emp1)
    manager.add_team_member(emp2)
    print(manager.get_team_info())
    
    # 使用静态方法
    print("\n9. 静态方法使用：")
    print(f"'技术部'是有效部门吗？{Employee.is_valid_department('技术部')}")
    print(f"'销售部'是有效部门吗？{Employee.is_valid_department('销售部')}")
    
    annual_salary = Employee.calculate_annual_salary(emp1.get_salary())
    print(f"{emp1.name}的年薪：{annual_salary:.2f}元")
    
    # 最终公司信息
    print("\n10. 最终公司信息：")
    print(Employee.get_company_info())
    
    # 演示类变量和实例变量的区别
    print("\n11. 类变量vs实例变量：")
    print(f"通过类访问公司名称：{Employee.company_name}")
    print(f"通过实例访问公司名称：{emp1.company_name}")
    print(f"通过实例访问公司名称：{manager.company_name}")
    
    # 修改类变量
    Employee.company_name = "新Python科技有限公司"
    print(f"\n修改类变量后：")
    print(f"通过类访问：{Employee.company_name}")
    print(f"通过emp1访问：{emp1.company_name}")
    print(f"通过manager访问：{manager.company_name}")
    
    # 修改实例的"类变量"（实际上创建了实例变量）
    emp1.company_name = "emp1的专属公司"
    print(f"\n修改emp1的company_name后：")
    print(f"通过类访问：{Employee.company_name}")
    print(f"通过emp1访问：{emp1.company_name}")
    print(f"通过emp2访问：{emp2.company_name}")


if __name__ == "__main__":
    main()