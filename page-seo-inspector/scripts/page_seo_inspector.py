#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "requests",
#   "beautifulsoup4",
# ]
# ///
"""
Page SEO Inspector: Comprehensive single-page technical SEO audit.

Checks 50+ signals across 9 categories, displayed per-category so every
check and its result is visible — not just the problems.

Usage:
    uv run <SKILL_DIR>/scripts/page_seo_inspector.py <url>
    uv run <SKILL_DIR>/scripts/page_seo_inspector.py <url> --json
"""

import json
import re
import sys
import time
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
TIMEOUT = 20
CRITICAL_PENALTY = 15
WARNING_PENALTY = 3

STATUS_ICON = {
    "critical": "🔴",
    "warning":  "🟡",
    "pass":     "✅",
    "info":     "ℹ️ ",
}


# ─── Check item ──────────────────────────────────────────────────────────────

class Check:
    """A single audited signal."""
    def __init__(self, name: str, status: str, detail: str = ""):
        self.name = name
        self.status = status   # critical | warning | pass | info
        self.detail = detail

    def to_dict(self):
        return {"name": self.name, "status": self.status, "detail": self.detail}

    def __str__(self):
        icon = STATUS_ICON.get(self.status, "  ")
        line = f"{icon} {self.name}"
        if self.detail:
            line += f": {self.detail}"
        return line


def C(name, detail=""):  return Check(name, "critical", detail)
def W(name, detail=""):  return Check(name, "warning",  detail)
def P(name, detail=""):  return Check(name, "pass",     detail)
def I(name, detail=""):  return Check(name, "info",     detail)


# ─── Fetch ───────────────────────────────────────────────────────────────────

def fetch_page(url: str) -> dict:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    t0 = time.time()
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        ttfb = round(time.time() - t0, 3)
        soup = BeautifulSoup(resp.text, "html.parser")
        return {
            "url": url,
            "final_url": resp.url,
            "status_code": resp.status_code,
            "ttfb_s": ttfb,
            "content_length_bytes": len(resp.content),
            "headers": requests.structures.CaseInsensitiveDict(resp.headers),
            "soup": soup,
            "redirected": resp.url.rstrip("/") != url.rstrip("/"),
            "error": None,
        }
    except Exception as e:
        return {"url": url, "error": str(e)}


# ─── 1. HTTP Signals ─────────────────────────────────────────────────────────

def check_http(data: dict) -> tuple[dict, list[Check]]:
    r, checks = {}, []

    sc = data["status_code"]
    r["status_code"] = sc
    r["script_request_time_s"] = data["ttfb_s"]
    r["content_length_kb"] = round(data["content_length_bytes"] / 1024, 1)
    r["redirected"] = data["redirected"]
    r["final_url"] = data["final_url"]

    if sc == 200:
        checks.append(P("HTTP status", f"{sc} OK"))
    elif 300 <= sc < 400:
        checks.append(W("HTTP status", f"{sc} redirect → {data['final_url']}"))
    else:
        checks.append(C("HTTP status", f"{sc} from this client; verify crawler access separately"))

    # Script-side request time (DNS + TCP + TLS + TTFB + download from this
    # machine's network location). NOT a substitute for browser TTFB —
    # for real server-response-time use PSI's audit. Reported as info only.
    rt = data["ttfb_s"]
    checks.append(I("Script-side request time",
                    f"{rt}s (DNS+TCP+TLS+TTFB from this host; "
                    f"use PSI server-response-time for real TTFB)"))

    ct = data["headers"].get("Content-Type", "")
    r["content_type"] = ct
    if "text/html" in ct:
        checks.append(P("Content-Type", ct.split(";")[0].strip()))
    else:
        checks.append(W("Content-Type", f"unexpected: '{ct}'"))

    enc = data["headers"].get("Content-Encoding", "")
    r["content_encoding"] = enc or None
    if enc in ("gzip", "br", "zstd"):
        checks.append(P("Compression", f"{enc} enabled"))
    else:
        checks.append(W("Compression", "not detected (gzip/brotli) — check server config"))

    size_kb = r["content_length_kb"]
    if size_kb <= 500:
        checks.append(P("Page HTML size", f"{size_kb}KB"))
    else:
        checks.append(W("Page HTML size", f"{size_kb}KB — consider reducing DOM size"))

    redirected = data["redirected"]
    if redirected:
        checks.append(I("Redirect detected", f"→ {data['final_url']}"))
    else:
        checks.append(P("No redirect", "URL resolves directly"))

    return r, checks


