---
layout: default
title: Skill Builder
nav_order: 3
description: "Core workflows and MCP tools for building QuickCreator skills."
---

# Skill Builder
{: .no_toc }

Core workflows and MCP tool reference for developing, publishing, and managing QuickCreator skills.
{: .fs-6 .fw-300 }

<details open markdown="block">
  <summary>Table of contents</summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

---

## MCP Tools Reference

The QuickCreator Skill MCP provides 13 tools for managing skills:

| Tool | Description |
|:-----|:------------|
| `list_skills` | List skills by category: `personal`, `builtin`, `marketplace`, `installed` |
| `search_marketplace` | Search marketplace by tag (sorted by publish time or downloads) |
| `get_skill` | Get skill detail and full file tree |
| `get_skill_file` | Read a specific file from any skill |
| `create_skill` | Create a new empty personal skill |
| `fork_skill` | Fork a builtin/marketplace/installed skill to personal |
| `update_skill_file` | Update a file in a personal skill |
| `create_skill_file` | Add a new file to a personal skill |
| `delete_skill` | Delete a personal skill |
| `publish_skill` | Publish a personal skill to the marketplace |
| `update_published_skill` | Update an existing marketplace listing |
| `install_skill` | Install a marketplace skill |
| `uninstall_skill` | Uninstall a marketplace skill |

### Skill ID Prefixes

| Prefix | Type | Access |
|:-------|:-----|:-------|
| `sk_` | Built-in | Read-only |
| `mk_` | Marketplace | Published by users |
| `p_` | Personal | Editable workspace |
| `i_` | Installed | Read-only copies |

---

## Core Workflows

### Browse & Discover

```python
list_skills(category="marketplace")    # Browse marketplace
list_skills(category="personal")       # View your skills
search_marketplace(tag="marketing")    # Search by tag
get_skill(skillId="mk_xxx")           # View skill details
```

### Create a New Skill

1. `create_skill(name="my-skill-name")` — creates an empty personal skill (`p_` prefixed)
2. `create_skill_file(...)` — add SKILL.md with proper frontmatter
3. Add reference files, scripts as needed via `create_skill_file`
4. **Before publishing**: run the [Pre-Publish Checklist](#pre-publish-checklist)
5. `publish_skill(personalSkillId="p_xxx")`

### Fork & Modify

1. `fork_skill(skillId="mk_xxx", source="marketplace")` — fork to personal
2. `get_skill(skillId="p_xxx")` — inspect the forked skill
3. `update_skill_file(...)` — modify files
4. Publish when ready

### Update an Existing Skill

1. `get_skill(skillId="p_xxx")` — read current state
2. `update_skill_file(...)` — modify files
3. If already published: `update_published_skill(marketplaceSkillId="mk_xxx", personalSkillId="p_xxx")`

### Delete

```python
delete_skill(personalSkillId="p_xxx")
```

---

## MCP Tool Usage Rules

{: .important }
Follow these rules to avoid common MCP errors (especially "Input validation error" / missing required fields).

### 1. Always Read the Tool Schema First

Before first use in a session, open the tool descriptor and inspect:
- `required` fields
- Allowed enums
- Whether an `arguments` object is mandatory

### 2. Always Pass the `arguments` Object

Even if only one field is required, you **must** pass `arguments:{...}`.

**Bad** (missing `category`, causes error):
```json
{
  "server": "quickcreator-skill",
  "toolName": "list_skills"
}
```

**Good:**
```json
{
  "server": "quickcreator-skill",
  "toolName": "list_skills",
  "arguments": { "category": "marketplace" }
}
```

### 3. Always Respect Enums and Field Names

- `list_skills.category` must be one of: `"personal"`, `"builtin"`, `"marketplace"`, `"installed"`
- `fork_skill` requires **both**: `skillId` and `source` (∈ `"marketplace"`, `"builtin"`, `"installed"`)

### 4. Use Explicit Examples

**list_skills:**
```json
{
  "server": "quickcreator-skill",
  "toolName": "list_skills",
  "arguments": { "category": "personal" }
}
```

**create_skill:**
```json
{
  "server": "quickcreator-skill",
  "toolName": "create_skill",
  "arguments": {
    "name": "ecommerce-product-image-batch",
    "description": "Generates e-commerce product images in batches."
  }
}
```

**publish_skill:**
```json
{
  "server": "quickcreator-skill",
  "toolName": "publish_skill",
  "arguments": {
    "personalSkillId": "p_xxx",
    "authorName": "Your Name",
    "tags": ["ecommerce", "images"],
    "version": "1.0.0"
  }
}
```

### 5. Fix Errors by Re-reading the Schema

On any MCP validation error, re-open the tool schema and fix arguments instead of retrying blindly. Look for:
- `expected` vs `received` types
- The property path (e.g. `["category"]`) to identify wrong or missing fields

---

## Skill File Structure

Every skill follows this layout:

```
skill-name/
├── SKILL.md              # Required — main instructions
├── reference.md          # Optional — detailed docs
├── examples.md           # Optional — usage examples
├── requirements.sh       # Required if scripts/ exists
└── scripts/              # Optional — utility scripts
    └── helper.py
```

### SKILL.md Template

```markdown
---
name: my-skill-name
description: Does X when the user needs Y. Use when working with Z.
---

# My Skill Name

## Instructions
Step-by-step guidance for the agent.

## Examples
Concrete usage examples.
```

---

## Pre-Publish Checklist

{: .warning }
Run this checklist before every `publish_skill` or `update_published_skill` call.

- [ ] `name` field: lowercase, hyphens, digits only; no leading/trailing/consecutive hyphens; ≤64 chars
- [ ] `description` field: English, ≤1024 chars, includes WHAT + WHEN + trigger keywords
- [ ] ALL content (headings, steps, notes, references) is in English
- [ ] No hardcoded API keys or secrets (use env vars)
- [ ] SKILL.md has valid YAML frontmatter with `name` and `description`
- [ ] SKILL.md body is under 500 lines
- [ ] Reference files are one level deep (linked directly from SKILL.md)
- [ ] If scripts/ exists: requirements.sh is present and lists all dependencies
- [ ] Consistent terminology throughout
- [ ] Follows [Agent Skills spec](https://agentskills.io)
