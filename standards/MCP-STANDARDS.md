# MCP standards

Rules for TAG's Model Context Protocol (MCP) servers: who owns which tools, how they are authorized, and how they are tested.

## Ownership

| MCP surface | Owner |
| --- | --- |
| Client-facing discovery, OAuth protected-resource metadata, client authentication and audience validation, routing, tool catalogue composition, tool exposure policy, request correlation | `tag-mcp` |
| TAG Back Office tools (Finance, People, Governance) | `tag-mcp`. This is a deliberate exception to [principle 7](ARCHITECTURE.md#principles): the tools move to `tag-mcp` and call `tag-backoffice` through its published API. |
| Accounting-provider tools | `tag-mcp` (**Proposed**; the split is settled when the connectors and MCP phases land). Provider credentials and provider calls stay in `tag-connectors`. |
| aletia tools | `aletia`. TAG reaches them as an external, published MCP server. |

Whatever server hosts a tool:

- **Business rules stay in their domain.** An MCP tool translates protocol and calls the domain's authorized operation. It never implements accounting rules, ledger-write semantics or authorization decisions of its own.
- **Never copy another domain's tool handlers.** Call the owner through a stable, authorized contract.
- **Do not deploy a facade that adds nothing.** If a unified server brings no measurable value over a domain's own endpoint, keep it to contracts, a tested routing prototype and documentation.

## Authorization

- Each MCP server is an OAuth 2.x **protected resource**. It publishes protected-resource metadata ([RFC 9728](https://www.rfc-editor.org/rfc/rfc9728)) and accepts only access tokens issued for its own audience ([IDENTITY-AND-AUTH](IDENTITY-AND-AUTH.md)).
- A token for one MCP audience must be rejected by every other.
- Each tool declares the scopes it needs. The server checks scope, then the owning domain checks authority over the specific resource, for example membership of the Nexus named in the call.
- A Nexus or organization identifier in a request is never proof of access.
- Delegation is explicit and scoped. Read-only analytical delegation can never execute a write.
- Write tools require confirmation where the domain requires it, accept an idempotency key, and record who acted, for whom and under which delegation.
- The tool list is an allowlist: a tool is exposed only when its exposure policy says so. Internal or administrative tools are never exposed to clients by default.

## Contracts

- Every tool has a JSON Schema for its input and output, committed in the repository and validated in tests ([API-CONTRACTS](API-CONTRACTS.md)).
- Tool names are stable, namespaced by domain, and versioned like any public contract. Renaming or removing a tool is a breaking change.
- Errors are returned as MCP tool errors with a stable error code and no internal details or secrets.

## Testing

MCP servers run these tests in CI ([TESTING](TESTING.md)):

- protocol initialization;
- tool discovery: the exposed list equals the allowlist, with no unintended tools;
- tool invocation for every exposed tool;
- input and output schema validation;
- OAuth audience and scope checks, including a token for another audience being rejected;
- cross-Nexus authorization: a caller cannot act on a Nexus they do not belong to;
- idempotency of writes;
- malformed requests, which fail cleanly without leaking internals.

## Observability

Every tool call is traced with the tool name, the caller's opaque subject, the acting agent where there is one, and the correlation ID ([OBSERVABILITY](OBSERVABILITY.md)). Tool arguments are logged only after removing secrets and personal data.
