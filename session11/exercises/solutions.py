#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session11 练习题答案: 错误处理与调试

本文件包含了练习题的参考答案，展示了错误处理与调试的最佳实践。

作者: Python教程团队
创建日期: 2024-01-15
"""

import logging
import json
import os
import shutil
from typing import List, Dict, Any, Optional, Union


# ==================== 练习1答案: 基础异常处理 ====================

def solution1_safe_division():
    """练习1答案: 安全除法函数"""
    print("练习1答案: 安全除法函数")
    
    def safe_divide(a, b):
        """
        安全的除法函数
        
        Args:
            a: 被除数
            b: 除数
        
        Returns:
            tuple: (success: bool, result: float or str)
        """
        try:
            # 尝试转换为数字
            num_a = float(a)
            num_b = float(b)
            
            # 检查除零
            if num_b == 0:
                return False, "错误: 除数不能为零"
            
            # 执行除法
            result = num_a / num_b
            return True, result
            
        except (TypeError, ValueError) as e:
            return False, f"错误: 输入类型无效 - {e}"
        except Exception as e:
            return False, f"未知错误: {e}"
    
    # 测试用例
    test_cases = [
        (10, 2),      # 正常情况
        (10, 0),      # 除零错误
        ("10", 2),    # 字符串数字
        (10, "a"),    # 无效字符串
        (10.5, 2.5),  # 浮点数
        (None, 5),    # None值
        ([], 5),      # 列表类型
    ]
    
    print("测试结果:")
    for a, b in test_cases:
        success, result = safe_divide(a, b)
        print(f"safe_divide({a}, {b}) -> 成功: {success}, 结果: {result}")


def solution2_file_operations():
    """练习2答案: 安全文件操作"""
    print("\n练习2答案: 安全文件操作")
    
    def safe_read_file(filename):
        """
        安全读取文件
        
        Args:
            filename (str): 文件名
        
        Returns:
            tuple: (success: bool, content: str or error_msg: str)
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                return True, content
        except FileNotFoundError:
            return False, f"文件不存在: {filename}"
        except PermissionError:
            return False, f"没有权限读取文件: {filename}"
        except UnicodeDecodeError:
            # 尝试其他编码
            try:
                with open(filename, 'r', encoding='gbk') as file:
                    content = file.read()
                    return True, content
            except Exception:
                return False, f"文件编码错误: {filename}"
        except IOError as e:
            return False, f"IO错误: {e}"
        except Exception as e:
            return False, f"未知错误: {e}"
    
    def safe_write_file(filename, content):
        """
        安全写入文件
        
        Args:
            filename (str): 文件名
            content (str): 文件内容
        
        Returns:
            tuple: (success: bool, message: str)
        """
        backup_file = None
        try:
            # 如果文件存在，创建备份
            if os.path.exists(filename):
                backup_file = f"{filename}.backup"
                shutil.copy2(filename, backup_file)
            
            # 写入文件
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(content)
            
            # 删除备份文件
            if backup_file and os.path.exists(backup_file):
                os.remove(backup_file)
            
            return True, f"文件写入成功: {filename}"
            
        except PermissionError:
            # 恢复备份
            if backup_file and os.path.exists(backup_file):
                shutil.move(backup_file, filename)
            return False, f"没有权限写入文件: {filename}"
        except IOError as e:
            # 恢复备份
            if backup_file and os.path.exists(backup_file):
                shutil.move(backup_file, filename)
            return False, f"IO错误: {e}"
        except Exception as e:
            # 恢复备份
            if backup_file and os.path.exists(backup_file):
                shutil.move(backup_file, filename)
            return False, f"未知错误: {e}"
    
    # 测试文件操作
    test_content = "这是测试内容\n第二行内容\n包含中文字符"
    
    # 测试写入
    success, msg = safe_write_file("test_file.txt", test_content)
    print(f"写入文件: 成功={success}, 消息={msg}")
    
    # 测试读取
    success, content = safe_read_file("test_file.txt")
    print(f"读取文件: 成功={success}, 内容长度={len(content) if success else 0}")
    if success:
        print(f"内容预览: {content[:50]}...")
    
    # 测试读取不存在的文件
    success, content = safe_read_file("nonexistent.txt")
    print(f"读取不存在文件: 成功={success}, 错误={content}")
    
    # 清理测试文件
    try:
        os.remove("test_file.txt")
    except:
        pass


