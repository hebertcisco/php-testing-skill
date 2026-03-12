# PHP Testing Skill

This skill helps an AI agent analyze PHP codebases and make safe testing changes in projects that use PHPUnit, Pest, Laravel, Symfony, or custom PHP application structures.

It is designed for coding agents that can read repository files, follow local instructions, and execute shell commands such as targeted test runs.

## What This Skill Covers

- Detecting the active PHP test stack before changing code
- Inspecting `app/`, `src/`, `tests/`, `config/`, and CI files
- Adding or repairing unit, feature, integration, and pragmatic end-to-end tests
- Improving `phpunit.xml` defaults and test performance
- Extending or creating GitHub Actions workflows for PHP test execution
- Surveying unfamiliar repositories with `scripts/survey_php_project.py`

## Repository Layout

- `SKILL.md`: the main operating instructions for the agent
- `references/`: focused reference documents used only when needed
- `scripts/survey_php_project.py`: helper script for summarizing a PHP repository's testing setup
- `agents/openai.yaml`: optional metadata for OpenAI-compatible skill registries or agent catalogs

## How To Configure The Skill

### 1. Install The Folder In Your Skills Directory

Place this repository in the directory your agent uses for local skills. In Codex-style setups, that is commonly:

```text
$CODEX_HOME/skills/php-testing-skill
```

or:

```text
~/.codex/skills/php-testing-skill
```

The important part is that the agent can read `SKILL.md` at runtime.

### 2. Keep The Skill Structure Intact

The agent expects these files and directories to remain relative to each other:

```text
php-testing-skill/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── framework-detection.md
│   ├── github-actions.md
│   ├── phpunit-optimization.md
│   └── test-authoring.md
└── scripts/
    └── survey_php_project.py
```

If you rename or move these files, update any loader or catalog that references them.

### 3. Make Sure The Runtime Can Execute Basic Tooling

For best results, the host agent should have access to:

- `python3` for `scripts/survey_php_project.py`
- a shell environment
- repository read access
- permission to run narrow test commands such as `./vendor/bin/pest`, `./vendor/bin/phpunit`, or `php artisan test`

The skill still provides value without execution access, but it becomes documentation-only instead of an active implementation workflow.

### 4. Register It In Your Agent Catalog If Needed

Some agents auto-discover `SKILL.md` files from a skills directory. Others require a catalog entry or manifest.

This repository already includes an OpenAI/Codex-oriented descriptor at `agents/openai.yaml`. If your platform supports agent cards or skill manifests, point it to:

- display name: `PHP Testing`
- short description: `PHPUnit, Pest, and PHP CI workflows`
- default prompt: `Use $php-testing-skill to analyze this PHP project, identify its test stack, and add or repair the right tests and CI setup.`

## How Agents Should Use It

The intended workflow is:

1. Read `SKILL.md`.
2. Detect the project's stack from local files before editing tests.
3. Load only the relevant reference files from `references/` and related docs.
4. Run `python3 ./scripts/survey_php_project.py <repo-root>` when the target repository is unfamiliar or large.
5. Add or repair the smallest useful test set first, then verify with the narrowest command.

## AI Compatibility

### Codex

This skill is a direct fit for Codex-style local skill systems that:

- load instructions from `SKILL.md`
- keep reusable assets on disk
- can run shell commands
- can edit files in the target repository

`agents/openai.yaml` is included specifically for OpenAI/Codex-oriented environments.

### Claude

Claude can use this skill effectively if your Claude-based workflow supports local prompt files, project instructions, or tool-enabled agents.

Recommended mapping for Claude-based environments:

- treat `SKILL.md` as the system or project instruction source
- attach only the relevant files from `references/`
- expose `scripts/survey_php_project.py` as an optional helper command
- preserve the workflow rule of detecting the stack before writing tests

Claude does not require the OpenAI YAML file. The important asset is `SKILL.md`.

### ChatGPT And Other OpenAI-Compatible Agents

Any agent that can ingest local instruction files can use this skill, even if it does not support a formal skill registry.

Minimum integration approach:

- load `SKILL.md` into the session
- make the repository files readable
- allow targeted shell execution for verification

### Other LLM Agents

This skill is mostly model-agnostic. It works best with agents that can:

- read multiple local files
- follow ordered workflows
- avoid loading unnecessary context
- run shell commands
- modify source code safely

If an agent is chat-only and cannot access files or tools, you can still reuse `SKILL.md` as a manual operating guide, but the results will be less reliable.

## Compatibility Notes

- The skill is written in plain Markdown and YAML, so there is no model-specific binary format.
- The skill assumes the agent can resolve relative paths correctly.
- The skill assumes the agent can decide when to read additional files instead of loading the entire repository at once.
- The helper script assumes `python3` is installed.
- Test execution assumes the target PHP project already has its own dependencies installed.

## Suggested Prompt Examples

Use prompts like:

- `Use $php-testing-skill to add regression tests for this Laravel bug.`
- `Use $php-testing-skill to detect whether this repo is Pest or PHPUnit first.`
- `Use $php-testing-skill to optimize phpunit.xml and the GitHub Actions test workflow.`

For systems that do not support named skills, adapt the prompt to:

```text
Follow the instructions in php-testing-skill/SKILL.md. Analyze the PHP project's testing stack first, then add or repair the smallest useful set of tests and verify them with the narrowest command.
```

## Maintenance

When updating this skill:

- keep `SKILL.md` as the source of truth for the workflow
- update `references/` only when the guidance meaningfully changes
- keep `agents/openai.yaml` aligned with the public description of the skill
- document new helper scripts in this README
