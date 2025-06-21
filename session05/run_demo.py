#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session05 快速演示脚本

这个脚本提供了多种方式来体验Session05的内容：
1. 运行基础演示代码
2. 启动学生管理系统演示
3. 启动交互式命令行界面
4. 运行练习题

使用方法：
    python run_demo.py

作者: Python教程团队
创建日期: 2024-12-21
"""

import os
import sys
import subprocess
from pathlib import Path


def clear_screen():
    """清屏"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f" {title} ".center(60))
    print("=" * 60)


def print_menu():
    """打印主菜单"""
    clear_screen()
    print_header("Session05 - Python数据结构基础")
    print("\n欢迎来到Session05！本节课将学习Python的核心数据结构：")
    print("📚 列表 (List) - 有序可变序列")
    print("📦 元组 (Tuple) - 有序不可变序列")
    print("🗂️  字典 (Dict) - 键值对映射")
    print("🔗 集合 (Set) - 无序不重复集合")
    
    print("\n请选择体验方式：")
    print("1. 📖 查看基础演示代码 (demo.py)")
    print("2. 🔍 运行示例代码")
    print("3. 🎯 学生管理系统演示")
    print("4. 💻 交互式管理系统")
    print("5. 📝 运行练习题")
    print("6. ✅ 查看练习答案")
    print("7. 📋 查看教程文档")
    print("8. ℹ️  项目信息")
    print("0. 🚪 退出")
    print("-" * 60)


