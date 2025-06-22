#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session10 项目：数据处理模块

这个模块提供数据处理功能，包括：
- CSV/JSON/文本文件读取和处理
- 数据清洗和转换
- 统计分析
- 数据验证
- 批处理支持

作者：Python学习教程
版本：1.0.0
"""

import os
import json
import csv
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Tuple
from collections import defaultdict, Counter
from datetime import datetime
import re
import math
from io import StringIO

# 尝试导入可选依赖
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False


class DataProcessor:
    """
    数据处理器类
    
    提供全面的数据处理功能，支持多种数据格式和处理模式。
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化数据处理器
        
        Args:
            config: 配置字典
        """
        self.config = self._load_config(config or {})
        self.stats = {
            'files_processed': 0,
            'records_processed': 0,
            'errors_encountered': 0,
            'start_time': None,
            'end_time': None
        }
        self.errors = []
        self.cache = {}
    
    def _load_config(self, config: Dict) -> Dict:
        """
        加载和验证配置
        
        Args:
            config: 用户配置
            
        Returns:
            完整的配置字典
        """
        default_config = {
            'default_encoding': 'utf-8',
            'encoding_fallbacks': ['gbk', 'gb2312', 'latin1'],
            'chunk_size': 1024 * 1024,  # 1MB
            'max_file_size': 100 * 1024 * 1024,  # 100MB
            'csv_delimiter': ',',
            'csv_quotechar': '"',
            'csv_max_rows': 100000,
            'json_ensure_ascii': False,
            'remove_empty_lines': True,
            'strip_whitespace': True,
            'normalize_line_endings': True,
            'enable_cache': True,
            'cache_size': 100,
            'validate_data': True,
            'auto_detect_types': True
        }
        
        # 合并配置
        merged_config = default_config.copy()
        merged_config.update(config)
        
        return merged_config
    
    def load_csv(self, file_path: str, **kwargs) -> List[Dict[str, Any]]:
        """
        加载CSV文件
        
        Args:
            file_path: CSV文件路径
            **kwargs: 额外的CSV读取参数
            
        Returns:
            数据记录列表
        """
        self._start_processing()
        
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"文件不存在: {file_path}")
            
            # 检查缓存
            cache_key = f"csv_{file_path}_{hash(str(kwargs))}"
            if self.config['enable_cache'] and cache_key in self.cache:
                print(f"从缓存加载: {file_path}")
                return self.cache[cache_key]
            
            print(f"加载CSV文件: {file_path}")
            
            # 设置CSV参数
            csv_params = {
                'delimiter': kwargs.get('delimiter', self.config['csv_delimiter']),
                'quotechar': kwargs.get('quotechar', self.config['csv_quotechar']),
                'encoding': kwargs.get('encoding', self.config['default_encoding'])
            }
            
            # 如果有pandas，优先使用
            if HAS_PANDAS and not kwargs.get('use_builtin', False):
                data = self._load_csv_pandas(file_path, csv_params, **kwargs)
            else:
                data = self._load_csv_builtin(file_path, csv_params, **kwargs)
            
            # 缓存结果
            if self.config['enable_cache']:
                self._cache_data(cache_key, data)
            
            self.stats['files_processed'] += 1
            self.stats['records_processed'] += len(data)
            
            print(f"成功加载 {len(data)} 条记录")
            return data
            
        except Exception as e:
            self._record_error(f"加载CSV文件失败: {e}", file_path)
            return []
        finally:
            self._end_processing()
    
    def _load_csv_pandas(self, file_path: Path, csv_params: Dict, **kwargs) -> List[Dict[str, Any]]:
        """
        使用pandas加载CSV文件
        
        Args:
            file_path: 文件路径
            csv_params: CSV参数
            **kwargs: 额外参数
            
        Returns:
            数据记录列表
        """
        try:
            # pandas参数
            pd_params = {
                'sep': csv_params['delimiter'],
                'encoding': csv_params['encoding'],
                'quotechar': csv_params['quotechar'],
                'nrows': kwargs.get('max_rows', self.config['csv_max_rows'])
            }
            
            # 读取数据
            df = pd.read_csv(file_path, **pd_params)
            
            # 转换为字典列表
            data = df.to_dict('records')
            
            # 处理NaN值
            for record in data:
                for key, value in record.items():
                    if pd.isna(value):
                        record[key] = None
            
            return data
            
        except Exception as e:
            print(f"pandas加载失败，回退到内置方法: {e}")
            return self._load_csv_builtin(file_path, csv_params, **kwargs)
    
    def _load_csv_builtin(self, file_path: Path, csv_params: Dict, **kwargs) -> List[Dict[str, Any]]:
        """
        使用内置csv模块加载文件
        
        Args:
            file_path: 文件路径
            csv_params: CSV参数
            **kwargs: 额外参数
            
        Returns:
            数据记录列表
        """
        data = []
        encoding = csv_params['encoding']
        
        # 尝试不同编码
        for attempt_encoding in [encoding] + self.config['encoding_fallbacks']:
            try:
                with open(file_path, 'r', encoding=attempt_encoding, newline='') as f:
                    # 检测方言
                    sample = f.read(1024)
                    f.seek(0)
                    
                    try:
                        dialect = csv.Sniffer().sniff(sample)
                        reader = csv.DictReader(f, dialect=dialect)
                    except csv.Error:
                        reader = csv.DictReader(
                            f,
                            delimiter=csv_params['delimiter'],
                            quotechar=csv_params['quotechar']
                        )
                    
                    # 读取数据
                    max_rows = kwargs.get('max_rows', self.config['csv_max_rows'])
                    for i, row in enumerate(reader):
                        if max_rows and i >= max_rows:
                            break
                        
                        # 清理数据
                        cleaned_row = {}
                        for key, value in row.items():
                            if key is not None:  # 跳过None键
                                cleaned_value = self._clean_value(value)
                                cleaned_row[key.strip()] = cleaned_value
                        
                        data.append(cleaned_row)
                
                break  # 成功读取，跳出编码尝试循环
                
            except UnicodeDecodeError:
                continue  # 尝试下一个编码
            except Exception as e:
                raise e
        
        return data
    
    def load_json(self, file_path: str, **kwargs) -> Union[Dict, List]:
        """
        加载JSON文件
        
        Args:
            file_path: JSON文件路径
            **kwargs: 额外参数
            
        Returns:
            JSON数据
        """
        self._start_processing()
        
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"文件不存在: {file_path}")
            
            # 检查缓存
            cache_key = f"json_{file_path}"
            if self.config['enable_cache'] and cache_key in self.cache:
                print(f"从缓存加载: {file_path}")
                return self.cache[cache_key]
            
            print(f"加载JSON文件: {file_path}")
            
            encoding = kwargs.get('encoding', self.config['default_encoding'])
            
            # 尝试不同编码
            for attempt_encoding in [encoding] + self.config['encoding_fallbacks']:
                try:
                    with open(file_path, 'r', encoding=attempt_encoding) as f:
                        data = json.load(f)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise ValueError("无法使用任何编码读取文件")
            
            # 缓存结果
            if self.config['enable_cache']:
                self._cache_data(cache_key, data)
            
            self.stats['files_processed'] += 1
            if isinstance(data, list):
                self.stats['records_processed'] += len(data)
            else:
                self.stats['records_processed'] += 1
            
            print(f"成功加载JSON数据")
            return data
            
        except Exception as e:
            self._record_error(f"加载JSON文件失败: {e}", file_path)
            return {}
        finally:
            self._end_processing()
    
    def load_text(self, file_path: str, **kwargs) -> List[str]:
        """
        加载文本文件
        
        Args:
            file_path: 文本文件路径
            **kwargs: 额外参数
            
        Returns:
            文本行列表
        """
        self._start_processing()
        
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"文件不存在: {file_path}")
            
            print(f"加载文本文件: {file_path}")
            
            encoding = kwargs.get('encoding', self.config['default_encoding'])
            
            # 尝试不同编码
            for attempt_encoding in [encoding] + self.config['encoding_fallbacks']:
                try:
                    with open(file_path, 'r', encoding=attempt_encoding) as f:
                        lines = f.readlines()
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise ValueError("无法使用任何编码读取文件")
            
            # 清理文本行
            if self.config['strip_whitespace']:
                lines = [line.strip() for line in lines]
            
            if self.config['remove_empty_lines']:
                lines = [line for line in lines if line]
            
            if self.config['normalize_line_endings']:
                lines = [line.replace('\r\n', '\n').replace('\r', '\n') for line in lines]
            
            self.stats['files_processed'] += 1
            self.stats['records_processed'] += len(lines)
            
            print(f"成功加载 {len(lines)} 行文本")
            return lines
            
        except Exception as e:
            self._record_error(f"加载文本文件失败: {e}", file_path)
            return []
        finally:
            self._end_processing()
    
    def clean_data(self, data: Union[List[Dict], List[str], Dict]) -> Union[List[Dict], List[str], Dict]:
        """
        清洗数据
        
        Args:
            data: 原始数据
            
        Returns:
            清洗后的数据
        """
        print("开始数据清洗...")
        
        if isinstance(data, list):
            if data and isinstance(data[0], dict):
                # 字典列表
                return self._clean_dict_list(data)
            else:
                # 字符串列表
                return self._clean_string_list(data)
        elif isinstance(data, dict):
            return self._clean_dict(data)
        else:
            return data
    
    def _clean_dict_list(self, data: List[Dict]) -> List[Dict]:
        """
        清洗字典列表
        
        Args:
            data: 字典列表
            
        Returns:
            清洗后的字典列表
        """
        cleaned_data = []
        
        for record in data:
            cleaned_record = {}
            for key, value in record.items():
                # 清理键名
                clean_key = self._clean_key(key)
                # 清理值
                clean_value = self._clean_value(value)
                
                if clean_key and clean_value is not None:
                    cleaned_record[clean_key] = clean_value
            
            if cleaned_record:  # 只添加非空记录
                cleaned_data.append(cleaned_record)
        
        return cleaned_data
    
    def _clean_string_list(self, data: List[str]) -> List[str]:
        """
        清洗字符串列表
        
        Args:
            data: 字符串列表
            
        Returns:
            清洗后的字符串列表
        """
        cleaned_data = []
        
        for line in data:
            cleaned_line = self._clean_value(line)
            if cleaned_line:
                cleaned_data.append(cleaned_line)
        
        return cleaned_data
    
    def _clean_dict(self, data: Dict) -> Dict:
        """
        清洗字典
        
        Args:
            data: 字典
            
        Returns:
            清洗后的字典
        """
        cleaned_data = {}
        
        for key, value in data.items():
            clean_key = self._clean_key(key)
            clean_value = self._clean_value(value)
            
            if clean_key and clean_value is not None:
                cleaned_data[clean_key] = clean_value
        
        return cleaned_data
    
    def _clean_key(self, key: str) -> str:
        """
        清理键名
        
        Args:
            key: 原始键名
            
        Returns:
            清理后的键名
        """
        if not isinstance(key, str):
            key = str(key)
        
        # 去除空白字符
        key = key.strip()
        
        # 替换特殊字符
        key = re.sub(r'[^\w\s-]', '', key)
        
        # 替换空格为下划线
        key = re.sub(r'\s+', '_', key)
        
        # 转换为小写
        key = key.lower()
        
        return key
    
    def _clean_value(self, value: Any) -> Any:
        """
        清理值
        
        Args:
            value: 原始值
            
        Returns:
            清理后的值
        """
        if value is None:
            return None
        
        if isinstance(value, str):
            # 去除空白字符
            value = value.strip()
            
            # 处理空字符串
            if not value or value.lower() in ['null', 'none', 'n/a', 'na', '']:
                return None
            
            # 自动类型检测
            if self.config['auto_detect_types']:
                return self._auto_convert_type(value)
        
        return value
    
    def _auto_convert_type(self, value: str) -> Any:
        """
        自动转换数据类型
        
        Args:
            value: 字符串值
            
        Returns:
            转换后的值
        """
        # 尝试转换为数字
        try:
            # 整数
            if '.' not in value and 'e' not in value.lower():
                return int(value)
            # 浮点数
            else:
                return float(value)
        except ValueError:
            pass
        
        # 尝试转换为布尔值
        if value.lower() in ['true', 'yes', 'y', '1']:
            return True
        elif value.lower() in ['false', 'no', 'n', '0']:
            return False
        
        # 尝试转换为日期
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
            r'\d{2}-\d{2}-\d{4}',  # MM-DD-YYYY
        ]
        
        for pattern in date_patterns:
            if re.match(pattern, value):
                try:
                    # 这里可以添加具体的日期解析逻辑
                    return value  # 暂时返回原字符串
                except:
                    pass
        
        # 返回原字符串
        return value
    
    def calculate_statistics(self, data: Union[List[Dict], List[str], Dict]) -> Dict[str, Any]:
        """
        计算统计信息
        
        Args:
            data: 数据
            
        Returns:
            统计信息字典
        """
        print("计算统计信息...")
        
        if isinstance(data, list):
            if data and isinstance(data[0], dict):
                return self._calculate_dict_list_stats(data)
            else:
                return self._calculate_string_list_stats(data)
        elif isinstance(data, dict):
            return self._calculate_dict_stats(data)
        else:
            return {'type': 'unknown', 'value': str(data)}
    
    def _calculate_dict_list_stats(self, data: List[Dict]) -> Dict[str, Any]:
        """
        计算字典列表的统计信息
        
        Args:
            data: 字典列表
            
        Returns:
            统计信息
        """
        if not data:
            return {'record_count': 0}
        
        stats = {
            'record_count': len(data),
            'field_count': 0,
            'fields': {},
            'field_types': {},
            'missing_values': {},
            'unique_values': {},
            'numeric_stats': {}
        }
        
        # 收集所有字段
        all_fields = set()
        for record in data:
            all_fields.update(record.keys())
        
        stats['field_count'] = len(all_fields)
        
        # 分析每个字段
        for field in all_fields:
            values = []
            missing_count = 0
            type_counter = Counter()
            
            for record in data:
                value = record.get(field)
                if value is None:
                    missing_count += 1
                else:
                    values.append(value)
                    type_counter[type(value).__name__] += 1
            
            # 字段统计
            stats['fields'][field] = {
                'total_count': len(data),
                'non_null_count': len(values),
                'null_count': missing_count,
                'null_percentage': (missing_count / len(data)) * 100
            }
            
            # 类型统计
            stats['field_types'][field] = dict(type_counter.most_common())
            
            # 唯一值统计
            unique_values = set(values)
            stats['unique_values'][field] = {
                'count': len(unique_values),
                'percentage': (len(unique_values) / len(values)) * 100 if values else 0
            }
            
            # 数值统计
            numeric_values = [v for v in values if isinstance(v, (int, float))]
            if numeric_values:
                stats['numeric_stats'][field] = self._calculate_numeric_stats(numeric_values)
        
        return stats
    
    def _calculate_string_list_stats(self, data: List[str]) -> Dict[str, Any]:
        """
        计算字符串列表的统计信息
        
        Args:
            data: 字符串列表
            
        Returns:
            统计信息
        """
        if not data:
            return {'line_count': 0}
        
        stats = {
            'line_count': len(data),
            'total_characters': sum(len(line) for line in data),
            'average_line_length': sum(len(line) for line in data) / len(data),
            'max_line_length': max(len(line) for line in data),
            'min_line_length': min(len(line) for line in data),
            'empty_lines': sum(1 for line in data if not line.strip()),
            'word_count': sum(len(line.split()) for line in data),
            'unique_lines': len(set(data))
        }
        
        # 字符统计
        all_text = ''.join(data)
        char_counter = Counter(all_text)
        stats['character_frequency'] = dict(char_counter.most_common(10))
        
        # 单词统计
        all_words = []
        for line in data:
            words = re.findall(r'\b\w+\b', line.lower())
            all_words.extend(words)
        
        word_counter = Counter(all_words)
        stats['word_frequency'] = dict(word_counter.most_common(10))
        stats['unique_words'] = len(set(all_words))
        
        return stats
    
    def _calculate_dict_stats(self, data: Dict) -> Dict[str, Any]:
        """
        计算字典的统计信息
        
        Args:
            data: 字典
            
        Returns:
            统计信息
        """
        stats = {
            'key_count': len(data),
            'keys': list(data.keys()),
            'value_types': {},
            'nested_objects': 0,
            'total_size': 0
        }
        
        # 分析值类型
        type_counter = Counter()
        for key, value in data.items():
            value_type = type(value).__name__
            type_counter[value_type] += 1
            
            if isinstance(value, (dict, list)):
                stats['nested_objects'] += 1
            
            # 估算大小
            try:
                stats['total_size'] += len(str(value))
            except:
                pass
        
        stats['value_types'] = dict(type_counter)
        
        return stats
    
    def _calculate_numeric_stats(self, values: List[Union[int, float]]) -> Dict[str, float]:
        """
        计算数值统计信息
        
        Args:
            values: 数值列表
            
        Returns:
            数值统计信息
        """
        if not values:
            return {}
        
        # 使用numpy（如果可用）
        if HAS_NUMPY:
            arr = np.array(values)
            return {
                'count': len(values),
                'mean': float(np.mean(arr)),
                'median': float(np.median(arr)),
                'std': float(np.std(arr)),
                'min': float(np.min(arr)),
                'max': float(np.max(arr)),
                'q25': float(np.percentile(arr, 25)),
                'q75': float(np.percentile(arr, 75))
            }
        else:
            # 使用内置函数
            sorted_values = sorted(values)
            n = len(values)
            
            return {
                'count': n,
                'mean': sum(values) / n,
                'median': sorted_values[n // 2] if n % 2 == 1 else (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2,
                'std': math.sqrt(sum((x - sum(values) / n) ** 2 for x in values) / n),
                'min': min(values),
                'max': max(values),
                'q25': sorted_values[n // 4],
                'q75': sorted_values[3 * n // 4]
            }
    
    def process_analysis_results(self, analysis_results: Dict) -> List[Dict[str, Any]]:
        """
        处理文件分析结果
        
        Args:
            analysis_results: 文件分析结果
            
        Returns:
            处理后的数据
        """
        print("处理分析结果...")
        
        files = analysis_results.get('files', [])
        processed_data = []
        
        for file_info in files:
            # 提取关键信息
            processed_record = {
                'file_name': file_info.get('name', ''),
                'file_path': file_info.get('path', ''),
                'file_extension': file_info.get('extension', ''),
                'file_size': file_info.get('size', 0),
                'file_type': self._categorize_file_type(file_info.get('extension', '')),
                'is_text_file': 'line_count' in file_info,
                'line_count': file_info.get('line_count', 0),
                'word_count': file_info.get('word_count', 0),
                'encoding': file_info.get('encoding', 'unknown'),
                'modified_time': file_info.get('modified_time', ''),
                'complexity_score': file_info.get('complexity_score', 0)
            }
            
            # 添加Python特定信息
            if file_info.get('extension') == '.py':
                processed_record.update({
                    'function_count': file_info.get('function_count', 0),
                    'class_count': file_info.get('class_count', 0),
                    'import_lines': file_info.get('import_lines', 0),
                    'comment_lines': file_info.get('comment_lines', 0)
                })
            
            processed_data.append(processed_record)
        
        return processed_data
    
    def _categorize_file_type(self, extension: str) -> str:
        """
        分类文件类型
        
        Args:
            extension: 文件扩展名
            
        Returns:
            文件类型类别
        """
        categories = {
            'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h', '.go', '.rs'],
            'data': ['.json', '.xml', '.csv', '.tsv', '.yaml', '.yml'],
            'document': ['.txt', '.md', '.rst', '.doc', '.docx', '.pdf'],
            'config': ['.ini', '.conf', '.cfg', '.properties'],
            'script': ['.sh', '.bat', '.ps1'],
            'image': ['.jpg', '.png', '.gif', '.svg', '.bmp'],
            'archive': ['.zip', '.tar', '.gz', '.rar', '.7z']
        }
        
        extension = extension.lower()
        for category, extensions in categories.items():
            if extension in extensions:
                return category
        
        return 'other'
    
    def process_sample_data(self, sample_data: Dict) -> Dict[str, Any]:
        """
        处理示例数据（用于演示）
        
        Args:
            sample_data: 示例数据
            
        Returns:
            处理结果
        """
        results = {
            'original_data': sample_data,
            'processed_data': {},
            'statistics': {}
        }
        
        for key, value in sample_data.items():
            if isinstance(value, list):
                # 处理列表数据
                cleaned_data = self.clean_data(value)
                stats = self.calculate_statistics(cleaned_data)
                
                results['processed_data'][key] = cleaned_data
                results['statistics'][key] = stats
        
        return results
    
    def _cache_data(self, key: str, data: Any):
        """
        缓存数据
        
        Args:
            key: 缓存键
            data: 数据
        """
        if len(self.cache) >= self.config['cache_size']:
            # 移除最旧的缓存项
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        
        self.cache[key] = data
    
    def _start_processing(self):
        """
        开始处理
        """
        if self.stats['start_time'] is None:
            self.stats['start_time'] = datetime.now()
    
    def _end_processing(self):
        """
        结束处理
        """
        self.stats['end_time'] = datetime.now()
    
    def _record_error(self, message: str, file_path: str):
        """
        记录错误
        
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
    
    def get_processing_summary(self) -> str:
        """
        获取处理摘要
        
        Returns:
            摘要字符串
        """
        duration = 0
        if self.stats['start_time'] and self.stats['end_time']:
            duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
        
        summary_lines = [
            "数据处理摘要:",
            f"处理时间: {duration:.2f} 秒",
            f"处理文件: {self.stats['files_processed']} 个",
            f"处理记录: {self.stats['records_processed']} 条",
            f"遇到错误: {self.stats['errors_encountered']} 个",
            f"缓存项目: {len(self.cache)} 个"
        ]
        
        return "\n".join(summary_lines)


