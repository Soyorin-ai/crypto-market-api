import os
from dotenv import load_dotenv

load_dotenv()

# API配置
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
API_ROOT_PATH = os.getenv("API_ROOT_PATH", "")

# 缓存配置
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CACHE_TTL = int(os.getenv("CACHE_TTL", 300))  # 5分钟缓存

# 外部API配置
COINCAP_API_BASE = "https://api.coincap.io/v2"
COINGECKO_API_BASE = "https://api.coingecko.com/api/v3"

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