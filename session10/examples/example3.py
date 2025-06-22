#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example3: 包的使用示例

演示Python包的概念、结构和使用方法
"""

import os
import sys
from datetime import datetime


# 模拟包的结构和功能
class MyToolsPackage:
    """
    模拟一个完整的工具包
    这个类模拟了包的层次结构和功能组织
    """
    
    # 包级别的信息
    __version__ = "2.1.0"
    __author__ = "Python开发团队"
    __description__ = "实用工具包集合"
    
    class MathUtils:
        """数学工具子模块"""
        
        @staticmethod
        def fibonacci(n):
            """
            生成斐波那契数列
            
            Args:
                n (int): 数列长度
            
            Returns:
                list: 斐波那契数列
            """
            if n <= 0:
                return []
            elif n == 1:
                return [0]
            elif n == 2:
                return [0, 1]
            
            fib = [0, 1]
            for i in range(2, n):
                fib.append(fib[i-1] + fib[i-2])
            return fib
        
        @staticmethod
        def prime_factors(n):
            """
            计算质因数分解
            
            Args:
                n (int): 要分解的数
            
            Returns:
                list: 质因数列表
            """
            factors = []
            d = 2
            while d * d <= n:
                while n % d == 0:
                    factors.append(d)
                    n //= d
                d += 1
            if n > 1:
                factors.append(n)
            return factors
        
        @staticmethod
        def is_perfect_number(n):
            """
            判断是否为完全数
            完全数：等于其所有真因数之和的正整数
            """
            if n <= 1:
                return False
            
            divisors_sum = 1  # 1总是因数
            for i in range(2, int(n ** 0.5) + 1):
                if n % i == 0:
                    divisors_sum += i
                    if i != n // i:  # 避免重复计算平方根
                        divisors_sum += n // i
            
            return divisors_sum == n
        
        @staticmethod
        def calculate_statistics(numbers):
            """
            计算数列的统计信息
            """
            if not numbers:
                return None
            
            n = len(numbers)
            total = sum(numbers)
            mean = total / n
            
            # 计算方差和标准差
            variance = sum((x - mean) ** 2 for x in numbers) / n
            std_dev = variance ** 0.5
            
            # 排序以计算中位数
            sorted_nums = sorted(numbers)
            if n % 2 == 0:
                median = (sorted_nums[n//2 - 1] + sorted_nums[n//2]) / 2
            else:
                median = sorted_nums[n//2]
            
            return {
                'count': n,
                'sum': total,
                'mean': mean,
                'median': median,
                'min': min(numbers),
                'max': max(numbers),
                'variance': variance,
                'std_dev': std_dev
            }
    
    class StringUtils:
        """字符串工具子模块"""
        
        @staticmethod
        def caesar_cipher(text, shift):
            """
            凯撒密码加密
            
            Args:
                text (str): 要加密的文本
                shift (int): 位移量
            
            Returns:
                str: 加密后的文本
            """
            result = ""
            for char in text:
                if char.isalpha():
                    ascii_offset = 65 if char.isupper() else 97
                    shifted = (ord(char) - ascii_offset + shift) % 26
                    result += chr(shifted + ascii_offset)
                else:
                    result += char
            return result
        
        @staticmethod
        def caesar_decipher(text, shift):
            """凯撒密码解密"""
            return MyToolsPackage.StringUtils.caesar_cipher(text, -shift)
        
        @staticmethod
        def generate_acronym(phrase):
            """
            生成首字母缩写
            
            Args:
                phrase (str): 短语
            
            Returns:
                str: 首字母缩写
            """
            words = phrase.split()
            acronym = ''.join(word[0].upper() for word in words if word)
            return acronym
        
        @staticmethod
        def text_similarity(text1, text2):
            """
            计算两个文本的相似度（简单的Jaccard相似度）
            
            Returns:
                float: 相似度（0-1之间）
            """
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            
            if not union:
                return 0.0
            
            return len(intersection) / len(union)
        
        @staticmethod
        def extract_emails(text):
            """
            从文本中提取邮箱地址
            """
            import re
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            return re.findall(email_pattern, text)
        
        @staticmethod
        def format_phone_number(phone):
            """
            格式化电话号码
            """
            # 移除所有非数字字符
            digits = ''.join(filter(str.isdigit, phone))
            
            if len(digits) == 11 and digits.startswith('1'):
                # 中国手机号格式
                return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
            elif len(digits) == 10:
                # 美国电话号格式
                return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
            else:
                return phone  # 无法识别格式，返回原始输入
    
    class FileUtils:
        """文件工具子模块"""
        
        @staticmethod
        def analyze_directory(directory_path):
            """
            分析目录结构
            
            Args:
                directory_path (str): 目录路径
            
            Returns:
                dict: 目录分析结果
            """
            if not os.path.exists(directory_path):
                return {'error': '目录不存在'}
            
            analysis = {
                'total_files': 0,
                'total_directories': 0,
                'total_size': 0,
                'file_types': {},
                'largest_file': {'name': '', 'size': 0},
                'oldest_file': {'name': '', 'date': None},
                'newest_file': {'name': '', 'date': None}
            }
            
            try:
                for root, dirs, files in os.walk(directory_path):
                    analysis['total_directories'] += len(dirs)
                    
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            # 文件大小
                            size = os.path.getsize(file_path)
                            analysis['total_size'] += size
                            analysis['total_files'] += 1
                            
                            # 文件类型统计
                            ext = os.path.splitext(file)[1].lower()
                            if not ext:
                                ext = '无扩展名'
                            analysis['file_types'][ext] = analysis['file_types'].get(ext, 0) + 1
                            
                            # 最大文件
                            if size > analysis['largest_file']['size']:
                                analysis['largest_file'] = {'name': file, 'size': size}
                            
                            # 文件时间
                            mtime = os.path.getmtime(file_path)
                            file_date = datetime.fromtimestamp(mtime)
                            
                            if analysis['oldest_file']['date'] is None or file_date < analysis['oldest_file']['date']:
                                analysis['oldest_file'] = {'name': file, 'date': file_date}
                            
                            if analysis['newest_file']['date'] is None or file_date > analysis['newest_file']['date']:
                                analysis['newest_file'] = {'name': file, 'date': file_date}
                        
                        except OSError:
                            continue  # 跳过无法访问的文件
            
            except PermissionError:
                analysis['error'] = '权限不足'
            
            return analysis
        
        @staticmethod
        def safe_filename(filename):
            """
            创建安全的文件名（移除或替换不安全字符）
            """
            import re
            # 移除或替换不安全的字符
            safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
            # 移除开头和结尾的空格和点
            safe_name = safe_name.strip(' .')
            # 确保不为空
            if not safe_name:
                safe_name = 'unnamed_file'
            return safe_name
        
        @staticmethod
        def generate_unique_filename(directory, base_name):
            """
            在指定目录中生成唯一的文件名
            """
            if not os.path.exists(os.path.join(directory, base_name)):
                return base_name
            
            name, ext = os.path.splitext(base_name)
            counter = 1
            
            while True:
                new_name = f"{name}_{counter}{ext}"
                if not os.path.exists(os.path.join(directory, new_name)):
                    return new_name
                counter += 1
    
    class DataUtils:
        """数据处理子模块"""
        
        @staticmethod
        def csv_to_dict(csv_text, delimiter=','):
            """
            将CSV文本转换为字典列表
            
            Args:
                csv_text (str): CSV格式的文本
                delimiter (str): 分隔符
            
            Returns:
                list: 字典列表
            """
            lines = csv_text.strip().split('\n')
            if not lines:
                return []
            
            headers = [h.strip() for h in lines[0].split(delimiter)]
            result = []
            
            for line in lines[1:]:
                values = [v.strip() for v in line.split(delimiter)]
                if len(values) == len(headers):
                    row_dict = dict(zip(headers, values))
                    result.append(row_dict)
            
            return result
        
        @staticmethod
        def dict_to_csv(data_list, delimiter=','):
            """
            将字典列表转换为CSV文本
            """
            if not data_list:
                return ""
            
            headers = list(data_list[0].keys())
            csv_lines = [delimiter.join(headers)]
            
            for row in data_list:
                values = [str(row.get(header, '')) for header in headers]
                csv_lines.append(delimiter.join(values))
            
            return '\n'.join(csv_lines)
        
        @staticmethod
        def group_by(data_list, key_func):
            """
            按指定条件对数据进行分组
            
            Args:
                data_list (list): 数据列表
                key_func (function): 分组键函数
            
            Returns:
                dict: 分组结果
            """
            groups = {}
            for item in data_list:
                key = key_func(item)
                if key not in groups:
                    groups[key] = []
                groups[key].append(item)
            return groups
        
        @staticmethod
        def filter_data(data_list, condition_func):
            """
            根据条件过滤数据
            """
            return [item for item in data_list if condition_func(item)]
        
        @staticmethod
        def sort_data(data_list, key_func, reverse=False):
            """
            对数据进行排序
            """
            return sorted(data_list, key=key_func, reverse=reverse)


def demonstrate_package_structure():
    """
    演示包的结构和信息
    """
    print("=== 包结构演示 ===")
    
    # 包的基本信息
    pkg = MyToolsPackage
    print(f"包名: MyToolsPackage")
    print(f"版本: {pkg.__version__}")
    print(f"作者: {pkg.__author__}")
    print(f"描述: {pkg.__description__}")
    
    # 包的模块结构
    print("\n包含的模块:")
    modules = ['MathUtils', 'StringUtils', 'FileUtils', 'DataUtils']
    for module in modules:
        print(f"  - {module}")
        # 列出模块的主要方法
        module_class = getattr(pkg, module)
        methods = [method for method in dir(module_class) 
                  if not method.startswith('_') and callable(getattr(module_class, method))]
        print(f"    方法: {', '.join(methods[:3])}{'...' if len(methods) > 3 else ''}")
    
    print()


def demonstrate_math_utils():
    """
    演示数学工具模块
    """
    print("=== MathUtils模块演示 ===")
    
    # 斐波那契数列
    fib_10 = MyToolsPackage.MathUtils.fibonacci(10)
    print(f"斐波那契数列(前10项): {fib_10}")
    
    # 质因数分解
    number = 60
    factors = MyToolsPackage.MathUtils.prime_factors(number)
    print(f"{number}的质因数分解: {factors}")
    
    # 完全数检测
    perfect_candidates = [6, 28, 12, 496]
    print("\n完全数检测:")
    for num in perfect_candidates:
        is_perfect = MyToolsPackage.MathUtils.is_perfect_number(num)
        print(f"  {num}: {'是' if is_perfect else '不是'}完全数")
    
    # 统计计算
    data = [85, 92, 78, 96, 88, 91, 84, 89, 93, 87]
    stats = MyToolsPackage.MathUtils.calculate_statistics(data)
    print(f"\n数据统计 {data}:")
    if stats:
        print(f"  平均值: {stats['mean']:.2f}")
        print(f"  中位数: {stats['median']:.2f}")
        print(f"  最小值: {stats['min']}")
        print(f"  最大值: {stats['max']}")
        print(f"  标准差: {stats['std_dev']:.2f}")
    
    print()


def demonstrate_string_utils():
    """
    演示字符串工具模块
    """
    print("=== StringUtils模块演示 ===")
    
    # 凯撒密码
    message = "Hello World"
    shift = 3
    encrypted = MyToolsPackage.StringUtils.caesar_cipher(message, shift)
    decrypted = MyToolsPackage.StringUtils.caesar_decipher(encrypted, shift)
    print(f"凯撒密码演示:")
    print(f"  原文: {message}")
    print(f"  加密(位移{shift}): {encrypted}")
    print(f"  解密: {decrypted}")
    
    # 首字母缩写
    phrases = [
        "Application Programming Interface",
        "Hypertext Transfer Protocol",
        "Artificial Intelligence"
    ]
    print("\n首字母缩写:")
    for phrase in phrases:
        acronym = MyToolsPackage.StringUtils.generate_acronym(phrase)
        print(f"  '{phrase}' -> {acronym}")
    
    # 文本相似度
    text1 = "Python is a programming language"
    text2 = "Java is a programming language"
    text3 = "I love eating pizza"
    
    similarity1 = MyToolsPackage.StringUtils.text_similarity(text1, text2)
    similarity2 = MyToolsPackage.StringUtils.text_similarity(text1, text3)
    
    print(f"\n文本相似度:")
    print(f"  文本1: '{text1}'")
    print(f"  文本2: '{text2}'")
    print(f"  相似度: {similarity1:.2f}")
    print(f"  文本3: '{text3}'")
    print(f"  相似度: {similarity2:.2f}")
    
    # 邮箱提取
    text_with_emails = "联系我们: support@example.com 或 admin@test.org，也可以发送到 user123@gmail.com"
    emails = MyToolsPackage.StringUtils.extract_emails(text_with_emails)
    print(f"\n从文本中提取邮箱:")
    print(f"  文本: '{text_with_emails}'")
    print(f"  邮箱: {emails}")
    
    # 电话号码格式化
    phone_numbers = ["13812345678", "1234567890", "(555) 123-4567"]
    print(f"\n电话号码格式化:")
    for phone in phone_numbers:
        formatted = MyToolsPackage.StringUtils.format_phone_number(phone)
        print(f"  {phone} -> {formatted}")
    
    print()


def demonstrate_file_utils():
    """
    演示文件工具模块
    """
    print("=== FileUtils模块演示 ===")
    
    # 分析当前目录
    current_dir = "."
    analysis = MyToolsPackage.FileUtils.analyze_directory(current_dir)
    
    print(f"目录分析结果 ('{current_dir}'):")
    if 'error' not in analysis:
        print(f"  总文件数: {analysis['total_files']}")
        print(f"  总目录数: {analysis['total_directories']}")
        print(f"  总大小: {analysis['total_size']:,} 字节")
        
        print(f"  文件类型分布:")
        for ext, count in sorted(analysis['file_types'].items()):
            print(f"    {ext}: {count}个")
        
        if analysis['largest_file']['name']:
            print(f"  最大文件: {analysis['largest_file']['name']} ({analysis['largest_file']['size']:,} 字节)")
    else:
        print(f"  错误: {analysis['error']}")
    
    # 安全文件名
    unsafe_names = [
        "file<name>.txt",
        "document:with|special*chars.pdf",
        "  .hidden file  ",
        ""
    ]
    
    print(f"\n安全文件名转换:")
    for unsafe in unsafe_names:
        safe = MyToolsPackage.FileUtils.safe_filename(unsafe)
        print(f"  '{unsafe}' -> '{safe}'")
    
    # 唯一文件名生成
    directory = "."
    base_names = ["test.txt", "example.py", "data.csv"]
    
    print(f"\n唯一文件名生成:")
    for base_name in base_names:
        unique_name = MyToolsPackage.FileUtils.generate_unique_filename(directory, base_name)
        print(f"  '{base_name}' -> '{unique_name}'")
    
    print()


def demonstrate_data_utils():
    """
    演示数据处理模块
    """
    print("=== DataUtils模块演示 ===")
    
    # CSV处理
    csv_data = """姓名,年龄,城市,职业
