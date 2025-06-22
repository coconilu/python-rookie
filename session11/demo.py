#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session11: 错误处理与调试 - 演示代码

本文件演示了Python异常处理的基本用法和实际应用，包括：
1. 基础异常处理
2. 自定义异常
3. 调试技巧
4. 日志记录
5. 健壮的代码设计

作者: Python教程团队
创建日期: 2024-01-15
最后修改: 2024-01-15
"""

import logging
import sys
import traceback
from typing import List, Dict, Any, Optional


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


# 自定义异常类
class CalculatorError(Exception):
    """计算器异常基类"""
    pass


class DivisionByZeroError(CalculatorError):
    """除零错误"""
    def __init__(self, message="不能除以零"):
        super().__init__(message)
        self.message = message


class InvalidOperatorError(CalculatorError):
    """无效操作符错误"""
    def __init__(self, operator):
        self.operator = operator
        super().__init__(f"无效的操作符: {operator}")


class Calculator:
    """演示异常处理的计算器类"""
    
    def __init__(self):
        self.history = []
        logger.info("计算器初始化完成")
    
    def add(self, a: float, b: float) -> float:
        """加法运算"""
        try:
            result = float(a) + float(b)
            self._record_operation("add", a, b, result)
            return result
        except (TypeError, ValueError) as e:
            logger.error(f"加法运算参数错误: {e}")
            raise ValueError(f"无效的数字参数: {a}, {b}")
    
    def subtract(self, a: float, b: float) -> float:
        """减法运算"""
        try:
            result = float(a) - float(b)
            self._record_operation("subtract", a, b, result)
            return result
        except (TypeError, ValueError) as e:
            logger.error(f"减法运算参数错误: {e}")
            raise ValueError(f"无效的数字参数: {a}, {b}")
    
    def multiply(self, a: float, b: float) -> float:
        """乘法运算"""
        try:
            result = float(a) * float(b)
            self._record_operation("multiply", a, b, result)
            return result
        except (TypeError, ValueError) as e:
            logger.error(f"乘法运算参数错误: {e}")
            raise ValueError(f"无效的数字参数: {a}, {b}")
    
    def divide(self, a: float, b: float) -> float:
        """除法运算"""
        try:
            if float(b) == 0:
                raise DivisionByZeroError()
            
            result = float(a) / float(b)
            self._record_operation("divide", a, b, result)
            return result
        except DivisionByZeroError:
            logger.error("尝试除以零")
            raise
        except (TypeError, ValueError) as e:
            logger.error(f"除法运算参数错误: {e}")
            raise ValueError(f"无效的数字参数: {a}, {b}")
    
    def calculate(self, expression: str) -> float:
        """计算表达式"""
        try:
            # 简单的表达式解析
            expression = expression.replace(" ", "")
            
            for op in ["+", "-", "*", "/"]:
                if op in expression:
                    parts = expression.split(op)
                    if len(parts) != 2:
                        raise ValueError("表达式格式错误")
                    
                    a, b = parts[0], parts[1]
                    
                    if op == "+":
                        return self.add(a, b)
                    elif op == "-":
                        return self.subtract(a, b)
                    elif op == "*":
                        return self.multiply(a, b)
                    elif op == "/":
                        return self.divide(a, b)
            
            raise InvalidOperatorError("未找到有效操作符")
        
        except Exception as e:
            logger.error(f"计算表达式失败: {expression} - {e}")
            raise
    
    def _record_operation(self, operation: str, a: float, b: float, result: float):
        """记录操作历史"""
        record = {
            "operation": operation,
            "operand1": a,
            "operand2": b,
            "result": result
        }
        self.history.append(record)
        logger.debug(f"记录操作: {record}")
    
    def get_history(self) -> List[Dict[str, Any]]:
        """获取操作历史"""
        return self.history.copy()
    
    def clear_history(self):
        """清空操作历史"""
        self.history.clear()
        logger.info("操作历史已清空")


def demo_basic_exception_handling():
    """演示基础异常处理"""
    print("\n=== 基础异常处理演示 ===")
    
    # 1. 处理除零错误
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        print(f"捕获到除零错误: {e}")
    
    # 2. 处理类型错误
    try:
        result = "hello" + 5
    except TypeError as e:
        print(f"捕获到类型错误: {e}")
    
    # 3. 处理索引错误
    try:
        my_list = [1, 2, 3]
        value = my_list[10]
    except IndexError as e:
        print(f"捕获到索引错误: {e}")
    
    # 4. 处理多种异常
    def risky_operation(data, index):
        try:
            return 100 / data[index]
        except (IndexError, KeyError):
            return "索引或键错误"
        except ZeroDivisionError:
            return "除零错误"
        except Exception as e:
            return f"其他错误: {e}"
    
    print(f"risky_operation([1, 2, 0], 2): {risky_operation([1, 2, 0], 2)}")
    print(f"risky_operation([1, 2, 3], 5): {risky_operation([1, 2, 3], 5)}")
    print(f"risky_operation([1, 2, 3], 1): {risky_operation([1, 2, 3], 1)}")


def demo_custom_exceptions():
    """演示自定义异常"""
    print("\n=== 自定义异常演示 ===")
    
    calc = Calculator()
    
    # 测试正常操作
    try:
        result = calc.add(10, 5)
        print(f"10 + 5 = {result}")
    except Exception as e:
        print(f"加法错误: {e}")
    
    # 测试除零错误
    try:
        result = calc.divide(10, 0)
    except DivisionByZeroError as e:
        print(f"自定义除零错误: {e}")
    
    # 测试无效操作符
    try:
        result = calc.calculate("10 % 3")
    except InvalidOperatorError as e:
        print(f"无效操作符错误: {e}")
    
    # 测试参数错误
    try:
        result = calc.multiply("abc", 5)
    except ValueError as e:
        print(f"参数错误: {e}")


def demo_finally_and_else():
    """演示finally和else子句"""
    print("\n=== finally和else子句演示 ===")
    
    def file_operation_demo(filename: str):
        file_handle = None
        try:
            print(f"尝试打开文件: {filename}")
            file_handle = open(filename, 'r')
            content = file_handle.read()
            print(f"文件内容长度: {len(content)}")
        except FileNotFoundError:
            print(f"文件 {filename} 不存在")
        except PermissionError:
            print(f"没有权限访问文件 {filename}")
        else:
            print("文件读取成功")
        finally:
            if file_handle:
                file_handle.close()
                print("文件已关闭")
            else:
                print("没有文件需要关闭")
    
    # 测试不存在的文件
    file_operation_demo("nonexistent.txt")
    
    # 测试存在的文件（如果有的话）
    try:
        # 创建一个临时文件进行测试
        with open("temp_test.txt", "w") as f:
            f.write("这是测试内容")
        
        file_operation_demo("temp_test.txt")
        
        # 清理临时文件
        import os
        os.remove("temp_test.txt")
    except Exception as e:
        print(f"临时文件操作失败: {e}")


def demo_exception_chaining():
    """演示异常链"""
    print("\n=== 异常链演示 ===")
    
    def low_level_function():
        """底层函数"""
        raise ValueError("底层错误")
    
    def mid_level_function():
        """中层函数"""
        try:
            low_level_function()
        except ValueError as e:
            raise RuntimeError("中层处理失败") from e
    
    def high_level_function():
        """高层函数"""
        try:
            mid_level_function()
        except RuntimeError as e:
            print(f"高层捕获到错误: {e}")
            print(f"原始错误: {e.__cause__}")
            print("\n完整的异常链:")
            traceback.print_exc()
    
    high_level_function()


def demo_context_manager():
    """演示上下文管理器"""
    print("\n=== 上下文管理器演示 ===")
    
    from contextlib import contextmanager
    
    @contextmanager
    def managed_resource(name):
        """自定义上下文管理器"""
        print(f"获取资源: {name}")
        try:
            yield f"资源_{name}"
        except Exception as e:
            print(f"处理异常: {e}")
            raise
        finally:
            print(f"释放资源: {name}")
    
    # 正常使用
    try:
        with managed_resource("数据库连接") as resource:
            print(f"使用资源: {resource}")
            # 模拟一些操作
            result = "操作成功"
            print(f"操作结果: {result}")
    except Exception as e:
        print(f"操作失败: {e}")
    
    print()
    
    # 异常情况
    try:
        with managed_resource("文件句柄") as resource:
            print(f"使用资源: {resource}")
            # 模拟异常
            raise ValueError("模拟的错误")
    except Exception as e:
        print(f"捕获到异常: {e}")


def demo_logging_with_exceptions():
    """演示异常处理中的日志记录"""
    print("\n=== 异常处理中的日志记录演示 ===")
    
    def process_data_with_logging(data: List[Any]) -> Dict[str, Any]:
        """带日志记录的数据处理函数"""
        logger.info(f"开始处理数据，共 {len(data)} 个元素")
        
        results = []
        errors = []
        
        for i, item in enumerate(data):
            try:
                logger.debug(f"处理第 {i} 个元素: {item}")
                
                # 模拟数据处理
                if not isinstance(item, (int, float)):
                    raise TypeError(f"元素必须是数字，得到: {type(item)}")
                
                if item < 0:
                    logger.warning(f"发现负数: {item}")
                
                result = item ** 2
                results.append(result)
                logger.debug(f"处理结果: {item} -> {result}")
                
            except Exception as e:
                error_info = {
                    'index': i,
                    'item': item,
                    'error': str(e),
                    'type': type(e).__name__
                }
                errors.append(error_info)
                logger.error(f"处理第 {i} 个元素时出错: {e}", exc_info=True)
        
        success_count = len(results)
        total_count = len(data)
        success_rate = success_count / total_count if total_count > 0 else 0
        
        logger.info(f"数据处理完成: 成功 {success_count}/{total_count} ({success_rate:.1%})")
        
        return {
            'results': results,
            'errors': errors,
            'success_count': success_count,
            'total_count': total_count,
            'success_rate': success_rate
        }
    
    # 测试数据处理
    test_data = [1, 2, "abc", 4, -5, 6.5, None, 8]
    result = process_data_with_logging(test_data)
    
    print(f"处理结果: {result['results']}")
    print(f"错误数量: {len(result['errors'])}")
    print(f"成功率: {result['success_rate']:.1%}")


def interactive_calculator_demo():
    """交互式计算器演示"""
    print("\n=== 交互式计算器演示 ===")
    print("输入数学表达式（如: 10+5, 20/4），输入 'quit' 退出")
    
    calc = Calculator()
    
    while True:
        try:
            expression = input("请输入表达式: ").strip()
            
            if expression.lower() in ['quit', 'exit', 'q']:
                print("退出计算器")
                break
            
            if expression.lower() == 'history':
                history = calc.get_history()
                if history:
                    print("\n操作历史:")
                    for i, record in enumerate(history, 1):
                        print(f"{i}. {record['operand1']} {record['operation']} {record['operand2']} = {record['result']}")
                else:
                    print("暂无操作历史")
                continue
            
            if expression.lower() == 'clear':
                calc.clear_history()
                print("历史记录已清空")
                continue
            
            if not expression:
                print("请输入有效的表达式")
                continue
            
            result = calc.calculate(expression)
            print(f"结果: {result}")
            
        except KeyboardInterrupt:
            print("\n用户中断操作")
            break
        except (DivisionByZeroError, InvalidOperatorError) as e:
            print(f"计算错误: {e}")
        except ValueError as e:
            print(f"输入错误: {e}")
        except Exception as e:
            print(f"未知错误: {e}")
            logger.error(f"计算器发生未知错误: {e}", exc_info=True)


def main():
    """主函数：演示程序的入口点"""
    print("Session11: 错误处理与调试演示")
    print("=" * 50)
    
    try:
        # 演示各种异常处理技术
        demo_basic_exception_handling()
        demo_custom_exceptions()
        demo_finally_and_else()
        demo_exception_chaining()
        demo_context_manager()
        demo_logging_with_exceptions()
        
        # 交互式演示（可选）
        print("\n是否要运行交互式计算器演示？(y/n): ", end="")
        choice = input().strip().lower()
        if choice in ['y', 'yes']:
            interactive_calculator_demo()
        
        print("\n演示完成！")
        
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        logger.error(f"程序执行过程中发生错误: {e}", exc_info=True)
        print(f"程序错误: {e}")
    finally:
        print("程序结束")


if __name__ == "__main__":
    main()