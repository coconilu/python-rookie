#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session08 示例1：基本类的定义和使用

本示例演示了：
- 如何定义一个简单的类
- 如何创建对象实例
- 如何使用构造函数初始化对象
- 如何定义和调用实例方法
"""


class Person:
    """人员类 - 演示基本的类定义"""
    
    def __init__(self, name, age, gender):
        """构造函数，初始化人员信息"""
        self.name = name
        self.age = age
        self.gender = gender
        self.hobbies = []  # 爱好列表
    
    def introduce(self):
        """自我介绍"""
        return f"大家好，我叫{self.name}，今年{self.age}岁，性别{self.gender}"
    
    def add_hobby(self, hobby):
        """添加爱好"""
        if hobby not in self.hobbies:
            self.hobbies.append(hobby)
            print(f"{self.name}添加了新爱好：{hobby}")
        else:
            print(f"{self.name}已经有这个爱好了：{hobby}")
    
    def remove_hobby(self, hobby):
        """移除爱好"""
        if hobby in self.hobbies:
            self.hobbies.remove(hobby)
            print(f"{self.name}移除了爱好：{hobby}")
        else:
            print(f"{self.name}没有这个爱好：{hobby}")
    
    def get_hobbies(self):
        """获取爱好列表"""
        if self.hobbies:
            return f"{self.name}的爱好：{', '.join(self.hobbies)}"
        else:
            return f"{self.name}还没有添加任何爱好"
    
    def celebrate_birthday(self):
        """过生日，年龄增加1"""
        self.age += 1
        print(f"🎉 {self.name}过生日了！现在{self.age}岁了！")
    
    def is_adult(self):
        """判断是否成年"""
        return self.age >= 18


def main():
    """主函数"""
    print("示例1：基本类的定义和使用")
    print("=" * 40)
    
    # 创建人员对象
    person1 = Person("张三", 25, "男")
    person2 = Person("李四", 17, "女")
    person3 = Person("王五", 30, "男")
    
    # 自我介绍
    print("\n1. 自我介绍：")
    print(person1.introduce())
    print(person2.introduce())
    print(person3.introduce())
    
    # 添加爱好
    print("\n2. 添加爱好：")
    person1.add_hobby("编程")
    person1.add_hobby("读书")
    person1.add_hobby("游泳")
    person1.add_hobby("编程")  # 重复添加
    
    person2.add_hobby("画画")
    person2.add_hobby("音乐")
    
    # 查看爱好
    print("\n3. 查看爱好：")
    print(person1.get_hobbies())
    print(person2.get_hobbies())
    print(person3.get_hobbies())
    
    # 移除爱好
    print("\n4. 移除爱好：")
    person1.remove_hobby("游泳")
    person1.remove_hobby("跑步")  # 移除不存在的爱好
    print(person1.get_hobbies())
    
    # 过生日
    print("\n5. 过生日：")
    person2.celebrate_birthday()
    print(person2.introduce())
    
    # 判断是否成年
    print("\n6. 成年判断：")
    people = [person1, person2, person3]
    for person in people:
        status = "成年人" if person.is_adult() else "未成年人"
        print(f"{person.name}（{person.age}岁）是{status}")
    
    # 对象属性直接访问
    print("\n7. 直接访问对象属性：")
    print(f"person1的姓名：{person1.name}")
    print(f"person1的年龄：{person1.age}")
    print(f"person1的性别：{person1.gender}")
    print(f"person1的爱好列表：{person1.hobbies}")
    
    # 修改属性
    print("\n8. 修改对象属性：")
    print(f"修改前：{person3.name}")
    person3.name = "王小五"
    print(f"修改后：{person3.name}")
    print(person3.introduce())


if __name__ == "__main__":
    main()