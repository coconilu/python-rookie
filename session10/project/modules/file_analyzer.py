#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session10 项目：文件分析模块

这个模块提供文件和目录分析功能，包括：
- 目录结构分析
- 文件类型统计
- 文件大小分析
- 代码复杂度检测
- 文件内容分析

作者：Python学习教程
版本：1.0.0
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import json
import hashlib
import mimetypes
from collections import defaultdict, Counter
from datetime import datetime
import re

# 导入标准库模块
import stat
import fnmatch
from concurrent.futures import ThreadPoolExecutor, as_completed

# 尝试导入可选依赖
try:
    import chardet
    HAS_CHARDET = True
except ImportError:
    HAS_CHARDET = False

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False


class FileAnalyzer:
    """
    文件分析器类
    
    提供全面的文件和目录分析功能，支持多种分析模式和配置选项。
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化文件分析器
        
        Args:
            config: 配置字典
        """
        self.config = self._load_config(config or {})
        self.stats = {
            'files_processed': 0,
            'directories_processed': 0,
            'errors_encountered': 0,
            'total_size': 0,
            'start_time': None,
            'end_time': None
        }
        self.errors = []
        
        # 初始化MIME类型检测
        mimetypes.init()
    
    def _load_config(self, config: Dict) -> Dict:
        """
        加载和验证配置
        
        Args:
            config: 用户配置
            
        Returns:
            完整的配置字典
        """
        default_config = {
            'max_file_size': 10 * 1024 * 1024,  # 10MB
            'max_depth': 10,
            'follow_symlinks': False,
            'include_hidden': False,
            'supported_extensions': [
                '.py', '.txt', '.md', '.json', '.xml', '.csv',
                '.html', '.css', '.js', '.sql', '.yaml', '.yml'
            ],
            'excluded_extensions': [
                '.pyc', '.pyo', '.pyd', '.so', '.dll', '.exe',
                '.jpg', '.png', '.gif', '.mp3', '.mp4', '.zip'
            ],
            'excluded_directories': [
                '__pycache__', '.git', '.svn', 'node_modules',
                '.vscode', '.idea', 'build', 'dist'
            ],
            'analyze_content': True,
            'calculate_hash': False,
            'detect_encoding': True,
            'use_multiprocessing': False,
            'max_workers': 4
        }
        
        # 合并配置
        merged_config = default_config.copy()
        merged_config.update(config)
        
        return merged_config
    
    def analyze_directory(self, directory_path: str) -> Dict[str, Any]:
        """
        分析指定目录
        
        Args:
            directory_path: 目录路径
            
        Returns:
            分析结果字典
        """
        self.stats['start_time'] = datetime.now()
        self.stats['files_processed'] = 0
        self.stats['directories_processed'] = 0
        self.stats['errors_encountered'] = 0
        self.stats['total_size'] = 0
        self.errors.clear()
        
        directory = Path(directory_path)
        if not directory.exists():
            raise FileNotFoundError(f"目录不存在: {directory_path}")
        
        if not directory.is_dir():
            raise ValueError(f"路径不是目录: {directory_path}")
        
        print(f"开始分析目录: {directory_path}")
        
        # 收集所有文件
        all_files = self._collect_files(directory)
        
        # 分析文件
        if self.config['use_multiprocessing'] and len(all_files) > 10:
            file_results = self._analyze_files_parallel(all_files)
        else:
            file_results = self._analyze_files_sequential(all_files)
        
        # 生成目录结构
        directory_structure = self._analyze_directory_structure(directory)
        
        # 计算统计信息
        statistics = self._calculate_statistics(file_results)
        
        self.stats['end_time'] = datetime.now()
        duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
        
        results = {
            'directory': str(directory),
            'analysis_time': duration,
            'statistics': statistics,
            'files': file_results,
            'directory_structure': directory_structure,
            'processing_stats': self.stats.copy(),
            'errors': self.errors.copy() if self.errors else [],
            'config': self.config.copy()
        }
        
        print(f"分析完成，耗时 {duration:.2f} 秒")
        print(f"处理文件: {self.stats['files_processed']} 个")
        print(f"处理目录: {self.stats['directories_processed']} 个")
        if self.errors:
            print(f"遇到错误: {len(self.errors)} 个")
        
        return results
    
    def _collect_files(self, directory: Path) -> List[Path]:
        """
        收集目录中的所有文件
        
        Args:
            directory: 目录路径
            
        Returns:
            文件路径列表
        """
        files = []
        
        try:
            for root, dirs, filenames in os.walk(directory, 
                                                followlinks=self.config['follow_symlinks']):
                root_path = Path(root)
                
                # 检查深度限制
                depth = len(root_path.relative_to(directory).parts)
                if depth > self.config['max_depth']:
                    continue
                
                # 过滤目录
                dirs[:] = [d for d in dirs if self._should_include_directory(d)]
                
                # 处理文件
                for filename in filenames:
                    if self._should_include_file(filename):
                        file_path = root_path / filename
                        files.append(file_path)
                
                self.stats['directories_processed'] += 1
        
        except Exception as e:
            self._record_error(f"收集文件时出错: {e}", str(directory))
        
        return files
    
    def _should_include_directory(self, dirname: str) -> bool:
        """
        判断是否应该包含目录
        
        Args:
            dirname: 目录名
            
        Returns:
            是否包含
        """
        # 检查隐藏目录
        if not self.config['include_hidden'] and dirname.startswith('.'):
            return False
        
        # 检查排除列表
        if dirname in self.config['excluded_directories']:
            return False
        
        return True
    
    def _should_include_file(self, filename: str) -> bool:
        """
        判断是否应该包含文件
        
        Args:
            filename: 文件名
            
        Returns:
            是否包含
        """
        # 检查隐藏文件
        if not self.config['include_hidden'] and filename.startswith('.'):
            return False
        
        # 检查文件扩展名
        file_ext = Path(filename).suffix.lower()
        
        # 检查排除的扩展名
        if file_ext in self.config['excluded_extensions']:
            return False
        
        # 如果指定了支持的扩展名，检查是否在列表中
        if self.config['supported_extensions']:
            if file_ext not in self.config['supported_extensions']:
                return False
        
        return True
    
    def _analyze_files_sequential(self, files: List[Path]) -> List[Dict[str, Any]]:
        """
        顺序分析文件
        
        Args:
            files: 文件路径列表
            
        Returns:
            文件分析结果列表
        """
        results = []
        
        # 使用进度条（如果可用）
        if HAS_TQDM:
            files_iter = tqdm(files, desc="分析文件")
        else:
            files_iter = files
        
        for file_path in files_iter:
            try:
                result = self._analyze_single_file(file_path)
                if result:
                    results.append(result)
                    self.stats['files_processed'] += 1
            except Exception as e:
                self._record_error(f"分析文件失败: {e}", str(file_path))
        
        return results
    
    def _analyze_files_parallel(self, files: List[Path]) -> List[Dict[str, Any]]:
        """
        并行分析文件
        
        Args:
            files: 文件路径列表
            
        Returns:
            文件分析结果列表
        """
        results = []
        
        with ThreadPoolExecutor(max_workers=self.config['max_workers']) as executor:
            # 提交任务
            future_to_file = {executor.submit(self._analyze_single_file, file_path): file_path 
                             for file_path in files}
            
            # 收集结果
            if HAS_TQDM:
                futures_iter = tqdm(as_completed(future_to_file), 
                                  total=len(files), desc="分析文件")
            else:
                futures_iter = as_completed(future_to_file)
            
            for future in futures_iter:
                file_path = future_to_file[future]
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                        self.stats['files_processed'] += 1
                except Exception as e:
                    self._record_error(f"分析文件失败: {e}", str(file_path))
        
        return results
    
    def _analyze_single_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        分析单个文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件分析结果
        """
        try:
            # 获取文件统计信息
            file_stat = file_path.stat()
            
            # 检查文件大小限制
            if file_stat.st_size > self.config['max_file_size']:
                return None
            
            # 基本信息
            result = {
                'path': str(file_path),
                'name': file_path.name,
                'extension': file_path.suffix.lower(),
                'size': file_stat.st_size,
                'modified_time': datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                'created_time': datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                'permissions': oct(file_stat.st_mode)[-3:],
                'is_executable': bool(file_stat.st_mode & stat.S_IEXEC)
            }
            
            # MIME类型检测
            mime_type, _ = mimetypes.guess_type(str(file_path))
            result['mime_type'] = mime_type
            
            # 文件内容分析
            if self.config['analyze_content'] and self._is_text_file(file_path):
                content_analysis = self._analyze_file_content(file_path)
                result.update(content_analysis)
            
            # 计算文件哈希（如果启用）
            if self.config['calculate_hash']:
                result['hash'] = self._calculate_file_hash(file_path)
            
            self.stats['total_size'] += file_stat.st_size
            return result
            
        except Exception as e:
            self._record_error(f"分析文件时出错: {e}", str(file_path))
            return None
    
    def _is_text_file(self, file_path: Path) -> bool:
        """
        判断是否为文本文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            是否为文本文件
        """
        # 基于扩展名判断
        text_extensions = {
            '.txt', '.py', '.js', '.html', '.css', '.json', '.xml',
            '.md', '.rst', '.yaml', '.yml', '.csv', '.sql', '.sh',
            '.bat', '.ps1', '.c', '.cpp', '.h', '.java', '.go'
        }
        
        if file_path.suffix.lower() in text_extensions:
            return True
        
        # 尝试读取文件开头判断
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                if not chunk:
                    return True
                
                # 检查是否包含空字节（二进制文件的特征）
                if b'\x00' in chunk:
                    return False
                
                # 尝试解码为文本
                try:
                    chunk.decode('utf-8')
                    return True
                except UnicodeDecodeError:
                    try:
                        chunk.decode('gbk')
                        return True
                    except UnicodeDecodeError:
                        return False
        except Exception:
            return False
    
    def _analyze_file_content(self, file_path: Path) -> Dict[str, Any]:
        """
        分析文件内容
        
        Args:
            file_path: 文件路径
            
        Returns:
            内容分析结果
        """
        result = {
            'encoding': 'unknown',
            'line_count': 0,
            'word_count': 0,
            'char_count': 0,
            'empty_lines': 0,
            'max_line_length': 0
        }
        
        try:
            # 检测编码
            if self.config['detect_encoding'] and HAS_CHARDET:
                with open(file_path, 'rb') as f:
                    raw_data = f.read()
                    encoding_result = chardet.detect(raw_data)
                    encoding = encoding_result.get('encoding', 'utf-8')
            else:
                encoding = 'utf-8'
            
            result['encoding'] = encoding
            
            # 读取文件内容
            try:
                with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                    lines = f.readlines()
            except UnicodeDecodeError:
                # 回退到其他编码
                for fallback_encoding in ['gbk', 'latin1']:
                    try:
                        with open(file_path, 'r', encoding=fallback_encoding, errors='ignore') as f:
                            lines = f.readlines()
                        result['encoding'] = fallback_encoding
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    return result
            
            # 分析内容
            result['line_count'] = len(lines)
            result['char_count'] = sum(len(line) for line in lines)
            result['empty_lines'] = sum(1 for line in lines if not line.strip())
            
            if lines:
                result['max_line_length'] = max(len(line.rstrip('\n\r')) for line in lines)
            
            # 计算单词数（简单统计）
            text_content = ''.join(lines)
            words = re.findall(r'\b\w+\b', text_content)
            result['word_count'] = len(words)
            
            # 代码特定分析
            if file_path.suffix.lower() == '.py':
                python_analysis = self._analyze_python_file(lines)
                result.update(python_analysis)
            
        except Exception as e:
            self._record_error(f"分析文件内容时出错: {e}", str(file_path))
        
        return result
    
    def _analyze_python_file(self, lines: List[str]) -> Dict[str, Any]:
        """
        分析Python文件
        
        Args:
            lines: 文件行列表
            
        Returns:
            Python文件分析结果
        """
        result = {
            'comment_lines': 0,
            'docstring_lines': 0,
            'import_lines': 0,
            'function_count': 0,
            'class_count': 0,
            'complexity_score': 0
        }
        
        in_docstring = False
        docstring_quote = None
        
        for line in lines:
            stripped = line.strip()
            
            # 跳过空行
            if not stripped:
                continue
            
            # 检查文档字符串
            if not in_docstring:
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    in_docstring = True
                    docstring_quote = stripped[:3]
                    result['docstring_lines'] += 1
                    if stripped.count(docstring_quote) >= 2:
                        in_docstring = False
                    continue
            else:
                result['docstring_lines'] += 1
                if docstring_quote in stripped:
                    in_docstring = False
                continue
            
            # 检查注释
            if stripped.startswith('#'):
                result['comment_lines'] += 1
                continue
            
            # 检查导入语句
            if stripped.startswith('import ') or stripped.startswith('from '):
                result['import_lines'] += 1
            
            # 检查函数定义
            if stripped.startswith('def '):
                result['function_count'] += 1
            
            # 检查类定义
            if stripped.startswith('class '):
                result['class_count'] += 1
            
            # 简单的复杂度计算（基于控制结构）
            complexity_keywords = ['if', 'elif', 'else', 'for', 'while', 'try', 'except', 'with']
            for keyword in complexity_keywords:
                if stripped.startswith(keyword + ' ') or stripped.startswith(keyword + ':'):
                    result['complexity_score'] += 1
        
        return result
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """
        计算文件哈希值
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件的MD5哈希值
        """
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            self._record_error(f"计算文件哈希时出错: {e}", str(file_path))
            return ""
    
    def _analyze_directory_structure(self, directory: Path) -> Dict[str, Any]:
        """
        分析目录结构
        
        Args:
            directory: 目录路径
            
        Returns:
            目录结构分析结果
        """
        structure = {
            'root': str(directory),
            'total_directories': 0,
            'total_files': 0,
            'max_depth': 0,
            'tree': self._build_directory_tree(directory)
        }
        
        # 递归计算统计信息
        def count_items(tree_node, current_depth=0):
            structure['max_depth'] = max(structure['max_depth'], current_depth)
            
            if tree_node['type'] == 'directory':
                structure['total_directories'] += 1
                for child in tree_node.get('children', []):
                    count_items(child, current_depth + 1)
            else:
                structure['total_files'] += 1
        
        count_items(structure['tree'])
        
        return structure
    
    def _build_directory_tree(self, directory: Path, max_depth: int = 3) -> Dict[str, Any]:
        """
        构建目录树结构
        
        Args:
            directory: 目录路径
            max_depth: 最大深度
            
        Returns:
            目录树字典
        """
        def build_tree(path: Path, current_depth: int = 0) -> Dict[str, Any]:
            if current_depth > max_depth:
                return None
            
            node = {
                'name': path.name,
                'path': str(path),
                'type': 'directory' if path.is_dir() else 'file'
            }
            
            if path.is_dir():
                children = []
                try:
                    for child in sorted(path.iterdir()):
                        if self._should_include_directory(child.name) if child.is_dir() else self._should_include_file(child.name):
                            child_node = build_tree(child, current_depth + 1)
                            if child_node:
                                children.append(child_node)
                except PermissionError:
                    pass
                
                if children:
                    node['children'] = children
            else:
                try:
                    stat_info = path.stat()
                    node['size'] = stat_info.st_size
                except (OSError, PermissionError):
                    node['size'] = 0
            
            return node
        
        return build_tree(directory)
    
    def _calculate_statistics(self, file_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        计算统计信息
        
        Args:
            file_results: 文件分析结果列表
            
        Returns:
            统计信息字典
        """
        if not file_results:
            return {}
        
        # 基本统计
        total_files = len(file_results)
        total_size = sum(f['size'] for f in file_results)
        
        # 文件类型统计
        extensions = Counter(f['extension'] for f in file_results if f['extension'])
        
        # 大小统计
        sizes = [f['size'] for f in file_results]
        avg_size = total_size / total_files if total_files > 0 else 0
        
        # 最大和最小文件
        largest_file = max(file_results, key=lambda x: x['size']) if file_results else None
        smallest_file = min(file_results, key=lambda x: x['size']) if file_results else None
        
        # 按大小排序的前10个文件
        largest_files = sorted(file_results, key=lambda x: x['size'], reverse=True)[:10]
        
        # 文本文件统计
        text_files = [f for f in file_results if 'line_count' in f]
        total_lines = sum(f.get('line_count', 0) for f in text_files)
        total_words = sum(f.get('word_count', 0) for f in text_files)
        
        # Python文件统计
        python_files = [f for f in file_results if f['extension'] == '.py']
        total_functions = sum(f.get('function_count', 0) for f in python_files)
        total_classes = sum(f.get('class_count', 0) for f in python_files)
        
        statistics = {
            'file_count': total_files,
            'total_size': total_size,
            'average_size': avg_size,
            'largest_file': {
                'name': largest_file['name'],
                'size': largest_file['size'],
                'path': largest_file['path']
            } if largest_file else None,
            'smallest_file': {
                'name': smallest_file['name'],
                'size': smallest_file['size'],
                'path': smallest_file['path']
            } if smallest_file else None,
            'file_types': dict(extensions.most_common()),
            'largest_files': [
                {
                    'name': f['name'],
                    'size': f['size'],
                    'path': f['path']
                } for f in largest_files
            ],
            'text_statistics': {
                'text_files': len(text_files),
                'total_lines': total_lines,
                'total_words': total_words,
                'average_lines_per_file': total_lines / len(text_files) if text_files else 0
            },
            'python_statistics': {
                'python_files': len(python_files),
                'total_functions': total_functions,
                'total_classes': total_classes,
                'average_functions_per_file': total_functions / len(python_files) if python_files else 0
            }
        }
        
        return statistics
    
    def _record_error(self, message: str, file_path: str):
        """
        记录错误信息
        
        Args:
            message: 错误消息
            file_path: 文件路径
        """
        error_info = {
            'message': message,
            'file_path': file_path,
            'timestamp': datetime.now().isoformat()
        }
        self.errors.append(error_info)
        self.stats['errors_encountered'] += 1
    
    def get_analysis_summary(self, results: Dict[str, Any]) -> str:
        """
        获取分析摘要
        
        Args:
            results: 分析结果
            
        Returns:
            摘要字符串
        """
        stats = results.get('statistics', {})
        
        summary_lines = [
            f"目录分析摘要: {results['directory']}",
            f"分析时间: {results['analysis_time']:.2f} 秒",
            f"文件总数: {stats.get('file_count', 0)}",
            f"总大小: {stats.get('total_size', 0) / (1024*1024):.2f} MB",
            f"平均大小: {stats.get('average_size', 0) / 1024:.2f} KB"
        ]
        
        if 'file_types' in stats:
            summary_lines.append("主要文件类型:")
            for ext, count in list(stats['file_types'].items())[:5]:
                summary_lines.append(f"  {ext or '无扩展名'}: {count} 个")
        
        if results.get('errors'):
            summary_lines.append(f"错误数量: {len(results['errors'])}")
        
        return "\n".join(summary_lines)


