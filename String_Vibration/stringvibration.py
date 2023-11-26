import numpy as np
import pandas as pd
import openpyxl
from pathlib import Path, PurePath
from scipy.optimize import curve_fit
from MathKit import Statistics

def search(header : pd.DataFrame, substring: str, case: bool=False):
    list_series = [header[col].astype(str).str.contains(substring.lower(), case = case, na = False) for col in header]
    mask = np.column_stack(list_series)
    return header.loc[mask.any(axis = 1)]


def linearfit(x, m, b):
    return m * x + b


class Guitarstring:
    """
    Observing transversal waves on a string, which is fixed on both ends.
    
    """

    def __init__(self, excelpath):
        """
        Args:
            excelpath (Path): PAth to my excelfile
        """
        self.excelpath = excelpath

    
    def excel_dataframes(self):
        """getting the data from the excel file.
        Task1 contains two tables. Task2 contains three tables. Task3 and Task4 contain one table each.
        
        Task1: Table 1: 9 different frequencies at fix length of the string, fix force, for nine different modes 
               Table 2: position of the nodes for mode 3 and 4 (n = 2, 3)
        
        Task2: Table 1: 9 different frequencies at fix length of the string for nine different modes by changing the force (total 3 forces -> 3 tables)

        Task3: Table 1: Resonancefrequency of the 1st harmonic for different lengths of the string, fix force

        Task4: Table 1: Resonancefrequency of the 1st harmonic for 8 different forces, fix length of the string

        Returns:
            List: List full of dataframes
        """
        excel = self.excelpath
        task1_table1 = pd.read_excel(excel, sheet_name = "Task 1", skiprows=3).iloc[0:9,np.arange(1,5)].dropna(axis = 0, how = 'all')
        task1_table2 = pd.read_excel(excel, sheet_name = "Task 1", skiprows=17).iloc[0:10,np.arange(1,4)].dropna(axis = 0, how = 'all')

        task2 = pd.read_excel(excel, sheet_name = "Task 2", skiprows=3).dropna(axis = 1, how = 'all')
        col_header = []

        for i in range(3):
            if i == 0:
                col_header.append("fn in Hz")

            else:
                col_header.append("fn in Hz" + "." + str(i))

        col_index = [task2.columns.get_loc(col_header[i]) for i in range(3)]    # columnindex for the header "fn in Hz"

        task2_dataframes = []   # contains all tables in a list

        for i in col_index:
            task2_dataframes.append(task2.iloc[:,i : i+4])

        task3 = pd.read_excel(excel, sheet_name = "Task 3", skiprows=2).dropna(axis = 1, how = 'all')
        task4 = pd.read_excel(excel, sheet_name = "Task 4", skiprows=2).dropna(axis = 1, how = 'all')

        return [task1_table1,task1_table2, task2_dataframes, task3, task4]


    def resonancefit_params(self, taskindex, x_column, y_column):

        data = self.excel_dataframes()[taskindex]
        x_value = data[x_column]
        y_value = data[y_column]
        
        popt, pcov = curve_fit(linearfit, x_value, y_value)

        residuals = y_value - linearfit(np.asarray(x_value), *popt)
        ss_res = np.sum(residuals ** 2)
        ss_total = np.sum((y_value - np.mean(y_value)) ** 2)
        r_square = 1 - (ss_res / ss_total)
        return popt, pcov, r_square




############
# examples #
############

excel = PurePath(str(Path.cwd()) + "/M12_Saitenschwingung.xlsx")

string = Guitarstring(excel)

print(string.resonancefit_params(0, "n", "fn in Hz"))


########
# test

