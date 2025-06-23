#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习1参考答案：基础数据库操作
学生成绩管理系统的完整实现
"""

import sqlite3
import os

class StudentGradeSystem:
    def __init__(self, db_name='student_grades.db'):
        """初始化数据库连接"""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
    
    def create_tables(self):
        """创建所需的表"""
        # 创建students表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            class_name TEXT
        )
        ''')
        
        # 创建courses表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id TEXT PRIMARY KEY,
            course_name TEXT NOT NULL,
            credits INTEGER
        )
        ''')
        
        # 创建scores表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            course_id TEXT NOT NULL,
            score REAL NOT NULL,
            exam_date DATE,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        )
        ''')
        
        self.conn.commit()
    
    def add_student(self, student_id, name, age, class_name):
        """添加学生"""
        try:
            self.cursor.execute('''
            INSERT INTO students (student_id, name, age, class_name)
            VALUES (?, ?, ?, ?)
            ''', (student_id, name, age, class_name))
            self.conn.commit()
            print(f"✓ 成功添加学生：{name}")
        except sqlite3.IntegrityError:
            print(f"✗ 学生 {student_id} 已存在")
    
    def add_course(self, course_id, course_name, credits):
        """添加课程"""
        try:
            self.cursor.execute('''
            INSERT INTO courses (course_id, course_name, credits)
            VALUES (?, ?, ?)
            ''', (course_id, course_name, credits))
            self.conn.commit()
            print(f"✓ 成功添加课程：{course_name}")
        except sqlite3.IntegrityError:
            print(f"✗ 课程 {course_id} 已存在")
    
    def add_score(self, student_id, course_id, score, exam_date):
        """添加成绩"""
        # 检查学生是否存在
        self.cursor.execute('SELECT 1 FROM students WHERE student_id = ?', (student_id,))
        if not self.cursor.fetchone():
            print(f"✗ 学生 {student_id} 不存在")
            return
        
        # 检查课程是否存在
        self.cursor.execute('SELECT 1 FROM courses WHERE course_id = ?', (course_id,))
        if not self.cursor.fetchone():
            print(f"✗ 课程 {course_id} 不存在")
            return
        
        # 添加成绩
        self.cursor.execute('''
        INSERT INTO scores (student_id, course_id, score, exam_date)
        VALUES (?, ?, ?, ?)
        ''', (student_id, course_id, score, exam_date))
        self.conn.commit()
        print(f"✓ 成功添加成绩")
    
    def get_all_students(self):
        """获取所有学生信息"""
        self.cursor.execute('''
        SELECT student_id, name, age, class_name 
        FROM students 
        ORDER BY student_id
        ''')
        return self.cursor.fetchall()
    
    def get_student_scores(self, student_id):
        """获取指定学生的所有成绩"""
        self.cursor.execute('''
        SELECT c.course_name, s.score, s.exam_date
        FROM scores s
        JOIN courses c ON s.course_id = c.course_id
        WHERE s.student_id = ?
        ORDER BY s.exam_date
        ''', (student_id,))
        return self.cursor.fetchall()
    
    def get_course_average(self, course_id):
        """获取指定课程的平均分"""
        self.cursor.execute('''
        SELECT AVG(score) 
        FROM scores 
        WHERE course_id = ?
        ''', (course_id,))
        
        result = self.cursor.fetchone()
        return result[0] if result[0] else 0
    
    def close(self):
        """关闭数据库连接"""
        self.conn.close()

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
        print(f"  学号:{student[0]}, 姓名:{student[1]}, 年龄:{student[2]}, 班级:{student[3]}")
    
    print("\n张三(2024001)的成绩：")
    scores = system.get_student_scores('2024001')
    for score in scores:
        print(f"  {score[0]}: {score[1]}分 (考试日期: {score[2]})")
    
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
    print("实现要点：")
    print("1. 使用外键保证数据完整性")
    print("2. 在添加成绩前检查学生和课程是否存在")
    print("3. 使用JOIN连接多个表查询")
    print("4. 使用AVG()聚合函数计算平均分")
    print("5. 使用参数化查询防止SQL注入") 