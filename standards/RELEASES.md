# Releases, versioning and rollback

## Versioning

- Libraries, SDKs, published contracts, skills and the shared workflows in this repository use [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html): MAJOR for breaking changes, MINOR for compatible additions, PATCH for compatible fixes.
- Services are identified by their image digest. Their releases are also tagged with a semantic version and the commit SHA, and their public contracts follow the [compatibility rules](API-CONTRACTS.md#compatibility).
- Release tags are `vMAJOR.MINOR.PATCH` and are immutable once pushed.
- Each repository keeps a `CHANGELOG.md` in the [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format, or generates equivalent release notes from Conventional Commit titles.
- Deprecations follow [API-CONTRACTS](API-CONTRACTS.md#deprecation).

## Release sequence

1. A pull request is opened.
2. All required CI passes.
3. A code owner reviews and approves.
4. The pull request is merged into the approved integration branch.
5. A versioned container image (or other artifact) is built.
6. The image is published to GHCR and referenced by its immutable digest.
7. An SBOM and build provenance are produced for that digest.
8. The published artifact is scanned.
9. A deployment candidate is created.
10. The approved environment deployment runs; production needs explicit human approval.
11. Service health and contract compatibility are verified.
12. Post-deployment smoke tests run.
13. The artifact digest and deployment revision are recorded.
14. If verification fails, the service rolls back automatically or manually, as its documented policy says.

Before changing how a repository deploys, check whether merges already deploy somewhere today, and keep existing auto-deployment rules unless a reviewed change moves them.

## Rollback

- Every deployable repository documents its rollback procedure in its `README.md` or `docs/`, and tests it in a non-production environment.
- **Rollback means redeploying the previous recorded digest.** That is why every deployment records its digest.
- **Database changes are expand and contract.** Add first, migrate readers and writers, remove later, so the previous version keeps working against the new schema. Applied migrations are never edited or rewritten; a fix is a new migration.
- Append-only business records are never deleted or edited to roll back; corrections are new records.
- Infrastructure changes roll back through a reviewed change in `tag-platform`, never by editing state by hand ([TERRAFORM](TERRAFORM.md#approvals)).
- Every migration step between repositories is reversible until its cutover is explicitly approved.
- If a rollback is part of an incident, follow [incident response](SECURITY.md#incident-response).

## Releasing this repository

Other repositories depend on the reusable workflows here, so they are released like a library:

- A **breaking change** to a workflow (an input removed or renamed, a default that makes passing callers fail, a changed job name that callers may require) is a MAJOR release, announced in the changelog with migration notes.
- New inputs and checks that are off by default are MINOR. Fixes are PATCH. A new check that is on by default and can fail existing callers is treated as breaking.
- Releases are tagged `vX.Y.Z` on `main` after `self-test` passes. Callers pin the tag's commit SHA ([CI-CD](CI-CD.md#pinning-the-shared-workflows)).
- Release tags are protected against updates and deletion ([administrator step 4](CI-CD.md#4-protect-release-tags-in-this-repository)).
