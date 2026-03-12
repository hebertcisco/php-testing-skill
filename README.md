# PHP Testing Skill

This project provides a comprehensive skill set for creating, repairing, and optimizing automated tests in PHP projects.

## Description

This skill is designed to assist with PHP projects using PHPUnit, PestPHP, Laravel, Symfony, or custom application structures. It can identify the active PHP test stack, analyze `app/` and `config/` directories, add or repair unit, feature, and end-to-end tests, tune `phpunit.xml`, migrate or introduce Pest in PHPUnit projects, increase test coverage safely, and create or update GitHub Actions for PHP test workflows.

## Quick Start

- **Prefer existing styles**: Always mirror the repository's current testing style, helpers, factories, fixtures, and naming conventions before introducing new patterns.
- **Detect the active stack**: Begin by detecting the active test stack using files like `composer.json`, `composer.lock`, `phpunit.xml` (or `phpunit.xml.dist`), `tests/Pest.php`, and directories such as `tests/`, `app/`, `src/`, `config/`, and `.github/workflows/`.
- **Survey unfamiliar projects**: For unfamiliar or large projects, run the `survey_php_project.py` script to summarize frameworks, test tooling, app layout, configurations, and CI setups.
- **Read relevant references**: Only consult the necessary reference documents for the current task.

## Workflow

1.  **Detect project type and test runner** before writing code.
2.  **Inventory the domain** under `app/` or `src/`, including controllers, models/entities, services, repositories, jobs/commands, middleware, events/listeners, exceptions, policies, helpers, and traits.
3.  **Inventory configuration files** (`config/`, `.env.example`, `phpunit.xml*`, and CI files) to find database settings, queue/cache/session/mail drivers, parallel-test hooks, bootstrap, and environment assumptions.
4.  **Match existing test style**: Adopt either PHPUnit class style or Pest syntax based on the project's primary convention.
5.  **Create or repair tests**: Develop the smallest test set that covers the requested behavior and the main regression path.
6.  **Verify narrowly**: Run the narrowest useful verification command first, then broaden if necessary.
7.  **Optimize/modernize**: If optimizing or modernizing test tooling, adjust configuration after checking for project-specific constraints.

## Test Layer Selection

-   **Unit Tests**: Use for pure helpers, value objects, services with mocked boundaries, repositories with isolated query behavior, custom exceptions, resources, and small framework adapters.
-   **Feature/Integration Tests**: Use for HTTP endpoints, console commands, jobs, notifications, policies, and database-backed flows.
-   **Pragmatic E2E Tests**: Extend existing browser tools (Laravel Dusk, Symfony Panther, Playwright, etc.) if present. If no browser stack exists, implement E2E coverage as full application-flow tests through HTTP, console, queues, or persistence boundaries using the existing PHP test harness. Do not add a new browser framework unless explicitly requested.

## Framework Detection

-   **PHPUnit-first**: `phpunit/phpunit` in dependencies, no `tests/Pest.php`, tests extend `Tests\TestCase` or `PHPUnit\Framework\TestCase`.
-   **Pest-first**: `pestphp/pest` installed, `tests/Pest.php` exists, tests use `it()`, `test()`, `beforeEach()`, datasets, and expectations.
-   **Mixed**: Both PHPUnit and Pest installed; keep both working and prefer local convention.
-   **Laravel**: `laravel/framework` in `composer.json`, `artisan` at root, tests use `php artisan test`, `RefreshDatabase`, factories, etc.
-   **Symfony**: `symfony/*` packages, `bin/console`, tests use `KernelTestCase`, `WebTestCase`, etc.

## Test Authoring

-   **Mirror existing style**: Follow the repository's current style.
-   **Cover behavior**: Focus on behavior, not implementation details.
-   **Reproduce regressions**: When fixing bugs, reproduce the regression first.
-   **Mock external boundaries**: Mock external dependencies, not the subject under test.

## PHPUnit Optimization

-   **Safe Defaults**: Keep test environment variables in `phpunit.xml`, prefer in-memory SQLite if supported, use fast drivers (array for cache/session/mail, sync for queue, null for logs), lower bcrypt cost, and disable optional observability/third-party integrations.
-   **Typical `phpunit.xml` Improvements**: Define explicit suites, scope coverage to app code, add focused `<php>` env settings, and avoid unnecessary bootstrap code.
-   **Laravel Notes**: Prefer `php artisan test`, use `RefreshDatabase` only where needed, and check for hidden slow paths in model observers, event listeners, queued jobs, external SDKs, and heavy seeders.
-   **Parallelization**: Use only after confirming isolation safety; check for collisions in static caches, shared files, singleton state, queue names, and external ports.

## GitHub Actions

-   **Common Structure**: Checkout code, set up PHP, cache Composer, install dependencies, prepare env/writable directories, prepare database/services (if needed), run test command, and upload logs/artifacts on failure.
-   **Laravel Template**: Includes steps for `artisan key:generate`, `mkdir -p database && touch database/database.sqlite`, and `php artisan migrate --force` with `DB_CONNECTION: sqlite`.
-   **Symfony or Plain PHP Template**: Simpler template, typically running `./vendor/bin/phpunit` or `./vendor/bin/pest`.
-   **Optimization Levers**: Use `coverage: none`, cache Composer, avoid unnecessary service containers, prefer SQLite for CI (if supported), and split unit/integration suites if justified.

## `survey_php_project.py` Script

This Python script surveys a PHP project to detect its testing context, including frameworks, test runners, application structure, configuration, and CI/CD workflows. It provides a structured JSON output summarizing these aspects.