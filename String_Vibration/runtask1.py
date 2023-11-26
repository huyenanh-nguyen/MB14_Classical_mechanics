import argparse
from pathlib import Path, PurePath
from stringvibration import Guitarstring
from MathKit import Statistics
import numpy as np

# terminal script:

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "String Vibration")
    parser.add_argument("excelpath", type = str, help = "Path to the Excelfile")
    parser.add_argument("taskindex", type = int, help = "index of the task")
    parser.add_argument("x_column", type = str, help = "column name of the x values")
    parser.add_argument("y_column", type = str, help = "column name of the y values")
    parser.add_argument("valueset", type = list, help = "list of values to calculate the statistics")
    parser.add_argument("systematic_error", type = float, help = "systematic error of the measuring tool")
    args = parser.parse_args()  # collects all arguments


    excelpath = PurePath(str(Path.cwd()) + "/" + (args.excelpath))
    taskindex = args.taskindex
    x_column = args.x_column
    y_column = args.y_column
    valueset = args.valueset
    systematic_error = args.systematic_error

    string = Guitarstring(excelpath)
    statistics = Statistics(valueset)

    print(string.resonancefit_params(taskindex, x_column, y_column))

    print(statistics.std_mean())
    print(statistics.std_dev())
    print(statistics.confidence_interval())

