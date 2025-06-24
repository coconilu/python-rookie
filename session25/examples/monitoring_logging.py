#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session25 示例3：监控与日志管理

这个示例展示了如何为Python应用添加监控和日志功能。

学习目标：
1. 理解应用监控的重要性
2. 学会配置结构化日志
3. 掌握性能指标收集
4. 了解健康检查的实现
"""

import os
import sys
import time
import json
import logging
import psutil
import threading
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional


@dataclass
class SystemMetrics:
    """系统指标数据类"""
    timestamp: str
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_total_mb: float
    disk_percent: float
    disk_used_gb: float
    disk_total_gb: float
    network_sent_mb: float
    network_recv_mb: float
    process_count: int
    load_average: Optional[List[float]] = None


@dataclass
class ApplicationMetrics:
    """应用指标数据类"""
    timestamp: str
    request_count: int
    response_time_avg: float
    response_time_p95: float
    error_count: int
    active_connections: int
    memory_usage_mb: float
    cpu_usage_percent: float


class StructuredLogger:
    """结构化日志记录器"""
    
    def __init__(self, name: str, log_file: str = None, level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # 清除现有处理器
        self.logger.handlers.clear()
        
        # 创建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # 文件处理器
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def log_structured(self, level: str, message: str, **kwargs):
        """记录结构化日志"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'message': message,
            **kwargs
        }
        
        log_message = json.dumps(log_data, ensure_ascii=False)
        getattr(self.logger, level.lower())(log_message)
    
    def info(self, message: str, **kwargs):
        self.log_structured('INFO', message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        self.log_structured('WARNING', message, **kwargs)
    
    def error(self, message: str, **kwargs):
        self.log_structured('ERROR', message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        self.log_structured('DEBUG', message, **kwargs)


class SystemMonitor:
    """系统监控器"""
    
    def __init__(self, logger: StructuredLogger):
        self.logger = logger
        self.metrics_history = deque(maxlen=1000)  # 保留最近1000条记录
        self.network_baseline = self._get_network_baseline()
        
    def _get_network_baseline(self):
        """获取网络基线数据"""
        try:
            net_io = psutil.net_io_counters()
            return {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv
            }
        except:
            return {'bytes_sent': 0, 'bytes_recv': 0}
    
    def collect_metrics(self) -> SystemMetrics:
        """收集系统指标"""
        try:
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # 内存信息
            memory = psutil.virtual_memory()
            memory_used_mb = memory.used / 1024 / 1024
            memory_total_mb = memory.total / 1024 / 1024
            
            # 磁盘信息
            disk = psutil.disk_usage('/')
            disk_used_gb = disk.used / 1024 / 1024 / 1024
            disk_total_gb = disk.total / 1024 / 1024 / 1024
            
            # 网络信息
            net_io = psutil.net_io_counters()
            network_sent_mb = (net_io.bytes_sent - self.network_baseline['bytes_sent']) / 1024 / 1024
            network_recv_mb = (net_io.bytes_recv - self.network_baseline['bytes_recv']) / 1024 / 1024
            
            # 进程数量
            process_count = len(psutil.pids())
            
            # 负载平均值 (仅Linux/Mac)
            load_average = None
            if hasattr(os, 'getloadavg'):
                load_average = list(os.getloadavg())
            
            metrics = SystemMetrics(
                timestamp=datetime.now().isoformat(),
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_used_mb=memory_used_mb,
                memory_total_mb=memory_total_mb,
                disk_percent=disk.percent,
                disk_used_gb=disk_used_gb,
                disk_total_gb=disk_total_gb,
                network_sent_mb=network_sent_mb,
                network_recv_mb=network_recv_mb,
                process_count=process_count,
                load_average=load_average
            )
            
            self.metrics_history.append(metrics)
            return metrics
            
        except Exception as e:
            self.logger.error("收集系统指标失败", error=str(e))
            return None
    
    def check_system_health(self, metrics: SystemMetrics) -> Dict[str, bool]:
        """检查系统健康状态"""
        health_checks = {
            'cpu_healthy': metrics.cpu_percent < 80,
            'memory_healthy': metrics.memory_percent < 85,
            'disk_healthy': metrics.disk_percent < 90,
            'process_count_normal': metrics.process_count < 500
        }
        
        # 记录健康检查结果
        for check, status in health_checks.items():
            if not status:
                self.logger.warning(
                    f"系统健康检查失败: {check}",
                    check_name=check,
                    metric_value=getattr(metrics, check.replace('_healthy', '_percent').replace('_normal', ''))
                )
        
        return health_checks
    
    def get_metrics_summary(self, minutes: int = 5) -> Dict:
        """获取指标摘要"""
        if not self.metrics_history:
            return {}
            
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        recent_metrics = [
            m for m in self.metrics_history 
            if datetime.fromisoformat(m.timestamp) > cutoff_time
        ]
        
        if not recent_metrics:
            return {}
            
        cpu_values = [m.cpu_percent for m in recent_metrics]
        memory_values = [m.memory_percent for m in recent_metrics]
        
        return {
            'time_range_minutes': minutes,
            'sample_count': len(recent_metrics),
            'cpu': {
                'avg': sum(cpu_values) / len(cpu_values),
                'max': max(cpu_values),
                'min': min(cpu_values)
            },
            'memory': {
                'avg': sum(memory_values) / len(memory_values),
                'max': max(memory_values),
                'min': min(memory_values)
            },
            'latest': asdict(recent_metrics[-1])
        }


class ApplicationMonitor:
    """应用监控器"""
    
    def __init__(self, logger: StructuredLogger):
        self.logger = logger
        self.request_times = deque(maxlen=1000)
        self.error_count = 0
        self.request_count = 0
        self.active_connections = 0
        
    def record_request(self, response_time: float, status_code: int = 200):
        """记录请求"""
        self.request_count += 1
        self.request_times.append(response_time)
        
        if status_code >= 400:
            self.error_count += 1
            self.logger.warning(
                "请求错误",
                status_code=status_code,
                response_time=response_time
            )
        
        self.logger.debug(
            "请求记录",
            response_time=response_time,
            status_code=status_code,
            total_requests=self.request_count
        )
    
    def get_application_metrics(self) -> ApplicationMetrics:
        """获取应用指标"""
        if not self.request_times:
            response_time_avg = 0
            response_time_p95 = 0
        else:
            response_time_avg = sum(self.request_times) / len(self.request_times)
            sorted_times = sorted(self.request_times)
            p95_index = int(len(sorted_times) * 0.95)
            response_time_p95 = sorted_times[p95_index] if p95_index < len(sorted_times) else sorted_times[-1]
        
        # 获取当前进程的资源使用情况
        current_process = psutil.Process()
        memory_usage_mb = current_process.memory_info().rss / 1024 / 1024
        cpu_usage_percent = current_process.cpu_percent()
        
        return ApplicationMetrics(
            timestamp=datetime.now().isoformat(),
            request_count=self.request_count,
            response_time_avg=response_time_avg,
            response_time_p95=response_time_p95,
            error_count=self.error_count,
            active_connections=self.active_connections,
            memory_usage_mb=memory_usage_mb,
            cpu_usage_percent=cpu_usage_percent
        )


class HealthChecker:
    """健康检查器"""
    
    def __init__(self, logger: StructuredLogger):
        self.logger = logger
        self.checks = {}
        
    def register_check(self, name: str, check_func, critical: bool = False):
        """注册健康检查"""
        self.checks[name] = {
            'func': check_func,
            'critical': critical
        }
        
    def run_checks(self) -> Dict[str, any]:
        """运行所有健康检查"""
        results = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'checks': {}
        }
        
        overall_healthy = True
        
        for name, check_info in self.checks.items():
            try:
                start_time = time.time()
                check_result = check_info['func']()
                check_time = time.time() - start_time
                
                is_healthy = bool(check_result)
                results['checks'][name] = {
                    'status': 'pass' if is_healthy else 'fail',
                    'response_time': round(check_time * 1000, 2),  # 毫秒
                    'critical': check_info['critical']
                }
                
                if not is_healthy and check_info['critical']:
                    overall_healthy = False
                    
                self.logger.debug(
                    f"健康检查: {name}",
                    check_name=name,
                    status='pass' if is_healthy else 'fail',
                    response_time_ms=round(check_time * 1000, 2),
                    critical=check_info['critical']
                )
                
            except Exception as e:
                results['checks'][name] = {
                    'status': 'error',
                    'error': str(e),
                    'critical': check_info['critical']
                }
                
                if check_info['critical']:
                    overall_healthy = False
                    
                self.logger.error(
                    f"健康检查失败: {name}",
                    check_name=name,
                    error=str(e),
                    critical=check_info['critical']
                )
        
        results['status'] = 'healthy' if overall_healthy else 'unhealthy'
        return results


class MonitoringDashboard:
    """监控仪表板"""
    
    def __init__(self, system_monitor: SystemMonitor, app_monitor: ApplicationMonitor, logger: StructuredLogger):
        self.system_monitor = system_monitor
        self.app_monitor = app_monitor
        self.logger = logger
        self.running = False
        
    def start_monitoring(self, interval: int = 30):
        """开始监控"""
        self.running = True
        
        def monitor_loop():
            while self.running:
                try:
                    # 收集系统指标
                    system_metrics = self.system_monitor.collect_metrics()
                    if system_metrics:
                        health_checks = self.system_monitor.check_system_health(system_metrics)
                        
                        self.logger.info(
                            "系统指标收集",
                            cpu_percent=system_metrics.cpu_percent,
                            memory_percent=system_metrics.memory_percent,
                            disk_percent=system_metrics.disk_percent,
                            health_checks=health_checks
                        )
                    
                    # 收集应用指标
                    app_metrics = self.app_monitor.get_application_metrics()
                    self.logger.info(
                        "应用指标收集",
                        request_count=app_metrics.request_count,
                        error_count=app_metrics.error_count,
                        avg_response_time=app_metrics.response_time_avg,
                        memory_usage_mb=app_metrics.memory_usage_mb
                    )
                    
                    time.sleep(interval)
                    
                except Exception as e:
                    self.logger.error("监控循环出错", error=str(e))
                    time.sleep(interval)
        
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
        self.logger.info(f"监控已启动，间隔: {interval}秒")
        
    def stop_monitoring(self):
        """停止监控"""
        self.running = False
        self.logger.info("监控已停止")
        
    def get_dashboard_data(self) -> Dict:
        """获取仪表板数据"""
        system_summary = self.system_monitor.get_metrics_summary()
        app_metrics = self.app_monitor.get_application_metrics()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'system': system_summary,
            'application': asdict(app_metrics)
        }


