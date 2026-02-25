# QuickCreator Developer Skill

This skill teaches AI agents (Cursor, Windsurf, Claude Code, and other Cursor-compatible agents) how to develop, maintain, and publish skills for the [QuickCreator](https://www.quickcreator.io) platform using the [QuickCreator Skill MCP](https://www.npmjs.com/package/@quickcreator/skill-mcp).

**Repository:** [github.com/kycloudtech/quickcreator-skills/quickcreator-developer-skill](https://github.com/kycloudtech/quickcreator-skills/tree/master/quickcreator-developer-skill)  
**Latest release:** [Releases](https://github.com/kycloudtech/quickcreator-skills/releases) — download the latest `quickcreator-developer-skill` zip or the full repo zip and install as below.

---

## Prerequisites (for the skill to work)

1. **QuickCreator developer token**  
   Create one at [QuickCreator Agent Dev](https://agent-dev.quickcreator.io/demo/chat) → Settings → Create Token (read, write, publish).

2. **Skill MCP registered** in the agent’s MCP config (e.g. Cursor: `~/.cursor/mcp.json`) with **both** env vars:

   - `QC_API_TOKEN` = your developer token  
   - `QC_API_URL` = `https://api-dev.quickcreator.io/ai-blog-chat-service`  
     (Keep this until the MCP is officially production-ready; then remove it to use the default production URL.)

Example `mcp.json` entry:

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

Install the **entire** `quickcreator-developer-skill` folder (the one that contains `SKILL.md`) into the directory listed for your environment. Use **one** of the paths that apply.

| Agent / Product        | Skills directory (install target) | Notes |
|------------------------|-----------------------------------|--------|
| **Cursor**             | `~/.cursor/skills/`               | Global skills; same on macOS, Linux, Windows (`%USERPROFILE%\.cursor\skills\`). |
| **Cursor (project)**  | `<project_root>/.cursor/skills/`  | Project-only skill. |
| **Windsurf (Codeium)**| `~/.cursor/skills/` or product docs | If it uses Cursor-compatible skills, use the same path as Cursor; else check [Windsurf docs](https://docs.windsurf.com). |
| **Claude Code / Codex** | `$CODEX_HOME/skills/` or `~/.cursor/skills/` | Use the skills root your agent is configured to load from. |
| **Other Cursor-compatible agents** | That agent’s documented “skills” or “rules” directory | Ensure the folder contains `SKILL.md` and is the one the agent scans. |

**Resulting path examples**

- **Cursor (global, macOS/Linux):**  
  `~/.cursor/skills/quickcreator-developer-skill/SKILL.md`
- **Cursor (Windows):**  
  `%USERPROFILE%\.cursor\skills\quickcreator-developer-skill\SKILL.md`
- **Project-scoped (Cursor):**  
  `<your-project>/.cursor/skills/quickcreator-developer-skill/SKILL.md`

After installation, the agent should auto-discover the skill when the user asks to list, create, fork, publish, or manage QuickCreator skills.

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
- [Repository](https://github.com/kycloudtech/quickcreator-skills/tree/master/quickcreator-developer-skill)
