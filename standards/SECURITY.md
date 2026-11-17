# Security engineering

Rules for secrets, supply chain, vulnerabilities and incidents. How to *report* a vulnerability is in the organization [security policy](../SECURITY.md).

## Secrets and credential custody

- **No secrets in source, images, build artifacts, logs, plans or test output.** Not in comments, fixtures, examples or git history either. `.env.example` holds names and safe example values only.
- **Each service has its own credentials.** A secret is never shared across a fleet of services so that any holder can act as any of them. Where a shared secret exists today, it is replaced by per-service credentials as that service migrates.
- **Least privilege and short lifetimes.** Credentials carry only the scopes their holder needs and expire as soon as practical. Long-lived cloud keys in CI are replaced by federated, short-lived credentials ([CI-CD](CI-CD.md#rules)).
- **Custody by owner.** External provider credentials (OAuth tokens, API keys for vendors) are held only by `tag-connectors`, encrypted at rest with keys that no other domain uses. Holding a provider credential never authorizes access by itself ([IDENTITY-AND-AUTH](IDENTITY-AND-AUTH.md#provider-credentials)).
- **Secret references, not values.** Infrastructure and deployment definitions refer to secrets in a secret store; they never contain the value.
- **Rotation.** Every credential has a documented rotation procedure. A credential that may have been exposed, including in git history, is rotated, not just deleted from the file.
- **Production secrets** are never copied into development, preview or CI environments, and never moved without explicit approval.
- **Detection.** CI runs gitleaks over the full git history ([`reusable-security.yml`](../.github/workflows/reusable-security.yml)). Running gitleaks as a pre-commit hook is recommended.

## Supply chain

- Dependencies are locked and upgraded as described in [CODE-STYLE](CODE-STYLE.md#dependencies).
- GitHub Actions and downloaded tools are pinned to commit SHAs and checksums ([CI-CD](CI-CD.md#rules)).
- **License allowlist** for dependencies: `MIT`, `Apache-2.0`, `BSD-2-Clause`, `BSD-3-Clause`, `ISC`, `0BSD`, `MPL-2.0`, `PSF-2.0`, `Python-2.0`, `Unlicense`, `CC0-1.0`, `BlueOak-1.0.0`, `Zlib`. Anything else, including unknown licenses, needs a per-package exception in `osv-scanner.toml` beside the lockfile, with the verified license and the reason. Copyleft licenses (GPL, AGPL, LGPL) need an ADR.
- **Your own packages.** OSV-Scanner reports a repository's own unpublished workspace package as `UNKNOWN`. Record it with `license.ignore = true` and a reason, as the [Python fixture](../tests/fixtures/python/osv-scanner.toml) shows.
- Published images carry an SBOM and build provenance ([CI-CD](CI-CD.md#container-images)).

## Vulnerability handling

Known vulnerabilities in dependencies or images fail CI (OSV-Scanner for lockfiles, Trivy for images). Each finding is fixed by upgrading, or accepted temporarily with a documented exception that names an owner and an expiry date.

Targets for fixing vulnerabilities in deployed code, from the time they are known:

| Severity | Fix or mitigate within |
| --- | --- |
| Critical | 7 days, or immediately when actively exploited |
| High | 30 days |
| Medium | 90 days |
| Low | Next routine upgrade |

Security findings about TAG systems are tracked privately. They are never described in public issues, pull requests, commit messages or this repository.

## Incident response

1. **Detect and declare.** Anyone who suspects an incident tells an organization owner immediately, privately. An incident lead is named.
2. **Contain.** Stop the exposure first: revoke or rotate credentials, disable the affected route or feature, or roll back ([RELEASES](RELEASES.md#rollback)).
3. **Preserve evidence.** Keep logs, audit records and artifact digests. Do not rewrite history or delete records.
4. **Eradicate and recover.** Fix the cause through a reviewed change, verify, and restore service.
5. **Notify.** Tell affected organizations and people, and authorities where the law requires it, within the required time.
6. **Review.** Write a blameless post-incident review within 5 business days, with actions, owners and dates. Add a test that would have caught the issue.

## Data

- Tests, fixtures, examples and demos use synthetic data only.
- Personal data is not logged ([OBSERVABILITY](OBSERVABILITY.md#what-never-to-log)).
- Append-only business records are never edited or deleted to fix an incident; corrections are new records.
