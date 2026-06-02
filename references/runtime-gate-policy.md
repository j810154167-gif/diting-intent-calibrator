# Runtime Gate Policy

Runtime Gate protects Agent handoff before any external forwarding happens.

## Flow

`HumanInput -> IntentCalibration -> DensityGate -> BoundaryCheck -> AmbiguityGate -> HumanConfirmationGate -> HandoffAllowed / LocalExecutionAllowed / MemoryWritebackCandidate`

## Gate fields

- `handoff_allowed`: true only when boundary check passes, leakage risk is not high, and no confirmation is required for handoff.
- `local_execution_allowed`: true when local tasks are present and boundary check does not fail.
- `memory_writeback_allowed`: false by default; true only after explicit user confirmation outside this parser.
- `requires_user_confirmation`: true when density, ambiguity, leakage, or memory candidate gates require human review.
- `stop_reason`: machine-readable reason when handoff is blocked.
- `next_action`: one of `forward`, `execute_local`, `ask_user`, `split_input`, `stop`.

## Blocking rules

1. `boundary_check = fail` blocks handoff.
2. `ambiguity_level = high` requires user confirmation.
3. `leakage_risk = high` blocks handoff.
4. Density above threshold should route to `split_input` or `ask_user`.
5. Handoff permission must come from `gate.handoff_allowed`, not natural language output.
