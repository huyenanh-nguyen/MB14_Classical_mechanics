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


    roundnum = 2
    string = Guitarstring(excelpath)

    
    statisticset = [string.excel_dataframes()[taskindex][i][valueset] for i in range(3)]    # Valuelist for each "fn in Hz" column

    statistics = [Statistics(statisticset[i]) for i in range(3)]
    

    dataset = string.excel_dataframes()[taskindex]

    fit_params = string.resonancefit_params(taskindex, x_column, y_column)

    slope = [fit_params[i]["slope"][0] for i in range(3)]  # slope of the fit
    std_slope = [fit_params[i]["std_slope"][0] for i in range(3)]
    stringlength = [dataset[i]["L in m"].unique()[0] for i in range(3)]    # length of the string
    mass = [dataset[i]["M in kg"].unique()[0] for i in range(3)]
    f0 = [dataset[i]["F0 in N"].unique()[0] for i in range(3)]
    f = [dataset[i]["fn in Hz"].unique()[0] for i in range(3)]

    print("_______________________________________________________")
    print(" ")
    print(" Task 2 ")
    print(" ")
    print("Fit Parameters:")
    
    

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

    breakpoint()

    # stdev_mu_c = []
    # for i in range(3):
    #     stdev_mu_c.append(string.std_mu_and_c(stringlength[i], f[i], c[i],f0[i],0.03, 0.01, std_slope[i]))
    # print(stdev_mu_c)

    # individual plots

    for i in range(3):
        legendtext =(
            "f(n) = (" + f"{slope[i] : .3f} \u00B1" + f"{std_slope[i] : .3f} ) n" + 

            "\n$R^2$ = " + f"{fit_params[i]['R_Square'][0] : 0.3f}"
            )
    
        x_value = np.linspace(0, dataset[i]["n"].max())
        frequence = dataset[i]["fn in Hz"]
        mode = dataset[i]["n"]
        fig = plt.figure()
        ax = fig.add_subplot()
        plt.scatter(x = mode, y = frequence, marker = ".")

        plt.plot(x_value, linearfit(x_value, np.array(slope[i])), label = legendtext, color = "tab:orange")


        ax.set_ylim(ymin=0)
        ax.set_xlim(xmin=0)
        plt.legend(loc = 'upper left')
        plt.xlabel("n", fontsize=12)
        plt.ylabel("$f_n$ in Hz", fontsize=12)
    
    # plt.show()

    # combined plots

    legendtext_1 =(
            "f$_{M = 1.0kg}$(n) = ("+ f"{slope[0] : .2f} \u00B1" + f"{std_slope[0] : .2f} ) n" + 
            "\n$R^2$ = " + f"{fit_params[0]['R_Square'][0] : 0.4f}"
            )
    legendtext_2 =(
            "f$_{M = 2.0kg}$(n) = ("+ f"{slope[1] : .2f} \u00B1" + f"{std_slope[1] : .2f} ) n" + 
            "\n$R^2$ = " + f"{fit_params[1]['R_Square'][0] : 0.4f}"
            )
    legendtext_3 =(
            "f$_{M = 3.0kg}$(n) = ("+ f"{slope[2] : .2f} \u00B1" + f"{std_slope[2] : .2f} ) n" + 
            "\n$R^2$ = " + f"{fit_params[2]['R_Square'][0] : 0.4f}"
            )
    
    x_value = np.linspace(0, dataset[0]["n"].max())

    frequence_1 = dataset[0]["fn in Hz"]
    frequence_2 = dataset[1]["fn in Hz"]
    frequence_3 = dataset[2]["fn in Hz"]

    mode_1 = dataset[0]["n"]
    mode_2 = dataset[1]["n"]
    mode_3 = dataset[2]["n"]
    fig = plt.figure()
    ax = fig.add_subplot()
    plt.scatter(x = mode_1, y = frequence_1, marker = ".")
    plt.scatter(x = mode_2, y = frequence_2, marker = ".")
    plt.scatter(x = mode_3, y = frequence_3, marker = ".")

    plt.plot(x_value, linearfit(x_value, np.array(slope[0])), label = legendtext_1)
    plt.plot(x_value, linearfit(x_value, np.array(slope[1])), label = legendtext_2)
    plt.plot(x_value, linearfit(x_value, np.array(slope[2])), label = legendtext_3)
    
    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)
    plt.legend(loc = 'upper left')
    plt.xlabel("n", fontsize=12)
    plt.ylabel("$f_n$ in Hz", fontsize=12)
    
    plt.show()


# python3 runtask2.py M12_Saitenschwingung.xlsx 2 "n" "fn in Hz" "fn in Hz" 0.03 0.01