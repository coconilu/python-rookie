#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session30: 项目部署与维护 - 演示代码

本文件演示了项目部署与维护的核心工具和最佳实践，包括：
- 部署脚本自动化
- 系统监控和健康检查
- 性能分析工具
- 备份管理
- 故障排查工具

作者: Python教程团队
创建日期: 2024-01-20
最后修改: 2024-01-20
"""

import os
import sys
import json
import time
import logging
import subprocess
import psutil
import requests
from datetime import datetime, timedelta
from functools import wraps
from typing import Dict, List, Optional
import threading
from collections import defaultdict


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class DeploymentManager:
    """
    部署管理器
    
    负责管理应用的部署流程，包括环境检查、代码部署、服务重启等。
    """
    
    def __init__(self, app_name: str, deploy_path: str):
        self.app_name = app_name
        self.deploy_path = deploy_path
        self.logger = logging.getLogger(f"{__name__}.DeploymentManager")
    
    def deploy(self, version: str, rollback_on_failure: bool = True) -> bool:
        """
        执行部署流程
        
        Args:
            version: 部署版本号
            rollback_on_failure: 失败时是否自动回滚
        
        Returns:
            bool: 部署是否成功
        """
        self.logger.info(f"开始部署 {self.app_name} 版本 {version}")
        backup_path = None
        
        try:
            # 1. 预检查
            if not self._pre_deployment_check():
                raise Exception("预检查失败")
            
            # 2. 备份当前版本
            backup_path = self._backup_current_version()
            self.logger.info(f"当前版本已备份到: {backup_path}")
            
            # 3. 下载新版本
            if not self._download_version(version):
                raise Exception("版本下载失败")
            
            # 4. 停止服务
            self._stop_service()
            
            # 5. 部署新版本
            self._deploy_version(version)
            
            # 6. 启动服务
            self._start_service()
            
            # 7. 健康检查
            if not self._health_check():
                if rollback_on_failure:
                    self.logger.warning("健康检查失败，开始回滚")
                    if backup_path:
                        self._rollback(backup_path)
                    return False
                else:
                    raise Exception("健康检查失败")
            
            self.logger.info(f"部署成功: {self.app_name} {version}")
            return True
            
        except Exception as e:
            self.logger.error(f"部署失败: {e}")
            if rollback_on_failure and backup_path:
                self._rollback(backup_path)
            return False
    
    def _pre_deployment_check(self) -> bool:
        """部署前检查"""
        checks = [
            self._check_disk_space(),
            self._check_memory(),
            self._check_dependencies()
        ]
        return all(checks)
    
    def _check_disk_space(self) -> bool:
        """检查磁盘空间"""
        disk_usage = psutil.disk_usage(self.deploy_path)
        free_gb = disk_usage.free / (1024**3)
        
        if free_gb < 1:  # 至少需要1GB空闲空间
            self.logger.error(f"磁盘空间不足: {free_gb:.2f}GB")
            return False
        
        self.logger.info(f"磁盘空间检查通过: {free_gb:.2f}GB 可用")
        return True
    
    def _check_memory(self) -> bool:
        """检查内存使用"""
        memory = psutil.virtual_memory()
        if memory.percent > 90:
            self.logger.error(f"内存使用率过高: {memory.percent}%")
            return False
        
        self.logger.info(f"内存检查通过: {memory.percent}% 使用中")
        return True
    
    def _check_dependencies(self) -> bool:
        """检查依赖"""
        # 这里可以检查Python版本、必要的包等
        try:
            import flask
            import gunicorn
            self.logger.info("依赖检查通过")
            return True
        except ImportError as e:
            self.logger.error(f"依赖检查失败: {e}")
            return False
    
    def _backup_current_version(self) -> str:
        """备份当前版本"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f"{self.deploy_path}_backup_{timestamp}"
        
        try:
            # 创建备份目录
            import os
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            
            # 模拟备份过程
            self.logger.info(f"正在备份到: {backup_path}")
            time.sleep(1)  # 模拟备份时间
            
            # 创建模拟备份文件
            os.makedirs(backup_path, exist_ok=True)
            with open(os.path.join(backup_path, "version.txt"), "w") as f:
                f.write("v1.0.0")
                
        except Exception as e:
            self.logger.warning(f"备份过程中出现警告: {e}")
        
        return backup_path
    
    def _download_version(self, version: str) -> bool:
        """下载指定版本"""
        try:
            self.logger.info(f"正在下载版本 {version}")
            time.sleep(1)  # 模拟下载时间
            self.logger.info("下载完成")
            return True
        except Exception as e:
            self.logger.error(f"下载失败: {e}")
            return False
    
    def _stop_service(self):
        """停止服务"""
        self.logger.info(f"正在停止服务: {self.app_name}")
        time.sleep(1)
    
    def _start_service(self):
        """启动服务"""
        self.logger.info(f"正在启动服务: {self.app_name}")
        time.sleep(2)
    
    def _deploy_version(self, version: str):
        """部署版本"""
        try:
            import os
            # 创建部署目录
            os.makedirs(self.deploy_path, exist_ok=True)
            
            self.logger.info(f"正在部署版本 {version}")
            time.sleep(2)  # 模拟部署时间
            
            # 更新版本文件
            with open(os.path.join(self.deploy_path, "version.txt"), "w") as f:
                f.write(version)
            
            self.logger.info("部署完成")
        except Exception as e:
            self.logger.error(f"部署过程中出现错误: {e}")
            raise
    
    def _health_check(self, max_retries: int = 5) -> bool:
        """健康检查"""
        for i in range(max_retries):
            try:
                # 模拟健康检查请求
                self.logger.info(f"健康检查 ({i+1}/{max_retries})")
                time.sleep(1)
                
                # 模拟90%的成功率
                import random
                if random.random() > 0.1:
                    self.logger.info("健康检查通过")
                    return True
                else:
                    self.logger.warning("健康检查失败，重试中...")
                    
            except Exception as e:
                self.logger.warning(f"健康检查异常: {e}")
        
        return False
    
    def _rollback(self, backup_path: str):
        """回滚到备份版本"""
        self.logger.info(f"正在回滚到: {backup_path}")
        self._stop_service()
        time.sleep(2)  # 模拟回滚时间
        self._start_service()
        self.logger.info("回滚完成")


