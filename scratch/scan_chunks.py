import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request("https://www.amu.ac.in/runtime.f41365ed84f19036.js", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
    runtime = resp.read().decode("utf-8", errors="ignore")

chunks = re.findall(r'(\d+):"([a-f0-9]+)"', runtime)
print("Scanning", len(chunks), "chunks...")

for chunk_id, chunk_hash in chunks:
    chunk_url = f"https://www.amu.ac.in/{chunk_id}.{chunk_hash}.js"
    try:
        req = urllib.request.Request(chunk_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as c_resp:
            text = c_resp.read().decode("utf-8", errors="ignore")
            if "linguistics" in text.lower() or "journal" in text.lower():
                print(f"Match in chunk {chunk_id}: length {len(text)}")
                # find URLs or api endpoints
                endpoints = re.findall(r'["\'](/api/[^"\']+)["\']', text)
                if endpoints:
                    print(f"  Endpoints: {set(endpoints)}")
                matches = re.findall(r'["\']([^"\']*(?:journal|linguistics|volume)[^"\']*)["\']', text, re.IGNORECASE)
                print(f"  Sample matches: {matches[:5]}")
    except Exception as e:
        pass

