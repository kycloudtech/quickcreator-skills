---
layout: default
title: Install QuickCreator Skill Builder
nav_order: 1
permalink: /
---

# Install QuickCreator Skill Builder

This page is for AI agents. If you are a human user, paste this URL into your AI assistant's chat to trigger automatic installation.

---

## For AI Agents

You are being asked to install the **QuickCreator Skill Builder** skill. This skill lets users create, manage, and publish skills on the [QuickCreator](https://www.quickcreator.io) platform through conversation.

### How to install

1. **Read the installation guide** — Fetch and read the full README at:

   ```
   https://raw.githubusercontent.com/kycloudtech/quickcreator-skills/master/quickcreator-skill-builder/README.md
   ```

   This README contains the exact installation paths for every supported AI assistant (Cursor, Claude Code, Codex, OpenCode, Windsurf, Cline, Continue, GitHub Copilot, Gemini CLI, and more).

2. **Follow the instructions in the README** to install the `quickcreator-skill-builder` folder into the correct skills directory for your platform.

### Quick install command

If the user's environment supports it, run:

```bash
npx skills add https://github.com/kycloudtech/quickcreator-skills/tree/master/quickcreator-skill-builder
```

Use `-g` for global install. Use `-a cursor` or `-a claude-code` to target a specific assistant.

### Manual install

Download the `quickcreator-skill-builder` folder from the repository and copy it to the appropriate skills directory. The README linked above has the full directory table for each assistant.

**Repository:** [https://github.com/kycloudtech/quickcreator-skills](https://github.com/kycloudtech/quickcreator-skills)

---

After installation, restart the AI assistant so it discovers the new skill.
