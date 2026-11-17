# Code style, package management and dependencies

Consistent policies with technology-specific implementations. This standard does **not** impose one package manager or runtime version on every repository: an existing repository keeps its pinned tools unless a reviewed change moves them.

## General

- Formatting is automatic and checked in CI. Nobody argues about formatting in review.
- Linters and type checkers run in CI as blocking checks ([CI-CD](CI-CD.md)). A repository with known lint debt uses a documented, blocking ratchet; it does not disable the check.
- Code, identifiers, comments and documentation are in English.
- No dead code, commented-out code or speculative abstractions. Delete what is not used.
- Configuration comes from the environment or configuration files, never from hard-coded hosts, credentials or tenant identifiers.

## File and directory names

| Kind | Convention | Example |
| --- | --- | --- |
| Repositories | lowercase kebab-case | `tag-connectors` |
| Directories (general) | lowercase kebab-case | `providers/azure-document-intelligence/` |
| Python packages and modules | snake_case (PEP 8) | `tag_connectors/providers/xero/` |
| TypeScript and JavaScript files | kebab-case, unless the framework requires otherwise (for example route segments) | `token-audience.ts` |
| Terraform files and identifiers | snake_case identifiers; files named by concern (`main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`) | `resource "x" "service_ingress"` |
| Skills | lowercase kebab-case, equal to the skill `name` | `skills/finance-month-end/` |
| ADRs | `NNNN-kebab-title.md` | `docs/adr/0003-agent-plugin-format.md` |
| Standards documents | UPPERCASE kebab-case, as in this directory | `CODE-STYLE.md` |

## Languages

### Python

- **Package management: `uv`.** Projects declare dependencies in `pyproject.toml` and commit `uv.lock`. CI installs with `uv sync --frozen` and checks the lock is current with `uv lock --check`.
- Pin the interpreter with `.python-version` and `requires-python`. Pin uv with `[tool.uv] required-version` where reproducibility matters.
- Images install from the lockfile too (`uv sync --frozen --no-dev`), never `pip install .` against unpinned ranges.
- **Formatting and lint:** Ruff (`ruff format`, `ruff check`). A repository with an existing linter keeps it until a reviewed change replaces it.
- **Types:** Pyright, or the repository's existing type checker. New code is fully annotated.
- **Tests:** pytest. Mark contract tests with `@pytest.mark.contract` and register markers with `--strict-markers`.
- **Boundaries:** import-linter contracts ([ARCHITECTURE](ARCHITECTURE.md#module-boundaries)).

### TypeScript and JavaScript

- **Package management: the repository's pinned manager.** Each repository keeps the manager it uses (npm or pnpm today), pinned through the `packageManager` field in `package.json` and its committed lockfile. Do not switch managers, and never commit two lockfiles.
- CI installs with the locked command: `npm ci` or `pnpm install --frozen-lockfile`.
- Pin the Node.js version in `.nvmrc` (or the `engines` field) and keep it in step with the container base image.
- **Formatting:** Prettier, or the repository's existing formatter, behind a `format:check` script.
- **Lint:** ESLint (flat config) behind a `lint` script.
- **Types:** `strict` TypeScript, checked by a `typecheck` script (`tsc --noEmit`).
- **Scripts expected by the shared workflow:** `format:check`, `lint`, `typecheck`, `test`, `test:contract`, `build`. A repository that lacks one turns it off explicitly in its caller ([CI-CD](CI-CD.md#shared-workflows)).

### Terraform and OpenTofu

- `fmt` formatting and TFLint, both blocking. The rules are in [TERRAFORM](TERRAFORM.md).

### Shell

- `#!/usr/bin/env bash` with `set -euo pipefail`. Quote every expansion. ShellCheck clean.
- Prefer a short script in a real language over long inline shell in workflow files.

### GitHub Actions workflows

- actionlint and zizmor clean. The rules for permissions, pinning and inputs are in [CI-CD](CI-CD.md).

### Markdown

- markdownlint clean, with the repository's configuration. Relative links must resolve; CI checks them.

## Dependencies

- **Lock everything.** Every repository commits the lockfile for each package manager it uses, and CI installs only from it.
- **Upgrades arrive as pull requests** from Dependabot or Renovate, grouped where that reduces noise. Major upgrades are reviewed one at a time.
- **Wait before adopting.** Automated updates use a cooldown of at least 7 days after a release is published, except for security fixes.
- **No floating references:** no unpinned git dependencies, `latest` tags, or install scripts piped from the network without a checksum.
- **Licenses** must be on the allowlist in [SECURITY](SECURITY.md#supply-chain); exceptions are recorded per package with a reason.
- **Vulnerable dependencies** are handled under [SECURITY](SECURITY.md#vulnerability-handling).
- **Remove unused dependencies** in the pull request that stops using them.
