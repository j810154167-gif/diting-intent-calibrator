# Mode Policy

## faithful_forward

Default mode. Extract boundaries only. Do not rewrite, summarize, polish, compress, or remove subjective wording.

## semantic_organize

Use when the user explicitly asks for structured organization, semantic organization, or clean separation. Preserve meaning and key wording.

## rewrite

Use only when the user explicitly asks for rewriting, polishing, compression, rephrasing, or tone changes.

## Confirmation gate

Set `requires_user_confirmation` to true when density is high, boundaries are ambiguous, or memory candidates are detected.