# ==================== 练习3答案: 自定义异常 ====================

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


def solution3_user_validation():
    """练习3答案: 用户数据验证"""
    print("\n练习3答案: 用户数据验证")
    
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
            if not isinstance(email, str):
                raise EmailValidationError("邮箱必须是字符串")
            
            if len(email) < 5:
                raise EmailValidationError("邮箱长度至少5个字符")
            
            if '@' not in email:
                raise EmailValidationError("邮箱必须包含@符号")
            
            if '.' not in email:
                raise EmailValidationError("邮箱必须包含.符号")
            
            # 检查@符号位置
            at_index = email.find('@')
            if at_index == 0 or at_index == len(email) - 1:
                raise EmailValidationError("@符号位置不正确")
            
            # 检查.符号在@之后
            if email.rfind('.') <= at_index:
                raise EmailValidationError(".符号必须在@符号之后")
            
            # 检查是否有连续的特殊字符
            if '..' in email or '@@' in email:
                raise EmailValidationError("邮箱格式不正确")
        
        @staticmethod
        def validate_password(password):
            """
            验证密码强度
            
            Args:
                password (str): 密码
            
            Raises:
                PasswordValidationError: 密码不符合要求
            """
            if not isinstance(password, str):
                raise PasswordValidationError("密码必须是字符串")
            
            if len(password) < 8:
                raise PasswordValidationError("密码长度至少8位")
            
            # 检查是否包含字母
            has_letter = any(c.isalpha() for c in password)
            if not has_letter:
                raise PasswordValidationError("密码必须包含字母")
            
            # 检查是否包含数字
            has_digit = any(c.isdigit() for c in password)
            if not has_digit:
                raise PasswordValidationError("密码必须包含数字")
            
            # 可选：检查是否包含大小写字母
            has_upper = any(c.isupper() for c in password)
            has_lower = any(c.islower() for c in password)
            if not (has_upper and has_lower):
                # 这里只是警告，不抛出异常
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
            try:
                age_int = int(age)
            except (ValueError, TypeError):
                raise AgeValidationError(f"年龄必须是数字，得到: {age}")
            
            if age_int < 18:
                raise AgeValidationError(f"年龄必须大于等于18岁，得到: {age_int}")
            
            if age_int > 120:
                raise AgeValidationError(f"年龄必须小于等于120岁，得到: {age_int}")
    
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
            # 验证所有字段
            UserValidator.validate_email(email)
            UserValidator.validate_password(password)
            UserValidator.validate_age(age)
            
            # 如果所有验证都通过
            return True, "用户注册成功"
            
        except EmailValidationError as e:
            return False, f"邮箱验证失败: {e}"
        except PasswordValidationError as e:
            return False, f"密码验证失败: {e}"
        except AgeValidationError as e:
            return False, f"年龄验证失败: {e}"
        except ValidationError as e:
            return False, f"验证失败: {e}"
        except Exception as e:
            return False, f"未知错误: {e}"
    
    # 测试用例
    test_users = [
        ("user@example.com", "Password123", 25),       # 正常用户
        ("invalid-email", "Password123", 25),           # 邮箱错误
        ("user@example.com", "123", 25),                # 密码太短
        ("user@example.com", "password", 25),           # 密码无数字
        ("user@example.com", "PASSWORD123", 25),        # 密码无小写
        ("user@example.com", "Password123", 15),        # 年龄太小
        ("user@example.com", "Password123", 150),       # 年龄太大
        ("user@example.com", "Password123", "abc"),     # 年龄格式错误
        ("user@", "Password123", 25),                   # 邮箱格式错误
        ("@example.com", "Password123", 25),            # 邮箱格式错误
    ]
    
    print("用户注册测试:")
    for email, password, age in test_users:
        success, message = register_user(email, password, age)
        status = "✓" if success else "✗"
        print(f"{status} {email}: {message}")


