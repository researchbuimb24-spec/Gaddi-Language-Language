import urllib.request
import ssl
from pathlib import Path

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

pdf_url = "https://api.amu.ac.in/storage//file/10353/file_management/1659595804.pdf"
repo_root = Path(__file__).resolve().parent.parent
dest = repo_root / "data/source_intake/dar_sheikh_2022.pdf"

req = urllib.request.Request(pdf_url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
        content = resp.read()
        print("Downloaded bytes:", len(content))
        with open(dest, "wb") as f:
            f.write(content)
        print("Saved to:", dest)
except Exception as e:
    print("Download failed:", e)

