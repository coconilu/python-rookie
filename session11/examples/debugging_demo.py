#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session11 示例3: 调试技巧演示

本文件演示了Python中常用的调试技巧和工具，包括：
1. print调试
2. 断言调试
3. pdb调试器
4. 日志调试
5. 性能调试

作者: Python教程团队
创建日期: 2024-01-15
"""

import sys
import time
import traceback
import logging
from typing import List, Dict, Any


# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
)
logger = logging.getLogger(__name__)


class DebugHelper:
    """调试辅助类"""
    
    def __init__(self, debug_mode=True):
        self.debug_mode = debug_mode
        self.call_count = {}
        self.execution_times = {}
    
    def debug_print(self, message, *args, **kwargs):
        """条件调试打印"""
        if self.debug_mode:
            if args or kwargs:
                print(f"DEBUG: {message}", *args, **kwargs)
            else:
                print(f"DEBUG: {message}")
    
    def trace_function_call(self, func_name, args=None, kwargs=None):
        """跟踪函数调用"""
        if self.debug_mode:
            self.call_count[func_name] = self.call_count.get(func_name, 0) + 1
            print(f"TRACE: 调用函数 {func_name} (第{self.call_count[func_name]}次)")
            if args:
                print(f"TRACE: 参数: {args}")
            if kwargs:
                print(f"TRACE: 关键字参数: {kwargs}")
    
    def measure_execution_time(self, func_name):
        """测量执行时间的装饰器"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    end_time = time.time()
                    execution_time = end_time - start_time
                    self.execution_times[func_name] = execution_time
                    if self.debug_mode:
                        print(f"PERF: {func_name} 执行时间: {execution_time:.4f}秒")
            return wrapper
        return decorator
    
    def get_statistics(self):
        """获取调试统计信息"""
        return {
            'call_count': self.call_count.copy(),
            'execution_times': self.execution_times.copy()
        }


# 全局调试助手
debug_helper = DebugHelper()


def demo_print_debugging():
    """演示print调试技巧"""
    print("=== Print调试技巧演示 ===")
    
    def buggy_function(data):
        """包含bug的函数"""
        print(f"DEBUG: 输入数据类型: {type(data)}, 长度: {len(data) if hasattr(data, '__len__') else 'N/A'}")
        print(f"DEBUG: 输入数据内容: {data}")
        
        result = []
        for i, item in enumerate(data):
            print(f"DEBUG: 处理第{i}个元素: {item} (类型: {type(item)})")
            
            try:
                # 尝试将元素转换为整数并乘以2
                if isinstance(item, str):
                    converted = int(item)
                    print(f"DEBUG: 字符串 '{item}' 转换为整数: {converted}")
                else:
                    converted = item
                    print(f"DEBUG: 元素已是数字: {converted}")
                
                processed = converted * 2
                print(f"DEBUG: 处理结果: {converted} * 2 = {processed}")
                result.append(processed)
                
            except ValueError as e:
                print(f"DEBUG: 转换失败: {e}")
                print(f"DEBUG: 跳过元素: {item}")
                continue
            except Exception as e:
                print(f"DEBUG: 未知错误: {e}")
                print(f"DEBUG: 跳过元素: {item}")
                continue
        
        print(f"DEBUG: 最终结果: {result}")
        return result
    
    # 测试数据
    test_cases = [
        [1, 2, 3, 4],
        ["1", "2", "3"],
        [1, "2", "abc", 4, "5"],
        []
    ]
    
    for i, test_data in enumerate(test_cases, 1):
        print(f"\n--- 测试用例 {i} ---")
        result = buggy_function(test_data)
        print(f"测试结果: {result}\n")


