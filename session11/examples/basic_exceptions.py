#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session11 示例1: 基础异常处理

本文件演示了Python中最常见的异常类型和基本的处理方法。

作者: Python教程团队
创建日期: 2024-01-15
"""


def demo_common_exceptions():
    """演示常见异常类型"""
    print("=== 常见异常类型演示 ===")
    
    # 1. ZeroDivisionError - 除零错误
    print("\n1. ZeroDivisionError 演示:")
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        print(f"除零错误: {e}")
        print(f"异常类型: {type(e).__name__}")
    
    # 2. ValueError - 值错误
    print("\n2. ValueError 演示:")
    try:
        number = int("abc")
    except ValueError as e:
        print(f"值错误: {e}")
        print(f"异常类型: {type(e).__name__}")
    
    # 3. TypeError - 类型错误
    print("\n3. TypeError 演示:")
    try:
        result = "hello" + 5
    except TypeError as e:
        print(f"类型错误: {e}")
        print(f"异常类型: {type(e).__name__}")
    
    # 4. IndexError - 索引错误
    print("\n4. IndexError 演示:")
    try:
        my_list = [1, 2, 3]
        value = my_list[10]
    except IndexError as e:
        print(f"索引错误: {e}")
        print(f"异常类型: {type(e).__name__}")
    
    # 5. KeyError - 键错误
    print("\n5. KeyError 演示:")
    try:
        my_dict = {"a": 1, "b": 2}
        value = my_dict["c"]
    except KeyError as e:
        print(f"键错误: {e}")
        print(f"异常类型: {type(e).__name__}")
    
    # 6. AttributeError - 属性错误
    print("\n6. AttributeError 演示:")
    try:
        my_string = "hello"
        my_string.nonexistent_method()
    except AttributeError as e:
        print(f"属性错误: {e}")
        print(f"异常类型: {type(e).__name__}")
    
    # 7. FileNotFoundError - 文件未找到错误
    print("\n7. FileNotFoundError 演示:")
    try:
        with open("nonexistent_file.txt", "r") as file:
            content = file.read()
    except FileNotFoundError as e:
        print(f"文件未找到错误: {e}")
        print(f"异常类型: {type(e).__name__}")


def demo_try_except_patterns():
    """演示不同的try-except模式"""
    print("\n=== try-except 模式演示 ===")
    
    # 1. 捕获单个异常
    print("\n1. 捕获单个异常:")
    def safe_divide(a, b):
        try:
            return a / b
        except ZeroDivisionError:
            print("错误: 不能除以零")
            return None
    
    print(f"safe_divide(10, 2) = {safe_divide(10, 2)}")
    print(f"safe_divide(10, 0) = {safe_divide(10, 0)}")
    
    # 2. 捕获多个异常（分别处理）
    print("\n2. 捕获多个异常（分别处理）:")
    def safe_convert_and_divide(a, b):
        try:
            num_a = float(a)
            num_b = float(b)
            return num_a / num_b
        except ValueError:
            print("错误: 输入的不是有效数字")
            return None
        except ZeroDivisionError:
            print("错误: 不能除以零")
            return None
    
    print(f"safe_convert_and_divide('10', '2') = {safe_convert_and_divide('10', '2')}")
    print(f"safe_convert_and_divide('abc', '2') = {safe_convert_and_divide('abc', '2')}")
    print(f"safe_convert_and_divide('10', '0') = {safe_convert_and_divide('10', '0')}")
    
    # 3. 捕获多个异常（统一处理）
    print("\n3. 捕获多个异常（统一处理）:")
    def safe_list_operation(data, index):
        try:
            return data[index] * 2
        except (IndexError, TypeError) as e:
            print(f"列表操作错误: {e}")
            return None
    
    test_list = [1, 2, 3, 4, 5]
    print(f"safe_list_operation([1,2,3,4,5], 2) = {safe_list_operation(test_list, 2)}")
    print(f"safe_list_operation([1,2,3,4,5], 10) = {safe_list_operation(test_list, 10)}")
    print(f"safe_list_operation([1,2,3,4,5], 'a') = {safe_list_operation(test_list, 'a')}")
    
    # 4. 捕获所有异常
    print("\n4. 捕获所有异常:")
    def robust_operation(func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"操作失败: {type(e).__name__}: {e}")
            return None
    
    # 测试各种操作
    print(f"robust_operation(int, '123') = {robust_operation(int, '123')}")
    print(f"robust_operation(int, 'abc') = {robust_operation(int, 'abc')}")
    print(f"robust_operation(lambda x: x/0, 10) = {robust_operation(lambda x: x/0, 10)}")


def demo_exception_information():
    """演示如何获取异常信息"""
    print("\n=== 异常信息获取演示 ===")
    
    import traceback
    import sys
    
    def detailed_exception_info():
        try:
            # 故意引发异常
            result = 10 / 0
        except Exception as e:
            print("1. 基本异常信息:")
            print(f"   异常类型: {type(e).__name__}")
            print(f"   异常消息: {str(e)}")
            print(f"   异常对象: {repr(e)}")
            
            print("\n2. 详细异常信息:")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(f"   异常类型: {exc_type}")
            print(f"   异常值: {exc_value}")
            print(f"   异常追踪: {exc_traceback}")
            
            print("\n3. 格式化的异常追踪:")
            traceback.print_exc()
            
            print("\n4. 获取异常追踪字符串:")
            tb_str = traceback.format_exc()
            print(f"   追踪字符串长度: {len(tb_str)} 字符")
            print(f"   前100个字符: {tb_str[:100]}...")
    
    detailed_exception_info()


def demo_nested_exceptions():
    """演示嵌套异常处理"""
    print("\n=== 嵌套异常处理演示 ===")
    
    def level_3_function():
        """第三层函数 - 最底层"""
        try:
            return 10 / 0
        except ZeroDivisionError as e:
            print(f"Level 3: 捕获到除零错误 - {e}")
            raise ValueError("Level 3 转换的错误") from e
    
    def level_2_function():
        """第二层函数 - 中间层"""
        try:
            return level_3_function()
        except ValueError as e:
            print(f"Level 2: 捕获到值错误 - {e}")
            print(f"Level 2: 原始异常 - {e.__cause__}")
            raise RuntimeError("Level 2 处理失败") from e
    
    def level_1_function():
        """第一层函数 - 最上层"""
        try:
            return level_2_function()
        except RuntimeError as e:
            print(f"Level 1: 捕获到运行时错误 - {e}")
            print(f"Level 1: 原始异常 - {e.__cause__}")
            print(f"Level 1: 根异常 - {e.__cause__.__cause__}")
            return "处理完成"
    
    result = level_1_function()
    print(f"最终结果: {result}")


def demo_exception_best_practices():
    """演示异常处理最佳实践"""
    print("\n=== 异常处理最佳实践演示 ===")
    
    # 1. 具体化异常处理
    print("\n1. 具体化异常处理:")
    def good_file_reader(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"文件 {filename} 不存在")
            return None
        except PermissionError:
            print(f"没有权限读取文件 {filename}")
            return None
        except UnicodeDecodeError:
            print(f"文件 {filename} 编码错误")
            return None
    
    # 测试文件读取
    content = good_file_reader("nonexistent.txt")
    
    # 2. 异常信息记录
    print("\n2. 异常信息记录:")
    import logging
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    def logged_operation(data):
        try:
            result = []
            for item in data:
                if isinstance(item, str):
                    result.append(int(item))
                else:
                    result.append(item * 2)
            return result
        except ValueError as e:
            logger.error(f"数据转换错误: {e}")
            raise
        except Exception as e:
            logger.error(f"未知错误: {e}", exc_info=True)
            raise
    
    # 测试数据处理
    try:
        test_data = [1, "2", "abc", 4]
        result = logged_operation(test_data)
    except Exception:
        print("操作失败，已记录日志")
    
    # 3. 资源清理
    print("\n3. 资源清理:")
    def safe_resource_operation():
        resource = None
        try:
            # 模拟获取资源
            resource = "重要资源"
            print(f"获取资源: {resource}")
            
            # 模拟可能失败的操作
            if True:  # 模拟条件
                raise RuntimeError("操作失败")
            
            return "操作成功"
        except Exception as e:
            print(f"操作异常: {e}")
            return None
        finally:
            if resource:
                print(f"清理资源: {resource}")
                resource = None
    
    result = safe_resource_operation()
    print(f"操作结果: {result}")


def main():
    """主函数"""
    print("Session11 示例1: 基础异常处理")
    print("=" * 50)
    
    demo_common_exceptions()
    demo_try_except_patterns()
    demo_exception_information()
    demo_nested_exceptions()
    demo_exception_best_practices()
    
    print("\n示例演示完成！")


if __name__ == "__main__":
    main()