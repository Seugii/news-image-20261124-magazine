#!/usr/bin/env python3
"""Search Wikimedia Commons for candidate photos (titles + thumb URLs)."""
import json
import urllib.parse
import urllib.request

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "makefun-entry-builder/1.0 (contact: seugii; research use)"}

QUERIES = {
    "huang": "Jensen Huang Nvidia",
    "bitcoin": "Bitcoin coins physical",
    "merkury": "Merkury corvette Russian navy",
    "zaporizhzhia": "Zaporizhzhia damaged building",
    "fire": "factory fire flames industrial",
    "russian_soldiers": "Russian soldiers Ukraine war",
    "nepal": "Kathmandu Nepal",
    "spacex": "Falcon 9 launch SpaceX",
    "un": "United Nations headquarters New York",
    "gaza": "Gaza City destruction",
}

for key, q in QUERIES.items():
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": q + " filetype:bitmap",
        "gsrnamespace": 6,
        "gsrlimit": 6,
        "prop": "imageinfo",
        "iiprop": "url|size|extmetadata",
        "iiurlwidth": 400,
    }
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params), headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    print(f"\n=== {key}: {q} ===")
    for page in (data.get("query", {}).get("pages", {}) or {}).values():
        ii = (page.get("imageinfo") or [{}])[0]
        lic = (ii.get("extmetadata", {}).get("LicenseShortName", {}) or {}).get("value", "?")
        print(f"- {page['title']} | {ii.get('width')}x{ii.get('height')} | {lic} | {ii.get('thumburl', '')}")
