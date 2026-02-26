---
layout: default
title: Home
nav_order: 1
description: "Create and publish skills for QuickCreator — no coding required."
permalink: /
---

# QuickCreator Skill Builder
{: .fs-9 }

Create and publish skills for the [QuickCreator](https://www.quickcreator.io) skill marketplace — right from your AI assistant. No coding required.
{: .fs-6 .fw-300 }

[Get Started](/quickcreator-skills/getting-started){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View on GitHub](https://github.com/kycloudtech/quickcreator-skills){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## What is it?

The QuickCreator Skill Builder lets you **create, manage, and publish skills** on the QuickCreator skill marketplace — all through a natural conversation with your AI assistant (Cursor, OpenCode, Claude Code, Windsurf, and more).

Just describe your idea, and the AI assistant handles everything: naming, structuring, building, and publishing.

### What you can do

| | |
|:--|:--|
| **Create a new skill** | Describe your idea, and the assistant builds it for you |
| **Browse the marketplace** | Discover skills published by others |
| **Edit your skills** | Update and improve skills you've created |
| **Publish to marketplace** | Share your skills with the community |
| **Copy & customize** | Take an existing skill and make it your own |
| **Install & uninstall** | Add or remove marketplace skills |

### How it works

```
You describe your idea  →  AI assistant builds the skill  →  Publish to marketplace
```

Your AI assistant understands what you want, creates the skill content, and handles all the technical details behind the scenes.

---

## Quick Install

**Using the skills CLI:**

```bash
npx skills add https://github.com/kycloudtech/quickcreator-skills/tree/master/quickcreator-skill-builder
```

Use `-g` for global install; use `-a cursor -a claude-code` to target specific assistants.

Or manually copy the `quickcreator-skill-builder` folder into your assistant's skills directory. See [Getting Started](/quickcreator-skills/getting-started) for detailed instructions.

---

## How to use after installation

| AI Assistant | How to start |
|:-------------|:-------------|
| **Cursor** | Type `/` in chat → select `quickcreator-skill-builder` → press Enter |
| **OpenCode** | Type `/quickcreator-skill-builder` in chat → press Enter |
| **Claude Code** | Just say "I want to create a QuickCreator skill" |
| **Other** | Mention "QuickCreator skill" in your conversation |

On first use, the skill will guide you to get your **developer key** from QuickCreator and automatically set up the connection. This is a one-time step.

---

## References

- [QuickCreator Platform](https://www.quickcreator.io)
- [Agent Skills Specification](https://agentskills.io)
- [QuickCreator Skill MCP (npm)](https://www.npmjs.com/package/@quickcreator/skill-mcp)
- [Skills CLI (npx skills)](https://github.com/vercel-labs/skills)
