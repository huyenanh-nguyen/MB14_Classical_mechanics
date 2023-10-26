import argparse
from pathlib import Path, PurePath
from pendulum import Pendulum
import numpy as np

# terminal script:


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Pendulum")
    parser.add_argument("excelpath", type = str, help = "Path to the Excelfile")
    parser.add_argument("guessingerror_length", type = float, help = "how accurate can we measure the length?")
    parser.add_argument("guessing_zeroerror_length", type = float, help = "how accurate can we measure the length of the pendulum from the center of mass?")
    parser.add_argument("guessing_timeerror", type = float, help = "how accurate can we measure the time?")
    parser.add_argument("reaction_error", type = float, help = "reaction error of stopping the time")
    args = parser.parse_args()  # collects all arguments

    excelpath = PurePath(str(Path.cwd()) + "/" + (args.excelpath))
    guessingerror_length = args.guessingerror_length
    guessing_zeroerror_length = args.guessing_zeroerror_length
    guessing_timeerror = args.guessing_timeerror
    reaction_error = args.reaction_error

    oma = Pendulum(excelpath)

    digit = 3

    print("___________________________________________________________")
    print(" ")
    print("∆li,Faden:")
    print(np.round(oma.stringlength_error(guessingerror_length),digit))
    print(" ")
    print("∆li,ges:")
    print(np.round(oma.total_length_error(guessingerror_length, guessing_zeroerror_length),digit))
    print("___________________________________________________________")
    print(" ")
    print("∆τ1, ges: ")
    print(np.round(oma.total_error_period(guessing_timeerror, reaction_error),digit))
    print(" ")
    