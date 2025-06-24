#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session23 练习2解决方案：代码格式化和工具配置练习

这是exercise2.py的修复版本，展示了：
1. 正确的代码格式化
2. 完整的类型注解
3. 安全的编程实践
4. 良好的代码结构
5. 适当的异常处理

作者: Python教程团队
创建日期: 2024-01-01
"""

import hashlib
import json
import os
import re
import secrets
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class DataProcessingError(Exception):
    """数据处理错误异常"""
    pass


class ConfigurationError(Exception):
    """配置错误异常"""
    pass


class DataProcessor:
    """
    数据处理器类
    
    负责加载配置、验证数据、处理数据批次和生成报告。
    提供安全的文件操作和错误处理。
    """
    
    def __init__(self, config_file: str, debug: bool = False) -> None:
        """
        初始化数据处理器
        
        Args:
            config_file: 配置文件路径
            debug: 是否启用调试模式
        """
        self.config_file: str = config_file
        self.debug: bool = debug
        self.data: List[Dict[str, Any]] = []
        self.processed_count: int = 0
        self._validate_config_file()
    
    def _validate_config_file(self) -> None:
        """
        验证配置文件路径的安全性
        
        Raises:
            ConfigurationError: 配置文件路径不安全
        """
        config_path = Path(self.config_file)
        try:
            # 确保路径在当前工作目录内
            config_path.resolve().relative_to(Path.cwd().resolve())
        except ValueError as e:
            raise ConfigurationError(
                f"配置文件路径不安全: {self.config_file}"
            ) from e
    
    def load_config(self) -> Dict[str, Any]:
        """
        加载配置文件
        
        Returns:
            配置字典
            
        Raises:
            ConfigurationError: 配置文件加载失败
        """
        config_path = Path(self.config_file)
        
        if not config_path.exists():
            if self.debug:
                print(f"配置文件不存在: {self.config_file}，使用默认配置")
            return {"default": True, "transform": False, "add_hash": False}
        
        try:
            with config_path.open('r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 验证配置格式
            if not isinstance(config, dict):
                raise ConfigurationError("配置文件格式错误：期望JSON对象")
            
            return config
            
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"配置文件JSON格式错误: {e}") from e
        except OSError as e:
            raise ConfigurationError(f"无法读取配置文件: {e}") from e
    
    def validate_data(self, item: Any) -> bool:
        """
        验证数据项格式
        
        Args:
            item: 要验证的数据项
            
        Returns:
            数据是否有效
        """
        if not isinstance(item, dict):
            return False
        
        required_fields = ['id', 'name', 'value']
        for field in required_fields:
            if field not in item:
                return False
            
            # 验证字段类型
            if field == 'id' and not isinstance(item[field], int):
                return False
            elif field == 'name' and (
                not isinstance(item[field], str) or not item[field].strip()
            ):
                return False
        
        return True
    
    def process_item(
        self,
        item: Dict[str, Any],
        config: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        处理单个数据项
        
        Args:
            item: 要处理的数据项
            config: 处理配置
            
        Returns:
            处理后的数据项，如果处理失败则返回None
        """
        if not self.validate_data(item):
            if self.debug:
                print(f"数据验证失败: {item}")
            return None
        
        # 创建处理结果
        result: Dict[str, Any] = {
            'id': item['id'],
            'name': item['name'],
            'value': item['value'],
            'processed': True,
            'timestamp': self._get_current_timestamp()
        }
        
        # 应用转换
        if config.get('transform', False):
            result['value'] = self._transform_value(item['value'])
        
        # 添加安全哈希
        if config.get('add_hash', False):
            result['hash'] = self._generate_secure_hash(item)
        
        return result
    
    def _transform_value(self, value: Any) -> Any:
        """
        转换数据值
        
        Args:
            value: 原始值
            
        Returns:
            转换后的值
        """
        if isinstance(value, str):
            return value.upper()
        elif isinstance(value, (int, float)):
            return value * 2
        else:
            return value
    
    def _generate_secure_hash(self, item: Dict[str, Any]) -> str:
        """
        生成安全哈希值
        
        Args:
            item: 数据项
            
        Returns:
            SHA256哈希值
        """
        # 使用SHA256替代不安全的MD5
        hash_input = f"{item['id']}{item['name']}{item['value']}"
        return hashlib.sha256(hash_input.encode('utf-8')).hexdigest()
    
    def _get_current_timestamp(self) -> str:
        """
        获取当前时间戳
        
        Returns:
            ISO格式的时间戳字符串
        """
        from datetime import datetime
        return datetime.now().isoformat()
    
    def process_batch(
        self,
        data_batch: List[Dict[str, Any]],
        config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        批量处理数据
        
        Args:
            data_batch: 数据批次
            config: 处理配置
            
        Returns:
            处理结果列表
            
        Raises:
            DataProcessingError: 批量处理失败
        """
        if not isinstance(data_batch, list):
            raise DataProcessingError("数据批次必须是列表类型")
        
        results: List[Dict[str, Any]] = []
        
        for i, item in enumerate(data_batch):
            try:
                processed = self.process_item(item, config)
                if processed:
                    results.append(processed)
                self.processed_count += 1
                
                if self.debug:
                    print(f"处理项目 {i + 1}/{len(data_batch)}: {'成功' if processed else '失败'}")
                    
            except Exception as e:
                if self.debug:
                    print(f"处理项目 {i + 1} 时出错: {e}")
                # 继续处理其他项目，不中断整个批次
                continue
        
        return results
    
    def save_results(
        self,
        results: List[Dict[str, Any]],
        output_file: str
    ) -> None:
        """
        保存处理结果到文件
        
        Args:
            results: 处理结果列表
            output_file: 输出文件路径
            
        Raises:
            DataProcessingError: 保存失败
        """
        output_path = Path(output_file)
        
        # 验证输出路径安全性
        try:
            output_path.resolve().relative_to(Path.cwd().resolve())
        except ValueError as e:
            raise DataProcessingError(
                f"输出文件路径不安全: {output_file}"
            ) from e
        
        # 确保目录存在
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with output_path.open('w', encoding='utf-8') as f:
                json.dump(
                    results,
                    f,
                    indent=2,
                    ensure_ascii=False,
                    sort_keys=True
                )
            
            if self.debug:
                print(f"结果已保存到: {output_file}")
                
        except (OSError, json.JSONEncodeError) as e:
            raise DataProcessingError(f"保存结果失败: {e}") from e
    
    def generate_report(self, results: List[Dict[str, Any]]) -> Dict[str, Union[int, float]]:
        """
        生成处理报告
        
        Args:
            results: 处理结果列表
            
        Returns:
            包含统计信息的报告字典
        """
        total = len(results)
        valid = sum(1 for r in results if r.get('processed', False))
        
        report: Dict[str, Union[int, float]] = {
            'total_items': total,
            'valid_items': valid,
            'invalid_items': total - valid,
            'processing_rate': round(valid / total, 4) if total > 0 else 0.0,
            'processed_count': self.processed_count
        }
        
        return report


def create_sample_data() -> List[Dict[str, Any]]:
    """
    创建示例数据
    
    Returns:
        示例数据列表
    """
    return [
        {'id': 1, 'name': 'item1', 'value': 'test'},
        {'id': 2, 'name': 'item2', 'value': 42},
        {'id': 3, 'name': 'item3', 'value': 3.14},
        {'id': 4, 'name': '', 'value': 'invalid'},  # 无效：空名称
        {'name': 'item5', 'value': 'missing_id'},  # 无效：缺少ID
        {'id': 5, 'name': 'item6', 'value': [1, 2, 3]},  # 复杂值类型
    ]


def create_config_file(filename: str) -> None:
    """
    创建配置文件
    
    Args:
        filename: 配置文件名
        
    Raises:
        OSError: 文件创建失败
    """
    config = {
        'transform': True,
        'add_hash': True,
        'debug': False,
        'version': '1.0',
        'description': 'Data processing configuration'
    }
    
    config_path = Path(filename)
    
    try:
        with config_path.open('w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"配置文件已创建: {filename}")
    except OSError as e:
        raise OSError(f"创建配置文件失败: {e}") from e


def cleanup_files(*filenames: str) -> None:
    """
    清理临时文件
    
    Args:
        *filenames: 要删除的文件名列表
    """
    for filename in filenames:
        file_path = Path(filename)
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"已删除临时文件: {filename}")
            except OSError as e:
                print(f"删除文件失败 {filename}: {e}")


def main() -> None:
    """
    主函数：演示数据处理器的使用
    
    包含完整的错误处理和资源清理。
    """
    print("Session23 练习2解决方案：数据处理系统")
    print("=" * 50)
    
    config_file = 'config.json'
    output_file = 'results.json'
    
    try:
        # 创建配置文件
        print("\n1. 创建配置文件")
        create_config_file(config_file)
        
        # 初始化处理器
        print("\n2. 初始化数据处理器")
        processor = DataProcessor(config_file, debug=True)
        
        # 加载配置
        print("\n3. 加载配置")
        config = processor.load_config()
        print(f"配置加载成功: {config}")
        
        # 创建示例数据
        print("\n4. 创建示例数据")
        sample_data = create_sample_data()
        print(f"创建了 {len(sample_data)} 个示例数据项")
        
        # 处理数据批次
        print("\n5. 处理数据批次")
        results = processor.process_batch(sample_data, config)
        print(f"处理完成，得到 {len(results)} 个有效结果")
        
        # 保存结果
        print("\n6. 保存处理结果")
        processor.save_results(results, output_file)
        
        # 生成报告
        print("\n7. 生成处理报告")
        report = processor.generate_report(results)
        
        print("\n处理报告:")
        print("-" * 20)
        for key, value in report.items():
            print(f"{key}: {value}")
        
        # 显示部分结果
        if results:
            print("\n示例处理结果:")
            print("-" * 20)
            for i, result in enumerate(results[:3], 1):
                print(f"结果 {i}: {result}")
        
        print("\n程序执行完成")
        
    except (ConfigurationError, DataProcessingError) as e:
        print(f"处理错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"未预期的错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # 清理临时文件
        print("\n8. 清理临时文件")
        cleanup_files(config_file, output_file)


if __name__ == '__main__':
    main()