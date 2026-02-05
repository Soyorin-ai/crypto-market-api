"""
Crypto Market Tool Interface
一个可以直接调用的加密货币查询工具
"""

from typing import Dict, List, Optional
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from simple_client import get_crypto_prices_summary, quick_crypto_check, SimpleCryptoClient
except ImportError as e:
    print(f"无法导入加密货币客户端: {e}")
    get_crypto_prices_summary = None
    quick_crypto_check = None
    SimpleCryptoClient = None


def run_crypto_tool(action: str = "summary", **kwargs) -> str:
    """
    运行加密货币工具的主要接口函数
    
    Args:
        action: 要执行的操作 ('summary', 'check', 'detail')
        **kwargs: 操作参数
        
    Returns:
        操作结果字符串
    """
    if SimpleCryptoClient is None:
        return "错误: 无法加载加密货币客户端。请确保相关依赖已安装。"
    
    base_url = kwargs.get('base_url', 'http://localhost:8000')
    client = SimpleCryptoClient(base_url)
    
    if action == "summary":
        if get_crypto_prices_summary:
            return get_crypto_prices_summary(base_url)
        else:
            return "错误: 无法获取价格摘要"
    
    elif action == "check":
        symbols = kwargs.get('symbols', [])
        if quick_crypto_check and symbols:
            return quick_crypto_check(symbols, base_url)
        else:
            return "错误: 请提供要检查的符号列表"
    
    elif action == "supported":
        supported = client.get_supported_cryptos()
        result = "📋 支持的加密货币:\n"
        result += "=" * 20 + "\n"
        for crypto in supported:
            result += f"- {crypto['symbol']} ({crypto['id']})\n"
        return result
    
    elif action == "detail":
        symbol = kwargs.get('symbol')
        if symbol:
            detail = client.get_crypto_detail(symbol)
            if detail:
                result = f"🔍 {detail['name']} ({detail['symbol']}) 详细信息:\n"
                result += "=" * 40 + "\n"
                result += f"价格 (USD): ${detail['price_usd']:,.2f}\n"
                result += f"24小时变化: {detail['change_percent_24h']:+.2f}%\n"
                result += f"24小时交易量: ${detail['volume_usd_24h']:,.2f}\n"
                result += f"市值: ${detail['market_cap_usd']:,.2f}\n"
                if detail.get('circulating_supply'):
                    result += f"流通量: {detail['circulating_supply']:,.2f}\n"
                return result
            else:
                return f"未找到加密货币 '{symbol}' 的详细信息"
        else:
            return "错误: 请提供要查询的加密货币符号"
    
    else:
        return f"未知操作: {action}。支持的操作: summary, check, supported, detail"


def crypto_summary() -> str:
    """获取加密货币市场总览"""
    return run_crypto_tool("summary")


def crypto_check(symbols: List[str]) -> str:
    """检查特定加密货币价格"""
    return run_crypto_tool("check", symbols=symbols)


def supported_cryptos() -> str:
    """获取支持的加密货币列表"""
    return run_crypto_tool("supported")


def crypto_detail(symbol: str) -> str:
    """获取特定加密货币的详细信息"""
    return run_crypto_tool("detail", symbol=symbol)


# 工具元数据
TOOL_INFO = {
    "name": "crypto_market_tool",
    "description": "加密货币市场数据查询工具",
    "functions": {
        "crypto_summary": "获取加密货币市场总览",
        "crypto_check": "检查特定加密货币价格",
        "supported_cryptos": "获取支持的加密货币列表", 
        "crypto_detail": "获取特定加密货币的详细信息"
    }
}


if __name__ == "__main__":
    # 当直接运行时，显示工具信息
    print("Crypto Market Tool Interface")
    print("=" * 30)
    print("可用函数:")
    for func_name, desc in TOOL_INFO["functions"].items():
        print(f"- {func_name}(): {desc}")