class SystemMonitor:
    """
    系统监控器
    
    监控系统资源使用情况，提供健康检查和性能指标。
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.SystemMonitor")
        self.metrics_history = defaultdict(list)
        self.monitoring = False
        self.monitor_thread = None
    
    def get_system_info(self) -> Dict:
        """获取系统信息"""
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu': {
                'percent': psutil.cpu_percent(interval=1),
                'count': psutil.cpu_count(),
                'load_avg': os.getloadavg() if hasattr(os, 'getloadavg') else None
            },
            'memory': {
                'total': psutil.virtual_memory().total,
                'available': psutil.virtual_memory().available,
                'percent': psutil.virtual_memory().percent,
                'used': psutil.virtual_memory().used
            },
            'disk': {
                'total': psutil.disk_usage('/').total,
                'free': psutil.disk_usage('/').free,
                'used': psutil.disk_usage('/').used,
                'percent': psutil.disk_usage('/').percent
            },
            'network': self._get_network_stats(),
            'processes': len(psutil.pids())
        }
    
    def _get_network_stats(self) -> Dict:
        """获取网络统计信息"""
        net_io = psutil.net_io_counters()
        return {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv
        }
    
    def start_monitoring(self, interval: int = 60):
        """开始监控"""
        if self.monitoring:
            self.logger.warning("监控已在运行中")
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(interval,),
            daemon=True
        )
        self.monitor_thread.start()
        self.logger.info(f"开始系统监控，间隔: {interval}秒")
    
    def stop_monitoring(self):
        """停止监控"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        self.logger.info("系统监控已停止")
    
    def _monitor_loop(self, interval: int):
        """监控循环"""
        while self.monitoring:
            try:
                metrics = self.get_system_info()
                self._store_metrics(metrics)
                self._check_alerts(metrics)
                time.sleep(interval)
            except Exception as e:
                self.logger.error(f"监控异常: {e}")
                time.sleep(interval)
    
    def _store_metrics(self, metrics: Dict):
        """存储指标数据"""
        timestamp = time.time()
        
        # 只保留最近1小时的数据
        cutoff_time = timestamp - 3600
        
        for key in ['cpu_percent', 'memory_percent', 'disk_percent']:
            # 清理旧数据
            self.metrics_history[key] = [
                (t, v) for t, v in self.metrics_history[key] 
                if t > cutoff_time
            ]
        
        # 添加新数据
        self.metrics_history['cpu_percent'].append(
            (timestamp, metrics['cpu']['percent'])
        )
        self.metrics_history['memory_percent'].append(
            (timestamp, metrics['memory']['percent'])
        )
        self.metrics_history['disk_percent'].append(
            (timestamp, metrics['disk']['percent'])
        )
    
    def _check_alerts(self, metrics: Dict):
        """检查告警条件"""
        alerts = []
        
        # CPU使用率告警
        if metrics['cpu']['percent'] > 80:
            alerts.append(f"CPU使用率过高: {metrics['cpu']['percent']:.1f}%")
        
        # 内存使用率告警
        if metrics['memory']['percent'] > 85:
            alerts.append(f"内存使用率过高: {metrics['memory']['percent']:.1f}%")
        
        # 磁盘使用率告警
        if metrics['disk']['percent'] > 90:
            alerts.append(f"磁盘使用率过高: {metrics['disk']['percent']:.1f}%")
        
        for alert in alerts:
            self.logger.warning(f"[ALERT] {alert}")
    
    def get_metrics_summary(self) -> Dict:
        """获取指标摘要"""
        summary = {}
        
        for metric_name, data_points in self.metrics_history.items():
            if data_points:
                values = [v for _, v in data_points]
                summary[metric_name] = {
                    'current': values[-1] if values else 0,
                    'average': sum(values) / len(values),
                    'min': min(values),
                    'max': max(values),
                    'count': len(values)
                }
        
        return summary


