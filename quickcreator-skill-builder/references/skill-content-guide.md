# Skill Content Generation Guide

This document provides guidelines, patterns, templates, and examples for generating skill content. Referenced from [SKILL.md](../SKILL.md) and [create-skill-workflow.md](create-skill-workflow.md) when the agent needs to write or edit SKILL.md content for a user's skill.

For platform tool parameters to use inside generated skills, see [tool-reference.md](tool-reference.md).
For hard rules and validation standards, see [skill-standards.md](skill-standards.md).

---

## Content Generation Principles

**Conciseness first**: Only include information the agent wouldn't already know. Every paragraph must justify its token cost. Avoid explaining what common tools do — just say how to use them.

**Progressive disclosure**: Put essential step-by-step instructions in SKILL.md. Detailed API references, extensive examples, or supplementary docs go in separate files (reference.md, examples.md) linked from SKILL.md. Keep references one level deep.

**Match freedom to fragility**:
- **High freedom** (text guidelines) — multiple valid approaches (e.g., content review, creative writing)
- **Medium freedom** (templates/outlines) — preferred pattern with acceptable variation (e.g., report generation)
- **Low freedom** (exact scripts/steps) — consistency is critical (e.g., data pipelines, image specs)

---

## Content Patterns

Select the best pattern based on what the skill does. Combine patterns as needed — most skills benefit from Workflow + Template.

### Template Pattern

Use when the skill produces structured output:
```
## Output format
# [Title]
## Summary: [one-paragraph overview]
## Details: [structured content]
```

### Workflow Pattern

Use when the skill follows sequential steps:
```
## Process
Step 1: [Action] — [what to do and why]
Step 2: [Action] — [what to do and why]
Step 3: [Action] — [what to do and why]
```

### Conditional Pattern

Use when the skill handles different scenarios:
```
## Determine the approach
**Scenario A?** → Follow "Approach A"
**Scenario B?** → Follow "Approach B"
```

### Examples Pattern

Use when output quality depends on seeing examples:
```
## Examples
**Input:** [sample input]
**Output:** [expected output]
```

### Feedback Loop Pattern

Use when quality verification is needed:
```
## Process
1. Generate the output
2. Validate the result
3. If issues found → fix and re-validate
4. Only proceed when validation passes
```

---

## Available Platform Tools

Skills running on QuickCreator can use these built-in tools. See [tool-reference.md](tool-reference.md) for full parameter reference.

| Tool | Capability |
|------|-----------|
| `nano-banana-pro-image` | Image generation (text-to-image, image-to-image) |
| `openai-image` | AI image generation from text prompts |
| `query_image_from_knowledge_base` | Retrieve images from user's knowledge base |
| `query_question_from_knowledge_base` | Retrieve information from user's knowledge base |
| `query_question_from_web` | Web search and research |
| `fetch_google_search` | Fetch Google search results with filters (time, locale, language) |
| `get_info_from_webpage` | Analyze and extract information from a specific web page |
| `scrape_webpage` | Scrape a web page and return content in markdown format |
| `ask_questions_to_user` | Structured user input collection |
| `shell_execute` | Run bash scripts in sandbox |
| `code_execute` | Run Python or JavaScript in sandbox |

Video generation uses Google Veo SDK via `code_execute`. See [../scripts/generate_video.py](../scripts/generate_video.py) and [tool-reference.md](tool-reference.md).

---

## Skill File Structure

```
skill-name/
├── SKILL.md              # Required — main instructions
├── reference.md          # Optional — detailed docs
├── examples.md           # Optional — usage examples
├── requirements.sh       # Required if scripts/ exists
└── scripts/              # Optional
    └── helper.py
```

---

## SKILL.md Template

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

---

## Complete Example

A well-structured skill for the QuickCreator platform:

```markdown
---
name: product-social-post
description: Generate social media posts with AI images for product promotion. Use when the user needs product marketing content, social media posts, or promotional images for Instagram, Facebook, or Twitter.
---

# Product Social Post

## Instructions

1. Ask the user which product they want to promote. Use `ask_questions_to_user` with:
   - Product name (short answer)
   - Target platform (single choice: Instagram / Facebook / Twitter)
   - Tone (single choice: Professional / Casual / Playful)

2. Search for product information using `query_question_from_knowledge_base` with the product name.

3. Generate a promotional image using `nano-banana-pro-image` with a prompt based on the product and selected tone.

4. Write platform-appropriate post copy:
   - Instagram: visual-first, hashtags, emoji
   - Facebook: conversational, longer format
   - Twitter: concise, punchy, under 280 chars

5. Present the image and copy to the user for review.

## Examples

**Input:** Product: "CloudSync Pro", Platform: Instagram, Tone: Professional
**Output:**
- Image: Clean product mockup with gradient background
- Copy: "Seamless collaboration starts here. CloudSync Pro keeps your team in sync — anywhere, anytime. #CloudSync #Productivity #TeamWork"
```
