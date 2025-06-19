#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BMI计算器启动脚本

这个脚本提供了多种运行模式，方便用户根据需要选择：
1. 完整版BMI计算器
2. 简化版BMI计算器（学习版）
3. 测试模式
4. 演示模式

作者：Python学习者
日期：2024年
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def show_menu():
    """
    显示主菜单
    """
    print("\n" + "="*60)
    print("BMI健康计算器 - 启动菜单")
    print("="*60)
    print("""
请选择运行模式：

1. 完整版BMI计算器
   - 功能完整的BMI计算和健康评估工具
   - 支持数据保存和历史记录
   - 提供详细的健康建议

2. 简化版BMI计算器（学习版）
   - 专为学习运算符设计
   - 详细展示计算过程
   - 演示各种运算符的使用

3. 运行测试套件
   - 执行所有单元测试
   - 验证程序功能正确性
   - 包含性能和边界测试

4. 查看项目信息
   - 显示项目结构和说明
   - 查看学习目标和要求

5. 退出程序

""")


def run_full_calculator():
    """
    运行完整版BMI计算器
    """
    try:
        print("\n启动完整版BMI计算器...")
        from bmi_calculator import main
        main()
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保 bmi_calculator.py 文件存在且无语法错误")
    except Exception as e:
        print(f"❌ 运行错误: {e}")


def run_simple_calculator():
    """
    运行简化版BMI计算器
    """
    try:
        print("\n启动简化版BMI计算器（学习版）...")
        from simple_bmi import main
        main()
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保 simple_bmi.py 文件存在且无语法错误")
    except Exception as e:
        print(f"❌ 运行错误: {e}")


def run_tests():
    """
    运行测试套件
    """
    try:
        print("\n启动测试套件...")
        from test_bmi import main
        main()
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保 test_bmi.py 文件存在且无语法错误")
    except Exception as e:
        print(f"❌ 运行错误: {e}")


def show_project_info():
    """
    显示项目信息
    """
    print("\n" + "="*60)
    print("项目信息")
    print("="*60)
    
    print("""
📁 项目结构：

project/
├── README.md              # 项目说明文档
├── bmi_calculator.py      # 完整版BMI计算器
├── simple_bmi.py          # 简化版BMI计算器（学习版）
├── test_bmi.py           # 测试文件
├── config.py             # 配置文件（常量定义）
└── run.py                # 启动脚本（当前文件）

🎯 学习目标：

1. 掌握算术运算符的使用
   - 基本运算：+, -, *, /, //, %, **
   - 在BMI计算中的应用
   - 单位转换计算

2. 理解比较运算符的应用
   - 关系比较：>, <, >=, <=, ==, !=
   - BMI分类判断
   - 数据验证

3. 掌握逻辑运算符的组合
   - 逻辑运算：and, or, not
   - 复合条件判断
   - 短路求值

4. 理解运算符优先级
   - 运算顺序规则
   - 括号的使用
   - 复杂表达式的计算

💡 使用建议：

- 初学者建议先运行"简化版BMI计算器"，详细了解运算符的使用
- 理解基本概念后，再体验"完整版BMI计算器"的实际应用
- 通过测试套件验证自己对代码的理解
- 可以修改代码参数，观察不同的计算结果

📚 相关文件：

- ../tutorial.md: 详细的运算符教程
- ../examples/: 运算符使用示例
- ../exercises/: 练习题和解答

""")


def check_dependencies():
    """
    检查依赖文件是否存在
    """
    required_files = [
        'bmi_calculator.py',
        'simple_bmi.py',
        'test_bmi.py',
        'config.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("\n⚠️  警告：以下文件缺失：")
        for file in missing_files:
            print(f"   - {file}")
        print("\n某些功能可能无法正常使用。")
        return False
    
    return True


def get_user_choice():
    """
    获取用户选择
    
    返回:
        str: 用户选择的选项
    """
    while True:
        try:
            choice = input("请输入您的选择 (1-5): ").strip()
            if choice in ['1', '2', '3', '4', '5']:
                return choice
            else:
                print("❌ 请输入有效的选项 (1-5)")
        except KeyboardInterrupt:
            print("\n\n程序已退出。")
            sys.exit(0)
        except Exception:
            print("❌ 输入错误，请重试")


def main():
    """
    主函数
    """
    # 检查依赖文件
    check_dependencies()
    
    while True:
        try:
            # 显示菜单
            show_menu()
            
            # 获取用户选择
            choice = get_user_choice()
            
            # 执行相应功能
            if choice == '1':
                run_full_calculator()
            elif choice == '2':
                run_simple_calculator()
            elif choice == '3':
                run_tests()
            elif choice == '4':
                show_project_info()
            elif choice == '5':
                print("\n感谢使用BMI健康计算器！")
                print("祝您学习愉快，身体健康！")
                break
            
            # 询问是否继续
            if choice in ['1', '2', '3']:
                input("\n按回车键返回主菜单...")
        
        except KeyboardInterrupt:
            print("\n\n程序已退出。")
            break
        except Exception as e:
            print(f"\n❌ 程序出现错误: {e}")
            print("请检查代码或联系开发者。")
            input("\n按回车键返回主菜单...")


if __name__ == "__main__":
    # 设置控制台编码（Windows系统）
    if sys.platform.startswith('win'):
        try:
            import locale
            locale.setlocale(locale.LC_ALL, 'Chinese')
        except:
            pass
    
    # 运行主程序
    main()