class PerformanceProfiler:
    """
    性能分析器
    
    用于分析应用性能，识别性能瓶颈。
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.PerformanceProfiler")
        self.function_stats = defaultdict(list)
        self.lock = threading.Lock()
    
    def profile(self, func):
        """性能分析装饰器"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss
            
            try:
                result = func(*args, **kwargs)
                status = 'success'
                return result
            except Exception as e:
                status = 'error'
                self.logger.error(f"函数 {func.__name__} 执行异常: {e}")
                raise
            finally:
                end_time = time.time()
                end_memory = psutil.Process().memory_info().rss
                
                duration = end_time - start_time
                memory_delta = end_memory - start_memory
                
                with self.lock:
                    self.function_stats[func.__name__].append({
                        'timestamp': start_time,
                        'duration': duration,
                        'memory_delta': memory_delta,
                        'status': status
                    })
                
                self.logger.info(
                    f"函数 {func.__name__} 执行完成: "
                    f"耗时 {duration:.3f}s, "
                    f"内存变化 {memory_delta/1024:.1f}KB, "
                    f"状态 {status}"
                )
        
        return wrapper
    
    def get_performance_report(self) -> Dict:
        """获取性能报告"""
        report = {}
        
        with self.lock:
            for func_name, stats in self.function_stats.items():
                if not stats:
                    continue
                
                durations = [s['duration'] for s in stats]
                memory_deltas = [s['memory_delta'] for s in stats]
                success_count = sum(1 for s in stats if s['status'] == 'success')
                
                report[func_name] = {
                    'call_count': len(stats),
                    'success_rate': success_count / len(stats) * 100,
                    'duration': {
                        'avg': sum(durations) / len(durations),
                        'min': min(durations),
                        'max': max(durations),
                        'total': sum(durations)
                    },
                    'memory': {
                        'avg_delta': sum(memory_deltas) / len(memory_deltas),
                        'max_delta': max(memory_deltas),
                        'min_delta': min(memory_deltas)
                    }
                }
        
        return report
    
    def clear_stats(self):
        """清空统计数据"""
        with self.lock:
            self.function_stats.clear()
        self.logger.info("性能统计数据已清空")


