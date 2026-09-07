"""Create a separate, cross-agent project knowledge repository."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path


PLACEHOLDER = "{{PROJECT_NAME}}"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    if not slug:
        raise ValueError("project name must contain at least one letter or number")
    return slug


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create an independent project knowledge repository."
    )
    parser.add_argument("parent", type=Path, help="Parent workspace directory")
    parser.add_argument("--project-name", help="Human-readable project name")
    parser.add_argument("--knowledge-name", help="Knowledge repository directory name")
    parser.add_argument(
        "--no-git", action="store_true", help="Create files without running git init"
    )
    return parser.parse_args()


def copy_scaffold(source: Path, target: Path, project_name: str) -> None:
    for source_path in sorted(source.rglob("*")):
        relative = source_path.relative_to(source)
        target_path = target / relative
        if source_path.is_dir():
            target_path.mkdir(parents=True, exist_ok=True)
            continue
        target_path.parent.mkdir(parents=True, exist_ok=True)
        if source_path.suffix in {".md", ".toml", ".py"} or source_path.name in {
            "Makefile",
            ".gitignore",
        }:
            text = (
                source_path.read_text(encoding="utf-8")
                .replace(PLACEHOLDER, project_name)
                .replace("{{TODAY}}", date.today().isoformat())
            )
            target_path.write_text(text, encoding="utf-8")
        else:
            shutil.copy2(source_path, target_path)


def main() -> int:
    args = parse_args()
    parent = args.parent.expanduser().resolve()
    if not parent.is_dir():
        print(f"Parent workspace does not exist: {parent}", file=sys.stderr)
        return 2

    project_name = args.project_name or parent.name.replace("_", " ").title()
    knowledge_name = args.knowledge_name or f"{slugify(project_name)}_knowledge"
    if Path(knowledge_name).name != knowledge_name or knowledge_name in {".", ".."}:
        print("--knowledge-name must be one directory name", file=sys.stderr)
        return 2

    target = parent / knowledge_name
    if target.exists() and any(target.iterdir()):
        print(f"Refusing to overwrite non-empty target: {target}", file=sys.stderr)
        return 3


    target.mkdir(parents=True, exist_ok=True)
    scaffold = Path(__file__).resolve().parents[1] / "assets" / "knowledge-repo"
    copy_scaffold(scaffold, target, project_name)

    agents = target / "AGENTS.md"
    if agents.exists() or agents.is_symlink():
        agents.unlink()
    agents.symlink_to("CLAUDE.md")

    git_initialized = False
    if not args.no_git:
        result = subprocess.run(
            ["git", "init", "-b", "main", str(target)],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(result.stderr.strip(), file=sys.stderr)
            return result.returncode
        git_initialized = True

    print(
        json.dumps(
            {
                "knowledge_repository": str(target),
                "project_name": project_name,
                "git_initialized": git_initialized,
                "next": [
                    "read _meta/schema.md and _meta/workflows.md",
                    "wire the parent CLAUDE.md and AGENTS.md",
                    "run make lint and make status",
                ],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
