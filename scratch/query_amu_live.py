import urllib.request
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base = "https://api.amu.ac.in/api/v1/"
test_queries = [
    "getNonAcademiceDetail?lang=en&slug=aligarh-journal-of-linguistics",
    "getNonAcadmicContent?lang=en&slug=aligarh-journal-of-linguistics",
    "getNonAcadmicContent?lang=en&slug=aligarh-journal-of-linguistics/home-page",
    "getNonAcadmicContent?lang=en&slug=aligarh-journal-of-linguistics/volume",
    "getNonAcadmicContent?lang=en&slug=aligarh-journal-of-linguistics/archive",
]

for tq in test_queries:
    url = base + tq
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = resp.read().decode("utf-8", errors="ignore")
            print(f"SUCCESS: {tq}")
            res_json = json.loads(data)
            print("  Keys:", list(res_json.keys()))
            if "data" in res_json:
                data_val = res_json["data"]
                if isinstance(data_val, dict):
                    print("  Data keys:", list(data_val.keys()))
                elif isinstance(data_val, list):
                    print("  Data length:", len(data_val))
                    if data_val:
                        print("  Sample item:", str(data_val[0])[:200])
                print("  Preview:", str(data_val)[:300])
    except Exception as e:
        print(f"FAILED: {tq} -> {e}")

