---
layout: default
title: Home
nav_order: 1
description: "Build, publish, and manage skills for the QuickCreator platform using AI agents."
permalink: /
---

# QuickCreator Skill Builder
{: .fs-9 }

Build, publish, and manage skills for the QuickCreator platform using AI agents and the QuickCreator Skill MCP.
{: .fs-6 .fw-300 }

[Get Started](/quickcreator-skills/getting-started){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View on GitHub](https://github.com/kycloudtech/quickcreator-skills){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## What is QuickCreator Skill Builder?

The QuickCreator Skill Builder is an **agent skill** that lets your AI coding agent (Cursor, Claude Code, Codex, Windsurf, etc.) **develop and maintain QuickCreator skills**: list, search, create, fork, publish, and manage skills on the [QuickCreator](https://www.quickcreator.io) platform using the [QuickCreator Skill MCP](https://www.npmjs.com/package/@quickcreator/skill-mcp).

### Key Capabilities

| Capability | Description |
|:-----------|:------------|
| **Browse & Discover** | List and search skills across personal, built-in, marketplace, and installed categories |
| **Create** | Build new skills with the correct structure and `SKILL.md` |
| **Fork & Modify** | Fork marketplace or built-in skills to personal workspace and update files |
| **Publish** | Publish personal skills to the marketplace and update existing listings |
| **Install / Uninstall** | Manage marketplace skill installations |
| **Delete** | Remove personal skills |

### How It Works

The skill teaches your AI agent how to interact with the **QuickCreator Skill MCP** — a Model Context Protocol server that provides 13 tools for managing skills on the QuickCreator platform.

```
Your AI Agent  ──→  QuickCreator Skill MCP  ──→  QuickCreator Platform
  (Cursor, etc.)       (npm package)             (skills marketplace)
```

---

## Quick Install

**Using npx skills CLI:**

```bash
npx skills add https://github.com/kycloudtech/quickcreator-skills/tree/master/quickcreator-skill-builder
```

Use `-g` for global install; use `-a cursor -a claude-code` to target specific agents.

Or manually copy the `quickcreator-skill-builder` folder into your agent's skills directory. See [Getting Started](/quickcreator-skills/getting-started) for detailed instructions.

---

## Repository Files

| File | Purpose |
|:-----|:--------|
| **SKILL.md** | Instructions for the agent: how to use the MCP tools, workflows, and rules |
| **skill-standards.md** | QuickCreator skill content and format rules |
| **tool-reference.md** | Reference for tools available to skills on QuickCreator |
| **requirements.sh** | Dependencies declaration for scripts |
| **scripts/generate_video.py** | Template script for video generation (Veo) via `code_execute` |

---

## References

- [QuickCreator Skill MCP (npm)](https://www.npmjs.com/package/@quickcreator/skill-mcp)
- [Agent Skills spec (agentskills.io)](https://agentskills.io)
- [Vercel Labs skills (npx skills)](https://github.com/vercel-labs/skills)
- [QuickCreator Platform](https://www.quickcreator.io)
