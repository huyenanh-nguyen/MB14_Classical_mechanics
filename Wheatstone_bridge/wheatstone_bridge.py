import numpy as np
import pandas as pd
import openpyxl
from pathlib import Path, PurePath
from scipy.optimize import curve_fit
from MathKit import Statistics

class Wheatstone:
    
    def __init__(self, excelpath):
        """
        Args:
            excelpath (Path): PAth to my excelfile
        """
        self.excelpath = excelpath
    

    