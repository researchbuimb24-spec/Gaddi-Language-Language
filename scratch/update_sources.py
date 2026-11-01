import json

path_data = "data/sources.json"
path_res = "src/gaddi/resources/sources.json"

with open(path_data, "r", encoding="utf-8") as f:
    sources = json.load(f)

for s in sources:
    if s.get("id") == "kumari_2026":
        s["required_attribution"] = "Kumari, P., Mehta, S., Nair, A., Nayak, A., Roy, Y., and Sharma, V. (2026). A Grammar of Gaddi. London: UCL Press. https://doi.org/10.14324/111.9781800089938"
        s["non_endorsement_disclaimer"] = "This library is an independent research project and is not affiliated with, endorsed by, or sponsored by UCL Press or the authors."
        s["adaptations_made"] = [
            "Digital PDF extraction and structured JSON normalization",
            "Documentation and resolution of typographical inversion in Appendix III Table C.3 fractionals (tenth vs sixteenth)",
            "Systematic part-of-speech classification for Appendix II vocabulary",
            "Separation of numbered linguistic examples from surrounding analytical prose",
            "Removal of PDF page running headers from example blocks",
            "Restoration of inter-word whitespace in multi-word IPA forms"
        ]
        s["third_party_materials_excluded_from_cc"] = [
            "Appendix III numeral data collected by Kumari Mamta (doctoral research, Centre for Linguistics, JNU; p. 125 footnote 1)",
            "Appendix II word list based on Anvita Abbi (2001, p. 244) Swadesh list template",
            "Examples 1 and 2 cited from Sir George A. Grierson (LSI 1916)",
            "Typological categories adapted from R.M.W. Dixon (1977) and Beth Levin (1993)"
        ]

with open(path_data, "w", encoding="utf-8") as f:
    json.dump(sources, f, ensure_ascii=False, indent=2)

with open(path_res, "w", encoding="utf-8") as f:
    json.dump(sources, f, ensure_ascii=False, indent=2)

print("sources.json updated successfully.")
