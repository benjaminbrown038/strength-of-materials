"""Run every implemented learning tier; stop if any subprocess fails."""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plot", action="store_true")
    parser.add_argument("--output", type=Path, default=ROOT / "results")
    args = parser.parse_args()
    for n in range(9):
        folder = ROOT / ("fundamentals" if n == 0 else "advanced") / ("tier-" + str(n))
        command = [sys.executable, str(folder / "main.py"), "--output", str(args.output / folder.name)]
        if args.plot:
            command.append("--plot")
        subprocess.run(command, check=True)

if __name__ == "__main__":
    main()
