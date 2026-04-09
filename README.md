# PHP Testing Skill

An agent skill that detects a PHP project's test stack and safely adds, repairs, or optimizes tests and CI workflows. Works with PHPUnit, PestPHP, Laravel, Symfony, and plain PHP projects.

## Features

- **Stack detection** -- identifies PHPUnit (8-13) and Pest (v2-v4) versions, mixed setups, and framework before touching code
- **Version-aware authoring** -- uses attributes vs annotations, correct mock APIs, and version-appropriate patterns based on the detected PHPUnit major version
- **App analysis** -- inspects `app/`, `src/`, `config/`, and CI files to understand project structure
- **Test authoring** -- adds unit, feature, integration, and E2E tests matching existing conventions
- **Pest v4 browser testing** -- supports Playwright-based browser tests, smoke testing, visual regression, and test sharding
- **PHPUnit tuning** -- optimizes `phpunit.xml` defaults, execution speed, and configuration migration
- **CI workflows** -- creates or refines GitHub Actions pipelines including sharded test matrix strategies
- **Project survey** -- Python script that summarizes an unfamiliar repo's testing setup as JSON, including detected versions

## Quick Start

### Claude Code

This skill is published to the Claude Code skill registry. Install it with:

```
/install-skill php-testing-skill
```

Or add it manually as a project skill by placing this folder inside your project and referencing `SKILL.md` in your project instructions.

### Other Agents

1. Place this folder where your agent reads local skills (e.g. `~/.codex/skills/php-testing-skill`).
2. Point your agent at `SKILL.md` -- that file contains all operating instructions.
3. Ensure the agent can run shell commands and read repository files.

## How It Works

The agent follows this workflow:

1. **Detect** the project's test runner and framework from `composer.json`, `phpunit.xml`, `tests/Pest.php`, and directory structure.
2. **Analyze** the domain code under `app/` or `src/` and the config under `config/` and `.env.example`.
3. **Match** the closest existing test layer and style (PHPUnit classes vs. Pest syntax).
4. **Create or repair** the smallest useful test set, then verify with the narrowest command.
5. **Load references** from `references/` only when the task requires deeper guidance.

## Repository Layout

```
php-testing-skill/
  SKILL.md                            # Main agent instructions (source of truth)
  README.md                           # This file
  agents/
    openai.yaml                       # OpenAI/Codex skill registry metadata
  references/
    framework-detection.md            # PHPUnit vs Pest vs mixed detection rules
    test-authoring.md                 # Patterns for unit, feature, and E2E tests
    phpunit-optimization.md           # Fast phpunit.xml and execution strategies
    github-actions.md                 # CI templates for Laravel, Symfony, plain PHP
  scripts/
    survey_php_project.py             # Project survey helper
```

## Survey Script

The included survey script produces a JSON summary of any PHP project's testing setup:

```bash
python3 ./scripts/survey_php_project.py /path/to/php-project
```

Output includes:
- Detected frameworks and test runner (PHPUnit, Pest, mixed)
- App structure breakdown (`app/` or `src/` directory classification)
- Test file inventory by suite (Unit, Feature, etc.)
- Config files and CI workflow paths
- Key file presence (composer.json, phpunit.xml, artisan, etc.)

Useful for large or unfamiliar codebases where manual inspection would be slow.

## Agent Compatibility

This skill is plain Markdown and YAML -- no model-specific binaries. It works with any agent that can read local files and run shell commands.

| Agent | Integration |
|-------|------------|
| **Claude Code** | Install as a skill or load `SKILL.md` as project instructions |
| **Codex** | Auto-discovers from skills directory; `agents/openai.yaml` included |
| **ChatGPT / OpenAI agents** | Load `SKILL.md` into the session with repo access |
| **Other LLM agents** | Load `SKILL.md` + enable file reading and shell execution |
| **Chat-only (no tools)** | Use `SKILL.md` as a manual reference guide (limited) |

### Runtime Requirements

- `python3` for the survey script
- Shell access for test verification commands
- Repository read access
- Permission to run `./vendor/bin/pest`, `./vendor/bin/phpunit`, or `php artisan test`

The skill still works without execution access, but becomes documentation-only.

## Prompt Examples

```
Use $php-testing-skill to add regression tests for this Laravel bug.
```

```
Use $php-testing-skill to detect whether this repo uses Pest or PHPUnit.
```

```
Use $php-testing-skill to optimize phpunit.xml and the GitHub Actions test workflow.
```

For agents without named skill support:

```
Follow the instructions in php-testing-skill/SKILL.md. Analyze the PHP project's
testing stack first, then add or repair the smallest useful set of tests and verify
them with the narrowest command.
```

## Maintenance

- `SKILL.md` is the source of truth for the agent workflow.
- Update `references/` only when guidance meaningfully changes.
- Keep `agents/openai.yaml` aligned with the skill's public description.
- Document new helper scripts in this README.
