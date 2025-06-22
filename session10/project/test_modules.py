#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session10 项目：模块测试文件

这个文件用于测试项目中的所有模块，确保它们能够正常工作。
包括：
- 模块导入测试
- 基本功能测试
- 集成测试
- 错误处理测试

作者：Python学习教程
版本：1.0.0
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 测试结果统计
test_results = {
    'total': 0,
    'passed': 0,
    'failed': 0,
    'errors': []
}


def test_function(test_name: str):
    """
    测试装饰器
    
    Args:
        test_name: 测试名称
    """
    def decorator(func):
        def wrapper():
            test_results['total'] += 1
            print(f"\n{'='*50}")
            print(f"测试: {test_name}")
            print(f"{'='*50}")
            
            try:
                result = func()
                if result is not False:
                    test_results['passed'] += 1
                    print(f"✅ {test_name} - 通过")
                else:
                    test_results['failed'] += 1
                    print(f"❌ {test_name} - 失败")
                    test_results['errors'].append(f"{test_name}: 测试返回False")
            except Exception as e:
                test_results['failed'] += 1
                error_msg = f"{test_name}: {str(e)}"
                test_results['errors'].append(error_msg)
                print(f"❌ {test_name} - 错误: {e}")
        
        return wrapper
    return decorator


@test_function("模块导入测试")
def test_module_imports():
    """
    测试所有模块的导入
    """
    try:
        # 测试核心模块导入
        from modules import file_analyzer, data_processor, report_generator, utils
        print("✓ 核心模块导入成功")
        
        # 测试具体类导入
        from modules.file_analyzer import FileAnalyzer
        from modules.data_processor import DataProcessor
        from modules.report_generator import ReportGenerator
        from modules.utils import Timer, Logger, PathUtils, StringUtils
        print("✓ 具体类导入成功")
        
        # 测试配置导入
        import config
        print("✓ 配置模块导入成功")
        
        return True
        
    except ImportError as e:
        print(f"导入错误: {e}")
        return False


@test_function("文件分析器测试")
def test_file_analyzer():
    """
    测试文件分析器功能
    """
    try:
        from modules.file_analyzer import FileAnalyzer
        
        # 创建分析器实例
        analyzer = FileAnalyzer()
        print("✓ 文件分析器创建成功")
        
        # 测试当前目录分析
        current_dir = Path(__file__).parent
        results = analyzer.analyze_directory(str(current_dir))
        
        # 验证结果结构
        assert 'summary' in results, "结果中缺少summary"
        assert 'files' in results, "结果中缺少files"
        assert 'directories' in results, "结果中缺少directories"
        
        print(f"✓ 分析完成，发现 {results['summary']['total_files']} 个文件")
        
        # 测试文件信息获取
        file_info = analyzer.get_file_info(__file__)
        assert file_info['exists'], "当前文件应该存在"
        assert file_info['extension'] == '.py', "文件扩展名应该是.py"
        
        print("✓ 文件信息获取正常")
        
        return True
        
    except Exception as e:
        print(f"文件分析器测试失败: {e}")
        return False


@test_function("数据处理器测试")
def test_data_processor():
    """
    测试数据处理器功能
    """
    try:
        from modules.data_processor import DataProcessor
        
        # 创建处理器实例
        processor = DataProcessor()
        print("✓ 数据处理器创建成功")
        
        # 测试数据清洗
        test_data = [
            {'name': '  Alice  ', 'age': '25', 'city': 'New York'},
            {'name': 'Bob', 'age': '30', 'city': ''},
            {'name': '', 'age': 'invalid', 'city': 'London'}
        ]
        
        cleaned_data = processor.clean_data(test_data)
        print(f"✓ 数据清洗完成，处理了 {len(cleaned_data)} 条记录")
        
        # 测试统计计算
        stats = processor.calculate_statistics(cleaned_data)
        assert 'record_count' in stats, "统计结果中缺少record_count"
        
        print(f"✓ 统计计算完成，记录数: {stats['record_count']}")
        
        # 测试文本数据处理
        text_data = ['Hello world', '  ', 'Python is great', '', 'Data processing']
        text_stats = processor.calculate_statistics(text_data)
        assert 'line_count' in text_stats, "文本统计中缺少line_count"
        
        print(f"✓ 文本数据处理完成，行数: {text_stats['line_count']}")
        
        return True
        
    except Exception as e:
        print(f"数据处理器测试失败: {e}")
        return False


