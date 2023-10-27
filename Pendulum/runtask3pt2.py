import argparse
from pathlib import Path, PurePath
from pendulum import Pendulum

# terminal script:


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Pendulum")
    parser.add_argument("excelpath", type = str, help = "Path to the Excelfile")
    parser.add_argument("guessing_timeerror", type = float, help = "guess the uncertainty of the time -> the last digit of my timer,mostly it is 10 ms")
    parser.add_argument("reaction_error", type = float, help = "there will be always some reaction delay by stopping the time. this is round about 150 - 200 ms")
    args = parser.parse_args()  # collects all arguments

    excelpath = PurePath(str(Path.cwd()) + "/" + (args.excelpath))
    guess_timeerror = args.guessing_timeerror
    reaction_error = args.reaction_error

    oma = Pendulum(excelpath)

    oma.plot_slope(guess_timeerror, reaction_error)