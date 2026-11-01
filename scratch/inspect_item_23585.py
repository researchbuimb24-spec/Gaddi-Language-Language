import urllib.request
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base = "https://api.amu.ac.in/api/v1/"
req = urllib.request.Request(base + "getNonAcadmicContent?lang=en&slug=aligarh-journal-of-linguistics/volume", headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
    vol_res = json.loads(resp.read().decode("utf-8"))
    vol_items = vol_res.get("data", [])
    for item in vol_items:
        if item.get("id") == 23585 or "GADDI" in item.get("link", "").upper():
            print("Full Item 23585:")
            print(json.dumps(item, indent=2))

