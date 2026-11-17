# 0002. No shared contracts repository; each owner publishes its contracts

- **Status:** Accepted
- **Date:** 2026-11-17
- **Deciders:** mission lead

## Context

Several TAG services expose APIs and payloads consumed by other repositories and languages. A separate `tag-contracts` repository was considered, to hold shared, independently versioned cross-language contracts. The inventory found that each existing contract has exactly one owning service. What is missing is publication: the owners do not yet publish machine-readable contracts.

## Decision

Do not create `tag-contracts`. Each owning service publishes its contracts from its own repository: OpenAPI 3.1 for HTTP APIs and JSON Schema 2020-12 for events and payloads ([API-CONTRACTS](../../standards/API-CONTRACTS.md)). Consumers generate clients and types from the published contract.

## Consequences

- Contracts change in the same pull request as the implementation, and are tested by the owner's contract tests.
- Owners must add contract publication and breaking-change detection to their CI.
- Revisit only if two owners need one jointly versioned schema that cannot be generated from either owner's contract. A new ADR would supersede this one.

## Alternatives considered

- **Create `tag-contracts` now.** Moves interfaces away from their implementations without a proven need, and adds a release step to every contract change.
- **Decide later.** Leaves consumers hand-writing clients in the meantime.
