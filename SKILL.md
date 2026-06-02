---
name: diting-intent-calibrator
description: >
  Diting intent calibrator 是 DitingOS 的人类意图显性校准中枢，用于将高密度人类输入分离为 Agent 转发文本、当前助手执行任务、背景上下文和记忆候选，并通过 Runtime Gate 输出显式 handoff 决策。Use when user mentions "语义剪枝", "发给 Agent", "纯指令", "干净版", "内部/外部指令分离", "意图校准", or "转发给其他 Agent".
---

# Diting intent calibrator

Use this skill to separate mixed human instructions before forwarding content to another Agent.

## Workflow

1. Preserve `raw_input` exactly.
2. Choose mode:
   - `faithful_forward`: default; extract only, do not rewrite user wording.
   - `semantic_organize`: structure content without changing meaning.
   - `rewrite`: use only when the user explicitly asks to polish, compress, rewrite, or rephrase.
3. Produce a structured intent package with:
   - `external_forward`
   - `local_execution`
   - `context_only`
   - `memory_candidates`
   - `ambiguities`, `risk`, and `verification`
   - `gate.handoff_allowed`, `gate.local_execution_allowed`, `gate.memory_writeback_allowed`, `gate.requires_user_confirmation`, `gate.stop_reason`, `gate.next_action`
4. Enforce Runtime Gate before handoff: failed boundary checks and high leakage risk block forwarding.
5. Never remove user-authored subjective words such as “我认为 / 建议你 / 应该 / 可以” by default.
6. Do not write memory candidates to long-term memory without explicit user confirmation.

## Bundled resources

- Use [scripts/calibrator.py](scripts/calibrator.py) for deterministic parsing.
- Use [scripts/runtime_gate.py](scripts/runtime_gate.py) when explicit Runtime Gate evaluation is needed.
- Read [references/runtime-gate-policy.md](references/runtime-gate-policy.md) for handoff blocking rules.
- Read [references/memory-writeback-policy.md](references/memory-writeback-policy.md) before handling memory candidates.
- Read [references/human-anchor-policy.md](references/human-anchor-policy.md) when user confirmation or re-entry is needed.
- Read [references/intent-boundary-contract.md](references/intent-boundary-contract.md) when boundary ownership is unclear.
- Read [references/mode-policy.md](references/mode-policy.md) when deciding the processing mode.
- Read [references/usage-examples.md](references/usage-examples.md) for input/output examples.
- Read [references/fault-cases.md](references/fault-cases.md) for known failure patterns.
