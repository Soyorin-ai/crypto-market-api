#!/bin/bash

# Soyo Crypto Tool - API启动脚本

echo "🔍 检查依赖..."

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3"
    exit 1
fi

# 检查pip是否安装
if ! command -v pip3 &> /dev/null; then
    echo "❌ 错误: 未找到pip3"
    exit 1
fi

# 检查Redis是否安装
if ! command -v redis-server &> /dev/null; then
    echo "⚠️  警告: 未找到Redis。API功能将受限。"
    echo "   请考虑安装Redis: sudo apt install redis-server"
fi

# 检查Docker是否安装
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo "🐳 发现Docker和Docker Compose，使用容器化部署"
    docker-compose up --build
else
    echo "🔧 使用本地Python环境部署"
    echo "   正在安装依赖..."
    
    # 检查并创建虚拟环境
    if [ ! -d "venv" ]; then
        echo "   创建虚拟环境..."
        python3 -m venv venv || {
            echo "❌ 无法创建虚拟环境，请确保安装了python3-venv"
            echo "   Ubuntu/Debian: sudo apt install python3-venv"
            exit 1
        }
    fi
    
    # 激活虚拟环境
    source venv/bin/activate
    
    # 安装依赖
    pip install -r requirements.txt || {
        echo "❌ 依赖安装失败"
        exit 1
    }
    
    echo "   启动API服务..."
    # 启动Redis（如果可用）
    if command -v redis-server &> /dev/null; then
        echo "   启动Redis服务..."
        redis-server --daemonize yes
    fi
    
    # 启动API服务
    uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
fi