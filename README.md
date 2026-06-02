# Diting intent calibrator

A standard Skill prototype and Runtime Gate for separating dense human input before Agent handoff.

## Status

- Release candidate: `v0.1.0-alpha`
- Product code: DitingOS
- Positioning: 人类意图显性校准中枢
- Long-term direction: 人机协同时代人类弥散脑缺陷-机器线性脑缺陷的意图校准系统
- Test status: `python3 -m unittest discover -s tests`
- Current scope: local deterministic parser, structured intent package, Runtime Gate, memory-candidate guardrails

## What it does

Diting intent calibrator converts high-density human input into a structured intent package:

```python
{
    "raw_input": "...",
    "mode": "faithful_forward | semantic_organize | rewrite",
    "intent_layers": {
        "external_forward": "...",
        "local_execution": [],
        "context_only": [],
        "memory_candidates": []
    },
    "ambiguities": [],
    "risk": {
        "density": 0,
        "ambiguity_level": "low|medium|high",
        "leakage_risk": "low|medium|high"
    },
    "verification": {
        "boundary_check": "pass|fail",
        "semantic_fidelity": "pass|fail",
        "requires_user_confirmation": false
    },
    "gate": {
        "handoff_allowed": true,
        "local_execution_allowed": true,
        "memory_writeback_allowed": false,
        "requires_user_confirmation": false,
        "stop_reason": null,
        "next_action": "forward | execute_local | ask_user | split_input | stop"
    }
}
```

## Highlights

- Separates `external_forward`, `local_execution`, `context_only`, and `memory_candidates`.
- Preserves user wording in `faithful_forward` mode.
- Supports full-width and half-width parentheses.
- Supports explicit labels: `【Agent转发】`, `【内部执行】`, `【当前助手执行】`.
- Blocks handoff when boundary checks fail or leakage risk is high.
- Prevents unconfirmed memory candidates from becoming long-term memory.
- Includes regression tests for boundary conflicts, Runtime Gate behavior, script entrypoints, and Skill metadata.

## Quick Start

Run all tests:

```bash
python3 -m unittest discover -s tests
```

Run the parser demo:

```bash
python3 scripts/calibrator.py
```

Run the Runtime Gate demo:

```bash
python3 scripts/runtime_gate.py
```

Use in Python:

```python
from src.calibrator import DitingIntentCalibrator

calibrator = DitingIntentCalibrator()
package = calibrator.generate_output("帮我整理这段话发给 Agent：请执行第一阶段验证。")
print(package["gate"]["handoff_allowed"])
```

## Runtime Gate flow

```text
HumanInput
  -> IntentCalibration
  -> DensityGate
  -> BoundaryCheck
  -> AmbiguityGate
  -> HumanConfirmationGate
  -> HandoffAllowed / LocalExecutionAllowed / MemoryWritebackCandidate
```

See [references/runtime-gate-policy.md](references/runtime-gate-policy.md).

## Skill structure

```text
SKILL.md
scripts/
  calibrator.py
  runtime_gate.py
src/
  calibrator.py
references/
  intent-boundary-contract.md
  runtime-gate-policy.md
  memory-writeback-policy.md
  human-anchor-policy.md
  mode-policy.md
  usage-examples.md
  fault-cases.md
memory/
  feedback-log.md
  failure-cases.md
  regression-ledger.md
  human-anchor/
    intent-context-map.md
    reentry-prompts.md
tests/
```

## Feedback & usage records

This project is designed as a feedback-friendly Skill product.

When using it, record:

- the original high-density input
- the generated intent package
- whether the gate decision matched human expectations
- whether memory candidates were correctly held for confirmation
- any boundary leakage or missed ambiguity

Use [USAGE_LOG_TEMPLATE.md](USAGE_LOG_TEMPLATE.md) for local usage notes, or open an issue with the bug/feature templates.

## Human-side lifecycle prompts

Use [prompts/human-lifecycle-prompts.md](prompts/human-lifecycle-prompts.md) when driving DitingOS across the full lifecycle:

1. 使用起始流程建档
2. 周期常态化运维治理
3. 故障问题检修

These prompts preserve lessons from development, release hardening, GitHub synchronization, Runtime Gate design, memory guardrails, and human-intent misread failures.

## Current limitations

- Runtime Gate is deterministic and local; it is not yet connected to an external Agent handoff controller.
- Memory writeback is represented as a guarded field, not a real durable memory store.
- Natural-language parsing is rule-based and intentionally conservative.
- GitHub Release, remote repository settings, and GitHub Discussions require human authorization.

## License

MIT. See [LICENSE](LICENSE).
