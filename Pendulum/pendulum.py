from MathKit.statsengine import Statistics
import pandas as pd
import numpy as np
from numpy import sqrt
import matplotlib.pyplot as plt
from scipy.interpolate import approximate_taylor_polynomial
from scipy.optimize import curve_fit
from pathlib import Path, PurePath

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

    ############################
    #         task 1           #
    ############################ 

    def equilibrium_period_stats(self):
        """
        Calculation the neccessary random statistical parameters for the Period at the equilibrium point.

        Returns:
            List: [Mean of Period at the equilibrium point, standard deviation of the mean, confidence interval of the mean]
        """

        excel = self.excel_to_df()[0]["T(Nullpunkt) in s"]
        stats = Statistics(excel)

        period_mean = stats.std_mean()
        period_stddev = stats.std_dev()
        period_cov = stats.confidence_interval()

        return [period_mean, period_stddev, period_cov]
    

    def equilibrium_period_total_err(self, systematic_error):
        """calculating the total uncertainty of the period at the equilibrium point

        Args:
            systematic_error (int, value): systematic error of the offset from my instrument. In this case the last digit of the timer

        Returns:
            Int: total uncertainty of the period at the equilibrium point
        """

        excel = self.excel_to_df()[0]["T(Nullpunkt) in s"]
        stats = Statistics(excel)

        return stats.total_uncertainty_value(systematic_error)
    

    def turningpoint_period_stats(self):
        """
        Calculation the neccessary random statistical parameters for the Period at the turning point.

        Returns:
            List: [Mean of Period at the turning point, standard deviation of the mean, confidence interval of the mean]
        """

        excel = self.excel_to_df()[0]["T(Umkehrpunkt) in s"]
        stats = Statistics(excel)

        period_mean = stats.std_mean()
        period_stddev = stats.std_dev()
        period_cov = stats.confidence_interval()

        return [period_mean, period_stddev, period_cov]
    

    def turningpoint_period_total_err(self, systematic_error):
        """calculating the total uncertainty of the period at the turning point

        Args:
            systematic_error (int, value): systematic error of the offset from my instrument. In this case the last digit of the timer

        Returns:
            Int: total uncertainty of the period at the turning point
        """

        excel = self.excel_to_df()[0]["T(Umkehrpunkt) in s"]
        stats = Statistics(excel)

        return stats.total_uncertainty_value(systematic_error)
    
    ############################
    #         task 3           #
    ############################

    # measuring 10 Periods 10 times for the longest and shortest pendulum length
    # Index 1 will be the longest length and Index 10 will be the shortest length
    # each period must be divided by 10 and then can be use here.
    # the largest standard deviation will be use for the rest of the length 


    def shortest_period_stats(self):

        excel = self.excel_to_df()[1]["Tkürzeste,10 durch 10 in s"]
        stats = Statistics(excel)

        period_mean = stats.std_mean() 
        period_stddev = stats.std_dev() 
        period_cov = stats.confidence_interval() 

        return [period_mean, period_stddev, period_cov]
    

    def longest_period_stats(self):

        excel = self.excel_to_df()[1]["Tlängste,1 durch 10 in s"]
        stats = Statistics(excel)

        period_mean = stats.std_mean() 
        period_stddev = stats.std_dev()
        period_cov = stats.confidence_interval() 

        return [period_mean, period_stddev, period_cov]
    

    # measuring 10 periods for 10 different pendulum length
    # I guess calculating the Errors would be easier if it is made in excel
    # so here will be the part where we just plot the grapf