# ==================== 练习4答案: 调试技巧 ====================

def solution4_debugging_practice():
    """练习4答案: 调试实践"""
    print("\n练习4答案: 调试实践")
    
    # 设置日志
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
    logger = logging.getLogger('debug_practice')
    
    def fixed_function(numbers):
        """
        修复后的函数：计算数字列表的平均值，忽略非数字项
        """
        logger.debug(f"开始处理数字列表: {numbers}")
        
        # 输入验证
        if not isinstance(numbers, (list, tuple)):
            logger.error(f"输入必须是列表或元组，得到: {type(numbers)}")
            raise TypeError("输入必须是列表或元组")
        
        if len(numbers) == 0:
            logger.warning("输入列表为空")
            raise ValueError("不能计算空列表的平均值")
        
        total = 0
        count = 0
        
        for i, item in enumerate(numbers):
            logger.debug(f"处理第 {i} 项: {item} (类型: {type(item)})")
            
            # 修复：正确的类型检查和转换
            try:
                if isinstance(item, (int, float)):
                    total += item
                    count += 1
                    logger.debug(f"添加数字: {item}, 当前总和: {total}, 计数: {count}")
                elif isinstance(item, str):
                    # 尝试转换字符串为数字
                    try:
                        num_value = float(item)
                        total += num_value
                        count += 1
                        logger.debug(f"转换字符串 '{item}' 为数字: {num_value}")
                    except ValueError:
                        logger.warning(f"无法转换字符串为数字: '{item}'")
                else:
                    logger.warning(f"跳过非数字项: {item} (类型: {type(item)})")
            except Exception as e:
                logger.error(f"处理项 {item} 时出错: {e}")
                continue
        
        # 修复：检查除零错误
        if count == 0:
            logger.error("没有有效的数字项")
            raise ValueError("列表中没有有效的数字")
        
        average = total / count
        logger.info(f"计算完成: 总和={total}, 数量={count}, 平均值={average}")
        
        # 断言验证结果
        assert isinstance(average, (int, float)), "平均值必须是数字"
        assert count > 0, "计数必须大于0"
        
        return average
    
    def calculate_statistics(data_list):
        """
        修复后的统计计算函数
        """
        logger.debug(f"计算统计信息，数据集数量: {len(data_list)}")
        
        if not isinstance(data_list, dict):
            logger.error(f"输入必须是字典，得到: {type(data_list)}")
            raise TypeError("输入必须是字典")
        
        results = {}
        
        for name, numbers in data_list.items():
            logger.debug(f"处理数据集: {name}, 数据: {numbers}")
            
            try:
                # 调用修复后的函数
                avg = fixed_function(numbers)
                results[name] = avg
                logger.info(f"{name} 的平均值: {avg:.2f}")
            except ValueError as e:
                logger.error(f"计算 {name} 时值错误: {e}")
                results[name] = None
            except TypeError as e:
                logger.error(f"计算 {name} 时类型错误: {e}")
                results[name] = None
            except Exception as e:
                logger.error(f"计算 {name} 时未知错误: {e}")
                results[name] = None
        
        return results
    
    # 测试数据（包含各种边界情况）
    test_data = {
        "正常数据": [1, 2, 3, 4, 5],
        "包含字符串数字": [1, "2", 3, "4.5", 5],
        "包含无效字符串": [1, "abc", 3, 4, 5],
        "包含None": [1, 2, None, 4, 5],
        "空列表": [],
        "全是字符串": ["a", "b", "c"],
        "全是字符串数字": ["1", "2", "3"],
        "混合类型": [1, 2.5, "3", 4, None, 5.5, "abc"]
    }
    
    print("调试测试结果:")
    try:
        results = calculate_statistics(test_data)
        
        for name, avg in results.items():
            if avg is not None:
                print(f"✓ {name}: {avg:.2f}")
            else:
                print(f"✗ {name}: 计算失败")
    except Exception as e:
        logger.exception(f"统计计算失败: {e}")
        print(f"统计计算失败: {e}")


