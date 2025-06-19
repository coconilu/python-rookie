#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BMI健康计算器 - 主程序

这是Session03项目的主程序文件，实现了完整的BMI计算和健康评估功能。
本程序综合运用了算术运算符、比较运算符和逻辑运算符。

功能特性：
1. BMI计算（支持公制和英制）
2. 健康等级分类
3. 个性化健康建议
4. 数据验证和错误处理
5. 历史记录管理

作者：Python学习者
日期：2024年
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union


class BMICalculator:
    """
    BMI计算器类
    
    提供BMI计算、分类、建议等功能
    """
    
    # BMI分类标准（WHO标准）
    WHO_CATEGORIES = {
        'underweight': (0, 18.5),
        'normal': (18.5, 25.0),
        'overweight': (25.0, 30.0),
        'obese': (30.0, float('inf'))
    }
    
    # 亚洲人群标准
    ASIAN_CATEGORIES = {
        'underweight': (0, 18.5),
        'normal': (18.5, 23.0),
        'overweight': (23.0, 27.5),
        'obese': (27.5, float('inf'))
    }
    
    # 中文分类名称
    CATEGORY_NAMES = {
        'underweight': '偏瘦',
        'normal': '正常',
        'overweight': '偏胖',
        'obese': '肥胖'
    }
    
    def __init__(self, use_asian_standard: bool = False):
        """
        初始化BMI计算器
        
        参数:
            use_asian_standard (bool): 是否使用亚洲人群标准
        """
        self.categories = self.ASIAN_CATEGORIES if use_asian_standard else self.WHO_CATEGORIES
        self.standard_name = "亚洲标准" if use_asian_standard else "WHO标准"
    
    def calculate_bmi(self, weight: float, height: float, unit: str = 'metric') -> float:
        """
        计算BMI值
        
        参数:
            weight (float): 体重
            height (float): 身高
            unit (str): 单位系统 ('metric' 或 'imperial')
        
        返回:
            float: BMI值
        
        异常:
            ValueError: 当输入值无效时
        """
        # 验证输入
        if not self._validate_measurements(weight, height, unit):
            raise ValueError("输入的体重或身高数值无效")
        
        # 单位转换
        if unit == 'imperial':
            # 英制转公制：磅转公斤，英寸转米
            weight_kg = weight * 0.453592  # 1磅 = 0.453592公斤
            height_m = height * 0.0254     # 1英寸 = 0.0254米
        else:
            # 公制单位
            weight_kg = weight
            height_m = height
        
        # BMI计算公式：BMI = 体重(kg) / 身高²(m²)
        bmi = weight_kg / (height_m ** 2)
        
        return round(bmi, 2)
    
    def classify_bmi(self, bmi: float) -> Tuple[str, str]:
        """
        根据BMI值进行分类
        
        参数:
            bmi (float): BMI值
        
        返回:
            Tuple[str, str]: (英文分类, 中文分类)
        """
        for category, (min_val, max_val) in self.categories.items():
            if min_val <= bmi < max_val:
                return category, self.CATEGORY_NAMES[category]
        
        # 如果没有匹配到任何分类，返回肥胖
        return 'obese', self.CATEGORY_NAMES['obese']
    
    def get_health_advice(self, bmi: float, age: int, gender: str, 
                         activity_level: str = 'moderate') -> Dict[str, Union[str, List[str]]]:
        """
        根据BMI和个人信息生成健康建议
        
        参数:
            bmi (float): BMI值
            age (int): 年龄
            gender (str): 性别 ('male' 或 'female')
            activity_level (str): 活动水平 ('low', 'moderate', 'high')
        
        返回:
            Dict: 包含健康建议的字典
        """
        category, category_name = self.classify_bmi(bmi)
        
        advice = {
            'category': category_name,
            'bmi_value': bmi,
            'standard': self.standard_name,
            'general_advice': '',
            'diet_tips': [],
            'exercise_tips': [],
            'health_risks': [],
            'target_weight_range': self._calculate_target_weight_range(bmi)
        }
        
        # 根据BMI分类提供建议
        if category == 'underweight':
            advice['general_advice'] = "您的体重偏轻，建议适当增重以达到健康体重范围。"
            advice['diet_tips'] = [
                "增加健康的高热量食物摄入",
                "多吃坚果、牛油果、全谷物",
                "少食多餐，增加营养密度",
                "适当补充蛋白质"
            ]
            advice['exercise_tips'] = [
                "进行力量训练增加肌肉量",
                "避免过度有氧运动",
                "注重核心肌群训练"
            ]
            
        elif category == 'normal':
            advice['general_advice'] = "恭喜！您的体重在健康范围内，请继续保持良好的生活习惯。"
            advice['diet_tips'] = [
                "保持均衡饮食",
                "多吃蔬菜水果",
                "控制加工食品摄入",
                "保持规律的饮食时间"
            ]
            advice['exercise_tips'] = [
                "每周至少150分钟中等强度运动",
                "结合有氧运动和力量训练",
                "保持运动的多样性"
            ]
            
        elif category == 'overweight':
            advice['general_advice'] = "您的体重略高于正常范围，建议适当减重以降低健康风险。"
            advice['diet_tips'] = [
                "控制总热量摄入",
                "减少高糖高脂食物",
                "增加蔬菜和蛋白质比例",
                "注意饮食份量控制"
            ]
            advice['exercise_tips'] = [
                "增加有氧运动时间",
                "每周至少300分钟中等强度运动",
                "加入力量训练维持肌肉量"
            ]
            advice['health_risks'] = [
                "心血管疾病风险增加",
                "2型糖尿病风险上升"
            ]
            
        elif category == 'obese':
            advice['general_advice'] = "您的体重超出健康范围较多，强烈建议咨询医生制定减重计划。"
            advice['diet_tips'] = [
                "严格控制热量摄入",
                "避免高热量密度食物",
                "增加膳食纤维摄入",
                "考虑寻求营养师指导"
            ]
            advice['exercise_tips'] = [
                "从低强度运动开始",
                "逐步增加运动时间和强度",
                "选择对关节友好的运动",
                "建议在专业指导下运动"
            ]
            advice['health_risks'] = [
                "心血管疾病高风险",
                "2型糖尿病高风险",
                "高血压风险",
                "睡眠呼吸暂停风险",
                "某些癌症风险增加"
            ]
        
        # 根据年龄调整建议
        if age >= 65:
            advice['exercise_tips'].append("注重平衡性训练预防跌倒")
            advice['diet_tips'].append("确保充足的钙和维生素D摄入")
        elif age < 18:
            advice['general_advice'] += " 建议在家长和医生指导下进行任何体重管理。"
        
        # 根据性别调整建议
        if gender == 'female':
            advice['diet_tips'].append("注意铁质和叶酸的摄入")
        
        return advice
    
    def _validate_measurements(self, weight: float, height: float, unit: str) -> bool:
        """
        验证体重和身高数据的合理性
        
        参数:
            weight (float): 体重
            height (float): 身高
            unit (str): 单位系统
        
        返回:
            bool: 数据是否有效
        """
        if unit == 'metric':
            # 公制：体重1-1000kg，身高0.5-3.0m
            weight_valid = 1 <= weight <= 1000
            height_valid = 0.5 <= height <= 3.0
        elif unit == 'imperial':
            # 英制：体重2-2200磅，身高20-120英寸
            weight_valid = 2 <= weight <= 2200
            height_valid = 20 <= height <= 120
        else:
            return False
        
        return weight_valid and height_valid
    
    def _calculate_target_weight_range(self, current_bmi: float) -> Optional[str]:
        """
        计算目标体重范围建议
        
        参数:
            current_bmi (float): 当前BMI值
        
        返回:
            Optional[str]: 目标体重建议
        """
        normal_range = self.categories['normal']
        
        if normal_range[0] <= current_bmi < normal_range[1]:
            return "您的体重已在健康范围内"
        elif current_bmi < normal_range[0]:
            return f"建议将BMI提高到{normal_range[0]}以上"
        else:
            return f"建议将BMI降低到{normal_range[1]}以下"


