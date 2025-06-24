#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session26: 项目需求分析与设计 - 演示代码

本文件演示了需求分析工具的基本用法和实际应用，包括：
1. 需求收集工具
2. 用例分析工具
3. 系统设计工具
4. 项目计划工具

作者: Python教程团队
创建日期: 2024-01-15
最后修改: 2024-01-15
"""

import json
import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class Priority(Enum):
    """需求优先级枚举"""
    LOW = "低"
    MEDIUM = "中"
    HIGH = "高"
    CRITICAL = "紧急"


class RequirementType(Enum):
    """需求类型枚举"""
    FUNCTIONAL = "功能性需求"
    NON_FUNCTIONAL = "非功能性需求"
    CONSTRAINT = "约束条件"


class RequirementStatus(Enum):
    """需求状态枚举"""
    DRAFT = "草稿"
    REVIEW = "评审中"
    APPROVED = "已批准"
    IMPLEMENTED = "已实现"
    TESTED = "已测试"
    REJECTED = "已拒绝"


@dataclass
class Requirement:
    """需求类"""
    id: str
    title: str
    description: str
    type: RequirementType
    priority: Priority
    status: RequirementStatus
    stakeholder: str
    created_date: str
    updated_date: str
    acceptance_criteria: List[str]
    dependencies: List[str]
    estimated_effort: int  # 人天


@dataclass
class UseCase:
    """用例类"""
    id: str
    name: str
    actor: str
    description: str
    preconditions: List[str]
    postconditions: List[str]
    main_flow: List[str]
    alternative_flows: Dict[str, List[str]]
    business_rules: List[str]


@dataclass
class SystemComponent:
    """系统组件类"""
    name: str
    type: str  # service, database, interface
    description: str
    responsibilities: List[str]
    interfaces: List[str]
    dependencies: List[str]


class RequirementAnalyzer:
    """需求分析器"""
    
    def __init__(self):
        self.requirements: List[Requirement] = []
        self.use_cases: List[UseCase] = []
        self.system_components: List[SystemComponent] = []
    
    def add_requirement(self, requirement: Requirement) -> None:
        """添加需求"""
        self.requirements.append(requirement)
        print(f"✅ 已添加需求: {requirement.title}")
    
    def get_requirements_by_priority(self, priority: Priority) -> List[Requirement]:
        """按优先级获取需求"""
        return [req for req in self.requirements if req.priority == priority]
    
    def get_requirements_by_status(self, status: RequirementStatus) -> List[Requirement]:
        """按状态获取需求"""
        return [req for req in self.requirements if req.status == status]
    
    def analyze_requirement_coverage(self) -> Dict[str, int]:
        """分析需求覆盖情况"""
        total = len(self.requirements)
        if total == 0:
            return {"总需求数": 0}
        
        status_count = {}
        for status in RequirementStatus:
            count = len(self.get_requirements_by_status(status))
            status_count[status.value] = count
        
        status_count["总需求数"] = total
        status_count["完成率"] = round(
            (status_count.get(RequirementStatus.IMPLEMENTED.value, 0) + 
             status_count.get(RequirementStatus.TESTED.value, 0)) / total * 100, 2
        )
        
        return status_count
    
    def estimate_total_effort(self) -> int:
        """估算总工作量"""
        return sum(req.estimated_effort for req in self.requirements)
    
    def generate_requirement_report(self) -> str:
        """生成需求报告"""
        report = ["\n" + "="*50]
        report.append("需求分析报告")
        report.append("="*50)
        
        # 需求统计
        coverage = self.analyze_requirement_coverage()
        report.append(f"\n📊 需求统计:")
        for key, value in coverage.items():
            if key == "完成率":
                report.append(f"   {key}: {value}%")
            else:
                report.append(f"   {key}: {value}")
        
        # 优先级分布
        report.append(f"\n🎯 优先级分布:")
        for priority in Priority:
            count = len(self.get_requirements_by_priority(priority))
            report.append(f"   {priority.value}: {count}个")
        
        # 工作量估算
        total_effort = self.estimate_total_effort()
        report.append(f"\n⏱️ 工作量估算: {total_effort}人天")
        
        # 详细需求列表
        report.append(f"\n📋 需求详情:")
        for req in self.requirements:
            report.append(f"\n   [{req.id}] {req.title}")
            report.append(f"   类型: {req.type.value} | 优先级: {req.priority.value} | 状态: {req.status.value}")
            report.append(f"   描述: {req.description}")
            report.append(f"   工作量: {req.estimated_effort}人天")
        
        return "\n".join(report)


class UseCaseAnalyzer:
    """用例分析器"""
    
    def __init__(self):
        self.use_cases: List[UseCase] = []
    
    def add_use_case(self, use_case: UseCase) -> None:
        """添加用例"""
        self.use_cases.append(use_case)
        print(f"✅ 已添加用例: {use_case.name}")
    
    def get_use_cases_by_actor(self, actor: str) -> List[UseCase]:
        """按参与者获取用例"""
        return [uc for uc in self.use_cases if uc.actor == actor]
    
    def generate_use_case_diagram_data(self) -> Dict[str, List[str]]:
        """生成用例图数据"""
        actors = {}
        for uc in self.use_cases:
            if uc.actor not in actors:
                actors[uc.actor] = []
            actors[uc.actor].append(uc.name)
        return actors
    
    def generate_use_case_report(self) -> str:
        """生成用例报告"""
        report = ["\n" + "="*50]
        report.append("用例分析报告")
        report.append("="*50)
        
        # 用例统计
        report.append(f"\n📊 用例统计:")
        report.append(f"   总用例数: {len(self.use_cases)}")
        
        # 参与者分析
        actors_data = self.generate_use_case_diagram_data()
        report.append(f"\n👥 参与者分析:")
        for actor, use_cases in actors_data.items():
            report.append(f"   {actor}: {len(use_cases)}个用例")
        
        # 详细用例列表
        report.append(f"\n📋 用例详情:")
        for uc in self.use_cases:
            report.append(f"\n   [{uc.id}] {uc.name}")
            report.append(f"   参与者: {uc.actor}")
            report.append(f"   描述: {uc.description}")
            report.append(f"   主要流程步骤: {len(uc.main_flow)}步")
            report.append(f"   异常流程: {len(uc.alternative_flows)}个")
        
        return "\n".join(report)


class SystemArchitectureDesigner:
    """系统架构设计器"""
    
    def __init__(self):
        self.components: List[SystemComponent] = []
    
    def add_component(self, component: SystemComponent) -> None:
        """添加系统组件"""
        self.components.append(component)
        print(f"✅ 已添加组件: {component.name}")
    
    def get_components_by_type(self, component_type: str) -> List[SystemComponent]:
        """按类型获取组件"""
        return [comp for comp in self.components if comp.type == component_type]
    
    def analyze_dependencies(self) -> Dict[str, List[str]]:
        """分析组件依赖关系"""
        dependencies = {}
        for comp in self.components:
            dependencies[comp.name] = comp.dependencies
        return dependencies
    
    def generate_architecture_report(self) -> str:
        """生成架构报告"""
        report = ["\n" + "="*50]
        report.append("系统架构设计报告")
        report.append("="*50)
        
        # 组件统计
        report.append(f"\n📊 组件统计:")
        report.append(f"   总组件数: {len(self.components)}")
        
        # 按类型分组
        component_types = {}
        for comp in self.components:
            if comp.type not in component_types:
                component_types[comp.type] = []
            component_types[comp.type].append(comp.name)
        
        report.append(f"\n🏗️ 组件分类:")
        for comp_type, components in component_types.items():
            report.append(f"   {comp_type}: {len(components)}个")
            for comp_name in components:
                report.append(f"     - {comp_name}")
        
        # 依赖关系分析
        dependencies = self.analyze_dependencies()
        report.append(f"\n🔗 依赖关系:")
        for comp_name, deps in dependencies.items():
            if deps:
                report.append(f"   {comp_name} 依赖于: {', '.join(deps)}")
        
        return "\n".join(report)


class ProjectPlanner:
    """项目计划器"""
    
    def __init__(self):
        self.tasks = []
        self.milestones = []
        self.resources = []
    
    def add_task(self, task_id: str, name: str, duration: int, 
                 dependencies: List[str] = None, resources: List[str] = None) -> None:
        """添加任务"""
        task = {
            "id": task_id,
            "name": name,
            "duration": duration,
            "dependencies": dependencies or [],
            "resources": resources or [],
            "start_date": None,
            "end_date": None
        }
        self.tasks.append(task)
        print(f"✅ 已添加任务: {name}")
    
    def add_milestone(self, milestone_id: str, name: str, date: str) -> None:
        """添加里程碑"""
        milestone = {
            "id": milestone_id,
            "name": name,
            "date": date
        }
        self.milestones.append(milestone)
        print(f"✅ 已添加里程碑: {name}")
    
    def calculate_critical_path(self) -> List[str]:
        """计算关键路径（简化版）"""
        # 这里是一个简化的关键路径计算
        # 实际项目中需要使用更复杂的算法
        task_durations = {task["id"]: task["duration"] for task in self.tasks}
        
        # 找出最长路径作为关键路径
        max_duration = 0
        critical_path = []
        
        for task in self.tasks:
            if not task["dependencies"]:
                path_duration = task["duration"]
                path = [task["id"]]
                
                if path_duration > max_duration:
                    max_duration = path_duration
                    critical_path = path
        
        return critical_path
    
    def estimate_project_duration(self) -> int:
        """估算项目总工期"""
        if not self.tasks:
            return 0
        
        # 简化计算：假设任务可以并行执行
        max_duration = max(task["duration"] for task in self.tasks)
        return max_duration
    
    def generate_project_plan_report(self) -> str:
        """生成项目计划报告"""
        report = ["\n" + "="*50]
        report.append("项目计划报告")
        report.append("="*50)
        
        # 项目统计
        total_tasks = len(self.tasks)
        total_duration = sum(task["duration"] for task in self.tasks)
        estimated_duration = self.estimate_project_duration()
        
        report.append(f"\n📊 项目统计:")
        report.append(f"   总任务数: {total_tasks}")
        report.append(f"   总工作量: {total_duration}人天")
        report.append(f"   预计工期: {estimated_duration}天")
        
        # 里程碑
        if self.milestones:
            report.append(f"\n🎯 项目里程碑:")
            for milestone in self.milestones:
                report.append(f"   {milestone['date']}: {milestone['name']}")
        
        # 关键路径
        critical_path = self.calculate_critical_path()
        if critical_path:
            report.append(f"\n🔥 关键路径:")
            report.append(f"   {' -> '.join(critical_path)}")
        
        # 任务列表
        report.append(f"\n📋 任务详情:")
        for task in self.tasks:
            report.append(f"\n   [{task['id']}] {task['name']}")
            report.append(f"   工期: {task['duration']}天")
            if task["dependencies"]:
                report.append(f"   依赖: {', '.join(task['dependencies'])}")
            if task["resources"]:
                report.append(f"   资源: {', '.join(task['resources'])}")
        
        return "\n".join(report)


def demo_requirement_analysis():
    """演示需求分析功能"""
    print("\n" + "="*60)
    print("🔍 需求分析演示")
    print("="*60)
    
    analyzer = RequirementAnalyzer()
    
    # 添加示例需求
    requirements = [
        Requirement(
            id="REQ-001",
            title="用户注册功能",
            description="用户可以通过邮箱和手机号注册账号",
            type=RequirementType.FUNCTIONAL,
            priority=Priority.HIGH,
            status=RequirementStatus.APPROVED,
            stakeholder="产品经理",
            created_date="2024-01-01",
            updated_date="2024-01-05",
            acceptance_criteria=[
                "支持邮箱注册",
                "支持手机号注册",
                "密码强度验证",
                "邮箱/手机验证"
            ],
            dependencies=[],
            estimated_effort=3
        ),
        Requirement(
            id="REQ-002",
            title="商品搜索功能",
            description="用户可以通过关键词搜索商品",
            type=RequirementType.FUNCTIONAL,
            priority=Priority.HIGH,
            status=RequirementStatus.IMPLEMENTED,
            stakeholder="用户",
            created_date="2024-01-02",
            updated_date="2024-01-10",
            acceptance_criteria=[
                "支持关键词搜索",
                "支持分类筛选",
                "支持价格排序",
                "搜索结果分页"
            ],
            dependencies=["REQ-001"],
            estimated_effort=5
        ),
        Requirement(
            id="REQ-003",
            title="系统响应时间",
            description="页面响应时间不超过2秒",
            type=RequirementType.NON_FUNCTIONAL,
            priority=Priority.MEDIUM,
            status=RequirementStatus.REVIEW,
            stakeholder="技术负责人",
            created_date="2024-01-03",
            updated_date="2024-01-03",
            acceptance_criteria=[
                "首页加载时间<2秒",
                "搜索响应时间<1秒",
                "商品详情页加载<2秒"
            ],
            dependencies=[],
            estimated_effort=8
        )
    ]
    
    for req in requirements:
        analyzer.add_requirement(req)
    
    # 生成并显示报告
    print(analyzer.generate_requirement_report())


def demo_use_case_analysis():
    """演示用例分析功能"""
    print("\n" + "="*60)
    print("📝 用例分析演示")
    print("="*60)
    
    uc_analyzer = UseCaseAnalyzer()
    
    # 添加示例用例
    use_cases = [
        UseCase(
            id="UC-001",
            name="用户登录",
            actor="顾客",
            description="用户通过用户名和密码登录系统",
            preconditions=["用户已注册账号", "用户记得登录凭据"],
            postconditions=["用户成功登录", "系统创建用户会话"],
            main_flow=[
                "1. 用户访问登录页面",
                "2. 用户输入用户名和密码",
                "3. 系统验证用户凭据",
                "4. 系统创建用户会话",
                "5. 系统跳转到用户主页"
            ],
            alternative_flows={
                "3a. 用户名或密码错误": [
                    "3a1. 系统显示错误信息",
                    "3a2. 返回步骤2"
                ],
                "3b. 账号被锁定": [
                    "3b1. 系统显示账号锁定信息",
                    "3b2. 提供账号解锁方式"
                ]
            },
            business_rules=[
                "密码错误3次后锁定账号",
                "会话超时时间为30分钟"
            ]
        ),
        UseCase(
            id="UC-002",
            name="商品搜索",
            actor="顾客",
            description="用户搜索感兴趣的商品",
            preconditions=["用户已访问网站"],
            postconditions=["显示搜索结果"],
            main_flow=[
                "1. 用户在搜索框输入关键词",
                "2. 用户点击搜索按钮",
                "3. 系统查询商品数据库",
                "4. 系统返回搜索结果",
                "5. 系统显示商品列表"
            ],
            alternative_flows={
                "4a. 没有找到匹配商品": [
                    "4a1. 系统显示'无搜索结果'信息",
                    "4a2. 系统提供搜索建议"
                ]
            },
            business_rules=[
                "搜索结果按相关性排序",
                "每页显示20个商品"
            ]
        )
    ]
    
    for uc in use_cases:
        uc_analyzer.add_use_case(uc)
    
    # 生成并显示报告
    print(uc_analyzer.generate_use_case_report())


def demo_system_architecture():
    """演示系统架构设计功能"""
    print("\n" + "="*60)
    print("🏗️ 系统架构设计演示")
    print("="*60)
    
    arch_designer = SystemArchitectureDesigner()
    
    # 添加系统组件
    components = [
        SystemComponent(
            name="用户服务",
            type="service",
            description="处理用户注册、登录、个人信息管理",
            responsibilities=[
                "用户注册",
                "用户认证",
                "个人信息管理",
                "权限控制"
            ],
            interfaces=[
                "POST /api/users/register",
                "POST /api/users/login",
                "GET /api/users/profile",
                "PUT /api/users/profile"
            ],
            dependencies=["用户数据库", "Redis缓存"]
        ),
        SystemComponent(
            name="商品服务",
            type="service",
            description="处理商品管理、搜索、分类",
            responsibilities=[
                "商品信息管理",
                "商品搜索",
                "分类管理",
                "库存管理"
            ],
            interfaces=[
                "GET /api/products",
                "GET /api/products/{id}",
                "POST /api/products/search",
                "GET /api/categories"
            ],
            dependencies=["商品数据库", "搜索引擎"]
        ),
        SystemComponent(
            name="订单服务",
            type="service",
            description="处理订单创建、支付、物流",
            responsibilities=[
                "订单创建",
                "订单状态管理",
                "支付处理",
                "物流跟踪"
            ],
            interfaces=[
                "POST /api/orders",
                "GET /api/orders/{id}",
                "PUT /api/orders/{id}/status",
                "POST /api/orders/{id}/payment"
            ],
            dependencies=["订单数据库", "支付网关", "用户服务"]
        ),
        SystemComponent(
            name="用户数据库",
            type="database",
            description="存储用户相关数据",
            responsibilities=[
                "用户基本信息存储",
                "用户认证信息存储",
                "用户权限数据存储"
            ],
            interfaces=["SQL接口"],
            dependencies=[]
        ),
        SystemComponent(
            name="API网关",
            type="interface",
            description="统一API入口，处理路由、认证、限流",
            responsibilities=[
                "请求路由",
                "身份认证",
                "请求限流",
                "API监控"
            ],
            interfaces=["HTTP/HTTPS接口"],
            dependencies=["用户服务", "商品服务", "订单服务"]
        )
    ]
    
    for comp in components:
        arch_designer.add_component(comp)
    
    # 生成并显示报告
    print(arch_designer.generate_architecture_report())


def demo_project_planning():
    """演示项目计划功能"""
    print("\n" + "="*60)
    print("📅 项目计划演示")
    print("="*60)
    
    planner = ProjectPlanner()
    
    # 添加项目任务
    tasks = [
        ("T001", "需求分析", 5, [], ["产品经理", "业务分析师"]),
        ("T002", "系统设计", 8, ["T001"], ["架构师", "技术负责人"]),
        ("T003", "数据库设计", 3, ["T002"], ["数据库工程师"]),
        ("T004", "用户服务开发", 10, ["T002"], ["后端工程师A"]),
        ("T005", "商品服务开发", 12, ["T002"], ["后端工程师B"]),
        ("T006", "订单服务开发", 15, ["T004"], ["后端工程师C"]),
        ("T007", "前端页面开发", 20, ["T002"], ["前端工程师"]),
        ("T008", "系统集成测试", 8, ["T004", "T005", "T006", "T007"], ["测试工程师"]),
        ("T009", "用户验收测试", 5, ["T008"], ["产品经理", "测试工程师"]),
        ("T010", "系统部署", 3, ["T009"], ["运维工程师"])
    ]
    
    for task_id, name, duration, deps, resources in tasks:
        planner.add_task(task_id, name, duration, deps, resources)
    
    # 添加里程碑
    milestones = [
        ("M001", "需求分析完成", "2024-02-01"),
        ("M002", "系统设计完成", "2024-02-15"),
        ("M003", "核心功能开发完成", "2024-03-15"),
        ("M004", "系统测试完成", "2024-03-30"),
        ("M005", "项目上线", "2024-04-05")
    ]
    
    for milestone_id, name, date in milestones:
        planner.add_milestone(milestone_id, name, date)
    
    # 生成并显示报告
    print(planner.generate_project_plan_report())


def main():
    """主函数：演示需求分析与设计工具"""
    print("Session26: 项目需求分析与设计演示")
    print("=" * 60)
    print("本演示展示了软件项目需求分析与设计的完整流程：")
    print("1. 需求收集与分析")
    print("2. 用例建模")
    print("3. 系统架构设计")
    print("4. 项目计划制定")
    print("\n让我们开始演示...")
    
    try:
        # 演示需求分析
        demo_requirement_analysis()
        
        # 演示用例分析
        demo_use_case_analysis()
        
        # 演示系统架构设计
        demo_system_architecture()
        
        # 演示项目计划
        demo_project_planning()
        
        print("\n" + "="*60)
        print("🎉 演示完成！")
        print("="*60)
        print("\n通过本演示，你学会了：")
        print("✅ 如何进行系统化的需求分析")
        print("✅ 如何建立用例模型")
        print("✅ 如何设计系统架构")
        print("✅ 如何制定项目计划")
        print("\n这些技能是成为项目负责人的重要基础！")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        print("请检查代码并重试。")


if __name__ == "__main__":
    main()