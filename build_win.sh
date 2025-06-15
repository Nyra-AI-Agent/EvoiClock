#!/bin/sh

# -----------------------------------------------------------------------------
# EVOI 時鐘應用程式 Windows 打包腳本
#
# 這個腳本使用 PyInstaller 將 Python 應用程式打包成一個獨立的 Windows .exe 檔案。
# 它會在 dist/EvoiClock_Win 資料夾中產生所有必要的檔案。
#
# 注意: 這個腳本需要在 macOS/Linux 上執行，並依賴於 PyInstaller。
# PyInstaller 會產生一個 Windows 可執行檔，但它本身需要在您的開發環境中執行。
# -----------------------------------------------------------------------------

echo "🚀 開始為 Windows 打包 EVOI 時鐘應用程式..."

# --- 環境變數 ---
# 指定 tkpy 環境中的 Python 直譯器完整路徑
PYTHON_EXEC="/Users/xy2024air15/miniforge3/envs/tkpy/bin/python"
PYINSTALLER_EXEC="/Users/xy2024air15/miniforge3/envs/tkpy/bin/pyinstaller"

# --- 專案路徑與檔案名稱 ---
APP_NAME="EvoiClock_Win"
SCRIPT_FILE="evoi_final.py"
# Windows 使用 .ico 格式, 暫時不指定圖示
# ICON_FILE="icon-shark2.ico" 
FONT_FILE="assets/Antonio-Regular.ttf"
IMAGE_FILE="icon-shark2.png"

# --- 輸出路徑 ---
DIST_PATH="dist"
BUILD_PATH="build"

# --- 清理舊的建置檔案 ---
echo "🧹 清理舊的建置檔案 (${DIST_PATH}/${APP_NAME}, ${BUILD_PATH})..."
rm -rf "${DIST_PATH}/${APP_NAME}"
rm -rf "${BUILD_PATH}"
rm -f "${APP_NAME}.spec"

# --- 執行 PyInstaller for Windows ---
echo "📦 正在使用 PyInstaller 為 Windows 進行打包..."

# 注意: --add-data 的路徑分隔符在 Windows 和 macOS/Linux 上不同。
# PyInstaller 在非 Windows 系統上打包 Windows target 時，能正確處理 ';' 或 ':'。
# 這裡我們使用跨平台更穩定的寫法，多次使用 --add-data。
${PYINSTALLER_EXEC} --noconsole \
    --distpath "${DIST_PATH}" \
    --workpath "${BUILD_PATH}" \
    --name "${APP_NAME}" \
    --add-data "${FONT_FILE}:assets" \
    --add-data "${IMAGE_FILE}:." \
    "${SCRIPT_FILE}"

# --- 檢查結果 ---
# 檢查 dist 資料夾中是否有名為 APP_NAME 的子資料夾
if [ -d "${DIST_PATH}/${APP_NAME}" ]; then
    echo "✅ 打包成功！"
    echo "Windows 應用程式檔案位於: ${DIST_PATH}/${APP_NAME}"
    echo "請將整個 ${APP_NAME} 資料夾複製到 Windows 電腦上執行其中的 .exe 檔案。"
    
    # 清理臨時檔案
    rm -rf "${BUILD_PATH}"
    rm -f "${APP_NAME}.spec"
    
    echo "✨ 已清理臨時檔案，打包完成。"
    # 打開所在的資料夾
    open "${DIST_PATH}"
else
    echo "❌ 打包失敗，請檢查上面的錯誤訊息。"
fi 