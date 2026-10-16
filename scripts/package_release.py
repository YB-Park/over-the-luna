#!/usr/bin/env python3
"""Deterministic RC2 local-plugin ZIP built from explicit allowlist only."""
from __future__ import annotations
import argparse
import hashlib
import sys
import zipfile
from pathlib import Path
from scripts.validate_release import ROOT,PACKAGE_FILES,validate

FILES=PACKAGE_FILES
DATE=(2026,10,16,0,0,0)

def package(root:Path,output:Path) -> tuple[str,int]:
    failures=validate(root)
    if failures:raise ValueError("; ".join(failures))
    for name in FILES:
        if not (root/name).is_file():raise ValueError("missing package member: "+name)
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
    try: sha,size=package(a.root,a.output)
    except ValueError as ex:
        print("RC2_PACKAGE_INVALID:",ex)
        sys.exit(1)
    print(f"RC2_PACKAGE_OK sha256={sha} bytes={size}")
