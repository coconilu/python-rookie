#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session08 练习题2参考答案：学生成绩管理系统

这是exercise2.py的参考答案，展示了如何设计一个完整的Student类。
"""


class Student:
    """学生类 - 管理学生信息和成绩"""
    
    # 类变量
    total_students = 0
    school_name = "Python编程学院"
    passing_score = 60  # 及格分数线
    
    def __init__(self, name, student_id, age, grade_level):
        """初始化学生信息
        
        Args:
            name (str): 学生姓名
            student_id (str): 学号
            age (int): 年龄
            grade_level (str): 年级
        
        Raises:
            ValueError: 当参数无效时
            TypeError: 当参数类型不正确时
        """
        # 参数验证
        if not isinstance(name, str) or not name.strip():
            raise ValueError("姓名必须是非空字符串")
        if not isinstance(student_id, str) or not student_id.strip():
            raise ValueError("学号必须是非空字符串")
        if not isinstance(age, int) or age <= 0 or age > 150:
            raise ValueError("年龄必须是1-150之间的整数")
        if not isinstance(grade_level, str) or not grade_level.strip():
            raise ValueError("年级必须是非空字符串")
        
        # 初始化实例变量
        self.name = name.strip()
        self.student_id = student_id.strip()
        self.age = age
        self.grade_level = grade_level.strip()
        self.scores = {}  # 存储各科成绩，格式：{科目: 分数}
        
        # 更新学生总数
        Student.total_students += 1
        self.enrollment_number = Student.total_students
    
    def add_score(self, subject, score):
        """添加成绩
        
        Args:
            subject (str): 科目名称
            score (float): 分数
        
        Raises:
            ValueError: 当参数无效时
        """
        if not isinstance(subject, str) or not subject.strip():
            raise ValueError("科目名称必须是非空字符串")
        if not isinstance(score, (int, float)) or not (0 <= score <= 100):
            raise ValueError("分数必须在0-100之间")
        
        subject = subject.strip()
        old_score = self.scores.get(subject)
        self.scores[subject] = float(score)
        
        if old_score is None:
            print(f"添加成绩：{self.name} - {subject}: {score}分")
        else:
            print(f"更新成绩：{self.name} - {subject}: {old_score}分 -> {score}分")
    
    def remove_score(self, subject):
        """删除成绩
        
        Args:
            subject (str): 科目名称
        
        Returns:
            bool: 删除是否成功
        """
        if not isinstance(subject, str):
            return False
        
        subject = subject.strip()
        if subject in self.scores:
            removed_score = self.scores.pop(subject)
            print(f"删除成绩：{self.name} - {subject}: {removed_score}分")
            return True
        else:
            print(f"未找到科目：{subject}")
            return False
    
    def update_score(self, subject, new_score):
        """修改成绩
        
        Args:
            subject (str): 科目名称
            new_score (float): 新分数
        
        Returns:
            bool: 修改是否成功
        """
        if not isinstance(subject, str):
            return False
        
        subject = subject.strip()
        if subject in self.scores:
            self.add_score(subject, new_score)  # 复用add_score的验证逻辑
            return True
        else:
            print(f"未找到科目：{subject}，无法修改")
            return False
    
    def get_score(self, subject):
        """获取指定科目成绩
        
        Args:
            subject (str): 科目名称
        
        Returns:
            float or None: 成绩，如果科目不存在返回None
        """
        if not isinstance(subject, str):
            return None
        
        return self.scores.get(subject.strip())
    
    def calculate_average(self):
        """计算平均分
        
        Returns:
            float: 平均分，如果没有成绩返回0
        """
        if not self.scores:
            return 0.0
        
        total = sum(self.scores.values())
        average = total / len(self.scores)
        return round(average, 2)
    
    def get_highest_score(self):
        """获取最高分
        
        Returns:
            tuple: (科目, 分数)，如果没有成绩返回None
        """
        if not self.scores:
            return None
        
        max_subject = max(self.scores, key=self.scores.get)
        return (max_subject, self.scores[max_subject])
    
    def get_lowest_score(self):
        """获取最低分
        
        Returns:
            tuple: (科目, 分数)，如果没有成绩返回None
        """
        if not self.scores:
            return None
        
        min_subject = min(self.scores, key=self.scores.get)
        return (min_subject, self.scores[min_subject])
    
    def count_passing_subjects(self):
        """统计及格科目数量
        
        Returns:
            int: 及格科目数量
        """
        return sum(1 for score in self.scores.values() if score >= self.passing_score)
    
    def count_failing_subjects(self):
        """统计不及格科目数量
        
        Returns:
            int: 不及格科目数量
        """
        return sum(1 for score in self.scores.values() if score < self.passing_score)
    
    def get_failing_subjects(self):
        """获取不及格科目列表
        
        Returns:
            list: 不及格科目列表，格式：[(科目, 分数), ...]
        """
        return [(subject, score) for subject, score in self.scores.items() 
                if score < self.passing_score]
    
    def is_excellent_student(self, threshold=85.0):
        """判断是否为优秀学生
        
        Args:
            threshold (float): 优秀学生平均分阈值，默认85分
        
        Returns:
            bool: 是否为优秀学生
        """
        if not self.scores:
            return False
        
        average = self.calculate_average()
        return average >= threshold and self.count_failing_subjects() == 0
    
    def get_grade_distribution(self):
        """获取成绩分布
        
        Returns:
            dict: 成绩分布，格式：{'优秀': count, '良好': count, '及格': count, '不及格': count}
        """
        distribution = {'优秀': 0, '良好': 0, '及格': 0, '不及格': 0}
        
        for score in self.scores.values():
            if score >= 90:
                distribution['优秀'] += 1
            elif score >= 80:
                distribution['良好'] += 1
            elif score >= 60:
                distribution['及格'] += 1
            else:
                distribution['不及格'] += 1
        
        return distribution
    
    def get_student_info(self):
        """获取学生详细信息
        
        Returns:
            str: 格式化的学生信息
        """
        info = [
            f"学生信息：",
            f"  姓名：{self.name}",
            f"  学号：{self.student_id}",
            f"  年龄：{self.age}岁",
            f"  年级：{self.grade_level}",
            f"  入学编号：{self.enrollment_number}",
            f"  学校：{self.school_name}"
        ]
        
        if self.scores:
            info.extend([
                f"\n成绩信息：",
                f"  科目数量：{len(self.scores)}门",
                f"  平均分：{self.calculate_average()}分"
            ])
            
            highest = self.get_highest_score()
            lowest = self.get_lowest_score()
            if highest:
                info.append(f"  最高分：{highest[0]} {highest[1]}分")
            if lowest:
                info.append(f"  最低分：{lowest[0]} {lowest[1]}分")
            
            info.extend([
                f"  及格科目：{self.count_passing_subjects()}门",
                f"  不及格科目：{self.count_failing_subjects()}门",
                f"  优秀学生：{'是' if self.is_excellent_student() else '否'}"
            ])
            
            # 显示各科成绩
            info.append("\n各科成绩：")
            for subject, score in sorted(self.scores.items()):
                grade = self._get_grade_level(score)
                info.append(f"  {subject}: {score}分 ({grade})")
        else:
            info.append("\n暂无成绩记录")
        
        return "\n".join(info)
    
    def _get_grade_level(self, score):
        """根据分数获取等级
        
        Args:
            score (float): 分数
        
        Returns:
            str: 等级
        """
        if score >= 90:
            return "优秀"
        elif score >= 80:
            return "良好"
        elif score >= 60:
            return "及格"
        else:
            return "不及格"
    
    @classmethod
    def get_school_info(cls):
        """获取学校信息（类方法）
        
        Returns:
            str: 学校信息
        """
        return f"{cls.school_name} - 在校学生：{cls.total_students}人，及格线：{cls.passing_score}分"
    
    @classmethod
    def set_passing_score(cls, new_score):
        """设置及格分数线（类方法）
        
        Args:
            new_score (float): 新的及格分数线
        
        Raises:
            ValueError: 当分数无效时
        """
        if not isinstance(new_score, (int, float)) or not (0 <= new_score <= 100):
            raise ValueError("及格分数线必须在0-100之间")
        
        old_score = cls.passing_score
        cls.passing_score = float(new_score)
        print(f"及格分数线已更新：{old_score}分 -> {new_score}分")
    
    @classmethod
    def create_from_dict(cls, student_data):
        """从字典创建学生对象（类方法）
        
        Args:
            student_data (dict): 学生数据字典
        
        Returns:
            Student: 学生对象
        """
        required_keys = ['name', 'student_id', 'age', 'grade_level']
        for key in required_keys:
            if key not in student_data:
                raise ValueError(f"缺少必需字段：{key}")
        
        student = cls(
            student_data['name'],
            student_data['student_id'],
            student_data['age'],
            student_data['grade_level']
        )
        
        # 添加成绩（如果有）
        if 'scores' in student_data and isinstance(student_data['scores'], dict):
            for subject, score in student_data['scores'].items():
                student.add_score(subject, score)
        
        return student
    
    @staticmethod
    def is_valid_student_id(student_id):
        """验证学号格式（静态方法）
        
        Args:
            student_id (str): 学号
        
        Returns:
            bool: 是否为有效的学号格式
        """
        if not isinstance(student_id, str):
            return False
        
        # 简化的学号验证：8-12位数字或字母数字组合
        clean_id = student_id.strip()
        return 8 <= len(clean_id) <= 12 and clean_id.isalnum()
    
    @staticmethod
    def calculate_class_average(students):
        """计算班级平均分（静态方法）
        
        Args:
            students (list): 学生对象列表
        
        Returns:
            float: 班级平均分
        """
        if not students:
            return 0.0
        
        total_average = sum(student.calculate_average() for student in students)
        return round(total_average / len(students), 2)
    
    def __str__(self):
        """字符串表示（用户友好）"""
        avg = self.calculate_average()
        subject_count = len(self.scores)
        return f"{self.name}({self.student_id}) - {self.grade_level} - 平均分:{avg}分 ({subject_count}门课)"
    
    def __repr__(self):
        """字符串表示（开发者友好）"""
        return f"Student('{self.name}', '{self.student_id}', {self.age}, '{self.grade_level}')"
    
    def __eq__(self, other):
        """相等比较（按学号）"""
        if isinstance(other, Student):
            return self.student_id == other.student_id
        return False
    
    def __lt__(self, other):
        """小于比较（按平均分）"""
        if isinstance(other, Student):
            return self.calculate_average() < other.calculate_average()
        return NotImplemented
    
    def __hash__(self):
        """哈希值（基于学号）"""
        return hash(self.student_id)
    
    def __len__(self):
        """返回科目数量"""
        return len(self.scores)
    
    def __contains__(self, subject):
        """检查是否包含某科目"""
        return subject in self.scores


def test_student():
    """测试Student类的功能"""
    print("=== 学生成绩管理系统测试 ===")
    
    # 1. 创建学生对象
    print("\n1. 创建学生对象：")
    print("-" * 40)
    
    try:
        student1 = Student("张三", "20230001", 18, "高三")
        student2 = Student("李四", "20230002", 17, "高二")
        student3 = Student("王五", "20230003", 19, "高三")
        
        print("学生创建成功！")
        print(Student.get_school_info())
        
    except ValueError as e:
        print(f"创建学生失败：{e}")
    
    # 2. 添加成绩
    print("\n2. 添加成绩：")
    print("-" * 40)
    
    # 为张三添加成绩
    print("\n为张三添加成绩：")
    student1.add_score("数学", 95)
    student1.add_score("语文", 88)
    student1.add_score("英语", 92)
    student1.add_score("物理", 87)
    student1.add_score("化学", 90)
    
    # 为李四添加成绩
    print("\n为李四添加成绩：")
    student2.add_score("数学", 78)
    student2.add_score("语文", 85)
    student2.add_score("英语", 82)
    student2.add_score("历史", 75)
    student2.add_score("地理", 80)
    
    # 为王五添加成绩（包含不及格）
    print("\n为王五添加成绩：")
    student3.add_score("数学", 45)
    student3.add_score("语文", 72)
    student3.add_score("英语", 58)
    student3.add_score("物理", 65)
    
    # 3. 显示学生信息
    print("\n3. 学生信息：")
    print("-" * 40)
    
    students = [student1, student2, student3]
    for i, student in enumerate(students, 1):
        print(f"\n学生{i}：{student}")
        print(student.get_student_info())
    
    # 4. 测试成绩操作
    print("\n4. 成绩操作测试：")
    print("-" * 40)
    
    print("\n修改张三的数学成绩：")
    student1.update_score("数学", 98)
    
    print("\n删除李四的地理成绩：")
    student2.remove_score("地理")
    
    print("\n查询王五的英语成绩：")
    english_score = student3.get_score("英语")
    print(f"王五的英语成绩：{english_score}分")
    
    # 5. 统计分析
    print("\n5. 统计分析：")
    print("-" * 40)
    
    for student in students:
        print(f"\n{student.name}的成绩分析：")
        print(f"  平均分：{student.calculate_average()}分")
        
        highest = student.get_highest_score()
        lowest = student.get_lowest_score()
        if highest:
            print(f"  最高分：{highest[0]} {highest[1]}分")
        if lowest:
            print(f"  最低分：{lowest[0]} {lowest[1]}分")
        
        print(f"  及格科目：{student.count_passing_subjects()}门")
        print(f"  不及格科目：{student.count_failing_subjects()}门")
        print(f"  优秀学生：{'是' if student.is_excellent_student() else '否'}")
        
        # 显示不及格科目
        failing = student.get_failing_subjects()
        if failing:
            print(f"  不及格科目详情：{failing}")
        
        # 显示成绩分布
        distribution = student.get_grade_distribution()
        print(f"  成绩分布：{distribution}")
    
    # 6. 班级统计
    print("\n6. 班级统计：")
    print("-" * 40)
    
    class_average = Student.calculate_class_average(students)
    print(f"班级平均分：{class_average}分")
    
    # 按平均分排序
    sorted_students = sorted(students, reverse=True)  # 从高到低
    print("\n按平均分排名：")
    for i, student in enumerate(sorted_students, 1):
        print(f"  第{i}名：{student}")
    
    # 7. 测试类方法和静态方法
    print("\n7. 类方法和静态方法测试：")
    print("-" * 40)
    
    # 修改及格分数线
    print("\n修改及格分数线：")
    Student.set_passing_score(65)
    
    # 重新统计及格情况
    print("\n新及格线下的统计：")
    for student in students:
        passing = student.count_passing_subjects()
        failing = student.count_failing_subjects()
        print(f"  {student.name}：及格{passing}门，不及格{failing}门")
    
    # 测试学号验证
    print("\n学号验证测试：")
    test_ids = ["20230001", "123", "abcd1234", "20230001abc", ""]
    for test_id in test_ids:
        is_valid = Student.is_valid_student_id(test_id)
        print(f"  学号'{test_id}': {'有效' if is_valid else '无效'}")
    
    # 从字典创建学生
    print("\n从字典创建学生：")
    student_data = {
        'name': '赵六',
        'student_id': '20230004',
        'age': 18,
        'grade_level': '高三',
        'scores': {
            '数学': 85,
            '语文': 90,
            '英语': 88
        }
    }
    
    try:
        student4 = Student.create_from_dict(student_data)
        print(f"创建成功：{student4}")
        students.append(student4)
    except ValueError as e:
        print(f"创建失败：{e}")
    
    # 8. 测试特殊方法
    print("\n8. 特殊方法测试：")
    print("-" * 40)
    
    print(f"student1 == student2: {student1 == student2}")
    print(f"student1 < student2: {student1 < student2}")
    print(f"len(student1): {len(student1)}门课")
    print(f"'数学' in student1: {'数学' in student1}")
    print(f"'体育' in student1: {'体育' in student1}")
    
    # 9. 异常处理测试
    print("\n9. 异常处理测试：")
    print("-" * 40)
    
    try:
        # 测试无效参数
        invalid_student = Student("", "123", -5, "")
    except ValueError as e:
        print(f"捕获异常：{e}")
    
    try:
        # 测试无效成绩
        student1.add_score("体育", 150)
    except ValueError as e:
        print(f"捕获异常：{e}")
    
    try:
        # 测试无效及格线
        Student.set_passing_score(-10)
    except ValueError as e:
        print(f"捕获异常：{e}")
    
    # 10. 最终状态
    print("\n10. 最终状态：")
    print("-" * 40)
    
    print(Student.get_school_info())
    print(f"班级平均分：{Student.calculate_class_average(students)}分")
    
    print("\n所有学生：")
    for student in students:
        print(f"  {student}")
    
    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    test_student()