class HealthDataManager:
    """
    健康数据管理器
    
    负责用户数据的保存、加载和管理
    """
    
    def __init__(self, data_file: str = 'data/user_data.json'):
        """
        初始化数据管理器
        
        参数:
            data_file (str): 数据文件路径
        """
        self.data_file = data_file
        self._ensure_data_directory()
    
    def save_record(self, user_id: str, weight: float, height: float, 
                   bmi: float, category: str, unit: str = 'metric') -> bool:
        """
        保存用户健康记录
        
        参数:
            user_id (str): 用户ID
            weight (float): 体重
            height (float): 身高
            bmi (float): BMI值
            category (str): BMI分类
            unit (str): 单位系统
        
        返回:
            bool: 保存是否成功
        """
        try:
            # 加载现有数据
            data = self._load_data()
            
            # 创建新记录
            record = {
                'timestamp': datetime.now().isoformat(),
                'weight': weight,
                'height': height,
                'bmi': bmi,
                'category': category,
                'unit': unit
            }
            
            # 添加到用户数据
            if user_id not in data:
                data[user_id] = {'records': []}
            
            data[user_id]['records'].append(record)
            
            # 保存数据
            return self._save_data(data)
            
        except Exception as e:
            print(f"保存数据时出错: {e}")
            return False
    
    def load_user_history(self, user_id: str) -> List[Dict]:
        """
        加载用户历史记录
        
        参数:
            user_id (str): 用户ID
        
        返回:
            List[Dict]: 用户历史记录列表
        """
        try:
            data = self._load_data()
            return data.get(user_id, {}).get('records', [])
        except Exception as e:
            print(f"加载数据时出错: {e}")
            return []
    
    def analyze_trend(self, user_id: str) -> Dict[str, Union[str, float, List]]:
        """
        分析用户BMI趋势
        
        参数:
            user_id (str): 用户ID
        
        返回:
            Dict: 趋势分析结果
        """
        records = self.load_user_history(user_id)
        
        if len(records) < 2:
            return {'error': '需要至少2条记录才能分析趋势'}
        
        # 按时间排序
        sorted_records = sorted(records, key=lambda x: x['timestamp'])
        
        # 计算趋势
        first_bmi = sorted_records[0]['bmi']
        last_bmi = sorted_records[-1]['bmi']
        bmi_change = last_bmi - first_bmi
        
        # 计算平均BMI
        avg_bmi = sum(record['bmi'] for record in sorted_records) / len(sorted_records)
        
        # 确定趋势方向
        if bmi_change > 0.5:
            trend = '上升'
        elif bmi_change < -0.5:
            trend = '下降'
        else:
            trend = '稳定'
        
        return {
            'total_records': len(sorted_records),
            'first_bmi': first_bmi,
            'last_bmi': last_bmi,
            'bmi_change': round(bmi_change, 2),
            'average_bmi': round(avg_bmi, 2),
            'trend': trend,
            'records': sorted_records
        }
    
    def _ensure_data_directory(self):
        """
        确保数据目录存在
        """
        data_dir = os.path.dirname(self.data_file)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def _load_data(self) -> Dict:
        """
        从文件加载数据
        
        返回:
            Dict: 用户数据字典
        """
        if not os.path.exists(self.data_file):
            return {}
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    
    def _save_data(self, data: Dict) -> bool:
        """
        保存数据到文件
        
        参数:
            data (Dict): 要保存的数据
        
        返回:
            bool: 保存是否成功
        """
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except IOError:
            return False


