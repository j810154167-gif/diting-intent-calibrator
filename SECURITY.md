# Security Policy

## Supported versions

This project is in `0.1.0-alpha`. Security fixes target the latest public version.

## Reporting a vulnerability

Please report security issues through a private channel before public disclosure.

If no dedicated security contact is configured yet, open a GitHub issue with minimal non-sensitive details and request a private reporting channel.

## Known risk areas

- Boundary leakage between `external_forward` and `local_execution`.
- Accidental forwarding of memory candidates.
- Treating unconfirmed memory candidates as durable memory.
- Over-trusting rule-based parsing for high-density multi-Agent input.

## Response expectations

- Acknowledge valid reports after maintainer review.
- Convert confirmed failures into `memory/failure-cases.md` and regression tests.
- Avoid publishing sensitive source input in public issues without user consent.
