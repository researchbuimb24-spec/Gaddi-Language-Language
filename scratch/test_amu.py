import urllib.request, ssl, re
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request("https://www.amu.ac.in/main.220254b7c6498a8a.js", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
    data = resp.read().decode("utf-8", errors="ignore")

urls = re.findall(r"https?://[a-zA-Z0-9.-]+(?:/[a-zA-Z0-9._~:/?#[\]@!$&'()*+,;=-]*)?", data)
amu_urls = [u for u in set(urls) if "amu.ac.in" in u]
for u in sorted(amu_urls)[:30]:
    print(u)
