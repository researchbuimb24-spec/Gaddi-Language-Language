import urllib.request
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base = "https://api.amu.ac.in/api/v1/"
test_queries = [
    "getNonAcademiceDetail?slug=aligarh-journal-of-linguistics",
    "getNonAcadmicContent?slug=aligarh-journal-of-linguistics",
    "department-detail?slug=linguistics",
    "department-detail?slug=department-of-linguistics",
    "left-side-menu?slug=aligarh-journal-of-linguistics",
    "left-side-menu?slug=linguistics",
]

for tq in test_queries:
    url = base + tq
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = resp.read().decode("utf-8", errors="ignore")
            print(f"SUCCESS: {tq}")
            print("  Response preview:", data[:300])
    except Exception as e:
        print(f"FAILED: {tq} -> {e}")

