---
name: php-testing-skill
description: Create, repair, and optimize automated tests in PHP projects that use PHPUnit, PestPHP, Laravel, Symfony, or custom app structures. Use when asked to identify the active PHP test stack, analyze `app/` and `config/`, add unit/feature/end-to-end tests, tune `phpunit.xml`, migrate or introduce Pest in PHPUnit projects, increase coverage safely, or create/update GitHub Actions for PHP test workflows.
---

# PHP Testing

## Quick Start

- Prefer the repository's current testing style, helpers, factories, fixtures, and naming before introducing new patterns.
- Detect the active stack first:
  - `composer.json` / `composer.lock`
  - `phpunit.xml` or `phpunit.xml.dist`
  - `tests/Pest.php`
  - `tests/`, `app/`, `src/`, `config/`, `.github/workflows/`
- Run `python3 ./scripts/survey_php_project.py <repo-root>` when the project is unfamiliar or large. Use the output to summarize frameworks, test tooling, app layout, configs, and CI.
- Read only the references needed for the current task:
  - `references/framework-detection.md`
  - `references/test-authoring.md`
  - `references/phpunit-optimization.md`
  - `references/github-actions.md`

## Workflow

1. Detect the project type and test runner before writing code.
2. Inventory the domain under `app/` or `src/`:
   - controllers, models/entities, services, repositories, jobs/commands, middleware, events/listeners, exceptions, policies, helpers, traits
3. Inventory `config/`, `.env.example`, `phpunit.xml*`, and CI files to find:
   - database settings
   - queue/cache/session/mail drivers
   - parallel-test hooks
   - bootstrap and environment assumptions
4. Match the closest existing test layer and style:
   - PHPUnit class style if the repo is PHPUnit-first
   - Pest syntax if the repo is Pest-first or mixed
5. Create or repair the smallest test set that covers the requested behavior and the main regression path.
6. Run the narrowest useful verification command first, then broaden if needed.
7. If asked to optimize or modernize test tooling, adjust config after checking for project-specific constraints.

## Test Layer Selection

- Create **unit tests** for pure helpers, value objects, services with mocked boundaries, repositories with isolated query behavior, custom exceptions, resources, and small framework adapters.
- Create **feature/integration tests** for HTTP endpoints, console commands, jobs, notifications, policies, and database-backed flows.
- Treat **E2E** in PHP pragmatically:
  - If Laravel Dusk, Symfony Panther, Playwright, or another browser/E2E tool already exists, extend that stack.
  - If no browser stack exists, implement end-to-end coverage as full application flow tests through HTTP, console, queues, or persistence boundaries using the repo's existing framework test harness.
- Do not add a new browser framework unless the user asks for it or the repo already supports it.

## App And Config Analysis

- Start with directory shape, not assumptions. Top-level folders often reveal the architecture faster than individual classes.
- In `app/` or `src/`, identify the project's real seams:
  - service layer and orchestration points
  - repositories or query objects
  - model/entity relationships
  - exception hierarchies
  - HTTP/controller validation boundaries
  - async boundaries such as jobs, events, listeners, mail, notifications
- In `config/`, focus on settings that change test behavior:
  - database connections
  - cache/queue/session/mail drivers
  - feature flags
  - third-party service toggles
  - auth and guard configuration
  - filesystem disks
- Prefer describing the discovered conventions back to the user through the resulting tests and config changes instead of writing generic boilerplate.

## Working In Mixed PHPUnit And Pest Repos

- Expect mixed repos. A project can depend on both `phpunit/phpunit` and `pestphp/pest`.
- If Pest is installed and `tests/Pest.php` exists, prefer Pest for new tests unless nearby files strongly suggest PHPUnit classes.
- If the repo is PHPUnit-only and the user asks for Pest:
  - install Pest packages consistent with the framework
  - create `tests/Pest.php`
  - keep existing PHPUnit tests working
  - convert incrementally, not as a large rewrite, unless explicitly requested
- Never convert an existing suite wholesale just to satisfy a small feature request.

## Regression Safety

- When fixing a bug, reproduce the failing behavior first in a focused test.
- When adjusting existing tests, preserve helper contracts, dataset shape, fixture behavior, and shared bootstrap conventions.
- Prefer surgical assertions over broad snapshots or brittle string matching.
- When mocks are necessary, mock external boundaries rather than the class under test.
- If the requested change risks altering global test config, add the minimal config needed and explain the tradeoff.

## Verification

- Prefer narrow commands first, for example:
  - `./vendor/bin/pest tests/Unit/Services/FooTest.php`
  - `./vendor/bin/pest --filter="it_handles_foo"`
  - `./vendor/bin/phpunit tests/Feature/BarTest.php`
  - `php artisan test --filter=FooTest`
- Broaden after the target passes:
  - `./vendor/bin/pest --testsuite=Unit`
  - `./vendor/bin/pest --testsuite=Feature`
  - `composer test`
- If verification cannot run because dependencies, services, or local infra are unavailable, state that clearly and describe the expected command.

## References

- `references/framework-detection.md`: Detect PHPUnit, Pest, Laravel, Symfony, and mixed setups.
- `references/test-authoring.md`: Patterns for unit, feature, and pragmatic E2E tests plus repair workflow.
- `references/phpunit-optimization.md`: Fast `phpunit.xml` and execution strategies.
- `references/github-actions.md`: CI templates and optimization guidance for Laravel, Symfony, and plain PHP.
