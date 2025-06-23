#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2：CRUD操作（增删改查）
学习如何进行数据的增加、删除、修改和查询操作
"""

import sqlite3
import os
from datetime import datetime

class EmployeeDatabase:
    """员工数据库管理类"""
    
    def __init__(self, db_name='employees.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        """创建员工表"""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            salary REAL NOT NULL,
            hire_date DATE NOT NULL
        )
        ''')
        self.conn.commit()
    
    # CREATE - 插入数据
    def add_employee(self, name, department, salary):
        """添加新员工"""
        hire_date = datetime.now().strftime('%Y-%m-%d')
        
        try:
            self.cursor.execute('''
            INSERT INTO employees (name, department, salary, hire_date)
            VALUES (?, ?, ?, ?)
            ''', (name, department, salary, hire_date))
            self.conn.commit()
            print(f"✓ 成功添加员工：{name}")
            return self.cursor.lastrowid
        except Exception as e:
            print(f"✗ 添加失败：{e}")
            return None
    
    # READ - 查询数据
    def get_all_employees(self):
        """获取所有员工"""
        self.cursor.execute('SELECT * FROM employees')
        return self.cursor.fetchall()
    
    def get_employee_by_id(self, emp_id):
        """根据ID获取员工"""
        self.cursor.execute('SELECT * FROM employees WHERE id = ?', (emp_id,))
        return self.cursor.fetchone()
    
    def search_employees(self, keyword):
        """搜索员工（按姓名或部门）"""
        self.cursor.execute('''
        SELECT * FROM employees 
        WHERE name LIKE ? OR department LIKE ?
        ''', (f'%{keyword}%', f'%{keyword}%'))
        return self.cursor.fetchall()
    
    # UPDATE - 更新数据
    def update_salary(self, emp_id, new_salary):
        """更新员工薪资"""
        self.cursor.execute('''
        UPDATE employees 
        SET salary = ? 
        WHERE id = ?
        ''', (new_salary, emp_id))
        
        if self.cursor.rowcount > 0:
            self.conn.commit()
            print(f"✓ 成功更新员工ID {emp_id} 的薪资")
            return True
        else:
            print(f"✗ 未找到ID为 {emp_id} 的员工")
            return False
    
    def transfer_department(self, emp_id, new_department):
        """调换部门"""
        self.cursor.execute('''
        UPDATE employees 
        SET department = ? 
        WHERE id = ?
        ''', (new_department, emp_id))
        
        if self.cursor.rowcount > 0:
            self.conn.commit()
            print(f"✓ 成功将员工调至 {new_department} 部门")
            return True
        return False
    
    # DELETE - 删除数据
    def delete_employee(self, emp_id):
        """删除员工"""
        # 先查询员工信息
        emp = self.get_employee_by_id(emp_id)
        if emp:
            self.cursor.execute('DELETE FROM employees WHERE id = ?', (emp_id,))
            self.conn.commit()
            print(f"✓ 成功删除员工：{emp[1]}")
            return True
        else:
            print(f"✗ 未找到ID为 {emp_id} 的员工")
            return False
    
    def display_employees(self):
        """显示所有员工"""
        employees = self.get_all_employees()
        
        if not employees:
            print("\n暂无员工数据")
            return
        
        print("\n员工列表：")
        print("-" * 70)
        print(f"{'ID':<5} {'姓名':<15} {'部门':<15} {'薪资':<15} {'入职日期':<15}")
        print("-" * 70)
        
        for emp in employees:
            print(f"{emp[0]:<5} {emp[1]:<15} {emp[2]:<15} "
                  f"¥{emp[3]:<14,.2f} {emp[4]:<15}")
    
    def close(self):
        """关闭数据库连接"""
        self.conn.close()

def demo_crud_operations():
    """演示CRUD操作"""
    print("CRUD操作演示")
    print("="*50)
    
    # 创建数据库实例
    db = EmployeeDatabase()
    
    # 1. CREATE - 添加员工
    print("\n1. 添加员工（CREATE）")
    db.add_employee("张三", "技术部", 15000)
    db.add_employee("李四", "市场部", 12000)
    db.add_employee("王五", "技术部", 18000)
    db.add_employee("赵六", "人事部", 10000)
    db.add_employee("钱七", "技术部", 20000)
    
    # 2. READ - 查询数据
    print("\n2. 查询数据（READ）")
    
    # 显示所有员工
    db.display_employees()
    
    # 搜索特定员工
    print("\n搜索技术部员工：")
    tech_employees = db.search_employees("技术部")
    for emp in tech_employees:
        print(f"  - {emp[1]} (薪资: ¥{emp[3]:,.2f})")
    
    # 3. UPDATE - 更新数据
    print("\n3. 更新数据（UPDATE）")
    
    # 给张三加薪
    db.update_salary(1, 18000)
    
    # 李四调换部门
    db.transfer_department(2, "技术部")
    
    print("\n更新后的员工列表：")
    db.display_employees()
    
    # 4. DELETE - 删除数据
    print("\n4. 删除数据（DELETE）")
    db.delete_employee(4)  # 删除赵六
    
    print("\n删除后的员工列表：")
    db.display_employees()
    
    # 高级查询示例
    print("\n5. 高级查询示例")
    
    # 统计各部门平均薪资
    db.cursor.execute('''
    SELECT department, AVG(salary) as avg_salary, COUNT(*) as count
    FROM employees
    GROUP BY department
    ''')
    
    print("\n各部门统计：")
    for row in db.cursor.fetchall():
        print(f"  {row[0]}: 平均薪资 ¥{row[1]:,.2f}, 人数 {row[2]}")
    
    # 找出薪资最高的员工
    db.cursor.execute('''
    SELECT * FROM employees
    ORDER BY salary DESC
    LIMIT 1
    ''')
    
    top_employee = db.cursor.fetchone()
    if top_employee:
        print(f"\n薪资最高的员工：{top_employee[1]} (¥{top_employee[3]:,.2f})")
    
    # 关闭数据库
    db.close()
    
    # 清理
    if os.path.exists('employees.db'):
        os.remove('employees.db')
        print("\n✓ 示例数据库已清理")

if __name__ == "__main__":
    demo_crud_operations()
    
    print("\n" + "="*50)
    print("CRUD操作总结：")
    print("- CREATE: INSERT INTO 语句")
    print("- READ: SELECT 语句")
    print("- UPDATE: UPDATE 语句")
    print("- DELETE: DELETE 语句")
    print("\n记住：")
    print("1. 使用参数化查询防止SQL注入")
    print("2. 检查操作结果（rowcount）")
    print("3. 记得提交事务（commit）")
    print("4. 妥善处理异常情况") 