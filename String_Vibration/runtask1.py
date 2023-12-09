import argparse
from pathlib import Path, PurePath
from stringvibration import Guitarstring
from MathKit import Statistics
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

def linearfit(x, m):
    return m * x 

# terminal script:

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "String Vibration")
    parser.add_argument("excelpath", type = str, help = "Path to the Excelfile -> here M12_Saitenschwingung.xlsx")
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

    m_string = 0.01 # mass in kg


    string = Guitarstring(excelpath)

    statsticset = string.excel_dataframes()[taskindex][valueset]
    statistics = Statistics(statsticset)

    dataset = string.excel_dataframes()[taskindex]  # Index 0 is for the first table and Index 1 is for the second table of the sheet "task 1"
    fit_params = string.resonancefit_params(taskindex, x_column, y_column)

    slope = fit_params["slope"][0]  # slope of the fit
    stringlength = dataset["L in m"].unique()[0]    # length of the string


    print("_______________________________________________________")
    print(" ")
    print(" Task 1 ")
    print(" ")
    print(fit_params)
    print("_______________________________________________________")
    print(" ")

    roundnum = 2
    # fundemental frequency and propagation speed of the vibration

    print("_______________________________________________________")
    print(" ")

    m = 1   # mass in kg
    c = slope * 2 * stringlength
    f0 = dataset["F0 in N"].unique()[0]

    print("slope: ", round(slope, roundnum),u" \u00B1 ", round(fit_params["std_slope"][0], roundnum), " Hz")
    print("c = ", round(c, roundnum), " m/s")  
    print("µ(f0 / c^2) = ", round(f0 /c ** 2, 6), " kg/m")
    print("µ(slope,script) = ", round((f0 /(slope ** 2 * 4 * stringlength ** 2)), 6), " kg/m")

    print(" ")
    print("_______________________________________________________")
    print(" ")


    # wavelength for mode n = 3 and n = 4

    print("λ3 = ", round(stringlength * 2 / 3, roundnum), " m")
    print("λ4 = ", round(stringlength * 2 / 4, roundnum), " m")
    print(" ")
    print("_______________________________________________________")
    print(" ")


    # plot 
    legendtext = ("f(n) = ("  
                  + str(round(slope, roundnum)) +  u" \u00B1 " + str(round(fit_params["std_slope"][0], roundnum)) + ") n" 
                  + "\n$R^2$ = " + f"{fit_params['R_Square'][0]: 0.4f}")
                  
    x_value = np.linspace(0, 10)
    frequence = dataset["fn in Hz"]
    mode = dataset["n"]

    fig = plt.figure()
    ax = fig.add_subplot()
    plt.scatter(x = mode, y = frequence, marker = ".")

    plt.plot(x_value, linearfit(x_value, np.array(slope)), label = legendtext, color = "tab:orange")
    # plt.errorbar(x = mode, y= frequence, yerr = np.repeat(0.3, len(dataset["L in m"])),fmt=' ', capsize=3, color = "dimgrey")

    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)
    plt.legend(loc = 'upper left')
    plt.xlabel("n", fontsize=12)
    plt.ylabel("$f_n$ in Hz", fontsize=12)
    plt.show()


# python3 runtask1.py M12_Saitenschwingung.xlsx 0 "n" "fn in Hz" "fn in Hz" 0.03 0.01