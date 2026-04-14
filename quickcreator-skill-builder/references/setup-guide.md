# First-Time Setup Guide

This document covers the complete first-time setup flow. Referenced from [SKILL.md](../SKILL.md) when the QuickCreator connection is not yet configured or the user explicitly wants to connect.

---

## When to Trigger

Run this setup flow when:
- This skill is invoked but the QuickCreator connection is not configured (tools like `list_personal_skills` are unavailable or error)
- The user explicitly wants to connect to QuickCreator

---

## Step 1: Ask for the Developer Key

Present this to the user in their language. Example in Chinese:

> 欢迎使用 QuickCreator Skill Builder！
>
> 首次使用需要进行一次简单的连接设置。你只需要完成一个步骤：
>
> 1. 打开 [QuickCreator 开发者平台](https://agent.quickcreator.io)
> 2. 登录你的账号（没有账号可以免费注册）
> 3. 进入 **设置** → 点击 **创建密钥**
> 4. 确保开启 **读取**、**写入** 和 **发布** 权限
> 5. 复制密钥，粘贴给我
>
> 这个设置只需要做一次，之后就可以直接使用了。

Wait for the user to provide the key. Validate it is a non-empty string.

---

## Step 2: Auto-Detect Agent & Write Config

> **Note for agents:** Before writing the config, check if the config file already contains an MCP entry named `quickcreator-skill`. If it does, it was likely set up against the old dev environment — rename it to `quickcreator-skill-dev` and set its `QC_API_URL` to `https://api-dev.quickcreator.io/ai-blog-chat-service` first, then proceed to write the new `quickcreator-skill` entry below.

Detect which agent is running by examining the skill's file path or environment:

| Path contains | Agent |
|---------------|-------|
| `.cursor/` | Cursor |
| `.claude/` | Claude Code |
| `.config/opencode/` or OpenCode context | OpenCode |
| `.codeium/` or `.windsurf/` | Windsurf |
| `.openclaw/` | OpenClaw |
| `.codex/` | Codex |
| `.cline/` | Cline |

If uncertain, ask the user in simple language: "You are currently using which tool? (Cursor / OpenCode / Claude Code / ...)"

**Check Node.js availability first:** Run `npx --version` silently. If it fails, tell the user:
> "Your computer needs to install a small runtime component. Please download and install Node.js from https://nodejs.org (choose the LTS version), then try again."

Then write the configuration file automatically:

### JSON Agents (Cursor, Windsurf, Claude Code, Cline, OpenClaw)

| Agent | Config file path |
|-------|-----------------|
| Cursor | `~/.cursor/mcp.json` |
| Windsurf | `~/.codeium/windsurf/mcp_config.json` |
| Claude Code | `~/.claude.json` or project `.mcp.json` |
| Cline | `~/.cline/data/settings/cline_mcp_settings.json` |
| OpenClaw | Project `.mcp.json` or `~/.openclaw/mcp.json` |

JSON content to merge into `mcpServers`:
```json
{
  "mcpServers": {
    "quickcreator-skill": {
      "command": "npx",
      "args": ["@quickcreator/skill-mcp"],
      "env": {
        "QC_API_TOKEN": "<DEVELOPER_KEY_HERE>",
        "QC_API_URL": "https://api.quickcreator.io/ai-blog-chat-service"
      }
    }
  }
}
```

### OpenCode

Edit project `opencode.json` or `~/.config/opencode/opencode.json`:
```json
{
  "mcp": {
    "quickcreator-skill": {
      "type": "local",
      "command": ["npx", "-y", "@quickcreator/skill-mcp"],
      "enabled": true,
      "environment": {
        "QC_API_TOKEN": "<DEVELOPER_KEY_HERE>",
        "QC_API_URL": "https://api.quickcreator.io/ai-blog-chat-service"
      }
    }
  }
}
```
OpenCode uses a different config format: root key is `"mcp"` (not `"mcpServers"`), requires `"type": "local"`, command is a single array (not separate `command`/`args`), and env vars use `"environment"` (not `"env"`). If `opencode.json` already has other settings (model, theme, etc.), merge the `"mcp"` field without overwriting existing content.

### TOML Agents (Codex)

Edit `~/.codex/config.toml`:
```toml
[mcp_servers.quickcreator-skill]
command = "npx"
args = ["@quickcreator/skill-mcp"]
env = { QC_API_TOKEN = "<DEVELOPER_KEY_HERE>", QC_API_URL = "https://api.quickcreator.io/ai-blog-chat-service" }
```

If the config file already exists, **merge** the entry without overwriting other content.

---

## Step 3: Notify Restart (ONE Combined Message)

After ALL setup is complete, send ONE message telling the user to restart. Include how to invoke the skill after restart:

| Agent | Restart message (adapt to user's language) |
|-------|---------------------------------------------|
| Cursor | "All set! Please restart Cursor. After restart, type `/` in chat, select `quickcreator-skill-builder`, and press Enter to start." |
| OpenCode | "All set! Please restart OpenCode. After restart, type `/quickcreator-skill-builder` in chat and press Enter to start." |
| Claude Code | "All set! Please restart Claude Code. After restart, just tell me you want to create or manage skills." |
| Windsurf | "All set! Please restart Windsurf to activate the connection." |
| OpenClaw | "All set! Please restart OpenClaw to activate the connection." |
| Codex | "All set! Please restart Codex to activate the connection." |

**IMPORTANT:** Send only ONE restart message at the very end. Never prompt restart after individual steps.

---

## Step 4: Verify Connection (After Restart)

When the user returns after restart, silently call `list_personal_skills()`.
- If it succeeds → Tell the user: "Connection is ready! Let's get started."
- If it fails → Ask user to re-enter their developer key, check if the key has correct permissions.

---

## How to Invoke This Skill

When guiding users (in their language), explain how to use this skill next time:

| Agent | Instructions |
|-------|-------------|
| Cursor | In the chat window, type `/`, then select or type `quickcreator-skill-builder` and press Enter |
| OpenCode | In the chat window, type `/quickcreator-skill-builder` and press Enter |
| Claude Code | Just mention that you want to create or manage QuickCreator skills |
| Other agents | Just ask about creating or managing QuickCreator skills in conversation |
