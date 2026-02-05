import requests
import json
from typing import Dict, List, Optional
from src.config import SUPPORTED_CRYPTO, CRYPTO_SYMBOLS


class CryptoMarketClient:
    """
    加密货币市场数据客户端
    用于调用本地运行的加密货币API服务
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Soyo-Crypto-Client/1.0',
            'Accept': 'application/json'
        })
    
    def get_all_prices(self) -> Dict[str, Dict[str, float]]:
        """
        获取所有支持的加密货币价格
        
        Returns:
            包含所有加密货币价格的字典
        """
        try:
            response = self.session.get(f"{self.base_url}/api/v1/crypto/prices")
            response.raise_for_status()
            data = response.json()
            return data.get('data', {})
        except requests.exceptions.RequestException as e:
            print(f"获取加密货币价格时出错: {e}")
            return {}
    
    def get_crypto_detail(self, symbol: str) -> Optional[Dict]:
        """
        获取特定加密货币的详细信息
        
        Args:
            symbol: 加密货币标识符（如 'bitcoin', 'ethereum'）
            
        Returns:
            加密货币详细信息字典，如果未找到则返回None
        """
        try:
            response = self.session.get(f"{self.base_url}/api/v1/crypto/{symbol}")
            if response.status_code == 404:
                return None
            response.raise_for_status()
            data = response.json()
            return data.get('data', {})
        except requests.exceptions.RequestException as e:
            print(f"获取 {symbol} 详细信息时出错: {e}")
            return None
    
    def get_supported_cryptos(self) -> List[Dict[str, str]]:
        """
        获取支持的加密货币列表
        
        Returns:
            支持的加密货币列表
        """
        try:
            response = self.session.get(f"{self.base_url}/api/v1/crypto/supported")
            response.raise_for_status()
            data = response.json()
            return data.get('data', [])
        except requests.exceptions.RequestException as e:
            print(f"获取支持的加密货币列表时出错: {e}")
            return []
    
    def get_price_by_symbol(self, symbol: str) -> Optional[float]:
        """
        根据符号获取特定加密货币的价格
        
        Args:
            symbol: 加密货币符号（如 'BTC', 'ETH'）
            
        Returns:
            价格（USD），如果未找到则返回None
        """
        # 首先尝试直接获取价格
        all_prices = self.get_all_prices()
        if symbol in all_prices:
            return all_prices[symbol]['price_usd']
        
        # 如果没找到，尝试通过ID获取
        for crypto_id in SUPPORTED_CRYPTO:
            if CRYPTO_SYMBOLS.get(crypto_id, '').lower() == symbol.lower():
                detail = self.get_crypto_detail(crypto_id)
                if detail:
                    return detail.get('price_usd')
        
        return None


# 创建全局客户端实例
client = CryptoMarketClient()


def get_crypto_prices_summary() -> str:
    """
    获取加密货币价格摘要，格式化为易读的字符串
    """
    prices = client.get_all_prices()
    
    if not prices:
        return "暂时无法获取加密货币价格数据。请确保API服务正在运行。"
    
    summary = "📈 加密货币市场价格概览:\n"
    summary += "=" * 30 + "\n"
    
    # 按市值大致排序显示（这里简单按价格显示）
    sorted_prices = sorted(prices.items(), key=lambda x: x[1]['price_usd'], reverse=True)
    
    for symbol, data in sorted_prices:
        price = data['price_usd']
        crypto_id = data['id']
        
        # 获取24小时变化（如果有详细数据）
        detail = client.get_crypto_detail(crypto_id)
        change_24h = detail.get('change_percent_24h', 0) if detail else 0
        
        change_str = f" ({change_24h:+.2f}%)" if change_24h != 0 else ""
        summary += f"{symbol}: ${price:,.2f}{change_str}\n"
    
    return summary


def quick_crypto_check(symbols: List[str]) -> str:
    """
    快速检查特定加密货币的价格
    
    Args:
        symbols: 要检查的加密货币符号列表
        
    Returns:
        格式化的检查结果
    """
    result = "🔍 加密货币快速检查:\n"
    result += "=" * 25 + "\n"
    
    for symbol in symbols:
        price = client.get_price_by_symbol(symbol)
        if price is not None:
            result += f"{symbol}: ${price:,.2f}\n"
        else:
            result += f"{symbol}: 未找到\n"
    
    return result


if __name__ == "__main__":
    # 示例用法
    print(get_crypto_prices_summary())