# theapotheosisgroup/.github: agent notes

Organization profile, engineering standards ([`standards/`](standards/README.md)), reusable workflows and community defaults. Start with [README.md](README.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

## Invariants

- **This repository is public.** Write policy and interfaces only. Never add internal host names or URLs (only the public product domains), IP addresses, deployment topology, security findings, secret names, or customer or synthetic business data. Ecosystem architecture documents belong in private repositories.
- **Every reusable workflow is exercised by [`self-test.yml`](.github/workflows/self-test.yml)** against [`tests/fixtures/`](tests/fixtures/README.md). A new code path in a workflow needs fixture coverage. Fixtures are not application code; keep them tiny.
- **Pin everything:** third-party actions by full commit SHA with a `# vX.Y.Z` comment; downloaded CLIs by version plus SHA-256 checksum (verify the checksum yourself before committing it).
- **Required check names are listed in [`standards/CI-CD.md`](standards/CI-CD.md#required-checks).** Renaming a job changes a check name; update that table in the same change.
- GitHub layout rules: reusable workflows must sit directly in `.github/workflows/`; templates need a matching `.properties.json`; issue templates live in `.github/ISSUE_TEMPLATE/`.

## Local checks (mirror `ci.yml`)

- `actionlint` and `actionlint workflow-templates/*.yml` (needs `shellcheck` on PATH)
- `uvx zizmor@<version in ci.yml> .github/workflows workflow-templates`
- `npx markdownlint-cli2@0.24.0 '**/*.md' '#**/node_modules'`; `lychee --offline --include-fragments './**/*.md'`
- `python3 -m unittest discover -s .github/scripts/tests` and `python3 .github/scripts/check_workflow_templates.py workflow-templates`
- In a git worktree (where `.git` is a file), OSV-Scanner may find no lockfiles unless run with `--no-ignore`; CI checkouts are unaffected.

## Maintaining this file

Keep this file for knowledge useful to almost every future agent session in this project.
Do not repeat what the codebase already shows; point to the authoritative file or command instead.
Prefer rewriting or pruning existing entries over appending new ones.
When updating this file, preserve this bar for all agents and keep entries concise.
