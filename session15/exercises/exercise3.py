#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习3：高级查询与优化 - 员工考勤系统
目标：实现一个具有复杂查询和性能优化的考勤系统

要求：
1. 设计复杂的关联表结构
2. 实现高级查询功能（JOIN、子查询、窗口函数等）
3. 创建合适的索引优化查询性能
4. 实现数据分析和报表功能
5. 处理大量数据的性能优化
"""

import sqlite3
import os
from datetime import datetime, timedelta, date
import random

class AttendanceSystem:
    def __init__(self, db_name='attendance.db'):
        """初始化考勤系统"""
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        # 启用外键约束
        self.conn.execute('PRAGMA foreign_keys = ON')
        self.cursor = self.conn.cursor()
    
    def create_tables(self):
        """创建数据表和索引"""
        # TODO: 创建以下表
        # 1. departments表：部门信息
        # 2. employees表：员工信息（包含部门ID外键）
        # 3. attendance_records表：考勤记录
        # 4. leave_requests表：请假申请
        # 5. overtime_records表：加班记录
        
        # TODO: 创建必要的索引以优化查询性能
        pass
    
    def generate_test_data(self, num_employees=100, days=30):
        """生成测试数据"""
        # TODO: 生成大量测试数据用于性能测试
        # 1. 创建5个部门
        # 2. 创建指定数量的员工
        # 3. 为每个员工生成指定天数的考勤记录
        # 4. 随机生成一些请假和加班记录
        pass
    
    def get_employee_attendance_summary(self, employee_id, year, month):
        """获取员工月度考勤汇总"""
        # TODO: 查询指定员工的月度考勤情况
        # 返回：出勤天数、迟到次数、早退次数、请假天数、加班小时数
        pass
    
    def get_department_attendance_stats(self, department_id, date):
        """获取部门某日考勤统计"""
        # TODO: 使用JOIN查询部门的考勤统计
        # 返回：应到人数、实到人数、请假人数、迟到人数等
        pass
    
    def find_attendance_anomalies(self):
        """查找考勤异常"""
        # TODO: 使用复杂查询找出考勤异常
        # 1. 连续迟到超过3天的员工
        # 2. 本月请假超过5天的员工
        # 3. 加班时间异常（超过100小时）的员工
        pass
    
    def calculate_monthly_salary_adjustments(self, year, month):
        """计算月度工资调整（基于考勤）"""
        # TODO: 根据考勤情况计算工资调整
        # 迟到扣款、加班费、全勤奖等
        # 使用窗口函数和子查询
        pass
    
    def get_attendance_trends(self, start_date, end_date):
        """分析考勤趋势"""
        # TODO: 分析指定时间段的考勤趋势
        # 1. 每日出勤率变化
        # 2. 部门间对比
        # 3. 迟到早退趋势
        pass
    
    def optimize_queries(self):
        """查询优化演示"""
        # TODO: 演示查询优化技巧
        # 1. 使用EXPLAIN QUERY PLAN分析查询
        # 2. 比较有无索引的查询性能
        # 3. 优化慢查询
        pass
    
    def create_materialized_view(self):
        """创建物化视图提高报表性能"""
        # TODO: 创建预计算的汇总表
        # 用于加速常用的统计查询
        pass
    
    def batch_insert_optimization(self, records):
        """批量插入优化"""
        # TODO: 演示批量插入的性能优化
        # 1. 使用事务
        # 2. 使用executemany
        # 3. 临时关闭索引
        pass
    
    def close(self):
        """关闭连接"""
        self.conn.close()

def performance_test():
    """性能测试和优化演示"""
    print("员工考勤系统 - 高级查询与优化")
    print("="*50)
    
    system = AttendanceSystem()
    system.create_tables()
    
    # 生成测试数据
    print("\n1. 生成测试数据（100名员工，30天记录）")
    system.generate_test_data(100, 30)
    
    # 员工考勤汇总
    print("\n2. 查询员工月度考勤汇总")
    summary = system.get_employee_attendance_summary(1, 2024, 1)
    print(f"  员工1的1月考勤：{summary}")
    
    # 部门统计
    print("\n3. 部门考勤统计")
    stats = system.get_department_attendance_stats(1, '2024-01-15')
    print(f"  技术部1月15日：{stats}")
    
    # 查找异常
    print("\n4. 考勤异常检测")
    anomalies = system.find_attendance_anomalies()
    for anomaly in anomalies[:5]:  # 只显示前5条
        print(f"  {anomaly}")
    
    # 工资调整计算
    print("\n5. 月度工资调整计算")
    adjustments = system.calculate_monthly_salary_adjustments(2024, 1)
    print(f"  已计算{len(adjustments)}名员工的工资调整")
    
    # 趋势分析
    print("\n6. 考勤趋势分析")
    trends = system.get_attendance_trends('2024-01-01', '2024-01-31')
    print(f"  趋势分析完成")
    
    # 查询优化
    print("\n7. 查询优化演示")
    system.optimize_queries()
    
    # 物化视图
    print("\n8. 创建物化视图")
    system.create_materialized_view()
    
    # 批量插入优化
    print("\n9. 批量插入性能测试")
    # 生成1000条测试记录
    test_records = [(i, '2024-01-01', '09:00', '18:00') for i in range(1000)]
    system.batch_insert_optimization(test_records)
    
    system.close()
    
    # 清理
    if os.path.exists('attendance.db'):
        os.remove('attendance.db')

if __name__ == "__main__":
    performance_test()
    
    print("\n" + "="*50)
    print("高级技巧总结：")
    print("1. 使用EXPLAIN分析查询计划")
    print("2. 为常用查询字段创建索引")
    print("3. 使用批量操作减少数据库调用")
    print("4. 合理使用事务提高性能")
    print("5. 考虑使用物化视图缓存复杂查询结果")
    print("6. 定期分析和优化慢查询") 