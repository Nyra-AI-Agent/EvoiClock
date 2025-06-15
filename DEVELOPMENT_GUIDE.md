# EvoiClock 專案開發指南

本文檔定義了 EvoiClock 專案及其衍生專案的標準開發流程 (SOP)。所有開發者，包括未來的 AI 代理，都應嚴格遵守本指南，以確保程式碼品質、可維護性與協作效率。

---

## 總覽：專案生命週期

一個標準的 EvoiClock 專案開發週期包含以下五個核心階段：

1.  **環境初始化 (Initialization)**
2.  **本地開發與版本控制 (Development & Git)**
3.  **資源處理 (Asset Handling)**
4.  **打包與分發 (Packaging & Distribution)**
5.  **倉庫與文件管理 (Repository & Documentation)**

---

## 階段一：環境初始化 (SOP)

### 1. 取得專案

**禁止**直接在舊有或混亂的目錄上工作。永遠從一個乾淨的起點開始。

```bash
# 1. 備份舊目錄 (如果有的話)
# mv ./evoi_clock ./evoi_clock_backup_YYYYMMDD

# 2. 從 GitHub 克隆最新的專案
git clone https://github.com/Nyra-AI-Agent/EvoiClock.git
cd EvoiClock
```

### 2. Conda 環境設置

**禁止**在 `base` 環境中安裝任何專案依賴。

```bash
# 1. 建立一個專屬的 Conda 環境 (以 python 3.12 為例)
conda create --name tkpy python=3.12 -y

# 2. 啟動環境
conda activate tkpy

# 3. 安裝依賴
pip install -r requirements.txt
```
*註：`requirements.txt` 應只包含最小執行必要的套件。*

### 3. 確認環境

在執行任何操作前，請務必確認目前處於正確的 Conda 環境。

```bash
conda info --envs
```
*應該會看到 `tkpy` 前面有一個 `*` 號。*

---

## 階段二：本地開發與版本控制 (SOP)

### 1. 目錄結構

所有新功能開發都必須遵循以下標準目錄結構：

```
EvoiClock/
├── .gitignore
├── README.md           
├── DEVELOPMENT_GUIDE.md  # 開發指南 (本文件)
├── requirements.txt      
├── build.sh              # macOS 打包腳本
│
├── src/                  # 所有 Python 原始碼
│   └── main.py           
│
└── assets/               # 所有非程式碼資源
    └── EvoiClock.icns      # 標準 macOS 應用程式圖示
```

### 2. 主程式入口

- 唯一的程式入口檔案為 `src/main.py`。
- 所有新的程式碼都應該以模組化的方式在 `src/` 目錄下建立，並由 `main.py` 進行呼叫。

### 3. Git 版本控制流程

我們採用功能分支 (Feature Branch) 的工作流程。

```bash
# 1. 確保在主分支，並拉取最新變更
git checkout main
git pull origin main

# 2. 為新功能建立一個描述性的分支
git checkout -b feat/add-new-quote-animation

# 3. 在新分支上進行開發和修改...
# (修改 src/main.py 等檔案)

# 4. 完成開發後，提交有意義的 Commit
git add .
git commit -m "feat(animation): Add fade-in effect for quote transition"

# 5. 推送到遠端
git push origin feat/add-new-quote-animation

# 6. 在 GitHub 上建立 Pull Request，請求合併到 main 分支
```
**Commit 訊息規範**: 我們遵循 [Conventional Commits](https://www.conventionalcommits.org/) 規範，格式為 `type(scope): description`。
- `feat`: 新功能
- `fix`: 修復 Bug
- `docs`: 文件變更
- `style`: 程式碼風格調整 (不影響功能)
- `refactor`: 重構
- `chore`: 建置流程、輔助工具的變動

---

## 階段三：資源處理 (SOP)

### 製作標準 macOS 圖示 (`.icns`)

為確保應用程式在 macOS Dock 中顯示完美，必須使用帶有**透明邊距**的標準 `.icns` 檔案。

**禁止**直接使用未經處理的 `.png` 作為圖示。

**操作流程**:

1.  **準備母版圖示**: 準備一張 `1024x1024` 像素的透明背景 `.png` 圖示母版 (例如 `icon_master.png`)。

2.  **增加透明邊距**: 使用 `ImageMagick` (需先用 `brew install imagemagick` 安裝) 為母版增加邊距。此步驟至關重要。

    ```bash
    # 將 1024px 的母版縮小到 820px，並置於一個 1024px 的透明畫布中央
    magick convert -size 1024x1024 xc:none \
      \( icon_master.png -resize 820x820 \) \
      -gravity center -composite \
      icon-padded.png
    ```

3.  **建立 `iconset` 資料夾**:

    ```bash
    # 清理舊的，建立新的
    rm -rf MyIcon.iconset
    mkdir MyIcon.iconset
    ```

4.  **生成所有尺寸**: 使用 `sips` 指令，以帶邊距的圖示 (`icon-padded.png`) 生成所有 Apple 需要的尺寸。

    ```bash
    sips -z 16 16     icon-padded.png --out MyIcon.iconset/icon_16x16.png
    sips -z 32 32     icon-padded.png --out MyIcon.iconset/icon_16x16@2x.png
    # ... (包含 32, 64, 128, 256, 512, 1024 所有尺寸)
    sips -z 1024 1024 icon-padded.png --out MyIcon.iconset/icon_512x512@2x.png
    ```

5.  **轉換為 `.icns`**: 使用 Apple 官方的 `iconutil` 工具完成轉換。

    ```bash
    iconutil -c icns MyIcon.iconset -o assets/EvoiClock.icns
    ```

6.  **清理**: 刪除 `icon-padded.png` 和 `MyIcon.iconset`。

---

## 階段四：打包與分發 (SOP)

### 使用 PyInstaller 打包

我們使用 `build.sh` 腳本來標準化打包流程。

```bash
# 確保腳本有執行權限
chmod +x build.sh

# 執行打包
./build.sh
```

`build.sh` 腳本的核心指令應如下：

```shell
#!/bin/sh

# ... (環境檢查) ...

APP_NAME="EvoiClock"
MAIN_SCRIPT="src/main.py"
ICON="assets/EvoiClock.icns"
VERSION="4.2.0" # 應從版本檔案讀取

# 清理舊的打包文件
rm -rf dist build *.spec

# 執行 PyInstaller
pyinstaller --name "$APP_NAME" \
            --windowed \
            --onefile \
            --icon="$ICON" \
            --add-data "cnlunar:cnlunar" \
            "$MAIN_SCRIPT"

# ... (可選的 DMG 製作流程) ...
```

---

## 階段五：倉庫與文件管理 (SOP)

- **README.md**: 專案的「門面」，應保持對**使用者**友好，簡潔介紹功能和安裝方法。
- **DEVELOPMENT_GUIDE.md**: 專案的「內部手冊」，詳細記錄所有**開發者**需要遵循的流程和標準。
- **.gitignore**: 必須包含 `_archive/`, `dist/`, `build/`, `*.spec`, `*.pyc`, `__pycache__/`, `*.DS_Store` 等。
- **Releases**: 所有提供給使用者下載的 `.dmg` 或 `.exe` 檔案，都必須在 GitHub 的 `Releases` 頁面進行發布，並附上該版本的更新日誌 (Changelog)。
