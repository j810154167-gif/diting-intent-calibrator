# Session Handoff

## Current release state

Diting intent calibrator has been upgraded from a two-section intent formatter into a standard Skill prototype with structured intent package output, Runtime Gate fields, memory-candidate guardrails, and release-hardening tests. Product code: DitingOS. Positioning: 人类意图显性校准中枢.

## Core decisions

- Public version starts at `0.1.0-alpha` despite historical internal `v1.x` labels.
- `faithful_forward` is the default mode and must preserve user-authored subjective wording.
- `context_only` and `memory_candidates` must not pollute `external_forward`.
- `memory_candidates` are never long-term memory writes without explicit human confirmation.
- Handoff decisions must use `gate.handoff_allowed`, not natural-language interpretation.

## Current verification

Run:

```bash
python3 -m unittest discover -s tests
```

Expected result: all tests pass.

## Technical debt

- Parser is rule-based and should remain conservative.
- Density scoring is heuristic and needs calibration from real usage logs.
- Runtime Gate is local; external Agent handoff control is not yet integrated.
- Skill packaging tooling is not included in this repository.
- GitHub remote, release, topics, and Discussions require human authorization.

## Next agent priorities

1. Re-run tests before any release action.
2. Confirm git repository and remote configuration with the human.
3. Ask before commit, push, tag, or GitHub release creation.
4. Avoid adding unconfirmed memory entries.
5. Keep release docs aligned with `SKILL.md`, `src/calibrator.py`, and tests.

## Cognitive map

- `SKILL.md` is the trigger and progressive-disclosure entrypoint.
- `src/calibrator.py` is the truth source for runtime behavior.
- `tests/` is the regression truth source.
- `references/` holds policy explanations, not executable behavior.
- `memory/` contains templates and candidate logs, not confirmed durable memory.
- `prompts/human-lifecycle-prompts.md` contains the human-side full-cycle prompt architecture for start-of-use filing, periodic governance, and failure repair.
