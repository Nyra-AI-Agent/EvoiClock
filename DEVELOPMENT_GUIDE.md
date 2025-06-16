# EvoiClock 專案開發指南
*(EvoiClock Project Development Guide)*

本文檔定義了 `EvoiClock` 專案及其衍生專案的標準開發流程 (SOP)。所有開發者，包括 AI 代理，都應嚴格遵守本指南，以確保程式碼品質、可維護性與協作效率。
*(This document defines the Standard Operating Procedures (SOP) for the `EvoiClock` project and its derivatives. All developers, including AI agents, must strictly adhere to this guide to ensure code quality, maintainability, and collaborative efficiency.)*

---

## 總覽：專案生命週期
*(Overview: Project Lifecycle)*

一個標準的 `EvoiClock` 專案開發週期包含以下五個核心階段：
*(A standard `EvoiClock` project development cycle consists of the following five core phases:)*

1.  **環境初始化 (Initialization)**
2.  **本地開發與版本控制 (Development & Git)**
3.  **資源處理 (Asset Handling)**
4.  **打包與分發 (Packaging & Distribution)**
5.  **倉庫與文件管理 (Repository & Documentation)**

---

## 階段一：環境初始化 (SOP)
*(Phase One: Environment Initialization - SOP)*

### 1. 取得專案
*(1. Obtain the Project)*

**禁止**直接在舊有或混亂的目錄上工作。永遠從一個乾淨的起點開始。
*(**Prohibited:** Working directly in old or messy directories. Always start from a clean slate.)*

```bash
# 1. 備份舊目錄 (如果有的話)
# (Backup the old directory, if any)
# mv ./evoi_clock ./evoi_clock_backup_YYYYMMDD

# 2. 從 GitHub 克隆最新的專案
# (Clone the latest project from GitHub)
git clone https://github.com/Nyra-AI-Agent/EvoiClock.git
cd EvoiClock
```

### 2. Conda 環境設置
*(2. Set up the Conda Environment)*

**禁止**在 `base` 環境中安裝任何專案依賴。
*(**Prohibited:** Installing any project dependencies in the `base` environment.)*

```bash
# 1. 建立一個專屬的 Conda 環境 (以 python 3.12 為例)
# (Create a dedicated Conda environment, e.g., with Python 3.12)
conda create --name tkpy python=3.12 -y

# 2. 啟動環境
# (Activate the environment)
conda activate tkpy

# 3. 安裝依賴
# (Install dependencies)
pip install -r requirements.txt
```
*註：`requirements.txt` 應只包含最小執行必要的套件。*
*(Note: `requirements.txt` should only contain the minimum necessary packages for execution.)*

### 3. 確認環境
*(3. Verify the Environment)*

在執行任何操作前，請務必確認目前處於正確的 Conda 環境。
*(Before any operation, always verify that you are in the correct Conda environment.)*

```bash
conda info --envs
```
*應該會看到 `tkpy` 前面有一個 `*` 號。*
*(You should see an asterisk `*` next to `tkpy`.)*

---

## 階段二：本地開發與版本控制 (SOP)
*(Phase Two: Local Development & Version Control - SOP)*

### 1. 目錄結構
*(1. Directory Structure)*

所有新功能開發都必須遵循以下標準目錄結構：
*(All new feature development must adhere to the following standard directory structure:)*

```
EvoiClock/
├── .gitignore
├── README.md           
├── DEVELOPMENT_GUIDE.md  # 開發指南 (本文件) (Development Guide - this file)
├── requirements.txt      
├── build.sh              # macOS 打包腳本 (macOS packaging script)
│
├── src/                  # 所有 Python 原始碼 (All Python source code)
│   └── main.py           
│
└── assets/               # 所有非程式碼資源 (All non-code assets)
    ├── EvoiClock.icns    # 標準 macOS 應用程式圖示 (Standard macOS app icon)
    └── Antonio-Regular.ttf # 專案字體 (Project font)
```

### 2. 主程式入口
*(2. Main Program Entry Point)*

- 唯一的程式入口檔案為 `src/main.py`。
  *(The single entry point file is `src/main.py`.)*
- 所有新的程式碼都應該以模組化的方式在 `src/` 目錄下建立，並由 `main.py` 進行呼叫。
  *(All new code should be created modularly within the `src/` directory and called by `main.py`.)*

### 3. Git 版本控制流程
*(3. Git Version Control Workflow)*

我們採用功能分支 (Feature Branch) 的工作流程。
*(We adopt a Feature Branch workflow.)*

