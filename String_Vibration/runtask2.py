import argparse
from pathlib import Path, PurePath
from stringvibration import Guitarstring
from MathKit import Statistics
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FormatStrFormatter

def linearfit(x, m):
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


    # some standard parameter and raw data variables
    roundnum = 2
    string = Guitarstring(excelpath)    # calling class

    # for this task we had to measure the frequency for three different mass -> there are three tables with data.

    statisticset = [string.excel_dataframes()[taskindex][i][valueset] for i in range(3)]    # Valuelist for each "fn in Hz" column

    statistics = [Statistics(statisticset[i]) for i in range(3)]    # for standard deviation
    dataset = string.excel_dataframes()[taskindex]     # the three tabels with the raw data as list

    fit_params = string.resonancefit_params(taskindex, x_column, y_column)

    slope = [fit_params[i]["slope"][0] for i in range(3)]  # slope of the fit
    std_slope = [fit_params[i]["std_slope"][0] for i in range(3)]
    stringlength = [dataset[i]["L in m"].unique()[0] for i in range(3)]    # length of the string
    mass = [dataset[i]["M in kg"].unique()[0] for i in range(3)]
    f0 = [dataset[i]["F0 in N"].unique()[0] for i in range(3)]
    f = [dataset[i]["fn in Hz"].unique()[0] for i in range(3)]
    
    
    
    
    # f0 /c ** 2
    fit_dict = {"slope" : {}, "c" : {}, "µ" : {}, "M" : {}, "F0" : {}}
    c = []
    for i in range(3):
        fit_dict["slope"][i] =  f"{slope[i] : .3f} \u00B1" + f"{std_slope[i] : .3f} Hz"
        fit_dict["c"][i] = f"{slope[i] * 2 * stringlength[i] : .3f} m/s"
        fit_dict["µ"][i] = f"{f0[i] / (slope[i] * 2 * stringlength[i]) ** 2: .3f} kg/m"
        fit_dict["M"][i] = f"{mass[i] : .3f} kg"
        fit_dict["F0"][i] = f"{f0[i] : .3f} kg"
        c.append(slope[i] * 2 * stringlength[i])
    
    fit_df = pd.DataFrame(fit_dict)
    print(" ")
    print("_______________________________________________________")
    print(fit_df)

    delta_total_f1 = [np.sqrt( (0.03)**2 + (std_slope[i])** 2) for i in range(3)]

    stdev_mu_c_2 = []
    for i in range(3):
        stdev_mu_c_2.append(string.mu_c_pt2(mass[i], c[i], stringlength[i], slope[i], delta_total_f1[i], 0.01))
    print(stdev_mu_c_2)




    # python3 runtask2.py M12_Saitenschwingung.xlsx 2 "n" "fn in Hz" "fn in Hz" 0.03 0.01