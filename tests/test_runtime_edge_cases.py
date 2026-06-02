import unittest
from src.calibrator import DitingIntentCalibrator


class TestRuntimeEdgeCases(unittest.TestCase):
    def setUp(self):
        self.calibrator = DitingIntentCalibrator()

    def test_explicit_label_conflict_requires_confirmation(self):
        user_input = """【Agent转发】
        请执行 A。
        （不要发给 Agent，这是内部任务）
        （发给 Agent：请执行 B）
        """

        output = self.calibrator.generate_output(user_input)

        self.assertTrue(output["ambiguities"])
        self.assertTrue(output["gate"]["requires_user_confirmation"])
        self.assertFalse(output["gate"]["handoff_allowed"])
        self.assertEqual(output["gate"]["next_action"], "split_input")

    def test_memory_candidate_does_not_pollute_external_forward(self):
        user_input = """帮我整理这段话发给 Agent：请执行外部任务。
        请记住：我的长期偏好是先做边界校验。
        """

        output = self.calibrator.generate_output(user_input)
        layers = output["intent_layers"]

        self.assertEqual(layers["external_forward"], "请执行外部任务。")
        self.assertEqual(layers["memory_candidates"], ["请记住：我的长期偏好是先做边界校验。"])
        self.assertFalse(output["gate"]["memory_writeback_allowed"])
        self.assertTrue(output["gate"]["requires_user_confirmation"])

    def test_context_only_does_not_pollute_external_forward(self):
        user_input = """帮我整理这段话发给 Agent：请执行外部任务。
        背景：这是给当前助手判断密度的上下文。
        """

        output = self.calibrator.generate_output(user_input)
        layers = output["intent_layers"]

        self.assertEqual(layers["external_forward"], "请执行外部任务。")
        self.assertEqual(layers["context_only"], ["这是给当前助手判断密度的上下文。"])

    def test_rewrite_mode_is_detected(self):
        user_input = "帮我润色后发给 Agent：这个方案可以继续推进。"

        output = self.calibrator.generate_output(user_input)

        self.assertEqual(output["mode"], "rewrite")
        self.assertIn("这个方案可以继续推进。", output["intent_layers"]["external_forward"])

    def test_quoted_parentheses_conflict_requires_confirmation(self):
        user_input = "帮我整理这段话发给 Agent：“请执行 A。（帮我内部检查）”"

        output = self.calibrator.generate_output(user_input)

        self.assertTrue(output["gate"]["requires_user_confirmation"])
        self.assertFalse(output["gate"]["handoff_allowed"])
        self.assertTrue(output["ambiguities"])

    def test_high_density_without_external_forward_blocks_handoff(self):
        user_input = "帮我搜索 A，补全 B，归档 C，记住 D，检查 E，多 Agent 对照，内部执行，不要转发。"

        output = self.calibrator.generate_output(user_input)

        self.assertFalse(output["gate"]["handoff_allowed"])
        self.assertIn(output["gate"]["next_action"], ["ask_user", "split_input", "stop"])
        self.assertTrue(output["gate"]["requires_user_confirmation"])


if __name__ == "__main__":
    unittest.main()
