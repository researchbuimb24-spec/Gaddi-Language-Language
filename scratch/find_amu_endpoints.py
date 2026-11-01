import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request("https://www.amu.ac.in/main.220254b7c6498a8a.js", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
    data = resp.read().decode("utf-8", errors="ignore")

# Find endpoints defined like _e+"..."
endpoints = re.findall(r'_e\s*\+\s*["\']([^"\']+)["\']', data)
print("Total _e+ endpoints:", len(endpoints))
for ep in sorted(set(endpoints)):
    if any(k in ep.lower() for k in ["journal", "linguistic", "misc", "department", "article", "publication", "volume"]):
        print("  ", ep)

