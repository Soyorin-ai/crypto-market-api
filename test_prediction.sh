#!/bin/bash

# 测试预测API的脚本

API_BASE="http://localhost:8000"

echo "=== 测试预测API ==="
echo ""

echo "1. 测试BTC 3天预测"
curl -s "${API_BASE}/api/v1/predict/btc?days=3" | python3 -m json.tool
echo ""
echo ""

echo "2. 测试SOL 7天预测"
curl -s "${API_BASE}/api/v1/predict/sol?days=7" | python3 -m json.tool
echo ""
echo ""

echo "3. 测试DOGE 30天预测"
curl -s "${API_BASE}/api/v1/predict/doge?days=30" | python3 -m json.tool
echo ""
echo ""

echo "4. 测试批量预测 (BTC, SOL, DOGE) 7天"
curl -s "${API_BASE}/api/v1/predict/btc-sol-doge?days=7" | python3 -m json.tool
echo ""
echo ""

echo "5. 测试批量预测 3天"
curl -s "${API_BASE}/api/v1/predict/btc-sol-doge?days=3" | python3 -m json.tool
echo ""
echo ""

echo "=== 测试完成 ==="