# PHPUnit Optimization

## Goal

Speed up feedback without breaking project assumptions.

## Safe Defaults

- Keep test environment variables inside `phpunit.xml` or `phpunit.xml.dist`.
- Prefer in-memory SQLite only when the app and migrations genuinely support it.
- Use fast drivers in test env:
  - cache: `array`
  - queue: `sync`
  - session: `array`
  - mail: `array` or `log`
  - logs: `null` or low-noise channel
- Lower bcrypt or hashing cost only in tests.
- Disable optional observability, debug, telescope, or third-party integrations in tests.

## Typical `phpunit.xml` Improvements

- Define explicit suites such as `Unit` and `Feature`.
- Scope `<source>` or coverage include paths to app code only.
- Add focused `<php>` env settings for speed.
- Avoid loading unnecessary bootstrap code or providers when the framework allows lighter test kernels.

## Laravel Notes

- Prefer `php artisan test` when the repo standardizes on it.
- Use `RefreshDatabase` only where isolation matters. For large suites, consider lighter database reset strategies already used by the project.
- Check for hidden slow paths in:
  - model observers
  - event listeners
  - queued jobs
  - external SDK bootstrapping
  - heavy seeders in base test case

## Parallelization

- Use parallel testing only after confirming the suite is isolation-safe.
- Check for collisions in:
  - static caches
  - shared files
  - singleton state
  - queue names
  - external ports or services

## Example Fast Test Env

```xml
<php>
    <env name="APP_ENV" value="testing"/>
    <env name="CACHE_DRIVER" value="array"/>
    <env name="QUEUE_CONNECTION" value="sync"/>
    <env name="SESSION_DRIVER" value="array"/>
    <env name="MAIL_MAILER" value="array"/>
    <env name="LOG_CHANNEL" value="null"/>
    <env name="BCRYPT_ROUNDS" value="4"/>
</php>
```

Use this as a direction, not a blind copy. Merge with the repository's actual required env values.

## Verification After Config Changes

- Run a narrow suite first.
- Run at least one database-backed test if database config changed.
- Run CI-equivalent commands when changing `phpunit.xml` or workflow files.
