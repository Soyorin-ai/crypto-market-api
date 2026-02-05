import requests
import asyncio
from typing import Dict, List, Optional
from src.config import (
    COINCAP_API_BASE, 
    COINGECKO_API_BASE, 
    SUPPORTED_CRYPTO, 
    CRYPTO_SYMBOLS
)
from src.cache import cache_manager


class CryptoService:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CryptoMarketBot/1.0'
        })

    async def fetch_crypto_prices(self) -> Dict[str, float]:
        """获取所有支持的加密货币价格"""
        cache_key = "crypto_prices"
        
        # 尝试从缓存获取
        cached_data = cache_manager.get(cache_key)
        if cached_data:
            return cached_data

        prices = {}
        try:
            # 从 CoinCap API 获取数据
            response = self.session.get(f"{COINCAP_API_BASE}/assets", params={"limit": 50})
            response.raise_for_status()
            
            data = response.json()
            assets = {asset['id'].lower(): asset for asset in data['data']}
            
            # 只获取我们支持的加密货币
            for crypto_id in SUPPORTED_CRYPTO:
                if crypto_id in assets:
                    price_str = assets[crypto_id]['priceUsd']
                    prices[crypto_id] = round(float(price_str), 2)
                    
        except Exception as e:
            print(f"Error fetching crypto prices: {str(e)}")
            # 如果 API 请求失败，返回空字典
            prices = {}

        # 存入缓存
        if prices:
            cache_manager.set(cache_key, prices)
        
        return prices

    async def fetch_crypto_detail(self, crypto_id: str) -> Optional[Dict]:
        """获取特定加密货币的详细信息"""
        if crypto_id.lower() not in SUPPORTED_CRYPTO:
            return None
            
        cache_key = f"crypto_detail_{crypto_id.lower()}"
        
        # 尝试从缓存获取
        cached_data = cache_manager.get(cache_key)
        if cached_data:
            return cached_data

        try:
            # 从 CoinCap API 获取数据
            response = self.session.get(f"{COINCAP_API_BASE}/assets/{crypto_id}")
            response.raise_for_status()
            
            data = response.json()['data']
            
            detail = {
                "id": data['id'],
                "name": data['name'],
                "symbol": data['symbol'],
                "price_usd": round(float(data['priceUsd']), 2),
                "change_percent_24h": round(float(data['changePercent24Hr']), 2),
                "volume_usd_24h": round(float(data['volumeUsd24Hr']), 2),
                "market_cap_usd": round(float(data['marketCapUsd']), 2),
                "supply": round(float(data['supply']), 2) if data['supply'] else None
            }
            
            # 存入缓存
            cache_manager.set(cache_key, detail)
            
            return detail
            
        except Exception as e:
            print(f"Error fetching detail for {crypto_id}: {str(e)}")
            return None

    async def get_supported_cryptos(self) -> List[Dict[str, str]]:
        """获取支持的加密货币列表"""
        cryptos = []
        for crypto_id in SUPPORTED_CRYPTO:
            symbol = CRYPTO_SYMBOLS.get(crypto_id, crypto_id.upper())
            cryptos.append({
                "id": crypto_id,
                "symbol": symbol
            })
        return cryptos


# 创建全局服务实例
crypto_service = CryptoService()