#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模块化设计详细示例

本文件演示了模块化设计的各种实现方式：
1. 基础模块化设计
2. 插件系统架构
3. 微服务模块化
4. 组件化架构
5. 模块间通信机制
6. 模块生命周期管理
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable, Type
from dataclasses import dataclass
from enum import Enum
import importlib
import inspect
from datetime import datetime
import json
import threading
import time


# ============================================================================
# 1. 基础模块化设计
# ============================================================================

print("1. 基础模块化设计演示")
print("=" * 40)

# 模块接口定义
class IModule(ABC):
    """模块接口"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """模块名称"""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """模块版本"""
        pass
    
    @property
    @abstractmethod
    def dependencies(self) -> List[str]:
        """模块依赖"""
        pass
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> bool:
        """初始化模块"""
        pass
    
    @abstractmethod
    def start(self) -> bool:
        """启动模块"""
        pass
    
    @abstractmethod
    def stop(self) -> bool:
        """停止模块"""
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """获取模块状态"""
        pass

class ModuleStatus(Enum):
    """模块状态枚举"""
    UNINITIALIZED = "uninitialized"
    INITIALIZED = "initialized"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"

# 基础模块实现
class BaseModule(IModule):
    """基础模块实现"""
    
    def __init__(self, name: str, version: str, dependencies: List[str] = None):
        self._name = name
        self._version = version
        self._dependencies = dependencies or []
        self._status = ModuleStatus.UNINITIALIZED
        self._config: Dict[str, Any] = {}
        self._error_message: Optional[str] = None
        self._start_time: Optional[datetime] = None
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def version(self) -> str:
        return self._version
    
    @property
    def dependencies(self) -> List[str]:
        return self._dependencies.copy()
    
    def initialize(self, config: Dict[str, Any]) -> bool:
        """初始化模块"""
        try:
            print(f"🔧 初始化模块: {self.name} v{self.version}")
            self._config = config.copy()
            self._status = ModuleStatus.INITIALIZED
            return True
        except Exception as e:
            self._status = ModuleStatus.ERROR
            self._error_message = str(e)
            print(f"❌ 模块 {self.name} 初始化失败: {e}")
            return False
    
    def start(self) -> bool:
        """启动模块"""
        try:
            if self._status != ModuleStatus.INITIALIZED:
                raise Exception(f"模块状态错误: {self._status.value}")
            
            print(f"🚀 启动模块: {self.name}")
            self._status = ModuleStatus.STARTING
            
            # 执行启动逻辑
            self._on_start()
            
            self._status = ModuleStatus.RUNNING
            self._start_time = datetime.now()
            print(f"✅ 模块 {self.name} 启动成功")
            return True
            
        except Exception as e:
            self._status = ModuleStatus.ERROR
            self._error_message = str(e)
            print(f"❌ 模块 {self.name} 启动失败: {e}")
            return False
    
    def stop(self) -> bool:
        """停止模块"""
        try:
            if self._status != ModuleStatus.RUNNING:
                print(f"⚠️ 模块 {self.name} 未在运行状态")
                return True
            
            print(f"🛑 停止模块: {self.name}")
            self._status = ModuleStatus.STOPPING
            
            # 执行停止逻辑
            self._on_stop()
            
            self._status = ModuleStatus.STOPPED
            print(f"✅ 模块 {self.name} 停止成功")
            return True
            
        except Exception as e:
            self._status = ModuleStatus.ERROR
            self._error_message = str(e)
            print(f"❌ 模块 {self.name} 停止失败: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """获取模块状态"""
        status_info = {
            "name": self.name,
            "version": self.version,
            "status": self._status.value,
            "dependencies": self.dependencies,
            "config": self._config
        }
        
        if self._error_message:
            status_info["error"] = self._error_message
        
        if self._start_time:
            status_info["uptime"] = str(datetime.now() - self._start_time)
        
        return status_info
    
    def _on_start(self):
        """启动时的具体逻辑，子类可重写"""
        pass
    
    def _on_stop(self):
        """停止时的具体逻辑，子类可重写"""
        pass

# 具体模块实现
class DatabaseModule(BaseModule):
    """数据库模块"""
    
    def __init__(self):
        super().__init__("database", "1.0.0", [])
        self._connection = None
        self._connection_pool_size = 10
    
    def _on_start(self):
        """启动数据库连接"""
        db_config = self._config.get("database", {})
        host = db_config.get("host", "localhost")
        port = db_config.get("port", 5432)
        
        print(f"   📊 连接数据库: {host}:{port}")
        print(f"   🔗 创建连接池: {self._connection_pool_size} 个连接")
        
        # 模拟数据库连接
        self._connection = f"postgresql://{host}:{port}/app"
    
    def _on_stop(self):
        """关闭数据库连接"""
        print("   📊 关闭数据库连接")
        print("   🔗 清理连接池")
        self._connection = None
    
    def execute_query(self, query: str) -> List[Dict]:
        """执行查询"""
        if self._status != ModuleStatus.RUNNING:
            raise Exception("数据库模块未运行")
        
        print(f"   🔍 执行查询: {query[:50]}...")
        # 模拟查询结果
        return [{"id": 1, "result": "数据库查询结果"}]

class CacheModule(BaseModule):
    """缓存模块"""
    
    def __init__(self):
        super().__init__("cache", "1.0.0", [])
        self._cache_store: Dict[str, Any] = {}
        self._max_size = 1000
    
    def _on_start(self):
        """启动缓存服务"""
        cache_config = self._config.get("cache", {})
        self._max_size = cache_config.get("max_size", 1000)
        
        print(f"   💾 启动缓存服务")
        print(f"   📏 最大缓存大小: {self._max_size}")
    
    def _on_stop(self):
        """停止缓存服务"""
        print("   💾 清理缓存数据")
        self._cache_store.clear()
    
    def get(self, key: str) -> Any:
        """获取缓存"""
        if self._status != ModuleStatus.RUNNING:
            raise Exception("缓存模块未运行")
        
        value = self._cache_store.get(key)
        print(f"   🔍 缓存查询: {key} -> {'命中' if value else '未命中'}")
        return value
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        """设置缓存"""
        if self._status != ModuleStatus.RUNNING:
            raise Exception("缓存模块未运行")
        
        if len(self._cache_store) >= self._max_size:
            # 简单的LRU策略：删除第一个元素
            first_key = next(iter(self._cache_store))
            del self._cache_store[first_key]
        
        self._cache_store[key] = {
            "value": value,
            "ttl": ttl,
            "created_at": datetime.now()
        }
        print(f"   💾 缓存设置: {key}")

class LoggingModule(BaseModule):
    """日志模块"""
    
    def __init__(self):
        super().__init__("logging", "1.0.0", [])
        self._log_level = "INFO"
        self._log_file = None
    
    def _on_start(self):
        """启动日志服务"""
        log_config = self._config.get("logging", {})
        self._log_level = log_config.get("level", "INFO")
        self._log_file = log_config.get("file", "app.log")
        
        print(f"   📝 启动日志服务")
        print(f"   📊 日志级别: {self._log_level}")
        print(f"   📁 日志文件: {self._log_file}")
    
    def _on_stop(self):
        """停止日志服务"""
        print("   📝 关闭日志文件")
    
    def log(self, level: str, message: str, module: str = "app"):
        """记录日志"""
        if self._status != ModuleStatus.RUNNING:
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] [{module}] {message}"
        print(f"   📝 {log_entry}")

class WebServerModule(BaseModule):
    """Web服务器模块"""
    
    def __init__(self):
        super().__init__("webserver", "1.0.0", ["database", "cache", "logging"])
        self._host = "localhost"
        self._port = 8080
        self._routes: Dict[str, Callable] = {}
    
    def _on_start(self):
        """启动Web服务器"""
        web_config = self._config.get("webserver", {})
        self._host = web_config.get("host", "localhost")
        self._port = web_config.get("port", 8080)
        
        print(f"   🌐 启动Web服务器: {self._host}:{self._port}")
        print(f"   📡 注册路由: {len(self._routes)} 个")
    
    def _on_stop(self):
        """停止Web服务器"""
        print("   🌐 关闭Web服务器")
    
    def register_route(self, path: str, handler: Callable):
        """注册路由"""
        self._routes[path] = handler
        print(f"   📡 注册路由: {path}")
    
    def handle_request(self, path: str, method: str = "GET") -> str:
        """处理请求"""
        if self._status != ModuleStatus.RUNNING:
            return "服务器未运行"
        
        handler = self._routes.get(path)
        if handler:
            print(f"   🌐 处理请求: {method} {path}")
            return handler()
        else:
            return f"404 Not Found: {path}"

# 模块管理器
class ModuleManager:
    """模块管理器"""
    
    def __init__(self):
        self._modules: Dict[str, IModule] = {}
        self._dependency_graph: Dict[str, List[str]] = {}
        self._config: Dict[str, Any] = {}
    
    def register_module(self, module: IModule):
        """注册模块"""
        print(f"📦 注册模块: {module.name} v{module.version}")
        self._modules[module.name] = module
        self._dependency_graph[module.name] = module.dependencies
    
    def set_config(self, config: Dict[str, Any]):
        """设置配置"""
        self._config = config
    
    def _resolve_dependencies(self) -> List[str]:
        """解析依赖关系，返回启动顺序"""
        visited = set()
        temp_visited = set()
        result = []
        
        def dfs(module_name: str):
            if module_name in temp_visited:
                raise Exception(f"检测到循环依赖: {module_name}")
            
            if module_name in visited:
                return
            
            temp_visited.add(module_name)
            
            # 先启动依赖的模块
            for dep in self._dependency_graph.get(module_name, []):
                if dep not in self._modules:
                    raise Exception(f"依赖模块 '{dep}' 未注册")
                dfs(dep)
            
            temp_visited.remove(module_name)
            visited.add(module_name)
            result.append(module_name)
        
        # 对所有模块进行拓扑排序
        for module_name in self._modules:
            if module_name not in visited:
                dfs(module_name)
        
        return result
    
    def start_all(self) -> bool:
        """启动所有模块"""
        try:
            print("🚀 开始启动所有模块...")
            
            # 解析启动顺序
            start_order = self._resolve_dependencies()
            print(f"📋 启动顺序: {' -> '.join(start_order)}")
            
            # 按顺序初始化和启动模块
            for module_name in start_order:
                module = self._modules[module_name]
                
                # 初始化模块
                if not module.initialize(self._config):
                    print(f"❌ 模块 {module_name} 初始化失败")
                    return False
                
                # 启动模块
                if not module.start():
                    print(f"❌ 模块 {module_name} 启动失败")
                    return False
            
            print("✅ 所有模块启动成功")
            return True
            
        except Exception as e:
            print(f"❌ 启动失败: {e}")
            return False
    
    def stop_all(self) -> bool:
        """停止所有模块"""
        try:
            print("🛑 开始停止所有模块...")
            
            # 按相反顺序停止模块
            start_order = self._resolve_dependencies()
            stop_order = list(reversed(start_order))
            
            for module_name in stop_order:
                module = self._modules[module_name]
                module.stop()
            
            print("✅ 所有模块停止成功")
            return True
            
        except Exception as e:
            print(f"❌ 停止失败: {e}")
            return False
    
    def get_module(self, name: str) -> Optional[IModule]:
        """获取模块"""
        return self._modules.get(name)
    
    def get_status(self) -> Dict[str, Any]:
        """获取所有模块状态"""
        return {
            module_name: module.get_status()
            for module_name, module in self._modules.items()
        }

# 演示基础模块化设计
print("🔹 基础模块化设计演示:")

# 创建模块管理器
module_manager = ModuleManager()

# 注册模块
module_manager.register_module(DatabaseModule())
module_manager.register_module(CacheModule())
module_manager.register_module(LoggingModule())
module_manager.register_module(WebServerModule())

# 设置配置
config = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "myapp"
    },
    "cache": {
        "max_size": 2000
    },
    "logging": {
        "level": "DEBUG",
        "file": "myapp.log"
    },
    "webserver": {
        "host": "0.0.0.0",
        "port": 8080
    }
}
module_manager.set_config(config)

# 启动所有模块
print("\n" + "="*50)
module_manager.start_all()

# 使用模块
print("\n📊 使用模块功能:")
db_module = module_manager.get_module("database")
if db_module and isinstance(db_module, DatabaseModule):
    db_module.execute_query("SELECT * FROM users")

cache_module = module_manager.get_module("cache")
if cache_module and isinstance(cache_module, CacheModule):
    cache_module.set("user:123", {"name": "Alice", "age": 25})
    user_data = cache_module.get("user:123")

log_module = module_manager.get_module("logging")
if log_module and isinstance(log_module, LoggingModule):
    log_module.log("INFO", "应用程序启动完成", "main")

web_module = module_manager.get_module("webserver")
if web_module and isinstance(web_module, WebServerModule):
    web_module.register_route("/api/users", lambda: "用户列表")
    response = web_module.handle_request("/api/users")
    print(f"   🌐 响应: {response}")

# 显示模块状态
print("\n📊 模块状态:")
status = module_manager.get_status()
for module_name, module_status in status.items():
    print(f"   {module_name}: {module_status['status']}")

# 停止所有模块
print("\n" + "="*50)
module_manager.stop_all()

print()


# ============================================================================
# 2. 插件系统架构
# ============================================================================

print("2. 插件系统架构演示")
print("=" * 40)

# 插件接口
class IPlugin(ABC):
    """插件接口"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        pass
    
    @abstractmethod
    def install(self) -> bool:
        """安装插件"""
        pass
    
    @abstractmethod
    def uninstall(self) -> bool:
        """卸载插件"""
        pass
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Any:
        """执行插件功能"""
        pass

