# Security policy

This policy applies to every repository and service of The Apotheosis Group, unless a repository publishes its own `SECURITY.md`.

## Reporting a vulnerability

Please report suspected vulnerabilities privately. **Do not open a public issue, discussion or pull request.**

- **Contact:** `SECURITY-CONTACT-TO-BE-SET` — a role mailbox the organization owner will publish here. Until it is set, use GitHub's private vulnerability reporting on this repository if it is enabled (the **Security** tab, then **Report a vulnerability**), or contact an organization owner through GitHub.

Please include:

- what is affected (repository, service or URL on a public TAG domain) and its version or commit, if known;
- how to reproduce the issue, and what an attacker could do with it;
- whether you have shared the issue with anyone else.

Use only test accounts and data you own. Do not access, change or keep other people's data, do not degrade a service, and stop as soon as you have enough to show the problem.

## What happens next

| Step | Target |
| --- | --- |
| Acknowledge the report | 3 business days |
| Initial assessment and severity | 10 business days |
| Fix or mitigation for critical and high severity | As fast as possible; the internal targets are in [`standards/SECURITY.md`](standards/SECURITY.md#vulnerability-handling) |
| Tell the reporter the outcome | When the fix ships, or when we decide it is not a vulnerability |

We will credit you in the release notes if you wish. We do not take legal action against good-faith research that follows this policy.

## Supported versions

Only the latest release of each service and library receives security fixes, unless its own `SECURITY.md` says otherwise.

## Engineering rules

How TAG repositories handle secrets, dependencies, vulnerabilities and incidents is defined in [`standards/SECURITY.md`](standards/SECURITY.md).
