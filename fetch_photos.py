#!/usr/bin/env python3
"""Download chosen Wikimedia Commons photos at fixed widths, record credits."""
import json
import os
import urllib.parse
import urllib.request

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "makefun-entry-builder/1.0 (contact: seugii; research use)"}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "photos")
os.makedirs(OUT, exist_ok=True)

# (local name, Commons file title, thumb width, credit line)
PHOTOS = [
    ("cover_trump_netanyahu.jpg",
     "File:President Donald J. Trump meets with Israeli Prime Minister Benjamin Netanyahu (55429150214).jpg",
     1000,
     "President Donald Trump meets Prime Minister Benjamin Netanyahu in the Oval Office, 28 July 2026. Official White House Photo by Daniel Torok / public domain."),
    ("russia_lyman.jpg",
     "File:Fallen Russian soldiers during the retreat from Lyman.jpg",
     500,
     "Fallen Russian soldiers near Lyman, 2022. File photo, CC BY 4.0."),
    ("zaporizhzhia.jpg",
     "File:Destructions in Zaporizhzhia after Russian attack, 2026-03-17 (13).webp",
     500,
     "Destruction in Zaporizhzhia after a Russian attack, March 2026. File photo, CC BY 4.0."),
    ("bitcoin.jpg",
     "File:Physical bitcoin statistic coin.JPG",
     500,
     "A physical Bitcoin coin. CC BY-SA 3.0."),
    ("huang.jpg",
     "File:Jensen Huang Nvidia Keynote CES 2025.jpg",
     500,
     "Jensen Huang at Nvidia's CES 2025 keynote. CC BY-SA 4.0."),
    ("merkury.jpg",
     "File:Russian Navy Corvette Merkury.jpg",
     500,
     "The Russian corvette Merkury before the attack. CC BY 4.0."),
    ("nepal.jpg",
     "File:Swayambhunath Stupa -Kathmandu Nepal-0336.jpg",
     500,
     "Swayambhunath Stupa, Kathmandu. CC BY-SA 4.0."),
    ("falcon9.jpg",
     "File:CRS-9 mission (28348649546).jpg",
     500,
     "A Falcon 9 launch. CC0, file photo."),
]

credits = {}
for name, title, width, credit in PHOTOS:
    params = {
        "action": "query", "format": "json", "titles": title,
        "prop": "imageinfo", "iiprop": "url|size|extmetadata",
        "iiurlwidth": width,
    }
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params), headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    pages = data.get("query", {}).get("pages", {})
    page = next(iter(pages.values()))
    ii = (page.get("imageinfo") or [{}])[0]
    url = ii.get("thumburl") or ii.get("url")
    lic = (ii.get("extmetadata", {}).get("LicenseShortName", {}) or {}).get("value", "?")
    print(f"{name}: {ii.get('width')}x{ii.get('height')} {lic} <- {url}")
    req2 = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req2, timeout=120) as r2:
        blob = r2.read()
    path = os.path.join(OUT, name)
    with open(path, "wb") as f:
        f.write(blob)
    print(f"  saved {path} ({len(blob)} bytes)")
    credits[name] = credit

with open(os.path.join(OUT, "credits.json"), "w") as f:
    json.dump(credits, f, indent=2)
print("done")
