import re
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKILL_FILE = PROJECT_ROOT / "SKILL.md"


class TestSkillMetadata(unittest.TestCase):
    def test_skill_frontmatter_is_valid(self):
        content = SKILL_FILE.read_text(encoding="utf-8")

        self.assertTrue(content.startswith("---\n"))
        match = re.match(r"---\n(?P<frontmatter>.*?)\n---\n", content, re.S)
        self.assertIsNotNone(match)

        frontmatter = match.group("frontmatter")
        fields = {}
        current_key = None
        for line in frontmatter.splitlines():
            if line.startswith("  ") and current_key:
                fields[current_key] += " " + line.strip()
                continue
            if ":" in line:
                key, value = line.split(":", 1)
                current_key = key.strip()
                fields[current_key] = "" if value.strip() == ">" else value.strip().strip('"')

        self.assertEqual(fields["name"], "diting-intent-calibrator")
        self.assertIn("description", fields)
        self.assertIn("高密度人类输入", fields["description"])
        self.assertIn("发给 Agent", fields["description"])
        self.assertNotRegex(fields["description"], r"[<>]")

    def test_scripts_entrypoints_run(self):
        for script in ["scripts/calibrator.py", "scripts/runtime_gate.py"]:
            with self.subTest(script=script):
                result = subprocess.run(
                    [sys.executable, script],
                    cwd=PROJECT_ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("gate", result.stdout)


if __name__ == "__main__":
    unittest.main()
