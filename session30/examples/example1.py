#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session30 示例1: Docker部署配置生成器

本示例演示如何自动生成Docker部署所需的配置文件，包括：
- Dockerfile
- docker-compose.yml
- nginx配置
- 环境变量模板

作者: Python教程团队
创建日期: 2024-01-20
"""

import os
import json
from typing import Dict, List
from pathlib import Path


class DockerConfigGenerator:
    """
    Docker配置生成器
    
    自动生成Docker部署所需的各种配置文件
    """
    
    def __init__(self, project_name: str, python_version: str = "3.11"):
        self.project_name = project_name
        self.python_version = python_version
        self.output_dir = Path("docker_configs")
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_dockerfile(self, 
                          app_file: str = "app.py",
                          port: int = 8000,
                          requirements_file: str = "requirements.txt") -> str:
        """
        生成Dockerfile
        
        Args:
            app_file: 应用入口文件
            port: 应用端口
            requirements_file: 依赖文件
        
        Returns:
            str: Dockerfile内容
        """
        dockerfile_content = f"""# Dockerfile for {self.project_name}
FROM python:{self.python_version}-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \\
    gcc \\
    libpq-dev \\
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY {requirements_file} .

# 安装Python依赖
RUN pip install --no-cache-dir -r {requirements_file}

# 复制应用代码
COPY . .

# 创建非root用户
RUN useradd --create-home --shell /bin/bash appuser \\
    && chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE {port}

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:{port}/health || exit 1

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:{port}", "{app_file.replace('.py', '')}:app"]
"""
        
        dockerfile_path = self.output_dir / "Dockerfile"
        with open(dockerfile_path, 'w', encoding='utf-8') as f:
            f.write(dockerfile_content)
        
        print(f"✅ Dockerfile 已生成: {dockerfile_path}")
        return dockerfile_content
    
    def generate_docker_compose(self, 
                              app_port: int = 8000,
                              db_type: str = "postgresql",
                              use_redis: bool = True,
                              use_nginx: bool = True) -> str:
        """
        生成docker-compose.yml
        
        Args:
            app_port: 应用端口
            db_type: 数据库类型 (postgresql/mysql)
            use_redis: 是否使用Redis
            use_nginx: 是否使用Nginx
        
        Returns:
            str: docker-compose.yml内容
        """
        services = {
            'web': {
                'build': '.',
                'ports': [f"{app_port}:{app_port}"],
                'environment': [
                    'FLASK_ENV=production',
                    f'DATABASE_URL={self._get_db_url(db_type)}',
                    'REDIS_URL=redis://redis:6379/0' if use_redis else None
                ],
                'depends_on': self._get_dependencies(db_type, use_redis),
                'volumes': ['./logs:/app/logs'],
                'restart': 'unless-stopped'
            }
        }
        
        # 添加数据库服务
        if db_type == 'postgresql':
            services['db'] = {
                'image': 'postgres:15',
                'environment': [
                    'POSTGRES_DB=myapp',
                    'POSTGRES_USER=postgres',
                    'POSTGRES_PASSWORD=password'
                ],
                'volumes': [
                    'postgres_data:/var/lib/postgresql/data',
                    './init.sql:/docker-entrypoint-initdb.d/init.sql'
                ],
                'restart': 'unless-stopped'
            }
        elif db_type == 'mysql':
            services['db'] = {
                'image': 'mysql:8.0',
                'environment': [
                    'MYSQL_DATABASE=myapp',
                    'MYSQL_USER=mysql',
                    'MYSQL_PASSWORD=password',
                    'MYSQL_ROOT_PASSWORD=rootpassword'
                ],
                'volumes': [
                    'mysql_data:/var/lib/mysql'
                ],
                'restart': 'unless-stopped'
            }
        
        # 添加Redis服务
        if use_redis:
            services['redis'] = {
                'image': 'redis:7-alpine',
                'ports': ['6379:6379'],
                'restart': 'unless-stopped'
            }
        
        # 添加Nginx服务
        if use_nginx:
            services['nginx'] = {
                'image': 'nginx:alpine',
                'ports': ['80:80', '443:443'],
                'volumes': [
                    './nginx.conf:/etc/nginx/nginx.conf',
                    './ssl:/etc/nginx/ssl'
                ],
                'depends_on': ['web'],
                'restart': 'unless-stopped'
            }
        
        # 过滤None值
        for service in services.values():
            if 'environment' in service:
                service['environment'] = [env for env in service['environment'] if env]
        
        compose_config = {
            'version': '3.8',
            'services': services,
            'volumes': self._get_volumes(db_type)
        }
        
        # 转换为YAML格式字符串
        compose_content = self._dict_to_yaml(compose_config)
        
        compose_path = self.output_dir / "docker-compose.yml"
        with open(compose_path, 'w', encoding='utf-8') as f:
            f.write(compose_content)
        
        print(f"✅ docker-compose.yml 已生成: {compose_path}")
        return compose_content
    
    def generate_nginx_config(self, 
                            app_port: int = 8000,
                            domain: str = "localhost") -> str:
        """
        生成Nginx配置
        
        Args:
            app_port: 应用端口
            domain: 域名
        
        Returns:
            str: nginx.conf内容
        """
        nginx_content = f"""events {{
    worker_connections 1024;
}}

