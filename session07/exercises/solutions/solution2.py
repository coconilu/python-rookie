#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session07 练习2解答：CSV和JSON文件操作

这个文件包含了练习2的完整解答。
学习者可以参考这些解答来理解正确的实现方法。

作者: Python教程团队
创建日期: 2024-12-22
"""

import csv
import json
import os
import glob
import time
from datetime import datetime, timedelta
import random
from copy import deepcopy


def exercise1_create_employee_csv():
    """
    练习1解答：创建员工CSV文件
    """
    filename = 'employees.csv'
    
    # 准备员工数据
    employees = [
        {'员工ID': 'E001', '姓名': '张三', '部门': '技术部', '职位': '软件工程师', '薪资': 12000, '入职日期': '2022-03-15'},
        {'员工ID': 'E002', '姓名': '李四', '部门': '销售部', '职位': '销售经理', '薪资': 15000, '入职日期': '2021-08-20'},
        {'员工ID': 'E003', '姓名': '王五', '部门': '人事部', '职位': 'HR专员', '薪资': 8000, '入职日期': '2023-01-10'},
        {'员工ID': 'E004', '姓名': '赵六', '部门': '技术部', '职位': '前端开发', '薪资': 10000, '入职日期': '2022-11-05'},
        {'员工ID': 'E005', '姓名': '钱七', '部门': '财务部', '职位': '会计师', '薪资': 9000, '入职日期': '2021-12-01'},
        {'员工ID': 'E006', '姓名': '孙八', '部门': '技术部', '职位': '架构师', '薪资': 18000, '入职日期': '2020-06-15'},
        {'员工ID': 'E007', '姓名': '周九', '部门': '市场部', '职位': '市场专员', '薪资': 7500, '入职日期': '2023-04-20'},
        {'员工ID': 'E008', '姓名': '吴十', '部门': '销售部', '职位': '销售代表', '薪资': 6500, '入职日期': '2023-02-28'},
        {'员工ID': 'E009', '姓名': '郑十一', '部门': '技术部', '职位': '测试工程师', '薪资': 9500, '入职日期': '2022-09-10'},
        {'员工ID': 'E010', '姓名': '王十二', '部门': '财务部', '职位': '财务经理', '薪资': 14000, '入职日期': '2021-05-18'}
    ]
    
    # 写入CSV文件
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['员工ID', '姓名', '部门', '职位', '薪资', '入职日期']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # 写入标题行
        writer.writeheader()
        
        # 写入数据行
        for employee in employees:
            writer.writerow(employee)
    
    print(f"✓ 创建员工CSV文件：{filename}，包含 {len(employees)} 个员工")
    return len(employees)


def exercise2_read_and_filter_csv():
    """
    练习2解答：读取和筛选CSV数据
    """
    input_filename = 'employees.csv'
    output_filename = 'high_salary_employees.csv'
    
    if not os.path.exists(input_filename):
        print(f"❌ 文件 {input_filename} 不存在，请先运行练习1")
        return None
    
    high_salary_employees = []
    
    # 读取CSV文件
    with open(input_filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            salary = int(row['薪资'])
            if salary >= 8000:  # 筛选高薪员工
                high_salary_employees.append(row)
    
    # 按薪资从高到低排序
    high_salary_employees.sort(key=lambda x: int(x['薪资']), reverse=True)
    
    # 写入新的CSV文件
    if high_salary_employees:
        with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['员工ID', '姓名', '部门', '职位', '薪资', '入职日期']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for employee in high_salary_employees:
                writer.writerow(employee)
    
    # 计算平均薪资
    if high_salary_employees:
        total_salary = sum(int(emp['薪资']) for emp in high_salary_employees)
        avg_salary = total_salary / len(high_salary_employees)
    else:
        avg_salary = 0
    
    print(f"✓ 筛选出 {len(high_salary_employees)} 个高薪员工")
    print(f"✓ 平均薪资：{avg_salary:.0f} 元")
    print(f"✓ 结果保存到：{output_filename}")
    
    return (len(high_salary_employees), avg_salary)


def exercise3_csv_data_analysis():
    """
    练习3解答：CSV数据分析
    """
    filename = 'employees.csv'
    output_filename = 'employee_analysis.json'
    
    if not os.path.exists(filename):
        print(f"❌ 文件 {filename} 不存在，请先运行练习1")
        return None
    
    employees = []
    
    # 读取员工数据
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            employees.append(row)
    
    # 分析数据
    analysis_result = {
        'analysis_date': datetime.now().isoformat(),
        'total_employees': len(employees),
        'department_analysis': {},
        'position_analysis': {},
        'hiring_year_analysis': {}
    }
    
    # 按部门分析
    dept_stats = {}
    for emp in employees:
        dept = emp['部门']
        salary = int(emp['薪资'])
        
        if dept not in dept_stats:
            dept_stats[dept] = {'count': 0, 'total_salary': 0, 'salaries': []}
        
        dept_stats[dept]['count'] += 1
        dept_stats[dept]['total_salary'] += salary
        dept_stats[dept]['salaries'].append(salary)
    
    # 计算部门统计信息
    for dept, stats in dept_stats.items():
        avg_salary = stats['total_salary'] / stats['count']
        analysis_result['department_analysis'][dept] = {
            'employee_count': stats['count'],
            'average_salary': round(avg_salary, 0),
            'total_salary': stats['total_salary']
        }
    
    # 按职位分析薪资范围
    position_stats = {}
    for emp in employees:
        position = emp['职位']
        salary = int(emp['薪资'])
        
        if position not in position_stats:
            position_stats[position] = []
        position_stats[position].append(salary)
    
    for position, salaries in position_stats.items():
        analysis_result['position_analysis'][position] = {
            'min_salary': min(salaries),
            'max_salary': max(salaries),
            'avg_salary': round(sum(salaries) / len(salaries), 0),
            'employee_count': len(salaries)
        }
    
    # 按入职年份分析
    year_stats = {}
    for emp in employees:
        hire_date = emp['入职日期']
        year = hire_date.split('-')[0]
        year_stats[year] = year_stats.get(year, 0) + 1
    
    analysis_result['hiring_year_analysis'] = year_stats
    
    # 保存分析结果
    with open(output_filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(analysis_result, jsonfile, ensure_ascii=False, indent=2)
    
    print(f"✓ 数据分析完成，结果保存到：{output_filename}")
    print(f"✓ 部门数量：{len(analysis_result['department_analysis'])}")
    print(f"✓ 职位类型：{len(analysis_result['position_analysis'])}")
    
    return analysis_result


def exercise4_create_product_json():
    """
    练习4解答：创建产品JSON文件
    """
    filename = 'products.json'
    
    # 创建产品数据结构
    products_data = {
        'store_info': {
            'name': 'Python学习商店',
            'created_at': datetime.now().isoformat(),
            'version': '1.0'
        },
        'categories': {
            '编程书籍': {
                'id': 1,
                'description': '各种编程语言学习书籍',
                'products': [
                    {
                        'id': 'B001',
                        'name': 'Python编程从入门到实践',
                        'price': 89.0,
                        'stock': 50,
                        'description': '适合初学者的Python教程',
                        'tags': ['Python', '入门', '实践']
                    },
                    {
                        'id': 'B002',
                        'name': 'JavaScript高级程序设计',
                        'price': 99.0,
                        'stock': 30,
                        'description': 'JavaScript权威指南',
                        'tags': ['JavaScript', '高级', '前端']
                    },
                    {
                        'id': 'B003',
                        'name': 'Java核心技术',
                        'price': 108.0,
                        'stock': 25,
                        'description': 'Java开发必备参考书',
                        'tags': ['Java', '核心', '技术']
                    },
                    {
                        'id': 'B004',
                        'name': 'C++程序设计',
                        'price': 95.0,
                        'stock': 20,
                        'description': 'C++编程经典教材',
                        'tags': ['C++', '程序设计', '经典']
                    },
                    {
                        'id': 'B005',
                        'name': 'Go语言实战',
                        'price': 85.0,
                        'stock': 35,
                        'description': 'Go语言实际应用指南',
                        'tags': ['Go', '实战', '应用']
                    }
                ]
            },
            '在线课程': {
                'id': 2,
                'description': '视频教程和在线培训课程',
                'products': [
                    {
                        'id': 'C001',
                        'name': 'Python Web开发课程',
                        'price': 299.0,
                        'stock': 100,
                        'description': '从零开始学习Python Web开发',
                        'tags': ['Python', 'Web', '开发', '视频']
                    },
                    {
                        'id': 'C002',
                        'name': '数据分析实战课程',
                        'price': 399.0,
                        'stock': 80,
                        'description': '使用Python进行数据分析',
                        'tags': ['数据分析', 'Python', '实战']
                    },
                    {
                        'id': 'C003',
                        'name': '机器学习入门',
                        'price': 499.0,
                        'stock': 60,
                        'description': '机器学习基础理论与实践',
                        'tags': ['机器学习', 'AI', '入门']
                    },
                    {
                        'id': 'C004',
                        'name': '前端开发全栈课程',
                        'price': 599.0,
                        'stock': 40,
                        'description': 'HTML/CSS/JavaScript全栈开发',
                        'tags': ['前端', '全栈', 'HTML', 'CSS', 'JavaScript']
                    },
                    {
                        'id': 'C005',
                        'name': 'Docker容器技术',
                        'price': 299.0,
                        'stock': 70,
                        'description': 'Docker容器化部署实战',
                        'tags': ['Docker', '容器', '部署']
                    }
                ]
            },
            '开发工具': {
                'id': 3,
                'description': '编程开发相关的软件和工具',
                'products': [
                    {
                        'id': 'T001',
                        'name': 'PyCharm专业版',
                        'price': 199.0,
                        'stock': 200,
                        'description': 'Python集成开发环境',
                        'tags': ['PyCharm', 'IDE', 'Python']
                    },
                    {
                        'id': 'T002',
                        'name': 'VS Code插件包',
                        'price': 49.0,
                        'stock': 150,
                        'description': '实用的VS Code扩展插件集合',
                        'tags': ['VS Code', '插件', '扩展']
                    },
                    {
                        'id': 'T003',
                        'name': 'Git版本控制工具',
                        'price': 0.0,
                        'stock': 999,
                        'description': '免费的版本控制系统',
                        'tags': ['Git', '版本控制', '免费']
                    },
                    {
                        'id': 'T004',
                        'name': 'Postman API测试工具',
                        'price': 99.0,
                        'stock': 80,
                        'description': 'API开发和测试工具',
                        'tags': ['Postman', 'API', '测试']
                    },
                    {
                        'id': 'T005',
                        'name': 'Sublime Text编辑器',
                        'price': 80.0,
                        'stock': 120,
                        'description': '轻量级代码编辑器',
                        'tags': ['Sublime', '编辑器', '轻量级']
                    }
                ]
            }
        }
    }
    
    # 计算总产品数
    total_products = 0
    for category in products_data['categories'].values():
        total_products += len(category['products'])
    
    products_data['statistics'] = {
        'total_products': total_products,
        'total_categories': len(products_data['categories']),
        'last_updated': datetime.now().isoformat()
    }
    
    # 保存到JSON文件
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(products_data, jsonfile, ensure_ascii=False, indent=2)
    
    print(f"✓ 创建产品JSON文件：{filename}")
    print(f"✓ 总产品数：{total_products}")
    print(f"✓ 类别数：{len(products_data['categories'])}")
    
    return total_products


def exercise5_json_data_manipulation():
    """
    练习5解答：JSON数据操作
    """
    filename = 'products.json'
    
    if not os.path.exists(filename):
        print(f"❌ 文件 {filename} 不存在，请先运行练习4")
        return None
    
    # 读取JSON数据
    with open(filename, 'r', encoding='utf-8') as jsonfile:
        products_data = json.load(jsonfile)
    
    # 操作统计
    stats = {'added': 0, 'updated': 0, 'deleted': 0}
    
    # 1. 添加新产品
    new_products = [
        {
            'id': 'B006',
            'name': 'Rust编程语言',
            'price': 92.0,
            'stock': 15,
            'description': '系统编程语言Rust入门',
            'tags': ['Rust', '系统编程', '安全']
        },
        {
            'id': 'C006',
            'name': '区块链开发课程',
            'price': 699.0,
            'stock': 30,
            'description': '区块链技术与智能合约开发',
            'tags': ['区块链', '智能合约', '开发']
        },
        {
            'id': 'T006',
            'name': 'IntelliJ IDEA',
            'price': 299.0,
            'stock': 90,
            'description': 'Java集成开发环境',
            'tags': ['IntelliJ', 'IDE', 'Java']
        }
    ]
    
    # 添加新产品到相应类别
    products_data['categories']['编程书籍']['products'].append(new_products[0])
    products_data['categories']['在线课程']['products'].append(new_products[1])
    products_data['categories']['开发工具']['products'].append(new_products[2])
    stats['added'] = len(new_products)
    
    # 2. 更新产品价格（涨价10%）
    for category in products_data['categories'].values():
        for product in category['products']:
            if product['price'] > 0:  # 跳过免费产品
                old_price = product['price']
                product['price'] = round(old_price * 1.1, 2)
                stats['updated'] += 1
    
    # 3. 删除库存为0的产品
    for category in products_data['categories'].values():
        original_count = len(category['products'])
        category['products'] = [p for p in category['products'] if p['stock'] > 0]
        stats['deleted'] += original_count - len(category['products'])
    
    # 4. 为所有产品添加last_updated字段
    current_time = datetime.now().isoformat()
    for category in products_data['categories'].values():
        for product in category['products']:
            product['last_updated'] = current_time
    
    # 更新统计信息
    total_products = sum(len(cat['products']) for cat in products_data['categories'].values())
    products_data['statistics']['total_products'] = total_products
    products_data['statistics']['last_updated'] = current_time
    
    # 保存修改后的数据
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(products_data, jsonfile, ensure_ascii=False, indent=2)
    
    print(f"✓ JSON数据操作完成")
    print(f"✓ 添加产品：{stats['added']} 个")
    print(f"✓ 更新产品：{stats['updated']} 个")
    print(f"✓ 删除产品：{stats['deleted']} 个")
    
    return stats


def exercise6_csv_to_json_conversion():
    """
    练习6解答：CSV到JSON格式转换
    """
    input_filename = 'employees.csv'
    output_filename = 'employees_by_department.json'
    
    if not os.path.exists(input_filename):
        print(f"❌ 文件 {input_filename} 不存在，请先运行练习1")
        return None
    
    employees = []
    
    # 读取CSV数据
    with open(input_filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            employees.append(row)
    
    # 按部门分组
    departments = {}
    for emp in employees:
        dept_name = emp['部门']
        if dept_name not in departments:
            departments[dept_name] = {
                'department_name': dept_name,
                'employees': [],
                'statistics': {
                    'employee_count': 0,
                    'total_salary': 0,
                    'average_salary': 0,
                    'min_salary': float('inf'),
                    'max_salary': 0
                }
            }
        
        # 添加员工信息
        employee_info = {
            'employee_id': emp['员工ID'],
            'name': emp['姓名'],
            'position': emp['职位'],
            'salary': int(emp['薪资']),
            'hire_date': emp['入职日期']
        }
        
        departments[dept_name]['employees'].append(employee_info)
    
    # 计算部门统计信息
    for dept_name, dept_data in departments.items():
        employees_list = dept_data['employees']
        salaries = [emp['salary'] for emp in employees_list]
        
        dept_data['statistics']['employee_count'] = len(employees_list)
        dept_data['statistics']['total_salary'] = sum(salaries)
        dept_data['statistics']['average_salary'] = round(sum(salaries) / len(salaries), 0)
        dept_data['statistics']['min_salary'] = min(salaries)
        dept_data['statistics']['max_salary'] = max(salaries)
    
    # 组织最终数据结构
    result_data = {
        'conversion_info': {
            'source_file': input_filename,
            'conversion_date': datetime.now().isoformat(),
            'total_employees': len(employees),
            'total_departments': len(departments)
        },
        'departments': departments
    }
    
    # 保存为JSON文件
    with open(output_filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(result_data, jsonfile, ensure_ascii=False, indent=2)
    
    print(f"✓ CSV转JSON完成，结果保存到：{output_filename}")
    print(f"✓ 转换部门数：{len(departments)}")
    print(f"✓ 总员工数：{len(employees)}")
    
    return len(departments)


def exercise7_data_validation():
    """
    练习7解答：数据验证和清洗
    """
    dirty_filename = 'dirty_data.csv'
    clean_filename = 'clean_data.csv'
    report_filename = 'data_quality_report.json'
    
    # 1. 创建包含错误数据的CSV文件
    dirty_data = [
        ['员工ID', '姓名', '部门', '职位', '薪资', '入职日期'],
        ['E001', '张三', '技术部', '软件工程师', '12000', '2022-03-15'],
        ['E002', '', '销售部', '销售经理', '15000', '2021-08-20'],  # 缺失姓名
        ['E003', '王五', '', 'HR专员', '8000', '2023-01-10'],  # 缺失部门
        ['E004', '赵六', '技术部', '前端开发', '-5000', '2022-11-05'],  # 负数薪资
        ['E005', '钱七', '财务部', '会计师', '9000', '2021-13-01'],  # 错误日期
        ['E006', '孙八', '技术部', '架构师', '18000', '2020-06-15'],
        ['E007', '周九', '市场部', '市场专员', 'abc', '2023-04-20'],  # 非数字薪资
        ['E008', '吴十', '销售部', '销售代表', '6500', ''],  # 缺失日期
        ['E009', '郑十一', '技术部', '测试工程师', '9500', '2022-09-10'],
        ['', '王十二', '财务部', '财务经理', '14000', '2021-05-18'],  # 缺失ID
    ]
    
    # 写入脏数据文件
    with open(dirty_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(dirty_data)
    
    print(f"✓ 创建脏数据文件：{dirty_filename}")
    
    # 2. 读取并验证数据
    clean_records = []
    validation_errors = []
    
    with open(dirty_filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row_num, row in enumerate(reader, start=2):  # 从第2行开始（跳过标题）
            errors = []
            
            # 验证员工ID
            if not row['员工ID'].strip():
                errors.append('员工ID为空')
            
            # 验证姓名
            if not row['姓名'].strip():
                errors.append('姓名为空')
                row['姓名'] = f'员工{row_num}'  # 填充默认值
            
            # 验证部门
            if not row['部门'].strip():
                errors.append('部门为空')
                row['部门'] = '未分配部门'  # 填充默认值
            
            # 验证薪资
            try:
                salary = int(row['薪资'])
                if salary < 0:
                    errors.append('薪资为负数')
                    row['薪资'] = '0'  # 修正为0
                elif salary > 100000:
                    errors.append('薪资过高，可能有误')
            except ValueError:
                errors.append('薪资格式错误')
                row['薪资'] = '0'  # 修正为0
            
            # 验证日期
            if row['入职日期'].strip():
                try:
                    datetime.strptime(row['入职日期'], '%Y-%m-%d')
                except ValueError:
                    errors.append('日期格式错误')
                    row['入职日期'] = '2023-01-01'  # 填充默认日期
            else:
                errors.append('入职日期为空')
                row['入职日期'] = '2023-01-01'  # 填充默认日期
            
            # 记录错误
            if errors:
                validation_errors.append({
                    'row_number': row_num,
                    'employee_id': row['员工ID'],
                    'errors': errors
                })
            
            # 如果员工ID不为空，则保留记录（即使有其他错误也尝试修复）
            if row['员工ID'].strip():
                clean_records.append(row)
    
    # 3. 保存清洗后的数据
    if clean_records:
        with open(clean_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['员工ID', '姓名', '部门', '职位', '薪资', '入职日期']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(clean_records)
    
    # 4. 生成数据质量报告
    quality_report = {
        'validation_date': datetime.now().isoformat(),
        'source_file': dirty_filename,
        'clean_file': clean_filename,
        'summary': {
            'original_records': len(dirty_data) - 1,  # 减去标题行
            'clean_records': len(clean_records),
            'removed_records': (len(dirty_data) - 1) - len(clean_records),
            'total_errors': len(validation_errors),
            'error_rate': round(len(validation_errors) / (len(dirty_data) - 1) * 100, 1)
        },
        'validation_errors': validation_errors,
        'data_quality_issues': {
            'missing_employee_id': sum(1 for e in validation_errors if any('员工ID' in err for err in e['errors'])),
            'missing_name': sum(1 for e in validation_errors if any('姓名' in err for err in e['errors'])),
            'missing_department': sum(1 for e in validation_errors if any('部门' in err for err in e['errors'])),
            'invalid_salary': sum(1 for e in validation_errors if any('薪资' in err for err in e['errors'])),
            'invalid_date': sum(1 for e in validation_errors if any('日期' in err for err in e['errors']))
        }
    }
    
    # 保存质量报告
    with open(report_filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(quality_report, jsonfile, ensure_ascii=False, indent=2)
    
    print(f"✓ 数据清洗完成")
    print(f"✓ 原始记录：{quality_report['summary']['original_records']} 条")
    print(f"✓ 清洗后记录：{quality_report['summary']['clean_records']} 条")
    print(f"✓ 错误率：{quality_report['summary']['error_rate']}%")
    print(f"✓ 质量报告保存到：{report_filename}")
    
    return (quality_report['summary']['original_records'], quality_report['summary']['clean_records'])


def exercise8_batch_file_processing():
    """
    练习8解答：批量文件处理
    """
    # 1. 创建多个月份的销售数据文件
    months = ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06']
    products = ['笔记本电脑', '鼠标', '键盘', '显示器', '耳机', '音响']
    customers = ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十']
    
    created_files = []
    total_records = 0
    
    for month in months:
        filename = f'sales_{month}.csv'
        
        # 生成该月的销售数据
        sales_data = []
        for _ in range(random.randint(50, 100)):  # 每月50-100条记录
            record = {
                '订单ID': f'ORD{month.replace("-", "")}{random.randint(1000, 9999)}',
                '日期': f'{month}-{random.randint(1, 28):02d}',
                '客户': random.choice(customers),
                '产品': random.choice(products),
                '数量': random.randint(1, 5),
                '单价': random.randint(100, 2000),
                '总金额': 0  # 将在下面计算
            }
            record['总金额'] = record['数量'] * record['单价']
            sales_data.append(record)
        
        # 写入CSV文件
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['订单ID', '日期', '客户', '产品', '数量', '单价', '总金额']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sales_data)
        
        created_files.append(filename)
        total_records += len(sales_data)
        print(f"✓ 创建销售数据文件：{filename}（{len(sales_data)}条记录）")
    
    # 2. 批量读取所有CSV文件
    all_sales_data = []
    
    for filename in glob.glob('sales_*.csv'):
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # 转换数据类型
                row['数量'] = int(row['数量'])
                row['单价'] = int(row['单价'])
                row['总金额'] = int(row['总金额'])
                all_sales_data.append(row)
    
    # 3. 数据分析
    analysis_result = {
        'analysis_date': datetime.now().isoformat(),
        'data_period': f'{months[0]} 到 {months[-1]}',
        'total_records': len(all_sales_data),
        'total_revenue': sum(record['总金额'] for record in all_sales_data),
        'monthly_trends': {},
        'top_products': {},
        'customer_analysis': {}
    }
    
    # 月度趋势分析
    monthly_sales = {}
    for record in all_sales_data:
        month = record['日期'][:7]  # 提取年-月
        if month not in monthly_sales:
            monthly_sales[month] = {'revenue': 0, 'orders': 0}
        monthly_sales[month]['revenue'] += record['总金额']
        monthly_sales[month]['orders'] += 1
    
    analysis_result['monthly_trends'] = monthly_sales
    
    # 产品销售分析
    product_sales = {}
    for record in all_sales_data:
        product = record['产品']
        if product not in product_sales:
            product_sales[product] = {'quantity': 0, 'revenue': 0, 'orders': 0}
        product_sales[product]['quantity'] += record['数量']
        product_sales[product]['revenue'] += record['总金额']
        product_sales[product]['orders'] += 1
    
    # 按销售额排序获取热销产品
    top_products = sorted(product_sales.items(), key=lambda x: x[1]['revenue'], reverse=True)
    analysis_result['top_products'] = dict(top_products)
    
    # 客户分析
    customer_stats = {}
    for record in all_sales_data:
        customer = record['客户']
        if customer not in customer_stats:
            customer_stats[customer] = {'total_spent': 0, 'order_count': 0, 'avg_order_value': 0}
        customer_stats[customer]['total_spent'] += record['总金额']
        customer_stats[customer]['order_count'] += 1
    
    # 计算平均订单价值
    for customer, stats in customer_stats.items():
        stats['avg_order_value'] = round(stats['total_spent'] / stats['order_count'], 2)
    
    analysis_result['customer_analysis'] = customer_stats
    
    # 4. 保存综合报告（JSON格式）
    json_report_file = 'sales_comprehensive_report.json'
    with open(json_report_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(analysis_result, jsonfile, ensure_ascii=False, indent=2)
    
    # 5. 保存综合报告（CSV格式）
    csv_report_file = 'sales_summary_report.csv'
    with open(csv_report_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # 写入总体统计
        writer.writerow(['销售综合报告'])
        writer.writerow(['分析日期', analysis_result['analysis_date']])
        writer.writerow(['数据期间', analysis_result['data_period']])
        writer.writerow(['总记录数', analysis_result['total_records']])
        writer.writerow(['总销售额', analysis_result['total_revenue']])
        writer.writerow([])
        
        # 写入月度趋势
        writer.writerow(['月度销售趋势'])
        writer.writerow(['月份', '销售额', '订单数'])
        for month, data in monthly_sales.items():
            writer.writerow([month, data['revenue'], data['orders']])
        writer.writerow([])
        
        # 写入产品销售排行
        writer.writerow(['产品销售排行'])
        writer.writerow(['产品', '销售额', '销售数量', '订单数'])
        for product, data in top_products[:5]:  # 前5名
            writer.writerow([product, data['revenue'], data['quantity'], data['orders']])
    
    print(f"\n✓ 批量文件处理完成")
    print(f"✓ 处理文件数：{len(created_files)}")
    print(f"✓ 总记录数：{total_records}")
    print(f"✓ 总销售额：{analysis_result['total_revenue']:,} 元")
    print(f"✓ JSON报告：{json_report_file}")
    print(f"✓ CSV报告：{csv_report_file}")
    
    return (len(created_files), total_records)


def exercise9_json_schema_validation():
    """
    练习9解答：JSON数据结构验证
    """
    # 1. 定义产品数据的JSON模式
    product_schema = {
        'required_fields': ['id', 'name', 'price', 'stock'],
        'optional_fields': ['description', 'tags', 'last_updated'],
        'field_types': {
            'id': str,
            'name': str,
            'price': (int, float),
            'stock': int,
            'description': str,
            'tags': list,
            'last_updated': str
        },
        'validation_rules': {
            'price': lambda x: x >= 0,
            'stock': lambda x: x >= 0,
            'name': lambda x: len(x.strip()) > 0
        }
    }
    
    def validate_product(product, schema):
        """验证单个产品数据"""
        errors = []
        
        # 检查必需字段
        for field in schema['required_fields']:
            if field not in product:
                errors.append(f'缺少必需字段: {field}')
        
        # 检查字段类型
        for field, expected_type in schema['field_types'].items():
            if field in product:
                if not isinstance(product[field], expected_type):
                    errors.append(f'字段 {field} 类型错误，期望 {expected_type.__name__}，实际 {type(product[field]).__name__}')
        
        # 检查验证规则
        for field, rule in schema['validation_rules'].items():
            if field in product:
                try:
                    if not rule(product[field]):
                        errors.append(f'字段 {field} 验证失败')
                except Exception as e:
                    errors.append(f'字段 {field} 验证时出错: {str(e)}')
        
        return errors
    
    # 2. 创建测试数据
    test_products = [
        # 正确的产品数据
        {
            'id': 'P001',
            'name': '测试产品1',
            'price': 99.99,
            'stock': 10,
            'description': '这是一个测试产品',
            'tags': ['测试', '产品']
        },
        # 缺少必需字段
        {
            'name': '测试产品2',
            'price': 199.99,
            'stock': 5
        },
        # 类型错误
        {
            'id': 'P003',
            'name': '测试产品3',
            'price': '免费',  # 应该是数字
            'stock': 15
        },
        # 验证规则失败
        {
            'id': 'P004',
            'name': '',  # 名称为空
            'price': -50,  # 负价格
            'stock': -5  # 负库存
        }
    ]
    
    # 3. 验证测试数据
    validation_results = []
    for i, product in enumerate(test_products):
        errors = validate_product(product, product_schema)
        validation_results.append({
            'product_index': i,
            'product_id': product.get('id', 'N/A'),
            'is_valid': len(errors) == 0,
            'errors': errors
        })
    
    # 4. 验证现有的products.json文件
    products_file = 'products.json'
    file_validation_result = None
    
    if os.path.exists(products_file):
        try:
            with open(products_file, 'r', encoding='utf-8') as jsonfile:
                products_data = json.load(jsonfile)
            
            file_errors = []
            valid_products = 0
            total_products = 0
            
            # 验证每个类别中的产品
            for category_name, category_data in products_data.get('categories', {}).items():
                for product in category_data.get('products', []):
                    total_products += 1
                    errors = validate_product(product, product_schema)
                    if errors:
                        file_errors.append({
                            'category': category_name,
                            'product_id': product.get('id', 'N/A'),
                            'errors': errors
                        })
                    else:
                        valid_products += 1
            
            file_validation_result = {
                'file_name': products_file,
                'total_products': total_products,
                'valid_products': valid_products,
                'invalid_products': total_products - valid_products,
                'validation_rate': round(valid_products / total_products * 100, 1) if total_products > 0 else 0,
                'errors': file_errors
            }
            
        except Exception as e:
            file_validation_result = {
                'file_name': products_file,
                'error': f'读取文件时出错: {str(e)}'
            }
    
    # 5. 生成验证报告
    validation_report = {
        'validation_date': datetime.now().isoformat(),
        'schema_definition': product_schema,
        'test_data_validation': {
            'total_test_products': len(test_products),
            'valid_test_products': sum(1 for r in validation_results if r['is_valid']),
            'results': validation_results
        },
        'file_validation': file_validation_result
    }
    
    # 保存验证报告
    report_file = 'json_validation_report.json'
    with open(report_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(validation_report, jsonfile, ensure_ascii=False, indent=2)
    
    print(f"✓ JSON模式验证完成")
    print(f"✓ 测试数据验证：{validation_report['test_data_validation']['valid_test_products']}/{validation_report['test_data_validation']['total_test_products']} 通过")
    
    if file_validation_result and 'error' not in file_validation_result:
        print(f"✓ 文件验证：{file_validation_result['valid_products']}/{file_validation_result['total_products']} 通过（{file_validation_result['validation_rate']}%）")
    
    print(f"✓ 验证报告保存到：{report_file}")
    
    return validation_report


def exercise10_performance_comparison():
    """
    练习10解答：性能对比测试
    """
    # 1. 生成大量测试数据
    test_data_size = 1000
    test_data = []
    
    for i in range(test_data_size):
        record = {
            'id': f'ID{i:04d}',
            'name': f'产品{i}',
            'category': random.choice(['电子产品', '服装', '食品', '图书', '家具']),
            'price': round(random.uniform(10, 1000), 2),
            'stock': random.randint(0, 100),
            'description': f'这是产品{i}的详细描述，包含一些随机文本内容。',
            'tags': [f'标签{j}' for j in range(random.randint(1, 5))],
            'created_at': (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat()
        }
        test_data.append(record)
    
    print(f"✓ 生成 {test_data_size} 条测试数据")
    
    # 2. 性能测试函数
    def time_operation(operation_func, *args, **kwargs):
        """测量操作执行时间"""
        start_time = time.time()
        result = operation_func(*args, **kwargs)
        end_time = time.time()
        return end_time - start_time, result
    
    # 3. CSV写入性能测试
    def write_csv_data(data, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            if data:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
    
    # 4. JSON写入性能测试
    def write_json_data(data, filename):
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=2)
    
    # 5. CSV读取性能测试
    def read_csv_data(filename):
        data = []
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
        return data
    
    # 6. JSON读取性能测试
    def read_json_data(filename):
        with open(filename, 'r', encoding='utf-8') as jsonfile:
            return json.load(jsonfile)
    
    # 执行性能测试
    performance_results = {
        'test_date': datetime.now().isoformat(),
        'data_size': test_data_size,
        'results': {}
    }
    
    # CSV写入测试
    csv_filename = 'performance_test.csv'
    csv_write_time, _ = time_operation(write_csv_data, test_data, csv_filename)
    csv_file_size = os.path.getsize(csv_filename)
    
    # JSON写入测试
    json_filename = 'performance_test.json'
    json_write_time, _ = time_operation(write_json_data, test_data, json_filename)
    json_file_size = os.path.getsize(json_filename)
    
    # CSV读取测试
    csv_read_time, csv_data = time_operation(read_csv_data, csv_filename)
    
    # JSON读取测试
    json_read_time, json_data = time_operation(read_json_data, json_filename)
    
    # 整理测试结果
    performance_results['results'] = {
        'csv_performance': {
            'write_time': round(csv_write_time, 4),
            'read_time': round(csv_read_time, 4),
            'file_size': csv_file_size,
            'records_read': len(csv_data)
        },
        'json_performance': {
            'write_time': round(json_write_time, 4),
            'read_time': round(json_read_time, 4),
            'file_size': json_file_size,
            'records_read': len(json_data)
        },
        'comparison': {
            'write_speed_ratio': round(csv_write_time / json_write_time, 2),
            'read_speed_ratio': round(csv_read_time / json_read_time, 2),
            'size_ratio': round(csv_file_size / json_file_size, 2)
        }
    }
    
    # 保存性能测试报告
    report_filename = 'performance_test_report.json'
    with open(report_filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(performance_results, jsonfile, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 性能测试完成")
    print(f"✓ CSV写入时间：{csv_write_time:.4f}秒")
    print(f"✓ JSON写入时间：{json_write_time:.4f}秒")
    print(f"✓ CSV读取时间：{csv_read_time:.4f}秒")
    print(f"✓ JSON读取时间：{json_read_time:.4f}秒")
    print(f"✓ CSV文件大小：{csv_file_size:,}字节")
    print(f"✓ JSON文件大小：{json_file_size:,}字节")
    print(f"✓ 性能报告保存到：{report_filename}")
    
    # 清理测试文件
    os.remove(csv_filename)
    os.remove(json_filename)
    
    return performance_results


def cleanup_exercise_files():
    """
    清理练习生成的文件
    """
    files_to_clean = [
        'employees.csv',
        'high_salary_employees.csv',
        'employee_analysis.json',
        'products.json',
        'employees_by_department.json',
        'dirty_data.csv',
        'clean_data.csv',
        'data_quality_report.json',
        'sales_comprehensive_report.json',
        'sales_summary_report.csv',
        'json_validation_report.json',
        'performance_test_report.json'
    ]
    
    # 清理批量文件
    batch_files = glob.glob('sales_*.csv')
    files_to_clean.extend(batch_files)
    
    cleaned_count = 0
    for filename in files_to_clean:
        if os.path.exists(filename):
            os.remove(filename)
            cleaned_count += 1
            print(f"✓ 删除文件: {filename}")
    
    print(f"\n总共清理了 {cleaned_count} 个文件")


def run_all_exercises():
    """
    运行所有练习解答
    """
    print("Session07 练习2解答：CSV和JSON文件操作")
    print("=" * 50)
    
    exercises = [
        ("练习1：创建员工CSV文件", exercise1_create_employee_csv),
        ("练习2：读取和筛选CSV数据", exercise2_read_and_filter_csv),
        ("练习3：CSV数据分析", exercise3_csv_data_analysis),
        ("练习4：创建产品JSON文件", exercise4_create_product_json),
        ("练习5：JSON数据操作", exercise5_json_data_manipulation),
        ("练习6：CSV到JSON格式转换", exercise6_csv_to_json_conversion),
        ("练习7：数据验证和清洗", exercise7_data_validation),
        ("练习8：批量文件处理", exercise8_batch_file_processing),
        ("练习9：JSON数据结构验证", exercise9_json_schema_validation),
        ("练习10：性能对比测试", exercise10_performance_comparison)
    ]
    
    for title, exercise_func in exercises:
        print(f"\n{title}")
        print("-" * 30)
        
        try:
            result = exercise_func()
            if result is not None:
                print(f"结果: {result}")
            print("✅ 练习完成")
        except Exception as e:
            print(f"❌ 练习出错: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("✅ 所有练习解答运行完成！")
    print("\n💡 解答要点总结：")
    print("- CSV适合表格数据，JSON适合结构化数据")
    print("- 使用csv.DictReader/DictWriter处理CSV更方便")
    print("- JSON数据操作要注意数据类型和结构")
    print("- 数据验证和清洗是重要的数据处理步骤")
    print("- 性能测试有助于选择合适的数据格式")
    print("- 批量处理时要考虑内存使用和错误处理")
    
    # 询问是否清理文件
    response = input("\n是否清理练习生成的文件？(y/n): ").lower().strip()
    if response == 'y':
        cleanup_exercise_files()
    else:
        print("练习文件已保留，你可以继续分析和学习。")


if __name__ == "__main__":
    run_all_exercises()