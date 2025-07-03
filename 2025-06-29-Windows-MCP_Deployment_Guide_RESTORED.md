---
title: "Windows MCP服务器部署指南 (RESTORED)"
description: "Windows環境7個官方MCP服務器完整部署方案，使用global-scripts路徑策略"
created: 2025-06-29
updated: 2025-07-03
author: "Claude (小西)"
tags: 
  - MCP
  - Windows部署
  - 7個MCP服務器
  - global-scripts策略
  - Windows環境
  - 跨平台路徑對應
  - Claude Desktop
  - Node.js
  - Python
  - PowerShell
category: "部署指南"
priority: "高"
status: "指南完成"
version: "1.1"
related_projects:
  - EvoiClock
  - XYSB-Lab
  - MCP服務器部署
platforms:
  - Windows 10/11
target_servers:
  - filesystem
  - memory
  - everything
  - sequentialthinking
  - fetch
  - git
  - time
deployment_path: "C:\\Users\\XYZ\\global-scripts\\mcp-servers"
system_requirements:
  - cpu: "13th Gen Intel i7-13700H"
  - memory: "32GB"
  - storage: "931.8GB SSD"
  - nodejs: "v24.3.0"
  - python: "3.12.3"
related_documents:
  - "[[2025-07-03_MCP_Cross-Platform_Integration_Strategy]]"
  - "[[2025-07-01_MCP_MacbookAir2M2_Environment_Setup_Record]]"
  - "[[2025-07-03_MCP_bi_Environment_Sync]]"
cross_platform_mapping:
  windows: "C:\\Users\\XYZ\\global-scripts"
  macos: "/Users/xy2024air15/.xykms"
---

# 🪟 Windows MCP服务器部署指南 (RESTORED)

> **文檔版本**: 1.2 (2025-07-03 緊急行動要求)  
> **原始建立**: 2025-06-29  
> **更新**: 2025-07-03 22:00 (基於macOS成功模板緊急更新)  
> **執行環境**: Windows + 9個MCP服務器  
> **對應環境**: macOS (.xykms目錄對應策略)

## 🚨 **緊急行動要求 (IMMEDIATE ACTION REQUIRED)**

### **⚠️ 關鍵狀況更新 (2025-07-03 22:00)**
```yaml
macOS狀況:
  ✅ 完整9個MCP服務器部署完成 (PRODUCTION READY)
  ✅ 全部功能驗證通過
  ✅ 路徑: /Users/xy2024air15/.xykms/mcp-servers/
  
Windows狀況:
  ❌ 尚未開始任何MCP服務器部署
  🚨 需要立即執行完整9個服務器建置
  ⏰ 24小時內必須完成以保持跨平台同步

風險評估:
  🔴 HIGH RISK: 延遲將導致開發環境不同步
  🔴 影響項目協作效率與跨平台開發流程
  🔴 可能造成配置分歧和維護複雜度增加
```

### **🎯 立即執行清單 (Windows Team)**

#### **Phase 1: 立即克隆與建置 (0-30分鐘)**
```cmd
# 1. 導航至目標目錄
cd C:\Users\[USERNAME]\global-scripts\

# 2. 克隆官方倉庫 (按照macOS成功模式)
git clone https://github.com/modelcontextprotocol/servers.git mcp-servers
cd mcp-servers

# 3. 建置TypeScript服務器 (按照macOS驗證方式)
npm install && npm run build

# 4. 驗證建置結果
dir src\filesystem\dist\index.js
dir src\memory\dist\index.js
dir src\everything\dist\index.js
dir src\sequentialthinking\dist\index.js
```

#### **Phase 2: Python環境設置 (30-60分鐘)**
```cmd
# 創建Python虛擬環境 (使用conda，按照macOS模式)
cd src\fetch
conda create -p .\venv python=3.10 -y
.\venv\Scripts\activate
pip install -e .

cd ..\git
conda create -p .\venv python=3.10 -y
.\venv\Scripts\activate
pip install -e .

cd ..\time
conda create -p .\venv python=3.10 -y
.\venv\Scripts\activate
pip install -e .
```

#### **Phase 3: 配置更新 (60-90分鐘)**
- 更新Cursor MCP配置文件 (.cursor/mcp.json)
- 配置所有9個服務器（7個官方 + 2個專用）
- 重啟Cursor IDE並測試功能

#### **Phase 4: 驗證與報告 (90-120分鐘)**  
- 測試所有MCP工具可用性
- 特別驗證time, everything, sequentialthinking功能
- 更新部署狀態文檔

## 🔄 **跨平台路徑對應關係 (2025-07-03新增)**