# ==================== 练习5答案: 日志记录实践 ====================

def solution5_logging_practice():
    """练习5答案: 日志记录实践"""
    print("\n练习5答案: 日志记录实践")
    
    # 配置日志系统
    def setup_logging():
        """设置日志配置"""
        # 创建日志目录
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # 获取根日志记录器
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        
        # 清除现有处理器
        root_logger.handlers.clear()
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_format)
        
        # 文件处理器
        file_handler = logging.FileHandler('logs/task_manager.log', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - '
            '%(filename)s:%(lineno)d - %(funcName)s() - %(message)s'
        )
        file_handler.setFormatter(file_format)
        
        # 错误文件处理器
        error_handler = logging.FileHandler('logs/task_errors.log', encoding='utf-8')
        error_handler.setLevel(logging.ERROR)
        error_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s\n'
            'Location: %(pathname)s:%(lineno)d in %(funcName)s()\n'
            'Exception: %(exc_text)s\n' + '='*50
        )
        error_handler.setFormatter(error_format)
        
        # 添加处理器
        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(error_handler)
    
    # 设置日志
    setup_logging()
    
    class TaskManager:
        """任务管理器"""
        
        def __init__(self):
            self.tasks = {}
            self.next_id = 1
            self.logger = logging.getLogger('TaskManager')
            self.logger.info("任务管理器初始化完成")
        
        def add_task(self, title, description=""):
            """
            添加任务
            
            Args:
                title (str): 任务标题
                description (str): 任务描述
            
            Returns:
                int: 任务ID
            """
            self.logger.debug(f"准备添加任务: title='{title}', description='{description}'")
            
            # 输入验证
            if not title or not isinstance(title, str):
                self.logger.error(f"无效的任务标题: {title}")
                raise ValueError("任务标题不能为空且必须是字符串")
            
            task_id = self.next_id
            self.next_id += 1
            
            task = {
                'id': task_id,
                'title': title.strip(),
                'description': description.strip() if description else "",
                'completed': False,
                'created_at': '2024-01-15 10:00:00'  # 简化时间
            }
            
            self.tasks[task_id] = task
            
            self.logger.info(f"任务添加成功: ID={task_id}, 标题='{title}'")
            self.logger.debug(f"当前任务总数: {len(self.tasks)}")
            
            return task_id
        
        def complete_task(self, task_id):
            """
            完成任务
            
            Args:
                task_id (int): 任务ID
            
            Returns:
                bool: 是否成功
            """
            self.logger.debug(f"尝试完成任务: ID={task_id}")
            
            if task_id not in self.tasks:
                self.logger.warning(f"任务不存在: ID={task_id}")
                return False
            
            if self.tasks[task_id]['completed']:
                self.logger.warning(f"任务已经完成: ID={task_id}")
                return False
            
            self.tasks[task_id]['completed'] = True
            task_title = self.tasks[task_id]['title']
            self.logger.info(f"任务完成: ID={task_id}, 标题='{task_title}'")
            
            return True
        
        def delete_task(self, task_id):
            """
            删除任务
            
            Args:
                task_id (int): 任务ID
            
            Returns:
                bool: 是否成功
            """
            self.logger.debug(f"尝试删除任务: ID={task_id}")
            
            if task_id not in self.tasks:
                self.logger.error(f"无法删除不存在的任务: ID={task_id}")
                return False
            
            task_title = self.tasks[task_id]['title']
            del self.tasks[task_id]
            self.logger.info(f"任务删除成功: ID={task_id}, 标题='{task_title}'")
            self.logger.debug(f"剩余任务数量: {len(self.tasks)}")
            
            return True
        
        def get_tasks(self, completed=None):
            """
            获取任务列表
            
            Args:
                completed (bool, optional): 过滤完成状态
            
            Returns:
                list: 任务列表
            """
            self.logger.debug(f"查询任务列表: completed={completed}")
            
            tasks = list(self.tasks.values())
            
            if completed is not None:
                original_count = len(tasks)
                tasks = [t for t in tasks if t['completed'] == completed]
                self.logger.debug(f"过滤后任务数量: {len(tasks)}/{original_count}")
            
            self.logger.info(f"返回任务列表: {len(tasks)} 个任务")
            
            return tasks
    
    # 测试任务管理器
    try:
        tm = TaskManager()
        
        # 添加任务
        task1 = tm.add_task("学习Python", "完成Session11的练习")
        task2 = tm.add_task("写代码", "实现任务管理系统")
        task3 = tm.add_task("调试", "修复所有bug")
        
        # 完成任务
        tm.complete_task(task1)
        tm.complete_task(999)  # 不存在的任务
        tm.complete_task(task1)  # 重复完成
        
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
        
        # 测试错误情况
        try:
            tm.add_task("")  # 空标题
        except ValueError as e:
            print(f"捕获预期错误: {e}")
        
        print("\n日志文件已生成:")
        print("- logs/task_manager.log (所有日志)")
        print("- logs/task_errors.log (错误日志)")
        
    except Exception as e:
        logging.exception(f"任务管理器测试失败: {e}")
        print(f"任务管理器测试失败: {e}")


