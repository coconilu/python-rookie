#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session26 练习2: 系统设计实践

练习目标：
1. 实践系统架构设计
2. 进行数据库设计
3. 设计API接口
4. 创建系统文档

练习场景：
设计一个在线学习平台系统

作者: Python教程团队
创建日期: 2024-01-15
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime


class ComponentType(Enum):
    """组件类型"""
    FRONTEND = "前端"
    BACKEND = "后端"
    DATABASE = "数据库"
    CACHE = "缓存"
    MESSAGE_QUEUE = "消息队列"
    FILE_STORAGE = "文件存储"
    CDN = "CDN"
    LOAD_BALANCER = "负载均衡器"
    API_GATEWAY = "API网关"


class DataType(Enum):
    """数据类型"""
    INT = "INT"
    BIGINT = "BIGINT"
    VARCHAR = "VARCHAR"
    TEXT = "TEXT"
    DECIMAL = "DECIMAL"
    DATETIME = "DATETIME"
    TIMESTAMP = "TIMESTAMP"
    BOOLEAN = "BOOLEAN"
    JSON = "JSON"
    BLOB = "BLOB"


class HttpMethod(Enum):
    """HTTP方法"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


@dataclass
class SystemComponent:
    """系统组件"""
    name: str
    component_type: ComponentType
    description: str
    technology: str = ""
    dependencies: List[str] = field(default_factory=list)
    interfaces: List[str] = field(default_factory=list)
    performance_requirements: Dict[str, Any] = field(default_factory=dict)
    
    def add_dependency(self, component_name: str):
        """添加依赖"""
        if component_name not in self.dependencies:
            self.dependencies.append(component_name)
    
    def add_interface(self, interface_name: str):
        """添加接口"""
        if interface_name not in self.interfaces:
            self.interfaces.append(interface_name)


@dataclass
class DatabaseField:
    """数据库字段"""
    name: str
    data_type: DataType
    length: Optional[int] = None
    nullable: bool = True
    default_value: Optional[str] = None
    comment: str = ""
    is_primary_key: bool = False
    is_foreign_key: bool = False
    foreign_table: Optional[str] = None
    foreign_field: Optional[str] = None


@dataclass
class DatabaseTable:
    """数据库表"""
    name: str
    description: str
    fields: List[DatabaseField] = field(default_factory=list)
    indexes: List[str] = field(default_factory=list)
    
    def add_field(self, field: DatabaseField):
        """添加字段"""
        self.fields.append(field)
    
    def add_index(self, index_name: str):
        """添加索引"""
        if index_name not in self.indexes:
            self.indexes.append(index_name)
    
    def get_primary_keys(self) -> List[str]:
        """获取主键字段"""
        return [field.name for field in self.fields if field.is_primary_key]
    
    def get_foreign_keys(self) -> List[Tuple[str, str, str]]:
        """获取外键关系 (field_name, foreign_table, foreign_field)"""
        return [(field.name, field.foreign_table, field.foreign_field) 
                for field in self.fields if field.is_foreign_key]


@dataclass
class APIEndpoint:
    """API端点"""
    path: str
    method: HttpMethod
    description: str
    request_params: Dict[str, str] = field(default_factory=dict)
    request_body: Optional[Dict[str, Any]] = None
    response_format: Dict[str, Any] = field(default_factory=dict)
    auth_required: bool = True
    rate_limit: Optional[str] = None
    
    def add_request_param(self, param_name: str, param_type: str, description: str = ""):
        """添加请求参数"""
        self.request_params[param_name] = f"{param_type} - {description}"


class SystemArchitect:
    """系统架构师"""
    
    def __init__(self, system_name: str):
        self.system_name = system_name
        self.components = {}
        self.database_tables = {}
        self.api_endpoints = []
        self.design_principles = []
        self.quality_attributes = {}
    
    def add_component(self, component: SystemComponent):
        """添加系统组件"""
        self.components[component.name] = component
    
    def add_database_table(self, table: DatabaseTable):
        """添加数据库表"""
        self.database_tables[table.name] = table
    
    def add_api_endpoint(self, endpoint: APIEndpoint):
        """添加API端点"""
        self.api_endpoints.append(endpoint)
    
    def add_design_principle(self, principle: str):
        """添加设计原则"""
        if principle not in self.design_principles:
            self.design_principles.append(principle)
    
    def set_quality_attribute(self, attribute: str, requirement: str):
        """设置质量属性"""
        self.quality_attributes[attribute] = requirement
    
    def generate_architecture_document(self) -> Dict[str, Any]:
        """生成架构文档"""
        doc = {
            "system_name": self.system_name,
            "generated_at": datetime.now().isoformat(),
            "overview": {
                "total_components": len(self.components),
                "total_tables": len(self.database_tables),
                "total_apis": len(self.api_endpoints)
            },
            "components": {},
            "database_design": {},
            "api_design": [],
            "design_principles": self.design_principles,
            "quality_attributes": self.quality_attributes
        }
        
        # 组件信息
        for name, component in self.components.items():
            doc["components"][name] = {
                "type": component.component_type.value,
                "description": component.description,
                "technology": component.technology,
                "dependencies": component.dependencies,
                "interfaces": component.interfaces,
                "performance_requirements": component.performance_requirements
            }
        
        # 数据库设计
        for name, table in self.database_tables.items():
            doc["database_design"][name] = {
                "description": table.description,
                "fields": [{
                    "name": field.name,
                    "type": field.data_type.value,
                    "length": field.length,
                    "nullable": field.nullable,
                    "comment": field.comment,
                    "is_primary_key": field.is_primary_key,
                    "is_foreign_key": field.is_foreign_key
                } for field in table.fields],
                "primary_keys": table.get_primary_keys(),
                "foreign_keys": table.get_foreign_keys(),
                "indexes": table.indexes
            }
        
        # API设计
        for endpoint in self.api_endpoints:
            doc["api_design"].append({
                "path": endpoint.path,
                "method": endpoint.method.value,
                "description": endpoint.description,
                "request_params": endpoint.request_params,
                "request_body": endpoint.request_body,
                "response_format": endpoint.response_format,
                "auth_required": endpoint.auth_required,
                "rate_limit": endpoint.rate_limit
            })
        
        return doc
    
    def analyze_architecture(self) -> Dict[str, Any]:
        """分析架构"""
        analysis = {
            "complexity_metrics": {},
            "dependency_analysis": {},
            "scalability_assessment": {},
            "recommendations": []
        }
        
        # 复杂度指标
        total_dependencies = sum(len(comp.dependencies) for comp in self.components.values())
        avg_dependencies = total_dependencies / len(self.components) if self.components else 0
        
        analysis["complexity_metrics"] = {
            "total_components": len(self.components),
            "total_dependencies": total_dependencies,
            "average_dependencies_per_component": avg_dependencies,
            "database_tables": len(self.database_tables),
            "api_endpoints": len(self.api_endpoints)
        }
        
        # 依赖分析
        component_types = {}
        for component in self.components.values():
            comp_type = component.component_type.value
            component_types[comp_type] = component_types.get(comp_type, 0) + 1
        
        analysis["dependency_analysis"] = {
            "component_distribution": component_types,
            "highly_coupled_components": [
                comp.name for comp in self.components.values() 
                if len(comp.dependencies) > 3
            ]
        }
        
        # 可扩展性评估
        has_load_balancer = any(
            comp.component_type == ComponentType.LOAD_BALANCER 
            for comp in self.components.values()
        )
        has_cache = any(
            comp.component_type == ComponentType.CACHE 
            for comp in self.components.values()
        )
        has_cdn = any(
            comp.component_type == ComponentType.CDN 
            for comp in self.components.values()
        )
        
        analysis["scalability_assessment"] = {
            "has_load_balancer": has_load_balancer,
            "has_cache_layer": has_cache,
            "has_cdn": has_cdn,
            "microservices_ready": len([c for c in self.components.values() 
                                       if c.component_type == ComponentType.BACKEND]) > 1
        }
        
        # 建议
        recommendations = []
        
        if avg_dependencies > 3:
            recommendations.append("组件间耦合度较高，建议考虑解耦")
        
        if not has_load_balancer and len(self.components) > 5:
            recommendations.append("建议添加负载均衡器以提高可用性")
        
        if not has_cache and len(self.database_tables) > 5:
            recommendations.append("建议添加缓存层以提高性能")
        
        if len(self.api_endpoints) > 20:
            recommendations.append("API数量较多，建议考虑API网关进行统一管理")
        
        analysis["recommendations"] = recommendations
        
        return analysis


# TODO: 练习任务
def exercise_learning_platform():
    """
    练习：在线学习平台系统设计
    
    请完成以下任务：
    1. 设计系统架构（包含前端、后端、数据库等组件）
    2. 设计数据库表结构（用户、课程、学习记录等）
    3. 设计API接口（用户管理、课程管理、学习进度等）
    4. 定义系统的质量属性和设计原则
    5. 生成系统设计文档
    """
    print("\n" + "="*60)
    print("🎓 在线学习平台系统设计练习")
    print("="*60)
    
    # 创建系统架构师
    architect = SystemArchitect("在线学习平台")
    
    # TODO: 添加系统组件
    # 示例：前端组件
    frontend = SystemComponent(
        name="Web前端",
        component_type=ComponentType.FRONTEND,
        description="用户界面，提供课程浏览、学习、测试等功能",
        technology="React + TypeScript"
    )
    frontend.add_interface("用户登录界面")
    frontend.add_interface("课程列表界面")
    frontend.add_interface("视频播放界面")
    frontend.performance_requirements = {
        "首屏加载时间": "< 3秒",
        "页面切换响应": "< 1秒"
    }
    architect.add_component(frontend)
    
    # TODO: 添加更多组件
    # 提示：考虑API服务器、数据库、文件存储、缓存等
    
    # TODO: 设计数据库表
    # 示例：用户表
    users_table = DatabaseTable("users", "用户信息表")
    users_table.add_field(DatabaseField(
        name="user_id",
        data_type=DataType.BIGINT,
        nullable=False,
        comment="用户ID",
        is_primary_key=True
    ))
    users_table.add_field(DatabaseField(
        name="username",
        data_type=DataType.VARCHAR,
        length=50,
        nullable=False,
        comment="用户名"
    ))
    users_table.add_field(DatabaseField(
        name="email",
        data_type=DataType.VARCHAR,
        length=100,
        nullable=False,
        comment="邮箱"
    ))
    users_table.add_field(DatabaseField(
        name="password_hash",
        data_type=DataType.VARCHAR,
        length=255,
        nullable=False,
        comment="密码哈希"
    ))
    users_table.add_field(DatabaseField(
        name="created_at",
        data_type=DataType.TIMESTAMP,
        nullable=False,
        default_value="CURRENT_TIMESTAMP",
        comment="创建时间"
    ))
    users_table.add_index("idx_username")
    users_table.add_index("idx_email")
    architect.add_database_table(users_table)
    
    # TODO: 添加更多数据库表
    # 提示：考虑课程表、章节表、学习记录表、评论表等
    
    # TODO: 设计API接口
    # 示例：用户注册接口
    register_api = APIEndpoint(
        path="/api/users/register",
        method=HttpMethod.POST,
        description="用户注册",
        auth_required=False
    )
    register_api.request_body = {
        "username": "string",
        "email": "string",
        "password": "string"
    }
    register_api.response_format = {
        "success": "boolean",
        "message": "string",
        "user_id": "integer"
    }
    register_api.rate_limit = "5次/分钟"
    architect.add_api_endpoint(register_api)
    
    # TODO: 添加更多API接口
    # 提示：考虑登录、课程列表、学习进度、评论等接口
    
    # TODO: 添加设计原则
    architect.add_design_principle("单一职责原则 - 每个组件只负责一个功能")
    architect.add_design_principle("开闭原则 - 对扩展开放，对修改关闭")
    # 添加更多设计原则...
    
    # TODO: 设置质量属性
    architect.set_quality_attribute("性能", "支持1000并发用户，响应时间<3秒")
    architect.set_quality_attribute("可用性", "99.9%可用性，年停机时间<8.76小时")
    # 添加更多质量属性...
    
    # 生成架构文档
    doc = architect.generate_architecture_document()
    print(f"\n📋 系统架构文档")
    print(f"系统名称：{doc['system_name']}")
    print(f"生成时间：{doc['generated_at']}")
    
    print(f"\n📊 系统概览：")
    overview = doc['overview']
    print(f"   组件数量：{overview['total_components']}")
    print(f"   数据表数量：{overview['total_tables']}")
    print(f"   API接口数量：{overview['total_apis']}")
    
    print(f"\n🏗️ 系统组件：")
    for name, component in doc['components'].items():
        print(f"   {name} ({component['type']})")
        print(f"     技术栈：{component['technology']}")
        print(f"     描述：{component['description']}")
        if component['dependencies']:
            print(f"     依赖：{', '.join(component['dependencies'])}")
    
    print(f"\n🗄️ 数据库设计：")
    for table_name, table_info in doc['database_design'].items():
        print(f"   {table_name}: {table_info['description']}")
        print(f"     字段数：{len(table_info['fields'])}")
        print(f"     主键：{', '.join(table_info['primary_keys'])}")
        if table_info['foreign_keys']:
            print(f"     外键：{len(table_info['foreign_keys'])}个")
    
    print(f"\n🔌 API接口：")
    for api in doc['api_design']:
        print(f"   {api['method']} {api['path']}")
        print(f"     描述：{api['description']}")
        print(f"     需要认证：{'是' if api['auth_required'] else '否'}")
    
    print(f"\n📐 设计原则：")
    for principle in doc['design_principles']:
        print(f"   - {principle}")
    
    print(f"\n🎯 质量属性：")
    for attr, req in doc['quality_attributes'].items():
        print(f"   {attr}：{req}")
    
    # 架构分析
    analysis = architect.analyze_architecture()
    print(f"\n📈 架构分析：")
    
    metrics = analysis['complexity_metrics']
    print(f"   复杂度指标：")
    print(f"     平均依赖数：{metrics['average_dependencies_per_component']:.1f}")
    print(f"     总依赖数：{metrics['total_dependencies']}")
    
    scalability = analysis['scalability_assessment']
    print(f"   可扩展性评估：")
    print(f"     负载均衡：{'✅' if scalability['has_load_balancer'] else '❌'}")
    print(f"     缓存层：{'✅' if scalability['has_cache_layer'] else '❌'}")
    print(f"     CDN：{'✅' if scalability['has_cdn'] else '❌'}")
    
    if analysis['recommendations']:
        print(f"\n💡 改进建议：")
        for rec in analysis['recommendations']:
            print(f"   - {rec}")
    
    print(f"\n💡 练习提示：")
    print(f"1. 尝试添加更多系统组件（如消息队列、搜索引擎等）")
    print(f"2. 完善数据库表设计，考虑表之间的关系")
    print(f"3. 设计完整的API接口，包括错误处理")
    print(f"4. 考虑系统的安全性、性能和可维护性")
    print(f"5. 思考系统的部署和监控策略")


def main():
    """主函数"""
    print("Session26 练习2: 系统设计实践")
    print("="*80)
    
    try:
        exercise_learning_platform()
        
        print("\n" + "="*60)
        print("✅ 练习完成！")
        print("="*60)
        print("\n🎯 学习目标检查：")
        print("□ 理解了系统架构设计的基本方法")
        print("□ 学会了数据库表结构设计")
        print("□ 掌握了API接口设计规范")
        print("□ 了解了系统质量属性的重要性")
        print("□ 能够进行架构分析和优化")
        
    except Exception as e:
        print(f"❌ 练习过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()