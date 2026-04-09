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
          php-version: "8.3"
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
          php-version: "8.3"
          coverage: none
      - uses: ramsey/composer-install@v3
        with:
          composer-options: --no-interaction --prefer-dist
      - run: ./vendor/bin/phpunit
```

Swap the final command for `./vendor/bin/pest` when the project is Pest-first.

## Pest v4 Browser Testing Template

When the project uses `pestphp/pest-plugin-browser`, add Playwright setup to CI:

```yaml
name: Browser Tests

on:
  pull_request:
  workflow_dispatch:

jobs:
  browser-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: "8.3"
          extensions: mbstring, sqlite3
          coverage: none
      - uses: ramsey/composer-install@v3
        with:
          composer-options: --no-interaction --prefer-dist
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
      - run: npm install playwright@latest
      - run: npx playwright install --with-deps chromium
      - run: php -r "file_exists('.env') || copy('.env.example', '.env');"
      - run: php artisan key:generate
      - run: php artisan migrate --force
        env:
          APP_ENV: testing
          DB_CONNECTION: sqlite
          DB_DATABASE: database/database.sqlite
      - run: ./vendor/bin/pest --group=browser
        env:
          APP_ENV: testing
          DB_CONNECTION: sqlite
          DB_DATABASE: database/database.sqlite
```

Adapt the Laravel-specific steps (artisan, migrations) to the actual framework.

## Test Sharding Template (Pest v4)

Use a matrix strategy to split tests across multiple runners:

```yaml
name: Sharded Tests

on:
  pull_request:
  workflow_dispatch:

jobs:
  tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        shard: [1/4, 2/4, 3/4, 4/4]
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: "8.3"
          coverage: none
      - uses: ramsey/composer-install@v3
        with:
          composer-options: --no-interaction --prefer-dist
      - run: ./vendor/bin/pest --shard=${{ matrix.shard }}
```

Adjust the shard count based on suite size and available CI minutes.

## Optimization Levers

- Use `coverage: none` unless coverage is required.
- Cache Composer downloads and vendor installs when appropriate.
- Avoid service containers the suite does not need.
- Prefer SQLite for CI only if the app supports it faithfully enough.
- Split fast unit suites from slower integration suites when the repo is large enough to justify it.
- Use Pest v4 `--shard` with matrix strategy for horizontal CI scaling on large suites.
- Use `--parallel` within each shard for maximum throughput.

## Reliability Checks

- Match the CI command to the local project standard.
- Keep env values in sync with `phpunit.xml` and `.env.ci` or `.env.testing`.
- If the workflow changes database backend, run at least one realistic database-backed test locally when possible.
- Match the PHP version in CI to the project's minimum or target version. Check `composer.json` `require.php` constraint.