张三,25,北京,工程师
李四,30,上海,设计师
王五,28,广州,教师
赵六,35,深圳,医生"""
    
    print("CSV数据处理:")
    print(f"原始CSV:\n{csv_data}")
    
    # CSV转字典
    dict_data = MyToolsPackage.DataUtils.csv_to_dict(csv_data)
    print(f"\n转换为字典列表:")
    for i, person in enumerate(dict_data):
        print(f"  {i+1}. {person}")
    
    # 数据分组
    city_groups = MyToolsPackage.DataUtils.group_by(dict_data, lambda x: x['城市'])
    print(f"\n按城市分组:")
    for city, people in city_groups.items():
        names = [person['姓名'] for person in people]
        print(f"  {city}: {', '.join(names)}")
    
    # 数据过滤
    young_people = MyToolsPackage.DataUtils.filter_data(
        dict_data, 
        lambda x: int(x['年龄']) < 30
    )
    print(f"\n年龄小于30的人:")
    for person in young_people:
        print(f"  {person['姓名']} ({person['年龄']}岁)")
    
    # 数据排序
    sorted_by_age = MyToolsPackage.DataUtils.sort_data(
        dict_data,
        lambda x: int(x['年龄']),
        reverse=True
    )
    print(f"\n按年龄降序排列:")
    for person in sorted_by_age:
        print(f"  {person['姓名']}: {person['年龄']}岁")
    
    # 转换回CSV
    new_csv = MyToolsPackage.DataUtils.dict_to_csv(young_people)
    print(f"\n年轻人数据转换为CSV:\n{new_csv}")
    
    print()


def demonstrate_package_integration():
    """
    演示包的集成应用
    """
    print("=== 包集成应用演示 ===")
    
    # 综合应用：处理学生成绩数据
    students_csv = """姓名,数学,英语,物理,化学
