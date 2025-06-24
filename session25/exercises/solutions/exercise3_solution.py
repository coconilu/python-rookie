#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session25 练习题3解决方案：部署配置生成
"""

import os
import sys
from pathlib import Path
from typing import Dict, Optional


def generate_gunicorn_config(app_path: str, app_name: str, port: int, workers: int) -> str:
    """
    生成Gunicorn配置文件
    
    Args:
        app_path: 应用路径
        app_name: 应用名称
        port: 端口号
        workers: 工作进程数
    
    Returns:
        str: 配置文件内容
    """
    config = f'''# Gunicorn配置文件
# 应用名称: {app_name}

# 绑定地址和端口
bind = "127.0.0.1:{port}"

# 工作进程数
workers = {workers}

# 工作进程类型
worker_class = "sync"

# 每个工作进程的线程数
worker_connections = 1000

# 最大请求数，超过后重启工作进程
max_requests = 1000
max_requests_jitter = 100

# 超时设置
timeout = 30
keepalive = 2

# 进程名称
proc_name = "{app_name}"

# PID文件
pidfile = "{app_path}/gunicorn.pid"

# 日志配置
accesslog = "{app_path}/logs/access.log"
errorlog = "{app_path}/logs/error.log"
loglevel = "info"

# 用户和组
# user = "www-data"
# group = "www-data"

# 预加载应用
preload_app = True

# 启用自动重载（开发环境）
# reload = True

# 临时目录
tmp_upload_dir = None

# 安全设置
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# 启动钩子
def when_ready(server):
    server.log.info("Server is ready. Spawning workers")

def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")

def pre_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_worker_init(worker):
    worker.log.info("Worker initialized (pid: %s)", worker.pid)

def worker_abort(worker):
    worker.log.info("Worker aborted (pid: %s)", worker.pid)
'''
    return config


def generate_nginx_config(app_name: str, domain: str, port: int, static_path: Optional[str] = None) -> str:
    """
    生成Nginx配置文件
    
    Args:
        app_name: 应用名称
        domain: 域名
        port: 应用端口号
        static_path: 静态文件路径，如果为None则使用默认路径
    
    Returns:
        str: 配置文件内容
    """
    if static_path is None:
        static_path = f"/var/www/{app_name}/static"
    
    config = f'''# Nginx配置文件
# 应用名称: {app_name}
# 域名: {domain}

# 上游服务器配置
upstream {app_name}_backend {{
    # Gunicorn服务器
    server 127.0.0.1:{port} fail_timeout=0;
    
    # 如果有多个Gunicorn实例，可以添加更多服务器
    # server 127.0.0.1:{port + 1} fail_timeout=0;
    # server 127.0.0.1:{port + 2} fail_timeout=0;
}}

# HTTP服务器配置
server {{
    listen 80;
    server_name {domain} www.{domain};
    
    # 重定向到HTTPS
    return 301 https://$server_name$request_uri;
}}

# HTTPS服务器配置
server {{
    listen 443 ssl http2;
    server_name {domain} www.{domain};
    
    # SSL证书配置
    ssl_certificate /etc/ssl/certs/{domain}.crt;
    ssl_certificate_key /etc/ssl/private/{domain}.key;
    
    # SSL安全配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # 安全头
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    add_header Referrer-Policy "strict-origin-when-cross-origin";
    
    # 根目录
    root /var/www/{app_name};
    
    # 客户端最大请求体大小
    client_max_body_size 100M;
    
    # 静态文件配置
    location /static/ {{
        alias {static_path}/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        
        # Gzip压缩
        gzip on;
        gzip_vary on;
        gzip_min_length 1024;
        gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
    }}
    
    # 媒体文件配置
    location /media/ {{
        alias /var/www/{app_name}/media/;
        expires 1y;
        add_header Cache-Control "public";
    }}
    
    # favicon配置
    location = /favicon.ico {{
        alias {static_path}/favicon.ico;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }}
    
    # robots.txt配置
    location = /robots.txt {{
        alias {static_path}/robots.txt;
        expires 1d;
    }}
    
    # 应用代理配置
    location / {{
        # 代理到Gunicorn
        proxy_pass http://{app_name}_backend;
        
        # 代理头设置
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $server_name;
        
        # 超时设置
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
        
        # 缓冲设置
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
        
        # 重试设置
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
        proxy_next_upstream_tries 3;
        proxy_next_upstream_timeout 30s;
    }}
    
    # 健康检查
    location /health {{
        access_log off;
        proxy_pass http://{app_name}_backend;
        proxy_set_header Host $host;
    }}
    
    # 错误页面
    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;
    
    location = /404.html {{
        root /var/www/{app_name}/templates/errors;
        internal;
    }}
    
    location = /50x.html {{
        root /var/www/{app_name}/templates/errors;
        internal;
    }}
    
    # 访问日志
    access_log /var/log/nginx/{app_name}_access.log;
    error_log /var/log/nginx/{app_name}_error.log;
}}
'''
    return config


def generate_systemd_service(app_path: str, app_name: str, user: str = "www-data") -> str:
    """
    生成systemd服务文件
    
    Args:
        app_path: 应用路径
        app_name: 应用名称
        user: 运行服务的用户
    
    Returns:
        str: 配置文件内容
    """
    config = f'''[Unit]
Description={app_name} Gunicorn Application Server
After=network.target
Requires=network.target

[Service]
# 服务类型
Type=notify

# 运行用户和组
User={user}
Group={user}

# 工作目录
WorkingDirectory={app_path}

# 环境变量
Environment=PATH={app_path}/venv/bin
Environment=PYTHONPATH={app_path}
Environment=FLASK_ENV=production
Environment=FLASK_APP=app:app

# 启动命令
ExecStart={app_path}/venv/bin/gunicorn --config {app_path}/gunicorn.conf.py app:app

# 重启策略
Restart=always
RestartSec=3

# 启动超时
TimeoutStartSec=30

# 停止超时
TimeoutStopSec=30

# 停止信号
KillMode=mixed
KillSignal=SIGTERM

# 进程限制
LimitNOFILE=65535
LimitNPROC=4096

# 内存和CPU限制
# MemoryLimit=1G
# CPUQuota=50%

# 安全设置
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths={app_path}

# 标准输出和错误输出
StandardOutput=journal
StandardError=journal

# 日志标识
SyslogIdentifier={app_name}

[Install]
WantedBy=multi-user.target
'''
    return config


def generate_deployment_guide(app_path: str, app_name: str, domain: str) -> str:
    """
    生成部署说明文档
    
    Args:
        app_path: 应用路径
        app_name: 应用名称
        domain: 域名
    
    Returns:
        str: 文档内容
    """
    guide = f'''# {app_name} 部署说明

## 概述

本文档描述了如何在生产环境中部署 {app_name} 应用。

## 系统要求

- Ubuntu 20.04+ 或 CentOS 8+
- Python 3.8+
- Nginx 1.18+
- 至少 2GB RAM
- 至少 10GB 磁盘空间

## 部署步骤

### 1. 准备服务器环境

```bash
# 更新系统包
sudo apt update && sudo apt upgrade -y

# 安装必要的软件包
sudo apt install -y python3 python3-pip python3-venv nginx supervisor git

# 创建应用用户
sudo useradd -m -s /bin/bash {app_name}
sudo usermod -aG sudo {app_name}
```

### 2. 部署应用代码

```bash
# 切换到应用用户
sudo su - {app_name}

# 创建应用目录
sudo mkdir -p {app_path}
sudo chown {app_name}:{app_name} {app_path}
cd {app_path}

# 克隆代码（替换为实际的仓库地址）
git clone https://github.com/yourusername/{app_name}.git .

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

### 3. 配置应用

```bash
# 创建必要的目录
mkdir -p logs media static

# 复制配置文件
cp gunicorn.conf.py {app_path}/

# 设置环境变量
echo "export FLASK_ENV=production" >> ~/.bashrc
echo "export FLASK_APP=app:app" >> ~/.bashrc
source ~/.bashrc

# 收集静态文件（如果使用Flask-Assets等）
# python manage.py collectstatic --noinput

# 运行数据库迁移（如果有）
# python manage.py migrate
```

### 4. 配置Gunicorn

```bash
# 测试Gunicorn配置
cd {app_path}
source venv/bin/activate
gunicorn --config gunicorn.conf.py app:app

# 如果测试成功，按Ctrl+C停止
```

### 5. 配置systemd服务

```bash
# 复制服务文件
sudo cp {app_name}.service /etc/systemd/system/

# 重新加载systemd
sudo systemctl daemon-reload

# 启用并启动服务
sudo systemctl enable {app_name}
sudo systemctl start {app_name}

# 检查服务状态
sudo systemctl status {app_name}
```

### 6. 配置Nginx

```bash
# 复制Nginx配置
sudo cp nginx.conf /etc/nginx/sites-available/{app_name}

# 创建软链接
sudo ln -s /etc/nginx/sites-available/{app_name} /etc/nginx/sites-enabled/

# 测试Nginx配置
sudo nginx -t

# 重启Nginx
sudo systemctl restart nginx
```

### 7. 配置SSL证书（推荐使用Let's Encrypt）

```bash
# 安装Certbot
sudo apt install -y certbot python3-certbot-nginx

# 获取SSL证书
sudo certbot --nginx -d {domain} -d www.{domain}

# 设置自动续期
sudo crontab -e
# 添加以下行：
# 0 12 * * * /usr/bin/certbot renew --quiet
```

### 8. 配置防火墙

```bash
# 启用UFW
sudo ufw enable

# 允许SSH
sudo ufw allow ssh

# 允许HTTP和HTTPS
sudo ufw allow 'Nginx Full'

# 检查防火墙状态
sudo ufw status
```

## 监控和维护

### 查看应用日志

```bash
# 查看应用日志
sudo journalctl -u {app_name} -f

# 查看Nginx日志
sudo tail -f /var/log/nginx/{app_name}_access.log
sudo tail -f /var/log/nginx/{app_name}_error.log

# 查看Gunicorn日志
tail -f {app_path}/logs/access.log
tail -f {app_path}/logs/error.log
```

### 重启服务

```bash
# 重启应用
sudo systemctl restart {app_name}

# 重启Nginx
sudo systemctl restart nginx

# 重新加载Nginx配置（无需重启）
sudo systemctl reload nginx
```

### 更新应用

```bash
# 切换到应用目录
cd {app_path}

# 拉取最新代码
git pull origin main

# 激活虚拟环境
source venv/bin/activate

# 更新依赖
pip install -r requirements.txt

# 运行迁移（如果有）
# python manage.py migrate

# 重启应用
sudo systemctl restart {app_name}
```

### 备份

```bash
# 创建备份脚本
cat > /home/{app_name}/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/home/{app_name}/backups"
DATE=$(date +"%Y%m%d_%H%M%S")

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份应用代码
tar -czf $BACKUP_DIR/{app_name}_code_$DATE.tar.gz -C {app_path} .

# 备份数据库（如果使用PostgreSQL）
# pg_dump {app_name}_db > $BACKUP_DIR/{app_name}_db_$DATE.sql

# 删除7天前的备份
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
EOF

# 设置执行权限
chmod +x /home/{app_name}/backup.sh

# 添加到crontab（每天凌晨2点备份）
echo "0 2 * * * /home/{app_name}/backup.sh" | crontab -
```

## 性能优化

### 1. 数据库优化

- 配置数据库连接池
- 添加适当的索引
- 定期分析查询性能

### 2. 缓存配置

- 配置Redis缓存
- 使用CDN加速静态资源
- 启用浏览器缓存

### 3. 监控配置

- 安装和配置Prometheus + Grafana
- 设置应用性能监控
- 配置告警规则

## 故障排查

### 常见问题

1. **应用无法启动**
   - 检查日志：`sudo journalctl -u {app_name} -n 50`
   - 检查配置文件语法
   - 检查文件权限

2. **502 Bad Gateway**
   - 检查Gunicorn是否运行
   - 检查端口是否正确
   - 检查防火墙设置

3. **静态文件无法加载**
   - 检查Nginx配置中的静态文件路径
   - 检查文件权限
   - 检查SELinux设置（CentOS）

### 联系信息

如有问题，请联系运维团队：
- 邮箱：ops@example.com
- 电话：+86-xxx-xxxx-xxxx

---

**注意：** 请根据实际环境调整配置参数，确保安全性和性能。
'''
    return guide


def write_file(file_path: str, content: str) -> bool:
    """
    将内容写入文件
    
    Args:
        file_path: 文件路径
        content: 文件内容
    
    Returns:
        bool: 写入成功返回True，失败返回False
    """
    try:
        # 确保目录存在
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 文件已生成：{file_path}")
        return True
    
    except Exception as e:
        print(f"❌ 写入文件失败 {file_path}: {e}")
        return False


def get_user_input() -> Dict[str, str]:
    """
    获取用户输入的部署参数
    
    Returns:
        Dict[str, str]: 用户输入的参数
    """
    print("请输入部署参数：")
    
    params = {}
    params['app_name'] = input("应用名称 [myapp]: ").strip() or "myapp"
    params['app_path'] = input(f"应用路径 [/var/www/{params['app_name']}]: ").strip() or f"/var/www/{params['app_name']}"
    params['domain'] = input("域名 [example.com]: ").strip() or "example.com"
    
    try:
        params['port'] = int(input("端口 [8000]: ").strip() or "8000")
    except ValueError:
        params['port'] = 8000
    
    try:
        params['workers'] = int(input("工作进程数 [4]: ").strip() or "4")
    except ValueError:
        params['workers'] = 4
    
    params['user'] = input("运行用户 [www-data]: ").strip() or "www-data"
    params['static_path'] = input(f"静态文件路径 [{params['app_path']}/static]: ").strip() or f"{params['app_path']}/static"
    
    return params


def main():
    """
    主函数：执行部署配置生成任务
    """
    print("Session25 练习题3：部署配置生成")
    print("=" * 40)
    
    # 获取用户输入
    # 在实际练习中，你可以使用get_user_input()函数获取用户输入
    # 这里为了演示，使用硬编码的参数
    use_interactive = input("是否使用交互式输入？(y/N): ").strip().lower() == 'y'
    
    if use_interactive:
        params = get_user_input()
    else:
        params = {
            "app_name": "myapp",
            "app_path": "/var/www/myapp",
            "domain": "example.com",
            "port": 8000,
            "workers": 4,
            "user": "www-data",
            "static_path": "/var/www/myapp/static"
        }
    
    print("\n使用以下参数生成配置：")
    for key, value in params.items():
        print(f"  {key}: {value}")
    
    # 创建输出目录
    output_dir = "deployment_configs"
    Path(output_dir).mkdir(exist_ok=True)
    
    print(f"\n配置文件将生成到：{output_dir}/")
    
    # 1. 生成Gunicorn配置
    print("\n1. 生成Gunicorn配置文件...")
    gunicorn_config = generate_gunicorn_config(
        params['app_path'], 
        params['app_name'], 
        params['port'], 
        params['workers']
    )
    write_file(f"{output_dir}/gunicorn.conf.py", gunicorn_config)
    
    # 2. 生成Nginx配置
    print("\n2. 生成Nginx配置文件...")
    nginx_config = generate_nginx_config(
        params['app_name'], 
        params['domain'], 
        params['port'], 
        params['static_path']
    )
    write_file(f"{output_dir}/nginx.conf", nginx_config)
    
    # 3. 生成systemd服务文件
    print("\n3. 生成systemd服务文件...")
    systemd_config = generate_systemd_service(
        params['app_path'], 
        params['app_name'], 
        params['user']
    )
    write_file(f"{output_dir}/{params['app_name']}.service", systemd_config)
    
    # 4. 生成部署说明文档
    print("\n4. 生成部署说明文档...")
    deployment_guide = generate_deployment_guide(
        params['app_path'], 
        params['app_name'], 
        params['domain']
    )
    write_file(f"{output_dir}/DEPLOYMENT.md", deployment_guide)
    
    print("\n" + "=" * 40)
    print("部署配置生成完成！")
    print(f"\n生成的文件：")
    print(f"  - {output_dir}/gunicorn.conf.py")
    print(f"  - {output_dir}/nginx.conf")
    print(f"  - {output_dir}/{params['app_name']}.service")
    print(f"  - {output_dir}/DEPLOYMENT.md")
    
    print(f"\n下一步：")
    print(f"  1. 将配置文件复制到服务器")
    print(f"  2. 按照DEPLOYMENT.md中的说明进行部署")
    print(f"  3. 测试应用是否正常运行")


if __name__ == "__main__":
    main()