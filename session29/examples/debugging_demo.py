#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session29 Examples: 调试技术演示

本文件演示了各种Python调试技术：
- pdb调试器的使用
- 日志调试
- 断言调试
- 性能分析
- 内存分析
- 异常处理和错误追踪

作者: Python教程团队
"""

import pdb
import logging
import traceback
import sys
import time
import cProfile
import pstats
import io
import psutil
import os
from functools import wraps
from typing import List, Dict, Any
from memory_profiler import profile


# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


# 调试装饰器
def debug_function(func):
    """函数调试装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"调用函数 {func.__name__}")
        logger.debug(f"参数: args={args}, kwargs={kwargs}")
        
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            
            logger.debug(f"函数 {func.__name__} 执行成功")
            logger.debug(f"返回值: {result}")
            logger.debug(f"执行时间: {end_time - start_time:.4f}秒")
            
            return result
        except Exception as e:
            end_time = time.perf_counter()
            logger.error(f"函数 {func.__name__} 执行失败")
            logger.error(f"异常类型: {type(e).__name__}")
            logger.error(f"异常信息: {str(e)}")
            logger.error(f"执行时间: {end_time - start_time:.4f}秒")
            logger.error(f"异常追踪:\n{traceback.format_exc()}")
            raise
    
    return wrapper


