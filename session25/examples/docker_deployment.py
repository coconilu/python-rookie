#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session25 示例2：Docker容器化部署

这个示例展示了如何使用Docker进行Python应用的容器化部署。

学习目标：
1. 理解Docker容器化的概念
2. 学会编写Dockerfile
3. 掌握Docker Compose的使用
4. 了解容器化部署的最佳实践
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime


class DockerDeployment:
    """Docker部署管理器"""
    
    def __init__(self, project_path="."):
        self.project_path = Path(project_path).resolve()
        self.image_name = "flask-app"
        self.container_name = "flask-container"
        
    def check_docker(self):
        """检查Docker是否安装"""
        try:
            result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"✅ Docker已安装: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Docker未安装或不在PATH中")
            print("💡 请访问 https://docs.docker.com/get-docker/ 安装Docker")
            return False
    
    def check_docker_compose(self):
        """检查Docker Compose是否可用"""
        try:
            # 尝试新版本的docker compose命令
            result = subprocess.run(
                ["docker", "compose", "version"],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"✅ Docker Compose已安装: {result.stdout.strip()}")
            return "docker compose"
        except subprocess.CalledProcessError:
            try:
                # 尝试旧版本的docker-compose命令
                result = subprocess.run(
                    ["docker-compose", "--version"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                print(f"✅ Docker Compose已安装: {result.stdout.strip()}")
                return "docker-compose"
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("❌ Docker Compose未安装")
                return None
    
    def create_dockerfile(self):
        """创建Dockerfile"""
        dockerfile_content = """# 使用官方Python镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements.txt并安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建非root用户
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE 5000

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# 启动命令
CMD ["python", "app.py"]
"""
        
        dockerfile_path = self.project_path / "Dockerfile"
        with open(dockerfile_path, "w", encoding="utf-8") as f:
            f.write(dockerfile_content)
            
        print(f"✅ Dockerfile已创建: {dockerfile_path}")
        return dockerfile_path
    
    def create_dockerignore(self):
        """创建.dockerignore文件"""
        dockerignore_content = """# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
.pytest_cache/
.coverage

# Virtual Environment
venv/
env/

# IDE
.vscode/
.idea/

# Git
.git/
.gitignore

# Documentation
*.md
README*

# Logs
logs/
*.log

# Environment
.env
.env.*

# OS
.DS_Store
Thumbs.db

# Docker
Dockerfile*
docker-compose*
.dockerignore

# Build artifacts
build/
dist/
*.egg-info/
"""
        
        dockerignore_path = self.project_path / ".dockerignore"
        with open(dockerignore_path, "w", encoding="utf-8") as f:
            f.write(dockerignore_content)
            
        print(f"✅ .dockerignore已创建: {dockerignore_path}")
        return dockerignore_path
    
    def create_docker_compose(self):
        """创建docker-compose.yml文件"""
        compose_content = """version: '3.8'

services:
  web:
    build: .
    image: flask-app:latest
    container_name: flask-container
    restart: unless-stopped
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY:-default-secret-key}
    volumes:
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
    networks:
      - app-network

  # 可选：添加数据库服务
  # db:
  #   image: postgres:13
  #   container_name: postgres-db
  #   restart: unless-stopped
  #   environment:
  #     POSTGRES_DB: ${DB_NAME:-myapp}
  #     POSTGRES_USER: ${DB_USER:-postgres}
  #     POSTGRES_PASSWORD: ${DB_PASSWORD:-password}
  #   volumes:
  #     - postgres_data:/var/lib/postgresql/data
  #   networks:
  #     - app-network

  # 可选：添加Redis服务
  # redis:
  #   image: redis:6-alpine
  #   container_name: redis-cache
  #   restart: unless-stopped
  #   volumes:
  #     - redis_data:/data
  #   networks:
  #     - app-network

networks:
  app-network:
    driver: bridge

# volumes:
#   postgres_data:
#   redis_data:
"""
        
        compose_path = self.project_path / "docker-compose.yml"
        with open(compose_path, "w", encoding="utf-8") as f:
            f.write(compose_content)
            
        print(f"✅ docker-compose.yml已创建: {compose_path}")
        return compose_path
    
    def build_image(self):
        """构建Docker镜像"""
        print(f"🔨 构建Docker镜像: {self.image_name}...")
        
        try:
            result = subprocess.run(
                ["docker", "build", "-t", self.image_name, "."],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True
            )
            print("✅ Docker镜像构建成功")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Docker镜像构建失败: {e.stderr}")
            return False
    
    def run_container(self, port=5000):
        """运行Docker容器"""
        print(f"🚀 启动Docker容器: {self.container_name}...")
        
        # 先停止并删除已存在的容器
        self.stop_container()
        
        try:
            result = subprocess.run([
                "docker", "run", "-d",
                "--name", self.container_name,
                "-p", f"{port}:5000",
                "-e", "FLASK_ENV=production",
                self.image_name
            ], capture_output=True, text=True, check=True)
            
            container_id = result.stdout.strip()
            print(f"✅ 容器启动成功: {container_id[:12]}")
            print(f"🌐 应用访问地址: http://localhost:{port}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ 容器启动失败: {e.stderr}")
            return False
    
    def stop_container(self):
        """停止并删除容器"""
        try:
            # 停止容器
            subprocess.run(
                ["docker", "stop", self.container_name],
                capture_output=True,
                check=True
            )
            print(f"🛑 容器已停止: {self.container_name}")
        except subprocess.CalledProcessError:
            pass  # 容器可能不存在
            
        try:
            # 删除容器
            subprocess.run(
                ["docker", "rm", self.container_name],
                capture_output=True,
                check=True
            )
            print(f"🗑️  容器已删除: {self.container_name}")
        except subprocess.CalledProcessError:
            pass  # 容器可能不存在
    
    def show_container_logs(self):
        """显示容器日志"""
        try:
            result = subprocess.run(
                ["docker", "logs", self.container_name],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"📋 容器日志 ({self.container_name}):")
            print("-" * 50)
            print(result.stdout)
            if result.stderr:
                print("错误日志:")
                print(result.stderr)
        except subprocess.CalledProcessError as e:
            print(f"❌ 获取日志失败: {e.stderr}")
    
    def show_container_status(self):
        """显示容器状态"""
        try:
            result = subprocess.run(
                ["docker", "ps", "-a", "--filter", f"name={self.container_name}", "--format", "table {{.Names}}\t{{.Status}}\t{{.Ports}}"],
                capture_output=True,
                text=True,
                check=True
            )
            print("📊 容器状态:")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"❌ 获取状态失败: {e.stderr}")
    
    def docker_compose_up(self, compose_command="docker compose"):
        """使用Docker Compose启动服务"""
        print("🚀 使用Docker Compose启动服务...")
        
        try:
            cmd = compose_command.split() + ["up", "-d", "--build"]
            result = subprocess.run(
                cmd,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True
            )
            print("✅ Docker Compose服务启动成功")
            print("🌐 应用访问地址: http://localhost:5000")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Docker Compose启动失败: {e.stderr}")
            return False
    
    def docker_compose_down(self, compose_command="docker compose"):
        """使用Docker Compose停止服务"""
        print("🛑 停止Docker Compose服务...")
        
        try:
            cmd = compose_command.split() + ["down"]
            result = subprocess.run(
                cmd,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True
            )
            print("✅ Docker Compose服务已停止")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 停止服务失败: {e.stderr}")
            return False
    
    def setup_docker_deployment(self):
        """完整的Docker部署设置"""
        print("🐳 开始设置Docker容器化部署...\n")
        
        # 1. 检查Docker环境
        if not self.check_docker():
            return False
            
        compose_command = self.check_docker_compose()
        
        # 2. 创建Docker相关文件
        self.create_dockerfile()
        self.create_dockerignore()
        self.create_docker_compose()
        
        print("\n🎉 Docker部署文件创建完成！")
        print("\n📋 可用的部署方式:")
        print("\n方式1 - 直接使用Docker:")
        print("  1. docker build -t flask-app .")
        print("  2. docker run -d -p 5000:5000 --name flask-container flask-app")
        print("  3. 访问: http://localhost:5000")
        
        if compose_command:
            print("\n方式2 - 使用Docker Compose (推荐):")
            print(f"  1. {compose_command} up -d --build")
            print("  2. 访问: http://localhost:5000")
            print(f"  3. 停止: {compose_command} down")
        
        print("\n🔧 管理命令:")
        print("  - 查看日志: docker logs flask-container")
        print("  - 查看状态: docker ps")
        print("  - 进入容器: docker exec -it flask-container /bin/bash")
        print("  - 停止容器: docker stop flask-container")
        print("  - 删除容器: docker rm flask-container")
        
        return True


def interactive_demo():
    """交互式演示"""
    print("=" * 60)
    print("Session25 示例2：Docker容器化部署")
    print("=" * 60)
    
    # 获取项目路径
    project_path = input("请输入项目路径 (回车使用当前目录): ").strip()
    if not project_path:
        project_path = "."
        
    deployment = DockerDeployment(project_path)
    
    while True:
        print("\n" + "=" * 40)
        print("请选择操作:")
        print("1. 设置Docker部署文件")
        print("2. 构建Docker镜像")
        print("3. 运行容器")
        print("4. 停止容器")
        print("5. 查看容器状态")
        print("6. 查看容器日志")
        print("7. Docker Compose启动")
        print("8. Docker Compose停止")
        print("0. 退出")
        
        choice = input("\n请输入选择 (0-8): ").strip()
        
        if choice == "1":
            deployment.setup_docker_deployment()
        elif choice == "2":
            deployment.build_image()
        elif choice == "3":
            port = input("请输入端口 (默认5000): ").strip()
            port = int(port) if port.isdigit() else 5000
            deployment.run_container(port)
        elif choice == "4":
            deployment.stop_container()
        elif choice == "5":
            deployment.show_container_status()
        elif choice == "6":
            deployment.show_container_logs()
        elif choice == "7":
            compose_cmd = deployment.check_docker_compose()
            if compose_cmd:
                deployment.docker_compose_up(compose_cmd)
            else:
                print("❌ Docker Compose不可用")
        elif choice == "8":
            compose_cmd = deployment.check_docker_compose()
            if compose_cmd:
                deployment.docker_compose_down(compose_cmd)
            else:
                print("❌ Docker Compose不可用")
        elif choice == "0":
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择，请重试")


def main():
    """主函数"""
    try:
        interactive_demo()
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，程序退出")
    except Exception as e:
        print(f"\n❌ 程序出错: {e}")


if __name__ == "__main__":
    main()