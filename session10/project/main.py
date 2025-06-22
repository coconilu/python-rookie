#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session10 项目：Python模块管理系统 - 主程序

这是一个综合性的Python项目，演示模块与包的实际应用。
主要功能包括文件分析、数据处理和报告生成。

作者：Python学习教程
版本：1.0.0
"""

import sys
import os
import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 导入项目配置
from config import (
    ANALYSIS_CONFIG,
    REPORT_CONFIG,
    PROCESSING_CONFIG,
    DEFAULT_CONFIG_FILE
)

# 导入自定义模块
try:
    from modules import file_analyzer, data_processor, report_generator
    from modules.utils import math_tools, string_tools, file_tools
except ImportError as e:
    print(f"模块导入错误: {e}")
    print("请确保所有必要的模块文件都已创建")
    sys.exit(1)


class ModuleManagementSystem:
    """
    模块管理系统主类
    
    整合文件分析、数据处理和报告生成功能，
    演示模块间的协作和包的使用。
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        初始化模块管理系统
        
        Args:
            config_file: 配置文件路径
        """
        self.config = self._load_config(config_file)
        self.file_analyzer = file_analyzer.FileAnalyzer(self.config.get('analysis', {}))
        self.data_processor = data_processor.DataProcessor(self.config.get('processing', {}))
        self.report_generator = report_generator.ReportGenerator(self.config.get('report', {}))
        
        # 创建输出目录
        self._ensure_output_directories()
    
    def _load_config(self, config_file: Optional[str]) -> Dict:
        """
        加载配置文件
        
        Args:
            config_file: 配置文件路径
            
        Returns:
            配置字典
        """
        # 默认配置
        config = {
            'analysis': ANALYSIS_CONFIG,
            'processing': PROCESSING_CONFIG,
            'report': REPORT_CONFIG
        }
        
        # 加载JSON配置文件
        if config_file:
            config_path = Path(config_file)
        else:
            config_path = project_root / DEFAULT_CONFIG_FILE
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                    # 合并配置
                    for key, value in file_config.items():
                        if key in config:
                            config[key].update(value)
                        else:
                            config[key] = value
                print(f"已加载配置文件: {config_path}")
            except Exception as e:
                print(f"配置文件加载失败: {e}，使用默认配置")
        
        return config
    
    def _ensure_output_directories(self):
        """
        确保输出目录存在
        """
        output_dir = Path(self.config['report']['output_dir'])
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建子目录
        (output_dir / 'reports').mkdir(exist_ok=True)
        (output_dir / 'data').mkdir(exist_ok=True)
        (output_dir / 'charts').mkdir(exist_ok=True)
    
    def analyze_directory(self, directory: str) -> Dict:
        """
        分析指定目录
        
        Args:
            directory: 要分析的目录路径
            
        Returns:
            分析结果字典
        """
        print(f"\n=== 开始分析目录: {directory} ===")
        
        # 验证目录存在
        dir_path = Path(directory)
        if not dir_path.exists():
            raise FileNotFoundError(f"目录不存在: {directory}")
        
        if not dir_path.is_dir():
            raise ValueError(f"路径不是目录: {directory}")
        
        # 执行文件分析
        analysis_results = self.file_analyzer.analyze_directory(directory)
        
        # 处理分析数据
        processed_data = self.data_processor.process_analysis_results(analysis_results)
        
        # 生成统计信息
        statistics = self.data_processor.calculate_statistics(processed_data)
        
        # 合并结果
        results = {
            'directory': directory,
            'analysis': analysis_results,
            'processed_data': processed_data,
            'statistics': statistics,
            'timestamp': file_tools.get_current_timestamp()
        }
        
        print(f"分析完成，共处理 {len(analysis_results.get('files', []))} 个文件")
        return results
    
    def process_data_file(self, file_path: str) -> Dict:
        """
        处理数据文件
        
        Args:
            file_path: 数据文件路径
            
        Returns:
            处理结果字典
        """
        print(f"\n=== 开始处理数据文件: {file_path} ===")
        
        # 验证文件存在
        if not Path(file_path).exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        # 根据文件类型选择处理方法
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.csv':
            data = self.data_processor.load_csv(file_path)
        elif file_ext == '.json':
            data = self.data_processor.load_json(file_path)
        elif file_ext == '.txt':
            data = self.data_processor.load_text(file_path)
        else:
            raise ValueError(f"不支持的文件类型: {file_ext}")
        
        # 数据清洗和处理
        cleaned_data = self.data_processor.clean_data(data)
        
        # 生成统计信息
        statistics = self.data_processor.calculate_statistics(cleaned_data)
        
        results = {
            'file_path': file_path,
            'file_type': file_ext,
            'raw_data': data,
            'cleaned_data': cleaned_data,
            'statistics': statistics,
            'timestamp': file_tools.get_current_timestamp()
        }
        
        print(f"数据处理完成，共处理 {len(cleaned_data)} 条记录")
        return results
    
    def generate_report(self, results: Dict, output_file: str, format_type: str = 'html') -> str:
        """
        生成分析报告
        
        Args:
            results: 分析结果
            output_file: 输出文件名
            format_type: 报告格式 ('html', 'markdown', 'json')
            
        Returns:
            生成的报告文件路径
        """
        print(f"\n=== 开始生成 {format_type.upper()} 报告 ===")
        
        # 确定输出路径
        output_dir = Path(self.config['report']['output_dir']) / 'reports'
        output_path = output_dir / output_file
        
        # 根据格式生成报告
        if format_type.lower() == 'html':
            report_path = self.report_generator.create_html_report(results, str(output_path))
        elif format_type.lower() == 'markdown':
            report_path = self.report_generator.create_markdown_report(results, str(output_path))
        elif format_type.lower() == 'json':
            report_path = self.report_generator.create_json_report(results, str(output_path))
        else:
            raise ValueError(f"不支持的报告格式: {format_type}")
        
        print(f"报告已生成: {report_path}")
        return report_path
    
    def run_full_analysis(self, directory: str, output_prefix: str = 'analysis') -> Dict[str, str]:
        """
        运行完整的分析流程
        
        Args:
            directory: 要分析的目录
            output_prefix: 输出文件前缀
            
        Returns:
            生成的报告文件路径字典
        """
        print(f"\n{'='*60}")
        print(f"开始完整分析流程: {directory}")
        print(f"{'='*60}")
        
        # 1. 分析目录
        results = self.analyze_directory(directory)
        
        # 2. 生成多种格式的报告
        reports = {}
        
        # HTML报告
        html_file = f"{output_prefix}.html"
        reports['html'] = self.generate_report(results, html_file, 'html')
        
        # Markdown报告
        md_file = f"{output_prefix}.md"
        reports['markdown'] = self.generate_report(results, md_file, 'markdown')
        
        # JSON数据
        json_file = f"{output_prefix}.json"
        reports['json'] = self.generate_report(results, json_file, 'json')
        
        # 3. 显示摘要信息
        self._display_summary(results)
        
        print(f"\n{'='*60}")
        print("分析完成！生成的报告文件:")
        for format_type, path in reports.items():
            print(f"  {format_type.upper()}: {path}")
        print(f"{'='*60}")
        
        return reports
    
    def _display_summary(self, results: Dict):
        """
        显示分析摘要
        
        Args:
            results: 分析结果
        """
        stats = results.get('statistics', {})
        
        print(f"\n=== 分析摘要 ===")
        print(f"分析目录: {results.get('directory', 'N/A')}")
        print(f"分析时间: {results.get('timestamp', 'N/A')}")
        
        if 'file_count' in stats:
            print(f"文件总数: {stats['file_count']}")
        
        if 'total_size' in stats:
            size_mb = stats['total_size'] / (1024 * 1024)
            print(f"总大小: {size_mb:.2f} MB")
        
        if 'file_types' in stats:
            print(f"文件类型: {len(stats['file_types'])} 种")
            for ext, count in list(stats['file_types'].items())[:5]:
                print(f"  {ext}: {count} 个")
        
        if 'largest_files' in stats:
            print("最大文件:")
            for file_info in stats['largest_files'][:3]:
                size_kb = file_info['size'] / 1024
                print(f"  {file_info['name']}: {size_kb:.1f} KB")
    
    def demonstrate_modules(self):
        """
        演示各个模块的功能
        """
        print(f"\n{'='*60}")
        print("模块功能演示")
        print(f"{'='*60}")
        
        # 演示工具模块
        print("\n=== 工具模块演示 ===")
        
        # 数学工具
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        mean = math_tools.calculate_mean(numbers)
        std_dev = math_tools.calculate_std_deviation(numbers)
        print(f"数学工具 - 平均值: {mean:.2f}, 标准差: {std_dev:.2f}")
        
        # 字符串工具
        text = "Hello, Python Modules!"
        formatted = string_tools.format_title(text)
        word_count = string_tools.count_words(text)
        print(f"字符串工具 - 格式化: '{formatted}', 单词数: {word_count}")
        
        # 文件工具
        current_time = file_tools.get_current_timestamp()
        temp_file = file_tools.get_temp_filename('demo', '.txt')
        print(f"文件工具 - 当前时间: {current_time}, 临时文件: {temp_file}")
        
        # 演示模块集成
        print("\n=== 模块集成演示 ===")
        
        # 创建示例数据
        sample_data = {
            'numbers': [1, 2, 3, 4, 5],
            'texts': ['hello', 'world', 'python'],
            'files': ['test1.py', 'test2.txt', 'test3.md']
        }
        
        # 处理数据
        processed = self.data_processor.process_sample_data(sample_data)
        print(f"数据处理结果: {processed}")
        
        print(f"\n{'='*60}")
        print("模块演示完成")
        print(f"{'='*60}")


def create_argument_parser() -> argparse.ArgumentParser:
    """
    创建命令行参数解析器
    
    Returns:
        配置好的参数解析器
    """
    parser = argparse.ArgumentParser(
        description='Python模块管理系统 - Session10项目',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python main.py --demo                          # 运行模块演示
  python main.py --directory ./src              # 分析src目录
  python main.py --data data/sample.csv         # 处理CSV数据
  python main.py --directory ./src --format html --output analysis.html
        """
    )
    
    # 主要操作选项
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--demo',
        action='store_true',
        help='运行模块功能演示'
    )
    group.add_argument(
        '--directory', '-d',
        type=str,
        help='要分析的目录路径'
    )
    group.add_argument(
        '--data',
        type=str,
        help='要处理的数据文件路径'
    )
    
    # 输出选项
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='analysis',
        help='输出文件名前缀 (默认: analysis)'
    )
    parser.add_argument(
        '--format', '-f',
        choices=['html', 'markdown', 'json', 'all'],
        default='html',
        help='报告格式 (默认: html)'
    )
    
    # 配置选项
    parser.add_argument(
        '--config', '-c',
        type=str,
        help='配置文件路径'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='显示详细输出'
    )
    
    return parser