def demo_health_checks():
    """演示健康检查"""
    logger = StructuredLogger("health_demo", "logs/health.log")
    health_checker = HealthChecker(logger)
    
    # 注册健康检查
    def check_disk_space():
        disk = psutil.disk_usage('/')
        return disk.percent < 90
    
    def check_memory():
        memory = psutil.virtual_memory()
        return memory.percent < 85
    
    def check_cpu():
        cpu_percent = psutil.cpu_percent(interval=1)
        return cpu_percent < 80
    
    def check_network():
        # 简单的网络检查
        try:
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except:
            return False
    
    health_checker.register_check("disk_space", check_disk_space, critical=True)
    health_checker.register_check("memory", check_memory, critical=True)
    health_checker.register_check("cpu", check_cpu, critical=False)
    health_checker.register_check("network", check_network, critical=False)
    
    # 运行健康检查
    print("🏥 运行健康检查...")
    results = health_checker.run_checks()
    
    print(f"\n📊 健康检查结果:")
    print(f"总体状态: {results['status']}")
    print(f"检查时间: {results['timestamp']}")
    print("\n详细结果:")
    
    for check_name, check_result in results['checks'].items():
        status_icon = "✅" if check_result['status'] == 'pass' else "❌" if check_result['status'] == 'fail' else "⚠️"
        critical_text = " (关键)" if check_result.get('critical') else ""
        response_time = check_result.get('response_time', 0)
        
        print(f"  {status_icon} {check_name}{critical_text}: {check_result['status']} ({response_time}ms)")
        
        if 'error' in check_result:
            print(f"    错误: {check_result['error']}")
    
    return results


