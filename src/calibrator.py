import re
from datetime import datetime


class DitingIntentCalibrator:
    def __init__(self, version="1.3"):
        self.version = version
        self.density_threshold = 2.5
        self.fault_history = []
        self.training_set = []

    def generate_output(self, user_input, memory_writeback_confirmed=False):
        """生成结构化意图包。"""
        package = self.parse_intent(user_input, memory_writeback_confirmed=memory_writeback_confirmed)
        self.training_set.append({
            "input": user_input,
            "output": package,
            "timestamp": self.get_timestamp()
        })
        return package

    def parse_intent(self, user_input, memory_writeback_confirmed=False):
        mode = self.detect_mode(user_input)
        density = self.calculate_input_density(user_input)

        external_parts = []
        local_execution = []
        context_only = []
        memory_candidates = []
        ambiguities = []

        explicit = self.extract_explicit_sections(user_input)
        consumed_text = user_input
        if explicit:
            external_parts.extend(explicit.get("external_forward", []))
            local_execution.extend(explicit.get("local_execution", []))
            consumed_text = self.remove_explicit_sections(user_input)

        bracket_result = self.extract_parentheses(consumed_text)
        external_parts.extend(bracket_result["external_forward"])
        local_execution.extend(bracket_result["local_execution"])
        text_without_brackets = bracket_result["remaining_text"]

        wrapper_forward = self.extract_wrapper_forward(text_without_brackets)
        if wrapper_forward:
            external_parts.append(wrapper_forward)
        elif not explicit and self.has_forwarding_intent(text_without_brackets):
            extracted = self.extract_after_forward_marker(text_without_brackets)
            if extracted:
                external_parts.append(extracted)
            else:
                ambiguities.append("检测到转发意图，但未找到清晰的转发正文边界")

        context_only.extend(self.extract_context_only(user_input))
        memory_candidates.extend(self.extract_memory_candidates(user_input))

        external_forward = self.filter_non_forward_lines(self.join_text(external_parts))
        local_execution = self.clean_list(local_execution)
        context_only = self.clean_list(context_only)
        memory_candidates = self.clean_list(memory_candidates)

        if self.looks_like_current_assistant_task(external_forward):
            ambiguities.append("Agent 转发正文疑似包含当前助手执行任务")
        ambiguities.extend(self.detect_confirmation_triggers(user_input, external_forward, local_execution, memory_candidates))

        ambiguity_level = self.calculate_ambiguity_level(density, ambiguities)
        leakage_risk = self.calculate_leakage_risk(external_forward, local_execution, density, ambiguities)
        boundary_pass = "fail" if any("疑似包含当前助手执行任务" in item or "边界重叠" in item for item in ambiguities) else "pass"
        requires_confirmation = density > self.density_threshold or bool(ambiguities) or bool(memory_candidates) or ambiguity_level == "high"

        package = {
            "raw_input": user_input,
            "mode": mode,
            "intent_layers": {
                "external_forward": external_forward,
                "local_execution": local_execution,
                "context_only": context_only,
                "memory_candidates": memory_candidates
            },
            "ambiguities": ambiguities,
            "risk": {
                "density": round(density, 2),
                "ambiguity_level": ambiguity_level,
                "leakage_risk": leakage_risk
            },
            "verification": {
                "boundary_check": boundary_pass,
                "semantic_fidelity": self.semantic_fidelity_check(user_input, external_forward),
                "requires_user_confirmation": requires_confirmation
            }
        }
        package["gate"] = self.evaluate_runtime_gate(package, memory_writeback_confirmed=memory_writeback_confirmed)
        return package

    def detect_mode(self, user_input):
        if re.search(r"润色|压缩|改写|重写|优化表达|换个说法", user_input):
            return "rewrite"
        if re.search(r"结构化整理|语义整理|按层整理|分层整理", user_input):
            return "semantic_organize"
        return "faithful_forward"

    def extract_explicit_sections(self, user_input):
        marker_pattern = re.compile(r"【(Agent\s*转发|内部执行|当前助手执行)】")
        matches = list(marker_pattern.finditer(user_input))
        if not matches:
            return {}

        sections = {"external_forward": [], "local_execution": []}
        for index, match in enumerate(matches):
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(user_input)
            content = user_input[start:end].strip()
            if not content:
                continue
            marker = re.sub(r"\s+", "", match.group(1))
            if marker == "Agent转发":
                sections["external_forward"].append(content)
            else:
                sections["local_execution"].extend(self.split_tasks(content))
        return sections

    def remove_explicit_sections(self, user_input):
        marker_pattern = re.compile(r"【(Agent\s*转发|内部执行|当前助手执行)】")
        first = marker_pattern.search(user_input)
        return user_input[:first.start()].strip() if first else user_input

    def extract_parentheses(self, user_input):
        result = {"external_forward": [], "local_execution": [], "remaining_text": user_input}

        def replace(match):
            content = match.group(1).strip()
            forward_match = re.search(r"(?:发给|转发给)\s*Agent\s*[:：](.*)", content, re.S | re.I)
            if forward_match:
                result["external_forward"].append(forward_match.group(1).strip())
            elif content:
                result["local_execution"].append(content)
            return ""

        result["remaining_text"] = re.sub(r"[（(]([^()（）]*?)[）)]", replace, user_input).strip()
        return result

    def extract_wrapper_forward(self, text):
        patterns = [
            r"帮我(?:整理|处理|提取|生成)?这段话(?:，|,)?(?:发给|转发给)\s*Agent\s*[:：](.*)",
            r"(?:发给|转发给)\s*Agent\s*[:：](.*)",
            r"(?:纯指令|干净版)\s*[:：](.*)"
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.S | re.I)
            if match:
                return match.group(1).strip()
        return ""

    def extract_after_forward_marker(self, text):
        match = re.search(r"(?:发给|转发给|复制发送)\s*(?:[^:：\n]{0,20})?[:：](.*)", text, re.S | re.I)
        return match.group(1).strip() if match else ""

    def has_forwarding_intent(self, text):
        return bool(re.search(r"发给|转发给|复制发送|纯指令|干净版", text, re.I))

    def has_explicit_agent_marker(self, text):
        return bool(re.search(r"【Agent\s*转发】|(?:发给|转发给)\s*Agent\s*[:：]", text, re.I))

    def looks_like_local_task(self, text):
        return bool(text and re.match(r"\s*(帮我|请你|你来|当前助手|内部执行|搜索|补全|整理|检查|生成)", text))

    def looks_like_current_assistant_task(self, text):
        return bool(text and re.match(r"\s*(帮我|你来|当前助手|内部执行|搜索|补全|整理|检查|生成)", text))

    def extract_context_only(self, user_input):
        items = []
        for line in user_input.splitlines():
            stripped = line.strip()
            if re.match(r"^(背景|上下文|补充背景)[:：]", stripped):
                items.append(re.split(r"[:：]", stripped, maxsplit=1)[1].strip())
        return items

    def extract_memory_candidates(self, user_input):
        items = []
        for line in user_input.splitlines():
            stripped = line.strip()
            if re.search(r"记住|长期记忆|记忆候选|写入记忆", stripped):
                items.append(stripped)
        return items

    def semantic_prune(self, content):
        """保持兼容：只规整空白，不删除用户主观词。"""
        return self.normalize_text(content)

    def detect_confirmation_triggers(self, user_input, external_forward, local_execution, memory_candidates):
        triggers = []
        for task in local_execution:
            if task and task in external_forward:
                triggers.append("external_forward 和 local_execution 边界重叠")
        if re.search(r"帮我整理", user_input) and re.search(r"发给\s*Agent", user_input, re.I) and not external_forward:
            triggers.append("用户同时使用帮我整理和发给 Agent，但正文边界不清晰")
        if memory_candidates and re.search(r"长期|偏好|身份|约束|战略|方向|原则", "\n".join(memory_candidates)):
            triggers.append("memory_candidates 涉及长期偏好、身份、约束或战略方向")
        if self.contains_high_density_agentic_pattern(user_input):
            triggers.append("输入包含高密度多任务、多 Agent 或多层转发")
        if self.has_marker_conflict(user_input):
            triggers.append("括号、引号或显式标签存在冲突")
        if self.has_quoted_parentheses_conflict(user_input):
            triggers.append("引号内括号指令存在边界冲突")
        return list(dict.fromkeys(triggers))

    def contains_high_density_agentic_pattern(self, user_input):
        multi_task = len(re.findall(r"帮我|请你|搜索|补全|生成|检查|归档|转发", user_input)) >= 4
        multi_agent = len(re.findall(r"Agent", user_input, re.I)) >= 2 or re.search(r"多\s*Agent|三台|多个Agent", user_input, re.I)
        multi_layer = len(re.findall(r"发给|转发给|内部|外部|当前助手", user_input)) >= 3
        return bool(multi_task and (multi_agent or multi_layer))

    def has_marker_conflict(self, user_input):
        has_explicit = bool(re.search(r"【Agent\s*转发】", user_input))
        has_local_parentheses = bool(re.search(r"[（(][^()（）]*(?:不要发给|内部|当前助手)[^()（）]*[）)]", user_input))
        has_forward_parentheses = bool(re.search(r"[（(][^()（）]*(?:发给|转发给)\s*Agent[^()（）]*[）)]", user_input, re.I))
        unbalanced = user_input.count("（") != user_input.count("）") or user_input.count("(") != user_input.count(")")
        return bool(unbalanced or (has_explicit and has_local_parentheses and has_forward_parentheses))

    def has_quoted_parentheses_conflict(self, user_input):
        quoted_parts = re.findall(r"[“\"]([^”\"]*[（(][^”\"]*[）)][^”\"]*)[”\"]", user_input)
        return any(self.looks_like_current_assistant_task(re.sub(r"^[^（(]*[（(]|[）)][^）)]*$", "", part).strip()) for part in quoted_parts)

    def filter_non_forward_lines(self, text):
        lines = []
        for line in self.normalize_text(text).splitlines():
            stripped = line.strip()
            if re.match(r"^(背景|上下文|补充背景)[:：]", stripped):
                continue
            if re.search(r"记住|长期记忆|记忆候选|写入记忆", stripped):
                continue
            lines.append(stripped)
        return self.normalize_text("\n".join(lines))

    def evaluate_runtime_gate(self, package, memory_writeback_confirmed=False):
        layers = package["intent_layers"]
        risk = package["risk"]
        verification = package["verification"]
        has_external = bool(layers["external_forward"])
        has_local = bool(layers["local_execution"])
        has_memory = bool(layers["memory_candidates"])

        memory_writeback_allowed = bool(has_memory and memory_writeback_confirmed)
        local_execution_allowed = has_local and verification["boundary_check"] == "pass"

        stop_reason = None
        next_action = "forward" if has_external else "execute_local" if has_local else "stop"
        handoff_allowed = has_external

        if verification["boundary_check"] == "fail":
            handoff_allowed = False
            local_execution_allowed = False
            stop_reason = "boundary_check_failed"
            next_action = "stop"
        elif risk["leakage_risk"] == "high":
            handoff_allowed = False
            stop_reason = "high_leakage_risk"
            next_action = "split_input" if risk["density"] > self.density_threshold else "ask_user"
        elif risk["ambiguity_level"] == "high":
            handoff_allowed = False
            stop_reason = "high_ambiguity"
            next_action = "ask_user"
        elif risk["density"] > self.density_threshold:
            handoff_allowed = False
            stop_reason = "density_threshold_exceeded"
            next_action = "split_input"
        elif verification["requires_user_confirmation"]:
            handoff_allowed = False
            stop_reason = "user_confirmation_required"
            next_action = "ask_user"
        elif not has_external and has_local:
            handoff_allowed = False
            next_action = "execute_local"

        if has_memory and not memory_writeback_allowed and stop_reason is None:
            stop_reason = "memory_confirmation_required"
            next_action = "ask_user"
            handoff_allowed = False

        requires_user_confirmation = verification["requires_user_confirmation"] or risk["ambiguity_level"] == "high" or has_memory
        return {
            "handoff_allowed": handoff_allowed,
            "local_execution_allowed": local_execution_allowed,
            "memory_writeback_allowed": memory_writeback_allowed,
            "requires_user_confirmation": requires_user_confirmation,
            "stop_reason": stop_reason,
            "next_action": next_action
        }

    def boundary_check(self, forward_content, internal_content):
        if self.looks_like_local_task(forward_content):
            return False, "Agent 转发正文疑似包含当前助手执行任务"
        for internal in internal_content:
            if internal and internal in forward_content:
                return False, "内部指令混入转发部分"
        return True, "边界校验通过"

    def calculate_input_density(self, user_input):
        sentence_count = max(1, len([s for s in re.split(r"[。！？!?\n]+", user_input) if s.strip()]))
        keywords = ["语义剪枝", "发给", "转发给", "补全", "搜索", "整理", "归档", "升维", "记忆链", "Agent", "内部", "外部", "上下文", "记忆"]
        keyword_count = sum(user_input.count(k) for k in keywords)
        bracket_count = len(re.findall(r"[（(][^()（）]*?[）)]", user_input))
        char_factor = len(user_input) / 180.0
        return sentence_count * 0.1 + keyword_count * 0.25 + bracket_count * 0.45 + char_factor

    def calculate_ambiguity_level(self, density, ambiguities):
        if density > self.density_threshold or len(ambiguities) >= 2:
            return "high"
        if density > 1.5 or ambiguities:
            return "medium"
        return "low"

    def calculate_leakage_risk(self, external_forward, local_execution, density, ambiguities):
        if density > self.density_threshold or ambiguities:
            return "high"
        if external_forward and local_execution:
            return "medium"
        return "low"

    def semantic_fidelity_check(self, raw_input, external_forward):
        if not external_forward:
            return "pass"
        subjective_terms = ["我认为", "建议你", "应该", "可以"]
        for term in subjective_terms:
            if term in raw_input and term not in external_forward:
                return "fail"
        return "pass"

    def split_tasks(self, content):
        tasks = []
        for line in content.splitlines():
            stripped = re.sub(r"^\s*\d+[.、]\s*", "", line).strip()
            if stripped:
                tasks.append(stripped)
        return tasks

    def clean_list(self, items):
        return [self.normalize_text(item) for item in items if self.normalize_text(item)]

    def join_text(self, parts):
        return self.normalize_text("\n".join(part for part in parts if self.normalize_text(part)))

    def normalize_text(self, text):
        text = re.sub(r"[ \t]+\n", "\n", text or "")
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def get_timestamp(self):
        return datetime.now().isoformat()


DitingIntentCalibratorCompat = DitingIntentCalibrator


if __name__ == "__main__":
    calibrator = DitingIntentCalibrator()
    sample = "帮我整理这段话发给 Agent：我认为这个方案可以继续推进。（帮我检查边界）"
    print(calibrator.generate_output(sample))