# 插件元数据
@dataclass
class PluginMetadata:
    """插件元数据"""
    name: str
    version: str
    description: str
    author: str
    dependencies: List[str]
    permissions: List[str]
    entry_point: str

# 具体插件实现
class EmailNotificationPlugin(IPlugin):
    """邮件通知插件"""
    
    @property
    def name(self) -> str:
        return "email_notification"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return "发送邮件通知的插件"
    
    def install(self) -> bool:
        print(f"📧 安装邮件通知插件 v{self.version}")
        print("   ✅ 配置SMTP服务器")
        print("   ✅ 注册邮件模板")
        return True
    
    def uninstall(self) -> bool:
        print(f"📧 卸载邮件通知插件")
        print("   🗑️ 清理邮件模板")
        print("   🗑️ 移除配置")
        return True
    
    def execute(self, context: Dict[str, Any]) -> Any:
        recipient = context.get("recipient")
        subject = context.get("subject")
        message = context.get("message")
        
        print(f"📧 发送邮件: {subject} -> {recipient}")
        print(f"   内容: {message[:50]}...")
        
        return {"status": "sent", "message_id": "msg_123456"}

class SMSNotificationPlugin(IPlugin):
    """短信通知插件"""
    
    @property
    def name(self) -> str:
        return "sms_notification"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return "发送短信通知的插件"
    
    def install(self) -> bool:
        print(f"📱 安装短信通知插件 v{self.version}")
        print("   ✅ 配置短信网关")
        print("   ✅ 验证API密钥")
        return True
    
    def uninstall(self) -> bool:
        print(f"📱 卸载短信通知插件")
        print("   🗑️ 清理API配置")
        return True
    
    def execute(self, context: Dict[str, Any]) -> Any:
        phone = context.get("phone")
        message = context.get("message")
        
        print(f"📱 发送短信: {message[:30]}... -> {phone}")
        
        return {"status": "sent", "sms_id": "sms_789012"}

