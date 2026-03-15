# Manage Skills — Browse, Copy, Edit, Delete

This document covers skill lifecycle operations other than creation and publishing. Referenced from [SKILL.md](../SKILL.md) when the user wants to browse, copy, edit, or delete skills.

For MCP tool details and usage rules, see [agent-technical-reference.md](agent-technical-reference.md).

---

## Browse & Search the Marketplace

- Call `list_marketplace_skills()` for an overview, or `search_marketplace(tag="...")` to find skills by topic
- Present results as a clean, readable list: skill name + what it does
- NEVER show skill IDs, file paths, or technical metadata to the user
- If user wants details: call `get_skill_tree(skillId=...)` and summarize in plain language
- For published version info: call `get_marketplace_skill_detail(marketplaceSkillId=...)`

---

## Create a Copy from an Existing Skill

Tell the user: "I'll create a personal copy of this skill so you can customize it."

1. Call `fork_skill_to_personal(skillId=..., source=...)` — internally handle the correct source type:
   - `marketplace` for marketplace skills (`mk_` prefix)
   - `builtin` for built-in skills (`sk_` prefix)
2. Call `get_skill_tree(skillId="p_...")` to inspect the copy
3. Ask the user what they want to change
4. Call `update_personal_skill_file(...)` to apply changes
5. Confirm: "Your customized version is ready!"

---

## Edit an Existing Skill

1. Call `list_personal_skills()` — show user their skills in a simple list
2. User picks which skill to edit
3. Call `get_skill_tree(skillId="p_...")` — summarize current content for the user
4. To read a specific file: call `get_skill_file(skillId=..., path="SKILL.md")`
5. Ask what they want to change
6. Call `update_personal_skill_file(skillId=..., path=..., content=...)` — apply changes
7. Confirm: "Changes saved!"

For content generation guidelines when rewriting skill content, see [skill-content-guide.md](skill-content-guide.md).

---

## Delete a Skill

Always confirm before deletion: "Are you sure you want to delete this skill? This action cannot be undone."

Then call `delete_personal_skill(skillId=...)`.

Only personal skills (`p_` prefix) can be deleted.

To remove a single file from a skill: call `delete_personal_skill_file(skillId=..., path=...)`.
