# API and event contracts

Who owns a contract, how it is published, and how it changes without breaking consumers.

## Ownership

- **The owning service publishes its contract.** HTTP APIs are described in **OpenAPI 3.1**. Events, messages and other payloads are described in **JSON Schema (draft 2020-12)**. MCP tools publish their input and output schemas through the MCP protocol and keep them in the repository as JSON Schema.
- There is **no shared contracts repository** ([ADR 0002](../docs/adr/0002-no-shared-contracts-repository.md)). Consumers generate clients and types from the owner's published contract instead of hand-writing copies.
- Contracts live in the owning repository under `contracts/` (`contracts/openapi.yaml`, `contracts/schemas/*.json`), are versioned with the code, and are published as part of each release.
- **Public and internal contracts:**
  - A **public contract** is anything consumed outside the owning repository: by another TAG repository, by `aletia` or TAG across the product boundary, by an MCP client, or by an external developer. It is versioned, compatibility-tested and changed only under the rules below.
  - An **internal contract** is used only inside its repository. It can change freely, and it must not be reachable from outside the service.
- `aletia` is a separate product. TAG depends only on its **published** APIs, and `aletia` depends on nothing inside TAG.

## Compatibility

- **Additive changes** are compatible: a new optional request field, a new response field, a new endpoint, a new event type, a new enum value *where consumers are documented to tolerate unknown values*.
- **Breaking changes** need a new major version: removing or renaming a field, endpoint or event; making an optional field required; changing a type, format, meaning, default or error behaviour; tightening validation.
- **HTTP versioning** is in the path (`/v1/`, `/v2/`). Both versions run side by side for the deprecation period.
- **Event versioning** is in the event type (`<domain>.<entity>.<action>.v1`). New event types should use the [CloudEvents 1.0](https://github.com/cloudevents/spec) envelope. Consumers must ignore fields they do not know.
- **Errors** use [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457) problem details.
- **Writes** that can be retried accept an idempotency key and return the original result on replay.
- **Existing published paths and shapes are preserved** when code moves between repositories, through compatibility routing if needed.

## Testing contracts

- The provider runs **contract tests** against its own published contract in CI: every documented route, status and schema is exercised and responses validate against it.
- Consumers test against the published contract (generated client or schema validation), not against a hand-written mock of their own.
- CI detects breaking changes to `contracts/` against the default branch and fails unless the change bumps the major version.

## Deprecation

1. Mark the element deprecated in the contract and announce it in the changelog.
2. Responses from deprecated HTTP endpoints carry the `Deprecation` header ([RFC 9745](https://www.rfc-editor.org/rfc/rfc9745)) and a `Sunset` header ([RFC 8594](https://www.rfc-editor.org/rfc/rfc8594)) with the removal date.
3. Keep the deprecated version working for **at least 90 days or two minor releases, whichever is longer**, and until known consumers have moved.
4. Remove it only in a major release.
