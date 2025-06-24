#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session20 API开发演示项目 - 启动脚本
图书管理系统API服务启动器

作者: Python学习教程
日期: 2024
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("❌ 错误: 需要Python 3.8或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    print(f"✅ Python版本: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """安装依赖包"""
    print("\n📦 检查并安装依赖包...")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ 找不到requirements.txt文件")
        return False
    
    try:
        # 检查pip是否可用
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        
        # 安装依赖
        print("正在安装依赖包，请稍候...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ 依赖包安装完成")
            return True
        else:
            print(f"❌ 依赖包安装失败: {result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 安装依赖时出错: {e}")
        return False
    except FileNotFoundError:
        print("❌ 找不到pip，请确保Python环境正确安装")
        return False

def check_database():
    """检查数据库文件"""
    print("\n🗄️ 检查数据库...")
    
    db_file = Path(__file__).parent / "bookstore.db"
    
    if db_file.exists():
        print(f"✅ 数据库文件已存在: {db_file}")
        return True
    else:
        print("📝 数据库文件不存在，将在首次启动时创建")
        return True

def start_server(host="0.0.0.0", port=5000, debug=True):
    """启动Flask服务器"""
    print(f"\n🚀 启动API服务器...")
    print(f"地址: http://{host}:{port}")
    print(f"调试模式: {'开启' if debug else '关闭'}")
    print("\n按 Ctrl+C 停止服务器")
    print("="*50)
    
    try:
        # 导入并运行应用
        from app import app, init_db
        
        # 初始化数据库
        init_db()
        
        # 启动服务器
        app.run(
            host=host,
            port=port,
            debug=debug,
            use_reloader=debug
        )
        
    except ImportError as e:
        print(f"❌ 导入应用失败: {e}")
        print("请确保app.py文件存在且无语法错误")
        return False
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ 端口 {port} 已被占用")
            print("请尝试使用其他端口或停止占用该端口的程序")
        else:
            print(f"❌ 启动服务器失败: {e}")
        return False
    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止")
        return True
    except Exception as e:
        print(f"❌ 启动服务器时发生错误: {e}")
        return False

def show_usage_info():
    """显示使用说明"""
    print("\n" + "="*60)
    print("📚 图书管理API服务使用说明")
    print("="*60)
    print("\n🔗 API端点:")
    print("  • GET    /api/books           - 获取图书列表")
    print("  • POST   /api/books           - 创建新图书 (需要认证)")
    print("  • GET    /api/books/{id}      - 获取图书详情")
    print("  • PUT    /api/books/{id}      - 更新图书信息 (需要认证)")
    print("  • DELETE /api/books/{id}      - 删除图书 (需要认证)")
    print("  • POST   /api/auth/register   - 用户注册")
    print("  • POST   /api/auth/login      - 用户登录")
    
    print("\n👤 默认管理员账号:")
    print("  • 用户名: admin")
    print("  • 密码: admin123")
    
    print("\n🧪 测试API:")
    print("  • 运行测试: python test_api.py")
    print("  • 指定地址: python test_api.py --url http://localhost:5000")
    
    print("\n📖 示例请求:")
    print("  # 获取图书列表")
    print("  curl http://localhost:5000/api/books")
    print("  ")
    print("  # 用户登录")
    print("  curl -X POST http://localhost:5000/api/auth/login \\")
    print("       -H 'Content-Type: application/json' \\")
    print("       -d '{\"username\": \"admin\", \"password\": \"admin123\"}'")
    
    print("\n" + "="*60)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='图书管理API服务启动器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python run.py                    # 使用默认设置启动
  python run.py --port 8000        # 指定端口
  python run.py --host 127.0.0.1   # 指定主机
  python run.py --no-debug         # 关闭调试模式
  python run.py --install-only     # 仅安装依赖
  python run.py --info             # 显示使用说明
        """
    )
    
    parser.add_argument('--host', default='0.0.0.0', 
                       help='服务器主机地址 (默认: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5000, 
                       help='服务器端口 (默认: 5000)')
    parser.add_argument('--no-debug', action='store_true', 
                       help='关闭调试模式')
    parser.add_argument('--install-only', action='store_true', 
                       help='仅安装依赖包，不启动服务器')
    parser.add_argument('--skip-install', action='store_true', 
                       help='跳过依赖包安装')
    parser.add_argument('--info', action='store_true', 
                       help='显示API使用说明')
    
    args = parser.parse_args()
    
    # 显示使用说明
    if args.info:
        show_usage_info()
        return
    
    print("🎯 Session20 API开发演示项目")
    print("📚 图书管理系统API服务")
    print("="*40)
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 安装依赖
    if not args.skip_install:
        if not install_dependencies():
            print("\n💡 提示: 如果依赖安装失败，可以手动运行:")
            print("pip install -r requirements.txt")
            if not args.install_only:
                response = input("\n是否继续启动服务器? (y/N): ")
                if response.lower() != 'y':
                    sys.exit(1)
    
    # 仅安装依赖
    if args.install_only:
        print("\n✅ 依赖安装完成，使用以下命令启动服务器:")
        print("python run.py")
        return
    
    # 检查数据库
    check_database()
    
    # 显示使用说明
    show_usage_info()
    
    # 启动服务器
    debug_mode = not args.no_debug
    success = start_server(args.host, args.port, debug_mode)
    
    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main()