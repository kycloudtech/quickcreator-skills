"""
Google Veo 3.1 video generation template for QuickCreator skills.

Prerequisites:
  - GOOGLE_API_KEY environment variable must be set
  - pip install google-genai

Usage:
  python generate_video.py --prompt "A cinematic scene..." [OPTIONS]

Options:
  --prompt TEXT              Text prompt (required)
  --image-url URL            Starting frame URL for image-to-video
  --aspect-ratio 16:9|9:16   Aspect ratio (default: 16:9)
  --resolution 720p|1080p|4k Resolution (default: 720p)
  --duration 4|6|8           Duration in seconds (default: 8)
  --negative-prompt TEXT     Content to exclude
  --output PATH              Output file path (default: output.mp4)
  --poll-interval SECONDS    Polling interval (default: 10)
"""

import argparse
import sys
import time

from google import genai
from google.genai import types


def generate_video(
    prompt: str,
    image_url: str | None = None,
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

    if image_url:
        kwargs["image"] = types.Image.from_uri(image_url)
        config.person_generation = "allow_adult"

    print(f"Starting video generation...")
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
    parser.add_argument("--image-url", default=None, help="Starting frame URL")
    parser.add_argument("--aspect-ratio", default="16:9", choices=["16:9", "9:16"])
    parser.add_argument("--resolution", default="720p", choices=["720p", "1080p", "4k"])
    parser.add_argument("--duration", type=int, default=8, choices=[4, 6, 8])
    parser.add_argument("--negative-prompt", default=None)
    parser.add_argument("--output", default="output.mp4")
    parser.add_argument("--poll-interval", type=int, default=10)

    args = parser.parse_args()

    generate_video(
        prompt=args.prompt,
        image_url=args.image_url,
        aspect_ratio=args.aspect_ratio,
        resolution=args.resolution,
        duration_seconds=args.duration,
        negative_prompt=args.negative_prompt,
        output_path=args.output,
        poll_interval=args.poll_interval,
    )


if __name__ == "__main__":
    main()
