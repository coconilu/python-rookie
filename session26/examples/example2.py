#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session26 示例2: 用例分析与系统架构设计

本示例演示了：
1. 用例图建模
2. 用例详细描述
3. 系统架构设计
4. 组件关系分析

作者: Python教程团队
创建日期: 2024-01-15
"""

import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


class ActorType(Enum):
    """参与者类型"""
    PRIMARY = "主要参与者"
    SECONDARY = "次要参与者"
    SYSTEM = "系统参与者"


class UseCasePriority(Enum):
    """用例优先级"""
    HIGH = "高"
    MEDIUM = "中"
    LOW = "低"


class UseCaseComplexity(Enum):
    """用例复杂度"""
    SIMPLE = "简单"
    MEDIUM = "中等"
    COMPLEX = "复杂"


class Actor:
    """参与者类"""
    
    def __init__(self, name: str, actor_type: ActorType, description: str):
        self.name = name
        self.actor_type = actor_type
        self.description = description
        self.responsibilities = []
        self.use_cases = []
    
    def add_responsibility(self, responsibility: str):
        """添加职责"""
        self.responsibilities.append(responsibility)
    
    def add_use_case(self, use_case_name: str):
        """关联用例"""
        if use_case_name not in self.use_cases:
            self.use_cases.append(use_case_name)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "name": self.name,
            "type": self.actor_type.value,
            "description": self.description,
            "responsibilities": self.responsibilities,
            "use_cases": self.use_cases
        }


class UseCase:
    """用例类"""
    
    def __init__(self, name: str, description: str, priority: UseCasePriority, 
                 complexity: UseCaseComplexity):
        self.name = name
        self.description = description
        self.priority = priority
        self.complexity = complexity
        self.actors = []
        self.preconditions = []
        self.postconditions = []
        self.main_flow = []
        self.alternative_flows = []
        self.exception_flows = []
        self.business_rules = []
        self.non_functional_requirements = []
        self.estimated_effort = 0  # 人天
    
    def add_actor(self, actor_name: str):
        """添加参与者"""
        if actor_name not in self.actors:
            self.actors.append(actor_name)
    
    def add_precondition(self, condition: str):
        """添加前置条件"""
        self.preconditions.append(condition)
    
    def add_postcondition(self, condition: str):
        """添加后置条件"""
        self.postconditions.append(condition)
    
    def add_main_flow_step(self, step: str):
        """添加主流程步骤"""
        step_number = len(self.main_flow) + 1
        self.main_flow.append(f"{step_number}. {step}")
    
    def add_alternative_flow(self, condition: str, steps: List[str]):
        """添加备选流程"""
        self.alternative_flows.append({
            "condition": condition,
            "steps": steps
        })
    
    def add_exception_flow(self, exception: str, handling: str):
        """添加异常流程"""
        self.exception_flows.append({
            "exception": exception,
            "handling": handling
        })
    
    def add_business_rule(self, rule: str):
        """添加业务规则"""
        self.business_rules.append(rule)
    
    def add_nfr(self, requirement: str):
        """添加非功能性需求"""
        self.non_functional_requirements.append(requirement)
    
    def set_estimated_effort(self, effort: int):
        """设置预估工作量"""
        self.estimated_effort = effort
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "name": self.name,
            "description": self.description,
            "priority": self.priority.value,
            "complexity": self.complexity.value,
            "actors": self.actors,
            "preconditions": self.preconditions,
            "postconditions": self.postconditions,
            "main_flow": self.main_flow,
            "alternative_flows": self.alternative_flows,
            "exception_flows": self.exception_flows,
            "business_rules": self.business_rules,
            "non_functional_requirements": self.non_functional_requirements,
            "estimated_effort": self.estimated_effort
        }


class SystemComponent:
    """系统组件类"""
    
    def __init__(self, name: str, component_type: str, description: str):
        self.name = name
        self.component_type = component_type  # 如：Controller, Service, Repository等
        self.description = description
        self.responsibilities = []
        self.dependencies = []
        self.interfaces = []
        self.technologies = []
    
    def add_responsibility(self, responsibility: str):
        """添加职责"""
        self.responsibilities.append(responsibility)
    
    def add_dependency(self, component_name: str):
        """添加依赖"""
        if component_name not in self.dependencies:
            self.dependencies.append(component_name)
    
    def add_interface(self, interface: str):
        """添加接口"""
        self.interfaces.append(interface)
    
    def add_technology(self, technology: str):
        """添加技术栈"""
        if technology not in self.technologies:
            self.technologies.append(technology)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "name": self.name,
            "type": self.component_type,
            "description": self.description,
            "responsibilities": self.responsibilities,
            "dependencies": self.dependencies,
            "interfaces": self.interfaces,
            "technologies": self.technologies
        }


class SystemArchitecture:
    """系统架构类"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.layers = []
        self.components = {}
        self.patterns = []
        self.quality_attributes = []
        self.constraints = []
    
    def add_layer(self, layer_name: str, description: str):
        """添加架构层"""
        self.layers.append({
            "name": layer_name,
            "description": description,
            "components": []
        })
    
    def add_component_to_layer(self, layer_name: str, component: SystemComponent):
        """将组件添加到指定层"""
        self.components[component.name] = component
        
        for layer in self.layers:
            if layer["name"] == layer_name:
                layer["components"].append(component.name)
                break
    
    def add_pattern(self, pattern_name: str, description: str):
        """添加架构模式"""
        self.patterns.append({
            "name": pattern_name,
            "description": description
        })
    
    def add_quality_attribute(self, attribute: str, description: str, measures: List[str]):
        """添加质量属性"""
        self.quality_attributes.append({
            "attribute": attribute,
            "description": description,
            "measures": measures
        })
    
    def add_constraint(self, constraint: str):
        """添加约束"""
        self.constraints.append(constraint)
    
    def analyze_dependencies(self) -> Dict[str, Any]:
        """分析组件依赖关系"""
        dependency_graph = {}
        circular_dependencies = []
        
        for component_name, component in self.components.items():
            dependency_graph[component_name] = component.dependencies
        
        # 简单的循环依赖检测
        for component_name in dependency_graph:
            visited = set()
            stack = [component_name]
            
            while stack:
                current = stack.pop()
                if current in visited:
                    circular_dependencies.append(f"循环依赖: {component_name} -> {current}")
                    break
                visited.add(current)
                
                if current in dependency_graph:
                    stack.extend(dependency_graph[current])
        
        return {
            "dependency_graph": dependency_graph,
            "circular_dependencies": list(set(circular_dependencies)),
            "component_count": len(self.components),
            "total_dependencies": sum(len(deps) for deps in dependency_graph.values())
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "name": self.name,
            "description": self.description,
            "layers": self.layers,
            "components": {name: comp.to_dict() for name, comp in self.components.items()},
            "patterns": self.patterns,
            "quality_attributes": self.quality_attributes,
            "constraints": self.constraints
        }


