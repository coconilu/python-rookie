#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session11 练习题: 错误处理与调试

本文件包含了关于错误处理与调试的练习题，涵盖：
1. 基础异常处理
2. 自定义异常
3. 调试技巧
4. 日志记录
5. 综合应用

作者: Python教程团队
创建日期: 2024-01-15
"""

import logging
import json
import os
from typing import List, Dict, Any, Optional


# ==================== 练习1: 基础异常处理 ====================

def exercise1_safe_division():
    """
    练习1: 安全除法函数
    
    要求:
    1. 编写一个安全的除法函数 safe_divide(a, b)
    2. 处理除零错误、类型错误等异常
    3. 返回结果或错误信息
    
    提示:
    - 使用 try-except 处理异常
    - 考虑不同类型的输入
    - 返回合适的错误信息
    """
    print("练习1: 安全除法函数")
    
    def safe_divide(a, b):
        """
        安全的除法函数
        
        Args:
            a: 被除数
            b: 除数
        
        Returns:
            tuple: (success: bool, result: float or str)
        """
        # TODO: 在这里实现安全除法逻辑
        # 提示: 处理 ZeroDivisionError, TypeError, ValueError 等异常
        pass
    
    # 测试用例
    test_cases = [
        (10, 2),      # 正常情况
        (10, 0),      # 除零错误
        ("10", 2),    # 类型错误
        (10, "a"),    # 类型错误
        (10.5, 2.5),  # 浮点数
    ]
    
    print("测试结果:")
    for a, b in test_cases:
        success, result = safe_divide(a, b)
        print(f"safe_divide({a}, {b}) -> 成功: {success}, 结果: {result}")


def exercise2_file_operations():
    """
    练习2: 安全文件操作
    
    要求:
    1. 编写函数 safe_read_file(filename) 安全读取文件
    2. 编写函数 safe_write_file(filename, content) 安全写入文件
    3. 处理文件不存在、权限错误等异常
    4. 使用 finally 确保资源清理
    
    提示:
    - 处理 FileNotFoundError, PermissionError, IOError
    - 使用 with 语句或 finally 确保文件关闭
    - 返回操作结果和错误信息
    """
    print("\n练习2: 安全文件操作")
    
    def safe_read_file(filename):
        """
        安全读取文件
        
        Args:
            filename (str): 文件名
        
        Returns:
            tuple: (success: bool, content: str or error_msg: str)
        """
        # TODO: 在这里实现安全文件读取逻辑
        pass
    
    def safe_write_file(filename, content):
        """
        安全写入文件
        
        Args:
            filename (str): 文件名
            content (str): 文件内容
        
        Returns:
            tuple: (success: bool, message: str)
        """
        # TODO: 在这里实现安全文件写入逻辑
        pass
    
    # 测试文件操作
    test_content = "这是测试内容\n第二行内容"
    
    # 测试写入
    success, msg = safe_write_file("test_file.txt", test_content)
    print(f"写入文件: 成功={success}, 消息={msg}")
    
    # 测试读取
    success, content = safe_read_file("test_file.txt")
    print(f"读取文件: 成功={success}, 内容={content[:50] if success else content}")
    
    # 测试读取不存在的文件
    success, content = safe_read_file("nonexistent.txt")
    print(f"读取不存在文件: 成功={success}, 错误={content}")
    
    # 清理测试文件
    try:
        os.remove("test_file.txt")
    except:
        pass


# ==================== 练习3: 自定义异常 ====================

class ValidationError(Exception):
    """验证错误基类"""
    pass

class EmailValidationError(ValidationError):
    """邮箱验证错误"""
    pass

class PasswordValidationError(ValidationError):
    """密码验证错误"""
    pass

class AgeValidationError(ValidationError):
    """年龄验证错误"""
    pass


def exercise3_user_validation():
    """
    练习3: 用户数据验证
    
    要求:
    1. 创建用户验证类 UserValidator
    2. 实现邮箱、密码、年龄验证方法
    3. 使用自定义异常处理验证错误
    4. 编写完整的用户注册函数
    
    验证规则:
    - 邮箱: 必须包含 @ 和 .
    - 密码: 长度至少8位，包含字母和数字
    - 年龄: 18-120之间的整数
    """
    print("\n练习3: 用户数据验证")
    
    class UserValidator:
        """用户数据验证器"""
        
        @staticmethod
        def validate_email(email):
            """
            验证邮箱格式
            
            Args:
                email (str): 邮箱地址
            
            Raises:
                EmailValidationError: 邮箱格式错误
            """
            # TODO: 实现邮箱验证逻辑
            # 提示: 检查是否包含 @ 和 ., 长度等
            pass
        
        @staticmethod
        def validate_password(password):
            """
            验证密码强度
            
            Args:
                password (str): 密码
            
            Raises:
                PasswordValidationError: 密码不符合要求
            """
            # TODO: 实现密码验证逻辑
            # 提示: 检查长度、是否包含字母和数字
            pass
        
        @staticmethod
        def validate_age(age):
            """
            验证年龄
            
            Args:
                age: 年龄（可能是字符串或数字）
            
            Raises:
                AgeValidationError: 年龄不符合要求
            """
            # TODO: 实现年龄验证逻辑
            # 提示: 转换为整数，检查范围
            pass
    
    def register_user(email, password, age):
        """
        用户注册函数
        
        Args:
            email (str): 邮箱
            password (str): 密码
            age: 年龄
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # TODO: 使用 UserValidator 验证所有字段
            # 如果验证通过，返回成功信息
            # 如果验证失败，捕获异常并返回错误信息
            pass
        except ValidationError as e:
            return False, f"验证失败: {e}"
        except Exception as e:
            return False, f"未知错误: {e}"
    
    # 测试用例
    test_users = [
        ("user@example.com", "password123", 25),      # 正常用户
        ("invalid-email", "password123", 25),          # 邮箱错误
        ("user@example.com", "123", 25),               # 密码太短
        ("user@example.com", "password", 25),          # 密码无数字
        ("user@example.com", "password123", 15),       # 年龄太小
        ("user@example.com", "password123", "abc"),    # 年龄格式错误
    ]
    
    print("用户注册测试:")
    for email, password, age in test_users:
        success, message = register_user(email, password, age)
        print(f"注册 {email}: 成功={success}, 消息={message}")


