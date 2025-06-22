#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件管理器配置文件

这个文件包含了应用程序的所有配置项，包括界面设置、
文件操作参数、搜索配置等。

作者: Python教程团队
创建日期: 2024-12-22
"""

import os
from pathlib import Path

# ==================== 应用基本信息 ====================
APP_NAME = "Python文件管理器"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Python教程团队"
APP_DESCRIPTION = "基于Python的文件管理器应用"

# ==================== 路径配置 ====================
# 应用根目录
APP_ROOT = Path(__file__).parent

# 用户配置目录
USER_CONFIG_DIR = Path.home() / ".file_manager"
USER_CONFIG_DIR.mkdir(exist_ok=True)

# 配置文件路径
CONFIG_FILE = USER_CONFIG_DIR / "config.yaml"
LOG_FILE = USER_CONFIG_DIR / "app.log"
HISTORY_FILE = USER_CONFIG_DIR / "history.json"
BOOKMARKS_FILE = USER_CONFIG_DIR / "bookmarks.json"
TAGS_FILE = USER_CONFIG_DIR / "tags.json"

# 临时目录
TEMP_DIR = USER_CONFIG_DIR / "temp"
TEMP_DIR.mkdir(exist_ok=True)

# 缓存目录
CACHE_DIR = USER_CONFIG_DIR / "cache"
CACHE_DIR.mkdir(exist_ok=True)

# ==================== 界面配置 ====================
# 主窗口设置
WINDOW_CONFIG = {
    'title': APP_NAME,
    'width': 1200,
    'height': 800,
    'min_width': 800,
    'min_height': 600,
    'resizable': True,
    'center_on_screen': True
}

# 颜色主题
COLOR_THEMES = {
    'default': {
        'bg_primary': '#ffffff',
        'bg_secondary': '#f5f5f5',
        'fg_primary': '#000000',
        'fg_secondary': '#666666',
        'accent': '#0078d4',
        'success': '#107c10',
        'warning': '#ff8c00',
        'error': '#d13438',
        'border': '#cccccc'
    },
    'dark': {
        'bg_primary': '#2d2d2d',
        'bg_secondary': '#3d3d3d',
        'fg_primary': '#ffffff',
        'fg_secondary': '#cccccc',
        'accent': '#0078d4',
        'success': '#107c10',
        'warning': '#ff8c00',
        'error': '#d13438',
        'border': '#555555'
    }
}

# 字体设置
FONT_CONFIG = {
    'family': 'Microsoft YaHei UI' if os.name == 'nt' else 'DejaVu Sans',
    'size': 9,
    'monospace_family': 'Consolas' if os.name == 'nt' else 'Monaco',
    'monospace_size': 9
}

# 图标设置
ICON_CONFIG = {
    'size': 16,
    'large_size': 32,
    'use_system_icons': True,
    'icon_theme': 'default'
}

# ==================== 文件操作配置 ====================
# 文件操作设置
FILE_OPERATIONS = {
    'confirm_delete': True,
    'use_recycle_bin': True,
    'show_hidden_files': False,
    'follow_symlinks': False,
    'buffer_size': 64 * 1024,  # 64KB
    'max_file_size_preview': 10 * 1024 * 1024,  # 10MB
    'backup_before_overwrite': True
}

# 复制/移动操作
COPY_MOVE_CONFIG = {
    'chunk_size': 1024 * 1024,  # 1MB
    'show_progress': True,
    'verify_checksum': True,
    'preserve_timestamps': True,
    'preserve_permissions': True
}

# 压缩设置
COMPRESSION_CONFIG = {
    'default_format': 'zip',
    'compression_level': 6,
    'supported_formats': ['zip', 'tar', 'tar.gz', 'tar.bz2', '7z'],
    'max_extract_size': 1024 * 1024 * 1024  # 1GB
}

# ==================== 搜索配置 ====================
# 搜索引擎设置
SEARCH_CONFIG = {
    'max_results': 1000,
    'search_timeout': 30,  # 秒
    'case_sensitive': False,
    'use_regex': False,
    'search_content': False,
    'max_content_size': 1024 * 1024,  # 1MB
    'index_cache_ttl': 3600,  # 1小时
    'enable_indexing': True
}

# 文件类型过滤
FILE_TYPE_FILTERS = {
    'documents': ['.txt', '.doc', '.docx', '.pdf', '.rtf', '.odt'],
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico'],
    'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
    'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma'],
    'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
    'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h'],
    'executables': ['.exe', '.msi', '.deb', '.rpm', '.dmg', '.app']
}

# ==================== 性能配置 ====================
# 缓存设置
CACHE_CONFIG = {
    'enable_cache': True,
    'cache_size_mb': 100,
    'cache_ttl': 3600,  # 1小时
    'auto_cleanup': True,
    'cleanup_interval': 24 * 3600  # 24小时
}

# 线程池设置
THREAD_CONFIG = {
    'max_workers': 4,
    'io_workers': 2,
    'search_workers': 2,
    'timeout': 30
}

# 内存限制
MEMORY_CONFIG = {
    'max_memory_mb': 512,
    'warning_threshold': 0.8,
    'auto_gc': True,
    'gc_interval': 60  # 秒
}

# ==================== 日志配置 ====================
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}',
    'rotation': '10 MB',
    'retention': '1 week',
    'compression': 'zip',
    'backtrace': True,
    'diagnose': True
}

# ==================== 安全配置 ====================
SECURITY_CONFIG = {
    'max_path_length': 4096,
    'allowed_extensions': None,  # None表示允许所有扩展名
    'blocked_extensions': ['.exe', '.bat', '.cmd', '.scr', '.com'],
    'scan_for_malware': False,
    'quarantine_suspicious': False
}

# ==================== 网络配置 ====================
NETWORK_CONFIG = {
    'enable_network': False,
    'ftp_timeout': 30,
    'sftp_timeout': 30,
    'max_connections': 5,
    'retry_attempts': 3,
    'retry_delay': 1
}

# ==================== 插件配置 ====================
PLUGIN_CONFIG = {
    'enable_plugins': True,
    'plugin_dir': APP_ROOT / 'plugins',
    'auto_load': True,
    'sandbox_mode': True
}

# ==================== 快捷键配置 ====================
KEYBOARD_SHORTCUTS = {
    'copy': 'Ctrl+C',
    'cut': 'Ctrl+X',
    'paste': 'Ctrl+V',
    'delete': 'Delete',
    'rename': 'F2',
    'refresh': 'F5',
    'search': 'Ctrl+F',
    'new_folder': 'Ctrl+Shift+N',
    'properties': 'Alt+Enter',
    'select_all': 'Ctrl+A',
    'go_up': 'Alt+Up',
    'go_back': 'Alt+Left',
    'go_forward': 'Alt+Right',
    'toggle_hidden': 'Ctrl+H'
}

# ==================== 默认设置 ====================
DEFAULT_SETTINGS = {
    'theme': 'default',
    'language': 'zh_CN',
    'startup_path': str(Path.home()),
    'remember_window_state': True,
    'auto_save_settings': True,
    'check_updates': True,
    'send_analytics': False
}

# ==================== 文件大小单位 ====================
SIZE_UNITS = {
    'B': 1,
    'KB': 1024,
    'MB': 1024 ** 2,
    'GB': 1024 ** 3,
    'TB': 1024 ** 4,
    'PB': 1024 ** 5
}

# ==================== 文件类型图标映射 ====================
FILE_TYPE_ICONS = {
    # 文档类型
    '.txt': '📄',
    '.doc': '📄',
    '.docx': '📄',
    '.pdf': '📕',
    '.rtf': '📄',
    '.odt': '📄',
    
    # 图片类型
    '.jpg': '🖼️',
    '.jpeg': '🖼️',
    '.png': '🖼️',
    '.gif': '🖼️',
    '.bmp': '🖼️',
    '.svg': '🖼️',
    '.ico': '🖼️',
    
    # 视频类型
    '.mp4': '🎬',
    '.avi': '🎬',
    '.mkv': '🎬',
    '.mov': '🎬',
    '.wmv': '🎬',
    '.flv': '🎬',
    '.webm': '🎬',
    
    # 音频类型
    '.mp3': '🎵',
    '.wav': '🎵',
    '.flac': '🎵',
    '.aac': '🎵',
    '.ogg': '🎵',
    '.wma': '🎵',
    
    # 压缩文件
    '.zip': '📦',
    '.rar': '📦',
    '.7z': '📦',
    '.tar': '📦',
    '.gz': '📦',
    '.bz2': '📦',
    
    # 代码文件
    '.py': '🐍',
    '.js': '📜',
    '.html': '🌐',
    '.css': '🎨',
    '.java': '☕',
    '.cpp': '⚙️',
    '.c': '⚙️',
    '.h': '⚙️',
    
    # 可执行文件
    '.exe': '⚙️',
    '.msi': '📦',
    '.deb': '📦',
    '.rpm': '📦',
    '.dmg': '💿',
    '.app': '📱',
    
    # 默认图标
    'folder': '📁',
    'file': '📄',
    'unknown': '❓'
}

# ==================== 多语言支持 ====================
LANGUAGE_CONFIG = {
    'default': 'zh_CN',
    'supported': ['zh_CN', 'en_US'],
    'fallback': 'en_US'
}

# ==================== 更新配置 ====================
UPDATE_CONFIG = {
    'check_interval': 24 * 3600,  # 24小时
    'auto_download': False,
    'beta_channel': False,
    'update_url': 'https://api.github.com/repos/python-rookie/file-manager/releases'
}

# ==================== 辅助函数 ====================
def get_config_value(key_path, default=None):
    """
    获取配置值
    
    Args:
        key_path: 配置键路径，如 'window.width'
        default: 默认值
    
    Returns:
        配置值或默认值
    """
    keys = key_path.split('.')
    value = globals()
    
    try:
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return default


def format_file_size(size_bytes):
    """
    格式化文件大小
    
    Args:
        size_bytes: 文件大小（字节）
    
    Returns:
        格式化后的文件大小字符串
    """
    if size_bytes == 0:
        return "0 B"
    
    for unit, factor in reversed(list(SIZE_UNITS.items())):
        if size_bytes >= factor:
            size = size_bytes / factor
            if size >= 100:
                return f"{size:.0f} {unit}"
            elif size >= 10:
                return f"{size:.1f} {unit}"
            else:
                return f"{size:.2f} {unit}"
    
    return f"{size_bytes} B"


def get_file_icon(file_path):
    """
    获取文件图标
    
    Args:
        file_path: 文件路径
    
    Returns:
        文件图标字符
    """
    if Path(file_path).is_dir():
        return FILE_TYPE_ICONS['folder']
    
    extension = Path(file_path).suffix.lower()
    return FILE_TYPE_ICONS.get(extension, FILE_TYPE_ICONS['file'])


def is_hidden_file(file_path):
    """
    判断是否为隐藏文件
    
    Args:
        file_path: 文件路径
    
    Returns:
        是否为隐藏文件
    """
    path = Path(file_path)
    
    # Unix/Linux系统：以点开头的文件
    if path.name.startswith('.'):
        return True
    
    # Windows系统：检查隐藏属性
    if os.name == 'nt':
        try:
            import stat
            return bool(os.stat(file_path).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
        except (AttributeError, OSError):
            pass
    
    return False


if __name__ == "__main__":
    # 配置文件测试
    print(f"应用名称: {APP_NAME}")
    print(f"版本: {APP_VERSION}")
    print(f"配置目录: {USER_CONFIG_DIR}")
    print(f"窗口配置: {WINDOW_CONFIG}")
    print(f"文件大小格式化测试: {format_file_size(1536)}")
    print(f"文件图标测试: {get_file_icon('test.py')}")