import urllib.request, ssl, re
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request("https://www.amu.ac.in/main.220254b7c6498a8a.js", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
    data = resp.read().decode("utf-8", errors="ignore")

for m in re.finditer(r'baseUrl|apiEndpoint|apiUrl|backend', data, re.IGNORECASE):
    start = max(0, m.start() - 50)
    end = min(len(data), m.end() + 100)
    print(data[start:end])
    print('---')