http {{
    upstream app {{
        server web:{app_port};
    }}
    
    # 日志格式
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    
    # Gzip压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
    
    # 限制请求大小
    client_max_body_size 10M;
    
    # HTTP服务器
    server {{
        listen 80;
        server_name {domain};
        
        access_log /var/log/nginx/access.log main;
        error_log /var/log/nginx/error.log;
        
        # 静态文件
        location /static/ {{
            alias /app/static/;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }}
        
        # 健康检查
        location /health {{
            proxy_pass http://app/health;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }}
        
        # 应用代理
        location / {{
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # 超时设置
            proxy_connect_timeout 30s;
            proxy_send_timeout 30s;
            proxy_read_timeout 30s;
        }}
    }}
    
    # HTTPS服务器 (需要SSL证书)
    # server {{
    #     listen 443 ssl http2;
    #     server_name {domain};
    #     
    #     ssl_certificate /etc/nginx/ssl/cert.pem;
    #     ssl_certificate_key /etc/nginx/ssl/key.pem;
    #     
    #     # SSL配置
    #     ssl_protocols TLSv1.2 TLSv1.3;
    #     ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    #     ssl_prefer_server_ciphers off;
    #     
    #     location / {{
    #         proxy_pass http://app;
    #         proxy_set_header Host $host;
    #         proxy_set_header X-Real-IP $remote_addr;
    #         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    #         proxy_set_header X-Forwarded-Proto $scheme;
    #     }}
    # }}
}}
"""
        
        nginx_path = self.output_dir / "nginx.conf"
        with open(nginx_path, 'w', encoding='utf-8') as f:
            f.write(nginx_content)
        
        print(f"✅ nginx.conf 已生成: {nginx_path}")
        return nginx_content
    
    def generate_env_template(self) -> str:
        """
        生成环境变量模板
        
        Returns:
            str: .env.example内容
        """
        env_content = """# 应用配置
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
DEBUG=False

# 数据库配置
DATABASE_URL=postgresql://postgres:password@db:5432/myapp
# 或者使用MySQL:
# DATABASE_URL=mysql://mysql:password@db:3306/myapp

# Redis配置
REDIS_URL=redis://redis:6379/0

# 邮件配置
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-email-password

# 第三方API
API_KEY=your-api-key
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_S3_BUCKET=your-s3-bucket

# 监控配置
SENTRY_DSN=your-sentry-dsn

# 其他配置
TIMEZONE=Asia/Shanghai
LOG_LEVEL=INFO
"""
        
        env_path = self.output_dir / ".env.example"
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print(f"✅ .env.example 已生成: {env_path}")
        return env_content
    
    def generate_requirements(self, 
                            framework: str = "flask",
                            include_dev: bool = False) -> str:
        """
        生成requirements.txt
        
        Args:
            framework: Web框架 (flask/django)
            include_dev: 是否包含开发依赖
        
        Returns:
            str: requirements.txt内容
        """
        base_requirements = [
            "python-dotenv>=1.0.0",
            "gunicorn>=21.0.0",
            "psycopg2-binary>=2.9.0",
            "redis>=4.5.0",
            "requests>=2.31.0",
            "celery>=5.3.0",
            "sentry-sdk>=1.32.0"
        ]
        
        if framework == "flask":
            base_requirements.extend([
                "Flask>=2.3.0",
                "Flask-SQLAlchemy>=3.0.0",
                "Flask-Migrate>=4.0.0",
                "Flask-Login>=0.6.0",
                "Flask-WTF>=1.1.0",
                "Flask-Mail>=0.9.0"
            ])
        elif framework == "django":
            base_requirements.extend([
                "Django>=4.2.0",
                "djangorestframework>=3.14.0",
                "django-cors-headers>=4.3.0",
                "django-environ>=0.11.0"
            ])
        
        dev_requirements = [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
            "mypy>=1.5.0"
        ]
        
        all_requirements = base_requirements
        if include_dev:
            all_requirements.extend(dev_requirements)
        
        requirements_content = "\n".join(sorted(all_requirements)) + "\n"
        
        req_path = self.output_dir / "requirements.txt"
        with open(req_path, 'w', encoding='utf-8') as f:
            f.write(requirements_content)
        
        print(f"✅ requirements.txt 已生成: {req_path}")
        return requirements_content
    
    def generate_all(self, 
                    framework: str = "flask",
                    db_type: str = "postgresql",
                    use_redis: bool = True,
                    use_nginx: bool = True):
        """
        生成所有配置文件
        
        Args:
            framework: Web框架
            db_type: 数据库类型
            use_redis: 是否使用Redis
            use_nginx: 是否使用Nginx
        """
        print(f"🚀 开始为项目 '{self.project_name}' 生成Docker配置...")
        print(f"框架: {framework}, 数据库: {db_type}, Redis: {use_redis}, Nginx: {use_nginx}")
        print("-" * 60)
        
        # 生成所有配置文件
        self.generate_dockerfile()
        self.generate_docker_compose(db_type=db_type, use_redis=use_redis, use_nginx=use_nginx)
        if use_nginx:
            self.generate_nginx_config()
        self.generate_env_template()
        self.generate_requirements(framework=framework)
        
        # 生成部署脚本
        self._generate_deploy_script()
        
        print("-" * 60)
        print(f"✅ 所有配置文件已生成到目录: {self.output_dir}")
        print("\n📋 下一步操作:")
        print("1. 复制 .env.example 为 .env 并填写实际配置")
        print("2. 根据需要修改生成的配置文件")
        print("3. 运行 docker-compose up -d 启动服务")
        print("4. 使用 ./deploy.sh 脚本进行部署")
    
    def _get_db_url(self, db_type: str) -> str:
        """获取数据库URL"""
        if db_type == 'postgresql':
            return 'postgresql://postgres:password@db:5432/myapp'
        elif db_type == 'mysql':
            return 'mysql://mysql:password@db:3306/myapp'
        else:
            return 'sqlite:///app.db'
    
    def _get_dependencies(self, db_type: str, use_redis: bool) -> List[str]:
        """获取服务依赖"""
        deps = ['db'] if db_type in ['postgresql', 'mysql'] else []
        if use_redis:
            deps.append('redis')
        return deps
    
    def _get_volumes(self, db_type: str) -> Dict:
        """获取数据卷配置"""
        volumes = {}
        if db_type == 'postgresql':
            volumes['postgres_data'] = None
        elif db_type == 'mysql':
            volumes['mysql_data'] = None
        return volumes
    
    def _dict_to_yaml(self, data: Dict, indent: int = 0) -> str:
        """简单的字典转YAML格式"""
        yaml_lines = []
        
        for key, value in data.items():
            if isinstance(value, dict):
                yaml_lines.append(f"{'  ' * indent}{key}:")
                yaml_lines.append(self._dict_to_yaml(value, indent + 1))
            elif isinstance(value, list):
                yaml_lines.append(f"{'  ' * indent}{key}:")
                for item in value:
                    if isinstance(item, str):
                        yaml_lines.append(f"{'  ' * (indent + 1)}- {item}")
                    else:
                        yaml_lines.append(f"{'  ' * (indent + 1)}- {item}")
            elif value is None:
                yaml_lines.append(f"{'  ' * indent}{key}:")
            else:
                yaml_lines.append(f"{'  ' * indent}{key}: {value}")
        
        return "\n".join(yaml_lines)
    
    def _generate_deploy_script(self):
        """生成部署脚本"""
        script_content = """#!/bin/bash
# 部署脚本

set -e

echo "🚀 开始部署..."

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker未运行，请先启动Docker"
    exit 1
fi

# 检查配置文件
if [ ! -f ".env" ]; then
    echo "❌ .env文件不存在，请复制.env.example并配置"
    exit 1
fi

# 构建镜像
echo "📦 构建Docker镜像..."
docker-compose build

# 停止旧服务
echo "⏹️ 停止旧服务..."
docker-compose down

# 启动新服务
echo "▶️ 启动新服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 健康检查
echo "🏥 执行健康检查..."
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo "✅ 部署成功！服务正常运行"
else
    echo "❌ 健康检查失败，请检查日志"
    docker-compose logs
    exit 1
fi

echo "🎉 部署完成！"
"""
        
        script_path = self.output_dir / "deploy.sh"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # 设置执行权限 (在Unix系统上)
        try:
            os.chmod(script_path, 0o755)
        except:
            pass  # Windows系统忽略权限设置
        
        print(f"✅ deploy.sh 已生成: {script_path}")


def main():
    """
    主函数：演示Docker配置生成器的使用
    """
    print("Session30 示例1: Docker部署配置生成器")
    print("=" * 60)
    
    # 创建配置生成器
    generator = DockerConfigGenerator(
        project_name="my-web-app",
        python_version="3.11"
    )
    
    # 生成所有配置文件
    generator.generate_all(
        framework="flask",
        db_type="postgresql",
        use_redis=True,
        use_nginx=True
    )
    
    print("\n📚 配置说明:")
    print("- Dockerfile: 定义应用容器镜像")
    print("- docker-compose.yml: 定义多容器应用栈")
    print("- nginx.conf: Nginx反向代理配置")
    print("- .env.example: 环境变量模板")
    print("- requirements.txt: Python依赖列表")
    print("- deploy.sh: 自动化部署脚本")
    
    print("\n🔧 使用方法:")
    print("1. 将生成的配置文件复制到你的项目根目录")
    print("2. 根据实际需求修改配置")
    print("3. 复制.env.example为.env并填写配置")
    print("4. 运行 docker-compose up -d 启动服务")


if __name__ == "__main__":
    main()