# ─── 2. Indexability ─────────────────────────────────────────────────────────

def check_indexability(data: dict, soup: BeautifulSoup) -> tuple[dict, list[Check]]:
    r, checks = {}, []
    headers = data["headers"]
    final_url = data["final_url"]

    # X-Robots-Tag
    x_robots = headers.get("X-Robots-Tag", "")
    r["x_robots_tag"] = x_robots or None
    if x_robots and re.search(r"(?:^|[\s,:])(?:noindex|none)(?:$|[\s,])", x_robots, re.I):
        checks.append(C("X-Robots-Tag (header)", f"noindex detected: '{x_robots}'"))
    elif x_robots and "nofollow" in x_robots.lower():
        checks.append(W("X-Robots-Tag (header)", f"nofollow: '{x_robots}'"))
    elif x_robots:
        checks.append(P("X-Robots-Tag (header)", f"present, no noindex: '{x_robots}'"))
    else:
        checks.append(P("X-Robots-Tag (header)", "no header restriction observed; indexability not proven"))

    # Meta robots
    meta_robots = soup.find("meta", attrs={"name": re.compile(r"^robots$", re.I)})
    r["meta_robots"] = meta_robots.get("content", "") if meta_robots else None
    if meta_robots:
        content = meta_robots.get("content", "")
        if re.search(r"(?:^|[\s,])(?:noindex|none)(?:$|[\s,])", content, re.I):
            checks.append(C("Meta robots tag", f"noindex: '{content}'"))
        elif "nofollow" in content.lower():
            checks.append(W("Meta robots tag", f"nofollow: '{content}'"))
        else:
            checks.append(P("Meta robots tag", f"'{content}'"))
    else:
        checks.append(P("Meta robots tag", "no meta restriction observed in served HTML"))

    # Canonical
    canonical = soup.find("link", rel=lambda v: v == "canonical"
                          or (isinstance(v, list) and "canonical" in v))
    r["canonical"] = canonical.get("href") if canonical else None
    if not canonical:
        checks.append(W("Canonical tag", "not declared in HTML; check HTTP Link header and duplicate URL handling"))
    else:
        href = urljoin(final_url, canonical.get("href") or "").split("#", 1)[0]
        final = final_url.split("#", 1)[0]
        if href == final:
            checks.append(P("Canonical tag", f"self-references correctly"))
        elif href:
            checks.append(I("Canonical tag", f"points elsewhere: {href}; verify intended consolidation"))

    # Viewport
    viewport = soup.find("meta", attrs={"name": re.compile(r"^viewport$", re.I)})
    r["viewport"] = viewport.get("content", "") if viewport else None
    if viewport:
        checks.append(P("Viewport meta", viewport.get("content", "")))
    else:
        checks.append(W("Viewport meta", "missing — mobile usability risk"))

    # Charset
    charset = soup.find("meta", charset=True) or soup.find(
        "meta", attrs={"http-equiv": re.compile(r"content-type", re.I)})
    r["charset_declared"] = bool(charset)
    if charset:
        checks.append(P("Charset declaration", "declared in HTML"))
    else:
        checks.append(W("Charset declaration", "not declared in <head>"))

    return r, checks


# ─── 3. Meta Tags ────────────────────────────────────────────────────────────