def performance_monitor(func):
    """性能监控装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 获取进程信息
        process = psutil.Process(os.getpid())
        
        # 执行前的资源使用情况
        cpu_before = process.cpu_percent()
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        start_time = time.perf_counter()
        
        try:
            result = func(*args, **kwargs)
            
            end_time = time.perf_counter()
            
            # 执行后的资源使用情况
            cpu_after = process.cpu_percent()
            memory_after = process.memory_info().rss / 1024 / 1024  # MB
            
            execution_time = end_time - start_time
            memory_diff = memory_after - memory_before
            
            print(f"\n{'='*60}")
            print(f"性能监控报告: {func.__name__}")
            print(f"{'='*60}")
            print(f"执行时间: {execution_time:.4f} 秒")
            print(f"CPU使用率: {cpu_before:.1f}% -> {cpu_after:.1f}%")
            print(f"内存使用: {memory_before:.1f}MB -> {memory_after:.1f}MB (差值: {memory_diff:+.1f}MB)")
            print(f"{'='*60}")
            
            return result
            
        except Exception as e:
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            
            print(f"\n{'='*60}")
            print(f"性能监控报告: {func.__name__} (异常)")
            print(f"{'='*60}")
            print(f"执行时间: {execution_time:.4f} 秒")
            print(f"异常: {type(e).__name__}: {str(e)}")
            print(f"{'='*60}")
            
            raise
    
    return wrapper


class BuggyCalculator:
    """有bug的计算器类 - 用于演示调试技术"""
    
    def __init__(self):
        self.history = []
        self.debug_mode = False
    
    def set_debug_mode(self, enabled: bool):
        """设置调试模式"""
        self.debug_mode = enabled
        if enabled:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
    
    @debug_function
    def add_numbers(self, numbers: List[float]) -> float:
        """加法运算 - 包含潜在bug"""
        if self.debug_mode:
            pdb.set_trace()  # 设置断点
        
        if not numbers:
            logger.warning("输入列表为空")
            return 0
        
        total = 0
        for i, num in enumerate(numbers):
            logger.debug(f"处理第{i+1}个数字: {num}")
            
            # 故意引入bug：当数字为负数时处理不当
            if num < 0:
                logger.warning(f"发现负数: {num}")
                # Bug: 应该直接加上负数，但这里错误地取了绝对值
                total += abs(num)  # 这是一个bug！
            else:
                total += num
        
        self.history.append({
            'operation': 'add',
            'inputs': numbers,
            'result': total
        })
        
        return total
    
    @debug_function
    def divide_numbers(self, dividend: float, divisor: float) -> float:
        """除法运算 - 包含异常处理"""
        logger.debug(f"执行除法: {dividend} / {divisor}")
        
        # 检查除数
        if divisor == 0:
            logger.error("除数不能为零")
            raise ZeroDivisionError("除数不能为零")
        
        # 检查是否为数字
        if not isinstance(dividend, (int, float)) or not isinstance(divisor, (int, float)):
            logger.error(f"参数类型错误: dividend={type(dividend)}, divisor={type(divisor)}")
            raise TypeError("参数必须是数字类型")
        
        result = dividend / divisor
        
        self.history.append({
            'operation': 'divide',
            'inputs': [dividend, divisor],
            'result': result
        })
        
        return result
    
    @debug_function
    def factorial(self, n: int) -> int:
        """阶乘计算 - 递归函数调试"""
        logger.debug(f"计算阶乘: {n}!")
        
        # 参数验证
        if not isinstance(n, int):
            raise TypeError("参数必须是整数")
        
        if n < 0:
            raise ValueError("参数不能为负数")
        
        # 递归基础情况
        if n == 0 or n == 1:
            logger.debug(f"递归基础情况: {n}! = 1")
            return 1
        
        # 递归调用
        logger.debug(f"递归调用: {n}! = {n} * {n-1}!")
        result = n * self.factorial(n - 1)
        
        logger.debug(f"递归返回: {n}! = {result}")
        return result
    
    def get_history(self) -> List[Dict]:
        """获取计算历史"""
        return self.history.copy()
    
    def clear_history(self):
        """清空历史记录"""
        logger.info("清空计算历史")
        self.history.clear()


class MemoryLeakDemo:
    """内存泄漏演示类"""
    
    def __init__(self):
        self.data_storage = []
    
    @profile  # 内存分析装饰器
    def create_large_data(self, size: int = 1000000):
        """创建大量数据 - 可能导致内存问题"""
        logger.info(f"创建大小为 {size} 的数据")
        
        # 创建大量数据
        large_list = list(range(size))
        
        # 故意保存引用（可能导致内存泄漏）
        self.data_storage.append(large_list)
        
        logger.info(f"数据创建完成，当前存储了 {len(self.data_storage)} 个数据集")
        
        return large_list
    
    @profile
    def process_data(self, data: List[int]) -> Dict[str, Any]:
        """处理数据 - CPU密集型操作"""
        logger.info(f"处理 {len(data)} 个数据点")
        
        # CPU密集型计算
        squares = [x * x for x in data]
        cubes = [x * x * x for x in data]
        
        # 统计计算
        result = {
            'count': len(data),
            'sum': sum(data),
            'sum_squares': sum(squares),
            'sum_cubes': sum(cubes),
            'average': sum(data) / len(data) if data else 0,
            'max': max(data) if data else 0,
            'min': min(data) if data else 0
        }
        
        logger.info("数据处理完成")
        return result
    
    def clear_storage(self):
        """清空存储的数据"""
        logger.info("清空数据存储")
        self.data_storage.clear()


def demonstrate_pdb_debugging():
    """演示pdb调试器的使用"""
    print("\n" + "="*50)
    print("PDB调试器演示")
    print("="*50)
    
    print("PDB调试器是Python内置的交互式调试器")
    print("常用命令：")
    print("- l(ist): 显示当前代码")
    print("- n(ext): 执行下一行")
    print("- s(tep): 进入函数内部")
    print("- c(ontinue): 继续执行")
    print("- p <变量名>: 打印变量值")
    print("- pp <变量名>: 美化打印变量值")
    print("- w(here): 显示调用栈")
    print("- u(p): 向上移动栈帧")
    print("- d(own): 向下移动栈帧")
    print("- q(uit): 退出调试器")
    
    calc = BuggyCalculator()
    
    print("\n演示1: 正常计算")
    result1 = calc.add_numbers([1, 2, 3, 4, 5])
    print(f"结果: {result1}")
    
    print("\n演示2: 包含负数的计算（有bug）")
    result2 = calc.add_numbers([1, -2, 3, -4, 5])
    print(f"结果: {result2} (注意：这个结果是错误的！)")
    print("正确结果应该是: 1 + (-2) + 3 + (-4) + 5 = 3")
    print("但由于bug，负数被取了绝对值")
    
    print("\n要启用交互式调试，请：")
    print("1. 取消注释 BuggyCalculator.add_numbers 中的 pdb.set_trace()")
    print("2. 调用 calc.set_debug_mode(True)")
    print("3. 重新运行程序")


def demonstrate_logging_debugging():
    """演示日志调试"""
    print("\n" + "="*50)
    print("日志调试演示")
    print("="*50)
    
    calc = BuggyCalculator()
    calc.set_debug_mode(True)
    
    print("启用详细日志记录...")
    
    # 正常操作
    logger.info("开始日志调试演示")
    
    try:
        result1 = calc.divide_numbers(10, 2)
        logger.info(f"除法结果: {result1}")
        
        result2 = calc.factorial(5)
        logger.info(f"阶乘结果: {result2}")
        
        # 故意触发异常
        logger.info("尝试除零操作...")
        result3 = calc.divide_numbers(10, 0)
        
    except ZeroDivisionError as e:
        logger.error(f"捕获到除零异常: {e}")
        print("异常已被正确处理")
    
    print("\n日志文件 'debug.log' 包含了详细的执行信息")
    print("日志级别: DEBUG < INFO < WARNING < ERROR < CRITICAL")


def demonstrate_assertion_debugging():
    """演示断言调试"""
    print("\n" + "="*50)
    print("断言调试演示")
    print("="*50)
    
    def validate_input(value, min_val=0, max_val=100):
        """验证输入值"""
        # 使用断言进行调试
        assert isinstance(value, (int, float)), f"值必须是数字，实际类型: {type(value)}"
        assert min_val <= value <= max_val, f"值必须在 {min_val} 到 {max_val} 之间，实际值: {value}"
        
        logger.debug(f"输入验证通过: {value}")
        return True
    
    # 正常情况
    print("测试正常输入:")
    try:
        validate_input(50)
        print("✓ 输入 50 验证通过")
        
        validate_input(0)
        print("✓ 输入 0 验证通过")
        
        validate_input(100)
        print("✓ 输入 100 验证通过")
    except AssertionError as e:
        print(f"✗ 断言失败: {e}")
    
    # 异常情况
    print("\n测试异常输入:")
    test_cases = [
        ("abc", "字符串输入"),
        (-10, "负数输入"),
        (150, "超出范围输入")
    ]
    
    for test_value, description in test_cases:
        try:
            validate_input(test_value)
            print(f"✓ {description} 验证通过")
        except AssertionError as e:
            print(f"✗ {description} 断言失败: {e}")
    
    print("\n断言调试技巧:")
    print("1. 使用断言验证函数前置条件")
    print("2. 使用断言验证函数后置条件")
    print("3. 使用断言验证不变量")
    print("4. 在生产环境中可以通过 python -O 禁用断言")


@performance_monitor
def demonstrate_performance_profiling():
    """演示性能分析"""
    print("\n" + "="*50)
    print("性能分析演示")
    print("="*50)
    
    # 创建性能分析器
    pr = cProfile.Profile()
    pr.enable()
    
    # 执行一些计算密集型操作
    memory_demo = MemoryLeakDemo()
    
    # 创建和处理数据
    data1 = memory_demo.create_large_data(100000)
    result1 = memory_demo.process_data(data1[:10000])
    
    data2 = memory_demo.create_large_data(50000)
    result2 = memory_demo.process_data(data2[:5000])
    
    # 停止性能分析
    pr.disable()
    
    # 生成性能报告
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s)
    ps.sort_stats('cumulative')
    ps.print_stats(15)  # 显示前15个最耗时的函数
    
    print("\n性能分析报告:")
    print(s.getvalue())
    
    print(f"\n处理结果1: 数据量={result1['count']}, 平均值={result1['average']:.2f}")
    print(f"处理结果2: 数据量={result2['count']}, 平均值={result2['average']:.2f}")
    
    # 清理内存
    memory_demo.clear_storage()
    
    return result1, result2


def demonstrate_exception_handling():
    """演示异常处理和错误追踪"""
    print("\n" + "="*50)
    print("异常处理和错误追踪演示")
    print("="*50)
    
    def risky_function(x, y):
        """可能出错的函数"""
        logger.debug(f"执行风险函数: x={x}, y={y}")
        
        if x == 0:
            raise ValueError("x不能为0")
        
        if y < 0:
            raise ValueError("y不能为负数")
        
        result = (x + y) / (x - 1)
        
        if result > 100:
            raise OverflowError("结果过大")
        
        return result
    
    def nested_function_call(a, b, c):
        """嵌套函数调用"""
        logger.debug(f"嵌套函数调用: a={a}, b={b}, c={c}")
        
        try:
            result1 = risky_function(a, b)
            result2 = risky_function(b, c)
            return result1 + result2
        except Exception as e:
            logger.error(f"嵌套函数中发生异常: {type(e).__name__}: {e}")
            raise  # 重新抛出异常
    
    # 测试不同的异常情况
    test_cases = [
        (2, 3, 4, "正常情况"),
        (0, 1, 2, "x为0的情况"),
        (2, -1, 3, "y为负数的情况"),
        (1, 1, 2, "x-1为0的情况"),
        (50, 60, 70, "结果过大的情况")
    ]
    
    for a, b, c, description in test_cases:
        print(f"\n测试 {description}: nested_function_call({a}, {b}, {c})")
        
        try:
            result = nested_function_call(a, b, c)
            print(f"✓ 成功: {result}")
            
        except Exception as e:
            print(f"✗ 异常: {type(e).__name__}: {e}")
            
            # 打印详细的异常追踪
            print("详细异常追踪:")
            traceback.print_exc()
            
            # 获取异常追踪信息
            exc_type, exc_value, exc_traceback = sys.exc_info()
            
            print("\n异常分析:")
            print(f"异常类型: {exc_type.__name__}")
            print(f"异常值: {exc_value}")
            print(f"异常文件: {exc_traceback.tb_frame.f_code.co_filename}")
            print(f"异常行号: {exc_traceback.tb_lineno}")
            
            # 打印调用栈
            print("\n调用栈:")
            for frame_info in traceback.extract_tb(exc_traceback):
                print(f"  文件: {frame_info.filename}")
                print(f"  行号: {frame_info.lineno}")
                print(f"  函数: {frame_info.name}")
                print(f"  代码: {frame_info.line}")
                print()


def demonstrate_memory_debugging():
    """演示内存调试"""
    print("\n" + "="*50)
    print("内存调试演示")
    print("="*50)
    
    print("注意: 需要安装 memory_profiler 和 psutil")
    print("pip install memory_profiler psutil")
    
    try:
        memory_demo = MemoryLeakDemo()
        
        print("\n创建大量数据并监控内存使用...")
        
        # 监控内存使用
        process = psutil.Process(os.getpid())
        
        print(f"初始内存使用: {process.memory_info().rss / 1024 / 1024:.1f} MB")
        
        # 创建多个大数据集
        for i in range(3):
            data = memory_demo.create_large_data(100000)
            current_memory = process.memory_info().rss / 1024 / 1024
            print(f"创建数据集 {i+1} 后内存使用: {current_memory:.1f} MB")
        
        print(f"\n总共存储了 {len(memory_demo.data_storage)} 个数据集")
        
        # 清理内存
        print("\n清理内存...")
        memory_demo.clear_storage()
        
        # 强制垃圾回收
        import gc
        gc.collect()
        
        final_memory = process.memory_info().rss / 1024 / 1024
        print(f"清理后内存使用: {final_memory:.1f} MB")
        
    except ImportError as e:
        print(f"导入错误: {e}")
        print("请安装所需的包: pip install memory_profiler psutil")


def main():
    """主函数：调试技术演示"""
    print("Session29: 调试技术演示")
    print("=" * 50)
    
    try:
        # 1. PDB调试演示
        demonstrate_pdb_debugging()
        
        # 2. 日志调试演示
        demonstrate_logging_debugging()
        
        # 3. 断言调试演示
        demonstrate_assertion_debugging()
        
        # 4. 性能分析演示
        demonstrate_performance_profiling()
        
        # 5. 异常处理演示
        demonstrate_exception_handling()
        
        # 6. 内存调试演示
        demonstrate_memory_debugging()
        
        print("\n" + "="*50)
        print("调试技术演示完成！")
        print("="*50)
        
        print("\n调试技术总结:")
        print("1. PDB: 交互式调试器，适合复杂逻辑调试")
        print("2. 日志: 记录程序执行状态，适合生产环境")
        print("3. 断言: 验证程序状态，适合开发阶段")
        print("4. 性能分析: 找出性能瓶颈")
        print("5. 异常处理: 优雅处理错误情况")
        print("6. 内存分析: 检测内存泄漏和优化内存使用")
        
        print("\n调试最佳实践:")
        print("- 使用适当的日志级别")
        print("- 编写有意义的错误消息")
        print("- 保留异常的上下文信息")
        print("- 定期进行性能分析")
        print("- 使用断言验证假设")
        print("- 监控内存使用情况")
        
    except Exception as e:
        logger.error(f"演示过程中发生错误: {e}")
        print(f"\n错误: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()