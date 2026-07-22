# 🤖 EP01：用 Agent 來學習 Agent — 專案工作藍圖 (agents.md)

> **專案名稱**：AI Agent 系列 EP01 - 用 Agent 來學習 Agent  
> **建立日期**：2026-07-21  
> **目前狀態**：初始化完成 / 規劃階段  

---

## 🎯 專案目標與核心理念

本專案「**EP01：用 Agent 來學習 Agent**」旨在透過實際操作與 AI Agent 協同開發，深入理解 AI Agent 的核心機制（包括 Context Management, Tool Use, Subagents, Model Context Protocol (MCP), Skills 等），並建立一套可自我迭代與擴展的 Agent 學習與開發體系。

### 核心原則
1. **Agent-First 實作**：將 Agent 視為對等的 Pair Programming 夥伴，透過任務拆解、Subagents 協同與工具呼叫解決問題。
2. **學習與實務並重**：不只停留在理論，而是透過建立真實代碼、自動化工作流與 Skill 模組來內化知識。
3. **持續積累與模組化**：所有的探索經驗與最佳實踐，均收錄為可複用的技能 (Skills) 與結構化文件。

---

## 🏗️ Agent 角色與職責架構 (Agent Ecosystem)

| 角色名稱 | Agent 類型 | 核心職責 | 工具與權限 |
| :--- | :--- | :--- | :--- |
| **Lead Orchestrator** | 主控 Agent (Antigravity) | 專案進度管理、總體規劃、工作拆解與調度 | 全域工具存取、Subagent 調用 |
| **Research Agent** | Subagent (`research`) | 技術文獻/文件檢索、技術選型評估與總結 | 唯讀 (web search, view_file) |
| **Code Builder Agent** | Subagent / Self | 核心程式碼實作、單元測試編寫與 Code Refactor | 讀寫工具 (write_to_file, run_command) |
| **Evaluator / Reviewer** | Subagent (`eval`) | 代碼審查、性能評估、規範與安全機制檢查 | 唯讀 / 評估工具 |

---

## 🗺️ 工作藍圖與發展里程碑 (Roadmap & Milestones)

### 📌 Phase 1: 專案基礎與環境建立 (Foundation & Setup)
- [x] **M1.1** 初始化 `agents.md` 專案工作藍圖
- [ ] **M1.2** 梳理專案目錄結構與開發環境配置
- [ ] **M1.3** 建立 `ANTIGRAVITY.md` 開工/收工與習慣規範文件

### 📌 Phase 2: Agent 核心機制學習與探索 (Core Mechanisms Exploration)
- [ ] **M2.1** **Prompt & System Persona**：設計結構化的 Agent 指令集與角色定位
- [ ] **M2.2** **Tools & Function Calling**：探索 API 工具對接與邊界處置
- [ ] **M2.3** **Context & Memory**：研究長上下文管理與持久化記憶機制
- [ ] **M2.4** **MCP (Model Context Protocol)**：串接並實作自訂 MCP Server

### 📌 Phase 3: 多 Agent 協同與自動化工作流 (Multi-Agent & Workflow)
- [ ] **M3.1** 實作任務拆解與 Subagent 派發機制
- [ ] **M3.2** 建立非同步任務與狀態追蹤機制
- [ ] **M3.3** 封裝實用的專案專屬 Skills / Custom Sidecars

### 📌 Phase 4: 實作專案與學習成果產出 (Build & Knowledge Output)
- [ ] **M4.1** 完成 EP01 綜合範例專案實作
- [ ] **M4.2** 自動生成互動教學簡報與技術文件
- [ ] **M4.3** 進行專案復盤與產出 EP02 展望

---

## 🔄 開發工作流程與規範 (Workflow & Best Practices)

### 開工流程 (`/start`)
1. 讀取 `agents.md` 與專案重點筆記。
2. 執行 `git status` 確認當前分支狀態。
3. 確定本次 Session 目標並更新 Task List。

### 開發與協同
- **單一職責**：複雜任務透過 `invoke_subagent` 拆分並平行執行。
- **實證驗證**：所有變更均須通過語法檢查與單元測試，絕不憑空宣告成功。

### 收工流程 (`/finish`)
1. 檢查敏感資料與金鑰。
2. 更新 `agents.md` 的進度與待辦事項。
3. 提交 Git commit 訊息（遵循 Conventional Commits）。

---

## 📝 變更記錄 (Change Log)

- **2026-07-21**：建立 `agents.md` 初版，完成專案目標、Agent 角色劃分與 Phase 1~4 發展藍圖定義。