def check_meta(soup: BeautifulSoup) -> tuple[dict, list[Check]]:
    r, checks = {}, []

    # Title
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else None
    r["title"] = title
    r["title_length"] = len(title) if title else 0
    if not title:
        checks.append(C("Title tag", "missing"))
    elif len(title) < 30:
        checks.append(I("Title tag", f"{len(title)} chars; review clarity for this language: '{title}'"))
    elif len(title) > 60:
        checks.append(I("Title tag", f"{len(title)} chars; preview display width, no fixed character limit: '{title[:50]}...'"))
    else:
        checks.append(P("Title tag", f"{len(title)} chars: '{title}'"))

    # Meta description
    meta_desc = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
    desc = meta_desc.get("content", "").strip() if meta_desc else None
    r["meta_description"] = desc
    r["meta_description_length"] = len(desc) if desc else 0
    if not desc:
        checks.append(W("Meta description", "missing"))
    elif len(desc) < 70:
        checks.append(I("Meta description", f"{len(desc)} chars; review usefulness, no fixed minimum"))
    elif len(desc) > 160:
        checks.append(I("Meta description", f"{len(desc)} chars; snippet length varies by query and device"))
    else:
        checks.append(P("Meta description", f"{len(desc)} chars"))

    # HTML lang
    html_tag = soup.find("html")
    lang = html_tag.get("lang", "").strip() if html_tag else ""
    r["html_lang"] = lang or None
    if lang:
        checks.append(P("HTML lang attribute", f"'{lang}'"))
    else:
        checks.append(W("HTML lang attribute", "missing — affects accessibility and i18n SEO"))

    # Hreflang
    hreflang_tags = soup.find_all("link", hreflang=True)
    r["hreflang_count"] = len(hreflang_tags)
    r["hreflang_langs"] = [t.get("hreflang") for t in hreflang_tags]
    if hreflang_tags:
        has_xdefault = any(t.get("hreflang") == "x-default" for t in hreflang_tags)
        langs_str = ", ".join(r["hreflang_langs"][:6])
        if has_xdefault:
            checks.append(P("Hreflang tags", f"{len(hreflang_tags)} tags including x-default ({langs_str})"))
        else:
            checks.append(I("Hreflang tags", f"{len(hreflang_tags)} tags; optional x-default not set ({langs_str})"))
    else:
        checks.append(I("Hreflang tags", "not set (single-language site or not implemented)"))

    # Keywords meta (deprecated but informational)
    kw_tag = soup.find("meta", attrs={"name": re.compile(r"^keywords$", re.I)})
    r["meta_keywords"] = kw_tag.get("content", "") if kw_tag else None
    if kw_tag:
        checks.append(I("Meta keywords", "present (ignored by Google, not harmful)"))
    else:
        checks.append(I("Meta keywords", "not set (expected — deprecated tag)"))

    return r, checks


# ─── 4. Heading Structure ────────────────────────────────────────────────────

def check_headings(soup: BeautifulSoup) -> tuple[dict, list[Check]]:
    r, checks = {}, []

    for lvl in range(1, 7):
        tags = soup.find_all(f"h{lvl}")
        r[f"h{lvl}_count"] = len(tags)
        r[f"h{lvl}_texts"] = [t.get_text(strip=True)[:100] for t in tags[:5]]

    h1_count = r["h1_count"]
    if h1_count == 0:
        checks.append(W("H1 tag", "not found in served HTML; verify visible main heading"))
    elif h1_count == 1:
        checks.append(P("H1 tag", f"exactly 1: '{r['h1_texts'][0]}'"))
    else:
        checks.append(I("H1 tag", f"{h1_count} found; review structure and visible main heading"))

    # Per-level presence
    for lvl in range(2, 7):
        count = r[f"h{lvl}_count"]
        if count > 0:
            checks.append(I(f"H{lvl} tags", f"{count} found"))

    # Hierarchy skip detection
    present = [lvl for lvl in range(1, 7) if r[f"h{lvl}_count"] > 0]
    skips = []
    for i in range(1, len(present)):
        if present[i] - present[i - 1] > 1:
            skips.append(f"H{present[i-1]} → H{present[i]}")
    if skips:
        checks.append(W("Heading hierarchy", f"level skip(s) detected: {', '.join(skips)}"))
    elif h1_count > 0:
        checks.append(P("Heading hierarchy", "sequential, no level skips"))

    return r, checks


# ─── 5. Social / OG Tags ─────────────────────────────────────────────────────

