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
```

## 文件说明

- `conversation.md`：按时间顺序保存完整对话，便于回溯与审计。
- `meta.json`：结构化元数据（标题、摘要、标签、决策等），支撑检索与二次消费。
- `chunks.jsonl`：分块后的纯文本，供向量化或索引重建；v0 可为空，按需生成。

## Quickstart

## 前置要求
- 已安装 **Claude Code / claude CLI**
- 已安装 **Python 3.10+**
- 已安装 **uv**（用于运行 Python 环境与依赖）

可选检查：
```bash
python --version
uv --version
claude --version
```

### 安装 Nidhogg 插件
1. git clone https://github.com/Shuimo03/Nidhogg.git
2. 启动 claude code

```bash
  /plugin marketplace add ./Nidhogg/nidhogg-marketplace
  /plugin install nidhogg@nidhogg
```

3. 查看 plugin 命令，如果出现 /nidhogg:save  表示安装成功。

## .mcp.json 配置

因为使用的是 stdio-server，需要确保 MCP 服务的 `cwd` 与 `PYTHONPATH` 指向
`nidhogg-mcp` 目录。以下示例基于仓库结构：

```
<repo-root>/
  nidhogg-mcp/
  nidhogg-marketplace/
    nidhogg/   # CLAUDE_PLUGIN_ROOT
```

举例说明：如果你在 `/Users/mac/code/prometheus` 下 clone 了 Nidhogg，
需要修改 `/Users/mac/code/prometheus/nidhogg-marketplace/nidhogg/.mcp.json`。

示例配置（插件目录内的 `.mcp.json`）：

```json
{
  "mcpServers": {
    "nidhogg-mcp": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "python", "-m", "nidhogg_mcp"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}/../../nidhogg-mcp",
      "env": {
        "PYTHONPATH": "${CLAUDE_PLUGIN_ROOT}/../../nidhogg-mcp/src"
      }
    }
  }
}
```

如果你将插件目录移动到其他位置，请相应调整 `cwd` 与 `PYTHONPATH`，
确保能定位到 `nidhogg-mcp`。
