#!/usr/bin/env python3
"""Enforce ADR-0012's 50-line host composition budget without building the app."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOST = ROOT / 'examples' / 'minimal-host'
MAX_COMPOSITION_LINES = 50

def main() -> None:
    if not (HOST / 'nuxt.config.ts').is_file():
        raise SystemExit('Missing minimal host nuxt.config.ts')
    if not (HOST / 'server/plugins/identity.ts').is_file():
        raise SystemExit('Missing one-call Identity plugin')
    total = 0
    for path in HOST.rglob('*'):
        if not path.is_file() or path.suffix not in {'.ts', '.js', '.json', '.vue'}:
            continue
        relative = path.relative_to(HOST).as_posix()
        if relative.startswith('app/') or relative.startswith('pages/') or relative.startswith('assets/') or relative.startswith('public/') or relative.startswith('content/') or relative.startswith('data/') or relative == 'app.vue':
            continue
        if '/api/' in relative or '/routes/' in relative:
            continue  # Host-owned routes and product code are excluded.
        contents = path.read_text(encoding='utf-8').splitlines()
        if 'identity' in contents.__str__().lower() or path.name == 'nuxt.config.ts':
            total += len(contents)
    if total > MAX_COMPOSITION_LINES:
        raise SystemExit(f'ADR-0012 host composition: {total} > {MAX_COMPOSITION_LINES} lines')
    print(f'ADR-0012 host composition: {total}/{MAX_COMPOSITION_LINES} lines')

if __name__ == '__main__':
    main()