class DataExportPlugin(IPlugin):
    """数据导出插件"""
    
    @property
    def name(self) -> str:
        return "data_export"
    
    @property
    def version(self) -> str:
        return "2.0.0"
    
    @property
    def description(self) -> str:
        return "数据导出插件，支持多种格式"
    
    def install(self) -> bool:
        print(f"📊 安装数据导出插件 v{self.version}")
        print("   ✅ 注册导出格式: CSV, JSON, Excel")
        print("   ✅ 创建临时目录")
        return True
    
    def uninstall(self) -> bool:
        print(f"📊 卸载数据导出插件")
        print("   🗑️ 清理临时文件")
        return True
    
    def execute(self, context: Dict[str, Any]) -> Any:
        data = context.get("data", [])
        format_type = context.get("format", "csv")
        filename = context.get("filename", "export")
        
        print(f"📊 导出数据: {len(data)} 条记录 -> {filename}.{format_type}")
        
        if format_type == "csv":
            print("   📄 生成CSV文件")
        elif format_type == "json":
            print("   📄 生成JSON文件")
        elif format_type == "excel":
            print("   📄 生成Excel文件")
        
        return {"status": "exported", "file_path": f"/exports/{filename}.{format_type}"}

# 插件管理器
class PluginManager:
    """插件管理器"""
    
    def __init__(self):
        self._plugins: Dict[str, IPlugin] = {}
        self._metadata: Dict[str, PluginMetadata] = {}
        self._installed_plugins: set = set()
        self._plugin_hooks: Dict[str, List[Callable]] = {}
    
    def register_plugin(self, plugin: IPlugin, metadata: PluginMetadata = None):
        """注册插件"""
        print(f"🔌 注册插件: {plugin.name} v{plugin.version}")
        self._plugins[plugin.name] = plugin
        
        if metadata:
            self._metadata[plugin.name] = metadata
        else:
            # 创建默认元数据
            self._metadata[plugin.name] = PluginMetadata(
                name=plugin.name,
                version=plugin.version,
                description=plugin.description,
                author="Unknown",
                dependencies=[],
                permissions=[],
                entry_point=plugin.__class__.__name__
            )
    
    def install_plugin(self, plugin_name: str) -> bool:
        """安装插件"""
        if plugin_name not in self._plugins:
            print(f"❌ 插件 '{plugin_name}' 未注册")
            return False
        
        if plugin_name in self._installed_plugins:
            print(f"⚠️ 插件 '{plugin_name}' 已安装")
            return True
        
        plugin = self._plugins[plugin_name]
        metadata = self._metadata[plugin_name]
        
        # 检查依赖
        for dep in metadata.dependencies:
            if dep not in self._installed_plugins:
                print(f"❌ 依赖插件 '{dep}' 未安装")
                return False
        
        # 安装插件
        if plugin.install():
            self._installed_plugins.add(plugin_name)
            print(f"✅ 插件 '{plugin_name}' 安装成功")
            return True
        else:
            print(f"❌ 插件 '{plugin_name}' 安装失败")
            return False
    
    def uninstall_plugin(self, plugin_name: str) -> bool:
        """卸载插件"""
        if plugin_name not in self._installed_plugins:
            print(f"⚠️ 插件 '{plugin_name}' 未安装")
            return True
        
        # 检查是否有其他插件依赖此插件
        dependents = []
        for name, metadata in self._metadata.items():
            if plugin_name in metadata.dependencies and name in self._installed_plugins:
                dependents.append(name)
        
        if dependents:
            print(f"❌ 无法卸载插件 '{plugin_name}'，以下插件依赖它: {', '.join(dependents)}")
            return False
        
        plugin = self._plugins[plugin_name]
        
        if plugin.uninstall():
            self._installed_plugins.remove(plugin_name)
            print(f"✅ 插件 '{plugin_name}' 卸载成功")
            return True
        else:
            print(f"❌ 插件 '{plugin_name}' 卸载失败")
            return False
    
    def execute_plugin(self, plugin_name: str, context: Dict[str, Any]) -> Any:
        """执行插件"""
        if plugin_name not in self._installed_plugins:
            raise Exception(f"插件 '{plugin_name}' 未安装")
        
        plugin = self._plugins[plugin_name]
        print(f"🔌 执行插件: {plugin_name}")
        
        try:
            result = plugin.execute(context)
            print(f"✅ 插件 '{plugin_name}' 执行成功")
            return result
        except Exception as e:
            print(f"❌ 插件 '{plugin_name}' 执行失败: {e}")
            raise
    
    def register_hook(self, hook_name: str, callback: Callable):
        """注册钩子"""
        if hook_name not in self._plugin_hooks:
            self._plugin_hooks[hook_name] = []
        self._plugin_hooks[hook_name].append(callback)
        print(f"🪝 注册钩子: {hook_name}")
    
    def trigger_hook(self, hook_name: str, *args, **kwargs):
        """触发钩子"""
        if hook_name in self._plugin_hooks:
            print(f"🪝 触发钩子: {hook_name}")
            for callback in self._plugin_hooks[hook_name]:
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    print(f"❌ 钩子回调失败: {e}")
    
    def list_plugins(self) -> Dict[str, Dict[str, Any]]:
        """列出所有插件"""
        result = {}
        for name, plugin in self._plugins.items():
            metadata = self._metadata[name]
            result[name] = {
                "name": plugin.name,
                "version": plugin.version,
                "description": plugin.description,
                "installed": name in self._installed_plugins,
                "author": metadata.author,
                "dependencies": metadata.dependencies
            }
        return result