def main():
    """
    主函数
    """
    # 解析命令行参数
    parser = create_argument_parser()
    args = parser.parse_args()
    
    try:
        # 初始化系统
        system = ModuleManagementSystem(args.config)
        
        if args.demo:
            # 运行演示
            system.demonstrate_modules()
            
        elif args.directory:
            # 分析目录
            if args.format == 'all':
                # 生成所有格式的报告
                reports = system.run_full_analysis(args.directory, args.output)
            else:
                # 分析目录
                results = system.analyze_directory(args.directory)
                
                # 生成指定格式的报告
                output_file = f"{args.output}.{args.format}"
                if args.format == 'markdown':
                    output_file = f"{args.output}.md"
                
                report_path = system.generate_report(results, output_file, args.format)
                print(f"\n报告已生成: {report_path}")
                
        elif args.data:
            # 处理数据文件
            results = system.process_data_file(args.data)
            
            # 生成报告
            output_file = f"{args.output}_data.{args.format}"
            if args.format == 'markdown':
                output_file = f"{args.output}_data.md"
            
            report_path = system.generate_report(results, output_file, args.format)
            print(f"\n数据处理报告已生成: {report_path}")
            
        else:
            # 显示帮助信息
            parser.print_help()
            print("\n提示: 使用 --demo 运行功能演示")
    
    except KeyboardInterrupt:
        print("\n用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()