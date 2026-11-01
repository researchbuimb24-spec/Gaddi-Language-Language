import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request("https://www.amu.ac.in/runtime.f41365ed84f19036.js", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
    runtime = resp.read().decode("utf-8", errors="ignore")

print("Runtime js length:", len(runtime))
chunks = re.findall(r'(\d+):"([a-f0-9]+)"', runtime)
print("Chunks found:", len(chunks))
for c in chunks[:10]:
    print(c)

