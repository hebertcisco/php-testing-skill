# Framework Detection

## Goal

Detect the real test stack and version before editing tests or CI.

## Check Order

1. Inspect `composer.json` and `composer.lock`.
2. Determine the PHPUnit major version from `composer.lock` or `composer.json` constraints.
3. Inspect `phpunit.xml` or `phpunit.xml.dist`.
4. Inspect `tests/Pest.php`.
5. Inspect `tests/`, `app/`, `src/`, `config/`, and `.github/workflows/`.
6. Confirm the nearest existing test style around the files you will edit.

## PHPUnit Version Detection

Check `composer.lock` for the installed `phpunit/phpunit` version. The major version determines available APIs:

| PHPUnit | PHP Required | Key Differences |
|---------|-------------|-----------------|
| **13** | >= 8.4.1 | Sealed mocks, `withParameterSetsInOrder()`, new array assertions |
| **12** | >= 8.3 | Annotations removed -- attributes only. Mock API cleanup |
| **11** | >= 8.2 | Annotations deprecated. Mock methods deprecated |
| **10** | >= 8.1 | Event system replaces TestListener. `withConsecutive()` removed |
| **9** | >= 7.3 | Legacy. Annotations and old mock API still available |

**Critical rule:** PHPUnit 12+ projects must use PHP 8 attributes (`#[Test]`, `#[CoversClass()]`, `#[DataProvider()]`) instead of docblock annotations. Writing `@test` or `@covers` in a PHPUnit 12+ project will fail silently or error.

## Pest Version Detection

| Pest | PHPUnit Base | PHP Required | Key Additions |
|------|-------------|-------------|---------------|
| **v4** | PHPUnit 12 | >= 8.3 | Browser testing (Playwright), smoke testing, visual regression, test sharding, profanity checking |
| **v3** | PHPUnit 11 | >= 8.2 | Arch testing, type coverage, mutation testing |
| **v2** | PHPUnit 10 | >= 8.1 | Arch presets, parallel testing |

Check for `pestphp/pest-plugin-browser` in dependencies -- this indicates Pest v4 browser testing is available.

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
  - `pestphp/pest-plugin-browser` (Pest v4, uses Playwright)
  - `laravel/dusk`
  - `symfony/panther`
  - Playwright, Cypress, Codeception, Behat, or custom scripts in the repo
- If no browser tool exists, interpret E2E as full application-flow testing through the existing PHP test harness unless the user asks for a browser stack.
- For new Pest v4 projects, prefer `pest-plugin-browser` over Dusk unless Dusk is already established.

## Files Worth Reading Next

- `phpunit.xml*`: suites, bootstrap, env, source/include, coverage, extensions
- `tests/Pest.php`: shared hooks, global `uses()`, traits
- `tests/TestCase.php`: base setup and helpers
- `.env.example` and `config/*.php`: test behavior dependencies
- `.github/workflows/*.yml`: CI assumptions that local changes must respect
