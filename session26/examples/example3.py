#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session26 示例3: 数据库设计与项目规划

本示例演示了：
1. 数据库概念设计（ER模型）
2. 数据库逻辑设计（关系模型）
3. 数据库物理设计（索引、分区等）
4. 项目规划和管理

作者: Python教程团队
创建日期: 2024-01-15
"""

import json
import random
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field


class DataType(Enum):
    """数据类型枚举"""
    INT = "INT"
    BIGINT = "BIGINT"
    VARCHAR = "VARCHAR"
    TEXT = "TEXT"
    DECIMAL = "DECIMAL"
    DATETIME = "DATETIME"
    TIMESTAMP = "TIMESTAMP"
    BOOLEAN = "BOOLEAN"
    JSON = "JSON"


class RelationshipType(Enum):
    """关系类型枚举"""
    ONE_TO_ONE = "1:1"
    ONE_TO_MANY = "1:N"
    MANY_TO_MANY = "M:N"


class IndexType(Enum):
    """索引类型枚举"""
    PRIMARY = "PRIMARY"
    UNIQUE = "UNIQUE"
    INDEX = "INDEX"
    FULLTEXT = "FULLTEXT"


class TaskStatus(Enum):
    """任务状态枚举"""
    NOT_STARTED = "未开始"
    IN_PROGRESS = "进行中"
    COMPLETED = "已完成"
    BLOCKED = "阻塞"
    CANCELLED = "已取消"


class TaskPriority(Enum):
    """任务优先级枚举"""
    LOW = "低"
    MEDIUM = "中"
    HIGH = "高"
    CRITICAL = "紧急"


@dataclass
class Attribute:
    """实体属性"""
    name: str
    data_type: DataType
    length: Optional[int] = None
    precision: Optional[int] = None
    scale: Optional[int] = None
    nullable: bool = True
    default_value: Optional[str] = None
    comment: str = ""
    
    def to_sql(self) -> str:
        """转换为SQL定义"""
        sql = f"`{self.name}` {self.data_type.value}"
        
        if self.data_type in [DataType.VARCHAR] and self.length:
            sql += f"({self.length})"
        elif self.data_type == DataType.DECIMAL and self.precision and self.scale:
            sql += f"({self.precision},{self.scale})"
        
        if not self.nullable:
            sql += " NOT NULL"
        
        if self.default_value:
            sql += f" DEFAULT {self.default_value}"
        
        if self.comment:
            sql += f" COMMENT '{self.comment}'"
        
        return sql


@dataclass
class Entity:
    """实体类"""
    name: str
    description: str
    attributes: List[Attribute] = field(default_factory=list)
    primary_key: List[str] = field(default_factory=list)
    
    def add_attribute(self, attribute: Attribute):
        """添加属性"""
        self.attributes.append(attribute)
    
    def set_primary_key(self, *attr_names: str):
        """设置主键"""
        self.primary_key = list(attr_names)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "name": self.name,
            "description": self.description,
            "attributes": [{
                "name": attr.name,
                "type": attr.data_type.value,
                "length": attr.length,
                "nullable": attr.nullable,
                "comment": attr.comment
            } for attr in self.attributes],
            "primary_key": self.primary_key
        }


@dataclass
class Relationship:
    """关系类"""
    name: str
    entity1: str
    entity2: str
    relationship_type: RelationshipType
    description: str = ""
    foreign_key_attrs: List[Tuple[str, str]] = field(default_factory=list)  # (from_attr, to_attr)
    
    def add_foreign_key(self, from_attr: str, to_attr: str):
        """添加外键关系"""
        self.foreign_key_attrs.append((from_attr, to_attr))
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "name": self.name,
            "entity1": self.entity1,
            "entity2": self.entity2,
            "type": self.relationship_type.value,
            "description": self.description,
            "foreign_keys": self.foreign_key_attrs
        }


@dataclass
class Index:
    """索引类"""
    name: str
    table_name: str
    index_type: IndexType
    columns: List[str]
    comment: str = ""
    
    def to_sql(self) -> str:
        """转换为SQL语句"""
        if self.index_type == IndexType.PRIMARY:
            return f"PRIMARY KEY ({', '.join(f'`{col}`' for col in self.columns)})"
        elif self.index_type == IndexType.UNIQUE:
            return f"UNIQUE KEY `{self.name}` ({', '.join(f'`{col}`' for col in self.columns)})"
        elif self.index_type == IndexType.INDEX:
            return f"KEY `{self.name}` ({', '.join(f'`{col}`' for col in self.columns)})"
        elif self.index_type == IndexType.FULLTEXT:
            return f"FULLTEXT KEY `{self.name}` ({', '.join(f'`{col}`' for col in self.columns)})"
        return ""


class DatabaseDesigner:
    """数据库设计器"""
    
    def __init__(self, database_name: str):
        self.database_name = database_name
        self.entities = {}
        self.relationships = []
        self.indexes = []
        self.constraints = []
    
    def add_entity(self, entity: Entity):
        """添加实体"""
        self.entities[entity.name] = entity
    
    def add_relationship(self, relationship: Relationship):
        """添加关系"""
        self.relationships.append(relationship)
    
    def add_index(self, index: Index):
        """添加索引"""
        self.indexes.append(index)
    
    def generate_create_table_sql(self, entity_name: str) -> str:
        """生成建表SQL"""
        if entity_name not in self.entities:
            return f"-- 实体 {entity_name} 不存在"
        
        entity = self.entities[entity_name]
        
        sql = f"CREATE TABLE `{entity_name}` (\n"
        
        # 添加字段定义
        column_definitions = []
        for attr in entity.attributes:
            column_definitions.append(f"  {attr.to_sql()}")
        
        sql += ",\n".join(column_definitions)
        
        # 添加主键
        if entity.primary_key:
            sql += f",\n  PRIMARY KEY ({', '.join(f'`{pk}`' for pk in entity.primary_key)})"
        
        # 添加索引
        entity_indexes = [idx for idx in self.indexes if idx.table_name == entity_name]
        for index in entity_indexes:
            if index.index_type != IndexType.PRIMARY:
                sql += f",\n  {index.to_sql()}"
        
        sql += f"\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='{entity.description}';\n"
        
        return sql
    
    def generate_all_tables_sql(self) -> str:
        """生成所有表的SQL"""
        sql = f"-- 数据库: {self.database_name}\n"
        sql += f"-- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        sql += f"CREATE DATABASE IF NOT EXISTS `{self.database_name}` DEFAULT CHARSET=utf8mb4;\n"
        sql += f"USE `{self.database_name}`;\n\n"
        
        # 按依赖关系排序表（简单实现）
        sorted_entities = self._sort_entities_by_dependency()
        
        for entity_name in sorted_entities:
            sql += self.generate_create_table_sql(entity_name) + "\n"
        
        # 添加外键约束
        sql += self._generate_foreign_key_constraints()
        
        return sql
    
    def _sort_entities_by_dependency(self) -> List[str]:
        """按依赖关系排序实体（简单拓扑排序）"""
        # 简化实现：主表在前，从表在后
        independent_entities = []
        dependent_entities = []
        
        for entity_name in self.entities.keys():
            has_foreign_key = any(
                rel.entity2 == entity_name for rel in self.relationships
                if rel.relationship_type in [RelationshipType.ONE_TO_MANY, RelationshipType.ONE_TO_ONE]
            )
            
            if has_foreign_key:
                dependent_entities.append(entity_name)
            else:
                independent_entities.append(entity_name)
        
        return independent_entities + dependent_entities
    
    def _generate_foreign_key_constraints(self) -> str:
        """生成外键约束SQL"""
        sql = "-- 外键约束\n"
        
        for rel in self.relationships:
            if rel.relationship_type in [RelationshipType.ONE_TO_MANY, RelationshipType.ONE_TO_ONE]:
                for from_attr, to_attr in rel.foreign_key_attrs:
                    constraint_name = f"fk_{rel.entity2}_{from_attr}"
                    sql += f"ALTER TABLE `{rel.entity2}` ADD CONSTRAINT `{constraint_name}` "
                    sql += f"FOREIGN KEY (`{from_attr}`) REFERENCES `{rel.entity1}`(`{to_attr}`);\n"
        
        return sql + "\n"
    
    def analyze_design(self) -> Dict[str, Any]:
        """分析数据库设计"""
        analysis = {
            "database_name": self.database_name,
            "total_entities": len(self.entities),
            "total_relationships": len(self.relationships),
            "total_indexes": len(self.indexes),
            "entity_analysis": {},
            "relationship_analysis": {},
            "design_suggestions": []
        }
        
        # 分析实体
        for entity_name, entity in self.entities.items():
            analysis["entity_analysis"][entity_name] = {
                "attribute_count": len(entity.attributes),
                "has_primary_key": bool(entity.primary_key),
                "nullable_attributes": sum(1 for attr in entity.attributes if attr.nullable),
                "text_attributes": sum(1 for attr in entity.attributes if attr.data_type in [DataType.VARCHAR, DataType.TEXT])
            }
        
        # 分析关系
        relationship_types = {}
        for rel in self.relationships:
            rel_type = rel.relationship_type.value
            relationship_types[rel_type] = relationship_types.get(rel_type, 0) + 1
        
        analysis["relationship_analysis"] = {
            "by_type": relationship_types,
            "entities_with_relationships": len(set(
                [rel.entity1 for rel in self.relationships] + 
                [rel.entity2 for rel in self.relationships]
            ))
        }
        
        # 设计建议
        suggestions = []
        
        # 检查缺少主键的实体
        entities_without_pk = [name for name, entity in self.entities.items() if not entity.primary_key]
        if entities_without_pk:
            suggestions.append(f"以下实体缺少主键: {', '.join(entities_without_pk)}")
        
        # 检查缺少索引的外键
        foreign_key_columns = set()
        for rel in self.relationships:
            for from_attr, _ in rel.foreign_key_attrs:
                foreign_key_columns.add((rel.entity2, from_attr))
        
        indexed_columns = set()
        for index in self.indexes:
            for col in index.columns:
                indexed_columns.add((index.table_name, col))
        
        unindexed_fks = foreign_key_columns - indexed_columns
        if unindexed_fks:
            suggestions.append(f"建议为以下外键添加索引: {unindexed_fks}")
        
        # 检查过多的nullable字段
        for entity_name, entity in self.entities.items():
            nullable_ratio = sum(1 for attr in entity.attributes if attr.nullable) / len(entity.attributes)
            if nullable_ratio > 0.7:
                suggestions.append(f"实体 {entity_name} 有过多可空字段({nullable_ratio:.1%})，考虑数据完整性")
        
        analysis["design_suggestions"] = suggestions
        
        return analysis


@dataclass
class Task:
    """项目任务"""
    id: str
    name: str
    description: str
    priority: TaskPriority
    status: TaskStatus
    estimated_hours: int
    actual_hours: int = 0
    assignee: str = ""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    
    def add_dependency(self, task_id: str):
        """添加依赖任务"""
        if task_id not in self.dependencies:
            self.dependencies.append(task_id)
    
    def add_tag(self, tag: str):
        """添加标签"""
        if tag not in self.tags:
            self.tags.append(tag)
    
    def get_progress(self) -> float:
        """获取进度百分比"""
        if self.estimated_hours == 0:
            return 0.0
        return min(self.actual_hours / self.estimated_hours * 100, 100.0)
    
    def is_overdue(self) -> bool:
        """是否逾期"""
        if not self.end_date or self.status == TaskStatus.COMPLETED:
            return False
        return datetime.now() > self.end_date
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "priority": self.priority.value,
            "status": self.status.value,
            "estimated_hours": self.estimated_hours,
            "actual_hours": self.actual_hours,
            "assignee": self.assignee,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "dependencies": self.dependencies,
            "tags": self.tags,
            "progress": self.get_progress(),
            "is_overdue": self.is_overdue()
        }


class ProjectPlanner:
    """项目规划器"""
    
    def __init__(self, project_name: str, start_date: datetime):
        self.project_name = project_name
        self.start_date = start_date
        self.tasks = {}
        self.milestones = []
        self.team_members = []
        self.risks = []
    
    def add_task(self, task: Task):
        """添加任务"""
        self.tasks[task.id] = task
    
    def add_milestone(self, name: str, date: datetime, description: str = ""):
        """添加里程碑"""
        self.milestones.append({
            "name": name,
            "date": date,
            "description": description
        })
    
    def add_team_member(self, name: str, role: str, skills: List[str]):
        """添加团队成员"""
        self.team_members.append({
            "name": name,
            "role": role,
            "skills": skills,
            "workload": 0  # 工作负荷（小时）
        })
    
    def add_risk(self, description: str, probability: str, impact: str, mitigation: str):
        """添加风险"""
        self.risks.append({
            "description": description,
            "probability": probability,  # 高/中/低
            "impact": impact,  # 高/中/低
            "mitigation": mitigation
        })
    
    def assign_task(self, task_id: str, assignee: str):
        """分配任务"""
        if task_id in self.tasks:
            self.tasks[task_id].assignee = assignee
            
            # 更新团队成员工作负荷
            for member in self.team_members:
                if member["name"] == assignee:
                    member["workload"] += self.tasks[task_id].estimated_hours
                    break
    
    def update_task_status(self, task_id: str, status: TaskStatus, actual_hours: int = None):
        """更新任务状态"""
        if task_id in self.tasks:
            self.tasks[task_id].status = status
            if actual_hours is not None:
                self.tasks[task_id].actual_hours = actual_hours
    
    def get_critical_path(self) -> List[str]:
        """获取关键路径（简化实现）"""
        # 简化的关键路径算法
        task_durations = {}
        for task_id, task in self.tasks.items():
            task_durations[task_id] = task.estimated_hours
        
        # 找出没有依赖的任务作为起点
        start_tasks = [task_id for task_id, task in self.tasks.items() if not task.dependencies]
        
        # 简单实现：返回最长的依赖链
        longest_path = []
        max_duration = 0
        
        def find_longest_path(task_id: str, current_path: List[str], current_duration: int):
            nonlocal longest_path, max_duration
            
            current_path = current_path + [task_id]
            current_duration += task_durations.get(task_id, 0)
            
            # 找到依赖当前任务的任务
            dependent_tasks = [tid for tid, task in self.tasks.items() if task_id in task.dependencies]
            
            if not dependent_tasks:
                # 到达终点
                if current_duration > max_duration:
                    max_duration = current_duration
                    longest_path = current_path.copy()
            else:
                for dep_task in dependent_tasks:
                    find_longest_path(dep_task, current_path, current_duration)
        
        for start_task in start_tasks:
            find_longest_path(start_task, [], 0)
        
        return longest_path
    
    def generate_gantt_data(self) -> List[Dict[str, Any]]:
        """生成甘特图数据"""
        gantt_data = []
        
        for task_id, task in self.tasks.items():
            if task.start_date and task.end_date:
                gantt_data.append({
                    "task_id": task_id,
                    "task_name": task.name,
                    "start_date": task.start_date.strftime("%Y-%m-%d"),
                    "end_date": task.end_date.strftime("%Y-%m-%d"),
                    "duration": (task.end_date - task.start_date).days + 1,
                    "progress": task.get_progress(),
                    "assignee": task.assignee,
                    "status": task.status.value,
                    "dependencies": task.dependencies
                })
        
        return sorted(gantt_data, key=lambda x: x["start_date"])
    
    def analyze_project(self) -> Dict[str, Any]:
        """分析项目"""
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for task in self.tasks.values() if task.status == TaskStatus.COMPLETED)
        in_progress_tasks = sum(1 for task in self.tasks.values() if task.status == TaskStatus.IN_PROGRESS)
        blocked_tasks = sum(1 for task in self.tasks.values() if task.status == TaskStatus.BLOCKED)
        overdue_tasks = sum(1 for task in self.tasks.values() if task.is_overdue())
        
        total_estimated_hours = sum(task.estimated_hours for task in self.tasks.values())
        total_actual_hours = sum(task.actual_hours for task in self.tasks.values())
        
        # 按优先级统计
        priority_stats = {}
        for priority in TaskPriority:
            priority_stats[priority.value] = sum(
                1 for task in self.tasks.values() if task.priority == priority
            )
        
        # 团队工作负荷
        team_workload = {}
        for member in self.team_members:
            assigned_tasks = [task for task in self.tasks.values() if task.assignee == member["name"]]
            team_workload[member["name"]] = {
                "total_hours": sum(task.estimated_hours for task in assigned_tasks),
                "completed_hours": sum(task.actual_hours for task in assigned_tasks if task.status == TaskStatus.COMPLETED),
                "task_count": len(assigned_tasks)
            }
        
        # 关键路径
        critical_path = self.get_critical_path()
        critical_path_duration = sum(
            self.tasks[task_id].estimated_hours for task_id in critical_path
        )
        
        return {
            "project_name": self.project_name,
            "start_date": self.start_date.strftime("%Y-%m-%d"),
            "task_statistics": {
                "total": total_tasks,
                "completed": completed_tasks,
                "in_progress": in_progress_tasks,
                "blocked": blocked_tasks,
                "overdue": overdue_tasks,
                "completion_rate": completed_tasks / total_tasks * 100 if total_tasks > 0 else 0
            },
            "effort_statistics": {
                "estimated_hours": total_estimated_hours,
                "actual_hours": total_actual_hours,
                "efficiency": total_estimated_hours / total_actual_hours * 100 if total_actual_hours > 0 else 0
            },
            "priority_distribution": priority_stats,
            "team_workload": team_workload,
            "critical_path": {
                "tasks": critical_path,
                "duration_hours": critical_path_duration,
                "duration_days": critical_path_duration / 8  # 假设每天8小时
            },
            "milestones": len(self.milestones),
            "risks": len(self.risks)
        }


def create_ecommerce_database_design():
    """创建电商数据库设计"""
    print("\n" + "="*60)
    print("🗄️ 创建电商数据库设计")
    print("="*60)
    
    designer = DatabaseDesigner("ecommerce_db")
    
    # 用户表
    user_entity = Entity("users", "用户信息表")
    user_entity.add_attribute(Attribute("user_id", DataType.BIGINT, nullable=False, comment="用户ID"))
    user_entity.add_attribute(Attribute("username", DataType.VARCHAR, 50, nullable=False, comment="用户名"))
    user_entity.add_attribute(Attribute("email", DataType.VARCHAR, 100, nullable=False, comment="邮箱"))
    user_entity.add_attribute(Attribute("password_hash", DataType.VARCHAR, 255, nullable=False, comment="密码哈希"))
    user_entity.add_attribute(Attribute("phone", DataType.VARCHAR, 20, comment="手机号"))
    user_entity.add_attribute(Attribute("real_name", DataType.VARCHAR, 50, comment="真实姓名"))
    user_entity.add_attribute(Attribute("gender", DataType.VARCHAR, 10, comment="性别"))
    user_entity.add_attribute(Attribute("birth_date", DataType.DATETIME, comment="出生日期"))
    user_entity.add_attribute(Attribute("avatar_url", DataType.VARCHAR, 255, comment="头像URL"))
    user_entity.add_attribute(Attribute("status", DataType.VARCHAR, 20, nullable=False, default_value="'active'", comment="状态"))
    user_entity.add_attribute(Attribute("created_at", DataType.TIMESTAMP, nullable=False, default_value="CURRENT_TIMESTAMP", comment="创建时间"))
    user_entity.add_attribute(Attribute("updated_at", DataType.TIMESTAMP, nullable=False, default_value="CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP", comment="更新时间"))
    user_entity.set_primary_key("user_id")
    designer.add_entity(user_entity)
    
    # 商品分类表
    category_entity = Entity("categories", "商品分类表")
    category_entity.add_attribute(Attribute("category_id", DataType.INT, nullable=False, comment="分类ID"))
    category_entity.add_attribute(Attribute("parent_id", DataType.INT, comment="父分类ID"))
    category_entity.add_attribute(Attribute("category_name", DataType.VARCHAR, 100, nullable=False, comment="分类名称"))
    category_entity.add_attribute(Attribute("description", DataType.TEXT, comment="分类描述"))
    category_entity.add_attribute(Attribute("image_url", DataType.VARCHAR, 255, comment="分类图片"))
    category_entity.add_attribute(Attribute("sort_order", DataType.INT, default_value="0", comment="排序"))
    category_entity.add_attribute(Attribute("is_active", DataType.BOOLEAN, nullable=False, default_value="1", comment="是否启用"))
    category_entity.add_attribute(Attribute("created_at", DataType.TIMESTAMP, nullable=False, default_value="CURRENT_TIMESTAMP", comment="创建时间"))
    category_entity.set_primary_key("category_id")
    designer.add_entity(category_entity)
    
    # 商品表
    product_entity = Entity("products", "商品信息表")
    product_entity.add_attribute(Attribute("product_id", DataType.BIGINT, nullable=False, comment="商品ID"))
    product_entity.add_attribute(Attribute("category_id", DataType.INT, nullable=False, comment="分类ID"))
    product_entity.add_attribute(Attribute("product_name", DataType.VARCHAR, 200, nullable=False, comment="商品名称"))
    product_entity.add_attribute(Attribute("description", DataType.TEXT, comment="商品描述"))
    product_entity.add_attribute(Attribute("price", DataType.DECIMAL, precision=10, scale=2, nullable=False, comment="价格"))
    product_entity.add_attribute(Attribute("original_price", DataType.DECIMAL, precision=10, scale=2, comment="原价"))
    product_entity.add_attribute(Attribute("stock_quantity", DataType.INT, nullable=False, default_value="0", comment="库存数量"))
    product_entity.add_attribute(Attribute("sku", DataType.VARCHAR, 100, comment="商品编码"))
    product_entity.add_attribute(Attribute("brand", DataType.VARCHAR, 100, comment="品牌"))
    product_entity.add_attribute(Attribute("weight", DataType.DECIMAL, precision=8, scale=2, comment="重量(kg)"))
    product_entity.add_attribute(Attribute("dimensions", DataType.VARCHAR, 100, comment="尺寸"))
    product_entity.add_attribute(Attribute("images", DataType.JSON, comment="商品图片JSON"))
    product_entity.add_attribute(Attribute("attributes", DataType.JSON, comment="商品属性JSON"))
    product_entity.add_attribute(Attribute("status", DataType.VARCHAR, 20, nullable=False, default_value="'active'", comment="状态"))
    product_entity.add_attribute(Attribute("created_at", DataType.TIMESTAMP, nullable=False, default_value="CURRENT_TIMESTAMP", comment="创建时间"))
    product_entity.add_attribute(Attribute("updated_at", DataType.TIMESTAMP, nullable=False, default_value="CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP", comment="更新时间"))
    product_entity.set_primary_key("product_id")
    designer.add_entity(product_entity)
    
    # 订单表
    order_entity = Entity("orders", "订单信息表")
    order_entity.add_attribute(Attribute("order_id", DataType.BIGINT, nullable=False, comment="订单ID"))
    order_entity.add_attribute(Attribute("user_id", DataType.BIGINT, nullable=False, comment="用户ID"))
    order_entity.add_attribute(Attribute("order_number", DataType.VARCHAR, 50, nullable=False, comment="订单号"))
    order_entity.add_attribute(Attribute("total_amount", DataType.DECIMAL, precision=10, scale=2, nullable=False, comment="订单总金额"))
    order_entity.add_attribute(Attribute("discount_amount", DataType.DECIMAL, precision=10, scale=2, default_value="0.00", comment="优惠金额"))
    order_entity.add_attribute(Attribute("shipping_fee", DataType.DECIMAL, precision=10, scale=2, default_value="0.00", comment="运费"))
    order_entity.add_attribute(Attribute("payment_method", DataType.VARCHAR, 50, comment="支付方式"))
    order_entity.add_attribute(Attribute("payment_status", DataType.VARCHAR, 20, nullable=False, default_value="'pending'", comment="支付状态"))
    order_entity.add_attribute(Attribute("order_status", DataType.VARCHAR, 20, nullable=False, default_value="'pending'", comment="订单状态"))
    order_entity.add_attribute(Attribute("shipping_address", DataType.JSON, comment="收货地址JSON"))
    order_entity.add_attribute(Attribute("remark", DataType.TEXT, comment="备注"))
    order_entity.add_attribute(Attribute("created_at", DataType.TIMESTAMP, nullable=False, default_value="CURRENT_TIMESTAMP", comment="创建时间"))
    order_entity.add_attribute(Attribute("updated_at", DataType.TIMESTAMP, nullable=False, default_value="CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP", comment="更新时间"))
    order_entity.set_primary_key("order_id")
    designer.add_entity(order_entity)
    
    # 订单商品表
    order_item_entity = Entity("order_items", "订单商品明细表")
    order_item_entity.add_attribute(Attribute("item_id", DataType.BIGINT, nullable=False, comment="明细ID"))
    order_item_entity.add_attribute(Attribute("order_id", DataType.BIGINT, nullable=False, comment="订单ID"))
    order_item_entity.add_attribute(Attribute("product_id", DataType.BIGINT, nullable=False, comment="商品ID"))
    order_item_entity.add_attribute(Attribute("product_name", DataType.VARCHAR, 200, nullable=False, comment="商品名称"))
    order_item_entity.add_attribute(Attribute("product_price", DataType.DECIMAL, precision=10, scale=2, nullable=False, comment="商品单价"))
    order_item_entity.add_attribute(Attribute("quantity", DataType.INT, nullable=False, comment="购买数量"))
    order_item_entity.add_attribute(Attribute("subtotal", DataType.DECIMAL, precision=10, scale=2, nullable=False, comment="小计"))
    order_item_entity.set_primary_key("item_id")
    designer.add_entity(order_item_entity)
    
    # 购物车表
    cart_entity = Entity("shopping_cart", "购物车表")
    cart_entity.add_attribute(Attribute("cart_id", DataType.BIGINT, nullable=False, comment="购物车ID"))
    cart_entity.add_attribute(Attribute("user_id", DataType.BIGINT, nullable=False, comment="用户ID"))
    cart_entity.add_attribute(Attribute("product_id", DataType.BIGINT, nullable=False, comment="商品ID"))
    cart_entity.add_attribute(Attribute("quantity", DataType.INT, nullable=False, comment="数量"))
    cart_entity.add_attribute(Attribute("created_at", DataType.TIMESTAMP, nullable=False, default_value="CURRENT_TIMESTAMP", comment="创建时间"))
    cart_entity.set_primary_key("cart_id")
    designer.add_entity(cart_entity)
    
    # 添加关系
    designer.add_relationship(Relationship(
        "用户-订单", "users", "orders", RelationshipType.ONE_TO_MANY,
        "一个用户可以有多个订单"
    ))
    designer.relationships[-1].add_foreign_key("user_id", "user_id")
    
    designer.add_relationship(Relationship(
        "分类-商品", "categories", "products", RelationshipType.ONE_TO_MANY,
        "一个分类可以有多个商品"
    ))
    designer.relationships[-1].add_foreign_key("category_id", "category_id")
    
    designer.add_relationship(Relationship(
        "订单-订单商品", "orders", "order_items", RelationshipType.ONE_TO_MANY,
        "一个订单可以有多个商品明细"
    ))
    designer.relationships[-1].add_foreign_key("order_id", "order_id")
    
    designer.add_relationship(Relationship(
        "商品-订单商品", "products", "order_items", RelationshipType.ONE_TO_MANY,
        "一个商品可以在多个订单中"
    ))
    designer.relationships[-1].add_foreign_key("product_id", "product_id")
    
    designer.add_relationship(Relationship(
        "用户-购物车", "users", "shopping_cart", RelationshipType.ONE_TO_MANY,
        "一个用户可以有多个购物车商品"
    ))
    designer.relationships[-1].add_foreign_key("user_id", "user_id")
    
    designer.add_relationship(Relationship(
        "商品-购物车", "products", "shopping_cart", RelationshipType.ONE_TO_MANY,
        "一个商品可以被多个用户加入购物车"
    ))
    designer.relationships[-1].add_foreign_key("product_id", "product_id")
    
    # 添加索引
    indexes = [
        Index("idx_users_username", "users", IndexType.UNIQUE, ["username"]),
        Index("idx_users_email", "users", IndexType.UNIQUE, ["email"]),
        Index("idx_users_phone", "users", IndexType.INDEX, ["phone"]),
        Index("idx_categories_parent", "categories", IndexType.INDEX, ["parent_id"]),
        Index("idx_products_category", "products", IndexType.INDEX, ["category_id"]),
        Index("idx_products_sku", "products", IndexType.UNIQUE, ["sku"]),
        Index("idx_products_name", "products", IndexType.FULLTEXT, ["product_name"]),
        Index("idx_orders_user", "orders", IndexType.INDEX, ["user_id"]),
        Index("idx_orders_number", "orders", IndexType.UNIQUE, ["order_number"]),
        Index("idx_orders_status", "orders", IndexType.INDEX, ["order_status"]),
        Index("idx_order_items_order", "order_items", IndexType.INDEX, ["order_id"]),
        Index("idx_order_items_product", "order_items", IndexType.INDEX, ["product_id"]),
        Index("idx_cart_user", "shopping_cart", IndexType.INDEX, ["user_id"]),
        Index("idx_cart_product", "shopping_cart", IndexType.INDEX, ["product_id"]),
        Index("idx_cart_user_product", "shopping_cart", IndexType.UNIQUE, ["user_id", "product_id"])
    ]
    
    for index in indexes:
        designer.add_index(index)
    
    return designer


def create_project_plan():
    """创建项目计划"""
    print("\n" + "="*60)
    print("📅 创建电商项目计划")
    print("="*60)
    
    # 创建项目规划器
    start_date = datetime(2024, 2, 1)
    planner = ProjectPlanner("电商系统开发项目", start_date)
    
    # 添加团队成员
    team_members = [
        ("张三", "项目经理", ["项目管理", "需求分析"]),
        ("李四", "前端工程师", ["React", "TypeScript", "UI设计"]),
        ("王五", "后端工程师", ["Java", "Spring Boot", "MySQL"]),
        ("赵六", "测试工程师", ["自动化测试", "性能测试"]),
        ("钱七", "运维工程师", ["Docker", "Kubernetes", "监控"])
    ]
    
    for name, role, skills in team_members:
        planner.add_team_member(name, role, skills)
    
    # 添加里程碑
    milestones = [
        ("需求分析完成", start_date + timedelta(days=14), "完成需求收集和分析"),
        ("系统设计完成", start_date + timedelta(days=28), "完成架构设计和数据库设计"),
        ("开发阶段完成", start_date + timedelta(days=70), "完成所有功能开发"),
        ("测试阶段完成", start_date + timedelta(days=84), "完成系统测试和用户验收测试"),
        ("项目上线", start_date + timedelta(days=90), "系统正式上线运行")
    ]
    
    for name, date, description in milestones:
        planner.add_milestone(name, date, description)
    
    # 添加风险
    risks = [
        ("需求变更频繁", "中", "高", "建立需求变更控制流程，定期与客户沟通确认"),
        ("技术难点攻克困难", "低", "高", "提前进行技术预研，准备备选方案"),
        ("团队成员离职", "低", "中", "建立知识文档，交叉培训"),
        ("第三方服务不稳定", "中", "中", "选择可靠的服务提供商，准备备用方案"),
        ("性能不达标", "中", "高", "早期进行性能测试，优化关键路径")
    ]
    
    for description, probability, impact, mitigation in risks:
        planner.add_risk(description, probability, impact, mitigation)
    
    # 创建任务
    tasks_data = [
        # 需求分析阶段
        {
            "id": "REQ001",
            "name": "业务需求调研",
            "description": "与客户沟通，收集业务需求",
            "priority": TaskPriority.HIGH,
            "estimated_hours": 40,
            "assignee": "张三",
            "start_date": start_date,
            "end_date": start_date + timedelta(days=5),
            "tags": ["需求分析", "调研"]
        },
        {
            "id": "REQ002",
            "name": "用例分析",
            "description": "编写用例文档，分析系统功能",
            "priority": TaskPriority.HIGH,
            "estimated_hours": 32,
            "assignee": "张三",
            "start_date": start_date + timedelta(days=5),
            "end_date": start_date + timedelta(days=9),
            "dependencies": ["REQ001"],
            "tags": ["需求分析", "用例"]
        },
        {
            "id": "REQ003",
            "name": "需求文档编写",
            "description": "整理需求文档，确认需求范围",
            "priority": TaskPriority.HIGH,
            "estimated_hours": 24,
            "assignee": "张三",
            "start_date": start_date + timedelta(days=9),
            "end_date": start_date + timedelta(days=12),
            "dependencies": ["REQ002"],
            "tags": ["需求分析", "文档"]
        },
        
        # 设计阶段
        {
            "id": "DES001",
            "name": "系统架构设计",
            "description": "设计系统整体架构",
            "priority": TaskPriority.HIGH,
            "estimated_hours": 40,
            "assignee": "王五",
            "start_date": start_date + timedelta(days=12),
            "end_date": start_date + timedelta(days=17),
            "dependencies": ["REQ003"],
            "tags": ["设计", "架构"]
        },
        {
            "id": "DES002",
            "name": "数据库设计",
            "description": "设计数据库表结构和关系",
            "priority": TaskPriority.HIGH,
            "estimated_hours": 32,
            "assignee": "王五",
            "start_date": start_date + timedelta(days=17),
            "end_date": start_date + timedelta(days=21),
            "dependencies": ["DES001"],
            "tags": ["设计", "数据库"]
        },
        {
            "id": "DES003",
            "name": "UI界面设计",
            "description": "设计用户界面原型",
            "priority": TaskPriority.MEDIUM,
            "estimated_hours": 48,
            "assignee": "李四",
            "start_date": start_date + timedelta(days=12),
            "end_date": start_date + timedelta(days=18),
            "dependencies": ["REQ003"],
            "tags": ["设计", "UI"]
        },
        
        # 开发阶段
        {
            "id": "DEV001",
            "name": "用户管理模块开发",
            "description": "开发用户注册、登录、信息管理功能",
            "priority": TaskPriority.HIGH,
            "estimated_hours": 80,
            "assignee": "王五",
            "start_date": start_date + timedelta(days=21),
            "end_date": start_date + timedelta(days=31),
            "dependencies": ["DES002"],
            "tags": ["开发", "后端", "用户"]
        },
        {
            "id": "DEV002",
            "name": "商品管理模块开发",
            "description": "开发商品CRUD、搜索、分类功能",
            "priority": TaskPriority.HIGH,
            "estimated_hours": 96,
            "assignee": "王五",
            "start_date": start_date + timedelta(days=31),
            "end_date": start_date + timedelta(days=43),
            "dependencies": ["DEV001"],
            "tags": ["开发", "后端", "商品"]
        },
        {
            "id": "DEV003",
            "name": "订单管理模块开发",
            "description": "开发订单创建、支付、状态管理功能",
            "priority": TaskPriority.HIGH,
            "estimated_hours": 120,
            "assignee": "王五",
            "start_date": start_date + timedelta(days=43),
            "end_date": start_date + timedelta(days=58),
            "dependencies": ["DEV002"],
            "tags": ["开发", "后端", "订单"]
        },
        {
            "id": "DEV004",
            "name": "前端页面开发",
            "description": "开发所有前端页面和交互功能",
            "priority": TaskPriority.HIGH,
            "estimated_hours": 160,
            "assignee": "李四",
            "start_date": start_date + timedelta(days=18),
            "end_date": start_date + timedelta(days=38),
            "dependencies": ["DES003"],
            "tags": ["开发", "前端"]
        },
        {
            "id": "DEV005",
            "name": "前后端联调",
            "description": "前后端接口联调和集成测试",
            "priority": TaskPriority.HIGH,
            "estimated_hours": 40,
            "assignee": "李四",
            "start_date": start_date + timedelta(days=58),
            "end_date": start_date + timedelta(days=63),
            "dependencies": ["DEV003", "DEV004"],
            "tags": ["开发", "联调"]
        },
        
        # 测试阶段
        {
            "id": "TEST001",
            "name": "单元测试",
            "description": "编写和执行单元测试",
            "priority": TaskPriority.MEDIUM,
            "estimated_hours": 48,
            "assignee": "赵六",
            "start_date": start_date + timedelta(days=63),
            "end_date": start_date + timedelta(days=69),
            "dependencies": ["DEV005"],
            "tags": ["测试", "单元测试"]
        },
        {
            "id": "TEST002",
            "name": "集成测试",
            "description": "系统集成测试和接口测试",
            "priority": TaskPriority.HIGH,
            "estimated_hours": 56,
            "assignee": "赵六",
            "start_date": start_date + timedelta(days=69),
            "end_date": start_date + timedelta(days=76),
            "dependencies": ["TEST001"],
            "tags": ["测试", "集成测试"]
        },
        {
            "id": "TEST003",
            "name": "性能测试",
            "description": "系统性能和压力测试",
            "priority": TaskPriority.MEDIUM,
            "estimated_hours": 32,
            "assignee": "赵六",
            "start_date": start_date + timedelta(days=76),
            "end_date": start_date + timedelta(days=80),
            "dependencies": ["TEST002"],
            "tags": ["测试", "性能测试"]
        },
        
        # 部署阶段
        {
            "id": "DEPLOY001",
            "name": "环境搭建",
            "description": "搭建生产环境和部署脚本",
            "priority": TaskPriority.HIGH,
            "estimated_hours": 40,
            "assignee": "钱七",
            "start_date": start_date + timedelta(days=80),
            "end_date": start_date + timedelta(days=85),
            "dependencies": ["TEST003"],
            "tags": ["部署", "运维"]
        },
        {
            "id": "DEPLOY002",
            "name": "系统上线",
            "description": "系统正式上线和监控",
            "priority": TaskPriority.CRITICAL,
            "estimated_hours": 24,
            "assignee": "钱七",
            "start_date": start_date + timedelta(days=85),
            "end_date": start_date + timedelta(days=88),
            "dependencies": ["DEPLOY001"],
            "tags": ["部署", "上线"]
        }
    ]
    
    # 创建任务并添加到规划器
    for task_data in tasks_data:
        task = Task(
            task_data["id"],
            task_data["name"],
            task_data["description"],
            task_data["priority"],
            TaskStatus.NOT_STARTED,
            task_data["estimated_hours"]
        )
        
        if "assignee" in task_data:
            task.assignee = task_data["assignee"]
        
        if "start_date" in task_data:
            task.start_date = task_data["start_date"]
        
        if "end_date" in task_data:
            task.end_date = task_data["end_date"]
        
        if "dependencies" in task_data:
            for dep in task_data["dependencies"]:
                task.add_dependency(dep)
        
        if "tags" in task_data:
            for tag in task_data["tags"]:
                task.add_tag(tag)
        
        planner.add_task(task)
    
    # 分配任务（已在创建时分配）
    for task_data in tasks_data:
        if "assignee" in task_data:
            planner.assign_task(task_data["id"], task_data["assignee"])
    
    # 模拟一些任务进度
    planner.update_task_status("REQ001", TaskStatus.COMPLETED, 38)
    planner.update_task_status("REQ002", TaskStatus.COMPLETED, 35)
    planner.update_task_status("REQ003", TaskStatus.IN_PROGRESS, 15)
    planner.update_task_status("DES003", TaskStatus.IN_PROGRESS, 20)
    
    return planner


def demo_database_design():
    """演示数据库设计"""
    designer = create_ecommerce_database_design()
    
    print(f"\n🗄️ 数据库设计: {designer.database_name}")
    print(f"实体数量: {len(designer.entities)}")
    print(f"关系数量: {len(designer.relationships)}")
    print(f"索引数量: {len(designer.indexes)}")
    
    # 显示实体信息
    print(f"\n📋 实体列表:")
    for entity_name, entity in designer.entities.items():
        print(f"   {entity_name}: {entity.description} ({len(entity.attributes)}个字段)")
    
    # 显示关系信息
    print(f"\n🔗 关系列表:")
    for rel in designer.relationships:
        print(f"   {rel.name}: {rel.entity1} {rel.relationship_type.value} {rel.entity2}")
    
    # 生成建表SQL
    print(f"\n📄 生成用户表SQL:")
    print("-" * 60)
    user_sql = designer.generate_create_table_sql("users")
    print(user_sql)
    
    # 分析设计
    analysis = designer.analyze_design()
    print(f"\n📊 设计分析:")
    print(f"   总实体数: {analysis['total_entities']}")
    print(f"   总关系数: {analysis['total_relationships']}")
    print(f"   有关系的实体数: {analysis['relationship_analysis']['entities_with_relationships']}")
    
    if analysis['design_suggestions']:
        print(f"\n💡 设计建议:")
        for suggestion in analysis['design_suggestions']:
            print(f"   - {suggestion}")
    else:
        print(f"\n✅ 设计良好，无明显问题")


def demo_project_planning():
    """演示项目规划"""
    planner = create_project_plan()
    
    # 分析项目
    analysis = planner.analyze_project()
    
    print(f"\n📅 项目: {analysis['project_name']}")
    print(f"开始日期: {analysis['start_date']}")
    
    print(f"\n📊 任务统计:")
    stats = analysis['task_statistics']
    print(f"   总任务数: {stats['total']}")
    print(f"   已完成: {stats['completed']} ({stats['completion_rate']:.1f}%)")
    print(f"   进行中: {stats['in_progress']}")
    print(f"   阻塞: {stats['blocked']}")
    print(f"   逾期: {stats['overdue']}")
    
    print(f"\n⏱️ 工作量统计:")
    effort = analysis['effort_statistics']
    print(f"   预估工时: {effort['estimated_hours']}小时")
    print(f"   实际工时: {effort['actual_hours']}小时")
    if effort['actual_hours'] > 0:
        print(f"   效率: {effort['efficiency']:.1f}%")
    
    print(f"\n🎯 优先级分布:")
    for priority, count in analysis['priority_distribution'].items():
        print(f"   {priority}: {count}个任务")
    
    print(f"\n👥 团队工作负荷:")
    for member, workload in analysis['team_workload'].items():
        print(f"   {member}: {workload['total_hours']}小时 ({workload['task_count']}个任务)")
    
    print(f"\n🛤️ 关键路径:")
    critical_path = analysis['critical_path']
    print(f"   任务: {' -> '.join(critical_path['tasks'])}")
    print(f"   总工期: {critical_path['duration_days']:.1f}天")
    
    print(f"\n🎯 里程碑: {analysis['milestones']}个")
    print(f"⚠️ 风险: {analysis['risks']}个")
    
    # 显示甘特图数据
    print(f"\n📊 甘特图数据 (前5个任务):")
    gantt_data = planner.generate_gantt_data()
    for i, task_data in enumerate(gantt_data[:5]):
        print(f"   {task_data['task_name']}: {task_data['start_date']} ~ {task_data['end_date']} ({task_data['progress']:.1f}%)")
    
    if len(gantt_data) > 5:
        print(f"   ... 还有 {len(gantt_data) - 5} 个任务")


def demo_comprehensive_analysis():
    """综合演示分析"""
    print("\n" + "="*60)
    print("🔍 综合项目分析")
    print("="*60)
    
    # 创建数据库设计和项目规划
    designer = create_ecommerce_database_design()
    planner = create_project_plan()
    
    # 分析数据库设计复杂度
    db_analysis = designer.analyze_design()
    project_analysis = planner.analyze_project()
    
    print(f"\n📈 项目复杂度分析:")
    
    # 数据库复杂度
    db_complexity = {
        "实体数量": db_analysis['total_entities'],
        "关系数量": db_analysis['total_relationships'],
        "索引数量": db_analysis['total_indexes'],
        "平均字段数": sum(len(entity.attributes) for entity in designer.entities.values()) / len(designer.entities)
    }
    
    print(f"   数据库复杂度:")
    for metric, value in db_complexity.items():
        print(f"     {metric}: {value:.1f}" if isinstance(value, float) else f"     {metric}: {value}")
    
    # 项目复杂度
    project_complexity = {
        "任务数量": project_analysis['task_statistics']['total'],
        "团队规模": len(planner.team_members),
        "项目周期": project_analysis['critical_path']['duration_days'],
        "风险数量": project_analysis['risks']
    }
    
    print(f"   项目管理复杂度:")
    for metric, value in project_complexity.items():
        print(f"     {metric}: {value:.1f}" if isinstance(value, float) else f"     {metric}: {value}")
    
    # 生成建议
    print(f"\n💡 综合建议:")
    
    # 数据库建议
    if db_analysis['design_suggestions']:
        print(f"   数据库设计:")
        for suggestion in db_analysis['design_suggestions'][:3]:  # 只显示前3个
            print(f"     - {suggestion}")
    
    # 项目管理建议
    completion_rate = project_analysis['task_statistics']['completion_rate']
    if completion_rate < 30:
        print(f"     - 项目刚开始，建议加强需求确认和设计评审")
    elif completion_rate < 70:
        print(f"     - 项目进行中，建议定期检查进度和质量")
    else:
        print(f"     - 项目接近完成，建议加强测试和上线准备")
    
    if project_analysis['task_statistics']['overdue'] > 0:
        print(f"     - 有逾期任务，建议重新评估计划和资源分配")
    
    # 风险评估
    high_risk_count = len([r for r in planner.risks if r['impact'] == '高'])
    if high_risk_count > 0:
        print(f"     - 存在{high_risk_count}个高影响风险，建议制定详细应对措施")


def main():
    """主函数 - 演示数据库设计与项目规划"""
    print("Session26: 数据库设计与项目规划演示")
    print("="*80)
    
    try:
        # 演示数据库设计
        demo_database_design()
        
        # 演示项目规划
        demo_project_planning()
        
        # 综合分析
        demo_comprehensive_analysis()
        
        print("\n" + "="*60)
        print("✅ 演示完成!")
        print("="*60)
        print("\n本示例展示了:")
        print("1. 📊 数据库概念设计 - 实体、属性、关系建模")
        print("2. 🗄️ 数据库逻辑设计 - 表结构、索引、约束设计")
        print("3. 📅 项目规划管理 - 任务分解、进度跟踪、资源分配")
        print("4. 🔍 风险识别管理 - 风险评估、应对措施")
        print("5. 📈 项目分析报告 - 进度分析、效率评估")
        print("\n💡 学习要点:")
        print("- 数据库设计要考虑业务需求、性能优化和扩展性")
        print("- 项目规划要合理分解任务、评估工期、分配资源")
        print("- 风险管理要提前识别、评估影响、制定应对措施")
        print("- 项目监控要定期检查进度、质量和风险状况")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()