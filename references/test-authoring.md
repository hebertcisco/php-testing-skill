# Test Authoring

## Default Approach

- Mirror the repository's current style before introducing new abstractions.
- Cover behavior, not implementation trivia.
- Reproduce the regression first when fixing a bug.
- Mock external boundaries, not the subject under test.

## Unit Tests

Use unit tests for:

- helpers and utility functions
- services with mocked collaborators
- repositories when query construction can be isolated
- exceptions, resources, transformers, policies, and value objects

Prefer:

- factories or simple object builders over hand-written arrays when the repo already uses them
- data providers or Pest datasets for branch-heavy cases
- direct assertions on returned values, thrown exceptions, dispatched domain calls, and transformed output

## Feature Or Integration Tests

Use feature tests for:

- controllers and routes
- request validation and auth checks
- database-backed services
- console commands and jobs
- notifications, mail, events, and queues at framework boundaries

Prefer:

- framework test helpers instead of manual bootstrapping
- fake or mock layers that the repo already standardizes on
- assertions on status codes, JSON shape, database state, queued work, and side effects the feature actually owns

## Pragmatic E2E Tests

If no browser tool is installed, write E2E-style coverage as one of:

- a complete HTTP flow from request to persistence
- a command-to-database or command-to-file flow
- a job or queue orchestration flow
- a service flow that exercises real infrastructure inside the test harness

If a browser tool is already installed, extend that stack instead of inventing a second one.

## Repairing Existing Tests

1. Read the failing test and nearby passing tests.
2. Identify whether the break is caused by:
   - changed behavior
   - broken fixtures or factories
   - timing, async, or transaction assumptions
   - shared bootstrap side effects
3. Fix the least-coupled layer first.
4. Keep assertions tight and intention-revealing.
5. Avoid broad snapshot rewrites or expectation loosening unless the user asked for that tradeoff.

## Pest In PHPUnit Projects

When adding Pest to a PHPUnit project:

1. Add `pestphp/pest` and any framework plugin needed.
2. Create `tests/Pest.php`.
3. Keep existing PHPUnit tests intact.
4. Prefer creating new tests in Pest rather than mass-converting old files.
5. Convert old tests only when touching them for real behavior changes or when the user explicitly requests migration.

## Narrow Verification Commands

- `./vendor/bin/pest tests/Unit/FooTest.php`
- `./vendor/bin/pest --filter="foo"`
- `./vendor/bin/phpunit tests/Feature/BarTest.php`
- `php artisan test --filter=FooTest`

Run broader suites only after the targeted command passes.
