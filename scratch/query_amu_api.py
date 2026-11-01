import urllib.request, ssl, json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Test endpoints
endpoints = [
    'https://api.amu.ac.in/api/v1/journal',
    'https://api.amu.ac.in/api/v1/aligarh-journal-of-linguistics',
    'https://api.amu.ac.in/api/v1/aligarh-journal-of-linguistics/volume',
    'https://api.amu.ac.in/api/v1/aligarh-journal-of-linguistics/volumes',
    'https://api.amu.ac.in/api/v1/miscellaneous/aligarh-journal-of-linguistics',
    'https://api.amu.ac.in/api/v1/miscellaneous/aligarh-journal-of-linguistics/volume',
]

for ep in endpoints:
    try:
        req = urllib.request.Request(ep, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            print('SUCCESS', ep, resp.status)
            res = resp.read().decode('utf-8', errors='ignore')
            print(res[:300])
    except Exception as e:
        print('FAILED', ep, e)

