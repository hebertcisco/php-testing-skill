#!/usr/bin/env python3
"""Survey a PHP project for test tooling, app structure, config, and CI files."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return {}


def top_level_dirs(path: Path) -> list[str]:
    if not path.exists():
        return []
    return sorted(item.name for item in path.iterdir() if item.is_dir())


def list_files(path: Path, limit: int = 40) -> list[str]:
    if not path.exists():
        return []
    files = sorted(
        str(item.relative_to(path.parent))
        for item in path.rglob("*")
        if item.is_file() and ".git" not in item.parts and not item.name.startswith(".")
    )
    return files[:limit]


def count_php_files(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for item in path.rglob("*.php") if item.is_file())


def classify_app_dirs(path: Path) -> dict[str, int]:
    counters: Counter[str] = Counter()
    if not path.exists():
        return {}
    for item in path.rglob("*.php"):
        rel_parts = item.relative_to(path).parts
        if not rel_parts:
            continue
        counters[rel_parts[0]] += 1
    return dict(sorted(counters.items()))


def detect_frameworks(composer: dict, root: Path) -> dict[str, object]:
    require = composer.get("require", {})
    require_dev = composer.get("require-dev", {})
    packages = {**require, **require_dev}

    phpunit = "phpunit/phpunit" in packages or (root / "phpunit.xml").exists() or (root / "phpunit.xml.dist").exists()
    pest = "pestphp/pest" in packages or (root / "tests" / "Pest.php").exists()
    laravel = "laravel/framework" in require or (root / "artisan").exists()
    symfony = (
        "symfony/framework-bundle" in packages
        or (root / "bin" / "console").exists()
        or (root / "config" / "bundles.php").exists()
    ) and not laravel
    codeception = "codeception/codeception" in packages
    dusk = "laravel/dusk" in packages
    panther = "symfony/panther" in packages

    if pest and phpunit:
        runner = "mixed-pest-phpunit"
    elif pest:
        runner = "pest"
    elif phpunit:
        runner = "phpunit"
    else:
        runner = "unknown"

    app_root = "app" if (root / "app").exists() else "src" if (root / "src").exists() else None

    return {
        "primary_test_runner": runner,
        "uses_phpunit": phpunit,
        "uses_pest": pest,
        "is_laravel": laravel,
        "is_symfony": symfony,
        "has_codeception": codeception,
        "has_browser_e2e": dusk or panther,
        "browser_e2e_tools": [name for name, enabled in {"laravel-dusk": dusk, "symfony-panther": panther}.items() if enabled],
        "app_root": app_root,
    }


def summarize_tests(root: Path) -> dict[str, object]:
    tests_dir = root / "tests"
    if not tests_dir.exists():
        return {"exists": False}

    buckets: Counter[str] = Counter()
    for item in tests_dir.rglob("*Test.php"):
        rel_parts = item.relative_to(tests_dir).parts
        bucket = rel_parts[0] if rel_parts else "tests"
        buckets[bucket] += 1

    return {
        "exists": True,
        "top_level_dirs": top_level_dirs(tests_dir),
        "test_file_counts": dict(sorted(buckets.items())),
        "has_pest_bootstrap": (tests_dir / "Pest.php").exists(),
        "sample_test_files": list_files(tests_dir, limit=30),
    }


def summarize_workflows(root: Path) -> dict[str, object]:
    workflows_dir = root / ".github" / "workflows"
    if not workflows_dir.exists():
        return {"exists": False}
    files = sorted(str(item.relative_to(root)) for item in workflows_dir.rglob("*") if item.is_file())
    return {
        "exists": True,
        "files": files,
    }


def summarize_config(root: Path) -> dict[str, object]:
    config_dir = root / "config"
    if not config_dir.exists():
        return {"exists": False}
    return {
        "exists": True,
        "files": sorted(item.stem for item in config_dir.glob("*.php")),
        "sample_nested_files": list_files(config_dir, limit=30),
    }


def summarize_app(root: Path, app_root: str | None) -> dict[str, object]:
    if not app_root:
        return {"exists": False}
    app_dir = root / app_root
    return {
        "exists": True,
        "root": app_root,
        "top_level_dirs": top_level_dirs(app_dir),
        "php_file_count": count_php_files(app_dir),
        "class_count_by_top_level_dir": classify_app_dirs(app_dir),
    }


def summarize_commands(composer: dict) -> dict[str, object]:
    scripts = composer.get("scripts", {})
    return {
        "composer_scripts": scripts,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Survey a PHP project for testing context.")
    parser.add_argument("root", nargs="?", default=".", help="Path to the repository root")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    composer = read_json(root / "composer.json")
    frameworks = detect_frameworks(composer, root)

    result = {
        "root": str(root),
        "project_name": composer.get("name"),
        "frameworks": frameworks,
        "app": summarize_app(root, frameworks["app_root"]),
        "config": summarize_config(root),
        "tests": summarize_tests(root),
        "ci": summarize_workflows(root),
        "tooling": summarize_commands(composer),
        "key_files_present": {
            "composer_json": (root / "composer.json").exists(),
            "phpunit_xml": (root / "phpunit.xml").exists(),
            "phpunit_xml_dist": (root / "phpunit.xml.dist").exists(),
            "pest_bootstrap": (root / "tests" / "Pest.php").exists(),
            "artisan": (root / "artisan").exists(),
            "symfony_console": (root / "bin" / "console").exists(),
        },
    }

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
