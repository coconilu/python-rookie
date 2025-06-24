#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session26 练习1: 需求收集与分析实践

练习目标：
1. 实践需求收集技术
2. 编写用例分析
3. 进行需求优先级排序
4. 创建需求跟踪矩阵

练习场景：
假设你要为一个小型图书馆开发管理系统

作者: Python教程团队
创建日期: 2024-01-15
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import json


class RequirementType(Enum):
    """需求类型"""
    FUNCTIONAL = "功能性需求"
    NON_FUNCTIONAL = "非功能性需求"
    BUSINESS = "业务需求"
    USER = "用户需求"
    SYSTEM = "系统需求"


class Priority(Enum):
    """优先级"""
    CRITICAL = "关键"
    HIGH = "高"
    MEDIUM = "中"
    LOW = "低"


class RequirementStatus(Enum):
    """需求状态"""
    DRAFT = "草稿"
    REVIEWED = "已评审"
    APPROVED = "已批准"
    IMPLEMENTED = "已实现"
    TESTED = "已测试"
    REJECTED = "已拒绝"


@dataclass
class Stakeholder:
    """利益相关者"""
    name: str
    role: str
    department: str
    contact: str
    influence_level: str  # 高/中/低
    interest_level: str   # 高/中/低
    expectations: List[str] = field(default_factory=list)
    
    def add_expectation(self, expectation: str):
        """添加期望"""
        self.expectations.append(expectation)


@dataclass
class Requirement:
    """需求类"""
    id: str
    title: str
    description: str
    requirement_type: RequirementType
    priority: Priority
    status: RequirementStatus
    source: str  # 需求来源
    stakeholder: str  # 提出者
    acceptance_criteria: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    estimated_effort: int = 0  # 预估工时
    business_value: int = 0    # 业务价值(1-10)
    technical_risk: int = 0    # 技术风险(1-10)
    
    def add_acceptance_criteria(self, criteria: str):
        """添加验收标准"""
        self.acceptance_criteria.append(criteria)
    
    def add_dependency(self, req_id: str):
        """添加依赖"""
        if req_id not in self.dependencies:
            self.dependencies.append(req_id)
    
    def calculate_priority_score(self) -> float:
        """计算优先级分数"""
        priority_weights = {
            Priority.CRITICAL: 4,
            Priority.HIGH: 3,
            Priority.MEDIUM: 2,
            Priority.LOW: 1
        }
        
        base_score = priority_weights[self.priority]
        value_factor = self.business_value / 10
        risk_factor = (11 - self.technical_risk) / 10  # 风险越低分数越高
        
        return base_score * value_factor * risk_factor


class RequirementCollector:
    """需求收集器"""
    
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.stakeholders = {}
        self.requirements = {}
        self.interview_records = []
        self.survey_results = []
    
    def add_stakeholder(self, stakeholder: Stakeholder):
        """添加利益相关者"""
        self.stakeholders[stakeholder.name] = stakeholder
    
    def conduct_interview(self, stakeholder_name: str, questions: List[str]) -> Dict[str, Any]:
        """进行访谈"""
        if stakeholder_name not in self.stakeholders:
            raise ValueError(f"利益相关者 {stakeholder_name} 不存在")
        
        # 模拟访谈过程
        interview_record = {
            "stakeholder": stakeholder_name,
            "date": "2024-01-15",
            "questions": questions,
            "answers": [],
            "identified_requirements": []
        }
        
        # 根据角色生成模拟回答
        stakeholder = self.stakeholders[stakeholder_name]
        for question in questions:
            if "功能" in question:
                if stakeholder.role == "图书管理员":
                    answer = "需要能够管理图书信息、借阅记录、读者信息"
                elif stakeholder.role == "读者":
                    answer = "希望能够快速查找图书、在线预约、查看借阅历史"
                else:
                    answer = "需要系统稳定可靠，数据安全"
            elif "性能" in question:
                answer = "系统响应时间应该在3秒以内，支持100个并发用户"
            elif "界面" in question:
                answer = "界面要简洁易用，支持移动端访问"
            else:
                answer = "这个需要进一步讨论"
            
            interview_record["answers"].append(answer)
        
        self.interview_records.append(interview_record)
        return interview_record
    
    def create_survey(self, title: str, questions: List[str]) -> Dict[str, Any]:
        """创建调查问卷"""
        survey = {
            "title": title,
            "questions": questions,
            "responses": [],
            "analysis": {}
        }
        
        # 模拟调查结果
        sample_responses = [
            {"respondent": "读者A", "answers": ["非常重要", "经常使用", "满意", "希望增加在线续借功能"]},
            {"respondent": "读者B", "answers": ["重要", "偶尔使用", "一般", "希望改进搜索功能"]},
            {"respondent": "读者C", "answers": ["非常重要", "经常使用", "满意", "希望增加图书推荐功能"]}
        ]
        
        survey["responses"] = sample_responses
        self.survey_results.append(survey)
        
        return survey
    
    def add_requirement(self, requirement: Requirement):
        """添加需求"""
        self.requirements[requirement.id] = requirement
    
    def prioritize_requirements(self) -> List[Requirement]:
        """需求优先级排序"""
        requirements_list = list(self.requirements.values())
        return sorted(requirements_list, key=lambda r: r.calculate_priority_score(), reverse=True)
    
    def generate_requirements_matrix(self) -> Dict[str, Any]:
        """生成需求跟踪矩阵"""
        matrix = {
            "project": self.project_name,
            "total_requirements": len(self.requirements),
            "by_type": {},
            "by_priority": {},
            "by_status": {},
            "requirements": []
        }
        
        # 按类型统计
        for req_type in RequirementType:
            count = sum(1 for req in self.requirements.values() if req.requirement_type == req_type)
            matrix["by_type"][req_type.value] = count
        
        # 按优先级统计
        for priority in Priority:
            count = sum(1 for req in self.requirements.values() if req.priority == priority)
            matrix["by_priority"][priority.value] = count
        
        # 按状态统计
        for status in RequirementStatus:
            count = sum(1 for req in self.requirements.values() if req.status == status)
            matrix["by_status"][status.value] = count
        
        # 需求详情
        for req in self.requirements.values():
            matrix["requirements"].append({
                "id": req.id,
                "title": req.title,
                "type": req.requirement_type.value,
                "priority": req.priority.value,
                "status": req.status.value,
                "stakeholder": req.stakeholder,
                "business_value": req.business_value,
                "technical_risk": req.technical_risk,
                "priority_score": req.calculate_priority_score()
            })
        
        return matrix


