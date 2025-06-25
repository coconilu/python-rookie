#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session30 示例4: 故障排查与恢复系统

本示例演示如何构建完整的故障排查与自动恢复系统，包括：
- 故障检测与诊断
- 自动恢复机制
- 日志分析与问题定位
- 健康检查与服务监控
- 故障报告生成

作者: Python教程团队
创建日期: 2024-01-20
"""

import os
import re
import json
import time
import psutil
import logging
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
from pathlib import Path
from enum import Enum


class FailureType(Enum):
    """故障类型枚举"""
    SERVICE_DOWN = "service_down"
    HIGH_CPU = "high_cpu"
    HIGH_MEMORY = "high_memory"
    DISK_FULL = "disk_full"
    NETWORK_ERROR = "network_error"
    DATABASE_ERROR = "database_error"
    APPLICATION_ERROR = "application_error"
    UNKNOWN = "unknown"


class Severity(Enum):
    """严重程度枚举"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class FailureEvent:
    """故障事件数据结构"""
    id: str
    timestamp: str
    failure_type: FailureType
    severity: Severity
    description: str
    affected_services: List[str]
    symptoms: List[str]
    root_cause: Optional[str] = None
    resolution_steps: List[str] = None
    resolved: bool = False
    resolution_time: Optional[str] = None
    
    def __post_init__(self):
        if self.resolution_steps is None:
            self.resolution_steps = []


@dataclass
class HealthCheckResult:
    """健康检查结果"""
    service_name: str
    status: str  # 'healthy', 'unhealthy', 'unknown'
    response_time: float
    error_message: Optional[str] = None
    details: Dict[str, Any] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
        if self.details is None:
            self.details = {}


