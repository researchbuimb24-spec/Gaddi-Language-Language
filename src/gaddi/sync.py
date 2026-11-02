"""Resource synchronization mechanism between authoritative data/ and packaged src/gaddi/resources/."""

import filecmp
import json
import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


def get_default_paths() -> Tuple[Path, Path]:
    """Return default (authoritative_data_dir, packaged_resource_dir) relative to repository root."""
    # Current file is in src/gaddi/sync.py -> root is 2 levels up
    repo_root = Path(__file__).resolve().parents[2]
    data_dir = repo_root / "data"
    res_dir = repo_root / "src" / "gaddi" / "resources"
    return data_dir, res_dir


def get_managed_json_files(data_dir: Path) -> List[str]:
    """Return sorted list of active JSON datasets (excluding .bak backup files)."""
    return sorted([
        f.name
        for f in data_dir.iterdir()
        if f.is_file() and f.suffix == ".json" and not f.name.endswith(".bak")
    ])


def check_resource_sync(
    data_dir: Optional[Path] = None,
    res_dir: Optional[Path] = None,
) -> Tuple[bool, List[str]]:
    """Check synchronization between authoritative data/ and packaged resources/.

    Returns:
        (is_synced: bool, issues: List[str])
    """
    if data_dir is None or res_dir is None:
        def_data, def_res = get_default_paths()
        data_dir = data_dir or def_data
        res_dir = res_dir or def_res

    issues: List[str] = []

    if not data_dir.exists():
        return False, [f"Authoritative data directory not found: {data_dir}"]
    if not res_dir.exists():
        return False, [f"Packaged resources directory not found: {res_dir}"]

    authoritative_files = get_managed_json_files(data_dir)
    res_files = set(get_managed_json_files(res_dir))

    for fname in authoritative_files:
        src_path = data_dir / fname
        dest_path = res_dir / fname

        if not dest_path.exists():
            issues.append(f"Missing packaged resource: {fname}")
            continue

        try:
            with open(src_path, "r", encoding="utf-8") as f1, open(dest_path, "r", encoding="utf-8") as f2:
                d1 = json.load(f1)
                d2 = json.load(f2)
                if d1 != d2:
                    issues.append(f"JSON content mismatch in: {fname}")
        except Exception as e:
            issues.append(f"Error comparing {fname}: {e}")

    for fname in res_files:
        if fname not in authoritative_files:
            issues.append(f"Orphan resource in packaged directory: {fname}")

    return len(issues) == 0, issues


def sync_resources(
    data_dir: Optional[Path] = None,
    res_dir: Optional[Path] = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Synchronize packaged resources from the authoritative data/ directory.

    Args:
        data_dir: Authoritative development source directory (defaults to repo data/).
        res_dir: Target packaged resources directory (defaults to src/gaddi/resources/).
        dry_run: If True, reports planned actions without writing.

    Returns:
        Dict detailing synced files, identical files, and any errors.
    """
    if data_dir is None or res_dir is None:
        def_data, def_res = get_default_paths()
        data_dir = data_dir or def_data
        res_dir = res_dir or def_res

    res_dir.mkdir(parents=True, exist_ok=True)
    authoritative_files = get_managed_json_files(data_dir)

    synced: List[str] = []
    identical: List[str] = []
    errors: List[str] = []

    for fname in authoritative_files:
        src_path = data_dir / fname
        dest_path = res_dir / fname

        try:
            if dest_path.exists() and filecmp.cmp(src_path, dest_path, shallow=False):
                identical.append(fname)
            else:
                if not dry_run:
                    shutil.copy2(src_path, dest_path)
                synced.append(fname)
        except Exception as e:
            errors.append(f"Failed to sync {fname}: {e}")

    return {
        "authoritative_dir": str(data_dir),
        "packaged_dir": str(res_dir),
        "dry_run": dry_run,
        "total_datasets": len(authoritative_files),
        "synced": synced,
        "identical": identical,
        "errors": errors,
        "success": len(errors) == 0,
    }