def demo_assertion_debugging():
    """演示断言调试"""
    print("=== 断言调试演示 ===")
    
    def calculate_average(numbers):
        """计算平均值（带断言）"""
        # 前置条件断言
        assert isinstance(numbers, (list, tuple)), f"输入必须是列表或元组，得到: {type(numbers)}"
        assert len(numbers) > 0, "列表不能为空"
        assert all(isinstance(n, (int, float)) for n in numbers), "所有元素必须是数字"
        
        print(f"DEBUG: 计算 {len(numbers)} 个数字的平均值")
        print(f"DEBUG: 数字列表: {numbers}")
        
        total = sum(numbers)
        count = len(numbers)
        average = total / count
        
        print(f"DEBUG: 总和: {total}, 数量: {count}, 平均值: {average}")
        
        # 后置条件断言
        assert isinstance(average, (int, float)), "平均值必须是数字"
        assert min(numbers) <= average <= max(numbers), "平均值应该在最小值和最大值之间"
        
        return average
    
    def safe_divide(a, b):
        """安全除法（带断言）"""
        assert isinstance(a, (int, float)), f"被除数必须是数字，得到: {type(a)}"
        assert isinstance(b, (int, float)), f"除数必须是数字，得到: {type(b)}"
        assert b != 0, "除数不能为零"
        
        result = a / b
        
        # 结果验证
        assert isinstance(result, (int, float)), "结果必须是数字"
        assert result * b == a or abs(result * b - a) < 1e-10, "结果验证失败"
        
        return result
    
    # 测试断言
    test_cases = [
        # 正常情况
        ([1, 2, 3, 4, 5], "正常数字列表"),
        ([10], "单个数字"),
        ([1.5, 2.5, 3.5], "浮点数列表"),
        
        # 异常情况
        ([], "空列表"),
        ([1, 2, "3"], "包含字符串"),
        ("not a list", "不是列表"),
    ]
    
    for test_data, description in test_cases:
        print(f"\n--- 测试: {description} ---")
        try:
            result = calculate_average(test_data)
            print(f"✓ 平均值: {result}")
        except AssertionError as e:
            print(f"✗ 断言失败: {e}")
        except Exception as e:
            print(f"✗ 其他错误: {e}")
    
    # 测试除法断言
    print("\n--- 除法断言测试 ---")
    division_tests = [
        (10, 2, "正常除法"),
        (10, 0, "除零错误"),
        ("10", 2, "被除数类型错误"),
        (10, "2", "除数类型错误"),
    ]
    
    for a, b, description in division_tests:
        print(f"\n测试: {description}")
        try:
            result = safe_divide(a, b)
            print(f"✓ 结果: {a} / {b} = {result}")
        except AssertionError as e:
            print(f"✗ 断言失败: {e}")
        except Exception as e:
            print(f"✗ 其他错误: {e}")


def demo_pdb_debugging():
    """演示pdb调试器使用"""
    print("=== PDB调试器演示 ===")
    
    def complex_calculation(x, y, z):
        """复杂计算函数（用于pdb演示）"""
        print(f"开始计算: x={x}, y={y}, z={z}")
        
        # 在这里可以设置断点：import pdb; pdb.set_trace()
        # 由于这是演示，我们不实际启动pdb，而是模拟调试过程
        
        step1 = x * 2
        print(f"步骤1: x * 2 = {step1}")
        
        step2 = y + 10
        print(f"步骤2: y + 10 = {step2}")
        
        step3 = step1 + step2
        print(f"步骤3: step1 + step2 = {step3}")
        
        if step3 > z:
            result = step3 / z
            print(f"步骤4a: step3 / z = {result}")
        else:
            result = step3 * z
            print(f"步骤4b: step3 * z = {result}")
        
        final_result = result ** 0.5
        print(f"最终结果: sqrt({result}) = {final_result}")
        
        return final_result
    
    print("PDB调试器常用命令:")
    print("  n (next)     - 执行下一行")
    print("  s (step)     - 进入函数内部")
    print("  c (continue) - 继续执行")
    print("  l (list)     - 显示当前代码")
    print("  p <var>      - 打印变量值")
    print("  pp <var>     - 美化打印变量")
    print("  w (where)    - 显示调用栈")
    print("  u (up)       - 上移一层调用栈")
    print("  d (down)     - 下移一层调用栈")
    print("  q (quit)     - 退出调试器")
    
    print("\n模拟调试过程:")
    result = complex_calculation(5, 3, 20)
    print(f"计算完成，结果: {result}")
    
    print("\n要启用实际的pdb调试，请在代码中添加:")
    print("  import pdb; pdb.set_trace()")
    print("或者使用命令行: python -m pdb script.py")


