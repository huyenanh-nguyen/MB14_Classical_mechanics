import argparse
from pathlib import Path, PurePath
from stringvibration import Guitarstring
from MathKit import Statistics
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FormatStrFormatter
from scipy.optimize import curve_fit

def linearfit(x, m, b):
    return m * x + b

def originfit(x, m):
    return m * x

# terminal script:

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "String Vibration")
    parser.add_argument("excelpath", type = str, help = "Path to the Excelfile -> M12_Saitenschwingung.xlsx")
    parser.add_argument("taskindex", type = int, help = "index of the task -> Task1 = 0 & 1, Task2 = 2, Task3 = 3, Task 4 = 4")
    parser.add_argument("x_column", type = str, help = "column name of the x values -> n is mostly the x_column")
    parser.add_argument("y_column", type = str, help = "column name of the y values -> fn is mostly the y_column")
    parser.add_argument("valueset", type = str, help = "name of the Valueset (like : fn in Hz)")
    parser.add_argument("systematic_error_frequence", type = float, help = "systematic error of the measuring tool -> ±0.02 Hz of the oscilloscop, 0.01 m of the ruler ")
    parser.add_argument("systematic_error_ruler", type = float, help = "systematic error of the measuring tool -> ±0.02 Hz of the oscilloscop, 0.01 m of the ruler ")
    args = parser.parse_args()  # collects all arguments


    excelpath = PurePath(str(Path.cwd()) + "/" + (args.excelpath))
    taskindex = args.taskindex
    x_column = args.x_column
    y_column = args.y_column
    valueset = args.valueset
    systematic_error_frequence = args.systematic_error_frequence
    systematic_error_ruler = args.systematic_error_ruler

    roundnum = 3
    string = Guitarstring(excelpath)
    data = string.excel_dataframes()[taskindex]
    x_value = data["F0 in N"] 
    y_value = [np.sqrt(data["f1 in Hz"][i]) for i in range(len(x_value))]

    print(string.resonancefit_params(taskindex, x_column, y_column))

    popt, pcov = curve_fit(linearfit, x_value, y_value)
    residuals = y_value - linearfit(np.asarray(x_value), *popt)
    ss_res = np.sum(residuals ** 2)
    ss_total = np.sum((y_value - np.mean(y_value)) ** 2)
    r_square = 1 - (ss_res / ss_total)


    ppt, cov = curve_fit(originfit, x_value, y_value)

    print("intercept:", popt, "std:", np.sqrt(np.diag(pcov)), r_square)
    print("_____________________________________")
    print("origin:",ppt, "std:", np.sqrt(np.diag(cov)))



    fig = plt.figure()

    plt.scatter(x = x_value, y = y_value, marker = ".")
    plt.plot(x_value, originfit(x_value, np.array(ppt[0])), color = "tab:orange")
    plt.plot(x_value, linearfit(x_value, np.array(popt[0]), np.array(popt[1])), color = "tab:blue")

    plt.show()

    # python3 runtask4.py M12_Saitenschwingung.xlsx 4 "F0 in N" "f1 in Hz" "f1 in Hz" 0.03 0.01