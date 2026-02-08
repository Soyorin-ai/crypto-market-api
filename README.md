# Crypto Market Data API

这是一个用于查询最新加密货币市场数据和价格预测的API服务。

## 功能特性
- 实时获取主要加密货币的价格信息
- 支持多种主流加密货币查询
- 基于技术分析的价格预测功能（BTC、SOL、DOGE）
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

### 价格查询
- `GET /api/v1/crypto/prices` - 获取所有支持的加密货币价格
- `GET /api/v1/crypto/{symbol}` - 获取特定加密货币详细信息
- `GET /api/v1/crypto/supported` - 获取支持的加密货币列表

### 价格预测
- `GET /api/v1/predict/{symbol}?days={days}` - 预测特定加密货币价格
  - `symbol`: 加密货币符号 (BTC, ETH, DOGE, SOL等)
  - `days`: 预测天数 (3, 7, 30)，默认7天

- `GET /api/v1/predict/btc-sol-doge?days={days}` - 批量预测BTC、SOL、DOGE价格
  - `days`: 预测天数 (3, 7, 30)，默认7天

### 其他
- `GET /api/v1/health` - 健康检查

## 预测功能说明

预测功能基于技术分析方法，包括：
- 移动平均线（短期和长期）
- 相对强弱指标（RSI）
- 布林带
- 动量指标
- 趋势分析

预测结果包括：
- 目标价格区间（最高价、最低价、预测价）
- 趋势判断（看涨/看跌/中性）
- 置信度（高/中/低）
- 技术指标详情

### 使用示例

```bash
# 预测BTC 7天后的价格
curl "http://localhost:8000/api/v1/predict/btc?days=7"

# 预测SOL 3天后的价格
curl "http://localhost:8000/api/v1/predict/sol?days=3"

# 批量预测BTC、SOL、DOGE 30天后的价格
curl "http://localhost:8000/api/v1/predict/btc-sol-doge?days=30"
```

## 支持的加密货币
- Bitcoin (BTC)
- Ethereum (ETH)
- Solana (SOL)
- Dogecoin (DOGE)
- Cardano (ADA)
- Binance Coin (BNB)
- Avalanche (AVAX)
- Polkadot (DOT)
- Litecoin (LTC)
- Chainlink (LINK)

## 免责声明
价格预测功能仅供参考，不构成投资建议。加密货币市场波动剧烈，投资需谨慎。