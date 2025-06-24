#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session23: 代码质量与规范 - 演示代码

本文件演示了代码质量检查工具的基本用法和实际应用。
包括PEP 8规范检查、代码格式化、静态分析等功能。

作者: Python教程团队
创建日期: 2024-01-01
最后修改: 2024-01-01
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class CodeQualityChecker:
    """
    代码质量检查工具类
    
    提供多种代码质量检查功能，包括：
    - PEP 8规范检查
    - 代码格式化
    - 静态类型检查
    - 安全漏洞检查
    """
    
    def __init__(self, project_path: str = "."):
        """
        初始化代码质量检查器
        
        Args:
            project_path: 项目路径，默认为当前目录
        """
        self.project_path = Path(project_path)
        self.tools = {
            'ruff': 'ruff check',
            'black': 'black --check',
            'mypy': 'mypy',
            'bandit': 'bandit -r'
        }
        self.results: Dict[str, Dict] = {}
    
    def check_tool_availability(self) -> Dict[str, bool]:
        """
        检查代码质量工具是否已安装
        
        Returns:
            工具可用性字典
        """
        availability = {}
        
        for tool_name in self.tools.keys():
            try:
                result = subprocess.run(
                    [tool_name, '--version'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                availability[tool_name] = result.returncode == 0
            except (subprocess.TimeoutExpired, FileNotFoundError):
                availability[tool_name] = False
        
        return availability
    
    def run_ruff_check(self, fix: bool = False) -> Tuple[bool, str]:
        """
        运行ruff代码检查
        
        Args:
            fix: 是否自动修复问题
        
        Returns:
            (是否成功, 输出信息)
        """
        cmd = ['ruff', 'check', str(self.project_path)]
        if fix:
            cmd.append('--fix')
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            success = result.returncode == 0
            output = result.stdout + result.stderr
            
            self.results['ruff'] = {
                'success': success,
                'output': output,
                'issues_count': len([line for line in output.split('\n') 
                                   if line.strip() and ':' in line])
            }
            
            return success, output
            
        except subprocess.TimeoutExpired:
            return False, "Ruff检查超时"
        except FileNotFoundError:
            return False, "Ruff未安装"
    
    def run_black_format(self, check_only: bool = True) -> Tuple[bool, str]:
        """
        运行black代码格式化
        
        Args:
            check_only: 是否只检查不修改
        
        Returns:
            (是否成功, 输出信息)
        """
        cmd = ['black']
        if check_only:
            cmd.append('--check')
        cmd.append(str(self.project_path))
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            success = result.returncode == 0
            output = result.stdout + result.stderr
            
            self.results['black'] = {
                'success': success,
                'output': output,
                'formatted_files': len([line for line in output.split('\n') 
                                      if 'reformatted' in line])
            }
            
            return success, output
            
        except subprocess.TimeoutExpired:
            return False, "Black格式化超时"
        except FileNotFoundError:
            return False, "Black未安装"
    
    def run_mypy_check(self) -> Tuple[bool, str]:
        """
        运行mypy静态类型检查
        
        Returns:
            (是否成功, 输出信息)
        """
        cmd = ['mypy', str(self.project_path)]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            success = result.returncode == 0
            output = result.stdout + result.stderr
            
            self.results['mypy'] = {
                'success': success,
                'output': output,
                'error_count': len([line for line in output.split('\n') 
                                  if 'error:' in line])
            }
            
            return success, output
            
        except subprocess.TimeoutExpired:
            return False, "Mypy检查超时"
        except FileNotFoundError:
            return False, "Mypy未安装"
    
    def analyze_code_file(self, file_path: str) -> Dict[str, any]:
        """
        分析单个代码文件的质量指标
        
        Args:
            file_path: 文件路径
        
        Returns:
            分析结果字典
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            analysis = {
                'file_path': file_path,
                'total_lines': len(lines),
                'code_lines': len([line for line in lines 
                                 if line.strip() and not line.strip().startswith('#')]),
                'comment_lines': len([line for line in lines 
                                    if line.strip().startswith('#')]),
                'blank_lines': len([line for line in lines if not line.strip()]),
                'long_lines': len([line for line in lines if len(line) > 79]),
                'has_docstring': '"""' in content or "'''" in content,
                'imports_count': len([line for line in lines 
                                    if line.strip().startswith(('import ', 'from '))])
            }
            
            # 计算代码质量评分
            score = self._calculate_quality_score(analysis)
            analysis['quality_score'] = score
            
            return analysis
            
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_quality_score(self, analysis: Dict) -> float:
        """
        计算代码质量评分
        
        Args:
            analysis: 代码分析结果
        
        Returns:
            质量评分 (0-100)
        """
        score = 100.0
        
        # 长行扣分
        if analysis['total_lines'] > 0:
            long_line_ratio = analysis['long_lines'] / analysis['total_lines']
            score -= long_line_ratio * 20
        
        # 注释比例加分
        if analysis['code_lines'] > 0:
            comment_ratio = analysis['comment_lines'] / analysis['code_lines']
            score += min(comment_ratio * 10, 10)
        
        # 有文档字符串加分
        if analysis['has_docstring']:
            score += 5
        
        return max(0, min(100, score))
    
    def generate_quality_report(self) -> str:
        """
        生成代码质量报告
        
        Returns:
            格式化的报告字符串
        """
        report = []
        report.append("=" * 60)
        report.append("代码质量检查报告")
        report.append("=" * 60)
        report.append(f"项目路径: {self.project_path}")
        report.append("")
        
        # 工具可用性
        availability = self.check_tool_availability()
        report.append("工具可用性:")
        for tool, available in availability.items():
            status = "✓" if available else "✗"
            report.append(f"  {status} {tool}")
        report.append("")
        
        # 检查结果
        if self.results:
            report.append("检查结果:")
            for tool, result in self.results.items():
                status = "通过" if result['success'] else "失败"
                report.append(f"  {tool}: {status}")
                
                if 'issues_count' in result:
                    report.append(f"    问题数量: {result['issues_count']}")
                if 'error_count' in result:
                    report.append(f"    错误数量: {result['error_count']}")
                if 'formatted_files' in result:
                    report.append(f"    需格式化文件: {result['formatted_files']}")
            report.append("")
        
        # 建议
        report.append("改进建议:")
        report.append("  1. 定期运行代码质量检查")
        report.append("  2. 使用pre-commit钩子自动检查")
        report.append("  3. 在CI/CD中集成代码质量检查")
        report.append("  4. 团队制定统一的代码规范")
        
        return "\n".join(report)
    
    def run_full_check(self) -> None:
        """
        运行完整的代码质量检查
        """
        print("开始代码质量检查...")
        print("=" * 50)
        
        # 检查工具可用性
        availability = self.check_tool_availability()
        
        # 运行ruff检查
        if availability.get('ruff', False):
            print("\n1. 运行Ruff检查...")
            success, output = self.run_ruff_check()
            if success:
                print("   ✓ Ruff检查通过")
            else:
                print("   ✗ Ruff检查发现问题:")
                print(f"   {output[:200]}..." if len(output) > 200 else f"   {output}")
        
        # 运行black检查
        if availability.get('black', False):
            print("\n2. 运行Black格式检查...")
            success, output = self.run_black_format()
            if success:
                print("   ✓ 代码格式符合规范")
            else:
                print("   ✗ 代码格式需要调整")
        
        # 运行mypy检查
        if availability.get('mypy', False):
            print("\n3. 运行Mypy类型检查...")
            success, output = self.run_mypy_check()
            if success:
                print("   ✓ 类型检查通过")
            else:
                print("   ✗ 发现类型问题")
        
        print("\n" + "=" * 50)
        print("检查完成！")


def demonstrate_pep8_examples():
    """
    演示PEP 8规范的正确和错误示例
    """
    print("\nPEP 8规范演示")
    print("=" * 30)
    
    # 正确的命名示例
    user_name = "Alice"  # 变量使用snake_case
    MAX_RETRY_COUNT = 3  # 常量使用UPPER_CASE
    
    class UserManager:  # 类名使用PascalCase
        def get_user_info(self):  # 方法使用snake_case
            return {"name": user_name}
    
    # 正确的函数定义
    def calculate_total_price(items: List[Dict[str, float]]) -> float:
        """
        计算商品总价
        
        Args:
            items: 商品列表，每个商品包含价格信息
        
        Returns:
            总价格
        """
        total = 0.0
        for item in items:
            total += item.get('price', 0.0)
        return total
    
    # 演示正确的空格使用
    result = 10 + 20  # 运算符周围有空格
    items = [{'price': 10.0}, {'price': 20.0}]  # 正确的列表格式
    
    print(f"用户名: {user_name}")
    print(f"最大重试次数: {MAX_RETRY_COUNT}")
    print(f"商品总价: {calculate_total_price(items)}")


def demonstrate_code_analysis():
    """
    演示代码分析功能
    """
    print("\n代码分析演示")
    print("=" * 30)
    
    checker = CodeQualityChecker()
    
    # 分析当前文件
    current_file = __file__
    analysis = checker.analyze_code_file(current_file)
    
    if 'error' not in analysis:
        print(f"文件: {os.path.basename(current_file)}")
        print(f"总行数: {analysis['total_lines']}")
        print(f"代码行数: {analysis['code_lines']}")
        print(f"注释行数: {analysis['comment_lines']}")
        print(f"空白行数: {analysis['blank_lines']}")
        print(f"长行数量: {analysis['long_lines']}")
        print(f"包含文档字符串: {analysis['has_docstring']}")
        print(f"导入语句数量: {analysis['imports_count']}")
        print(f"质量评分: {analysis['quality_score']:.1f}/100")
    else:
        print(f"分析出错: {analysis['error']}")


def main():
    """
    主函数：演示代码质量检查工具的使用
    """
    print("Session23: 代码质量与规范演示")
    print("=" * 40)
    
    # 演示PEP 8规范
    demonstrate_pep8_examples()
    
    # 演示代码分析
    demonstrate_code_analysis()
    
    # 创建代码质量检查器
    print("\n代码质量检查工具演示")
    print("=" * 30)
    
    checker = CodeQualityChecker()
    
    # 检查工具可用性
    availability = checker.check_tool_availability()
    print("\n可用的代码质量工具:")
    for tool, available in availability.items():
        status = "✓ 已安装" if available else "✗ 未安装"
        print(f"  {tool}: {status}")
    
    # 如果有可用工具，运行检查
    if any(availability.values()):
        print("\n提示: 可以运行 checker.run_full_check() 进行完整检查")
        print("注意: 需要先安装相应的工具 (pip install ruff black mypy bandit)")
    else:
        print("\n建议安装代码质量工具:")
        print("  pip install ruff black mypy bandit")
    
    # 生成示例报告
    print("\n" + checker.generate_quality_report())
    
    print("\n演示完成！")
    print("\n学习要点:")
    print("1. 遵循PEP 8编码规范")
    print("2. 使用自动化工具检查代码质量")
    print("3. 定期进行代码审查")
    print("4. 将质量检查集成到开发流程中")


if __name__ == "__main__":
    main()