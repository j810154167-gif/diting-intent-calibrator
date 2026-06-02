# Usage Examples

## Wrapper instruction

Input:

```text
帮我整理这段话发给 Agent：
我认为这个方案可以继续推进。
（帮我检查是否有内部指令混入）
```

Expected layers:

- `external_forward`: `我认为这个方案可以继续推进。`
- `local_execution`: `帮我检查是否有内部指令混入`

## Explicit markers

Input:

```text
【Agent转发】
请执行 A。
【当前助手执行】
检查边界。
```

Expected layers:

- `external_forward`: `请执行 A。`
- `local_execution`: `检查边界。`

## Parentheses forwarding override

Input:

```text
（发给 Agent：请只处理这句话）
```

Expected layers:

- `external_forward`: `请只处理这句话`