# 便捷函数
def load_and_process_csv(file_path: str, config: Optional[Dict] = None) -> Tuple[List[Dict], Dict]:
    """
    加载并处理CSV文件
    
    Args:
        file_path: CSV文件路径
        config: 配置字典
        
    Returns:
        (数据, 统计信息)元组
    """
    processor = DataProcessor(config)
    data = processor.load_csv(file_path)
    cleaned_data = processor.clean_data(data)
    stats = processor.calculate_statistics(cleaned_data)
    
    return cleaned_data, stats


def quick_analyze_data(data: Any) -> str:
    """
    快速分析数据
    
    Args:
        data: 数据
        
    Returns:
        分析摘要
    """
    processor = DataProcessor()
    stats = processor.calculate_statistics(data)
    
    if isinstance(data, list) and data and isinstance(data[0], dict):
        return f"记录数: {stats['record_count']}, 字段数: {stats['field_count']}"
    elif isinstance(data, list):
        return f"行数: {stats['line_count']}, 单词数: {stats['word_count']}"
    else:
        return f"类型: {type(data).__name__}, 大小: {len(str(data))}"


# 如果直接运行此模块，进行演示
if __name__ == '__main__':
    print("=== 数据处理器演示 ===")
    
    # 创建示例数据
    sample_csv_data = [
        {'name': 'Alice', 'age': '25', 'city': 'New York'},
        {'name': 'Bob', 'age': '30', 'city': 'London'},
        {'name': 'Charlie', 'age': '35', 'city': 'Tokyo'}
    ]
    
    sample_text_data = [
        "Hello, world!",
        "This is a test.",
        "Python is awesome.",
        "",
        "Data processing is fun."
    ]
    
    processor = DataProcessor()
    
    # 演示数据清洗
    print("\n=== 数据清洗演示 ===")
    cleaned_csv = processor.clean_data(sample_csv_data)
    print(f"清洗前: {len(sample_csv_data)} 条记录")
    print(f"清洗后: {len(cleaned_csv)} 条记录")
    
    # 演示统计计算
    print("\n=== 统计信息演示 ===")
    csv_stats = processor.calculate_statistics(cleaned_csv)
    print(f"CSV统计: 记录数={csv_stats['record_count']}, 字段数={csv_stats['field_count']}")
    
    text_stats = processor.calculate_statistics(sample_text_data)
    print(f"文本统计: 行数={text_stats['line_count']}, 单词数={text_stats['word_count']}")
    
    # 演示示例数据处理
    print("\n=== 示例数据处理 ===")
    sample_data = {
        'numbers': [1, 2, 3, 4, 5],
        'texts': ['hello', 'world', 'python'],
        'files': ['test1.py', 'test2.txt', 'test3.md']
    }
    
    results = processor.process_sample_data(sample_data)
    print(f"处理结果: {len(results['processed_data'])} 个数据集")
    
    # 显示处理摘要
    print("\n=== 处理摘要 ===")
    print(processor.get_processing_summary())