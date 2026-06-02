# Fault Cases

## FC-001 High-density mixed intent

High-density single-turn input can mix forwarding text, local tasks, background, and memory candidates. Mark ambiguity and require confirmation when density is high.

## FC-002 Parentheses ambiguity

Parentheses default to local execution, except when the parenthesized content explicitly says it should be sent to Agent.

## FC-003 Over-pruning

Do not remove user-authored subjective phrases such as “我认为”, “建议你”, “应该”, or “可以”. Removing them can violate semantic fidelity.