# TODO: 练习任务
def exercise_library_system():
    """
    练习：图书馆管理系统需求分析
    
    请完成以下任务：
    1. 添加更多利益相关者（如：系统管理员、采购员等）
    2. 为每个利益相关者设计访谈问题
    3. 添加更多需求（至少10个功能性需求和5个非功能性需求）
    4. 为每个需求设置合理的优先级、业务价值和技术风险
    5. 生成需求分析报告
    """
    print("\n" + "="*60)
    print("📚 图书馆管理系统需求分析练习")
    print("="*60)
    
    # 创建需求收集器
    collector = RequirementCollector("图书馆管理系统")
    
    # TODO: 添加利益相关者
    # 示例：
    librarian = Stakeholder(
        name="张图书管理员",
        role="图书管理员",
        department="图书馆",
        contact="zhang@library.com",
        influence_level="高",
        interest_level="高"
    )
    librarian.add_expectation("系统能够提高工作效率")
    librarian.add_expectation("减少手工操作错误")
    collector.add_stakeholder(librarian)
    
    # TODO: 添加更多利益相关者
    # 提示：考虑读者、系统管理员、图书馆主任、采购员等
    
    # TODO: 进行访谈
    # 示例：
    questions = [
        "您在日常工作中最需要哪些功能？",
        "当前系统有哪些问题？",
        "对新系统的性能有什么要求？",
        "希望系统界面是什么样的？"
    ]
    interview = collector.conduct_interview("张图书管理员", questions)
    print(f"\n📋 访谈记录：{interview['stakeholder']}")
    for i, (q, a) in enumerate(zip(interview['questions'], interview['answers'])):
        print(f"   Q{i+1}: {q}")
        print(f"   A{i+1}: {a}")
    
    # TODO: 创建调查问卷
    survey_questions = [
        "图书馆系统对您的重要性？",
        "您使用图书馆系统的频率？",
        "对当前系统的满意度？",
        "希望新增哪些功能？"
    ]
    survey = collector.create_survey("图书馆系统用户满意度调查", survey_questions)
    print(f"\n📊 调查结果：{survey['title']}")
    for response in survey['responses']:
        print(f"   {response['respondent']}: {response['answers'][-1]}")
    
    # TODO: 添加需求
    # 示例需求：
    req1 = Requirement(
        id="REQ001",
        title="图书信息管理",
        description="系统应该能够添加、修改、删除和查询图书信息",
        requirement_type=RequirementType.FUNCTIONAL,
        priority=Priority.HIGH,
        status=RequirementStatus.DRAFT,
        source="访谈",
        stakeholder="张图书管理员",
        business_value=9,
        technical_risk=3,
        estimated_effort=40
    )
    req1.add_acceptance_criteria("能够录入图书基本信息（书名、作者、ISBN等）")
    req1.add_acceptance_criteria("支持图书信息的批量导入")
    req1.add_acceptance_criteria("提供图书信息的模糊查询功能")
    collector.add_requirement(req1)
    
    # TODO: 添加更多需求
    # 提示：考虑借阅管理、读者管理、统计报表、系统性能等需求
    
    # 生成需求分析报告
    matrix = collector.generate_requirements_matrix()
    print(f"\n📈 需求分析报告")
    print(f"项目：{matrix['project']}")
    print(f"总需求数：{matrix['total_requirements']}")
    
    print(f"\n按类型分布：")
    for req_type, count in matrix['by_type'].items():
        if count > 0:
            print(f"   {req_type}: {count}个")
    
    print(f"\n按优先级分布：")
    for priority, count in matrix['by_priority'].items():
        if count > 0:
            print(f"   {priority}: {count}个")
    
    # 优先级排序
    prioritized_reqs = collector.prioritize_requirements()
    print(f"\n🎯 需求优先级排序（前5个）：")
    for i, req in enumerate(prioritized_reqs[:5]):
        print(f"   {i+1}. {req.title} (分数: {req.calculate_priority_score():.2f})")
    
    print(f"\n💡 练习提示：")
    print(f"1. 尝试添加更多利益相关者和需求")
    print(f"2. 为需求设置合理的验收标准")
    print(f"3. 分析需求之间的依赖关系")
    print(f"4. 考虑非功能性需求（性能、安全、可用性等）")
    print(f"5. 评估需求的业务价值和技术风险")


def main():
    """主函数"""
    print("Session26 练习1: 需求收集与分析实践")
    print("="*80)
    
    try:
        exercise_library_system()
        
        print("\n" + "="*60)
        print("✅ 练习完成！")
        print("="*60)
        print("\n🎯 学习目标检查：")
        print("□ 理解了需求收集的基本方法")
        print("□ 学会了利益相关者分析")
        print("□ 掌握了需求优先级评估")
        print("□ 能够创建需求跟踪矩阵")
        print("□ 了解了需求管理的重要性")
        
    except Exception as e:
        print(f"❌ 练习过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()