#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session30 示例3: 项目监控与性能分析

本示例演示如何实现完整的项目监控和性能分析系统，包括：
- 应用性能监控(APM)
- 系统资源监控
- 日志聚合与分析
- 告警系统
- 性能分析与优化建议

作者: Python教程团队
创建日期: 2024-01-20
"""

import os
import time
import json
import psutil
import logging
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
from collections import deque, defaultdict
import sqlite3
from pathlib import Path


@dataclass
class MetricData:
    """
    监控指标数据结构
    """
    timestamp: str
    metric_name: str
    value: float
    unit: str
    tags: Dict[str, str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = {}


@dataclass
class AlertRule:
    """
    告警规则数据结构
    """
    name: str
    metric_name: str
    condition: str  # 'gt', 'lt', 'eq'
    threshold: float
    duration: int  # 持续时间(秒)
    severity: str  # 'low', 'medium', 'high', 'critical'
    enabled: bool = True
    callback: Optional[Callable] = None


class MetricsCollector:
    """
    指标收集器
    
    收集系统和应用的各种性能指标
    """
    
    def __init__(self):
        self.metrics_buffer = deque(maxlen=1000)
        self.collection_interval = 5  # 秒
        self.running = False
        self.collection_thread = None
    
    def collect_system_metrics(self) -> List[MetricData]:
        """
        收集系统指标
        
        Returns:
            List[MetricData]: 系统指标列表
        """
        timestamp = datetime.now().isoformat()
        metrics = []
        
        # CPU使用率
        cpu_percent = psutil.cpu_percent(interval=1)
        metrics.append(MetricData(
            timestamp=timestamp,
            metric_name="cpu_usage",
            value=cpu_percent,
            unit="percent",
            tags={"type": "system"}
        ))
        
        # 内存使用情况
        memory = psutil.virtual_memory()
        metrics.append(MetricData(
            timestamp=timestamp,
            metric_name="memory_usage",
            value=memory.percent,
            unit="percent",
            tags={"type": "system"}
        ))
        
        metrics.append(MetricData(
            timestamp=timestamp,
            metric_name="memory_available",
            value=memory.available / (1024**3),  # GB
            unit="GB",
            tags={"type": "system"}
        ))
        
        # 磁盘使用情况
        disk = psutil.disk_usage('/')
        metrics.append(MetricData(
            timestamp=timestamp,
            metric_name="disk_usage",
            value=(disk.used / disk.total) * 100,
            unit="percent",
            tags={"type": "system", "mount": "/"}
        ))
        
        # 网络IO
        net_io = psutil.net_io_counters()
        metrics.append(MetricData(
            timestamp=timestamp,
            metric_name="network_bytes_sent",
            value=net_io.bytes_sent / (1024**2),  # MB
            unit="MB",
            tags={"type": "network", "direction": "sent"}
        ))
        
        metrics.append(MetricData(
            timestamp=timestamp,
            metric_name="network_bytes_recv",
            value=net_io.bytes_recv / (1024**2),  # MB
            unit="MB",
            tags={"type": "network", "direction": "received"}
        ))
        
        # 进程数量
        process_count = len(psutil.pids())
        metrics.append(MetricData(
            timestamp=timestamp,
            metric_name="process_count",
            value=process_count,
            unit="count",
            tags={"type": "system"}
        ))
        
        return metrics
    
    def collect_application_metrics(self) -> List[MetricData]:
        """
        收集应用指标（模拟）
        
        Returns:
            List[MetricData]: 应用指标列表
        """
        timestamp = datetime.now().isoformat()
        metrics = []
        
        # 模拟应用指标
        import random
        
        # 响应时间
        response_time = random.uniform(50, 500)  # ms
        metrics.append(MetricData(
            timestamp=timestamp,
            metric_name="response_time",
            value=response_time,
            unit="ms",
            tags={"type": "application", "endpoint": "/api/users"}
        ))
        
        # 请求数量
        request_count = random.randint(10, 100)
        metrics.append(MetricData(
            timestamp=timestamp,
            metric_name="request_count",
            value=request_count,
            unit="count",
            tags={"type": "application", "method": "GET"}
        ))
        
        # 错误率
        error_rate = random.uniform(0, 5)  # %
        metrics.append(MetricData(
            timestamp=timestamp,
            metric_name="error_rate",
            value=error_rate,
            unit="percent",
            tags={"type": "application"}
        ))
        
        # 数据库连接数
        db_connections = random.randint(5, 50)
        metrics.append(MetricData(
            timestamp=timestamp,
            metric_name="db_connections",
            value=db_connections,
            unit="count",
            tags={"type": "database"}
        ))
        
        # 缓存命中率
        cache_hit_rate = random.uniform(80, 99)  # %
        metrics.append(MetricData(
            timestamp=timestamp,
            metric_name="cache_hit_rate",
            value=cache_hit_rate,
            unit="percent",
            tags={"type": "cache"}
        ))
        
        return metrics
    
    def start_collection(self):
        """
        开始指标收集
        """
        if self.running:
            return
        
        self.running = True
        self.collection_thread = threading.Thread(target=self._collection_loop)
        self.collection_thread.daemon = True
        self.collection_thread.start()
        print("📊 指标收集已启动")
    
    def stop_collection(self):
        """
        停止指标收集
        """
        self.running = False
        if self.collection_thread:
            self.collection_thread.join()
        print("⏹️ 指标收集已停止")
    
    def _collection_loop(self):
        """
        指标收集循环
        """
        while self.running:
            try:
                # 收集系统指标
                system_metrics = self.collect_system_metrics()
                self.metrics_buffer.extend(system_metrics)
                
                # 收集应用指标
                app_metrics = self.collect_application_metrics()
                self.metrics_buffer.extend(app_metrics)
                
                time.sleep(self.collection_interval)
                
            except Exception as e:
                print(f"⚠️ 指标收集错误: {e}")
                time.sleep(self.collection_interval)
    
    def get_recent_metrics(self, metric_name: str = None, limit: int = 100) -> List[MetricData]:
        """
        获取最近的指标数据
        
        Args:
            metric_name: 指标名称过滤
            limit: 返回数量限制
        
        Returns:
            List[MetricData]: 指标数据列表
        """
        metrics = list(self.metrics_buffer)
        
        if metric_name:
            metrics = [m for m in metrics if m.metric_name == metric_name]
        
        return metrics[-limit:]


class AlertManager:
    """
    告警管理器
    
    管理告警规则和发送告警通知
    """
    
    def __init__(self):
        self.alert_rules: List[AlertRule] = []
        self.alert_states = defaultdict(dict)  # 存储告警状态
        self.alert_history = deque(maxlen=1000)
        
        # 设置日志
        self.logger = logging.getLogger('AlertManager')
        self.logger.setLevel(logging.INFO)
        
        # 默认告警规则
        self._setup_default_rules()
    
    def _setup_default_rules(self):
        """
        设置默认告警规则
        """
        default_rules = [
            AlertRule(
                name="高CPU使用率",
                metric_name="cpu_usage",
                condition="gt",
                threshold=80.0,
                duration=60,
                severity="high"
            ),
            AlertRule(
                name="高内存使用率",
                metric_name="memory_usage",
                condition="gt",
                threshold=85.0,
                duration=120,
                severity="high"
            ),
            AlertRule(
                name="磁盘空间不足",
                metric_name="disk_usage",
                condition="gt",
                threshold=90.0,
                duration=300,
                severity="critical"
            ),
            AlertRule(
                name="高响应时间",
                metric_name="response_time",
                condition="gt",
                threshold=1000.0,
                duration=30,
                severity="medium"
            ),
            AlertRule(
                name="高错误率",
                metric_name="error_rate",
                condition="gt",
                threshold=5.0,
                duration=60,
                severity="high"
            )
        ]
        
        self.alert_rules.extend(default_rules)
    
    def add_rule(self, rule: AlertRule):
        """
        添加告警规则
        
        Args:
            rule: 告警规则
        """
        self.alert_rules.append(rule)
        print(f"✅ 告警规则已添加: {rule.name}")
    
    def check_alerts(self, metrics: List[MetricData]):
        """
        检查告警条件
        
        Args:
            metrics: 指标数据列表
        """
        current_time = datetime.now()
        
        for rule in self.alert_rules:
            if not rule.enabled:
                continue
            
            # 查找匹配的指标
            matching_metrics = [m for m in metrics if m.metric_name == rule.metric_name]
            
            if not matching_metrics:
                continue
            
            # 获取最新指标值
            latest_metric = matching_metrics[-1]
            
            # 检查条件
            condition_met = self._check_condition(latest_metric.value, rule)
            
            rule_key = f"{rule.name}_{rule.metric_name}"
            
            if condition_met:
                # 条件满足，记录或更新告警状态
                if rule_key not in self.alert_states:
                    self.alert_states[rule_key] = {
                        'first_triggered': current_time,
                        'last_triggered': current_time,
                        'count': 1,
                        'notified': False
                    }
                else:
                    self.alert_states[rule_key]['last_triggered'] = current_time
                    self.alert_states[rule_key]['count'] += 1
                
                # 检查是否达到持续时间要求
                state = self.alert_states[rule_key]
                duration = (current_time - state['first_triggered']).total_seconds()
                
                if duration >= rule.duration and not state['notified']:
                    self._trigger_alert(rule, latest_metric, duration)
                    state['notified'] = True
            
            else:
                # 条件不满足，清除告警状态
                if rule_key in self.alert_states:
                    if self.alert_states[rule_key]['notified']:
                        self._resolve_alert(rule, latest_metric)
                    del self.alert_states[rule_key]
    
    def _check_condition(self, value: float, rule: AlertRule) -> bool:
        """
        检查告警条件
        
        Args:
            value: 指标值
            rule: 告警规则
        
        Returns:
            bool: 是否满足条件
        """
        if rule.condition == 'gt':
            return value > rule.threshold
        elif rule.condition == 'lt':
            return value < rule.threshold
        elif rule.condition == 'eq':
            return abs(value - rule.threshold) < 0.001
        else:
            return False
    
    def _trigger_alert(self, rule: AlertRule, metric: MetricData, duration: float):
        """
        触发告警
        
        Args:
            rule: 告警规则
            metric: 触发的指标
            duration: 持续时间
        """
        alert_info = {
            'timestamp': datetime.now().isoformat(),
            'rule_name': rule.name,
            'metric_name': rule.metric_name,
            'current_value': metric.value,
            'threshold': rule.threshold,
            'severity': rule.severity,
            'duration': duration,
            'status': 'triggered'
        }
        
        self.alert_history.append(alert_info)
        
        # 输出告警信息
        severity_emoji = {
            'low': '🟡',
            'medium': '🟠', 
            'high': '🔴',
            'critical': '🚨'
        }
        
        emoji = severity_emoji.get(rule.severity, '⚠️')
        print(f"{emoji} 告警触发: {rule.name}")
        print(f"   指标: {rule.metric_name} = {metric.value:.2f} {metric.unit}")
        print(f"   阈值: {rule.threshold} (条件: {rule.condition})")
        print(f"   持续时间: {duration:.0f}秒")
        print(f"   严重程度: {rule.severity}")
        
        # 调用回调函数
        if rule.callback:
            try:
                rule.callback(alert_info)
            except Exception as e:
                self.logger.error(f"告警回调执行失败: {e}")
    
    def _resolve_alert(self, rule: AlertRule, metric: MetricData):
        """
        解决告警
        
        Args:
            rule: 告警规则
            metric: 当前指标
        """
        alert_info = {
            'timestamp': datetime.now().isoformat(),
            'rule_name': rule.name,
            'metric_name': rule.metric_name,
            'current_value': metric.value,
            'threshold': rule.threshold,
            'severity': rule.severity,
            'status': 'resolved'
        }
        
        self.alert_history.append(alert_info)
        
        print(f"✅ 告警已解决: {rule.name}")
        print(f"   当前值: {metric.value:.2f} {metric.unit}")
    
    def get_active_alerts(self) -> List[Dict]:
        """
        获取活跃告警
        
        Returns:
            List[Dict]: 活跃告警列表
        """
        active_alerts = []
        
        for rule_key, state in self.alert_states.items():
            if state['notified']:
                active_alerts.append({
                    'rule_key': rule_key,
                    'first_triggered': state['first_triggered'].isoformat(),
                    'last_triggered': state['last_triggered'].isoformat(),
                    'count': state['count']
                })
        
        return active_alerts
    
    def get_alert_history(self, limit: int = 50) -> List[Dict]:
        """
        获取告警历史
        
        Args:
            limit: 返回数量限制
        
        Returns:
            List[Dict]: 告警历史列表
        """
        return list(self.alert_history)[-limit:]


class PerformanceAnalyzer:
    """
    性能分析器
    
    分析性能指标并提供优化建议
    """
    
    def __init__(self):
        self.analysis_history = deque(maxlen=100)
    
    def analyze_metrics(self, metrics: List[MetricData]) -> Dict:
        """
        分析性能指标
        
        Args:
            metrics: 指标数据列表
        
        Returns:
            Dict: 分析结果
        """
        if not metrics:
            return {'status': 'no_data', 'message': '没有可分析的数据'}
        
        # 按指标名称分组
        metrics_by_name = defaultdict(list)
        for metric in metrics:
            metrics_by_name[metric.metric_name].append(metric.value)
        
        analysis_result = {
            'timestamp': datetime.now().isoformat(),
            'metrics_analyzed': len(metrics),
            'time_range': self._get_time_range(metrics),
            'summary': {},
            'recommendations': [],
            'performance_score': 0
        }
        
        total_score = 0
        score_count = 0
        
        # 分析各个指标
        for metric_name, values in metrics_by_name.items():
            if not values:
                continue
            
            metric_analysis = self._analyze_metric(metric_name, values)
            analysis_result['summary'][metric_name] = metric_analysis
            
            # 计算性能评分
            if 'score' in metric_analysis:
                total_score += metric_analysis['score']
                score_count += 1
            
            # 生成建议
            recommendations = self._generate_recommendations(metric_name, metric_analysis)
            analysis_result['recommendations'].extend(recommendations)
        
        # 计算总体性能评分
        if score_count > 0:
            analysis_result['performance_score'] = total_score / score_count
        
        # 保存分析历史
        self.analysis_history.append(analysis_result)
        
        return analysis_result
    
    def _get_time_range(self, metrics: List[MetricData]) -> Dict:
        """
        获取时间范围
        
        Args:
            metrics: 指标数据列表
        
        Returns:
            Dict: 时间范围信息
        """
        timestamps = [datetime.fromisoformat(m.timestamp) for m in metrics]
        
        return {
            'start': min(timestamps).isoformat(),
            'end': max(timestamps).isoformat(),
            'duration_minutes': (max(timestamps) - min(timestamps)).total_seconds() / 60
        }
    
    def _analyze_metric(self, metric_name: str, values: List[float]) -> Dict:
        """
        分析单个指标
        
        Args:
            metric_name: 指标名称
            values: 指标值列表
        
        Returns:
            Dict: 指标分析结果
        """
        if not values:
            return {'status': 'no_data'}
        
        # 基本统计
        avg_value = sum(values) / len(values)
        min_value = min(values)
        max_value = max(values)
        
        # 计算趋势
        trend = self._calculate_trend(values)
        
        # 计算变异系数（稳定性指标）
        if avg_value > 0:
            std_dev = (sum((x - avg_value) ** 2 for x in values) / len(values)) ** 0.5
            cv = std_dev / avg_value
        else:
            cv = 0
        
        analysis = {
            'count': len(values),
            'average': round(avg_value, 2),
            'minimum': round(min_value, 2),
            'maximum': round(max_value, 2),
            'trend': trend,
            'stability': 'stable' if cv < 0.1 else 'unstable' if cv < 0.3 else 'highly_unstable',
            'coefficient_of_variation': round(cv, 3)
        }
        
        # 根据指标类型计算评分
        score = self._calculate_metric_score(metric_name, analysis)
        if score is not None:
            analysis['score'] = score
        
        return analysis
    
    def _calculate_trend(self, values: List[float]) -> str:
        """
        计算趋势
        
        Args:
            values: 数值列表
        
        Returns:
            str: 趋势描述
        """
        if len(values) < 2:
            return 'insufficient_data'
        
        # 简单线性回归计算趋势
        n = len(values)
        x = list(range(n))
        
        sum_x = sum(x)
        sum_y = sum(values)
        sum_xy = sum(x[i] * values[i] for i in range(n))
        sum_x2 = sum(xi ** 2 for xi in x)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        
        if abs(slope) < 0.01:
            return 'stable'
        elif slope > 0:
            return 'increasing'
        else:
            return 'decreasing'
    
    def _calculate_metric_score(self, metric_name: str, analysis: Dict) -> Optional[float]:
        """
        计算指标评分
        
        Args:
            metric_name: 指标名称
            analysis: 指标分析结果
        
        Returns:
            Optional[float]: 评分(0-100)
        """
        avg_value = analysis['average']
        
        # 根据不同指标类型计算评分
        if metric_name == 'cpu_usage':
            if avg_value < 50:
                return 100
            elif avg_value < 70:
                return 80
            elif avg_value < 85:
                return 60
            else:
                return 30
        
        elif metric_name == 'memory_usage':
            if avg_value < 60:
                return 100
            elif avg_value < 75:
                return 80
            elif avg_value < 90:
                return 60
            else:
                return 30
        
        elif metric_name == 'response_time':
            if avg_value < 100:
                return 100
            elif avg_value < 300:
                return 80
            elif avg_value < 500:
                return 60
            elif avg_value < 1000:
                return 40
            else:
                return 20
        
        elif metric_name == 'error_rate':
            if avg_value < 0.1:
                return 100
            elif avg_value < 1:
                return 80
            elif avg_value < 3:
                return 60
            elif avg_value < 5:
                return 40
            else:
                return 20
        
        return None
    
    def _generate_recommendations(self, metric_name: str, analysis: Dict) -> List[str]:
        """
        生成优化建议
        
        Args:
            metric_name: 指标名称
            analysis: 指标分析结果
        
        Returns:
            List[str]: 建议列表
        """
        recommendations = []
        avg_value = analysis['average']
        trend = analysis['trend']
        stability = analysis['stability']
        
        # CPU使用率建议
        if metric_name == 'cpu_usage':
            if avg_value > 80:
                recommendations.append("🔧 CPU使用率过高，建议优化算法或增加服务器资源")
            if trend == 'increasing':
                recommendations.append("📈 CPU使用率呈上升趋势，需要关注性能瓶颈")
            if stability == 'highly_unstable':
                recommendations.append("⚡ CPU使用率波动较大，检查是否有异常进程")
        
        # 内存使用率建议
        elif metric_name == 'memory_usage':
            if avg_value > 85:
                recommendations.append("💾 内存使用率过高，考虑增加内存或优化内存使用")
            if trend == 'increasing':
                recommendations.append("📊 内存使用率持续上升，检查是否存在内存泄漏")
        
        # 响应时间建议
        elif metric_name == 'response_time':
            if avg_value > 500:
                recommendations.append("🚀 响应时间过长，优化数据库查询和代码逻辑")
            if avg_value > 200:
                recommendations.append("⚡ 考虑添加缓存层以提高响应速度")
            if stability == 'unstable':
                recommendations.append("🔄 响应时间不稳定，检查网络和服务器负载")
        
        # 错误率建议
        elif metric_name == 'error_rate':
            if avg_value > 1:
                recommendations.append("🐛 错误率偏高，需要检查应用日志和错误处理")
            if trend == 'increasing':
                recommendations.append("⚠️ 错误率上升，立即检查系统状态")
        
        # 磁盘使用率建议
        elif metric_name == 'disk_usage':
            if avg_value > 90:
                recommendations.append("💿 磁盘空间不足，清理日志文件或扩容")
            elif avg_value > 80:
                recommendations.append("📁 磁盘使用率较高，建议定期清理")
        
        return recommendations
    
    def generate_performance_report(self, analysis_result: Dict) -> str:
        """
        生成性能报告
        
        Args:
            analysis_result: 分析结果
        
        Returns:
            str: 性能报告
        """
        report_lines = []
        report_lines.append("📊 性能分析报告")
        report_lines.append("=" * 50)
        
        # 基本信息
        report_lines.append(f"分析时间: {analysis_result['timestamp']}")
        report_lines.append(f"指标数量: {analysis_result['metrics_analyzed']}")
        report_lines.append(f"时间范围: {analysis_result['time_range']['duration_minutes']:.1f} 分钟")
        report_lines.append(f"性能评分: {analysis_result['performance_score']:.1f}/100")
        report_lines.append("")
        
        # 指标摘要
        report_lines.append("📈 指标摘要:")
        for metric_name, summary in analysis_result['summary'].items():
            score_text = f" (评分: {summary['score']:.1f})" if 'score' in summary else ""
            report_lines.append(f"  {metric_name}: 平均 {summary['average']}, 趋势 {summary['trend']}{score_text}")
        report_lines.append("")
        
        # 优化建议
        if analysis_result['recommendations']:
            report_lines.append("💡 优化建议:")
            for i, rec in enumerate(analysis_result['recommendations'], 1):
                report_lines.append(f"  {i}. {rec}")
        else:
            report_lines.append("✅ 系统运行良好，暂无优化建议")
        
        return "\n".join(report_lines)


def main():
    """
    主函数：演示监控与性能分析系统
    """
    print("Session30 示例3: 项目监控与性能分析")
    print("=" * 60)
    
    # 创建组件
    collector = MetricsCollector()
    alert_manager = AlertManager()
    analyzer = PerformanceAnalyzer()
    
    print("🚀 启动监控系统...")
    
    # 启动指标收集
    collector.start_collection()
    
    try:
        # 运行监控循环
        for i in range(6):  # 运行30秒
            print(f"\n⏰ 监控周期 {i+1}/6")
            
            # 等待收集数据
            time.sleep(5)
            
            # 获取最近的指标
            recent_metrics = collector.get_recent_metrics(limit=50)
            
            if recent_metrics:
                print(f"📊 收集到 {len(recent_metrics)} 个指标")
                
                # 检查告警
                alert_manager.check_alerts(recent_metrics)
                
                # 显示活跃告警
                active_alerts = alert_manager.get_active_alerts()
                if active_alerts:
                    print(f"🚨 活跃告警: {len(active_alerts)} 个")
                
                # 每3个周期进行一次性能分析
                if (i + 1) % 3 == 0:
                    print("\n🔍 执行性能分析...")
                    analysis_result = analyzer.analyze_metrics(recent_metrics)
                    
                    # 生成并显示报告
                    report = analyzer.generate_performance_report(analysis_result)
                    print("\n" + report)
            
            else:
                print("⏳ 等待数据收集...")
    
    except KeyboardInterrupt:
        print("\n⏹️ 用户中断监控")
    
    finally:
        # 停止收集
        collector.stop_collection()
        
        print("\n📋 监控总结:")
        
        # 显示告警历史
        alert_history = alert_manager.get_alert_history()
        if alert_history:
            print(f"📜 告警历史: {len(alert_history)} 条记录")
            for alert in alert_history[-3:]:  # 显示最近3条
                status_emoji = "🚨" if alert['status'] == 'triggered' else "✅"
                print(f"  {status_emoji} {alert['rule_name']}: {alert['current_value']:.2f}")
        
        # 显示最终指标统计
        all_metrics = collector.get_recent_metrics()
        if all_metrics:
            print(f"\n📊 总计收集指标: {len(all_metrics)} 个")
            
            # 按类型统计
            metric_counts = defaultdict(int)
            for metric in all_metrics:
                metric_counts[metric.metric_name] += 1
            
            print("📈 指标分布:")
            for metric_name, count in sorted(metric_counts.items()):
                print(f"  {metric_name}: {count} 个数据点")
        
        print("\n🎯 监控系统功能演示完成！")
        print("\n💡 实际应用建议:")
        print("1. 🔧 集成到现有应用中进行实时监控")
        print("2. 📊 配置Grafana等可视化工具")
        print("3. 🚨 设置邮件/短信告警通知")
        print("4. 📈 定期分析性能趋势")
        print("5. 🔄 根据分析结果优化系统")


if __name__ == "__main__":
    main()