#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session05 项目: 学生成绩管理系统

这是一个综合运用Python数据结构的实际项目，包括：
- 列表：存储学生信息和成绩
- 字典：组织学生数据
- 集合：管理专业和课程
- 元组：存储不可变的配置信息

功能特性：
1. 学生信息管理（增删改查）
2. 成绩录入和修改
3. 统计分析（平均分、排名等）
4. 数据导入导出
5. 多种查询和过滤功能

作者: Python教程团队
创建日期: 2024-12-21
"""

import json
import csv
from typing import Dict, List, Set, Tuple, Optional, Any
from collections import defaultdict, Counter
from datetime import datetime
import statistics


class StudentManager:
    """
    学生成绩管理系统主类
    
    使用多种数据结构来高效管理学生信息：
    - students: 字典，以学号为键存储学生信息
    - majors: 集合，存储所有专业
    - courses: 集合，存储所有课程
    - grade_config: 元组，存储成绩等级配置
    """
    
    def __init__(self):
        # 主要数据存储：字典，键为学号，值为学生信息字典
        self.students: Dict[str, Dict[str, Any]] = {}
        
        # 专业集合：使用集合确保唯一性
        self.majors: Set[str] = set()
        
        # 课程集合：使用集合确保唯一性
        self.courses: Set[str] = set()
        
        # 成绩等级配置：使用元组存储不可变配置
        self.grade_config: Tuple[Tuple[str, int, int], ...] = (
            ('A', 90, 100),
            ('B', 80, 89),
            ('C', 70, 79),
            ('D', 60, 69),
            ('F', 0, 59)
        )
        
        # 系统配置：使用字典存储可变配置
        self.config = {
            'max_students': 1000,
            'min_score': 0,
            'max_score': 100,
            'required_courses': ['数学', '英语'],
            'created_at': datetime.now().isoformat()
        }
    
    def add_student(self, student_id: str, name: str, major: str, 
                   age: int = None, email: str = None) -> bool:
        """
        添加新学生
        
        Args:
            student_id: 学号
            name: 姓名
            major: 专业
            age: 年龄（可选）
            email: 邮箱（可选）
        
        Returns:
            bool: 添加成功返回True，学号已存在返回False
        """
        if student_id in self.students:
            print(f"错误：学号 {student_id} 已存在")
            return False
        
        if len(self.students) >= self.config['max_students']:
            print(f"错误：学生数量已达上限 {self.config['max_students']}")
            return False
        
        # 创建学生信息字典
        student_info = {
            'name': name,
            'major': major,
            'age': age,
            'email': email,
            'scores': {},  # 字典存储各科成绩
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # 添加到主数据结构
        self.students[student_id] = student_info
        
        # 更新专业集合
        self.majors.add(major)
        
        print(f"成功添加学生：{name} ({student_id})")
        return True
    
    def remove_student(self, student_id: str) -> bool:
        """
        删除学生
        
        Args:
            student_id: 学号
        
        Returns:
            bool: 删除成功返回True，学号不存在返回False
        """
        if student_id not in self.students:
            print(f"错误：学号 {student_id} 不存在")
            return False
        
        student_name = self.students[student_id]['name']
        del self.students[student_id]
        
        print(f"成功删除学生：{student_name} ({student_id})")
        return True
    
    def update_student(self, student_id: str, **kwargs) -> bool:
        """
        更新学生信息
        
        Args:
            student_id: 学号
            **kwargs: 要更新的字段
        
        Returns:
            bool: 更新成功返回True，学号不存在返回False
        """
        if student_id not in self.students:
            print(f"错误：学号 {student_id} 不存在")
            return False
        
        # 更新允许的字段
        allowed_fields = {'name', 'major', 'age', 'email'}
        updated_fields = []
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                old_value = self.students[student_id].get(field)
                self.students[student_id][field] = value
                updated_fields.append(f"{field}: {old_value} -> {value}")
                
                # 如果更新专业，添加到专业集合
                if field == 'major':
                    self.majors.add(value)
        
        if updated_fields:
            self.students[student_id]['updated_at'] = datetime.now().isoformat()
            print(f"成功更新学生 {student_id}：{', '.join(updated_fields)}")
            return True
        else:
            print("没有有效的字段被更新")
            return False
    
    def add_score(self, student_id: str, course: str, score: float) -> bool:
        """
        添加或更新学生成绩
        
        Args:
            student_id: 学号
            course: 课程名
            score: 成绩
        
        Returns:
            bool: 操作成功返回True
        """
        if student_id not in self.students:
            print(f"错误：学号 {student_id} 不存在")
            return False
        
        if not (self.config['min_score'] <= score <= self.config['max_score']):
            print(f"错误：成绩必须在 {self.config['min_score']}-{self.config['max_score']} 之间")
            return False
        
        # 添加成绩
        self.students[student_id]['scores'][course] = score
        self.students[student_id]['updated_at'] = datetime.now().isoformat()
        
        # 更新课程集合
        self.courses.add(course)
        
        # 计算等级
        grade = self.get_grade(score)
        print(f"成功添加成绩：{self.students[student_id]['name']} - {course}: {score} ({grade})")
        return True
    
    def get_grade(self, score: float) -> str:
        """
        根据分数获取等级
        
        Args:
            score: 分数
        
        Returns:
            str: 等级字母
        """
        for grade, min_score, max_score in self.grade_config:
            if min_score <= score <= max_score:
                return grade
        return 'F'
    
    def get_student(self, student_id: str) -> Optional[Dict[str, Any]]:
        """
        获取学生信息
        
        Args:
            student_id: 学号
        
        Returns:
            Optional[Dict]: 学生信息字典，不存在返回None
        """
        return self.students.get(student_id)
    
    def search_students(self, **criteria) -> List[Dict[str, Any]]:
        """
        搜索学生
        
        Args:
            **criteria: 搜索条件
        
        Returns:
            List[Dict]: 符合条件的学生列表
        """
        results = []
        
        for student_id, student_info in self.students.items():
            match = True
            
            for field, value in criteria.items():
                if field == 'name' and value.lower() not in student_info.get('name', '').lower():
                    match = False
                    break
                elif field == 'major' and student_info.get('major') != value:
                    match = False
                    break
                elif field == 'min_age' and (student_info.get('age') or 0) < value:
                    match = False
                    break
                elif field == 'max_age' and (student_info.get('age') or 999) > value:
                    match = False
                    break
            
            if match:
                result = student_info.copy()
                result['student_id'] = student_id
                results.append(result)
        
        return results
    
    def get_students_by_major(self, major: str) -> List[Dict[str, Any]]:
        """
        按专业获取学生列表
        
        Args:
            major: 专业名称
        
        Returns:
            List[Dict]: 该专业的学生列表
        """
        return self.search_students(major=major)
    
    def calculate_student_average(self, student_id: str) -> Optional[float]:
        """
        计算学生平均分
        
        Args:
            student_id: 学号
        
        Returns:
            Optional[float]: 平均分，无成绩返回None
        """
        if student_id not in self.students:
            return None
        
        scores = list(self.students[student_id]['scores'].values())
        if not scores:
            return None
        
        return sum(scores) / len(scores)
    
    def get_course_statistics(self, course: str) -> Dict[str, Any]:
        """
        获取课程统计信息
        
        Args:
            course: 课程名
        
        Returns:
            Dict: 统计信息
        """
        scores = []
        students_with_scores = []
        
        # 收集该课程的所有成绩
        for student_id, student_info in self.students.items():
            if course in student_info['scores']:
                score = student_info['scores'][course]
                scores.append(score)
                students_with_scores.append({
                    'student_id': student_id,
                    'name': student_info['name'],
                    'score': score,
                    'grade': self.get_grade(score)
                })
        
        if not scores:
            return {'error': f'课程 {course} 没有成绩记录'}
        
        # 计算统计信息
        stats = {
            'course': course,
            'student_count': len(scores),
            'average': statistics.mean(scores),
            'median': statistics.median(scores),
            'max_score': max(scores),
            'min_score': min(scores),
            'std_dev': statistics.stdev(scores) if len(scores) > 1 else 0,
            'grade_distribution': dict(Counter(self.get_grade(score) for score in scores)),
            'students': sorted(students_with_scores, key=lambda x: x['score'], reverse=True)
        }
        
        return stats
    
    def get_major_statistics(self) -> Dict[str, Dict[str, Any]]:
        """
        获取各专业统计信息
        
        Returns:
            Dict: 各专业的统计信息
        """
        major_stats = defaultdict(lambda: {
            'student_count': 0,
            'total_scores': [],
            'students': []
        })
        
        # 按专业分组统计
        for student_id, student_info in self.students.items():
            major = student_info['major']
            major_stats[major]['student_count'] += 1
            major_stats[major]['students'].append({
                'student_id': student_id,
                'name': student_info['name'],
                'average': self.calculate_student_average(student_id)
            })
            
            # 收集该专业所有学生的所有成绩
            scores = list(student_info['scores'].values())
            major_stats[major]['total_scores'].extend(scores)
        
        # 计算每个专业的统计信息
        result = {}
        for major, data in major_stats.items():
            scores = data['total_scores']
            if scores:
                result[major] = {
                    'student_count': data['student_count'],
                    'average_score': statistics.mean(scores),
                    'median_score': statistics.median(scores),
                    'max_score': max(scores),
                    'min_score': min(scores),
                    'students': sorted(data['students'], 
                                     key=lambda x: x['average'] or 0, 
                                     reverse=True)
                }
            else:
                result[major] = {
                    'student_count': data['student_count'],
                    'message': '该专业暂无成绩记录',
                    'students': data['students']
                }
        
        return result
    
    def get_top_students(self, n: int = 10, course: str = None) -> List[Dict[str, Any]]:
        """
        获取成绩排名前N的学生
        
        Args:
            n: 返回的学生数量
            course: 指定课程，None表示按平均分排名
        
        Returns:
            List[Dict]: 排名前N的学生信息
        """
        student_scores = []
        
        for student_id, student_info in self.students.items():
            if course:
                # 按指定课程排名
                if course in student_info['scores']:
                    score = student_info['scores'][course]
                    student_scores.append({
                        'student_id': student_id,
                        'name': student_info['name'],
                        'major': student_info['major'],
                        'score': score,
                        'grade': self.get_grade(score),
                        'course': course
                    })
            else:
                # 按平均分排名
                avg_score = self.calculate_student_average(student_id)
                if avg_score is not None:
                    student_scores.append({
                        'student_id': student_id,
                        'name': student_info['name'],
                        'major': student_info['major'],
                        'average_score': avg_score,
                        'grade': self.get_grade(avg_score),
                        'course_count': len(student_info['scores'])
                    })
        
        # 按分数降序排序
        sort_key = 'score' if course else 'average_score'
        student_scores.sort(key=lambda x: x[sort_key], reverse=True)
        
        return student_scores[:n]
    
    def export_to_json(self, filename: str) -> bool:
        """
        导出数据到JSON文件
        
        Args:
            filename: 文件名
        
        Returns:
            bool: 导出成功返回True
        """
        try:
            export_data = {
                'students': self.students,
                'majors': list(self.majors),
                'courses': list(self.courses),
                'config': self.config,
                'export_time': datetime.now().isoformat()
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            print(f"数据已导出到 {filename}")
            return True
        except Exception as e:
            print(f"导出失败：{e}")
            return False
    
    def import_from_json(self, filename: str) -> bool:
        """
        从JSON文件导入数据
        
        Args:
            filename: 文件名
        
        Returns:
            bool: 导入成功返回True
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.students = data.get('students', {})
            self.majors = set(data.get('majors', []))
            self.courses = set(data.get('courses', []))
            
            # 合并配置，保留现有配置的优先级
            imported_config = data.get('config', {})
            for key, value in imported_config.items():
                if key not in self.config:
                    self.config[key] = value
            
            print(f"数据已从 {filename} 导入")
            print(f"导入了 {len(self.students)} 个学生，{len(self.majors)} 个专业，{len(self.courses)} 门课程")
            return True
        except Exception as e:
            print(f"导入失败：{e}")
            return False
    
    def export_to_csv(self, filename: str) -> bool:
        """
        导出学生信息到CSV文件
        
        Args:
            filename: 文件名
        
        Returns:
            bool: 导出成功返回True
        """
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # 写入表头
                headers = ['学号', '姓名', '专业', '年龄', '邮箱', '平均分', '课程数']
                all_courses = sorted(self.courses)
                headers.extend(all_courses)
                writer.writerow(headers)
                
                # 写入学生数据
                for student_id, student_info in self.students.items():
                    row = [
                        student_id,
                        student_info['name'],
                        student_info['major'],
                        student_info.get('age', ''),
                        student_info.get('email', ''),
                        self.calculate_student_average(student_id) or '',
                        len(student_info['scores'])
                    ]
                    
                    # 添加各科成绩
                    for course in all_courses:
                        score = student_info['scores'].get(course, '')
                        row.append(score)
                    
                    writer.writerow(row)
            
            print(f"学生信息已导出到 {filename}")
            return True
        except Exception as e:
            print(f"导出失败：{e}")
            return False
    
    def get_summary(self) -> Dict[str, Any]:
        """
        获取系统概览信息
        
        Returns:
            Dict: 系统概览
        """
        total_students = len(self.students)
        total_majors = len(self.majors)
        total_courses = len(self.courses)
        
        # 统计有成绩的学生数
        students_with_scores = sum(1 for s in self.students.values() if s['scores'])
        
        # 统计总成绩记录数
        total_score_records = sum(len(s['scores']) for s in self.students.values())
        
        # 最新添加的学生
        latest_student = None
        if self.students:
            latest_student_id = max(self.students.keys(), 
                                  key=lambda x: self.students[x]['created_at'])
            latest_student = {
                'student_id': latest_student_id,
                'name': self.students[latest_student_id]['name'],
                'created_at': self.students[latest_student_id]['created_at']
            }
        
        return {
            'total_students': total_students,
            'total_majors': total_majors,
            'total_courses': total_courses,
            'students_with_scores': students_with_scores,
            'total_score_records': total_score_records,
            'majors_list': sorted(self.majors),
            'courses_list': sorted(self.courses),
            'latest_student': latest_student,
            'system_created_at': self.config['created_at']
        }
    
    def print_summary(self):
        """
        打印系统概览信息
        """
        summary = self.get_summary()
        
        print("\n" + "=" * 50)
        print("学生成绩管理系统 - 概览")
        print("=" * 50)
        print(f"学生总数：{summary['total_students']}")
        print(f"专业数量：{summary['total_majors']}")
        print(f"课程数量：{summary['total_courses']}")
        print(f"有成绩学生：{summary['students_with_scores']}")
        print(f"成绩记录总数：{summary['total_score_records']}")
        
        if summary['majors_list']:
            print(f"\n专业列表：{', '.join(summary['majors_list'])}")
        
        if summary['courses_list']:
            print(f"\n课程列表：{', '.join(summary['courses_list'])}")
        
        if summary['latest_student']:
            latest = summary['latest_student']
            print(f"\n最新添加学生：{latest['name']} ({latest['student_id']})")
        
        print("=" * 50)


