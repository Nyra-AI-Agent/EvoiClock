#!/bin/sh

# -----------------------------------------------------------------------------
# EVOI 時鐘應用程式打包腳本
#
# 這個腳本使用 PyInstaller 將 Python 應用程式打包成一個獨立的 macOS .app 檔案。
# 它會自動處理所有依賴、圖示和資料檔案。
#
# 使用方法:
# 在終端機中，cd 到 evoi_clock 目錄，然後執行 ./build.sh
# -----------------------------------------------------------------------------

echo "🚀 開始打包 EVOI 時鐘應用程式..."

# --- 環境變數 ---
# 指定 tkpy 環境中的 Python 直譯器完整路徑
PYTHON_EXEC="/Users/xy2024air15/miniforge3/envs/tkpy/bin/python"
PYINSTALLER_EXEC="/Users/xy2024air15/miniforge3/envs/tkpy/bin/pyinstaller"

# --- 專案路徑與檔案名稱 (相對於此腳本位置) ---
APP_NAME="EvoiClock"
SCRIPT_FILE="evoi_final.py"
ICON_FILE="icon-shark2.icns"
FONT_FILE="assets/Antonio-Regular.ttf"
IMAGE_FILE="icon-shark2.png"

# --- 輸出路徑 (相對於此腳本位置) ---
DIST_PATH="dist"
BUILD_PATH="build"

# --- 清理舊的建置檔案 ---
echo "🧹 清理舊的建置檔案 (${DIST_PATH}, ${BUILD_PATH})..."
rm -rf "${DIST_PATH}"
rm -rf "${BUILD_PATH}"
rm -f "${APP_NAME}.spec"

# --- 執行 PyInstaller ---
echo "📦 正在使用 PyInstaller 進行打包..."
${PYINSTALLER_EXEC} --windowed \
    --distpath "${DIST_PATH}" \
    --workpath "${BUILD_PATH}" \
    --name "${APP_NAME}" \
    --icon="${ICON_FILE}" \
    --add-data "${FONT_FILE}:assets" \
    --add-data "${IMAGE_FILE}:." \
    "${SCRIPT_FILE}"

# --- 檢查結果 ---
if [ -d "${DIST_PATH}/${APP_NAME}.app" ]; then
    echo "✅ 打包成功！"
    echo "新的應用程式位於: ${DIST_PATH}/${APP_NAME}.app"
    # 清理臨時檔案
    rm -rf "${BUILD_PATH}"
    rm -f "${APP_NAME}.spec"
    echo "✨ 已清理臨時檔案，打包完成。"
    # 打開所在的資料夾
    open "${DIST_PATH}"
else
    echo "❌ 打包失敗，請檢查上面的錯誤訊息。"
fi 