#!/usr/bin/env python3
"""Validate, package at ZIP root, revalidate; never overwrite or execute source files."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import zipfile
from validate_plugin import validate


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source',help='Portable plugin directory')
    p.add_argument('output',help='New ZIP outside the source directory')
    p.add_argument('--profile',choices=['workspace','public'],default='workspace')
    args=p.parse_args()
    source=Path(args.source).resolve()
    output=Path(args.output).absolute()
    if not source.is_dir() or output.exists() or output.is_symlink() or output.resolve().is_relative_to(source):
        print(json.dumps({'status':'fail','error':'Source must be a directory; output must be new and outside source'})); return 1
    report=validate(source,args.profile)
    if report['status']!='pass': print(json.dumps(report,indent=2)); return 1
    temp=None
    try:
        # Stage on the same filesystem, then exclusive-create final output after revalidation.
        fd,name=tempfile.mkstemp(suffix='.zip',prefix='.plugin-build-',dir=output.parent)
        os.close(fd); temp=Path(name)
        with zipfile.ZipFile(temp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for entry in report['files']:
                file=source/entry['path']
                if file.is_symlink() or not file.is_file(): raise ValueError('Source changed while packaging')
                data=file.read_bytes()
                if hashlib.sha256(data).hexdigest()!=entry['sha256']: raise ValueError('Source changed while packaging')
                info=zipfile.ZipInfo(entry['path'],date_time=(2026,1,1,0,0,0))
                info.create_system=3; info.external_attr=0o100644<<16; info.compress_type=zipfile.ZIP_DEFLATED
                z.writestr(info,data,compresslevel=9)
        packed=validate(temp,args.profile)
        if packed['status']!='pass': print(json.dumps(packed,indent=2)); return 1
        with output.open('xb') as dest, temp.open('rb') as src:
            while True:
                chunk=src.read(65536)
                if not chunk: break
                dest.write(chunk)
        print(json.dumps({'status':'pass','archive':output.name,'bytes':output.stat().st_size,'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'files':len(packed['files']),'warnings':packed['warnings'],'not_checked':packed['not_checked']},indent=2)); return 0
    except (OSError,ValueError,zipfile.BadZipFile) as e:
        print(json.dumps({'status':'fail','error':str(e)})); return 1
    finally:
        if temp is not None: temp.unlink(missing_ok=True)

if __name__=='__main__': sys.exit(main())