def run_file(file_path, description):
    """运行指定的Python文件"""
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    print(f"\n🚀 正在运行: {description}")
    print(f"📁 文件路径: {file_path}")
    print("-" * 50)
    
    try:
        # 使用subprocess运行Python文件
        result = subprocess.run([sys.executable, file_path], 
                              capture_output=False, 
                              text=True, 
                              cwd=os.path.dirname(file_path) or '.')
        
        if result.returncode == 0:
            print("\n✅ 运行完成")
        else:
            print(f"\n❌ 运行出错，退出码: {result.returncode}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"\n❌ 运行失败: {e}")
        return False


def show_file_content(file_path, description, max_lines=50):
    """显示文件内容"""
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return
    
    print(f"\n📖 {description}")
    print(f"📁 文件路径: {file_path}")
    print("-" * 60)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if len(lines) <= max_lines:
            print(''.join(lines))
        else:
            print(''.join(lines[:max_lines]))
            print(f"\n... (文件还有 {len(lines) - max_lines} 行，请直接打开文件查看完整内容)")
            
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")


def get_user_input(prompt):
    """获取用户输入"""
    try:
        return input(prompt).strip()
    except KeyboardInterrupt:
        print("\n\n👋 再见！")
        sys.exit(0)


def pause():
    """暂停等待用户输入"""
    get_user_input("\n按回车键继续...")


def show_project_info():
    """显示项目信息"""
    clear_screen()
    print_header("Session05 项目信息")
    
    print("\n📚 学习目标：")
    print("• 掌握Python四种核心数据结构的特点和用法")
    print("• 理解不同数据结构的适用场景")
    print("• 学会在实际项目中选择合适的数据结构")
    print("• 掌握数据结构的常用方法和操作技巧")
    
    print("\n🗂️ 文件结构：")
    print("session05/")
    print("├── README.md              # 总体介绍")
    print("├── tutorial.md            # 详细教程")
    print("├── demo.py               # 基础演示代码")
    print("├── run_demo.py           # 快速启动脚本")
    print("├── examples/             # 示例代码")
    print("│   ├── example1.py       # 列表详解")
    print("│   ├── example2.py       # 元组和字典")
    print("│   └── example3.py       # 集合和最佳实践")
    print("├── exercises/            # 练习题")
    print("│   ├── exercise1.py      # 列表和元组练习")
    print("│   ├── exercise2.py      # 字典和集合练习")
    print("│   └── solutions/        # 参考答案")
    print("│       ├── solution1.py  # 练习1答案")
    print("│       └── solution2.py  # 练习2答案")
    print("└── project/              # 综合项目")
    print("    ├── student_manager.py # 核心管理类")
    print("    ├── cli_interface.py   # 命令行界面")
    print("    └── README.md          # 项目说明")
    
    print("\n🎯 核心概念：")
    print("• 列表 (List): [1, 2, 3] - 有序、可变、允许重复")
    print("• 元组 (Tuple): (1, 2, 3) - 有序、不可变、允许重复")
    print("• 字典 (Dict): {'key': 'value'} - 无序、可变、键唯一")
    print("• 集合 (Set): {1, 2, 3} - 无序、可变、元素唯一")
    
    print("\n💡 学习建议：")
    print("1. 先运行基础演示，理解各数据结构的特点")
    print("2. 查看示例代码，学习实际应用场景")
    print("3. 完成练习题，巩固所学知识")
    print("4. 体验综合项目，理解数据结构在实际开发中的应用")
    print("5. 对比不同数据结构的性能和适用场景")
    
    pause()


def main():
    """主函数"""
    # 获取当前脚本所在目录
    current_dir = Path(__file__).parent
    
    # 定义文件路径
    files = {
        'demo': current_dir / 'demo.py',
        'example1': current_dir / 'examples' / 'example1.py',
        'example2': current_dir / 'examples' / 'example2.py',
        'example3': current_dir / 'examples' / 'example3.py',
        'exercise1': current_dir / 'exercises' / 'exercise1.py',
        'exercise2': current_dir / 'exercises' / 'exercise2.py',
        'solution1': current_dir / 'exercises' / 'solutions' / 'solution1.py',
        'solution2': current_dir / 'exercises' / 'solutions' / 'solution2.py',
        'student_manager': current_dir / 'project' / 'student_manager.py',
        'cli_interface': current_dir / 'project' / 'cli_interface.py',
        'tutorial': current_dir / 'tutorial.md',
        'readme': current_dir / 'README.md'
    }
    
    while True:
        print_menu()
        choice = get_user_input("请选择 (0-8): ")
        
        if choice == '1':
            # 查看基础演示代码
            show_file_content(files['demo'], "基础演示代码 (demo.py)", 100)
            pause()
            
        elif choice == '2':
            # 运行示例代码
            clear_screen()
            print_header("示例代码演示")
            print("\n选择要运行的示例：")
            print("1. 📝 列表详解 (example1.py)")
            print("2. 📦 元组和字典 (example2.py)")
            print("3. 🔗 集合和最佳实践 (example3.py)")
            print("4. 🎯 基础演示 (demo.py)")
            print("0. 返回主菜单")
            
            sub_choice = get_user_input("\n请选择 (0-4): ")
            
            if sub_choice == '1':
                run_file(files['example1'], "列表详解示例")
            elif sub_choice == '2':
                run_file(files['example2'], "元组和字典示例")
            elif sub_choice == '3':
                run_file(files['example3'], "集合和最佳实践示例")
            elif sub_choice == '4':
                run_file(files['demo'], "基础演示")
            elif sub_choice == '0':
                continue
            else:
                print("❌ 无效选择")
            
            if sub_choice != '0':
                pause()
                
        elif choice == '3':
            # 学生管理系统演示
            run_file(files['student_manager'], "学生管理系统演示")
            pause()
            
        elif choice == '4':
            # 交互式管理系统
            print("\n🚀 启动交互式学生管理系统...")
            print("💡 提示：这是一个完整的命令行应用，你可以：")
            print("   • 添加和管理学生信息")
            print("   • 录入和查询成绩")
            print("   • 查看统计分析")
            print("   • 导入导出数据")
            print("\n按Ctrl+C可以随时退出程序")
            pause()
            
            run_file(files['cli_interface'], "交互式学生管理系统")
            pause()
            
        elif choice == '5':
            # 运行练习题
            clear_screen()
            print_header("练习题")
            print("\n选择要运行的练习：")
            print("1. 📝 练习1：列表和元组基础操作")
            print("2. 🗂️  练习2：字典和集合操作")
            print("0. 返回主菜单")
            
            sub_choice = get_user_input("\n请选择 (0-2): ")
            
            if sub_choice == '1':
                run_file(files['exercise1'], "列表和元组练习")
            elif sub_choice == '2':
                run_file(files['exercise2'], "字典和集合练习")
            elif sub_choice == '0':
                continue
            else:
                print("❌ 无效选择")
            
            if sub_choice != '0':
                pause()
                
        elif choice == '6':
            # 查看练习答案
            clear_screen()
            print_header("练习答案")
            print("\n选择要查看的答案：")
            print("1. 📝 练习1答案：列表和元组操作")
            print("2. 🗂️  练习2答案：字典和集合操作")
            print("3. 🚀 运行答案演示")
            print("0. 返回主菜单")
            
            sub_choice = get_user_input("\n请选择 (0-3): ")
            
            if sub_choice == '1':
                show_file_content(files['solution1'], "练习1参考答案", 80)
            elif sub_choice == '2':
                show_file_content(files['solution2'], "练习2参考答案", 80)
            elif sub_choice == '3':
                print("\n选择要运行的答案演示：")
                print("1. 运行练习1答案演示")
                print("2. 运行练习2答案演示")
                
                demo_choice = get_user_input("请选择 (1-2): ")
                if demo_choice == '1':
                    run_file(files['solution1'], "练习1答案演示")
                elif demo_choice == '2':
                    run_file(files['solution2'], "练习2答案演示")
            elif sub_choice == '0':
                continue
            else:
                print("❌ 无效选择")
            
            if sub_choice != '0':
                pause()
                
        elif choice == '7':
            # 查看教程文档
            clear_screen()
            print_header("教程文档")
            print("\n选择要查看的文档：")
            print("1. 📚 完整教程 (tutorial.md)")
            print("2. 📋 项目说明 (README.md)")
            print("3. 🎯 项目详细说明 (project/README.md)")
            print("0. 返回主菜单")
            
            sub_choice = get_user_input("\n请选择 (0-3): ")
            
            if sub_choice == '1':
                show_file_content(files['tutorial'], "完整教程文档", 100)
            elif sub_choice == '2':
                show_file_content(files['readme'], "项目说明文档", 80)
            elif sub_choice == '3':
                show_file_content(current_dir / 'project' / 'README.md', "项目详细说明", 100)
            elif sub_choice == '0':
                continue
            else:
                print("❌ 无效选择")
            
            if sub_choice != '0':
                pause()
                
        elif choice == '8':
            # 项目信息
            show_project_info()
            
        elif choice == '0':
            # 退出
            clear_screen()
            print_header("感谢学习 Session05！")
            print("\n🎉 恭喜你完成了Python数据结构基础的学习！")
            print("\n📚 你已经掌握了：")
            print("   ✅ 列表 (List) 的创建、操作和应用")
            print("   ✅ 元组 (Tuple) 的特性和使用场景")
            print("   ✅ 字典 (Dict) 的键值对操作")
            print("   ✅ 集合 (Set) 的去重和运算")
            print("   ✅ 数据结构的选择原则")
            print("   ✅ 实际项目中的应用技巧")
            
            print("\n🚀 下一步建议：")
            print("   • 继续学习更高级的数据结构（如deque、namedtuple）")
            print("   • 深入理解算法复杂度和性能优化")
            print("   • 在实际项目中应用所学知识")
            print("   • 学习函数式编程和面向对象编程")
            
            print("\n💡 记住：选择合适的数据结构是编程的基本功！")
            print("\n👋 再见，继续加油学习Python！")
            break
            
        else:
            print("❌ 无效选择，请重新输入")
            pause()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 程序被用户中断，再见！")
    except Exception as e:
        print(f"\n❌ 程序发生错误: {e}")
        print("请检查文件是否完整或联系开发者。")