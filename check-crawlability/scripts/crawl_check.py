#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "requests",
# ]
# ///
"""Check crawlability signals for a domain: robots.txt, sitemap, HTTPS redirect, basic metadata,
and AI crawler access (GEO-critical: OAI-SearchBot, PerplexityBot, Claude-SearchBot, etc.).

Usage:
    uv run crawl_check.py https://example.com
    uv run crawl_check.py example.com
"""

import gzip
import json
import re
import sys
from html import unescape
from typing import Optional
from urllib.parse import urljoin, urlparse, quote
from xml.etree import ElementTree as ET

import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; TechnicalSEOAuditBot/1.0)"
}
TIMEOUT = 15

_MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")

# AI bots from official documentation (platform.openai.com, docs.perplexity.ai,
# support.claude.com, developers.google.com, support.apple.com, developers.facebook.com)
_AI_BOTS = {
    "OAI-SearchBot":     {"desc": "ChatGPT Search 索引", "geo_impact": "critical"},
    "GPTBot":            {"desc": "OpenAI 训练爬虫",     "geo_impact": "high"},
    "ChatGPT-User":      {"desc": "ChatGPT 用户请求",    "geo_impact": "high"},
    "PerplexityBot":     {"desc": "Perplexity Search 索引", "geo_impact": "critical"},
    "Perplexity-User":   {"desc": "Perplexity 用户请求", "geo_impact": "high"},
    "Claude-SearchBot":  {"desc": "Claude Search 索引",  "geo_impact": "critical"},
    "ClaudeBot":         {"desc": "Anthropic 训练爬虫",  "geo_impact": "medium"},
    "Claude-User":       {"desc": "Claude 用户请求",     "geo_impact": "medium"},
    "Google-Extended":   {"desc": "Gemini AI 训练（非 AIO，AIO 由 Googlebot 索引）", "geo_impact": "medium"},
    "Applebot-Extended": {"desc": "Apple Intelligence 训练", "geo_impact": "low"},
    "meta-externalagent":{"desc": "Meta AI 训练",        "geo_impact": "low"},
    "meta-webindexer":   {"desc": "Meta AI 搜索",        "geo_impact": "low"},
}


def normalize_url(raw: str) -> str:
    if not raw.startswith(("http://", "https://")):
        raw = "https://" + raw
    parsed = urlparse(raw)
    return f"{parsed.scheme}://{parsed.netloc}"


def candidate_paths(input_url: str) -> list:
    """Return list of path prefixes to probe, from deepest to root.

    Example: input '/blogs/abc/def' -> ['/blogs/abc/', '/blogs/', '/']
    Root '/' is always included and listed last (so deeper paths win on tie).
    """
    if not input_url.startswith(("http://", "https://")):
        input_url = "https://" + input_url
    parsed = urlparse(input_url)
    path = parsed.path or "/"
    # Strip trailing filename: split into segments, drop last if it looks like a file
    segments = [s for s in path.split("/") if s]
    prefixes = []
    # Build parent dirs from deepest to shallowest (excluding the leaf which is typically the page itself)
    for i in range(len(segments) - 1, 0, -1):
        prefixes.append("/" + "/".join(segments[:i]) + "/")
    if "/" not in prefixes:
        prefixes.append("/")
    return prefixes


