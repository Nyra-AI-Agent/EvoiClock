@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: EVOI Trading Clock 快速啟動腳本
:: 適用於 Windows

:: 顏色定義
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "NC=[0m"

:: 顯示啟動訊息
echo %GREEN%🚀 啟動 EVOI Trading Clock%NC%
echo %YELLOW%專業NQ期貨交易時鐘%NC%
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━

:: 檢查 Conda 環境
where conda >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo %RED%錯誤: 未找到 Conda%NC%
    echo 請先安裝 Miniforge 或 Miniconda
    pause
    exit /b 1
)

:: 檢查 tkpy 環境
conda env list | findstr "tkpy" >nul
if %ERRORLEVEL% neq 0 (
    echo %YELLOW%警告: 未找到 tkpy 環境%NC%
    echo 正在創建 tkpy 環境...
    conda create -n tkpy python=3.12 tk -y
)

:: 啟動 Conda 環境
echo %GREEN%啟動 tkpy 環境...%NC%
call conda activate tkpy

:: 檢查 Python 版本
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo %GREEN%Python 版本: !PYTHON_VERSION!%NC%

:: 檢查必要套件
echo %GREEN%檢查必要套件...%NC%
python -c "import tkinter" 2>nul || pip install tk

:: 切換到程式目錄
cd /d "%~dp0"

:: 執行測試
echo.
echo %YELLOW%執行功能測試...%NC%
python test_clock.py

:: 啟動主程式
echo.
echo %GREEN%啟動 EVOI Trading Clock...%NC%
python main.py

:: 程式結束時顯示訊息
echo.
echo %YELLOW%EVOI Trading Clock 已關閉%NC%
pause 