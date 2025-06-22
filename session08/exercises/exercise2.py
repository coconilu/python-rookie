#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session08 练习题2：学生成绩管理系统

题目描述：
设计一个Student类，用于管理学生的成绩信息：
1. 属性：学号(student_id)、姓名(name)、年龄(age)、班级(class_name)
2. 成绩管理：
   - 添加科目成绩
   - 删除科目成绩
   - 修改科目成绩
   - 计算平均分
   - 获取最高分和最低分
   - 获取及格科目数量
3. 类变量：
   - 学生总数
   - 学校名称

要求：
- 成绩范围为0-100
- 及格分数为60分
- 实现__str__和__repr__方法
- 添加类方法获取学校信息
- 添加静态方法判断成绩是否及格

输入示例：
创建学生对象，添加各科成绩，进行成绩统计

输出示例：
学生信息、各科成绩、统计结果等

提示：
- 使用字典存储科目和成绩
- 在添加成绩时验证分数范围
- 计算平均分时要处理空成绩的情况
"""

# 在这里编写你的代码

class Student:
    """学生类"""
    
    # 类变量
    total_students = 0
    school_name = "Python学院"
    
    def __init__(self, student_id, name, age, class_name):
        """初始化学生信息"""
        # 在这里实现构造函数
        pass
    
    # 在这里添加其他方法
    

def test_student():
    """测试Student类的功能"""
    print("=== 学生成绩管理系统测试 ===")
    
    # 测试代码将在这里编写
    pass


if __name__ == "__main__":
    test_student()