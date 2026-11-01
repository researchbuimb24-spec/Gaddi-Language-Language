import pypdf

reader = pypdf.PdfReader('data/source_intake/LSI_HIMACHAL_PRADESH.pdf')

# Check PDF page for printed page 1090: offset is 24, so PDF page 1114
p1114 = reader.pages[1114].extract_text()
print("=== PRINTED PAGE 1090 (PDF 1114) ===")
for line in p1114.splitlines():
    if any(k in line.lower() for k in ['eziz', 'amma', 'gobru', 'go:bru', 'mama', 'sala', 'sali', 'mother', 'son', 'boy']):
        print(" ", line)

# Check PDF page for printed page 1092: PDF page 1116
p1116 = reader.pages[1116].extract_text()
print("\n=== PRINTED PAGE 1092 (PDF 1116) ===")
for line in p1116.splitlines():
    if any(k in line.lower() for k in ['146', 'water', 'kú', 'ku']):
        print(" ", line)

# Check PDF page for printed page 1100: PDF page 1124
p1124 = reader.pages[1124].extract_text()
print("\n=== PRINTED PAGE 1100 (PDF 1124) ===")
for line in p1124.splitlines():
    if any(k in line.lower() for k in ['466', 'spider', 'grodd', 'gro']):
        print(" ", line)