def check_https_redirect(domain_url: str) -> dict:
    http_url = domain_url.replace("https://", "http://")
    result = {"http_url": http_url, "redirects_to_https": False, "final_url": None, "chain": []}
    try:
        resp = requests.get(http_url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        result["final_url"] = resp.url
        result["redirects_to_https"] = resp.url.startswith("https://")
        result["chain"] = [r.url for r in resp.history] + [resp.url]
        result["status_code"] = resp.status_code
    except Exception as e:
        result["error"] = str(e)
    return result


def check_robots(base_url: str, path_prefixes: list = None) -> dict:
    """Only the origin-root robots.txt governs this origin, never a subdirectory."""
    robots_url = urljoin(base_url, "/robots.txt")
    result = {"accessible": False, "found_at": None, "url": robots_url,
              "content_full": None, "rules_state": "unknown", "issues": [], "attempts": []}
    try:
        resp = requests.get(robots_url, headers=HEADERS, timeout=TIMEOUT)
        result["status_code"] = resp.status_code
        result["final_url"] = resp.url
        result["attempts"].append({"url": robots_url, "status_code": resp.status_code})
        if resp.status_code in (404, 410):
            result.update(rules_state="not_found", content_full="")
            return result
        if resp.status_code != 200:
            result["issues"].append(f"UNVERIFIED: root robots.txt returned HTTP {resp.status_code}")
            return result
        content = resp.text
        if re.search(r"<(?:!doctype|html|head|body)\b", content, re.I):
            result["issues"].append("UNVERIFIED: root robots.txt returned HTML instead of rules")
            return result
        sections = _parse_robots_sections(content)
        wildcard = sections.get("*", {})
        disallow_all = (any(v in ("/", "/*") for v in wildcard.get("disallow", []))
                        and not any(wildcard.get("allow", [])))
        result.update(accessible=True, found_at="/", content_preview=content[:500],
                      content_full=content, rules_state="parsed", disallow_all=disallow_all,
                      has_sitemap_directive=bool(re.search(r"(?im)^\s*Sitemap:", content)),
                      sitemap_urls_in_robots=re.findall(r"(?im)^\s*Sitemap:\s*(\S+)", content))
        if disallow_all:
            result["issues"].append("REVIEW: wildcard group disallows all paths; specific bot groups may override")
    except requests.RequestException as exc:
        result["error"] = str(exc)
        result["attempts"].append({"url": robots_url, "error": str(exc)})
        result["issues"].append(f"UNVERIFIED: root robots.txt request failed: {exc}")
    return result


def check_sitemap(base_url: str, sitemap_urls_hint: list = None, path_prefixes: list = None) -> dict:
    """Probe sitemap at: (1) URLs hinted by robots.txt Sitemap directive,
    (2) standard filenames under every candidate path prefix (deepest first)."""
    prefixes = path_prefixes or ["/"]
    default_files = ["sitemap.xml", "sitemap_index.xml", "sitemap-index.xml"]

    candidates = []
    # robots.txt hints have highest priority
    for hinted in (sitemap_urls_hint or []):
        if hinted not in candidates:
            candidates.append(hinted)
    # then path-prefix combinations
    for prefix in prefixes:
        for fname in default_files:
            url = urljoin(base_url, prefix + fname)
            if url not in candidates:
                candidates.append(url)

    attempts = []
    result = {"found": False, "found_at": None, "url": None, "issues": []}
    for url in candidates:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            attempts.append({"url": url, "status_code": resp.status_code})
            if resp.status_code == 200:
                try:
                    payload = resp.content
                    if payload.startswith(b"\x1f\x8b"):
                        payload = gzip.decompress(payload)
                    root = ET.fromstring(payload)
                except (ET.ParseError, OSError, EOFError):
                    continue
                root_name = root.tag.rsplit("}", 1)[-1]
                if root_name not in ("urlset", "sitemapindex"):
                    continue
                result["found"] = True
                result["url"] = resp.url
                result["found_at"] = urlparse(resp.url).path.rsplit("/", 1)[0] + "/"
                result["status_code"] = resp.status_code
                locations = [el.text.strip() for el in root.iter()
                             if el.tag.rsplit("}", 1)[-1] == "loc" and el.text]
                sitemap_index = root_name == "sitemapindex"
                result["is_index"] = sitemap_index
                result["url_count"] = len(locations)
                result["count_kind"] = "child_sitemaps" if sitemap_index else "page_urls"
                if sitemap_index:
                    result["child_sitemaps"] = locations[:10]
                result["attempts"] = attempts
                return result
        except Exception as e:
            attempts.append({"url": url, "error": str(e)})

    result["attempts"] = attempts
    result["issues"].append(
        f"No sitemap found (tried {len(attempts)} locations: "
        + ", ".join(a['url'] for a in attempts) + ")"
    )
    return result


def _parse_robots_sections(content: str) -> dict:
    """Merge groups for identical product tokens; comments and blank lines are ignored."""
    sections, current_agents = {}, []
    seen_rules = False
    for raw_line in content.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        field, _, value = line.partition(":")
        field, value = field.strip().lower(), value.strip()
        if field == "user-agent":
            if seen_rules:
                current_agents, seen_rules = [], False
            agent = value.lower()
            if agent:
                current_agents.append(agent)
                sections.setdefault(agent, {"disallow": [], "allow": []})
        elif field in ("disallow", "allow") and current_agents:
            seen_rules = True
            for agent in current_agents:
                sections[agent][field].append(value)
    return sections


def _normalize_robots_path(value: str) -> str:
    """Compare percent-encoded UTF-8, decoding only unreserved escaped ASCII."""
    value = quote(value, safe="/%*?=&:$,;@!+~'()[]-")
    def normalize(match):
        char = chr(int(match.group(1), 16))
        return char if re.fullmatch(r"[A-Za-z0-9._~-]", char) else "%" + match.group(1).upper()
    return re.sub(r"%([0-9a-fA-F]{2})", normalize, value)


def _bot_crawl_status(sections: dict, bot_name: str, path: str = "/") -> str:
    """Evaluate the tested path, longest match wins, Allow wins equal-length ties."""
    key = bot_name.lower()
    # Product tokens identify the bot; exact named groups take precedence over *.
    rules = sections.get(key, sections.get("*"))
    if rules is None:
        return "not_declared"
    matches = []
    target = _normalize_robots_path(path)
    for field in ("disallow", "allow"):
        for raw_pattern in rules.get(field, []):
            if not raw_pattern:
                continue
            pattern = _normalize_robots_path(raw_pattern)
            anchored = pattern.endswith("$")
            if anchored:
                pattern = pattern[:-1]
            regex = "^" + re.escape(pattern).replace(r"\*", ".*") + ("$" if anchored else "")
            if re.search(regex, target):
                length = len(pattern.replace("*", "").encode("utf-8"))
                matches.append((length, field == "allow"))
    if not matches or max(matches)[1]:
        return "allowed"
    return "blocked" if key in sections else "blocked_by_wildcard"


def check_ai_crawlers(robots_content: Optional[str], path: str = "/") -> dict:
    """Rule interpretation only; search, training, and user-request bots are distinct."""
    sections = _parse_robots_sections(robots_content or "")
    bots, issues = {}, []
    bot_specs = dict(_AI_BOTS)
    bot_specs.update({"Googlebot": {"desc": "Google Search", "geo_impact": "critical"},
                      "Bingbot": {"desc": "Bing Search", "geo_impact": "critical"}})
    search_bots = {"Googlebot", "Bingbot", "OAI-SearchBot", "PerplexityBot", "Claude-SearchBot", "meta-webindexer"}
    for name, meta in bot_specs.items():
        status = "unknown" if robots_content is None else _bot_crawl_status(sections, name, path)
        purpose = "search" if name in search_bots else "user_request" if "User" in name else "training_or_other"
        bots[name] = {"description": meta["desc"], "purpose": purpose,
                      "status": status, "tested_path": path}
        if purpose == "search" and status in ("blocked", "blocked_by_wildcard"):
            issues.append(f"REVIEW: robots disallows {name} for tested path {path}")
    blocked = [name for name in search_bots if bots[name]["status"] in ("blocked", "blocked_by_wildcard")]
    return {"rules_status": "unknown" if robots_content is None else "evaluated",
            "geo_status": "unknown" if robots_content is None else "blocked_for_tested_path" if blocked else "not_blocked_by_robots",
            "critical_blocked": blocked, "bots": bots, "issues": issues,
            "note": "Public robots rules only; not a real-bot access, indexing or AI visibility test."}


def check_llms_txt(base_url: str, path_prefixes: list = None) -> dict:
    """Check if /llms.txt exists at any candidate path prefix (proposed standard by
    Jeremy Howard / Answer.AI, llmstxt.org). Not yet W3C/IETF standardized.

    `url` is the final URL after redirects (e.g. bare domain -> www); relative
    links inside the file are resolved against that URL, as a browser would.
    """
    prefixes = path_prefixes or ["/"]
    attempts = []
    result = {"found": False, "found_at": None, "url": None}

    for prefix in prefixes:
        url = urljoin(base_url, prefix + "llms.txt")
        try:
            resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            attempts.append({"url": url, "status_code": resp.status_code})
            if resp.status_code == 200 and resp.text.strip():
                result["found"] = True
                result["url"] = resp.url
                if resp.url != url:
                    result["requested_url"] = url
                result["found_at"] = prefix
                result["size_bytes"] = len(resp.content)
                result["preview"] = resp.text[:300]
                result["content_type"] = resp.headers.get("Content-Type", "")
                result["has_h1"] = bool(re.search(r"(?m)^#\s+\S", resp.text))
                result["links"] = _extract_markdown_links(resp.text, resp.url)
                result["attempts"] = attempts
                return result
        except Exception as e:
            attempts.append({"url": url, "error": str(e)})

    result["url"] = urljoin(base_url, "/llms.txt")
    result["attempts"] = attempts
    last_status = next((a.get("status_code") for a in reversed(attempts) if "status_code" in a), None)
    if last_status:
        result["status_code"] = last_status
    result["note"] = (
        "llms.txt 未找到（已尝试 "
        + str(len(attempts))
        + " 个候选路径）。非强制要求，不据此判断 AI 平台可见度。"
        "规范见 llmstxt.org（社区提案，非正式标准）。"
    )
    return result


def _extract_markdown_links(markdown: str, llms_url: str) -> list:
    """Return unique Markdown links from an llms.txt file, resolved against the
    llms.txt URL itself (so `guide.md` in /blog/llms.txt -> /blog/guide.md)."""
    links = []
    seen = set()
    for match in _MARKDOWN_LINK_RE.finditer(markdown):
        raw_url = match.group(1).strip("<>")
        absolute_url = urljoin(llms_url, raw_url)
        parsed = urlparse(absolute_url)
        if parsed.scheme not in ("http", "https") or absolute_url in seen:
            continue
        seen.add(absolute_url)
        links.append(absolute_url)
    return links


def _first_markdown_h1(markdown: str) -> Optional[str]:
    match = re.search(r"(?m)^#\s+(.+?)\s*$", markdown)
    return match.group(1).strip() if match else None


def _first_html_h1(html: str) -> Optional[str]:
    match = re.search(r"<h1\b[^>]*>(.*?)</h1>", html, re.IGNORECASE | re.DOTALL)
    if not match:
        return None
    text = re.sub(r"<[^>]+>", "", match.group(1))
    return re.sub(r"\s+", " ", unescape(text)).strip()


def _url_identity(url: str, base_url: str) -> tuple:
    """Resolve a URL into a comparison-safe scheme, host, port, path and query tuple.

    Trailing-slash variants (`/guide` vs `/guide/`) are treated as the same page;
    the root path stays `/`. Fragments are ignored.
    """
    parsed = urlparse(urljoin(base_url, unescape(url.strip())))
    default_port = 443 if parsed.scheme.lower() == "https" else 80
    path = (parsed.path or "/").rstrip("/") or "/"
    return (
        parsed.scheme.lower(),
        (parsed.hostname or "").lower(),
        parsed.port or default_port,
        path,
        parsed.query,
    )


def _same_origin(first_url: str, second_url: str) -> bool:
    return _url_identity(first_url, first_url)[:3] == _url_identity(second_url, second_url)[:3]


def _media_type(value: str) -> str:
    """`text/markdown; charset=utf-8` -> `text/markdown`."""
    return value.split(";", 1)[0].strip().strip('"').lower()


def _has_html_link_relation(
    headers: str,
    html: str,
    source_url: str,
    relation: str,
    target_urls,
    expected_type: Optional[str] = None,
) -> bool:
    """Check an HTML <link> element or RFC 8288 Link header for one relation.

    `target_urls` may be one URL or several equivalent URLs (e.g. requested and
    post-redirect forms). This is intentionally small and conservative: it checks
    an explicit target and relation rather than becoming a general HTML parser.
    """
    if isinstance(target_urls, str):
        target_urls = [target_urls]
    target_identities = {_url_identity(t, source_url) for t in target_urls if t}

    def _matches(href: str, rel: str, type_value: Optional[str]) -> bool:
        relations = {part.lower() for part in rel.split()}
        type_matches = not expected_type or (
            type_value is not None and _media_type(type_value) == _media_type(expected_type)
        )
        return (
            relation.lower() in relations
            and _url_identity(href, source_url) in target_identities
            and type_matches
        )

    for value in headers.split(","):
        href_match = re.search(r"<([^>]+)>", value)
        rel_match = re.search(r'\brel\s*=\s*"?([^";]+)', value, re.IGNORECASE)
        type_match = re.search(r'\btype\s*=\s*(?:"([^"]+)"|([^\s;,]+))', value, re.IGNORECASE)
        if not href_match or not rel_match:
            continue
        type_value = (type_match.group(1) or type_match.group(2)) if type_match else None
        if _matches(href_match.group(1), rel_match.group(1), type_value):
            return True

    for tag in re.findall(r"<link\b[^>]*>", html, re.IGNORECASE):
        href_match = re.search(r'\bhref\s*=\s*["\']([^"\']+)["\']', tag, re.IGNORECASE)
        rel_match = re.search(r'\brel\s*=\s*["\']([^"\']+)["\']', tag, re.IGNORECASE)
        type_match = re.search(r'\btype\s*=\s*["\']([^"\']+)["\']', tag, re.IGNORECASE)
        if not href_match or not rel_match:
            continue
        if _matches(href_match.group(1), rel_match.group(1), type_match.group(1) if type_match else None):
            return True
    return False


def _html_pair_candidate(markdown_url: str) -> Optional[str]:
    """Map llmstxt.org Markdown companion forms back to the HTML page URL.

    /x/index.html.md and /x/index.md -> /x/ ; /x.html.md -> /x.html ; /x.md -> /x.
    Trailing-slash variants are compared as equivalent elsewhere.
    """
    parsed = urlparse(markdown_url)
    if parsed.path.endswith("/index.html.md"):
        path = parsed.path[: -len("index.html.md")]
    elif parsed.path.endswith("/index.md"):
        path = parsed.path[: -len("index.md")]
    elif parsed.path.endswith(".md"):
        path = parsed.path[: -len(".md")]
    else:
        return None
    return parsed._replace(path=path or "/", fragment="").geturl()


def _robots_value_is_noindex(value: str) -> bool:
    tokens = {t.strip().lower() for t in re.split(r"[,\s]+", value) if t.strip()}
    # X-Robots-Tag may be prefixed with a user agent ("googlebot: noindex").
    tokens |= {t.split(":", 1)[1] for t in tokens if ":" in t}
    return bool(tokens & {"noindex", "none"})


def _has_html_noindex(html: str) -> bool:
    for tag in re.findall(r"<meta\b[^>]*>", html, re.IGNORECASE):
        name_match = re.search(r'\bname\s*=\s*["\']([^"\']+)["\']', tag, re.IGNORECASE)
        content_match = re.search(r'\bcontent\s*=\s*["\']([^"\']+)["\']', tag, re.IGNORECASE)
        if name_match and content_match and name_match.group(1).lower() in ("robots", "googlebot"):
            if _robots_value_is_noindex(content_match.group(1)):
                return True
    return False


_SITEMAP_CACHE: dict = {}


def _sitemap_body(response) -> str:
    content = response.content
    if content[:2] == b"\x1f\x8b":  # raw .xml.gz (not transfer-encoded)
        content = gzip.decompress(content)
    return content.decode(response.encoding or "utf-8", errors="replace")


def _load_sitemap_urls(sitemap_url: str) -> dict:
    """Fetch a sitemap (and child sitemaps, max 25 files) once; cache the URL keys."""
    if sitemap_url in _SITEMAP_CACHE:
        return _SITEMAP_CACHE[sitemap_url]
    queue = [sitemap_url]
    visited = []
    keys = set()
    errors = []
    while queue and len(visited) < 25:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.append(current)
        try:
            response = requests.get(current, headers=HEADERS, timeout=TIMEOUT)
            if response.status_code != 200:
                errors.append(f"{current} returned HTTP {response.status_code}")
                continue
            body = _sitemap_body(response)
            locs = [unescape(u) for u in re.findall(r"<loc>\s*(.*?)\s*</loc>", body, re.IGNORECASE | re.DOTALL)]
            if re.search(r"<sitemapindex\b", body, re.IGNORECASE):
                queue.extend(u for u in locs if u not in visited)
            else:
                keys.update(_url_identity(u, current) for u in locs)
        except Exception as e:
            errors.append(f"{current} failed: {e}")
    data = {"keys": keys, "visited": visited, "errors": errors, "truncated": bool(queue)}
    _SITEMAP_CACHE[sitemap_url] = data
    return data


def _sitemap_membership(sitemap_url: Optional[str], target_urls) -> dict:
    """Look for a page (any of its equivalent URLs) in the discovered sitemap tree."""
    if not sitemap_url:
        return {"status": "not_checked", "reason": "No sitemap was discovered."}
    if isinstance(target_urls, str):
        target_urls = [target_urls]
    data = _load_sitemap_urls(sitemap_url)
    if any(_url_identity(t, t) in data["keys"] for t in target_urls if t):
        return {"status": "included", "checked_sitemaps": data["visited"]}
    if data["truncated"]:
        return {
            "status": "not_checked",
            "reason": "Sitemap traversal reached the 25-file safety limit.",
            "checked_sitemaps": data["visited"],
        }
    return {"status": "missing", "checked_sitemaps": data["visited"], "errors": data["errors"]}


_MAX_PAIRS = 10


def check_llms_markdown_pairs(llms_result: dict, base_url: str, sitemap_result: dict) -> dict:
    """Inspect same-origin Markdown links in llms.txt and their HTML companions.

    Origin is taken from the llms.txt URL *after redirects*. A Markdown link is
    checked whether or not llms.txt also lists the HTML page: if the HTML is not
    listed, its URL is derived by llmstxt.org convention (/x/index.md -> /x/,
    /x.md -> /x) and marked `html_declared_in_llms_txt: false`.

    Generic docs can be pairs too, so the output never assumes every pair is an
    "LLM guide". External links are not audited here.
    """
    result = {"declared_pairs": [], "issues": []}
    if not llms_result.get("found"):
        result["note"] = "llms.txt 未找到，因此未检查 HTML/Markdown 配对。"
        return result

    llms_url = llms_result.get("url") or urljoin(base_url, "/llms.txt")
    llms_targets = [llms_url, llms_result.get("requested_url")]
    links = llms_result.get("links", [])
    local_links = [url for url in links if _same_origin(url, llms_url)]
    local_by_key = {_url_identity(url, url): url for url in local_links}
    markdown_links = [url for url in local_links if urlparse(url).path.endswith(".md")]

    if len(markdown_links) > _MAX_PAIRS:
        result["truncated_note"] = (
            f"llms.txt 列了 {len(markdown_links)} 个同源 Markdown 链接，只检查前 {_MAX_PAIRS} 个。"
        )
        markdown_links = markdown_links[:_MAX_PAIRS]

    for markdown_url in markdown_links:
        derived_html = _html_pair_candidate(markdown_url)
        if not derived_html:
            continue
        declared_html = local_by_key.get(_url_identity(derived_html, derived_html))
        html_url = declared_html or derived_html

        pair = {
            "html_url": html_url,
            "markdown_url": markdown_url,
            "html_declared_in_llms_txt": bool(declared_html),
            "html_status_code": None,
            "markdown_status_code": None,
            "relations": {},
            "content_equivalence": "not_checked: this checker verifies delivery signals, not factual equivalence.",
        }
        if not declared_html:
            pair["html_url_source"] = "derived_by_convention"
        markdown_targets = [markdown_url]
        try:
            markdown_response = requests.get(markdown_url, headers=HEADERS, timeout=TIMEOUT)
            pair["markdown_status_code"] = markdown_response.status_code
            if markdown_response.url != markdown_url:
                pair["markdown_final_url"] = markdown_response.url
                markdown_targets.append(markdown_response.url)
            pair["markdown_content_type"] = markdown_response.headers.get("Content-Type", "")
            pair["markdown_h1"] = _first_markdown_h1(markdown_response.text)
            if markdown_response.status_code != 200:
                result["issues"].append(f"HIGH: llms.txt 声明的 Markdown 返回 HTTP {markdown_response.status_code}: {markdown_url}")
            else:
                if _media_type(pair["markdown_content_type"]) != "text/markdown":
                    result["issues"].append(f"WARN: llms.txt 声明的 Markdown 未以 text/markdown 返回: {markdown_url}")
                if not pair["markdown_h1"]:
                    result["issues"].append(f"WARN: llms.txt 声明的 Markdown 缺少 H1: {markdown_url}")
        except Exception as e:
            pair["markdown_error"] = str(e)
            result["issues"].append(f"HIGH: 无法请求 llms.txt 声明的 Markdown: {markdown_url} ({e})")

        label = "llms.txt 声明的 HTML" if declared_html else "按约定推导的 HTML（llms.txt 未列出）"
        try:
            html_response = requests.get(html_url, headers=HEADERS, timeout=TIMEOUT)
            final_html = html_response.url
            html_targets = [html_url, final_html]
            pair["html_status_code"] = html_response.status_code
            if final_html != html_url:
                pair["html_final_url"] = final_html
            pair["html_content_type"] = html_response.headers.get("Content-Type", "")
            pair["html_h1"] = _first_html_h1(html_response.text)
            link_header = html_response.headers.get("Link", "")
            pair["relations"] = {
                "alternate_markdown": _has_html_link_relation(
                    link_header, html_response.text, final_html, "alternate", markdown_targets, "text/markdown"
                ),
                "describedby_llms_txt": _has_html_link_relation(
                    link_header, html_response.text, final_html, "describedby", llms_targets
                ),
            }
            pair["self_canonical"] = _has_html_link_relation("", html_response.text, final_html, "canonical", final_html)
            pair["x_robots_tag"] = html_response.headers.get("X-Robots-Tag", "")
            pair["has_noindex"] = _has_html_noindex(html_response.text) or _robots_value_is_noindex(pair["x_robots_tag"])
            if html_response.status_code == 200:
                pair["sitemap"] = _sitemap_membership(sitemap_result.get("url"), html_targets)
            if not declared_html:
                # 只列了 Markdown：站点没有声明「这是一对」，普通文档站的 llms.txt 也长这样。
                # 推导出的 HTML 各项结果照记在 pair 里，但不报成问题，免得对非配对站刷一堆 WARN。
                pass
            elif html_response.status_code != 200:
                result["issues"].append(f"HIGH: {label} 返回 HTTP {html_response.status_code}: {html_url}")
            else:
                if not pair["html_h1"]:
                    result["issues"].append(f"WARN: {label} 缺少 H1: {html_url}")
                if pair["markdown_h1"] and pair["html_h1"] and pair["markdown_h1"] != pair["html_h1"]:
                    result["issues"].append(f"WARN: HTML 与 Markdown 的 H1 不一致: {html_url}")
                if not pair["self_canonical"]:
                    result["issues"].append(f"WARN: {label} 缺少 self-canonical: {final_html}")
                if pair["has_noindex"]:
                    result["issues"].append(f"HIGH: {label} 含 noindex: {final_html}")
                if pair["sitemap"].get("status") == "missing":
                    result["issues"].append(f"WARN: {label} 不在已发现 sitemap: {final_html}")
                if not pair["relations"]["alternate_markdown"]:
                    result["issues"].append(f"WARN: HTML 缺少指向 Markdown 的 alternate relation: {final_html}")
                if not pair["relations"]["describedby_llms_txt"]:
                    result["issues"].append(f"WARN: HTML 缺少指向 llms.txt 的 describedby relation: {final_html}")
        except Exception as e:
            pair["html_error"] = str(e)
            if declared_html:
                result["issues"].append(f"HIGH: 无法请求 {label}: {html_url} ({e})")

        result["declared_pairs"].append(pair)

    if not result["declared_pairs"]:
        result["note"] = (
            f"llms.txt（{llms_url}）中没有同源 Markdown 链接，未检查配对；这不是失败。"
            f"同源判断以 llms.txt 重定向后的地址为准；llms.txt 共 {len(links)} 个链接，其中同源 {len(local_links)} 个。"
        )
    return result


def check_page_headers(url: str) -> dict:
    result = {"url": url, "status_code": None, "issues": []}
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        result["status_code"] = resp.status_code
        result["final_url"] = resp.url
        result["content_type"] = resp.headers.get("Content-Type", "")
        result["x_robots_tag"] = resp.headers.get("X-Robots-Tag", "")
        result["server"] = resp.headers.get("Server", "")
        result["powered_by"] = resp.headers.get("X-Powered-By", "")
        result["cache_control"] = resp.headers.get("Cache-Control", "")

        if result["x_robots_tag"]:
            tag = result["x_robots_tag"].lower()
            if "noindex" in tag:
                result["issues"].append(f"CRITICAL: X-Robots-Tag contains noindex: {result['x_robots_tag']}")
    except Exception as e:
        result["error"] = str(e)
    return result


def main():
    if len(sys.argv) < 2:
        print(
            json.dumps({"error": "Usage: crawl_check.py <url>"}),
            file=sys.stderr,
        )
        sys.exit(1)

    raw_url = sys.argv[1]
    base_url = normalize_url(raw_url)
    path_prefixes = candidate_paths(raw_url)

    https_result = check_https_redirect(base_url)
    robots_result = check_robots(base_url, path_prefixes)
    sitemap_hints = robots_result.get("sitemap_urls_in_robots", [])
    sitemap_result = check_sitemap(base_url, sitemap_hints, path_prefixes)
    page_url = raw_url if raw_url.startswith(("http://", "https://")) else "https://" + raw_url
    headers_result = check_page_headers(page_url)

    robots_content = robots_result.get("content_full")
    ai_crawlers_result = check_ai_crawlers(robots_content, urlparse(page_url).path + ("?" + urlparse(page_url).query if urlparse(page_url).query else ""))
    llms_txt_result = check_llms_txt(base_url, path_prefixes)
    llms_markdown_pairs_result = check_llms_markdown_pairs(llms_txt_result, base_url, sitemap_result)

    output = {
        "domain": urlparse(base_url).netloc,
        "input_url": page_url,
        "probed_path_prefixes": path_prefixes,
        "https_redirect": https_result,
        "robots": robots_result,
        "sitemap": sitemap_result,
        "page_headers": headers_result,
        "ai_crawlers": ai_crawlers_result,
        "llms_txt": llms_txt_result,
        "llms_markdown_pairs": llms_markdown_pairs_result,
    }

    all_issues = (
        robots_result.get("issues", [])
        + sitemap_result.get("issues", [])
        + headers_result.get("issues", [])
        + ai_crawlers_result.get("issues", [])
        + llms_markdown_pairs_result.get("issues", [])
    )
    output["issues_summary"] = all_issues

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
