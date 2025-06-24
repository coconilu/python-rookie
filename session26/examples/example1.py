#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session26 示例1: 需求收集技术演示

本示例演示了不同的需求收集技术：
1. 访谈法
2. 问卷调查法
3. 观察法
4. 头脑风暴法

作者: Python教程团队
创建日期: 2024-01-15
"""

import json
import random
from typing import List, Dict, Any
from datetime import datetime, timedelta


class InterviewTechnique:
    """访谈法需求收集"""
    
    def __init__(self):
        self.interview_data = []
    
    def conduct_interview(self, stakeholder: str, questions: List[str]) -> Dict[str, Any]:
        """进行访谈"""
        print(f"\n🎤 正在访谈: {stakeholder}")
        print("-" * 40)
        
        interview_record = {
            "stakeholder": stakeholder,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "questions_and_answers": [],
            "key_requirements": [],
            "concerns": []
        }
        
        # 模拟访谈过程
        sample_answers = {
            "请描述您的业务流程": "我们需要一个在线商城来销售产品，用户可以浏览、搜索、购买商品",
            "目前遇到的主要问题是什么？": "现有系统响应慢，用户体验差，订单处理效率低",
            "期望通过系统解决什么问题？": "提高用户体验，增加销售额，简化订单管理流程",
            "对系统性能有什么要求？": "页面加载时间不超过2秒，支持1000个并发用户",
            "预算和时间限制是什么？": "预算50万，希望3个月内上线"
        }
        
        for question in questions:
            answer = sample_answers.get(question, "这个问题需要进一步讨论")
            interview_record["questions_and_answers"].append({
                "question": question,
                "answer": answer
            })
            print(f"Q: {question}")
            print(f"A: {answer}\n")
        
        # 提取关键需求
        if "商城" in str(interview_record["questions_and_answers"]):
            interview_record["key_requirements"].extend([
                "用户注册登录功能",
                "商品浏览和搜索功能",
                "购物车功能",
                "订单管理功能",
                "支付功能"
            ])
        
        # 识别关注点
        if "性能" in str(interview_record["questions_and_answers"]):
            interview_record["concerns"].append("系统性能要求")
        if "时间" in str(interview_record["questions_and_answers"]):
            interview_record["concerns"].append("项目时间限制")
        
        self.interview_data.append(interview_record)
        return interview_record
    
    def analyze_interviews(self) -> Dict[str, Any]:
        """分析访谈结果"""
        all_requirements = []
        all_concerns = []
        
        for interview in self.interview_data:
            all_requirements.extend(interview["key_requirements"])
            all_concerns.extend(interview["concerns"])
        
        # 统计需求频次
        requirement_frequency = {}
        for req in all_requirements:
            requirement_frequency[req] = requirement_frequency.get(req, 0) + 1
        
        # 统计关注点频次
        concern_frequency = {}
        for concern in all_concerns:
            concern_frequency[concern] = concern_frequency.get(concern, 0) + 1
        
        return {
            "total_interviews": len(self.interview_data),
            "requirement_frequency": requirement_frequency,
            "concern_frequency": concern_frequency,
            "top_requirements": sorted(requirement_frequency.items(), 
                                     key=lambda x: x[1], reverse=True)[:5],
            "top_concerns": sorted(concern_frequency.items(), 
                                 key=lambda x: x[1], reverse=True)[:3]
        }


class SurveyTechnique:
    """问卷调查法需求收集"""
    
    def __init__(self):
        self.survey_responses = []
    
    def create_survey(self, title: str, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """创建问卷"""
        survey = {
            "title": title,
            "created_date": datetime.now().strftime("%Y-%m-%d"),
            "questions": questions,
            "responses": []
        }
        return survey
    
    def simulate_responses(self, survey: Dict[str, Any], num_responses: int = 100) -> None:
        """模拟问卷回答"""
        print(f"\n📊 模拟 {num_responses} 份问卷回答...")
        
        # 模拟不同类型的回答
        age_groups = ["18-25", "26-35", "36-45", "46+"]
        occupations = ["学生", "上班族", "自由职业", "其他"]
        tech_levels = ["初级", "中级", "高级"]
        shopping_frequencies = ["每天", "每周", "每月", "偶尔"]
        devices = ["手机", "电脑", "平板", "都用"]
        payment_methods = ["支付宝", "微信", "银行卡", "其他"]
        important_features = ["搜索", "推荐", "比价", "评价"]
        
        for i in range(num_responses):
            response = {
                "response_id": f"R{i+1:03d}",
                "timestamp": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d %H:%M:%S"),
                "answers": {
                    "年龄段": random.choice(age_groups),
                    "职业": random.choice(occupations),
                    "技术水平": random.choice(tech_levels),
                    "购物频率": random.choice(shopping_frequencies),
                    "设备偏好": random.choice(devices),
                    "支付方式": random.choice(payment_methods),
                    "最重要功能": random.choice(important_features),
                    "满意度评分": random.randint(1, 10)
                }
            }
            survey["responses"].append(response)
        
        self.survey_responses = survey["responses"]
        print(f"✅ 已收集 {len(self.survey_responses)} 份有效回答")
    
    def analyze_survey_results(self) -> Dict[str, Any]:
        """分析问卷结果"""
        if not self.survey_responses:
            return {"error": "没有问卷数据"}
        
        analysis = {
            "total_responses": len(self.survey_responses),
            "demographics": {},
            "preferences": {},
            "satisfaction": {}
        }
        
        # 分析人口统计信息
        age_distribution = {}
        occupation_distribution = {}
        tech_distribution = {}
        
        for response in self.survey_responses:
            answers = response["answers"]
            
            # 年龄分布
            age = answers["年龄段"]
            age_distribution[age] = age_distribution.get(age, 0) + 1
            
            # 职业分布
            occupation = answers["职业"]
            occupation_distribution[occupation] = occupation_distribution.get(occupation, 0) + 1
            
            # 技术水平分布
            tech_level = answers["技术水平"]
            tech_distribution[tech_level] = tech_distribution.get(tech_level, 0) + 1
        
        analysis["demographics"] = {
            "age_distribution": age_distribution,
            "occupation_distribution": occupation_distribution,
            "tech_distribution": tech_distribution
        }
        
        # 分析用户偏好
        device_preferences = {}
        payment_preferences = {}
        feature_preferences = {}
        
        for response in self.survey_responses:
            answers = response["answers"]
            
            device = answers["设备偏好"]
            device_preferences[device] = device_preferences.get(device, 0) + 1
            
            payment = answers["支付方式"]
            payment_preferences[payment] = payment_preferences.get(payment, 0) + 1
            
            feature = answers["最重要功能"]
            feature_preferences[feature] = feature_preferences.get(feature, 0) + 1
        
        analysis["preferences"] = {
            "device_preferences": device_preferences,
            "payment_preferences": payment_preferences,
            "feature_preferences": feature_preferences
        }
        
        # 分析满意度
        satisfaction_scores = [response["answers"]["满意度评分"] for response in self.survey_responses]
        analysis["satisfaction"] = {
            "average_score": round(sum(satisfaction_scores) / len(satisfaction_scores), 2),
            "min_score": min(satisfaction_scores),
            "max_score": max(satisfaction_scores),
            "score_distribution": {str(i): satisfaction_scores.count(i) for i in range(1, 11)}
        }
        
        return analysis


class ObservationTechnique:
    """观察法需求收集"""
    
    def __init__(self):
        self.observation_logs = []
    
    def conduct_observation(self, user_id: str, session_duration: int = 30) -> Dict[str, Any]:
        """进行用户行为观察"""
        print(f"\n👀 观察用户 {user_id} 的行为 ({session_duration}分钟)...")
        
        # 模拟用户行为序列
        possible_actions = [
            "访问首页",
            "搜索商品",
            "浏览商品详情",
            "查看商品评价",
            "比较商品价格",
            "加入购物车",
            "查看购物车",
            "修改商品数量",
            "删除购物车商品",
            "进入结算页面",
            "填写收货信息",
            "选择支付方式",
            "完成支付",
            "返回上一页",
            "退出系统"
        ]
        
        action_sequence = []
        current_time = 0
        
        while current_time < session_duration * 60:  # 转换为秒
            action = random.choice(possible_actions)
            duration = random.randint(5, 120)  # 5秒到2分钟
            
            action_sequence.append({
                "timestamp": current_time,
                "action": action,
                "duration": duration,
                "page_load_time": random.uniform(0.5, 5.0)  # 页面加载时间
            })
            
            current_time += duration
            
            if current_time >= session_duration * 60:
                break
        
        # 识别用户痛点
        pain_points = []
        for action in action_sequence:
            if action["page_load_time"] > 3.0:
                pain_points.append(f"{action['action']}页面加载慢")
            if action["duration"] > 90 and "搜索" in action["action"]:
                pain_points.append("搜索结果不够精准")
            if action["action"] == "返回上一页" and action["duration"] < 10:
                pain_points.append("用户快速离开页面")
        
        observation_log = {
            "user_id": user_id,
            "session_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "session_duration": session_duration,
            "action_sequence": action_sequence,
            "total_actions": len(action_sequence),
            "pain_points": list(set(pain_points)),  # 去重
            "user_efficiency": len(action_sequence) / (session_duration / 60)  # 每分钟操作数
        }
        
        self.observation_logs.append(observation_log)
        
        # 显示观察结果
        print(f"📝 观察结果:")
        print(f"   总操作数: {observation_log['total_actions']}")
        print(f"   操作效率: {observation_log['user_efficiency']:.1f} 操作/分钟")
        print(f"   发现痛点: {len(observation_log['pain_points'])}个")
        for pain_point in observation_log['pain_points']:
            print(f"     - {pain_point}")
        
        return observation_log
    
    def analyze_observations(self) -> Dict[str, Any]:
        """分析观察结果"""
        if not self.observation_logs:
            return {"error": "没有观察数据"}
        
        all_pain_points = []
        all_actions = []
        efficiency_scores = []
        
        for log in self.observation_logs:
            all_pain_points.extend(log["pain_points"])
            all_actions.extend([action["action"] for action in log["action_sequence"]])
            efficiency_scores.append(log["user_efficiency"])
        
        # 统计痛点频次
        pain_point_frequency = {}
        for pain_point in all_pain_points:
            pain_point_frequency[pain_point] = pain_point_frequency.get(pain_point, 0) + 1
        
        # 统计操作频次
        action_frequency = {}
        for action in all_actions:
            action_frequency[action] = action_frequency.get(action, 0) + 1
        
        return {
            "total_observations": len(self.observation_logs),
            "average_efficiency": round(sum(efficiency_scores) / len(efficiency_scores), 2),
            "top_pain_points": sorted(pain_point_frequency.items(), 
                                    key=lambda x: x[1], reverse=True)[:5],
            "most_common_actions": sorted(action_frequency.items(), 
                                        key=lambda x: x[1], reverse=True)[:10],
            "improvement_suggestions": [
                "优化页面加载速度",
                "改进搜索算法",
                "简化操作流程",
                "增加用户引导"
            ]
        }


class BrainstormingTechnique:
    """头脑风暴法需求收集"""
    
    def __init__(self):
        self.brainstorming_sessions = []
    
    def conduct_brainstorming(self, topic: str, participants: List[str], 
                            duration: int = 60) -> Dict[str, Any]:
        """进行头脑风暴会议"""
        print(f"\n🧠 头脑风暴会议: {topic}")
        print(f"参与者: {', '.join(participants)}")
        print(f"会议时长: {duration}分钟")
        print("-" * 50)
        
        # 模拟头脑风暴产生的想法
        sample_ideas = [
            "增加语音搜索功能",
            "实现AR试穿功能",
            "添加社交分享功能",
            "集成智能推荐系统",
            "支持多语言界面",
            "增加会员积分系统",
            "实现一键下单功能",
            "添加商品比价功能",
            "支持分期付款",
            "增加客服聊天机器人",
            "实现个性化首页",
            "添加商品收藏功能",
            "支持团购功能",
            "增加用户评价系统",
            "实现快速退换货",
            "添加优惠券系统",
            "支持直播购物",
            "增加商品问答功能",
            "实现智能客服",
            "添加购物助手功能"
        ]
        
        # 随机选择一些想法作为会议结果
        num_ideas = random.randint(8, 15)
        session_ideas = random.sample(sample_ideas, num_ideas)
        
        # 为每个想法分配提出者和优先级
        ideas_with_details = []
        for idea in session_ideas:
            ideas_with_details.append({
                "idea": idea,
                "proposer": random.choice(participants),
                "priority": random.choice(["高", "中", "低"]),
                "feasibility": random.choice(["容易", "中等", "困难"]),
                "estimated_effort": random.randint(1, 20)  # 人天
            })
        
        session_record = {
            "topic": topic,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "participants": participants,
            "duration": duration,
            "ideas": ideas_with_details,
            "total_ideas": len(ideas_with_details)
        }
        
        self.brainstorming_sessions.append(session_record)
        
        # 显示会议结果
        print(f"💡 产生想法: {len(ideas_with_details)}个")
        for i, idea_detail in enumerate(ideas_with_details, 1):
            print(f"{i:2d}. {idea_detail['idea']}")
            print(f"     提出者: {idea_detail['proposer']} | "
                  f"优先级: {idea_detail['priority']} | "
                  f"可行性: {idea_detail['feasibility']}")
        
        return session_record
    
    def prioritize_ideas(self, session_index: int = -1) -> List[Dict[str, Any]]:
        """对想法进行优先级排序"""
        if not self.brainstorming_sessions:
            return []
        
        session = self.brainstorming_sessions[session_index]
        ideas = session["ideas"]
        
        # 按优先级和可行性排序
        priority_weight = {"高": 3, "中": 2, "低": 1}
        feasibility_weight = {"容易": 3, "中等": 2, "困难": 1}
        
        for idea in ideas:
            idea["score"] = (priority_weight[idea["priority"]] + 
                           feasibility_weight[idea["feasibility"]]) / 2
        
        sorted_ideas = sorted(ideas, key=lambda x: x["score"], reverse=True)
        
        print(f"\n🏆 想法优先级排序:")
        for i, idea in enumerate(sorted_ideas[:10], 1):
            print(f"{i:2d}. {idea['idea']} (评分: {idea['score']:.1f})")
        
        return sorted_ideas


def demo_interview_technique():
    """演示访谈法"""
    print("\n" + "="*60)
    print("🎤 访谈法需求收集演示")
    print("="*60)
    
    interview = InterviewTechnique()
    
    # 定义访谈问题
    business_questions = [
        "请描述您的业务流程",
        "目前遇到的主要问题是什么？",
        "期望通过系统解决什么问题？"
    ]
    
    technical_questions = [
        "对系统性能有什么要求？",
        "预算和时间限制是什么？",
        "有哪些技术约束？"
    ]
    
    # 进行多个访谈
    stakeholders = [
        ("产品经理", business_questions),
        ("技术总监", technical_questions),
        ("运营经理", business_questions[:2] + ["用户反馈的主要问题是什么？"])
    ]
    
    for stakeholder, questions in stakeholders:
        interview.conduct_interview(stakeholder, questions)
    
    # 分析访谈结果
    analysis = interview.analyze_interviews()
    print(f"\n📊 访谈分析结果:")
    print(f"总访谈次数: {analysis['total_interviews']}")
    print(f"\n🔥 高频需求:")
    for req, freq in analysis['top_requirements']:
        print(f"   {req}: {freq}次提及")
    print(f"\n⚠️ 主要关注点:")
    for concern, freq in analysis['top_concerns']:
        print(f"   {concern}: {freq}次提及")


def demo_survey_technique():
    """演示问卷调查法"""
    print("\n" + "="*60)
    print("📊 问卷调查法需求收集演示")
    print("="*60)
    
    survey = SurveyTechnique()
    
    # 创建问卷
    questions = [
        {"type": "single_choice", "question": "您的年龄段", "options": ["18-25", "26-35", "36-45", "46+"]},
        {"type": "single_choice", "question": "您的职业", "options": ["学生", "上班族", "自由职业", "其他"]},
        {"type": "single_choice", "question": "您的技术水平", "options": ["初级", "中级", "高级"]},
        {"type": "single_choice", "question": "购物频率", "options": ["每天", "每周", "每月", "偶尔"]},
        {"type": "single_choice", "question": "设备偏好", "options": ["手机", "电脑", "平板", "都用"]},
        {"type": "single_choice", "question": "支付方式", "options": ["支付宝", "微信", "银行卡", "其他"]},
        {"type": "single_choice", "question": "最重要功能", "options": ["搜索", "推荐", "比价", "评价"]},
        {"type": "rating", "question": "满意度评分", "scale": "1-10"}
    ]
    
    user_survey = survey.create_survey("在线商城用户需求调查", questions)
    
    # 模拟收集回答
    survey.simulate_responses(user_survey, 150)
    
    # 分析结果
    analysis = survey.analyze_survey_results()
    
    print(f"\n📈 问卷分析结果:")
    print(f"总回答数: {analysis['total_responses']}")
    
    print(f"\n👥 用户画像:")
    print(f"年龄分布: {analysis['demographics']['age_distribution']}")
    print(f"职业分布: {analysis['demographics']['occupation_distribution']}")
    
    print(f"\n💡 用户偏好:")
    print(f"设备偏好: {analysis['preferences']['device_preferences']}")
    print(f"功能偏好: {analysis['preferences']['feature_preferences']}")
    
    print(f"\n😊 满意度:")
    print(f"平均评分: {analysis['satisfaction']['average_score']}/10")


def demo_observation_technique():
    """演示观察法"""
    print("\n" + "="*60)
    print("👀 观察法需求收集演示")
    print("="*60)
    
    observation = ObservationTechnique()
    
    # 观察多个用户
    users = ["User001", "User002", "User003", "User004", "User005"]
    
    for user_id in users:
        session_duration = random.randint(15, 45)  # 15-45分钟
        observation.conduct_observation(user_id, session_duration)
    
    # 分析观察结果
    analysis = observation.analyze_observations()
    
    print(f"\n📊 观察分析结果:")
    print(f"总观察次数: {analysis['total_observations']}")
    print(f"平均操作效率: {analysis['average_efficiency']} 操作/分钟")
    
    print(f"\n🔥 主要痛点:")
    for pain_point, freq in analysis['top_pain_points']:
        print(f"   {pain_point}: {freq}次观察到")
    
    print(f"\n📱 常见操作:")
    for action, freq in analysis['most_common_actions'][:5]:
        print(f"   {action}: {freq}次")
    
    print(f"\n💡 改进建议:")
    for suggestion in analysis['improvement_suggestions']:
        print(f"   - {suggestion}")


def demo_brainstorming_technique():
    """演示头脑风暴法"""
    print("\n" + "="*60)
    print("🧠 头脑风暴法需求收集演示")
    print("="*60)
    
    brainstorming = BrainstormingTechnique()
    
    # 进行头脑风暴会议
    participants = ["产品经理", "UI设计师", "前端工程师", "后端工程师", "测试工程师"]
    
    session = brainstorming.conduct_brainstorming(
        "在线商城创新功能设计", 
        participants, 
        90
    )
    
    # 对想法进行优先级排序
    brainstorming.prioritize_ideas()


def main():
    """主函数：演示各种需求收集技术"""
    print("Session26 示例1: 需求收集技术演示")
    print("=" * 60)
    print("本示例展示了四种主要的需求收集技术：")
    print("1. 访谈法 - 深度了解利益相关者需求")
    print("2. 问卷调查法 - 大规模收集用户反馈")
    print("3. 观察法 - 发现用户真实行为模式")
    print("4. 头脑风暴法 - 激发创新想法")
    
    try:
        # 演示各种技术
        demo_interview_technique()
        demo_survey_technique()
        demo_observation_technique()
        demo_brainstorming_technique()
        
        print("\n" + "="*60)
        print("🎉 需求收集技术演示完成！")
        print("="*60)
        print("\n💡 关键要点:")
        print("✅ 访谈法适合深度需求挖掘")
        print("✅ 问卷调查适合大规模数据收集")
        print("✅ 观察法能发现隐性需求")
        print("✅ 头脑风暴能激发创新思维")
        print("\n🔧 实践建议:")
        print("• 结合多种方法使用")
        print("• 针对不同利益相关者选择合适方法")
        print("• 持续验证和完善需求")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        print("请检查代码并重试。")


if __name__ == "__main__":
    main()