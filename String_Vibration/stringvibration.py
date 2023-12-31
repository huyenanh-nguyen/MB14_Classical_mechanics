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


def linearfit(x, m):
    return m * x

def task4_fit(Fo, n, L, µ):
    return (n / 2*L) * np.sqrt((Fo / µ))


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

        Task3: Table 1: Resonancefrequency of the fundemental frequency for different lengths of the string, fix force

        Task4: Table 1: Resonancefrequency of the fundemental frequency for 8 different forces, fix length of the string

        Returns:
            List: List full of dataframes
        """
        excel = self.excelpath
        task1_table1 = pd.read_excel(excel, sheet_name = "Task 1", skiprows=3).iloc[0:9,np.arange(1,6)].dropna(axis = 0, how = 'all')
        task1_table2 = pd.read_excel(excel, sheet_name = "Task 1", skiprows=17).iloc[0:10,np.arange(1,4)].dropna(axis = 0, how = 'all')

        # Start Task 2
        # Task 2 has three same table, that has the same length and sam columnheader. But because of that, I have to write a slightly different code
        # then for the other Tasks. For example, Pandas would rename the columnheader from "fn in Hz, fn in Hz, fn in Hz" to "fn in Hz, fn in Hz.1, fn in Hz.2"
        # which is not ideal for a simple use ... so i have to rename the columnheader.
        # I hope it is not too confusing from here.
        columnheader = pd.read_excel(excel, sheet_name= "Task 2", header = None, skiprows=3).dropna(axis = 1, how = "all").values[0]
        table = pd.read_excel(excel, sheet_name= "Task 2", header = None, skiprows=4).dropna(axis = 1, how = "all")
        table.columns = columnheader

        col_index = [0, 5, 10] # columnindex for the header "fn in Hz" 

        task2_dataframes = []   # contains all tables in a list

        for i in col_index:
            task2_dataframes.append(table.iloc[:,i : i+5])

        # End Task 2


        task3 = pd.read_excel(excel, sheet_name = "Task 3", skiprows=3).dropna(axis = 1, how = 'all')
        task4 = pd.read_excel(excel, sheet_name = "Task 4", skiprows=3).dropna(axis = 1, how = 'all')

        return [task1_table1,task1_table2, task2_dataframes, task3, task4]


    def resonancefit_params(self, taskindex : int, x_column : str, y_column : str):
        """Collection of the fit parameters.
        For Task 2 there will be a list for each table (there are 3)

        Args:
            taskindex (int): index of the task -> Task1 = 0 & 1, Task2 = 2, Task3 = 3, Task 4 = 4
            x_column (str): Name of the Column where the x_values are
            y_column (str): Name of the Column where the y_values are

        Returns:
            DataFrame: Returning slope, y_interception, standard deviation of those two parameters and R_Square from the linear fit 
                        >>>     slope   y_inter  std_slope  std_inter  R_Square
                            0  164.85 -4.916668   0.105221    0.59211  0.999997
        """

        data = self.excel_dataframes()[taskindex]
        if taskindex != 2:
            x_value = data[x_column]
            y_value = data[y_column]

            popt, pcov = curve_fit(linearfit, x_value, y_value)

            residuals = y_value - linearfit(np.asarray(x_value), *popt)
            ss_res = np.sum(residuals ** 2)
            ss_total = np.sum((y_value - np.mean(y_value)) ** 2)
            r_square = 1 - (ss_res / ss_total)

            std = np.sqrt(np.diag(pcov))

            data = {"slope": popt[0], "std_slope": std[0], "R_Square": r_square}
            resonancefit = pd.DataFrame(data, index=[0])

            return resonancefit

        else:
            
            x_list = []
            y_list = []
            for i in range(3):
                x_list.append(data[i][x_column])
                y_list.append(data[i][y_column])
            
            
            
            resonance_list = []

            for i in range(3):

                popt, pcov = curve_fit(linearfit, x_list[i], y_list[i])

                residuals = y_list[i] - linearfit(np.asarray(x_list[i]), *popt)
                ss_res = np.sum(residuals ** 2)
                ss_total = np.sum((y_list[i] - np.mean(y_list[i])) ** 2)
                r_square = 1 - (ss_res / ss_total)

                std = np.sqrt(np.diag(pcov))

                data = {"slope": popt[0], "std_slope": std[0], "R_Square": r_square}
                resonancefit = pd.DataFrame(data, index=[0])
                resonance_list.append(resonancefit)



            return resonance_list
        

    def task4_fit_params(self, taskindex : int, x_column : str, y_column : str):
        """there is a another way to fit the data.
        In Task 4 we should use this fit f(n) = (n / 2*L) * np.sqrt(F0 / µ)

        Args:
            taskindex (int): index of the task -> Task1 = 0 & 1, Task2 = 2, Task3 = 3, Task 4 = 4
            x_column (str): Name of the Column where the x_values are
            y_column (str): Name of the Column where the y_values are

        Returns:
            List: _description_
        """
        data = self.excel_dataframes()[taskindex]
        x_value = data[x_column]
        y_value = data[y_column]

        popt, pcov = curve_fit(task4_fit, x_value, y_value)
        residuals = y_value - task4_fit(np.asarray(x_value), *popt)
        ss_res = np.sum(residuals ** 2)
        ss_total = np.sum((y_value - np.mean(y_value)) ** 2)
        r_square = 1 - (ss_res / ss_total)

        std = np.sqrt(np.diag(pcov))

        return  "popt:", popt, "std:" , std, "R_square:",  r_square
    
    def std_mu_and_c(self, L: float, f: float, c : float, f0 : float, delta_f: float, delta_L: float, delta_f0 : float):
        """_summary_

        Args:
            L (float): stringlength
            f (float): frequence
            c (float): _description_
            f0 (float): tension
            delta_f (float): _description_
            delta_L (float): _description_
            delta_f0 (float): _description_
        """
        delta_c = np.sqrt( ((2 * (L) * delta_f)**2) + ((f * delta_L)**2) )
        delta_mu = np.sqrt( ((-2 * f0 * delta_c)**2) + ((c**(-2) * delta_f0)**2) )
        return delta_c, delta_mu
    
    def mu_c_pt2(self, M, c, L, f1, delta_f1, delta_L):
        delta_c = np.sqrt( (2* L * delta_f1)**2 + (2 * f1 * delta_L)**2 )
        delta_mu = np.sqrt( (-2 * M * 9.81 * (c)**(-3) * delta_c)**2 )
        
        return "∆c:", delta_c, "∆µ:", delta_mu


############
# examples #
############

excel = PurePath(str(Path.cwd()) + "/M12_Saitenschwingung.xlsx")

string = Guitarstring(excel)

# print(string.excel_dataframes()[2][2])
# print(string.resonancefit_params(3, "fn in Hz", "F0 in N"))


########
# test

# columnheader = pd.read_excel(excel, sheet_name= "Task 2", header = None, skiprows=3).dropna(axis = 1, how = "all").values[0]
# table = pd.read_excel(excel, sheet_name= "Task 2", header = None, skiprows=4).dropna(axis = 1, how = "all")
# table.columns = columnheader
# print(table)
