# Publish Workflow

This document covers publishing skills to the marketplace and updating already-published skills. Referenced from [SKILL.md](../SKILL.md) when the user wants to publish or update a skill.

For development standards that skills must meet before publishing, see [skill-standards.md](skill-standards.md).

---

## Pre-Publish Checklist (Agent Enforced Silently)

The agent MUST run this checklist and fix all issues automatically before publishing. **Never show this checklist to the user or burden them with details.**

- `name`: lowercase a-z, 0-9, hyphens only; ≤64 chars; no leading/trailing/consecutive hyphens
- `description`: English, ≤1024 chars, describes WHAT + WHEN + trigger keywords
- All SKILL.md content in English (except preserved non-English text in original prompts)
- No hardcoded API keys or secrets (use environment variables)
- Valid YAML frontmatter with `name` and `description`
- SKILL.md body under 500 lines
- Reference files one level deep
- `requirements.sh` present if `scripts/` directory exists
- Consistent terminology throughout
- Follows [Agent Skills spec](https://agentskills.io)

Full validation rules are documented in [skill-standards.md](skill-standards.md).

---

## Publish to the Marketplace

1. Silently run the pre-publish checklist above and auto-fix any issues
2. Ask the user for:
   - **Author name** — suggest using their account name
   - **Tags** — suggest relevant tags based on skill content (e.g., `marketing`, `image`, `social-media`)
3. Call `publish_skill_version(personalSkillId=..., authorName=..., tags=[...], version="1.0.0")`
4. Confirm: "Your skill is now live on the marketplace! Others can find and install it."

---

## Update an Already-Published Skill

When the user wants to update a skill they've already published:

1. Silently run the pre-publish checklist and auto-fix any issues
2. Confirm the changes with the user: "I'll publish a new version with these updates. Ready?"
3. Call `publish_skill_version(personalSkillId=..., marketplaceSkillId=..., version="x.y.z")`
   - If `marketplaceSkillId` is provided, this publishes a new version to the existing package
   - Increment the version number (e.g., `1.0.0` → `1.1.0` for minor updates)
4. Confirm: "Your skill has been updated!"

---

## Manage Published Versions

For users who want to manage versions of a published skill:

- **List versions**: Call `list_published_skill_versions(marketplaceSkillId=...)`
- **Switch active version**: Call `set_marketplace_latest_version(marketplaceSkillId=..., versionId=...)` to promote an older version as the current latest
- **Deprecate a version**: Call `deprecate_skill_version(marketplaceSkillId=..., versionId=...)` to mark an old version as deprecated

Present version lists to the user in plain language (e.g., "version 1.2.0, published March 15"). Never expose version IDs.
