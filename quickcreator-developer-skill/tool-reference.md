# Available Tools for Generated Skills

These built-in tools are available for skills running on the QuickCreator platform.

## Image Generation

### `nano-banana-pro-image`

Text-to-image and image-to-image generation.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | **Yes** | Text prompt for generation or editing |
| `image_urls` | string[]\|null | No | Source image URLs for image-to-image |

### `openai-image`

AI image generation from text prompts.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | **Yes** | — | Detailed text prompt |
| `size` | enum | No | `1024x1024` | `1024x1024`, `1536x1024` (landscape), `1024x1536` (portrait) |
| `quality` | enum | No | `medium` | `low`, `medium`, `high` |

---

## Knowledge Base

### `query_image_from_knowledge_base`

Query images from user knowledge base.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | **Yes** | S3 file key in the knowledge base |

### `query_question_from_knowledge_base`

Retrieve and synthesize information from knowledge base.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `question` | string | **Yes** | Query question, preferably in question format |

---

## Web Search

### `query_question_from_web`

Web search and research.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `question` | string | **Yes** | — | Query question; AI combines online content to answer |
| `search_after_date_filter` | string\|null | No | null | Only return content after this date (MM/DD/YYYY) |
| `search_domain_filter` | string[]\|null | No | null | Limit search domains (max 10); prefix `-` to exclude |
| `user_location_country_code` | string\|null | No | null | ISO 3166-1 alpha-2 country code for localized search |

---

## User Interaction

### `ask_questions_to_user`

Structured user input collection.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `questions` | Question[] | **Yes** | Array of question objects |

**Question object:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `question` | string | **Yes** | Question text |
| `question_type` | enum | **Yes** | `single_choice_question`, `multiple_choice_question`, `short_answer_question` |
| `options` | string[] | **Yes** | Options list; must be `[]` for short answer |
| `need_other_option` | boolean | **Yes** | Add "Other" free-input option; must be `false` for short answer |

---

## Code Execution

### `shell_execute`

Execute bash scripts in the sandbox.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `script` | string | **Yes** | — | Shell script to execute |
| `skill_id` | string | **Yes** | — | Skill ID; files mounted at `/home/user/` |
| `timeout` | number\|null | No | 30000 | Timeout in ms, max 300000 |

### `code_execute`

Execute Python or JavaScript code in the sandbox.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `code` | string | **Yes** | — | Code to execute |
| `skill_id` | string | **Yes** | — | Skill ID; files mounted at `/home/user/` |
| `language` | enum\|null | No | `python` | `python` or `javascript` |
| `timeout` | number\|null | No | 30000 | Timeout in ms, max 300000 |

---

## Video Generation (Google Veo SDK)

**Do NOT use a `generate_video` tool.** Use `code_execute` to run Python code calling the Google Veo 3.1 SDK.

**Prerequisite**: `GOOGLE_API_KEY` env var must be set. The `google-genai` package must be installed (add to `requirements.sh`).

A reusable template script is provided at [scripts/generate_video.py](../scripts/generate_video.py).

### Veo 3.1 Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string | — | Text prompt (required) |
| `image` | Image | None | Starting frame for image-to-video |
| `last_frame` | Image | None | Ending frame (must be used with `image`) for interpolation |
| `reference_images` | list | None | Up to 3 reference images (cannot be used with `image`) |
| `config.aspect_ratio` | `16:9`\|`9:16` | `16:9` | Aspect ratio |
| `config.resolution` | `720p`\|`1080p`\|`4k` | `720p` | Resolution |
| `config.duration_seconds` | `4`\|`6`\|`8` | `8` | Duration in seconds |
| `config.negative_prompt` | string | None | Content exclusion |
| `config.person_generation` | string | — | `allow_adult` for image-to-video |

### Text-to-Video Example

```python
import time
from google import genai
from google.genai import types

client = genai.Client()

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="A cinematic product showcase...",
    config=types.GenerateVideosConfig(
        aspect_ratio="16:9",
        negative_prompt="blurry, distorted",
    ),
)

while not operation.done:
    time.sleep(10)
    operation = client.operations.get(operation)

video = operation.response.generated_videos[0]
client.files.download(file=video.video)
video.video.save("output.mp4")
```

### Image-to-Video Example

```python
operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="The camera slowly orbits...",
    image=types.Image.from_uri("https://example.com/frame.png"),
    config=types.GenerateVideosConfig(
        aspect_ratio="16:9",
        person_generation="allow_adult",
    ),
)
```
