import requests
import asyncio
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import statistics
from src.config import COINCAP_API_BASE


class PredictionService:
    """加密货币价格预测服务"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CryptoMarketBot/1.0'
        })

    async def fetch_historical_data(self, crypto_id: str, interval: str = "h1", limit: int = 24) -> List[Dict]:
        """
        获取历史价格数据

        Args:
            crypto_id: 加密货币ID
            interval: 时间间隔 (m1, m5, m15, m30, h1, h2, h4, h6, h12, d1)
            limit: 获取的数据点数量

        Returns:
            历史价格数据列表
        """
        try:
            response = self.session.get(
                f"{COINCAP_API_BASE}/assets/{crypto_id}/history",
                params={"interval": interval, "limit": limit}
            )
            response.raise_for_status()

            data = response.json()
            return data.get('data', [])

        except Exception as e:
            print(f"Error fetching historical data for {crypto_id}: {str(e)}")
            return []

    def calculate_technical_indicators(self, prices: List[float]) -> Dict:
        """
        计算技术指标

        Args:
            prices: 价格列表

        Returns:
            技术指标字典
        """
        if not prices or len(prices) < 5:
            return {}

        # 移动平均线
        ma_short = statistics.mean(prices[-5:])  # 5期移动平均
        ma_long = statistics.mean(prices[-20:]) if len(prices) >= 20 else ma_short

        # 相对强弱指标（简化版）
        def calculate_rsi(price_list, period=14):
            if len(price_list) < period + 1:
                return 50

            gains = []
            losses = []

            for i in range(1, len(price_list)):
                change = price_list[i] - price_list[i-1]
                if change > 0:
                    gains.append(change)
                    losses.append(0)
                else:
                    gains.append(0)
                    losses.append(abs(change))

            avg_gain = statistics.mean(gains[-period:])
            avg_loss = statistics.mean(losses[-period:])

            if avg_loss == 0:
                return 100

            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            return rsi

        # 布林带
        std_dev = statistics.stdev(prices[-20:]) if len(prices) >= 20 else 0
        upper_band = ma_long + (2 * std_dev)
        lower_band = ma_long - (2 * std_dev)

        # 动量指标
        momentum = prices[-1] - prices[-5] if len(prices) >= 5 else 0
        momentum_percent = (momentum / prices[-5]) * 100 if prices[-5] != 0 else 0

        return {
            "ma_short": round(ma_short, 2),
            "ma_long": round(ma_long, 2),
            "rsi": round(calculate_rsi(prices), 2),
            "upper_band": round(upper_band, 2),
            "lower_band": round(lower_band, 2),
            "momentum": round(momentum, 2),
            "momentum_percent": round(momentum_percent, 2),
            "current_price": round(prices[-1], 2)
        }

    def analyze_trend(self, indicators: Dict) -> str:
        """
        分析趋势

        Args:
            indicators: 技术指标字典

        Returns:
            趋势判断 (bullish/bearish/neutral)
        """
        score = 0

        # MA交叉判断
        if indicators.get("ma_short", 0) > indicators.get("ma_long", 0):
            score += 2  # 金叉，看涨
        else:
            score -= 2  # 死叉，看跌

        # RSI判断
        rsi = indicators.get("rsi", 50)
        if rsi < 30:
            score += 1  # 超卖，可能反弹
        elif rsi > 70:
            score -= 1  # 超买，可能回调

        # 动量判断
        if indicators.get("momentum_percent", 0) > 5:
            score += 2  # 强劲上涨动量
        elif indicators.get("momentum_percent", 0) < -5:
            score -= 2  # 下跌动量

        # 布林带位置
        current = indicators.get("current_price", 0)
        upper = indicators.get("upper_band", 0)
        lower = indicators.get("lower_band", 0)

        if current > upper:
            score -= 1  # 超过上轨，可能回调
        elif current < lower:
            score += 1  # 低于下轨，可能反弹

        # 综合判断
        if score >= 3:
            return "strong_bullish"  # 强烈看涨
        elif score >= 1:
            return "bullish"  # 看涨
        elif score <= -3:
            return "strong_bearish"  # 强烈看跌
        elif score <= -1:
            return "bearish"  # 看跌
        else:
            return "neutral"  # 中性

    def calculate_price_target(self, indicators: Dict, trend: str, days: int) -> Dict:
        """
        计算价格目标

        Args:
            indicators: 技术指标
            trend: 趋势判断
            days: 预测天数

        Returns:
            价格目标字典
        """
        current_price = indicators.get("current_price", 0)
        volatility = (indicators.get("upper_band", 0) - indicators.get("lower_band", 0)) / 2 if current_price > 0 else 0
        volatility_percent = (volatility / current_price) * 100 if current_price > 0 else 0

        # 基于趋势和波动性计算目标价格
        trend_multiplier = {
            "strong_bullish": 0.08,
            "bullish": 0.05,
            "neutral": 0.02,
            "bearish": -0.05,
            "strong_bearish": -0.08
        }.get(trend, 0.02)

        # 基于天数调整
        day_factor = min(days / 30, 1.0)  # 最多30天的因子

        # 基础变化
        base_change = current_price * trend_multiplier * day_factor

        # 波动性调整
        volatility_adjustment = current_price * (volatility_percent / 100) * day_factor * 0.5

        # 计算目标价格
        target_high = current_price + base_change + volatility_adjustment
        target_low = current_price + base_change - volatility_adjustment
        target_price = (target_high + target_low) / 2

        # 计算变化百分比
        change_percent = ((target_price - current_price) / current_price) * 100 if current_price > 0 else 0

        return {
            "current_price": round(current_price, 2),
            "target_price": round(target_price, 2),
            "target_high": round(target_high, 2),
            "target_low": round(target_low, 2),
            "change_percent": round(change_percent, 2),
            "trend": trend,
            "confidence": self.calculate_confidence(trend, indicators)
        }

    def calculate_confidence(self, trend: str, indicators: Dict) -> str:
        """
        计算预测置信度

        Args:
            trend: 趋势判断
            indicators: 技术指标

        Returns:
            置信度 (high/medium/low)
        """
        rsi = indicators.get("rsi", 50)
        momentum = indicators.get("momentum_percent", 0)

        # 如果RSI处于极端区域，置信度较高
        if trend in ["strong_bullish", "strong_bearish"]:
            if (rsi < 25 or rsi > 75) and abs(momentum) > 10:
                return "high"
            else:
                return "medium"
        elif trend in ["bullish", "bearish"]:
            if (rsi < 35 or rsi > 65) and abs(momentum) > 5:
                return "medium"
            else:
                return "low"
        else:
            return "low"

    async def predict_crypto_price(self, crypto_id: str, days: int) -> Dict:
        """
        预测加密货币价格

        Args:
            crypto_id: 加密货币ID
            days: 预测天数 (3, 7, 30)

        Returns:
            预测结果字典
        """
        # 验证天数
        if days not in [3, 7, 30]:
            return {
                "error": "days must be 3, 7, or 30",
                "symbol": crypto_id.upper()
            }

        # 根据天数选择不同的时间间隔
        interval_map = {
            3: ("h1", 72),    # 3天 = 72小时
            7: ("h4", 42),    # 7天 = 42个4小时
            30: ("d1", 30)     # 30天 = 30个1天
        }

        interval, limit = interval_map[days]

        # 获取历史数据
        historical_data = await self.fetch_historical_data(crypto_id, interval, limit)

        if not historical_data or len(historical_data) < 5:
            return {
                "error": "Insufficient data for prediction",
                "symbol": crypto_id.upper()
            }

        # 提取价格数据
        prices = [float(data['priceUsd']) for data in historical_data if 'priceUsd' in data]

        if len(prices) < 5:
            return {
                "error": "Insufficient price data",
                "symbol": crypto_id.upper()
            }

        # 计算技术指标
        indicators = self.calculate_technical_indicators(prices)

        # 分析趋势
        trend = self.analyze_trend(indicators)

        # 计算价格目标
        price_target = self.calculate_price_target(indicators, trend, days)

        # 构建预测结果
        result = {
            "symbol": crypto_id.upper(),
            "prediction_period": f"{days}_days",
            "prediction_date": (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d"),
            "technical_indicators": {
                "rsi": indicators.get("rsi"),
                "ma_short": indicators.get("ma_short"),
                "ma_long": indicators.get("ma_long"),
                "momentum_percent": indicators.get("momentum_percent")
            },
            "prediction": price_target,
            "disclaimer": "此预测基于技术分析，仅供参考，不构成投资建议。"
        }

        return result

    async def predict_multiple_cryptos(self, crypto_ids: List[str], days: int) -> Dict:
        """
        批量预测多个加密货币

        Args:
            crypto_ids: 加密货币ID列表
            days: 预测天数

        Returns:
            预测结果字典
        """
        results = {}

        # 并发获取所有预测
        tasks = [self.predict_crypto_price(crypto_id, days) for crypto_id in crypto_ids]
        predictions = await asyncio.gather(*tasks, return_exceptions=True)

        for crypto_id, prediction in zip(crypto_ids, predictions):
            if isinstance(prediction, Exception):
                results[crypto_id.upper()] = {
                    "error": str(prediction),
                    "symbol": crypto_id.upper()
                }
            else:
                results[crypto_id.upper()] = prediction

        return {
            "data": results,
            "prediction_period": f"{days}_days",
            "timestamp": datetime.now().isoformat()
        }


# 创建全局预测服务实例
prediction_service = PredictionService()