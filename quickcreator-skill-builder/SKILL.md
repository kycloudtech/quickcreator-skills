---
name: quickcreator-skill-builder
description: Develop, maintain, and publish skills for the QuickCreator platform. Use when the user wants to list, search, fork, create, update, publish, or delete QuickCreator skills, or when working with the QuickCreator skill marketplace and skill lifecycle management.
---

# QuickCreator Skill Builder

This skill teaches the agent to develop and maintain QuickCreator skills (list, create, fork, publish, install, delete) using the **QuickCreator Skill MCP**.

## Prerequisites (user must have done this)

This skill only works if the **QuickCreator Skill MCP** is set up:

1. **Developer token** — The user has a QuickCreator developer token (from [QuickCreator Agent Dev](https://agent-dev.quickcreator.io/demo/chat) → Settings → Create Token, with read/write/publish).
2. **MCP config** — The `quickcreator-skill` MCP server is added to the user's agent config with `QC_API_TOKEN` and `QC_API_URL`.

**If the user has not set this up:** Guide them to the repository [README](https://github.com/kycloudtech/quickcreator-skills/tree/master/quickcreator-skill-builder). The README has step-by-step instructions (get token → add MCP to the config file for their agent). You can also perform those steps: read the README, identify the MCP config path for their agent from the table, and add or merge the `quickcreator-skill` entry with the user's token. Do not duplicate the full path table or JSON/TOML examples here—they are in the README.

---

## MCP Tools Reference

| Tool | Description |
|------|-------------|
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

### MCP Tool Usage Rules (VERY IMPORTANT)

To avoid common MCP errors (especially \"Input validation error\" / missing required fields), **always follow these rules when calling `quickcreator-skill` tools**:

1. **Always read the tool schema before first use in a session**
   - Open the tool descriptor for the QuickCreator MCP server (e.g. in Cursor this may be under a path like `mcps/<mcp-server-id>/tools/<tool_name>.json`; in other agents, check where MCP tool schemas are exposed or use the agent’s tool documentation).
   - Inspect:
     - `required` fields
     - Allowed enums
     - Whether an `arguments` object is mandatory

2. **Never call `CallMcpTool` without an `arguments` object when the schema defines any properties**
   - Even if only one field is required, you **must** pass `arguments:{...}`.
   - Bad (missing `category`, causes `invalid_type` / `Required` error):
     ```json
     {
       "server": "quickcreator-skill",
       "toolName": "list_skills"
     }
     ```
   - Good:
     ```json
     {
       "server": "quickcreator-skill",
       "toolName": "list_skills",
       "arguments": { "category": "marketplace" }
     }
     ```

3. **Always respect enums and field names from the schema**
   - Example: `list_skills.category` must be **one of**  
     `"personal" | "builtin" | "marketplace" | "installed"`.
   - Example: `fork_skill` requires **both**:
     - `skillId` (e.g. `"mk_XXXX"`, `"p_XXXX"`, `"i_XXXX"`, `"sk_XXXX"`)
     - `source` ∈ `"marketplace" | "builtin" | "installed"`.

4. **Use explicit examples for each core tool**
   - `list_skills`:
     ```json
     {
       "server": "quickcreator-skill",
       "toolName": "list_skills",
       "arguments": { "category": "personal" }
     }
     ```
   - `create_skill`:
     ```json
     {
       "server": "quickcreator-skill",
       "toolName": "create_skill",
       "arguments": {
         "name": "ecommerce-product-image-batch",
         "description": "Generates e-commerce product images in batches from text prompts or product data."
       }
     }
     ```
   - `publish_skill`:
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

5. **On any MCP validation error, re-open the tool schema and fix arguments instead of retrying blindly**
   - Look for:
     - `expected` vs `received` types in the error
     - The property path (e.g. `["category"]`) to see which field is wrong or missing.

These rules are specifically to prevent the most frequent mistakes seen when driving QuickCreator via MCP.

### Skill ID Prefixes

| Prefix | Type | Access |
|--------|------|--------|
| `sk_` | Built-in | Read-only |
| `mk_` | Marketplace | Published by users |
| `p_` | Personal | Editable workspace |
| `i_` | Installed | Read-only copies |

---

## Core Workflows

### Browse & Discover

```
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

```
delete_skill(personalSkillId="p_xxx")
```

---

## Skill Development Standards

**ALL skills created or updated MUST comply with these standards.** Read [skill-standards.md](skill-standards.md) for the full specification.

### Hard Rules (Quick Reference)

1. **ALL content in English** — `name`, `description`, SKILL.md body, headings, step descriptions, notes, reference files. The ONLY exception: preserving non-English text inside original prompts verbatim.

2. **`name` field format** — lowercase `a-z`, digits `0-9`, hyphens `-` only. No uppercase, spaces, underscores, or unicode. Must not start/end with hyphen. No consecutive hyphens. Max 64 chars. Directory name must match.

3. **`description` field** — max 1024 chars, English, third-person. Describe WHAT and WHEN. Include trigger keywords.

4. **No hardcoded secrets** — all API keys loaded from environment variables.

5. **Follow [Agent Skills spec](https://agentskills.io)** strictly.

### Script Requirements

If a skill has a `scripts/` directory, include a `requirements.sh` file that declares all dependencies. The sandbox is Ubuntu with standard Python pre-installed.

```bash
#!/bin/bash
# requirements.sh — runs at sandbox startup
pip install google-genai requests
apt-get update && apt-get install -y jq
```

---

## Pre-Publish Checklist

**Run this checklist before every `publish_skill` or `update_published_skill` call.**

```
Publish Readiness:
- [ ] `name` field: lowercase, hyphens, digits only; no leading/trailing/consecutive hyphens; ≤64 chars
- [ ] `description` field: English, ≤1024 chars, includes WHAT + WHEN + trigger keywords
- [ ] ALL content (headings, steps, notes, references) is in English
- [ ] No hardcoded API keys or secrets (use env vars)
- [ ] SKILL.md has valid YAML frontmatter with `name` and `description`
- [ ] SKILL.md body is under 500 lines
- [ ] Reference files are one level deep (linked directly from SKILL.md)
- [ ] If scripts/ exists: requirements.sh is present and lists all dependencies
- [ ] Consistent terminology throughout
- [ ] Follows Agent Skills spec (https://agentskills.io)
```

If any item fails, fix it before publishing.

---

## Available Tools for Generated Skills

Generated skills can use built-in tools within the QuickCreator platform. For the full parameter reference, see [tool-reference.md](tool-reference.md).

| Tool | Purpose |
|------|---------|
| `nano-banana-pro-image` | Text-to-image and image-to-image generation |
| `openai-image` | AI image generation from text prompts |
| `query_image_from_knowledge_base` | Query images from user knowledge base |
| `query_question_from_knowledge_base` | Retrieve information from knowledge base |
| `query_question_from_web` | Web search and research |
| `ask_questions_to_user` | Structured user input collection |
| `shell_execute` | Execute bash shell scripts in sandbox |
| `code_execute` | Execute Python or JavaScript code in sandbox |

### Video Generation

Video generation uses **Google Veo SDK via `code_execute`** — do NOT use a `generate_video` tool. A reusable template is at [scripts/generate_video.py](scripts/generate_video.py). See [tool-reference.md](tool-reference.md) for full Veo parameter docs.

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
description: Does X when the user needs Y. Use when working with Z or when the user mentions A, B, or C.
---

# My Skill Name

## Instructions
Step-by-step guidance for the agent.

## Examples
Concrete usage examples.
```
