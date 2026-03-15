# Create a New Skill — Workflow

This document covers the complete 4-phase workflow for creating a new skill. Referenced from [SKILL.md](../SKILL.md) when the user wants to create a skill from scratch.

For content patterns, templates, and examples to use during skill generation, see [skill-content-guide.md](skill-content-guide.md).

---

## Inferring from Conversation Context

If previous conversation provides context (e.g., the user described a workflow, demonstrated a process, or discussed a problem), **proactively offer** to turn that into a skill:
> "Based on what we just discussed, I can create a skill that [does X]. Would you like me to build it?"

This saves the user from re-explaining. Skip directly to Phase 2 if enough context exists.

---

## Phase 1: Discovery

Have a natural dialogue. Ask ONE question at a time — never dump all questions at once. Use AskQuestion tool for structured choices when available; otherwise ask conversationally.

1. **Purpose**: "What do you want this skill to help people accomplish?"
2. **Target users**: "Who would use this skill? What problem does it solve for them?"
3. **Workflow steps**: "Walk me through the ideal process step by step."
4. **Capabilities needed** — Offer as concrete choices, not open-ended:
   - "Should it generate images?"
   - "Should it search the internet for information?"
   - "Should it ask the user questions during the process?"
   - "Should it access the user's knowledge base?"
   - "Should it create videos?"
5. **Output expectations**: "What should the final result look like? Any specific format or style?"
6. **Examples**: "Can you show me a sample input and what the ideal result looks like?"

If the user wants inspiration, call `search_marketplace(tag=...)` or `list_builtin_skills()` and present relevant results in plain language.

---

## Phase 2: Design

The agent silently designs the skill, then presents a brief summary for confirmation:

> "Here's what I'll build: **[skill concept in user's language]**. It will [do X, Y, Z]. Does that sound right?"

Wait for user confirmation before proceeding. If the user wants adjustments, iterate on the design.

Internally, the agent:
1. Generates a valid `name` (lowercase, hyphens, ≤64 chars) — see [skill-standards.md](skill-standards.md) for naming rules
2. Writes an English `description` (≤1024 chars, WHAT + WHEN + triggers) — translate from user's language if needed
3. Selects appropriate content patterns from [skill-content-guide.md](skill-content-guide.md)
4. Plans the file structure

---

## Phase 3: Build

The agent silently creates the skill:
1. `create_personal_skill(name=..., description=...)` — see [agent-technical-reference.md](agent-technical-reference.md) for tool usage
2. `create_personal_skill_file(skillId=..., path="SKILL.md", content=...)` — SKILL.md with proper frontmatter and content using selected patterns
3. Adds reference files or scripts as needed using additional `create_personal_skill_file` calls

When generating SKILL.md content, follow the guidelines and patterns in [skill-content-guide.md](skill-content-guide.md).

For available platform tools to include in the generated skill, see [tool-reference.md](tool-reference.md).

---

## Phase 4: Review & Iterate

Present the result in plain language: "Your skill is ready! Here's what it does: [summary in user's language]."

Ask: "Would you like to adjust anything, or publish it right away?"

If the user wants changes, iterate using `update_personal_skill_file(...)` until satisfied. Each time, confirm the change: "Done! Here's what I updated: [change summary]."

If the user wants to publish immediately, follow the workflow in [publish-workflow.md](publish-workflow.md).