class UseCaseAnalyzer:
    """用例分析器"""
    
    def __init__(self):
        self.actors = {}
        self.use_cases = {}
        self.relationships = []
    
    def add_actor(self, actor: Actor):
        """添加参与者"""
        self.actors[actor.name] = actor
    
    def add_use_case(self, use_case: UseCase):
        """添加用例"""
        self.use_cases[use_case.name] = use_case
        
        # 建立参与者和用例的关系
        for actor_name in use_case.actors:
            if actor_name in self.actors:
                self.actors[actor_name].add_use_case(use_case.name)
    
    def add_relationship(self, from_use_case: str, to_use_case: str, 
                        relationship_type: str):
        """添加用例关系"""
        self.relationships.append({
            "from": from_use_case,
            "to": to_use_case,
            "type": relationship_type  # include, extend, generalization
        })
    
    def analyze_use_cases(self) -> Dict[str, Any]:
        """分析用例"""
        analysis = {
            "total_use_cases": len(self.use_cases),
            "total_actors": len(self.actors),
            "priority_distribution": {},
            "complexity_distribution": {},
            "effort_estimation": {},
            "actor_involvement": {},
            "relationships": self.relationships
        }
        
        # 统计优先级分布
        for use_case in self.use_cases.values():
            priority = use_case.priority.value
            analysis["priority_distribution"][priority] = \
                analysis["priority_distribution"].get(priority, 0) + 1
        
        # 统计复杂度分布
        for use_case in self.use_cases.values():
            complexity = use_case.complexity.value
            analysis["complexity_distribution"][complexity] = \
                analysis["complexity_distribution"].get(complexity, 0) + 1
        
        # 工作量估算
        total_effort = sum(uc.estimated_effort for uc in self.use_cases.values())
        analysis["effort_estimation"] = {
            "total_effort": total_effort,
            "average_effort": total_effort / len(self.use_cases) if self.use_cases else 0,
            "by_priority": {}
        }
        
        # 按优先级统计工作量
        for priority in UseCasePriority:
            priority_effort = sum(
                uc.estimated_effort for uc in self.use_cases.values() 
                if uc.priority == priority
            )
            analysis["effort_estimation"]["by_priority"][priority.value] = priority_effort
        
        # 参与者参与度
        for actor_name, actor in self.actors.items():
            analysis["actor_involvement"][actor_name] = {
                "type": actor.actor_type.value,
                "use_case_count": len(actor.use_cases),
                "use_cases": actor.use_cases
            }
        
        return analysis
    
    def generate_use_case_document(self, use_case_name: str) -> str:
        """生成用例文档"""
        if use_case_name not in self.use_cases:
            return f"用例 '{use_case_name}' 不存在"
        
        use_case = self.use_cases[use_case_name]
        
        doc = f"""
用例文档
========

用例名称: {use_case.name}
用例描述: {use_case.description}
优先级: {use_case.priority.value}
复杂度: {use_case.complexity.value}
预估工作量: {use_case.estimated_effort} 人天

参与者
------
{chr(10).join(f"- {actor}" for actor in use_case.actors)}

前置条件
--------
{chr(10).join(f"- {condition}" for condition in use_case.preconditions)}

后置条件
--------
{chr(10).join(f"- {condition}" for condition in use_case.postconditions)}

主流程
------
{chr(10).join(use_case.main_flow)}
"""
        
        if use_case.alternative_flows:
            doc += "\n备选流程\n--------\n"
            for i, alt_flow in enumerate(use_case.alternative_flows, 1):
                doc += f"\n{i}. 条件: {alt_flow['condition']}\n"
                doc += "\n".join(f"   {step}" for step in alt_flow['steps'])
                doc += "\n"
        
        if use_case.exception_flows:
            doc += "\n异常流程\n--------\n"
            for i, exc_flow in enumerate(use_case.exception_flows, 1):
                doc += f"{i}. 异常: {exc_flow['exception']}\n"
                doc += f"   处理: {exc_flow['handling']}\n\n"
        
        if use_case.business_rules:
            doc += "\n业务规则\n--------\n"
            doc += "\n".join(f"- {rule}" for rule in use_case.business_rules)
            doc += "\n"
        
        if use_case.non_functional_requirements:
            doc += "\n非功能性需求\n------------\n"
            doc += "\n".join(f"- {nfr}" for nfr in use_case.non_functional_requirements)
            doc += "\n"
        
        return doc


