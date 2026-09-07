"""Structural checks for the Markdown knowledge base."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FIELDS = {"title", "type", "status", "updated", "scope", "sources", "related"}
PAGE_TYPES = {"concept", "system", "decision", "initiative", "question", "source"}
TYPE_DIRECTORIES = {
    "concept": "domain",
    "system": "systems",
    "decision": "decisions",
    "initiative": "initiatives",
    "question": "questions",
    "source": "sources/records",
}
STATUSES = {
    "concept": {"draft", "synthesized", "accepted", "verified", "superseded"},
    "system": {"draft", "synthesized", "accepted", "verified", "superseded"},
    "decision": {"proposed", "accepted", "superseded"},
    "initiative": {"planned", "active", "blocked", "complete", "cancelled"},
    "question": {"open", "answered", "deferred"},
    "source": {"current", "superseded", "unavailable"},
}
REQUIRED_PATHS = {
    "CLAUDE.md",
    "AGENTS.md",
    "index.md",
    "sources/index.md",
    "_meta/schema.md",
    "_meta/workflows.md",
    "_meta/log.md",
}
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
WIKILINK_RE = re.compile(r"^\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]$")
BODY_WIKILINK_RE = re.compile(r"\[\[([^\]|#\n]+)(?:[#|][^\]\n]*)?\]\]")
LOG_HEADING_RE = re.compile(
    r"^## \[\d{4}-\d{2}-\d{2}\] "
    r"(?:bootstrap|ingest|update|decision|query|lint|archive) \| .+$"
)


def frontmatter(path: Path) -> dict[str, str] | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return None
    values: dict[str, str] = {}
    for line in parts[1].splitlines():
        match = re.match(r"^([a-z_]+):(?:\s*(.*))?$", line)
        if match:
            values[match.group(1)] = (match.group(2) or "").strip().strip("\"'")
    return values


def frontmatter_list(path: Path, key: str) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return []
    block = text.split("---\n", 2)[1]
    values: list[str] = []
    active = False
    for line in block.splitlines():
        if re.match(r"^[a-z_]+:", line):
            active = line.startswith(f"{key}:")
            if active and line.split(":", 1)[1].strip() == "[]":
                return []
            continue
        if active:
            match = re.match(r"^\s+-\s+(.+?)\s*$", line)
            if match:
                values.append(match.group(1).strip().strip("\"'"))
    return values


def content_pages() -> list[Path]:
    pages: list[Path] = []
    for path in ROOT.rglob("*.md"):
        relative = path.relative_to(ROOT)
        if relative.parts[:2] == ("_meta", "templates"):
            continue
        if frontmatter(path) is not None:
            pages.append(path)
    return sorted(pages)


def check_required_structure(errors: list[str]) -> None:
    for relative in sorted(REQUIRED_PATHS):
        if not (ROOT / relative).exists():
            errors.append(f"missing required path: {relative}")
    agents = ROOT / "AGENTS.md"
    if agents.exists() and (not agents.is_symlink() or agents.readlink() != Path("CLAUDE.md")):
        errors.append("AGENTS.md must be a relative symlink to CLAUDE.md")


def check_frontmatter(errors: list[str]) -> None:
    for path in content_pages():
        relative = path.relative_to(ROOT)
        metadata = frontmatter(path)
        assert metadata is not None
        missing = REQUIRED_FIELDS - metadata.keys()
        if missing:
            errors.append(f"{relative}: missing frontmatter fields {sorted(missing)}")
            continue
        page_type = metadata["type"]
        status = metadata["status"]
        if page_type not in PAGE_TYPES:
            errors.append(f"{relative}: unsupported type {page_type!r}")
        else:
            if status not in STATUSES[page_type]:
                errors.append(f"{relative}: unsupported status {status!r} for {page_type!r}")
            expected = TYPE_DIRECTORIES[page_type]
            parent = relative.parent.as_posix()
            if parent != expected and not parent.startswith("archive"):
                errors.append(f"{relative}: type {page_type!r} belongs under {expected}/")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", metadata["updated"]):
            errors.append(f"{relative}: updated must use YYYY-MM-DD")


def check_links(errors: list[str]) -> None:
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        prose = re.sub(r"`[^`\n]*`", "", prose)
        for target in LINK_RE.findall(prose):
            target = target.strip().strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")) or "://" in target:
                continue
            local_target = target.split("#", 1)[0]
            if local_target and not (path.parent / local_target).resolve().exists():
                errors.append(f"{path.relative_to(ROOT)}: broken link {target!r}")
        for target in BODY_WIKILINK_RE.findall(prose):
            target = target.strip().rstrip("\\")
            if not (ROOT / f"{target}.md").resolve().exists():
                errors.append(f"{path.relative_to(ROOT)}: broken wikilink {target!r}")


def check_frontmatter_references(errors: list[str]) -> None:
    for path in content_pages():
        for key in ("sources", "related"):
            for target in frontmatter_list(path, key):
                match = WIKILINK_RE.match(target)
                if match is None:
                    errors.append(f'{path.relative_to(ROOT)}: {key} must use "[[dir/page]]": {target!r}')
                elif not (ROOT / f"{match.group(1)}.md").resolve().exists():
                    errors.append(f"{path.relative_to(ROOT)}: broken {key} reference {target!r}")


def check_index(errors: list[str]) -> None:
    index_text = (ROOT / "index.md").read_text(encoding="utf-8")
    source_text = (ROOT / "sources" / "index.md").read_text(encoding="utf-8")
    for path in content_pages():
        metadata = frontmatter(path)
        assert metadata is not None
        if metadata["status"] == "superseded":
            continue
        relative = path.relative_to(ROOT).as_posix()
        if metadata["type"] == "source":
            marker = f"({path.relative_to(ROOT / 'sources').as_posix()})"
            count = source_text.count(marker)
            location = "sources/index.md"
        else:
            marker = f"({relative})"
            count = index_text.count(marker)
            location = "index.md"
        if count != 1:
            errors.append(f"{location}: active page must be indexed once: {relative} (found {count})")


def check_log(errors: list[str]) -> None:
    path = ROOT / "_meta" / "log.md"
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("## ") and not LOG_HEADING_RE.fullmatch(line):
            errors.append(f"_meta/log.md:{number}: invalid operation heading")


def main() -> int:
    errors: list[str] = []
    check_required_structure(errors)
    if not errors:
        check_frontmatter(errors)
        check_links(errors)
        check_frontmatter_references(errors)
        check_index(errors)
        check_log(errors)
    if errors:
        print("Knowledge checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Knowledge checks passed: {len(content_pages())} canonical pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