def check_social(soup: BeautifulSoup) -> tuple[dict, list[Check]]:
    r, checks = {}, []

    def og(prop):
        tag = soup.find("meta", attrs={"property": re.compile(f"^og:{prop}$", re.I)})
        return tag.get("content", "").strip() if tag else None

    def tw(name):
        tag = soup.find("meta", attrs={"name": re.compile(f"^twitter:{name}$", re.I)})
        return tag.get("content", "").strip() if tag else None

    og_data = {k: og(k) for k in ("title", "description", "image", "url", "type")}
    r["og"] = og_data

    for key in ("title", "description", "image", "url", "type"):
        val = og_data[key]
        if val:
            snippet = val[:60] + "..." if len(val) > 60 else val
            checks.append(P(f"og:{key}", snippet))
        elif key in ("title", "description", "image"):
            checks.append(W(f"og:{key}", "missing (required for social sharing previews)"))
        else:
            checks.append(I(f"og:{key}", "not set"))

    tw_data = {k: tw(k) for k in ("card", "title", "description", "image")}
    r["twitter"] = tw_data

    for key in ("card", "title", "description", "image"):
        val = tw_data[key]
        if val:
            checks.append(P(f"twitter:{key}", val[:60]))
        elif key == "card":
            checks.append(W("twitter:card", "missing — Twitter/X preview won't render"))
        else:
            checks.append(I(f"twitter:{key}", "not set (falls back to og: tags)"))

    return r, checks


# ─── 6. Structured Data ──────────────────────────────────────────────────────

def check_schema(soup: BeautifulSoup) -> tuple[dict, list[Check]]:
    r, checks = {}, []

    scripts = soup.find_all("script", type="application/ld+json")
    schemas, parse_errors, shape_errors = [], 0, 0

    def collect(value):
        nonlocal shape_errors
        if isinstance(value, list):
            for item in value:
                collect(item)
        elif isinstance(value, dict):
            if "@type" in value:
                schemas.append(value)
            if "@graph" in value:
                collect(value["@graph"])
        else:
            shape_errors += 1

    for script in scripts:
        try:
            collect(json.loads(script.string or ""))
        except (json.JSONDecodeError, TypeError):
            parse_errors += 1

    schema_types = []
    for item in schemas:
        types = item.get("@type", [])
        for value in types if isinstance(types, list) else [types]:
            if isinstance(value, str) and value not in schema_types:
                schema_types.append(value)
    r.update(schema_count=len(schemas), schema_types=schema_types,
             schema_parse_errors=parse_errors, schema_shape_errors=shape_errors)
    checks.append(I("JSON-LD blocks found", str(len(scripts))))
    if parse_errors:
        checks.append(W("JSON-LD parse errors", f"{parse_errors} invalid JSON block(s)"))
    elif scripts:
        checks.append(P("JSON-LD syntax", "valid JSON; not a schema or rich-result validation"))
    else:
        checks.append(I("JSON-LD syntax", "not applicable"))
    if shape_errors:
        checks.append(W("JSON-LD structure", f"{shape_errors} non-object/list value(s); verify markup"))
    if not schemas:
        checks.append(I("Structured data (JSON-LD)", "no typed nodes found in served HTML; check rendered HTML and other markup"))
    else:
        checks.append(I("Structured data types", ", ".join(schema_types) or "no string types"))
    checks.append(I("Structured data validation", "verify applicable type, visible facts, current required fields and feature eligibility separately"))

    # Microdata
    microdata = soup.find_all(attrs={"itemtype": True})
    r["microdata_count"] = len(microdata)
    if microdata and not schemas:
        checks.append(I("Microdata", f"{len(microdata)} items; not validated by this JSON-LD parser"))
    elif microdata:
        checks.append(I("Microdata", f"{len(microdata)} items also present alongside JSON-LD"))
    else:
        checks.append(I("Microdata", "not used"))

    return r, checks


# ─── 7. Content Quality ───────────────────────────────────────────────────────

