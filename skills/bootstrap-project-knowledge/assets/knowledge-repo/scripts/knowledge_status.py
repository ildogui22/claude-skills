"""Print a compact knowledge-base status snapshot."""

from __future__ import annotations

from collections import Counter

from check_knowledge import ROOT, content_pages, frontmatter


def main() -> None:
    pages = content_pages()
    by_type: Counter[str] = Counter()
    by_status: Counter[str] = Counter()
    initiatives: list[tuple[str, str, str]] = []
    for path in pages:
        metadata = frontmatter(path)
        assert metadata is not None
        by_type[metadata["type"]] += 1
        by_status[metadata["status"]] += 1
        if metadata["type"] == "initiative":
            initiatives.append((metadata["title"], metadata["status"], metadata["updated"]))

    print("{{PROJECT_NAME}} knowledge status")
    print(f"Pages: {len(pages)}")
    print("By type: " + (", ".join(f"{key}={by_type[key]}" for key in sorted(by_type)) or "none"))
    print("By status: " + (", ".join(f"{key}={by_status[key]}" for key in sorted(by_status)) or "none"))
    print("\nInitiatives:")
    if initiatives:
        for title, status, updated in sorted(initiatives):
            print(f"- {title}: {status} (updated {updated})")
    else:
        print("- none")

    headings = [
        line.removeprefix("## ")
        for line in (ROOT / "_meta" / "log.md").read_text(encoding="utf-8").splitlines()
        if line.startswith("## [")
    ]
    print("\nRecent knowledge operations:")
    for heading in headings[-5:]:
        print(f"- {heading}")


if __name__ == "__main__":
    main()