class FailureDetector:
    """
    故障检测器
    
    检测各种类型的系统故障
    """
    
    def __init__(self):
        self.detection_rules = {
            FailureType.HIGH_CPU: self._check_high_cpu,
            FailureType.HIGH_MEMORY: self._check_high_memory,
            FailureType.DISK_FULL: self._check_disk_full,
            FailureType.SERVICE_DOWN: self._check_service_down,
            FailureType.NETWORK_ERROR: self._check_network_error
        }
        
        # 检测阈值
        self.thresholds = {
            'cpu_usage': 85.0,
            'memory_usage': 90.0,
            'disk_usage': 95.0,
            'response_time': 5.0  # 秒
        }
    
    def detect_failures(self) -> List[FailureEvent]:
        """
        检测系统故障
        
        Returns:
            List[FailureEvent]: 检测到的故障列表
        """
        failures = []
        
        for failure_type, check_func in self.detection_rules.items():
            try:
                failure = check_func()
                if failure:
                    failures.append(failure)
            except Exception as e:
                print(f"⚠️ 故障检测错误 ({failure_type.value}): {e}")
        
        return failures
    
    def _check_high_cpu(self) -> Optional[FailureEvent]:
        """检查CPU使用率过高"""
        cpu_percent = psutil.cpu_percent(interval=1)
        
        if cpu_percent > self.thresholds['cpu_usage']:
            return FailureEvent(
                id=f"cpu_{int(time.time())}",
                timestamp=datetime.now().isoformat(),
                failure_type=FailureType.HIGH_CPU,
                severity=Severity.HIGH if cpu_percent > 95 else Severity.MEDIUM,
                description=f"CPU使用率过高: {cpu_percent:.1f}%",
                affected_services=["system"],
                symptoms=[
                    f"CPU使用率: {cpu_percent:.1f}%",
                    "系统响应缓慢",
                    "可能影响应用性能"
                ]
            )
        return None
    
    def _check_high_memory(self) -> Optional[FailureEvent]:
        """检查内存使用率过高"""
        memory = psutil.virtual_memory()
        
        if memory.percent > self.thresholds['memory_usage']:
            return FailureEvent(
                id=f"memory_{int(time.time())}",
                timestamp=datetime.now().isoformat(),
                failure_type=FailureType.HIGH_MEMORY,
                severity=Severity.CRITICAL if memory.percent > 98 else Severity.HIGH,
                description=f"内存使用率过高: {memory.percent:.1f}%",
                affected_services=["system"],
                symptoms=[
                    f"内存使用率: {memory.percent:.1f}%",
                    f"可用内存: {memory.available / (1024**3):.2f} GB",
                    "可能导致OOM错误"
                ]
            )
        return None
    
    def _check_disk_full(self) -> Optional[FailureEvent]:
        """检查磁盘空间不足"""
        try:
            disk = psutil.disk_usage('/')
            usage_percent = (disk.used / disk.total) * 100
            
            if usage_percent > self.thresholds['disk_usage']:
                return FailureEvent(
                    id=f"disk_{int(time.time())}",
                    timestamp=datetime.now().isoformat(),
                    failure_type=FailureType.DISK_FULL,
                    severity=Severity.CRITICAL,
                    description=f"磁盘空间不足: {usage_percent:.1f}%",
                    affected_services=["system", "database", "logs"],
                    symptoms=[
                        f"磁盘使用率: {usage_percent:.1f}%",
                        f"剩余空间: {disk.free / (1024**3):.2f} GB",
                        "可能导致写入失败"
                    ]
                )
        except Exception as e:
            print(f"磁盘检查错误: {e}")
        
        return None
    
    def _check_service_down(self) -> Optional[FailureEvent]:
        """检查服务是否宕机（模拟）"""
        # 模拟服务检查
        import random
        
        services = ["web-server", "database", "redis", "nginx"]
        
        for service in services:
            # 随机模拟服务故障
            if random.random() < 0.1:  # 10%概率
                return FailureEvent(
                    id=f"service_{service}_{int(time.time())}",
                    timestamp=datetime.now().isoformat(),
                    failure_type=FailureType.SERVICE_DOWN,
                    severity=Severity.CRITICAL,
                    description=f"服务 {service} 无响应",
                    affected_services=[service],
                    symptoms=[
                        f"服务 {service} 连接超时",
                        "健康检查失败",
                        "用户无法访问功能"
                    ]
                )
        
        return None
    
    def _check_network_error(self) -> Optional[FailureEvent]:
        """检查网络错误"""
        try:
            # 检查网络接口统计
            net_io = psutil.net_io_counters()
            
            # 简单的错误率检查（实际应用中需要更复杂的逻辑）
            total_packets = net_io.packets_sent + net_io.packets_recv
            error_packets = net_io.errin + net_io.errout + net_io.dropin + net_io.dropout
            
            if total_packets > 0:
                error_rate = (error_packets / total_packets) * 100
                
                if error_rate > 1.0:  # 错误率超过1%
                    return FailureEvent(
                        id=f"network_{int(time.time())}",
                        timestamp=datetime.now().isoformat(),
                        failure_type=FailureType.NETWORK_ERROR,
                        severity=Severity.MEDIUM,
                        description=f"网络错误率过高: {error_rate:.2f}%",
                        affected_services=["network"],
                        symptoms=[
                            f"网络错误率: {error_rate:.2f}%",
                            f"丢包数: {net_io.dropin + net_io.dropout}",
                            "网络连接不稳定"
                        ]
                    )
        except Exception as e:
            print(f"网络检查错误: {e}")
        
        return None


