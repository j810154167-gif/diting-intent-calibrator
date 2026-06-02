# GitHub Release Notes Draft

## v0.1.0-alpha

Initial public alpha for Diting intent calibrator, the DitingOS human explicit intent calibration hub.

### Highlights

- Standard Skill prototype with `SKILL.md`.
- Structured intent package output.
- Runtime Gate with explicit handoff fields.
- Memory-candidate writeback guardrails.
- Context and memory pollution prevention for `external_forward`.
- Release-hardening tests for metadata, script entrypoints, edge cases, and Runtime Gate behavior.

### Verification

```bash
python3 -m unittest discover -s tests
```

Expected result: all tests pass.

### Known limitations

- Rule-based parser.
- Local Runtime Gate only.
- No external Agent handoff controller yet.
- No durable memory store integration yet.
