# Human Anchor Policy

Human anchors are stable re-entry points for human-machine collaboration. They help recover context without silently converting assumptions into memory.

## Ask-user triggers

Do not guess. Ask the user when:

1. `external_forward` and `local_execution` overlap.
2. The user says both `帮我整理` and `发给 Agent`, but the forwarded body boundary is unclear.
3. `memory_candidates` mention long-term preferences, identity, constraints, or strategy.
4. Input contains high-density multi-task, multi-Agent, or multi-layer forwarding.
5. Parentheses, quotes, or explicit labels conflict.

## Human anchor fields

- original user input
- calibrated intent package
- unresolved ambiguity
- confirmation question
- user decision
- resulting gate state