def create_ecommerce_use_case_model():
    """创建电商系统用例模型"""
    print("\n" + "="*60)
    print("🎭 创建电商系统用例模型")
    print("="*60)
    
    analyzer = UseCaseAnalyzer()
    
    # 创建参与者
    customer = Actor("顾客", ActorType.PRIMARY, "购买商品的用户")
    customer.add_responsibility("浏览商品")
    customer.add_responsibility("下单购买")
    customer.add_responsibility("管理个人信息")
    
    admin = Actor("管理员", ActorType.PRIMARY, "系统管理人员")
    admin.add_responsibility("管理商品")
    admin.add_responsibility("处理订单")
    admin.add_responsibility("用户管理")
    
    payment_system = Actor("支付系统", ActorType.SYSTEM, "第三方支付服务")
    payment_system.add_responsibility("处理支付")
    payment_system.add_responsibility("支付状态通知")
    
    logistics_system = Actor("物流系统", ActorType.SYSTEM, "物流配送服务")
    logistics_system.add_responsibility("配送商品")
    logistics_system.add_responsibility("物流状态更新")
    
    # 添加参与者到分析器
    for actor in [customer, admin, payment_system, logistics_system]:
        analyzer.add_actor(actor)
    
    # 创建用例
    use_cases_data = [
        {
            "name": "用户注册",
            "description": "新用户创建账户",
            "priority": UseCasePriority.HIGH,
            "complexity": UseCaseComplexity.SIMPLE,
            "actors": ["顾客"],
            "effort": 3
        },
        {
            "name": "用户登录",
            "description": "用户身份验证",
            "priority": UseCasePriority.HIGH,
            "complexity": UseCaseComplexity.SIMPLE,
            "actors": ["顾客", "管理员"],
            "effort": 2
        },
        {
            "name": "浏览商品",
            "description": "查看商品列表和详情",
            "priority": UseCasePriority.HIGH,
            "complexity": UseCaseComplexity.MEDIUM,
            "actors": ["顾客"],
            "effort": 5
        },
        {
            "name": "搜索商品",
            "description": "根据关键词搜索商品",
            "priority": UseCasePriority.HIGH,
            "complexity": UseCaseComplexity.MEDIUM,
            "actors": ["顾客"],
            "effort": 8
        },
        {
            "name": "管理购物车",
            "description": "添加、删除、修改购物车商品",
            "priority": UseCasePriority.HIGH,
            "complexity": UseCaseComplexity.MEDIUM,
            "actors": ["顾客"],
            "effort": 6
        },
        {
            "name": "下单购买",
            "description": "创建订单并完成购买",
            "priority": UseCasePriority.HIGH,
            "complexity": UseCaseComplexity.COMPLEX,
            "actors": ["顾客", "支付系统"],
            "effort": 12
        },
        {
            "name": "管理商品",
            "description": "添加、编辑、删除商品",
            "priority": UseCasePriority.HIGH,
            "complexity": UseCaseComplexity.MEDIUM,
            "actors": ["管理员"],
            "effort": 8
        },
        {
            "name": "订单管理",
            "description": "查看和处理订单",
            "priority": UseCasePriority.HIGH,
            "complexity": UseCaseComplexity.COMPLEX,
            "actors": ["管理员", "物流系统"],
            "effort": 10
        },
        {
            "name": "用户评价",
            "description": "对购买的商品进行评价",
            "priority": UseCasePriority.MEDIUM,
            "complexity": UseCaseComplexity.SIMPLE,
            "actors": ["顾客"],
            "effort": 4
        },
        {
            "name": "推荐系统",
            "description": "基于用户行为推荐商品",
            "priority": UseCasePriority.LOW,
            "complexity": UseCaseComplexity.COMPLEX,
            "actors": ["顾客"],
            "effort": 20
        }
    ]
    
    # 创建详细用例
    for uc_data in use_cases_data:
        use_case = UseCase(
            uc_data["name"],
            uc_data["description"],
            uc_data["priority"],
            uc_data["complexity"]
        )
        
        for actor_name in uc_data["actors"]:
            use_case.add_actor(actor_name)
        
        use_case.set_estimated_effort(uc_data["effort"])
        
        # 为关键用例添加详细信息
        if use_case.name == "下单购买":
            use_case.add_precondition("用户已登录")
            use_case.add_precondition("购物车中有商品")
            use_case.add_precondition("用户有有效的收货地址")
            
            use_case.add_postcondition("订单创建成功")
            use_case.add_postcondition("库存数量更新")
            use_case.add_postcondition("支付流程启动")
            
            use_case.add_main_flow_step("用户点击结算")
            use_case.add_main_flow_step("系统显示订单确认页面")
            use_case.add_main_flow_step("用户确认收货地址")
            use_case.add_main_flow_step("用户选择支付方式")
            use_case.add_main_flow_step("用户确认订单")
            use_case.add_main_flow_step("系统创建订单")
            use_case.add_main_flow_step("系统跳转到支付页面")
            use_case.add_main_flow_step("用户完成支付")
            use_case.add_main_flow_step("系统确认支付成功")
            
            use_case.add_alternative_flow(
                "用户选择货到付款",
                ["跳过在线支付步骤", "直接创建订单", "等待配送"]
            )
            
            use_case.add_exception_flow(
                "支付失败",
                "显示错误信息，允许用户重新支付或选择其他支付方式"
            )
            
            use_case.add_exception_flow(
                "库存不足",
                "提示用户库存不足，建议减少数量或选择其他商品"
            )
            
            use_case.add_business_rule("单笔订单金额不能超过10000元")
            use_case.add_business_rule("每个用户每天最多下10个订单")
            
            use_case.add_nfr("订单创建响应时间不超过3秒")
            use_case.add_nfr("支持1000个并发下单")
        
        analyzer.add_use_case(use_case)
    
    # 添加用例关系
    analyzer.add_relationship("下单购买", "用户登录", "include")
    analyzer.add_relationship("下单购买", "管理购物车", "include")
    analyzer.add_relationship("搜索商品", "浏览商品", "extend")
    
    return analyzer