# 便捷函数
def analyze_directory(directory_path: str, config: Optional[Dict] = None) -> Dict[str, Any]:
    """
    便捷的目录分析函数
    
    Args:
        directory_path: 目录路径
        config: 配置字典
        
    Returns:
        分析结果
    """
    analyzer = FileAnalyzer(config)
    return analyzer.analyze_directory(directory_path)


def quick_analyze(directory_path: str) -> str:
    """
    快速分析并返回摘要
    
    Args:
        directory_path: 目录路径
        
    Returns:
        分析摘要
    """
    config = {
        'analyze_content': False,
        'calculate_hash': False,
        'max_depth': 3
    }
    
    analyzer = FileAnalyzer(config)
    results = analyzer.analyze_directory(directory_path)
    return analyzer.get_analysis_summary(results)


# 如果直接运行此模块，进行演示
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = "."
    
    print(f"=== 文件分析器演示 ===")
    print(f"分析目录: {directory}")
    
    try:
        # 快速分析
        summary = quick_analyze(directory)
        print("\n=== 快速分析结果 ===")
        print(summary)
        
        # 详细分析
        print("\n=== 详细分析 ===")
        analyzer = FileAnalyzer()
        results = analyzer.analyze_directory(directory)
        
        # 显示统计信息
        stats = results['statistics']
        print(f"\n文件类型分布:")
        for ext, count in list(stats.get('file_types', {}).items())[:10]:
            print(f"  {ext or '无扩展名'}: {count} 个")
        
        if stats.get('largest_files'):
            print(f"\n最大的文件:")
            for file_info in stats['largest_files'][:5]:
                size_kb = file_info['size'] / 1024
                print(f"  {file_info['name']}: {size_kb:.1f} KB")
        
    except Exception as e:
        print(f"分析失败: {e}")