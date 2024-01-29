import numpy as np
import pandas as pd
import openpyxl
from pathlib import Path, PurePath
from scipy.optimize import curve_fit
from MathKit import Statistics

class Wheatstone:
    
    def __init__(self, excelpath, task1, task2):
        """
        Args:
            excelpath (Path): PAth to my excelfile
        """
        self.excelpath = excelpath
        self.excelsheet_task1 = task1
        self.excelsheet_task2 = task2


    def excelsheet_to_dataframe(self):
        """
        Returns:
            Dataframe: returns the two sheets as Dataframes
        """
        excel = self.excelpath
        sheetname1 = self.excelsheet_task1
        sheetname2 = self.excelsheet_task2
        sheet1 = pd.read_excel(excel, sheet_name = sheetname1, skiprows= 1).dropna(axis = 1, how = "all")
        sheet2 = pd.read_excel(excel, sheet_name = sheetname2, skiprows= 1).dropna(axis = 1, how = "all")

        return sheet1, sheet2   
    

    def task1_dataframe(self):
        """
        In Task 1 we should do a scatterplot of the volatage and current.
        while the lecturer set a volatage at the voltage supply, we measured the voltage and the current with a voltmeter and an Ammeter and we want
        to understand the electrical resistance of the instrument or the electrical network itself.
        (Two way how we assembled the network -> Spannungsrichtig: placing the instrument, so we get the right voltage-value and 
                                                 Stromrichtig: placing the instrument, so we get the right current-values)

        Returns:
            Dataframe: returns Dataframe with the current- and voltage-data
        """
        sheet_df = self.excelsheet_to_dataframe()[0]
        columnheader = [sheet_df.columns]
   
        spannungsrichtig = sheet_df.loc[0:, [columnheader[0][i] for i in range(3)]]
        spannungsrichtig.columns = spannungsrichtig.iloc[0]
        

        return spannungsrichtig








excelpath = PurePath(str(Path.cwd()) + "/E2_Wheatstone_bridge.xlsx")
sheet1 = "Aufgabe 1"
sheet2 = "Aufgabe 2"

results = Wheatstone(excelpath = excelpath, task1 = sheet1, task2 = sheet2)

print(results.task1_dataframe())

    