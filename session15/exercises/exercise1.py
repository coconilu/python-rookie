#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习1：基础数据库操作
目标：创建一个学生成绩管理系统的数据库

要求：
1. 创建students表（学号、姓名、年龄、班级）
2. 创建courses表（课程ID、课程名、学分）
3. 创建scores表（学号、课程ID、成绩、考试日期）
4. 实现基本的数据插入功能
5. 实现查询功能：
   - 查询所有学生信息
   - 查询特定学生的所有成绩
   - 查询特定课程的平均分
"""

import sqlite3
import os

class StudentGradeSystem:
    def __init__(self, db_name='student_grades.db'):
        """初始化数据库连接"""
        # TODO: 连接数据库
        pass
    
    def create_tables(self):
        """创建所需的表"""
        # TODO: 创建students表
        # 字段：student_id (主键), name, age, class_name
        
        # TODO: 创建courses表
        # 字段：course_id (主键), course_name, credits
        
        # TODO: 创建scores表
        # 字段：id (主键), student_id, course_id, score, exam_date
        # 注意：student_id和course_id应该是外键
        pass
    
    def add_student(self, student_id, name, age, class_name):
        """添加学生"""
        # TODO: 实现添加学生功能
        pass
    
    def add_course(self, course_id, course_name, credits):
        """添加课程"""
        # TODO: 实现添加课程功能
        pass
    
    def add_score(self, student_id, course_id, score, exam_date):
        """添加成绩"""
        # TODO: 实现添加成绩功能
        # 注意：需要验证学生和课程是否存在
        pass
    
    def get_all_students(self):
        """获取所有学生信息"""
        # TODO: 查询并返回所有学生
        pass
    
    def get_student_scores(self, student_id):
        """获取指定学生的所有成绩"""
        # TODO: 使用JOIN查询学生的成绩
        # 返回格式：[(课程名, 成绩, 考试日期), ...]
        pass
    
    def get_course_average(self, course_id):
        """获取指定课程的平均分"""
        # TODO: 计算并返回课程平均分
        pass
    
    def close(self):
        """关闭数据库连接"""
        # TODO: 关闭连接
        pass

def test_system():
    """测试函数"""
    print("测试学生成绩管理系统")
    print("="*50)
    
    # 创建系统实例
    system = StudentGradeSystem()
    
    # 创建表
    system.create_tables()
    print("✓ 数据表创建完成")
    
    # 添加测试数据
    # 添加学生
    students = [
        ('2024001', '张三', 18, '计算机1班'),
        ('2024002', '李四', 19, '计算机1班'),
        ('2024003', '王五', 18, '计算机2班')
    ]
    
    for student in students:
        system.add_student(*student)
    
    # 添加课程
    courses = [
        ('CS101', 'Python编程', 3),
        ('CS102', '数据结构', 4),
        ('CS103', '数据库原理', 3)
    ]
    
    for course in courses:
        system.add_course(*course)
    
    # 添加成绩
    scores = [
        ('2024001', 'CS101', 85, '2024-01-15'),
        ('2024001', 'CS102', 90, '2024-01-16'),
        ('2024002', 'CS101', 88, '2024-01-15'),
        ('2024002', 'CS103', 92, '2024-01-17'),
        ('2024003', 'CS101', 78, '2024-01-15'),
        ('2024003', 'CS102', 85, '2024-01-16')
    ]
    
    for score in scores:
        system.add_score(*score)
    
    # 测试查询功能
    print("\n所有学生信息：")
    students = system.get_all_students()
    for student in students:
        print(f"  {student}")
    
    print("\n张三(2024001)的成绩：")
    scores = system.get_student_scores('2024001')
    for score in scores:
        print(f"  {score}")
    
    print("\nPython编程(CS101)的平均分：")
    avg = system.get_course_average('CS101')
    print(f"  {avg:.2f}分")
    
    # 关闭系统
    system.close()
    
    # 清理
    if os.path.exists('student_grades.db'):
        os.remove('student_grades.db')

if __name__ == "__main__":
    test_system()
    
    print("\n" + "="*50)
    print("练习要点：")
    print("1. 正确创建表结构，包括主键和外键")
    print("2. 使用参数化查询防止SQL注入")
    print("3. 实现JOIN查询连接多个表")
    print("4. 使用聚合函数计算平均分") 