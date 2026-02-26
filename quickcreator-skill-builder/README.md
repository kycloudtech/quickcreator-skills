# QuickCreator Skill Builder

Create, manage, and publish skills on the [QuickCreator](https://www.quickcreator.io) skill marketplace — right from your AI assistant.

No coding required. Just describe your idea, and the AI assistant will handle everything: building the skill, setting up the content, and publishing it to the marketplace.

---

## Quick Start

### Step 1 — Install the skill

Put the `quickcreator-skill-builder` folder (containing `SKILL.md`) into your AI assistant's **skills directory**.

**Option A: Download manually**

Download from [this repository](https://github.com/kycloudtech/quickcreator-skills) and copy the `quickcreator-skill-builder` folder to the correct location (see table below).

**Option B: Use the skills CLI**

```bash
npx skills add https://github.com/kycloudtech/quickcreator-skills/tree/master/quickcreator-skill-builder
```

Use `-g` for global install; use `-a cursor -a claude-code` to target specific assistants.

#### Where to put the folder

Copy the **entire** `quickcreator-skill-builder` folder to one of these locations. **Global** = available in all projects; **Project** = only in that project.

| AI Assistant | Project path | Global path |
|-------------|--------------|-------------|
| **Cursor** | `.cursor/skills/` | `~/.cursor/skills/` |
| **Claude Code** | `.claude/skills/` | `~/.claude/skills/` |
| **Codex** | `.agents/skills/` | `~/.codex/skills/` |
| **OpenCode** | `.agents/skills/` | `~/.config/opencode/skills/` |
| **Windsurf** | `.windsurf/skills/` | `~/.codeium/windsurf/skills/` |
| **Cline** | `.cline/skills/` | `~/.cline/skills/` |
| **Continue** | `.continue/skills/` | `~/.continue/skills/` |
| **GitHub Copilot** | `.agents/skills/` | `~/.copilot/skills/` |
| **OpenClaw** | `skills/` | `~/.openclaw/skills/` |
| **OpenHands** | `.openhands/skills/` | `~/.openhands/skills/` |
| **Gemini CLI** | `.agents/skills/` | `~/.gemini/skills/` |

On Windows, replace `~` with `%USERPROFILE%`. For other assistants, see [agentskills.io](https://agentskills.io).

### Step 2 — Restart your AI assistant

Restart or reload your AI assistant so it picks up the new skill.

### Step 3 — Start using it

| AI Assistant | How to start |
|-------------|-------------|
| **Cursor** | Type `/` in chat → select `quickcreator-skill-builder` → press Enter |
| **OpenCode** | Type `/quickcreator-skill-builder` in chat → press Enter |
| **Claude Code** | Just say "I want to create a QuickCreator skill" |
| **Other** | Mention "QuickCreator skill" in your conversation |

**On first use**, the skill will guide you to get your **developer key** from QuickCreator and automatically set up the connection. This is a one-time setup — you won't need to do it again.

---

## What you can do

- **Create a new skill** — Describe your idea, and the assistant builds it for you
- **Browse the marketplace** — Discover skills published by others
- **Edit your skills** — Update and improve skills you've created
- **Publish to marketplace** — Share your skills with the community
- **Copy & customize** — Take an existing skill and make it your own
- **Install & uninstall** — Add or remove marketplace skills

---

## Getting your developer key

1. Visit [QuickCreator Developer Platform](https://agent-dev.quickcreator.io/demo/chat)
2. Log in or create a free account
3. Go to **Settings** → **Create Key**
4. Enable **read**, **write**, and **publish** permissions
5. Copy the key — you'll paste it when the skill asks for it

This is done once. The skill guides you through it on first use.

---

## Files in this package

| File | What it does |
|------|-------------|
| **SKILL.md** | Instructions for the AI assistant — loaded automatically |
| **skill-standards.md** | Content and format rules for QuickCreator skills |
| **tool-reference.md** | Reference for tools available to skills on the QuickCreator platform |
| **requirements.sh** | Dependency declarations for script-based skills |
| **scripts/generate_video.py** | Template for video generation capabilities |

---

## References

- [QuickCreator Platform](https://www.quickcreator.io)
- [Agent Skills Specification](https://agentskills.io)
- [QuickCreator Skill MCP (npm)](https://www.npmjs.com/package/@quickcreator/skill-mcp)
- [Skills CLI (npx skills)](https://github.com/vercel-labs/skills)
