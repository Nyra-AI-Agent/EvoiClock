#!/bin/bash

# EVOI Trading Clock 啟動腳本
# 適用於 macOS + Conda 環境

set -e  # 遇到錯誤立即停止

echo "🕒 EVOI Trading Clock v1.0 啟動腳本"
echo "====================================="
echo

# 檢查當前目錄
EVOI_DIR="$HOME/.xykms/evoi_clock"
echo "📁 檢查工作目錄: $EVOI_DIR"

if [[ ! -d "$EVOI_DIR" ]]; then
    echo "📁 創建工作目錄..."
    mkdir -p "$EVOI_DIR"
fi

cd "$EVOI_DIR"
echo "✅ 當前目錄: $(pwd)"
echo

# 檢查 Conda 環境
echo "🐍 檢查 Python 環境..."

if command -v conda >/dev/null 2>&1; then
    echo "✅ Conda 已安裝"
    
    # 檢查 tkpy 環境
    if conda env list | grep -q "tkpy"; then
        echo "✅ tkpy 環境已存在"
    else
        echo "📦 創建 tkpy 環境..."
        conda create -n tkpy python=3.12 tk -y
    fi
    
    # 激活環境
    echo "🔧 激活 tkpy 環境..."
    source $(conda info --base)/etc/profile.d/conda.sh
    conda activate tkpy
    
    echo "✅ Python: $(python --version)"
    echo "✅ 環境: $(conda info --envs | grep tkpy)"
    
else
    echo "❌ Conda 未安裝，嘗試使用系統 Python..."
    if command -v python3 >/dev/null 2>&1; then
        echo "✅ 使用系統 Python: $(python3 --version)"
        alias python=python3
    else
        echo "❌ 未找到 Python，請安裝 Python 3.12+"
        exit 1
    fi
fi

echo

# 檢查檔案
echo "📋 檢查程式檔案..."

FILES=("main.py" "test.py" "run.sh")
MISSING_FILES=()

for file in "${FILES[@]}"; do
    if [[ -f "$file" ]]; then
        echo "✅ $file 存在"
    else
        echo "❌ $file 不存在"
        MISSING_FILES+=("$file")
    fi
done

# 如果檔案缺失，提供下載或創建指令
if [[ ${#MISSING_FILES[@]} -gt 0 ]]; then
    echo
    echo "⚠️  缺失檔案，請執行以下操作："
    echo "1. 將 EVOI Trading Clock 主程式儲存為 main.py"
    echo "2. 將測試腳本儲存為 test.py"
    echo "3. 重新運行此腳本"
    echo
    echo "或者手動創建檔案："
    echo "touch main.py test.py"
    echo
    read -p "是否繼續運行測試？(y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo

# 運行測試（如果存在）
if [[ -f "test.py" && -s "test.py" ]]; then
    echo "🧪 運行環境測試..."
    python test.py
    echo
    
    read -p "測試是否通過？繼續啟動主程式？(Y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        echo "測試未通過，請檢查問題後重試"
        exit 1
    fi
fi

# 啟動主程式
echo "🚀 啟動 EVOI Trading Clock..."

if [[ -f "main.py" && -s "main.py" ]]; then
    echo "執行指令: python main.py"
    echo "按 Ctrl+C 可隨時停止程式"
    echo
    
    # 啟動主程式
    python main.py
    
else
    echo "❌ main.py 不存在或為空檔案"
    echo "請將 EVOI Trading Clock 主程式碼儲存為 main.py"
    echo
    echo "建立空檔案進行測試："
    echo "touch main.py"
    echo "nano main.py  # 編輯檔案"
    exit 1
fi

echo
echo "👋 EVOI Trading Clock 已結束"
echo "感謝使用！"