def check_content(data: dict, soup: BeautifulSoup) -> tuple[dict, list[Check]]:
    r, checks = {}, []
    domain = urlparse(data["final_url"]).netloc

    # Word count
    body = soup.find("body")
    if body:
        body_copy = BeautifulSoup(str(body), "html.parser")
        for tag in body_copy.find_all(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()
        text = body_copy.get_text(separator=" ", strip=True)
        word_count = len(text.split())
    else:
        word_count = 0
    r["word_count"] = word_count
    checks.append(I("Word count", f"{word_count} whitespace-delimited tokens; not a quality threshold or reliable segmentation for all languages"))

    # Images — exclude <noscript> fallbacks: html.parser parses their content
    # as real markup, so lazyload fallback <img> would be double-counted (and
    # they typically carry no alt/dimensions, inflating every image check).
    images = [im for im in soup.find_all("img") if im.find_parent("noscript") is None]
    total_img = len(images)
    missing_alt = sum(1 for img in images if img.get("alt") is None)
    # Whitespace-only alt is equivalent to empty for assistive tech; attribute
    # values are case-insensitive per HTML spec (loading="Lazy" counts).
    empty_alt   = sum(1 for img in images
                      if img.get("alt") is not None and not img.get("alt").strip())
    def _is_lazy(img) -> bool:
        return (img.get("loading") or "").strip().lower() == "lazy"
    lazy = sum(1 for img in images if _is_lazy(img))
    first_img_lazy = bool(images) and _is_lazy(images[0])

    def _numeric(v) -> bool:
        # width="100%" / width="auto" are invalid per spec and ignored by
        # browsers — they reserve nothing, so they must not count as sized.
        return bool(v) and str(v).strip().isdigit()

    def _css_reserves_box(img) -> bool:
        # Framework fill images (Next <Image fill>, Nuxt/Astro equivalents)
        # and inline aspect-ratio styles reserve space without width/height
        # attributes — no layout shift. Counting them as unsized produced a
        # "111 images, only 2 declared" false finding on a real project
        # where the true unsized count was zero (issue #117).
        if img.get("data-nimg") == "fill":
            return True
        style = (img.get("style") or "").replace(" ", "").lower()
        if "aspect-ratio:" in style:
            return True
        return ("position:absolute" in style
                and ("inset:0" in style
                     or ("width:100%" in style and "height:100%" in style)))

    sized = css_reserved = 0
    for img in images:
        if _numeric(img.get("width")) and _numeric(img.get("height")):
            sized += 1
        elif _css_reserves_box(img):
            css_reserved += 1
    unsized = total_img - sized - css_reserved

    r.update({"images_total": total_img, "images_missing_alt": missing_alt,
               "images_empty_alt": empty_alt, "images_missing_dimensions": unsized,
               "images_css_reserved": css_reserved, "images_lazy_loaded": lazy,
               "images_first_lazy": first_img_lazy})

    checks.append(I("Images total", str(total_img)))

    if total_img > 0:
        if missing_alt == 0:
            checks.append(P("Images — alt attribute", f"all {total_img} have alt attributes"))
        else:
            checks.append(W("Images — alt attribute", f"{missing_alt}/{total_img} missing alt (SEO + accessibility)"))

        if empty_alt > 0:
            # alt="" is the CORRECT markup for decorative images (WAI) — the
            # script can't tell decorative from content, so this is a verify
            # prompt, never a defect count (issue #125).
            checks.append(I("Images — empty alt", f"{empty_alt}/{total_img} have empty alt (correct for decorative images — verify none are content images)"))
        else:
            checks.append(P("Images — empty alt", "none (good — empty alt reserved for decorative images)"))

        if unsized > 0:
            checks.append(W("Images — width/height", f"{unsized}/{total_img} unsized — no numeric width/height, no fill/aspect-ratio CSS; verify in DevTools whether external CSS reserves the box, else add dimensions (CLS risk)"))
        else:
            checks.append(P("Images — width/height", f"all {total_img} reserve space (explicit dimensions, fill, or aspect-ratio)"))
        if css_reserved > 0:
            checks.append(I("Images — fill/aspect layout", f"{css_reserved}/{total_img} reserve space via CSS (fill / aspect-ratio) — spot-check each parent/style actually constrains the ratio"))

        if first_img_lazy:
            # The real lazy-loading defect: the first (likely LCP) image being
            # deferred delays LCP (Lighthouse lcp-lazy-loaded). Zero lazy is
            # NOT a defect — a single-hero landing page legitimately has none.
            checks.append(W("Images — lazy loading", "first image is loading='lazy' — if it's the LCP element this delays it; make it eager"))
        elif lazy > 0:
            checks.append(P("Images — lazy loading", f"{lazy}/{total_img} use loading='lazy' (first image eager)"))
        else:
            checks.append(I("Images — lazy loading", "none use loading='lazy' — fine for single-hero pages; consider it for below-fold images"))
    else:
        checks.append(I("Images", "no images found on this page"))

    # Links
    all_links = soup.find_all("a", href=True)
    web_links = [(a, urlparse(urljoin(data["final_url"], a["href"]))) for a in all_links
                 if a["href"].strip() and not a["href"].strip().startswith("#")]
    web_links = [(a, u) for a, u in web_links if u.scheme in ("http", "https")]
    internal = [a for a, u in web_links if u.netloc == domain]
    external = [a for a, u in web_links if u.netloc != domain]
    nofollow  = [a for a in all_links if "nofollow" in " ".join(a.get("rel") or [])]
    no_anchor = [a for a in all_links if not a.get_text(strip=True) and not a.find("img")]

    r.update({"internal_links": len(internal), "external_links": len(external),
               "nofollow_links": len(nofollow), "no_anchor_text_links": len(no_anchor)})

    if not internal:
        checks.append(W("Internal links", "none found — poor site interconnection"))
    else:
        checks.append(P("Internal links", f"{len(internal)} found"))

    checks.append(I("External links", str(len(external))))
    checks.append(I("Nofollow links", str(len(nofollow))))

    if len(no_anchor) > 3:
        checks.append(W("Links without anchor text", f"{len(no_anchor)} found — missed keyword signal"))
    else:
        checks.append(P("Links without anchor text", f"{len(no_anchor)} (acceptable)"))

    return r, checks


# ─── 8. Security Headers ─────────────────────────────────────────────────────

def check_security_headers(data: dict) -> tuple[dict, list[Check]]:
    r, checks = {}, []
    headers = data["headers"]

    security_checks = [
        ("Strict-Transport-Security", "HSTS"),
        ("Content-Security-Policy",   "CSP"),
        ("X-Frame-Options",           "X-Frame-Options"),
        ("X-Content-Type-Options",    "X-Content-Type-Options"),
        ("Referrer-Policy",           "Referrer-Policy"),
        ("Permissions-Policy",        "Permissions-Policy"),
    ]
    for header, label in security_checks:
        val = headers.get(header, "")
        r[header] = val or None
        if val:
            snippet = val[:50] + "..." if len(val) > 50 else val
            checks.append(P(label, snippet))
        else:
            checks.append(I(label, "header not observed; security configuration review, not an SEO ranking defect"))

    # HSTS preload bonus check
    hsts = headers.get("Strict-Transport-Security", "")
    if hsts:
        if "preload" in hsts:
            checks.append(P("HSTS — preload directive", "present"))
        else:
            checks.append(I("HSTS — preload directive", "not set; opt-in security choice requiring separate review"))

    return r, checks


# ─── 9. Page Resources ───────────────────────────────────────────────────────

def check_page_resources(soup: BeautifulSoup) -> tuple[dict, list[Check]]:
    r, checks = {}, []

    head = soup.find("head") or soup

    # Scripts
    all_scripts     = soup.find_all("script")
    external_scripts = [s for s in all_scripts if s.get("src")]
    inline_scripts   = [s for s in all_scripts if not s.get("src") and s.string]
    head_scripts     = head.find_all("script", src=True)
    # Render-blocking = same-origin synchronous external scripts in <head>.
    # Use has_attr() not .get() — boolean attributes return "" which is falsy
    # and would mis-classify async/defer scripts as blocking.
    # Exclude: async, defer, type="module" (deferred by default), nomodule.
    render_blocking  = [
        s for s in head_scripts
        if not s.has_attr("async")
        and not s.has_attr("defer")
        and s.get("type", "").lower() != "module"
        and not s.has_attr("nomodule")
    ]

    r.update({"external_scripts": len(external_scripts),
               "inline_scripts": len(inline_scripts),
               "render_blocking_scripts": len(render_blocking)})

    checks.append(I("External scripts total", str(len(external_scripts))))
    checks.append(I("Inline scripts total",   str(len(inline_scripts))))

    if render_blocking:
        checks.append(W("Render-blocking scripts", f"{len(render_blocking)} in <head> without async/defer"))
    else:
        checks.append(P("Render-blocking scripts", "none in <head>"))

    if len(external_scripts) > 15:
        checks.append(W("Script count", f"{len(external_scripts)} external — consider bundling"))
    else:
        checks.append(P("Script count", f"{len(external_scripts)} external (acceptable)"))

    # Stylesheets
    stylesheets  = soup.find_all("link", rel=lambda v: v and "stylesheet" in v)
    inline_styles = soup.find_all("style")
    r.update({"external_stylesheets": len(stylesheets), "inline_styles": len(inline_styles)})

    checks.append(I("Inline style blocks", str(len(inline_styles))))
    if len(stylesheets) > 6:
        checks.append(W("External stylesheets", f"{len(stylesheets)} — consider consolidating"))
    else:
        checks.append(P("External stylesheets", f"{len(stylesheets)} (acceptable)"))

    # Favicon
    favicon = soup.find("link", rel=lambda v: v and any(
        "icon" in x for x in (v if isinstance(v, list) else [v])))
    r["has_favicon"] = bool(favicon)
    if favicon:
        checks.append(P("Favicon", "declared in <head>"))
    else:
        checks.append(W("Favicon", "not declared in <head>"))

    # Resource hints
    preconnect   = soup.find_all("link", rel=lambda v: v and "preconnect" in v)
    dns_prefetch = soup.find_all("link", rel=lambda v: v and "dns-prefetch" in v)
    preloads     = soup.find_all("link", rel=lambda v: v and "preload" in v)
    r.update({"preconnect_hints": len(preconnect), "dns_prefetch_hints": len(dns_prefetch),
               "preload_hints": len(preloads)})

    if preconnect:
        checks.append(P("Preconnect hints", f"{len(preconnect)} found"))
    else:
        checks.append(I("Preconnect hints", "none; only useful for measured critical cross-origin connections"))

    if dns_prefetch:
        checks.append(P("DNS-prefetch hints", f"{len(dns_prefetch)} found"))
    else:
        checks.append(I("DNS-prefetch hints", "none"))

    if preloads:
        checks.append(P("Preload hints", f"{len(preloads)} found"))
    else:
        checks.append(I("Preload hints", "none (consider preloading LCP image/font)"))

    return r, checks


# ─── Score ────────────────────────────────────────────────────────────────────

def calculate_score(all_checks: list[Check]) -> int:
    penalty = sum(
        CRITICAL_PENALTY if c.status == "critical" else
        WARNING_PENALTY  if c.status == "warning"  else 0
        for c in all_checks
    )
    return max(0, 100 - penalty)


def grade(score: int) -> str:
    if score >= 90: return "A"
    if score >= 75: return "B"
    if score >= 60: return "C"
    if score >= 40: return "D"
    return "F"


# ─── Report ───────────────────────────────────────────────────────────────────

SECTION_TITLES = [
    "1. HTTP Signals",
    "2. Indexability",
    "3. Meta Tags",
    "4. Heading Structure",
    "5. Social / OG Tags",
    "6. Structured Data",
    "7. Content Quality",
    "8. Security Headers",
    "9. Page Resources",
]


def format_report(url: str, sections: list[tuple[str, list[Check]]],
                  score: int, full_results: dict) -> str:
    g = grade(score)
    all_checks = [c for _, checks in sections for c in checks]
    n_crit = sum(1 for c in all_checks if c.status == "critical")
    n_warn = sum(1 for c in all_checks if c.status == "warning")
    n_pass = sum(1 for c in all_checks if c.status == "pass")
    n_info = sum(1 for c in all_checks if c.status == "info")
    total  = len(all_checks)

    lines = [
        f"# Page SEO Inspector Report",
        f"",
        f"**URL:** {url}",
        f"**Custom checklist score:** {score}/100  **Grade:** {g}",
        "This is a local heuristic, not a Google score or a ranking forecast.",
        "Scope: served HTML only; JavaScript-rendered content and real-user performance are not tested.",
        f"**Checks:** {total} total — "
        f"🔴 {n_crit} critical  🟡 {n_warn} warnings  ✅ {n_pass} pass  ℹ️  {n_info} info",
        "",
        "---",
        "",
    ]

    for title, checks in sections:
        lines.append(f"## {title}")
        lines.append("")
        for chk in checks:
            lines.append(f"  {chk}")
        lines.append("")

    # Summary table
    lines += [
        "---",
        "",
        "## Quick Reference",
        "",
        "| Signal | Value |",
        "|--------|-------|",
    ]
    m  = full_results.get("meta_tags", {})
    h  = full_results.get("heading_structure", {})
    c  = full_results.get("content_quality", {})
    sc = full_results.get("structured_data", {})
    ht = full_results.get("http_signals", {})
    lines += [
        f"| Title length        | {m.get('title_length', '—')} chars |",
        f"| Meta desc length    | {m.get('meta_description_length', '—')} chars |",
        f"| H1 count            | {h.get('h1_count', '—')} |",
        f"| Word count          | {c.get('word_count', '—')} |",
        f"| Images total        | {c.get('images_total', '—')} |",
        f"| Images missing alt  | {c.get('images_missing_alt', '—')} |",
        f"| Internal links      | {c.get('internal_links', '—')} |",
        f"| External links      | {c.get('external_links', '—')} |",
        f"| Schema types        | {', '.join(sc.get('schema_types', [])) or 'None'} |",
        f"| Script request time | {ht.get('script_request_time_s', '—')}s (not browser TTFB) |",
        f"| Page HTML size      | {ht.get('content_length_kb', '—')}KB |",
    ]

    return "\n".join(lines)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: page_seo_inspector.py <url> [--json]"}),
              file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    output_json = "--json" in sys.argv

    data = fetch_page(url)
    if data.get("error"):
        print(json.dumps({"error": data["error"], "url": url}, ensure_ascii=False))
        sys.exit(1)

    soup = data.pop("soup")
    data.pop("html", None)

    full_results: dict = {"url": data["final_url"]}

    raw_sections = [
        ("1. HTTP Signals",    check_http(data)),
        ("2. Indexability",    check_indexability(data, soup)),
        ("3. Meta Tags",       check_meta(soup)),
        ("4. Heading Structure", check_headings(soup)),
        ("5. Social / OG Tags",  check_social(soup)),
        ("6. Structured Data",   check_schema(soup)),
        ("7. Content Quality",   check_content(data, soup)),
        ("8. Security Headers",  check_security_headers(data)),
        ("9. Page Resources",    check_page_resources(soup)),
    ]

    sections: list[tuple[str, list[Check]]] = []
    for title, (result, checks) in raw_sections:
        key = title.split(". ", 1)[1].lower().replace(" ", "_").replace("/", "_")
        full_results[key] = result
        sections.append((title, checks))

    all_checks = [c for _, checks in sections for c in checks]
    score = calculate_score(all_checks)
    full_results["score"] = score
    full_results["score_kind"] = "custom_checklist_not_google_score"
    full_results["scope"] = "served_html_only_not_rendered_or_real_user_performance"
    full_results["grade"] = grade(score)
    full_results["issues"] = {
        "critical": [c.to_dict() for c in all_checks if c.status == "critical"],
        "warning":  [c.to_dict() for c in all_checks if c.status == "warning"],
        "pass":     [c.to_dict() for c in all_checks if c.status == "pass"],
        "info":     [c.to_dict() for c in all_checks if c.status == "info"],
    }

    if output_json:
        print(json.dumps(full_results, indent=2, ensure_ascii=False))
    else:
        print(format_report(url, sections, score, full_results))


if __name__ == "__main__":
    main()
