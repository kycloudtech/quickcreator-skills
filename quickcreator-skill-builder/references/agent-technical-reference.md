# Agent-Internal: Technical Reference

**Everything in this document is for the agent's internal use. NEVER expose these details to the user.**

This document covers MCP tool usage rules, tool quick reference, and skill ID conventions. Referenced from [SKILL.md](../SKILL.md) and other workflow files when the agent needs to call MCP tools.

---

## MCP Tool Usage Rules

1. **Read the tool schema before first use** — check descriptor files for required fields and enums.
2. **Always pass `arguments` object** — even when only one field is required:
   ```json
   { "server": "quickcreator-skill", "toolName": "list_personal_skills", "arguments": {} }
   ```
3. **Respect enum values exactly** — e.g., `fork_skill_to_personal` `source` must be one of: `marketplace`, `builtin`.
4. **On validation errors**, re-read the tool schema and fix. Never retry blindly.

---

## MCP Tools Quick Reference

| Tool | Key Arguments |
|------|--------------|
| `list_personal_skills` | _(no arguments)_ |
| `list_builtin_skills` | _(no arguments)_ |
| `list_marketplace_skills` | optional: `tag`, `sortBy` ∈ publishTime/downloads, `offset`, `limit` |
| `search_marketplace` | optional: `tag`, `sortBy` ∈ publishTime/downloads, `offset`, `limit` |
| `get_skill_tree` | `skillId` |
| `get_skill_file` | `skillId`, `path` |
| `get_marketplace_skill_detail` | `marketplaceSkillId` |
| `create_personal_skill` | `name`, optional: `description` |
| `fork_skill_to_personal` | `skillId`, `source` ∈ marketplace/builtin |
| `update_personal_skill_file` | `skillId`, `path`, `content` |
| `create_personal_skill_file` | `skillId`, `path`, `content` |
| `delete_personal_skill_file` | `skillId`, `path` |
| `delete_personal_skill` | `skillId` |
| `publish_skill_version` | `personalSkillId`, optional: `marketplaceSkillId`, `authorName`, `tags`, `version` |
| `list_published_skill_versions` | `marketplaceSkillId` |
| `set_marketplace_latest_version` | `marketplaceSkillId`, `versionId` |
| `deprecate_skill_version` | `marketplaceSkillId`, `versionId` |

---

## Skill ID Prefixes

| Prefix | Type | Editable |
|--------|------|----------|
| `sk_` | Built-in | Read-only |
| `mk_` | Marketplace (published) | Read-only |
| `p_` | Personal | Editable |

Use the correct prefix when calling tools. Only `p_` skills can be edited, deleted, or published.