def demo_logging_debugging():
    """演示日志调试"""
    print("=== 日志调试演示 ===")
    
    # 创建专门的调试日志记录器
    debug_logger = logging.getLogger('debug_demo')
    debug_logger.setLevel(logging.DEBUG)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    # 添加处理器到日志记录器
    debug_logger.addHandler(console_handler)
    
    def process_user_data(users_data):
        """处理用户数据（带日志调试）"""
        debug_logger.info(f"开始处理用户数据，共 {len(users_data)} 条记录")
        
        processed_users = []
        errors = []
        
        for i, user_data in enumerate(users_data):
            debug_logger.debug(f"处理第 {i+1} 条用户数据: {user_data}")
            
            try:
                # 验证必填字段
                if 'name' not in user_data:
                    raise ValueError("缺少用户名")
                if 'age' not in user_data:
                    raise ValueError("缺少年龄")
                
                name = user_data['name']
                age = user_data['age']
                
                debug_logger.debug(f"用户信息: 姓名={name}, 年龄={age}")
                
                # 验证数据类型
                if not isinstance(name, str) or not name.strip():
                    raise ValueError(f"无效的用户名: {name}")
                
                if not isinstance(age, int) or age < 0 or age > 150:
                    raise ValueError(f"无效的年龄: {age}")
                
                # 处理数据
                processed_user = {
                    'id': i + 1,
                    'name': name.strip().title(),
                    'age': age,
                    'category': 'adult' if age >= 18 else 'minor'
                }
                
                debug_logger.debug(f"处理后的用户数据: {processed_user}")
                processed_users.append(processed_user)
                
                debug_logger.info(f"成功处理用户: {name}")
                
            except Exception as e:
                error_info = {
                    'index': i,
                    'data': user_data,
                    'error': str(e)
                }
                errors.append(error_info)
                debug_logger.error(f"处理用户数据失败: {e}", exc_info=True)
        
        debug_logger.info(f"数据处理完成: 成功 {len(processed_users)} 条，失败 {len(errors)} 条")
        
        if errors:
            debug_logger.warning(f"处理过程中发生 {len(errors)} 个错误")
            for error in errors:
                debug_logger.warning(f"错误详情: 索引 {error['index']}, 数据 {error['data']}, 错误 {error['error']}")
        
        return {
            'processed': processed_users,
            'errors': errors,
            'success_rate': len(processed_users) / len(users_data) if users_data else 0
        }
    
    # 测试数据
    test_users = [
        {'name': 'Alice', 'age': 25},
        {'name': 'Bob', 'age': 17},
        {'name': '', 'age': 30},  # 无效姓名
        {'name': 'Charlie', 'age': -5},  # 无效年龄
        {'name': 'David'},  # 缺少年龄
        {'age': 40},  # 缺少姓名
        {'name': 'Eve', 'age': 35},
    ]
    
    result = process_user_data(test_users)
    
    print(f"\n处理结果:")
    print(f"成功处理: {len(result['processed'])} 条")
    print(f"处理失败: {len(result['errors'])} 条")
    print(f"成功率: {result['success_rate']:.1%}")


def demo_performance_debugging():
    """演示性能调试"""
    print("=== 性能调试演示 ===")
    
    import time
    import functools
    
    def timing_decorator(func):
        """计时装饰器"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"函数 {func.__name__} 执行时间: {execution_time:.4f}秒")
            return result
        return wrapper
    
    def profile_decorator(func):
        """性能分析装饰器"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import cProfile
            import pstats
            import io
            
            pr = cProfile.Profile()
            pr.enable()
            
            result = func(*args, **kwargs)
            
            pr.disable()
            s = io.StringIO()
            ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
            ps.print_stats(10)  # 显示前10个最耗时的函数
            
            print(f"\n函数 {func.__name__} 的性能分析:")
            print(s.getvalue())
            
            return result
        return wrapper
    
    @timing_decorator
    def slow_function_v1(n):
        """低效的函数实现"""
        result = []
        for i in range(n):
            # 模拟低效操作
            temp = []
            for j in range(i):
                temp.append(j ** 2)
            result.append(sum(temp))
        return result
    
    @timing_decorator
    def optimized_function_v2(n):
        """优化后的函数实现"""
        result = []
        for i in range(n):
            # 使用数学公式优化
            if i == 0:
                result.append(0)
            else:
                # 平方和公式: 1² + 2² + ... + (i-1)² = (i-1)*i*(2i-1)/6
                sum_of_squares = (i - 1) * i * (2 * i - 1) // 6
                result.append(sum_of_squares)
        return result
    
    @profile_decorator
    def memory_intensive_function(size):
        """内存密集型函数"""
        # 创建大量数据
        data = list(range(size))
        
        # 进行一些计算
        squared = [x ** 2 for x in data]
        filtered = [x for x in squared if x % 2 == 0]
        
        return len(filtered)
    
    # 性能比较
    print("\n性能比较测试:")
    test_size = 1000
    
    print(f"\n测试数据大小: {test_size}")
    
    print("\n1. 低效实现:")
    result1 = slow_function_v1(test_size)
    
    print("\n2. 优化实现:")
    result2 = optimized_function_v2(test_size)
    
    # 验证结果一致性
    if result1 == result2:
        print("✓ 两种实现结果一致")
    else:
        print("✗ 两种实现结果不一致")
    
    print("\n3. 内存使用分析:")
    memory_result = memory_intensive_function(10000)
    print(f"内存密集型函数结果: {memory_result}")
    
    # 内存使用监控
    print("\n4. 内存使用监控:")
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    print(f"当前进程内存使用: {memory_info.rss / 1024 / 1024:.2f} MB")
    print(f"虚拟内存使用: {memory_info.vms / 1024 / 1024:.2f} MB")


