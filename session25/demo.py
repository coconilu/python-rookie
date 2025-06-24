#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session25: 部署与运维 - 演示代码

本文件演示了Python项目部署的核心概念和实际操作，包括：
- 环境检查和配置
- 依赖管理
- 部署脚本示例
- 监控和日志

作者: Python教程团队
创建日期: 2024-12-24
最后修改: 2024-12-24
"""

import os
import sys
import subprocess
import platform
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


def setup_logging():
    """
    配置日志系统
    """
    # 创建logs目录
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 配置日志格式
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'deployment.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)


class EnvironmentChecker:
    """
    环境检查器：检查部署环境的各项配置
    """
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.results = {}
    
    def check_python_version(self) -> bool:
        """
        检查Python版本
        """
        version = sys.version_info
        version_str = f"{version.major}.{version.minor}.{version.micro}"
        
        self.logger.info(f"Python版本: {version_str}")
        
        # 检查是否满足最低版本要求（3.8+）
        if version >= (3, 8):
            self.results['python_version'] = {
                'status': 'OK',
                'version': version_str,
                'message': 'Python版本满足要求'
            }
            return True
        else:
            self.results['python_version'] = {
                'status': 'ERROR',
                'version': version_str,
                'message': 'Python版本过低，建议升级到3.8+'
            }
            return False
    
    def check_virtual_environment(self) -> bool:
        """
        检查是否在虚拟环境中
        """
        in_venv = hasattr(sys, 'real_prefix') or (
            hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
        )
        
        if in_venv:
            venv_path = sys.prefix
            self.logger.info(f"当前在虚拟环境中: {venv_path}")
            self.results['virtual_env'] = {
                'status': 'OK',
                'path': venv_path,
                'message': '正在使用虚拟环境'
            }
            return True
        else:
            self.logger.warning("未检测到虚拟环境")
            self.results['virtual_env'] = {
                'status': 'WARNING',
                'path': None,
                'message': '建议使用虚拟环境隔离项目依赖'
            }
            return False
    
    def check_required_packages(self, packages: List[str]) -> bool:
        """
        检查必需的包是否已安装
        """
        missing_packages = []
        installed_packages = {}
        
        for package in packages:
            try:
                result = subprocess.run(
                    [sys.executable, '-m', 'pip', 'show', package],
                    capture_output=True,
                    text=True,
                    check=False
                )
                
                if result.returncode == 0:
                    # 解析版本信息
                    for line in result.stdout.split('\n'):
                        if line.startswith('Version:'):
                            version = line.split(':', 1)[1].strip()
                            installed_packages[package] = version
                            break
                else:
                    missing_packages.append(package)
            except Exception as e:
                self.logger.error(f"检查包 {package} 时出错: {e}")
                missing_packages.append(package)
        
        if missing_packages:
            self.results['packages'] = {
                'status': 'ERROR',
                'installed': installed_packages,
                'missing': missing_packages,
                'message': f'缺少必需的包: {", ".join(missing_packages)}'
            }
            return False
        else:
            self.results['packages'] = {
                'status': 'OK',
                'installed': installed_packages,
                'missing': [],
                'message': '所有必需的包都已安装'
            }
            return True
    
    def check_system_resources(self) -> bool:
        """
        检查系统资源
        """
        try:
            import psutil
            
            # 获取系统信息
            cpu_count = psutil.cpu_count()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            memory_gb = memory.total / (1024**3)
            disk_gb = disk.total / (1024**3)
            disk_free_gb = disk.free / (1024**3)
            
            self.logger.info(f"CPU核心数: {cpu_count}")
            self.logger.info(f"内存总量: {memory_gb:.1f}GB")
            self.logger.info(f"磁盘总量: {disk_gb:.1f}GB")
            self.logger.info(f"磁盘可用: {disk_free_gb:.1f}GB")
            
            # 检查资源是否充足
            warnings = []
            if memory_gb < 1:
                warnings.append("内存不足1GB")
            if disk_free_gb < 5:
                warnings.append("磁盘可用空间不足5GB")
            
            status = 'WARNING' if warnings else 'OK'
            message = '; '.join(warnings) if warnings else '系统资源充足'
            
            self.results['system_resources'] = {
                'status': status,
                'cpu_cores': cpu_count,
                'memory_gb': round(memory_gb, 1),
                'disk_total_gb': round(disk_gb, 1),
                'disk_free_gb': round(disk_free_gb, 1),
                'message': message
            }
            
            return len(warnings) == 0
            
        except ImportError:
            self.logger.warning("psutil未安装，无法检查系统资源")
            self.results['system_resources'] = {
                'status': 'SKIP',
                'message': 'psutil未安装，跳过系统资源检查'
            }
            return True
        except Exception as e:
            self.logger.error(f"检查系统资源时出错: {e}")
            self.results['system_resources'] = {
                'status': 'ERROR',
                'message': f'检查系统资源时出错: {e}'
            }
            return False
    
    def run_all_checks(self, required_packages: Optional[List[str]] = None) -> Dict:
        """
        运行所有检查
        """
        self.logger.info("开始环境检查...")
        
        checks = [
            self.check_python_version(),
            self.check_virtual_environment(),
            self.check_system_resources()
        ]
        
        if required_packages:
            checks.append(self.check_required_packages(required_packages))
        
        # 计算总体状态
        all_passed = all(checks)
        has_warnings = any(
            result.get('status') == 'WARNING' 
            for result in self.results.values()
        )
        
        overall_status = 'OK' if all_passed else ('WARNING' if has_warnings else 'ERROR')
        
        self.results['overall'] = {
            'status': overall_status,
            'checks_passed': sum(checks),
            'total_checks': len(checks),
            'timestamp': datetime.now().isoformat()
        }
        
        self.logger.info(f"环境检查完成，状态: {overall_status}")
        return self.results


class DeploymentManager:
    """
    部署管理器：管理应用的部署流程
    """
    
    def __init__(self, project_name: str, project_path: str):
        self.project_name = project_name
        self.project_path = Path(project_path)
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def create_deployment_config(self) -> Dict:
        """
        创建部署配置
        """
        config = {
            'project_name': self.project_name,
            'project_path': str(self.project_path),
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}",
            'platform': platform.system(),
            'deployment_time': datetime.now().isoformat(),
            'environment': {
                'FLASK_ENV': 'production',
                'PYTHONPATH': str(self.project_path),
            },
            'gunicorn': {
                'bind': '0.0.0.0:8000',
                'workers': 4,
                'worker_class': 'sync',
                'timeout': 30,
                'keepalive': 2,
                'max_requests': 1000
            }
        }
        
        # 保存配置文件
        config_file = self.project_path / 'deployment_config.json'
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"部署配置已保存到: {config_file}")
        return config
    
    def generate_gunicorn_config(self) -> str:
        """
        生成Gunicorn配置文件
        """
        config_content = '''# Gunicorn配置文件
# 绑定地址和端口
bind = "0.0.0.0:8000"

# 工作进程数（建议设置为CPU核心数的2-4倍）
workers = 4

# 工作进程类型
worker_class = "sync"

# 每个工作进程的连接数
worker_connections = 1000

# 请求超时时间（秒）
timeout = 30

# 保持连接时间（秒）
keepalive = 2

# 每个工作进程处理的最大请求数
max_requests = 1000

# 最大请求数的随机偏移
max_requests_jitter = 100

# 预加载应用
preload_app = True

# 日志配置
accesslog = "logs/gunicorn_access.log"
errorlog = "logs/gunicorn_error.log"
loglevel = "info"

# 进程名称
proc_name = "myproject"

# 用户和组（生产环境中建议使用非root用户）
# user = "www-data"
# group = "www-data"
'''
        
        config_file = self.project_path / 'gunicorn.conf.py'
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        self.logger.info(f"Gunicorn配置文件已生成: {config_file}")
        return str(config_file)
    
    def generate_dockerfile(self) -> str:
        """
        生成Dockerfile
        """
        dockerfile_content = '''# 使用官方Python运行时作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY pyproject.toml uv.lock* ./

# 安装uv和Python依赖
RUN pip install uv
RUN uv sync --frozen

# 复制应用代码
COPY . .

# 创建日志目录
RUN mkdir -p logs

# 暴露端口
EXPOSE 8000

# 设置环境变量
ENV PYTHONPATH=/app
ENV FLASK_ENV=production

# 健康检查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 启动命令
CMD ["uv", "run", "gunicorn", "-c", "gunicorn.conf.py", "app:app"]
'''
        
        dockerfile = self.project_path / 'Dockerfile'
        with open(dockerfile, 'w', encoding='utf-8') as f:
            f.write(dockerfile_content)
        
        self.logger.info(f"Dockerfile已生成: {dockerfile}")
        return str(dockerfile)
    
    def generate_docker_compose(self) -> str:
        """
        生成docker-compose.yml
        """
        compose_content = '''version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=sqlite:///app.db
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./static:/usr/share/nginx/html/static:ro
    depends_on:
      - web
    restart: unless-stopped

volumes:
  app_data:
'''
        
        compose_file = self.project_path / 'docker-compose.yml'
        with open(compose_file, 'w', encoding='utf-8') as f:
            f.write(compose_content)
        
        self.logger.info(f"docker-compose.yml已生成: {compose_file}")
        return str(compose_file)
    
    def generate_systemd_service(self) -> str:
        """
        生成systemd服务文件
        """
        service_content = f'''[Unit]
Description={self.project_name} Web Application
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory={self.project_path}
Environment=PATH={self.project_path}/.venv/bin
Environment=FLASK_ENV=production
ExecStart={self.project_path}/.venv/bin/gunicorn -c gunicorn.conf.py app:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
'''
        
        service_file = self.project_path / f'{self.project_name}.service'
        with open(service_file, 'w', encoding='utf-8') as f:
            f.write(service_content)
        
        self.logger.info(f"systemd服务文件已生成: {service_file}")
        self.logger.info(f"使用方法: sudo cp {service_file} /etc/systemd/system/")
        return str(service_file)


class HealthChecker:
    """
    健康检查器：监控应用运行状态
    """
    
    def __init__(self, app_url: str = "http://localhost:8000"):
        self.app_url = app_url
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def check_app_health(self) -> Dict:
        """
        检查应用健康状态
        """
        try:
            import requests
            
            # 发送健康检查请求
            response = requests.get(f"{self.app_url}/health", timeout=10)
            
            if response.status_code == 200:
                self.logger.info("应用健康检查通过")
                return {
                    'status': 'healthy',
                    'response_time': response.elapsed.total_seconds(),
                    'status_code': response.status_code,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                self.logger.warning(f"应用健康检查失败，状态码: {response.status_code}")
                return {
                    'status': 'unhealthy',
                    'status_code': response.status_code,
                    'timestamp': datetime.now().isoformat()
                }
                
        except ImportError:
            self.logger.warning("requests库未安装，无法进行HTTP健康检查")
            return {
                'status': 'skip',
                'message': 'requests库未安装',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"健康检查失败: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def check_process_status(self, process_name: str) -> Dict:
        """
        检查进程状态
        """
        try:
            import psutil
            
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if process_name in ' '.join(proc.info['cmdline'] or []):
                        processes.append({
                            'pid': proc.info['pid'],
                            'name': proc.info['name'],
                            'cmdline': ' '.join(proc.info['cmdline'] or [])
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if processes:
                self.logger.info(f"找到 {len(processes)} 个 {process_name} 进程")
                return {
                    'status': 'running',
                    'process_count': len(processes),
                    'processes': processes,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                self.logger.warning(f"未找到 {process_name} 进程")
                return {
                    'status': 'not_running',
                    'process_count': 0,
                    'timestamp': datetime.now().isoformat()
                }
                
        except ImportError:
            return {
                'status': 'skip',
                'message': 'psutil库未安装',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"检查进程状态失败: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }


def main():
    """
    主函数：演示部署与运维的核心功能
    """
    print("Session25: 部署与运维演示")
    print("=" * 50)
    
    # 设置日志
    logger = setup_logging()
    logger.info("开始部署与运维演示")
    
    try:
        # 1. 环境检查
        print("\n1. 环境检查")
        print("-" * 30)
        
        checker = EnvironmentChecker()
        required_packages = ['flask', 'gunicorn']
        results = checker.run_all_checks(required_packages)
        
        # 显示检查结果
        for check_name, result in results.items():
            if check_name != 'overall':
                status_icon = {
                    'OK': '✅',
                    'WARNING': '⚠️',
                    'ERROR': '❌',
                    'SKIP': '⏭️'
                }.get(result['status'], '❓')
                
                print(f"{status_icon} {check_name}: {result['message']}")
        
        # 2. 部署配置生成
        print("\n2. 部署配置生成")
        print("-" * 30)
        
        project_path = Path.cwd()
        deployment_manager = DeploymentManager("myproject", str(project_path))
        
        # 生成各种配置文件
        config = deployment_manager.create_deployment_config()
        print(f"✅ 部署配置已生成")
        
        gunicorn_config = deployment_manager.generate_gunicorn_config()
        print(f"✅ Gunicorn配置已生成")
        
        dockerfile = deployment_manager.generate_dockerfile()
        print(f"✅ Dockerfile已生成")
        
        compose_file = deployment_manager.generate_docker_compose()
        print(f"✅ docker-compose.yml已生成")
        
        service_file = deployment_manager.generate_systemd_service()
        print(f"✅ systemd服务文件已生成")
        
        # 3. 健康检查演示
        print("\n3. 健康检查演示")
        print("-" * 30)
        
        health_checker = HealthChecker()
        
        # 检查应用健康状态（模拟）
        health_status = health_checker.check_app_health()
        print(f"应用健康状态: {health_status['status']}")
        
        # 检查进程状态
        process_status = health_checker.check_process_status('python')
        print(f"Python进程状态: {process_status['status']}")
        if process_status['status'] == 'running':
            print(f"运行中的Python进程数: {process_status['process_count']}")
        
        # 4. 部署命令示例
        print("\n4. 部署命令示例")
        print("-" * 30)
        
        deployment_commands = [
            "# 使用uv部署",
            "uv sync",
            "uv run gunicorn -c gunicorn.conf.py app:app",
            "",
            "# 使用Docker部署",
            "docker build -t myproject:latest .",
            "docker run -d -p 8000:8000 --name myproject myproject:latest",
            "",
            "# 使用docker-compose部署",
            "docker-compose up -d",
            "",
            "# 使用systemd管理服务",
            "sudo systemctl enable myproject",
            "sudo systemctl start myproject",
            "sudo systemctl status myproject"
        ]
        
        for cmd in deployment_commands:
            print(cmd)
        
        # 5. 监控命令示例
        print("\n5. 监控命令示例")
        print("-" * 30)
        
        monitoring_commands = [
            "# 查看应用日志",
            "tail -f logs/gunicorn_access.log",
            "tail -f logs/gunicorn_error.log",
            "",
            "# 查看系统资源",
            "top",
            "htop",
            "free -h",
            "df -h",
            "",
            "# 查看网络连接",
            "netstat -tulpn | grep :8000",
            "ss -tulpn | grep :8000",
            "",
            "# Docker监控",
            "docker ps",
            "docker logs myproject",
            "docker stats"
        ]
        
        for cmd in monitoring_commands:
            print(cmd)
        
        print("\n" + "=" * 50)
        print("部署与运维演示完成！")
        print("\n生成的文件:")
        print("- deployment_config.json: 部署配置")
        print("- gunicorn.conf.py: Gunicorn配置")
        print("- Dockerfile: Docker镜像构建文件")
        print("- docker-compose.yml: Docker Compose配置")
        print("- myproject.service: systemd服务文件")
        print("- logs/deployment.log: 部署日志")
        
        logger.info("部署与运维演示成功完成")
        
    except Exception as e:
        logger.error(f"演示过程中出现错误: {e}")
        print(f"\n❌ 错误: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)