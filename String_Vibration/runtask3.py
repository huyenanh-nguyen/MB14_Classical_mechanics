import argparse
from pathlib import Path, PurePath
from stringvibration import Guitarstring
from MathKit import Statistics
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FormatStrFormatter
from scipy.optimize import curve_fit

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


    roundnum = 3
    string = Guitarstring(excelpath)

    
    statisticset = string.excel_dataframes()[taskindex][valueset]   # Valuelist for each "fn in Hz" column

    statistics = Statistics(statisticset)
    

    dataset = string.excel_dataframes()[taskindex]

    # curve_fit 
    x_value = dataset[x_column]
    y_value = [(1 / dataset[y_column][i]) for i in range(len(dataset[y_column]))]

    popt, pcov = curve_fit(linearfit, x_value, y_value)

    residuals = y_value - linearfit(np.asarray(x_value), *popt)
    ss_res = np.sum(residuals ** 2)
    ss_total = np.sum((y_value - np.mean(y_value)) ** 2)
    r_square = 1 - (ss_res / ss_total)

    std = np.sqrt(np.diag(pcov))

    slope = popt[0]  # slope of the fit
    std_slope = std[0]
    stringlength = dataset["L in m"].unique()[0]    # length of the string
    mass = dataset["M in kg"].unique()[0]
    
    print("_______________________________________________________")
    print(" ")
    print(" Task 3 ")
    print(" ")
    print("Fit Parameters:")
    
    fit_dict = {"slope" : f"{slope: .3f} \u00B1 " + f"{std_slope: .3f} Hz" , "c": f"{2 / slope : 0.3f}", "M" : f"{mass: 0.3f} kg"}
    print(pd.DataFrame(fit_dict, index=[0]))
    print(" ")
    print("_______________________________________________________")
    print(" ")

    legendtext =(
    "f(n) = (" + f"{popt[0] : .3f} \u00B1" + f"{std[0] : .3f} ) n" + 
    "\n$R^2$ = " + f"{r_square : 0.3f}"
    )

    x_value = np.linspace(0, dataset["L in m"].max())
    frequence = y_value
    mode = dataset["L in m"]
    fig = plt.figure()
    ax = fig.add_subplot()
    plt.scatter(x = mode, y = frequence, marker = ".")

    plt.plot(x_value, linearfit(x_value, np.array(popt[0])), label = legendtext, color = "tab:orange")


    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)
    plt.legend(loc = 'upper left')
    plt.xlabel("L in m", fontsize=12)
    plt.ylabel(r'$\frac{1}{f_1}$ in $\frac{1}{Hz}$', fontsize=12)
    
   
    
    plt.show()




# python3 runtask3.py M12_Saitenschwingung.xlsx 3 "L in m" "f1 in Hz" "f1 in Hz" 0.03 0.01