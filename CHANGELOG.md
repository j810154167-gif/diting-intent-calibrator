# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and versioning follows [Semantic Versioning](https://semver.org/).

## [0.1.0-alpha] - 2026-06-02

### Added

- Standard Skill metadata in `SKILL.md` using `diting-intent-calibrator`.
- Structured intent package output with `raw_input`, `mode`, `intent_layers`, `ambiguities`, `risk`, and `verification`.
- Runtime Gate fields: `handoff_allowed`, `local_execution_allowed`, `memory_writeback_allowed`, `requires_user_confirmation`, `stop_reason`, and `next_action`.
- References for intent boundaries, Runtime Gate policy, memory writeback policy, human anchor policy, mode policy, examples, and fault cases.
- Memory template layer for feedback logs, failure cases, regression ledger, and human anchor re-entry prompts.
- Script entrypoints for parser and Runtime Gate demos.
- Human-side lifecycle prompt architecture in `prompts/human-lifecycle-prompts.md` for start-of-use filing, periodic governance, and failure repair.

### Changed

- Reworked the prototype from a two-section text formatter into a structured Runtime Gate Skill prototype.
- Preserved user-authored subjective wording in `faithful_forward` mode.
- Filtered `context_only` and `memory_candidates` from `external_forward` unless explicitly intended for forwarding.
- Strengthened tests from basic parser cases to release-hardening coverage.

### Fixed

- Prevented local execution instructions from leaking into Agent handoff.
- Prevented unconfirmed memory candidates from being treated as long-term memory writes.
- Added conflict detection for explicit labels and quoted parentheses.

## Historical prototype notes

Earlier prototype versions used `v1.x` labels internally. Public release resets the open-source version line to `0.1.0-alpha` because the project is now presented as a Skill prototype with test-backed Runtime Gate behavior.
