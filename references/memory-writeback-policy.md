# Memory Writeback Policy

Memory candidates are not memory writes.

## Rules

1. Extract possible memory items only into `intent_layers.memory_candidates`.
2. Set `gate.memory_writeback_allowed = false` by default.
3. Set `gate.requires_user_confirmation = true` whenever memory candidates exist.
4. Do not write long-term memory without explicit user confirmation and a separate writeback action.
5. Treat long-term preferences, identity statements, operating constraints, and strategic directions as sensitive memory candidates.

## Candidate fields

When recording a candidate manually, include:

- source input
- candidate text
- memory type: preference | identity | constraint | strategy | project_context | other
- confirmation status: pending | approved | rejected
- timestamp
- regression link if the candidate came from a failure case
