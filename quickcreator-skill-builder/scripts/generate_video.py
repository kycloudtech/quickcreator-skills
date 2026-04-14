"""
Google Veo 3.1 video generation template for QuickCreator skills.

Prerequisites:
  - GOOGLE_API_KEY environment variable must be set
  - pip install google-genai

Usage:
  python generate_video.py --prompt "A cinematic scene..." [OPTIONS]

Options:
  --prompt TEXT              Text prompt (required)
  --image PATH_OR_URL        Starting frame — local file path or HTTP(S) URL
  --aspect-ratio 16:9|9:16   Aspect ratio (default: 16:9)
  --resolution 720p|1080p|4k Resolution (default: 720p)
  --duration 4|6|8           Duration in seconds (default: 8)
  --negative-prompt TEXT     Content to exclude
  --output PATH              Output file path (default: output.mp4)
  --poll-interval SECONDS    Polling interval (default: 10)
"""

import argparse
import base64
import mimetypes
import sys
import time
from pathlib import Path

from google import genai
from google.genai import types


def load_image(image_source: str) -> types.Image:
    """Load an image from a local file path or a remote URL."""
    if image_source.startswith("http://") or image_source.startswith("https://"):
        return types.Image.from_uri(image_source)

    path = Path(image_source)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {image_source}")

    mime_type, _ = mimetypes.guess_type(str(path))
    if not mime_type:
        mime_type = "image/jpeg"

    image_bytes = path.read_bytes()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    return types.Image(image_bytes=base64.b64decode(image_b64), mime_type=mime_type)


def generate_video(
    prompt: str,
    image_source: str | None = None,
    aspect_ratio: str = "16:9",
    resolution: str = "720p",
    duration_seconds: int = 8,
    negative_prompt: str | None = None,
    output_path: str = "output.mp4",
    poll_interval: int = 10,
) -> str:
    client = genai.Client()

    config = types.GenerateVideosConfig(
        aspect_ratio=aspect_ratio,
        resolution=resolution,
        duration_seconds=duration_seconds,
    )
    if negative_prompt:
        config.negative_prompt = negative_prompt

    kwargs = {
        "model": "veo-3.1-generate-preview",
        "prompt": prompt,
        "config": config,
    }

    if image_source:
        kwargs["image"] = load_image(image_source)
        config.person_generation = "allow_adult"

    print("Starting video generation...")
    operation = client.models.generate_videos(**kwargs)

    while not operation.done:
        print(f"Generating... (polling every {poll_interval}s)")
        time.sleep(poll_interval)
        operation = client.operations.get(operation)

    video = operation.response.generated_videos[0]
    client.files.download(file=video.video)
    video.video.save(output_path)
    print(f"Video saved to: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate video using Google Veo 3.1")
    parser.add_argument("--prompt", required=True, help="Text prompt")
    parser.add_argument("--image", default=None, dest="image_source",
                        help="Starting frame — local file path or HTTP(S) URL")
    parser.add_argument("--aspect-ratio", default="16:9", choices=["16:9", "9:16"])
    parser.add_argument("--resolution", default="720p", choices=["720p", "1080p", "4k"])
    parser.add_argument("--duration", type=int, default=8, choices=[4, 6, 8])
    parser.add_argument("--negative-prompt", default=None)
    parser.add_argument("--output", default="output.mp4")
    parser.add_argument("--poll-interval", type=int, default=10)

    args = parser.parse_args()

    generate_video(
        prompt=args.prompt,
        image_source=args.image_source,
        aspect_ratio=args.aspect_ratio,
        resolution=args.resolution,
        duration_seconds=args.duration,
        negative_prompt=args.negative_prompt,
        output_path=args.output,
        poll_interval=args.poll_interval,
    )


if __name__ == "__main__":
    main()
