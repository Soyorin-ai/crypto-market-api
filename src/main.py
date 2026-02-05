from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import uvicorn

from src.config import API_HOST, API_PORT, API_ROOT_PATH
from src.crypto_service import crypto_service
from src.cache import cache_manager


app = FastAPI(
    title="Crypto Market Data API",
    description="实时加密货币市场价格查询API",
    version="1.0.0",
    root_path=API_ROOT_PATH
)

# CORS中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """API根路径"""
    return {
        "message": "Crypto Market Data API",
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
    prices = await crypto_service.fetch_crypto_prices()
    
    # 添加符号信息
    result = {}
    for crypto_id, price in prices.items():
        symbol = crypto_service.CRYPTO_SYMBOLS.get(crypto_id, crypto_id.upper())
        result[symbol] = {
            "id": crypto_id,
            "price_usd": price
        }
    
    return {"data": result}


@app.get("/api/v1/crypto/{crypto_id}")
async def get_crypto_detail(crypto_id: str):
    """获取特定加密货币的详细信息"""
    detail = await crypto_service.fetch_crypto_detail(crypto_id.lower())
    
    if not detail:
        raise HTTPException(status_code=404, detail="Cryptocurrency not found")
    
    return {"data": detail}


@app.get("/api/v1/crypto/supported")
async def get_supported_cryptos():
    """获取支持的加密货币列表"""
    cryptos = await crypto_service.get_supported_cryptos()
    return {"data": cryptos}


@app.get("/api/v1/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "crypto-market-api"}


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True
    )