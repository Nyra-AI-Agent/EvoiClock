#!/bin/bash

# EVOI Trading Clock 快速啟動腳本
# 適用於 macOS (ARM/M1/M2)

# 顏色定義
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 顯示啟動訊息
echo -e "${GREEN}🚀 啟動 EVOI Trading Clock${NC}"
echo -e "${YELLOW}專業NQ期貨交易時鐘${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 檢查 Conda 環境
if ! command -v conda &> /dev/null; then
    echo -e "${RED}錯誤: 未找到 Conda${NC}"
    echo "請先安裝 Miniforge 或 Miniconda"
    exit 1
fi

# 檢查 tkpy 環境
if ! conda env list | grep -q "tkpy"; then
    echo -e "${YELLOW}警告: 未找到 tkpy 環境${NC}"
    echo "正在創建 tkpy 環境..."
    conda create -n tkpy python=3.12 tk -y
fi

# 啟動 Conda 環境
echo -e "${GREEN}啟動 tkpy 環境...${NC}"
source $(conda info --base)/etc/profile.d/conda.sh
conda activate tkpy

# 檢查 Python 版本
PYTHON_VERSION=$(python --version 2>&1)
echo -e "${GREEN}Python 版本: ${PYTHON_VERSION}${NC}"

# 檢查必要套件
echo -e "${GREEN}檢查必要套件...${NC}"
python -c "import tkinter" 2>/dev/null || pip install tk

# 切換到程式目錄
cd "$(dirname "$0")"

# 執行測試
echo -e "\n${YELLOW}執行功能測試...${NC}"
python test_clock.py

# 啟動主程式
echo -e "\n${GREEN}啟動 EVOI Trading Clock...${NC}"
python main.py

# 程式結束時顯示訊息
echo -e "\n${YELLOW}EVOI Trading Clock 已關閉${NC}" 