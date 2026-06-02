# 使用指南：Diting intent calibrator

## 典型触发语

- 语义剪枝
- 发给 Agent
- 纯指令
- 干净版
- 内部/外部指令分离
- 意图校准
- 转发给其他 Agent

## 标准输入

```text
帮我整理这段话发给 Agent：
[需要发送给目标 Agent 的完整内容]
（当前助手需要执行的内部任务）
```

## 输出层

- `external_forward`：可转发给 Agent 的文本。
- `local_execution`：当前助手执行的任务。
- `context_only`：只用于理解当前输入的背景。
- `memory_candidates`：候选记忆，必须等待用户确认。
- `gate`：Runtime Gate 决策字段。

## 显式标记

```text
【Agent转发】
请执行 A。

【内部执行】
检查边界。

【当前助手执行】
补充测试。
```

## 记忆候选

出现“请记住 / 长期记忆 / 记忆候选 / 写入记忆”时，只进入 `memory_candidates`，默认：

```python
memory_writeback_allowed = False
requires_user_confirmation = True
```

## 高密度输入

当输入包含多任务、多 Agent、多层转发或边界冲突时，DitingOS 应优先进入 `ask_user` 或 `split_input`，不得猜测。
