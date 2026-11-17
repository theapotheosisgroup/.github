# Terraform and infrastructure

How infrastructure code is owned, structured and validated. The infrastructure-specific extension of this standard, including state layout and deployment topology, lives privately in `tag-platform` (`docs/architecture/`).

## Ownership

- **`tag-platform` is the single source of truth for shared infrastructure.** Root modules, environment definitions, network topology, the authorization server's infrastructure, routing and TLS, observability infrastructure and the service deployment inventory live there.
- Application repositories **do not** contain root Terraform projects or copies of the platform's infrastructure. They publish a **service contract** that the platform applies (below).
- Never create a second state for resources that already exist in another state.
- Terraform and OpenTofu are both supported by the shared workflow. A repository pins one tool and its version; `tag-platform` uses OpenTofu.

## Service contract (application repositories)

Each deployable application repository documents, beside its code:

- its Dockerfile or other artifact build;
- required environment variables (names only, in `.env.example`) and secret references;
- health and readiness endpoints;
- resource requirements;
- network requirements, ports and protocols;
- dependency contracts (which APIs it calls);
- schema migration behaviour;
- its expected runtime identity;
- release and rollback steps.

## Structure

- Reusable modules live under `modules/`, one directory per module, each with `variables.tf`, `outputs.tf`, `versions.tf` and a `README.md` of its inputs and outputs.
- Environments live under `environments/<environment>/`, each a root module with its own state.
- Extract a module only when it meaningfully reduces duplication. Do not restructure an existing layout without an ADR.

## Requirements

- **State:** remote and encrypted, with locking or an equivalent serialization mechanism, and a separate state per environment. `.tfstate` files are never committed.
- **Pinning:** `required_version`, provider versions and module versions are pinned, and `.terraform.lock.hcl` is committed for root modules.
- **Secrets:** no credentials in variables, outputs, `tfvars` files or plans. Use secret references, not secret values.
- **Images:** services are referenced by immutable image digest.
- **Network:** least privilege. Services are internal-only by default, and every ingress rule is explicit.
- **Plans** are generated for review before any change, and the plan output is reviewable without exposing secrets.
- **Drift:** each environment has a documented drift detection strategy.
- **Imports:** resources that already exist are brought under management with a documented, reviewed import procedure, never by recreating them.
- **Disaster recovery** is documented for state and for each stateful service.

## Approvals

`apply`, `destroy`, state migrations and resource imports **never** run without separate, explicit approval by a person. CI may plan; it does not apply to production.

## CI

[`reusable-terraform-ci.yml`](../.github/workflows/reusable-terraform-ci.yml) runs on every pull request, for each listed module and root:

- `fmt -check -recursive`;
- `init -backend=false` (no state, no credentials);
- `validate`;
- TFLint, with the directory's `.tflint.hcl` or the configured file;
- a Trivy infrastructure policy scan that fails on high and critical misconfigurations.

Plan generation runs only in `tag-platform`'s own workflows, in authorized environments with federated, short-lived credentials ([CI-CD](CI-CD.md#rules)).