def get_user_input() -> Dict[str, Union[str, float, int]]:
    """
    获取用户输入
    
    返回:
        Dict: 用户输入的数据
    """
    print("\n=== BMI健康计算器 ===")
    print("请输入您的基本信息：")
    
    # 获取用户ID
    user_id = input("请输入您的用户名（用于保存记录）: ").strip()
    if not user_id:
        user_id = "anonymous"
    
    # 选择单位系统
    while True:
        unit_choice = input("请选择单位系统 (1-公制kg/m, 2-英制lb/in): ").strip()
        if unit_choice == '1':
            unit = 'metric'
            break
        elif unit_choice == '2':
            unit = 'imperial'
            break
        else:
            print("请输入1或2")
    
    # 获取体重和身高
    while True:
        try:
            if unit == 'metric':
                weight = float(input("请输入您的体重（公斤）: "))
                height = float(input("请输入您的身高（米）: "))
            else:
                weight = float(input("请输入您的体重（磅）: "))
                height = float(input("请输入您的身高（英寸）: "))
            break
        except ValueError:
            print("请输入有效的数字")
    
    # 获取年龄
    while True:
        try:
            age = int(input("请输入您的年龄: "))
            if 1 <= age <= 150:
                break
            else:
                print("请输入有效的年龄（1-150）")
        except ValueError:
            print("请输入有效的数字")
    
    # 获取性别
    while True:
        gender_choice = input("请选择性别 (1-男性, 2-女性): ").strip()
        if gender_choice == '1':
            gender = 'male'
            break
        elif gender_choice == '2':
            gender = 'female'
            break
        else:
            print("请输入1或2")
    
    # 获取活动水平
    while True:
        activity_choice = input("请选择活动水平 (1-低, 2-中等, 3-高): ").strip()
        if activity_choice == '1':
            activity_level = 'low'
            break
        elif activity_choice == '2':
            activity_level = 'moderate'
            break
        elif activity_choice == '3':
            activity_level = 'high'
            break
        else:
            print("请输入1、2或3")
    
    # 选择BMI标准
    while True:
        standard_choice = input("请选择BMI标准 (1-WHO标准, 2-亚洲标准): ").strip()
        if standard_choice == '1':
            use_asian_standard = False
            break
        elif standard_choice == '2':
            use_asian_standard = True
            break
        else:
            print("请输入1或2")
    
    return {
        'user_id': user_id,
        'weight': weight,
        'height': height,
        'age': age,
        'gender': gender,
        'activity_level': activity_level,
        'unit': unit,
        'use_asian_standard': use_asian_standard
    }


