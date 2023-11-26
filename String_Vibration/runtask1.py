import argparse
from pathlib import Path, PurePath
from stringvibration import Guitarstring
from MathKit import Statistics
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

def linearfit(x, m, b):
    return m * x + b

# terminal script:

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "String Vibration")
    parser.add_argument("excelpath", type = str, help = "Path to the Excelfile")
    parser.add_argument("taskindex", type = int, help = "index of the task")
    parser.add_argument("x_column", type = str, help = "column name of the x values")
    parser.add_argument("y_column", type = str, help = "column name of the y values")
    parser.add_argument("valueset", type = str, help = "name of the Valueset (like : fn in Hz)")
    parser.add_argument("systematic_error", type = float, help = "systematic error of the measuring tool")
    args = parser.parse_args()  # collects all arguments


    excelpath = PurePath(str(Path.cwd()) + "/" + (args.excelpath))
    taskindex = args.taskindex
    x_column = args.x_column
    y_column = args.y_column
    valueset = args.valueset
    systematic_error = args.systematic_error

    string = Guitarstring(excelpath)

    statsticset = string.excel_dataframes()[taskindex][valueset]
    statistics = Statistics(statsticset)

    dataset = string.excel_dataframes()[taskindex]
    fit_params = string.resonancefit_params(taskindex, x_column, y_column)

    print(fit_params)

    roundnum = 3
    print("dont know if we need that:")
    print("f_n(mean) in Hz : ", round(statistics.std_mean(), roundnum))
    print("f_n(sdt) in Hz : ",round(statistics.std_dev(), roundnum))
    print("f_n(confidenveinterval) in Hz : ",round(statistics.confidence_interval(), roundnum))


    legendtext = "y = ("  + str(round(fit_params["slope"][0], roundnum)) +  u" \u00B1 " + str(round(fit_params["std_slope"][0], roundnum)) + ") x (" + str(round(fit_params["y_inter"][0], roundnum))  + u" \u00B1 " + str(round(fit_params["std_inter"][0], roundnum)) + ") \n$R^2$ = " + str(round(fit_params["R_Square"][0], roundnum))
                  
    x_value = np.linspace(0, dataset["n"].max())
    frequence = dataset["fn in Hz"]
    mode = dataset["n"]

    fig = plt.figure()
    ax = fig.add_subplot()
    plt.scatter(x = mode, y = frequence, marker = ".")

    plt.plot(x_value, linearfit(x_value, np.array(fit_params["slope"]), np.array(fit_params["y_inter"])), label = legendtext, color = "tab:orange")


    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)
    plt.legend(loc = 'upper left')
    plt.xlabel("n", fontsize=12)
    plt.ylabel("$f_n$ in Hz", fontsize=12)
    plt.show()

    print(legendtext)