#!/bin/bash

# EvoiClock 標準化打包腳本 for macOS
# 遵循 DEVELOPMENT_GUIDE.md 中定義的 SOP

# --- 前置檢查 ---
echo "INFO: 正在檢查 Conda 環境..."
if [[ "$CONDA_DEFAULT_ENV" != "tkpy" ]]; then
    echo "ERROR: 當前非 'tkpy' 環境！"
    echo "請先執行 'conda activate tkpy' 後再重新運行此腳本。"
    exit 1
fi

# --- 變數定義 ---
APP_NAME="EvoiClock"
MAIN_SCRIPT="src/main.py"
ICON="assets/EvoiClock.icns"
VERSION="4.2.0"

# --- 強制指定 tkpy 環境中的絕對路徑 (解決 PATH 問題) ---
CONDA_ENV_PATH="/Users/xy2024air15/miniforge3/envs/tkpy"
PYTHON_EXEC="${CONDA_ENV_PATH}/bin/python"
PYINSTALLER_EXEC="${CONDA_ENV_PATH}/bin/pyinstaller"


echo "INFO: 正在檢查必要工具..."
if ! command -v "$PYINSTALLER_EXEC" &> /dev/null; then
    echo "ERROR: 找不到 PyInstaller 執行檔於: $PYINSTALLER_EXEC"
    echo "請確認 'tkpy' 環境已正確建立。"
    exit 1
fi

echo "========================================="
echo "開始打包 $APP_NAME v$VERSION for macOS"
echo "========================================="
echo "主程式: $MAIN_SCRIPT"
echo "圖示:   $ICON"
echo "Python 直譯器: $PYTHON_EXEC"
echo "PyInstaller 路徑: $PYINSTALLER_EXEC"
echo "-----------------------------------------"

# --- 清理舊檔案 ---
echo "INFO: 正在清理舊的打包文件..."
rm -rf dist/ build/ "$APP_NAME.spec"
echo "INFO: 清理完成。"

# --- 執行 PyInstaller ---
echo "INFO: 正在執行 PyInstaller..."

# 使用絕對路徑的 Python 獲取 cnlunar 的絕對路徑
CNLUNAR_PATH=$($PYTHON_EXEC -c "import cnlunar; import os; print(os.path.dirname(cnlunar.__file__))")

if [ -z "$CNLUNAR_PATH" ]; then
    echo "ERROR: 無法找到 cnlunar 函式庫的路徑！"
    exit 1
fi
echo "INFO: 找到 cnlunar 路徑於: $CNLUNAR_PATH"

"$PYINSTALLER_EXEC" --name "$APP_NAME" \
            --windowed \
            --onefile \
            --icon="$ICON" \
            --add-data "${CNLUNAR_PATH}:cnlunar" \
            "$MAIN_SCRIPT"

# 檢查打包是否成功
if [ $? -ne 0 ]; then
    echo "ERROR: PyInstaller 打包失敗。請檢查上方輸出訊息。"
    exit 1
fi

echo "-----------------------------------------"
echo "🎉 SUCCESS: $APP_NAME.app 已成功建立於 dist/ 目錄下！"
echo "========================================="

# --- (可選) 建立 DMG ---
# 待未來實現，可參考 create-dmg 工具
# create-dmg \
#   --volname "$APP_NAME Installer" \
#   --volicon "$ICON" \
#   --window-pos 200 120 \
#   --window-size 800 400 \
#   --icon-size 100 \
#   --icon "$APP_NAME.app" 200 190 \
#   --hide-extension "$APP_NAME.app" \
#   --app-drop-link 600 185 \
#   "dist/$APP_NAME-$VERSION.dmg" \
#   "dist/" 