def create_system_architecture():
    """创建系统架构"""
    print("\n" + "="*60)
    print("🏗️ 创建系统架构设计")
    print("="*60)
    
    # 创建系统架构
    architecture = SystemArchitecture(
        "电商系统架构",
        "基于微服务的分层架构设计"
    )
    
    # 定义架构层
    architecture.add_layer("表现层", "用户界面和API接口")
    architecture.add_layer("业务层", "业务逻辑处理")
    architecture.add_layer("数据访问层", "数据持久化")
    architecture.add_layer("基础设施层", "基础服务和中间件")
    
    # 创建组件
    components_data = [
        # 表现层组件
        {
            "name": "Web前端",
            "type": "UI组件",
            "layer": "表现层",
            "description": "用户Web界面",
            "responsibilities": ["用户交互", "数据展示", "表单验证"],
            "technologies": ["React", "TypeScript", "Ant Design"],
            "interfaces": ["/api/products", "/api/orders", "/api/users"]
        },
        {
            "name": "移动端App",
            "type": "UI组件",
            "layer": "表现层",
            "description": "移动应用界面",
            "responsibilities": ["移动端交互", "推送通知", "离线缓存"],
            "technologies": ["React Native", "Redux"],
            "interfaces": ["/api/products", "/api/orders", "/api/users"]
        },
        {
            "name": "API网关",
            "type": "网关组件",
            "layer": "表现层",
            "description": "统一API入口",
            "responsibilities": ["路由转发", "认证授权", "限流熔断"],
            "technologies": ["Spring Cloud Gateway", "Redis"],
            "interfaces": ["/api/*"]
        },
        
        # 业务层组件
        {
            "name": "用户服务",
            "type": "微服务",
            "layer": "业务层",
            "description": "用户管理服务",
            "responsibilities": ["用户注册", "用户认证", "用户信息管理"],
            "technologies": ["Spring Boot", "JWT", "BCrypt"],
            "interfaces": ["/users", "/auth"]
        },
        {
            "name": "商品服务",
            "type": "微服务",
            "layer": "业务层",
            "description": "商品管理服务",
            "responsibilities": ["商品CRUD", "库存管理", "商品搜索"],
            "technologies": ["Spring Boot", "Elasticsearch"],
            "interfaces": ["/products", "/inventory"]
        },
        {
            "name": "订单服务",
            "type": "微服务",
            "layer": "业务层",
            "description": "订单处理服务",
            "responsibilities": ["订单创建", "订单状态管理", "订单查询"],
            "technologies": ["Spring Boot", "RabbitMQ"],
            "interfaces": ["/orders"]
        },
        {
            "name": "支付服务",
            "type": "微服务",
            "layer": "业务层",
            "description": "支付处理服务",
            "responsibilities": ["支付处理", "退款处理", "支付状态查询"],
            "technologies": ["Spring Boot", "支付宝SDK", "微信支付SDK"],
            "interfaces": ["/payments"]
        },
        
        # 数据访问层组件
        {
            "name": "用户数据访问",
            "type": "Repository",
            "layer": "数据访问层",
            "description": "用户数据持久化",
            "responsibilities": ["用户数据CRUD", "数据缓存"],
            "technologies": ["MyBatis", "MySQL", "Redis"],
            "interfaces": ["UserRepository"]
        },
        {
            "name": "商品数据访问",
            "type": "Repository",
            "layer": "数据访问层",
            "description": "商品数据持久化",
            "responsibilities": ["商品数据CRUD", "搜索索引"],
            "technologies": ["MyBatis", "MySQL", "Elasticsearch"],
            "interfaces": ["ProductRepository"]
        },
        {
            "name": "订单数据访问",
            "type": "Repository",
            "layer": "数据访问层",
            "description": "订单数据持久化",
            "responsibilities": ["订单数据CRUD", "事务管理"],
            "technologies": ["MyBatis", "MySQL"],
            "interfaces": ["OrderRepository"]
        },
        
        # 基础设施层组件
        {
            "name": "配置中心",
            "type": "基础服务",
            "layer": "基础设施层",
            "description": "统一配置管理",
            "responsibilities": ["配置管理", "配置热更新"],
            "technologies": ["Spring Cloud Config", "Git"],
            "interfaces": ["/config"]
        },
        {
            "name": "服务注册中心",
            "type": "基础服务",
            "layer": "基础设施层",
            "description": "服务发现和注册",
            "responsibilities": ["服务注册", "服务发现", "健康检查"],
            "technologies": ["Eureka", "Consul"],
            "interfaces": ["/eureka"]
        },
        {
            "name": "监控系统",
            "type": "基础服务",
            "layer": "基础设施层",
            "description": "系统监控和告警",
            "responsibilities": ["性能监控", "日志收集", "告警通知"],
            "technologies": ["Prometheus", "Grafana", "ELK"],
            "interfaces": ["/metrics", "/logs"]
        }
    ]
    
    # 创建组件并添加到架构
    for comp_data in components_data:
        component = SystemComponent(
            comp_data["name"],
            comp_data["type"],
            comp_data["description"]
        )
        
        for responsibility in comp_data["responsibilities"]:
            component.add_responsibility(responsibility)
        
        for technology in comp_data["technologies"]:
            component.add_technology(technology)
        
        for interface in comp_data["interfaces"]:
            component.add_interface(interface)
        
        architecture.add_component_to_layer(comp_data["layer"], component)
    
    # 添加组件依赖关系
    dependencies = [
        ("Web前端", "API网关"),
        ("移动端App", "API网关"),
        ("API网关", "用户服务"),
        ("API网关", "商品服务"),
        ("API网关", "订单服务"),
        ("订单服务", "支付服务"),
        ("订单服务", "商品服务"),
        ("用户服务", "用户数据访问"),
        ("商品服务", "商品数据访问"),
        ("订单服务", "订单数据访问"),
        ("用户服务", "配置中心"),
        ("商品服务", "配置中心"),
        ("订单服务", "配置中心"),
        ("支付服务", "配置中心"),
        ("用户服务", "服务注册中心"),
        ("商品服务", "服务注册中心"),
        ("订单服务", "服务注册中心"),
        ("支付服务", "服务注册中心")
    ]
    
    for from_comp, to_comp in dependencies:
        if from_comp in architecture.components:
            architecture.components[from_comp].add_dependency(to_comp)
    
    # 添加架构模式
    architecture.add_pattern(
        "微服务架构",
        "将系统拆分为多个独立的微服务，每个服务负责特定的业务功能"
    )
    architecture.add_pattern(
        "分层架构",
        "将系统分为表现层、业务层、数据访问层和基础设施层"
    )
    architecture.add_pattern(
        "API网关模式",
        "通过统一的API网关处理所有客户端请求"
    )
    
    # 添加质量属性
    architecture.add_quality_attribute(
        "性能",
        "系统响应时间和吞吐量",
        ["API响应时间 < 200ms", "支持1000并发用户", "数据库查询 < 100ms"]
    )
    architecture.add_quality_attribute(
        "可用性",
        "系统正常运行时间",
        ["系统可用性 > 99.9%", "故障恢复时间 < 5分钟"]
    )
    architecture.add_quality_attribute(
        "可扩展性",
        "系统扩展能力",
        ["支持水平扩展", "微服务独立部署", "数据库分库分表"]
    )
    architecture.add_quality_attribute(
        "安全性",
        "系统安全保障",
        ["HTTPS通信", "JWT认证", "SQL注入防护", "XSS防护"]
    )
    
    # 添加约束
    architecture.add_constraint("必须使用Java技术栈")
    architecture.add_constraint("数据库使用MySQL")
    architecture.add_constraint("部署在云平台")
    architecture.add_constraint("支持Docker容器化")
    
    return architecture


