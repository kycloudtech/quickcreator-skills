---
layout: default
title: Getting Started
nav_order: 2
description: "Install the QuickCreator Skill Builder and set up the MCP server."
---

# Getting Started
{: .no_toc }

Install the skill, configure the MCP server, and start building QuickCreator skills with your AI agent.
{: .fs-6 .fw-300 }

<details open markdown="block">
  <summary>Table of contents</summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

---

## Step 1 — Install the Skill

Put the `quickcreator-skill-builder` folder (the one that contains `SKILL.md`) into your agent's **skills directory** so the agent can load it.

### Option A: Using npx skills CLI

If you have [vercel-labs/skills](https://github.com/vercel-labs/skills), run:

```bash
npx skills add https://github.com/kycloudtech/quickcreator-skills/tree/master/quickcreator-skill-builder
```

Use `-g` for global install; use `-a cursor -a claude-code` to target specific agents.

### Option B: Manual Installation

1. Clone or download [the repository](https://github.com/kycloudtech/quickcreator-skills)
2. Copy the `quickcreator-skill-builder` folder into the appropriate skills directory for your agent

### Skills Directory by Agent

Copy the **entire** `quickcreator-skill-builder` folder into one of the paths below. **Global** = available in all projects; **Project** = only in that project. On Windows, use `%USERPROFILE%` instead of `~`.

| Agent | Project path | Global path |
|:------|:-------------|:------------|
| **Cursor** | `.cursor/skills/` or `.agents/skills/` | `~/.cursor/skills/` |
| **Claude Code** | `.claude/skills/` | `~/.claude/skills/` |
| **Codex** | `.agents/skills/` | `~/.codex/skills/` |
| **OpenCode** | `.agents/skills/` | `~/.config/opencode/skills/` |
| **Windsurf** | `.windsurf/skills/` | `~/.codeium/windsurf/skills/` |
| **Cline** | `.cline/skills/` | `~/.cline/skills/` |
| **Continue** | `.continue/skills/` | `~/.continue/skills/` |
| **GitHub Copilot** | `.agents/skills/` | `~/.copilot/skills/` |
| **OpenHands** | `.openhands/skills/` | `~/.openhands/skills/` |
| **Gemini CLI** | `.agents/skills/` | `~/.gemini/skills/` |
| **Amp, Kimi, Replit** | `.agents/skills/` | `~/.config/agents/skills/` |
| **Antigravity** | `.agent/skills/` | `~/.gemini/antigravity/skills/` |
| **Augment** | `.augment/skills/` | `~/.augment/skills/` |

{: .note }
After copying the folder, you may need to **restart or reload your agent** so it discovers the new skill.

---

## Step 2 — Set Up the QuickCreator MCP

This skill communicates with QuickCreator through an MCP server. You need two things: a developer token and the MCP configuration.

### 2a. Get a Developer Token

1. Open [QuickCreator Agent Dev](https://agent-dev.quickcreator.io/demo/chat)
2. Go to **Settings → Create Token**
3. Create a token with **read, write, and publish** permissions
4. Copy the token and keep it safe

### 2b. Add the MCP Server to Your Agent

The config file path depends on your agent:

| Agent | MCP config file (global) | Format |
|:------|:--------------------------|:-------|
| **Cursor** | `~/.cursor/mcp.json` | JSON |
| **Windsurf** | `~/.codeium/windsurf/mcp_config.json` | JSON |
| **Claude Code** | `~/.claude.json` or project `.mcp.json` | JSON |
| **Cline** | `~/.cline/data/settings/cline_mcp_settings.json` | JSON |
| **Codex** | `~/.codex/config.toml` | TOML |
| **Continue** | `~/.continue/config.json` (MCP section) | JSON |

### JSON Config (Cursor, Windsurf, Claude Code, Cline)

Add the block below to the config file. If the file already has `mcpServers`, merge this entry into it. Replace `<your_developer_token>` with the token from step 2a.

```json
{
  "mcpServers": {
    "quickcreator-skill": {
      "command": "npx",
      "args": ["@quickcreator/skill-mcp"],
      "env": {
        "QC_API_TOKEN": "<your_developer_token>",
        "QC_API_URL": "https://api-dev.quickcreator.io/ai-blog-chat-service"
      }
    }
  }
}
```

### TOML Config (Codex)

Edit `~/.codex/config.toml` and add:

```toml
[mcp_servers.quickcreator-skill]
command = "npx"
args = ["@quickcreator/skill-mcp"]
env = { QC_API_TOKEN = "<your_developer_token>", QC_API_URL = "https://api-dev.quickcreator.io/ai-blog-chat-service" }
```

{: .note }
`QC_API_URL` is set to the dev API while the MCP is in development. When the MCP reaches production, you can remove `QC_API_URL` and the MCP will use the default production URL.

---

## Step 3 — You're Ready

Restart or reload the agent if you just installed the skill or changed the MCP config.

You can now ask your agent to:

- **List** your QuickCreator skills (personal, marketplace, installed)
- **Create** a new skill
- **Fork** a skill from the marketplace and edit it
- **Publish** a skill to the marketplace
- **Install** or **uninstall** marketplace skills

The skill (`SKILL.md`) teaches the agent how to do these things using the QuickCreator Skill MCP.
