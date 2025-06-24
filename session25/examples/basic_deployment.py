#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session25 示例1：基础部署配置

这个示例展示了如何为Python应用创建基础的部署配置。

学习目标：
1. 理解虚拟环境的重要性
2. 学会生成requirements.txt
3. 掌握基础的部署配置
4. 了解环境变量的使用
"""

import os
import sys
import subprocess
import venv
from pathlib import Path


class BasicDeployment:
    """基础部署配置管理器"""
    
    def __init__(self, project_path="."):
        self.project_path = Path(project_path).resolve()
        self.venv_path = self.project_path / "venv"
        
    def create_virtual_environment(self):
        """创建虚拟环境"""
        print(f"📦 在 {self.project_path} 创建虚拟环境...")
        
        if self.venv_path.exists():
            print("⚠️  虚拟环境已存在")
            return True
            
        try:
            venv.create(self.venv_path, with_pip=True)
            print("✅ 虚拟环境创建成功")
            return True
        except Exception as e:
            print(f"❌ 创建虚拟环境失败: {e}")
            return False
    
    def get_activation_command(self):
        """获取虚拟环境激活命令"""
        if sys.platform == "win32":
            return str(self.venv_path / "Scripts" / "activate.bat")
        else:
            return f"source {self.venv_path / 'bin' / 'activate'}"
    
    def install_packages(self, packages):
        """在虚拟环境中安装包"""
        if sys.platform == "win32":
            pip_path = self.venv_path / "Scripts" / "pip.exe"
        else:
            pip_path = self.venv_path / "bin" / "pip"
            
        if not pip_path.exists():
            print("❌ 虚拟环境中找不到pip")
            return False
            
        print(f"📦 安装包: {', '.join(packages)}")
        
        for package in packages:
            try:
                result = subprocess.run(
                    [str(pip_path), "install", package],
                    capture_output=True,
                    text=True,
                    check=True
                )
                print(f"✅ {package} 安装成功")
            except subprocess.CalledProcessError as e:
                print(f"❌ {package} 安装失败: {e.stderr}")
                return False
                
        return True
    
    def generate_requirements(self):
        """生成requirements.txt文件"""
        if sys.platform == "win32":
            pip_path = self.venv_path / "Scripts" / "pip.exe"
        else:
            pip_path = self.venv_path / "bin" / "pip"
            
        try:
            result = subprocess.run(
                [str(pip_path), "freeze"],
                capture_output=True,
                text=True,
                check=True
            )
            
            requirements_file = self.project_path / "requirements.txt"
            with open(requirements_file, "w", encoding="utf-8") as f:
                f.write(result.stdout)
                
            print(f"✅ requirements.txt 已生成: {requirements_file}")
            print("📋 已安装的包:")
            for line in result.stdout.strip().split("\n"):
                if line.strip():
                    print(f"   {line}")
                    
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ 生成requirements.txt失败: {e.stderr}")
            return False
    
    def create_env_file(self):
        """创建环境变量配置文件"""
        env_content = """# 环境配置文件
# 复制此文件为 .env 并根据实际情况修改

# Flask配置
FLASK_ENV=development
FLASK_APP=app.py
FLASK_DEBUG=True

# 应用配置
SECRET_KEY=your-secret-key-here
HOST=127.0.0.1
PORT=5000

# 数据库配置
# DATABASE_URL=sqlite:///app.db
# DATABASE_URL=postgresql://user:password@localhost/dbname
# DATABASE_URL=mysql://user:password@localhost/dbname

# Redis配置
# REDIS_URL=redis://localhost:6379/0

# 邮件配置
# MAIL_SERVER=smtp.gmail.com
# MAIL_PORT=587
# MAIL_USE_TLS=True
# MAIL_USERNAME=your-email@gmail.com
# MAIL_PASSWORD=your-app-password

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# 安全配置
# JWT_SECRET_KEY=your-jwt-secret
# SESSION_COOKIE_SECURE=True
# SESSION_COOKIE_HTTPONLY=True
"""
        
        env_file = self.project_path / ".env.example"
        with open(env_file, "w", encoding="utf-8") as f:
            f.write(env_content)
            
        print(f"✅ 环境配置示例文件已创建: {env_file}")
        print("💡 请复制为 .env 文件并根据实际情况修改")
    
    def create_gitignore(self):
        """创建.gitignore文件"""
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
PIPFILE.lock

# Virtual Environment
venv/
env/
ENV/

# Environment Variables
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
logs/
*.log

# Database
*.db
*.sqlite
*.sqlite3

# OS
.DS_Store
Thumbs.db

# Flask
instance/
.webassets-cache

# Coverage
.coverage
htmlcov/
.pytest_cache/

# Docker
.dockerignore

# Temporary files
*.tmp
*.temp
"""
        
        gitignore_file = self.project_path / ".gitignore"
        with open(gitignore_file, "w", encoding="utf-8") as f:
            f.write(gitignore_content)
            
        print(f"✅ .gitignore文件已创建: {gitignore_file}")
    
    def create_simple_app(self):
        """创建一个简单的Flask应用示例"""
        app_content = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')

@app.route('/')
def index():
    return '''
    <h1>Hello, Deployment!</h1>
    <p>这是一个简单的Flask应用部署示例。</p>
    <p>当前时间: <span id="time"></span></p>
    <p><a href="/api/status">查看API状态</a></p>
    
    <script>
        function updateTime() {
            document.getElementById('time').textContent = new Date().toLocaleString();
        }
        updateTime();
        setInterval(updateTime, 1000);
    </script>
    '''

@app.route('/api/status')
def api_status():
    return jsonify({
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'environment': os.environ.get('FLASK_ENV', 'development')
    })

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)
"""
        
        app_file = self.project_path / "app.py"
        with open(app_file, "w", encoding="utf-8") as f:
            f.write(app_content)
            
        print(f"✅ 简单Flask应用已创建: {app_file}")
    
    def setup_project(self):
        """完整的项目设置"""
        print("🚀 开始设置Python项目部署环境...\n")
        
        # 1. 创建虚拟环境
        if not self.create_virtual_environment():
            return False
            
        # 2. 安装基础包
        packages = ["flask", "python-dotenv"]
        if not self.install_packages(packages):
            return False
            
        # 3. 生成requirements.txt
        if not self.generate_requirements():
            return False
            
        # 4. 创建配置文件
        self.create_env_file()
        self.create_gitignore()
        self.create_simple_app()
        
        print("\n🎉 项目设置完成！")
        print("\n📋 下一步操作:")
        print(f"1. 激活虚拟环境: {self.get_activation_command()}")
        print("2. 复制 .env.example 为 .env 并配置")
        print("3. 运行应用: python app.py")
        print("4. 访问: http://127.0.0.1:5000")
        
        return True


def main():
    """主函数"""
    print("=" * 60)
    print("Session25 示例1：基础部署配置")
    print("=" * 60)
    
    # 获取项目路径
    project_path = input("请输入项目路径 (回车使用当前目录): ").strip()
    if not project_path:
        project_path = "."
        
    # 创建部署管理器
    deployment = BasicDeployment(project_path)
    
    # 设置项目
    success = deployment.setup_project()
    
    if success:
        print("\n✅ 基础部署配置完成！")
    else:
        print("\n❌ 部署配置失败，请检查错误信息")


if __name__ == "__main__":
    main()