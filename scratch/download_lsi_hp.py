import urllib.request
import ssl
import sys
import os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://censusindia.gov.in/nada/index.php/catalog/45246/download/48953/LSI_HIMACHAL_PRADESH.pdf'
out_dir = 'C:/Users/Hp/Documents/Gaddi-Python-Language/data/source_intake'
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, 'LSI_HIMACHAL_PRADESH.pdf')

if os.path.exists(out_file) and os.path.getsize(out_file) > 1000000:
    print(f"Already downloaded: {out_file} ({os.path.getsize(out_file)} bytes)")
    sys.exit(0)

print(f"Downloading from {url}...")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
    total_size = int(resp.headers.get('Content-Length', 0))
    downloaded = 0
    chunk_size = 65536
    with open(out_file, 'wb') as f:
        while True:
            chunk = resp.read(chunk_size)
            if not chunk:
                break
            f.write(chunk)
            downloaded += len(chunk)
            print(f"\rDownloaded {downloaded}/{total_size} bytes ({downloaded*100//total_size}%)", end="")
print("\nDownload complete.")

