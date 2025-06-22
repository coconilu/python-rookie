#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session10 项目配置文件

定义项目中使用的所有常量、配置选项和默认值。
这个文件演示了如何组织和管理项目配置。

作者：Python学习教程
版本：1.0.0
"""

import os
from pathlib import Path

# ============================================================================
# 项目基本信息
# ============================================================================

PROJECT_NAME = "Python模块管理系统"
PROJECT_VERSION = "1.0.0"
PROJECT_AUTHOR = "Python学习教程"
PROJECT_DESCRIPTION = "Session10项目：演示Python模块与包的实际应用"

# ============================================================================
# 路径配置
# ============================================================================

# 项目根目录
PROJECT_ROOT = Path(__file__).parent

# 数据目录
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
TEMPLATE_DIR = PROJECT_ROOT / "templates"
TEST_DIR = PROJECT_ROOT / "tests"

# 模块目录
MODULES_DIR = PROJECT_ROOT / "modules"
UTILS_DIR = MODULES_DIR / "utils"

# 输出子目录
REPORTS_DIR = OUTPUT_DIR / "reports"
DATA_OUTPUT_DIR = OUTPUT_DIR / "data"
CHARTS_DIR = OUTPUT_DIR / "charts"
LOGS_DIR = OUTPUT_DIR / "logs"

# ============================================================================
# 文件配置
# ============================================================================

# 配置文件
DEFAULT_CONFIG_FILE = "data/config.json"
LOG_CONFIG_FILE = "data/logging.json"

# 模板文件
HTML_TEMPLATE = "report_template.html"
MARKDOWN_TEMPLATE = "report_template.md"

# 示例数据文件
SAMPLE_DATA_FILE = "data/sample_data.txt"
SAMPLE_CSV_FILE = "data/sample_data.csv"
SAMPLE_JSON_FILE = "data/sample_data.json"

# ============================================================================
# 文件分析配置
# ============================================================================

ANALYSIS_CONFIG = {
    # 文件大小限制 (字节)
    'max_file_size': 10 * 1024 * 1024,  # 10MB
    'min_file_size': 0,  # 0字节
    
    # 目录遍历配置
    'max_depth': 10,  # 最大遍历深度
    'follow_symlinks': False,  # 是否跟随符号链接
    'include_hidden_files': False,  # 是否包含隐藏文件
    'include_hidden_dirs': False,  # 是否包含隐藏目录
    
    # 文件类型配置
    'supported_extensions': [
        '.py', '.txt', '.md', '.rst', '.json', '.xml', '.yaml', '.yml',
        '.csv', '.tsv', '.html', '.htm', '.css', '.js', '.sql',
        '.c', '.cpp', '.h', '.hpp', '.java', '.go', '.rs', '.php',
        '.rb', '.pl', '.sh', '.bat', '.ps1'
    ],
    
    # 排除的文件扩展名
    'excluded_extensions': [
        '.pyc', '.pyo', '.pyd', '.so', '.dll', '.exe', '.bin',
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico', '.svg',
        '.mp3', '.mp4', '.avi', '.mov', '.wav', '.pdf', '.zip',
        '.tar', '.gz', '.rar', '.7z'
    ],
    
    # 排除的目录名
    'excluded_directories': [
        '__pycache__', '.git', '.svn', '.hg', '.bzr',
        'node_modules', '.vscode', '.idea', '.vs',
        'build', 'dist', 'target', 'bin', 'obj',
        '.pytest_cache', '.coverage', '.tox'
    ],
    
    # 排除的文件名模式
    'excluded_patterns': [
        '*.tmp', '*.temp', '*.log', '*.bak', '*.swp',
        '.DS_Store', 'Thumbs.db', 'desktop.ini'
    ],
    
    # 代码分析配置
    'analyze_code_complexity': True,  # 是否分析代码复杂度
    'count_lines': True,  # 是否统计行数
    'detect_encoding': True,  # 是否检测文件编码
    'calculate_hash': False,  # 是否计算文件哈希
    
    # 性能配置
    'use_multiprocessing': False,  # 是否使用多进程
    'max_workers': 4,  # 最大工作进程数
    'chunk_size': 100,  # 批处理大小
}

# ============================================================================
# 数据处理配置
# ============================================================================

PROCESSING_CONFIG = {
    # 文件读取配置
    'default_encoding': 'utf-8',  # 默认编码
    'encoding_fallbacks': ['gbk', 'gb2312', 'latin1'],  # 编码回退列表
    'chunk_size': 1024 * 1024,  # 读取块大小 (1MB)
    'max_file_size': 100 * 1024 * 1024,  # 最大文件大小 (100MB)
    
    # CSV处理配置
    'csv_delimiter': ',',  # CSV分隔符
    'csv_quotechar': '"',  # CSV引号字符
    'csv_encoding': 'utf-8',  # CSV编码
    'csv_max_rows': 100000,  # CSV最大行数
    
    # JSON处理配置
    'json_encoding': 'utf-8',  # JSON编码
    'json_ensure_ascii': False,  # JSON是否确保ASCII
    'json_indent': 2,  # JSON缩进
    
    # 文本处理配置
    'text_line_ending': '\n',  # 文本行结束符
    'text_tab_size': 4,  # 制表符大小
    'text_max_line_length': 1000,  # 最大行长度
    
    # 数据清洗配置
    'remove_empty_lines': True,  # 是否移除空行
    'strip_whitespace': True,  # 是否去除空白字符
    'normalize_line_endings': True,  # 是否标准化行结束符
    'remove_bom': True,  # 是否移除BOM
    
    # 统计配置
    'calculate_statistics': True,  # 是否计算统计信息
    'generate_histograms': False,  # 是否生成直方图
    'top_items_count': 10,  # 显示前N项
    
    # 缓存配置
    'enable_cache': True,  # 是否启用缓存
    'cache_size': 100,  # 缓存大小
    'cache_ttl': 3600,  # 缓存生存时间 (秒)
}

# ============================================================================
# 报告生成配置
# ============================================================================

REPORT_CONFIG = {
    # 输出配置
    'output_dir': str(OUTPUT_DIR),  # 输出目录
    'reports_dir': str(REPORTS_DIR),  # 报告目录
    'template_dir': str(TEMPLATE_DIR),  # 模板目录
    
    # 默认设置
    'default_format': 'html',  # 默认格式
    'default_encoding': 'utf-8',  # 默认编码
    'default_title': '分析报告',  # 默认标题
    
    # HTML报告配置
    'html_template': HTML_TEMPLATE,  # HTML模板
    'html_css_inline': True,  # 是否内联CSS
    'html_js_inline': True,  # 是否内联JavaScript
    'html_responsive': True,  # 是否响应式设计
    'html_dark_mode': False,  # 是否支持暗色模式
    
    # Markdown报告配置
    'markdown_template': MARKDOWN_TEMPLATE,  # Markdown模板
    'markdown_toc': True,  # 是否生成目录
    'markdown_code_highlight': True,  # 是否代码高亮
    'markdown_table_format': 'github',  # 表格格式
    
    # JSON报告配置
    'json_indent': 2,  # JSON缩进
    'json_ensure_ascii': False,  # 是否确保ASCII
    'json_sort_keys': True,  # 是否排序键
    'json_separators': (',', ': '),  # JSON分隔符
    
    # 图表配置
    'enable_charts': True,  # 是否启用图表
    'chart_width': 800,  # 图表宽度
    'chart_height': 600,  # 图表高度
    'chart_dpi': 100,  # 图表DPI
    'chart_format': 'png',  # 图表格式
    
    # 样式配置
    'color_scheme': 'default',  # 颜色方案
    'font_family': 'Arial, sans-serif',  # 字体族
    'font_size': '14px',  # 字体大小
    'line_height': '1.6',  # 行高
    
    # 内容配置
    'include_summary': True,  # 是否包含摘要
    'include_details': True,  # 是否包含详细信息
    'include_charts': True,  # 是否包含图表
    'include_raw_data': False,  # 是否包含原始数据
    'max_items_display': 50,  # 最大显示项目数
}

# ============================================================================
# 日志配置
# ============================================================================

LOGGING_CONFIG = {
    # 基本配置
    'version': 1,
    'disable_existing_loggers': False,
    
    # 格式化器
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '[%(levelname)s] %(message)s'
        }
    },
    
    # 处理器
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': str(LOGS_DIR / 'application.log'),
            'mode': 'a',
            'encoding': 'utf-8'
        },
        'error_file': {
            'class': 'logging.FileHandler',
            'level': 'ERROR',
            'formatter': 'detailed',
            'filename': str(LOGS_DIR / 'errors.log'),
            'mode': 'a',
            'encoding': 'utf-8'
        }
    },
    
    # 记录器
    'loggers': {
        'modules.file_analyzer': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False
        },
        'modules.data_processor': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False
        },
        'modules.report_generator': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False
        }
    },
    
    # 根记录器
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file', 'error_file']
    }
}

# ============================================================================
# 工具模块配置
# ============================================================================

# 数学工具配置
MATH_TOOLS_CONFIG = {
    'precision': 6,  # 计算精度
    'use_decimal': False,  # 是否使用Decimal
    'infinity_threshold': 1e10,  # 无穷大阈值
    'zero_threshold': 1e-10,  # 零值阈值
}

# 字符串工具配置
STRING_TOOLS_CONFIG = {
    'default_encoding': 'utf-8',  # 默认编码
    'max_length': 10000,  # 最大长度
    'word_separators': [' ', '\t', '\n', '\r'],  # 单词分隔符
    'sentence_endings': ['.', '!', '?'],  # 句子结束符
    'title_case_exceptions': ['a', 'an', 'the', 'and', 'or', 'but'],  # 标题大小写例外
}

# 文件工具配置
FILE_TOOLS_CONFIG = {
    'temp_dir': str(PROJECT_ROOT / 'temp'),  # 临时目录
    'backup_dir': str(PROJECT_ROOT / 'backup'),  # 备份目录
    'default_permissions': 0o644,  # 默认文件权限
    'buffer_size': 8192,  # 缓冲区大小
    'timestamp_format': '%Y%m%d_%H%M%S',  # 时间戳格式
    'date_format': '%Y-%m-%d',  # 日期格式
    'time_format': '%H:%M:%S',  # 时间格式
}

# ============================================================================
# 性能配置
# ============================================================================

PERFORMANCE_CONFIG = {
    # 内存配置
    'max_memory_usage': 512 * 1024 * 1024,  # 最大内存使用 (512MB)
    'memory_check_interval': 100,  # 内存检查间隔
    
    # 并发配置
    'max_threads': 4,  # 最大线程数
    'max_processes': 2,  # 最大进程数
    'thread_timeout': 30,  # 线程超时 (秒)
    'process_timeout': 60,  # 进程超时 (秒)
    
    # 缓存配置
    'enable_file_cache': True,  # 是否启用文件缓存
    'cache_max_size': 1000,  # 缓存最大大小
    'cache_ttl': 3600,  # 缓存生存时间 (秒)
    
    # 优化配置
    'lazy_loading': True,  # 是否延迟加载
    'batch_processing': True,  # 是否批处理
    'compress_output': False,  # 是否压缩输出
}

# ============================================================================
# 错误处理配置
# ============================================================================

ERROR_CONFIG = {
    # 重试配置
    'max_retries': 3,  # 最大重试次数
    'retry_delay': 1.0,  # 重试延迟 (秒)
    'backoff_factor': 2.0,  # 退避因子
    
    # 超时配置
    'default_timeout': 30,  # 默认超时 (秒)
    'file_operation_timeout': 10,  # 文件操作超时 (秒)
    'network_timeout': 30,  # 网络超时 (秒)
    
    # 错误处理
    'ignore_permission_errors': True,  # 是否忽略权限错误
    'ignore_encoding_errors': True,  # 是否忽略编码错误
    'continue_on_error': True,  # 是否在错误时继续
    'collect_error_details': True,  # 是否收集错误详情
}

# ============================================================================
# 开发配置
# ============================================================================

DEVELOPMENT_CONFIG = {
    # 调试配置
    'debug_mode': False,  # 是否调试模式
    'verbose_output': False,  # 是否详细输出
    'profile_performance': False,  # 是否性能分析
    
    # 测试配置
    'run_tests': False,  # 是否运行测试
    'test_coverage': False,  # 是否测试覆盖率
    'mock_external_calls': False,  # 是否模拟外部调用
    
    # 开发工具
    'auto_reload': False,  # 是否自动重载
    'hot_reload': False,  # 是否热重载
    'code_formatting': True,  # 是否代码格式化
    'type_checking': True,  # 是否类型检查
}

# ============================================================================
# 环境变量配置
# ============================================================================

# 从环境变量读取配置
def get_env_config():
    """
    从环境变量获取配置
    
    Returns:
        环境配置字典
    """
    return {
        'debug': os.getenv('DEBUG', 'False').lower() == 'true',
        'log_level': os.getenv('LOG_LEVEL', 'INFO').upper(),
        'output_dir': os.getenv('OUTPUT_DIR', str(OUTPUT_DIR)),
        'max_workers': int(os.getenv('MAX_WORKERS', '4')),
        'cache_enabled': os.getenv('CACHE_ENABLED', 'True').lower() == 'true',
    }

# ============================================================================
# 配置验证
# ============================================================================

def validate_config():
    """
    验证配置的有效性
    
    Raises:
        ValueError: 配置无效时抛出
    """
    # 验证路径存在
    required_dirs = [DATA_DIR, OUTPUT_DIR]
    for dir_path in required_dirs:
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
    
    # 验证数值配置
    if ANALYSIS_CONFIG['max_file_size'] <= 0:
        raise ValueError("max_file_size must be positive")
    
    if PROCESSING_CONFIG['chunk_size'] <= 0:
        raise ValueError("chunk_size must be positive")
    
    if PERFORMANCE_CONFIG['max_threads'] <= 0:
        raise ValueError("max_threads must be positive")

# ============================================================================
# 配置合并函数
# ============================================================================

def merge_configs(*configs):
    """
    合并多个配置字典
    
    Args:
        *configs: 要合并的配置字典
        
    Returns:
        合并后的配置字典
    """
    merged = {}
    for config in configs:
        if isinstance(config, dict):
            for key, value in config.items():
                if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                    merged[key].update(value)
                else:
                    merged[key] = value
    return merged

# ============================================================================
# 导出的配置
# ============================================================================

# 主要配置字典
CONFIG = {
    'project': {
        'name': PROJECT_NAME,
        'version': PROJECT_VERSION,
        'author': PROJECT_AUTHOR,
        'description': PROJECT_DESCRIPTION
    },
    'paths': {
        'root': str(PROJECT_ROOT),
        'data': str(DATA_DIR),
        'output': str(OUTPUT_DIR),
        'modules': str(MODULES_DIR),
        'utils': str(UTILS_DIR)
    },
    'analysis': ANALYSIS_CONFIG,
    'processing': PROCESSING_CONFIG,
    'report': REPORT_CONFIG,
    'logging': LOGGING_CONFIG,
    'performance': PERFORMANCE_CONFIG,
    'error': ERROR_CONFIG,
    'development': DEVELOPMENT_CONFIG,
    'tools': {
        'math': MATH_TOOLS_CONFIG,
        'string': STRING_TOOLS_CONFIG,
        'file': FILE_TOOLS_CONFIG
    }
}

# 在模块加载时验证配置
if __name__ != '__main__':
    try:
        validate_config()
    except Exception as e:
        print(f"配置验证失败: {e}")

# 如果直接运行此文件，显示配置信息
if __name__ == '__main__':
    import json
    print("=== 项目配置信息 ===")
    print(json.dumps(CONFIG, indent=2, ensure_ascii=False, default=str))
    
    print("\n=== 配置验证 ===")
    try:
        validate_config()
        print("配置验证通过")
    except Exception as e:
        print(f"配置验证失败: {e}")