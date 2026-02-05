# Crypto Market Data API

这是一个用于查询最新加密货币市场数据的API服务。

## 功能特性
- 实时获取主要加密货币的价格信息
- 支持多种主流加密货币查询
- 数据缓存机制，减少API请求频率
- RESTful API 接口

## 技术栈
- FastAPI: Web框架
- Requests: HTTP客户端
- Redis: 数据缓存
- Uvicorn: ASGI服务器

## 安装部署
```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## API端点
- `GET /api/v1/crypto/prices` - 获取所有支持的加密货币价格
- `GET /api/v1/crypto/{symbol}` - 获取特定加密货币价格