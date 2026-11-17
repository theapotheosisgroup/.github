# Workflow fixtures

These directories exist only so that [`self-test.yml`](../../.github/workflows/self-test.yml) can call each reusable workflow on every pull request and prove it runs. They are **not application code** and are never built, published or deployed.

| Fixture | Exercised by | What it covers |
| --- | --- | --- |
| [`node-npm/`](node-npm/) | `reusable-node-ci.yml` | npm lockfile install, every script, `.nvmrc` |
| [`node-pnpm/`](node-pnpm/) | `reusable-node-ci.yml` | pnpm from the `packageManager` field, frozen lockfile, and an explicitly skipped check |
| [`python/`](python/) | `reusable-python-ci.yml` | `uv lock --check`, `uv sync --frozen`, Ruff, Pyright, an import-linter contract, pytest and a `contract`-marked test |
| [`container/`](container/) | `reusable-container-ci.yml` | hadolint, build without push, Trivy image scan, SBOM upload |
| [`terraform/`](terraform/) | `reusable-terraform-ci.yml` (OpenTofu and Terraform) | `fmt`, `init -backend=false`, `validate`, TFLint, Trivy policy scan; no provider and no resource |

The lockfiles here are also scanned by `reusable-security.yml` from [`ci.yml`](../../.github/workflows/ci.yml), which exercises the OSV-Scanner vulnerability and license checks. [`python/osv-scanner.toml`](python/osv-scanner.toml) shows how a per-package license exception is recorded.

Keep fixtures as small as possible. When a reusable workflow gains a code path, extend a fixture so the self-test covers it.