# 演示插件系统
print("🔹 插件系统架构演示:")

# 创建插件管理器
plugin_manager = PluginManager()

# 注册插件
email_plugin = EmailNotificationPlugin()
sms_plugin = SMSNotificationPlugin()
export_plugin = DataExportPlugin()

plugin_manager.register_plugin(email_plugin)
plugin_manager.register_plugin(sms_plugin)
plugin_manager.register_plugin(export_plugin)

# 列出所有插件
print("\n📋 可用插件:")
plugins_info = plugin_manager.list_plugins()
for name, info in plugins_info.items():
    status = "已安装" if info["installed"] else "未安装"
    print(f"   {name} v{info['version']} - {info['description']} ({status})")

# 安装插件
print("\n🔧 安装插件:")
plugin_manager.install_plugin("email_notification")
plugin_manager.install_plugin("sms_notification")
plugin_manager.install_plugin("data_export")

# 使用插件
print("\n🚀 使用插件:")

# 发送邮件通知
email_result = plugin_manager.execute_plugin("email_notification", {
    "recipient": "user@example.com",
    "subject": "系统通知",
    "message": "您的订单已处理完成，请查收。"
})
print(f"   邮件结果: {email_result}")

# 发送短信通知
sms_result = plugin_manager.execute_plugin("sms_notification", {
    "phone": "+86 138 0013 8000",
    "message": "验证码: 123456，5分钟内有效。"
})
print(f"   短信结果: {sms_result}")

