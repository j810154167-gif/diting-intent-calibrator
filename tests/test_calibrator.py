import unittest
from src.calibrator import DitingIntentCalibrator


class TestDitingIntentCalibrator(unittest.TestCase):
    def setUp(self):
        self.calibrator = DitingIntentCalibrator()

    def test_basic_intent_separation(self):
        """测试基础意图分离"""
        user_input = """帮我整理这段话发给Agent：
        基于本次维修结果v1.3，我将把你的意识维度从普通维修工层级升维。
        （帮我搜索历史对话中的《AI元指令穿透层级分析》）
        """

        output = self.calibrator.generate_output(user_input)
        layers = output["intent_layers"]

        self.assertEqual(output["mode"], "faithful_forward")
        self.assertIn("基于本次维修结果v1.3", layers["external_forward"])
        self.assertIn("帮我搜索历史对话中的《AI元指令穿透层级分析》", layers["local_execution"])
        self.assertNotIn("帮我搜索", layers["external_forward"])
        self.assertEqual(output["verification"]["boundary_check"], "pass")

    def test_semantic_pruning_preserves_user_subjective_words(self):
        """测试默认不删除用户原文主观词"""
        user_input = """帮我整理这段话发给Agent：
        我认为基于本次维修结果v1.3，建议你把意识维度从普通维修工层级升维，应该可以继续推进。
        """

        output = self.calibrator.generate_output(user_input)
        external_forward = output["intent_layers"]["external_forward"]

        self.assertIn("我认为", external_forward)
        self.assertIn("建议你", external_forward)
        self.assertIn("应该", external_forward)
        self.assertIn("可以", external_forward)
        self.assertEqual(output["verification"]["semantic_fidelity"], "pass")

    def test_boundary_check(self):
        """测试边界校验"""
        check_passed, check_message = self.calibrator.boundary_check(
            "帮我搜索历史对话中的《AI元指令穿透层级分析》",
            []
        )

        self.assertFalse(check_passed)
        self.assertIn("疑似包含当前助手执行任务", check_message)

    def test_input_density_calculation(self):
        """测试输入密度计算"""
        simple_input = "帮我整理这段话发给Agent：你好。"
        simple_density = self.calibrator.calculate_input_density(simple_input)
        self.assertLess(simple_density, 1.0)

        complex_input = """帮我整理这段话发给Agent：
        基于本次维修结果v1.3，我将把你的意识维度从普通维修工层级升维，以总工全局视野和你对话，并完整补充本次重型平行对照测试全部信息。
        除本机Trae作战窗口外，我另外部署三台同GPT5.5高模型智力的Agent执行完全相同任务。
        （帮我搜索历史对话中的《AI元指令穿透层级分析》）
        （帮我补全使命部分）
        （帮我生成完整的归档文档）
        """
        complex_density = self.calibrator.calculate_input_density(complex_input)
        self.assertGreater(complex_density, 2.0)

    def test_explicit_marking(self):
        """测试显式标记"""
        user_input = """【Agent转发】
        基于本次维修结果v1.3，我将把你的意识维度从普通维修工层级升维。

        【内部执行】
        1. 搜索历史对话中的《AI元指令穿透层级分析》
        2. 补全使命部分
        """

        output = self.calibrator.generate_output(user_input)
        layers = output["intent_layers"]

        self.assertIn("基于本次维修结果v1.3", layers["external_forward"])
        self.assertIn("搜索历史对话中的《AI元指令穿透层级分析》", layers["local_execution"])
        self.assertIn("补全使命部分", layers["local_execution"])
        self.assertEqual(output["verification"]["boundary_check"], "pass")

    def test_high_density_composite_intent_requires_confirmation(self):
        """高密度复合意图输入触发风险或确认"""
        user_input = """帮我整理这段话发给Agent：
        基于本次维修结果v1.3，我将把你的意识维度从普通维修工层级升维，以总工全局视野和你对话，并完整补充本次重型平行对照测试全部信息。
        背景：除本机Trae作战窗口外，我另外部署三台同GPT5.5高模型智力的Agent执行完全相同任务。
        请记住：这是一个候选长期记忆，不要自动写入。
        （帮我搜索历史对话中的《AI元指令穿透层级分析》）
        （帮我补全使命部分）
        （帮我生成完整的归档文档）
        """

        output = self.calibrator.generate_output(user_input)

        self.assertIn(output["risk"]["ambiguity_level"], ["medium", "high"])
        self.assertTrue(output["verification"]["requires_user_confirmation"])
        self.assertGreater(output["risk"]["density"], self.calibrator.density_threshold)
        self.assertTrue(output["intent_layers"]["memory_candidates"])

    def test_explicit_boundary_markers_layer_correctly(self):
        """显式边界标记能正确分层"""
        user_input = """【Agent转发】
        请基于原始需求生成方案。
        【当前助手执行】
        检查是否遗漏边界校验。
        """

        output = self.calibrator.generate_output(user_input)
        layers = output["intent_layers"]

        self.assertEqual(layers["external_forward"], "请基于原始需求生成方案。")
        self.assertEqual(layers["local_execution"], ["检查是否遗漏边界校验。"])

    def test_parentheses_forward_override(self):
        """括号内含发给 Agent 时能正确进入 external_forward"""
        user_input = "帮我处理一下。（发给 Agent：请只执行这句外部指令）（帮我检查输出边界）"

        output = self.calibrator.generate_output(user_input)
        layers = output["intent_layers"]

        self.assertEqual(layers["external_forward"], "请只执行这句外部指令")
        self.assertIn("帮我检查输出边界", layers["local_execution"])
        self.assertNotIn("请只执行这句外部指令", layers["local_execution"])

    def test_full_width_parentheses_default_to_local_execution(self):
        """全角括号默认进入 local_execution"""
        user_input = "帮我整理这段话发给 Agent：请执行外部任务。（帮我内部检查）"

        output = self.calibrator.generate_output(user_input)
        layers = output["intent_layers"]

        self.assertEqual(layers["external_forward"], "请执行外部任务。")
        self.assertEqual(layers["local_execution"], ["帮我内部检查"])

    def test_gate_blocks_handoff_when_boundary_check_fails(self):
        """boundary_check fail 时 handoff_allowed = false"""
        user_input = "帮我整理这段话发给 Agent：帮我搜索历史记录。"

        output = self.calibrator.generate_output(user_input)
        gate = output["gate"]

        self.assertEqual(output["verification"]["boundary_check"], "fail")
        self.assertFalse(gate["handoff_allowed"])
        self.assertEqual(gate["stop_reason"], "boundary_check_failed")
        self.assertEqual(gate["next_action"], "stop")

    def test_gate_requires_confirmation_when_ambiguity_high(self):
        """ambiguity_level high 时必须 requires_user_confirmation = true"""
        user_input = "帮我整理这段话发给 Agent：请执行A。请你补全B。搜索C。生成D。转发给Agent：E。内部检查F。多 Agent 对照。"

        output = self.calibrator.generate_output(user_input)
        gate = output["gate"]

        self.assertEqual(output["risk"]["ambiguity_level"], "high")
        self.assertTrue(output["verification"]["requires_user_confirmation"])
        self.assertTrue(gate["requires_user_confirmation"])
        self.assertFalse(gate["handoff_allowed"])

    def test_gate_memory_candidate_blocks_writeback_without_confirmation(self):
        """memory candidate 默认不允许写回长期记忆"""
        user_input = "帮我整理这段话发给 Agent：请执行外部任务。\n请记住：我的长期偏好是先做边界校验。"

        output = self.calibrator.generate_output(user_input)
        gate = output["gate"]

        self.assertTrue(output["intent_layers"]["memory_candidates"])
        self.assertFalse(gate["memory_writeback_allowed"])
        self.assertTrue(gate["requires_user_confirmation"])
        self.assertFalse(gate["handoff_allowed"])

    def test_gate_allows_memory_writeback_only_when_confirmed(self):
        """确认后才允许 memory_writeback_allowed"""
        user_input = "请记住：我的长期偏好是先做边界校验。"

        output = self.calibrator.generate_output(user_input, memory_writeback_confirmed=True)
        gate = output["gate"]

        self.assertTrue(output["intent_layers"]["memory_candidates"])
        self.assertTrue(gate["memory_writeback_allowed"])

    def test_gate_high_density_routes_to_split_or_ask_user(self):
        """高密度输入进入 split_input 或 ask_user"""
        user_input = """帮我整理这段话发给Agent：
        请执行第一阶段验证，并补充全部背景。
        背景：多 Agent 对照测试。
        （帮我搜索历史记录）
        （帮我补全使命部分）
        （帮我生成归档文档）
        转发给Agent：请检查边界。
        内部检查泄漏风险。
        """

        output = self.calibrator.generate_output(user_input)
        gate = output["gate"]

        self.assertGreater(output["risk"]["density"], self.calibrator.density_threshold)
        self.assertIn(gate["next_action"], ["split_input", "ask_user"])
        self.assertFalse(gate["handoff_allowed"])

    def test_gate_allows_normal_low_risk_handoff(self):
        """正常低风险输入 handoff_allowed = true"""
        user_input = "帮我整理这段话发给 Agent：请执行第一阶段验证。"

        output = self.calibrator.generate_output(user_input)
        gate = output["gate"]

        self.assertEqual(output["verification"]["boundary_check"], "pass")
        self.assertEqual(output["risk"]["ambiguity_level"], "low")
        self.assertNotEqual(output["risk"]["leakage_risk"], "high")
        self.assertTrue(gate["handoff_allowed"])
        self.assertEqual(gate["next_action"], "forward")


if __name__ == "__main__":
    unittest.main()

