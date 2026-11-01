import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request("https://www.amu.ac.in/main.220254b7c6498a8a.js", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
    data = resp.read().decode("utf-8", errors="ignore")

# Find environment API URLs
env_matches = re.findall(r'apiUrl:[^,}]+|baseUrl:[^,}]+|apiEndpoint:[^,}]+|api:[^,}]+', data)
print("Env matches:", set(env_matches[:20]))

# Search for any URL with /api/
api_urls = re.findall(r'https?://[a-zA-Z0-9.-]+/api/[^\s"\'`)]+', data)
print("API URLs found:", set(api_urls[:20]))

# Search for "linguistics" anywhere in the file (case-insensitive)
ling_matches = re.findall(r'.{0,50}linguistics.{0,50}', data, re.IGNORECASE)
print("Linguistics occurrences:", len(ling_matches))
for lm in ling_matches[:5]:
    print("  ", lm)

