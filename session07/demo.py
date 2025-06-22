#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session07: 文件操作 - 演示代码

本文件演示了Python文件操作的基本用法和实际应用。
包括文件读写、路径处理、目录操作和异常处理。

作者: Python教程团队
创建日期: 2024-12-22
最后修改: 2024-12-22
"""

import os
import json
import csv
from pathlib import Path
from datetime import datetime


def demo_basic_file_operations():
    """
    演示基本文件操作
    """
    print("=== 基本文件操作演示 ===")
    
    # 创建示例文件
    sample_text = """这是一个示例文件。
第二行内容。
第三行包含一些数字：123, 456, 789
最后一行。"""
    
    # 写入文件
    with open('demo_file.txt', 'w', encoding='utf-8') as f:
        f.write(sample_text)
    print("✓ 文件写入完成")
    
    # 读取整个文件
    with open('demo_file.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"文件内容：\n{content}")
    
    # 按行读取
    print("\n按行读取：")
    with open('demo_file.txt', 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            print(f"第{i}行: {line.strip()}")
    
    # 追加内容
    with open('demo_file.txt', 'a', encoding='utf-8') as f:
        f.write(f"\n追加时间: {datetime.now()}")
    print("✓ 内容追加完成")


def demo_path_operations():
    """
    演示路径操作
    """
    print("\n=== 路径操作演示 ===")
    
    # 获取当前工作目录
    current_dir = os.getcwd()
    print(f"当前目录: {current_dir}")
    
    # 使用pathlib进行路径操作
    demo_file = Path('demo_file.txt')
    print(f"文件是否存在: {demo_file.exists()}")
    print(f"文件大小: {demo_file.stat().st_size} 字节")
    print(f"文件名: {demo_file.name}")
    print(f"文件扩展名: {demo_file.suffix}")
    print(f"文件名（无扩展名）: {demo_file.stem}")
    
    # 创建目录结构
    data_dir = Path('demo_data')
    data_dir.mkdir(exist_ok=True)
    
    logs_dir = data_dir / 'logs'
    logs_dir.mkdir(exist_ok=True)
    
    config_dir = data_dir / 'config'
    config_dir.mkdir(exist_ok=True)
    
    print(f"✓ 创建目录结构: {data_dir}")


def demo_csv_operations():
    """
    演示CSV文件操作
    """
    print("\n=== CSV文件操作演示 ===")
    
    # 准备示例数据
    students_data = [
        {'姓名': '张三', '年龄': 20, '成绩': 85, '城市': '北京'},
        {'姓名': '李四', '年龄': 21, '成绩': 92, '城市': '上海'},
        {'姓名': '王五', '年龄': 19, '成绩': 78, '城市': '广州'},
        {'姓名': '赵六', '年龄': 22, '成绩': 88, '城市': '深圳'}
    ]
    
    # 写入CSV文件
    csv_file = Path('demo_data') / 'students.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['姓名', '年龄', '成绩', '城市']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students_data)
    
    print(f"✓ CSV文件已创建: {csv_file}")
    
    # 读取CSV文件
    print("\nCSV文件内容：")
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f"{row['姓名']} - 年龄:{row['年龄']}, 成绩:{row['成绩']}, 城市:{row['城市']}")
    
    # 计算平均成绩
    total_score = 0
    count = 0
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_score += int(row['成绩'])
            count += 1
    
    average_score = total_score / count if count > 0 else 0
    print(f"\n平均成绩: {average_score:.1f}")


def demo_json_operations():
    """
    演示JSON文件操作
    """
    print("\n=== JSON文件操作演示 ===")
    
    # 准备配置数据
    config_data = {
        'app_name': '文件操作演示程序',
        'version': '1.0.0',
        'settings': {
            'debug': True,
            'max_file_size': 1024 * 1024,  # 1MB
            'allowed_extensions': ['.txt', '.csv', '.json'],
            'default_encoding': 'utf-8'
        },
        'database': {
            'host': 'localhost',
            'port': 5432,
            'name': 'demo_db'
        },
        'created_at': datetime.now().isoformat()
    }
    
    # 写入JSON文件
    json_file = Path('demo_data') / 'config' / 'app_config.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(config_data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ JSON配置文件已创建: {json_file}")
    
    # 读取JSON文件
    with open(json_file, 'r', encoding='utf-8') as f:
        loaded_config = json.load(f)
    
    print("\n配置信息：")
    print(f"应用名称: {loaded_config['app_name']}")
    print(f"版本: {loaded_config['version']}")
    print(f"调试模式: {loaded_config['settings']['debug']}")
    print(f"最大文件大小: {loaded_config['settings']['max_file_size']} 字节")
    print(f"允许的扩展名: {', '.join(loaded_config['settings']['allowed_extensions'])}")


def demo_directory_operations():
    """
    演示目录操作
    """
    print("\n=== 目录操作演示 ===")
    
    # 遍历当前目录
    print("当前目录内容：")
    for item in Path('.').iterdir():
        if item.is_file():
            size = item.stat().st_size
            print(f"📄 {item.name} ({size} 字节)")
        elif item.is_dir():
            print(f"📁 {item.name}/")
    
    # 查找特定类型的文件
    print("\n查找所有.txt文件：")
    for txt_file in Path('.').rglob('*.txt'):
        print(f"📄 {txt_file}")
    
    # 查找所有.json文件
    print("\n查找所有.json文件：")
    for json_file in Path('.').rglob('*.json'):
        print(f"📄 {json_file}")


def demo_error_handling():
    """
    演示错误处理
    """
    print("\n=== 错误处理演示 ===")
    
    # 尝试读取不存在的文件
    try:
        with open('nonexistent_file.txt', 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ 文件不存在错误已捕获")
    
    # 安全的文件读取函数
    def safe_read_file(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"❌ 文件 {filename} 不存在")
            return None
        except PermissionError:
            print(f"❌ 没有权限读取文件 {filename}")
            return None
        except UnicodeDecodeError:
            print(f"❌ 文件 {filename} 编码错误")
            return None
        except Exception as e:
            print(f"❌ 读取文件时发生未知错误: {e}")
            return None
    
    # 测试安全读取
    content = safe_read_file('demo_file.txt')
    if content:
        print("✓ 文件读取成功")
    
    content = safe_read_file('nonexistent.txt')
    if content is None:
        print("✓ 错误处理正常")


def demo_file_statistics():
    """
    演示文件统计功能
    """
    print("\n=== 文件统计演示 ===")
    
    filename = 'demo_file.txt'
    
    if not Path(filename).exists():
        print(f"文件 {filename} 不存在")
        return
    
    # 统计文件信息
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 计算统计信息
    line_count = len(lines)
    word_count = 0
    char_count = 0
    
    for line in lines:
        words = line.split()
        word_count += len(words)
        char_count += len(line)
    
    file_size = Path(filename).stat().st_size
    
    print(f"文件: {filename}")
    print(f"文件大小: {file_size} 字节")
    print(f"行数: {line_count}")
    print(f"单词数: {word_count}")
    print(f"字符数: {char_count}")


def cleanup_demo_files():
    """
    清理演示文件
    """
    print("\n=== 清理演示文件 ===")
    
    # 删除演示文件
    demo_file = Path('demo_file.txt')
    if demo_file.exists():
        demo_file.unlink()
        print("✓ 删除 demo_file.txt")
    
    # 删除演示目录（可选）
    # 注意：这里不删除demo_data目录，因为它包含了有用的示例文件
    print("✓ 保留 demo_data/ 目录供进一步学习")


def main():
    """
    主函数：演示程序的入口点
    """
    print("Session07: 文件操作演示")
    print("=" * 50)
    
    try:
        # 执行各种演示
        demo_basic_file_operations()
        demo_path_operations()
        demo_csv_operations()
        demo_json_operations()
        demo_directory_operations()
        demo_error_handling()
        demo_file_statistics()
        
        print("\n" + "=" * 50)
        print("✅ 所有演示完成！")
        print("\n💡 提示：")
        print("- 查看 demo_data/ 目录中生成的示例文件")
        print("- 尝试修改代码并重新运行")
        print("- 完成 exercises/ 目录中的练习题")
        
        # 询问是否清理文件
        response = input("\n是否清理演示文件？(y/n): ").lower().strip()
        if response == 'y':
            cleanup_demo_files()
        
    except Exception as e:
        print(f"\n❌ 演示过程中发生错误: {e}")
        print("请检查代码并重试")


if __name__ == "__main__":
    main()