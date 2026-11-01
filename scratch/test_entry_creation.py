import json
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent

# Let's import Gaddi models and validator
import sys
sys.path.insert(0, str(repo_root / "src"))

from gaddi.models import LexicalEntry, Sense, Attestation, ExampleSentence, EvidenceStatus
from gaddi.validator import GaddiValidator

print("Testing validator import successfully.")

