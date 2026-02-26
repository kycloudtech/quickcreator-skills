# QuickCreator Skill Builder

This skill lets your AI agent **develop and maintain QuickCreator skills**: list, search, create, fork, publish, and manage skills on the [QuickCreator](https://www.quickcreator.io) platform using the [QuickCreator Skill MCP](https://www.npmjs.com/package/@quickcreator/skill-mcp).

If the user asked to **install this skill**, follow the steps below. The agent can use this README to install the skill and then guide the user to set up the MCP. Other files in this repo (e.g. `SKILL.md`, `skill-standards.md`, `tool-reference.md`, `requirements.sh`) can be read when needed.

---

## Step 1 — Install the skill

Put the `quickcreator-skill-builder` folder (the one that contains `SKILL.md`) into your agent’s **skills directory** so the agent can load it.

### Get the folder

- **From the repo**: Clone or download [this repository](https://github.com/kycloudtech/quickcreator-skills), then use the folder `quickcreator-skills/quickcreator-skill-builder`.
- **From a release**: Download the latest zip from [Releases](https://github.com/kycloudtech/quickcreator-skills/releases) and unzip so you have a folder named `quickcreator-skill-builder` with `SKILL.md` inside.

### Where to put it (by agent)

Copy the **entire** `quickcreator-skill-builder` folder into one of the paths below. **Global** = available in all projects; **Project** = only in that project. On Windows, use `%USERPROFILE%` instead of `~`.

| Agent | Project path | Global path |
|-------|--------------|-------------|
| **Cursor** | `.cursor/skills/` or `.agents/skills/` | `~/.cursor/skills/` |
| **Claude Code** | `.claude/skills/` | `~/.claude/skills/` |
| **Codex** | `.agents/skills/` | `~/.codex/skills/` |
| **OpenCode** | `.agents/skills/` | `~/.config/opencode/skills/` |
| **Windsurf** | `.windsurf/skills/` | `~/.codeium/windsurf/skills/` |
| **Cline** | `.cline/skills/` | `~/.cline/skills/` |
| **Continue** | `.continue/skills/` | `~/.continue/skills/` |
| **GitHub Copilot** | `.agents/skills/` | `~/.copilot/skills/` |
| **OpenHands** | `.openhands/skills/` | `~/.openhands/skills/` |
| **Amp, Kimi, Replit** | `.agents/skills/` | `~/.config/agents/skills/` |
| **Antigravity** | `.agent/skills/` | `~/.gemini/antigravity/skills/` |
| **Augment** | `.augment/skills/` | `~/.augment/skills/` |
| **OpenClaw** | `skills/` | `~/.openclaw/skills/` |
| **CodeBuddy** | `.codebuddy/skills/` | `~/.codebuddy/skills/` |
| **Command Code** | `.commandcode/skills/` | `~/.commandcode/skills/` |
| **Cortex** | `.cortex/skills/` | `~/.snowflake/cortex/skills/` |
| **Crush** | `.crush/skills/` | `~/.config/crush/skills/` |
| **Droid** | `.factory/skills/` | `~/.factory/skills/` |
| **Gemini CLI** | `.agents/skills/` | `~/.gemini/skills/` |
| **Goose** | `.goose/skills/` | `~/.config/goose/skills/` |
| **Junie** | `.junie/skills/` | `~/.junie/skills/` |
| **iFlow CLI** | `.iflow/skills/` | `~/.iflow/skills/` |
| **Kilo, Kiro, Kode** | (see agent docs) | `~/.kilocode/skills/`, `~/.kiro/skills/`, `~/.kode/skills/` |
| **MCPJam** | `.mcpjam/skills/` | `~/.mcpjam/skills/` |
| **Mistral Vibe** | `.vibe/skills/` | `~/.vibe/skills/` |
| **Mux** | `.mux/skills/` | `~/.mux/skills/` |
| **Pi** | `.pi/skills/` | `~/.pi/agent/skills/` |
| **Qoder, Qwen, Roo** | (see agent docs) | `~/.qoder/skills/`, `~/.qwen/skills/`, `~/.roo/skills/` |
| **Trae / Trae CN** | `.trae/skills/` | `~/.trae/skills/`, `~/.trae-cn/skills/` |
| **Zencoder, Neovate, Pochi, AdaL** | (see agent docs) | `~/.zencoder/skills/`, etc. |

**Using the npx skills CLI:** If the user has [vercel-labs/skills](https://github.com/vercel-labs/skills), you can run:

```bash
npx skills add https://github.com/kycloudtech/quickcreator-skills/tree/master/quickcreator-skill-builder
```

Use `-g` for global install; use `-a cursor -a claude-code` to target specific agents.

After copying the folder, the user may need to **restart or reload the agent** so it sees the new skill.

---

## Step 2 — Set up the QuickCreator MCP (required)

This skill talks to QuickCreator through an MCP server. The user must do two things: get a developer token, then add the MCP to their agent’s config.

### 2a. Get a QuickCreator developer token

1. Open [QuickCreator Agent Dev](https://agent-dev.quickcreator.io/demo/chat).
2. Go to **Settings → Create Token**.
3. Create a token with **read, write, and publish** permissions.
4. Copy the token and keep it safe (you will paste it into the MCP config as `QC_API_TOKEN`).

### 2b. Add the MCP server to your agent’s config

The config file path depends on the agent. Create the file if it doesn’t exist. On Windows, use `%USERPROFILE%` instead of `~`.

| Agent | MCP config file (global) | Format |
|-------|---------------------------|--------|
| **Cursor** | `~/.cursor/mcp.json` | JSON |
| **Windsurf** | `~/.codeium/windsurf/mcp_config.json` | JSON |
| **Claude Code** | `~/.claude.json` or project `.mcp.json` | JSON |
| **Cline** (CLI) | `~/.cline/data/settings/cline_mcp_settings.json` | JSON |
| **Codex** | `~/.codex/config.toml` | TOML |
| **Continue** | `~/.continue/config.json` (MCP section) | JSON |

**For JSON configs (Cursor, Windsurf, Claude Code, Cline):** Add the block below to the config file. If the file already has `mcpServers`, merge this entry into it. Replace `<your_developer_token>` with the token from step 2a.

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

**For Codex (TOML):** Edit `~/.codex/config.toml` and add:

```toml
[mcp_servers.quickcreator-skill]
command = "npx"
args = ["@quickcreator/skill-mcp"]
env = { QC_API_TOKEN = "<your_developer_token>", QC_API_URL = "https://api-dev.quickcreator.io/ai-blog-chat-service" }
```

**Note:** `QC_API_URL` is set to the dev API while the MCP is in development. When the MCP is officially production-ready, you can remove `QC_API_URL` and the MCP will use the default production URL.

---

## Step 3 — You’re ready

Restart or reload the agent if you just installed the skill or changed the MCP config.

You can now ask your agent to:

- List your QuickCreator skills (personal, marketplace, installed)
- Create a new skill
- Fork a skill from the marketplace and edit it
- Publish a skill to the marketplace
- Install or uninstall marketplace skills

The skill (`SKILL.md`) teaches the agent how to do these things using the QuickCreator Skill MCP.

---

## What this skill does

- **List and search** QuickCreator skills (personal, built-in, marketplace, installed).
- **Create** new skills with the correct structure and `SKILL.md`.
- **Fork** marketplace or built-in skills to personal and **update** files.
- **Publish** personal skills to the marketplace and **update** existing listings.
- **Install / uninstall** marketplace skills.
- **Delete** personal skills.
- Follow QuickCreator skill standards and pre-publish checklist (see `skill-standards.md`).

---

## Other files in this repo

| File | Purpose |
|------|---------|
| **SKILL.md** | Instructions for the agent: how to use the MCP tools, workflows, and rules. The agent loads this when the skill is active. |
| **skill-standards.md** | QuickCreator skill content and format rules (English, naming, no secrets, etc.). Used when creating or publishing skills. |
| **tool-reference.md** | Reference for tools available to skills that run on QuickCreator (images, knowledge base, code execution, video). |
| **requirements.sh** | Declares dependencies for scripts (e.g. `google-genai` for `scripts/generate_video.py`). Required when the skill has a `scripts/` directory; see skill-standards.md. |
| **scripts/generate_video.py** | Template script for video generation (Veo) via `code_execute`. |

The agent can read these when helping the user create or edit QuickCreator skills.

---

## References

- [QuickCreator Skill MCP (npm)](https://www.npmjs.com/package/@quickcreator/skill-mcp)
- [Agent Skills spec (agentskills.io)](https://agentskills.io)
- [Vercel Labs skills (npx skills)](https://github.com/vercel-labs/skills)
- [Repository](https://github.com/kycloudtech/quickcreator-skills/tree/master/quickcreator-skill-builder)
