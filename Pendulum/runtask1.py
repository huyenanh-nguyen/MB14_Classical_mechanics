import argparse
from pathlib import Path, PurePath
from pendulum import Pendulum
import numpy as np

# terminal script:

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Pendulum")
    parser.add_argument("excelpath", type = str, help = "Path to the Excelfile")
    parser.add_argument("time_systematic_error", type = float, help = "Systematic error of the offset from my instrument. In this case the last digit of the timer")
    args = parser.parse_args()  # collects all arguments

    excelpath = PurePath(str(Path.cwd()) + "/" + (args.excelpath))
    time_systematic_error = args.time_systematic_error

    oma = Pendulum(excelpath)   # oma is an acronym for our group

    digit = 3

    print("___________________________________________________________")
    print(" ")
    print("period at equilibrium point:")
    print("mean: ", np.round(oma.equilibrium_period_stats()[0], digit), "s")
    print("standard deviation: ", np.round(oma.equilibrium_period_stats()[1], digit), "s")
    print("confidence interval: " , np.round(oma.equilibrium_period_stats()[2], digit), "s")
    print("total uncertainty of period at equilibrium point: ", np.round(oma.equilibrium_period_total_err(time_systematic_error), digit), "s")
    print(" ")
    print("absolute results at equilibrium point: ", np.round(oma.equilibrium_period_stats()[0],digit), u" \u00B1 ", np.round(oma.equilibrium_period_total_err(time_systematic_error), digit), "s")
    print("relative results at equilibrium point: ", np.round(oma.equilibrium_period_stats()[0],digit), u"(1 \u00B1 ",np.round(oma.relative_equilibrium_error(time_systematic_error), digit), "%) s")
    print(" ")
    print(" ")
    print("period at turning point:")
    print("mean: ", np.round(oma.turningpoint_period_stats()[0], digit), "s")
    print("standard deviation: ", np.round(oma.turningpoint_period_stats()[1], digit), "s")
    print("confidence interval: ", np.round(oma.turningpoint_period_stats()[2], digit), "s")
    print("total uncertainty of period at the turning point: ", np.round(oma.turningpoint_period_total_err(time_systematic_error), digit), "s")
    print(" ")
    print("absolute results at equilibrium point: ", np.round(oma.turningpoint_period_stats()[0], digit), u"\u00B1", np.round(oma.turningpoint_period_total_err(time_systematic_error), digit), "s")
    print(" ")
    print("relative results at equilibrium point: ", np.round(oma.turningpoint_period_stats()[0],digit), u"(1 \u00B1 ",np.round(oma.turningpoint_period_total_err(time_systematic_error), digit), "%) s")
    print("___________________________________________________________")