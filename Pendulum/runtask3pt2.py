import argparse
from pathlib import Path, PurePath
from pendulum import Pendulum

# terminal script:


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Pendulum")
    parser.add_argument("excelpath", type = str, help = "Path to the Excelfile")
    args = parser.parse_args()  # collects all arguments

    excelpath = PurePath(str(Path.cwd()) + "/" + (args.excelpath))

    oma = Pendulum(excelpath)

    oma.plot_slope()