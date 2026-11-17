# CI/CD

Every repository has blocking CI built on the shared workflows in this repository, and every deployment is traceable to an immutable artifact.

## Rules

- **CI is blocking.** Every new repository has required checks that must pass before merge. No essential step uses `continue-on-error`.
- **Least privilege.** Workflows declare `permissions: {}` at the top level and grant each job only what it needs, usually `contents: read`. Write permissions (`packages: write`, `id-token: write`, `attestations: write`, `pull-requests: write`) are granted only to the job that uses them.
- **Pin everything third-party.** Actions are pinned to a full 40-character commit SHA with the version as a trailing comment (`uses: actions/checkout@<sha> # v7.0.1`). Downloaded tools are pinned to a version and verified against a SHA-256 checksum committed in the workflow. No `latest`.
- **No secrets in workflows or artifacts.** Secrets come from GitHub environments or repository secrets and are referenced by name. Never echo them, write them to files that get uploaded, or pass them as build arguments.
- **Short-lived cloud credentials.** Use OpenID Connect federation instead of long-lived cloud keys wherever the provider supports it.
- **Untrusted input stays data.** Pass `${{ }}` expressions to scripts through `env:`, never inline in `run:`. Do not use `pull_request_target` or `workflow_run` to run code from a pull request.
- **Check out without persisting credentials** (`persist-credentials: false`) unless a later step must push.
- **Every job has a timeout**, and pull request runs cancel superseded runs with `concurrency`.
- **Lint the workflows.** actionlint and zizmor run as blocking checks in this repository, and repositories with many workflows should run them too.
- **Existing repositories** may keep a documented, blocking quality ratchet for known debt ([TESTING](TESTING.md#rules)). Before changing a repository's CI triggers, check whether merges already deploy somewhere, and never change an existing auto-deployment rule as a side effect.

## Minimum checks

| Kind | Checks |
| --- | --- |
| All repositories | Install from lockfile, format, lint, type check where applicable, unit tests, contract tests, secret scanning, dependency vulnerability scanning, license policy, container build where applicable |
| Python | `uv sync --frozen`, Ruff (or the existing linter), Pyright (or the existing type checker), pytest, import-boundary tests |
| TypeScript | Locked install, ESLint, `tsc` type check, unit tests, production build, route and API contract tests |
| MCP | [MCP-STANDARDS](MCP-STANDARDS.md#testing) |
| Skills | [AGENTS-AND-SKILLS](AGENTS-AND-SKILLS.md#ci-for-skills) |
| Terraform | `fmt -check`, `init -backend=false`, `validate`, TFLint, infrastructure policy scan; plans only in authorized environments ([TERRAFORM](TERRAFORM.md#ci)) |

## Shared workflows

Reusable workflows live in [`.github/workflows/`](../.github/workflows/) of this repository. GitHub requires reusable workflows to sit directly in `.github/workflows/` (no subdirectories), and callers reference them by repository path and ref:

```yaml
jobs:
  python:
    permissions:
      contents: read
    uses: theapotheosisgroup/.github/.github/workflows/reusable-python-ci.yml@<40-character-sha> # v1.0.0
    with:
      working-directory: .
```

| Workflow | Job | Main inputs (all optional) | Caller grants |
| --- | --- | --- | --- |
| `reusable-node-ci.yml` | `node` | `working-directory`, `package-manager` (`npm`/`pnpm`, else detected from the lockfile), `node-version` or `node-version-file`, and one input per script: `format-script`, `lint-script`, `typecheck-script`, `test-script`, `contract-test-script`, `build-script` | `contents: read` |
| `reusable-python-ci.yml` | `python` | `working-directory`, `python-version`, `uv-version`, and one input per command: `format-command`, `lint-command`, `typecheck-command`, `boundary-command`, `test-command`, `contract-test-command` | `contents: read` |
| `reusable-container-ci.yml` | `container` | `context`, `dockerfile`, `target`, `build-args`, `platform`, `hadolint`, `scan-severity`, `ignore-unfixed`, `sbom-artifact` | `contents: read` |
| `reusable-terraform-ci.yml` | `terraform` | `tool` (`tofu`/`terraform`), `tool-version`, `directories` (one per line), `tflint-version`, `tflint-config`, `scan-severity` | `contents: read` |
| `reusable-security.yml` | `secrets`, `dependencies`, `dependency-review` | `gitleaks-config`, `require-lockfiles`, `license-allowlist`, `dependency-review`, `dependency-review-fail-on-severity` | `contents: read` |

- Every check has a conventional default and runs unless the caller turns it off by passing an empty string. The job summary lists each check as run or **skipped by caller**, so an opt-out is visible.
- The workflows never push, publish, deploy or read cloud credentials.
- `dependency-review` is off by default because GitHub provides it on public repositories, and on private repositories only with GitHub Code Security or GitHub Advanced Security. Vulnerability and license checks run for every repository through OSV-Scanner in the `dependencies` job.
- The workflow headers document every input. [`self-test.yml`](../.github/workflows/self-test.yml) calls each workflow against the fixtures in [`tests/fixtures/`](../tests/fixtures/README.md) on every pull request, so a change that breaks a workflow cannot merge.
- [Workflow templates](../workflow-templates/) give new repositories a starting caller for each workflow (**Actions → New workflow**, under the organization's templates).

### Pinning the shared workflows

- Callers pin a shared workflow to the **full commit SHA of a release tag** of this repository, with the tag as a trailing comment. Dependabot's `github-actions` ecosystem updates these pins.
- The workflow templates reference `@main` only as a placeholder, because they ship before the first release. Replace it with a release SHA when you adopt a template.
- Release rules for this repository are in [RELEASES](RELEASES.md#releasing-this-repository).

### Calling from private repositories

This repository is **public**, so private repositories in the organization can call its reusable workflows and use its templates without any per-repository access setting. GitHub's documented conditions are that the called workflow is in a public repository, the organization allows public reusable workflows, and the caller's Actions policy allows the actions the workflow uses. The organization's Actions settings must therefore allow it; see the [administrator steps](#administrator-steps).

## Required checks

- **Names are stable.** A reusable workflow's check appears as `<caller job> / <called job>`, for example `python / python`. Never rename a job that a ruleset requires, and never rename or remove a required check without first updating the ruleset.
- Existing repositories keep their current required check names until their rulesets are deliberately migrated.
- Required checks for this repository:

  | Workflow | Check names |
  | --- | --- |
  | `ci` | `actionlint`, `zizmor`, `workflow-templates`, `markdown`, `links`, `codeowners`, `security / secrets`, `security / dependencies`, `security / dependency-review` |
  | `self-test` | `node-npm / node`, `node-pnpm / node`, `python / python`, `container / container`, `terraform-tofu / terraform`, `terraform-terraform / terraform` |

## Container images

Status: build validation, scanning and SBOM generation are implemented (`reusable-container-ci.yml`). A shared **publish** workflow is **Proposed**: it will be added with the first repository that publishes images, because it cannot be exercised here without publishing artifacts.

- Images are published to **GitHub Container Registry** (`ghcr.io/theapotheosisgroup/<image>`) and deployed **by digest**, never by mutable tag.
- Tags are the semantic version and the commit SHA. `latest` is never used for deployment.
- Each published image has an SBOM and build provenance attested to its digest, and is scanned after publication.
- Base images are pinned by digest and updated through dependency pull requests. Containers run as a non-root user.
- Publishing happens from the default branch or a release tag, in a job that alone holds `packages: write`.

## Deployment

- Deployments use GitHub environments. Production requires explicit approval by a person in the environment's required reviewers, and nothing deploys to production automatically.
- Every deployment records the artifact digest and the deployment revision.
- The release sequence and rollback rules are in [RELEASES](RELEASES.md).

## Administrator steps

These steps need organization or repository administrator rights. Nothing in this repository changes organization settings.

### 1. Allow the organization's repositories to use the shared workflows

Calling a reusable workflow stored in this **public** repository needs no per-repository access setting (that setting exists only for private and internal repositories). It needs the organization's Actions policy to allow it.

Observed on 2026-11-17 through the REST API: this repository reports `allowed_actions: all` and `sha_pinning_required: false`. The organization-level policy could not be read without organization-administrator rights, so confirm it:

1. Open **Organization settings → Actions → General**.
2. Under **Policies**, check that Actions is enabled for all repositories (or at least the repositories that will call these workflows).
3. Check the actions policy:
   - **Allow all actions and reusable workflows**: nothing more to do.
   - **Allow theapotheosisgroup actions and reusable workflows** (organization only): this blocks `actions/checkout` and every other action the workflows use. Change to one of the other options.
   - **Allow theapotheosisgroup, and select non-theapotheosisgroup, actions and reusable workflows**: tick **Allow actions created by GitHub**, and add these entries to the allowlist:

     ```text
     astral-sh/setup-uv@*,
     pnpm/action-setup@*,
     docker/setup-buildx-action@*,
     docker/build-push-action@*,
     hashicorp/setup-terraform@*,
     opentofu/setup-opentofu@*,
     terraform-linters/setup-tflint@*,
     zizmorcore/zizmor-action@*,
     DavidAnson/markdownlint-cli2-action@*,
     lycheeverse/lychee-action@*
     ```

4. **Require actions to be pinned to a full-length commit SHA** may be turned on: every action here is SHA-pinned, and GitHub still allows reusable workflows to be referenced by tag.
5. Proof: the first CI run in a private repository that calls one of these workflows succeeds. If the policy blocks it, the run fails at startup with a message naming the blocked action or workflow.

### 2. Default workflow permissions

In **Organization settings → Actions → General → Workflow permissions**, select **Read repository contents and packages permissions**, and leave **Allow GitHub Actions to create and approve pull requests** unticked. Workflows request anything more per job.

### 3. Protect `main` in this repository

In **Repository settings → Rules → Rulesets → New branch ruleset**:

1. Name `main`, enforcement **Active**, target **Default branch**.
2. Tick **Restrict deletions** and **Block force pushes**.
3. Tick **Require a pull request before merging** with 1 required approval, **Require review from Code Owners**, **Require approval of the most recent reviewable push**, **Dismiss stale pull request approvals when new commits are pushed**, **Require conversation resolution before merging**, and allowed merge method **Squash**.
4. Tick **Require status checks to pass** and **Require branches to be up to date before merging**, and add every check listed under [Required checks](#required-checks) for this repository.
5. Tick **Require linear history**.
6. Leave the bypass list empty, or limit it to organization owners for emergencies.

### 4. Protect release tags in this repository

New tag ruleset: name `releases`, enforcement **Active**, target pattern `v*`, tick **Restrict updates**, **Restrict deletions** and **Block force pushes**. Release tags then stay immutable, which the callers' SHA pins rely on.

### 5. Private vulnerability reporting and the security contact

In **Repository settings → Security → Private vulnerability reporting**, select **Enable**, and set the role address in [SECURITY.md](../SECURITY.md).

### 6. Code owner teams

When the organization creates teams, replace the individual owners in [CODEOWNERS](../CODEOWNERS) with a team that has write access to this repository.
