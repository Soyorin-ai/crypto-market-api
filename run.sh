#!/bin/bash

echo "Crypto Market Data API 启动脚本"

# 检查是否提供了Redis服务
if ! command -v docker &> /dev/null; then
    echo "警告: Docker 未安装，将尝试直接运行应用"
    echo "请确保已安装Python依赖: pip install -r requirements.txt"
    echo "请确保Redis服务正在运行"
    python3 src/main.py
else
    echo "使用Docker Compose启动服务..."
    docker-compose up
fi