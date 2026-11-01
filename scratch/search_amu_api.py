import urllib.request, ssl, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request('https://www.amu.ac.in/main.220254b7c6498a8a.js', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        content = resp.read().decode('utf-8', errors='ignore')
        print('JS size:', len(content))
        # Search for api endpoints
        apis = re.findall(r'https?://[^\s"\']+/api/[^\s"\']+', content)
        print('APIs found:', set(apis[:20]))
        # Search for journal or linguistics in js
        matches = re.findall(r'[\'"]([^\'"]*aligarh-journal[^\'"]*)[\'"]', content)
        print('Journal routes:', set(matches))
except Exception as e:
    print('Error:', e)

