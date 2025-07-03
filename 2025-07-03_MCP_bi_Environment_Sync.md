---
title: "MCP雙平台環境同步策略與執行計畫"
description: "Windows與macOS MCP環境統一部署與EvoiClock跨平台開發優化方案"
created: 2025-07-03
updated: 2025-07-03
tags: 
  - MCP
  - 跨平台開發
  - EvoiClock
  - 環境同步
  - Windows
  - macOS
category: "技術部署"
priority: "高"
status: "規劃中"
related_projects:
  - EvoiClock
  - XYSB-Lab
dependencies:
  - Claude Desktop
  - Node.js
  - Python
platforms:
  - Windows 10/11
  - macOS (M2)
---

# 🔄 MCP雙平台環境同步策略與執行計畫

## 📚 **相關文檔參考**

### **Background References**
- 📄 [Windows MCP服務器部署指南](./2025-06-29-Windows-MCP_Deployment_Guide_RESTORED.md) - Windows環境7服務器完整部署方案
- 📄 [MacBook Air M2環境設定記錄](./2025-07-01_MCP_MacbookAir2M2_Environment_Setup_Record.md) - macOS基礎MCP環境與技術棧分析

---

## 📋 **檔案內容分析**

### 🪟 **Windows MCP部署指南特點**
- **目標**: 部署7個官方MCP服務器到Windows環境
- **核心策略**: 使用 `C:\Users\XYZ\global-scripts` 路徑避開Obsidian Sync衝突
- **系統規格**: i7-13700H、32GB RAM、強大硬體配置
- **服務器清單**: 7個服務器（4個TypeScript + 3個Python）

### 💻 **MacBook Air M2環境記錄特點**
- **當前狀態**: 基礎MCP環境已完成（3個服務器）
- **技術棧**: Node.js v24.1.0、Docker完整環境、多個conda環境
- **擴展建議**: Playwright MCP、Sequential Thinking MCP

## 🎯 **環境狀況澄清 (2025-07-03更新)**

### **✅ 實際部署狀況** *(UPDATED: 2025-07-03 22:00)*
```yaml
macOS環境 (MacBook Air M2 - 主要開發平台):
  現況: ✅ 完整9個MCP服務器部署完成 (PRODUCTION READY)
  角色: 🎯 主要規劃與測試平台
  策略: ✅ 已成功建立標準配置模板
  詳細配置:
    - 官方7個: filesystem, memory, everything, sequentialthinking, fetch, git, time
    - 專用2個: task-master-ai, obsidian-xysb
    - 路徑: /Users/xy2024air15/.xykms/mcp-servers/
    - 配置: Cursor + Claude Desktop 完整更新
  
Windows環境:
  現況: 🚨 URGENT ACTION REQUIRED - 完全未開始任何MCP部署
  角色: 📋 跟進實施平台  
  策略: 基於macOS成功模板立即執行
  風險: 🔴 HIGH - 跨平台開發環境嚴重不同步
  
部署狀況:
  ✅ 1️⃣ macOS環境完善 (已完成)
  ✅ 2️⃣ 建立標準配置模板 (已完成)
  🚨 3️⃣ Windows環境按模板部署 (URGENT - 24小時內完成)
  ⏳ 4️⃣ 雙平台驗證與測試 (待Windows完成後執行)
```

### **🔄 修正版策略重點**
```yaml
階段重新定義:
  階段1: macOS環境標準化 (7個MCP服務器統一部署)
  階段2: 建立跨平台配置模板  
  階段3: Windows環境按模板實施
  階段4: 雙平台測試與驗證
  
當前重點:
  🎯 集中資源完善macOS環境
  📋 建立可復制的部署標準
  🚀 確保後續Windows部署的順利性
```

## 🎯 **關鍵發現與建議**

### ✅ **優勢分析**
1. **雙平台策略清晰**: Windows和macOS各有完整部署方案
2. **路徑策略智能**: Windows使用global-scripts避免同步衝突
3. **硬體條件充足**: 兩台電腦都具備強大的MCP服務器運行能力

### ⚠️ **潛在問題識別**

#### **1. 服務器數量不一致**
- **Windows**: 7個MCP服務器
- **macOS**: 3個MCP服務器  
- **風險**: 開發環境不一致可能導致功能差異
- **建議**: 統一MCP服務器配置，確保跨平台一致性

#### **2. 配置管理複雜性 (✅ 已解決)**
- **原始理解**: 兩套不同的配置檔案和路徑策略
- **澄清後**: .xykms目錄完全對應Windows的global-scripts
- **現況**: 路徑策略完全統一，配置格式100%相同
- **優勢**: 維護複雜性大幅降低，配置漂移風險消除

#### **3. 同步策略已優化 (✅ 已解決)**
- **原始擔憂**: "Windows使用global-scripts避開同步，macOS直接在XYSB目錄"
- **澄清後現況**: 兩平台都使用獨立目錄(.xykms ↔ global-scripts)
- **統一策略**: 完全避開Obsidian Sync，跨平台工作流程統一
- **實施**: 所有MCP服務器統一安裝至平台對應的獨立目錄

