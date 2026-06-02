# Intent Boundary Contract

## Layers

- `external_forward`: text intended to be sent to another Agent. Preserve user wording in `faithful_forward` mode.
- `local_execution`: tasks for the current assistant, including bracketed instructions by default.
- `context_only`: background information that informs the current interaction but should not be forwarded as an instruction.
- `memory_candidates`: possible durable memory items. They require explicit confirmation before any writeback.

## Boundary rules

1. Explicit markers override heuristics:
   - `【Agent转发】`
   - `【内部执行】`
   - `【当前助手执行】`
2. Parentheses `()` and `（）` default to `local_execution`.
3. Parentheses that explicitly contain `发给 Agent：` or equivalent enter `external_forward`.
4. Phrases like `帮我整理这段话发给 Agent：` are local wrapper instructions; they must not appear in `external_forward`.
5. Do not delete user-authored subjective words from forwarded text.