def demo_use_case_analysis():
    """演示用例分析"""
    analyzer = create_ecommerce_use_case_model()
    
    # 分析用例
    analysis = analyzer.analyze_use_cases()
    
    print(f"\n📊 用例分析结果:")
    print(f"总用例数: {analysis['total_use_cases']}")
    print(f"总参与者数: {analysis['total_actors']}")
    
    print(f"\n🎯 优先级分布:")
    for priority, count in analysis['priority_distribution'].items():
        print(f"   {priority}: {count}个")
    
    print(f"\n🔧 复杂度分布:")
    for complexity, count in analysis['complexity_distribution'].items():
        print(f"   {complexity}: {count}个")
    
    print(f"\n⏱️ 工作量估算:")
    print(f"   总工作量: {analysis['effort_estimation']['total_effort']} 人天")
    print(f"   平均工作量: {analysis['effort_estimation']['average_effort']:.1f} 人天/用例")
    
    print(f"\n👥 参与者参与度:")
    for actor, involvement in analysis['actor_involvement'].items():
        print(f"   {actor} ({involvement['type']}): {involvement['use_case_count']}个用例")
    
    # 生成详细用例文档
    print(f"\n📄 生成'下单购买'用例详细文档:")
    print("-" * 60)
    doc = analyzer.generate_use_case_document("下单购买")
    print(doc)


