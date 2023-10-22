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

    print("___________________________________________________________")
    print(" ")
    print("period from the shortest length:")
    print("mean: ", oma.shortest_period_stats()[0], "s")
    print("standard deviation: ", oma.shortest_period_stats()[1], "s")
    print("confidence interval: " , oma.shortest_period_stats()[2], "s")
    print(" ")
    print(" ")
    print(" ")
    print("period from the longest length:")
    print("mean: ", oma.longest_period_stats()[0], "s")
    print("standard deviation: ", oma.longest_period_stats()[1], "s")
    print("confidence interval: ", oma.longest_period_stats()[2], "s")
    print(" ")
    print("___________________________________________________________")