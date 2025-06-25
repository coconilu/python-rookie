#!/bin/bash
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
