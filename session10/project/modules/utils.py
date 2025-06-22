#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session10 项目：工具模块

这个模块提供各种实用工具函数，包括：
- 文件和路径操作
- 字符串处理
- 数据验证
- 时间和日期处理
- 系统信息获取
- 配置管理
- 日志记录
- 性能监控

作者：Python学习教程
版本：1.0.0
"""

import os
import sys
import time
import json
import hashlib
import platform
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Tuple, Callable
from datetime import datetime, timedelta
from functools import wraps
from collections import defaultdict
import re
import logging
from contextlib import contextmanager

# 尝试导入可选依赖
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


class Timer:
    """
    计时器类，用于性能监控
    """
    
    def __init__(self, name: str = "Timer"):
        self.name = name
        self.start_time = None
        self.end_time = None
        self.elapsed_time = None
    
    def start(self):
        """开始计时"""
        self.start_time = time.time()
        return self
    
    def stop(self):
        """停止计时"""
        if self.start_time is None:
            raise ValueError("计时器尚未启动")
        
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time
        return self.elapsed_time
    
    def __enter__(self):
        """上下文管理器入口"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.stop()
        print(f"{self.name}: {self.elapsed_time:.4f} 秒")
    
    def get_elapsed(self) -> float:
        """获取已用时间"""
        if self.elapsed_time is not None:
            return self.elapsed_time
        elif self.start_time is not None:
            return time.time() - self.start_time
        else:
            return 0.0


class Logger:
    """
    日志记录器类
    """
    
    def __init__(self, name: str = "Utils", level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # 避免重复添加处理器
        if not self.logger.handlers:
            # 控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # 格式化器
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)
            
            self.logger.addHandler(console_handler)
    
    def debug(self, message: str):
        """调试日志"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """信息日志"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """警告日志"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """错误日志"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """严重错误日志"""
        self.logger.critical(message)


# 全局日志记录器
logger = Logger()


# 装饰器函数
def timing_decorator(func: Callable) -> Callable:
    """
    计时装饰器
    
    Args:
        func: 被装饰的函数
        
    Returns:
        装饰后的函数
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        with Timer(f"{func.__name__}"):
            return func(*args, **kwargs)
    return wrapper


