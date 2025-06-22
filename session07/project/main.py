#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件管理器主程序

这是文件管理器应用的主入口文件，支持GUI和CLI两种运行模式。

使用方法：
    python main.py              # 启动GUI模式
    python main.py --cli        # 启动CLI模式
    python main.py --help       # 显示帮助信息

作者: Python教程团队
创建日期: 2024-12-22
"""

import sys
import os
import argparse
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 导入配置
from config import (
    APP_NAME, APP_VERSION, APP_DESCRIPTION,
    LOGGING_CONFIG, DEFAULT_SETTINGS
)

# 设置日志
try:
    from loguru import logger
    
    # 配置日志
    logger.remove()  # 移除默认处理器
    logger.add(
        sys.stderr,
        level=LOGGING_CONFIG['level'],
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    
    # 添加文件日志
    from config import LOG_FILE
    logger.add(
        LOG_FILE,
        level=LOGGING_CONFIG['level'],
        format=LOGGING_CONFIG['format'],
        rotation=LOGGING_CONFIG['rotation'],
        retention=LOGGING_CONFIG['retention'],
        compression=LOGGING_CONFIG['compression']
    )
except ImportError:
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)


def check_dependencies():
    """
    检查必要的依赖是否已安装
    
    Returns:
        tuple: (是否满足依赖, 缺失的依赖列表)
    """
    required_packages = {
        'tkinter': 'GUI界面支持',
        'pathlib': '路径处理（Python 3.4+内置）'
    }
    
    optional_packages = {
        'send2trash': '安全删除文件',
        'watchdog': '文件系统监控',
        'Pillow': '图像预览',
        'click': '命令行界面增强',
        'colorama': '彩色终端输出',
        'rich': '富文本终端显示'
    }
    
    missing_required = []
    missing_optional = []
    
    # 检查必需依赖
    for package, description in required_packages.items():
        try:
            if package == 'tkinter':
                import tkinter
            elif package == 'pathlib':
                from pathlib import Path
        except ImportError:
            missing_required.append((package, description))
    
    # 检查可选依赖
    for package, description in optional_packages.items():
        try:
            __import__(package)
        except ImportError:
            missing_optional.append((package, description))
    
    return len(missing_required) == 0, missing_required, missing_optional


def print_dependency_info(missing_required, missing_optional):
    """
    打印依赖信息
    """
    if missing_required:
        print("❌ 缺少必需依赖:")
        for package, description in missing_required:
            print(f"   - {package}: {description}")
        print("\n请安装缺少的依赖后重试。")
        print("安装命令: pip install tkinter")
        return False
    
    if missing_optional:
        print("⚠️  缺少可选依赖（功能可能受限）:")
        for package, description in missing_optional:
            print(f"   - {package}: {description}")
        print("\n建议安装: pip install -r requirements.txt")
        print()
    
    return True


def run_gui_mode():
    """
    运行GUI模式
    """
    try:
        logger.info("启动GUI模式")
        
        # 检查tkinter是否可用
        try:
            import tkinter as tk
            from tkinter import messagebox
        except ImportError:
            print("❌ 无法导入tkinter，GUI模式不可用")
            print("请确保Python安装包含tkinter支持")
            return 1
        
        # 导入GUI模块
        try:
            from gui.main_window import FileManagerApp
        except ImportError as e:
            logger.error(f"无法导入GUI模块: {e}")
            print("❌ GUI模块导入失败，请检查项目文件完整性")
            return 1
        
        # 创建并运行应用
        try:
            app = FileManagerApp()
            app.run()
            logger.info("GUI应用正常退出")
            return 0
        except Exception as e:
            logger.error(f"GUI应用运行错误: {e}")
            print(f"❌ 应用运行错误: {e}")
            return 1
            
    except KeyboardInterrupt:
        logger.info("用户中断GUI应用")
        print("\n👋 应用已退出")
        return 0
    except Exception as e:
        logger.error(f"GUI模式未知错误: {e}")
        print(f"❌ 未知错误: {e}")
        return 1


def run_cli_mode(args):
    """
    运行CLI模式
    
    Args:
        args: 命令行参数
    """
    try:
        logger.info("启动CLI模式")
        
        # 导入CLI模块
        try:
            from cli.interface import FileManagerCLI
        except ImportError as e:
            logger.error(f"无法导入CLI模块: {e}")
            print("❌ CLI模块导入失败，请检查项目文件完整性")
            return 1
        
        # 创建并运行CLI
        try:
            cli = FileManagerCLI()
            return cli.run(args)
        except Exception as e:
            logger.error(f"CLI应用运行错误: {e}")
            print(f"❌ CLI运行错误: {e}")
            return 1
            
    except KeyboardInterrupt:
        logger.info("用户中断CLI应用")
        print("\n👋 CLI已退出")
        return 0
    except Exception as e:
        logger.error(f"CLI模式未知错误: {e}")
        print(f"❌ 未知错误: {e}")
        return 1


def create_argument_parser():
    """
    创建命令行参数解析器
    
    Returns:
        ArgumentParser: 配置好的参数解析器
    """
    parser = argparse.ArgumentParser(
        prog=APP_NAME,
        description=APP_DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s                    # 启动GUI模式
  %(prog)s --cli              # 启动CLI模式
  %(prog)s --cli ls /path     # CLI模式列出目录
  %(prog)s --version          # 显示版本信息
  %(prog)s --check-deps       # 检查依赖

更多信息请访问: https://github.com/python-rookie/file-manager
        """
    )
    
    # 基本选项
    parser.add_argument(
        '--version',
        action='version',
        version=f'{APP_NAME} {APP_VERSION}'
    )
    
    parser.add_argument(
        '--cli',
        action='store_true',
        help='启动命令行界面模式'
    )
    
    parser.add_argument(
        '--check-deps',
        action='store_true',
        help='检查依赖包安装情况'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='启用调试模式'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='指定配置文件路径'
    )
    
    # CLI特定选项
    cli_group = parser.add_argument_group('CLI模式选项')
    
    cli_group.add_argument(
        'command',
        nargs='?',
        help='CLI命令 (ls, search, copy, move, delete, analyze等)'
    )
    
    cli_group.add_argument(
        'args',
        nargs='*',
        help='命令参数'
    )
    
    cli_group.add_argument(
        '--no-color',
        action='store_true',
        help='禁用彩色输出'
    )
    
    cli_group.add_argument(
        '--verbose', '-v',
        action='count',
        default=0,
        help='详细输出 (可重复使用增加详细程度)'
    )
    
    return parser