```bash
# 1. 確保在主分支，並拉取最新變更
# (Ensure you are on the main branch and pull the latest changes)
git checkout main
git pull origin main

# 2. 為新功能建立一個描述性的分支
# (Create a descriptive branch for the new feature)
git checkout -b feat/add-new-quote-animation

# 3. 在新分支上進行開發和修改...
# (Develop and make changes on the new branch...)

# 4. 完成開發後，提交有意義的 Commit
# (After development, make a meaningful commit)
git add .
git commit -m "feat(animation): Add fade-in effect for quote transition"

# 5. 推送到遠端
# (Push to the remote repository)
git push origin feat/add-new-quote-animation

# 6. 在 GitHub 上建立 Pull Request，請求合併到 main 分支
# (Create a Pull Request on GitHub to merge into the main branch)
```
**Commit 訊息規範**: 我們遵循 [Conventional Commits](https://www.conventionalcommits.org/) 規範，格式為 `type(scope): description`。
*(**Commit Message Convention**: We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification. The format is `type(scope): description`.)*
- `feat`: 新功能 (A new feature)
- `fix`: 修復 Bug (A bug fix)
- `docs`: 文件變更 (Documentation changes)
- `style`: 程式碼風格調整 (不影響功能) (Code style adjustments without functional changes)
- `refactor`: 重構 (Code refactoring)
- `chore`: 建置流程、輔助工具的變動 (Changes to the build process or auxiliary tools)

---

## 階段三：資源處理 (SOP)
*(Phase Three: Asset Handling - SOP)*

### 製作標準 macOS 圖示 (`.icns`)
*(Creating a Standard macOS Icon - .icns)*

為確保應用程式在 macOS Dock 中顯示完美，必須使用帶有**透明邊距**的標準 `.icns` 檔案。
*(To ensure the application displays perfectly in the macOS Dock, a standard `.icns` file with **transparent padding** must be used.)*

**禁止**直接使用未經處理的 `.png` 作為圖示。
*(**Prohibited:** Directly using an unprocessed `.png` as the icon.)*

**操作流程 (Workflow):**
1.  **準備母版圖示 (Prepare Master Icon)**: 準備一張 `1024x1024` 像素的透明背景 `.png` 圖示母版 (例如 `icon_master.png`)。
    *(Prepare a `1024x1024` pixel master icon file (`.png`) with a transparent background (e.g., `icon_master.png`).)*

2.  **增加透明邊距 (Add Transparent Padding)**: 使用 `ImageMagick` (需先用 `brew install imagemagick` 安裝) 為母版增加邊距。此步驟至關重要。
    *(Use `ImageMagick` (install via `brew install imagemagick`) to add padding to the master icon. This step is critical.)*
    ```bash
    # 將 1024px 的母版縮小到 820px，並置於一個 1024px 的透明畫布中央
    # (Resize the 1024px master to 820px and place it in the center of a 1024px transparent canvas)
    magick convert -size 1024x1024 xc:none \
      \( icon_master.png -resize 820x820 \) \
      -gravity center -composite \
      icon-padded.png
    ```

3.  **建立 `iconset` 資料夾 (Create `iconset` Folder):**
    ```bash
    # 清理舊的，建立新的 (Clean up the old, create a new one)
    rm -rf MyIcon.iconset
    mkdir MyIcon.iconset
    ```

4.  **生成所有尺寸 (Generate All Sizes)**: 使用 `sips` 指令，以帶邊距的圖示 (`icon-padded.png`) 生成所有 Apple 需要的尺寸。
    *(Use the `sips` command with the padded icon (`icon-padded.png`) to generate all sizes required by Apple.)*
    ```bash
    sips -z 16 16     icon-padded.png --out MyIcon.iconset/icon_16x16.png
    sips -z 32 32     icon-padded.png --out MyIcon.iconset/icon_16x16@2x.png
    # ... (包含 32, 64, 128, 256, 512, 1024 所有尺寸)
    # ... (include all sizes: 32, 64, 128, 256, 512, 1024)
    sips -z 1024 1024 icon-padded.png --out MyIcon.iconset/icon_512x512@2x.png
    ```

5.  **轉換為 `.icns` (Convert to `.icns`)**: 使用 Apple 官方的 `iconutil` 工具完成轉換。
    *(Use Apple's official `iconutil` tool to complete the conversion.)*
    ```bash
    iconutil -c icns MyIcon.iconset -o assets/EvoiClock.icns
    ```

6.  **清理 (Cleanup)**: 刪除 `icon-padded.png` 和 `MyIcon.iconset`。
    *(Delete `icon-padded.png` and `MyIcon.iconset`.)*

---

## 階段四：打包與分發 (SOP)
*(Phase Four: Packaging & Distribution - SOP)*

我們的標準打包工具是 `PyInstaller`。它同時用於本地 macOS 打包和雲端 Windows 自動化打包，以確保邏輯的統一性。
*(Our standard packaging tool is `PyInstaller`. It is used for both local macOS packaging and automated cloud-based Windows packaging to ensure logical consistency.)*

### macOS 本地打包
*(macOS Local Build)*

macOS 的本地打包透過 `build.sh` 腳本執行，該腳本對 `PyInstaller` 的打包流程進行了標準化。
*(Local packaging for macOS is executed via the `build.sh` script, which standardizes the `PyInstaller` workflow.)*

**操作流程 (Workflow):**
```bash
# 1. 啟動正確的 Conda 環境
# (Activate the correct Conda environment)
conda activate tkpy

# 2. 確保腳本有執行權限
# (Ensure the script has execute permissions)
chmod +x build.sh

# 3. 執行打包
# (Execute the packaging script)
./build.sh
```

`build.sh` 腳本的核心 `pyinstaller` 指令應遵循以下範本，以確保所有資源都被正確包含：
*(The core `pyinstaller` command within `build.sh` should follow this template to ensure all assets are correctly included:)*
```shell
# 這是指令範本，實際腳本中可能包含更多如清理、路徑檢查等輔助指令
# (This is a command template; the actual script may contain additional helper commands like cleanup, path checks, etc.)

pyinstaller --noconfirm --windowed --onefile \
    --name "EvoiClock" \
    --icon "assets/EvoiClock.icns" \
    --add-data "src/cnlunar:cnlunar" \
    --add-data "assets:assets" \
    "src/main.py"
```

### Windows 自動化打包 (CI/CD)
*(Windows Automated Build - CI/CD)*

Windows 的 `.exe` 應用程式是透過位於 `.github/workflows/build-windows.yml` 的 GitHub Actions 工作流程**自動建置**的。
*(The Windows `.exe` application is **automatically built** via the GitHub Actions workflow located at `.github/workflows/build-windows.yml`.)*

**運作方式 (How it works):**
1.  當有新的程式碼被推送到 `main` 分支時，此工作流程會自動觸發。
    *(When new code is pushed to the `main` branch, this workflow is triggered automatically.)*
2.  它會在一個由 GitHub 提供的 Windows 虛擬環境中啟動，並安裝 Python 3.12 及所有依賴。
    *(It runs in a Windows virtual environment provided by GitHub, installing Python 3.12 and all dependencies.)*
3.  流程會使用 `Pillow` 函式庫，將標準的 `.icns` 圖示即時轉換為 Windows 需要的 `.ico` 格式。
    *(The process uses the `Pillow` library to convert the standard `.icns` icon into the `.ico` format required by Windows on the fly.)*
4.  最後，它會執行與 macOS 邏輯一致的 `PyInstaller` 指令，生成 `EvoiClock.exe`。
    *(Finally, it executes a `PyInstaller` command, consistent with the macOS logic, to generate `EvoiClock.exe`.)*
5.  打包完成的 `.exe` 檔案會被上傳到該次 Action 的「Artifacts」(產出物) 中，供開發者下載。
    *(The packaged `.exe` file is uploaded as an "Artifact" of the Action run, ready for download.)*

**如何取得 Windows 版本 (How to get the Windows version):**
1.  在 GitHub 倉庫頁面，點擊「Actions」分頁。
    *(On the GitHub repository page, click the "Actions" tab.)*
2.  選擇「Build EvoiClock for Windows」工作流程。
    *(Select the "Build EvoiClock for Windows" workflow.)*
3.  點擊最近一次成功運行的紀錄 (綠色勾號)。
    *(Click the latest successful run (with a green checkmark).)*
4.  在頁面下方的「Artifacts」區塊，點擊「EvoiClock-windows-exe」即可下載。
    *(In the "Artifacts" section at the bottom of the page, click "EvoiClock-windows-exe" to download.)*

---

## 階段五：倉庫與文件管理 (SOP)
*(Phase Five: Repository & Documentation - SOP)*

- **README.md**: 專案的「門面」，應保持對**使用者**友好，簡潔介紹功能和安裝方法。
  *(The "front door" of the project. It should be kept user-friendly, briefly introducing features and installation methods.)*
- **DEVELOPMENT_GUIDE.md**: 專案的「內部手冊」，詳細記錄所有**開發者**需要遵循的流程和標準。
  *(The "internal manual" of the project. It details all the processes and standards that **developers** must follow.)*
- **.gitignore**: 必須包含 `_archive/`, `dist/`, `build/`, `*.spec`, `*.pyc`, `__pycache__/`, `*.DS_Store` 等。
  *(Must include `_archive/`, `dist/`, `build/`, `*.spec`, `*.pyc`, `__pycache__/`, `*.DS_Store`, etc.)*
- **Releases**: 所有提供給使用者下載的 `.dmg` 或 `.exe` 檔案，都必須在 GitHub 的 `Releases` 頁面進行發布，並附上該版本的更新日誌 (Changelog)。
  *(All downloadable files for users (like `.dmg` or `.exe`) must be published on the GitHub `Releases` page, accompanied by a changelog for that version.)*
