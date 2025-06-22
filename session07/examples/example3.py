#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session07 示例3：CSV文件处理

本示例演示了Python中CSV文件的处理，包括：
- 使用csv模块读写CSV文件
- 处理带标题的CSV文件
- 数据的筛选和统计
- 处理不同分隔符的CSV文件
- CSV文件的数据验证和清洗

作者: Python教程团队
创建日期: 2024-12-22
"""

import csv
import random
from pathlib import Path
from datetime import datetime, timedelta


def create_sample_csv():
    """
    创建示例CSV文件
    """
    print("=== 创建示例CSV文件 ===")
    
    # 学生成绩数据
    students_data = [
        ['姓名', '年龄', '性别', '班级', '数学', '语文', '英语', '入学日期'],
        ['张三', '18', '男', '高三1班', '85', '92', '78', '2021-09-01'],
        ['李四', '17', '女', '高三1班', '92', '88', '95', '2021-09-01'],
        ['王五', '18', '男', '高三2班', '78', '85', '82', '2021-09-01'],
        ['赵六', '17', '女', '高三2班', '88', '90', '87', '2021-09-01'],
        ['钱七', '18', '男', '高三1班', '95', '87', '92', '2021-09-01'],
        ['孙八', '17', '女', '高三3班', '82', '94', '89', '2021-09-01'],
        ['周九', '18', '男', '高三3班', '89', '86', '91', '2021-09-01'],
        ['吴十', '17', '女', '高三2班', '91', '89', '88', '2021-09-01']
    ]
    
    # 写入CSV文件
    csv_file = 'students.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(students_data)
    
    print(f"✓ 创建学生成绩CSV文件: {csv_file}")
    print(f"✓ 包含 {len(students_data)-1} 条学生记录")
    
    return csv_file


def read_csv_basic(filename):
    """
    基本CSV文件读取
    """
    print(f"\n=== 基本CSV读取: {filename} ===")
    
    try:
        # 方法1: 使用csv.reader
        print("方法1: 使用csv.reader")
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row_num, row in enumerate(reader, 1):
                print(f"第{row_num}行: {row}")
        
        print("\n方法2: 使用csv.DictReader（推荐）")
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            print(f"字段名: {reader.fieldnames}")
            print()
            for row_num, row in enumerate(reader, 1):
                print(f"学生{row_num}: {row['姓名']}, 年龄: {row['年龄']}, 班级: {row['班级']}")
                
    except FileNotFoundError:
        print(f"❌ 文件 {filename} 不存在")
    except Exception as e:
        print(f"❌ 读取CSV文件时发生错误: {e}")


def analyze_student_data(filename):
    """
    分析学生数据
    """
    print(f"\n=== 学生数据分析: {filename} ===")
    
    try:
        students = []
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # 转换数值字段
                student = {
                    '姓名': row['姓名'],
                    '年龄': int(row['年龄']),
                    '性别': row['性别'],
                    '班级': row['班级'],
                    '数学': int(row['数学']),
                    '语文': int(row['语文']),
                    '英语': int(row['英语']),
                    '入学日期': row['入学日期']
                }
                # 计算总分和平均分
                student['总分'] = student['数学'] + student['语文'] + student['英语']
                student['平均分'] = round(student['总分'] / 3, 1)
                students.append(student)
        
        # 基本统计
        total_students = len(students)
        male_count = sum(1 for s in students if s['性别'] == '男')
        female_count = total_students - male_count
        
        print(f"学生总数: {total_students}")
        print(f"男生: {male_count}人, 女生: {female_count}人")
        
        # 年龄统计
        ages = [s['年龄'] for s in students]
        avg_age = sum(ages) / len(ages)
        print(f"平均年龄: {avg_age:.1f}岁")
        
        # 成绩统计
        subjects = ['数学', '语文', '英语']
        print("\n各科平均分:")
        for subject in subjects:
            scores = [s[subject] for s in students]
            avg_score = sum(scores) / len(scores)
            max_score = max(scores)
            min_score = min(scores)
            print(f"  {subject}: 平均{avg_score:.1f}, 最高{max_score}, 最低{min_score}")
        
        # 总分排名
        students_sorted = sorted(students, key=lambda x: x['总分'], reverse=True)
        print("\n总分排名前3名:")
        for i, student in enumerate(students_sorted[:3], 1):
            print(f"  第{i}名: {student['姓名']} - 总分{student['总分']}, 平均分{student['平均分']}")
        
        # 班级统计
        class_stats = {}
        for student in students:
            class_name = student['班级']
            if class_name not in class_stats:
                class_stats[class_name] = []
            class_stats[class_name].append(student['总分'])
        
        print("\n班级平均分:")
        for class_name, scores in class_stats.items():
            avg_score = sum(scores) / len(scores)
            print(f"  {class_name}: {avg_score:.1f}分 ({len(scores)}人)")
        
        return students
        
    except Exception as e:
        print(f"❌ 分析数据时发生错误: {e}")
        return []


def filter_and_export_data(students, output_file):
    """
    筛选数据并导出
    """
    print(f"\n=== 数据筛选和导出: {output_file} ===")
    
    if not students:
        print("❌ 没有学生数据")
        return
    
    # 筛选条件：总分大于250分的学生
    high_achievers = [s for s in students if s['总分'] > 250]
    
    print(f"总分超过250分的学生: {len(high_achievers)}人")
    
    # 导出筛选结果
    fieldnames = ['姓名', '班级', '数学', '语文', '英语', '总分', '平均分']
    
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for student in high_achievers:
                # 只写入需要的字段
                filtered_data = {field: student[field] for field in fieldnames}
                writer.writerow(filtered_data)
        
        print(f"✓ 高分学生数据已导出到: {output_file}")
        
        # 显示导出的数据
        print("\n导出的数据:")
        with open(output_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                print(f"  {row['姓名']} ({row['班级']}) - 总分: {row['总分']}")
                
    except Exception as e:
        print(f"❌ 导出数据时发生错误: {e}")


def create_sales_data_csv():
    """
    创建销售数据CSV文件（包含更复杂的数据）
    """
    print("\n=== 创建销售数据CSV ===")
    
    # 生成随机销售数据
    products = ['笔记本电脑', '台式机', '显示器', '键盘', '鼠标', '音响', '摄像头', '耳机']
    regions = ['北京', '上海', '广州', '深圳', '杭州', '南京', '成都', '武汉']
    
    sales_data = []
    sales_data.append(['日期', '产品', '地区', '销售员', '数量', '单价', '总金额'])
    
    # 生成30天的销售数据
    start_date = datetime.now() - timedelta(days=30)
    for i in range(100):  # 100条销售记录
        date = start_date + timedelta(days=random.randint(0, 29))
        product = random.choice(products)
        region = random.choice(regions)
        salesperson = f"销售员{random.randint(1, 20):02d}"
        quantity = random.randint(1, 10)
        
        # 根据产品设置价格范围
        price_ranges = {
            '笔记本电脑': (3000, 8000),
            '台式机': (2000, 6000),
            '显示器': (800, 3000),
            '键盘': (50, 500),
            '鼠标': (30, 300),
            '音响': (100, 1000),
            '摄像头': (200, 800),
            '耳机': (50, 500)
        }
        
        min_price, max_price = price_ranges[product]
        unit_price = random.randint(min_price, max_price)
        total_amount = quantity * unit_price
        
        sales_data.append([
            date.strftime('%Y-%m-%d'),
            product,
            region,
            salesperson,
            str(quantity),
            str(unit_price),
            str(total_amount)
        ])
    
    # 写入CSV文件
    sales_file = 'sales_data.csv'
    with open(sales_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(sales_data)
    
    print(f"✓ 创建销售数据CSV文件: {sales_file}")
    print(f"✓ 包含 {len(sales_data)-1} 条销售记录")
    
    return sales_file


def analyze_sales_data(filename):
    """
    分析销售数据
    """
    print(f"\n=== 销售数据分析: {filename} ===")
    
    try:
        sales_records = []
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                record = {
                    '日期': datetime.strptime(row['日期'], '%Y-%m-%d'),
                    '产品': row['产品'],
                    '地区': row['地区'],
                    '销售员': row['销售员'],
                    '数量': int(row['数量']),
                    '单价': float(row['单价']),
                    '总金额': float(row['总金额'])
                }
                sales_records.append(record)
        
        # 总体统计
        total_records = len(sales_records)
        total_revenue = sum(record['总金额'] for record in sales_records)
        total_quantity = sum(record['数量'] for record in sales_records)
        
        print(f"销售记录总数: {total_records}")
        print(f"总销售额: ¥{total_revenue:,.2f}")
        print(f"总销售数量: {total_quantity}")
        print(f"平均订单金额: ¥{total_revenue/total_records:,.2f}")
        
        # 产品销售统计
        product_stats = {}
        for record in sales_records:
            product = record['产品']
            if product not in product_stats:
                product_stats[product] = {'数量': 0, '金额': 0}
            product_stats[product]['数量'] += record['数量']
            product_stats[product]['金额'] += record['总金额']
        
        print("\n产品销售排行（按金额）:")
        sorted_products = sorted(product_stats.items(), key=lambda x: x[1]['金额'], reverse=True)
        for i, (product, stats) in enumerate(sorted_products[:5], 1):
            print(f"  {i}. {product}: ¥{stats['金额']:,.2f} ({stats['数量']}件)")
        
        # 地区销售统计
        region_stats = {}
        for record in sales_records:
            region = record['地区']
            if region not in region_stats:
                region_stats[region] = 0
            region_stats[region] += record['总金额']
        
        print("\n地区销售排行:")
        sorted_regions = sorted(region_stats.items(), key=lambda x: x[1], reverse=True)
        for i, (region, amount) in enumerate(sorted_regions[:5], 1):
            print(f"  {i}. {region}: ¥{amount:,.2f}")
        
        # 销售员业绩统计
        salesperson_stats = {}
        for record in sales_records:
            salesperson = record['销售员']
            if salesperson not in salesperson_stats:
                salesperson_stats[salesperson] = 0
            salesperson_stats[salesperson] += record['总金额']
        
        print("\n销售员业绩排行（前5名）:")
        sorted_salespeople = sorted(salesperson_stats.items(), key=lambda x: x[1], reverse=True)
        for i, (salesperson, amount) in enumerate(sorted_salespeople[:5], 1):
            print(f"  {i}. {salesperson}: ¥{amount:,.2f}")
        
        return sales_records
        
    except Exception as e:
        print(f"❌ 分析销售数据时发生错误: {e}")
        return []


def handle_different_delimiters():
    """
    处理不同分隔符的CSV文件
    """
    print("\n=== 处理不同分隔符的CSV文件 ===")
    
    # 创建使用分号分隔的CSV文件
    semicolon_data = [
        ['姓名;年龄;城市;职业'],
        ['张三;25;北京;工程师'],
        ['李四;30;上海;设计师'],
        ['王五;28;广州;产品经理']
    ]
    
    semicolon_file = 'semicolon_data.csv'
    with open(semicolon_file, 'w', encoding='utf-8') as f:
        for row in semicolon_data:
            f.write(row[0] + '\n')
    
    print(f"✓ 创建分号分隔的CSV文件: {semicolon_file}")
    
    # 读取分号分隔的文件
    print("\n读取分号分隔的CSV:")
    with open(semicolon_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        for row_num, row in enumerate(reader, 1):
            print(f"第{row_num}行: {row}")
    
    # 创建制表符分隔的文件
    tab_data = [
        ['产品\t价格\t库存\t类别'],
        ['苹果\t5.5\t100\t水果'],
        ['香蕉\t3.2\t80\t水果'],
        ['牛奶\t12.8\t50\t饮品']
    ]
    
    tab_file = 'tab_data.tsv'
    with open(tab_file, 'w', encoding='utf-8') as f:
        for row in tab_data:
            f.write(row[0] + '\n')
    
    print(f"\n✓ 创建制表符分隔的文件: {tab_file}")
    
    # 读取制表符分隔的文件
    print("\n读取制表符分隔的文件:")
    with open(tab_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            print(f"  {row['产品']}: ¥{row['价格']}, 库存{row['库存']}")
    
    return [semicolon_file, tab_file]


def data_validation_and_cleaning():
    """
    数据验证和清洗
    """
    print("\n=== 数据验证和清洗 ===")
    
    # 创建包含错误数据的CSV文件
    dirty_data = [
        ['姓名', '年龄', '邮箱', '电话', '工资'],
        ['张三', '25', 'zhangsan@email.com', '13800138000', '8000'],
        ['李四', 'abc', 'lisi@email', '138001380001', '9000'],  # 年龄错误，邮箱格式错误，电话号码过长
        ['王五', '30', 'wangwu@email.com', '13800138002', 'abc'],  # 工资格式错误
        ['', '28', 'zhaoliu@email.com', '13800138003', '7500'],  # 姓名为空
        ['钱七', '-5', 'qianqi@email.com', '13800138004', '8500'],  # 年龄为负数
    ]
    
    dirty_file = 'dirty_data.csv'
    with open(dirty_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(dirty_data)
    
    print(f"✓ 创建包含错误数据的CSV文件: {dirty_file}")
    
    # 读取并验证数据
    valid_records = []
    error_records = []
    
    with open(dirty_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, 2):  # 从第2行开始（第1行是标题）
            errors = []
            
            # 验证姓名
            if not row['姓名'].strip():
                errors.append('姓名不能为空')
            
            # 验证年龄
            try:
                age = int(row['年龄'])
                if age < 0 or age > 120:
                    errors.append('年龄必须在0-120之间')
            except ValueError:
                errors.append('年龄必须是数字')
            
            # 验证邮箱
            email = row['邮箱']
            if '@' not in email or '.' not in email.split('@')[-1]:
                errors.append('邮箱格式不正确')
            
            # 验证电话
            phone = row['电话']
            if not phone.isdigit() or len(phone) != 11:
                errors.append('电话号码必须是11位数字')
            
            # 验证工资
            try:
                salary = float(row['工资'])
                if salary < 0:
                    errors.append('工资不能为负数')
            except ValueError:
                errors.append('工资必须是数字')
            
            if errors:
                error_records.append({
                    '行号': row_num,
                    '数据': row,
                    '错误': errors
                })
            else:
                valid_records.append(row)
    
    print(f"\n数据验证结果:")
    print(f"有效记录: {len(valid_records)}条")
    print(f"错误记录: {len(error_records)}条")
    
    if error_records:
        print("\n错误详情:")
        for error_record in error_records:
            print(f"  第{error_record['行号']}行: {error_record['数据']['姓名']}")
            for error in error_record['错误']:
                print(f"    - {error}")
    
    # 导出清洗后的数据
    if valid_records:
        clean_file = 'clean_data.csv'
        with open(clean_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['姓名', '年龄', '邮箱', '电话', '工资']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(valid_records)
        
        print(f"\n✓ 清洗后的数据已保存到: {clean_file}")
        return [dirty_file, clean_file]
    
    return [dirty_file]


def cleanup_csv_files():
    """
    清理CSV示例文件
    """
    print("\n=== 清理CSV文件 ===")
    
    csv_files = [
        'students.csv',
        'high_achievers.csv',
        'sales_data.csv',
        'semicolon_data.csv',
        'tab_data.tsv',
        'dirty_data.csv',
        'clean_data.csv'
    ]
    
    for filename in csv_files:
        file_path = Path(filename)
        if file_path.exists():
            file_path.unlink()
            print(f"✓ 删除文件: {filename}")
        else:
            print(f"- 文件不存在: {filename}")


def main():
    """
    主函数
    """
    print("Session07 示例3：CSV文件处理")
    print("=" * 50)
    
    try:
        # 1. 创建和读取基本CSV文件
        students_file = create_sample_csv()
        read_csv_basic(students_file)
        
        # 2. 分析学生数据
        students = analyze_student_data(students_file)
        
        # 3. 筛选和导出数据
        filter_and_export_data(students, 'high_achievers.csv')
        
        # 4. 创建和分析销售数据
        sales_file = create_sales_data_csv()
        analyze_sales_data(sales_file)
        
        # 5. 处理不同分隔符的文件
        delimiter_files = handle_different_delimiters()
        
        # 6. 数据验证和清洗
        validation_files = data_validation_and_cleaning()
        
        print("\n" + "=" * 50)
        print("✅ 示例3演示完成！")
        print("\n💡 重要提示：")
        print("- 使用csv.DictReader处理带标题的CSV文件")
        print("- 注意数据类型转换和验证")
        print("- 处理不同分隔符时指定delimiter参数")
        print("- 实际项目中要做好数据清洗和异常处理")
        
        # 询问是否清理文件
        response = input("\n是否清理CSV示例文件？(y/n): ").lower().strip()
        if response == 'y':
            cleanup_csv_files()
        else:
            print("CSV示例文件已保留，你可以手动查看和分析它们。")
            
    except Exception as e:
        print(f"\n❌ 示例运行过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()