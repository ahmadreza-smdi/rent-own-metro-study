"""Rebuild twice in a disposable copy; compare bytes, not economic validity."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def output_hashes(root):
    paths = [root / 'preparation.json']
    for directory in ('prepared', 'model', 'web'):
        paths.extend(p for p in (root / directory).rglob('*') if p.is_file())
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(paths)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--javascript", action="store_true", help="Also compare the JS model with Python CSV outputs; requires Node.js 18+")
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'MANIFEST.json').read_text())
    for name, expected in manifest.items():
        data = (ROOT / name).read_bytes()
        if len(data) != expected['bytes'] or hashlib.sha256(data).hexdigest() != expected['sha256']:
            raise ValueError('Package manifest mismatch: ' + name)
    with tempfile.TemporaryDirectory(prefix='rent-own-rebuild-') as temporary:
        target = Path(temporary)
        for name in manifest:
            destination = target / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, destination)
        snapshots = []
        for _ in range(2):
            for command in ('prepare_sources.py', 'build_scenarios.py', 'build_preview.py'):
                subprocess.run([sys.executable, '-B', command], cwd=target, check=True,
                               stdout=subprocess.DEVNULL)
            snapshots.append(output_hashes(target))
        if snapshots[0] != snapshots[1]:
            raise ValueError('Repeated rebuild output bytes differ')
        if args.javascript:
            def rows(name):
                with (target / 'model' / name).open(encoding='utf-8', newline='') as stream:
                    return list(csv.DictReader(stream))
            payload = {'data': json.loads((target / 'web/studies/rent-own-2026/study-data.json').read_text()),
                       'summary': rows('metro-scenarios.csv'),
                       'detail': rows('hud-area-scenarios.csv')}
            subprocess.run(['node', 'check_model_parity.mjs'], cwd=target, check=True,
                           input=json.dumps(payload), text=True)
        print(json.dumps({'status': 'PASS', 'manifest_files_checked': len(manifest),
                          'repeated_output_files': len(snapshots[0]),
                          'same_runtime_rebuilds': 2,
                          'scope': 'Package integrity and repeated offline build; not market validity, cross-platform equivalence or browser interaction'}, indent=2))


if __name__ == '__main__':
    main()
