# The Apotheosis Group

We build **TAG**, an agent-first back-office platform for organizations that provide services to each other. People work with TAG through its own workspace or through the personal AI agents they already use. TAG covers finance, people and governance work, with reusable agents and installable skills.

## How we build

- **One owner per domain.** Each repository owns one part of the platform and publishes its contracts as OpenAPI or JSON Schema.
- **Authorization where the data lives.** Every service checks authority for the resources it owns, and every agent acts under its own attributable identity.
- **Blocking tests and reproducible infrastructure.** Every repository has CI that must pass before a merge, and infrastructure is defined in code.
- **Open formats.** Skills follow the open Agent Skills format. Agents are reachable over the Model Context Protocol (MCP).

## Repositories

Most of our repositories are private. Our engineering standards, shared CI workflows and contribution guidelines are public in [`theapotheosisgroup/.github`](https://github.com/theapotheosisgroup/.github):

- [Organization structure and repository catalogue](https://github.com/theapotheosisgroup/.github#repository-catalogue)
- [Engineering standards](https://github.com/theapotheosisgroup/.github/tree/main/standards)
- [Contributing](https://github.com/theapotheosisgroup/.github/blob/main/CONTRIBUTING.md) and [security policy](https://github.com/theapotheosisgroup/.github/blob/main/SECURITY.md)
