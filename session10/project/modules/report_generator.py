#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session10 项目：报告生成模块

这个模块提供报告生成功能，包括：
- HTML报告生成
- Markdown报告生成
- JSON报告生成
- 图表和可视化
- 模板系统
- 多格式导出

作者：Python学习教程
版本：1.0.0
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from collections import defaultdict
import base64
from io import BytesIO

# 尝试导入可选依赖
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

try:
    from jinja2 import Template, Environment, FileSystemLoader
    HAS_JINJA2 = True
except ImportError:
    HAS_JINJA2 = False

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.offline import plot
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False


class ReportGenerator:
    """
    报告生成器类
    
    提供多种格式的报告生成功能，支持模板和可视化。
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化报告生成器
        
        Args:
            config: 配置字典
        """
        self.config = self._load_config(config or {})
        self.templates = {}
        self.charts = []
        self.report_data = {}
        self.metadata = {
            'generated_at': datetime.now(),
            'generator_version': '1.0.0',
            'python_version': None
        }
        
        # 初始化模板环境
        if HAS_JINJA2:
            self.jinja_env = Environment(
                loader=FileSystemLoader(self.config['template_dir'])
            )
    
    def _load_config(self, config: Dict) -> Dict:
        """
        加载和验证配置
        
        Args:
            config: 用户配置
            
        Returns:
            完整的配置字典
        """
        default_config = {
            'output_dir': 'reports',
            'template_dir': 'templates',
            'default_format': 'html',
            'include_charts': True,
            'chart_format': 'png',
            'chart_dpi': 300,
            'chart_width': 10,
            'chart_height': 6,
            'html_theme': 'default',
            'css_framework': 'bootstrap',
            'include_toc': True,
            'include_summary': True,
            'include_details': True,
            'max_items_per_section': 100,
            'date_format': '%Y-%m-%d %H:%M:%S',
            'number_format': '.2f',
            'encoding': 'utf-8',
            'auto_open': False
        }
        
        # 合并配置
        merged_config = default_config.copy()
        merged_config.update(config)
        
        # 确保输出目录存在
        output_dir = Path(merged_config['output_dir'])
        output_dir.mkdir(parents=True, exist_ok=True)
        
        return merged_config
    
    def generate_analysis_report(self, analysis_data: Dict, output_path: Optional[str] = None) -> str:
        """
        生成文件分析报告
        
        Args:
            analysis_data: 分析数据
            output_path: 输出路径
            
        Returns:
            生成的报告文件路径
        """
        print("生成文件分析报告...")
        
        # 准备报告数据
        self.report_data = self._prepare_analysis_data(analysis_data)
        
        # 生成图表
        if self.config['include_charts']:
            self._generate_analysis_charts()
        
        # 确定输出路径
        if not output_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"analysis_report_{timestamp}.{self.config['default_format']}"
            output_path = Path(self.config['output_dir']) / filename
        
        # 根据格式生成报告
        format_type = Path(output_path).suffix.lower().lstrip('.')
        
        if format_type == 'html':
            return self._generate_html_report(output_path)
        elif format_type == 'md':
            return self._generate_markdown_report(output_path)
        elif format_type == 'json':
            return self._generate_json_report(output_path)
        else:
            raise ValueError(f"不支持的报告格式: {format_type}")
    
    def generate_data_report(self, data: Any, statistics: Dict, output_path: Optional[str] = None) -> str:
        """
        生成数据处理报告
        
        Args:
            data: 处理后的数据
            statistics: 统计信息
            output_path: 输出路径
            
        Returns:
            生成的报告文件路径
        """
        print("生成数据处理报告...")
        
        # 准备报告数据
        self.report_data = self._prepare_data_report(data, statistics)
        
        # 生成图表
        if self.config['include_charts']:
            self._generate_data_charts(statistics)
        
        # 确定输出路径
        if not output_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"data_report_{timestamp}.{self.config['default_format']}"
            output_path = Path(self.config['output_dir']) / filename
        
        # 根据格式生成报告
        format_type = Path(output_path).suffix.lower().lstrip('.')
        
        if format_type == 'html':
            return self._generate_html_report(output_path)
        elif format_type == 'md':
            return self._generate_markdown_report(output_path)
        elif format_type == 'json':
            return self._generate_json_report(output_path)
        else:
            raise ValueError(f"不支持的报告格式: {format_type}")
    
    def _prepare_analysis_data(self, analysis_data: Dict) -> Dict:
        """
        准备分析数据
        
        Args:
            analysis_data: 原始分析数据
            
        Returns:
            格式化的报告数据
        """
        report_data = {
            'title': '文件分析报告',
            'summary': {},
            'details': {},
            'charts': [],
            'metadata': self.metadata.copy()
        }
        
        # 摘要信息
        summary = analysis_data.get('summary', {})
        report_data['summary'] = {
            'total_files': summary.get('total_files', 0),
            'total_directories': summary.get('total_directories', 0),
            'total_size': self._format_size(summary.get('total_size', 0)),
            'file_types': summary.get('file_types', {}),
            'largest_files': summary.get('largest_files', [])[:5],
            'analysis_time': summary.get('analysis_time', 0)
        }
        
        # 详细信息
        files = analysis_data.get('files', [])
        report_data['details'] = {
            'files': files[:self.config['max_items_per_section']],
            'file_count': len(files),
            'truncated': len(files) > self.config['max_items_per_section']
        }
        
        # 统计信息
        report_data['statistics'] = self._calculate_file_statistics(files)
        
        return report_data
    
    def _prepare_data_report(self, data: Any, statistics: Dict) -> Dict:
        """
        准备数据报告
        
        Args:
            data: 数据
            statistics: 统计信息
            
        Returns:
            格式化的报告数据
        """
        report_data = {
            'title': '数据处理报告',
            'summary': {},
            'details': {},
            'charts': [],
            'metadata': self.metadata.copy()
        }
        
        # 摘要信息
        if isinstance(data, list) and data and isinstance(data[0], dict):
            # 字典列表
            report_data['summary'] = {
                'data_type': '结构化数据',
                'record_count': statistics.get('record_count', 0),
                'field_count': statistics.get('field_count', 0),
                'data_quality': self._assess_data_quality(statistics)
            }
        elif isinstance(data, list):
            # 字符串列表
            report_data['summary'] = {
                'data_type': '文本数据',
                'line_count': statistics.get('line_count', 0),
                'word_count': statistics.get('word_count', 0),
                'unique_lines': statistics.get('unique_lines', 0)
            }
        else:
            report_data['summary'] = {
                'data_type': type(data).__name__,
                'size': len(str(data))
            }
        
        # 详细统计
        report_data['statistics'] = statistics
        
        # 数据样本
        if isinstance(data, list):
            sample_size = min(10, len(data))
            report_data['sample_data'] = data[:sample_size]
        
        return report_data
    
    def _calculate_file_statistics(self, files: List[Dict]) -> Dict:
        """
        计算文件统计信息
        
        Args:
            files: 文件列表
            
        Returns:
            统计信息
        """
        if not files:
            return {}
        
        # 扩展名统计
        extension_counts = defaultdict(int)
        extension_sizes = defaultdict(int)
        
        # 大小统计
        sizes = []
        
        # 代码文件统计
        code_files = 0
        total_lines = 0
        
        for file_info in files:
            ext = file_info.get('extension', '').lower()
            size = file_info.get('size', 0)
            
            extension_counts[ext] += 1
            extension_sizes[ext] += size
            sizes.append(size)
            
            if ext in ['.py', '.js', '.java', '.cpp', '.c', '.h']:
                code_files += 1
                total_lines += file_info.get('line_count', 0)
        
        # 计算统计值
        total_size = sum(sizes)
        avg_size = total_size / len(sizes) if sizes else 0
        
        return {
            'extension_distribution': dict(extension_counts),
            'size_distribution': dict(extension_sizes),
            'total_size': total_size,
            'average_size': avg_size,
            'largest_file': max(sizes) if sizes else 0,
            'smallest_file': min(sizes) if sizes else 0,
            'code_files': code_files,
            'total_lines': total_lines,
            'average_lines_per_file': total_lines / code_files if code_files > 0 else 0
        }
    
    def _assess_data_quality(self, statistics: Dict) -> Dict:
        """
        评估数据质量
        
        Args:
            statistics: 统计信息
            
        Returns:
            数据质量评估
        """
        quality = {
            'completeness': 0,
            'consistency': 0,
            'accuracy': 0,
            'overall': 0
        }
        
        fields = statistics.get('fields', {})
        if fields:
            # 完整性：基于缺失值比例
            null_percentages = [field.get('null_percentage', 0) for field in fields.values()]
            avg_null_percentage = sum(null_percentages) / len(null_percentages)
            quality['completeness'] = max(0, 100 - avg_null_percentage)
            
            # 一致性：基于数据类型一致性
            type_consistency = []
            for field_stats in fields.values():
                field_types = field_stats.get('field_types', {})
                if field_types:
                    # 主要类型占比
                    total_count = sum(field_types.values())
                    main_type_count = max(field_types.values())
                    consistency = (main_type_count / total_count) * 100
                    type_consistency.append(consistency)
            
            if type_consistency:
                quality['consistency'] = sum(type_consistency) / len(type_consistency)
            
            # 准确性：基于唯一值比例（简化评估）
            unique_percentages = []
            for field_stats in fields.values():
                unique_info = field_stats.get('unique_values', {})
                unique_percentage = unique_info.get('percentage', 0)
                # 对于某些字段，高唯一性是好的（如ID），对其他字段可能不是
                # 这里使用简化的评估
                if unique_percentage > 90:  # 可能是ID字段
                    unique_percentages.append(100)
                elif unique_percentage < 10:  # 可能是分类字段
                    unique_percentages.append(80)
                else:  # 中等唯一性
                    unique_percentages.append(60)
            
            if unique_percentages:
                quality['accuracy'] = sum(unique_percentages) / len(unique_percentages)
        
        # 总体质量
        quality['overall'] = (quality['completeness'] + quality['consistency'] + quality['accuracy']) / 3
        
        return quality
    
    def _generate_analysis_charts(self):
        """
        生成分析图表
        """
        if not HAS_MATPLOTLIB:
            print("matplotlib未安装，跳过图表生成")
            return
        
        summary = self.report_data.get('summary', {})
        statistics = self.report_data.get('statistics', {})
        
        # 文件类型分布饼图
        file_types = summary.get('file_types', {})
        if file_types:
            self._create_pie_chart(
                file_types,
                '文件类型分布',
                'file_types_distribution'
            )
        
        # 文件大小分布柱状图
        size_distribution = statistics.get('size_distribution', {})
        if size_distribution:
            self._create_bar_chart(
                size_distribution,
                '文件大小分布（按扩展名）',
                'size_distribution',
                ylabel='大小 (字节)'
            )
    
    def _generate_data_charts(self, statistics: Dict):
        """
        生成数据图表
        
        Args:
            statistics: 统计信息
        """
        if not HAS_MATPLOTLIB:
            print("matplotlib未安装，跳过图表生成")
            return
        
        # 字段类型分布
        if 'field_types' in statistics:
            field_types = statistics['field_types']
            for field_name, types in field_types.items():
                if types:
                    self._create_pie_chart(
                        types,
                        f'{field_name} 字段类型分布',
                        f'field_types_{field_name}'
                    )
        
        # 缺失值分析
        if 'fields' in statistics:
            fields = statistics['fields']
            missing_data = {}
            for field_name, field_stats in fields.items():
                null_percentage = field_stats.get('null_percentage', 0)
                if null_percentage > 0:
                    missing_data[field_name] = null_percentage
            
            if missing_data:
                self._create_bar_chart(
                    missing_data,
                    '字段缺失值百分比',
                    'missing_values',
                    ylabel='缺失值百分比 (%)'
                )
    
    def _create_pie_chart(self, data: Dict, title: str, filename: str):
        """
        创建饼图
        
        Args:
            data: 数据字典
            title: 图表标题
            filename: 文件名
        """
        try:
            plt.figure(figsize=(self.config['chart_width'], self.config['chart_height']))
            
            labels = list(data.keys())
            values = list(data.values())
            
            plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
            plt.title(title)
            plt.axis('equal')
            
            # 保存图表
            chart_path = self._save_chart(filename)
            self.charts.append({
                'type': 'pie',
                'title': title,
                'filename': filename,
                'path': chart_path
            })
            
            plt.close()
            
        except Exception as e:
            print(f"创建饼图失败: {e}")
    
    def _create_bar_chart(self, data: Dict, title: str, filename: str, ylabel: str = '数量'):
        """
        创建柱状图
        
        Args:
            data: 数据字典
            title: 图表标题
            filename: 文件名
            ylabel: Y轴标签
        """
        try:
            plt.figure(figsize=(self.config['chart_width'], self.config['chart_height']))
            
            labels = list(data.keys())
            values = list(data.values())
            
            plt.bar(labels, values)
            plt.title(title)
            plt.xlabel('类别')
            plt.ylabel(ylabel)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            # 保存图表
            chart_path = self._save_chart(filename)
            self.charts.append({
                'type': 'bar',
                'title': title,
                'filename': filename,
                'path': chart_path
            })
            
            plt.close()
            
        except Exception as e:
            print(f"创建柱状图失败: {e}")
    
    def _save_chart(self, filename: str) -> str:
        """
        保存图表
        
        Args:
            filename: 文件名
            
        Returns:
            保存的文件路径
        """
        chart_filename = f"{filename}.{self.config['chart_format']}"
        chart_path = Path(self.config['output_dir']) / chart_filename
        
        plt.savefig(
            chart_path,
            format=self.config['chart_format'],
            dpi=self.config['chart_dpi'],
            bbox_inches='tight'
        )
        
        return str(chart_path)
    
    def _generate_html_report(self, output_path: str) -> str:
        """
        生成HTML报告
        
        Args:
            output_path: 输出路径
            
        Returns:
            生成的文件路径
        """
        print(f"生成HTML报告: {output_path}")
        
        # 使用模板（如果可用）
        if HAS_JINJA2:
            return self._generate_html_with_template(output_path)
        else:
            return self._generate_html_builtin(output_path)
    
    def _generate_html_with_template(self, output_path: str) -> str:
        """
        使用Jinja2模板生成HTML报告
        
        Args:
            output_path: 输出路径
            
        Returns:
            生成的文件路径
        """
        try:
            template = self.jinja_env.get_template('report_template.html')
            html_content = template.render(
                report_data=self.report_data,
                charts=self.charts,
                config=self.config
            )
        except Exception as e:
            print(f"模板渲染失败，使用内置方法: {e}")
            return self._generate_html_builtin(output_path)
        
        with open(output_path, 'w', encoding=self.config['encoding']) as f:
            f.write(html_content)
        
        return str(output_path)
    
    def _generate_html_builtin(self, output_path: str) -> str:
        """
        使用内置方法生成HTML报告
        
        Args:
            output_path: 输出路径
            
        Returns:
            生成的文件路径
        """
        html_content = self._build_html_content()
        
        with open(output_path, 'w', encoding=self.config['encoding']) as f:
            f.write(html_content)
        
        return str(output_path)
    
    def _build_html_content(self) -> str:
        """
        构建HTML内容
        
        Returns:
            HTML内容字符串
        """
        title = self.report_data.get('title', '报告')
        
        html_parts = [
            '<!DOCTYPE html>',
            '<html lang="zh-CN">',
            '<head>',
            '    <meta charset="UTF-8">',
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            f'    <title>{title}</title>',
            '    <style>',
            self._get_default_css(),
            '    </style>',
            '</head>',
            '<body>',
            '    <div class="container">',
            f'        <h1>{title}</h1>',
        ]
        
        # 添加摘要部分
        if self.config['include_summary']:
            html_parts.extend(self._build_summary_section())
        
        # 添加图表部分
        if self.config['include_charts'] and self.charts:
            html_parts.extend(self._build_charts_section())
        
        # 添加详细信息部分
        if self.config['include_details']:
            html_parts.extend(self._build_details_section())
        
        # 添加元数据部分
        html_parts.extend(self._build_metadata_section())
        
        html_parts.extend([
            '    </div>',
            '</body>',
            '</html>'
        ])
        
        return '\n'.join(html_parts)
    
    def _get_default_css(self) -> str:
        """
        获取默认CSS样式
        
        Returns:
            CSS样式字符串
        """
        return """
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1, h2, h3 {
            color: #333;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .summary-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 6px;
            border-left: 4px solid #007bff;
        }
        .summary-card h4 {
            margin: 0 0 10px 0;
            color: #007bff;
        }
        .summary-card .value {
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }
        .chart-container {
            text-align: center;
            margin: 20px 0;
        }
        .chart-container img {
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #007bff;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .metadata {
            background: #e9ecef;
            padding: 15px;
            border-radius: 4px;
            margin-top: 30px;
            font-size: 0.9em;
        }
        .progress-bar {
            width: 100%;
            height: 20px;
            background-color: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background-color: #007bff;
            transition: width 0.3s ease;
        }
        """
    
    def _build_summary_section(self) -> List[str]:
        """
        构建摘要部分
        
        Returns:
            HTML行列表
        """
        summary = self.report_data.get('summary', {})
        
        html_parts = [
            '        <h2>摘要信息</h2>',
            '        <div class="summary-grid">'
        ]
        
        for key, value in summary.items():
            if isinstance(value, (int, float, str)):
                display_key = key.replace('_', ' ').title()
                html_parts.extend([
                    '            <div class="summary-card">',
                    f'                <h4>{display_key}</h4>',
                    f'                <div class="value">{value}</div>',
                    '            </div>'
                ])
        
        html_parts.append('        </div>')
        
        return html_parts
    
    def _build_charts_section(self) -> List[str]:
        """
        构建图表部分
        
        Returns:
            HTML行列表
        """
        html_parts = [
            '        <h2>图表分析</h2>'
        ]
        
        for chart in self.charts:
            chart_path = Path(chart['path'])
            if chart_path.exists():
                # 转换为相对路径或base64编码
                img_src = chart_path.name  # 假设图片在同一目录
                
                html_parts.extend([
                    '        <div class="chart-container">',
                    f'            <h3>{chart["title"]}</h3>',
                    f'            <img src="{img_src}" alt="{chart["title"]}">',
                    '        </div>'
                ])
        
        return html_parts
    
    def _build_details_section(self) -> List[str]:
        """
        构建详细信息部分
        
        Returns:
            HTML行列表
        """
        details = self.report_data.get('details', {})
        
        html_parts = [
            '        <h2>详细信息</h2>'
        ]
        
        # 如果有文件列表
        files = details.get('files', [])
        if files:
            html_parts.extend([
                '        <h3>文件列表</h3>',
                '        <table>',
                '            <thead>',
                '                <tr>',
                '                    <th>文件名</th>',
                '                    <th>大小</th>',
                '                    <th>类型</th>',
                '                    <th>修改时间</th>',
                '                </tr>',
                '            </thead>',
                '            <tbody>'
            ])
            
            for file_info in files[:50]:  # 限制显示数量
                name = file_info.get('name', '')
                size = self._format_size(file_info.get('size', 0))
                ext = file_info.get('extension', '')
                modified = file_info.get('modified_time', '')
                
                html_parts.extend([
                    '                <tr>',
                    f'                    <td>{name}</td>',
                    f'                    <td>{size}</td>',
                    f'                    <td>{ext}</td>',
                    f'                    <td>{modified}</td>',
                    '                </tr>'
                ])
            
            html_parts.extend([
                '            </tbody>',
                '        </table>'
            ])
            
            if details.get('truncated', False):
                html_parts.append('        <p><em>注：由于数量较多，仅显示前50个文件。</em></p>')
        
        return html_parts
    
    def _build_metadata_section(self) -> List[str]:
        """
        构建元数据部分
        
        Returns:
            HTML行列表
        """
        metadata = self.report_data.get('metadata', {})
        
        html_parts = [
            '        <div class="metadata">',
            '            <h3>报告信息</h3>'
        ]
        
        for key, value in metadata.items():
            if value is not None:
                display_key = key.replace('_', ' ').title()
                if isinstance(value, datetime):
                    value = value.strftime(self.config['date_format'])
                
                html_parts.append(f'            <p><strong>{display_key}:</strong> {value}</p>')
        
        html_parts.append('        </div>')
        
        return html_parts
    
    def _generate_markdown_report(self, output_path: str) -> str:
        """
        生成Markdown报告
        
        Args:
            output_path: 输出路径
            
        Returns:
            生成的文件路径
        """
        print(f"生成Markdown报告: {output_path}")
        
        markdown_content = self._build_markdown_content()
        
        with open(output_path, 'w', encoding=self.config['encoding']) as f:
            f.write(markdown_content)
        
        return str(output_path)
    
    def _build_markdown_content(self) -> str:
        """
        构建Markdown内容
        
        Returns:
            Markdown内容字符串
        """
        title = self.report_data.get('title', '报告')
        
        md_parts = [
            f"# {title}",
            "",
            f"生成时间: {datetime.now().strftime(self.config['date_format'])}",
            ""
        ]
        
        # 添加摘要
        if self.config['include_summary']:
            md_parts.extend(self._build_markdown_summary())
        
        # 添加图表
        if self.config['include_charts'] and self.charts:
            md_parts.extend(self._build_markdown_charts())
        
        # 添加详细信息
        if self.config['include_details']:
            md_parts.extend(self._build_markdown_details())
        
        return "\n".join(md_parts)
    
    def _build_markdown_summary(self) -> List[str]:
        """
        构建Markdown摘要
        
        Returns:
            Markdown行列表
        """
        summary = self.report_data.get('summary', {})
        
        md_parts = [
            "## 摘要信息",
            ""
        ]
        
        for key, value in summary.items():
            if isinstance(value, (int, float, str)):
                display_key = key.replace('_', ' ').title()
                md_parts.append(f"- **{display_key}**: {value}")
        
        md_parts.append("")
        
        return md_parts
    
    def _build_markdown_charts(self) -> List[str]:
        """
        构建Markdown图表
        
        Returns:
            Markdown行列表
        """
        md_parts = [
            "## 图表分析",
            ""
        ]
        
        for chart in self.charts:
            chart_path = Path(chart['path'])
            if chart_path.exists():
                md_parts.extend([
                    f"### {chart['title']}",
                    "",
                    f"![{chart['title']}]({chart_path.name})",
                    ""
                ])
        
        return md_parts
    
    def _build_markdown_details(self) -> List[str]:
        """
        构建Markdown详细信息
        
        Returns:
            Markdown行列表
        """
        details = self.report_data.get('details', {})
        
        md_parts = [
            "## 详细信息",
            ""
        ]
        
        # 文件列表
        files = details.get('files', [])
        if files:
            md_parts.extend([
                "### 文件列表",
                "",
                "| 文件名 | 大小 | 类型 | 修改时间 |",
                "|--------|------|------|----------|"
            ])
            
            for file_info in files[:50]:
                name = file_info.get('name', '')
                size = self._format_size(file_info.get('size', 0))
                ext = file_info.get('extension', '')
                modified = file_info.get('modified_time', '')
                
                md_parts.append(f"| {name} | {size} | {ext} | {modified} |")
            
            md_parts.append("")
            
            if details.get('truncated', False):
                md_parts.append("*注：由于数量较多，仅显示前50个文件。*")
                md_parts.append("")
        
        return md_parts
    
    def _generate_json_report(self, output_path: str) -> str:
        """
        生成JSON报告
        
        Args:
            output_path: 输出路径
            
        Returns:
            生成的文件路径
        """
        print(f"生成JSON报告: {output_path}")
        
        # 准备JSON数据
        json_data = self.report_data.copy()
        
        # 处理datetime对象
        json_data = self._serialize_datetime(json_data)
        
        with open(output_path, 'w', encoding=self.config['encoding']) as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        return str(output_path)
    
    def _serialize_datetime(self, obj: Any) -> Any:
        """
        序列化datetime对象
        
        Args:
            obj: 对象
            
        Returns:
            序列化后的对象
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {key: self._serialize_datetime(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._serialize_datetime(item) for item in obj]
        else:
            return obj
    
    def _format_size(self, size_bytes: int) -> str:
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
    
    def create_custom_report(self, data: Dict, template_name: str, output_path: str) -> str:
        """
        创建自定义报告
        
        Args:
            data: 报告数据
            template_name: 模板名称
            output_path: 输出路径
            
        Returns:
            生成的文件路径
        """
        if not HAS_JINJA2:
            raise ValueError("需要安装jinja2才能使用自定义模板")
        
        try:
            template = self.jinja_env.get_template(template_name)
            content = template.render(data=data, config=self.config)
            
            with open(output_path, 'w', encoding=self.config['encoding']) as f:
                f.write(content)
            
            return str(output_path)
            
        except Exception as e:
            raise ValueError(f"生成自定义报告失败: {e}")
    
    def get_available_formats(self) -> List[str]:
        """
        获取可用的报告格式
        
        Returns:
            格式列表
        """
        return ['html', 'md', 'json']
    
    def clear_charts(self):
        """
        清除生成的图表
        """
        for chart in self.charts:
            chart_path = Path(chart['path'])
            if chart_path.exists():
                try:
                    chart_path.unlink()
                except Exception as e:
                    print(f"删除图表文件失败: {e}")
        
        self.charts.clear()


# 便捷函数
def quick_html_report(data: Dict, output_path: str, title: str = "快速报告") -> str:
    """
    快速生成HTML报告
    
    Args:
        data: 数据
        output_path: 输出路径
        title: 报告标题
        
    Returns:
        生成的文件路径
    """
    generator = ReportGenerator()
    generator.report_data = {
        'title': title,
        'summary': data,
        'metadata': {'generated_at': datetime.now()}
    }
    
    return generator._generate_html_report(output_path)


def create_analysis_summary(analysis_data: Dict) -> str:
    """
    创建分析摘要
    
    Args:
        analysis_data: 分析数据
        
    Returns:
        摘要字符串
    """
    summary = analysis_data.get('summary', {})
    
    lines = [
        "文件分析摘要:",
        f"总文件数: {summary.get('total_files', 0)}",
        f"总目录数: {summary.get('total_directories', 0)}",
        f"总大小: {summary.get('total_size', 0)} 字节",
        f"分析时间: {summary.get('analysis_time', 0):.2f} 秒"
    ]
    
    return "\n".join(lines)


# 如果直接运行此模块，进行演示
if __name__ == '__main__':
    print("=== 报告生成器演示 ===")
    
    # 创建示例数据
    sample_analysis_data = {
        'summary': {
            'total_files': 25,
            'total_directories': 5,
            'total_size': 1024000,
            'file_types': {'.py': 15, '.txt': 5, '.md': 3, '.json': 2},
            'analysis_time': 1.5
        },
        'files': [
            {'name': 'main.py', 'size': 2048, 'extension': '.py', 'modified_time': '2024-01-01 10:00:00'},
            {'name': 'config.json', 'size': 512, 'extension': '.json', 'modified_time': '2024-01-01 09:30:00'},
            {'name': 'README.md', 'size': 1024, 'extension': '.md', 'modified_time': '2024-01-01 09:00:00'}
        ]
    }
    
    generator = ReportGenerator()
    
    # 演示HTML报告生成
    print("\n=== HTML报告生成演示 ===")
    html_path = generator.generate_analysis_report(
        sample_analysis_data,
        'demo_report.html'
    )
    print(f"HTML报告已生成: {html_path}")
    
    # 演示Markdown报告生成
    print("\n=== Markdown报告生成演示 ===")
    md_path = generator.generate_analysis_report(
        sample_analysis_data,
        'demo_report.md'
    )
    print(f"Markdown报告已生成: {md_path}")
    
    # 演示JSON报告生成
    print("\n=== JSON报告生成演示 ===")
    json_path = generator.generate_analysis_report(
        sample_analysis_data,
        'demo_report.json'
    )
    print(f"JSON报告已生成: {json_path}")
    
    # 演示快速报告
    print("\n=== 快速报告演示 ===")
    quick_data = {
        '处理文件数': 10,
        '总大小': '2.5 MB',
        '处理时间': '3.2 秒'
    }
    
    quick_path = quick_html_report(quick_data, 'quick_report.html', '快速处理报告')
    print(f"快速报告已生成: {quick_path}")
    
    # 显示可用格式
    print("\n=== 可用格式 ===")
    formats = generator.get_available_formats()
    print(f"支持的报告格式: {', '.join(formats)}")