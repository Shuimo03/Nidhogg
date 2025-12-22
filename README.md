# Nidhogg

> A local-first conversation, context, and knowledge recorder for LLM workflows.

**Nidhogg** 是一个面向工程师、重度 LLM 使用者的 **本地优先（local-first）上下文与对话管理工具**。  
它关注的不是“如何把聊天做得更像人”，而是一个更工程化、更长期的问题：

> **LLM 的上下文是易失的，但工程知识应该是可重建、可审计、可复用的。**

Nidhogg 通过 **结构化存储 + MCP（Model Context Protocol）+ Plugin 机制**，  
把一次次与模型的对话，沉淀为真正可以长期积累的工程资产。

---

## 为什么要做 Nidhogg？

在真实的工程场景中，你大概率遇到过这些情况：

- 架构设计、排障推理、决策讨论都消失在聊天窗口里  
- Prompt 很复杂，但无法被版本化或回溯  
- 每次都要“重新喂上下文”，效率极低  
- 模型很强，但上下文管理极其原始  

Nidhogg 想解决的核心问题只有一个：

> **把 LLM 对话，从“临时交流”升级为“工程材料”。**

---

## 核心理念

- **Local-first**  
  所有数据默认存储在本地文件系统，可离线、可备份、可审计  

- **Rebuildable（可重建）**  
  向量、索引、统计数据都不是源数据，随时可以丢弃并重建  

- **LLM-agnostic**  
  不绑定任何模型或厂商，通过 MCP 与上层工具交互  

- **Engineering-friendly**  
  面向工程师，而不是泛聊天用户  

---

## 项目结构（当前）

```text
Nidhogg/
├── README.md
├── LICENSE
├── AGENTS.md
│
├── nidhogg-mcp/              # MCP Server（Python）
│   └── src/
│       └── nidhogg_mcp/
│
├── nidhogg-marketplace/      # Claude Code Plugin Marketplace
│   ├── .claude-plugin/
│   │   └── marketplace.json
│   └── nidhogg/              # Plugin 定义
│
└── prd/                      # 设计 / 产品文档
