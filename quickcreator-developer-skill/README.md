# QuickCreator Developer Skill

This skill teaches AI agents (Cursor, Windsurf, Claude Code, and other Cursor-compatible agents) how to develop, maintain, and publish skills for the [QuickCreator](https://www.quickcreator.io) platform using the [QuickCreator Skill MCP](https://www.npmjs.com/package/@quickcreator/skill-mcp).

**Repository:** [github.com/kycloudtech/quickcreator-skills/quickcreator-developer-skill](https://github.com/kycloudtech/quickcreator-skills/tree/master/quickcreator-developer-skill)  
**Latest release:** [Releases](https://github.com/kycloudtech/quickcreator-skills/releases) — download the latest `quickcreator-developer-skill` zip or the full repo zip and install as below.

---

## Prerequisites (for the skill to work)

1. **QuickCreator developer token**  *(do this first)*  
   Create a token at [QuickCreator Agent Dev](https://agent-dev.quickcreator.io/demo/chat) → **Settings → Create Token** (select **read, write, publish**).  
   You will paste this value into the MCP config as `QC_API_TOKEN`.

2. **Create / update MCP config file** for the Skill MCP  
   For Cursor and most Cursor-compatible agents this is `~/.cursor/mcp.json` (create the file if it does not exist yet).  
   Register the `quickcreator-skill` MCP server with **both** env vars:

   - `QC_API_TOKEN` = your developer token  
   - `QC_API_URL` = `https://api-dev.quickcreator.io/ai-blog-chat-service`  
     (Keep this until the MCP is officially production-ready; then remove it to use the default production URL.)

Example `~/.cursor/mcp.json`:

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

---

## Installation (for AI agents)

Install by placing this skill into the **skills directory** used by your agent. The agent must support **Cursor-style skills** (a folder containing `SKILL.md`).

### Option A — From latest release (recommended)

1. Open [Releases](https://github.com/kycloudtech/quickcreator-skills/releases) and download the **latest** asset that contains this skill (e.g. `quickcreator-developer-skill-vX.Y.Z.zip` or the repo source zip).
2. Unzip it so you have a single folder named `quickcreator-developer-skill` (with `SKILL.md` inside).
3. Copy that folder into the correct **skills directory** for your agent (see table below).
4. Restart or reload the agent so it picks up the new skill.

### Option B — From repository

```bash
git clone --depth 1 https://github.com/kycloudtech/quickcreator-skills.git
cp -r quickcreator-skills/quickcreator-developer-skill "<SKILLS_DIR>/"
```

Replace `<SKILLS_DIR>` with the path for your agent from the table below.

---

## Where to install (by agent)

Install the **entire** `quickcreator-developer-skill` folder (the one that contains `SKILL.md`) into the skills directory used by your agent. Path conventions below follow the [open agent skills ecosystem](https://github.com/vercel-labs/skills) (Vercel Labs **npx skills**). Use **project** path for a single repo, **global** path for all projects.

### Install via npx skills (if you use the skills CLI)

If you already use [vercel-labs/skills](https://github.com/vercel-labs/skills), you can install this skill with:

```bash
# Direct path to this skill in the repo
npx skills add https://github.com/kycloudtech/quickcreator-skills/tree/master/quickcreator-developer-skill

# Global install (all projects)
npx skills add https://github.com/kycloudtech/quickcreator-skills/tree/master/quickcreator-developer-skill -g

# Target specific agents (e.g. Cursor + Claude Code)
npx skills add https://github.com/kycloudtech/quickcreator-skills/tree/master/quickcreator-developer-skill -a cursor -a claude-code
```

### Manual install — skills directory by agent

Copy the `quickcreator-developer-skill` folder into **Project path** (repo-scoped) or **Global path** (user-wide). On Windows, replace `~` with `%USERPROFILE%`.

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
| **Amp** | `.agents/skills/` | `~/.config/agents/skills/` |
| **Kimi Code CLI** | `.agents/skills/` | `~/.config/agents/skills/` |
| **Replit** | `.agents/skills/` | `~/.config/agents/skills/` |
| **Antigravity** | `.agent/skills/` | `~/.gemini/antigravity/skills/` |
| **Augment** | `.augment/skills/` | `~/.augment/skills/` |
| **OpenClaw** | `skills/` | `~/.openclaw/skills/` |
| **CodeBuddy** | `.codebuddy/skills/` | `~/.codebuddy/skills/` |
| **Command Code** | `.commandcode/skills/` | `~/.commandcode/skills/` |
| **Cortex Code** | `.cortex/skills/` | `~/.snowflake/cortex/skills/` |
| **Crush** | `.crush/skills/` | `~/.config/crush/skills/` |
| **Droid (Factory)** | `.factory/skills/` | `~/.factory/skills/` |
| **Gemini CLI** | `.agents/skills/` | `~/.gemini/skills/` |
| **Goose** | `.goose/skills/` | `~/.config/goose/skills/` |
| **Junie** | `.junie/skills/` | `~/.junie/skills/` |
| **iFlow CLI** | `.iflow/skills/` | `~/.iflow/skills/` |
| **Kilo Code** | `.kilocode/skills/` | `~/.kilocode/skills/` |
| **Kiro CLI** | `.kiro/skills/` | `~/.kiro/skills/` |
| **Kode** | `.kode/skills/` | `~/.kode/skills/` |
| **MCPJam** | `.mcpjam/skills/` | `~/.mcpjam/skills/` |
| **Mistral Vibe** | `.vibe/skills/` | `~/.vibe/skills/` |
| **Mux** | `.mux/skills/` | `~/.mux/skills/` |
| **Pi** | `.pi/skills/` | `~/.pi/agent/skills/` |
| **Qoder** | `.qoder/skills/` | `~/.qoder/skills/` |
| **Qwen Code** | `.qwen/skills/` | `~/.qwen/skills/` |
| **Roo Code** | `.roo/skills/` | `~/.roo/skills/` |
| **Trae** | `.trae/skills/` | `~/.trae/skills/` |
| **Trae CN** | `.trae/skills/` | `~/.trae-cn/skills/` |
| **Zencoder** | `.zencoder/skills/` | `~/.zencoder/skills/` |
| **Neovate** | `.neovate/skills/` | `~/.neovate/skills/` |
| **Pochi** | `.pochi/skills/` | `~/.pochi/skills/` |
| **AdaL** | `.adal/skills/` | `~/.adal/skills/` |

**Examples**

- **Cursor (global, macOS/Linux):** `~/.cursor/skills/quickcreator-developer-skill/`
- **Cursor (Windows):** `%USERPROFILE%\.cursor\skills\quickcreator-developer-skill\`
- **Claude Code (project):** `<project_root>/.claude/skills/quickcreator-developer-skill/`
- **Windsurf (global):** `~/.codeium/windsurf/skills/quickcreator-developer-skill/`

After installation, the agent should auto-discover the skill when the user asks to list, create, fork, publish, or manage QuickCreator skills. **MCP config** (`~/.cursor/mcp.json` or your agent’s MCP config path) must still be set up with `QC_API_TOKEN` and `QC_API_URL` as in [Prerequisites](#prerequisites-for-the-skill-to-work).

---

## What this skill does

- **List / search** personal, built-in, marketplace, and installed skills.
- **Create** new QuickCreator skills (with correct `SKILL.md` and structure).
- **Fork** marketplace/built-in/installed skills to personal and **update** files.
- **Publish** personal skills to the marketplace and **update** existing listings.
- **Install / uninstall** marketplace skills.
- **Delete** personal skills.
- Enforces QuickCreator skill standards and pre-publish checklist; references MCP tool schemas to avoid invalid arguments.

---

## References

- [QuickCreator Skill MCP (npm)](https://www.npmjs.com/package/@quickcreator/skill-mcp)
- [Agent Skills spec (agentskills.io)](https://agentskills.io)
- [Vercel Labs skills (npx skills)](https://github.com/vercel-labs/skills) — agent paths and install via `npx skills add`
- [Repository](https://github.com/kycloudtech/quickcreator-skills/tree/master/quickcreator-developer-skill)
