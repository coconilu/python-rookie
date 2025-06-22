#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件管理器核心模块

这个包包含了文件管理器的核心功能，包括：
- 文件管理器主类
- 文件操作功能
- 搜索引擎
- 文件分析器

作者: Python教程团队
创建日期: 2024-12-22
"""

# 版本信息
__version__ = '1.0.0'
__author__ = 'Python教程团队'

# 导入核心类
try:
    from .file_manager import FileManager
    from .file_operations import FileOperations
    from .search_engine import SearchEngine
    from .analyzer import FileAnalyzer
    
    # 定义公开接口
    __all__ = [
        'FileManager',
        'FileOperations', 
        'SearchEngine',
        'FileAnalyzer'
    ]
    
except ImportError as e:
    # 如果导入失败，提供友好的错误信息
    import warnings
    warnings.warn(f"核心模块导入失败: {e}", ImportWarning)
    
    # 提供空的__all__列表
    __all__ = []


def get_version():
    """
    获取核心模块版本
    
    Returns:
        str: 版本号
    """
    return __version__


def get_core_info():
    """
    获取核心模块信息
    
    Returns:
        dict: 模块信息字典
    """
    return {
        'version': __version__,
        'author': __author__,
        'modules': __all__,
        'description': '文件管理器核心功能模块'
    }