@test_function("报告生成器测试")
def test_report_generator():
    """
    测试报告生成器功能
    """
    try:
        from modules.report_generator import ReportGenerator
        
        # 创建生成器实例
        generator = ReportGenerator()
        print("✓ 报告生成器创建成功")
        
        # 准备测试数据
        test_analysis_data = {
            'summary': {
                'total_files': 10,
                'total_directories': 3,
                'total_size': 50000,
                'file_types': {'.py': 5, '.txt': 3, '.md': 2},
                'analysis_time': 1.2
            },
            'files': [
                {
                    'name': 'test.py',
                    'size': 1024,
                    'extension': '.py',
                    'modified_time': '2024-01-01 10:00:00'
                }
            ]
        }
        
        # 测试JSON报告生成
        json_path = generator.generate_analysis_report(
            test_analysis_data,
            'test_report.json'
        )
        
        # 验证文件是否生成
        assert Path(json_path).exists(), "JSON报告文件未生成"
        print(f"✓ JSON报告生成成功: {json_path}")
        
        # 测试Markdown报告生成
        md_path = generator.generate_analysis_report(
            test_analysis_data,
            'test_report.md'
        )
        
        assert Path(md_path).exists(), "Markdown报告文件未生成"
        print(f"✓ Markdown报告生成成功: {md_path}")
        
        # 测试HTML报告生成
        html_path = generator.generate_analysis_report(
            test_analysis_data,
            'test_report.html'
        )
        
        assert Path(html_path).exists(), "HTML报告文件未生成"
        print(f"✓ HTML报告生成成功: {html_path}")
        
        # 清理测试文件
        for path in [json_path, md_path, html_path]:
            try:
                Path(path).unlink()
            except:
                pass
        
        return True
        
    except Exception as e:
        print(f"报告生成器测试失败: {e}")
        return False


@test_function("工具模块测试")
def test_utils_module():
    """
    测试工具模块功能
    """
    try:
        from modules.utils import (
            Timer, Logger, PathUtils, StringUtils, 
            ValidationUtils, DateTimeUtils, SystemUtils,
            format_size, safe_divide
        )
        
        # 测试计时器
        timer = Timer("测试计时器")
        timer.start()
        import time
        time.sleep(0.01)  # 短暂延时
        elapsed = timer.stop()
        assert elapsed > 0, "计时器应该返回正数"
        print(f"✓ 计时器测试通过，耗时: {elapsed:.4f}秒")
        
        # 测试路径工具
        current_file = __file__
        file_info = PathUtils.get_file_info(current_file)
        assert file_info['exists'], "当前文件应该存在"
        assert file_info['name'] == Path(current_file).name, "文件名不匹配"
        print("✓ 路径工具测试通过")
        
        # 测试字符串工具
        test_text = "Hello World! This is a test."
        truncated = StringUtils.truncate(test_text, 20)
        assert len(truncated) <= 20, "截断后的文本长度应该不超过20"
        
        numbers = StringUtils.extract_numbers("价格是123.45元，折扣10%")
        assert 123.45 in numbers, "应该提取到123.45"
        assert 10 in numbers, "应该提取到10"
        print("✓ 字符串工具测试通过")
        
        # 测试数据验证
        test_data = {'name': 'Alice', 'age': 25}
        required_fields = ['name', 'age']
        is_valid, missing = ValidationUtils.validate_required_fields(test_data, required_fields)
        assert is_valid, "数据验证应该通过"
        assert len(missing) == 0, "不应该有缺失字段"
        print("✓ 数据验证测试通过")
        
        # 测试时间工具
        duration_str = DateTimeUtils.format_duration(3665)
        assert "小时" in duration_str, "应该包含小时单位"
        print("✓ 时间工具测试通过")
        
        # 测试系统信息
        sys_info = SystemUtils.get_system_info()
        assert 'platform' in sys_info, "系统信息应该包含platform"
        assert 'python_version' in sys_info, "系统信息应该包含python_version"
        print("✓ 系统信息测试通过")
        
        # 测试便捷函数
        size_str = format_size(1024)
        assert "KB" in size_str, "1024字节应该显示为KB"
        
        result = safe_divide(10, 2)
        assert result == 5, "10除以2应该等于5"
        
        result = safe_divide(10, 0, default=-1)
        assert result == -1, "除零应该返回默认值"
        print("✓ 便捷函数测试通过")
        
        return True
        
    except Exception as e:
        print(f"工具模块测试失败: {e}")
        return False


@test_function("配置模块测试")
def test_config_module():
    """
    测试配置模块
    """
    try:
        import config
        
        # 测试基本配置常量
        assert hasattr(config, 'PROJECT_NAME'), "配置中应该有PROJECT_NAME"
        assert hasattr(config, 'VERSION'), "配置中应该有VERSION"
        assert hasattr(config, 'DEFAULT_ENCODING'), "配置中应该有DEFAULT_ENCODING"
        
        print(f"✓ 项目名称: {config.PROJECT_NAME}")
        print(f"✓ 版本: {config.VERSION}")
        print(f"✓ 默认编码: {config.DEFAULT_ENCODING}")
        
        # 测试路径配置
        assert hasattr(config, 'PROJECT_ROOT'), "配置中应该有PROJECT_ROOT"
        assert hasattr(config, 'OUTPUT_DIR'), "配置中应该有OUTPUT_DIR"
        
        print("✓ 路径配置正常")
        
        # 测试文件配置
        assert hasattr(config, 'SUPPORTED_EXTENSIONS'), "配置中应该有SUPPORTED_EXTENSIONS"
        assert isinstance(config.SUPPORTED_EXTENSIONS, (list, tuple)), "SUPPORTED_EXTENSIONS应该是列表或元组"
        
        print(f"✓ 支持的文件扩展名: {len(config.SUPPORTED_EXTENSIONS)}个")
        
        return True
        
    except Exception as e:
        print(f"配置模块测试失败: {e}")
        return False


