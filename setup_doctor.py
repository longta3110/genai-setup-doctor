"""Check whether a local Python environment is ready for GenAI development.

This homework project performs local configuration checks only. It never sends
an API request and never prints the value of an API key.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent
MINIMUM_PYTHON = (3, 10)

REQUIRED_PACKAGES = {
    "dotenv": "python-dotenv",
    "openai": "openai",
    "pydantic": "pydantic",
    "pytest": "pytest",
}

REQUIRED_FILES = (
    ".env",
    ".env.example",
    ".gitignore",
    "README.md",
    "requirements.txt",
)

PLACEHOLDER_WORDS = (
    "replace_with",
    "your_private",
    "your_api",
    "your_available",
    "add_your",
    "changeme",
)


def is_configured(value: str | None) -> bool:
    """Return True when a setting is present and is not an obvious placeholder."""
    if value is None or not value.strip():
        return False

    normalized = value.strip().lower()
    return not any(word in normalized for word in PLACEHOLDER_WORDS)


def package_is_installed(import_name: str) -> bool:
    """Check for an importable Python module without importing it."""
    return importlib.util.find_spec(import_name) is not None


def gitignore_has_rule(project_root: Path, rule: str) -> bool:
    """Check whether .gitignore contains an active rule exactly matching rule."""
    gitignore = project_root / ".gitignore"
    if not gitignore.exists():
        return False

    active_rules = {
        line.strip()
        for line in gitignore.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    return rule in active_rules


def collect_checks(project_root: Path = PROJECT_ROOT) -> list[tuple[str, bool]]:
    """Run every readiness check and return (description, passed) pairs."""
    load_dotenv(project_root / ".env", override=False)

    checks: list[tuple[str, bool]] = []
    checks.append(
        (
            f"Python {MINIMUM_PYTHON[0]}.{MINIMUM_PYTHON[1]} or newer",
            sys.version_info >= MINIMUM_PYTHON,
        )
    )
    checks.append(("Virtual environment is active", sys.prefix != sys.base_prefix))
    checks.append(("Git repository is initialized", (project_root / ".git").is_dir()))

    for import_name, package_name in REQUIRED_PACKAGES.items():
        checks.append(
            (f"Required package is installed: {package_name}", package_is_installed(import_name))
        )

    for file_name in REQUIRED_FILES:
        checks.append((f"Required file exists: {file_name}", (project_root / file_name).exists()))

    checks.append((".env is ignored by Git", gitignore_has_rule(project_root, ".env")))
    checks.append((".venv is ignored by Git", gitignore_has_rule(project_root, ".venv/")))
    checks.append(
        (
            "OPENAI_API_KEY is configured without displaying it",
            is_configured(os.getenv("OPENAI_API_KEY")),
        )
    )
    checks.append(("OPENAI_MODEL is configured", is_configured(os.getenv("OPENAI_MODEL"))))

    return checks


def print_report(checks: list[tuple[str, bool]]) -> bool:
    """Print a readable report and return True only when every check passes."""
    print("Generative AI Setup Doctor")
    print("=" * 72)

    for description, passed in checks:
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {description}")

    all_ready = all(passed for _, passed in checks)
    print("=" * 72)

    if all_ready:
        print("READY: The environment passed every check.")
    else:
        print("NOT READY: Fix each FAIL item and run the doctor again.")

    return all_ready


def main() -> int:
    """Run the doctor and provide a useful shell exit code."""
    return 0 if print_report(collect_checks()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
