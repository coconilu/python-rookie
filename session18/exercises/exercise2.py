#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
练习2：数据操作练习
练习SQLAlchemy的各种查询和数据操作技巧

要求：
1. 完成基础查询操作
2. 实现复杂的关系查询
3. 练习聚合和分组查询
4. 掌握事务处理
5. 优化查询性能

学习目标：
- 熟练使用SQLAlchemy查询API
- 理解不同查询方法的应用场景
- 掌握性能优化技巧
- 学会处理复杂的业务逻辑
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, and_, or_, desc, text
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exercise2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==================== 模型定义 ====================

class Student(db.Model):
    """学生模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    major = db.Column(db.String(100))
    grade = db.Column(db.Integer)  # 年级
    gpa = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    enrollments = db.relationship('Enrollment', backref='student', lazy=True)
    
    def __repr__(self):
        return f'<Student {self.name}>'

class Course(db.Model):
    """课程模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    credits = db.Column(db.Integer, default=3)
    department = db.Column(db.String(100))
    description = db.Column(db.Text)
    instructor = db.Column(db.String(100))
    
    # 关系
    enrollments = db.relationship('Enrollment', backref='course', lazy=True)
    
    def __repr__(self):
        return f'<Course {self.name}>'

class Enrollment(db.Model):
    """选课记录模型"""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    semester = db.Column(db.String(20))  # 学期：2024春、2024秋
    grade = db.Column(db.String(2))  # 成绩：A, B, C, D, F
    credits_earned = db.Column(db.Integer, default=0)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Enrollment {self.student.name} - {self.course.name}>'

# ==================== 数据初始化 ====================

def create_sample_data():
    """创建示例数据"""
    # 创建课程
    courses_data = [
        ('Python编程', 'CS101', 3, '计算机科学', '张教授'),
        ('数据结构', 'CS201', 4, '计算机科学', '李教授'),
        ('数据库原理', 'CS301', 3, '计算机科学', '王教授'),
        ('Web开发', 'CS401', 3, '计算机科学', '赵教授'),
        ('机器学习', 'CS501', 4, '计算机科学', '孙教授'),
        ('高等数学', 'MATH101', 4, '数学', '陈教授'),
        ('线性代数', 'MATH201', 3, '数学', '刘教授'),
        ('大学英语', 'ENG101', 2, '外语', '周教授'),
    ]
    
    courses = []
    for name, code, credits, dept, instructor in courses_data:
        course = Course(name=name, code=code, credits=credits, 
                       department=dept, instructor=instructor)
        courses.append(course)
    
    db.session.add_all(courses)
    db.session.commit()
    
    # 创建学生
    students_data = [
        ('张三', '2021001', 'zhangsan@university.edu', 20, '男', '计算机科学', 3),
        ('李四', '2021002', 'lisi@university.edu', 19, '女', '计算机科学', 3),
        ('王五', '2022001', 'wangwu@university.edu', 19, '男', '计算机科学', 2),
        ('赵六', '2022002', 'zhaoliu@university.edu', 18, '女', '数学', 2),
        ('孙七', '2023001', 'sunqi@university.edu', 18, '男', '计算机科学', 1),
        ('周八', '2023002', 'zhouba@university.edu', 17, '女', '数学', 1),
        ('吴九', '2021003', 'wujiu@university.edu', 20, '男', '外语', 3),
        ('郑十', '2022003', 'zhengshi@university.edu', 19, '女', '外语', 2),
    ]
    
    students = []
    for name, student_id, email, age, gender, major, grade in students_data:
        student = Student(name=name, student_id=student_id, email=email,
                         age=age, gender=gender, major=major, grade=grade)
        students.append(student)
    
    db.session.add_all(students)
    db.session.commit()
    
    # 创建选课记录
    semesters = ['2024春', '2024秋']
    grades = ['A', 'B', 'C', 'D', 'F']
    
    for student in students:
        # 每个学生随机选择3-6门课程
        selected_courses = random.sample(courses, random.randint(3, 6))
        for course in selected_courses:
            enrollment = Enrollment(
                student=student,
                course=course,
                semester=random.choice(semesters),
                grade=random.choice(grades),
                credits_earned=course.credits if random.choice(grades[:4]) else 0
            )
            db.session.add(enrollment)
    
    db.session.commit()
    
    # 计算学生GPA
    for student in students:
        total_points = 0
        total_credits = 0
        grade_points = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}
        
        for enrollment in student.enrollments:
            if enrollment.grade in grade_points:
                points = grade_points[enrollment.grade] * enrollment.course.credits
                total_points += points
                total_credits += enrollment.course.credits
        
        if total_credits > 0:
            student.gpa = total_points / total_credits
    
    db.session.commit()

