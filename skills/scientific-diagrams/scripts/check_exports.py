#!/usr/bin/env python3
"""Structural QA for trusted outputs produced by the bundled renderer."""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET


def check(directory):
    directory = Path(directory)
    reports = sorted(directory.glob("*.qa.json"))
    errors = []
    if not reports:
        return ["No QA reports found"]
    for path in reports:
        stem = path.name.removesuffix(".qa.json")
        report = json.loads(path.read_text())
        if report.get("violations") or report.get("text_overlaps"):
            errors.append(f"{stem}: layout report has errors")
        for ext in ("svg","pdf","png"):
            asset = directory/f"{stem}.{ext}"
            if not asset.is_file():
                errors.append(f"Missing {asset.name}"); continue
            actual = hashlib.sha256(asset.read_bytes()).hexdigest()
            if report.get("sha256",{}).get(ext) != actual:
                errors.append(f"{asset.name}: export hash missing or changed")
        svg = directory/f"{stem}.svg"
        if not svg.exists():
            continue
        root = ET.parse(svg).getroot()
        tags = [e.tag.rsplit("}",1)[-1] for e in root.iter()]
        if "text" not in tags or "title" not in tags or "desc" not in tags:
            errors.append(f"{stem}: missing live text or accessible description")
        if set(tags) & {"image","script","foreignObject"}:
            errors.append(f"{stem}: unexpected raster/active content")
        for element in root.iter():
            for key,value in element.attrib.items():
                if key.lower().startswith("on") or (key.endswith("href") and not value.startswith("#")):
                    errors.append(f"{stem}: active or external reference")
        dimensions = [float(root.attrib[k].removesuffix("pt")) for k in ("width","height")]
        if dimensions != report.get("canvas_pt"):
            errors.append(f"{stem}: SVG and QA dimensions disagree")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    args = parser.parse_args()
    errors = check(args.directory)
    for error in errors:
        print(error)
    if errors:
        raise SystemExit(1)
    print("Structural export checks passed; visual/scientific review remains separate.")


if __name__ == "__main__":
    main()
