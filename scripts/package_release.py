#!/usr/bin/env python3
"""Reproducible allowlisted local-plugin zip, without experimental scripts/secrets."""
from __future__ import annotations
import argparse
import hashlib
import sys
import zipfile
from pathlib import Path
from scripts.validate_release import ROOT, validate

FILES=("plugin.json","agents/over-the-luna-next.agent.md",
       "README.md","README.ko.md","LICENSE")
DATE=(2026,10,16,0,0,0)

def package(root:Path, output:Path) -> tuple[str,int]:
    errors=validate(root)
    if errors: raise ValueError("invalid candidate: "+"; ".join(errors))
    for name in FILES:
        if not (root/name).is_file(): raise ValueError("missing "+name)
    output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zf:
        for name in FILES:
            info=zipfile.ZipInfo(name,DATE)
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16
            zf.writestr(info,(root/name).read_bytes(),compress_type=zipfile.ZIP_DEFLATED)
    return hashlib.sha256(output.read_bytes()).hexdigest(),output.stat().st_size

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root",type=Path,default=ROOT)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    try:
        digest,size=package(a.root,a.output)
    except ValueError as exc:
        print("PACKAGE_FAILED:",exc)
        sys.exit(1)
    print(f"PACKAGE_OK sha256={digest} bytes={size}")
