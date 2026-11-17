# Observability

Logging, tracing, metrics and correlation, so that any request can be followed across services without exposing secrets or personal data.

## Logging

- Services write **structured JSON logs** to standard output, one event per line.
- Every log event has: `timestamp` (UTC, RFC 3339), `level`, `service`, `version`, `environment`, `message`, and, when handling a request, `trace_id`, `span_id` and `correlation_id`.
- When known, add the acting `subject` (opaque identifier), the acting `agent`, and the `organization` or `nexus` identifier the request concerns.
- Levels: `error` needs attention, `warn` is unexpected but handled, `info` is a significant business or lifecycle event, `debug` is off in production by default.
- **Audit records are not logs.** Who did what to which business record belongs in the owning domain's audit trail, not only in application logs.

### What never to log

Secrets, tokens, authorization headers, cookies, passwords, private keys, full request or response bodies that may contain them, and personal data such as emails, phone numbers and names. Redact before logging, and test that redaction works.

## Tracing

- Services use **OpenTelemetry** SDKs and export over OTLP. The collector and backend are platform infrastructure ([TERRAFORM](TERRAFORM.md)).
- Trace context propagates with the **W3C Trace Context** headers (`traceparent`, `tracestate`) on every inbound and outbound HTTP call, and in message or event metadata.
- Spans cover inbound requests, outbound calls, database queries, queue operations, model-provider calls and MCP tool calls. Span attributes follow OpenTelemetry semantic conventions and obey the same "never log" rules.

## Correlation IDs

- Each inbound request has a correlation ID: taken from an incoming `X-Request-Id` header when the caller is trusted, otherwise generated.
- The ID is returned in the `X-Request-Id` response header, included in every log event, passed to downstream calls, and carried in events and background jobs started by the request.
- Error responses (RFC 9457 problem details) include the correlation ID so a user can quote it.

## Metrics and health

- Services expose request rate, error rate and duration for each endpoint and tool, plus saturation metrics for their resources.
- Every service exposes **liveness** and **readiness** endpoints as part of its service contract ([TERRAFORM](TERRAFORM.md#service-contract-application-repositories)). Readiness fails when a hard dependency is unavailable; liveness does not depend on other services.
- Alerts are defined on user-visible symptoms (errors, latency, failed jobs), each with a runbook link.