def retry_decorator(max_attempts: int = 3, delay: float = 1.0, exceptions: Tuple = (Exception,)):
    """
    重试装饰器
    
    Args:
        max_attempts: 最大尝试次数
        delay: 重试间隔（秒）
        exceptions: 需要重试的异常类型
        
    Returns:
        装饰器函数
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(f"{func.__name__} 第{attempt + 1}次尝试失败: {e}")
                        time.sleep(delay)
                    else:
                        logger.error(f"{func.__name__} 所有尝试都失败了")
            
            raise last_exception
        return wrapper
    return decorator


def cache_decorator(max_size: int = 128):
    """
    简单的缓存装饰器
    
    Args:
        max_size: 缓存最大大小
        
    Returns:
        装饰器函数
    """
    def decorator(func: Callable) -> Callable:
        cache = {}
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 创建缓存键
            key = str(args) + str(sorted(kwargs.items()))
            
            if key in cache:
                return cache[key]
            
            # 如果缓存已满，删除最旧的项
            if len(cache) >= max_size:
                oldest_key = next(iter(cache))
                del cache[oldest_key]
            
            result = func(*args, **kwargs)
            cache[key] = result
            return result
        
        wrapper.cache_clear = lambda: cache.clear()
        wrapper.cache_info = lambda: {'size': len(cache), 'max_size': max_size}
        
        return wrapper
    return decorator


# 文件和路径工具
class PathUtils:
    """
    路径工具类
    """
    
    @staticmethod
    def ensure_dir(path: Union[str, Path]) -> Path:
        """
        确保目录存在
        
        Args:
            path: 目录路径
            
        Returns:
            Path对象
        """
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @staticmethod
    def get_file_info(file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        获取文件信息
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件信息字典
        """
        path = Path(file_path)
        
        if not path.exists():
            return {'exists': False}
        
        stat = path.stat()
        
        return {
            'exists': True,
            'name': path.name,
            'stem': path.stem,
            'suffix': path.suffix,
            'size': stat.st_size,
            'created': datetime.fromtimestamp(stat.st_ctime),
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'accessed': datetime.fromtimestamp(stat.st_atime),
            'is_file': path.is_file(),
            'is_dir': path.is_dir(),
            'is_symlink': path.is_symlink(),
            'parent': str(path.parent),
            'absolute_path': str(path.absolute())
        }
    
    @staticmethod
    def find_files(directory: Union[str, Path], pattern: str = "*", recursive: bool = True) -> List[Path]:
        """
        查找文件
        
        Args:
            directory: 搜索目录
            pattern: 文件模式
            recursive: 是否递归搜索
            
        Returns:
            文件路径列表
        """
        directory = Path(directory)
        
        if not directory.exists():
            return []
        
        if recursive:
            return list(directory.rglob(pattern))
        else:
            return list(directory.glob(pattern))
    
    @staticmethod
    def get_directory_size(directory: Union[str, Path]) -> int:
        """
        获取目录大小
        
        Args:
            directory: 目录路径
            
        Returns:
            目录大小（字节）
        """
        directory = Path(directory)
        total_size = 0
        
        try:
            for file_path in directory.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        except (OSError, PermissionError) as e:
            logger.warning(f"计算目录大小时出错: {e}")
        
        return total_size
    
    @staticmethod
    def clean_filename(filename: str) -> str:
        """
        清理文件名，移除非法字符
        
        Args:
            filename: 原始文件名
            
        Returns:
            清理后的文件名
        """
        # 移除或替换非法字符
        illegal_chars = r'[<>:"/\\|?*]'
        cleaned = re.sub(illegal_chars, '_', filename)
        
        # 移除前后空格和点
        cleaned = cleaned.strip(' .')
        
        # 确保不为空
        if not cleaned:
            cleaned = 'unnamed'
        
        return cleaned
    
    @staticmethod
    def get_relative_path(path: Union[str, Path], base: Union[str, Path]) -> str:
        """
        获取相对路径
        
        Args:
            path: 目标路径
            base: 基础路径
            
        Returns:
            相对路径字符串
        """
        try:
            return str(Path(path).relative_to(Path(base)))
        except ValueError:
            return str(Path(path).absolute())


# 字符串工具
class StringUtils:
    """
    字符串工具类
    """
    
    @staticmethod
    def truncate(text: str, max_length: int, suffix: str = "...") -> str:
        """
        截断字符串
        
        Args:
            text: 原始文本
            max_length: 最大长度
            suffix: 后缀
            
        Returns:
            截断后的文本
        """
        if len(text) <= max_length:
            return text
        
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """
        规范化空白字符
        
        Args:
            text: 原始文本
            
        Returns:
            规范化后的文本
        """
        # 替换多个空白字符为单个空格
        return re.sub(r'\s+', ' ', text.strip())
    
    @staticmethod
    def extract_numbers(text: str) -> List[float]:
        """
        从文本中提取数字
        
        Args:
            text: 文本
            
        Returns:
            数字列表
        """
        pattern = r'-?\d+(?:\.\d+)?'
        matches = re.findall(pattern, text)
        return [float(match) for match in matches]
    
    @staticmethod
    def camel_to_snake(text: str) -> str:
        """
        驼峰命名转下划线命名
        
        Args:
            text: 驼峰命名文本
            
        Returns:
            下划线命名文本
        """
        # 在大写字母前插入下划线
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    @staticmethod
    def snake_to_camel(text: str, capitalize_first: bool = False) -> str:
        """
        下划线命名转驼峰命名
        
        Args:
            text: 下划线命名文本
            capitalize_first: 是否首字母大写
            
        Returns:
            驼峰命名文本
        """
        components = text.split('_')
        if capitalize_first:
            return ''.join(word.capitalize() for word in components)
        else:
            return components[0] + ''.join(word.capitalize() for word in components[1:])
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        验证邮箱格式
        
        Args:
            email: 邮箱地址
            
        Returns:
            是否有效
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def generate_slug(text: str) -> str:
        """
        生成URL友好的slug
        
        Args:
            text: 原始文本
            
        Returns:
            slug字符串
        """
        # 转换为小写
        text = text.lower()
        
        # 替换空格和特殊字符为连字符
        text = re.sub(r'[^a-z0-9]+', '-', text)
        
        # 移除前后的连字符
        text = text.strip('-')
        
        return text


