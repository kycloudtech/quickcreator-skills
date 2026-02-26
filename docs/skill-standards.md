---
layout: default
title: Skill Standards
nav_order: 4
description: "Content and format standards for QuickCreator skills."
---

# Skill Development Standards
{: .no_toc }

All skills created, updated, or published on the QuickCreator platform MUST comply with these standards.
{: .fs-6 .fw-300 }

<details open markdown="block">
  <summary>Table of contents</summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

---

## Hard Rules (Non-Negotiable)

### 1. All Content in English

Every part of the skill — `name`, `description`, SKILL.md body, headings, step descriptions, notes, reference files — MUST be in English. This applies regardless of the user's language, conversation language, or source workflow language.

{: .note }
**Only exception**: Preserve non-English text that appears inside original prompts verbatim (e.g., a prompt designed to generate Chinese content keeps its Chinese examples intact).

### 2. `name` Field Specification

Must follow the [agentskills.io](https://agentskills.io) spec exactly:

| Rule | Example |
|:-----|:--------|
| Lowercase letters `a-z`, digits `0-9`, hyphens `-` only | `social-media-factory` ✅ |
| No uppercase | `Marketing-Email` ❌ |
| No spaces | `my skill` ❌ |
| No underscores | `marketing_email` ❌ |
| No unicode / non-ASCII | `个性化邮件` ❌ |
| Must not start or end with hyphen | `-my-skill-` ❌ |
| No consecutive hyphens | `my--skill` ❌ |
| Max 64 characters | — |
| Directory name must match `name` field | — |

### 3. `description` Field

- Max 1024 characters
- Written in English, third person
- Must describe **WHAT** the skill does AND **WHEN** to use it
- Include specific trigger keywords for agent discovery

**Good example:**
```
Generate personalized marketing emails based on customer segments
and product data. Use when the user needs email campaigns, drip
sequences, or promotional content tailored to audience segments.
```

**Bad example:**
```
Helps with emails.
```

### 4. No Hardcoded Secrets

All third-party API keys MUST be loaded from environment variables:

```python
# ✅ Correct
import os
api_key = os.environ["GOOGLE_API_KEY"]

# ❌ Wrong
api_key = "sk-abc123..."
```

Common env var names: `GOOGLE_API_KEY`, `OPENAI_API_KEY`, etc.

### 5. Agent Skills Spec Compliance

All generated skills must strictly follow the [Agent Skills specification](https://agentskills.io).

---

## SKILL.md Requirements

### Frontmatter

Every SKILL.md must have valid YAML frontmatter with exactly two fields:

```yaml
---
name: my-skill-name
description: Brief description of what this skill does and when to use it.
---
```

### Body Guidelines

| Requirement | Details |
|:------------|:--------|
| Max length | Under 500 lines |
| Instructions | Clear, step-by-step |
| Terminology | Consistent (pick one term, use it everywhere) |
| Time references | No time-sensitive information |
| Reference files | Linked one level deep from SKILL.md |
| Examples | Concrete, not abstract |

---

## Script Requirements

### requirements.sh

If the skill has a `scripts/` directory, a `requirements.sh` file MUST exist at the skill root. This file runs at sandbox startup (Ubuntu environment with standard Python).

```bash
#!/bin/bash
# Install Python packages
pip install google-genai pillow requests

# Install system packages if needed
apt-get update && apt-get install -y ffmpeg imagemagick
```

### Script Best Practices

| Practice | Details |
|:---------|:--------|
| Error handling | Include proper error handling in all scripts |
| Environment variables | Document expected env vars at the top of each script |
| Paths | Use absolute paths or paths relative to `/home/user/` |
| File mounting | Files in the sandbox are mounted at `/home/user/` |
| Timeout | Default 30s, max 300s (300000ms) |

---

## Quality Checklist

Before publishing or updating any skill:

- [ ] `name`: valid format (lowercase, hyphens, digits, ≤64 chars)
- [ ] `description`: English, ≤1024 chars, WHAT + WHEN + trigger keywords
- [ ] All content in English (except preserved prompt text)
- [ ] No hardcoded API keys or secrets
- [ ] Valid YAML frontmatter
- [ ] SKILL.md under 500 lines
- [ ] Reference files one level deep
- [ ] `requirements.sh` present if `scripts/` exists
- [ ] Consistent terminology
- [ ] Follows Agent Skills spec