class HealthChecker:
    """
    健康检查器
    
    检查各种服务的健康状态
    """
    
    def __init__(self):
        self.services = {
            "web-server": {"url": "http://localhost:8000/health", "timeout": 5},
            "database": {"host": "localhost", "port": 5432, "timeout": 3},
            "redis": {"host": "localhost", "port": 6379, "timeout": 2},
            "nginx": {"url": "http://localhost/health", "timeout": 3}
        }
    
    def check_all_services(self) -> List[HealthCheckResult]:
        """
        检查所有服务健康状态
        
        Returns:
            List[HealthCheckResult]: 健康检查结果列表
        """
        results = []
        
        for service_name, config in self.services.items():
            result = self.check_service(service_name, config)
            results.append(result)
        
        return results
    
    def check_service(self, service_name: str, config: Dict) -> HealthCheckResult:
        """
        检查单个服务健康状态
        
        Args:
            service_name: 服务名称
            config: 服务配置
        
        Returns:
            HealthCheckResult: 健康检查结果
        """
        start_time = time.time()
        
        try:
            if "url" in config:
                # HTTP健康检查
                result = self._check_http_service(config["url"], config["timeout"])
            else:
                # TCP端口检查
                result = self._check_tcp_service(config["host"], config["port"], config["timeout"])
            
            response_time = time.time() - start_time
            
            return HealthCheckResult(
                service_name=service_name,
                status="healthy" if result["success"] else "unhealthy",
                response_time=response_time,
                error_message=result.get("error"),
                details=result.get("details", {})
            )
        
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheckResult(
                service_name=service_name,
                status="unknown",
                response_time=response_time,
                error_message=str(e)
            )
    
    def _check_http_service(self, url: str, timeout: int) -> Dict:
        """
        HTTP服务健康检查
        
        Args:
            url: 检查URL
            timeout: 超时时间
        
        Returns:
            Dict: 检查结果
        """
        try:
            import urllib.request
            import urllib.error
            
            response = urllib.request.urlopen(url, timeout=timeout)
            status_code = response.getcode()
            
            if status_code == 200:
                return {
                    "success": True,
                    "details": {"status_code": status_code}
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {status_code}",
                    "details": {"status_code": status_code}
                }
        
        except urllib.error.URLError as e:
            return {
                "success": False,
                "error": f"连接错误: {e}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"未知错误: {e}"
            }
    
    def _check_tcp_service(self, host: str, port: int, timeout: int) -> Dict:
        """
        TCP端口健康检查
        
        Args:
            host: 主机地址
            port: 端口号
            timeout: 超时时间
        
        Returns:
            Dict: 检查结果
        """
        try:
            import socket
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                return {
                    "success": True,
                    "details": {"host": host, "port": port}
                }
            else:
                return {
                    "success": False,
                    "error": f"端口 {port} 无法连接",
                    "details": {"host": host, "port": port}
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"连接错误: {e}"
            }