## 🚀 **整合優化建議**

### **階段1: 環境對齊** 
```yaml
目標: 讓兩台電腦的MCP能力一致

Windows環境驗證:
  - 確認7個服務器正常運行
  - 驗證EvoiClock專案相關MCP功能
  - 測試Claude Desktop響應性能

macOS環境補強 (修正版 - 統一.xykms部署):
  - 使用.xykms目錄對應Windows的global-scripts策略
  - 安裝完整7個MCP服務器:
    - filesystem (檔案系統操作)
    - memory (知識圖譜持久化記憶)
    - everything (參考/測試服務器) 
    - sequentialthinking (結構化思維)
    - fetch (網頁內容抓取轉換)
    - git (Git倉庫操作)
    - time (時間和時區轉換)
  - 確保與Windows相同的7服務器配置
  - 性能基準測試
```

### **階段2: EvoiClock跨平台開發優化**
```yaml
Mac開發環境:
  - 主要開發: EvoiClock Python程式
  - 容器測試: Docker + MCP輔助
  - 版本控制: Git + MCP git服務器
  - 字體管理: 跨平台字體系統驗證

Windows建置環境:
  - 最終打包: PyInstaller .exe建置
  - MCP輔助: 自動化建置流程
  - 測試驗證: Windows特定功能測試
  - 最終用戶測試: .exe檔案分發驗證
```

### **階段3: 自動化工作流**
```yaml
跨平台同步:
  - 標準化MCP配置檔案
  - 自動化部署腳本
  - 統一的開發→測試→建置流程

EvoiClock特定:
  - MCP輔助容器化開發
  - 自動化Windows建置
  - 跨平台字體管理驗證
  - 端到端測試自動化
```

## 📊 **詳細執行計畫**

### **🔥 階段1執行步驟 (立即執行)**

#### **macOS環境補強具體指令 (修正版 - 統一.xykms部署)**
```bash
# 1. 切換到.xykms目錄 (對應Windows的global-scripts)
cd "/Users/xy2024air15/.xykms"

# 2. 克隆官方MCP服務器倉庫
git clone https://github.com/modelcontextprotocol/servers.git mcp-servers
cd mcp-servers

# 3. 安裝Node.js依賴並構建TypeScript服務器
npm install
npm run build

# 4. 安裝uv (Python包管理器) 
pip install uv

# 5. 為Python服務器創建虛擬環境
cd src/fetch && uv sync && cd ../..
cd src/git && uv sync && cd ../..  
cd src/time && uv sync && cd ../..
```

**原始指令 (已修正)**:
```bash
# ❌ 原始建議 (npm global + 分散安裝)
# npm install -g @modelcontextprotocol/server-memory
# npm install -g @modelcontextprotocol/server-everything
# cd ~/temp-mcp-setup && git clone...

# ✅ 修正建議 (統一.xykms部署)
# 透過上述統一部署指令獲得所有7個MCP服務器
```

#### **Claude Desktop設定 (統一配置檔案)**
**位置**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**統一配置 (macOS修正版 - 對應Windows格式)**:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "node",
      "args": ["/Users/xy2024air15/.xykms/mcp-servers/src/filesystem/dist/index.js", "/Users/xy2024air15/Documents/XYSB"],
      "env": {}
    },
    "memory": {
      "command": "node", 
      "args": ["/Users/xy2024air15/.xykms/mcp-servers/src/memory/dist/index.js"],
      "env": {}
    },
    "everything": {
      "command": "node",
      "args": ["/Users/xy2024air15/.xykms/mcp-servers/src/everything/dist/index.js"],
      "env": {}
    },
    "sequentialthinking": {
      "command": "node",
      "args": ["/Users/xy2024air15/.xykms/mcp-servers/src/sequentialthinking/dist/index.js"],
      "env": {}
    },
    "fetch": {
      "command": "uv",
      "args": ["--directory", "/Users/xy2024air15/.xykms/mcp-servers/src/fetch", "run", "mcp-server-fetch"],
      "env": {}
    },
    "git": {
      "command": "uv", 
      "args": ["--directory", "/Users/xy2024air15/.xykms/mcp-servers/src/git", "run", "mcp-server-git"],
      "env": {}
    },
    "time": {
      "command": "uv",
      "args": ["--directory", "/Users/xy2024air15/.xykms/mcp-servers/src/time", "run", "mcp-server-time"],
      "env": {}
    }
  }
}
```

### **⚠️ 風險評估與應對策略**

#### **潛在風險**
```yaml
配置衝突風險:
  - 風險: 新增MCP服務器可能與現有配置產生衝突
  - 應對: 在修改前完整備份claude_desktop_config.json
  - 驗證: 逐一添加服務器並測試

性能影響風險:
  - 風險: 7個MCP服務器同時運行可能影響系統性能
  - 應對: 監控系統資源使用情況
  - 基準: MacBook Air M2應能輕鬆處理(<1GB總記憶體使用)

Python環境風險:
  - 風險: uv sync可能與現有conda環境產生衝突
  - 應對: 使用獨立目錄安裝，避免影響現有環境
  - 隔離: ~/temp-mcp-setup作為臨時安裝目錄