def demo_monitoring():
    """演示监控功能"""
    print("📊 启动监控演示...")
    
    # 创建日志记录器
    logger = StructuredLogger("monitoring_demo", "logs/monitoring.log")
    
    # 创建监控器
    system_monitor = SystemMonitor(logger)
    app_monitor = ApplicationMonitor(logger)
    dashboard = MonitoringDashboard(system_monitor, app_monitor, logger)
    
    # 启动监控
    dashboard.start_monitoring(interval=5)
    
    try:
        # 模拟应用请求
        print("🔄 模拟应用请求...")
        for i in range(10):
            # 模拟请求处理时间
            response_time = 0.1 + (i % 3) * 0.05
            status_code = 200 if i % 10 != 9 else 500  # 10%错误率
            
            app_monitor.record_request(response_time, status_code)
            time.sleep(1)
        
        # 显示仪表板数据
        print("\n📈 仪表板数据:")
        dashboard_data = dashboard.get_dashboard_data()
        print(json.dumps(dashboard_data, indent=2, ensure_ascii=False))
        
        # 等待一段时间收集更多数据
        print("\n⏳ 等待收集更多监控数据...")
        time.sleep(10)
        
        # 显示系统指标摘要
        print("\n📊 系统指标摘要:")
        summary = system_monitor.get_metrics_summary(minutes=1)
        if summary:
            print(json.dumps(summary, indent=2, ensure_ascii=False))
        
    except KeyboardInterrupt:
        print("\n⏹️  用户中断")
    finally:
        dashboard.stop_monitoring()
        print("✅ 监控演示完成")


def main():
    """主函数"""
    print("=" * 60)
    print("Session25 示例3：监控与日志管理")
    print("=" * 60)
    
    # 创建日志目录
    Path("logs").mkdir(exist_ok=True)
    
    while True:
        print("\n" + "=" * 40)
        print("请选择演示:")
        print("1. 健康检查演示")
        print("2. 监控功能演示")
        print("3. 结构化日志演示")
        print("0. 退出")
        
        choice = input("\n请输入选择 (0-3): ").strip()
        
        if choice == "1":
            demo_health_checks()
        elif choice == "2":
            demo_monitoring()
        elif choice == "3":
            # 结构化日志演示
            logger = StructuredLogger("log_demo", "logs/demo.log")
            logger.info("这是一条信息日志", user_id=123, action="login")
            logger.warning("这是一条警告日志", resource="memory", usage_percent=85)
            logger.error("这是一条错误日志", error_code="DB_CONNECTION_FAILED", retry_count=3)
            print("✅ 结构化日志已记录到 logs/demo.log")
        elif choice == "0":
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择，请重试")


if __name__ == "__main__":
    main()