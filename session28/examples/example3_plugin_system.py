#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session28 示例3：插件系统架构详解

本示例展示了可扩展插件系统的设计和实现。

作者: Python教程团队
创建日期: 2024-01-15
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Type, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import importlib
import inspect
import json
import os
import sys
from pathlib import Path


# ============================================================================
# 1. 插件基础设施
# ============================================================================

class PluginStatus(Enum):
    """插件状态"""
    UNLOADED = "unloaded"
    LOADED = "loaded"
    ACTIVE = "active"
    ERROR = "error"
    DISABLED = "disabled"


@dataclass
class PluginInfo:
    """插件信息"""
    name: str
    version: str
    description: str
    author: str
    dependencies: List[str] = field(default_factory=list)
    min_app_version: str = "1.0.0"
    max_app_version: str = "999.0.0"
    enabled: bool = True
    priority: int = 100  # 数字越小优先级越高
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'author': self.author,
            'dependencies': self.dependencies,
            'min_app_version': self.min_app_version,
            'max_app_version': self.max_app_version,
            'enabled': self.enabled,
            'priority': self.priority
        }


class PluginInterface(ABC):
    """插件接口"""
    
    @abstractmethod
    def get_info(self) -> PluginInfo:
        """获取插件信息"""
        pass
    
    @abstractmethod
    def initialize(self, context: 'PluginContext') -> bool:
        """初始化插件"""
        pass
    
    @abstractmethod
    def activate(self) -> bool:
        """激活插件"""
        pass
    
    @abstractmethod
    def deactivate(self) -> bool:
        """停用插件"""
        pass
    
    @abstractmethod
    def cleanup(self) -> bool:
        """清理插件资源"""
        pass
    
    def get_hooks(self) -> Dict[str, Callable]:
        """获取插件提供的钩子函数"""
        return {}
    
    def get_commands(self) -> Dict[str, Callable]:
        """获取插件提供的命令"""
        return {}


class PluginContext:
    """插件上下文"""
    
    def __init__(self, app_version: str = "1.0.0"):
        self.app_version = app_version
        self.shared_data: Dict[str, Any] = {}
        self.services: Dict[str, Any] = {}
        self.config: Dict[str, Any] = {}
    
    def get_service(self, service_name: str) -> Optional[Any]:
        """获取服务"""
        return self.services.get(service_name)
    
    def register_service(self, service_name: str, service: Any) -> None:
        """注册服务"""
        self.services[service_name] = service
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """获取配置"""
        return self.config.get(key, default)
    
    def set_config(self, key: str, value: Any) -> None:
        """设置配置"""
        self.config[key] = value


# ============================================================================
# 2. 插件管理器
# ============================================================================

