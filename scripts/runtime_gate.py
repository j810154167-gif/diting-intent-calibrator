from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.calibrator import DitingIntentCalibrator


class RuntimeGate(DitingIntentCalibrator):
    """Runtime Gate wrapper for calibrated intent packages."""

    def evaluate(self, user_input, memory_writeback_confirmed=False):
        return self.generate_output(
            user_input,
            memory_writeback_confirmed=memory_writeback_confirmed
        )


if __name__ == "__main__":
    gate = RuntimeGate()
    sample = "帮我整理这段话发给 Agent：请执行外部任务。"
    print(gate.evaluate(sample))
