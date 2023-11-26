import numpy as np
import pandas as pd
import openpyxl
from pathlib import Path, PurePath
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
        excel = self.excelpath
        task1_table1 = pd.read_excel(excel, sheet_name = "Task 1", skiprows=3).iloc[0:10,np.arange(1,5)]
        task1_table2 = pd.read_excel(excel, sheet_name = "Task 1", skiprows=17).iloc[0:10,np.arange(1,4)]

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


    # def resonancefit(self):



############
# examples #
############

excel = PurePath(str(Path.cwd()) + "/M12_Saitenschwingung.xlsx")

string = Guitarstring(excel)

print(string.excel_dataframes()[4])


########
# test