def display_results(bmi: float, advice: Dict, calculator: BMICalculator):
    """
    显示计算结果和健康建议
    
    参数:
        bmi (float): BMI值
        advice (Dict): 健康建议
        calculator (BMICalculator): BMI计算器实例
    """
    print("\n" + "="*50)
    print("BMI计算结果")
    print("="*50)
    
    print(f"您的BMI值: {bmi}")
    print(f"健康分类: {advice['category']}")
    print(f"评估标准: {advice['standard']}")
    print(f"\n总体建议: {advice['general_advice']}")
    
    if advice['target_weight_range']:
        print(f"目标建议: {advice['target_weight_range']}")
    
    # 显示饮食建议
    if advice['diet_tips']:
        print("\n饮食建议:")
        for i, tip in enumerate(advice['diet_tips'], 1):
            print(f"  {i}. {tip}")
    
    # 显示运动建议
    if advice['exercise_tips']:
        print("\n运动建议:")
        for i, tip in enumerate(advice['exercise_tips'], 1):
            print(f"  {i}. {tip}")
    
    # 显示健康风险
    if advice['health_risks']:
        print("\n⚠️  健康风险提醒:")
        for i, risk in enumerate(advice['health_risks'], 1):
            print(f"  {i}. {risk}")
    
    print("\n" + "="*50)


def display_history(trend_analysis: Dict):
    """
    显示历史记录和趋势分析
    
    参数:
        trend_analysis (Dict): 趋势分析结果
    """
    if 'error' in trend_analysis:
        print(f"\n历史记录: {trend_analysis['error']}")
        return
    
    print("\n" + "="*50)
    print("历史记录和趋势分析")
    print("="*50)
    
    print(f"总记录数: {trend_analysis['total_records']}")
    print(f"首次BMI: {trend_analysis['first_bmi']}")
    print(f"最新BMI: {trend_analysis['last_bmi']}")
    print(f"BMI变化: {trend_analysis['bmi_change']:+.2f}")
    print(f"平均BMI: {trend_analysis['average_bmi']}")
    print(f"趋势方向: {trend_analysis['trend']}")
    
    # 显示最近几条记录
    recent_records = trend_analysis['records'][-5:]  # 最近5条记录
    print("\n最近记录:")
    for record in recent_records:
        date = datetime.fromisoformat(record['timestamp']).strftime('%Y-%m-%d %H:%M')
        print(f"  {date}: BMI {record['bmi']} ({record['category']})")
    
    print("\n" + "="*50)


def main():
    """
    主函数
    """
    try:
        # 获取用户输入
        user_data = get_user_input()
        
        # 创建BMI计算器
        calculator = BMICalculator(use_asian_standard=user_data['use_asian_standard'])
        
        # 计算BMI
        bmi = calculator.calculate_bmi(
            weight=user_data['weight'],
            height=user_data['height'],
            unit=user_data['unit']
        )
        
        # 获取健康建议
        advice = calculator.get_health_advice(
            bmi=bmi,
            age=user_data['age'],
            gender=user_data['gender'],
            activity_level=user_data['activity_level']
        )
        
        # 显示结果
        display_results(bmi, advice, calculator)
        
        # 保存记录
        data_manager = HealthDataManager()
        category, _ = calculator.classify_bmi(bmi)
        
        save_success = data_manager.save_record(
            user_id=user_data['user_id'],
            weight=user_data['weight'],
            height=user_data['height'],
            bmi=bmi,
            category=advice['category'],
            unit=user_data['unit']
        )
        
        if save_success:
            print("\n✅ 记录已保存")
        else:
            print("\n❌ 记录保存失败")
        
        # 显示历史记录
        trend_analysis = data_manager.analyze_trend(user_data['user_id'])
        display_history(trend_analysis)
        
        # 询问是否继续
        while True:
            continue_choice = input("\n是否继续计算？(y/n): ").strip().lower()
            if continue_choice in ['y', 'yes', '是']:
                main()  # 递归调用
                break
            elif continue_choice in ['n', 'no', '否']:
                print("\n感谢使用BMI健康计算器！祝您身体健康！")
                break
            else:
                print("请输入 y 或 n")
    
    except ValueError as e:
        print(f"\n❌ 输入错误: {e}")
        print("请检查您的输入并重试。")
    except KeyboardInterrupt:
        print("\n\n程序已退出。")
    except Exception as e:
        print(f"\n❌ 程序出现错误: {e}")
        print("请联系开发者或重新启动程序。")


if __name__ == "__main__":
    main()