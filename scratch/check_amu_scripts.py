with open('C:/Users/Hp/Documents/Gaddi-Python-Language/scratch/amu_raw.html', 'w', encoding='utf-8') as f:
    import urllib.request, ssl
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request('https://www.amu.ac.in/miscellaneous/aligarh-journal-of-linguistics/volume', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        data = resp.read().decode('utf-8', errors='ignore')
        f.write(data)

import re
scripts = re.findall(r'<script[^>]*src=[\'"](.*?)[\'"]', data)
print('Scripts:', scripts)

