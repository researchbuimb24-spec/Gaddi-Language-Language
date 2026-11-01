import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.amu.ac.in/miscellaneous/aligarh-journal-of-linguistics"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

try:
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        content = resp.read().decode("utf-8", errors="ignore")
        print("Page size:", len(content))
        # Look for angular scripts or api calls
        scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', content)
        print("Scripts:", scripts)
        links = re.findall(r'href=["\']([^"\']+)["\']', content)
        print("Linguistic/Journal links:")
        for l in set(links):
            if any(k in l.lower() for k in ["journal", "linguistic", "volume", "pdf", "issue"]):
                print("  ", l)
except Exception as e:
    print("Error:", e)
