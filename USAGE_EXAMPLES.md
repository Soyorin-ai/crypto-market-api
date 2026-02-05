# Soyo Crypto Tool - 使用示例

这个工具允许您查询实时加密货币市场数据。

## 主要功能

### 1. 获取市场总览
```python
from soyo-crypto-tool.tool_interface import crypto_summary
result = crypto_summary()
print(result)
```

### 2. 检查特定加密货币
```python
from soyo-crypto-tool.tool_interface import crypto_check
result = crypto_check(['BTC', 'ETH'])
print(result)
```

### 3. 查看支持的加密货币
```python
from soyo-crypto-tool.tool_interface import supported_cryptos
result = supported_cryptos()
print(result)
```

### 4. 获取特定加密货币详细信息
```python
from soyo-crypto-tool.tool_interface import crypto_detail
result = crypto_detail('bitcoin')  # 或使用符号 'BTC'
print(result)
```

## 如何启动API服务

要使用这些功能，您需要先启动API服务：

```bash
cd soyo-crypto-tool
# 如果使用Docker
docker-compose up

# 或者手动运行（需要安装依赖）
python3 -m pip install -r requirements.txt
# 启动Redis服务（需要预先安装）
redis-server &
# 然后运行API
uvicorn src.main:app --reload
```

## 支持的加密货币

- Bitcoin (BTC)
- Ethereum (ETH) 
- Binance Coin (BNB)
- Solana (SOL)
- Cardano (ADA)
- Avalanche (AVAX)
- Polkadot (DOT)
- Dogecoin (DOGE)
- Litecoin (LTC)
- Chainlink (LINK)

## 注意事项

- API服务必须在 http://localhost:8000 上运行
- 如果服务不可用，工具会返回相应的错误消息
- 数据每5分钟从CoinCap API更新一次（取决于缓存设置）