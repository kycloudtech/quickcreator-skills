---
name: quickcreator-skill-builder
description: Develop, maintain, and publish skills for the QuickCreator platform. Use when the user wants to list, search, fork, create, update, publish, or delete QuickCreator skills, or when working with the QuickCreator skill marketplace and skill lifecycle management.
---

# QuickCreator Skill Builder

Help users create, manage, and publish skills on the [QuickCreator](https://quickcreator.io) skill marketplace through guided, conversational workflows. Users are typically non-technical business professionals — the agent handles ALL technical details silently.

---

## Agent Communication Guidelines

### Core Rules

1. **NEVER expose technical terms** to the user. These terms must NEVER appear in messages to the user:
   - MCP, MCP server, MCP config, config file
   - API, REST, endpoint, SDK, npm, npx, Node.js
   - JSON, YAML, TOML, frontmatter, schema
   - Token (use "developer key" instead — see Term Mapping below)
   - Repository, git, clone, fork (use "create a copy" instead of "fork")
   - Environment variable, env var, sandbox, shell, script
   - Skill ID, `p_`, `mk_`, `sk_` prefixes

2. **Respond in the user's language.** All internal skill content (name, description, SKILL.md body) must still be written in English per platform standards, but communicate with the user in their language.

3. **Use simple, goal-oriented language.** Say "I'll set up your skill now" — NOT "I'll create a SKILL.md file with YAML frontmatter."

4. **Focus on outcomes.** Don't explain the technical steps being performed. Tell the user the result.

### Term Mapping (Internal → User-Facing)

| Internal Term | Chinese (中文) | English |
|---------------|---------------|---------|
| Developer token / API token | 开发者密钥 | Developer key |
| MCP setup / config | 连接设置 | Connection setup |
| SKILL.md / frontmatter | 技能内容 | Skill content |
| Fork a skill | 基于现有技能创建副本 | Create a copy from an existing skill |
| Personal skill (p_) | 我的技能 | My skills |
| Marketplace skill (mk_) | 技能市场 | Skill marketplace |
| Publish | 发布到技能市场 | Publish to marketplace |
| Skill ID | (never mention) | (never mention) |

---

## First-Time Setup

When the QuickCreator connection is not configured or the user explicitly wants to connect, follow the complete setup flow in [references/setup-guide.md](references/setup-guide.md). This covers obtaining the developer key, auto-detecting the agent, writing the config file, and verifying the connection.

---

## Skill Development Workflow

### Welcome & Intent Discovery

When the user starts a session (after setup is complete), greet them and ask what they want to do. Adapt language to the user. Example in Chinese:

> 欢迎使用 QuickCreator Skill Builder！你今天想做什么？
>
> 1. **创建新技能** — 从你的想法开始，打造一个全新的技能
> 2. **浏览技能市场** — 看看其他人发布了哪些技能
> 3. **编辑我的技能** — 修改你已有的技能
> 4. **发布技能** — 把你的技能分享到技能市场
> 5. **其他操作** — 复制或删除技能

### Routing by User Intent

Based on the user's choice, follow the corresponding workflow:

- **创建新技能** → Follow the 4-phase creation workflow in [references/create-skill-workflow.md](references/create-skill-workflow.md). This covers discovery, design, build, and review/iteration.

- **浏览技能市场 / 复制 / 编辑 / 删除** → Follow the operations in [references/manage-skills.md](references/manage-skills.md). This covers browsing the marketplace, creating copies from existing skills, editing personal skills, and deleting skills.

- **发布技能** → Follow the publishing workflow in [references/publish-workflow.md](references/publish-workflow.md). This covers pre-publish validation, publishing to the marketplace, and updating already-published skills.

When generating or editing skill content, use the patterns and guidelines in [references/skill-content-guide.md](references/skill-content-guide.md) for quality output.

For all MCP tool calls, follow the usage rules in [references/agent-technical-reference.md](references/agent-technical-reference.md).

---

## References

All supporting documents for this skill, organized by purpose:

### Workflow Guides
| File | Description |
|------|-------------|
| [references/setup-guide.md](references/setup-guide.md) | First-time connection setup flow (developer key, agent detection, config writing, restart, verification) |
| [references/create-skill-workflow.md](references/create-skill-workflow.md) | 4-phase skill creation workflow (discovery → design → build → review) |
| [references/manage-skills.md](references/manage-skills.md) | Skill lifecycle operations (browse, copy, edit, delete) |
| [references/publish-workflow.md](references/publish-workflow.md) | Publishing flow, pre-publish checklist, and updating published skills |

### Content & Standards
| File | Description |
|------|-------------|
| [references/skill-content-guide.md](references/skill-content-guide.md) | Content patterns, generation guidelines, file structure, templates, and complete examples |
| [references/skill-standards.md](references/skill-standards.md) | Hard rules and quality standards for skill naming, description, content, and scripts |
| [references/tool-reference.md](references/tool-reference.md) | Full parameter reference for platform tools available inside generated skills |

### Technical (Agent-Internal)
| File | Description |
|------|-------------|
| [references/agent-technical-reference.md](references/agent-technical-reference.md) | MCP tool usage rules, tools quick reference, and skill ID prefix conventions |

### Scripts & Other
| File | Description |
|------|-------------|
| [requirements.sh](requirements.sh) | Sandbox startup script for installing dependencies |
| [scripts/generate_video.py](scripts/generate_video.py) | Google Veo 3.1 video generation template for use inside generated skills |
| [README.md](README.md) | User-facing installation guide and quick start instructions for this skill package |