# ==================== 练习任务 ====================

def exercise_basic_queries():
    """练习1：基础查询操作"""
    print("\n=== 练习1：基础查询操作 ===")
    
    # TODO: 完成以下查询任务
    
    # 任务1.1：查询所有学生的姓名和专业
    print("任务1.1：查询所有学生的姓名和专业")
    # 提示：使用query和all()方法
    # students = Student.query.all()
    # for student in students:
    #     print(f"{student.name} - {student.major}")
    
    # 任务1.2：查询计算机科学专业的学生
    print("\n任务1.2：查询计算机科学专业的学生")
    # 提示：使用filter_by()方法
    
    # 任务1.3：查询GPA大于3.0的学生，按GPA倒序排列
    print("\n任务1.3：查询GPA大于3.0的学生，按GPA倒序排列")
    # 提示：使用filter()和order_by()方法
    
    # 任务1.4：查询年龄在18-20岁之间的学生
    print("\n任务1.4：查询年龄在18-20岁之间的学生")
    # 提示：使用between()或者多个条件
    
    # 任务1.5：查询前5名GPA最高的学生
    print("\n任务1.5：查询前5名GPA最高的学生")
    # 提示：使用order_by()和limit()方法

def exercise_relationship_queries():
    """练习2：关系查询操作"""
    print("\n=== 练习2：关系查询操作 ===")
    
    # TODO: 完成以下关系查询任务
    
    # 任务2.1：查询每个学生选修的课程数量
    print("任务2.1：查询每个学生选修的课程数量")
    # 提示：使用关系属性和len()函数
    
    # 任务2.2：查询"Python编程"课程的所有选课学生
    print("\n任务2.2：查询'Python编程'课程的所有选课学生")
    # 提示：先查询课程，然后通过关系查询学生
    
    # 任务2.3：查询张三同学选修的所有课程及成绩
    print("\n任务2.3：查询张三同学选修的所有课程及成绩")
    # 提示：通过学生的enrollments关系查询
    
    # 任务2.4：查询每门课程的选课人数
    print("\n任务2.4：查询每门课程的选课人数")
    # 提示：使用join和group_by
    
    # 任务2.5：查询同时选修了"Python编程"和"数据结构"的学生
    print("\n任务2.5：查询同时选修了'Python编程'和'数据结构'的学生")
    # 提示：使用子查询或复杂的join

def exercise_aggregation_queries():
    """练习3：聚合查询操作"""
    print("\n=== 练习3：聚合查询操作 ===")
    
    # TODO: 完成以下聚合查询任务
    
    # 任务3.1：统计各专业的学生人数
    print("任务3.1：统计各专业的学生人数")
    # 提示：使用func.count()和group_by()
    
    # 任务3.2：计算各专业学生的平均GPA
    print("\n任务3.2：计算各专业学生的平均GPA")
    # 提示：使用func.avg()和group_by()
    
    # 任务3.3：统计各年级的学生人数和平均年龄
    print("\n任务3.3：统计各年级的学生人数和平均年龄")
    # 提示：使用多个聚合函数
    
    # 任务3.4：查询选课人数最多的课程
    print("\n任务3.4：查询选课人数最多的课程")
    # 提示：使用聚合查询和order_by()
    
    # 任务3.5：统计每个学期的选课总数
    print("\n任务3.5：统计每个学期的选课总数")
    # 提示：在Enrollment表上进行聚合

def exercise_complex_queries():
    """练习4：复杂查询操作"""
    print("\n=== 练习4：复杂查询操作 ===")
    
    # TODO: 完成以下复杂查询任务
    
    # 任务4.1：查询GPA高于专业平均值的学生
    print("任务4.1：查询GPA高于专业平均值的学生")
    # 提示：使用子查询
    
    # 任务4.2：查询选课门数最多的学生
    print("\n任务4.2：查询选课门数最多的学生")
    # 提示：使用聚合查询和子查询
    
    # 任务4.3：查询没有获得A等级成绩的学生
    print("\n任务4.3：查询没有获得A等级成绩的学生")
    # 提示：使用NOT EXISTS或者左连接
    
    # 任务4.4：查询各专业GPA最高的学生
    print("\n任务4.4：查询各专业GPA最高的学生")
    # 提示：使用窗口函数或子查询
    
    # 任务4.5：查询课程平均分低于2.0的课程
    print("\n任务4.5：查询课程平均分低于2.0的课程")
    # 提示：需要将字母成绩转换为数字

