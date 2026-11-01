import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request("https://www.amu.ac.in/main.220254b7c6498a8a.js", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
    data = resp.read().decode("utf-8", errors="ignore")

for pattern in ["department-detail", "getNonAcademiceDetail", "getNonAcadmicContent"]:
    for m in re.finditer(re.escape(pattern), data):
        start = max(0, m.start() - 150)
        end = min(len(data), m.end() + 250)
        print(f"Pattern '{pattern}':")
        print(data[start:end])
        print("=" * 60)

