#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
示例3：数据操作示例
演示SQLAlchemy高级查询和数据操作技巧

学习要点：
1. 高级查询技巧
2. 聚合函数和分组
3. 子查询和连接
4. 批量操作
5. 事务处理
6. 性能优化
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, and_, or_, desc, asc, text
from datetime import datetime, timedelta
import random

# 创建Flask应用和数据库实例
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==================== 模型定义 ====================

class Department(db.Model):
    """部门模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    budget = db.Column(db.Numeric(15, 2))
    
    # 一对多关系：部门有多个员工
    employees = db.relationship('Employee', backref='department', lazy='dynamic')
    
    def __repr__(self):
        return f'<Department {self.name}>'

class Employee(db.Model):
    """员工模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    salary = db.Column(db.Numeric(10, 2))
    hire_date = db.Column(db.Date, default=datetime.utcnow().date)
    position = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    
    # 外键
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    manager_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    
    # 自引用关系：经理-下属
    subordinates = db.relationship('Employee', backref=db.backref('manager', remote_side=[id]))
    
    def __repr__(self):
        return f'<Employee {self.name}>'

class Project(db.Model):
    """项目模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    budget = db.Column(db.Numeric(15, 2))
    status = db.Column(db.String(20), default='Planning')  # Planning, Active, Completed, Cancelled
    
    def __repr__(self):
        return f'<Project {self.name}>'

# 多对多关系：员工参与项目
employee_project = db.Table('employee_project',
    db.Column('employee_id', db.Integer, db.ForeignKey('employee.id'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True),
    db.Column('role', db.String(50)),  # 角色：Manager, Developer, Tester
    db.Column('hours_allocated', db.Integer),  # 分配工时
    db.Column('join_date', db.Date, default=datetime.utcnow().date)
)

# 为模型添加多对多关系
Employee.projects = db.relationship('Project', secondary=employee_project, 
                                  backref=db.backref('team_members', lazy='dynamic'))

# ==================== 数据初始化 ====================

def create_sample_data():
    """创建示例数据"""
    print("创建示例数据...")
    
    # 创建部门
    departments = [
        Department(name='技术部', location='北京', budget=1000000),
        Department(name='市场部', location='上海', budget=500000),
        Department(name='人事部', location='广州', budget=300000),
        Department(name='财务部', location='深圳', budget=200000),
    ]
    db.session.add_all(departments)
    db.session.commit()
    
    # 创建员工
    employees_data = [
        ('张三', 'zhangsan@company.com', '技术部', '高级工程师', 15000, None),
        ('李四', 'lisi@company.com', '技术部', '技术经理', 20000, '张三'),
        ('王五', 'wangwu@company.com', '技术部', '初级工程师', 8000, '李四'),
        ('赵六', 'zhaoliu@company.com', '技术部', '中级工程师', 12000, '李四'),
        ('孙七', 'sunqi@company.com', '市场部', '市场专员', 9000, None),
        ('周八', 'zhouba@company.com', '市场部', '市场经理', 18000, '孙七'),
        ('吴九', 'wujiu@company.com', '人事部', 'HR专员', 7000, None),
        ('郑十', 'zhengshi@company.com', '财务部', '会计', 9500, None),
    ]
    
    employees = []
    for name, email, dept_name, position, salary, manager_name in employees_data:
        dept = Department.query.filter_by(name=dept_name).first()
        employee = Employee(
            name=name,
            email=email,
            department=dept,
            position=position,
            salary=salary,
            hire_date=datetime.utcnow().date() - timedelta(days=random.randint(30, 365))
        )
        employees.append(employee)
    
    db.session.add_all(employees)
    db.session.commit()
    
    # 设置经理关系
    for name, email, dept_name, position, salary, manager_name in employees_data:
        if manager_name:
            employee = Employee.query.filter_by(name=name).first()
            manager = Employee.query.filter_by(name=manager_name).first()
            if manager:
                employee.manager = manager
    
    db.session.commit()
    
    # 创建项目
    projects = [
        Project(name='ERP系统升级', description='企业资源规划系统升级', 
               start_date=datetime(2024, 1, 1).date(), end_date=datetime(2024, 6, 30).date(),
               budget=500000, status='Active'),
        Project(name='移动应用开发', description='公司官方移动应用开发',
               start_date=datetime(2024, 2, 1).date(), end_date=datetime(2024, 8, 31).date(),
               budget=300000, status='Active'),
        Project(name='数据分析平台', description='内部数据分析和报告平台',
               start_date=datetime(2024, 3, 1).date(), end_date=datetime(2024, 12, 31).date(),
               budget=800000, status='Planning'),
        Project(name='客户管理系统', description='CRM系统开发和实施',
               start_date=datetime(2023, 10, 1).date(), end_date=datetime(2024, 3, 31).date(),
               budget=400000, status='Completed'),
    ]
    db.session.add_all(projects)
    db.session.commit()
    
    # 分配员工到项目
    project_assignments = [
        ('张三', 'ERP系统升级', 'Developer', 40),
        ('李四', 'ERP系统升级', 'Manager', 20),
        ('王五', 'ERP系统升级', 'Developer', 40),
        ('赵六', 'ERP系统升级', 'Tester', 30),
        ('张三', '移动应用开发', 'Developer', 20),
        ('王五', '移动应用开发', 'Developer', 30),
        ('李四', '数据分析平台', 'Manager', 15),
        ('赵六', '数据分析平台', 'Developer', 35),
        ('张三', '客户管理系统', 'Developer', 40),
        ('李四', '客户管理系统', 'Manager', 25),
    ]
    
    for emp_name, proj_name, role, hours in project_assignments:
        employee = Employee.query.filter_by(name=emp_name).first()
        project = Project.query.filter_by(name=proj_name).first()
        if employee and project:
            # 使用原生SQL插入关联表数据
            db.session.execute(
                employee_project.insert().values(
                    employee_id=employee.id,
                    project_id=project.id,
                    role=role,
                    hours_allocated=hours,
                    join_date=datetime.utcnow().date() - timedelta(days=random.randint(1, 90))
                )
            )
    
    db.session.commit()
    print("示例数据创建完成！")

# ==================== 高级查询演示 ====================

def demonstrate_basic_queries():
    """基础查询演示"""
    print("\n=== 基础查询演示 ===")
    
    # 简单查询
    print("1. 所有部门:")
    for dept in Department.query.all():
        print(f"  {dept.name} - {dept.location}")
    
    # 条件查询
    print("\n2. 技术部员工:")
    tech_dept = Department.query.filter_by(name='技术部').first()
    for emp in tech_dept.employees:
        print(f"  {emp.name} - {emp.position} - ${emp.salary}")
    
    # 复合条件查询
    print("\n3. 高薪员工 (薪资 > 10000):")
    high_salary_employees = Employee.query.filter(Employee.salary > 10000).all()
    for emp in high_salary_employees:
        print(f"  {emp.name} - ${emp.salary}")
    
    # 排序查询
    print("\n4. 按薪资倒序排列的员工:")
    sorted_employees = Employee.query.order_by(desc(Employee.salary)).limit(5).all()
    for emp in sorted_employees:
        print(f"  {emp.name} - ${emp.salary}")

def demonstrate_aggregation_queries():
    """聚合查询演示"""
    print("\n=== 聚合查询演示 ===")
    
    # 统计函数
    print("1. 基本统计:")
    total_employees = Employee.query.count()
    avg_salary = db.session.query(func.avg(Employee.salary)).scalar()
    max_salary = db.session.query(func.max(Employee.salary)).scalar()
    min_salary = db.session.query(func.min(Employee.salary)).scalar()
    
    print(f"  总员工数: {total_employees}")
    print(f"  平均薪资: ${avg_salary:.2f}")
    print(f"  最高薪资: ${max_salary}")
    print(f"  最低薪资: ${min_salary}")
    
    # 分组查询
    print("\n2. 各部门员工统计:")
    dept_stats = db.session.query(
        Department.name,
        func.count(Employee.id).label('employee_count'),
        func.avg(Employee.salary).label('avg_salary'),
        func.sum(Employee.salary).label('total_salary')
    ).join(Employee).group_by(Department.id).all()
    
    for dept_name, count, avg_sal, total_sal in dept_stats:
        print(f"  {dept_name}: {count}人, 平均薪资${avg_sal:.2f}, 总薪资${total_sal}")
    
    # 条件分组查询
    print("\n3. 各职位薪资统计:")
    position_stats = db.session.query(
        Employee.position,
        func.count(Employee.id).label('count'),
        func.avg(Employee.salary).label('avg_salary')
    ).group_by(Employee.position).having(func.count(Employee.id) > 1).all()
    
    for position, count, avg_sal in position_stats:
        print(f"  {position}: {count}人, 平均薪资${avg_sal:.2f}")

def demonstrate_advanced_queries():
    """高级查询演示"""
    print("\n=== 高级查询演示 ===")
    
    # 子查询
    print("1. 子查询 - 薪资高于平均值的员工:")
    avg_salary_subquery = db.session.query(func.avg(Employee.salary)).scalar_subquery()
    above_avg_employees = Employee.query.filter(Employee.salary > avg_salary_subquery).all()
    for emp in above_avg_employees:
        print(f"  {emp.name} - ${emp.salary}")
    
    # 连接查询
    print("\n2. 连接查询 - 员工及其部门信息:")
    results = db.session.query(Employee, Department).join(Department).limit(5).all()
    for emp, dept in results:
        print(f"  {emp.name} - {dept.name} ({dept.location})")
    
    # 外连接查询
    print("\n3. 左外连接 - 所有部门及员工数:")
    dept_emp_count = db.session.query(
        Department.name,
        func.count(Employee.id).label('employee_count')
    ).outerjoin(Employee).group_by(Department.id).all()
    
    for dept_name, count in dept_emp_count:
        print(f"  {dept_name}: {count}人")
    
    # 复杂条件查询
    print("\n4. 复杂条件 - 技术部高级职位或其他部门经理:")
    complex_query = Employee.query.filter(
        or_(
            and_(Department.name == '技术部', Employee.position.like('%工程师')),
            Employee.position.like('%经理')
        )
    ).join(Department).all()
    
    for emp in complex_query:
        print(f"  {emp.name} - {emp.position} ({emp.department.name})")

def demonstrate_relationship_queries():
    """关系查询演示"""
    print("\n=== 关系查询演示 ===")
    
    # 预加载关系数据
    print("1. 预加载查询 - 员工及其部门:")
    employees_with_dept = Employee.query.options(db.joinedload(Employee.department)).limit(3).all()
    for emp in employees_with_dept:
        print(f"  {emp.name} - {emp.department.name}")
    
    # 关系过滤
    print("\n2. 关系过滤 - 有员工的部门:")
    departments_with_employees = Department.query.filter(Department.employees.any()).all()
    for dept in departments_with_employees:
        print(f"  {dept.name}: {dept.employees.count()}人")
    
    # 多对多关系查询
    print("\n3. 多对多关系 - 项目团队成员:")
    projects_with_team = Project.query.filter(Project.team_members.any()).all()
    for project in projects_with_team:
        print(f"  {project.name}:")
        # 查询项目成员及其角色
        members = db.session.query(Employee, employee_project.c.role, employee_project.c.hours_allocated).\
            join(employee_project).filter(employee_project.c.project_id == project.id).all()
        for member, role, hours in members:
            print(f"    - {member.name} ({role}, {hours}h)")
    
    # 自引用关系查询
    print("\n4. 自引用关系 - 经理和下属:")
    managers = Employee.query.filter(Employee.subordinates.any()).all()
    for manager in managers:
        print(f"  经理 {manager.name}:")
        for subordinate in manager.subordinates:
            print(f"    - {subordinate.name}")

def demonstrate_dynamic_queries():
    """动态查询演示"""
    print("\n=== 动态查询演示 ===")
    
    # 构建动态查询条件
    def build_employee_query(department=None, min_salary=None, position=None):
        query = Employee.query
        
        if department:
            query = query.join(Department).filter(Department.name == department)
        
        if min_salary:
            query = query.filter(Employee.salary >= min_salary)
        
        if position:
            query = query.filter(Employee.position.like(f'%{position}%'))
        
        return query
    
    print("1. 动态条件查询:")
    
    # 查询技术部薪资大于10000的工程师
    engineers = build_employee_query(department='技术部', min_salary=10000, position='工程师').all()
    print(f"  技术部高薪工程师: {[emp.name for emp in engineers]}")
    
    # 查询所有经理
    managers = build_employee_query(position='经理').all()
    print(f"  所有经理: {[emp.name for emp in managers]}")
    
    # 分页查询
    print("\n2. 分页查询:")
    page = Employee.query.paginate(page=1, per_page=3, error_out=False)
    print(f"  第1页员工 (每页3人):")
    for emp in page.items:
        print(f"    {emp.name}")
    print(f"  总页数: {page.pages}, 总记录数: {page.total}")

def demonstrate_bulk_operations():
    """批量操作演示"""
    print("\n=== 批量操作演示 ===")
    
    # 批量更新
    print("1. 批量更新 - 给技术部员工加薪10%:")
    tech_dept = Department.query.filter_by(name='技术部').first()
    old_salaries = [(emp.name, emp.salary) for emp in tech_dept.employees]
    
    # 更新薪资
    db.session.query(Employee).filter(Employee.department_id == tech_dept.id).\
        update({Employee.salary: Employee.salary * 1.1}, synchronize_session=False)
    db.session.commit()
    
    print("  薪资变化:")
    for emp in tech_dept.employees:
        old_salary = next(sal for name, sal in old_salaries if name == emp.name)
        print(f"    {emp.name}: ${old_salary} -> ${emp.salary}")
    
    # 批量插入（演示）
    print("\n2. 批量插入演示:")
    new_employees_data = [
        {'name': '临时员工1', 'email': 'temp1@company.com', 'salary': 5000, 'position': '实习生'},
        {'name': '临时员工2', 'email': 'temp2@company.com', 'salary': 5000, 'position': '实习生'},
    ]
    
    for emp_data in new_employees_data:
        emp = Employee(**emp_data)
        db.session.add(emp)
    
    db.session.commit()
    print(f"  添加了 {len(new_employees_data)} 名临时员工")
    
    # 清理临时数据
    db.session.query(Employee).filter(Employee.position == '实习生').delete()
    db.session.commit()
    print("  清理了临时员工数据")

def demonstrate_transaction_handling():
    """事务处理演示"""
    print("\n=== 事务处理演示 ===")
    
    try:
        # 开始事务
        print("1. 事务处理 - 创建新部门和员工:")
        
        # 创建新部门
        new_dept = Department(name='研发部', location='杭州', budget=1500000)
        db.session.add(new_dept)
        db.session.flush()  # 获取ID但不提交
        
        # 创建新员工
        new_employee = Employee(
            name='新员工',
            email='new@company.com',
            department=new_dept,
            position='研发工程师',
            salary=12000
        )
        db.session.add(new_employee)
        
        # 模拟可能的错误
        # raise Exception("模拟错误")
        
        # 提交事务
        db.session.commit()
        print(f"  成功创建部门: {new_dept.name}")
        print(f"  成功创建员工: {new_employee.name}")
        
    except Exception as e:
        # 回滚事务
        db.session.rollback()
        print(f"  事务回滚: {str(e)}")
    
    # 使用上下文管理器
    print("\n2. 使用上下文管理器:")
    try:
        with db.session.begin():
            # 在这个块中的所有操作都在同一个事务中
            temp_dept = Department(name='临时部门', location='临时地点', budget=0)
            db.session.add(temp_dept)
            # 如果出现异常，会自动回滚
            # 如果成功，会自动提交
            
        print("  临时部门创建成功")
        
        # 清理
        db.session.delete(temp_dept)
        db.session.commit()
        print("  临时部门已清理")
        
    except Exception as e:
        print(f"  事务失败: {str(e)}")

def main():
    """主函数"""
    print("=" * 60)
    print("示例3：数据操作演示")
    print("=" * 60)
    
    with app.app_context():
        # 创建表
        db.create_all()
        
        # 清空数据
        db.session.query(Employee).delete()
        db.session.query(Department).delete()
        db.session.query(Project).delete()
        db.session.execute(employee_project.delete())
        db.session.commit()
        
        # 创建示例数据
        create_sample_data()
        
        # 运行演示
        demonstrate_basic_queries()
        demonstrate_aggregation_queries()
        demonstrate_advanced_queries()
        demonstrate_relationship_queries()
        demonstrate_dynamic_queries()
        demonstrate_bulk_operations()
        demonstrate_transaction_handling()
    
    print("\n" + "=" * 60)
    print("示例3完成！")
    print("学习要点总结：")
    print("1. 基础查询：filter, filter_by, order_by, limit等")
    print("2. 聚合查询：func.count, func.avg, group_by, having等")
    print("3. 高级查询：子查询、连接、复杂条件等")
    print("4. 关系查询：预加载、关系过滤、多对多查询等")
    print("5. 动态查询：条件构建、分页查询等")
    print("6. 批量操作：批量更新、批量插入等")
    print("7. 事务处理：提交、回滚、上下文管理器等")
    print("=" * 60)

if __name__ == '__main__':
    main() 