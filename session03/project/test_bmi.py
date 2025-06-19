#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BMI计算器测试文件

这个文件包含了对BMI计算器各项功能的测试用例，
帮助验证程序的正确性和健壮性。

测试内容：
1. BMI计算功能测试
2. 分类功能测试
3. 数据验证测试
4. 边界值测试
5. 异常处理测试

作者：Python学习者
日期：2024年
"""

import unittest
import os
import json
import tempfile
from bmi_calculator import BMICalculator, HealthDataManager


class TestBMICalculator(unittest.TestCase):
    """
    BMI计算器测试类
    """
    
    def setUp(self):
        """
        测试前的准备工作
        """
        self.calculator_who = BMICalculator(use_asian_standard=False)
        self.calculator_asian = BMICalculator(use_asian_standard=True)
    
    def test_bmi_calculation_metric(self):
        """
        测试公制单位BMI计算
        """
        # 测试正常值
        bmi = self.calculator_who.calculate_bmi(70, 1.75, 'metric')
        expected_bmi = 70 / (1.75 ** 2)  # 22.86
        self.assertAlmostEqual(bmi, round(expected_bmi, 2), places=2)
        
        # 测试边界值
        bmi_min = self.calculator_who.calculate_bmi(1, 0.5, 'metric')
        self.assertEqual(bmi_min, 4.0)
        
        bmi_max = self.calculator_who.calculate_bmi(1000, 3.0, 'metric')
        self.assertAlmostEqual(bmi_max, 111.11, places=2)
    
    def test_bmi_calculation_imperial(self):
        """
        测试英制单位BMI计算
        """
        # 154磅，69英寸 ≈ 70kg，1.75m
        bmi = self.calculator_who.calculate_bmi(154, 69, 'imperial')
        # 154磅 = 69.85kg, 69英寸 = 1.7526m
        # BMI = 69.85 / (1.7526^2) ≈ 22.75
        self.assertAlmostEqual(bmi, 22.75, delta=0.5)
    
    def test_bmi_classification_who(self):
        """
        测试WHO标准BMI分类
        """
        # 测试各个分类
        category, name = self.calculator_who.classify_bmi(17.0)
        self.assertEqual(category, 'underweight')
        self.assertEqual(name, '偏瘦')
        
        category, name = self.calculator_who.classify_bmi(22.0)
        self.assertEqual(category, 'normal')
        self.assertEqual(name, '正常')
        
        category, name = self.calculator_who.classify_bmi(27.0)
        self.assertEqual(category, 'overweight')
        self.assertEqual(name, '偏胖')
        
        category, name = self.calculator_who.classify_bmi(32.0)
        self.assertEqual(category, 'obese')
        self.assertEqual(name, '肥胖')
    
    def test_bmi_classification_asian(self):
        """
        测试亚洲标准BMI分类
        """
        # 测试亚洲标准的差异
        category, name = self.calculator_asian.classify_bmi(24.0)
        self.assertEqual(category, 'overweight')  # 亚洲标准23以上为偏胖
        
        category, name = self.calculator_who.classify_bmi(24.0)
        self.assertEqual(category, 'normal')  # WHO标准25以下为正常
    
    def test_input_validation(self):
        """
        测试输入验证
        """
        # 测试无效输入
        with self.assertRaises(ValueError):
            self.calculator_who.calculate_bmi(-10, 1.75, 'metric')  # 负体重
        
        with self.assertRaises(ValueError):
            self.calculator_who.calculate_bmi(70, 0, 'metric')  # 零身高
        
        with self.assertRaises(ValueError):
            self.calculator_who.calculate_bmi(70, 1.75, 'invalid')  # 无效单位
        
        with self.assertRaises(ValueError):
            self.calculator_who.calculate_bmi(2000, 1.75, 'metric')  # 超出范围
    
    def test_health_advice_generation(self):
        """
        测试健康建议生成
        """
        # 测试正常体重建议
        advice = self.calculator_who.get_health_advice(22.0, 30, 'male', 'moderate')
        self.assertEqual(advice['category'], '正常')
        self.assertIn('恭喜', advice['general_advice'])
        self.assertTrue(len(advice['diet_tips']) > 0)
        self.assertTrue(len(advice['exercise_tips']) > 0)
        
        # 测试肥胖建议
        advice = self.calculator_who.get_health_advice(32.0, 40, 'female', 'low')
        self.assertEqual(advice['category'], '肥胖')
        self.assertIn('咨询医生', advice['general_advice'])
        self.assertTrue(len(advice['health_risks']) > 0)
    
    def test_age_specific_advice(self):
        """
        测试年龄特定建议
        """
        # 测试老年人建议
        advice = self.calculator_who.get_health_advice(22.0, 70, 'male', 'moderate')
        exercise_tips_text = ' '.join(advice['exercise_tips'])
        self.assertIn('平衡性', exercise_tips_text)
        
        # 测试未成年人建议
        advice = self.calculator_who.get_health_advice(22.0, 16, 'female', 'moderate')
        self.assertIn('家长和医生指导', advice['general_advice'])
    
    def test_gender_specific_advice(self):
        """
        测试性别特定建议
        """
        # 测试女性特定建议
        advice = self.calculator_who.get_health_advice(22.0, 25, 'female', 'moderate')
        diet_tips_text = ' '.join(advice['diet_tips'])
        self.assertIn('铁质', diet_tips_text)


class TestHealthDataManager(unittest.TestCase):
    """
    健康数据管理器测试类
    """
    
    def setUp(self):
        """
        测试前的准备工作
        """
        # 创建临时文件用于测试
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.data_manager = HealthDataManager(self.temp_file.name)
    
    def tearDown(self):
        """
        测试后的清理工作
        """
        # 删除临时文件
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_save_and_load_record(self):
        """
        测试记录保存和加载
        """
        # 保存记录
        success = self.data_manager.save_record(
            user_id='test_user',
            weight=70.0,
            height=1.75,
            bmi=22.86,
            category='正常',
            unit='metric'
        )
        self.assertTrue(success)
        
        # 加载记录
        records = self.data_manager.load_user_history('test_user')
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['weight'], 70.0)
        self.assertEqual(records[0]['bmi'], 22.86)
    
    def test_multiple_records(self):
        """
        测试多条记录处理
        """
        # 保存多条记录
        records_data = [
            (70.0, 1.75, 22.86, '正常'),
            (72.0, 1.75, 23.51, '正常'),
            (68.0, 1.75, 22.20, '正常')
        ]
        
        for weight, height, bmi, category in records_data:
            self.data_manager.save_record(
                user_id='test_user',
                weight=weight,
                height=height,
                bmi=bmi,
                category=category
            )
        
        # 验证记录数量
        records = self.data_manager.load_user_history('test_user')
        self.assertEqual(len(records), 3)
    
    def test_trend_analysis(self):
        """
        测试趋势分析
        """
        # 保存递增的BMI记录
        bmi_values = [20.0, 21.0, 22.0, 23.0]
        for bmi in bmi_values:
            self.data_manager.save_record(
                user_id='trend_user',
                weight=bmi * 1.75 * 1.75,  # 反推体重
                height=1.75,
                bmi=bmi,
                category='正常'
            )
        
        # 分析趋势
        analysis = self.data_manager.analyze_trend('trend_user')
        
        self.assertEqual(analysis['total_records'], 4)
        self.assertEqual(analysis['first_bmi'], 20.0)
        self.assertEqual(analysis['last_bmi'], 23.0)
        self.assertEqual(analysis['bmi_change'], 3.0)
        self.assertEqual(analysis['trend'], '上升')
    
    def test_insufficient_data_trend(self):
        """
        测试数据不足时的趋势分析
        """
        # 只保存一条记录
        self.data_manager.save_record(
            user_id='single_user',
            weight=70.0,
            height=1.75,
            bmi=22.86,
            category='正常'
        )
        
        # 分析趋势
        analysis = self.data_manager.analyze_trend('single_user')
        self.assertIn('error', analysis)


class TestIntegration(unittest.TestCase):
    """
    集成测试类
    """
    
    def test_complete_workflow(self):
        """
        测试完整的工作流程
        """
        # 创建计算器和数据管理器
        calculator = BMICalculator(use_asian_standard=False)
        
        # 模拟用户数据
        user_data = {
            'weight': 70.0,
            'height': 1.75,
            'age': 30,
            'gender': 'male',
            'activity_level': 'moderate',
            'unit': 'metric'
        }
        
        # 计算BMI
        bmi = calculator.calculate_bmi(
            weight=user_data['weight'],
            height=user_data['height'],
            unit=user_data['unit']
        )
        
        # 验证BMI计算
        expected_bmi = 70 / (1.75 ** 2)
        self.assertAlmostEqual(bmi, round(expected_bmi, 2), places=2)
        
        # 获取健康建议
        advice = calculator.get_health_advice(
            bmi=bmi,
            age=user_data['age'],
            gender=user_data['gender'],
            activity_level=user_data['activity_level']
        )
        
        # 验证建议内容
        self.assertIn('category', advice)
        self.assertIn('general_advice', advice)
        self.assertIn('diet_tips', advice)
        self.assertIn('exercise_tips', advice)
        
        # 验证分类正确性
        category, _ = calculator.classify_bmi(bmi)
        self.assertEqual(category, 'normal')


def run_performance_tests():
    """
    运行性能测试
    """
    import time
    
    print("\n=== 性能测试 ===")
    
    calculator = BMICalculator()
    
    # 测试大量BMI计算的性能
    start_time = time.time()
    for i in range(10000):
        bmi = calculator.calculate_bmi(70 + i % 50, 1.75, 'metric')
        category, _ = calculator.classify_bmi(bmi)
    end_time = time.time()
    
    print(f"10000次BMI计算和分类耗时: {end_time - start_time:.4f}秒")
    
    # 测试健康建议生成性能
    start_time = time.time()
    for i in range(1000):
        advice = calculator.get_health_advice(22.0, 30, 'male', 'moderate')
    end_time = time.time()
    
    print(f"1000次健康建议生成耗时: {end_time - start_time:.4f}秒")


def run_boundary_tests():
    """
    运行边界值测试
    """
    print("\n=== 边界值测试 ===")
    
    calculator = BMICalculator()
    
    # 测试极值
    test_cases = [
        (1, 0.5, 'metric', '极小值'),
        (1000, 3.0, 'metric', '极大值'),
        (2, 20, 'imperial', '英制极小值'),
        (2200, 120, 'imperial', '英制极大值')
    ]
    
    for weight, height, unit, description in test_cases:
        try:
            bmi = calculator.calculate_bmi(weight, height, unit)
            category, name = calculator.classify_bmi(bmi)
            print(f"{description}: BMI={bmi}, 分类={name}")
        except ValueError as e:
            print(f"{description}: 验证失败 - {e}")


def run_stress_tests():
    """
    运行压力测试
    """
    print("\n=== 压力测试 ===")
    
    # 创建临时数据管理器
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
    temp_file.close()
    
    try:
        data_manager = HealthDataManager(temp_file.name)
        
        # 测试大量数据保存
        start_time = time.time()
        for i in range(1000):
            data_manager.save_record(
                user_id=f'user_{i % 10}',  # 10个用户
                weight=70 + i % 30,
                height=1.75,
                bmi=22 + i % 10,
                category='正常'
            )
        end_time = time.time()
        
        print(f"保存1000条记录耗时: {end_time - start_time:.4f}秒")
        
        # 测试数据加载性能
        start_time = time.time()
        for i in range(100):
            records = data_manager.load_user_history(f'user_{i % 10}')
        end_time = time.time()
        
        print(f"100次数据加载耗时: {end_time - start_time:.4f}秒")
        
    finally:
        # 清理临时文件
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)


def main():
    """
    主测试函数
    """
    print("BMI计算器测试套件")
    print("=" * 50)
    
    # 运行单元测试
    print("\n运行单元测试...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # 运行性能测试
    run_performance_tests()
    
    # 运行边界值测试
    run_boundary_tests()
    
    # 运行压力测试
    run_stress_tests()
    
    print("\n=== 测试完成 ===")
    print("如果所有测试都通过，说明BMI计算器功能正常！")


if __name__ == '__main__':
    main()