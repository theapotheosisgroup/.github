# Repositories

Naming, required contents, visibility, and the branch and pull request rules. The list of repositories is the [catalogue in the README](../README.md#repository-catalogue).

## Naming

- New repositories **must** use lowercase kebab-case: `tag-connectors`, `tag-skills`, `aletia`.
- TAG platform repositories use the `tag-` prefix. A standalone product, such as `aletia`, uses its own name.
- Existing repositories keep their names. A legacy repository is never renamed, archived or deleted as part of a reorganization, and its name is never reused while anything may still point at it.
- Before creating a repository whose name was once used and later renamed, an administrator confirms nothing still uses the old URL, because the new repository takes over GitHub's redirect.

## Visibility

- Repositories are **private by default**.
- A repository may be public when it is meant for end users or external developers, such as an SDK, a client library or a public specification. Each such decision is an ADR in that repository, and its `README.md` states the visibility.
- `.github` is public so that GitHub applies its community health defaults and the public organization profile ([ADR 0001](../docs/adr/0001-public-dot-github-repository.md)). Nothing internal goes in it.
- Before a private repository goes public, its full git history is scanned for secrets and internal details, not only its current tree.

## Required contents

Every application repository **must** have:

- `README.md`: responsibility, contract, status label ([DOCUMENTATION](DOCUMENTATION.md#status-labels)), local development commands, release and rollback summary;
- `AGENTS.md`: a short file that links to these standards and holds only repository-specific instructions and verified invariants ([AGENTS-AND-SKILLS](AGENTS-AND-SKILLS.md#coding-agents));
- `ARCHITECTURE.md`, `CONTRIBUTING.md`, `SECURITY.md` (may defer to the organization policy) and `CODEOWNERS`;
- `docs/` and `docs/adr/`;
- `tests/`;
- `.github/workflows/` with blocking CI ([CI-CD](CI-CD.md));
- `.env.example` where the service reads environment variables (names and safe examples only);
- a committed dependency lockfile for its language ([CODE-STYLE](CODE-STYLE.md#dependencies));
- documented release and rollback procedures ([RELEASES](RELEASES.md)).

A repository created ahead of its code holds an explicitly justified scaffold: its contract, documentation, CI for what exists, and a status of *Proposed but not implemented*. It must not contain placeholder application code written only to make CI pass.

`CODEOWNERS` is not inherited from `.github`; each repository keeps its own.

## Branches and pull requests

- **Default branch.** New repositories use `main`. Existing repositories keep their default branch, and its deployment behaviour, until a reviewed change moves it.
- **Feature branches** are short-lived and named `<type>/<short-description>`. Automated agents may use their own prefix, for example `xo/<task>`.
- **Every change goes through a pull request.** No direct pushes and no force-pushes to the default branch.
- **Merging requires:**
  - all required status checks passing;
  - approval from a code owner, and the most recent push approved by someone other than its author;
  - all review conversations resolved.
- **Merge method:** squash merge with a [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) title, so the default branch has a linear history. A repository may allow merge commits for long-running integration branches, documented in its `CONTRIBUTING.md`.
- **Protection** is configured with repository rulesets. When rulesets cannot be applied, an administrator applies them using the exact steps recorded with the change.
- **Required check names are stable.** Never rename or remove a required status check without first updating the ruleset that requires it ([CI-CD](CI-CD.md#required-checks)).
- Signed commits are recommended and may be required per repository.
- Coding agents open pull requests but never merge their own.
