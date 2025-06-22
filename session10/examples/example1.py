#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example1: 基础模块导入示例

演示Python中各种模块导入方式的使用
"""

# 1. 导入整个模块
import math
import os
import sys

# 2. 导入模块并使用别名
import datetime as dt
import random as rd

# 3. 从模块中导入特定函数或类
from collections import Counter, defaultdict
from pathlib import Path

# 4. 导入多个项目
from json import dumps, loads, JSONDecodeError


def demonstrate_basic_imports():
    """
    演示基本的模块导入和使用
    """
    print("=== 基础模块导入演示 ===")
    
    # 使用math模块
    print("数学运算:")
    print(f"  π = {math.pi:.6f}")
    print(f"  e = {math.e:.6f}")
    print(f"  sin(π/2) = {math.sin(math.pi/2)}")
    print(f"  log(10) = {math.log10(10)}")
    print(f"  √25 = {math.sqrt(25)}")
    
    # 使用os模块
    print("\n系统信息:")
    print(f"  当前目录: {os.getcwd()}")
    print(f"  用户名: {os.environ.get('USERNAME', '未知')}")
    print(f"  路径分隔符: '{os.sep}'")
    
    # 使用sys模块
    print("\nPython信息:")
    print(f"  Python版本: {sys.version.split()[0]}")
    print(f"  平台: {sys.platform}")
    print(f"  模块搜索路径数量: {len(sys.path)}")
    
    print()


def demonstrate_alias_imports():
    """
    演示使用别名的模块导入
    """
    print("=== 别名导入演示 ===")
    
    # 使用datetime别名
    now = dt.datetime.now()
    print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 计算时间差
    future = now + dt.timedelta(days=30, hours=12)
    print(f"30天12小时后: {future.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 使用random别名
    print("\n随机数生成:")
    print(f"  随机整数(1-100): {rd.randint(1, 100)}")
    print(f"  随机浮点数: {rd.random():.4f}")
    
    # 随机选择
    fruits = ['苹果', '香蕉', '橙子', '葡萄', '草莓']
    print(f"  随机水果: {rd.choice(fruits)}")
    
    # 随机打乱列表
    numbers = list(range(1, 6))
    rd.shuffle(numbers)
    print(f"  打乱后的数字: {numbers}")
    
    print()


def demonstrate_specific_imports():
    """
    演示导入特定函数和类
    """
    print("=== 特定导入演示 ===")
    
    # 使用Counter统计
    text = "hello world python programming"
    char_count = Counter(text)
    print(f"字符统计: {dict(char_count.most_common(5))}")
    
    word_list = ['python', 'java', 'python', 'c++', 'python', 'java']
    word_count = Counter(word_list)
    print(f"单词统计: {dict(word_count)}")
    
    # 使用defaultdict
    dd = defaultdict(list)
    dd['fruits'].append('apple')
    dd['fruits'].append('banana')
    dd['colors'].append('red')
    print(f"默认字典: {dict(dd)}")
    
    # 使用Path处理路径
    current_file = Path(__file__)
    print(f"\n文件路径信息:")
    print(f"  文件名: {current_file.name}")
    print(f"  父目录: {current_file.parent.name}")
    print(f"  文件扩展名: {current_file.suffix}")
    print(f"  绝对路径: {current_file.absolute()}")
    
    print()


def demonstrate_json_operations():
    """
    演示JSON模块的使用
    """
    print("=== JSON操作演示 ===")
    
    # 创建Python对象
    student = {
        'name': '张三',
        'age': 20,
        'major': '计算机科学',
        'grades': [85, 92, 78, 96],
        'is_graduate': False
    }
    
    # 转换为JSON字符串
    json_str = dumps(student, ensure_ascii=False, indent=2)
    print(f"JSON字符串:\n{json_str}")
    
    # 从JSON字符串解析
    try:
        parsed_data = loads(json_str)
        print(f"\n解析后的数据类型: {type(parsed_data)}")
        print(f"学生姓名: {parsed_data['name']}")
        print(f"平均成绩: {sum(parsed_data['grades']) / len(parsed_data['grades']):.1f}")
    except JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
    
    print()


def demonstrate_module_introspection():
    """
    演示模块内省功能
    """
    print("=== 模块内省演示 ===")
    
    # 查看模块的属性
    print("math模块的部分函数:")
    math_functions = [name for name in dir(math) 
                     if callable(getattr(math, name)) and not name.startswith('_')]
    for i, func in enumerate(math_functions[:8]):
        print(f"  {func}")
    
    print(f"\nmath模块总共有 {len(math_functions)} 个公开函数")
    
    # 查看模块文档
    print(f"\nmath模块文档摘要:")
    print(f"  {math.__doc__[:100]}...")
    
    # 检查对象类型
    print(f"\n类型检查:")
    print(f"  math.pi 是数字吗? {isinstance(math.pi, (int, float))}")
    print(f"  math.sqrt 是函数吗? {callable(math.sqrt)}")
    
    print()


def practical_example():
    """
    实际应用示例：文件分析器
    """
    print("=== 实际应用：文件分析器 ===")
    
    # 分析当前目录的文件
    current_dir = Path('.')
    
    # 统计文件类型
    file_types = Counter()
    file_sizes = []
    
    try:
        for file_path in current_dir.iterdir():
            if file_path.is_file():
                file_types[file_path.suffix or '无扩展名'] += 1
                try:
                    file_sizes.append(file_path.stat().st_size)
                except OSError:
                    pass
        
        print(f"当前目录文件统计:")
        print(f"  总文件数: {sum(file_types.values())}")
        print(f"  文件类型分布:")
        for ext, count in file_types.most_common():
            print(f"    {ext}: {count}个")
        
        if file_sizes:
            total_size = sum(file_sizes)
            avg_size = total_size / len(file_sizes)
            print(f"  总大小: {total_size:,} 字节")
            print(f"  平均大小: {avg_size:.1f} 字节")
            print(f"  最大文件: {max(file_sizes):,} 字节")
            print(f"  最小文件: {min(file_sizes):,} 字节")
    
    except PermissionError:
        print("  权限不足，无法访问某些文件")
    
    print()


def main():
    """
    主函数
    """
    print("Example1: 基础模块导入示例")
    print("=" * 40)
    
    demonstrate_basic_imports()
    demonstrate_alias_imports()
    demonstrate_specific_imports()
    demonstrate_json_operations()
    demonstrate_module_introspection()
    practical_example()
    
    print("=" * 40)
    print("示例完成！")
    print("\n关键要点:")
    print("1. import module_name - 导入整个模块")
    print("2. import module_name as alias - 使用别名")
    print("3. from module import item - 导入特定项目")
    print("4. 合理使用导入方式可以提高代码可读性")


if __name__ == "__main__":
    main()