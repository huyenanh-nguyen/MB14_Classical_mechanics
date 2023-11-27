import argparse
from pathlib import Path, PurePath
from stringvibration import Guitarstring
from MathKit import Statistics
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FormatStrFormatter

def linearfit(x, m, b):
    return m * x + b

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

    
    statisticset = [string.excel_dataframes()[taskindex][i][valueset] for i in range(3)]    # Valuelist for each "fn in Hz" column

    statistics = [Statistics(statisticset[i]) for i in range(3)]
    

    dataset = string.excel_dataframes()[taskindex]

    fit_params = string.resonancefit_params(taskindex, x_column, y_column)

    slope = [fit_params[i]["slope"][0] for i in range(3)]  # slope of the fit
    std_slope = [fit_params[i]["std_slope"][0] for i in range(3)]
    stringlength = [dataset[i]["L in m"].unique()[0] for i in range(3)]    # length of the string
    mass = [dataset[i]["M in kg"].unique()[0] for i in range(3)]

    print("_______________________________________________________")
    print(" ")
    print("Fit Parameters:")
    
    fit_dict = {"slope" : {}, "c" : {}, "µ" : {}, "M" : {}}
    for i in range(3):
        fit_dict["slope"][i] =  f"{slope[i] : .3f} \u00B1" + f"{std_slope[i] : .3f} Hz"
        fit_dict["c"][i] = f"{slope[i] * 2 * stringlength[i] : .3f} m/s"
        fit_dict["µ"][i] = f"{mass[i] / stringlength[i]: .3f} kg/m"
        fit_dict["M"][i] = f"{mass[i] : .3f} kg"

    fit_df = pd.DataFrame(fit_dict)
    print(" ")
    print("_______________________________________________________")
    print(fit_params)

    # individual plots

    for i in range(3):
        legendtext =(
            "y = (" + f"{slope[i] : .3f} \u00B1" + f"{std_slope[i] : .3f} ) x (" + 
            f"{fit_params[i]['y_inter'][0] : 0.3f} \u00B1" + f"{fit_params[i]['std_inter'][0]: 0.3f} ) " + 
            "\n $R^2$ = " + f"{fit_params[i]['R_Square'][0] : 0.3f}"
            )
    
        x_value = np.linspace(0, dataset[i]["n"].max())
        frequence = dataset[i]["fn in Hz"]
        mode = dataset[i]["n"]
        fig = plt.figure()
        ax = fig.add_subplot()
        plt.scatter(x = mode, y = frequence, marker = ".")

        plt.plot(x_value, linearfit(x_value, np.array(slope[i]), np.array(fit_params[i]["y_inter"][0])), label = legendtext, color = "tab:orange")


        ax.set_ylim(ymin=0)
        ax.set_xlim(xmin=0)
        plt.legend(loc = 'upper left')
        plt.xlabel("n", fontsize=12)
        plt.ylabel("$f_n$ in Hz", fontsize=12)
    
    # plt.show()

    # combined plots

    legendtext_1 =(
            "y(M=" + f"{mass[0]: 0.1f} kg ) = (" + f"{slope[0] : .3f} \u00B1" + f"{std_slope[0] : .3f} ) x (" + 
            f"{fit_params[0]['y_inter'][0] : 0.3f} \u00B1" + f"{fit_params[0]['std_inter'][0]: 0.3f} ) " + 
            "\n $R^2$ = " + f"{fit_params[0]['R_Square'][0] : 0.3f}"
            )
    legendtext_2 =(
            "y(M=" + f"{mass[1]: 0.1f} kg ) = (" + f"{slope[1] : .3f} \u00B1" + f"{std_slope[1] : .3f} ) x (" + 
            f"{fit_params[1]['y_inter'][0] : 0.3f} \u00B1" + f"{fit_params[1]['std_inter'][0]: 0.3f} ) " + 
            "\n $R^2$ = " + f"{fit_params[1]['R_Square'][0] : 0.3f}"
            )
    legendtext_3 =(
            "y(M=" + f"{mass[2]: 0.1f} kg ) = (" + f"{slope[2] : .3f} \u00B1" + f"{std_slope[2] : .3f} ) x (" + 
            f"{fit_params[2]['y_inter'][0] : 0.3f} \u00B1" + f"{fit_params[2]['std_inter'][0]: 0.3f} ) " + 
            "\n $R^2$ = " + f"{fit_params[2]['R_Square'][0] : 0.3f}"
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

    plt.plot(x_value, linearfit(x_value, np.array(slope[0]), np.array(fit_params[0]["y_inter"][0])), label = legendtext_1)
    plt.plot(x_value, linearfit(x_value, np.array(slope[1]), np.array(fit_params[1]["y_inter"][0])), label = legendtext_2)
    plt.plot(x_value, linearfit(x_value, np.array(slope[2]), np.array(fit_params[2]["y_inter"][0])), label = legendtext_3)
    
    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)
    plt.legend(loc = 'upper left')
    plt.xlabel("n", fontsize=12)
    plt.ylabel("$f_n$ in Hz", fontsize=12)
    
    plt.show()


    # legendtext = "y = ("  + str(round(slope, roundnum)) +  u" \u00B1 " + str(round(fit_params["std_slope"][0], roundnum)) + ") x (" + str(round(fit_params["y_inter"][0], roundnum))  + u" \u00B1 " + str(round(fit_params["std_inter"][0], roundnum)) + ") \n$R^2$ = " + str(round(fit_params["R_Square"][0], roundnum))
                  
    # x_value = np.linspace(0, dataset["n"].max())
    # frequence = dataset["fn in Hz"]
    # mode = dataset["n"]

    # fig = plt.figure()
    # ax = fig.add_subplot()
    # plt.scatter(x = mode, y = frequence, marker = ".")

    # plt.plot(x_value, linearfit(x_value, np.array(slope), np.array(fit_params["y_inter"][0])), label = legendtext, color = "tab:orange")


    # ax.set_ylim(ymin=0)
    # ax.set_xlim(xmin=0)
    # plt.legend(loc = 'upper left')
    # plt.xlabel("n", fontsize=12)
    # plt.ylabel("$f_n$ in Hz", fontsize=12)
    # plt.show()
