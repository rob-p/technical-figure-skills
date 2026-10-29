#!/usr/bin/env python3
"""Create and verify a deterministic, single-root skill.zip using stdlib only."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT/"skills"/"scientific-diagrams"


def validate_tree(skill):
    text = (skill/"SKILL.md").read_text()
    if not text.startswith("---\n"):
        raise ValueError("Missing frontmatter")
    frontmatter = text.split("---",2)[1]
    if not re.search(r"^name: scientific-diagrams$",frontmatter,re.M) or not re.search(r"^description: .+",frontmatter,re.M):
        raise ValueError("Missing skill name/description")
    required = ["LICENSE","LICENSE.baoyu","THIRD_PARTY_NOTICES.md","upstream.json",
                "scripts/vector.py","scripts/build_examples.py","assets/toy-data.json"]
    for name in required:
        if not (skill/name).is_file(): raise ValueError(f"Missing {name}")
    for path in skill.rglob("*"):
        if path.is_symlink(): raise ValueError(f"Symlink in skill: {path}")
        if path.suffix == ".md":
            for target in re.findall(r"\]\(([^)]+)\)",path.read_text()):
                if "://" in target or target.startswith("#"): continue
                resolved = (path.parent/target.split("#")[0]).resolve()
                if not resolved.is_relative_to(skill.resolve()) or not resolved.exists():
                    raise ValueError(f"Broken/escaping reference in {path.name}: {target}")


def build(destination):
    validate_tree(SKILL)
    files = [p for p in sorted(SKILL.rglob("*")) if p.is_file() and
             "__pycache__" not in p.parts and p.suffix != ".pyc"]
    manifest = {str(p.relative_to(SKILL)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    payload = {f"scientific-diagrams/{p.relative_to(SKILL).as_posix()}":p.read_bytes() for p in files}
    payload["scientific-diagrams/PACKAGE_MANIFEST.json"] = (json.dumps(manifest,sort_keys=True,indent=2)+"\n").encode()
    destination.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(destination,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name,content in sorted(payload.items()):
            info = zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info,content)
    verify(destination)
    return hashlib.sha256(destination.read_bytes()).hexdigest()


def verify(path):
    with zipfile.ZipFile(path) as archive:
        if archive.testzip(): raise ValueError("Corrupt zip entry")
        names = archive.namelist()
        if len(names) != len(set(names)): raise ValueError("Duplicate archive paths")
        for name in names:
            p = PurePosixPath(name)
            if p.is_absolute() or ".." in p.parts or p.parts[0] != "scientific-diagrams":
                raise ValueError(f"Unsafe archive path: {name}")
        manifest = json.loads(archive.read("scientific-diagrams/PACKAGE_MANIFEST.json"))
        expected = {f"scientific-diagrams/{key}" for key in manifest} | {"scientific-diagrams/PACKAGE_MANIFEST.json"}
        if set(names) != expected: raise ValueError("Archive/manifest contents disagree")
        for name,digest in manifest.items():
            if hashlib.sha256(archive.read(f"scientific-diagrams/{name}")).hexdigest() != digest:
                raise ValueError(f"Manifest hash mismatch: {name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,default=ROOT/"dist"/"skill.zip")
    parser.add_argument("--verify",type=Path)
    args = parser.parse_args()
    if args.verify:
        verify(args.verify); print("Archive paths, CRCs, and file hashes verified.")
    else:
        digest = build(args.out)
        print(f"{args.out}: sha256 {digest}")


if __name__ == "__main__":
    main()