def exercise_data_operations():
    """练习5：数据操作练习"""
    print("\n=== 练习5：数据操作练习 ===")
    
    # TODO: 完成以下数据操作任务
    
    # 任务5.1：批量更新学生邮箱域名
    print("任务5.1：批量更新学生邮箱域名")
    # 提示：将所有@university.edu改为@newuniversity.edu
    
    # 任务5.2：为所有计算机科学专业学生的GPA加0.1分
    print("\n任务5.2：为所有计算机科学专业学生的GPA加0.1分")
    # 提示：使用update()方法
    
    # 任务5.3：删除所有F等级的选课记录
    print("\n任务5.3：删除所有F等级的选课记录")
    # 提示：使用delete()方法，注意先保存数据用于恢复
    
    # 任务5.4：为优秀学生（GPA > 3.5）批量添加奖学金标记
    print("\n任务5.4：为优秀学生批量添加奖学金标记")
    # 提示：可以在Student模型中添加scholarship字段
    
    # 任务5.5：使用事务处理创建新学生和选课记录
    print("\n任务5.5：使用事务处理创建新学生和选课记录")
    # 提示：使用try-except和事务回滚

def exercise_performance_optimization():
    """练习6：性能优化练习"""
    print("\n=== 练习6：性能优化练习 ===")
    
    # TODO: 完成以下性能优化任务
    
    # 任务6.1：使用预加载查询学生及其选课信息
    print("任务6.1：使用预加载查询学生及其选课信息")
    # 提示：使用joinedload或subqueryload
    
    # 任务6.2：优化重复查询，使用一次查询获取所有需要的数据
    print("\n任务6.2：优化重复查询")
    # 提示：避免N+1查询问题
    
    # 任务6.3：使用索引优化查询性能
    print("\n任务6.3：使用索引优化查询性能")
    # 提示：在模型中添加适当的索引
    
    # 任务6.4：使用分页查询处理大量数据
    print("\n任务6.4：使用分页查询处理大量数据")
    # 提示：使用paginate()方法
    
    # 任务6.5：使用原生SQL进行复杂统计
    print("\n任务6.5：使用原生SQL进行复杂统计")
    # 提示：使用text()和execute()方法

# ==================== 主函数 ====================

def run_exercises():
    """运行所有练习"""
    print("=" * 60)
    print("练习2：数据操作练习")
    print("=" * 60)
    
    with app.app_context():
        # 创建表
        db.create_all()
        
        # 清空数据
        db.session.query(Enrollment).delete()
        db.session.query(Student).delete()
        db.session.query(Course).delete()
        db.session.commit()
        
        # 创建示例数据
        print("创建示例数据...")
        create_sample_data()
        print("示例数据创建完成！")
        
        # 运行练习
        exercise_basic_queries()
        exercise_relationship_queries()
        exercise_aggregation_queries()
        exercise_complex_queries()
        exercise_data_operations()
        exercise_performance_optimization()
    
    print("\n" + "=" * 60)
    print("练习2完成！")
    print("\n学习检查点：")
    print("1. ✓ 能够熟练使用基础查询方法")
    print("2. ✓ 理解并应用关系查询")
    print("3. ✓ 掌握聚合函数的使用")
    print("4. ✓ 能够编写复杂的查询语句")
    print("5. ✓ 了解性能优化的基本技巧")
    print("6. ✓ 掌握事务处理的重要性")
    print("\n继续学习建议：")
    print("- 多练习不同类型的查询")
    print("- 关注查询性能和优化")
    print("- 学习使用数据库分析工具")
    print("- 了解索引设计原则")

if __name__ == '__main__':
    run_exercises()

# ==================== 练习提示 ====================

"""
参考代码片段（仅供参考）：

# 基础查询示例
students = Student.query.filter(Student.major == '计算机科学').all()
high_gpa_students = Student.query.filter(Student.gpa > 3.0).order_by(desc(Student.gpa)).all()

# 关系查询示例
python_course = Course.query.filter_by(name='Python编程').first()
students_in_python = [enrollment.student for enrollment in python_course.enrollments]

# 聚合查询示例
major_stats = db.session.query(
    Student.major, 
    func.count(Student.id), 
    func.avg(Student.gpa)
).group_by(Student.major).all()

# 复杂查询示例
subquery = db.session.query(func.avg(Student.gpa)).filter(Student.major == 'CS').scalar_subquery()
above_avg = Student.query.filter(Student.gpa > subquery).all()

# 批量操作示例
Student.query.filter(Student.major == '计算机科学').update({Student.gpa: Student.gpa + 0.1})

# 预加载示例
students_with_courses = Student.query.options(db.joinedload(Student.enrollments)).all()
""" 