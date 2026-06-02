# 设计原理：Diting intent calibrator

DitingOS 将本项目定位为“人类意图显性校准中枢”，用于在人机协同时代缓解两类结构性缺陷：

- 人类弥散脑缺陷：高密度、跳跃式、隐含上下文过多，容易把转发文本、本地任务、背景和记忆候选混在一起。
- 机器线性脑缺陷：模型倾向按单一线性任务执行，容易误把本地指令转发给 Agent，或把记忆候选当成长期记忆写入。

## 问题定义

在人机协同生产流中，最常见的风险是指令边界模糊：

- 人类在单轮输入中同时包含发给 Agent 的指令和当前助手要执行的任务。
- 当前助手无法准确区分责任主体，导致内部执行指令混入外部转发文本。
- 背景上下文或记忆候选污染 Agent handoff。
- 高密度复合意图触发注意力衰减，导致输出错误。

## 解决方案

Diting intent calibrator 通过显性意图分层和 Runtime Gate 实现边界隔离：

1. 将输入拆分为 `external_forward`、`local_execution`、`context_only`、`memory_candidates`。
2. `faithful_forward` 默认保留用户原文，不主动删除主观词。
3. Runtime Gate 输出显式 `handoff_allowed` 字段，禁止靠自然语言判断是否可转发。
4. 记忆候选只进入候选层，未经用户确认不得写入长期记忆。
5. 失败案例应迁移为回归测试，形成持续硬化闭环。

## 演进方向

- 增强高密度输入分段策略。
- 增加多 Agent handoff schema。
- 引入外部 handoff controller。
- 引入带审批状态的 durable memory store。
