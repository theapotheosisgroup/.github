# Contributing

This guide applies to every repository in The Apotheosis Group that does not have its own `CONTRIBUTING.md`. A repository's own guide adds to it and documents any local exception. The rules themselves are defined once, in [`standards/`](standards/README.md); this page is the short version.

## Before you start

- Read the repository's `README.md`, `AGENTS.md` and `ARCHITECTURE.md`.
- For a non-trivial change, open or find an issue first. A change to a boundary, a contract or a standard needs an [ADR](standards/DOCUMENTATION.md#architecture-decision-records).
- Never commit secrets, credentials, real customer data or production identifiers. Use synthetic data in tests and examples ([`standards/SECURITY.md`](standards/SECURITY.md)).

## Branches and commits

- Branch from the repository's default branch. Name branches `<type>/<short-description>`, for example `feat/nexus-invite-api` or `fix/token-audience-check`.
- Keep a branch short-lived and focused on one change.
- Write commit subjects in the imperative mood. Pull request titles follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`, `ci:`), because the squashed commit takes the title.

Details: [`standards/REPOSITORIES.md`](standards/REPOSITORIES.md#branches-and-pull-requests).

## Pull requests

- Every change reaches the default branch through a pull request. Nobody pushes to it directly.
- Fill in the pull request template: what changed, why, how it was tested, and the rollback path.
- All required checks must pass. A check must not be made to pass by `continue-on-error`, by skipping tests or by lowering a baseline ([`standards/TESTING.md`](standards/TESTING.md)).
- A code owner approves before merge (`CODEOWNERS`).
- Update documentation in the same pull request as the behaviour it describes.
- Contract changes follow [`standards/API-CONTRACTS.md`](standards/API-CONTRACTS.md): additive changes are fine; breaking changes need a new version and a deprecation period.

## Local development

Each repository documents its own setup, test and build commands in its `README.md`. Use the package manager and runtime versions pinned in the repository: `uv` for Python, and the repository's pinned npm or pnpm for TypeScript ([`standards/CODE-STYLE.md`](standards/CODE-STYLE.md)).

## Coding agents

Coding agents follow the same rules as people, plus the conventions in [`standards/AGENTS-AND-SKILLS.md`](standards/AGENTS-AND-SKILLS.md#coding-agents). An agent opens pull requests; a person with the right to approve reviews and merges them.

## Reporting security issues

Do not open a public issue for a vulnerability. Follow [SECURITY.md](SECURITY.md).

## Contributing to this repository

- A change to a reusable workflow must keep [`self-test.yml`](.github/workflows/self-test.yml) green. Add or extend a fixture under [`tests/fixtures/`](tests/fixtures/README.md) when you add a code path.
- Pin every third-party action to a full commit SHA with its version as a trailing comment, and every downloaded tool to a version and SHA-256 checksum.
- This repository is public. Write standards as policy and interfaces. Host names other than the public product domains, internal URLs, network or deployment details, security findings, secret names and customer data do not belong here.