### **✅ 統一部署策略**
```yaml
Windows環境:
  全域工具目錄: C:\Users\XYZ\global-scripts
  MCP服務器位置: C:\Users\XYZ\global-scripts\mcp-servers
  
macOS對應環境:
  全域工具目錄: /Users/xy2024air15/.xykms  # ← 對應global-scripts
  MCP服務器位置: /Users/xy2024air15/.xykms/mcp-servers
  
統一配置格式:
  - 兩平台使用相同的7個MCP服務器
  - 相同的配置檔案結構 (僅路徑不同)
  - 相同的依賴管理方式 (npm + uv)
```

### **🎯 跨平台一致性優勢**
- **避免同步衝突**: 兩平台都使用獨立於筆記庫的目錄
- **配置統一**: 相同的服務器清單和依賴管理
- **維護簡化**: 單一配置模板適用兩平台
- **開發無縫**: Windows開發 ↔ macOS開發完全一致

## 🎯 **关键发现: global-scripts路径**

### **Windows PATH环境变量中的黄金路径**
```
C:\Users\XYZ\global-scripts    # 用戶自定義腳本 (已在PATH中)
```

### **为什么这是最佳选择**
- ✅ **已在PATH中** - 无需额外配置
- ✅ **用户习惯** - 符合既有工具管理模式  
- ✅ **避开同步** - 完全独立于XYSB/Obsidian vault
- ✅ **权限友好** - 用户目录，无需管理员权限
- ✅ **集中管理** - 所有自定义工具统一位置

## 🚀 **快速部署脚本** (PowerShell)

### **一键部署命令**
```powershell
# 1. 切换到global-scripts目录
cd "C:\Users\XYZ\global-scripts"

# 2. 克隆官方MCP服务器仓库
git clone https://github.com/modelcontextprotocol/servers.git mcp-servers
cd mcp-servers

# 3. 安装Node.js依赖并构建TypeScript服务器
npm install
npm run build

# 4. 安装uv (Python包管理器)
pip install uv

# 5. 为Python服务器创建虚拟环境
cd src/fetch && uv sync && cd ../..
cd src/git && uv sync && cd ../..  
cd src/time && uv sync && cd ../..
```

## 📋 **完整Claude Desktop配置**

### **配置文件路径**
```
%APPDATA%\Claude\claude_desktop_config.json
```

### **完整9個服務器配置 (基於macOS成功模板)**
```json
{
  "mcpServers": {
    "task-master-ai": {
      "command": "npx",
      "args": ["-y", "--package=task-master-ai", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "ANTHROPIC_API_KEY_HERE",
        "PERPLEXITY_API_KEY": "PERPLEXITY_API_KEY_HERE",
        "OPENAI_API_KEY": "OPENAI_API_KEY_HERE",
        "GOOGLE_API_KEY": "GOOGLE_API_KEY_HERE",
        "XAI_API_KEY": "XAI_API_KEY_HERE",
        "OPENROUTER_API_KEY": "OPENROUTER_API_KEY_HERE",
        "MISTRAL_API_KEY": "MISTRAL_API_KEY_HERE",
        "AZURE_OPENAI_API_KEY": "AZURE_OPENAI_API_KEY_HERE",
        "OLLAMA_API_KEY": "OLLAMA_API_KEY_HERE"
      }
    },
    "obsidian-xysb": {
      "command": "npx",
      "args": ["-y", "mcp-obsidian", "C:\\Users\\[USERNAME]\\Documents\\XYSB"],
      "env": {
        "OBSIDIAN_API_KEY": "YOUR_OBSIDIAN_API_KEY_HERE",
        "OBSIDIAN_HOST": "127.0.0.1",
        "OBSIDIAN_PORT": "27124"
      }
    },
    "filesystem": {
      "command": "node",
      "args": ["C:\\Users\\[USERNAME]\\global-scripts\\mcp-servers\\src\\filesystem\\dist\\index.js", "C:\\Users\\[USERNAME]\\global-scripts\\"],
      "env": {}
    },
    "memory": {
      "command": "node",
      "args": ["C:\\Users\\[USERNAME]\\global-scripts\\mcp-servers\\src\\memory\\dist\\index.js"],
      "env": {}
    },
    "everything": {
      "command": "node", 
      "args": ["C:\\Users\\[USERNAME]\\global-scripts\\mcp-servers\\src\\everything\\dist\\index.js"],
      "env": {}
    },
    "sequentialthinking": {
      "command": "node",
      "args": ["C:\\Users\\[USERNAME]\\global-scripts\\mcp-servers\\src\\sequentialthinking\\dist\\index.js"],
      "env": {}
    },
    "fetch": {
      "command": "C:\\Users\\[USERNAME]\\global-scripts\\mcp-servers\\src\\fetch\\venv\\Scripts\\python.exe",
      "args": ["-m", "mcp_server_fetch"],
      "cwd": "C:\\Users\\[USERNAME]\\global-scripts\\mcp-servers\\src\\fetch",
      "env": {}
    },
    "git": {
      "command": "C:\\Users\\[USERNAME]\\global-scripts\\mcp-servers\\src\\git\\venv\\Scripts\\python.exe", 
      "args": ["-m", "mcp_server_git", "C:\\Users\\[USERNAME]\\global-scripts\\"],
      "cwd": "C:\\Users\\[USERNAME]\\global-scripts\\mcp-servers\\src\\git",
      "env": {}
    },
    "time": {
      "command": "C:\\Users\\[USERNAME]\\global-scripts\\mcp-servers\\src\\time\\venv\\Scripts\\python.exe",
      "args": ["-m", "mcp_server_time"],
      "cwd": "C:\\Users\\[USERNAME]\\global-scripts\\mcp-servers\\src\\time", 
      "env": {}
    }
  }
}
```

