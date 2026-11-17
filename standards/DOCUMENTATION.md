# Documentation

What every repository documents, where it lives, and how decisions are recorded.

## Where documentation lives

| Kind | Location |
| --- | --- |
| Organization-wide standards and policy | This repository (`standards/`), public |
| Infrastructure implementation and deployment | `tag-platform` (`docs/`), private |
| Ecosystem architecture, catalogues, identity, security invariants, migration matrix | Private ([README](../README.md#where-the-other-documents-live)) |
| Everything about one repository | That repository, beside the code |

- Each standard has **one canonical source**. Repository documents link to it and record only local exceptions, with their reasons.
- Documentation changes ship in the same pull request as the behaviour they describe.
- Document **why** a boundary exists, not only which directory the code sits in.
- Use [Mermaid](https://mermaid.js.org/) diagrams where they make structure or flow clearer.

## Required documents

The files every application repository must have are listed in [REPOSITORIES](REPOSITORIES.md#required-contents). In addition:

- `ARCHITECTURE.md` describes the internal structure, the boundaries and any known violation of the dependency rules ([ARCHITECTURE](ARCHITECTURE.md#forbidden-dependencies)) with its migration plan.
- Code migrated from another repository has a `PROVENANCE.md` recording, for each moved module, the original repository, path and commit SHA, the new path, contract differences, tests migrated, consumers affected, compatibility strategy and cutover prerequisites.

## Status labels

Every document that describes components (services, modules, MCP servers, agents, workflows and other deployable or runnable parts) **must** say which state each one is in, using exactly these labels. Repositories are not components: they use the [repository status labels](#repository-status-labels) instead.

| Label | Meaning |
| --- | --- |
| **Currently deployed** | Running in at least one shared environment |
| **Implemented but not deployed** | Code exists and passes CI, but nothing runs it in a shared environment |
| **Migrated and locally tested** | Moved from a legacy repository and passing tests locally or in CI, not yet deployed from its new home |
| **Proposed but not implemented** | Designed or agreed, no working code yet |
| **Deprecated or legacy** | Still present, being replaced, receives only necessary fixes |
| **Blocked** | Cannot proceed until a named dependency or decision is resolved |

Never describe future architecture as operational. When the state changes, update the label in the same pull request.

### Repository status labels

A repository's lifecycle is recorded with exactly these labels, for example in the organization [repository catalogue](../README.md#repository-catalogue). The components inside a repository still carry their own component status labels.

| Label | Meaning |
| --- | --- |
| **Active** | Maintained and in use |
| **New** | Created in the foundation reorganization; scaffolding only, nothing migrated yet |
| **Legacy source** | Read-only migration source that still runs its existing deployments |
| **Not in scope** | Kept for reference, not part of TAG or the reorganization |

## Architecture decision records

- Important choices are recorded as ADRs in `docs/adr/`, named `NNNN-kebab-title.md` and numbered in sequence. Use the [template](../docs/adr/0000-template.md).
- An ADR is needed for: a new repository or service, a change to a boundary or ownership, a new public contract or a breaking change to one, a technology or vendor choice, a security or identity model decision, and any exception to a standard.
- ADR status is one of **Proposed**, **Accepted**, **Rejected**, **Deprecated** or **Superseded by NNNN**. Accepted ADRs are not rewritten; a later ADR supersedes them.
- Organization-wide decisions are recorded in this repository's [`docs/adr/`](../docs/adr/).
