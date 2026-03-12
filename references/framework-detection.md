# Framework Detection

## Goal

Detect the real test stack before editing tests or CI.

## Check Order

1. Inspect `composer.json` and `composer.lock`.
2. Inspect `phpunit.xml` or `phpunit.xml.dist`.
3. Inspect `tests/Pest.php`.
4. Inspect `tests/`, `app/`, `src/`, `config/`, and `.github/workflows/`.
5. Confirm the nearest existing test style around the files you will edit.

## Detection Rules

- **PHPUnit-first**
  - `phpunit/phpunit` exists in dependencies.
  - No `tests/Pest.php`.
  - Existing tests mostly extend `Tests\TestCase` or `PHPUnit\Framework\TestCase`.
- **Pest-first**
  - `pestphp/pest` exists.
  - `tests/Pest.php` exists.
  - Existing tests mainly use `it()`, `test()`, `beforeEach()`, datasets, and expectations.
- **Mixed**
  - Both PHPUnit and Pest are installed.
  - Keep both working.
  - Prefer the local convention near the changed area.

## Framework Hints

- **Laravel**
  - `laravel/framework` in `composer.json`
  - `artisan` at repo root
  - tests often use `php artisan test`, `RefreshDatabase`, factories, notifications, queues
- **Symfony**
  - one or more `symfony/*` packages
  - `bin/console`
  - tests may use `KernelTestCase`, `WebTestCase`, Panther, Messenger, Doctrine fixtures
- **Plain PHP or custom framework**
  - no major framework package
  - lean harder on the existing bootstrap and helpers

## E2E Detection

- Reuse an existing browser tool if present:
  - `laravel/dusk`
  - `symfony/panther`
  - Playwright, Cypress, Codeception, Behat, or custom scripts in the repo
- If no browser tool exists, interpret E2E as full application-flow testing through the existing PHP test harness unless the user asks for a browser stack.

## Files Worth Reading Next

- `phpunit.xml*`: suites, bootstrap, env, source/include, coverage, extensions
- `tests/Pest.php`: shared hooks, global `uses()`, traits
- `tests/TestCase.php`: base setup and helpers
- `.env.example` and `config/*.php`: test behavior dependencies
- `.github/workflows/*.yml`: CI assumptions that local changes must respect