def demo_error_tracking():
    """演示错误跟踪和分析"""
    print("=== 错误跟踪和分析演示 ===")
    
    class ErrorTracker:
        """错误跟踪器"""
        
        def __init__(self):
            self.errors = []
            self.error_counts = {}
        
        def track_error(self, error, context=None):
            """跟踪错误"""
            error_info = {
                'timestamp': time.time(),
                'error_type': type(error).__name__,
                'error_message': str(error),
                'context': context,
                'traceback': traceback.format_exc()
            }
            
            self.errors.append(error_info)
            
            # 统计错误类型
            error_type = error_info['error_type']
            self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
            
            logger.error(f"错误跟踪: {error_type} - {error_info['error_message']}")
        
        def get_error_summary(self):
            """获取错误摘要"""
            return {
                'total_errors': len(self.errors),
                'error_types': self.error_counts.copy(),
                'recent_errors': self.errors[-5:] if self.errors else []
            }
        
        def analyze_errors(self):
            """分析错误模式"""
            if not self.errors:
                return "没有错误记录"
            
            analysis = []
            analysis.append(f"总错误数: {len(self.errors)}")
            analysis.append(f"错误类型分布: {self.error_counts}")
            
            # 找出最常见的错误
            if self.error_counts:
                most_common = max(self.error_counts.items(), key=lambda x: x[1])
                analysis.append(f"最常见错误: {most_common[0]} ({most_common[1]}次)")
            
            # 时间分析
            if len(self.errors) > 1:
                first_error_time = self.errors[0]['timestamp']
                last_error_time = self.errors[-1]['timestamp']
                time_span = last_error_time - first_error_time
                error_rate = len(self.errors) / max(time_span, 1)
                analysis.append(f"错误频率: {error_rate:.2f} 错误/秒")
            
            return "\n".join(analysis)
    
    # 创建错误跟踪器
    error_tracker = ErrorTracker()
    
    def risky_operations():
        """执行一些可能出错的操作"""
        operations = [
            lambda: 10 / 0,  # 除零错误
            lambda: int("abc"),  # 值错误
            lambda: [1, 2, 3][10],  # 索引错误
            lambda: {"a": 1}["b"],  # 键错误
            lambda: "hello".nonexistent_method(),  # 属性错误
        ]
        
        for i, operation in enumerate(operations):
            try:
                result = operation()
                print(f"操作 {i+1} 成功: {result}")
            except Exception as e:
                context = {
                    'operation_index': i + 1,
                    'operation_name': f"operation_{i+1}"
                }
                error_tracker.track_error(e, context)
                print(f"操作 {i+1} 失败: {type(e).__name__}")
    
    # 执行风险操作
    print("执行风险操作...")
    risky_operations()
    
    # 分析错误
    print("\n错误分析结果:")
    summary = error_tracker.get_error_summary()
    print(f"错误摘要: {summary}")
    
    print("\n详细分析:")
    analysis = error_tracker.analyze_errors()
    print(analysis)


def main():
    """主函数"""
    print("Session11 示例3: 调试技巧演示")
    print("=" * 50)
    
    try:
        demo_print_debugging()
        print("\n" + "="*50)
        
        demo_assertion_debugging()
        print("\n" + "="*50)
        
        demo_pdb_debugging()
        print("\n" + "="*50)
        
        demo_logging_debugging()
        print("\n" + "="*50)
        
        demo_performance_debugging()
        print("\n" + "="*50)
        
        demo_error_tracking()
        
    except Exception as e:
        logger.error(f"演示过程中发生错误: {e}", exc_info=True)
        print(f"演示错误: {e}")
    
    print("\n示例演示完成！")


if __name__ == "__main__":
    main()