# ==================== 练习4: 调试技巧 ====================

def exercise4_debugging_practice():
    """
    练习4: 调试实践
    
    要求:
    1. 找出并修复以下代码中的错误
    2. 使用调试技巧定位问题
    3. 添加适当的日志记录
    
    提示:
    - 使用 print 调试
    - 使用 assert 验证假设
    - 添加日志记录
    """
    print("\n练习4: 调试实践")
    
    # 设置日志
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
    logger = logging.getLogger('debug_practice')
    
    def buggy_function(numbers):
        """
        这个函数有多个错误，需要调试和修复
        目标: 计算数字列表的平均值，忽略非数字项
        """
        logger.debug(f"开始处理数字列表: {numbers}")
        
        total = 0
        count = 0
        
        for i in range(len(numbers)):
            item = numbers[i]
            logger.debug(f"处理第 {i} 项: {item}")
            
            # TODO: 这里有错误，需要修复
            # 提示: 需要检查类型，处理异常
            if isinstance(item, (int, float)):
                total += item
                count += 1
            else:
                logger.warning(f"跳过非数字项: {item}")
        
        # TODO: 这里可能有除零错误
        average = total / count
        logger.info(f"计算完成: 总和={total}, 数量={count}, 平均值={average}")
        
        return average
    
    def calculate_statistics(data_list):
        """
        计算统计信息
        这个函数也有错误需要修复
        """
        logger.debug(f"计算统计信息: {data_list}")
        
        results = {}
        
        for name, numbers in data_list.items():
            logger.debug(f"处理数据集: {name}")
            
            try:
                # TODO: 调用 buggy_function，处理可能的异常
                avg = buggy_function(numbers)
                results[name] = avg
                logger.info(f"{name} 的平均值: {avg}")
            except Exception as e:
                logger.error(f"计算 {name} 时出错: {e}")
                results[name] = None
        
        return results
    
    # 测试数据（包含各种边界情况）
    test_data = {
        "正常数据": [1, 2, 3, 4, 5],
        "包含字符串": [1, "abc", 3, 4, 5],
        "包含None": [1, 2, None, 4, 5],
        "空列表": [],
        "全是字符串": ["a", "b", "c"],
        "混合类型": [1, 2.5, "3", 4, None, 5.5]
    }
    
    print("调试测试结果:")
    results = calculate_statistics(test_data)
    
    for name, avg in results.items():
        if avg is not None:
            print(f"{name}: {avg:.2f}")
        else:
            print(f"{name}: 计算失败")


