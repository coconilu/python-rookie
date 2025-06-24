#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session25 项目示例：Flask Web应用

这是一个简单的Flask应用，用于演示部署与运维的各个方面。
应用包含以下功能：
1. 基本的Web页面
2. API接口
3. 健康检查端点
4. 静态文件服务
5. 错误处理
6. 日志记录
7. 配置管理
"""

import os
import sys
import logging
from datetime import datetime
from flask import Flask, render_template, jsonify, request, send_from_directory
from werkzeug.exceptions import NotFound, InternalServerError
import psutil


def create_app(config_name=None):
    """
    应用工厂函数
    
    Args:
        config_name: 配置名称 ('development', 'production', 'testing')
    
    Returns:
        Flask: Flask应用实例
    """
    app = Flask(__name__)
    
    # 配置应用
    configure_app(app, config_name)
    
    # 配置日志
    configure_logging(app)
    
    # 注册蓝图和路由
    register_routes(app)
    
    # 注册错误处理器
    register_error_handlers(app)
    
    return app


def configure_app(app, config_name=None):
    """
    配置Flask应用
    
    Args:
        app: Flask应用实例
        config_name: 配置名称
    """
    # 默认配置
    app.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production'),
        DEBUG=False,
        TESTING=False,
        LOG_LEVEL='INFO',
        LOG_FILE='app.log'
    )
    
    # 根据环境设置配置
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    
    if config_name == 'development':
        app.config.update(
            DEBUG=True,
            LOG_LEVEL='DEBUG'
        )
    elif config_name == 'testing':
        app.config.update(
            TESTING=True,
            LOG_LEVEL='WARNING'
        )
    elif config_name == 'production':
        app.config.update(
            DEBUG=False,
            LOG_LEVEL='INFO'
        )
        # 生产环境必须设置SECRET_KEY
        if app.config['SECRET_KEY'] == 'dev-secret-key-change-in-production':
            raise ValueError("生产环境必须设置SECRET_KEY环境变量")


def configure_logging(app):
    """
    配置日志记录
    
    Args:
        app: Flask应用实例
    """
    # 创建logs目录
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 设置日志级别
    log_level = getattr(logging, app.config['LOG_LEVEL'].upper())
    
    # 配置日志格式
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(name)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    )
    
    # 文件处理器
    file_handler = logging.FileHandler(
        os.path.join(log_dir, app.config['LOG_FILE'])
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # 配置应用日志
    app.logger.setLevel(log_level)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    
    # 配置Werkzeug日志
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(log_level)
    werkzeug_logger.addHandler(file_handler)


def register_routes(app):
    """
    注册路由
    
    Args:
        app: Flask应用实例
    """
    
    @app.route('/')
    def index():
        """首页"""
        app.logger.info('访问首页')
        return render_template('index.html')
    
    @app.route('/about')
    def about():
        """关于页面"""
        app.logger.info('访问关于页面')
        return render_template('about.html')
    
    @app.route('/api/status')
    def api_status():
        """API状态接口"""
        return jsonify({
            'status': 'ok',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        })
    
    @app.route('/api/info')
    def api_info():
        """系统信息接口"""
        try:
            # 获取系统信息
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return jsonify({
                'system': {
                    'cpu_percent': cpu_percent,
                    'memory': {
                        'total': memory.total,
                        'available': memory.available,
                        'percent': memory.percent
                    },
                    'disk': {
                        'total': disk.total,
                        'free': disk.free,
                        'percent': (disk.used / disk.total) * 100
                    }
                },
                'app': {
                    'debug': app.debug,
                    'testing': app.testing,
                    'config': dict(app.config)
                }
            })
        except Exception as e:
            app.logger.error(f'获取系统信息失败: {e}')
            return jsonify({'error': '获取系统信息失败'}), 500
    
    @app.route('/health')
    def health_check():
        """健康检查端点"""
        try:
            # 执行健康检查
            checks = {
                'database': check_database(),
                'disk_space': check_disk_space(),
                'memory': check_memory()
            }
            
            # 判断整体健康状态
            overall_status = 'healthy' if all(checks.values()) else 'unhealthy'
            status_code = 200 if overall_status == 'healthy' else 503
            
            return jsonify({
                'status': overall_status,
                'timestamp': datetime.now().isoformat(),
                'checks': checks
            }), status_code
        
        except Exception as e:
            app.logger.error(f'健康检查失败: {e}')
            return jsonify({
                'status': 'unhealthy',
                'error': str(e)
            }), 503
    
    @app.route('/api/echo', methods=['GET', 'POST'])
    def api_echo():
        """回显接口"""
        if request.method == 'GET':
            return jsonify({
                'method': 'GET',
                'args': dict(request.args),
                'headers': dict(request.headers)
            })
        else:
            return jsonify({
                'method': 'POST',
                'json': request.get_json(),
                'form': dict(request.form),
                'headers': dict(request.headers)
            })
    
    @app.route('/static/<path:filename>')
    def static_files(filename):
        """静态文件服务"""
        return send_from_directory('static', filename)


def register_error_handlers(app):
    """
    注册错误处理器
    
    Args:
        app: Flask应用实例
    """
    
    @app.errorhandler(404)
    def not_found_error(error):
        """404错误处理"""
        app.logger.warning(f'404错误: {request.url}')
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Not Found'}), 404
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """500错误处理"""
        app.logger.error(f'500错误: {error}')
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Internal Server Error'}), 500
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        """通用异常处理"""
        app.logger.error(f'未处理的异常: {e}', exc_info=True)
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Internal Server Error'}), 500
        return render_template('errors/500.html'), 500


def check_database():
    """
    检查数据库连接
    
    Returns:
        bool: 数据库是否正常
    """
    # 这里应该实现实际的数据库连接检查
    # 为了演示，我们总是返回True
    return True


def check_disk_space():
    """
    检查磁盘空间
    
    Returns:
        bool: 磁盘空间是否充足
    """
    try:
        disk = psutil.disk_usage('/')
        free_percent = (disk.free / disk.total) * 100
        return free_percent > 10  # 至少10%的空闲空间
    except:
        return False


def check_memory():
    """
    检查内存使用情况
    
    Returns:
        bool: 内存使用是否正常
    """
    try:
        memory = psutil.virtual_memory()
        return memory.percent < 90  # 内存使用率低于90%
    except:
        return False


# 创建应用实例
app = create_app()


if __name__ == '__main__':
    # 开发服务器
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    
    app.logger.info(f'启动开发服务器: http://{host}:{port}')
    app.run(host=host, port=port, debug=app.config['DEBUG'])