# ==================== 练习6答案: 综合应用 ====================

def solution6_comprehensive_application():
    """练习6答案: 综合应用 - 配置文件管理器"""
    print("\n练习6答案: 综合应用 - 配置文件管理器")
    
    # 自定义异常类
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
            
            # 设置日志记录器
            self.logger = logging.getLogger('ConfigManager')
            self.logger.info(f"配置管理器初始化: {config_file}")
        
        def load_config(self):
            """
            加载配置文件
            
            Raises:
                ConfigFileError: 文件操作错误
            """
            self.logger.debug(f"开始加载配置文件: {self.config_file}")
            
            try:
                if not os.path.exists(self.config_file):
                    self.logger.warning(f"配置文件不存在，创建默认配置: {self.config_file}")
                    self.config_data = {}
                    self.save_config()
                    return
                
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config_data = json.load(f)
                
                self.logger.info(f"配置文件加载成功，包含 {len(self.config_data)} 个顶级配置项")
                
            except json.JSONDecodeError as e:
                self.logger.error(f"JSON格式错误: {e}")
                raise ConfigFileError(f"配置文件JSON格式错误: {e}")
            except FileNotFoundError:
                self.logger.error(f"配置文件不存在: {self.config_file}")
                raise ConfigFileError(f"配置文件不存在: {self.config_file}")
            except PermissionError:
                self.logger.error(f"没有权限读取配置文件: {self.config_file}")
                raise ConfigFileError(f"没有权限读取配置文件: {self.config_file}")
            except Exception as e:
                self.logger.error(f"加载配置文件时发生未知错误: {e}")
                raise ConfigFileError(f"加载配置文件失败: {e}")
        
        def save_config(self):
            """
            保存配置文件
            
            Raises:
                ConfigFileError: 文件操作错误
            """
            self.logger.debug(f"开始保存配置文件: {self.config_file}")
            
            try:
                # 创建备份
                if os.path.exists(self.config_file):
                    self.create_backup()
                
                # 保存配置
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(self.config_data, f, indent=2, ensure_ascii=False)
                
                self.logger.info(f"配置文件保存成功: {self.config_file}")
                
            except PermissionError:
                self.logger.error(f"没有权限写入配置文件: {self.config_file}")
                raise ConfigFileError(f"没有权限写入配置文件: {self.config_file}")
            except Exception as e:
                self.logger.error(f"保存配置文件时发生错误: {e}")
                # 尝试恢复备份
                if os.path.exists(self.backup_file):
                    self.restore_backup()
                raise ConfigFileError(f"保存配置文件失败: {e}")
        
        def get_config(self, key, default=None):
            """
            获取配置项
            
            Args:
                key (str): 配置键，支持点号分隔的嵌套键
                default: 默认值
            
            Returns:
                配置值或默认值
            """
            self.logger.debug(f"获取配置项: {key}")
            
            try:
                keys = key.split('.')
                value = self.config_data
                
                for k in keys:
                    if isinstance(value, dict) and k in value:
                        value = value[k]
                    else:
                        self.logger.debug(f"配置项不存在: {key}，返回默认值: {default}")
                        return default
                
                self.logger.debug(f"配置项获取成功: {key} = {value}")
                return value
                
            except Exception as e:
                self.logger.error(f"获取配置项时发生错误: {e}")
                return default
        
        def set_config(self, key, value):
            """
            设置配置项
            
            Args:
                key (str): 配置键
                value: 配置值
            """
            self.logger.debug(f"设置配置项: {key} = {value}")
            
            try:
                keys = key.split('.')
                config = self.config_data
                
                # 创建嵌套字典结构
                for k in keys[:-1]:
                    if k not in config:
                        config[k] = {}
                    elif not isinstance(config[k], dict):
                        self.logger.warning(f"覆盖非字典配置项: {k}")
                        config[k] = {}
                    config = config[k]
                
                # 设置最终值
                old_value = config.get(keys[-1])
                config[keys[-1]] = value
                
                self.logger.info(f"配置项设置成功: {key} = {value} (原值: {old_value})")
                
            except Exception as e:
                self.logger.error(f"设置配置项时发生错误: {e}")
                raise ConfigFileError(f"设置配置项失败: {e}")
        
        def validate_config(self, schema):
            """
            验证配置格式
            
            Args:
                schema (dict): 配置模式
            
            Raises:
                ConfigValidationError: 验证失败
            """
            self.logger.debug("开始验证配置格式")
            
            def validate_item(data, schema_item, path=""):
                """验证单个配置项"""
                if isinstance(schema_item, dict):
                    if 'required' in schema_item and schema_item['required']:
                        if not data:
                            raise ConfigValidationError(f"必需的配置项缺失: {path}")
                    
                    if 'type' in schema_item:
                        expected_type = schema_item['type']
                        if not isinstance(data, expected_type):
                            raise ConfigValidationError(
                                f"配置项类型错误: {path}，期望 {expected_type.__name__}，得到 {type(data).__name__}"
                            )
                    
                    if 'children' in schema_item and isinstance(data, dict):
                        for child_key, child_schema in schema_item['children'].items():
                            child_path = f"{path}.{child_key}" if path else child_key
                            child_data = data.get(child_key)
                            validate_item(child_data, child_schema, child_path)
            
            try:
                for key, schema_item in schema.items():
                    data_item = self.config_data.get(key)
                    validate_item(data_item, schema_item, key)
                
                self.logger.info("配置验证通过")
                
            except ConfigValidationError:
                raise
            except Exception as e:
                self.logger.error(f"配置验证时发生错误: {e}")
                raise ConfigValidationError(f"配置验证失败: {e}")
        
        def create_backup(self):
            """
            创建配置备份
            
            Returns:
                bool: 是否成功
            """
            try:
                if os.path.exists(self.config_file):
                    shutil.copy2(self.config_file, self.backup_file)
                    self.logger.debug(f"配置备份创建成功: {self.backup_file}")
                    return True
                return False
            except Exception as e:
                self.logger.error(f"创建配置备份失败: {e}")
                return False
        
        def restore_backup(self):
            """
            恢复配置备份
            
            Returns:
                bool: 是否成功
            """
            try:
                if os.path.exists(self.backup_file):
                    shutil.move(self.backup_file, self.config_file)
                    self.logger.info(f"配置备份恢复成功: {self.config_file}")
                    return True
                return False
            except Exception as e:
                self.logger.error(f"恢复配置备份失败: {e}")
                return False
    
    # 测试配置管理器
    config_file = "test_config.json"
    
    try:
        # 创建配置管理器
        cm = ConfigManager(config_file)
        
        # 设置一些配置
        cm.set_config("app.name", "测试应用")
        cm.set_config("app.version", "1.0.0")
        cm.set_config("app.debug", True)
        cm.set_config("database.host", "localhost")
        cm.set_config("database.port", 5432)
        cm.set_config("database.name", "testdb")
        cm.set_config("logging.level", "INFO")
        cm.set_config("logging.file", "app.log")
        
        # 保存配置
        cm.save_config()
        print("✓ 配置保存成功")
        
        # 重新加载
        cm.load_config()
        print("✓ 配置加载成功")
        
        # 获取配置
        app_name = cm.get_config("app.name")
        db_host = cm.get_config("database.host")
        unknown_config = cm.get_config("unknown.config", "默认值")
        
        print(f"✓ 应用名称: {app_name}")
        print(f"✓ 数据库主机: {db_host}")
        print(f"✓ 未知配置: {unknown_config}")
        
        # 验证配置
        schema = {
            "app": {
                "required": True,
                "type": dict,
                "children": {
                    "name": {"required": True, "type": str},
                    "version": {"required": True, "type": str}
                }
            },
            "database": {
                "required": True,
                "type": dict,
                "children": {
                    "host": {"required": True, "type": str},
                    "port": {"required": True, "type": int}
                }
            }
        }
        
        cm.validate_config(schema)
        print("✓ 配置验证通过")
        
        # 测试错误情况
        try:
            # 设置无效配置并验证
            cm.set_config("database.port", "invalid_port")
            cm.validate_config(schema)
        except ConfigValidationError as e:
            print(f"✓ 捕获验证错误: {e}")
            # 恢复正确配置
            cm.set_config("database.port", 5432)
        
        print("\n配置管理器测试完成")
        
    except ConfigError as e:
        print(f"✗ 配置错误: {e}")
    except Exception as e:
        print(f"✗ 未知错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理测试文件
        for file in [config_file, f"{config_file}.backup"]:
            try:
                if os.path.exists(file):
                    os.remove(file)
            except:
                pass


def main():
    """主函数 - 运行所有练习答案"""
    print("Session11 练习题答案: 错误处理与调试")
    print("=" * 60)
    
    solutions = [
        solution1_safe_division,
        solution2_file_operations,
        solution3_user_validation,
        solution4_debugging_practice,
        solution5_logging_practice,
        solution6_comprehensive_application
    ]
    
    for i, solution in enumerate(solutions, 1):
        try:
            print(f"\n{'='*20} 练习 {i} 答案 {'='*20}")
            solution()
        except Exception as e:
            print(f"练习 {i} 答案执行失败: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("所有练习答案演示完成！")
    print("\n学习要点总结:")
    print("1. 异常处理要具体化，针对不同异常类型采用不同处理策略")
    print("2. 自定义异常类有助于更好地组织和处理业务逻辑错误")
    print("3. 日志记录是调试和监控应用程序的重要工具")
    print("4. 输入验证和边界条件检查是编写健壮代码的关键")
    print("5. 使用断言来验证程序假设，但不要依赖它们处理用户输入")
    print("6. 资源管理要使用 with 语句或 try-finally 确保清理")


if __name__ == "__main__":
    main()