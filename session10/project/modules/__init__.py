#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session10 项目模块包

这个包包含了项目的核心模块：
- file_analyzer: 文件分析模块
- data_processor: 数据处理模块  
- report_generator: 报告生成模块
- utils: 工具模块子包

这个文件演示了Python包的初始化和模块导出管理。

作者：Python学习教程
版本：1.0.0
"""

# ============================================================================
# 包信息
# ============================================================================

__version__ = "1.0.0"
__author__ = "Python学习教程"
__email__ = "tutorial@python.org"
__description__ = "Session10项目核心模块包"
__license__ = "MIT"

# ============================================================================
# 导入核心模块
# ============================================================================

# 尝试导入核心模块，如果失败则提供友好的错误信息
try:
    from . import file_analyzer
    from . import data_processor
    from . import report_generator
    from . import utils
except ImportError as e:
    import warnings
    warnings.warn(
        f"无法导入某些模块: {e}\n"
        "请确保所有模块文件都已正确创建。",
        ImportWarning
    )
    # 创建占位符模块，避免导入错误
    file_analyzer = None
    data_processor = None
    report_generator = None
    utils = None

# ============================================================================
# 便捷导入
# ============================================================================

# 从子模块导入主要类，提供便捷的访问方式
try:
    # 文件分析器
    if file_analyzer:
        from .file_analyzer import FileAnalyzer
    else:
        FileAnalyzer = None
    
    # 数据处理器
    if data_processor:
        from .data_processor import DataProcessor
    else:
        DataProcessor = None
    
    # 报告生成器
    if report_generator:
        from .report_generator import ReportGenerator
    else:
        ReportGenerator = None
    
    # 工具函数
    if utils:
        from .utils import math_tools, string_tools, file_tools
    else:
        math_tools = None
        string_tools = None
        file_tools = None
        
except ImportError as e:
    import warnings
    warnings.warn(
        f"无法导入某些类或函数: {e}\n"
        "某些功能可能不可用。",
        ImportWarning
    )

# ============================================================================
# 公共API定义
# ============================================================================

# 定义包的公共API，控制 from modules import * 的行为
__all__ = [
    # 模块
    'file_analyzer',
    'data_processor', 
    'report_generator',
    'utils',
    
    # 主要类
    'FileAnalyzer',
    'DataProcessor',
    'ReportGenerator',
    
    # 工具模块
    'math_tools',
    'string_tools', 
    'file_tools',
    
    # 包信息
    '__version__',
    '__author__',
    '__description__',
    
    # 便捷函数
    'get_version',
    'get_module_info',
    'list_available_modules',
    'check_dependencies'
]

# ============================================================================
# 便捷函数
# ============================================================================

def get_version():
    """
    获取包版本信息
    
    Returns:
        str: 版本字符串
    """
    return __version__

def get_module_info():
    """
    获取模块包信息
    
    Returns:
        dict: 包含包信息的字典
    """
    return {
        'name': __name__,
        'version': __version__,
        'author': __author__,
        'description': __description__,
        'license': __license__
    }

def list_available_modules():
    """
    列出可用的模块
    
    Returns:
        dict: 模块可用性状态
    """
    modules_status = {
        'file_analyzer': file_analyzer is not None,
        'data_processor': data_processor is not None,
        'report_generator': report_generator is not None,
        'utils': utils is not None
    }
    
    # 检查工具模块
    if utils:
        modules_status.update({
            'utils.math_tools': math_tools is not None,
            'utils.string_tools': string_tools is not None,
            'utils.file_tools': file_tools is not None
        })
    
    return modules_status

def check_dependencies():
    """
    检查依赖项是否满足
    
    Returns:
        dict: 依赖检查结果
    """
    dependencies = {
        'required': [],
        'optional': [],
        'missing': [],
        'status': 'ok'
    }
    
    # 检查必需的标准库模块
    required_stdlib = [
        'os', 'sys', 'pathlib', 'json', 'csv', 
        'datetime', 'collections', 'itertools', 'functools'
    ]
    
    for module_name in required_stdlib:
        try:
            __import__(module_name)
            dependencies['required'].append(module_name)
        except ImportError:
            dependencies['missing'].append(module_name)
            dependencies['status'] = 'error'
    
    # 检查可选的第三方模块
    optional_packages = [
        'pandas', 'numpy', 'jinja2', 'matplotlib', 
        'seaborn', 'plotly', 'tqdm'
    ]
    
    for package_name in optional_packages:
        try:
            __import__(package_name)
            dependencies['optional'].append(package_name)
        except ImportError:
            pass  # 可选依赖，不影响状态
    
    return dependencies

# ============================================================================
# 模块级别的配置
# ============================================================================

# 默认配置
DEFAULT_CONFIG = {
    'debug': False,
    'verbose': False,
    'encoding': 'utf-8',
    'timeout': 30
}

# 全局配置变量
_config = DEFAULT_CONFIG.copy()

def configure(**kwargs):
    """
    配置模块包的全局设置
    
    Args:
        **kwargs: 配置参数
    """
    global _config
    _config.update(kwargs)

def get_config(key=None):
    """
    获取配置值
    
    Args:
        key: 配置键，如果为None则返回所有配置
        
    Returns:
        配置值或配置字典
    """
    if key is None:
        return _config.copy()
    return _config.get(key)

# ============================================================================
# 包级别的工厂函数
# ============================================================================

def create_analyzer(config=None):
    """
    创建文件分析器实例
    
    Args:
        config: 配置字典
        
    Returns:
        FileAnalyzer实例
    """
    if FileAnalyzer is None:
        raise ImportError("FileAnalyzer类不可用")
    
    return FileAnalyzer(config or {})

def create_processor(config=None):
    """
    创建数据处理器实例
    
    Args:
        config: 配置字典
        
    Returns:
        DataProcessor实例
    """
    if DataProcessor is None:
        raise ImportError("DataProcessor类不可用")
    
    return DataProcessor(config or {})

def create_generator(config=None):
    """
    创建报告生成器实例
    
    Args:
        config: 配置字典
        
    Returns:
        ReportGenerator实例
    """
    if ReportGenerator is None:
        raise ImportError("ReportGenerator类不可用")
    
    return ReportGenerator(config or {})

def create_full_system(config=None):
    """
    创建完整的模块管理系统
    
    Args:
        config: 配置字典
        
    Returns:
        包含所有组件的字典
    """
    system = {}
    
    try:
        system['analyzer'] = create_analyzer(config)
    except ImportError:
        system['analyzer'] = None
    
    try:
        system['processor'] = create_processor(config)
    except ImportError:
        system['processor'] = None
    
    try:
        system['generator'] = create_generator(config)
    except ImportError:
        system['generator'] = None
    
    return system

# ============================================================================
# 包初始化时的自动检查
# ============================================================================

def _initialize_package():
    """
    包初始化时的自动检查和设置
    """
    # 检查依赖
    deps = check_dependencies()
    if deps['status'] == 'error':
        import warnings
        warnings.warn(
            f"缺少必需的依赖: {deps['missing']}\n"
            "某些功能可能不可用。",
            ImportWarning
        )
    
    # 设置默认编码
    import sys
    if hasattr(sys, 'setdefaultencoding'):
        sys.setdefaultencoding('utf-8')

# 执行包初始化
_initialize_package()

# ============================================================================
# 调试和开发辅助
# ============================================================================

def _debug_info():
    """
    获取调试信息
    
    Returns:
        str: 调试信息字符串
    """
    info = []
    info.append(f"Package: {__name__}")
    info.append(f"Version: {__version__}")
    info.append(f"Author: {__author__}")
    
    # 模块状态
    modules = list_available_modules()
    info.append("\nModule Status:")
    for module, available in modules.items():
        status = "✓" if available else "✗"
        info.append(f"  {status} {module}")
    
    # 依赖状态
    deps = check_dependencies()
    info.append(f"\nDependencies Status: {deps['status']}")
    info.append(f"Required: {len(deps['required'])}")
    info.append(f"Optional: {len(deps['optional'])}")
    if deps['missing']:
        info.append(f"Missing: {deps['missing']}")
    
    return "\n".join(info)

# 如果直接运行此模块，显示调试信息
if __name__ == '__main__':
    print("=== Session10 项目模块包 ===")
    print(_debug_info())
    
    print("\n=== 功能测试 ===")
    try:
        # 测试工厂函数
        system = create_full_system()
        available_components = sum(1 for comp in system.values() if comp is not None)
        print(f"可用组件: {available_components}/3")
        
        # 测试配置
        configure(debug=True, verbose=True)
        config = get_config()
        print(f"当前配置: {config}")
        
        print("\n包初始化成功！")
        
    except Exception as e:
        print(f"测试失败: {e}")