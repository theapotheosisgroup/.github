# 0003. Define an "agent plugin 1.0" format and installer

- **Status:** Proposed
- **Date:** 2026-11-17
- **Deciders:** mission lead (direction); specification pending

> This ADR records a direction, not a specification. No format, schema or installer exists yet, and nothing should be built against an assumed format until this ADR is accepted.

## Context

Agent definitions live in `tag-agents`, and the agent registry will be the AGNTCY Agent Directory, deployed from `tag-platform` (proposed, not yet deployed) ([AGENTS-AND-SKILLS](../../standards/AGENTS-AND-SKILLS.md#agents)). There is no standard way to package an agent so that it can be installed, registered and run the same way everywhere. The mission lead has set the direction that an "agent plugin 1.0" format and an installer for it become the standard.

## Decision (proposed)

Define a versioned **agent plugin** package format, starting at 1.0, and an installer that installs plugins in that format. Agent definitions in `tag-agents` will be published as agent plugins, and registry records will be generated from them.

## Questions the specification must answer

- **Contents:** the manifest fields (identity, version, capabilities, required tools and MCP capabilities, model-provider requirements, runtime policy), and which supporting files a plugin may carry.
- **Relationship to existing formats:** how a plugin maps to AGNTCY directory records, and how it relates to Agent Skills packages, so the two do not overlap.
- **Identity:** how a plugin references an agent's existing identifier without carrying keys, and how attribution is preserved across versions.
- **Permissions:** a plugin declares what it needs; it must not grant anything. Authorization stays with resource owners.
- **Installer:** what installing means (fetch, verify, register, configure), which targets it supports, how it verifies integrity and provenance, and how it uninstalls and upgrades.
- **Versioning and compatibility** of the format itself.
- **Validation:** a schema and a CI validator for plugins.

## Consequences

Until accepted, agent definitions stay as they are in `tag-agents`, and no tooling assumes a plugin format.

## Alternatives considered

To be completed with the specification.
