#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session23 项目演示：代码质量检查器

这是一个完整的代码质量检查工具，展示了如何：
1. 集成多种代码质量检查工具
2. 生成详细的质量报告
3. 提供代码改进建议
4. 支持配置文件和命令行参数
5. 实现良好的错误处理和日志记录

作者: Python教程团队
创建日期: 2024-01-01
"""

import argparse
import json
import logging
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union


@dataclass
class QualityResult:
    """
    代码质量检查结果
    """
    tool: str
    success: bool
    exit_code: int
    output: str
    errors: str
    execution_time: float
    issues_count: int = 0
    warnings_count: int = 0


@dataclass
class QualityReport:
    """
    代码质量报告
    """
    timestamp: str
    project_path: str
    total_files: int
    results: List[QualityResult] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)


class QualityCheckError(Exception):
    """代码质量检查错误"""
    pass


class CodeQualityChecker:
    """
    代码质量检查器
    
    集成多种代码质量检查工具，提供统一的检查接口和报告生成。
    """
    
    def __init__(self, project_path: str, config_file: Optional[str] = None) -> None:
        """
        初始化代码质量检查器
        
        Args:
            project_path: 项目路径
            config_file: 配置文件路径
        """
        self.project_path = Path(project_path).resolve()
        self.config_file = config_file
        self.config = self._load_config()
        self.logger = self._setup_logging()
        
        # 验证项目路径
        if not self.project_path.exists():
            raise QualityCheckError(f"项目路径不存在: {self.project_path}")
        
        # 支持的工具配置
        self.tools = {
            'ruff': {
                'command': ['ruff', 'check'],
                'args': ['--output-format=json'],
                'description': 'Ruff 代码检查',
                'enabled': True
            },
            'black': {
                'command': ['black', '--check', '--diff'],
                'args': [],
                'description': 'Black 代码格式检查',
                'enabled': True
            },
            'mypy': {
                'command': ['mypy'],
                'args': ['--show-error-codes', '--pretty'],
                'description': 'MyPy 类型检查',
                'enabled': True
            },
            'bandit': {
                'command': ['bandit', '-r'],
                'args': ['-f', 'json'],
                'description': 'Bandit 安全检查',
                'enabled': True
            }
        }
    
    def _load_config(self) -> Dict[str, Any]:
        """
        加载配置文件
        
        Returns:
            配置字典
        """
        if not self.config_file:
            return {}
        
        config_path = Path(self.config_file)
        if not config_path.exists():
            return {}
        
        try:
            with config_path.open('r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"警告: 无法加载配置文件 {self.config_file}: {e}")
            return {}
    
    def _setup_logging(self) -> logging.Logger:
        """
        设置日志记录
        
        Returns:
            配置好的日志记录器
        """
        logger = logging.getLogger('quality_checker')
        logger.setLevel(logging.INFO)
        
        # 避免重复添加处理器
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def check_tool_availability(self) -> Dict[str, bool]:
        """
        检查工具可用性
        
        Returns:
            工具可用性字典
        """
        availability = {}
        
        for tool_name, tool_config in self.tools.items():
            try:
                result = subprocess.run(
                    [tool_config['command'][0], '--version'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                availability[tool_name] = result.returncode == 0
                if result.returncode == 0:
                    self.logger.info(f"{tool_name} 可用")
                else:
                    self.logger.warning(f"{tool_name} 不可用")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                availability[tool_name] = False
                self.logger.warning(f"{tool_name} 未安装或不可用")
        
        return availability
    
    def run_tool(
        self,
        tool_name: str,
        target_path: Optional[str] = None
    ) -> QualityResult:
        """
        运行单个质量检查工具
        
        Args:
            tool_name: 工具名称
            target_path: 目标路径，默认为项目路径
            
        Returns:
            质量检查结果
        """
        if tool_name not in self.tools:
            raise QualityCheckError(f"不支持的工具: {tool_name}")
        
        tool_config = self.tools[tool_name]
        target = target_path or str(self.project_path)
        
        # 构建命令
        command = tool_config['command'] + tool_config['args'] + [target]
        
        self.logger.info(f"运行 {tool_name}: {' '.join(command)}")
        
        start_time = datetime.now()
        
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=300,  # 5分钟超时
                cwd=self.project_path
            )
            
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            # 解析结果
            issues_count, warnings_count = self._parse_tool_output(
                tool_name, result.stdout, result.stderr
            )
            
            return QualityResult(
                tool=tool_name,
                success=result.returncode == 0,
                exit_code=result.returncode,
                output=result.stdout,
                errors=result.stderr,
                execution_time=execution_time,
                issues_count=issues_count,
                warnings_count=warnings_count
            )
            
        except subprocess.TimeoutExpired:
            self.logger.error(f"{tool_name} 执行超时")
            return QualityResult(
                tool=tool_name,
                success=False,
                exit_code=-1,
                output="",
                errors="执行超时",
                execution_time=300.0
            )
        except Exception as e:
            self.logger.error(f"{tool_name} 执行失败: {e}")
            return QualityResult(
                tool=tool_name,
                success=False,
                exit_code=-1,
                output="",
                errors=str(e),
                execution_time=0.0
            )
    
    def _parse_tool_output(
        self,
        tool_name: str,
        stdout: str,
        stderr: str
    ) -> Tuple[int, int]:
        """
        解析工具输出，提取问题和警告数量
        
        Args:
            tool_name: 工具名称
            stdout: 标准输出
            stderr: 标准错误
            
        Returns:
            (问题数量, 警告数量)
        """
        issues_count = 0
        warnings_count = 0
        
        try:
            if tool_name == 'ruff' and stdout:
                # Ruff JSON 输出解析
                try:
                    data = json.loads(stdout)
                    issues_count = len(data)
                except json.JSONDecodeError:
                    # 如果不是JSON格式，尝试计数行数
                    issues_count = len([line for line in stdout.split('\n') if line.strip()])
            
            elif tool_name == 'bandit' and stdout:
                # Bandit JSON 输出解析
                try:
                    data = json.loads(stdout)
                    issues_count = len(data.get('results', []))
                except json.JSONDecodeError:
                    pass
            
            elif tool_name in ['mypy', 'black']:
                # 基于行数的简单计数
                if stdout:
                    lines = [line for line in stdout.split('\n') if line.strip()]
                    issues_count = len(lines)
                if stderr:
                    error_lines = [line for line in stderr.split('\n') if line.strip()]
                    warnings_count = len(error_lines)
        
        except Exception as e:
            self.logger.warning(f"解析 {tool_name} 输出时出错: {e}")
        
        return issues_count, warnings_count
    
    def run_all_checks(self, enabled_tools: Optional[List[str]] = None) -> QualityReport:
        """
        运行所有启用的质量检查
        
        Args:
            enabled_tools: 启用的工具列表，None表示使用默认配置
            
        Returns:
            质量检查报告
        """
        self.logger.info("开始代码质量检查")
        
        # 检查工具可用性
        availability = self.check_tool_availability()
        
        # 确定要运行的工具
        tools_to_run = enabled_tools or [
            name for name, config in self.tools.items()
            if config['enabled'] and availability.get(name, False)
        ]
        
        if not tools_to_run:
            raise QualityCheckError("没有可用的质量检查工具")
        
        # 统计项目文件
        total_files = self._count_python_files()
        
        # 创建报告
        report = QualityReport(
            timestamp=datetime.now().isoformat(),
            project_path=str(self.project_path),
            total_files=total_files
        )
        
        # 运行每个工具
        for tool_name in tools_to_run:
            self.logger.info(f"运行 {tool_name}...")
            result = self.run_tool(tool_name)
            report.results.append(result)
            
            if result.success:
                self.logger.info(f"{tool_name} 完成: {result.issues_count} 个问题")
            else:
                self.logger.error(f"{tool_name} 失败: {result.errors}")
        
        # 生成摘要和建议
        report.summary = self._generate_summary(report.results)
        report.recommendations = self._generate_recommendations(report.results)
        
        self.logger.info("代码质量检查完成")
        return report
    
    def _count_python_files(self) -> int:
        """
        统计Python文件数量
        
        Returns:
            Python文件数量
        """
        try:
            return len(list(self.project_path.rglob('*.py')))
        except Exception:
            return 0
    
    def _generate_summary(self, results: List[QualityResult]) -> Dict[str, Any]:
        """
        生成检查摘要
        
        Args:
            results: 检查结果列表
            
        Returns:
            摘要字典
        """
        total_issues = sum(r.issues_count for r in results)
        total_warnings = sum(r.warnings_count for r in results)
        successful_tools = sum(1 for r in results if r.success)
        total_time = sum(r.execution_time for r in results)
        
        return {
            'total_tools': len(results),
            'successful_tools': successful_tools,
            'failed_tools': len(results) - successful_tools,
            'total_issues': total_issues,
            'total_warnings': total_warnings,
            'total_execution_time': round(total_time, 2),
            'overall_success': successful_tools == len(results) and total_issues == 0
        }
    
    def _generate_recommendations(self, results: List[QualityResult]) -> List[str]:
        """
        生成改进建议
        
        Args:
            results: 检查结果列表
            
        Returns:
            建议列表
        """
        recommendations = []
        
        for result in results:
            if not result.success:
                recommendations.append(
                    f"修复 {result.tool} 工具的执行问题: {result.errors}"
                )
            elif result.issues_count > 0:
                recommendations.append(
                    f"解决 {result.tool} 检测到的 {result.issues_count} 个问题"
                )
        
        # 通用建议
        total_issues = sum(r.issues_count for r in results)
        if total_issues > 0:
            recommendations.extend([
                "定期运行代码质量检查",
                "在CI/CD流程中集成质量检查",
                "使用pre-commit钩子自动检查代码",
                "团队制定统一的代码规范"
            ])
        else:
            recommendations.append("代码质量良好，继续保持！")
        
        return recommendations
    
    def save_report(self, report: QualityReport, output_file: str) -> None:
        """
        保存质量报告到文件
        
        Args:
            report: 质量报告
            output_file: 输出文件路径
        """
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 转换为可序列化的格式
        report_dict = {
            'timestamp': report.timestamp,
            'project_path': report.project_path,
            'total_files': report.total_files,
            'summary': report.summary,
            'recommendations': report.recommendations,
            'results': [
                {
                    'tool': r.tool,
                    'success': r.success,
                    'exit_code': r.exit_code,
                    'output': r.output,
                    'errors': r.errors,
                    'execution_time': r.execution_time,
                    'issues_count': r.issues_count,
                    'warnings_count': r.warnings_count
                }
                for r in report.results
            ]
        }
        
        try:
            with output_path.open('w', encoding='utf-8') as f:
                json.dump(report_dict, f, indent=2, ensure_ascii=False)
            self.logger.info(f"报告已保存到: {output_file}")
        except OSError as e:
            raise QualityCheckError(f"保存报告失败: {e}") from e
    
    def print_report(self, report: QualityReport) -> None:
        """
        打印质量报告到控制台
        
        Args:
            report: 质量报告
        """
        print("\n" + "=" * 60)
        print("代码质量检查报告")
        print("=" * 60)
        
        print(f"\n项目路径: {report.project_path}")
        print(f"检查时间: {report.timestamp}")
        print(f"Python文件数: {report.total_files}")
        
        print("\n摘要:")
        print("-" * 30)
        for key, value in report.summary.items():
            print(f"{key}: {value}")
        
        print("\n工具检查结果:")
        print("-" * 30)
        for result in report.results:
            status = "✓" if result.success else "✗"
            print(f"{status} {result.tool}: {result.issues_count} 问题, "
                  f"{result.warnings_count} 警告 ({result.execution_time:.2f}s)")
        
        if report.recommendations:
            print("\n改进建议:")
            print("-" * 30)
            for i, rec in enumerate(report.recommendations, 1):
                print(f"{i}. {rec}")
        
        print("\n" + "=" * 60)


def create_sample_config() -> Dict[str, Any]:
    """
    创建示例配置文件
    
    Returns:
        示例配置字典
    """
    return {
        "tools": {
            "ruff": {
                "enabled": True,
                "args": ["--select=E,W,F,I,N"]
            },
            "black": {
                "enabled": True,
                "args": ["--line-length=88"]
            },
            "mypy": {
                "enabled": True,
                "args": ["--strict"]
            },
            "bandit": {
                "enabled": True,
                "args": ["--skip=B101"]
            }
        },
        "output": {
            "format": "json",
            "file": "quality_report.json"
        }
    }


def main() -> None:
    """
    主函数：命令行接口
    """
    parser = argparse.ArgumentParser(
        description="代码质量检查器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s .                          # 检查当前目录
  %(prog)s /path/to/project           # 检查指定项目
  %(prog)s . --tools ruff black       # 只运行指定工具
  %(prog)s . --config config.json    # 使用配置文件
  %(prog)s . --output report.json    # 保存报告到文件
        """
    )
    
    parser.add_argument(
        'project_path',
        help='项目路径'
    )
    parser.add_argument(
        '--config',
        help='配置文件路径'
    )
    parser.add_argument(
        '--tools',
        nargs='+',
        choices=['ruff', 'black', 'mypy', 'bandit'],
        help='要运行的工具列表'
    )
    parser.add_argument(
        '--output',
        help='输出报告文件路径'
    )
    parser.add_argument(
        '--create-config',
        action='store_true',
        help='创建示例配置文件'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='详细输出'
    )
    
    args = parser.parse_args()
    
    # 创建配置文件
    if args.create_config:
        config = create_sample_config()
        config_file = 'quality_config.json'
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"示例配置文件已创建: {config_file}")
        return
    
    try:
        # 创建检查器
        checker = CodeQualityChecker(args.project_path, args.config)
        
        # 设置日志级别
        if args.verbose:
            checker.logger.setLevel(logging.DEBUG)
        
        # 运行检查
        report = checker.run_all_checks(args.tools)
        
        # 输出报告
        checker.print_report(report)
        
        # 保存报告
        if args.output:
            checker.save_report(report, args.output)
        
        # 根据结果设置退出码
        if not report.summary['overall_success']:
            sys.exit(1)
    
    except QualityCheckError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n检查被用户中断", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"未预期的错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()