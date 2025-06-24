# Flask部署示例项目

这是Session25的示例项目，展示了Python Web应用的完整部署与运维流程。

## 项目概述

本项目是一个完整的Flask Web应用，包含以下特性：

- 🌐 响应式Web界面
- 🔌 RESTful API接口
- 💓 健康检查端点
- 📊 系统监控功能
- 📝 完整的日志记录
- 🐳 Docker容器化支持
- 🔧 生产环境配置

## 技术栈

### 后端
- Python 3.9+
- Flask 2.3+
- Gunicorn WSGI服务器
- psutil系统监控

### 前端
- HTML5 + CSS3
- Bootstrap 5
- JavaScript (ES6+)

### 部署
- Docker & Docker Compose
- Nginx反向代理
- Redis缓存
- Prometheus + Grafana监控

## 快速开始

### 方法1：本地开发环境

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd session25/project
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **运行应用**
   ```bash
   python app.py
   ```

5. **访问应用**
   - 打开浏览器访问：http://localhost:5000
   - API接口：http://localhost:5000/api/status
   - 健康检查：http://localhost:5000/health

### 方法2：Docker部署

1. **构建镜像**
   ```bash
   docker build -t flask-deploy-demo .
   ```

2. **运行容器**
   ```bash
   docker run -p 8000:8000 flask-deploy-demo
   ```

3. **访问应用**
   - 打开浏览器访问：http://localhost:8000

### 方法3：Docker Compose（推荐）

1. **启动所有服务**
   ```bash
   docker-compose up -d
   ```

2. **访问服务**
   - Flask应用：http://localhost:80
   - Prometheus：http://localhost:9090
   - Grafana：http://localhost:3000

3. **停止服务**
   ```bash
   docker-compose down
   ```

## 项目结构

```
project/
├── app.py                 # Flask应用主文件
├── requirements.txt       # Python依赖
├── Dockerfile            # Docker镜像构建文件
├── docker-compose.yml    # Docker Compose配置
├── README.md             # 项目说明
├── templates/            # HTML模板
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   └── errors/
│       ├── 404.html
│       └── 500.html
├── static/               # 静态文件
├── logs/                 # 日志文件
└── nginx/                # Nginx配置
    └── nginx.conf
```

## API接口

### 基础接口

- `GET /` - 首页
- `GET /about` - 关于页面
- `GET /health` - 健康检查

### API接口

- `GET /api/status` - 应用状态
- `GET /api/info` - 系统信息
- `GET|POST /api/echo` - 回显接口

### 健康检查响应示例

```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "checks": {
    "database": true,
    "disk_space": true,
    "memory": true
  }
}
```

## 配置说明

### 环境变量

- `FLASK_ENV` - 运行环境 (development/production/testing)
- `FLASK_APP` - Flask应用入口
- `SECRET_KEY` - 应用密钥（生产环境必须设置）
- `HOST` - 绑定主机地址
- `PORT` - 绑定端口

### 配置文件

应用支持多环境配置：

- **开发环境**：DEBUG=True，详细日志
- **测试环境**：TESTING=True，警告级别日志
- **生产环境**：DEBUG=False，信息级别日志

## 部署指南

### 生产环境部署

1. **服务器准备**
   ```bash
   # 更新系统
   sudo apt update && sudo apt upgrade -y
   
   # 安装Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   
   # 安装Docker Compose
   sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

2. **部署应用**
   ```bash
   # 克隆代码
   git clone <repository-url>
   cd session25/project
   
   # 设置环境变量
   export SECRET_KEY="your-secret-key-here"
   
   # 启动服务
   docker-compose -f docker-compose.yml up -d
   ```

3. **配置Nginx（可选）**
   ```bash
   # 如果需要自定义域名和SSL
   sudo apt install nginx certbot python3-certbot-nginx
   
   # 获取SSL证书
   sudo certbot --nginx -d yourdomain.com
   ```

### 监控配置

1. **Prometheus配置**
   - 访问：http://localhost:9090
   - 配置文件：`prometheus/prometheus.yml`

2. **Grafana配置**
   - 访问：http://localhost:3000
   - 默认用户名/密码：admin/admin
   - 添加Prometheus数据源：http://prometheus:9090

## 开发指南

### 代码规范

```bash
# 代码格式化
black .

# 代码检查
flake8 .

# 运行测试
pytest

# 测试覆盖率
pytest --cov=.
```

### 添加新功能

1. 在`app.py`中添加新路由
2. 创建对应的HTML模板
3. 添加必要的测试
4. 更新文档

### 日志查看

```bash
# 应用日志
tail -f logs/app.log

# Docker容器日志
docker-compose logs -f web

# Nginx日志
docker-compose logs -f nginx
```

## 故障排查

### 常见问题

1. **应用无法启动**
   ```bash
   # 检查日志
   docker-compose logs web
   
   # 检查端口占用
   netstat -tulpn | grep :8000
   ```

2. **502 Bad Gateway**
   ```bash
   # 检查应用是否运行
   docker-compose ps
   
   # 检查健康状态
   curl http://localhost:8000/health
   ```

3. **静态文件无法加载**
   ```bash
   # 检查文件权限
   ls -la static/
   
   # 检查Nginx配置
   docker-compose exec nginx nginx -t
   ```

### 性能优化

1. **应用优化**
   - 增加Gunicorn工作进程数
   - 启用Redis缓存
   - 优化数据库查询

2. **服务器优化**
   - 配置Nginx缓存
   - 启用Gzip压缩
   - 使用CDN加速静态资源

## 安全建议

1. **生产环境必须**
   - 设置强密码的SECRET_KEY
   - 使用HTTPS
   - 定期更新依赖
   - 配置防火墙

2. **可选安全措施**
   - 启用CSRF保护
   - 配置速率限制
   - 使用WAF
   - 定期安全扫描

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

MIT License

## 联系方式

- 项目地址：https://github.com/yourusername/python-rookie
- 问题反馈：https://github.com/yourusername/python-rookie/issues
- 邮箱：your.email@example.com

---

**注意**：这是一个教学示例项目，请根据实际需求调整配置和安全设置。