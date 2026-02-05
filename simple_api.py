from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import requests
import time
from datetime import datetime, timedelta


app = FastAPI(
    title="Simple Crypto Market Data API",
    description="简化版加密货币市场价格查询API（无Redis依赖）",
    version="1.0.0"
)

# CORS中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 内存缓存
cache = {}
CACHE_TTL = 300  # 5分钟缓存


def is_cached_data_valid(timestamp):
    """检查缓存的数据是否仍然有效"""
    return time.time() - timestamp < CACHE_TTL


def get_from_cache(key):
    """从缓存获取数据"""
    if key in cache:
        data, timestamp = cache[key]
        if is_cached_data_valid(timestamp):
            return data
        else:
            del cache[key]  # 删除过期数据
    return None


def set_to_cache(key, data):
    """设置缓存数据"""
    cache[key] = (data, time.time())


# 支持的加密货币
SUPPORTED_CRYPTO = [
    "bitcoin",
    "ethereum", 
    "binancecoin",
    "solana",
    "cardano",
    "avalanche",
    "polkadot",
    "dogecoin",
    "litecoin",
    "chainlink"
]

CRYPTO_SYMBOLS = {
    "bitcoin": "BTC",
    "ethereum": "ETH", 
    "binancecoin": "BNB",
    "solana": "SOL",
    "cardano": "ADA",
    "avalanche": "AVAX",
    "polkadot": "DOT",
    "dogecoin": "DOGE",
    "litecoin": "LTC",
    "chainlink": "LINK"
}


@app.get("/")
async def root():
    """API根路径"""
    return {
        "message": "Simple Crypto Market Data API (No Redis)",
        "version": "1.0.0",
        "endpoints": {
            "/api/v1/crypto/prices": "获取所有支持的加密货币价格",
            "/api/v1/crypto/{symbol}": "获取特定加密货币详情",
            "/api/v1/crypto/supported": "获取支持的加密货币列表"
        }
    }


@app.get("/api/v1/crypto/prices")
async def get_crypto_prices():
    """获取所有支持的加密货币价格"""
    cache_key = "crypto_prices"
    
    # 尝试从缓存获取
    cached_data = get_from_cache(cache_key)
    if cached_data:
        return {"data": cached_data}

    prices = {}
    try:
        # 从 CoinGecko API 获取数据
        response = requests.get("https://api.coingecko.com/api/v3/simple/price", 
                               params={
                                   "ids": ",".join(SUPPORTED_CRYPTO),
                                   "vs_currencies": "usd",
                                   "include_24hr_change": "true"
                               })
        response.raise_for_status()
        
        data = response.json()
        
        # 只获取我们支持的加密货币
        for crypto_id in SUPPORTED_CRYPTO:
            if crypto_id in data:
                price_data = data[crypto_id]
                prices[crypto_id] = {
                    "id": crypto_id,
                    "price_usd": round(price_data['usd'], 2),
                    "change_24h": round(price_data.get('usd_24h_change', 0), 2)
                }
                
    except Exception as e:
        print(f"Error fetching crypto prices: {str(e)}")
        # 如果 API 请求失败，返回空字典
        prices = {}

    # 存入缓存
    if prices:
        set_to_cache(cache_key, prices)
    
    return {"data": prices}


@app.get("/api/v1/crypto/{crypto_id}")
async def get_crypto_detail(crypto_id: str):
    """获取特定加密货币的详细信息"""
    if crypto_id.lower() not in SUPPORTED_CRYPTO:
        raise HTTPException(status_code=404, detail="Cryptocurrency not found")
        
    cache_key = f"crypto_detail_{crypto_id.lower()}"
    
    # 尝试从缓存获取
    cached_data = get_from_cache(cache_key)
    if cached_data:
        return {"data": cached_data}

    try:
        # 从 CoinGecko API 获取数据
        response = requests.get(f"https://api.coingecko.com/api/v3/coins/{crypto_id}")
        response.raise_for_status()
        
        data = response.json()
        
        detail = {
            "id": data['id'],
            "name": data['name'],
            "symbol": data['symbol'].upper(),
            "price_usd": round(data['market_data']['current_price']['usd'], 2),
            "change_percent_24h": round(data['market_data']['price_change_percentage_24h'], 2),
            "volume_usd_24h": round(data['market_data']['total_volume']['usd'], 2),
            "market_cap_usd": round(data['market_data']['market_cap']['usd'], 2),
            "circulating_supply": round(data['market_data']['circulating_supply'], 2) if data['market_data']['circulating_supply'] else None,
            "total_supply": round(data['market_data']['total_supply'], 2) if data['market_data']['total_supply'] else None
        }
        
        # 存入缓存
        set_to_cache(cache_key, detail)
        
        return {"data": detail}
        
    except Exception as e:
        print(f"Error fetching detail for {crypto_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching data for {crypto_id}")


@app.get("/api/v1/crypto/supported")
async def get_supported_cryptos():
    """获取支持的加密货币列表"""
    cryptos = []
    for crypto_id in SUPPORTED_CRYPTO:
        symbol = CRYPTO_SYMBOLS.get(crypto_id, crypto_id.upper())
        cryptos.append({
            "id": crypto_id,
            "symbol": symbol
        })
    return {"data": cryptos}


@app.get("/api/v1/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "simple-crypto-market-api"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)