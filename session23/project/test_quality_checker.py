#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session23 项目测试：代码质量检查器测试

这个文件包含了对代码质量检查器的基本测试，
验证其核心功能是否正常工作。

运行测试:
    python test_quality_checker.py

作者: Python教程团队
创建日期: 2024-01-01
"""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from quality_checker import CodeQualityChecker, QualityCheckError, QualityResult


class TestCodeQualityChecker(unittest.TestCase):
    """
    代码质量检查器测试类
    """
    
    def setUp(self) -> None:
        """
        测试前的设置
        """
        # 创建临时目录作为测试项目
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)
        
        # 创建一些测试文件
        self._create_test_files()
        
        # 创建检查器实例
        self.checker = CodeQualityChecker(str(self.project_path))
    
    def tearDown(self) -> None:
        """
        测试后的清理
        """
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def _create_test_files(self) -> None:
        """
        创建测试用的Python文件
        """
        # 创建一个简单的Python文件
        test_file = self.project_path / "test_module.py"
        test_file.write_text(
            '#!/usr/bin/env python3\n'
            '"""测试模块"""\n'
            '\n'
            'def hello_world() -> str:\n'
            '    """返回问候语"""\n'
            '    return "Hello, World!"\n'
            '\n'
            'if __name__ == "__main__":\n'
            '    print(hello_world())\n',
            encoding='utf-8'
        )
        
        # 创建一个有问题的Python文件
        problem_file = self.project_path / "problem_module.py"
        problem_file.write_text(
            '# 这个文件包含一些代码质量问题\n'
            'import os,sys\n'  # 导入格式问题
            '\n'
            'def bad_function(x,y,z):\n'  # 缺少类型注解和空格
            '    if x>0:\n'  # 缺少空格
            '        return x+y+z\n'  # 缺少空格
            '    else:\n'
            '        return 0\n',
            encoding='utf-8'
        )
    
    def test_initialization(self) -> None:
        """
        测试检查器初始化
        """
        self.assertEqual(self.checker.project_path, self.project_path)
        self.assertIsInstance(self.checker.tools, dict)
        self.assertIn('ruff', self.checker.tools)
        self.assertIn('black', self.checker.tools)
        self.assertIn('mypy', self.checker.tools)
        self.assertIn('bandit', self.checker.tools)
    
    def test_invalid_project_path(self) -> None:
        """
        测试无效项目路径
        """
        with self.assertRaises(QualityCheckError):
            CodeQualityChecker("/nonexistent/path")
    
    def test_count_python_files(self) -> None:
        """
        测试Python文件计数
        """
        count = self.checker._count_python_files()
        self.assertEqual(count, 2)  # 我们创建了2个Python文件
    
    def test_parse_tool_output(self) -> None:
        """
        测试工具输出解析
        """
        # 测试Ruff JSON输出解析
        ruff_output = '[{"code": "E302", "message": "expected 2 blank lines"}]'
        issues, warnings = self.checker._parse_tool_output('ruff', ruff_output, '')
        self.assertEqual(issues, 1)
        self.assertEqual(warnings, 0)
        
        # 测试Bandit JSON输出解析
        bandit_output = '{"results": [{"issue_severity": "HIGH"}]}'
        issues, warnings = self.checker._parse_tool_output('bandit', bandit_output, '')
        self.assertEqual(issues, 1)
        
        # 测试MyPy输出解析
        mypy_output = 'file.py:1: error: Missing type annotation\nfile.py:2: warning: Unused import'
        issues, warnings = self.checker._parse_tool_output('mypy', mypy_output, '')
        self.assertEqual(issues, 2)
    
    @patch('subprocess.run')
    def test_run_tool_success(self, mock_run: Mock) -> None:
        """
        测试成功运行工具
        """
        # 模拟成功的工具执行
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = '[]'  # 空的JSON数组，表示没有问题
        mock_result.stderr = ''
        mock_run.return_value = mock_result
        
        result = self.checker.run_tool('ruff')
        
        self.assertIsInstance(result, QualityResult)
        self.assertEqual(result.tool, 'ruff')
        self.assertTrue(result.success)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.issues_count, 0)
    
    @patch('subprocess.run')
    def test_run_tool_failure(self, mock_run: Mock) -> None:
        """
        测试工具执行失败
        """
        # 模拟失败的工具执行
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = '[{"code": "E302"}]'  # 有问题的输出
        mock_result.stderr = ''
        mock_run.return_value = mock_result
        
        result = self.checker.run_tool('ruff')
        
        self.assertIsInstance(result, QualityResult)
        self.assertEqual(result.tool, 'ruff')
        self.assertFalse(result.success)  # 因为exit_code != 0
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(result.issues_count, 1)
    
    @patch('subprocess.run')
    def test_check_tool_availability(self, mock_run: Mock) -> None:
        """
        测试工具可用性检查
        """
        # 模拟工具可用
        mock_result = Mock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        availability = self.checker.check_tool_availability()
        
        self.assertIsInstance(availability, dict)
        # 所有工具都应该被检查
        for tool_name in self.checker.tools.keys():
            self.assertIn(tool_name, availability)
    
    def test_generate_summary(self) -> None:
        """
        测试摘要生成
        """
        # 创建测试结果
        results = [
            QualityResult(
                tool='ruff',
                success=True,
                exit_code=1,  # 有问题但执行成功
                output='',
                errors='',
                execution_time=1.0,
                issues_count=5,
                warnings_count=2
            ),
            QualityResult(
                tool='black',
                success=False,
                exit_code=1,
                output='',
                errors='Tool failed',
                execution_time=0.5,
                issues_count=0,
                warnings_count=0
            )
        ]
        
        summary = self.checker._generate_summary(results)
        
        self.assertEqual(summary['total_tools'], 2)
        self.assertEqual(summary['successful_tools'], 1)
        self.assertEqual(summary['failed_tools'], 1)
        self.assertEqual(summary['total_issues'], 5)
        self.assertEqual(summary['total_warnings'], 2)
        self.assertEqual(summary['total_execution_time'], 1.5)
        self.assertFalse(summary['overall_success'])
    
    def test_generate_recommendations(self) -> None:
        """
        测试建议生成
        """
        # 创建测试结果
        results = [
            QualityResult(
                tool='ruff',
                success=True,
                exit_code=1,
                output='',
                errors='',
                execution_time=1.0,
                issues_count=3,
                warnings_count=0
            ),
            QualityResult(
                tool='black',
                success=False,
                exit_code=1,
                output='',
                errors='Tool execution failed',
                execution_time=0.5,
                issues_count=0,
                warnings_count=0
            )
        ]
        
        recommendations = self.checker._generate_recommendations(results)
        
        self.assertIsInstance(recommendations, list)
        self.assertTrue(len(recommendations) > 0)
        
        # 检查是否包含预期的建议
        rec_text = ' '.join(recommendations)
        self.assertIn('ruff', rec_text)
        self.assertIn('black', rec_text)
    
    def test_save_and_load_report(self) -> None:
        """
        测试报告保存和加载
        """
        from quality_checker import QualityReport
        
        # 创建测试报告
        report = QualityReport(
            timestamp='2024-01-01T12:00:00',
            project_path=str(self.project_path),
            total_files=2
        )
        
        report.results = [
            QualityResult(
                tool='ruff',
                success=True,
                exit_code=0,
                output='',
                errors='',
                execution_time=1.0,
                issues_count=0,
                warnings_count=0
            )
        ]
        
        report.summary = {'total_issues': 0}
        report.recommendations = ['Keep up the good work!']
        
        # 保存报告
        report_file = self.project_path / 'test_report.json'
        self.checker.save_report(report, str(report_file))
        
        # 验证文件存在
        self.assertTrue(report_file.exists())
        
        # 验证文件内容
        with report_file.open('r', encoding='utf-8') as f:
            saved_data = json.load(f)
        
        self.assertEqual(saved_data['timestamp'], report.timestamp)
        self.assertEqual(saved_data['project_path'], report.project_path)
        self.assertEqual(saved_data['total_files'], report.total_files)
        self.assertEqual(len(saved_data['results']), 1)
    
    def test_config_loading(self) -> None:
        """
        测试配置文件加载
        """
        # 创建测试配置文件
        config_file = self.project_path / 'test_config.json'
        config_data = {
            'tools': {
                'ruff': {'enabled': True},
                'black': {'enabled': False}
            }
        }
        
        with config_file.open('w', encoding='utf-8') as f:
            json.dump(config_data, f)
        
        # 创建带配置的检查器
        checker_with_config = CodeQualityChecker(
            str(self.project_path),
            str(config_file)
        )
        
        self.assertEqual(checker_with_config.config, config_data)


def run_integration_test() -> None:
    """
    运行集成测试
    
    这个函数测试整个工具链是否正常工作
    """
    print("运行集成测试...")
    
    try:
        # 创建临时项目
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            
            # 创建测试文件
            test_file = project_path / "integration_test.py"
            test_file.write_text(
                '#!/usr/bin/env python3\n'
                '"""集成测试文件"""\n'
                '\n'
                'def add_numbers(a: int, b: int) -> int:\n'
                '    """添加两个数字"""\n'
                '    return a + b\n'
                '\n'
                'if __name__ == "__main__":\n'
                '    result = add_numbers(1, 2)\n'
                '    print(f"结果: {result}")\n',
                encoding='utf-8'
            )
            
            # 创建检查器并运行
            checker = CodeQualityChecker(str(project_path))
            
            # 检查工具可用性
            availability = checker.check_tool_availability()
            available_tools = [name for name, available in availability.items() if available]
            
            if not available_tools:
                print("警告: 没有可用的代码质量工具")
                return
            
            print(f"可用工具: {', '.join(available_tools)}")
            
            # 运行检查
            report = checker.run_all_checks(available_tools)
            
            # 显示结果
            print(f"检查完成: {report.summary['total_issues']} 个问题")
            print("集成测试通过!")
            
    except Exception as e:
        print(f"集成测试失败: {e}")
        raise


def main() -> None:
    """
    主函数：运行所有测试
    """
    print("Session23 代码质量检查器测试")
    print("=" * 50)
    
    # 运行单元测试
    print("\n运行单元测试...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # 运行集成测试
    print("\n运行集成测试...")
    try:
        run_integration_test()
    except Exception as e:
        print(f"集成测试失败: {e}")
        return
    
    print("\n所有测试完成!")


if __name__ == '__main__':
    main()