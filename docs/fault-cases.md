# 故障案例库

## FC-001 高密度混合意图导致边界坍缩

### 触发条件

- 单轮输入包含多层复合意图。
- 同时包含转发文本、本地执行任务、背景和记忆候选。
- 未使用显式边界标记。

### 症状

- 本地执行指令混入 `external_forward`。
- 背景上下文污染 Agent handoff。
- 记忆候选被误判为可写入长期记忆。

### 修复策略

- 使用 Runtime Gate 阻断高风险 handoff。
- 高密度输入进入 `split_input` 或 `ask_user`。
- 将失败迁移为 regression-ledger 条目和测试。

## FC-002 括号边界冲突

### 触发条件

- 括号内既出现本地执行语义，又出现 `发给 Agent`。
- 显式标签与括号规则冲突。

### 修复策略

- 括号默认进入 `local_execution`。
- 括号内显式 `发给 Agent：` 才进入 `external_forward`。
- 标签冲突时必须 `requires_user_confirmation = true`。

## FC-003 过度剪枝破坏忠实转发

### 触发条件

- 用户原文包含“我认为 / 建议你 / 应该 / 可以”等主观词。

### 修复策略

- `faithful_forward` 模式只提取，不改写。
- 不默认删除用户原文主观词。
