## Summary

<!-- What changes, and why. Link the issue or ADR. -->

## How it was tested

<!-- Commands you ran and their results. Say what was not tested and why. -->

## Rollback

<!-- How to undo this change if it misbehaves after merge or deploy. -->

## Checklist

- [ ] Required checks pass, and no test or check was disabled, skipped or set to `continue-on-error` to get there.
- [ ] No secrets, credentials, real customer data or production identifiers are added (including in tests, fixtures and logs).
- [ ] Documentation and status labels are updated in this pull request.
- [ ] Published API, event or MCP contract changes are backward compatible, or versioned with a deprecation plan ([API-CONTRACTS](https://github.com/theapotheosisgroup/.github/blob/main/standards/API-CONTRACTS.md)).
- [ ] Authorization stays where the protected resource is owned ([IDENTITY-AND-AUTH](https://github.com/theapotheosisgroup/.github/blob/main/standards/IDENTITY-AND-AUTH.md)).
- [ ] Database migrations are additive; no applied migration is edited.
- [ ] An ADR is added or updated if this changes a boundary, a contract or a standard.
- [ ] This change does not deploy to production on merge, or the production approval path is described above.