小明,85,92,78,88
小红,92,88,85,90
小刚,78,85,92,82
小丽,88,90,80,85
小华,90,78,88,92"""
    
    print("学生成绩分析系统")
    print("=" * 30)
    
    # 1. 解析CSV数据
    students = MyToolsPackage.DataUtils.csv_to_dict(students_csv)
    print(f"共有 {len(students)} 名学生")
    
    # 2. 计算每个学生的总分和平均分
    for student in students:
        scores = [int(student[subject]) for subject in ['数学', '英语', '物理', '化学']]
        stats = MyToolsPackage.MathUtils.calculate_statistics(scores)
        student['总分'] = stats['sum']
        student['平均分'] = round(stats['mean'], 1)
    
    # 3. 按总分排序
    sorted_students = MyToolsPackage.DataUtils.sort_data(
        students, 
        lambda x: x['总分'], 
        reverse=True
    )
    
    print("\n成绩排名:")
    for i, student in enumerate(sorted_students, 1):
        print(f"  {i}. {student['姓名']}: 总分{student['总分']}, 平均分{student['平均分']}")
    
    # 4. 分析各科成绩
    subjects = ['数学', '英语', '物理', '化学']
    print("\n各科成绩统计:")
    
    for subject in subjects:
        scores = [int(student[subject]) for student in students]
        stats = MyToolsPackage.MathUtils.calculate_statistics(scores)
        print(f"  {subject}: 平均分{stats['mean']:.1f}, 最高分{stats['max']}, 最低分{stats['min']}")
    
    # 5. 生成成绩报告文件名
    report_filename = "学生成绩报告.txt"
    safe_filename = MyToolsPackage.FileUtils.safe_filename(report_filename)
    unique_filename = MyToolsPackage.FileUtils.generate_unique_filename(".", safe_filename)
    
    print(f"\n报告文件名: {unique_filename}")
    
    # 6. 创建简单的加密消息
    message = f"本次考试共有{len(students)}名学生参加"
    encrypted_message = MyToolsPackage.StringUtils.caesar_cipher(message, 5)
    print(f"\n加密消息: {encrypted_message}")
    print(f"解密消息: {MyToolsPackage.StringUtils.caesar_decipher(encrypted_message, 5)}")
    
    print()


def main():
    """
    主函数
    """
    print("Example3: 包的使用示例")
    print("=" * 60)
    
    demonstrate_package_structure()
    demonstrate_math_utils()
    demonstrate_string_utils()
    demonstrate_file_utils()
    demonstrate_data_utils()
    demonstrate_package_integration()
    
    print("=" * 60)
    print("示例完成！")
    print("\n包设计要点:")
    print("1. 包提供了更好的代码组织结构")
    print("2. 子模块按功能分类，职责明确")
    print("3. 包级别的信息和文档很重要")
    print("4. 模块间可以相互配合实现复杂功能")
    print("5. 良好的包设计能提高开发效率")


if __name__ == "__main__":
    main()