def demo_system_architecture():
    """演示系统架构设计"""
    architecture = create_system_architecture()
    
    print(f"\n🏗️ 系统架构: {architecture.name}")
    print(f"描述: {architecture.description}")
    
    print(f"\n📚 架构层次:")
    for layer in architecture.layers:
        print(f"   {layer['name']}: {layer['description']}")
        print(f"     组件: {', '.join(layer['components'])}")
    
    print(f"\n🎨 架构模式:")
    for pattern in architecture.patterns:
        print(f"   {pattern['name']}: {pattern['description']}")
    
    print(f"\n⭐ 质量属性:")
    for qa in architecture.quality_attributes:
        print(f"   {qa['attribute']}: {qa['description']}")
        for measure in qa['measures']:
            print(f"     - {measure}")
    
    print(f"\n⚠️ 架构约束:")
    for constraint in architecture.constraints:
        print(f"   - {constraint}")
    
    # 分析依赖关系
    dependency_analysis = architecture.analyze_dependencies()
    print(f"\n🔗 依赖关系分析:")
    print(f"   组件总数: {dependency_analysis['component_count']}")
    print(f"   依赖关系总数: {dependency_analysis['total_dependencies']}")
    
    if dependency_analysis['circular_dependencies']:
        print(f"   ⚠️ 发现循环依赖:")
        for circular in dependency_analysis['circular_dependencies']:
            print(f"     {circular}")
    else:
        print(f"   ✅ 未发现循环依赖")


def main():
    """主函数：演示用例分析与系统架构设计"""
    print("Session26 示例2: 用例分析与系统架构设计")
    print("=" * 60)
    print("本示例展示了：")
    print("1. 用例建模和分析")
    print("2. 系统架构设计")
    print("3. 组件关系分析")
    print("4. 质量属性定义")
    
    try:
        # 演示用例分析
        demo_use_case_analysis()
        
        # 演示系统架构设计
        demo_system_architecture()
        
        print("\n" + "="*60)
        print("🎉 用例分析与系统架构设计演示完成！")
        print("="*60)
        print("\n💡 关键要点:")
        print("✅ 用例分析帮助理解系统功能需求")
        print("✅ 系统架构设计确保系统质量")
        print("✅ 组件化设计提高系统可维护性")
        print("✅ 质量属性指导架构决策")
        print("\n🔧 实践建议:")
        print("• 用例要覆盖所有功能需求")
        print("• 架构设计要考虑非功能性需求")
        print("• 组件职责要单一明确")
        print("• 定期评估和优化架构")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        print("请检查代码并重试。")


if __name__ == "__main__":
    main()