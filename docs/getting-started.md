---
layout: default
title: Getting Started
nav_order: 2
description: "Install the QuickCreator Skill Builder and start creating skills."
---

# Getting Started
{: .no_toc }

Install the skill, restart your AI assistant, and you're ready to go. The skill handles everything else automatically.
{: .fs-6 .fw-300 }

<details open markdown="block">
  <summary>Table of contents</summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

---

## Step 1 — Install the Skill

Put the `quickcreator-skill-builder` folder (containing `SKILL.md`) into your AI assistant's **skills directory**.

### Option A: Using the skills CLI

```bash
npx skills add https://github.com/kycloudtech/quickcreator-skills/tree/master/quickcreator-skill-builder
```

Use `-g` for global install; use `-a cursor -a claude-code` to target specific assistants.

### Option B: Manual download

1. Download from [the repository](https://github.com/kycloudtech/quickcreator-skills)
2. Copy the `quickcreator-skill-builder` folder into the appropriate skills directory for your assistant

### Skills directory by assistant

Copy the **entire** `quickcreator-skill-builder` folder to one of the paths below. **Global** = available in all projects; **Project** = only in that project. On Windows, replace `~` with `%USERPROFILE%`.

| AI Assistant | Project path | Global path |
|:-------------|:-------------|:------------|
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

For other assistants, see [agentskills.io](https://agentskills.io).

---

## Step 2 — Restart Your AI Assistant

After installing the skill, restart your AI assistant so it can discover the new skill.

---

## Step 3 — Start Using It

| AI Assistant | How to start |
|:-------------|:-------------|
| **Cursor** | Type `/` in chat → select `quickcreator-skill-builder` → press Enter |
| **OpenCode** | Type `/quickcreator-skill-builder` in chat → press Enter |
| **Claude Code** | Just say "I want to create a QuickCreator skill" |
| **Other** | Mention "QuickCreator skill" in your conversation |

---

## First-Time Setup (Automatic)

On your first use, the skill will guide you through a one-time connection setup:

1. **Get your developer key** — The skill will direct you to the [QuickCreator Developer Platform](https://agent-dev.quickcreator.io/demo/chat) where you can create a key in **Settings → Create Key** (enable read, write, and publish permissions)
2. **Paste the key** — Share it with the assistant when prompted
3. **Automatic connection** — The assistant sets up everything behind the scenes
4. **Restart once more** — The assistant will tell you when to restart to activate the connection

After this one-time setup, you can use the skill immediately every time — no further configuration needed.

{: .tip }
You only need to do this setup once. The next time you use the skill, it will connect automatically.

---

## What's Next?

Once connected, you can:

- **Create a new skill** — Describe your idea and the assistant builds it
- **Browse the marketplace** — See what others have published
- **Edit your skills** — Update skills you've already created
- **Publish** — Share your skills with the community

See the [Skill Builder Guide](/skill-builder) for a detailed walkthrough.
