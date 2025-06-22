#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session10 项目：运行脚本

这个脚本提供了一个简单的命令行界面来运行项目的各种功能。
用户可以通过这个脚本来：
- 运行模块演示
- 分析文件和目录
- 处理数据文件
- 生成报告
- 运行测试

使用方法:
    python run.py --help                    # 显示帮助
    python run.py demo                       # 运行演示
    python run.py analyze <directory>        # 分析目录
    python run.py process <file>             # 处理数据文件
    python run.py test                       # 运行测试
    python run.py interactive                # 交互模式

作者：Python学习教程
版本：1.0.0
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 导入项目模块
try:
    import config
    from modules.file_analyzer import FileAnalyzer
    from modules.data_processor import DataProcessor
    from modules.report_generator import ReportGenerator
    from modules.utils import Logger, Timer, format_size
except ImportError as e:
    print(f"❌ 模块导入失败: {e}")
    print("请确保所有依赖都已正确安装")
    sys.exit(1)


class ProjectRunner:
    """
    项目运行器
    
    提供统一的接口来运行项目的各种功能
    """
    
    def __init__(self):
        """
        初始化运行器
        """
        self.logger = Logger("ProjectRunner")
        self.analyzer = FileAnalyzer()
        self.processor = DataProcessor()
        self.generator = ReportGenerator()
        
        # 创建输出目录
        self.output_dir = Path(config.OUTPUT_DIR)
        self.output_dir.mkdir(exist_ok=True)
        
        print(f"🚀 {config.PROJECT_NAME} v{config.VERSION}")
        print(f"📁 输出目录: {self.output_dir}")
    
    def run_demo(self):
        """
        运行项目演示
        """
        print("\n" + "="*50)
        print("🎯 运行项目演示")
        print("="*50)
        
        timer = Timer("演示")
        timer.start()
        
        try:
            # 1. 分析当前项目目录
            print("\n1️⃣ 分析项目目录...")
            analysis_results = self.analyzer.analyze_directory(str(project_root))
            
            summary = analysis_results['summary']
            print(f"   📊 发现 {summary['total_files']} 个文件")
            print(f"   📁 发现 {summary['total_directories']} 个目录")
            print(f"   💾 总大小: {format_size(summary['total_size'])}")
            
            # 显示文件类型分布
            if summary['file_types']:
                print("   📋 文件类型分布:")
                for ext, count in sorted(summary['file_types'].items(), 
                                        key=lambda x: x[1], reverse=True)[:5]:
                    print(f"      {ext}: {count} 个")
            
            # 2. 处理分析结果
            print("\n2️⃣ 处理分析数据...")
            processed_data = self.processor.process_analysis_results(analysis_results)
            statistics = self.processor.calculate_statistics(processed_data)
            
            print(f"   📈 处理了 {statistics.get('record_count', 0)} 条记录")
            
            # 3. 生成报告
            print("\n3️⃣ 生成分析报告...")
            
            # 生成多种格式的报告
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            reports = {
                'JSON': self.generator.generate_analysis_report(
                    analysis_results, 
                    self.output_dir / f"demo_report_{timestamp}.json"
                ),
                'HTML': self.generator.generate_analysis_report(
                    analysis_results, 
                    self.output_dir / f"demo_report_{timestamp}.html"
                ),
                'Markdown': self.generator.generate_analysis_report(
                    analysis_results, 
                    self.output_dir / f"demo_report_{timestamp}.md"
                )
            }
            
            for format_name, report_path in reports.items():
                if Path(report_path).exists():
                    size = Path(report_path).stat().st_size
                    print(f"   📄 {format_name}报告: {report_path} ({format_size(size)})")
            
            elapsed = timer.stop()
            print(f"\n✅ 演示完成！耗时: {elapsed:.2f}秒")
            
            return True
            
        except Exception as e:
            print(f"❌ 演示运行失败: {e}")
            self.logger.error(f"Demo failed: {e}")
            return False
    
    def analyze_directory(self, directory_path: str, output_format: str = 'html'):
        """
        分析指定目录
        
        Args:
            directory_path: 要分析的目录路径
            output_format: 输出格式 (html, json, md)
        """
        print(f"\n🔍 分析目录: {directory_path}")
        
        if not Path(directory_path).exists():
            print(f"❌ 目录不存在: {directory_path}")
            return False
        
        if not Path(directory_path).is_dir():
            print(f"❌ 路径不是目录: {directory_path}")
            return False
        
        timer = Timer("目录分析")
        timer.start()
        
        try:
            # 执行分析
            results = self.analyzer.analyze_directory(directory_path)
            
            # 显示分析结果摘要
            summary = results['summary']
            print(f"📊 分析完成:")
            print(f"   文件数量: {summary['total_files']}")
            print(f"   目录数量: {summary['total_directories']}")
            print(f"   总大小: {format_size(summary['total_size'])}")
            print(f"   分析耗时: {summary['analysis_time']:.2f}秒")
            
            # 生成报告
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dir_name = Path(directory_path).name or "root"
            report_filename = f"analysis_{dir_name}_{timestamp}.{output_format}"
            report_path = self.output_dir / report_filename
            
            generated_path = self.generator.generate_analysis_report(
                results, str(report_path)
            )
            
            if Path(generated_path).exists():
                size = Path(generated_path).stat().st_size
                print(f"📄 报告已生成: {generated_path} ({format_size(size)})")
            
            elapsed = timer.stop()
            print(f"✅ 总耗时: {elapsed:.2f}秒")
            
            return True
            
        except Exception as e:
            print(f"❌ 分析失败: {e}")
            self.logger.error(f"Analysis failed: {e}")
            return False
    
    def process_data_file(self, file_path: str, output_format: str = 'json'):
        """
        处理数据文件
        
        Args:
            file_path: 数据文件路径
            output_format: 输出格式
        """
        print(f"\n📊 处理数据文件: {file_path}")
        
        if not Path(file_path).exists():
            print(f"❌ 文件不存在: {file_path}")
            return False
        
        timer = Timer("数据处理")
        timer.start()
        
        try:
            # 读取和处理数据
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext == '.csv':
                data = self.processor.read_csv(file_path)
                print(f"📋 读取CSV文件，{len(data)} 行数据")
            elif file_ext == '.json':
                data = self.processor.read_json(file_path)
                print(f"📋 读取JSON文件")
            elif file_ext == '.txt':
                data = self.processor.read_text_file(file_path)
                print(f"📋 读取文本文件，{len(data)} 行")
            else:
                print(f"❌ 不支持的文件格式: {file_ext}")
                return False
            
            # 数据清洗
            if isinstance(data, list) and data:
                cleaned_data = self.processor.clean_data(data)
                print(f"🧹 数据清洗完成，保留 {len(cleaned_data)} 条有效记录")
                
                # 计算统计信息
                statistics = self.processor.calculate_statistics(cleaned_data)
                print(f"📈 统计信息计算完成")
                
                # 显示关键统计
                if 'record_count' in statistics:
                    print(f"   记录数: {statistics['record_count']}")
                if 'field_count' in statistics:
                    print(f"   字段数: {statistics['field_count']}")
                if 'data_types' in statistics:
                    print(f"   数据类型: {list(statistics['data_types'].keys())}")
            
            # 生成处理报告
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = Path(file_path).stem
            report_filename = f"processing_{file_name}_{timestamp}.{output_format}"
            report_path = self.output_dir / report_filename
            
            # 准备报告数据
            report_data = {
                'source_file': str(file_path),
                'processing_time': datetime.now().isoformat(),
                'statistics': statistics if 'statistics' in locals() else {},
                'data_sample': data[:5] if isinstance(data, list) and len(data) > 5 else data
            }
            
            generated_path = self.generator.generate_data_report(
                report_data, str(report_path)
            )
            
            if Path(generated_path).exists():
                size = Path(generated_path).stat().st_size
                print(f"📄 处理报告已生成: {generated_path} ({format_size(size)})")
            
            elapsed = timer.stop()
            print(f"✅ 处理完成！耗时: {elapsed:.2f}秒")
            
            return True
            
        except Exception as e:
            print(f"❌ 数据处理失败: {e}")
            self.logger.error(f"Data processing failed: {e}")
            return False
    
    def run_tests(self):
        """
        运行项目测试
        """
        print("\n🧪 运行项目测试")
        
        test_file = project_root / "test_modules.py"
        if not test_file.exists():
            print(f"❌ 测试文件不存在: {test_file}")
            return False
        
        try:
            # 导入并运行测试
            import subprocess
            result = subprocess.run(
                [sys.executable, str(test_file)],
                cwd=str(project_root),
                capture_output=True,
                text=True
            )
            
            print(result.stdout)
            if result.stderr:
                print("错误输出:")
                print(result.stderr)
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ 测试运行失败: {e}")
            return False
    
    def interactive_mode(self):
        """
        交互模式
        """
        print("\n🎮 进入交互模式")
        print("输入 'help' 查看可用命令，输入 'quit' 退出")
        
        while True:
            try:
                command = input("\n> ").strip().lower()
                
                if command in ['quit', 'exit', 'q']:
                    print("👋 再见！")
                    break
                elif command in ['help', 'h']:
                    self.show_interactive_help()
                elif command == 'demo':
                    self.run_demo()
                elif command.startswith('analyze '):
                    path = command[8:].strip()
                    if path:
                        self.analyze_directory(path)
                    else:
                        print("❌ 请指定要分析的目录路径")
                elif command.startswith('process '):
                    path = command[8:].strip()
                    if path:
                        self.process_data_file(path)
                    else:
                        print("❌ 请指定要处理的文件路径")
                elif command == 'test':
                    self.run_tests()
                elif command == 'status':
                    self.show_status()
                else:
                    print(f"❌ 未知命令: {command}")
                    print("输入 'help' 查看可用命令")
                    
            except KeyboardInterrupt:
                print("\n👋 再见！")
                break
            except Exception as e:
                print(f"❌ 命令执行失败: {e}")
    
    def show_interactive_help(self):
        """
        显示交互模式帮助
        """
        print("\n📖 可用命令:")
        print("  demo                    - 运行项目演示")
        print("  analyze <directory>     - 分析指定目录")
        print("  process <file>          - 处理数据文件")
        print("  test                    - 运行测试")
        print("  status                  - 显示系统状态")
        print("  help                    - 显示此帮助")
        print("  quit                    - 退出程序")
    
    def show_status(self):
        """
        显示系统状态
        """
        print("\n📊 系统状态:")
        print(f"  项目名称: {config.PROJECT_NAME}")
        print(f"  版本: {config.VERSION}")
        print(f"  Python版本: {sys.version.split()[0]}")
        print(f"  工作目录: {os.getcwd()}")
        print(f"  输出目录: {self.output_dir}")
        
        # 检查输出目录中的文件
        if self.output_dir.exists():
            files = list(self.output_dir.glob("*"))
            print(f"  输出文件数: {len(files)}")
            if files:
                total_size = sum(f.stat().st_size for f in files if f.is_file())
                print(f"  输出文件总大小: {format_size(total_size)}")


