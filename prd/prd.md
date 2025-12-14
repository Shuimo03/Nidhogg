# Claude Code Plugin：对话存储与向量化演进设计

> 本文档用于**冻结本轮讨论的上下文**，作为后续实现 Claude Code Plugin（Nidhogg 子项目）的设计基线。

---

## 一、问题背景

在多轮需求与系统设计讨论中，随着对话持续增长，LLM 的上下文窗口容易溢出，进而引入幻觉与不一致推理。为解决这一问题，需要一个 **Claude Code Plugin**，用于：

* 保存对话内容
* 冻结阶段性共识与决策
* 支持后续 RAG（Retrieval-Augmented Generation）检索
* 本地优先、低运维、可重建

---

## 二、核心设计原则（不随阶段变化）

1. **Markdown 是唯一事实源（Source of Truth）**
2. **数据库内容必须可从 Markdown 重建**
3. **向量仅作为索引，不是知识本体**

---

## 三、分阶段实现路线

### Phase 0：三文件制（当前阶段）

**目标**：冻结上下文、抗幻觉、零基础设施

#### 文件结构

```
conversations/
  <conversation-id>/
    conversation.md
    meta.json
    chunks.jsonl
```

#### 各文件职责

* `conversation.md`

  * 保存完整对话
  * 人类可读、可审阅、可版本控制
  * 保持角色（system / user / assistant）
  * 不丢任何信息

* `meta.json`
  * 作用:
    * 快速知道这段对话大概在讲什么 
    * 冻结阶段性结论，防止重复讨论 
    * 作为后续检索、聚合、筛选的锚点
  * 结构化元信息：

    * topic
    * summary
    * decisions
    * tags
    * status（active / frozen / deprecated）

举个例子:
```json
{
  "topic": "Nidhogg Phase 0 conversation storage design",
  "summary": "Defined a three-file storage model using conversation.md, meta.json, and chunks.jsonl to stabilize long-running conversations and support future RAG.",
  "decisions": [
    "Use Markdown as the single source of truth",
    "Treat vector data as disposable, rebuildable index",
    "Introduce conversation lifecycle states: ACTIVE, FROZEN, DEPRECATED"
  ],
  "tags": ["nidhogg", "mcp", "rag", "design"],
  "status": "frozen",
  "created_at": "2025-12-14T06:40:12Z"
}


```

* `chunks.jsonl`

  * 已按语义切分的最小 RAG 单元
  * 每行一个 chunk，包含：

    * stable_id
    * text
    * metadata（来源、标签、决策引用等）

---

### Phase 1：SQLite 作为派生索引层

**触发条件（满足任意两条）：**

* 对话数量 > 30
* 开始频繁“我记得之前聊过这个”
* grep 已无法满足查找需求

#### 新增组件

```
knowledge.db   # SQLite
```

#### SQLite 的职责

* 存储 chunk 索引
* 存储 embedding
* 提供 metadata + 向量联合检索

> SQLite 不存完整对话，仅存可丢弃、可重建的派生数据。

---

### Phase 2：抽象 VectorStore 接口

**目标**：为未来迁移做准备，但不引入新基础设施。

#### 抽象接口示意

* `upsert(chunks)`
* `query(embedding, filters)`
* `delete_by_source(source_id)`

> SQLite 仍为默认实现，仅在代码层解耦。

---

### Phase 3：引入 Qdrant（可选）

**明确触发条件：**

* chunk 数量 > 5–10 万
* 多项目共享知识
* SQLite 查询出现明显性能瓶颈

#### 正确定位

```
Markdown / JSON  → 真相
SQLite           → 本地索引 & fallback
Qdrant           → 高性能向量引擎
```

> Qdrant 永远不是唯一存储，仅作为向量检索服务。

---

## 四、数据库与向量库选型结论

* **默认数据库**：SQLite（带向量扩展）
* **默认策略**：本地优先、可删除、可重建
* **独立向量库（如必须）**：Qdrant（唯一推荐）

---

## 五、当前阶段的实施重点

* 明确并实现三文件制
* 定义稳定的 chunk schema 与 stable_id
* 保证任何派生数据都可从 Markdown 重建

---

## 六、设计共识总结

本插件的本质不是“聊天记录保存器”，而是：

> **上下文边界稳定器（Context Boundary Stabilizer）**

它的价值在于：

* 在正确的时间冻结正确的信息
* 将一次性对话转化为长期可积累的知识资产

---

## 七、MCP 实现决策与职责划分（补充）

### 7.1 为什么必须使用 MCP

* Markdown / Agent / Hook **都不能承担确定性 I/O 与持久化**
* 对话落盘、结构化、索引必须由一个 **确定性执行体** 完成
* MCP 是 Claude Code 生态中 **唯一正确的“执行边界”**

职责边界如下：

* **Claude / Agent**：理解、总结、判断是否需要冻结
* **Hook / Command**：决定“什么时候触发”
* **MCP Server**：执行、校验、写文件、建索引

---

## 八、MCP v0 命令（Tool）设计

> 本阶段 MCP 使用 **Python SDK + stdio 模式** 实现，目标是最小可用、可测试、可演进。

### 8.1 save_conversation（核心命令）

**用途**：

* 将当前对话冻结为稳定的三文件结构
* 防止上下文继续膨胀导致幻觉

**输入（v0）**：

* `title: string` —— 对话标题 / 主题
* `messages: [{ role: string, content: string }]` —— 原始对话（推荐）
* `out_dir: string` —— conversations 根目录
* `meta?: object` —— Claude 生成的结构化信息（summary / tags / decisions）

**行为**：

* MCP 根据 messages **自行生成** `conversation.md`
* 校验并写入 `meta.json`
* 生成空的 `chunks.jsonl`（后续版本填充）

**输出**：

* 冻结目录路径

---

### 8.2 reindex (预留)

**用途**：

* 从已有 Markdown / JSON 重新生成索引
* 保证数据库 / 向量索引可完全重建

**输入**：

* `path: string` —— conversations 目录

**行为**：

* 扫描三文件结构
* 重新生成 chunks / embedding（后续版本）

---

### 8.3 search (预留)

**用途**：

* 对已冻结知识进行检索
* Phase 1 可先做关键词 / 文件级搜索

---

## 九、Claude Code Plugin 中的调用方式（补充说明）

* Markdown 仅用于 **声明 command / agent / skill**
* 实际存储与检索逻辑 **全部委托给 MCP**
* 插件中的 `/freeze` / `/save` 命令应直接调用 `save_conversation`

---

## 十、当前阶段的开发优先级（更新）

1. 实现 Python MCP Server（stdio）
2. 完成 `save_conversation` 的稳定实现
3. 固定 `conversation.md` 的生成模板
4. 定义 `meta.json` v0 schema

---

*本文件已补充 MCP 实现与命令设计，作为后续编码的直接依据*

## 参考
1. https://modelcontextprotocol.io/docs/sdk
2. https://code.claude.com/docs/en/plugins


