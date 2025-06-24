# Session25: 部署与运维 - 详细教程

## 1. 课程概述

在软件开发的生命周期中，部署与运维是将代码从开发环境转移到生产环境的关键步骤。本课程将带你了解Python项目部署的完整流程，从虚拟环境管理到生产环境部署。

## 2. 虚拟环境管理

### 2.1 为什么需要虚拟环境？

虚拟环境解决了以下问题：
- **依赖冲突**：不同项目可能需要同一个包的不同版本
- **环境隔离**：避免全局安装包污染系统环境
- **可重现性**：确保开发、测试、生产环境的一致性

### 2.2 Python内置venv

```python
# 创建虚拟环境
python -m venv myproject_env

# 激活虚拟环境
# Windows
myproject_env\Scripts\activate
# Linux/macOS
source myproject_env/bin/activate

# 停用虚拟环境
deactivate
```

### 2.3 现代化工具：uv

```bash
# 安装uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 创建项目
uv init myproject
cd myproject

# 添加依赖
uv add flask
uv add --dev pytest

# 同步环境
uv sync

# 运行脚本
uv run python app.py
```

**uv的优势：**
- 极快的依赖解析速度（比pip快10-100倍）
- 内置虚拟环境管理
- 自动生成锁文件确保版本一致性
- 支持Python版本管理

## 3. 依赖管理

### 3.1 requirements.txt（传统方式）

```txt
# requirements.txt
flask==2.3.3
requests>=2.25.0
numpy>=1.21.0,<2.0.0
```

```bash
# 安装依赖
pip install -r requirements.txt

# 生成requirements.txt
pip freeze > requirements.txt
```

### 3.2 pyproject.toml（现代方式）

```toml
[project]
name = "myproject"
version = "1.0.0"
description = "My awesome project"
requires-python = ">=3.8"
dependencies = [
    "flask>=2.0.0",
    "requests>=2.25.0",
    "sqlalchemy>=1.4.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=6.0.0",
    "black>=21.0.0",
    "flake8>=3.9.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### 3.3 锁文件的重要性

锁文件（如uv.lock、poetry.lock）记录了确切的依赖版本，确保：
- 开发团队使用相同的依赖版本
- 生产环境与开发环境一致
- 可重现的构建过程

## 4. 服务器部署基础

### 4.1 Linux基本命令

```bash
# 文件操作
ls -la                    # 列出文件
cd /path/to/directory     # 切换目录
mkdir myproject           # 创建目录
cp file1 file2           # 复制文件
mv file1 file2           # 移动/重命名文件
rm file                  # 删除文件

# 权限管理
chmod 755 script.py      # 修改文件权限
chown user:group file    # 修改文件所有者

# 进程管理
ps aux                   # 查看进程
kill PID                 # 终止进程
nohup python app.py &    # 后台运行

# 系统信息
top                      # 查看系统资源
df -h                    # 查看磁盘使用
free -h                  # 查看内存使用
```

### 4.2 SSH连接与文件传输

```bash
# SSH连接
ssh username@server_ip

# 使用密钥连接
ssh -i ~/.ssh/id_rsa username@server_ip

# 文件传输
scp local_file username@server_ip:/remote/path/
scp -r local_directory username@server_ip:/remote/path/

# 使用rsync同步
rsync -avz local_directory/ username@server_ip:/remote/path/
```

## 5. Web应用部署

### 5.1 使用Gunicorn部署Flask应用

**安装Gunicorn：**
```bash
uv add gunicorn
```

**创建Gunicorn配置文件（gunicorn.conf.py）：**
```python
# gunicorn.conf.py
bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True
```

**启动应用：**
```bash
# 基本启动
gunicorn app:app

# 使用配置文件
gunicorn -c gunicorn.conf.py app:app

# 后台运行
nohup gunicorn -c gunicorn.conf.py app:app > gunicorn.log 2>&1 &
```

### 5.2 Nginx反向代理

**安装Nginx：**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx

# CentOS/RHEL
sudo yum install nginx
```

**Nginx配置文件（/etc/nginx/sites-available/myproject）：**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/your/static/files;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

**启用配置：**
```bash
# 创建软链接
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启Nginx
sudo systemctl restart nginx
```

## 6. 容器化部署（Docker）

### 6.1 Docker基础概念

- **镜像（Image）**：应用程序的只读模板
- **容器（Container）**：镜像的运行实例
- **Dockerfile**：构建镜像的指令文件

### 6.2 创建Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY pyproject.toml uv.lock ./

# 安装uv和依赖
RUN pip install uv
RUN uv sync --frozen

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 设置环境变量
ENV PYTHONPATH=/app
ENV FLASK_ENV=production

# 启动命令
CMD ["uv", "run", "gunicorn", "-c", "gunicorn.conf.py", "app:app"]
```

### 6.3 Docker命令

```bash
# 构建镜像
docker build -t myproject:latest .

