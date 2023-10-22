from MathKit.statsengine import Statistics
import pandas as pd
import numpy as np
from numpy import sqrt
import matplotlib.pyplot as plt
from pathlib import PurePath, Path
from scipy.interpolate import approximate_taylor_polynomial
from scipy.optimize import curve_fit

class Pendulum:
    """
    Well using Jupyter Notebook is quite annoying.

    I dont want to spend to many time on this project, I will use the Excelfile as input.
    This Excelfile is already prepared for the analysis and the layout shouldn't change.
    This code is very specific for this Excelfile in this Pendulum-folder and will not work for other Excelfiles.
    But for someone who doesn't like the layout of the Excelfile, it is possible to change the code. 

    The important Parameter is the Path to the Excelfile!
    """

    def __init__(self, excelpath):
        """
        Args:
            excelpath(Path): Path to my Excelfile
        """

        self.excel = excelpath


    def excel_to_df(self):
        """
        skipping enough rows, so it begins and ends on the right row where I put the table.

        Returns:
            List: List with three Dataframes -> first Item is for task 1, second Item is for the longest and shortest length of the pendulum, where 
                  we measured 10 times 10 periods and the last Item is for task 3
        """

        excel = self.excel
        task1_excelsheeet = pd.read_excel(excel, sheet_name = "Rohdaten", skiprows=2).iloc[0:10].dropna(axis = 'columns') 
        task3a_excelsheet = pd.read_excel(excel, sheet_name = "Rohdaten", skiprows=19).iloc[0:10].dropna(axis = 'columns') 
        task3b_excelsheet = pd.read_excel(excel, sheet_name = "Rohdaten", skiprows=37).iloc[0:10].dropna(axis = 'columns')

        return [task1_excelsheeet, task3a_excelsheet, task3b_excelsheet]


    def equilibrium_period_stats(self):
        """
        Calculation the neccessary statistical parameters for the Period at the equilibrium point.

        Returns:
            List: [Mean of Period at the equilibrium point, standard deviation of the mean, confidence interval of the mean]
        """

        excel = self.excel_to_df()[0]["T(Nullpunkt) in s"]
        stats = Statistics(excel)

        period_mean = stats.std_mean()
        period_stddev = stats.std_dev()
        period_cov = stats.confidence_interval()

        return [period_mean, period_stddev, period_cov]
    

    def turningpoint_period_stats(self):
        """
        Calculation the neccessary statistical parameters for the Period at the turning point.

        Returns:
            List: [Mean of Period at the turning point, standard deviation of the mean, confidence interval of the mean]
        """

        excel = self.excel_to_df()[0]["T(Umkehrpunkt) in s"]
        stats = Statistics(excel)

        period_mean = stats.std_mean()
        period_stddev = stats.std_dev()
        period_cov = stats.confidence_interval()

        return [period_mean, period_stddev, period_cov]




excelpath = PurePath(str(Path.cwd()) + "/Pendulum/F3_Fadenpendel.xlsx")
test = Pendulum(excelpath)
print(test.equilibrium_period_stats())
print(test.turningpoint_period_stats())