@test_function("集成测试")
def test_integration():
    """
    测试模块间的集成
    """
    try:
        from modules.file_analyzer import FileAnalyzer
        from modules.data_processor import DataProcessor
        from modules.report_generator import ReportGenerator
        
        # 创建所有组件
        analyzer = FileAnalyzer()
        processor = DataProcessor()
        generator = ReportGenerator()
        
        print("✓ 所有组件创建成功")
        
        # 执行完整的工作流程
        # 1. 分析当前目录
        current_dir = Path(__file__).parent
        analysis_results = analyzer.analyze_directory(str(current_dir))
        print(f"✓ 目录分析完成，发现 {analysis_results['summary']['total_files']} 个文件")
        
        # 2. 处理分析结果
        processed_data = processor.process_analysis_results(analysis_results)
        print(f"✓ 数据处理完成，处理了 {len(processed_data)} 条记录")
        
        # 3. 计算统计信息
        statistics = processor.calculate_statistics(processed_data)
        print(f"✓ 统计计算完成")
        
        # 4. 生成报告
        report_path = generator.generate_analysis_report(
            analysis_results,
            'integration_test_report.json'
        )
        
        # 验证报告文件
        assert Path(report_path).exists(), "集成测试报告文件未生成"
        print(f"✓ 集成测试报告生成成功: {report_path}")
        
        # 清理测试文件
        try:
            Path(report_path).unlink()
        except:
            pass
        
        return True
        
    except Exception as e:
        print(f"集成测试失败: {e}")
        return False


@test_function("错误处理测试")
def test_error_handling():
    """
    测试错误处理机制
    """
    try:
        from modules.file_analyzer import FileAnalyzer
        from modules.data_processor import DataProcessor
        from modules.report_generator import ReportGenerator
        
        # 测试文件分析器错误处理
        analyzer = FileAnalyzer()
        
        # 分析不存在的目录
        results = analyzer.analyze_directory("/nonexistent/directory")
        assert 'error' in results or results['summary']['total_files'] == 0, "应该处理不存在目录的错误"
        print("✓ 文件分析器错误处理正常")
        
        # 测试数据处理器错误处理
        processor = DataProcessor()
        
        # 处理无效数据
        invalid_data = None
        try:
            stats = processor.calculate_statistics(invalid_data)
            # 应该返回空统计或处理错误
            print("✓ 数据处理器错误处理正常")
        except Exception:
            print("✓ 数据处理器正确抛出异常")
        
        # 测试报告生成器错误处理
        generator = ReportGenerator()
        
        # 尝试生成到无效路径
        try:
            invalid_path = "/invalid/path/report.html"
            generator.generate_analysis_report({}, invalid_path)
        except Exception:
            print("✓ 报告生成器正确处理无效路径")
        
        return True
        
    except Exception as e:
        print(f"错误处理测试失败: {e}")
        return False


def print_test_summary():
    """
    打印测试摘要
    """
    print("\n" + "="*60)
    print("测试摘要")
    print("="*60)
    print(f"总测试数: {test_results['total']}")
    print(f"通过: {test_results['passed']}")
    print(f"失败: {test_results['failed']}")
    print(f"成功率: {(test_results['passed'] / test_results['total'] * 100):.1f}%")
    
    if test_results['errors']:
        print("\n错误详情:")
        for i, error in enumerate(test_results['errors'], 1):
            print(f"{i}. {error}")
    
    print("\n" + "="*60)
    
    if test_results['failed'] == 0:
        print("🎉 所有测试都通过了！")
    else:
        print(f"⚠️  有 {test_results['failed']} 个测试失败")
    
    print("="*60)


def main():
    """
    主测试函数
    """
    print("Session10 项目模块测试")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python版本: {sys.version}")
    print(f"工作目录: {os.getcwd()}")
    
    # 运行所有测试
    test_module_imports()
    test_config_module()
    test_utils_module()
    test_file_analyzer()
    test_data_processor()
    test_report_generator()
    test_integration()
    test_error_handling()
    
    # 打印测试摘要
    print_test_summary()
    
    # 返回测试结果
    return test_results['failed'] == 0


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)