# 导出数据
export_result = plugin_manager.execute_plugin("data_export", {
    "data": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}],
    "format": "json",
    "filename": "users_export"
})
print(f"   导出结果: {export_result}")

# 注册和触发钩子
print("\n🪝 钩子系统演示:")

def on_user_created(user_data):
    print(f"   🪝 用户创建钩子: 新用户 {user_data['name']} 已创建")

def on_order_completed(order_data):
    print(f"   🪝 订单完成钩子: 订单 {order_data['id']} 已完成")

plugin_manager.register_hook("user_created", on_user_created)
plugin_manager.register_hook("order_completed", on_order_completed)

plugin_manager.trigger_hook("user_created", {"name": "Charlie", "email": "charlie@example.com"})
plugin_manager.trigger_hook("order_completed", {"id": "ORD001", "amount": 299.99})

print()


# ============================================================================
# 总结和对比
# ============================================================================

print("模块化设计总结")
print("=" * 50)

print("✅ 模块化设计的优点:")
print("  1. 关注点分离 - 每个模块专注特定功能")
print("  2. 可维护性强 - 模块独立开发和维护")
print("  3. 可扩展性好 - 易于添加新模块")
print("  4. 可测试性强 - 模块可独立测试")
print("  5. 代码复用 - 模块可在不同项目中复用")
print("  6. 团队协作 - 不同团队可并行开发不同模块")

print("\n📊 不同模块化方式对比:")
print("  基础模块化: 静态依赖，编译时确定")
print("  插件系统: 动态加载，运行时扩展")
print("  微服务: 独立部署，网络通信")
print("  组件化: 界面组件，可视化复用")

print("\n🎯 设计原则:")
print("  1. 单一职责 - 每个模块只负责一个功能")
print("  2. 接口隔离 - 定义清晰的模块接口")
print("  3. 依赖倒置 - 依赖抽象而非具体实现")
print("  4. 开闭原则 - 对扩展开放，对修改关闭")
print("  5. 松耦合 - 模块间依赖最小化")

print("\n🔧 实施建议:")
print("  1. 合理划分模块边界")
print("  2. 设计清晰的模块接口")
print("  3. 管理模块依赖关系")
print("  4. 实现模块生命周期管理")
print("  5. 提供配置和监控机制")
print("  6. 考虑模块的版本兼容性")