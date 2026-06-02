from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.calibrator import DitingIntentCalibrator


if __name__ == "__main__":
    calibrator = DitingIntentCalibrator()
    sample = "帮我整理这段话发给 Agent：我认为这个方案可以继续推进。（帮我检查边界）"
    print(calibrator.generate_output(sample))