# 数据验证工具
class ValidationUtils:
    """
    数据验证工具类
    """
    
    @staticmethod
    def validate_required_fields(data: Dict, required_fields: List[str]) -> Tuple[bool, List[str]]:
        """
        验证必需字段
        
        Args:
            data: 数据字典
            required_fields: 必需字段列表
            
        Returns:
            (是否有效, 缺失字段列表)
        """
        missing_fields = []
        
        for field in required_fields:
            if field not in data or data[field] is None or data[field] == '':
                missing_fields.append(field)
        
        return len(missing_fields) == 0, missing_fields
    
    @staticmethod
    def validate_data_types(data: Dict, type_mapping: Dict[str, type]) -> Tuple[bool, List[str]]:
        """
        验证数据类型
        
        Args:
            data: 数据字典
            type_mapping: 字段类型映射
            
        Returns:
            (是否有效, 错误信息列表)
        """
        errors = []
        
        for field, expected_type in type_mapping.items():
            if field in data:
                value = data[field]
                if value is not None and not isinstance(value, expected_type):
                    errors.append(f"字段 '{field}' 应该是 {expected_type.__name__} 类型，实际是 {type(value).__name__}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_range(value: Union[int, float], min_val: Optional[Union[int, float]] = None, 
                      max_val: Optional[Union[int, float]] = None) -> bool:
        """
        验证数值范围
        
        Args:
            value: 数值
            min_val: 最小值
            max_val: 最大值
            
        Returns:
            是否在范围内
        """
        if min_val is not None and value < min_val:
            return False
        
        if max_val is not None and value > max_val:
            return False
        
        return True
    
    @staticmethod
    def validate_length(text: str, min_length: Optional[int] = None, 
                       max_length: Optional[int] = None) -> bool:
        """
        验证字符串长度
        
        Args:
            text: 文本
            min_length: 最小长度
            max_length: 最大长度
            
        Returns:
            是否符合长度要求
        """
        length = len(text)
        
        if min_length is not None and length < min_length:
            return False
        
        if max_length is not None and length > max_length:
            return False
        
        return True


# 时间和日期工具
class DateTimeUtils:
    """
    时间和日期工具类
    """
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """
        格式化持续时间
        
        Args:
            seconds: 秒数
            
        Returns:
            格式化的时间字符串
        """
        if seconds < 60:
            return f"{seconds:.2f} 秒"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f} 分钟"
        else:
            hours = seconds / 3600
            return f"{hours:.1f} 小时"
    
    @staticmethod
    def parse_date_string(date_string: str, formats: Optional[List[str]] = None) -> Optional[datetime]:
        """
        解析日期字符串
        
        Args:
            date_string: 日期字符串
            formats: 尝试的格式列表
            
        Returns:
            datetime对象或None
        """
        if formats is None:
            formats = [
                '%Y-%m-%d',
                '%Y-%m-%d %H:%M:%S',
                '%Y/%m/%d',
                '%Y/%m/%d %H:%M:%S',
                '%d-%m-%Y',
                '%d/%m/%Y',
                '%m-%d-%Y',
                '%m/%d/%Y'
            ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_string, fmt)
            except ValueError:
                continue
        
        return None
    
    @staticmethod
    def get_time_ago(dt: datetime) -> str:
        """
        获取相对时间描述
        
        Args:
            dt: datetime对象
            
        Returns:
            相对时间字符串
        """
        now = datetime.now()
        diff = now - dt
        
        if diff.days > 0:
            return f"{diff.days} 天前"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} 小时前"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} 分钟前"
        else:
            return "刚刚"
    
    @staticmethod
    def is_business_day(dt: datetime) -> bool:
        """
        判断是否为工作日
        
        Args:
            dt: datetime对象
            
        Returns:
            是否为工作日
        """
        return dt.weekday() < 5  # 0-4 是周一到周五
    
    @staticmethod
    def get_next_business_day(dt: datetime) -> datetime:
        """
        获取下一个工作日
        
        Args:
            dt: datetime对象
            
        Returns:
            下一个工作日
        """
        next_day = dt + timedelta(days=1)
        
        while not DateTimeUtils.is_business_day(next_day):
            next_day += timedelta(days=1)
        
        return next_day


