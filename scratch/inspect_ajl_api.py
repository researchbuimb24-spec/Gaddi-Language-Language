import urllib.request
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base = "https://api.amu.ac.in/api/v1/"

# 1. Inspect links
req = urllib.request.Request(base + "getNonAcademiceDetail?lang=en&slug=aligarh-journal-of-linguistics", headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
    res = json.loads(resp.read().decode("utf-8"))
    links = res.get("data", {}).get("links", [])
    print("Links in journal page:")
    for l in links:
        print(f"  {l.get('id')}: {l.get('link')} -> slug: {l.get('slug')}")

# 2. Inspect volume items
req = urllib.request.Request(base + "getNonAcadmicContent?lang=en&slug=aligarh-journal-of-linguistics/volume", headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
    vol_res = json.loads(resp.read().decode("utf-8"))
    vol_items = vol_res.get("data", [])
    print(f"\nVolume items ({len(vol_items)}):")
    for item in vol_items:
        print(f"  ID: {item.get('id')}")
        print(f"  Link: {item.get('link')}")
        desc = item.get('link_description', '')
        # print first 150 chars of desc stripped of tags
        import re
        clean_desc = re.sub(r'<[^>]+>', ' ', desc)
        clean_desc = ' '.join(clean_desc.split())
        print(f"  Desc: {clean_desc[:150]}")
        print(f"  File: {item.get('file')}")
        print("-" * 40)

