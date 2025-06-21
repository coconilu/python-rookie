#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session05 项目: 学生成绩管理系统 - 命令行界面

提供一个简单的命令行界面来操作学生成绩管理系统。
这个界面演示了如何将数据结构知识应用到实际的用户交互中。

功能菜单：
1. 学生管理（增删改查）
2. 成绩管理
3. 统计查询
4. 数据导入导出
5. 系统信息

作者: Python教程团队
创建日期: 2024-12-21
"""

import os
import sys
from typing import Optional
from student_manager import StudentManager


class StudentManagerCLI:
    """
    学生成绩管理系统命令行界面
    
    提供用户友好的交互界面来操作StudentManager
    """
    
    def __init__(self):
        self.manager = StudentManager()
        self.running = True
    
    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pause(self):
        """暂停等待用户输入"""
        input("\n按回车键继续...")
    
    def print_header(self, title: str):
        """打印标题"""
        print("\n" + "=" * 60)
        print(f" {title} ".center(60))
        print("=" * 60)
    
    def print_menu(self):
        """打印主菜单"""
        self.clear_screen()
        self.print_header("学生成绩管理系统")
        print("\n请选择操作：")
        print("1. 学生管理")
        print("2. 成绩管理")
        print("3. 查询统计")
        print("4. 数据管理")
        print("5. 系统信息")
        print("6. 加载示例数据")
        print("0. 退出系统")
        print("-" * 60)
    
    def get_input(self, prompt: str, input_type: type = str, required: bool = True) -> Optional[any]:
        """获取用户输入并进行类型转换和验证"""
        while True:
            try:
                value = input(prompt).strip()
                
                if not value and not required:
                    return None
                
                if not value and required:
                    print("输入不能为空，请重新输入。")
                    continue
                
                if input_type == int:
                    return int(value)
                elif input_type == float:
                    return float(value)
                else:
                    return value
                    
            except ValueError:
                print(f"输入格式错误，请输入{input_type.__name__}类型的值。")
            except KeyboardInterrupt:
                print("\n操作已取消。")
                return None
    
    def student_management_menu(self):
        """学生管理菜单"""
        while True:
            self.clear_screen()
            self.print_header("学生管理")
            print("\n1. 添加学生")
            print("2. 删除学生")
            print("3. 修改学生信息")
            print("4. 查看学生信息")
            print("5. 搜索学生")
            print("6. 按专业查看学生")
            print("0. 返回主菜单")
            print("-" * 60)
            
            choice = self.get_input("请选择操作 (0-6): ")
            
            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.remove_student()
            elif choice == "3":
                self.update_student()
            elif choice == "4":
                self.view_student()
            elif choice == "5":
                self.search_students()
            elif choice == "6":
                self.view_students_by_major()
            elif choice == "0":
                break
            else:
                print("无效选择，请重新输入。")
                self.pause()
    
    def add_student(self):
        """添加学生"""
        self.print_header("添加学生")
        
        student_id = self.get_input("学号: ")
        if not student_id:
            return
        
        name = self.get_input("姓名: ")
        if not name:
            return
        
        major = self.get_input("专业: ")
        if not major:
            return
        
        age = self.get_input("年龄 (可选): ", int, False)
        email = self.get_input("邮箱 (可选): ", str, False)
        
        success = self.manager.add_student(student_id, name, major, age, email)
        if success:
            print("\n学生添加成功！")
        
        self.pause()
    
    def remove_student(self):
        """删除学生"""
        self.print_header("删除学生")
        
        student_id = self.get_input("请输入要删除的学号: ")
        if not student_id:
            return
        
        # 先显示学生信息确认
        student = self.manager.get_student(student_id)
        if student:
            print(f"\n找到学生: {student['name']} ({student['major']})")
            confirm = self.get_input("确认删除？(y/N): ")
            if confirm.lower() == 'y':
                self.manager.remove_student(student_id)
                print("学生已删除。")
            else:
                print("操作已取消。")
        
        self.pause()
    
    def update_student(self):
        """修改学生信息"""
        self.print_header("修改学生信息")
        
        student_id = self.get_input("请输入学号: ")
        if not student_id:
            return
        
        student = self.manager.get_student(student_id)
        if not student:
            print(f"学号 {student_id} 不存在。")
            self.pause()
            return
        
        print(f"\n当前信息:")
        print(f"姓名: {student['name']}")
        print(f"专业: {student['major']}")
        print(f"年龄: {student.get('age', '未设置')}")
        print(f"邮箱: {student.get('email', '未设置')}")
        
        print("\n请输入新信息（直接回车保持不变）:")
        
        updates = {}
        new_name = self.get_input(f"新姓名 [{student['name']}]: ", str, False)
        if new_name:
            updates['name'] = new_name
        
        new_major = self.get_input(f"新专业 [{student['major']}]: ", str, False)
        if new_major:
            updates['major'] = new_major
        
        new_age = self.get_input(f"新年龄 [{student.get('age', '未设置')}]: ", int, False)
        if new_age:
            updates['age'] = new_age
        
        new_email = self.get_input(f"新邮箱 [{student.get('email', '未设置')}]: ", str, False)
        if new_email:
            updates['email'] = new_email
        
        if updates:
            self.manager.update_student(student_id, **updates)
            print("\n学生信息更新成功！")
        else:
            print("\n没有信息被修改。")
        
        self.pause()
    
    def view_student(self):
        """查看学生信息"""
        self.print_header("查看学生信息")
        
        student_id = self.get_input("请输入学号: ")
        if not student_id:
            return
        
        student = self.manager.get_student(student_id)
        if student:
            print(f"\n学生详细信息:")
            print(f"学号: {student_id}")
            print(f"姓名: {student['name']}")
            print(f"专业: {student['major']}")
            print(f"年龄: {student.get('age', '未设置')}")
            print(f"邮箱: {student.get('email', '未设置')}")
            
            avg_score = self.manager.calculate_student_average(student_id)
            print(f"平均分: {avg_score:.2f if avg_score else '无成绩'}")
            
            if student['scores']:
                print("\n成绩详情:")
                for course, score in student['scores'].items():
                    grade = self.manager.get_grade(score)
                    print(f"  {course}: {score} ({grade})")
            else:
                print("\n暂无成绩记录")
        else:
            print(f"学号 {student_id} 不存在。")
        
        self.pause()
    
    def search_students(self):
        """搜索学生"""
        self.print_header("搜索学生")
        
        print("搜索条件（直接回车跳过）:")
        criteria = {}
        
        name = self.get_input("姓名包含: ", str, False)
        if name:
            criteria['name'] = name
        
        major = self.get_input("专业: ", str, False)
        if major:
            criteria['major'] = major
        
        min_age = self.get_input("最小年龄: ", int, False)
        if min_age:
            criteria['min_age'] = min_age
        
        max_age = self.get_input("最大年龄: ", int, False)
        if max_age:
            criteria['max_age'] = max_age
        
        if not criteria:
            print("没有设置搜索条件。")
            self.pause()
            return
        
        results = self.manager.search_students(**criteria)
        
        if results:
            print(f"\n找到 {len(results)} 个学生:")
            print("-" * 80)
            print(f"{'学号':<10} {'姓名':<10} {'专业':<15} {'年龄':<5} {'平均分':<8}")
            print("-" * 80)
            
            for student in results:
                avg_score = self.manager.calculate_student_average(student['student_id'])
                avg_str = f"{avg_score:.2f}" if avg_score else "无"
                age_str = str(student.get('age', '未知'))
                
                print(f"{student['student_id']:<10} {student['name']:<10} {student['major']:<15} {age_str:<5} {avg_str:<8}")
        else:
            print("\n没有找到符合条件的学生。")
        
        self.pause()
    
    def view_students_by_major(self):
        """按专业查看学生"""
        self.print_header("按专业查看学生")
        
        if not self.manager.majors:
            print("系统中还没有专业信息。")
            self.pause()
            return
        
        print("可选专业:")
        majors_list = sorted(self.manager.majors)
        for i, major in enumerate(majors_list, 1):
            print(f"{i}. {major}")
        
        choice = self.get_input("\n请选择专业编号或直接输入专业名称: ")
        
        if choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(majors_list):
                major = majors_list[choice_num - 1]
            else:
                print("无效的专业编号。")
                self.pause()
                return
        else:
            major = choice
        
        students = self.manager.get_students_by_major(major)
        
        if students:
            print(f"\n{major} 专业学生 ({len(students)} 人):")
            print("-" * 60)
            print(f"{'学号':<10} {'姓名':<10} {'平均分':<8} {'课程数':<6}")
            print("-" * 60)
            
            for student in students:
                avg_score = self.manager.calculate_student_average(student['student_id'])
                avg_str = f"{avg_score:.2f}" if avg_score else "无"
                course_count = len(student['scores'])
                
                print(f"{student['student_id']:<10} {student['name']:<10} {avg_str:<8} {course_count:<6}")
        else:
            print(f"\n{major} 专业暂无学生。")
        
        self.pause()
    
    def score_management_menu(self):
        """成绩管理菜单"""
        while True:
            self.clear_screen()
            self.print_header("成绩管理")
            print("\n1. 添加/修改成绩")
            print("2. 查看学生成绩")
            print("3. 课程成绩统计")
            print("0. 返回主菜单")
            print("-" * 60)
            
            choice = self.get_input("请选择操作 (0-3): ")
            
            if choice == "1":
                self.add_score()
            elif choice == "2":
                self.view_student_scores()
            elif choice == "3":
                self.view_course_statistics()
            elif choice == "0":
                break
            else:
                print("无效选择，请重新输入。")
                self.pause()
    
    def add_score(self):
        """添加成绩"""
        self.print_header("添加/修改成绩")
        
        student_id = self.get_input("学号: ")
        if not student_id:
            return
        
        student = self.manager.get_student(student_id)
        if not student:
            print(f"学号 {student_id} 不存在。")
            self.pause()
            return
        
        print(f"\n学生: {student['name']} ({student['major']})")
        
        course = self.get_input("课程名称: ")
        if not course:
            return
        
        score = self.get_input("成绩 (0-100): ", float)
        if score is None:
            return
        
        self.manager.add_score(student_id, course, score)
        self.pause()
    
    def view_student_scores(self):
        """查看学生成绩"""
        self.print_header("查看学生成绩")
        
        student_id = self.get_input("请输入学号: ")
        if not student_id:
            return
        
        student = self.manager.get_student(student_id)
        if not student:
            print(f"学号 {student_id} 不存在。")
            self.pause()
            return
        
        print(f"\n{student['name']} ({student_id}) 的成绩:")
        
        if student['scores']:
            print("-" * 40)
            print(f"{'课程':<15} {'成绩':<8} {'等级':<5}")
            print("-" * 40)
            
            total_score = 0
            for course, score in student['scores'].items():
                grade = self.manager.get_grade(score)
                print(f"{course:<15} {score:<8} {grade:<5}")
                total_score += score
            
            print("-" * 40)
            avg_score = total_score / len(student['scores'])
            print(f"平均分: {avg_score:.2f} ({self.manager.get_grade(avg_score)})")
        else:
            print("暂无成绩记录。")
        
        self.pause()
    
    def view_course_statistics(self):
        """查看课程统计"""
        self.print_header("课程成绩统计")
        
        if not self.manager.courses:
            print("系统中还没有课程信息。")
            self.pause()
            return
        
        print("可选课程:")
        courses_list = sorted(self.manager.courses)
        for i, course in enumerate(courses_list, 1):
            print(f"{i}. {course}")
        
        choice = self.get_input("\n请选择课程编号或直接输入课程名称: ")
        
        if choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(courses_list):
                course = courses_list[choice_num - 1]
            else:
                print("无效的课程编号。")
                self.pause()
                return
        else:
            course = choice
        
        stats = self.manager.get_course_statistics(course)
        
        if 'error' in stats:
            print(f"\n{stats['error']}")
        else:
            print(f"\n{course} 课程统计:")
            print("-" * 50)
            print(f"学生人数: {stats['student_count']}")
            print(f"平均分: {stats['average']:.2f}")
            print(f"中位数: {stats['median']:.2f}")
            print(f"最高分: {stats['max_score']}")
            print(f"最低分: {stats['min_score']}")
            print(f"标准差: {stats['std_dev']:.2f}")
            
            print("\n等级分布:")
            for grade, count in sorted(stats['grade_distribution'].items()):
                print(f"  {grade}: {count} 人")
            
            print("\n成绩排名:")
            print("-" * 50)
            print(f"{'排名':<4} {'学号':<10} {'姓名':<10} {'成绩':<6} {'等级':<4}")
            print("-" * 50)
            
            for i, student in enumerate(stats['students'][:10], 1):  # 只显示前10名
                print(f"{i:<4} {student['student_id']:<10} {student['name']:<10} {student['score']:<6} {student['grade']:<4}")
        
        self.pause()
    
    def query_statistics_menu(self):
        """查询统计菜单"""
        while True:
            self.clear_screen()
            self.print_header("查询统计")
            print("\n1. 成绩排名")
            print("2. 专业统计")
            print("3. 优秀学生 (平均分90+)")
            print("4. 课程排名")
            print("0. 返回主菜单")
            print("-" * 60)
            
            choice = self.get_input("请选择操作 (0-4): ")
            
            if choice == "1":
                self.view_rankings()
            elif choice == "2":
                self.view_major_statistics()
            elif choice == "3":
                self.view_excellent_students()
            elif choice == "4":
                self.view_course_rankings()
            elif choice == "0":
                break
            else:
                print("无效选择，请重新输入。")
                self.pause()
    
    def view_rankings(self):
        """查看成绩排名"""
        self.print_header("成绩排名")
        
        n = self.get_input("显示前几名 (默认10): ", int, False) or 10
        
        top_students = self.manager.get_top_students(n)
        
        if top_students:
            print(f"\n平均分排名 (前{len(top_students)}名):")
            print("-" * 70)
            print(f"{'排名':<4} {'学号':<10} {'姓名':<10} {'专业':<15} {'平均分':<8} {'课程数':<6}")
            print("-" * 70)
            
            for i, student in enumerate(top_students, 1):
                print(f"{i:<4} {student['student_id']:<10} {student['name']:<10} {student['major']:<15} {student['average_score']:<8.2f} {student['course_count']:<6}")
        else:
            print("\n暂无学生成绩数据。")
        
        self.pause()
    
    def view_major_statistics(self):
        """查看专业统计"""
        self.print_header("专业统计")
        
        major_stats = self.manager.get_major_statistics()
        
        if major_stats:
            print("\n各专业统计信息:")
            print("=" * 80)
            
            for major, stats in major_stats.items():
                print(f"\n专业: {major}")
                print("-" * 40)
                print(f"学生人数: {stats['student_count']}")
                
                if 'average_score' in stats:
                    print(f"平均分: {stats['average_score']:.2f}")
                    print(f"中位数: {stats['median_score']:.2f}")
                    print(f"最高分: {stats['max_score']}")
                    print(f"最低分: {stats['min_score']}")
                    
                    print("\n优秀学生 (前3名):")
                    for i, student in enumerate(stats['students'][:3], 1):
                        avg = student['average']
                        avg_str = f"{avg:.2f}" if avg else "无"
                        print(f"  {i}. {student['name']} ({student['student_id']}) - {avg_str}")
                else:
                    print(f"{stats['message']}")
        else:
            print("\n暂无专业数据。")
        
        self.pause()
    
    def view_excellent_students(self):
        """查看优秀学生"""
        self.print_header("优秀学生 (平均分90+)")
        
        excellent_students = []
        for student_id, student_info in self.manager.students.items():
            avg_score = self.manager.calculate_student_average(student_id)
            if avg_score and avg_score >= 90:
                excellent_students.append({
                    'student_id': student_id,
                    'name': student_info['name'],
                    'major': student_info['major'],
                    'average_score': avg_score,
                    'course_count': len(student_info['scores'])
                })
        
        if excellent_students:
            # 按平均分降序排序
            excellent_students.sort(key=lambda x: x['average_score'], reverse=True)
            
            print(f"\n优秀学生名单 ({len(excellent_students)} 人):")
            print("-" * 70)
            print(f"{'排名':<4} {'学号':<10} {'姓名':<10} {'专业':<15} {'平均分':<8} {'课程数':<6}")
            print("-" * 70)
            
            for i, student in enumerate(excellent_students, 1):
                print(f"{i:<4} {student['student_id']:<10} {student['name']:<10} {student['major']:<15} {student['average_score']:<8.2f} {student['course_count']:<6}")
        else:
            print("\n暂无平均分90分以上的学生。")
        
        self.pause()
    
    def view_course_rankings(self):
        """查看课程排名"""
        self.print_header("课程排名")
        
        if not self.manager.courses:
            print("系统中还没有课程信息。")
            self.pause()
            return
        
        print("可选课程:")
        courses_list = sorted(self.manager.courses)
        for i, course in enumerate(courses_list, 1):
            print(f"{i}. {course}")
        
        choice = self.get_input("\n请选择课程编号或直接输入课程名称: ")
        
        if choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(courses_list):
                course = courses_list[choice_num - 1]
            else:
                print("无效的课程编号。")
                self.pause()
                return
        else:
            course = choice
        
        n = self.get_input("显示前几名 (默认10): ", int, False) or 10
        
        top_students = self.manager.get_top_students(n, course)
        
        if top_students:
            print(f"\n{course} 课程排名 (前{len(top_students)}名):")
            print("-" * 60)
            print(f"{'排名':<4} {'学号':<10} {'姓名':<10} {'专业':<15} {'成绩':<6} {'等级':<4}")
            print("-" * 60)
            
            for i, student in enumerate(top_students, 1):
                print(f"{i:<4} {student['student_id']:<10} {student['name']:<10} {student['major']:<15} {student['score']:<6} {student['grade']:<4}")
        else:
            print(f"\n{course} 课程暂无成绩数据。")
        
        self.pause()
    
    def data_management_menu(self):
        """数据管理菜单"""
        while True:
            self.clear_screen()
            self.print_header("数据管理")
            print("\n1. 导出到JSON文件")
            print("2. 从JSON文件导入")
            print("3. 导出到CSV文件")
            print("4. 清空所有数据")
            print("0. 返回主菜单")
            print("-" * 60)
            
            choice = self.get_input("请选择操作 (0-4): ")
            
            if choice == "1":
                self.export_json()
            elif choice == "2":
                self.import_json()
            elif choice == "3":
                self.export_csv()
            elif choice == "4":
                self.clear_all_data()
            elif choice == "0":
                break
            else:
                print("无效选择，请重新输入。")
                self.pause()
    
    def export_json(self):
        """导出JSON"""
        self.print_header("导出到JSON文件")
        
        filename = self.get_input("文件名 (默认: students_export.json): ", str, False) or "students_export.json"
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        success = self.manager.export_to_json(filename)
        if success:
            print(f"\n数据已成功导出到 {filename}")
        
        self.pause()
    
    def import_json(self):
        """导入JSON"""
        self.print_header("从JSON文件导入")
        
        filename = self.get_input("文件名: ")
        if not filename:
            return
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        if not os.path.exists(filename):
            print(f"文件 {filename} 不存在。")
            self.pause()
            return
        
        confirm = self.get_input("导入将覆盖现有数据，确认继续？(y/N): ")
        if confirm.lower() == 'y':
            success = self.manager.import_from_json(filename)
            if success:
                print(f"\n数据已成功从 {filename} 导入")
        else:
            print("操作已取消。")
        
        self.pause()
    
    def export_csv(self):
        """导出CSV"""
        self.print_header("导出到CSV文件")
        
        filename = self.get_input("文件名 (默认: students_export.csv): ", str, False) or "students_export.csv"
        
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        success = self.manager.export_to_csv(filename)
        if success:
            print(f"\n学生信息已成功导出到 {filename}")
        
        self.pause()
    
    def clear_all_data(self):
        """清空所有数据"""
        self.print_header("清空所有数据")
        
        print("警告：此操作将删除所有学生和成绩数据，且无法恢复！")
        confirm1 = self.get_input("确认清空所有数据？(yes/no): ")
        
        if confirm1.lower() == 'yes':
            confirm2 = self.get_input("再次确认，输入 'DELETE' 来确认删除: ")
            if confirm2 == 'DELETE':
                self.manager = StudentManager()  # 重新创建实例
                print("\n所有数据已清空。")
            else:
                print("确认码错误，操作已取消。")
        else:
            print("操作已取消。")
        
        self.pause()
    
    def show_system_info(self):
        """显示系统信息"""
        self.clear_screen()
        self.print_header("系统信息")
        
        self.manager.print_summary()
        
        print("\n数据结构使用情况:")
        print("-" * 50)
        print(f"主数据字典大小: {len(self.manager.students)} 个学生")
        print(f"专业集合大小: {len(self.manager.majors)} 个专业")
        print(f"课程集合大小: {len(self.manager.courses)} 门课程")
        print(f"等级配置元组: {len(self.manager.grade_config)} 个等级")
        
        # 内存使用估算
        import sys
        students_size = sys.getsizeof(self.manager.students)
        majors_size = sys.getsizeof(self.manager.majors)
        courses_size = sys.getsizeof(self.manager.courses)
        
        print(f"\n内存使用估算:")
        print(f"学生数据: ~{students_size} 字节")
        print(f"专业数据: ~{majors_size} 字节")
        print(f"课程数据: ~{courses_size} 字节")
        
        self.pause()
    
    def load_sample_data(self):
        """加载示例数据"""
        self.print_header("加载示例数据")
        
        if self.manager.students:
            confirm = self.get_input("系统中已有数据，是否继续添加示例数据？(y/N): ")
            if confirm.lower() != 'y':
                return
        
        print("正在加载示例数据...")
        
        # 添加示例学生
        sample_students = [
            ("2024001", "张三", "计算机科学", 20, "zhangsan@example.com"),
            ("2024002", "李四", "数学", 19, "lisi@example.com"),
            ("2024003", "王五", "计算机科学", 21, "wangwu@example.com"),
            ("2024004", "赵六", "物理", 20, "zhaoliu@example.com"),
            ("2024005", "钱七", "数学", 19, "qianqi@example.com"),
            ("2024006", "孙八", "化学", 22, "sunba@example.com"),
            ("2024007", "周九", "计算机科学", 20, "zhoujiu@example.com"),
            ("2024008", "吴十", "物理", 21, "wushi@example.com")
        ]
        
        for student_id, name, major, age, email in sample_students:
            self.manager.add_student(student_id, name, major, age, email)
        
        # 添加示例成绩
        sample_scores = [
            # 张三的成绩
            ("2024001", "数学", 95), ("2024001", "英语", 88), ("2024001", "程序设计", 92),
            ("2024001", "数据结构", 89), ("2024001", "计算机网络", 91),
            
            # 李四的成绩
            ("2024002", "数学", 98), ("2024002", "英语", 85), ("2024002", "高等数学", 96),
            ("2024002", "线性代数", 94), ("2024002", "概率论", 92),
            
            # 王五的成绩
            ("2024003", "数学", 82), ("2024003", "程序设计", 89), ("2024003", "数据结构", 91),
            ("2024003", "英语", 78), ("2024003", "操作系统", 85),
            
            # 赵六的成绩
            ("2024004", "数学", 87), ("2024004", "物理", 93), ("2024004", "英语", 79),
            ("2024004", "量子力学", 88), ("2024004", "电磁学", 90),
            
            # 钱七的成绩
            ("2024005", "数学", 94), ("2024005", "高等数学", 91), ("2024005", "线性代数", 89),
            ("2024005", "英语", 83), ("2024005", "数学分析", 95),
            
            # 孙八的成绩
            ("2024006", "数学", 86), ("2024006", "化学", 92), ("2024006", "英语", 81),
            ("2024006", "有机化学", 89), ("2024006", "无机化学", 87),
            
            # 周九的成绩
            ("2024007", "数学", 90), ("2024007", "程序设计", 94), ("2024007", "英语", 86),
            ("2024007", "数据结构", 92), ("2024007", "算法设计", 88),
            
            # 吴十的成绩
            ("2024008", "数学", 84), ("2024008", "物理", 89), ("2024008", "英语", 77),
            ("2024008", "理论力学", 91), ("2024008", "热力学", 85)
        ]
        
        for student_id, course, score in sample_scores:
            self.manager.add_score(student_id, course, score)
        
        print(f"\n示例数据加载完成！")
        print(f"已添加 {len(sample_students)} 个学生")
        print(f"已添加 {len(sample_scores)} 条成绩记录")
        
        self.pause()
    
    def run(self):
        """运行主程序"""
        while self.running:
            self.print_menu()
            choice = self.get_input("请选择操作 (0-6): ")
            
            if choice == "1":
                self.student_management_menu()
            elif choice == "2":
                self.score_management_menu()
            elif choice == "3":
                self.query_statistics_menu()
            elif choice == "4":
                self.data_management_menu()
            elif choice == "5":
                self.show_system_info()
            elif choice == "6":
                self.load_sample_data()
            elif choice == "0":
                print("\n感谢使用学生成绩管理系统！")
                print("这个项目演示了Python数据结构的实际应用：")
                print("- 字典：高效的学生信息存储和查找")
                print("- 集合：唯一性约束的专业和课程管理")
                print("- 列表：有序的成绩和排名数据")
                print("- 元组：不可变的配置信息")
                print("- defaultdict和Counter：简化统计和分组操作")
                print("\n继续学习Python，探索更多可能！")
                self.running = False
            else:
                print("无效选择，请重新输入。")
                self.pause()


if __name__ == "__main__":
    try:
        cli = StudentManagerCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断。")
    except Exception as e:
        print(f"\n程序发生错误: {e}")
        print("请检查输入或联系开发者。")