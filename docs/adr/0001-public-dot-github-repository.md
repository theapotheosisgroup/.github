# 0001. Make the organization `.github` repository public

- **Status:** Accepted
- **Date:** 2026-11-17
- **Deciders:** mission lead

## Context

The organization needs one place for its engineering standards, reusable workflows, workflow templates and default community health files. GitHub applies default community health files (contributing guide, security policy, code of conduct, issue and pull request templates) only from a **public** `.github` repository, and shows a public organization profile only from `profile/README.md` in that repository. Workflow templates in a public `.github` repository are available to every repository in the organization, and reusable workflows in a public repository can be called by private repositories without a per-repository access setting.

The member-only profile stays in the separate, private `.github-private` repository.

## Decision

`theapotheosisgroup/.github` is public. Its README explains the organization structure and lists the public and private repositories with a visibility marker. It holds policy and interfaces only.

## Consequences

- Community health defaults, the public profile and the workflow templates work for every repository.
- Nothing internal may be committed: no internal host names or URLs, deployment topology, security findings, secret names or customer data. Documents that describe internal architecture, identity, security invariants or deployment live in private repositories.
- The organization's Actions policy must allow repositories to use public reusable workflows ([CI-CD administrator steps](../../standards/CI-CD.md#administrator-steps)).

## Alternatives considered

- **A private `.github` repository.** Its workflow templates would be available only to private repositories, and GitHub would not apply its community health files or show its profile.
- **Standards in `tag-platform`.** Mixes organization policy with infrastructure, and gives no community health defaults.
