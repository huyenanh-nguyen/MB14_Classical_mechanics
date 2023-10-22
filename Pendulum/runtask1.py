import argparse
from pathlib import Path, PurePath
from pendulum import Pendulum

# terminal script:

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Pendulum")
    parser.add_argument("excelpath", type = str, help = "Path to the Excelfile")
    parser.add_argument("time_systematic_error", type = float, help = "Systematic error of the offset from my instrument. In this case the last digit of the timer")
    args = parser.parse_args()  # collects all arguments

    excelpath = PurePath(str(Path.cwd()) + "/" + (args.excelpath))
    time_systematic_error = args.time_systematic_error

    oma = Pendulum(excelpath)   # oma is an acronym for our group

    print("___________________________________________________________")
    print(" ")
    print("period at equilibrium point:")
    print("mean: ", oma.equilibrium_period_stats()[0], "s")
    print("standard deviation: ", oma.equilibrium_period_stats()[1], "s")
    print("confidence interval: " , oma.equilibrium_period_stats()[2], "s")
    print("total uncertainty of period at the equilibrium point: ", oma.equilibrium_period_total_err(time_systematic_error), "s")
    print(" ")
    print("results period at equilibrium point: ", oma.equilibrium_period_stats()[0], u" \u00B1 ", oma.equilibrium_period_total_err(time_systematic_error), "s")
    print(" ")
    print(" ")
    print(" ")
    print("period at turning point:")
    print("mean: ", oma.turningpoint_period_stats()[0], "s")
    print("standard deviation: ", oma.turningpoint_period_stats()[1], "s")
    print("confidence interval: ", oma.turningpoint_period_stats()[2], "s")
    print("total uncertainty of period at the turning point: ", oma.turningpoint_period_total_err(time_systematic_error), "s")
    print(" ")
    print("results period at turning point: ", oma.turningpoint_period_stats()[0], u"\u00B1", oma.turningpoint_period_total_err(time_systematic_error), "s")
    print(" ")
    print("___________________________________________________________")