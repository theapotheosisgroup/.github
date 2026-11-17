# Engineering standards

These files are the single canonical source for TAG's organization-wide engineering rules. Repository documentation links here and records only local exceptions, each with its reason.

**Status of this set:** adopted for every new TAG repository from phase R01. Existing repositories align through separate, reviewed pull requests; until then they keep their current behaviour and required check names. Rules that are not yet implemented anywhere are marked **Proposed** where they appear.

The words **must**, **must not**, **should** and **may** are used as in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

## The 20 required conventions

| # | Convention | Defined in |
| --- | --- | --- |
| 1 | Repository naming: lowercase kebab-case for new repositories | [REPOSITORIES](REPOSITORIES.md#naming) |
| 2 | Directory naming and module boundaries | [ARCHITECTURE](ARCHITECTURE.md#module-boundaries), [CODE-STYLE](CODE-STYLE.md#file-and-directory-names) |
| 3 | Public versus internal contract ownership | [API-CONTRACTS](API-CONTRACTS.md#ownership) |
| 4 | API and event schema compatibility | [API-CONTRACTS](API-CONTRACTS.md#compatibility) |
| 5 | Semantic versioning and deprecation | [RELEASES](RELEASES.md#versioning), [API-CONTRACTS](API-CONTRACTS.md#deprecation) |
| 6 | Coding style by language | [CODE-STYLE](CODE-STYLE.md#languages) |
| 7 | Python package management with `uv` | [CODE-STYLE](CODE-STYLE.md#python) |
| 8 | TypeScript package management with the repository's pinned manager | [CODE-STYLE](CODE-STYLE.md#typescript-and-javascript) |
| 9 | Dependency locking and upgrades | [CODE-STYLE](CODE-STYLE.md#dependencies) |
| 10 | Authentication and delegated authorization | [IDENTITY-AND-AUTH](IDENTITY-AND-AUTH.md) |
| 11 | Secrets and credential custody | [SECURITY](SECURITY.md#secrets-and-credential-custody) |
| 12 | Testing and minimum security coverage | [TESTING](TESTING.md) |
| 13 | CI/CD rules | [CI-CD](CI-CD.md) |
| 14 | Terraform module and state ownership | [TERRAFORM](TERRAFORM.md) |
| 15 | Container image publishing | [CI-CD](CI-CD.md#container-images) |
| 16 | Git branch and pull request policies | [REPOSITORIES](REPOSITORIES.md#branches-and-pull-requests) |
| 17 | Documentation and ADR requirements | [DOCUMENTATION](DOCUMENTATION.md) |
| 18 | Logging, tracing and correlation IDs | [OBSERVABILITY](OBSERVABILITY.md) |
| 19 | Incident response and rollback | [SECURITY](SECURITY.md#incident-response), [RELEASES](RELEASES.md#rollback) |
| 20 | Skills and coding-agent conventions | [AGENTS-AND-SKILLS](AGENTS-AND-SKILLS.md) |

## Changing a standard

Open a [standards change issue](https://github.com/theapotheosisgroup/.github/issues/new?template=standards_change.yml), then a pull request. A change that alters a boundary or a technology choice also needs an ADR in [`docs/adr/`](../docs/adr/). Say in the pull request which repositories must change and whether they can adopt the change incrementally.