class PluginManager:
    """插件管理器"""
    
    def __init__(self, context: PluginContext):
        self.context = context
        self.plugins: Dict[str, PluginInterface] = {}
        self.plugin_status: Dict[str, PluginStatus] = {}
        self.plugin_paths: List[str] = []
        self.hooks: Dict[str, List[Callable]] = {}
        self.commands: Dict[str, Callable] = {}
        self.load_order: List[str] = []
    
    def add_plugin_path(self, path: str) -> None:
        """添加插件搜索路径"""
        if path not in self.plugin_paths:
            self.plugin_paths.append(path)
            if path not in sys.path:
                sys.path.insert(0, path)
            print(f"📁 添加插件路径: {path}")
    
    def discover_plugins(self) -> List[str]:
        """发现插件"""
        discovered = []
        
        for plugin_path in self.plugin_paths:
            if not os.path.exists(plugin_path):
                continue
            
            for item in os.listdir(plugin_path):
                item_path = os.path.join(plugin_path, item)
                
                # 检查Python文件
                if item.endswith('.py') and not item.startswith('_'):
                    module_name = item[:-3]
                    discovered.append(module_name)
                
                # 检查包目录
                elif os.path.isdir(item_path) and not item.startswith('_'):
                    init_file = os.path.join(item_path, '__init__.py')
                    if os.path.exists(init_file):
                        discovered.append(item)
        
        print(f"🔍 发现插件: {discovered}")
        return discovered
    
    def load_plugin(self, plugin_name: str) -> bool:
        """加载插件"""
        try:
            if plugin_name in self.plugins:
                print(f"⚠️ 插件 {plugin_name} 已加载")
                return True
            
            # 动态导入插件模块
            module = importlib.import_module(plugin_name)
            
            # 查找插件类
            plugin_class = None
            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and 
                    issubclass(obj, PluginInterface) and 
                    obj != PluginInterface):
                    plugin_class = obj
                    break
            
            if not plugin_class:
                print(f"❌ 在模块 {plugin_name} 中未找到插件类")
                self.plugin_status[plugin_name] = PluginStatus.ERROR
                return False
            
            # 创建插件实例
            plugin_instance = plugin_class()
            
            # 检查依赖
            plugin_info = plugin_instance.get_info()
            if not self._check_dependencies(plugin_info):
                print(f"❌ 插件 {plugin_name} 依赖检查失败")
                self.plugin_status[plugin_name] = PluginStatus.ERROR
                return False
            
            # 初始化插件
            if not plugin_instance.initialize(self.context):
                print(f"❌ 插件 {plugin_name} 初始化失败")
                self.plugin_status[plugin_name] = PluginStatus.ERROR
                return False
            
            # 注册插件
            self.plugins[plugin_name] = plugin_instance
            self.plugin_status[plugin_name] = PluginStatus.LOADED
            
            # 注册钩子和命令
            self._register_plugin_hooks(plugin_name, plugin_instance)
            self._register_plugin_commands(plugin_name, plugin_instance)
            
            print(f"✅ 插件 {plugin_name} 加载成功")
            return True
            
        except Exception as e:
            print(f"❌ 加载插件 {plugin_name} 时发生错误: {str(e)}")
            self.plugin_status[plugin_name] = PluginStatus.ERROR
            return False
    
    def activate_plugin(self, plugin_name: str) -> bool:
        """激活插件"""
        if plugin_name not in self.plugins:
            print(f"❌ 插件 {plugin_name} 未加载")
            return False
        
        if self.plugin_status[plugin_name] == PluginStatus.ACTIVE:
            print(f"⚠️ 插件 {plugin_name} 已激活")
            return True
        
        try:
            plugin = self.plugins[plugin_name]
            if plugin.activate():
                self.plugin_status[plugin_name] = PluginStatus.ACTIVE
                print(f"✅ 插件 {plugin_name} 激活成功")
                return True
            else:
                print(f"❌ 插件 {plugin_name} 激活失败")
                return False
        except Exception as e:
            print(f"❌ 激活插件 {plugin_name} 时发生错误: {str(e)}")
            self.plugin_status[plugin_name] = PluginStatus.ERROR
            return False
    
    def deactivate_plugin(self, plugin_name: str) -> bool:
        """停用插件"""
        if plugin_name not in self.plugins:
            print(f"❌ 插件 {plugin_name} 未加载")
            return False
        
        try:
            plugin = self.plugins[plugin_name]
            if plugin.deactivate():
                self.plugin_status[plugin_name] = PluginStatus.LOADED
                print(f"✅ 插件 {plugin_name} 停用成功")
                return True
            else:
                print(f"❌ 插件 {plugin_name} 停用失败")
                return False
        except Exception as e:
            print(f"❌ 停用插件 {plugin_name} 时发生错误: {str(e)}")
            return False
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """卸载插件"""
        if plugin_name not in self.plugins:
            print(f"⚠️ 插件 {plugin_name} 未加载")
            return True
        
        try:
            # 先停用插件
            if self.plugin_status[plugin_name] == PluginStatus.ACTIVE:
                self.deactivate_plugin(plugin_name)
            
            # 清理插件资源
            plugin = self.plugins[plugin_name]
            plugin.cleanup()
            
            # 移除钩子和命令
            self._unregister_plugin_hooks(plugin_name)
            self._unregister_plugin_commands(plugin_name)
            
            # 移除插件
            del self.plugins[plugin_name]
            self.plugin_status[plugin_name] = PluginStatus.UNLOADED
            
            print(f"✅ 插件 {plugin_name} 卸载成功")
            return True
            
        except Exception as e:
            print(f"❌ 卸载插件 {plugin_name} 时发生错误: {str(e)}")
            return False
    
    def load_all_plugins(self) -> None:
        """加载所有发现的插件"""
        discovered_plugins = self.discover_plugins()
        
        # 按优先级排序
        plugin_priorities = []
        for plugin_name in discovered_plugins:
            try:
                # 临时加载以获取优先级信息
                module = importlib.import_module(plugin_name)
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, PluginInterface) and 
                        obj != PluginInterface):
                        temp_instance = obj()
                        info = temp_instance.get_info()
                        plugin_priorities.append((plugin_name, info.priority))
                        break
            except:
                plugin_priorities.append((plugin_name, 999))  # 默认最低优先级
        
        # 按优先级排序（数字越小优先级越高）
        plugin_priorities.sort(key=lambda x: x[1])
        
        # 按顺序加载插件
        for plugin_name, priority in plugin_priorities:
            self.load_plugin(plugin_name)
            self.load_order.append(plugin_name)
    
    def activate_all_plugins(self) -> None:
        """激活所有已加载的插件"""
        for plugin_name in self.load_order:
            if (plugin_name in self.plugins and 
                self.plugin_status[plugin_name] == PluginStatus.LOADED):
                self.activate_plugin(plugin_name)
    
    def execute_hook(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """执行钩子函数"""
        results = []
        if hook_name in self.hooks:
            for hook_func in self.hooks[hook_name]:
                try:
                    result = hook_func(*args, **kwargs)
                    results.append(result)
                except Exception as e:
                    print(f"❌ 执行钩子 {hook_name} 时发生错误: {str(e)}")
        return results
    
    def execute_command(self, command_name: str, *args, **kwargs) -> Any:
        """执行命令"""
        if command_name in self.commands:
            try:
                return self.commands[command_name](*args, **kwargs)
            except Exception as e:
                print(f"❌ 执行命令 {command_name} 时发生错误: {str(e)}")
                return None
        else:
            print(f"❌ 未找到命令: {command_name}")
            return None
    
    def get_plugin_info(self, plugin_name: str) -> Optional[PluginInfo]:
        """获取插件信息"""
        if plugin_name in self.plugins:
            return self.plugins[plugin_name].get_info()
        return None
    
    def list_plugins(self) -> Dict[str, Dict[str, Any]]:
        """列出所有插件"""
        result = {}
        for plugin_name, plugin in self.plugins.items():
            info = plugin.get_info()
            result[plugin_name] = {
                'info': info.to_dict(),
                'status': self.plugin_status[plugin_name].value
            }
        return result
    
    def _check_dependencies(self, plugin_info: PluginInfo) -> bool:
        """检查插件依赖"""
        for dep in plugin_info.dependencies:
            if dep not in self.plugins:
                print(f"❌ 缺少依赖插件: {dep}")
                return False
            if self.plugin_status[dep] != PluginStatus.LOADED:
                print(f"❌ 依赖插件 {dep} 未正确加载")
                return False
        return True
    
    def _register_plugin_hooks(self, plugin_name: str, plugin: PluginInterface) -> None:
        """注册插件钩子"""
        hooks = plugin.get_hooks()
        for hook_name, hook_func in hooks.items():
            if hook_name not in self.hooks:
                self.hooks[hook_name] = []
            self.hooks[hook_name].append(hook_func)
            print(f"🔗 注册钩子: {plugin_name}.{hook_name}")
    
    def _register_plugin_commands(self, plugin_name: str, plugin: PluginInterface) -> None:
        """注册插件命令"""
        commands = plugin.get_commands()
        for command_name, command_func in commands.items():
            full_command_name = f"{plugin_name}.{command_name}"
            self.commands[full_command_name] = command_func
            print(f"⚡ 注册命令: {full_command_name}")
    
    def _unregister_plugin_hooks(self, plugin_name: str) -> None:
        """取消注册插件钩子"""
        plugin = self.plugins[plugin_name]
        hooks = plugin.get_hooks()
        for hook_name, hook_func in hooks.items():
            if hook_name in self.hooks and hook_func in self.hooks[hook_name]:
                self.hooks[hook_name].remove(hook_func)
                if not self.hooks[hook_name]:  # 如果列表为空，删除键
                    del self.hooks[hook_name]
    
    def _unregister_plugin_commands(self, plugin_name: str) -> None:
        """取消注册插件命令"""
        plugin = self.plugins[plugin_name]
        commands = plugin.get_commands()
        for command_name in commands.keys():
            full_command_name = f"{plugin_name}.{command_name}"
            if full_command_name in self.commands:
                del self.commands[full_command_name]


# ============================================================================
# 3. 示例插件实现
# ============================================================================

class LoggingPlugin(PluginInterface):
    """日志插件"""
    
    def __init__(self):
        self.log_entries: List[Dict[str, Any]] = []
        self.is_active = False
    
    def get_info(self) -> PluginInfo:
        return PluginInfo(
            name="logging",
            version="1.0.0",
            description="提供日志记录功能",
            author="Plugin Team",
            priority=10  # 高优先级
        )
    
    def initialize(self, context: PluginContext) -> bool:
        print("🔧 日志插件初始化")
        context.register_service("logger", self)
        return True
    
    def activate(self) -> bool:
        print("🟢 日志插件激活")
        self.is_active = True
        return True
    
    def deactivate(self) -> bool:
        print("🔴 日志插件停用")
        self.is_active = False
        return True
    
    def cleanup(self) -> bool:
        print("🧹 日志插件清理")
        self.log_entries.clear()
        return True
    
    def get_hooks(self) -> Dict[str, Callable]:
        return {
            'before_action': self.log_before_action,
            'after_action': self.log_after_action,
            'on_error': self.log_error
        }
    
    def get_commands(self) -> Dict[str, Callable]:
        return {
            'show_logs': self.show_logs,
            'clear_logs': self.clear_logs
        }
    
    def log_before_action(self, action_name: str, *args, **kwargs) -> None:
        """动作前日志钩子"""
        if self.is_active:
            entry = {
                'timestamp': datetime.now(),
                'type': 'before_action',
                'action': action_name,
                'args': str(args),
                'kwargs': str(kwargs)
            }
            self.log_entries.append(entry)
            print(f"📝 [BEFORE] {action_name}")
    
    def log_after_action(self, action_name: str, result: Any = None) -> None:
        """动作后日志钩子"""
        if self.is_active:
            entry = {
                'timestamp': datetime.now(),
                'type': 'after_action',
                'action': action_name,
                'result': str(result)
            }
            self.log_entries.append(entry)
            print(f"📝 [AFTER] {action_name} -> {result}")
    
    def log_error(self, error_message: str, context: str = "") -> None:
        """错误日志钩子"""
        if self.is_active:
            entry = {
                'timestamp': datetime.now(),
                'type': 'error',
                'message': error_message,
                'context': context
            }
            self.log_entries.append(entry)
            print(f"📝 [ERROR] {error_message}")
    
    def show_logs(self, count: int = 10) -> List[Dict[str, Any]]:
        """显示日志命令"""
        recent_logs = self.log_entries[-count:] if count > 0 else self.log_entries
        print(f"📋 显示最近 {len(recent_logs)} 条日志:")
        for i, log in enumerate(recent_logs, 1):
            print(f"   {i}. [{log['type']}] {log.get('action', log.get('message', 'N/A'))}")
        return recent_logs
    
    def clear_logs(self) -> int:
        """清空日志命令"""
        count = len(self.log_entries)
        self.log_entries.clear()
        print(f"🗑️ 已清空 {count} 条日志")
        return count


class CachePlugin(PluginInterface):
    """缓存插件"""
    
    def __init__(self):
        self.cache: Dict[str, Any] = {}
        self.cache_stats = {'hits': 0, 'misses': 0}
        self.is_active = False
    
    def get_info(self) -> PluginInfo:
        return PluginInfo(
            name="cache",
            version="1.0.0",
            description="提供缓存功能",
            author="Plugin Team",
            dependencies=["logging"],  # 依赖日志插件
            priority=20
        )
    
    def initialize(self, context: PluginContext) -> bool:
        print("🔧 缓存插件初始化")
        context.register_service("cache", self)
        return True
    
    def activate(self) -> bool:
        print("🟢 缓存插件激活")
        self.is_active = True
        return True
    
    def deactivate(self) -> bool:
        print("🔴 缓存插件停用")
        self.is_active = False
        return True
    
    def cleanup(self) -> bool:
        print("🧹 缓存插件清理")
        self.cache.clear()
        self.cache_stats = {'hits': 0, 'misses': 0}
        return True
    
    def get_hooks(self) -> Dict[str, Callable]:
        return {
            'before_data_access': self.check_cache,
            'after_data_access': self.update_cache
        }
    
    def get_commands(self) -> Dict[str, Callable]:
        return {
            'cache_stats': self.get_cache_stats,
            'clear_cache': self.clear_cache,
            'cache_info': self.get_cache_info
        }
    
    def check_cache(self, key: str) -> Optional[Any]:
        """检查缓存钩子"""
        if not self.is_active:
            return None
        
        if key in self.cache:
            self.cache_stats['hits'] += 1
            print(f"💾 缓存命中: {key}")
            return self.cache[key]
        else:
            self.cache_stats['misses'] += 1
            print(f"💾 缓存未命中: {key}")
            return None
    
    def update_cache(self, key: str, value: Any) -> None:
        """更新缓存钩子"""
        if self.is_active:
            self.cache[key] = value
            print(f"💾 缓存更新: {key}")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计命令"""
        total = self.cache_stats['hits'] + self.cache_stats['misses']
        hit_rate = (self.cache_stats['hits'] / total * 100) if total > 0 else 0
        
        stats = {
            'hits': self.cache_stats['hits'],
            'misses': self.cache_stats['misses'],
            'total_requests': total,
            'hit_rate': f"{hit_rate:.2f}%",
            'cache_size': len(self.cache)
        }
        
        print(f"📊 缓存统计: {stats}")
        return stats
    
    def clear_cache(self) -> int:
        """清空缓存命令"""
        count = len(self.cache)
        self.cache.clear()
        print(f"🗑️ 已清空 {count} 个缓存项")
        return count
    
    def get_cache_info(self) -> Dict[str, Any]:
        """获取缓存信息命令"""
        info = {
            'cache_keys': list(self.cache.keys()),
            'cache_size': len(self.cache),
            'is_active': self.is_active
        }
        print(f"ℹ️ 缓存信息: {len(self.cache)} 个缓存项")
        return info


class MetricsPlugin(PluginInterface):
    """指标插件"""
    
    def __init__(self):
        self.metrics: Dict[str, int] = {}
        self.is_active = False
    
    def get_info(self) -> PluginInfo:
        return PluginInfo(
            name="metrics",
            version="1.0.0",
            description="提供指标收集功能",
            author="Plugin Team",
            priority=30
        )
    
    def initialize(self, context: PluginContext) -> bool:
        print("🔧 指标插件初始化")
        context.register_service("metrics", self)
        return True
    
    def activate(self) -> bool:
        print("🟢 指标插件激活")
        self.is_active = True
        return True
    
    def deactivate(self) -> bool:
        print("🔴 指标插件停用")
        self.is_active = False
        return True
    
    def cleanup(self) -> bool:
        print("🧹 指标插件清理")
        self.metrics.clear()
        return True
    
    def get_hooks(self) -> Dict[str, Callable]:
        return {
            'after_action': self.collect_action_metric,
            'on_error': self.collect_error_metric
        }
    
    def get_commands(self) -> Dict[str, Callable]:
        return {
            'show_metrics': self.show_metrics,
            'reset_metrics': self.reset_metrics
        }
    
    def collect_action_metric(self, action_name: str, result: Any = None) -> None:
        """收集动作指标钩子"""
        if self.is_active:
            metric_key = f"action.{action_name}"
            self.metrics[metric_key] = self.metrics.get(metric_key, 0) + 1
            print(f"📊 指标收集: {metric_key} = {self.metrics[metric_key]}")
    
    def collect_error_metric(self, error_message: str, context: str = "") -> None:
        """收集错误指标钩子"""
        if self.is_active:
            metric_key = "errors.total"
            self.metrics[metric_key] = self.metrics.get(metric_key, 0) + 1
            print(f"📊 错误指标: {metric_key} = {self.metrics[metric_key]}")
    
    def show_metrics(self) -> Dict[str, int]:
        """显示指标命令"""
        print(f"📊 当前指标:")
        for metric, value in self.metrics.items():
            print(f"   {metric}: {value}")
        return self.metrics.copy()
    
    def reset_metrics(self) -> int:
        """重置指标命令"""
        count = len(self.metrics)
        self.metrics.clear()
        print(f"🔄 已重置 {count} 个指标")
        return count


# ============================================================================
# 4. 应用程序示例
# ============================================================================

class Application:
    """示例应用程序"""
    
    def __init__(self):
        self.context = PluginContext("1.0.0")
        self.plugin_manager = PluginManager(self.context)
        self.data_store: Dict[str, Any] = {}
    
    def initialize(self) -> None:
        """初始化应用程序"""
        print("🚀 应用程序初始化")
        
        # 注册内置插件类（模拟从文件加载）
        self._register_builtin_plugins()
        
        # 加载并激活所有插件
        self.plugin_manager.load_all_plugins()
        self.plugin_manager.activate_all_plugins()
    
    def _register_builtin_plugins(self) -> None:
        """注册内置插件（模拟插件发现）"""
        # 在实际应用中，这些插件会从文件系统加载
        import sys
        
        # 创建模拟的插件模块
        logging_module = type(sys)('logging_plugin')
        logging_module.LoggingPlugin = LoggingPlugin
        sys.modules['logging_plugin'] = logging_module
        
        cache_module = type(sys)('cache_plugin')
        cache_module.CachePlugin = CachePlugin
        sys.modules['cache_plugin'] = cache_module
        
        metrics_module = type(sys)('metrics_plugin')
        metrics_module.MetricsPlugin = MetricsPlugin
        sys.modules['metrics_plugin'] = metrics_module
        
        # 模拟插件发现
        self.plugin_manager.plugin_paths = ['.']
        self.plugin_manager.discover_plugins = lambda: ['logging_plugin', 'cache_plugin', 'metrics_plugin']
    
    def perform_action(self, action_name: str, *args, **kwargs) -> Any:
        """执行动作（带插件钩子）"""
        # 执行前置钩子
        self.plugin_manager.execute_hook('before_action', action_name, *args, **kwargs)
        
        try:
            # 执行实际动作
            result = self._execute_action(action_name, *args, **kwargs)
            
            # 执行后置钩子
            self.plugin_manager.execute_hook('after_action', action_name, result)
            
            return result
            
        except Exception as e:
            # 执行错误钩子
            self.plugin_manager.execute_hook('on_error', str(e), action_name)
            raise
    
    def _execute_action(self, action_name: str, *args, **kwargs) -> Any:
        """执行具体动作"""
        if action_name == "store_data":
            return self._store_data(*args, **kwargs)
        elif action_name == "get_data":
            return self._get_data(*args, **kwargs)
        elif action_name == "calculate":
            return self._calculate(*args, **kwargs)
        else:
            raise ValueError(f"未知动作: {action_name}")
    
    def _store_data(self, key: str, value: Any) -> bool:
        """存储数据"""
        self.data_store[key] = value
        
        # 触发缓存更新钩子
        self.plugin_manager.execute_hook('after_data_access', key, value)
        
        print(f"💾 数据已存储: {key} = {value}")
        return True
    
    def _get_data(self, key: str) -> Any:
        """获取数据"""
        # 检查缓存钩子
        cache_results = self.plugin_manager.execute_hook('before_data_access', key)
        for result in cache_results:
            if result is not None:
                return result
        
        # 从数据存储获取
        value = self.data_store.get(key)
        if value is not None:
            # 触发缓存更新钩子
            self.plugin_manager.execute_hook('after_data_access', key, value)
        
        print(f"📖 数据获取: {key} = {value}")
        return value
    
    def _calculate(self, operation: str, a: float, b: float) -> float:
        """执行计算"""
        if operation == "add":
            result = a + b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            if b == 0:
                raise ValueError("除数不能为零")
            result = a / b
        else:
            raise ValueError(f"不支持的操作: {operation}")
        
        print(f"🧮 计算结果: {a} {operation} {b} = {result}")
        return result
    
    def execute_plugin_command(self, command: str, *args, **kwargs) -> Any:
        """执行插件命令"""
        return self.plugin_manager.execute_command(command, *args, **kwargs)
    
    def show_plugin_status(self) -> None:
        """显示插件状态"""
        print("\n📋 插件状态:")
        plugins_info = self.plugin_manager.list_plugins()
        for plugin_name, info in plugins_info.items():
            status = info['status']
            version = info['info']['version']
            description = info['info']['description']
            print(f"   {plugin_name} v{version} [{status}] - {description}")


# ============================================================================
# 5. 演示函数
# ============================================================================

def demo_plugin_system():
    """演示插件系统"""
    print("插件系统架构演示")
    print("=" * 50)
    
    # 1. 创建应用程序
    print("\n1. 创建应用程序")
    app = Application()
    app.initialize()
    
    # 2. 显示插件状态
    print("\n2. 插件状态")
    app.show_plugin_status()
    
    # 3. 执行带钩子的操作
    print("\n3. 执行操作（观察插件钩子）")
    
    # 存储数据
    print("\n--- 存储数据 ---")
    app.perform_action("store_data", "user:123", {"name": "Alice", "age": 30})
    app.perform_action("store_data", "user:456", {"name": "Bob", "age": 25})
    
    # 获取数据（第一次从存储获取，第二次从缓存获取）
    print("\n--- 获取数据 ---")
    app.perform_action("get_data", "user:123")  # 缓存未命中
    app.perform_action("get_data", "user:123")  # 缓存命中
    
    # 执行计算
    print("\n--- 执行计算 ---")
    app.perform_action("calculate", "add", 10, 20)
    app.perform_action("calculate", "multiply", 5, 6)
    
    # 触发错误
    print("\n--- 触发错误 ---")
    try:
        app.perform_action("calculate", "divide", 10, 0)
    except ValueError as e:
        print(f"捕获错误: {e}")
    
    # 4. 执行插件命令
    print("\n4. 执行插件命令")
    
    # 显示日志
    print("\n--- 显示日志 ---")
    app.execute_plugin_command("logging_plugin.show_logs", 5)
    
    # 显示缓存统计
    print("\n--- 缓存统计 ---")
    app.execute_plugin_command("cache_plugin.cache_stats")
    
    # 显示指标
    print("\n--- 显示指标 ---")
    app.execute_plugin_command("metrics_plugin.show_metrics")
    
    # 5. 插件管理操作
    print("\n5. 插件管理操作")
    
    # 停用缓存插件
    print("\n--- 停用缓存插件 ---")
    app.plugin_manager.deactivate_plugin("cache_plugin")
    
    # 再次获取数据（缓存已停用）
    print("\n--- 缓存停用后获取数据 ---")
    app.perform_action("get_data", "user:456")
    
    # 重新激活缓存插件
    print("\n--- 重新激活缓存插件 ---")
    app.plugin_manager.activate_plugin("cache_plugin")
    
    # 6. 最终状态
    print("\n6. 最终状态")
    app.show_plugin_status()
    
    # 显示可用的钩子和命令
    print(f"\n📎 可用钩子: {list(app.plugin_manager.hooks.keys())}")
    print(f"⚡ 可用命令: {list(app.plugin_manager.commands.keys())}")
    
    print("\n演示完成！")


if __name__ == "__main__":
    demo_plugin_system()