# 系统信息工具
class SystemUtils:
    """
    系统信息工具类
    """
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """
        获取系统信息
        
        Returns:
            系统信息字典
        """
        info = {
            'platform': platform.platform(),
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'python_implementation': platform.python_implementation()
        }
        
        # 如果有psutil，添加更多信息
        if HAS_PSUTIL:
            try:
                info.update({
                    'cpu_count': psutil.cpu_count(),
                    'cpu_percent': psutil.cpu_percent(interval=1),
                    'memory_total': psutil.virtual_memory().total,
                    'memory_available': psutil.virtual_memory().available,
                    'memory_percent': psutil.virtual_memory().percent,
                    'disk_usage': psutil.disk_usage('/').percent if platform.system() != 'Windows' else psutil.disk_usage('C:\\').percent
                })
            except Exception as e:
                logger.warning(f"获取系统信息时出错: {e}")
        
        return info
    
    @staticmethod
    def get_python_packages() -> List[Dict[str, str]]:
        """
        获取已安装的Python包
        
        Returns:
            包信息列表
        """
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'list', '--format=json'],
                capture_output=True,
                text=True,
                check=True
            )
            
            packages = json.loads(result.stdout)
            return packages
            
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            logger.warning(f"获取Python包信息失败: {e}")
            return []
    
    @staticmethod
    def check_internet_connection(url: str = "https://www.google.com", timeout: int = 5) -> bool:
        """
        检查网络连接
        
        Args:
            url: 测试URL
            timeout: 超时时间
            
        Returns:
            是否连接成功
        """
        if not HAS_REQUESTS:
            logger.warning("requests库未安装，无法检查网络连接")
            return False
        
        try:
            response = requests.get(url, timeout=timeout)
            return response.status_code == 200
        except Exception:
            return False
    
    @staticmethod
    def get_environment_variables() -> Dict[str, str]:
        """
        获取环境变量
        
        Returns:
            环境变量字典
        """
        return dict(os.environ)


