# Testing

Every repository has meaningful tests, and they block merges.

## Rules

- **Tests are blocking.** A required check must not pass because an essential step uses `continue-on-error`, because tests were skipped, or because a baseline was quietly reset.
- **Ratchets, not resets.** An existing repository with known failures may run a documented, blocking quality ratchet: the number of failures may go down, never up. The baseline lives in the repository and changes only in a reviewed pull request that says why.
- **Test what exists.** Never add placeholder application code just to make CI green. A scaffold repository tests the files it has.
- **Synthetic data only.** Tests and fixtures use synthetic people and organizations, never real customer data or production identifiers.
- **Isolated infrastructure.** Integration and security tests run against local or disposable environments, never production.
- **Mock-only tests are not security validation.** A security property is validated only by a test that exercises the real authorization path.
- **Flaky tests** are fixed or quarantined within one working day. A quarantined test has an issue and an owner, still runs, and its result stays visible.
- **Report honestly.** Results are reported as PASS, FAIL or BLOCKED, with evidence: the commands run, exit codes and test counts. An unexecuted test is never reported as PASS.

## Test levels

| Level | What it proves | Where |
| --- | --- | --- |
| Unit | Logic in isolation | Every repository, every pull request |
| Contract | The service honours its published contract; consumers match it ([API-CONTRACTS](API-CONTRACTS.md#testing-contracts)) | Every repository with a public contract |
| Integration | Real adapters against real local dependencies (database, queue, provider sandbox) | Pull requests where practical, otherwise on merge |
| Security | The invariants below | Every repository that owns protected resources |
| End-to-end and smoke | A deployed environment works | After each deployment ([RELEASES](RELEASES.md)) |

The checks each language must run are in [CI-CD](CI-CD.md#minimum-checks).

## Minimum security coverage

Every repository that owns protected resources has automated tests showing that:

- one user cannot access another user's protected data;
- one organization cannot read another organization's data without authority;
- a Nexus or organization identifier cannot bypass membership checks;
- a provider credential cannot reach an unrelated provider tenant;
- a token for one audience is rejected by another;
- revoked membership or delegation fails the next protected call;
- an agent's identity is attributable and cannot be forged with a shared, unverified label;
- business writes keep confirmation, idempotency and authoritative attribution;
- no secret appears in source, build artifacts, logs, plans or test output;
- a service's privileged endpoints reject callers that are merely reachable on the network;
- conversations and tools stay isolated across people and organizations;
- read-only analytical delegation cannot execute a write.

The full catalogue, with the evidence required before any release recommendation, is maintained privately (`SECURITY_INVARIANTS.md`).

## MCP servers and skills

MCP servers and skills have their own required tests: [MCP-STANDARDS](MCP-STANDARDS.md#testing) and [AGENTS-AND-SKILLS](AGENTS-AND-SKILLS.md#ci-for-skills).

## Coverage

Repositories report line and branch coverage in CI. Coverage is a signal, not a target: a pull request that changes behaviour adds tests for it, and coverage of authorization and ledger code is reviewed explicitly.
