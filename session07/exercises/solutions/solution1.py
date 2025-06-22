#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session07 练习1解答：基础文件操作

这个文件包含了练习1的完整解答。
学习者可以参考这些解答来理解正确的实现方法。

作者: Python教程团队
创建日期: 2024-12-22
"""

import os
import shutil
from datetime import datetime


def exercise1_create_student_file():
    """
    练习1解答：创建学生信息文件
    """
    filename = 'students.txt'
    
    # 准备学生数据
    students = [
        "张三,20,计算机科学,85",
        "李四,21,数学,92",
        "王五,19,物理,78",
        "赵六,22,化学,88",
        "钱七,20,生物,95",
        "孙八,21,英语,82",
        "周九,19,历史,76",
        "吴十,23,经济学,90"
    ]
    
    # 写入文件
    with open(filename, 'w', encoding='utf-8') as f:
        for student in students:
            f.write(student + '\n')
    
    print(f"✓ 创建文件 {filename}，包含 {len(students)} 个学生")
    return filename


def exercise2_read_and_analyze():
    """
    练习2解答：读取并分析学生文件
    """
    filename = 'students.txt'
    
    if not os.path.exists(filename):
        print(f"❌ 文件 {filename} 不存在，请先运行练习1")
        return None
    
    students = []
    
    # 读取文件并解析数据
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):  # 跳过空行和注释
                parts = line.split(',')
                if len(parts) == 4:
                    name, age, major, score = parts
                    students.append({
                        'name': name,
                        'age': int(age),
                        'major': major,
                        'score': int(score)
                    })
    
    if not students:
        print("❌ 没有找到有效的学生数据")
        return None
    
    # 计算统计信息
    total_students = len(students)
    total_age = sum(s['age'] for s in students)
    total_score = sum(s['score'] for s in students)
    
    avg_age = total_age / total_students
    avg_score = total_score / total_students
    
    # 找到成绩最高的学生
    top_student = max(students, key=lambda s: s['score'])
    
    # 统计各专业学生数量
    major_count = {}
    for student in students:
        major = student['major']
        major_count[major] = major_count.get(major, 0) + 1
    
    # 组织结果
    result = {
        'total_students': total_students,
        'average_age': round(avg_age, 1),
        'average_score': round(avg_score, 1),
        'top_student': top_student['name'],
        'top_score': top_student['score'],
        'major_distribution': major_count
    }
    
    print(f"✓ 分析完成：{total_students}个学生，平均年龄{avg_age:.1f}岁，平均成绩{avg_score:.1f}分")
    print(f"✓ 成绩最高：{top_student['name']}（{top_student['score']}分）")
    print(f"✓ 专业分布：{major_count}")
    
    return result


def exercise3_append_new_students():
    """
    练习3解答：追加新学生信息
    """
    filename = 'students.txt'
    
    if not os.path.exists(filename):
        print(f"❌ 文件 {filename} 不存在，请先运行练习1")
        return 0
    
    # 新学生数据
    new_students = [
        "陈十一,20,艺术,87",
        "林十二,22,音乐,93",
        "黄十三,19,体育,79"
    ]
    
    # 追加到文件
    with open(filename, 'a', encoding='utf-8') as f:
        # 添加注释行
        f.write(f"# 新增学生 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # 添加新学生
        for student in new_students:
            f.write(student + '\n')
    
    print(f"✓ 追加了 {len(new_students)} 个新学生")
    return len(new_students)


def exercise4_filter_students():
    """
    练习4解答：筛选学生信息
    """
    filename = 'students.txt'
    output_filename = 'excellent_students.txt'
    
    if not os.path.exists(filename):
        print(f"❌ 文件 {filename} 不存在，请先运行练习1")
        return 0
    
    students = []
    
    # 读取所有学生数据
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split(',')
                if len(parts) == 4:
                    name, age, major, score = parts
                    students.append({
                        'name': name,
                        'age': int(age),
                        'major': major,
                        'score': int(score),
                        'line': line
                    })
    
    # 筛选优秀学生（成绩>=90）
    excellent_students = [s for s in students if s['score'] >= 90]
    
    # 按成绩从高到低排序
    excellent_students.sort(key=lambda s: s['score'], reverse=True)
    
    # 写入新文件
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write("优秀学生名单\n")
        f.write("=" * 30 + "\n")
        f.write("姓名,年龄,专业,成绩\n")
        
        for student in excellent_students:
            f.write(student['line'] + '\n')
    
    print(f"✓ 筛选出 {len(excellent_students)} 个优秀学生，保存到 {output_filename}")
    if excellent_students:
        print(f"✓ 最高分：{excellent_students[0]['name']}（{excellent_students[0]['score']}分）")
    
    return len(excellent_students)


def exercise5_backup_and_modify():
    """
    练习5解答：备份和修改文件
    """
    filename = 'students.txt'
    backup_filename = 'students_backup.txt'
    
    if not os.path.exists(filename):
        print(f"❌ 文件 {filename} 不存在，请先运行练习1")
        return 0
    
    # 创建备份
    shutil.copy2(filename, backup_filename)
    print(f"✓ 创建备份文件：{backup_filename}")
    
    students = []
    comments = []
    modified_count = 0
    
    # 读取原文件
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or not line:
                comments.append(line)
            else:
                parts = line.split(',')
                if len(parts) == 4:
                    name, age, major, score = parts
                    old_score = int(score)
                    new_score = min(100, old_score + 5)  # 提高5分，但不超过100
                    
                    students.append(f"{name},{age},{major},{new_score}")
                    if new_score != old_score:
                        modified_count += 1
    
    # 写回原文件
    with open(filename, 'w', encoding='utf-8') as f:
        # 写入学生数据
        for student in students:
            f.write(student + '\n')
        
        # 写入原有注释
        for comment in comments:
            f.write(comment + '\n')
        
        # 添加修改日志
        f.write(f"# 成绩已于{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}统一提高5分\n")
    
    print(f"✓ 修改了 {modified_count} 个学生的成绩")
    return modified_count


def exercise6_file_statistics():
    """
    练习6解答：文件统计信息
    """
    filename = 'students.txt'
    report_filename = 'file_stats.txt'
    
    if not os.path.exists(filename):
        print(f"❌ 文件 {filename} 不存在，请先运行练习1")
        return None
    
    # 获取文件大小
    file_size = os.path.getsize(filename)
    
    # 读取文件内容进行分析
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    # 计算统计信息
    line_count = len([line for line in lines if line.strip()])
    char_count = len(content)
    word_count = len(content.split())
    
    # 组织统计结果
    stats = {
        'filename': filename,
        'file_size_bytes': file_size,
        'line_count': line_count,
        'character_count': char_count,
        'word_count': word_count,
        'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # 创建统计报告
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write("文件统计报告\n")
        f.write("=" * 30 + "\n")
        f.write(f"文件名: {stats['filename']}\n")
        f.write(f"文件大小: {stats['file_size_bytes']} 字节\n")
        f.write(f"行数: {stats['line_count']} 行\n")
        f.write(f"字符数: {stats['character_count']} 个字符\n")
        f.write(f"单词数: {stats['word_count']} 个单词\n")
        f.write(f"分析时间: {stats['analysis_time']}\n")
        
        # 添加详细分析
        f.write("\n详细分析:\n")
        f.write("-" * 20 + "\n")
        f.write(f"平均每行字符数: {char_count / line_count if line_count > 0 else 0:.1f}\n")
        f.write(f"平均每行单词数: {word_count / line_count if line_count > 0 else 0:.1f}\n")
        f.write(f"文件大小（KB）: {file_size / 1024:.2f}\n")
    
    print(f"✓ 文件统计完成，报告保存到 {report_filename}")
    print(f"✓ 文件大小：{file_size}字节，{line_count}行，{char_count}个字符")
    
    return stats


def exercise7_error_handling():
    """
    练习7解答：错误处理
    """
    nonexistent_file = 'nonexistent.txt'
    error_log_file = 'error_log.txt'
    
    error_info = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'attempted_file': nonexistent_file,
        'error_type': None,
        'error_message': None,
        'handled_successfully': False
    }
    
    try:
        # 尝试读取不存在的文件
        with open(nonexistent_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        error_info['handled_successfully'] = True
        error_info['error_message'] = "文件读取成功（意外情况）"
        
    except FileNotFoundError as e:
        error_info['error_type'] = 'FileNotFoundError'
        error_info['error_message'] = f"文件不存在: {str(e)}"
        error_info['handled_successfully'] = True
        
    except PermissionError as e:
        error_info['error_type'] = 'PermissionError'
        error_info['error_message'] = f"权限不足: {str(e)}"
        error_info['handled_successfully'] = True
        
    except Exception as e:
        error_info['error_type'] = type(e).__name__
        error_info['error_message'] = f"未知错误: {str(e)}"
        error_info['handled_successfully'] = True
    
    # 记录错误日志
    try:
        with open(error_log_file, 'a', encoding='utf-8') as f:
            f.write(f"错误日志记录\n")
            f.write(f"时间: {error_info['timestamp']}\n")
            f.write(f"尝试访问文件: {error_info['attempted_file']}\n")
            f.write(f"错误类型: {error_info['error_type']}\n")
            f.write(f"错误信息: {error_info['error_message']}\n")
            f.write(f"处理状态: {'成功' if error_info['handled_successfully'] else '失败'}\n")
            f.write("-" * 50 + "\n")
        
        print(f"✓ 错误处理完成，日志记录到 {error_log_file}")
        print(f"✓ 错误类型：{error_info['error_type']}")
        print(f"✓ 处理状态：{'成功' if error_info['handled_successfully'] else '失败'}")
        
    except Exception as log_error:
        print(f"❌ 写入错误日志失败: {log_error}")
        error_info['handled_successfully'] = False
    
    return f"错误处理{'成功' if error_info['handled_successfully'] else '失败'}：{error_info['error_type']}"


def run_all_exercises():
    """
    运行所有练习解答
    """
    print("Session07 练习1解答：基础文件操作")
    print("=" * 50)
    
    exercises = [
        ("练习1：创建学生信息文件", exercise1_create_student_file),
        ("练习2：读取并分析学生文件", exercise2_read_and_analyze),
        ("练习3：追加新学生信息", exercise3_append_new_students),
        ("练习4：筛选学生信息", exercise4_filter_students),
        ("练习5：备份和修改文件", exercise5_backup_and_modify),
        ("练习6：文件统计信息", exercise6_file_statistics),
        ("练习7：错误处理", exercise7_error_handling)
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
    print("- 使用with语句确保文件正确关闭")
    print("- 注意异常处理，特别是FileNotFoundError")
    print("- 数据解析时要验证格式和类型")
    print("- 备份重要文件是好习惯")
    print("- 记录操作日志便于调试")
    print("- 统计信息有助于了解数据特征")
    
    # 显示生成的文件
    generated_files = [
        'students.txt', 'students_backup.txt', 'excellent_students.txt',
        'file_stats.txt', 'error_log.txt'
    ]
    
    print("\n📁 生成的文件：")
    for filename in generated_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"  ✓ {filename} ({size} 字节)")
        else:
            print(f"  - {filename} (未生成)")


if __name__ == "__main__":
    run_all_exercises()