# ==================== 练习5: 日志记录实践 ====================

def exercise5_logging_practice():
    """
    练习5: 日志记录实践
    
    要求:
    1. 创建一个简单的任务管理系统
    2. 实现完整的日志记录
    3. 使用不同级别的日志
    4. 配置文件和控制台输出
    
    功能:
    - 添加任务
    - 完成任务
    - 删除任务
    - 查看任务列表
    """
    print("\n练习5: 日志记录实践")
    
    # TODO: 配置日志系统
    # 提示: 设置文件和控制台处理器，不同的格式和级别
    
    class TaskManager:
        """任务管理器"""
        
        def __init__(self):
            self.tasks = {}
            self.next_id = 1
            # TODO: 创建日志记录器
            self.logger = logging.getLogger('TaskManager')
        
        def add_task(self, title, description=""):
            """
            添加任务
            
            Args:
                title (str): 任务标题
                description (str): 任务描述
            
            Returns:
                int: 任务ID
            """
            # TODO: 添加适当的日志记录
            # 提示: 使用 info 级别记录任务添加
            
            task_id = self.next_id
            self.next_id += 1
            
            task = {
                'id': task_id,
                'title': title,
                'description': description,
                'completed': False,
                'created_at': '2024-01-15 10:00:00'  # 简化时间
            }
            
            self.tasks[task_id] = task
            
            # TODO: 记录任务添加成功
            
            return task_id
        
        def complete_task(self, task_id):
            """
            完成任务
            
            Args:
                task_id (int): 任务ID
            
            Returns:
                bool: 是否成功
            """
            # TODO: 添加调试日志
            
            if task_id not in self.tasks:
                # TODO: 记录警告日志
                return False
            
            if self.tasks[task_id]['completed']:
                # TODO: 记录警告日志
                return False
            
            self.tasks[task_id]['completed'] = True
            # TODO: 记录信息日志
            
            return True
        
        def delete_task(self, task_id):
            """
            删除任务
            
            Args:
                task_id (int): 任务ID
            
            Returns:
                bool: 是否成功
            """
            # TODO: 添加调试和信息日志
            
            if task_id not in self.tasks:
                # TODO: 记录错误日志
                return False
            
            del self.tasks[task_id]
            # TODO: 记录信息日志
            
            return True
        
        def get_tasks(self, completed=None):
            """
            获取任务列表
            
            Args:
                completed (bool, optional): 过滤完成状态
            
            Returns:
                list: 任务列表
            """
            # TODO: 添加调试日志
            
            tasks = list(self.tasks.values())
            
            if completed is not None:
                tasks = [t for t in tasks if t['completed'] == completed]
            
            # TODO: 记录查询结果
            
            return tasks
    
    # 测试任务管理器
    tm = TaskManager()
    
    # 添加任务
    task1 = tm.add_task("学习Python", "完成Session11的练习")
    task2 = tm.add_task("写代码", "实现任务管理系统")
    task3 = tm.add_task("调试", "修复所有bug")
    
    # 完成任务
    tm.complete_task(task1)
    tm.complete_task(999)  # 不存在的任务
    
    # 查看任务
    all_tasks = tm.get_tasks()
    completed_tasks = tm.get_tasks(completed=True)
    pending_tasks = tm.get_tasks(completed=False)
    
    print(f"总任务数: {len(all_tasks)}")
    print(f"已完成: {len(completed_tasks)}")
    print(f"待完成: {len(pending_tasks)}")
    
    # 删除任务
    tm.delete_task(task2)
    tm.delete_task(999)  # 不存在的任务
    
    print("\n最终任务列表:")
    for task in tm.get_tasks():
        status = "✓" if task['completed'] else "○"
        print(f"{status} [{task['id']}] {task['title']}")


# ==================== 练习6: 综合应用 ====================