class HealthChecker:
    """
    健康检查器
    
    检查应用和依赖服务的健康状态。
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.HealthChecker")
        self.checks = {}
    
    def add_check(self, name: str, check_func, timeout: int = 5):
        """添加健康检查项"""
        self.checks[name] = {
            'func': check_func,
            'timeout': timeout
        }
        self.logger.info(f"添加健康检查项: {name}")
    
    def run_all_checks(self) -> Dict:
        """运行所有健康检查"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'healthy',
            'checks': {}
        }
        
        for name, check_config in self.checks.items():
            try:
                start_time = time.time()
                
                # 运行检查函数
                check_result = check_config['func']()
                
                duration = time.time() - start_time
                
                results['checks'][name] = {
                    'status': 'healthy' if check_result else 'unhealthy',
                    'duration': duration,
                    'details': check_result if isinstance(check_result, dict) else None
                }
                
                if not check_result:
                    results['overall_status'] = 'unhealthy'
                    
            except Exception as e:
                results['checks'][name] = {
                    'status': 'error',
                    'error': str(e),
                    'duration': 0
                }
                results['overall_status'] = 'unhealthy'
                self.logger.error(f"健康检查 {name} 异常: {e}")
        
        return results
    
    def check_database(self) -> bool:
        """数据库连接检查"""
        try:
            # 模拟数据库连接检查
            time.sleep(0.1)
            return True
        except Exception:
            return False
    
    def check_redis(self) -> bool:
        """Redis连接检查"""
        try:
            # 模拟Redis连接检查
            time.sleep(0.05)
            return True
        except Exception:
            return False
    
    def check_external_api(self) -> bool:
        """外部API检查"""
        try:
            response = requests.get('https://httpbin.org/status/200', timeout=3)
            return response.status_code == 200
        except Exception:
            return False


def demo_deployment():
    """演示部署流程"""
    print("\n" + "="*60)
    print("项目部署演示")
    print("="*60)
    
    # 创建部署管理器
    deployer = DeploymentManager("my-web-app", "/opt/my-web-app")
    
    # 执行部署
    success = deployer.deploy("v2.1.0")
    
    if success:
        print("\n✅ 部署成功！")
    else:
        print("\n❌ 部署失败！")


def demo_monitoring():
    """演示系统监控"""
    print("\n" + "="*60)
    print("系统监控演示")
    print("="*60)
    
    monitor = SystemMonitor()
    
    # 获取当前系统信息
    system_info = monitor.get_system_info()
    
    print(f"\n📊 系统信息 ({system_info['timestamp']})")
    print(f"CPU使用率: {system_info['cpu']['percent']:.1f}%")
    print(f"内存使用率: {system_info['memory']['percent']:.1f}%")
    print(f"磁盘使用率: {system_info['disk']['percent']:.1f}%")
    print(f"运行进程数: {system_info['processes']}")
    
    # 启动短期监控
    print("\n🔍 启动监控 (10秒)...")
    monitor.start_monitoring(interval=2)
    time.sleep(10)
    monitor.stop_monitoring()
    
    # 显示监控摘要
    summary = monitor.get_metrics_summary()
    if summary:
        print("\n📈 监控摘要:")
        for metric, stats in summary.items():
            print(f"{metric}: 当前 {stats['current']:.1f}%, "
                  f"平均 {stats['average']:.1f}%, "
                  f"最大 {stats['max']:.1f}%")


