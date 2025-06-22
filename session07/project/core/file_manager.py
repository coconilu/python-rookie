#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件管理器核心类

这个模块包含了文件管理器的核心逻辑，负责协调各个功能模块，
管理应用状态，处理用户操作等。

作者: Python教程团队
创建日期: 2024-12-22
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional, Callable, Any
from datetime import datetime
import threading
import queue

try:
    from loguru import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

# 导入配置
from config import (
    USER_CONFIG_DIR, HISTORY_FILE, BOOKMARKS_FILE, TAGS_FILE,
    FILE_OPERATIONS, DEFAULT_SETTINGS, CACHE_CONFIG
)


class FileManagerError(Exception):
    """文件管理器异常基类"""
    pass


class PermissionError(FileManagerError):
    """权限错误"""
    pass


class FileNotFoundError(FileManagerError):
    """文件未找到错误"""
    pass


class FileManager:
    """
    文件管理器核心类
    
    这个类是整个文件管理器应用的核心，负责：
    - 管理当前工作目录
    - 维护操作历史
    - 管理书签和标签
    - 协调各个功能模块
    - 处理事件和回调
    """
    
    def __init__(self, initial_path: Optional[str] = None):
        """
        初始化文件管理器
        
        Args:
            initial_path: 初始路径，默认为用户主目录
        """
        # 基本属性
        self._current_path = Path(initial_path or Path.home())
        self._history = []
        self._history_index = -1
        self._bookmarks = {}
        self._tags = {}
        self._settings = DEFAULT_SETTINGS.copy()
        
        # 事件系统
        self._event_handlers = {}
        self._event_queue = queue.Queue()
        
        # 缓存系统
        self._cache = {}
        self._cache_lock = threading.Lock()
        
        # 状态管理
        self._is_running = False
        self._background_tasks = []
        
        # 初始化
        self._load_data()
        self._setup_event_system()
        
        logger.info(f"文件管理器初始化完成，当前路径: {self._current_path}")
    
    @property
    def current_path(self) -> Path:
        """获取当前路径"""
        return self._current_path
    
    @current_path.setter
    def current_path(self, path: str | Path):
        """设置当前路径"""
        new_path = Path(path)
        if not new_path.exists():
            raise FileNotFoundError(f"路径不存在: {new_path}")
        if not new_path.is_dir():
            raise ValueError(f"路径不是目录: {new_path}")
        
        old_path = self._current_path
        self._current_path = new_path
        
        # 添加到历史记录
        self._add_to_history(new_path)
        
        # 触发事件
        self._emit_event('path_changed', {
            'old_path': old_path,
            'new_path': new_path
        })
        
        logger.debug(f"路径已更改: {old_path} -> {new_path}")
    
    @property
    def history(self) -> List[Path]:
        """获取历史记录"""
        return self._history.copy()
    
    @property
    def bookmarks(self) -> Dict[str, str]:
        """获取书签"""
        return self._bookmarks.copy()
    
    @property
    def tags(self) -> Dict[str, List[str]]:
        """获取标签"""
        return self._tags.copy()
    
    def start(self):
        """启动文件管理器"""
        if self._is_running:
            logger.warning("文件管理器已在运行")
            return
        
        self._is_running = True
        
        # 启动后台任务
        self._start_background_tasks()
        
        # 触发启动事件
        self._emit_event('manager_started', {})
        
        logger.info("文件管理器已启动")
    
    def stop(self):
        """停止文件管理器"""
        if not self._is_running:
            return
        
        self._is_running = False
        
        # 停止后台任务
        self._stop_background_tasks()
        
        # 保存数据
        self._save_data()
        
        # 触发停止事件
        self._emit_event('manager_stopped', {})
        
        logger.info("文件管理器已停止")
    
    def list_directory(self, path: Optional[Path] = None, 
                      show_hidden: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        列出目录内容
        
        Args:
            path: 要列出的目录路径，默认为当前路径
            show_hidden: 是否显示隐藏文件，默认使用设置
        
        Returns:
            文件和目录信息列表
        """
        target_path = path or self._current_path
        show_hidden = show_hidden if show_hidden is not None else self._settings.get('show_hidden_files', False)
        
        # 检查缓存
        cache_key = f"list_{target_path}_{show_hidden}"
        if CACHE_CONFIG['enable_cache']:
            cached_result = self._get_from_cache(cache_key)
            if cached_result:
                return cached_result
        
        try:
            items = []
            
            for item_path in target_path.iterdir():
                # 跳过隐藏文件（如果设置不显示）
                if not show_hidden and self._is_hidden_file(item_path):
                    continue
                
                try:
                    stat_info = item_path.stat()
                    
                    item_info = {
                        'name': item_path.name,
                        'path': str(item_path),
                        'is_dir': item_path.is_dir(),
                        'is_file': item_path.is_file(),
                        'is_symlink': item_path.is_symlink(),
                        'size': stat_info.st_size if item_path.is_file() else 0,
                        'modified_time': datetime.fromtimestamp(stat_info.st_mtime),
                        'created_time': datetime.fromtimestamp(stat_info.st_ctime),
                        'permissions': oct(stat_info.st_mode)[-3:],
                        'extension': item_path.suffix.lower() if item_path.is_file() else '',
                        'tags': self._get_file_tags(str(item_path))
                    }
                    
                    items.append(item_info)
                    
                except (OSError, PermissionError) as e:
                    logger.warning(f"无法获取文件信息: {item_path}, 错误: {e}")
                    continue
            
            # 排序：目录在前，然后按名称排序
            items.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
            
            # 缓存结果
            if CACHE_CONFIG['enable_cache']:
                self._add_to_cache(cache_key, items)
            
            # 触发事件
            self._emit_event('directory_listed', {
                'path': target_path,
                'items': items
            })
            
            return items
            
        except PermissionError:
            raise PermissionError(f"没有权限访问目录: {target_path}")
        except Exception as e:
            logger.error(f"列出目录失败: {target_path}, 错误: {e}")
            raise FileManagerError(f"列出目录失败: {e}")
    
    def navigate_to(self, path: str | Path):
        """导航到指定路径"""
        self.current_path = path
    
    def navigate_up(self):
        """导航到上级目录"""
        parent = self._current_path.parent
        if parent != self._current_path:  # 不是根目录
            self.current_path = parent
    
    def navigate_back(self) -> bool:
        """后退到历史记录中的上一个位置"""
        if self._history_index > 0:
            self._history_index -= 1
            self._current_path = self._history[self._history_index]
            self._emit_event('path_changed', {
                'old_path': self._current_path,
                'new_path': self._current_path
            })
            return True
        return False
    
    def navigate_forward(self) -> bool:
        """前进到历史记录中的下一个位置"""
        if self._history_index < len(self._history) - 1:
            self._history_index += 1
            self._current_path = self._history[self._history_index]
            self._emit_event('path_changed', {
                'old_path': self._current_path,
                'new_path': self._current_path
            })
            return True
        return False
    
    def add_bookmark(self, name: str, path: Optional[str] = None):
        """添加书签"""
        bookmark_path = path or str(self._current_path)
        self._bookmarks[name] = bookmark_path
        self._save_bookmarks()
        
        self._emit_event('bookmark_added', {
            'name': name,
            'path': bookmark_path
        })
        
        logger.info(f"添加书签: {name} -> {bookmark_path}")
    
    def remove_bookmark(self, name: str) -> bool:
        """删除书签"""
        if name in self._bookmarks:
            path = self._bookmarks.pop(name)
            self._save_bookmarks()
            
            self._emit_event('bookmark_removed', {
                'name': name,
                'path': path
            })
            
            logger.info(f"删除书签: {name}")
            return True
        return False
    
    def navigate_to_bookmark(self, name: str) -> bool:
        """导航到书签位置"""
        if name in self._bookmarks:
            bookmark_path = self._bookmarks[name]
            if Path(bookmark_path).exists():
                self.current_path = bookmark_path
                return True
            else:
                logger.warning(f"书签路径不存在: {bookmark_path}")
                # 可以选择删除无效书签
                self.remove_bookmark(name)
        return False
    
    def add_file_tag(self, file_path: str, tag: str):
        """为文件添加标签"""
        if file_path not in self._tags:
            self._tags[file_path] = []
        
        if tag not in self._tags[file_path]:
            self._tags[file_path].append(tag)
            self._save_tags()
            
            self._emit_event('tag_added', {
                'file_path': file_path,
                'tag': tag
            })
            
            logger.debug(f"添加标签: {file_path} -> {tag}")
    
    def remove_file_tag(self, file_path: str, tag: str) -> bool:
        """删除文件标签"""
        if file_path in self._tags and tag in self._tags[file_path]:
            self._tags[file_path].remove(tag)
            
            # 如果没有标签了，删除整个条目
            if not self._tags[file_path]:
                del self._tags[file_path]
            
            self._save_tags()
            
            self._emit_event('tag_removed', {
                'file_path': file_path,
                'tag': tag
            })
            
            logger.debug(f"删除标签: {file_path} -> {tag}")
            return True
        return False
    
    def get_files_by_tag(self, tag: str) -> List[str]:
        """根据标签获取文件列表"""
        return [file_path for file_path, tags in self._tags.items() if tag in tags]
    
    def on(self, event_name: str, handler: Callable):
        """注册事件处理器"""
        if event_name not in self._event_handlers:
            self._event_handlers[event_name] = []
        self._event_handlers[event_name].append(handler)
        
        logger.debug(f"注册事件处理器: {event_name}")
    
    def off(self, event_name: str, handler: Callable) -> bool:
        """取消注册事件处理器"""
        if event_name in self._event_handlers:
            try:
                self._event_handlers[event_name].remove(handler)
                logger.debug(f"取消注册事件处理器: {event_name}")
                return True
            except ValueError:
                pass
        return False
    
    def get_setting(self, key: str, default=None):
        """获取设置值"""
        return self._settings.get(key, default)
    
    def set_setting(self, key: str, value):
        """设置配置值"""
        old_value = self._settings.get(key)
        self._settings[key] = value
        
        self._emit_event('setting_changed', {
            'key': key,
            'old_value': old_value,
            'new_value': value
        })
        
        logger.debug(f"设置已更改: {key} = {value}")
    
    def refresh(self):
        """刷新当前目录"""
        # 清除相关缓存
        self._clear_cache_by_pattern(f"list_{self._current_path}")
        
        # 触发刷新事件
        self._emit_event('directory_refreshed', {
            'path': self._current_path
        })
        
        logger.debug(f"刷新目录: {self._current_path}")
    
    # ==================== 私有方法 ====================
    
    def _add_to_history(self, path: Path):
        """添加路径到历史记录"""
        # 如果当前不在历史记录末尾，删除后面的记录
        if self._history_index < len(self._history) - 1:
            self._history = self._history[:self._history_index + 1]
        
        # 避免重复添加相同路径
        if not self._history or self._history[-1] != path:
            self._history.append(path)
            self._history_index = len(self._history) - 1
            
            # 限制历史记录长度
            max_history = 100
            if len(self._history) > max_history:
                self._history = self._history[-max_history:]
                self._history_index = len(self._history) - 1
    
    def _is_hidden_file(self, path: Path) -> bool:
        """判断是否为隐藏文件"""
        # Unix/Linux: 以点开头
        if path.name.startswith('.'):
            return True
        
        # Windows: 检查隐藏属性
        if os.name == 'nt':
            try:
                import stat
                return bool(path.stat().st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
            except (AttributeError, OSError):
                pass
        
        return False
    
    def _get_file_tags(self, file_path: str) -> List[str]:
        """获取文件标签"""
        return self._tags.get(file_path, [])
    
    def _emit_event(self, event_name: str, data: Dict[str, Any]):
        """触发事件"""
        if event_name in self._event_handlers:
            for handler in self._event_handlers[event_name]:
                try:
                    handler(data)
                except Exception as e:
                    logger.error(f"事件处理器错误: {event_name}, {e}")
    
    def _setup_event_system(self):
        """设置事件系统"""
        # 这里可以设置事件处理的后台线程
        pass
    
    def _start_background_tasks(self):
        """启动后台任务"""
        # 这里可以启动文件监控、缓存清理等后台任务
        pass
    
    def _stop_background_tasks(self):
        """停止后台任务"""
        for task in self._background_tasks:
            if hasattr(task, 'stop'):
                task.stop()
        self._background_tasks.clear()
    
    def _get_from_cache(self, key: str):
        """从缓存获取数据"""
        with self._cache_lock:
            if key in self._cache:
                data, timestamp = self._cache[key]
                # 检查是否过期
                if datetime.now().timestamp() - timestamp < CACHE_CONFIG['cache_ttl']:
                    return data
                else:
                    del self._cache[key]
        return None
    
    def _add_to_cache(self, key: str, data):
        """添加数据到缓存"""
        with self._cache_lock:
            self._cache[key] = (data, datetime.now().timestamp())
            
            # 检查缓存大小限制
            if len(self._cache) > 1000:  # 简单的缓存大小限制
                # 删除最旧的条目
                oldest_key = min(self._cache.keys(), 
                                key=lambda k: self._cache[k][1])
                del self._cache[oldest_key]
    
    def _clear_cache_by_pattern(self, pattern: str):
        """根据模式清除缓存"""
        with self._cache_lock:
            keys_to_remove = [key for key in self._cache.keys() if pattern in key]
            for key in keys_to_remove:
                del self._cache[key]
    
    def _load_data(self):
        """加载数据"""
        self._load_bookmarks()
        self._load_tags()
        self._load_settings()
    
    def _save_data(self):
        """保存数据"""
        self._save_bookmarks()
        self._save_tags()
        self._save_settings()
    
    def _load_bookmarks(self):
        """加载书签"""
        try:
            if BOOKMARKS_FILE.exists():
                with open(BOOKMARKS_FILE, 'r', encoding='utf-8') as f:
                    self._bookmarks = json.load(f)
                logger.debug(f"加载书签: {len(self._bookmarks)} 个")
        except Exception as e:
            logger.error(f"加载书签失败: {e}")
            self._bookmarks = {}
    
    def _save_bookmarks(self):
        """保存书签"""
        try:
            with open(BOOKMARKS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self._bookmarks, f, ensure_ascii=False, indent=2)
            logger.debug("书签已保存")
        except Exception as e:
            logger.error(f"保存书签失败: {e}")
    
    def _load_tags(self):
        """加载标签"""
        try:
            if TAGS_FILE.exists():
                with open(TAGS_FILE, 'r', encoding='utf-8') as f:
                    self._tags = json.load(f)
                logger.debug(f"加载标签: {len(self._tags)} 个文件")
        except Exception as e:
            logger.error(f"加载标签失败: {e}")
            self._tags = {}
    
    def _save_tags(self):
        """保存标签"""
        try:
            with open(TAGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self._tags, f, ensure_ascii=False, indent=2)
            logger.debug("标签已保存")
        except Exception as e:
            logger.error(f"保存标签失败: {e}")
    
    def _load_settings(self):
        """加载设置"""
        # 这里可以从配置文件加载设置
        pass
    
    def _save_settings(self):
        """保存设置"""
        # 这里可以保存设置到配置文件
        pass
    
    def __enter__(self):
        """上下文管理器入口"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.stop()
    
    def __repr__(self):
        return f"FileManager(current_path='{self._current_path}')"