# 配置管理工具
class ConfigManager:
    """
    配置管理器
    """
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file
        self.config = {}
        
        if config_file and Path(config_file).exists():
            self.load_config()
    
    def load_config(self, config_file: Optional[str] = None) -> Dict:
        """
        加载配置文件
        
        Args:
            config_file: 配置文件路径
            
        Returns:
            配置字典
        """
        if config_file:
            self.config_file = config_file
        
        if not self.config_file or not Path(self.config_file).exists():
            return {}
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                if self.config_file.endswith('.json'):
                    self.config = json.load(f)
                else:
                    # 简单的键值对格式
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if '=' in line:
                                key, value = line.split('=', 1)
                                self.config[key.strip()] = value.strip()
            
            logger.info(f"配置文件加载成功: {self.config_file}")
            
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
        
        return self.config
    
    def save_config(self, config_file: Optional[str] = None):
        """
        保存配置文件
        
        Args:
            config_file: 配置文件路径
        """
        if config_file:
            self.config_file = config_file
        
        if not self.config_file:
            raise ValueError("未指定配置文件路径")
        
        try:
            # 确保目录存在
            Path(self.config_file).parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                if self.config_file.endswith('.json'):
                    json.dump(self.config, f, ensure_ascii=False, indent=2)
                else:
                    for key, value in self.config.items():
                        f.write(f"{key}={value}\n")
            
            logger.info(f"配置文件保存成功: {self.config_file}")
            
        except Exception as e:
            logger.error(f"保存配置文件失败: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键
            default: 默认值
            
        Returns:
            配置值
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """
        设置配置值
        
        Args:
            key: 配置键
            value: 配置值
        """
        self.config[key] = value
    
    def update(self, new_config: Dict):
        """
        更新配置
        
        Args:
            new_config: 新配置字典
        """
        self.config.update(new_config)


# 哈希和加密工具
class HashUtils:
    """
    哈希工具类
    """
    
    @staticmethod
    def md5_hash(text: str) -> str:
        """
        计算MD5哈希
        
        Args:
            text: 文本
            
        Returns:
            MD5哈希值
        """
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    @staticmethod
    def sha256_hash(text: str) -> str:
        """
        计算SHA256哈希
        
        Args:
            text: 文本
            
        Returns:
            SHA256哈希值
        """
        return hashlib.sha256(text.encode('utf-8')).hexdigest()
    
    @staticmethod
    def file_hash(file_path: Union[str, Path], algorithm: str = 'md5') -> str:
        """
        计算文件哈希
        
        Args:
            file_path: 文件路径
            algorithm: 哈希算法
            
        Returns:
            文件哈希值
        """
        hash_obj = hashlib.new(algorithm)
        
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
            
            return hash_obj.hexdigest()
            
        except Exception as e:
            logger.error(f"计算文件哈希失败: {e}")
            return ""


# 上下文管理器
@contextmanager
def change_directory(path: Union[str, Path]):
    """
    临时改变工作目录的上下文管理器
    
    Args:
        path: 目标目录
    """
    original_dir = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(original_dir)


@contextmanager
def suppress_output():
    """
    抑制输出的上下文管理器
    """
    import sys
    from io import StringIO
    
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    
    try:
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        yield
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr


# 便捷函数
def format_size(size_bytes: int) -> str:
    """
    格式化文件大小
    
    Args:
        size_bytes: 字节数
        
    Returns:
        格式化的大小字符串
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def safe_divide(a: Union[int, float], b: Union[int, float], default: Union[int, float] = 0) -> Union[int, float]:
    """
    安全除法，避免除零错误
    
    Args:
        a: 被除数
        b: 除数
        default: 默认值
        
    Returns:
        除法结果或默认值
    """
    try:
        return a / b if b != 0 else default
    except (TypeError, ZeroDivisionError):
        return default


def flatten_dict(d: Dict, parent_key: str = '', sep: str = '.') -> Dict:
    """
    扁平化嵌套字典
    
    Args:
        d: 嵌套字典
        parent_key: 父键
        sep: 分隔符
        
    Returns:
        扁平化的字典
    """
    items = []
    
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    
    return dict(items)


def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """
    将列表分块
    
    Args:
        lst: 原始列表
        chunk_size: 块大小
        
    Returns:
        分块后的列表
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def deep_merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """
    深度合并字典
    
    Args:
        dict1: 字典1
        dict2: 字典2
        
    Returns:
        合并后的字典
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result


# 如果直接运行此模块，进行演示
if __name__ == '__main__':
    print("=== 工具模块演示 ===")
    
    # 演示计时器
    print("\n=== 计时器演示 ===")
    with Timer("测试操作"):
        time.sleep(0.1)
    
    # 演示路径工具
    print("\n=== 路径工具演示 ===")
    current_file = __file__
    file_info = PathUtils.get_file_info(current_file)
    print(f"当前文件信息: {file_info['name']}, 大小: {format_size(file_info['size'])}")
    
    # 演示字符串工具
    print("\n=== 字符串工具演示 ===")
    test_text = "Hello World! This is a test."
    print(f"原文: {test_text}")
    print(f"截断: {StringUtils.truncate(test_text, 20)}")
    print(f"提取数字: {StringUtils.extract_numbers('价格是123.45元，折扣10%')}")
    
    # 演示系统信息
    print("\n=== 系统信息演示 ===")
    sys_info = SystemUtils.get_system_info()
    print(f"操作系统: {sys_info['system']} {sys_info['release']}")
    print(f"Python版本: {sys_info['python_version']}")
    
    # 演示哈希工具
    print("\n=== 哈希工具演示 ===")
    test_string = "Hello, World!"
    print(f"MD5: {HashUtils.md5_hash(test_string)}")
    print(f"SHA256: {HashUtils.sha256_hash(test_string)}")
    
    # 演示数据验证
    print("\n=== 数据验证演示 ===")
    test_data = {'name': 'Alice', 'age': 25, 'email': 'alice@example.com'}
    required_fields = ['name', 'age', 'email']
    is_valid, missing = ValidationUtils.validate_required_fields(test_data, required_fields)
    print(f"数据验证: {'通过' if is_valid else '失败'}, 缺失字段: {missing}")
    
    # 演示时间工具
    print("\n=== 时间工具演示 ===")
    past_time = datetime.now() - timedelta(hours=2, minutes=30)
    print(f"相对时间: {DateTimeUtils.get_time_ago(past_time)}")
    print(f"格式化持续时间: {DateTimeUtils.format_duration(3665)}")
    
    print("\n=== 演示完成 ===")