def print_banner():
    """
    打印应用横幅
    """
    banner = f"""
╔══════════════════════════════════════════════════════════════╗
║                    {APP_NAME:<30}                    ║
║                         版本 {APP_VERSION:<10}                         ║
║                                                              ║
║  一个功能强大的Python文件管理器，支持GUI和CLI两种模式        ║
║                                                              ║
║  作者: {APP_AUTHOR:<20}                                ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """
    主函数
    """
    # 解析命令行参数
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # 设置调试模式
    if args.debug:
        logger.remove()
        logger.add(sys.stderr, level="DEBUG")
        logger.debug("调试模式已启用")
    
    # 检查依赖
    deps_ok, missing_required, missing_optional = check_dependencies()
    
    if args.check_deps:
        print_banner()
        print("\n🔍 检查依赖包...")
        if print_dependency_info(missing_required, missing_optional):
            print("✅ 依赖检查完成")
        return 0 if deps_ok else 1
    
    # 如果缺少必需依赖，显示错误并退出
    if not deps_ok:
        print_dependency_info(missing_required, missing_optional)
        return 1
    
    # 显示可选依赖警告（如果有）
    if missing_optional and not args.cli:
        print_dependency_info([], missing_optional)
    
    try:
        # 根据参数选择运行模式
        if args.cli:
            # CLI模式
            return run_cli_mode(args)
        else:
            # GUI模式（默认）
            if not missing_optional:
                print_banner()
                print("\n🚀 启动GUI模式...")
            return run_gui_mode()
            
    except Exception as e:
        logger.error(f"应用启动失败: {e}")
        print(f"❌ 应用启动失败: {e}")
        return 1


if __name__ == "__main__":
    # 设置退出码
    exit_code = main()
    sys.exit(exit_code)