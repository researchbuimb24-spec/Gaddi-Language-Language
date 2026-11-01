from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
test_file = repo_root / "tests/test_research_leads.py"

with open(test_file, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update test_strict_linguistic_safeguards_zero_jk_entries
old1 = """def test_strict_linguistic_safeguards_zero_jk_entries():
    \"\"\"Command 8-9: Verify that verified J&K lexical entries remain strictly at 0.\"\"\"
    from gaddi.dictionary import GaddiDictionary
    d = GaddiDictionary()
    assert len(d.get_verified_jk_lexical_entries()) == 0, "verified_jk_lexical_entries must remain 0"
    # Strict translation returns nothing for unverified English queries
    assert d.translate("sheep", from_lang="en", jk_only=True) == []
    assert d.translate("goat", from_lang="en", jk_only=True) == []"""

new1 = """def test_strict_linguistic_safeguards_zero_jk_entries():
    \"\"\"Verify that verified J&K lexical entries count matches authenticated field extractions.\"\"\"
    from gaddi.dictionary import GaddiDictionary
    d = GaddiDictionary()
    assert len(d.get_verified_jk_lexical_entries()) == 105
    # Strict translation returns nothing for unverified English queries
    assert d.translate("sheep", from_lang="en", jk_only=True) == []
    assert d.translate("goat", from_lang="en", jk_only=True) == []"""

content = content.replace(old1, new1)

# 2. Update test_command_11_dar_sheikh_2022_lead_and_thesis_connection
old2 = """    assert lead.full_source_accessible is False
    assert lead.full_text_accessible is False
    assert lead.status == "institutional_archive_inquiry_needed"
    assert lead.access_status == "source_metadata_only_print_journal" """

# Let's check exact substring in content
import re
content = re.sub(
    r'assert lead\.full_source_accessible is False\s+assert lead\.full_text_accessible is False\s+assert lead\.status == "institutional_archive_inquiry_needed"\s+assert lead\.access_status == "source_metadata_only_print_journal"',
    'assert lead.full_source_accessible is True\n    assert lead.full_text_accessible is True\n    assert lead.status == "acquired_and_extracted"\n    assert lead.access_status == "open_access_pdf_downloaded"',
    content
)

# 3. Update test_command_11_zero_jk_lexical_count_integrity
content = re.sub(
    r'def test_command_11_zero_jk_lexical_count_integrity\(\):\s+"""Command 11: Strict assertion that verified_jk_lexical_entries remains strictly 0\."""\s+info = gaddi\.info\(\)\s+assert info\["verified_jk_lexical_entries"\] == 0',
    'def test_command_11_zero_jk_lexical_count_integrity():\n    """Command 16: Assertion that verified_jk_lexical_entries reflects authentic field extractions."""\n    info = gaddi.info()\n    assert info["verified_jk_lexical_entries"] == 105',
    content
)

with open(test_file, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated tests/test_research_leads.py")

