## Summary

<!-- 1-3 sentences: what does this PR do and why. -->

## Related

- HELIOS master plan: <https://github.com/577Industries/helios-program/blob/main/plan/master-plan.md>
- Closes #
{REPO_LINKS}

## Quality

- [ ] Tests added or updated
- [ ] `ruff check .` and `ruff format --check .` pass
- [ ] `mypy --strict` passes (or `# type: ignore[...]` added with a justification)
- [ ] `pytest --cov` coverage threshold maintained
- [ ] CHANGELOG.md entry added under `[Unreleased]`
- [ ] Conventional-commit message in PR title (`feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`)
{REPO_CHECKS}

## Backwards compatibility

<!-- Any breaking changes to public API, JSON Schema, on-disk format, env vars? If yes, document the migration path. -->

## Provenance

- [ ] Any new data flow emits a `helios_provenance.HeliosModelOutputRecord` (or downstream equivalent) per the [provenance spec](https://github.com/577Industries/helios-provenance-spec).