# 运行容器
docker run -d -p 8000:8000 --name myproject-container myproject:latest

# 查看容器
docker ps
docker logs myproject-container

# 进入容器
docker exec -it myproject-container /bin/bash

# 停止和删除容器
docker stop myproject-container
docker rm myproject-container
```

### 6.4 Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://user:password@db:5432/myproject
    depends_on:
      - db
    volumes:
      - ./logs:/app/logs

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=myproject
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - web

volumes:
  postgres_data:
```

```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs web

# 停止所有服务
docker-compose down
```

## 7. 持续集成与持续部署（CI/CD）

### 7.1 CI/CD概念

- **持续集成（CI）**：频繁地将代码集成到主分支，自动运行测试
- **持续部署（CD）**：自动将通过测试的代码部署到生产环境

### 7.2 GitHub Actions示例

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install uv
      run: curl -LsSf https://astral.sh/uv/install.sh | sh
    
    - name: Install dependencies
      run: uv sync
    
    - name: Run tests
      run: uv run pytest
    
    - name: Run linting
      run: uv run flake8 .

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to server
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /path/to/your/project
          git pull origin main
          uv sync
          sudo systemctl restart myproject
```

## 8. 监控与日志

### 8.1 应用日志

```python
# 配置日志
import logging
from logging.handlers import RotatingFileHandler

# 创建日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)

# 文件日志处理器
file_handler = RotatingFileHandler(
    'logs/app.log', 
    maxBytes=10240000,  # 10MB
    backupCount=10
)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s %(name)s %(message)s'
))

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
```

### 8.2 系统监控

```bash
# 使用systemd管理服务
# /etc/systemd/system/myproject.service
[Unit]
Description=My Project
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/project
Environment=PATH=/path/to/your/project/.venv/bin
ExecStart=/path/to/your/project/.venv/bin/gunicorn -c gunicorn.conf.py app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 启用和启动服务
sudo systemctl enable myproject
sudo systemctl start myproject
sudo systemctl status myproject
```

## 9. 安全最佳实践

### 9.1 环境变量管理

```python
# 使用python-dotenv管理环境变量
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DATABASE_URL = os.environ.get('DATABASE_URL')
    REDIS_URL = os.environ.get('REDIS_URL')
```

```bash
# .env文件（不要提交到版本控制）
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost/myproject
REDIS_URL=redis://localhost:6379/0
```

### 9.2 HTTPS配置

```bash
# 使用Let's Encrypt获取免费SSL证书
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 9.3 防火墙配置

```bash
# 使用ufw配置防火墙
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw status
```

## 10. 性能优化

### 10.1 应用层优化

```python
# 使用缓存
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis'})

@app.route('/api/data')
@cache.cached(timeout=300)  # 缓存5分钟
def get_data():
    # 耗时操作
    return expensive_operation()
```

### 10.2 数据库优化

```python
# 数据库连接池
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True
)
```

### 10.3 静态文件优化

```nginx
# Nginx静态文件配置
location /static {
    alias /path/to/static/files;
    expires 1y;
    add_header Cache-Control "public, immutable";
    gzip on;
    gzip_types text/css application/javascript image/svg+xml;
}
```

## 11. 故障排查

### 11.1 常见问题

1. **端口被占用**
```bash
# 查看端口使用情况
netstat -tulpn | grep :8000
lsof -i :8000

# 终止占用端口的进程
kill -9 PID
```

2. **权限问题**
```bash
# 检查文件权限
ls -la /path/to/file

# 修改权限
chmod 644 file.py
chown user:group file.py
```

3. **依赖问题**
```bash
# 重新安装依赖
uv sync --reinstall

# 清理缓存
uv cache clean
```

### 11.2 日志分析

```bash
# 查看实时日志
tail -f /var/log/nginx/access.log
tail -f logs/app.log

# 搜索错误日志
grep "ERROR" logs/app.log
grep "500" /var/log/nginx/access.log
```

## 12. 总结

本课程涵盖了Python项目部署的完整流程：

1. **环境管理**：使用虚拟环境隔离项目依赖
2. **依赖管理**：使用现代工具管理项目依赖
3. **服务器部署**：掌握Linux基本操作和Web服务器配置
4. **容器化**：使用Docker实现一致的部署环境
5. **自动化**：通过CI/CD实现自动化部署
6. **监控运维**：确保应用稳定运行

### 最佳实践总结

- 使用版本控制管理代码
- 环境变量管理敏感信息
- 自动化测试和部署
- 监控应用性能和错误
- 定期备份数据
- 保持依赖更新

### 下一步学习

- 学习Kubernetes进行容器编排
- 深入学习云平台部署（AWS、Azure、GCP）
- 学习微服务架构
- 掌握更多监控工具（Prometheus、Grafana）

通过本课程的学习，你已经具备了将Python项目部署到生产环境的基本能力。记住，部署是一个持续改进的过程，需要根据实际需求不断优化和调整。