#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session07 示例1：基本文件读写操作

本示例演示了Python中最基本的文件读写操作，包括：
- 文件的创建和写入
- 文件的读取（整体读取、按行读取）
- 文件的追加
- with语句的使用

作者: Python教程团队
创建日期: 2024-12-22
"""

from pathlib import Path
from datetime import datetime


def create_sample_file():
    """
    创建一个示例文件
    """
    print("=== 创建示例文件 ===")
    
    # 示例内容
    content = """欢迎来到Python文件操作世界！
这是第二行内容。
这里有一些数字：1, 2, 3, 4, 5
这是包含中文的一行：你好，世界！
最后一行内容。"""
    
    # 使用with语句写入文件（推荐方式）
    filename = 'sample.txt'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"✓ 文件 '{filename}' 创建成功")
    print(f"✓ 文件大小: {Path(filename).stat().st_size} 字节")
    return filename


def read_entire_file(filename):
    """
    读取整个文件内容
    """
    print("\n=== 读取整个文件 ===")
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        
        print("文件内容：")
        print("-" * 30)
        print(content)
        print("-" * 30)
        
        return content
        
    except FileNotFoundError:
        print(f"❌ 文件 '{filename}' 不存在")
        return None
    except Exception as e:
        print(f"❌ 读取文件时发生错误: {e}")
        return None


def read_file_by_lines(filename):
    """
    按行读取文件内容
    """
    print("\n=== 按行读取文件 ===")
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            print("逐行读取：")
            for line_number, line in enumerate(file, 1):
                # strip()去除行尾的换行符
                clean_line = line.strip()
                print(f"第{line_number:2d}行: {clean_line}")
        
        print("\n使用readlines()方法：")
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for i, line in enumerate(lines, 1):
                print(f"第{i:2d}行: {line.strip()}")
                
    except FileNotFoundError:
        print(f"❌ 文件 '{filename}' 不存在")
    except Exception as e:
        print(f"❌ 读取文件时发生错误: {e}")


def append_to_file(filename):
    """
    向文件追加内容
    """
    print("\n=== 向文件追加内容 ===")
    
    # 要追加的内容
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    append_content = f"\n--- 追加内容 ---\n追加时间: {timestamp}\n这是追加的新行内容。"
    
    try:
        # 使用'a'模式追加内容
        with open(filename, 'a', encoding='utf-8') as file:
            file.write(append_content)
        
        print(f"✓ 内容已追加到文件 '{filename}'")
        
        # 显示追加后的文件内容
        print("\n追加后的文件内容：")
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            print("-" * 40)
            print(content)
            print("-" * 40)
            
    except Exception as e:
        print(f"❌ 追加内容时发生错误: {e}")


def write_multiple_lines(filename):
    """
    写入多行内容
    """
    print("\n=== 写入多行内容 ===")
    
    # 准备多行数据
    lines = [
        "这是使用writelines()方法写入的内容\n",
        "第一行：Python文件操作\n",
        "第二行：学习文件读写\n",
        "第三行：掌握文件处理技巧\n",
        "第四行：实践出真知\n"
    ]
    
    new_filename = 'multilines.txt'
    
    try:
        # 使用writelines()写入多行
        with open(new_filename, 'w', encoding='utf-8') as file:
            file.writelines(lines)
        
        print(f"✓ 多行内容已写入文件 '{new_filename}'")
        
        # 读取并显示内容
        with open(new_filename, 'r', encoding='utf-8') as file:
            content = file.read()
            print("\n文件内容：")
            print("-" * 30)
            print(content)
            print("-" * 30)
            
        return new_filename
        
    except Exception as e:
        print(f"❌ 写入多行内容时发生错误: {e}")
        return None


def demonstrate_file_modes():
    """
    演示不同的文件打开模式
    """
    print("\n=== 文件打开模式演示 ===")
    
    test_file = 'mode_test.txt'
    
    # 模式 'w' - 写入模式（覆盖）
    print("1. 'w' 模式 - 写入（覆盖）")
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("这是写入模式的内容\n")
    print("   ✓ 文件已创建并写入内容")
    
    # 模式 'a' - 追加模式
    print("2. 'a' 模式 - 追加")
    with open(test_file, 'a', encoding='utf-8') as f:
        f.write("这是追加的内容\n")
    print("   ✓ 内容已追加")
    
    # 模式 'r' - 读取模式
    print("3. 'r' 模式 - 读取")
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"   文件内容:\n{content}")
    
    # 模式 'r+' - 读写模式
    print("4. 'r+' 模式 - 读写")
    with open(test_file, 'r+', encoding='utf-8') as f:
        # 读取当前内容
        current_content = f.read()
        # 移动到文件开头
        f.seek(0)
        # 写入新内容
        f.write("[修改] " + current_content)
    print("   ✓ 文件内容已修改")
    
    # 显示最终内容
    with open(test_file, 'r', encoding='utf-8') as f:
        final_content = f.read()
        print(f"   最终内容:\n{final_content}")


def file_statistics(filename):
    """
    计算文件统计信息
    """
    print(f"\n=== 文件 '{filename}' 统计信息 ===")
    
    if not Path(filename).exists():
        print(f"❌ 文件 '{filename}' 不存在")
        return
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            lines = content.split('\n')
        
        # 计算统计信息
        file_size = Path(filename).stat().st_size
        line_count = len(lines)
        word_count = len(content.split())
        char_count = len(content)
        char_count_no_spaces = len(content.replace(' ', '').replace('\n', ''))
        
        print(f"文件大小: {file_size} 字节")
        print(f"行数: {line_count}")
        print(f"单词数: {word_count}")
        print(f"字符数（含空格）: {char_count}")
        print(f"字符数（不含空格）: {char_count_no_spaces}")
        
        # 找出最长的行
        if lines:
            longest_line = max(lines, key=len)
            print(f"最长行长度: {len(longest_line)} 字符")
            print(f"最长行内容: '{longest_line.strip()}'")
            
    except Exception as e:
        print(f"❌ 计算统计信息时发生错误: {e}")


def cleanup_files():
    """
    清理示例文件
    """
    print("\n=== 清理示例文件 ===")
    
    files_to_remove = ['sample.txt', 'multilines.txt', 'mode_test.txt']
    
    for filename in files_to_remove:
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
    print("Session07 示例1：基本文件读写操作")
    print("=" * 50)
    
    try:
        # 1. 创建示例文件
        filename = create_sample_file()
        
        # 2. 读取整个文件
        read_entire_file(filename)
        
        # 3. 按行读取文件
        read_file_by_lines(filename)
        
        # 4. 向文件追加内容
        append_to_file(filename)
        
        # 5. 写入多行内容
        multilines_file = write_multiple_lines(filename)
        
        # 6. 演示不同文件模式
        demonstrate_file_modes()
        
        # 7. 计算文件统计信息
        file_statistics(filename)
        if multilines_file:
            file_statistics(multilines_file)
        
        print("\n" + "=" * 50)
        print("✅ 示例1演示完成！")
        
        # 询问是否清理文件
        response = input("\n是否清理示例文件？(y/n): ").lower().strip()
        if response == 'y':
            cleanup_files()
        else:
            print("示例文件已保留，你可以手动查看它们。")
            
    except Exception as e:
        print(f"\n❌ 示例运行过程中发生错误: {e}")


if __name__ == "__main__":
    main()