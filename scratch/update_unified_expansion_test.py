from pathlib import Path
import re

repo_root = Path(__file__).resolve().parent.parent
test_file = repo_root / "tests/test_unified_expansion.py"

with open(test_file, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update test_unified_loading_and_counts
content = content.replace("assert len(unified) == 1866", "assert len(unified) == 1971")
content = content.replace("assert len(headwords) == 1682", "assert len(headwords) == 1781")
content = content.replace("assert len(categories) == 19", "assert len(categories) == 24")
content = content.replace("assert d.get_total_records() == 2347", "assert d.get_total_records() == 2472")

content = content.replace('assert info["unified_total_entries"] == 1866', 'assert info["unified_total_entries"] == 1971')
content = content.replace('assert info["unique_headwords"] == 1682', 'assert info["unique_headwords"] == 1781')
content = content.replace('assert info["total_lexical_records"] == 2347', 'assert info["total_lexical_records"] == 2472')
content = content.replace('assert info["categories_count"] == 19', 'assert info["categories_count"] == 24')

# 2. Update test_category_overlap_consistency
content = content.replace("assert sum_cat_entries == 2158", "assert sum_cat_entries == 2202")

# 3. Update test_cli_new_functionality
content = content.replace('assert "Total Unified Entries:           1866" in cap_st.out', 'assert "Total Unified Entries:           1971" in cap_st.out')
content = content.replace('assert "Unique Headwords (Devanagari):   1682" in cap_st.out', 'assert "Unique Headwords (Devanagari):   1781" in cap_st.out')
content = content.replace('assert "Total Lexical Records / Sources: 2347" in cap_st.out', 'assert "Total Lexical Records / Sources: 2472" in cap_st.out')

with open(test_file, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated tests/test_unified_expansion.py")

