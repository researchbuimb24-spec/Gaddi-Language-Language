import urllib.request
import ssl
import json
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base = "https://api.amu.ac.in/api/v1/"
vol_slugs = [
    "volume-12-2022-23",
    "volume-13-2023-2024",
    "volume-14-2024-2025",
    "volume-15-2025-26",
]

for slug in vol_slugs:
    url = f"{base}getNonAcadmicContent?lang=en&slug=aligarh-journal-of-linguistics/{slug}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            items = res.get("data", [])
            print(f"\n=== {slug} ({len(items)} items) ===")
            for item in items:
                link = item.get("link", "")
                desc = item.get("link_description", "")
                clean_desc = re.sub(r'<[^>]+>', ' ', desc)
                clean_desc = ' '.join(clean_desc.split())
                print(f"  ID: {item.get('id')} | Title: {link[:80]}")
                text_to_check = (link + " " + clean_desc).lower()
                if any(k in text_to_check for k in ["gaddi", "kinship", "dar", "zargar", "bhaderwah"]):
                    print(f"    --> KEY MATCH: {link}")
                    print(f"    --> Desc: {clean_desc[:250]}")
                    pdf_urls = re.findall(r'href=["\'](https?://[^"\']+\.pdf)["\']', desc)
                    print(f"    --> PDFs: {pdf_urls}")
    except Exception as e:
        print(f"Error fetching {slug}: {e}")
