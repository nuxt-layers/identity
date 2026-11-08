"""Validate Markdown headings, repository-local links and architecture provenance."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys

root = Path(__file__).resolve().parents[1]
# ADR-0010: only RESOURCES.md may link directly to external architecture files,\n# and those references must identify a verified immutable revision.
architecture_link = re.compile(
    r"^https?://github\\.com/nuxt-layers/architecture-rules/(?:blob|tree|raw)/([^/]+)(?:/|$)",
    re.IGNORECASE,
)
errors = []
files = sorted(root.rglob("*.md"))
# .github holds templates whose body GitHub pastes into issues and pull requests.
for file in files:
    if any(part in {".git", ".github", "node_modules", ".nuxt"} for part in file.relative_to(root).parts):
        continue
    lines = file.read_text(encoding="utf-8").splitlines()
    if not any(re.match(r"^#\s+\S", line) for line in lines):
        errors.append(f"{file.relative_to(root)}: missing H1 heading")
    in_fence = False
    for number, line in enumerate(lines, 1):
        if re.match(r"^\s*(?:`{3,}|~{3,})", line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for match in re.finditer(r"!?\[[^\]]*\]\(([^\s)]+)\)", line):
            href = match.group(1).strip("<>")
            parsed = urlsplit(href)
            architecture_match = architecture_link.match(href)
            if architecture_match:
                if file.relative_to(root).as_posix() != "RESOURCES.md":
                    errors.append(f"{file.relative_to(root)}:{number}: architecture links belong in RESOURCES.md")
                elif not re.fullmatch(r"[0-9a-f]{40}", architecture_match.group(1), re.IGNORECASE):
                    errors.append(f"{file.relative_to(root)}:{number}: architecture revision must be a commit SHA")
                continue
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (file.parent / unquote(parsed.path)).resolve()
            if not target.is_relative_to(root) or not target.exists():
                errors.append(f"{file.relative_to(root)}:{number}: broken local link {href}")
if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print(f"Checked {len(files)} Markdown files for headings, local links and architecture provenance")
