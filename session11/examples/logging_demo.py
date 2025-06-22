#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session11 示例4: 日志记录演示

本文件演示了Python中日志记录的各种用法，包括：
1. 基础日志配置
2. 不同日志级别
3. 自定义格式化器
4. 多个处理器
5. 日志轮转
6. 结构化日志

作者: Python教程团队
创建日期: 2024-01-15
"""

import logging
import logging.handlers
import os
import sys
import json
import time
from datetime import datetime
from typing import Dict, Any


def demo_basic_logging():
    """演示基础日志记录"""
    print("=== 基础日志记录演示 ===")
    
    # 基本配置
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 获取日志记录器
    logger = logging.getLogger('basic_demo')
    
    # 不同级别的日志
    logger.debug("这是调试信息")
    logger.info("这是一般信息")
    logger.warning("这是警告信息")
    logger.error("这是错误信息")
    logger.critical("这是严重错误信息")
    
    # 带参数的日志
    user_name = "Alice"
    user_age = 25
    logger.info(f"用户登录: {user_name}, 年龄: {user_age}")
    logger.info("用户登录: %s, 年龄: %d", user_name, user_age)
    
    # 异常日志
    try:
        result = 10 / 0
    except Exception as e:
        logger.error("计算错误: %s", e)
        logger.exception("计算过程中发生异常")  # 自动包含异常堆栈


def demo_custom_formatter():
    """演示自定义格式化器"""
    print("\n=== 自定义格式化器演示 ===")
    
    class ColoredFormatter(logging.Formatter):
        """彩色日志格式化器"""
        
        # ANSI颜色代码
        COLORS = {
            'DEBUG': '\033[36m',    # 青色
            'INFO': '\033[32m',     # 绿色
            'WARNING': '\033[33m',  # 黄色
            'ERROR': '\033[31m',    # 红色
            'CRITICAL': '\033[35m', # 紫色
            'RESET': '\033[0m'      # 重置
        }
        
        def format(self, record):
            # 添加颜色
            color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            reset = self.COLORS['RESET']
            
            # 格式化消息
            formatted = super().format(record)
            return f"{color}{formatted}{reset}"
    
    class DetailedFormatter(logging.Formatter):
        """详细信息格式化器"""
        
        def format(self, record):
            # 添加额外信息
            record.filename_line = f"{record.filename}:{record.lineno}"
            record.func_name = record.funcName
            
            # 自定义格式
            format_str = (
                "%(asctime)s | %(levelname)-8s | "
                "%(name)s | %(filename_line)s | "
                "%(func_name)s() | %(message)s"
            )
            
            formatter = logging.Formatter(format_str)
            return formatter.format(record)
    
    # 创建日志记录器
    logger = logging.getLogger('custom_formatter_demo')
    logger.setLevel(logging.DEBUG)
    
    # 清除现有处理器
    logger.handlers.clear()
    
    # 创建控制台处理器（彩色）
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(ColoredFormatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))
    
    # 创建文件处理器（详细信息）
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    file_handler = logging.FileHandler('logs/detailed.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(DetailedFormatter())
    
    # 添加处理器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    # 测试日志
    logger.debug("调试信息 - 只在文件中显示")
    logger.info("一般信息 - 控制台和文件都显示")
    logger.warning("警告信息 - 带颜色显示")
    logger.error("错误信息 - 红色显示")
    logger.critical("严重错误 - 紫色显示")
    
    print("详细日志已保存到 logs/detailed.log")


def demo_multiple_handlers():
    """演示多个处理器"""
    print("\n=== 多个处理器演示 ===")
    
    # 创建日志记录器
    logger = logging.getLogger('multi_handler_demo')
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    
    # 确保日志目录存在
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # 1. 控制台处理器 - 只显示INFO及以上级别
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    # 2. 一般日志文件处理器 - 记录所有级别
    file_handler = logging.FileHandler('logs/application.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    # 3. 错误日志文件处理器 - 只记录ERROR及以上级别
    error_handler = logging.FileHandler('logs/errors.log', encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s\n'
        'File: %(pathname)s, Line: %(lineno)d, Function: %(funcName)s\n'
        'Exception: %(exc_text)s\n' + '-'*50
    )
    error_handler.setFormatter(error_formatter)
    
    # 4. 邮件处理器（模拟）- 严重错误时发送邮件
    class MockSMTPHandler(logging.Handler):
        """模拟SMTP处理器"""
        
        def emit(self, record):
            msg = self.format(record)
            print(f"[模拟邮件] 发送严重错误通知:\n{msg}")
    
    smtp_handler = MockSMTPHandler()
    smtp_handler.setLevel(logging.CRITICAL)
    smtp_formatter = logging.Formatter(
        '严重错误报告\n'
        '时间: %(asctime)s\n'
        '级别: %(levelname)s\n'
        '消息: %(message)s\n'
        '位置: %(pathname)s:%(lineno)d'
    )
    smtp_handler.setFormatter(smtp_formatter)
    
    # 添加所有处理器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    logger.addHandler(smtp_handler)
    
    # 测试不同级别的日志
    logger.debug("调试信息 - 只在application.log中")
    logger.info("一般信息 - 控制台和application.log中")
    logger.warning("警告信息 - 控制台和application.log中")
    logger.error("错误信息 - 控制台、application.log和errors.log中")
    logger.critical("严重错误 - 所有处理器都会处理，包括邮件通知")
    
    print("\n日志文件已创建:")
    print("- logs/application.log (所有日志)")
    print("- logs/errors.log (仅错误日志)")


def demo_rotating_logs():
    """演示日志轮转"""
    print("\n=== 日志轮转演示 ===")
    
    # 确保日志目录存在
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # 1. 按大小轮转的日志
    size_logger = logging.getLogger('size_rotation')
    size_logger.setLevel(logging.INFO)
    size_logger.handlers.clear()
    
    # 创建按大小轮转的处理器（最大1KB，保留3个备份）
    size_handler = logging.handlers.RotatingFileHandler(
        'logs/size_rotation.log',
        maxBytes=1024,  # 1KB
        backupCount=3,
        encoding='utf-8'
    )
    size_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    size_handler.setFormatter(size_formatter)
    size_logger.addHandler(size_handler)
    
    # 2. 按时间轮转的日志
    time_logger = logging.getLogger('time_rotation')
    time_logger.setLevel(logging.INFO)
    time_logger.handlers.clear()
    
    # 创建按时间轮转的处理器（每分钟轮转，保留5个备份）
    time_handler = logging.handlers.TimedRotatingFileHandler(
        'logs/time_rotation.log',
        when='M',  # 按分钟轮转（实际应用中通常用'D'按天轮转）
        interval=1,
        backupCount=5,
        encoding='utf-8'
    )
    time_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    time_handler.setFormatter(time_formatter)
    time_logger.addHandler(time_handler)
    
    # 生成大量日志来测试轮转
    print("生成日志测试轮转...")
    
    for i in range(50):
        size_logger.info(f"这是第 {i+1} 条日志消息，用于测试大小轮转功能。" * 5)
        time_logger.info(f"这是第 {i+1} 条时间轮转日志消息。")
        
        if i % 10 == 0:
            print(f"已生成 {i+1} 条日志")
    
    print("\n日志轮转文件已创建:")
    print("- logs/size_rotation.log (及其备份文件)")
    print("- logs/time_rotation.log (及其备份文件)")
    
    # 显示生成的文件
    log_files = [f for f in os.listdir('logs') if f.startswith(('size_rotation', 'time_rotation'))]
    for file in sorted(log_files):
        file_path = os.path.join('logs', file)
        size = os.path.getsize(file_path)
        print(f"  {file}: {size} bytes")


def demo_structured_logging():
    """演示结构化日志"""
    print("\n=== 结构化日志演示 ===")
    
    class JSONFormatter(logging.Formatter):
        """JSON格式化器"""
        
        def format(self, record):
            log_entry = {
                'timestamp': datetime.fromtimestamp(record.created).isoformat(),
                'level': record.levelname,
                'logger': record.name,
                'message': record.getMessage(),
                'module': record.module,
                'function': record.funcName,
                'line': record.lineno,
                'thread': record.thread,
                'process': record.process
            }
            
            # 添加异常信息
            if record.exc_info:
                log_entry['exception'] = self.formatException(record.exc_info)
            
            # 添加自定义字段
            if hasattr(record, 'user_id'):
                log_entry['user_id'] = record.user_id
            if hasattr(record, 'request_id'):
                log_entry['request_id'] = record.request_id
            if hasattr(record, 'extra_data'):
                log_entry['extra_data'] = record.extra_data
            
            return json.dumps(log_entry, ensure_ascii=False)
    
    # 创建结构化日志记录器
    struct_logger = logging.getLogger('structured')
    struct_logger.setLevel(logging.INFO)
    struct_logger.handlers.clear()
    
    # 确保日志目录存在
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # JSON文件处理器
    json_handler = logging.FileHandler('logs/structured.json', encoding='utf-8')
    json_handler.setFormatter(JSONFormatter())
    struct_logger.addHandler(json_handler)
    
    # 控制台处理器（可读格式）
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    struct_logger.addHandler(console_handler)
    
    # 创建日志适配器来添加上下文信息
    class ContextAdapter(logging.LoggerAdapter):
        """上下文适配器"""
        
        def process(self, msg, kwargs):
            # 添加上下文信息到日志记录
            extra = kwargs.get('extra', {})
            extra.update(self.extra)
            kwargs['extra'] = extra
            return msg, kwargs
    
    # 模拟用户会话
    user_logger = ContextAdapter(struct_logger, {
        'user_id': 'user_123',
        'session_id': 'session_456'
    })
    
    # 记录结构化日志
    user_logger.info("用户登录", extra={
        'action': 'login',
        'ip_address': '192.168.1.100',
        'user_agent': 'Mozilla/5.0...'
    })
    
    user_logger.info("查看商品", extra={
        'action': 'view_product',
        'product_id': 'prod_789',
        'category': 'electronics'
    })
    
    user_logger.warning("登录尝试失败", extra={
        'action': 'login_failed',
        'reason': 'invalid_password',
        'attempt_count': 3
    })
    
    # 记录异常
    try:
        result = 10 / 0
    except Exception as e:
        user_logger.error("计算错误", extra={
            'action': 'calculation',
            'operation': 'division',
            'error_type': type(e).__name__
        }, exc_info=True)
    
    print("结构化日志已保存到 logs/structured.json")
    
    # 读取并显示JSON日志的一部分
    try:
        with open('logs/structured.json', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if lines:
                print("\n最后一条JSON日志记录:")
                last_log = json.loads(lines[-1])
                print(json.dumps(last_log, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"读取JSON日志失败: {e}")


def demo_application_logging():
    """演示应用程序日志记录最佳实践"""
    print("\n=== 应用程序日志记录最佳实践演示 ===")
    
    class ApplicationLogger:
        """应用程序日志管理器"""
        
        def __init__(self, name, log_dir='logs'):
            self.name = name
            self.log_dir = log_dir
            self.logger = self._setup_logger()
        
        def _setup_logger(self):
            """设置日志记录器"""
            # 创建日志目录
            if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir)
            
            # 创建日志记录器
            logger = logging.getLogger(self.name)
            logger.setLevel(logging.DEBUG)
            logger.handlers.clear()
            
            # 控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_format = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_format)
            
            # 应用日志文件处理器（轮转）
            app_handler = logging.handlers.RotatingFileHandler(
                os.path.join(self.log_dir, f'{self.name}.log'),
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
            app_handler.setLevel(logging.DEBUG)
            app_format = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - '
                '%(filename)s:%(lineno)d - %(funcName)s() - %(message)s'
            )
            app_handler.setFormatter(app_format)
            
            # 错误日志文件处理器
            error_handler = logging.handlers.RotatingFileHandler(
                os.path.join(self.log_dir, f'{self.name}_errors.log'),
                maxBytes=5*1024*1024,  # 5MB
                backupCount=3,
                encoding='utf-8'
            )
            error_handler.setLevel(logging.ERROR)
            error_format = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s\n'
                'Location: %(pathname)s:%(lineno)d in %(funcName)s()\n'
                'Exception: %(exc_text)s\n' + '='*80
            )
            error_handler.setFormatter(error_format)
            
            # 添加处理器
            logger.addHandler(console_handler)
            logger.addHandler(app_handler)
            logger.addHandler(error_handler)
            
            return logger
        
        def debug(self, msg, *args, **kwargs):
            self.logger.debug(msg, *args, **kwargs)
        
        def info(self, msg, *args, **kwargs):
            self.logger.info(msg, *args, **kwargs)
        
        def warning(self, msg, *args, **kwargs):
            self.logger.warning(msg, *args, **kwargs)
        
        def error(self, msg, *args, **kwargs):
            self.logger.error(msg, *args, **kwargs)
        
        def critical(self, msg, *args, **kwargs):
            self.logger.critical(msg, *args, **kwargs)
        
        def exception(self, msg, *args, **kwargs):
            self.logger.exception(msg, *args, **kwargs)
    
    # 创建应用程序日志记录器
    app_logger = ApplicationLogger('myapp')
    
    # 模拟应用程序运行
    app_logger.info("应用程序启动")
    
    # 模拟用户操作
    def process_user_request(user_id, action):
        app_logger.info(f"处理用户请求: user_id={user_id}, action={action}")
        
        try:
            if action == "login":
                app_logger.debug(f"验证用户 {user_id} 的登录凭据")
                # 模拟登录逻辑
                time.sleep(0.1)
                app_logger.info(f"用户 {user_id} 登录成功")
                return True
            
            elif action == "purchase":
                app_logger.debug(f"处理用户 {user_id} 的购买请求")
                # 模拟可能的错误
                if user_id == "user_error":
                    raise ValueError("无效的用户ID")
                app_logger.info(f"用户 {user_id} 购买成功")
                return True
            
            elif action == "critical_error":
                app_logger.warning(f"用户 {user_id} 触发了危险操作")
                raise RuntimeError("系统严重错误")
            
            else:
                app_logger.warning(f"未知操作: {action}")
                return False
        
        except Exception as e:
            app_logger.exception(f"处理用户 {user_id} 请求时发生错误: {e}")
            return False
    
    # 模拟各种请求
    requests = [
        ("user_123", "login"),
        ("user_456", "purchase"),
        ("user_error", "purchase"),
        ("user_789", "unknown_action"),
        ("user_critical", "critical_error"),
    ]
    
    for user_id, action in requests:
        result = process_user_request(user_id, action)
        app_logger.debug(f"请求处理结果: {result}")
    
    app_logger.info("应用程序运行完成")
    
    print("\n应用程序日志已保存到:")
    print("- logs/myapp.log (所有日志)")
    print("- logs/myapp_errors.log (错误日志)")


def main():
    """主函数"""
    print("Session11 示例4: 日志记录演示")
    print("=" * 50)
    
    try:
        demo_basic_logging()
        demo_custom_formatter()
        demo_multiple_handlers()
        demo_rotating_logs()
        demo_structured_logging()
        demo_application_logging()
        
    except Exception as e:
        print(f"演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n示例演示完成！")
    print("\n生成的日志文件:")
    if os.path.exists('logs'):
        for file in os.listdir('logs'):
            file_path = os.path.join('logs', file)
            size = os.path.getsize(file_path)
            print(f"  {file}: {size} bytes")
    else:
        print("  没有生成日志文件")


if __name__ == "__main__":
    main()