def demo_performance_profiling():
    """演示性能分析"""
    print("\n" + "="*60)
    print("性能分析演示")
    print("="*60)
    
    profiler = PerformanceProfiler()
    
    # 定义一些测试函数
    @profiler.profile
    def cpu_intensive_task():
        """CPU密集型任务"""
        total = 0
        for i in range(1000000):
            total += i * i
        return total
    
    @profiler.profile
    def memory_intensive_task():
        """内存密集型任务"""
        data = [i for i in range(100000)]
        return len(data)
    
    @profiler.profile
    def io_intensive_task():
        """IO密集型任务"""
        time.sleep(0.1)
        return "completed"
    
    # 执行测试函数
    print("\n🧪 执行性能测试...")
    
    for i in range(3):
        cpu_intensive_task()
        memory_intensive_task()
        io_intensive_task()
    
    # 生成性能报告
    report = profiler.get_performance_report()
    
    print("\n📊 性能分析报告:")
    for func_name, stats in report.items():
        print(f"\n函数: {func_name}")
        print(f"  调用次数: {stats['call_count']}")
        print(f"  成功率: {stats['success_rate']:.1f}%")
        print(f"  平均耗时: {stats['duration']['avg']:.3f}s")
        print(f"  最大耗时: {stats['duration']['max']:.3f}s")
        print(f"  平均内存变化: {stats['memory']['avg_delta']/1024:.1f}KB")


def demo_health_check():
    """演示健康检查"""
    print("\n" + "="*60)
    print("健康检查演示")
    print("="*60)
    
    health_checker = HealthChecker()
    
    # 添加检查项
    health_checker.add_check('database', health_checker.check_database)
    health_checker.add_check('redis', health_checker.check_redis)
    health_checker.add_check('external_api', health_checker.check_external_api)
    
    # 运行健康检查
    print("\n🏥 运行健康检查...")
    results = health_checker.run_all_checks()
    
    print(f"\n📋 健康检查结果 ({results['timestamp']})")
    print(f"总体状态: {'✅ 健康' if results['overall_status'] == 'healthy' else '❌ 不健康'}")
    
    print("\n详细检查结果:")
    for check_name, check_result in results['checks'].items():
        status_icon = {
            'healthy': '✅',
            'unhealthy': '⚠️',
            'error': '❌'
        }.get(check_result['status'], '❓')
        
        print(f"  {status_icon} {check_name}: {check_result['status']} "
              f"({check_result.get('duration', 0):.3f}s)")
        
        if 'error' in check_result:
            print(f"    错误: {check_result['error']}")


def main():
    """
    主函数：演示项目部署与维护的核心功能
    """
    print("Session30: 项目部署与维护演示")
    print("=" * 60)
    print("本演示展示了项目部署与维护的核心工具和最佳实践")
    
    try:
        # 1. 部署流程演示
        demo_deployment()
        
        # 2. 系统监控演示
        demo_monitoring()
        
        # 3. 性能分析演示
        demo_performance_profiling()
        
        # 4. 健康检查演示
        demo_health_check()
        
        print("\n" + "="*60)
        print("🎉 所有演示完成！")
        print("="*60)
        
        print("\n📚 学习要点:")
        print("1. 自动化部署流程可以大大提高部署效率和可靠性")
        print("2. 系统监控是保证服务稳定运行的重要手段")
        print("3. 性能分析帮助识别和优化性能瓶颈")
        print("4. 健康检查确保服务和依赖的正常运行")
        print("5. 完善的运维体系是项目成功的关键保障")
        
        print("\n🚀 恭喜你完成了Python新手到项目负责人的完整学习旅程！")
        print("现在你已经具备了完整的项目开发和部署能力。")
        print("继续保持学习的热情，在实践中不断提升自己的技能！")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ 演示被用户中断")
    except Exception as e:
        logger.error(f"演示过程中发生错误: {e}")
        print(f"\n❌ 演示失败: {e}")
    finally:
        print("\n演示结束！")


if __name__ == "__main__":
    main()