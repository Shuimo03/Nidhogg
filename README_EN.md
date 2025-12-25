# Nidhogg

> A local-first conversation, context, and knowledge recorder for LLM workflows.

Nidhogg is a **local-first context and conversation manager** for engineers and heavy LLM users.  
It is not about making chat more human; it solves a longer-term, engineering problem:

> **LLM context is ephemeral; engineering knowledge must be rebuildable, auditable, and reusable.**

By combining **structured storage + MCP (Model Context Protocol) + plugins**, Nidhogg turns each
conversation with a model into durable engineering assets.

---

## Why Nidhogg?

You have probably seen this in real engineering work:

- Architecture, troubleshooting, and decision threads disappear in chat windows.  
- Complex prompts cannot be versioned or revisited.  
- You keep “rehydrating context” over and over, wasting time.  
- Models are powerful, but context management is primitive.  

Nidhogg focuses on one thing:

> **Upgrade LLM conversations from “ephemeral chat” to “engineering material.”**

---

## Core Principles

- **Local-first**  
  Data lives on the local filesystem by default—offline friendly, backup-able, auditable.  

- **Rebuildable**  
  Vectors, indexes, and stats are derivatives, not source. They can be discarded and rebuilt.  

- **LLM-agnostic**  
  No vendor lock-in; interaction flows through MCP to higher-level tools.  

- **Engineering-friendly**  
  Built for engineers, not generic chat users.  

---

## Current Layout

```text
Nidhogg/
├── README.md
├── README_EN.md
├── LICENSE
├── AGENTS.md
│
├── nidhogg-mcp/              # MCP server (Python)
│   └── src/
│       └── nidhogg_mcp/
│
├── nidhogg-marketplace/      # Claude Code plugin marketplace
│   ├── .claude-plugin/
│   │   └── marketplace.json
│   └── nidhogg/              # Plugin definition
│
└── prd/                      # Design / product docs
```

## Conversation Storage Trio

- `conversation.md`: Chronological, full conversation for human audit and recall.  
- `meta.json`: Structured metadata (title, summary, tags, decisions) to power retrieval and reuse.  
- `chunks.jsonl`: Text chunks for vectorization or index rebuilds; v0 can stay empty until needed.  

## Quickstart

## Prerequisites
- Claude Code / `claude` CLI installed
- Python 3.10+
- `uv` installed (for running the Python environment and dependencies)

Optional checks:
```bash
python --version
uv --version
claude --version
```

### Install Nidhogg Plugin
1. `git clone https://github.com/Shuimo03/Nidhogg.git`
2. Launch Claude Code

```bash
/plugin marketplace add ./nidhogg-marketplace
/plugin install nidhogg
```

3. Check plugin commands; if `/nidhogg:save` appears, the installation is successful.

## .mcp.json Configuration

Because we use a stdio-server, make sure `cwd` and `PYTHONPATH` point to the
`nidhogg-mcp` directory. The example below assumes this layout:

```
<repo-root>/
  nidhogg-mcp/
  nidhogg-marketplace/
    nidhogg/   # CLAUDE_PLUGIN_ROOT
```

Example: if you cloned Nidhogg under `/Users/mac/code/prometheus`,
update `/Users/mac/code/prometheus/nidhogg-marketplace/nidhogg/.mcp.json`.

Example config (inside the plugin `.mcp.json`):

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

If you move the plugin directory, adjust `cwd` and `PYTHONPATH` accordingly so
they still resolve to `nidhogg-mcp`.