def exercise6_comprehensive_application():
    """
    练习6: 综合应用 - 配置文件管理器
    
    要求:
    1. 创建一个配置文件管理器
    2. 支持JSON格式的配置文件
    3. 实现完整的错误处理
    4. 添加详细的日志记录
    5. 使用自定义异常
    6. 包含调试功能
    
    功能:
    - 加载配置文件
    - 保存配置文件
    - 获取/设置配置项
    - 验证配置格式
    - 备份和恢复
    """
    print("\n练习6: 综合应用 - 配置文件管理器")
    
    # TODO: 定义自定义异常类
    class ConfigError(Exception):
        """配置错误基类"""
        pass
    
    class ConfigFileError(ConfigError):
        """配置文件错误"""
        pass
    
    class ConfigValidationError(ConfigError):
        """配置验证错误"""
        pass
    
    class ConfigManager:
        """配置文件管理器"""
        
        def __init__(self, config_file):
            self.config_file = config_file
            self.config_data = {}
            self.backup_file = f"{config_file}.backup"
            
            # TODO: 设置日志记录器
            self.logger = logging.getLogger('ConfigManager')
        
        def load_config(self):
            """
            加载配置文件
            
            Raises:
                ConfigFileError: 文件操作错误
            """
            # TODO: 实现配置加载逻辑
            # 提示: 处理文件不存在、JSON格式错误等异常
            # 添加适当的日志记录
            pass
        
        def save_config(self):
            """
            保存配置文件
            
            Raises:
                ConfigFileError: 文件操作错误
            """
            # TODO: 实现配置保存逻辑
            # 提示: 创建备份，处理写入错误
            # 添加适当的日志记录
            pass
        
        def get_config(self, key, default=None):
            """
            获取配置项
            
            Args:
                key (str): 配置键，支持点号分隔的嵌套键
                default: 默认值
            
            Returns:
                配置值或默认值
            """
            # TODO: 实现配置获取逻辑
            # 提示: 支持嵌套键如 "database.host"
            # 添加调试日志
            pass
        
        def set_config(self, key, value):
            """
            设置配置项
            
            Args:
                key (str): 配置键
                value: 配置值
            """
            # TODO: 实现配置设置逻辑
            # 提示: 支持嵌套键设置
            # 添加信息日志
            pass
        
        def validate_config(self, schema):
            """
            验证配置格式
            
            Args:
                schema (dict): 配置模式
            
            Raises:
                ConfigValidationError: 验证失败
            """
            # TODO: 实现配置验证逻辑
            # 提示: 检查必需字段、类型等
            pass
        
        def create_backup(self):
            """
            创建配置备份
            
            Returns:
                bool: 是否成功
            """
            # TODO: 实现备份逻辑
            pass
        
        def restore_backup(self):
            """
            恢复配置备份
            
            Returns:
                bool: 是否成功
            """
            # TODO: 实现恢复逻辑
            pass
    
    # 测试配置管理器
    config_file = "test_config.json"
    
    try:
        # 创建配置管理器
        cm = ConfigManager(config_file)
        
        # 设置一些配置
        cm.set_config("app.name", "测试应用")
        cm.set_config("app.version", "1.0.0")
        cm.set_config("database.host", "localhost")
        cm.set_config("database.port", 5432)
        
        # 保存配置
        cm.save_config()
        
        # 重新加载
        cm.load_config()
        
        # 获取配置
        app_name = cm.get_config("app.name")
        db_host = cm.get_config("database.host")
        
        print(f"应用名称: {app_name}")
        print(f"数据库主机: {db_host}")
        
        # 验证配置
        schema = {
            "app": {"required": True, "type": dict},
            "database": {"required": True, "type": dict}
        }
        cm.validate_config(schema)
        
        print("配置验证通过")
        
    except Exception as e:
        print(f"配置管理器测试失败: {e}")
    
    finally:
        # 清理测试文件
        for file in [config_file, f"{config_file}.backup"]:
            try:
                os.remove(file)
            except:
                pass


def main():
    """主函数 - 运行所有练习"""
    print("Session11 练习题: 错误处理与调试")
    print("=" * 60)
    
    exercises = [
        exercise1_safe_division,
        exercise2_file_operations,
        exercise3_user_validation,
        exercise4_debugging_practice,
        exercise5_logging_practice,
        exercise6_comprehensive_application
    ]
    
    for i, exercise in enumerate(exercises, 1):
        try:
            print(f"\n{'='*20} 练习 {i} {'='*20}")
            exercise()
        except Exception as e:
            print(f"练习 {i} 执行失败: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("所有练习完成！")
    print("\n提示:")
    print("1. 这些练习需要你自己实现 TODO 部分的代码")
    print("2. 运行练习时注意观察日志输出")
    print("3. 尝试故意制造错误来测试异常处理")
    print("4. 使用调试器逐步执行代码")
    print("5. 查看生成的日志文件")


if __name__ == "__main__":
    main()