#### **配置說明**
- **總計9個服務器**: 7個官方 + 2個專用
- **路徑模板**: 使用 `[USERNAME]` 占位符，實際使用時替換為具體用戶名
- **API Keys**: 需要配置相應的API密鑰
- **Virtual Environment**: Python服務器使用conda創建的虛擬環境路徑

## 🛠️ **系统环境信息**

### **Windows系统规格**
- **CPU**: 13th Gen Intel i7-13700H (14核20线程)
- **内存**: 32GB
- **存储**: 931.8GB SSD 
- **系统**: Windows 10 Home Build 26100
- **Node.js**: v24.3.0
- **Python**: 3.12.3

### **MCP服务器列表**
1. **filesystem** - 安全文件操作 (TypeScript)
2. **memory** - 知识图谱持久化记忆 (TypeScript)
3. **everything** - 参考/测试服务器 (TypeScript)
4. **sequentialthinking** - 动态反思问题解决 (TypeScript)
5. **fetch** - 网页内容抓取转换 (Python)
6. **git** - Git仓库操作 (Python)
7. **time** - 时间和时区转换 (Python)

## 💾 **资源消耗预估**
- **filesystem**: ~50MB
- **memory**: ~80MB  
- **fetch**: ~120MB
- **git**: ~70MB
- **time**: ~45MB
- **everything**: ~150MB
- **sequentialthinking**: ~200MB
- **总计**: ~715MB (32GB系统轻松支持)

## 🔧 **故障排除**

### **常见问题**
1. **npm找不到包**: 使用GitHub克隆而非npm install
2. **uv命令不存在**: 运行 `pip install uv`
3. **Node.js PATH问题**: 添加 `C:\Program Files\nodejs` 到PATH
4. **Python虚拟环境失败**: 确认Python 3.12.x已安装

### **验证部署**
```powershell
# 检查部署结果
Test-Path "C:\Users\XYZ\global-scripts\mcp-servers\src\filesystem\dist\index.js"
Test-Path "C:\Users\XYZ\global-scripts\mcp-servers\src\fetch\.venv\Scripts\python.exe"

# 检查Claude配置
Test-Path "$env:APPDATA\Claude\claude_desktop_config.json"

# 启动Claude Desktop进行测试
Start-Process "Claude"
```

## 🌙 **晚上部署建议**

1. **确保干净环境**: XYSB目录不含servers
2. **使用global-scripts**: 完全避开Obsidian Sync
3. **分步验证**: 每步完成后测试
4. **最终测试**: Claude Desktop识别7个MCP服务器

---

**重要**: 此配置避免了所有Obsidian Sync跨设备冲突，Windows和macOS可以独立部署！ 

---

**文档恢复时间**: 2025-06-29  
**最後更新**: 2025-07-03 (跨平台路徑對應關係新增)  
**成功部署**: 7个官方MCP服务器  
**关键创新**: global-scripts路径策略  
**跨平台對應**: macOS使用.xykms目錄實現相同策略

**更新記錄**:
- **v1.0** (2025-06-29): Windows MCP部署指南恢復版本
- **v1.1** (2025-07-03): 新增macOS跨平台路徑對應說明，確保兩平台部署策略統一 

## 📋 **部署狀況澄清 (2025-07-03更新)**

### **🔄 實際部署時程**
```yaml
文檔原始定位:
  - 作為Windows MCP部署的完整指引
  - 提供7個MCP服務器的詳細安裝流程
  
當前實際狀況:
  Windows環境: 🔄 尚未開始部署 (等待macOS規劃完成)
  macOS環境: 🎯 主要規劃與測試平台 (當前進行中)
  
部署策略:
  1️⃣ macOS環境先行完善 (使用.xykms統一策略)
  2️⃣ 建立跨平台配置模板
  3️⃣ Windows按本指南執行部署
  4️⃣ 雙平台驗證與同步測試
```

### **📝 指南使用建議**
```yaml
當前階段 (macOS規劃):
  - 本指南作為Windows部署的參考標準
  - macOS使用相同的7個MCP服務器清單
  - 配置格式完全相同 (僅路徑不同)
  
後續階段 (Windows實施):
  - 直接按本指南執行完整部署
  - 確保與已完善的macOS環境一致
  - 實現真正的跨平台開發環境
```

--- 