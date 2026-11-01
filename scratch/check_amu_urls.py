import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    "https://www.amu.ac.in/department/linguistics/journals",
    "https://amu.ac.in/miscellaneous/aligarh-journal-of-linguistics/home-page",
    "https://amu.ac.in/miscellaneous/aligarh-journal-of-linguistics/volume",
    "https://amu.ac.in/miscellaneous/aligarh-journal-of-linguistics/archive",
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = resp.read()
            print(f"URL: {url} | Status: {resp.status} | Size: {len(data)}")
    except Exception as e:
        print(f"URL: {url} | Error: {e}")