class AutoRecovery:
    """
    自动恢复系统
    
    根据故障类型执行相应的恢复操作
    """
    
    def __init__(self):
        self.recovery_strategies = {
            FailureType.HIGH_CPU: self._recover_high_cpu,
            FailureType.HIGH_MEMORY: self._recover_high_memory,
            FailureType.DISK_FULL: self._recover_disk_full,
            FailureType.SERVICE_DOWN: self._recover_service_down,
            FailureType.NETWORK_ERROR: self._recover_network_error
        }
        
        self.recovery_history = deque(maxlen=100)
    
    def attempt_recovery(self, failure: FailureEvent) -> bool:
        """
        尝试自动恢复
        
        Args:
            failure: 故障事件
        
        Returns:
            bool: 恢复是否成功
        """
        print(f"🔧 尝试自动恢复: {failure.description}")
        
        recovery_func = self.recovery_strategies.get(failure.failure_type)
        
        if not recovery_func:
            print(f"⚠️ 没有找到恢复策略: {failure.failure_type.value}")
            return False
        
        try:
            success = recovery_func(failure)
            
            recovery_record = {
                "timestamp": datetime.now().isoformat(),
                "failure_id": failure.id,
                "failure_type": failure.failure_type.value,
                "success": success,
                "steps": failure.resolution_steps
            }
            
            self.recovery_history.append(recovery_record)
            
            if success:
                print(f"✅ 自动恢复成功: {failure.description}")
                failure.resolved = True
                failure.resolution_time = datetime.now().isoformat()
            else:
                print(f"❌ 自动恢复失败: {failure.description}")
            
            return success
        
        except Exception as e:
            print(f"💥 恢复过程出错: {e}")
            return False
    
    def _recover_high_cpu(self, failure: FailureEvent) -> bool:
        """
        恢复CPU使用率过高
        
        Args:
            failure: 故障事件
        
        Returns:
            bool: 恢复是否成功
        """
        steps = [
            "识别高CPU使用进程",
            "检查进程是否异常",
            "尝试优化或重启异常进程"
        ]
        
        failure.resolution_steps.extend(steps)
        
        try:
            # 获取CPU使用率最高的进程
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    proc_info = proc.info
                    if proc_info['cpu_percent'] > 10:  # CPU使用率超过10%
                        processes.append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # 按CPU使用率排序
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            
            if processes:
                top_process = processes[0]
                print(f"🔍 发现高CPU进程: {top_process['name']} (PID: {top_process['pid']}, CPU: {top_process['cpu_percent']:.1f}%)")
                
                # 模拟进程优化（实际应用中可能需要重启特定服务）
                print("⚡ 执行进程优化...")
                time.sleep(2)  # 模拟优化时间
                
                # 检查优化效果
                current_cpu = psutil.cpu_percent(interval=1)
                if current_cpu < 80:  # 假设优化成功
                    return True
            
            return False
        
        except Exception as e:
            print(f"CPU恢复错误: {e}")
            return False
    
    def _recover_high_memory(self, failure: FailureEvent) -> bool:
        """
        恢复内存使用率过高
        
        Args:
            failure: 故障事件
        
        Returns:
            bool: 恢复是否成功
        """
        steps = [
            "清理系统缓存",
            "识别内存泄漏进程",
            "重启高内存使用服务"
        ]
        
        failure.resolution_steps.extend(steps)
        
        try:
            print("🧹 清理系统缓存...")
            
            # 在Linux系统上清理缓存（Windows上此操作无效）
            try:
                if os.name == 'posix':  # Unix/Linux系统
                    subprocess.run(['sync'], check=True)
                    # 注意：实际清理缓存需要root权限
                    print("💾 缓存清理完成")
            except:
                print("⚠️ 缓存清理需要管理员权限")
            
            # 检查内存使用情况
            memory = psutil.virtual_memory()
            if memory.percent < 85:  # 假设清理成功
                return True
            
            return False
        
        except Exception as e:
            print(f"内存恢复错误: {e}")
            return False
    
    def _recover_disk_full(self, failure: FailureEvent) -> bool:
        """
        恢复磁盘空间不足
        
        Args:
            failure: 故障事件
        
        Returns:
            bool: 恢复是否成功
        """
        steps = [
            "清理临时文件",
            "压缩日志文件",
            "删除过期备份"
        ]
        
        failure.resolution_steps.extend(steps)
        
        try:
            print("🗑️ 清理磁盘空间...")
            
            # 清理临时文件
            temp_dirs = ['/tmp', '/var/tmp'] if os.name == 'posix' else [os.environ.get('TEMP', 'C:\\temp')]
            
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    try:
                        # 删除超过7天的临时文件
                        cutoff_time = time.time() - (7 * 24 * 60 * 60)
                        
                        for root, dirs, files in os.walk(temp_dir):
                            for file in files:
                                file_path = os.path.join(root, file)
                                try:
                                    if os.path.getmtime(file_path) < cutoff_time:
                                        os.remove(file_path)
                                        print(f"🗑️ 删除临时文件: {file_path}")
                                except:
                                    pass  # 忽略无法删除的文件
                    except Exception as e:
                        print(f"清理 {temp_dir} 时出错: {e}")
            
            # 模拟日志压缩
            print("📦 压缩日志文件...")
            time.sleep(1)
            
            # 检查磁盘空间
            disk = psutil.disk_usage('/')
            usage_percent = (disk.used / disk.total) * 100
            
            if usage_percent < 90:  # 假设清理成功
                return True
            
            return False
        
        except Exception as e:
            print(f"磁盘清理错误: {e}")
            return False
    
    def _recover_service_down(self, failure: FailureEvent) -> bool:
        """
        恢复服务宕机
        
        Args:
            failure: 故障事件
        
        Returns:
            bool: 恢复是否成功
        """
        steps = [
            "检查服务状态",
            "尝试重启服务",
            "验证服务恢复"
        ]
        
        failure.resolution_steps.extend(steps)
        
        try:
            service_name = failure.affected_services[0] if failure.affected_services else "unknown"
            
            print(f"🔄 尝试重启服务: {service_name}")
            
            # 模拟服务重启
            time.sleep(3)
            
            # 模拟重启成功（实际应用中需要真实的服务管理）
            import random
            success = random.random() > 0.3  # 70%成功率
            
            if success:
                print(f"✅ 服务 {service_name} 重启成功")
            else:
                print(f"❌ 服务 {service_name} 重启失败")
            
            return success
        
        except Exception as e:
            print(f"服务恢复错误: {e}")
            return False
    
    def _recover_network_error(self, failure: FailureEvent) -> bool:
        """
        恢复网络错误
        
        Args:
            failure: 故障事件
        
        Returns:
            bool: 恢复是否成功
        """
        steps = [
            "检查网络接口状态",
            "重置网络连接",
            "验证网络连通性"
        ]
        
        failure.resolution_steps.extend(steps)
        
        try:
            print("🌐 检查网络状态...")
            
            # 检查网络接口
            interfaces = psutil.net_if_stats()
            
            for interface, stats in interfaces.items():
                if stats.isup:
                    print(f"📡 网络接口 {interface}: 正常")
                else:
                    print(f"❌ 网络接口 {interface}: 异常")
            
            # 模拟网络修复
            print("🔧 尝试网络修复...")
            time.sleep(2)
            
            # 模拟修复成功
            return True
        
        except Exception as e:
            print(f"网络恢复错误: {e}")
            return False
    
    def get_recovery_history(self, limit: int = 10) -> List[Dict]:
        """
        获取恢复历史
        
        Args:
            limit: 返回数量限制
        
        Returns:
            List[Dict]: 恢复历史列表
        """
        return list(self.recovery_history)[-limit:]


