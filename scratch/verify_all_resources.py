from pathlib import Path

data_dir = Path("data")
res_dir = Path("src/gaddi/resources")

for f in data_dir.glob("*.json"):
    res_f = res_dir / f.name
    if res_f.exists():
        b1 = f.read_bytes()
        b2 = res_f.read_bytes()
        assert b1 == b2, f"Mismatch in {f.name}: {len(b1)} bytes vs {len(b2)} bytes"
        print(f"Verified match: {f.name:30s} ({len(b1):,} bytes)")
    else:
        print(f"Note: {f.name} only in data/")

print("ALL resource files verified byte-synchronized!")

