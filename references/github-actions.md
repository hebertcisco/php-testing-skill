# GitHub Actions

## Goal

Create or refine fast, dependable CI for PHP projects without assuming every repo is Laravel.

## Common Structure

1. Checkout code.
2. Set up PHP with required extensions.
3. Cache Composer dependencies.
4. Install dependencies with stable Composer flags.
5. Prepare env and writable directories.
6. Prepare database or services only if the suite needs them.
7. Run the narrow project-standard test command.
8. Upload useful logs or artifacts on failure.

## Laravel Template

Use this shape when the project has `artisan`, framework test helpers, and migrations:

```yaml
name: Laravel Tests

on:
  pull_request:
  workflow_dispatch:

jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: "8.2"
          extensions: mbstring, sqlite3
          coverage: none
      - uses: ramsey/composer-install@v3
        with:
          composer-options: --no-interaction --prefer-dist
      - run: php -r "file_exists('.env') || copy('.env.example', '.env');"
      - run: php artisan key:generate
      - run: mkdir -p database && touch database/database.sqlite
      - run: php artisan migrate --force
        env:
          APP_ENV: testing
          DB_CONNECTION: sqlite
          DB_DATABASE: database/database.sqlite
      - run: php artisan test --env=testing
        env:
          APP_ENV: testing
          DB_CONNECTION: sqlite
          DB_DATABASE: database/database.sqlite
```

## Symfony Or Plain PHP Template

Use this shape when the project is not Laravel:

```yaml
name: PHP Tests

on:
  pull_request:
  workflow_dispatch:

jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: "8.2"
          coverage: none
      - uses: ramsey/composer-install@v3
        with:
          composer-options: --no-interaction --prefer-dist
      - run: ./vendor/bin/phpunit
```

Swap the final command for `./vendor/bin/pest` when the project is Pest-first.

## Optimization Levers

- Use `coverage: none` unless coverage is required.
- Cache Composer downloads and vendor installs when appropriate.
- Avoid service containers the suite does not need.
- Prefer SQLite for CI only if the app supports it faithfully enough.
- Split fast unit suites from slower integration suites when the repo is large enough to justify it.

## Reliability Checks

- Match the CI command to the local project standard.
- Keep env values in sync with `phpunit.xml` and `.env.ci` or `.env.testing`.
- If the workflow changes database backend, run at least one realistic database-backed test locally when possible.