```

#### **回滾策略**
```bash
# 如果新配置出現問題，快速回滾
cp "~/Library/Application Support/Claude/claude_desktop_config.json.backup.$(date +%Y%m%d)" \
   "~/Library/Application Support/Claude/claude_desktop_config.json"

# 清理臨時安裝
rm -rf ~/temp-mcp-setup

# 重啟Claude Desktop
killall Claude
open -a Claude
```

### **✅ 成功標準與驗證清單**

#### **階段1完成標準**
- [ ] macOS Claude Desktop成功識別7個MCP服務器
- [ ] 每個MCP服務器都能正常響應基本指令
- [ ] 系統記憶體使用增量<500MB
- [ ] Claude Desktop啟動時間<10秒
- [ ] 所有服務器狀態為"已連接"

#### **功能驗證測試**
```yaml
基礎功能測試:
  filesystem: 
    - 測試: 建立/讀取/刪除檔案
    - 預期: 成功操作EvoiClock目錄
  
  memory:
    - 測試: 儲存/查詢知識片段
    - 預期: 成功記憶EvoiClock開發記錄
  
  git:
    - 測試: 查詢EvoiClock倉庫狀態
    - 預期: 正確顯示分支和提交資訊
  
  time:
    - 測試: 時區轉換查詢
    - 預期: 正確轉換台灣/美國時間
  
  fetch:
    - 測試: 抓取網頁內容
    - 預期: 成功獲取Python相關技術文檔

EvoiClock整合測試:
  - 測試: 使用MCP工具分析main.py結構  
  - 測試: 透過git MCP檢查專案歷史
  - 測試: 用memory MCP記錄開發決策
  - 預期: 所有測試通過，MCP工具能有效輔助EvoiClock開發
```

## 📊 **資源消耗與性能預估**

### **硬體需求對比**
| 項目 | Windows (i7-13700H) | macOS (M2) | 建議 |
|------|-------------------|------------|------|
| MCP服務器 | 7個 (~715MB) | 3個→7個 (~715MB) | ✅ 兩者都綽綽有餘 |
| 開發負載 | 中等 | 高 (主要開發) | ✅ 硬體充足 |
| 容器化 | 支援 | 原生支援 | ✅ 跨平台容器化可行 |
| Claude響應 | <2秒 | <2秒 | ✅ 性能目標 |

### **記憶體使用預估**
```yaml
當前macOS (3個服務器): ~250MB
目標macOS (7個服務器): ~715MB  
可用記憶體: 24GB (M2 Unified Memory)
使用率影響: <3% (完全可接受)
```

## 🎯 **立即行動建議**

### **🔥 最高優先級 (今日執行)**
1. **macOS環境補強**: 安裝缺失的4個MCP服務器，達到與Windows相同的7服務器配置
2. **配置驗證**: 確保所有7個服務器在macOS上正常運行
3. **基礎功能測試**: 驗證每個MCP服務器的核心功能

### **🔧 中期優化 (本週完成)**
1. **EvoiClock MCP整合**: 驗證當前MCP工具對EvoiClock開發的支援程度
2. **性能基準建立**: 記錄7服務器環境的性能基準
3. **標準化配置**: 建立跨平台MCP配置模板

### **🌟 長期願景 (2週內)**
1. **自動化腳本**: 建立EvoiClock跨平台建置自動化
2. **完整工作流**: Mac開發 → Docker測試 → Windows建置的無縫流程
3. **MCP生態**: 為EvoiClock建立專屬的MCP工具鏈

## 📈 **進度追蹤**

### **當前狀態**
- ✅ Windows: 7個MCP服務器部署方案完成
- ✅ macOS: 3個MCP服務器基礎環境已建立
- 🔄 進行中: macOS環境補強至7服務器
- ⏳ 待執行: EvoiClock專案MCP整合驗證

### **下一步行動**
1. **立即執行**: macOS補強4個MCP服務器
2. **驗證測試**: 完整功能測試清單
3. **整合測試**: EvoiClock開發工作流驗證

---

## 🔗 **相關資源**

### **技術文檔**
- [MCP Protocol官方文檔](https://modelcontextprotocol.io/)
- [Claude Desktop MCP設定指南](https://claude.ai/docs/mcp)
- [EvoiClock專案文檔](./README.md)

### **工具連結**
- [官方MCP服務器倉庫](https://github.com/modelcontextprotocol/servers)
- [Python uv包管理器](https://github.com/astral-sh/uv)
- [Node.js官方網站](https://nodejs.org/)

---

**文檔建立**: 2025-07-03 09:45  
**最後更新**: 2025-07-03 (路徑策略澄清與統一部署方案)  
**執行環境**: Windows (已完成) + MacBook Air M2 (待補強)  
**目標**: 雙平台MCP環境完全一致

**更新記錄**:
- **v1.0** (2025-07-03 09:45): 初始雙平台MCP環境同步策略分析
- **v1.1** (2025-07-03): 路徑策略澄清，統一.xykms部署方案，與Windows策略100%對應