def create_parser():
    """
    创建命令行参数解析器
    """
    parser = argparse.ArgumentParser(
        description=f"{config.PROJECT_NAME} - Python模块与包学习项目",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python run.py demo                           # 运行演示
  python run.py analyze ./src                 # 分析src目录
  python run.py process data.csv              # 处理CSV文件
  python run.py test                          # 运行测试
  python run.py interactive                   # 交互模式
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # demo命令
    subparsers.add_parser('demo', help='运行项目演示')
    
    # analyze命令
    analyze_parser = subparsers.add_parser('analyze', help='分析目录')
    analyze_parser.add_argument('directory', help='要分析的目录路径')
    analyze_parser.add_argument(
        '--format', '-f', 
        choices=['html', 'json', 'md'], 
        default='html',
        help='输出格式 (默认: html)'
    )
    
    # process命令
    process_parser = subparsers.add_parser('process', help='处理数据文件')
    process_parser.add_argument('file', help='要处理的文件路径')
    process_parser.add_argument(
        '--format', '-f',
        choices=['json', 'html', 'md'],
        default='json',
        help='输出格式 (默认: json)'
    )
    
    # test命令
    subparsers.add_parser('test', help='运行测试')
    
    # interactive命令
    subparsers.add_parser('interactive', help='进入交互模式')
    
    return parser


def main():
    """
    主函数
    """
    parser = create_parser()
    args = parser.parse_args()
    
    # 创建运行器
    try:
        runner = ProjectRunner()
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return 1
    
    # 执行命令
    success = True
    
    if args.command == 'demo':
        success = runner.run_demo()
    elif args.command == 'analyze':
        success = runner.analyze_directory(args.directory, args.format)
    elif args.command == 'process':
        success = runner.process_data_file(args.file, args.format)
    elif args.command == 'test':
        success = runner.run_tests()
    elif args.command == 'interactive':
        runner.interactive_mode()
    else:
        # 如果没有指定命令，显示帮助并进入交互模式
        parser.print_help()
        print("\n💡 提示: 可以使用 'python run.py interactive' 进入交互模式")
        
        response = input("\n是否现在进入交互模式？(y/N): ").strip().lower()
        if response in ['y', 'yes']:
            runner.interactive_mode()
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())