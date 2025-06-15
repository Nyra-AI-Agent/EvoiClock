# EVOI Trading Clock

## 專案概述

EVOI Trading Clock 是一個 Windows 桌面應用程序，提供交易時間顯示、紐約時間模式、交易名言等功能。

## 開發環境設置

### 必要條件
- Python 3.8+
- Docker Desktop
- Cursor IDE
- Git

### 安裝步驟

1. 克隆專案
```bash
git clone [repository_url]
cd evoi_clock
```

2. 安裝依賴
```bash
pip install -r requirements.txt
```

3. 運行開發環境
```bash
python main.py
```

## 開發流程

### 1. 本地開發 (macOS)
- 使用 Cursor IDE 進行開發
- 使用 Python + Tkinter 編寫代碼
- 使用 Git 進行版本控制

### 2. Docker 測試環境
```bash
# 構建 Docker 映像
docker build -t evoi-clock-test .

# 運行測試容器
docker-compose up
```

### 3. MCP 工具整合
- 使用 mcp_config.json 配置專案
- 自動化測試和部署
- 版本控制和配置管理

### 4. 打包流程
```bash
# 運行打包腳本
python build.py
```

## 專案結構

```
evoi_clock/
├── main.py              # 主程序入口
├── clock_widget.py      # 主時鐘組件
├── config_manager.py    # 配置管理
├── time_logic.py        # 時間狀態邏輯
├── animations.py        # 動畫效果
├── tray_manager.py      # 系統托盤
├── build.py            # 打包腳本
├── Dockerfile          # Docker 配置
├── docker-compose.yml  # Docker Compose 配置
├── mcp_config.json     # MCP 配置
├── config.json         # 用戶配置
├── requirements.txt    # 依賴清單
└── assets/            # 資源文件
    ├── icon.ico
    └── tray_icon.ico
```

## 功能說明

### 1. 時鐘模式
- 正常模式：顯示本地時間
- NYAM模式：顯示紐約時間，帶有特殊提醒
- 名言模式：顯示交易名言

### 2. 界面功能
- 拖拽移動
- 大小切換 (F11)
- 顯示/隱藏 (F12)
- 右鍵選單

### 3. 系統功能
- 系統托盤
- 開機自啟動
- 配置保存

## 開發指南

### 添加新功能
1. 在相應模組中添加代碼
2. 更新配置文件
3. 添加測試用例
4. 更新文檔

### 修改現有功能
1. 備份相關文件
2. 修改代碼
3. 運行測試
4. 更新文檔

### 打包發布
1. 更新版本號
2. 運行打包腳本
3. 測試安裝包
4. 發布更新

## 故障排除

### 常見問題
1. 窗口無法顯示
   - 檢查 Python 和 Tkinter 安裝
   - 檢查顯示設置

2. 系統托盤圖標不顯示
   - 檢查圖標文件
   - 檢查 pystray 安裝

3. 打包失敗
   - 檢查 PyInstaller 安裝
   - 檢查資源文件

### 日誌文件
- 位置：logs/app.log
- 級別：INFO/ERROR

## 版本歷史

### v1.0.0
- 初始版本
- 基本時鐘功能
- 三種模式支持
- 系統托盤集成

## 貢獻指南

1. Fork 專案
2. 創建特性分支
3. 提交更改
4. 推送到分支
5. 創建 Pull Request

## 授權協議

[授權協議說明]

## 聯繫方式

[聯繫信息] 