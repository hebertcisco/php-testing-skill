# Test Authoring

## Default Approach

- Mirror the repository's current style before introducing new abstractions.
- Cover behavior, not implementation trivia.
- Reproduce the regression first when fixing a bug.
- Mock external boundaries, not the subject under test.
- Check the PHPUnit major version before writing test metadata or mock code.

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

## Browser Tests (Pest v4)

When `pestphp/pest-plugin-browser` is installed:

- Uses Playwright as the backend (Chrome, Firefox, Safari).
- Supports device simulation (mobile, tablet, custom viewports) and color scheme switching.
- Supports parallel browser test execution.

Key patterns:

```php
// Basic browser test
visit('/sign-in')
    ->assertSee('Sign In')
    ->type('email', 'user@example.com')
    ->press('Submit')
    ->assertPathIs('/dashboard');

// Smoke testing -- visit pages and assert no JS errors
visit(['/', '/about', '/contact'])->assertNoSmoke();

// Visual regression -- compare against baseline screenshots
visit(['/', '/about'])->assertScreenshotMatches();

// Device simulation
visit('/')->on()->mobile()->inDarkMode()
    ->assertSee('Mobile Menu');
```

Installation requires both the Composer plugin and Playwright:

```bash
composer require pestphp/pest-plugin-browser --dev
npm install playwright@latest
npx playwright install
```

Laravel integration supports `RefreshDatabase`, model factories, and faked events within browser tests.

## Pragmatic E2E Tests

If no browser tool is installed, write E2E-style coverage as one of:

- a complete HTTP flow from request to persistence
- a command-to-database or command-to-file flow
- a job or queue orchestration flow
- a service flow that exercises real infrastructure inside the test harness

If a browser tool is already installed, extend that stack instead of inventing a second one.

## PHPUnit Version-Specific Patterns

### Test Metadata (Annotations vs Attributes)

PHPUnit 12+ removed all docblock annotations. Use attributes exclusively:

```php
// PHPUnit 12+ (required)
#[Test]
#[CoversClass(UserService::class)]
#[DataProvider('userDataProvider')]
public function it_creates_a_user(): void { ... }

// PHPUnit 10-11 (attributes preferred, annotations still work)
/** @test @covers UserService @dataProvider userDataProvider */
public function it_creates_a_user(): void { ... }
```

### Mock API Changes

```php
// PHPUnit 13: sealed mocks -- unconfigured methods auto-reject
$mock = $this->createMock(Gateway::class);
$mock->method('charge')->willReturn(true);
$mock->seal(); // any other method call will fail

// PHPUnit 13: consecutive call replacement
$mock->expects($this->exactly(3))
    ->method('process')
    ->withParameterSetsInOrder([1], [2], [3])
    ->willReturnOnConsecutiveCalls('a', 'b', 'c');

// PHPUnit 12+: removed methods
// - getMockForAbstractClass() -> use createMock()
// - getMockForTrait() -> removed
// - createTestProxy() -> removed
// - configuring expectations on createStub() -> not allowed
```

### PHPUnit 10 withConsecutive() Removal

For PHPUnit 10-12 (before `withParameterSetsInOrder` exists):

```php
// Option 1: willReturnCallback with a counter
$call = 0;
$mock->method('process')
    ->willReturnCallback(function ($arg) use (&$call) {
        return match (++$call) {
            1 => ($this->assertSame('a', $arg) || true) ? 'x' : '',
            2 => ($this->assertSame('b', $arg) || true) ? 'y' : '',
        };
    });

// Option 2: separate expects() calls (when order doesn't matter)
```

## Repairing Existing Tests

1. Read the failing test and nearby passing tests.
2. Identify whether the break is caused by:
   - changed behavior
   - broken fixtures or factories
   - timing, async, or transaction assumptions
   - shared bootstrap side effects
   - PHPUnit version upgrade (annotations, removed mock methods, changed error handling)
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
6. Use `pestphp/pest-plugin-drift` for automated conversion of PHPUnit classes to Pest syntax when migrating at scale.

## Narrow Verification Commands

- `./vendor/bin/pest tests/Unit/FooTest.php`
- `./vendor/bin/pest --filter="foo"`
- `./vendor/bin/phpunit tests/Feature/BarTest.php`
- `php artisan test --filter=FooTest`

Run broader suites only after the targeted command passes.
