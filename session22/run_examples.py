#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session22 TDD教程 - 运行脚本

这个脚本用于运行所有的示例和演示代码
作者: Python教程
日期: 2024年
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"\n{'='*60}")
    print(f"正在运行: {description}")
    print(f"命令: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        if result.stdout:
            print("输出:")
            print(result.stdout)
        if result.stderr:
            print("错误:")
            print(result.stderr)
        if result.returncode != 0:
            print(f"命令执行失败，返回码: {result.returncode}")
        else:
            print("命令执行成功!")
    except Exception as e:
        print(f"执行命令时出错: {e}")
    
    print(f"{'='*60}\n")

def main():
    """主函数"""
    print("Session22 TDD教程 - 示例运行器")
    print("本脚本将依次运行所有示例和演示代码")
    
    # 获取当前目录
    current_dir = Path(__file__).parent
    os.chdir(current_dir)
    
    # 检查Python环境
    print(f"Python版本: {sys.version}")
    print(f"当前工作目录: {current_dir}")
    
    # 运行示例列表
    examples = [
        {
            'cmd': [sys.executable, 'demo.py'],
            'desc': 'TDD演示 - 科学计算器开发'
        },
        {
            'cmd': [sys.executable, 'examples/example1_basic_unittest.py'],
            'desc': '示例1 - unittest基础用法'
        },
        {
            'cmd': [sys.executable, 'examples/example2_pytest_advanced.py'],
            'desc': '示例2 - pytest高级用法（仅显示说明）'
        },
        {
            'cmd': ['pytest', 'demo.py', '-v'],
            'desc': '使用pytest运行TDD演示'
        },
        {
            'cmd': ['pytest', 'examples/example2_pytest_advanced.py', '-v', '--tb=short'],
            'desc': '使用pytest运行高级示例'
        }
    ]
    
    # 询问用户是否要运行所有示例
    choice = input("\n是否运行所有示例？(y/n，默认y): ").strip().lower()
    if choice in ['n', 'no']:
        print("用户取消运行")
        return
    
    # 运行所有示例
    for i, example in enumerate(examples, 1):
        print(f"\n[{i}/{len(examples)}] {example['desc']}")
        
        # 检查文件是否存在
        if example['cmd'][0] == sys.executable and len(example['cmd']) > 1:
            file_path = Path(example['cmd'][1])
            if not file_path.exists():
                print(f"文件不存在: {file_path}")
                continue
        
        run_command(example['cmd'], example['desc'])
        
        # 询问是否继续
        if i < len(examples):
            continue_choice = input("按Enter继续下一个示例，输入'q'退出: ").strip().lower()
            if continue_choice == 'q':
                print("用户选择退出")
                break
    
    print("\n" + "="*60)
    print("所有示例运行完成！")
    print("\n学习建议:")
    print("1. 仔细阅读 tutorial.md 了解TDD理论")
    print("2. 研究 demo.py 中的完整TDD流程")
    print("3. 逐个运行 examples/ 目录下的示例")
    print("4. 尝试完成 exercises/ 目录下的练习")
    print("5. 使用 pytest 命令运行测试并查看覆盖率")
    print("="*60)

if __name__ == '__main__':
    main()