class TroubleshootingSystem:
    """
    故障排查系统
    
    整合故障检测、健康检查和自动恢复功能
    """
    
    def __init__(self):
        self.detector = FailureDetector()
        self.health_checker = HealthChecker()
        self.auto_recovery = AutoRecovery()
        
        self.failure_history = deque(maxlen=1000)
        self.running = False
    
    def start_monitoring(self, duration: int = 60):
        """
        开始监控
        
        Args:
            duration: 监控持续时间（秒）
        """
        print(f"🚀 启动故障排查系统，监控时长: {duration}秒")
        self.running = True
        
        start_time = time.time()
        check_interval = 10  # 每10秒检查一次
        
        try:
            while self.running and (time.time() - start_time) < duration:
                print(f"\n🔍 执行系统检查... ({datetime.now().strftime('%H:%M:%S')})")
                
                # 健康检查
                health_results = self.health_checker.check_all_services()
                self._report_health_status(health_results)
                
                # 故障检测
                failures = self.detector.detect_failures()
                
                if failures:
                    print(f"🚨 检测到 {len(failures)} 个故障")
                    
                    for failure in failures:
                        print(f"  ❌ {failure.description} (严重程度: {failure.severity.value})")
                        
                        # 记录故障
                        self.failure_history.append(failure)
                        
                        # 尝试自动恢复
                        if failure.severity in [Severity.HIGH, Severity.CRITICAL]:
                            recovery_success = self.auto_recovery.attempt_recovery(failure)
                            
                            if recovery_success:
                                print(f"  ✅ 自动恢复成功")
                            else:
                                print(f"  ⚠️ 需要人工干预")
                                self._generate_troubleshooting_guide(failure)
                else:
                    print("✅ 系统运行正常")
                
                # 等待下次检查
                time.sleep(check_interval)
        
        except KeyboardInterrupt:
            print("\n⏹️ 用户中断监控")
        
        finally:
            self.running = False
            self._generate_final_report()
    
    def _report_health_status(self, health_results: List[HealthCheckResult]):
        """
        报告健康状态
        
        Args:
            health_results: 健康检查结果列表
        """
        healthy_count = sum(1 for r in health_results if r.status == 'healthy')
        total_count = len(health_results)
        
        print(f"🏥 健康检查: {healthy_count}/{total_count} 服务正常")
        
        for result in health_results:
            status_emoji = {
                'healthy': '✅',
                'unhealthy': '❌',
                'unknown': '❓'
            }.get(result.status, '❓')
            
            print(f"  {status_emoji} {result.service_name}: {result.status} ({result.response_time:.2f}s)")
            
            if result.error_message:
                print(f"    错误: {result.error_message}")
    
    def _generate_troubleshooting_guide(self, failure: FailureEvent):
        """
        生成故障排查指南
        
        Args:
            failure: 故障事件
        """
        print(f"\n📋 故障排查指南: {failure.description}")
        print("-" * 50)
        
        # 症状描述
        print("🔍 症状:")
        for symptom in failure.symptoms:
            print(f"  • {symptom}")
        
        # 可能原因
        possible_causes = self._get_possible_causes(failure.failure_type)
        print("\n🤔 可能原因:")
        for cause in possible_causes:
            print(f"  • {cause}")
        
        # 排查步骤
        troubleshooting_steps = self._get_troubleshooting_steps(failure.failure_type)
        print("\n🔧 排查步骤:")
        for i, step in enumerate(troubleshooting_steps, 1):
            print(f"  {i}. {step}")
        
        # 预防措施
        prevention_tips = self._get_prevention_tips(failure.failure_type)
        print("\n🛡️ 预防措施:")
        for tip in prevention_tips:
            print(f"  • {tip}")
    
    def _get_possible_causes(self, failure_type: FailureType) -> List[str]:
        """获取可能原因"""
        causes_map = {
            FailureType.HIGH_CPU: [
                "CPU密集型进程异常",
                "无限循环或死锁",
                "系统负载过高",
                "恶意软件感染"
            ],
            FailureType.HIGH_MEMORY: [
                "内存泄漏",
                "大数据处理",
                "缓存过度使用",
                "进程异常增长"
            ],
            FailureType.DISK_FULL: [
                "日志文件过大",
                "临时文件堆积",
                "数据库增长",
                "备份文件占用"
            ],
            FailureType.SERVICE_DOWN: [
                "进程崩溃",
                "配置错误",
                "依赖服务故障",
                "资源不足"
            ],
            FailureType.NETWORK_ERROR: [
                "网络设备故障",
                "DNS解析问题",
                "防火墙阻断",
                "带宽不足"
            ]
        }
        
        return causes_map.get(failure_type, ["未知原因"])
    
    def _get_troubleshooting_steps(self, failure_type: FailureType) -> List[str]:
        """获取排查步骤"""
        steps_map = {
            FailureType.HIGH_CPU: [
                "使用top/htop查看进程CPU使用情况",
                "检查是否有异常进程",
                "分析进程调用栈",
                "检查系统负载历史",
                "考虑增加CPU资源或优化代码"
            ],
            FailureType.HIGH_MEMORY: [
                "使用free/ps命令查看内存使用",
                "检查进程内存占用",
                "分析内存泄漏",
                "清理不必要的缓存",
                "重启高内存使用的服务"
            ],
            FailureType.DISK_FULL: [
                "使用df命令查看磁盘使用情况",
                "使用du命令找出大文件/目录",
                "清理日志文件",
                "删除临时文件",
                "考虑磁盘扩容"
            ],
            FailureType.SERVICE_DOWN: [
                "检查服务状态",
                "查看服务日志",
                "检查配置文件",
                "验证依赖服务",
                "尝试重启服务"
            ],
            FailureType.NETWORK_ERROR: [
                "检查网络连接",
                "测试DNS解析",
                "检查防火墙规则",
                "验证网络配置",
                "联系网络管理员"
            ]
        }
        
        return steps_map.get(failure_type, ["联系技术支持"])
    
    def _get_prevention_tips(self, failure_type: FailureType) -> List[str]:
        """获取预防措施"""
        tips_map = {
            FailureType.HIGH_CPU: [
                "定期监控CPU使用率",
                "优化代码性能",
                "设置CPU使用率告警",
                "合理分配系统资源"
            ],
            FailureType.HIGH_MEMORY: [
                "定期检查内存使用",
                "及时修复内存泄漏",
                "设置内存告警阈值",
                "优化内存使用策略"
            ],
            FailureType.DISK_FULL: [
                "设置磁盘空间监控",
                "定期清理日志文件",
                "实施日志轮转策略",
                "规划磁盘容量"
            ],
            FailureType.SERVICE_DOWN: [
                "实施健康检查",
                "设置服务监控",
                "配置自动重启",
                "建立服务依赖管理"
            ],
            FailureType.NETWORK_ERROR: [
                "监控网络状态",
                "配置网络冗余",
                "定期检查网络设备",
                "建立网络故障应急预案"
            ]
        }
        
        return tips_map.get(failure_type, ["建立完善的监控体系"])
    
    def _generate_final_report(self):
        """
        生成最终报告
        """
        print("\n" + "=" * 60)
        print("📊 故障排查系统报告")
        print("=" * 60)
        
        # 统计信息
        total_failures = len(self.failure_history)
        resolved_failures = sum(1 for f in self.failure_history if f.resolved)
        
        print(f"总故障数: {total_failures}")
        print(f"已解决: {resolved_failures}")
        print(f"自动恢复率: {(resolved_failures/total_failures*100):.1f}%" if total_failures > 0 else "自动恢复率: N/A")
        
        # 故障类型统计
        if self.failure_history:
            failure_types = defaultdict(int)
            for failure in self.failure_history:
                failure_types[failure.failure_type.value] += 1
            
            print("\n故障类型分布:")
            for failure_type, count in failure_types.items():
                print(f"  {failure_type}: {count} 次")
        
        # 恢复历史
        recovery_history = self.auto_recovery.get_recovery_history()
        if recovery_history:
            print("\n最近恢复记录:")
            for record in recovery_history[-5:]:  # 显示最近5次
                status = "成功" if record['success'] else "失败"
                print(f"  {record['timestamp']}: {record['failure_type']} - {status}")
        
        print("\n🎯 系统监控完成！")


def main():
    """
    主函数：演示故障排查与恢复系统
    """
    print("Session30 示例4: 故障排查与恢复系统")
    print("=" * 60)
    
    # 创建故障排查系统
    troubleshooting_system = TroubleshootingSystem()
    
    print("🔧 系统功能演示:")
    print("1. 🔍 故障检测")
    print("2. 🏥 健康检查")
    print("3. 🔄 自动恢复")
    print("4. 📋 故障排查指南")
    print("5. 📊 监控报告")
    
    # 启动监控（运行30秒进行演示）
    troubleshooting_system.start_monitoring(duration=30)
    
    print("\n💡 实际应用建议:")
    print("1. 🔧 集成到生产环境监控")
    print("2. 📱 配置告警通知（邮件/短信/Slack）")
    print("3. 📊 建立监控仪表板")
    print("4. 📚 完善故障知识库")
    print("5. 🔄 定期演练故障恢复流程")
    print("6. 📈 分析故障趋势和模式")


if __name__ == "__main__":
    main()