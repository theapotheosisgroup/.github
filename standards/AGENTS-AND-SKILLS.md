# Agents, skills and coding agents

Conventions for TAG's AI agents, for installable skills, and for coding agents that work in TAG repositories.

## Agents

### Definitions

- Agent definitions and capability metadata live in **`tag-agents`**, under `agents/`, one directory per agent.
- A definition declares the agent's identity, its capabilities, the tools and MCP capabilities it may call, its model-provider requirements and its runtime policy. It never contains credentials.
- Agent handlers separate definition, application logic, execution interface, identity and caller attribution, transport, model-provider access, observability and runtime policy, so each can change on its own.
- Domain decisions stay in their domain repository. A generic agent asks the domain through its approved interface; it does not reimplement finance or governance rules.
- Inactive or incomplete components (for example an unfinished transport) are documented as such and never described as operational.

### Registry — **Proposed**

- The agent registry will be the **AGNTCY Agent Directory**, deployed from `tag-platform`. It is not deployed yet. Agent records are generated from the definitions in `tag-agents`; the registry is not a second source of truth.
- Registering an agent publishes metadata only. It grants no permission: every call an agent makes is still authorized by the owner of the resource.

### Agent plugin format and installer — **Proposed**

An **agent plugin 1.0** format, and an installer that installs plugins in that format, are to become the standard way to package and install an agent. **Neither exists yet.** The format is not specified here; [ADR 0003](../docs/adr/0003-agent-plugin-format.md) records the decision to define it and the questions the specification must answer. Until that ADR is accepted, do not build tooling that assumes a format.

### Identity

- Every agent acts under **its own attributable identity**. Shared, unverified caller labels must not be accepted as identity.
- An agent never uses a global administrator identity to read customer data. It acts with the delegated authority of the person or organization it serves ([IDENTITY-AND-AUTH](IDENTITY-AND-AUTH.md)).
- Existing agent identifiers (DIDs) are preserved with their audit history. Moving code never mints a replacement identifier.
- Agent execution interfaces are authenticated and are not exposed publicly.

## Skills

Skills live in **`tag-skills`** and follow the open [Agent Skills](https://agentskills.io/specification) format. They are installed with the [Vercel Skills CLI](https://github.com/vercel-labs/skills) (`npx skills`).

### Format

- One directory per skill under `skills/`, flat, named in lowercase kebab-case.
- Each skill has a `SKILL.md` whose YAML frontmatter has at least:
  - `name`: equal to the directory name; lowercase letters, digits and single hyphens, at most 64 characters;
  - `description`: what the skill does and when to use it, at most 1024 characters.
- Optional supporting directories: `references/`, `scripts/`, `assets/`.
- Check the current Agent Skills specification and Skills CLI documentation for optional fields and for where each agent client installs skills. Do not assume every client uses the same directory.

### Rules

- A skill is **self-contained**: everything it needs is inside its directory or declared as a pinned, reviewed dependency.
- A skill contains **no credentials** and **confers no permissions**. It refers to authoritative MCP capabilities, which enforce authorization.
- A skill never writes a ledger or other business record directly. It asks the owning domain through its tools.
- Scripts are executable, tested in CI and use only the dependencies they declare.
- Each skill documents which agent clients it supports. Installing a skill does not make it available in every hosted client.
- Versions and installation instructions are reproducible.

### CI for skills

`tag-skills` CI validates:

- `SKILL.md` frontmatter;
- discovery (`npx skills add . --list`);
- links and references;
- script tests;
- an installation smoke test in a disposable environment;
- that no secret is in any published file.

## Coding agents

These rules apply to Claude Code, Codex and any other coding agent working in a TAG repository.

- **`AGENTS.md`** in each repository root is the agent's entry point. It links to these standards and holds **only** repository-specific instructions and verified invariants: build and test commands, boundaries, things that must not change. It does not copy organization policy. Keep it short. `CLAUDE.md`, if present, imports `AGENTS.md` rather than duplicating it.
- Agents follow the same branch, pull request, testing and security rules as people ([REPOSITORIES](REPOSITORIES.md#branches-and-pull-requests)).
- Agents never commit secrets, never weaken or skip a check to get a green build, and never claim a test passed that they did not run.
- Agents open pull requests; people with the right to approve review and merge them. Agents do not merge, deploy to production, or change organization settings.
- An agent that finds a security problem reports it privately ([SECURITY.md](../SECURITY.md)) instead of describing it in a public place.