def demonstrate_system():
    """
    演示学生成绩管理系统的功能
    """
    print("学生成绩管理系统演示")
    print("=" * 50)
    
    # 创建管理系统实例
    manager = StudentManager()
    
    # 1. 添加学生
    print("\n1. 添加学生")
    manager.add_student("2024001", "张三", "计算机科学", 20, "zhangsan@example.com")
    manager.add_student("2024002", "李四", "数学", 19, "lisi@example.com")
    manager.add_student("2024003", "王五", "计算机科学", 21)
    manager.add_student("2024004", "赵六", "物理", 20)
    manager.add_student("2024005", "钱七", "数学", 19)
    
    # 2. 添加成绩
    print("\n2. 添加成绩")
    # 张三的成绩
    manager.add_score("2024001", "数学", 95)
    manager.add_score("2024001", "英语", 88)
    manager.add_score("2024001", "程序设计", 92)
    
    # 李四的成绩
    manager.add_score("2024002", "数学", 98)
    manager.add_score("2024002", "英语", 85)
    manager.add_score("2024002", "高等数学", 96)
    
    # 王五的成绩
    manager.add_score("2024003", "数学", 82)
    manager.add_score("2024003", "程序设计", 89)
    manager.add_score("2024003", "数据结构", 91)
    
    # 赵六的成绩
    manager.add_score("2024004", "数学", 87)
    manager.add_score("2024004", "物理", 93)
    manager.add_score("2024004", "英语", 79)
    
    # 钱七的成绩
    manager.add_score("2024005", "数学", 94)
    manager.add_score("2024005", "高等数学", 91)
    
    # 3. 查询学生信息
    print("\n3. 查询学生信息")
    student = manager.get_student("2024001")
    if student:
        print(f"学生信息：{student['name']}, 专业：{student['major']}, 平均分：{manager.calculate_student_average('2024001'):.2f}")
    
    # 4. 按专业搜索
    print("\n4. 按专业搜索学生")
    cs_students = manager.get_students_by_major("计算机科学")
    print(f"计算机科学专业学生：")
    for student in cs_students:
        avg = manager.calculate_student_average(student['student_id'])
        print(f"  - {student['name']} ({student['student_id']})，平均分：{avg:.2f if avg else '无'}")
    
    # 5. 课程统计
    print("\n5. 数学课程统计")
    math_stats = manager.get_course_statistics("数学")
    if 'error' not in math_stats:
        print(f"课程：{math_stats['course']}")
        print(f"学生数：{math_stats['student_count']}")
        print(f"平均分：{math_stats['average']:.2f}")
        print(f"最高分：{math_stats['max_score']}")
        print(f"最低分：{math_stats['min_score']}")
        print(f"等级分布：{math_stats['grade_distribution']}")
    
    # 6. 专业统计
    print("\n6. 各专业统计")
    major_stats = manager.get_major_statistics()
    for major, stats in major_stats.items():
        print(f"\n专业：{major}")
        print(f"  学生数：{stats['student_count']}")
        if 'average_score' in stats:
            print(f"  平均分：{stats['average_score']:.2f}")
            print(f"  最高分：{stats['max_score']}")
        else:
            print(f"  {stats['message']}")
    
    # 7. 成绩排名
    print("\n7. 成绩排名（前3名）")
    top_students = manager.get_top_students(3)
    for i, student in enumerate(top_students, 1):
        print(f"{i}. {student['name']} ({student['major']}) - 平均分：{student['average_score']:.2f}")
    
    # 8. 数学课程排名
    print("\n8. 数学课程排名")
    math_top = manager.get_top_students(5, "数学")
    for i, student in enumerate(math_top, 1):
        print(f"{i}. {student['name']} ({student['major']}) - 数学：{student['score']} ({student['grade']})")
    
    # 9. 系统概览
    print("\n9. 系统概览")
    manager.print_summary()
    
    # 10. 数据导出演示
    print("\n10. 数据导出演示")
    print("导出到JSON文件...")
    manager.export_to_json("students_data.json")
    
    print("导出到CSV文件...")
    manager.export_to_csv("students_data.csv")
    
    print("\n演示完成！")
    print("\n学习要点：")
    print("1. 字典用于存储结构化的学生数据，支持快速查找")
    print("2. 集合用于管理唯一的专业和课程列表")
    print("3. 元组用于存储不可变的配置信息")
    print("4. 列表用于存储排序后的结果")
    print("5. defaultdict简化了分组统计的代码")
    print("6. Counter用于统计等级分布")
    print("7. 合理的数据结构选择提高了程序效率")


if __name__ == "__main__":
    demonstrate_system()