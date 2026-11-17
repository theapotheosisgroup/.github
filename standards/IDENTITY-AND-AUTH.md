# Identity, authentication and delegated authorization

Policy and interfaces only. The identity and delegation design is documented privately (`IDENTITY_AND_DELEGATION.md`, see [README](../README.md#where-the-other-documents-live)).

## Authorization server

- **Ory Hydra** is TAG's OAuth 2.x and OpenID Connect authorization server. New services integrate with it rather than with another identity provider.
- Services do not issue their own long-lived bearer tokens to people or agents. Signed tokens for service-to-service calls are short-lived and verified against published keys.

## Subjects

- **Subjects are opaque.** The `sub` of a person, organization or agent is a stable, opaque identifier. It is never an email address, phone number, name or other personal data, and consumers must not parse meaning out of it.
- Tokens carry the minimum claims a resource server needs. Personal data is fetched from its owner when needed, under its own authorization.

## Access tokens

- Every token is issued **for a specific audience** (resource indicators, [RFC 8707](https://www.rfc-editor.org/rfc/rfc8707)) and every resource server rejects tokens for any other audience.
- Scopes are narrow and named by capability. Each endpoint or tool declares the scopes it needs.
- Access tokens are short-lived. Refresh tokens rotate, and revocation takes effect on the next protected call.
- Tokens are never logged, never put in URLs, and never forwarded to a service they were not issued for. A service that calls another on a user's behalf obtains a token for that audience (token exchange) instead of passing the caller's token along.

## Where authorization happens

- **Authorization is enforced where the protected resource is owned.** The owning service decides, on every request, whether this subject, acting in this capacity, may perform this action on this resource.
- Network reachability is not authorization: a service rejects calls to its privileged endpoints from any caller without valid credentials, wherever the call comes from.
- Frontends and gateways may check early for user experience, but the owner checks again.
- An identifier in a request (Nexus, organization, tenant) is never proof of access; membership and standing are checked against the owner's records.

## Delegation

Delegation keeps these concepts separate, and each must be checked on its own: person identity, organization membership, acting capacity, Nexus standing, data-source authorization, permission to combine information, report ownership, and permission to disclose a result ([ARCHITECTURE](ARCHITECTURE.md#cross-organization-analysis-future)).

- A delegation names who delegates, to whom (person or agent), which scopes, which resources, and until when.
- Read-only analytical delegation can never be used to write financial records or ledgers.
- Revoking membership or a delegation fails every later protected call that depended on it.
- Agents act with delegated authority and their own identity, never a global administrator identity ([AGENTS-AND-SKILLS](AGENTS-AND-SKILLS.md#identity)).

## Provider credentials

A connector may hold a provider credential (for example an accounting provider's OAuth token). That never grants access by itself: access to a particular organization's data is tied to independently verified business authority and tenant binding, checked by the owner of that authority. Custody rules are in [SECURITY](SECURITY.md#secrets-and-credential-custody).

## Decentralized identifiers (DIDs)

- **A DID follows its environment's domain.** Each environment publishes the identifiers it mints under its own identity domain, `id.<environment domain>`. Identifiers minted for one environment are not used in another.
- Existing identifiers keep resolving, unchanged, with their audit history. Moving code or infrastructure never re-mints an identifier; a new identifier is minted only for a genuinely new identity.
- Private keys for DIDs are held by the operator or a key service, never in a repository, image or log.

## Open decision

How identity assertions bridge between TAG and `aletia`, now that `aletia` is a standalone product, is not yet decided. It will be settled in an ADR before either side builds on it. Until then, neither side depends on the other's internal identity tables.
